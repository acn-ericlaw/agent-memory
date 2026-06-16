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
| 3.6.0 | Memory smoke test: `memory/smoke-test.md` — manual eval, N questions a fresh agent should answer from memory alone |
| 3.7.0 | Provenance + retrieval: optional `origin:` footer (the session a fact came from); retrieval documented as lexical + indexed by design |
| 4.0.0 | Forward layer (VBDI): `memory/vision.md` + `(blueprint)` gap threads + altitude trace; the cognitive loop over the memory substrate. Upgrade bootstraps a DRAFT Vision + human gate |
| 4.1.0 | Cross-vendor skills layer: neutral committed `agent-skills/<name>/SKILL.md` + an `AGENTS.md` baseline (agent-as-runtime) + regenerated Claude/Gemini/Cursor adapters. Migration promotes vendor `.claude/skills/` into `agent-skills/`; upgrade promotes any existing vendor skills in place |
| 4.1.1 | Skills-layer refinements (PATCH): folder finalized as `agent-skills/` (collision-safe); Cursor adapter uses the agent-requested type (`description` + empty `globs` + `alwaysApply: false`); collision guard; vendor-dir double-duty clarified |
| 4.2.0 | "Sync skill adapters" operation: regenerate the per-vendor adapters from `agent-skills/` on demand (needed after clone/pull — adapters are gitignored, don't travel). The adapter recipe + sync steps now live in the installed `AGENTS.md` "Skills" section (canonical); `ENABLE.md` Step 5h references it |
| 4.3.0 | Skill **authoring convention** (create in `agent-skills/`, never a vendor folder) + **"adopt skill"** safety-net (promote a vendor-folder-authored skill into `agent-skills/`), wired into the session-close ritual so a natively-authored skill is never left unshared |
| 4.3.1 | Skills-layer doc fixes (PATCH, from a session-close test-drive): "Adopt a skill" no longer says "commit" mid-ritual (stage for the session-end commit); session-close check notes adopt-before-log ordering; body-normalization + detection clarified |
| 4.3.2 | Skills-layer description hardening (PATCH, from a lifecycle sanity check): adapter `description` mirrors the neutral skill's verbatim; skill descriptions kept single-line & quote-free (escape/quote if unavoidable) so they embed safely in TOML/MDC/YAML — prevents invalid or drifted adapters |

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

---

## Rung: 3.5.0 → 3.6.0 — memory smoke test

Additive: a new installed file, `memory/smoke-test.md` — a manual memory-quality check.

1. **Create `memory/smoke-test.md`** from `templates/memory/smoke-test.md`, filling
   `{{PROJECT_NAME}}` and `{{TODAY}}`. Seed `{{PROJECT_SMOKE_QUESTIONS}}` with 2–4
   project-specific questions inferred from the existing `instructions.md` /
   `continuity.md` (a newcomer should be able to answer them from memory). Skip if the
   file already exists.
2. **Re-sync `.agent/schema.md`** (it now documents `memory/smoke-test.md`).
3. **Stamp** `.agent/version.md` → `version: 3.6.0`, `last_upgraded: <today>`,
   preserving `enabled_with` and `mode`.
4. **Report**: smoke test created; suggest running it once to set a baseline.

---

## Rung: 3.6.0 → 3.7.0 — provenance + retrieval-at-scale

Additive: an optional `origin:` footer field (provenance) + retrieval guidance. No new
machinery, no forced migration.

1. **Re-sync the generic docs** (copy verbatim where different): `DECAY.md` (the `origin`
   row in §1 + new §11 "Provenance & retrieval"), `REVIEW.md` (the `origin`-backfill
   note), `.agent/schema.md` (the `origin` field + the retrieval note), and `AGENTS.md`
   (set `origin` on new facts; the retrieval pointer in "Before Every Session").
2. **No backfill required.** `origin` is optional; new facts get it going forward, and a
   later review can repair it from the earliest `Created` event. Existing facts are fine
   without it.
3. **Stamp** `.agent/version.md` → `version: 3.7.0`, `last_upgraded: <today>`,
   preserving `enabled_with` and `mode`.
4. **Report**: docs re-synced; provenance pointers available on new facts.

---

## Rung: 3.7.0 → 4.0.0 — the forward layer (VBDI), with Vision bootstrap

A **new layer**, but still **additive**: a repo with no Vision works exactly as before
(an un-upgraded agent ignores `memory/vision.md` and `(blueprint)` threads). The catch
is that existing repos have no Vision/Blueprint — so this rung **bootstraps** them rather
than fabricating intent.

1. **Re-sync the generic docs** (copy verbatim where different): `DECAY.md` (§10 altitude
   drift + new §12 "The forward layer"), `REVIEW.md` (the Vision in the invariant-verify
   step + altitude drift in the backstop), `.agent/schema.md` (the `memory/vision.md` +
   Blueprint sections), and `AGENTS.md` (the "cognitive loop" section + Vision in the
   session read-list).
2. **Bootstrap the Vision — never fabricate it** (the target is the human's to set, like
   User Preferences). Create `memory/vision.md` from `templates/memory/vision.md`: fill
   `{{PROJECT_NAME}}` / `{{PROJECT_SLUG}}` / `{{TODAY}}` and the **Current-state context
   only** (`{{PROJECT_DESCRIPTION}}` / `{{PROJECT_TYPE}}` from the existing
   `instructions.md`); leave the target / success criteria / non-goals as the template's
   `(…)` prompts; keep the ⚠️ DRAFT banner. Skip if `memory/vision.md` already exists.
3. **Raise the human gate** in `continuity.md`:
   `- [ ] (vision-bootstrap) Confirm the Vision in memory/vision.md — set the target / success criteria / non-goals; then derive the Blueprint.`
   **Do not derive the Blueprint yet** (it needs the confirmed target). Until the Vision
   is confirmed, VBDI drift-detection stays advisory.
4. **Stamp** `.agent/version.md` → `version: 4.0.0`, `last_upgraded: <today>`,
   preserving `enabled_with` and `mode`.
5. **Report**: docs re-synced; Vision **bootstrapped as a DRAFT** — the maintainer must
   confirm it (the `(vision-bootstrap)` thread), after which the Blueprint is derived.

---

## Rung: 4.0.0 → 4.1.0 — the cross-vendor skills layer

Additive (a new optional shared layer): a repo with no skills works exactly as before, and
an un-upgraded agent simply ignores `agent-skills/`. Design: `docs/DESIGN-skills-layer.md`.

1. **Re-sync the generic docs** (copy verbatim where different): `.agent/schema.md` (the
   new `agent-skills/` section) and `AGENTS.md` (the new "Skills" section + the `agent-skills/` entry
   in Memory File Locations). `DECAY.md` / `REVIEW.md` are unchanged in 4.1.0.
2. **`.gitignore` — no entry change needed.** The vendor adapter dirs (`.claude/`,
   `.gemini/`, `.cursor/`) are already ignored by the v3.1.0 managed block, and `agent-skills/`
   is tracked by default (never ignored). Optionally refresh the managed-block comment to
   mention `agent-skills/` + adapters (cosmetic only).
3. **Promote any existing vendor skills.** If the target has `.claude/skills/` (or another
   vendor's skill bundle), promote each into `agent-skills/<name>/SKILL.md` per `MIGRATE.md`
   Section B2 (keep the procedure; normalize frontmatter to `name` + `description`; copy
   bundled scripts to `agent-skills/<name>/scripts/`), preserve the original under `legacy/`,
   then regenerate the Claude / Gemini / Cursor adapters per `ENABLE.md` Step 5h. **If there
   are no vendor skills, skip — do not create an empty `agent-skills/`.**
4. **Stamp** `.agent/version.md` → `version: 4.1.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
5. **Report**: docs re-synced; skills promoted (N) + adapters regenerated, or "no skills
   found — skills layer available on demand."

---

## Rung: 4.1.0 → 4.1.1 — skills-layer refinements (PATCH)

Wording/format corrections to the 4.1.0 skills layer; no shape change. (4.1.0 shipped
same-day and was unconsumed, so a target on 4.0.0 reaches 4.1.1 via the 4.0.0→4.1.0 rung
above — which already produces `agent-skills/`. This rung only matters for a repo that ran
the original 4.1.0, where the folder was briefly named `skills/`.)

1. **Rename the folder if needed.** If the target has a top-level `skills/` created by the
   original 4.1.0, rename it to `agent-skills/` (preserve history with `git mv` if tracked)
   and update the regenerated adapters' pointers. If it is already `agent-skills/` — or
   there are no skills — this is a no-op.
2. **Apply the doc/format fixes** (verbatim where different): `.agent/schema.md` and
   `AGENTS.md` now say `agent-skills/`; the Cursor adapter uses the agent-requested type
   (`description` + empty `globs:` + `alwaysApply: false`) — refresh any `.cursor/rules/`
   skill adapters accordingly.
3. **Stamp** `.agent/version.md` → `version: 4.1.1`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: folder renamed (if applicable), adapters refreshed, docs re-synced.

---

## Rung: 4.1.1 → 4.2.0 — "sync skill adapters" operation

Additive: a new agent-driven operation to regenerate per-vendor skill adapters from the
committed neutral skills — needed because adapters are gitignored and don't travel with a
clone/pull. No data, skill, or shape change.

1. **Re-sync the generic docs** (verbatim where different): `AGENTS.md` — its "Skills"
   section now carries the **canonical adapter recipe + the "sync skill adapters" operation**
   (the recipe moved here from `ENABLE.md` Step 5h, which now references it); and
   `.agent/schema.md` (notes the on-demand sync). `DECAY.md` / `REVIEW.md` unchanged.
2. **No data migration.** Existing skills/adapters are untouched. Optionally run "sync skill
   adapters" now to (re)generate this machine's adapters — it's on-demand and local.
3. **Stamp** `.agent/version.md` → `version: 4.2.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: `AGENTS.md` re-synced (now documents adapter sync); the operation is available.

---

## Rung: 4.2.0 → 4.3.0 — skill authoring convention + "adopt skill" safety-net

Additive (docs/protocol; no data or shape change). Closes the footgun where a skill authored
natively in a vendor folder (e.g. a built-in skill creator) is gitignored and never reaches
the shared `agent-skills/` layer.

1. **Re-sync the generic docs** (verbatim where different): `AGENTS.md` — its "Skills"
   section gains **"Authoring a skill"** (create in `agent-skills/`, never a vendor folder)
   and **"Adopt a skill"** (promote a vendor-authored skill into `agent-skills/`, then sync);
   the **"After Every Session"** ritual gains a **skills safety check** step + checklist line.
   `.agent/schema.md` notes it. `DECAY.md` / `REVIEW.md` unchanged.
2. **No data migration.** Existing skills/adapters untouched.
3. **Stamp** `.agent/version.md` → `version: 4.3.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: `AGENTS.md` re-synced (authoring convention + adopt safety-net + session-close check).

---

## Rung: 4.3.0 → 4.3.1 — skills-layer doc fixes (PATCH)

Wording/clarity only — surfaced by a fresh-agent test-drive of the session-close ritual. No
shape, data, or behavior change.

1. **Re-sync `AGENTS.md`** (verbatim where different): "Skills" → "Adopt a skill" no longer
   instructs a mid-ritual commit (stage the neutral skill for the session-end commit; the
   agent doesn't self-commit), and clarifies body normalization; the "After Every Session"
   skills safety check notes the adopt-before-log ordering. `DECAY.md` / `REVIEW.md` unchanged.
2. **Stamp** `.agent/version.md` → `version: 4.3.1`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
3. **Report**: `AGENTS.md` re-synced (adopt/commit + ordering + body clarifications).

---

## Rung: 4.3.1 → 4.3.2 — skill description hardening (PATCH)

Wording/clarity only — surfaced by a skill-lifecycle sanity check. Prevents two hard-to-spot
sync hazards: an adapter `description` drifting from the neutral skill, and a description with
special characters (e.g. `"`) producing invalid TOML / `.mdc`.

1. **Re-sync `AGENTS.md`** (verbatim where different): "Skills" → "Authoring a skill" now
   requires a **single-line, quote-free `description`**; the adapter recipe states the adapter
   `description` **mirrors the skill's verbatim** + an escape/quote fallback. `DECAY.md` /
   `REVIEW.md` unchanged.
2. **(If the target has skills)** re-run **"sync skill adapters"** so adapters pick up the
   verbatim description; if any skill `description` contains a `"`, rephrase it single-line and
   quote-free (or rely on the escape fallback). No committed change (adapters gitignored).
3. **Stamp** `.agent/version.md` → `version: 4.3.2`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: `AGENTS.md` re-synced; adapters re-synced if skills present.
