#!/usr/bin/env bash
set -Eeuo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_sfs_common.sh"

sfs_assert_inside_repo "${sfs_repo_root}"

find "${sfs_repo_root}" \
  \( -type d -name '__pycache__' -o -type d -name '.pytest_cache' \) \
  -prune -print -exec rm -rf {} +

find "${sfs_repo_root}" -type f -name '*.pyc' -print -delete
