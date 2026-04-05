"""
Main application file for LangChain Agent
"""
import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.schemas.agent_schema import AgentRequest, AgentResponse
from src.services.agent_service import MultiAgentService
from src.services.langsmith_service import init_langsmith
from src.logging_config import setup_logging

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging()

# Validate required env vars at startup
_REQUIRED_ENV_VARS = ["OPENAI_API_KEY", "SERPAPI_KEY"]


def _validate_env() -> None:
    missing = [v for v in _REQUIRED_ENV_VARS if not os.getenv(v)]
    if missing:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing)}"
        )


# Holds the singleton service instance
_agent_service: MultiAgentService | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    global _agent_service
    _validate_env()
    init_langsmith()
    _agent_service = MultiAgentService()
    logger.info("MultiAgentService initialized")
    yield
    _agent_service = None


# Initialize FastAPI app
app = FastAPI(
    title="LangChain Agent API",
    description="API for interacting with custom LangChain agent",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/agent", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    """
    Run the agent with the given input query
    """
    try:
        assert _agent_service is not None, "Service not initialized"
        return await _agent_service.process_query(request.query)
    except Exception as e:
        logger.error(f"Error running agent: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Check if the API is running"""
    return {"status": "ok"}
