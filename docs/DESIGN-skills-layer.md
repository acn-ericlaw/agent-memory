# DESIGN — Cross-Vendor Skills Layer (portable capabilities over the shared layer)

> **Status:** **implemented v4.1.0** (2026-06-15), **refined v4.1.1** (folder finalized as
> `agent-skills/`; Cursor adapter fixed), **+ "sync skill adapters" v4.2.0** (regenerate
> adapters from the neutral skill on demand — adapters are gitignored, so they don't travel),
> **+ authoring convention & "adopt skill" safety-net v4.3.0** (author in `agent-skills/`,
> never a vendor folder; promote a natively-authored skill back into `agent-skills/`),
> **+ description guidance v4.3.1–4.3.3**, **+ lightweight-skills v4.4.0** (recipe + sync/adopt/
> sanity ops moved to an on-demand `SKILLS.md`; per-session safety check removed — skill work
> is conscious/on-demand; upgrades do a read-only filename check that *recommends* sync),
> **+ Kiro adapter v4.5.0** (4th adapter target `.kiro/skills/<name>/SKILL.md` — Kiro follows
> the open Agent Skills standard, same shape as the Claude adapter; Kiro added to the Mode C
> detection table; Kiro auto-reads root `AGENTS.md`, so the memory layer needs no pointer file),
> **+ trigger-semantics & commit-guard clarifications v4.5.1** (from a Gemini CLI dogfood: the
> Gemini adapter is a *slash command* `/<name>`, not a natural-language auto-trigger — NL routes
> through the baseline to the same skill; and `sync` must never commit / recommend committing the
> gitignored adapter dirs),
> **+ enforced adapter sync v4.12.0** (enable + every Mode B re-enable now *run* `sync skill
> adapters` — idempotent, gitignored-only — instead of a read-only "recommend, don't run" check, so a
> skill's vendor-native adapters are materialized at enable/upgrade rather than left for the user to
> sync by hand; closes the loose end where an upgrade left newer/old-target adapters missing),
> **+ tool-provided-skill provenance v4.13.0** (the three shipped built-ins carry
> `provenance: agent-memory-builtin` so a target's AI recognizes a *system* skill at edit time;
> `SKILLS.md` routes a change to **fork** a variant or **upstream** a genuine fix for back-port +
> validation — closing the gap where a real `memory-lint` fix in a target nearly got stranded),
> **+ GitHub Copilot CLI adapter v4.17.0** (5th adapter target `.github/skills/<name>/SKILL.md` —
> Copilot CLI follows the open Agent Skills standard, same shape as the Claude/Kiro adapter,
> description-matched + `/<name>`; gitignored **path-scoped** since `.github/` itself stays tracked;
> Copilot project skills also promoted in Mode C — found dogfooding `~/sandbox/simple-proxy`),
> **+ runnable `sync-adapters` script v4.18.0** (the `sync skill adapters` operation becomes a bundled
> built-in script — Node + Python at parity — instead of a prose recipe the agent acts out by hand;
> dogfooding showed Copilot/Gemini couldn't *run* a prose operation and hunted for a non-existent
> command. Consistent with `no-build-step-agent-run`: same category as the `memory-lint` script).
> Sibling to `DESIGN-evolving-memory.md` and `DESIGN-vbdi-lifecycle.md`.
> The maintainer chose **all-vendor adapters** at build time (Claude + Gemini + Cursor + Kiro + Copilot),
> so §4c is fully realized rather than Claude-only.
> **Source:** a real-work finding (2026-06-15) — a client repo enabled with agent-memory
> carried user-defined **Claude skills** under `.claude/skills/`, which the tool neither
> shares across vendors nor (today) even lets travel with the repo (`.claude/` is
> gitignored). Captured as Blueprint gap `bp-skills-layer` (serves `vision-agent-memory`).

---

## 1. Why

agent-memory shares two things across vendors today: **memory** (`memory/`) and
**steering** (folded into `memory/instructions.md`, surfaced through the `AGENTS.md` hub +
thin per-vendor pointers). It shares **no capabilities** — the *procedural skills* a team
builds up (a `SKILL.md` that says *when* to do something and *how*, plus optional helper
scripts).

Two concrete failures motivate this:

1. **Skills don't travel.** `templates/.gitignore` ignores `.claude/` wholesale (personal
   per-machine runtime). A team that commits project skills under `.claude/skills/` finds
   them excluded from git — they never reach a teammate at all, on any vendor.
2. **Skills don't cross vendors.** Even shared, a Claude `SKILL.md` is Claude-shaped; a
   teammate on Gemini or Cursor can't run it. That contradicts the Vision —
   *"many **different** AI vendors collaborate through one shared, committed layer."*

This is the missing third leg of the shared layer: **memory + steering + skills**.

## 2. Principles (inherited — already ours)

- **No-code, markdown-only** — *the files are the product, the agent is the runtime.* A
  skill is markdown + optional portable scripts; nothing here needs an engine.
- **Vendor-neutral / never-pick-a-winner** — one neutral source of truth; vendors adapt to
  it. The tool does not privilege Claude's format.
