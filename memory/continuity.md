# Continuity — agent-memory

> Shared ground truth for this tool's own development state.

---

## Project State

- **project:** agent-memory
- **status:** v4.38.0 — a vendor-neutral, no-code (markdown) shared-AI-memory + AI-enablement tool. Three shared layers: **backward memory** (v3.x — fact metadata + ids, decay/review/archive), a **forward VBDI cognitive loop** (v4.0 — Vision→Blueprint→Design→Impl over the memory substrate), and a **cross-vendor skills layer** (v4.1+ — neutral committed `agent-skills/` + a runnable `sync-adapters`; six adapter targets: Claude/Gemini/Cursor/Kiro/Copilot/Antigravity). Agent-as-runtime; `memory/` is committed + shared; activation enters through a one-line root `AGENTS.md` shim to the canonical `memory/PROTOCOL.md` (v4.37.0; consumer-product repos may carry the sanctioned contributor/consumer fork, v4.38.0); enable/upgrade converge **declaratively** against a `MANIFEST.md` target state via the reconcile helper — O(diff), not O(steps/rungs) (v4.35.0). Built-in skills: `memory-lint`, `second-opinion`+`apply-critique`, `sync-adapters`, `harvest-knowledge`, `archive-fact`, `refresh-metadata`. Vendor-neutral, **forge-aware** ritual triggers (composable pre/post-commit **fragment dispatchers** over `.githooks/<hook>.d/*` — pre-commit secret guard (v4.34.0) + post-commit ritual capture as managed `50-` fragments (v4.36.0) — plus a CI floor matched to the hosting forge: GitHub Actions, GitLab CI, or Azure Pipelines, v4.31.0–v4.32.0) with first-run self-init; Windows LF hardening. **Per-version history lives in `UPGRADE.md` (the version ladder) + `memory/sessions/` — kept OUT of this line by design (v4.22.0): `status` is a short current-state descriptor, not a changelog, so this shared line doesn't become a merge-conflict hotspot.** `.agent/version.md` is the canonical version. Validated across six vendors (Claude, Gemini, Cursor, Kiro, Copilot CLI, Antigravity).
- **last_enabled:** 2026-06-12
- **last_session:** 2026-08-22 | agent: Claude Code (2026-08-22-174047)
- **last_review:** 2026-08-22 | through 2026-08-22-174047
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

- [x] **Shipped v4.38.0 (MINOR) — consumer routing + close-record economy.** From the
  mercury-composable onboarding handoff (ratified 2026-08-21): sanctioned root fork
  (`fork-ok`; the live artifact pinned verbatim in both suites), consumers-exit-here
  step-0, 3–6-line close records + review-time condensation + `[closed-thread-bloat]`
  (knob 150), optional ready-to-work checkpoint; first exercise of the protocol-propagation
  semantic row. Lesson: my ≤8-line bound from the handoff's *paraphrase* rejected the live
  11-line fork — verbatim fixtures, third strike. → serves: vision-agent-memory
  <!-- id: onboarding-efficiency-v4380 | created: 2026-08-21 | last_used: 2026-08-22 | uses: 1 | tier: working | origin: 2026-08-22-010250 -->

