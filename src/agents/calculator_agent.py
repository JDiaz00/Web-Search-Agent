"""
Specialized agent for calculator and math-related queries
"""
import logging
from src.agents.base_agent import BaseAgent
from src.tools.calculator_tool import CalculatorTool

logger = logging.getLogger("langchain_agent")

class CalculatorAgent(BaseAgent):
    """
    Specialized agent for handling calculator and math-related queries
    """
    
    def __init__(self):
        """Initialize the calculator agent"""
        # Create the calculator tool
        tool = CalculatorTool()
        
        # Create system prompt
        system_prompt = f"""You are a specialized assistant that expertly handles mathematical calculations.
Your specialty is: {tool.description}
You provide accurate, step-by-step solutions when appropriate.
Always double-check your calculations before providing the final answer.
For complex problems, explain your approach briefly.
"""
        
        # Initialize the base agent
        super().__init__(system_prompt, [tool])
        logger.info("Calculator agent initialized") 