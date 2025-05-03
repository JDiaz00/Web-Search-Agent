"""
Main application file for LangChain Agent
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory

from src.tools.tool_registry import get_all_tools
from src.schemas.agent_schema import AgentRequest, AgentResponse
from src.services.langsmith_service import init_langsmith
from src.logging_config import setup_logging

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging()

# Initialize LangSmith
init_langsmith()

# Initialize FastAPI app
app = FastAPI(title="LangChain Agent API", 
              description="API for interacting with custom LangChain agent",
              version="0.1.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create agent instance
def get_agent():
    # Get all tools from registry
    tools = get_all_tools()
    
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    # Initialize memory
    memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")
    
    # Create prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an intelligent assistant that uses tools to help users. "
                  "Be concise but helpful in your responses."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Create agent
    agent = create_openai_tools_agent(llm, tools, prompt)
    
    # Create agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        return_intermediate_steps=True
    )
    
    return agent_executor

# Initialize the agent
agent_executor = get_agent()

@app.post("/api/agent", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    """
    Run the agent with the given input query
    """
    try:
        # Process the input with the agent
        response = agent_executor.invoke({"input": request.query})
        
        # Return response
        return AgentResponse(
            answer=response["output"],
            steps=[step[0].tool + ": " + str(step[0].tool_input) for step in response["intermediate_steps"]]
        )
    except Exception as e:
        logger.error(f"Error running agent: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Check if the API is running"""
    return {"status": "ok"} 