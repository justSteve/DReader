# Rule: No Bare wsl --shutdown

You MUST NEVER suggest, output, or execute `wsl --shutdown` (or any command that terminates the WSL instance) without first completing a mini-handoff.

## Why

You run inside WSL. `wsl --shutdown` kills your session instantly — no graceful exit, no handoff, no state capture. Steve learned this the hard way when Claude suggested running it and the session evaporated.

## What To Do Instead

If the situation calls for a WSL restart (e.g., after system config changes, memory issues):

1. **Perform a mini-handoff first** — use the `/handoff` skill to write a DaysActivity entry
2. **Then tell Steve** what command to run *after* the handoff is confirmed written
3. **Never execute it yourself** — even via tmux, even via a script

This applies to:
- `wsl --shutdown`
- `wsl --terminate`
- `shutdown` / `poweroff` / `reboot` inside WSL
- Any command that would terminate the WSL distribution

## The --shutdown Shorthand

Steve may also type `--shutdown` as a conversational signal meaning "wrap it up." A `UserPromptSubmit` hook (`shutdown-filter.sh`) detects this and injects mini-handoff instructions. Honor them.
