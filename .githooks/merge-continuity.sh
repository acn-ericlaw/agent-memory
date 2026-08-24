#!/usr/bin/env bash
# agent-memory — custom git merge driver for memory/continuity.md.
#
# Registered per-clone by .githooks/init.sh, selected by `.gitattributes`:
#     memory/continuity.md merge=agent-memory-continuity
#
# It applies MERGE.md's own Tier 1 rules, both of them, instead of only the first:
#
#   Additive -> UNION.  The accreting sections (Open Threads, Key Decisions, Conventions,
#                       Architectural Invariants) are independent bullets. Keep both sides'.
#   Scalar   -> LATER.  `## Project State` holds one value per key. Two branches will usually
#                       both have bumped `last_session`, because it changes every session --
#                       so union alone would leave both lines, in an order nobody chose.
#
# A plain `merge=union` gets the first rule right and the second wrong. This gets both, which
# is why it exists rather than the one-line attribute.
#
# Not registered? Git falls back to a normal three-way merge and you get an ordinary conflict --
# exactly the behaviour before this driver existed. Safe to ship ahead of every clone running
# init.sh: the worst case is the status quo, never a wrong merge.
#
# Usage (git calls it): merge-continuity.sh %O %A %B
#   %O ancestor   %A ours (also the OUTPUT file)   %B theirs
set -euo pipefail

ancestor="$1"; ours="$2"; theirs="$3"
merged="$(mktemp)"; deduped="$(mktemp)"
trap 'rm -f "$merged" "$deduped"' EXIT

# (1) Union: keep both sides of every conflicting hunk. Never drops a line, so it cannot lose a
# fact -- which is the failure the memory layer exists to prevent.
git merge-file --union -p "$ours" "$ancestor" "$theirs" > "$merged" || true

# (2) Collapse duplicated scalars in `## Project State` to the later value. ISO dates compare
# correctly as plain strings, so no date parsing is needed. A value with no leading ISO date
# (`(none yet)`) sorts below any real date, which is the intent: a real check beats "never ran".
awk '
  function keyof(line,   m) {
    if (match(line, /^-[ \t]+\*\*[a-z_]+:\*\*/)) {
      m = substr(line, RSTART, RLENGTH); gsub(/^-[ \t]+\*\*|:\*\*$/, "", m); return m
    }
    return ""
  }
  function stamp(line,   v) { v = ""; if (match(line, /[0-9]{4}-[0-9]{2}-[0-9]{2}/)) v = substr(line, RSTART, RLENGTH); return v }
  NR == FNR {
    if ($0 ~ /^## /) { instate = ($0 ~ /^## Project State[ \t]*$/); next }
    if (!instate) next
    k = keyof($0); if (k == "") next
    if (!(k in best) || stamp($0) > stamp(best[k])) best[k] = $0
    next
  }
  {
    if ($0 ~ /^## /) { out_state = ($0 ~ /^## Project State[ \t]*$/); print; next }
    if (!out_state) { print; next }
    k = keyof($0)
    if (k == "") { print; next }
    if (k in done) next            # a later duplicate of a key already emitted -- drop it
    done[k] = 1; print best[k]     # emit the winner in the position of the first occurrence
  }
' "$merged" "$merged" > "$deduped"

cp "$deduped" "$ours"

# Exit 0 = merged cleanly. Union leaves no conflict markers, so there is nothing to report.
exit 0
