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
3. **Report the result — not your invocation path.** Confirm the skill ran (show the greeting +
   timestamps) and that you read the single neutral source `agent-skills/hello-world/SKILL.md` —
   that is the demonstration: the portable layer works on this vendor.
   **Do not try to report *which* path triggered you** (native adapter vs. `AGENTS.md` baseline).
   You can't tell reliably: a vendor like Gemini **expands a `/hello-world` slash command into this
   prompt *before you see it***, so the trigger is invisible to you, and the neutral skill reads
   identically on every path. The proof of native wiring is simply that the user's invocation *ran
   this skill*; **how** they invoked it (a `/`-command, a description match, or plain language) is
   theirs to know, not yours to guess. (Don't re-introduce path self-reporting — three cross-vendor
   dogfood runs showed agents get it wrong because the signal isn't available to them.)

## Notes — this *is* the design demo

- This file (`agent-skills/hello-world/SKILL.md`) is the **single, committed, vendor-neutral
  source of truth**. Edit a skill here — **never** in an adapter.
- Per-vendor adapters are **thin, regenerated, gitignored pointers** to this file; they
  exist only for native auto-trigger and must not diverge from it.
- A real skill puts genuine capability here (steps, references, scripts). hello-world keeps
  it minimal on purpose.
