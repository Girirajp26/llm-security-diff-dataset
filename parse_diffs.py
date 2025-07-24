import os
import json
import re

diff_folder = "diffs"
output = []

# Go through all .diff files
for filename in os.listdir(diff_folder):
    if not filename.endswith(".diff"):
        continue

    filepath = os.path.join(diff_folder, filename)
    
    # Extract repo and PR number from filename
    match = re.match(r"(.+)__(\d+)__(.+)\.diff", filename)
    if not match:
        continue

    repo_clean, pr_number, file_path = match.groups()

    code_before = []
    code_after = []

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            # Only look at changed lines (not metadata)
            if line.startswith("-") and not line.startswith("---"):
                code_before.append(line[1:].strip())
            elif line.startswith("+") and not line.startswith("+++"):
                code_after.append(line[1:].strip())

    if code_before or code_after:
        output.append({
            "repo": repo_clean.replace("_", "/"),
            "pr_number": int(pr_number),
            "file": file_path.replace("_", "/"),
            "code_before": "\n".join(code_before),
            "code_after": "\n".join(code_after)
        })

# Save to structured JSON
with open("parsed_examples.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print(f"Parsed {len(output)} before/after code examples.")
