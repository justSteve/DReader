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

# Bead-ID pattern. The estate migrated to two-character prefixes in April
# (conventions/zgent-bead-prefixes.md); `gt-` is listed there as deprecated Gas
# Town and is retained below only so historical commits still match. Until
# 2026-08-16 this gate matched `gt-` ONLY, so it emitted the identical warning
# on every commit whether or not it cited a bead: 427 warnings in 14 days, 14 of
# them on commits that DID cite one, and zero commits in that window used `gt-`
# [co-69nhv, co-03ojd.4, sweep D-F1]. Three chars kept for the legacy `coo-`
# form; the trailing class allows sub-bead ids such as [co-03ojd.4].
BEAD_ID_RE='\[[a-z]{2,3}-[a-z0-9][a-zA-Z0-9._-]*\]'
BEAD_HINT="add the bead ID in brackets, e.g. [dr-a1b2c] — conventions/zgent-bead-prefixes.md lists the prefix for each repo"

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
    if echo "$COMMAND" | grep -qE "$BEAD_ID_RE"; then
        exit 0
    fi
    enforcement_warn "$HOOK_NAME" "missing_bead" \
        "No bead reference in commit message. If this is substantive work, $BEAD_HINT." \
        "(unparseable commit message)"
fi

# --- Check for bead ID --------------------------------------------------------
if echo "$COMMIT_MSG" | grep -qE "$BEAD_ID_RE"; then
    exit 0
fi

# --- No bead reference — warn -------------------------------------------------
enforcement_warn "$HOOK_NAME" "missing_bead" \
    "No bead reference in commit message. If this is substantive work, $BEAD_HINT." \
    "$COMMIT_MSG"
