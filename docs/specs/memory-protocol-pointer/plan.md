# Plan: Memory protocol pointer

- **Spec:** [`spec.md`](spec.md)
- **Status:** Done

> **Plan contract:** this is the implementation strategy. It may change while
> Drafting or Executing; the spec remains the behavior contract.

## Approach

First separate the two current protocol variants from their bootstrap filenames:
the tool's existing dual-mode `AGENTS.md` becomes an optimized
`memory/PROTOCOL.md`, and the installed target protocol becomes
`templates/memory/PROTOCOL.md`; both root `AGENTS.md` files collapse to the same
one-line pointer. Then update eager vendor bootstraps and every install, upgrade,
schema, source-of-truth, and release surface that owns or describes the boundary.
Verification combines mechanical pointer/size/reference checks with a semantic
obligation audit and real entry-path walkthroughs.

## Constraints

- `upgrades-additive` (ADR-0005): preserve target-owned content and stop on an
  ambiguous merge.
- `no-build-step-agent-run` (ADR-0006): Markdown remains the product and the agent
  remains the runtime.
- The tool root protocol may route to operator-only files; the installed target
  protocol may not.
- Repository edits use `apply_patch`; Git remains read-only in this environment.

## Construction tests

**Integration tests:**

- Build an exhaustive directive inventory from every normative statement in
  `git show HEAD:AGENTS.md` and `git show HEAD:templates/AGENTS.md`; treat that inventory,
  not AC-MP-04's category summary, as the canonical checklist. Every directive must map to one
  live destination with equivalent normative force or an explicitly approved correction.
- Search current documentation and bootstraps for stale assertions that `AGENTS.md`
  carries the memory protocol; classify historical changelog/upgrade text separately.
- Audit the instruction-versus-evidence trust boundary and confirm collision content remains
  inert until target-local provenance and active-session authority are established.
- Run the built-in `memory-lint` implementation available in this checkout and confirm
  no new errors.

**Manual verification:**

- Tool path: begin with only root `AGENTS.md`; follow the pointer and confirm that an
  enable request reaches `ENABLE.md`, while work inside this repository performs the
  required memory activation.
- Target path: assemble the installed pointer/protocol/bootstrap set in an approved
  temporary directory; confirm a fresh agent reaches the ordered session activation
  without any operator-only reference.
- Fresh-enable collision path: repeat enablement with an unambiguously mergeable
  target-owned `memory/PROTOCOL.md` and with an ambiguous collision; assert preservation
  without duplication in the first case and a pre-write human stop in the second.
- Upgrade path: walk and repeat the rung for a stock target and a target with a local
  `AGENTS.md` addition; also exercise a pre-existing `memory/PROTOCOL.md` and an ambiguous
  merge, asserting zero content loss, zero duplication, and a human stop where required.
- Recovery path: verify byte restoration from a committed baseline, then verify that an
  uncommitted/non-Git case stops until the human names a target-local backup.

## Design (LLD)

### Design decisions

- `AGENTS.md` is a universal discovery shim, not a second protocol copy. This gives
  enterprise IDEs a stable, minimal auto-loaded surface while preserving a vendor-neutral
  path to the full contract. Traces to AC-MP-01, AC-MP-02, AC-MP-03.
- The tool and target protocols remain separate source artifacts because their routing
  authority differs. Shared wording is manually kept aligned where the contracts overlap;
  generating either file would violate the no-build-step invariant. Traces to AC-MP-02,
  AC-MP-04.
- Activation precedes rationale. The protocol presents mode selection, required reads, and
  matching-skill dispatch before explanatory or end-of-session material. Traces to
  AC-MP-03, AC-MP-04, AC-MP-05, AC-MP-06.

### Component / module decomposition

- `AGENTS.md` and `templates/AGENTS.md`: identical one-line discovery shims.
- `memory/PROTOCOL.md`: tool operator dispatch plus this repository's memory protocol.
- `templates/memory/PROTOCOL.md`: installed target memory protocol with placeholders only
  where target generation requires them.
- Vendor bootstraps: eager-import or prose activation adapters.
- `ENABLE.md` and `UPGRADE.md`: lifecycle ownership for fresh installs and safe relocation.
- README/schema/smoke/release docs: discoverability and published contract mirrors.

### State & control flow

1. Runtime auto-loads or is directed to root `AGENTS.md`.
2. The single line activates `memory/PROTOCOL.md`.
3. Tool checkout: the protocol selects enablement vs. internal-memory work.
4. Enabled target: the protocol immediately performs session orientation and skill routing.
5. At session close, the same protocol applies the tracked-diff logging and review rules.

### Failure, edge cases & resilience

- Missing `memory/PROTOCOL.md`: enable/upgrade verification fails; the pointer is never
  considered complete alone.
- Customized installed `AGENTS.md`: upgrade extracts and preserves local additions, or
  stops before replacement when provenance is ambiguous.
- Runtime ignores Markdown links: import-capable bootstraps directly import the protocol;
  prose-only bootstraps name it directly as well as relying on the universal shim.
- Historical references: changelog and old upgrade rungs remain historical unless they
  claim a current source-of-truth rule.

## Tasks

### T1: One-line shims activate complete, optimized protocols

**Depends on:** none

**Touches:** `AGENTS.md`, `memory/PROTOCOL.md`, `templates/AGENTS.md`, `templates/memory/PROTOCOL.md`, `CLAUDE.md`, `GEMINI.md`, `.cursorrules`, `.windsurfrules`, `.github/copilot-instructions.md`, `templates/CLAUDE.md`, `templates/GEMINI.md`, `templates/.cursorrules`, `templates/.windsurfrules`, `templates/.github/copilot-instructions.md`

