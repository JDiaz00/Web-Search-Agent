"""
Specialized agent for search-related queries
"""

import logging

from src.agents.base_agent import BaseAgent
from src.tools.search_tool import SearchTool

logger = logging.getLogger("langchain_agent")


class SearchAgent(BaseAgent):
    """
    Specialized agent for handling search-related queries
    """

    def __init__(self):
        """Initialize the search agent"""
        # Create the search tool
        tool = SearchTool()

        # Define system prompt for the agent
        system_prompt = f"""You are a specialized assistant that expertly handles search queries.
            
You provide accurate, helpful information based on web search results.
When asked to search for information, you query for the information and format the results clearly.
Always cite your sources when providing information from search results.

Here are the tools available to you: {tool.name}: {tool.description}
"""

        # Initialize the base agent
        super().__init__(tools=[tool], system_prompt=system_prompt)
        logger.info("Search agent initialized")
