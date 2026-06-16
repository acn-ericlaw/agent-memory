# Continuity — agent-memory

> Shared ground truth for this tool's own development state.

---

## Project State

- **project:** agent-memory
- **status:** v4.1.1 — backward memory layer (v3.x) + forward cognitive layer (VBDI, v4.0.0) + **cross-vendor skills layer (v4.1.0, refined v4.1.1)**: neutral committed `agent-skills/` + AGENTS.md baseline + Claude/Gemini/Cursor adapters; migration promotes vendor `.claude/skills/`. v4.1.1 = folder finalized as `agent-skills/` (collision-safe) + Cursor adapter `globs` fix + collision guard + vendor-dir double-duty clarified. Not yet validated on a real target (client run pending).
- **last_enabled:** 2026-06-12
- **last_session:** 2026-06-16 | agent: Claude Code (2026-06-16-001342)
- **last_review:** 2026-06-15 | through 2026-06-15-231502
- **last_invariant_check:** 2026-06-15 | through 2026-06-15-231502
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

- Target-repo scope only — never read/modify/move anything outside the resolved
  target-repo root (never `~`, `~/.claude/`, Application Support, AppData, system paths)
  <!-- id: target-repo-scope-only | created: 2026-06-13 | last_used: 2026-06-15 | uses: 4 | tier: core -->
- Never delete vendor files — move originals to `legacy/<vendor>/`, preserving paths
  <!-- id: never-delete-vendor-files | created: 2026-06-13 | last_used: 2026-06-15 | uses: 2 | tier: core -->
- Never overwrite, never pick a winner — fold vendor steering under
  `## Migrated rules from <vendor>`; surface contradictions as Open Threads
  <!-- id: never-pick-a-winner | created: 2026-06-13 | last_used: 2026-06-15 | uses: 4 | tier: core -->
- No-code, markdown-only — the files are the product; the agent is the runtime
  <!-- id: no-code-markdown-only | created: 2026-06-13 | last_used: 2026-06-15 | uses: 15 | tier: core -->
- Upgrades are additive and non-destructive — enrich and add, never rewrite or delete
  <!-- id: upgrades-additive | created: 2026-06-13 | last_used: 2026-06-15 | uses: 12 | tier: core -->

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

- [ ] Re-verify invariants (due): confirm target-repo-scope-only, never-delete-vendor-files, never-pick-a-winner, no-code-markdown-only, upgrades-additive and the Vision (vision-agent-memory) still hold, or supersede any that don't (DECAY.md §9)
  <!-- id: ot-reverify-invariants-20260615 | created: 2026-06-15 | last_used: 2026-06-15 | uses: 1 | tier: working | origin: 2026-06-15-231502 -->
- [x] Drift: Blueprint subsection header was stale ("Current State (v3.7.0)"). **Resolved
  2026-06-16** — refreshed the baseline label to v4.1.1 (current state); the gap set itself
  is still valid (bp-greenfield, bp-multi-user, bp-sdlc-overlay remain open).
  <!-- id: ot-drift-blueprint-baseline-20260615 | created: 2026-06-15 | last_used: 2026-06-15 | uses: 1 | tier: working | origin: 2026-06-15-231502 -->

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
  <!-- id: gitignore-propagation-v310 | created: 2026-06-13 | last_used: 2026-06-15 | uses: 3 | tier: active -->
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
  <!-- id: gitignore-v310-mercury-validation | created: 2026-06-13 | last_used: 2026-06-13 | uses: 1 | tier: archive-candidate -->

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
  <!-- id: field-report-v320 | created: 2026-06-13 | last_used: 2026-06-13 | uses: 1 | tier: archive-candidate -->

### Shipped — v3.3.0: supersession / fact-invalidation (2026-06-14)
- [x] **P1 (supersession) shipped.** The evolving-memory layer can now represent a fact
  becoming *false*, not just unused: a terminal `superseded` tier + optional
  `superseded-by`/`supersedes` footer fields. The agent marks a reversed/invalidated
  fact `superseded` immediately (a truth-state edit it owns) and records
  `Superseded: old → new` in the session log; the review archives it flagged
  "superseded" (not "faded"), terminal (never reactivated). Touched `DECAY.md` (§9 +
  tier + rule), `REVIEW.md`, `.agent/schema.md`, both `AGENTS.md`, the
  `evolving-memory-example/` (a worked REST-versioning supersession), `VERSION`→3.3.0,
  `UPGRADE.md` 3.2.0→3.3.0 rung + tables, `README`/`CHANGELOG`. Flipped the
  industry-alignment assessment's gap #1 ⬜→✅ — the one "High" gap closed.
  <!-- id: supersession-v330 | created: 2026-06-14 | last_used: 2026-06-14 | uses: 3 | tier: archive-candidate -->
