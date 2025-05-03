"""
Router agent that determines which specialized agent to use
"""
import logging
from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.tools import BaseTool

logger = logging.getLogger("langchain_agent")

class RouterAgent:
    """
    Router agent that determines which specialized agent to use
    """
    
    def __init__(self, tools: List[BaseTool]):
        """
        Initialize the router agent
        
        Args:
            tools: List of all available tools
        """
        self.tools = tools
        self.agent_executor = self._create_router_executor()
        logger.info("Router agent initialized")
    
    def _create_router_executor(self) -> AgentExecutor:
        """
        Create the router agent executor
        
        Returns:
            AgentExecutor: Router agent executor instance
        """
        # Initialize LLM
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        
        # Initialize memory
        memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")
        
        # Create prompt for router
        tool_descriptions = "\n".join([f"- {tool.name}: {tool.description}" for tool in self.tools])
        router_prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are a router assistant that determines which specialized tool would best handle a user query.
Based on the user's query, select the most appropriate tool from the available tools.
Return ONLY the name of the tool without any explanation.

Available tools:
{tool_descriptions}

If the query doesn't clearly match any tool, select the one that is most relevant.
"""),
            ("human", "{input}"),
        ])
        
        # Create agent executor directly with LLM (no tools needed for routing)
        agent_executor = AgentExecutor.from_agent_and_tools(
            agent=router_prompt | llm,
            tools=[],  # No tools needed for routing
            memory=memory,
            verbose=True
        )
        
        return agent_executor
    
    async def route_query(self, query: str) -> str:
        """
        Route a query to determine which tool to use
        
        Args:
            query: User query to process
            
        Returns:
            str: Name of the tool to use
        """
        response = await self.agent_executor.ainvoke({"input": query})
        # Clean the response to get just the tool name
        tool_name = response["output"].strip()
        
        # Validate the tool name
        valid_tool_names = [tool.name for tool in self.tools]
        if tool_name not in valid_tool_names:
            logger.warning(f"Router returned invalid tool name: {tool_name}. Defaulting to first tool.")
            return valid_tool_names[0]
        
        return tool_name 