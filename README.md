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

This loads the one-line universal shim, which points to `memory/PROTOCOL.md` before any
substantive work. It is the reliable entry point on every vendor — and is **required** in enterprise IDEs
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
| 4.39.0 | **Merge-scale memory — threads as files:** from maintainer field reports, `continuity.md` merge conflicts became regular business as team adoption grew, concentrated in `## Open Threads` and the `last_session` scalar. Structural fix, no merge-time machinery: each Open Thread lives in its own `memory/open-threads/thread-<id>.md` (filename = the fact id; the directory is the index, like `sessions/`) so parallel work on different threads cannot conflict, while a same-thread edit conflicts per-file — the MERGE.md Tier 2 human gate, preserved by design; `last_session` is dropped (derivable from the newest session log); archive files union-merge via `.gitattributes`; reviews run serialized. All three built-in script pairs treat thread files as fact surfaces; new lint checks `[thread-file]`, `[duplicate-id]`, `[duplicate-state-key]` (the last absorbed from PR #27 — credit: Roland Heusser); `tests/test_thread_layout_merge.sh` pins the merge contract with real git merges. Design record: `docs/DESIGN-merge-scale.md` |
| 4.38.1 | **Scanner-neutral guidance constant:** an enterprise security pipeline (Snyk) in a downstream field deployment rejected builds, flagging `memory-lint`'s prose guidance constant as a hardcoded secret — that detector class keys on identifier-contains-SECRET + string-literal assignment. Renamed (`GUIDANCE`) in both runtimes with zero output or behavior change (byte-identical lint results before/after, python and node in agreement); each mirror suite gains a script-hygiene self-check that scans the shipped scripts for the flagged identifier shape (trigger words assembled at runtime, so the suites never commit the shape), and `SKILLS.md` records the house rule: prose-constant identifiers in shipped scripts stay scanner-neutral. Downstream interim edits converge to zero diff on the next re-copy |
| 4.38.0 | **Onboarding efficiency — consumer routing + close-record economy:** from a fresh-agent assessment of an enabled repo that is *also a consumable product* (mercury-composable): consumers were routed into contributor memory, and 64% of continuity was completed-thread ship narrative. The root shim gains a **sanctioned contributor/consumer fork** (structure-checked by the reconcile: canonical read-imperative + repo-local consumer entry, a ≤ 16-line routing stub sized to the live field artifact — anything else stays drift with the PRE-APPLY stop), and the target protocol opens with a consumers-exit-here step-0. **Close-record economy:** completed `[x]` threads are specced as 3–6-line stubs (full narrative lives in the origin session log), `REVIEW.md` condenses oversized records at review time, and the new `[closed-thread-bloat]` advisory (knob: `closed_narrative_max_lines`, default 150) measures exactly that class. Plus an optional ready-to-work checkpoint in Work-from-intent |
| 4.37.0 | **Enterprise-efficient protocol activation:** root `AGENTS.md` is now an exact one-line pointer to `memory/PROTOCOL.md`, cutting the enterprise IDE auto-loaded surface from ~20 KB to 61 bytes. The relocated tool and target protocols are ordered for activation, compressed without weakening directives (both under 11.2 KB), and directly imported by capable bootstraps. Reconcile installs the target protocol before the shim and enforces the PRE-APPLY boundary: fresh enable and upgrade preserve pre-existing protocol destinations, customized roots, and hook behavior, refusing every write until the protected files are safe and explicitly confirmed |
| 4.36.0 | **Composable Git hook dispatchers:** `.githooks/pre-commit` and `post-commit` are now stable run-parts-style dispatchers; agent-memory's secret guard and ritual capture live in ordered `*.d/50-agent-memory-*` fragments. Executable fragments run in deterministic filename order, every layer gets a chance to report, and the first non-zero status is returned (so any failing pre-commit fragment blocks; Git still ignores post-commit status). Other hook layers can occupy before/after slots without replacing an entrypoint; focused tests pin ordering, filtering, argument forwarding, continue-after-failure, and status propagation. Fragment LF rules travel to Windows targets |
| 4.35.0 | **Target-state reconcile — enable/upgrade in O(diff), not O(steps/rungs):** from a greenfield field case (a fresh Mode A enable of a nearly-empty repo took >10 minutes; Mode B paid O(rungs-behind) across a ladder of 80). The stepwise protocol becomes **declarative convergence**: `MANIFEST.md` (tool-side) declares every installed artifact as one row — target, source, policy (`verbatim` / `verbatim-dir` / `seed-copy` / `sentinel-merge` / `seed-generate` / `stamp`), forge — plus a **Semantic steps** table distilling the ladder's 14 non-mechanical migrations, version-gated. A runnable reconcile helper (`scripts/reconcile.py` + `.mjs`, byte-parity, 25 mirror tests each) diffs a target against it: dry-run by default (the consent artifact), one `--apply` pass for the mechanics, and a printed work-list for the judgment half (seeding, vision gate, hook activation, GitLab root-CI wiring, semantic steps, the closing stamp — which the script deliberately never writes). Never deletes, never touches seeded/user files, never edits a pre-existing `.gitlab-ci.yml`; drift on tool-owned files becomes *visible* before re-copy (live probe: surfaced 11 managed `.gitignore` entries no rung ever back-filled). The ladder stays as the per-version record; `--check-manifest` gates every release's manifest lockstep |
| 4.34.2 | **`[secret-material]` self-knob FP fix:** the pre-commit guard's blocking message prints `AGENT_MEMORY_SECRET_GUARD=advisory` — and any memory file documenting that guidance then flagged as a credential assignment (the key contains SECRET; the tool taught a phrase, then blocked its quotation). Now an exact-key, value-constrained exemption covers only the knob's documented settings (`advisory`/`enforcing`, trailing punctuation tolerated — the guard's own line ends `…=advisory)`); any other value under that key still flags. Verbatim mirror fixtures both runtimes (50 each). Also recorded: AWS's canonical doc-example keys still flag by design — waive visibly, no invisible whitelist |
| 4.34.1 | **Secret-guard output readability:** field feedback from the maintainer's own regression test of the enforcing guard — every finding line repeated the same advisory tail. `[secret-material]` finding lines now end at `(N hit(s), first at line N)`; the redact/rotate/history guidance appears **once per run** — in the pre-commit hook's `-> fix it` footer (with a blank separator line), and as a single trailer in `--scan-files` and full-lint runs. Both runtimes at parity; the hook's grep contract unchanged |
| 4.34.0 | **Pre-commit secret guard — prevention, not detection, on both surfaces:** the v4.33.x incident's *origin* was never a memory file — the credentials entered inside a Postman JSON and an OpenShift YAML, then contaminated a session log via a dry-run. The committed `.githooks/pre-commit` scans the **staged** content (the index — exactly what the commit would publish; only what THIS commit stages) of `memory/**.md` (full profile) **and of config files** (`.json`/`.yml`/`.yaml`/`.properties`/`.toml`/`.ini`/`.env*` — credential-class checks) **before the commit exists**; the CI floor's three forge wrappers run the matching changed-config scan on push (`memory-lint --scan-files`). The guard **enforces by default** — findings block the commit, the deliberate exception to the advisory doctrine (secrets carry irreversible after-the-fact cost); `AGENT_MEMORY_SECRET_GUARD=advisory` opts down, `--no-verify` bypasses once; JSON/properties exemptions in the committed `.agent/secret-scan-ignore`; the CI floor stays advisory (`AGENT_MEMORY_STRICT=1` gates). Detector tuned on a **661-file live-corpus probe to zero false positives** (single-brace + GH-Actions templates, `demo`/`test` placeholder words, placeholder-fallback defaults, dotted route refs, JAAS `;` delimiter, Postman split-pair pattern); 49 mirror tests per runtime |
| 4.33.4 | **`[secret-material]`: reject non-empty template defaults:** v4.33.3's broad `${…}` exemption accepted literal fallbacks, allowing `client_secret=${CLIENT_SECRET:-RealSecret123}` to bypass assignment detection. `${NAME}`, `${NAME:}`, and dotted references remain safe; non-empty defaults flag without echoing values. Python/Node remain byte-identical, 46 mirror tests each |

When you "AI enable" a repo that's already on an older version, Mode B detects the
drift and **reconciles it against the current target state** (`MANIFEST.md`) — one
diff-and-apply pass plus the few version-gated semantic steps, with `UPGRADE.md` as the
per-version record (the user's entry point stays the single "AI enable this repo"
command). A missing `.agent/version.md` is treated as a pre-versioning install and
upgraded from the 2.x baseline.

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
  UPGRADE.md                         ← in-place version-upgrade ladder: per-version record + semantic-step detail (tool-only)
  MANIFEST.md                        ← declarative install target state + semantic-steps index (tool-only, v4.35.0)
  scripts/                           ← reconcile helper: reconcile.py / reconcile.mjs + mirror tests (tool-only)
  DECAY.md                           ← evolving-memory rules (installed into targets)
  REVIEW.md                          ← the review ritual (installed into targets)
  SKILLS.md                          ← skills reference: author/sync/adopt/sanity (installed; on-demand)
  MERGE.md                           ← git-conflict resolution protocol (installed; on-demand)
  AGENTS.md                          ← one-line universal pointer to memory/PROTOCOL.md
  CLAUDE.md / GEMINI.md              ← vendor bootstraps for this repo
  .cursorrules / .windsurfrules      ← Cursor / Windsurf bootstraps
  .github/copilot-instructions.md    ← GitHub Copilot bootstrap
  .github/pull_request_template.md   ← PR description convention: What / Why (installed on GitHub-hosted targets)
  .github/workflows/agent-memory.yml ← CI floor: memory-lint + session-log check (GitHub half; GitLab twin under templates/.gitlab/)
  .githooks/                         ← composable ritual triggers (committed; agent-activated)
    pre-commit / post-commit         ← deterministic fragment dispatchers
    pre-commit.d/ / post-commit.d/   ← ordered hook fragments (managed behavior at 50-*)
    init.sh · README.md
  .gitignore / .gitattributes        ← AI-infra ignores + LF pinning (merged into targets)
  CHANGELOG.md / LICENSE             ← official release notes / Apache-2.0

  templates/                         ← installed into target repos
    AGENTS.md, CLAUDE.md, GEMINI.md, ...
    memory/PROTOCOL.md               ← canonical target-only memory protocol
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
    PROTOCOL.md                      ← dual-mode tool protocol + session lifecycle
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
                    Mode B: Already Ours   (memory/ exists → up-to-date skips; older → reconcile vs MANIFEST.md + semantic steps)
                    Mode C: Migrate Vendor (vendor files found → MIGRATE.md takes over)
```

---

## Changelog

Notable changes are recorded in the [CHANGELOG.md](CHANGELOG.md).

## License

Licensed under the [Apache License, Version 2.0](LICENSE). See the [`LICENSE`](LICENSE) file for the full text.