- [x] **P2 (invariant-verification cadence) shipped as v3.4.0.** Never-decay facts
  (`core` / Architectural Invariants) can quietly go "confidently wrong"; the review now
  prompts a human to re-confirm them. Added `verify_invariants_every` (default 20) to
  `decay-policy.md` and a `last_invariant_check` tracker to continuity Project State;
  `REVIEW.md` step 6 raises **one** Open Thread to confirm-or-supersede when due (never
  auto-invalidates) + a summary line; `DECAY.md` §6 note; `.agent/schema.md`; worked
  example shows a first invariant prompt. `VERSION`→3.4.0, `UPGRADE.md` 3.3.0→3.4.0 rung
  + tables, `README`/`CHANGELOG`. Assessment gap #2 ⬜→✅. Pairs with v3.3.0: P1 retires
  a fact you *notice* is false; P2 makes you *check*.
  <!-- id: invariant-verify-v340 | created: 2026-06-14 | last_used: 2026-06-14 | uses: 2 | tier: archive-candidate -->
- [x] **P3 (write-time contradiction check) shipped as v3.5.0.** Generalized the
  migration-time "surface contradictions, never pick a winner" rule to normal sessions:
  `DECAY.md` §10 — on adding/rewriting a fact, scan `core`/invariants + active decisions
  in the same area; a clear replacement → supersede (§9), a genuine conflict →
  `Contradiction:` Open Thread, a clash with a `core` invariant → stop and surface.
  Added a review contradiction-backstop (`REVIEW.md`) and the before-adding check in
  both `AGENTS.md`. `VERSION`→3.5.0, `UPGRADE.md` 3.4.0→3.5.0 rung + tables,
  `README`/`CHANGELOG`; assessment gap #3 ⬜→✅ and Truth-maintenance scorecard ◐→✅.
  Completes the truth-maintenance trio: P3 catches a conflict at write time, P1
  resolves it (supersede) or P3 raises a thread, P2 re-checks invariants periodically.
  <!-- id: contradiction-check-v350 | created: 2026-06-14 | last_used: 2026-06-14 | uses: 1 | tier: archive-candidate -->
- [x] **P4 (memory smoke test) shipped as v3.6.0.** A cheap, no-code answer to the
  "evaluation is unsolved" gap: `memory/smoke-test.md` — N questions (generic orientation
  + project-specific, seeded at enable) a *fresh* agent should answer from `memory/`
  alone; a ❌ is a memory gap to fill. New `templates/memory/smoke-test.md`; `ENABLE.md`
  step 5f generates it (+ Step 8 verify, Step 9 report); `.agent/schema.md` documents it;
  `REVIEW.md` notes running it at a review. This repo's own `memory/smoke-test.md`
  created (dogfood, not yet run). `VERSION`→3.6.0, `UPGRADE.md` 3.5.0→3.6.0 rung + tables,
  `README`/`CHANGELOG`; assessment gap #5 + Evaluation scorecard ⬜→✅.
  <!-- id: memory-smoke-test-v360 | created: 2026-06-14 | last_used: 2026-06-14 | uses: 1 | tier: active -->
- [x] **P5 (provenance + retrieval-at-scale) shipped as v3.7.0 — completes the vNext
  backlog.** Event-sourcing already records a fact's source session; v3.7.0 *surfaces* it
  as an optional `origin: <session-file>` footer (set at creation, repairable by review).
  `DECAY.md` §11 also documents retrieval as deliberately lexical + indexed (grep +
  `archive/INDEX.md` + `origin` pointers); vector/semantic retrieval stays out of scope
  (would break no-code). Touched `DECAY.md` (§1 row + §11), `REVIEW.md`, `.agent/schema.md`,
  both `AGENTS.md`, `ENABLE.md`, the worked example (origin on session-created facts),
  `VERSION`→3.7.0, `UPGRADE.md` 3.6.0→3.7.0 rung + tables, `README`/`CHANGELOG`. Assessment
  gap #6 ⬜→✅; gap #4 (lexical retrieval) ◐ by-design (semantic out of scope).
  <!-- id: provenance-retrieval-v370 | created: 2026-06-14 | last_used: 2026-06-14 | uses: 2 | tier: active | origin: 2026-06-14-024407 -->

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
  <!-- id: vbdi-lifecycle-direction | created: 2026-06-14 | last_used: 2026-06-15 | uses: 3 | tier: active | origin: 2026-06-14-030729 -->

