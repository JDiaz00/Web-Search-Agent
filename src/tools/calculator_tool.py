"""
Calculator tool for performing basic arithmetic operations
"""
import logging
from typing import Type, Optional
from pydantic import BaseModel, Field
from langchain.tools import BaseTool

logger = logging.getLogger("langchain_agent")

class CalculatorInput(BaseModel):
    """Input for the calculator tool."""
    expression: str = Field(
        description="A mathematical expression to evaluate. Can include numbers, operators (+, -, *, /, ^), parentheses, and common functions."
    )

class CalculatorTool(BaseTool):
    """Tool for performing basic arithmetic calculations."""
    name = "calculator"
    description = "Useful for performing mathematical calculations. Input should be a valid mathematical expression."
    args_schema: Type[BaseModel] = CalculatorInput
    
    def _run(self, expression: str) -> str:
        """
        Evaluate a mathematical expression and return the result.
        
        Args:
            expression (str): The mathematical expression to evaluate
            
        Returns:
            str: The result of the calculation
        """
        try:
            # Use eval with a safe namespace for basic calculations
            # This is not safe for production use as is - consider using a proper math parser
            # like sympy.sympify or numexpr for production
            safe_namespace = {"__builtins__": None}
            # Add safe math functions
            import math
            safe_math = {
                'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                'sqrt': math.sqrt, 'abs': abs, 'pow': pow,
                'pi': math.pi, 'e': math.e
            }
            
            # Replace ^ with ** for exponentiation
            expression = expression.replace('^', '**')
            
            result = eval(expression, {"__builtins__": {}}, safe_math)
            result_str = str(result)
            
            # Log the calculation
            logger.info(f"Calculated: {expression} = {result_str}")
            
            return result_str
        except Exception as e:
            error_msg = f"Error calculating '{expression}': {str(e)}"
            logger.error(error_msg)
            return f"Error: {str(e)}. Please check your expression and try again."
            
    async def _arun(self, expression: str) -> str:
        """Async implementation of the calculator tool."""
        return self._run(expression) 