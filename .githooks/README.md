# `.githooks/` — vendor-neutral ritual triggers (agent-memory v4.19.0)

These are **committed, vendor-neutral git hooks** that reinforce the after-session ritual for *any*
agent (Claude, Copilot, Kiro, …) — because everyone commits, regardless of which AI did the work. They
are **advisory** (never block) and the **tool runs nothing itself**: git invokes them in your env at your
opt-in (`no-build-step-agent-run`). See `docs/optional-ritual-hook.md` and `DECAY.md` for the rationale.

## Activation (no manual step in the common path)

Git does **not** auto-run committed hooks on clone (deliberate security). One command activates them:

```sh
git config core.hooksPath .githooks
```

**The agent runs this for you at enable** (and on a first-run check), so an untrained user does nothing.
**CI is the zero-config floor** (`.github/workflows/agent-memory.yml`) — it runs server-side on push/PR
with no per-user setup, so the ritual is enforced even on a clone where no hook was activated.

## Hooks

- **`post-commit`** — after a commit: re-syncs skill adapters if a skill changed; and if the commit did
  real work but carried no session log, **auto-stubs one** (`memory/sessions/<ts>.md`) and nudges you to
  enrich it. The stub guarantees the ledger never has a silent gap; the *thoughtful* summary stays the
  agent's job (capture vs. judgment — same split as `memory-lint`).

To deactivate: `git config --unset core.hooksPath`.
