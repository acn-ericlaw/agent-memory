# Continuity — agent-memory

> Shared ground truth for this tool's own development state.

---

## Project State

- **project:** agent-memory
- **status:** v4.33.2 — a vendor-neutral, no-code (markdown) shared-AI-memory + AI-enablement tool. Three shared layers: **backward memory** (v3.x — fact metadata + ids, decay/review/archive), a **forward VBDI cognitive loop** (v4.0 — Vision→Blueprint→Design→Impl over the memory substrate), and a **cross-vendor skills layer** (v4.1+ — neutral committed `agent-skills/` + a runnable `sync-adapters`; six adapter targets: Claude/Gemini/Cursor/Kiro/Copilot/Antigravity). Agent-as-runtime; `memory/` is committed + shared. Built-in skills: `memory-lint`, `second-opinion`+`apply-critique`, `sync-adapters`, `harvest-knowledge`, `archive-fact`, `refresh-metadata`. Vendor-neutral, **forge-aware** ritual triggers (committed git hook + a CI floor matched to the hosting forge — GitHub Actions, GitLab CI, or Azure Pipelines, v4.31.0–v4.32.0) with first-run self-init; Windows LF hardening. **Per-version history lives in `UPGRADE.md` (the version ladder) + `memory/sessions/` — kept OUT of this line by design (v4.22.0): `status` is a short current-state descriptor, not a changelog, so this shared line doesn't become a merge-conflict hotspot.** `.agent/version.md` is the canonical version. Validated across six vendors (Claude, Gemini, Cursor, Kiro, Copilot CLI, Antigravity).
- **last_enabled:** 2026-06-12
- **last_session:** 2026-08-13 | agent: Claude Code (2026-08-13-231459)
- **last_review:** 2026-07-27 | through 2026-07-27-203400
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

