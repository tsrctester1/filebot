# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add the current directory contents into the container at /app
ADD . /app

# Run filebot.py when the container launches
CMD ["python", "filebot.py"]

