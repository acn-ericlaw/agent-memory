# Continuity — agent-memory

> Shared ground truth for this tool's own development state.

---

## Project State

- **project:** agent-memory
- **status:** v3.2.0 — evolving memory (v3.0.0), `.gitignore` propagation (v3.1.0), protocol clarifications from field report (v3.2.0)
- **last_enabled:** 2026-06-12
- **last_session:** 2026-06-13 | agent: Claude Code (2026-06-13-225207)
- **last_review:** 2026-06-13 | through 2026-06-13-223743

## What's Been Built

**Core protocol & templates**
- `ENABLE.md` — 10-step protocol: detection (Step 2), mode selection (Step 3),
  analysis (4), generate/complete (5), bootstrap install (6), `.gitignore` install
  (7), verify (8), report (9), post-enable actions (10); version-aware Mode B
- `MIGRATE.md` — per-vendor migration protocols for 11 vendors (reached via Mode C)
- `AGENTS.md` — dual-mode dispatch (memory protocol + enable)
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

- Target-repo scope only — never read/modify/move anything outside the resolved
  target-repo root (never `~`, `~/.claude/`, Application Support, AppData, system paths)
  <!-- id: target-repo-scope-only | created: 2026-06-13 | last_used: 2026-06-13 | uses: 3 | tier: core -->
- Never delete vendor files — move originals to `legacy/<vendor>/`, preserving paths
  <!-- id: never-delete-vendor-files | created: 2026-06-13 | last_used: 2026-06-13 | uses: 1 | tier: core -->
- Never overwrite, never pick a winner — fold vendor steering under
  `## Migrated rules from <vendor>`; surface contradictions as Open Threads
  <!-- id: never-pick-a-winner | created: 2026-06-13 | last_used: 2026-06-13 | uses: 2 | tier: core -->
- No-code, markdown-only — the files are the product; the agent is the runtime
  <!-- id: no-code-markdown-only | created: 2026-06-13 | last_used: 2026-06-13 | uses: 3 | tier: core -->
- Upgrades are additive and non-destructive — enrich and add, never rewrite or delete
  <!-- id: upgrades-additive | created: 2026-06-13 | last_used: 2026-06-13 | uses: 4 | tier: core -->

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

### Evolving long-term memory layer (v3.0.0) — BUILT 2026-06-13
- [x] **Evolving-memory layer implemented.** Design: `docs/DESIGN-evolving-memory.md`.
  Deterministic integer tier rules (no float `strength`); event-sourced metadata
  (derived from session-log `## Memory References` at review); stable kebab fact IDs;
  `sessions/` = immutable event log; tiers by counting session files; decay sweeps
  completed `[x]` threads; auto-core off (human-set); default windows 3/8/20, review
  every 10. Created: `DECAY.md`, `REVIEW.md`, `UPGRADE.md`, `VERSION` (3.0.0),
  `templates/memory/decay-policy.md`, `templates/.agent/version.md`,
  `examples/evolving-memory-example/`. Wired: `templates/memory/continuity.md`
  (Architectural Invariants + last_review + metadata note), `templates/.agent/schema.md`
  (metadata fields + Memory References + new files), `templates/AGENTS.md` + root
  `AGENTS.md` (Before/During/After), `ENABLE.md` (Step 5e generate, Step 6 install
  DECAY/REVIEW, version-aware Mode B, Step 8 verify), root `CLAUDE.md` + `README.md`
  (architecture + version table + evolving-memory section).
- [x] **Versioning + in-place upgrade.** Root `VERSION` (semver); per-repo
  `.agent/version.md` stamp; `UPGRADE.md` ladder reached only via ENABLE Mode B
  (operator-only, like MIGRATE.md ← Mode C). 2.x→3.0.0 rung backfills ids/metadata.
- [x] **Refinement vs. literal plan:** DECAY.md/REVIEW.md are *installed into every
  enabled repo's root* (the ritual runs inside the repo), not tool-operator-only.
  UPGRADE.md stays operator-only. (Flagged to user.)
- [ ] **Dogfood backfill (optional):** this repo adopted the layer — added
  Architectural Invariants (core), `memory/decay-policy.md`, `memory/archive/INDEX.md`,
  `last_review`, and Memory References in session logs going forward. Legacy facts in
  What's Been Built / Key Decisions are grandfathered as `active` (no metadata footers
  yet); backfill them with ids/metadata if/when desired (or let the first review do it).
- [x] **Validate version-aware Mode B + UPGRADE.md** — test-drove on TWO real
  pre-versioning repos (2026-06-13), both 2.x → 3.0.0 in place, both idempotent:
  - `~/sandbox/mercury-composable` (orig. Mode C, git-tracked): committed `0d4cc3b9`;
    promote-into-invariants style (2 hard constraints moved up from Key Decisions).
  - `~/sandbox/rust/rust_event_bus_example` (orig. Mode A, **not git-tracked**):
    additive-only style (no content moved); source untouched. (No git → not committed.)
  All files present, no placeholder/path leaks, sessions untouched, no protocol
  ambiguity. Validated across both original modes (A, C) and git/non-git.
