# Kubernetes Microservices Project with Helm and Autoscaling

This project demonstrates a microservices architecture deployed on Kubernetes using Helm for packaging and deployment. The application consists of three primary services: `frontend`, `customer-management`, and `customer-web-server`. Additionally, the application uses MongoDB as a database and Kafka for messaging. The application is configured with Horizontal Pod Autoscalers (HPA) for autoscaling based on CPU and memory usage.

## Table of Contents

- [Project Structure](#project-structure)
- [Components](#components)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Testing Autoscaling](#testing-autoscaling)
- [Cleanup](#cleanup)

## Project Structure

## Components

### Frontend

- **Dockerfile**: `app/frontend/Dockerfile`
- **Code**: `app/frontend/app.py`, `app/frontend/static/app.js`, `app/frontend/templates/index.html`

### Customer Management Service

- **Dockerfile**: `app/customer-management/Dockerfile`
- **Code**: `app/customer-management/customerManagement.py`, `app/customer-management/requirements.txt`

### Customer Web Server

- **Dockerfile**: `app/customer-webServer/Dockerfile`
- **Code**: `app/customer-webServer/customer-webServer.py`, `app/customer-webServer/requirements.txt`

### MongoDB

- **Kubernetes Manifests**: `deployment/templates/mongodb-*`

### Ingress

- **Ingress Manifest**: `deployment/ingress.yaml`

## Prerequisites

- Kubernetes cluster
- Helm
- AWS CLI (for configuring AWS EKS and ALB Ingress Controller)
- kubectl

## Installation

1. **Clone the repository**:

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Build and push Docker images**:

    Modify `app/build-and-push.sh` to update the ECR registry and version as per your requirements, then run:

    ```sh
    cd app
    ./build-and-push.sh
    ```

3. **Install the Helm chart**:

    ```sh
    cd ../deployment
    helm upgrade --install application .
    ```

4. **Verify the deployment**:

    ```sh
    kubectl get all
    ```

## Configuration

The Helm chart values can be configured by modifying the `values.yaml` file. Key configuration options include:

### `frontend`

- `image`: Docker image for the frontend.
- `port`: Port for the frontend service.
- `replicas`: Number of replicas for the frontend deployment.
- `serviceName`: Name of the frontend service.
- `customerWebServerUrl`: URL of the customer web server service.
- `customerManagementUrl`: URL of the customer management service.

### `customerManagement`

- `image`: Docker image for the customer management service.
- `port`: Port for the customer management service.
- `replicas`: Number of replicas for the customer management deployment.
- `mongoHost`: MongoDB host.
- `mongoPort`: MongoDB port.
- `kafkaBroker`: Kafka broker.
- `kafkaGroupId`: Kafka group ID.
- `mongoDatabase`: MongoDB database name.
- `mongoCollection`: MongoDB collection name.

### `customerWebServer`

- `image`: Docker image for the customer web server service.
- `port`: Port for the customer web server service.
- `replicas`: Number of replicas for the customer web server deployment.
- `kafkaBroker`: Kafka broker.
- `managementServiceHost`: Hostname for the customer management service.
- `managementServicePort`: Port for the customer management service.

### `mongo`

- `image`: Docker image for MongoDB.
- `port`: Port for MongoDB.
- `replicas`: Number of replicas for MongoDB deployment.
- `storage`: Persistent volume size for MongoDB.
- `hostPath`: Host path for the persistent volume.

## Testing Autoscaling

1. **Simulate Load**:

    ```sh
    kubectl run -i --tty load-generator --image=busybox /bin/sh
    ```

2. **Generate CPU Load**:

    Inside the container, run a loop to generate CPU load:

    ```sh
    while true; do wget -q -O- http://<your-service-name>; done
    ```

    Replace `<your-service-name>` with the appropriate service name.

3. **Monitor HPA**:

    ```sh
    kubectl get hpa
    ```

    Ensure that the HPA scales the pods based on the load.

## Cleanup

To remove the Helm release and clean up the resources:

```sh
helm uninstall application
```

To remove the generated load pod:
```
kubectl delete pod load-generator
```




# Customer Purchase System

## Setup



# installing the metrixs server 
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# installing kafka 
kubectl apply -f 'https://strimzi.io/install/latest?namespace=default' -n default

kubectl get pods

kubectl get crds | grep kafka


kubectl apply -f https://strimzi.io/examples/latest/kafka/kafka-ephemeral.yaml -n default
or 


kubectl get pods
```
NAME                                          READY   STATUS    RESTARTS      AGE
my-cluster-entity-operator-7dfb85ccf9-28dqd   3/3     Running   0             95s
my-cluster-kafka-0                            1/1     Running   0             118s
my-cluster-kafka-1                            1/1     Running   0             118s
my-cluster-kafka-2                            1/1     Running   0             118s
my-cluster-zookeeper-0                        1/1     Running   0             2m21s
my-cluster-zookeeper-1                        1/1     Running   0             2m21s
my-cluster-zookeeper-2                        1/1     Running   0             2m21s
strimzi-cluster-operator-f696c85f7-9fggx      1/1     Running   0             7m49s
```

kubectl get services

```
NAME                          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                               AGE
kubernetes                    ClusterIP   10.96.0.1       <none>        443/TCP                               10m33s
my-cluster-kafka-bootstrap    ClusterIP   10.98.94.157    <none>        9091/TCP,9092/TCP,9093/TCP            3m12s
my-cluster-kafka-brokers      ClusterIP   None            <none>        9090/TCP,9091/TCP,9092/TCP,9093/TCP   3m12s
my-cluster-zookeeper-client   ClusterIP   10.104.185.52   <none>        2181/TCP                              3m35s
my-cluster-zookeeper-nodes    ClusterIP   None            <none>        2181/TCP,2888/TCP,3888/TCP            3m35s
```
### Prerequisites

- Docker
- Kubernetes
- kubectl
- Kafka

### Steps

1. Deploy MongoDB:
   ```bash
   kubectl apply -f mongo-pvc.yaml
   kubectl apply -f mongo-deployment.yaml





 # push and buils managment-server 
 docker build -t customer-management:1.0.0 app/customer-management/python
 docker tag customer-management:1.0.0 851725517080.dkr.ecr.eu-west-1.amazonaws.com/customer-management:1.0.0
 docker push 851725517080.dkr.ecr.eu-west-1.amazonaws.com/customer-management:1.0.0



 # push and buils web-server 
 docker build -t customer-web-server:1.0.0 app/customer-webServer/python
 docker tag customer-web-server:1.0.0 851725517080.dkr.ecr.eu-west-1.amazonaws.com/customer-web-server:1.0.0
 docker push 851725517080.dkr.ecr.eu-west-1.amazonaws.com/customer-web-server:1.0.0


 # push and buils frontend
 docker build --platform=linux/amd64 -t unity-frontend .
 docker build -t unity-frontend .
 docker tag unity-frontend:1.0.1 851725517080.dkr.ecr.eu-west-1.amazonaws.com/unity-frontend:1.0.1
 docker push 851725517080.dkr.ecr.eu-west-1.amazonaws.com/unity-frontend:1.0.1


 #login to eks 
 aws eks  update-kubeconfig --name orasraf-cluster




DEBUGING KAFKA
 
to add items to kafka manualy 
kubectl run kafka-producer -ti --image=bitnami/kafka:latest --rm=true --restart=Never -- bash

kafka-console-producer.sh --broker-list my-cluster-kafka-bootstrap:9092 --topic purchase
>{"username": "testuser_cli", "userid": "cli001", "price": 150}

kafka-console-consumer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic purchase --from-beginning



1.Send Purchase Data:
  curl -X POST http://customer-web-server-service:3001/buy -H "Content-Type: application/json" -d '{"username": "new_testuser", "userid": "user009", "price": 500}'

2.Consume Messages:
  curl http://customer-management-service:3000/consume

3. Verify Data in MongoDB:
  curl http://customer-management-service:3000/purchases

4. Verify Data via Web Server:
  curl http://customer-web-server-service:3001/getAllUserBuys



######################################


1. Connect to the MongoDB Pod:
  kubectl exec -it <mongo-pod-name> -- mongo

2. Switch to the Database:
  mongo
  use mydatabase

3. List Collections:
    show collections

4. Find All Documents in the Purchases Collection:
  db.purchases.find().pretty()



