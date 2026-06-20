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
| 4.3.3 | Skills-layer description guidance (PATCH): `description` should be **concise** + trigger-phrase-rich (~1–2 sentences — matched within a small discovery budget, so long abstract paragraphs weaken activation); YAML `>`/`|` blocks are YAML-only, so the canonical value stays one logical line (it also mirrors into TOML) |
| 4.4.0 | Lightweight skills: per-session `AGENTS.md` keeps only the runtime baseline + a pointer; the adapter recipe + **sync**/**adopt**/**sanity-check** ops move to an on-demand installed `SKILLS.md`. The per-session "skills safety check" is **removed** (skill work is a conscious, on-demand action); upgrades do a read-only filename check that *recommends* sync |
| 4.5.0 | Kiro adapter: a 4th skills adapter target `.kiro/skills/<name>/SKILL.md` (Kiro follows the open Agent Skills standard — same shape as the Claude adapter); Kiro added to the Mode C detection table (steering/specs/skills). Kiro auto-reads root `AGENTS.md`, so the memory layer needs no pointer file |
| 4.5.1 | Skills-layer guidance (PATCH, from a Gemini CLI dogfood): the Gemini adapter is a **slash command** `/<name>` (explicit, not natural-language auto-matched) — NL routes through the baseline to the same skill; trigger semantics differ per vendor; and `sync skill adapters` must **never commit / recommend committing** the gitignored adapter dirs (only `agent-skills/` is shared) |
| 4.5.2 | Kiro hooks in Mode C (PATCH, from a Windows/Kiro enable): the `MIGRATE.md` Kiro protocol now handles `.kiro/hooks/*.kiro.hook` — preserved verbatim under `legacy/kiro/hooks/`, never converted/run. Human-gated commit hooks (like Kiro's) align with agent-memory; only an *unprompted* auto-commit/push is surfaced as an Open Thread. README gains a bootstrap edge-case note ("Start from `AGENTS.md`" when an enterprise IDE self-bootstraps) |
| 4.6.0 | Vendor-neutral **commit attribution**: `AGENTS.md` extends "identify yourself" (already true for session logs) to commits — deliberate, human-initiated, with a `Co-Authored-By: <agent>` trailer. Encodes once in the shared layer what Claude Code does automatically and Kiro needed a per-machine hook for; soft guidance, a no-op where the runtime already does it |
| 4.7.0 | **Lightweight mode** for memory-neutral tasks (from a Kiro enablement): a trivial task (no new fact/decision/thread/state change) writes a **one-line "lite" session log** (`## Memory References` → `(none)`) and skips the full template / fact-footers / continuity edits. Ledger stays continuous; the review handles it as a normal reference-free session. Scales the per-session ceremony to the actual memory impact |
| 4.7.1 | Lightweight mode keyed to **file-change, not "trivial"** (a judgment call both AI and human misjudge): **read-only** sessions (no file changes) write **no log**; **any file change** (even one line) writes at least a **lite log** (never skipped on a "felt trivial" call); a memory-relevant event → full ritual |
| 4.8.0 | Review **self-verify guard** (from a Copilot review that over-archived recent facts): a new `REVIEW.md` step greps the last `archive_window` sessions for each about-to-be-archived id — any hit ⇒ the `sessions_since_last_used` count was wrong, keep the fact — and confirms no id lives in both `continuity.md` and the archive. Replaces a hand-counted judgment with a checkable signal for the riskiest operation |
| 4.9.0 | **`memory-lint`** — a portable, optional verifier skill (`agent-skills/memory-lint/` + `scripts/memory-lint.py`, Python 3 stdlib) that runs the decay-integrity checks *deterministically* (id-in-both-places, archived-but-recently-referenced, overdue advisory, supersession links). Moves the arithmetic off the LLM; `REVIEW.md` step 6 points to it. Caught a real over-archival on first run. The tool never runs it (`no-build-step-agent-run`) — agent/human/CI-invoked |
| 4.10.0 | **Fresh-context second opinion** — a skill pair (`second-opinion` + `apply-critique`): snapshot the current task (derived from `continuity.md` + recent sessions, never a parallel state file) for a clean-memory reviewer (any vendor / fresh session) behind a **security advisory**, then apply the returned critique through a **bounded, validated, human-gated** loop (build/tests + `memory-lint`; critique is advisory). Snapshots/critiques live in gitignored `review-scratch/`. ENABLE and the upgrade ladder now **install** the built-in skills (this pair + `memory-lint`, which the review ritual relies on). Folds the "AIF" idea into skills + VBDI |
| 4.10.1 | **`memory-lint` bug fix:** its Memory-References parser is now **line-anchored** (`(?m)^## +Memory References[ \t]*$`) instead of `find("## Memory References")`, so a session log that *quotes* the heading in prose no longer trips a false `over-archived` error. Script-only; no description/shape change |
| 4.10.2 | **Fresh-context-review critique fixes (PATCH):** `memory-lint`'s `FOOTER_RE` now binds to a single line so an *unclosed* footer can't silently swallow the file and misparse decay metadata; the install protocol (`ENABLE.md` §5i) **warns before overwriting a locally-modified built-in** instead of silently clobbering it; the `upgrades-additive` invariant text carries its tool-managed-built-ins exception inline; and `second-opinion` gains a same-vendor-vs-different-vendor caveat. No description/shape change |
| 4.10.3 | **Lightweight-mode wording fix (PATCH):** `AGENTS.md` now keys the session-log test to whether a **tracked** file changed (the *objective* test is the **git diff**, not any filesystem write), and explicitly exempts runs whose only writes are **gitignored, regenerated artifacts** (`sync skill adapters`, `review-scratch/`, the compiled lint artifact) → **no log**. Aligns the lightweight-mode note with what `SKILLS.md` already states (sync "touches no committed file"); prevents a spurious lite log after every adapter sync. Wording-only |
| 4.10.4 | **`memory-lint` nested list fix (PATCH):** hardened the verifier script to handle deeply-nested lists correctly. `pinned_open_threads` now checks indentation level so a parent Open Thread's pinned state isn't dropped by a standard sub-bullet. |
| 4.11.0 | **`memory-lint` Node runtime (MINOR):** the deterministic verifier now ships in **both** Python (`memory-lint.py`) and Node (`memory-lint.mjs`, Node ≥ 18, built-ins only) at feature + output parity, so a machine with only Node still runs the script instead of a hand count. `SKILL.md` documents both commands as interchangeable; a shared test contract (`test_memory_lint.mjs` ↔ `.py`) holds them equivalent. Additive — no dispatcher, no installer (the agent picks the runtime) |
| 4.11.1 | **Review step-6 archival guard hardened (PATCH):** `REVIEW.md` step 6 now defines a "use" as a `## Memory References` entry, not a prose mention — `memory-lint` is the preferred check (Memory-References-only, immune to the trap) and the by-hand fallback only counts in-block hits. Fixes an archival livelock (`ot-review-step6-prose`) where a review naming a fact while deferring it re-armed the guard forever. Doc + tests only; the verifier script was already correct (`memref_ids` line-anchored since 4.10.1) |
| 4.12.0 | **Enforced adapter sync at enable + upgrade (MINOR):** ENABLE and **every** Mode B re-enable (upgrade or already-up-to-date) now **run** `sync skill adapters` instead of the read-only "recommend, don't run" check — so a skill's vendor-native adapters are actually materialized (closing the gap where a skill predating a new adapter target, e.g. Kiro, or a fresh clone/pull, was left without working native skills). Idempotent, writes only gitignored files (no committed change, no version bump, no session log); `no-build-step-agent-run` holds (the agent runs it during a human-invoked enable/upgrade). The per-session path still never touches skills; content-drift realignment is still the on-demand `skill sanity check` |
| 4.12.1 | **`memory-lint` dangling-link cross-file fix (PATCH):** `load_repo` now pools footers from other `memory/*.md` files (e.g. `vision.md`), excluding `continuity.md`/`decay-policy.md`, into an `extra` set used **only** for supersession-link resolution in `check_dangling` — so a fact superseded by a target whose footer lives in `vision.md` no longer false-flags as `[dangling]`. Both runtimes (`.py` + `.mjs`) fixed at parity; regression test added to both suites (`.mjs` now also exports `load_repo`/`check_dangling` to enable it). Found dogfooding `~/sandbox/simple-proxy`; ported back from there |
| 4.13.0 | **Tool-provided (system) skills marked + upstream advisory (MINOR):** the three shipped built-ins carry `provenance: agent-memory-builtin` in their `SKILL.md` frontmatter (+ a body banner), so a target's AI recognizes a system skill **at edit time** — and `SKILLS.md` (new "Tool-provided (system) skills" section) tells it to **fork** a local variant or **upstream** a genuine fix to the agent-memory project (issue in production; maintainer advisory pre-release) rather than strand it. `ENABLE.md` §5i's warn-before-overwrite extended with the same upstream advice. Closes the gap that let the simple-proxy `memory-lint` fix nearly get lost. Adapters unchanged (mirror only name+description) |
| 4.14.0 | **Optional Architecture Decision Record log (MINOR):** documents an **optional** human-facing `docs/ADR.md` decision log at the VBDI **Design** altitude — one durable architecture decision per entry (Status/Date/Abstract/Rationale-with-consequences), newest-first, `Proposed → Accepted → Superseded/Deprecated`, **never deleted** (mirrors `DECAY.md` §9). Map-don't-duplicate: live constraints stay in `continuity.md`, the ADR carries the *why*, cross-linked by `formalizes:` ↔ a visible `(ADR-NNNN)` tag in the invariant title (a human pointer, not an agent read-cue). Read **on demand** — **not** in the per-session read path (zero default token cost). Documented in `.agent/schema.md` + `AGENTS.md`; **not auto-installed** into targets (adopt on demand) |


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
either branch (incl. "up to date"):  also run `sync skill adapters` (below) — idempotent, gitignored-only.
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

## Skills adapter sync (every enable + Mode B re-enable) — enforced, v4.12.0

Independent of the version ladder: skill adapters are gitignored, so they don't travel with a
clone/pull, and a rung that adds a new adapter target (e.g. Kiro in 4.5.0) leaves older skills'
adapters incomplete. So on **any** enable and **any** Mode B re-enable — including "already up to
date" — **run `sync skill adapters`** (see `SKILLS.md`) as the closing skills step: for each
`agent-skills/<name>/`, (re)write the four vendor adapters (`.claude/skills/<name>/SKILL.md`,
`.gemini/commands/<name>.toml`, `.cursor/rules/<name>.mdc`, `.kiro/skills/<name>/SKILL.md`) and
**prune** orphaned *generated* adapters (one whose `agent-skills/<name>/` no longer exists; never
touch other files in a vendor dir).

This is safe to run unconditionally because it is **idempotent** and writes **only gitignored**
files — never `agent-skills/`, never a committed file. So it is **not a version change and needs no
session log** (the lightweight-mode rule: a run whose only writes are gitignored, regenerated
artifacts). It does not violate `no-build-step-agent-run`: the **agent** runs it during a
human-invoked enable/upgrade — there is no daemon and no per-session automation. Report the counts:
*"synced N skill(s) → M adapters (gitignored — do not commit; only `agent-skills/` is shared); pruned
K orphan(s)."* If there are no skills, it is a no-op.

This **replaces the former read-only "recommend, don't run" check** (≤ v4.11.1): enable and upgrade
are deliberate, human-invoked moments, so *materializing* adapters then — rather than printing advice
the user must act on before the skills work natively — is correct. The **per-session** path still
never touches skills; deliberate **content-drift** realignment (a description that no longer mirrors
its skill) is still the heavyweight, on-demand `skill sanity check` in `SKILLS.md`.

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

---

## Rung: 4.3.2 → 4.3.3 — skill description guidance (PATCH)

Wording/clarity only — a discovery-budget refinement (a `description` is a model-matched
activation signal read within a small budget). No shape, data, or behavior change.

1. **Re-sync `AGENTS.md`** (verbatim where different): "Authoring a skill" now asks for a
   **concise**, trigger-phrase-rich `description` (~1–2 sentences, not a long abstract
   paragraph); the recipe notes YAML `>`/`|` blocks are YAML-only (the description also lands
   in a TOML adapter), so the canonical value is one logical line. `DECAY.md`/`REVIEW.md` unchanged.
2. **(If the target has skills)** optionally tighten any over-long `description` and re-run
   **"sync skill adapters"**. No committed change (adapters gitignored).
3. **Stamp** `.agent/version.md` → `version: 4.3.3`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: `AGENTS.md` re-synced; descriptions tightened if any were over-long.

---

## Rung: 4.3.3 → 4.4.0 — lightweight skills (recipe → on-demand `SKILLS.md`)

Additive relocation + a deliberate simplification: skill work is a *conscious, occasional*
developer action, so it leaves the per-session path. No skill data changes.

1. **Install `SKILLS.md`** at the target root (copied verbatim from this tool's root, like
   `DECAY.md`/`REVIEW.md`). It holds the authoring convention, the adapter recipe, and the
   **sync** / **adopt** / **sanity-check** operations — read on demand, not per-session.
2. **Re-sync `AGENTS.md`** (verbatim where different): the "Skills" section is now just the
   runtime baseline + a pointer to `SKILLS.md`; the verbose recipe/ops are gone from it. The
   **"After Every Session" ritual no longer has a skills safety-check step** (removed — see
   the standing skills-adapter sync this doc runs at every Mode B re-enable instead).
3. **No skill regeneration in this rung.** The standing skills-adapter sync (above) handles
   adapters — since **v4.12.0** it *runs* `sync skill adapters` (idempotent, gitignored-only) on
   every Mode B re-enable rather than only recommending it.
4. **Stamp** `.agent/version.md` → `version: 4.4.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
5. **Report**: `SKILLS.md` installed; `AGENTS.md` slimmed (per-session skills footprint cut;
   no per-session skills check); skills adapter check result.

---

## Rung: 4.4.0 → 4.5.0 — Kiro skills adapter (+ Mode C detection)

Additive: a 4th adapter target plus Kiro in the migration detection table. No skill data
changes; a repo with no skills (or no Kiro) works exactly as before. Design:
`docs/DESIGN-skills-layer.md`.

1. **Re-sync the generic docs** (copy verbatim where different): `SKILLS.md` (the adapter
   recipe now lists a **Kiro** target — `.kiro/skills/<name>/SKILL.md`, same shape as the
   Claude adapter, since Kiro follows the open Agent Skills standard), `AGENTS.md` (root +
   template: the adapter list now includes `.kiro/skills/`). `DECAY.md` / `REVIEW.md` unchanged.
2. **`.gitignore` — no entry change needed.** `.kiro/` is already in the v3.1.0 managed block
   (it is the adapter target for `.kiro/skills/`). Optionally refresh the managed-block comment
   to name `.kiro/skills/` among the adapters (cosmetic only).
3. **No skill regeneration in this rung.** If the target has skills but no `.kiro/skills/`
   adapters, the standing skills-adapter sync (above) materializes them — since **v4.12.0** it
   *runs* `sync skill adapters` (which writes the Kiro adapter too) on every Mode B re-enable,
   rather than only recommending it.
4. **Stamp** `.agent/version.md` → `version: 4.5.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
5. **Report**: docs re-synced; Kiro adapter now in the recipe; skills-adapter sync result
   (the `.kiro/skills/` adapters are (re)written by the standing sync).

---

## Rung: 4.5.0 → 4.5.1 — skills-layer guidance (PATCH, from a Gemini CLI dogfood)

Wording/guidance only; no shape change, no skill data changes.

1. **Re-sync the generic docs** (copy verbatim where different): `SKILLS.md` (the Gemini adapter
   is now noted as a **slash command `/<name>`** — explicit, not NL-auto-matched; a
   "trigger semantics differ per vendor" note; and a **never-commit-the-adapters** guard on the
   `sync skill adapters` operation), `AGENTS.md` (root + template: the adapter line now says
   "never commit them"). `DECAY.md` / `REVIEW.md` unchanged.
2. **No skill regeneration; no `.gitignore` change.** Adapters and `agent-skills/` are untouched;
   the managed block already ignores the adapter dirs.
3. **Stamp** `.agent/version.md` → `version: 4.5.1`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: docs re-synced (Gemini = slash command; adapters are never committed).

---

## Rung: 4.5.1 → 4.5.2 — Kiro hooks in Mode C (PATCH, from a Windows/Kiro enable)

Additive migration sub-case + a usage note; no shape change, no skill data changes.

1. **Re-sync the generic docs** (copy verbatim where different): `MIGRATE.md` (the Kiro protocol
   now has a **Hooks** sub-case — `.kiro/hooks/*.kiro.hook` are preserved verbatim under
   `legacy/kiro/hooks/`, never converted/run; human-gated commit hooks like Kiro's align — only an
   *unprompted* auto-commit/push is surfaced as an Open Thread, never disabled). `AGENTS.md` / `SKILLS.md`
   / `DECAY.md` / `REVIEW.md` unchanged.
2. **No skill regeneration; no `.gitignore` change.** `.kiro/` is already ignored.
3. **Stamp** `.agent/version.md` → `version: 4.5.2`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: Kiro migration now handles hooks (preserve, never run).

---

## Rung: 4.5.2 → 4.6.0 — vendor-neutral commit attribution (MINOR)

Additive convention; no shape change, no skill data changes. Makes any vendor add the deliberate,
self-identifying commit trailer that Claude Code does automatically and Kiro needed a hook for.

1. **Re-sync `AGENTS.md`** (root + template, verbatim where different): the "After Every Session"
   step 4 + checklist now carry the **commit-attribution convention** — *"commits are deliberate
   and human-initiated; identify yourself (e.g. a `Co-Authored-By: <agent>` trailer) the way you do
   in session logs."* Soft guidance, a no-op for runtimes that already do it. `SKILLS.md` /
   `DECAY.md` / `REVIEW.md` unchanged.
2. **No skill regeneration; no `.gitignore` change.**
3. **Stamp** `.agent/version.md` → `version: 4.6.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: `AGENTS.md` re-synced; commit-attribution convention now applies to every vendor.

---

## Rung: 4.6.0 → 4.7.0 — lightweight mode for memory-neutral tasks (MINOR)

Additive ritual carve-out; no shape change, no skill/memory data changes. From a Kiro enablement
finding (per-session write ceremony is heavy for trivial tasks).

1. **Re-sync `AGENTS.md`** (root + template, verbatim where different): "After Every Session" now
   has a **Lightweight mode** note — for a **memory-neutral** task (no new/changed fact, no
   decision, no Open Thread touched, no project-state change) write a **one-line "lite" session
   log** (`## Memory References` → `(none)`) and skip the full template / fact-footers / continuity
   edits. The ledger stays continuous; the review handles a lite log as a normal session with no
   references. `SKILLS.md` / `DECAY.md` / `REVIEW.md` unchanged.
2. **No skill regeneration; no `.gitignore` change.**
3. **Stamp** `.agent/version.md` → `version: 4.7.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: `AGENTS.md` re-synced; lightweight mode available for trivial tasks.

---

## Rung: 4.7.0 → 4.7.1 — lightweight mode keyed to file-change, not "trivial" (PATCH)

Refinement of the v4.7.0 carve-out; no shape change. "Trivial" is a judgment call (both AI and
human misjudge), so the skip is keyed to the **objective** "did a file change?" test.

1. **Re-sync `AGENTS.md`** (root + template, verbatim where different): the "Lightweight mode" note
   is now three-tier — **read-only** (no file changes) → **no session log**; **any file change** with
   no memory-relevant event → a **one-line lite log** (never skipped on a "felt trivial" call);
   **memory-relevant event** → full ritual. `SKILLS.md` / `DECAY.md` / `REVIEW.md` unchanged.
2. **No skill regeneration; no `.gitignore` change.**
3. **Stamp** `.agent/version.md` → `version: 4.7.1`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: `AGENTS.md` re-synced; lightweight mode now keyed to file-change (read-only = no log,
   any change = at least a lite log).

---

## Rung: 4.7.1 → 4.8.0 — review self-verify guard against decay miscounts (MINOR)

Additive review step; no shape change, no data changes. From a Copilot CLI review that
over-archived recent active facts (miscounted `sessions_since_last_used`).

1. **Re-sync `REVIEW.md`** (verbatim where different): new **step 6 "Verify archival"** before
   stamping — for each fact about to be archived as faded, `grep` the last `archive_window` session
   files for its id; any hit ⇒ keep it (count was wrong), don't archive; confirm no id lives in both
   `continuity.md` and the archive. Adds an `Archive-verify:` line to the review-summary format.
   `AGENTS.md` / `SKILLS.md` / `DECAY.md` unchanged.
2. **No skill regeneration; no `.gitignore` change.** No memory data changes (this is a review
   *process* guard for future reviews).
3. **Stamp** `.agent/version.md` → `version: 4.8.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: `REVIEW.md` re-synced; reviews now self-verify archival before stamping.

---

## Rung: 4.8.0 → 4.9.0 — `memory-lint` deterministic verifier skill (MINOR)

Additive: a portable verifier skill + a `REVIEW.md` pointer to it. The markdown guard (v4.8.0) is
still the in-ritual default; this adds the deterministic, CI-able version.

1. **Re-sync `REVIEW.md`** (verbatim where different): step 6 now points to the `memory-lint` skill
   as the recommended deterministic version of the verify ("let the script count"). The pointer is
   guarded with "if present," so it's a no-op where the skill isn't installed. `AGENTS.md` /
   `SKILLS.md` / `DECAY.md` unchanged.
2. **The skill itself is in the tool's `agent-skills/memory-lint/`** (neutral `SKILL.md` +
   `scripts/memory-lint.py`). It is **not** auto-installed into targets by this rung — a target that
   wants it can adopt/copy the skill (it's portable, Python 3 stdlib, optional). Auto-install into
   targets is a deliberate future option (it would add a script to every enabled repo).
3. **No skill regeneration; no `.gitignore` change.**
4. **Stamp** `.agent/version.md` → `version: 4.9.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
5. **Report**: `REVIEW.md` re-synced (points to `memory-lint`); the verifier skill is available.

---

## Rung: 4.9.0 → 4.10.0 — fresh-context second opinion + install the built-in skills (MINOR)

Additive: installs the built-in skills into the repo + a gitignored scratch dir. Folds the
"AIF" brainstorming idea into the skills layer + VBDI (`docs/DESIGN-fresh-context-review.md`) —
net-new is the security advisory on export, the handoff ritual, and the critique shape;
everything else reuses memory.

1. **Install the built-in skills** into the repo's `agent-skills/` — copy `second-opinion/`,
   `apply-critique/`, **and `memory-lint/`** (with its `scripts/`) verbatim from this tool's
   root, then regenerate adapters (Step 5h recipe). `memory-lint` is installed here too: v4.9.0
   left it tool-local, but the **review ritual relies on it**, so the 4.10.0 upgrade brings it
   into the target. Idempotent — overwrite these built-ins (they are ours); never touch
   unrelated `agent-skills/` content (`never-pick-a-winner`). **Tool-managed copies:** because
   upgrade overwrites them, the user must **not** customize an installed built-in — fork under a
   **new skill name** for a variant. The overwrite is scoped to these three, so
   `upgrades-additive` holds for all other `agent-skills/`. **Before overwriting an already-installed
   built-in, apply `ENABLE.md` §5i's modified-built-in check** — if the target's copy was locally
   changed, warn the human and let them decide rather than silently clobbering it.
2. **`review-scratch/`** — add to the repo `.gitignore` (personal, per-machine
   snapshots/critiques; never committed). `second-opinion` writes a `review-scratch/README.md`
   marking the folder personal on first run.
3. **Re-sync `.agent/schema.md`** (verbatim where different): adds the `review-scratch/`
   section. `templates/.gitignore` gains the `review-scratch/` entry. `AGENTS.md` / `SKILLS.md`
   / `DECAY.md` / `REVIEW.md` unchanged — the critique→repair loop reuses the existing ritual.
4. **Stamp** `.agent/version.md` → `version: 4.10.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
5. **Report**: built-in skills installed (`second-opinion` + `apply-critique` + `memory-lint`)
   with adapters regenerated; `review-scratch/` gitignored.

---

## Rung: 4.10.0 → 4.10.1 — `memory-lint` line-anchor bug fix (PATCH)

Script-only fix to a built-in skill. No memory-file shape change, no description change, so
adapters are untouched. Only matters for a repo that has `memory-lint` installed (v4.10.0+, or
adopted earlier).

1. **Re-copy `agent-skills/memory-lint/scripts/memory-lint.py`** verbatim from this tool's root,
   overwriting the installed copy (it is a tool-managed built-in — `upgrades-additive` holds; the
   overwrite is scoped to this tool-owned file). The fix: `memref_ids()` anchors the heading to a
   real line (`(?m)^## +Memory References[ \t]*$`) and bounds at the next line-anchored heading,
   so a session log that quotes the heading in prose no longer yields a false `over-archived`
   error. `SKILL.md` unchanged → **no adapter regeneration**.
2. **Ignore Python bytecode caches** — append `__pycache__/` + `*.py[cod]` to the repo's
   `.gitignore` (create-or-append, add-only, idempotent — same mechanism as the v3.1.0 propagation).
   `memory-lint` generates these on run; the `.py` source stays tracked.
3. **Nothing else changes** — `AGENTS.md` / `SKILLS.md` / `DECAY.md` / `REVIEW.md` / `.agent/schema.md`
   untouched. If `memory-lint` isn't installed, step 1 is a no-op (step 2's cache rule is harmless either way).
