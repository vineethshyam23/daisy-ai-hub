from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from google.cloud import secretmanager
import os
import sys
import pathlib
import yaml

# Use centralized logging configuration
from config import get_logger

logger = get_logger(__name__)
logger.info("🔐 Auth middleware module loaded")

# Security scheme for Bearer token
security = HTTPBearer()

def load_gcp_config():
    """Load GCP configuration from gcp.yml file"""
    try:
        # Get the path to gcp.yml (go up one level from middleware to project root, then into config)
        current_dir = pathlib.Path(__file__).parent
        config_path = current_dir.parent / 'config' / 'gcp.yml'
        
        if config_path.exists():
            logger.info(f'Loading GCP config from: {config_path}')
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
                logger.info("✅ Successfully loaded GCP configuration")
                return config
        else:
            logger.warning(f"⚠️  GCP config file not found at: {config_path}")
            return {}
    except Exception as e:
        logger.error(f"❌ Error loading GCP config: {str(e)}")
        return {}

class TokenAuth:
    def __init__(self, project_id: str = None):
        # Load GCP configuration from gcp.yml
        self.config = load_gcp_config()
        
        # Get project ID/number with priority: parameter > env vars > config > hardcoded fallback
        if project_id is None:
            project_id = (
                os.environ.get('GOOGLE_CLOUD_PROJECT') or 
                os.environ.get('GCP_PROJECT') or 
                self.config.get('secret_manager', {}).get('project_for_secrets') or
                self.config.get('project_number')
            )
        
        # Get secret name from config
        self.secret_name = self.config.get('secret_manager', {}).get('api_token_secret', 'ai-hub-api-token')
        
        logger.info(f"🚀 Initializing TokenAuth for project: {project_id}")
        logger.info(f"🔑 Using secret name: {self.secret_name}")
        self.project_id = project_id
        self.api_token = None  # Store the token in memory
        self.token_load_failed = False  # Track if token loading failed
        
        # Load the token immediately at startup
        self._load_api_token()
        
    def _load_api_token(self) -> None:
        """
        Load the API token from Google Secret Manager at startup.
        This is called once during initialization to avoid repeated Secret Manager calls.
        """
        logger.info("🔑 Loading API token from Secret Manager at startup")
        try:
            # Initialize Secret Manager client
            client = secretmanager.SecretManagerServiceClient()
            logger.info("✅ Secret Manager client initialized successfully")
            
            # Try latest version first, then fall back to version 1 if needed
            for version in ["latest", "1"]:
                try:
                    name = f"projects/{self.project_id}/secrets/{self.secret_name}/versions/{version}"
                    logger.info(f"📍 Accessing secret: {name}")
                    
                    # Access the secret version
                    response = client.access_secret_version(request={"name": name})
                    
                    # Decode the secret payload
                    secret_value = response.payload.data.decode("UTF-8")
                    
                    # Store the token in memory
                    self.api_token = secret_value
                    self.token_load_failed = False
                    logger.info(f"✅ Successfully loaded API token from Secret Manager (version {version})")
                    return
                    
                except Exception as version_error:
                    logger.warning(f"⚠️  Failed to access version {version}: {str(version_error)}")
                    if version == "1":  # If this was the last attempt, continue to fallback
                        continue
            
        except Exception as e:
            logger.error(f"❌ Error loading API token from Secret Manager: {str(e)}")
        
        # Fallback to environment variable for local development
        fallback_token = os.getenv("AI_HUB_API_TOKEN")
        if fallback_token:
            logger.warning("⚠️  Using fallback API token from environment variable")
            self.api_token = fallback_token
            self.token_load_failed = False
            return
        else:
            logger.error("💥 No API token available from Secret Manager or environment variables")
            logger.warning("⚠️  Application will start but authentication will return 503 Service Unavailable")
            logger.info("🔧 To fix: Set AI_HUB_API_TOKEN environment variable or fix Secret Manager access")
            self.api_token = None
            self.token_load_failed = True
    
    def refresh_token(self) -> None:
        """
        Refresh the API token from Secret Manager.
        This can be called manually if you need to update the token without restarting.
        """
        logger.info("🔄 Manually refreshing API token")
        self._load_api_token()
    
    def verify_token(self, credentials: HTTPAuthorizationCredentials = Security(security)) -> bool:
        """
        Verify the provided Bearer token against the pre-loaded token.
        This is fast since the token was loaded once at startup.
        """
        logger.info("🔍 Starting token verification")
        try:
            # Check if token loading failed during startup
            if self.token_load_failed or not self.api_token:
                logger.error("💥 Authentication service unavailable - no API token loaded")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Authentication service temporarily unavailable. Please try again later."
                )
            
            # Get the token from the Authorization header
            provided_token = credentials.credentials
            token_preview = provided_token[:8] + "..." if len(provided_token) > 8 else provided_token
            logger.info(f"🎫 Received token: {token_preview}")
            
            # Compare tokens (using the pre-loaded token)
            if provided_token == self.api_token:
                logger.info("✅ Token verification successful - access granted")
                return True
            else:
                logger.warning("❌ Token verification failed - invalid token provided")
                valid_preview = self.api_token[:8] + "..." if len(self.api_token) > 8 else self.api_token
                logger.warning(f"🔍 Expected token starts with: {valid_preview}")
                logger.warning(f"🔍 Received token starts with: {token_preview}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
                
        except HTTPException:
            # Re-raise HTTP exceptions (like 401 Unauthorized or 503 Service Unavailable)
            raise
        except Exception as e:
            logger.error(f"💥 Error during token verification: {str(e)}")
            logger.error(f"🔍 Exception type: {type(e).__name__}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Token verification failed"
            )

# Global instance
logger.info("🔧 Creating global TokenAuth instance")
token_auth = TokenAuth()

# Check if token loading was successful and log appropriately
if token_auth.token_load_failed:
    logger.warning("🚨 TokenAuth instance created but authentication is disabled")
    logger.info("🔧 To enable authentication:")
    logger.info("   1. Fix Secret Manager permissions")
    logger.info("   2. Set AI_HUB_API_TOKEN environment variable")
    logger.info("   3. Call token_auth.refresh_token() after fixing")
else:
    logger.info("🔧 Global TokenAuth instance created successfully with working authentication")

# Dependency function for FastAPI routes
async def verify_api_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> bool:
    """
    FastAPI dependency function to verify API tokens.
    Use this in your route dependencies to protect endpoints.
    """
    logger.info("🚪 API token verification requested via dependency")
    result = token_auth.verify_token(credentials)
    logger.info(f"🎯 Token verification result: {result}")
    return result