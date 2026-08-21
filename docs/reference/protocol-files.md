# Protocol Files

The protocol is a small set of Markdown files rooted at `memory/` and the repository root. They are written for an
**AI agent to execute**, so they're terse and operational — this page is a map. Each links to
the source on GitHub.

## Always read

| File | Role |
|---|---|
| [`AGENTS.md`](https://github.com/acn-ericlaw/agent-memory/blob/main/AGENTS.md) | Exact one-line universal discovery shim to `memory/PROTOCOL.md`. |
| [`memory/PROTOCOL.md`](https://github.com/acn-ericlaw/agent-memory/blob/main/memory/PROTOCOL.md) | Canonical activation and lifecycle protocol. The tool copy includes dual-mode operator routing; enabled targets receive the target-only source from `templates/memory/PROTOCOL.md`. |
| [`README.md`](https://github.com/acn-ericlaw/agent-memory/blob/main/README.md) | Human-facing quickstart + design philosophy. |

## Read on demand

| File | Role |
|---|---|
| [`DECAY.md`](https://github.com/acn-ericlaw/agent-memory/blob/main/DECAY.md) | The authoritative decay rules — tiers, windows, what never decays, supersession. |
| [`REVIEW.md`](https://github.com/acn-ericlaw/agent-memory/blob/main/REVIEW.md) | The review ritual, step by step, with the safe-write Safety section. |
| [`MERGE.md`](https://github.com/acn-ericlaw/agent-memory/blob/main/MERGE.md) | The tiered, human-gated `memory/` conflict-resolution protocol. |
| [`SKILLS.md`](https://github.com/acn-ericlaw/agent-memory/blob/main/SKILLS.md) | The skills layer — authoring, syncing, deleting, the adapter recipe. |

The protocol's instruction-versus-evidence boundary is governed by the
[agent instruction and memory security contract](../architecture/security.md).

## Operator-only

| File | Role |
|---|---|
| [`ENABLE.md`](https://github.com/acn-ericlaw/agent-memory/blob/main/ENABLE.md) | The 10-step enablement flow (Modes A / B / C). Lives in the tool, never installed into a target. |
| [`MIGRATE.md`](https://github.com/acn-ericlaw/agent-memory/blob/main/MIGRATE.md) | Vendor-file detection + promotion for Mode C. |
| [`UPGRADE.md`](https://github.com/acn-ericlaw/agent-memory/blob/main/UPGRADE.md) | The version ladder — the per-version record + the detailed text behind each semantic step. |
| [`MANIFEST.md`](https://github.com/acn-ericlaw/agent-memory/blob/main/MANIFEST.md) | The declarative target state (v4.35.0): every installed artifact + policy, the semantic-steps table, and the coverage contract behind `scripts/reconcile.py`/`.mjs`. |

## Per-repo state (generated)

| Path | Role |
|---|---|
| `memory/continuity.md` | The live projection — facts, decisions, open threads. |
| `memory/vision.md` | The north star (`core`, invariant-verified). |
| `memory/sessions/` | Immutable dated session logs — the event ledger. |
| `memory/archive/` | Faded facts + a greppable `INDEX.md`. |
| `memory/decay-policy.md` | This repo's tunable [decay parameters](decay-parameters.md). |
| `.agent/version.md` | Install manifest — gates [in-place upgrades](../guides/upgrade.md). |
| `.agent/schema.md` | The file-format reference for the memory layer. |

!!! tip "Going deeper"
    For the *why* behind these, read the [Whitepaper](../agent-memory-whitepaper.md) and the
    design notes under **Background** in the nav.
