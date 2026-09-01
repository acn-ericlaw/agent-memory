- [x] **Shipped v4.33.4 (PATCH) — reject non-empty `${…}` defaults in `[secret-material]`.**
  v4.33.3's placeholder exemption also trusted literal fallbacks; template forms stay safe
  while values with real-looking defaults flag without echo (46 mirror tests ×2). Full
  detail: origin log. → serves: vision-agent-memory
  <!-- id: secret-template-default-v4334 | created: 2026-08-14 | last_used: 2026-08-14 | uses: 3 | tier: archive-candidate | origin: 2026-08-14-003952 -->
