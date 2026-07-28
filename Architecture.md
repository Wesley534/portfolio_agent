# Portfolio Agent — Architecture

## System Overview

An AI-powered digital twin for Wesley's portfolio. Visitors interact with a chatbot that answers questions about Wesley's work, skills, projects, and background using Retrieval-Augmented Generation (RAG). The system uses agent orchestration with tool calling for scoped actions like searching portfolio data, sending emails, and generating WhatsApp contact links.

```
┌──────────────────────────────────────────────────────────────────┐
│                         Internet                                 │
└──────────┬───────────────────────────────────────┬───────────────┘
           │                                       │
           ▼                                       ▼
┌──────────────────────┐             ┌──────────────────────────────┐
│   Vite + React SPA   │             │    FastAPI Backend           │
│   (Existing Portfolio)│             │                              │
│                      │             │  ┌────────────────────────┐  │
│  ┌────────────────┐  │   REST     │  │  Agent Orchestrator    │  │
│  │ ChatBot Widget │──┼───────────┼─┼─▶ (Pydantic AI)         │  │
│  │                │  │            │  │  - Tool selection      │  │
│  │ - Chat UI      │  │            │  │  - Context building    │  │
│  │ - Email form   │  │            │  │  - Response generation │  │
│  │ - WhatsApp link│  │            │  └───────────┬────────────┘  │
│  └────────────────┘  │            │              │               │
│                      │            │     ┌────────┼────────┐      │
│  Hosted: Netlify     │            │     ▼        ▼        ▼      │
└──────────────────────┘            │  ┌────┐ ┌──────┐ ┌───────┐  │
                                    │  │RAG │ │Tools │ │Guard  │  │
                                    │  │    │ │      │ │rails  │  │
                                    │  └────┘ └──────┘ └───────┘  │
                                    │                              │
                                    │  ┌────────────────────────┐  │
                                    │  │  Provider Abstraction  │  │
                                    │  │  ┌─────┐ ┌──────┐     │  │
                                    │  │  │Groq │ │Gemini│ ...  │  │
                                    │  │  └─────┘ └──────┘     │  │
                                    │  └────────────────────────┘  │
                                    │                              │
                                    │  Dockerized                  │
                                    │  Hosted: Railway             │
                                    └──────────────────────────────┘
```

---

## Tech Stack

### Frontend (Existing Portfolio — Vite + React)

| Technology | Purpose |
|-----------|---------|
| React 18 | UI framework |
| Vite | Build tool |
| TailwindCSS | Styling |
| Framer Motion | Animations |
| React Router | Client-side routing |
| Hosting: **Netlify** (free tier) |

The chatbot is a new component added to the existing SPA. No rewrite needed.

### Backend (New — FastAPI)

| Technology | Purpose |
|-----------|---------|
| **FastAPI** | REST API framework |
| **Pydantic AI** | Agent orchestration (tool calling, context management) |
| **ChromaDB** | Vector store (embedded, regenerated on deploy) |
| **FastEmbed** | Embedding model (lightweight, runs in-process) |
| **slowapi** | Rate limiting (in-memory, no Redis needed) |
| **Resend** | Email sending (free tier: 100 emails/day) |
| Hosting: **Railway** (Dockerized) |

### AI Layer

| Component | Choice | Why |
|-----------|--------|-----|
| **LLM Provider** | Groq API (free) / Gemini API (free) | Both have generous free tiers |
| **Embedding Model** | `FastEmbed BAAI/bge-small-en-v1.5` | Lightweight, in-process, no PyTorch needed |
| **Vector DB** | ChromaDB (embedded mode) | File-based, regenerated on each deploy |
| **Agent Framework** | Pydantic AI | Type-safe, minimal boilerplate, built-in tool support |

---

## Core Flows

### 1. Chat Flow

```
Visitor Message
       │
       ▼
┌──────────────────┐
│  Guardrails       │── If out of scope → polite rejection
│  (Scope Check)    │
└──────┬───────────┘
       │ (in scope)
       ▼
┌──────────────────┐
│  Pydantic AI     │── Selects tool(s) based on intent
│  Agent           │
│                  │  Tools available:
│  ┌────────────┐  │  • portfolio_search(query) → ChromaDB
│  │ Tool Router │  │  • resume_search(query) → ChromaDB
│  └────────────┘  │  • github_search(query) → GitHub API
│                  │  • certificate_search(query) → ChromaDB
│                  │  • blog_search(query) → ChromaDB
│                  │  • get_contact_info() → static
│                  │  • send_email(name, email, msg) → Resend
│                  │  • generate_whatsapp_link(msg) → wa.me URL
│                  │  • web_search(query) → restricted domains
└──────┬───────────┘
       │ (tool results + conversation history)
       ▼
┌──────────────────┐
│  LLM Provider    │── Generates natural language response
│  (Groq/Gemini)   │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Response        │── Returns to visitor
│  Sanitization    │
└──────────────────┘
```

