# Changelog

## Release notes

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> Releases 1.0.0–3.0.0 below were reconstructed retrospectively (this changelog was
> introduced after 3.0.0 shipped), organized by capability rather than by individual
> commit. The capability ladder matches `VERSION` and `UPGRADE.md`.

## Version 4.29.1, 7/12/2026

> **Template import blocks become a `{{BOOTSTRAP_IMPORTS}}` placeholder (PATCH).** Cross-vendor
> dogfooding of v4.29.0 (a GitHub Copilot assessment, independently corroborated live on Claude Code)
> found a tool-repo instruction bleed-through the release amplified: runtimes that auto-load
> **directory-scoped instruction files** picked up `templates/CLAUDE.md`, and because `@`-imports
> resolve *relative to the containing file*, its live import block pulled the **placeholder template
> stubs** (`templates/AGENTS.md`, `templates/memory/*` — `{{PROJECT_NAME}}` junk, "last_session:
> (none yet)", conflicting "Identify yourself as…" lines) into context as if they were real
> instructions. Tool-repo-only: installed targets have no `templates/` directory.

### Fixed
- **`templates/CLAUDE.md` + `templates/GEMINI.md` no longer carry live import lines.** The block is
  now a `{{BOOTSTRAP_IMPORTS}}` placeholder (the established `{{UPPER_SNAKE_CASE}}` mechanism);
  `ENABLE.md` Step 6 defines each vendor's literal block (Claude `@path` idiom / Gemini `@./path.md`)
  and expands it at install. **Installed output is byte-identical to v4.29.0's** — enabled repos need
  nothing beyond a version stamp (see the `4.29.0 → 4.29.1` rung).
- **The `4.28.4 → 4.29.0` rung no longer points at the templates for the block** — it references the
  literal blocks in `ENABLE.md` Step 6, so a ladder run can't copy the placeholder verbatim.

### Changed
- **Honest residual, documented:** a runtime that auto-loads a nested `AGENTS.md` directly may still
  surface `templates/AGENTS.md` itself — behavior that predates v4.29.0 and belongs to the runtime;
  this patch removes the amplification (the memory-stub pull-in via imports), which is the part the
  tool controls. Root `CLAUDE.md`/`GEMINI.md` keep their live imports — that's the feature, dogfooded.
- **Lockstep:** `VERSION` → 4.29.1; `CHANGELOG`; `README` row; `UPGRADE.md` row + rung (+ the 4.29.0
  rung amendment); `templates/CLAUDE.md`/`GEMINI.md`; `ENABLE.md` Step 6. No memory-file shape change;
  skills/adapters unchanged.

## Version 4.29.0, 7/12/2026

> **Before-session context presence — bootstrap `@`-imports + an opt-in SessionStart recipe (MINOR).**
> A child-repo field report (2026-07-11) showed agents skipping the before-session read chain
> (`CLAUDE.md → AGENTS.md → memory/*`) under task pressure — skill-unawareness, off-model engagement,
> rework, apparent "memory loss." The root cause is structural, not a one-off lapse: the v4.19.0
> trigger layer reinforces only the *after*-session rituals, because its vendor-neutral substrate
> (git + CI) has no session-start moment — so the before-session read rested on prompt adherence,
> the same non-determinism v4.20.1 recorded for Copilot self-init. This closes the *presence* half
> of that asymmetry; *attendance* remains agent judgment.

### Added
- **Native `@`-imports in the bootstrap pointers.** `templates/CLAUDE.md` and `templates/GEMINI.md`
  (and this repo's own root pointers — dogfooded) now import `@AGENTS.md`,
  `@memory/instructions.md`, `@memory/continuity.md`, `@memory/vision.md`, so the hub + core
  memory files are **structurally present** at session start on import-capable runtimes
  (Claude Code: `@path`, relative to the containing file, max 4 hops, code blocks skipped;
  Gemini CLI: the `@./path.md` form, `.md` files only, max depth 5). Markdown-only, no hooks —
  the same fix-shape as v4.20.1's copilot-instructions front-load. Imports live **only in the
  per-vendor bootstrap files**; `AGENTS.md` stays vendor-neutral.
- **Opt-in `SessionStart` injection recipe** in `docs/optional-ritual-hook.md` (tool-only, never
  installed) — "Option A0," for teams that also want `memory/sessions/` recency injected (imports
  can't express dynamic paths). Deliberately **not** installed by `ENABLE.md`: the installed
  `.gitignore` ignores all of `.claude/` (personal runtime config; a committed `settings.json`
  accretes personal allow-lists — observed in the field), and the hook is Claude-Code-only —
  Layer-2 in the trigger-design taxonomy, a per-vendor nicety, not the vendor-neutral floor.

### Changed
- **Honest limits, stated where they bite:** the bootstrap note tells the agent imports can't
  express dynamic paths — the newest 2–3 `memory/sessions/` logs stay an explicit read;
  Cursor/Windsurf/Copilot have no import mechanism and keep the prose pointer (Copilot's
  mitigation remains the v4.20.1 front-load pattern). The imported files enter context every
  session, so the continuity-bloat controls (v4.24.0/4.28.2/4.28.3) are now load-bearing, not
  cosmetic. Attestation canaries (a child repo's local hardening) remain a downstream per-repo
  pattern, not part of the tool.
- **Lockstep:** `VERSION` → 4.29.0; `CHANGELOG`; `README` row; `UPGRADE.md` row +
  `4.28.4 → 4.29.0` rung; root + template `CLAUDE.md`/`GEMINI.md`; `docs/optional-ritual-hook.md`
  (retitled "Reinforcing the session rituals with hooks" — it now covers a before-session layer).
  No memory-file shape change; skills/adapters unchanged.

## Version 4.28.4, 7/6/2026

> **`Co-Authored-By` trailer duplication — reframed as a dedup-by-email invariant (PATCH).** Third
> field report from `mercury-composable`: the v4.28.0 commit-attribution guidance assumed the agent
> *fully authors* the message, but the agent co-authors it **with its harness**, which often injects
> its *own* (model-version) `Co-Authored-By`. A conscientious agent then appended a second (stable-name)
> trailer → duplicate co-authors for one collaborator; squash-merges compounded it (one observed commit
> had 55 trailer lines). Doc-only refinement of the convention; no code, no shape change.

### Changed
- **The rule is now a deterministic invariant, keyed on email.** `AGENTS.md` (root + `templates/`)
  reframes the mental model — *you co-author the commit message **with** your harness; treat the
  harness's message as the base and **reconcile**, don't blindly append* — and states the invariant:
  **at most one `Co-Authored-By` per collaborator, matched on email** (`Claude Code`, `Claude Opus 4.8`,
  `Gemini CLI`, `Gemini 2.5` … are one collaborator at one `noreply@…` address; the name varies, the
  email doesn't). A three-branch resolution tree replaces the ambiguous "accept it": harness trailer you
  can't suppress → that's your one; you control the message → emit exactly one stable-name trailer and
  drop the harness duplicate at the same email; **never both**.
- **Squash-merge guidance is forge-aware.** The canonical trailer lives **once** (PR-description footer;
  omitted from per-commit bodies); trim inline repeats so one line per collaborator survives.
- **PR template + docs.** The `.github/pull_request_template.md` footer comment (root + `templates/`)
  and `docs/getting-started.md` now carry the one-per-collaborator-by-email rule.
- **Enforcement deferred (deliberate).** A dedup **hook** and a `memory-lint` advisory were proposed;
  both deferred — an auto-dedup `commit-msg` hook would *rewrite* commit messages, a departure from the
  tool's "never mutate your commits" stance. Revisit (an *observational* lint advisory first) if the doc
  fix doesn't hold in the field.
- **Lockstep:** `VERSION` → 4.28.4; `README` row; `UPGRADE.md` row + `4.28.3 → 4.28.4` rung; docs site.
  Re-sync `AGENTS.md` + `.github/pull_request_template.md` on enabled repos. No memory-file shape change;
  skills/adapters unchanged.

## Version 4.28.3, 7/6/2026

> **`[continuity-bloat]` line-count message is now decay-aware (PATCH).** Second field report from
> `mercury-composable` (a 29-module Maven reactor): after a by-the-book review the *fact* count is
> healthy but the `continuity_max_lines` backstop trips on genuinely-active, information-dense Key
> Decisions — and the review has **nothing to archive**, so the warning can't be honestly cleared.
> Same failure class as v4.28.2 (an unclearable warning erodes the signal), but on the line axis; the
> generic "a review is due to lean it down" also *nudges toward premature archival of active facts* —
> REVIEW.md's costliest error.

### Fixed
- **The line-count `[continuity-bloat]` message branches on whether anything is actually archivable.**
  `memory-lint` now computes `archivable` = facts overdue for decay (`sslu > archive_window`, excluding
  core/superseded/pinned) + superseded facts. When lines exceed `continuity_max_lines` **and**
  `archivable == 0`, the message tells the truth — *"nothing is archivable yet; the excess is
  active/dense facts. Condense shipped decisions, or raise continuity_max_lines in decay-policy.md if
  this repo is legitimately large."* — instead of prescribing a review that can't help. When something
  *is* archivable, the original actionable message stands. Validated on mercury's live memory (37 facts
  / 708 lines / 0 archivable → the honest message; both runtimes byte-identical).
- **`decay-policy.md` note.** The `continuity_max_lines` comment now states it is *meant* to be raised
  for a legitimately large/complex repo (covers the field report's per-repo-acknowledgement ask cheaply;
  the value was already per-repo tunable).
- **Scope / deferred.** Only the line-count message changed; the fact-count check (v4.28.2) is untouched.
  A dedicated non-archival "condense shipped decisions" lever was proposed but **deferred** until the need
  recurs in the field — the honest message points at that lever without building it yet.
- **Lockstep:** `VERSION` → 4.28.3; `check_continuity_health` gains an optional `archivable` arg
  (default unknown → generic message; backward compatible) in both runtimes at parity; `main()` computes
  and passes it; two new mirror tests (`archivable > 0` → actionable, `archivable == 0` → active-verbosity).
  `README` row; `UPGRADE.md` row + `4.28.2 → 4.28.3` rung. Skill description unchanged → adapters need no re-sync.

## Version 4.28.2, 7/4/2026

> **Fix `[continuity-bloat]` false positive on mature repos (PATCH).** Field report from
> `mercury-composable`: the bloat check fired permanently after a correct review because it
> counted `tier: core` facts and pinned open threads against the cap, even though those entries
> can never be archived. The fix aligns the count with `decay-policy.md`'s documented intent
> ("count of **decaying** facts/threads") by excluding non-archivable entries.

### Fixed
- **`memory-lint` bloat check now counts only decay-eligible facts.** `tier: core` entries
  (structural invariants) and pinned open `- [ ]` threads are excluded from `nfacts` before
  comparing against `continuity_max_facts`. A repo with 14 core facts + 11 open threads + 16
  working facts now correctly reads `16 < 30` (clean) rather than `41 > 30` (chronic WARN) after
  a fully correct review. The warning message updated to say "decay-eligible facts" so the scope
  is unambiguous.
- **Lockstep:** `VERSION` → 4.28.2; `check_continuity_health` gains optional `pinned` param
  (default `set()` — backward compatible); call site passes the already-computed `pinned` set;
  new test `test_fact_bloat_excludes_core_and_pinned` covers the mercury scenario directly.

## Version 4.28.1, 7/2/2026

> **Post-commit hook: uncommitted-session-log guard (PATCH).** The auto-stub window check misfired
> on the recommended two-commit pattern (feature commit → `chore(memory)` commit) when the session
> log was written more than 30 min before the feature commit — the clock is the wrong proxy when the
> artifact state is directly observable.

### Fixed
- **Suppress the auto-stub when a session log already exists uncommitted.** The `.githooks/post-commit`
  auto-stub gained a **primary guard**: before the filename-timestamp window check, it inspects
  `git status --porcelain -- memory/sessions/` for any uncommitted `.md`. If one is staged, modified,
  or untracked, the agent already has a log for this session — the hook emits the enrich-and-commit
  nudge and skips stubbing. Previously the filename-timestamp threshold treated an in-flight
  (uncommitted) log written >30 min before the feature commit as "too old" and stubbed a
  near-duplicate. The window check stays as fallback for already-committed, hours-old logs (e.g. a
  follow-on commit). Bash 3.2-compatible; hook stays non-blocking.
- **Lockstep:** `VERSION` → 4.28.1; `UPGRADE.md` row + `4.28.0 → 4.28.1` rung. Re-copy
  `.githooks/post-commit`. No memory-file shape change; no skill/adapter change.

## Version 4.28.0, 6/29/2026

> **Co-author convention cleanup — stable agent identity + one trailer (MINOR).** From a real-world
> finding dogfooding the v4.27.0 convention on `mercury-composable`: a squash-merged PR (#126)
> surfaced two imperfections in how the `Co-Authored-By` self-identification *renders*. The
> attribution itself worked (human + AI both credited, Verified) — these are consistency fixes.

### Changed
- **Stable agent identity, not a model version.** The convention said "identify yourself *the same
  way you do in session logs*," but session logs use a stable agent name (`Claude Code`) while the
  commit/PR trailer was a **model-version** string (`Claude Opus 4.8`) — so it (a) wasn't actually
  "the same," and (b) churns every model release, fragmenting the co-author across many identities
  over time. `AGENTS.md` (root + `templates/`) and the PR-template footer comment now specify the
  **stable agent name** — the *actual AI collaborator* (`Claude Code`, `Gemini CLI`, …), kept
  vendor-neutral via a `<your agent name>` placeholder — explicitly **not** a model version. Where a
  runtime auto-injects a model-version *commit* trailer it can't override, that's accepted (the
  agent controls the PR footer + session logs, which carry the stable name).
- **One trailer on squash-merge.** Every commit carries the trailer (often harness-injected), so a
  squash-merged PR stacked ~9 identical inline `Co-Authored-By` lines **plus** the consolidated one
  GitHub appends after the `---------` separator. The convention now notes: on a squash-merge,
  collapse to a **single** `Co-Authored-By:` — GitHub's appended consolidated line is canonical;
  trim the redundant inline repeats. Advisory (the agent can't suppress the harness trailer or
  GitHub's squash template; this is merge-time guidance).
- **Lockstep:** `VERSION` → 4.28.0; `UPGRADE.md` row + `4.27.0 → 4.28.0` rung; `README` row (and the
  recent-releases table trimmed back to its 10-most-recent cap); docs site (Getting Started). No
  memory-file shape change; no skill/adapter change.

## Version 4.27.0, 6/29/2026

> **Standardized PR description — lead with What / Why (MINOR).** From a maintainer suggestion:
> standardize the look-and-feel of pull-request descriptions created under the agent-memory
> protocol with two short summary sections — **What** and **Why** — so the standard propagates to
> every AI-enabled repo. A natural fit: *why* is already a first-class artifact throughout the
> protocol (the VBDI intent trace, ADR rationale, supersession reasons, even this changelog's own
> `> summary + Why` shape), and the content projects straight from the session log(s) in the PR —
> What from the change, Why from the Blueprint gap / decision it serves. There was no PR guidance
> before this (only a commit `Co-Authored-By` trailer convention), so it fills a real gap.

### Added
- **`.github/pull_request_template.md`** (this repo + `templates/`, so every enabled repo inherits
  it) — two sections, **What** (the change) and **Why** (the intent it serves; substantive intent,
  **not** a restatement of What), each **1–2 short paragraphs** (flexible — a trivial PR isn't
  padded; a What may use a bullet or two). GitHub auto-populates the PR body from it; the agent
  draws the content from the session log(s) in the PR. The template also closes with a
  self-identifying **`Co-Authored-By:`** footer — the same authorship-traceability convention as
  commits and session logs, now extended to the PR altitude. **Advisory, never a gate**
  (`guide-don't-prescribe`). Installed by `ENABLE.md` Step 6 (tracked — it travels).

### Changed
- **`AGENTS.md` (root + `templates/`)** — the after-session commit step gains an "Opening a pull
  request? → lead with **What** / **Why**" convention next to the co-author-trailer note, plus a
  checklist line. This is the **vendor-neutral backstop**: the `.github/` template only covers the
  GitHub web UI / `gh pr create`, so the steering line carries the convention for agents that
  compose a PR body themselves. Re-sync a target's `AGENTS.md` from `templates/AGENTS.md`.
- **`ENABLE.md` Step 6** installs the new template; **`UPGRADE.md`** gains the `4.26.1 → 4.27.0`
  rung + version-table row; **`README`** version-table row + file-tree entry; docs site updated.
  `VERSION` → 4.27.0. No memory-file shape change.

## Version 4.26.1, 6/28/2026

> **`[stale-metadata]` / `refresh-metadata` no longer opine on a pinned thread's tier (PATCH).** A sanity
> check of mercury (post-Copilot review) surfaced that v4.26.0 flagged every `working`-tagged **pinned
> `- [ ]` open thread** as "should be `active`" — noise, since a pinned thread never decays *regardless* of
> its tier label. The protection is its pinned-ness (being unchecked), not the label. Refinement: the tooling
> now has **no opinion** on a pinned thread's tier — `memory-lint` won't flag it and `refresh-metadata` won't
> rewrite it (it still refreshes the factual `uses`/`last_used`). Surfaced comparing `refresh-metadata`
> against Copilot's own `update-metadata.py` (which *skipped* pinned threads); this lands on the same
> outcome, by a cleaner rule.

### Changed
- **`memory-lint` `expected_tier`** (check 9) + **`refresh-metadata` `expected_tier`**: a pinned thread
  returns its **stored** tier (no drift, no rewrite) instead of being forced to `active`. Both runtimes at
  parity; tests added (memory-lint 34, refresh-metadata unchanged count — assertion updated).
- **`DECAY.md` rule 4** + both SKILL.md notes clarify: pinned-ness protects an open thread, not its tier
  label; `working` on a pinned thread is fine. Doc-only otherwise; no shape change.

## Version 4.26.0, 6/28/2026

> **`refresh-metadata` + a `memory-lint` `[stale-metadata]` advisory — close the skipped-re-tier gap (MINOR).**
> From a cross-vendor field test: Copilot / Gemini 3.1 Pro committed the v4.25.0 upgrade to mercury and,
> seeing the `[review-overdue]` advisory, **ran the review unprompted** — correctly using `archive-fact`
> (the over-archival guard even caught a premature-archive attempt and it reverted). But it did Step 4
> (archive) + Step 5 (sweep) and **skipped Step 2 (apply events) + Step 3 (re-tier)** — leaving stale
> `last_used`/`uses`/`tier` footers on the facts that stayed. A capable agent silently did half the ritual.
> This is the **third instance of one failure class** (after the truncation trap → `archive-fact`, and the
> never-fired review → `[review-overdue]`): *multi-step agent rituals get partially executed.* The fix
> refines the earlier "reject auto-fix" stance — the real boundary is **judgment vs. arithmetic**: deciding
> *what to archive* is judgment (stays with the agent); recomputing metadata is **arithmetic** (the "full
> rebuild" path REVIEW.md already calls deterministic + reproducible) and is safe to mechanize.

### Added
- **`agent-skills/refresh-metadata/`** — the **7th** built-in (`provenance: agent-memory-builtin`). Executes
  REVIEW.md steps 2–3 deterministically: recomputes every fact's `last_used` / `uses` / `tier` from the
  `## Memory References` across `memory/sessions/` and writes the footers back (reads into memory, writes
  once). Pure arithmetic — `core`/`superseded` and never-referenced facts are untouched, and it clamps at
  `archive-candidate` (it never archives; that's `archive-fact` + the agent's judgment). Python *or* Node at
  parity, with mirror tests; `--dry-run`; idempotent.
- **`memory-lint` check (9) `[stale-metadata]`** — flags a fact whose stored `tier` ≠ the tier recomputed
  from the reference log (i.e. steps 2–3 were skipped), excluding `core`/`superseded`/never-referenced. Both
  runtimes + mirror tests. This is what makes the skipped-re-tier gap *visible* on every lint run + CI.

### Changed
- **`REVIEW.md`** steps 2–3 now lead with `refresh-metadata` (the deterministic path; hand-editing 30
  footers is discouraged). **`ENABLE.md` §5i** installs **seven** built-ins. **`README` / `ADR` /
  `continuity`** built-in lists updated. `sync skill adapters` now writes 8 skills → 48 adapters.

## Version 4.25.0, 6/28/2026

> **`archive-fact` — a deterministic, safe archive-move helper (MINOR).** From a cross-vendor critique
> (Copilot / Gemini 3.1 Pro): "agent behaviors vary by vendor; the reliance on agent interpretation of
> `REVIEW.md` to safely mutate state is vulnerable to LLM regressions / file-editing precision — harden the
> memory-writing mechanism itself, perhaps a small CLI helper for safe writes." Spot-on, and it names our
> most-repeated bug: the `open(f,"w").write(open(f).read()+…)` truncate-before-read trap wiped a
> `version.md` stamp and then this repo's archive (50 facts → 6), once each. The v4.22.4 safeguard moved
> the rule from a personal note → shared doc; this is the logical next step — doc → **tool**.

### Added
- **`agent-skills/archive-fact/`** — the **6th** built-in (`provenance: agent-memory-builtin`). Executes
  `REVIEW.md` step 4's archive-move deterministically: given fact id(s) the agent has *decided* to retire, it
  extracts each block (the column-0 bullet through its `<!-- id: … -->` footer, whole), **appends** it to the
  quarter archive + `INDEX.md` (append-mode), and rewrites `continuity.md` without it (**read whole file into
  memory, write once** — truncation is structurally impossible). Python *or* Node at output parity, with
  mirror tests (`test_archive_fact.py` / `.mjs`). Guards (refuse, exit 1): id with no footer, id already
  archived, or a move that would empty continuity; the move is **all-or-nothing**. `--dry-run` to preview.
  Keeps the meaning/mechanics split intact (same as `memory-lint`): the **agent judges what to archive**;
  the helper performs the **move** safely — it never decides (`never-pick-a-winner`).

### Changed
- **`REVIEW.md`** step 4 now leads with `archive-fact` as the preferred path (manual append-mode / read-into-var
  stays the no-runtime fallback). **`ENABLE.md` §5i** installs **six** built-ins. **`README.md`** / **`ADR.md`** /
  `continuity.md` built-in lists updated. `sync skill adapters` now writes 7 skills → 42 adapters.

### Critique disposition (also from the same review)
- *Auto-fix, not just lint* — **declined for semantic decay** (auto-deciding what to archive violates
  `never-pick-a-winner`); the `REVIEW.md` ritual **is** the agent-driven fix, the v4.24.0 advisory triggers it,
  and `archive-fact` now makes the *move* deterministic. *Upgrade automation* — logged as a backlog thread
  (the mechanical steps could be scripted, but the rungs are semantic merges that must stay agent-judged;
  the chosen mitigation is deterministic guardrails like `memory-lint`).

## Version 4.24.0, 6/28/2026

> **Decay-policy retune + a review-cadence/size advisory in `memory-lint` (MINOR).** Grounded in
> real measurements across two enabled repos: this tool (121 sessions, continuity 490 lines / 24 facts
> *right after a clean review*) and a product repo (61 sessions, **585 lines / 41 facts, 0 archived** —
> the cadence review never fired in the field). Findings: (1) `continuity_max_lines: 300` was
> permanently-red on both (alert fatigue) and conflates non-decaying structural sections (Vision,
> Invariants, Key Decisions, Blueprint) with the decaying region; (2) there was **no count-based trigger**,
> though fact-count is the verbosity- and velocity-independent signal; (3) **nothing enforced the review
> cadence**, so a real repo silently accumulated; (4) `verify_invariants_every: 20` meant near-daily
> human re-confirms at burst velocity (10–20 sessions/day).

### Changed
- **`memory-lint` — new advisory check (8), both runtimes at parity + mirror tests (29 each).**
  `[review-overdue]` fires when `sessions_since_last_review ≥ review_every` (read from the `last_review`
  Project-State stamp; never reviewed ⇒ all sessions count). `[continuity-bloat]` fires when continuity
  holds more than `continuity_max_facts` decaying facts/threads, or more than `continuity_max_lines` lines.
  All **advisory (WARN)** — a review is a ritual, never a hard gate — but they ride every lint run + the CI
  floor, so a lapsed review can't hide. This is the keystone: parameters alone don't fix a review that
  never runs.
- **Decay-policy defaults retuned** (`templates/memory/decay-policy.md` + this repo's): `continuity_max_facts: 30`
  (NEW — primary lean signal), `continuity_max_lines: 300 → 600` (a mature layer sits ~450–600 when healthy),
  `verify_invariants_every: 20 → 40` (anti-fatigue). `working/active/archive_window` and `review_every`
  unchanged — they work; the bloat came from reviews not running, not from the windows.
- **Docs:** `REVIEW.md` size trigger (facts primary + the new lint advisories), `agent-skills/memory-lint/SKILL.md`
  (check 8), `AGENTS.md` (root + template) review-cadence note, `templates/.agent/schema.md` windows list.
  Skill *description* unchanged → adapters need no re-sync.

## Version 4.23.2, 6/28/2026

> **Context-hygiene guidance: keep state externalized so compaction is safe (PATCH).** From a maintainer
> exchange about multi-hour AI sessions. Two corrections to an initial "brain fog" framing: **(1)** the
> agent usually **can't compact itself** (compaction is user-invoked or a harness auto-compact), so the
> agent's reliable lever is *externalizing state*, not self-compacting; **(2)** "retrieval degrades over
> hours" is a judgment call — the **objective** health signal is **context-window utilization (tokens used
> vs. the model's limit)**, which the harness tracks and may auto-act on, while time and a felt "fog" are
> only proxies. `AGENTS.md` now teaches: write the session log + `continuity.md` at each natural seam
> (milestone, phase shift, before a topic pivot) **before** compaction; at a seam with high utilization,
> suggest compacting (or rely on auto-compact), never mid-task; re-verify specifics against live files
> after any compaction. Reinforces *why* the memory layer lives in files, not the chat buffer.

### Changed
- **`templates/AGENTS.md` + root `AGENTS.md`** — new "Long session? Keep state externalized so compaction is
  safe" block, placed as a corollary to lightweight mode (the session-log write is the seam). Vendor-neutral
  (`/compact` / auto-compact / fresh session). Doc-only, additive, no memory-file shape change; re-sync
  `templates/AGENTS.md` into targets on the `4.23.1 → 4.23.2` rung.

## Version 4.23.1, 6/28/2026

> **`last_harvest` marker for incremental harvests (PATCH).** From a cross-vendor test drive: mercury's
> agent ran `harvest-knowledge` correctly but had to **infer the harvest window** ("since enable") because
> nothing recorded *when the last harvest ran*. Add a `last_harvest` marker so each run scopes "docs changed
> since then" deterministically. Decided to keep it in **`continuity.md` Project State** (with `last_review`
> / `last_invariant_check` — same family: "when did this periodic memory ritual last run"), **not**
> `.agent/version.md` (the install manifest, a different concern).

### Changed
- **`templates/.agent/schema.md`** — Project State gains an optional **`last_harvest:` `YYYY-MM-DD | through
  <session-file>`** field (omitted until the first harvest).
- **`agent-skills/harvest-knowledge/SKILL.md`** — now **reads** `last_harvest` to scope the next run to
  docs changed since then (full first pass if absent), and **stamps** it on completion (even on a no-op
  run — "docs checked through here"). The harvest owns `last_harvest` as the review owns `last_review`. The
  check-existing-first guard still prevents duplicates, so a re-scan is always safe — `last_harvest` only
  *scopes* the read. `VERSION` → 4.23.1; re-synced on the `4.23.0 → 4.23.1` rung (skill description
  unchanged → adapters unchanged).

## Version 4.23.0, 6/28/2026

> **`harvest-knowledge` — on-demand knowledge harvest as a built-in skill (MINOR).** The curious harvest
> (v4.22.0, `ENABLE.md` Step 4b) seeds memory from the team's docs **once**, at enable. But a *living*
> repo's docs keep evolving, and there was no recurring way to fold new ADRs / design specs / decision-log
> entries into memory short of re-enabling. This adds a **5th built-in skill** that does exactly that, on
> demand — and moves "re-harvest" out of the Mode B upgrade path (it was a one-time backfill bolted onto a
> rung) into a proper, repeatable skill. The enable-time harvest stays a **fresh-enable** event.

### Added
- **`agent-skills/harvest-knowledge/`** — a no-code, agent-run built-in (`provenance: agent-memory-builtin`).
  Re-scans the repo's human-authored documentation (recursive `docs/` trees + root sweep for ADRs, decision
  logs, design specs, roadmaps, kanban — same net as Step 4b) and distills **durable** facts into the
  **neutral, shared** `memory/` layer **additively**: map-don't-mirror, check-existing-first so a re-run
  doesn't duplicate, conflicts → a `Contradiction` thread (`never-pick-a-winner`), genuine replacements →
  supersession, budget-with-disclosure → a `(knowledge-harvest)` Open Thread. Installed into every repo by
  `ENABLE.md` §5i (now **five** built-ins); added to the `upgrades-additive` managed-built-ins list.
  **Explicitly not a vendor `/init`:** `/init` does a deep *code* analysis and (re)writes/overwrites a
  *vendor* steering file; `harvest-knowledge` reads *human-authored knowledge*, writes *neutral shared
  memory*, and is *additive + repeatable* — borrow `/init`'s analysis muscle, but the output goes to
  `memory/`, never a vendor file.

### Changed
- **`UPGRADE.md`** — the `4.21.0 → 4.22.0` rung no longer offers an inline Mode B re-harvest; backfilling an
  already-enabled repo from docs is now the `harvest-knowledge` skill's job (run on demand). The
  enable-time harvest remains a fresh-enable event. `VERSION` → 4.23.0; the `4.22.4 → 4.23.0` rung installs
  the new built-in.

## Version 4.22.4, 6/28/2026

> **Safe-write safeguard in `REVIEW.md` (PATCH).** A truncate-before-read antipattern
> (`open(f,"w").write(open(f).read() + …)`) wiped this repo's archive during a review (50 facts → 6;
> caught by `memory-lint`, recovered from git). The lesson belonged in the **shared, committed protocol**
> (every contributor + every vendor's agent inherits it), not a per-machine personal note — so it's now a
> rule in the review ritual's **Safety** section.

### Changed
- **`REVIEW.md` → Safety** gains two rules: (1) **never truncate a memory file when scripting the move** —
  append with `>>` / append-mode for the archive + `INDEX.md`, read-into-a-variable-then-write for
  `continuity.md`; never `open(f,"w").write(open(f).read() + …)` (opening `"w"` truncates *before* the
  read). (2) **After any scripted memory mutation, run `memory-lint`** — it catches a truncation (count
  drops, links dangle), and git-tracked memory files recover via `git checkout HEAD -- <file>`. Installed
  verbatim into every enabled repo; re-synced on the `4.22.3 → 4.22.4` rung. `VERSION` → 4.22.4.

## Version 4.22.3, 6/27/2026

> **Tighten the post-commit session window: 2h → 30 min (PATCH).** v4.22.1 shipped a 2-hour
> active-session window, but the observed problem was follow-up stubs **minutes** apart, and 2h is long
> enough to wrongly conflate a *genuinely new* session that starts within 2h of the previous one's log
> (the hook would nudge "enrich the old log" for a new session). 30 minutes spans a working session's
> commit cadence — including a short test/think gap — while a real new session (a longer pause) still
> gets its own stub.

### Changed
- **`.githooks/post-commit`** — the active-session window default is now **30 minutes** (was 2h), and the
  override env var is **`AGENT_MEMORY_SESSION_WINDOW_MINUTES`** (integer minutes), replacing
  `AGENT_MEMORY_SESSION_WINDOW_HOURS`. The unit changed to minutes because BSD `date -v` rejects a
  fractional hour (`-v-0.5H`), so sub-hour windows need integer minutes; both runtimes stay supported
  (`date -v-30M` / `date -d "30 minutes ago"`). Re-validated (2 min & 25 min → suppress; 45 min & none →
  stub; custom override honored). `.githooks/README.md` + `docs/DESIGN-ritual-triggers.md` updated;
  `VERSION` → 4.22.3; re-copied into targets on the `4.22.2 → 4.22.3` rung.

## Version 4.22.2, 6/27/2026

> **Lightweight mode: one log per working *session*, not per commit (PATCH).** The agent-side mirror of
> v4.22.1. The lightweight-mode rule wrote a lite session log for *every* memory-neutral tracked-file
> change — so an agent making several small commits in one sitting produced a near-duplicate lite log per
> commit (the same clutter + decay session-count inflation the v4.22.1 hook fix addressed, but on the
> agent-behavior side). The agent has context the hook lacks — it *knows* it's the same working session —
> so it needs no time-window: it simply enriches the log it already wrote.

### Changed
- **`AGENTS.md` (root + `templates/`)** — the lightweight-mode "lite log" tier gains: *if you already wrote
  a session log earlier in **this** working session, a later **memory-neutral** commit should **enrich that
  existing log** (a one-line "also: …" note) rather than spawn another lite log — a burst of commits in one
  sitting is one session.* Explicitly preserves the existing model for **memory-relevant** work (distinct
  events still each get their own log, so a multi-task conversation may still yield several); the rule only
  stops *trivial* follow-on commits from minting near-duplicate lite logs that would also inflate the decay
  session-count. Wording-only — no file shape, skill, or script change. `VERSION` → 4.22.2; re-synced into
  targets on the `4.22.1 → 4.22.2` rung (re-copy `templates/AGENTS.md`).

## Version 4.22.1, 6/27/2026

> **post-commit auto-stub is now per *session*, not per *commit* (PATCH).** A downstream report
> (`mercury-composable`) found the hook's auto-stub fired on **every** work commit: its only de-dup guard
> checked for an *untracked* stub, so once the agent enriched and **committed** the session log, the next
> work commit found no waiting stub and wrote a **fresh** one. One long session produced ~6 near-identical
> lite logs (each with an extra `memory: session log …` commit), and — since the decay model counts session
> files — inflated `sessions_since_last_used`, so facts decayed ~N× too fast (ironic, given `memory-lint`
> exists to catch decay miscounts).

### Fixed
- **`.githooks/post-commit`** — the auto-stub now suppresses a new stub when a session log already exists
  **within an active-session window** (default **2h**; override `AGENT_MEMORY_SESSION_WINDOW_HOURS`),
  nudging the agent to **enrich that log** instead. Detection is by the newest session **filename**
  timestamp (immutable + **clone-safe** — `mtime` is reset by `git clone`/checkout, which would wrongly
  suppress stubs for hours after a clone), compared lexicographically against a window-ago stamp in the
  same `YYYY-MM-DD-HHMMSS` form. This subsumes the old untracked-stub guard (a fresh stub has a recent
  filename) and covers the just-committed case too. A genuinely **new** session (no log within the window)
  still gets a stub — the "no silent gap" guarantee holds. Net: **one enriched log per working session**,
  and the session-file count tracks sessions, not commits. Bash 3.2-compatible (BSD `date -v` with a GNU
  `date -d` fallback). `VERSION` → 4.22.1; re-copied into targets on the `4.22.0 → 4.22.1` rung.

## Version 4.22.0, 6/27/2026

> **Discovery, consent & merge-friendliness + `MERGE.md` (MINOR).** One release bundling four additive
> improvements developed iteratively in a single session (dev-numbered 4.22–4.25) and **consolidated into
> one version** per a new *"one version per release"* policy — `VERSION` and the upgrade ladder track
> *releases*, not per-feature dev iterations (granular history lives in the session logs + Open Threads).
> The work came from three real signals — a client enablement complaint, a teammate-concurrency review,
> and a GitHub Copilot review — and was hardened by a full **fresh-context review loop validated
> end-to-end by a different vendor**: Gemini 3.1 Pro critiqued the milestone *and* re-validated the
> applied fixes, proving the `second-opinion` → `apply-critique` pair cross-vendor on this very release.

### Added
- **Curious knowledge harvest at enable** (`ENABLE.md` Step 4b) — discovery now **recursively** descends
  every documentation tree (`docs/`, `doc/`, `wiki/`, `rfcs/`, `adr/`, … all subfolders) and sweeps repo +
  module roots for human-authored knowledge markdown (decision logs, ADRs, kanban/roadmap, architecture &
  design notes, CONTRIBUTING, RFCs), distilling the durable facts into memory (map-don't-mirror). Bounded
  by a read **budget with disclosure** — overflow is recorded as a `(knowledge-harvest)` Open Thread so
  nothing vanishes silently. From a client complaint: a canonical `docs/` tree was skipped entirely and a
  recursive re-ask still stopped at depth-1.
- **Fresh-enable advisory + discovery depth** (`ENABLE.md` Mode A) — a fresh enable now opens with a
  concise **exec summary of the protocol** (what it is, what it writes, what it leaves untouched, that it's
  committed + shared) and a `cancel` gate, for **informed consent** rather than a blind yes. It then offers
  a **discovery depth**: standard scan (default) or an **`/init`-depth deep analysis** — which borrows the
  *capability* of a vendor's built-in `/init` but writes findings into the **neutral** memory layer, never
  a vendor steering file. A **first enable session log** records the chosen depth.
- **`MERGE.md`** — a new installed, no-code, on-demand protocol for resolving a git merge/rebase conflict
  in `memory/`. Tiered + human-gated, enforcing the `never-pick-a-winner` invariant: classify the hunk →
  Tier-1 mechanical (additive → union/keep-both; scalar → take-later, deterministic) → Tier-2 semantic
  clash (**the AI never decides** — preserve both + raise a Contradiction; a supersession only on the
  human's explicit instruction) → `memory-lint` gate → **human approves the merge commit** (never
  auto-commit). Joins `DECAY`/`REVIEW`/`SKILLS` as a root protocol doc, read on demand.
- **`memory-lint` check 7** — a leftover VCS merge-conflict marker (`<<<<<<<` / `>>>>>>>` / diff3
  `|||||||`) in the **live top-level `memory/*.md`** files is now an **ERROR** (a bare `=======` line is
  exempt — it's a valid Markdown setext heading underline). `sessions/` and `archive/` are **excluded**
  (immutable/append narrative that legitimately *quotes* markers — e.g. a session log pasting a diff). Both
  runtimes at parity, with mirror tests.

### Changed
- **`continuity.md` merge-friendliness** — `status` is now spec'd as a **short current-state line, not a
  changelog** (`.agent/schema.md` + `AGENTS.md`): a single ~20 KB accreted `status` line was a
  merge-conflict hotspot for concurrent teammates and duplicated the upgrade ladder. A new schema section
  **"Concurrency & merge-friendliness"** documents the conventions (one fact per line; append-only sections
  → keep-both/union on conflict; scalar bumps → take-later; same-thread clash → human). This repo's own
  `status` line slimmed 19,828 → ~1,100 chars.
- **"One version per release" policy** added to `UPGRADE.md`'s versioning model — bump for a release event,
  not per feature; keep a single pending version while unreleased; magnitude = the largest change in the
  batch; consolidate working-tree bumps beyond `HEAD` before committing. (This release is the first to
  apply it: four dev-iterations → one v4.22.0.)
- **`upgrades-additive` invariant + ADR-0005** — added `sync-adapters` to the managed-built-ins example
  list (it became a tool-managed built-in in v4.18.0). Surfaced and applied during a maintainer
  **invariant re-verification** (all five core invariants + the Vision re-confirmed, none superseded).
- **`REVIEW.md` step 9** now codifies that archived ids go in the `## Memory Review` block, **never** under
  `## Memory References` (which re-arms the over-archival guard → false reactivation). **`.githooks/README.md`**
  documents that a feat/memory commit split trips the advisory hook on the code commit (expected/benign;
  prefer an atomic commit). `VERSION` → 4.22.0.

### Notes
- **Mostly operator-side** (`ENABLE.md`) plus the `memory-lint` skill and one new root doc (`MERGE.md`) —
  **no memory-file shape change**. The single `4.21.0 → 4.22.0` upgrade rung bundles all four features.
- A full **memory review** ran alongside this release (continuity 753 → 577 lines; 14 faded facts archived).

## Version 4.21.0, 6/26/2026

> **Google Antigravity (`agy`) skills adapter (MINOR).** Adds a **6th** skills adapter target,
> `.agents/skills/<name>/SKILL.md`. Antigravity — the successor to Gemini CLI — merged custom commands
> into the open **Agent Skills** standard and reads workspace skills from **`.agents/skills/`**, **not**
> the old `.gemini/commands/*.toml`. So on an enabled repo, `init.sh` faithfully populated the Gemini
> adapter, yet `agy` reported `/<command>` (e.g. `/memory-lint`) as **not found** — it never looks in
> `.gemini/commands`. The new adapter uses the same `SKILL.md` shape as the Claude/Kiro/Copilot adapters,
> so it is a one-line addition per runtime, no new format. The `.gemini/commands` TOML adapter **stays**
> for now so Gemini CLI keeps working through the transition. Found dogfooding `agy` on an enabled repo.

### Added
- **6th vendor adapter `.agents/skills/<name>/SKILL.md`** in all three sync-adapters runtimes
  (`sync-adapters.py` / `.mjs` / `.sh`, kept byte-for-byte equivalent — verified identical output): each
  now writes **six** adapters per skill and prunes orphaned `.agents/skills/` dirs by the shared pointer
  signature. `.agents/` added to the root and template `.gitignore` (regenerated, local-only).
- **Google Antigravity (`agy`)** added to the Mode C detection/migration table and the bootstrap-files
  table in `README.md` (reads `AGENTS.md` + `.agents/skills/`; Gemini CLI successor). Vendor adapter
  lists updated across `ENABLE.md`, `templates/AGENTS.md`, `templates/.agent/schema.md`, and the
  `sync-adapters` `SKILL.md` (five → six). `VERSION` → 4.21.0.

## Version 4.20.3, 6/24/2026

> **memory-lint catches an empty/malformed version manifest (PATCH).** Adds a deterministic
> `check_version_manifest` check (an **ERROR**) so a present-but-empty or malformed `.agent/version.md`
> is caught by the lint floor (CI + reviews + manual runs) instead of silently breaking Mode B upgrade
> detection. This closes the loop on the v4.20.1 bug: a truncating stamp one-liner emptied a target's
> `version.md`, which made an agent misread the repo's version — now that exact failure mode fails the
> lint rather than going unnoticed. A *missing* `version.md` stays valid (the pre-versioning baseline)
> and is **not** flagged.

### Added
- **`check_version_manifest`** in both `memory-lint.py` and `memory-lint.mjs` (byte-identical message,
  at parity) — wired into `main`'s error list; with mirror tests in `test_memory_lint.py` /
  `test_memory_lint.mjs` (empty → error, malformed → error, valid → ok, missing → ok). `SKILL.md`
  documents the new check. Re-copied into targets on the `4.20.2 → 4.20.3` rung. `VERSION` → 4.20.3.

## Version 4.20.2, 6/24/2026

> **Windows line-ending hardening (PATCH).** Adds a **`.gitattributes`** pinning `*.sh` and `.githooks/*`
> to **LF**, so Git for Windows (`core.autocrlf=true` by default) doesn't rewrite them to CRLF on checkout —
> which would break bash (`bad interpreter: /usr/bin/env bash^M`) and silently disable the hook + `init.sh`.
> From a Copilot Windows-feasibility check: the bootstrap works via Git Bash/WSL, but without this it was
> luck-of-the-default. Now robust on Windows.

### Added
- **`.gitattributes`** (root + `templates/`) — `*.sh text eol=lf`, `.githooks/* text eol=lf`. Installed /
  merged into targets additively (ENABLE Step 7b + a `4.20.1 → 4.20.2` rung), same discipline as the
  `.gitignore` block. `VERSION` → 4.20.2.

## Version 4.20.1, 6/24/2026

> **Self-init folded into `copilot-instructions.md` (PATCH).** A fresh-clone dogfood showed v4.20.0's
> self-init worked for **Claude Code** (which acts on `AGENTS.md`) but **not GitHub Copilot CLI** — its
> `start` is driven by `copilot-instructions.md`'s front-loaded read list, so it loaded memory and
> summarized without acting on the AGENTS.md self-init step (hook stayed inactive, adapters absent). Fix:
> put the first-run init **at the top of `copilot-instructions.md`** (the file Copilot reliably
> front-loads), as the first action — run `bash .githooks/init.sh` if `core.hooksPath` is unset / adapters
> absent, *before* summarizing. Improves Copilot's odds of self-initing; `bash .githooks/init.sh` remains
> the one-command fallback and CI remains the zero-config floor.

### Changed
- **`templates/.github/copilot-instructions.md`** — now leads with a first-run-init block. `VERSION` → 4.20.1.

## Version 4.20.0, 6/24/2026

> **First-run init for fresh clones (MINOR).** Closes the gap a Copilot fresh-clone dogfood exposed: the
> memory bootstrap self-initializes (the agent reads AGENTS.md/memory on its own), but a clone has the
> gitignored skill **adapters absent** and the git hook **unactivated** (git can't auto-run committed
> hooks on clone). That had meant a two-command manual setup. Now: **`.githooks/init.sh`** (one idempotent
> command — regenerate adapters + `git config core.hooksPath .githooks`) + an **`AGENTS.md` self-init
> note** so the agent does it on its first session. CI remains the zero-config floor regardless.

### Added
- **`.githooks/init.sh`** — one-command first-run init (sync adapters + activate the hook). Idempotent;
  not a git-hook name, so git never auto-runs it (run `bash .githooks/init.sh`). Committed executable (`100755`).

### Changed
- **`AGENTS.md` (root + template)** — first-session **self-init** note: run `bash .githooks/init.sh` if
  adapter dirs are empty / `core.hooksPath` is unset.
- **`.githooks/README.md`** — now leads with the one-command init.
- `UPGRADE.md` (rung + table), `docs/DESIGN-ritual-triggers.md`, `README`, `VERSION` → 4.20.0.

## Version 4.19.0, 6/24/2026

> **Vendor-neutral ritual triggers (MINOR).** The after-session ritual (session log, review, sync) no
> longer depends on the agent *self-triggering* — which failed in practice: client teams report it isn't
> followed through even with Claude, a Copilot-only team had no triggers at all, and the hook layer was
> opt-in, per-vendor, and didn't travel into targets. Enable now installs a committed, vendor-neutral
> **`.githooks/post-commit`** and a **CI floor**, and the **agent activates** the local hook — **zero
> manual user step** (the adoption constraint: any manual op is a barrier as the protocol gains traction
> and lands with untrained users). `no-build-step-agent-run` holds: git/CI invoke them in the user's env;
> the tool runs nothing. Design: `docs/DESIGN-ritual-triggers.md`.

### Added
- **`.githooks/post-commit`** (bash, advisory, never blocks) — after a commit: auto-stubs a session log
  when the commit did real work but carried none (capture; the thoughtful summary stays the agent's job —
  same split as `memory-lint`) and re-syncs adapters when a skill changed. Activated by
  `git config core.hooksPath .githooks` (the agent runs this at enable). Plus `.githooks/README.md`.
- **`.github/workflows/agent-memory.yml`** — the **CI floor**: runs `memory-lint` + an advisory
  session-log presence check on push/PR with **zero per-user setup** (the untrained-user-proof layer).
  Advisory by default; opt-in gate via `AGENT_MEMORY_STRICT=1`.
- **`docs/DESIGN-ritual-triggers.md`** — the design (layered: agent-primary + git-hook/CI net + optional
  vendor hooks; the capture/judgment split; the no-code reconciliation).

### Changed
- **`ENABLE.md`** — Step 6 installs `.githooks/` + the CI workflow and **activates** `core.hooksPath`
  (agent-run, no user step); Notes scope + the honest git-clone-activation limit (CI backstops).
- **`AGENTS.md` (root + template)** — the ritual note is now "reinforced, not just documented" + a
  **definition-of-done** framing (*a task that changed tracked files isn't done until its log exists*).
- **`docs/optional-ritual-hook.md`** — reframed: the vendor-neutral git-hook + CI are now installed and
  agent-activated; this doc is the *optional* per-vendor end-of-turn hooks + git pre-commit reminder.
- `UPGRADE.md` (rung + table), `README`, `VERSION` → 4.19.0.

### Honest limit
- Git **cannot** auto-run committed hooks on a fresh clone (security). So local hooks are
  **agent-activated** (no user step in the common path) and **CI is the always-on, zero-config backstop**.

## Version 4.18.0, 6/24/2026

> **`sync skill adapters` is now a runnable script (MINOR).** A new built-in **`sync-adapters`** skill
> ships a deterministic adapter-regeneration script (bash `sync-adapters.sh` + Node `sync-adapters.mjs`
> + Python `sync-adapters.py`, at three-way output parity; **bash needs no runtime install — preferred**). For each `agent-skills/<name>/SKILL.md` it
> (re)writes the five vendor adapters and prunes the orphans it generated (signature-guarded — never
> deletes a hand-authored vendor file). **Why:** dogfooding `~/sandbox/simple-proxy`, GitHub Copilot CLI
> (Gemini 3.1 Pro) read `SKILLS.md` and *still* couldn't run `sync skill adapters` — it was a prose
> recipe with no executable, so the agent hunted for a non-existent command (`node memory-lint.mjs sync
> skill adapters`, an `mcp-agent-memory` npm package, `npm run`, grep for functions) and flailed. A real
> script removes the ambiguity. Consistent with `no-build-step-agent-run` (same category as the
> `memory-lint` script — an optional helper the agent/vendor/CI invokes; the tool runs nothing itself).

### Added
- **`agent-skills/sync-adapters/`** — the built-in `sync-adapters` skill: `SKILL.md` + bundled
  `scripts/sync-adapters.sh` (**bash — no runtime install, preferred**), `sync-adapters.mjs` (Node ≥ 18),
  and `sync-adapters.py` (Python 3 stdlib) at **three-way byte-identical** output parity. `--dry-run`
  previews; prune is **signature-guarded** (never deletes a hand-authored vendor file). Installed into
  every enabled repo (ENABLE §5i). The bash runtime is from a Copilot finding — the script must run in a
  non-Node project (no `npm`/`npx`/`package.json`).
- **`SKILLS.md` documents a `delete a skill` operation** — remove the neutral source
  (`rm -rf agent-skills/<name>/`), run the sync script (it auto-prunes the orphaned adapters,
  signature-guarded), and mark the continuity id superseded (DECAY §9). From Copilot feedback: the delete
  path was undocumented and required manual adapter cleanup. The script never deletes `agent-skills/`
  itself — removing the committed source stays a deliberate, human-visible `rm`.

### Changed
- **`sync skill adapters` is now the script**, not a prose recipe — `SKILLS.md` (the operation +
  "Authoring a skill"), `ENABLE.md` (§5h closing step + §5i "all four" built-ins), and `UPGRADE.md`
  (standing sync + new `4.17.0 → 4.18.0` rung + version table) now *run* it. The adapter recipe remains
  as the format spec the script implements. `VERSION` → 4.18.0.
- **Built-ins are now four** (memory-lint, second-opinion, apply-critique, **sync-adapters**) in the
  current-state docs; historical rungs/changelog entries keep their period-accurate "three".

## Version 4.17.0, 6/24/2026

> **GitHub Copilot CLI skills adapter (MINOR).** Adds a **5th** vendor adapter target so a skill
> authored once in the neutral `agent-skills/` layer is natively discoverable by **GitHub Copilot
> CLI**. Copilot CLI follows the open Agent Skills standard (the same `SKILL.md` shape as the
> Claude/Kiro adapter) and discovers project skills under `.github/skills/<name>/SKILL.md`,
> auto-matching by `description` (and also accepting an explicit `/<name>`). Found dogfooding
> `~/sandbox/simple-proxy`: Copilot CLI could not find a skill that lived only in `agent-skills/`,
> because no `.github/skills/` adapter had been generated. Mirrors the v4.5.0 Kiro addition. **Cross-vendor validated 2026-06-24** by GitHub Copilot CLI
> (Gemini 3.1 Pro) in Agent mode: it authored a `greeting` skill, ran `sync skill adapters`, generated
> all **five** adapters, and recognized the `.github/skills/` adapter (after a session restart — Copilot
> loads adapters at init) — "behaves exactly as documented."

### Added
- **`.github/skills/<name>/SKILL.md` adapter** — `sync skill adapters` now writes **five** adapters
  (Claude / Gemini / Cursor / Kiro / Copilot). Recipe in `SKILLS.md`; same thin-pointer shape as the
  Claude/Kiro adapters.
- **Copilot skills in Mode C migration** — `MIGRATE.md` now detects and promotes Copilot project
  skills (`.github/skills/`, `.agents/skills/`) into `agent-skills/`, with adapters regenerated.
- **Optional GitHub Copilot CLI `sessionEnd` ritual hook** — `docs/optional-ritual-hook.md` documents
  a Copilot `sessionEnd` hook (the analog of the Claude `Stop` hook) that nudges the after-session
  ritual on a non-agentic vendor; advisory (echo, never blocks), **opt-in, not installed by `ENABLE.md`**
  (lives in repo-level `.github/hooks/` or user-level `~/.copilot/hooks/`). Addresses review point #4
  (manual session upkeep) by making a skipped ritual *visible*, not enforced.
- **Optional GitHub Copilot CLI `postToolUse` adapter auto-sync hook** — `docs/optional-ritual-hook.md`
  documents an opt-in hook that regenerates the Copilot `.github/skills/` adapter after a tool use, so
  authoring a skill no longer requires remembering to run `sync skill adapters` (from a real-vendor
  finding: agents don't reliably auto-sync). **Convenience-scoped:** Copilot adapter only, no prune,
  duplicates the recipe in bash (regenerate if the recipe changes), and `/restart` still loads it — the
  canonical path stays the agent-run `sync skill adapters`. The tool ships no sync *script* by design.

### Changed
- **`.gitignore` (template + this repo)** — `.github/skills/` is now ignored **path-scoped**. Unlike
  the other adapter dirs, `.github/` is *not* ignored wholesale: it holds the tracked
  `copilot-instructions.md` and `workflows/`. Only `.github/skills/` (the regenerated adapter) is ignored.
- **`templates/.github/copilot-instructions.md`** — now **front-loads the explicit `memory/` read
  list** (not just a pointer to `AGENTS.md`), states the **lightweight-mode logging rule** (log when
  tracked files change; read-only Ask/Plan sessions correctly write no log), plus points Copilot at
  the skills layer. Copilot's **Ask/Plan** modes don't reliably chase a pointer chain, so the steering
  file carries the read list directly — a deliberate, **Copilot-scoped** reversal of the thin-pointer /
  single-source-read-order convention (reliability over DRY; Claude/Gemini/Kiro keep their thin
  pointers since they proactively load `AGENTS.md`). (Copilot later confirmed it reads `memory/` in
  Ask/Plan and logs in Agent mode — fully lightweight-mode-conformant, so the steering wording avoids
  framing read-only no-log as a deficiency.)
- **Adapter lists** updated across living docs to include `.github/skills/`: `AGENTS.md` (root +
  template), `SKILLS.md`, `ENABLE.md` (Step 5h + the Step 8 completeness assertion now requires five
  adapters), `UPGRADE.md` (standing sync + new `4.16.1 → 4.17.0` rung + version table), `.agent/schema.md`,
  `README.md`, `docs/DESIGN-skills-layer.md`. `VERSION` → 4.17.0.
- **`SKILLS.md`** — `sync skill adapters` gains a **hot-reload caveat**: some runtimes load skill
  adapters only at startup (e.g. **GitHub Copilot CLI** parses `.github/skills/` on init), so a
  freshly-synced `/<name>` needs a session restart / skills rescan to appear mid-session. From the
  Copilot validation above.
- **Authoring convention strengthened** (`SKILLS.md` + `AGENTS.md` root/template) — "Authoring a skill"
  is now an explicit **3-step action** (write `agent-skills/<name>/SKILL.md` → run `sync skill adapters`
  → reload the runtime), because agents (incl. Copilot/Gemini) don't reliably auto-sync after writing
  the file. The tool can't force it mid-session (`no-build-step-agent-run`; auto-sync is guaranteed only
  at enable/upgrade per v4.12.0), so the instruction is now emphatic in both the on-demand `SKILLS.md`
  and the always-read `AGENTS.md`.

## Version 4.16.1, 6/23/2026

> **Session filename drift fix (PATCH).** Two independent gaps allowed agents to write
> date-only session filenames (`2026-06-23.md`) instead of timestamped ones
> (`2026-06-23-153401.md`): (1) the protocol said "Use `date -u` *or equivalent*",
> letting agents treat the context-injected `currentDate` (date-only) as equivalent;
> (2) `memory-lint` had no filename-format check, so drift was invisible until manual
> inspection. Fixed both: tightened protocol wording to an explicit prohibition, and
> added a `check_session_filenames` warning to both linters. Surfaced from drift in
> this session.

### Changed
- **`templates/AGENTS.md`** — Step 1 and checklist: "always run `date -u +%Y-%m-%d-%H%M%S`"
  replaces "or equivalent"; explicit warning against using `currentDate` from context.
- **`templates/.agent/schema.md`** — same prohibition in the session-naming paragraph.
- **`memory-lint.py` + `memory-lint.mjs`** — new `check_session_filenames` warning (check 5):
  flags `YYYY-MM-DD.md` sessions; exported from the Node module. Registered in `main()`
  for both runtimes. Tests added to both suites (3 cases each, Python + Node).

## Version 4.16.0, 6/23/2026

> **ADR default path aligned to industry convention (MINOR).** The optional Architecture
> Decision Record log default moves from `docs/ADR.md` to `docs/arch-decisions/ADR.md`,
> matching the wider convention of placing the ledger in a named subdirectory (purpose-signalling;
> leaves `docs/` root uncluttered). Surfaced from `mercury-composable` feedback — that project
> had already adopted `docs/arch-decisions/ADR.md` ahead of the default. Targets at the new path
> need no file move; targets at the old path rename on upgrade.

### Changed
- **`templates/.agent/schema.md`** — section header updated to `## docs/arch-decisions/ADR.md`
  and the one body reference to the path updated.
- **`templates/AGENTS.md`** — ADR path reference updated.
- **`AGENTS.md` (root)** — ADR path reference updated.
- **`DECAY.md` §12** — *Design* primitive path reference updated.
- **`README.md`** — file-tree entry updated; new version-table row.
- **`UPGRADE.md`** — new `4.15.0 → 4.16.0` rung + version-table row.
- **`docs/arch-decisions/ADR.md`** — this repo's own ADR log moved from `docs/ADR.md`
  (dogfooding the new default).

## Version 4.15.0, 6/22/2026

> **ADR log upkeep trigger (MINOR).** The optional `docs/ADR.md` log (4.14.0) could be *adopted*
> but had no cue to *evolve* — the per-session ritual covered continuity-fact supersession yet
> never said to maintain a linked ADR. This adds the missing trigger: once the log exists, a new
> durable architecture decision, or the supersession/invalidation of a continuity fact carrying an
> `(ADR-NNNN)` tag, **prompts a human-gated ledger update** (add a newer ADR; mark the old
> `Superseded`/`Deprecated`, never delete; keep `formalizes:` ↔ `(ADR-NNNN)` in sync). Surfaced
> dogfooding `mercury-composable`'s ADR opt-in.

### Changed
- **`AGENTS.md` (root + `templates/`)** — the ADR paragraph gains an "If the log exists, keep it
  alive" maintenance/supersession trigger (propose; human-gated).
- **`.agent/schema.md`** (`docs/ADR.md` section) — a new "When to maintain it" paragraph spelling
  out the on-demand-but-kept-in-sync lifecycle.
- **`DECAY.md` §12** — the *Design* primitive notes the ADR lifecycle is kept in sync with fact
  supersession.
- **`UPGRADE.md`** — new `4.14.1 → 4.15.0` rung (re-sync the guidance; **merge** into a
  repo-customized ADR note rather than overwrite) + version-table row.

## Version 4.14.1, 6/20/2026

> **Re-synced `AGENTS.md` source clarified (PATCH).** A cross-vendor dogfood (GitHub Copilot
> upgrading `mercury-composable` from v3.7.0 → v4.14.0) re-synced the target's `AGENTS.md` from the
> tool's **root** `AGENTS.md` — the operator/dual-mode dispatcher — instead of `templates/AGENTS.md`,
> leaving the target presenting itself as an enablement tool and referencing the non-installed
> `ENABLE.md`. The other synced docs were correct; only `AGENTS.md` has a different canonical source
> for a target, and the upgrade ladder didn't say so per-file.

### Changed
- **`UPGRADE.md` gains a "Source of truth for re-synced files" section** — a per-file map: a target's
  `AGENTS.md` comes from **`templates/AGENTS.md`** (the memory hub); `DECAY.md`/`REVIEW.md`/`SKILLS.md`
  from the tool **root**; `.agent/schema.md` + bootstrap pointers from `templates/`. Explicit warning
  that the tool's **root** `AGENTS.md` (which references `ENABLE.md`/`MIGRATE.md`/`UPGRADE.md`) must
  **never** be installed into a target, plus a grep self-check ("AI-Enable Another Repository").
- **New `4.14.0 → 4.14.1` rung** that **verifies and repairs** a mis-synced `AGENTS.md` (re-copies
  from `templates/AGENTS.md` if the target's copy looks operator-sourced).

### Notes
- `UPGRADE.md` is tool-operator-only — **no target memory-file shape change**; `ENABLE.md` (fresh
  enable) was already explicit and unaffected. Purely an upgrade-path clarity + self-heal fix.

## Version 4.14.0, 6/20/2026

> **Optional Architecture Decision Record (ADR) log (MINOR).** The VBDI **Design** altitude was
> realized by the `## Architectural Invariants` / `## Key Decisions` in `continuity.md` and the
> long-form `docs/DESIGN-*.md`, but there was no atomic, dated, status-tracked, never-deleted record
> of an individual architecture decision *with its rationale*, browsable by a human IT-governance
> audience. This adds the well-established ADR practice (Nygard 2011) as a **lightweight, optional,
> human-facing** ledger — kept token-efficient by living under `docs/` and being read **on demand**,
> never in the per-session agent read path.

### Added
- **`docs/ADR.md`** (this tool's own, dogfooded) — a single-file decision log, entries **newest
  first**, each with **Status · Date · Abstract · Rationale (incl. consequences/trade-offs)** and
  `formalizes:` / `serves:` trace links. Status lifecycle `Proposed → Accepted → Superseded /
  Deprecated`; **nothing is ever deleted** (mirrors the memory layer's supersession model,
  `DECAY.md` §9). **Seeded with the 5 standing Architectural Invariants, plus the superseded
  `no-code-markdown-only` decision** (ADR-0001…0006 — `no-code-markdown-only` recorded as ADR-0004,
  *Superseded by ADR-0006*).
- **`.agent/schema.md`** documents the optional `docs/ADR.md` section (format + lifecycle +
  map-don't-duplicate cross-linking + the "on-demand, not per-session" rule).

### Changed
- `AGENTS.md` (root + template) and `DECAY.md` §12 note that the Design altitude *may* keep an
  optional `docs/ADR.md` log, explicitly **not** part of the Before-session read path.
- `docs/DESIGN-vbdi-lifecycle.md` §4 names the optional ADR log on the **Design** row.
- each `memory/continuity.md` Architectural Invariant title gains a visible `(ADR-NNNN)` pointer
  to its record (e.g. `Target-repo scope only (ADR-0001)`) — a **human cue**, explicitly **not** a
  prompt for the agent to open `docs/ADR.md`.

### Notes
- **Map, don't duplicate:** `continuity.md` keeps the live *what* (with `id`); the ADR carries the
  durable *why*. The constraint text is never restated as competing truth.
- **Not auto-installed.** ENABLE/UPGRADE *document* the convention; no `docs/ADR.md` is created in a
  target — a team adopts one on demand. Additive → no memory-file shape change.

## Version 4.13.0, 6/20/2026

> **Tool-provided (system) skills are marked + carry an upstream advisory (MINOR).** The built-ins
> agent-memory installs into every repo (`memory-lint`, `second-opinion`, `apply-critique`) are
> tool-managed copies — overwritten on upgrade — but nothing told a target's AI that *at edit time*, so
> a local change could be made (and stranded) without anyone realizing it should go back upstream. This
> is exactly what happened with the `memory-lint` dangling-link fix in `~/sandbox/simple-proxy`: it was
> a genuine fix, but the target session didn't surface it for back-port. (The existing
> warn-before-overwrite only fires during an upgrade, which that session never ran.)

### Added
- **`provenance: agent-memory-builtin` frontmatter marker** on the three shipped built-ins, plus a
  one-line banner in each `SKILL.md` body. Any vendor's agent can now recognize a system skill by
  reading the file — no out-of-band knowledge needed. (`hello-world` is a dogfood sample, never
  installed into targets, so it is not marked.)
- **Edit-time advisory** (`SKILLS.md` → new "Tool-provided (system) skills" section): before editing a
  skill, check its frontmatter; if it is `provenance: agent-memory-builtin`, don't edit in place —
  advise the human and either **fork** under a new name (local variant) or **upstream** a genuine fix to
  the agent-memory project for back-port + validation. **Production:** file an issue in the agent-memory
  repo. **Pre-release:** an advisory message to the maintainer (best effort until there's an issue
  tracker). The upstream pointer is kept **generic** (not a hard-coded URL) until the project's
  enterprise-GitHub move.
- **Upgrade-time backstop extended:** `ENABLE.md` §5i's warn-before-overwrite now also advises
  upstreaming a locally-modified built-in (not just keep-yours/take-update).

### Changed
- `.agent/schema.md` documents the optional `provenance` field; `AGENTS.md` (root + template) gains a
  one-line pointer; `docs/DESIGN-skills-layer.md` gains a status entry. `DECAY.md` / `REVIEW.md` and the
  adapter recipe are unchanged (adapters mirror only `name` + `description`, so the marker doesn't
  touch them). Lockstep: `VERSION` → 4.13.0, `UPGRADE.md` rung + table, `README`.

## Version 4.12.1, 6/20/2026

> **`memory-lint` dangling-link check resolves supersession targets across `memory/*.md` (PATCH).**
> `check_dangling` resolved `superseded-by` / `supersedes` links against footers from `continuity.md`
> + the archive only — so a fact superseded by one whose footer lives in another memory file (notably
> `vision.md`) was falsely flagged `[dangling] … which has no footer anywhere`. Found dogfooding on
> `~/sandbox/simple-proxy` (a retired vision was superseded by a `vision.md` fact); the maintainer
> fixed it there, and this ports the fix back to the tool with a regression test.

### Fixed
- **`load_repo` now also pools footers from other `memory/*.md` files** (e.g. `vision.md`), excluding
  `continuity.md` + `decay-policy.md`, into an `extra` set used **only** for supersession-link
  resolution in `check_dangling` — never counted as continuity/archive facts (counts, overdue, and
  over-archived checks are unchanged). Fixed identically in **both** `memory-lint.py` and
  `memory-lint.mjs` (code-point sort preserved → byte-identical output).
- **Regression test added to both suites** (`test_memory_lint.py` / `.mjs`): a continuity fact
  superseded by a `vision.md` fact must not warn, while a genuinely missing target still warns.
  Exercises `load_repo` end-to-end against a temp `memory/` layer (the bug site), not `check_dangling`
  alone. To enable it, `memory-lint.mjs` now also exports `load_repo` + `check_dangling` (the Python
  module already exposed them) — additive, no behavior change.
- Lockstep: `VERSION` → 4.12.1, `UPGRADE.md` rung + table, `README`. Verified: both suites 8/8;
  `memory-lint` parity byte-identical on the tool's own memory (0 errors, 0 warnings).

## Version 4.12.0, 6/19/2026

> **Enforced skill-adapter sync at enable + upgrade (MINOR).** Skill adapters are gitignored
> per-machine pointers, so they don't travel with a clone/pull, and a rung that adds a new adapter
> target (e.g. Kiro in 4.5.0) left older skills' adapters incomplete. Previously enable/upgrade only
> did a read-only **"recommend, don't run"** check, so after an upgrade a skill's vendor-native
> adapters could be missing — blocking subsequent work that relies on native auto-trigger until the
> user manually ran sync. Surfaced upgrading `~/sandbox/simple-proxy` (v4.4.0 → v4.11.1): the
> pre-existing `hello-world` skill was left without its Kiro adapter.

### Changed
- **ENABLE and every Mode B re-enable (upgrade or already-up-to-date) now *run* `sync skill
  adapters`** as their closing skills step, instead of recommending it. For each
  `agent-skills/<name>/` it (re)writes the four vendor adapters and prunes orphaned generated
  adapters. Safe to run unconditionally: it is **idempotent** and writes **only gitignored** files
  (never `agent-skills/`, never a committed file) — so it is not a version change and needs no session
  log. `no-build-step-agent-run` holds: the agent runs it during a human-invoked enable/upgrade, not a
  daemon or per-session automation. The per-session path still never touches skills; content-drift
  realignment is still the on-demand `skill sanity check`.
- **`ENABLE.md` Step 8 now *asserts* adapter completeness** (every skill has all four adapters, no
  orphans) — enforcement is checked, not convention.
- Touched: `UPGRADE.md` (standing "Skills adapter sync" section + 4.11.1 → 4.12.0 rung + version
  table; stale back-references in older rungs updated), `SKILLS.md`, `ENABLE.md` (Step 5h + Step 8),
  `docs/DESIGN-skills-layer.md`, `VERSION` → 4.12.0, `README`. `AGENTS.md` / `DECAY.md` / `REVIEW.md`
  unchanged.

## Version 4.11.1, 6/19/2026

> **Review step-6 archival guard hardened against prose (PATCH).** The `REVIEW.md` step-6
> archival-verify told the agent to grep recent session *files* for an about-to-be-archived id and
> keep it if found — but a raw full-text grep also matches a prior **review summary** that merely
> *names* the fact while recording its decay status. Because every review that defers a fact re-names
> it, the guard re-armed each cycle: an **archival livelock** (tracked as `ot-review-step6-prose`,
> same class as the v4.10.1 prose-vs-heading bug). Found during the 2026-06-19 review.

### Fixed
- **`REVIEW.md` step 6 now defines a "use" as a `## Memory References` entry, not a prose mention.**
  It makes `memory-lint` the preferred archival check (it counts Memory-References only, so it is
  immune to the trap), and scopes the by-hand fallback to hits **inside** a `## Memory References`
  block — explicitly ignoring `## Memory Review` / `## What happened` mentions. The verifier script
  itself needed no change (`memref_ids` was already line-anchored since v4.10.1); added
  `memref_ids` regression tests (prose/review-summary mention is not counted; block bounded at the
  next heading) to both `test_memory_lint.py` and `test_memory_lint.mjs`.

---

## Version 4.11.0, 6/19/2026

> **`memory-lint` gains a Node runtime (MINOR).** The deterministic decay-integrity check is the
> answer to "LLM hand-counting isn't reliable" — but that guarantee shouldn't depend on the machine
> having Python. `memory-lint` now ships in **both** Python and Node; on a node-only box you still get
> the script, not a hand count.

### Added
- **`memory-lint.mjs` — a Node port of the verifier** (Node ≥ 18, built-in modules only, no npm
  install), at **feature + output parity** with `memory-lint.py`. `SKILL.md` documents both commands
  as interchangeable; the agent runs whichever runtime the machine has (no dispatcher, no installer —
  the agent is the runtime). Verified byte-identical output (default and `--strict`) on this repo.
- **`test_memory_lint.mjs` — the cross-runtime contract.** Mirrors `test_memory_lint.py`'s fixtures
  exactly; both suites must pass, which is what holds the two implementations equivalent over time.

---

## Version 4.10.4, 6/18/2026

> **memory-lint nested list fix (PATCH).** Hardened the verifier script to handle deeply-nested lists correctly.

### Fixed
- **`memory-lint` pinned Open Threads:** Fixed a bug where `pinned_open_threads()` incorrectly reset its state on any standard list bullet, causing it to lose track of the "pinned" state if a parent Open Thread contained deeply nested sub-items. It now correctly checks indentation level. (tracked via `ot-memlint-pinned-nested`.)

---

---
## Version 4.10.3, 6/18/2026

> **Lightweight-mode wording fix (PATCH).** A loose end surfaced while running `sync skill adapters`:
> the sync (re)wrote 16 gitignored vendor adapters but left `git status` clean — yet `AGENTS.md`'s
> lightweight-mode note, read literally ("did a *file* change?"), seemed to demand a lite session log.
> It shouldn't: `SKILLS.md` already says the sync op "touches no committed file… not a version change,"
> and the note's own anchor is the git diff. The wording just didn't say *tracked*.

### Changed

1. **Lightweight-mode test re-keyed to a *tracked* change.** `AGENTS.md` (root + template) now states
   the objective test is the **git diff over tracked files**, not any filesystem write. The **Read-only**
   tier explicitly covers a run whose only writes are **gitignored, regenerated artifacts** —
   `sync skill adapters`, `review-scratch/` snapshots, the compiled lint artifact — as **no session
   log**. The middle tier reads "**A tracked file changed**…"; the closing line, "anything that touched
   a *tracked* file." Aligns the note with `SKILLS.md` (sync touches no committed file) and prevents a
   spurious lite log after every adapter sync. Wording-only — no file shape, skill, or script change.

Lockstep: `AGENTS.md` (root + template), `VERSION`→4.10.3, `UPGRADE.md` 4.10.2→4.10.3 rung + table,
`README` table. `SKILLS.md` / `DECAY.md` / `REVIEW.md` / `.agent/schema.md` unchanged.

---
## Version 4.10.2, 6/18/2026

> **Fresh-context-review critique fixes (PATCH).** The v4.10.x line was put through its own
> `second-opinion` ritual: a clean-vendor reviewer (GitHub Copilot CLI) challenged the milestone and
> returned a critique applied through the `apply-critique` loop. It confirmed the design was sound,
> cleared the `no-build-step-agent-run` question, and surfaced four scoped refinements — two
> documentation-consistency gaps that would have re-triggered the same review noise, one real parser
> robustness hole the v4.10.1 fix didn't cover, and one expectation-setting caveat.

### Fixed

1. **`memory-lint` — guard against an unclosed footer.** `FOOTER_RE` is now bound to a single line
   (`[^\n]`, no `re.S`). A malformed footer (`<!-- id: foo | ...` with no closing `-->`) can no longer
   let the non-greedy field capture span newlines and swallow the rest of the file up to a stray
   `-->`, which would have silently misparsed `tier`/`superseded` fields and corrupted decay counts
   with no error. Same lesson as v4.10.1: a verifier whose job is trustworthy counting must not be
   fooled by malformed input. Script-only; no description change → adapters unchanged.

### Changed

2. **Install protocol warns before overwriting a locally-modified built-in.** `ENABLE.md` §5i (and the
   `UPGRADE.md` 4.10.0 / 4.10.2 rungs) now say: before overwriting an already-installed tool-managed
   built-in, diff it against the source; if it was locally customized, **warn the human and let them
   decide** rather than silently discarding their change. Makes the tool-managed-copies contract a
   *checked* step, not convention-only. Agent-run at the human's direction (`no-build-step-agent-run`);
   a no-op on a fresh enable.
3. **`upgrades-additive` invariant text carries its exception inline.** The invariant in this repo's
   `memory/continuity.md` now states the tool-managed-built-ins carve-out at its declaration (it was
   only in ENABLE/UPGRADE prose), so a reader encountering it cold no longer re-flags the overwrite as
   a contradiction — the exact noise the dogfood reviewer raised.
4. **`second-opinion` — same-vendor vs. different-vendor caveat.** A *Notes* bullet now states that a
   same-vendor clean session (or spawned subagent) tests the **mechanism**, while a **different vendor**
   adds the **epistemic diversity** that is the whole point of a fresh reviewer for high-stakes
   milestones. Body only — description unchanged → adapters unchanged.

> Deferred (reviewer rated low-confidence/contrived): hardening `pinned_open_threads` against deeply
> nested lists — tracked as an Open Thread, not changed, since current session-log formatting is flat.

---
## Version 4.10.1, 6/18/2026

> **`memory-lint` bug fix — line-anchor the Memory-References detection (PATCH).** Found while
> *running* the verifier during a memory review: a first pass false-positived
> `[over-archived] sync-adapters-v420`. The review's own session log quoted the heading string
> "## Memory References" in its prose (describing the very check), and the script's un-anchored
> `find()` matched that inline mention before the real section — scooping the neighbouring
> `## What happened` paragraph (which named the archived id) in as the references block. The
> archival was in fact correct. A verifier whose whole job (v4.9.0) is trustworthy decay-counting
> must not be fooled by prose, so this anchors the heading match to the start of a line.

### Fixed

1. **`agent-skills/memory-lint/scripts/memory-lint.py` — `memref_ids()` now anchors the heading**
   to a real line (`(?m)^## +Memory References[ \t]*$`) and bounds the block at the next
   line-anchored heading, instead of `text.find("## Memory References")`. A session log may now
   safely quote the heading inline without producing a false `over-archived` error. Verified with
   added cases: the false-positive is gone, genuine references in the real section are still
   detected, and block-bounding still stops at the next heading. No description change → adapters
   unchanged; the tool still never runs it (`no-build-step-agent-run`).
2. **Ignore Python bytecode caches** — `.gitignore` and `templates/.gitignore` now ignore
   `__pycache__/` + `*.py[cod]`. The bundled `memory-lint` helper generates these on run (in this
   repo *and* in every enabled target as of v4.10.0); the `.py` source under `agent-skills/` stays
   tracked. Add-only, consistent with the v3.1.0 `.gitignore` propagation.

---
## Version 4.10.0, 6/18/2026

> **Fresh-context second opinion — a clean-memory reviewer as a deliberate gate.** A long
> session accumulates self-trust; the agent that built a solution over-trusts its own
> trajectory. This release adds a skill pair for the highest-value antidote: at a
> milestone or risk point, hand a compact snapshot to an AI with **clean memory** (a fresh
> session or a different vendor) and ask it to challenge the work. It folds an external
> brainstorming idea (the "Agent Interchange Format" draft) into the existing **skills layer +
> VBDI** rather than a standalone spec — the net-new surface is small: a **security advisory**
> on export, the handoff ritual, and the critique shape. Everything else reuses `continuity.md`
> + session logs, the VBDI human gate, and `memory-lint`/build-tests. It carries the hard-won
> v4.8/v4.9 lesson in its bones: **the fresh reviewer is a hypothesis generator, not an
> authority** (a clean-context reviewer once over-archived still-referenced facts here), so
> critique is advisory and gated by deterministic checks + a human.

### Added

1. **`agent-skills/second-opinion/`** — generates a review snapshot **derived from**
   `continuity.md` + recent session logs (decision-relevant deltas only — never a parallel
   committed state file), behind a **security advisory** the human must acknowledge before any
   state is exported. Supports *milestone* mode (challenge a done-looking milestone) and
   *reactive* mode (blocked / uncertain / risky). Writes to gitignored `review-scratch/`.
2. **`agent-skills/apply-critique/`** — consumes the reviewer's critique through a **bounded,
   validated, human-gated** loop: parse → plan a few scoped fixes → apply → validate
   (build/tests + `memory-lint` if memory changed) → summarize applied vs. rejected. Conflicts
   become Open Threads (`never-pick-a-winner`); the cycle writes a normal session log.
3. **`review-scratch/`** — a gitignored, per-machine scratch dir for snapshots/critiques, with
   a README marking the files personal. Sharing one is a conscious human decision. Added to the
   root and `templates/.gitignore`; documented in `.agent/schema.md`.

### Changed

1. **Built-in skills now installed (`ENABLE.md` Step 5i + the 4.10.0 upgrade rung).** Every
   enabled repo gets the built-in skills — `second-opinion` + `apply-critique` **and
   `memory-lint`** — copied into `agent-skills/` with adapters regenerated; `review-scratch/`
   added to the target `.gitignore`. `memory-lint` is installed too because the **review ritual
   relies on it** — this supersedes its v4.9.0 "tool-local / not auto-installed" stance. Install
   is idempotent and never touches unrelated `agent-skills/` content; a fresh Mode A enable now
   creates a populated (never empty) `agent-skills/`. Report + scope + verify notes updated.
2. `VERSION` → 4.10.0; `UPGRADE.md` 4.9.0→4.10.0 rung + table; `README` version table.
   `AGENTS.md` / `SKILLS.md` / `DECAY.md` / `REVIEW.md` unchanged — the critique→repair loop
   reuses the existing ritual. Design: `docs/DESIGN-fresh-context-review.md`.

---
## Version 4.9.0, 6/18/2026

> **`memory-lint` — a deterministic verifier skill (move the decay arithmetic off the LLM).**
> v4.8.0 added a markdown self-verify step, but the *primary* count was still hand-done — and an
> LLM (Copilot, then a hand re-check) miscounts. This release ships the stronger fix Copilot
> argued for: a portable, optional **`memory-lint`** skill whose bundled script *deterministically*
> checks memory integrity. The agent judges meaning; the script does the counting. **On its very
> first run it caught a real over-archival that two rounds of human review had missed**
> (`skills-layer-v411-fixes`, last referenced 16 sessions ago ≤ archive_window 20) — now reactivated.

### Added

1. **`agent-skills/memory-lint/`** — a portable skill (neutral `SKILL.md` + `scripts/memory-lint.py`,
   Python 3 stdlib, no install). Deterministic checks: no id in both `continuity.md` and the archive;
   no archived-as-faded fact referenced within `archive_window` (the decay-miscount guard); advisory
   overdue-for-archival (excluding `core` / `superseded` / pinned `- [ ]` threads); supersession links
   resolve. Exit non-zero on error → wire to a pre-commit hook / CI. Optional and agent/human-invoked
   (`no-build-step-agent-run` — the tool never runs it); it lints the *arithmetic*, not the *meaning*.

### Changed

1. `REVIEW.md` step 6 ("Verify archival") now points to `memory-lint` as the recommended
   deterministic version of the check ("let the script count"). `VERSION` → 4.9.0; `UPGRADE.md`
   4.8.0→4.9.0 rung + table; `README`. `AGENTS.md` / `SKILLS.md` / `DECAY.md` unchanged.

### Fixed

1. **Reactivated `skills-layer-v411-fixes`** — `memory-lint` flagged it as over-archived by the
   2026-06-18 Copilot review (sslu 16 ≤ archive_window 20); moved back to `continuity.md` (`active`).

---
## Version 4.8.0, 6/18/2026

> **Review self-verify guard — catch decay miscounts before they archive.** A GitHub Copilot CLI
> review (2026-06-18) over-archived three recent, active facts — it miscomputed
> `sessions_since_last_used` (counted ~5–9 as ">20") and ignored its own "still referenced in
> review window" note. The decay *rule* was right; what was missing was a check that the count was.
> Counting session files by hand is the easiest review step to get wrong, and archival is the
> costliest error — so the review now verifies its own archival against a cheap, grep-able signal.

### Added

1. **"Verify archival" step in `REVIEW.md`** (new step 6, before stamping): for each fact about to
   be archived as *faded*, `grep` the last `archive_window` session files for its id — **any hit
   means the count was wrong, so keep the fact** (it's `active`/`archive-candidate`), don't archive.
   Then confirm **no id lives in both `continuity.md` and the archive**. Superseded facts are exempt
   (they archive on truth-state, not recency). Added an `Archive-verify:` line to the review-summary
   format. Pure markdown; replaces a hand-counted judgment with a checkable signal for the riskiest
   operation.

### Changed

1. `VERSION` → 4.8.0; `UPGRADE.md` 4.7.1→4.8.0 rung (re-sync `REVIEW.md`) + table; `README`.
   `AGENTS.md` / `SKILLS.md` / `DECAY.md` unchanged.

---
## Version 4.7.1, 6/17/2026

> **Lightweight mode — sharpen the skip criterion to an *objective* test.** v4.7.0 let any
> "memory-neutral" task drop to a lite log. But **"trivial" is a judgment call — both AI and human
> misjudge it**, and a misjudged change that actually mattered would slip out of the ledger. So the
> distinction is now keyed to the **objective question "did a file change?"**, not a subjective
> "is this trivial?":
> - **Read-only** (no file changes — orientation, Q&A, exploration) → **no session log**.
> - **Any file change, however small** (a one-line fix, a typo) with no memory-relevant event →
>   a **one-line "lite" session log** (never skipped on a "felt trivial" call; the git diff anchors it).
> - **Memory-relevant event** → the full ritual.

### Changed

1. `AGENTS.md` (root + template) "Lightweight mode" note rewritten to the three-tier,
   file-change-keyed form above. `VERSION` → 4.7.1; `UPGRADE.md` 4.7.0→4.7.1 rung + table; `README`.
   `SKILLS.md` / `DECAY.md` / `REVIEW.md` unchanged.

---
## Version 4.7.0, 6/17/2026

> **Lightweight mode — scale the ceremony to the memory impact.** From a real cross-vendor
> enablement: **Kiro** used the installed tool to AI-enable a new source-code repo and gave an
> honest assessment — the protocol "helps more than it interferes" (immediate orientation from
> `memory/`, actionable `SKILLS.md`, real multi-agent-continuity value), but the **per-session write
> ceremony is disproportionate for trivial tasks** ("for a two-line script and a skill file, the
> protocol's weight is noticeable") and "could benefit from a lightweight mode." This release adds
> exactly that — without breaking the event-sourced ledger.

### Added

1. **Lightweight mode (memory-neutral tasks)** in `AGENTS.md` (root + template), in "After Every
   Session": if a task produced **no memory-relevant event** (no new/changed fact, no decision, no
   Open Thread touched, no project-state change), write a **one-line "lite" session log**
   (persist-time filename + `**Agent:**` + a *lightweight*-marked summary + `## Memory References` →
   `(none)`) and **skip** the full template, fact-footer bookkeeping, and continuity edits. The
   **ledger stays continuous** (every session still logged), so multi-agent continuity is preserved;
   the review counts a lite log like any session but it carries no references, so usage is
   unaffected. When unsure, write the full log; Vision/Blueprint/invariant/supersession changes are
   never memory-neutral. **`DECAY.md` / `REVIEW.md` need no change** — a lite log is just a session
   file with no `## Memory References`.

### Changed

1. `VERSION` → 4.7.0; `UPGRADE.md` 4.6.0→4.7.0 rung (re-sync `AGENTS.md`) + table; `README`.
   `SKILLS.md` / `DECAY.md` / `REVIEW.md` unchanged.

---
## Version 4.6.0, 6/17/2026

> **Vendor-neutral commit attribution — encode the convention once, every vendor follows.** A
> Kiro observation crystallized it: Claude Code adds a deliberate, human-gated `Co-Authored-By:`
> trailer *automatically* (it's in its harness), Kiro needed a per-machine **hook + steering** to
> do the same, and Gemini/Cursor do nothing by default. That's exactly the gap the shared layer
> closes — so `AGENTS.md` now extends its existing **"identify yourself"** principle (already true
> for session logs) to **commits**: any vendor's agent gets Claude's behavior with **no per-vendor
> hook**. Serves multi-contributor traceability (`bp-multi-user`) + provenance.

### Added

1. **Commit-attribution convention** in `AGENTS.md` (root + template), in the "After Every
   Session" step 4 + checklist: *"Commits are deliberate and human-initiated. When you commit at
   the human's direction, identify yourself the same way you do in session logs — e.g. a
   `Co-Authored-By: <your agent name>` trailer — so authorship is traceable across vendors. (If
   your runtime already adds one, nothing to do.)"* Soft by design — guides, doesn't prescribe git
   workflow; a no-op for runtimes (like Claude Code) that already do it.

### Changed

1. `VERSION` → 4.6.0; `UPGRADE.md` 4.5.2→4.6.0 rung (re-sync `AGENTS.md`) + table; `README`.
   `SKILLS.md` / `DECAY.md` / `REVIEW.md` unchanged.

---
## Version 4.5.2, 6/17/2026

> **Kiro hooks in Mode C + a bootstrap edge-case note — from a Windows/Kiro enable.** Cloning an
> agent-memory repo on a fresh machine and opening it in an **enterprise Kiro** surfaced two things:
> (1) `.kiro/` doesn't exist on a fresh clone (gitignored, per-machine), and an enterprise IDE may
> **self-bootstrap from its own onboarding/MCP before reading `AGENTS.md`** — the fix is the human
> nudge *"Start from `AGENTS.md`"*; and (2) once Kiro is running it deposits **hooks** and steering
> into `.kiro/` (e.g. a commit-signature hook). Those stay gitignored/per-machine and don't touch
> the shared `memory/` layer, but the migration protocol didn't cover hooks for *other* repos being
> enabled. (The Kiro commit hook is **human-gated** — it fires only when the human says "commit" and
> adds a co-author trailer — so it *aligns* with agent-memory's deliberate-commit model; no tension.)

### Changed

1. **`MIGRATE.md`** — the Kiro per-vendor protocol gains a **Hooks** sub-case:
   `.kiro/hooks/*.kiro.hook` are **preserved verbatim under `legacy/kiro/hooks/`, never converted
   or run** (automation is a human, gated decision). **Human-gated** commit hooks (like Kiro's,
   triggered by the human saying "commit") align with agent-memory and need no action; only a hook
   that commits or pushes **unprompted** is surfaced as an Open Thread (`never-pick-a-winner`).
2. **`README.md`** — a bootstrap **edge-case note**: on a fresh clone the vendor dirs are
   gitignored, so an enterprise IDE may self-bootstrap first; tell the agent *"Start from
   `AGENTS.md`"*, then run `sync skill adapters`. Enterprise hooks/steering in `.kiro/` stay
   gitignored and per-machine.
3. `VERSION` → 4.5.2; `UPGRADE.md` 4.5.1→4.5.2 rung + table. `AGENTS.md` / `SKILLS.md` /
   `DECAY.md` / `REVIEW.md` unchanged.

---
## Version 4.5.1, 6/17/2026

> **Skills-layer guidance — from a cross-machine Gemini CLI dogfood.** A real Gemini CLI run
> (different machine) surfaced two rough edges, both wording/guidance, no shape change:
> (1) after `sync`, a natural-language "run hello-world" kept reading `agent-skills/` instead of
> the freshly-generated `.gemini/commands/` command; (2) the agent told the user to **commit** the
> vendor adapter dirs. Root causes: Gemini custom commands are **slash commands** (`/<name>`,
> explicit) — *not* natural-language auto-triggers like Claude/Cursor/Kiro — so NL correctly
> routes through the `AGENTS.md` baseline to the **same** neutral skill (identical result, not a
> defect); and our docs stated adapters are gitignored but never explicitly said *don't commit /
> recommend committing them*.

### Changed

1. **`SKILLS.md`** — the Gemini adapter is now documented as a **slash command `/<name>`**
   (explicit, not NL-matched); added a "trigger semantics differ per vendor" note (Claude /
   Cursor / Kiro are description-matched, Gemini is slash-invoked, all pointing to the same
   neutral skill); and a **never-commit-the-adapters** guard on the `sync skill adapters`
   operation (report adapters as "gitignored — do not commit; only `agent-skills/` is shared").
2. **`AGENTS.md`** (root + template) — the adapter line now says **"never commit them"**.
3. **`docs/DESIGN-skills-layer.md`** — recipe table flags Gemini as slash-invoked; a trigger-
   semantics + commit-guard note under the table; status line. `VERSION` → 4.5.1; `UPGRADE.md`
   4.5.0→4.5.1 rung + table; `README`. `DECAY.md` / `REVIEW.md` unchanged.

---
## Version 4.5.0, 6/16/2026

> **Kiro support — convergence on open standards.** Amazon's Kiro IDE adopts the two open
> standards this tool already bets on: it auto-reads a root **`AGENTS.md`** (so the memory
> layer works with no pointer file) and its Agent Skills follow the **open Agent Skills
> standard** (the same `SKILL.md` shape as Claude). So enabling a Kiro repo needs almost
> nothing new — this release adds a 4th skills **adapter** target and teaches Mode C to
> detect/migrate Kiro's repo-local artifacts. **Kiro Powers need no special handling**: they
> are partner-published bundles (MCP + steering + hooks) that *consume* open-standard skills,
> which ours already are — the tool never emits a Power.

### Added

1. **Kiro skills adapter** (`SKILLS.md` recipe): a 4th target `.kiro/skills/<name>/SKILL.md` —
   identical shape to the Claude adapter (frontmatter `name` + `description` + a pointer body),
   since Kiro follows the open Agent Skills standard. `sync skill adapters` now writes four
   adapters; the standing read-only **Skills adapter check** (`UPGRADE.md`) now scans for it too.
2. **Kiro in the Mode C detection table** (`MIGRATE.md`) + a per-vendor **Kiro** protocol:
   `.kiro/steering/*.md` → `memory/instructions.md`; `.kiro/skills/` → promoted to
   `agent-skills/` (open-standard, same as Claude); `.kiro/specs/` preserved verbatim under
   `legacy/kiro/specs/` (never auto-flattened — folding a spec into the Vision/Blueprint is a
   human, altitude-gated decision).

### Changed

1. Adapter lists across the living docs now include `.kiro/skills/` (`AGENTS.md` root + template,
   `ENABLE.md` Step 5h / Step 8 / scope, `docs/DESIGN-skills-layer.md` recipe table + Option A).
   `.gitignore` needs no change — `.kiro/` was already in the managed block; the comment now
   names `.kiro/skills/` among the adapters. `VERSION` → 4.5.0; `UPGRADE.md` 4.4.0→4.5.0 rung +
   table; `README`. `DECAY.md` / `REVIEW.md` unchanged.

---
## Version 4.4.0, 6/16/2026

> **Lightweight skills — conscious, not per-session.** Skill creation is a deliberate,
> occasional developer action, so it leaves the per-session path. The per-session `AGENTS.md`
> now carries only the **runtime baseline** (read & follow a matching skill) + a pointer; the
> adapter recipe and the **sync** / **adopt** / **sanity-check** operations move to a new
> on-demand **`SKILLS.md`** (installed like `DECAY.md`/`REVIEW.md`). The v4.3.0 per-session
> "skills safety check" is **removed**; upgrades instead do a read-only filename check that
> *recommends* `sync skill adapters` if an adapter is missing/orphaned. Trims the per-session
> bootstrap (the skills recipe was ~1.3K tokens read every session).

### Added

1. **`SKILLS.md`** (installed at repo root) — the on-demand skills reference: authoring
   convention, adapter recipe, and the `sync` / `adopt` / `skill sanity check` operations.
2. **Standing "Skills adapter check"** in `UPGRADE.md` — read-only, filename-only; runs on any
   Mode B re-enable (incl. "up to date") and *recommends* sync if adapters are missing/orphaned.

### Removed

1. The per-session **"Skills safety check"** step from "After Every Session" (both `AGENTS.md`
   files) + its checklist line — superseded by the on-demand + upgrade-time model.

### Changed

1. `AGENTS.md` (root + template): "Skills" reduced to the runtime baseline + a pointer to
   `SKILLS.md`. `ENABLE.md` (Step 5h references `SKILLS.md`; Step 6 installs it; Step 8 verifies),
   `MIGRATE.md`, `.agent/schema.md` now point at `SKILLS.md`. `VERSION` → 4.4.0; `UPGRADE.md`
   4.3.3→4.4.0 rung + standing check + table; `README`. `DECAY.md` / `REVIEW.md` unchanged.

---
## Version 4.3.3, 6/16/2026

> **Skill description guidance** (reviewed from external feedback). A `description` is a
> model-matched activation signal read within a small discovery budget, so it should be a
> **concise, trigger-phrase-rich summary** — not a long abstract paragraph (which weakens
> activation). Also clarified that YAML `>`/`|` folded/literal blocks are YAML-only and don't
> carry into the TOML adapter, so the canonical value stays one logical line. Wording only.

### Changed

1. `AGENTS.md` "Authoring a skill" asks for a concise (~1–2 sentence), trigger-rich
   `description`; the recipe notes the `>`/`|` YAML-only caveat.
2. Tightened the dogfood `hello-world` description (~35 words) and regenerated its adapters.

`VERSION` → 4.3.3; `UPGRADE.md` 4.3.2→4.3.3 rung + table; `README`; `docs/DESIGN-skills-layer.md`
§9 note. `DECAY.md` / `REVIEW.md` unchanged.

---
## Version 4.3.2, 6/16/2026

> **Skill description hardening**, surfaced by a deliberate skill-lifecycle sanity check
> (dogfood). The check confirmed the mechanics (git split / pointer integrity / per-vendor
> format / adopt / prune all correct) but found two **hard-to-spot** `description` hazards.
> Wording/clarity only — no shape, data, or behavior change.

### Changed

1. **Adapter `description` mirrors the neutral skill's verbatim** — never abbreviate it (the
   prior hand-made `hello-world` adapters had abbreviated descriptions that silently drifted
   from the skill).
2. **Skill descriptions must be single-line and quote-free** — a `description` containing a
   `"` would otherwise emit invalid TOML (Gemini) or `.mdc`/YAML frontmatter (Cursor) when
   synced. The recipe adds an escape/quote fallback for unavoidable cases.
3. Fixed the dogfooded `hello-world` skill's description (dropped inner quotes) and regenerated
   its adapters to mirror it.

`VERSION` → 4.3.2; `UPGRADE.md` 4.3.1→4.3.2 rung + table; `README`. `templates/AGENTS.md`
(+ root `AGENTS.md`) re-synced; `docs/DESIGN-skills-layer.md` §9 note; `DECAY.md` / `REVIEW.md`
unchanged.

---
## Version 4.3.1, 6/16/2026

> **Skills-layer doc fixes**, surfaced by a fresh-agent test-drive of the v4.3.0 session-close
> ritual (dogfooded on a real target). Wording/clarity only — no shape, data, or behavior change.

### Changed

1. **"Adopt a skill" no longer instructs a mid-ritual commit** — it conflicted with the
   session-close ritual (which only *reminds* to commit). Adopt now says to stage the neutral
   skill for the session-end commit; the agent doesn't self-commit mid-ritual.
2. **Session-close skills check** notes that adoption (which changes the tree) should run
   **before** writing the session log, so the log records it.
3. Clarified adopt **body normalization** (preserve the procedure, neutralize vendor phrasing)
   and the detection locations.

`VERSION` → 4.3.1; `UPGRADE.md` 4.3.0→4.3.1 rung + table; `README`. `templates/AGENTS.md`
re-synced; `DECAY.md` / `REVIEW.md` unchanged.

---
## Version 4.3.0, 6/16/2026

> **Skill authoring convention + "adopt skill" safety-net.** Closes a footgun in the skills
> layer: the source of truth is `agent-skills/<name>/SKILL.md`, but a user — or a vendor's
> built-in skill creator — might author a skill directly in a vendor folder (`.claude/skills/`,
> …), which is gitignored, so it's never shared and isn't the source of truth. v4.3.0 makes
> the authoring convention explicit and adds a reverse "adopt" operation, checked at session
> close. Additive (docs/protocol only).

### Added

1. **Authoring convention** (`AGENTS.md` "Skills" → "Authoring a skill"): create skills in
   `agent-skills/<name>/SKILL.md`, then "sync skill adapters"; never author in a vendor folder.
2. **"Adopt a skill" operation** (`AGENTS.md` "Skills" → "Adopt a skill"): promote a skill
   authored natively in a vendor folder into `agent-skills/` (the reverse of sync — the same
   move migration makes at enable), then sync. The on-demand complement to migration's
   one-time promote.
3. **Session-close safety check**: the "After Every Session" ritual gains a step (+ checklist
   line) that detects a skill stranded in a vendor folder and prompts adoption before commit.

### Removed

N/A.

### Changed

1. `AGENTS.md` (root + template), `MIGRATE.md` (on-demand-adopt note), `.agent/schema.md`,
   `docs/DESIGN-skills-layer.md`. `VERSION` → 4.3.0; `UPGRADE.md` 4.2.0→4.3.0 rung + table;
   `README`. `DECAY.md` / `REVIEW.md` unchanged.

---
## Version 4.2.0, 6/16/2026

> **"Sync skill adapters."** Closes a gap surfaced by a real cross-machine test: the neutral
> `agent-skills/<name>/SKILL.md` travels via git, but the per-vendor adapters are gitignored
> and **don't travel** — so a freshly cloned/pulled repo has no native `/`-command /
> auto-trigger until they're regenerated locally, and re-running "AI enable" on an
> up-to-date repo is a no-op. v4.2.0 adds an on-demand operation to regenerate them, and
> moves the adapter recipe into the installed `AGENTS.md` so a target's own agent (any
> vendor) can self-sync. **Additive** (the runtime baseline always worked without adapters).

### Added

1. **"Sync skill adapters" operation** — for each `agent-skills/<name>/SKILL.md`, regenerate
   the Claude/Gemini/Cursor adapters (idempotent) and prune orphaned ones. Invoked by saying
   "sync skill adapters"; touches no committed file (adapters are gitignored).
2. **Canonical adapter recipe relocated** to the installed `AGENTS.md` "Skills" section, so a
   contributor's agent — on any vendor, on any machine — can self-sync by reading its own
   `AGENTS.md`. `ENABLE.md` Step 5h now references this single recipe (DRY).

### Removed

N/A.

### Changed

1. `AGENTS.md` (root + template): "Skills" section gains the adapter recipe + the sync
   operation. `ENABLE.md` Step 5h references the recipe instead of duplicating it.
   `.agent/schema.md` notes on-demand sync. `VERSION` → 4.2.0; `UPGRADE.md` 4.1.1→4.2.0 rung
   + version table; `README`. `DECAY.md` / `REVIEW.md` unchanged.

---
## Version 4.1.1, 6/16/2026

> **Skills-layer refinements** — pre-adoption corrections to v4.1.0 (which shipped the same
> day and was not yet consumed by any repo), so the first real target run starts clean. The
> adapter formats were verified against current vendor docs in the process.

### Changed

1. **Folder renamed `skills/` → `agent-skills/`.** `skills/` is a common top-level dir;
   `agent-skills/` is namespaced to avoid collision (and stays visible/discoverable, a peer
   to `memory/`). All living docs updated; vendor `.claude/skills/` references unchanged.
2. **Cursor adapter fixed.** `.cursor/rules/<name>.mdc` now emits the **agent-requested**
   rule type — `description` + empty `globs:` + `alwaysApply: false` — verified against
   current Cursor docs. (Gemini `.gemini/commands/*.toml` with `description`/`prompt`/
   `{{args}}`, and Claude `.claude/skills/<name>/SKILL.md`, were verified correct as shipped.)
3. **Collision guard.** Enable/migrate never overwrite a pre-existing `agent-skills/` — they
   raise a `Contradiction:` Open Thread (`never-pick-a-winner`) and stop.
4. **Vendor-dir double-duty clarified** (`MIGRATE.md`): `.cursor/rules/` and `.gemini/` are
   both migration sources and adapter targets — archive originals to `legacy/` first, then
   generate adapters, so they never collide.

`VERSION` → 4.1.1; `UPGRADE.md` 4.1.0→4.1.1 rung + version table; `README`. `DECAY.md` /
`REVIEW.md` unchanged.

---
## Version 4.1.0, 6/15/2026

> **Cross-vendor skills layer.** The shared layer gains its third leg — *capabilities* —
> beside memory and steering. A skill is committed, vendor-neutral markdown
> (`skills/<name>/SKILL.md`: a `name`, a `description` = when-to-use, a procedure, optional
> scripts). The `AGENTS.md` "Skills" section is the universal runtime (the agent reads the
> skill — works on any vendor); native adapters (`.claude/skills/`, `.gemini/commands/`,
> `.cursor/rules/`) are thin, regenerated, gitignored pointers. Migration **promotes**
> vendor skill bundles (e.g. `.claude/skills/`) into `skills/` rather than flattening them
> into steering. **Additive** (a repo with no skills is unchanged). Design:
> `docs/DESIGN-skills-layer.md`.

### Added

1. **`skills/` layer** — neutral, committed `skills/<name>/SKILL.md` capabilities (the
   shared source of truth), documented in `.agent/schema.md`.
2. **`AGENTS.md` "Skills" baseline** (root + template) — the agent-as-runtime mechanism;
   works on any vendor with no per-vendor engine.
3. **Per-vendor adapters** — generated Claude (`.claude/skills/`), Gemini
   (`.gemini/commands/`), and Cursor (`.cursor/rules/`) pointers; regenerated, gitignored.
4. **Migration promotion** — `MIGRATE.md` Section B2 + the Claude Code skills protocol:
   detect `.claude/skills/`, promote into `skills/` (originals preserved under `legacy/`),
   regenerate adapters. `ENABLE.md` Step 5h defines adapter generation.

### Removed

N/A.

### Changed

1. `ENABLE.md` (Step 5h + verify/report/scope), `MIGRATE.md` (principle 6, Section B2,
   Claude protocol, detection table, continuity note), `AGENTS.md` (root + template),
   `.agent/schema.md`, `templates/.gitignore` (comment), `README`. `VERSION` → 4.1.0;
   `UPGRADE.md` 4.0.0→4.1.0 rung + version table. `DECAY.md` / `REVIEW.md` unchanged.

---
## Version 4.0.0, 6/15/2026

> **The forward layer.** agent-memory gains a cognitive lifecycle loop on top of its
> memory substrate: **Current State → Vision → Blueprint → Design → Implementation →
> Feedback**. Memory was backward-looking (faithful to what happened); VBDI makes it
> *goal-aware* (faithful to what was *intended*) — the "predictable innovation with human
> partnership" mission. Integrates an independently-drafted cognitive framework
> (`docs/agent-cognitive-framework.md`), designed in `docs/DESIGN-vbdi-lifecycle.md`.
> **Additive** (a repo with no Vision is unchanged) — bumped to 4.0.0 to mark the new
> layer, the forward counterpart to 3.0.0's evolving-memory layer.

### Added

1. **`memory/vision.md`** — the north-star artifact (`templates/memory/vision.md`): target
   state, for whom, success criteria, non-goals. `core`, invariant-verified, one per repo.
2. **Blueprint** — the Vision↔Current-State gap as typed `(blueprint)` Open Threads
   (`… → serves: <vision-id>`); no new file.
3. **Altitude trace** — Implementation → Design → Blueprint → Vision, linked by `id`; a
   broken link is drift (`DECAY.md` §10/§12), grep-detectable.
4. **Bootstrap, never fabricate** — `ENABLE.md` (Step 5g) and the `UPGRADE.md` 3.7.0→4.0.0
   rung create a ⚠️ DRAFT Vision (Current-state context only; target left for the human)
   and raise a `(vision-bootstrap)` human gate.

### Removed

N/A.

### Changed

1. `DECAY.md` (§10 altitude drift + new §12 "The forward layer"), `REVIEW.md` (Vision in
   invariant-verification + altitude drift in the backstop), `.agent/schema.md`, `AGENTS.md`
   (root + template: a "cognitive loop" section + Vision in the session read-list),
   `ENABLE.md` (Step 5g + verify + report). `VERSION` → 4.0.0; `UPGRADE.md` rung + version
   tables; `README`. The tool dogfoods its own confirmed Vision + Blueprint.

---
## Version 3.7.0, 6/14/2026

> Provenance + retrieval-at-scale — the last backlog item. Event-sourcing already records
> which session each fact came from; v3.7.0 *surfaces* it as an optional `origin:` footer,
> and documents retrieval as deliberately lexical + indexed (grep + `archive/INDEX.md` +
> `origin` pointers), with vector/semantic retrieval intentionally out of scope. Closes
> the assessment's provenance gap (#6); addresses the retrieval gap (#4) by design.

### Added

1. Optional **`origin: <session-file>`** footer field (`DECAY.md` §1 + new §11) — the
   session where a fact was `Created`; set at creation, repairable by review (the earliest
   `Created` event). Provenance becomes one hop, and is the cheap defence against memory
   poisoning (every fact traces to an immutable session).
2. `DECAY.md` §11 "Provenance & retrieval" documents the lexical+indexed retrieval strategy
   (grep continuity → grep `archive/INDEX.md` → follow `origin` → optional
   `sessions/INDEX.md`), bounded by project scale.

### Removed

N/A.

### Changed

1. `AGENTS.md` (root + template) set `origin` on new facts and point at the retrieval path;
   `.agent/schema.md` documents `origin` + the retrieval note; `REVIEW.md` notes `origin`
   backfill; `ENABLE.md` notes `origin` is omitted at enable. The worked example shows
   `origin` on the facts created in its session.
2. `VERSION` → 3.7.0; `UPGRADE.md` 3.6.0→3.7.0 rung + version tables; `README`. Assessment
   gap #6 flipped ⬜ → ✅; gap #4 (lexical retrieval) marked ◐ by-design; Retrieval
   scorecard row updated.

---
## Version 3.6.0, 6/14/2026

> Memory smoke test — a cheap, no-code answer to "memory evaluation is unsolved": a
> `memory/smoke-test.md` whose questions a *fresh* agent should be able to answer from
> the memory layer alone. A ❌ is a memory gap to fix, not a question to soften. Closes
> the assessment's gap #5. Additive (a new installed file).

### Added

1. `templates/memory/smoke-test.md` — generic orientation questions (project & type,
   stack, invariants, recent decisions + *why*, open threads, conventions, preferences,
   supersessions) plus project-specific questions seeded at enable, a how-to-run, and a
   result log.
2. `ENABLE.md` step 5f generates it (seeding 2–4 project-specific questions from the
   analysis); Step 8 verifies it; Step 9 reports it. `REVIEW.md` notes that a review is
   a natural time to run it.

### Removed

N/A.

### Changed

1. `.agent/schema.md` documents the file. `VERSION` → 3.6.0; `UPGRADE.md` 3.5.0→3.6.0
   rung + version tables; `README`. Assessment gap #5 flipped ⬜ → ✅ and the Evaluation
   scorecard row ⬜ → ✅.

---
## Version 3.5.0, 6/14/2026

> Write-time contradiction check — the migration-time "surface contradictions, never
> pick a winner" rule now applies to normal sessions: a new fact is scanned against
> existing ones *before* it's recorded. Closes the assessment's gap #3 (the last
> "Partial"). Additive — a behavioral rule + a review backstop; no new fields or knobs.

### Added

1. `DECAY.md` §10 — write-time contradiction check: on adding/rewriting a fact, scan
   `core`/invariants + active decisions in the same area; a clear replacement →
   supersede (§9), a genuine conflict → a `Contradiction:` Open Thread, a clash with a
   `core` invariant → stop and surface.
2. A **contradiction backstop** in `REVIEW.md` (the review scans the facts it already
   reads and flags conflicts it finds).
3. The before-adding-a-fact check in the after-session step of `AGENTS.md` (root + template).

### Removed

N/A.

### Changed

1. `VERSION` → 3.5.0; `UPGRADE.md` 3.4.0→3.5.0 rung + version tables; `README`.
   Assessment gap #3 flipped ⬜ → ✅ and the "Truth maintenance" scorecard row ◐ → ✅.

---
## Version 3.4.0, 6/14/2026

> Invariant verification — never-decay facts (`core` / Architectural Invariants) can
> quietly go "confidently wrong" when circumstances change. The review now periodically
> prompts a human to re-confirm them (or supersede the false ones via v3.3.0). Closes
> the assessment's gap #2. Additive (a policy knob + a tracker field); already-enabled
> repos catch up via the `UPGRADE.md` 3.3.0→3.4.0 rung.

### Added

1. `verify_invariants_every` (default 20) in `decay-policy.md`, and a
   `last_invariant_check` tracker in `continuity.md` Project State.
2. Review routine **step 6** (`REVIEW.md`): when due, raise **one** Open Thread asking a
   human to re-confirm every never-decay fact, then stamp `last_invariant_check`. The
   review **never auto-invalidates** — it only prompts; the human confirms or supersedes
   (§9). An `Invariants:` line joins the review summary.
3. The worked example shows a first invariant-verification prompt.

### Removed

N/A.

### Changed

1. `DECAY.md` §6 gains a "never-decay ≠ never-checked" note; `.agent/schema.md` documents
   the `last_invariant_check` field + the knob. `VERSION` → 3.4.0; `UPGRADE.md`
   3.3.0→3.4.0 rung + version tables; `README`. Assessment gap #2 flipped ⬜ → ✅.

---
## Version 3.3.0, 6/13/2026

> Supersession / fact-invalidation — the evolving-memory layer can now represent a fact
> becoming *false* (a decision reversed, a dependency dropped), not just fading from
> disuse. Closes the industry-alignment assessment's one "High" gap. Additive (optional
> footer fields + a terminal tier); already-enabled repos pick it up via the
> `UPGRADE.md` 3.2.0→3.3.0 rung.

### Added

1. A terminal **`superseded`** tier and optional **`superseded-by`** / **`supersedes`**
   footer fields (`DECAY.md` §9). When a fact is reversed/invalidated, the agent marks
   it `superseded` immediately, adds the successor (`supersedes: <old>`), and records
   `Superseded: <old> → <new>` in the session log's `## Memory References`.
2. Review behavior: superseded facts are archived **flagged "superseded"** (distinct
   from "faded"), promptly (no `archive_window` wait), links preserved in the archive +
   `INDEX.md`; a `Superseded: N` line joins the review summary. Superseded is
   **terminal** — never reactivated by a reference (only a human can reverse it).
3. A worked supersession in `examples/evolving-memory-example/` — a reversed
   REST-versioning decision threaded through before/after/session-log/archive.

### Removed

N/A.

### Changed

1. `DECAY.md`, `REVIEW.md`, `.agent/schema.md`, and `AGENTS.md` (root + template) updated
   for the above; `VERSION` → 3.3.0; `UPGRADE.md` 3.2.0→3.3.0 rung + version tables; the
   industry-alignment assessment flips gap #1 ⬜ → ✅.

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
   deterministically from session logs. Full design in `docs/DESIGN-evolving-memory.md`.
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
