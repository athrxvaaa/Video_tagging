# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies (ffmpeg for audio extraction)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all project files
COPY . .

# Expose the port (Render uses $PORT)
EXPOSE 8000

# Start the FastAPI app with uvicorn, using the $PORT environment variable
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 