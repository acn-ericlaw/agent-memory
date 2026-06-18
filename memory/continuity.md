# Continuity — agent-memory

> Shared ground truth for this tool's own development state.

---

## Project State

- **project:** agent-memory
- **status:** v4.8.0 — backward memory layer (v3.x) + forward cognitive layer (VBDI, v4.0.0) + **cross-vendor skills layer (v4.1–4.5)**: neutral committed `agent-skills/` + `AGENTS.md` runtime baseline; recipe + **sync**/**adopt**/**sanity-check** ops live in an **on-demand `SKILLS.md`** (per-session footprint is just a pointer — no skills check in the ritual); Claude/Gemini/Cursor/**Kiro** adapters (gitignored, regenerated, **never committed**); Claude/Cursor/Kiro adapters are description-matched, **Gemini is a slash command** `/<name>`; single-line/quote-free/concise descriptions mirrored verbatim; migration promotes vendor `.claude/skills/` + `.kiro/skills/` and preserves Kiro **hooks** under `legacy/` (never run); upgrades do a read-only filename check that recommends sync. **v4.6.0:** `AGENTS.md` now carries a vendor-neutral **commit-attribution** convention (deliberate, human-initiated commits with a self-identifying `Co-Authored-By:` trailer). **v4.7.0–4.7.1:** + a **lightweight mode** keyed to the *objective* "did a file change?" test — **read-only** sessions write **no log**; **any file change** (even one line) writes at least a one-line **lite log**; a memory-relevant event → full ritual ("trivial" is a judgment call, so it never decides the skip). **v4.8.0:** the review **self-verifies its archival** — greps the last `archive_window` sessions for each fading id before archiving (guards against decay miscounts). **Validated across five vendors 2026-06-16/18** (Claude, Gemini cross-machine, Cursor-format, enterprise Kiro on Windows, GitHub Copilot CLI — the Copilot enablement + review surfaced the decay-miscount that drove v4.8.0). **All cross-vendor validations closed.**
- **last_enabled:** 2026-06-12
- **last_session:** 2026-06-18 | agent: Claude Code (2026-06-18-062730)
- **last_review:** 2026-06-18 | through 2026-06-18-051933
- **last_invariant_check:** 2026-06-18 | through 2026-06-18-054159
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
  <!-- id: target-repo-scope-only | created: 2026-06-13 | last_used: 2026-06-17 | uses: 8 | tier: core -->
- Never delete vendor files — move originals to `legacy/<vendor>/`, preserving paths
  <!-- id: never-delete-vendor-files | created: 2026-06-13 | last_used: 2026-06-17 | uses: 6 | tier: core -->
- Never overwrite, never pick a winner — fold vendor steering under
  `## Migrated rules from <vendor>`; surface contradictions as Open Threads
  <!-- id: never-pick-a-winner | created: 2026-06-13 | last_used: 2026-06-17 | uses: 10 | tier: core -->
- No build step; agent-run — the tool itself runs no code and needs none (no install, no
  daemon). The markdown files are the product and the agent is the runtime. A skill MAY
  bundle optional helper scripts, but those are invoked by the agent/vendor at the user's
  direction, never executed by the tool.
  <!-- id: no-build-step-agent-run | created: 2026-06-16 | last_used: 2026-06-18 | uses: 26 | tier: core | supersedes: no-code-markdown-only | origin: 2026-06-16-002134 -->
- Upgrades are additive and non-destructive — enrich and add, never rewrite or delete
  <!-- id: upgrades-additive | created: 2026-06-13 | last_used: 2026-06-16 | uses: 16 | tier: core -->

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

- [x] **Re-verify invariants (due):** confirm `target-repo-scope-only`, `never-delete-vendor-files`, `never-pick-a-winner`, `no-build-step-agent-run`, `upgrades-additive`, and the Vision (`vision-agent-memory`) still hold, or supersede any that don't (`DECAY.md` §9). Due: 34 sessions since last check (`verify_invariants_every: 20`).
  **Confirmed 2026-06-18 (maintainer):** all 5 invariants and the Vision still hold.
  <!-- id: ot-reverify-invariants-20260618 | created: 2026-06-18 | last_used: 2026-06-18 | uses: 2 | tier: active | origin: 2026-06-18-051933 -->

- [x] Incorporate findings from real-world enablement / validation. **Closed 2026-06-17
  (maintainer):** the validation loop is satisfied — a **team demo of "AI enable" drew member
  support**, and the v4.x upgrade was exercised across real targets and **three non-Claude vendors**
  (Gemini cross-machine run, enterprise-Kiro bootstrap on Windows, Kiro enablement of a new
  source-code repo with an honest "helps more than it interferes" assessment). No blocking issues;
  findings drove the **v4.5.1–v4.7.1** refinements (Gemini slash-command + commit guard; Kiro
  hooks; commit attribution; lightweight mode). The dogfood-feedback loop did its job.
  <!-- id: ot-realworld-v411-findings | created: 2026-06-16 | last_used: 2026-06-17 | uses: 2 | tier: active | origin: 2026-06-16-141614 -->

- [x] Validate the memory + skills layer with **GitHub Copilot CLI**. Maintainer's account was
  **approved 2026-06-17**, activating in ~1–2 days (≈2026-06-18/19); they'll then test and report.
  Copilot is already in the Mode C detection table (`.github/copilot-instructions.md`) and gets a
  bootstrap pointer — this validates whether Copilot CLI actually reads `AGENTS.md` / follows the
  protocol, and whether skills need a Copilot adapter (today the recipe covers Claude/Gemini/Cursor/Kiro).
  Last open cross-vendor validation; same dogfood loop.
  **Closed 2026-06-18 (GitHub Copilot):** Copilot CLI reads `AGENTS.md`, follows the full protocol
  (before-session reads, multi-agent continuity, VBDI, session log, lightweight-mode, fact metadata,
  supersession, skills, invariants — all verified). Skills work via the `AGENTS.md` baseline; no
  native adapter format exists for Copilot (not a blocker — the baseline is sufficient). Cross-vendor
  validation set is now complete: Claude, Gemini, Cursor, Kiro, **GitHub Copilot CLI** ✅.
  <!-- id: ot-copilot-cli-validation | created: 2026-06-17 | last_used: 2026-06-18 | uses: 2 | tier: active | origin: 2026-06-17-190301 -->

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
  <!-- id: skills-layer-v410 | created: 2026-06-15 | last_used: 2026-06-18 | uses: 7 | tier: active | origin: 2026-06-15-234801 -->

### Shipped — v4.2.0: "sync skill adapters" (2026-06-16)
- [x] **"Sync skill adapters" operation shipped (additive MINOR).** Closes the cross-machine
  gap (surfaced while prepping the simple-proxy Gemini-CLI test): adapters are gitignored, so
  they don't travel with a clone/pull, and re-running "AI enable" on an up-to-date repo is a
  no-op. New on-demand operation: regenerate the Claude/Gemini/Cursor adapters from each
  `agent-skills/<name>/SKILL.md` (idempotent; prune orphans; never touch the neutral skill).
  The **canonical adapter recipe moved into the installed `AGENTS.md` "Skills" section** (so a
  target's own agent — any vendor — self-syncs by reading its own AGENTS.md); `ENABLE.md`
  Step 5h now references it (DRY). Touched: `AGENTS.md` (root + template), `ENABLE.md`,
  `.agent/schema.md`, `VERSION`→4.2.0, `UPGRADE.md` 4.1.1→4.2.0 rung + table, `README`/`CHANGELOG`,
  `docs/DESIGN-skills-layer.md` (§9 resolved). `DECAY.md`/`REVIEW.md` unchanged. Dogfooded:
  deleted the tool's hello-world Gemini adapter and regenerated it via the operation. Supports
  multi-machine contributors (`bp-multi-user`). → serves: vision-agent-memory
  <!-- id: sync-adapters-v420 | created: 2026-06-16 | last_used: 2026-06-17 | uses: 9 | tier: archive-candidate | origin: 2026-06-16-171539 -->

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
  <!-- id: dogfood-hello-world-skill | created: 2026-06-16 | last_used: 2026-06-18 | uses: 9 | tier: active | origin: 2026-06-16-152327 -->
- [x] **v4.4.0 (MINOR): lightweight skills — conscious, not per-session.** Maintainer's frame:
  "skill creation is a conscious developer act; don't do heavy skill work every session." The
  adapter recipe + **sync** / **adopt** / **sanity-check** ops moved OUT of the per-session
  `AGENTS.md` into an on-demand installed **`SKILLS.md`** (sibling of DECAY/REVIEW); the per-session
  "Skills" section is now just the runtime baseline + a pointer. Removed the v4.3.0 per-session
  "skills safety check" (partially supersedes `authoring-adopt-v430` — authoring + adopt stand).
  Trims ~1.3K tok off every-session bootstrap. → serves: vision-agent-memory
  <!-- id: lightweight-skills-v440 | created: 2026-06-16 | last_used: 2026-06-18 | uses: 1 | tier: active | origin: 2026-06-16-194434 -->
- **Shipped v4.5.0 — Kiro support (a 4th adapter + Mode C detection).** Amazon's **Kiro IDE**
  converges on the two open standards this tool bets on: it auto-reads root **`AGENTS.md`** (memory
  layer needs no pointer file) and its Agent Skills follow the **open Agent Skills standard** (same
  `SKILL.md` shape as Claude). Added a 4th adapter target `.kiro/skills/<name>/SKILL.md` (`sync`
  writes four adapters) + **Kiro in the Mode C detection table** (`MIGRATE.md`: steering →
  instructions, skills → `agent-skills/`, specs → `legacy/`). **Kiro Powers need no special
  handling** (partner bundles that *consume* open-standard skills). → serves: vision-agent-memory
  <!-- id: kiro-adapter-v450 | created: 2026-06-16 | last_used: 2026-06-18 | uses: 1 | tier: active | origin: 2026-06-16-221832 -->

### Shipped — v4.5.1–v4.7.1: cross-vendor refinements (2026-06-17)
- **Shipped v4.5.1 — skills-layer guidance (PATCH, from the Gemini CLI cross-machine dogfood).**
  Two rough edges surfaced by a real Gemini CLI run (see `dogfood-hello-world-skill`), both
  wording/guidance — no shape change: **(1)** after `sync`, a natural-language "run hello-world"
  kept reading `agent-skills/` rather than the new `.gemini/commands/` command. **Root cause:**
  Gemini custom commands are **slash commands** (`/<name>`, explicit) — *not* NL auto-triggers
  like Claude/Cursor/Kiro — so NL correctly routes through the `AGENTS.md` baseline to the **same**
  neutral skill (identical result; both the slash command and the baseline are pointers to
  `agent-skills/`, so nothing can diverge). **(2)** the agent told the user to **commit** the
  vendor adapter dirs — wrong: adapters are gitignored/per-machine/regenerated; only
  `agent-skills/` is committed (the `.gitignore` already blocks it, but the agent shouldn't
  recommend it). **Fixes:** `SKILLS.md` — Gemini adapter documented as a slash command + a
  "trigger semantics differ per vendor" note + a **never-commit-the-adapters** guard on the
  `sync` op; `AGENTS.md` (root + template) adapter line now says "never commit them"; `DESIGN`
  recipe table + note. `VERSION`→4.5.1, `UPGRADE.md` 4.5.0→4.5.1 rung + table, `README`/`CHANGELOG`.
  `DECAY.md`/`REVIEW.md` unchanged. The dogfood-feedback loop (drove v3.1.0/v3.2.0/v4.2.0) again.
  → serves: vision-agent-memory
  <!-- id: skills-gemini-dogfood-v451 | created: 2026-06-17 | last_used: 2026-06-17 | uses: 6 | tier: archive-candidate | origin: 2026-06-17-044933 -->

- **Shipped v4.5.2 — Kiro hooks in Mode C + a bootstrap edge-case note (PATCH, from a Windows/Kiro
  enable).** The maintainer cloned this repo on a fresh Windows 11 machine and opened it in
  **enterprise Kiro**. Two findings: **(1) chicken-and-egg bootstrap** — on a fresh clone `.kiro/`
  doesn't exist (gitignored, per-machine), and enterprise Kiro **self-bootstraps from its
  onboarding/MCP before reading `AGENTS.md`**; the human nudge **"Start from `AGENTS.md`"** puts the
  agent-memory protocol in charge (works — then `sync skill adapters` regenerates local adapters).
  **(2) Kiro deposits hooks + steering** into `.kiro/` (e.g. `kiro-commit-signature.kiro.hook` +
  `auto-commit-prompt.md`). **Compatibility verdict: no hard incompatibility** — all of `.kiro/` is
  gitignored (verified `git check-ignore` on hooks/steering/skills paths), so enterprise content
  stays per-machine and never enters the shared `memory/`/`agent-skills/` layer, and `sync` only
  writes `.kiro/skills/<name>/` ("never touch other files in a vendor dir"). **No tension after
  all (maintainer-clarified):** my first "auto-commit" worry was a wrong inference from the
  filename — the Kiro commit hook is **human-gated** (fires only when the human says "commit"; Kiro
  writes a context-aware message + a "co-authored by Kiro" trailer), which *matches* agent-memory's
  deliberate-commit model (agent-memory itself uses co-author trailers). The only hypothetical
  concern would be a hook that commits/pushes **unprompted** — none here. **Changes:** `MIGRATE.md`
  Kiro protocol gains a **Hooks** sub-case (`.kiro/hooks/*.kiro.hook` → preserve verbatim under
  `legacy/kiro/hooks/`, never convert/run; human-gated commit hooks align, only unprompted
  auto-commit/push → Open Thread); `README` bootstrap edge-case note;
  `VERSION`→4.5.2, `UPGRADE.md` rung + table. `AGENTS.md`/`SKILLS.md`/`DECAY.md`/`REVIEW.md`
  unchanged. → serves: vision-agent-memory (multi-vendor, multi-machine without drift)
  <!-- id: kiro-hooks-edgecase-v452 | created: 2026-06-17 | last_used: 2026-06-17 | uses: 3 | tier: active | origin: 2026-06-17-175728 -->

- **Shipped v4.6.0 — vendor-neutral commit attribution (MINOR).** Came from the maintainer's
  observation: **Claude Code adds a deliberate, human-gated `Co-Authored-By:` trailer
  automatically** (it's in its harness), **Kiro needed a per-machine hook + steering** to do the
  same, and Gemini/Cursor do nothing by default. That vendor-by-vendor inconsistency is exactly the
  gap the shared layer closes. So `AGENTS.md` (root + template) now **extends its existing "identify
  yourself" principle** (already true for session logs) **to commits**: "After Every Session" step 4
  + checklist say *commits are deliberate and human-initiated; identify yourself the way you do in
  session logs — e.g. a `Co-Authored-By: <agent>` trailer.* **Soft by design** (guides, doesn't
  prescribe git workflow; a no-op for runtimes that already do it). Now any vendor gets Claude's
  behavior with **no per-vendor hook** — a concrete "encode once in the shared layer vs. N
  per-vendor configs" proof point. Touched: `AGENTS.md` (root + template), `VERSION`→4.6.0,
  `UPGRADE.md` 4.5.2→4.6.0 rung + table, `README`/`CHANGELOG`. `SKILLS.md`/`DECAY.md`/`REVIEW.md`
  unchanged. → serves: vision-agent-memory (`bp-multi-user` — multi-contributor traceability + provenance)
  <!-- id: commit-attribution-v460 | created: 2026-06-17 | last_used: 2026-06-17 | uses: 2 | tier: active | origin: 2026-06-17-181607 -->

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
  <!-- id: lightweight-mode-v470 | created: 2026-06-17 | last_used: 2026-06-17 | uses: 3 | tier: active | origin: 2026-06-17-184652 -->

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
  <!-- id: review-verify-v480 | created: 2026-06-18 | last_used: 2026-06-18 | uses: 1 | tier: working | origin: 2026-06-18-062730 -->

### Blueprint — gaps from Current State (v4.8.0) to the Vision  (serves: vision-agent-memory)
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

### Backlog — vNext (temporal & supersession) + beyond
> From the 2026-06-13 industry-alignment assessment:
> `docs/assessments/2026-06-13-industry-alignment.md`. Verdict: on track; distinctive
> on event-sourcing/determinism/governance; one real gap = temporal/supersession.
> Re-run the assessment after meaningful iterations and compare its scorecard.

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
