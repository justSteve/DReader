#!/usr/bin/env bash
# repo-guard.sh — PreToolUse enforcement hook for repo boundary
# Blocks writes to files outside the current repository tree.
#
# Fail-closed pattern and threat taxonomy adapted from
# Delanoe Pirard's claude-code-blueprint (Apache 2.0)
# https://github.com/Aedelon/claude-code-blueprint
#
# Bead: gt-enforce

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SCRIPT_DIR}/../lib/enforcement-common.sh"
enforcement_trap

# --- Read and filter ----------------------------------------------------------
enforcement_read_input
enforcement_require_tool "Write" "Edit" "MultiEdit"
enforcement_detect_repo_root

HOOK_NAME="repo-guard"

# --- Extract file path --------------------------------------------------------
FILE_PATH=$(echo "$TOOL_INPUT" | jq -r '.file_path // empty')
[[ -z "$FILE_PATH" ]] && exit 0

# Resolve to absolute path if relative
if [[ "$FILE_PATH" != /* ]]; then
    FILE_PATH="${REPO_ROOT}/${FILE_PATH}"
fi

# Normalize (remove /../ etc)
if [[ -e "$FILE_PATH" ]]; then
    FILE_PATH=$(realpath "$FILE_PATH")
else
    # For new files, normalize the directory portion
    dir_part="${FILE_PATH%/*}"
    base_part="${FILE_PATH##*/}"
    if [[ -d "$dir_part" ]]; then
        FILE_PATH="$(realpath "$dir_part")/${base_part}"
    fi
fi

# --- Allowed exceptions -------------------------------------------------------
# /var/moo/ — shared logging infrastructure
if [[ "$FILE_PATH" == /var/moo/* ]]; then
    exit 0
fi

# ~/.claude/ — Claude Code configuration
if [[ "$FILE_PATH" == "${HOME:-/root}/.claude/"* || "$FILE_PATH" == /root/.claude/* ]]; then
    exit 0
fi

# --- Repo boundary check -----------------------------------------------------
if [[ "$FILE_PATH" != "${REPO_ROOT}/"* && "$FILE_PATH" != "${REPO_ROOT}" ]]; then
    enforcement_deny "$HOOK_NAME" "repo_boundary" \
        "Write outside repo boundary blocked: $FILE_PATH (repo: $REPO_ROOT)" \
        "$FILE_PATH"
fi

# --- Inside repo boundary, allow ---------------------------------------------
exit 0
