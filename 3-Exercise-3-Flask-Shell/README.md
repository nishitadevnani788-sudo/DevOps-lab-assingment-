# Exercise 3: Scaling Flask App Using ReplicaSets

## Objective
The objective of this exercise is to deploy a Flask application on Kubernetes using Minikube and ReplicaSets. It demonstrates how to manage multiple replicas, scale the application, and test pod self-healing.

## Application
The Flask application provides three endpoints:
- `/` – Displays application information.
- `/buy` – Simulates a product purchase.
- `/health` – Checks application health.

## Steps to Run

### 1. Build the Docker Image
Build the Docker image and make it available to Minikube.

```bash
docker build -t flashsale:1.0 .
minikube image load flashsale:1.0
```

### 2. Deploy the Application
Apply the Kubernetes configuration to create the ReplicaSet and Service.

```bash
kubectl apply -f flashsale-replicaset.yaml
```

### 3. Check the Replicas
Verify that the ReplicaSet is running with three replicas.

```bash
kubectl get pods
kubectl get rs
```

### 4. Scale the Application
Increase the number of replicas from three to five.

```bash
kubectl scale rs flashsale-rs --replicas=5
kubectl get pods
```

### 5. Test Self-Healing
Delete one of the running pods and check whether Kubernetes creates a replacement.

```bash
kubectl delete pod <pod-name>
kubectl get pods
```

### 6. Access the Application
Get the service URL using Minikube.

```bash
minikube service flashsale-svc --url
```

### 7. Test the Endpoints
Use the service URL to test the application endpoints.

```bash
curl http://<service-url>/
curl "http://<service-url>/buy?user=alice"
curl http://<service-url>/health
```

## Result
This exercise demonstrates deploying a Flask application using Kubernetes ReplicaSets, scaling from three to five replicas, and testing pod self-healing and application endpoints.