- [x] **First review cycle ran** (2026-06-13, 10 session files, `review_every: 10`).
  Recompute + re-tier validated on real `## Memory References` data (4 of 10 logs
  carried events; the 6 pre-adoption logs none). `uses` recomputed (e.g.
  upgrades-additive 1→4, target-repo-scope-only / no-code-markdown-only 1→3); 2
  completed threads re-tiered active→working per the rules. **Archive/sweep paths NOT
  yet exercised** — nothing is older than `archive_window` (20 sessions); revisit when
  facts actually age out. Observation: the tier model has no "done" state for completed
  `[x]` threads — they read as `working` until swept (candidate refinement).
- [ ] Optionally update `examples/` to mention the mercury upgrade as a real Mode B
  upgrade fixture (analogous to rust-event-bus being a real Mode A).

### Shipped — v3.1.0: AI-infrastructure `.gitignore` propagation (2026-06-13)
- [x] **Propagate the `.gitignore` design into enabled repos.** Found during the
  first real-work dogfood (enabling `~/sandbox/simple-proxy`): the tool's own repo
  ignores personal AI-IDE runtime dirs (`.claude/`, `.kiro/`, `.cursor/`, …) but
  `ENABLE.md` Step 7 never passed that on — it only appended a comment to an
  *existing* `.gitignore` and refused to create one. Fix shipped as **v3.1.0**
  (additive → MINOR): new `templates/.gitignore` (sentinel-headed managed block);
  `ENABLE.md` Step 7 now creates-or-appends idempotently (add-only, never reorders);
  Step 8 verifies it; Step 9 report + Notes scope list updated; `UPGRADE.md` rung
  3.0.0→3.1.0 added; `VERSION`→3.1.0; version tables in `UPGRADE.md`/`README.md` and
  `CHANGELOG.md` updated. Steering files + `memory/` stay tracked (verified via
  `git check-ignore`).
  <!-- id: gitignore-propagation-v310 | created: 2026-06-13 | last_used: 2026-06-13 | uses: 2 | tier: active -->
- [x] **Validated via Mode B upgrade of `~/sandbox/mercury-composable`** (3.0.0→3.1.0,
  2026-06-13). Two refinements surfaced and fixed during the run: (1) **de-dup** — the
  "no sentinel → append full block" wording would have duplicated `.kiro/` (already in
  mercury's pre-existing `.gitignore`); `ENABLE.md` Step 7 + the UPGRADE rung now append
  only entries not already present anywhere in the file. (2) **`legacy/` contradiction**
  — mercury ignores `legacy/` though `legacy/claude-code/CLAUDE.md` is tracked and the
  design treats legacy as committed; surfaced as an Open Thread in the target (never
  pick a winner), not auto-fixed. Verified: no dup `.kiro/`, steering/memory tracked,
  runtime dirs ignored, idempotent re-run is a no-op, stamp 3.1.0 (enabled_with/mode
  preserved). Target not committed (separate repo; offered to user).
  <!-- id: gitignore-v310-mercury-validation | created: 2026-06-13 | last_used: 2026-06-13 | uses: 1 | tier: working -->

### Shipped — v3.2.0: protocol clarifications from a real-work field report (2026-06-13)
- [x] **Acted on a field report** from a separate Claude Code session that refactored
  `~/sandbox/simple-proxy` Node.js→Rust (itself validating the self-contained-target
  design). Shipped 5 fixes as v3.2.0 (docs/wording, no file-shape change): (1) session
  = **one log-write** (several per conversation OK), `start` now **best-effort** — no
  fabricated timestamps; (2) **metadata ownership** pinned + a real contradiction fixed
  (ENABLE Step 5b seeded new facts `tier: active` while DECAY/AGENTS said `working` →
  now uniformly **born working**; agent seeds id/created/tier/uses:1, review owns
  uses/last_used/tier); (3) surfaced the **leave-`[x]`-for-the-review** rule to the
  agent; (4) **stack-fact altitude** — `continuity.md` Stack & Tools is canonical,
  instructions points there; (5) **after-session checklist** in AGENTS + an optional
  hook recipe (`docs/optional-ritual-hook.md`). Touched DECAY, schema, both AGENTS,
  ENABLE, templates, UPGRADE (+3.1.0→3.2.0 rung), VERSION→3.2.0, README/CHANGELOG.
  Report archived at `docs/assessments/2026-06-13-protocol-field-report.md`.
  <!-- id: field-report-v320 | created: 2026-06-13 | last_used: 2026-06-13 | uses: 1 | tier: working -->

### First real-work dogfood — enabled `~/sandbox/simple-proxy` (Mode A, 2026-06-13)
- [x] **Real Mode A fresh enable** of a zero-dep Node.js TCP-proxy CLI (no prior AI
  footprint). 15 files generated, source untouched, verified. Logged 7 refactor Open
  Threads in the target's continuity (package.json `main` points at a non-existent
  file; stale README `moment`/`source_port` references; ES5 modernization; duplicate
  code across the two entry points; per-connection signal handlers; no tests). This
  enable is what surfaced the `.gitignore` gap above. Target later stamped 3.1.0.
  Refactor of the target is the user's planned next step.
  <!-- id: dogfood-simple-proxy-enable | created: 2026-06-13 | last_used: 2026-06-13 | uses: 2 | tier: active -->
