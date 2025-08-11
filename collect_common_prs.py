import os
from github import Github
import json
import time

# Insert your GitHub token here
gh_token = os.getenv("GITHUB_TOKEN")
g = Github(gh_token)

# Load repos
with open("common_repos.txt", "r") as f:
    repos = [line.strip() for line in f if line.strip()]

# Bug/security keywords
keywords = ["bug", "fix", "patch", "vulnerability", "exploit", "security", "issue", "error", "crash"]

# Where results will be saved
all_prs = []

for repo_name in repos:
    print(f" Pull Requests for {repo_name}...")

    try:
        repo = g.get_repo(repo_name)
        pulls = repo.get_pulls(state="closed", sort="created", direction="desc")
        
        for pr in pulls:
            title = pr.title.lower()
            body = (pr.body or "").lower()
            
            if any(kw in title or kw in body for kw in keywords):
                all_prs.append({
                    "repo": repo_name,
                    "title": pr.title,
                    "created_at": pr.created_at.isoformat(),
                    "labels": [label.name for label in pr.labels],
                    "url": pr.html_url
                })
        
        time.sleep(1)  # prevent rate-limiting

    except Exception as e:
        print(f" Error with {repo_name}: {e}")

# Save to file
with open("common_prs.json", "w") as f:
    json.dump(all_prs, f, indent=2)

print(" PR collection complete! Saved to common_prs.json")
