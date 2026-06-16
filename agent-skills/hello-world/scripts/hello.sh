#!/bin/sh
# Bundled helper for the hello-world skill — an AGENT-INVOKED helper, never run by the
# tool itself (the `no-build-step-agent-run` invariant). Portable POSIX sh, no dependencies.
name="${1:-world}"
printf 'Hello, %s! 👋 — from the agent-memory portable skills layer.\n' "$name"
printf 'Local time: %s\n' "$(date '+%Y-%m-%d %H:%M:%S %Z')"
printf 'UTC time:   %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
printf 'Reminder: agent-memory records ALL session logs in UTC (persist-time). Local time is shown here for convenience only.\n'
