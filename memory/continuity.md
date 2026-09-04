# Continuity — agent-memory

> Shared ground truth for this tool's own development state.

---

## Project State

- **project:** agent-memory
- **status:** v4.39.2 — a vendor-neutral, no-code (markdown) shared-AI-memory + AI-enablement tool: backward memory (decay/review/archive), forward VBDI loop, cross-vendor skills layer, declarative enable/upgrade (MANIFEST reconcile), forge-aware ritual triggers (GitHub/GitLab/AzDO), and the merge-scale thread layout (`memory/open-threads/`). Detail: What's Been Built below; per-version history: `UPGRADE.md` + session logs.
- **last_enabled:** 2026-06-12
- **last_review:** 2026-08-22 | through 2026-08-22-174047
- **last_invariant_check:** 2026-08-22 | through 2026-08-22-174808 (all 6 confirmed by Eric — walkthrough with live-tree evidence; no-build-step wording refreshed)
- **vision:** `memory/vision.md` (north star; Blueprint gaps in Open Threads below)

## What's Been Built

**Core protocol & templates**
- `ENABLE.md` — 10-step protocol: detection (Step 2), mode selection (Step 3),
  analysis (4), generate/complete (5), bootstrap install (6), `.gitignore` install
  (7), verify (8), report (9), post-enable actions (10); version-aware Mode B
- `MIGRATE.md` — per-vendor migration protocols for 11 vendors (reached via Mode C)
- `AGENTS.md` — exact one-line universal shim to `memory/PROTOCOL.md`
- `memory/PROTOCOL.md` — dual-mode operator dispatch + internal session protocol;
  `templates/memory/PROTOCOL.md` is the installed target-only source
- `CLAUDE.md`, `GEMINI.md`, `.cursorrules`, `.windsurfrules`, Copilot bootstrap
- `templates/` — bootstrap + memory templates with `{{placeholders}}`, including
  `templates/.gitignore` (v3.1.0), `memory/decay-policy.md`, `.agent/version.md`
- `memory/` — this tool's own memory layer (dogfooded)

**Evolving-memory layer (v3.0.0)**
- `DECAY.md` (deterministic integer tier rules), `REVIEW.md` (review ritual),
  `UPGRADE.md` (in-place version ladder, operator-only), `VERSION` (semver)
- `docs/DESIGN-evolving-memory.md` (design) + `docs/assessments/` (industry-alignment baseline)
- `memory/archive/` cold storage; fact metadata footers + `## Memory References`

**v3.1.0**
- AI-infrastructure `.gitignore` propagation into enabled repos (create-or-append,
  de-duplicating, add-only)

**Governance / licensing**
- `LICENSE` (Apache-2.0), `CHANGELOG.md` (Keep a Changelog; v1.0.0–3.1.0)

**Examples**
- `examples/rust-event-bus/` — Mode A, a REAL fixture (unedited output from enabling
  `~/sandbox/rust/rust_event_bus_example`); replaced the old node-project mock
- `examples/migrated-cursor-aider-project/` — Mode C (Cursor + Aider, originals under
  `legacy/`, 3 converted sessions)
- `examples/evolving-memory-example/` — the review ritual in action (continuity
  before/after, archive, session log with Memory References)

## Supported Migration Sources (v2)

Claude Code, Cursor, Cline, Roo Code, Aider, Continue.dev, Codeium/Windsurf,
GitHub Copilot, GPT/Codex agents, Zed AI, Gemini CLI.

## Architectural Invariants

> Hard constraints — the tool's core safety philosophy. These never decay (`core`).
> (Added 2026-06-13 when this repo adopted the evolving-memory layer.)
>
> Each invariant's `(ADR-NNNN)` tag points to its full Architecture Decision Record in
> `docs/arch-decisions/ADR.md` (rationale + trade-offs) — a **pointer for humans**. The invariant text here
> is authoritative for the agent; **don't open `docs/arch-decisions/ADR.md` to orient** — read it on demand only.

- Target-repo scope only (ADR-0001) — never read/modify/move anything outside the resolved
  target-repo root (never `~`, `~/.claude/`, Application Support, AppData, system paths)
  <!-- id: target-repo-scope-only | created: 2026-06-13 | last_used: 2026-06-18 | uses: 12 | tier: core -->
