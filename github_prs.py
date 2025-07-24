from github import Github
import os

# Github Token
gh_token = os.getenv("GITHUB_TOKEN")

# Connect to GitHub API
g = Github(gh_token)

# Replace with any repo from StarCoder1
repo_name = "pallets/flask"  # Very active open-source repo


try:
    repo = g.get_repo(repo_name)
    prs = repo.get_pulls(state="closed", sort="updated", direction="desc")

    print(f"\n🔍 Pull Requests for {repo_name}:\n")

    for pr in prs[:10]:  # Get 10 recent PRs
        print(f"Title: {pr.title}")
        print(f"Created: {pr.created_at}")
        print(f"Labels: {[label.name for label in pr.labels]}")
        print(f"URL: {pr.html_url}")
        print("-" * 40)

except Exception as e:
    print("⚠️ Error fetching PRs:", e)
