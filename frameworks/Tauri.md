# Tauri Architecture

> **Agent load:** Open Project Structure, Principles, Error Handling, Configuration, and Project Prompt / Validation first. Open other sections only when the task needs them. Read the project's `AGENTS.md`. Coding standards come from `../standards/Clean-Code/`. Reviews: `skills/review/audit/SKILL.md`. Craft: `skills/engineering/craft/SKILL.md`. Prefer extending an existing repo over scaffolding a parallel tree.

Structure for cross-platform desktop apps built with **Tauri v2**: a React and TypeScript
webview frontend over a Rust backend, connected by typed IPC. The result is a small binary with
native OS access and a web UI. The Rust core stays pure and testable, and the UI stays a thin
view. For React conventions, also see [`React-Tailwind.md`](./React-Tailwind.md).

---

## House style vs minimal

This document describes a **reference house style** for larger Tauri apps: Clean Architecture
layers in Rust, a React shell, design tokens, and a full plugin set. Take what fits the
project's size.

- **Greenfield small tool** (few commands, no complex domain): Tauri v2, typed IPC, a CSP, and
  secrets in env only. Skip the full `domain/application/infrastructure` split until complexity
  demands it (Clean-Code `classes/06`).
- **Greenfield product or complex domain:** the layered tree below.
- **Existing repo:** match what is already there. Do not re-scaffold to match this tree unless
  asked.
- **Versions** in the tables are snapshots. The project's lockfile wins when they disagree.

---

## Tech Stack

A default stack for a larger Tauri app. Swap pieces per project.

### Frontend (`package.json`)

| Package | Version | Role |
|---|---|---|
| `react` / `react-dom` | ^19 | UI |
| `@tauri-apps/api` | ^2 | IPC (`invoke`, events, window, app) |
| `@tauri-apps/plugin-opener` | ^2 | open external URLs/files |
| `framer-motion` | ^12 | dialog / toast animation |
| `recharts` | ^3 | charts (only if the app graphs data) |
| `lucide-react` | latest | icon set |
| `clsx` | ^2 | conditional classNames |
| `tailwindcss` + `@tailwindcss/vite` | ^4 | styling |
| `vite` | ^7 | dev server / bundler |

### Backend (`src-tauri/Cargo.toml`)

| Crate | Role |
|---|---|
| `tauri` v2 | app runtime, IPC, windowing |
| `tauri-plugin-log` | logging to stdout + log dir |
| `tauri-plugin-opener` | open external targets |
| `tokio` v1 (rt-multi-thread, macros, time, sync) | async tasks |
| `serde` / `serde_json` | (de)serialization across IPC |
| `thiserror` | typed error enum |
| `async-trait` | async traits for ports |
| `reqwest` (rustls, json) | outbound HTTP, **from Rust, never the webview** |

Build the crate as a `*_lib` library plus a thin `main.rs` binary. Size-optimize the release
profile with `opt-level = "s"`, `lto = true`, `panic = "abort"`, and `strip = true`.

---

## Project Structure

```
my-app/
├─ index.html                  app entry (#root)
├─ package.json                scripts + deps
├─ vite.config.ts              dev server :1420, manual vendor chunks
├─ src/                        React webview
│  ├─ main.tsx                 React root (StrictMode)
│  ├─ App.tsx                  shell: ErrorBoundary → Titlebar/Sidebar/Workspace → Toasts
│  ├─ index.css                Tailwind theme tokens, fonts, scrollbars, reduced-motion
│  ├─ types.ts                 shared TS shapes mirroring Rust DTOs
│  ├─ api/                     invoke/listen wrappers (one file per domain)
│  ├─ hooks/                   data + UI hooks
│  ├─ lib/                     pure, framework-free logic
│  ├─ pages/                   one component per tab/route
│  └─ components/
│     ├─ shared/               Titlebar, Sidebar, GlassPanel, Button, Toasts, …
│     └─ <feature>/            feature-specific components
└─ src-tauri/                  Rust backend
   ├─ Cargo.toml               crate <name>_lib + deps
   ├─ tauri.conf.json          window, CSP, bundle
   ├─ icons/                   app/installer icons
   └─ src/
      ├─ main.rs               binary → <name>_lib::run()
      ├─ lib.rs                Tauri builder: plugins, setup, invoke_handler
      ├─ state.rs              AppState wiring all adapters
      ├─ dto.rs                IPC view structs (Serialize, camelCase)
      ├─ error.rs              AppError enum
      ├─ domain/               pure logic, no I/O
      ├─ application/          use-cases + ports (traits)
      ├─ infrastructure/       adapters implementing the ports
      └─ commands/             thin #[command] handlers over AppState
```

