---
description: Beads operations — check, create, update, close, show, deps
allowed-tools: Bash(bd *)
argument-hint: [check | create <title> | update <id> <status> | close <id> | show <id> | deps <id>]
---

You are handling a `/bead` command invocation. Parse `$ARGUMENTS` to determine the subcommand and execute it.

**Arguments received:** $ARGUMENTS

## Routing

Parse the first word of `$ARGUMENTS` as the subcommand. If `$ARGUMENTS` is empty, default to `check`.

| First word | Subcommand | Remaining words become |
|---|---|---|
| *(empty)* | **check** | — |
| `check` | **check** | — |
| `create` | **create** | `<title>` (all remaining words) |
| `update` | **update** | `<id> <status>` (second word = id, third = status) |
| `close` | **close** | `<id>` (second word) |
| `show` | **show** | `<id>` (second word) |
| `deps` | **deps** | `<id>` (second word) |
| anything else | **check** | — (treat unrecognized input as check) |

---

## Subcommand: check

Show the current beads landscape — what's ready to claim and what's in progress.

```bash
bd ready
```
```bash
bd list --status in_progress
```

Present both outputs clearly:
- **Ready work** — beads available to claim
- **In progress** — beads currently being worked

If nothing is ready and nothing is in progress, say so explicitly. This is the agent's situational awareness of available work.

---

## Subcommand: create

**Title:** everything after `create` in `$ARGUMENTS`

Before creating, enforce these factory rules:

1. **Title must be non-empty.** If the title is missing, stop and ask for one.
2. **Determine the prefix.** Run `bd config get prefix` to discover this rig's bead prefix. If that fails, extract the prefix from the most recent bead in the local database: `bd list --limit 1 --json`. The prefix is the alphabetic portion before the ID hash (e.g., `gt-` from `gt-abc123`).
3. **Create the bead:**
   ```bash
   bd create -t "<title>"
   ```
4. **Show the result.** After creation, run `bd show --current` to display the new bead.
5. **Commit integration reminder.** Tell the agent: "Reference this bead ID in all commit messages for this work: `[<bead-id>]`"

---

## Subcommand: update

**ID:** second word of `$ARGUMENTS`
**Status:** third word of `$ARGUMENTS`

1. **Both fields required.** If either is missing, stop and ask. Valid statuses: `open`, `in_progress`, `blocked`, `deferred`, `closed`.
2. **Run the update:**
   ```bash
   bd update <id> --status <status>
   ```
3. **Show updated state:**
   ```bash
   bd show <id>
   ```

If the agent needs to update fields other than status (title, priority, assignee, labels), it should use `bd update` directly — this command covers the most common case.

---

## Subcommand: close

**ID:** second word of `$ARGUMENTS`

1. **ID required.** If missing, show in-progress beads (`bd list --status in_progress`) and ask which one to close.
2. **Close the bead:**
   ```bash
   bd close <id>
   ```
3. **Suggest next work:**
   ```bash
   bd ready --limit 3
   ```
   Show what's available to pick up next.

---

## Subcommand: show

**ID:** second word of `$ARGUMENTS`

1. **If ID provided:**
   ```bash
   bd show <id>
   ```
2. **If no ID:** show the currently active bead:
   ```bash
   bd show --current
   ```

---

## Subcommand: deps

**ID:** second word of `$ARGUMENTS`

1. **ID required.** If missing, stop and ask.
2. **Show children:**
   ```bash
   bd children <id>
   ```
3. **Show blockers:**
   ```bash
   bd blocked --parent <id>
   ```

Present the dependency tree clearly — what's done, what's blocked, what's ready.

---

## Factory Rules (always enforced)

These rules apply regardless of subcommand:

- **No orphan work.** If an agent is about to start work without an active bead, this command exists to fix that. Every `/bead check` that shows no in-progress beads is a signal to either `/bead create` or `/bead update <id> in_progress`.
- **Status awareness.** After any mutation (create, update, close), always show the resulting state. Never fire-and-forget.
- **Commit integration.** After create or update-to-in_progress, remind the agent: "Reference `[<bead-id>]` in commit messages."
- **This command does not replace `bd`.** It's a convenience layer that enforces conventions. For advanced operations (labels, dependencies, molecules, gates), use `bd` directly.
