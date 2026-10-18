# Exercise 2 – Deploy a Flask App on Minikube Using kubectl and YAML

## Objective

Learn Kubernetes basics by deploying a Flask application on a single-node Minikube cluster using Docker, kubectl, and YAML configuration files.

## Project Overview

This project deploys a simple Flask web application on Kubernetes. The application listens on port `15000` and returns the message:

`Hello from Flask on Kubernetes!`

The application is packaged into a Docker image, deployed using a Kubernetes Deployment, and exposed through a NodePort Service.

## Project Files

- `app.py` — Flask application.
- `Dockerfile` — Defines the Docker image.
- `flask-deployment.yaml` — Defines the Kubernetes Deployment and Service.
- `run.sh` — Automates the build and deployment commands.
- `logs/` — Stores test logs.
- `screenshots/` — Stores testing and deployment screenshots.
- `QUESTION.md` — Original assignment instructions.

## Technologies Used

- Python
- Flask
- Docker
- Kubernetes
- Minikube
- kubectl
- YAML
- Bash

## Application

The Flask application defines a route at `/` that returns:

`Hello from Flask on Kubernetes!`

The application listens on `0.0.0.0:15000`, allowing it to accept connections through the container's network interface.

## Docker Configuration

The Dockerfile uses the `python:3.8-slim` base image, sets `/app` as the working directory, copies the application files, installs Flask, and starts the application with Python.

## Kubernetes Configuration

The file `flask-deployment.yaml` defines two Kubernetes resources.

### Deployment

- Deployment name: `flask-app`
- Replicas: `1`
- Container image: `flask-app:latest`
- Image pull policy: `Never`
- Container port: `15000`

The Deployment manages the application Pod and maintains the desired number of replicas.

### Service

- Service name: `flask-app-service`
- Service type: `NodePort`
- Service port: `15000`
- Target port: `15000`

The Service routes requests to the application Pod.

## How to Run

### 1. Start Minikube

```bash
minikube start
```

### 2. Configure Docker to Use Minikube's Docker Daemon

```bash
eval $(minikube docker-env)
```

### 3. Build the Docker Image

```bash
docker build -t flask-app .
```

### 4. Deploy the Application

```bash
kubectl apply -f flask-deployment.yaml
```

### 5. Verify the Deployment

```bash
kubectl get deployments
kubectl get pods -l app=flask-app
kubectl describe deployment flask-app
kubectl logs <pod-name>
kubectl get services
```

Confirm that the Deployment has one available replica and the Pod is running.

### 6. Access the Application

```bash
minikube service flask-app-service --url
```

Use the URL printed by the command to access the application from a browser or with `curl`, following the networking requirements of the Minikube driver.

Expected response:

```text
Hello from Flask on Kubernetes!
```

## Verification

The application can be verified by checking the Deployment status, Pod status, application logs, Service configuration, and HTTP response.

Screenshots and logs can be used to document the actual results of these checks.

## Key Concepts Learned

- Creating a Flask application.
- Building a Docker image.
- Running a local Kubernetes cluster with Minikube.
- Deploying an application using Kubernetes YAML.
- Understanding Pods, Deployments, and Services.
- Using `kubectl` to inspect Kubernetes resources.
- Exposing an application through a NodePort Service.
- Accessing a deployed application using the Minikube service URL.

## Conclusion

This exercise demonstrates how to package a Flask application into a Docker image, deploy it on Kubernetes using Minikube, and expose it through a Kubernetes Service. It provides practical experience with containerization, Kubernetes resource configuration, deployment verification, and application access.