# Exercise 8: Hello World Jenkins Job

## Objective
Create and run a Jenkins Freestyle job that executes a shell script and prints Hello, Jenkins!

## Prerequisites
- Docker Desktop and Jenkins running
- Git installed
- A GitHub repository named devops-sample-code
- Jenkins accessible at http://localhost:8080/

## Step 1: Create the Shell Script
The file `hello-world.sh` contains:

```bash
#!/bin/bash
echo "Hello, Jenkins!"
```

## Step 2: Upload the Script to GitHub
Upload `hello-world.sh` to the public `devops-sample-code` repository.

## Step 3: Create a Jenkins Job
1. Open http://localhost:8080/
2. Click New Item.
3. Enter `HelloWorld` as the job name.
4. Select Freestyle project and click OK.
5. Under Source Code Management, select Git.
6. Enter the URL of your `devops-sample-code` repository.
7. Under Build Steps, select Execute shell.
8. Enter:

```bash
sh hello-world.sh
```

9. Click Save.

## Step 4: Run and Verify
1. Open the HelloWorld job.
2. Click Build Now.
3. Open the build number and select Console Output.
4. Verify that the output contains `Hello, Jenkins!` and `Finished: SUCCESS`.

## Screenshots
Save actual screenshots in the `screenshots` folder and add them here.

### GitHub Script
![GitHub Script](./screenshots/github-script.png)

### Jenkins Job Configuration
![Jenkins Job Configuration](./screenshots/jenkins-job-config.png)

### Successful Build Output
![Successful Build Output](./screenshots/jenkins-success.png)

## Result
Document the actual result after running the Jenkins job.

## Conclusion
This exercise demonstrates how to execute a shell script using a Jenkins Freestyle job.
