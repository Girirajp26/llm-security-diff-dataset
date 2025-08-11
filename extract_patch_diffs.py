import requests
import json

# Load filtered PRs
with open("common_prs.json", "r") as f:
    data = json.load(f)

# Loop through top N
for pr in data[:5]:  # Change number as needed
    print(f"\n {pr['repo']} | {pr['title']}")
    print(f"URL: {pr['url']}\n")

    # Get the raw patch diff
    headers = {"Accept": "application/vnd.github.v3.diff"}
    r = requests.get(pr["url"], headers=headers)

    if r.status_code == 200:
        print(r.text[:1000])  # print first 1000 characters only
        print("... [diff trimmed]\n")
    else:
        print(" Failed to fetch diff\n")
