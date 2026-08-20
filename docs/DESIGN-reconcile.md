# Design — Target-State Reconcile (v4.35.0)

> Why enable/upgrade became declarative convergence, what the manifest and the reconcile
> helper are, and where the judgment boundary sits. Tool-side design record (sibling to
> `DESIGN-ritual-triggers.md`); not installed into targets.

## The problem — O(steps) and O(rungs)

A greenfield field case (2026-08-19): a fresh Mode A enable of a nearly-empty AI-hackathon
monorepo took **over ten minutes**. Nothing was wrong with the repo or the agent — the
cost was structural:

- `ENABLE.md` had grown to ~1,000 lines the agent had to ingest before acting, and it
  prescribed the install imperatively, file by file: ~60 files / ~600 KB flow through
  read→fill→write tool calls, even though most are verbatim copies that never needed to
  enter the model's context at all.
- `UPGRADE.md` had grown to 80 rungs, and Mode B walked `installed → current` one rung at
  a time — **O(rungs-behind)** — re-deriving the current state stepwise when a direct
  diff against the final state visits each file once.
- Both costs grow monotonically with the tool's own release velocity. The faster the
  flywheel spins, the slower every enable and upgrade gets.

The giveaway that the fix was already latent in the design: rungs were **required to be
idempotent** ("check whether it is already present and skip") — that *is* reconciliation
semantics, executed one historical version at a time — and `UPGRADE.md` already carried a
proto-manifest (the "Source of truth for re-synced files" table, four rows, incomplete).
The standing `ot-mode-b-automation-backlog` thread had prescribed the boundary years of
rungs earlier: *script the mechanical parts, leave the merges to the agent.*

## The model

**Classify every unit of enable/upgrade work by what it fundamentally is:**

1. **Mechanical convergence (~80% of wall-clock)** — "this file must equal that source" /
   "these entries must exist in this managed block." Declarative; a script's job.
2. **One-time generation** — analysis-derived seeding (instructions, continuity, vision,
   smoke-test, bootstraps with placeholders). Judgment; happens once at enable; never
   touched again by machinery.
3. **Semantic migrations** — version-gated data/judgment steps a file-sync cannot perform
   (metadata backfill, vision bootstrap gating, knob merges that preserve tuned values,
   secret triage, waiver drops). Rare: 14 of 80 rungs carry one.

Three artifacts encode the classification:

- **`MANIFEST.md`** — the declarative target state. One row per installed artifact:
  `Target | Source | Policy | Forge | Attrs`. Six policies: `verbatim` (tool-owned,
  byte-identical, re-copied on drift), `verbatim-dir` (the built-in skills), `seed-copy`
  (install-if-absent, never overwritten — user content accumulates there), `sentinel-merge`
  (managed blocks in user-owned files, add-only + de-duplicated), `seed-generate`
  (agent-authored, reported when missing, never inspected when present), `stamp` (the
  version manifest — written only by the agent, as the closing step). Plus the **Semantic
  steps** table: the ladder's non-mechanical migrations, each gated `Below` a version and
  pointing at its rung for full detail.
- **`scripts/reconcile.py` / `.mjs`** — byte-parity twins (the `memory-lint` pattern; 25
  mirror tests each). Dry-run by default; `--apply` performs the mechanical policies in
  one pass; `--check-manifest` is the release-time lockstep gate (every source exists,
  every file under `templates/`, `.githooks/`, and the built-in skill dirs is reachable
  from a row). Pure stdlib, no subprocesses: forge and hook state are read from
  `.git/config` directly, and everything that needs `git` to *run* (hooksPath activation,
  `--renormalize`) is emitted as a work-list item instead.
- **`ENABLE.md` — restructured, not rewritten.** A "Reconcile Core" section defines the
  operation; Steps 5–7 tag their mechanical parts `[reconcile-covered]` and keep their
  full text as the behavior spec and the no-runtime fallback. Mode A = consent → analysis
  → reconcile → generation → verify. Mode B = reconcile → semantic steps → stamp. Mode C
  is unchanged and reconciles **only after** migration (originals must reach `legacy/`
  before any verbatim row could re-copy over a vendor file).

