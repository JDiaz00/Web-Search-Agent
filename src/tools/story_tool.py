"""
Tool for generating story elements based on user input
"""
import logging
from typing import Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool

logger = logging.getLogger("langchain_agent")

class StoryInput(BaseModel):
    """Input for the story generation tool."""
    elements: str = Field(
        description="Elements of the story to incorporate (characters, setting, theme, genre, etc.)"
    )

class StoryTool(BaseTool):
    """Tool for generating story elements based on user input."""
    name = "story_generator"
    description = "Generates story elements such as title, characters, and summary based on user input. Use this when you need to create or develop story ideas."
    args_schema: Type[BaseModel] = StoryInput
    
    def _run(self, elements: str) -> str:
        """
        Generate story elements based on user input
        
        Args:
            elements: Elements to incorporate into the story
            
        Returns:
            str: Generated story elements in a structured format
        """
        try:
            logger.info(f"Generating story with elements: {elements}")
            
            # This tool doesn't actually perform complex processing itself.
            # The LLM will generate the story elements based on the prompt.
            # This method is mainly for logging and structure.
            
            return f"Story elements for: {elements}\n\nThe LLM will generate a title, character list, page count, and summary based on these elements."
            
        except Exception as e:
            logger.error(f"Error generating story: {str(e)}")
            return f"Error generating story: {str(e)}"
    
    async def _arun(self, elements: str) -> str:
        """Async implementation of the story generation tool."""
        return self._run(elements) 