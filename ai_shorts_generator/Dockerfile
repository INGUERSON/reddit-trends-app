FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    git \
    && rm -rf /var/lib/apt/lists/*

# Fix ImageMagick security policy for MoviePy
RUN sed -i 's/domain="path" rights="none" pattern="@\*"/domain="path" rights="read|write" pattern="@\*"/g' /etc/ImageMagick-6/policy.xml

WORKDIR /app

# Copy requirements and install
COPY ai_shorts_generator/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY ai_shorts_generator/ ./

# Command to run the pipeline
CMD ["python", "empire_pipeline.py"]
