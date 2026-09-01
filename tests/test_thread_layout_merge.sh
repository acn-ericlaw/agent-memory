#!/usr/bin/env bash
# Contract tests for the merge-scale memory layout (v4.39.0).
#
# The layout claims three merge behaviors, pinned here with real git merges rather than
# asserted (the rehearsal pattern is absorbed from PR #27 — credit: Roland Heusser):
#   (1) parallel work on DIFFERENT threads cannot conflict — one file per thread;
#   (2) both sides editing the SAME thread file conflict when the hunks are
#       adjacent/overlapping — the MERGE.md Tier 2 human gate is load-bearing, so a
#       clean merge there would be a regression; 2b/2c pin the measured boundary
#       (v4.39.1): edits separated by an unchanged line merge cleanly keeping BOTH
#       sides, adjacent edits conflict;
#   (3) archive files union-merge via the committed `.gitattributes` (git-native
#       `merge=union`, no driver, no per-clone registration) — concurrent review
#       sweeps' appends keep both sides.
#
# Uses only temporary git repositories; no repository Git metadata is changed.
set -u

repo_root="$(CDPATH= cd "$(dirname "$0")/.." 2>/dev/null && pwd)" || exit 1
scratch="$(mktemp -d "${TMPDIR:-/tmp}/agent-memory-thread-layout.XXXXXX")" || exit 1
trap 'rm -rf "$scratch"' EXIT

fail() { printf 'FAIL: %s\n' "$1" >&2; exit 1; }

# A repo with the new layout: continuity (pointer note only), open-threads/, archive/,
# and the shipped .gitattributes (the union rule under test comes from the template).
make_repo() {
  case_dir="$scratch/$1"
  mkdir -p "$case_dir/memory/open-threads" "$case_dir/memory/archive"
  cp "$repo_root/templates/.gitattributes" "$case_dir/.gitattributes"
  printf '# Continuity — t\n\n## Project State\n\n- **project:** t\n\n## Open Threads\n\n> Threads live one per file in memory/open-threads/.\n' \
    > "$case_dir/memory/continuity.md"
  printf -- '- [ ] **Base thread.** exists on base\n  <!-- id: base-thread | created: 2026-09-01 | last_used: 2026-09-01 | uses: 1 | tier: working -->\n' \
    > "$case_dir/memory/open-threads/thread-base-thread.md"
  printf -- '# Archive Index\n\n- old-fact — an archived fact — faded — 2026-Q2.md\n' \
    > "$case_dir/memory/archive/INDEX.md"
  ( cd "$case_dir" || exit 1
    git init -q -b base . && git config user.email t@t && git config user.name t
    git add -A && git commit -q -m base )
}

thread_file() { printf -- '- [ ] **Thread %s.** work by %s\n  <!-- id: gap-%s | created: 2026-09-01 | last_used: 2026-09-01 | uses: 1 | tier: working -->\n' "$1" "$1" "$1"; }

# (1) Different threads: two branches each create their own thread file -> clean merge,
# both files survive, no markers anywhere.
make_repo different
( cd "$scratch/different" || exit 1
  git checkout -q -b A
  thread_file a > memory/open-threads/thread-gap-a.md
  git add -A && git commit -q -m A
  git checkout -q base && git checkout -q -b B
  thread_file b > memory/open-threads/thread-gap-b.md
  git add -A && git commit -q -m B
  git merge -q A >/dev/null 2>&1 ) || fail "different-threads: merge did not complete cleanly"
[ -f "$scratch/different/memory/open-threads/thread-gap-a.md" ] || fail "different-threads: lost A's thread"
[ -f "$scratch/different/memory/open-threads/thread-gap-b.md" ] || fail "different-threads: lost B's thread"
if grep -rq '^<<<<<<<' "$scratch/different/memory"; then fail "different-threads: conflict markers left behind"; fi

# (2) Same thread, both sides edit the body -> MUST conflict (Tier 2 human gate).
# A clean merge here would silently fork the thread — the regression this layout must never have.
make_repo same
( cd "$scratch/same" || exit 1
  git checkout -q -b A
  perl -pi -e 's/exists on base/REWRITTEN BY A/' memory/open-threads/thread-base-thread.md
  git commit -q -am A
  git checkout -q base && git checkout -q -b B
  perl -pi -e 's/exists on base/REWRITTEN BY B/' memory/open-threads/thread-base-thread.md
  git commit -q -am B )
if ( cd "$scratch/same" && git merge -q A >/dev/null 2>&1 ); then
  fail "same-thread: both-sides edit merged silently; expected a conflict (Tier 2 human gate)"
fi
grep -q '^<<<<<<<' "$scratch/same/memory/open-threads/thread-base-thread.md" \
  || fail "same-thread: expected conflict markers in the thread file"

