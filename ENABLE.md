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
No AI footprint found. Proceed to Step 4 (generate from scratch).

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

(Skip this step if Mode C populated everything already — go to Step 5.
Otherwise, proceed.)

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

**Structure signals**
- Top-level folder names (src/, app/, lib/, api/, frontend/, backend/, etc.)
- Presence of `Dockerfile`, `docker-compose.yml`, `.github/workflows/`
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

---

## Step 5 — Generate or Complete Memory Files

If Mode A (fresh): generate all memory files from templates, replacing every
`{{placeholder}}` with real content derived from your analysis.

If Mode C (post-migration): the migration process will have created partial
files. Fill in any sections still containing placeholders, using your repo
analysis. Do NOT overwrite content that migration already placed.

### 5a. `memory/instructions.md`

Fill in:
- What this project actually is (from README / package description)
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
  - Otherwise `(none yet)`
- `last_review`: `(none yet)`
- **repo:** write the path `~`-relative (e.g. `~/projects/foo`) — never an absolute
  `/Users/<name>/…` (or `/home/<name>/…`) path. `memory/` is committed to git and
  shared across the team, so absolute home paths would leak the enabling user's
  username to everyone.
- **Architectural Invariants:** seed from hard constraints in the build manifest /
  README / `instructions.md` (things that must never change — e.g. "POST-only API",
  "no runtime deps"). If none are obvious, remove the section. Facts here never decay.
