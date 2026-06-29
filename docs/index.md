---
title: agent-memory
hide:
  - navigation
---

# agent-memory

**A lightweight, vendor-neutral AI memory + cognitive-loop system.**
No-code, markdown-only. One shared `memory/` layer that any AI agent — Claude, Gemini,
Cursor, Kiro, GitHub Copilot, Antigravity — can read, write, and evolve.

[Get started](getting-started.md){ .md-button .md-button--primary }
[Read the whitepaper](agent-memory-whitepaper.md){ .md-button }
[View the deck](agent-memory-deck.html){ .md-button }

---

## Why it exists

AI agents are moving from single-turn prompting to persistent, memory-driven runtimes.
Two problems dominate production use:

<div class="grid cards" markdown>

-   :material-broom:{ .lg .middle } __Memory drift & vendor silos__

    ---

    Context is re-explained every session, decisions are silently forgotten or
    contradicted, and each AI tool hoards its own steering files. A team using more
    than one vendor has no shared, durable project memory.

-   :material-target:{ .lg .middle } __The intent ↔ delivery gap__

    ---

    Agents are creative, but keeping what is *built* faithful to what was *intended*
    is largely unmanaged. "Confidently wrong" facts and reversed decisions accumulate.

</div>

agent-memory addresses both with a **no-code, markdown-only** system layered over a single,
git-committed `memory/` directory. The files **are** the product; the agent is the runtime.

## Two layers

<div class="grid cards" markdown>

-   :material-history:{ .lg .middle } __Backward — Evolving Memory__

    ---

    An event-sourced ledger (immutable session logs) projected into a live
    `continuity.md`, with **deterministic** decay, supersession, invariant
    re-verification, contradiction checks, and provenance.

    *"Where are we, and why?"*

    [:octicons-arrow-right-24: Evolving Memory](concepts/evolving-memory.md)

-   :material-compass-outline:{ .lg .middle } __Forward — the VBDI Loop__

    ---

    A lightweight cognitive loop — *Current State → Vision → Blueprint → Design →
    Implementation → Feedback* — with an enforceable intent trace and a human gate at
    every altitude change.

    *"Where are we going, and is delivery faithful?"*

    [:octicons-arrow-right-24: The VBDI Loop](concepts/vbdi-loop.md)

</div>

## What makes it different

- **Vendor-neutral.** One shared memory; thin per-vendor pointers route every agent to a
  single hub. No lock-in.
- **Deterministic — no floating-point.** Every decision reduces to counting or comparing
  integers, so results are reproducible across agents and runs.
- **Mechanize the arithmetic, not the judgment.** The deterministic parts of a memory
  ritual (re-tiering, the archive move, adapter sync, integrity checks) are runnable
  helpers; every act of judgment stays with the agent and the human.
- **No manual user step.** Triggers, init, and adapter sync are agent-activated, with CI as
  the zero-config backstop.
- **Additive, non-destructive upgrades.** Versioned; an older repo upgrades in place via an
  idempotent ladder. Nothing is ever deleted — faded facts archive to a greppable index.

## Get going

<div class="grid cards" markdown>

-   __:material-rocket-launch: Getting Started__

    Install, enable a repo, and run your first session.

    [:octicons-arrow-right-24: Getting Started](getting-started.md)

-   __:material-book-open-variant: Concepts__

    How evolving memory, the VBDI loop, skills, and decay work.

    [:octicons-arrow-right-24: Concepts](concepts/index.md)

-   __:material-map-marker-path: Guides__

    Enable, upgrade, review, resolve conflicts, author skills.

    [:octicons-arrow-right-24: Guides](guides/index.md)

-   __:material-file-document-multiple: Reference__

    Built-in skills, decay parameters, vendor support, protocol files.

    [:octicons-arrow-right-24: Reference](reference/index.md)

</div>

!!! note "Status"
    agent-memory is independent research published under Apache-2.0. It is **not** an
    official Accenture product. The current release is documented against **v4.26.1**.