### Shipped — v4.0.0: the forward layer (VBDI) (2026-06-15)
- [x] **VBDI forward layer shipped.** The cognitive loop (Current State → Vision →
  Blueprint → Design → Implementation → Feedback) now lives in the protocol: new
  `templates/memory/vision.md`; Blueprint = typed `(blueprint)` Open Threads; altitude
  trace (`serves:` / `id`); `DECAY.md` §12 + §10 altitude-drift; `REVIEW.md` (Vision in
  invariant-verify + drift backstop); `.agent/schema.md`; both `AGENTS.md` (cognitive-loop
  section + Vision in the read-list); `ENABLE.md` Step 5g (+ verify + report).
  **Bootstrap:** enable/upgrade create a ⚠️ DRAFT Vision (current-state context only; the
  target is left to the human) + a `(vision-bootstrap)` gate — never fabricated.
  `VERSION`→4.0.0 (new-layer milestone; additive); `UPGRADE.md` 3.7.0→4.0.0 rung + version
  tables; `README`/`CHANGELOG`. **Vendor-neutrality fix** (maintainer caught it in review):
  root `CLAUDE.md` thinned to a pointer like `GEMINI.md`; its project guide + architecture
  map moved to vendor-neutral `memory/instructions.md` — the architecture had been
  Claude-only, a drift from the vendor-neutral Vision. **Follow-on (2026-06-15):**
  standardized all 10 bootstrap pointers (root + templates) to one minimal parallel form —
  the read-order now lives **only in `AGENTS.md`** (DRY), which also retroactively fixed the
  v4.0.0 `vision.md` miss in the template pointers. Closes `bp-vbdi-loop` + `bp-altitude-drift`.
  Decisions locked with the maintainer: **4.0.0** + **context-only bootstrap**.
  <!-- id: vbdi-shipped-v400 | created: 2026-06-15 | last_used: 2026-06-15 | uses: 4 | tier: active | origin: 2026-06-15-002837 -->

### Shipped — v4.1.0: cross-vendor skills layer (2026-06-15)
- [x] **Skills layer shipped (additive MINOR).** The shared layer's third leg —
  *capabilities* — beside memory and steering. Neutral, committed `agent-skills/<name>/SKILL.md`
  (name + when-to-use description + procedure + optional scripts); `AGENTS.md` "Skills"
  section is the universal agent-as-runtime baseline; native adapters regenerated for
  Claude (`.claude/skills/`), Gemini (`.gemini/commands/`), Cursor (`.cursor/rules/`) —
  thin, gitignored, **Option A** (only `agent-skills/` committed). Migration **promotes** vendor
  `.claude/skills/` into `agent-skills/` (preserve original under `legacy/`, never flatten into
  steering). Maintainer chose all-vendor adapter scope at build. Touched: `ENABLE.md`
  (Step 5h + verify/report/scope), `MIGRATE.md` (principle 6 + Section B2 + Claude protocol
  + detection table + continuity note), `AGENTS.md` (root + template), `.agent/schema.md`,
  `templates/.gitignore` (comment), `VERSION`→4.1.0, `UPGRADE.md` 4.0.0→4.1.0 rung + table,
  `README`/`CHANGELOG`. `DECAY.md`/`REVIEW.md` unchanged. Design: `docs/DESIGN-skills-layer.md`.
  Realizes `bp-skills-layer`. Not yet validated on a real target (next: upgrade the client).
  <!-- id: skills-layer-v410 | created: 2026-06-15 | last_used: 2026-06-15 | uses: 1 | tier: working | origin: 2026-06-15-234801 -->

### Shipped — v4.1.1: skills-layer refinements (2026-06-16)
- [x] **Skills layer refined (PATCH)** — pre-adoption corrections before the first real
  target run (the client Mode B tonight): (1) **folder renamed `skills/` → `agent-skills/`**
  (collision-safe — `skills/` is too common a top-level dir); (2) **Cursor adapter fix** —
  `.cursor/rules/*.mdc` now emits the "agent-requested" type (`description` + empty `globs:`
  + `alwaysApply: false`), verified against current Cursor docs (Gemini `.toml` + Claude
  formats verified correct as-is); (3) **collision guard** — never overwrite a pre-existing
  `agent-skills/`, surface a Contradiction thread; (4) **vendor-dir double-duty clarified**
  in MIGRATE.md (archive originals to `legacy/` first, then generate adapters). `VERSION`→
  4.1.1; `UPGRADE.md` 4.1.0→4.1.1 rung + table; `README`/`CHANGELOG`; all living docs
  renamed (perl, `.claude/skills/` preserved). v4.1.0 was same-day + unconsumed → a
  pre-adoption correction, not a breaking change. Closes the (a)+(b) follow-ups to
  `skills-layer-v410`.
  <!-- id: skills-layer-v411-fixes | created: 2026-06-16 | last_used: 2026-06-16 | uses: 1 | tier: working | origin: 2026-06-16-001342 -->