- [x] **Shipped v4.36.0 (MINOR) — composable Git hook dispatchers.** Hook entrypoints became
  fragment dispatchers over `.githooks/<hook>.d/*`; guard + ritual capture moved intact to
  managed `50-` fragments (PR #22, first external contribution; ADR-0007). Lesson: the id
  keeps its dev-numbered slug after a rebase renumber — origin logs are immutable. Full
  detail: origin log + the `4.35.0→4.36.0` rung. → serves: vision-agent-memory
  <!-- id: hook-dispatchers-v4350 | created: 2026-08-20 | last_used: 2026-08-20 | uses: 1 | tier: archive-candidate | origin: 2026-08-20-210047 -->

- [x] **(blueprint — SHIPPED v4.35.0 MINOR, 2026-08-20) Target-state reconcile — enable/upgrade
  in O(diff), not O(steps/rungs).** From the >10-min AI-hackathon enable field report:
  `MANIFEST.md` declares the target state; `scripts/reconcile.py`/`.mjs` (byte-parity twins)
  converge a repo against it — dry-run consent artifact, one mechanical `--apply`, judgment
  stays agent-owned. Pre-ship adversarial review fixed 2 blockers (silent downgrade; mjs
  symlink escape). Lesson: mechanize arithmetic, never judgment. Full detail: origin log +
  the `4.34.2→4.35.0` rung + `docs/DESIGN-reconcile.md`. → serves: vision-agent-memory
  <!-- id: bp-reconcile-target-state | created: 2026-08-20 | last_used: 2026-08-22 | uses: 4 | tier: active | supersedes: ot-mode-b-automation-backlog | origin: 2026-08-20-223624 -->

- [x] **(blueprint — SHIPPED v4.37.0 MINOR, 2026-08-21) Protocol behind a one-line root
  shim.** Root `AGENTS.md` (tool + template) became a 61-byte pointer to the canonical
  `memory/PROTOCOL.md` (dual-mode tool copy; target-only template), killing the ~20 KB
  auto-load tax; PRE-APPLY fail-closed gating protects customized roots (PR #24, eugenelim;
  3 review findings fixed pre-merge). Lesson: the consent artifact must agree with apply.
  Full detail: origin log + spec under `docs/specs/memory-protocol-pointer/` + the
  `4.36.0→4.37.0` rung. → serves: vision-agent-memory
  <!-- id: protocol-pointer-enterprise-activation | created: 2026-08-20 | last_used: 2026-08-22 | uses: 8 | tier: active | origin: 2026-08-20-204952 -->

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
  <!-- id: ot-protocol-text-propagation | created: 2026-08-21 | last_used: 2026-08-22 | uses: 2 | tier: working | origin: 2026-08-21-052644 -->

- [ ] **Field canary: AGENTS.md-native activation is unproven.** Codex, Kiro, and Antigravity
  auto-load root `AGENTS.md`, so v4.37.0 trades their inline protocol for a 61-byte imperative
  plus one read-action — the v4.29.0 failure class (pointer prose, skipped under task pressure)
  reintroduced for exactly the enterprise-IDE class this targets. Mitigated by the single
  unambiguous imperative and the activation-first rewrite, motivated by a real ~20 KB/session
  tax, but never observed on a live Kiro or Codex session: treat activation there as unvalidated
  until a field canary confirms it (the v4.29.0 attestation pattern). → serves:
  vision-agent-memory (cross-vendor activation is a claim to observe, not assume)
  <!-- id: ot-agents-native-activation-canary | created: 2026-08-21 | last_used: 2026-08-21 | uses: 1 | tier: working | origin: 2026-08-21-052644 -->

- [x] **Shipped v4.34.2 (PATCH) — the guard's own opt-down knob is not a credential.**
  mercury-composable field FP: documenting the guard's advisory knob tripped the guard;
  fixed with their endorsed exact-key, value-constrained exemption (trailing-punctuation
  variant caught pre-ship by the verbatim-fixture rule). Lesson: a guard must never block
  the documentation of its own controls. Full detail: origin log + the `4.34.1→4.34.2`
  rung. → serves: vision-agent-memory
  <!-- id: secret-fp-self-knob-v4342 | created: 2026-08-19 | last_used: 2026-08-19 | uses: 1 | tier: archive-candidate | origin: 2026-08-19-203132 -->

- [x] **Shipped v4.34.0 (MINOR) — pre-commit secret guard on both surfaces (memory + config).**
  Staged-content scan blocks committed secrets by default (the deliberate, scoped exception
  to the advisory doctrine — secrets carry irreversible cost); knob opts down, `--no-verify`
  bypasses once; probe-tuned to 0 FPs on a 661-file live corpus. Fold-up v4.34.1: guidance
  prints once per run. Full detail: origin log + the `4.33.4→4.34.0` rung.
  → serves: vision-agent-memory
  <!-- id: pre-commit-secret-guard-v4340 | created: 2026-08-14 | last_used: 2026-08-19 | uses: 3 | tier: archive-candidate | origin: 2026-08-14-021712 -->

- [ ] **Re-verify invariants (due):** confirm `target-repo-scope-only`,
  `never-delete-vendor-files`, `never-pick-a-winner`, `no-build-step-agent-run`,
  `upgrades-additive`, and the `vision-agent-memory` Vision still hold, or supersede any
  that do not (`DECAY.md` §9).
  <!-- id: ot-reverify-invariants-20260814 | created: 2026-08-14 | last_used: 2026-08-14 | uses: 1 | tier: working | origin: 2026-08-14-011037 -->

- [x] **Hardened `memory-lint` test fixtures against repo secret-scanner FPs (no release
  bump).** Suites construct shape-constrained dummy secrets at runtime instead of
  committing signatures; full coverage retained (46/46 ×2). Lesson: security tooling must
  not make its own repository noisy to enterprise scanners. Full detail: origin log.
  → serves: vision-agent-memory
  <!-- id: secret-test-fixtures-env | created: 2026-08-14 | last_used: 2026-08-21 | uses: 2 | tier: active | origin: 2026-08-14-011037 -->

- [x] **Shipped v4.33.4 (PATCH) — reject non-empty `${…}` defaults in `[secret-material]`.**
  v4.33.3's placeholder exemption also trusted literal fallbacks; template forms stay safe
  while values with real-looking defaults flag without echo (46 mirror tests ×2). Full
  detail: origin log. → serves: vision-agent-memory
  <!-- id: secret-template-default-v4334 | created: 2026-08-14 | last_used: 2026-08-14 | uses: 3 | tier: archive-candidate | origin: 2026-08-14-003952 -->

- [x] **Shipped v4.33.3 (PATCH) — security-review hardening for `[secret-material]`.** A
  fresh-context review's four gaps fixed (real strict gate in CI wrappers; key-scoped enum
  exemption; quoted/header/embedded forms flag; Mode C redaction triage); a pre-tag
  live-target probe caught 2 template-pattern FPs the review missed. Lesson: always probe
  the live target, not just suites. Full detail: origin log. → serves: vision-agent-memory
  <!-- id: secret-review-hardening-v4333 | created: 2026-08-13 | last_used: 2026-08-14 | uses: 5 | tier: archive-candidate | origin: 2026-08-13-235301 -->

