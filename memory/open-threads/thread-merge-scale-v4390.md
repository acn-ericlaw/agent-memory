- [x] **Shipped v4.39.0 (MINOR) — merge-scale memory: threads as files** (PR pending
  maintainer merge). From Eric's field report (team-scale `continuity.md` conflicts) +
  PR #27's artifact: one thread per `memory/open-threads/thread-<id>.md` (no index — the
  directory is it), `last_session` dropped (derived), archive `merge=union`, serialized
  reviews; PR #27 reviewed (3 verified never-pick-a-winner findings), closed with credit,
  `[duplicate-state-key]` + rehearsal-test pattern absorbed (Roland Heusser). Lesson:
  structure beats merge-time machinery — the rejected driver silently unioned the one case
  that must reach a human. Detail: docs/DESIGN-merge-scale.md + the 4.38.1→4.39.0 rung.
  → serves: vision-agent-memory (via bp-multi-user)
  <!-- id: merge-scale-v4390 | created: 2026-09-01 | last_used: 2026-09-01 | uses: 1 | tier: working | origin: 2026-09-01-185108 -->
