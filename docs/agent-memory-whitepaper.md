# agent-memory: A Lightweight, Vendor-Neutral Memory + Cognitive-Loop System for Predictable AI–Human Delivery

## Deterministic memory as a substrate; a lightweight cognitive loop as the control layer

**Version:** 1.1 (describes agent-memory **v4.1.1**)
**Status:** Draft for peer / leadership review
**Date:** June 16, 2026

---

## Executive Summary

AI agents are moving from single-turn prompting to persistent, tool-using, memory-driven
runtimes. Two problems dominate production use:

1. **Memory drift and context loss** — context is re-explained every session, decisions
   are silently forgotten or contradicted, and different AI vendors can't share a common
   understanding of a project.
2. **The gap between intent and delivery** — agents can be creative, but keeping what is
   *built* faithful to what was *intended* is largely unmanaged.

**agent-memory** addresses both with a **no-code, markdown-only** system layered over a
single, git-committed `memory/` directory that any AI vendor can read and write. It has
two complementary layers:

- **Backward layer — Evolving Memory.** An event-sourced ledger (immutable session logs)
  is projected into a live `continuity.md`, with **deterministic** decay, **supersession**
  (facts that become false, not just unused), periodic **invariant re-verification**,
  **write-time contradiction** checks, and **provenance**. It answers *"where are we, and
  why?"*
- **Forward layer — the VBDI cognitive loop.** *Current State → Vision → Blueprint →
  Design → Implementation → Feedback*, with an **enforceable intent trace** and a **human
  gate** at every altitude change. It answers *"where are we going, and is delivery
  faithful to intent?"*

The system is **vendor-neutral** (one shared memory; any agent — Claude, Gemini, Cursor,
…), **deterministic** (no floating-point scoring — every agent reaches the same result by
counting, never estimating), **lightweight** (you "point it at a repo"; there is no
ceremony), and it **migrates** existing vendor AI files into the unified format.

The shared, committed layer carries three things across vendors: **memory**, **steering**,
and — as of **v4.1.0** — **portable skills** (reusable capabilities authored once and run
by any agent; see §5).

Its central claim: pairing a **deterministic memory substrate** with a **lightweight
cognitive loop** yields **predictable innovation with human partnership** — bold ideas,
faithful delivery, a human in the loop at every altitude. This was demonstrated on a real
Node.js→Rust rewrite that delivered with **no drift**, and the tool was built **using its
own loop** (dogfooded).

---

## 1. Motivation

Most LLM applications begin stateless: each interaction restarts from scratch, and any
persistent understanding of the project must be manually reintroduced. Recent industry and
academic work converges on a view that the production bottleneck is no longer the model
alone but the **surrounding architecture** — memory, planning coherence, and adaptive
execution — and that memory is best understood as a **write–manage–read loop** coupled to
action, not a passive context buffer.

Two consequences follow that existing tools handle poorly:

- **Vendor silos.** Each AI tool keeps its own steering files and history (`CLAUDE.md`,
  `.cursorrules`, Aider chat logs, …). A team using more than one vendor — or migrating
  between them — has no shared, durable project memory.
- **Intent drift.** Even with memory, nothing ties a delivered change back to the decision,
  the plan, and the goal it was meant to serve. "Confidently wrong" facts and reversed
  decisions accumulate silently.

agent-memory targets both: a **shared, vendor-neutral memory** that *evolves* faithfully,
and a **forward cognitive loop** that makes intent traceable and drift detectable — without
imposing a heavyweight process.

---

## 2. What agent-memory Is

A **no-code, markdown-only** system with three jobs in one repository:

1. **A shared memory system** — a `memory/` layer that persists project context across
   sessions and across vendors. It is committed to git and travels with the code.
2. **An AI-enablement tool** — point it at any repo and it generates a tailored memory
   system there ("AI enable this repo").
3. **A migration tool** — when the target already has vendor AI files, it folds them into
   the unified format (originals preserved under `legacy/`, never deleted).

As of **v4.1.0**, the shared layer also carries **portable skills** (§5) — reusable
capabilities beside memory and steering.

