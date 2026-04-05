"""
Logging configuration for the application
"""
import os
import logging
import sys

def setup_logging():
    """
    Setup logging configuration
    """
    # Get log level from env or default to INFO
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s | %(name)s | %(levelname)-8s | %(module)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ],
        force=True,
    )
    
    # Create logger
    logger = logging.getLogger("langchain_agent")
    
    # Log configuration
    logger.info(f"Logging configured with level: {log_level}")
    
    return logger