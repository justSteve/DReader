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
# NotebookEdit reaches the same filesystem as Write/Edit and was simply absent
# from this list, so a .ipynb anywhere on the box was writable unguarded
# [co-03ojd.4, sweep D-F3]. It carries the path under `notebook_path`, not
# `file_path` — adding the tool name alone leaves the guard inert.
enforcement_require_tool "Write" "Edit" "MultiEdit" "NotebookEdit"
enforcement_detect_repo_root

HOOK_NAME="write-guard"

# --- Extract file path and content -------------------------------------------
FILE_PATH=$(echo "$TOOL_INPUT" | jq -r '.file_path // .notebook_path // empty')
[[ -z "$FILE_PATH" ]] && exit 0

# Extract content based on tool type
CONTENT=""
if [[ "$TOOL_NAME" == "Write" ]]; then
    CONTENT=$(echo "$TOOL_INPUT" | jq -r '.content // empty')
elif [[ "$TOOL_NAME" == "Edit" ]]; then
    CONTENT=$(echo "$TOOL_INPUT" | jq -r '.new_string // empty')
elif [[ "$TOOL_NAME" == "MultiEdit" ]]; then
    CONTENT=$(echo "$TOOL_INPUT" | jq -r '.edits[]?.new_string // empty' 2>/dev/null)
elif [[ "$TOOL_NAME" == "NotebookEdit" ]]; then
    CONTENT=$(echo "$TOOL_INPUT" | jq -r '.new_source // empty')
fi

# --- Protected Path Check -----------------------------------------------------
# Anchored to directory segments, file extensions, and whole basenames — never a
# bare word anywhere in the path. The previous pattern carried bare `credentials`
# and `secret`, so prose ABOUT credentials could not be written with the Write
# tool: myDesk/reports/secrets-handling-policy.md and
# docs/runbooks/credentials-rotation.md were both denied, 75 protected_path
# denials since 2026-08-02, while the same write succeeded via Bash — friction
# without safety [co-03ojd.4, sweep D-F11]. The content scan below is the real
# control and is unchanged; this check is only for files whose NAME says they
# hold a credential.
PROTECTED_PATH_RE='(^|/)\.ssh/|(^|/)\.env(\.[^/]*)?$|\.pem$|\.key$|(^|/)credentials(\.[^/]*)?$|(^|/)secrets?(\.[^/]*)?$|(^|/)id_rsa|(^|/)id_ed25519'
if echo "$FILE_PATH" | grep -qiE "$PROTECTED_PATH_RE"; then
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
