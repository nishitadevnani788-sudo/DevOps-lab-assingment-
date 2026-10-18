# Exercise 1 – Hello Pod (Kubernetes Getting Started)

Deploy an Nginx web server on a local Kubernetes cluster using Minikube and kubectl.

## Project Structure

- `run.sh` — Script to execute the Kubernetes setup commands
- `hello-pod.yaml` — Kubernetes Pod configuration
- `QUESTION.md` — Assignment instructions
- `README.md` — Exercise documentation
- `logs/` — Execution logs and verification results
- `screenshots/` — Screenshots of the exercise

## How It Works

1. Minikube starts a local Kubernetes cluster.
2. A Pod is created using the Nginx container image.
3. kubectl checks the Pod status.
4. A NodePort Service exposes the Nginx Pod.
5. Minikube provides access to the Nginx welcome page.

## Steps to Run

### 1. Start Minikube

```bash
minikube start
```

### 2. Create the Nginx Pod

```bash
kubectl run hello-k8s --image=nginx --port=80
```

### 3. Check Pod Status

```bash
kubectl get pods
```

### 4. Expose the Pod

```bash
kubectl expose pod hello-k8s --type=NodePort --port=80
```

### 5. Access the Nginx Service

```bash
minikube service hello-k8s
```

## Screenshots

The exercise includes screenshots of the Kubernetes Pod, Service, and Nginx welcome page.

## Verification Results

- Kubernetes cluster started successfully.
- Nginx Pod reached the Running state.
- NodePort Service was created successfully.
- Nginx welcome page was accessible through Minikube.

## Technologies Used

- Kubernetes
- Minikube
- kubectl
- Docker
- Nginx