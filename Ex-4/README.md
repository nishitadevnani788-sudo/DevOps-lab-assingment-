# Exercise 4 – Docker Networking with Multiple Containers

## Objective

Understand Docker networking concepts and configure a multi-container application using a custom bridge network.

## Scenario

Develop a multi-container application consisting of:

- Python Flask web server
- MySQL database
- Redis cache

All three containers are connected to the same custom Docker bridge network so they can communicate with each other.

## Project Structure

- `app.py` — Flask application code
- `requirements.txt` — Python dependencies
- `Dockerfile` — Instructions to build the Flask Docker image
- `README.md` — Exercise documentation
- `screenshots/` — Screenshots of the exercise

## How It Works

1. Create a custom Docker bridge network.
2. Verify and inspect the network.
3. Create a Flask application and Dockerfile.
4. Build the Flask Docker image.
5. Run MySQL, Redis, and Flask containers on the same network.
6. Test connectivity between containers.
7. Stop and remove the containers and network.

## Steps to Run

### 1. Create a Bridge Network

    docker network create --driver bridge my-bridge-net

### 2. Verify the Network

    docker network ls

### 3. Inspect the Network

    docker network inspect my-bridge-net

### 4. Create the Flask Application

Create a file named `app.py`.

    from flask import Flask, jsonify

    app = Flask(__name__)

    @app.route('/about', methods=['GET'])
    def about():
        return jsonify({
            "name": "Simple REST API",
            "version": "1.0",
            "description": "This is a simple REST API built with Flask."
        })

    if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=False, port=5001)

### 5. Create requirements.txt

    Flask==2.0.1

### 6. Create the Dockerfile

    FROM python:3.9-slim
    WORKDIR /app
    COPY requirements.txt .
    COPY app.py .
    RUN pip install --no-cache-dir -r requirements.txt
    EXPOSE 5001
    CMD ["python", "app.py"]

### 7. Build the Flask Image

    docker build -t flask-api .

### 8. Launch the Containers

Run the MySQL container.

    docker run -d --name mysql --network my-bridge-net -e MYSQL_ROOT_PASSWORD=change-me mysql:latest

Run the Redis container.

    docker run -d --name redis --network my-bridge-net redis:latest

Run the Flask container.

    docker run -d --name flask --network my-bridge-net -p 5001:5001 flask-api

### 9. Verify the Running Containers

    docker ps

### 10. Test the Flask Application

Open the following URL in your browser:

    http://localhost:5001/about

You should receive a JSON response containing the application name, version, and description.

### 11. Test Connectivity Between Containers

Open a shell inside the Flask container.

    docker exec -it flask sh

Test the MySQL hostname.

    ping mysql

Test the Redis hostname.

    ping redis

If `ping` is not installed in the Flask image, use another available network diagnostic tool.

Exit the container shell.

    exit

### 12. Clean Up

Stop the containers.

    docker stop mysql redis flask

Remove the containers.

    docker rm mysql redis flask

Remove the custom network.

    docker network rm my-bridge-net

## Screenshots

Include screenshots showing:

- Docker bridge network creation.
- Network details using `docker network inspect`.
- Successful Docker image build.
- MySQL, Redis, and Flask containers running.
- Container connectivity tests.
- Flask API response in the browser.

## Verification Results

- Custom bridge network created successfully.
- Flask Docker image built successfully.
- MySQL, Redis, and Flask containers started.
- Containers connected to the same bridge network.
- Flask API accessible through port 5001.
- Containers and network removed during cleanup.

## Technologies Used

- Docker
- Docker Networking
- Python
- Flask
- MySQL
- Redis

## Questions and Answers

**Q1. What is the purpose of the `--network` flag in Docker?**

Answer: It connects a container to a specified Docker network.

**Q2. How do containers communicate on the same bridge network?**

Answer: They can communicate using container names or IP addresses.

**Q3. What is the difference between bridge and host networking?**

Answer: Bridge networking provides an isolated network for containers. Host networking shares the host's network stack.

**Q4. How can you expose a container port to the host machine?**

Answer: Use the `-p` flag, for example, `-p 5001:5001`.

## Conclusion

Successfully created a custom Docker bridge network and ran Flask, MySQL, and Redis containers on it. Verified container networking and accessed the Flask API through the host machine.

