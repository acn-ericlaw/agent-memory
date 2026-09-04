#!/usr/bin/env bash
# Regression tests for the CI floors' changed-config secret-scan waiver filter (v4.39.2).
#
# Field origin (2026-09-04, Accenture/mercury-composable PR #318 — the first PR ever to
# exercise a `.agent/secret-scan-ignore` entry in that repo): when the LAST changed config
# file is waived, the filter loop's final command was `[ "$keep" = "1" ] && printf ...`,
# whose false test made the loop — and therefore the command substitution and the
# assignment — exit 1, aborting the whole step under `set -e` with no output at all.
# The fix is `if ... fi`, which returns 0 on a false condition.
#
# Two layers:
#   1. Static guard (any bash, incl. macOS 3.2): the buggy idiom is absent and the safe
#      form present in all three shipped floors.
#   2. Behavioral cases (bash >= 4 only — bash 3.2 cannot parse `case` inside `$(...)`,
#      matching the GitHub runner note in the field report; skipped with a notice
#      otherwise): the filter loop is extracted VERBATIM from each shipped file and run
#      under `set -e` against the motivating fixture plus its neighbors.
set -u

repo_root="$(CDPATH= cd "$(dirname "$0")/.." 2>/dev/null && pwd)" || exit 1
scratch="$(mktemp -d "${TMPDIR:-/tmp}/agent-memory-secret-waiver.XXXXXX")" || exit 1
trap 'rm -rf "$scratch"' EXIT

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

floors="
.github/workflows/agent-memory.yml
templates/.gitlab/agent-memory-ci.yml
templates/.azuredevops/agent-memory-ci.yml
"

# --- 1. static idiom guard -------------------------------------------------------------
for floor in $floors; do
  file="$repo_root/$floor"
  [ -f "$file" ] || fail "$floor is missing"
  if grep -qF '[ "$keep" = "1" ] && printf' "$file"; then
    fail "$floor still carries the test-and-act idiom that aborts under -e when the last file is waived"
  fi
  grep -qF 'if [ "$keep" = "1" ]; then printf' "$file" \
    || fail "$floor lost the waiver filter's safe if/fi form"
done
printf 'ok: static idiom guard (3 floors)\n'

# --- 2. behavioral cases (need bash >= 4, like the CI runners) --------------------------
BASH4=""
for cand in bash /opt/homebrew/bin/bash /usr/local/bin/bash /usr/bin/bash; do
  major="$(command "$cand" -c 'echo "${BASH_VERSINFO[0]}"' 2>/dev/null || echo 0)"
  if [ "${major:-0}" -ge 4 ]; then BASH4="$cand"; break; fi
done
if [ -z "$BASH4" ]; then
  printf 'SKIP: behavioral cases need bash >= 4 (bash 3.2 cannot parse the loop; CI runs them)\n'
  printf 'PASS: test_ci_secret_scan_waiver (static guard only)\n'
  exit 0
fi

# run_case <floor> <case-name> <cfgs-input> <expected-survivors>
run_case() {
  floor="$1"; name="$2"; input="$3"; expected="$4"
  case_dir="$scratch/$(printf '%s-%s' "$name" "$(basename "$floor")")"
  mkdir -p "$case_dir/.agent"
  printf '# audited fixture waiver\nwaived-file.properties\n' > "$case_dir/.agent/secret-scan-ignore"

  # the shipped loop, verbatim (dedented — shell is indentation-insensitive)
  awk '/cfgs="\$\(printf/ && /\| while /{grab=1} grab{print} grab && /done\)"/{exit}' "$repo_root/$floor" \
    | sed 's/^[[:space:]]*//' > "$case_dir/loop.sh"
  [ -s "$case_dir/loop.sh" ] || fail "could not extract the waiver filter loop from $floor"

  {
    printf 'set -e\n'
    printf 'cfgs="%s"\n' "$input"
    cat "$case_dir/loop.sh"
    printf 'printf "AFTER\\n%%s\\n" "$cfgs"\n'
  } > "$case_dir/run.sh"

  out="$(cd "$case_dir" && "$BASH4" run.sh 2>&1)" || fail "$floor/$name: script aborted under -e (exit $?): $out"
  case "$out" in AFTER*) ;; *) fail "$floor/$name: never reached the post-filter code: $out" ;; esac
  got="$(printf '%s\n' "$out" | sed '1d')"
  [ "$got" = "$expected" ] || fail "$floor/$name: survivors [$got] != expected [$expected]"
}

for floor in $floors; do
  # the motivating artifact: the ONLY changed config file is the waived one
  run_case "$floor" last-file-waived 'waived-file.properties' ''
  # neighbor: last file NOT waived — the scan list keeps it
  run_case "$floor" last-file-not-waived 'other.yml' 'other.yml'
  # ordering: waived then unwaived — survivor only
  run_case "$floor" waived-then-unwaived 'waived-file.properties
other.yml' 'other.yml'
  # ordering: unwaived then waived LAST — the trigger position in a multi-file list
  run_case "$floor" unwaived-then-waived-last 'other.yml
waived-file.properties' 'other.yml'
done
printf 'ok: behavioral cases (4 x 3 floors, %s)\n' "$BASH4"
printf 'PASS: test_ci_secret_scan_waiver\n'
