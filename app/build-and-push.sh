#!/bin/bash

# Variables
ECR_REGISTRY="851725517080.dkr.ecr.eu-west-1.amazonaws.com"


CUSTOMER_MANAGEMENT_IMAGE_NAME="customer-management"
CUSTOMER_WEBSERVER_IMAGE_NAME="customer-web-server"
FRONTEND_IMAGE_NAME="unity-frontend"

CUSTOMER_MANAGEMENT_VERSION="1.0.12"
CUSTOMER_WEBSERVER_VERSION="1.1.0"
FRONTEND_VERSION="1.1.3"

# Function to build, tag, and push Docker images
build_and_push() {
  local app_dir=$1
  local image_name=$2
  local version=$3

  echo "Building Docker image for ${image_name}..."

  cd ${app_dir} || exit
  docker build -t ${image_name}:${version} .

  echo "Tagging Docker image ${image_name}:${version}..."
  docker tag ${image_name}:${version} ${ECR_REGISTRY}/${image_name}:${version}

  echo "Pushing Docker image ${image_name}:${version} to ECR..."
  docker push ${ECR_REGISTRY}/${image_name}:${version}

  cd ..
}

# Login to AWS ECR
echo "Logging in to AWS ECR..."
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin ${ECR_REGISTRY}

# Build, tag, and push customer-management
build_and_push "customer-management" ${CUSTOMER_MANAGEMENT_IMAGE_NAME} ${CUSTOMER_MANAGEMENT_VERSION}

# Build, tag, and push customer-webServer
build_and_push "customer-webServer" ${CUSTOMER_WEBSERVER_IMAGE_NAME} ${CUSTOMER_WEBSERVER_VERSION}

# Build, tag, and push unity-frontend
build_and_push "frontend" ${FRONTEND_IMAGE_NAME} ${FRONTEND_VERSION}

echo "Build, tag, and push process completed."
