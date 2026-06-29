# Decay & Tiers

Facts don't accumulate forever. They **strengthen with use and fade without it** — measured
deterministically by *counting session files*, never by a similarity score. Every agent, on
every vendor, reaches the same result.

## The tiers

```
working → active → archive-candidate → archived
                                          (+ superseded, core)
```

| Tier | Meaning |
|---|---|
| `working` | Recently created or touched; in active rotation |
| `active` | Used steadily; the healthy middle |
| `archive-candidate` | Going stale; the next review may retire it |
| `archived` | Moved to `memory/archive/` with a greppable `INDEX.md` — never deleted |
| `superseded` | Terminal: reversed/false, with a `superseded-by` link (change, not disuse) |
| `core` | Never decays — invariants, the Vision (periodically re-verified by a human) |

The key quantity is **`sessions_since_last_used`**: how many session files have been written
since a fact was last referenced. Compare it against the windows below to decide the tier.

## Tunable windows

All windows are counted in **sessions**, not days — integers only. Defaults (this repo's own
`memory/decay-policy.md`):

| Parameter | Default | What it controls |
|---|---:|---|
| `working_window` | `3` | Within this many sessions of last use → `working` |
| `active_window` | `8` | Beyond `working` but within this → `active` |
| `archive_window` | `20` | Beyond `active` but within this → `archive-candidate`; past it → archive |
| `review_every` | `10` | Run a review at least every N sessions |
| `continuity_max_facts` | `30` | Primary lean signal — decaying facts/threads before a review is advised |
| `continuity_max_lines` | `600` | Coarse backstop on `continuity.md` size |
| `verify_invariants_every` | `40` | Sessions between human re-confirmations of `core` / invariants |

!!! note "Why these numbers"
    The defaults were retuned in v4.24.0 from real measurements across two enabled repos.
    `continuity_max_facts` is the **primary** signal because a count is immune to verbosity
    and velocity; `continuity_max_lines` was raised 300 → 600 because a *healthy* mature layer
    already sits ~450–600 lines. See [Decay Parameters](../reference/decay-parameters.md) to
    tune them.

## What never decays

- Anything in tier `core`.
- Anything under `## Architectural Invariants`.
- **Unchecked Open Threads** (`- [ ]`) — they are *pinned* by being unchecked. Their pinned-ness
  is the protection, **not** the tier label, so the tooling leaves a pinned thread's tier
  alone (it still refreshes the factual `uses` / `last_used`).

## Running it deterministically

The mechanical steps of a review are packaged as runnable helpers so a capable agent can't
silently skip them:

- [`refresh-metadata`](../reference/built-in-skills.md#refresh-metadata) recomputes every
  fact's `tier` / `uses` / `last_used` from the ledger.
- [`archive-fact`](../reference/built-in-skills.md#archive-fact) performs the archive *move*
  safely.
- [`memory-lint`](../reference/built-in-skills.md#memory-lint) verifies the result and flags a
  review that has gone overdue or a layer that has grown past budget.

*Deciding what to retire* stays the agent's judgment. See [Review Memory](../guides/review-memory.md)
for the full ritual, and [`DECAY.md`](../reference/protocol-files.md) for the authoritative rules.
