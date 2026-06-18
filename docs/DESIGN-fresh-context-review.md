# DESIGN — Fresh-Context Second Opinion (a critique gate over the VBDI loop)

> **Status:** **implemented v4.10.0** (2026-06-18) — the §10 forks were settled by the
> maintainer and built as a skill pair. Sibling to `DESIGN-evolving-memory.md`,
> `DESIGN-vbdi-lifecycle.md`, and `DESIGN-skills-layer.md`.
> **Source:** an independent brainstorming artifact — the *Agent Interchange Format (AIF)*
> draft (architecture paper + snapshot/critique specs, 2026-06). This document maps that
> idea onto the agent-memory foundation, **lightweight**, and deliberately keeps the tool's
> own vocabulary ("fresh-context second opinion") rather than importing a "format / protocol
> / standard" framing — the latter cuts against the lightweight, never-heavyweight Vision
> non-goals.
> **Decision locked (2026-06-18, maintainer):** fold into the **skills layer + VBDI**, not a
> standalone spec.

---

## 1. Why

A long AI session accumulates assumptions, partial conclusions, and self-trust: the model
that built a solution over-trusts its own trajectory. agent-memory already *bets on the
opposite* — its **smoke test** asks whether a **fresh** agent can orient from memory alone,
and **multi-agent continuity** has different vendors read each other's logs. What it has no
*deliberate ritual* for is the highest-value version of that: **at a milestone or a risk
point, hand a curated snapshot to an AI with clean memory and ask it to challenge the
work.** The reviewer's value is precisely that it did *not* live the session.

This is not theoretical here. In v4.8.0/v4.9.0 a fresh-context reviewer (GitHub Copilot CLI)
reviewed this repo's memory and **over-archived three still-referenced facts** because it
lacked the session context and miscounted. That episode is the design's anchor in **both**
directions: it proves fresh-context review surfaces things the in-session agent misses **and**
that the reviewer is not an authority — it can introduce its own errors. The remediation was
a *deterministic verifier* (`memory-lint`), not "trust the reviewer." This design carries
that lesson in its bones (§7, §9).

## 2. Principles (inherited — already ours)

- **No-code, markdown-only** — the snapshot and critique are markdown; the agent is the
  runtime. Any helper is an optional, agent-invoked script (`no-build-step-agent-run`).
- **Zero overhead by default** — nothing runs during ordinary interaction; the ritual fires
  only on explicit human invocation, exactly like `memory-lint`.
- **Human-gated** — the human decides when to invoke, acknowledges the trust boundary, and
  gates whether critique is applied. Critique is **advisory**, never auto-merged.
- **Vendor-neutral / never-pick-a-winner** — the reviewer may be any vendor or a clean
  session of the same one; the critique is one input, not a verdict.
- **Map, don't duplicate** — reuse `continuity.md` + session logs (state), VBDI gates
  (when), `memory-lint` + the target's build/tests (validation). Add the *minimum* that is
  genuinely missing.
- **Additive / non-destructive** — an optional skill pair; absent it, the tool is unchanged.

## 3. Observation — the net-new surface is tiny

Compare the AIF snapshot spec to what the tool already holds:

| Snapshot field (AIF) | Already in the tool? |
|---|---|
| Context / Objective / Actions / State Changes / Current State | ✅ `continuity.md` + recent session logs |
| Open Questions / Next Actions | ✅ Open Threads |
| Reasoning / Assumptions | ✅ Key Decisions + session logs |
| Verification (build / tests / structural) | ✅ target build/tests + `memory-lint` |
| **Milestone Check** (why complete, risk areas, confidence) | ◐ implicit in a VBDI gate — not structured |
| **Exchange Intent / trigger** (blocked \| risk \| milestone) | ❌ net-new framing |
| **Security advisory** before export to another system | ❌ **net-new** |
| **Critique artifact** (structured feedback shape) | ❌ net-new shape |

So ~70% of the snapshot is *derivable from existing memory*. **Net-new is three things:**
(1) the **security advisory** as a trust-boundary event, (2) the **fresh-context handoff
ritual** as a named, repeatable skill, (3) the **critique artifact shape**. Everything else
is reuse — the same "map, don't duplicate" discipline that kept VBDI to two new primitives.

> **Hard rule: do not introduce a parallel, hand-maintained state file.** The snapshot is
> *generated from* `continuity.md` + the last N session logs and is **transient scratch**
> (§5). A second source of truth for "current state" would be exactly the drift/bloat the
> lightweight-mode work (v4.7) fought.

