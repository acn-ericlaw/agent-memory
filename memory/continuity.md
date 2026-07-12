# Continuity — agent-memory

> Shared ground truth for this tool's own development state.

---

## Project State

- **project:** agent-memory
- **status:** v4.29.0 — a vendor-neutral, no-code (markdown) shared-AI-memory + AI-enablement tool. Three shared layers: **backward memory** (v3.x — fact metadata + ids, decay/review/archive), a **forward VBDI cognitive loop** (v4.0 — Vision→Blueprint→Design→Impl over the memory substrate), and a **cross-vendor skills layer** (v4.1+ — neutral committed `agent-skills/` + a runnable `sync-adapters`; six adapter targets: Claude/Gemini/Cursor/Kiro/Copilot/Antigravity). Agent-as-runtime; `memory/` is committed + shared. Built-in skills: `memory-lint`, `second-opinion`+`apply-critique`, `sync-adapters`, `harvest-knowledge`, `archive-fact`, `refresh-metadata`. Vendor-neutral ritual triggers (committed git hook + CI floor) with first-run self-init; Windows LF hardening. **Per-version history lives in `UPGRADE.md` (the version ladder) + `memory/sessions/` — kept OUT of this line by design (v4.22.0): `status` is a short current-state descriptor, not a changelog, so this shared line doesn't become a merge-conflict hotspot.** `.agent/version.md` is the canonical version. Validated across six vendors (Claude, Gemini, Cursor, Kiro, Copilot CLI, Antigravity).
- **last_enabled:** 2026-06-12
- **last_session:** 2026-07-12 | agent: Claude Code (2026-07-12-022432)
- **last_review:** 2026-06-30 | through 2026-06-30-055707
- **last_invariant_check:** 2026-06-27 | through 2026-06-27-215825
- **vision:** `memory/vision.md` (north star; Blueprint gaps in Open Threads below)

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
  daemon). The markdown files are the product and the agent is the runtime. A skill MAY
  bundle optional helper scripts, but those are invoked by the agent/vendor at the user's
  direction, never executed by the tool.
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

## Open Threads

- [ ] **(backlog) Before-session presence for Cursor/Kiro — path-scoped steering imports.** From a
  maintainer question after v4.29.0 shipped ("what about other vendors' entry points?"). v4.29.0
  covered the only two entry files with native import syntax (`CLAUDE.md` `@path`, `GEMINI.md`
  `@./path.md`); AGENTS.md-native runtimes (Codex, Kiro, Antigravity) already auto-load the hub —
  only the `AGENTS.md → memory/*` hop stays voluntary; Copilot/`.cursorrules`/`.windsurfrules` have
  no import mechanism (the v4.20.1 front-load pattern is the one inline lever — small stable
  snippets only, never protocol copies). **Two real levers exist, blocked by our own `.gitignore`
  stance, not the vendors:** Cursor modern rules (`.cursor/rules/*.mdc`) attach files via
  `@`-references; Kiro steering (`.kiro/steering/*.md`) supports `#[[file:…]]` inclusion. Both dirs
  are gitignored-personal wholesale today; adopting needs a **path-scoped carve-out** (the
  `.github/skills/`-inside-tracked-`.github/` pattern) + a committed steering file per vendor.
  **Don't build speculatively** — trigger is a Cursor or Kiro team reporting the context-read
  failure class (complaints = adoption signal). → serves: vision-agent-memory
  <!-- id: ot-before-session-cursor-kiro-backlog | created: 2026-07-12 | last_used: 2026-07-12 | uses: 1 | tier: working | origin: 2026-07-12-022432 -->

