- [x] **Shipped v4.38.1 (PATCH) — scanner-neutral guidance constant** ([PR #26](https://github.com/acn-ericlaw/agent-memory/pull/26)).
  Downstream field FP (Snyk, enterprise Java deployment): memory-lint's prose guidance
  constant carried the hardcoded-secret detector shape (identifier-contains-SECRET +
  string-literal assignment) and rejected builds. Renamed `GUIDANCE` (byte-identical
  outputs, both runtimes); runtime-assembled hygiene self-check per suite (53 ×2,
  red-verified first); SKILLS.md house rule. Lesson: the tool's subject matter names its
  own identifiers into scanner FPs — prose constants stay scanner-neutral, now
  suite-enforced. → serves: vision-agent-memory
  <!-- id: secret-fp-guidance-ident-v4381 | created: 2026-08-26 | last_used: 2026-08-26 | uses: 1 | tier: working | origin: 2026-08-26-000208 -->
