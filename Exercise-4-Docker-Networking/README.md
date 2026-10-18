# Exercise 4: Docker Networking with Multiple Containers

## Objective
Create a custom Docker bridge network and run Flask, MySQL, and Redis containers on it.

## Containers
- Flask REST API: host port 5001, container port 5001
- MySQL database: port 3306 inside the Docker network
- Redis cache: port 6379 inside the Docker network

## Build the Flask image
docker build -t flask-api .

## Create and inspect the network
docker network create --driver bridge my-bridge-net
docker network ls
docker network inspect my-bridge-net

## Launch containers
docker run -d --name mysql --network my-bridge-net -e MYSQL_ROOT_PASSWORD=LabPass123 mysql:latest
docker run -d --name redis --network my-bridge-net redis:latest
docker run -d --name flask --network my-bridge-net -p 5001:5001 flask-api

## Verify
docker ps
docker network inspect my-bridge-net
docker exec flask ping -c 3 mysql
docker exec flask ping -c 3 redis

Open http://localhost:5001/about in a browser, or run:
Invoke-RestMethod http://localhost:5001/about

## Questions and answers

1. What is the purpose of --net / --network?
It connects a container to a specified Docker network.

2. How do containers communicate on the same network?
Containers can use each other's container names as DNS hostnames and communicate through the relevant service ports.

3. What is the difference between bridge and host networking?
A bridge network connects containers through an isolated virtual network. Host networking shares the host's network stack and does not provide the same network isolation.

4. How do you expose a container port to the host?
Use -p HOST_PORT:CONTAINER_PORT, for example -p 5001:5001.

## Cleanup (run only after collecting evidence)
docker stop mysql redis flask
docker rm mysql redis flask
docker network rm my-bridge-net