There is **no build, lint, or test step**: the markdown files *are* the product, and the
"runtime" is an AI agent reading and acting on them. Two memory layers coexist by design —
the repo's shared `memory/` (team, committed) and each contributor's personal runtime store
(e.g. `~/.claude/`, individual). The tool only ever touches the shared layer.

---

## 3. The Backward Layer — Evolving Memory

Memory here is **event-sourced**, not a mutable blob:

- **The ledger.** Each work segment writes an immutable session log containing a
  `## Memory References` section — the *events* (which facts were referenced, created,
  reactivated, superseded). Session logs are never edited.
- **The projection.** `continuity.md` is the *derived* live state: facts, each carrying a
  metadata footer (`id`, `created`, `last_used`, `uses`, `tier`, optional `origin`). The
  projection is recomputable from the ledger at any time (full replay).
- **Deterministic decay.** A periodic **review** recomputes usage by *counting session
  files* — never a floating-point score — so any agent (Claude, Gemini, …) reaches the
  **same** result. Facts fade through tiers (`working → active → archive-candidate →
  archived`); nothing is ever deleted (archived, with a greppable index).

On top of that substrate sit four capabilities that make the memory *trustworthy*:

- **Supersession (truth maintenance).** When a decision is reversed or a fact becomes
  false, it is marked `superseded` (terminal) with a `superseded-by` link and archived
  flagged "superseded," not "faded." Memory can represent *change*, not just disuse.
- **Invariant re-verification.** Never-decay facts (`core` / architectural invariants) are
  periodically surfaced for a human to re-confirm — because "never-decay" must not mean
  "never-checked" (the "confidently wrong" failure mode).
- **Write-time contradiction check.** When a fact is added, the agent scans for one it
  contradicts → supersede it, or raise an Open Thread. The system *never picks a winner*.
- **Provenance.** Each fact can carry an `origin` pointer to its source session — one-hop
  traceability and a cheap defense against memory poisoning.

Retrieval is deliberately **lexical + indexed** (grep + a greppable archive index +
provenance pointers), bounded by project scale — *not* a vector/index server. That keeps
the layer no-code, human-auditable, and replayable.

---

## 4. The Forward Layer — the VBDI Cognitive Loop

The backward layer keeps memory faithful to what *happened*. The **VBDI loop** is its
forward complement — it keeps delivery faithful to what was *intended*:

```text
Current State → Vision → Blueprint → Design → Implementation → Feedback → (repeat)
```

This integrates a generalized **Agent Cognitive Framework** (a lightweight, loop-based
scaffold of six primitives) as the control layer above the memory substrate. The key
integration insight is that **most of the loop already exists in the memory layer** — so
only two primitives are genuinely new:

| Primitive | Realized by |
|---|---|
| **Current State** | `continuity.md` (read at session start) |
| **Vision** *(new)* | `memory/vision.md` — the north star (`core`, invariant-verified) |
| **Blueprint** *(new)* | typed `(blueprint)` Open Threads — the Vision↔reality gaps |
| **Design** | Key Decisions + Architectural Invariants |
| **Implementation** | code / commits, traced in session logs |
| **Feedback** | the review ritual + decay + supersession |

Four properties make the loop work without becoming heavyweight:

- **The trace is the determinism.** Implementation → Design → Blueprint (`serves: <gap>`)
  → Vision (`serves: <vision-id>`), linked by stable `id`s. A missing or broken link *is*
  drift — and it is grep-detectable. The trace and the gates are deterministic; the
  *content* (the vision, the design ideas) is the open human–AI partnership. No scoring.
- **Human gates.** Each altitude transition (confirming the Vision, opening/closing a gap)
  is an Open Thread the human checks off — the agent proposes, the human approves. Not a
  phase review.
- **Bootstrap, never fabricate.** Enable and upgrade create a **DRAFT** Vision with only
  the safe current-state context inferred — the *target* is left for the human, gated by a
  `(vision-bootstrap)` thread. The Vision is the human's to set, like a user preference.
- **Process-neutral.** The loop is the lightweight default; it neither requires nor forbids
  a heavier process. A target's owner may layer SDLC / scrum on top — that is their call —
  but ceremony and any scoring stay in the target's own space, never in `memory/`.

---

## 5. The Capability Layer — Cross-Vendor Skills

