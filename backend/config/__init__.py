"""
Configuration package for the AI Hub Backend.
Contains application configuration files and logging setup.
"""

from .logging_config import setup_logging, get_logger

__all__ = ["setup_logging", "get_logger"]
