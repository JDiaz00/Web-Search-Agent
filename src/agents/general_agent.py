"""
General agent that can use all tools as a fallback
"""
import logging
from typing import List
from src.agents.base_agent import BaseAgent
from langchain.tools import BaseTool

logger = logging.getLogger("langchain_agent")

class GeneralAgent(BaseAgent):
    """
    General agent that can use all tools as a fallback
    """
    
    def __init__(self, tools: List[BaseTool]):
        """
        Initialize the general agent
        
        Args:
            tools: List of all available tools
        """
        # Create system prompt
        system_prompt = """You are an intelligent assistant that can use all available tools to help users.
You analyze user queries and determine the best tool or combination of tools to answer their questions.
Be concise but thorough in your responses.
For complex queries, break down your approach step by step.
"""
        
        # Initialize the base agent
        super().__init__(system_prompt, tools)
        logger.info("General agent initialized") 