4. **Stamp** `.agent/version.md` → `version: 4.10.1`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
5. **Report**: `memory-lint` updated (false-positive on inline heading mentions fixed); Python-cache
   `.gitignore` rule added.

---

## Rung: 4.10.1 → 4.10.2 — fresh-context-review critique fixes (PATCH)

Refinements from a fresh-context review of the v4.10.x line (a clean-vendor reviewer). Two
built-in skills get re-copied and the install protocol gains a safety check. Only matters for a
repo that has the built-ins installed (v4.10.0+).

1. **Re-copy two built-ins** verbatim from this tool's root, overwriting the installed copies
   (tool-managed built-ins — `upgrades-additive` holds; overwrite scoped to tool-owned files):
   - `agent-skills/memory-lint/scripts/memory-lint.py` — `FOOTER_RE` is now bound to a single line
     (`[^\n]`, no `re.S`), so an *unclosed* footer can no longer let the field capture swallow the
     rest of the file up to a stray `-->` and silently misparse decay metadata. Same theme as
     v4.10.1: the verifier must not be fooled by malformed input.
   - `agent-skills/second-opinion/SKILL.md` — adds a "same-vendor vs. different-vendor" caveat under
     *Notes* (a same-vendor clean session tests the *mechanism*; a different vendor adds *epistemic
     diversity* for high-stakes milestones). **Body only — description unchanged → no adapter
     regeneration.**
