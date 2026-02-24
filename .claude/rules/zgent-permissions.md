# Rule: Zgent Permissions — Service Provider

DReader is an **enterprise service provider**. It exists to serve other agents with Discord intelligence — channel history, thread reconstructions, message search, and channel metadata.

## Filesystem
- READ any file under the enterprise root directory tree
- READ Discord data directories and cached content
- WRITE within this repository's directory
- WRITE to shared data exchange paths (e.g., /var/moo/, shared temp)
- NEVER read or write credentials, tokens, or secrets from other repos

## GitHub
- READ any repository under the same GitHub owner as this repo's origin
- WRITE (push, branch, PR, issues) only to this repository
- Cross-repo writes require explicit delegation via beads

## Service API
- EXPOSE channel, message, thread, and scrape job endpoints
- ACCEPT queries from any authenticated enterprise agent
- SERVE read-only data by default; mutations require bead authorization
- LOG all cross-agent queries for observability

## Data Collection
- SCRAPE Discord channels via computer-use (pywinauto, DOM)
- STORE messages, threads, and metadata in SQLite
- RECONSTRUCT conversation threads from flat message streams
- DEDUPLICATE entries using content hashing

## Secrets
- NEVER commit credentials, tokens, or API keys to tracked files
- Use environment variables or gitignored .env files
