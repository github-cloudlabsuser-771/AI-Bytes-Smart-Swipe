# Use an official Python runtime as a parent image
FROM python:3.9-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /ai_bytes_app

# Copy the service account JSON file into the container
COPY /apps/static/secrets/cap-ai-bytes-credentials.json /ai_bytes_app/service-account.json

# Set the environment variable GOOGLE_APPLICATION_CREDENTIALS to point to the service account JSON file
ENV GOOGLE_APPLICATION_CREDENTIALS=/ai_bytes_app/service-account.json

ENV HOST 0.0.0.0
ENV PORT=5085

# Copy the current directory contents into the container at /app
COPY . /ai_bytes_app

COPY requirements.txt .
# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5085 to allow communication to/from server
EXPOSE 5085

# Define environment variable
ENV NAME World

# running migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]
