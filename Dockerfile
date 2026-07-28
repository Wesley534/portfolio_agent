# ──────────────────────────────────────────────
# Stage 1: Build RAG index
# ──────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

# Install only the dependencies needed for indexing
RUN pip install --no-cache-dir fastembed chromadb==0.5.5

# Copy knowledge base and indexing code
COPY knowledge/ knowledge/
COPY rag/ rag/

# Build the vector index
RUN python -m rag.indexer --knowledge-dir knowledge/ --output-dir /index

# ──────────────────────────────────────────────
# Stage 2: Runtime
# ──────────────────────────────────────────────
FROM python:3.12-slim

WORKDIR /app

# Install runtime dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache

# Copy pre-built index from builder
COPY --from=builder /index/ /app/index/

# Copy application code (excludes .env, __pycache__ via .dockerignore)
COPY . .

# Create non-root user
RUN addgroup --system app && adduser --system --group app && \
    chown -R app:app /app
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
