# Architecture Decision Records (ADR)

> **For humans.** This is the project's governance-facing log of significant, durable
> **architecture decisions** — one decision per entry, with its rationale and the
> trade-offs it accepts. It is read **on demand**, not part of the per-session agent
> read path, so it adds **zero default token cost** (the same footing as
> `docs/DESIGN-*.md`).

## What an ADR is (and is not)

An ADR records *why* a load-bearing architectural choice was made — the kind of
decision that is expensive to reverse and that a newcomer or auditor needs the
reasoning behind. It is the **Design** altitude of the VBDI loop made durable
(`docs/DESIGN-vbdi-lifecycle.md` §4): Current State → Vision → Blueprint → **Design**
→ Implementation → Feedback.

**Map, don't duplicate.** The live constraint text stays in `memory/continuity.md`
(`## Architectural Invariants` / `## Key Decisions`) — that is the *what* that holds
*now*, carries an `id`, and is read every session. An ADR is the durable *why*:
context, alternatives, and consequences. The two cross-link by `id`
(`formalizes:` here ↔ `adr:` on the continuity footer); the constraint is never
restated as competing truth.

## Lifecycle (mirrors `DECAY.md` §9)

- **Status:** `Proposed` → `Accepted` → `Superseded` / `Deprecated`.
- **Never deleted.** A decision that no longer holds is **superseded** (replaced by a
  newer ADR) or **deprecated** (no longer relevant, not replaced) — the old entry
  stays in place, its `Status` updated. History is the point.
- To supersede: add a new ADR, set the old one to `Status: Superseded by ADR-NNNN`,
  and the new one to `Supersedes: ADR-NNNN`.

## Format

```
## ADR-NNNN — <Title>
**Status:** Accepted · **Date:** YYYY-MM-DDThh:mm:ss.mmmZ · **Serves:** <vision-id>
<!-- id: adr-NNNN | status: accepted | formalizes: <continuity-id> -->

**Abstract.** One paragraph: what was decided and its scope.

**Rationale.** Why this, why now, the alternatives weighed, **and the consequences /
trade-offs** the decision accepts.
```

- **Numbering** is monotonic (`ADR-NNNN`); entries are listed **newest first**.
- **Date** is the persist-time UTC ISO 8601 stamp (the session-log convention) at the
  moment the decision is recorded.

> **Seed note.** ADR-0001…0006 below were seeded **2026-06-20** from the five standing
> `## Architectural Invariants` in `memory/continuity.md`, **plus the superseded
> `no-code-markdown-only` decision** (ADR-0004, now archived) that ADR-0006 replaced; each
> `Date` is the original *decision* date (day granularity — the precise instant predates
> this log).

---

## ADR-0006 — No build step; the agent is the runtime
**Status:** Accepted · **Date:** 2026-06-16 · **Serves:** vision-agent-memory · **Supersedes:** ADR-0004
<!-- id: adr-0006 | status: accepted | formalizes: no-build-step-agent-run | supersedes: ADR-0004 -->

**Abstract.** The tool itself runs no code and needs none — no install, no daemon, no
build/lint/test step. The markdown files *are* the product and an AI agent is the
runtime. A skill MAY bundle optional helper scripts (e.g. `memory-lint`), but those are
invoked by the agent/vendor at the user's direction — **never executed by the tool**.

**Rationale.** Maximizes portability and vendor-neutrality: any agent, on any machine,
can read and act on the files with zero setup, and a human can audit the whole system by
reading it. This supersedes **ADR-0004** (the earlier *"no-code, markdown-only"* framing),
which was too absolute once optional helper scripts appeared — the principle is *the tool
runs nothing*, not *no script may exist*. **Trade-off:** the determinism a compiler or test
gate would provide must instead come from convention + the optional verifier skills
(`memory-lint`) + human review; correctness leans on the agent reading carefully rather
than on a build gate.

## ADR-0005 — Upgrades are additive and non-destructive
**Status:** Accepted · **Date:** 2026-06-13 · **Serves:** vision-agent-memory
<!-- id: adr-0005 | status: accepted | formalizes: upgrades-additive -->

