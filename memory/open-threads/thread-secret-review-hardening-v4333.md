- [x] **Shipped v4.33.3 (PATCH) — security-review hardening for `[secret-material]`.** A
  fresh-context review's four gaps fixed (real strict gate in CI wrappers; key-scoped enum
  exemption; quoted/header/embedded forms flag; Mode C redaction triage); a pre-tag
  live-target probe caught 2 template-pattern FPs the review missed. Lesson: always probe
  the live target, not just suites. Full detail: origin log. → serves: vision-agent-memory
  <!-- id: secret-review-hardening-v4333 | created: 2026-08-13 | last_used: 2026-08-14 | uses: 5 | tier: archive-candidate | origin: 2026-08-13-235301 -->
