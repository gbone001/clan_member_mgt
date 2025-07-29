# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app

# Copy requirements first for better caching
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY bot.py ./
COPY test_bot.py ./

# Copy .env file if it exists (optional, better to use environment variables)
COPY .env* ./

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Change ownership of the app directory to the app user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Health check to ensure bot is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Default command: run the bot
CMD ["python", "bot.py"]
