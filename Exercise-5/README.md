# Exercise 5: Docker Security with AppArmor and Python

## Objective

To secure Docker containers using AppArmor profiles and Python. This exercise restricts access to sensitive directories and prevents unauthorized actions inside a container.

## Prerequisites

- Docker installed
- Python installed
- Flask installed
- Docker SDK for Python installed
- AppArmor utilities installed on a Linux system

Install the required packages:

    sudo apt-get update
    sudo apt-get install apparmor-utils
    pip install flask docker

## Task 1: Create Flask Application

Create a file named `app.py`.

    from flask import Flask

    app = Flask(__name__)

    @app.route('/')
    def home():
        return "Hello, this is a secure Flask application running inside a Docker container!"

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)

## Task 2: Create Dockerfile

Create a file named `Dockerfile`.

    FROM python:3.8-slim

    WORKDIR /app
    COPY . /app
    RUN pip install flask
    EXPOSE 5000
    CMD ["python", "app.py"]

Build the Docker image:

    docker build -t flask-apparmor .

## Task 3: Create and Apply AppArmor Profile

Create the profile file:

    sudo nano /etc/apparmor.d/my-apparmor-profile

Add the following configuration:

    #include <tunables/global>

    /usr/bin/python3 {
        deny /etc/** r,
        deny /var/** rw,

        network inet stream,

        /app/** rwk,

        deny /bin/** rmix,
        deny /usr/bin/** rmix,

        capability net_bind_service,
        deny capability sys_admin,
    }

Load the profile:

    sudo apparmor_parser -r /etc/apparmor.d/my-apparmor-profile

Run the container with the AppArmor profile:

    docker run --security-opt="apparmor=my-apparmor-profile" -p 5000:5000 flask-apparmor

## Task 4: Apply AppArmor Using Docker SDK for Python

Create a file named `apply_apparmor.py`.

    import docker

    client = docker.from_env()

    client.images.build(path=".", tag="flask-apparmor")

    container = client.containers.run(
        "flask-apparmor",
        ports={'5000/tcp': 5000},
        security_opt=["apparmor=my-apparmor-profile"],
        detach=True
    )

    print(f"Container started: {container.short_id}")

    container_info = client.api.inspect_container(container.id)
    apparmor_profile = container_info['HostConfig']['SecurityOpt']

    print(f"AppArmor profile applied: {apparmor_profile}")

    container.stop()

Run the script:

    python apply_apparmor.py

Expected output includes the container ID and the applied AppArmor profile.

## Task 5: Test Restricted Actions

Create a file named `test_restricted_actions.py`.

    import docker

    client = docker.from_env()

    container = client.containers.run(
        "flask-apparmor",
        ports={'5000/tcp': 5000},
        security_opt=["apparmor=my-apparmor-profile"],
        detach=True
    )

    exit_code, output = container.exec_run("cat /etc/passwd")
    print(f"Attempt to read /etc/passwd: Exit Code {exit_code}, Output: {output.decode()}")

    exit_code, output = container.exec_run("/bin/bash")
    print(f"Attempt to execute /bin/bash: Exit Code {exit_code}, Output: {output.decode()}")

    container.stop()

Run the script:

    python test_restricted_actions.py

The expected result is that restricted actions are denied by the AppArmor profile.

## Questions and Answers

**1. What is the purpose of using AppArmor with Docker containers?**

AppArmor enforces security policies and confines applications to a limited set of resources. It helps limit access to system resources, files, and networks.

**2. How do AppArmor profiles help secure a Docker container?**

AppArmor profiles define what a containerized application can and cannot do. They can restrict access to directories, network capabilities, file execution, and system resources.

**3. Why is it important to restrict access to sensitive directories such as `/etc/` and `/var/`?**

The `/etc/` directory contains configuration files and system settings. Restricting access helps prevent unauthorized reading or modification of important files.

**4. What other capabilities can you restrict using AppArmor profiles?**

AppArmor can restrict network access, file writes, binary execution, directory access, and system administration capabilities such as `cap_sys_admin`.

**5. How can you verify if an AppArmor profile is successfully applied to a Docker container?**

You can inspect the container using the Docker SDK or Docker CLI. The `HostConfig.SecurityOpt` field shows the configured security options, including the AppArmor profile name.

## Conclusion

In this exercise, a Flask application was containerized using Docker and secured using an AppArmor profile. The Docker SDK for Python was used to apply and inspect the profile, and restricted actions were tested inside the container.