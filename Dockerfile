# Use a lightweight Python image
FROM python:3.11-slim

# Prevent .pyc and force unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Workdir
WORKDIR /app

# System deps (example: LightGBM runtime needs libgomp1)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Copy only dependency list first for better caching
# (Use ONE of these files, whichever you have)
COPY requirements.txt ./ 
# If you use pyproject.toml/poetry instead, copy those instead and adjust the install command.

# Install Python deps (no cache to keep image small)
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Now copy app code (keeps cache effective if only code changes)
COPY . .

# If you have a small trained model needed at runtime, ensure it exists at build time (Step 4)
# and is inside ./models/ so it gets copied here.

# Expose Flask port
EXPOSE 5000

# Start the app
CMD ["python", "application.py"]
