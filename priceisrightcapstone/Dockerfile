# =============================================================================
# The Price Is Right — Dockerfile
# Base : python:3.11-slim
# Author: Lalit Nayyar | lalitnayyar@gmail.com
# =============================================================================

FROM python:3.11-slim

WORKDIR /app

# ── System dependencies ───────────────────────────────────────────────────────
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        curl \
    && rm -rf /var/lib/apt/lists/*

# ── Python dependencies ───────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ── Pre-cache the embedding model weights (runs once at build time) ───────────
# Uses a try/except so a network hiccup during build does not fail the image.
# The model will be downloaded at first runtime if not cached here.
RUN python - <<'EOF'
try:
    from sentence_transformers import SentenceTransformer
    SentenceTransformer('all-MiniLM-L6-v2')
    print("Embedding model cached successfully.")
except Exception as e:
    print(f"WARNING: Could not pre-cache embedding model: {e}")
    print("Model will be downloaded at first runtime.")
EOF

# ── Application code ──────────────────────────────────────────────────────────
COPY . .

# ── Runtime setup ─────────────────────────────────────────────────────────────
RUN mkdir -p /app/data /app/tests/reports

ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1

# ── Ports ─────────────────────────────────────────────────────────────────────
EXPOSE 7860 8000

# ── Default command (overridden by docker-compose) ────────────────────────────
CMD ["python", "main.py", "--mode", "api"]
