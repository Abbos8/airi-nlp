from __future__ import annotations

import argparse
from pathlib import Path

from huggingface_hub import HfApi


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--token", required=True)
    args = parser.parse_args()
    api = HfApi(token=args.token)
    api.create_repo(args.repo, repo_type="dataset", exist_ok=True)
    commit = api.upload_file(
        path_or_fileobj=Path(args.file),
        path_in_repo="uz_sentiment_mini.jsonl",
        repo_id=args.repo,
        repo_type="dataset",
        commit_message="Publish P16 dataset snapshot",
    )
    print(commit.oid)


if __name__ == "__main__":
    main()
