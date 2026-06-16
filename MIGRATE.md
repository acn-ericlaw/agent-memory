# Migration Protocol

This file tells the AI agent how to migrate existing vendor-specific AI memory
files into the unified `agent-memory` format. Read it when `ENABLE.md` Step 3
selects Mode C (Migrate from Vendor).

---

## Migration Principles

0. **Target-repo scope only — this is non-negotiable.**
   All read, move, and write operations during migration are restricted to
   files **inside the target repository directory**. Never read from, modify,
   move, or even list contents of:
   - The user's home directory (`~`, `$HOME`, `%USERPROFILE%`)
   - User-global config directories (`~/.config/`, `~/.claude/`, `~/.aider/`,
     `~/.continue/`, `~/.cursor/`, `~/.codeium/`, `~/.gemini/`, etc.)
   - macOS Application Support (`~/Library/Application Support/`)
   - Windows AppData (`%APPDATA%`, `%LOCALAPPDATA%`)
   - System-wide config (`/etc/`, `C:\ProgramData\`)
   - Any path that resolves outside the target repo root, including via symlinks
     (resolve symlinks before reading — if the resolved path leaves the repo,
     skip the file and note it in the report)

   If a vendor's primary storage is user-global (Cursor chat, Continue user
   profiles, Aider's per-user history outside the repo, etc.), state this in
   the migration report and migrate **only what exists inside the target repo**.
   The user's global tooling is left completely untouched.

   **Why:** the user's `~/` is *their* personal AI environment — the vendor
   they chose, their history, their settings. They will keep using it after
   enablement. The repo's `memory/` is the *team's* shared collaboration layer,
   committed to git, designed so contributors using different AI vendors can
   share project context without disturbing each other's personal setups.
   These two layers are meant to coexist, not replace each other.

1. **Never delete vendor files.** Move originals to `legacy/<vendor>/` in the
   target repo, preserving their relative paths.
2. **Append, don't replace.** When folding vendor steering content into
   `memory/instructions.md`, append under clear section headers — do not
   discard vendor rules.
3. **Convert chronologically.** Session and history data must become dated
   `memory/sessions/YYYY-MM-DD-HHMMSS.md` files. Use the original session
   timestamp (UTC, colons omitted) as the filename. If the original timestamp is
   unavailable, use the file mtime. Title line: `# Session (startZ - endZ)`; when
   only one timestamp is available, use it for both. Order files chronologically;
   lexicographic sort = time order.
4. **Mark migrated content.** Every migrated session block must begin with
   `> Migrated from <vendor> on <today's-date>`.
5. **One pass per vendor.** Process each detected vendor independently —
   if one fails, continue with the others and report what was skipped.
6. **Promote skills, don't flatten.** Vendor skill bundles (capabilities, e.g.
   `.claude/skills/`) are *promoted* into the neutral, committed `agent-skills/` layer
   (Section B2) with per-vendor adapters regenerated — never folded into
   `memory/instructions.md`.

---

## Detection Table

For each row, if any "Indicator file/dir" exists in the target repo,
the vendor is present. Apply the rules in that row's migration section.