### 2. RAG Pipeline

```
┌─────────────────────┐
│  knowledge/          │  Markdown files committed to repo
│  ├── resume.md       │
│  ├── projects/       │
│  ├── certificates/   │
│  ├── case_studies/   │
│  ├── blogs/          │
│  └── personality.md  │  ← NEW: defines voice & tone
└─────────┬───────────┘
          │ read during Docker build
          ▼
┌─────────────────────┐
│  Embedding Pipeline  │  FastEmbed → vector chunks
│  (build step)        │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  ChromaDB Index      │  Written to disk in the container
│  (persistent volume) │  Rebuilt on every deploy
└─────────────────────┘
          │
          ▼  (at query time)
┌─────────────────────┐
│  Similarity Search   │  Top-K chunks retrieved
│  (cosine similarity) │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Context Assembly    │  Injected into LLM prompt
│  + Personality Spec  │
└─────────────────────┘
```

### 3. Email Flow

```
Visitor → "I want to contact Wesley"
       │
       ▼
Bot asks for: name, email, message
       │
       ▼
Visitor provides info
       │
       ▼
Bot shows summary and asks for confirmation
       │
       ▼
Visitor confirms
       │
       ▼
Bot calls send_email tool
       │
       ▼
Resend API delivers email to peterwesley484@gmail.com
       │
       ▼
Bot confirms to visitor
```

### 4. WhatsApp Flow

```
Visitor → "I want to WhatsApp Wesley"
       │
       ▼
Bot asks for: name, message
       │
       ▼
Bot generates wa.me link with pre-filled message
       │
       ▼
Returns: https://wa.me/254114578444?text=...
       │
       ▼
Visitor clicks → opens WhatsApp
```

---

## System Prompt Design

The system prompt has two layers:

### Layer 1: Static Personality Spec (`knowledge/personality.md`)

Defines voice, tone, identity, and behavioral rules — crafted from Wesley's actual writing patterns.

Key sections:
- Identity & background
- Voice principles (em-dash rhythm, contrast framing, direct declarations)
- Example Q&A pairs (few-shot examples)
- Rejection templates
- Things to NEVER say

### Layer 2: Dynamic Context (RAG results)

Retrieved chunks from the vector database are injected at query time:

```
You are Wesley's digital twin.

## Personality & Voice
{personality_spec_content}

## Example Responses (match this tone)
{example_qa_content}

## What I Know About This Topic
{retrieved_documents}

## Rules
{guardrails}

## Conversation History
{recent_messages}
```

---

## Directory Structure

```
portfolio-agent/
│
├── api/
│   ├── __init__.py
│   ├── routes.py            # FastAPI route definitions
│   └── schemas.py           # Pydantic request/response models
│
├── agents/
│   ├── __init__.py
│   ├── orchestrator.py      # Pydantic AI agent setup, tool registration
│   └── context.py           # System prompt builder
│
├── providers/
│   ├── __init__.py
│   ├── base.py              # Abstract LLM provider interface
│   ├── groq.py              # Groq API provider
│   ├── gemini.py            # Google Gemini provider
│   └── ollama.py            # Ollama provider (future)
│
├── rag/
│   ├── __init__.py
│   ├── chroma.py            # ChromaDB setup, query interface
│   ├── embeddings.py        # FastEmbed wrapper
│   └── indexer.py           # Build index from markdown knowledge base
│
├── tools/
│   ├── __init__.py
│   ├── portfolio.py         # Portfolio/project search tool
│   ├── resume.py            # Resume search tool
│   ├── github.py            # GitHub API search tool
│   ├── certificates.py      # Certificate search tool
│   ├── blog.py              # Blog search tool
│   ├── case_studies.py      # Case study search tool
│   ├── email.py             # Email sending tool (Resend)
│   ├── whatsapp.py          # WhatsApp link generator
│   ├── contact.py           # Static contact info tool
│   └── web_search.py        # Restricted web search tool
│
├── security/
│   ├── __init__.py
│   ├── guardrails.py        # Scope validation, prompt injection detection
│   ├── rate_limit.py        # slowapi configuration
│   └── sanitize.py          # Input/output sanitization
│
├── knowledge/
│   ├── resume.md            # Resume content
│   ├── personality.md       # Personality spec + voice instructions
│   ├── example_qa.md        # Few-shot Q&A examples
│   ├── projects/            # Individual project pages
│   ├── certificates/        # Certificate descriptions
│   ├── case_studies/        # Case study documents
│   └── blogs/               # Blog posts
│
├── main.py                  # FastAPI app entry point
├── Dockerfile               # Multi-stage Docker build
├── docker-compose.yml       # Local development setup
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
└── README.md                # Project documentation
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/chat` | Main chat endpoint (accepts messages, returns response) |
| `POST` | `/api/chat/stream` | Streaming chat endpoint (SSE) |
| `GET`  | `/api/health` | Health check + model status |
| `GET`  | `/api/tools` | List available tools and descriptions |

