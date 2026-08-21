# Continuity — agent-memory

> Shared ground truth for this tool's own development state.

---

## Project State

- **project:** agent-memory
- **status:** v4.37.0 — a vendor-neutral, no-code (markdown) shared-AI-memory + AI-enablement tool. Three shared layers: **backward memory** (v3.x — fact metadata + ids, decay/review/archive), a **forward VBDI cognitive loop** (v4.0 — Vision→Blueprint→Design→Impl over the memory substrate), and a **cross-vendor skills layer** (v4.1+ — neutral committed `agent-skills/` + a runnable `sync-adapters`; six adapter targets: Claude/Gemini/Cursor/Kiro/Copilot/Antigravity). Agent-as-runtime; `memory/` is committed + shared; activation enters through a one-line root `AGENTS.md` shim to the canonical `memory/PROTOCOL.md` (v4.37.0); enable/upgrade converge **declaratively** against a `MANIFEST.md` target state via the reconcile helper — O(diff), not O(steps/rungs) (v4.35.0). Built-in skills: `memory-lint`, `second-opinion`+`apply-critique`, `sync-adapters`, `harvest-knowledge`, `archive-fact`, `refresh-metadata`. Vendor-neutral, **forge-aware** ritual triggers (composable pre/post-commit **fragment dispatchers** over `.githooks/<hook>.d/*` — pre-commit secret guard (v4.34.0) + post-commit ritual capture as managed `50-` fragments (v4.36.0) — plus a CI floor matched to the hosting forge: GitHub Actions, GitLab CI, or Azure Pipelines, v4.31.0–v4.32.0) with first-run self-init; Windows LF hardening. **Per-version history lives in `UPGRADE.md` (the version ladder) + `memory/sessions/` — kept OUT of this line by design (v4.22.0): `status` is a short current-state descriptor, not a changelog, so this shared line doesn't become a merge-conflict hotspot.** `.agent/version.md` is the canonical version. Validated across six vendors (Claude, Gemini, Cursor, Kiro, Copilot CLI, Antigravity).
- **last_enabled:** 2026-06-12
- **last_session:** 2026-08-21 | agent: Claude Code (2026-08-21-052644)
- **last_review:** 2026-08-20 | through 2026-08-20-223624
- **last_invariant_check:** 2026-08-14 | through 2026-08-14-011037
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
- Git hook entrypoints dispatch ordered fragments (ADR-0007) — `.githooks/pre-commit` and
  `.githooks/post-commit` stay minimal and stable; executable `.githooks/<hook>.d/*` fragments run
  in C-locale filename order, all fragments run, and the first non-zero status is returned.
  Agent-memory owns only its `50-` fragments; differently named fragments belong to other layers
  and upgrades preserve them.
  <!-- id: git-hook-fragment-dispatch | created: 2026-08-20 | last_used: 2026-08-21 | uses: 3 | tier: active | origin: 2026-08-20-210047 -->

## Open Threads

- [x] **Shipped v4.36.0 (MINOR) — composable Git hook dispatchers.** The `pre-commit`/`post-commit`
  monoliths became deterministic fragment dispatchers; the secret guard and ritual capture moved
  intact to managed `50-` fragments (+2 `MANIFEST.md` rows). All executable fragments run in
  filename order and the first failure propagates, so pre-commit still enforces while every layer
  reports; tests pin order, filtering, arg forwarding, continue-after-failure, status propagation,
  empty-dir. Install, upgrade, LF hardening, docs, ADR-0007 in lockstep. Renumbered 4.35.0→4.36.0
  on rebase (4.35.0 shipped upstream as `bp-reconcile-target-state`); the `id` keeps its original
  slug — its origin log is immutable. → serves: vision-agent-memory (shared automation composes
  without ownership collisions and stays directly testable)
  <!-- id: hook-dispatchers-v4350 | created: 2026-08-20 | last_used: 2026-08-20 | uses: 1 | tier: active | origin: 2026-08-20-210047 -->