- **Map, don't duplicate** — reuse the existing hub-and-pointers mechanism (`AGENTS.md` +
  thin vendor files), the `legacy/` preservation rule, and the personal-vs-shared split.
- **Target-repo scope only** — skills live in the repo; `~/` and `~/.claude/` are untouched.
- **Additive / non-destructive** — a repo with no skills works exactly as before; an
  un-upgraded agent simply ignores `agent-skills/`.

## 3. Observation: a skill is ~90% already neutral

A Claude `SKILL.md` is just markdown: a `name`, a `description` (the *when-to-use*
trigger), a procedure, and maybe a script. The only vendor-specific parts are **where the
file lives** and **how that runtime auto-discovers it**. So the neutral form ≈ the content
itself, lifted to a neutral location with a minimal normalized frontmatter. (There is no
cross-vendor *skill* standard the way `AGENTS.md` is becoming one for steering — so the
tool defining the neutral substrate is the pragmatic move, exactly as it did for `memory/`.)

## 4. The design

### 4a. Neutral source of truth — `agent-skills/` (committed)

A new top-level shared layer, parallel to `memory/`:

```
agent-skills/
  <skill-name>/
    SKILL.md        # frontmatter: name + description(when-to-use); body: the procedure
    scripts/…       # optional portable helpers (sh / python), referenced by relative path
```

`agent-skills/` is **committed** — it travels with the repo and reaches every contributor
regardless of vendor. Normalized frontmatter is deliberately minimal (`name`,
`description`); Claude's existing `SKILL.md` frontmatter already matches, so Claude is the
trivial case and other vendors adapt.

### 4b. Universal runtime — the `AGENTS.md` hub (no per-vendor code)

`AGENTS.md` — which every bootstrap file already points to — gains a short **Skills**
section:

> *Capabilities live in `agent-skills/`. When a task matches a skill's `description`, read and
> follow its `SKILL.md` (and any scripts it references).*

Because **the agent is the runtime**, this works for *every* vendor, including those with
no native skill mechanism (Codex/AGENTS.md, plain Cursor). Zero per-vendor code; the
baseline is just "an agent reading markdown."

### 4c. Optional per-vendor adapters (thin, generated, pointers)

For vendors with a *native* skill/command system, the enable/sync step may generate a thin
adapter so the skill **auto-triggers** in that runtime — each adapter a 2-line pointer to
the neutral skill, never a copy (no duplicated content to drift, same reason the read-order
lives only in `AGENTS.md`):

| Vendor | Native mechanism | Adapter |
|---|---|---|
| Claude Code | `.claude/skills/<n>/SKILL.md` (Skill tool auto-discovers) | frontmatter + body "follow `agent-skills/<n>/SKILL.md`" |
| Gemini CLI | custom command (`.gemini/commands/<n>.toml`) — **slash command `/<n>`, explicit (not NL-matched)** | command that reads the neutral skill |
| Cursor | rule (`.cursor/rules/*.mdc`) | rule referencing the neutral skill |
| Kiro | `.kiro/skills/<n>/SKILL.md` (open Agent Skills standard — auto-matched) | same shape as Claude: frontmatter + body "follow `agent-skills/<n>/SKILL.md`" |
| GitHub Copilot CLI | `.github/skills/<n>/SKILL.md` (open Agent Skills standard — auto-matched + `/<n>`) | same shape as Claude/Kiro: frontmatter + body "follow `agent-skills/<n>/SKILL.md`" |
| Codex / Kiro / AGENTS.md-only | *(none)* | nothing needed — auto-reads root `AGENTS.md`, uses the §4b baseline |

