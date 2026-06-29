# Decay Parameters

Every repo carries its own `memory/decay-policy.md` — tunable windows and triggers for its
evolving-memory layer. **All windows are in sessions, not days. Integers only** — count session
files, never compute a score. The rules that consume them live in `DECAY.md` / `REVIEW.md`.

## The full policy

```yaml
# Lifecycle windows (sessions)
working_window:   3
active_window:    8
archive_window:   20

# Review triggers
review_every:          10
continuity_max_facts:  30   # primary lean signal
continuity_max_lines:  600  # coarse backstop

# Invariant verification
verify_invariants_every: 40

# Auto-core (default: off — core is human-set)
enabled:          false
core_min_uses:    12
core_min_reviews: 5

# Never decays
# - tier: core
# - anything under "## Architectural Invariants"
# - unchecked Open Threads ( - [ ] )
```

## Reference

| Parameter | Default | Meaning |
|---|---:|---|
| `working_window` | `3` | `sessions_since_last_used` ≤ this → `working` |
| `active_window` | `8` | ≤ this (and past `working`) → `active` |
| `archive_window` | `20` | ≤ this (and past `active`) → `archive-candidate`; past it → archive |
| `review_every` | `10` | Run a review at least every N sessions; drives `[review-overdue]` |
| `continuity_max_facts` | `30` | Decaying facts/threads before `[continuity-bloat]` advises a review |
| `continuity_max_lines` | `600` | Coarse size backstop on `continuity.md` |
| `verify_invariants_every` | `40` | Sessions between human re-confirmations of `core` / invariants |
| `enabled` (auto-core) | `false` | Whether usage can auto-promote a fact to `core` (off by default — core is human-set) |
| `core_min_uses` | `12` | Auto-core threshold (only if `enabled`) |
| `core_min_reviews` | `5` | Auto-core threshold (only if `enabled`) |

## Tuning advice

- **`continuity_max_facts` is the primary signal.** A *count* of decaying facts is immune to
  verbosity and velocity, unlike a line count. Tune this first.
- **`continuity_max_lines` is a coarse backstop.** It was raised 300 → 600 in v4.24.0 because a
  *healthy* mature layer already sits ~450–600 lines (structural sections — Vision, Invariants,
  Key Decisions, Blueprint — don't decay but do count toward lines). Set too low and it's
  permanently red (alert fatigue).
- **`verify_invariants_every`** was raised 20 → 40 to avoid near-daily human re-confirms at
  burst velocity (10–20 sessions/day).
- The lifecycle windows (`working` / `active` / `archive`) and `review_every` rarely need
  changing — the common bloat cause was reviews not *running*, not the windows being wrong.
  The `[review-overdue]` advisory exists precisely for that.

!!! tip "Make changes a review, not a guess"
    After editing the policy, run [`memory-lint`](built-in-skills.md#memory-lint) and a
    [review](../guides/review-memory.md) so the new thresholds are applied consistently.
