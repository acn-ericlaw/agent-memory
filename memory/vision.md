# Vision — agent-memory

> The north star: the target future state of this tool. Set by the maintainer
> (2026-06-14), fine-tuned with Claude Code. Treated as `core` (never decays) but
> re-confirmed on the invariant-verification cadence — a vision can go stale. The
> **Blueprint** (Open Threads tagged `(blueprint)` in `continuity.md`) tracks the gap
> from Current State to here; Designs and Implementations trace back to this id.
>
> <!-- id: vision-agent-memory | created: 2026-06-14 | last_used: 2026-06-18 | uses: 39 | tier: core -->

## Elevator statement

A **lightweight, vendor-neutral AI memory tool for human–AI collaboration** that turns a
clear, shared vision into **deterministic delivery with near-zero drift**.

## What it should become

- **Evolving memory + a forward cognitive loop.** Beyond a faithful record (decay,
  supersession, provenance, review), a *goal-aware* driver of delivery:
  Current State → Vision → Blueprint → Design → Implementation → Feedback.
- **Greenfield *and* brownfield.** Build from a vision where there is no code yet, **and**
  enable/migrate an existing repo — each delivered increment becoming the next Current State.
- **Multi-contributor by design.** Many people and many *different* AI vendors collaborate
  through one shared, committed `memory/` on the same enabled repository — without drift,
  and without stepping on each other.

## For whom

Human–AI pairs and teams building or evolving software together — across any AI vendor,
with multiple contributors on one enabled repository.

## Success criteria

- **Near-zero drift, faithful delivery** — what gets built traces to what was intended
  (the Node→Rust rewrite, generalized to all work).
- A fresh agent or teammate can **orient and contribute from memory alone** (the smoke
  test passes) — no re-explaining, no rabbit holes.
- Intent is **traceable end-to-end** (Implementation → Design → Blueprint → Vision) and
  **drift is detectable** (grep / review), never silent.
- Adoption stays **"point it at a repo,"** not a process rollout.

## Non-goals (what it must never become)

- **Never heavyweight** — no SDLC ceremony, no phase-gated waterfall, no Jira.
- **Never vendor-locked** — no dependence on a single AI vendor or runtime.
- **Never requires code** — markdown-only; the files are the product, the agent is the runtime.
- **Never caps creativity** — it guides thinking, it does not prescribe execution;
  structure *enables* creativity, it does not cage it.
- **Never a database / index server** — retrieval stays lexical + indexed, bounded by
  project scale.

## Mental model

> Move from the current state to the target state through gap identification, structured
> action, and continuous learning — with evolving memory as the deterministic substrate.