Memory and steering were already shared across vendors. **v4.1.0** adds the third shared
leg — **skills**: reusable *capabilities* (a `name`, a *when-to-use* `description`, a
procedure, optionally helper scripts) authored once and usable by any agent.

- **Neutral source of truth.** A committed `agent-skills/<name>/SKILL.md` — vendor-neutral
  markdown — is the single definition; it travels with the repo, like `memory/`.
- **Universal runtime.** The `AGENTS.md` "Skills" section is the baseline: when a task
  matches a skill's `description`, the agent reads and follows that `SKILL.md`. Because the
  agent *is* the runtime, this works on **any** vendor with no engine.
- **Thin per-vendor adapters.** For runtimes with a native skill/command system, the tool
  regenerates *pointers* — `.claude/skills/`, `.gemini/commands/`, `.cursor/rules/` — for
  native auto-trigger. Adapters are gitignored and regenerated (never copies), so the
  neutral skill never drifts.
- **Migration promotes, never flattens.** A vendor's existing skills (e.g.
  `.claude/skills/`) are *promoted* into `agent-skills/` (originals preserved under
  `legacy/`), not folded into steering — skills are procedures, not rules.

The layer honors the same invariants as the rest of the tool — vendor-neutral,
never-pick-a-winner, additive/non-destructive — and it refined the tool's own "no-code"
invariant into **"no build step; agent-run"**: the *tool* runs no code, while a skill may
carry optional, **agent-invoked** helper scripts.

---

## 6. Design Principles

- **No-code, markdown-only.** The files are the product; the agent is the runtime.
- **Vendor-neutral.** One shared memory; thin per-vendor bootstrap pointers route every
  agent to a single hub (`AGENTS.md`). No lock-in.
- **Deterministic — no floating-point.** Every decision reduces to counting or comparing
  integers, so results are reproducible across agents and runs.
- **Reversible reconciliation.** Immutable ledger + mutable projection + replay — the
  governance/audit story is just git + markdown.
- **Lightweight; guide thinking, don't prescribe execution.** Loop over process; simplicity
  over completeness.
- **Never pick a winner; never fabricate intent.** Contradictions and the Vision are
  surfaced for a human, not resolved silently.
- **Additive, non-destructive upgrades.** Versioned (`VERSION` + per-repo stamp); a repo on
  an older version upgrades in place via an idempotent ladder.

---

## 7. How It Works in Practice

- **Enable a repo.** "AI enable this repo `/path`." The tool detects any existing AI
  footprint and chooses a mode: **Fresh** (generate from analysis), **Already-Ours**
  (idempotent; upgrade in place if on an older version), or **Migrate** (fold vendor files
  in, preserving originals). It generates `memory/`, the bootstrap pointers, and a DRAFT
  Vision + gate.
- **A session.** The agent reads Current State (`continuity.md`) + the Vision, does the
  work tying it to a Blueprint gap and the Design it realizes, writes a session log with
  `## Memory References`, and updates `continuity.md`.
- **A review.** On cadence (or on demand), the review replays the ledger, re-tiers facts,
  archives faded ones, applies supersessions, prompts invariant re-verification, and scans
  for contradictions/altitude drift.
- **A memory smoke test.** A short, manual eval — questions a *fresh* agent should answer
  from memory alone. A failure is a memory *gap* to fill, not a test to soften.

---

## 8. Evidence & Validation

- **A real rewrite, no drift.** A Node.js→Rust rewrite of a TCP-proxy CLI was delivered
  against recorded intent (invariants, decisions, and their *why* were pinned and
  traceable) with **deterministic, faithful** results and no drift — the proof point the
  whole design rests on.
