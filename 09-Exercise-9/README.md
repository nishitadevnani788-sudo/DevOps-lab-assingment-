# Exercise 9: Jenkins Multi-Stage Pipeline

## Objective
Automate the build, testing, and mock deployment of a Python Flask application using Jenkins.

## Files
- app.py: Flask application
- requirements.txt: Python dependencies
- test_app.py: Unit test
- Jenkinsfile: Declarative Jenkins pipeline

## Pipeline stages
1. Build: Create a Python virtual environment and install dependencies.
2. Test: Run Python unit tests.
3. Deploy: Copy the application to python-app-deploy.
4. Run Application: Start the deployed Flask application.
5. Test Application: Run unit tests and verify the HTTP response.

## Jenkins configuration
1. Create a Pipeline job named Python-MultiStage-Pipeline.
2. Select Pipeline script from SCM.
3. Select Git as SCM.
4. Repository URL:
   https://github.com/AyushiPachauri54/DevOps-Assignment.git
5. Branch: */main
6. Script Path: Exercise-9/Jenkinsfile
7. Save and click Build Now.

## Expected result
The pipeline should finish with SUCCESS and display:
Hello, Jenkins Multi-Stage Pipeline!

## Requirements
The Jenkins Linux environment needs Python 3, pip, and the Python venv module.
