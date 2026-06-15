# Agent Instructions — agent-memory

> Project context + architecture for **any** agent (Claude, Gemini, Cursor, …) working on
> this repo. Vendor-neutral by design — the bootstrap files (`CLAUDE.md`, `GEMINI.md`, …)
> are thin pointers; this is where the substance lives.

## What This Project Is

`agent-memory` is a **no-code, markdown-only** system with three jobs in one repo:

1. **A shared memory system** — a `memory/` layer that persists project context across
   sessions and across different AI vendors. It *evolves*: facts carry usage metadata,
   fade through tiers, and archive when stale, recomputed deterministically from the
   session-log event stream (`DECAY.md`). On top of that backward-looking substrate sits
   the **forward cognitive loop (VBDI, v4.0.0)**: Current State → Vision → Blueprint →
   Design → Implementation → Feedback (`DECAY.md` §12).
2. **An AI-enablement tool** — point it at any other repo to generate a tailored memory
   system there.
3. **A migration tool** — when the target repo already has vendor AI files (Cursor,
   Aider, Continue, Cline, …), fold them into the unified format.

**Type:** Developer tooling / meta-framework. **Primary language:** Markdown — there is
**no build, lint, or test step**; the markdown files *are* the product, and the "runtime"
is an AI agent reading them. Validation is manual: confirm the protocol files read
unambiguously and that `examples/` still reflect documented behavior.

> **Control flow.** Every agent enters via its bootstrap pointer (`CLAUDE.md`, `GEMINI.md`,
> `.cursorrules`, …) → **`AGENTS.md`** (the hub), which branches: working *within* this
> repo → the memory protocol (read this file + `continuity.md` + `vision.md` + recent
> `sessions/`); *AI-enabling another repo* → `ENABLE.md` (then `MIGRATE.md`/`UPGRADE.md`
> as it directs). Don't improvise from memory — read the protocol file.

## Repository Structure — how the files relate

The system is layered, and the layering is the design (README "Two Layers"):

- **Root bootstrap files** (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`, `.cursorrules`,
  `.windsurfrules`, `.github/copilot-instructions.md`) — one per vendor, **each a thin
  pointer** so any agent lands in the same `AGENTS.md` protocol. `AGENTS.md` is the hub.
- **`ENABLE.md`** — enablement protocol (detect footprint → Mode A/B/C → analyze →
  generate). **`MIGRATE.md`** — per-vendor detection + conversion, only via Mode C.
  **`UPGRADE.md`** — in-place version-upgrade ladder, only via Mode B. `MIGRATE.md` and
  `UPGRADE.md` are tool-operator-only (never installed into targets).
- **Evolving-memory layer (backward)** — `DECAY.md` (metadata, tiers, deterministic decay
  — no floating-point scoring) and `REVIEW.md` (the review ritual). Generic and *installed
  into every enabled repo's root*. `VERSION` = the tool's semver; each enabled repo stamps
  `.agent/version.md`.
- **Forward layer (VBDI, v4.0.0)** — `memory/vision.md` (north star) + Blueprint as typed
  `(blueprint)` Open Threads + the altitude trace (`serves:` / `id`). Rules in `DECAY.md`
  §12 (+ the §10 drift check); design rationale in `docs/DESIGN-vbdi-lifecycle.md`
  (tool-only). Enable/upgrade **bootstrap a DRAFT Vision and gate it** — never fabricated.
- **`templates/`** — exactly what installs into a target repo: bootstrap files + `memory/`
  files with `{{UPPER_SNAKE_CASE}}` placeholders (incl. `decay-policy.md`, `vision.md`),
  `.agent/schema.md` (canonical memory-file format, copied verbatim), `.agent/version.md`.
- **`memory/`** — this repo's *own* memory layer (it eats its own dog food): this file,
  `continuity.md` (live state + Architectural Invariants + Blueprint), `vision.md`,
  `decay-policy.md`, `sessions/` (immutable event log), `archive/`, `smoke-test.md`.
- **`examples/`** — real filled-in output, not placeholders: `rust-event-bus/` (Mode A),
  `migrated-cursor-aider-project/` (Mode C), `evolving-memory-example/` (the review cycle).
- **`docs/`** — design rationale + assessments (`DESIGN-evolving-memory.md`,
  `DESIGN-vbdi-lifecycle.md`, `agent-cognitive-framework.md`, `assessments/`).

**Changes span layers in lockstep:** a new vendor → a row in `MIGRATE.md`'s table + a
per-vendor section + the supported-vendor tables in `README.md` and `AGENTS.md`. A
memory-file shape change → `templates/`, `templates/.agent/schema.md`, and `examples/`
together. An evolving-memory change → `DECAY.md`, `REVIEW.md`,
`templates/memory/decay-policy.md`, the schema, and `examples/evolving-memory-example/`;
if the shape changes, bump `VERSION` and add an `UPGRADE.md` rung.

## Non-Negotiable Constraints

The core safety philosophy (also pinned as Architectural Invariants in `continuity.md`):

- **Target-repo scope only.** Never read/modify/move/list anything outside the resolved
  target-repo root — never `~`, `~/.claude/`, Application Support, AppData, or system
  paths. Resolve symlinks first; report any path that escapes. The user's home dir is
  *their* personal AI environment; the repo's `memory/` is the *team's* shared layer.
- **Never delete vendor files** — move originals to `legacy/<vendor>/`, preserving paths.
- **Never overwrite, never pick a winner** — fold vendor steering under `## Migrated rules
  from <vendor>`; surface contradictions as Open Threads.
- **Never modify source code or package manifests** in a target repo.
- **Idempotent + additive** — Mode B detects "already ours" (older → upgrade in place via
  `UPGRADE.md`); dry-run supported; upgrades only enrich and add, never rewrite or delete.

## Conventions

- Placeholders use `{{UPPER_SNAKE_CASE}}`; templates mirror final output exactly; examples
  show real content, never placeholders.
- "Ours vs. vendor" for shared filenames (`CLAUDE.md`, `AGENTS.md`, …) is decided by
  content: ours references the agent-memory system / `memory/instructions.md`.
- Remind the user to commit memory changes:
  `git add memory/ && git commit -m "session YYYY-MM-DD [agent]"`.

## Core Rules

1. If asked to AI-enable a repo, read `ENABLE.md` before anything; never copy templates
   blindly — analyse the target first.
2. Never modify source code in target repos — only create memory and bootstrap files.
3. Templates in `templates/` are the structure guide; keep the layers in lockstep.
4. Record every session in this repo's own session log; update `continuity.md` after.
5. If you see a TODO, contradiction, or drift, surface it as an Open Thread — never
   silently reconcile or pick a winner.

## Testing & CI / CD

None — no build/lint/test step. Validation is manual: the protocol files must read
unambiguously, and `examples/` must reflect documented behavior.
