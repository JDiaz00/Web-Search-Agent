"""
General search tool using SerpAPI to search on Bing
"""
import logging
import json
import os
from typing import Dict, Any, Optional
from langchain.tools import BaseTool
from serpapi import Client

logger = logging.getLogger("langchain_agent")

class SearchTool(BaseTool):
    """Tool for general searching using SerpAPI with Bing"""
    
    name = "search"
    description = "Search for information using Bing search engine. Use this tool when you need to find general information about any topic."
    
    def _get_api_key(self) -> str:
        """
        Get the SerpAPI key from environment variables
        
        Returns:
            str: The SerpAPI key
        """
        # Try to get the key from environment variables
        api_key = os.environ.get("API_KEY")
        
        # If not found, use a default key (for development only, not recommended for production)
        if not api_key:
            logger.warning("API_KEY not found in environment variables. Using default key.")
            api_key = "jaja"
            
        return api_key
    
    def _run(self, query: str) -> str:
        """
        Search for information based on the query
        
        Args:
            query: The search query (e.g., "coffee", "history of Rome")
            
        Returns:
            str: Search results formatted as a string
        """
        try:
            logger.info(f"Searching with query: {query}")
            
            # Initialize the SerpApi Client
            client = Client(api_key=self._get_api_key())
            
            # Execute the search
            results = client.search({
                "engine": "google",
                "q": query
            })
            logger.info(f"Results: {results}")
            
            # Process results
            if isinstance(results, dict) and "error" in results:
                return f"Error: {results['error']}"
            
            # Extract organic results
            if "organic_results" in results and results["organic_results"]:
                organic = results["organic_results"][:5]  # Get top 5 results
                return "\n".join([
                    f"{result.get('title', 'No title')} - {result.get('link', '')}\n{result.get('snippet', '')}"
                    for result in organic
                ])
            
            # If no results found
            return "No search results found for this query."
            
        except Exception as e:
            logger.error(f"Error performing search: {str(e)}")
            return f"Error during search: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """
        Async version of _run
        
        Args:
            query: The search query
            
        Returns:
            str: Search results formatted as a string
        """
        return self._run(query) 