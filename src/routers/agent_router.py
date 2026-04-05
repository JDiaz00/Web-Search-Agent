"""
Router for agent API endpoints
"""

import logging

from fastapi import APIRouter, Depends, HTTPException

from src.schemas.agent_schema import AgentRequest, AgentResponse
from src.services.agent_service import get_agent_service

logger = logging.getLogger("langchain_agent")

# Create router
router = APIRouter(prefix="/api/agent", tags=["agent"])


@router.post("", response_model=AgentResponse)
async def process_agent_query(request: AgentRequest):
    """
    Process a query with the agent
    """
    try:
        # Get agent service
        agent_service = get_agent_service()

        # Log the request
        logger.info(f"Processing agent query: {request.query}")

        # Process the query
        result = await agent_service.process_query(request.query)

        # Return the response
        return result

    except Exception as e:
        logger.error(f"Error processing agent query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
