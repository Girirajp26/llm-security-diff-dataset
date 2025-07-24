# LLM Code Patch Analysis

This research project explores how outdated training data affects the behavior of large language models (LLMs) when generating code. It focuses on identifying security vulnerabilities and bugs in training datasets used for models like StarCoder.

## Research Goal

To compare the state of code in the StarCoder1 dataset vs. its later version, StarCoder2, and determine if bug/security fixes made in open-source projects were learned over time.

## What This Repository Includes

- `extract_repos.py` — extracts GitHub repos from StarCoder1 via HuggingFace
- `collect_prs.py` — uses GitHub API to collect pull requests from those repos
- `filter_prs.py` — filters PRs for bug, security, and breaking change keywords
- `extract_code_diffs.py` — downloads raw diff patches for selected PRs
- `parse_diffs.py` — parses patches into structured before/after code samples

## Key Files

- `repo_list.txt` — list of GitHub repos extracted from StarCoder1
- `pr_data.csv` — raw pull request data from GitHub API
- `filtered_prs.csv` — filtered PRs related to bug/security fixes
- `parsed_examples.json` — structured before/after code from actual PRs
- `/diffs/` — example `.diff` files showing code patches

## Future Work

- Compare these examples with StarCoder2
- Prompt LLMs to fix buggy code and evaluate performance
- Expand dataset and fine-tune models on security patches

