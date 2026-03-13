FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	UV_LINK_MODE=copy

WORKDIR /app

RUN pip install --no-cache-dir uv

# Copy dependency metadata first to maximize Docker layer caching.
COPY pyproject.toml uv.lock README.md /app/
RUN uv sync --frozen --no-dev --no-install-project

# Copy application source and install the project itself.
COPY src /app/src
RUN uv sync --frozen --no-dev

EXPOSE 8000 8501

CMD ["uv", "run", "--no-sync", "uvicorn", "age_detection_service.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