Once features grow, organize both sides by **domain** rather than by type. Stay flat until
that becomes painful.

---

## Principles

**The webview is a view; the Rust core is the app**
All real work (I/O, system access, heavy computation) lives in Rust. The frontend renders state
and sends intent. Business rules never live in React.

**Hexagonal backend (ports and adapters)**
`application/ports.rs` defines traits, `infrastructure/` implements them, and `domain/` stays
pure. Dependencies point inward (`../standards/Principles.md` §8.2). Collaborators cross
boundaries as `Arc<dyn Trait>`, so use-cases are unit-testable with fakes
(Clean-Code `boundaries/02`).

**Thin commands**
`#[command]` functions are glue: parse arguments, call a use-case on `AppState`, map the error.
No logic in command handlers (Clean-Code `classes/04`).

**Typed IPC contract**
Every payload is a `Serialize` DTO in `dto.rs` with a matching TS type in `types.ts`. The two
files are the contract and change together.

**Single source of state**
The backend owns the truth. The frontend subscribes to events and keeps a local view, and never
invents state the backend does not know about (Clean-Code 14).

---

## Backend (Rust, `src-tauri/src`)

### Entry and wiring

- **`main.rs`:** `#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]` (no
  console window in release), then calls `<name>_lib::run()`.
- **`lib.rs`:** `run()` builds the Tauri app. It registers plugins (`opener`, and `log` to stdout
  and the log dir), constructs `AppState` in `setup`, calls `app.manage(state)`, and registers
  the `invoke_handler` with every command.
- **`state.rs`:** `AppState` holds each use-case behind an `Arc`. Build it once at startup and
  inject it into commands via `tauri::State`.

### Layers

- **`domain/`:** pure, dependency-free logic and value types. No I/O, no Tauri, no `async`. The
  most heavily unit-tested layer.
- **`application/`:** use-cases that orchestrate the domain through ports. Owns long-running
  tasks and in-memory caches.
- **`application/ports.rs`:** the trait boundary (`trait Store`, `trait HttpClient`,
  `trait EventSink`, and so on), plus the value types they exchange.
- **`infrastructure/`:** concrete adapters implementing the ports (a file store, an HTTP client
  via `reqwest`, a Tauri event emitter). The only layer that knows about the outside world.
- **`commands/`:** Tauri `#[command]` functions. Thin handlers calling `AppState`.

### Ports and adapters example

`find` returns `Option` because a missing key is a normal outcome, and Rust forces every caller
to handle it (Clean-Code 13). I/O failure is a separate `Err`.

```rust
// application/ports.rs: the boundary
#[async_trait::async_trait]
pub trait Store: Send + Sync {
    async fn find(&self, key: &str) -> Result<Option<String>, AppError>;
    async fn save(&self, key: &str, value: &str) -> Result<(), AppError>;
}

// infrastructure/json_store.rs: one adapter
pub struct JsonStore { path: PathBuf }

#[async_trait::async_trait]
impl Store for JsonStore {
    async fn save(&self, key: &str, value: &str) -> Result<(), AppError> {
        // write to `${path}.tmp` then rename, so a crash never leaves a half-written file
        atomic_write(&self.path, key, value).await
    }
    // ...
}
```

### Async tasks

Long-running work (watchers, pollers, pipelines) runs on `tokio` tasks spawned from a use-case.
Tasks communicate over bounded channels and push results to the frontend through an
`EventSink` port. Each task holds a `StopToken` (an `Arc<AtomicBool>`) so the command layer can
stop it cleanly.

---

## IPC

There are two directions: the frontend **calls** commands, and the backend **emits** events.

### Commands (frontend → backend)

```rust
#[tauri::command]
async fn save_note(
    state: tauri::State<'_, AppState>,
    id: String,
    body: String,
) -> Result<(), String> {
    state.notes.save(&id, &body).await.map_err(|e| e.to_string())
}
```

