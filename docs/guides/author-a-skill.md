# Author a Skill

A skill is a reusable capability — a `name`, a *when-to-use* `description`, a procedure,
optionally helper scripts — authored once in the neutral `agent-skills/` layer and runnable by
any agent. See [Skills & Built-ins](../concepts/skills.md) for the concept.

## The three-step action

Authoring is an explicit **3-step action** — agents (including Copilot/Gemini) don't reliably
auto-sync after writing the file, so do all three:

1. **Write** the neutral source: `agent-skills/<name>/SKILL.md`.
2. **Run** `sync skill adapters` (the [`sync-adapters`](../reference/built-in-skills.md#sync-adapters)
   script) to regenerate the six vendor adapters.
3. **Reload** the runtime if it loads adapters at startup.

```bash
# step 2 — regenerate the six adapters (bash; Node/Python also available)
bash agent-skills/sync-adapters/scripts/sync-adapters.sh
```

## The SKILL.md shape

```markdown
---
name: my-skill
description: When to use this — the auto-trigger match string.
---

# my-skill

A short procedure the agent follows when the description matches.
Optionally reference helper scripts under `scripts/`.
```

## What `sync skill adapters` does

For each `agent-skills/<name>/SKILL.md` it (re)writes the six vendor adapters
(`.claude/skills/`, `.gemini/commands/`, `.cursor/rules/`, `.kiro/`, `.github/skills/`,
`.agents/skills/`) and **prunes orphaned generated adapters** — signature-guarded, so it never
deletes a hand-authored vendor file. Adapters are gitignored pointers, never copies, so the
neutral skill never drifts.

!!! warning "Hot-reload caveat (vendor-specific)"
    Some runtimes read skill adapters only at startup. **GitHub Copilot CLI** parses
    `.github/skills/` at init, so a freshly-synced `/<name>` isn't live mid-session until you
    `/restart` (or run its skills rescan). **Claude, Cursor, and Kiro** pick up a new
    description-matched skill without a restart.

## Editing a built-in

Before editing a skill, check its frontmatter. If it is `provenance: agent-memory-builtin`,
**don't edit in place** — it's tool-managed and overwritten on upgrade. Instead:

- **Fork** it under a new name for a local variant, or
- **Upstream** a genuine fix to the agent-memory project for back-port + validation.

## Deleting a skill

Remove the neutral source (`rm -rf agent-skills/<name>/`), run `sync skill adapters` (it
auto-prunes the orphaned adapters), and mark the related continuity id `superseded`.

For the full reference, see [`SKILLS.md`](../reference/protocol-files.md) and the
[Skills Layer design note](../DESIGN-skills-layer.md).
