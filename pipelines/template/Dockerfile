# ──────────────────────────────────────────────
# {PIPELINE_NAME} — Dockerfile
# Reproducible pipeline execution environment.
# ──────────────────────────────────────────────

FROM python:3.11-slim

LABEL maintainer="LILA Lab <lila.lab0x@gmail.com>"
LABEL description="{PIPELINE_NAME} — LILA Lab pipeline for {LANGUAGE_NAME}"

WORKDIR /pipeline

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy pipeline code
COPY . .

# Default: run annotation help
CMD ["python3", "-c", "print('{PIPELINE_NAME} pipeline ready')"]