- [x] **(blueprint — SHIPPED v4.35.0 MINOR, 2026-08-20) Target-state reconcile — enable/upgrade in
  O(diff), not O(steps/rungs).** Field report (2026-08-19): a fresh Mode A enable of a nearly-empty
  **AI-hackathon monorepo** took >10 min; maintainer direction — compare a repo's current state to
  the current tool's target state. Cause: an imperative, history-ordered protocol (989-line
  `ENABLE.md`, ~60 files write-by-write; 80-rung ladder = O(rungs-behind)) doing ~80% convergence
  work — a fix the design already implied (idempotent rungs = reconciliation semantics; the 4-row
  proto-manifest). **Shipped:** `MANIFEST.md` (40 rows
  — target | source | policy: verbatim / verbatim-dir / seed-copy / sentinel-merge / seed-generate
  / stamp | forge — + a **Semantic steps** table: the ladder's 14 non-mechanical migrations,
  version-gated, each pointing at its rung); `scripts/reconcile.py`+`.mjs` (byte-parity, 25 mirror
  tests each, stdlib, subprocess-free; dry-run default = the consent artifact; `--apply` = one
  mechanical pass + printed judgment work-list; `--check-manifest` = release lockstep gate; never
  deletes / never touches seeded files / never edits a pre-existing `.gitlab-ci.yml` / never
  stamps (agent stamps last) / realpath guard / refuses the tool repo + `~`; azdo only on positive
  detection). `ENABLE.md` restructured (Reconcile Core; Mode A = consent→analysis→reconcile→
  generation; Mode B = reconcile→semantic steps→stamp; Mode C reconciles only AFTER migration;
  Steps 5–7 tagged [reconcile-covered], prose = spec + no-runtime fallback); `UPGRADE.md` =
  per-version record + semantic detail (release checklist gains manifest lockstep); new
  archive-INDEX template; `docs/DESIGN-reconcile.md`; 3 docs-site pages.
  **Verified:** 25/25 ×2 runtimes, byte parity incl. error paths, scratch e2e, live read-only
  probes — the 4.34.1 AI-hackathon repo's dry-run reproduced its pending rung *exactly*;
  mercury-composable surfaced 11 managed `.gitignore` entries no rung ever back-filled (drift made
  visible — §5i warn-before-clobber now *checked* per run). **Pre-ship adversarial review (2
  lenses; dispositions in the log): 2 blockers fixed** — newer-than-tool target silently
  downgraded → the hard Mode B stop, mechanized; mjs path guard missed symlink resolution (could
  write outside the target) → non-strict-realpath parity — **+ 6 hardenings**, all test-pinned
  (CRLF, wrong-kind/UTF-8/home, hooksPath, worktree, forge); mechanics swept claims (fixed). Judgment
  boundary per the mechanize-arithmetic-not-judgment doctrine: the manifest absorbs arithmetic;
  analysis, seeding, vision gate, arbitration, semantic merges stay agent-owned. Lockstep: VERSION,
  CHANGELOG, README (row + 10-cap trim drops 4.32.0), UPGRADE (flow + checklist + row + rung).
  → serves: vision-agent-memory (adoption stays "point it at a repo" — in minutes, at any version)
  <!-- id: bp-reconcile-target-state | created: 2026-08-20 | last_used: 2026-08-21 | uses: 3 | tier: active | supersedes: ot-mode-b-automation-backlog | origin: 2026-08-20-223624 -->

- [x] **(blueprint) Relocate the memory protocol behind a one-line root `AGENTS.md`
  pointer and optimize it for activation, efficiency, instruction accuracy, and
  terseness.** The maintainer confirmed the boundary applies to both this tool and
  enabled targets, preserves the tool-vs-target protocol split, and ships through a
  v4.37.0 upgrade. A full-mode spec and plan are under
  `docs/specs/memory-protocol-pointer/`. Rebased onto v4.36.0 as v4.37.0: both 61-byte shims,
  optimized tool/target protocols, lifecycle/release wiring, a durable
  instruction-versus-evidence boundary, and fail-closed collision handling are complete.
  Strict gates, target-local Git recovery/idempotence walkthrough, and final adversarial,
  quality, and security reviews pass. **PR #24 multi-vendor review, 2026-08-21:** dry-run's
  closing hint now names the real next move (it pointed at an `--apply` that refuses with zero
  writes — the consent artifact must agree with apply; test-pinned both runtimes); `status:`
  restored after a WIP marker leaked in (v4.22.0 anti-pattern); protocol row stays `seed-copy`.
  → serves: vision-agent-memory (lower default context cost without weakening deterministic,
  cross-vendor activation)
  <!-- id: protocol-pointer-enterprise-activation | created: 2026-08-20 | last_used: 2026-08-21 | uses: 7 | tier: active | origin: 2026-08-20-204952 -->