- [x] **Design validated: enabled target repos are self-contained.** The user chose to
  run the simple-proxy refactor in a *separate* Claude Code session launched inside the
  target — driven by simple-proxy's own `CLAUDE.md`→`AGENTS.md`→`memory/`, needing no
  knowledge of this tool. Confirms the two-layer model: the tool's job ends at
  enablement; the enabled repo then stands on its own. Baselines committed cleanly
  (simple-proxy: source import + AI-enable; mercury: v3.1.0 upgrade) so the new
  sessions start from committed state. (2026-06-13)
  <!-- id: dogfood-target-repo-self-contained | created: 2026-06-13 | last_used: 2026-06-13 | uses: 1 | tier: working -->

### Backlog — vNext (temporal & supersession) + beyond
> From the 2026-06-13 industry-alignment assessment:
> `docs/assessments/2026-06-13-industry-alignment.md`. Verdict: on track; distinctive
> on event-sourcing/determinism/governance; one real gap = temporal/supersession.
> Re-run the assessment after meaningful iterations and compare its scorecard.

- [ ] **P1 — Supersession / fact-invalidation semantics.** On a reversed decision,
  tombstone the old fact (`superseded-by: <id>`; new fact `supersedes: <id>`) and
  archive it flagged "superseded", not "faded". Markdown-native `expired_at`/`invalid_at`
  (cf. Zep); closes assessment gaps #1+#2; buys the "knowledge updates" ability.
  Touches DECAY.md, REVIEW.md, schema, examples. Highest-value next step.
  <!-- id: backlog-supersession | created: 2026-06-13 | last_used: 2026-06-13 | uses: 1 | tier: active -->
- [ ] **P2 — Invalidation cadence for never-decay facts.** Add `verify_invariants_every: N`
  to decay-policy.md; review prompts a human to confirm `core`/Architectural Invariants
  are still true (never-decay ≠ never-checked).
  <!-- id: backlog-invariant-verify-cadence | created: 2026-06-13 | last_used: 2026-06-13 | uses: 1 | tier: active -->
- [ ] **P3 — Write-time contradiction flag.** Extend the migration-time contradiction
  check into REVIEW.md: when a fact is added, scan for one it contradicts → raise an
  Open Thread (SSGM "pre-consolidation validation", scaled down).
  <!-- id: backlog-contradiction-check | created: 2026-06-13 | last_used: 2026-06-13 | uses: 1 | tier: active -->
- [ ] **P4 — Minimal memory eval.** `memory-smoke-test.md`: N questions a fresh agent
  should answer from memory alone. Manual, but app-level eval is unsolved industry-wide.
  <!-- id: backlog-memory-eval | created: 2026-06-13 | last_used: 2026-06-13 | uses: 1 | tier: active -->
- [ ] **P5 — Provenance surfacing + retrieval-at-scale.** Surface each fact's originating
  session; lean on archive/INDEX.md (+ optional sessions/INDEX.md) as the no-code
  mitigation if memory grows large. Full vector/semantic retrieval stays out of scope.
  <!-- id: backlog-provenance-retrieval | created: 2026-06-13 | last_used: 2026-06-13 | uses: 1 | tier: active -->
- [ ] **Dogfooding on real work (ongoing).** Already delivering: the simple-proxy
  enable surfaced v3.1.0 (`.gitignore`), and the simple-proxy Node→Rust refactor's
  field report drove v3.2.0 (protocol clarifications). Keep feeding real-work insights
  back into this backlog. (Stated 2026-06-13.)
  <!-- id: backlog-real-work-dogfood | created: 2026-06-13 | last_used: 2026-06-13 | uses: 3 | tier: active -->

- [ ] ~~**Knowledge graph layer — SurrealDB for long-term memory.**~~ **Set aside**
  (2026-06-13) in favor of the markdown-native evolving-memory layer above. Not
  deleted — revisit if the markdown layer hits limits. Original open questions:
  replace vs supplement markdown; entity/relation schema; agent interaction
  (SurrealQL/REST/SDK); fit with no-code philosophy; single- vs multi-agent access;
  Cloud vs self-hosted.

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
