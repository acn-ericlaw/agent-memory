# Agent Instructions

This repository has two purposes:

1. **A shared memory system** — use it directly as your project's AI memory layer.
2. **An AI-enablement tool** — use it to AI-enable any other repository on your
   machine, including repos that already have vendor-specific AI files
   (Cursor, Aider, Continue, Cline, etc.) — those get migrated automatically.

Read the relevant section below based on what you have been asked to do.

---

## Purpose A — AI-Enable Another Repository

If the user says something like:

> "AI enable this repo `/path/to/project`"
> "Set up AI memory for `../my-app`"
> "AI enable this folder"
> "Migrate this repo to agent-memory"

**Read [`ENABLE.md`](./ENABLE.md) immediately and follow it exactly.**
That file contains the complete step-by-step protocol, including:

- Detection of existing vendor AI files (Cursor, Aider, Continue, etc.)
- Migration of vendor steering files and chat history into our unified format
- Conflict handling, dry-run support, and idempotent re-runs

For per-vendor migration rules (e.g. how to convert Aider's chat history,
where Cursor stores rules, how to parse Continue session JSON), see
[`MIGRATE.md`](./MIGRATE.md).

Do not proceed from memory. Do not improvise. Read `ENABLE.md` first.

---

## Purpose B — Use This Repo as Your Own Memory System

If the user is working *within* this repository (improving the tool itself,
adding vendor support, etc.), follow the standard memory protocol below.

### Before Every Session

Read these files before responding to anything:

1. `memory/instructions.md` — persona, rules, project context
2. `memory/continuity.md`   — current state, open threads, decisions (+ Blueprint gaps)
3. `memory/vision.md`       — the target the work serves (the VBDI north star)
4. `memory/sessions/`       — scan the most recent 2–3 session files

If a topic seems unfamiliar, grep `memory/archive/INDEX.md` (and follow a fact's
`origin` to its session) before saying you have no context — retrieval here is lexical
+ indexed by design (`DECAY.md` §11); facts fade to the archive but are never deleted.

### The cognitive loop (VBDI)

A forward loop rides on the memory layer (`DECAY.md` §12; design:
`docs/DESIGN-vbdi-lifecycle.md`): **Current State (`continuity.md`) → Vision
(`memory/vision.md`) → Blueprint (gap) → Design → Implementation → Feedback → repeat.**
Tie significant work to a `(blueprint)` Open Thread that `serves:` the Vision and to the
Design it realizes; surface altitude drift; gate each transition with the human. Never
fabricate the Vision.

> The Design altitude *may* keep an **optional** Architecture Decision Record log,
> `docs/arch-decisions/ADR.md` (a human-facing governance ledger; see `.agent/schema.md`). It is read
> **on demand** — deliberately **not** part of the Before-session read above; the
> `(ADR-NNNN)` tags on invariants are human pointers, not a cue to open it.
> **If the log exists, keep it alive:** on a new durable architecture decision — or when you
> supersede/invalidate a continuity fact carrying an `(ADR-NNNN)` tag — **propose** a matching
> ledger update (add a newer ADR; mark the old `Superseded`/`Deprecated`, never delete; keep
> `formalizes:` ↔ `(ADR-NNNN)` in sync) and let the human approve (`DECAY.md` §9, §12).

### Skills

If a `agent-skills/` directory exists, it holds the project's **capabilities** — committed,
vendor-neutral `agent-skills/<name>/SKILL.md` files. When a task matches a skill's
`description`, read and follow that `SKILL.md` (and any scripts it references) — the agent
is the runtime, so it works on any vendor. Native adapters (`.claude/skills/`,
`.gemini/commands/`, `.cursor/rules/`, `.kiro/skills/`, `.github/skills/`, `.agents/skills/`) are thin, gitignored, regenerated
pointers — **never commit them** (only `agent-skills/` is shared); the source of truth is
always `agent-skills/<name>/SKILL.md`.

**Authoring, syncing, adopting, sanity-checking, or editing a tool-provided skill?** See **`SKILLS.md`**
(read on demand — not part of the per-session read). **Authoring a skill is a 3-step action — write
`agent-skills/<name>/SKILL.md`, run `sync skill adapters`, then reload your runtime if it loads adapters
at startup (e.g. GitHub Copilot CLI `/restart`); it is not done after step 1.** Skill work is a
deliberate, occasional action, never part of the session ritual. A skill whose frontmatter says `provenance: agent-memory-builtin` is
**tool-managed** (overwritten on upgrade) — don't edit it in place; fork it under a new name, or
upstream a genuine fix to the agent-memory project (`SKILLS.md` → "Tool-provided (system) skills").

### During the Session

