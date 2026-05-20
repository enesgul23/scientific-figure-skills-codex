#!/usr/bin/env bash
set -Eeuo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_sfs_common.sh"

sfs_require_python

printf '[SFS-DOCTOR] repo=%s\n' "${sfs_repo_root}"
printf '[SFS-DOCTOR] skill=%s\n' "${sfs_skill_dir}"
sfs_run_skill "${sfs_python}" --version
sfs_run_skill "${sfs_python}" scripts/probe_python_environment.py --library pandas --library numpy --library matplotlib
sfs_run_skill "${sfs_python}" scripts/validate_render_template_registry.py
sfs_run_skill "${sfs_python}" scripts/validate_library_pool.py
sfs_run_skill "${sfs_python}" scripts/validate_memory.py --memory-dir tests/sample_memory/scientific-figure-memory
