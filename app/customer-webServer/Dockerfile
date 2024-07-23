# Use the official Python image as a base image
FROM  --platform=linux/amd64  python:3.8-slim-buster as build

# Set the working directory
WORKDIR /usr/src/app

# Copy requirements.txt and install dependencies
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 3001

# Command to run the application
CMD ["python", "customer-webServer.py"]
