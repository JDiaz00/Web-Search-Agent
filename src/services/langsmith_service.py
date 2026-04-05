"""
LangSmith integration service
"""

import logging
import os

from langsmith import Client

logger = logging.getLogger("langchain_agent")


def init_langsmith():
    """
    Initialize LangSmith tracing
    """
    # Check if LangSmith API key is set
    langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
    if not langchain_api_key:
        logger.warning("LANGCHAIN_API_KEY not set. LangSmith tracing will not be available.")
        return False

    # Configure LangSmith project
    project_name = os.getenv("LANGCHAIN_PROJECT", "clases_ia")
    tracing_v2 = os.getenv("LANGCHAIN_TRACING_V2", "true").lower() == "true"
    endpoint = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")

    # Log LangSmith configuration
    logger.info(f"LangSmith initialized with project: {project_name}")
    logger.info(f"LangSmith tracing v2: {tracing_v2}")

    # Initialize LangSmith client
    try:
        client = Client(api_key=langchain_api_key, api_url=endpoint)
        logger.info("LangSmith client initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Error initializing LangSmith client: {str(e)}")
        return False
