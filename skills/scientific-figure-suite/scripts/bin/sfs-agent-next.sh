#!/usr/bin/env bash
set -Eeuo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_sfs_common.sh"

sfs_require_python
sfs_run_skill "${sfs_python}" scripts/advance_agentic_runbook.py "$@"
