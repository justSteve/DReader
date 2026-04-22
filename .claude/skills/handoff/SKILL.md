---
name: handoff
description: Prepend session handoff to DaysActivity.md for PaneWarden
allowed-tools: Bash, Read, Write, Glob
---

# Session Handoff (PaneWarden)

Prepend a session handoff entry to `DaysActivity.md` (cumulative daily log).

## Workflow

1. **Get current date and time**

   ```bash
   date +%Y-%m-%d
   date +%H:%M
   ```

2. **Check if DaysActivity.md exists for today**

   ```bash
   head -1 /root/projects/PaneWarden/DaysActivity.md 2>/dev/null
   ```

   - If missing or wrong date: create fresh file with today's header (see §Creating Fresh below).
   - If today's date: prepend new entry.

3. **Gather context**

   - Review recent conversation for what was accomplished.
   - Note discoveries, friction, things parked.
   - Check open beads: `bd list --status open` and `bd list --status in_progress`.

4. **Create handoff entry**

   ```markdown
   ## HH:MM — Session Handoff [Brief Topic Tag]

   **Summary**: [1–2 sentence description of what was accomplished]

   **Open Work**:
   - [in-progress item]

   **Decisions**:
   - [decision made this session, if any]

   **Files Changed**:
   path/to/file1
   path/to/file2

   **Tmux sessions touched**: [names, or "none"]

   **Next Session Actions**:
   - [specific next step]

   ---
   ```

5. **Prepend to DaysActivity.md**

   - Read existing content.
   - Write: `# DaysActivity - <date>` header + blank line + new entry + existing body (minus the header).
   - If creating fresh, use the template in §Creating Fresh.

## Entry Format Rules

- **Timestamp**: 24-hour format (HH:MM).
- **Summary**: standalone sentence, no bullet.
- **Files Changed**: one file per line, no bullets, relative paths.
- **Tmux sessions touched**: PaneWarden-specific — always note which shared-executable-space rooms were entered this session.
- **Separator**: `---` between entries.

## Creating Fresh DaysActivity.md

```markdown
# DaysActivity - YYYY-MM-DD

## HH:MM — Session Handoff [Topic]

[Entry content]

---
```

## Notes

- Entries are **prepended** (newest on top).
- Keep summaries concise and actionable.
- Evaluate importance — not everything needs detailed logging.
- **Files Changed** section only if files were actually modified.
- **Tmux sessions touched** is always present (even if "none") — it's PaneWarden's primary domain and worth logging every session.
