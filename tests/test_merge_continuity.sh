#!/usr/bin/env bash
# Contract tests for the memory/continuity.md merge driver (.githooks/merge-continuity.sh).
#
# The driver applies MERGE.md's two Tier 1 rules: the accreting sections UNION, and the
# `## Project State` scalars take the LATER value. Each rule is asserted separately, plus the
# combined case, the merge-order symmetry, and the un-registered fallback -- because the whole
# design rests on that fallback being an ordinary conflict rather than a wrong merge.
#
# Uses only temporary git repositories; no repository Git metadata is changed.
set -u

repo_root="$(CDPATH= cd "$(dirname "$0")/.." 2>/dev/null && pwd)" || exit 1
driver="$repo_root/.githooks/merge-continuity.sh"
scratch="$(mktemp -d "${TMPDIR:-/tmp}/agent-memory-merge-continuity.XXXXXX")" || exit 1
trap 'rm -rf "$scratch"' EXIT

fail() { printf 'FAIL: %s\n' "$1" >&2; exit 1; }

# A repo holding the real continuity template, with the driver registered unless $1 = noregister.
make_repo() {
  case_dir="$scratch/$1"; mode="${2:-register}"
  mkdir -p "$case_dir/memory"
  cp "$repo_root/templates/memory/continuity.md" "$case_dir/memory/continuity.md"
  ( cd "$case_dir" || exit 1
    git init -q -b base . && git config user.email t@t && git config user.name t
    printf 'memory/continuity.md merge=agent-memory-continuity\n' > .gitattributes
    if [ "$mode" = register ]; then
      git config merge.agent-memory-continuity.name "test"
      git config merge.agent-memory-continuity.driver "$driver %O %A %B"
    fi
    git add -A && git commit -q -m base )
}

# Rewrite the scalar and/or append a thread, then commit on a branch off base.
branch_with() {
  case_dir="$scratch/$1"; branch="$2"; session="$3"; thread="$4"
  ( cd "$case_dir" || exit 1
    git checkout -q base && git checkout -q -b "$branch"
    [ -n "$session" ] && perl -pi -e "s/^- \\*\\*last_session:\\*\\*.*/- **last_session:** $session/" memory/continuity.md
    [ -n "$thread" ] && perl -pi -e "s/^## Open Threads\$/## Open Threads\n\n- [ ] thread $thread/" memory/continuity.md
    git commit -q -am "$branch" )
}

# `grep -c` already prints 0 when nothing matches -- it just exits non-zero doing it, so a
# `|| printf 0` fallback would append a SECOND zero and every comparison against 0 would fail.
count() { grep -c "$1" "$scratch/$2/memory/continuity.md" 2>/dev/null; }

# (1) Additive -> UNION. Two branches each append a thread; both must survive.
make_repo union
branch_with union A "" A
branch_with union B "" B
( cd "$scratch/union" && git checkout -q B && git merge -q A >/dev/null 2>&1 ) \
  || fail "union: merge did not complete cleanly"
[ "$(count '^- \[ \] thread ' union)" = 2 ] || fail "union: expected both threads, got $(count '^- \[ \] thread ' union)"
[ "$(count '^<<<<<<<' union)" = 0 ] || fail "union: conflict markers left behind"

# (2) Scalar -> LATER. Two branches each bump last_session; one line, the later value.
make_repo scalar
branch_with scalar A "2026-08-26 | agent: A" ""
branch_with scalar B "2026-08-20 | agent: B" ""
( cd "$scratch/scalar" && git checkout -q B && git merge -q A >/dev/null 2>&1 ) \
  || fail "scalar: merge did not complete cleanly"
[ "$(count 'last_session' scalar)" = 1 ] || fail "scalar: expected one last_session, got $(count 'last_session' scalar)"
grep -q '2026-08-26' "$scratch/scalar/memory/continuity.md" || fail "scalar: kept the earlier value"

# (3) Merge order must not change the winner.
make_repo order
branch_with order A "2026-08-26 | agent: A" ""
branch_with order B "2026-08-20 | agent: B" ""
( cd "$scratch/order" && git checkout -q A && git merge -q B >/dev/null 2>&1 ) \
  || fail "order: merge did not complete cleanly"
grep -q '2026-08-26' "$scratch/order/memory/continuity.md" || fail "order: reverse merge picked a different winner"

# (4) Both rules at once -- the real shape of a parallel-branch conflict.
make_repo both
branch_with both A "2026-08-26 | agent: A" A
branch_with both B "2026-08-20 | agent: B" B
( cd "$scratch/both" && git checkout -q B && git merge -q A >/dev/null 2>&1 ) \
  || fail "both: merge did not complete cleanly"
[ "$(count '^- \[ \] thread ' both)" = 2 ] || fail "both: lost a thread"
[ "$(count 'last_session' both)" = 1 ] || fail "both: duplicated the scalar"
grep -q '2026-08-26' "$scratch/both/memory/continuity.md" || fail "both: kept the earlier value"

# (5) A real date beats "(none yet)". The base must carry a real date first -- the template's
# own default for last_review IS "(none yet)", so setting it on a branch would be a no-op and
# the case would never diverge.
make_repo none
( cd "$scratch/none" || exit 1
  perl -pi -e 's/^- \*\*last_review:\*\*.*/- **last_review:** 2026-08-01/' memory/continuity.md
  git commit -q -am "seed a real date" ) || fail "none-yet: could not seed the base"
review_branch() {
  ( cd "$scratch/none" || exit 1
    git checkout -q base && git checkout -q -b "$1"
    perl -pi -e "s/^- \*\*last_review:\*\*.*/- **last_review:** $2/" memory/continuity.md
    git commit -q -am "$1" )
}
review_branch A "2026-08-25" || fail "none-yet: branch A did not commit"
review_branch B "(none yet)" || fail "none-yet: branch B did not commit"
( cd "$scratch/none" && git checkout -q B && git merge -q A >/dev/null 2>&1 ) \
  || fail "none-yet: merge did not complete cleanly"
grep -q 'last_review:\*\* 2026-08-25' "$scratch/none/memory/continuity.md" \
  || fail "none-yet: '(none yet)' beat a real date"

# (6) THE LOAD-BEARING ONE. An unregistered driver must degrade to an ordinary conflict --
# the behaviour before any of this existed. If this ever silently "succeeds", the attribute is
# no longer safe to ship ahead of clones running init.sh.
make_repo fallback noregister
branch_with fallback A "2026-08-26 | agent: A" ""
branch_with fallback B "2026-08-20 | agent: B" ""
if ( cd "$scratch/fallback" && git checkout -q B && git merge -q A >/dev/null 2>&1 ); then
  fail "fallback: unregistered driver merged silently; expected an ordinary conflict"
fi
[ "$(count '^<<<<<<<' fallback)" -ge 1 ] || fail "fallback: expected conflict markers"

printf 'PASS: continuity merge driver — union, later-scalar, order-symmetry, fallback (6 cases)\n'
