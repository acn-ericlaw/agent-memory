# Vendor Support

One shared memory, every major AI tool. "AI enable this repo" detects whatever AI footprint
already exists, folds it into the shared layer, and routes that vendor's agent to the one hub
(`AGENTS.md`) — originals preserved, never deleted.

## How neutrality works

agent-memory bets on **open standards**:

- **`AGENTS.md`** for steering — the hub every agent reads first.
- The open **Agent Skills** standard for capabilities — one `SKILL.md` shape.

Tools that adopt them plug in with little or no glue, which is why new vendors (Kiro, Copilot,
Antigravity) have shipped as point releases.

## Detected & migrated

A vendor's steering folds into `memory/`; checked-in chat history (e.g.
`.aider.chat.history.md`, `.continue/sessions/`) becomes dated session logs; a vendor's skills
are **promoted** into the neutral `agent-skills/` layer. Anything in your home folder stays in
your home folder.

Supported footprints include: **Claude Code, Cursor, GitHub Copilot, Gemini CLI, Google
Antigravity, Amazon Kiro, GPT / Codex, Cline, Roo Code, Aider, Continue.dev, Codeium /
Windsurf, Zed AI.**

## Native skill adapters

For runtimes with a native skill/command system, `sync skill adapters` regenerates thin
pointers across **six** targets (gitignored, never copies):

| Vendor | Adapter path |
|---|---|
| Claude Code | `.claude/skills/<name>/SKILL.md` |
| Gemini CLI | `.gemini/commands/<name>.toml` |
| Cursor | `.cursor/rules/<name>.mdc` |
| Amazon Kiro | `.kiro/steering/` (skill pointer) |
| GitHub Copilot CLI | `.github/skills/<name>/SKILL.md` |
| Google Antigravity | `.agents/skills/<name>/SKILL.md` |

!!! note "Antigravity vs. Gemini CLI"
    Antigravity (the Gemini CLI successor) reads workspace skills from **`.agents/skills/`**,
    **not** the old `.gemini/commands/*.toml`. The Gemini TOML adapter stays for now so Gemini
    CLI keeps working through the transition.

!!! warning "Copilot hot-reload"
    GitHub Copilot CLI loads `.github/skills/` at init, so a freshly-synced skill needs a
    `/restart` (or skills rescan) to appear. Claude / Cursor / Kiro don't.

## Vendor-specific notes

- **Enterprise IDEs (Kiro).** Per-machine vendor dirs (`.kiro/`, `.claude/`, …) are gitignored,
  so a fresh clone won't have them — run `sync skill adapters` after the agent loads the
  protocol. Human-gated commit hooks (like Kiro's) align with the deliberate-commit model.
- **GitHub Copilot.** Its `copilot-instructions.md` front-loads the explicit `memory/` read
  list (Copilot's Ask/Plan modes don't reliably chase a pointer chain) and leads with a
  first-run init block.