- Reference `memory/continuity.md` when relevant.
- Note any new facts, decisions, or preferences for post-session write.
- Track which fact **ids** you rely on, create, or reactivate — record them in the
  session log's `## Memory References`. Don't edit fact metadata mid-session.

### After Every Session

A "session" is **one log-write** — the work since the last log, not necessarily a
whole conversation. A long, multi-task conversation may produce several logs; that's
expected (the decay math counts log files — `DECAY.md` §4).

1. **Create** `memory/sessions/YYYY-MM-DD-HHMMSS.md` using the UTC timestamp at
   **persist time** (when you write the file). Use `date -u +%Y-%m-%d-%H%M%S` or
   equivalent; omit colons for cross-platform compatibility. Title line:
   `# Session (endZ)` — the persist-time UTC stamp (full ISO 8601 ms) is required; a
   start time is optional/best-effort, so don't fabricate one. Never append to
   another contributor's session file.
   Include a `## Memory References` section (fact ids referenced / created /
   reactivated) — the event log the review ritual reads (`DECAY.md`).
2. **Update** `memory/continuity.md`:
   - Set `last_session` to today's date and your agent name.
   - Keep **`status` a short current-state line — never a changelog.** Don't accrete
     per-version history onto it; that shared line becomes a merge-conflict hotspot for
     concurrent teammates. History lives in the session logs / `UPGRADE.md` ladder. One
     fact per line; see `.agent/schema.md` → "Concurrency & merge-friendliness" for the
     keep-both / take-later merge conventions.
   - Mark completed Open Threads `- [x]` and **leave them** — the review sweeps them
     once older than `archive_window`; don't archive them by hand.
   - Add new Open Threads; give each new fact a kebab `id` + footer: set `id`,
     `created`, `tier: working` (or `core` for an invariant), `origin: <this session's
     file>`, and seed `last_used: today | uses: 1`. Don't hand-edit
     `uses`/`last_used`/`tier` after — the review owns them.
   - **Check a new fact against existing ones first** (`DECAY.md` §10): supersede a
     clear replacement (below), or raise a `- [ ] Contradiction: …` Open Thread for a
     genuine conflict — don't silently keep both.
   - Update the substance of any changed fact (not its usage metadata).
   - **Reversed a decision / a fact became false?** Add the successor (born
     `tier: working`, `supersedes: <old>`), mark the old `tier: superseded` +
     `superseded-by: <new>` (omit the link for pure invalidation), and record
     `Superseded: <old> → <new>` in `## Memory References` — a truth-state edit you
     own; the review archives it flagged "superseded" (`DECAY.md` §9).
3. **Review cadence.** If `sessions_since_last_review ≥ review_every`
   (`memory/decay-policy.md`) or `continuity.md` exceeds `continuity_max_facts` /
   `continuity_max_lines`, run the review ritual (`REVIEW.md`). `memory-lint` flags all
   three (`[review-overdue]` / `[continuity-bloat]`). Also run on demand if the user says "review memory".
4. Remind the user to commit: `git add memory/ && git commit -m "session YYYY-MM-DD [agent]"`.
   **Commits are deliberate and human-initiated.** When you commit at the human's direction,
   **identify yourself** the same way you do in session logs — e.g. a `Co-Authored-By: <your agent
   name>` trailer — so authorship is traceable across vendors. (If your runtime already adds one,
   nothing to do.)

**After-session checklist** (the ritual is convention — run it each time):
- [ ] session log written (persist-time filename + `## Memory References`)
- [ ] `continuity.md`: `last_session` set, threads checked, new facts have footers
- [ ] review run if cadence/size triggered (`REVIEW.md`)
- [ ] reminded the user to commit `memory/` (deliberate, human-initiated, with a self-identifying co-author trailer)

> **Lightweight mode — key the write to whether a *tracked* file changed (the *objective* test is the
> git diff, not any filesystem write — and never a "trivial" judgment; both AI and human misjudge "trivial").**
> - **Read-only session** (no tracked file changed — orientation, Q&A, exploration, **or a run whose
>   only writes are gitignored, regenerated artifacts**: `sync skill adapters`, `review-scratch/`
>   snapshots, the compiled lint artifact): **no session log** — nothing entered the repo, nothing to
>   commit, no event to record.
> - **A tracked file changed but produced no memory-relevant event** (no new/changed fact, no decision
>   worth recording, no Open Thread touched, no project-state change — e.g. a one-line fix, a typo):
>   write a **one-line "lite" session log** (persist-time filename + `**Agent:**` + a *lightweight*-marked
>   summary + `## Memory References` → `(none)`) and skip the rest (full template, fact-footers,
>   continuity edits; `last_session` is derivable from the newest session file). **Don't skip the log
>   just because it felt "trivial"** — a misjudged change that actually mattered must still be logged.
>   **One log per working *session*, not per commit:** if you already wrote a session log earlier in
>   *this* working session, a later **memory-neutral** commit should **enrich that existing log** (a
>   one-line "also: …" note) rather than spawn another near-duplicate lite log — a burst of commits in
>   one sitting is *one* session. This keeps the decay session-count honest (it counts log files) and
>   mirrors the post-commit hook's per-session windowing (v4.22.1).
> - **A memory-relevant event** (fact / decision / Open Thread / project-state change, or anything
>   touching Vision / Blueprint / invariant / supersession): the **full** ritual. (Distinct
>   memory-relevant work still gets its **own** log, so a multi-task conversation may still yield several —
>   the rule above only stops *trivial* follow-on commits from each minting a near-duplicate lite log.)
> The ledger stays continuous for anything that touched a *tracked* file; the review treats a lite log
> as a normal reference-free session, so usage is unaffected.

