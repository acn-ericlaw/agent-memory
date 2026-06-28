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
| 4.14.1 | **Re-synced `AGENTS.md` source clarified (PATCH):** `UPGRADE.md` now maps each re-synced file to its one canonical source — a target's `AGENTS.md` comes from **`templates/AGENTS.md`** (the memory hub), **never** the tool's **root** `AGENTS.md` (the operator/dual-mode dispatcher, which references the non-installed `ENABLE.md`) — with a self-check (a target `AGENTS.md` must not say "AI-Enable Another Repository"). The 4.14.1 rung **verifies + repairs** a mis-synced `AGENTS.md`. Found dogfooding a v3.7.0→v4.14.0 upgrade (GitHub Copilot, `mercury-composable`) that grabbed the root file |
| 4.14.0 | **Optional Architecture Decision Record log (MINOR):** documents an **optional** human-facing `docs/ADR.md` decision log at the VBDI **Design** altitude — one durable architecture decision per entry (Status/Date/Abstract/Rationale-with-consequences), newest-first, `Proposed → Accepted → Superseded/Deprecated`, **never deleted** (mirrors `DECAY.md` §9). Map-don't-duplicate: live constraints stay in `continuity.md`, the ADR carries the *why*, cross-linked by `formalizes:` ↔ a visible `(ADR-NNNN)` tag in the invariant title (a human pointer, not an agent read-cue). Read **on demand** — **not** in the per-session read path (zero default token cost). Documented in `.agent/schema.md` + `AGENTS.md`; **not auto-installed** into targets (adopt on demand) |
| 4.16.1 | **Session filename drift fix (PATCH):** closes two gaps that caused date-only filenames (`YYYY-MM-DD.md`): `templates/AGENTS.md` + `schema.md` now require `date -u +%Y-%m-%d-%H%M%S` (no "or equivalent"); `memory-lint` gains `check_session_filenames` warning (check 5) in both runtimes |
| 4.16.0 | **ADR default path aligned to industry convention (MINOR):** the optional ADR log default path changes from `docs/ADR.md` to `docs/arch-decisions/ADR.md`. Normative: `.agent/schema.md`, `AGENTS.md` (root + template), `DECAY.md §12`; this repo moves its own `docs/ADR.md`. Targets at the new path already (e.g. `mercury-composable`) need no file move — version bump only |
| 4.15.0 | **ADR log upkeep trigger (MINOR):** the optional `docs/ADR.md` log is now *maintained*, not just documented — **once it exists**, making a new durable architecture decision, or superseding/invalidating a continuity fact carrying an `(ADR-NNNN)` tag, **prompts a human-gated ledger update** (add a newer ADR; mark the old `Superseded`/`Deprecated`, never delete; keep `formalizes:` ↔ `(ADR-NNNN)` in sync). Closes the 4.14.0 gap where the log could be adopted but had no cue to evolve. Re-syncs `templates/AGENTS.md` + root `AGENTS.md`, `templates/.agent/schema.md`, and `DECAY.md §12`; still **not auto-installed**. Surfaced dogfooding `mercury-composable`'s ADR opt-in |
| 4.17.0 | **GitHub Copilot CLI skills adapter (MINOR):** a **5th** skills adapter target `.github/skills/<name>/SKILL.md` — Copilot CLI follows the open Agent Skills standard (same `SKILL.md` shape as the Claude/Kiro adapter) and auto-matches by `description` (also accepts `/<name>`). `sync skill adapters` now writes **five** adapters; `.github/skills/` is gitignored **path-scoped** (the rest of `.github/` — `copilot-instructions.md`, `workflows/` — stays tracked). Copilot also gains skills in the Mode C detection/migration table (`.github/skills/`, `.agents/skills/` → `agent-skills/`); `templates/.github/copilot-instructions.md` now points Copilot at the skills layer. Mirrors the 4.5.0 Kiro rung. Surfaced dogfooding `~/sandbox/simple-proxy` (Copilot CLI couldn't find a skill authored only in `agent-skills/`) |
| 4.18.0 | **`sync skill adapters` is now a runnable script (MINOR):** a new built-in **`sync-adapters`** skill ships a deterministic adapter-regeneration script (Node + Python at parity, built-ins only) that (re)writes the five vendor adapters for every skill and prunes the orphans it generated. Replaces the prose-recipe-only sync that agents (e.g. Copilot CLI / Gemini) struggled to *run* — they hunted for a non-existent npm/MCP command and flailed. Enable + every Mode B re-enable now invoke the script; an agent also triggers it by description. Consistent with `no-build-step-agent-run` (same category as the `memory-lint` script). Surfaced dogfooding `~/sandbox/simple-proxy` |
| 4.19.0 | **Vendor-neutral ritual triggers (MINOR):** the after-session ritual no longer relies on the agent self-triggering. Enable installs a committed **`.githooks/post-commit`** (auto-stubs a session log when a commit does real work without one; re-syncs adapters), **agent-activated** via `git config core.hooksPath .githooks` (no manual user step), plus a **CI floor** (`.github/workflows/agent-memory.yml`: `memory-lint` + advisory session-log check on push/PR, zero per-user setup). Advisory by default (opt-in `AGENT_MEMORY_STRICT=1` gate); `no-build-step-agent-run` holds (git/CI invoke them; the tool runs nothing). Honest limit: git can't auto-run hooks on a bare clone → CI is the backstop. From real client-team pain (ritual not followed even with Claude; Copilot-only teams had no triggers) + the zero-manual/untrained-user constraint; design `docs/DESIGN-ritual-triggers.md` |
| 4.20.0 | **First-run init (MINOR):** closes the fresh-clone activation gap (Copilot dogfood: the memory bootstrap self-initializes, but a clone has the gitignored adapters **absent** + the hook **unactivated**). Adds **`.githooks/init.sh`** (one idempotent command: regenerate adapters + `git config core.hooksPath .githooks`) + an **`AGENTS.md` self-init note** so the agent does it on its first session. One agent-run step (or one human command) instead of two; CI stays the zero-config floor |
| 4.20.1 | **Self-init in `copilot-instructions.md` (PATCH):** v4.20.0's self-init reached Claude (acts on `AGENTS.md`) but **not Copilot CLI** (its `start` front-loads `copilot-instructions.md` + summarizes — so on a fresh clone the hook stayed inactive + adapters absent). Folds the first-run init into the **top of `copilot-instructions.md`** so Copilot runs `bash .githooks/init.sh` before summarizing. Re-sync that one file; the `init.sh` fallback + CI floor are unchanged |
| 4.20.2 | **Windows line-ending hardening (PATCH):** adds a **`.gitattributes`** pinning `*.sh` + `.githooks/*` to **LF**, so Git for Windows (`core.autocrlf=true`) doesn't rewrite them to CRLF on checkout (which breaks bash: `bad interpreter: /usr/bin/env bash^M`, silently disabling the hook + `init.sh`). Installed/merged into targets additively (like the `.gitignore` block). Makes the bootstrap + hooks robust on Windows (Git Bash / WSL), not luck-of-the-default. From a Copilot Windows-feasibility check |
| 4.20.3 | **memory-lint catches an empty/malformed version manifest (PATCH):** adds a deterministic **`check_version_manifest`** ERROR to both runtimes (`memory-lint.py` + `memory-lint.mjs`, at parity, with mirror tests) so a present-but-empty/malformed `.agent/version.md` fails the lint floor (CI + reviews) instead of silently breaking Mode B upgrade detection. Closes the loop on the v4.20.1 bug (a truncating stamp one-liner emptied a target's `version.md` → an agent misread the version). A *missing* `version.md` stays valid (pre-versioning baseline) and is not flagged. Re-copy the memory-lint skill files |
| 4.21.0 | **Google Antigravity (`agy`) skills adapter (MINOR):** a **6th** adapter target `.agents/skills/<name>/SKILL.md` — the open Agent Skills standard dir read by Google Antigravity (the Gemini CLI successor), which reads `.agents/skills/`, **not** the old `.gemini/commands/*.toml`. `sync skill adapters` now writes six; `.agents/` gitignored; `.gemini/commands` kept for the transition. Skill-only re-copy + re-sync; no memory-file shape change |
| 4.26.0 | **`refresh-metadata` + `memory-lint` `[stale-metadata]` advisory (MINOR):** a **7th** built-in executing REVIEW.md steps 2–3 (apply events + re-tier) deterministically — recomputes every fact's `last_used`/`uses`/`tier` from the session reference log and writes footers back (the "full rebuild" path, runnable; pure arithmetic, never archives, `core`/`superseded` untouched). Python + Node at parity + mirror tests; `--dry-run`; idempotent. `memory-lint` gains check (9) `[stale-metadata]` (stored tier ≠ recomputed tier) to make the skipped-re-tier gap visible. From a cross-vendor field test where Gemini 3.1 Pro ran the overdue review but did the archive and skipped the metadata pass. Install via §5i (now 7 built-ins); re-copy the skill + re-copy memory-lint + re-sync adapters + re-sync `REVIEW.md`/`ENABLE.md` |
| 4.25.0 | **`archive-fact` — deterministic safe archive-move (MINOR):** a **6th** built-in (`provenance: agent-memory-builtin`) executing `REVIEW.md` step 4's move (continuity → quarter archive + INDEX) deterministically — reads the file into memory and writes once, so the truncate-before-read trap that wiped this repo's archive can't recur. Python + Node at parity + mirror tests; all-or-nothing guards (missing id / already-archived / would-empty); `--dry-run`. The agent decides *what* to archive; the helper does the *move* (`never-pick-a-winner` intact). From a cross-vendor critique (Gemini 3.1 Pro: "harden the memory-writing mechanism itself"). doc → tool, after v4.22.4's doc safeguard. Install via §5i (now 6 built-ins); re-copy the skill + re-sync adapters; re-sync `REVIEW.md`/`ENABLE.md` |
| 4.24.0 | **Decay-policy retune + review-cadence/size advisory in `memory-lint` (MINOR):** from real measurements across two enabled repos (one ran 61 sessions / 41 facts / 585 lines and **archived nothing** — the cadence review never fired in the field). `memory-lint` gains advisory check (8), both runtimes + mirror tests: `[review-overdue]` (`sessions_since_last_review ≥ review_every`, from the `last_review` stamp) and `[continuity-bloat]` (> `continuity_max_facts` / `continuity_max_lines`) — so a lapsed review rides every lint run + CI. New default `continuity_max_facts: 30` (count-based primary signal); `continuity_max_lines: 300 → 600`; `verify_invariants_every: 20 → 40`. Re-copy the memory-lint skill files; re-sync `REVIEW.md` + `AGENTS.md` + `.agent/schema.md`; merge the policy additively (preserve any custom-tuned values). Skill description unchanged → adapters need no re-sync |
| 4.23.2 | **Context-hygiene guidance — keep state externalized so compaction is safe (PATCH):** `AGENTS.md` (template + root) gains a "Long session? Keep state externalized" block. Two corrections to an initial "brain fog" framing: the agent usually **can't compact itself** (so its lever is *externalizing state*), and the **objective** health signal is **context-window utilization (tokens vs. limit)**, not time or a felt "fog." Teaches: write the session log + `continuity.md` at each natural seam **before** compaction; at high utilization suggest compacting (or rely on auto-compact), never mid-task; re-verify against live files afterward. Re-sync `templates/AGENTS.md`; doc-only, no shape change |
| 4.23.1 | **`last_harvest` marker for incremental harvests (PATCH):** Project State gains an optional `last_harvest: YYYY-MM-DD | through <session>` field (in `continuity.md`, with `last_review`/`last_invariant_check` — **not** `version.md`); `harvest-knowledge` reads it to scope the next run to docs changed since then (full pass if absent) and stamps it on completion (even a no-op). From a cross-vendor test drive where the agent had to infer the window. Re-sync `.agent/schema.md` + the `harvest-knowledge` skill; no shape change (the field is additive + optional) |
| 4.23.0 | **`harvest-knowledge` built-in skill (MINOR):** a **5th** built-in (`provenance: agent-memory-builtin`) — the on-demand, recurring counterpart to the enable-time curious harvest (Step 4b). Re-scans the repo's human-authored docs and folds newly-durable facts into the neutral, shared `memory/` **additively** (map-don't-mirror; check-existing-first; conflicts → `Contradiction`; budget-with-disclosure). Keeps a living repo's memory in sync as docs evolve; **not** a vendor `/init` (that does code-analysis → a vendor steering file; this does knowledge-distillation → neutral memory, additive + repeatable). "Re-harvest" moves out of the Mode B upgrade path into this skill — the enable-time harvest stays a fresh-enable event. Installed by §5i (now 5 built-ins); on the rung, re-copy the skill + re-sync adapters |
| 4.22.4 | **Safe-write safeguard in `REVIEW.md` (PATCH):** the review ritual's Safety section now mandates **append-mode / read-into-var (never `open(f,"w").write(open(f).read()+…)`, which truncates before the read)** for scripted archive/`continuity.md` edits, and **running `memory-lint` after any scripted memory mutation** (it catches truncation; git recovers). From a real archive-truncation incident during a review. Re-sync `REVIEW.md`; no shape change |
| 4.22.3 | **Tighten the post-commit session window: 2h → 30 min (PATCH):** v4.22.1's window was 2h, but observed follow-up stubs were **minutes** apart and 2h can conflate a *new* session started within 2h of the prior log. Default now **30 min**; override env var renamed to **`AGENT_MEMORY_SESSION_WINDOW_MINUTES`** (integer minutes — BSD `date -v` rejects fractional hours). Re-copy `.githooks/post-commit`; no shape change |
| 4.22.2 | **Lightweight mode: one log per session, not per commit (PATCH):** the agent-side mirror of 4.22.1. `AGENTS.md` lightweight mode now says that if a session log already exists for *this* working session, a later **memory-neutral** commit **enriches** it rather than spawning another lite log (clutter + decay session-count inflation). Memory-relevant work still gets its own full log. Doc-only; re-sync `templates/AGENTS.md` (+ root `AGENTS.md`). No shape change |
| 4.22.1 | **post-commit auto-stub: per session, not per commit (PATCH):** the `.githooks/post-commit` auto-stub now suppresses a new stub when a session log already exists within an **active-session window** (default 2h; override `AGENT_MEMORY_SESSION_WINDOW_HOURS`), nudging the agent to enrich the existing log instead. Detected by the newest session **filename** timestamp (immutable + clone-safe; `mtime` is reset by checkout) vs a window-ago stamp. The old guard checked only for an *untracked* stub, so after the log was committed every later work commit wrote a fresh stub — ~6 near-identical lite logs/session, inflating the decay session-count. New session (no log in window) still stubbed; bash 3.2-compatible. From downstream `mercury-composable` feedback |
| 4.22.0 | **Discovery, consent & merge-friendliness — four bundled additive improvements (MINOR).** One release; developed iteratively in one unreleased session (dev-numbered 4.22–4.25), consolidated per "one version per release." **(a) Curious knowledge harvest at enable** — `ENABLE.md` Step 4b recursively descends every doc tree (`docs/`/`wiki/`/`rfcs/`/`adr/`/…, all subfolders) + sweeps repo roots for human-authored knowledge markdown (decision logs, ADRs, kanban/roadmap, architecture notes), distilling durable facts into memory (map-don't-mirror), bounded by a read **budget with disclosure** (overflow → a `(knowledge-harvest)` thread). **(b) Fresh-enable advisory + discovery depth** — Mode A opens with a concise **exec summary of the protocol** (what it is / writes / won't touch / is committed+shared) + a `cancel` gate (**informed consent**), then offers **standard scan vs `/init`-depth deep analysis** (deep written to the neutral memory layer, never a vendor file); a first enable session log records the choice. **(c) `continuity.md` merge-friendliness** — `status` is spec'd a SHORT current-state line, **not a changelog** (`.agent/schema.md` + `AGENTS.md`); new **"Concurrency & merge-friendliness"** conventions (one fact/line; append-only union/keep-both; scalar take-later); `memory-lint` **check 7** flags a leftover conflict marker (`<<<<<<<`/`>>>>>>>`/diff3 `|||||||`) as an ERROR (bare `=======` setext underline exempt), both runtimes + tests. **(d) `MERGE.md`** — a new installed, no-code on-demand protocol for resolving a git conflict in `memory/`: tiered + human-gated, enforcing **`never-pick-a-winner`** (mechanical → rule; semantic clash → preserve both + Contradiction/supersession; `memory-lint` gate; human approves). Mostly operator-side (`ENABLE.md`) + the `memory-lint` skill + one new root doc (`MERGE.md`); no memory-file shape change. From a client enablement complaint, a teammate-concurrency review, and a GitHub Copilot review |


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
