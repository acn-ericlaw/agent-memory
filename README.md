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
| 4.22.0 | **Discovery, consent & merge-friendliness + `MERGE.md`** — four bundled, additive features consolidated into one release (per a new *one version per release* policy): a curious **knowledge harvest** at enable (recursive doc-tree descent + repo-root sweep, budgeted with disclosure); a fresh-enable **advisory + informed-consent exec summary** with a standard-vs-`/init`-depth **discovery choice** (deep analysis written to the neutral memory layer, never a vendor file); **`continuity.md` merge-friendliness** (`status` is a short current-state line, *not* a changelog; keep-both / take-later merge conventions; `memory-lint` **check 7** errors on a leftover conflict marker in the live memory files); and **`MERGE.md`**, a tiered, human-gated, `never-pick-a-winner` git-conflict-resolution protocol. Hardened end-to-end by a cross-vendor fresh-context review (Gemini 3.1 Pro critiqued + re-validated the applied fixes) |
| 4.21.0 | **Google Antigravity (`agy`) skills adapter:** a **6th** skills adapter target `.agents/skills/<name>/SKILL.md` — Antigravity (the Gemini CLI successor) merged custom commands into the open Agent Skills standard and reads `.agents/skills/`, **not** the old `.gemini/commands/*.toml`, so `agy` reported `/<command>` as not found despite `init.sh` populating the Gemini adapter. `sync skill adapters` now writes six adapters (same `SKILL.md` shape as the Claude/Kiro/Copilot adapter); `.agents/` is gitignored. The `.gemini/commands` TOML adapter stays for now so Gemini CLI keeps working during the transition. Antigravity added to the Mode C detection/migration + bootstrap tables. Found dogfooding `agy` on an enabled repo |
| 4.20.3 | **memory-lint catches an empty/malformed version manifest:** a deterministic `check_version_manifest` ERROR (both runtimes, at parity, with tests) so a present-but-empty/malformed `.agent/version.md` fails the lint floor (CI + reviews) instead of silently breaking Mode B upgrade detection. Closes the loop on the v4.20.1 bug (a truncating stamp one-liner emptied a target's `version.md` → an agent misread the version). A *missing* `version.md` stays valid (pre-versioning baseline) and is not flagged |
| 4.20.2 | **Windows line-ending hardening:** a `.gitattributes` pins `*.sh` + `.githooks/*` to LF so Git for Windows (`core.autocrlf=true`) doesn't rewrite them to CRLF and break bash (`bad interpreter: …^M`). Installed/merged into targets additively. Makes the bootstrap + hooks robust on Windows (Git Bash / WSL), not luck-of-the-default. From a Copilot Windows-feasibility check |
| 4.20.1 | **Self-init in `copilot-instructions.md`:** v4.20.0's self-init reached Claude but not Copilot CLI (its `start` front-loads `copilot-instructions.md` + summarizes). Folds the first-run init into the top of `copilot-instructions.md` so Copilot runs `bash .githooks/init.sh` before summarizing; the `init.sh` fallback + CI floor are unchanged |
| 4.20.0 | **First-run init for fresh clones:** a Copilot dogfood showed a fresh clone self-initializes the *memory* bootstrap but not the gitignored adapters or the (unactivated) hook. Adds **`.githooks/init.sh`** (one idempotent command: regenerate adapters + activate the hook) + an **`AGENTS.md` self-init note** so the agent does it on its first session — one step (or one human command) instead of two. CI stays the zero-config floor |
| 4.19.0 | **Vendor-neutral ritual triggers:** the after-session ritual no longer depends on the agent self-triggering (which failed in practice — skipped even with Claude; Copilot-only teams had no triggers). Enable installs a committed **`.githooks/post-commit`** (auto-stubs a session log when a commit does real work without one; re-syncs adapters) — **agent-activated** via `core.hooksPath`, zero manual user step — plus a **CI floor** (`.github/workflows/agent-memory.yml`: `memory-lint` + advisory session-log check on push/PR, zero per-user setup). Advisory by default (opt-in `AGENT_MEMORY_STRICT` gate); `no-build-step-agent-run` holds (git/CI invoke them; the tool runs nothing). Honest limit: git can't auto-run hooks on a bare clone → CI is the backstop. Design: `docs/DESIGN-ritual-triggers.md` |
| 4.18.0 | **`sync skill adapters` is now a runnable script:** a new built-in **`sync-adapters`** skill ships a deterministic adapter-regeneration script (Node + Python at parity) that (re)writes the five vendor adapters for every skill and prunes the orphans it generated. Replaces the prose-recipe-only sync that agents (e.g. Copilot CLI / Gemini) struggled to *run* — they hunted for a non-existent npm/MCP command and flailed. Enable + every Mode B re-enable invoke the script; an agent also triggers it by description. Consistent with `no-build-step-agent-run` (same category as the `memory-lint` script). Surfaced dogfooding `~/sandbox/simple-proxy` |
| 4.17.0 | **GitHub Copilot CLI skills adapter:** a **5th** skills adapter target `.github/skills/<name>/SKILL.md` — Copilot CLI follows the open Agent Skills standard (same `SKILL.md` shape as the Claude/Kiro adapter) and auto-matches by `description` (also accepts an explicit `/<name>`). `sync skill adapters` now writes five adapters; `.github/skills/` is gitignored **path-scoped** (the rest of `.github/` — `copilot-instructions.md`, `workflows/` — stays tracked). Copilot also gains skills in the Mode C detection/migration table (`.github/skills/`, `.agents/skills/` → `agent-skills/`), and the Copilot steering template now **front-loads the `memory/` read list** + a manual-upkeep note (Copilot's Ask/Plan modes don't follow a pointer chain or auto-maintain memory — reliability over DRY, Copilot-scoped). Found dogfooding `~/sandbox/simple-proxy`, where Copilot CLI couldn't discover a skill authored only in `agent-skills/` |
| 4.16.1 | **Session filename drift fix:** two gaps allowed date-only session filenames (`YYYY-MM-DD.md`): the protocol said "or equivalent" (allowing context `currentDate`), and `memory-lint` had no filename check. Fixed: explicit `date -u` requirement in `templates/AGENTS.md` + `schema.md`; new `check_session_filenames` warning (check 5) in both linter runtimes with tests |


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
    hello-world/                     ← dogfood demo skill
    (the four built-ins ship provenance: agent-memory-builtin and install into every enabled repo)

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