- [x] **Shipped v4.33.2 (PATCH) — `[secret-material]`: backtick is a value delimiter.** The
  v4.33.1 fix missed the field line's real markdown-inline-code form; backtick joined the
  delimiter set and the mirror test now quotes the field line verbatim. Lesson (origin of
  the verbatim-fixture doctrine): a field fix's fixture must quote the motivating artifact
  verbatim, never a paraphrase. Full detail: origin log + the `4.33.1→4.33.2` rung.
  → serves: vision-agent-memory
  <!-- id: secret-fp-backtick-v4332 | created: 2026-08-13 | last_used: 2026-08-19 | uses: 4 | tier: archive-candidate | origin: 2026-08-13-231459 -->

- [x] **Shipped v4.33.1 (PATCH) — ALL-CAPS enum constants are not credentials.** Check 10's
  first field contact was one FP (a documented enum value); the detector now treats
  ALL-CAPS identifiers as config constants while token shapes stay covered. Lesson
  (honest-signal doctrine): fix the detector, never sprinkle waivers through client repos.
  Full detail: origin log + the `4.33.0→4.33.1` rung. → serves: vision-agent-memory
  <!-- id: secret-fp-enum-constants-v4331 | created: 2026-08-13 | last_used: 2026-08-19 | uses: 4 | tier: archive-candidate | origin: 2026-08-13-225859 -->

- [x] **Shipped v4.33.0 (MINOR) — session-log secret redaction: ritual rule +
  `[secret-material]` advisory.** From a client-side DLP incident (live OAuth secret in a
  committed session log): the redaction rule joined the after-session ritual and lint
  check 10 became the deterministic backstop (never echoes values; scans sessions +
  archive). Lesson: shared memory must be safe to share — a committed secret is exposed,
  rotate it. Full detail: origin log + the `4.32.1→4.33.0` rung.
  → serves: vision-agent-memory
  <!-- id: secret-redaction-lint-v4330 | created: 2026-08-13 | last_used: 2026-08-19 | uses: 9 | tier: archive-candidate | origin: 2026-08-13-222439 -->

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
### Backlog — vNext (temporal & supersession) + beyond
> From the 2026-06-13 industry-alignment assessment:
> `docs/assessments/2026-06-13-industry-alignment.md`. Verdict: on track; distinctive
> on event-sourcing/determinism/governance; one real gap = temporal/supersession.
> Re-run the assessment after meaningful iterations and compare its scorecard.

- [ ] **Dogfooding on real work (ongoing).** Already delivering: the simple-proxy
  enable surfaced v3.1.0 (`.gitignore`), and the simple-proxy Node→Rust refactor's
  field report drove v3.2.0 (protocol clarifications). Keep feeding real-work insights
  back into this backlog. (Stated 2026-06-13.)
  <!-- id: backlog-real-work-dogfood | created: 2026-06-13 | last_used: 2026-08-22 | uses: 19 | tier: active -->

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
- [x] **Publish to GitHub — DONE 2026-06-18.** Migrated GitLab → public GitHub
  (`acn-ericlaw/agent-memory`, Apache-2.0, full history; the `-tool` suffix dropped; old
  GitLab retired; publication gate satisfied with maintainer approval). **`origin` is
  GitHub; assume GitHub for git ops.** Full detail: sessions of 2026-06-18.
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
