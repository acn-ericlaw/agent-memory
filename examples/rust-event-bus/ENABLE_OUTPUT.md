# Example: AI Enable Output (real run)

Unlike a mockup, this is the **actual** output of enabling a real repository —
a small Rust async event-bus demo — captured when running:

> "AI enable this repo `~/sandbox/rust/rust_event_bus_example`"

The `memory/` files beside this README are the real, unedited result.

---

```
Analysing ~/sandbox/rust/rust_event_bus_example...

  Listing top-level contents (including hidden files)... ✓
  Note: not a git repository; no .gitignore present.

Detecting existing AI footprint...

  Steering files:  none
  Vendor history:  none
  agent-memory:    not present

  → No AI footprint found. Mode A — Fresh Enable.

Analysing project...

  Reading: Cargo.toml ✓
  Scanning: src/ ✓   (single file: src/main.rs)
  Reading: README.md … not found

Detected:
  • Project:    event_bus_demo  (dir: rust_event_bus_example)
  • Language:   Rust (edition 2021)
  • Stack:      tokio (async runtime), flume (channels)
  • Type:       CLI / single-binary demo
  • Tests:      none (cargo test runs nothing)
  • CI/CD:      none

Generating memory files...

  ✓ memory/instructions.md   (tailored: EventBus / route-name dispatch model)
  ✓ memory/continuity.md     (4 open threads detected)
  ✓ memory/sessions/         (empty, ready)
  ✓ .agent/schema.md

Installing bootstrap files...

  ✓ AGENTS.md
  ✓ CLAUDE.md                (inline header: project name + one-line description)
  ✓ GEMINI.md                (inline header)
  ✓ .cursorrules
  ✓ .windsurfrules
  ✓ .github/copilot-instructions.md

Step 7 (.gitignore): skipped — no .gitignore present and repo is not under git.

─────────────────────────────────────────────────
✓ AI-enabled: ~/sandbox/rust/rust_event_bus_example
  Mode: Fresh Enable (A)
─────────────────────────────────────────────────

  Open threads seeded:
  • No tests — add unit tests for EventBus::send routing (hit + miss)
  • Not under version control / no .gitignore — ignore target/ if git init'd
  • No README — a short usage note would help
  • Dead commented import `// use tokio;` in src/main.rs — remove

  Next steps:
  1. Review memory/instructions.md and memory/continuity.md
  2. (optional) git init && add a .gitignore for target/
  3. Open with your AI agent and start working

Would you like me to open memory/continuity.md so you can review
what I detected before your first session? (yes/no)
```