> **Reinforced, not just documented (v4.19.0).** Enabled repos ship vendor-neutral triggers — a committed
> `.githooks/post-commit` (auto-stubs a session log when a commit does real work without one;
> agent-activated via `git config core.hooksPath .githooks`) + a CI floor
> (`.github/workflows/agent-memory.yml`, zero per-user setup) — so the ritual fires for any vendor. Treat
> the log as part of **done**. Advisory (never blocks) + no-code (git/CI run them in your env; the tool
> runs nothing). Design + per-vendor hook extras: `docs/DESIGN-ritual-triggers.md`, `docs/optional-ritual-hook.md`.
>
> **First session in a fresh clone? Self-initialize.** A clone has the gitignored skill adapters
> **absent** and the hook **unactivated** (git can't auto-run committed hooks on clone). If vendor
> adapter dirs are empty or `git config core.hooksPath` is unset, run **`bash .githooks/init.sh`** once
> (regenerates adapters + activates the post-commit hook) — proactively, before other work. (CI runs
> server-side regardless.)

> **Long session? Keep state externalized so compaction is safe (v4.23.2).** Compaction (your tool's
> `/compact`, an auto-compact at a context-usage threshold, or a fresh session) summarizes the
> conversation and drops verbatim detail. The **objective** health signal is **context-window utilization —
> tokens used vs. the model's limit** — which your harness tracks and may auto-act on; wall-clock time and
> a "replies feel vague" sense are only proxies (the model can't reliably self-measure its own context, so
> don't gate on a felt "fog"). You usually **can't compact yourself**, but you control the one thing that
> makes compaction lossless:
> - **Write the session log + any `continuity.md` update at each natural seam** — a milestone landed, a
>   phase shift (explore → implement → verify), or before pivoting to an unrelated task — **before**
>   compaction, not after. Externalized state reloads as context next turn; whatever lives **only** in the
>   buffer is what a summary can lose (summaries keep the narrative, not the verbatim texture).
> - **At a seam with high utilization, suggest compacting** (or rely on the harness's auto-compact) rather
>   than carrying a full buffer into the next phase. **Never mid-task**, with hot, unwritten state.
> - **After any compaction, re-verify specifics against live files** rather than trusting the paraphrase.
> The session log *is* the seam marker: "when do I write the log?" and "when is it safe to compact?" share
> the same beat. This is *why* the memory layer lives in **files**, not the chat buffer.

### Multi-Agent Continuity

Check `last_session` in `continuity.md` and note the agent name. If it is **not
your own agent family** (e.g. Claude, Gemini, Copilot, Cursor), read that session
log in full before responding.

> Two memory layers: this repo's `memory/` is shared project state (committed to
> git); your runtime's user-scoped store (e.g. Claude Code's `~/.claude/`) is for
> personal preferences. Keep project facts here, preferences there.

---

## Supported Agent Bootstrap Files

| Agent | File |
|---|---|
| Claude Code | `CLAUDE.md` |
| Gemini CLI | `GEMINI.md` |
| ChatGPT / Codex | `AGENTS.md` (this file) |
| Cursor | `.cursorrules` |
| Windsurf | `.windsurfrules` |
| GitHub Copilot | `.github/copilot-instructions.md` |

## Supported Migration Sources

When AI-enabling a repo that already has AI tooling, these vendors are detected
and migrated automatically: Claude Code, Cursor, Cline, Roo Code, Aider,
Continue.dev, Codeium/Windsurf, GitHub Copilot, GPT/Codex agents, Zed AI,
Gemini CLI, Kiro. See `MIGRATE.md` for protocols.

Vendor **agent-skills/capabilities** (e.g. `.claude/skills/`) are also migrated — *promoted*
into the neutral, committed `agent-skills/` layer (not flattened into steering), with originals
preserved under `legacy/` and native adapters regenerated. See `MIGRATE.md`.
