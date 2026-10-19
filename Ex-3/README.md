# Exercise 3 – Scaling Flask App on a Single Node Using ReplicaSets

## Real-Life Use Case: E-commerce Flash Sale

During an e-commerce flash sale, website traffic can suddenly increase from hundreds to thousands of requests per minute. If the application runs on a single Pod, it may struggle to handle the increased traffic.

Kubernetes ReplicaSets help maintain multiple copies of the application. If a Pod fails or is deleted, the ReplicaSet automatically creates a replacement to maintain the desired number of replicas.

## Objective

- Understand Kubernetes Pods and ReplicaSets.
- Deploy a Flask application on Kubernetes.
- Scale the application from 3 to 5 replicas.
- Verify Pod status and distribution across nodes.
- Understand how ReplicaSets replace deleted Pods.

## Project Structure

- `app.py` — Flask application code.
- `Dockerfile` — Instructions to build the Docker image.
- `flashsale-replicaset.yaml` — ReplicaSet and Service configuration.
- `README.md` — Exercise documentation.
- `logs/` — Execution logs and verification results.
- `screenshots/` — Screenshots of the exercise.

## How It Works

1. Minikube starts a single-node Kubernetes cluster.
2. A Flask application simulates an e-commerce flash sale.
3. A Docker image packages the Flask application.
4. A ReplicaSet creates and maintains multiple application Pods.
5. A Kubernetes Service provides access to the application.
6. The ReplicaSet is scaled from 3 to 5 replicas.
7. When a Pod is deleted, Kubernetes automatically creates a replacement.

## Steps to Run

### 1. Start Minikube

Stop and delete an existing Minikube cluster if you want a fresh setup.

    minikube stop
    minikube delete

Start a single-node cluster.

    minikube start --nodes=1

Verify the node status.

    kubectl get nodes

### 2. Create the Flask Application

Create a file named `app.py`.

The application provides three endpoints:

- `/` — Displays a welcome message and the Pod hostname.
- `/buy` — Simulates a flash sale purchase