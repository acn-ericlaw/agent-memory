# Agent Instructions — orderbook-api

## What This Project Is

A Node.js + Fastify API for an orderbook / matching engine. Accepts order
submissions, validates them, and persists to a Postgres database via Drizzle ORM.

**Type:** Backend API service
**Primary language:** TypeScript (strict mode)
**Framework / stack:** Fastify, Drizzle ORM, Postgres, zod, pnpm

## Repository Structure

```
src/
  routes/        ← one file per resource
  lib/           ← shared utilities
  db/            ← Drizzle ORM queries
  schemas/       ← zod validation schemas
  matching/      ← matching engine module
```

## Conventions Observed

- TypeScript strict mode
- 2-space indents, no semicolons
- async/await only — never .then()
- All files end with a newline
- POST for all mutations (no PUT/PATCH)
- Standard response shape: `{ ok: boolean, data?: any, error?: string }`
- Auth required on everything except `/health` and `/auth/*`
- Input validation via zod schemas in `src/schemas/`

## Tone & Style

- Be concise unless detail is explicitly requested.
- Match the existing TypeScript style — no Prettier rewrites.
- Always run `pnpm typecheck` before claiming code is complete.

## Core Rules

1. Never modify files outside the project scope without asking.
2. Follow the existing code style — do not reformat files unnecessarily.
3. Run `pnpm typecheck` before considering any code change complete.
4. All new endpoints need a zod schema in `src/schemas/`.
5. Record significant decisions in the session log and continuity file.

---

## Migrated rules from Cursor

You are working on the orderbook-api project, a Node.js + Fastify API.

Code style:
- TypeScript with strict mode
- 2-space indents, no semicolons
- Use async/await, never .then()
- All files end with a newline

Project structure:
- src/routes/ - one file per resource
- src/lib/ - shared utilities
- src/db/ - Drizzle ORM queries

Always run `pnpm typecheck` before suggesting code is complete.

### Migrated rule: api

## API conventions

- Use POST for all mutations; never PUT or PATCH (legacy decision, do not change)
- All endpoints return JSON with shape: { ok: boolean, data?: any, error?: string }
- Always validate input with zod schemas in src/schemas/
- Auth required on everything except /health and /auth/*

---

## Testing

- Framework: vitest (detected from package.json)
- Run: `pnpm test`

## CI / CD

- GitHub Actions: `.github/workflows/ci.yml`
- Runs typecheck, lint, and tests on PRs
