# Industry-Alignment Assessment — agent-memory

> **Baseline snapshot.** Re-run this assessment periodically and compare the
> scorecard to track progress. Each gap closed should flip a row from ⬜ → ✅.
>
> - **Date:** 2026-06-13
> - **Tool version:** 3.0.0 (evolving-memory layer)
> - **Assessed by:** Claude Code, against web research (June 2026) — sources at bottom
> - **Purpose:** measure the tool against 2026 agent-memory best practice; set a backlog

---

## Fairness frame (read first)

Most high-profile memory work (Mem0, Zep, Letta; the LoCoMo / LongMemEval / BEAM
benchmarks) targets **conversational / personal-assistant memory** at scale —
millions of turns, vector retrieval, identity resolution. This tool is a different,
narrower niche: **human-curated, cross-vendor, project/team dev memory.**

The right yardstick is therefore **Anthropic's file-based memory tool, the upcoming
"Memory Files," the AGENTS.md standard, and the "context engineering" school** — not
Mem0-vs-Zep. Judged there, the tool is on the frontier. Some "gaps" below (vector
search, identity resolution) barely apply to this niche; one or two genuinely do.

## Verdict (2026-06-13)

**On track — and in two places ahead of where you'd expect a markdown tool to be.**
The design independently landed on a memory-governance pattern a 2026 paper proposes
as best practice (immutable ledger + mutable projection + replay), and its deliberate
omissions (external graph DB, vector store) are being *validated* by the industry's
own retreat toward deployment simplicity. The one real, addressable gap is
**temporal / supersession handling** — facts that become *false*, not just unused.

## Where the tool is aligned with the 2026 direction

- **File-based, agent-managed memory is now first-class.** Anthropic's memory tool is
  "a memory file directory" the agent CRUDs across sessions; the unreleased "Memory
  Files" feature distributes notes "across multiple structured documents organized by
  topic, project, or context" — precisely `memory/{continuity,instructions}.md` +
  `sessions/` + `archive/`. The "just-in-time / NOTES.md" context-engineering pattern
  is this model exactly.
- **Vendor neutrality via AGENTS.md is now *the* standard** — Linux Foundation /
  Agentic AI Foundation, ~60k repos, read by 20+ tools. The hub-and-spoke design
  (AGENTS.md as dispatcher; thin vendor pointers deferring to it) matches it, and
  avoids the one anti-pattern: forking divergent content per vendor.
- **Consolidation + forgetting is the hot theme** ("evolving memory" is now a named
  research area). The review ritual + tiers + archive *is* consolidation-and-forgetting.
- **"2026 agents need a write path, not just a retriever."** The event-sourced write
  path (sessions → review → continuity) is squarely this.
- **Memory taxonomy** (episodic / semantic / procedural) maps cleanly: `sessions/` =
  episodic, `continuity.md` = semantic, `instructions.md` + conventions = procedural
  (the type the field calls "underexplored").

## Where the tool is arguably ahead / distinctive