```typescript
// src/api/notes.ts
import { invoke } from '@tauri-apps/api/core';

export function saveNote(id: string, body: string): Promise<void> {
  return invoke('save_note', { id, body });
}
```

### Events (backend → frontend)

Namespace channels as `domain://action`. The backend emits through an `EventSink` adapter, and
the frontend subscribes through a typed wrapper.

```typescript
// src/api/events.ts
import { listen } from '@tauri-apps/api/event';
import type { NoteView } from '../types';

export const onNoteSaved = (callback: (note: NoteView) => void) =>
  listen<NoteView>('notes://saved', (event) => callback(event.payload));
```

### Shared shapes

`dto.rs` (`#[derive(Serialize)]`, `#[serde(rename_all = "camelCase")]`) and `types.ts` mirror
each other field for field and change together.

---

## Frontend (React, `src/`)

### Shell

```
<ErrorBoundary>
  <div h-screen flex-col>
    <Titlebar/>                       ← frameless drag region + window controls
    <div flex flex-1>
      <Sidebar tab onSelect/>
      <main p-6><Workspace tab/></main>
    </div>
  </div>
  <ToastContainer/>                    ← fixed bottom-right
</ErrorBoundary>
```

`App.tsx` holds the active `tab` and composes the data layer once, passing it down.
`Workspace` maps the `Tab` string union to a page component through a lookup table; a
single-window app does not need a router library.

### State management

No Redux or context-heavy store. Use **local hooks plus module-level external stores** via
`useSyncExternalStore` for cross-cutting state such as toasts. A top-level hook composes the
data layer:

```typescript
function useApp() {
  // subscribe to backend events, keep a local view, expose actions
  const notes = useNotes();      // listens to notes://*, exposes save/delete
  return { notes };
}
```

- One hook per backend domain. Each owns its events and its `invoke` calls.
- Small UI preferences persist in `localStorage` under namespaced keys such as
  `app.selection`.
- The wrappers in `src/api/` are the only place that calls `invoke` or `listen`
  (Clean-Code 31).

---

## Design System

A reusable dark, glassmorphic system. Tokens live in `index.css` under `@theme`. The accent is
violet by default; changing `--color-primary` rebrands the rest.

### Window shell (`tauri.conf.json`)

Frameless (`decorations: false`), for example `1180×760` with a minimum of `960×640`, centered,
resizable, with an opaque `#080810` background. A custom `Titlebar` provides the drag region
(`data-tauri-drag-region`) and Minimize and Close controls via `getCurrentWindow()`.

### Color tokens (`index.css` `@theme`)

| Token | Value | Use |
|---|---|---|
| `--color-bg` | `#080810` | app background |
| `--color-surface` | `rgba(10,10,20,0.7)` | panels |
| `--color-surface-alt` | `#0e0e1a` | menus, dialogs, tooltips |
| `--color-border` / `-subtle` | white 8% / 5% | borders |
| `--color-primary` / `-bright` | `#7c3aed` / `#8b5cf6` | accent |
| `--color-accent-light` | `#a78bfa` | highlights, group labels |
| `--color-danger/success/warning/info` | red/emerald/amber/blue | status |
| `--shadow-sm/md/lg/glow` | (project-defined) | elevation + accent glow |

Text is tinted with white opacity: primary about 95%, secondary 70%, muted 45%.

### Typography

A geometric sans (for example **Plus Jakarta Sans**, weights 300-700) as `--font-sans`. The
recurring label style is `text-[10px] font-medium uppercase tracking-wider text-white/40`,
used consistently.

### Surfaces and shape

Glassmorphism comes from translucent fills (`bg-white/2`) and hairline borders
(`border-white/5-10`) with `backdrop-blur-xl`. Panels use `rounded-2xl`, cards and inputs
`rounded-lg` or `rounded-xl`, and pills `rounded-full`. The `GlassPanel` primitive
(`rounded-2xl border-white/8 bg-white/2 backdrop-blur-xl`) is the base surface.

### Iconography

`lucide-react`, sized consistently (16-20px) and tinted to the text opacity scale. Window and
installer icons live in `src-tauri/icons/`.

### Interaction polish (`index.css`)

- Global `user-select: none` for an app feel, re-enabled on inputs, `textarea`, and
  `contenteditable`.
