# AI Enable a Repository

This file tells you (the AI agent) exactly how to AI-enable a target repository
when a user says something like:

> "AI enable this repo `/path/to/target-repo`"
> "AI enable `../my-project`"
> "Set up AI memory for this folder"

Follow every step in order. Do not skip steps. Do not copy templates blindly —
your job is to **analyse first, detect existing AI footprint, then generate or migrate**.

---

## Scope of Changes — Read This First

### What gets touched
Every file operation in this protocol (read, write, move, delete) is restricted
to the **target repository directory only**. You must never read from, modify,
move, or list contents of:

- The user's home directory (`~`, `$HOME`, `%USERPROFILE%`)
- User-global AI config directories (`~/.claude/`, `~/.cursor/`, `~/.aider/`,
  `~/.continue/`, `~/.codeium/`, `~/.gemini/`, `~/.config/<vendor>/`, etc.)
- macOS Application Support (`~/Library/Application Support/`)
- Windows AppData (`%APPDATA%`, `%LOCALAPPDATA%`)
- System-wide paths (`/etc/`, `/usr/`, `C:\ProgramData\`)
- Any path that resolves outside the target repo root (resolve symlinks first)

If a vendor stores its primary data outside the target repo, only what is
*inside* the repo gets migrated. The user's global AI tooling, their other
projects, and their machine-wide config are completely untouched.

If you are ever tempted to read or modify something outside the resolved
target-repo path, stop and tell the user instead.

### Why this boundary exists (design intent)

This is not only a safety guardrail — it is the core philosophy of the tool.

- **The user's `~/` is their personal AI environment.** Whatever vendor a
  user prefers (Cursor, Claude Code, Aider, Continue, etc.) is their own
  workflow choice. They will keep using it after enablement. Their personal
  history, profile, model preferences, and global settings must remain intact.

- **The repo's `memory/` is the team's shared collaboration layer.** It exists
  so that multiple contributors using *different* AI vendors can share a
  common project memory. It is committed to git and travels with the code.

These two layers are designed to coexist. A user can keep using Cursor with
all their personal settings, while their teammate uses Claude Code, while a
third uses Aider — and all of them collaborate through the repo's `memory/`
without disturbing each other's individual tooling.

Migration moves only the repo-local vendor artifacts (steering files committed
to the repo, chat history files written into the repo). Anything in the user's
home directory is theirs and stays theirs.

---

## Step 1 — Locate the Target Repo

Resolve the path the user provided to an absolute path.
Confirm the directory exists. If it does not, stop and tell the user.

List the top-level contents (including hidden files) of the target directory.
Use `ls -la` or equivalent — many AI footprints live in dotfiles and dot-directories.

---

## Step 2 — Detect Existing AI Footprint

Before analysing the codebase, check whether this repo has already been touched
by any AI tooling. **Read `MIGRATE.md` for the full detection table and migration
rules.** Quick checklist:

**Steering files (instructions to AI):**
- `CLAUDE.md`, `GEMINI.md`, `AGENTS.md`
- `.cursorrules`, `.cursor/rules/*.mdc`
- `.clinerules`, `.roorules`
- `.windsurfrules`, `.codeiumrc`
- `.aider.conf.yml`, `CONVENTIONS.md`
- `.continue/config.json`
- `.github/copilot-instructions.md`
- `.rules` (Zed)

**Memory / session / history files:**
- `memory/` (ours — already enabled)
- `.claude/`, `.codex/`
- `.aider.chat.history.md`, `.aider.input.history`
- `.continue/sessions/*.json`
- `.cursor/`, `.windsurf/`, `.cline/`

Build a list of detected footprints. Categorise each as:

- **OURS** — `memory/instructions.md`, `memory/continuity.md`, `memory/sessions/`
  exist AND match the schema in `templates/.agent/schema.md`
- **VENDOR** — any file from the lists above that is *not* in our format
- **AMBIGUOUS** — a file with our name (e.g. `CLAUDE.md`) but different content
  (e.g. someone hand-wrote project rules into it before knowing about our system)

---

## Step 3 — Decide the Mode

Based on detection, choose one of three modes:

### Mode A — Fresh Enable
No AI footprint found.

**Before generating anything, show an advisory and offer a discovery depth.** A fresh
enable is the one moment to set how rich the initial memory is, and the user should know
what is about to happen to their repo. **Lead with a concise exec summary of what the
agent-memory protocol is** — so the user is giving *informed* consent, not a blind "yes."
Honesty and integrity are an architect's first duty: state plainly what it does, what it
writes, what it leaves alone, and that it's committed and shared. Then let them choose:

> **About to AI-enable `<repo>` with the agent-memory protocol — here's what that means:**
>
> **What it is.** A **vendor-neutral, no-code, markdown** layer that gives your repo a
> **shared AI memory** (`memory/`) plus AI **steering** files. Any teammate — on Claude
> Code, Cursor, Gemini, Copilot, Kiro, etc. — reads and writes the *same* project memory, so
> context survives across people, sessions, and tools. It **adds** this layer; it does **not**
> replace or reconfigure your own CLI/IDE.
>
> **What I will write into the repo** (nothing outside it, ever):
> - `memory/` — the shared memory layer (project facts, decisions, an evolving/decaying log).
> - Steering/bootstrap files at the root for each vendor — `AGENTS.md`, `CLAUDE.md`,
>   `GEMINI.md`, `.cursorrules`, `.windsurfrules`, `.github/copilot-instructions.md`.
> - `agent-skills/` (portable capabilities) + protocol docs (`DECAY.md`, `REVIEW.md`, `SKILLS.md`, `MERGE.md`).
> - Add-only edits to `.gitignore`/`.gitattributes` (on GitLab, also an add-only `include:` line in
>   a pre-existing `.gitlab-ci.yml` — never your rules), a committed git hook I activate locally,
>   and an advisory CI job + PR/MR description template matched to your hosting forge.
>
> **What I will NOT touch.** Your **source code**, build manifests, and anything **outside
> this repo** (your home dir, global AI config, other projects) — never read or modified.
>
> **It's committed and shared.** `memory/` and the steering files travel with the repo in
> git, so they're visible to everyone with access (personal/per-machine runtime dirs stay
> gitignored). It's all plain markdown you can read, edit, or delete by hand at any time.
>
> **To seed the memory I'll analyse the repo — pick a depth:**
> - **Standard scan** (default) — read the build manifests and **recursively harvest the
>   repo's markdown knowledge** (docs trees, decision logs, ADRs, kanban, roadmap — Step 4 /
>   4b) and distill the durable facts into memory.
> - **Deep analysis** — an **`/init`-depth pass** over the codebase (entry points,
>   module/architecture map, control & data flow, conventions, build/test/CI) *plus* that
>   same markdown harvest, for a richer initial memory. Reads more of the repo; takes longer.
>
> **Proceed? And standard scan or deep analysis?** (standard / deep / cancel)"

If the user declines (`cancel`), **write nothing** and stop — consent is the gate, not a
formality.

- **Default = standard scan.** If the user doesn't choose, or the enable is
  non-interactive, proceed to Step 4 as normal.
- **Deep analysis** replaces the standard path (it does **not** skip the markdown harvest —
  it *subsumes* it, so the docs are never skipped — and adds the code/architecture pass).
  Seed Step 5 from the richer findings. **Critical — keep the output neutral:** a vendor's
  built-in `/init` writes a *vendor* steering file (e.g. `CLAUDE.md`); here you use that
  *capability* but write everything you learn into the **neutral memory layer**
  (`memory/instructions.md` + `memory/continuity.md`), **never** into a vendor file. You are
  borrowing the analysis depth, not its default destination.
- **Record the choice in the first session log** (Step 5c) — `standard` or `deep` — so the
  depth of the initial analysis is traceable and a later session/review knows what was (and
  wasn't) examined.

Then proceed to Step 4 (generate from scratch).

### Mode B — Already Ours (Idempotent, version-aware)
`memory/` exists and matches our schema. Now check the version:

- `installed` = the target's `.agent/version.md` → `version` (a **missing** file
  means it was enabled before versioning existed → treat as `2.x baseline`).
- `current` = this tool's root `VERSION`.

Then:
- **Up to date** (`installed == current`): tell the user and stop —
  > "This repo is already AI-enabled with agent-memory v<current>.
  > Found N sessions logged. Nothing to migrate or upgrade. Last session: <date> by <agent>."
- **Older** (`installed < current`): an in-place upgrade is available.
  **Read `UPGRADE.md` and run its ladder** from `installed` up to `current`, then
  re-stamp `.agent/version.md` and report what changed. Ask first:
  > "This repo is on agent-memory v<installed>; current is v<current>.
  > I can upgrade it in place (additive, non-destructive). Proceed? (yes/no/dry-run)"
- **Newer** (`installed > current`): the repo is ahead of this tool checkout —
  stop and tell the user to update the tool.

If they instead want to re-run a fresh enable, treat as Mode A but skip any file
that already exists unless they say "overwrite".

### Mode C — Migrate from Vendor
Vendor footprint detected. **Read `MIGRATE.md` and follow its protocol.**
After migration completes, return to this file at Step 4 to fill any gaps.

Ask the user before starting migration:
> "Detected existing AI setup: <list of footprints>.
> I can migrate these into the unified agent-memory format.
> Originals will be preserved under `legacy/`. Proceed? (yes/no/dry-run)"

If `dry-run`, print what would happen without writing anything.
If `no`, ask whether to proceed with fresh enable instead, or abort.

---

## Step 4 — Analyse the Target Repo

(Skip this step if Mode C populated everything already — go to Step 5. **Exception: the
Hosting-forge determination below always runs** — Mode C never populates it. Otherwise, proceed.)

Read the following files if they exist:

**Identity & purpose**
- `README.md` or `README.rst` or `README.txt`
- `package.json` → name, description, scripts, dependencies
- `pyproject.toml` or `setup.py` or `setup.cfg`
- `Cargo.toml`
- `go.mod`
- `composer.json`
- `*.gemspec`
- `pubspec.yaml`

**Structure signals** (these classify the repo; the *knowledge harvest* below is what
reads the team's own docs — don't stop at top-level names)
- Folder names (src/, app/, lib/, api/, frontend/, backend/, etc.) — and **descend**:
  a `docs/` (or `doc/`, `documentation/`, `wiki/`) tree is a structure signal *and* a
  knowledge source; recurse it in the harvest below, don't just note that it exists.
- Presence of `Dockerfile`, `docker-compose.yml`, and CI config — `.github/workflows/`
  (GitHub Actions), **`.gitlab-ci.yml` (GitLab CI)**, or **`azure-pipelines.yml` /
  `.azuredevops/` (Azure Pipelines, v4.32.0)** — note which (v4.31.0)
- **Hosting forge (v4.31.0; +Azure DevOps v4.32.0):** read `git remote get-url origin` —
  `github.com` → GitHub; `gitlab.com` or a self-managed GitLab host → GitLab (corroborate with
  `.gitlab-ci.yml` / `.gitlab/` presence); `dev.azure.com` or `*.visualstudio.com` → Azure DevOps
  (corroborate with `azure-pipelines.yml` / `.azuredevops/`). No remote or ambiguous →
  **unknown** (Step 6 then installs the GitHub + GitLab sets — each forge ignores the other's
  files, so that is additive-safe; the Azure DevOps set installs only on positive detection,
  since its pipeline needs a one-time activation and blind installs would just add noise)
- Presence of `Makefile`, `justfile`, `Taskfile.yml`
- Presence of test directories (`tests/`, `spec/`, `__tests__/`, `test/`)

From this analysis, determine:

1. **Project name** — from package file or folder name
2. **Primary language(s)** — from file extensions and package files
3. **Framework / stack** — from dependencies
4. **Project type** — web app / API / CLI / library / **monorepo** / data / other.
   Monorepo detection signals:
   - JS/TS: `pnpm-workspace.yaml`, `lerna.json`, `nx.json`, `turbo.json`, `rush.json`,
     multiple `package.json` files in subdirectories
   - Go: `go.work`
   - Rust: root `Cargo.toml` containing `[workspace]`
   - Java/Kotlin: root `pom.xml` with `<modules>` section, or root `settings.gradle`
     with `include(...)` statements
   - Python: multiple `pyproject.toml` or `setup.py` files under subdirectories
5. **Test setup** — yes/no, framework name if detectable
6. **CI/CD** — yes/no, platform if detectable
7. **Version (source of truth)** — read from the canonical build manifest only
   (`pom.xml` → `<version>`, `package.json` → `"version"`, `Cargo.toml` →
   `version =`, `pyproject.toml` → `version =`, `*.gemspec` → `spec.version`).
   If README, docs, comments, or other files reference a *different* version
   string, **do not fix the drift** — log it as an Open Thread in
   `memory/continuity.md`:
   `- [ ] Version drift: build manifest is X.Y.Z but <file(s)> reference a different version — verify and align`
   Resolving drift is the user's responsibility, not the enablement step.
8. **Hosting forge** — GitHub | GitLab | Azure DevOps | unknown (from the Structure-signals
   check above; drives the Step 6 forge-matched install — determined even on a Mode C run)

**Monorepo handling:** If project type is monorepo, additionally enumerate each
top-level module or package: its path, language (if the repo is mixed), and a
one-line description of its purpose. You will use this to fill the
`## Module Inventory` section of `memory/instructions.md` in Step 5.

Default strategy: **one root `memory/` for the whole repo.** A shared memory
layer is more useful than per-module silos in most monorepos, because conventions,
cross-cutting decisions, and team context are repo-wide. Only recommend adding
per-module `memory/` directories if modules are independently deployed and
maintained by separate teams who never collaborate across module boundaries —
and note that recommendation as an Open Thread rather than implementing it.

### Step 4b — Harvest existing project knowledge (be curious)

The steps above *classify* the repo. This step asks the more important question:
**what does this team already know that the memory layer should inherit?** A repo's
canonical knowledge usually already lives in human-authored markdown — and the most
common enablement complaint is that the first pass was *not curious enough*: it read
the manifest files and stopped, skipping a `docs/` tree, a decision log, or a kanban
board sitting in plain sight. **Do not stop at the fixed list above. Go look.**

**1. Enumerate, recursively.** Find candidate knowledge artifacts across the *whole*
repo tree (not depth-1). These are **human-authored prose**, not source or generated
output. Cast a wide net by location and by name:

- **Recurse every documentation tree fully** — `docs/`, `doc/`, `documentation/`,
  `wiki/`, `rfcs/`, `adr/`, `design/`, `notes/`, **including all subfolders**. The
  reported failure mode is grabbing a folder's top-level files and never descending —
  descend.
- **Sweep the repo root and module roots** for stray knowledge markdown the manifest
  scan ignores: decision logs / `DECISIONS*`, `ADR*` / architecture-decision records,
  `ROADMAP*`, `TODO*`, `BACKLOG*`, kanban boards (`KANBAN*`, `BOARD*`), `CHANGELOG*`,
  `ARCHITECTURE*`, `DESIGN*`, `CONTRIBUTING*`, `RFC*`, `SECURITY*`, `GLOSSARY*`,
  onboarding / runbook / postmortem notes.
- **Match by extension** `.md`, `.markdown`, `.mdx`, `.rst`, `.txt`, `.adoc` — but treat
  prose, not data. (Use a recursive listing, e.g. `find`/`rg --files`, then filter.)

**Exclude** (knowledge harvest only — these are not team prose): `node_modules/`,
`vendor/`, `.venv`/`venv/`, `target/`, `dist/`, `build/`, `.git/`, generated API
reference, minified or vendored files, and anything already ignored by `.gitignore`.

**2. Read within a budget, and disclose what you skipped.** On a large repo the doc
tree can be huge, so don't blindly read everything:

- Read up to a sensible budget (e.g. ~40 files / ~400 KB of prose). **Prioritize**:
  repo-root knowledge files → `docs/` (breadth first, then depth) → most-recently-modified
  (recent docs reflect current reality) → everything else.
- If the budget is hit, **never let the remainder vanish silently.** Record an Open
  Thread in `memory/continuity.md` listing what was found-but-not-yet-ingested, e.g.:
  `- [ ] (knowledge-harvest) N knowledge docs found beyond the enable-time read budget (<paths/globs>) — skim and fold the durable facts into memory when convenient.`
- A re-run / upgrade can resume from that thread (see `UPGRADE.md`).

**3. Distill — do not transcribe.** These docs are *source material*, not memory.
Extract the durable, project-defining facts and feed them into the Step 5 seeding:

- Conventions, architecture decisions, hard constraints → `memory/instructions.md`
  (and seed **Architectural Invariants** in `continuity.md` from explicit
  "must / never" rules; record an `(ADR-…)` cross-link only if an ADR log exists).
- Current goals, roadmap, in-flight work, kanban "in progress" / decision-log open
  items → **Open Threads** in `continuity.md`, and the aspiration → the
  **Current-state context** of `memory/vision.md` (5g) — still never *fabricate* the
  target.
- Newcomer-facing knowledge → candidate **smoke-test questions** (5f).

Do not copy doc bodies into memory or duplicate a living doc; **map, don't mirror** —
link to the canonical doc and capture only the enduring fact (`DECAY.md` map-don't-duplicate).
If a harvested fact contradicts a manifest or another doc, raise a `- [ ] Contradiction:`
Open Thread rather than silently picking one.

---

## Step 5 — Generate or Complete Memory Files

If Mode A (fresh): generate all memory files from templates, replacing every
`{{placeholder}}` with real content derived from your analysis.

If Mode C (post-migration): the migration process will have created partial
files. Fill in any sections still containing placeholders, using your repo
analysis. Do NOT overwrite content that migration already placed.

### 5a. `memory/instructions.md`

Fill in:
- What this project actually is (from README / package description **and the Step 4b
  knowledge harvest** — fold in conventions, architecture decisions, and hard
  constraints distilled from the team's own docs)
- The tech stack at an **enduring, high-level** altitude (e.g. "async Rust CLI") —
  *not* a precise dependency list. The volatile specifics (current language version,
  deps, tool versions) belong in `continuity.md` → `## Stack & Tools`; don't
  duplicate them here. Point to continuity instead.
- Project-specific rules (incorporate any rules migrated from vendor steering files)
- Conventions you observed

### 5b. `memory/continuity.md`

Fill in:
- Real project name and detected status
- **`## Stack & Tools`** — the canonical live home for the current language version,
  dependencies, and tool versions (the precise facts `instructions.md` defers here)
- Today's date as `last_enabled`
- `last_session`:
  - If migrated from vendor history, use the most recent session date from those logs
  - Otherwise point it at the **first enable session log** (Step 5c) — the enable *is* the
    first session: `<today> | agent: <your agent name> (<the 5c log's filename stem>)`, e.g.
    `2026-08-06 | agent: Claude Code (2026-08-06-142530)`. Fill it when you write that log —
    the same moment its stem becomes the seeded facts' `origin`. Never leave `(none yet)`:
    it is false the instant the enable completes, and it defeats the multi-agent continuity
    check that reads this field (`AGENTS.md` → Multi-Agent Continuity).
- `last_review`: `(none yet)`
- **repo:** write the path `~`-relative (e.g. `~/projects/foo`) — never an absolute
  `/Users/<name>/…` (or `/home/<name>/…`) path. `memory/` is committed to git and
  shared across the team, so absolute home paths would leak the enabling user's
  username to everyone.
- **Architectural Invariants:** seed from hard constraints in the build manifest /
  README / `instructions.md` (things that must never change — e.g. "POST-only API",
  "no runtime deps"). If none are obvious, remove the section. Facts here never decay.
- Open Threads: include any TODOs surfaced during analysis or migration
- **Greenfield only:** seed a `- [ ] Greenfield — no code yet` Open Thread listing what to
  record as the first code lands: the stack in `## Stack & Tools`, coding conventions,
  Architectural Invariants, **and the stack's build-output `.gitignore` entries** (apply the
  Step 7 stack-aware seed table then — at enable there is no stack to seed)
- **Metadata footers:** give every fact you write a kebab `id` and the footer
  `<!-- id: … | created: <today> | last_used: <today> | uses: 1 | tier: working -->`.
  Ordinary facts are born `tier: working`; **Architectural Invariants get `tier: core`**;
  unchecked Open Threads get an id but never decay. `uses: 1` / `last_used: today` is
  the honest seed (the enable counts as the first reference) — the review owns those
  fields thereafter; don't hand-edit them. See `.agent/schema.md` and `DECAY.md` §1.
  (Set the optional `origin` field to the **first enable session log** (Step 5c) — the
  enable now writes one. If you skip that log, omit `origin`; a later review can backfill it.)

### 5c. `memory/sessions/`

If Mode C, sessions will already be populated from migrated history.
Otherwise create the directory.

**Write a first enable session log** (all fresh enables — Mode A). The enable *is* the
first piece of work, so record it like any session: create
`memory/sessions/YYYY-MM-DD-HHMMSS.md` (persist-time UTC stamp, `date -u +%Y-%m-%d-%H%M%S`)
with the standard title line and a short summary that captures:

- that the repo was AI-enabled with agent-memory v<version> (Mode A), and
- **the discovery depth the user chose** (`standard scan` or `deep analysis`) — and, if
  `deep`, a one-line note of what the deep pass covered (so a later session knows what was
  examined). This is the decision the Step 3 advisory asked the user to make.
- a `## Memory References` section listing the fact ids you seeded at enable.

Apply the **redaction rule** (`AGENTS.md` → After Every Session): never write secrets or PII
into the log — redact any pasted command output to `(REDACTED)` before persisting.

This makes the enable traceable, lets the facts you seed in 5b set a real `origin`, and
supplies the value 5b's `last_session` points at (the enable *is* the first session — never
leave `(none yet)`). (A `.gitkeep` is then unnecessary — the directory is non-empty; only add
one if for some reason no first log is written.)

### 5d. `.agent/schema.md`

Copy `templates/.agent/schema.md` verbatim. No customisation.

### 5e. Evolving-memory layer

Install the layer so the repo's memory can decay, review, and archive over time:

- `memory/decay-policy.md` — copy from `templates/memory/decay-policy.md`, filling
  `{{PROJECT_NAME}}`. The default windows (3/8/20, review every 10) suit most repos.
- `memory/archive/INDEX.md` — create with a header and an empty table.
- `.agent/version.md` — copy from `templates/.agent/version.md`. Fill
  `{{AGENT_MEMORY_VERSION}}` from this tool's root `VERSION`, `{{TODAY}}`, and
  `{{ENABLE_MODE}}` (`A` for fresh, `C` for migrate).

`DECAY.md`, `REVIEW.md`, and `SKILLS.md` are installed at the repo root in Step 6.

### 5f. `memory/smoke-test.md`

Copy from `templates/memory/smoke-test.md`, filling `{{PROJECT_NAME}}` and `{{TODAY}}`.
Seed `{{PROJECT_SMOKE_QUESTIONS}}` with **2–4 project-specific questions** drawn from your
Step 4 analysis **and the Step 4b knowledge harvest** — things a newcomer should be able to
learn from memory alone (e.g. "How does `<entry point>` discover/route X?", "What gates Y?",
or a key decision/constraint surfaced from the docs). They join the generic
orientation questions already in the template. It's a manual memory-quality check — see
the file's header for how it's run.

### 5g. `memory/vision.md` (the forward layer — VBDI)

Install the Vision artifact so the repo's memory becomes *goal-aware* (see `DECAY.md` §12
and `docs/DESIGN-vbdi-lifecycle.md`). Copy from `templates/memory/vision.md`, filling
`{{PROJECT_NAME}}`, `{{PROJECT_SLUG}}` (kebab project name, for the `id`), `{{TODAY}}`,
`{{PROJECT_DESCRIPTION}}`, and `{{PROJECT_TYPE}}`.

**Bootstrap rule — never fabricate the Vision.** A Vision is the *target* state, and the
target is the human's to set (same principle as User Preferences: never infer). So:

- Pre-fill **only** the safe *Current-state context* (`{{PROJECT_DESCRIPTION}}`,
  `{{PROJECT_TYPE}}` from your Step 4 analysis **and the Step 4b harvest** — what the
  project *is* today; a roadmap/decision-log may describe direction, but the *target* is
  still the human's to confirm, never inferred).
- Leave the **target, success criteria, and non-goals as prompts** (the template's `(…)`
  placeholders) — do not infer the aspiration. Keep the ⚠️ DRAFT banner.
- Raise a human-gate Open Thread in `memory/continuity.md`:
  `- [ ] (vision-bootstrap) Confirm the Vision in memory/vision.md — set the target / success criteria / non-goals; then derive the Blueprint.`
- **Do not derive the Blueprint yet** — Blueprint gaps depend on a confirmed target. The
  gate thread carries that forward. Until the Vision is confirmed, VBDI drift-detection is
  advisory.

(Greenfield — an empty repo with no code — inverts this: ask the human for the Vision
*first*, since there's no current state to read.)

### 5h. Skills layer (capabilities — cross-vendor)

Skills are the project's portable **capabilities** — a third shared layer beside memory
and steering: committed, vendor-neutral `agent-skills/<name>/SKILL.md` files (a `name`, a
`description` that says *when* to use it, a procedure, optional helper scripts). The
`AGENTS.md` "Skills" section is the universal runtime (the agent reads the skill — works
on any vendor). See `docs/DESIGN-skills-layer.md` and `.agent/schema.md`.

- **Fresh enable (Mode A):** a repo with no AI footprint has no *vendor* skills to promote —
  **skip the promotion/adapter work in this step** (don't create an *empty* `agent-skills/`
  here). Mode A still **receives the built-in skills** via **5i**, which populates
  `agent-skills/` — so a fresh enable does end up with a (non-empty) `agent-skills/`.
- **Migration (Mode C):** if `MIGRATE.md` promoted vendor skill bundles into `agent-skills/`
  (e.g. from `.claude/skills/`), **(re)generate the per-vendor adapters** below. The
  neutral `agent-skills/<name>/SKILL.md` is the source of truth; adapters are thin pointers,
  regenerated (never hand-edited), living in the gitignored vendor dirs (Step 7), so they
  stay per-machine while only `agent-skills/` is committed.

**Adapter generation** is the canonical **`sync skill adapters`** operation in **`SKILLS.md`** — a
**runnable script** (v4.18.0; the `sync-adapters` built-in, installed in 5i): for each
`agent-skills/<name>/SKILL.md` it writes the Claude / Gemini / Cursor / Kiro / Copilot / Antigravity
pointers and prunes orphans — idempotent, gitignored-only. **Run the script as the closing skills step of every
enable** (`bash agent-skills/sync-adapters/scripts/sync-adapters.sh`, or the `.mjs`/`.py`; and, per
`UPGRADE.md`, on every Mode B re-enable), so the adapters are *materialized*, not merely recommended —
a skill is then usable via its vendor's native auto-trigger immediately. Adapters don't travel with a clone/pull (they're gitignored), so a
contributor on another machine gets them from their own next enable/upgrade, or by running **"sync
skill adapters"** by hand. `SKILLS.md` is read on demand — it's not in the per-session path.

**Collision guard.** `agent-skills/` is namespaced to make a clash with a pre-existing
project dir unlikely, but if a top-level `agent-skills/` already exists with unrelated
content, **do not overwrite it** — surface it as a `- [ ] Contradiction:` Open Thread
(`never-pick-a-winner`) and stop, rather than merging blindly.

### 5i. Built-in skills (installed — all modes)

agent-memory ships portable, vendor-neutral skills of its own that **every enabled repo
gets**, because they support the core workflow:

- **`memory-lint`** — deterministic integrity check for the memory layer (Python 3 stdlib, no
  install — **Python 3 is its one soft prerequisite**; absent it, the agent simply doesn't invoke
  it); the periodic **review ritual** relies on it to verify decay arithmetic. Wire it to a
  pre-commit hook / CI.
- **`second-opinion`** + **`apply-critique`** — the fresh-context review pair: snapshot the
  current task for a clean-memory reviewer (any vendor / a fresh session), then apply the
  returned critique through a bounded, validated, human-gated loop. See
  `docs/DESIGN-fresh-context-review.md`.
- **`sync-adapters`** (v4.18.0) — the runnable **`sync skill adapters`** operation (bash + Node + Python
  at parity; **bash needs no runtime install**): (re)writes the six vendor adapters for every skill and
  prunes the orphans it generated (signature-guarded). Enable and every Mode B re-enable invoke it; an agent can also trigger it by
  description. Replaces the prior prose-recipe-only sync that agents (e.g. Copilot CLI) struggled to
  perform — they hunted for a non-existent command.
- **`harvest-knowledge`** (v4.23.0) — the on-demand, recurring counterpart to the enable-time knowledge
  harvest (Step 4b): re-scan the repo's human-authored docs (docs trees, ADRs, decision logs, design
  specs, roadmaps) and fold newly-durable facts into `memory/` **additively** (map-don't-mirror;
  conflicts → a `Contradiction` thread; never overwrites curated facts). No-code/agent-run. Keeps memory
  in sync as a living repo's docs evolve — and is the home for "re-harvest," so the enable-time harvest
  stays a fresh-enable event, not an upgrade behavior.
- **`archive-fact`** (v4.25.0) — the deterministic executor for the **review ritual's archive-move**
  (`REVIEW.md` step 4): given fact id(s) the agent has *decided* to retire, it moves each block from
  `continuity.md` to the quarter archive + `INDEX.md` safely (reads into memory, writes once — the
  truncate-before-read trap is structurally impossible). Python *or* Node at parity, with mirror tests;
  refuses if an id is missing or already archived. The agent judges *what*; the helper does the *move*.
- **`refresh-metadata`** (v4.26.0) — the deterministic executor for **review steps 2–3** (apply events +
  re-tier): recomputes every fact's `last_used` / `uses` / `tier` from the session reference log and writes
  the footers back (the "full rebuild" path, made runnable). Pure arithmetic — `core`/`superseded` untouched,
  never archives. Closes the gap where agents archive but skip the metadata pass (`memory-lint` flags it as
  `[stale-metadata]`). Python *or* Node at parity, with mirror tests.

**Install all seven** (every mode, including a fresh Mode A enable): copy `agent-skills/<name>/`
**verbatim from this tool's root** into the target's `agent-skills/` (including `memory-lint`'s and
`sync-adapters`' bundled `scripts/`), then regenerate their adapters via the 5h recipe (which now
*runs* the freshly-installed `sync-adapters` script). Each ships marked
**`provenance: agent-memory-builtin`** in its frontmatter (with a banner in its body), so a target's
agent — any vendor — can recognize it as a tool-provided *system* skill and route any change correctly
(see `SKILLS.md` → "Tool-provided (system) skills"). Add **`review-scratch/`**
to the target `.gitignore` (Step 7) for the review pair's personal, per-machine
snapshots/critiques (never committed); `second-opinion` writes a README there on first run.
Idempotent on re-enable — overwrite these built-ins (they are ours); never touch unrelated
`agent-skills/` content (`never-pick-a-winner`). This is the one case where a fresh Mode A
enable **does** create `agent-skills/` — populated with these built-ins, never empty.

> **The built-ins are tool-managed copies.** Re-enable/upgrade **overwrites** them, so do **not**
> customize an installed built-in — if you need a variant, fork it under a **new skill name**
> (your own `agent-skills/<your-name>/`, which is never overwritten). **If the change is a genuine fix
> rather than a customization, upstream it to the agent-memory project** (file an issue in its repo in
> production; bring it to the maintainer pre-release) so it is back-ported + validated and survives
> upgrades. The overwrite is scoped to these three tool-owned skills, so `upgrades-additive` still holds
> for everything else in `agent-skills/`.
>
> **Warn before you clobber.** Before overwriting an *already-installed* built-in, check whether the
> target's copy was locally modified — diff it against the source you're about to write (or, if it's
> committed there, `git diff`/`git status` on `agent-skills/<name>/`). If it differs by more than this
> version's update (a sign someone customized it despite the rule above), **stop and warn the human,
> show what differs, and let them choose** to keep their version or take the update — never silently
> discard a local change. Because such a change is often a *genuine fix* (the simple-proxy case), the
> warning also **advises upstreaming it to the agent-memory project** (an issue in its repo in
> production; the maintainer pre-release) for back-port + validation — see `SKILLS.md` → "Tool-provided
> (system) skills". This keeps the tool-managed-copies contract *checked*, not convention-only,
> and is itself agent-run at the human's direction (`no-build-step-agent-run`). On a fresh Mode A
> enable there is nothing to overwrite, so the check is a no-op.

---

## Step 6 — Install Bootstrap Files

Copy from `templates/` into target repo root:

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `.cursorrules`
- `.windsurfrules`
- `.github/copilot-instructions.md` — read by **local** Copilot tooling from the working tree,
  so install it on **every** forge (it is not a forge artifact; GitLab-hosted repos keep it).
- A **What / Why description template** (v4.27.0) — **forge-aware (v4.31.0)**, per the Step 4
  forge detection:
  - GitHub-hosted: `templates/.github/pull_request_template.md` → `.github/pull_request_template.md`
  - GitLab-hosted: `templates/.gitlab/merge_request_templates/Default.md` →
    `.gitlab/merge_request_templates/Default.md` (auto-applies to new MRs on all tiers; a
    Premium settings-based default template overrides it — mention in the report if the team
    uses one)
  - Azure-DevOps-hosted: `templates/.azuredevops/pull_request_template.md` →
    `.azuredevops/pull_request_template.md` (auto-applies to new PRs; read from the **default**
    branch; keep content lean — Azure Repos caps PR descriptions at 4000 characters)
  - Forge unknown → install the GitHub + GitLab templates.
  Installs verbatim, **tracked** (it travels). If the target already has one, ask per-file
  (overwrite / skip / rename) like any other bootstrap file.

`CLAUDE.md` and `GEMINI.md` contain `{{PROJECT_NAME}}` and `{{PROJECT_ONELINE}}`
placeholders — fill them from your Step 4 analysis (project name + a one-line
description) so eagerly-loaded runtimes get context without an extra hop. They also
contain a `{{BOOTSTRAP_IMPORTS}}` placeholder — expand it to that vendor's **native
import block** (the v4.29.0 before-session presence feature; it is held as a
placeholder in `templates/` so the tool repo itself carries no live imports under
`templates/` — with live imports there, runtimes that auto-load directory-scoped
instruction files pulled the placeholder template stubs into context, v4.29.1):

For `CLAUDE.md` (Claude Code `@path` idiom):

```text
@AGENTS.md
@memory/instructions.md
@memory/continuity.md
@memory/vision.md
```

For `GEMINI.md` (Gemini CLI `@./path.md` idiom — it imports `.md` files only):

```text
@./AGENTS.md
@./memory/instructions.md
@./memory/continuity.md
@./memory/vision.md
```

The remaining bootstrap files install verbatim.

Also install the evolving-memory protocol docs at the target root, **copied
verbatim from this tool's root** (they are generic — no placeholders):

- `DECAY.md`
- `REVIEW.md`
- `SKILLS.md`
- `MERGE.md`

These must travel into the target because the review ritual, skill sync/adopt, and
**conflict resolution** (`MERGE.md`) all run *inside* the enabled repo. (`UPGRADE.md` is
tool-operator-only — do **not** install it.)

**Ritual triggers (v4.19.0; forge-aware v4.31.0) — install + activate (no manual user step).** Also
install these — the GitHub set copies verbatim from this tool's root, the GitLab and Azure
DevOps sets from `templates/` — so the after-session ritual fires reliably for *any* vendor (see `docs/DESIGN-ritual-triggers.md`):

- **`.githooks/`** — the committed, vendor-neutral git hooks (`post-commit` + its `README.md`): auto-stub
  a session log when a commit does real work without one; re-sync adapters when a skill changed.
- The **CI floor** — runs `memory-lint` + an advisory session-log check on every push and
  pull/merge request (on Azure DevOps: pushes only, until an admin adds the optional Build
  Validation policy). **Forge-aware (v4.31.0; +Azure DevOps v4.32.0):**
  - **GitHub-hosted:** copy **`.github/workflows/agent-memory.yml`** verbatim from this tool's root.
  - **GitLab-hosted:** copy `templates/.gitlab/agent-memory-ci.yml` → `.gitlab/agent-memory-ci.yml`,
    then wire the root config:
    - target has **no `.gitlab-ci.yml`** → copy `templates/.gitlab-ci.yml` verbatim (it carries the
      include line **and** the canonical `workflow:rules` duplicate-pipeline guard, which GitLab
      requires in the *root* file for merge-request pipelines to fire).
    - target **already has `.gitlab-ci.yml`** → **add-only**: append the include entry
      (`include:` → `- local: '.gitlab/agent-memory-ci.yml'`, or add that entry to an existing
      `include:` list) — **skip if an include entry for that path is already present anywhere in
      the file** (de-duplicate, like Step 7's `.gitignore` edit). **Stage check (mandatory):** the
      job runs in the default `test` stage — if the file defines a custom `stages:` list without
      `test`, **append `test` to that list** (add-only; an extra stage name changes nothing about
      when existing jobs run, while omitting it makes the whole pipeline config invalid and stops
      ALL the repo's CI). **Never add or edit `workflow:rules` in a pre-existing file** — that
      changes when the repo's *own* jobs run. Coverage: the job rides whatever pipelines the
      existing root config creates (branch pipelines where they fire; MR pipelines if the root
      already carries MR-matching rules; a restrictive root workflow restricts the floor too) —
      read the file and state the actual coverage in the report.
  - **Azure-DevOps-hosted:** copy `templates/.azuredevops/agent-memory-ci.yml` →
    `.azuredevops/agent-memory-ci.yml` — the **own-pipeline model**: a complete, self-contained
    pipeline, so an existing `azure-pipelines.yml` is **never touched** (one repo can carry many
    pipelines, each bound to its own YAML). **Activation is not file-driven on this forge:** the
    committed file is inert until a pipeline resource is bound to it — put the one-time command in
    the Step 9 report and run it **only at the user's explicit direction** (their credentials;
    default permission is Contributors), **after the enable commit is pushed** (`az pipelines
    create --yml-path` binds to the YAML as it exists on the remote — run early, it falls into the
    CLI's interactive flow):
    `az pipelines create --name agent-memory --repository <repo> --repository-type tfsgit --branch <default> --yml-path .azuredevops/agent-memory-ci.yml --skip-first-run`
    **Seed the pending state into memory** so it can't be silently forgotten: add a
    `- [ ] (forge) Azure DevOps CI floor awaiting one-time activation: <the command>` Open Thread
    to the target's `continuity.md` (checked off once the first `agent-memory` run appears).
    Once bound, the file's trigger runs it on every push. PR-time validation on Azure Repos is a
    **Build Validation branch policy** (admin settings; its "Optional" mode is notify-only) —
    document it, never configure it. Honest limit: Microsoft-hosted agents need parallelism — the
    free grant (Microsoft's request form) or paid parallel jobs via a linked Azure subscription —
    or a self-hosted agent.
  - **Forge unknown** → install the GitHub + GitLab sets (each forge ignores the other's files).

**Ensure `.githooks/post-commit` is executable** (`chmod +x`; it must be committed with mode `100755`) —
git **silently ignores** a non-executable hook. Then **the agent activates the local hook**: run
`git config core.hooksPath .githooks` in the target — **do this yourself; never ask the user** (the
adoption constraint: any manual step is a barrier). CI needs
no activation on GitHub or GitLab.com (a committed config runs server-side, zero per-user config);
a **self-managed GitLab** needs an admin-registered runner or the job queues unrun, and an
**Azure DevOps** pipeline is inert until its one-time `az pipelines create` binding — say so in the
report (v4.31.0/v4.32.0). *Honest limit:* git can't
auto-run committed hooks on a fresh clone (security), so where no agent has run, **CI is the backstop**.
Both `.githooks/` and the CI config (`.github/workflows/` on GitHub; `.gitlab-ci.yml` +
`.gitlab/agent-memory-ci.yml` on GitLab; `.azuredevops/agent-memory-ci.yml` on Azure DevOps) are
**tracked** (they travel); only `.github/skills/` is
gitignored. The hooks/CI are **advisory** (never block); the tool runs nothing itself
(`no-build-step-agent-run` — git/CI invoke them in the user's env).

**Conflict handling:**
- If Mode C ran and a vendor bootstrap file was migrated, the migration step
  already moved it to `legacy/` — proceed to install our version.
- If the file exists but is identical to our template, skip silently.
- Otherwise ask the user per-file: overwrite / skip / rename existing to `.bak`.

Create `.github/` in the target if it does not exist — Copilot's bootstrap lives there on every
forge (it is read by local tooling, not by the forge). On a GitLab-hosted target, also create
`.gitlab/` (the CI job + MR template live there); on an Azure-DevOps-hosted target, `.azuredevops/`
(the pipeline + PR template live there).

---

## Step 7 — Install / Update Target .gitignore

Personal AI-IDE runtime directories (`.claude/`, `.kiro/`, `.cursor/`, …) are
per-machine state that should never be committed to the shared repo — but the
agent-memory *steering* files and the `memory/` layer **must** stay tracked. The
canonical managed block that encodes this lives in `templates/.gitignore`; its first
line is a sentinel:

```
# === agent-memory: AI infrastructure (personal / per-machine — do not commit) ===
```

Apply it idempotently. In every case, **de-duplicate**: an entry that already appears
anywhere in the file (e.g. an older enable or the user already ignores `.kiro/`) is
never added a second time, even under a different heading.

- **No `.gitignore` in the target** → create one by copying `templates/.gitignore`
  verbatim.
- **`.gitignore` exists** → make sure the managed block is present and complete:
  - if the sentinel line is absent, append a blank line, the sentinel header, and the
    comment — then only the entries not already present elsewhere in the file;
  - if the sentinel is present, add under it only the template entries still missing.
  - if every template entry is already present (sentinel or not), make no change.

Never remove, rewrite, or reorder the user's existing `.gitignore` entries — only
add. Adding a path to `.gitignore` does not untrack files already committed, so this
is safe even if a vendor dir was previously committed (e.g. before a Mode C migration
moved it to `legacy/`).

### Stack-aware build-output seed (v4.30.0)

The managed block above is deliberately scoped to **AI infrastructure** — it never covers
language build output. But an enabled repo whose `.gitignore` misses its stack's build
directory has its first build pollute `git status` (field case: a greenfield enable later
gained a Rust toolchain, and `target/` had to be hand-added). So, after the managed block:

- **If Step 4 detected a primary language/stack**, check whether its canonical build-output
  paths (table below) are already ignored **anywhere** in the file. Append only the missing
  ones under a second, separately-scoped sentinel:

  ```
  # === agent-memory: build output (stack-aware seed — extend as your stack grows) ===
  ```

  | Stack | Seed entries |
  |---|---|
  | Rust | `target/` |
  | Node / JS / TS | `node_modules/`, `dist/` |
  | Python | `.venv/`, `venv/` (bytecode is already in the managed block) |
  | Java / Kotlin (Maven / Gradle) | `target/`, `build/`, `*.class` |
  | .NET | `bin/`, `obj/` |
  | Go | *(none — builds out of tree; skip)* |

  Same discipline as the managed block: **add-only, de-duplicating, never remove or
  reorder**. If every entry already exists, add nothing (most brownfield repos — this seed
  is a no-op for them by design).
- **Greenfield (no stack yet):** there is nothing to seed at enable — the fix is *timing*.
  Ensure the greenfield Open Thread (Step 5b) carries the "seed the stack's build-output
  ignores when the stack lands" action, and mention it in the Step 9 next steps. The agent
  working in the repo when the first build manifest appears applies this table then.

**Non-goal:** this is a minimal seed to keep the first build from polluting `git status`,
not gitignore management — the team owns their `.gitignore`; never expand the table into
IDE/OS/coverage/etc. entries.

### Step 7b — Install / merge `.gitattributes` (Windows line-ending hardening, v4.20.2)

The executable scripts (`*.sh`) and git hooks (`.githooks/*`) **must stay LF**, or Git for Windows
(`core.autocrlf=true` by default) rewrites them to CRLF on checkout and bash fails with
`bad interpreter: /usr/bin/env bash^M`. The canonical rules live in `templates/.gitattributes`:

```
*.sh        text eol=lf
.githooks/* text eol=lf
```

Apply additively (same discipline as `.gitignore`): **no `.gitattributes`** → copy
`templates/.gitattributes` verbatim; **exists** → add only the LF rules not already present
(de-duplicate; never remove/reorder the user's entries). After adding, run `git add --renormalize .`
(a no-op if the files are already LF) so the index reflects the attributes.

---

## Step 8 — Verify

Before reporting, sanity-check the output. Fix any issue found here before
proceeding — the report should describe a correct state, not optimistically
describe what was intended.

1. **Files exist.** Confirm all of the following are present in the target repo:
   - `memory/instructions.md`, `memory/continuity.md`, `memory/sessions/`
   - `memory/decay-policy.md`, `memory/archive/INDEX.md`, `memory/smoke-test.md`, `memory/vision.md`
   - `.agent/schema.md`, `.agent/version.md`
   - `DECAY.md`, `REVIEW.md`, `SKILLS.md`, `MERGE.md`
   - `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursorrules`, `.windsurfrules`,
     `.github/copilot-instructions.md`
   - The forge set (v4.31.0/v4.32.0), per Step 4 detection — GitHub:
     `.github/workflows/agent-memory.yml` + `.github/pull_request_template.md`; GitLab:
     `.gitlab/agent-memory-ci.yml` + `.gitlab/merge_request_templates/Default.md` + the
     `include: local:` entry present in `.gitlab-ci.yml`; Azure DevOps:
     `.azuredevops/agent-memory-ci.yml` + `.azuredevops/pull_request_template.md` (+ the
     activation command present in the Step 9 report); unknown forge: the GitHub + GitLab sets
   - `.gitignore` exists and contains the agent-memory sentinel line plus the
     AI-infrastructure entries (Step 7) — and, when Step 4 detected a stack, its
     build-output paths are ignored (pre-existing or via the stack-aware seed;
     greenfield instead carries the action in its Open Thread).
   - `.agent/version.md` records the version from this tool's root `VERSION`.

2. **No unfilled placeholders.** Grep for `{{` in every file you created.
   If any remain, fill them now.

3. **Mode C — integration is faithful.** For each vendor file migrated, confirm
   that at least the project name, stack, or a key rule from the original appears
   in `memory/instructions.md`. If the vendor content is absent, re-run the
   integration step for that vendor.

4. **Mode C — session files are well-formed.** Confirm each session file under
   `memory/sessions/` has a title line matching
   `# Session (YYYY-MM-DDThh:mm:ss.mmmZ - YYYY-MM-DDThh:mm:ss.mmmZ)`.

5. **Vision bootstrapped (not fabricated).** `memory/vision.md` exists with the
   Current-state context filled and the target / success criteria / non-goals left as
   prompts. The ⚠️ DRAFT banner and the `(…)` prompts are **intentional** — not unfilled
   placeholders. A `- [ ] (vision-bootstrap)` Open Thread is present in `continuity.md`,
   and no Blueprint gaps were derived yet (they await the confirmed Vision).

6. **Skills installed + promoted + adapters complete.** Confirm the **built-in skills**
   (`memory-lint`, `second-opinion`, `apply-critique`, `sync-adapters`, `harvest-knowledge`) were
   installed into `agent-skills/` (Step 5i) and `review-scratch/` is gitignored. Additionally (Mode C), if the source repo had
   vendor skills (e.g. `.claude/skills/`), confirm each was promoted to
   `agent-skills/<name>/SKILL.md` (committed), the original preserved under `legacy/`.
   **Assert adapter completeness (v4.12.0):** after the closing `sync skill adapters` (Step 5h),
   **every** `agent-skills/<name>/` has all six adapters present
   (`.claude/skills/<name>/SKILL.md`, `.gemini/commands/<name>.toml`, `.cursor/rules/<name>.mdc`,
   `.kiro/skills/<name>/SKILL.md`, `.github/skills/<name>/SKILL.md`, `.agents/skills/<name>/SKILL.md`) and no *generated* adapter is orphaned (each has a live
   `agent-skills/<name>/`). Any miss or orphan ⇒ re-run sync. (Enforcement is now *checked*, not
   convention — the loose end that a recommend-only check left open.)

7. **Knowledge harvest ran (curious discovery).** Confirm Step 4b actually descended
   into any documentation tree (recursively, not depth-1) and swept the repo root for
   knowledge markdown (decision logs, ADRs, kanban/roadmap, architecture notes). If a
   `docs/` tree or root-level knowledge doc exists, its durable facts should be reflected
   in `instructions.md` / `continuity.md` / smoke-test / vision — or, if it exceeded the
   read budget, captured in a `- [ ] (knowledge-harvest)` Open Thread. A docs folder that
   exists but left **no trace anywhere** means the harvest was skipped — re-run Step 4b.

8. **First enable session log written (Mode A).** Confirm a session log exists under
   `memory/sessions/` (title line `# Session (…Z)`, persist-time UTC filename) recording
   the enable **and the discovery depth the user chose** (`standard scan` / `deep analysis`).
   If the user chose `deep`, confirm the deep findings landed in the **neutral** memory layer
   (`instructions.md` / `continuity.md`) and **not** in a vendor steering file. Missing log ⇒
   write it now (Step 5c).

Log any issue you cannot fix as an Open Thread in `memory/continuity.md` and
note it in the report.

---

## Step 9 — Report

Print a clear summary including migration details if Mode C ran:

```
✓ AI-enabled: /absolute/path/to/target-repo
  Mode: <Fresh Enable | Migrated from <vendors> | Already Ours>

  Detected:
  • Project:    <name>
  • Language:   <language>
  • Stack:      <stack>
  • Type:       <type>
  • Forge:      <GitHub | GitLab | Azure DevOps | unknown → GitHub+GitLab sets installed>  (self-managed GitLab: note the runner prerequisite; Azure DevOps: one-time pipeline activation in Next steps)
  • Discovery:  <standard scan | deep analysis>  (Fresh Enable — user's choice, recorded in the first session log)

  Migrated (Mode C only):
  • <vendor>:  <files>  →  <where>
  • Sessions converted: N (from <oldest>  to  <newest>)
  • Skills promoted: N → agent-skills/  (+ Claude / Gemini / Cursor / Kiro / Copilot / Antigravity adapters regenerated)

  Created:
  • memory/instructions.md
  • memory/continuity.md
  • memory/decay-policy.md
  • memory/smoke-test.md
  • memory/vision.md   (⚠️ DRAFT — maintainer to confirm the target; see the (vision-bootstrap) thread)
  • memory/sessions/   (N session files)
  • memory/archive/INDEX.md
  • memory/sessions/<first enable log>  (Fresh Enable — records the enable + chosen discovery depth)
  • .agent/schema.md, .agent/version.md  (v<version>)
  • DECAY.md, REVIEW.md, SKILLS.md, MERGE.md
  • agent-skills/  (built-in skills: memory-lint, second-opinion, apply-critique — + regenerated adapters)
  • AGENTS.md, CLAUDE.md, GEMINI.md, .cursorrules,
    .windsurfrules, .github/copilot-instructions.md
  • .githooks/ + CI floor  (<.github/workflows/agent-memory.yml | .gitlab-ci.yml (created | include appended) + .gitlab/agent-memory-ci.yml | .azuredevops/agent-memory-ci.yml (inert until activated) | GitHub+GitLab sets (forge unknown)>; GitLab add-only: state the actual pipeline coverage)
  • <.github/pull_request_template.md | .gitlab/merge_request_templates/Default.md | .azuredevops/pull_request_template.md | GitHub+GitLab (forge unknown)>  (What/Why description template)
  • .gitignore  (created | updated — AI-infrastructure entries; + review-scratch/ for the review pair)

  Preserved (Mode C only):
  • legacy/<original-files>  (originals, do not edit)

  Skipped:      <any>

  Next steps:
  1. Review memory/instructions.md and memory/continuity.md
  2. Verify migrated sessions look correct (memory/sessions/)
  3. cd /path/to/target-repo
  4. git add . && git commit -m "chore: AI-enable repo (migrated from <vendor>)"
  5. (greenfield only) When your stack lands, seed its build-output .gitignore
     entries — the greenfield Open Thread carries this action (Step 7 table)
  6. (Azure DevOps only) AFTER pushing the enable commit, activate the ritual floor —
     one-time, your credentials (also carried by the (forge) Open Thread until done):
     az pipelines create --name agent-memory --repository <repo> --repository-type tfsgit --branch <default> --yml-path .azuredevops/agent-memory-ci.yml --skip-first-run
```

---

## Step 10 — Offer Post-Enable Actions

After reporting, offer:

> "Would you like me to:
>   (a) Open memory/continuity.md so you can review what I detected
>   (b) Walk through the migrated sessions
>   (c) Both
>   (d) Done"

Respond accordingly.

---

## Notes

- Never modify source code in the target repo.
- Never modify `package.json`, `Cargo.toml`, etc.
- Only create/modify files within: `memory/`, `.agent/`, `legacy/`, `agent-skills/` (the
  neutral capability layer) and its regenerated per-machine adapters (`.claude/skills/`,
  `.gemini/commands/`, `.cursor/rules/`, `.kiro/skills/`, `.github/skills/`, `.agents/skills/`), `review-scratch/` (gitignored
  fresh-context review scratch, if the review pair is accepted), `DECAY.md`, `REVIEW.md`,
  `SKILLS.md`, `MERGE.md`, `.gitignore` (add-only, never remove existing entries),
  `.github/copilot-instructions.md`, `.githooks/` + the forge CI floor —
  `.github/workflows/agent-memory.yml` (GitHub) / `.gitlab/agent-memory-ci.yml` +
  `.gitlab/merge_request_templates/` + `.gitlab-ci.yml` (GitLab; **add-only** when the file
  pre-exists — only the `include:` entry, never `workflow:rules`) /
  `.azuredevops/agent-memory-ci.yml` + `.azuredevops/pull_request_template.md` (Azure DevOps;
  never touch an existing `azure-pipelines.yml`) — the v4.19.0/v4.31.0/v4.32.0
  ritual triggers, and the bootstrap files listed in Step 6. (`UPGRADE.md` and `VERSION` are tool-only — never written into a
  target.)
- **Activating the local git hook** (`git config core.hooksPath .githooks`) is the one allowed git-*config*
  change in the target — it points git at the committed `.githooks/`; it writes no source and is reversible
  (`git config --unset core.hooksPath`). Do it for the user; never ask them to.
- If the target repo is the agent-memory tool itself, say so and stop.
- Always preserve vendor originals under `legacy/` — they are user data.
