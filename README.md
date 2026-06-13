# agent-memory

A no-code AI memory system, AI-enablement tool, **and migration tool** —
all in one repo. Markdown only. No code to run. No API keys.

Three things in one:

1. **A memory system** — clone it, open with your agent, work normally.
   Context persists across sessions and across different AI agents.

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
  ENABLE.md                          ← protocol: detect, migrate, generate
  MIGRATE.md                         ← per-vendor migration rules
  AGENTS.md                          ← memory protocol + enable dispatch
  CLAUDE.md / GEMINI.md              ← vendor bootstraps for this repo
  .cursorrules / .windsurfrules      ← Cursor / Windsurf bootstraps
  .github/copilot-instructions.md

  templates/                         ← installed into target repos
    AGENTS.md, CLAUDE.md, GEMINI.md, ...
    memory/
      instructions.md                ← with {{placeholders}}
      continuity.md                  ← with {{placeholders}}
      sessions/.gitkeep
    .agent/schema.md

  memory/                            ← this tool's own memory layer
    instructions.md
    continuity.md
    sessions/

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
                    Mode B: Already Ours   (memory/ exists in our format → idempotent skip)
                    Mode C: Migrate Vendor (vendor files found → MIGRATE.md takes over)
```
