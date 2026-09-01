- [x] **(blueprint — SHIPPED v4.35.0 MINOR, 2026-08-20) Target-state reconcile — enable/upgrade
  in O(diff), not O(steps/rungs).** From the >10-min AI-hackathon enable field report:
  `MANIFEST.md` declares the target state; `scripts/reconcile.py`/`.mjs` (byte-parity twins)
  converge a repo against it — dry-run consent artifact, one mechanical `--apply`, judgment
  stays agent-owned. Pre-ship adversarial review fixed 2 blockers (silent downgrade; mjs
  symlink escape). Lesson: mechanize arithmetic, never judgment. Full detail: origin log +
  the `4.34.2→4.35.0` rung + `docs/DESIGN-reconcile.md`. → serves: vision-agent-memory
  <!-- id: bp-reconcile-target-state | created: 2026-08-20 | last_used: 2026-08-22 | uses: 4 | tier: active | supersedes: ot-mode-b-automation-backlog | origin: 2026-08-20-223624 -->
