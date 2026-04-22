#!/usr/bin/env bash
# write-guard.sh — PreToolUse enforcement hook for Write/Edit/MultiEdit
# Blocks: writes containing secrets (content scan) and writes to protected paths.
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

HOOK_NAME="write-guard"

# --- Extract file path and content -------------------------------------------
FILE_PATH=$(echo "$TOOL_INPUT" | jq -r '.file_path // empty')
[[ -z "$FILE_PATH" ]] && exit 0

# Extract content based on tool type
CONTENT=""
if [[ "$TOOL_NAME" == "Write" ]]; then
    CONTENT=$(echo "$TOOL_INPUT" | jq -r '.content // empty')
elif [[ "$TOOL_NAME" == "Edit" ]]; then
    CONTENT=$(echo "$TOOL_INPUT" | jq -r '.new_string // empty')
elif [[ "$TOOL_NAME" == "MultiEdit" ]]; then
    CONTENT=$(echo "$TOOL_INPUT" | jq -r '.edits[]?.new_string // empty' 2>/dev/null)
fi

# --- Protected Path Check -----------------------------------------------------
if echo "$FILE_PATH" | grep -qiE '(^|/)\.ssh/|\.pem$|\.key$|credentials|secret|id_rsa|id_ed25519'; then
    enforcement_deny "$HOOK_NAME" "protected_path" \
        "Write to protected path blocked: $FILE_PATH" \
        "$FILE_PATH"
fi

# --- Secret Content Scan ------------------------------------------------------
if [[ -n "$CONTENT" ]]; then

    # AWS Access Keys
    if echo "$CONTENT" | grep -qE 'AKIA[0-9A-Z]{16}'; then
        enforcement_deny "$HOOK_NAME" "secret_in_content" \
            "AWS access key detected in file content" \
            "$FILE_PATH"
    fi

    # GitHub tokens
    if echo "$CONTENT" | grep -qE '(ghp_[a-zA-Z0-9]{36}|gho_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9_]{22,})'; then
        enforcement_deny "$HOOK_NAME" "secret_in_content" \
            "GitHub token detected in file content" \
            "$FILE_PATH"
    fi

    # OpenAI keys (40+ chars — real keys are 48+)
    if echo "$CONTENT" | grep -qE 'sk-[a-zA-Z0-9]{40,}'; then
        enforcement_deny "$HOOK_NAME" "secret_in_content" \
            "OpenAI API key detected in file content" \
            "$FILE_PATH"
    fi

    # Private keys (PEM format)
    if echo "$CONTENT" | grep -qE 'BEGIN (RSA|DSA|EC|OPENSSH|PGP) PRIVATE KEY'; then
        enforcement_deny "$HOOK_NAME" "secret_in_content" \
            "Private key detected in file content" \
            "$FILE_PATH"
    fi

    # Database connection strings with inline passwords
    if echo "$CONTENT" | grep -qE '(mysql|postgres|postgresql|mongodb|redis)://[^:]+:[^@]+@'; then
        enforcement_deny "$HOOK_NAME" "secret_in_content" \
            "Database connection string with password detected" \
            "$FILE_PATH"
    fi

    # Generic secret assignments (key = "value" patterns)
    SECRET_ASSIGN='(api_key|api_secret|secret_key|private_key|access_token)\s*[:=]\s*["\x27][^"\x27]{8,}'
    if echo "$CONTENT" | grep -qiE "$SECRET_ASSIGN"; then
        enforcement_deny "$HOOK_NAME" "secret_in_content" \
            "Secret assignment pattern detected in file content" \
            "$FILE_PATH"
    fi
fi

# --- All checks passed --------------------------------------------------------
exit 0
