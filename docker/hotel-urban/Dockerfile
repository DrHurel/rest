# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

COPY ./docker/hotel-urban/ .
COPY ./docker/requirement.txt .
# Install dependencies
RUN pip install -r requirement.txt

COPY ./hotel/hotel.py .
COPY ./hotel/hotel.yaml .
COPY ./hotel/hotel.ini .

# Expose the Uvicorn port
EXPOSE 5678

# Command to run Uvicorn
CMD ["uvicorn", "hotel:app", "--port", "5678","--host","0.0.0.0"]
