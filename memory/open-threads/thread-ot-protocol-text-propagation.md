- [ ] **Protocol-text propagation is a per-release obligation, not a mechanism.**
  `memory/PROTOCOL.md` is `seed-copy`, so an installed protocol is never re-copied — deliberate
  (the v4.37.0 rung merges the old root's local directives into it, and a re-copy could drop
  them irrecoverably), but it ends the automatic propagation the old `verbatim` `AGENTS.md` hub
  had, and ~half of recent releases edited protocol text. Now stated in `MANIFEST.md`'s row
  notes + the `UPGRADE.md` manifest-lockstep rule: any release editing
  `templates/memory/PROTOCOL.md` ships a Semantic steps row (re-copy a still-stock protocol,
  arbitrate a customized one per §5i). **Open for the maintainer:** keep that cost, or move the
  row to `verbatim` and lean on §5i drift arbitration — truer to the house model, but it weakens
  AC-MP-07/08's "preserved without loss". → serves: vision-agent-memory (a protocol fix must
  reach the repos running it)
  <!-- id: ot-protocol-text-propagation | created: 2026-08-21 | last_used: 2026-09-01 | uses: 3 | tier: working | origin: 2026-08-21-052644 -->
