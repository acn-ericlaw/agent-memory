# Memory Policy — taskflow-api

> Tunable windows and triggers for the evolving-memory layer. All windows are in
> **sessions**, not days. Integers only — the agent counts session files, it never
> computes a score. Rules live in `DECAY.md` / `REVIEW.md`.

## Lifecycle windows (sessions)
- working_window:   3
- active_window:    8
- archive_window:   20

## Review triggers
- review_every:         10
- continuity_max_facts:  30  # primary lean signal (count of decaying facts/threads)
- continuity_max_lines: 600  # coarse backstop

## Invariant verification
- verify_invariants_every: 40  # sessions between human re-checks of core / invariants

## Auto-core (default: off — core is human-set)
- enabled:          false
- core_min_uses:    12
- core_min_reviews: 5

## Never decays
- tier: core
- anything under "## Architectural Invariants"
- unchecked Open Threads ( - [ ] )