| Vendor | Indicator files / directories |
|---|---|
| Claude Code | `CLAUDE.md` (non-ours), `.claude/`, `.claude/settings.json`, `.claude/projects/`, `.claude/skills/` |
| Cursor | `.cursorrules`, `.cursor/`, `.cursor/rules/*.mdc` |
| Cline | `.clinerules`, `.cline/` |
| Roo Code | `.roorules`, `.roo/` |
| Aider | `.aider.conf.yml`, `.aider.chat.history.md`, `.aider.input.history`, `CONVENTIONS.md` |
| Continue.dev | `.continue/`, `.continue/config.json`, `.continue/sessions/` |
| Codeium / Windsurf | `.windsurfrules`, `.codeiumrc`, `.windsurf/` |
| GitHub Copilot | `.github/copilot-instructions.md` (non-ours) |
| GPT / Codex | `AGENTS.md` (non-ours), `.codex/` |
| Zed AI | `.rules` (when not a different tool's file), `.zed/` |
| Gemini CLI | `GEMINI.md` (non-ours), `.gemini/` |

**How to tell "ours" vs "non-ours" for shared filenames (CLAUDE.md, AGENTS.md, etc.):**
Open the file. If it contains the line `This project uses the agent-memory
shared memory system` or references `memory/instructions.md`, it's ours — skip
migration. Otherwise treat as vendor content to migrate.

---

## General Migration Workflow

For each detected vendor:

### A. Archive originals

Create `legacy/<vendor>/` in the target repo (e.g. `legacy/cursor/`).
Move (do not copy) every vendor file into that directory, preserving relative
paths inside it. Examples:

```
.cursorrules            →  legacy/cursor/.cursorrules
.cursor/rules/api.mdc   →  legacy/cursor/.cursor/rules/api.mdc
.aider.chat.history.md  →  legacy/aider/.aider.chat.history.md
```

**Git-aware move:** check whether the target repo is a git repository
(`git -C <repo> rev-parse --is-inside-work-tree 2>/dev/null`). If it is,
check each file's tracking status (`git -C <repo> ls-files --error-unmatch
<file>`). Use `git mv` for tracked files so git preserves the rename in history;
use a plain filesystem move for untracked files. If `git mv` fails (e.g. the
destination directory doesn't exist yet), create the `legacy/<vendor>/` directory
first, then retry. Record in the report whether each file was moved with `git mv`
or a plain move.

### B. Extract steering content → `memory/instructions.md`

Read the vendor's steering file (the "instructions" equivalent). Before writing
anything, assess its quality:

**Does the file contain project-specific context** — what the project is, its
tech stack, architecture, key decisions? If yes, it is *project instructions*
and warrants the integration path. If it contains only coding conventions, style
rules, or AI behavioral directives with no project context, use the verbatim path.

**Integration path — project instructions:**

Map content into the appropriate sections of `memory/instructions.md` instead
of appending it verbatim:

- Project description / purpose → "What this project is" section
- Tech stack, frameworks, tools → stack section
- Architecture, module layout → relevant descriptive sections
- Coding conventions, style rules → conventions section
- AI-specific behavioral directives that don't fit the schema → append under
  `## Migrated rules from <vendor>` (these are the residue after integration)

If `memory/instructions.md` does not yet exist, create it from the template and
fill the relevant sections from the vendor content.

**Verbatim path — AI rules only:**

If the content is non-trivial (more than a one-line pointer) but contains no
project-specific context, append it to `memory/instructions.md` under:

```markdown
## Migrated rules from <vendor>

<verbatim content, lightly cleaned of vendor-specific syntax>
```

If `memory/instructions.md` does not yet exist, create it from the template and
add the section after the standard headings.

### B2. Promote skills (capabilities) → `agent-skills/`

Vendor **skill bundles** are *capabilities*, not steering and not history — currently
Claude Code's `.claude/skills/<name>/SKILL.md` (each a `name` + `description` + a
procedure, plus optional bundled scripts). Do **not** flatten them into
`memory/instructions.md`. Instead **promote** each into the neutral, committed capability
layer:

- For each `<name>`, write `agent-skills/<name>/SKILL.md` — keep the procedure as-is and
  normalize the frontmatter to the neutral minimum (`name`, `description`). Copy any
  bundled scripts to `agent-skills/<name>/scripts/`, preserving relative references.
- The verbatim original is preserved by Section A's move to `legacy/<vendor>/` — so
  `agent-skills/` is the promoted, shared copy and `legacy/` keeps the untouched original.
- After promoting, **regenerate the per-vendor adapters** (Claude / Gemini / Cursor) from
  each neutral skill exactly as `ENABLE.md` Step 5h specifies — thin pointers living in the
  gitignored vendor dirs.

`agent-skills/` is tracked (Step 7 keeps it committed); the adapter dirs are ignored and
regenerated per machine, so the neutral skill stays the single source of truth. See
`docs/DESIGN-skills-layer.md`.

