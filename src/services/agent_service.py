"""
Multi-agent service for processing queries using specialized agents
"""
import logging
from typing import Dict, List, Any, Optional

from src.tools.tool_registry import get_all_tools
from src.schemas.agent_schema import AgentResponse
from src.agents import (
    CalculatorAgent,
    RouterAgent,
    GeneralAgent,
    SearchAgent,
    StoryAgent
)

logger = logging.getLogger("langchain_agent")

class MultiAgentService:
    """
    Service for managing and interacting with specialized agents
    """
    
    def __init__(self):
        """Initialize the multi-agent service"""
        # Get all tools
        self.tools = get_all_tools()
        
        # Map of tool names to agent classes
        self.tool_agent_map = {
            "calculator": CalculatorAgent,
            "search": SearchAgent,
            "story_generator": StoryAgent
        }
        
        # Create specialized agents
        self.specialized_agents = {}
        for tool in self.tools:
            # Get the tool name
            tool_name = tool.name.lower()
            
            # Create the appropriate agent for this tool
            if tool_name in self.tool_agent_map:
                agent_class = self.tool_agent_map[tool_name]
                self.specialized_agents[tool_name] = agent_class()
                logger.info(f"Created specialized agent for tool: {tool_name}")
        
        # Create router agent
        self.router = RouterAgent(self.tools)
        
        # Create fallback general agent
        self.general_agent = GeneralAgent(self.tools)
        
        logger.info(f"Multi-agent service initialized with {len(self.specialized_agents)} specialized agents")
    
    async def process_query(self, query: str) -> AgentResponse:
        """
        Process a query with the specialized agents
        
        Args:
            query: User query to process
            
        Returns:
            AgentResponse: Agent response with answer and steps
        """
        try:
            # Route the query to determine which specialized agent to use
            tool_name = await self.router.route_query(query)
            logger.info(f"Router selected tool: {tool_name}")
            
            # Get the specialized agent
            specialized_agent = self.specialized_agents.get(tool_name.lower())
            
            # Process with specialized agent or fallback to general agent
            if specialized_agent:
                response = await specialized_agent.process_query(query)
                agent_type = f"specialized ({tool_name})"
            else:
                # Fallback to general agent if specialized agent not found
                response = await self.general_agent.process_query(query)
                agent_type = "general (fallback)"
            
            logger.info(f"Query processed by {agent_type} agent")
            
            # Extract steps safely
            steps = []
            if isinstance(response, dict) and "intermediate_steps" in response:
                intermediate_steps = response["intermediate_steps"]
                for step in intermediate_steps:
                    try:
                        if isinstance(step, tuple) and len(step) >= 1:
                            step_info = step[0]
                            if hasattr(step_info, 'tool'):
                                step_tool_name = step_info.tool
                                tool_input = step_info.tool_input
                                steps.append(f"{step_tool_name}: {tool_input}")
                            else:
                                # Handle case where step_info doesn't have expected attributes
                                steps.append(f"Step: {str(step_info)}")
                        else:
                            # Handle case where step is not a tuple or is empty
                            steps.append(f"Step: {str(step)}")
                    except Exception as e:
                        # Log error and continue with next step
                        logger.error(f"Error processing step: {str(e)}")
                        continue
            
            # Create response
            return AgentResponse(
                answer=response.get("output", str(response)) if isinstance(response, dict) else str(response),
                steps=steps
            )
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise Exception(f"Failed to process query: {str(e)}")

# Singleton instance
_agent_service = None

def get_agent_service() -> MultiAgentService:
    """
    Get the multi-agent service instance (singleton)
    
    Returns:
        MultiAgentService: Multi-agent service instance
    """
    global _agent_service
    if _agent_service is None:
        _agent_service = MultiAgentService()
    return _agent_service