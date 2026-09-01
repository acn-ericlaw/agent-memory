- [x] **Shipped v4.36.0 (MINOR) — composable Git hook dispatchers.** Hook entrypoints became
  fragment dispatchers over `.githooks/<hook>.d/*`; guard + ritual capture moved intact to
  managed `50-` fragments (PR #22, first external contribution; ADR-0007). Lesson: the id
  keeps its dev-numbered slug after a rebase renumber — origin logs are immutable. Full
  detail: origin log + the `4.35.0→4.36.0` rung. → serves: vision-agent-memory
  <!-- id: hook-dispatchers-v4350 | created: 2026-08-20 | last_used: 2026-08-20 | uses: 1 | tier: archive-candidate | origin: 2026-08-20-210047 -->
