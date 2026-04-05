"""
Router agent that determines which specialized agent to use.
Uses a simple LLM classifier to return the agent name, then dispatches.
"""
import logging
from typing import List
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.tools import BaseTool

logger = logging.getLogger("langchain_agent")


class RouterAgent:
    """
    Router agent that classifies queries and returns the appropriate tool name.
    """

    def __init__(self, tools: List[BaseTool]):
        self.tools = tools
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.valid_tool_names = [tool.name for tool in self.tools]

        tool_descriptions = "\n".join(
            [f"- {tool.name}: {tool.description}" for tool in self.tools]
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are a router that selects the best tool for a user query.\n"
                "Return ONLY the tool name, nothing else.\n\n"
                f"Available tools:\n{tool_descriptions}\n\n"
                "If the query doesn't clearly match any tool, select the most relevant one."
            )),
            ("human", "{input}"),
        ])
        self.chain = self.prompt | self.llm
        logger.info("Router agent initialized with %d tools", len(self.tools))

    async def route_query(self, query: str) -> str:
        """
        Route a query to determine which tool to use.

        Returns:
            str: Name of the tool to use
        """
        response = await self.chain.ainvoke({"input": query})
        tool_name = response.content.strip()

        if tool_name not in self.valid_tool_names:
            logger.warning(
                "Router returned invalid tool name: %s. Defaulting to first tool.",
                tool_name,
            )
            return self.valid_tool_names[0]

        return tool_name