- [x] **Shipped v4.33.2 (PATCH) — `[secret-material]`: backtick is a value delimiter.** The
  `4.33.0→4.33.1` rung's own verify step on the live target caught, minutes after v4.33.1
  released, that the enum-constant exclusion missed the form the motivating field line actually
  used — **markdown inline code**: in a backticked `key=VALUE` span the closing backtick rode
  into the captured value, so the ALL-CAPS fullmatch never applied and the FP survived. Fix:
  backtick joins the quote/value delimiter set in the credential-assignment pattern (both
  runtimes; a backticked mixed-case literal still flags — negative control added); the mirror
  enum test now quotes the **exact field line verbatim** (45 each). Verified three ways: suites,
  dogfood (0 errors, byte-parity), and live target — zero `[secret-material]` on
  mercury-composable with no waiver. **Lesson: a field-motivated fix's fixture must quote the
  field line verbatim** — the paraphrased bare form validated a fix the real markdown form
  defeated. Lockstep: `VERSION`→4.33.2, `CHANGELOG`, `README` (row + 10-cap trim, drops 4.28.3),
  `UPGRADE` (row + `4.33.1→4.33.2` rung — the waiver drop 4.33.1 promised becomes true here).
  SKILL.md description unchanged → adapters untouched. **Also folded in** (maintainer feedback
  on this release's own PR): the PR/MR description templates' rendered `<sub>` convention
  footer (own + 3 forge variants) became an **HTML comment** — guides authors, never renders
  in a created PR/MR; rung gains an optional template re-copy step. → serves:
  vision-agent-memory (the advisory stays signal — and the trigger layer's verify steps are
  what keep it honest)
  <!-- id: secret-fp-backtick-v4332 | created: 2026-08-13 | last_used: 2026-08-13 | uses: 1 | tier: working | origin: 2026-08-13-231459 -->

- [x] **Shipped v4.33.1 (PATCH) — `[secret-material]`: ALL-CAPS enum constants are not credentials.**
  Check 10's first field contact (the 2026-08-13 Mode B upgrades of mercury + mercury-composable,
  both public) produced exactly one finding — a **false positive**: a session log documenting
  Confluent's `bearer.auth.credentials.source` property with its enum value `OAUTHBEARER` (a source
  *type*, not a credential). Fix the detector, don't sprinkle waivers through client repos (the
  honest-signal doctrine — same class as v4.26.1/v4.28.2): the credential-assignment pattern now
  treats ALL-CAPS identifiers (`^[A-Z][A-Z0-9_]{2,}$` — `OAUTHBEARER`, `SASL_SSL`, `STATIC_TOKEN`,
  …) as config constants; real credentials carry mixed case/symbols, and uppercase-only token
  shapes (AWS key ids) stay covered by the value-shape patterns independently. Both runtimes at
  parity, mirror test added (45 each); dogfood lint clean. The rung lets a target drop a waiver
  added solely for this FP class (mercury-composable's `2026-07-09-212417.md`). Lockstep:
  `VERSION`→4.33.1, `CHANGELOG`, `README` (row + 10-cap trim, drops 4.28.2), `UPGRADE` (row +
  `4.33.0→4.33.1` rung). SKILL.md description unchanged → adapters untouched. → serves:
  vision-agent-memory (the advisory stays signal, not noise)
  <!-- id: secret-fp-enum-constants-v4331 | created: 2026-08-13 | last_used: 2026-08-13 | uses: 2 | tier: active | origin: 2026-08-13-225859 -->

- [x] **Shipped v4.33.0 (MINOR) — session-log secret redaction: ritual rule + `[secret-material]`
  lint advisory.** From a **client-side field incident** (reported 2026-08-13): a DLP scanner caught
  a live OAuth client secret in a committed session log (dated 2026-07-13) — pasted smoke-test
  output, verbatim; nothing in the protocol or tooling stood between a rendered credential and
  `git push`. Maintainer directive: any secrets (PII and credentials) must be redacted from session
  memory. Incident repo is client-side (no direct access; their team rotated + cleaned history) —
  this closes the loose end forward. **Shipped:** (a) redaction rule in the after-session ritual
  (`AGENTS.md` ×2, `ENABLE.md` 5c, schema session-file section): never write secrets/PII into
  `memory/`; redact pasted output to `(REDACTED)`; a committed secret is exposed — rotate it,
  redaction ≠ un-leaking; the one sanctioned edit to an immutable log. (b) `memory-lint` check 10
  `[secret-material]` (py + mjs parity, mirror tests 44 each): token shapes, credential-key
  assignments with literal values (rendered-JAAS class; placeholders / redaction markers /
  number-shapes safe), emails (public forms excluded), SSN + Luhn-verified cards, absolute home
  paths; scans `sessions/` + `archive/` (unlike check 7); **never echoes the matched value**;
  `lint:allow-secret-material` waives a quoted-example line. Advisory (STRICT gates red); CI floor
  picks it up with no forge-file changes. Dogfood: 2 real pre-existing home-path hits (mock quotes
  in old cleanup logs — waived in place), zero credential/PII noise across 145 logs + archive.
  Lockstep: `SKILL.md` (description → adapters 8→48), docs-site built-in-skills (ten checks),
  `VERSION`→4.33.0, `CHANGELOG`, `README` (row + 10-cap trim, drops 4.28.1), `UPGRADE` (row +
  `4.32.1→4.33.0` rung with a triage-now step). → serves: vision-agent-memory (shared memory must
  be *safe to share* — a faithful record that leaks credentials is a liability, not memory)
  <!-- id: secret-redaction-lint-v4330 | created: 2026-08-13 | last_used: 2026-08-13 | uses: 3 | tier: active | origin: 2026-08-13-222439 -->

- [x] **Shipped v4.32.1 (PATCH) — Mode A `last_session` contradiction fix.** From a **real Mode A
  enable** (2026-08-06, target `~/sandbox/demo`), confirmed by an adversarial protocol audit:
  `ENABLE.md` Step 5b still said a non-migrated enable leaves `last_session: (none yet)`, but Step 5c
  (added later) mandates a **first enable session log** for every fresh enable — so "(none yet)" was
  false the moment the enable completed, and it blinded the multi-agent continuity check (`AGENTS.md`
  reads `last_session` to decide whether another agent family worked last). The contradiction was
  internal to 5b — its own footer bullet already pointed the seeded facts' `origin` at the 5c log.
  **Shipped:** 5b's non-migrated branch now points `last_session` at the 5c log (`<today> | agent:
  <your agent name> (<the 5c log's filename stem>)`, filled when the log is written; Mode C branch
  unchanged; 5c carries the back-reference); template seed `(none yet)` → `{{LAST_SESSION}}`
  placeholder (the `{{BOOTSTRAP_IMPORTS}}` pattern); schema marks `(none yet)` as legacy — a
  value-domain note, not a format change (date+agent-only live values stay valid); `rust-event-bus`
  fixture kept unedited by design behind an `ENABLE_OUTPUT.md` grandfathered-detail note. No code
  surface reads `last_session` (lint/hooks/CI untouched); no docs-site page carries the 5b detail.
  Lockstep: `ENABLE.md` (5b + 5c), templates ×2, example header, `VERSION`→4.32.1, `CHANGELOG`,
  `README` (row + 10-cap trim, drops 4.28.0), `UPGRADE` (row + `4.32.0→4.32.1` rung — re-copy schema;
  optional truth fix for a never-worked enable still showing `(none yet)`). → serves:
  vision-agent-memory (a fresh enable must leave a *true* memory state — the continuity check has to
  work from session one)
  <!-- id: last-session-enable-log-v4321 | created: 2026-08-06 | last_used: 2026-08-13 | uses: 2 | tier: active | origin: 2026-08-06-153509 -->

- [x] **Shipped v4.31.0 (MINOR) — GitLab forge support: forge-aware ritual floor + MR template.** From a
  **GitLab-hosted field report** (2026-07-26): GitLab ignores `.github/` entirely (verified — no shim in
  templates/CODEOWNERS/importer docs). A 5-agent workflow gap-analysis found exactly **two** dead
  artifacts — the **CI floor** (fresh clones had NO ritual backstop; the v4.19.0 guarantee silently
  collapsed) and the **What/Why PR template** — while `.github/` files read by *local* tooling
  (copilot-instructions, skills adapters) were never broken and stay put on every forge. Root cause
  named: "vendor-neutral" had conflated *AI vendor* with *hosting forge*. **Shipped:** `ENABLE.md` forge
  detection (Step 4: remote URL + `.gitlab-ci.yml`/`.gitlab/`; unknown → both sets, additive-safe) +
  forge-matched install (Step 6/8/9 + write-scope); `templates/.gitlab/agent-memory-ci.yml` (same two
  checks; advisory via `allow_failure: exit_codes: [42]`, `AGENT_MEMORY_STRICT=1` gates; `image:
  python:3`, `GIT_DEPTH: 0`); root wiring additive-safe (`templates/.gitlab-ci.yml` verbatim when
  absent — carries the canonical `workflow:rules` guard GitLab requires in the ROOT file for MR
  pipelines; pre-existing file → **add-only `include:` entry, never `workflow:rules`** — that would
  change when the repo's own jobs run; job then rides branch-push pipelines, a sufficient floor);
  `templates/.gitlab/merge_request_templates/Default.md` (auto-applies, all tiers). **Squash guidance
  inverts per forge** (AGENTS.md root + template): GitHub piles trailers (dedup, v4.28.x) — GitLab
  DROPS them (default squash message = MR title only; survive via re-add-at-merge or `%{all_commits}`
  in the project squash template — NOT `%{co_authored_by}`, which credits commit authors only; the
  pre-ship adversarial review caught that misprescription against GitLab's own source, plus a
  missing-`stage:` hazard that could invalidate a target's whole pipeline — both fixed pre-commit).
  Honest limit: GitLab.com runners zero-config; self-managed needs an
  admin-registered runner. Lockstep: ENABLE (detection/install/verify/report/consent/write-scope),
  AGENTS ×2, `.githooks/README` + `init.sh`, `REVIEW.md`,
  DESIGN-ritual-triggers amendment, 6 docs-site pages, `VERSION`→4.31.0, `CHANGELOG`, `README` (row +
  10-cap trim + file tree), `UPGRADE` (row + `4.30.0→4.31.0` rung). Non-goals: CODEOWNERS, issue templates, other
  forges (the forge seam is where they'd slot in). → serves: vision-agent-memory (adoption stays
  "point it at a repo" — on whichever forge the repo lives)
  <!-- id: gitlab-forge-support-v4310 | created: 2026-07-27 | last_used: 2026-07-27 | uses: 3 | tier: active | origin: 2026-07-27-203400 -->

- [x] **(SHIPPED v4.32.0 MINOR, 2026-07-27) Azure DevOps forge support — field installation exists; mechanics
  verified (2026-07-27); maintainer approved and shipped same day.** Delivered exactly per the proposed
  shape below: own-pipeline model (`templates/.azuredevops/agent-memory-ci.yml` — existing
  `azure-pipelines.yml` never touched; script-owned result so STRICT stays a true red), PR template,
  forge detection, activation command REPORTED never silently run, unknown-forge = GitHub+GitLab sets
  only, third squash branch. Ship record: session `2026-07-27-211935` + the `4.31.0→4.32.0` rung.
  Original verified fact sheet kept below for the record: A real installation runs on Azure DevOps, so the
  complaints-=-adoption trigger is satisfied (unlike Bitbucket, below). Verified against
  learn.microsoft.com: **clean wins** — `.azuredevops/pull_request_template.md` auto-applies
  (default-branch-read, `.azuredevops/`→`.vsts/`→`docs/`→root precedence, 4000-char cap); best
  advisory semantics of any forge (`continueOnError: true` → "partially succeeded" tri-state +
  `##vso[task.logissue type=warning]`; Build Validation policy has a notify-only Optional mode); two
  additive seams (multiple pipelines per repo each bound to its own YAML — an own-file job touches
  nothing of theirs; `- template:` local includes, triggers must stay in the main file); needs
  `fetchDepth: 0` (shallow=1 default since sprint 209); `System.PullRequest.*` base vars.
  **The honest asymmetry — activation is not file-driven, twice:** (1) a pipeline is a RESOURCE —
  committing YAML is inert until `az pipelines create --yml-path … --skip-first-run` binds it
  (one-time, scriptable, default permission Contributors; implied CI trigger then runs on pushes);
  (2) Azure Repos ignores the YAML `pr:` trigger — PR-time validation needs the Build Validation
  branch policy (admin settings change; document as optional human step, never made by the tool).
  Microsoft-hosted parallelism needs an Azure-subscription link (self-hosted automatic). Attribution:
  squash drops trailers, no template mechanism, editable at merge — PR-description footer is the
  durable record. **Proposed shape (v4.32.0):** own-pipeline model (`templates/.azuredevops/
  agent-memory-ci.yml` + PR template), ENABLE forge detection (dev.azure.com/visualstudio.com), Step 6
  installs files + REPORTS the one-time activation command (run only at explicit user direction),
  third squash branch, rung. → serves: vision-agent-memory
  <!-- id: ot-azure-devops-forge-next | created: 2026-07-27 | last_used: 2026-07-27 | uses: 2 | tier: active | origin: 2026-07-27-210655 -->

- [ ] **(backlog) Bitbucket forge support — trigger-gated; mechanics pre-verified (2026-07-27).** From a
  maintainer question during the v4.31.0 GitLab release ("investigate viability to include Bitbucket").
  Verified against Atlassian docs (July 2026) so a future field report can act immediately: **(1) the
  clean win** — Bitbucket CLOUD supports a committed `.bitbucket/pull_request_template.md` (KB Apr
  2026; read from the PR's SOURCE branch; overrides the settings field) — the What/Why template is
  seedable file-based. **(2) The CI floor cannot keep its promise there** — committing
  `bitbucket-pipelines.yml` runs nothing until a repo ADMIN enables Pipelines (`repository:admin`, a
  forge setting the agent must never touch); free tier = 50 build-min/month; and there is NO additive
  include seam (the `import` mechanism is Premium **and** whole-pipeline replacement — adding to an
  existing file means inserting a step into their sequential list, against add-only). Advisory
  semantics do exist (`on-fail: strategy: ignore`); PR pipelines carry base-SHA vars
  (`BITBUCKET_PR_DESTINATION_COMMIT`); clone needs `depth: full`. **(3) Cloud-only** — Data Center has
  NO native Pipelines and NO committed template file (settings-UI only): enterprise Bitbucket gets
  nothing. **(4) Attribution** — squash message not templatable on Cloud, trailers mangle into bullet
  lists, UI ignores Co-authored-by (BSERV-10529 closed won't-fix) — the PR-description footer is the
  only durable record. **Decision (maintainer, 2026-07-27): defer — don't build speculatively.** The
  pre-scoped viable shape when a Bitbucket team reports the failure class:
  `.bitbucket/pull_request_template.md` (clean) + an optional fresh-file-only pipelines floor carrying
  the admin-toggle honest limit + never editing an existing pipelines file (report a recommendation
  instead). → serves: vision-agent-memory
  <!-- id: ot-bitbucket-forge-backlog | created: 2026-07-27 | last_used: 2026-07-27 | uses: 2 | tier: working | origin: 2026-07-27-203400 -->

- [x] **Shipped v4.30.0 (MINOR) — stack-aware `.gitignore` build-output seed.** From a **greenfield
  field case** (`mercury` — a Rust port of mercury-composable started from an empty repo, enabled
  2026-07-15 at v4.29.1): the installed `.gitignore` is deliberately **AI-infrastructure-scoped**, so
  when the stack landed *after* enable, the first `cargo build` polluted `git status` until the user
  hand-added `target/`. The gap splits by **when the stack is knowable**: (a) brownfield — `ENABLE.md`
  **Step 7** now appends the detected stack's canonical build-output entries under a second,
  separately-scoped sentinel (`# === agent-memory: build output (stack-aware seed …) ===`; table: Rust
  `target/`; Node `node_modules/`, `dist/`; Python venvs; Java/Kotlin `target/`, `build/`, `*.class`;
  .NET `bin/`, `obj/`; Go none) — add-only, de-duplicating (a no-op where entries already exist);
  (b) greenfield — nothing to seed at enable, so **Step 5b** seeds a `Greenfield — no code yet` Open
  Thread carrying the "seed when the stack lands" action for the working agent to apply (also fixes
  that the greenfield thread was previously improvised, not protocol); Step 8 verifies, Step 9 reports.
  **Explicit non-goal:** minimal seed, never a gitignore manager (no IDE/OS/coverage entries).
  Operator-side only — templates unchanged (AI-infra scoping is by design), no shape/skill/adapter
  change. Lockstep: `ENABLE.md` (5b + 7 + 8 + 9), `VERSION`→4.30.0, `CHANGELOG`, `README` (row +
  10-cap trim), `UPGRADE` (row + `4.29.1→4.30.0` rung with optional additive target steps). → serves:
  vision-agent-memory (faithful enablement — the first build after enable must not dirty the repo)
  <!-- id: gitignore-stack-seed-v4300 | created: 2026-07-15 | last_used: 2026-07-15 | uses: 1 | tier: active | origin: 2026-07-15-232735.md -->

- [x] **Shipped v4.29.1 (PATCH) — template import blocks → `{{BOOTSTRAP_IMPORTS}}` placeholder.** From a
  **GitHub Copilot assessment of v4.29.0** (its "Dogfood Finding"), **corroborated live on Claude Code**
  the same day: runtimes that auto-load directory-scoped instruction files picked up
  `templates/CLAUDE.md` inside the tool repo, and since `@`-imports resolve *relative to the containing
  file*, its v4.29.0 import block pulled the **placeholder template stubs** (`templates/AGENTS.md`,
  `templates/memory/*` — `{{PROJECT_NAME}}` junk, "(none yet)" state, conflicting identity lines) into
  live context as instructions. Tool-repo-only (targets have no `templates/`), but a real dogfood
  hazard v4.29.0 amplified. **Fix:** the two templates now hold a `{{BOOTSTRAP_IMPORTS}}` placeholder;
  `ENABLE.md` Step 6 defines the per-vendor literal blocks (fenced — never import-parsed) and expands at
  install, so **installed output stays byte-identical to v4.29.0's**; the `4.28.4→4.29.0` rung was
  amended to reference the Step 6 blocks (not the templates) so a ladder run can't copy the placeholder
  verbatim. Honest residual: direct nested-`AGENTS.md` auto-load (pre-4.29.0 runtime behavior) may still
  surface `templates/AGENTS.md`; the amplification is what the patch removes. Root bootstraps keep live
  imports (the feature, dogfooded). Lockstep: templates ×2, `ENABLE.md` Step 6, `UPGRADE` (row + rung +
  4.29.0-rung amendment), `VERSION`→4.29.1, `CHANGELOG`, `README` (row + 10-cap trim). Targets:
  version-stamp only. → serves: vision-agent-memory (the tool's own repo must stay a faithful memory
  environment while it dogfoods the features it ships)
  <!-- id: template-import-bleed-v4291 | created: 2026-07-12 | last_used: 2026-08-06 | uses: 2 | tier: active | origin: 2026-07-12-030710 -->

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
  <!-- id: coauthor-stable-identity-v4280 | created: 2026-06-30 | last_used: 2026-07-27 | uses: 2 | tier: active | origin: 2026-06-30-054342 -->

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
  <!-- id: pr-what-why-convention-v4270 | created: 2026-06-29 | last_used: 2026-06-30 | uses: 2 | tier: archive-candidate | origin: 2026-06-29-175644 -->

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
  <!-- id: pinned-tier-refinement-v4261 | created: 2026-06-28 | last_used: 2026-06-28 | uses: 1 | tier: archive-candidate | origin: 2026-06-28-181738 -->

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
  <!-- id: refresh-metadata-builtin-v4260 | created: 2026-06-28 | last_used: 2026-06-28 | uses: 2 | tier: archive-candidate | origin: 2026-06-28-175909 -->

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
  <!-- id: archive-fact-builtin-v4250 | created: 2026-06-28 | last_used: 2026-06-28 | uses: 1 | tier: archive-candidate | origin: 2026-06-28-172159 -->

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
  <!-- id: bp-multi-user | created: 2026-06-15 | last_used: 2026-08-06 | uses: 5 | tier: active | origin: 2026-06-15-000531 -->
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
  <!-- id: bp-before-session-presence | created: 2026-07-12 | last_used: 2026-07-12 | uses: 3 | tier: active | origin: 2026-07-12-013817 -->

### Backlog — vNext (temporal & supersession) + beyond
> From the 2026-06-13 industry-alignment assessment:
> `docs/assessments/2026-06-13-industry-alignment.md`. Verdict: on track; distinctive
> on event-sourcing/determinism/governance; one real gap = temporal/supersession.
> Re-run the assessment after meaningful iterations and compare its scorecard.

- [ ] **Dogfooding on real work (ongoing).** Already delivering: the simple-proxy
  enable surfaced v3.1.0 (`.gitignore`), and the simple-proxy Node→Rust refactor's
  field report drove v3.2.0 (protocol clarifications). Keep feeding real-work insights
  back into this backlog. (Stated 2026-06-13.)
  <!-- id: backlog-real-work-dogfood | created: 2026-06-13 | last_used: 2026-08-13 | uses: 16 | tier: active -->

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
  schema `repo:` guidance, and flagged by `memory-lint` `[secret-material]` since v4.33.0.)
- Any secrets — PII and credentials — must be redacted from session memory, never
  committed. (Stated 2026-08-13, after a client-side DLP catch; enforced via the
  AGENTS.md redaction rule + `memory-lint` `[secret-material]`, v4.33.0.)
