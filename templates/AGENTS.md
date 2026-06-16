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
2. `memory/continuity.md`   — current state, open threads, key decisions (+ Blueprint gaps)
3. `memory/vision.md`       — the target the work serves (the VBDI north star)
4. `memory/sessions/`       — scan the most recent 2–3 session logs

If a topic seems unfamiliar, grep `memory/archive/INDEX.md` (and follow a fact's
`origin` to its session) before saying you have no context — retrieval here is lexical
+ indexed by design (`DECAY.md` §11); facts fade to the archive but are never deleted.

## The cognitive loop (VBDI)

This repo runs a forward loop on top of the memory layer (`DECAY.md` §12):
**Current State (`continuity.md`) → Vision (`memory/vision.md`) → Blueprint (gap) →
Design → Implementation → Feedback (review) → repeat.** When you propose significant
work, tie it to a Blueprint gap (a `(blueprint)` Open Thread that `serves:` the Vision)
and to the Design it realizes — so intent is traceable and drift is detectable. Each
altitude transition (confirming the Vision, opening or closing a gap) is a **human
gate**: propose, then let the human approve. Never fabricate the Vision.

## Skills

If a `agent-skills/` directory exists, it holds the project's **capabilities** — committed,
vendor-neutral `agent-skills/<name>/SKILL.md` files (a `name`, a `description` that says *when*
to use it, a procedure, and maybe helper scripts). **This is the runtime:** when a task
matches a skill's `description`, read and follow that `SKILL.md` (and any scripts it
references). The agent is the runtime — no engine required, so this works on any vendor.

### Authoring a skill

To add a skill, create **`agent-skills/<name>/SKILL.md`** (the committed source of truth):
frontmatter `name` + a sharp `description` (the *when-to-use* trigger), then the procedure;
put any helper scripts in `agent-skills/<name>/scripts/`. Then run **"sync skill adapters"**
to generate your vendor's adapter. **Never author a skill directly in a vendor folder**
(`.claude/skills/`, `.gemini/commands/`, `.cursor/rules/`) — those are gitignored, regenerated
*pointers*; a skill written there won't be shared and isn't the source of truth. (Some
vendors' built-in skill creators default to their own folder — if that happens, **adopt** it
into `agent-skills/`; see "Adopt a skill" below.)

### Adapters — optional, local, regenerated

Some runtimes auto-discover a *native* adapter for ergonomic auto-trigger. Adapters are
**thin pointers** to the neutral skill, **gitignored** (personal/per-machine), and
**regenerated** — never hand-edited, never a copy. The source of truth is always
`agent-skills/<name>/SKILL.md`; edit skills there. For each `agent-skills/<name>/SKILL.md`
(using its `name` + `description`), the adapters are:

- **Claude Code** → `.claude/skills/<name>/SKILL.md`:
  ```
  ---
  name: <name>
  description: <description>
  ---
  Maintained vendor-neutrally. Read and follow `agent-skills/<name>/SKILL.md` (repo root)
  and any scripts it references.
  ```
- **Gemini CLI** → `.gemini/commands/<name>.toml`:
  ```
  description = "<description>"
  prompt = "Read and follow the skill at agent-skills/<name>/SKILL.md (repo root), including any scripts it references, then carry out: {{args}}"
  ```
- **Cursor** → `.cursor/rules/<name>.mdc` (the "agent-requested" type — description-matched,
  so `globs` is empty and `alwaysApply` is false):
  ```
  ---
  description: <description>
  globs:
  alwaysApply: false
  ---
  When this applies, read and follow `agent-skills/<name>/SKILL.md` (repo root) and any
  scripts it references.
  ```

### Sync skill adapters

Adapters are gitignored, so a freshly **cloned or pulled** repo has the neutral skills but
**no adapters on this machine** — native `/`-commands / auto-trigger won't exist until you
regenerate them. (The runtime baseline above always works regardless; this is only for
native ergonomics.) When the user says **"sync skill adapters"** — or after cloning a repo
that has `agent-skills/` — regenerate them:

1. For **each** `agent-skills/<name>/SKILL.md`, (re)write all three adapters above
   (idempotent — overwrite the adapter; never touch the neutral skill or its scripts).
2. **Prune** orphans: remove any *generated adapter* (one whose body points at
   `agent-skills/<name>/`) whose neutral skill no longer exists, so adapters stay in
   lockstep. Never delete other files in those vendor dirs.
3. Report what was regenerated / pruned. This touches no committed file (adapters are
   gitignored) and is **not** a version change.

### Adopt a skill (vendor → neutral) — the safety net

If a skill was authored natively in a vendor folder (e.g. a built-in skill creator wrote to
`.claude/skills/<name>/`), it's **stranded** — gitignored and not the source of truth.
**Adopt it** into the shared layer (the reverse of sync — the same move migration makes at
enable):

1. Copy its content into `agent-skills/<name>/SKILL.md` — normalize the frontmatter to
   `name` + `description`; move any bundled scripts to `agent-skills/<name>/scripts/`.
2. Run **"sync skill adapters"** — regenerates the vendor adapter as a *pointer*, replacing
   the hand-authored native file (now redundant).
3. Commit `agent-skills/<name>/`. It is now the shared source of truth; teammates pull + sync.

Run it on demand ("adopt skill `<name>`"), and it is **checked at session close** (see "After
Every Session") so a natively-authored skill never silently stays unshared.

See `.agent/schema.md` and `docs/DESIGN-skills-layer.md`.

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
3. **Skills safety check** (if `agent-skills/` exists or you authored a skill). Did a skill
   land in a **vendor folder** (`.claude/skills/<name>/`, `.gemini/commands/<name>.toml`,
   `.cursor/rules/<name>.mdc`) with **no matching `agent-skills/<name>/`**? If so it is
   stranded (gitignored, unshared) — **adopt it** before committing: promote it into
   `agent-skills/<name>/SKILL.md`, then "sync skill adapters" (see "Skills" → "Adopt a
   skill"). If nothing was authored in a vendor folder, this is a no-op.
4. **Review cadence.** If `sessions_since_last_review ≥ review_every`
   (`memory/decay-policy.md`), or `continuity.md` has grown past
   `continuity_max_lines`, run the review ritual now — see `REVIEW.md`. (Also run it
   on demand if the user says "review memory".)
5. Remind the user: `git add memory/ && git commit -m "session YYYY-MM-DD [agent]"`

**After-session checklist** (the ritual is convention — run it each time):
- [ ] session log written (persist-time filename + `## Memory References`)
- [ ] `continuity.md`: `last_session` set, threads checked, new facts have footers
- [ ] review run if cadence/size triggered (`REVIEW.md`)
- [ ] skills safety check — any skill authored in a vendor folder adopted into `agent-skills/`?
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
agent-skills/               ← cross-vendor capabilities          (committed; vendor-neutral)
  <name>/SKILL.md     ← one skill: name + when-to-use + procedure (the source of truth)
.agent/
  schema.md           ← file format reference
  version.md          ← which agent-memory version this repo is on
DECAY.md              ← evolving-memory rules (metadata, tiers, deterministic decay)
REVIEW.md             ← the review ritual (when/how to recompute + archive)
```
