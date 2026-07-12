# agent-memory

A no-code AI memory system, AI-enablement tool, **and migration tool** —
all in one repo. Markdown only. No code to run. No API keys.

Three things in one:

1. **A memory system** — clone it, open with your agent, work normally.
   Context persists across sessions and across different AI agents — and it
   *evolves*: frequently-used facts strengthen, unused ones fade to an archive,
   and the live `continuity.md` stays lean (see "Evolving Memory" below).

2. **An enablement tool** — point your agent at any existing repo and it
   gets a tailored memory system set up automatically.

3. **A migration tool** — if the target repo already uses vendor AI files
   (Cursor, Aider, Continue, Cline, Roo, Windsurf, Copilot, etc.), they get
   migrated into the unified format. Steering files folded in, chat history
   converted to dated session logs, originals preserved under `legacy/`.

---

## Quickstart

Three short phases: **install the tool**, **enable a repo**, then **work in that repo**.

### 1 · Install agent-memory (one-time)

```bash
git clone https://github.com/your-org/agent-memory
cd agent-memory
```

Open the cloned folder with your AI agent (Claude Code, Gemini CLI, Cursor, Kiro, …), and make
your **first prompt**:

> **"Start from `AGENTS.md`."**

This points the agent at the hub so it loads the agent-memory protocol *before* doing anything
else. It's the reliable entry point on every vendor — and it's **required** in enterprise IDEs
(e.g. Kiro) that otherwise self-bootstrap from their own onboarding before reading `AGENTS.md`.

### 2 · Enable a target repo

> **VS Code / Kiro:** add the target repo to the **same workspace** as this tool, so the agent can
> read both. Other CLIs (Claude Code, Gemini CLI, …) work fine without this.

Then ask:

> **"AI enable `/path/to/your-project`."**

The agent will detect any existing AI footprint (Cursor, Aider, Copilot, Kiro, …) and offer
migration (with a dry-run option), analyse the repo (language, stack, type), generate tailored
`memory/` files, install bootstrap files for all major agents, preserve originals under `legacy/`,
and report exactly what happened.

### 3 · Work in your AI-enabled repo

```bash
# Commit the freshly enabled repo
cd /path/to/your-project
git add . && git commit -m "chore: AI-enable repo"
```

From now on, **open the target repo with any AI agent and just work** — it reads `memory/`
automatically, orients without re-explaining, and records decisions as it goes. Commits stay
deliberate and human-initiated, with a self-identifying `Co-Authored-By:` trailer.

