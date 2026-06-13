# Agent Instructions

This repository uses the **agent-memory** shared memory system.
It is configured for AI-assisted development with any major agent runtime.

## Two Memory Layers

This repo's `memory/` holds **project state, shared across all agents and committed
to git.** It is separate from any **personal, user-scoped memory your runtime keeps
outside the repo** (e.g. Claude Code's `~/.claude/`, which holds your individual
preferences). Project facts, decisions, and session logs go in this repo's
`memory/`; personal preferences stay in your runtime's own store.

## Before Every Session

Read these files before responding to anything:

1. `memory/instructions.md` — project context, rules, and conventions
2. `memory/continuity.md`   — current project state, open threads, key decisions
3. `memory/sessions/`       — scan the most recent 2–3 session logs

## During the Session

- Treat `memory/continuity.md` as your working memory.
- Reference prior decisions before suggesting changes that might contradict them.
- Note any new facts, preferences, or decisions for post-session write.

## After Every Session

1. **Create** `memory/sessions/YYYY-MM-DD-XXXX.md` where `XXXX` is a 4-character
   random hex suffix you generate at session-start (e.g. `a3f2`). Write a single
   `## Session 1` block. Never append to another contributor's session file.
2. **Update** `memory/continuity.md`:
   - Set `last_session` to today's date and your agent name.
   - Check off completed Open Threads.
   - Add new Open Threads surfaced during the session.
   - Update any facts that changed.
3. Remind the user: `git add memory/ && git commit -m "session YYYY-MM-DD [agent]"`

## Multi-Agent Continuity

Check `last_session` in `continuity.md` and note the agent name recorded there.
If it is **not your own agent family** (e.g. Claude, Gemini, Copilot, Cursor),
read that day's session log in full before proceeding — the memory files are the
shared ground truth across all agents.

## Memory File Locations

```
memory/
  instructions.md     ← project context + agent rules    (edit rarely)
  continuity.md       ← live project state               (update every session)
  sessions/           ← dated session logs               (append every session)
.agent/
  schema.md           ← file format reference
```
