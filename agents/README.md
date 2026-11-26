# Version-controlled Hermes profile files

This directory stores only explicitly selected, reviewable profile instructions. `SOUL.md` is the current versioned file; the live profile path `~/.hermes/profiles/edm/SOUL.md` points to it.

Do not move or symlink the entire live profile into this repository. It contains credentials and private/runtime data such as `.env`, `auth.json`, configuration, session and state databases, logs, caches, and locks. Keep those under the Hermes profile directory and out of version control. The profile's `memories/` directory was empty when this setup was made; add memory files here only after reviewing them for secrets and personal/private information.
