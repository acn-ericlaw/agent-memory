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
3. **Report which path invoked you**, so the test is legible. **Attribute by *how you were
   invoked* — not by the file you read, and never by a directory scan.** Both paths read this same
   neutral `SKILL.md`, so "I read the neutral skill" is **not** evidence of the baseline. Decide
   from the trigger:
   - **Vendor adapter (native trigger).** You were invoked by a **slash command** — e.g. the user
     typed `/hello-world` (Gemini `.gemini/commands/hello-world.toml`) — or your runtime
     **auto-matched a description** (Claude `.claude/skills/`, Cursor `.cursor/rules/`, Kiro
     `.kiro/skills/`). A slash command **cannot exist unless its adapter is loaded**, so the
     invocation itself *proves* the adapter fired — name it; don't second-guess it.
   - **`AGENTS.md` baseline.** *Only* a plain **natural-language** request ("run hello-world") with
     no slash command and no auto-match. (On Gemini, natural language always takes this path — the
     `.toml` is a slash command, not an NL auto-trigger.)
   **Do not infer "no adapter" from a directory scan.** Adapters are **gitignored**, so file/folder
   tools routinely hide them — a listing may report *"0 items (1 ignored)"* while the adapter is
   right there. Trust the invocation method, not the folder listing.

## Notes — this *is* the design demo

- This file (`agent-skills/hello-world/SKILL.md`) is the **single, committed, vendor-neutral
  source of truth**. Edit a skill here — **never** in an adapter.
- Per-vendor adapters are **thin, regenerated, gitignored pointers** to this file; they
  exist only for native auto-trigger and must not diverge from it.
- A real skill puts genuine capability here (steps, references, scripts). hello-world keeps
  it minimal on purpose.
