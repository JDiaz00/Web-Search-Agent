"""
Specialized agent for story generation queries
"""
import logging
from src.tools.story_tool import StoryTool
from src.agents.base_agent import BaseAgent

logger = logging.getLogger("langchain_agent")

class StoryAgent(BaseAgent):
    """
    Specialized agent for handling story generation requests
    """
    
    def __init__(self):
        """Initialize the story generation agent"""
        # Create the story tool
        tool = StoryTool()
        
        # Define system prompt for the agent
        system_prompt = """You are a creative writing assistant specialized in story development.

When provided with elements of a story, you will generate:
1. A compelling title for the book
2. An estimated page count (typically between 200-500 pages)
3. A list of main characters with brief descriptions
4. A concise plot summary (1-3 paragraphs)

Format your response clearly with sections for each element:

TITLE: [The generated title]
PAGES: [Page count] pages
CHARACTERS:
- [Character Name]: [Brief description]
- [Character Name]: [Brief description]
...
SUMMARY:
[The plot summary]

Be creative and engaging. Incorporate the user's requested elements seamlessly into your story concept.
For fantasy elements, create rich, imaginative worlds. For realistic elements, focus on deep character development.
"""
        
        # Initialize the base agent
        super().__init__(tools=[tool], system_prompt=system_prompt)
        logger.info("Story agent initialized") 