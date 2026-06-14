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

If a topic seems unfamiliar, grep `memory/archive/INDEX.md` (and follow a fact's
`origin` to its session) before saying you have no context — retrieval here is lexical
+ indexed by design (`DECAY.md` §11); facts fade to the archive but are never deleted.

## During the Session

- Treat `memory/continuity.md` as your working memory.
- Reference prior decisions before suggesting changes that might contradict them.
- Note any new facts, preferences, or decisions for post-session write.
- Track which fact **ids** you rely on, create, or pull back from the archive — you
  will list them in the session log's `## Memory References`. Do **not** edit fact
  metadata mid-session; the review ritual does the counting.

## After Every Session

A "session" is **one log-write** — the work since the last log, not necessarily a
whole conversation. A long, multi-task conversation may produce several logs; that's
expected (the decay math counts log files — `DECAY.md` §4).

1. **Create** `memory/sessions/YYYY-MM-DD-HHMMSS.md` using the UTC timestamp at
   **persist time** (when you write the file). Use `date -u +%Y-%m-%d-%H%M%S` or
   equivalent; omit colons for cross-platform compatibility. Title line:
   `# Session (endZ)` — the persist-time UTC stamp (full ISO 8601 ms) is required; a
   start time is optional/best-effort, so don't fabricate one. Never append to
   another contributor's session file.
   Include a `## Memory References` section listing the fact ids you referenced,
   created (born `tier: working`), or reactivated. This is the event log the review
   ritual reads — see `DECAY.md`.
2. **Update** `memory/continuity.md`:
   - Set `last_session` to today's date and your agent name.
   - Mark completed Open Threads `- [x]` and **leave them in place** — the review
     sweeps them once older than `archive_window`; don't archive them by hand.
   - Add new Open Threads surfaced during the session.
   - **Before recording a new fact, check it against existing ones** (`DECAY.md` §10):
     if it clearly replaces one, supersede that one (see below); if it genuinely
     conflicts, raise a `- [ ] Contradiction: …` Open Thread rather than keeping both.
   - Give any new fact a kebab `id` + footer: set `id`, `created`, `tier: working`
     (or `core` for an Architectural Invariant), `origin: <this session's file>`, and
     seed `last_used: today | uses: 1`. Don't hand-edit `uses`/`last_used`/`tier`
     afterward — the review owns them.
   - Update the substance of any fact that changed (not its usage metadata).
   - **Reversed a decision / a fact became false?** Add the successor (born
     `tier: working`, `supersedes: <old>`), mark the old fact `tier: superseded` +
     `superseded-by: <new>` (omit the link for pure invalidation), and record
     `Superseded: <old> → <new>` in `## Memory References`. This is a truth-state edit
     you own; the review archives it flagged "superseded" (`DECAY.md` §9).
3. **Review cadence.** If `sessions_since_last_review ≥ review_every`
   (`memory/decay-policy.md`), or `continuity.md` has grown past
   `continuity_max_lines`, run the review ritual now — see `REVIEW.md`. (Also run it
   on demand if the user says "review memory".)
4. Remind the user: `git add memory/ && git commit -m "session YYYY-MM-DD [agent]"`

**After-session checklist** (the ritual is convention — run it each time):
- [ ] session log written (persist-time filename + `## Memory References`)
- [ ] `continuity.md`: `last_session` set, threads checked, new facts have footers
- [ ] review run if cadence/size triggered (`REVIEW.md`)
- [ ] reminded the user to commit `memory/`

> Optional reinforcement: wire a lightweight Stop or pre-commit hook in your runtime
> so this ritual is *prompted*, not merely documented. It stays optional — the
> protocol itself is no-code.

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
