# Exercise 10: Multi-Node Kubernetes Cluster

## Applications
- Product Catalog: returns a list of products; 2 replicas.
- Shopping Cart: supports GET and POST requests; 3 replicas.

## Files
- product_catalog.py
- shopping_cart.py
- Dockerfile.product
- Dockerfile.shopping
- product_catalog_deployment.yaml
- shopping_cart_deployment.yaml
- product_catalog_service.yaml
- shopping_cart_service.yaml

## Setup
Start a three-node Minikube profile named devops-multinode.
Build both Docker images, load them into Minikube, apply the deployments and services.

## Verification
Run `kubectl get nodes`
Run `kubectl get pods -o wide`
Run `kubectl get deployments`
Run `kubectl get services`

The deployments use required pod anti-affinity to distribute replicas across different nodes.
