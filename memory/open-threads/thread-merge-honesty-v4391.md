- [x] **Shipped v4.39.1 (PATCH) — same-thread merge claim: honest boundary** (PR pending
  maintainer merge). An independent CoPilot assessment of v4.39.0 (same-day, 8/10) caught
  the docs overstating git: conflicts arise only on adjacent/overlapping hunks; separated
  same-thread edits merge cleanly keeping both sides (verified by rehearsal; boundary =
  one unchanged line). Docs state the boundary; merge-contract test pins it (4 → 6 cases).
  Lesson: state what the mechanism guarantees, not what the design intends — and external
  fresh-context review catches exactly this class. Detail: the 4.39.0→4.39.1 rung.
  → serves: vision-agent-memory (via bp-multi-user)
  <!-- id: merge-honesty-v4391 | created: 2026-09-01 | last_used: 2026-09-01 | uses: 1 | tier: working | origin: 2026-09-01-204203 -->
