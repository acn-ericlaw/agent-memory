# Design — Evolving Long-Term Memory

> **Status:** proposal, for review. Nothing here is wired into the protocol yet.
> When approved, this doc spawns `DECAY.md` + `REVIEW.md` and edits to the
> templates/schema/examples (see §10 Implementation Plan).
>
> Refines `~/Downloads/INSIGHT-evolving-memory.md` (the Claude.io sketch). Two
> design forks were settled before writing this: tier decisions use
> **deterministic integer rules** (no floating-point strength score), and usage
> metadata is **event-sourced** (derived from session logs, not hand-maintained).
> See §2 for what changed from the original insight and why.
>
> **Update (2026-06-13):** §11 open questions resolved; **tool versioning + an
> in-place upgrade path added (§12)** so repos enabled by an older version can be
> upgraded. Design approved in principle — implementation pending green light.

---

## 1. The Problem (stated precisely)

`continuity.md` is a flat ledger — everything appended stays forever at equal
weight. The goal is human-like memory: frequently-used facts strengthen, unused
ones fade, truly important ones stay permanent.

But check the premise against this repo's *actual* state: `continuity.md` is
~113 lines and most of it is **Open Threads** (many already `[x]`) plus Key
Decisions. The thing that grows unboundedly by design is `sessions/` (one file
per session, forever). So the lean-ness win comes from two targets the original
sketch under-weighted:

1. **Stale facts** — Key Decisions / free facts nobody references anymore.
2. **Completed Open Threads** (`[x]`) — these pile up and are the bulk of the
   current file.

`sessions/` is **not** a decay target. It is the event log (see §4). We never
rewrite or archive it.

---

## 2. What Changed From the Original Insight — and Why

| Original sketch | This design | Why |
|---|---|---|
| `strength` float, `w1·recency + w2·frequency + w3·importance`, `exp(-n/half_life)` | **Dropped.** Tiers from two integers + override flags | An LLM cannot reliably compute `exp(-7/30)`, and two vendors (Claude/Gemini/Cursor) will disagree. In a vendor-neutral tool that means one agent archives what another just promoted. The float was false precision the substrate can't deliver. |
| Each session edits `uses`/`last_used` inline on every referenced fact | **Event-sourced.** Sessions record a short reference list; review *recomputes* metadata from logs | Per-session inline editing is the most forgettable step; if skipped, every fact reads stale and live facts get archived. Counts derived from logs are reproducible by any agent re-running review. |
| (implicit fact identity) | **Stable fact IDs** (kebab-case) on every fact | The linchpin of event-sourcing: a session log references facts by ID; review tallies by ID. Without IDs, "which fact did this session touch?" is fuzzy matching — non-deterministic. |
| `tunable weights` in `decay-policy.md` | **Integer thresholds only** (windows in *sessions*) | Nothing to tune that requires arithmetic. The agent counts files; LLMs count short lists reliably. |
| `sessions/` "unchanged" (by omission) | `sessions/` is the **immutable event log** (by principle) | Once metadata is derived from logs, mutating a log corrupts the projection's source of truth. This is now a hard constraint. |
| decay targets "facts" | decay targets facts **and completed `[x]` Open Threads** | That's where the real bloat is in practice. |

Kept from the original (these were right): tier system, archive-as-cold-storage,
two-way reactivation, sessions-not-days as the time unit, Open Threads never
decay, `core` as a human override, all-markdown / agent-does-the-work.

---

## 3. Memory Shape — Metadata + Stable IDs

Each fact carries a short HTML-comment footer. Invisible in rendered markdown,
fully readable by any agent, hand-editable, clean-ish diffs.

```markdown
## Key Decisions

- POST-only for mutations, no PUT/PATCH (legacy decision, do not change)
  <!-- id: post-only-mutations | created: 2026-06-08 | last_used: 2026-06-12 | uses: 14 | tier: core -->

- Webhooks use fire-and-forget, no retry queue
  <!-- id: webhook-fire-forget | created: 2026-06-10 | last_used: 2026-06-10 | uses: 1 | tier: working -->
```

### Fields

| Field | Set when | Recomputed at review? |
|---|---|---|
| `id` | once, at fact creation (kebab-case, unique within the file) | no — stable forever |
| `created` | once, at fact creation (date) | no |
| `last_used` | date of the most recent session referencing this id | **yes** (from logs) |
| `uses` | count of sessions that referenced this id | **yes** (from logs) |
| `tier` | lifecycle bucket | **yes** (from rules) |

