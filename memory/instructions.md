# Agent Instructions — agent-memory

## What This Project Is

A no-code shared memory system and AI-enablement tool. It has two modes:

1. **Memory system** — used directly as the AI memory layer for any project.
2. **Enablement tool** — used to AI-enable any other repository on the user's machine.

When a user says "AI enable this repo [path]", read `ENABLE.md` and follow it exactly.
When the user is working on this repo itself, follow the standard memory protocol.

**Type:** Developer tooling / meta-framework
**Primary language:** Markdown (no code — files are the interface)

## Core Rules

1. If asked to AI-enable a repo, read `ENABLE.md` before doing anything.
2. Never copy templates blindly — always analyse the target repo first.
3. Never modify source code in target repos — only create memory and bootstrap files.
4. Templates live in `templates/` — always use them as the structure guide.
5. Record all enablement sessions in this repo's own session log.

## Conventions

- All placeholder text uses `{{UPPER_SNAKE_CASE}}` format
- Templates mirror the final output structure exactly
- Examples in `examples/` show real filled-in output, not generic placeholders
