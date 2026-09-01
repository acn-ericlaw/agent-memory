- [x] **Hardened `memory-lint` test fixtures against repo secret-scanner FPs (no release
  bump).** Suites construct shape-constrained dummy secrets at runtime instead of
  committing signatures; full coverage retained (46/46 ×2). Lesson: security tooling must
  not make its own repository noisy to enterprise scanners. Full detail: origin log.
  → serves: vision-agent-memory
  <!-- id: secret-test-fixtures-env | created: 2026-08-14 | last_used: 2026-08-26 | uses: 3 | tier: active | origin: 2026-08-14-011037 -->
