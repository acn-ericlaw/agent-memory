- [x] **Shipped v4.39.2 (PATCH) — CI secret-scan waiver: silent abort on waived last file.**
  Field report (mercury-composable PR #318, 2026-09-04 — first-ever waiver use there): a
  waived LAST changed config file made the filter loop's trailing `[ ... ] && printf` fail
  the substitution's assignment, killing the step under `set -e` with zero output. One-line
  `if ... fi` fix in all three forge floors; class sweep clean (pre-commit guard already
  `if/else`); `tests/test_ci_secret_scan_waiver.sh` pins 4 cases per floor verbatim,
  red-verified. Lesson: never end a `-e`-governed loop/substitution with bare test-and-act;
  the bug class fires on a feature's *first legitimate use*. Detail: the 4.39.1→4.39.2 rung.
  → serves: vision-agent-memory (via bp-multi-user)
  <!-- id: secret-scan-waiver-abort-v4392 | created: 2026-09-04 | last_used: 2026-09-04 | uses: 1 | tier: working | origin: 2026-09-04-184835 -->
