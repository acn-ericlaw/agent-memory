# Changelog

## Release notes

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> Releases 1.0.0–3.0.0 below were reconstructed retrospectively (this changelog was
> introduced after 3.0.0 shipped), organized by capability rather than by individual
> commit. The capability ladder matches `VERSION` and `UPGRADE.md`.

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
