---
name: hello-world
description: Demonstration / self-test skill for the agent-memory portable skills layer. Use when the user asks to "run the hello-world skill", to test or verify that portable skills work, or wants a friendly greeting (with local + UTC time) that proves the skills layer is wired up.
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
3. **Report which path invoked you**, so the test is legible:
   - the **`AGENTS.md` baseline** — you read this `SKILL.md` because the task matched the
     `description` (works on every vendor, no engine), or
   - a **vendor adapter** (`.claude/skills/`, `.gemini/commands/`, `.cursor/rules/`) that
     pointed here.

## Notes — this *is* the design demo

- This file (`agent-skills/hello-world/SKILL.md`) is the **single, committed, vendor-neutral
  source of truth**. Edit a skill here — **never** in an adapter.
- Per-vendor adapters are **thin, regenerated, gitignored pointers** to this file; they
  exist only for native auto-trigger and must not diverge from it.
- A real skill puts genuine capability here (steps, references, scripts). hello-world keeps
  it minimal on purpose.