> **Note for enterprise IDEs (e.g. Kiro).** Per-machine vendor dirs (`.kiro/`, `.claude/`, …) are
> gitignored, so a fresh clone won't have them — after the agent loads the protocol, run
> **`sync skill adapters`** to regenerate your local skill adapters. Anything the IDE later deposits
> in `.kiro/` (hooks, steering) stays gitignored and per-machine, so it never touches the shared
> `memory/` layer; human-gated commit hooks (like Kiro's) align with agent-memory's
> deliberate-commit model.

---

## Design Philosophy — Two Layers That Coexist

There are two distinct AI memory layers in a developer's life, and this tool
treats them as separate by design:

| Layer | Where it lives | Who owns it | What it holds |
|---|---|---|---|
| **Personal** | `~/` (your home folder) | You | Your chosen vendor's chat history, model preferences, global settings — your own AI workflow |
| **Shared (team)** | The repo's `memory/` directory | The team, via git | Project rules, decisions, session logs — collaboration context across contributors |

The tool **only ever touches the team layer**. Your personal `~/.claude/`,
`~/.cursor/`, `~/.aider/`, Application Support folders, AppData — none of it
is read, modified, or moved. Whatever vendor you prefer keeps working exactly
as it did before.

This matters because:

- **Users keep their workflow.** If you love Cursor, you keep using Cursor
  with all your personal history and tweaks. Enablement does not migrate or
  disturb that.
- **Teams get a shared layer.** Contributors using different vendors —
  one on Claude Code, one on Cursor, one on Aider — all read and write to
  the same `memory/` folder in the repo. Common ground without forcing a
  common tool.
- **Migration only touches repo-committed artifacts.** If a vendor's chat
  history happened to be checked into the repo (e.g. `.aider.chat.history.md`,
  `.continue/sessions/`), that gets converted. Anything in your home folder
  stays in your home folder.

---

## Evolving Memory (Long-Term)

Memory doesn't just accumulate — it evolves, the way human memory does:
**frequently-used facts strengthen, unused ones fade, important ones stay
permanent.** It stays 100% markdown; the agent does the work, no code runs.

- **Each fact carries metadata** in an HTML comment (`id`, `created`, `last_used`,
  `uses`, `tier`) — invisible when rendered, maintained by the agent.
- **Usage is event-sourced.** Session logs record a `## Memory References` list of
  the fact ids they touched; that log *is* the ledger. A periodic **review ritual**
  recomputes `uses`/`last_used` from it — so the numbers are reproducible by any
  agent, on any vendor.
- **No floating-point scoring.** Tiers (`core → active → working → archive-candidate
  → archived`) are decided by *counting session files* against integer windows, so
  Claude, Gemini, and Cursor all reach the same decision. Tunable in
  `memory/decay-policy.md`.
- **Nothing is deleted.** Faded facts move to `memory/archive/` (cold storage,
  greppable via `INDEX.md`); referencing one again pulls it back to `active`.
- **`core` is human-set** and `## Architectural Invariants` + open work never decay.

Reference: `DECAY.md` (the rules) and `REVIEW.md` (the ritual), installed at the
root of every enabled repo.

---

## Fresh-Context Second Opinion

A long AI session over-trusts its own trajectory — the agent that built a solution is the
least likely to challenge it. The highest-value antidote is a reviewer with **clean memory**:
a fresh session or a different vendor that didn't live the work. agent-memory ships this as two
built-in skills, **installed into every enabled repo**:

- **`second-opinion`** — at a milestone (or when blocked or facing a risky change), it distills
  a compact snapshot **from** `continuity.md` + recent session logs (never a parallel state
  file) and, behind a **security advisory you must acknowledge**, hands it to a clean-context
  reviewer to challenge.
- **`apply-critique`** — takes the reviewer's critique back through a **bounded, validated,
  human-gated** loop: a few scoped fixes, then deterministic checks (build/tests + `memory-lint`),
  then a summary of what was applied vs. rejected and why.

The reviewer is a **hypothesis generator, not an authority** — its critique is advisory and
gated by deterministic checks and your decision. (That's the lesson the memory layer learned when
a clean-context reviewer once over-archived still-referenced facts — so the guardrail is built
in.) Snapshots and critiques are personal, gitignored scratch (`review-scratch/`); sharing one
with another AI is your conscious decision, which the advisory makes explicit. Like the rest of
the tool: **zero overhead by default** — nothing runs unless you invoke it.

> Also installed: **`memory-lint`**, the deterministic Python-3 verifier the review ritual relies
> on (see *Evolving Memory* above). All three built-ins are tool-managed — fork under a new skill
> name to customize, since upgrades overwrite them.

---

## Versioning & Upgrades

The tool is versioned (root `VERSION`, semver). Each enabled repo stamps
`.agent/version.md` with the version it's on, so re-running enablement can **upgrade
it in place** — additively, never destructively.

> **Recent releases — the 10 most recent.** The complete, official record is in
> **[CHANGELOG.md](CHANGELOG.md)**; the full in-place upgrade ladder — every rung, including the
> foundational milestones (**1.0.0** fresh enable · **2.0.0** vendor migration · **3.0.0** evolving
> memory · **4.0.0** the VBDI cognitive loop · **4.1.0** the cross-vendor skills layer) — lives in
> `UPGRADE.md`.

| Version | Capability |
|---|---|
| 4.29.0 | **Before-session context presence — bootstrap `@`-imports + an opt-in SessionStart recipe:** a child-repo field report showed agents skipping the before-session read chain (`CLAUDE.md → AGENTS.md → memory/*`) under task pressure — the v4.19.0 trigger layer reinforces only the *after*-session rituals (git/CI has no session-start moment), so the read rested on prompt adherence. The `CLAUDE.md`/`GEMINI.md` bootstrap pointers now **import** the hub + core memory files (`@AGENTS.md`, `@memory/instructions.md`, `@memory/continuity.md`, `@memory/vision.md`), making them structurally present at session start on import-capable runtimes — markdown-only, no hooks; `AGENTS.md` stays vendor-neutral. An opt-in Claude Code `SessionStart` injection recipe (for `memory/sessions/` recency — imports can't express dynamic paths) lands in the tool-side hook doc, never installed by default. Presence is guaranteed; *attendance* remains agent judgment |
| 4.28.4 | **`Co-Authored-By` dedup — one trailer per collaborator, keyed on email:** a third `mercury-composable` report — the agent co-authors the commit message *with* its harness, which often injects its own (model-version) `Co-Authored-By`; appending a second stable-name trailer produced duplicate co-authors for one collaborator (squash-merges compounded it — one commit had 55 trailer lines). `AGENTS.md` now reframes the model (reconcile the harness's message, don't blindly append) and states the invariant — **at most one `Co-Authored-By` per collaborator, matched on email** (`Claude Code` / `Claude Opus 4.8` / `Gemini CLI` are one collaborator at one address) — with a deterministic resolution tree + forge-aware squash guidance. Doc-only; enforcement hook deliberately deferred |
| 4.28.3 | **`[continuity-bloat]` line-count message is now decay-aware:** a second `mercury-composable` report (a 29-module reactor) — after a clean review the *fact* count is healthy but `continuity_max_lines` trips on dense, active Key Decisions, and the review has **nothing to archive**, so the warning is unclearable and its "a review is due to lean it down" wording nudges toward premature archival (REVIEW.md's costliest error). `memory-lint` now computes whether anything is archivable (facts overdue for decay + superseded); when lines are over budget but nothing is archivable it says so — *"condense shipped decisions, or raise `continuity_max_lines`"* — instead. Same failure class as v4.28.2, on the line axis. Both runtimes at parity + tests |
| 4.28.2 | **`memory-lint` `[continuity-bloat]` counts only decay-eligible facts:** a field report (`mercury-composable`) showed the fact-count check firing **permanently** even right after a fully correct review — because it counted `tier: core` invariants and pinned `- [ ]` open threads (which can never be archived) against `continuity_max_facts`, turning the primary lean signal into chronic noise. Now it excludes core + pinned before comparing (aligning with `decay-policy.md`'s "count of *decaying* facts/threads"): a repo with 14 core + 11 open threads + 16 working facts reads `16 < 30` (clean) instead of `41 > 30`. Both runtimes at parity + regression tests |
| 4.28.1 | **Post-commit hook — uncommitted-session-log guard:** the auto-stub window check misfired on the recommended two-commit pattern (feature commit → `chore(memory)` commit) when the log was written >30 min before the feature commit — the filename-timestamp threshold treated an in-flight (uncommitted) log as "too old" and stubbed a near-duplicate. Fix: before the time-window check, inspect `git status --porcelain -- memory/sessions/`; if any `.md` is staged/modified/untracked, emit the enrich-and-commit nudge and skip the stub. Filename-window check stays as fallback for already-committed logs. Non-blocking |
| 4.28.0 | **Co-author convention cleanup — stable agent identity + one trailer:** the `Co-Authored-By` self-identification now specifies the **stable agent name** (e.g. `Claude Code`, `Gemini CLI`) — the actual AI collaborator, **not** a model-version string that churns each release — matching session logs. Plus squash-merge guidance: collapse to a **single** trailer (GitHub appends a consolidated one after `---------`; trim the inline repeats). Refines the v4.27.0 PR convention; advisory, doc-only |
| 4.27.0 | **Standardized PR descriptions — lead with What / Why:** every AI-enabled repo now ships a `.github/pull_request_template.md` with two short sections — **What** (the change) and **Why** (the intent it serves — Blueprint gap / decision / problem, not a restatement of What), 1–2 paragraphs each, drawn from the session log(s) in the PR. Mirrored by an `AGENTS.md` convention (the vendor-neutral backstop) + a checklist line. Advisory, never a gate — *why* is a first-class artifact throughout the protocol, so a PR is no exception |
| 4.26.1 | **Refinement — the tooling no longer opines on a pinned thread's tier:** a sanity check of mercury found v4.26.0 flagged every `working`-tagged pinned `- [ ]` open thread as "should be `active`" — noise, since a pinned thread never decays regardless of its tier label (its pinned-ness protects it, not the label). `memory-lint` `[stale-metadata]` no longer flags pinned threads and `refresh-metadata` no longer rewrites their tier (it still refreshes their factual `uses`/`last_used`). Found comparing `refresh-metadata` to Copilot's own `update-metadata.py` |
| 4.26.0 | **`refresh-metadata` + a `[stale-metadata]` lint advisory — close the skipped-re-tier gap (7th built-in):** a cross-vendor field test (Gemini 3.1 Pro committed the v4.25.0 upgrade, then ran the overdue review unprompted — correctly using `archive-fact`, and the over-archival guard caught a premature archive) surfaced that it did the archive but **skipped review steps 2–3 (re-tier)**, leaving stale footers. Third instance of one pattern: *agents partially execute multi-step rituals.* `refresh-metadata` recomputes `last_used`/`uses`/`tier` from the reference log deterministically (pure arithmetic — the "full rebuild" path, made runnable; never archives); `memory-lint` gains `[stale-metadata]` to flag the drift. Refines the judgment-vs-arithmetic boundary: deciding *what to archive* stays with the agent; recomputing metadata is mechanized |
| 4.25.0 | **`archive-fact` — deterministic, safe archive-move (6th built-in):** from a cross-vendor critique (Gemini 3.1 Pro) — "harden the memory-writing mechanism itself; agent interpretation of safe writes is vulnerable to LLM/vendor variance." It names our most-repeated bug (the truncate-before-read trap that wiped the archive). A new built-in executes `REVIEW.md`'s archive-move deterministically: reads `continuity.md` into memory and writes once, so truncation is structurally impossible. Python + Node at parity, mirror tests, all-or-nothing guards, `--dry-run`. The agent still decides *what* to archive; the helper does the *move* (`never-pick-a-winner` intact). doc → tool, the next step after v4.22.4's doc safeguard |


When you "AI enable" a repo that's already on an older version, Mode B detects the
drift and runs the upgrade ladder in `UPGRADE.md` (the user's entry point stays the
single "AI enable this repo" command). A missing `.agent/version.md` is treated as a
pre-versioning install and upgraded from the 2.x baseline.

---

The tool detects and migrates from these vendors:

| Vendor | Detected via | What's migrated |
|---|---|---|
| Claude Code | `CLAUDE.md` (non-ours), `.claude/`, `.claude/skills/` | Steering, JSONL session history, **skills → `agent-skills/`** |
| Cursor | `.cursorrules`, `.cursor/rules/*.mdc` | All steering files |
| Cline | `.clinerules`, `.cline/` | Steering, history |
| Roo Code | `.roorules`, `.roo/` | Steering, history |
| Aider | `.aider.conf.yml`, `.aider.chat.history.md`, `CONVENTIONS.md` | Steering, full chat history |
| Continue.dev | `.continue/config.json`, `.continue/sessions/*.json` | Steering, JSON sessions |
| Codeium / Windsurf | `.windsurfrules`, `.codeiumrc`, `.windsurf/` | Steering, history |
| GitHub Copilot | `.github/copilot-instructions.md` (non-ours), `.github/skills/`, `.agents/skills/` | Steering, **skills → `agent-skills/`** (no history) |
| GPT / Codex | `AGENTS.md` (non-ours), `.codex/` | Steering, history |
| Zed AI | `.rules`, `.zed/` | Steering, history (with safety check) |
| Gemini CLI | `GEMINI.md` (non-ours), `.gemini/` | Steering, history |
| Google Antigravity (`agy`) | `.agents/` (`skills/`, `mcp_config.json`), `~/.gemini/antigravity-cli/` | Steering, **skills → `agent-skills/`** (Antigravity is the Gemini CLI successor; reads `.agents/skills/`, not `.gemini/commands/`) |
| Kiro | `.kiro/` (`steering/`, `skills/`, `specs/`); also auto-reads root `AGENTS.md` | Steering → instructions, **skills → `agent-skills/`**, specs preserved under `legacy/` |

Migration rules per vendor: see [`MIGRATE.md`](./MIGRATE.md).

---

## Migration Behaviour

- **Target repo only.** Every read, move, and write is scoped to the target
  repository. The user's `~/`, AppData, Application Support, and global vendor
  config are never touched. See "Design Philosophy" above.
- **Originals preserved.** Every vendor file is moved (not deleted) to
  `legacy/<vendor>/` in the target repo, with its relative path preserved.
- **Steering folded in.** Vendor rules become a `## Migrated rules from <vendor>`
  section inside `memory/instructions.md`. Nothing is discarded.
- **History becomes sessions.** Chat logs and JSONL files are parsed and split
  into dated `memory/sessions/YYYY-MM-DD-HHMMSS.md` files in our standard format.
- **Skills promoted.** Vendor skill bundles (e.g. `.claude/skills/`, `.kiro/skills/`, `.github/skills/`) become
  neutral, committed `agent-skills/<name>/SKILL.md` capabilities — not flattened into steering —
  with Claude/Gemini/Cursor/Kiro/Copilot adapters regenerated. See [`docs/DESIGN-skills-layer.md`](./docs/DESIGN-skills-layer.md).
- **Contradictions surfaced.** If two vendors had conflicting rules, both are
  preserved and an Open Thread is added asking the user to resolve.
- **Idempotent.** Running enable on an already-migrated repo detects our format
  and exits cleanly without changes.
- **Dry-run supported.** Answer `dry-run` when prompted to see what would happen
  without writing anything.

---

## Use as a Memory System Directly

If you want this repo to be your project's memory layer (not a tool):

```bash
git clone https://github.com/your-org/agent-memory my-project-memory
cd my-project-memory

# Edit memory/instructions.md and memory/continuity.md for your project
# Then open with your agent — it reads the memory files automatically
claude
```

---

## Supported Agents (Bootstrap Files Installed)

| Agent | Bootstrap file installed |
|---|---|
| Claude Code | `CLAUDE.md` |
| Gemini CLI | `GEMINI.md` |
| Google Antigravity (`agy`) | `AGENTS.md` (Agent Skills standard; reads `.agents/skills/`) |
| ChatGPT / Codex | `AGENTS.md` |
| Cursor | `.cursorrules` |
| Windsurf | `.windsurfrules` |
| GitHub Copilot | `.github/copilot-instructions.md` |

---

## Repo Structure

```
agent-memory/
  VERSION                            ← tool version (semver)
  ENABLE.md                          ← protocol: detect, migrate, generate, upgrade
  MIGRATE.md                         ← per-vendor migration rules (tool-only)
  UPGRADE.md                         ← in-place version-upgrade ladder (tool-only)
  DECAY.md                           ← evolving-memory rules (installed into targets)
  REVIEW.md                          ← the review ritual (installed into targets)
  SKILLS.md                          ← skills reference: author/sync/adopt/sanity (installed; on-demand)
  MERGE.md                           ← git-conflict resolution protocol (installed; on-demand)
  AGENTS.md                          ← memory protocol + enable dispatch
  CLAUDE.md / GEMINI.md              ← vendor bootstraps for this repo
  .cursorrules / .windsurfrules      ← Cursor / Windsurf bootstraps
  .github/copilot-instructions.md    ← GitHub Copilot bootstrap
  .github/pull_request_template.md   ← PR description convention: What / Why (installed)
  .github/workflows/agent-memory.yml ← CI floor: memory-lint + session-log check (installed)
  .githooks/                         ← vendor-neutral ritual triggers (committed; agent-activated)
    post-commit · init.sh · README.md
  .gitignore / .gitattributes        ← AI-infra ignores + LF pinning (merged into targets)
  CHANGELOG.md / LICENSE             ← official release notes / Apache-2.0

  templates/                         ← installed into target repos
    AGENTS.md, CLAUDE.md, GEMINI.md, ...
    memory/
      instructions.md                ← with {{placeholders}}
      continuity.md                  ← with {{placeholders}}
      decay-policy.md                ← evolving-memory windows/triggers
      sessions/.gitkeep
    .agent/schema.md                 ← canonical file format (verbatim)
    .agent/version.md                ← install manifest (with {{placeholders}})

  memory/                            ← this tool's own memory layer
    instructions.md
    continuity.md
    decay-policy.md
    sessions/                        ← dated logs (immutable event log)
    archive/                         ← faded facts (cold storage, never deleted)

  agent-skills/                      ← portable skills: neutral source of truth (vendor adapters gitignored)
    memory-lint/                     ← built-in: deterministic memory verifier (Python + Node, at parity)
    second-opinion/                  ← built-in: snapshot the task for a clean-memory reviewer
    apply-critique/                  ← built-in: apply a critique via a gated, human-approved loop
    sync-adapters/                   ← built-in: regenerate per-vendor adapters (bash · node · python)
    harvest-knowledge/               ← built-in: re-scan docs → fold durable facts into memory (on-demand)
    archive-fact/                    ← built-in: safe deterministic archive-move for the review (Python + Node)
    refresh-metadata/                ← built-in: recompute fact footers (last_used/uses/tier) from the log (Python + Node)
    hello-world/                     ← dogfood demo skill
    (the seven built-ins ship provenance: agent-memory-builtin and install into every enabled repo)

  docs/                              ← design rationale + governance (human-facing, on-demand)
    arch-decisions/
      ADR.md                         ← Architecture Decision Records (optional convention; dogfooded here)
    DESIGN-*.md                      ← long-form per-feature design narratives
    agent-cognitive-framework.md     ← the VBDI source framework

  examples/
    rust-event-bus/                  ← Mode A: REAL fresh enable on a Rust repo
      memory/                        ← actual generated output (unedited)
        instructions.md
        continuity.md
        sessions/.gitkeep
      ENABLE_OUTPUT.md               ← real terminal output of the enablement
    migrated-cursor-aider-project/   ← Mode C: migration from Cursor + Aider
      legacy/                        ← originals preserved
        cursor/.cursorrules
        cursor/.cursor/rules/api.mdc
        aider/.aider.chat.history.md
      memory/
        instructions.md              ← real output with migrated rules folded in
        continuity.md                ← real output with migration summary
        sessions/
          2026-06-08.md              ← Aider session migrated to our format
          2026-06-09.md
          2026-06-10.md
      ENABLE_OUTPUT.md               ← terminal output of the migration
    evolving-memory-example/         ← the review ritual in action
      continuity-before.md           ← live state before a review
      continuity-after.md            ← same file after (lean: archived + reactivated)
      decay-policy.md                ← the windows used in the example
      archive/2026-Q2.md             ← facts moved to cold storage
      archive/INDEX.md
      sessions/2026-06-20-141503.md  ← session log with Memory References + review summary
```

---

## Customising the Tool

The agent's behaviour is controlled entirely by `ENABLE.md` and `MIGRATE.md` —
plain markdown files. Edit them to:

- Change how detection works
- Add support for a new vendor (add a row to the table + a per-vendor section)
- Adjust conflict-handling defaults
- Change the report format

No code changes ever required.

---

## Three Modes at a Glance

```
ENABLE.md Step 3 →  Mode A: Fresh Enable   (nothing detected → templates fill from analysis)
                    Mode B: Already Ours   (memory/ exists → up-to-date skips; older → UPGRADE.md)
                    Mode C: Migrate Vendor (vendor files found → MIGRATE.md takes over)
```

---

## Changelog

Notable changes are recorded in the [CHANGELOG.md](CHANGELOG.md).

## License

Licensed under the [Apache License, Version 2.0](LICENSE). See the [`LICENSE`](LICENSE) file for the full text.