- [ ] **Protocol-text propagation is a per-release obligation, not a mechanism.**
  `memory/PROTOCOL.md` is `seed-copy`, so an installed protocol is never re-copied — deliberate
  (the v4.37.0 rung merges the old root's local directives into it, and a re-copy could drop
  them irrecoverably), but it ends the automatic propagation the old `verbatim` `AGENTS.md` hub
  had, and ~half of recent releases edited protocol text. Now stated in `MANIFEST.md`'s row
  notes + the `UPGRADE.md` manifest-lockstep rule: any release editing
  `templates/memory/PROTOCOL.md` ships a Semantic steps row (re-copy a still-stock protocol,
  arbitrate a customized one per §5i). **Open for the maintainer:** keep that cost, or move the
  row to `verbatim` and lean on §5i drift arbitration — truer to the house model, but it weakens
  AC-MP-07/08's "preserved without loss". → serves: vision-agent-memory (a protocol fix must
  reach the repos running it)
  <!-- id: ot-protocol-text-propagation | created: 2026-08-21 | last_used: 2026-08-21 | uses: 1 | tier: working | origin: 2026-08-21-052644 -->

- [ ] **Field canary: AGENTS.md-native activation is unproven.** Codex, Kiro, and Antigravity
  auto-load root `AGENTS.md`, so v4.37.0 trades their inline protocol for a 61-byte imperative
  plus one read-action — the v4.29.0 failure class (pointer prose, skipped under task pressure)
  reintroduced for exactly the enterprise-IDE class this targets. Mitigated by the single
  unambiguous imperative and the activation-first rewrite, motivated by a real ~20 KB/session
  tax, but never observed on a live Kiro or Codex session: treat activation there as unvalidated
  until a field canary confirms it (the v4.29.0 attestation pattern). → serves:
  vision-agent-memory (cross-vendor activation is a claim to observe, not assume)
  <!-- id: ot-agents-native-activation-canary | created: 2026-08-21 | last_used: 2026-08-21 | uses: 1 | tier: working | origin: 2026-08-21-052644 -->

- [x] **Shipped v4.34.2 (PATCH) — `[secret-material]`: the guard's own opt-down knob is not a
  credential.** Field issue from the **mercury-composable team** (2026-08-19, during their v4.34.0
  hook regression test): the pre-commit guard's blocking message prints
  `AGENT_MEMORY_SECRET_GUARD=advisory`, and any memory file documenting that guidance then flagged
  as a `credential-assignment` (key contains `SECRET`; `advisory` meets the value floor; no
  exemption path applied) — the tool taught a phrase, then blocked its quotation. **Their analysis
  was code-accurate and their fix shape was endorsed as-is** (exact-key, value-constrained
  exemption; their rejected alternatives — global `advisory` placeholder, widening `ENUM_KEY_RE` —
  were rejected for the right reasons). **The v4.33.2 verbatim-fixture lesson caught a real
  variant pre-ship:** the guard's guidance line ends `…=advisory)` and the closing paren rides
  into the captured value, so the exemption tolerates trailing `).,` punctuation while staying
  token-constrained (`advisory`/`enforcing` only — any other value under that key still flags; no
  smuggling envelope; non-echo preserved). Both runtimes at parity, verbatim mirror fixtures
  (50/50). **Secondary question resolved as a doc note:** AWS's canonical doc-example keys still
  flag by design — redact or *visibly* waive (`lint:allow-secret-material`); no invisible built-in
  whitelist (SKILL.md body note; description unchanged → adapters untouched). Re-probed: this repo
  0/0; mercury-composable 0 `[secret-material]` with the fixed script. Lockstep: skill files ×5,
  `VERSION`→4.34.2, `CHANGELOG`, `README` (row + 10-cap trim, drops 4.31.0), `UPGRADE` (row +
  `4.34.1→4.34.2` rung incl. the drop-obsolete-waivers step). → serves: vision-agent-memory (the
  advisory stays signal — a guard must never block the documentation of its own controls)
  <!-- id: secret-fp-self-knob-v4342 | created: 2026-08-19 | last_used: 2026-08-19 | uses: 1 | tier: archive-candidate | origin: 2026-08-19-203132 -->

