import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
from config import get_logger

# Import routes
from routes import email, shopping, images, social_media, career, productivity, llm, invoice_validator
# Import authentication
from middleware.auth import verify_api_token

logger = get_logger(__name__)
logger.info("🚀 Starting AI Hub Backend application")

# Initialize FastAPI app
app = FastAPI(
    title="AI Hub Backend",
    description="A comprehensive AI-powered backend service with multiple specialized endpoints for email assistance, content creation, image generation, career development, and productivity tools.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

origins = [
    "http://localhost:3000",  # Local front-end
    "http://localhost:3001",  # Local front-end
    "http://localhost:8080",  # Local back-end
    # Add your Cloud Run frontend URLs here, e.g.:
    # "https://your-frontend-service-hash.europe-west3.run.app",
    # "https://yourdomain.com",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Include routers with authentication dependency
# Note: We apply the auth dependency to each router's routes
app.include_router(email.router, dependencies=[Depends(verify_api_token)])
app.include_router(shopping.router, dependencies=[Depends(verify_api_token)])
app.include_router(images.router, dependencies=[Depends(verify_api_token)])
app.include_router(social_media.router, dependencies=[Depends(verify_api_token)])
app.include_router(career.router, dependencies=[Depends(verify_api_token)])
app.include_router(productivity.router, dependencies=[Depends(verify_api_token)])
app.include_router(llm.router)
app.include_router(invoice_validator.router, dependencies=[Depends(verify_api_token)])


# Health check endpoint (public - no authentication required)
@app.get("/health")
async def health_check():
    """Health check endpoint to verify the service is running."""
    return {"status": "healthy", "message": "AI Hub Backend is running"}


# Root endpoint (public - no authentication required)
@app.get("/")
async def root():
    """Root endpoint with basic information about the API."""
    logger.info("📍 Root endpoint accessed")
    return {
        "message": "AI Hub Backend API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# if __name__ == "__main__":
#    uvicorn.run(app, host="127.0.0.1", port=8002)