**Vendor dirs serve double duty — order matters.** `.cursor/rules/` and `.gemini/` are
both *migration sources* (their existing steering/history is archived to `legacy/` in
Section A) **and** *adapter targets* (Step 5h writes fresh adapters there). Always do
Section A first (move the originals to `legacy/`), then generate adapters into the
now-cleared vendor dirs — so a migrated rule and a regenerated adapter never collide. A
migrated Cursor rule lives in `legacy/cursor/`; a generated skill adapter lives in
`.cursor/rules/` and points at `agent-skills/`.

**Collision guard.** If a top-level `agent-skills/` already exists in the target with
unrelated content, do **not** overwrite — raise a `- [ ] Contradiction:` Open Thread
(`never-pick-a-winner`) and stop.

### C. Convert history → `memory/sessions/`

Read the vendor's history/session data and convert each session or chat into
the standard session log format. Each converted session gets its own file:
`memory/sessions/YYYY-MM-DD-HHMMSS.md` using the original session timestamp
(UTC, colons omitted). Multiple sessions on the same date naturally sort by time.

Standard format for a migrated session:

```markdown
# Session (<original-timestamp>Z - <original-timestamp>Z)

> Migrated from <vendor> on <YYYY-MM-DD-of-migration>
> Original timestamp: <vendor's timestamp if available>

**Agent:** <vendor agent name>
**User:** (migrated history — user context not preserved)

## Summary
<extracted summary, see per-vendor rules below>

## Original excerpt
<first ~200 chars of the conversation if useful>
```

Vendor-specific extraction rules are in the sections below.

### D. Note in continuity

In `memory/continuity.md`, add to Open Threads:

```markdown
- [ ] Review migrated sessions from <vendor> (under memory/sessions/)
- [ ] Verify legacy/<vendor>/ contents — delete after confirming migration is complete
- [ ] Review promoted skills under agent-skills/ — confirm each SKILL.md + regenerated adapters (only if the vendor had skills)
```

---

## Per-Vendor Protocols

> **Before writing any steering content**, apply the quality assessment in
> Section B above. Per-vendor instructions below describe what to read and
> archive — the integration vs. verbatim decision is always made by Section B.

### Claude Code

**Steering:** `CLAUDE.md` (non-ours version)
- Apply the Section B quality assessment. A hand-written `CLAUDE.md` often
  contains real project instructions and warrants the integration path, not
  verbatim append.

**History:** `.claude/projects/<project-id>/sessions/` or similar
- Claude Code stores sessions as JSONL files (`<uuid>.jsonl`).
- Each line is a JSON object representing a message. Parse line-by-line.
- Group all lines from one JSONL file as one session.
- Use the file's mtime (or first message timestamp if embedded) for the date.
- Summary: take the first user message + last assistant message, condense to 2–3 sentences.

**Settings:** `.claude/settings.json`
- Archive verbatim. Do NOT attempt to map settings to our format — different concept.

**Skills:** `.claude/skills/<name>/SKILL.md` (+ any bundled scripts)
- **Promote** to the neutral `agent-skills/` layer per Section B2 — do NOT flatten into
  instructions (skills are *procedures*, not steering). Preserve the original under
  `legacy/`; regenerate the Claude/Gemini/Cursor adapters per `ENABLE.md` Step 5h.

---

### Cursor

**Steering:** `.cursorrules` and any `.cursor/rules/*.mdc`
- `.cursorrules`: append under `## Migrated rules from Cursor`.
- `.cursor/rules/*.mdc`: each `.mdc` file is a separate scoped rule. Append each
  as its own subsection: `### Migrated rule: <filename without extension>`.

**History:** Cursor stores chat history in `~/Library/Application Support/Cursor/`
or `%APPDATA%\Cursor\` — **outside the repo**. Do NOT touch user-global storage.
Only migrate repo-local files. Note this in the report:
> "Cursor chat history is stored globally per user, not in the repo.
> No session data to migrate."

---

### Cline

**Steering:** `.clinerules`
- Append under `## Migrated rules from Cline`.

