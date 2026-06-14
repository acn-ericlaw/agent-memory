# UPGRADE — Version Ladder

> How a repo already enabled with agent-memory is upgraded in place to the current
> tool version. **This file is reached only through `ENABLE.md` Mode B** — never
> invoked directly, exactly as `MIGRATE.md` is reached only through Mode C. The
> user's single entry point stays "AI enable this repo". This doc is
> tool-operator-only; it is *not* installed into target repos.

---

## Versioning model

The current tool version lives in the root **`VERSION`** file (semver):
- **MAJOR** — breaking change to memory-file shape/protocol (an un-upgraded agent
  couldn't correctly read/maintain the new files).
- **MINOR** — additive, backward-compatible (new optional file, vendor, section).
- **PATCH** — wording/clarity only.

| Version | Capability |
|---|---|
| 1.0.0 | Fresh enable from templates (Mode A) |
| 2.0.0 | Vendor detection + migration (Mode C); idempotent re-runs (Mode B) |
| 3.0.0 | Evolving memory: fact metadata + ids, decay-policy, review ritual, archive |
| 3.1.0 | AI-infrastructure `.gitignore` propagated into enabled repos (created or appended) |
| 3.2.0 | Protocol clarifications: session = one log-write (start best-effort); metadata ownership; stack-fact altitude; after-session checklist |
| 3.3.0 | Supersession: a fact can be marked `superseded` (replaced/invalidated), archived flagged "superseded" not "faded", terminal (never reactivated) |
| 3.4.0 | Invariant verification: `verify_invariants_every` prompts a human to re-confirm never-decay facts (`core` / Architectural Invariants) — never-decay ≠ never-checked |
| 3.5.0 | Write-time contradiction check: a new fact is scanned against existing ones → supersede (§9) or raise a `Contradiction:` Open Thread; review backstop |

Each enabled repo records what it is on in **`.agent/version.md`**:

```markdown
# agent-memory install manifest
- version:       3.0.0
- enabled_with:  2.0.0
- last_upgraded: 2026-06-13
- mode:          A
```

---

## How `ENABLE.md` Mode B uses this file

```
installed = read target .agent/version.md → version   (missing file → "2.x baseline")
current   = read tool root VERSION
if installed == current:  report "up to date — nothing to upgrade", stop.   # idempotent
if installed <  current:  run each rung below from installed up to current, in order;
                          then re-stamp .agent/version.md (version=current, last_upgraded=today);
                          report what changed.
if installed >  current:  the repo is newer than this tool checkout — stop and tell the user.
```

A **missing** `.agent/version.md` means the repo was enabled before versioning
existed. Treat it as `2.x` and run the 2→3 rung; create the stamp at the end.

Rungs are **idempotent**: before each change, check whether it is already present
and skip if so. Re-running an upgrade must be safe.

## Scope (unchanged from `ENABLE.md`)

Target-repo only. Never touch `~/`, `~/.claude/`, `~/.cursor/`, Application
Support, AppData, or system paths. Never delete; preserve/append. Never modify
source code or package manifests.

---

## Rung: 2.x → 3.0.0 — add the evolving-memory layer

Backward-compatible: do not remove or rewrite existing content; only enrich and add.

1. **Backfill fact metadata in `memory/continuity.md`.** For every existing fact
   (Key Decisions, Conventions, Stack lines, User Preferences, …):
   - assign a unique kebab `id`,
   - append the footer
     `<!-- id: … | created: <today> | last_used: <today> | uses: 1 | tier: working -->`.
   Unchecked Open Threads (`- [ ]`) get an id but are pinned (never decay). Do not
   fabricate history — `created`/`last_used` = today, `uses` = 1 is the honest
   baseline for a repo that had no metadata before. Facts are born `working`; the
   first review re-tiers them from the session-log event stream.

2. **Add `## Architectural Invariants`** immediately above `## Key Decisions`. Seed
   it from hard constraints already visible in `memory/instructions.md` (things that
   must never change). If none are obvious, leave a one-line note and add an Open
   Thread asking the user to populate it. Facts here never decay.

3. **Add `last_review`** to Project State: `- **last_review:** (none yet)`.

4. **Install `DECAY.md` and `REVIEW.md`** at the repo root (copy verbatim from the
   agent-memory tool root). Skip any that already exist and match.

5. **Create `memory/decay-policy.md`** from `templates/memory/decay-policy.md`
   (default windows; fill `{{PROJECT_NAME}}`). Skip if it already exists.

6. **Create the archive.** `memory/archive/INDEX.md` with a header and an empty
   table. Skip if present.

7. **Add `## Memory References` to the session-log convention.** Re-sync
   `.agent/schema.md` from `templates/.agent/schema.md` (it now documents the
   section). Do **not** edit past session logs — they predate the convention and
   are immutable; the first review tallies forward only.

8. **Re-sync changed protocol files.** Compare the target's `AGENTS.md` against
   `templates/AGENTS.md` (Before/During/After now mention metadata + review) and
   update only if different. Other bootstrap files (`CLAUDE.md`, `GEMINI.md`,
   dotfiles) are unchanged in 3.0.0 — leave them.

9. **Stamp** `.agent/version.md` → `version: 3.0.0`, `last_upgraded: <today>`,
   preserving `enabled_with` and `mode` (if the stamp was missing, set
   `enabled_with` to the detected baseline and `mode: A`).

10. **Report**: facts backfilled (N), files created/installed, where the policy and
    archive now live, and a reminder to populate `## Architectural Invariants`.

---

## Rung: 3.0.0 → 3.1.0 — propagate the AI-infrastructure `.gitignore`

Additive: the enabling user's personal AI-IDE runtime directories (`.claude/`,
`.kiro/`, `.cursor/`, …) should not be committed to the shared repo. Earlier
versions only added a comment to an existing `.gitignore` and never created one, so
those entries never reached the target. Bring the target up to the current behavior.

