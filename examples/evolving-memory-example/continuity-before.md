# Continuity — taskflow-api

> Snapshot **before** the review at session `2026-06-20-141503`. Compare with
> `continuity-after.md`. Fictional project; worked example only.

---

## Project State

- **project:** taskflow-api
- **status:** active development
- **last_enabled:** 2026-03-02
- **last_session:** 2026-06-20 | agent: Claude Code (2026-06-20-141503)
- **last_review:** 2026-05-30 | through 2026-05-30-093210
- **repo:** ~/projects/taskflow-api

## Architectural Invariants

- POST-only for mutations; no PUT/PATCH (clients depend on it)
  <!-- id: post-only-mutations | created: 2026-03-02 | last_used: 2026-06-18 | uses: 24 | tier: core -->
- All times stored and returned as UTC ISO-8601
  <!-- id: utc-everywhere | created: 2026-03-02 | last_used: 2026-06-12 | uses: 17 | tier: core -->

## Stack & Tools

- Node 20 + Fastify; Postgres via Drizzle
  <!-- id: stack-node-fastify | created: 2026-03-02 | last_used: 2026-06-20 | uses: 30 | tier: active -->

## Key Decisions

- Webhooks are fire-and-forget; no retry queue
  <!-- id: webhook-fire-forget | created: 2026-04-10 | last_used: 2026-06-19 | uses: 9 | tier: active -->
- Rate limiting backed by a Redis token bucket
  <!-- id: rate-limit-redis | created: 2026-04-22 | last_used: 2026-06-15 | uses: 6 | tier: active -->
- GraphQL gateway in front of REST for the mobile client
  <!-- id: graphql-gateway | created: 2026-06-17 | last_used: 2026-06-17 | uses: 1 | tier: working -->
- JWT access tokens expire in 15 minutes; refresh via cookie
  <!-- id: jwt-15min-expiry | created: 2026-04-01 | last_used: 2026-05-28 | uses: 4 | tier: active -->
- SOAP adapter kept for the legacy billing vendor
  <!-- id: legacy-soap-adapter | created: 2026-03-15 | last_used: 2026-04-30 | uses: 3 | tier: archive-candidate -->
- CSV bulk-import endpoint for the onboarding team
  <!-- id: csv-bulk-import | created: 2026-03-20 | last_used: 2026-04-25 | uses: 2 | tier: archive-candidate -->
- ~~API version in the URI path (`/v1/…`)~~ — **superseded** today by header-based versioning
  <!-- id: rest-versioning-uri | created: 2026-03-10 | last_used: 2026-06-20 | uses: 7 | tier: superseded | superseded-by: rest-versioning-header -->
- API version selected via the `Accept` header, not the URI path
  <!-- id: rest-versioning-header | created: 2026-06-20 | last_used: 2026-06-20 | uses: 1 | tier: working | supersedes: rest-versioning-uri -->

## Conventions

- Conventional Commits; PRs squash-merged
  <!-- id: conventional-commits | created: 2026-03-02 | last_used: 2026-06-14 | uses: 12 | tier: active -->

## Open Threads

- [ ] Add idempotency keys to the payments endpoint
  <!-- id: thread-idempotency-keys | created: 2026-06-11 | last_used: 2026-06-20 | uses: 3 | tier: active -->
- [x] Migrate CI from CircleCI to GitHub Actions
  <!-- id: thread-ci-migration | created: 2026-04-05 | last_used: 2026-04-28 | uses: 5 | tier: active -->

## User Preferences

(none recorded yet — record ONLY what the user explicitly states; never infer)

## Team / Members

(none recorded yet)
