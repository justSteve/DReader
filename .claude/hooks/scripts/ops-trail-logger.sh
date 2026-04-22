#!/usr/bin/env bash
# Ops Trail Logger — PostToolUse observer hook
# Logs every tool call with input summary, result status, and timing
# to JSONL for live observation (tail -f) and retroactive search (cass).
#
# Pure observer: always exits 0, never blocks.
# Bead: gt-otl

set -euo pipefail
set -f  # noglob: prevent * expansion in parsed content

LOG_FILE="/var/moo/logs/ops-trail.jsonl"

# Read hook input from stdin
INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
TOOL_INPUT=$(echo "$INPUT" | jq -c '.tool_input // {}')
TOOL_RESULT=$(echo "$INPUT" | jq -c '.tool_result // {}')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"')
CWD=$(echo "$INPUT" | jq -r '.cwd // ""')

# Nothing to log if tool name is empty
[[ -z "$TOOL_NAME" ]] && exit 0

# Build a human-readable summary based on tool type
build_summary() {
    local tool="$1"
    local input="$2"

    case "$tool" in
        Bash)
            local cmd
            cmd=$(echo "$input" | jq -r '.command // empty')
            # Truncate long commands
            if [[ ${#cmd} -gt 120 ]]; then
                echo "${cmd:0:117}..."
            else
                echo "$cmd"
            fi
            ;;
        Read)
            echo "$input" | jq -r '.file_path // empty'
            ;;
        Edit)
            local fp
            fp=$(echo "$input" | jq -r '.file_path // empty')
            local old_len new_len
            old_len=$(echo "$input" | jq -r '.old_string // "" | length')
            new_len=$(echo "$input" | jq -r '.new_string // "" | length')
            echo "${fp} (${old_len}→${new_len} chars)"
            ;;
        Write)
            local fp
            fp=$(echo "$input" | jq -r '.file_path // empty')
            local len
            len=$(echo "$input" | jq -r '.content // "" | length')
            echo "${fp} (${len} chars)"
            ;;
        MultiEdit)
            local fp
            fp=$(echo "$input" | jq -r '.file_path // empty')
            local edits
            edits=$(echo "$input" | jq -r '.edits // [] | length')
            echo "${fp} (${edits} edits)"
            ;;
        Glob)
            local pattern path
            pattern=$(echo "$input" | jq -r '.pattern // empty')
            path=$(echo "$input" | jq -r '.path // "."')
            echo "${path}/${pattern}"
            ;;
        Grep)
            local pattern path
            pattern=$(echo "$input" | jq -r '.pattern // empty')
            path=$(echo "$input" | jq -r '.path // "."')
            echo "/${pattern}/ in ${path}"
            ;;
        WebFetch)
            echo "$input" | jq -r '.url // empty'
            ;;
        WebSearch)
            echo "$input" | jq -r '.query // empty'
            ;;
        Agent)
            local desc stype
            desc=$(echo "$input" | jq -r '.description // empty')
            stype=$(echo "$input" | jq -r '.subagent_type // empty')
            if [[ -n "$stype" ]]; then
                echo "[${stype}] ${desc}"
            else
                echo "$desc"
            fi
            ;;
        Skill)
            echo "$input" | jq -r '.name // empty'
            ;;
        mcp__*)
            # MCP tools — show the tool name itself as summary, plus any key arg
            local first_val
            first_val=$(echo "$input" | jq -r 'to_entries | .[0].value // empty' 2>/dev/null)
            if [[ -n "$first_val" && ${#first_val} -lt 80 ]]; then
                echo "$first_val"
            else
                echo "(mcp call)"
            fi
            ;;
        *)
            echo ""
            ;;
    esac
}

# Extract result status
get_result_status() {
    local result="$1"
    # Check if result has error indicators
    local is_error
    is_error=$(echo "$result" | jq -r 'if .error then "error" elif .is_error then "error" else "ok" end' 2>/dev/null)
    echo "${is_error:-ok}"
}

SUMMARY=$(build_summary "$TOOL_NAME" "$TOOL_INPUT")
STATUS=$(get_result_status "$TOOL_RESULT")

# Write log entry
jq -n -c \
    --arg ts "$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)" \
    --arg sid "$SESSION_ID" \
    --arg tool "$TOOL_NAME" \
    --arg summary "$SUMMARY" \
    --arg status "$STATUS" \
    --arg cwd "$CWD" \
    '{timestamp:$ts, session_id:$sid, tool:$tool, summary:$summary, status:$status, cwd:$cwd}' \
    >> "$LOG_FILE" 2>/dev/null || true

# Always exit 0 — pure observer, never interfere
exit 0
