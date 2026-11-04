"""
Centralized logging configuration for Cloud Run deployment.
This module sets up proper logging that works with Google Cloud Logging.
"""

import logging
import sys
import os


def setup_logging():
    """
    Configure logging for the application.
    Uses structured logging suitable for Cloud Run.
    """
    # Get log level from environment variable, default to INFO
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    
    # Configure basic logging
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout,
        force=True
    )
    
    # Set specific log levels for different modules
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("google").setLevel(logging.WARNING)  # Reduce Google library noise
    logging.getLogger("urllib3").setLevel(logging.WARNING)  # Reduce HTTP library noise
    
    # Log that configuration is complete
    logger = logging.getLogger(__name__)
    is_cloud_run = os.environ.get('K_SERVICE') is not None
    environment = "Cloud Run" if is_cloud_run else "Local"
    logger.info(f"📊 Logging configured - Level: {log_level}, Environment: {environment}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    Args:
        name: The name for the logger (usually __name__)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)


# Auto-setup logging when module is imported
setup_logging()
