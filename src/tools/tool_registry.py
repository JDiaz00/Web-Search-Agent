"""
Tool registry to manage and provide access to tools
"""

import logging
from typing import List

from langchain.tools import BaseTool

from src.tools.calculator_tool import CalculatorTool
from src.tools.search_tool import SearchTool
from src.tools.story_tool import StoryTool

logger = logging.getLogger("langchain_agent")


def get_all_tools() -> List[BaseTool]:
    """
    Get all registered tools for the agent

    Returns:
        List[BaseTool]: List of all available tools
    """
    # Initialize tools
    tools = [
        CalculatorTool(),
        SearchTool(),
        StoryTool(),
    ]

    # Log available tools
    tool_names = [tool.name for tool in tools]
    logger.info(f"Registered tools: {', '.join(tool_names)}")

    return tools