## The judgment boundary (what the script must never do)

The helper deliberately cannot: write `.agent/version.md` (an early stamp would mask an
unfinished upgrade — the stamp is the agent's closing act), touch an existing `seed-copy`
or `seed-generate` file, edit a pre-existing `.gitlab-ci.yml` (user CI is wired by the
agent, add-only, per Step 6's stage-check rules), delete anything, or write outside the
target (path-realpath guard; it also refuses to run against the tool checkout itself).
Consent stays where it was: the dry-run report *is* the informed-consent artifact, shown
before `--apply`.

Drift on `verbatim` rows is the one place mechanics and judgment meet: on an older target
drift is expected staleness and re-copy is the fix, but it can also be a local
customization. The dry-run lists every drifted file *before* apply so the §5i
warn-before-clobber arbitration can run — which makes the tool-managed-copies contract
*checked* on every reconcile rather than remembered. The first live probe proved the
detection value immediately: a production repo showed 11 managed `.gitignore` entries
that accumulated across template versions and that **no rung had ever back-filled** —
invisible for months under the ladder, one `merge` line under reconcile.

## What it buys

- **Mode A:** ~50 mechanical tool calls collapse into one script run (seconds); the
  remaining wall-clock is the honest judgment surface (analysis, ~8 seeded files, the
  vision gate, verify) plus one stamp.
- **Mode B:** O(diff) instead of O(rungs). A 4.14.1 → current upgrade stops being 44
  rung walks and becomes one reconcile + the handful of semantic rows in range + stamp.
  Verified live: a 4.34.1 target's dry-run reproduced its pending rung *exactly*
  (memory-lint files stale, waiver-drop semantic step, stamp) — derived mechanically.
- **De-drift:** targets that silently diverged (half-applied upgrades, stale managed
  blocks, hand-edited protocol docs) become visible on every run.
- **Release honesty:** `--check-manifest` mechanizes the lockstep arithmetic
  (mechanize-arithmetic-not-judgment); a release that forgets the manifest fails its own
  checklist.

## Rejected alternatives

- **Per-version content hashes** (to distinguish "stale at vN" from "customized"):
  a hash table per release is real maintenance surface for marginal gain — git history
  in the target plus the drift report gives the agent the same signal. Rejected.
- **Scripting the `.gitlab-ci.yml` include wiring:** line-level YAML surgery on a user's
  CI file is exactly the kind of mutation the tooling doctrine forbids
  (tooling-advisory-never-mutates); the stage-check hazard (a custom `stages:` list
  without `test` invalidating the whole pipeline) needs eyes. Stays agent work.
- **Auto-stamping after apply:** conditional stamping ("stamp only if no semantic steps
  remain") reintroduces ordering coupling; a uniform "the agent stamps last" rule is
  simpler and self-documenting. Rejected conditional, kept uniform.
- **Full Mode B automation:** the original backlog framing — rejected then and now for
  the same reason: semantic merges (preserve tuned knobs, arbitration, redaction triage)
  are judgment. The manifest absorbs the arithmetic; the rungs keep the judgment.

## Honest limits

- Byte comparison assumes both checkouts normalize line endings the same way; on a mixed
  CRLF setup a false `drifted` is possible (re-copy is harmless — it converges to the
  tool's bytes; `.gitattributes` hardening keeps the executable surface LF regardless).
- The helper reads `.git/config` textually; exotic setups (worktree `.git` files, no
  `origin`) degrade to `forge: unknown` + a verify-by-hand work item — never a wrong
  silent action. `--forge` overrides detection.
- Semantic steps remain prose executed by an agent — reconcile shrinks their number per
  upgrade (usually to one or two) but does not mechanize them. That is the design, not a
  gap: the boundary is judgment vs. arithmetic.
- The manifest is one more lockstep surface. `--check-manifest` guards the file↔tree
  seam; the Semantic-steps↔rung seam is guarded by the release checklist (a human-gated
  classification per release).
