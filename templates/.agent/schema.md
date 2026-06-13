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

Keep this file at the **enduring** altitude: what kind of project it is, its
structure, and conventions that rarely change. The precise, *volatile* stack facts
(current language version, dependency list, tool versions) are **not** duplicated
here — they live in `continuity.md` → `## Stack & Tools` (the live source of truth).
A one-line high-level descriptor here (e.g. "async Rust CLI") is enough; point to
continuity for specifics.

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
## Stack & Tools             canonical live home for language/deps/tool versions (key: value)
## Key Decisions             bullet list, present tense
## Conventions               bullet list
## Open Threads              - [ ] incomplete  /  - [x] complete (leave [x] for the review to sweep)
## User Preferences          bullet list — record ONLY what the user explicitly states; never infer
## Team / Members            name: preferred agent
```

`## Stack & Tools` is the single canonical home for the current stack — language
version, dependencies, tool versions. `instructions.md` gives only an enduring
high-level descriptor and points here; don't maintain the dep list in both.

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

**At creation** the agent sets only `id`, `created`, and `tier` — `working` for an
ordinary fact, `core` for an Architectural Invariant — and seeds `last_used: <today>
| uses: 1`. It does **not** hand-edit `uses`/`last_used`/`tier` afterward; those are
recomputed by the review from session-log `## Memory References` (see `DECAY.md` §1).

`## Architectural Invariants` facts and unchecked Open Threads (`- [ ]`) never decay.
Completed threads (`- [x]`) stay in place until the review sweeps them (see below /
`REVIEW.md`) — don't archive them by hand.

---

## memory/sessions/YYYY-MM-DD-HHMMSS.md

**A "session" is one write of a session-log file** — the unit of work since the last
log was written, not necessarily a whole conversation. A single long conversation
that spans several distinct tasks may produce **multiple** session logs (one per
work segment); that is expected and correct. The decay math counts session *files*
(`DECAY.md` §4), so each log is one event regardless of how conversations are sliced.

Name the file with the UTC timestamp at **persist time** — the moment you write it.
Use `date -u +%Y-%m-%d-%H%M%S` or equivalent; colons omitted for cross-platform
filename compatibility. Filenames sort lexicographically = chronologically, so the
most recent log is always the last file — unambiguous even with multiple
contributors on the same day.

```
# Session (YYYY-MM-DDThh:mm:ss.mmmZ)

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
- Created:     <new fact ids added this session (born tier: working)>
- Reactivated: <fact ids pulled back from the archive>
```

The `## Memory References` section is the **event log** the review ritual reads to
recompute `uses`/`last_used` (see `DECAY.md` §2). List fact ids, not prose; omit any
line that doesn't apply. Don't edit metadata on facts mid-session — just record the
ids here; the review does the counting.

Title format: `# Session (endZ)` — the persist-time UTC timestamp (full ISO 8601 with
milliseconds) is **required**. A start time is **best-effort and optional**: if you
genuinely tracked when you began, you may write `# Session (startZ - endZ)`, but do
not fabricate one — a consuming agent rarely knows its exact start instant, and the
persist time already orders the log.

Rules: never edit past files. Each session-log write creates its own file. To resume
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
