from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from api.routes import limiter, router
from agents.orchestrator import PortfolioAgent

load_dotenv()

# ──────────────────────────────────────────────
# Logging Configuration
# ──────────────────────────────────────────────

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format="%(asctime)s | %(name)-24s | %(levelname)-6s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Lifecycle Management
# ──────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle: startup and shutdown."""
    # Startup: initialize the agent singleton and warm the vector store
    logger.info("Starting Portfolio Agent API...")
    agent = PortfolioAgent()
    index_info = agent.get_index_info()
    if index_info["loaded"]:
        logger.info(
            "Vector store loaded with %d documents",
            index_info["document_count"],
        )
    else:
        logger.warning("Vector store is empty — knowledge base may need rebuilding")

    provider = agent.active_provider
    if provider and provider != "none":
        logger.info("Using LLM provider: %s", provider)
    else:
        logger.warning("No LLM provider configured — set GROQ_API_KEY or GEMINI_API_KEY")

    yield

    # Shutdown: clean up resources
    logger.info("Shutting down Portfolio Agent API...")
    await agent.cleanup()


# ──────────────────────────────────────────────
# App Initialization
# ──────────────────────────────────────────────

app = FastAPI(
    title="Portfolio Agent API",
    description="AI-powered digital twin for Wesley's portfolio. Chat with an agent that "
    "knows about projects, skills, certifications, and case studies.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ──────────────────────────────────────────────
# CORS
# ──────────────────────────────────────────────

cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────────────────────────────────────
# Rate Limiting
# ──────────────────────────────────────────────

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────

app.include_router(router)


# ──────────────────────────────────────────────
# Global Exception Handler
# ──────────────────────────────────────────────

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )


# ──────────────────────────────────────────────
# Entry Point
# ──────────────────────────────────────────────

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host=host, port=port, reload=True)
