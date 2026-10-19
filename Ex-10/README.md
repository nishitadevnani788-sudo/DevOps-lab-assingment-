# Multi-Node Kubernetes Cluster with Multiple Applications and Replicasets

## Objective
To deploy two Python Flask applications, Product Catalog and Shopping Cart, on a three-node Minikube Kubernetes cluster. The exercise demonstrates multiple replicas, pod distribution across nodes, Kubernetes Deployments, Services, and application testing.

## Storyboard
The e-commerce application consists of two services:

- **Product Catalog (AppA):** Provides information about available products.
- **Shopping Cart (AppB):** Allows users to view and add items to their shopping cart.

To improve availability and fault tolerance, the Product Catalog runs two replicas and the Shopping Cart runs three replicas.

## Prerequisites
- Docker installed and running
- Minikube installed
- kubectl installed
- Python and Flask for local application development
- Git installed
- Basic knowledge of Docker and Kubernetes

## Step 1: Clean Up Existing Minikube Cluster

Stop and delete the default Minikube profile if required:

```bash
minikube stop
minikube delete
```

**Note:** These commands delete the default Minikube cluster. Do not run them if you need to preserve another exercise's cluster.

## Step 2: Create a Three-Node Minikube Cluster

```bash
minikube start --nodes 3 -p devops-multinode --force
```

This creates a Minikube profile named `devops-multinode` with three nodes.

Verify the cluster:

```bash
kubectl get nodes
```

## Step 3: Enable the Minikube Registry Add-on

Enable the registry add-on:

```bash
minikube -p devops-multinode addons enable registry
```

This prepares the cluster's registry add-on for working with container images.

## Step 4: Create the Product Catalog Application

Create a file named `product_catalog.py`:

```python
from flask import Flask, jsonify

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop", "price": 1200},
    {"id": 2, "name": "Phone", "price": 800},
    {"id": 3, "name": "Headphones", "price": 150},
]

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
```

The `/products` endpoint returns a list of available products in JSON format.

## Step 5: Create the Shopping Cart Application

Create a file named `shopping_cart.py`:

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

cart = []

@app.route("/cart", methods=["GET"])
def get_cart():
    return jsonify(cart)

@app.route("/cart", methods=["POST"])
def add_to_cart():
    item = request.json
    cart.append(item)
    return jsonify(cart), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
```

The `/cart` endpoint supports viewing the cart and adding items using a POST request.

## Step 6: Dockerize Both Applications

### Product Catalog Dockerfile

Create `Dockerfile.product`:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY product_catalog.py /app/
RUN pip install flask
CMD ["python", "product_catalog.py"]
```

### Shopping Cart Dockerfile

Create `Dockerfile.shopping`:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY shopping_cart.py /app/
RUN pip install flask
CMD ["python", "shopping_cart.py"]
```

### Build the Docker Images

```bash
docker build -t product-catalog:latest -f Dockerfile.product .
docker build -t shopping-cart:latest -f Dockerfile.shopping .
```

Verify the images:

```bash
docker images
```

## Step 7: Load Images into Minikube

```bash
minikube -p devops-multinode image load product-catalog:latest
minikube -p devops-multinode image load shopping-cart:latest
```

Verify the images in Minikube:

```bash
minikube -p devops-multinode ssh -- docker images
```

## Step 8: Create Kubernetes Deployments

### Product Catalog Deployment

Create `product_catalog_deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: product-catalog
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: product-catalog
  template:
    metadata:
      labels:
        app: product-catalog
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels:
                  app: product-catalog
              topologyKey: kubernetes.io/hostname
      containers:
        - name: product-catalog-container
          image: product-catalog:latest
          imagePullPolicy: Never
          ports:
            - containerPort: 80
```

### Shopping Cart Deployment

Create `shopping_cart_deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: shopping-cart
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: shopping-cart
  template:
    metadata:
      labels:
        app: shopping-cart
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels:
                  app: shopping-cart
              topologyKey: kubernetes.io/hostname
      containers:
        - name: shopping-cart-container
          image: shopping-cart:latest
          imagePullPolicy: Never
          ports:
            - containerPort: 80
```

The pod anti-affinity rules request that replicas of each application run on different nodes.

**Note:** Both deployments use the `default` namespace so that they can be applied without creating an additional namespace.

## Step 9: Create Kubernetes Services

### Product Catalog Service

Create `product_catalog_service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: product-catalog-service
  namespace: default
spec:
  selector:
    app: product-catalog
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: NodePort
```

### Shopping Cart Service

Create `shopping_cart_service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: shopping-cart-service
  namespace: default
spec:
  selector:
    app: shopping-cart
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: NodePort
```

## Step 10: Apply the Configurations

Apply both deployments:

```bash
kubectl apply -f product_catalog_deployment.yaml
kubectl apply -f shopping_cart_deployment.yaml
```

Apply both services:

```bash
kubectl apply -f product_catalog_service.yaml
kubectl apply -f shopping_cart_service.yaml
```

## Step 11: Verify the Deployments and Pod Distribution

Check the nodes:

```bash
kubectl get nodes
```

Check the deployments:

```bash
kubectl get deployments
```

Check the pods and their node assignments:

```bash
kubectl get pods -o wide
```

Check the services:

```bash
kubectl get services
```

### Expected Result

- Product Catalog: 2 running replicas on different nodes.
- Shopping Cart: 3 running replicas, ideally one per node.
- Both services should have endpoints corresponding to their application pods.

The exact pod names and IP addresses will vary by cluster.

## Step 12: Access the Product Catalog Service

Run:

```bash
minikube -p devops-multinode service product-catalog-service
```

Open the URL provided by Minikube and append `/products` to the URL.

Expected JSON response:

```json
[
  {"id": 1, "name": "Laptop", "price": 1200},
  {"id": 2, "name": "Phone", "price": 800},
  {"id": 3, "name": "Headphones", "price": 150}
]
```

## Step 13: Access the Shopping Cart Service

Run:

```bash
minikube -p devops-multinode service shopping-cart-service
```

Open the URL provided by Minikube and append `/cart` to the URL.

The initial response should be:

```json
[]
```

### Add an Item to the Cart

Use the service URL provided by Minikube:

```bash
curl -X POST http://127.0.0.1:YOUR_PORT/cart -H "Content-Type: application/json" -d "{\"id\": 1, \"name\": \"Laptop\", \"quantity\": 1}"
```

Replace `YOUR_PORT` with the actual port from your service URL.

Expected response:

```json
[
  {"id": 1, "name": "Laptop", "quantity": 1}
]
```

## Result
Deployed the Product Catalog application with two replicas and the Shopping Cart application with three replicas on a three-node Minikube cluster. Configured Kubernetes Deployments and NodePort Services and documented how to verify pod distribution and test application endpoints.

## Conclusion
This exercise demonstrates multi-node Kubernetes deployment, container image management, replica configuration