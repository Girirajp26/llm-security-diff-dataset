import os
from github import Github
import requests
import json
import time

# Load GitHub token from environment (or add a fallback if needed)
gh_token = os.getenv("GITHUB_TOKEN")
g = Github(gh_token)

# Load saved PRs from common_prs.json
with open("common_prs.json", "r") as f:
    prs = json.load(f)

# Try to load existing output if it exists (so we don't re-download everything)
output = []
output_path = "common_diffs.json"
if os.path.exists(output_path):
    with open(output_path, "r", encoding="utf-8") as f:
        output = json.load(f)

# Track already-processed URLs to avoid duplicates
processed_urls = {entry["url"] for entry in output}

# Analyze and save diffs
for pr in prs:
    if pr["url"] in processed_urls:
        continue  # Skip PRs already processed

    print(f" {pr['repo']} | {pr['title']}")
    print(f"URL: {pr['url']}")

    try:
        repo = g.get_repo(pr["repo"])
        pr_number = int(pr["url"].split("/")[-1])
        gh_pr = repo.get_pull(pr_number)

        # Get diff from the .patch_url
        patch_url = gh_pr.patch_url
        response = requests.get(patch_url)

        if response.status_code == 200:
            patch_text = response.text
            print(" Diff downloaded\n")
            output.append({
                "repo": pr["repo"],
                "title": pr["title"],
                "url": pr["url"],
                "patch": patch_text
            })

            # Save progress after each diff
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2)

        else:
            print(" Could not fetch diff\n")

        time.sleep(1)  # avoid rate-limiting

    except Exception as e:
        print(f" Error: {e}\n")

print(" All available diffs collected and saved to common_diffs.json!")
