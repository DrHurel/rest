# Use a lightweight Python image
FROM python:3.10-slim

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive


# Set the working directory
WORKDIR /app


COPY ./docker/hotel-mountain/ .
COPY ./docker/requirement.txt .

# Install system dependencies, including PostgreSQL development libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirement.txt

COPY ./hotel/hotel.py .
COPY ./hotel/hotel.yaml .
COPY ./hotel/hotel.ini .



# Expose the Uvicorn port
EXPOSE 2345

# Command to run Uvicorn
CMD ["uvicorn", "hotel:app",  "--port", "2345","--host","0.0.0.0"]