- `:focus-visible` draws the accent ring (`0 0 0 2px rgba(139,92,246,0.5)`); mouse focus does
  not.
- Thin custom scrollbars (white 10%, 20% on hover). Image dragging disabled.

### Motion

| Where | Tech | Behavior |
|---|---|---|
| Dialogs | framer-motion | `scale 0.96→1` + `opacity 0→1` over a dimmed backdrop |
| Toasts | framer-motion | slide-up fade + `layout` reflow of the stack |
| Charts | recharts | area draws over ~400ms linear |
| Hover/nav/buttons | Tailwind | `transition-colors duration-150` |

**Reduced motion is non-negotiable.** A global `@media (prefers-reduced-motion: reduce)` rule
forces near-zero durations, and any `requestAnimationFrame` canvas effect checks
`matchMedia('(prefers-reduced-motion: reduce)')` and skips the animation.

---

## Error Handling

Errors pass through three layers, each translating for the next (`../standards/Principles.md`
§5, and `skills/engineering/errors/SKILL.md` for user-facing copy).

**Rust: one typed error enum**

```rust
#[derive(Debug, thiserror::Error)]
pub enum AppError {
    #[error("validation: {0}")] Validation(String),
    #[error("storage: {0}")]    Storage(String),
    #[error("network: {0}")]    Network(String),
}
```

Domain code and use-cases return `Result<T, AppError>` with context (which operation, which id).
Commands map it once at the boundary with `.map_err(|e| e.to_string())`, so the frontend
receives a string rather than a panic. A panic crashes the webview, so **never `unwrap()` or
`expect()` on a command path**.

**Frontend: render errors vs async errors**

- **Render errors:** an `ErrorBoundary` class component shows fallback UI.
- **Async and IPC errors:** boundaries do not catch these. Catch the `invoke` failure, log the
  technical detail, and show the user a translated message (what, why, action), never the raw
  `AppError` string.

```typescript
try {
  await saveNote(id, body);
} catch (error) {
  console.error(`saveNote failed for note ${id}:`, error);
  toast("Your note wasn't saved because the app couldn't write to disk. Check free space, then try again.", 'error');
}
```

---

## Testing

**Rust: unit-test the pure layers**

`domain/` has no I/O, so it tests directly. Use-cases test against **fake adapters** that
implement the ports, with no real files, network, or Tauri.

```rust
#[cfg(test)]
mod tests {
    use super::*;

    struct FakeStore;
    #[async_trait::async_trait]
    impl Store for FakeStore {
        async fn find(&self, _: &str) -> Result<Option<String>, AppError> { Ok(None) }
        async fn save(&self, _: &str, _: &str) -> Result<(), AppError> { Ok(()) }
    }

    #[tokio::test]
    async fn saves_a_valid_note() {
        let notes = Notes::new(Arc::new(FakeStore));
        assert!(notes.save("1", "hello").await.is_ok());
    }
}
```

Run with `cargo test`. Keep tests fast and self-validating (Clean-Code `unit-tests/06`).

**Frontend: logic, not chrome**

Test hooks and pure `lib/` functions with Vitest, and **stub the Tauri API** so nothing hits IPC:

```typescript
vi.mock('@tauri-apps/api/core', () => ({ invoke: vi.fn() }));
```

Check the thin `api/` wrappers and visual chrome manually in `tauri dev`.

---

## Configuration

Configuration is split across `tauri.conf.json`, the Rust backend, and per-user data. Keep the
three distinct.

### `tauri.conf.json`

- **Window:** size, minimum size, `decorations: false`, background color.
- **CSP:** locked down. `default-src 'self'`; allow `data:` and `asset:` for images, the font
  host for styles, and `connect-src 'self' ipc: http://ipc.localhost` for IPC. The webview talks
  **only** IPC. Outbound HTTP goes through Rust (`reqwest`), which the webview CSP does not
  govern.
- **Bundle:** a reverse-DNS `identifier` (for example `dev.you.app`) and targets (msi, nsis,
  deb, appimage, dmg).

### Secrets and env

API keys and tokens live in the **Rust** process, read from the environment at run time, and
are **never bundled into the webview**, where any user can read them. Expose only results over
IPC. Commit a `.env.example` and gitignore the real `.env`.

### Per-user data

