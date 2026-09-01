- [x] **Shipped v4.33.0 (MINOR) — session-log secret redaction: ritual rule +
  `[secret-material]` advisory.** From a client-side DLP incident (live OAuth secret in a
  committed session log): the redaction rule joined the after-session ritual and lint
  check 10 became the deterministic backstop (never echoes values; scans sessions +
  archive). Lesson: shared memory must be safe to share — a committed secret is exposed,
  rotate it. Full detail: origin log + the `4.32.1→4.33.0` rung.
  → serves: vision-agent-memory
  <!-- id: secret-redaction-lint-v4330 | created: 2026-08-13 | last_used: 2026-08-19 | uses: 9 | tier: archive-candidate | origin: 2026-08-13-222439 -->