- **Dogfooding.** The tool builds itself: it carries its own `memory/`, its own Vision and
  Blueprint, and the VBDI layer was designed and shipped **using the VBDI loop** ("using
  the thing to design the thing").
- **Closing the known gaps.** An industry-alignment self-assessment identified the real
  gaps (supersession, invariant re-checking, write-time contradiction, evaluation,
  provenance); each shipped as an additive, versioned release.
- **Real-world cross-vendor validation.** The skills layer (v4.1.0–4.1.1) was exercised
  end-to-end by an in-place upgrade of a large, pre-existing project — promoting that
  project's vendor skills into the shared `agent-skills/` layer and regenerating the
  per-vendor adapters — confirming the migration path on a real codebase, not just a fixture.

---

## 9. Relationship to the Literature

agent-memory is not a new agent paradigm; it is a **concrete, file-first, deterministic
realization** of patterns the field already endorses:

- **Simple, composable structures over heavy frameworks** (Anthropic's agent guidance) —
  realized as markdown + a small set of primitives.
- **Memory as a write–manage–read loop** (autonomous-agent memory surveys) — realized as
  sessions (write) → review (manage) → continuity (read), with replay.
- **Interleaved reasoning and action** (ReAct) — the loop's Design/Implementation/Feedback
  are not disjoint phases.
- **Reversible reconciliation and pre-consolidation validation** (recent memory-systems
  work) — realized as the immutable ledger + the write-time contradiction check.

Its differentiators relative to mainstream memory stacks: **determinism (no scoring),
truth-maintenance (supersession + contradiction + invariant re-verification),
vendor-neutral shared memory, no-code/markdown, git-native governance, and the forward VBDI
loop with human gates.**

---

## 10. What Makes It Different

| Dimension | Common practice | agent-memory |
|---|---|---|
| Persistence | per-vendor files / vector store | one shared, git-committed markdown layer |
| Forgetting | similarity scores, TTLs | deterministic tiering by counting session files |
| Truth maintenance | overwrite / let stale persist | supersession + contradiction check + invariant re-verify |
| Retrieval | semantic / vector | lexical + indexed + provenance, by design |
| Intent → delivery | unmanaged | VBDI altitude trace, grep-detectable drift |
| Governance | opaque | git history + markdown + human gates |
| Vendor coupling | locked to one tool | neutral; thin pointers to one hub |
| Capabilities / skills | per-vendor skill files, not shared | neutral `agent-skills/` + regenerated per-vendor adapters; authored once, any agent |
| Process weight | often heavy | lightweight default; SDLC is the target's opt-in |

---

## 11. Roadmap

Tracked as Blueprint gaps against the Vision:

- **Greenfield flow** — start from a Vision with no code yet (the substrate now exists).
- **Multi-user hardening** — strengthen conventions for simultaneous contributors on one
  enabled repo.
- **Optional SDLC overlay** — a scrum-inspired profile a target *owner* can opt into
  (`(sprint)` tagging + sprint-boundary review, no points/ceremony). Optional, never core.

---

## 12. Conclusion

As agents become persistent, memory-driven systems, they need scaffolds that are both
operationally useful and light enough to embed in real repositories. agent-memory pairs a
**deterministic, event-sourced memory substrate** (faithful to what happened) with a
**lightweight cognitive loop** (faithful to what was intended), under a vendor-neutral,
no-code, human-gated design.

> Memory is the deterministic substrate; the loop is the lightweight control layer.
> Together they turn memory-aware agent work into **predictable innovation with human
> partnership** — bold ideas, faithful delivery, the human in the loop at every altitude.

---

## References

1. Anthropic. *Building Effective Agents*. 2024. https://www.anthropic.com/research/building-effective-agents
2. Du, Pengfei. *Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers*. 2026. https://arxiv.org/html/2603.07670v1
3. Hu, Yuyang et al. *Memory in the Age of AI Agents*. 2025/2026. https://arxiv.org/abs/2512.13564
4. Yao, Shunyu et al. *ReAct: Synergizing Reasoning and Acting in Language Models*. 2022/2023. https://arxiv.org/abs/2210.03629
5. Mem0 Engineering. *State of AI Agent Memory 2026: Benchmarks, Architectures & Production Gaps*. 2026. https://mem0.ai/blog/state-of-ai-agent-memory-2026
6. *Agent Cognitive Framework for Memory-Driven AI Systems* (the framework integrated here as the forward layer). 2026. `docs/agent-cognitive-framework.md`.
7. Internal design docs: `docs/DESIGN-evolving-memory.md` (backward layer), `docs/DESIGN-vbdi-lifecycle.md` (forward layer), `docs/assessments/2026-06-13-industry-alignment.md`.
