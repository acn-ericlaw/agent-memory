# Concepts

agent-memory pairs a **deterministic memory substrate** with a **lightweight cognitive
loop**. Together they turn memory-aware agent work into *predictable innovation with human
partnership* — bold ideas, faithful delivery, a human in the loop at every altitude.

<div class="grid cards" markdown>

-   :material-history:{ .lg .middle } __[Evolving Memory](evolving-memory.md)__

    ---

    The backward layer: an event-sourced ledger projected into live state, with
    deterministic decay, supersession, and provenance. Faithful to what *happened*.

-   :material-compass-outline:{ .lg .middle } __[The VBDI Loop](vbdi-loop.md)__

    ---

    The forward layer: *Current State → Vision → Blueprint → Design → Implementation →
    Feedback*, with an enforceable intent trace. Faithful to what was *intended*.

-   :material-puzzle:{ .lg .middle } __[Skills & Built-ins](skills.md)__

    ---

    Reusable capabilities authored once in a neutral `agent-skills/` layer and run by any
    agent — plus seven tool-managed built-ins.

-   :material-chart-timeline-variant:{ .lg .middle } __[Decay & Tiers](decay.md)__

    ---

    How facts strengthen, fade, and archive — by counting session files, never by a
    floating-point score.

-   :material-shield-check:{ .lg .middle } __[Reliability](reliability.md)__

    ---

    How the ritual actually happens without depending on an agent self-triggering:
    triggers, CI, init, and the judgment-vs-arithmetic boundary.

</div>

## The mental model

There are **two distinct memory layers** in a developer's life, and agent-memory keeps them
separate by design:

| Layer | Where it lives | Who owns it | What it holds |
|---|---|---|---|
| **Personal** | `~/` (home) | You | Your vendor's chat history, model prefs, global settings |
| **Shared (team)** | the repo's `memory/` | The team, via git | Project rules, decisions, session logs |

The tool **only ever touches the team layer**. Your personal `~/.claude/`, `~/.cursor/`,
Application Support, AppData — none of it is read, modified, or moved. Whatever vendor you
prefer keeps working exactly as before.
