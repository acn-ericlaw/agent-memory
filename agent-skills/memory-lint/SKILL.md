---
name: memory-lint
description: Deterministic integrity check for the agent-memory layer. Use after a memory review, before committing memory/ changes, or in CI to catch decay miscounts — facts archived while still referenced, an id in both continuity and the archive, tier or supersession drift. The agent judges meaning; the script does the counting.
---

# memory-lint

A deterministic safety net for the evolving-memory layer. Decay is integer-counting by design, but
an agent counting session files **by hand** can miscompute `sessions_since_last_used` and archive a
fact that's still in use — this actually happened (a fresh-agent review over-archived recent facts,
and a hand re-check still missed one). This skill moves that counting from agent judgment to a
script, so the riskiest operation is verified against observable evidence.

## When to use

- **After** running the memory **review** ritual (`REVIEW.md`) — verify its archival decisions.
- **Before** committing `memory/` changes.
- In **CI** or a **pre-commit hook** (the optional reinforcement `AGENTS.md` mentions) — a non-zero
  exit fails the gate.

## What to do

1. Run the bundled checker from the repo root (needs **Python 3**, stdlib only — no install):
   ```
   python3 agent-skills/memory-lint/scripts/memory-lint.py
   ```
   Flags: `--strict` (also fail on warnings), `--root PATH` (point at a specific repo).
2. It checks, deterministically:
   - **no id lives in both `continuity.md` and the archive** (a fact exists in exactly one place);
   - **no archived-as-faded fact was referenced within `archive_window` sessions** — the decay-miscount
     guard: if it was, the count was wrong, so **reactivate it**;
   - *advisory* — continuity facts overdue for archival (`sslu > archive_window`), excluding `core`,
     `superseded`, and pinned `- [ ]` open threads (which never decay);
   - supersession links resolve (`supersedes` / `superseded-by` point at real footers).
3. **ERROR** (exit 1) → fix per `DECAY.md` / `REVIEW.md`: reactivate an over-archived fact (move it
   back into `continuity.md`), de-duplicate, or repair a link. **WARN** is advisory — the next review
   may act on it.

## Notes — scope and philosophy

- **Optional; the tool never runs it.** The memory layer works without it (markdown + agent is the
  runtime — `no-build-step-agent-run`). This is a *verifier*, invoked by the agent / human / CI at
  your direction.
- It lints the **arithmetic and integrity**; it does **not** judge *meaning* (what's worth recording,
  supersession truth-state, contradictions) — that stays human/agent.
- **No Python?** Run the checks by hand per the list above — e.g. `grep` each about-to-be-archived id
  against the last `archive_window` session logs (any hit ⇒ don't archive). The script just makes it
  reliable and CI-able.
