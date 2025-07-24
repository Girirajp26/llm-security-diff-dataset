from datasets import load_dataset
from itertools import islice

# Load the dataset in streaming mode (no full download)
dataset = load_dataset("bigcode/starcoderdata", split="train", streaming=True)

# Take the first 10 examples only
sample = list(islice(dataset, 10))

for i, entry in enumerate(sample, 1):
    print(f"\nExample {i}")
    print(f"Repo: {entry.get('repo_name', 'N/A')}")
    print(f"Path: {entry.get('path', 'N/A')}")
    print(f"Language: {entry.get('language', 'N/A')}")
    print(f"Content snippet:\n{entry['content'][:300]}...")
