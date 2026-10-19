# Introduction to Continuous Integration (CI) and Jenkins Installation

## Objective
To understand Continuous Integration (CI), explore popular CI/CD tools, and install Jenkins using Docker.

## What is Continuous Integration (CI)?
Continuous Integration (CI) is a software development practice in which developers frequently integrate code changes into a shared repository. It helps detect errors early, improve software quality, and accelerate software delivery.

## Key Features of CI
1. **Frequent Code Integration:** Developers commit code changes regularly.
2. **Automated Builds:** Builds are triggered automatically to verify code changes.
3. **Automated Testing:** Tests run to check application functionality.
4. **Immediate Feedback:** Developers receive quick feedback about build and test results.

## Benefits of CI
- Early bug detection
- Improved collaboration
- Faster development cycles
- Better code quality
- Reduced integration issues

## How CI Works
1. Developers write code and push changes to a Git repository.
2. The CI server detects code changes.
3. An automated build process runs.
4. Automated tests verify the application.
5. Build and test results are reported to developers.

## Popular CI/CD Tools
- **GitLab CI/CD:** Integrated CI/CD platform for GitLab repositories.
- **CircleCI:** Cloud-based CI/CD platform.
- **Travis CI:** CI service supporting automated builds and tests.
- **Bamboo:** Atlassian CI/CD tool.
- **TeamCity:** CI/CD server developed by JetBrains.
- **Azure DevOps Pipelines:** CI/CD solution from Microsoft.
- **GitHub Actions:** Automates workflows in GitHub repositories.
- **Spinnaker:** Continuous delivery platform for cloud applications.
- **Buildkite:** CI/CD platform supporting self-hosted build agents.
- **Drone:** Container-based CI/CD platform.

## Introduction to Jenkins
Jenkins is an open-source automation server used to build, test, and deploy software. It supports Continuous Integration (CI) and Continuous Delivery (CD) through automation and plugins.

### Why Use Jenkins?
- Automates repetitive tasks
- Supports continuous integration
- Provides a large plugin ecosystem
- Supports distributed builds using agents

## Key Jenkins Concepts
1. **Job/Project:** A task or process executed by Jenkins.
2. **Build:** An execution of a job.
3. **Pipeline:** A sequence of automated build, test, and deployment steps.
4. **Plugins:** Extensions that add functionality to Jenkins.
5. **Nodes:** Machines that execute Jenkins jobs.

## Jenkins Installation Using Docker

### Step 1: Run Jenkins Container
```bash
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts
```

### Step 2: Verify the Container
```bash
docker ps -a
```

### Step 3: Retrieve the Initial Administrator Password
```bash
docker exec -it jenkins bash
cat /var/jenkins_home/secrets/initialAdminPassword
```

Alternatively, run this command directly:
```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### Step 4: Access Jenkins
Open the following URL in a web browser:

http://localhost:8080/

Enter the initial administrator password on the Unlock Jenkins page and follow the setup instructions.

### Step 5: Complete Initial Setup
1. Unlock Jenkins using the initial administrator password.
2. Install the suggested plugins.
3. Create an administrator account.
4. Complete the setup and open the Jenkins dashboard.

## CI Workflow Example
1. A developer makes code changes.
2. The changes are pushed to a Git repository.
3. Jenkins detects the changes or runs a configured job.
4. Jenkins builds the application and runs tests.
5. Jenkins reports the build status.

## Result
Studied the fundamentals of Continuous Integration, explored popular CI/CD tools, and documented the steps to install and configure Jenkins using Docker.

## Conclusion
Continuous Integration helps teams identify errors early and improve software quality. Jenkins automates build, testing, and deployment workflows, making it a useful tool for implementing CI/CD pipelines.
