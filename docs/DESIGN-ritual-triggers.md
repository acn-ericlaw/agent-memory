# DESIGN — Reliable, Vendor-Neutral Ritual Triggers

> **Status:** **IMPLEMENTED v4.19.0** (2026-06-24) — maintainer endorsed git-hooks + CI and added the
> zero-manual / untrained-user adoption constraint; built (`.githooks/post-commit` + CI workflow,
> agent-activated, advisory) and dogfooded. The §6 forks were resolved as recommended (auto-stub + nudge,
> advisory-by-default with an opt-in `AGENT_MEMORY_STRICT` gate, no-manual activation).
> **+ first-run init v4.20.0:** `.githooks/init.sh` (one idempotent command — regenerate adapters +
> activate the hook) + an `AGENTS.md` **self-init** note. Closes the fresh-clone gap a Copilot dogfood
> exposed: a clone has gitignored adapters absent + the hook unactivated, and the memory bootstrap
> self-initializes but the adapters/hook did not. Now the agent self-inits on its first session (or one
> human command does it); CI remains the zero-config floor regardless.
> **+ 4.20.1:** self-init also folded into **`copilot-instructions.md`** — a fresh-clone dogfood showed
> Claude self-inits (it acts on `AGENTS.md`) but Copilot CLI did **not** (its `start` front-loads
> `copilot-instructions.md` + summarizes), so the first-run init now **leads** that file too.
> Sibling to `DESIGN-evolving-memory.md`, `DESIGN-vbdi-lifecycle.md`, `DESIGN-skills-layer.md`, and
> `DESIGN-fresh-context-review.md`. Realizes the `(blueprint)` gap **`bp-ritual-triggers`** →
> serves `vision-agent-memory`.
> **Source:** real client-team complaints (2026-06): the after-session ritual is **not followed
> through even with Claude** (long/pressured sessions just end), and a **Copilot-only team has no
> triggers at all** for any ritual (end-of-session log, review, sync skill adapters). Surfaced
> alongside the Copilot CLI dogfood that also proved the trigger layer doesn't travel (see below).

---

## 1. Problem

The three rituals — **end-of-session log**, **memory review** (decay reconciliation), and **sync skill
adapters** — are *conventions the agent must self-trigger*. That is structurally unreliable:

- **Even with Claude**, nothing forces the close-of-session moment; a busy session just ends.
- **Copilot-only teams have no trigger at all.** And the current hook story is opt-in, **per-vendor**,
  **not installed**, and — proven dogfooding `~/sandbox/simple-proxy` — the **opt-in recipe doesn't even
  travel into the target** (`docs/optional-ritual-hook.md` is tool-only; a target's `AGENTS.md` only
  says "wire a hook" with no recipe). So "wire a hook" is not self-serve, and it differs per vendor.

**The weak point is the trigger layer, not the ritual.** Reliability can't come from more documentation
of a convention; it needs a trigger that actually fires, uniformly, across vendors.

## 2. Constraints (the Vision — non-negotiable)

Lightweight · no-code · **agent-is-the-runtime** · vendor-neutral. The reconciliation that makes this
design *consistent* with the Vision rather than a violation of it:

> **"No-code" means the *tool* runs no code; the markdown is the product.** A git hook, a CI check, or
> a bundled script is run by **the user's own environment at their opt-in** — the **same category** as
> the already-shipped `memory-lint` and `sync-adapters` scripts (`no-build-step-agent-run`: an optional
> helper the agent/vendor/CI invokes; the tool itself runs nothing, hosts no daemon).

So this design does **not** abandon the Vision. It **flips the trigger layer** from *"opt-in afterthought
that doesn't travel"* → *"first-class, vendor-neutral, installed (or one-command-activated) reinforcement."*

> **Adoption constraint (2026-06-24, maintainer): zero-manual-step.** The protocol is gaining traction, so
> enabled repos increasingly land with **untrained users**. *Any manual operation or per-user setup is a
> barrier to adoption.* Triggers must require **no manual user step** in the common path: the
> **agent-runtime** performs activation, and **CI** (server-side, zero-config) is the reliability floor.
> This raises the bar on §6.4 — enable **installs and activates**, it does not merely *offer*.

## 3. Key insight — git + CI is the only vendor-neutral trigger substrate

Vendor hooks (Claude `Stop`, Copilot `sessionEnd`, Kiro hooks) are **all different**, some modes have
**none** (Copilot Ask/Plan are read-only — correctly no-log anyway), and they **don't travel**. But
**everyone commits, and everyone runs CI**, regardless of which agent did the work. So the reliable,
uniform reinforcement layer is **git hooks + CI**; vendor hooks drop to an *optional real-time nicety*.

A committed **`.githooks/`** dir activated by a one-line `git config core.hooksPath .githooks` gives a
**vendor-neutral, travels-with-the-repo** trigger — exactly what today's model lacks.

## 4. The capture/judgment split (the crux for the session log)

The session log felt un-automatable because two things were conflated:

- **Thoughtful summary + `## Memory References`** = irreducible **agent judgment**. No script writes good
  memory. *Stays the agent's job.*
