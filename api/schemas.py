from __future__ import annotations

from pydantic import BaseModel, Field


# ──────────────────────────────────────────────
# Chat
# ──────────────────────────────────────────────

class ChatMessage(BaseModel):
    role: str = Field(description="Either 'user' or 'assistant'")
    content: str = Field(description="Message content")


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(
        ..., description="Conversation history + latest user message"
    )
    session_id: str | None = Field(
        None, description="Optional session ID for conversation tracking"
    )
    stream: bool = Field(
        False, description="Whether to stream the response via SSE"
    )


class ToolCallInfo(BaseModel):
    tool: str | None = Field(None, description="Name of the tool that was used")
    result_summary: str | None = Field(
        None, description="Brief summary of what the tool returned"
    )


class ChatResponse(BaseModel):
    reply: str = Field(description="The assistant's response")
    tool_used: str | None = Field(None, description="Name of the tool used, if any")
    session_id: str | None = Field(None, description="Session ID for continued conversation")


# ──────────────────────────────────────────────
# Email
# ──────────────────────────────────────────────

class EmailRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=5, max_length=200)
    message: str = Field(..., min_length=1, max_length=5000)


class EmailResponse(BaseModel):
    success: bool
    message: str


# ──────────────────────────────────────────────
# Health
# ──────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "0.1.0"
    provider: str | None = None
    index_loaded: bool = False
    document_count: int = 0
