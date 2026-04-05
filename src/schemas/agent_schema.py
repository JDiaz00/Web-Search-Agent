"""
Schemas for agent requests and responses
"""

from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class AgentRequest(BaseModel):
    """
    Request model for agent API
    """

    query: str = Field(..., description="The user query to process with the agent", max_length=2000)
    session_id: Optional[str] = Field(None, description="Optional session ID for tracking conversations")

    @field_validator("query")
    @classmethod
    def query_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Query must not be blank")
        return v.strip()


class AgentResponse(BaseModel):
    """
    Response model for agent API
    """

    answer: str = Field(..., description="The agent's answer to the query")
    steps: List[str] = Field(default_factory=list, description="The steps taken by the agent")


class ToolResponse(BaseModel):
    """
    Response model for tool execution
    """

    status: str = Field(..., description="Status of the tool execution (success/error)")
    data: Optional[dict] = Field(None, description="Data returned by the tool")
    error: Optional[str] = Field(None, description="Error message if tool execution failed")
