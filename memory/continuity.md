# Continuity — agent-memory

> Shared ground truth for this tool's own development state.

---

## Project State

- **project:** agent-memory
- **status:** v4.16.1 — backward memory layer (v3.x) + forward cognitive layer (VBDI, v4.0.0) + **cross-vendor skills layer (v4.1–4.5)**: neutral committed `agent-skills/` + `AGENTS.md` runtime baseline; recipe + **sync**/**adopt**/**sanity-check** ops live in an **on-demand `SKILLS.md`** (per-session footprint is just a pointer — no skills check in the ritual); Claude/Gemini/Cursor/**Kiro** adapters (gitignored, regenerated, **never committed**); Claude/Cursor/Kiro adapters are description-matched, **Gemini is a slash command** `/<name>`; single-line/quote-free/concise descriptions mirrored verbatim; migration promotes vendor `.claude/skills/` + `.kiro/skills/` and preserves Kiro **hooks** under `legacy/` (never run); enable + every Mode B re-enable **run** `sync skill adapters` (v4.12.0; idempotent, gitignored-only) so adapters are materialized, not merely recommended. **v4.6.0:** `AGENTS.md` now carries a vendor-neutral **commit-attribution** convention (deliberate, human-initiated commits with a self-identifying `Co-Authored-By:` trailer). **v4.7.0–4.7.1:** + a **lightweight mode** keyed to the *objective* "did a file change?" test — **read-only** sessions write **no log**; **any file change** (even one line) writes at least a one-line **lite log**; a memory-relevant event → full ritual ("trivial" is a judgment call, so it never decides the skip). **v4.8.0:** the review **self-verifies its archival** — greps the last `archive_window` sessions for each fading id before archiving (guards against decay miscounts). **v4.9.0:** + a portable **`memory-lint`** verifier skill (`agent-skills/memory-lint/`, Python 3 stdlib) that runs the decay-integrity checks *deterministically* — moves the counting off the LLM (the real fix Copilot argued for). **v4.10.0:** + an optional **fresh-context second-opinion** skill pair — `second-opinion` snapshots the task (derived from continuity+sessions, behind an acknowledge-gated security advisory) for a clean-memory reviewer; `apply-critique` applies the returned critique through a bounded, validated, human-gated loop (build/tests + memory-lint). Snapshots in gitignored `review-scratch/`; **ENABLE + upgrades now install the built-in skills** (`second-opinion` + `apply-critique` + `memory-lint`, which the review ritual relies on). Folds the external "AIF" idea into skills+VBDI; the fresh reviewer is **advisory**, gated by deterministic checks + human (the v4.8/v4.9 lesson). **Dogfooded end-to-end 2026-06-18** (clean-context reviewer caught an upgrade-overwrite invariant tension; fixed via apply-critique); README/deck/whitepaper updated. **Validated across five vendors 2026-06-16/18** (Claude, Gemini cross-machine, Cursor-format, enterprise Kiro on Windows, GitHub Copilot CLI — the Copilot enablement + review surfaced the decay-miscount that drove v4.8.0). **All cross-vendor validations closed.** **v4.10.1 (PATCH):** line-anchored `memory-lint`'s Memory-References parser (`ot-memlint-anchor-bug`) — found while running the verifier during a memory review, where a log quoting the heading in prose tripped a false `over-archived`; the verifier must not be fooled by prose. **v4.10.2 (PATCH):** four fixes from a fresh-context review of the v4.10.x line (GitHub Copilot CLI, applied via the `apply-critique` loop — the second dogfood of the review pair, this time a *different vendor*): `memory-lint`'s `FOOTER_RE` bound to one line (unclosed-footer guard); install protocol **warns before overwriting a locally-modified built-in** (tool-managed-copies contract now *checked*, not convention-only); the `upgrades-additive` invariant text carries its tool-managed-built-ins exception inline; `second-opinion` gains a same-vendor-vs-different-vendor caveat. One low-confidence finding deferred (`ot-memlint-pinned-nested`). **v4.10.3 (PATCH):** lightweight-mode **wording fix** — the session-log test is now keyed to whether a *tracked* file changed (the objective test is the **git diff**, not any filesystem write), and a run whose only writes are **gitignored, regenerated artifacts** (`sync skill adapters`, `review-scratch/`, the compiled lint artifact) is explicitly **no log** (`lightweight-tracked-change-v4103`). Surfaced when a fresh `sync skill adapters` (re)wrote 16 gitignored adapters but left `git status` clean — yet the old "did a *file* change?" wording seemed to demand a lite log; aligns `AGENTS.md` with what `SKILLS.md` already says (sync "touches no committed file"). **v4.10.4 (PATCH):** hardened `memory-lint` to correctly preserve pinned Open Threads that contain deeply-nested sub-items. **v4.11.0 (MINOR):** `memory-lint` now ships a **Node** runtime (`memory-lint.mjs`, Node ≥ 18, built-ins only) alongside Python, at output parity and held equivalent by a **shared test contract** (`test_memory_lint.mjs` ↔ `.py`) — so the deterministic decay check no longer requires a Python install (motivated by a node-preferring collaborator; the determinism guarantee shouldn't depend on which runtime a machine has). Additive: no dispatcher, no installer — the agent picks the runtime. Shipped `25677a7`; **cross-vendor validated** by Gemini 3.1 Pro (GitHub Copilot CLI), which reran both runtimes + suites live and reproduced byte-identical output. **v4.11.1 (PATCH):** hardened `REVIEW.md` step-6 archival-verify against prose — a "use" is now defined as a `## Memory References` entry (not a passing mention), `memory-lint` is the preferred check, and the by-hand fallback only counts in-block hits; fixes an archival livelock (`ot-review-step6-prose`) found in the 2026-06-19 review. Doc + tests only; verifier already correct. **v4.12.0 (MINOR):** enforced skill-adapter sync — ENABLE + every Mode B re-enable now *run* `sync skill adapters` (idempotent, gitignored-only) instead of the read-only "recommend, don't run" check, so a skill's vendor-native adapters are materialized at enable/upgrade (Step 8 asserts adapter completeness); the per-session path still never touches skills. Surfaced upgrading `~/sandbox/simple-proxy` (v4.4.0→4.11.1), where the pre-existing `hello-world` skill was left without its Kiro adapter (`ot-enforce-sync-adapters-v4120`). **v4.12.1 (PATCH):** `memory-lint` dangling-link check now resolves `superseded-by`/`supersedes` targets across other `memory/*.md` files (e.g. `vision.md`) — `load_repo` pools their footers into an `extra` set used *only* for link resolution (not counted as facts), fixed at parity in `.py` + `.mjs` with a cross-file regression test in both suites. A false `[dangling]` the tool's own check would emit when a fact is superseded by a `vision.md` fact; found + fixed by the maintainer dogfooding `~/sandbox/simple-proxy`, ported back here (`ot-memlint-dangling-crossfile-v4121`). **v4.13.0 (MINOR):** tool-provided (system) skills now carry **`provenance: agent-memory-builtin`** in their `SKILL.md` frontmatter (+ a body banner) so a target's AI recognizes a system skill **at edit time**; `SKILLS.md` (new "Tool-provided (system) skills" section) routes a change to **fork** a local variant or **upstream** a genuine fix to the agent-memory project (issue in production; maintainer advisory pre-release, kept generic until enterprise-GitHub) — and `ENABLE.md` §5i's warn-before-overwrite carries the same advice. Closes the gap that nearly stranded the simple-proxy `memory-lint` fix (`ot-system-skill-provenance-v4130`). **Cross-vendor validated 2026-06-20:** a **Gemini CLI** agent in `~/sandbox/simple-proxy` recognized the `provenance` marker and refused an in-place edit (Claude wrote the marker, Gemini honored it — clean-room, different-vendor proof). **v4.14.0 (MINOR):** + an **optional, human-facing Architecture Decision Record log** (`docs/ADR.md`) at the VBDI **Design** altitude — one durable architecture decision per entry (Status · Date · Abstract · Rationale-with-consequences), newest-first, `Proposed → Accepted → Superseded/Deprecated`, **never deleted** (mirrors `DECAY.md` §9); seeded with the 5 standing Architectural Invariants plus the superseded `no-code-markdown-only` decision (ADR-0001…0006; `no-code-markdown-only` recorded as **ADR-0004**, *Superseded by ADR-0006* — surfaced + inserted on maintainer review). **Map-don't-duplicate:** `continuity.md` keeps the live *what* (with `id`), the ADR carries the durable *why*, cross-linked by `formalizes:` ↔ a **visible `(ADR-NNNN)` tag in the invariant title** (a human pointer, **not** an agent read-cue — the invariant text stays authoritative; on maintainer review, moved off the hidden footer so a human auditor sees it). Read **on demand** — **not** in the per-session read path (zero default token cost, like `docs/DESIGN-*.md`); **not auto-installed** into targets (documented as an optional convention in `.agent/schema.md`/`AGENTS.md`; adopt on demand). Dogfooded on this repo. **v4.14.1 (PATCH):** `UPGRADE.md` gains a **"Source of truth for re-synced files"** map — a target's `AGENTS.md` comes from **`templates/AGENTS.md`** (memory hub), **never** the tool's **root** `AGENTS.md` (operator/dual-mode dispatcher, references the non-installed `ENABLE.md`); `DECAY/REVIEW/SKILLS` from root, `schema`/bootstraps from `templates/`; + a grep self-check and a `4.14.0→4.14.1` rung that **verifies + repairs** a mis-synced `AGENTS.md`. Found dogfooding a Copilot v3.7.0→v4.14.0 upgrade of `mercury-composable` that grabbed the root file (operator-only doc fix; no installed-shape change). **v4.15.0 (MINOR):** the optional ADR log gains an **upkeep trigger** — once `docs/ADR.md` exists, a new durable architecture decision, or the supersession/invalidation of an `(ADR-NNNN)`-tagged `continuity.md` fact, **prompts a human-gated ledger update** (add a newer ADR; mark the old `Superseded`/`Deprecated`, never delete; keep `formalizes:` ↔ `(ADR-NNNN)` in sync), closing the 4.14.0 gap where the log could be *adopted* but had no cue to *evolve*. Re-syncs `AGENTS.md` (root + template) + `.agent/schema.md` (`docs/ADR.md` "When to maintain it") + `DECAY.md §12`; the `4.14.1→4.15.0` rung **merges** the trigger into a repo-customized ADR note rather than overwriting. Surfaced + first-propagated dogfooding `mercury-composable`'s ADR opt-in (same session as the upgrade that validated propagation end-to-end). **v4.16.0 (MINOR):** ADR default path changed from `docs/ADR.md` to `docs/arch-decisions/ADR.md` (industry-convention alignment — named subdirectory signals purpose, leaves `docs/` root uncluttered); normative update to `.agent/schema.md`, `AGENTS.md` (root + template), `DECAY.md §12`; this repo's own ADR log moved to `docs/arch-decisions/ADR.md` (dogfooding the new default). Targets already at the new path (e.g. `mercury-composable`) need no file move — version bump only (`ot-adr-path-alignment-v4160`). **v4.16.1 (PATCH):** session filename drift fix — two gaps allowed date-only session filenames (`YYYY-MM-DD.md`): `templates/AGENTS.md`/`schema.md` said "or equivalent" (letting agents use context `currentDate`), and `memory-lint` had no filename check. Both fixed: explicit `date -u +%Y-%m-%d-%H%M%S` requirement + `check_session_filenames` warning (check 5) in both linter runtimes with tests. Surfaced in this repo's own session (`ot-session-filename-drift-fix`). **v4.17.0 (MINOR):** GitHub Copilot CLI skills adapter — a **5th** adapter target `.github/skills/<name>/SKILL.md` (Copilot CLI follows the open Agent Skills standard, same shape as Claude/Kiro; description-matched + `/<name>`); `sync skill adapters` now writes five; `.github/skills/` gitignored **path-scoped** (the rest of `.github/` stays tracked — the one structural difference from the other four adapter dirs); Copilot also promotes skills in Mode C and its steering template now **front-loads the explicit `memory/` read list** + a manual-upkeep note + points at the skills layer (Copilot Ask/Plan modes don't follow a pointer chain or auto-run the ritual — a real-vendor review finding; reliability-over-DRY, **Copilot-scoped** since other vendors proactively load `AGENTS.md`). Mirrors v4.5.0 Kiro. Surfaced dogfooding `~/sandbox/simple-proxy` (Copilot couldn't find a skill authored only in `agent-skills/`); upgraded it to 4.17.0 (`copilot-adapter-v4170`). **v4.18.0 (MINOR):** `sync skill adapters` is now a **runnable script** (the `sync-adapters` built-in: bash + Node + Python at 3-way byte-identical parity, bash preferred (no runtime install); regen 5 adapters/skill + signature-guarded prune; gitignored-only). Replaces the prose-recipe-only sync that agents (Copilot/Gemini) couldn't *run* — they hunted for a non-existent npm/MCP command and flailed. Maintainer-gated reversal of "no sync script"; consistent with `no-build-step-agent-run` (same category as `memory-lint`). Surfaced + dogfooded on `~/sandbox/simple-proxy` → 4.18.0 (`sync-adapters-script-v4180`). **v4.19.0 (MINOR):** **vendor-neutral ritual triggers** — the after-session ritual no longer depends on the agent self-triggering. Enable installs a committed `.githooks/post-commit` (auto-stubs a session log on a real-work commit; re-syncs adapters) **agent-activated** via `git config core.hooksPath .githooks` (zero manual step) + a **CI floor** (`.github/workflows/agent-memory.yml`: `memory-lint` + advisory session-log check on push/PR, zero per-user setup; opt-in `AGENT_MEMORY_STRICT` gate). Advisory, never blocks; `no-build-step-agent-run` holds (git/CI invoke them; the tool runs nothing). From client-team pain (ritual skipped even with Claude; a Copilot-only team had no triggers) + the zero-manual/untrained-user adoption constraint. Design `docs/DESIGN-ritual-triggers.md`; closes `bp-ritual-triggers`. **v4.20.0 (MINOR):** **first-run init** — closes the fresh-clone activation gap a Copilot fresh-clone dogfood exposed (the memory bootstrap self-initializes from `start`, but a clone has the gitignored adapters absent + the hook unactivated). Added `.githooks/init.sh` (one idempotent command: regenerate adapters + `git config core.hooksPath .githooks`) + an `AGENTS.md` self-init note (agent runs it on first session) — one agent step (or one human command) instead of two; CI stays the zero-config floor (`ritual-init-v4200`). **v4.20.1 (PATCH):** folded the first-run self-init into the **top of `copilot-instructions.md`** — a fresh-clone re-test showed Claude self-inits (acts on `AGENTS.md`) but **Copilot CLI did not** (it front-loads `copilot-instructions.md` + summarizes, skipping the AGENTS.md self-init → hook inactive + adapters absent); now Copilot runs `bash .githooks/init.sh` before summarizing. Still prompt-adherence (non-deterministic); `init.sh` fallback + CI floor unchanged. **v4.20.2 (PATCH):** added a `.gitattributes` (root + template) pinning `*.sh` + `.githooks/*` to **LF** so the scripts/hook run under bash on **Windows** (Git Bash/WSL) regardless of `core.autocrlf` — without it a Windows clone (`autocrlf=true`) rewrites them to CRLF and bash fails (`bad interpreter: …^M`). Installed/merged into targets additively (ENABLE Step 7b). From a Copilot Windows-feasibility check (it confirmed Git Bash runs the hook but missed the CRLF trap).
- **last_enabled:** 2026-06-12
- **last_session:** 2026-06-24 | agent: Claude Code (2026-06-24-201500)
- **last_review:** 2026-06-20 | through 2026-06-20-005953
- **last_invariant_check:** 2026-06-20 | through 2026-06-20-005953
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
  **except the tool's own managed built-ins** (`memory-lint`, `second-opinion`, `apply-critique`),
  which are re-copied (overwritten) on upgrade; that overwrite is scoped to those tool-owned files,
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

- [x] **Re-verify invariants (due at the 2026-06-20 review):** confirm `target-repo-scope-only`,
  `never-delete-vendor-files`, `never-pick-a-winner`, `no-build-step-agent-run`, `upgrades-additive`,
  and the Vision (`vision-agent-memory`) still hold, or supersede any that don't (`DECAY.md` §9).
  `sessions_since_last_invariant_check` reached ≥ `verify_invariants_every: 20` (last confirmed
  2026-06-18). The review only prompts — a human checks this off or supersedes the false ones.
  **Confirmed 2026-06-20 (maintainer):** all 5 invariants and the Vision still hold — "the vision and
  our design principles survive real-world use." None superseded. This session's work reinforced them:
  enforce-sync (v4.12.0) + provenance (v4.13.0) leaned on `no-build-step-agent-run` and
  `upgrades-additive`, and the **Gemini CLI** cross-vendor validation confirmed the vendor-neutral Vision.
  <!-- id: ot-reverify-invariants-20260620 | created: 2026-06-20 | last_used: 2026-06-20 | uses: 1 | tier: active | origin: 2026-06-20-005953 -->

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

- [x] **Shipped v4.13.0 (MINOR) — tool-provided (system) skills: provenance marker + upstream advisory.**
  **Edge case (maintainer):** a target's AI edited an agent-memory *built-in* (`memory-lint` in
  `~/sandbox/simple-proxy`) without recognizing it as a tool-managed/system skill, so it neither warned
  nor advised upstreaming — the genuine fix nearly got stranded (overwritten on next upgrade). The
  existing warn-before-overwrite only fires *during an upgrade*, which that session never ran. **Fix:**
  the three shipped built-ins now carry **`provenance: agent-memory-builtin`** in `SKILL.md` frontmatter
  (+ a one-line body banner), so any vendor's agent recognizes a system skill **at edit time** by reading
  the file. `SKILLS.md` gains a "Tool-provided (system) skills" section: before editing, check the
  frontmatter; if marked, don't edit in place — **fork** a local variant under a new name, or **upstream**
  a genuine fix to the agent-memory project (file an issue *in production*; advise the maintainer
  *pre-release* — best-effort back-port + validation). Upstream pointer kept **generic** (no hard-coded
  URL) until the enterprise-GitHub move (maintainer's call). `ENABLE.md` §5i warn-before-overwrite
  extended with the same advice (upgrade-time backstop). `hello-world` is a dogfood sample (never
  installed into targets) → not marked. Adapters untouched (mirror only name+description). Verified:
  description extraction excludes `provenance`; `memory-lint` 0/0 on this repo. Lockstep: 3 built-in
  `SKILL.md`, `SKILLS.md`, `ENABLE.md` §5i, `AGENTS.md` (root + template), `.agent/schema.md`,
  `docs/DESIGN-skills-layer.md`, `VERSION`→4.13.0, `CHANGELOG`, `UPGRADE.md` rung + table, `README`.
  **Cross-vendor validated 2026-06-20 (Gemini CLI, in `~/sandbox/simple-proxy`):** a Gemini agent tried an
  in-place cosmetic edit to `agent-skills/memory-lint/SKILL.md`, **recognized the
  `provenance: agent-memory-builtin` marker** + the no-in-place-edit rule, and **refused** — enforcing
  fork-or-upstream ("guardrail test successful"). First real-world, *different-vendor* confirmation the
  guardrail fires: Claude Code wrote the marker, Gemini independently honored it. Clean-room evidence the
  marker is self-describing across vendors (no out-of-band knowledge needed).
  → serves: vision-agent-memory (vendor-neutral; real-work dogfooding feeds the tool — a target's change
  finds its way home instead of being stranded)
  <!-- id: ot-system-skill-provenance-v4130 | created: 2026-06-20 | last_used: 2026-06-20 | uses: 2 | tier: active | origin: 2026-06-20-002602 -->

- [x] **Shipped v4.12.1 (PATCH) — `memory-lint` dangling-link check resolves targets across `memory/*.md`.**
  `check_dangling` pooled only `continuity.md` + archive footers, so a fact `superseded-by` a target
  whose footer lives in another memory file (notably `vision.md`) false-flagged as `[dangling] … no
  footer anywhere`. **Origin:** the maintainer hit this dogfooding `~/sandbox/simple-proxy` (a retired
  vision superseded by a `vision.md` fact), diagnosed it as a tool bug, and fixed it *there*; the
  simple-proxy AI session didn't surface it for porting, so it was caught by diffing the target's
  built-in against the tool's during the v4.12.0 commit. (My first-turn `memory-lint` run had
  mis-reported the same warning as *data* rot — it was a verifier bug.) **Fix (ported back):**
  `load_repo` now pools footers from other `memory/*.md` (excluding `continuity.md`/`decay-policy.md`)
  into an `extra` set used **only** for supersession-link resolution — never counted as facts, so
  counts/overdue/over-archived are unchanged. Fixed at parity in `memory-lint.py` + `.mjs`
  (code-point sort preserved → byte-identical); `.mjs` now also exports `load_repo`/`check_dangling`
  (additive, test-enabling). Added a cross-file regression test to both suites (exercises `load_repo`
  end-to-end — the bug site — not `check_dangling` alone); proved it fails on the pre-fix pool.
  Verified: both suites 8/8; parity byte-identical on the tool's own memory (0 errors, 0 warnings).
  Lockstep: scripts + tests, `VERSION`→4.12.1, `CHANGELOG`, `UPGRADE.md` rung + table, `README`.
  `SKILL.md` unchanged (no description change → no adapter regen). → serves: vision-agent-memory
  (faithful, verifiable memory; real-work dogfooding feeds the tool — `backlog-real-work-dogfood`)
  <!-- id: ot-memlint-dangling-crossfile-v4121 | created: 2026-06-20 | last_used: 2026-06-20 | uses: 2 | tier: active | origin: 2026-06-20-000243 -->

- [x] **Shipped v4.12.0 (MINOR) — enforce `sync skill adapters` at enable + upgrade.** Surfaced
  upgrading `~/sandbox/simple-proxy` (v4.4.0 → v4.11.1, Mode B): the built-in skills got their
  adapters (the 4.10.0 install rung generates them), but the **pre-existing `hello-world` skill was
  left without its Kiro adapter** (Kiro became a 4th adapter target in 4.5.0) — and the standing
  "Skills adapter check" only **recommended** `sync skill adapters` rather than running it, so a skill
  whose vendor-native adapter is missing can block native auto-trigger until the user syncs by hand.
  Maintainer's call (I agreed): enable + upgrade are deliberate, human-invoked moments, so *materialize*
  the adapters then. **Fix:** the standing step now **runs** `sync skill adapters` on every enable and
  every Mode B re-enable (incl. already-up-to-date) — idempotent, **gitignored-only** (no committed
  change, no version bump, no session log; `no-build-step-agent-run` holds — the agent runs it during a
  human-invoked enable/upgrade). `ENABLE.md` Step 8 now **asserts** adapter completeness (every skill
  has all four adapters, no orphans) — enforcement checked, not convention. The **per-session** path
  still never touches skills; **content-drift** realignment stays the on-demand `skill sanity check`.
  Lockstep: `UPGRADE.md` (standing section + 4.11.1→4.12.0 rung + table + stale back-refs),
  `SKILLS.md`, `ENABLE.md` (5h + Step 8), `docs/DESIGN-skills-layer.md`, `VERSION`→4.12.0,
  `CHANGELOG`, `README`. `AGENTS.md`/`DECAY.md`/`REVIEW.md` unchanged. Dogfooded on simple-proxy
  (re-ran Mode B → hello-world's Kiro adapter materialized; stamped 4.12.0). → serves: vision-agent-memory
  (vendor-neutral, lightweight; a skill works natively across vendors without a manual step)
  <!-- id: ot-enforce-sync-adapters-v4120 | created: 2026-06-19 | last_used: 2026-06-20 | uses: 3 | tier: active | origin: 2026-06-19-234240 -->

- [x] **Fixed v4.11.1 — `REVIEW.md` step-6 archival guard no longer fooled by prose (archival livelock).**
  Step 6 told the agent to grep recent session *files* for an about-to-be-archived id and keep it if
  found — but a raw full-text grep also matched a prior **review summary** naming the fact while
  recording its decay status, so every review that deferred a fact re-armed the guard: it could never
  archive. Surfaced in the 2026-06-19 review (`skills-gemini-dogfood-v451` / `kiro-hooks-edgecase-v452`
  / `commit-attribution-v460` all tripped it on **prose-only** hits; archived by judgment per DECAY §2).
  Same class as the v4.10.1 prose-vs-heading bug. **Fix:** rewrote step 6 to define a "use" as a
  `## Memory References` entry — `memory-lint` is the preferred check (Memory-References-only, immune to
  the trap), the by-hand fallback only counts in-block hits. **The verifier script needed no change**
  (`memref_ids` was already line-anchored since v4.10.1) — confirmed and locked with new `memref_ids`
  regression tests in both `test_memory_lint.py` and `.mjs` (prose mention not counted; block bounded).
  Doc + tests only. Lockstep: `VERSION`→4.11.1, `CHANGELOG`, `UPGRADE.md` rung + table, `README`.
  → serves: vision-agent-memory (faithful, verifiable memory)
  <!-- id: ot-review-step6-prose | created: 2026-06-19 | last_used: 2026-06-19 | uses: 3 | tier: active | origin: 2026-06-19-162522 -->

- [x] **Shipped v4.11.0 (MINOR) — `memory-lint` Node runtime.** A node-preferring collaborator asked
  why the deterministic verifier was Python-only; the principled answer is that "LLM hand-counting is
  unreliable, so prefer a deterministic script" must hold on a node-only machine too. Added
  `memory-lint.mjs` (Node ≥ 18, built-in modules only — `fs`/`path`/`url`; no npm) as a faithful port
  of `memory-lint.py`, plus `test_memory_lint.mjs` mirroring the Python fixtures. **The shared test
  suite is the cross-runtime contract** that keeps the two equivalent. Deliberately minimal per the
  agent-is-the-runtime model (`no-build-step-agent-run`): **no dispatcher, no installer, no
  `detect_runtime.sh`** — `SKILL.md` documents both commands and the agent runs whichever the machine
  has. Verified **byte-identical** output (default + `--strict`) on this repo; both 5-case suites pass;
  confirmed the node tests would fail against the pre-fix reset logic (genuine guards). Lockstep:
  `VERSION`→4.11.0, `CHANGELOG`, `UPGRADE.md` rung 4.10.4→4.11.0 + table, `README` table, `SKILL.md`.
  Committed `25677a7`, pushed to `origin/main`. **Cross-vendor validated 2026-06-19:** Gemini 3.1 Pro
  (GitHub Copilot CLI) independently reran both verifiers + both suites *live* and reproduced
  byte-identical output (same 3 overdue warnings), confirming feature/output parity and the
  no-dispatcher / halt-don't-hand-count design. Reproduction-grade (it reran what we ran); the Sonar
  complexity verdict and the halt-path *behavior* itself remain unexercised. → serves: vision-agent-memory
  (faithful, verifiable memory)
  <!-- id: memlint-node-runtime-v4110 | created: 2026-06-19 | last_used: 2026-06-20 | uses: 3 | tier: active | origin: 2026-06-19-153355 -->

- [x] **Bug: `memory-lint`'s Memory-References detection wasn't line-anchored — FIXED v4.10.1.**
  `memref_ids()` used `text.find("## Memory References")`, matching the *first* occurrence anywhere —
  including the heading string quoted in a session log's prose. Surfaced during the 2026-06-18 review:
  the review log described the method as "the `## Memory References` section", and lint then read the
  log's `## What happened` paragraph as the references block → a **false-positive**
  `[over-archived] sync-adapters-v420` (the archival was in fact correct). **Shipped v4.10.1 (PATCH):**
  anchored the heading match to a real line (`(?m)^## +Memory References[ \t]*$`) and bound the block at
  the next line-anchored heading; added cases (false-positive gone, real references still detected,
  bounding intact); script-only — no description change, adapters untouched. Lockstep: `VERSION`→4.10.1,
  `CHANGELOG`, `UPGRADE.md` rung 4.10.0→4.10.1 + table, `README` table. → serves: vision-agent-memory
  (faithful, verifiable memory)
  <!-- id: ot-memlint-anchor-bug | created: 2026-06-18 | last_used: 2026-06-18 | uses: 1 | tier: active | origin: 2026-06-18-181132 -->

- [x] **(low) Harden `memory-lint`'s `pinned_open_threads` for nested lists.** The v4.10.2 fresh-context
  review (GitHub Copilot CLI) noted the state machine resets `state=None` on a child `- ` bullet, so a
  deeply-nested list could drop a parent's `- [ ]` pin before its footer is read. **Fixed v4.10.4:**
  Updated `pinned_open_threads` to track the indentation level of the parent Open Thread, ignoring
  regular `- ` or `* ` sub-bullets that are indented deeper. Tests confirmed it correctly handles
  both deeply-nested lists and same-level resets. → serves: vision-agent-memory
  <!-- id: ot-memlint-pinned-nested | created: 2026-06-18 | last_used: 2026-06-18 | uses: 1 | tier: active | origin: 2026-06-18-185731 -->

- [x] **Shipped v4.10.3 (PATCH) — lightweight-mode wording fix.** `AGENTS.md`'s lightweight-mode note
  keyed the session-log decision to "did a *file* change?", which reads as *any* filesystem write — but
  its own anchor is the git diff and `SKILLS.md` says `sync skill adapters` "touches no committed
  file… not a version change." Surfaced this session when a fresh sync (re)wrote **16 gitignored**
  adapters yet left `git status` clean, and the literal wording seemed to demand a lite log (maintainer
  caught it). **Fix:** re-keyed all three tiers to a *tracked* change (objective test = the **git
  diff**); the **Read-only** tier now explicitly covers "a run whose only writes are gitignored,
  regenerated artifacts" — `sync skill adapters`, `review-scratch/`, the compiled lint artifact — as
  **no log**. **Refines, does not supersede** `lightweight-mode-v470` — "any file change writes a lite
  log" still holds *for tracked files*. Wording-only; no shape/skill/script change. Lockstep:
  `AGENTS.md` (root + template), `VERSION`→4.10.3, `UPGRADE.md` rung + table, `README`, `CHANGELOG`.
  → serves: vision-agent-memory (faithful, lightweight memory)
  <!-- id: lightweight-tracked-change-v4103 | created: 2026-06-18 | last_used: 2026-06-19 | uses: 2 | tier: active | origin: 2026-06-18-221335 -->

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

- [x] **Dogfood: `hello-world` portable skill (2026-06-16).** The tool now carries its own
  skill — `agent-skills/hello-world/SKILL.md` (neutral source of truth, committed) + a bundled
  `scripts/hello.sh` (agent-invoked helper, exercises `no-build-step-agent-run`) + regenerated,
  gitignored adapters (`.claude/skills/`, `.gemini/commands/`, `.cursor/rules/`, `.kiro/skills/`).
  Tested end-to-end via the `AGENTS.md` baseline. The tool now dogfoods `agent-skills/` the way it
  dogfoods `memory/`. **Cross-vendor + cross-machine validated 2026-06-17** (Gemini CLI, another
  machine): ran via the baseline with no adapter, then natively after `sync skill adapters` — the
  strongest agent-as-runtime portability proof. Surfaced the **invocation-path self-report** issue
  (3 Gemini runs): a vendor expands a `/cmd` into the prompt before the model sees it, so an agent
  can't reliably self-report its trigger → **option B**: `hello-world` step 3 reports the *result,
  not the trigger* (`docs/DESIGN-skills-layer.md` §4c). → serves: vision-agent-memory
  <!-- id: dogfood-hello-world-skill | created: 2026-06-16 | last_used: 2026-06-19 | uses: 21 | tier: active | origin: 2026-06-16-152327 -->
- [x] **v4.4.0 (MINOR): lightweight skills — conscious, not per-session.** Maintainer's frame:
  "skill creation is a conscious developer act; don't do heavy skill work every session." The
  adapter recipe + **sync** / **adopt** / **sanity-check** ops moved OUT of the per-session
  `AGENTS.md` into an on-demand installed **`SKILLS.md`** (sibling of DECAY/REVIEW); the per-session
  "Skills" section is now just the runtime baseline + a pointer. Removed the v4.3.0 per-session
  "skills safety check" (partially supersedes `authoring-adopt-v430` — authoring + adopt stand).
  Trims ~1.3K tok off every-session bootstrap. → serves: vision-agent-memory
  <!-- id: lightweight-skills-v440 | created: 2026-06-16 | last_used: 2026-06-19 | uses: 8 | tier: active | origin: 2026-06-16-194434 -->
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

- **Shipped v4.8.0 — review self-verify guard against decay miscounts (MINOR).** The 2026-06-18
  GitHub Copilot CLI review over-archived 3 recent active facts (`dogfood-hello-world-skill`,
  `kiro-adapter-v450`, `lightweight-skills-v440`) — it **miscomputed `sessions_since_last_used`**
  (counted ~5–9 as ">20") and ignored its own "still referenced in window" note. The decay *rule*
  was correct; the *count* wasn't, and nothing forced a check. Remediation (maintainer chose the
  lightweight markdown guard over an optional lint script): `REVIEW.md` gains **step 6 "Verify
  archival"** — before stamping, `grep` the last `archive_window` session files for each
  about-to-be-archived id; **any hit ⇒ the count was wrong, keep the fact**; also confirm no id lives
  in both `continuity.md` and the archive. Replaces a hand-counted judgment with a checkable signal
  for the riskiest op. Honest framing: agent misjudgment isn't fully eliminable (no-code = trust the
  agent), but this error *class* is now self-catching. Touched: `REVIEW.md` (step + summary line),
  `VERSION`→4.8.0, `UPGRADE.md` 4.7.1→4.8.0 rung + table, `README`/`CHANGELOG`. `AGENTS.md`/`SKILLS.md`/`DECAY.md`
  unchanged. → serves: vision-agent-memory (faithful memory; deterministic, verifiable decay)
  <!-- id: review-verify-v480 | created: 2026-06-18 | last_used: 2026-06-18 | uses: 6 | tier: active | origin: 2026-06-18-062730 -->

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

- **Shipped v4.10.0 — fresh-context second opinion (optional skill pair) (MINOR).** Folded an
  external brainstorming artifact (the "AIF" draft — architecture paper + snapshot/critique specs)
  into the **skills layer + VBDI** rather than a standalone spec — net-new surface is small: a
  **security advisory** on export, the handoff ritual, and the critique shape; the rest reuses
  continuity+sessions, the VBDI human gate, and memory-lint/build-tests. Built
  `agent-skills/second-opinion/` (snapshot *derived from* continuity + recent sessions — never a
  parallel state file — behind an acknowledge-gated advisory; milestone & reactive modes) +
  `agent-skills/apply-critique/` (parse → ≤N scoped fixes → validate (build/tests + memory-lint) →
  summarize applied/rejected; conflicts → Open Thread; writes a session log). Snapshots/critiques
  live in gitignored `review-scratch/` (README marks it personal — sharing is a conscious decision).
  **ENABLE Step 5i + the UPGRADE 4.10.0 rung now install the built-in skills** (`second-opinion`
  + `apply-critique` + `memory-lint`) into every enabled repo — **superseding memory-lint's
  v4.9.0 "tool-local / not auto-installed" stance** (the review ritual relies on it; maintainer
  revised the initial opt-in choice — installing ≠ running, still zero-overhead-by-default).
  Load-bearing lesson baked in (v4.8/v4.9): the fresh reviewer is a **hypothesis
  generator, not an authority** — critique is advisory, gated by deterministic checks + human.
  **Dogfooded end-to-end 2026-06-18** — ran `second-opinion` on this milestone; a clean-context
  subagent reviewer (no session memory) caught a **real invariant tension the author missed**
  (upgrade silently overwriting a user-customized built-in vs. `upgrades-additive`), fixed via
  `apply-critique` (tool-managed-copies contract in ENABLE+UPGRADE, 5h/5i contradiction, no-gate
  fallback, deeper-log reach, Python-3 prereq). Human-facing docs updated (`README`,
  `docs/agent-memory-deck.html` +slide & version bump, `docs/agent-memory-whitepaper.md`).
  **Post-dogfood refinement (real-use consideration):** `second-opinion` now makes the snapshot
  **self-contained** + names an *Attach to reviewer* manifest, so a **repo-less web reviewer**
  works (not only a repo-access agent — the dogfood used a filesystem reviewer, masking this).
  Touched: the two skills (+ gitignored adapters regenerated), `ENABLE.md` (5i + report/scope),
  root & `templates/.gitignore` (`review-scratch/`), `.agent/schema.md`, `VERSION`→4.10.0,
  `UPGRADE.md` rung + table, `README`/`CHANGELOG`, `docs/DESIGN-fresh-context-review.md`.
  `AGENTS.md`/`SKILLS.md`/`DECAY.md`/`REVIEW.md` unchanged. Realizes `bp-fresh-context-review`.
  → serves: vision-agent-memory
  <!-- id: fresh-review-v4100 | created: 2026-06-18 | last_used: 2026-06-20 | uses: 5 | tier: active | origin: 2026-06-18-170657 -->

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
- [x] **(blueprint)** Fresh-context second opinion — no deliberate ritual for handing a
  curated snapshot to a clean-memory reviewer (any vendor / clean session) at a milestone or
  risk point, getting structured critique back, and applying it through a bounded, validated,
  human-gated loop. **Direction confirmed 2026-06-18 (maintainer): fold into skills + VBDI**,
  not a standalone "AIF" spec. Design drafted & under review:
  `docs/DESIGN-fresh-context-review.md`. Net-new surface is small (security advisory on export
  + the handoff ritual + the critique shape); the rest reuses continuity/sessions, VBDI gates,
  and memory-lint/build-tests. Carries the v4.8/v4.9 lesson: fresh critique is **advisory**,
  gated by deterministic checks + human. Next: settle the design's §10 forks, then build a
  skill pair (`second-opinion` + `apply-critique`) on an additive MINOR rung. **Delivered
  v4.10.0 this session** (`fresh-review-v4100`): pair built, ENABLE + upgrades install the
  built-in skills (incl. `memory-lint`), snapshots in gitignored `review-scratch/`.
  → serves: vision-agent-memory
  <!-- id: bp-fresh-context-review | created: 2026-06-18 | last_used: 2026-06-18 | uses: 5 | tier: active | origin: 2026-06-18-164859 -->

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
