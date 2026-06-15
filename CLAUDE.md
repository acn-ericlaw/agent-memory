# CLAUDE.md — agent-memory

This repo is the **agent-memory** system — both a shared AI memory layer and an
AI-enablement / migration tool. (No build/lint/test; the markdown files *are* the product.)

**Read [`AGENTS.md`](./AGENTS.md) first** — it is the hub and branches into the right mode:

- **Working *within* this repo** → the memory protocol: read `memory/instructions.md`
  (project context + the full architecture), `memory/continuity.md`, `memory/vision.md`,
  and the latest 2–3 `memory/sessions/` *before responding*; log a session + update
  `continuity.md` *after*.
- **AI-enabling another repo** (user says "AI enable `/path`") → read [`ENABLE.md`](./ENABLE.md)
  and follow its protocol exactly.

Identify yourself as **Claude Code** in all session logs.
