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

| Version | Capability |
|---|---|
| 1.0.0 | Fresh enable from templates (Mode A) |
| 2.0.0 | Vendor detection + migration (Mode C); idempotent re-runs (Mode B) |
| 3.0.0 | Evolving memory: fact metadata + ids, decay-policy, review ritual, archive |
| 3.1.0 | AI-infrastructure `.gitignore` propagated into enabled repos |
| 3.2.0 | Protocol clarifications: session = one log-write; metadata ownership; stack-fact altitude; after-session checklist |
| 3.3.0 | Supersession: facts that become *false* are marked `superseded` (replaced/invalidated) and archived flagged "superseded", not "faded" |
| 3.4.0 | Invariant verification: the review periodically prompts a human to re-confirm never-decay facts (`verify_invariants_every`) |
| 3.5.0 | Write-time contradiction check: a new fact is checked against existing ones → supersede or raise a `Contradiction:` Open Thread (review backstop) |
| 3.6.0 | Memory smoke test (`memory/smoke-test.md`): a manual check that a fresh agent can orient from memory alone |
| 3.7.0 | Provenance + retrieval: optional `origin:` footer traces a fact to its source session; retrieval is lexical + indexed by design |
| 4.0.0 | Forward layer (VBDI): `memory/vision.md` + `(blueprint)` gaps + altitude trace — a cognitive loop (Current State → Vision → Blueprint → Design → Implementation → Feedback) over the memory substrate |
| 4.1.0 | Cross-vendor skills layer: neutral committed `agent-skills/<name>/SKILL.md` + an `AGENTS.md` baseline (agent-as-runtime) + regenerated Claude/Gemini/Cursor adapters; migration promotes vendor `.claude/skills/` into `agent-skills/` |
| 4.1.1 | Skills-layer refinements: folder finalized as `agent-skills/` (collision-safe), Cursor adapter `globs` fix (agent-requested type), collision guard, vendor-dir double-duty clarified |
| 4.2.0 | "Sync skill adapters": regenerate the per-vendor adapters from `agent-skills/` on demand (after clone/pull, since adapters are gitignored and don't travel). Adapter recipe + sync steps now live in the installed `AGENTS.md` "Skills" section |
| 4.3.0 | Skill authoring convention (create in `agent-skills/`, never a vendor folder) + **"adopt skill"** safety-net: promote a skill authored natively in a vendor folder back into `agent-skills/`, checked at session close so it's never left unshared |
| 4.3.1 | Skills-layer doc fixes (from a session-close test-drive): "Adopt" no longer says "commit" mid-ritual; adopt-before-log ordering noted; body-normalization clarified |
| 4.3.2 | Skills-layer description hardening (from a lifecycle sanity check): adapter `description` mirrors the neutral skill verbatim; descriptions kept single-line & quote-free so they embed safely in TOML/MDC/YAML |
| 4.3.3 | Skills-layer description guidance: keep `description` concise + trigger-phrase-rich (small discovery budget); YAML `>`/`|` are YAML-only, so the value stays one logical line (it mirrors into TOML too) |
| 4.4.0 | Lightweight skills: per-session `AGENTS.md` keeps only the runtime baseline + a pointer; the recipe + **sync**/**adopt**/**sanity-check** ops move to an on-demand `SKILLS.md`. Per-session "skills safety check" removed (skill work is conscious/on-demand); upgrades do a read-only filename check that *recommends* sync |
| 4.5.0 | Kiro support: a 4th skills adapter target `.kiro/skills/<name>/SKILL.md` (Kiro follows the open Agent Skills standard — same shape as the Claude adapter) + Kiro in the Mode C detection/migration table (steering → instructions, skills → `agent-skills/`, specs → `legacy/`). Kiro auto-reads root `AGENTS.md`, so the memory layer needs no pointer file |
| 4.5.1 | Skills-layer guidance (from a Gemini CLI dogfood): documents that the Gemini adapter is a **slash command** `/<name>` (explicit, not natural-language auto-matched) while Claude/Cursor/Kiro adapters are description-matched — all point to the same neutral skill; and a **never-commit-the-adapters** guard on `sync skill adapters` (only `agent-skills/` is shared) |
| 4.5.2 | Kiro hooks in Mode C (from a Windows/Kiro enable): migration preserves `.kiro/hooks/*.kiro.hook` verbatim under `legacy/` — never converted or run. Human-gated commit hooks (like Kiro's, triggered by the human saying "commit") align with agent-memory; only an *unprompted* auto-commit/push is surfaced as an Open Thread. Plus a README bootstrap edge-case note ("Start from `AGENTS.md`" when an enterprise IDE self-bootstraps) |
| 4.6.0 | Vendor-neutral **commit attribution**: `AGENTS.md` extends "identify yourself" (already true for session logs) to commits — deliberate, human-initiated, with a `Co-Authored-By: <agent>` trailer. Encodes once what Claude Code does automatically and Kiro needed a per-machine hook for — every vendor follows with no per-vendor setup |
| 4.7.0 | **Lightweight mode** for memory-neutral tasks (from a Kiro enablement): a trivial task (no new fact/decision/thread/state change) writes a **one-line "lite" session log** and skips the full template / fact-footers / continuity edits. The ledger stays continuous; the review treats it as a normal reference-free session. Scales the per-session ceremony to the actual memory impact |
| 4.7.1 | Lightweight mode keyed to **file-change, not "trivial"** (a judgment call both AI and human misjudge): **read-only** sessions (no file changes) write **no log**; **any file change** (even one line) writes at least a **lite log**; a memory-relevant event → the full ritual |
| 4.8.0 | Review **self-verify guard**: before archiving, the review greps the last `archive_window` sessions for each fading id (any hit ⇒ the count was wrong, keep it) and confirms no id is in both `continuity.md` and the archive. Catches the decay miscount that's the most common — and costliest — review error |
| 4.9.0 | **`memory-lint`** — a portable, optional verifier skill (`agent-skills/memory-lint/`, Python 3 stdlib) that runs the decay-integrity checks *deterministically* — moving the counting off the LLM entirely. Wire it to a pre-commit hook / CI. `REVIEW.md` points to it; it caught a real over-archival on first run. The tool never runs it (agent/human/CI-invoked) |
| 4.10.0 | **Fresh-context second opinion** — a skill pair (`second-opinion` + `apply-critique`): snapshot the current task for a clean-memory reviewer (any vendor / a fresh session) behind a **security advisory**, then apply the returned critique through a **bounded, validated, human-gated** loop (build/tests + `memory-lint`; critique stays advisory). Snapshots live in gitignored `review-scratch/`. ENABLE and upgrades now **install** the built-in skills (incl. `memory-lint`, which the review ritual relies on). The reviewer is a hypothesis generator, not an authority — the lesson the layer learned in 4.8/4.9 |
| 4.10.1 | **`memory-lint` fix:** line-anchor its Memory-References parser so a session log that *quotes* the heading in prose no longer trips a false `over-archived` error (found while running the verifier during a review). Script-only |
| 4.10.2 | **Fresh-context-review critique fixes:** harden `memory-lint`'s footer parse against an *unclosed* footer (bind to one line); the install protocol now **warns before overwriting a locally-modified built-in** rather than silently clobbering it; the `upgrades-additive` invariant carries its tool-managed-built-ins exception inline; `second-opinion` notes that a *different* vendor adds epistemic diversity a same-vendor session can't. Applied via the `apply-critique` loop |
| 4.10.3 | **Lightweight-mode wording fix:** the session-log test is now keyed to whether a **tracked** file changed (the objective test is the **git diff**), and runs whose only writes are **gitignored, regenerated artifacts** (`sync skill adapters`, `review-scratch/`, the compiled lint artifact) are explicitly **no log** — aligning the note with what `SKILLS.md` already says (sync touches no committed file). Wording-only |
| 4.10.4 | **`memory-lint` nested list fix:** hardened the script's `pinned_open_threads` parsing to track indentation level, preventing standard sub-bullets from dropping a parent Open Thread's pinned state. |
| 4.11.0 | **`memory-lint` Node runtime:** the deterministic verifier now ships in **both** Python and Node (`memory-lint.mjs`, Node ≥ 18, built-ins only) at output parity, so a node-only machine still gets the script instead of an unreliable hand count. `SKILL.md` documents both as interchangeable; a shared test contract (`test_memory_lint.mjs` ↔ `.py`) keeps them equivalent. Additive — no dispatcher, no installer |
| 4.11.1 | **Review step-6 archival guard hardened:** `REVIEW.md` now defines a "use" as a `## Memory References` entry (not a prose mention), making `memory-lint` the preferred archival check and scoping the by-hand fallback to in-block hits — fixing an archival livelock where a review naming a fact while deferring it re-armed the guard forever. Added `memref_ids` regression tests (both runtimes) |
| 4.12.0 | **Enforced adapter sync at enable + upgrade:** ENABLE and every Mode B re-enable now **run** `sync skill adapters` (idempotent, gitignored-only) instead of a read-only "recommend, don't run" check, so a skill's vendor-native adapters are materialized at enable/upgrade — closing the gap where a skill predating a new adapter target (e.g. Kiro), or a fresh clone/pull, was left without working native skills. Step 8 now asserts adapter completeness. The per-session path still never touches skills |
| 4.12.1 | **`memory-lint` dangling-link cross-file fix:** `check_dangling` now resolves `superseded-by`/`supersedes` targets against footers in other `memory/*.md` files (e.g. `vision.md`), not just `continuity.md` + the archive — so a fact superseded by a `vision.md` fact no longer false-flags as `[dangling]`. Fixed at parity in both runtimes with a regression test in both suites. Found dogfooding a real target, ported back |
| 4.13.0 | **Tool-provided (system) skills marked + upstream advisory:** the built-ins agent-memory installs into every repo (`memory-lint`, `second-opinion`, `apply-critique`) now carry `provenance: agent-memory-builtin` in their `SKILL.md` frontmatter (+ a body banner), so a target's AI recognizes a system skill at edit time. `SKILLS.md` tells it to **fork** a local variant or **upstream** a genuine fix to the agent-memory project (file an issue in production; advise the maintainer pre-release) instead of stranding it — closing the gap where a real `memory-lint` fix in a target nearly got lost. The upgrade warn-before-overwrite carries the same advice |
| 4.14.1 | **Re-synced `AGENTS.md` source clarified:** the upgrade ladder now maps each re-synced file to its one canonical source — a target's `AGENTS.md` comes from `templates/AGENTS.md` (the memory hub), **never** the tool's root `AGENTS.md` (the operator/dual-mode dispatcher) — with a self-check and a corrective rung that repairs a mis-synced one. Found dogfooding a v3.7.0→v4.14.0 upgrade on another vendor |
| 4.14.0 | **Optional Architecture Decision Record log:** an **optional**, human-facing `docs/ADR.md` decision log at the VBDI **Design** altitude — one durable architecture decision per entry (Status · Date · Abstract · Rationale-with-consequences), newest-first, `Proposed → Accepted → Superseded/Deprecated`, **never deleted**. Map-don't-duplicate: `continuity.md` keeps the live *what*, the ADR carries the *why* (cross-linked by `formalizes:` ↔ a visible `(ADR-NNNN)` tag in the invariant title — a human pointer, not an agent read-cue). Read **on demand** — not in the per-session read path (zero default token cost). Documented in `.agent/schema.md`; **not auto-installed** (adopt on demand) |
| 4.16.1 | **Session filename drift fix:** two gaps allowed date-only session filenames (`YYYY-MM-DD.md`): the protocol said "or equivalent" (allowing context `currentDate`), and `memory-lint` had no filename check. Fixed: explicit `date -u` requirement in `templates/AGENTS.md` + `schema.md`; new `check_session_filenames` warning (check 5) in both linter runtimes with tests |
| 4.16.0 | **ADR default path aligned to industry convention:** the optional Architecture Decision Record log moves from `docs/ADR.md` to `docs/arch-decisions/ADR.md` — aligning the default with the widely-adopted subdirectory convention (signals purpose, leaves `docs/` root uncluttered). Normative change to `.agent/schema.md`, `AGENTS.md` (root + template), `DECAY.md §12`; this repo dogfoods the new path (`docs/arch-decisions/ADR.md`). Targets already at the new path (e.g. `mercury-composable`) need no file move — only a version bump; targets still at `docs/ADR.md` rename the file. Not auto-installed; the upgrade rung handles the migration |
| 4.15.0 | **ADR log upkeep trigger:** the optional `docs/ADR.md` decision log is now *maintained*, not merely documented — once a repo has one, a new durable architecture decision (or superseding/invalidating an `(ADR-NNNN)`-tagged `continuity.md` fact) **prompts a human-gated ledger update**: add a newer ADR, mark the old `Superseded`/`Deprecated` (never deleted), keep `formalizes:` ↔ `(ADR-NNNN)` in sync. Closes the 4.14.0 gap where the log could be adopted but had no cue to evolve. Documented in `AGENTS.md` + `.agent/schema.md` + `DECAY.md §12`; still not auto-installed |
| 4.17.0 | **GitHub Copilot CLI skills adapter:** a **5th** skills adapter target `.github/skills/<name>/SKILL.md` — Copilot CLI follows the open Agent Skills standard (same `SKILL.md` shape as the Claude/Kiro adapter) and auto-matches by `description` (also accepts an explicit `/<name>`). `sync skill adapters` now writes five adapters; `.github/skills/` is gitignored **path-scoped** (the rest of `.github/` — `copilot-instructions.md`, `workflows/` — stays tracked). Copilot also gains skills in the Mode C detection/migration table (`.github/skills/`, `.agents/skills/` → `agent-skills/`), and the Copilot steering template now **front-loads the `memory/` read list** + a manual-upkeep note (Copilot's Ask/Plan modes don't follow a pointer chain or auto-maintain memory — reliability over DRY, Copilot-scoped). Found dogfooding `~/sandbox/simple-proxy`, where Copilot CLI couldn't discover a skill authored only in `agent-skills/` |
| 4.18.0 | **`sync skill adapters` is now a runnable script:** a new built-in **`sync-adapters`** skill ships a deterministic adapter-regeneration script (Node + Python at parity) that (re)writes the five vendor adapters for every skill and prunes the orphans it generated. Replaces the prose-recipe-only sync that agents (e.g. Copilot CLI / Gemini) struggled to *run* — they hunted for a non-existent npm/MCP command and flailed. Enable + every Mode B re-enable invoke the script; an agent also triggers it by description. Consistent with `no-build-step-agent-run` (same category as the `memory-lint` script). Surfaced dogfooding `~/sandbox/simple-proxy` |
| 4.19.0 | **Vendor-neutral ritual triggers:** the after-session ritual no longer depends on the agent self-triggering (which failed in practice — skipped even with Claude; Copilot-only teams had no triggers). Enable installs a committed **`.githooks/post-commit`** (auto-stubs a session log when a commit does real work without one; re-syncs adapters) — **agent-activated** via `core.hooksPath`, zero manual user step — plus a **CI floor** (`.github/workflows/agent-memory.yml`: `memory-lint` + advisory session-log check on push/PR, zero per-user setup). Advisory by default (opt-in `AGENT_MEMORY_STRICT` gate); `no-build-step-agent-run` holds (git/CI invoke them; the tool runs nothing). Honest limit: git can't auto-run hooks on a bare clone → CI is the backstop. Design: `docs/DESIGN-ritual-triggers.md` |
| 4.20.0 | **First-run init for fresh clones:** a Copilot dogfood showed a fresh clone self-initializes the *memory* bootstrap but not the gitignored adapters or the (unactivated) hook. Adds **`.githooks/init.sh`** (one idempotent command: regenerate adapters + activate the hook) + an **`AGENTS.md` self-init note** so the agent does it on its first session — one step (or one human command) instead of two. CI stays the zero-config floor |
| 4.20.1 | **Self-init in `copilot-instructions.md`:** v4.20.0's self-init reached Claude but not Copilot CLI (its `start` front-loads `copilot-instructions.md` + summarizes). Folds the first-run init into the top of `copilot-instructions.md` so Copilot runs `bash .githooks/init.sh` before summarizing; the `init.sh` fallback + CI floor are unchanged |
| 4.20.2 | **Windows line-ending hardening:** a `.gitattributes` pins `*.sh` + `.githooks/*` to LF so Git for Windows (`core.autocrlf=true`) doesn't rewrite them to CRLF and break bash (`bad interpreter: …^M`). Installed/merged into targets additively. Makes the bootstrap + hooks robust on Windows (Git Bash / WSL), not luck-of-the-default. From a Copilot Windows-feasibility check |
| 4.20.3 | **memory-lint catches an empty/malformed version manifest:** a deterministic `check_version_manifest` ERROR (both runtimes, at parity, with tests) so a present-but-empty/malformed `.agent/version.md` fails the lint floor (CI + reviews) instead of silently breaking Mode B upgrade detection. Closes the loop on the v4.20.1 bug (a truncating stamp one-liner emptied a target's `version.md` → an agent misread the version). A *missing* `version.md` stays valid (pre-versioning baseline) and is not flagged |
| 4.21.0 | **Google Antigravity (`agy`) skills adapter:** a **6th** skills adapter target `.agents/skills/<name>/SKILL.md` — Antigravity (the Gemini CLI successor) merged custom commands into the open Agent Skills standard and reads `.agents/skills/`, **not** the old `.gemini/commands/*.toml`, so `agy` reported `/<command>` as not found despite `init.sh` populating the Gemini adapter. `sync skill adapters` now writes six adapters (same `SKILL.md` shape as the Claude/Kiro/Copilot adapter); `.agents/` is gitignored. The `.gemini/commands` TOML adapter stays for now so Gemini CLI keeps working during the transition. Antigravity added to the Mode C detection/migration + bootstrap tables. Found dogfooding `agy` on an enabled repo |


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

  agent-skills/                      ← this tool's own portable skills (dogfood)
    hello-world/SKILL.md             ← demo skill: neutral source of truth (adapters gitignored)

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
