# DECAY — Evolving Memory Reference

> The rules of the evolving-memory layer: the metadata each fact carries, the tier
> lifecycle, and the **deterministic** rules that move facts between tiers.
> `REVIEW.md` is the *ritual* that applies these rules; this file is the *reference*.
>
> **This doc is generic and ships into every enabled repo** (installed at the repo
> root by `ENABLE.md`), because the review ritual runs *inside* the repo during
> normal sessions — an agent there needs the rules locally. It is the same in every
> repo; it carries no project-specific content.
>
> **Design principle — no floating-point math.** Every decision below reduces to
> counting items in a list or comparing integers, so any agent (Claude, Gemini,
> Cursor, …) reaches the *same* result. There is deliberately no `strength` score.

---

## 1. Fact metadata

Every fact in `memory/continuity.md` carries an HTML-comment footer. Invisible
when rendered, readable and editable by any agent or human, diff-friendly.

```markdown
- POST-only for mutations, no PUT/PATCH (legacy decision, do not change)
  <!-- id: post-only-mutations | created: 2026-06-08 | last_used: 2026-06-12 | uses: 14 | tier: active -->
```

| Field | Set | Recomputed at review? |
|---|---|---|
| `id` | once at creation; kebab-case, unique within the file; never changes | no |
| `created` | once at creation (date the fact entered memory) | no |
| `last_used` | date of the most recent session that referenced the id | **yes** |
| `uses` | count of sessions that referenced the id | **yes** |
| `tier` | lifecycle bucket (see §3) | **yes** |

There is no `strength` field. Importance is expressed structurally: `tier: core`,
or membership in the `## Architectural Invariants` section.

### Assigning an id
Lowercase, hyphenated, derived from the fact's gist (`webhook-fire-forget`,
`drizzle-over-prisma`). Unique within `continuity.md`. Once assigned it is
permanent — it is the handle that session logs use to reference the fact.

---

## 2. The event log — how usage is recorded

Usage is **not** hand-maintained on each fact. It is *derived* from session logs.
Every session log carries a `## Memory References` section:

```markdown
## Memory References
- Referenced: post-only-mutations, webhook-fire-forget
- Created: graphql-gateway-added (tier: working)
- Reactivated: drizzle-over-prisma
```

- **Referenced** — ids the session relied on or reinforced.
- **Created** — new facts added this session (born `tier: working`).
- **Reactivated** — ids pulled back from the archive.

So, for any id:
- `uses` = number of session logs whose `## Memory References` name it.
- `last_used` = the date of the latest such session log.

Both are recomputed during review (`REVIEW.md`), never typed by hand mid-session.

> **Session logs are immutable.** They are the source of truth for this projection.
> Never edit, renumber, or archive a past session log. `continuity.md` metadata is
> the *derived view*; the logs are the *ledger*.

---

## 3. Tiers

```
core              permanent. Human-set (§5). Never decays.
active            referenced within active_window sessions.
working           created within working_window sessions, not yet re-referenced. Probationary.
archive-candidate not referenced for > active_window but ≤ archive_window. Flagged, not yet moved.
archived          not referenced for > archive_window. Moved to memory/archive/YYYY-QN.md.
```

Movement is **bidirectional**: an archived id named in a session's `Referenced` or
`Reactivated` list is pulled back to `active`. Nothing is ever deleted.

---

## 4. The only arithmetic: counting session files

`sessions_since_last_used` = **the number of session files chronologically after
the one in `last_used`.** Session files are named `YYYY-MM-DD-HHMMSS.md` and sort
lexicographically = chronologically, so this is the length of a list, not a
formula: list `memory/sessions/`, find the file matching `last_used`, count what
comes after it. Every agent gets the same integer.

(If several sessions share a `last_used` date, count by file, not by date.)

---

## 5. Tier decision rules — apply in order, first match wins

Windows come from `memory/decay-policy.md` (integers, in sessions).

1. `tier: core` → **stays core.** Never auto-demoted. (Human override.)
2. Under `## Architectural Invariants` → **pinned**, treated as core.
3. Unchecked Open Thread (`- [ ]`) → **pinned active**, never decays (incomplete work).
4. `created` ≤ `working_window` sessions ago AND `uses ≤ 1` → **working**.
5. `sessions_since_last_used ≤ active_window` → **active**.
6. `active_window < sessions_since_last_used ≤ archive_window` → **archive-candidate**.
7. `sessions_since_last_used > archive_window` → **archived** → move to archive/.

---

## 6. Never-decay set

Exempt from steps 4–7 regardless of counts:
- `tier: core`
- everything under `## Architectural Invariants`
- unchecked Open Threads (`- [ ]`)

A *checked* Open Thread (`- [x]`) becomes eligible to be swept to the archive once
its completion is older than `archive_window` sessions (see `REVIEW.md`).

---

## 7. Auto-core (default OFF)

`core` is **human-set only** by default — the system never silently makes a fact
permanent. If `auto-core` is enabled in `decay-policy.md`, a fact may be promoted
to `core` only when `uses ≥ core_min_uses` **and** it has stayed `active` across
`core_min_reviews` consecutive reviews — and even then, surface it for the user to
confirm rather than promoting silently.

---

## 8. Manual override always wins

Any field a human edits by hand — especially `tier:` — is authoritative. Review
must not overwrite a hand-set `tier: core` or a hand-set `id`. Prefer archiving
over deleting, but if a human deletes a fact outright, respect it.
