# DESIGN — VBDI Cognitive Lifecycle (forward layer over the memory substrate)

> **Status:** design, under review. Sibling to `DESIGN-evolving-memory.md`.
> **Source:** a generalized cognitive framework drafted independently of this tool
> (`docs/agent-cognitive-framework.md`); this document maps it onto the agent-memory
> foundation, **lightweight**. Terminology decision locked (2026-06-14): the framework's
> "Mission" (= current reality) is renamed **Current State** to avoid the usual
> "mission = purpose" collision.

---

## 1. Why

agent-memory is **backward-anchored**: `continuity.md` (current reality) and the
REVIEW / decay / supersession machinery (learning) are strong — it answers *"where are
we, and why?"* It has **no forward anchor**: no explicit **Vision** (target) or
**Blueprint** (the gap to it). So Open Threads are ad hoc, and drift is only ever
checked fact-vs-fact, never against an *intent*.

The mission — **predictable innovation with human partnership** — needs that forward
layer: a deterministic *process* and an enforceable *trace* from intent to delivery,
human-gated at each altitude. The Node→Rust rewrite proved the backward half (no drift,
faithful delivery); VBDI generalizes that guarantee to **creation**.

## 2. Principles (inherited — already ours)

The source framework's principles and this tool's are the same: **guide thinking, not
prescribe execution; loop over process; simplicity over completeness; map, don't
duplicate; no new ceremony; determinism lives in the trace, not the ideas; structure
enables creativity.** Over-engineering — too many layers, premature abstraction, heavy
process — is the named anti-pattern on both sides. This design must not violate it.

## 3. The loop

```
Current State → Vision → Blueprint → Design → Implementation → Feedback → (repeat)
```

Non-linear — a loop, not a waterfall. **Greenfield → brownfield:** each delivered
increment becomes the next Current State. Crucially, **the tool already runs this loop**
session-to-session — Before-session reads Current State; the work yields Design /
Implementation; After-session + REVIEW is Feedback. VBDI *names* the loop and adds the
two missing forward steps.

## 4. Mapping to the foundation — map, don't duplicate

| Primitive | Question | In the tool today | Maps to / how |
|---|---|---|---|
| **Current State** | What exists now? | ✅ strong | `continuity.md`, read at session start |
| **Vision** | What should exist? | ❌ **gap** | *new* — the north-star artifact (§5) |
| **Blueprint** | What's missing? | ◐ partial | Open Threads — formalized as *Vision-derived* gaps (§5) |
| **Design** | How should it work? | ✅ strong | Key Decisions + Architectural Invariants + `docs/DESIGN-*.md` (+ an optional human-facing `docs/arch-decisions/ADR.md` decision log) |
| **Implementation** | What next? | ✅ external | code/commits; memory holds the *trace* (sessions, `origin`) |
| **Feedback** | What changed/learned? | ✅ strong | REVIEW ritual + session ledger + decay/supersession |
| **Memory loop** (Capture→Store→Retrieve→Reflect→Update) | — | ✅ *is the tool* | sessions → grep+`origin` → REVIEW → continuity/decay |

**Net-new is exactly two primitives: Vision and Blueprint.** Everything else is reuse.

## 5. The two new artifacts (lightweight)

### Vision — the north star  *(proposed: `memory/vision.md`)*
*What* should exist, *for whom*, success criteria, and explicit **non-goals**. One per
repo (per-epic nesting deferred). Short. Treated as `core` (never decays) **but subject
to invariant-verification** — a Vision can go stale, so it is re-confirmed on the P2
cadence. Carries a kebab `id`.

### Blueprint — the gap (Vision − Current State)  *(no new file)*
The required capabilities / gaps, expressed as **typed Open Threads**:
`- [ ] (blueprint) <gap> → serves: <vision-id>`. Reuses the Open-Thread machinery
(unchecked = pinned, never decays); a Blueprint item closes when its gap is delivered.
Keeping it a *flavor of Open Thread* is what keeps this light — no new structure.

### Trace — the determinism
Up-the-altitude linkage via the **existing `id` mechanism**:
Implementation (commit/session) → Design (decision id) → Blueprint (gap id) → Vision (id).
A missing or broken link **is** drift, and it's grep-detectable. This is the enforceable
trace — the whole point.

## 6. How it plugs into the existing machinery (the enhancement)

- **Decay:** Vision = `core`; Blueprint gaps = unchecked Open Threads (pinned). No rule change.
- **Contradiction check (§10):** extend from fact-vs-fact to **altitude drift** —
  Implementation vs Design, Design vs Blueprint, Blueprint vs Vision. Surface as a thread.
- **Supersession (§9):** when the Vision or a Blueprint gap changes, supersede the
  dependent Designs/gaps — intent changes ripple down, with history preserved.
- **Invariant verification (P2):** the re-confirm cadence now also covers the **Vision**
  (never-true ≠ never-checked).
- **Smoke test (P4):** add *"does the Implementation satisfy its Blueprint/Design
  acceptance criteria?"*