2. **Warn-before-overwrite check** — `ENABLE.md` §5i (and this rung's step 1, and the 4.10.0 rung)
   now say: before overwriting an *already-installed* built-in, diff it against the source; if it was
   locally modified, **warn the human and let them decide** rather than silently clobbering. Makes
   the tool-managed-copies contract checked, not convention-only. Agent-run at the human's direction
   (`no-build-step-agent-run`); no-op on a fresh enable. **Apply that check before step 1's re-copy.**
3. **Nothing else changes** — `AGENTS.md` / `SKILLS.md` / `DECAY.md` / `REVIEW.md` / `.agent/schema.md`
   untouched. `apply-critique` and `memory-lint`'s `SKILL.md` are unchanged. If the built-ins aren't
   installed, steps 1–2 are no-ops.
4. **Stamp** `.agent/version.md` → `version: 4.10.2`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
5. **Report**: `memory-lint` hardened (unclosed-footer guard); `second-opinion` caveat added; install
   now warns before overwriting a locally-modified built-in.

## Rung: 4.10.2 → 4.10.3 — lightweight-mode wording fix (PATCH)

Wording-only clarification to the `AGENTS.md` lightweight-mode note. No file shape, no skill, no
script changes — only the installed `AGENTS.md` text.

1. **Re-key the lightweight-mode test to a *tracked* change.** In the target's installed `AGENTS.md`
   ("After Every Session" → lightweight-mode block), the objective test is now the **git diff over
   tracked files**, not "did any file change":
   - the opening line reads "whether a *tracked* file changed (the *objective* test is the git diff,
     not any filesystem write)";
   - the **Read-only** tier now also covers "a run whose only writes are gitignored, regenerated
     artifacts" — naming `sync skill adapters`, `review-scratch/` snapshots, and the compiled lint
     artifact — as **no session log**;
   - the second tier reads "**A tracked file changed** but produced no memory-relevant event";
   - the closing line reads "anything that touched a *tracked* file."
   This aligns the note with what `SKILLS.md` already states — `sync skill adapters` "touches no
   committed file… not a version change" — so an adapter sync (or any gitignored-only write) no
   longer implies a spurious lite log. **If the target's `AGENTS.md` was locally modified, warn the
   human and let them decide** (same warn-before-overwrite courtesy as the built-ins).
