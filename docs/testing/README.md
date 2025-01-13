# **Testing GitHub Actions Locally with `act`**

This guide explains how to use [`act`](https://github.com/nektos/act) to test your GitHub Actions workflows locally, including pytest workflows and other CI/CD processes.

---

## **What is `act`?**

`act` is a CLI tool that allows you to run GitHub Actions workflows locally in a Docker container. It simulates the GitHub Actions environment, enabling faster debugging and reducing the need for commits and pushes to test workflows.

---

## Benefits of Using act

#### 1. Test GitHub Actions workflows without committing or pushing changes.
#### 2. Debug and iterate faster by running workflows locally.
#### 3. Reduce costs for private repositories by minimizing unnecessary Actions usage.

---

## **Installation**

### **MacOS/Linux (Homebrew)**
```bash
brew install act
```

### **Debian/Ubuntu (apt)**
```bash
sudo apt install act
```

### **Manual Installation**
```bash
curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
```

### **Windows**
Download the executable from the [releases page](https://github.com/nektos/act/releases) and add it to your PATH.

---

## **Usage**

#### 1. **Verify Installation**
   Check that act is installed:
   ```bash
    act --version
   ```
   
#### 2. **Configure Secrets**
   If your workflows use secrets (e.g., for JIRA, Codecov, or GitHub tokens), create a .secrets file in the root of your repository:
   ```text
   JIRA_BASE_URL=https://your-jira-instance.atlassian.net
   JIRA_USER_EMAIL=your-jira-email@example.com
   JIRA_API_TOKEN=your-jira-api-token
   CODECOV_TOKEN=your-codecov-token
   ```
   
   > **Note**: This file should not be committed to your repository. Add .secrets to your .gitignore.

#### 3. **Run Workflows**
   Simulate GitHub Actions events using act:

   **Test All Workflows**
   ```bash
    act
   ```

   **Test a Specific Workflow**
   Run a specific workflow file:
   ```bash
   act -W .github/workflows/backend-pytest.yml
   ```
   
   **Simulate Events**
   Simulate GitHub Actions events such as pull_request or push:

   ```bash
   act pull_request
   act push
   ```

   **Test Specific Jobs**
   Specify a particular job to run:
   ```bash
   act pull_request -j pytest
   ```
   **Debugging Logs**
   Run with verbose output to debug:
   ```bash
   act -v
   ```

---

## **Tips for Using `act`**

#### 1. **Cache Docker Images**
   The first time you run act, it may pull large Docker images. Use the --pull flag to ensure the latest images:
   ```bash
   act --pull
   ```

#### 2. **Manage Runner Images**
   By default, act uses ubuntu-latest as the runner image. You can specify smaller or custom images:
   ```bash
   act -P ubuntu-latest=nektos/act-environments-ubuntu:18.04
   ```

##### 3. **Test Secrets**
   Verify that secrets are loaded properly in .secrets:
   ```text
   CODECOV_TOKEN=your-codecov-token
   ```

#### 4. **Ensure Docker Is Running**
   `act` relies on Docker. Make sure the Docker daemon is running:
   ```bash
   docker ps
   ```

---

## **Example Commands**
   **Run All Workflows**
   ```bash
   act
   ```

   **Run the pytest Job**
   ```bash
   act pull_request -j pytest
   ```

   **Run a Specific Workflow File**
   ```bash
   act -W .github/workflows/lint.yml
   ```

   **Run with Debugging**
   ```bash
   act -v
   ```