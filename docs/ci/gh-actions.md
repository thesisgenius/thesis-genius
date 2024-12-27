## GitHub Actions

### Local Testing with Act (Optional)

Before pushing changes to GitHub, you can use Act, a tool for running GitHub Actions locally:

Install Act:

```shell
brew install act      # macOS (using Homebrew)
sudo apt install act  # Ubuntu
```

Install Act:


Run the workflow locally:

```shell
act push -j lint
```

**_Sample Output_**:

```shell
.... (cut for brevity)
[Lint and Format Check/lint]   ✅  Success - Main Run Linting
[Lint and Format Check/lint] ⭐ Run Post Set up Python
[Lint and Format Check/lint]   🐳  docker exec cmd=[/opt/acttoolcache/node/18.20.5/arm64/bin/node /var/run/act/actions/actions-setup-python@v4/dist/cache-save/index.js] user= workdir=
[Lint and Format Check/lint]   ✅  Success - Post Set up Python
[Lint and Format Check/lint] Cleaning up container for job lint
[Lint and Format Check/lint] 🏁  Job succeeded
```

* push simulates a push event.
* -j lint runs only the lint job.

**Benefits**:
* Quick feedback without committing and pushing changes.
* Identifies any missing dependencies or setup issues locally.

---

### Manual Trigger in GitHub

1. Push your changes to a branch in the repo (e.g., `test-lint`)
    ```shell
    git checkout -b test-lint
    git add .github/workflows/lint.yml Makefile
    git commit -m "Test CI lint workflow"
    git push origin test-lint
    ```
2. Open a pull request (PR) from test-lint to main in your GitHub repository. 
3. Check the Actions tab in your repository:
   * Navigate to Actions > Lint and Format Check.
   * Verify the workflow executes and completes successfully.