2. **Nothing else changes** — `SKILLS.md` / `DECAY.md` / `REVIEW.md` / `.agent/schema.md` / templates'
   memory files / skills / scripts untouched.
3. **Stamp** `.agent/version.md` → `version: 4.10.3`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: lightweight-mode test re-keyed to tracked changes (git diff); gitignored regenerated
   artifacts (adapter sync, `review-scratch/`, lint artifact) are explicitly no-log.

## Rung: 4.10.3 → 4.10.4 — memory-lint nested list fix (PATCH)

Updates the bundled `memory-lint` script to correctly parse deeply-nested lists in continuity.md Open Threads. No memory-file shape or procedural changes.

1. **Re-copy the `memory-lint` script.** Overwrite the target's `agent-skills/memory-lint/scripts/memory-lint.py` and its new test file with the ones from the tool's `agent-skills/memory-lint/scripts/` directory. **If the target's script was locally modified, WARN the human first** ("The built-in memory-lint skill has been updated in v4.10.4, but you have local modifications...") and ask before overwriting (this enforces the built-in exception to the `upgrades-additive` invariant).
2. **Re-copy the memory-lint `SKILL.md`.** It now contains a note about running the test harness. Same warn-before-overwrite rule applies.
3. **Stamp** `.agent/version.md` → `version: 4.10.4`, `last_upgraded: <today>`, preserving `enabled_with` and `mode`.
4. **Report**: `memory-lint` hardened to correctly preserve the pinned state of Open Threads containing deeply-nested sub-items.

