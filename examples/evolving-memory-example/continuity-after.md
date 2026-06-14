# Continuity — taskflow-api

> Snapshot **after** the review at session `2026-06-20-141503` (compare with
> `continuity-before.md`). Leaner: two stale facts archived (faded), one decision
> superseded (false → archived), one completed thread swept, one fact reactivated from
> cold storage — plus a first invariant-verification prompt raised. Fictional project;
> worked example.

---

## Project State

- **project:** taskflow-api
- **status:** active development
- **last_enabled:** 2026-03-02
- **last_session:** 2026-06-20 | agent: Claude Code (2026-06-20-141503)
- **last_review:** 2026-06-20 | through 2026-06-20-141503
- **last_invariant_check:** 2026-06-20 | through 2026-06-20-141503
- **repo:** ~/projects/taskflow-api

## Architectural Invariants

- POST-only for mutations; no PUT/PATCH (clients depend on it)
  <!-- id: post-only-mutations | created: 2026-03-02 | last_used: 2026-06-20 | uses: 25 | tier: core -->
- All times stored and returned as UTC ISO-8601
  <!-- id: utc-everywhere | created: 2026-03-02 | last_used: 2026-06-12 | uses: 17 | tier: core -->

## Stack & Tools

- Node 20 + Fastify; Postgres via Drizzle
  <!-- id: stack-node-fastify | created: 2026-03-02 | last_used: 2026-06-20 | uses: 31 | tier: active -->

## Key Decisions

- Webhooks are fire-and-forget; no retry queue
  <!-- id: webhook-fire-forget | created: 2026-04-10 | last_used: 2026-06-20 | uses: 10 | tier: active -->
- Rate limiting backed by a Redis token bucket
  <!-- id: rate-limit-redis | created: 2026-04-22 | last_used: 2026-06-15 | uses: 6 | tier: active -->
- GraphQL gateway in front of REST for the mobile client
  <!-- id: graphql-gateway | created: 2026-06-17 | last_used: 2026-06-20 | uses: 2 | tier: active -->
- Stay on Drizzle; do not adopt a second ORM (reaffirmed for the reporting service)
  <!-- id: drizzle-over-prisma | created: 2026-03-08 | last_used: 2026-06-20 | uses: 6 | tier: active -->
- Reporting service reuses Drizzle (no second ORM)
  <!-- id: reporting-service-drizzle | created: 2026-06-20 | last_used: 2026-06-20 | uses: 1 | tier: working -->
- API version selected via the `Accept` header, not the URI path
  <!-- id: rest-versioning-header | created: 2026-06-20 | last_used: 2026-06-20 | uses: 1 | tier: working | supersedes: rest-versioning-uri -->
- JWT access tokens expire in 15 minutes; refresh via cookie
  <!-- id: jwt-15min-expiry | created: 2026-04-01 | last_used: 2026-05-28 | uses: 4 | tier: archive-candidate -->

## Conventions

- Conventional Commits; PRs squash-merged
  <!-- id: conventional-commits | created: 2026-03-02 | last_used: 2026-06-14 | uses: 12 | tier: active -->

## Open Threads

- [ ] Add idempotency keys to the payments endpoint
  <!-- id: thread-idempotency-keys | created: 2026-06-11 | last_used: 2026-06-20 | uses: 3 | tier: active -->
- [ ] Re-verify invariants (first check, due): confirm `post-only-mutations` and
  `utc-everywhere` still hold, or supersede any that don't (`DECAY.md` §9)
  <!-- id: thread-verify-invariants | created: 2026-06-20 | last_used: 2026-06-20 | uses: 1 | tier: active -->

## User Preferences

(none recorded yet — record ONLY what the user explicitly states; never infer)

## Team / Members

(none recorded yet)
