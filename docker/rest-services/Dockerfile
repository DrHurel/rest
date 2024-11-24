# Use a lightweight Python image
FROM python:3.10-slim

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive


# Set the working directory
WORKDIR /app

ARG REST_SERVICE
ARG SERVICE_ID
ARG EXPOSED_PORT

COPY ./docker/${SERVICE_ID}/ . 
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

COPY ./${REST_SERVICE}/ .
# Expose the Uvicorn port
EXPOSE ${EXPOSED_PORT}


ENV SERVICE=${REST_SERVICE}
ENV PORT=${EXPOSED_PORT}

# Command to run Uvicorn
CMD uvicorn $SERVICE:app --port $PORT --host "0.0.0.0"
