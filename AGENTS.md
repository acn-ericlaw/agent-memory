# Agent Instructions

This repository has two purposes:

1. **A shared memory system** — use it directly as your project's AI memory layer.
2. **An AI-enablement tool** — use it to AI-enable any other repository on your
   machine, including repos that already have vendor-specific AI files
   (Cursor, Aider, Continue, Cline, etc.) — those get migrated automatically.

Read the relevant section below based on what you have been asked to do.

---

## Purpose A — AI-Enable Another Repository

If the user says something like:

> "AI enable this repo `/path/to/project`"
> "Set up AI memory for `../my-app`"
> "AI enable this folder"
> "Migrate this repo to agent-memory"

**Read [`ENABLE.md`](./ENABLE.md) immediately and follow it exactly.**
That file contains the complete step-by-step protocol, including:

- Detection of existing vendor AI files (Cursor, Aider, Continue, etc.)
- Migration of vendor steering files and chat history into our unified format
- Conflict handling, dry-run support, and idempotent re-runs

For per-vendor migration rules (e.g. how to convert Aider's chat history,
where Cursor stores rules, how to parse Continue session JSON), see
[`MIGRATE.md`](./MIGRATE.md).

Do not proceed from memory. Do not improvise. Read `ENABLE.md` first.

---

## Purpose B — Use This Repo as Your Own Memory System

If the user is working *within* this repository (improving the tool itself,
adding vendor support, etc.), follow the standard memory protocol below.

### Before Every Session

Read these files before responding to anything:

1. `memory/instructions.md` — persona, rules, project context
2. `memory/continuity.md`   — current project state, open threads, decisions
3. `memory/sessions/`       — scan the most recent 2–3 session files

### During the Session

- Reference `memory/continuity.md` when relevant.
- Note any new facts, decisions, or preferences for post-session write.

### After Every Session

1. **Create** `memory/sessions/YYYY-MM-DD-HHMMSS.md` using the UTC timestamp at
   **persist time** (when you write the file — i.e. session end). Use
   `date -u +%Y-%m-%d-%H%M%S` or equivalent; omit colons for cross-platform
   compatibility. Title line: `# Session (startZ - endZ)` — full ISO 8601 with
   milliseconds for both. Write one session block. Never append to another
   contributor's session file.
2. **Update** `memory/continuity.md`:
   - Set `last_session` to today's date and your agent name.
   - Check off completed Open Threads.
   - Add new Open Threads.
   - Update any changed facts.
3. Remind the user to commit: `git add memory/ && git commit -m "session YYYY-MM-DD [agent]"`

### Multi-Agent Continuity

Check `last_session` in `continuity.md` and note the agent name. If it is **not
your own agent family** (e.g. Claude, Gemini, Copilot, Cursor), read that session
log in full before responding.

> Two memory layers: this repo's `memory/` is shared project state (committed to
> git); your runtime's user-scoped store (e.g. Claude Code's `~/.claude/`) is for
> personal preferences. Keep project facts here, preferences there.

---

## Supported Agent Bootstrap Files

| Agent | File |
|---|---|
| Claude Code | `CLAUDE.md` |
| Gemini CLI | `GEMINI.md` |
| ChatGPT / Codex | `AGENTS.md` (this file) |
| Cursor | `.cursorrules` |
| Windsurf | `.windsurfrules` |
| GitHub Copilot | `.github/copilot-instructions.md` |

## Supported Migration Sources

When AI-enabling a repo that already has AI tooling, these vendors are detected
and migrated automatically: Claude Code, Cursor, Cline, Roo Code, Aider,
Continue.dev, Codeium/Windsurf, GitHub Copilot, GPT/Codex agents, Zed AI,
Gemini CLI. See `MIGRATE.md` for protocols.
