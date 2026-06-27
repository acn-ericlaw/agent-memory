# Continuity — agent-memory

> Shared ground truth for this tool's own development state.

---

## Project State

- **project:** agent-memory
- **status:** v4.22.0 — a vendor-neutral, no-code (markdown) shared-AI-memory + AI-enablement tool. Three shared layers: **backward memory** (v3.x — fact metadata + ids, decay/review/archive), a **forward VBDI cognitive loop** (v4.0 — Vision→Blueprint→Design→Impl over the memory substrate), and a **cross-vendor skills layer** (v4.1+ — neutral committed `agent-skills/` + a runnable `sync-adapters`; six adapter targets: Claude/Gemini/Cursor/Kiro/Copilot/Antigravity). Agent-as-runtime; `memory/` is committed + shared. Built-in skills: `memory-lint`, `second-opinion`+`apply-critique`, `sync-adapters`. Vendor-neutral ritual triggers (committed git hook + CI floor) with first-run self-init; Windows LF hardening. **Per-version history lives in `UPGRADE.md` (the version ladder) + `memory/sessions/` — kept OUT of this line by design (v4.22.0): `status` is a short current-state descriptor, not a changelog, so this shared line doesn't become a merge-conflict hotspot.** `.agent/version.md` is the canonical version. Validated across six vendors (Claude, Gemini, Cursor, Kiro, Copilot CLI, Antigravity).
- **last_enabled:** 2026-06-12
- **last_session:** 2026-06-27 | agent: Claude Code (2026-06-27-224339)
- **last_review:** 2026-06-27 | through 2026-06-27-215825
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
  `sync-adapters`), which are re-copied (overwritten) on upgrade; that overwrite is scoped to those tool-owned files,
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

