# Memory Smoke Test — agent-memory

> A cheap, manual check that the memory layer can actually orient a newcomer. **A fresh
> agent answers these from `memory/` alone** — no source code, no asking the user — then
> marks each ✅ (answerable from memory) or ❌ (gap). An ❌ is a *memory* gap: fix it by
> adding the missing fact, never by softening the question. App-level memory evaluation
> is an unsolved, bespoke problem industry-wide; this is the no-code, markdown version.

## How to run

1. Read **only** `memory/instructions.md`, `memory/continuity.md`, the latest 2–3
   `memory/sessions/`, and `memory/archive/INDEX.md`. Do not read source or ask the user.
2. Answer each question from those alone; mark ✅ or ❌ (with a one-line note on misses).
3. Append a row to the **Result log**. For each ❌, add the missing fact to memory (or
   open a thread to capture it) — then the next run should pass.

Run it **on demand** ("run the memory smoke test"), after a large change, or alongside a
review. Don't edit the questions to make them pass.

## Orientation questions (generic — apply to any repo)

1. What does this project do, and what type is it? *(→ instructions "What This Project Is")*
2. What is the stack — language, key dependencies, versions? *(→ continuity "Stack & Tools")*
3. What are the architectural invariants — things that must never change? *(→ continuity "Architectural Invariants")*
4. What were the last 2–3 key decisions, and **why**? *(→ continuity "Key Decisions" / recent sessions)*
5. What is in progress right now? *(→ continuity "Open Threads")*
6. What conventions should new code follow? *(→ instructions / continuity "Conventions")*
7. Any recorded user preferences or team / agent assignments? *(→ continuity — explicit only)*
8. Has any past decision been reversed or **superseded** — and by what? *(→ continuity superseded facts / `archive/INDEX.md`)*

## Project-specific questions (seeded at enable; grow these as the project does)

9. What are the three enable **modes** (A / B / C), and when does each apply? *(→ continuity "Key Decisions" / ENABLE.md)*
10. Where do the evolving-memory rules live, and which docs ship into enabled repos vs. stay operator-only? *(→ continuity / CLAUDE.md architecture: DECAY.md & REVIEW.md ship; MIGRATE.md & UPGRADE.md are operator-only)*
11. What is the current `VERSION`, and what did the recent releases (3.1.0–3.6.0) add? *(→ continuity "What's Been Built" + Shipped threads / CHANGELOG)*
12. What are the non-negotiable scope constraints when enabling a target repo? *(→ continuity "Architectural Invariants": target-repo scope only; never delete vendor files; never pick a winner)*

## Result log

| Date | Through session | Score (✅/total) | Gaps found → action |
|---|---|---|---|
| 2026-06-14 | (P4 enable) | — | baseline — run the test to populate |
