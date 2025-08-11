FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PORT=8080

# Expose the port
EXPOSE 8080

# Start the application with Uvicorn
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT}