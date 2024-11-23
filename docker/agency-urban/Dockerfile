# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app


COPY ./docker/agency-urban/ .
COPY ./docker/requirement.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirement.txt

COPY ./agency/agency.py .
COPY ./agency/agency.yaml .
COPY ./agency/agency.ini .


# Expose the Uvicorn port
EXPOSE 5555

# Command to run Uvicorn
CMD ["uvicorn", "agency:app", "--port", "5555","--host","0.0.0.0"]
