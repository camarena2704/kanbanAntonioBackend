# Get official base image
FROM python:3.13

# Set working directory
WORKDIR /usr/src/

# Set environment variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1
# Set Python path
ENV PYTHONPATH /usr/src/

# Install system dependencies
RUN apt-get update \
  && apt-get -y install git netcat-traditional gcc postgresql \
  && apt-get clean

# Install Python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Add application
COPY . .

# Run gunicorn
CMD gunicorn --bind 0.0.0.0:$PORT app.main:app -k uvicorn.workers.UvicornWorker