- **The log's *existence* and *triggering*** = **deterministic**. A commit-time hook can **auto-write a
  stub** so the ledger never has a gap, and the agent/review **enriches** it.

This mirrors `memory-lint`: **deterministic capture + the agent judges meaning.** It is the move that lets
"reliable" and "agent-is-the-runtime" coexist.

**Stub shape** (auto-written when a commit changes tracked files and no fresh log exists):

```markdown
# Session (<persist-time UTC stamp>)
**Agent:** (auto-stub — enrich on next session)
**Lightweight:** auto-captured at commit; summary pending.

<git diff --stat>

## Memory References
(none — auto-stub; the next session/review enriches or downgrades to a lite log)
```

`memory-lint` learns to recognize an auto-stub (a marker line) so it is **not** counted as a
reference-bearing session and is flagged for enrichment — never silently treated as "done."

## 5. The layered model

| Layer | Mechanism | Reliability |
|---|---|---|
| **0 — Primary (unchanged)** | Agent-runtime ritual; strengthen the **"a task is not *done* until the log exists"** framing in `AGENTS.md` (definition-of-done, not a trailing chore). | Best-effort (agent judgment) |
| **1 — Vendor-neutral net (NEW)** | **(a) git hook** (committed `.githooks/` + `core.hooksPath`, one-command activate): on a commit touching tracked files → **auto-stub the session log** (or loud nudge), **run `memory-lint`** to warn if **review is due** (it already computes `sessions_since_last_review`), and **run `sync-adapters`**. **(b) CI check**: a workflow that runs `memory-lint` and **warns** (configurable: fail) when a change lacks a session log — *"checked, not convention."* | Reliable, uniform across vendors |
| **2 — Optional real-time nicety** | Vendor hooks (Claude `Stop`, Copilot `sessionEnd`) for end-of-turn nudges **where a vendor supports them** — now with the **recipe traveling into the target** (fix the gap: install `optional-ritual-hook.md` or document hook-setup in the installed `SKILLS.md`). | Best-effort, vendor-specific |

**All three rituals, covered vendor-neutrally:**

| Ritual | Layer-1 reinforcement |
|---|---|
| End-of-session log | git hook auto-stub (capture) + agent enrichment; CI warns if missing |
| Review cadence | hook/CI runs `memory-lint` → warns when `sessions_since_last_review ≥ review_every` |
| Sync skill adapters | hook/CI runs the `sync-adapters` script (idempotent, gitignored-only) |

## 6. Open design decisions (for the plan-gate)

1. **Nudge vs. auto-stub vs. both?** Auto-stub guarantees no ledger gap but writes a low-value file the
   agent must enrich; a pure nudge is lighter but can still be ignored. Recommend **auto-stub, with a
   marker** so `memory-lint` flags it — best of both.
2. **Advisory vs. hard-gate?** Default **advisory** (warn, never block) to honor the no-code/no-friction
   ethos; CI *fail* offered as an opt-in for teams that want enforcement.
3. **pre-commit vs. post-commit?** pre-commit can fold the stub *into* the same commit (cleaner history)
   but adds latency/friction; post-commit is frictionless but the stub lands in a follow-up commit.
   Recommend **post-commit nudge + opt-in pre-commit auto-stub**.
4. **Activation/install — RESOLVED toward zero-manual (2026-06-24, adoption constraint).** Enable
   **installs** `.githooks/` + the CI workflow + the recipe into the target, and the **agent
   auto-activates** the local git hook (`git config core.hooksPath .githooks`) during enable + via an
   idempotent first-run check — **no manual user step**. **CI is the zero-setup floor:** a committed
   workflow runs server-side on push/PR with **no per-user config at all** — the untrained-user-proof
   layer. *Honest limit:* git **cannot** auto-run committed hooks on a fresh clone (deliberate
   security — no auto-exec on clone), so a clone where **no agent has run** relies on **CI** as the
   backstop until an agent (its next enable/run) activates the local hook. Net: **CI = always-on,
   zero-config**; **git hook = agent-activated** (no user step in the common path); the two cover each
   other. Not "offer" — **installed + activated**. **(v4.20.0)** `.githooks/init.sh` + the `AGENTS.md`
   self-init note collapse the fresh-clone setup to a **single agent-run step** (the agent self-initializes
   on its first session) or **one human command** (`bash .githooks/init.sh`) — closing the gap a Copilot
   fresh-clone dogfood exposed (memory bootstrap self-initialized, but adapters + hook did not).
5. **Where the no-code line sits.** Document explicitly: these are env-run optional helpers
   (`no-build-step-agent-run` holds); the tool still ships/maintains only markdown + the bundled scripts.

## 7. Non-goals

No daemon; the tool runs nothing itself; **no hard-block by default**; the agent's *thoughtful* log is
never replaced by a script (only the stub/trigger is mechanized); not a CI mandate (advisory by default).

## 8. Vision linkage

Closes `bp-ritual-triggers` (Vision↔reality gap: *rituals fire reliably across every vendor, by default,
without per-vendor manual setup*) → serves `vision-agent-memory`. Reuses existing primitives: `memory-lint`
(deterministic checks), the `sync-adapters` script, the lightweight-mode rule (read-only = no log), and the
`(blueprint)` human-gate pattern.
