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
| 4.33.3 | **`[secret-material]` security-review hardening:** closes four fresh-context findings: forge wrappers now invoke `memory-lint --strict` so advisory findings are observable and `AGENT_MEMORY_STRICT=1` genuinely blocks; the ALL-CAPS exemption is limited to enum-dimension keys instead of trusting uppercase secrets globally; quoted JSON/YAML assignments, Authorization headers, and embedded-placeholder bypasses now flag without echoing values; Mode C must redact migrated history and triage lint before commit. Python/Node remain byte-identical, 46 mirror tests each |
| 4.33.2 | **`[secret-material]`: backtick is a value delimiter:** the v4.33.1 enum-constant exclusion missed the form the motivating field line actually used — markdown inline code. In `` `key=VALUE` `` the closing backtick rode into the captured value, so the ALL-CAPS rule didn't match and the false positive survived; caught minutes after release by the 4.33.1 rung's own verify step against the live target. Every scanned memory surface is markdown — the assignment pattern now treats backticks like quotes; the mirror enum test uses the exact field form plus a backticked real-secret negative control. Also folded in (maintainer feedback on this release's own PR): the PR/MR description templates' rendered `<sub>` convention footer became an HTML comment — guides authors, never renders in a created PR/MR |
| 4.33.1 | **`[secret-material]`: ALL-CAPS enum constants are not credentials:** check 10's first field contact (the 2026-08-13 Mode B upgrades of two production repos) produced exactly one finding — a **false positive**: a log documenting Confluent's `bearer.auth.credentials.source` property with its enum value `OAUTHBEARER` (a source *type*). The credential-assignment pattern now treats ALL-CAPS identifiers (`OAUTHBEARER`, `SASL_SSL`, `STATIC_TOKEN`, …) as config constants — real credentials carry mixed case/symbols, and uppercase-only token shapes (e.g. AWS key ids) stay covered by the value-shape patterns independently. Fix the detector, don't sprinkle waivers through client repos; both runtimes at parity + mirror tests |
| 4.33.0 | **Session-log secret redaction — ritual rule + `memory-lint` `[secret-material]` advisory:** a client-side DLP scanner caught a live OAuth client secret in a committed session log — pasted smoke-test output, with nothing in the protocol between a rendered credential and `git push`. The after-session ritual now carries an explicit redaction rule (never write secrets or PII into `memory/`; redact pasted output to `(REDACTED)`; a committed secret is **exposed** — rotate it, redaction is not un-leaking), and `memory-lint` gains check 10: known token shapes, credential-key assignments (the rendered-JAAS class), emails, SSN / Luhn-verified card shapes, absolute home paths — scanning `sessions/` + `archive/` too, **never echoing the matched value**, waivable per-line with `lint:allow-secret-material`. Advisory by doctrine: the tool warns; the human redacts and rotates |
| 4.32.1 | **Mode A `last_session` contradiction fix:** a real enable + an adversarial protocol audit caught `ENABLE.md` disagreeing with itself — Step 5b still said a fresh (non-migrated) enable leaves `last_session: (none yet)`, while Step 5c (added later) writes a **first enable session log** for every fresh enable, making "(none yet)" false the moment the enable completes and blinding the multi-agent continuity check that reads the field. Step 5b now points `last_session` at the Step 5c log (`<today> | agent: <name> (<log filename stem>)`); the template seed became a `{{LAST_SESSION}}` placeholder; the schema marks `(none yet)` as legacy. The `rust-event-bus` fixture stays unedited (it truthfully predates Step 5c) behind a header note |
| 4.32.0 | **Azure DevOps forge support — own-pipeline ritual floor + PR template:** third forge, from a real field installation. Enable detects `dev.azure.com`/`*.visualstudio.com` and installs `.azuredevops/agent-memory-ci.yml` — a complete, self-contained pipeline (an existing `azure-pipelines.yml` is **never touched**) with native tri-state advisory (`##vso` warnings + "partially succeeded"; `AGENT_MEMORY_STRICT` gates) — plus `.azuredevops/pull_request_template.md` (auto-applies). Honest limit stated everywhere: a pipeline is a *resource* — the committed file is inert until a one-time `az pipelines create` binding (enable reports the command, runs it only at explicit user direction); Azure Repos ignores YAML `pr:` (Build Validation branch policy instead). Squash guidance gains the third branch (trailers dropped; re-add at completion) |
| 4.31.0 | **GitLab forge support — forge-aware ritual floor + MR template:** a GitLab-hosted field report showed `.github/` is ignored entirely there, killing exactly two installed artifacts — the **CI floor** (fresh clones were left with *no* ritual backstop, the gap v4.19.0 exists to close) and the **What/Why PR template**. Enable now detects the hosting forge and installs a matched set: GitLab gets `.gitlab/agent-memory-ci.yml` (same checks, advisory via `allow_failure: exit_codes`, `AGENT_MEMORY_STRICT` gates) wired from `.gitlab-ci.yml` (verbatim when absent; **add-only include** when pre-existing — never touches the repo's `workflow:rules`) + `.gitlab/merge_request_templates/Default.md`. Squash guidance now covers the forge **inversion**: GitHub piles trailers up, GitLab drops them (re-add at merge, or `%{all_commits}` in the squash template — `%{co_authored_by}` credits commit authors only). Local-tooling `.github/` files (Copilot) stay on every forge |
| 4.30.0 | **Stack-aware `.gitignore` build-output seed:** a greenfield field case (`mercury`, a Rust port started from an empty repo) — the installed `.gitignore` is deliberately AI-infrastructure-scoped, so when the stack landed later, the first `cargo build` polluted `git status` until `target/` was hand-added. `ENABLE.md` Step 7 now appends a **minimal, separately-sentineled build-output seed** when Step 4 detects a stack (Rust `target/`; Node `node_modules/`, `dist/`; Python venvs; Java/Kotlin `target/`, `build/`; .NET `bin/`, `obj/`) — add-only, de-duplicating (a no-op for repos that already ignore them). Greenfield enables instead carry the action in their seeded Open Thread, applied by the working agent when the stack lands. Explicit non-goal: a minimal seed, not gitignore management |
| 4.29.1 | **Template import blocks → `{{BOOTSTRAP_IMPORTS}}` placeholder:** cross-vendor dogfooding of v4.29.0 (Copilot assessment, corroborated on Claude Code) found tool-repo instruction bleed-through — runtimes that auto-load directory-scoped instruction files picked up `templates/CLAUDE.md`, whose live `@`-imports (relative to the containing file) pulled the placeholder template stubs into context as instructions. The templates now hold a `{{BOOTSTRAP_IMPORTS}}` placeholder; `ENABLE.md` Step 6 expands the per-vendor literal block at install — installed output byte-identical to v4.29.0. Tool-repo containment only; targets just stamp the version |
| 4.29.0 | **Before-session context presence — bootstrap `@`-imports + an opt-in SessionStart recipe:** a child-repo field report showed agents skipping the before-session read chain (`CLAUDE.md → AGENTS.md → memory/*`) under task pressure — the v4.19.0 trigger layer reinforces only the *after*-session rituals (git/CI has no session-start moment), so the read rested on prompt adherence. The `CLAUDE.md`/`GEMINI.md` bootstrap pointers now **import** the hub + core memory files (`@AGENTS.md`, `@memory/instructions.md`, `@memory/continuity.md`, `@memory/vision.md`), making them structurally present at session start on import-capable runtimes — markdown-only, no hooks; `AGENTS.md` stays vendor-neutral. An opt-in Claude Code `SessionStart` injection recipe (for `memory/sessions/` recency — imports can't express dynamic paths) lands in the tool-side hook doc, never installed by default. Presence is guaranteed; *attendance* remains agent judgment |
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
  .github/pull_request_template.md   ← PR description convention: What / Why (installed on GitHub-hosted targets)
  .github/workflows/agent-memory.yml ← CI floor: memory-lint + session-log check (GitHub half; GitLab twin under templates/.gitlab/)
  .githooks/                         ← vendor-neutral ritual triggers (committed; agent-activated)
    post-commit · init.sh · README.md
  .gitignore / .gitattributes        ← AI-infra ignores + LF pinning (merged into targets)
  CHANGELOG.md / LICENSE             ← official release notes / Apache-2.0

  templates/                         ← installed into target repos
    AGENTS.md, CLAUDE.md, GEMINI.md, ...
    .gitlab-ci.yml                   ← GitLab CI floor root wiring (v4.31.0; installed when target has none)
    .gitlab/agent-memory-ci.yml      ← GitLab CI floor job (advisory; forge twin of the GitHub workflow)
    .gitlab/merge_request_templates/Default.md  ← MR What / Why template (GitLab)
    .azuredevops/agent-memory-ci.yml ← Azure DevOps CI floor (own pipeline; one-time activation)
    .azuredevops/pull_request_template.md  ← PR What / Why template (Azure DevOps)
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