**Abstract.** In-place upgrades (Mode B) only **enrich and add** — never rewrite or delete
a user's content — **except** the tool's own managed built-ins (`memory-lint`,
`second-opinion`, `apply-critique`), which are re-copied (overwritten) on upgrade. That
overwrite is scoped to tool-owned files; a user customizes a built-in only by **forking**
it under a new skill name.

**Rationale.** A repo enabled by an older version must be able to move forward safely
without losing local customization or history, and idempotent re-runs must be harmless.
The built-ins exception keeps the shared verifier/review machinery correct across every
enabled repo. **Trade-off:** the tool must carry a version ladder (`UPGRADE.md`) and
warn-before-overwrite logic for locally-modified built-ins; "additive-only" also means
superseded guidance *accumulates* rather than being deleted — which is exactly what this
ADR lifecycle and the memory decay model then manage.

## ADR-0004 — No-code, markdown-only (the files are the product)
**Status:** Superseded by ADR-0006 · **Date:** 2026-06-13 · **Serves:** vision-agent-memory
<!-- id: adr-0004 | status: superseded | formalizes: no-code-markdown-only | superseded-by: ADR-0006 -->

**Abstract.** The system is **no-code and markdown-only**: the markdown files *are* the
product and an AI agent is the runtime — no build, lint, or test step, nothing executes.

**Rationale.** Portability and vendor-neutrality with zero setup, and a system a human can
audit by reading it; a CLI / daemon / index-server alternative was rejected as install +
maintenance burden and vendor coupling. **Superseded by ADR-0006 (2026-06-16):** the v4.1.x
skills layer introduced optional bundled helper `scripts/` (e.g. `memory-lint`), so the
absolute *"markdown-only"* no longer strictly held. ADR-0006 preserves the intent in refined
form — *the tool itself runs no code*; a skill may carry optional scripts the agent/vendor
runs at the user's direction. **Consequence:** the line moved from "no script may exist" to
"the tool executes nothing," keeping the no-install / auditable guarantees while allowing
optional, agent-invoked helpers.

## ADR-0003 — Never overwrite, never pick a winner
**Status:** Accepted · **Date:** 2026-06-13 · **Serves:** vision-agent-memory
<!-- id: adr-0003 | status: accepted | formalizes: never-pick-a-winner -->

**Abstract.** When migrating a repo that already has vendor steering, never overwrite and
never pick a winner between conflicting rules — fold each vendor's steering under a
`## Migrated rules from <vendor>` section and surface any contradiction as an Open Thread
for a human to resolve.

**Rationale.** The tool cannot safely adjudicate a team's intent; silently choosing would
destroy information and erode trust. Preserving both rules and flagging the conflict keeps
the human in control of the resolution. **Trade-off:** the merged instructions may
temporarily hold contradictory guidance until a human closes the Open Thread — the system
favors faithful preservation over immediate tidiness.

## ADR-0002 — Never delete vendor files; preserve under `legacy/`
**Status:** Accepted · **Date:** 2026-06-13 · **Serves:** vision-agent-memory
<!-- id: adr-0002 | status: accepted | formalizes: never-delete-vendor-files -->

**Abstract.** Migration never deletes a vendor's original files — it **moves** them to
`legacy/<vendor>/`, preserving their relative paths.

**Rationale.** Migration must be reversible and auditable: a user can always see, diff, and
recover exactly what they had before enablement. **Trade-off:** the repo carries a
`legacy/` tree that is otherwise dead weight — accepted as the price of a non-destructive,
trustable migration.

## ADR-0001 — Target-repo scope only
**Status:** Accepted · **Date:** 2026-06-13 · **Serves:** vision-agent-memory
<!-- id: adr-0001 | status: accepted | formalizes: target-repo-scope-only -->

**Abstract.** Every read, modify, move, and list is scoped to the resolved target-repo
root. The tool never touches anything outside it — never `~`, `~/.claude/`, Application
Support, AppData, or system paths; symlinks are resolved first and any escaping path is
reported, not followed.

**Rationale.** The user's home directory is *their* personal AI environment; the repo's
`memory/` is the *team's* shared layer. Hard isolation is the core safety guarantee that
makes the tool safe to point at any repository. **Trade-off:** the tool deliberately gives
up conveniences that would reach into personal/home config (e.g. syncing a user's global
vendor settings) — the safety boundary is worth more than the feature.
