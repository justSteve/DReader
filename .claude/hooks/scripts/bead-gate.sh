#!/usr/bin/env bash
# bead-gate.sh — PreToolUse soft enforcement hook for bead references
# Warns (systemMessage) when git commit messages lack a bead ID.
# Does NOT deny — minor housekeeping is exempt per beads-first rule.
#
# Bead: gt-enforce

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SCRIPT_DIR}/../lib/enforcement-common.sh"
enforcement_trap

# --- Read and filter ----------------------------------------------------------
enforcement_read_input
enforcement_require_tool "Bash"
enforcement_detect_repo_root

COMMAND=$(echo "$TOOL_INPUT" | jq -r '.command // empty')
[[ -z "$COMMAND" ]] && exit 0

HOOK_NAME="bead-gate"

# --- Only check git commit commands -------------------------------------------
if ! echo "$COMMAND" | grep -qE '\bgit\s+commit\b'; then
    exit 0
fi

# --- Extract commit message from -m flag --------------------------------------
COMMIT_MSG=""
if echo "$COMMAND" | grep -qE '(-m\s+|--message[= ])'; then
    # Extract the message — grab text between first quote pair after -m
    COMMIT_MSG=$(echo "$COMMAND" | sed -nE 's/.*(-m|--message)[= ]*["\x27]([^"\x27]*)["\x27].*/\2/p')
    # Fallback: try without quotes (bare -m word)
    if [[ -z "$COMMIT_MSG" ]]; then
        COMMIT_MSG=$(echo "$COMMAND" | sed -nE 's/.*(-m|--message)[= ]*([^ ]+).*/\2/p')
    fi
fi

# If we couldn't parse the message, OR the parsed message looks like a subshell
# (heredoc pattern: "$(cat <<"), fall back to scanning the full command
if [[ -z "$COMMIT_MSG" ]] || [[ "$COMMIT_MSG" == *'$('* ]]; then
    if echo "$COMMAND" | grep -qE '\[gt-[a-zA-Z0-9-]+\]'; then
        exit 0
    fi
    enforcement_warn "$HOOK_NAME" "missing_bead" \
        "No bead reference in commit message. If this is substantive work, add a bead ID like [gt-xxx]." \
        "(unparseable commit message)"
fi

# --- Check for bead ID --------------------------------------------------------
if echo "$COMMIT_MSG" | grep -qE '\[gt-[a-zA-Z0-9-]+\]'; then
    exit 0
fi

# --- No bead reference — warn -------------------------------------------------
enforcement_warn "$HOOK_NAME" "missing_bead" \
    "No bead reference in commit message. If this is substantive work, add a bead ID like [gt-xxx]." \
    "$COMMIT_MSG"