## Rung: 4.10.4 → 4.11.0 — memory-lint Node runtime (MINOR)

Adds a Node implementation of the `memory-lint` verifier alongside the Python one, so a target machine that has Node but not Python still gets the deterministic check. Additive only — no memory-file shape or procedural changes; the Python script and command are unchanged.

1. **Copy the two new `memory-lint` files** into the target's `agent-skills/memory-lint/scripts/`: `memory-lint.mjs` (the Node verifier) and `test_memory_lint.mjs` (its tests). These are net-new; nothing is overwritten. (If a target somehow already has local copies, the built-in **warn-before-overwrite** rule from 4.10.2 applies.)
2. **Re-copy the memory-lint `SKILL.md`.** It now documents both runtimes as interchangeable and the cross-runtime test command. Same warn-before-overwrite rule applies.
3. **Verify parity (optional but recommended):** if both runtimes are present, `python3 …/memory-lint.py` and `node …/memory-lint.mjs` should produce identical output; `node --test …/test_memory_lint.mjs` should pass.
4. **Stamp** `.agent/version.md` → `version: 4.11.0`, `last_upgraded: <today>`, preserving `enabled_with` and `mode`.
5. **Report**: `memory-lint` now runs under Node as well as Python — deterministic decay checks no longer require a Python install.

