from __future__ import annotations

import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from api.schemas import (
    ChatRequest,
    ChatResponse,
    EmailRequest,
    EmailResponse,
    HealthResponse,
)
from agents.orchestrator import PortfolioAgent
from security.guardrails import Guardrails
from security.sanitize import sanitize_input

logger = logging.getLogger(__name__)

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
guardrails = Guardrails()


def get_agent() -> PortfolioAgent:
    """Dependency that provides a singleton agent instance."""
    return PortfolioAgent()


# ──────────────────────────────────────────────
# Health Check
# ──────────────────────────────────────────────

@router.get("/api/health", response_model=HealthResponse)
async def health_check(agent: PortfolioAgent = Depends(get_agent)):
    """Check API health and RAG index status."""
    index_info = agent.get_index_info()
    return HealthResponse(
        status="ok",
        version="0.1.0",
        provider=agent.active_provider,
        index_loaded=index_info.get("loaded", False),
        document_count=index_info.get("document_count", 0),
    )


# ──────────────────────────────────────────────
# Chat
# ──────────────────────────────────────────────

@router.post("/api/chat", response_model=ChatResponse)
@limiter.limit("10/minute")
async def chat(
    request: Request,
    body: ChatRequest,
    agent: PortfolioAgent = Depends(get_agent),
):
    """Send a chat message and receive a response."""
    # Get the latest user message
    if not body.messages or body.messages[-1].role != "user":
        raise HTTPException(status_code=400, detail="Last message must be from user")

    user_message = body.messages[-1].content

    # Run guardrails check
    guardrail_result = guardrails.check(user_message)
    if guardrail_result.blocked:
        return ChatResponse(
            reply=guardrail_result.response,
            tool_used=None,
            session_id=body.session_id or str(uuid.uuid4()),
        )

    # Sanitize input
    sanitized = sanitize_input(user_message)

    # Build conversation history for the agent
    conversation = [m.model_dump() for m in body.messages]
    conversation[-1]["content"] = sanitized  # Use sanitized version

    # Generate session ID if not provided
    session_id = body.session_id or str(uuid.uuid4())

    # Run agent
    try:
        result = await agent.run(conversation, session_id=session_id)
        return ChatResponse(
            reply=result["response"],
            tool_used=result.get("tool_used"),
            session_id=session_id,
        )
    except Exception as e:
        logger.exception("Agent run failed")
        raise HTTPException(status_code=500, detail="Failed to generate response")


# ──────────────────────────────────────────────
# Tools Listing
# ──────────────────────────────────────────────

@router.get("/api/tools")
async def list_tools(agent: PortfolioAgent = Depends(get_agent)):
    """List available tools and their descriptions."""
    return {"tools": agent.get_tool_descriptions()}


# ──────────────────────────────────────────────
# Direct Email (bypasses agent for simple contact forms)
# ──────────────────────────────────────────────

@router.post("/api/send-email", response_model=EmailResponse)
@limiter.limit("1/10minute")
async def send_email(
    request: Request,
    body: EmailRequest,
    agent: PortfolioAgent = Depends(get_agent),
):
    """Send an email to Wesley directly."""
    try:
        # Reuse the email tool from the agent
        email_tool = agent.get_tool("email")
        if not email_tool:
            raise HTTPException(status_code=500, detail="Email tool not available")

        result = await email_tool.execute(
            to_email="peterwesley484@gmail.com",
            from_name=body.name,
            from_email=body.email,
            message=body.message,
        )
        return EmailResponse(success=True, message="Email sent successfully")
    except Exception as e:
        logger.exception("Email send failed")
        return EmailResponse(success=False, message=str(e))
