# Continuity — event_bus_demo

> Shared ground truth for project state across all agents and sessions.
> Update at the end of every session. Never delete — only append or update.

---

## Project State

- **project:** event_bus_demo (dir: rust_event_bus_example)
- **status:** working demo / learning project — single source file
- **last_enabled:** 2026-06-12
- **last_session:** (none yet)
- **repo:** ~/sandbox/rust/rust_event_bus_example

## Stack & Tools

- Language: Rust, edition 2021
- Async runtime: tokio (full features)
- Channels: flume (unbounded, multi-producer)
- Build/run: cargo
- VCS: none yet (not a git repo)

## Key Decisions

- Routing by string key — publishers/subscribers coupled only by route name.
- Unbounded channels for simplicity (no backpressure in the demo).
- One async handler task per route, spawned on the tokio runtime.

## Conventions

- All code in `src/main.rs`; keep handlers decoupled (no cross-references).
- Async consumption via `recv_async().await`.
- Diagnostics via `println!`.

## Open Threads

- [ ] No tests — add unit tests for `EventBus::send` routing (hit + miss cases).
- [ ] Not under version control and no `.gitignore` — if `git init`'d, ignore
  `target/` (and `Cargo.lock` is fine to keep for a binary).
- [ ] No README — a short usage note would help newcomers.
- [ ] `// use tokio;` in `src/main.rs` is a dead commented import — remove.
- [x] AI-enable repo via agent-memory (fresh enable, Mode A)

## User Preferences

(none recorded yet — record ONLY what the user explicitly states; never infer)

## Team / Members

(none recorded yet)