**History:** `.cline/` directory (if present in repo).
- Look for any `.json` or `.jsonl` files. Treat each conversation file as one session.
- Use file mtime for date grouping.

---

### Roo Code

**Steering:** `.roorules`
- Append under `## Migrated rules from Roo Code`.

**History:** `.roo/` (if present). Same approach as Cline.

---

### Aider

**Steering:** `CONVENTIONS.md`, `.aider.conf.yml`
- `CONVENTIONS.md`: append under `## Migrated rules from Aider (CONVENTIONS.md)`.
- `.aider.conf.yml`: archive verbatim; do not try to map YAML config to our format.

**History:** `.aider.chat.history.md`
- This is markdown with chat blocks separated by `# aider chat started at <timestamp>`.
- Split on that pattern. Each block becomes one session.
- Extract the timestamp from the header line and use it for date grouping.
- Summary: take the first user prompt and condense.

**Input history:** `.aider.input.history`
- Archive only. Don't migrate to sessions — this is just prompt history,
  not full conversations.

---

### Continue.dev

**Steering:** `.continue/config.json`
- Parse JSON. If it contains a `customCommands` or `systemMessage` field, extract
  those values and append under `## Migrated rules from Continue.dev`.
- Archive the full config under `legacy/continue/config.json`.

**History:** `.continue/sessions/*.json`
- Each file is one session in JSON. Read all messages, format as our session schema.
- Use the file's mtime for date grouping (or `sessionStart` field if present).

---

### Codeium / Windsurf

**Steering:** `.windsurfrules`, `.codeiumrc`
- Both: append under `## Migrated rules from Windsurf`.

**History:** `.windsurf/` (if present in repo) — apply general workflow.
- Most Windsurf history lives in user-global storage; if so, note in report.

---

### GitHub Copilot

**Steering:** `.github/copilot-instructions.md` (non-ours)
- Append content under `## Migrated rules from GitHub Copilot`.

**History:** None — Copilot does not store session history in the repo.
Note this in the report.

---

### GPT / Codex / OpenAI agents

**Steering:** `AGENTS.md` (non-ours)
- Append under `## Migrated rules from AGENTS.md (pre-existing)`.

**History:** `.codex/` (if present) — apply general workflow.

---

### Zed AI

**Steering:** `.rules`
- Caution: `.rules` is also used by other tools. Open the file. If it references
  Zed, AI assistants, or contains conversational instructions to an AI, migrate.
  If it looks like a build tool config, **skip and warn the user**.

---

### Gemini CLI

**Steering:** `GEMINI.md` (non-ours)
- Append under `## Migrated rules from Gemini`.

**History:** `.gemini/` (if present) — apply general workflow.

---

## JSONL History Conversion — Reference

Several vendors use JSONL (one JSON object per line) for chat history. Generic
conversion:

```
For each .jsonl file:
  messages = [parse(line) for each line]
  date     = earliest timestamp in messages (or file mtime as fallback)
  session  = group(messages by 30-minute idle gap)
  for each grouped session:
    write to memory/sessions/<date>-<hhmmss>.md as a session block
```

Be conservative with summaries — better to say "Migrated session, content
preserved in legacy/" and let the user review than to hallucinate a summary
from incomplete data.

---

## Conflict Resolution

If multiple vendors have steering files that contradict each other (e.g.
`.cursorrules` says "use 2-space indents" but `CLAUDE.md` says "use tabs"),
preserve both in their migrated sections and add an Open Thread:

```markdown
- [ ] Resolve contradictory rules from migrated vendors
  - Cursor:       2-space indents
  - Claude Code:  tabs
```

Do not pick a winner. Let the user decide.

---

## Dry-Run Mode

If the user said "dry-run" in Step 3 of `ENABLE.md`, do the full detection and
print exactly what would be moved/created/appended, but **make no file changes**.
End with:

```
This was a dry run. No files were modified.
Run "AI enable this repo <path>" without dry-run to apply.
```
