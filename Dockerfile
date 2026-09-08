# Dockerfile for CI Bottleneck Analyzer

# Use official lightweight Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if any)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . ./

# Expose ports
EXPOSE 8000 8501

# Default command runs both backend and frontend via Docker Compose (no default)