Persist under `app_data_dir()` (via `tauri::Manager::path`), never next to the binary, which may
be read-only. Write atomically (`.tmp` plus rename). A missing file is a normal first run. A file
that exists but is malformed is a failure: keep the original (rename it to `*.corrupt`), tell
the user what happened and what to do, and never silently replace it with defaults
(Clean-Code 34). Small UI preferences can stay in the webview's `localStorage`.

---

## Summary

- **Rust owns the app; the webview renders it.** No business logic in React.
- **Hexagonal backend:** pure `domain/`, use-cases and ports in `application/`, adapters in
  `infrastructure/`, thin `commands/`, with `Arc<dyn Trait>` injection for testability.
- **Typed IPC:** `dto.rs` and `types.ts` in lockstep, with namespaced `domain://` events.
- **One `AppError` enum,** mapped to `String` at the command boundary. No `unwrap()` on a
  command path.
- **Design system** in `@theme` tokens: dark glassmorphism, swappable accent, mandatory
  reduced-motion support.
- **Locked CSP,** secrets and HTTP in Rust, per-user data under `app_data_dir()` with atomic
  writes.

---

## Project Prompt

Build a Tauri v2 desktop app with React and TypeScript in the webview and Rust in the backend,
following the structure and rules above. This file decides framework structure and idiom;
coding standards come from `../standards/Clean-Code/`, which wins on any conflict. Open the
sections of `../standards/Principles.md` the task needs.

**Architecture**
- Hexagonal Rust backend: pure `domain/`, use-cases and ports in `application/`, adapters in
  `infrastructure/`, thin `commands/`
- Dependencies point inward; collaborators cross boundaries as `Arc<dyn Trait>`
- The webview stays a thin view; all real work lives in Rust

**IPC**
- Typed DTOs in `dto.rs` mirrored by `types.ts`
- Thin `#[command]` handlers and namespaced `domain://` events
- All `invoke` and `listen` calls isolated in `src/api/`

**Error Handling**
- One `AppError` enum (`thiserror`) mapped to `String` at the command boundary
- No `unwrap()` or `expect()` on a command path
- `ErrorBoundary` for render errors; logged, translated toasts for async and IPC errors

**Security**
- Strict CSP; the webview talks only IPC
- Outbound HTTP and secrets stay in Rust
- Per-user data under `app_data_dir()`, written atomically

### Setup

```bash
npm create tauri-app@latest          # React + TypeScript template
cd my-app
npm install
npm run tauri dev                    # Vite (:1420) + Rust app, hot-reload
```

### Deliverables

1. A complete project following the structure above
2. A hexagonal Rust backend (domain, application plus ports, infrastructure, commands)
3. `AppState` wiring adapters at startup
4. Typed IPC with `dto.rs` and `types.ts`, plus namespaced events
5. A React shell (Titlebar, Sidebar, Workspace) with hook-based state
6. Design-system tokens in `index.css` plus a `GlassPanel` primitive
7. An `AppError` enum, an `ErrorBoundary`, and toast feedback
8. A locked-down `tauri.conf.json` (window, CSP, bundle)
9. A README with setup and build instructions
10. Rust unit tests for domain and use-cases, and frontend hook tests

### Validation Checklist

- [ ] Verify commands from the project's AGENTS.md or README run (or honest manual checks are listed)
- [ ] No secrets committed; env examples use placeholders only
- [ ] Functions do one thing at one level of abstraction (Clean-Code 15, 27)
- [ ] No business logic in the webview or in command handlers
- [ ] No `unwrap()` or `expect()` on a command path
- [ ] Every IPC payload is a typed DTO mirrored in `types.ts`
- [ ] CSP locked down; no secrets in the webview
- [ ] Per-user data under `app_data_dir()`, written atomically; malformed files never silently replaced
- [ ] `prefers-reduced-motion` respected
- [ ] Domain and use-cases unit-tested with fake adapters
- [ ] Names match the domain and local convention (Clean-Code 06)
- [ ] `cargo clippy` and `tsc` are clean

### Pre-Delivery

```bash
cargo fmt --check && cargo clippy -- -D warnings   # Rust clean
cargo test                                         # backend tests pass
npm run build                                      # tsc + vite build, no errors
npm test                                           # frontend tests pass
npm run tauri build                                # production bundles
```
