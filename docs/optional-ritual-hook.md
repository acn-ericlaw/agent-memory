# Optional: reinforce the after-session ritual with a hook

> **Optional and opt-in.** agent-memory is deliberately no-code — the markdown files
> are the product, and the after-session ritual (write a session log, update
> `continuity.md`, run the review when due) is a convention an agent follows.
> Conventions get skipped under time pressure. If you want the ritual *prompted*
> rather than only documented, wire one of the lightweight, advisory hooks below.
> **None of this is installed by `ENABLE.md`** — add it yourself if you want it, and
> keep it advisory (a nudge, never a hard block) so the no-code philosophy holds.

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
