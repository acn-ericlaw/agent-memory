# Continuity — orderbook-api

> Shared ground truth for project state across all agents and sessions.

---

## Project State

- **project:** orderbook-api
- **status:** active development — migration engine refactor in progress
- **last_enabled:** 2026-06-12
- **last_session:** 2026-06-10 | agent: Aider (migrated)
- **repo:** ~/projects/orderbook-api

## Stack & Tools

- Runtime: Node.js 20
- Framework: Fastify
- Database: Postgres via Drizzle ORM
- Validation: zod
- Testing: vitest
- Package manager: pnpm
- CI: GitHub Actions

## Key Decisions

- POST-only for mutations (no PUT/PATCH) — legacy decision, do not change
- Standard response shape: `{ ok, data?, error? }`
- TypeScript strict mode, 2-space indents, no semicolons
- Matching engine extracted into its own module (`src/matching/`) — June 10

## Conventions

- One route file per resource in `src/routes/`
- Zod schemas in `src/schemas/`, one file per resource
- Drizzle queries in `src/db/`
- Always run `pnpm typecheck` before declaring code complete

## Open Threads

- [ ] Review migrated sessions from Cursor and Aider (see memory/sessions/)
- [ ] Verify legacy/cursor/ and legacy/aider/ — delete after confirming migration
- [ ] Validation gap reported in 2026-06-09 session — confirm fix is in place
- [ ] No tests exist yet for the matching engine refactor (2026-06-10)
- [x] Migrate from vendor AI tooling to agent-memory format

## Migration Summary

- **From:** Cursor (`.cursorrules`, `.cursor/rules/api.mdc`)
- **From:** Aider (`.aider.chat.history.md` — 3 sessions)
- **Date:** 2026-06-12
- **Sessions migrated:** 3 (2026-06-08, 2026-06-09, 2026-06-10)
- **Originals:** preserved under `legacy/cursor/` and `legacy/aider/`

## User Preferences

(none recorded yet — record ONLY what the user explicitly states; never infer)

## Team / Members

(none recorded yet)