## Rung: 4.11.0 → 4.11.1 — review step-6 archival guard hardened (PATCH)

Fixes a wording bug in the review ritual's archival-verify (step 6): a raw full-text grep of recent sessions counted prose mentions (e.g. a prior review summary naming a fact while deferring it) as "uses," creating an archival livelock. No memory-file shape change; the verifier script is unchanged (it was already correct).

1. **Re-copy `REVIEW.md`** to the target's repo root. Step 6 now defines a "use" as a `## Memory References` entry, makes `memory-lint` the preferred check, and scopes the by-hand fallback to in-block hits.
2. **Re-copy the memory-lint test files** into `agent-skills/memory-lint/scripts/`: `test_memory_lint.py` and `test_memory_lint.mjs` now include `memref_ids` regression tests (prose/review-summary mention is not counted; block bounded at next heading). `memory-lint.py`/`.mjs` themselves are unchanged. Warn-before-overwrite rule (4.10.2) applies if locally modified.
3. **Stamp** `.agent/version.md` → `version: 4.11.1`, `last_upgraded: <today>`, preserving `enabled_with` and `mode`.
4. **Report**: review step-6 archival guard no longer livelocks on prose mentions; a "use" is a Memory-References entry, counted deterministically by `memory-lint`.

## Rung: 4.11.1 → 4.12.0 — enforce `sync skill adapters` at enable + upgrade (MINOR)

