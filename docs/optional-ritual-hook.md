# Reinforcing the after-session ritual with hooks

> **As of v4.19.0 the vendor-neutral reinforcement is installed by `ENABLE.md` and agent-activated** — a
> committed **`.githooks/post-commit`** (auto-stubs a session log when a commit does real work without
> one; activated via `git config core.hooksPath .githooks`) and a **CI floor**
> (`.github/workflows/agent-memory.yml`, zero per-user setup). Both are **advisory** (never block) and
> **no-code** (git/CI run them in the user's env; the tool runs nothing). Rationale + design:
> `docs/DESIGN-ritual-triggers.md`; activation: `.githooks/README.md`.
>
> **This doc covers two *further, optional* layers** you add yourself if you want them — keep them
> advisory (a nudge, never a hard block) so the no-code philosophy holds:
> (1) **per-vendor end-of-turn hooks** (Claude `Stop`, Copilot `sessionEnd`/`postToolUse`) for real-time
> nudges where a vendor supports them; (2) a **git pre-commit reminder**.

The schemas below are illustrative — confirm the exact format against your runtime's
current hook documentation before relying on them.

## Option A — Claude Code Stop hook (nudge at end of a turn)

Claude Code can run a `Stop` hook when it finishes responding. Use it to remind the
agent to persist memory. In your project's or personal `.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "test -n \"$(find memory/sessions -name '*.md' -newer memory/continuity.md 2>/dev/null)\" || echo 'Reminder: write a session log + update memory/continuity.md before wrapping up (see AGENTS.md).'"
          }
        ]
      }
    ]
  }
}
```

Tune the condition to taste — the goal is a visible reminder, not enforcement.

## GitHub Copilot CLI — `sessionEnd` hook (Copilot's equivalent of Option A)

Copilot CLI runs hooks on lifecycle events; **`sessionEnd`** is the end-of-work analog of Claude's
`Stop`. Put the JSON in a **repo-level `.github/hooks/`** file (committed — travels with the repo, so
every Copilot user on the team gets the nudge) or a **user-level `~/.copilot/hooks/`** file (personal,
per-machine). Keep it advisory — just `echo`, never a non-zero exit that could block:

```json
{
  "version": 1,
  "hooks": {
    "sessionEnd": [
      {
        "type": "command",
        "bash": "test -z \"$(git status --porcelain 2>/dev/null)\" || test -n \"$(find memory/sessions -name '*.md' -newer memory/continuity.md 2>/dev/null)\" || echo 'agent-memory: the working tree changed but no session log is newer than continuity.md — follow AGENTS.md \"After Every Session\" before wrapping up.'",
        "timeoutSec": 10
      }
    ]
  }
}
```

Copilot loads hook configs at CLI **start**, so restart the session to pick up a new one.
`.github/hooks/` is tracked (unlike `.github/skills/`), so a repo-level hook is shared; a
`~/.copilot/hooks/` hook stays personal. Like every option here it is **opt-in and never installed by
`ENABLE.md`**. It only *nudges* — it can't write the log for you (no hook can; the agent does that).
It's a **backstop**: when a session changed tracked files but left no fresh log, make that **visible**,
not enforced. (It stays silent on read-only sessions — no tracked change — which is the
lightweight-mode-correct no-log case, so it doesn't nag Ask/Plan-style work.)

## GitHub Copilot CLI — `postToolUse` adapter auto-sync (opt-in, advanced)

Author skills often in Copilot CLI and don't want to remember to run `sync skill adapters` each time?
A **`postToolUse`** hook can run the bundled **`sync-adapters`** script (v4.18.0) after each tool use.
Save to `.github/hooks/`:

```json
{
  "version": 1,
  "hooks": {
    "postToolUse": [
      {
        "type": "command",
        "bash": "bash agent-skills/sync-adapters/scripts/sync-adapters.sh >/dev/null 2>&1 || node agent-skills/sync-adapters/scripts/sync-adapters.mjs >/dev/null 2>&1 || python3 agent-skills/sync-adapters/scripts/sync-adapters.py >/dev/null 2>&1 || true",
        "timeoutSec": 20
      }
    ]
  }
}
```

**Notes:**
- It invokes the **canonical `sync-adapters` script** — so it regenerates **all six** vendor adapters
  and prunes orphans, with **no recipe duplication** (the script is the single source of truth).
- It runs on **every tool use** (idempotent; a quick Node/Python invocation). Switch the event to
  `sessionEnd` if you'd rather sync once per session.
- Silent + non-blocking (`|| true`); tries **bash** first (no runtime install), then Node ≥ 18, then
  Python 3 — whichever is on PATH.
- You **still need `/restart`** (or a skills rescan) for a freshly-synced `/<name>` to load — Copilot
  reads `.github/skills/` at init, which no hook can dodge.

## Option B — git pre-commit reminder

Remind (don't block) when a commit touches code but not `memory/`. Save as
`.git/hooks/pre-commit` (`chmod +x`) or wire it through your hooks manager:

```sh
#!/bin/sh
# Advisory: remind to update memory/ when committing non-memory changes.
staged="$(git diff --cached --name-only)"
if echo "$staged" | grep -qv '^memory/' && ! echo "$staged" | grep -q '^memory/'; then
  echo "Note: committing changes with no memory/ update."
  echo "Did you log the session and update continuity.md? (see AGENTS.md)"
fi
exit 0   # advisory only — never fail the commit
```

## Option C — no tooling at all

Prefer zero hooks? The after-session checklist lives in `AGENTS.md`; re-read it at the
end of a working session. That is the default, and it is enough for solo work.