No `strength`. No `importance` field — importance is expressed by `tier: core`
or living under `## Architectural Invariants`.

---

## 4. The Event Log — How Sessions Record References

Session logs gain one lightweight section. The agent writes it at session end
(it's already writing the log), so there is **no per-fact bookkeeping**:

```markdown
## Memory References
- Referenced: post-only-mutations, webhook-fire-forget
- Created: graphql-gateway-added (tier: working)
- Reactivated: drizzle-vs-prisma
```

- **Referenced** — ids the session relied on or reinforced.
- **Created** — new facts this session added to `continuity.md` (born `working`).
- **Reactivated** — ids pulled back from the archive because they came up again.

That's it. The agent never counts and never edits metadata mid-session. Counting
is the review's job, and it's derivable: `uses` for an id = number of session
logs listing it; `last_used` = date of the latest such log.

> **Constraint:** session logs are append-only and immutable. They are the
> source of truth for the projection. Never rewrite, renumber, or archive them.
> (Optional quarterly *summaries* are fine — see §7 — but the raw logs stay.)

---

## 5. Tiers + Deterministic Rules

```
core              ← permanent. Human-set (or sustained auto-core). Never decays.
active            ← referenced within active_window sessions.
working           ← created within working_window sessions, not yet re-referenced. Probationary.
archive-candidate ← not referenced for > active_window but ≤ archive_window. Flagged.
archived          ← not referenced for > archive_window. Moved to memory/archive/YYYY-QN.md.
```

Movement is **bidirectional** — an archived id that appears in a session's
`Referenced`/`Reactivated` list is pulled back to `active`. Nothing is deleted.

### The only arithmetic: counting session files

`sessions_since_last_used` = **the number of session files chronologically after
the one named in `last_used`**. Session files sort lexicographically =
chronologically (`YYYY-MM-DD-HHMMSS.md`), so this is a count of a list, not a
formula. Any agent gets the same integer.

### Tier decision (applied in order — first match wins)

1. `tier: core` → **stays core**. (human override; never auto-demoted)
2. Lives under `## Architectural Invariants` → **pinned**, treated as core.
3. Unchecked Open Thread (`- [ ]`) → **pinned active**, never decays.
4. `created` within `working_window` sessions ago AND `uses ≤ 1` → **working**.
5. `sessions_since_last_used ≤ active_window` → **active**.
6. `active_window < sessions_since_last_used ≤ archive_window` → **archive-candidate** (warn).
7. `sessions_since_last_used > archive_window` → **archived** (move to archive/).

### Auto-core (conservative; off by default)

The system never silently makes something permanent. Optional rule, documented
but disabled unless the user opts in: promote to `core` only if `uses ≥
core_min_uses` AND it has stayed `active` across `core_min_reviews` consecutive
reviews. Default posture: **`core` is human-only.**

---

## 6. Policy File — `templates/memory/decay-policy.md`

Integer windows measured in **sessions**. No weights, no half-life, no floats.

```markdown
# Memory Policy

## Lifecycle windows (sessions)
- working_window:   3     # new facts stay "working" until re-referenced within this many sessions
- active_window:    8     # referenced within this many sessions → active
- archive_window:   20    # not referenced for more than this → archived

## Review triggers
- review_every:         10   # run a review this many sessions after the last one
- continuity_max_facts:  30  # primary lean signal — count of decaying facts/threads (verbosity/velocity-immune)
- continuity_max_lines: 600  # coarse backstop (a mature layer sits ~450–600 even when healthy)

## Auto-core (default: off — core is human-set)
- enabled:          false
- core_min_uses:    12
- core_min_reviews: 5

## Never decays
- tier: core
- anything under "## Architectural Invariants"
- unchecked Open Threads ( - [ ] )
```

Users tune by editing integers. Hand-editing any `tier:` in `continuity.md`
always wins over the rules.

---

## 7. The Review Ritual — `REVIEW.md`

**Triggered** three ways: every `review_every` sessions (automatic, post-session);
on user command (*"review memory"* / *"compact memory"*); or when
`continuity.md` exceeds `continuity_max_lines`.

**Steps (incremental — the routine path):**

1. Determine the window: session logs since `last_review` (tracked in
   `continuity.md`). Read their `## Memory References` sections.
2. For each referenced id: `uses += (count in window)`, `last_used = latest date`.
3. For each id in `continuity.md`: count `sessions_since_last_used`, apply the
   §5 tier rules.
4. **Archive** ids that fell to `archived` → append to `memory/archive/YYYY-QN.md`,
   update `archive/INDEX.md`, remove from `continuity.md`.
5. **Reactivate** any archived id named in the window → move back to
   `continuity.md` as `active`, refresh `last_used`/`uses`.
6. **Sweep completed Open Threads:** `[x]` threads whose completion is older than
   `archive_window` sessions → move to the archive (this is the real bloat win).
7. Set `last_review` to today; write the review summary into the session log.

**Full rebuild (the ground-truth path):** because everything is derived, an agent
can ignore stored counts and recompute `uses`/`last_used`/`tier` for every id by
scanning *all* session logs. Use this to repair drift or after manual edits.

### Review summary (in the session log)

```markdown
## Memory Review (2026-06-20)
- Reactivated:  1  (drizzle-vs-prisma — referenced today after 9 dormant sessions)
- Archived:     3  (→ memory/archive/2026-Q2.md)
- Swept threads: 4 completed Open Threads archived
- Tier changes: 6  (2 working→active, 1 active→archive-candidate, 3 →archived)
```

---

## 8. Archive Structure

```
memory/
  continuity.md        ← active + core + working + open threads (stays lean)
  decay-policy.md      ← integer windows + triggers
  sessions/            ← immutable event log (NEVER archived/rewritten)
  archive/
    2026-Q1.md         ← archived facts + swept completed threads, this quarter
    2026-Q2.md
    INDEX.md           ← id → one-line + which quarter file it lives in (greppable)
```

Before saying "I don't have context on that," an agent greps `archive/INDEX.md`.

---

## 9. What the Agent Does Each Session (after this lands)

```
Before:
  Read continuity.md (lean: active + core + working + open threads).
  Optionally grep archive/INDEX.md for relevant past topics.

During:
  Note which fact ids you rely on, which you create, which you pull from archive.
  (No metadata editing. Just remember for the log.)

After:
  Write the session log as usual + a "## Memory References" section.
  Born-this-session facts get an id and tier: working.
  If sessions-since-last-review ≥ review_every (or continuity.md > max lines):
    run REVIEW.md.
```

---

## 10. Implementation Plan (when approved)

Each step is independently testable. Ordering mirrors how `MIGRATE.md` sits
beside `ENABLE.md`.

1. **`DECAY.md`** — reference doc: metadata fields, fact IDs, the deterministic
   tier rules, the "count session files" rule. (The §3/§5 content, formalized.)
2. **`REVIEW.md`** — the §7 protocol: triggers, incremental vs full rebuild,
   archive/reactivate/sweep, summary format.
3. **`templates/memory/decay-policy.md`** — the §6 file.
4. **`templates/memory/continuity.md`** — add `## Architectural Invariants`
   (above Key Decisions; never decays), show metadata comments + ids on sample
   facts, add a `last_review:` field to Project State.
5. **Session-log schema** — add the `## Memory References` section to
   `templates/.agent/schema.md` **and** anywhere the session block is documented.
   *(CLAUDE.md rule: schema changes move templates/, schema.md, and examples in
   lockstep.)*
6. **`AGENTS.md` + `templates/AGENTS.md`** — Before/During/After additions:
   grep archive INDEX; record Memory References; run REVIEW every N sessions.
7. **`ENABLE.md`** — Step 5 copies `decay-policy.md`; generated `continuity.md`
   emits `## Architectural Invariants` + metadata/ids; add the post-session
   "if ≥ review_every, run REVIEW.md" step.
8. **`examples/evolving-memory-example/`** — a worked before/after: `continuity.md`
   pre- and post-review, an `archive/2026-Q2.md`, and a session log showing a
   reactivation + a Memory Review summary.
9. **Versioning files** — add a root `VERSION` (`3.0.0`), a
   `templates/.agent/version.md` install-manifest template, and make `ENABLE.md`
   Mode B version-aware (installed vs. current → up-to-date exits, older runs the
   ladder, re-stamp). See §12.
10. **`UPGRADE.md`** — the version ladder (reference doc, reached only via Mode B,
    like `MIGRATE.md`). Ships with the 2.x→3.0.0 rung: assign ids, backfill
    metadata, add Architectural Invariants + `decay-policy.md` + `archive/`, re-sync
    bootstrap files.
11. **Sync the docs that must not drift** — `README.md` two-layer section + a
    version table, and the root `CLAUDE.md` architecture section (standing Open
    Thread to keep these in sync when file shapes change).

---

## 11. Resolved Decisions

1. **Fact IDs everywhere — YES.** Every fact gets a stable kebab `id` at birth.
   The linchpin that makes review tallies deterministic.
2. **Upgrade mechanism — `ENABLE.md` Mode B, made version-aware** (accepted). The
   per-version migration steps live in `UPGRADE.md`, reached only through Mode B
   (mirrors `MIGRATE.md` ← Mode C). "AI enable this repo" stays the single entry
   point. See §12.
3. **Auto-core — OFF. `core` is human-set only.** The system never silently makes
   a fact permanent.
4. **Default windows — shipping** `working_window: 3`, `active_window: 8`,
   `archive_window: 20`, `review_every: 10`; tunable per-repo in `decay-policy.md`.
5. **Doc location** — the rules shipped as `DECAY.md` + `REVIEW.md` (repo root,
   installed into enabled repos). This document is kept as the design rationale and
   now lives under `docs/` (moved 2026-06-13); history stays in git.

---

## 12. Tool Versioning & Upgrade Path

The tool evolves; repos enabled by an older version must be upgradable in place.
This is what makes `ENABLE.md` Mode B more than a no-op.

### Semantic version — single source of truth

Root **`VERSION`** holds the current tool version (one line, e.g. `3.0.0`):

- **MAJOR** — breaking change to memory-file *shape* or protocol (an un-upgraded
  agent couldn't correctly read/maintain the new files).
- **MINOR** — additive, backward-compatible (new optional file, vendor, section).
- **PATCH** — wording/clarity, no structural change.

| Version | Capability |
|---|---|
| 1.0.0 | Fresh enable from templates (Mode A) |
| 2.0.0 | Vendor detection + migration (Mode C), idempotent re-runs (Mode B) |
| 3.0.0 | Evolving memory: metadata + fact IDs, decay-policy, review ritual, archive |

Evolving memory is **3.0.0** and **backward-compatible**: metadata lives in HTML
comments (invisible to an un-upgraded reader) and new files are additive, so a 2.x
repo still functions before upgrade — the upgrade just turns the layer on.

### Per-repo install stamp — `.agent/version.md`

Each enabled repo carries a small manifest. It lives in `.agent/` but **not** in
`schema.md` (which is copied verbatim and must stay identical across repos —
install-specific state can't live in a verbatim file):

```markdown
# agent-memory install manifest
- version:       3.0.0       # what this repo is currently on
- enabled_with:  2.0.0       # version that first enabled it
- last_upgraded: 2026-06-13
- mode:          A           # how first enabled: A fresh / C migrate
```

A **missing** stamp ⇒ enabled before versioning existed (≤ 2.x) ⇒ run the full
ladder from the 2→3 rung.

### The upgrade ladder — `UPGRADE.md`

Reference doc with the exact migration per version transition, **reached only
through `ENABLE.md` Mode B** — never invoked directly (the `MIGRATE.md` ← Mode C
pattern). Keeps one user-facing entry point.

```
Mode B (Already Ours):
  installed = read .agent/version.md   (missing → treat as 2.x baseline)
  current   = read root VERSION
  if installed == current:  report "up to date", exit            # idempotent
  if installed <  current:  run UPGRADE.md rungs installed→current, in order
                            re-stamp .agent/version.md (version, last_upgraded)
                            report what changed
```

**The 2.x → 3.0.0 rung** (the only rung today):
1. Assign a kebab `id` to every fact in `continuity.md`.
2. Backfill metadata: `created: <today>`, `last_used: <today>`, `uses: 1`,
   `tier: active`. (Old `sessions/` predate `## Memory References` and are
   immutable — leave them; the first review tallies forward only.)
3. Add `## Architectural Invariants` above Key Decisions (empty; prompt to fill).
4. Copy in `memory/decay-policy.md` (default windows); create empty
   `memory/archive/INDEX.md`.
5. Re-sync changed bootstrap/protocol files (e.g. the session-log schema).
6. Stamp `.agent/version.md` → `3.0.0`.

Idempotent: a repo already at `3.0.0` hits "up to date" and exits.

---

## 13. Scope Reminder

All of this lives inside a target repo's `memory/` directory. Nothing in `~/`,
`~/.claude/`, AppData, or Application Support is touched. The evolving memory is
the *team's* shared, git-committed layer — not the user's personal AI tooling.
