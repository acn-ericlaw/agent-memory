# Agent Instructions — event_bus_demo

## What This Project Is

A small Rust learning demo of an **in-memory, async event bus**. Handlers
("functions") are decoupled from publishers — the only thing linking them is a
**route-name string**. Events are dispatched over `flume` channels and consumed by
async tasks on the `tokio` runtime. (Conceptually a miniature cousin of
route/event-flow frameworks like mercury-composable.)

**Type:** CLI / single-binary demo (not a library)
**Primary language:** Rust (edition 2021)
**Crate:** `event_bus_demo` v0.1.0
**Dependencies:** `tokio` (full features) for async runtime/tasks; `flume` for
multi-producer channels.

## Repository Structure

```
Cargo.toml        ← crate manifest (deps: tokio, flume)
Cargo.lock        ← pinned dependency graph
src/main.rs       ← entire program: Event, EventBus, run_function, main
target/            ← cargo build output (generated; not source)
```

There is a single source file. All types live in `src/main.rs`.

## Core Abstractions (src/main.rs)

- **`Event`** — `{ route: String, payload: String }`; `Debug + Clone`.
- **`EventBus`** — holds `routes: HashMap<String, Sender<Event>>`.
  - `register(route) -> Receiver<Event>` — creates an **unbounded** `flume`
    channel, stores the sender under the route, returns the receiver.
  - `send(event)` — looks up the sender by `event.route` and forwards it; prints
    `"No route found for <route>"` if the route is unregistered.
- **`run_function(name, rx)`** — async handler loop: `while let Ok(event) =
  rx.recv_async().await { ... }`. Spawned as a `tokio` task per route.
- **`main`** — `#[tokio::main]`: registers `route.a`/`route.b`, spawns a handler
  per route, sends a few events, then `sleep`s briefly so the async tasks drain.

## Conventions Observed

- Routing is by string key; publishers and subscribers share only the route name.
- Channels are unbounded (`flume::unbounded`) — no backpressure in this demo.
- Async consumption uses `recv_async().await`, not blocking `recv()`.
- Status/diagnostics go to stdout via `println!`.

## Core Rules

1. Keep the route-name decoupling — handlers should not reference each other.
2. This is a demo; favor clarity over abstraction. Don't introduce a framework.
3. Record significant decisions in the session log and `continuity.md`.

## Testing

No tests yet (`cargo test` runs nothing). The matching/dispatch logic in
`EventBus` is the natural first unit-test target if tests are added.

## Build & Run

```bash
cargo run        # build + run the demo
cargo build      # build only
cargo test       # no tests yet
```

## CI / CD

None configured. Not currently a git repository and has no `.gitignore`
(so `target/` is not ignored — see Open Threads in continuity).
