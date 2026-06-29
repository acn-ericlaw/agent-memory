# The VBDI Loop

The [backward layer](evolving-memory.md) keeps memory faithful to what *happened*. The
**VBDI loop** is its forward complement — it keeps delivery faithful to what was *intended*:

```mermaid
flowchart LR
  CS[Current State] --> V[Vision]
  V --> B[Blueprint]
  B --> D[Design]
  D --> I[Implementation]
  I --> F[Feedback]
  F -.-> CS
```

## Only two primitives are new

Most of the loop already exists in the memory layer, so VBDI integrates by **mapping**, not
rebuilding. Only **Vision** and **Blueprint** are genuinely new:

| Primitive | Realized by |
|---|---|
| **Current State** | `continuity.md` (read at session start) |
| **Vision** *(new)* | `memory/vision.md` — the north star (`core`, invariant-verified) |
| **Blueprint** *(new)* | typed `(blueprint)` Open Threads — the Vision ↔ reality gaps |
| **Design** | Key Decisions + Architectural Invariants (optionally an [ADR log](../reference/protocol-files.md)) |
| **Implementation** | code / commits, traced in session logs |
| **Feedback** | the review ritual + decay + supersession |

## Why it stays lightweight

- **The trace is the determinism.** Implementation → Design → Blueprint (`serves: <gap>`) →
  Vision (`serves: <vision-id>`), linked by stable `id`s. A missing or broken link **is**
  drift — and it is grep-detectable. The trace and the gates are deterministic; the
  *content* (the vision, the design ideas) is the open human–AI partnership. No scoring.
- **Human gates.** Each altitude transition (confirming the Vision, opening/closing a gap)
  is an Open Thread the human checks off — the agent proposes, the human approves. Not a
  phase review.
- **Bootstrap, never fabricate.** Enable and upgrade create a **DRAFT** Vision with only the
  safe current-state context inferred — the *target* is left for the human, gated by a
  `(vision-bootstrap)` thread. The Vision is the human's to set, like a user preference.
- **Process-neutral.** The loop is the lightweight default; it neither requires nor forbids a
  heavier process. A target's owner may layer SDLC / scrum on top — that is their call — but
  ceremony and any scoring stay in the target's own space, never in `memory/`.

!!! quote ""
    Memory is the deterministic substrate; the loop is the lightweight control layer.
    Together they yield **predictable innovation with human partnership**.

For the full design rationale, see the [VBDI Lifecycle design note](../DESIGN-vbdi-lifecycle.md)
and the [Agent Cognitive Framework](../agent-cognitive-framework.md).
