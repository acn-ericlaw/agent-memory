# Skills & Built-ins

Memory and steering were already shared across vendors. **Skills** are the third shared leg:
reusable *capabilities* — a `name`, a *when-to-use* `description`, a procedure, optionally
helper scripts — authored once and usable by any agent.

## How the layer works

- **Neutral source of truth.** A committed `agent-skills/<name>/SKILL.md` — vendor-neutral
  markdown — is the single definition; it travels with the repo, like `memory/`.
- **Universal runtime.** The `AGENTS.md` "Skills" section is the baseline: when a task
  matches a skill's `description`, the agent reads and follows that `SKILL.md`. Because the
  agent *is* the runtime, this works on **any** vendor with no engine.
- **Thin per-vendor adapters.** For runtimes with a native skill/command system, the tool
  regenerates *pointers* across **six** vendor targets for native auto-trigger. Adapters are
  gitignored and regenerated (never copies), so the neutral skill never drifts.
- **Migration promotes, never flattens.** A vendor's existing skills (e.g. `.claude/skills/`)
  are *promoted* into `agent-skills/` (originals preserved under `legacy/`), not folded into
  steering — skills are procedures, not rules.

The six adapter targets: `.claude/skills/`, `.gemini/commands/`, `.cursor/rules/`, `.kiro/`,
`.github/skills/` (GitHub Copilot), and `.agents/skills/` (Google Antigravity). Regeneration
is itself a runnable script ([`sync-adapters`](../reference/built-in-skills.md#sync-adapters)),
so it never depends on an agent improvising the recipe.

## The judgment-vs-arithmetic boundary

Real cross-vendor use surfaced a recurring failure class: *a capable agent silently does only
part of a multi-step ritual.* The fix pattern, applied every time, became a core principle:

> **Mechanize the arithmetic, not the judgment.**

The deterministic, mechanical parts of a memory ritual become **runnable helpers** so an
agent can't silently skip them; every act of judgment stays with the agent and the human.

## The seven built-ins

Installed into every enabled repo and tool-managed (marked `provenance: agent-memory-builtin`).
They sort cleanly along that boundary:

| Built-in | Role | Side |
|---|---|---|
| [`memory-lint`](../reference/built-in-skills.md#memory-lint) | Deterministic integrity verifier (nine checks; Python *and* Node) | arithmetic — read-only |
| [`refresh-metadata`](../reference/built-in-skills.md#refresh-metadata) | Recompute every fact's tier/usage from the ledger | arithmetic |
| [`archive-fact`](../reference/built-in-skills.md#archive-fact) | Perform the archive *move* safely (truncation-proof) | arithmetic |
| [`sync-adapters`](../reference/built-in-skills.md#sync-adapters) | Regenerate the six vendor adapters | arithmetic |
| [`harvest-knowledge`](../reference/built-in-skills.md#harvest-knowledge) | Distil durable facts from the team's docs | judgment-assisted |
| [`second-opinion`](../reference/built-in-skills.md#second-opinion) | Snapshot for a clean-memory reviewer | judgment-assisted |
| [`apply-critique`](../reference/built-in-skills.md#apply-critique) | Bounded, human-gated apply loop | judgment-assisted |

!!! info "Zero overhead by default"
    The built-ins are tool-managed (fork under a new name to customize, or upstream a genuine
    fix). Like everything else, they are **installed ≠ run**.

To write your own, see [Author a Skill](../guides/author-a-skill.md). For the full design,
see the [Skills Layer design note](../DESIGN-skills-layer.md).