Behavior change (additive, backward-compatible): the standing skills-adapter step stops being a
read-only "recommend, don't run" check and instead **runs** `sync skill adapters`. Closes the loose
end where, after an upgrade, a skill's vendor-native adapters could be missing — a skill that predates
a new adapter target (e.g. Kiro, added in 4.5.0), or any fresh clone/pull (adapters are gitignored and
don't travel) — so subsequent work that relies on native skill auto-trigger was blocked until the user
manually ran sync. No memory-file shape change; safe because the sync is idempotent and writes only
gitignored files.

1. **Re-sync the generic docs** (copy verbatim where different): `SKILLS.md` (its "Lightweight by
   design" note now says enable + every Mode B re-enable *run* the idempotent sync, not a read-only
   recommend; the `sync skill adapters` operation notes it's auto-run then). `AGENTS.md` / `DECAY.md`
   / `REVIEW.md` are unchanged (the per-session path still never touches skills, and `AGENTS.md`
   already only points to `SKILLS.md`).
2. **Run `sync skill adapters`** now as the closing skills step (this is the new enforced behavior,
   applied to this very upgrade): for each `agent-skills/<name>/`, (re)write the four vendor adapters
   and prune orphaned generated adapters. Idempotent; writes only gitignored files (no committed
   change, no session log). If the target has no skills, it's a no-op.
3. **Stamp** `.agent/version.md` → `version: 4.12.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: enable/upgrade now materialize skill adapters automatically; *"synced N skill(s) → M
   adapters (gitignored — do not commit; only `agent-skills/` is shared); pruned K orphan(s)."*

## Rung: 4.12.0 → 4.12.1 — `memory-lint` dangling-link cross-file fix (PATCH)

Script fix to a built-in: `check_dangling` resolved supersession links against `continuity.md` +
archive footers only, so a fact superseded by a target whose footer lives in another `memory/*.md`
(notably `vision.md`) false-flagged as `[dangling] … which has no footer anywhere`. Only matters for a
repo that has `memory-lint` installed (v4.10.0+).

1. **Re-copy the `memory-lint` scripts** verbatim from this tool's root, overwriting the installed
   copies (tool-managed built-ins; `upgrades-additive` holds — overwrite scoped to tool-owned files):
   `agent-skills/memory-lint/scripts/memory-lint.py` and `memory-lint.mjs`. The fix: `load_repo` now
   pools footers from other `memory/*.md` files (excluding `continuity.md`/`decay-policy.md`) into an
   `extra` set used **only** for supersession-link resolution in `check_dangling` — never counted as
   continuity/archive facts. `.mjs` additionally **exports** `load_repo` + `check_dangling` (additive,
   test-enabling; the `.py` already exposed them). **If the target's scripts were locally modified,
   WARN the human first** (the 4.10.2 warn-before-overwrite rule) and let them decide.
2. **Re-copy the test files** into `agent-skills/memory-lint/scripts/`: `test_memory_lint.py` and
   `test_memory_lint.mjs` now include a cross-file dangling regression test (a fact superseded by a
   `vision.md` fact must not warn; a genuinely missing target still warns). Same warn-before-overwrite
   rule. `SKILL.md` unchanged → **no adapter regeneration**.
3. **Stamp** `.agent/version.md` → `version: 4.12.1`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: `memory-lint` no longer false-flags a supersession target whose footer lives in
   `vision.md` (or another `memory/*.md`); both runtimes at parity; both suites 8/8.

## Rung: 4.12.1 → 4.13.0 — tool-provided (system) skills: marker + upstream advisory (MINOR)

Additive: marks the shipped built-ins as tool-provided so a target's AI recognizes a *system* skill at
edit time and routes a change correctly (fork a variant, or upstream a genuine fix), instead of silently
editing it and having the change overwritten on the next upgrade. No memory-file shape change; adapters
are untouched (they mirror only `name` + `description`).

1. **Re-copy the three built-ins' `SKILL.md`** verbatim from this tool's root, overwriting the installed
   copies (tool-managed built-ins — `upgrades-additive` holds; overwrite scoped to tool-owned files):
   `agent-skills/{memory-lint,second-opinion,apply-critique}/SKILL.md`. The expected delta is the new
   **`provenance: agent-memory-builtin`** frontmatter field + a one-line body banner. **Warn-before-overwrite
   (4.10.2) applies:** if a target's `SKILL.md` differs *beyond* this marker addition (a local
   modification), stop, show the diff, and — because such a change is often a genuine fix — **advise
   upstreaming it to the agent-memory project** (issue in production; maintainer pre-release) in addition
   to the keep/take choice. Scripts/tests are unchanged in this rung → no re-copy needed there.
2. **Re-sync the generic docs** (copy verbatim where different): `SKILLS.md` (new "Tool-provided (system)
   skills" section — the marker + the fork-or-upstream edit-time advisory), `AGENTS.md` (root + template:
   the one-line pointer), `.agent/schema.md` (the optional `provenance` field). `DECAY.md` / `REVIEW.md`
   unchanged.
3. **No adapter regeneration** — `name`/`description` are unchanged, so existing adapters still point
   correctly (adapters never carried `provenance`).
4. **Stamp** `.agent/version.md` → `version: 4.13.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
5. **Report**: built-ins now marked `provenance: agent-memory-builtin`; editing a system skill prompts
   fork-or-upstream; the upgrade warn-before-overwrite also advises upstreaming.

## Rung: 4.13.0 → 4.14.0 — optional Architecture Decision Record log (MINOR)

Additive and **documentation-only**: introduces an **optional** human-facing `docs/ADR.md`
decision log at the VBDI **Design** altitude. No memory-file shape change; adapters, scripts,
`DECAY.md`/`REVIEW.md` rules, and the per-session read path are untouched. **Nothing is
auto-created in the target** — a team adopts an ADR log only if it wants one.

1. **Re-sync the generic docs** (copy verbatim where different): `.agent/schema.md` (new
   optional `docs/ADR.md` section), `AGENTS.md` (root + template: the one-line "Design altitude
   may keep an optional `docs/ADR.md`, read on demand, not per-session" note), `DECAY.md` §12
   (the *Design* primitive now names the optional ADR log + its supersede/deprecate-never-delete
   lifecycle). `REVIEW.md` unchanged.
2. **Do not create `docs/ADR.md`** in the target. If the team wants one, they author it by hand
   following `.agent/schema.md` — seeding it (optionally) from their `## Architectural Invariants`,
   cross-linking `formalizes:` on the ADR ↔ a visible `(ADR-NNNN)` tag in the invariant title (a
   human pointer, not an agent read-cue). This repo's own `docs/ADR.md` is the worked reference.
3. **Stamp** `.agent/version.md` → `version: 4.14.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: an optional `docs/ADR.md` Architecture Decision Record log is now documented
   (Design-altitude, human-facing, on-demand — not in the per-session read path); no file was
   created; adopt on demand.
