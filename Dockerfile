FROM tiangolo/uvicorn-gunicorn-fastapi:python3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the project files
COPY pyproject.toml uv.lock /app/

# Install dependencies
WORKDIR /app
RUN uv sync --frozen --no-install-project --no-dev

# Copy the application code
COPY ./api /app/app
