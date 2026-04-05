# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

RUN pip install --no-cache-dir poetry==1.8.5

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.in-project true && \
    poetry install --no-interaction --no-ansi --without dev --no-root

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /app/.venv .venv

COPY src/ src/
COPY gradio_app.py .
COPY pyproject.toml .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