> **Trigger semantics differ (v4.5.1, from a Gemini dogfood).** "Auto-triggers" above holds for
> the *description-matched* mechanisms (Claude Skill tool, Cursor agent-requested rules, Kiro's and
> GitHub Copilot CLI's open-standard skills). **Gemini is the exception**: a custom command fires only on an explicit
> `/<name>`, never on natural-language prose — so a phrase like "run hello-world" correctly routes
> through the §4b baseline to the same neutral skill (identical result; not a missing adapter).
> Because every adapter is a pointer back to `agent-skills/`, no path can diverge. **Adapters are
> never committed** (Option A, §4d) — `sync` must not stage or recommend committing them.
>
> **Agents can't self-report the trigger (2026-06-17, three dogfood runs).** A Gemini `/<name>` is
> *expanded into the adapter's `prompt` text before the model sees anything* — the model never
> receives the slash token, only the expanded prompt, indistinguishable from a typed request. So an
> agent **cannot** reliably tell "native adapter" from "baseline," and no instruction inside the
> neutral `SKILL.md` can fix it (the `SKILL.md` is read *after* the trigger). The `hello-world` demo
> therefore **does not ask the agent to narrate its invocation path** (self-report dropped — the
> "B" option): the proof of native wiring is that the user's invocation *ran the skill at all*. Do
> not re-add path self-reporting; if a future demo truly needs deterministic path proof, carry it in
> the **adapter's own prompt text** (the only thing injected on a native trigger), not agent introspection.

### 4d. The committed-vs-personal decision — **Option A (chosen)**

`.claude/`, `.gemini/`, `.cursor/`, `.kiro/` are personal/per-machine and stay **gitignored**. So:

- **Option A (chosen):** the neutral `agent-skills/` is committed; per-vendor adapter dirs stay
  gitignored and are **regenerated locally** by the enable/sync step. The only fully
  vendor-neutral option — every vendor's user gets the skill — and it keeps the
  personal-vs-shared split clean (`.claude/` stays entirely personal, consistent with the
  `target-repo-scope-only` philosophy).
- **Option B (rejected as default):** carve a committed exception (`!.claude/skills/`).
  Pragmatic for a Claude-only team, but re-couples the shared layer to one vendor and
  muddies "`.claude/` is personal." Available as an opt-in, never the default.

## 5. Migration — promote, don't flatten

On enable (Mode C) of a repo with `.claude/skills/` (or another vendor's skill bundles):

- **Promote** them into `agent-skills/` — they are *procedures*, so they must **not** be
  flattened into `memory/instructions.md` (that home is for *steering rules*).
- **Preserve originals** under `legacy/<vendor>/skills/…` per `never-delete-vendor-files`.
- **Regenerate** the native adapter(s) from the promoted neutral skill.
- Use `git mv` for tracked files (history-preserving), per the existing migration rule.

**Authoring convention & the reverse path (v4.2.0–4.3.0).** Going forward, skills are
authored directly in `agent-skills/<name>/SKILL.md` (never a vendor folder) and forward-synced
to adapters via **"sync skill adapters"**. The migration promote above is the *one-time*
vendor→neutral import; its ongoing complement is **"adopt skill"** — the same promote, run on
demand when a skill is authored natively in a vendor folder (e.g. by a built-in skill
creator). The **session-close ritual** checks for stranded vendor-folder skills and prompts
adoption, so the neutral `agent-skills/` layer stays the single source of truth.

## 6. Alignment with the Architectural Invariants

| Invariant | How this honors it |
|---|---|
| `target-repo-scope-only` | `agent-skills/` and adapters live in the repo; `~/.claude/` untouched |
| `never-delete-vendor-files` | original skill bundles preserved under `legacy/` |
| `never-pick-a-winner` | neutral source of truth; vendors adapt; no vendor privileged |
| `no-code-markdown-only` | skills are markdown + portable scripts; agent is the runtime |
| `upgrades-additive` | new optional layer; absent `agent-skills/` ⇒ no behavior change |

## 7. Scope / non-goals

- **Not** a skill marketplace, registry, or dependency resolver — just a shared folder.
- **Not** a sandbox/execution engine — skill scripts run exactly as they do today under
  whatever vendor invokes them; the tool adds no new execution surface.
- **Not** a new frontmatter spec war — normalize the *minimum* (`name`, `description`);
  leave richer per-vendor fields to the adapters.
- Skills are **capabilities**, not memory facts and not steering — a distinct third layer,
  not metadata-tracked/decayed like `memory/` facts.

## 8. Integration points (when built — not in this doc)

A future implementation rung would touch, additively:
`ENABLE.md` (a Step to generate `agent-skills/` baseline + adapters), `MIGRATE.md` (detect &
promote vendor skill bundles → `agent-skills/`, preserve under `legacy/`), `templates/AGENTS.md`
+ root `AGENTS.md` (the §4b Skills section), `templates/.gitignore` (confirm adapter dirs
stay ignored under Option A; `agent-skills/` tracked), `.agent/schema.md` (document `agent-skills/`),
and the version ladder (`VERSION` / `UPGRADE.md` — additive ⇒ **MINOR**, e.g. a 4.x rung).

## 9. Open questions (deferred to build time)

- **Normalized frontmatter** — exact minimal key set, and how an adapter declares richer
  vendor-specific fields without polluting the neutral file. **(refined v4.3.2:** a skill
  `description` is single-line + quote-free; the adapter `description` mirrors the neutral
  skill's **verbatim**; escape/quote for the target format only if a special char is
  unavoidable — a lifecycle sanity check showed a quoted description otherwise emits invalid
  TOML/`.mdc`. **v4.3.3:** also keep it **concise + trigger-phrase-rich** (matched within a
  small discovery budget — long abstract paragraphs weaken activation); YAML `>`/`|` blocks
  are YAML-only and don't carry into the TOML adapter, so the canonical value is one logical
  line.)
- **Adapter generation locus** — **RESOLVED v4.2.0:** a "sync skill adapters" operation lives
  in the installed `AGENTS.md` "Skills" section (so a target's own agent, any vendor, can
  self-sync), idempotent (overwrite adapters, prune orphans, never touch the neutral skill);
  `ENABLE.md` Step 5h references that single recipe. Surfaced by a real cross-machine test
  (adapters are gitignored → don't travel with a clone/pull).
- **Per-vendor fidelity** — Gemini/Cursor mechanisms differ in trigger semantics; how
  faithfully a single `description` maps to each (or whether the baseline §4b suffices and
  adapters are best-effort).
- **Skill-local scripts & portability** — shell vs. python, declaring interpreter/deps in a
  no-code way.