- [x] **Applied a fresh-context critique (second-opinion → apply-critique) to the v4.22.0 work — 4 fixes,
  all folded into the unreleased v4.22.0 (no version bump, per the one-version-per-release policy).** A
  clean-context reviewer (different vendor, via `review-scratch/`) challenged the milestone; 3 of 4 items
  were real and applied, 1 validated-no-change: **(1) version consolidation — reviewer agreed, no change.
  (2) `MERGE.md` Tier 2 supersession was AI-discretionary** ("one side genuinely supersedes" = a disguised
  winner-pick risk) → **tightened**: a semantic clash is **always** keep-both + Contradiction *unless the
  human explicitly instructs* a supersession; the AI no longer judges "unambiguous." Reinforces
  `never-pick-a-winner`. **(3) `memory-lint` check 7 false-positive** — session logs legitimately *quote*
  conflict markers (a pasted diff/terminal block), so scanning `memory/**` would false-fail → **rescoped to
  live top-level `memory/*.md`** (continuity/instructions/vision/decay-policy/smoke-test); `sessions/` +
  `archive/` excluded. Both runtimes + 2 new tests each (now 22/22 at parity). **(4a) Review-block gotcha
  codified in `REVIEW.md` step 9** — don't list archived ids under `## Memory References` (re-arms the
  over-archival guard); they go in the `## Memory Review` block. **(4b) Hook-fatigue note** in
  `.githooks/README.md` — a feat/memory split trips the advisory on the code commit (expected/benign);
  prefer an atomic commit to avoid it. Gate: tests 22/22 both runtimes, `memory-lint` 0/0, parity OK. The
  fresh reviewer earned its keep (the check-7 false-positive was latent — it didn't fire only because this
  session's markers sit inline in backticks, not at line-start). **Cross-vendor re-validated 2026-06-27:**
  **Gemini 3.1 Pro** re-reviewed the *applied* fixes (read-only) and confirmed all four correctly address the
  critique with **no new issues** — closing the second-opinion → apply-critique loop **end-to-end across
  vendors** (Claude built + applied; Gemini critiqued + re-validated). Gemini also correctly followed
  **lightweight mode** (read-only → no session log) — incidental cross-vendor proof of that protocol too.
  → serves: vision-agent-memory (`apply-critique-v4220-fixes`).
  <!-- id: apply-critique-v4220-fixes | created: 2026-06-27 | last_used: 2026-06-27 | uses: 1 | tier: working | origin: 2026-06-27-224339 -->

- [x] **Consolidated this session's four unreleased version bumps into a single v4.22.0 release + encoded
  the policy.** Maintainer observation: v4.22.0–v4.25.0 were all developed in one session with **nothing
  released to GitHub** (HEAD was v4.21.0) — four version numbers + four `UPGRADE.md` rungs for work no repo
  ever ran independently, inflating the ladder. **Fix:** `VERSION`→**4.22.0** (one MINOR over the released
  4.21.0; all four changes are additive); the four `UPGRADE.md` table rows + four rungs collapsed into one
  `4.21.0 → 4.22.0` row + rung that enumerates the four bundled features (a/b discovery+advisory, c
  merge-friendliness, d MERGE.md). **Policy encoded** in `UPGRADE.md` "Versioning model" → *"One version
  per release, not per feature"*: bump for a release event not per feature; keep a single **pending**
  version while unreleased; magnitude = largest change in the batch; released baseline = `VERSION` at
  `HEAD`, consolidate working-tree bumps beyond it before committing; per-feature detail lives in session
  logs + Open Threads, not extra version numbers. Memory handling: **session logs left immutable** (honest
  dev journal showing the 4.22–4.25 iteration); the four shipped threads kept as distinct facts but
  **headers relabeled** "Shipped in v4.22.0 (dev-iter 4.2X)"; `status` token → v4.22.0. → serves:
  vision-agent-memory (a clean, easy upgrade ladder is part of "adoption stays 'point it at a repo'")
  (`version-consolidation-policy-v4220`).
  <!-- id: version-consolidation-policy-v4220 | created: 2026-06-27 | last_used: 2026-06-27 | uses: 1 | tier: working | origin: 2026-06-27-222424 -->

- [x] **Re-verify invariants (due at the 2026-06-27 review) — CONFIRMED by maintainer 2026-06-27,
  one by one.** All 5 core invariants (`target-repo-scope-only`, `never-delete-vendor-files`,
  `never-pick-a-winner`, `no-build-step-agent-run`, `upgrades-additive`) **and** the Vision
  (`vision-agent-memory`) still hold; none superseded. Recent work *reinforced* them — `never-pick-a-winner`
  is now the backbone of `MERGE.md` (v4.25.0); `no-build-step-agent-run` was invoked to reject a
  resolver-*engine* in favor of a markdown protocol; the multi-contributor Vision pillar was materially
  advanced (v4.24.0 + v4.25.0). **One wording fix** (substance-preserving, maintainer-approved): added
  `sync-adapters` to the `upgrades-additive` managed-built-ins example list (it became a tool-managed
  built-in in v4.18.0) — updated in both the invariant text and ADR-0005. The review only prompts;
  the human confirmed.
  <!-- id: ot-reverify-invariants-20260627 | created: 2026-06-27 | last_used: 2026-06-27 | uses: 1 | tier: active | origin: 2026-06-27-215825 -->

- [x] **Shipped in v4.22.0 (MINOR; dev-iter 4.25) — `MERGE.md` conflict-resolution protocol.** From a **GitHub Copilot
  review** of the v4.24.0 marker check (relayed by the maintainer): *don't let the LLM directly edit git
  conflict markers* — instead convert→classify→propose→validate→human-approve. **My assessment (honest,
  both ways):** Copilot's *principle* is right and maps onto an existing invariant (**`never-pick-a-winner`**)
  + existing primitives (Contradiction thread, supersession, provenance, `memory-lint` as the deterministic
  floor); but its framing over-reaches for this project — "never edit the markers" is unachievable (someone
  deletes them; the real rule is *never silently pick a winner*), most `continuity.md` conflicts are
  **mechanical** (the v4.24.0 union/take-later rules already handle them, no AI needed), and a
  convert/classify *engine* would cut against **`no-build-step-agent-run`**. **Chosen (maintainer): tiered
  markdown protocol**, not the full pipeline. **Done:** new installed root doc **`MERGE.md`** (read on
  demand, like `DECAY`/`REVIEW`/`SKILLS`): classify hunk → **Tier 1 mechanical** (additive → union/keep-both;
  scalar → take-later; deterministic) → **Tier 2 semantic clash** (AI **never** decides — preserve both +
  raise a `Contradiction` or an unambiguous **supersession**; `[ ]`→`[x]` race keeps checked; keep provenance)
  → **`memory-lint` gate** (reuses the v4.24.0 **check 7**, no linter change) → **human approves the merge
  commit** (never auto-commit). Wired: ENABLE Step 6 install + Step 8 verify + Notes + report + advisory
  footprint; `.agent/schema.md` "Concurrency & merge-friendliness" points to it; `UPGRADE.md` source-of-truth
  map + table row + `4.24.0→4.25.0` rung. `VERSION`→4.25.0. **Dogfood:** bumped this status line's version
  token only (no changelog prose) — exercising the v4.24.0 rule live. → serves: vision-agent-memory (a shared
  memory layer must survive concurrent multi-vendor use *without an AI silently losing a teammate's fact*).
  Builds on `continuity-merge-friendly-v4240` (`merge-conflict-protocol-v4250`).
  <!-- id: merge-conflict-protocol-v4250 | created: 2026-06-27 | last_used: 2026-06-27 | uses: 1 | tier: working | origin: 2026-06-27-215127 -->

- [x] **Shipped in v4.22.0 (MINOR; dev-iter 4.24) — `continuity.md` merge-friendliness.** From a **teammate-concurrency
  observation** (maintainer): session logs are conflict-free by construction (timestamped filenames),
  but `continuity.md` is a single shared file every teammate edits — and the **`status` line had become
  a ~20 KB single-line changelog**, the worst-possible git-merge surface (concurrent bumps ⇒ unresolvable
  conflict) and a `map-don't-duplicate` violation (it shadowed `UPGRADE.md`). Chosen scope (maintainer):
  **slim status + conventions + lint guard** (MINOR; *not* the MAJOR file-split — the status anti-pattern
  was ~90% of the pain). **Done:** (1) **`status` is now spec'd as a SHORT current-state line, not a
  changelog** — `.agent/schema.md` + both `AGENTS.md` (root + template) say don't accrete per-version
  history; history lives in session logs / the `UPGRADE.md` ladder. (2) New schema section **"Concurrency
  & merge-friendliness"**: one fact per line; append-only sections are independent facts; **conflict =
  keep-both (union)** by default; scalar bumps (`last_session`/`last_review`/version token) **take the
  later/higher**; only same-thread edits need a human. (3) **`memory-lint` check 7** — a leftover
  merge-conflict marker (`<<<<<<<`/`>>>>>>>`/diff3 `|||||||`) in any `memory/*.md` is an **ERROR**; a bare
  `=======` setext heading underline is **not** flagged (false-positive guard); added to both runtimes at
  parity with **5 mirror tests each** (`.py` + `.mjs` now 20/20). (4) **Dogfooded**: this repo's own status
  line slimmed **19,828 → 1,105 chars** (read-then-write, never truncate-first — `version-md-stamp-safe-write`).
  Lockstep: `.agent/schema.md`, `AGENTS.md` (root + template), `memory-lint` (scripts + tests + SKILL.md),
  `VERSION`→4.24.0, `UPGRADE.md` (table row + rung). **Note:** continuity is still 753 lines (> `continuity_max_lines`
  300) — that bloat is accumulated `[x] Shipped` Open Threads, the **review ritual's** job to archive (overdue);
  not hand-archived here. → serves: vision-agent-memory (a shared memory layer must survive real *concurrent*
  team use; conflict-friendliness is part of faithful multi-vendor collaboration) (`continuity-merge-friendly-v4240`).
  <!-- id: continuity-merge-friendly-v4240 | created: 2026-06-27 | last_used: 2026-06-27 | uses: 1 | tier: working | origin: 2026-06-27-214222 -->

- [x] **Shipped in v4.22.0 (MINOR; dev-iter 4.23) — fresh-enable advisory + discovery-depth choice.** From a
  **user suggestion** (same conversation as v4.22.0): every agentic AI CLI has a built-in
  deep `/init` that analyses a repo and writes the findings to a **vendor** steering file
  (e.g. `CLAUDE.md`). For a *fresh* AI-enable, **show an advisory** ("about to AI-enable
  `<repo>` with the agent-memory protocol"), **say you'll scan for markdown knowledge
  artifacts, and ask whether a deep analysis is preferred** — if yes, do the deep analysis
  **and record the decision in the first session log**. **Implemented:** `ENABLE.md` **Mode A**
  now opens with the advisory + a **standard-scan (default) vs deep-analysis** choice. The
  advisory **leads with a concise exec summary** of the protocol (what it is, what it writes,
  what it won't touch, that it's committed + shared) so the user gives **informed consent**,
  plus a `cancel` option that writes nothing — added on maintainer feedback ("honesty and
  integrity are an architect's most important virtue"). **Key
  reframe (mine):** deep analysis borrows the *capability* of a vendor `/init` but writes into
  the **neutral** `memory/` layer (`instructions.md` + `continuity.md`), **never** a vendor
  file — *capability, not destination* — and deep **subsumes** (doesn't skip) the 4b markdown
  harvest, so docs are never dropped. **Mode A now writes a first enable session log** capturing
  the enable + chosen depth (faithful to "record that decision in the first session log"); this
  retires the `.gitkeep`-only sessions dir and lets enable-seeded facts set a real `origin`
  (5b note updated). Default = standard scan (also the non-interactive default; deep is opt-in).
  Lockstep: `ENABLE.md` (Mode A + 5b + 5c + Step 8 check 8 + Step 9 report line), `VERSION`→4.23.0,
  `UPGRADE.md` (table row + a `4.22.0→4.23.0` rung that optionally offers the deep analysis to
  enrich a repo enabled by the lighter path). `memory-lint` OK. **Operator-side only** — no
  installed-file shape change, no template/skill/adapter touched. → serves: vision-agent-memory
  (faithful enablement: use the best analysis the runtime offers, but keep the memory vendor-neutral
  and the choice transparent + logged). Builds on `knowledge-harvest-curious-v4220`.
  <!-- id: fresh-enable-advisory-depth-v4230 | created: 2026-06-27 | last_used: 2026-06-27 | uses: 1 | tier: working | origin: 2026-06-27-211817 -->

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
  <!-- id: knowledge-harvest-curious-v4220 | created: 2026-06-27 | last_used: 2026-06-27 | uses: 1 | tier: working | origin: 2026-06-27-210953 -->

- [x] **Shipped v4.20.3 (PATCH) — `memory-lint` catches an empty/malformed version manifest.**
  Closes the loop on the v4.20.1 bug I introduced: a truncating stamp one-liner
  (`open(p,"w").write(open(p).read()…)` — opens-for-write *before* reading, truncating to 0 bytes)
  emptied `~/sandbox/simple-proxy/.agent/version.md` at the v4.20.1 commit (pushed), which broke Mode B
  upgrade detection and made Copilot misread the repo's version (inferred "v4.19.0" from an old session
  log). Fixed in the v4.20.2 session (restored version.md). The maintainer then asked "will this happen
  again on the next upgrade?" → make it **self-catching**, not just remembered. **Fix:** added a
  deterministic `check_version_manifest` (an **ERROR**, exit 1) to both `memory-lint.py` and
  `memory-lint.mjs` at byte-identical-message parity, wired into `main`'s error list: if `.agent/version.md`
  is **present** it must carry a parseable `- **version:** X.Y.Z` line; empty/malformed → ERROR. A
  **missing** file is the valid pre-versioning baseline (handled by ENABLE/UPGRADE) and is **not** flagged.
  Mirror tests in `test_memory_lint.py` + `test_memory_lint.mjs` (empty→error, malformed→error, valid→ok,
  missing→ok) — both suites 15/15, parity. Now runs in the CI floor + every review + manual runs, so the
  exact failure mode that slipped through fails the lint instead of going unnoticed. Lockstep: scripts +
  tests + `SKILL.md` (new check #6 documented), `VERSION`→4.20.3, `UPGRADE.md` (rung + table — re-copy the
  memory-lint skill files), `README`, `CHANGELOG`. Re-copied into `~/sandbox/simple-proxy` + stamped
  4.20.3 via the **Edit tool** (never the truncate-first one-liner — the bug this rung guards against; see
  the `version-md-stamp-safe-write` operator memory). → serves: vision-agent-memory (faithful, verifiable
  enablement — a tool-managed invariant is enforced by the tool's own deterministic check, not left to
  agent diligence)
  <!-- id: memlint-version-manifest-v4203 | created: 2026-06-24 | last_used: 2026-06-24 | uses: 1 | tier: working | origin: 2026-06-24-203424 -->

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
  <!-- id: ritual-init-v4200 | created: 2026-06-24 | last_used: 2026-06-24 | uses: 1 | tier: working | origin: 2026-06-24-193329 -->

- [x] **Shipped v4.18.0 (MINOR) — `sync skill adapters` is now a runnable script (`sync-adapters` built-in).**
  Cross-vendor dogfood (continuation of v4.17.0): GitHub Copilot CLI (Gemini, Agent mode) authored a
  `greeting` skill in simple-proxy fine, but **couldn't *run* `sync skill adapters`** — it read
  `SKILLS.md` and still hunted for a non-existent command (`node memory-lint.mjs sync…`, an
  `mcp-agent-memory` npm pkg, `npm run`, grep for functions) and flailed. Root cause: sync was a **prose
  recipe with no executable**; agents expect a command. **Maintainer-gated decision:** ship a real
  script — does **not** violate `no-build-step-agent-run` (same category as the `memory-lint` script;
  the agent/vendor/CI invokes it, the tool runs nothing). **Reverses** the prior deliberate "no sync
  script" choice (evidence showed a real reliability cost). Built `agent-skills/sync-adapters/` —
  `scripts/sync-adapters.sh` (bash, no runtime — preferred) + `.mjs` (Node) + `.py` (Python) at **three-way byte-identical parity**, regen 5
  adapters/skill + signature-guarded prune (never deletes hand-authored vendor files), gitignored-only,
  `--dry-run`; `provenance: agent-memory-builtin`; an agent finds it **by description**. Lockstep:
  `SKILLS.md` (op + authoring → script), `ENABLE.md` (5i "four built-ins" + 5h runs the script),
  `UPGRADE.md` (standing sync runs script + 4.17.0→4.18.0 rung + table), `README`,
  `docs/DESIGN-skills-layer.md`, `CHANGELOG`, `VERSION`→4.18.0; the Copilot autosync hook now **calls the
  script** (no recipe duplication). `AGENTS.md`/`DECAY.md`/`REVIEW.md` unchanged. Dogfooded: parity
  verified on the tool; simple-proxy → 4.18.0 (6 skills → 30 adapters; memory-lint 0 errors).
  **Follow-up (Copilot feedback, same day):** (1) added a **bash** runtime (`sync-adapters.sh`, 3-way
  byte-identical parity) and made it the **preferred** path — Copilot needed it in a non-Node project
  (no `npm`/`package.json`); the hook + docs try bash → node → python. (2) Documented a **`delete a
  skill`** operation in `SKILLS.md` (rm the neutral source → sync auto-prunes the orphaned adapters,
  signature-guarded → mark continuity superseded) — the delete path was undocumented. Both folded into
  v4.18.0. Not committed (human-gated).
  → serves: vision-agent-memory (vendor-neutral; an operation an agent can reliably *run* on any vendor,
  not a prose recipe some agents can't execute)
  <!-- id: sync-adapters-script-v4180 | created: 2026-06-24 | last_used: 2026-06-24 | uses: 1 | tier: working | origin: 2026-06-24-172742 -->

- [x] **Shipped v4.17.0 (MINOR) — GitHub Copilot CLI skills adapter (a 5th adapter + Mode C promotion).**
  Real-work dogfood: **GitHub Copilot CLI couldn't discover a newly created skill** in
  `~/sandbox/simple-proxy` — the skills layer had four adapters (Claude/Gemini/Cursor/Kiro) but none for
  Copilot, so a skill authored in `agent-skills/` had no Copilot-native discovery path. Grounded in current
  GitHub docs (not memory): Copilot CLI has a **native agent-skills feature** on the **open Agent Skills
  standard** — project skills under `.github/skills/<name>/SKILL.md` (same `SKILL.md` shape as Claude/Kiro),
  **description-matched + `/<name>`**. So Copilot is the same shape as the Kiro adapter — this **mirrors
  v4.5.0** exactly. Added `.github/skills/` as the **5th** adapter (`sync` writes five) + Copilot
  skill-promotion in Mode C (`.github/skills/` + `.agents/skills/` → `agent-skills/`) + a skills pointer in
  the Copilot steering template — which now also **front-loads the explicit `memory/` read list** + a
  **lightweight-mode logging note** (a follow-up review finding from the maintainer's Copilot teammate:
  Copilot's **Ask/Plan** modes don't reliably chase a pointer chain, so the steering file carries the
  read list directly — a deliberate **Copilot-scoped** reversal of the thin-pointer/single-source-read-order
  convention; reliability over DRY, since Claude/Gemini/Kiro proactively load `AGENTS.md`).
  **Clarified by Copilot itself:** its Ask/Plan modes ARE read-only and *do* read `memory/`, so writing
  no session log there is **lightweight-mode-correct** (v4.7.1/v4.10.3), not a gap; in Agent mode it
  autonomously wrote a **lint-clean** session log + continuity update. So point #4 is *conformant
  behavior*, not a deficiency — corrected the initial "manual upkeep" framing in the steering file. My v4.17.0 rung had re-synced simple-proxy's *front-loaded*
  copilot-instructions to the thin template — a regression the review caught; the template is now the
  front-loaded version for everyone. Also documented an **optional Copilot `sessionEnd` hook** in
  `docs/optional-ritual-hook.md` (the analog of the Claude `Stop` hook) to *nudge* the manual ritual
  point #4 raised — advisory, opt-in, **not** auto-installed; dropped a ready
  `.github/hooks/agent-memory-session.json` into `~/sandbox/simple-proxy` for the maintainer's test
  (`.github/hooks/` is tracked, unlike `.github/skills/`). **Key subtlety:** `.github/` can't be gitignored
  wholesale (holds the tracked `copilot-instructions.md` + `workflows/`), so `.github/skills/` is ignored
  **path-scoped** — the one structural difference from the other four adapter dirs. No new ADR (a vendor
  adapter is not a new architecture decision — same call as Kiro 4.5.0). Lockstep: `SKILLS.md`, `AGENTS.md`
  (root + template), `templates/.agent/schema.md`, `ENABLE.md` (5h + Step 8 five-adapter assertion + Notes +
  report), `UPGRADE.md` (rung + table + standing sync), `MIGRATE.md` (table + B2 + Copilot section),
  `templates/.github/copilot-instructions.md`, `README`, `docs/DESIGN-skills-layer.md`, `CHANGELOG`,
  `VERSION`→4.17.0, root + `templates/.gitignore`. `DECAY.md`/`REVIEW.md` unchanged. Dogfooded: 5-adapter
  sync on the tool (4 skills → 20 adapters; em-dash + apostrophe embed cleanly in YAML+TOML) + upgraded
  `~/sandbox/simple-proxy` to 4.17.0 (`memory-lint` 0 errors). **Cross-vendor validated 2026-06-24:**
  GitHub Copilot CLI (Gemini 3.1 Pro), **Agent mode**, autonomously authored a `greeting` skill in
  simple-proxy, ran `sync skill adapters`, generated **all 5** adapters, and recognized the
  `.github/skills/` adapter — "behaves exactly as documented." (The `date -u` guardrail + single-line/
  quote-free descriptions also held up.) One friction point → fix: Copilot loads adapters at **init**,
  so a freshly-synced `/greeting` needed a session restart/rescan — added a **hot-reload caveat** to
  `SKILLS.md`'s sync op (re-synced to simple-proxy). **Further friction (2026-06-24):** agents don't
  reliably run `sync skill adapters` *after* authoring a skill (Copilot needed prompting; it had
  self-claimed autonomy earlier — non-deterministic) → strengthened the **authoring convention** to an
  explicit **3-step action** (write → `sync` → reload) in `SKILLS.md` + `AGENTS.md` (root/template).
  Can't force it mid-session (`no-build-step-agent-run`; auto-sync guaranteed only at enable/upgrade,
  v4.12.0), but it's now emphatic + always-read. Plus an **opt-in Copilot `postToolUse` auto-sync hook**
  (documented in `docs/optional-ritual-hook.md` + a ready one dropped in simple-proxy) that regenerates
  the `.github/skills/` adapter automatically after a tool use — convenience-scoped (Copilot-only, no
  prune, duplicates the recipe in bash → local opt-in; `/restart` still loads it); the agent-run
  `sync skill adapters` stays canonical, and the tool still ships **no sync script** (no-code held).
  Not committed (human-gated).
  → serves: vision-agent-memory (vendor-neutral; a skill authored once works natively on every vendor —
  now including GitHub Copilot CLI)
  <!-- id: copilot-adapter-v4170 | created: 2026-06-24 | last_used: 2026-06-24 | uses: 1 | tier: working | origin: 2026-06-24-155506 -->

- [x] **Shipped v4.14.1 (PATCH) — clarify the re-synced `AGENTS.md` source (cross-vendor finding).**
  Validating Copilot's (Gemini 3.1 Pro) Mode B upgrade of `~/sandbox/mercury-composable` (v3.7.0 →
  v4.14.0, uncommitted): mostly correct (enabled_with/mode preserved; DECAY/REVIEW/SKILLS/schema
  byte-identical; `vision.md` proper DRAFT + `(vision-bootstrap)`; built-ins provenance-marked + scripts
  faithful; `.gitignore` additive; `docs/ADR.md` correctly absent; `memory-lint` 0/0). **One defect:** it
  re-synced the target's `AGENTS.md` from the tool's **root** `AGENTS.md` (operator/dual-mode dispatcher)
  instead of `templates/AGENTS.md` — a regression (correct before; clobbered), leaving the target
  referencing the non-installed `ENABLE.md`. **Root cause = tool ambiguity:** `UPGRADE.md`'s
  "(root + template)" notation + "copy from the tool root / templates" guidance never said *per file*
  which source a target gets. **Fix:** `UPGRADE.md` "Source of truth for re-synced files" map (target
  `AGENTS.md` ← `templates/AGENTS.md`; `DECAY/REVIEW/SKILLS` ← root; `schema`/bootstraps ← `templates/`)
  + never-install-root-`AGENTS.md` warning + grep self-check, and a `4.14.0→4.14.1` rung that
  verifies/repairs a mis-synced `AGENTS.md`. `ENABLE.md` Step 6 was already explicit (fresh enable
  unaffected). Operator-only doc fix → no installed-shape change. Lockstep: `UPGRADE.md` (callout + rung
  + table), `VERSION`→4.14.1, `README`, `CHANGELOG`. mercury to be reset + re-enabled to re-test the fix.
  → serves: vision-agent-memory (faithful multi-vendor enablement; a target never receives operator docs)
  <!-- id: ot-agents-source-fix-v4141 | created: 2026-06-20 | last_used: 2026-06-20 | uses: 1 | tier: active | origin: 2026-06-20-231636 -->

- [x] **Shipped v4.14.0 (MINOR) — optional Architecture Decision Record log (`docs/ADR.md`).**
  Examined the VBDI framework (`docs/agent-cognitive-framework.md`, `docs/DESIGN-vbdi-lifecycle.md` §4)
  to organize the key architectural principles as ADRs. Finding: the **Design** altitude was realized
  only by `continuity.md`'s `## Architectural Invariants`/`## Key Decisions` + the long-form
  `docs/DESIGN-*.md` — missing was an *atomic, dated, status-tracked, never-deleted* record of each
  decision *with its rationale*, browsable by a human IT-governance audience. That is exactly an ADR
  (Nygard 2011), and its "superseded/deprecated-never-deleted" lifecycle **is** the memory layer's own
  supersession model (`DECAY.md` §9). Built `docs/ADR.md` (single-file decision log, **newest-first**),
  **seeded with the 5 standing Architectural Invariants + the superseded `no-code-markdown-only`
  decision** (ADR-0001…0006; `no-code-markdown-only` = **ADR-0004**, *Superseded by ADR-0006* — the
  prior decision ADR-0006 replaced; surfaced + inserted on maintainer review), each Status · Date · Abstract ·
  **Rationale incl. consequences/trade-offs** + `formalizes:`/`serves:` links. Forks settled with the
  maintainer (plan-gated): corrected terminology to "Architecture **Decision** Record" + canonical
  `Deprecated` (not "retired"); single-file newest-on-top (the lighter decision-log variant vs.
  file-per-record `adr-tools`/MADR — accepted deliberately); **tool-only + optional, not auto-installed**;
  **seed = the 5 invariants only** (minimalist — ADR is for human IT governance, kept bare-minimum +
  token-efficient); **on-demand, never in the per-session read path** (the decisive token constraint);
  **map-don't-duplicate** cross-linking (`formalizes:` ↔ a visible `(ADR-NNNN)` invariant-title tag —
  a human pointer, not an agent read-cue; moved off the hidden footer on maintainer review so a human
  auditor sees it). Lockstep: `docs/ADR.md` (new),
  `.agent/schema.md`, `AGENTS.md` (+ template), `DECAY.md` §12, `docs/DESIGN-vbdi-lifecycle.md` §4,
  `continuity.md` (5 invariant footers + this), `README`, `VERSION`→4.14.0, `UPGRADE.md` rung + table,
  `CHANGELOG`. `REVIEW.md`/skills/scripts untouched. Verified: `memory-lint` 0/0 (the new `adr:` footer
  fields parse cleanly); all 5 `formalizes:` ids resolve; ADR absent from the read list. Dogfooded here
  only — no target gets a `docs/ADR.md` unless its team adopts one. Possible future: a `memory-lint` ADR
  link-resolution check (out of scope to avoid bloat).
  → serves: vision-agent-memory (faithful, traceable Design record; lightweight, token-efficient,
  human-facing governance — intent traceable end-to-end without ceremony)
  <!-- id: adr-ledger-v4140 | created: 2026-06-20 | last_used: 2026-06-20 | uses: 1 | tier: active | origin: 2026-06-20-174156 -->

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
  <!-- id: vbdi-lifecycle-direction | created: 2026-06-14 | last_used: 2026-06-15 | uses: 3 | tier: active | origin: 2026-06-14-030729 -->

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
  <!-- id: skills-layer-v410 | created: 2026-06-15 | last_used: 2026-06-18 | uses: 10 | tier: active | origin: 2026-06-15-234801 -->

> _v4.2.0 ("sync skill adapters", `sync-adapters-v420`) archived faded → `archive/2026-Q2.md` (2026-06-18 review)._

### Shipped — v4.4.0 / v4.5.0 + the hello-world dogfood (reactivated 2026-06-18)

> Reactivated from `archive/2026-Q2.md` 2026-06-18 — the 2026-06-18-051933 review (GitHub Copilot)
> swept these while they were still referenced in the window (low sslu); restored to `active`.

- **Shipped v4.5.0 — Kiro support (a 4th adapter + Mode C detection).** Amazon's **Kiro IDE**
  converges on the two open standards this tool bets on: it auto-reads root **`AGENTS.md`** (memory
  layer needs no pointer file) and its Agent Skills follow the **open Agent Skills standard** (same
  `SKILL.md` shape as Claude). Added a 4th adapter target `.kiro/skills/<name>/SKILL.md` (`sync`
  writes four adapters) + **Kiro in the Mode C detection table** (`MIGRATE.md`: steering →
  instructions, skills → `agent-skills/`, specs → `legacy/`). **Kiro Powers need no special
  handling** (partner bundles that *consume* open-standard skills). → serves: vision-agent-memory
  <!-- id: kiro-adapter-v450 | created: 2026-06-16 | last_used: 2026-06-19 | uses: 7 | tier: active | origin: 2026-06-16-221832 -->

### Shipped — v4.7.0–v4.7.1: cross-vendor refinements (2026-06-17)
- **Shipped v4.7.0 — lightweight mode for memory-neutral tasks (MINOR).** From a **real
  cross-vendor enablement**: the maintainer used the *installed* tool to AI-enable a **new
  source-code repo via Kiro IDE**, and Kiro gave an honest assessment (strong validation — the
  full text is a notable artifact): the protocol "helps more than it interferes," praising immediate
  orientation from `instructions.md`/`continuity.md` ("no archaeology"), the directly-actionable
  `SKILLS.md`, and the multi-session/multi-agent continuity value. **The one critique:** the
  per-session *write* ceremony is disproportionate for trivial tasks ("for a two-line script and a
  skill file, the protocol's weight is noticeable") → suggested a **"lightweight mode."** Shipped it
  (maintainer chose the conservative **lite-log** variant): for a memory-neutral task (no
  fact/decision/thread/state change), write a **one-line "lite" session log** (`## Memory References`
  → `(none)`) and **skip** the full template / fact-footers / continuity edits — the **ledger stays
  continuous** (multi-agent continuity preserved), and the review treats a lite log as a normal
  reference-free session (so `DECAY.md`/`REVIEW.md` need no change). Scales ceremony to memory
  impact — same "lightweight" north star that drove v4.4.0. Touched: `AGENTS.md` (root + template),
  `VERSION`→4.7.0, `UPGRADE.md` 4.6.0→4.7.0 rung + table, `README`/`CHANGELOG`. → serves:
  vision-agent-memory (lightweight; multi-contributor). **Independent third-vendor endorsement —
  good leadership/demo evidence.**
  **Refined v4.7.1 (maintainer):** the skip is keyed to the **objective "did a file change?"**
  test, **not** a subjective "is this trivial?" call — because *trivial is a judgment call and both
  AI and human misjudge it*, and a misjudged change that actually mattered would slip out of the
  ledger. So: **read-only** sessions (no file changes) write **no log**; **any file change, even one
  line,** writes at least a **lite log** (never skipped on a "felt trivial" call; the git diff
  anchors it); a memory-relevant event → full ritual. `AGENTS.md` note rewritten to this three-tier
  form; `VERSION`→4.7.1, `UPGRADE.md` 4.7.0→4.7.1 rung + table, `README`/`CHANGELOG`.
  <!-- id: lightweight-mode-v470 | created: 2026-06-17 | last_used: 2026-06-17 | uses: 3 | tier: archive-candidate | origin: 2026-06-17-184652 -->

- **Shipped v4.9.0 — `memory-lint`, a deterministic verifier skill (MINOR).** The stronger fix
  Copilot argued for after v4.8.0: v4.8.0's markdown guard still left the *primary* count to the
  LLM, and LLMs miscount. So built a portable, optional **`memory-lint`** skill
  (`agent-skills/memory-lint/SKILL.md` + `scripts/memory-lint.py`, Python 3 stdlib, no install) that
  checks integrity *deterministically*: no id in both `continuity.md` + archive; no archived-as-faded
  fact referenced within `archive_window` (the decay-miscount guard); advisory overdue (excludes
  `core`/`superseded`/pinned `- [ ]`); supersession links resolve. Exit non-zero → wire to pre-commit/CI.
  The tool never runs it (`no-build-step-agent-run`); it lints the *arithmetic*, the agent judges
  *meaning*. **First run caught a real over-archival both Copilot AND a hand re-check missed** —
  `skills-layer-v411-fixes` (sslu 16 ≤ 20) — now reactivated. `REVIEW.md` step 6 points to it.
  **Not auto-installed into targets** at v4.9.0 (would add a script to every repo) — a deliberate
  future option **taken in v4.10.0** (now installed into every enabled repo; see `fresh-review-v4100`).
  Touched: `agent-skills/memory-lint/` (new), `REVIEW.md`, `VERSION`→4.9.0, `UPGRADE.md` rung + table,
  `README`/`CHANGELOG`. → serves: vision-agent-memory (faithful, verifiable memory)
  <!-- id: lint-skill-v490 | created: 2026-06-18 | last_used: 2026-06-20 | uses: 7 | tier: active | origin: 2026-06-18-065458 -->

### Blueprint — gaps from Current State (v4.10.0) to the Vision  (serves: vision-agent-memory)
> Derived 2026-06-15 from `memory/vision.md` (maintainer-confirmed). Typed Open Threads
> `(blueprint)`: each is a Vision↔reality gap that closes when delivered. The *backward*
> memory layer is not here — it's done; every gap is *forward*. These operationalize the
> `vbdi-lifecycle-direction` thread above. First real VBDI loop, dogfooded on the tool itself.

- [x] **(blueprint) DELIVERED v4.19.0.** Reliable, vendor-neutral **ritual triggers** — the rituals (end-of-session log,
  review, sync) are agent-self-triggered conventions that fail in practice (client teams: not followed
  through even with Claude; a Copilot-only team has *no* triggers; the hook layer is opt-in, per-vendor,
  and doesn't travel into targets — proven on `~/sandbox/simple-proxy`). **Design drafted (PROPOSED):**
  `docs/DESIGN-ritual-triggers.md` — a layered model: agent-primary (strengthen the *definition-of-done*
  framing) + a **vendor-neutral git-hook + CI net** (auto-stub the session log via the capture/judgment
  split; `memory-lint` warns when review is due; run the `sync-adapters` script) + vendor hooks demoted
  to an optional real-time nicety **with the recipe finally traveling into targets**. Reconciled with the
  Vision: env-run optional helpers (`no-build-step-agent-run`); the tool still runs nothing itself.
  **Maintainer (2026-06-24): endorsed git-hooks + CI as the direction**, and added a **zero-manual /
  untrained-user adoption constraint** ("any manual operation or trigger is a barrier to adoption") →
  §6.4 **resolved**: **CI = zero-setup floor** (committed workflow runs server-side, no per-user config),
  **agent auto-activates** the git hook at enable (no manual user step); *honest limit:* git can't
  auto-run hooks on a bare clone (security), so **CI backstops** until an agent activates the local hook.
  Remaining forks (auto-stub / advisory-default / post-commit) carried my recommendations. **Built +
  shipped v4.19.0 (2026-06-24):** committed `.githooks/post-commit` (auto-stub the session log on a
  real-work commit; re-sync adapters) **agent-activated** via `git config core.hooksPath .githooks`
  (no manual user step) + a **CI floor** `.github/workflows/agent-memory.yml` (`memory-lint` + advisory
  session-log check on push/PR, zero per-user setup; opt-in `AGENT_MEMORY_STRICT` gate). Advisory, never
  blocks; `no-build-step-agent-run` holds. Honest limit recorded: git can't auto-run hooks on a bare
  clone → CI backstops. ENABLE installs + activates; `AGENTS.md` gains the "reinforced, not just
  documented" + *definition-of-done* framing; `optional-ritual-hook.md` reframed to the optional
  per-vendor extras. Hook tested in a throwaway repo (auto-stub, no pile-up, quiet-when-logged); dogfooded
  on the tool + `~/sandbox/simple-proxy` (→ 4.19.0). → serves: vision-agent-memory
  <!-- id: bp-ritual-triggers | created: 2026-06-24 | last_used: 2026-06-24 | uses: 1 | tier: working | origin: 2026-06-24-181136 -->
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

### Backlog — vNext (temporal & supersession) + beyond
> From the 2026-06-13 industry-alignment assessment:
> `docs/assessments/2026-06-13-industry-alignment.md`. Verdict: on track; distinctive
> on event-sourcing/determinism/governance; one real gap = temporal/supersession.
> Re-run the assessment after meaningful iterations and compare its scorecard.

- [ ] **Dogfooding on real work (ongoing).** Already delivering: the simple-proxy
  enable surfaced v3.1.0 (`.gitignore`), and the simple-proxy Node→Rust refactor's
  field report drove v3.2.0 (protocol clarifications). Keep feeding real-work insights
  back into this backlog. (Stated 2026-06-13.)
  <!-- id: backlog-real-work-dogfood | created: 2026-06-13 | last_used: 2026-06-20 | uses: 5 | tier: active -->

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
