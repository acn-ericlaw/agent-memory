# UPGRADE — Version Ladder

> How a repo already enabled with agent-memory is upgraded in place to the current
> tool version. **This file is reached only through `ENABLE.md` Mode B** — never
> invoked directly, exactly as `MIGRATE.md` is reached only through Mode C. The
> user's single entry point stays "AI enable this repo". This doc is
> tool-operator-only; it is *not* installed into target repos.

---

## Versioning model

The current tool version lives in the root **`VERSION`** file (semver):
- **MAJOR** — breaking change to memory-file shape/protocol (an un-upgraded agent
  couldn't correctly read/maintain the new files).
- **MINOR** — additive, backward-compatible (new optional file, vendor, section).
- **PATCH** — wording/clarity only.

### One version per *release*, not per feature (consolidate unreleased increments)

`VERSION` and the ladder below are **release** artifacts — there is **one rung per released
version**, i.e. per state a user could actually have been running. So:

- **Bump for a release event** (the commit/push that ships the work), not once per feature.
  Several features developed before a release **collapse into a single version bump**.
- While work is **unreleased**, treat the next version as **pending and mutable**: keep adding
  features under that one number; the rung enumerates them. Do not mint 4.23, 4.24, … for
  successive features that never shipped independently — that inflates the ladder with rungs no
  repo ever stepped through.
- **Bump magnitude = the largest change in the batch** (MAJOR > MINOR > PATCH). Four additive
  features ⇒ one **MINOR**.
- **The released baseline is `VERSION` at `HEAD`** (the last commit/push). Before committing a
  batch, **consolidate** any working-tree bumps beyond that baseline into the single next version.
- The **per-feature** record is not lost — it lives in the **session logs** (immutable journal)
  and the `## Open Threads` in `continuity.md`, which carry each feature's id, origin, and detail.
  Version numbers track releases; memory tracks the work.

*(Precedent: v4.22.0 bundles four features iterated in one unreleased session — originally
dev-numbered 4.22–4.25 — into a single MINOR over the released 4.21.0.)*

| Version | Capability |
|---|---|
| 1.0.0 | Fresh enable from templates (Mode A) |
| 2.0.0 | Vendor detection + migration (Mode C); idempotent re-runs (Mode B) |
| 3.0.0 | Evolving memory: fact metadata + ids, decay-policy, review ritual, archive |
| 3.1.0 | AI-infrastructure `.gitignore` propagated into enabled repos (created or appended) |
| 3.2.0 | Protocol clarifications: session = one log-write (start best-effort); metadata ownership; stack-fact altitude; after-session checklist |
| 3.3.0 | Supersession: a fact can be marked `superseded` (replaced/invalidated), archived flagged "superseded" not "faded", terminal (never reactivated) |
| 3.4.0 | Invariant verification: `verify_invariants_every` prompts a human to re-confirm never-decay facts (`core` / Architectural Invariants) — never-decay ≠ never-checked |
| 3.5.0 | Write-time contradiction check: a new fact is scanned against existing ones → supersede (§9) or raise a `Contradiction:` Open Thread; review backstop |
| 3.6.0 | Memory smoke test: `memory/smoke-test.md` — manual eval, N questions a fresh agent should answer from memory alone |
| 3.7.0 | Provenance + retrieval: optional `origin:` footer (the session a fact came from); retrieval documented as lexical + indexed by design |
| 4.0.0 | Forward layer (VBDI): `memory/vision.md` + `(blueprint)` gap threads + altitude trace; the cognitive loop over the memory substrate. Upgrade bootstraps a DRAFT Vision + human gate |
| 4.1.0 | Cross-vendor skills layer: neutral committed `agent-skills/<name>/SKILL.md` + an `AGENTS.md` baseline (agent-as-runtime) + regenerated Claude/Gemini/Cursor adapters. Migration promotes vendor `.claude/skills/` into `agent-skills/`; upgrade promotes any existing vendor skills in place |
| 4.1.1 | Skills-layer refinements (PATCH): folder finalized as `agent-skills/` (collision-safe); Cursor adapter uses the agent-requested type (`description` + empty `globs` + `alwaysApply: false`); collision guard; vendor-dir double-duty clarified |
| 4.2.0 | "Sync skill adapters" operation: regenerate the per-vendor adapters from `agent-skills/` on demand (needed after clone/pull — adapters are gitignored, don't travel). The adapter recipe + sync steps now live in the installed `AGENTS.md` "Skills" section (canonical); `ENABLE.md` Step 5h references it |
| 4.3.0 | Skill **authoring convention** (create in `agent-skills/`, never a vendor folder) + **"adopt skill"** safety-net (promote a vendor-folder-authored skill into `agent-skills/`), wired into the session-close ritual so a natively-authored skill is never left unshared |
| 4.3.1 | Skills-layer doc fixes (PATCH, from a session-close test-drive): "Adopt a skill" no longer says "commit" mid-ritual (stage for the session-end commit); session-close check notes adopt-before-log ordering; body-normalization + detection clarified |
| 4.3.2 | Skills-layer description hardening (PATCH, from a lifecycle sanity check): adapter `description` mirrors the neutral skill's verbatim; skill descriptions kept single-line & quote-free (escape/quote if unavoidable) so they embed safely in TOML/MDC/YAML — prevents invalid or drifted adapters |
| 4.3.3 | Skills-layer description guidance (PATCH): `description` should be **concise** + trigger-phrase-rich (~1–2 sentences — matched within a small discovery budget, so long abstract paragraphs weaken activation); YAML `>`/`|` blocks are YAML-only, so the canonical value stays one logical line (it also mirrors into TOML) |
| 4.4.0 | Lightweight skills: per-session `AGENTS.md` keeps only the runtime baseline + a pointer; the adapter recipe + **sync**/**adopt**/**sanity-check** ops move to an on-demand installed `SKILLS.md`. The per-session "skills safety check" is **removed** (skill work is a conscious, on-demand action); upgrades do a read-only filename check that *recommends* sync |
| 4.5.0 | Kiro adapter: a 4th skills adapter target `.kiro/skills/<name>/SKILL.md` (Kiro follows the open Agent Skills standard — same shape as the Claude adapter); Kiro added to the Mode C detection table (steering/specs/skills). Kiro auto-reads root `AGENTS.md`, so the memory layer needs no pointer file |
| 4.5.1 | Skills-layer guidance (PATCH, from a Gemini CLI dogfood): the Gemini adapter is a **slash command** `/<name>` (explicit, not natural-language auto-matched) — NL routes through the baseline to the same skill; trigger semantics differ per vendor; and `sync skill adapters` must **never commit / recommend committing** the gitignored adapter dirs (only `agent-skills/` is shared) |
| 4.5.2 | Kiro hooks in Mode C (PATCH, from a Windows/Kiro enable): the `MIGRATE.md` Kiro protocol now handles `.kiro/hooks/*.kiro.hook` — preserved verbatim under `legacy/kiro/hooks/`, never converted/run. Human-gated commit hooks (like Kiro's) align with agent-memory; only an *unprompted* auto-commit/push is surfaced as an Open Thread. README gains a bootstrap edge-case note ("Start from `AGENTS.md`" when an enterprise IDE self-bootstraps) |
| 4.6.0 | Vendor-neutral **commit attribution**: `AGENTS.md` extends "identify yourself" (already true for session logs) to commits — deliberate, human-initiated, with a `Co-Authored-By: <agent>` trailer. Encodes once in the shared layer what Claude Code does automatically and Kiro needed a per-machine hook for; soft guidance, a no-op where the runtime already does it |
| 4.7.0 | **Lightweight mode** for memory-neutral tasks (from a Kiro enablement): a trivial task (no new fact/decision/thread/state change) writes a **one-line "lite" session log** (`## Memory References` → `(none)`) and skips the full template / fact-footers / continuity edits. Ledger stays continuous; the review handles it as a normal reference-free session. Scales the per-session ceremony to the actual memory impact |
| 4.7.1 | Lightweight mode keyed to **file-change, not "trivial"** (a judgment call both AI and human misjudge): **read-only** sessions (no file changes) write **no log**; **any file change** (even one line) writes at least a **lite log** (never skipped on a "felt trivial" call); a memory-relevant event → full ritual |
| 4.8.0 | Review **self-verify guard** (from a Copilot review that over-archived recent facts): a new `REVIEW.md` step greps the last `archive_window` sessions for each about-to-be-archived id — any hit ⇒ the `sessions_since_last_used` count was wrong, keep the fact — and confirms no id lives in both `continuity.md` and the archive. Replaces a hand-counted judgment with a checkable signal for the riskiest operation |
| 4.9.0 | **`memory-lint`** — a portable, optional verifier skill (`agent-skills/memory-lint/` + `scripts/memory-lint.py`, Python 3 stdlib) that runs the decay-integrity checks *deterministically* (id-in-both-places, archived-but-recently-referenced, overdue advisory, supersession links). Moves the arithmetic off the LLM; `REVIEW.md` step 6 points to it. Caught a real over-archival on first run. The tool never runs it (`no-build-step-agent-run`) — agent/human/CI-invoked |
| 4.10.0 | **Fresh-context second opinion** — a skill pair (`second-opinion` + `apply-critique`): snapshot the current task (derived from `continuity.md` + recent sessions, never a parallel state file) for a clean-memory reviewer (any vendor / fresh session) behind a **security advisory**, then apply the returned critique through a **bounded, validated, human-gated** loop (build/tests + `memory-lint`; critique is advisory). Snapshots/critiques live in gitignored `review-scratch/`. ENABLE and the upgrade ladder now **install** the built-in skills (this pair + `memory-lint`, which the review ritual relies on). Folds the "AIF" idea into skills + VBDI |
| 4.10.1 | **`memory-lint` bug fix:** its Memory-References parser is now **line-anchored** (`(?m)^## +Memory References[ \t]*$`) instead of `find("## Memory References")`, so a session log that *quotes* the heading in prose no longer trips a false `over-archived` error. Script-only; no description/shape change |
| 4.10.2 | **Fresh-context-review critique fixes (PATCH):** `memory-lint`'s `FOOTER_RE` now binds to a single line so an *unclosed* footer can't silently swallow the file and misparse decay metadata; the install protocol (`ENABLE.md` §5i) **warns before overwriting a locally-modified built-in** instead of silently clobbering it; the `upgrades-additive` invariant text carries its tool-managed-built-ins exception inline; and `second-opinion` gains a same-vendor-vs-different-vendor caveat. No description/shape change |
| 4.10.3 | **Lightweight-mode wording fix (PATCH):** `AGENTS.md` now keys the session-log test to whether a **tracked** file changed (the *objective* test is the **git diff**, not any filesystem write), and explicitly exempts runs whose only writes are **gitignored, regenerated artifacts** (`sync skill adapters`, `review-scratch/`, the compiled lint artifact) → **no log**. Aligns the lightweight-mode note with what `SKILLS.md` already states (sync "touches no committed file"); prevents a spurious lite log after every adapter sync. Wording-only |
| 4.10.4 | **`memory-lint` nested list fix (PATCH):** hardened the verifier script to handle deeply-nested lists correctly. `pinned_open_threads` now checks indentation level so a parent Open Thread's pinned state isn't dropped by a standard sub-bullet. |
| 4.11.0 | **`memory-lint` Node runtime (MINOR):** the deterministic verifier now ships in **both** Python (`memory-lint.py`) and Node (`memory-lint.mjs`, Node ≥ 18, built-ins only) at feature + output parity, so a machine with only Node still runs the script instead of a hand count. `SKILL.md` documents both commands as interchangeable; a shared test contract (`test_memory_lint.mjs` ↔ `.py`) holds them equivalent. Additive — no dispatcher, no installer (the agent picks the runtime) |
| 4.11.1 | **Review step-6 archival guard hardened (PATCH):** `REVIEW.md` step 6 now defines a "use" as a `## Memory References` entry, not a prose mention — `memory-lint` is the preferred check (Memory-References-only, immune to the trap) and the by-hand fallback only counts in-block hits. Fixes an archival livelock (`ot-review-step6-prose`) where a review naming a fact while deferring it re-armed the guard forever. Doc + tests only; the verifier script was already correct (`memref_ids` line-anchored since 4.10.1) |
| 4.12.0 | **Enforced adapter sync at enable + upgrade (MINOR):** ENABLE and **every** Mode B re-enable (upgrade or already-up-to-date) now **run** `sync skill adapters` instead of the read-only "recommend, don't run" check — so a skill's vendor-native adapters are actually materialized (closing the gap where a skill predating a new adapter target, e.g. Kiro, or a fresh clone/pull, was left without working native skills). Idempotent, writes only gitignored files (no committed change, no version bump, no session log); `no-build-step-agent-run` holds (the agent runs it during a human-invoked enable/upgrade). The per-session path still never touches skills; content-drift realignment is still the on-demand `skill sanity check` |
| 4.12.1 | **`memory-lint` dangling-link cross-file fix (PATCH):** `load_repo` now pools footers from other `memory/*.md` files (e.g. `vision.md`), excluding `continuity.md`/`decay-policy.md`, into an `extra` set used **only** for supersession-link resolution in `check_dangling` — so a fact superseded by a target whose footer lives in `vision.md` no longer false-flags as `[dangling]`. Both runtimes (`.py` + `.mjs`) fixed at parity; regression test added to both suites (`.mjs` now also exports `load_repo`/`check_dangling` to enable it). Found dogfooding `~/sandbox/simple-proxy`; ported back from there |
| 4.13.0 | **Tool-provided (system) skills marked + upstream advisory (MINOR):** the three shipped built-ins carry `provenance: agent-memory-builtin` in their `SKILL.md` frontmatter (+ a body banner), so a target's AI recognizes a system skill **at edit time** — and `SKILLS.md` (new "Tool-provided (system) skills" section) tells it to **fork** a local variant or **upstream** a genuine fix to the agent-memory project (issue in production; maintainer advisory pre-release) rather than strand it. `ENABLE.md` §5i's warn-before-overwrite extended with the same upstream advice. Closes the gap that let the simple-proxy `memory-lint` fix nearly get lost. Adapters unchanged (mirror only name+description) |
| 4.14.0 | **Optional Architecture Decision Record log (MINOR):** documents an **optional** human-facing `docs/ADR.md` decision log at the VBDI **Design** altitude — one durable architecture decision per entry (Status/Date/Abstract/Rationale-with-consequences), newest-first, `Proposed → Accepted → Superseded/Deprecated`, **never deleted** (mirrors `DECAY.md` §9). Map-don't-duplicate: live constraints stay in `continuity.md`, the ADR carries the *why*, cross-linked by `formalizes:` ↔ a visible `(ADR-NNNN)` tag in the invariant title (a human pointer, not an agent read-cue). Read **on demand** — **not** in the per-session read path (zero default token cost). Documented in `.agent/schema.md` + `AGENTS.md`; **not auto-installed** into targets (adopt on demand) |
| 4.14.1 | **Re-synced `AGENTS.md` source clarified (PATCH):** `UPGRADE.md` now maps each re-synced file to its one canonical source — a target's `AGENTS.md` comes from **`templates/AGENTS.md`** (the memory hub), **never** the tool's **root** `AGENTS.md` (the operator/dual-mode dispatcher, which references the non-installed `ENABLE.md`) — with a self-check (a target `AGENTS.md` must not say "AI-Enable Another Repository"). The 4.14.1 rung **verifies + repairs** a mis-synced `AGENTS.md`. Found dogfooding a v3.7.0→v4.14.0 upgrade (GitHub Copilot, `mercury-composable`) that grabbed the root file |
| 4.15.0 | **ADR log upkeep trigger (MINOR):** the optional `docs/ADR.md` log is now *maintained*, not just documented — **once it exists**, making a new durable architecture decision, or superseding/invalidating a continuity fact carrying an `(ADR-NNNN)` tag, **prompts a human-gated ledger update** (add a newer ADR; mark the old `Superseded`/`Deprecated`, never delete; keep `formalizes:` ↔ `(ADR-NNNN)` in sync). Closes the 4.14.0 gap where the log could be adopted but had no cue to evolve. Re-syncs `templates/AGENTS.md` + root `AGENTS.md`, `templates/.agent/schema.md`, and `DECAY.md §12`; still **not auto-installed**. Surfaced dogfooding `mercury-composable`'s ADR opt-in |
| 4.16.0 | **ADR default path aligned to industry convention (MINOR):** the optional ADR log default path changes from `docs/ADR.md` to `docs/arch-decisions/ADR.md`. Normative: `.agent/schema.md`, `AGENTS.md` (root + template), `DECAY.md §12`; this repo moves its own `docs/ADR.md`. Targets at the new path already (e.g. `mercury-composable`) need no file move — version bump only |
| 4.16.1 | **Session filename drift fix (PATCH):** closes two gaps that caused date-only filenames (`YYYY-MM-DD.md`): `templates/AGENTS.md` + `schema.md` now require `date -u +%Y-%m-%d-%H%M%S` (no "or equivalent"); `memory-lint` gains `check_session_filenames` warning (check 5) in both runtimes |
| 4.17.0 | **GitHub Copilot CLI skills adapter (MINOR):** a **5th** skills adapter target `.github/skills/<name>/SKILL.md` — Copilot CLI follows the open Agent Skills standard (same `SKILL.md` shape as the Claude/Kiro adapter) and auto-matches by `description` (also accepts `/<name>`). `sync skill adapters` now writes **five** adapters; `.github/skills/` is gitignored **path-scoped** (the rest of `.github/` — `copilot-instructions.md`, `workflows/` — stays tracked). Copilot also gains skills in the Mode C detection/migration table (`.github/skills/`, `.agents/skills/` → `agent-skills/`); `templates/.github/copilot-instructions.md` now points Copilot at the skills layer. Mirrors the 4.5.0 Kiro rung. Surfaced dogfooding `~/sandbox/simple-proxy` (Copilot CLI couldn't find a skill authored only in `agent-skills/`) |
| 4.18.0 | **`sync skill adapters` is now a runnable script (MINOR):** a new built-in **`sync-adapters`** skill ships a deterministic adapter-regeneration script (Node + Python at parity, built-ins only) that (re)writes the five vendor adapters for every skill and prunes the orphans it generated. Replaces the prose-recipe-only sync that agents (e.g. Copilot CLI / Gemini) struggled to *run* — they hunted for a non-existent npm/MCP command and flailed. Enable + every Mode B re-enable now invoke the script; an agent also triggers it by description. Consistent with `no-build-step-agent-run` (same category as the `memory-lint` script). Surfaced dogfooding `~/sandbox/simple-proxy` |
| 4.19.0 | **Vendor-neutral ritual triggers (MINOR):** the after-session ritual no longer relies on the agent self-triggering. Enable installs a committed **`.githooks/post-commit`** (auto-stubs a session log when a commit does real work without one; re-syncs adapters), **agent-activated** via `git config core.hooksPath .githooks` (no manual user step), plus a **CI floor** (`.github/workflows/agent-memory.yml`: `memory-lint` + advisory session-log check on push/PR, zero per-user setup). Advisory by default (opt-in `AGENT_MEMORY_STRICT=1` gate); `no-build-step-agent-run` holds (git/CI invoke them; the tool runs nothing). Honest limit: git can't auto-run hooks on a bare clone → CI is the backstop. From real client-team pain (ritual not followed even with Claude; Copilot-only teams had no triggers) + the zero-manual/untrained-user constraint; design `docs/DESIGN-ritual-triggers.md` |
| 4.20.0 | **First-run init (MINOR):** closes the fresh-clone activation gap (Copilot dogfood: the memory bootstrap self-initializes, but a clone has the gitignored adapters **absent** + the hook **unactivated**). Adds **`.githooks/init.sh`** (one idempotent command: regenerate adapters + `git config core.hooksPath .githooks`) + an **`AGENTS.md` self-init note** so the agent does it on its first session. One agent-run step (or one human command) instead of two; CI stays the zero-config floor |
| 4.20.1 | **Self-init in `copilot-instructions.md` (PATCH):** v4.20.0's self-init reached Claude (acts on `AGENTS.md`) but **not Copilot CLI** (its `start` front-loads `copilot-instructions.md` + summarizes — so on a fresh clone the hook stayed inactive + adapters absent). Folds the first-run init into the **top of `copilot-instructions.md`** so Copilot runs `bash .githooks/init.sh` before summarizing. Re-sync that one file; the `init.sh` fallback + CI floor are unchanged |
| 4.20.2 | **Windows line-ending hardening (PATCH):** adds a **`.gitattributes`** pinning `*.sh` + `.githooks/*` to **LF**, so Git for Windows (`core.autocrlf=true`) doesn't rewrite them to CRLF on checkout (which breaks bash: `bad interpreter: /usr/bin/env bash^M`, silently disabling the hook + `init.sh`). Installed/merged into targets additively (like the `.gitignore` block). Makes the bootstrap + hooks robust on Windows (Git Bash / WSL), not luck-of-the-default. From a Copilot Windows-feasibility check |
| 4.20.3 | **memory-lint catches an empty/malformed version manifest (PATCH):** adds a deterministic **`check_version_manifest`** ERROR to both runtimes (`memory-lint.py` + `memory-lint.mjs`, at parity, with mirror tests) so a present-but-empty/malformed `.agent/version.md` fails the lint floor (CI + reviews) instead of silently breaking Mode B upgrade detection. Closes the loop on the v4.20.1 bug (a truncating stamp one-liner emptied a target's `version.md` → an agent misread the version). A *missing* `version.md` stays valid (pre-versioning baseline) and is not flagged. Re-copy the memory-lint skill files |
| 4.21.0 | **Google Antigravity (`agy`) skills adapter (MINOR):** a **6th** adapter target `.agents/skills/<name>/SKILL.md` — the open Agent Skills standard dir read by Google Antigravity (the Gemini CLI successor), which reads `.agents/skills/`, **not** the old `.gemini/commands/*.toml`. `sync skill adapters` now writes six; `.agents/` gitignored; `.gemini/commands` kept for the transition. Skill-only re-copy + re-sync; no memory-file shape change |
| 4.22.0 | **Discovery, consent & merge-friendliness — four bundled additive improvements (MINOR).** One release; developed iteratively in one unreleased session (dev-numbered 4.22–4.25), consolidated per "one version per release." **(a) Curious knowledge harvest at enable** — `ENABLE.md` Step 4b recursively descends every doc tree (`docs/`/`wiki/`/`rfcs/`/`adr/`/…, all subfolders) + sweeps repo roots for human-authored knowledge markdown (decision logs, ADRs, kanban/roadmap, architecture notes), distilling durable facts into memory (map-don't-mirror), bounded by a read **budget with disclosure** (overflow → a `(knowledge-harvest)` thread). **(b) Fresh-enable advisory + discovery depth** — Mode A opens with a concise **exec summary of the protocol** (what it is / writes / won't touch / is committed+shared) + a `cancel` gate (**informed consent**), then offers **standard scan vs `/init`-depth deep analysis** (deep written to the neutral memory layer, never a vendor file); a first enable session log records the choice. **(c) `continuity.md` merge-friendliness** — `status` is spec'd a SHORT current-state line, **not a changelog** (`.agent/schema.md` + `AGENTS.md`); new **"Concurrency & merge-friendliness"** conventions (one fact/line; append-only union/keep-both; scalar take-later); `memory-lint` **check 7** flags a leftover conflict marker (`<<<<<<<`/`>>>>>>>`/diff3 `|||||||`) as an ERROR (bare `=======` setext underline exempt), both runtimes + tests. **(d) `MERGE.md`** — a new installed, no-code on-demand protocol for resolving a git conflict in `memory/`: tiered + human-gated, enforcing **`never-pick-a-winner`** (mechanical → rule; semantic clash → preserve both + Contradiction/supersession; `memory-lint` gate; human approves). Mostly operator-side (`ENABLE.md`) + the `memory-lint` skill + one new root doc (`MERGE.md`); no memory-file shape change. From a client enablement complaint, a teammate-concurrency review, and a GitHub Copilot review |
| 4.22.1 | **post-commit auto-stub: per session, not per commit (PATCH):** the `.githooks/post-commit` auto-stub now suppresses a new stub when a session log already exists within an **active-session window** (default 2h; override `AGENT_MEMORY_SESSION_WINDOW_HOURS`), nudging the agent to enrich the existing log instead. Detected by the newest session **filename** timestamp (immutable + clone-safe; `mtime` is reset by checkout) vs a window-ago stamp. The old guard checked only for an *untracked* stub, so after the log was committed every later work commit wrote a fresh stub — ~6 near-identical lite logs/session, inflating the decay session-count. New session (no log in window) still stubbed; bash 3.2-compatible. From downstream `mercury-composable` feedback |
| 4.22.2 | **Lightweight mode: one log per session, not per commit (PATCH):** the agent-side mirror of 4.22.1. `AGENTS.md` lightweight mode now says that if a session log already exists for *this* working session, a later **memory-neutral** commit **enriches** it rather than spawning another lite log (clutter + decay session-count inflation). Memory-relevant work still gets its own full log. Doc-only; re-sync `templates/AGENTS.md` (+ root `AGENTS.md`). No shape change |
| 4.22.3 | **Tighten the post-commit session window: 2h → 30 min (PATCH):** v4.22.1's window was 2h, but observed follow-up stubs were **minutes** apart and 2h can conflate a *new* session started within 2h of the prior log. Default now **30 min**; override env var renamed to **`AGENT_MEMORY_SESSION_WINDOW_MINUTES`** (integer minutes — BSD `date -v` rejects fractional hours). Re-copy `.githooks/post-commit`; no shape change |
| 4.22.4 | **Safe-write safeguard in `REVIEW.md` (PATCH):** the review ritual's Safety section now mandates **append-mode / read-into-var (never `open(f,"w").write(open(f).read()+…)`, which truncates before the read)** for scripted archive/`continuity.md` edits, and **running `memory-lint` after any scripted memory mutation** (it catches truncation; git recovers). From a real archive-truncation incident during a review. Re-sync `REVIEW.md`; no shape change |
| 4.23.0 | **`harvest-knowledge` built-in skill (MINOR):** a **5th** built-in (`provenance: agent-memory-builtin`) — the on-demand, recurring counterpart to the enable-time curious harvest (Step 4b). Re-scans the repo's human-authored docs and folds newly-durable facts into the neutral, shared `memory/` **additively** (map-don't-mirror; check-existing-first; conflicts → `Contradiction`; budget-with-disclosure). Keeps a living repo's memory in sync as docs evolve; **not** a vendor `/init` (that does code-analysis → a vendor steering file; this does knowledge-distillation → neutral memory, additive + repeatable). "Re-harvest" moves out of the Mode B upgrade path into this skill — the enable-time harvest stays a fresh-enable event. Installed by §5i (now 5 built-ins); on the rung, re-copy the skill + re-sync adapters |
| 4.23.1 | **`last_harvest` marker for incremental harvests (PATCH):** Project State gains an optional `last_harvest: YYYY-MM-DD | through <session>` field (in `continuity.md`, with `last_review`/`last_invariant_check` — **not** `version.md`); `harvest-knowledge` reads it to scope the next run to docs changed since then (full pass if absent) and stamps it on completion (even a no-op). From a cross-vendor test drive where the agent had to infer the window. Re-sync `.agent/schema.md` + the `harvest-knowledge` skill; no shape change (the field is additive + optional) |
| 4.23.2 | **Context-hygiene guidance — keep state externalized so compaction is safe (PATCH):** `AGENTS.md` (template + root) gains a "Long session? Keep state externalized" block. Two corrections to an initial "brain fog" framing: the agent usually **can't compact itself** (so its lever is *externalizing state*), and the **objective** health signal is **context-window utilization (tokens vs. limit)**, not time or a felt "fog." Teaches: write the session log + `continuity.md` at each natural seam **before** compaction; at high utilization suggest compacting (or rely on auto-compact), never mid-task; re-verify against live files afterward. Re-sync `templates/AGENTS.md`; doc-only, no shape change |
| 4.24.0 | **Decay-policy retune + review-cadence/size advisory in `memory-lint` (MINOR):** from real measurements across two enabled repos (one ran 61 sessions / 41 facts / 585 lines and **archived nothing** — the cadence review never fired in the field). `memory-lint` gains advisory check (8), both runtimes + mirror tests: `[review-overdue]` (`sessions_since_last_review ≥ review_every`, from the `last_review` stamp) and `[continuity-bloat]` (> `continuity_max_facts` / `continuity_max_lines`) — so a lapsed review rides every lint run + CI. New default `continuity_max_facts: 30` (count-based primary signal); `continuity_max_lines: 300 → 600`; `verify_invariants_every: 20 → 40`. Re-copy the memory-lint skill files; re-sync `REVIEW.md` + `AGENTS.md` + `.agent/schema.md`; merge the policy additively (preserve any custom-tuned values). Skill description unchanged → adapters need no re-sync |
| 4.25.0 | **`archive-fact` — deterministic safe archive-move (MINOR):** a **6th** built-in (`provenance: agent-memory-builtin`) executing `REVIEW.md` step 4's move (continuity → quarter archive + INDEX) deterministically — reads the file into memory and writes once, so the truncate-before-read trap that wiped this repo's archive can't recur. Python + Node at parity + mirror tests; all-or-nothing guards (missing id / already-archived / would-empty); `--dry-run`. The agent decides *what* to archive; the helper does the *move* (`never-pick-a-winner` intact). From a cross-vendor critique (Gemini 3.1 Pro: "harden the memory-writing mechanism itself"). doc → tool, after v4.22.4's doc safeguard. Install via §5i (now 6 built-ins); re-copy the skill + re-sync adapters; re-sync `REVIEW.md`/`ENABLE.md` |
| 4.26.0 | **`refresh-metadata` + `memory-lint` `[stale-metadata]` advisory (MINOR):** a **7th** built-in executing REVIEW.md steps 2–3 (apply events + re-tier) deterministically — recomputes every fact's `last_used`/`uses`/`tier` from the session reference log and writes footers back (the "full rebuild" path, runnable; pure arithmetic, never archives, `core`/`superseded` untouched). Python + Node at parity + mirror tests; `--dry-run`; idempotent. `memory-lint` gains check (9) `[stale-metadata]` (stored tier ≠ recomputed tier) to make the skipped-re-tier gap visible. From a cross-vendor field test where Gemini 3.1 Pro ran the overdue review but did the archive and skipped the metadata pass. Install via §5i (now 7 built-ins); re-copy the skill + re-copy memory-lint + re-sync adapters + re-sync `REVIEW.md`/`ENABLE.md` |
| 4.26.1 | **Pinned-thread tier no longer flagged/rewritten (PATCH):** v4.26.0's `[stale-metadata]` flagged every `working`-tagged pinned `- [ ]` open thread as "should be `active`" — noise (a pinned thread never decays regardless of tier label; pinned-ness protects it). `memory-lint` `expected_tier` + `refresh-metadata` `expected_tier` now return a pinned thread's **stored** tier (no flag, no rewrite; factual `uses`/`last_used` still refresh). Re-copy the `memory-lint` + `refresh-metadata` skill files; `DECAY.md` rule 4 clarified. From a mercury sanity check + comparison with Copilot's `update-metadata.py`. Both runtimes at parity + tests |
| 4.27.0 | **Standardized PR description: lead with What / Why (MINOR):** every agent-memory-enabled repo now ships a **`.github/pull_request_template.md`** with two sections — **What** (the change) and **Why** (the intent it serves — Blueprint gap / decision / problem, not a restatement of What), each 1–2 short paragraphs drawn from the session log(s) in the PR. Mirrored by an `AGENTS.md` convention (the vendor-neutral backstop for agents composing PR bodies via `gh`, not the web UI) + a checklist line. Advisory, never a gate — consistent with *why-as-first-class-artifact* throughout the protocol. Install the template into the target (`.github/`); re-sync `AGENTS.md` from `templates/AGENTS.md`. No memory-file shape change |
| 4.28.0 | **Co-author convention cleanup — stable agent identity + one trailer (MINOR):** refines the v4.27.0 self-identification. The `Co-Authored-By` trailer should use the **stable agent name** (e.g. `Claude Code`, `Gemini CLI`) — the actual AI collaborator, **not** a model-version string (which churns each release and fragments attribution) — matching session logs. Adds squash-merge guidance: collapse to a **single** trailer (GitHub appends a consolidated one after the `---------` line; trim the redundant inline repeats). Re-sync `AGENTS.md` from `templates/AGENTS.md` + re-copy `.github/pull_request_template.md` (footer comment updated). Doc-only; advisory; no memory-file shape change |
| 4.28.1 | **Post-commit hook: uncommitted-session-log guard (PATCH):** the auto-stub window check misfired on the recommended two-commit pattern (feature commit → `chore(memory)` commit) when the session log was written more than 30 min before the feature commit — the filename-timestamp threshold treated an in-flight (uncommitted) log as "too old" and stubbed a near-duplicate. Fix: before the time-window check, inspect `git status --porcelain -- memory/sessions/` — if any `.md` is staged, modified, or untracked, the agent already has a log for this session; emit the enrich-and-commit nudge and skip the stub. The existing filename-window check stays as fallback for already-committed, hours-old logs. Bash 3.2-compatible; hook stays non-blocking. Re-copy `.githooks/post-commit` |
| 4.28.2 | **`memory-lint` `[continuity-bloat]` counts only decay-eligible facts (PATCH):** field report from `mercury-composable` — the fact-count check fired **permanently** even right after a fully correct review, because it counted `tier: core` facts (structural invariants) and pinned `- [ ]` open threads against `continuity_max_facts`, and those can never be archived. That turned the primary lean signal into chronic noise → alarm fatigue (the exact "nobody archives" failure v4.24.0 set out to fix). Fix aligns the count with `decay-policy.md`'s documented intent ("count of **decaying** facts/threads"): `check_continuity_health` now excludes `tier: core` + pinned ids before comparing (both runtimes at parity + mirror regression tests; warning text now reads "decay-eligible facts"). A repo with 14 core + 11 open threads + 16 working facts now reads `16 < 30` (clean) instead of `41 > 30`. Re-copy the `memory-lint` skill files (both runtimes). Skill description unchanged → adapters need no re-sync |
| 4.28.3 | **`[continuity-bloat]` line-count message is decay-aware (PATCH):** a second `mercury-composable` report (29-module reactor) — after a clean review the *fact* count is healthy but the `continuity_max_lines` backstop trips on genuinely-active, dense Key Decisions, and the review has **nothing to archive**, so the warning is unclearable *and* its "a review is due to lean it down" wording nudges toward premature archival of active facts (REVIEW.md's costliest error). Same failure class as v4.28.2, on the line axis. `memory-lint` now computes `archivable` (facts overdue for decay + superseded); when lines exceed the cap but `archivable == 0` the message names the real lever — "condense shipped decisions, or raise `continuity_max_lines`" — instead of prescribing a review that can't help; the actionable message still fires when something *is* archivable. `decay-policy.md` comment notes the cap is meant to be raised for a legitimately large repo. Fact-count check untouched; a dedicated "condense" lever deferred until the need recurs. Re-copy the `memory-lint` skill files (both runtimes) + re-sync `memory/decay-policy.md` comment additively. Skill description unchanged → adapters need no re-sync |
| 4.28.4 | **`Co-Authored-By` dedup invariant — one trailer per collaborator, keyed on email (PATCH):** a third `mercury-composable` report — the v4.28.0 attribution guidance assumed the agent *fully authors* the message, but it co-authors it **with its harness**, which often injects its own (model-version) `Co-Authored-By`; appending a second stable-name trailer produced duplicate co-authors for one collaborator (squash-merges compounded it — one commit reached 55 trailer lines). `AGENTS.md` (root + `templates/`) reframes the model (*reconcile* the harness's message, don't blindly append) and states the invariant — **at most one `Co-Authored-By` per collaborator, matched on email** (`Claude Code` / `Claude Opus 4.8` / `Gemini CLI` are one collaborator at one `noreply@…` address) — with a 3-branch resolution tree + forge-aware squash guidance. PR-template footer + docs site updated to match. Doc-only; a dedup **hook** and lint advisory were deliberately **deferred** (an auto-dedup `commit-msg` hook would rewrite commits — a departure from the tool's never-mutate-your-commits stance). Re-sync `AGENTS.md` + `.github/pull_request_template.md`. No memory-file shape change; skills/adapters unchanged |
| 4.29.0 | **Before-session context presence (MINOR):** closes the before-session half of the ritual-trigger asymmetry — v4.19.0 made the *after*-session rituals fire vendor-neutrally, but git/CI has no session-start moment, so "read `AGENTS.md`/`memory/*` first" stayed advisory prose (empirically skipped under task pressure; child-repo field report 2026-07-11). `templates/CLAUDE.md` + `templates/GEMINI.md` now carry native **`@`-imports** (`@AGENTS.md`, `@memory/instructions.md`, `@memory/continuity.md`, `@memory/vision.md`; Gemini uses the `@./` form, `.md`-only) so the hub + core memory files are structurally present every session on import-capable runtimes — same fix-shape as v4.20.1's copilot-instructions front-load; imports live only in per-vendor bootstrap files, `AGENTS.md` stays vendor-neutral. `docs/optional-ritual-hook.md` (tool-only) gains an **opt-in** Claude Code `SessionStart` injection recipe — never installed by default (a committed `.claude/settings.json` conflicts with the installed `.gitignore` and risks leaking personal allowlists). Attestation canaries remain a downstream per-repo pattern. Honest limits: imports can't express dynamic paths (`memory/sessions/`); Cursor/Windsurf/Copilot keep the prose pointer; imported files enter context every session, so the continuity-bloat controls (v4.24.0/4.28.2/4.28.3) are now load-bearing. No memory-file shape change; skills/adapters unchanged |
| 4.29.1 | **Template import blocks → `{{BOOTSTRAP_IMPORTS}}` placeholder (PATCH):** tool-repo containment of instruction bleed-through that v4.29.0 amplified. Runtimes that auto-load directory-scoped instruction files picked up `templates/CLAUDE.md` in the tool repo, and its live `@`-imports (relative to the containing file) pulled the **placeholder template stubs** (`templates/AGENTS.md`, `templates/memory/*`) into context as instructions — found by a GitHub Copilot assessment, corroborated live on Claude Code. `templates/CLAUDE.md` + `templates/GEMINI.md` now hold a `{{BOOTSTRAP_IMPORTS}}` placeholder; `ENABLE.md` Step 6 defines the per-vendor literal blocks and expands at install — **installed output byte-identical to v4.29.0**. Targets: version-stamp only |
| 4.30.0 | **Stack-aware `.gitignore` build-output seed (MINOR):** from a greenfield field case (`mercury` — the installed AI-infra-scoped `.gitignore` left the later-arriving Rust toolchain's `target/` unignored; the first build polluted `git status`). `ENABLE.md` Step 7 gains a minimal, separately-sentineled **build-output seed** applied when Step 4 detects a stack (Rust `target/`; Node `node_modules/`, `dist/`; Python venvs; Java/Kotlin `target/`, `build/`, `*.class`; .NET `bin/`, `obj/`) — add-only, de-duplicating; Step 5b seeds a **greenfield Open Thread** carrying the "seed when the stack lands" action (at enable there is no stack to detect); Step 8/9 verify + report it. Explicit non-goal: minimal seed, never a gitignore manager. Operator-side only — no template/shape change |
| 4.31.0 | **GitLab forge support — forge-aware ritual floor + MR template (MINOR):** a GitLab-hosted field report (`.github/` is ignored entirely by GitLab) showed exactly two installed artifacts die there: the **CI floor** (`.github/workflows/agent-memory.yml` never runs → a fresh clone has NO ritual backstop — the v4.19.0 guarantee's silent collapse) and the **What/Why PR template**. "Vendor-neutral" had conflated *AI vendor* with *hosting forge*. Now: `ENABLE.md` Step 4 detects the forge (remote URL + `.gitlab-ci.yml`/`.gitlab/` signals; unknown → install both sets, additive-safe) and Step 6 installs a forge-matched set — GitLab gets `.gitlab/agent-memory-ci.yml` (same two checks; advisory via `allow_failure: exit_codes: [42]`, `AGENT_MEMORY_STRICT=1` gates) wired from `.gitlab-ci.yml` (copied verbatim when absent — carries the canonical `workflow:rules` guard; **add-only `include:` entry when pre-existing — never `workflow:rules`**, which would change when the repo's own jobs run) + `.gitlab/merge_request_templates/Default.md` (auto-applies, all tiers). `AGENTS.md` squash guidance is now forge-aware — the failure mode **inverts**: GitHub piles trailers up (dedup), GitLab's default squash message is the MR title only so trailers are **dropped** (make them survive: re-add at merge, or `%{all_commits}` in the squash template — `%{co_authored_by}` credits commit authors only, never body trailers). Local-tooling `.github/` files (copilot-instructions, skills adapters) correctly stay on every forge. Honest limit: GitLab.com runners are zero-config; self-managed needs an admin-registered runner. Docs/design claims forge-qualified throughout. No memory-file shape change; skills/adapters unchanged |
| 4.32.0 | **Azure DevOps forge support — own-pipeline ritual floor + PR template (MINOR):** third forge, from a real field installation. Enable detects `dev.azure.com`/`*.visualstudio.com` remotes (+ `azure-pipelines.yml`/`.azuredevops/` signals) and installs `.azuredevops/agent-memory-ci.yml` — a complete, self-contained pipeline (an existing `azure-pipelines.yml` is **never touched**; one repo carries many pipelines) with the best advisory semantics of the set (`##vso` warnings + `task.complete result=SucceededWithIssues` → native "partially succeeded"; `AGENT_MEMORY_STRICT=1` fails the run; `fetchDepth: 0`) — plus `.azuredevops/pull_request_template.md` (auto-applies; default-branch-read; 4000-char cap). **Honest limit — activation is not file-driven:** a pipeline is a *resource*; the committed file is inert until a one-time `az pipelines create … --skip-first-run` binding (Contributors-level; enable REPORTS the command, runs it only at explicit user direction), and Azure Repos ignores the YAML `pr:` key — PR-time validation is an optional Build Validation branch policy (admin; "Optional" mode = notify-only). Squash guidance gains the third branch (ADO drops trailers; no template mechanism; re-add via "Customize merge commit message"). Unknown forge installs GitHub+GitLab sets only (ADO needs positive detection). No memory-file shape change; skills/adapters unchanged |
| 4.32.1 | **Mode A `last_session` contradiction fix (PATCH):** `ENABLE.md` Step 5b still said a non-migrated enable leaves `last_session: (none yet)` — but Step 5c (added later) writes a **first enable session log** for every fresh enable, so "(none yet)" was false the moment the enable completed and it blinded the multi-agent continuity check that reads the field (5b's own footer bullet already pointed the seeded facts' `origin` at the 5c log). Step 5b now points `last_session` at the 5c log (`<today> | agent: <name> (<log filename stem>)`, filled when the log is written; Mode C branch unchanged); the template seed became a `{{LAST_SESSION}}` placeholder; the schema marks `(none yet)` as legacy (pre-4.32.1 enables only); the `rust-event-bus` fixture stays unedited (it truthfully predates Step 5c) behind a header note. Enable-time only — targets re-copy the schema + stamp, with an optional truth fix for a never-worked enable still showing `(none yet)` |
| 4.33.0 | **Session-log secret redaction — ritual rule + `memory-lint` `[secret-material]` advisory (MINOR):** a client-side DLP scanner caught a live OAuth client secret in a committed session log (pasted smoke-test output — nothing in the protocol stood between a rendered credential and `git push`). The after-session ritual (AGENTS.md root + template, ENABLE.md Step 5c, schema session-file section) now carries an explicit redaction rule — never write secrets or PII into `memory/`; redact pasted output to `(REDACTED)`; a committed secret is **exposed**: rotate it, redaction is not un-leaking, history cleanup is separate and human-led. `memory-lint` gains check 10 `[secret-material]` (both runtimes + mirror tests, 44 each): known token shapes (AWS/GitHub/GitLab/Slack/Google, private keys, JWTs), credential-key assignments with literal values (rendered-JAAS class; placeholders/`(REDACTED)`/number-shapes safe), emails (`noreply`/`git@`/example excluded), SSN + Luhn-verified cards, absolute home paths; scans `sessions/` + `archive/` (unlike check 7); **never echoes the matched value**; `lint:allow-secret-material` waives a quoted example line. Advisory (STRICT gates red). Redaction is the one sanctioned edit to an otherwise-immutable session log |
| 4.33.1 | **`[secret-material]`: ALL-CAPS enum constants are not credentials (PATCH):** check 10's first field contact (the 2026-08-13 Mode B upgrades of two production repos) produced exactly one finding — a **false positive**: a session log documenting Confluent's `bearer.auth.credentials.source` property with its enum value `OAUTHBEARER` (a source *type*, not a credential). The credential-assignment pattern now treats ALL-CAPS identifiers (`^[A-Z][A-Z0-9_]{2,}$` — `OAUTHBEARER`, `SASL_SSL`, `STATIC_TOKEN`, …) as config constants: real credentials carry mixed case/symbols, and uppercase-only token shapes (AWS key ids) stay covered by the value-shape patterns independently. Both runtimes at parity + mirror test (45 each). Detector-only — targets re-copy the built-in + stamp; a waiver added solely for this FP class can be dropped |
| 4.33.2 | **`[secret-material]`: backtick is a value delimiter (PATCH):** the v4.33.1 enum-constant exclusion missed the form the motivating field line actually used — markdown inline code: in `` `key=VALUE` `` the closing backtick rode into the captured value, so the ALL-CAPS rule didn't match and the FP survived (caught minutes after release by the 4.33.1 rung's own verify step against the live target). Every scanned memory surface is markdown — the assignment pattern now treats backticks like quotes; mirror enum test uses the exact field form + a backticked real-secret negative control (45 each). Also: the PR/MR description templates' rendered `<sub>` convention footer became an HTML comment (guides authors, never renders in a created PR/MR — maintainer feedback). Targets re-copy the built-in + stamp; the waiver drop 4.33.1 promised becomes genuinely possible here; optionally re-copy the forge description template if uncustomized |
| 4.33.3 | **`[secret-material]` security-review hardening (PATCH):** closes four fresh-context findings: all forge wrappers invoke `memory-lint --strict` so warnings reach their advisory/blocking branch and `AGENT_MEMORY_STRICT=1` genuinely gates; ALL-CAPS enums are exempt only on enum-dimension keys, closing uppercase-secret bypasses; quoted JSON/YAML assignments, Authorization headers, and embedded-placeholder values now flag without echoing secrets; Mode C redacts migrated history and triages lint before commit. Both runtimes byte-identical, 46 mirror tests each. Targets re-copy the built-in + forge CI file, merge migration guidance if applicable, then stamp |
| 4.33.4 | **`[secret-material]`: reject non-empty template defaults (PATCH):** v4.33.3's broad `${…}` placeholder exemption also trusted literal fallbacks, so `client_secret=${CLIENT_SECRET:-RealSecret123}` bypassed assignment detection. `${NAME}`, `${NAME:}`, and dotted references remain safe; non-empty defaults flag without echoing values. Both runtimes at parity, 46 mirror tests each. Targets re-copy the built-in + stamp |
| 4.34.0 | **Pre-commit secret guard, memory + config surfaces (MINOR):** the v4.33.x arc's missing timing layer — and the field incident's true *origin*: credentials entered the repo inside a Postman JSON and an OpenShift YAML before a dry-run contaminated a session log. The committed `.githooks/pre-commit` scans the **staged** content (index; only what THIS commit stages) of `memory/**.md` (full profile) and of config files (`.json`/`.yml`/`.yaml`/`.properties`/`.toml`/`.ini`/`.env*` — credential-class) **before the commit exists**; all three forge CI wrappers run the matching changed-config scan on push via the new `memory-lint --scan-files` mode. The guard **enforces by default** — findings block the commit, the deliberate exception to the advisory doctrine (secrets carry irreversible after-the-fact cost); `AGENT_MEMORY_SECRET_GUARD=advisory` opts down to warn-only, `--no-verify` bypasses once; JSON/properties exemptions in the committed, human-audited `.agent/secret-scan-ignore` (config only, never memory/); the CI floor stays advisory (`AGENT_MEMORY_STRICT=1` gates). Detector tuned on a 661-file live-corpus probe to zero FPs (single-brace + GH-Actions template forms, `demo`/`test` placeholder words, placeholder-fallback defaults, dotted route refs exempt from Authorization, `;` value delimiter, Postman split-pair pattern); 49 mirror tests per runtime, parity held. Rides existing `core.hooksPath` activation; never-initialized clones fall through to the CI floor |
| 4.34.1 | **Secret-guard output readability (PATCH):** field feedback from the maintainer's regression test — every `[secret-material]` finding line repeated the same advisory tail. Finding lines now end at `(N hit(s), first at line N)`; guidance appears **once per run**: the pre-commit hook's `-> fix it` footer (blank separator line added, shared/rotation/history wording folded in), a single trailer in `--scan-files` mode, and a single trailer after warnings in a full lint run. Both runtimes at parity, 49 mirror tests unchanged; hook grep contract unaffected. Targets re-copy the built-in + `.githooks/pre-commit`, stamp |
| 4.34.2 | **`[secret-material]`: the guard's own opt-down knob is not a credential (PATCH):** field FP (mercury-composable, 2026-08-19) — the pre-commit guard's blocking message prints `AGENT_MEMORY_SECRET_GUARD=advisory`, and any memory file documenting that guidance then flagged (`credential-assignment` — the key contains SECRET, `advisory` meets the value floor, no exemption applied). The tool taught a phrase and blocked its quotation. Fix (issue-proposed shape, endorsed): exact-key, value-constrained exemption in `_is_placeholder_value` — key `AGENT_MEMORY_SECRET_GUARD` (case-insensitive) with a documented setting (`advisory`/`enforcing`; trailing `).,` punctuation tolerated — the guard's own line ends `…=advisory)`, the v4.33.2 capture behavior). Any other value under that key still flags (no smuggling envelope; non-echo preserved). Both runtimes at parity, verbatim mirror fixtures (50 each). Also documented (maintainer call on the issue's secondary question): AWS's canonical doc-example keys **still flag by design** — waive deliberately with `lint:allow-secret-material`; no built-in whitelist |


Each enabled repo records what it is on in **`.agent/version.md`**:

```markdown
# agent-memory install manifest
- version:       3.0.0
- enabled_with:  2.0.0
- last_upgraded: 2026-06-13
- mode:          A
```

---

## How `ENABLE.md` Mode B uses this file

```
installed = read target .agent/version.md → version   (missing file → "2.x baseline")
current   = read tool root VERSION
if installed == current:  report "up to date — nothing to upgrade", stop.   # idempotent
if installed <  current:  run each rung below from installed up to current, in order;
                          then re-stamp .agent/version.md (version=current, last_upgraded=today);
                          report what changed.
if installed >  current:  the repo is newer than this tool checkout — stop and tell the user.
either branch (incl. "up to date"):  also run `sync skill adapters` (below) — idempotent, gitignored-only.
```

A **missing** `.agent/version.md` means the repo was enabled before versioning
existed. Treat it as `2.x` and run the 2→3 rung; create the stamp at the end.

Rungs are **idempotent**: before each change, check whether it is already present
and skip if so. Re-running an upgrade must be safe.

## Source of truth for re-synced files (read before any rung)

When a rung says "re-sync the generic docs," each file has **one** canonical source in this
tool's checkout. Copy from the right one into the **target repo root** — getting this wrong
silently installs operator-facing docs into a target:

| Target file | Copy from (this tool's checkout) |
|---|---|
| `DECAY.md`, `REVIEW.md`, `SKILLS.md`, `MERGE.md` | the tool **root** (`<tool>/DECAY.md`, …) — generic, no placeholders |
| **`AGENTS.md`** | **`<tool>/templates/AGENTS.md`** — the *target* memory-protocol hub |
| `.agent/schema.md` | `<tool>/templates/.agent/schema.md` |
| `CLAUDE.md`, `GEMINI.md`, `.cursorrules`, `.windsurfrules`, `.github/copilot-instructions.md` | `<tool>/templates/` |

⚠️ **Never install the tool's _root_ `AGENTS.md` into a target.** The root `AGENTS.md` is the
operator/dual-mode dispatcher — it routes between "AI-enable another repository" (→ `ENABLE.md`) and
"use as a memory system," and references operator-only files (`ENABLE.md`, `MIGRATE.md`, `UPGRADE.md`)
that are **not** installed in a target. The target gets `templates/AGENTS.md` (memory protocol only).
Rung notes that read "`AGENTS.md` (root + template)" mean the *change* lives in both copies **inside
this tool**; for the **target**, always install the **template**.

**Self-check after re-syncing `AGENTS.md`:** the target's `AGENTS.md` must **not** contain
"AI-Enable Another Repository" or reference `ENABLE.md`/`MIGRATE.md`/`UPGRADE.md`. If it does, the
wrong file was copied — replace it with `templates/AGENTS.md`.

## Scope (unchanged from `ENABLE.md`)

Target-repo only. Never touch `~/`, `~/.claude/`, `~/.cursor/`, Application
Support, AppData, or system paths. Never delete; preserve/append. Never modify
source code or package manifests.

---

## Skills adapter sync (every enable + Mode B re-enable) — enforced, v4.12.0

Independent of the version ladder: skill adapters are gitignored, so they don't travel with a
clone/pull, and a rung that adds a new adapter target (e.g. Kiro in 4.5.0) leaves older skills'
adapters incomplete. So on **any** enable and **any** Mode B re-enable — including "already up to
date" — **run the `sync skill adapters` script** (v4.18.0: `bash
agent-skills/sync-adapters/scripts/sync-adapters.sh`, or the `.mjs`/`.py`; see `SKILLS.md`) as the
closing skills step. For each `agent-skills/<name>/` it (re)writes the six vendor adapters
(`.claude/skills/<name>/SKILL.md`, `.gemini/commands/<name>.toml`, `.cursor/rules/<name>.mdc`,
`.kiro/skills/<name>/SKILL.md`, `.github/skills/<name>/SKILL.md`, `.agents/skills/<name>/SKILL.md`) and **prunes** orphaned adapters it
generated (signature-guarded — never touches a hand-authored vendor file; for Copilot, only
`.github/skills/`, never the rest of `.github/`). Older targets without the `sync-adapters` built-in
get it from the 4.18.0 rung; if absent, fall back to the prose recipe in `SKILLS.md`.

This is safe to run unconditionally because it is **idempotent** and writes **only gitignored**
files — never `agent-skills/`, never a committed file. So it is **not a version change and needs no
session log** (the lightweight-mode rule: a run whose only writes are gitignored, regenerated
artifacts). It does not violate `no-build-step-agent-run`: the **agent** runs it during a
human-invoked enable/upgrade — there is no daemon and no per-session automation. Report the counts:
*"synced N skill(s) → M adapters (gitignored — do not commit; only `agent-skills/` is shared); pruned
K orphan(s)."* If there are no skills, it is a no-op.

This **replaces the former read-only "recommend, don't run" check** (≤ v4.11.1): enable and upgrade
are deliberate, human-invoked moments, so *materializing* adapters then — rather than printing advice
the user must act on before the skills work natively — is correct. The **per-session** path still
never touches skills; deliberate **content-drift** realignment (a description that no longer mirrors
its skill) is still the heavyweight, on-demand `skill sanity check` in `SKILLS.md`.

---

## Rung: 2.x → 3.0.0 — add the evolving-memory layer

Backward-compatible: do not remove or rewrite existing content; only enrich and add.

1. **Backfill fact metadata in `memory/continuity.md`.** For every existing fact
   (Key Decisions, Conventions, Stack lines, User Preferences, …):
   - assign a unique kebab `id`,
   - append the footer
     `<!-- id: … | created: <today> | last_used: <today> | uses: 1 | tier: working -->`.
   Unchecked Open Threads (`- [ ]`) get an id but are pinned (never decay). Do not
   fabricate history — `created`/`last_used` = today, `uses` = 1 is the honest
   baseline for a repo that had no metadata before. Facts are born `working`; the
   first review re-tiers them from the session-log event stream.

2. **Add `## Architectural Invariants`** immediately above `## Key Decisions`. Seed
   it from hard constraints already visible in `memory/instructions.md` (things that
   must never change). If none are obvious, leave a one-line note and add an Open
   Thread asking the user to populate it. Facts here never decay.

3. **Add `last_review`** to Project State: `- **last_review:** (none yet)`.

4. **Install `DECAY.md` and `REVIEW.md`** at the repo root (copy verbatim from the
   agent-memory tool root). Skip any that already exist and match.

5. **Create `memory/decay-policy.md`** from `templates/memory/decay-policy.md`
   (default windows; fill `{{PROJECT_NAME}}`). Skip if it already exists.

6. **Create the archive.** `memory/archive/INDEX.md` with a header and an empty
   table. Skip if present.

7. **Add `## Memory References` to the session-log convention.** Re-sync
   `.agent/schema.md` from `templates/.agent/schema.md` (it now documents the
   section). Do **not** edit past session logs — they predate the convention and
   are immutable; the first review tallies forward only.

8. **Re-sync changed protocol files.** Compare the target's `AGENTS.md` against
   `templates/AGENTS.md` (Before/During/After now mention metadata + review) and
   update only if different. Other bootstrap files (`CLAUDE.md`, `GEMINI.md`,
   dotfiles) are unchanged in 3.0.0 — leave them.

9. **Stamp** `.agent/version.md` → `version: 3.0.0`, `last_upgraded: <today>`,
   preserving `enabled_with` and `mode` (if the stamp was missing, set
   `enabled_with` to the detected baseline and `mode: A`).

10. **Report**: facts backfilled (N), files created/installed, where the policy and
    archive now live, and a reminder to populate `## Architectural Invariants`.

---

## Rung: 3.0.0 → 3.1.0 — propagate the AI-infrastructure `.gitignore`

Additive: the enabling user's personal AI-IDE runtime directories (`.claude/`,
`.kiro/`, `.cursor/`, …) should not be committed to the shared repo. Earlier
versions only added a comment to an existing `.gitignore` and never created one, so
those entries never reached the target. Bring the target up to the current behavior.

1. **Apply the managed `.gitignore` block** exactly as `ENABLE.md` Step 7 describes
   (the same logic — keep them in lockstep): create from `templates/.gitignore` if
   the target has none, otherwise add the sentinel-headed block and **only the entries
   not already present anywhere in the file** (de-duplicate — an older enable or the
   user may already ignore `.kiro/` etc.). The sentinel is
   `# === agent-memory: AI infrastructure (personal / per-machine — do not commit) ===`.

2. **Never remove or reorder** existing `.gitignore` entries — add-only. Adding a
   path does not untrack already-committed files, so this is safe.

3. **Stamp** `.agent/version.md` → `version: 3.1.0`, `last_upgraded: <today>`,
   preserving `enabled_with` and `mode`.

4. **Report**: whether `.gitignore` was created or appended, and how many entries
   were added.

---

## Rung: 3.1.0 → 3.2.0 — protocol clarifications (session model, metadata ownership, altitude)

Documentation/protocol clarifications from a real-work field report. **No memory-file
*shape* change** — re-sync the generic protocol docs and leave existing facts alone;
the review reconciles tiers as usual.

1. **Re-sync the generic protocol docs** (copy verbatim from the tool root / templates,
   only where different): `DECAY.md`, `REVIEW.md`, `.agent/schema.md`
   (from `templates/.agent/schema.md`), and `AGENTS.md` (from `templates/AGENTS.md`).
   These now define a session as **one log-write** (several per conversation OK) with
   `start` **best-effort**; pin metadata ownership (agent seeds `id`/`created`/`tier` +
   `uses: 1`, the review owns `uses`/`last_used`/`tier`); state the
   leave-`[x]`-for-the-review rule; mark `## Stack & Tools` as the canonical stack
   home; and add an after-session checklist.

2. **Add the stack-altitude notes** (only if absent, don't move existing content): in
   `memory/instructions.md` that precise deps/versions live in `continuity.md` →
   `## Stack & Tools`, and the canonical-home note on that section.

3. **Don't rewrite existing fact metadata.** "Born `working`" applies to facts created
   from now on; leave already-stamped tiers for the review to reconcile.

4. **Stamp** `.agent/version.md` → `version: 3.2.0`, `last_upgraded: <today>`,
   preserving `enabled_with` and `mode`.

5. **Report**: which docs were re-synced and the notes added.

---

## Rung: 3.2.0 → 3.3.0 — supersession / fact-invalidation

Additive: a new terminal `superseded` tier + optional `superseded-by`/`supersedes`
footer fields, so a fact that becomes *false* (not just unused) is retired correctly.
**No shape change to existing facts** — repos without superseded facts are unaffected,
and the optional fields appear only when a fact is actually superseded.

1. **Re-sync the generic rule/protocol docs** (copy verbatim from the tool root /
   templates, only where different): `DECAY.md` (new `superseded` tier, §9, the rule),
   `REVIEW.md` (applies `Superseded:` events; archives flagged "superseded"),
   `.agent/schema.md` (footer fields + the `Superseded:` Memory-References line), and
   `AGENTS.md` (the after-session supersession step).
2. **No data migration.** Existing facts are untouched; supersession applies only when
   a fact is reversed/invalidated from now on.
3. **Stamp** `.agent/version.md` → `version: 3.3.0`, `last_upgraded: <today>`,
   preserving `enabled_with` and `mode`.
4. **Report**: docs re-synced; the supersession capability is now available.

---

## Rung: 3.3.0 → 3.4.0 — invariant verification cadence

Additive: never-decay facts (`core` / Architectural Invariants) can quietly go
*wrong*; the review now periodically prompts a human to re-confirm them. A new policy
knob + tracker field; no change to existing facts.

1. **Add `verify_invariants_every`** to `memory/decay-policy.md` (default `20`) — only
   if absent; preserve any existing value.
2. **Add `last_invariant_check`** to `continuity.md` Project State, just below
   `last_review` (value `(none yet)` if never run). It will first fire at the next
   review once that many session files exist.
3. **Re-sync the generic protocol docs** (copy verbatim where different): `REVIEW.md`
   (new routine step 6 + the verify trigger + summary line), `DECAY.md` (the
   "never-decay ≠ never-checked" note in §6), `.agent/schema.md` (the
   `last_invariant_check` Project-State field + the policy knob).
4. **Stamp** `.agent/version.md` → `version: 3.4.0`, `last_upgraded: <today>`,
   preserving `enabled_with` and `mode`.
5. **Report**: knob + tracker added, docs re-synced.

---

## Rung: 3.4.0 → 3.5.0 — write-time contradiction check

Additive (a behavioral rule + a review backstop; no new fields, tiers, or knobs). It
generalizes the migration-time contradiction check to normal sessions, resolving via
supersession (§9) or an Open Thread.

1. **Re-sync the generic protocol docs** (copy verbatim where different): `DECAY.md`
   (new §10), `REVIEW.md` (the "Contradiction backstop" note after the routine), and
   `AGENTS.md` (the before-adding-a-fact contradiction check in the after-session step).
2. **No data migration, no new metadata.** Nothing to backfill.
3. **Stamp** `.agent/version.md` → `version: 3.5.0`, `last_upgraded: <today>`,
   preserving `enabled_with` and `mode`.
4. **Report**: docs re-synced; the write-time contradiction check is now in effect.

---

## Rung: 3.5.0 → 3.6.0 — memory smoke test

Additive: a new installed file, `memory/smoke-test.md` — a manual memory-quality check.

1. **Create `memory/smoke-test.md`** from `templates/memory/smoke-test.md`, filling
   `{{PROJECT_NAME}}` and `{{TODAY}}`. Seed `{{PROJECT_SMOKE_QUESTIONS}}` with 2–4
   project-specific questions inferred from the existing `instructions.md` /
   `continuity.md` (a newcomer should be able to answer them from memory). Skip if the
   file already exists.
2. **Re-sync `.agent/schema.md`** (it now documents `memory/smoke-test.md`).
3. **Stamp** `.agent/version.md` → `version: 3.6.0`, `last_upgraded: <today>`,
   preserving `enabled_with` and `mode`.
4. **Report**: smoke test created; suggest running it once to set a baseline.

---

## Rung: 3.6.0 → 3.7.0 — provenance + retrieval-at-scale

Additive: an optional `origin:` footer field (provenance) + retrieval guidance. No new
machinery, no forced migration.

1. **Re-sync the generic docs** (copy verbatim where different): `DECAY.md` (the `origin`
   row in §1 + new §11 "Provenance & retrieval"), `REVIEW.md` (the `origin`-backfill
   note), `.agent/schema.md` (the `origin` field + the retrieval note), and `AGENTS.md`
   (set `origin` on new facts; the retrieval pointer in "Before Every Session").
2. **No backfill required.** `origin` is optional; new facts get it going forward, and a
   later review can repair it from the earliest `Created` event. Existing facts are fine
   without it.
3. **Stamp** `.agent/version.md` → `version: 3.7.0`, `last_upgraded: <today>`,
   preserving `enabled_with` and `mode`.
4. **Report**: docs re-synced; provenance pointers available on new facts.

---

## Rung: 3.7.0 → 4.0.0 — the forward layer (VBDI), with Vision bootstrap

A **new layer**, but still **additive**: a repo with no Vision works exactly as before
(an un-upgraded agent ignores `memory/vision.md` and `(blueprint)` threads). The catch
is that existing repos have no Vision/Blueprint — so this rung **bootstraps** them rather
than fabricating intent.

1. **Re-sync the generic docs** (copy verbatim where different): `DECAY.md` (§10 altitude
   drift + new §12 "The forward layer"), `REVIEW.md` (the Vision in the invariant-verify
   step + altitude drift in the backstop), `.agent/schema.md` (the `memory/vision.md` +
   Blueprint sections), and `AGENTS.md` (the "cognitive loop" section + Vision in the
   session read-list).
2. **Bootstrap the Vision — never fabricate it** (the target is the human's to set, like
   User Preferences). Create `memory/vision.md` from `templates/memory/vision.md`: fill
   `{{PROJECT_NAME}}` / `{{PROJECT_SLUG}}` / `{{TODAY}}` and the **Current-state context
   only** (`{{PROJECT_DESCRIPTION}}` / `{{PROJECT_TYPE}}` from the existing
   `instructions.md`); leave the target / success criteria / non-goals as the template's
   `(…)` prompts; keep the ⚠️ DRAFT banner. Skip if `memory/vision.md` already exists.
3. **Raise the human gate** in `continuity.md`:
   `- [ ] (vision-bootstrap) Confirm the Vision in memory/vision.md — set the target / success criteria / non-goals; then derive the Blueprint.`
   **Do not derive the Blueprint yet** (it needs the confirmed target). Until the Vision
   is confirmed, VBDI drift-detection stays advisory.
4. **Stamp** `.agent/version.md` → `version: 4.0.0`, `last_upgraded: <today>`,
   preserving `enabled_with` and `mode`.
5. **Report**: docs re-synced; Vision **bootstrapped as a DRAFT** — the maintainer must
   confirm it (the `(vision-bootstrap)` thread), after which the Blueprint is derived.

---

## Rung: 4.0.0 → 4.1.0 — the cross-vendor skills layer

Additive (a new optional shared layer): a repo with no skills works exactly as before, and
an un-upgraded agent simply ignores `agent-skills/`. Design: `docs/DESIGN-skills-layer.md`.

1. **Re-sync the generic docs** (copy verbatim where different): `.agent/schema.md` (the
   new `agent-skills/` section) and `AGENTS.md` (the new "Skills" section + the `agent-skills/` entry
   in Memory File Locations). `DECAY.md` / `REVIEW.md` are unchanged in 4.1.0.
2. **`.gitignore` — no entry change needed.** The vendor adapter dirs (`.claude/`,
   `.gemini/`, `.cursor/`) are already ignored by the v3.1.0 managed block, and `agent-skills/`
   is tracked by default (never ignored). Optionally refresh the managed-block comment to
   mention `agent-skills/` + adapters (cosmetic only).
3. **Promote any existing vendor skills.** If the target has `.claude/skills/` (or another
   vendor's skill bundle), promote each into `agent-skills/<name>/SKILL.md` per `MIGRATE.md`
   Section B2 (keep the procedure; normalize frontmatter to `name` + `description`; copy
   bundled scripts to `agent-skills/<name>/scripts/`), preserve the original under `legacy/`,
   then regenerate the Claude / Gemini / Cursor adapters per `ENABLE.md` Step 5h. **If there
   are no vendor skills, skip — do not create an empty `agent-skills/`.**
4. **Stamp** `.agent/version.md` → `version: 4.1.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
5. **Report**: docs re-synced; skills promoted (N) + adapters regenerated, or "no skills
   found — skills layer available on demand."

---

## Rung: 4.1.0 → 4.1.1 — skills-layer refinements (PATCH)

Wording/format corrections to the 4.1.0 skills layer; no shape change. (4.1.0 shipped
same-day and was unconsumed, so a target on 4.0.0 reaches 4.1.1 via the 4.0.0→4.1.0 rung
above — which already produces `agent-skills/`. This rung only matters for a repo that ran
the original 4.1.0, where the folder was briefly named `skills/`.)

1. **Rename the folder if needed.** If the target has a top-level `skills/` created by the
   original 4.1.0, rename it to `agent-skills/` (preserve history with `git mv` if tracked)
   and update the regenerated adapters' pointers. If it is already `agent-skills/` — or
   there are no skills — this is a no-op.
2. **Apply the doc/format fixes** (verbatim where different): `.agent/schema.md` and
   `AGENTS.md` now say `agent-skills/`; the Cursor adapter uses the agent-requested type
   (`description` + empty `globs:` + `alwaysApply: false`) — refresh any `.cursor/rules/`
   skill adapters accordingly.
3. **Stamp** `.agent/version.md` → `version: 4.1.1`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: folder renamed (if applicable), adapters refreshed, docs re-synced.

---

## Rung: 4.1.1 → 4.2.0 — "sync skill adapters" operation

Additive: a new agent-driven operation to regenerate per-vendor skill adapters from the
committed neutral skills — needed because adapters are gitignored and don't travel with a
clone/pull. No data, skill, or shape change.

1. **Re-sync the generic docs** (verbatim where different): `AGENTS.md` — its "Skills"
   section now carries the **canonical adapter recipe + the "sync skill adapters" operation**
   (the recipe moved here from `ENABLE.md` Step 5h, which now references it); and
   `.agent/schema.md` (notes the on-demand sync). `DECAY.md` / `REVIEW.md` unchanged.
2. **No data migration.** Existing skills/adapters are untouched. Optionally run "sync skill
   adapters" now to (re)generate this machine's adapters — it's on-demand and local.
3. **Stamp** `.agent/version.md` → `version: 4.2.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: `AGENTS.md` re-synced (now documents adapter sync); the operation is available.

---

## Rung: 4.2.0 → 4.3.0 — skill authoring convention + "adopt skill" safety-net

Additive (docs/protocol; no data or shape change). Closes the footgun where a skill authored
natively in a vendor folder (e.g. a built-in skill creator) is gitignored and never reaches
the shared `agent-skills/` layer.

1. **Re-sync the generic docs** (verbatim where different): `AGENTS.md` — its "Skills"
   section gains **"Authoring a skill"** (create in `agent-skills/`, never a vendor folder)
   and **"Adopt a skill"** (promote a vendor-authored skill into `agent-skills/`, then sync);
   the **"After Every Session"** ritual gains a **skills safety check** step + checklist line.
   `.agent/schema.md` notes it. `DECAY.md` / `REVIEW.md` unchanged.
2. **No data migration.** Existing skills/adapters untouched.
3. **Stamp** `.agent/version.md` → `version: 4.3.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: `AGENTS.md` re-synced (authoring convention + adopt safety-net + session-close check).

---

## Rung: 4.3.0 → 4.3.1 — skills-layer doc fixes (PATCH)

Wording/clarity only — surfaced by a fresh-agent test-drive of the session-close ritual. No
shape, data, or behavior change.

1. **Re-sync `AGENTS.md`** (verbatim where different): "Skills" → "Adopt a skill" no longer
   instructs a mid-ritual commit (stage the neutral skill for the session-end commit; the
   agent doesn't self-commit), and clarifies body normalization; the "After Every Session"
   skills safety check notes the adopt-before-log ordering. `DECAY.md` / `REVIEW.md` unchanged.
2. **Stamp** `.agent/version.md` → `version: 4.3.1`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
3. **Report**: `AGENTS.md` re-synced (adopt/commit + ordering + body clarifications).

---

## Rung: 4.3.1 → 4.3.2 — skill description hardening (PATCH)

Wording/clarity only — surfaced by a skill-lifecycle sanity check. Prevents two hard-to-spot
sync hazards: an adapter `description` drifting from the neutral skill, and a description with
special characters (e.g. `"`) producing invalid TOML / `.mdc`.

1. **Re-sync `AGENTS.md`** (verbatim where different): "Skills" → "Authoring a skill" now
   requires a **single-line, quote-free `description`**; the adapter recipe states the adapter
   `description` **mirrors the skill's verbatim** + an escape/quote fallback. `DECAY.md` /
   `REVIEW.md` unchanged.
2. **(If the target has skills)** re-run **"sync skill adapters"** so adapters pick up the
   verbatim description; if any skill `description` contains a `"`, rephrase it single-line and
   quote-free (or rely on the escape fallback). No committed change (adapters gitignored).
3. **Stamp** `.agent/version.md` → `version: 4.3.2`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: `AGENTS.md` re-synced; adapters re-synced if skills present.

---

## Rung: 4.3.2 → 4.3.3 — skill description guidance (PATCH)

Wording/clarity only — a discovery-budget refinement (a `description` is a model-matched
activation signal read within a small budget). No shape, data, or behavior change.

1. **Re-sync `AGENTS.md`** (verbatim where different): "Authoring a skill" now asks for a
   **concise**, trigger-phrase-rich `description` (~1–2 sentences, not a long abstract
   paragraph); the recipe notes YAML `>`/`|` blocks are YAML-only (the description also lands
   in a TOML adapter), so the canonical value is one logical line. `DECAY.md`/`REVIEW.md` unchanged.
2. **(If the target has skills)** optionally tighten any over-long `description` and re-run
   **"sync skill adapters"**. No committed change (adapters gitignored).
3. **Stamp** `.agent/version.md` → `version: 4.3.3`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: `AGENTS.md` re-synced; descriptions tightened if any were over-long.

---

## Rung: 4.3.3 → 4.4.0 — lightweight skills (recipe → on-demand `SKILLS.md`)

Additive relocation + a deliberate simplification: skill work is a *conscious, occasional*
developer action, so it leaves the per-session path. No skill data changes.

1. **Install `SKILLS.md`** at the target root (copied verbatim from this tool's root, like
   `DECAY.md`/`REVIEW.md`). It holds the authoring convention, the adapter recipe, and the
   **sync** / **adopt** / **sanity-check** operations — read on demand, not per-session.
2. **Re-sync `AGENTS.md`** (verbatim where different): the "Skills" section is now just the
   runtime baseline + a pointer to `SKILLS.md`; the verbose recipe/ops are gone from it. The
   **"After Every Session" ritual no longer has a skills safety-check step** (removed — see
   the standing skills-adapter sync this doc runs at every Mode B re-enable instead).
3. **No skill regeneration in this rung.** The standing skills-adapter sync (above) handles
   adapters — since **v4.12.0** it *runs* `sync skill adapters` (idempotent, gitignored-only) on
   every Mode B re-enable rather than only recommending it.
4. **Stamp** `.agent/version.md` → `version: 4.4.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
5. **Report**: `SKILLS.md` installed; `AGENTS.md` slimmed (per-session skills footprint cut;
   no per-session skills check); skills adapter check result.

---

## Rung: 4.4.0 → 4.5.0 — Kiro skills adapter (+ Mode C detection)

Additive: a 4th adapter target plus Kiro in the migration detection table. No skill data
changes; a repo with no skills (or no Kiro) works exactly as before. Design:
`docs/DESIGN-skills-layer.md`.

1. **Re-sync the generic docs** (copy verbatim where different): `SKILLS.md` (the adapter
   recipe now lists a **Kiro** target — `.kiro/skills/<name>/SKILL.md`, same shape as the
   Claude adapter, since Kiro follows the open Agent Skills standard), `AGENTS.md` (root +
   template: the adapter list now includes `.kiro/skills/`). `DECAY.md` / `REVIEW.md` unchanged.
2. **`.gitignore` — no entry change needed.** `.kiro/` is already in the v3.1.0 managed block
   (it is the adapter target for `.kiro/skills/`). Optionally refresh the managed-block comment
   to name `.kiro/skills/` among the adapters (cosmetic only).
3. **No skill regeneration in this rung.** If the target has skills but no `.kiro/skills/`
   adapters, the standing skills-adapter sync (above) materializes them — since **v4.12.0** it
   *runs* `sync skill adapters` (which writes the Kiro adapter too) on every Mode B re-enable,
   rather than only recommending it.
4. **Stamp** `.agent/version.md` → `version: 4.5.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
5. **Report**: docs re-synced; Kiro adapter now in the recipe; skills-adapter sync result
   (the `.kiro/skills/` adapters are (re)written by the standing sync).

---

## Rung: 4.5.0 → 4.5.1 — skills-layer guidance (PATCH, from a Gemini CLI dogfood)

Wording/guidance only; no shape change, no skill data changes.

1. **Re-sync the generic docs** (copy verbatim where different): `SKILLS.md` (the Gemini adapter
   is now noted as a **slash command `/<name>`** — explicit, not NL-auto-matched; a
   "trigger semantics differ per vendor" note; and a **never-commit-the-adapters** guard on the
   `sync skill adapters` operation), `AGENTS.md` (root + template: the adapter line now says
   "never commit them"). `DECAY.md` / `REVIEW.md` unchanged.
2. **No skill regeneration; no `.gitignore` change.** Adapters and `agent-skills/` are untouched;
   the managed block already ignores the adapter dirs.
3. **Stamp** `.agent/version.md` → `version: 4.5.1`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: docs re-synced (Gemini = slash command; adapters are never committed).

---

## Rung: 4.5.1 → 4.5.2 — Kiro hooks in Mode C (PATCH, from a Windows/Kiro enable)

Additive migration sub-case + a usage note; no shape change, no skill data changes.

1. **Re-sync the generic docs** (copy verbatim where different): `MIGRATE.md` (the Kiro protocol
   now has a **Hooks** sub-case — `.kiro/hooks/*.kiro.hook` are preserved verbatim under
   `legacy/kiro/hooks/`, never converted/run; human-gated commit hooks like Kiro's align — only an
   *unprompted* auto-commit/push is surfaced as an Open Thread, never disabled). `AGENTS.md` / `SKILLS.md`
   / `DECAY.md` / `REVIEW.md` unchanged.
2. **No skill regeneration; no `.gitignore` change.** `.kiro/` is already ignored.
3. **Stamp** `.agent/version.md` → `version: 4.5.2`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: Kiro migration now handles hooks (preserve, never run).

---

## Rung: 4.5.2 → 4.6.0 — vendor-neutral commit attribution (MINOR)

Additive convention; no shape change, no skill data changes. Makes any vendor add the deliberate,
self-identifying commit trailer that Claude Code does automatically and Kiro needed a hook for.

1. **Re-sync `AGENTS.md`** (root + template, verbatim where different): the "After Every Session"
   step 4 + checklist now carry the **commit-attribution convention** — *"commits are deliberate
   and human-initiated; identify yourself (e.g. a `Co-Authored-By: <agent>` trailer) the way you do
   in session logs."* Soft guidance, a no-op for runtimes that already do it. `SKILLS.md` /
   `DECAY.md` / `REVIEW.md` unchanged.
2. **No skill regeneration; no `.gitignore` change.**
3. **Stamp** `.agent/version.md` → `version: 4.6.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: `AGENTS.md` re-synced; commit-attribution convention now applies to every vendor.

---

## Rung: 4.6.0 → 4.7.0 — lightweight mode for memory-neutral tasks (MINOR)

Additive ritual carve-out; no shape change, no skill/memory data changes. From a Kiro enablement
finding (per-session write ceremony is heavy for trivial tasks).

1. **Re-sync `AGENTS.md`** (root + template, verbatim where different): "After Every Session" now
   has a **Lightweight mode** note — for a **memory-neutral** task (no new/changed fact, no
   decision, no Open Thread touched, no project-state change) write a **one-line "lite" session
   log** (`## Memory References` → `(none)`) and skip the full template / fact-footers / continuity
   edits. The ledger stays continuous; the review handles a lite log as a normal session with no
   references. `SKILLS.md` / `DECAY.md` / `REVIEW.md` unchanged.
2. **No skill regeneration; no `.gitignore` change.**
3. **Stamp** `.agent/version.md` → `version: 4.7.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: `AGENTS.md` re-synced; lightweight mode available for trivial tasks.

---

## Rung: 4.7.0 → 4.7.1 — lightweight mode keyed to file-change, not "trivial" (PATCH)

Refinement of the v4.7.0 carve-out; no shape change. "Trivial" is a judgment call (both AI and
human misjudge), so the skip is keyed to the **objective** "did a file change?" test.

1. **Re-sync `AGENTS.md`** (root + template, verbatim where different): the "Lightweight mode" note
   is now three-tier — **read-only** (no file changes) → **no session log**; **any file change** with
   no memory-relevant event → a **one-line lite log** (never skipped on a "felt trivial" call);
   **memory-relevant event** → full ritual. `SKILLS.md` / `DECAY.md` / `REVIEW.md` unchanged.
2. **No skill regeneration; no `.gitignore` change.**
3. **Stamp** `.agent/version.md` → `version: 4.7.1`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: `AGENTS.md` re-synced; lightweight mode now keyed to file-change (read-only = no log,
   any change = at least a lite log).

---

## Rung: 4.7.1 → 4.8.0 — review self-verify guard against decay miscounts (MINOR)

Additive review step; no shape change, no data changes. From a Copilot CLI review that
over-archived recent active facts (miscounted `sessions_since_last_used`).

1. **Re-sync `REVIEW.md`** (verbatim where different): new **step 6 "Verify archival"** before
   stamping — for each fact about to be archived as faded, `grep` the last `archive_window` session
   files for its id; any hit ⇒ keep it (count was wrong), don't archive; confirm no id lives in both
   `continuity.md` and the archive. Adds an `Archive-verify:` line to the review-summary format.
   `AGENTS.md` / `SKILLS.md` / `DECAY.md` unchanged.
2. **No skill regeneration; no `.gitignore` change.** No memory data changes (this is a review
   *process* guard for future reviews).
3. **Stamp** `.agent/version.md` → `version: 4.8.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: `REVIEW.md` re-synced; reviews now self-verify archival before stamping.

---

## Rung: 4.8.0 → 4.9.0 — `memory-lint` deterministic verifier skill (MINOR)

Additive: a portable verifier skill + a `REVIEW.md` pointer to it. The markdown guard (v4.8.0) is
still the in-ritual default; this adds the deterministic, CI-able version.

1. **Re-sync `REVIEW.md`** (verbatim where different): step 6 now points to the `memory-lint` skill
   as the recommended deterministic version of the verify ("let the script count"). The pointer is
   guarded with "if present," so it's a no-op where the skill isn't installed. `AGENTS.md` /
   `SKILLS.md` / `DECAY.md` unchanged.
2. **The skill itself is in the tool's `agent-skills/memory-lint/`** (neutral `SKILL.md` +
   `scripts/memory-lint.py`). It is **not** auto-installed into targets by this rung — a target that
   wants it can adopt/copy the skill (it's portable, Python 3 stdlib, optional). Auto-install into
   targets is a deliberate future option (it would add a script to every enabled repo).
3. **No skill regeneration; no `.gitignore` change.**
4. **Stamp** `.agent/version.md` → `version: 4.9.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
5. **Report**: `REVIEW.md` re-synced (points to `memory-lint`); the verifier skill is available.

---

## Rung: 4.9.0 → 4.10.0 — fresh-context second opinion + install the built-in skills (MINOR)

Additive: installs the built-in skills into the repo + a gitignored scratch dir. Folds the
"AIF" brainstorming idea into the skills layer + VBDI (`docs/DESIGN-fresh-context-review.md`) —
net-new is the security advisory on export, the handoff ritual, and the critique shape;
everything else reuses memory.

1. **Install the built-in skills** into the repo's `agent-skills/` — copy `second-opinion/`,
   `apply-critique/`, **and `memory-lint/`** (with its `scripts/`) verbatim from this tool's
   root, then regenerate adapters (Step 5h recipe). `memory-lint` is installed here too: v4.9.0
   left it tool-local, but the **review ritual relies on it**, so the 4.10.0 upgrade brings it
   into the target. Idempotent — overwrite these built-ins (they are ours); never touch
   unrelated `agent-skills/` content (`never-pick-a-winner`). **Tool-managed copies:** because
   upgrade overwrites them, the user must **not** customize an installed built-in — fork under a
   **new skill name** for a variant. The overwrite is scoped to these three, so
   `upgrades-additive` holds for all other `agent-skills/`. **Before overwriting an already-installed
   built-in, apply `ENABLE.md` §5i's modified-built-in check** — if the target's copy was locally
   changed, warn the human and let them decide rather than silently clobbering it.
2. **`review-scratch/`** — add to the repo `.gitignore` (personal, per-machine
   snapshots/critiques; never committed). `second-opinion` writes a `review-scratch/README.md`
   marking the folder personal on first run.
3. **Re-sync `.agent/schema.md`** (verbatim where different): adds the `review-scratch/`
   section. `templates/.gitignore` gains the `review-scratch/` entry. `AGENTS.md` / `SKILLS.md`
   / `DECAY.md` / `REVIEW.md` unchanged — the critique→repair loop reuses the existing ritual.
4. **Stamp** `.agent/version.md` → `version: 4.10.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
5. **Report**: built-in skills installed (`second-opinion` + `apply-critique` + `memory-lint`)
   with adapters regenerated; `review-scratch/` gitignored.

---

## Rung: 4.10.0 → 4.10.1 — `memory-lint` line-anchor bug fix (PATCH)

Script-only fix to a built-in skill. No memory-file shape change, no description change, so
adapters are untouched. Only matters for a repo that has `memory-lint` installed (v4.10.0+, or
adopted earlier).

1. **Re-copy `agent-skills/memory-lint/scripts/memory-lint.py`** verbatim from this tool's root,
   overwriting the installed copy (it is a tool-managed built-in — `upgrades-additive` holds; the
   overwrite is scoped to this tool-owned file). The fix: `memref_ids()` anchors the heading to a
   real line (`(?m)^## +Memory References[ \t]*$`) and bounds at the next line-anchored heading,
   so a session log that quotes the heading in prose no longer yields a false `over-archived`
   error. `SKILL.md` unchanged → **no adapter regeneration**.
2. **Ignore Python bytecode caches** — append `__pycache__/` + `*.py[cod]` to the repo's
   `.gitignore` (create-or-append, add-only, idempotent — same mechanism as the v3.1.0 propagation).
   `memory-lint` generates these on run; the `.py` source stays tracked.
3. **Nothing else changes** — `AGENTS.md` / `SKILLS.md` / `DECAY.md` / `REVIEW.md` / `.agent/schema.md`
   untouched. If `memory-lint` isn't installed, step 1 is a no-op (step 2's cache rule is harmless either way).
4. **Stamp** `.agent/version.md` → `version: 4.10.1`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
5. **Report**: `memory-lint` updated (false-positive on inline heading mentions fixed); Python-cache
   `.gitignore` rule added.

---

## Rung: 4.10.1 → 4.10.2 — fresh-context-review critique fixes (PATCH)

Refinements from a fresh-context review of the v4.10.x line (a clean-vendor reviewer). Two
built-in skills get re-copied and the install protocol gains a safety check. Only matters for a
repo that has the built-ins installed (v4.10.0+).

1. **Re-copy two built-ins** verbatim from this tool's root, overwriting the installed copies
   (tool-managed built-ins — `upgrades-additive` holds; overwrite scoped to tool-owned files):
   - `agent-skills/memory-lint/scripts/memory-lint.py` — `FOOTER_RE` is now bound to a single line
     (`[^\n]`, no `re.S`), so an *unclosed* footer can no longer let the field capture swallow the
     rest of the file up to a stray `-->` and silently misparse decay metadata. Same theme as
     v4.10.1: the verifier must not be fooled by malformed input.
   - `agent-skills/second-opinion/SKILL.md` — adds a "same-vendor vs. different-vendor" caveat under
     *Notes* (a same-vendor clean session tests the *mechanism*; a different vendor adds *epistemic
     diversity* for high-stakes milestones). **Body only — description unchanged → no adapter
     regeneration.**
2. **Warn-before-overwrite check** — `ENABLE.md` §5i (and this rung's step 1, and the 4.10.0 rung)
   now say: before overwriting an *already-installed* built-in, diff it against the source; if it was
   locally modified, **warn the human and let them decide** rather than silently clobbering. Makes
   the tool-managed-copies contract checked, not convention-only. Agent-run at the human's direction
   (`no-build-step-agent-run`); no-op on a fresh enable. **Apply that check before step 1's re-copy.**
3. **Nothing else changes** — `AGENTS.md` / `SKILLS.md` / `DECAY.md` / `REVIEW.md` / `.agent/schema.md`
   untouched. `apply-critique` and `memory-lint`'s `SKILL.md` are unchanged. If the built-ins aren't
   installed, steps 1–2 are no-ops.
4. **Stamp** `.agent/version.md` → `version: 4.10.2`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
5. **Report**: `memory-lint` hardened (unclosed-footer guard); `second-opinion` caveat added; install
   now warns before overwriting a locally-modified built-in.

## Rung: 4.10.2 → 4.10.3 — lightweight-mode wording fix (PATCH)

Wording-only clarification to the `AGENTS.md` lightweight-mode note. No file shape, no skill, no
script changes — only the installed `AGENTS.md` text.

1. **Re-key the lightweight-mode test to a *tracked* change.** In the target's installed `AGENTS.md`
   ("After Every Session" → lightweight-mode block), the objective test is now the **git diff over
   tracked files**, not "did any file change":
   - the opening line reads "whether a *tracked* file changed (the *objective* test is the git diff,
     not any filesystem write)";
   - the **Read-only** tier now also covers "a run whose only writes are gitignored, regenerated
     artifacts" — naming `sync skill adapters`, `review-scratch/` snapshots, and the compiled lint
     artifact — as **no session log**;
   - the second tier reads "**A tracked file changed** but produced no memory-relevant event";
   - the closing line reads "anything that touched a *tracked* file."
   This aligns the note with what `SKILLS.md` already states — `sync skill adapters` "touches no
   committed file… not a version change" — so an adapter sync (or any gitignored-only write) no
   longer implies a spurious lite log. **If the target's `AGENTS.md` was locally modified, warn the
   human and let them decide** (same warn-before-overwrite courtesy as the built-ins).
2. **Nothing else changes** — `SKILLS.md` / `DECAY.md` / `REVIEW.md` / `.agent/schema.md` / templates'
   memory files / skills / scripts untouched.
3. **Stamp** `.agent/version.md` → `version: 4.10.3`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: lightweight-mode test re-keyed to tracked changes (git diff); gitignored regenerated
   artifacts (adapter sync, `review-scratch/`, lint artifact) are explicitly no-log.

## Rung: 4.10.3 → 4.10.4 — memory-lint nested list fix (PATCH)

Updates the bundled `memory-lint` script to correctly parse deeply-nested lists in continuity.md Open Threads. No memory-file shape or procedural changes.

1. **Re-copy the `memory-lint` script.** Overwrite the target's `agent-skills/memory-lint/scripts/memory-lint.py` and its new test file with the ones from the tool's `agent-skills/memory-lint/scripts/` directory. **If the target's script was locally modified, WARN the human first** ("The built-in memory-lint skill has been updated in v4.10.4, but you have local modifications...") and ask before overwriting (this enforces the built-in exception to the `upgrades-additive` invariant).
2. **Re-copy the memory-lint `SKILL.md`.** It now contains a note about running the test harness. Same warn-before-overwrite rule applies.
3. **Stamp** `.agent/version.md` → `version: 4.10.4`, `last_upgraded: <today>`, preserving `enabled_with` and `mode`.
4. **Report**: `memory-lint` hardened to correctly preserve the pinned state of Open Threads containing deeply-nested sub-items.

## Rung: 4.10.4 → 4.11.0 — memory-lint Node runtime (MINOR)

Adds a Node implementation of the `memory-lint` verifier alongside the Python one, so a target machine that has Node but not Python still gets the deterministic check. Additive only — no memory-file shape or procedural changes; the Python script and command are unchanged.

1. **Copy the two new `memory-lint` files** into the target's `agent-skills/memory-lint/scripts/`: `memory-lint.mjs` (the Node verifier) and `test_memory_lint.mjs` (its tests). These are net-new; nothing is overwritten. (If a target somehow already has local copies, the built-in **warn-before-overwrite** rule from 4.10.2 applies.)
2. **Re-copy the memory-lint `SKILL.md`.** It now documents both runtimes as interchangeable and the cross-runtime test command. Same warn-before-overwrite rule applies.
3. **Verify parity (optional but recommended):** if both runtimes are present, `python3 …/memory-lint.py` and `node …/memory-lint.mjs` should produce identical output; `node --test …/test_memory_lint.mjs` should pass.
4. **Stamp** `.agent/version.md` → `version: 4.11.0`, `last_upgraded: <today>`, preserving `enabled_with` and `mode`.
5. **Report**: `memory-lint` now runs under Node as well as Python — deterministic decay checks no longer require a Python install.

## Rung: 4.11.0 → 4.11.1 — review step-6 archival guard hardened (PATCH)

Fixes a wording bug in the review ritual's archival-verify (step 6): a raw full-text grep of recent sessions counted prose mentions (e.g. a prior review summary naming a fact while deferring it) as "uses," creating an archival livelock. No memory-file shape change; the verifier script is unchanged (it was already correct).

1. **Re-copy `REVIEW.md`** to the target's repo root. Step 6 now defines a "use" as a `## Memory References` entry, makes `memory-lint` the preferred check, and scopes the by-hand fallback to in-block hits.
2. **Re-copy the memory-lint test files** into `agent-skills/memory-lint/scripts/`: `test_memory_lint.py` and `test_memory_lint.mjs` now include `memref_ids` regression tests (prose/review-summary mention is not counted; block bounded at next heading). `memory-lint.py`/`.mjs` themselves are unchanged. Warn-before-overwrite rule (4.10.2) applies if locally modified.
3. **Stamp** `.agent/version.md` → `version: 4.11.1`, `last_upgraded: <today>`, preserving `enabled_with` and `mode`.
4. **Report**: review step-6 archival guard no longer livelocks on prose mentions; a "use" is a Memory-References entry, counted deterministically by `memory-lint`.

## Rung: 4.11.1 → 4.12.0 — enforce `sync skill adapters` at enable + upgrade (MINOR)

Behavior change (additive, backward-compatible): the standing skills-adapter step stops being a
read-only "recommend, don't run" check and instead **runs** `sync skill adapters`. Closes the loose
end where, after an upgrade, a skill's vendor-native adapters could be missing — a skill that predates
a new adapter target (e.g. Kiro, added in 4.5.0), or any fresh clone/pull (adapters are gitignored and
don't travel) — so subsequent work that relies on native skill auto-trigger was blocked until the user
manually ran sync. No memory-file shape change; safe because the sync is idempotent and writes only
gitignored files.

1. **Re-sync the generic docs** (copy verbatim where different): `SKILLS.md` (its "Lightweight by
   design" note now says enable + every Mode B re-enable *run* the idempotent sync, not a read-only
   recommend; the `sync skill adapters` operation notes it's auto-run then). `AGENTS.md` / `DECAY.md`
   / `REVIEW.md` are unchanged (the per-session path still never touches skills, and `AGENTS.md`
   already only points to `SKILLS.md`).
2. **Run `sync skill adapters`** now as the closing skills step (this is the new enforced behavior,
   applied to this very upgrade): for each `agent-skills/<name>/`, (re)write the four vendor adapters
   and prune orphaned generated adapters. Idempotent; writes only gitignored files (no committed
   change, no session log). If the target has no skills, it's a no-op.
3. **Stamp** `.agent/version.md` → `version: 4.12.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: enable/upgrade now materialize skill adapters automatically; *"synced N skill(s) → M
   adapters (gitignored — do not commit; only `agent-skills/` is shared); pruned K orphan(s)."*

## Rung: 4.12.0 → 4.12.1 — `memory-lint` dangling-link cross-file fix (PATCH)

Script fix to a built-in: `check_dangling` resolved supersession links against `continuity.md` +
archive footers only, so a fact superseded by a target whose footer lives in another `memory/*.md`
(notably `vision.md`) false-flagged as `[dangling] … which has no footer anywhere`. Only matters for a
repo that has `memory-lint` installed (v4.10.0+).

1. **Re-copy the `memory-lint` scripts** verbatim from this tool's root, overwriting the installed
   copies (tool-managed built-ins; `upgrades-additive` holds — overwrite scoped to tool-owned files):
   `agent-skills/memory-lint/scripts/memory-lint.py` and `memory-lint.mjs`. The fix: `load_repo` now
   pools footers from other `memory/*.md` files (excluding `continuity.md`/`decay-policy.md`) into an
   `extra` set used **only** for supersession-link resolution in `check_dangling` — never counted as
   continuity/archive facts. `.mjs` additionally **exports** `load_repo` + `check_dangling` (additive,
   test-enabling; the `.py` already exposed them). **If the target's scripts were locally modified,
   WARN the human first** (the 4.10.2 warn-before-overwrite rule) and let them decide.
2. **Re-copy the test files** into `agent-skills/memory-lint/scripts/`: `test_memory_lint.py` and
   `test_memory_lint.mjs` now include a cross-file dangling regression test (a fact superseded by a
   `vision.md` fact must not warn; a genuinely missing target still warns). Same warn-before-overwrite
   rule. `SKILL.md` unchanged → **no adapter regeneration**.
3. **Stamp** `.agent/version.md` → `version: 4.12.1`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: `memory-lint` no longer false-flags a supersession target whose footer lives in
   `vision.md` (or another `memory/*.md`); both runtimes at parity; both suites 8/8.

## Rung: 4.12.1 → 4.13.0 — tool-provided (system) skills: marker + upstream advisory (MINOR)

Additive: marks the shipped built-ins as tool-provided so a target's AI recognizes a *system* skill at
edit time and routes a change correctly (fork a variant, or upstream a genuine fix), instead of silently
editing it and having the change overwritten on the next upgrade. No memory-file shape change; adapters
are untouched (they mirror only `name` + `description`).

1. **Re-copy the three built-ins' `SKILL.md`** verbatim from this tool's root, overwriting the installed
   copies (tool-managed built-ins — `upgrades-additive` holds; overwrite scoped to tool-owned files):
   `agent-skills/{memory-lint,second-opinion,apply-critique}/SKILL.md`. The expected delta is the new
   **`provenance: agent-memory-builtin`** frontmatter field + a one-line body banner. **Warn-before-overwrite
   (4.10.2) applies:** if a target's `SKILL.md` differs *beyond* this marker addition (a local
   modification), stop, show the diff, and — because such a change is often a genuine fix — **advise
   upstreaming it to the agent-memory project** (issue in production; maintainer pre-release) in addition
   to the keep/take choice. Scripts/tests are unchanged in this rung → no re-copy needed there.
2. **Re-sync the generic docs** (copy verbatim where different): `SKILLS.md` (new "Tool-provided (system)
   skills" section — the marker + the fork-or-upstream edit-time advisory), `AGENTS.md` (root + template:
   the one-line pointer), `.agent/schema.md` (the optional `provenance` field). `DECAY.md` / `REVIEW.md`
   unchanged.
3. **No adapter regeneration** — `name`/`description` are unchanged, so existing adapters still point
   correctly (adapters never carried `provenance`).
4. **Stamp** `.agent/version.md` → `version: 4.13.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
5. **Report**: built-ins now marked `provenance: agent-memory-builtin`; editing a system skill prompts
   fork-or-upstream; the upgrade warn-before-overwrite also advises upstreaming.

## Rung: 4.13.0 → 4.14.0 — optional Architecture Decision Record log (MINOR)

Additive and **documentation-only**: introduces an **optional** human-facing `docs/ADR.md`
decision log at the VBDI **Design** altitude. No memory-file shape change; adapters, scripts,
`DECAY.md`/`REVIEW.md` rules, and the per-session read path are untouched. **Nothing is
auto-created in the target** — a team adopts an ADR log only if it wants one.

1. **Re-sync the generic docs** (copy verbatim where different): `.agent/schema.md` (new
   optional `docs/ADR.md` section), `AGENTS.md` (root + template: the one-line "Design altitude
   may keep an optional `docs/ADR.md`, read on demand, not per-session" note), `DECAY.md` §12
   (the *Design* primitive now names the optional ADR log + its supersede/deprecate-never-delete
   lifecycle). `REVIEW.md` unchanged.
2. **Do not create `docs/ADR.md`** in the target. If the team wants one, they author it by hand
   following `.agent/schema.md` — seeding it (optionally) from their `## Architectural Invariants`,
   cross-linking `formalizes:` on the ADR ↔ a visible `(ADR-NNNN)` tag in the invariant title (a
   human pointer, not an agent read-cue). This repo's own `docs/ADR.md` is the worked reference.
3. **Stamp** `.agent/version.md` → `version: 4.14.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: an optional `docs/ADR.md` Architecture Decision Record log is now documented
   (Design-altitude, human-facing, on-demand — not in the per-session read path); no file was
   created; adopt on demand.

## Rung: 4.14.0 → 4.14.1 — clarify the re-synced `AGENTS.md` source (+ corrective verify) (PATCH)

Operator-protocol fix (`UPGRADE.md` is tool-operator-only — **no** target memory-file shape change).
Surfaced by a cross-vendor dogfood: a v3.7.0 → v4.14.0 upgrade (GitHub Copilot, `mercury-composable`)
re-synced the target's `AGENTS.md` from the tool's **root** `AGENTS.md` (the operator/dual-mode
dispatcher) instead of `templates/AGENTS.md`, leaving the target presenting itself as an enablement
tool and referencing the non-installed `ENABLE.md`. Root cause: the rungs' "(root + template)" notation
+ the standing "copy verbatim from the tool root / templates" guidance never said, per file, which
source a *target* gets. Fixed by the new **"Source of truth for re-synced files"** section above.

1. **Verify the target's `AGENTS.md` is the target hub, not the operator dispatcher.** If it contains
   `AI-Enable Another Repository` or references `ENABLE.md`/`MIGRATE.md`/`UPGRADE.md`, it was
   mis-synced from the tool's root — **re-copy it from `templates/AGENTS.md`** (current content).
   Otherwise leave it unchanged. (This repairs any target an earlier AI-run upgrade got wrong.)
2. **No other file changes** — `DECAY.md`/`REVIEW.md`/`SKILLS.md`/`.agent/schema.md`/built-ins are
   unaffected by this rung.
3. **Stamp** `.agent/version.md` → `version: 4.14.1`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: confirmed (or repaired) the target's `AGENTS.md` source; re-stamped to 4.14.1.

## Rung: 4.14.1 → 4.15.0 — ADR log upkeep trigger (MINOR)

Additive and **documentation-only** (same shape as 4.13.0 → 4.14.0): teaches the protocol to
**maintain** an existing `docs/ADR.md`, closing the 4.14.0 gap where the log could be adopted but
nothing cued it to evolve. No memory-file shape change; adapters, scripts, `REVIEW.md`, and the
per-session read path are untouched. **Nothing is created in the target** — a target with no ADR
log only receives the updated generic guidance.

1. **Re-sync the generic docs** (copy verbatim where different — see "Source of truth for
   re-synced files"): `AGENTS.md` (from `templates/AGENTS.md` — the new "If the log exists, keep it
   alive" maintenance/supersession trigger), `.agent/schema.md` (from `templates/.agent/schema.md`
   — the new "When to maintain it" paragraph in the `docs/ADR.md` section), and `DECAY.md` §12 (the
   *Design* primitive now notes the ADR lifecycle is kept in sync with fact supersession).
   `REVIEW.md` / `SKILLS.md` / built-ins unchanged.
   - **If the target's `AGENTS.md` ADR note is repo-customized** (e.g. it records an *adopted* ADR
     log at a non-default path), **merge** the maintenance sentence into that paragraph instead of
     overwriting — preserve the repo-specific adoption text + path. (Likewise for `.agent/schema.md`
     if a target localized it.)
2. **Do not create `docs/ADR.md`.** A target without one is unaffected beyond the guidance update;
   a target with one now has the maintenance trigger documented and is expected to keep it in sync.
3. **Stamp** `.agent/version.md` → `version: 4.15.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: the optional ADR log now carries a documented upkeep trigger (human-gated — a new
   durable decision or `(ADR-NNNN)`-tagged-fact supersession → propose a ledger update); no file
   created; re-stamped to 4.15.0.

## Rung: 4.15.0 → 4.16.0 — ADR default path aligned to industry convention (MINOR)

**Normative path change only.** The default Architecture Decision Record log path moves from
`docs/ADR.md` to `docs/arch-decisions/ADR.md`, matching the wider industry convention of placing
the ledger in a named subdirectory (purpose-signalling; leaves `docs/` root uncluttered).
No memory-file shape change; the ADR log remains optional, not auto-installed, and on-demand.

1. **Re-sync the generic docs** (copy verbatim where different — see "Source of truth for
   re-synced files"): `AGENTS.md` (from `templates/AGENTS.md` — path updated to
   `docs/arch-decisions/ADR.md`), `.agent/schema.md` (from `templates/.agent/schema.md` —
   section header + one body reference updated). `DECAY.md` §12 reference updated.
   - **If the target's `AGENTS.md` ADR note is repo-customized** (e.g. it already records
     `docs/arch-decisions/ADR.md`), **merge** only the path tokens — do not overwrite surrounding
     repo-specific text. Likewise for `.agent/schema.md` if localized.
2. **Rename the ADR file if it exists at the old path.**
   - If `docs/ADR.md` exists, move it to `docs/arch-decisions/ADR.md` (create the subdirectory;
     preserve all content). Update any `formalizes:` ↔ `(ADR-NNNN)` cross-links that referenced
     `docs/ADR.md` by path in prose (rare — most cross-links are id-based).
   - If `docs/arch-decisions/ADR.md` already exists (target adopted the new path ahead of this
     rung, e.g. `mercury-composable`), **no file move needed**.
   - If no ADR file exists, nothing to move.
3. **Stamp** `.agent/version.md` → `version: 4.16.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: ADR default path updated to `docs/arch-decisions/ADR.md`; file moved (or already
   at new path / not present); re-stamped to 4.16.0.

## Rung: 4.16.0 → 4.16.1 — Session filename drift fix (PATCH)

Wording-only changes to generic docs + linter improvement; no memory-file shape change.

1. **Re-sync the generic docs** (copy verbatim where different): `templates/AGENTS.md` (step 1
   and checklist now say "always run `date -u +%Y-%m-%d-%H%M%S`" and warn against using
   `currentDate` directly), `templates/.agent/schema.md` (same prohibition in the
   session-naming paragraph). `DECAY.md` / `REVIEW.md` / `SKILLS.md` / built-ins unchanged.
2. **Update the built-in `memory-lint` skill** (`agent-skills/memory-lint/scripts/`): sync
   `memory-lint.py` + `memory-lint.mjs` (new `check_session_filenames` warning) and their
   test files — see "Source of truth for re-synced files". If a target has forked a local
   variant, apply the same check to the fork rather than overwriting.
3. **Stamp** `.agent/version.md` → `version: 4.16.1`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
4. **Report**: session filename convention tightened; `memory-lint` will now warn on
   date-only session filenames; re-stamped to 4.16.1.

## Rung: 4.16.1 → 4.17.0 — GitHub Copilot CLI skills adapter (MINOR)

Additive: a **5th** adapter target plus Copilot skills in the Mode C detection table. No skill data
changes; a repo with no skills (or no Copilot) works exactly as before. Mirrors the 4.4.0 → 4.5.0
Kiro rung. Design: `docs/DESIGN-skills-layer.md`.

1. **Re-sync the installed docs** (copy verbatim where different — see "Source of truth for
   re-synced files"): `SKILLS.md` (the adapter recipe now lists a **GitHub Copilot CLI** target —
   `.github/skills/<name>/SKILL.md`, same shape as the Claude/Kiro adapter, since Copilot CLI
   follows the open Agent Skills standard; description-matched + `/<name>`), `AGENTS.md` (from
   `templates/AGENTS.md` — the adapter list now includes `.github/skills/`), and `.agent/schema.md`
   (from `templates/.agent/schema.md` — the adapter list). `DECAY.md` / `REVIEW.md` unchanged.
   (`MIGRATE.md`'s Copilot skill-promotion update is **operator-only** — `MIGRATE.md` is not
   installed into targets, so there is nothing to re-sync there.)
2. **`.gitignore` — add `.github/skills/` (path-scoped).** Unlike the other adapter dirs, `.github/`
   is **not** ignored wholesale (it holds the tracked `copilot-instructions.md` + `workflows/`), so
   add the single entry `.github/skills/` to the managed block (de-duplicate; add-only; same
   mechanism as the v3.1.0 propagation). If it's already present, no change.
3. **Re-sync `.github/copilot-instructions.md`** (from `templates/`) where the target's copy differs.
   The template now **front-loads the explicit `memory/` read list** (not just a pointer to
   `AGENTS.md`) and notes that **session upkeep is manual in Copilot** — because Copilot's **Ask/Plan**
   modes don't follow a pointer chain or auto-maintain the memory layer (a real-vendor finding). It
   also points Copilot at the skills layer. **If the target's copy was genuinely locally customized**
   (project-specific rules, not just an older default), **warn the human and let them decide** rather
   than overwriting.
4. **No skill regeneration in this rung directly.** The standing skills-adapter sync (above) now
   writes the `.github/skills/` adapter too — since v4.12.0 it **runs** `sync skill adapters` on
   every Mode B re-enable, materializing the Copilot adapter for every existing skill.
5. **Stamp** `.agent/version.md` → `version: 4.17.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
6. **Report**: docs re-synced; Copilot CLI adapter (`.github/skills/`) now in the recipe + gitignored
   path-scoped; skills-adapter sync result (the `.github/skills/` adapters are (re)written by the
   standing sync).

## Rung: 4.17.0 → 4.18.0 — `sync skill adapters` becomes a runnable script (MINOR)

Additive: installs the new **`sync-adapters`** built-in (the runnable script) and switches the standing
sync + the authoring convention to *run the script* rather than act out a prose recipe. No memory-file
shape change. Surfaced dogfooding `~/sandbox/simple-proxy`: Copilot CLI (Gemini) read `SKILLS.md` and
still couldn't *run* `sync skill adapters` — it was an agent operation with no executable, so the agent
hunted for an npm/MCP command and flailed. A real script removes the ambiguity (consistent with
`no-build-step-agent-run` — same category as the `memory-lint` script: an optional helper the
agent/vendor/CI invokes, never the tool).

1. **Install the `sync-adapters` built-in** — copy `agent-skills/sync-adapters/` (its `SKILL.md` +
   `scripts/sync-adapters.sh` + `.mjs` + `.py`) **verbatim from this tool's root** into the target's
   `agent-skills/`. It carries `provenance: agent-memory-builtin`; **apply the
   warn-before-overwrite check** (`ENABLE.md` §5i) if the target already has a modified copy.
2. **Re-sync `SKILLS.md`** (from the tool root — see "Source of truth"): the `sync skill adapters`
   operation **and** "Authoring a skill" now point to the runnable script; the adapter recipe stays as
   the format spec the script implements. `AGENTS.md` / `DECAY.md` / `REVIEW.md` are unchanged (the
   per-session path still never touches skills; `AGENTS.md`'s authoring 3-step already says "run
   `sync skill adapters`", which now resolves to the script).
3. **Run the script** as the closing skills step (the standing sync, now script-based):
   `bash agent-skills/sync-adapters/scripts/sync-adapters.sh` (or the `.mjs`/`.py`). Idempotent,
   gitignored-only — materializes all five adapters for every skill (incl. `sync-adapters`' own) and
   prunes the orphans it generated.
4. **Stamp** `.agent/version.md` → `version: 4.18.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`.
5. **Report**: `sync-adapters` built-in installed; `sync skill adapters` is now a runnable script;
   adapters re-synced via the script.

## Rung: 4.18.0 → 4.19.0 — vendor-neutral ritual triggers (MINOR)

Additive: installs the committed `.githooks/` + the CI workflow and **agent-activates** the local hook, so
the after-session ritual fires reliably for any vendor **without the agent self-triggering**. No
memory-file shape change. Surfaced from real client-team pain (ritual not followed through even with
Claude; a Copilot-only team had no triggers) + the maintainer's **zero-manual / untrained-user** adoption
constraint ("any manual operation is a barrier"). Design: `docs/DESIGN-ritual-triggers.md`.

1. **Install the triggers** (copy verbatim from this tool's root): **`.githooks/`** (the `post-commit`
   hook + its `README.md`) and **`.github/workflows/agent-memory.yml`** (the CI floor). Both are
   **tracked** (committed, they travel); **no `.gitignore` change** (only `.github/skills/` is ignored,
   path-scoped — `.github/workflows/` stays tracked). **Ensure `.githooks/post-commit` is executable**
   (`chmod +x`; committed mode `100755`) — git silently ignores a non-executable hook. Warn-before-overwrite
   if a target already has a customized `.github/workflows/agent-memory.yml`.
2. **Activate the local hook:** run `git config core.hooksPath .githooks` in the target — **the agent does
   this; never ask the user.** Idempotent; reversible (`git config --unset core.hooksPath`). CI needs no
   activation (a committed workflow runs server-side). *Honest limit:* git can't auto-run committed hooks
   on a fresh clone (security), so where no agent has run, **CI is the backstop**.
3. **Re-sync the generic docs** (copy verbatim where different — see "Source of truth"): `AGENTS.md` (from
   `templates/AGENTS.md` — the "reinforced, not just documented" note + definition-of-done framing).
   `docs/optional-ritual-hook.md` is **tool-only** (not installed into targets);
   `DECAY.md`/`REVIEW.md`/`SKILLS.md`/`.agent/schema.md` unchanged.
4. **Stamp** `.agent/version.md` → `version: 4.19.0`, `last_upgraded: <today>`, preserving `enabled_with`
   and `mode`.
5. **Report**: ritual triggers installed (`.githooks/` + CI) and the local hook activated; the
   after-session ritual now fires vendor-neutrally (advisory; CI is the zero-config floor).

## Rung: 4.19.0 → 4.20.0 — first-run init for fresh clones (MINOR)

Additive: closes the fresh-clone activation gap exposed dogfooding `~/sandbox/simple-proxy` with Copilot —
the memory bootstrap self-initializes, but a clone has the gitignored skill **adapters absent** and the
git hook **unactivated** (git can't auto-run committed hooks on clone). No memory-file shape change.

1. **Install `.githooks/init.sh`** (copy verbatim from this tool's root; **ensure executable** —
   `chmod +x`, committed mode `100755`). It's the one-command first-run init (regenerate adapters +
   activate the hook). It lives in `.githooks/` but is **not** a git hook name, so git never auto-runs it.
   (`.githooks/` itself is already installed by the 4.19.0 rung / Step 6.)
2. **Re-sync `AGENTS.md`** (from `templates/AGENTS.md`) — adds the **first-session self-init** note (run
   `bash .githooks/init.sh` if adapters are absent / `core.hooksPath` unset). Re-sync `.githooks/README.md`
   (now leads with the one-command init). `DECAY`/`REVIEW`/`SKILLS`/`.agent/schema.md` unchanged.
3. **Note:** ENABLE/UPGRADE already activate `core.hooksPath` directly (a deliberate enable is not a bare
   clone). `init.sh` + the self-init note are for **clones** (which never go through enable). For an
   in-place upgrade you may run `bash .githooks/init.sh` to confirm activation.
4. **Stamp** `.agent/version.md` → `version: 4.20.0`, `last_upgraded: <today>`, preserving `enabled_with`
   and `mode`.
5. **Report**: first-run init added (`.githooks/init.sh` + the AGENTS.md self-init note); fresh clones now
   self-initialize in one agent step (or one human command).

## Rung: 4.20.0 → 4.20.1 — self-init in `copilot-instructions.md` (PATCH)

Wording/placement fix to an installed file — no shape change. v4.20.0's self-init note (in `AGENTS.md`)
reached Claude Code but **not GitHub Copilot CLI**: a fresh-clone dogfood showed Copilot's `start` is
driven by `copilot-instructions.md`'s front-loaded read list, so it loaded memory + summarized without
acting on the AGENTS.md self-init (hook stayed inactive, adapters absent).

1. **Re-sync `.github/copilot-instructions.md`** (from `templates/.github/copilot-instructions.md`) — it
   now **leads** with a first-run-init block (*run `bash .githooks/init.sh` if `core.hooksPath` is unset /
   adapters absent, before summarizing*). **If a target's copy is locally customized, merge the block in**
   rather than overwriting. Nothing else changes.
2. **Stamp** `.agent/version.md` → `version: 4.20.1`, `last_upgraded: <today>`, preserving `enabled_with`
   and `mode`.
3. **Report**: `copilot-instructions.md` now carries the first-run self-init (Copilot acts before
   summarizing); the `bash .githooks/init.sh` fallback + CI floor are unchanged.

## Rung: 4.20.1 → 4.20.2 — Windows line-ending hardening (PATCH)

Additive: a `.gitattributes` that keeps the executable scripts + git hooks LF, so they run under bash on
Windows. No memory-file shape change. Surfaced from a Copilot Windows-feasibility check — the bootstrap
works via Git Bash, but with **no `.gitattributes`** a Windows clone (`core.autocrlf=true` by default)
rewrites `*.sh` + `.githooks/*` to CRLF and bash fails (`bad interpreter: /usr/bin/env bash^M`).

1. **Install / merge `.gitattributes`** (per ENABLE Step 7b): if the target has none, copy
   `templates/.gitattributes` verbatim; if it has one, **add only** the LF rules not already present
   (`*.sh text eol=lf`, `.githooks/* text eol=lf`) — de-duplicate; never remove/reorder existing entries.
   Then `git add --renormalize .` (a no-op if the files are already LF).
2. **Stamp** `.agent/version.md` → `version: 4.20.2`, `last_upgraded: <today>`, preserving `enabled_with`
   and `mode`.
3. **Report**: `.gitattributes` added/merged (LF for `*.sh` + `.githooks/*`); the bootstrap + hooks are now
   robust on Windows (Git Bash / WSL).

## Rung: 4.20.2 → 4.20.3 — memory-lint catches an empty/malformed version manifest (PATCH)

Skill-only: re-copy the updated `memory-lint` files. No memory-file shape change. Adds a deterministic
`check_version_manifest` ERROR so a present-but-empty/malformed `.agent/version.md` fails the lint floor
instead of silently breaking Mode B upgrade detection — closing the loop on the v4.20.1 bug (a truncating
stamp one-liner emptied a target's `version.md`, which made an agent misread the repo's version). A
*missing* `version.md` stays valid (the pre-versioning baseline) and is **not** flagged.

1. **Re-copy the `memory-lint` skill** from `agent-skills/memory-lint/` into the target (this is a
   tool-provided skill — overwrite in place, don't merge): `scripts/memory-lint.py`, `scripts/memory-lint.mjs`,
   `scripts/test_memory_lint.py`, `scripts/test_memory_lint.mjs`, and `SKILL.md`. Then re-sync skill
   adapters (`bash agent-skills/sync-adapters/scripts/sync-adapters.sh`, or any runtime at parity) so each
   vendor's regenerated copy picks up the change.
2. **Verify**: run `python3 .../memory-lint.py` (or the `.mjs`) at the target root — it should report
   `OK` (a correctly-stamped `version.md` passes). Optionally run the test suite.
3. **Stamp** `.agent/version.md` → `version: 4.20.3`, `last_upgraded: <today>`, preserving `enabled_with`
   and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a truncate-first
   one-liner** (the very bug this rung guards against).
4. **Report**: `check_version_manifest` added to memory-lint (both runtimes, at parity, with tests); an
   empty/malformed `.agent/version.md` now fails the lint, a missing one does not.

## Rung: 4.20.3 → 4.21.0 — Google Antigravity (`agy`) skills adapter (MINOR)

Skill-only: re-copy the updated `sync-adapters` files, add `.agents/` to `.gitignore`, then re-sync. No
memory-file shape change. Adds a **6th** vendor adapter target, `.agents/skills/<name>/SKILL.md` — the
open Agent Skills standard dir read by **Google Antigravity (`agy`)**, the Gemini CLI successor.
Antigravity reads `.agents/skills/`, **not** the old `.gemini/commands/*.toml`, so on an enabled repo
`init.sh` populated the Gemini adapter yet `agy` reported `/<command>` (e.g. `/memory-lint`) as **not
found**. The `.gemini/commands` TOML adapter **stays** (Gemini CLI keeps working through the transition).

1. **Re-copy the `sync-adapters` skill** from `agent-skills/sync-adapters/` into the target (tool-provided
   — overwrite in place, don't merge): `scripts/sync-adapters.sh`, `scripts/sync-adapters.mjs`,
   `scripts/sync-adapters.py`, and `SKILL.md`. (All three runtimes now write the `.agents/skills/`
   adapter and prune its orphans; they remain byte-for-byte equivalent.)
2. **Add `.agents/` to `.gitignore`** (after the `.github/skills/` line), add-only — it joins the other
   regenerated, local-only adapter dirs. Update the adapter-list comment (five → six) if you mirror it.
3. **Re-sync skill adapters** at the target root: `bash agent-skills/sync-adapters/scripts/sync-adapters.sh`
   (or any runtime at parity). Confirm `.agents/skills/<name>/SKILL.md` now exists for every skill.
4. **Verify**: in Antigravity, `/<name>` (e.g. `/memory-lint`) now resolves; reload/rescan if `agy`
   loads skills at startup. Run `memory-lint` — should report `OK`.
5. **Stamp** `.agent/version.md` → `version: 4.21.0`, `last_upgraded: <today>`, preserving `enabled_with`
   and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a truncate-first one-liner.**
6. **Report**: 6th adapter (`.agents/skills/`) added for Antigravity; `.agents/` gitignored; adapters
   re-synced; Gemini CLI (`.gemini/commands`) still served during the transition.

---

## Rung: 4.21.0 → 4.22.0 — discovery, consent & merge-friendliness (MINOR, four bundled features)

One release bundling four additive features (developed iteratively in one unreleased session,
dev-numbered 4.22–4.25; see "one version per release"). Mostly operator-side (`ENABLE.md`), plus the
`memory-lint` skill re-copy and one new installed root doc (`MERGE.md`). **No memory-file shape change.**

**(a) + (b) Curious discovery & fresh-enable advisory — operator-side `ENABLE.md`.** These change how
*future fresh enables* behave; an already-enabled repo has nothing structural to migrate, and the
curious harvest is a **fresh-enable event, not an upgrade behavior**. To backfill an already-enabled
repo from docs the older shallow scan skipped, use the **`harvest-knowledge` skill** (installed by the
`4.22.4 → 4.23.0` rung below) **on demand** — that is the home for "re-harvest." This rung does **not**
perform an inline re-harvest.

**(c) Merge-friendliness — installed docs + the linter:**
1. **Re-sync `.agent/schema.md`** (from `templates/.agent/schema.md`) — gains the
   `status`-is-not-a-changelog note + the **"Concurrency & merge-friendliness"** section (which points
   to `MERGE.md`). Ensure the target's `AGENTS.md` (from `templates/AGENTS.md`) carries the "keep
   `status` a short current-state line" bullet. Merge additively into a customized `AGENTS.md`.
2. **Re-copy the `memory-lint` skill** (tool-managed built-in — overwrite in place; warn first if
   locally modified, §5i): `scripts/memory-lint.py`, `.mjs`, the test files, `SKILL.md`. **Check 7**
   (leftover merge-conflict markers → ERROR) joins the lint floor.
3. **Slim a bloated `status`** (optional, recommended): if the target's `status` line has accreted a
   per-version changelog, rewrite it to a short current-state descriptor (history lives in session logs
   / changelog). **Read fully, then write** — never a truncate-first one-liner (`version-md-stamp-safe-write`).
   Leave append-only sections to the review ritual; don't hand-archive.

**(d) MERGE.md:**
4. **Install `MERGE.md`** at the target root — copy verbatim from this tool's root (generic, no
   placeholders; see the source-of-truth map). It joins `DECAY`/`REVIEW`/`SKILLS` as an on-demand
   protocol doc that runs *inside* the enabled repo. (No further `memory-lint` change — `MERGE.md`
   reuses check 7 as its validation gate.)

5. **Run `memory-lint`** at the target — must report `OK` (0 errors): no conflict markers, files parse.
6. **Stamp** `.agent/version.md` → `version: 4.22.0`, `last_upgraded: <today>`, preserving `enabled_with`
   and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a truncate-first one-liner.**
7. **Report**: discovery is curious + budgeted; fresh enable shows an advisory + standard-vs-deep depth
   choice; `status` is a short current-state line with documented merge conventions; `memory-lint` errors
   on leftover conflict markers; `MERGE.md` gives git conflicts a tiered, human-gated,
   `never-pick-a-winner` resolution protocol.

---

## Rung: 4.22.0 → 4.22.1 — post-commit auto-stub per session, not per commit (PATCH)

A one-file fix to the **installed** git hook. No memory-file shape change, no skill/template change.

1. **Re-copy `.githooks/post-commit`** from this tool's root into the target (verbatim; it's installed,
   like the rest of `.githooks/`). The auto-stub now suppresses a new stub when a session log exists within
   the **active-session window** (default 2h; `AGENT_MEMORY_SESSION_WINDOW_HOURS`), detected by the newest
   session **filename** (clone-safe), and nudges to enrich the existing log instead — so a multi-commit
   session yields **one** log, not one stub per commit. Ensure it stays executable (`chmod +x`; mode `100755`).
2. **Re-sync `.githooks/README.md`** (it documents the per-session window) and, if the target tracks it,
   `docs/DESIGN-ritual-triggers.md` (the granularity note). Both are verbatim copies from the tool root.
3. **(Optional) prune duplicate stubs** the old per-commit behavior may have left: if `memory/sessions/`
   has several near-identical auto-stubs from a single past session, the next **review** will sweep the
   reference-free ones normally — no manual action required; do **not** hand-delete session logs.
4. **Stamp** `.agent/version.md` → `version: 4.22.1`, `last_upgraded: <today>`, preserving `enabled_with`
   and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a truncate-first one-liner.**
5. **Report**: the post-commit hook now stubs at most once per working session (windowed); a recent log
   triggers an enrich-nudge instead of a duplicate stub.

---

## Rung: 4.22.1 → 4.22.2 — lightweight mode: one log per session, not per commit (PATCH)

Doc-only; the agent-side mirror of 4.22.1. No memory-file shape change, no skill/hook change.

1. **Re-sync `AGENTS.md`** from **`templates/AGENTS.md`** (source-of-truth map): the lightweight-mode "lite
   log" tier now says — if a session log already exists for *this* working session, a later
   **memory-neutral** commit **enriches** that log rather than spawning another lite one; **memory-relevant**
   work still gets its own full log. Merge additively into a repo-customized `AGENTS.md`.
2. **Stamp** `.agent/version.md` → `version: 4.22.2`, `last_upgraded: <today>`, preserving `enabled_with`
   and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a truncate-first one-liner.**
3. **Report**: lightweight mode coalesces a working session's trivial follow-on commits into one enriched
   log (keeps the decay session-count honest), symmetric with the v4.22.1 hook windowing.

---

## Rung: 4.22.2 → 4.22.3 — tighten the post-commit session window (2h → 30 min) (PATCH)

A one-file retune of the **installed** git hook. No memory-file shape change, no skill/template change.

1. **Re-copy `.githooks/post-commit`** from this tool's root (verbatim; keep it executable, mode `100755`).
   The active-session window default is now **30 min** (was 2h), and the override env var is
   **`AGENT_MEMORY_SESSION_WINDOW_MINUTES`** (integer minutes), replacing `AGENT_MEMORY_SESSION_WINDOW_HOURS`.
   If a target set the old hours var, switch it to the minutes var (× 60).
2. **Re-sync `.githooks/README.md`** and (if tracked) `docs/DESIGN-ritual-triggers.md` — both now state the
   30-min default + the minutes var. Verbatim copies from the tool root.
3. **Stamp** `.agent/version.md` → `version: 4.22.3`, `last_upgraded: <today>`, preserving `enabled_with`
   and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a truncate-first one-liner.**
4. **Report**: the post-commit session window is now 30 min (override via
   `AGENT_MEMORY_SESSION_WINDOW_MINUTES`); a new session after a >30-min pause still gets its own stub.

---

## Rung: 4.22.3 → 4.22.4 — safe-write safeguard in REVIEW.md (PATCH)

Doc-only; re-sync one installed protocol doc. No memory-file shape change, no skill/hook change.

1. **Re-sync `REVIEW.md`** from the tool root (verbatim — it's installed). Its **Safety** section now adds:
   never truncate a memory file when scripting the move (append-mode / read-into-var; never
   `open(f,"w").write(open(f).read()+…)`), and run `memory-lint` after any scripted memory mutation (it
   catches truncation; git-tracked files recover via `git checkout HEAD -- <file>`). Merge additively into
   a repo-customized `REVIEW.md`.
2. **Stamp** `.agent/version.md` → `version: 4.22.4`, `last_upgraded: <today>`, preserving `enabled_with`
   and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a truncate-first one-liner.**
3. **Report**: the review ritual now carries a shared safe-write safeguard against the archive-truncation
   antipattern.

---

## Rung: 4.22.4 → 4.23.0 — harvest-knowledge built-in skill (MINOR)

Adds a 5th tool-managed built-in skill. No memory-file shape change.

1. **Install `harvest-knowledge`** — copy `agent-skills/harvest-knowledge/SKILL.md` **verbatim from this
   tool's root** into the target's `agent-skills/harvest-knowledge/`. It's no-code (no bundled scripts).
   Marked `provenance: agent-memory-builtin` (tool-managed; overwrite on upgrade, never edit in place).
2. **Re-sync adapters** — run `sync skill adapters` (`bash agent-skills/sync-adapters/scripts/sync-adapters.sh`)
   so `harvest-knowledge` gets its six vendor adapters (gitignored). Confirm 6/6.
3. **No re-harvest is performed by the upgrade.** If the maintainer wants to backfill memory from docs the
   older shallow scan skipped, that is now the **`harvest-knowledge` skill, run on demand** — offer it, but
   it writes nothing unless invoked.
4. **Stamp** `.agent/version.md` → `version: 4.23.0`, `last_upgraded: <today>`, preserving `enabled_with`
   and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a truncate-first one-liner.**
5. **Report**: `harvest-knowledge` installed (5 built-ins); on-demand doc→memory harvest available; the
   enable-time harvest remains a fresh-enable event.

---

## Rung: 4.23.0 → 4.23.1 — last_harvest marker for incremental harvests (PATCH)

Doc/skill-only; additive. No memory-file *shape* change (the new Project State field is optional).

1. **Re-sync `.agent/schema.md`** (from `templates/.agent/schema.md`) — Project State now lists an optional
   `last_harvest:` field (sits with `last_review` / `last_invariant_check`). Merge additively.
2. **Re-copy the `harvest-knowledge` skill** (`agent-skills/harvest-knowledge/SKILL.md`, tool-managed) — it
   now reads `last_harvest` to scope the run and stamps it on completion. Skill **description unchanged**, so
   adapters need no regeneration (re-running sync is a harmless no-op).
3. **Do not add `last_harvest` by hand** — it appears the next time `harvest-knowledge` runs. (An existing
   repo simply has no marker until then; the first post-upgrade harvest is a full pass, as designed.)
4. **Stamp** `.agent/version.md` → `version: 4.23.1`, `last_upgraded: <today>`, preserving `enabled_with`
   and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a truncate-first one-liner.**
5. **Report**: harvests now scope incrementally via a `last_harvest` Project-State marker.

---

## Rung: 4.23.1 → 4.23.2 — context-hygiene guidance (keep state externalized) (PATCH)

Doc-only; additive. No memory-file shape change, no skill change.

1. **Re-sync `AGENTS.md`** (from `templates/AGENTS.md` — the memory hub, **never** the tool's root
   `AGENTS.md` dispatcher; see the 4.14.1 rung). It now carries a "Long session? Keep state externalized so
   compaction is safe" block: the objective health signal is **context-window utilization**, not time/"fog";
   the agent can't self-compact, so its lever is writing the session log + `continuity.md` at each natural
   seam **before** compaction (never mid-task), then re-verifying against live files afterward. Merge
   additively — keep any target-local `AGENTS.md` customizations.
2. **Stamp** `.agent/version.md` → `version: 4.23.2`, `last_upgraded: <today>`, preserving `enabled_with`
   and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a truncate-first one-liner.**
3. **Report**: `AGENTS.md` now teaches when to compact a long session (seam + after a memory write).

---

## Rung: 4.23.2 → 4.24.0 — decay-policy retune + review-cadence advisory (MINOR)

Additive. No memory-file shape change. The `memory-lint` check is advisory (never an ERROR), and the
policy retune is **merge-additive** — a repo that has tuned its own windows keeps them.

1. **Re-copy the memory-lint skill files** (tool-managed, byte-parity): `agent-skills/memory-lint/scripts/`
   `memory-lint.py`, `memory-lint.mjs`, `test_memory_lint.py`, `test_memory_lint.mjs`. They add advisory
   check (8): `[review-overdue]` + `[continuity-bloat]`. Skill **description unchanged** → adapters need no
   regeneration (re-running sync is a harmless no-op).
2. **Merge `memory/decay-policy.md` additively** (from `templates/memory/decay-policy.md`):
   - **Add** `continuity_max_facts: 30` under Review triggers if absent (the new primary lean signal).
   - If the repo still carries the **old defaults**, bump them: `continuity_max_lines: 300 → 600`,
     `verify_invariants_every: 20 → 40`. **If the repo has custom-tuned values, preserve them** — these
     are user knobs. (The `memory-lint` script defaults to 30 / 600 / 40 when a field is absent, so an
     un-retuned repo still gets sane thresholds.)
3. **Re-sync** `REVIEW.md` (size trigger now names `continuity_max_facts` + the lint advisories),
   `AGENTS.md` (root + template — review-cadence note), `.agent/schema.md` (windows list adds
   `continuity_max_facts`). Merge additively; keep target-local customizations.
4. **Run `memory-lint`** — expect it may now emit `[review-overdue]` / `[continuity-bloat]` advisories on a
   repo that's overdue (that's the point — they're informational, not errors). Address by running the
   `REVIEW.md` ritual when convenient.
5. **Stamp** `.agent/version.md` → `version: 4.24.0`, `last_upgraded: <today>`, preserving `enabled_with`
   and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a truncate-first one-liner.**
6. **Report**: `memory-lint` now surfaces overdue reviews + continuity bloat; defaults retuned
   (facts:30 / lines:600 / invariants:40).

---

## Rung: 4.24.0 → 4.25.0 — archive-fact built-in (safe archive-move) (MINOR)

Additive — a new built-in skill. No memory-file shape change.

1. **Copy the new built-in** `agent-skills/archive-fact/` **verbatim from this tool's root** into the
   target's `agent-skills/` (SKILL.md + `scripts/archive-fact.py`, `.mjs`, `test_archive_fact.py`, `.mjs`).
   It's tool-managed (`provenance: agent-memory-builtin`) — overwrite on upgrade; never customize in place.
2. **Re-sync skill adapters** (`bash agent-skills/sync-adapters/scripts/sync-adapters.sh`, or `.mjs`/`.py`) —
   materializes `archive-fact`'s six vendor adapters (gitignored). The target now has **six** built-ins.
3. **Re-sync `REVIEW.md`** (step 4 now leads with the `archive-fact` helper; manual append-mode stays the
   no-runtime fallback) and **`ENABLE.md`** (§5i installs six built-ins). Merge additively.
4. **Stamp** `.agent/version.md` → `version: 4.25.0`, `last_upgraded: <today>`, preserving `enabled_with`
   and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a truncate-first one-liner.**
   *(Fittingly, this rung ships the tool that makes that mistake structurally impossible.)*
5. **Report**: `archive-fact` installed — the review's archive-move is now deterministic + safe.

---

## Rung: 4.25.0 → 4.26.0 — refresh-metadata built-in + [stale-metadata] advisory (MINOR)

Additive — a new built-in skill + a new `memory-lint` advisory check. No memory-file shape change.

1. **Copy the new built-in** `agent-skills/refresh-metadata/` **verbatim from this tool's root** (SKILL.md +
   `scripts/refresh-metadata.py`, `.mjs`, `test_refresh_metadata.py`, `.mjs`). Tool-managed
   (`provenance: agent-memory-builtin`) — overwrite on upgrade; never customize in place.
2. **Re-copy the `memory-lint` skill files** (it gains check (9) `[stale-metadata]`): `memory-lint.py`,
   `.mjs`, `test_memory_lint.py`, `.mjs`. Byte-parity; description unchanged → adapters need no regen.
3. **Re-sync skill adapters** (`bash agent-skills/sync-adapters/scripts/sync-adapters.sh`) — materializes
   `refresh-metadata`'s adapters (gitignored). The target now has **seven** built-ins.
4. **Re-sync `REVIEW.md`** (steps 2–3 now lead with the `refresh-metadata` helper) and **`ENABLE.md`** (§5i
   installs seven built-ins). Merge additively.
5. **Stamp** `.agent/version.md` → `version: 4.26.0`, `last_upgraded: <today>`, preserving `enabled_with`
   and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a truncate-first one-liner.**
6. **Run `memory-lint`** — it may now emit `[stale-metadata]` advisories on facts whose tier drifted; clear
   them by running `refresh-metadata` (then `archive-fact` for any that come out past `archive_window`).
7. **Report**: review steps 2–3 are now deterministic (`refresh-metadata`); `[stale-metadata]` makes a
   skipped re-tier visible.

---

## Rung: 4.26.0 → 4.26.1 — pinned-thread tier not flagged/rewritten (PATCH)

Refinement; no shape change. Tool-managed skill files only.

1. **Re-copy the `memory-lint` skill files** (`memory-lint.py`, `.mjs`, `test_memory_lint.py`, `.mjs`) and the
   **`refresh-metadata` skill files** (`refresh-metadata.py`, `.mjs`, `test_refresh_metadata.py`, `.mjs`) —
   both `expected_tier`s now return a pinned `- [ ]` thread's stored tier (no flag, no rewrite). Skill
   descriptions unchanged → adapters need no regeneration.
2. **Re-sync `DECAY.md`** (rule 4 clarified — pinned-ness protects an open thread, not its tier label).
3. **Stamp** `.agent/version.md` → `version: 4.26.1`, `last_upgraded: <today>`, preserving `enabled_with`
   and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a truncate-first one-liner.**
4. **Run `memory-lint`** then **`refresh-metadata`** — pinned threads no longer appear as `[stale-metadata]`.
5. **Report**: a `working`-tagged pinned open thread is no longer treated as drift.

## Rung: 4.26.1 → 4.27.0 — standardized PR description (What / Why) (MINOR)

Additive convention + one new tracked bootstrap file. No memory-file shape change.

1. **Install `.github/pull_request_template.md`** into the target from
   `templates/.github/pull_request_template.md` (verbatim; tracked — it travels). Create
   `.github/` if absent. If the target already has a `pull_request_template.md`, **don't
   overwrite silently** — ask the user (overwrite / skip / merge the What/Why headings in).
2. **Re-sync `AGENTS.md`** from **`templates/AGENTS.md`** (the memory hub — *not* the tool root):
   it now carries the "Opening a pull request? → lead with What / Why" convention next to the
   commit-trailer note, plus the checklist line. Merge into a repo-customized `AGENTS.md` rather
   than overwrite.
3. **Stamp** `.agent/version.md` → `version: 4.27.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a
   truncate-first one-liner.**
4. **Report**: PRs opened in this repo now lead with **What** and **Why** (advisory; the template
   seeds it, the `AGENTS.md` convention is the vendor-neutral backstop).

## Rung: 4.27.0 → 4.28.0 — co-author convention cleanup (stable identity + one trailer) (MINOR)

Doc-only convention refinement. No memory-file shape change.

1. **Re-sync `AGENTS.md`** from **`templates/AGENTS.md`** (the memory hub — *not* the tool root):
   the commit-trailer note now specifies the **stable agent name** (e.g. `Claude Code`, `Gemini
   CLI`) — the actual AI collaborator, not a model-version string — and adds the squash-merge
   "collapse to a single `Co-Authored-By:`" guidance. Merge into a repo-customized `AGENTS.md`
   rather than overwrite.
2. **Re-copy `.github/pull_request_template.md`** from `templates/.github/pull_request_template.md`
   (the footer comment now names the AI collaborator's stable agent name, not a model version). If
   the target locally customized its template, merge the footer-comment change rather than clobber.
3. **Stamp** `.agent/version.md` → `version: 4.28.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a
   truncate-first one-liner.**
4. **Report**: the co-author trailer now uses a stable agent identity, and squash-merges collapse
   to one trailer.

---

## Rung: 4.28.0 → 4.28.1 — post-commit hook uncommitted-session-log guard (PATCH)

**What changed:** `.githooks/post-commit` auto-stub gained a primary guard — before the filename-timestamp window check, it inspects `git status --porcelain -- memory/sessions/` for any uncommitted `.md`. If one exists, the agent already has a log for this session; the hook emits the enrich-and-commit nudge and skips stubbing. The time-window check becomes the fallback for already-committed logs (e.g. a follow-on commit hours later). Fixes spurious near-duplicate stubs in the two-commit pattern and in long sessions.

**Steps:**

1. Re-copy `.githooks/post-commit` from this repo (or from your agent-memory upstream).
2. Stamp `.agent/version.md` → `version: 4.28.1`, `last_upgraded: <today>`, preserving all other fields.
3. Commit: `chore(memory): upgrade agent-memory → v4.28.1`.

---

## Rung: 4.28.1 → 4.28.2 — memory-lint continuity-bloat decay-eligible count (PATCH)

**What changed:** `memory-lint`'s `[continuity-bloat]` fact-count check now compares
`continuity_max_facts` against **decay-eligible** facts only — excluding `tier: core` invariants and
pinned `- [ ]` open threads, which can never be archived. Before, a repo carrying a healthy invariant
set + a few active workstreams tripped the cap **structurally** and stayed red even right after a
fully correct review (field report: `mercury-composable`, 41 footers / 14 core / 11 open threads →
chronic WARN). This aligns the code with `decay-policy.md`'s documented intent ("count of *decaying*
facts/threads"). Both runtimes at parity + mirror regression tests; warning text now reads
"decay-eligible facts". Tool-managed built-in skill; no memory-file shape change.

**Steps:**

1. **Re-copy the `memory-lint` skill files** (both runtimes) from this repo (or your agent-memory
   upstream): `agent-skills/memory-lint/scripts/memory-lint.py`, `.../memory-lint.mjs`, and the two
   mirror test files. Skill description unchanged → **adapters need no re-sync**.
2. **Stamp** `.agent/version.md` → `version: 4.28.2`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a
   truncate-first one-liner.**
3. **Run `memory-lint`** — a mature layer whose fact count was inflated only by core facts + pinned
   threads should now report clean (or a lower, decay-eligible count).
4. **Report**: `[continuity-bloat]` now counts only what a review can actually act on.

---

## Rung: 4.28.2 → 4.28.3 — memory-lint continuity-bloat line message decay-aware (PATCH)

**What changed:** the `continuity_max_lines` half of `[continuity-bloat]` now branches on whether a
review could actually reduce the file. `memory-lint` computes `archivable` = facts overdue for decay
(`sslu > archive_window`, excluding core/superseded/pinned) + superseded facts. When lines exceed the
cap **and** `archivable == 0`, the message stops prescribing "a review is due to lean it down" (which
a review can't satisfy, and which pressures archiving an *active* fact — REVIEW.md's costliest error)
and instead names the real lever: *"nothing is archivable yet; the excess is active/dense facts.
Condense shipped decisions, or raise `continuity_max_lines` in decay-policy.md if this repo is
legitimately large."* When something *is* archivable the original actionable message stands. Same
failure class as v4.28.2 (an unclearable warning erodes signal), on the line axis. From a second
`mercury-composable` field report (29-module reactor, 37 facts / 708 lines / 0 archivable). The
fact-count check is untouched; a dedicated non-archival "condense" lever was **deferred** until the
need recurs. Tool-managed built-in skill; no memory-file shape change.

**Steps:**

1. **Re-copy the `memory-lint` skill files** (both runtimes) from this repo (or your agent-memory
   upstream): `agent-skills/memory-lint/scripts/memory-lint.py`, `.../memory-lint.mjs`, and the two
   mirror test files. Skill description unchanged → **adapters need no re-sync**.
2. **Re-sync the `continuity_max_lines` comment** in `memory/decay-policy.md` additively (it now notes
   the cap is meant to be raised for a legitimately large/complex repo). Preserve any custom-tuned
   integer values — merge the comment, don't overwrite a raised cap.
3. **Stamp** `.agent/version.md` → `version: 4.28.3`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a
   truncate-first one-liner.**
4. **Run `memory-lint`** — a large repo over the line cap with nothing currently archivable should now
   show the "nothing is archivable yet" message rather than "a review is due to lean it down."
5. **Report**: the line-count bloat warning now tells the truth about what a review can do.

---

## Rung: 4.28.3 → 4.28.4 — Co-Authored-By dedup invariant (one per collaborator, keyed on email) (PATCH)

**What changed:** doc-only refinement of the v4.28.0 commit-attribution convention. The agent
**co-authors the commit message with its harness**, which often injects its own (model-version)
`Co-Authored-By`; the old guidance ("identify yourself … accept it if unavoidable") led a
conscientious agent to *append* a second stable-name trailer → two lines for one collaborator, which
squash-merges compounded. `AGENTS.md` now reframes the model (treat the harness's message as the base
and **reconcile**) and states the invariant: **at most one `Co-Authored-By` per collaborator, matched
on email** (`Claude Code` / `Claude Opus 4.8` / `Gemini CLI` are one collaborator at one address), with
a deterministic resolution tree and forge-aware squash guidance. No code, no memory-file shape change.

**Steps:**

1. **Re-sync `AGENTS.md`** from **`templates/AGENTS.md`** (the memory hub) — the commit-attribution
   block now carries the co-author-with-harness reframe, the dedup-by-email invariant, the 3-branch
   resolution tree, and the forge-aware squash note. Merge into a repo-customized `AGENTS.md` rather
   than overwrite.
2. **Re-copy `.github/pull_request_template.md`** from `templates/.github/pull_request_template.md`
   (its footer comment now states the one-trailer-per-collaborator-by-email rule). If the target
   customized its template, merge the footer-comment change rather than clobber.
3. **Stamp** `.agent/version.md` → `version: 4.28.4`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a
   truncate-first one-liner.**
4. **Report**: commit/PR co-author trailers now reconcile to one line per collaborator (keyed on
   email); the enforcement hook was deliberately deferred. Adapters need no re-sync (skills unchanged).

---

## Rung: 4.28.4 → 4.29.0 — before-session context presence: bootstrap `@`-imports + opt-in SessionStart recipe (MINOR)

**What changed:** closes the before-session half of the ritual-trigger asymmetry. v4.19.0 made the
*after*-session rituals fire vendor-neutrally (git hook + CI), but that substrate has no
session-start moment, so the "read `AGENTS.md` / `memory/*` first" instruction remained advisory
prose — prompt adherence, empirically skipped under task pressure (child-repo field report,
2026-07-11: skill-unawareness, off-model engagement, rework). Fix, in philosophy order: **(a)** the
`templates/CLAUDE.md` and `templates/GEMINI.md` bootstrap pointers now carry native **`@`-imports**
(`@AGENTS.md`, `@memory/instructions.md`, `@memory/continuity.md`, `@memory/vision.md` — Gemini CLI
uses the `@./path.md` form and imports `.md` files only) so the hub and core memory files are
**structurally present** in every Claude Code / Gemini CLI session — markdown-only, no hooks, the
same fix-shape as v4.20.1's copilot-instructions front-load. Imports live only in the per-vendor
bootstrap files; `AGENTS.md` stays vendor-neutral. **(b)** `docs/optional-ritual-hook.md`
(tool-only, not installed) gains an **opt-in** Claude Code `SessionStart` injection recipe for
teams that also want `memory/sessions/` recency injected — never installed by default (a committed
`.claude/settings.json` conflicts with the installed `.gitignore`, and risks leaking personal
allowlist entries into a shared file). Attestation canaries remain a downstream per-repo pattern,
not part of the tool. Honest limits: imports can't express dynamic paths (`memory/sessions/`
newest-N); Cursor/Windsurf/Copilot have no import mechanism and keep the prose pointer; the
imported files enter context every session, so the continuity-bloat controls
(v4.24.0/4.28.2/4.28.3) are now load-bearing, not cosmetic. Presence is guaranteed; *attendance*
remains agent judgment. No memory-file shape change; skills/adapters unchanged.

**Steps:**

1. **Re-sync the bootstrap pointers additively.** Only for bootstrap files that are *ours*
   (content check: they reference the agent-memory system / `memory/instructions.md`): merge the
   presence note plus that vendor's **literal import block from `ENABLE.md` Step 6** (in
   `templates/` the block appears as the `{{BOOTSTRAP_IMPORTS}}` placeholder since v4.29.1 —
   never copy the placeholder itself) into the target's `CLAUDE.md` / `GEMINI.md`,
   **preserving** the project name/one-liner and any repo-specific lines — merge, never
   overwrite. Skip a vendor's file the target doesn't have.
2. **Offer (don't install) the SessionStart recipe.** Point the user at
   `docs/optional-ritual-hook.md` → "Option A0" (tool-side doc); adopting it is a conscious
   per-user/per-repo choice.
3. **Stamp** `.agent/version.md` → `version: 4.29.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a
   truncate-first one-liner.**
4. **Verify:** in a fresh Claude Code session the memory files are present without an explicit
   read (the agent can state the current `last_session` / top open thread before opening any
   file); `memory-lint` clean.
5. **Report**: before-session context presence is now structural on import-capable runtimes and
   documented as an opt-in hook elsewhere; the after/before trigger asymmetry is closed at the
   presence level.

---

## Rung: 4.29.0 → 4.29.1 — template import blocks become a `{{BOOTSTRAP_IMPORTS}}` placeholder (PATCH)

**What changed:** tool-repo containment of an instruction bleed-through that v4.29.0 amplified —
**no installed file changes shape or content**, so this rung is a version-stamp for targets.
Cross-vendor dogfooding (a GitHub Copilot assessment, corroborated live on Claude Code) showed that
runtimes which auto-load **directory-scoped instruction files** picked up `templates/CLAUDE.md`
inside the tool repo — and because `@`-imports resolve *relative to the containing file*, its
v4.29.0 import block pulled the **placeholder template stubs** (`templates/AGENTS.md`,
`templates/memory/*` — `{{PROJECT_NAME}}`, "last_session: (none yet)", conflicting identity lines)
into live context as instructions. Fix: `templates/CLAUDE.md` + `templates/GEMINI.md` now carry a
`{{BOOTSTRAP_IMPORTS}}` placeholder instead of live import lines; `ENABLE.md` Step 6 defines the
per-vendor literal blocks and expands the placeholder at install, so **installed output is
byte-identical to v4.29.0's**. Honest residual: a runtime that auto-loads a nested `AGENTS.md`
directly may still surface `templates/AGENTS.md` itself — that behavior predates v4.29.0 and is the
runtime's, not the tool's; this patch removes the amplification (the memory-stub pull-in).

**Steps:**

1. **Nothing to re-sync in the target** — enabled repos have no `templates/` directory, and their
   installed `CLAUDE.md`/`GEMINI.md` import blocks are already the expanded (correct) form.
2. **Stamp** `.agent/version.md` → `version: 4.29.1`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a
   truncate-first one-liner.**
3. **Report**: operator-side containment only; target files unchanged.

---

## Rung: 4.29.1 → 4.30.0 — stack-aware `.gitignore` build-output seed (MINOR)

**What changed:** `ENABLE.md` gains a minimal, bounded build-output `.gitignore` seed — Step 7
appends the detected stack's canonical build-output entries under a second, separately-scoped
sentinel (`# === agent-memory: build output (stack-aware seed …) ===`), add-only and
de-duplicating; Step 5b seeds a greenfield Open Thread carrying the "seed when the stack lands"
action; Step 8/9 verify and report it. From a greenfield field case (`mercury`): the installed
`.gitignore` is deliberately AI-infrastructure-scoped, so a stack arriving *after* enable had no
build-output ignore and the first build polluted `git status`. Explicit non-goal: a minimal seed,
never a gitignore manager.

**Steps:**

1. **Optionally apply the seed to the target** (additive): if the target's `.gitignore` does not
   ignore its detected stack's build output, append the missing entries from the `ENABLE.md`
   Step 7 table under the build-output sentinel — **add-only, de-duplicated against the whole
   file; never remove or reorder existing entries**. If the entries already exist anywhere
   (the common case — e.g. the user added them by hand), add nothing.
2. **Greenfield targets** (no stack yet): if the target's `continuity.md` lacks a greenfield
   Open Thread carrying the "seed build-output ignores when the stack lands" action, offer to
   add one (additive; skip if the stack has since landed and the entries exist).
3. **Stamp** `.agent/version.md` → `version: 4.30.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a
   truncate-first one-liner.**
4. **Report**: operator-side protocol change; the only possible target edits are additive
   `.gitignore` entries and an optional Open Thread.

---

## Rung: 4.30.0 → 4.31.0 — GitLab forge support: forge-aware ritual floor + MR template (MINOR)

**What changed:** the ritual floor and description template are now **forge-aware**. A GitLab-hosted
field report showed GitLab ignores `.github/` entirely, so two installed artifacts were dead there:
the CI floor (`.github/workflows/agent-memory.yml`) — leaving fresh clones with **no** ritual
backstop, the exact gap v4.19.0 existed to close — and the What/Why PR template. `ENABLE.md` now
detects the hosting forge (Step 4) and installs a matched set (Step 6): on GitLab,
`.gitlab/agent-memory-ci.yml` (memory-lint + session-log check; advisory via
`allow_failure: exit_codes: [42]`; `AGENT_MEMORY_STRICT=1` gates) wired from the root
`.gitlab-ci.yml`, plus `.gitlab/merge_request_templates/Default.md`. `AGENTS.md` squash-merge
guidance is forge-aware (GitHub compounds trailers → dedup; GitLab drops them → make the trailer
survive: re-add at merge, or `%{all_commits}` in the project squash template — `%{co_authored_by}`
credits commit authors only, never body trailers). Local-tooling `.github/` files
(copilot-instructions, `.github/skills/` adapters) are forge-independent and stay put everywhere.
No memory-file shape change; skills/adapters unchanged.

**Steps:**

1. **Detect the target's forge**: `git remote get-url origin` (`github.com` → GitHub; `gitlab.com`
   or a self-managed GitLab host → GitLab; corroborate with `.gitlab-ci.yml` / `.gitlab/`).
   GitHub-hosted → skip to step 3. Unknown → treat as both (install the GitLab set too).
2. **GitLab-hosted: install the GitLab set.**
   - Copy `templates/.gitlab/agent-memory-ci.yml` → `.gitlab/agent-memory-ci.yml`.
   - Root wiring: target has **no `.gitlab-ci.yml`** → copy `templates/.gitlab-ci.yml` verbatim.
     Target **has one** → **add-only**: append the `include:` entry
     (`- local: '.gitlab/agent-memory-ci.yml'`) — skip if an entry for that path already exists
     (de-duplicate). **Stage check (mandatory):** the job uses the default `test` stage; if the
     file defines a custom `stages:` list without `test`, append `test` to it (add-only — omitting
     it invalidates the whole pipeline config and stops ALL the repo's CI). **Never add or edit
     `workflow:rules` in a pre-existing file** (it changes when the repo's own jobs run). The job
     then rides whatever pipelines the existing config creates — read the file and note the actual
     coverage in the report.
   - Copy `templates/.gitlab/merge_request_templates/Default.md` →
     `.gitlab/merge_request_templates/Default.md` (ask per-file if one already exists).
   - The now-inert `.github/workflows/agent-memory.yml` + `.github/pull_request_template.md` may
     be **left in place** (harmless; the default — upgrades are additive) or removed at the
     user's explicit direction — a user-directed cleanup *outside* the upgrade's own scope
     (upgrades themselves never delete; the files are tool-installed, not vendor originals). Keep
     `.github/copilot-instructions.md` regardless — local Copilot tooling reads it on any forge.
3. **Re-sync the forge-aware docs**: `AGENTS.md` from `templates/AGENTS.md` (squash-inversion
   guidance, PR/MR wording, forge-qualified CI-floor notes) — merge into a customized `AGENTS.md`,
   never overwrite; re-copy `.githooks/README.md` and `REVIEW.md` verbatim from the tool root.
4. **Stamp** `.agent/version.md` → `version: 4.31.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a
   truncate-first one-liner.**
5. **Verify:** GitLab targets — next pipeline shows the `agent-memory` job (advisory; orange on
   findings), a new MR auto-fills the What/Why template; `memory-lint` clean. Self-managed GitLab:
   confirm a runner is registered, or report the prerequisite to the user.
6. **Report**: the ritual floor + description template now match the hosting forge; on GitLab,
   state the actual pipeline coverage read from the root file's rules (fresh root file → branch +
   MR; add-only include → whatever pipelines the existing config creates).

---

## Rung: 4.31.0 → 4.32.0 — Azure DevOps forge support: own-pipeline ritual floor + PR template (MINOR)

**What changed:** the forge seam gains its third member, from a real field installation. Azure
DevOps differs from both shipped forges in one structural way — **activation is not file-driven**:
a pipeline is a *resource*, so a committed YAML is inert until a one-time
`az pipelines create --yml-path … --skip-first-run` binding (default permission: Contributors),
and Azure Repos ignores the YAML `pr:` key (PR-time validation is a Build Validation branch
policy — an admin settings change the tool never makes). The install is therefore the
**own-pipeline model**: `.azuredevops/agent-memory-ci.yml` is a complete pipeline (an existing
`azure-pipelines.yml` is never touched), advisory via `##vso[task.logissue type=warning]` +
`task.complete result=SucceededWithIssues` (native "partially succeeded"; `AGENT_MEMORY_STRICT=1`
fails the run), `fetchDepth: 0` for the diff-based check. Plus
`.azuredevops/pull_request_template.md` (auto-applies to new PRs; read from the default branch —
it takes effect once merged there; 4000-char description cap) and a third squash-guidance branch (ADO drops trailers, no template
mechanism — re-add via "Customize merge commit message"; the PR-description footer is the durable
record). No memory-file shape change; skills/adapters unchanged.

**Steps:**

1. **Detect the target's forge**: `git remote get-url origin` — `dev.azure.com` or
   `*.visualstudio.com` → Azure DevOps (corroborate with `azure-pipelines.yml` / `.azuredevops/`).
   Not Azure DevOps → skip to step 3.
2. **Azure-DevOps-hosted: install the set.** Copy `templates/.azuredevops/agent-memory-ci.yml` →
   `.azuredevops/agent-memory-ci.yml` and `templates/.azuredevops/pull_request_template.md` →
   `.azuredevops/pull_request_template.md` (ask per-file if one already exists). Do **not** touch
   any existing `azure-pipelines.yml`. **Report the one-time activation command** (run it only at
   the user's explicit direction, with their credentials):
   `az pipelines create --name agent-memory --repository <repo> --repository-type tfsgit --branch <default> --yml-path .azuredevops/agent-memory-ci.yml --skip-first-run`
   Run it **only after the install commit is pushed** (`--yml-path` binds to the server-side
   YAML). **Seed a `- [ ] (forge) Azure DevOps CI floor awaiting one-time activation: <command>`
   Open Thread** in the target's `continuity.md` so the pending state survives the session.
   Mention the optional Build Validation branch policy (admin; "Optional" = notify-only) and the
   Microsoft-hosted parallelism prerequisite (free grant via Microsoft's request form, or paid
   parallel jobs via a linked Azure subscription — or a self-hosted agent).
3. **Re-sync the forge-aware docs**: `AGENTS.md` from `templates/AGENTS.md` (third squash branch +
   forge-qualified CI-floor notes) — merge into a customized `AGENTS.md`, never overwrite;
   re-copy `.githooks/README.md`, `.githooks/init.sh`, and `REVIEW.md` verbatim from the tool root.
   Also re-copy the existing forge CI job file (`.github/workflows/agent-memory.yml` or
   `.gitlab/agent-memory-ci.yml`) — v4.32.0 hardens their base-ref fallback
   (`git rev-parse --verify --quiet`).
4. **Stamp** `.agent/version.md` → `version: 4.32.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a
   truncate-first one-liner.**
5. **Verify:** all targets — `memory-lint` clean; `.agent/version.md` reads 4.32.0. Azure DevOps
   targets additionally: after the user pushes and runs the activation command, the next push
   shows the `agent-memory` run (findings → "partially succeeded", orange); a new PR auto-fills
   the What/Why template; the `(forge)` Open Thread is checked off.
6. **Report**: the ritual floor + description template now cover GitHub, GitLab, and Azure DevOps;
   on Azure DevOps state plainly whether the pipeline has been activated or is awaiting the
   one-time command.

---

## Rung: 4.32.0 → 4.32.1 — Mode A `last_session` contradiction fix (PATCH)

**What changed:** a real Mode A enable (2026-08-06) plus an adversarial protocol audit caught
`ENABLE.md` disagreeing with itself: Step 5b still said a non-migrated enable leaves
`last_session: (none yet)`, while Step 5c (added later) mandates a **first enable session log**
for every fresh enable — so "(none yet)" was false the moment the enable completed, and it
blinded the multi-agent continuity check that reads the field. Step 5b now points
`last_session` at the 5c log (`<today> | agent: <your agent name> (<the 5c log's filename
stem>)`, filled when that log is written — the same moment its stem becomes the seeded facts'
`origin`); the template seed became a `{{LAST_SESSION}}` placeholder; the schema marks
`(none yet)` as legacy; the `rust-event-bus` example stays unedited (it truthfully predates
Step 5c) behind a header note. Enable-time behavior only — no memory-file shape change;
skills/adapters unchanged.

**Steps:**

1. **Re-copy** `.agent/schema.md` verbatim from `templates/.agent/schema.md` (the
   `last_session` line now marks `(none yet)` as legacy).
2. **Optional truth fix:** if the target's `continuity.md` still reads
   `last_session: (none yet)` but `memory/sessions/` is non-empty, point the field at the
   newest session file (`<date> | agent: <name> (<filename stem>)`). Only an
   enabled-but-never-worked repo legitimately still carries `(none yet)`; any real session
   overwrites it in the normal ritual anyway.
3. **Stamp** `.agent/version.md` → `version: 4.32.1`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a
   truncate-first one-liner.**
4. **Verify:** `memory-lint` clean; `.agent/version.md` reads 4.32.1; `last_session` in
   `memory/continuity.md` shows a real value, or a justified legacy `(none yet)` (empty
   `memory/sessions/`).

---

## Rung: 4.32.1 → 4.33.0 — session-log secret redaction: ritual rule + `[secret-material]` advisory (MINOR)

**What changed:** a client-side DLP scanner caught a live OAuth client secret in a committed
session log — an agent had pasted smoke-test output verbatim, and nothing in the protocol or
tooling stood between a rendered credential and `git push`. The after-session ritual now carries
an explicit **redaction rule** (never write secrets or PII into `memory/`; redact pasted output
to `(REDACTED)`; a committed secret is *exposed* — rotate it; history cleanup is separate and
human-led; redaction is the one sanctioned edit to an otherwise-immutable session log), and
`memory-lint` gains check 10 **`[secret-material]`** — token shapes, credential-key assignments
with literal values, emails, SSN / Luhn-verified card shapes, absolute home paths — scanning
`memory/*.md`, `sessions/`, **and** `archive/`, never echoing the matched value, waivable
per-line with `lint:allow-secret-material`. Advisory (WARN; `--strict` / `AGENT_MEMORY_STRICT=1`
gate it red). No memory-file shape change.

**Steps:**

1. **Re-copy the tool-managed built-in** `agent-skills/memory-lint/` (scripts, tests, SKILL.md)
   verbatim from the tool repo — built-ins are re-copied on upgrade (`upgrades-additive`
   carve-out) — then run `sync skill adapters` (the SKILL.md description changed).
2. **Merge the redaction rule into the target's `AGENTS.md`** from `templates/AGENTS.md`
   (After Every Session → step 1) — merge into a customized hub, never overwrite. **Re-copy**
   `.agent/schema.md` verbatim (its session-file section gained the rule).
3. **Run `memory-lint` and triage any `[secret-material]` findings now:** redact each hit to
   `(REDACTED)`; if it was a live credential, **rotate it** and treat git history as exposed
   (escalate per the org's process — rotation first; a history rewrite is a separate, human-led
   decision); tag deliberately-quoted examples with `lint:allow-secret-material` instead of
   deleting the narrative.
4. **Stamp** `.agent/version.md` → `version: 4.33.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a
   truncate-first one-liner.**
5. **Verify:** both mirror test suites pass (44 each: `python3 -m unittest
   agent-skills/memory-lint/scripts/test_memory_lint.py`, `node --test
   agent-skills/memory-lint/scripts/test_memory_lint.mjs`); `memory-lint` reports clean or only
   consciously-triaged advisories.

---

## Rung: 4.33.0 → 4.33.1 — `[secret-material]`: ALL-CAPS enum constants are not credentials (PATCH)

**What changed:** check 10's first field contact (the 2026-08-13 Mode B upgrades) produced one
finding across two production repos — a false positive: a session log documenting Confluent's
`bearer.auth.credentials.source` property with its ALL-CAPS enum value (`OAUTHBEARER` — a source
*type*, not a credential). The credential-assignment pattern now recognizes ALL-CAPS identifiers
(`^[A-Z][A-Z0-9_]{2,}$`) as config constants; real credentials carry mixed case/symbols, and
uppercase-only token shapes (e.g. AWS access-key ids) stay covered by the value-shape patterns
independently. Detector-only — no memory-file shape change; SKILL.md description unchanged
(adapters untouched).

**Steps:**

1. **Re-copy the tool-managed built-in** `agent-skills/memory-lint/` (scripts + tests) verbatim
   from the tool repo.
2. **Optional cleanup:** a `lint:allow-secret-material` waiver added solely for this FP class —
   an ALL-CAPS enum value on a credential-keyed property (e.g. mercury-composable's
   `memory/sessions/2026-07-09-212417.md`) — can now be dropped; re-run `memory-lint` to confirm
   it stays clean.
3. **Stamp** `.agent/version.md` → `version: 4.33.1`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a
   truncate-first one-liner.**
4. **Verify:** both mirror suites pass (45 each); `memory-lint` clean or consciously triaged.

---

## Rung: 4.33.1 → 4.33.2 — `[secret-material]`: backtick is a value delimiter (PATCH)

**What changed:** the v4.33.1 enum-constant exclusion missed the form the motivating field line
actually used — markdown inline code. In `` `key=VALUE` `` the closing backtick rode into the
captured value (``OAUTHBEARER` ``), so the ALL-CAPS rule didn't match and the false positive
survived; the 4.33.1 rung's own verify step caught it against the live target minutes after
release. Every scanned memory surface is markdown, so the credential-assignment pattern now
treats backticks like quotes (a backticked mixed-case literal still flags). Detector-only — no
memory-file shape change; SKILL.md description unchanged (adapters untouched).

**Steps:**

1. **Re-copy the tool-managed built-in** `agent-skills/memory-lint/` (scripts + tests) verbatim
   from the tool repo.
2. **Drop the FP-class waiver** the 4.33.1 rung described (an ALL-CAPS enum value on a
   credential-keyed property — e.g. mercury-composable's `memory/sessions/2026-07-09-212417.md`),
   including the markdown inline-code form this rung fixes; re-run `memory-lint` to confirm zero
   `[secret-material]` findings without it.
3. **Optional — re-copy the forge description template** (`.github/pull_request_template.md`,
   `.gitlab/merge_request_templates/Default.md`, or `.azuredevops/pull_request_template.md`):
   v4.33.2 converts its rendered `<sub>` advisory footer into an HTML comment (guides authors,
   never renders in a created PR/MR). Skip if the target customized its template.
4. **Stamp** `.agent/version.md` → `version: 4.33.2`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`. **Use the Edit tool (or read-into-a-variable then write) — never a
   truncate-first one-liner.**
5. **Verify:** both mirror suites pass (45 each); `memory-lint` clean or consciously triaged.

---

## Rung: 4.33.2 → 4.33.3 — `[secret-material]` security-review hardening (PATCH)

**What changed:** a fresh-context security review found four gaps in the v4.33.x defense:
forge wrappers did not pass `--strict`, so warnings never reached the branch that applies
`AGENT_MEMORY_STRICT`; the global ALL-CAPS exemption also trusted uppercase secrets; quoted
JSON/YAML keys and Authorization headers escaped assignment detection; and Mode C migration did
not require redaction/lint triage. All four are fixed. The linter remains non-echoing and
advisory by default; the forge wrapper decides whether a finding warns or blocks. Fold-in
(pre-tag, from the post-merge live-target review): the template-value pattern accepts any
brace-delimited `${…}` reference — default-value / dotted forms like `${REDIS_PASSWORD:}` and
`${a.b.c}` are placeholders, verified against the live targets — while staying full-value
anchored.

**Steps:**

1. **Re-copy the tool-managed built-in** `agent-skills/memory-lint/` (scripts, tests, SKILL.md)
   verbatim from the tool repo. Its body changed but its frontmatter description did not, so
   adapters do not need regeneration.
2. **Re-copy the forge CI floor** from the tool repo: GitHub
   `.github/workflows/agent-memory.yml`, GitLab `.gitlab/agent-memory-ci.yml`, or Azure DevOps
   `.azuredevops/agent-memory-ci.yml`. Preserve any target customization by merging only the
   `memory-lint.py --strict` invocation when a verbatim copy is unsafe. This fixes both
   advisory annotations and the opt-in strict gate.
3. **If the target uses Mode C migration, merge the migrated-history redaction rule** from
   `MIGRATE.md` / `ENABLE.md`: redact during conversion and triage every `[secret-material]`
   finding before committing generated sessions.
4. **Run `memory-lint` and triage newly detected forms:** uppercase literals on secret-bearing
   keys, quoted JSON/YAML credential assignments, Authorization headers, and values that only
   *contain* placeholder words. Redact real material; rotate any live credential; waive only a
   deliberately quoted, non-live example.
5. **Stamp** `.agent/version.md` → `version: 4.33.3`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`. Use an edit/read-before-write path, never truncate first.
6. **Verify:** both mirror suites pass (46 each); Python/Node linter output is byte-identical;
   the target's forge CI invocation includes `memory-lint.py --strict`; lint is clean or only
   consciously triaged.

---

## Rung: 4.33.3 → 4.33.4 — `[secret-material]`: reject non-empty template defaults (PATCH)

**What changed:** v4.33.3 accepted any brace-delimited `${…}` value as a safe placeholder.
That fixed empty-default and dotted-reference false positives, but also exempted a literal
fallback that may itself be a rendered secret. `${NAME}`, `${NAME:}`, and dotted references
remain safe; a non-empty fallback such as `${CLIENT_SECRET:-RealSecret123}` now flags without
echoing its value. Detector-only — no memory-file shape change; SKILL.md description unchanged
(adapters untouched).

**Steps:**

1. **Re-copy the tool-managed built-in** `agent-skills/memory-lint/` (scripts + tests) verbatim
   from the tool repo.
2. **Stamp** `.agent/version.md` → `version: 4.33.4`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`. Use an edit/read-before-write path, never truncate first.
3. **Verify:** both mirror suites pass (46 each); lint is clean or consciously triaged.

---

## Rung: 4.33.4 → 4.34.0 — pre-commit secret guard, memory + config surfaces (MINOR)

**What changed:** the v4.33.x DLP arc covered agents at write time (ritual redaction rule) and
pushes (CI floor), but a human teammate committing directly met no automated check until the
remote already had the secret — and the incident's *origin* was never a memory file: the
credentials entered the repo inside a Postman JSON and an OpenShift YAML, then contaminated a
session log when a dry-run rendered them. The new committed `.githooks/pre-commit` scans the
**staged content** (the index — exactly what the commit would publish; only what THIS commit
stages) of `memory/**.md` (full profile) **and of config files**
(`.json`/`.yml`/`.yaml`/`.properties`/`.toml`/`.ini`/`.env*` — credential-class checks)
**before the commit exists**; the three forge CI wrappers run the matching changed-config scan
on push via the new `memory-lint --scan-files` mode. The guard **enforces by default** —
findings block the commit (the deliberate, maintainer-decided exception to the advisory
doctrine: secrets carry irreversible after-the-fact cost); opt down to warn-only with
`AGENT_MEMORY_SECRET_GUARD=advisory` (env or `git config agent-memory.secretguard advisory`);
one-off bypass `git commit --no-verify`; merge commits skipped. The CI floor stays
advisory-by-default (`AGENT_MEMORY_STRICT=1` gates). JSON/properties exemptions live in the
committed, human-audited `.agent/secret-scan-ignore` (config files only, never `memory/`).
Detector refinements were tuned on a 661-file live-corpus probe to zero false positives; the
mirror suites grow to 49 tests per runtime. SKILL.md frontmatter description unchanged →
adapters untouched.

**Steps:**

1. **Re-copy the tool-managed built-in** `agent-skills/memory-lint/` (scripts, tests, SKILL.md)
   verbatim from the tool repo — the runtimes gained `--scan-files` and the probe-tuned
   placeholder refinements.
2. **Copy the new hook** `.githooks/pre-commit` verbatim from the tool repo, and **re-copy**
   `.githooks/README.md` + `.githooks/init.sh` (both updated for the two-hook layout).
   **`chmod +x .githooks/pre-commit`** — git silently ignores a non-executable hook (commit
   mode `100755`).
3. **Copy the exemptions stub** `templates/.agent/secret-scan-ignore` →
   `.agent/secret-scan-ignore` (verbatim; skip if the target already carries one — additive).
4. **Re-copy the forge CI file** (`.github/workflows/agent-memory.yml`,
   `.gitlab/agent-memory-ci.yml`, or `.azuredevops/agent-memory-ci.yml`) — all three gained the
   changed-config secret scan. Preserve target customization by merging only the new scan block
   when a verbatim copy is unsafe.
5. **Merge the trigger-layer note into the target's `AGENTS.md`** from `templates/AGENTS.md`
   (the v4.19.0 blockquote now describes both surfaces and the "advisory by default; the
   pre-commit secret guard alone enforces" doctrine) — merge, never overwrite a customized
   hub. **Tell the team the default changed**: a staged-secret finding now blocks the commit;
   the opt-down (`AGENT_MEMORY_SECRET_GUARD=advisory`) and `--no-verify` are the escape
   hatches.
6. **No activation step** — the hook rides the target's existing `core.hooksPath .githooks`.
   If `git config core.hooksPath` is unset (never-initialized clone), run
   `bash .githooks/init.sh` once.
7. **Stamp** `.agent/version.md` → `version: 4.34.0`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`. Use an edit/read-before-write path, never truncate first.
8. **Verify:** mirror suites pass (49 each); `.githooks/pre-commit` is present and executable
   and runs clean with nothing staged; `memory-lint --scan-files <a-known-config-file>` exits 0
   on clean content; `memory-lint` clean or consciously triaged.

---

## Rung: 4.34.0 → 4.34.1 — secret-guard output readability (PATCH)

**What changed:** field feedback from the maintainer's own regression test of the enforcing
guard — every `[secret-material]` finding line carried the same advisory tail, burying the
findings. Finding lines now end at `(N hit(s), first at line N)`; the redact/rotate/history
guidance appears **once per run**: in the pre-commit hook's `-> fix it` footer (now preceded
by a blank separator line and carrying the shared/rotation/history wording), as a one-line
trailer in `--scan-files` mode, and as a one-line trailer after the warnings in a full
`memory-lint` run. Output-format only — no detection change; both runtimes at parity.

**Steps:**

1. **Re-copy the tool-managed built-in** `agent-skills/memory-lint/` (scripts + tests) and
   **`.githooks/pre-commit`** verbatim from the tool repo; keep the hook executable
   (`chmod +x`, mode `100755`).
2. **Stamp** `.agent/version.md` → `version: 4.34.1`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`. Use an edit/read-before-write path, never truncate first.
3. **Verify:** mirror suites pass (49 each); stage a scratch file with a dummy credential and
   run `bash .githooks/pre-commit` directly — findings print without per-line tails, one
   consolidated footer, then the block line; unstage and remove the scratch file.

---

## Rung: 4.34.1 → 4.34.2 — secret guard: the tool's own opt-down knob is not a credential (PATCH)

**What changed:** a self-inflicted `[secret-material]` false positive, reported from the field
(mercury-composable, 2026-08-19): the pre-commit guard's blocking message prints
`AGENT_MEMORY_SECRET_GUARD=advisory`, and a memory file documenting that guidance (a session log
describing a hook regression test, a runbook) was itself flagged as a `credential-assignment` —
the key contains `SECRET` and `advisory` meets the value floor. `_is_placeholder_value` (both
runtimes) now exempts exactly the knob's documented settings — key `AGENT_MEMORY_SECRET_GUARD`
(case-insensitive), value `advisory`/`enforcing` with trailing `).,` punctuation tolerated
(prose/parenthesized guidance rides it into the captured value; the guard's own line ends
`…=advisory)`). Any other value under that key still flags, so the exemption is not a smuggling
envelope. Mirror suites gain a verbatim pinning case each (50/50). The skill doc also records the
maintainer's call on the issue's secondary question: AWS's canonical doc-example keys
(`AKIA…EXAMPLE` pair) **still flag by design** — quote them deliberately with
`lint:allow-secret-material`; the guard keeps one contract (redact or visibly waive) rather than
an invisible whitelist. Tool-managed built-in; no memory-file shape change.

**Steps:**

1. **Re-copy the `memory-lint` skill files** (both runtimes + mirror tests) from this repo:
   `agent-skills/memory-lint/scripts/memory-lint.py`, `.../memory-lint.mjs`,
   `.../test_memory_lint.py`, `.../test_memory_lint.mjs`, and `agent-skills/memory-lint/SKILL.md`
   (body note only — the description is unchanged, so **adapters need no re-sync**).
2. **Drop any waiver added for this FP class**: a `lint:allow-secret-material` tag on a line whose
   only "credential" is `AGENT_MEMORY_SECRET_GUARD=advisory`/`=enforcing` is now unnecessary —
   remove the tag (the line itself stays). Leave all other waivers alone.
3. **Stamp** `.agent/version.md` → `version: 4.34.2`, `last_upgraded: <today>`, preserving
   `enabled_with` and `mode`. Use an edit/read-before-write path, never truncate first.
4. **Verify:** mirror suites pass (50 each); `memory-lint` on the repo shows no
   `[secret-material]` finding for knob-guidance lines; a scratch line such as
   `AGENT_MEMORY_SECRET_GUARD=Xk9fQ2mZlp0TrN` (any 8+-char opaque value — not an
   angle-bracket placeholder, which is exempt as a template shape) still flags.
