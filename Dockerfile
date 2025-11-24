# --------------------
# STAGE 1: Builder
# --------------------
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies (optional depending on project)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# --------------------
# STAGE 2: Runtime (Final Image)
# --------------------
FROM python:3.11-slim

WORKDIR /app

# Copy only installed packages from builder
COPY --from=builder /root/.local /root/.local

# Ensure Python can find built packages
ENV PATH=/root/.local/bin:$PATH

# Copy your project
COPY . .    

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn demo:app --host 0.0.0.0 --port 8000"]

