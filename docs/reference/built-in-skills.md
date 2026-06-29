# Built-in Skills

Seven skills are installed into every enabled repo, marked `provenance: agent-memory-builtin`
and tool-managed (overwritten on upgrade — [fork or upstream](../guides/author-a-skill.md#editing-a-built-in)
to customize). They sort along the **judgment-vs-arithmetic** boundary: the deterministic
moves are mechanized; the judgment stays with the agent.

| Skill | Side of the boundary |
|---|---|
| [`memory-lint`](#memory-lint) | arithmetic — read-only |
| [`refresh-metadata`](#refresh-metadata) | arithmetic |
| [`archive-fact`](#archive-fact) | arithmetic |
| [`sync-adapters`](#sync-adapters) | arithmetic |
| [`harvest-knowledge`](#harvest-knowledge) | judgment-assisted |
| [`second-opinion`](#second-opinion) | judgment-assisted |
| [`apply-critique`](#apply-critique) | judgment-assisted |

A `hello-world` demo skill also ships in the tool's own repo but is **not** installed into
targets.

---

## memory-lint

The deterministic integrity verifier the review ritual relies on. Ships in **both Python and
Node** at output parity, so it runs on a node-only box too. Nine checks:

1. duplicate facts (`[both]`)
2. over-archived (`[over-archived]`)
3. overdue archival (`[overdue]`)
4. dangling supersession links (`[dangling]`)
5. date-only session filenames (`[date-only-session]`)
6. empty/malformed version manifest (`[version-manifest]`)
7. leftover VCS merge-conflict markers (`[conflict-marker]`)
8. review cadence + size (`[review-overdue]` / `[continuity-bloat]`)
9. stale metadata — stored tier ≠ recomputed tier (`[stale-metadata]`)

```bash
python agent-skills/memory-lint/scripts/memory-lint.py      # or
node   agent-skills/memory-lint/scripts/memory-lint.mjs
```

Read-only — it **verifies**, it never mutates. Errors fail CI; advisories warn.

## refresh-metadata

Executes the review's deterministic re-tier (REVIEW.md steps 2–3): recomputes every fact's
`last_used` / `uses` / `tier` from the `## Memory References` across `memory/sessions/` and
writes the footers back (read into memory, write once). Pure arithmetic — `core` / `superseded`
and never-referenced facts are untouched; it clamps at `archive-candidate` (it **never
archives** — that's `archive-fact` plus the agent's judgment); pinned threads keep their tier.
Python *or* Node, `--dry-run`, idempotent.

## archive-fact

Performs the archive *move* safely, given fact id(s) the agent has **decided** to retire. It
extracts each block (bullet through its footer), **appends** it to the quarter archive +
`INDEX.md`, and rewrites `continuity.md` without it — reading the whole file into memory and
writing once, so **truncation is structurally impossible**. Guards (refuse, exit 1): id with
no footer, id already archived, or a move that would empty continuity. All-or-nothing;
`--dry-run` to preview. It never decides *what* to archive (`never-pick-a-winner`).

## sync-adapters

Regenerates the six vendor adapters from each neutral `SKILL.md`, pruning orphaned generated
adapters (signature-guarded — never deletes a hand-authored file). Ships in **bash, Node, and
Python** at byte-identical output parity; the bash runtime needs no install and is preferred.

```bash
bash agent-skills/sync-adapters/scripts/sync-adapters.sh --dry-run
```

## harvest-knowledge

Re-scans the repo's human-authored documentation (recursive `docs/` trees + a root sweep for
ADRs, decision logs, design specs, roadmaps) and distils **durable** facts into the neutral
`memory/` layer **additively**: map-don't-mirror, check-existing-first (a re-run never
duplicates), conflicts → a Contradiction thread, genuine replacements → supersession. Scoped
incrementally by a `last_harvest` marker. Not a vendor `/init` — the output goes to `memory/`,
never a vendor steering file.

## second-opinion

Distils a compact snapshot **from** `continuity.md` + recent session logs (never a parallel
state file) and, behind a **security advisory** you must acknowledge, hands it to a reviewer
with *clean memory* — a fresh session or a different vendor that didn't live the work. The
reviewer is a **hypothesis generator, not an authority**.

## apply-critique

Feeds a returned critique through a **bounded, validated, human-gated** loop: a few scoped
fixes → build/tests + `memory-lint` → an applied-vs-rejected summary. Deterministic checks and
a human gate the result — the lesson baked in after a clean-context reviewer once over-archived
still-referenced facts.

---

!!! info "Zero overhead by default"
    Installed ≠ run. The built-ins sit in `agent-skills/` until an agent's task matches one's
    `description` (or you invoke it explicitly).
