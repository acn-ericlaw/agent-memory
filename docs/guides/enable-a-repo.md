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
    pointers, skill adapters, and the git-hook + CI triggers (forge-aware: GitHub Actions,
    GitLab CI, or Azure Pipelines) — plus a DRAFT Vision and its
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
    version, it [upgrades in place](upgrade.md) by **reconciling against the current
    target state** (v4.35.0) — one diff-and-apply pass plus the few version-gated
    semantic steps, not a walk of every release in between. A `PRE-APPLY` step runs
    before mechanics when it must preserve content that would otherwise be re-copied;
    reconcile refuses writes until the protected boundary is safe and explicitly confirmed.

## How it converges (v4.35.0)

The mechanical ~80% of an enable — verbatim protocol docs, the seven built-in skills,
hooks, forge CI, managed `.gitignore`/`.gitattributes` blocks — is declared in a
tool-side **install manifest** and applied by a runnable **reconcile helper** in one
pass (dry-run first; the report doubles as the consent summary). The agent's time goes
where judgment lives: analyzing your repo, harvesting your docs, seeding `memory/`, and
the DRAFT-Vision gate. On a fresh repo that turns a >10-minute stepwise install into
seconds of mechanics plus a few minutes of real analysis.

## What lands in the repo

| Path | Purpose |
|---|---|
| `memory/` | protocol, continuity, vision, sessions, archive, decay-policy |
| `AGENTS.md` | the one-line universal shim to `memory/PROTOCOL.md` |
| `agent-skills/` | seven built-ins + any promoted skills |
| `.githooks/` + the forge CI config (`.github/workflows/`, `.gitlab-ci.yml` + `.gitlab/`, or `.azuredevops/`) | the ritual triggers (agent-activated, forge-aware) |
| `.agent/version.md` | version stamp (gates upgrades) |
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
