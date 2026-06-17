---
name: hello-world
description: Demo / self-test of the agent-memory portable skills layer. Use when the user asks to run hello-world, test or verify portable skills work, or wants a greeting that proves the skills layer is wired up.
---

# hello-world

The canonical demonstration skill. It proves the agent-memory **portable skills layer**
works end-to-end, on any vendor. It deliberately does something tiny — the *mechanism* is
the lesson, not the capability.

## When to use

Run this when the user asks to test the skills layer, says "run hello-world", or wants a
greeting that confirms skills are wired up.

## What to do

1. **Run the bundled helper** (preferred — it computes the timestamps). With an optional
   name, run it and show its output:
   ```
   sh agent-skills/hello-world/scripts/hello.sh "<name-or-omit>"
   ```
   It prints the greeting, the **local time**, a **UTC timestamp**, and a reminder that
   agent-memory records **all session logs in UTC** (persist-time). The script is
   **agent-invoked** — the *tool itself* runs no code (the `no-build-step-agent-run`
   invariant); you run it at the user's direction.
2. **No shell available?** Print the greeting directly —
   `Hello from the agent-memory portable skills layer 👋` — and still tell the user the
   current **local time** and **UTC time**, and that **session logs are recorded in UTC**.
3. **Report which path invoked you**, so the test is legible. **Attribute by the *entry point*
   that triggered you, not by the file you read** — both paths read this same neutral `SKILL.md`,
   so "I read the neutral skill" is **not** evidence of the baseline. Before reporting "baseline,"
   check whether a vendor adapter for *your* runtime fired:
   - **Vendor adapter** — a native trigger pointed here: you were invoked by a **slash command**
     `/hello-world` (Gemini `.gemini/commands/hello-world.toml`), or your runtime **auto-matched
     a description** in `.claude/skills/`, `.cursor/rules/`, or `.kiro/skills/`. Name the adapter.
   - **`AGENTS.md` baseline** — *only* when no adapter fired: a natural-language request (e.g.
     Gemini "run hello-world", or any vendor with no synced adapter) led you here via the
     `AGENTS.md` "Skills" baseline. (Reminder: on Gemini, natural language always takes this path —
     the `.toml` is a slash command, not an NL auto-trigger.)
   If unsure which fired, check for a matching adapter file first, then report.

## Notes — this *is* the design demo

- This file (`agent-skills/hello-world/SKILL.md`) is the **single, committed, vendor-neutral
  source of truth**. Edit a skill here — **never** in an adapter.
- Per-vendor adapters are **thin, regenerated, gitignored pointers** to this file; they
  exist only for native auto-trigger and must not diverge from it.
- A real skill puts genuine capability here (steps, references, scripts). hello-world keeps
  it minimal on purpose.
