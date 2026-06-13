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
## Module Inventory     (monorepos only — remove for single-package repos)
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
- last_session:   YYYY-MM-DD | agent: string          (or "none yet")
- last_review:    YYYY-MM-DD | through <session-file>  (or "none yet")
- repo:           ~-relative path (e.g. ~/projects/foo) — NEVER absolute /Users/<name>/…; memory is committed & shared

## Architectural Invariants  hard constraints; never decay (omit the section if none)
## Stack & Tools             key: value pairs
## Key Decisions             bullet list, present tense
## Conventions               bullet list
## Open Threads              - [ ] incomplete  /  - [x] complete
## User Preferences          bullet list — record ONLY what the user explicitly states; never infer
## Team / Members            name: preferred agent
```

Each fact carries a metadata footer (HTML comment), maintained by the review ritual
— invisible when rendered, read/written by agents:

```
<!-- id: kebab-id | created: YYYY-MM-DD | last_used: YYYY-MM-DD | uses: N | tier: core|active|working|archive-candidate -->
  id         stable, unique within the file, assigned once at creation
  created    date the fact entered memory
  last_used  date of the most recent session referencing the id  (recomputed at review)
  uses       count of sessions referencing the id                (recomputed at review)
  tier       lifecycle bucket — see DECAY.md / REVIEW.md at the repo root
```

`## Architectural Invariants` facts and unchecked Open Threads (`- [ ]`) never decay.

---

## memory/sessions/YYYY-MM-DD-HHMMSS.md

One file per session, named with the UTC timestamp at **persist time** — the
moment the file is written (i.e. session end), not session start. Use
`date -u +%Y-%m-%d-%H%M%S` or equivalent. Colons are omitted for cross-platform
filename compatibility. Because filenames sort lexicographically, the last session
is always the last file alphabetically — no ambiguity even with multiple
contributors on the same day.

```
# Session (YYYY-MM-DDThh:mm:ss.mmmZ - YYYY-MM-DDThh:mm:ss.mmmZ)

**Agent:** string
**User:** brief task context

## What We Did
Prose summary, 2–5 sentences.

## Decisions Made
Bullet list (if any).

## Context for Next Session
What the next agent needs to know.

## Memory References
- Referenced:  <continuity fact ids this session relied on / reinforced>
- Created:     <new fact ids added this session (tier: working)>
- Reactivated: <fact ids pulled back from the archive>
```

The `## Memory References` section is the **event log** the review ritual reads to
recompute `uses`/`last_used` (see `DECAY.md` §2). List fact ids, not prose; omit any
line that doesn't apply. Don't edit metadata on facts mid-session — just record the
ids here; the review does the counting.

Title format: `# Session (startZ - endZ)` where both are full ISO 8601 UTC
timestamps with milliseconds. Record the UTC time when you begin your first
action as the start; the time when you write this file as the end. Both are
required — they remove ambiguity about session boundaries and aid conflict tracing.

Rules: never edit past files. Each session creates its own file. To resume
context before responding, sort `memory/sessions/` lexicographically and read
the most recent 2–3 files.

---

## memory/sessions/INDEX.md  (optional)

A lightweight, one-line-per-session index so agents can orient without listing or
opening files: `YYYY-MM-DD-HHMMSS — <agent> — <one-line summary>`. Optional and
progressive — maintain it only if the team wants it. If kept, append one line each
session. A stale index is worse than none, so skip it rather than let it drift.

---

## memory/decay-policy.md

Tunable integer windows + triggers for the evolving-memory layer (`working_window`,
`active_window`, `archive_window`, `review_every`, `continuity_max_lines`, and
auto-core). All windows are in **sessions**. The rules these feed live in `DECAY.md`
and `REVIEW.md` at the repo root.

---

## memory/archive/

Cold storage for archived facts and swept completed threads. Nothing here is
deleted; reactivation moves a fact back into `continuity.md` (see `REVIEW.md`).

```
archive/
  YYYY-QN.md   facts (with their metadata footers) moved out of continuity.md, grouped by quarter
  INDEX.md     one line per archived fact: `id — one-line summary — <quarter file>`  (greppable)
```

---

## .agent/version.md

Install manifest recording which agent-memory version this repo is on:
`version`, `enabled_with`, `last_upgraded`, `mode`. It gates the in-place upgrade
ladder — see the tool's `UPGRADE.md` (reached only via `ENABLE.md` Mode B).

---

## Bootstrap Files

Thin pointers to `AGENTS.md`. `CLAUDE.md` and `GEMINI.md` additionally carry an
inline one-line project header (`{{PROJECT_NAME}}` + `{{PROJECT_ONELINE}}`) so
eagerly-loaded runtimes get immediate context without an extra hop; the enable step
fills those placeholders. The dotfile rules (`.cursorrules`, `.windsurfrules`,
`.github/copilot-instructions.md`) stay as plain pointers.
