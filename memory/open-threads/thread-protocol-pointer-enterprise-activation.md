- [x] **(blueprint — SHIPPED v4.37.0 MINOR, 2026-08-21) Protocol behind a one-line root
  shim.** Root `AGENTS.md` (tool + template) became a 61-byte pointer to the canonical
  `memory/PROTOCOL.md` (dual-mode tool copy; target-only template), killing the ~20 KB
  auto-load tax; PRE-APPLY fail-closed gating protects customized roots (PR #24, eugenelim;
  3 review findings fixed pre-merge). Lesson: the consent artifact must agree with apply.
  Full detail: origin log + spec under `docs/specs/memory-protocol-pointer/` + the
  `4.36.0→4.37.0` rung. → serves: vision-agent-memory
  <!-- id: protocol-pointer-enterprise-activation | created: 2026-08-20 | last_used: 2026-08-22 | uses: 8 | tier: active | origin: 2026-08-20-204952 -->