- **Reversible reconciliation — the standout.** The *Governing Evolving Memory* (SSGM)
  paper's flagship principle: "dual-track storage — a mutable active store paired with
  an immutable episodic ledger, enabling periodic replay and correction against raw
  traces to bound drift." That is exactly `continuity.md` (mutable projection) +
  `sessions/` (immutable ledger) + the review's full-rebuild path. Also confers strong
  protection against **semantic drift** (the paper's #1 stability risk): facts are
  *moved/retiered*, never iteratively re-summarized — no lossy rewriting.
- **Determinism-first.** The field tolerates non-deterministic LLM scoring and leans on
  benchmarks for reproducible *comparisons*. "Count session files, never compute a
  score" makes the memory *operations* reproducible across vendors — rarer and more
  rigorous than the norm.
- **Human governance / auditability.** Git-versioned, diff-able, hand-editable, human
  override — the "retention / inspection / deletion" layer enterprises say is missing.
- **Bet right on graphs.** Setting aside SurrealDB aged well: Mem0's 2026 retrospective
  reports a shift *away from* external graph stores toward "built-in entity linking,"
  calling it "a net improvement" for deployment simplicity.

## Gaps & risks

| # | Gap | Why it matters (2026) | Severity (this niche) | Status |
|---|---|---|---|---|
| 1 | **No supersession / fact-invalidation** | Zep models `valid_at`/`expired_at`/`invalid_at`; LongMemEval tests "knowledge updates"; Mem0 names "change as *replacement* not *evolution*" a top gap. Decay handles *unused*, not *false-when-reversed*. | **High — the one real gap** | ⬜ open → P1 |
| 2 | **Never-decay facts can go "confidently wrong"** | "High-relevance facts become confidently wrong when circumstances change" is a named open problem. `core` / Architectural Invariants never age out. | Medium-High | ⬜ open → P2 |
| 3 | **No write-time contradiction check** | SSGM "pre-consolidation validation" rejects updates contradicting core facts. Done at *migration* only, not normal sessions. | Medium | ⬜ open → P3 |
| 4 | **Lexical-only retrieval** | Production leans multi-signal (semantic + BM25 + entity + rerank). Tool has grep + read-whole-file. | Low (bounded by project scale) | ⬜ open → P5 |
| 5 | **No evaluation harness** | Even leaders admit "application-level evaluation is still a manual, bespoke process." | Low — but a cheap way to lead | ⬜ open → P4 |
| 6 | **Memory poisoning / provenance** | SSGM flags injected memory. Event-sourcing *gives* provenance (which session); it's just not surfaced. | Low (human-curated) | ⬜ open → P5 |

## Scorecard

| Dimension | 2026 best practice | agent-memory v3.0.0 | Status |
|---|---|---|---|
| Persistence substrate | File-based memory first-class (Anthropic memory tool / Memory Files) | markdown `memory/` | ✅ Aligned |
| Vendor neutrality | AGENTS.md standard (LF), 20+ tools | AGENTS.md hub + thin pointers | ✅ Aligned |
| Memory taxonomy | episodic / semantic / procedural | sessions / continuity / instructions | ✅ Aligned |
| Consolidation + forgetting | decay, archive, reflection | tiers + review ritual + archive | ✅ Aligned |
| Write path | "write path, not just retriever" | event-sourced sessions→review→continuity | ⭐ Ahead |
| Reversible reconciliation | SSGM: immutable ledger + mutable + replay | sessions ledger + continuity + full-rebuild | ⭐ Ahead |
| Determinism / reproducibility | benchmark-based comparison repro | deterministic integer operations | ⭐ Ahead |
| Human governance / audit | emerging need | git + markdown + override | ⭐ Ahead |
| Temporal / supersession | valid/expired/invalid, knowledge updates | — | ⬜ Gap (P1) |
| Truth maintenance | pre-consolidation validation | migration-only + core pinning | ◐ Partial (P3) |
| Stale pinned-fact handling | open problem | never-decay, no recheck | ⬜ Gap (P2) |
| Retrieval sophistication | multi-signal + rerank | lexical grep + read | ◐ Partial (P5) |
| Knowledge graph / entities | shift to built-in entity linking | flat markdown (graph deferred) | ◐ Partial / validated deferral |
| Evaluation | bespoke, unsolved industry-wide | none | ⬜ Gap (P4) |
| Privacy / access scoping | SSGM access-scoped retrieval | two-layer + target-scope boundary | ◐ Partial |

Legend: ✅ aligned · ⭐ ahead/distinctive · ◐ partial · ⬜ gap

## Backlog (prioritized) — all stay no-code / markdown

1. **P1 — Supersession semantics.** On a reversed decision, tombstone the old fact
   (`superseded-by: <id>`; new fact `supersedes: <id>`) and archive it flagged
   "superseded," not "faded." Markdown-native `expired_at`/`invalid_at`; closes gaps
   #1 and #2; buys the "knowledge updates" ability.
2. **P2 — Invalidation cadence for pinned facts.** `verify_invariants_every: N` in
   `decay-policy.md`; the review prompts a human to confirm `core` / Architectural
   Invariants are still true. Never-decay shouldn't mean never-checked.
3. **P3 — Write-time contradiction flag.** When a session adds a fact, scan for one it
   contradicts and raise an Open Thread (extend the migration-time check into `REVIEW.md`).
4. **P4 — Minimal eval.** `memory-smoke-test.md`: N questions a fresh agent should
   answer from memory alone. Manual, but ahead of most — app-level eval is unsolved.
5. **P5 — Provenance + retrieval-at-scale.** Surface each fact's originating session;
   lean on `archive/INDEX.md` + optional `sessions/INDEX.md` as the no-code mitigation
   if memory grows large. (Full vector/semantic retrieval is intentionally out of scope.)

## How to use this doc

- This is a **baseline**. Re-run the assessment (web research + this comparison) after
  meaningful iterations, or quarterly. Save the next one alongside this (dated file).
- When a backlog item ships, flip its scorecard/gap row ⬜ → ✅ and note the version.
- Watch the field for: supersession/temporal-KG becoming table stakes; whether the
  memory layer settles into "file system" vs "backend" (this tool bets file system —
  the same bet as Anthropic's memory tool).

## Sources (June 2026)

- State of AI Agent Memory 2026 — Mem0 — https://mem0.ai/blog/state-of-ai-agent-memory-2026
- Governing Evolving Memory in LLM Agents (SSGM) — arXiv — https://arxiv.org/html/2603.11768v1
- Effective context engineering for AI agents — Anthropic — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Memory tool — Claude API Docs — https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool
- Anthropic plans Claude memory update with new Memory Files — TestingCatalog — https://www.testingcatalog.com/anthropic-plans-claude-memory-update-with-new-memory-files/
- AGENTS.md Complete Guide 2026 — Codersera — https://codersera.com/blog/agents-md-complete-guide-2026/
- The State of AI Agent Memory in 2026 — DEV — https://dev.to/vektor_memory_43f51a32376/the-state-of-ai-agent-memory-in-2026-what-the-research-actually-shows-3aja
- The Consolidation Problem in Agent Memory — Hindsight/Vectorize — https://hindsight.vectorize.io/blog/2026/05/21/agent-memory-consolidation
- Knowledge and Memory Beyond RAG: Why 2026 Agents Need a Write Path — Medium — https://medium.com/@Micheal-Lanham/knowledge-and-memory-beyond-rag-why-2026-agents-need-a-write-path-not-just-a-retriever-ae2547b7ffe9
- AI Memory Benchmarks in 2026 — Mem0 — https://mem0.ai/blog/ai-memory-benchmarks-in-2026