### Blueprint — gaps from Current State (v4.1.1) to the Vision  (serves: vision-agent-memory)
> Derived 2026-06-15 from `memory/vision.md` (maintainer-confirmed). Typed Open Threads
> `(blueprint)`: each is a Vision↔reality gap that closes when delivered. The *backward*
> memory layer is not here — it's done; every gap is *forward*. These operationalize the
> `vbdi-lifecycle-direction` thread above. First real VBDI loop, dogfooded on the tool itself.

- [x] **(blueprint)** Build the forward cognitive loop (VBDI) — **SHIPPED v4.0.0**: the Blueprint mechanism,
  the altitude trace (id-linkage Implementation→Design→Blueprint→Vision), drift-detection,
  and human gates. Design drafted: `docs/DESIGN-vbdi-lifecycle.md`. → serves: vision-agent-memory
  <!-- id: bp-vbdi-loop | created: 2026-06-15 | last_used: 2026-06-15 | uses: 2 | tier: active | origin: 2026-06-15-000531 -->
- [ ] **(blueprint)** Greenfield path — the tool handles brownfield (enable/migrate) well
  but has no "start from a Vision, no code yet" flow. → serves: vision-agent-memory
  <!-- id: bp-greenfield | created: 2026-06-15 | last_used: 2026-06-15 | uses: 1 | tier: active | origin: 2026-06-15-000531 -->
- [x] **(blueprint)** Altitude drift-detection — **SHIPPED v4.0.0**: extend the §10 contradiction-check across
  Vision ↔ Blueprint ↔ Design ↔ Implementation. → serves: vision-agent-memory
  <!-- id: bp-altitude-drift | created: 2026-06-15 | last_used: 2026-06-15 | uses: 2 | tier: active | origin: 2026-06-15-000531 -->
- [ ] **(blueprint)** Multi-user concurrent contribution — mostly supported (shared
  committed `memory/`, multi-agent continuity, collision-safe session filenames); validate
  and harden for *simultaneous* contributors. → serves: vision-agent-memory
  <!-- id: bp-multi-user | created: 2026-06-15 | last_used: 2026-06-15 | uses: 1 | tier: active | origin: 2026-06-15-000531 -->
- [ ] **(blueprint)** *(optional)* SDLC overlay for targets — a scrum-inspired profile a
  target *owner* can opt into: a `(sprint)` tag over Blueprint gaps + a sprint-boundary
  review, **no points/velocity/ceremony**. Not core; only if a real target wants it. The
  memory design is already **process-neutral** and survives an overlay (`DECAY.md` §12 /
  `docs/DESIGN-vbdi-lifecycle.md` §13): ceremony + scoring live in the target's own space,
  never in `memory/`. → serves: vision-agent-memory
  <!-- id: bp-sdlc-overlay | created: 2026-06-15 | last_used: 2026-06-15 | uses: 1 | tier: active | origin: 2026-06-15-010142 -->
- [x] **(blueprint)** Cross-vendor skills layer — **SHIPPED v4.1.0** (2026-06-15). Neutral
  committed `agent-skills/<name>/SKILL.md` source of truth + an `AGENTS.md` "Skills" baseline
  (agent-as-runtime) + regenerated Claude/Gemini/Cursor adapters (gitignored — **Option A**,
  all-vendor scope chosen at build). Migration promotes `.claude/skills/` into `agent-skills/`
  (preserve under `legacy/`, don't flatten). Design: `docs/DESIGN-skills-layer.md`. Realized
  by `skills-layer-v410`. → serves: vision-agent-memory
  <!-- id: bp-skills-layer | created: 2026-06-15 | last_used: 2026-06-15 | uses: 1 | tier: active | origin: 2026-06-15-231502 -->
- [x] **Review artifacts authored (2026-06-15)** for peer / leadership review:
  `docs/agent-memory-whitepaper.md` (technical paper) + `docs/agent-memory-deck.html`
  (self-contained HTML deck, ~13 slides, keyboard/click nav). Built on the reference ACF
  framework (`docs/agent-cognitive-framework.md`), articulating the integrated v4.0.0
  (memory substrate + VBDI loop). **Company-neutral** per the personal-research rule —
  add organizational framing at presentation time, not in the repo.
  <!-- id: review-artifacts-v400 | created: 2026-06-15 | last_used: 2026-06-15 | uses: 1 | tier: active | origin: 2026-06-15-012034 -->

### First real-work dogfood — enabled `~/sandbox/simple-proxy` (Mode A, 2026-06-13)
- [x] **Real Mode A fresh enable** of a zero-dep Node.js TCP-proxy CLI (no prior AI
  footprint). 15 files generated, source untouched, verified. Logged 7 refactor Open
  Threads in the target's continuity (package.json `main` points at a non-existent
  file; stale README `moment`/`source_port` references; ES5 modernization; duplicate
  code across the two entry points; per-connection signal handlers; no tests). This
  enable is what surfaced the `.gitignore` gap above. Target later stamped 3.1.0.
  Refactor of the target is the user's planned next step.
  <!-- id: dogfood-simple-proxy-enable | created: 2026-06-13 | last_used: 2026-06-13 | uses: 2 | tier: archive-candidate -->
