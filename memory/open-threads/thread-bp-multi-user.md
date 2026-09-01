- [ ] **(blueprint)** Multi-user concurrent contribution — mostly supported (shared
  committed `memory/`, multi-agent continuity, collision-safe session filenames); validate
  and harden for *simultaneous* contributors. → serves: vision-agent-memory
  Progress (v4.39.0, merge-scale layout): threads-as-files + archive union-merge +
  serialized reviews + derived last_session removed the structural conflict surfaces
  (docs/DESIGN-merge-scale.md). Remaining: live simultaneous-contributor validation
  in the field.
  <!-- id: bp-multi-user | created: 2026-06-15 | last_used: 2026-09-01 | uses: 7 | tier: active | origin: 2026-06-15-000531 -->
