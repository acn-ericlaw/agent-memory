# Memory File Schema

Format reference for all memory files. Use this when creating missing files
or when an agent needs to understand expected structure.

---

## memory/instructions.md

Stable project context and agent rules. Edit rarely.

```
# Agent Instructions — {project name}

## What This Project Is
## Repository Structure
## Conventions Observed
## Tone & Style
## Core Rules
## Testing
## CI / CD
```

---

## memory/continuity.md

Live project state. Update every session.

```
# Continuity — {project name}

## Project State
- project:        string
- status:         string
- last_enabled:   YYYY-MM-DD
- last_session:   YYYY-MM-DD | agent: string   (or "none yet")
- repo:           ~-relative path (e.g. ~/projects/foo) — NEVER absolute /Users/<name>/…; memory is committed & shared

## Stack & Tools        key: value pairs
## Key Decisions        bullet list, present tense
## Conventions          bullet list
## Open Threads         - [ ] incomplete  /  - [x] complete
## User Preferences     bullet list — record ONLY what the user explicitly states; never infer from behaviour
## Team / Members       name: preferred agent
```

---

## memory/sessions/YYYY-MM-DD-HHMMSS.md

One file per session, named with the UTC timestamp at session-start
(e.g. `2026-06-13-053000.md`). Colons are omitted for cross-platform filename
compatibility. Because filenames sort lexicographically, the last session is
always the last file alphabetically — no ambiguity even with multiple contributors
on the same day.

```
# Session — YYYY-MM-DD-HHMMSS UTC

**Agent:** string
**User:** brief task context

## What We Did
Prose summary, 2–5 sentences.

## Decisions Made
Bullet list (if any).

## Context for Next Session
What the next agent needs to know.
```

Rules: never edit past files. Each session creates its own file. To resume
context before responding, sort `memory/sessions/` lexicographically and read
the most recent 2–3 files. Do not record a session duration — agents cannot
measure it reliably; include a timestamp only if the user provides one.

---

## memory/sessions/INDEX.md  (optional)

A lightweight, one-line-per-session index so agents can orient without listing or
opening files: `YYYY-MM-DD-HHMMSS — <agent> — <one-line summary>`. Optional and
progressive — maintain it only if the team wants it. If kept, append one line each
session. A stale index is worse than none, so skip it rather than let it drift.

---

## Bootstrap Files

Thin pointers to `AGENTS.md`. `CLAUDE.md` and `GEMINI.md` additionally carry an
inline one-line project header (`{{PROJECT_NAME}}` + `{{PROJECT_ONELINE}}`) so
eagerly-loaded runtimes get immediate context without an extra hop; the enable step
fills those placeholders. The dotfile rules (`.cursorrules`, `.windsurfrules`,
`.github/copilot-instructions.md`) stay as plain pointers.
