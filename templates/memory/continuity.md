# Continuity — {{PROJECT_NAME}}

> Shared ground truth for project state across all agents and sessions.
> Update at the end of every session. Never delete — only archive (see `REVIEW.md`).
>
> Each fact carries a metadata footer in an HTML comment, maintained by the review
> ritual — invisible when rendered, read/written by agents:
> `<!-- id: kebab-id | created: YYYY-MM-DD | last_used: YYYY-MM-DD | uses: N | tier: active -->`
> See `.agent/schema.md` for the fields and `memory/decay-policy.md` for the windows.

---

## Project State

- **project:** {{PROJECT_NAME}}
- **status:** {{PROJECT_STATUS}}
- **last_enabled:** {{TODAY}}
- **last_session:** (none yet)
- **last_review:** (none yet)
- **repo:** {{REPO_PATH}}

## Stack & Tools

{{STACK_DETAILS}}

## Architectural Invariants

> Hard constraints that must never change. These never decay (treated as `core`).
> Remove this section if the repo genuinely has none.

{{ARCHITECTURAL_INVARIANTS}}

## Key Decisions

{{INITIAL_DECISIONS}}

## Conventions

{{CONVENTIONS_SUMMARY}}

## Open Threads

{{OPEN_THREADS}}

## User Preferences

(none recorded yet — record ONLY what the user explicitly states; never infer)

## Team / Members

(none recorded yet)
