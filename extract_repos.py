from datasets import load_dataset
from itertools import islice
import re

# Load the StarCoder1 dataset in streaming mode
dataset = load_dataset("bigcode/starcoderdata", split="train", streaming=True)

# We'll collect repo names from content field
repo_names = set()
for entry in islice(dataset, 500):  # You can increase this later
    content = entry.get("content", "")
    match = re.search(r"<reponame>([\w\-/]+)", content)
    if match:
        repo_names.add(match.group(1))

# Save the repos to a text file
with open("repo_list.txt", "w") as f:
    for repo in sorted(repo_names):
        f.write(repo + "\n")

print(f"Extracted {len(repo_names)} repo names.")