- Never delete vendor files (ADR-0002) — move originals to `legacy/<vendor>/`, preserving paths
  <!-- id: never-delete-vendor-files | created: 2026-06-13 | last_used: 2026-06-18 | uses: 8 | tier: core -->
- Never overwrite, never pick a winner (ADR-0003) — fold vendor steering under
  `## Migrated rules from <vendor>`; surface contradictions as Open Threads
  <!-- id: never-pick-a-winner | created: 2026-06-13 | last_used: 2026-06-18 | uses: 14 | tier: core -->
- No build step; agent-run (ADR-0006) — the tool itself runs no code and needs none (no install, no
  daemon). The markdown files are the product and the agent is the runtime. Optional helpers
  MAY ship — skill-bundled scripts, the operator-side reconcile twins (`scripts/`), the
  committed git-hook fragments, and the forge CI wrappers — but every one is invoked by the
  agent, vendor, git, or CI at the user's direction, never required: the no-runtime fallback
  is real (`MANIFEST.md` is walkable by hand) and nothing daemonizes. (Wording refreshed
  2026-08-22 at invariant re-verify to name the grown helper family — substance unchanged.)
  <!-- id: no-build-step-agent-run | created: 2026-06-16 | last_used: 2026-06-20 | uses: 31 | tier: core | supersedes: no-code-markdown-only | origin: 2026-06-16-002134 -->
- Upgrades are additive and non-destructive (ADR-0005) — enrich and add, never rewrite or delete —
  **except the tool's own managed built-ins** (`memory-lint`, `second-opinion`, `apply-critique`,
  `sync-adapters`, `harvest-knowledge`, `archive-fact`, `refresh-metadata`), which are re-copied (overwritten) on upgrade; that overwrite is scoped to those tool-owned files,
  and a user customizes only by forking under a new skill name (see `ENABLE.md` §5i). For everything
  the user authors, the invariant holds unchanged.
  <!-- id: upgrades-additive | created: 2026-06-13 | last_used: 2026-06-20 | uses: 22 | tier: core -->

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
- **`origin` is GitHub; assume GitHub for git ops** (public repo `acn-ericlaw/agent-memory`,
  Apache-2.0 — migrated from GitLab 2026-06-18; extracted from the publish-github thread at
  the v4.39.0 thread migration)
  <!-- id: github-origin-git-ops | created: 2026-09-01 | last_used: 2026-09-01 | uses: 1 | tier: working -->
- Git hook entrypoints dispatch ordered fragments (ADR-0007) — `.githooks/pre-commit` and
  `.githooks/post-commit` stay minimal and stable; executable `.githooks/<hook>.d/*` fragments run
  in C-locale filename order, all fragments run, and the first non-zero status is returned.
  Agent-memory owns only its `50-` fragments; differently named fragments belong to other layers
  and upgrades preserve them.
  <!-- id: git-hook-fragment-dispatch | created: 2026-08-20 | last_used: 2026-08-21 | uses: 3 | tier: active | origin: 2026-08-20-210047 -->

## Open Threads

> Open Threads live **one per file** in `memory/open-threads/` (`thread-<id>.md`;
> filename = the thread's fact id) so concurrent thread work never merge-conflicts
> (v4.39.0 — `docs/DESIGN-merge-scale.md`). List that directory to see them; unchecked
> `- [ ]` threads are the live workstreams and never decay. Mark a completed thread
> `- [x]` in its file and leave it — the review sweeps it to the archive once older than
> `archive_window` sessions. Don't archive by hand. See `.agent/schema.md`.


## User Preferences

- Never expose the user's absolute home path (`/Users/<name>/…`) in file content —
  use `~`-relative paths. (Stated 2026-06-12; now enforced in ENABLE.md Step 5b +
  schema `repo:` guidance, and flagged by `memory-lint` `[secret-material]` since v4.33.0.)
- Any secrets — PII and credentials — must be redacted from session memory, never
  committed. (Stated 2026-08-13, after a client-side DLP catch; enforced via the
  `memory/PROTOCOL.md` redaction rule + `memory-lint` `[secret-material]`, v4.33.0.)
