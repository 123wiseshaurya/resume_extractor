# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Create uploads directory with proper permissions
RUN mkdir -p /app/uploads && chmod 777 /app/uploads

# Copy project files
COPY . .

# Switch to non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Install requirements again for the non-root user
RUN pip install --no-cache-dir -r requirements.txt

# Ensure the uploads directory is accessible to the appuser
RUN chmod 777 /app/uploads

# Verify python-dotenv is installed
RUN python -c "import dotenv"

# Expose port
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5050"]
