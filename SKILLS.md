# SKILLS — Portable Capabilities (cross-vendor)

> How skills work in an agent-memory repo: **author once in `agent-skills/`, run on any vendor.**
> **Read this on demand** — only when authoring, syncing, adopting, or sanity-checking a skill.
> It is deliberately **not** part of the per-session read (that's `AGENTS.md`). Like `DECAY.md`
> / `REVIEW.md`, it ships into every enabled repo so a target's own agent — any vendor — can
> act on its own.
>
> **Why on-demand:** skill creation is a *conscious, occasional* developer action. The
> per-session path does not police skills; alignment is explicit (the operations below).

---

## What a skill is

A committed, vendor-neutral **`agent-skills/<name>/SKILL.md`**: frontmatter `name` + a
`description` (the *when-to-use* trigger), then the procedure, plus optional helper scripts
under `agent-skills/<name>/scripts/`.

The **runtime is the agent itself** — when a task matches a skill's `description`, it reads and
follows that `SKILL.md`. That baseline lives in `AGENTS.md` and works on any vendor with no
engine. `agent-skills/` is **committed** (it travels with the repo); per-vendor **adapters**
are **thin, gitignored, regenerated pointers** for native auto-trigger — the neutral skill is
always the source of truth.

## Authoring a skill

Create **`agent-skills/<name>/SKILL.md`** — **never** a vendor folder (those are gitignored,
regenerated pointers, and won't be shared). Keep the `description` a **single line, quote-free,
and concise**: a compact, trigger-phrase-rich summary (~1–2 sentences; it's matched within a
small discovery budget, so avoid long abstract paragraphs). Put helper scripts under
`agent-skills/<name>/scripts/`. Then run **sync skill adapters** so your vendor gets a native
adapter.

## Adapter recipe

The adapter `description` **mirrors the neutral skill's verbatim** (never abbreviate — that
drifts). For each `agent-skills/<name>/SKILL.md` (using its `name` + `description`):

- **Claude Code** → `.claude/skills/<name>/SKILL.md`:
  ```
  ---
  name: <name>
  description: <description>
  ---
  Maintained vendor-neutrally. Read and follow `agent-skills/<name>/SKILL.md` (repo root)
  and any scripts it references.
  ```
- **Gemini CLI** → `.gemini/commands/<name>.toml` (a **slash command** — invoked explicitly as
  `/<name>`; Gemini does **not** auto-match commands against natural language, so a phrase like
  "run <name>" routes through the `AGENTS.md` baseline instead — which reads the *same* neutral
  skill, so the result is identical):
  ```
  description = "<description>"
  prompt = "Read and follow the skill at agent-skills/<name>/SKILL.md (repo root), including any scripts it references, then carry out: {{args}}"
  ```
- **Cursor** → `.cursor/rules/<name>.mdc` (the "agent-requested" type — description-matched,
  so `globs` is empty and `alwaysApply` is false):
  ```
  ---
  description: <description>
  globs:
  alwaysApply: false
  ---
  When this applies, read and follow `agent-skills/<name>/SKILL.md` (repo root) and any
  scripts it references.
  ```
- **Kiro** → `.kiro/skills/<name>/SKILL.md` (Kiro follows the open Agent Skills standard, so
  this is the **same shape as the Claude adapter** — workspace skills live under `.kiro/skills/`):
  ```
  ---
  name: <name>
  description: <description>
  ---
  Maintained vendor-neutrally. Read and follow `agent-skills/<name>/SKILL.md` (repo root)
  and any scripts it references.
  ```

**Trigger semantics differ per vendor — set expectations accordingly.** Claude / Cursor / Kiro
adapters are *description-matched* — they auto-fire when a natural-language request matches the
`description`. The **Gemini** adapter is a *slash command* — it fires only on an explicit
`/<name>`, never on a natural-language phrase. This is **not** drift or a missing adapter: every
adapter is a thin pointer back to the **same** `agent-skills/<name>/SKILL.md`, and the
`AGENTS.md` baseline runs that neutral skill on any vendor regardless. So "checks `agent-skills/`
first" for a natural-language request on Gemini is *correct* — the baseline and the slash command
land on the identical file. Don't expect Gemini to auto-trigger a command from prose.

Keep descriptions single-line and free of `"` so they embed safely into TOML / `.mdc` / YAML
frontmatter; if a `"` is unavoidable, escape it for the target format (TOML: a single-quoted
literal string; `.mdc`/YAML: quote the whole value). YAML `>`/`|` folded/literal blocks work
*only* in YAML frontmatter — the value also lands in a TOML adapter, so the canonical value is
**one logical line** (a clean `>` folds to that anyway).

## Operations

### `sync skill adapters`
For **each** `agent-skills/<name>/SKILL.md`, (re)write the four adapters above — idempotent;
overwrite the adapter, never the neutral skill — and **prune** orphaned *generated* adapters
(one whose `agent-skills/<name>/` no longer exists; never touch other files in a vendor dir).
Touches no committed file (adapters are gitignored); not a version change. Run it after
authoring/editing a skill, or after a clone/pull on a machine that wants native auto-trigger.

> **Never commit the adapters — and never tell the user to.** The vendor adapter dirs
> (`.claude/`, `.gemini/`, `.cursor/`, `.kiro/`) are gitignored, per-machine, and regenerated;
> the **only** committed skills artifact is the neutral `agent-skills/`. After a sync, do **not**
> `git add` an adapter dir or suggest the user commit one. Report it like: *"regenerated N local
> adapters (gitignored — do not commit; only `agent-skills/` is shared)."*

### `adopt skill` (vendor → neutral)
If a skill was authored natively in a vendor folder (e.g. a vendor's built-in skill creator
wrote to `.claude/skills/<name>/`), it's **stranded** — gitignored, not the source of truth.
Promote it:
1. Copy its content into `agent-skills/<name>/SKILL.md` — preserve the procedure, neutralize
   vendor-specific phrasing; normalize frontmatter to `name` + `description`; move bundled
   scripts to `agent-skills/<name>/scripts/`.
2. Run **`sync skill adapters`** — regenerates the vendor file as a *pointer*.
3. Stage `agent-skills/<name>/` for the normal commit (on demand you may commit directly; the
   agent doesn't self-commit mid-ritual).

### `skill sanity check` (heavyweight — run deliberately)
The full alignment, for when you've been authoring/editing skills or suspect drift. Reads file
contents (heavier than the upgrade-time filename check), so run it **on demand**, not every
session:
1. **Adopt** any vendor-folder skill with no matching `agent-skills/<name>/`.
2. **Content check** each adapter against its neutral skill (description mirrors verbatim;
   pointer path correct); regenerate any that drifted.
3. **Prune** orphaned generated adapters.
4. Report adopted / regenerated / pruned.

---

> **Lightweight by design.** Enable does a full adaptation once; **upgrade** does only a cheap,
> read-only **filename** check that *recommends* `sync skill adapters` if an adapter is missing
> or orphaned (it never acts); the deliberate `skill sanity check` realigns everything when you
> choose to run it. None of this is in the per-session path.
