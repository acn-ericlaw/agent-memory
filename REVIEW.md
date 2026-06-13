# REVIEW — The Memory Review Ritual

> When and how to recompute usage metadata, reshuffle tiers, and keep
> `memory/continuity.md` lean. Applies the rules in `DECAY.md`.
>
> Like `DECAY.md`, this doc is generic and **ships into every enabled repo**
> (installed at the repo root by `ENABLE.md`): the ritual runs *inside* the repo
> as part of the normal session routine, so the agent needs it locally.

---

## When it runs

Three triggers:
1. **Cadence** — when `sessions_since_last_review ≥ review_every` (from
   `memory/decay-policy.md`). Checked during the post-session update.
2. **On command** — the user says *"review memory"* / *"compact memory"*.
3. **Size** — when `memory/continuity.md` exceeds `continuity_max_lines`.

`last_review` is tracked in `continuity.md` Project State (a `YYYY-MM-DD` plus the
session file it last ran through).

## Inputs

- `memory/continuity.md` — facts + metadata
- `memory/decay-policy.md` — windows + triggers
- `memory/sessions/` — the event log; read each `## Memory References`
- `memory/archive/` — cold storage + `INDEX.md`

---

## The routine (incremental — the normal path)

1. **Gather the window.** List session files after `last_review`. Read each one's
   `## Memory References`.
2. **Apply events.** For every id named:
   - `Referenced` / `Created`: increment `uses`; set `last_used` to the latest
     session date that names the id.
   - `Reactivated`: if the id currently lives in the archive, move it back into
     `continuity.md` as `active`, then apply the Referenced bump.
3. **Re-tier every fact.** For each fact in `continuity.md`, compute
   `sessions_since_last_used` (count files — `DECAY.md` §4) and apply the
   `DECAY.md` §5 rules in order. Record each tier change.
4. **Archive.** Facts that resolve to `archived`:
   - append the fact *with its metadata comment* to `memory/archive/<YYYY>-Q<n>.md`
     under a dated heading,
   - add/refresh its line in `memory/archive/INDEX.md` (`id — one-line — <quarter file>`),
   - remove it from `continuity.md`.
5. **Sweep completed threads.** `- [x]` Open Threads whose completion is older than
   `archive_window` sessions move to the archive the same way (usually the biggest
   lean-up). Keep recently-completed threads for context.
6. **Stamp.** Set `last_review` to today + the latest session file name.
7. **Summarise.** Write a `## Memory Review` block into *this* session's log.

## Full rebuild (the ground-truth path)

Because metadata is *derived*, you can discard stored `uses`/`last_used`/`tier`
and recompute everything from scratch by scanning **all** session logs'
`## Memory References`. Use this to repair drift, after heavy manual edits, or if
reviews were skipped for a long stretch. The result is deterministic and
reproducible by any agent.

## Reactivation

When an archived id is named in a session (`Referenced`/`Reactivated`):
- move the fact from its `archive/<quarter>.md` back into `continuity.md`,
- set `tier: active`, refresh `last_used`, increment `uses`,
- remove or annotate its `archive/INDEX.md` line,
- note it in the review summary.

This two-way movement is what keeps the system smart rather than merely lossy.

---

## Review summary format

```markdown
## Memory Review (2026-06-20, through 2026-06-20-141503)
- Reactivated:   1  (drizzle-over-prisma — referenced today after 9 dormant sessions)
- Archived:      3  facts → memory/archive/2026-Q2.md
- Swept threads: 4  completed Open Threads → archive
- Tier changes:  6  (2 working→active, 1 active→archive-candidate, 3 →archived)
- Promoted core: 0  (auto-core off; core is human-set)
```

## Safety

- Never delete a fact — archiving is a *move*, not a removal.
- Never overwrite a hand-set `tier:` (especially `core`) or a hand-set `id`.
- Never edit past session logs — they are the immutable ledger this ritual reads.
- Stay within the repo's `memory/` and `archive/`; never touch `~/`, `~/.claude/`,
  Application Support, AppData, or system paths.
