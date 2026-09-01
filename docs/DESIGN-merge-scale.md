# Design — Merge-scale memory: threads as files (v4.39.0)

> Design record for the merge-conflict reduction iteration. Serves the
> `bp-multi-user` Blueprint gap → `vision-agent-memory` ("multi-contributor by
> design"). Tool-only; read on demand. Origin: maintainer field reports of regular
> `continuity.md` merge conflicts as team adoption grew, plus PR #27's field
> artifact (two stacked branches, both appending an Open Thread and bumping
> `last_session`).

## Problem

`memory/continuity.md` is the one file every teammate edits on every branch, and its
`## Open Threads` section is where the churn concentrates: multi-line thread blocks
appended and edited at the same anchor collide constantly. `last_session` bumps on
nearly every session, so parallel branches almost always conflicted on it too. At
R&D scale this was an annoyance; at team scale it is a per-merge tax.

## Decision: structure over machinery

Two candidate shapes were evaluated against a maintainer preference for minimalist
design:

1. **A custom git merge driver** (PR #27) that auto-applies MERGE.md's Tier 1 rules
   (union the accreting sections, later-value the scalars). Rejected: verified
   against the branch, whole-file `--union` silently merges Tier 2 semantic clashes
   (both sides editing the *same* thread emerged as two checkbox lines sharing one
   footer — no conflict, no Contradiction, invisible to `memory-lint`), and dateless
   scalars (`status`) resolve as a direction-dependent silent winner-pick. Fixing
   that honestly needs a diff3 hunk classifier, at which point the driver stops
   being small — and it only runs on clones that registered it (`init.sh`), so merge
   behavior would silently differ per clone. The `[duplicate-state-key]` lint check
   is absorbed from the PR with credit; a scalars-only driver remains the pre-scoped
   follow-up if field pain persists.
2. **A structural layout change** — remove the conflict surface instead of resolving
   it. **Chosen**: no merge-time code, no per-clone registration, no partial-coverage
   mode; pure file layout, the same construction that already makes `sessions/`
   conflict-free.

## The shape

- **One thread, one file:** `memory/open-threads/thread-<id>.md`, where `<id>` is the
  thread's existing kebab fact id. File content is exactly the bullet block that
  previously sat in continuity — checkbox line, body, `serves:` trace, metadata
  footer. Nothing else. Migration is a verbatim cut-paste per thread.
- **Stable id filenames, not timestamps.** A timestamped delete-and-recreate scheme
  was considered (mirroring session logs) and rejected: session logs are immutable
  events, threads are mutable state. Delete+recreate converts a visible same-thread
  conflict into a silent fork (both branches recreate under different names, git
  merges cleanly, two divergent copies survive), churns filenames on every review
  metadata refresh, and divorces filename from fact identity. With stable names,
  parallel work on *different* threads cannot conflict (different files), and both
  sides editing the *same* thread conflicts per-file — which is MERGE.md Tier 2
  reaching a human, the required behavior, not a gap.
- **No index.** The directory is the index, exactly like `sessions/`: an index line
  per thread in continuity would recreate the add/add conflict, one line at a time.
  Discovery is `ls memory/open-threads/`; open vs closed is the checkbox in each
  file (`grep -l '^- \[ \]' memory/open-threads/` lists the open ones). The
  activation protocol lists the directory and reads unchecked threads — presence by
  protocol, at parity with when threads sat in the always-imported continuity.
- **`last_session` is dropped** from Project State: it is fully derivable (newest
  `sessions/` filename; the agent name is that log's `**Agent:**` header), and it was
  the most frequent scalar conflict. The multi-agent continuity check reads the
  newest log instead. Installed repos delete the line at upgrade (mechanical, safe).
- **Archive files union-merge:** `memory/archive/*.md merge=union` in
  `.gitattributes`. These are append-mostly cold storage; concurrent review sweeps
  appended at EOF and conflicted spuriously. Union is git-native (no driver). The
  one unsafe case — a reactivation's line removal resurrected by union — is exactly
  what the existing `[both]` / `[over-archived]` ERROR checks detect
  deterministically. Continuity and thread files never get union: there a conflict
  is signal.
- **Reviews serialize by protocol:** run from an up-to-date default branch, commit
  promptly — the metadata refresh touches many footers and must not run tangled
  with in-flight substantive edits.

## Lifecycle semantics (unchanged rules, new location)

Decay/pinning/supersession rules (`DECAY.md`) are location-independent: an unchecked
thread file is pinned; a checked one condenses to a 3–6-line stub and waits out
`archive_window`; the sweep *moves the file's block* to the quarter archive + INDEX
and deletes the file (`archive-fact` does this deterministically). `refresh-metadata`
rewrites footers in place — filenames never churn. New/Contradiction/Drift threads
are created as new files. Fact-id creation collisions across branches surface as
`[duplicate-id]` (new ERROR check), and `[thread-file]` pins the filename↔id
contract.

## What was deliberately deferred

- **Millisecond session filenames** — same-second add/add collisions across
  contributors are vanishingly rare, and `date -u +%3N` is not portable (BSD/macOS);
  a MERGE.md line covers the resolution (rename one file +1s).
- **A scalars-only merge driver** — pre-scoped in PR #27's close comment; build it
  only if scalar-bump conflicts persist in the field after this layout ships.
- **Splitting `status` further** — the schema already mandates a short status line;
  the fix is compliance, not new structure.
