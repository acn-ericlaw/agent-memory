# Example: AI Enable with Migration

This file shows what the agent prints when you run:

> "AI enable this repo `~/projects/orderbook-api`"

on a repo that already uses Cursor and Aider.

---

```
Analysing ~/projects/orderbook-api...

  Listing top-level contents (including hidden files)... ✓

Detecting existing AI footprint...

  Found vendor files:
  • Cursor:  .cursorrules, .cursor/rules/api.mdc
  • Aider:   .aider.chat.history.md, .aider.input.history, .aider.conf.yml

  No agent-memory format detected. This will be a migration.

? Detected existing AI setup. I can migrate these into the unified
  agent-memory format. Originals will be preserved under legacy/.
  Proceed?  (yes / no / dry-run)
> yes

Migrating Cursor...
  • Moving  .cursorrules                    →  legacy/cursor/.cursorrules
  • Moving  .cursor/rules/api.mdc           →  legacy/cursor/.cursor/rules/api.mdc
  • Extracting steering content → memory/instructions.md
  ✓ Cursor migration complete

Migrating Aider...
  • Moving  .aider.chat.history.md          →  legacy/aider/.aider.chat.history.md
  • Moving  .aider.input.history            →  legacy/aider/.aider.input.history
  • Moving  .aider.conf.yml                 →  legacy/aider/.aider.conf.yml
  • Parsing chat history... found 3 sessions
  • Writing  memory/sessions/2026-06-08-a1b2.md
  • Writing  memory/sessions/2026-06-09-c3d4.md
  • Writing  memory/sessions/2026-06-10-e5f6.md
  ✓ Aider migration complete

Analysing project (post-migration)...

  Reading: package.json ✓
  Reading: README.md ✓
  Reading: tsconfig.json ✓
  Scanning: src/ ✓
  Checking: .github/workflows/ ✓

Detected:
  • Project:    orderbook-api
  • Language:   TypeScript (strict)
  • Stack:      Fastify, Drizzle ORM, Postgres, zod, vitest
  • Type:       Backend API service
  • Tests:      vitest
  • CI/CD:      GitHub Actions

Completing memory files...

  ✓ memory/instructions.md  (folded in migrated rules from Cursor + Aider)
  ✓ memory/continuity.md    (last_session set to 2026-06-10, 4 open threads)
  ✓ .agent/schema.md

Installing bootstrap files...

  ✓ AGENTS.md
  ✓ CLAUDE.md
  ✓ GEMINI.md
  ✓ .cursorrules           (replaces migrated original)
  ✓ .windsurfrules
  ✓ .github/copilot-instructions.md

Updated .gitignore: added agent-memory + legacy/ block.

─────────────────────────────────────────────────────────────────────
✓ AI-enabled: ~/projects/orderbook-api
  Mode: Migrated from Cursor + Aider
─────────────────────────────────────────────────────────────────────

  Migrated:
  • Cursor:  2 files  →  legacy/cursor/
  • Aider:   3 files  →  legacy/aider/
  • Sessions converted: 3 (2026-06-08 to 2026-06-10)

  Created:
  • memory/instructions.md, memory/continuity.md
  • memory/sessions/  (3 migrated files)
  • .agent/schema.md
  • 6 bootstrap files (AGENTS.md, CLAUDE.md, GEMINI.md,
    .cursorrules, .windsurfrules, .github/copilot-instructions.md)

  Preserved:
  • legacy/cursor/, legacy/aider/  (originals — do not edit)

  Next steps:
  1. Review memory/instructions.md  (migrated rules folded in)
  2. Verify migrated sessions in memory/sessions/
  3. cd ~/projects/orderbook-api
  4. git add . && git commit -m "chore: migrate to agent-memory from Cursor + Aider"

? Would you like me to:
   (a) Open memory/continuity.md so you can review what I detected
   (b) Walk through the migrated sessions
   (c) Both
   (d) Done
>
```
