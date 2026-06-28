# Memory Policy — agent-memory

> Tunable windows and triggers for this repo's own evolving-memory layer. All
> windows are in **sessions**, not days. Integers only — count session files, never
> compute a score. Rules live in `DECAY.md` / `REVIEW.md` at the repo root.

## Lifecycle windows (sessions)
- working_window:   3
- active_window:    8
- archive_window:   20

## Review triggers
- review_every:         10
- continuity_max_facts:  30  # primary lean signal (count of decaying facts/threads; verbosity/velocity-immune)
- continuity_max_lines: 600  # coarse backstop (raised from 300 in v4.24.0 — a mature layer sits ~450–600 even when healthy)

## Invariant verification
- verify_invariants_every: 40  # sessions between human re-checks of core / invariants (raised from 20: anti-fatigue at burst velocity)

## Auto-core (default: off — core is human-set)
- enabled:          false
- core_min_uses:    12
- core_min_reviews: 5

## Never decays
- tier: core
- anything under "## Architectural Invariants"
- unchecked Open Threads ( - [ ] )
