# {{PROJECT_NAME}} — Claude Code

{{PROJECT_ONELINE}}

This project uses the agent-memory shared memory system. **Follow
[`memory/PROTOCOL.md`](./memory/PROTOCOL.md) first.** Root `AGENTS.md` is its one-line
universal discovery shim.

The protocol and core memory files are imported below, so they are structurally present at
session start (presence is guaranteed; *attending* to them is still the protocol). Imports
can't express dynamic paths — still list `memory/open-threads/` (read the unchecked
thread files) and scan the newest 2–3 logs in `memory/sessions/` per the protocol.

{{BOOTSTRAP_IMPORTS}}

Identify yourself as **Claude Code** in all session logs.
