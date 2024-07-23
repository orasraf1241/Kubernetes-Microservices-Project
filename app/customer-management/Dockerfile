# Dockerfile for customer-management
FROM --platform=linux/amd64 python:3.8-slim-buster as build

WORKDIR /usr/src/app

COPY requirements.txt ./


RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["python", "customerManagement.py"]
