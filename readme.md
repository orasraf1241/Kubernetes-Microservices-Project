# Kubernetes Microservices Project with Helm and Autoscaling

This project demonstrates a microservices architecture deployed on Kubernetes using Helm for packaging and deployment. 
The application consists of three primary services: `frontend`, `customer-management`, and `customer-web-server`. 
Additionally, the application uses MongoDB as a database and Kafka for messaging. 

## Table of Contents

- [Architecture](#architecture)
- [Components](#components)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Testing Autoscaling](#testing-autoscaling)
- [Debugging Kafka](#debugging-kafka)
- [Cleanup](#cleanup)

## Application Architecture
![Application Architecture Diagram](/image.png)
### MongoDB
- Store the user’s purchases in MongoDB.

### Customer Management API
1. Read & Write data into MongoDB.
2. Consume messages from Kafka.
3. GET route - Return all customer purchases.

### Customer Facing Web Server
1. Handle a “buy” request and publish the data object to Kafka (username, userid, price, timestamp).
2. Handle a “getAllUserBuys” and send a GET request to Customer Management service and present the response.

### Frontend
1. Button 1 named Buy - Send a purchase request.
2. Button 2 named getAllUserBuys - Display all purchase requests for the user.

### Autoscaling
autoscaling resources for the software components based CPU and RAM


## Prerequisites

- Kubernetes cluster
- Helm
- AWS CLI (for configuring AWS EKS and ALB Ingress Controller)
- kubectl

## Installation

1. **Clone the repository**:

    ```sh
    git clone https://github.com/orasraf1241/kafka-demo.git
    cd https://github.com/orasraf1241/kafka-demo.git
    ```

2. **Build and push Docker images**:

    Modify `app/build-and-push.sh` to update the ECR registry and version as per your requirements, then run:

    ```sh
    cd app
    ./build-and-push.sh
    ```
3. **Install kafka**:
```
k create  namespace kafka 
kubectl apply -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka


kubectl apply -f https://strimzi.io/examples/latest/kafka/kafka-ephemeral.yaml -n kafka
```

# Need to get this output 
kubectl get pods -n kafka
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

kubectl get services -n kafka

NAME                          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                               AGE
kubernetes                    ClusterIP   10.96.0.1       <none>        443/TCP                               10m33s
my-cluster-kafka-bootstrap    ClusterIP   10.98.94.157    <none>        9091/TCP,9092/TCP,9093/TCP            3m12s
my-cluster-kafka-brokers      ClusterIP   None            <none>        9090/TCP,9091/TCP,9092/TCP,9093/TCP   3m12s
my-cluster-zookeeper-client   ClusterIP   10.104.185.52   <none>        2181/TCP                              3m35s
my-cluster-zookeeper-nodes    ClusterIP   None            <none>        2181/TCP,2888/TCP,3888/TCP            3m35s
```

4. **Install the Helm chart**:

    ```sh
    cd ../deployment
    kubectl apply ingress.yaml
    helm upgrade --install application .
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



### Debugging Kafka

1. **Add items to Kafka manually**:
    ```
    kubectl run kafka-producer -ti --image=bitnami/kafka:latest --rm=true --restart=Never -- bash
    ```

    Inside the pod, run the following command to add items to Kafka:
    ```
    kafka-console-producer.sh --broker-list my-cluster-kafka-bootstrap:9092 --topic purchase
    >{"username": "testuser_cli", "userid": "cli001", "price": 150}
    ```

    To consume messages from Kafka:
    ```
    kafka-console-consumer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic purchase --from-beginning
    ```

2. **Send Purchase manually Data**:
    ```
    curl -X POST http://customer-web-server-service:3001/buy -H "Content-Type: application/json" -d '{"username": "new_testuser", "userid": "user009", "price": 500}'
    ```

3. **Consume Messages**:
    ```
    curl http://customer-management-service:3000/consume
    ```

4. **Verify Data in MongoDB**:
    ```
    curl http://customer-management-service:3000/purchases
    ```

5. **Verify Data via Web Server**:
    ```
    curl http://customer-web-server-service:3001/getAllUserBuys
    ```


### Accessing MongoDB

1. **Connect to the MongoDB Pod**:
    ```sh
    kubectl exec -it <mongo-pod-name> -- mongo
    ```

2. **Switch to the Database**:
    ```sh
    mongo
    use mydatabase
    ```

3. **List Collections**:
    ```sh
    show collections
    ```

4. **Find All Documents in the Purchases Collection**:
    ```sh
    db.purchases.find().pretty()
    ```


## Cleanup

To remove the Helm release and clean up the resources:

```sh
kubectl delete -f 'https://strimzi.io/install/latest?namespace=default' -n kafka

kubectl delete -f https://strimzi.io/examples/latest/kafka/kafka-ephemeral.yaml -n default

helm uninstall application
```