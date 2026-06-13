# Continuity — agent-memory

> Shared ground truth for this tool's own development state.

---

## Project State

- **project:** agent-memory
- **status:** v2 complete — added detection and migration of vendor AI files
- **last_enabled:** 2026-06-12
- **last_session:** 2026-06-13 | agent: Claude Code (2026-06-13-013154)

## What's Been Built

- `ENABLE.md` — 9-step protocol with detection (Step 2), mode selection (Step 3),
  and post-migration completion logic
- `MIGRATE.md` — per-vendor migration protocols for 11 vendors
- `templates/` — bootstrap + memory templates with `{{placeholders}}`
- `AGENTS.md` — dual-mode dispatch (memory protocol + enable)
- `CLAUDE.md`, `GEMINI.md`, `.cursorrules`, `.windsurfrules`, Copilot bootstrap
- `memory/` — this tool's own memory layer
- `examples/rust-event-bus/` — Mode A example, now a REAL fixture (unedited output
  from enabling ~/sandbox/rust/rust_event_bus_example); replaced the old node-project mock
- `examples/migrated-cursor-aider-project/` — Mode C example (migration from
  Cursor + Aider, with originals preserved under legacy/ and 3 converted sessions)

## Supported Migration Sources (v2)

Claude Code, Cursor, Cline, Roo Code, Aider, Continue.dev, Codeium/Windsurf,
GitHub Copilot, GPT/Codex agents, Zed AI, Gemini CLI.

## Key Decisions

- Originals preserved under `legacy/<vendor>/`, never deleted
- Steering content folded into `memory/instructions.md` as
  `## Migrated rules from <vendor>` sections
- History (JSONL, markdown chat logs, JSON sessions) converted to dated
  `memory/sessions/YYYY-MM-DD-HHMMSS.md` files (one per session; filename =
  persist time UTC; title = `# Session (startZ - endZ)` with full ISO 8601 ms;
  lexicographic sort = chronological sort, resolves last-session unambiguously
  across multiple contributors)
- Contradictions between vendors surface as Open Threads — the tool never picks a winner
- Three modes: Fresh Enable (A), Already Ours (B, idempotent), Migrate Vendor (C)
- Dry-run support so users can preview before committing

## Open Threads

### Design improvements from first real test drive (mercury-composable, 2026-06-12)
- [x] **MIGRATE.md: add an "integration" path for good steering files.** Section B
  of the General Migration Workflow now has a quality gate: project instructions
  (stack, architecture, purpose) → integrated into schema sections; AI rules only
  → verbatim append. Per-vendor protocols have a cross-reference note so the gate
  always applies.
- [x] **Fix `legacy/` gitignore contradiction.** Removed `legacy/` from the
  Step 7 gitignore block; it now commits to git, consistent with the "preserved"
  promise in README/MIGRATE.
- [x] **Add source-of-truth / version-drift guidance** to ENABLE.md Step 4
  (prefer build manifest e.g. pom.xml/package.json; surface drift as an Open Thread).
- [x] **Make migration git-aware** in MIGRATE.md (use `git mv` for tracked files to
  preserve history; plain move otherwise).
- [x] **Add a post-report verification step** to ENABLE.md (sanity-check generated
  files exist and integration is faithful) instead of ending at the report.
- [x] **Add monorepo/multi-module guidance** — templates are single-project shaped.
- [x] Replace mockup examples with a REAL fixture: `examples/node-project` (mock,
  taskflow-api) removed; `examples/rust-event-bus` added as the unedited output of a
  real Mode A enable. (migrated-cursor-aider remains a mockup — still a candidate to
  replace with a real Mode C run.)

### Refinements from first-session agent feedback (mercury-composable, 2026-06-12)
- [x] Document the two memory layers (repo `memory/` vs runtime `~/.claude/`) —
  `templates/AGENTS.md` + tool `AGENTS.md`
- [x] Inline project header (`{{PROJECT_NAME}}`/`{{PROJECT_ONELINE}}`) in
  `templates/CLAUDE.md` + `GEMINI.md`; `ENABLE.md` Step 6 fills them (cold-start fix)
- [x] Drop unreliable `Duration` field from the session schema
- [x] Sharpen the different-agent check to compare agent *family*
- [x] User Preferences "explicit only, never infer" guard (schema + continuity template)
- [x] Document optional `sessions/INDEX.md` (kept optional to avoid stale-index drift)
- [x] Retro-fit the live mercury-composable repo: inline header in CLAUDE.md +
  GEMINI.md, re-synced AGENTS.md + .agent/schema.md from updated templates,
  no-infer guard in continuity.md
- [x] Align mockup examples with new schema. NOTE: verification showed the examples
  never contained `Duration` (migrated-block format) and have no CLAUDE.md to carry
  a stale header — the only real drift was the User Preferences line, now fixed in
  both. (Earlier thread overstated the drift.)

### Pre-existing
- [ ] Test migration on a real repo with Cursor + Aider footprint
- [ ] Test migration on a Claude Code repo with .claude/projects/*.jsonl
- [ ] Test Continue.dev session JSON migration end-to-end
- [ ] Add example for migrating a Continue.dev project
- [ ] Consider a `DISABLE.md` protocol for cleanly removing AI memory
- [ ] Publish to GitHub
- [ ] Keep root `CLAUDE.md` architecture section in sync when file shapes or
  vendor support change (also touches `templates/`, `MIGRATE.md`, `README.md`,
  `examples/`)
- [x] v1 — Fresh enable from templates
- [x] v2 — Detection + migration from vendor AI files

## User Preferences

- Never expose the user's absolute home path (`/Users/<name>/…`) in file content —
  use `~`-relative paths. (Stated 2026-06-12; now enforced in ENABLE.md Step 5b +
  schema `repo:` guidance.)
