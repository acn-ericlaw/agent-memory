# Changelog

## Release notes

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> Releases 1.0.0–3.0.0 below were reconstructed retrospectively (this changelog was
> introduced after 3.0.0 shipped), organized by capability rather than by individual
> commit. The capability ladder matches `VERSION` and `UPGRADE.md`.

---
## Version 3.2.0, 6/13/2026

> Protocol clarifications from a real-work field report (a Node.js→Rust refactor of an
> enabled repo, driven entirely by that repo's own memory layer). Documentation and
> wording only — no memory-file shape change; already-enabled repos pick these up via
> the `UPGRADE.md` 3.1.0→3.2.0 rung.

### Added

1. After-session **checklist** in `AGENTS.md` (root + template), plus an optional
   Stop/pre-commit hook recipe (`docs/optional-ritual-hook.md`) to prompt the ritual
   without breaking the no-code core.
2. Stack-fact **altitude rule**: `continuity.md` → `## Stack & Tools` is the canonical
   live home for language/deps/versions; `instructions.md` keeps a high-level
   descriptor and points there (notes added to both templates and `.agent/schema.md`).

### Removed

N/A.

### Changed

1. **Session model** defined precisely: a session is **one log-write** (a long
   conversation may produce several), and the title's `start` is now **best-effort**
   (the persist-time `end` is the required ordering stamp) — no more fabricated starts.
2. **Metadata ownership** pinned and a contradiction fixed: `ENABLE.md` Step 5b seeded
   new facts as `tier: active` while `DECAY.md`/`AGENTS.md` said `tier: working` — now
   uniformly **born `working`**. The agent seeds `id`/`created`/`tier`/`uses: 1`; the
   review owns `uses`/`last_used`/`tier` thereafter.
3. **Open-Thread archival** rule surfaced to the agent: mark `[x]` and leave it for the
   review to sweep — don't self-archive.

---
## Version 3.1.0, 6/13/2026

> Propagate the AI-infrastructure `.gitignore` into enabled repos. Personal AI-IDE
> runtime directories (`.claude/`, `.kiro/`, `.cursor/`, …) are per-machine state
> that should never be committed to a shared repo; the tool's own repo already
> ignored them, but enablement never passed that design on to targets. Additive and
> backward-compatible; already-enabled repos catch up in place via `UPGRADE.md`
> Mode B.

### Added

1. `templates/.gitignore` — the canonical managed block (sentinel-headed) listing
   the AI-IDE runtime directories and Aider local-history/cache files to ignore,
   while explicitly keeping steering files and the `memory/` layer tracked.
2. `UPGRADE.md` rung 3.0.0 → 3.1.0 — creates or appends the `.gitignore` block in
   already-enabled repos (idempotent, add-only).

### Removed

N/A — additive.

### Changed

1. `ENABLE.md` Step 7 — now **installs** a `.gitignore` (copied from the template)
   when the target has none, and appends only the missing managed entries when one
   exists; never removes or reorders the user's existing entries. Previously it only
   added a comment to an existing file and refused to create one.
2. `ENABLE.md` — Step 8 verifies the `.gitignore` sentinel + entries; the Step 9
   report and the Notes file-scope list now include `.gitignore`.
3. `VERSION` → 3.1.0; version tables in `UPGRADE.md` and `README.md` updated.

---
## Version 3.0.0, 6/13/2026

> Evolving memory layer. Facts stop being static: they carry usage metadata, fade
> through tiers, and archive when stale — recomputed deterministically from the
> session-log event stream. **Breaking** memory-file shape change (an un-upgraded
> agent couldn't correctly maintain the new files); already-enabled repos catch up
> in place via `UPGRADE.md` Mode B. Upgrades are additive and non-destructive.

### Added

1. Evolving-memory layer — facts carry usage metadata (`id`, `created`, `last_used`,
   `uses`, `tier`) and fade through tiers (active → recent → archive), recomputed
   deterministically from session logs. Full design in `DESIGN-evolving-memory.md`.
2. `DECAY.md` — metadata fields, tier lifecycle, and the deterministic integer decay
   rules (no floating-point scoring).
3. `REVIEW.md` — the review ritual that recomputes usage from session logs and
   archives faded facts.
4. `## Architectural Invariants` section in `memory/continuity.md` — core-tier facts
   (the tool's safety philosophy) that never decay.
5. `## Memory References` section in the session-log schema — the event source the
   review tallies usage from.
6. `templates/memory/decay-policy.md` — tunable decay windows (defaults 3/8/20,
   review every 10 sessions).
7. `memory/archive/` — cold storage for faded facts (never deleted).
8. Versioning: root `VERSION` file (semver) plus a per-repo `.agent/version.md`
   install manifest recording what each enabled repo is on.
9. `UPGRADE.md` — the in-place version-upgrade ladder (reached only via `ENABLE.md`
   Mode B); tool-operator-only, not installed into targets.
10. `examples/evolving-memory-example/` — the review ritual in action (continuity
    before/after, archive, a session log with Memory References).
11. Completed the root vendor bootstraps (`.cursorrules`, `.windsurfrules`,
    `.github/copilot-instructions.md`) and added `.gitignore`.

### Removed

N/A — the upgrade is additive and non-destructive.

### Changed

1. `ENABLE.md` — Mode B is now version-aware: an up-to-date repo is skipped, an older
   one is upgraded in place via `UPGRADE.md`; added the generate / install / verify
   steps for the evolving-memory files.
2. `AGENTS.md` (root + template) — the Before / During / After flow now references
   fact metadata and the review ritual.
3. `.agent/schema.md` — documents the metadata fields, the Memory References section,
   and the new files.
4. `README.md` and `CLAUDE.md` — added the architecture map, version table, and the
   evolving-memory section.

---
## Version 2.0.0, 6/12/2026

> Vendor detection and migration. The tool can now be pointed at a repo that already
> uses vendor AI files and fold them into the unified format, plus recognize and skip
> its own prior installs (idempotent re-runs).

### Added

1. `MIGRATE.md` — a per-vendor detection table and conversion rules for 11 sources:
   Claude Code, Cursor, Cline, Roo Code, Aider, Continue.dev, Codeium/Windsurf,
   GitHub Copilot, GPT/Codex agents, Zed AI, and Gemini CLI.
2. Mode C (Migrate Vendor) — originals preserved under `legacy/<vendor>/`, steering
   folded into `memory/instructions.md` as `## Migrated rules from <vendor>`, chat
   history converted to dated `memory/sessions/` logs, and contradictions surfaced as
   Open Threads (the tool never picks a winner).
3. Mode B (Already Ours) — idempotent re-runs: an existing install is detected and
   skipped.
4. Dry-run support, so users can preview changes before committing.
5. Monorepo / multi-module guidance — detection signals, single-root default, and a
   Module Inventory template.
6. `examples/rust-event-bus/` — a real Mode A fixture (the unedited output of enabling
   an actual Rust repo), replacing the earlier mock example.
7. `examples/migrated-cursor-aider-project/` — a Mode C example with originals under
   `legacy/` and converted session logs.
8. Documented the two memory layers (the repo's shared `memory/` vs. the runtime's
   personal `~/.claude/`).

### Removed

1. The mock `examples/node-project` (taskflow-api) — replaced by the real
   `rust-event-bus` fixture.
2. The unreliable `Duration` field from the session-log schema.

### Changed

1. Session-log filenames moved to `YYYY-MM-DD-HHMMSS.md` (UTC persist time); the title
   line is `# Session (startZ - endZ)` with full ISO 8601 millisecond timestamps —
   multi-contributor safe, with lexicographic sort matching chronological sort.
2. `ENABLE.md` — added version-drift guidance (prefer the build manifest as source of
   truth, surface drift as an Open Thread) and a post-report verification step.
3. `MIGRATE.md` — git-aware archiving (`git mv` for tracked files, plain move
   otherwise) and an integration quality gate that distinguishes project instructions
   (integrated into schema sections) from AI-only rules (appended verbatim).
4. Fixed a `legacy/` `.gitignore` contradiction — `legacy/` now commits to git,
   consistent with the "preserved" promise in `README.md` / `MIGRATE.md`.
5. Cold-start and accuracy refinements: inline project header in the `CLAUDE.md` /
   `GEMINI.md` templates, a User Preferences "explicit only, never infer" guard, and a
   sharpened different-agent check that compares agent *family*.

---
## Version 1.0.0, 6/12/2026

> Initial release. A no-code, markdown-only memory system that any AI agent can read,
> plus a Mode A enablement protocol to generate a tailored memory system in any repo.

### Added

1. `ENABLE.md` — the enablement protocol (detect footprint → choose mode → analyze the
   repo → generate tailored memory files).
2. Mode A (Fresh Enable) — generate a tailored `memory/` system from repo analysis.
3. `templates/` — exactly what gets installed into a target repo: bootstrap files plus
   `memory/` files with `{{UPPER_SNAKE_CASE}}` placeholders, and `.agent/schema.md`
   (the canonical memory-file format).
4. `AGENTS.md` — the dual-mode dispatcher: the memory protocol when working *within*
   the repo, the enablement protocol when AI-enabling *another* repo.
5. Per-vendor root bootstrap pointers — `CLAUDE.md`, `GEMINI.md`, `.cursorrules`,
   `.windsurfrules`, `.github/copilot-instructions.md` — each a thin pointer so any
   agent lands in the same `AGENTS.md` protocol.
6. This repo's own `memory/` layer (`instructions.md`, `continuity.md`, `sessions/`) —
   the tool eats its own dog food.
7. The core safety constraints: target-repo scope only; never delete or overwrite
   vendor files; never modify source code or package manifests.

### Removed

N/A — initial release.

### Changed

N/A — initial release.
