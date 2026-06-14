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

## Quickstart — Enable + Migrate Any Repo

```bash
# 1. Clone this tool
git clone https://github.com/your-org/agent-memory
cd agent-memory

# 2. Open with your AI agent
claude        # or gemini, cursor, etc.

# 3. Say:
"AI enable this repo /path/to/your-project"

# 4. The agent will:
#    - Detect existing AI footprint (Cursor, Aider, etc.)
#    - Offer migration (with dry-run option)
#    - Analyse the repo (language, stack, type)
#    - Generate tailored memory files
#    - Install bootstrap files for all major agents
#    - Preserve originals under legacy/
#    - Report exactly what happened

# 5. Commit the result
cd /path/to/your-project
git add . && git commit -m "chore: AI-enable repo"
```

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

## Versioning & Upgrades

The tool is versioned (root `VERSION`, semver). Each enabled repo stamps
`.agent/version.md` with the version it's on, so re-running enablement can **upgrade
it in place** — additively, never destructively.

| Version | Capability |
|---|---|
| 1.0.0 | Fresh enable from templates (Mode A) |
| 2.0.0 | Vendor detection + migration (Mode C); idempotent re-runs (Mode B) |
| 3.0.0 | Evolving memory: fact metadata + ids, decay-policy, review ritual, archive |
| 3.1.0 | AI-infrastructure `.gitignore` propagated into enabled repos |
| 3.2.0 | Protocol clarifications: session = one log-write; metadata ownership; stack-fact altitude; after-session checklist |
| 3.3.0 | Supersession: facts that become *false* are marked `superseded` (replaced/invalidated) and archived flagged "superseded", not "faded" |
| 3.4.0 | Invariant verification: the review periodically prompts a human to re-confirm never-decay facts (`verify_invariants_every`) |

When you "AI enable" a repo that's already on an older version, Mode B detects the
drift and runs the upgrade ladder in `UPGRADE.md` (the user's entry point stays the
single "AI enable this repo" command). A missing `.agent/version.md` is treated as a
pre-versioning install and upgraded from the 2.x baseline.

---

The tool detects and migrates from these vendors:

| Vendor | Detected via | What's migrated |
|---|---|---|
| Claude Code | `CLAUDE.md` (non-ours), `.claude/` | Steering, JSONL session history |
| Cursor | `.cursorrules`, `.cursor/rules/*.mdc` | All steering files |
| Cline | `.clinerules`, `.cline/` | Steering, history |
| Roo Code | `.roorules`, `.roo/` | Steering, history |
| Aider | `.aider.conf.yml`, `.aider.chat.history.md`, `CONVENTIONS.md` | Steering, full chat history |
| Continue.dev | `.continue/config.json`, `.continue/sessions/*.json` | Steering, JSON sessions |
| Codeium / Windsurf | `.windsurfrules`, `.codeiumrc`, `.windsurf/` | Steering, history |
| GitHub Copilot | `.github/copilot-instructions.md` (non-ours) | Steering only (no history) |
| GPT / Codex | `AGENTS.md` (non-ours), `.codex/` | Steering, history |
| Zed AI | `.rules`, `.zed/` | Steering, history (with safety check) |
| Gemini CLI | `GEMINI.md` (non-ours), `.gemini/` | Steering, history |

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
  AGENTS.md                          ← memory protocol + enable dispatch
  CLAUDE.md / GEMINI.md              ← vendor bootstraps for this repo
  .cursorrules / .windsurfrules      ← Cursor / Windsurf bootstraps
  .github/copilot-instructions.md

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
