# Creating "Hello World" Jenkins Job

## Objective
To create a simple shell script, push it to a GitHub repository, and configure a Freestyle project in Jenkins to execute the script.

## Prerequisites
- Git installed on the local system
- GitHub account
- Docker installed and running
- Jenkins installed and accessible
- GitHub repository for the sample script

## Step 1: Create a GitHub Repository
1. Log in to GitHub.
2. Click the **+** icon and select **New repository**.
3. Enter the repository name: `devops-sample-code`.
4. Add the description: `A demo repository for Jenkins scripting`.
5. Select **Public** visibility.
6. Click **Create repository**.

## Step 2: Create a Fine-Grained Personal Access Token
Create a fine-grained Personal Access Token (PAT) in GitHub if authentication is required for your Git operations.

Refer to the official GitHub documentation:

https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token

**Security Note:** Never upload your PAT to GitHub or include it in this README.

## Step 3: Create the Shell Script
Create a file named `hello-world.sh` and add the following content:

```bash
#!/bin/bash
echo "Hello, Jenkins!"
```

On Linux or macOS, make the script executable:

```bash
chmod +x hello-world.sh
```

On Windows, the script can be created using VS Code or Notepad. Jenkins must have a shell environment capable of running the script.

## Step 4: Initialize the Git Repository
Configure your Git identity if it has not already been configured:

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

Initialize the local repository:

```bash
git init
```

## Step 5: Add and Commit the Script
Stage the script:

```bash
git add hello-world.sh
```

Check the repository status:

```bash
git status
```

Commit the changes:

```bash
git commit -m "Add hello-world.sh"
```

## Step 6: Connect the Repository to GitHub
Add the remote repository URL. Replace `your-username` with your GitHub username.

```bash
git remote add origin https://github.com/your-username/devops-sample-code.git
```

If the repository is already connected to a different remote, check it first:

```bash
git remote -v
```

Push the script to the `main` branch:

```bash
git branch -M main
git push -u origin main
```

Authenticate using your GitHub credentials or an approved authentication method when prompted. If using HTTPS with a PAT, use the token instead of your GitHub account password.

## Step 7: Verify the Script on GitHub
Open your repository:

`https://github.com/your-username/devops-sample-code`

Verify that `hello-world.sh` is present and contains the expected script.

## Step 8: Ensure Jenkins Is Running
Open Jenkins in your browser:

http://localhost:8080

Log in using your own Jenkins credentials.

If Jenkins is running in Docker, check its status:

```bash
docker ps
```

## Step 9: Create a New Jenkins Job
1. Open the Jenkins dashboard.
2. Click **New Item**.
3. Enter the job name: `HelloWorld`.
4. Select **Freestyle project**.
5. Click **OK**.

## Step 10: Configure the Jenkins Job

### General
Add the description:

`Hello World! Jenkins job.`

### Source Code Management
1. Select **Git**.
2. Enter the repository URL:

```text
https://github.com/your-username/devops-sample-code.git
```

3. For a public repository, credentials are generally not required for cloning.
4. For a private repository, configure the appropriate Git credentials.

### Build Steps
1. Scroll to the **Build** section.
2. Click **Add build step**.
3. Select **Execute shell** if available in your Jenkins environment.
4. Enter the command:

```bash
sh hello-world.sh
```

**Note:** The Jenkins build agent must have a compatible shell environment. If Jenkins runs in a Linux container, the shell command can run inside that environment.

## Step 11: Save and Run the Job
1. Click **Save**.
2. Open the `HelloWorld` job.
3. Click **Build Now**.
4. Wait for the build to finish.

## Step 12: View Console Output
1. Open the job's **Build History**.
2. Click the relevant build number, such as `#1`.
3. Select **Console Output**.
4. Verify that the script output appears.

Expected output:

```text
Hello, Jenkins!
Finished: SUCCESS
```

## Result
Created a `hello-world.sh` script, committed and pushed it to GitHub, configured a Jenkins Freestyle project to retrieve the repository, and executed the script through a Jenkins build.

## Conclusion
This exercise demonstrates how Jenkins can integrate with GitHub and execute a simple shell script as part of a basic Continuous Integration workflow.
