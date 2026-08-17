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
# NotebookEdit reaches the same filesystem as Write/Edit and was simply absent
# from this list, so a .ipynb anywhere on the box was writable unguarded
# [co-03ojd.4, sweep D-F3]. It carries the path under `notebook_path`, not
# `file_path` — adding the tool name alone leaves the guard inert.
enforcement_require_tool "Write" "Edit" "MultiEdit" "NotebookEdit"
enforcement_detect_repo_root

HOOK_NAME="repo-guard"

# --- Extract file path --------------------------------------------------------
FILE_PATH=$(echo "$TOOL_INPUT" | jq -r '.file_path // .notebook_path // empty')
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

# /mnt/c/Users/steve/zgent-bridge/ — sanctioned cross-instance dropbox
# (WSL agents <-> Windows agents like Claude Desktop). Single discrete path
# outside the enterprise root, authorized per zgent-permissions.md exception.
#
# Ported from COO's copy [co-03ojd.4, sweep D-F8]. COO's zgent-permissions.md
# lists this under "Sanctioned exceptions (whitelisted in repo-guard.sh)" and
# describes the bridge as being for "COO and other zgents" — but only COO's
# repo-guard actually whitelisted it, and DReader's own .claude/rules/ and
# CLAUDE.md never mention zgent-bridge at all (measured 2026-08-16). If the
# bridge is meant to be COO-only, the correct fix is the opposite of this hunk:
# narrow the wording in COO's zgent-permissions.md instead. That is Steve's call.
#
# NOTE: COO's copy also carries a /root/projects/Strader/ block. That one is
# correctly absent here — the Strader standing authority is COO-only
# [co-qliwo] — so do NOT "restore parity" by porting it as well.
if [[ "$FILE_PATH" == /mnt/c/Users/steve/zgent-bridge/* ]]; then
    exit 0
fi

# Harness-designated session scratchpad. Claude Code's own system prompt names
# /tmp/claude-<uid>/<project-slug>/<session-id>/scratchpad as the place for ALL
# temporary files, then this guard denied every Write to it — so the agent
# learned to route around the guard with Bash (which it does not cover at all,
# sweep D-F3) rather than to respect it. A guard that is stale against practice
# trains evasion [co-03ojd.4, sweep D-F7]. Anchored: the /scratchpad segment
# must sit exactly three levels under /tmp/claude-<uid>.
if [[ "$FILE_PATH" =~ ^/tmp/claude-[0-9]+/[^/]+/[^/]+/scratchpad(/|$) ]]; then
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
