# Example — Evolving Memory in Action

A worked example of the evolving-memory layer (`DECAY.md` + `REVIEW.md`) on a
**fictional** project, `taskflow-api`. It shows one review cycle end to end:

| File | What it shows |
|---|---|
| `continuity-before.md` | Live state *before* the review at session `2026-06-20-141503` |
| `sessions/2026-06-20-141503.md` | The session log — its `## Memory References` (the event log) and the `## Memory Review` summary |
| `continuity-after.md` | The same `continuity.md` *after* the review ran |
| `archive/2026-Q2.md` | Cold storage — facts moved out, plus the reactivated one annotated |
| `archive/INDEX.md` | Greppable index of archived facts |
| `decay-policy.md` | The windows used here (the defaults) |

## What happened in this cycle

The review ran because 10 sessions had passed since `last_review` (the
`review_every` default). Reading the session log's `## Memory References` and
counting session files (no floating-point math — see `DECAY.md` §4), the review:

- **Reactivated** `drizzle-over-prisma` — it had been archived in Q2, but the team
  referenced it today when deciding the new reporting service's ORM. Pulled back to
  `active`.
- **Archived** `legacy-soap-adapter` and `csv-bulk-import` — both unreferenced for
  more than `archive_window` (20) sessions.
- **Swept** the completed thread `thread-ci-migration` (`[x]`, done long ago) to
  the archive.
- **Superseded** `rest-versioning-uri` — the team reversed API versioning to be
  header-based today, so the URI-path decision is now *false* (not merely stale). It
  was marked `tier: superseded` at write time and archived flagged "superseded," its
  successor `rest-versioning-header` carrying the `supersedes` link. (`DECAY.md` §9)
- **Re-tiered**: `graphql-gateway` `working → active` (referenced again), and
  `jwt-15min-expiry` `active → archive-candidate` (going stale, not yet gone).
- Left `core` facts and the open thread untouched — they never decay.
- **Prompted invariant re-verification** — the `core` invariants had never been
  re-confirmed, and `verify_invariants_every` (20) was due, so the review raised a
  one-off Open Thread asking a human to re-confirm `post-only-mutations` and
  `utc-everywhere` (or supersede them). The review never auto-invalidates an invariant
  — never-decay ≠ never-checked. (`DECAY.md` §6/§9)

Net effect: `continuity.md` got leaner, nothing was lost, and a still-relevant fact
came back automatically.