- [x] **Shipped v4.28.0 (MINOR) — co-author convention cleanup: stable agent identity + one trailer.** From a
  real-world finding dogfooding v4.27.0 on **mercury-composable**: a squash-merged PR (#126) showed the
  `Co-Authored-By` self-identification renders imperfectly (attribution itself worked — human + AI both
  credited). **(1) Identity churn:** the convention said "identify the same way as session logs," but logs
  use the stable `Claude Code` while the commit/PR trailer was the **model version** `Claude Opus 4.8` — not
  "the same," and it fragments attribution across model releases. Fix: use the **stable agent name** (the
  actual AI collaborator — `Claude Code`/`Gemini CLI`/…, kept neutral via a `<your agent name>` placeholder),
  **not** a model version. **(2) Trailer pile-up:** every commit carries the trailer, so a squash stacked ~9
  inline copies **plus** GitHub's consolidated one after `---------`; convention now says collapse to a
  **single** trailer on squash (GitHub's appended one is canonical; trim the inline repeats). Both advisory —
  the agent can't suppress the harness trailer or GitHub's squash template. Lockstep: `AGENTS.md` (root +
  template) + PR-template footer comment, `VERSION`→4.28.0, `CHANGELOG`, `README` (row + 10-cap trim),
  `UPGRADE` (row + rung), docs site. No memory-shape/skill/adapter change. → serves: vision-agent-memory
  (authorship stays a faithful, stable representation of the AI collaborator over time)
  <!-- id: coauthor-stable-identity-v4280 | created: 2026-06-30 | last_used: 2026-06-30 | uses: 1 | tier: working | origin: 2026-06-30-054342 -->

- [x] **Shipped v4.27.0 (MINOR) — standardized PR descriptions: lead with What / Why.** From a **maintainer
  suggestion** to standardize the look-and-feel of pull-request descriptions and **propagate it to every
  AI-enabled repo**. A natural fit — *why* is already a first-class artifact throughout the protocol (VBDI
  intent trace, ADR rationale, supersession reasons, the changelog's own `> summary + Why` shape), and the
  content projects from the session log(s) in the PR (What from the change, Why from the Blueprint gap /
  decision). Confirmed **no prior PR guidance existed** (only the commit `Co-Authored-By` trailer) — a real
  gap. **Shape:** two sections, **What** + **Why** (substantive intent, not a restatement of What), each 1–2
  short paragraphs (flexible, not rigidly two), closing with a self-identifying `Co-Authored-By:` footer
  (extends the commit/session-log authorship convention to the PR altitude); **advisory, never a gate**
  (`guide-don't-prescribe`). **Built**
  `.github/pull_request_template.md` (this repo + `templates/`, so enabled repos inherit it) + an `AGENTS.md`
  convention (root + template) as the **vendor-neutral backstop** (the template only covers GitHub web UI /
  `gh pr create`; the steering line covers agents composing a PR body) + a checklist line. Lockstep:
  `ENABLE.md` Step 6 (install template), `VERSION`→4.27.0, `CHANGELOG`, `README` (row + file tree), `UPGRADE`
  (row + rung), docs site (`getting-started`). No memory-file shape change. → serves: vision-agent-memory
  (faithful, traceable delivery — intent is carried at the PR altitude too, across vendors)
  <!-- id: pr-what-why-convention-v4270 | created: 2026-06-29 | last_used: 2026-06-30 | uses: 2 | tier: active | origin: 2026-06-29-175644 -->

- [x] **Shipped v4.26.1 (PATCH) — `[stale-metadata]` / `refresh-metadata` no longer opine on a pinned
  thread's tier.** From a **mercury sanity check** (post-Copilot review): v4.26.0 flagged every
  `working`-tagged pinned `- [ ]` open thread as "should be `active`" — noise, since a pinned thread never
  decays *regardless* of its tier label (its **pinned-ness** protects it, not the label). Refinement: both
  `expected_tier`s (memory-lint check 9 + refresh-metadata) now return a pinned thread's **stored** tier — no
  flag, no rewrite — while still refreshing its factual `uses`/`last_used`. Surfaced by the comparison of
  `refresh-metadata` vs Copilot's `update-metadata.py` (which *skipped* pinned threads; this lands on the same
  outcome by a cleaner rule, and `refresh-metadata` is otherwise a strict, safer superset — preserves all
  footer fields, reads `decay-policy.md`, clamps at archive-candidate). The same sanity check confirmed
  **no data loss** on mercury (it never used `supersedes`/`superseded-by`/`formalizes` footer fields) and a
  **correct archival**. Lockstep: memory-lint + refresh-metadata scripts + tests (memory-lint 34), `DECAY.md`
  rule 4, both SKILL.md notes, `VERSION`→4.26.1, `CHANGELOG`, `README`, `UPGRADE` (row + rung). Descriptions
  unchanged → adapters untouched. → serves: vision-agent-memory (the advisory stays signal, not noise)
  <!-- id: pinned-tier-refinement-v4261 | created: 2026-06-28 | last_used: 2026-06-28 | uses: 1 | tier: active | origin: 2026-06-28-181738 -->

- [x] **Shipped v4.26.0 (MINOR) — `refresh-metadata` (7th built-in) + a `memory-lint` `[stale-metadata]`
  advisory.** From a **cross-vendor field test**: Copilot / Gemini 3.1 Pro committed the v4.25.0 upgrade to
  mercury and, seeing `[review-overdue]`, **ran the review unprompted** — correctly using `archive-fact`
  (the over-archival guard even caught a premature archive of `adr-pattern-adopted` → it reverted). But it did
  Step 4 (archive) + Step 5 (sweep) and **skipped Step 2 (apply events) + Step 3 (re-tier)**, leaving stale
  `last_used`/`uses`/`tier` footers. **Third instance of one failure class** (truncation → `archive-fact`;
  never-fired review → `[review-overdue]`; now half-done ritual): multi-step agent rituals get partially
  executed. **The fix refines the judgment-vs-arithmetic boundary** — deciding *what to archive* is judgment
  (stays with the agent); recomputing metadata is **arithmetic** (REVIEW.md's "full rebuild," deterministic),
  safe to mechanize. **Built** `agent-skills/refresh-metadata/` (recompute footers from the reference log,
  read-into-memory-write-once; `core`/`superseded`/never-referenced untouched; clamps at `archive-candidate`,
  never archives) + `memory-lint` check (9) `[stale-metadata]` (stored tier ≠ recomputed). Both Python+Node at
  parity + mirror tests (memory-lint 33, refresh-metadata 5). **Dogfooded:** the new advisory flagged 11 stale
  footers on THIS repo (my own earlier reviews skipped re-tiering too — universal, not vendor-specific);
  `refresh-metadata` cleared all 11 → lint 0/0. Lockstep: skill + tests, memory-lint + tests, `REVIEW.md`
  (steps 2–3), `ENABLE.md` §5i (7 built-ins), `README`/`ADR`/continuity lists, adapters (8 skills → 48),
  `VERSION`→4.26.0, `CHANGELOG`, `UPGRADE` (row + rung). → serves: vision-agent-memory (the review's
  deterministic half is now mechanized; only judgment is left to the agent — across vendors)
  <!-- id: refresh-metadata-builtin-v4260 | created: 2026-06-28 | last_used: 2026-06-28 | uses: 2 | tier: active | origin: 2026-06-28-175909 -->

- [x] **Shipped v4.25.0 (MINOR) — `archive-fact`, a deterministic safe archive-move helper (6th built-in).**
  From a **cross-vendor critique** (Copilot / Gemini 3.1 Pro, `review-scratch/critique.md`): "agent behaviors
  vary by vendor; relying on agent interpretation of `REVIEW.md` to safely mutate state is vulnerable to LLM
  regressions / file-editing precision — harden the memory-writing mechanism itself (a small CLI helper for
  safe writes)." Spot-on, and it names our **most-repeated bug**: the `open(f,"w").write(open(f).read()+…)`
  truncate-before-read trap (wiped a `version.md` stamp, then this repo's archive 50→6, once each;
  [[version-md-stamp-safe-write]]). v4.22.4 moved the safeguard personal-note → shared doc; this is doc →
  **tool**. **Built** `agent-skills/archive-fact/` (`provenance: agent-memory-builtin`): executes `REVIEW.md`
  step 4's move (extract block by footer id → append to quarter archive + INDEX → rewrite continuity
  *read-into-memory-then-write-once*). Python + Node at output parity + mirror tests; guards refuse a missing/
  already-archived id or a would-empty move (all-or-nothing); `--dry-run`. **Keeps the meaning/mechanics
  split** (same as `memory-lint`): the agent decides *what* to archive, the helper does the *move* — it never
  decides (`never-pick-a-winner`). Lockstep: skill + tests, `REVIEW.md` step 4 (preferred path), `ENABLE.md`
  §5i (6 built-ins), `README`/`ADR`/continuity built-in lists, adapters synced (7 skills → 42),
  `VERSION`→4.25.0, `CHANGELOG`, `UPGRADE` (row + rung). → serves: vision-agent-memory (faithful enablement —
  the riskiest state-mutation is now deterministic, not left to per-vendor agent diligence)
  <!-- id: archive-fact-builtin-v4250 | created: 2026-06-28 | last_used: 2026-06-28 | uses: 1 | tier: active | origin: 2026-06-28-172159 -->

- [ ] **(backlog) Mode B upgrade automation — scope the mechanical steps only.** From the same Gemini critique
  (point 1): as the user base grows, the high-touch Mode B upgrade (re-sync specific files, run tools, stamp
  version) could be a source of drift/user error; "consider automating more of `ENABLE.md` Mode B via a
  script." **Deliberate tension:** the rungs are *semantic merges* (additive, preserve customizations, "re-sync
  `AGENTS.md` but never the root one") that must stay agent-judged — the chosen mitigation is **deterministic
  guardrails** (`check_version_manifest`, the v4.24.0 review-cadence advisory), not full automation. *If*
  revisited, script only the **mechanical** parts (file copies, version stamp — like `sync-adapters` did in
  v4.18.0) and leave the merges to the agent. Lower priority; logged so the critique isn't lost.
  <!-- id: ot-mode-b-automation-backlog | created: 2026-06-28 | last_used: 2026-06-28 | uses: 1 | tier: active | origin: 2026-06-28-172159 -->

- [x] **Shipped v4.24.0 (MINOR) — decay-policy retune + a review-cadence/size advisory in `memory-lint`.**
  From a maintainer question (after the v4.23.2 review flagged continuity at 490 lines, still over the old
  300 cap): "recommend new parameters based on the mercury-composable learning." **Measured both enabled
  repos:** this tool (121 sessions, continuity 490 lines / 24 facts *right after a clean review*) and
  `mercury-composable` (61 sessions, **585 lines / 41 facts, 0 archived** — the cadence review had never
  fired in the field). **Four findings:** (1) `continuity_max_lines: 300` was permanently-red on both
  (alert fatigue) + conflates non-decaying structural sections with the decaying region; (2) no
  count-based trigger, though fact-count is the verbosity/velocity-independent signal; (3) **nothing
  enforced the review cadence** (mercury's smoking gun); (4) `verify_invariants_every: 20` = near-daily
  human re-confirms at burst velocity. **Shipped:** `memory-lint` advisory check (8) — `[review-overdue]`
  (reads the `last_review` stamp) + `[continuity-bloat]` (facts/lines), **both runtimes at parity + mirror
  tests (29 each)**; the keystone, since parameters alone can't fix a review that never runs. Retuned
  defaults: `continuity_max_facts: 30` (NEW, primary), `continuity_max_lines: 300→600`,
  `verify_invariants_every: 20→40`; `working/active/archive_window` + `review_every` unchanged (they work —
  bloat came from reviews not running). Lockstep: lint scripts+tests, `decay-policy.md` (template + this
  repo), `REVIEW.md`, `SKILL.md`, `AGENTS.md` (root+template), `.agent/schema.md`, `VERSION`→4.24.0,
  `CHANGELOG`, `README` (table), `UPGRADE` (row + rung). Skill description unchanged → adapters untouched.
  → serves: vision-agent-memory (faithful, verifiable enablement — the layer's own health is enforced by a
  deterministic check, not left to agent diligence; the lesson came from a real product repo's drift)
  <!-- id: decay-policy-retune-v4240 | created: 2026-06-28 | last_used: 2026-06-28 | uses: 1 | tier: archive-candidate | origin: 2026-06-28-165455 -->

- [x] **Shipped v4.23.1 (PATCH) — `last_harvest` marker for incremental harvests.** From a **cross-vendor
  test drive**: mercury-composable's own agent ran `harvest-knowledge` correctly (clean no-op — memory was
  already current; full protocol followed, good map-don't-mirror judgment) but had to **infer the harvest
  window** ("since enable") because nothing recorded *when the last harvest ran*. **Fix:** an optional
  `last_harvest: YYYY-MM-DD | through <session>` field in `continuity.md` Project State (with `last_review`
  / `last_invariant_check` — same family: "when did this periodic memory ritual last run"). **Decided
  against `.agent/version.md`** (the install manifest, version-gating — a different concern; like-with-like
  + separation-of-concerns favored Project State; maintainer agreed). `harvest-knowledge` now **reads** it
  to scope the next run and **stamps** it on completion (even a no-op — "docs checked through here"); the
  check-existing-first guard still prevents duplicates so a re-scan stays safe (`last_harvest` only
  *scopes*). Wired: `templates/.agent/schema.md` (field), `harvest-knowledge/SKILL.md` (read step 2 + stamp
  step 7), `VERSION`→4.23.1, `CHANGELOG`, `README` (table), `UPGRADE` (row + `4.23.0→4.23.1` rung). Skill
  *description* unchanged → adapters unchanged. → serves: vision-agent-memory (recurring harvest scopes
  incrementally; the marker mirrors the review's `last_review`) (`last-harvest-marker-v4231`).
  <!-- id: last-harvest-marker-v4231 | created: 2026-06-28 | last_used: 2026-06-28 | uses: 1 | tier: archive-candidate | origin: 2026-06-28-041540 -->

- [x] **Shipped v4.23.0 (MINOR) — `harvest-knowledge` built-in skill (on-demand doc→memory harvest).**
  Surfaced when test-driving the mercury-composable upgrade: the curious harvest (v4.22.0, `ENABLE.md`
  Step 4b) seeds memory **once** at enable, but a *living* repo's docs keep evolving with no recurring way
  to fold new ADRs/design-specs/decision-log entries into memory. Maintainer's call: **leave the
  enable-time (re-)harvest a fresh-enable event (Mode A), and make the recurring need a skill.** Added a
  **5th built-in** `agent-skills/harvest-knowledge/` (`provenance: agent-memory-builtin`, no-code/agent-run):
  re-scan human-authored docs (same net as Step 4b) → distill durable facts into **neutral, shared**
  `memory/` **additively** (map-don't-mirror; check-existing-first so a re-run doesn't duplicate; conflicts
  → `Contradiction`; supersede a genuine replacement; budget-with-disclosure). **Explicitly not a vendor
  `/init`** (which does *code*-analysis → a *vendor* steering file, overwriting): this does
  knowledge-distillation → neutral memory, additive + repeatable — borrow /init's muscle, output stays
  neutral. Removed the inline Mode B re-harvest from the `4.21.0→4.22.0` upgrade rung (it's the skill's job
  now). Wired: `ENABLE.md` §5i (5 built-ins) + Step 8 list, `upgrades-additive` invariant + ADR-0005 (5
  built-ins), README (tree + version table), `CHANGELOG`, `UPGRADE` (row + `4.22.4→4.23.0` rung),
  `VERSION`→4.23.0; adapters synced (6 skills → 36; harvest-knowledge 6/6). `memory-lint` OK. → serves:
  vision-agent-memory (curiosity becomes a recurring capability for living repos, not a one-shot)
  (`harvest-knowledge-skill-v4230`).
  <!-- id: harvest-knowledge-skill-v4230 | created: 2026-06-28 | last_used: 2026-06-28 | uses: 2 | tier: archive-candidate | origin: 2026-06-28-032539 -->

- [x] **Shipped v4.22.4 (PATCH) — safe-write safeguard moved into the SHARED layer (`REVIEW.md`).**
  Maintainer correction: the safe-write lesson from the 2026-06-28 archive-truncation incident
  (`open(f,"w").write(open(f).read()+…)` wiped the archive 50→6) had only been recorded in my **personal**
  `~/.claude/` memory — per-machine, useless to teammates/other vendors. A safeguard protecting the review
  ritual belongs in the **committed shared layer** (the tool's own two-layer principle: personal prefs in
  `~/`, shared project knowledge in the repo). **Fix:** added two rules to `REVIEW.md` → **Safety** —
  (1) never truncate a memory file when scripting the move (append-mode `>>` / read-into-var for the
  archive/`INDEX.md`/`continuity.md`; never the truncate-before-read one-liner); (2) **run `memory-lint`
  after any scripted memory mutation** (it catches truncation — count drops, links dangle — and git-tracked
  files recover via `git checkout HEAD`). `REVIEW.md` is installed verbatim into every enabled repo, so all
  contributors + vendors now inherit it. (Kept the personal memory too — broadened it — but `REVIEW.md` is
  the authoritative team-facing safeguard.) Lockstep: `REVIEW.md`, `VERSION`→4.22.4, `CHANGELOG`, `README`
  (table +1/−1, drops 4.19.0), `UPGRADE` (row + `4.22.3→4.22.4` rung). → serves: vision-agent-memory
  (operational safety for the shared memory layer must itself be shared, not per-machine)
  (`safe-write-review-safety-v4224`).
  <!-- id: safe-write-review-safety-v4224 | created: 2026-06-28 | last_used: 2026-06-28 | uses: 1 | tier: archive-candidate | origin: 2026-06-28-025906 -->

- [x] **Shipped v4.22.3 (PATCH) — tightened the post-commit session window 2h → 30 min.** Maintainer
  observed the v4.22.1 window (2h) was too long: the real problem was follow-up stubs **minutes** apart,
  and 2h is long enough to wrongly conflate a *genuinely new* session that starts within 2h of the prior
  session's log (the hook would nudge "enrich the old log" for new work). **Fix:** default window → **30
  min** (spans a session's commit cadence incl. a short test/think gap; a new session after a >30-min pause
  still gets its own stub). The override env var changed unit to **minutes** —
  `AGENT_MEMORY_SESSION_WINDOW_MINUTES` (was `_HOURS`) — because BSD `date -v` rejects a fractional hour
  (`-v-0.5H`), so a sub-hour default needs integer minutes; both runtimes still supported (`date -v-30M` /
  `date -d "30 minutes ago"`). Re-validated (2m/25m → suppress; 45m/none → stub; custom override honored).
  Lockstep: `.githooks/post-commit`, `.githooks/README.md`, `docs/DESIGN-ritual-triggers.md`,
  `VERSION`→4.22.3, `CHANGELOG`, `README` (table +1/−1, drops 4.18.0), `UPGRADE` (row + `4.22.2→4.22.3` rung).
  → serves: vision-agent-memory (the backstop should distinguish a session from a new one, not over-suppress)
  (`session-window-30min-v4223`).
  <!-- id: session-window-30min-v4223 | created: 2026-06-28 | last_used: 2026-06-28 | uses: 1 | tier: archive-candidate | origin: 2026-06-28-024518 -->

- [x] **Shipped v4.22.2 (PATCH) — lightweight mode: one log per *session*, not per *commit* (agent-side
  mirror of v4.22.1).** Maintainer accepted the recommendation flagged at v4.22.1: the same per-commit
  granularity the hook fix addressed also lived on the **agent-behavior** side — the lightweight-mode rule
  wrote a lite session log for *every* memory-neutral tracked-file change, so an agent making several small
  commits in one sitting produced a near-duplicate lite log per commit (clutter + decay session-count
  inflation). **Fix:** `AGENTS.md` (root + template) lightweight "lite log" tier now says — if a session log
  already exists for *this* working session, a later **memory-neutral** commit **enriches** that log (a
  one-line "also: …" note) rather than spawning another. The agent needs **no time-window** (unlike the
  hook): it *knows* it's the same working session. Explicitly preserves the existing model for
  **memory-relevant** work — distinct events each get their own full log (a multi-task conversation may
  still yield several), so this only coalesces *trivial* follow-ons. **Dogfooded immediately:** this very
  v4.22.2 work is memory-relevant → it got its **own** full log (this session), while the prior trivial doc
  commits would now coalesce. Wording-only — no shape/skill/hook change. Lockstep: `AGENTS.md` (root +
  template), `VERSION`→4.22.2, `CHANGELOG`, `README` (table +1/−1, drops 4.17.0), `UPGRADE` (row +
  `4.22.1→4.22.2` rung). → serves: vision-agent-memory (the decay model's integrity needs the session-file
  count to track *sessions*, not commits — closed on both the hook and agent sides) (`lite-log-per-session-v4222`).
  <!-- id: lite-log-per-session-v4222 | created: 2026-06-28 | last_used: 2026-06-28 | uses: 1 | tier: archive-candidate | origin: 2026-06-28-023654 -->

- [x] **Shipped v4.22.1 (PATCH) — post-commit auto-stub is per *session*, not per *commit*.** From
  **downstream `mercury-composable` feedback** (`review-scratch/feedback-2026-06-27-post-commit-session-stub.md`):
  the `.githooks/post-commit` auto-stub fired on **every** work commit because its only de-dup guard checked
  for an *untracked* stub — once the agent committed the session log, the next work commit found no waiting
  stub and wrote a fresh one (~6 near-identical lite logs/session, each with an extra `memory:` commit, and
  — since the decay model counts session files — `sessions_since_last_used` inflated so facts decayed ~N×
  fast; ironic given `memory-lint` exists to catch decay miscounts). **Fix:** the auto-stub now suppresses a
  new stub when a session log exists **within an active-session window** (default 2h; override
  `AGENT_MEMORY_SESSION_WINDOW_HOURS`), nudging the agent to **enrich that log** instead. Detected by the
  newest session **filename** timestamp — **immutable + clone-safe** (deliberately *not* `mtime`, which
  `git clone`/checkout resets to now → would wrongly suppress stubs for hours after a clone) — compared
  lexicographically to a window-ago stamp (`YYYY-MM-DD-HHMMSS` sorts chronologically). Subsumes the old
  untracked guard (a fresh stub has a recent filename) and covers the just-committed case; a genuinely new
  session (no log in window) still stubs (no silent gap). **Tested end-to-end** in a temp repo (S1 work →
  stub; S2 commit log; S3 work → *suppress*, not a 2nd stub) + the threshold/comparison in isolation (5m/90m
  → suppress; 3h/none → stub); BSD `date -v` with GNU `date -d` fallback. Lockstep: `.githooks/post-commit`,
  `.githooks/README.md`, `docs/DESIGN-ritual-triggers.md`, `VERSION`→4.22.1, `CHANGELOG`, `README` (table +1/−1),
  `UPGRADE` (row + `4.22.0→4.22.1` rung). First post-release patch under the *one version per release*
  policy (4.22.0 was pushed). → serves: vision-agent-memory (the decay model's integrity depends on a
  session-file count that tracks *sessions*, not commits) (`post-commit-per-session-v4221`).
  <!-- id: post-commit-per-session-v4221 | created: 2026-06-28 | last_used: 2026-06-28 | uses: 3 | tier: archive-candidate | origin: 2026-06-28-022903 -->

- [x] **Shipped in v4.22.0 (MINOR; dev-iter 4.22) — curious knowledge harvest at enable.** From a **client-team
  enablement complaint** (another team, first run on their repo): discovery "was less curious than
  expected" — a canonical `docs/` folder was **skipped entirely**; when re-asked to recursively analyze
  it, the agent grabbed only the folder's **top-level** files (not subfolders); and a root-level markdown
  **kanban board + decision log** were missed. Root cause: `ENABLE.md` **Step 4** was a *classifier*
  (read a fixed manifest list; "Structure signals" looked only at **top-level** folder names) with **no
  knowledge-harvest** of the team's own docs. **Fix:** added **Step 4b — Harvest existing project
  knowledge (be curious)**: recursively descend every doc tree (`docs/`/`doc/`/`wiki/`/`rfcs/`/`adr/`/…,
  *all* subfolders) + sweep repo/module roots for human-authored knowledge markdown (decision logs, ADRs,
  kanban/roadmap/TODO, architecture/design, CONTRIBUTING, RFCs) by location and name; **read within a
  budget (~40 files/~400 KB, prioritized root→docs→recent) and disclose overflow as a
  `(knowledge-harvest)` Open Thread** so nothing vanishes silently; **distill, don't transcribe**
  (map-don't-mirror into instructions/Invariants/Open Threads/smoke-test/vision; conflicts → a
  `Contradiction:` thread). Wired into seeding 5a/5f/5g and a Step 8 verify check. **Operator-side only**
  (`ENABLE.md`) — **no installed-file shape change, no template re-sync, no adapter sync**; the
  `4.21.0→4.22.0` rung is a human-gated **optional re-harvest** to backfill a repo enabled by the older
  shallow scan (additive, never overwrites curated facts). Lockstep: `ENABLE.md` (Step 4 + 4b + 5a/5f/5g
  + Step 8), `VERSION`→4.22.0, `UPGRADE.md` (table rows for 4.21.0 *and* 4.22.0 — the 4.21.0 row was
  missing — plus the new rung). `memory-lint` OK (0 errors). Scoping (harvest breadth + bounding)
  confirmed with the maintainer before authoring. → serves: vision-agent-memory (a memory layer should
  inherit what the team already knows; curiosity is part of faithful enablement). Complaints = adoption
  signal.
  <!-- id: knowledge-harvest-curious-v4220 | created: 2026-06-27 | last_used: 2026-06-28 | uses: 3 | tier: archive-candidate | origin: 2026-06-27-210953 -->

- [x] **Shipped v4.20.0 (MINOR) — first-run init for fresh clones.** Dogfooding `~/sandbox/simple-proxy`
  with Copilot (fresh clone) exposed the gap: the **memory bootstrap self-initializes** (Copilot read
  AGENTS.md/memory on `start` — "start from AGENTS.md" was unnecessary), but a clone has the **gitignored
  skill adapters absent** and the **git hook unactivated** (`core.hooksPath` is local config; git can't
  auto-run committed hooks on clone). So the user had to run `sync skill adapters` **and** (easily missed)
  activate the hook — two manual steps, contra the zero-manual/untrained-user constraint. **Fix:**
  `.githooks/init.sh` (one idempotent command — regenerate adapters + `git config core.hooksPath .githooks`;
  not a git-hook name so never auto-run) + an `AGENTS.md` **self-init** note (the agent runs it on its first
  session, since Copilot already reads AGENTS.md on `start`). One agent step (or one human command) instead
  of two; CI stays the zero-config floor. Lockstep: `.githooks/init.sh` + `README.md`, `AGENTS.md` (root +
  template), `docs/DESIGN-ritual-triggers.md`, `UPGRADE.md` (rung + table), `README`, `CHANGELOG`,
  `VERSION`→4.20.0. Dogfooded: init.sh on the tool; pushed to both repos. **Strong validation in the same
  dogfood:** Copilot praised the separation of concerns, idempotent sync, "executable documentation", and
  resiliency — "highly robust, deterministic, and easy to reason about." → serves: vision-agent-memory
  (untrained-user adoption — a fresh clone self-initializes with no manual ritual)
  **v4.20.1 follow-up (fresh-clone re-test, 2026-06-24):** self-init worked for **Claude Code** (it
  checked `core.hooksPath`, ran `init.sh` proactively → hook active + adapters synced) but **NOT Copilot
  CLI** (its `start` front-loads `copilot-instructions.md` + summarizes; skipped the AGENTS.md self-init →
  hook inactive + adapters absent). The v4.20.0 "Copilot reads AGENTS.md on start" assumption was
  optimistic. **Fix (4.20.1):** folded the first-run init into the **top of `copilot-instructions.md`**
  (the file Copilot reliably front-loads). Honest: still prompt-adherence (non-deterministic) —
  `bash .githooks/init.sh` is the one-command fallback, CI the floor.
  **VALIDATED 2026-06-24 (fresh re-clone, Copilot CLI / Gemini):** the 4.20.1 fix works — Copilot
  **self-inited**, running `.githooks/init.sh` as its first step ("explicit and straightforward") before
  summarizing. So a fresh clone now self-initializes with **zero manual steps on both Claude and Copilot**
  — the untrained-user / fresh-clone goal is met cross-vendor. Closes the Copilot arc (v4.17.0 → 4.20.1).
  <!-- id: ritual-init-v4200 | created: 2026-06-24 | last_used: 2026-06-28 | uses: 7 | tier: archive-candidate | origin: 2026-06-24-193329 -->

### Evolving long-term memory layer (v3.0.0) — BUILT 2026-06-13
- [ ] **Dogfood backfill (optional):** this repo adopted the layer — added
  Architectural Invariants (core), `memory/decay-policy.md`, `memory/archive/INDEX.md`,
  `last_review`, and Memory References in session logs going forward. Legacy facts in
  What's Been Built / Key Decisions are grandfathered as `active` (no metadata footers
  yet); backfill them with ids/metadata if/when desired (or let the first review do it).
- [ ] Optionally update `examples/` to mention the mercury upgrade as a real Mode B
  upgrade fixture (analogous to rust-event-bus being a real Mode A).

### Next major iteration — Vision → Blueprint → Design → Implementation (VBDI) lifecycle
> Set 2026-06-14. The vNext backlog (P1–P5) is complete; this is the next headline direction.
> Paused at the framing stage by mutual agreement — to be tackled methodically next.

- [ ] **Build a VBDI lifecycle layer** — *forward*-looking intent traceability to complement
  the *backward*-looking memory layer. Mission: empower AI to deliver **predictable
  innovation** with human partnership — a deterministic *process* + an enforceable *trace*
  from intent → delivery, with a human gate at each altitude change (Vision → Blueprint →
  Design → Implementation). "Predictable" = the process/trace, not the ideas. Reuses
  existing primitives: id/origin/supersedes linkage (trace across altitudes), §10
  contradiction-check (drift detection: impl vs design, design vs blueprint vs vision),
  §9 supersession (intent changes ripple down), the human-gate pattern
  (never-pick-a-winner / invariant-verify prompt), and the smoke test (acceptance vs
  design criteria). Stays no-code/markdown + deterministic. **Plan:** dogfood it — write
  the Vision (human's to set), then `DESIGN-vbdi-lifecycle.md` (sibling to
  `DESIGN-evolving-memory.md`), settle forks via structured decisions, build on the
  version ladder. **Hard parts:** drift across altitudes needs real structure (not
  hand-waving); keep gates lightweight (Open-Thread-like, not Jira); the trace must be
  enforceable (grep/review), not just documented. Validated motivation: the Node→Rust
  rewrite delivered deterministically with no drift — VBDI generalizes that to creation.
  <!-- id: vbdi-lifecycle-direction | created: 2026-06-14 | last_used: 2026-06-20 | uses: 4 | tier: active | origin: 2026-06-14-030729 -->

### Shipped — v4.1.0: cross-vendor skills layer (2026-06-15)

> _v4.2.0 ("sync skill adapters", `sync-adapters-v420`) archived faded → `archive/2026-Q2.md` (2026-06-18 review)._

### Shipped — v4.4.0 / v4.5.0 + the hello-world dogfood (reactivated 2026-06-18)

> Reactivated from `archive/2026-Q2.md` 2026-06-18 — the 2026-06-18-051933 review (GitHub Copilot)
> swept these while they were still referenced in the window (low sslu); restored to `active`.

### Shipped — v4.7.0–v4.7.1: cross-vendor refinements (2026-06-17)

### Blueprint — gaps from Current State (v4.10.0) to the Vision  (serves: vision-agent-memory)
> Derived 2026-06-15 from `memory/vision.md` (maintainer-confirmed). Typed Open Threads
> `(blueprint)`: each is a Vision↔reality gap that closes when delivered. The *backward*
> memory layer is not here — it's done; every gap is *forward*. These operationalize the
> `vbdi-lifecycle-direction` thread above. First real VBDI loop, dogfooded on the tool itself.

- [ ] **(blueprint)** Greenfield path — the tool handles brownfield (enable/migrate) well
  but has no "start from a Vision, no code yet" flow. → serves: vision-agent-memory
  <!-- id: bp-greenfield | created: 2026-06-15 | last_used: 2026-06-15 | uses: 1 | tier: active | origin: 2026-06-15-000531 -->
- [ ] **(blueprint)** Multi-user concurrent contribution — mostly supported (shared
  committed `memory/`, multi-agent continuity, collision-safe session filenames); validate
  and harden for *simultaneous* contributors. → serves: vision-agent-memory
  <!-- id: bp-multi-user | created: 2026-06-15 | last_used: 2026-06-17 | uses: 4 | tier: active | origin: 2026-06-15-000531 -->
- [ ] **(blueprint)** *(optional)* SDLC overlay for targets — a scrum-inspired profile a
  target *owner* can opt into: a `(sprint)` tag over Blueprint gaps + a sprint-boundary
  review, **no points/velocity/ceremony**. Not core; only if a real target wants it. The
  memory design is already **process-neutral** and survives an overlay (`DECAY.md` §12 /
  `docs/DESIGN-vbdi-lifecycle.md` §13): ceremony + scoring live in the target's own space,
  never in `memory/`. → serves: vision-agent-memory
  <!-- id: bp-sdlc-overlay | created: 2026-06-15 | last_used: 2026-06-15 | uses: 1 | tier: active | origin: 2026-06-15-010142 -->
- [x] **(blueprint — SHIPPED v4.29.0 MINOR, 2026-07-12)** Before-session context *presence* — the read chain (`CLAUDE.md` →
  `AGENTS.md` → `memory/*`) is advisory prose; the v4.19.0 trigger layer reinforces only the
  *after*-session rituals (its substrate — git + CI — has no session-start moment), so the
  before-session read rests on prompt adherence, the same non-determinism v4.20.1 recorded for
  Copilot self-init. **Field-proven gap** (child-repo report, 2026-07-11: reads skipped under
  task pressure → skill-unawareness, off-model engagement, rework; patched locally with a
  SessionStart injection + attestation canary and recommended upstreaming). **Agreed upstream
  shape:** (a) native `@`-imports in `templates/CLAUDE.md` + `templates/GEMINI.md`
  (`@AGENTS.md`, `@memory/instructions.md`, `@memory/continuity.md`, `@memory/vision.md`) —
  markdown-only, presence becomes structural on import-capable runtimes; imports stay in the
  per-vendor bootstrap files, `AGENTS.md` stays vendor-neutral; (b) an **opt-in** Claude Code
  `SessionStart` injection recipe in `docs/optional-ritual-hook.md` (tool-only; never installed
  by default — a committed `.claude/settings.json` conflicts with the installed `.gitignore`
  and leaks personal allowlists); (c) the attestation canary/oracle stays **downstream**
  (per-repo, Claude-specific). Honest limits: imports can't cover `memory/sessions/` (dynamic
  paths); Cursor/Windsurf/Copilot keep prose pointers (Copilot's mitigation is the v4.20.1
  front-load pattern); imported files enter context every session, so the continuity-bloat
  controls (v4.24.0/4.28.2/4.28.3) become load-bearing. **Shipped 2026-07-12 as v4.29.0**:
  root + template `CLAUDE.md`/`GEMINI.md` imports (Gemini in its `@./` form, `.md`-only),
  optional-hook doc "Option A0" (+ retitle), full lockstep (VERSION/CHANGELOG/README/UPGRADE
  row + `4.28.4→4.29.0` rung; site changelog auto-includes). Import syntax verified against
  both vendors' current docs before shipping. → serves: vision-agent-memory
  (the memory layer is *present* every session, not contingent on the agent choosing to read)
  <!-- id: bp-before-session-presence | created: 2026-07-12 | last_used: 2026-07-12 | uses: 1 | tier: working | origin: 2026-07-12-013817 -->

### Backlog — vNext (temporal & supersession) + beyond
> From the 2026-06-13 industry-alignment assessment:
> `docs/assessments/2026-06-13-industry-alignment.md`. Verdict: on track; distinctive
> on event-sourcing/determinism/governance; one real gap = temporal/supersession.
> Re-run the assessment after meaningful iterations and compare its scorecard.

- [ ] **Dogfooding on real work (ongoing).** Already delivering: the simple-proxy
  enable surfaced v3.1.0 (`.gitignore`), and the simple-proxy Node→Rust refactor's
  field report drove v3.2.0 (protocol clarifications). Keep feeding real-work insights
  back into this backlog. (Stated 2026-06-13.)
  <!-- id: backlog-real-work-dogfood | created: 2026-06-13 | last_used: 2026-06-24 | uses: 11 | tier: active -->

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
- [x] **Publish to GitHub — DONE 2026-06-18.** Migrated GitLab → **public GitHub** at
  `git@github.com:acn-ericlaw/agent-memory.git` (Apache-2.0; **release-candidate** status; full
  73-commit history mirrored). The repo + working dir are now **`agent-memory`** (dropped the
  `-tool` suffix — the canonical name everywhere already). GitLab
  (`git@gitlab.com:ericclaw/agent-memory-tool.git`) is being **retired**. The
  `no-company-references-until-publication-approved` gate is satisfied — company protocol followed,
  maintainer approved public publication. **`origin` is now GitHub; assume GitHub for git ops.**
- [ ] **Remaining: migrate to enterprise GitHub** for the official repo (one more hop after this
  public-GitHub staging step). (Set 2026-06-18.)
- [ ] Keep root `CLAUDE.md` architecture section in sync when file shapes or
  vendor support change (also touches `templates/`, `MIGRATE.md`, `README.md`,
  `examples/`)

## User Preferences

- Never expose the user's absolute home path (`/Users/<name>/…`) in file content —
  use `~`-relative paths. (Stated 2026-06-12; now enforced in ENABLE.md Step 5b +
  schema `repo:` guidance.)
