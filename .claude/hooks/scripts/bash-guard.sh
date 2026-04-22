#!/usr/bin/env bash
# bash-guard.sh — PreToolUse enforcement hook for Bash commands
# Blocks: privilege escalation, destructive patterns, pipe-to-shell, obfuscation.
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
enforcement_require_tool "Bash"

COMMAND=$(echo "$TOOL_INPUT" | jq -r '.command // empty')
[[ -z "$COMMAND" ]] && exit 0

HOOK_NAME="bash-guard"

# --- Privilege Escalation -----------------------------------------------------
if echo "$COMMAND" | grep -qE '(^|;|&&|\|)\s*(sudo|su|doas|pkexec)\b'; then
    enforcement_deny "$HOOK_NAME" "privilege_escalation" \
        "Privilege escalation blocked: $(echo "$COMMAND" | grep -oE '(sudo|su |doas |pkexec)[^ ]*')" \
        "$COMMAND"
fi

# --- Destructive Patterns -----------------------------------------------------
# rm -rf with dangerous targets (/, ~, .)
if echo "$COMMAND" | grep -qE 'rm\s+(-[a-zA-Z]*f[a-zA-Z]*\s+|--force\s+)*-[a-zA-Z]*r[a-zA-Z]*\s+(/\s*$|/\s*;|~\s*$|~\s*;|\.\s*$|\.\s*;)'; then
    enforcement_deny "$HOOK_NAME" "destructive_pattern" \
        "Destructive rm blocked: targets /, ~, or ." \
        "$COMMAND"
fi
# Also catch reversed flags (rm -fr /)
if echo "$COMMAND" | grep -qE 'rm\s+(-[a-zA-Z]*r[a-zA-Z]*\s+|--recursive\s+)*-[a-zA-Z]*f[a-zA-Z]*\s+(/\s*$|/\s*;|~\s*$|~\s*;|\.\s*$|\.\s*;)'; then
    enforcement_deny "$HOOK_NAME" "destructive_pattern" \
        "Destructive rm blocked: targets /, ~, or ." \
        "$COMMAND"
fi

# Fork bombs
if echo "$COMMAND" | grep -qE ':\(\)\s*\{.*\|.*&.*\}'; then
    enforcement_deny "$HOOK_NAME" "destructive_pattern" \
        "Fork bomb detected" \
        "$COMMAND"
fi

# Filesystem destruction
if echo "$COMMAND" | grep -qE '(^|;|&&|\|)\s*(mkfs\.[a-z0-9]+|mkfs)\s'; then
    enforcement_deny "$HOOK_NAME" "destructive_pattern" \
        "Filesystem format command blocked" \
        "$COMMAND"
fi

# dd to/from device
if echo "$COMMAND" | grep -qE 'dd\s+.*(if=/dev/|of=/dev/)'; then
    enforcement_deny "$HOOK_NAME" "destructive_pattern" \
        "dd device operation blocked" \
        "$COMMAND"
fi

# --- Pipe-to-Shell ------------------------------------------------------------
if echo "$COMMAND" | grep -qE '(curl|wget)\s.*\|\s*(bash|sh|zsh|dash)'; then
    enforcement_deny "$HOOK_NAME" "pipe_to_shell" \
        "Pipe-to-shell blocked: remote code execution risk" \
        "$COMMAND"
fi

# --- Obfuscation --------------------------------------------------------------
if echo "$COMMAND" | grep -qE 'eval\s+\$'; then
    enforcement_deny "$HOOK_NAME" "obfuscation" \
        "eval with variable blocked: indirect execution risk" \
        "$COMMAND"
fi

if echo "$COMMAND" | grep -qE 'base64\s+(-d|--decode).*\|\s*(bash|sh)'; then
    enforcement_deny "$HOOK_NAME" "obfuscation" \
        "base64 decode to shell blocked" \
        "$COMMAND"
fi

# --- All checks passed --------------------------------------------------------
exit 0
