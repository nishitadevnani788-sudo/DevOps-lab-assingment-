# Jenkins Multi-Stage Pipeline: Deploying a Python Application

## Objective
To create and execute a Jenkins Pipeline for a Python Flask application using multiple stages: Build, Test, Deploy, Run Application, and Test Application.

## Scenario
This exercise demonstrates how Jenkins automates the CI/CD workflow for a sample Python Flask application. The pipeline installs dependencies, runs unit tests, copies the application to a deployment directory, starts the application, and tests its response.

## Prerequisites
- Docker installed and running
- Jenkins installed and accessible
- Git installed
- GitHub account and repository
- Python 3 installed in the Jenkins build environment
- Jenkins Pipeline plugin installed

## Step 1: Set Up Jenkins
Start Jenkins and open the following URL in your browser:

http://localhost:8080

Install the Pipeline plugin if it is not already installed.

## Step 2: Create the Python Flask Application

Create a project directory:

```bash
mkdir python-flask-app
cd python-flask-app
```

### File 1: app.py

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Jenkins Multi-Stage Pipeline!"

if __name__ == "__main__":
    app.run(debug=True)
```

### File 2: requirements.txt

```text
flask==2.1.2
```

### File 3: test_app.py

```python
import unittest
from app import app

class TestApp(unittest.TestCase):
    def test_home(self):
        tester = app.test_client()
        response = tester.get("/")
        print(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data.decode("utf-8"),
            "Hello, Jenkins Multi-Stage Pipeline!"
        )

if __name__ == "__main__":
    unittest.main()
```

## Step 3: Push the Application to GitHub

Initialize Git:

```bash
git init
git add .
git commit -m "Initial commit"
```

Connect your GitHub repository. Replace `your-username` with your GitHub username:

```bash
git remote add origin https://github.com/your-username/devops-sample-code.git
git branch -M main
git push -u origin main
```

## Step 4: Create a Jenkins Pipeline Job

1. Open the Jenkins dashboard.
2. Click **New Item**.
3. Enter the job name: `Python-MultiStage-Pipeline`.
4. Select **Pipeline**.
5. Click **OK**.

## Step 5: Create the Jenkinsfile

Create a file named `Jenkinsfile` in the root directory of the repository.

```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Creating virtual environment and installing dependencies...'
                sh 'python3 -m pip install --user -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo 'Running unit tests...'
                sh 'python3 -m unittest discover -s .'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                sh '''
                    mkdir -p "${WORKSPACE}/python-app-deploy"
                    cp "${WORKSPACE}/app.py" "${WORKSPACE}/python-app-deploy/"
                '''
            }
        }

        stage('Run Application') {
            steps {
                echo 'Starting application...'
                sh '''
                    nohup python3 "${WORKSPACE}/python-app-deploy/app.py" \
                      > "${WORKSPACE}/python-app-deploy/app.log" 2>&1 &
                    echo $! > "${WORKSPACE}/python-app-deploy/app.pid"
                '''
            }
        }

        stage('Test Application') {
            steps {
                echo 'Testing application...'
                sh 'python3 -m unittest discover -s .'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the logs for more details.'
        }
    }
}
```

**Note:** This pipeline uses Linux shell commands (`sh`) and requires Python and pip in the Jenkins build environment. The Build stage installs the listed Python dependencies.

## Step 6: Push the Jenkinsfile to GitHub

```bash
git add Jenkinsfile
git commit -m "Add Jenkins multi-stage pipeline"
git push
```

## Step 7: Configure the Jenkins Job

1. Open `Python-MultiStage-Pipeline` in Jenkins.
2. Click **Configure**.
3. Find the **Pipeline** section.
4. Select **Pipeline script from SCM**.
5. Select **Git**.
6. Enter your repository URL:

   `https://github.com/your-username/devops-sample-code.git`

7. Set the branch to `*/main`.
8. Set the script path to `Jenkinsfile`.
9. Click **Save**.

## Step 8: Run the Pipeline

1. Open the pipeline job.
2. Click **Build Now**.
3. Select the build number from Build History.
4. Open **Console Output** to view the execution logs.
5. Review each stage and check for errors.

## Step 9: Resolve Missing Python Dependencies

If the Jenkins container does not have Python or pip installed, inspect the container:

```bash
docker ps -a
```

Connect to the Jenkins container as root, replacing `jenkins` with the actual container name if needed:

```bash
docker exec -it -u root jenkins bash
```

Inside the container, install Python and pip:

```bash
apt-get update
apt-get install -y python3 python3-pip
```

Exit the container and run the pipeline again.

**Important:** Installing packages directly in a running container may not persist if the container is replaced. A custom Jenkins image with Python preinstalled is a more durable approach.

## Expected Outcome

### Build Stage
Python dependencies are installed successfully.

### Test Stage
The unit test executes and verifies that the Flask application's home route returns HTTP status code `200` and the expected message.

### Deploy Stage
The `app.py` file is copied into the `python-app-deploy` directory inside the Jenkins workspace.

### Run Application Stage
The Flask application is started as a background process.

### Test Application Stage
The application test executes and checks the expected response.

Expected test output:

```text
.
----------------------------------------------------------------------
Ran 1 test in 0.004s

OK
Hello, Jenkins Multi-Stage Pipeline!
```

Expected final status:

```text
Pipeline completed successfully!
Finished: SUCCESS
```

## Additional Enhancements
- Add code quality checks using Flake8 or Pylint.
- Build and deploy the application using Docker.
- Add email or Slack notifications for build success and failure.
- Configure automated pipeline triggers for GitHub changes.

## Result
Created a Python Flask application, pushed the source code to GitHub, and configured a Jenkins multi-stage pipeline to install dependencies, run tests, copy the application to a deployment directory, and start the application.

## Conclusion
This exercise demonstrates how Jenkins pipelines automate multiple stages of a CI/CD workflow and provide feedback on application builds and tests.
