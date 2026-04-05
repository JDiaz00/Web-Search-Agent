"""Search tool using SerpAPI with the Google search engine."""

import logging
import os

from langchain.tools import BaseTool
from serpapi import Client

logger = logging.getLogger("langchain_agent")


class SearchTool(BaseTool):
    """Tool for performing web searches via SerpAPI's Google engine.

    Requires the SERPAPI_KEY environment variable to be set with a valid
    SerpAPI API key. Results are returned as formatted text with titles,
    links, and snippets for the top 5 organic results.
    """

    name: str = "search"
    description: str = (
        "Search for information using Google search engine via SerpAPI. "
        "Use this tool when you need to find general information about any topic."
    )

    def _get_api_key(self) -> str:
        """Retrieve the SerpAPI key from the SERPAPI_KEY environment variable.

        Returns:
            The SerpAPI key.

        Raises:
            ValueError: If SERPAPI_KEY is not set in the environment.
        """
        api_key = os.environ.get("SERPAPI_KEY")
        if not api_key:
            raise ValueError(
                "SERPAPI_KEY environment variable is not set. "
                "Please set it to a valid SerpAPI key."
            )
        return api_key

    def _run(self, query: str) -> str:
        """Search for information based on the query.

        Args:
            query: The search query (e.g., "coffee", "history of Rome").

        Returns:
            Search results formatted as a string.
        """
        try:
            logger.info(f"Searching with query: {query}")

            client = Client(api_key=self._get_api_key())

            results = client.search(
                {
                    "engine": "google",
                    "q": query,
                }
            )
            logger.info(f"Results: {results}")

            if isinstance(results, dict) and "error" in results:
                return f"Error: {results['error']}"

            if "organic_results" in results and results["organic_results"]:
                organic = results["organic_results"][:5]
                return "\n".join(
                    [
                        f"{result.get('title', 'No title')} - {result.get('link', '')}\n{result.get('snippet', '')}"
                        for result in organic
                    ]
                )

            return "No search results found for this query."

        except ValueError:
            raise
        except ConnectionError as e:
            logger.error(f"Network error during search: {e}")
            return f"Network error during search: {e}"
        except TimeoutError as e:
            logger.error(f"Search request timed out: {e}")
            return f"Search request timed out: {e}"
        except Exception as e:
            logger.error(f"Unexpected error performing search: {e}")
            return f"Error during search: {e}"

    async def _arun(self, query: str) -> str:
        """Async search is not supported.

        Raises:
            NotImplementedError: Always, as async execution is not supported.
        """
        raise NotImplementedError("SearchTool does not support async execution.")
