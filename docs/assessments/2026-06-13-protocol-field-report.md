# Feedback: agent-memory protocol (field report)

**From:** Claude Code (acting as a consuming agent)
**Date:** 2026-06-13
**Protocol version exercised:** agent-memory v3.1.0 templates, Mode A install
**Where:** the `simple-proxy` repo (a small Rust/Tokio CLI), AI-enabled with agent-memory
**Workload:** a multi-task session — a Node.js→Rust rewrite, a dependency removal, building
a new module, and a workspace refactor — i.e. several distinct tasks within one long
interactive conversation.

> This is a standalone hand-off note. It assumes no shared context with the reader. File
> references below point at the installed template set (`AGENTS.md`, `memory/instructions.md`,
> `memory/continuity.md`, `.agent/schema.md`, `REVIEW.md`, `DECAY.md`, `memory/decay-policy.md`).

---

## What the protocol got right

1. **Single vendor-neutral entry point.** The `CLAUDE.md → AGENTS.md → {instructions,
   continuity, sessions}` chain is unambiguous. Orientation took one read with zero
   guessing, and a different agent family would land in exactly the same place.

2. **Open Threads created a closed loop.** Threads surfaced during enablement became a
   ready-made punch list later: during the rewrite I closed seven JS-era threads in one
   pass and could trace each to its fix. "Surface at analysis → resolve later, traceably"
   is the single most valuable behavior the protocol produced.

3. **Architectural Invariants as guardrails.** Core-tier invariants (e.g. "minimal
   dependencies", "Layer-4 only") were exactly what I consulted when making design calls.
   Marking them never-decay and separating them from ordinary decisions is the strongest
   part of the design.

4. **Unobtrusive metadata + markdown-only.** The HTML-comment fact footers vanish when
   rendered, so files stay human-readable while carrying machine state. No runtime/codegen
   meant plain file tools were enough.

---

## Friction points (observation → impact → suggestion)

### 1. "Session" is under-defined for long, multi-task conversations
- **Observation:** The schema prescribes one session file per session with full ISO 8601
  start/end timestamps. My single conversation covered several distinct tasks over ~an
  hour. I wrote **three** session logs, and I had to **invent the start timestamps** — a
  consuming agent generally does not track the wall-clock instant it began.
- **Impact:** Inconsistent practice (one-file-per-conversation vs. per-task), and
  fabricated `start` values that undermine the "removes ambiguity about session
  boundaries" goal.
- **Suggestion:** Define a "session" precisely — recommend the **persist-event** model
  (a session = one write of a log file, covering the work since the last write). Make
  `start` **best-effort/optional** (or just record persist time), and explicitly bless
  multiple work-segment logs per conversation.

### 2. The agent-vs-review metadata split is subtle
- **Observation:** Guidance says "don't edit fact metadata mid-session; the review ritual
  does the counting." But on **fact creation** I still had to hand-set
  `tier: working | created | last_used | uses: 1`, and my `uses:` seeds (1, 2) were
  guesses. Maintaining the manual `## Memory References` list correctly (referenced /
  created / reactivated ids) was the easiest thing to get out of sync with what I actually
  touched.
- **Impact:** Ambiguous ownership of metadata; hand-seeded counts that the review must
  then reconcile; risk of drift between the fact footers and the Memory References log.
- **Suggestion:** State explicitly *which fields the agent sets at creation* vs. *which the
  review owns* (ideally: agent sets only `id` + `tier: working` + `created`; review owns
  `uses`/`last_used` entirely, including the initial count). Consider deriving Memory
  References mechanically rather than asking the agent to curate it by hand.

### 3. Resolved Open Threads accumulate in the live file
- **Observation:** I marked threads `[x]` but left them in `continuity.md`; the protocol
  says completed threads are archived by the review, cadence every ~10 sessions.
- **Impact:** For a young repo, the live continuity file carries resolved cruft for a long
  time before any review fires. I was unsure whether to archive them myself.
- **Suggestion:** Give the agent an explicit rule — e.g. "leave `[x]` threads for the
  review" **or** "archive a thread in the same session you complete it." State one.

### 4. Stack/structure facts live in two files
- **Observation:** After the rewrite I updated language/deps/structure in **both**
  `instructions.md` (Repository Structure / Stack) and `continuity.md` (Stack & Tools /
  invariants).
- **Impact:** Duplication that can drift; "what's the stack" genuinely straddles the
  stable-config vs. live-state boundary.
- **Suggestion:** Pick one canonical home for stack facts and have the other reference it,
  or carve a crisp rule for what counts as "stable" (instructions) vs. "live" (continuity).

### 5. No reinforcement of the after-session ritual
- **Observation:** The protocol is pure convention; nothing verified I wrote the log or
  updated continuity. The surrounding harness, by contrast, actively nudged me toward its
  task-tracking tool.
- **Impact:** Compliance depends on agent diligence; easy to skip under time pressure.
- **Suggestion:** Provide a lightweight, surfaced "after-session checklist" (or an optional
  hook/linter) so the ritual is prompted, not merely documented.

---

## Things that were correctly guarded (keep these)

- **Personal vs. project memory boundary** (repo `memory/` vs. runtime `~/.claude/`) was
  clear; I never conflated them.
- **"User Preferences: record ONLY what the user explicitly states; never infer"** actively
  stopped me from over-recording inferred preferences. Good guard — keep it.

---

## Prioritized recommendations

1. **(High)** Define the session boundary (persist-event model) and relax `start` to
   best-effort. This removes the most real-world friction.
2. **(High)** Pin down metadata ownership (agent-set vs. review-computed) and consider
   auto-deriving Memory References.
3. **(Medium)** State the archive-on-complete vs. defer-to-review rule for Open Threads.
4. **(Medium)** Resolve the instructions/continuity duplication for stack facts.
5. **(Low)** Add a surfaced after-session checklist or hook.

---

## Net assessment

The protocol earned its keep on this workload: the Open-Thread backlog and the invariants
shaped real engineering decisions, and continuity gave a clean "where things stand" each
time work resumed. The cost was session-log bookkeeping and dual-file updates. For
multi-agent or team use the trade clearly favors the protocol; for a fast solo session the
overhead is noticeable but modest. The highest-leverage fixes are tightening the session
definition and the metadata-ownership rules.