# (2b) Same thread, SEPARATED edits (v4.39.1 precision — from an independent CoPilot
# assessment): git conflicts only on adjacent/overlapping hunks. Edits to the same thread
# file separated by unchanged lines merge cleanly with BOTH sides kept — documented
# behavior, not a bug (nothing is lost; consistency of the merged statements is the
# write-time contradiction check's job, and the pre-4.39.0 layout merged identically).
# This case pins the claim's honest boundary so the docs can never overstate it again.
make_repo separated
( cd "$scratch/separated" || exit 1
  printf -- '- [ ] **Sep thread.** line-one\n  body line-two\n  body line-three\n  body line-four\n  body line-five\n  <!-- id: sep-thread | created: 2026-09-01 | last_used: 2026-09-01 | uses: 1 | tier: working -->\n' \
    > memory/open-threads/thread-sep-thread.md
  git add -A && git commit -q -m seed
  git checkout -q -b A
  perl -pi -e 's/line-one/EDIT-BY-A/' memory/open-threads/thread-sep-thread.md
  git commit -q -am A
  git checkout -q -b B A~1
  perl -pi -e 's/line-five/EDIT-BY-B/' memory/open-threads/thread-sep-thread.md
  git commit -q -am B
  git merge -q A >/dev/null 2>&1 ) || fail "separated-edits: expected a CLEAN merge (both sides kept)"
grep -q 'EDIT-BY-A' "$scratch/separated/memory/open-threads/thread-sep-thread.md" || fail "separated-edits: lost A's edit"
grep -q 'EDIT-BY-B' "$scratch/separated/memory/open-threads/thread-sep-thread.md" || fail "separated-edits: lost B's edit"

# (2c) Same thread, ADJACENT lines — the measured conflict boundary: with no unchanged
# line between the edits, git must conflict (the Tier 2 gate engages here).
make_repo adjacent
( cd "$scratch/adjacent" || exit 1
  printf -- '- [ ] **Adj thread.** line-one\n  body line-two\n  body line-three\n  <!-- id: adj-thread | created: 2026-09-01 | last_used: 2026-09-01 | uses: 1 | tier: working -->\n' \
    > memory/open-threads/thread-adj-thread.md
  git add -A && git commit -q -m seed
  git checkout -q -b A
  perl -pi -e 's/line-two/EDIT-BY-A/' memory/open-threads/thread-adj-thread.md
  git commit -q -am A
  git checkout -q -b B A~1
  perl -pi -e 's/line-three/EDIT-BY-B/' memory/open-threads/thread-adj-thread.md
  git commit -q -am B )
if ( cd "$scratch/adjacent" && git merge -q A >/dev/null 2>&1 ); then
  fail "adjacent-edits: merged silently; adjacent same-thread edits must conflict"
fi

# (3) Archive union: both branches append a different line to INDEX.md at EOF ->
# merges cleanly via the template's `memory/archive/*.md merge=union`, keeping both.
make_repo archive
( cd "$scratch/archive" || exit 1
  git checkout -q -b A
  printf -- '- fact-a — swept by A — faded — 2026-Q3.md\n' >> memory/archive/INDEX.md
  git commit -q -am A
  git checkout -q base && git checkout -q -b B
  printf -- '- fact-b — swept by B — faded — 2026-Q3.md\n' >> memory/archive/INDEX.md
  git commit -q -am B
  git merge -q A >/dev/null 2>&1 ) || fail "archive-union: merge did not complete cleanly"
grep -q 'fact-a' "$scratch/archive/memory/archive/INDEX.md" || fail "archive-union: lost A's line"
grep -q 'fact-b' "$scratch/archive/memory/archive/INDEX.md" || fail "archive-union: lost B's line"
if grep -q '^<<<<<<<' "$scratch/archive/memory/archive/INDEX.md"; then fail "archive-union: markers left behind"; fi

# Mutation checks (a suite that cannot fail proves nothing): strip the union attribute
# and the archive append case must degrade to an ordinary conflict.
make_repo noattr
( cd "$scratch/noattr" || exit 1
  : > .gitattributes && git commit -q -am "drop attributes"
  git checkout -q -b A
  printf -- '- fact-a — swept by A — faded — 2026-Q3.md\n' >> memory/archive/INDEX.md
  git commit -q -am A
  git checkout -q base && git checkout -q -b B
  printf -- '- fact-b — swept by B — faded — 2026-Q3.md\n' >> memory/archive/INDEX.md
  git commit -q -am B )
if ( cd "$scratch/noattr" && git merge -q A >/dev/null 2>&1 ); then
  fail "mutation: without the union attribute the archive append should conflict"
fi

printf 'PASS: thread layout merge contract — different-threads clean, same-thread overlap conflicts, separated edits keep both, adjacent edits conflict, archive union (6 cases)\n'
