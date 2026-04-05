"""
Tool for generating story elements based on user input
"""

import logging
from typing import Type

from langchain.tools import BaseTool
from pydantic import BaseModel, Field

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

            # Parse elements and provide structured story building blocks
            elements_lower = elements.lower()

            # Detect genre
            genre_keywords = {
                "fantasy": ["fantasy", "magic", "dragon", "wizard", "elf", "kingdom"],
                "sci-fi": [
                    "sci-fi",
                    "science fiction",
                    "space",
                    "future",
                    "robot",
                    "alien",
                    "cyberpunk",
                ],
                "mystery": [
                    "mystery",
                    "detective",
                    "crime",
                    "murder",
                    "clue",
                    "investigation",
                ],
                "romance": ["romance", "love", "relationship", "heart"],
                "horror": ["horror", "scary", "ghost", "haunted", "dark", "terror"],
                "adventure": ["adventure", "quest", "journey", "explore", "treasure"],
                "thriller": ["thriller", "suspense", "chase", "spy", "conspiracy"],
            }

            detected_genre = "general fiction"
            for genre, keywords in genre_keywords.items():
                if any(kw in elements_lower for kw in keywords):
                    detected_genre = genre
                    break

            # Detect setting
            setting_keywords = {
                "urban": ["city", "urban", "metropolis", "downtown"],
                "rural": ["village", "farm", "countryside", "rural"],
                "futuristic": ["future", "futuristic", "cyberpunk", "space station"],
                "medieval": ["medieval", "castle", "kingdom", "knight"],
                "contemporary": ["modern", "present", "today", "contemporary"],
            }

            detected_setting = "unspecified"
            for setting, keywords in setting_keywords.items():
                if any(kw in elements_lower for kw in keywords):
                    detected_setting = setting
                    break

            # Build structured output
            result = f"""STORY ELEMENTS ANALYSIS
Genre: {detected_genre}
Setting: {detected_setting}
User Input: {elements}

SUGGESTED STRUCTURE:
- Develop 2-4 main characters that fit the {detected_genre} genre
- Create a central conflict appropriate for a {detected_setting} setting
- Include a clear three-act structure (setup, confrontation, resolution)
- Weave the user's requested elements throughout the narrative

Use these elements to generate a complete story concept with title, characters, page count, and summary."""

            return result

        except Exception as e:
            logger.error(f"Error generating story: {str(e)}")
            return f"Error generating story: {str(e)}"

    async def _arun(self, elements: str) -> str:
        """Async implementation - not supported."""
        raise NotImplementedError("StoryTool does not support async execution.")