- [x] **Shipped v4.34.0 (MINOR) — pre-commit secret guard: prevention on both surfaces (memory +
  config).** From the maintainer's post-DLP-arc question + the decisive incident detail (the
  leak's *origin* was a Postman JSON + an OpenShift YAML with live credentials). `.githooks/
  pre-commit` scans **staged** `memory/**.md` (full profile) + config files (credential-class;
  JSON/properties waivers in the committed `.agent/secret-scan-ignore`); `memory-lint
  --scan-files` powers it + the changed-config scan in all three forge CI wrappers; detector
  probe-tuned on a 661-file live corpus to 0 FPs. **Enforcing by default** (maintainer decision —
  the deliberate, scoped exception to the advisory doctrine; secrets carry irreversible
  after-the-fact cost); `AGENT_MEMORY_SECRET_GUARD` opts down, `--no-verify` bypasses once, the
  CI floor stays advisory. Verified 49/49 ×2 runtimes + 14 scratch hook paths; both live corpora
  clean. **Fold-up v4.34.1 (same day):** finding lines no longer repeat the advisory tail —
  guidance prints once per run. Full detail: origin log + the `4.33.4→4.34.0` rung. → serves:
  vision-agent-memory (shared memory must be safe to share — guarded at write, commit, AND push
  time, wherever the secret lands)
  <!-- id: pre-commit-secret-guard-v4340 | created: 2026-08-14 | last_used: 2026-08-19 | uses: 3 | tier: archive-candidate | origin: 2026-08-14-021712 -->

- [ ] **Re-verify invariants (due):** confirm `target-repo-scope-only`,
  `never-delete-vendor-files`, `never-pick-a-winner`, `no-build-step-agent-run`,
  `upgrades-additive`, and the `vision-agent-memory` Vision still hold, or supersede any
  that do not (`DECAY.md` §9).
  <!-- id: ot-reverify-invariants-20260814 | created: 2026-08-14 | last_used: 2026-08-14 | uses: 1 | tier: working | origin: 2026-08-14-011037 -->

- [x] **Hardened `memory-lint` test fixtures against repository secret-scanner false
  positives without a release bump.** The Python and Node mirror suites no longer commit
  complete secret/PII signatures: tests deterministically construct shape-constrained dummy
  values at runtime, store them in test-scoped environment variables, and remove them after
  each case. Provider shapes, generic credential assignments, template fallbacks, private-key
  markers, PII, waiver behavior, non-echo guarantees, and negative controls remain covered
  (46/46 in each runtime). This changes tests only, so `VERSION` remains 4.33.4. → serves:
  vision-agent-memory (security tooling should not make the repository itself noisy to
  enterprise scanners)
  <!-- id: secret-test-fixtures-env | created: 2026-08-14 | last_used: 2026-08-21 | uses: 2 | tier: active | origin: 2026-08-14-011037 -->

- [x] **Shipped v4.33.4 (PATCH) — reject non-empty `${…}` defaults in `[secret-material]`.**
  Post-release review caught that v4.33.3's broad brace-delimited placeholder exemption fixed
  empty-default and dotted-reference false positives but also trusted literal fallbacks.
  `${NAME}`, `${NAME:}`, and dotted references remain safe; a value such as
  `client_secret=${CLIENT_SECRET:-RealSecret123}` now flags without echoing the value. Python <!-- lint:allow-secret-material -->
  and Node remain byte-identical, 46 mirror tests each. → serves: vision-agent-memory
  <!-- id: secret-template-default-v4334 | created: 2026-08-14 | last_used: 2026-08-14 | uses: 3 | tier: archive-candidate | origin: 2026-08-14-003952 -->

- [x] **Shipped v4.33.3 (PATCH) — security-review hardening for `[secret-material]`.** A
  fresh-context security review judged v4.33.x useful defense-in-depth but found four concrete
  gaps: CI wrappers never passed `--strict` (so WARN findings exited 0 before
  `AGENT_MEMORY_STRICT` could act); v4.33.1's global ALL-CAPS exemption also trusted uppercase
  secrets; quoted JSON/YAML assignments, Authorization headers, and embedded placeholder words
  bypassed detection; Mode C migration lacked mandatory redaction/lint triage. Fixed all four:
  forge wrappers now deliberately consume strict lint status while preserving advisory defaults;
  enum exemption is key-scoped; placeholder matching is anchored; pasted-output formats flag
  without value echo; migration redacts and verifies before commit. Python/Node byte-identical,
  46 mirror tests each. **Fold-in (pre-tag, Claude Code post-merge review):** the live-target
  probe the review had skipped caught the tightened template pattern rejecting default-value /
  dotted env-var forms — `${REDIS_PASSWORD:}`, mercury-composable's own documented safe pattern
  for secrets, 2 live FPs; the `${…}` alternative now accepts any brace-delimited reference
  (still fullmatch-anchored), verbatim fixture added, both live targets re-probe zero findings.
  → serves: vision-agent-memory (shared memory is safe to share, and the
  advertised strict gate is real)
  <!-- id: secret-review-hardening-v4333 | created: 2026-08-13 | last_used: 2026-08-14 | uses: 5 | tier: archive-candidate | origin: 2026-08-13-235301 -->

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
  <!-- id: secret-fp-backtick-v4332 | created: 2026-08-13 | last_used: 2026-08-19 | uses: 4 | tier: archive-candidate | origin: 2026-08-13-231459 -->

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
  <!-- id: secret-fp-enum-constants-v4331 | created: 2026-08-13 | last_used: 2026-08-19 | uses: 4 | tier: archive-candidate | origin: 2026-08-13-225859 -->

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
  <!-- id: secret-redaction-lint-v4330 | created: 2026-08-13 | last_used: 2026-08-19 | uses: 9 | tier: archive-candidate | origin: 2026-08-13-222439 -->

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
  <!-- id: last-session-enable-log-v4321 | created: 2026-08-06 | last_used: 2026-08-13 | uses: 2 | tier: archive-candidate | origin: 2026-08-06-153509 -->

- [x] **Shipped v4.31.0 (MINOR) — GitLab forge support: forge-aware ritual floor + MR template.** From a
  **GitLab-hosted field report** (2026-07-26): GitLab ignores `.github/` entirely — exactly two
  installed artifacts were dead there (the CI floor and the What/Why template); local-tooling
  `.github/` files stay put on every forge. Root cause named: "vendor-neutral" had conflated *AI
  vendor* with *hosting forge*. Shipped ENABLE forge detection (unknown → both sets, additive-safe)
  + matched install: `.gitlab/agent-memory-ci.yml` (advisory via `allow_failure: exit_codes: [42]`),
  root wiring additive-safe (verbatim root file when absent — carries the required `workflow:rules`;
  pre-existing → **add-only `include:` + mandatory stage check, never `workflow:rules`**), MR
  template (auto-applies, all tiers). **Squash guidance inverts per forge:** GitHub piles trailers
  (dedup) — GitLab DROPS them (re-add at merge or `%{all_commits}`; NOT `%{co_authored_by}` — the
  pre-ship review caught that misprescription + a missing-`stage:` pipeline killer). Honest limit:
  self-managed GitLab needs an admin-registered runner. Full detail: origin log + the
  `4.30.0→4.31.0` rung. → serves: vision-agent-memory (adoption stays "point it at a repo" — on
  whichever forge the repo lives)
  <!-- id: gitlab-forge-support-v4310 | created: 2026-07-27 | last_used: 2026-07-27 | uses: 3 | tier: archive-candidate | origin: 2026-07-27-203400 -->

- [x] **(SHIPPED v4.32.0 MINOR, 2026-07-27) Azure DevOps forge support.** A real field installation
  satisfied the complaints-=-adoption trigger (unlike Bitbucket, below); mechanics verified against
  learn.microsoft.com pre-ship; maintainer approved and shipped same day. **Own-pipeline model:**
  `.azuredevops/agent-memory-ci.yml` is complete and self-contained — an existing
  `azure-pipelines.yml` is never touched; best advisory semantics of any forge (`##vso` warnings +
  "partially succeeded" tri-state; STRICT stays a true red); PR template auto-applies
  (default-branch-read, 4000-char cap); needs `fetchDepth: 0`. **Honest asymmetry — activation is
  not file-driven, twice:** a pipeline is a RESOURCE (inert until the one-time `az pipelines create
  … --skip-first-run` binding — REPORTED, never silently run, after push), and Azure Repos ignores
  YAML `pr:` (PR-time validation = Build Validation branch policy — admin; documented, never
  configured). Squash drops trailers (no template mechanism; re-add at completion — the
  PR-description footer is the durable record). Unknown forge = GitHub+GitLab sets only. Ship
  record: session `2026-07-27-211935` + the `4.31.0→4.32.0` rung. → serves: vision-agent-memory
  <!-- id: ot-azure-devops-forge-next | created: 2026-07-27 | last_used: 2026-07-27 | uses: 2 | tier: archive-candidate | origin: 2026-07-27-210655 -->

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
  <!-- id: gitignore-stack-seed-v4300 | created: 2026-07-15 | last_used: 2026-07-15 | uses: 1 | tier: archive-candidate | origin: 2026-07-15-232735.md -->

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
  <!-- id: template-import-bleed-v4291 | created: 2026-07-12 | last_used: 2026-08-06 | uses: 2 | tier: archive-candidate | origin: 2026-07-12-030710 -->

- [ ] **(backlog) Before-session presence for Cursor/Kiro — path-scoped steering imports.** From a
  maintainer question after v4.29.0 shipped ("what about other vendors' entry points?"). v4.29.0
  covered the only two entry files with native import syntax (`CLAUDE.md` `@path`, `GEMINI.md`
  `@./path.md`); AGENTS.md-native runtimes (Codex, Kiro, Antigravity) auto-load the one-line shim —
  only the `AGENTS.md → memory/PROTOCOL.md` hop stays voluntary; Copilot/`.cursorrules`/`.windsurfrules` have
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
  <!-- id: coauthor-stable-identity-v4280 | created: 2026-06-30 | last_used: 2026-07-27 | uses: 2 | tier: archive-candidate | origin: 2026-06-30-054342 -->

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
  <!-- id: bp-greenfield | created: 2026-06-15 | last_used: 2026-08-20 | uses: 2 | tier: active | origin: 2026-06-15-000531 -->
- [ ] **(blueprint)** Multi-user concurrent contribution — mostly supported (shared
  committed `memory/`, multi-agent continuity, collision-safe session filenames); validate
  and harden for *simultaneous* contributors. → serves: vision-agent-memory
  <!-- id: bp-multi-user | created: 2026-06-15 | last_used: 2026-08-20 | uses: 6 | tier: active | origin: 2026-06-15-000531 -->
- [ ] **(blueprint)** *(optional)* SDLC overlay for targets — a scrum-inspired profile a
  target *owner* can opt into: a `(sprint)` tag over Blueprint gaps + a sprint-boundary
  review, **no points/velocity/ceremony**. Not core; only if a real target wants it. The
  memory design is already **process-neutral** and survives an overlay (`DECAY.md` §12 /
  `docs/DESIGN-vbdi-lifecycle.md` §13): ceremony + scoring live in the target's own space,
  never in `memory/`. → serves: vision-agent-memory
  <!-- id: bp-sdlc-overlay | created: 2026-06-15 | last_used: 2026-06-15 | uses: 1 | tier: active | origin: 2026-06-15-010142 -->
- [x] **(blueprint — SHIPPED v4.29.0 MINOR, 2026-07-12)** Before-session context *presence* — the
  read chain was advisory prose, empirically skipped under task pressure (child-repo field
  report, 2026-07-11: skill-unawareness, off-model engagement, rework). Shipped native
  `@`-imports in `templates/CLAUDE.md` + `templates/GEMINI.md` (hub + core memory files
  structurally present on import-capable runtimes; Gemini `@./` form, `.md`-only; imports stay in
  per-vendor bootstraps — `AGENTS.md` stays vendor-neutral) + an **opt-in** Claude Code
  SessionStart recipe in `docs/optional-ritual-hook.md` (never installed by default); the
  attestation canary stays downstream. Honest limits: imports can't express `memory/sessions/`
  (dynamic paths); Cursor/Windsurf/Copilot keep prose pointers; imported files enter context
  every session, so the continuity-bloat controls became load-bearing. Import syntax verified
  against both vendors' docs pre-ship. Full detail: origin log + the `4.28.4→4.29.0` rung.
  → serves: vision-agent-memory (the memory layer is *present* every session, not contingent on
  the agent choosing to read)
  <!-- id: bp-before-session-presence | created: 2026-07-12 | last_used: 2026-07-12 | uses: 3 | tier: archive-candidate | origin: 2026-07-12-013817 -->

### Backlog — vNext (temporal & supersession) + beyond
> From the 2026-06-13 industry-alignment assessment:
> `docs/assessments/2026-06-13-industry-alignment.md`. Verdict: on track; distinctive
> on event-sourcing/determinism/governance; one real gap = temporal/supersession.
> Re-run the assessment after meaningful iterations and compare its scorecard.

- [ ] **Dogfooding on real work (ongoing).** Already delivering: the simple-proxy
  enable surfaced v3.1.0 (`.gitignore`), and the simple-proxy Node→Rust refactor's
  field report drove v3.2.0 (protocol clarifications). Keep feeding real-work insights
  back into this backlog. (Stated 2026-06-13.)
  <!-- id: backlog-real-work-dogfood | created: 2026-06-13 | last_used: 2026-08-20 | uses: 18 | tier: active -->

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
  `memory/PROTOCOL.md` redaction rule + `memory-lint` `[secret-material]`, v4.33.0.)
