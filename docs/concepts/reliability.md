# Reliability

A protocol that *depends on an agent reliably self-triggering* fails the moment it lands with
an untrained team or a less-agentic vendor. The governing adoption constraint became:

> **Any manual user step is a barrier.**

So agent-memory hardens the ritual's *execution*, not just its documentation.

## Vendor-neutral triggers

Enable installs two things, agent-activated, with **no manual user step**:

- A committed **`post-commit` git hook** (advisory; never blocks). After a commit it
  auto-stubs a session log when the commit did real work but carried none, and re-syncs
  adapters when a skill changed.
- A **CI floor** — `memory-lint` plus a session-log presence check — with zero per-user
  setup.

`no-build-step-agent-run` still holds: git and CI invoke these in *your* environment; the
tool itself runs nothing.

!!! warning "Honest limit"
    Git cannot auto-run a committed hook on a fresh clone (a security boundary). So local
    hooks are **agent-activated** at enable, and **CI is the always-on, zero-config backstop**.

### One log per session, not per commit

The hook windows by session. Because the decay model counts session *files*, per-commit logs
would inflate the count and decay facts too fast — so a burst of commits in one sitting is
treated as one session.

## First-run init & Windows hardening

A fresh clone has gitignored adapters absent and the hook unactivated. Two safeguards close
that gap:

- **`.githooks/init.sh`** — one idempotent command to regenerate adapters and activate the
  hook.
- **`.gitattributes`** — pins shell scripts to LF so Git for Windows doesn't rewrite them to
  CRLF and silently break the hook.

`memory-lint` also catches an empty or malformed install manifest, so a botched version stamp
fails the lint instead of quietly breaking upgrade detection.

## Conflict resolution that never picks a winner

[`MERGE.md`](../guides/resolve-merge-conflicts.md) is a no-code, human-gated protocol for a git
conflict in `memory/`:

- Mechanical hunks reconcile deterministically (additive → union/keep-both; scalar →
  take-later).
- A **semantic clash preserves both + raises a Contradiction** — a supersession only on the
  human's explicit instruction.
- `memory-lint` gates; the human approves the merge commit (never auto-commit).

The `status` line is specified as a short current-state line (not an accreted changelog), so
it stops being a merge hotspot.

## Safe-write discipline

The most-repeated bug was a truncate-before-read shortcut —
`open(f,"w").write(open(f).read()+…)` — which empties a file *before* reading it. The rule is
now in the shared protocol:

> Append-mode or read-into-a-variable-then-write. Run `memory-lint` after any scripted memory
> mutation.

And the [`archive-fact`](../reference/built-in-skills.md#archive-fact) helper makes truncation
*structurally impossible* for the one move that kept hitting it.

## Informed consent

A fresh enable opens with a concise **exec summary** (what the protocol is, what it writes,
what it leaves untouched, that it's committed + shared) and a **cancel gate** — a blind "yes"
is replaced by informed consent before anything is written.
