#!/usr/bin/env bash
set -Eeuo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_sfs_common.sh"

run_quick=1
if [[ "${1:-}" == "--no-quick" ]]; then
  run_quick=0
  shift
fi

sfs_require_python
sfs_run_skill "${sfs_python}" scripts/validate_repo_hygiene.py --repo-root "${sfs_repo_root}" "$@"

if [[ "${run_quick}" == "1" ]]; then
  sfs_run_repo "${sfs_python}" quick_validate.py
fi
