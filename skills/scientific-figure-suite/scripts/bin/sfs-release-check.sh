#!/usr/bin/env bash
set -Eeuo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_sfs_common.sh"

sfs_require_python
sfs_run_repo git diff --check
sfs_run_skill bash -lc 'bash -n scripts/bin/*.sh'
sfs_run_skill "${sfs_python}" scripts/validate_repo_hygiene.py --repo-root "${sfs_repo_root}"
sfs_run_repo "${sfs_python}" quick_validate.py