## 4. The two modes (map onto VBDI altitudes)

```
Reactive:   stuck/uncertain/risky  → snapshot → fresh critique → scoped repair → validate
Milestone:  looks complete         → snapshot → clean-context gate → accept or revise
```

- **Reactive mode** = a critique when the in-session agent is stuck at **Design** or
  **Implementation**. On-demand; the human invokes it.
- **Milestone mode** = the **fresh-context flavor of a VBDI human gate** at an altitude
  transition (`DESIGN-vbdi-lifecycle.md` §7). The gate already exists ("AI proposes, human
  approves"); this adds an *optional* second-opinion step the human can run before approving.

Neither mode is automatic. Milestone mode is the more distinctive contribution — it is
valuable *even when the session looks successful*, which is exactly when the in-session
agent is least likely to challenge itself.

## 5. The design — a skill pair (delivery via the skills layer)

The skills layer is the natural vehicle: author once in `agent-skills/`, run on any vendor,
optional, not auto-installed (same posture as `memory-lint`).

### 5a. `second-opinion` — generate the snapshot

1. Compute trigger context (reactive vs. milestone) from the human's invocation.
2. **Show the security advisory and wait for explicit acknowledgment** (§6).
3. Distill a snapshot **from `continuity.md` + the last N session logs** — only the
   decision-relevant deltas, open questions, assumptions, risk areas, and (milestone) "why I
   believe this is complete / confidence before review." Not a memory dump.
4. Emit the snapshot as **transient scratch** the human carries to a fresh reviewer (a clean
   session, or another vendor). The reviewer needs no session history — that is the point.
   **Self-contained + an attach-manifest (v4.10.0 refinement, from a real-use consideration):**
   a repo-access reviewer (a CLI agent pointed at the repo) can read cited paths, but a
   **repo-less reviewer** (a web-based chat AI — the common case) sees only the snapshot. So the
   snapshot carries the decision-relevant substance inline (not bare path citations) and names,
   under *Attach to reviewer*, the exact files/excerpts the human must attach — so delivery
   works for any reviewer, not just one with filesystem access.

### 5b. `apply-critique` — consume the critique, bounded

1. Parse the returned critique (critical issues / gaps / execution guidance / risks /
   confidence).
2. Plan **≤ a small number** of focused, scoped actions — a bounded critique→repair loop,
   never an open autonomous loop.
3. Apply scoped changes; **run validation** — the target's build/tests and, for memory
   changes, `memory-lint`.
4. Summarize **applied vs. rejected** recommendations and **why** — the human gates the
   result. A genuine conflict surfaces as an Open Thread (`never-pick-a-winner`), not a
   silent overwrite.
5. A completed cycle is a **memory-relevant event** → it writes a normal session log +
   `## Memory References` (it stays *inside* the existing ritual, not beside it).

### 5c. The critique artifact

Markdown, transient scratch (not committed, not memory): summary, critical issues, gaps,
design feedback, execution guidance (numbered), validation strategy, risks, confidence.
(The AIF `CRITIQUE_SPEC.md` shape is a fine starting template — bundle it with the skill.)

## 6. The security advisory — the clearest net-new value

Packaging cognitive state for *another AI system* is a **trust-boundary event**, even when
the reviewer is internal. The tool today has `target-repo-scope-only` (don't read/write
outside the repo) and the no-home-path rule, but nothing that pauses before **exporting**
state outward. `second-opinion` shows an advisory and waits for acknowledgment before
generating a snapshot:

- no client secrets, credentials, or tokens;
- no PII;
- content appropriate to share beyond the immediate project perimeter.

Framing stays **assertive, not fear-based** (the AIF banner wording is a good base). This is
a no-code gate: the *agent shows the advisory and waits for "acknowledge"* — runtime behavior
expressed as a skill instruction, consistent with agent-as-runtime. It *strengthens*
`target-repo-scope-only` by extending it from "what the tool touches" to "what the human
exports."

## 7. The honest hard part — the reviewer is a hypothesis generator, not an authority

The v4.8/v4.9 episode is the cautionary tale: a fresh reviewer's confident output was
**wrong** because it lacked context and miscounted. So this design's load-bearing rule:

> **Fresh-context critique is advisory. It is gated by deterministic checks (`memory-lint`,
> build/tests) and a human decision before anything is applied.** `apply-critique` never
> merges on the critique's say-so alone.

This is not a weakness in the pitch — it is the strongest evidence the repo has. We ran this
pattern ad-hoc, learned exactly where it breaks, and already built the guardrail. The skill
makes the *good* part repeatable and bakes in the guardrail.

## 8. Alignment with the Architectural Invariants

| Invariant | How this honors it |
|---|---|
| `no-build-step-agent-run` | snapshot + critique are markdown; agent is the runtime; any helper is optional/agent-invoked |
| `target-repo-scope-only` | snapshot derived from the target's own memory; the advisory *strengthens* the perimeter on export |
| `never-pick-a-winner` | critique is advisory; conflicts → Open Threads; human gates application |
| `upgrades-additive` | optional skill pair; absent it, no behavior change; un-upgraded agent ignores it |

## 9. Scope / non-goals

- **Not an orchestration runtime / A2A transport.** No automatic agent-to-agent messaging;
  the **human carries the snapshot** (or runs a clean session). Low-friction,
  human-mediated, by design — the AIF paper's own stance.
- **Not a new state format.** The snapshot is *derived and transient*; `continuity.md` +
  session logs remain the single source of truth (§3 hard rule).
- **Not the AIF metrics / governance dashboard.** Defer (§10 of the AIF paper leans
  heavyweight) — markdown-recorded observations only, if anything.
- **Installed, but zero-overhead-by-default.** The built-in skills *are* installed into every
  enabled repo (they support the core workflow — `memory-lint` for the review ritual, the pair
  for milestone/risk review), but **nothing runs unless explicitly invoked** — installing a
  skill ≠ running it. `review-scratch/` is created on first use and gitignored.
- **Not a re-brand.** Land it in the tool's vocabulary; "AIF" stays an origin reference here.

## 10. Open questions — resolved (2026-06-18, maintainer)

1. **Naming** — ✅ a **skill pair**: `second-opinion` (snapshot) + `apply-critique` (return
   path). Tool-native vocabulary; "AIF" stays an origin reference.
2. **One skill vs. pair** — ✅ a **pair** (generate vs. apply are distinct triggers/moments;
   better usability than one flagged skill).
3. **Critique/snapshot location** — ✅ **gitignored `review-scratch/`**, with a README marking
   it personal and "sharing is a conscious decision." Never committed, never memory.
4. **Snapshot delivery** — ✅ a **file** in `review-scratch/`, ephemeral; the human carries it.
5. **Security advisory** — ✅ adopt the AIF banner (assertive, non-fear-based); the
   "acknowledge to proceed" gate is a no-code agent-instruction in the skill.
6. **ENABLE behavior** — ✅ **installed** into every enabled repo, via both ENABLE (Step 5i,
   all modes) and the UPGRADE 4.10.0 rung — `second-opinion` + `apply-critique` **and
   `memory-lint`** (the review ritual relies on it; this supersedes its v4.9.0 "tool-local"
   stance). *(Maintainer revised the initial opt-in choice: these are essential/important
   enough to ship by default. Installing a skill ≠ running it — still zero-overhead-by-default.)*
7. **Version rung** — ✅ additive **MINOR** → **v4.10.0**.

## 11. Test-drive (dogfood)

The natural first run reproduces the episode that motivated it — **structured this time.**
At the milestone where this feature's *own* implementation looks complete, invoke
`second-opinion`, carry the snapshot to a clean session (or a different vendor), and run the
critique→`apply-critique`→validate loop. Using fresh-context review to ship fresh-context
review — if that loop feels light and catches something real, that is the strongest
validation we can give it. (And it directly re-tests the v4.8/v4.9 failure mode under the
new guardrail.)

## 12. Integration points (as built — v4.10.0)

Touched, additively: `agent-skills/second-opinion/SKILL.md` +
`agent-skills/apply-critique/SKILL.md` (neutral skills with **inline** snapshot/critique
templates — no scripts), `ENABLE.md` Step 5i (built-in-skills **install**, all modes +
report/scope/verify), the `UPGRADE.md` 4.10.0 rung (installs the three built-ins into existing
repos), root & `templates/.gitignore` (`review-scratch/`), `.agent/schema.md` (`review-scratch/`
section), and the version ladder (`VERSION` → 4.10.0, `UPGRADE.md` rung + table, `README`,
`CHANGELOG`). `AGENTS.md` / `SKILLS.md` / `DECAY.md` / `REVIEW.md` **unchanged** — skills
auto-discover via the existing `AGENTS.md` "Skills" baseline, and the critique→repair loop
reuses the existing session ritual.