- **Provenance (P5):** `origin` already traces a fact to its session; the altitude links
  extend that **upward, to intent**.

**The enhancement to memory:** it becomes **goal-aware**. Decay, review, and drift now
have a *teleological* reference — *does this serve the Vision?* — not only a usage /
consistency one. One anchor, reused everywhere; that is the leverage.

## 7. Human gates (partnership)

Each altitude transition is a **human gate**: the AI proposes, the human approves —
implemented with the existing "surface as an Open Thread / never pick a winner / prompt"
pattern, **not** a phase review. Lightweight: a thread to check off, not a meeting.

## 8. Determinism

The **trace and gates** are deterministic (id linkage, grep-checkable, human-approved).
The **content** — the vision, the design ideas — is the open human–AI creative
partnership. No scoring, no float; same discipline as the rest of the tool.

## 9. Hard parts (honest)

1. Drift across altitudes is subtler than fact-vs-fact — the link structure must be real,
   or "this doesn't serve the vision" becomes hand-waving.
2. Gates must stay Open-Thread-light — never Jira.
3. The trace must be **enforceable** (grep / review), not merely documented.
4. Don't bloat: map don't duplicate; only Vision (a file) + Blueprint (a typed thread) are new.
5. Implementation lives in the target's **code**, not `memory/` — memory holds the trace,
   not the artifact.

## 10. What changes (implementation plan)

- **New:** `templates/memory/vision.md` (+ the tool's own `memory/vision.md`). Blueprint =
  a typed Open Thread (no new file).
- **Wire the loop in:** `AGENTS.md` (Before/During/After name the loop + the gates),
  `DECAY.md` / `REVIEW.md` (the §9/§10/P2/P4 extensions in §6), `.agent/schema.md`
  (`vision.md` + the altitude-link convention), `ENABLE.md` (seed a Vision *stub* at
  enable — open question), and the smoke test.
- **Versioned** with an UPGRADE rung. Strictly **additive** (a repo with no Vision works
  unchanged), so by the semver rule it is a **MINOR** — but as a whole new cognitive
  layer it is a milestone. **3.8.0 vs 4.0.0 is an open question** (§11).

## 11. Open questions (for review)

1. **Vision location** — `memory/vision.md` (proposed; it's live project state) vs a root
   `VISION.md` vs a section of `continuity.md`?
2. **Blueprint shape** — typed Open Thread (proposed, lightest) vs its own section/file?
3. **ENABLE behavior** — seed a Vision *stub* at enable (prompting the team to fill it),
   or leave Vision creation entirely to the team?
4. **Granularity** — one Vision per repo now, per-epic nesting deferred — agree?
5. **Version** — 3.8.0 (additive minor) or 4.0.0 (mark the new-layer milestone)?
6. **Gate weight** — a one-line thread per transition, or a short approval note?

## 12. Test-drive

The first real loop: write **this tool's own Vision** (`memory/vision.md`) with the shape
above, derive the **Blueprint** (Current State `v3.7.0` → Vision), and confirm the loop
feels light. Using VBDI to build VBDI — if the bootstrap is clean, that is the strongest
validation we can give it.

## 13. Process neutrality — surviving an SDLC overlay

The tool stays lightweight by design (no ceremony — a Vision non-goal). But the `memory/`
layer is *enabled into a target repo*, and that target's owner is free to run heavier
process — automated AI scrum, sprints, the works — if they want. The memory design must
**survive that edge case** without breaking and without being dragged heavy. The rules
(also in `DECAY.md` §12):

- **Neither require nor forbid.** VBDI is the lean default; SDLC is an **opt-in overlay in
  the target**, never imposed at enable and never in the tool's core — same pattern as
  `docs/optional-ritual-hook.md`. The lightweight non-goal constrains the *tool*, not the
  target's freedom to choose its own process weight.
- **Ceremony + scoring stay out of `memory/`.** Velocity, story points, estimates, sprint
  ritual → the target's own tracker/docs. `memory/` stays determinism-pure (no float) —
  that's what keeps the substrate vendor-neutral and replayable. Crossing that line is the
  failure mode to guard against.
- **Reuse, don't reinvent.** Scrum maps onto the existing primitives: backlog = Blueprint;
  sprint = a bounded subset of gaps (a `(sprint)` tag); Definition of Done = smoke test +
  altitude trace; retro = the review ritual; PO/SM = the human gates. Extra tags coexist
  with the rules (an unchecked `(blueprint) (sprint)` thread is still a pinned Open Thread).
- **Cadence-agnostic loop.** A sprint boundary is just "run a review" (on demand). The loop
  rides whatever rhythm the team uses; the decay windows count sessions, not sprints.

Net: the tool is the *lightweight memory substrate*; the target owner decides the process
weight on top. The design bends to that — the core never gets heavy, and the substrate
never absorbs ceremony.

> A dedicated **optional** scrum profile for targets (a `(sprint)` convention +
> sprint-boundary review, no points/ceremony) is a possible future add-on — tracked as the
> `bp-sdlc-overlay` Blueprint gap. Not core; only if a real target wants it.
