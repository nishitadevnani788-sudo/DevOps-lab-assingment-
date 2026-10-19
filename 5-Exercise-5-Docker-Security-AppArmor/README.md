# Problem 5: Docker Security with AppArmor and Python

## Objective
Secure a Dockerized Flask application using AppArmor and the Docker SDK for Python.

## Files
- app.py: Flask application on port 5000.
- Dockerfile: Docker image definition.
- requirements.txt: Python dependencies.
- my-apparmor-profile: AppArmor policy.
- apply_apparmor.py: build and inspect a container.
- test_restricted_actions.py: test restricted commands.
- screenshots/: save genuine screenshots here.

## Prerequisites
Docker Engine with AppArmor support, an AppArmor-enabled Linux host, and Python 3.

AppArmor is a Linux kernel feature. Windows PowerShell does not provide apparmor_parser directly. Docker Desktop/WSL2 may not support loading custom profiles. If Docker rejects the profile, use an AppArmor-enabled Linux host or VM.

## Build
```bash
docker build -t flask-apparmor .
```

## Load profile on Linux
```bash
sudo apt-get update
sudo apt-get install -y apparmor-utils
sudo apparmor_status
```

Install this profile at /etc/apparmor.d/my-apparmor-profile, then run:
```bash
sudo apparmor_parser -r /etc/apparmor.d/my-apparmor-profile
```

This example profile may require adjustment for the host's Python executable and runtime files. Validate it on the target Linux system.

## Run the container
```bash
docker run --rm --security-opt="apparmor=my-apparmor-profile" -p 5000:5000 flask-apparmor
```

Open http://localhost:5000 to verify the Flask response.

## Docker SDK scripts
```bash
python -m pip install docker
python apply_apparmor.py
python test_restricted_actions.py
```

The Docker daemon must support AppArmor and the profile must be loaded before running these scripts.

## Questions and Answers

### 1. What is the purpose of AppArmor with Docker?
AppArmor confines processes through mandatory access-control policies. It limits access to files, executables, network operations, and selected capabilities.

### 2. How do AppArmor profiles secure containers?
Profiles define allowed and denied operations. Docker can apply a loaded profile to a container, adding host-kernel protection alongside container isolation.

### 3. Why restrict /etc and /var?
/etc contains system configuration, while /var may contain logs, caches, and application data. Restricting unnecessary access helps protect sensitive information and prevent unwanted changes.

### 4. What other capabilities can be restricted?
AppArmor can restrict file access, program execution, network operations, and selected Linux capabilities. Docker capabilities such as SYS_ADMIN can also be dropped separately.

### 5. How do you verify a profile is applied?
Inspect HostConfig.SecurityOpt and AppArmorProfile using Docker CLI or the Docker SDK. Confirm the profile is loaded on the host and review AppArmor audit logs during controlled tests. A configured option alone does not prove enforcement.

## Screenshots
Save genuine screenshots of:
1. Docker image build.
2. AppArmor profile loaded.
3. Container inspection.
4. Browser response.
5. Restricted-action tests.
6. Relevant AppArmor audit logs, if available.

Only report results actually observed on your system.
