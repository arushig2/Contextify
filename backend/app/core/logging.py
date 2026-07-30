"""
Application logging configuration.

This module configures Python's logging system for the entire
application. It should be initialized once during application
startup.

Responsibilities:
- Configure log format
- Configure log level
- Configure log handlers

This module should not contain business logic or create module-specific loggers.
"""
import logging
from .config import settings

def setup_logging():
    # Configure the logging system
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s [%(levelname)s] %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler()],
        force=True # Ensures configuration overrides existing settings
    )

    # Suppress verbose third-party HTTP logs
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

setup_logging()