- Open Threads: include any TODOs surfaced during analysis or migration
- **Metadata footers:** give every fact you write a kebab `id` and the footer
  `<!-- id: … | created: <today> | last_used: <today> | uses: 1 | tier: working -->`.
  Ordinary facts are born `tier: working`; **Architectural Invariants get `tier: core`**;
  unchecked Open Threads get an id but never decay. `uses: 1` / `last_used: today` is
  the honest seed (the enable counts as the first reference) — the review owns those
  fields thereafter; don't hand-edit them. See `.agent/schema.md` and `DECAY.md` §1.
  (The optional `origin` field is set when facts are created in normal sessions; omit
  it at enable — there's no session log yet. A later review can backfill it.)

### 5c. `memory/sessions/`

If Mode C, sessions will already be populated from migrated history.
Otherwise create the directory with a `.gitkeep` file.

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
Step 4 analysis — things a newcomer should be able to learn from memory alone (e.g. "How
does `<entry point>` discover/route X?", "What gates Y?"). They join the generic
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
  `{{PROJECT_TYPE}}` from your Step 4 analysis — what the project *is* today).
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

**Install all four** (every mode, including a fresh Mode A enable): copy `agent-skills/<name>/`
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
- `.github/copilot-instructions.md`

`CLAUDE.md` and `GEMINI.md` contain `{{PROJECT_NAME}}` and `{{PROJECT_ONELINE}}`
placeholders — fill them from your Step 4 analysis (project name + a one-line
description) so eagerly-loaded runtimes get context without an extra hop. The
remaining bootstrap files install verbatim.

Also install the evolving-memory protocol docs at the target root, **copied
verbatim from this tool's root** (they are generic — no placeholders):

- `DECAY.md`
- `REVIEW.md`
- `SKILLS.md`

These must travel into the target because the review ritual (and skill sync/adopt) run
*inside* the enabled repo. (`UPGRADE.md` is tool-operator-only — do **not** install it.)

**Ritual triggers (v4.19.0) — install + activate (no manual user step).** Also copy verbatim from this
tool's root, so the after-session ritual fires reliably for *any* vendor (see `docs/DESIGN-ritual-triggers.md`):

- **`.githooks/`** — the committed, vendor-neutral git hooks (`post-commit` + its `README.md`): auto-stub
  a session log when a commit does real work without one; re-sync adapters when a skill changed.
- **`.github/workflows/agent-memory.yml`** — the **CI floor**: runs `memory-lint` + an advisory
  session-log check on push/PR.

**Ensure `.githooks/post-commit` is executable** (`chmod +x`; it must be committed with mode `100755`) —
git **silently ignores** a non-executable hook. Then **the agent activates the local hook**: run
`git config core.hooksPath .githooks` in the target — **do this yourself; never ask the user** (the
adoption constraint: any manual step is a barrier). CI needs
no activation (a committed workflow runs server-side, zero per-user config). *Honest limit:* git can't
auto-run committed hooks on a fresh clone (security), so where no agent has run, **CI is the backstop**.
Both `.githooks/` and `.github/workflows/` are **tracked** (they travel); only `.github/skills/` is
gitignored. The hooks/CI are **advisory** (never block); the tool runs nothing itself
(`no-build-step-agent-run` — git/CI invoke them in the user's env).

**Conflict handling:**
- If Mode C ran and a vendor bootstrap file was migrated, the migration step
  already moved it to `legacy/` — proceed to install our version.
- If the file exists but is identical to our template, skip silently.
- Otherwise ask the user per-file: overwrite / skip / rename existing to `.bak`.

Create `.github/` in the target if it does not exist.

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
   - `DECAY.md`, `REVIEW.md`, `SKILLS.md`
   - `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursorrules`, `.windsurfrules`,
     `.github/copilot-instructions.md`
   - `.gitignore` exists and contains the agent-memory sentinel line plus the
     AI-infrastructure entries (Step 7).
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
   (`memory-lint`, `second-opinion`, `apply-critique`) were installed into `agent-skills/`
   (Step 5i) and `review-scratch/` is gitignored. Additionally (Mode C), if the source repo had
   vendor skills (e.g. `.claude/skills/`), confirm each was promoted to
   `agent-skills/<name>/SKILL.md` (committed), the original preserved under `legacy/`.
   **Assert adapter completeness (v4.12.0):** after the closing `sync skill adapters` (Step 5h),
   **every** `agent-skills/<name>/` has all six adapters present
   (`.claude/skills/<name>/SKILL.md`, `.gemini/commands/<name>.toml`, `.cursor/rules/<name>.mdc`,
   `.kiro/skills/<name>/SKILL.md`, `.github/skills/<name>/SKILL.md`, `.agents/skills/<name>/SKILL.md`) and no *generated* adapter is orphaned (each has a live
   `agent-skills/<name>/`). Any miss or orphan ⇒ re-run sync. (Enforcement is now *checked*, not
   convention — the loose end that a recommend-only check left open.)

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
  • .agent/schema.md, .agent/version.md  (v<version>)
  • DECAY.md, REVIEW.md
  • agent-skills/  (built-in skills: memory-lint, second-opinion, apply-critique — + regenerated adapters)
  • AGENTS.md, CLAUDE.md, GEMINI.md, .cursorrules,
    .windsurfrules, .github/copilot-instructions.md
  • .gitignore  (created | updated — AI-infrastructure entries; + review-scratch/ for the review pair)

  Preserved (Mode C only):
  • legacy/<original-files>  (originals, do not edit)

  Skipped:      <any>

  Next steps:
  1. Review memory/instructions.md and memory/continuity.md
  2. Verify migrated sessions look correct (memory/sessions/)
  3. cd /path/to/target-repo
  4. git add . && git commit -m "chore: AI-enable repo (migrated from <vendor>)"
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
  `SKILLS.md`, `.gitignore` (add-only, never remove existing entries),
  `.github/copilot-instructions.md`, `.githooks/` + `.github/workflows/agent-memory.yml` (the v4.19.0
  ritual triggers), and the bootstrap files listed in Step 6. (`UPGRADE.md` and `VERSION` are tool-only — never written into a
  target.)
- **Activating the local git hook** (`git config core.hooksPath .githooks`) is the one allowed git-*config*
  change in the target — it points git at the committed `.githooks/`; it writes no source and is reversible
  (`git config --unset core.hooksPath`). Do it for the user; never ask them to.
- If the target repo is the agent-memory tool itself, say so and stop.
- Always preserve vendor originals under `legacy/` — they are user data.
