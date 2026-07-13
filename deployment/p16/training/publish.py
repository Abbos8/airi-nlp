from __future__ import annotations

import argparse

from huggingface_hub import HfApi


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--token", required=True)
    parser.add_argument("--message", default="Publish approved P16 model")
    args = parser.parse_args()
    api = HfApi(token=args.token)
    api.create_repo(args.repo, repo_type="model", exist_ok=True)
    commit = api.upload_folder(
        folder_path=args.folder,
        repo_id=args.repo,
        repo_type="model",
        commit_message=args.message,
    )
    print(commit.oid)


if __name__ == "__main__":
    main()
