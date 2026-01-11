"""
Parses GitHub Advanced Security vulnerability results on a PR, and prints any results to a comment on the PR

If no results are found in the vulnerability results, prints a comment that says "PR is clear of vulnerabilities"

If any commits are pushed to the PR, the comment made originally is edited with any updated findings.
"""

import os
import json
from github import Github

# Collect env vars
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY")
GITHUB_REF = os.environ.get("GITHUB_REF")
PR_NUMBER = os.environ.get("PR_NUMBER")
# Get the workflow run ID from the environment
RUN_ID = os.environ.get("GITHUB_RUN_ID")

# Initialize PyGithub
g = Github(GITHUB_TOKEN)
repo = g.get_user().get_repo(GITHUB_REPOSITORY.split('/')[1])
pull_request = repo.get_pull(int(PR_NUMBER))

def get_most_recent_security_scan_results():
    """
    Fetches the most recent security scan results from the workflow run.
    """
    workflow_runs = repo.get_workflow_runs(event="pull_request")
    for run in workflow_runs:
        if run.id == int(RUN_ID):
            artifacts = run.get_artifacts()
            for artifact in artifacts:
                if artifact.name == "advanced-security-results":
                    # Download the artifact
                    # PyGithub's download artifact method is a bit clunky,
                    # it returns a zip file. We'll need to extract it.
                    # For simplicity, let's assume the artifact content is directly accessible
                    # or that we have a way to parse the downloaded zip.
                    # In a real scenario, you'd download and unzip.
                    # For this example, we'll simulate reading the content.
                    # This part needs actual implementation to download and extract.
                    # For now, let's assume a direct way to get the JSON content.
                    # This is a placeholder for actual artifact content retrieval.
                    print(f"Found artifact: {artifact.name}")
                    # In a real scenario, you'd download the artifact and read its content.
                    # Example: artifact.download() would return a zip file.
                    # For this script, we'll assume the content is passed or directly readable.
                    # Let's mock a return for demonstration.
                    # You would typically download the artifact, unzip it, and read the JSON file.
                    #