1. **Apply the managed `.gitignore` block** exactly as `ENABLE.md` Step 7 describes
   (the same logic — keep them in lockstep): create from `templates/.gitignore` if
   the target has none, otherwise add the sentinel-headed block and **only the entries
   not already present anywhere in the file** (de-duplicate — an older enable or the
   user may already ignore `.kiro/` etc.). The sentinel is
   `# === agent-memory: AI infrastructure (personal / per-machine — do not commit) ===`.

2. **Never remove or reorder** existing `.gitignore` entries — add-only. Adding a
   path does not untrack already-committed files, so this is safe.

3. **Stamp** `.agent/version.md` → `version: 3.1.0`, `last_upgraded: <today>`,
   preserving `enabled_with` and `mode`.

4. **Report**: whether `.gitignore` was created or appended, and how many entries
   were added.

---

## Rung: 3.1.0 → 3.2.0 — protocol clarifications (session model, metadata ownership, altitude)

Documentation/protocol clarifications from a real-work field report. **No memory-file
*shape* change** — re-sync the generic protocol docs and leave existing facts alone;
the review reconciles tiers as usual.

1. **Re-sync the generic protocol docs** (copy verbatim from the tool root / templates,
   only where different): `DECAY.md`, `REVIEW.md`, `.agent/schema.md`
   (from `templates/.agent/schema.md`), and `AGENTS.md` (from `templates/AGENTS.md`).
   These now define a session as **one log-write** (several per conversation OK) with
   `start` **best-effort**; pin metadata ownership (agent seeds `id`/`created`/`tier` +
   `uses: 1`, the review owns `uses`/`last_used`/`tier`); state the
   leave-`[x]`-for-the-review rule; mark `## Stack & Tools` as the canonical stack
   home; and add an after-session checklist.

2. **Add the stack-altitude notes** (only if absent, don't move existing content): in
   `memory/instructions.md` that precise deps/versions live in `continuity.md` →
   `## Stack & Tools`, and the canonical-home note on that section.

3. **Don't rewrite existing fact metadata.** "Born `working`" applies to facts created
   from now on; leave already-stamped tiers for the review to reconcile.

4. **Stamp** `.agent/version.md` → `version: 3.2.0`, `last_upgraded: <today>`,
   preserving `enabled_with` and `mode`.

5. **Report**: which docs were re-synced and the notes added.

---

## Rung: 3.2.0 → 3.3.0 — supersession / fact-invalidation

Additive: a new terminal `superseded` tier + optional `superseded-by`/`supersedes`
footer fields, so a fact that becomes *false* (not just unused) is retired correctly.
**No shape change to existing facts** — repos without superseded facts are unaffected,
and the optional fields appear only when a fact is actually superseded.

1. **Re-sync the generic rule/protocol docs** (copy verbatim from the tool root /
   templates, only where different): `DECAY.md` (new `superseded` tier, §9, the rule),
   `REVIEW.md` (applies `Superseded:` events; archives flagged "superseded"),
   `.agent/schema.md` (footer fields + the `Superseded:` Memory-References line), and
   `AGENTS.md` (the after-session supersession step).
2. **No data migration.** Existing facts are untouched; supersession applies only when
   a fact is reversed/invalidated from now on.
3. **Stamp** `.agent/version.md` → `version: 3.3.0`, `last_upgraded: <today>`,
   preserving `enabled_with` and `mode`.
4. **Report**: docs re-synced; the supersession capability is now available.

---

## Rung: 3.3.0 → 3.4.0 — invariant verification cadence

Additive: never-decay facts (`core` / Architectural Invariants) can quietly go
*wrong*; the review now periodically prompts a human to re-confirm them. A new policy
knob + tracker field; no change to existing facts.

1. **Add `verify_invariants_every`** to `memory/decay-policy.md` (default `20`) — only
   if absent; preserve any existing value.
2. **Add `last_invariant_check`** to `continuity.md` Project State, just below
   `last_review` (value `(none yet)` if never run). It will first fire at the next
   review once that many session files exist.
3. **Re-sync the generic protocol docs** (copy verbatim where different): `REVIEW.md`
   (new routine step 6 + the verify trigger + summary line), `DECAY.md` (the
   "never-decay ≠ never-checked" note in §6), `.agent/schema.md` (the
   `last_invariant_check` Project-State field + the policy knob).
4. **Stamp** `.agent/version.md` → `version: 3.4.0`, `last_upgraded: <today>`,
   preserving `enabled_with` and `mode`.
5. **Report**: knob + tracker added, docs re-synced.

---

## Rung: 3.4.0 → 3.5.0 — write-time contradiction check

Additive (a behavioral rule + a review backstop; no new fields, tiers, or knobs). It
generalizes the migration-time contradiction check to normal sessions, resolving via
supersession (§9) or an Open Thread.

1. **Re-sync the generic protocol docs** (copy verbatim where different): `DECAY.md`
   (new §10), `REVIEW.md` (the "Contradiction backstop" note after the routine), and
   `AGENTS.md` (the before-adding-a-fact contradiction check in the after-session step).
2. **No data migration, no new metadata.** Nothing to backfill.
3. **Stamp** `.agent/version.md` → `version: 3.5.0`, `last_upgraded: <today>`,
   preserving `enabled_with` and `mode`.
4. **Report**: docs re-synced; the write-time contradiction check is now in effect.