**Tests:**

- Goal-based: each `AGENTS.md` has exactly one physical line plus one terminal newline,
  the two files are byte-identical, and their link resolves to an existing protocol
  (AC-MP-01, AC-MP-02).
- Goal-based: each protocol is at most 14,500 bytes and target protocol searches find no
  operator-only filenames (AC-MP-02, AC-MP-05).
- Manual QA: audit the old normative obligations and walk both activation paths
  (AC-MP-03, AC-MP-04, AC-MP-05, AC-MP-06, AC-MP-12).

**Approach:**

- Inventory each operative rule in the two existing protocol files before replacing them.
- Re-author each protocol in activation order, merging duplicate prose without weakening
  normative force.
- Collapse both root files to the exact pointer and update vendor bootstrap activation/imports.

**Done when:** AC-MP-01 through AC-MP-06, AC-MP-12, the exhaustive directive inventory,
and the tool/target manual entry walkthroughs pass.

### T2: Enablement, upgrades, and published documentation own the new boundary

**Depends on:** T1

**Touches:** `ENABLE.md`, `UPGRADE.md`, `README.md`, `CHANGELOG.md`, `VERSION`, `templates/.agent/version.md`, `templates/.agent/schema.md`, `memory/instructions.md`, `memory/smoke-test.md`, `templates/memory/smoke-test.md`, applicable `examples/**/ENABLE_OUTPUT.md`, `docs/DESIGN-ritual-triggers.md`, `docs/optional-ritual-hook.md`, and any additional current-contract surface identified by the reference audit

**Tests:**

- Goal-based/manual: fresh-enable file lists, verification, and reports include both the
  shim and protocol; repeated unambiguous and ambiguous destination collisions preserve
  content or stop before writing (AC-MP-07).
- Goal-based/manual: repeated `4.36.0 → 4.37.0` walks handle stock, customized,
  pre-existing-destination, and ambiguous cases without content loss or duplication
  (AC-MP-08, AC-MP-09).
- Goal-based: current-source searches and version checks pass; historical records remain
  intact (AC-MP-10, AC-MP-11).

**Approach:**

- Teach enablement to create `memory/PROTOCOL.md`, expand direct bootstrap imports, and verify
  the pointer/protocol pair.
- Add an explicit, customization-safe relocation rung and update the source-of-truth map.
- Update current architecture maps, schema/smoke guidance, release notes, and version stamps.

**Done when:** AC-MP-07 through AC-MP-11 pass and the full repository reference audit has
no unexplained stale current-contract claim.

### T3: Repository gates and session close are clean

**Depends on:** T1, T2

**Tests:**

- Goal-based: memory lint and all repository-specific validation commands pass.
- Manual QA: the semantic obligation checklist and every named manual-verification path
  above are recorded with observed outcomes.
- Goal-based: the final tracked diff has a compliant session log and continuity update.

**Approach:**

- Run the full gate set, repair in-scope failures, and complete the bounded adversarial,
  quality, and experience review passes required by full work-loop mode.
- Write the full memory session record and update the active project state.

**Done when:** all acceptance criteria are checked, review findings are resolved, no
unintended change was introduced, and every pre-existing worktree change remains untouched.

## Rollout

Release as v4.37.0. Fresh enables receive the new pair immediately. Existing enabled
repositories adopt it through the ordered upgrade rung; the old root protocol remains
operative until any customized content has been safely migrated and the human approves
the one-line replacement. A committed pre-upgrade blob is the normal byte-recovery
artifact. Without one, the upgrade stops before replacement until the human approves a
target-local byte-preserving backup; rollback support is never inferred from an
uncommitted diff alone. No data migration or runtime deployment exists.

## Risks

- Compression can silently weaken a normative instruction; the explicit obligation inventory
  and adversarial review are the primary controls.
- A one-line shim can reduce activation on runtimes that do not follow links; direct vendor
  bootstrap imports/pointers mitigate this where a supported mechanism exists.
- An upgrade can erase local root instructions if stock-vs-custom detection is careless;
  preservation and a human stop are mandatory.
- Current and historical references to `AGENTS.md` are interleaved across a long upgrade
  ladder; a blind global replacement would corrupt history.

## Changelog

- 2026-08-20: initial plan after maintainer confirmation of scope and optimization goals.
- 2026-08-20: post-implementation security-review amendment approved by the maintainer —
  add AC-MP-13's authority/evidence/provenance contract, a durable security reference,
  collision preflight, and last-moment source-hash revalidation.
- 2026-08-21: rebase amendment authorized by the maintainer — renumber the pending MINOR
  from v4.35.0 to v4.37.0 after main shipped v4.35.0 and v4.36.0, and integrate the
  protocol boundary as a pre-apply reconcile semantic step.
- 2026-08-21: post-rebase review amendment — enforce both the v4.36 hook-preservation
  inspection and v4.37 protocol boundary in the reconcile CLI, require an explicit
  completion handshake, and pin zero-write refusal/confirmed apply in both runtimes.
- 2026-08-21: the maintainer ran the current-baseline target-Git walkthrough; committed
  recovery, zero-write refusal, protocol-before-shim ordering, customized-hook survival,
  confirmed apply, and repeated zero-change apply all passed (`walkthrough.md`).
