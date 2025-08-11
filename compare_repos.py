from datasets import load_dataset

# Stream the full dataset (safe, doesn't store all on disk)
dataset = load_dataset("bigcode/starcoderdata", split="train", streaming=True)

v2_repos = set()
count = 0

# Extract repos from first 10,000 StarCoder2 samples
for entry in dataset:
    if count >= 10000:
        break

    content = entry.get("content", "")
    if "<reponame>" in content and "v2" in content.lower():
        for line in content.splitlines():
            if line.startswith("<reponame>"):
                repo = line.replace("<reponame>", "").split("<")[0].strip()
                if repo:
                    v2_repos.add(repo)
    count += 1

# Load StarCoder1 repo list from earlier
try:
    with open("repo_list.txt", "r") as f:
        v1_repos = set([line.strip() for line in f if line.strip()])
except FileNotFoundError:
    print(" Error: repo_list.txt not found.")
    exit()

# Compare
both = v1_repos & v2_repos
only_v1 = v1_repos - v2_repos
only_v2 = v2_repos - v1_repos

# Save results
with open("repo_comparison.txt", "w", encoding="utf-8") as f:
    f.write(f" Repos in both (v1 & v2): {len(both)}\n")
    f.write("\n".join(sorted(both)))
    f.write("\n\n Repos only in StarCoder1: %d\n" % len(only_v1))
    f.write("\n".join(sorted(only_v1)))
    f.write("\n\n Repos only in StarCoder2: %d\n" % len(only_v2))
    f.write("\n".join(sorted(only_v2)))

print("Comparison complete! Check 'repo_comparison.txt'")
