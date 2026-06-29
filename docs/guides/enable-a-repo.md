# Enable a Repo

"AI enable this repo" is the single entry point. Point your agent at a path and it picks the
right mode automatically.

## Ask the agent

> **"AI enable `/path/to/your-project`."**

The agent first shows an **exec summary + cancel gate** (informed consent), then detects any
existing AI footprint and chooses one of three modes.

## The three modes

=== "Fresh (Mode A)"

    No prior AI footprint. The agent analyses the repo (language, stack, type), harvests
    durable facts from your docs, and **generates** a tailored `memory/` layer, bootstrap
    pointers, skill adapters, and the git-hook + CI triggers — plus a DRAFT Vision and its
    confirmation gate.

    You may choose a **discovery depth**: a standard scan (default) or an `/init`-depth deep
    analysis (which writes findings into the *neutral* memory layer, never a vendor steering
    file).

=== "Migrate (Mode C)"

    The target already uses vendor AI files (Cursor, Aider, Continue, Cline, Roo, Windsurf,
    Copilot, …). The agent **folds steering into `memory/`**, converts chat history into dated
    session logs, and **promotes** any vendor skills into the neutral `agent-skills/` layer —
    with **originals preserved under `legacy/`, never deleted**. A dry-run is offered.

=== "Already-Ours (Mode B)"

    The repo is already enabled. The agent is idempotent — and if the repo is on an older
    version, it [upgrades in place](upgrade.md) via the version ladder.

## What lands in the repo

| Path | Purpose |
|---|---|
| `memory/` | continuity, vision, sessions, archive, decay-policy |
| `AGENTS.md` | the hub every vendor's agent reads first |
| `agent-skills/` | seven built-ins + any promoted skills |
| `.githooks/` + `.github/workflows/` | the ritual triggers (agent-activated) |
| `.agent/version.md` | install manifest (gates upgrades) |
| `legacy/` | preserved originals (migration only) |

## After enabling

```bash
cd /path/to/your-project
git add . && git commit -m "chore: AI-enable repo"
```

Then just work — see [Getting Started, step 3](../getting-started.md#3-work-in-your-ai-enabled-repo).

!!! tip "Scope guarantee"
    Enable only ever creates or modifies files **within the target repo root**. It never
    touches `~`, `~/.claude/`, Application Support, AppData, or system paths.
