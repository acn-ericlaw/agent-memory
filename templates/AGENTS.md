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

If a topic seems unfamiliar, grep `memory/archive/INDEX.md` before saying you have
no context — facts fade to the archive but are never deleted.

## During the Session

- Treat `memory/continuity.md` as your working memory.
- Reference prior decisions before suggesting changes that might contradict them.
- Note any new facts, preferences, or decisions for post-session write.
- Track which fact **ids** you rely on, create, or pull back from the archive — you
  will list them in the session log's `## Memory References`. Do **not** edit fact
  metadata mid-session; the review ritual does the counting.

## After Every Session

1. **Create** `memory/sessions/YYYY-MM-DD-HHMMSS.md` using the UTC timestamp at
   **persist time** (when you write the file — i.e. session end). Use
   `date -u +%Y-%m-%d-%H%M%S` or equivalent; omit colons for cross-platform
   compatibility. Title line: `# Session (startZ - endZ)` — full ISO 8601 with
   milliseconds for both. Write one session block. Never append to another
   contributor's session file.
   Include a `## Memory References` section listing the fact ids you referenced,
   created (born `tier: working`), or reactivated. This is the event log the review
   ritual reads — see `DECAY.md`.
2. **Update** `memory/continuity.md`:
   - Set `last_session` to today's date and your agent name.
   - Check off completed Open Threads.
   - Add new Open Threads surfaced during the session.
   - Give any new fact a kebab `id` + metadata footer, `tier: working`.
   - Update any facts that changed.
3. **Review cadence.** If `sessions_since_last_review ≥ review_every`
   (`memory/decay-policy.md`), or `continuity.md` has grown past
   `continuity_max_lines`, run the review ritual now — see `REVIEW.md`. (Also run it
   on demand if the user says "review memory".)
4. Remind the user: `git add memory/ && git commit -m "session YYYY-MM-DD [agent]"`

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
  decay-policy.md     ← evolving-memory windows/triggers (tune as needed)
  sessions/           ← dated session logs (event log)   (append; never edit past logs)
  archive/            ← faded facts + swept threads       (cold storage; never deleted)
    INDEX.md          ← greppable index of archived facts
.agent/
  schema.md           ← file format reference
  version.md          ← which agent-memory version this repo is on
DECAY.md              ← evolving-memory rules (metadata, tiers, deterministic decay)
REVIEW.md             ← the review ritual (when/how to recompute + archive)
```
