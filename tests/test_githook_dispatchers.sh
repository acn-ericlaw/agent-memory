#!/usr/bin/env bash
# Focused contract tests for the pre-commit and post-commit fragment dispatchers.
# Uses only a temporary directory; no repository Git metadata is changed.
set -u

repo_root="$(CDPATH= cd "$(dirname "$0")/.." 2>/dev/null && pwd)" || exit 1
scratch="$(mktemp -d "${TMPDIR:-/tmp}/agent-memory-hook-dispatch.XXXXXX")" || exit 1
trap 'rm -rf "$scratch"' EXIT

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

make_fragment() {
  path="$1"
  label="$2"
  result="$3"
  printf '%s\n' \
    '#!/usr/bin/env bash' \
    "printf '$label:%s:%s\\n' \"\$1\" \"\$2\" >> \"\$HOOK_TEST_LOG\"" \
    "exit $result" > "$path"
  chmod +x "$path"
}

test_dispatcher() {
  hook="$1"
  case_dir="$scratch/$hook-case"
  fragment_dir="$case_dir/$hook.d"
  log="$case_dir/order.log"
  expected="$case_dir/expected.log"
  errors="$case_dir/errors.log"

  mkdir -p "$fragment_dir"
  cp "$repo_root/.githooks/$hook" "$case_dir/$hook"
  chmod +x "$case_dir/$hook"

  make_fragment "$fragment_dir/10-first" first 7
  make_fragment "$fragment_dir/20 second fragment" second 3
  make_fragment "$fragment_dir/90-last" last 0
  make_fragment "$fragment_dir/.05-hidden" hidden 5
  printf '%s\n' '#!/usr/bin/env bash' 'exit 6' > "$fragment_dir/15-not-executable"

  if HOOK_TEST_LOG="$log" "$case_dir/$hook" alpha "two words" 2> "$errors"; then
    result=0
  else
    result=$?
  fi

  [ "$result" -eq 7 ] || fail "$hook returned $result instead of its first failure (7)"
  printf '%s\n' \
    'first:alpha:two words' \
    'second:alpha:two words' \
    'last:alpha:two words' > "$expected"
  cmp -s "$expected" "$log" || fail "$hook order, filtering, or argument forwarding changed"
  grep -Fq "$hook: fragment 10-first failed with status 7" "$errors" \
    || fail "$hook did not identify the first failed fragment"
  grep -Fq "$hook: fragment 20 second fragment failed with status 3" "$errors" \
    || fail "$hook did not continue after a fragment failure"

  empty_dir="$scratch/$hook-empty"
  mkdir -p "$empty_dir"
  cp "$repo_root/.githooks/$hook" "$empty_dir/$hook"
  chmod +x "$empty_dir/$hook"
  "$empty_dir/$hook" || fail "$hook should succeed when its fragment directory is absent"
}

test_dispatcher pre-commit
test_dispatcher post-commit

printf 'PASS: pre-commit and post-commit dispatcher contracts\n'