- [x] **Design validated: enabled target repos are self-contained.** The user chose to
  run the simple-proxy refactor in a *separate* Claude Code session launched inside the
  target — driven by simple-proxy's own `CLAUDE.md`→`AGENTS.md`→`memory/`, needing no
  knowledge of this tool. Confirms the two-layer model: the tool's job ends at
  enablement; the enabled repo then stands on its own. Baselines committed cleanly
  (simple-proxy: source import + AI-enable; mercury: v3.1.0 upgrade) so the new
  sessions start from committed state. (2026-06-13)
  <!-- id: dogfood-target-repo-self-contained | created: 2026-06-13 | last_used: 2026-06-14 | uses: 2 | tier: active -->

### Backlog — vNext (temporal & supersession) + beyond
> From the 2026-06-13 industry-alignment assessment:
> `docs/assessments/2026-06-13-industry-alignment.md`. Verdict: on track; distinctive
> on event-sourcing/determinism/governance; one real gap = temporal/supersession.
> Re-run the assessment after meaningful iterations and compare its scorecard.

- [x] **P1 — Supersession / fact-invalidation semantics — SHIPPED v3.3.0** (see Shipped section above). On a reversed decision,
  tombstone the old fact (`superseded-by: <id>`; new fact `supersedes: <id>`) and
  archive it flagged "superseded", not "faded". Markdown-native `expired_at`/`invalid_at`
  (cf. Zep); closes assessment gaps #1+#2; buys the "knowledge updates" ability.
  Touches DECAY.md, REVIEW.md, schema, examples. Highest-value next step.
  <!-- id: backlog-supersession | created: 2026-06-13 | last_used: 2026-06-14 | uses: 2 | tier: archive-candidate -->
- [x] **P2 — Invariant-verification cadence — SHIPPED v3.4.0** (see Shipped section above). Add `verify_invariants_every: N`
  to decay-policy.md; review prompts a human to confirm `core`/Architectural Invariants
  are still true (never-decay ≠ never-checked).
  <!-- id: backlog-invariant-verify-cadence | created: 2026-06-13 | last_used: 2026-06-14 | uses: 2 | tier: archive-candidate -->
- [x] **P3 — Write-time contradiction flag — SHIPPED v3.5.0** (see Shipped section above). Extend the migration-time contradiction
  check into REVIEW.md: when a fact is added, scan for one it contradicts → raise an
  Open Thread (SSGM "pre-consolidation validation", scaled down).
  <!-- id: backlog-contradiction-check | created: 2026-06-13 | last_used: 2026-06-14 | uses: 2 | tier: archive-candidate -->
- [x] **P4 — Minimal memory eval — SHIPPED v3.6.0** (see Shipped section above). `memory-smoke-test.md`: N questions a fresh agent
  should answer from memory alone. Manual, but app-level eval is unsolved industry-wide.
  <!-- id: backlog-memory-eval | created: 2026-06-13 | last_used: 2026-06-14 | uses: 2 | tier: active -->
- [x] **P5 — Provenance surfacing + retrieval-at-scale — SHIPPED v3.7.0** (see Shipped section above). Surface each fact's originating
  session; lean on archive/INDEX.md (+ optional sessions/INDEX.md) as the no-code
  mitigation if memory grows large. Full vector/semantic retrieval stays out of scope.
  <!-- id: backlog-provenance-retrieval | created: 2026-06-13 | last_used: 2026-06-14 | uses: 2 | tier: active -->
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

## User Preferences

- Never expose the user's absolute home path (`/Users/<name>/…`) in file content —
  use `~`-relative paths. (Stated 2026-06-12; now enforced in ENABLE.md Step 5b +
  schema `repo:` guidance.)
