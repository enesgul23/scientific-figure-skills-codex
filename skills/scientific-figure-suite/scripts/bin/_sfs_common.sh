#!/usr/bin/env bash
set -Eeuo pipefail

sfs_script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
sfs_skill_dir="$(cd "${sfs_script_dir}/../.." && pwd)"
sfs_repo_root="$(cd "${sfs_skill_dir}/../.." && pwd)"
if [[ -n "${PYTHON:-}" ]]; then
  sfs_python="${PYTHON}"
elif command -v python >/dev/null 2>&1; then
  sfs_python="python"
else
  sfs_python="python3"
fi
export PYTHONDONTWRITEBYTECODE="${PYTHONDONTWRITEBYTECODE:-1}"

sfs_fail() {
  printf '[FAIL] %s\n' "$*" >&2
  exit 1
}

sfs_require_python() {
  command -v "${sfs_python}" >/dev/null 2>&1 || sfs_fail "python not found: ${sfs_python}"
}

sfs_run_skill() {
  (cd "${sfs_skill_dir}" && "$@")
}

sfs_run_repo() {
  (cd "${sfs_repo_root}" && "$@")
}

sfs_assert_inside_repo() {
  local target
  target="$(cd "$1" && pwd)"
  case "${target}" in
    "${sfs_repo_root}"|"${sfs_repo_root}"/*) ;;
    *) sfs_fail "refusing path outside repository: ${target}" ;;
  esac
}
