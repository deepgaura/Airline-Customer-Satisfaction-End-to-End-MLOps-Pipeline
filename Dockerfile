# syntax=docker/dockerfile:1.7

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# LightGBM needs this
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install only runtime deps; BuildKit cache speeds up repeat builds
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy app last to maximize layer cache
COPY . .

# Expose Flask port (adjust if different)
EXPOSE 5000

CMD ["python", "application.py"]
