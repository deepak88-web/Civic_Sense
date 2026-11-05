
FROM python:3.13-slim

WORKDIR /app

# Copy application source and configuration
COPY setup.py requirements.txt ./
COPY src/ ./src/
COPY config/ ./config/
COPY backend/ ./backend/

# Install production dependencies and CivicSense package
RUN pip install --no-cache-dir -r requirements.txt

# Application port
EXPOSE 8000

# Start FastAPI
CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
