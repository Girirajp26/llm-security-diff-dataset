from github import Github
import csv
import time
import os

# Replace with your actual token
gh_token = os.getenv("GITHUB_TOKEN")
g = Github(gh_token)

# Load repo names
with open("repo_list.txt", "r") as f:
    repos = [line.strip() for line in f if line.strip()]

# Prepare CSV output
with open("pr_data.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["repo", "title", "created_at", "labels", "url"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for repo_name in repos:
        print(f"\n🔍 Checking {repo_name}")
        try:
            repo = g.get_repo(repo_name)
            prs = repo.get_pulls(state="closed", sort="updated", direction="desc")
            for pr in prs[:10]:  # limit to top 10 per repo
                labels = [label.name for label in pr.labels]
                writer.writerow({
                    "repo": repo_name,
                    "title": pr.title,
                    "created_at": pr.created_at,
                    "labels": ", ".join(labels),
                    "url": pr.html_url
                })
        except Exception as e:
            print(f"Skipping {repo_name}: {e}")
        time.sleep(1)  # To avoid GitHub rate limiting
