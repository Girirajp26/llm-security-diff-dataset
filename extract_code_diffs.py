from github import Github
import csv
import os
import time
import os

# Github Token
gh_token = os.getenv("GITHUB_TOKEN")
g = Github(gh_token)

# Load the filtered PRs
with open("filtered_prs.csv", "r", encoding="utf-8") as infile:
    reader = csv.DictReader(infile)
    filtered_prs = list(reader)

# Make a folder to save diffs
os.makedirs("diffs", exist_ok=True)

for pr_data in filtered_prs:
    repo_name = pr_data["repo"]
    pr_url = pr_data["url"]

    # Extract PR number from URL
    try:
        pr_number = int(pr_url.rstrip("/").split("/")[-1])
    except:
        print(f"Skipping invalid PR URL: {pr_url}")
        continue

    try:
        repo = g.get_repo(repo_name)
        pr = repo.get_pull(pr_number)

        print(f"\nProcessing PR #{pr_number} from {repo_name}...")

        # Get list of changed files in the PR
        files = pr.get_files()

        for file in files:
            filename = file.filename
            patch = file.patch if hasattr(file, "patch") else None

            if not patch:
                continue  # Skip binary or unsupported diffs

            # Save patch to a text file
            safe_filename = f"{repo_name.replace('/', '_')}__{pr_number}__{filename.replace('/', '_')}.diff"
            with open(os.path.join("diffs", safe_filename), "w", encoding="utf-8") as f:
                f.write(patch)

    except Exception as e:
        print(f"Failed to process {repo_name} PR #{pr_number}: {e}")
    
    time.sleep(1)  # prevent rate-limiting
