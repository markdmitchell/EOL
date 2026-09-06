# Production Multi-Stage Dockerfile for Software EOL/EOS Database Portal
FROM python:3.11-slim

# Prevent Python from writing pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8501

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy codebase
COPY . .

# Initialize and seed database
RUN python seed_db.py

# Expose Streamlit port
EXPOSE 8501

# Healthcheck for container orchestrators
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Launch Streamlit app
CMD ["streamlit", "run", "app.py", "--server.headless", "true", "--server.address", "0.0.0.0", "--server.port", "8501"]
