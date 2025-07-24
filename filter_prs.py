import csv

# Define keywords to look for in PR titles or labels
keywords = ["bug", "fix", "security", "patch", "vulnerability", "crash", "breaking"]

# Load the raw PR data
with open("pr_data.csv", "r", encoding="utf-8") as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)

# Filter PRs based on keywords
filtered = []
for row in rows:
    title = row["title"].lower()
    labels = row["labels"].lower()
    if any(kw in title for kw in keywords) or any(kw in labels for kw in keywords):
        filtered.append(row)

# Write filtered PRs to a new CSV
with open("filtered_prs.csv", "w", newline="", encoding="utf-8") as outfile:
    fieldnames = ["repo", "title", "created_at", "labels", "url"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(filtered)

print(f"Found {len(filtered)} filtered PRs with bug/security-related keywords.")
