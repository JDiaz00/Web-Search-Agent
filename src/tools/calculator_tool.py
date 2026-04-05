"""
Calculator tool for performing basic arithmetic operations.

Uses an AST-based expression evaluator instead of eval() for safety.
"""
import ast
import math
import logging
import operator
from typing import Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool

logger = logging.getLogger("langchain_agent")

# Allowed math constants and functions
_MATH_CONSTANTS = {
    'pi': math.pi,
    'e': math.e,
}

_MATH_FUNCTIONS = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'sqrt': math.sqrt,
    'log': math.log,
    'abs': abs,
}

# Allowed binary operators
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}

# Allowed unary operators
_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _safe_eval(node: ast.AST) -> float:
    """Recursively evaluate an AST node containing only safe math operations."""
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Name):
        if node.id in _MATH_CONSTANTS:
            return _MATH_CONSTANTS[node.id]
        raise ValueError(f"Unknown variable: '{node.id}'")

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _OPERATORS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        return _OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _UNARY_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _UNARY_OPERATORS[op_type](_safe_eval(node.operand))

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls are allowed")
        func_name = node.func.id
        if func_name not in _MATH_FUNCTIONS:
            raise ValueError(f"Unknown function: '{func_name}'")
        if node.keywords:
            raise ValueError("Keyword arguments are not allowed")
        args = [_safe_eval(arg) for arg in node.args]
        return _MATH_FUNCTIONS[func_name](*args)

    raise ValueError(f"Unsupported expression type: {type(node).__name__}")


class CalculatorInput(BaseModel):
    """Input for the calculator tool."""
    expression: str = Field(
        description="A mathematical expression to evaluate. Can include numbers, "
        "operators (+, -, *, /, **, %, ^), parentheses, and functions "
        "(sin, cos, tan, sqrt, log, abs) plus constants (pi, e)."
    )


class CalculatorTool(BaseTool):
    """Tool for performing basic arithmetic calculations."""
    name: str = "calculator"
    description: str = (
        "Useful for performing mathematical calculations. Input should be a "
        "valid mathematical expression."
    )
    args_schema: Type[BaseModel] = CalculatorInput

    def _run(self, expression: str) -> str:
        """
        Evaluate a mathematical expression safely using AST parsing.

        Args:
            expression: The mathematical expression to evaluate.

        Returns:
            The result of the calculation as a string.
        """
        try:
            # Replace ^ with ** for exponentiation
            expr = expression.replace('^', '**')

            tree = ast.parse(expr, mode='eval')
            result = _safe_eval(tree)
            result_str = str(result)

            logger.info(f"Calculated: {expression} = {result_str}")
            return result_str
        except Exception as e:
            error_msg = f"Error calculating '{expression}': {str(e)}"
            logger.error(error_msg)
            return f"Error: {str(e)}. Please check your expression and try again."

    async def _arun(self, expression: str) -> str:
        """Async implementation of the calculator tool."""
        return self._run(expression) 