"""
Base agent class that all specialized agents will inherit from
"""
import logging
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferWindowMemory
from langchain.tools import BaseTool

logger = logging.getLogger("langchain_agent")

class BaseAgent:
    """
    Base agent class that provides common functionality
    """

    def __init__(self, system_prompt: str, tools: list):
        """
        Initialize a base agent

        Args:
            system_prompt: The system prompt for this agent
            tools: The tools this agent has access to
        """
        self.system_prompt = system_prompt
        self.tools = tools
        self.agent_executor = self._create_agent_executor()

    def _create_agent_executor(self) -> AgentExecutor:
        """
        Create the agent executor

        Returns:
            AgentExecutor: Agent executor instance
        """
        # Initialize LLM
        llm = ChatOpenAI(model="gpt-4o", temperature=0)

        # Initialize memory with window limit to prevent unbounded growth
        memory = ConversationBufferWindowMemory(
            return_messages=True,
            memory_key="chat_history",
            k=20,
        )

        # Create prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # Create agent
        agent = create_openai_tools_agent(llm, self.tools, prompt)

        # Create agent executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=memory,
            verbose=True,
            return_intermediate_steps=True
        )

        return agent_executor

    async def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a query with this agent

        Args:
            query: User query to process

        Returns:
            Dict[str, Any]: Agent response
        """
        return await self.agent_executor.ainvoke({"input": query})