### Request/Response Schemas

**POST /api/chat**

```json
// Request
{
  "messages": [
    {"role": "user", "content": "Tell me about your projects"}
  ],
  "session_id": "abc123",
  "stream": false
}

// Response
{
  "reply": "I've worked on several projects across backend engineering...",
  "tool_used": "portfolio_search",
  "session_id": "abc123"
}
```

---

## Security Architecture

### Layered Defense

```
Layer 1: Rate Limiting (slowapi)
  ├── 10 requests/minute per IP
  ├── 100 requests/day per IP
  └── 1 email send per 10 minutes per IP

Layer 2: Scope Validation (guardrails.py)
  ├── Check intent before LLM call
  └── Reject off-topic prompts with polite redirect

Layer 3: Prompt Injection Detection
  ├── Scan for "ignore instructions", "act as", etc.
  └── Strip or reject suspicious content

Layer 4: Tool Permissions
  ├── Agent can only call registered tools
  └── Web search restricted to trusted domains

Layer 5: Retrieval Confidence
  ├── Minimum similarity threshold for RAG results
  └── "I can't find that in my portfolio" fallback

Layer 6: Output Sanitization
  ├── Strip sensitive patterns from responses
  └── Never reveal system prompt
```

---

## Deployment Architecture

### Production (Railway)

```
┌─────────────────┐     ┌──────────────────────────────────┐
│  Netlify         │     │  Railway                         │
│  (Frontend SPA)  │     │                                  │
│                  │     │  ┌───────────────────────────┐   │
│  portfolio.      │     │  │  Docker Container         │   │
│  example.com     │────▶│  │                           │   │
│                  │     │  │  FastAPI (uvicorn)        │   │
│  ChatBot.jsx ────┤     │  │  │                       │   │
│  fetches from ───┤     │  │  ├── ChromaDB (volume)   │   │
│  api.railway.com │     │  │  ├── slowapi (memory)    │   │
└─────────────────┘     │  │  └── Knowledge (bundled)  │   │
                         │  └───────────────────────────┘   │
                         │                                  │
                         │  Groq API (external)              │
                         │  Resend API (external)            │
                         │  GitHub API (external)            │
                         └──────────────────────────────────┘
```

### Local Development

```bash
# Start with Docker Compose
docker compose up

# Frontend: http://localhost:5173
# Backend:  http://localhost:8000
# Docs:     http://localhost:8000/docs
```

---

## Data Flow During Docker Build

```dockerfile
# Multi-stage Dockerfile

# Stage 1: Build RAG index
FROM python:3.12-slim AS builder
COPY knowledge/ /app/knowledge/
RUN python -c "
    from rag.indexer import build_index
    build_index('knowledge/', 'index/')
"

# Stage 2: Run application
FROM python:3.12-slim
COPY --from=builder /app/index/ /app/index/
COPY . /app/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

The vector index is rebuilt on every deploy — no persistent storage needed. ChromaDB loads from the pre-built index at startup.

---

## Environment Variables

```bash
# LLM Provider (choose one or both)
GROQ_API_KEY=           # Free tier: ~2000 requests/day
GEMINI_API_KEY=         # Free tier: 60 requests/min

# Email
RESEND_API_KEY=         # Free tier: 100 emails/day

# GitHub
GITHUB_TOKEN=           # Free: 5000 requests/hour

# Optional: for web search tool
TAVILY_API_KEY=         # Free tier: 1000 requests/month

# App
CORS_ORIGINS=https://yourportfolio.com
RATE_LIMIT_PER_MINUTE=10
RATE_LIMIT_PER_DAY=100
```

---

## Cost Breakdown

| Service | Cost | Notes |
|---------|------|-------|
| Railway (FastAPI) | ~$5/month | Shared CPU, 1GB RAM, includes volume |
| Groq free API | $0 | 2000 requests/day limit |
| Resend free tier | $0 | 100 emails/day |
| GitHub API free tier | $0 | 5000 requests/hour |
| Netlify free tier | $0 | Frontend hosting |
| **Total** | **~$5/month** | |

---

## Future Upgrades

| Feature | Architecture Impact |
|---------|-------------------|
| Ollama on VPS | Add `providers/ollama.py`, swap API URL in env |
| Voice conversations | WebSocket streaming, browser speech API |
| Memory between sessions | Add SQLite or Redis for conversation persistence |
| Recruiter mode | Different system prompt, focus on experience + resume |
| Calendar scheduling | Add calendar tool + Calendly/Cal API integration |
| Analytics dashboard | Log to SQLite, expose `/api/analytics` endpoint |
| GitHub code search | Expand `tools/github.py` with code search API |
