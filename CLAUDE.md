# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

`agent-memory` is a **no-code, markdown-only** system with three jobs in one repo:

1. **A shared memory system** — a `memory/` layer that persists project context
   across sessions and across different AI vendors (Claude, Gemini, Cursor, …).
2. **An AI-enablement tool** — point it at any other repo to generate a tailored
   memory system there.
3. **A migration tool** — when the target repo already has vendor AI files
   (Cursor, Aider, Continue, Cline, …), fold them into the unified format.

There is **no build, lint, or test step** — the markdown files *are* the product.
The "runtime" is an AI agent reading these files and acting on them. Validation is
manual: read the protocol files and confirm an agent could follow them unambiguously,
and check `examples/` still reflect the documented behavior.

## First Action Every Session

Identify yourself as **Claude Code** in all session logs.

`CLAUDE.md` (this file, at repo root) is intentionally a thin dispatcher. The real
control flow lives in `AGENTS.md`. **Read `AGENTS.md` first** — it branches into one
of two modes:

- **Working *within* this repo** (improving the tool) → follow the memory protocol:
  read `memory/instructions.md`, `memory/continuity.md`, and the latest 2–3
  `memory/sessions/` files *before responding*; append a session log and update
  `continuity.md` *after*.
- **AI-enabling another repo** (user says "AI enable `/path`") → read `ENABLE.md`
  and follow its 10-step protocol exactly. For vendor migration specifics, read
  `MIGRATE.md`. Do not improvise from memory.

## Architecture — How the Files Relate

The system is layered, and the layering is the design (see README "Two Layers"):

- **Root bootstrap files** (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`, `.cursorrules`,
  `.windsurfrules`, `.github/copilot-instructions.md`) — one per vendor, each a thin
  pointer so *any* agent lands in the same `AGENTS.md` protocol. `AGENTS.md` is the
  hub; the rest defer to it.
- **`ENABLE.md`** — the enablement protocol (detect footprint → choose Mode A/B/C →
  analyze → generate). **`MIGRATE.md`** — per-vendor detection table and conversion
  rules, invoked only when `ENABLE.md` selects Mode C.
- **`templates/`** — exactly what gets installed into a *target* repo: bootstrap
  files plus `memory/` files containing `{{UPPER_SNAKE_CASE}}` placeholders, and
  `.agent/schema.md` (the canonical memory-file format, copied verbatim).
- **`memory/`** — this repo's *own* memory layer (not a template). It eats its own
  dog food: `instructions.md` (stable rules), `continuity.md` (live state, open
  threads, decisions), `sessions/` (dated logs).
- **`examples/`** — real filled-in output, not placeholders: `rust-event-bus/` is a
  Mode A (a *real* fresh enable on a Rust repo — unedited generated `memory/`);
  `migrated-cursor-aider-project/` is a Mode C (migration, with originals under
  `legacy/` and converted session logs).

When you change behavior, the change usually spans several of these in lockstep:
a new vendor needs a row in both `MIGRATE.md`'s detection table and a per-vendor
section, plus the supported-vendor tables in `README.md` and `AGENTS.md`. Editing
a memory-file shape means updating `templates/`, `templates/.agent/schema.md`, and
the `examples/` together.

## Non-Negotiable Constraints (from ENABLE.md / MIGRATE.md)

These govern enablement/migration and are the tool's core safety philosophy, not
mere guardrails:

- **Target-repo scope only.** Never read, modify, move, or list anything outside the
  resolved target-repo root — never `~`, `~/.claude/`, `~/.cursor/`, Application
  Support, AppData, or system paths. Resolve symlinks first; skip and report any path
  that escapes the repo. The user's home dir is *their* personal AI environment; the
  repo's `memory/` is the *team's* shared layer. The two coexist; migration only
  touches repo-committed vendor artifacts.
- **Never delete vendor files.** Move originals to `legacy/<vendor>/`, preserving
  relative paths.
- **Never overwrite, never pick a winner.** Fold vendor steering in under
  `## Migrated rules from <vendor>`; surface contradictions as Open Threads for the
  user to resolve.
- **Never modify source code or package manifests** in a target repo.
- Migration is **idempotent** (Mode B detects "already ours" and exits) and supports
  **dry-run**.

## Conventions

- Placeholders use `{{UPPER_SNAKE_CASE}}`. Templates mirror final output exactly;
  examples show real content, never placeholders.
- "Ours vs. vendor" for shared filenames (`CLAUDE.md`, `AGENTS.md`, …) is decided by
  content: ours references the agent-memory system / `memory/instructions.md`.
- Remind the user to commit memory changes:
  `git add memory/ && git commit -m "session YYYY-MM-DD [agent]"`.
