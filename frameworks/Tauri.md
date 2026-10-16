# Tauri Architecture

> **Agent load:** You open Project Structure, Principles, Error Handling, Configuration, and Project Prompt / Validation first. You open other sections only when your task needs them. You pair with the matching `languages/*` file and project `AGENTS.md`. Reviews: `skills/review/audit/SKILL.md`. Craft: `skills/engineering/craft/SKILL.md`. You prefer extending an existing repo over scaffolding a parallel tree.

You keep a clean structure for cross-platform desktop apps with **Tauri v2**, a React + TypeScript
webview frontend over a Rust backend, talking through typed IPC. You get small binaries. You get native
OS access. You get a web UI. You layer it so your Rust core stays pure and testable and your UI stays a
thin view. Why mix what you can keep clean?

---

## House style vs minimal

This document describes a **reference house style** used on larger Tauri apps. You get Clean Architecture layers on the Rust side. You get a React shell. You get design tokens. You get a full plugin set. You take what fits your size.

- **Greenfield small tool** (few commands, no complex domain): you use Tauri v2 + typed IPC + CSP + secrets in env only. You skip full `domain/application/infrastructure` until complexity demands it.
- **Greenfield product / complex domain**: the layered tree below fits your needs.
- **Existing repo**: you match what is already there. You do not re-scaffold to match this tree unless asked.
- **Versions** in the tables are snapshots, not eternal pins. You prefer the project's lockfile over this doc when they disagree.

---

## Tech Stack

This is a solid default stack for your larger Tauri app. You swap pieces per project. You treat versions as guidance. Your project lockfiles win.

### Frontend (`package.json`)

| Package | Version | Role |
|---|---|---|
| `react` / `react-dom` | ^19 | UI |
| `@tauri-apps/api` | ^2 | IPC (`invoke`, events, window, app) |
| `@tauri-apps/plugin-opener` | ^2 | open external URLs/files |
| `framer-motion` | ^12 | dialog / toast animation |
| `recharts` | ^3 | charts (add only if you graph data) |
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

You keep the crate as a `*_lib` library plus a thin `main.rs` binary. You size-optimize your
release profile with `opt-level = "s"`, `lto = true`, `panic = "abort"`, `strip = true`. You pay for size once in config. You gain it on every ship.

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
│  ├─ utils/                   pure helpers
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

You organize both sides by **domain**, not by type, once your feature grows. You keep it flat until
that hurts. Flat is honest until it is not.

---

## Principles

**The webview is a view, the Rust core is the app**
All your real work, your I/O, your system access, your heavy compute, lives in Rust. Your frontend renders
state and sends intent. You never put business rules in React that Rust should own. Why let your view think for your app?

**Hexagonal backend (ports & adapters)**
`application/ports.rs` defines traits. `infrastructure/` implements them. `domain/` stays
pure. Your dependencies point **inward** (`../standards/Principles.md` §8.2). Everything crosses
boundaries as `Arc<dyn Trait>`. That is how your use-cases stay unit-testable with fakes.

**Thin commands**
Your `#[command]` functions are glue. You parse args. You call a use-case on `AppState`. You map the error.
You keep no logic in your command handlers.

**Typed IPC contract**
Every payload is a `Serialize` DTO in `dto.rs` with a matching TS type in `types.ts`. Your
two files are the contract. You keep them in lockstep.

**Single source of state**
Your backend owns the truth. Your frontend subscribes to events and keeps a local view. It never invents state your backend does not know about.

---

## Backend (Rust, `src-tauri/src`)

### Entry & wiring

- **`main.rs`**, `#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]`
  (no console window in release). You call `<name>_lib::run()`.
- **`lib.rs`**, `run()` builds your Tauri app. It registers plugins (`opener`, `log` → stdout
  + log dir). It constructs `AppState` in `setup`. It calls `app.manage(state)`. It registers
  the `invoke_handler` with every command.
- **`state.rs`**, `AppState` holds each use-case behind an `Arc`. You build it once at startup.
  You inject it into commands via `tauri::State`.

### Layers

- **`domain/`**, your pure, dependency-free logic and value types. No I/O, no Tauri, no
  `async`. Your most heavily unit-tested layer.
- **`application/`**, your use-cases that orchestrate the domain through ports. It owns
  long-running tasks and in-memory caches.
- **`application/ports.rs`**, your trait boundary with `trait Store`, `trait HttpClient`,
  `trait EventSink`, etc., plus the request and response value types they exchange.
- **`infrastructure/`**, your concrete adapters implementing the ports (a file store, an HTTP
  client via `reqwest`, a Tauri event emitter). The only layer that knows about the
  outside world.
- **`commands/`**, your Tauri `#[command]` functions. Thin handlers calling `AppState`.

### Ports & adapters example

```rust
// application/ports.rs, the boundary
#[async_trait::async_trait]
pub trait Store: Send + Sync {
    async fn load(&self, key: &str) -> Result<Option<String>, AppError>;
    async fn save(&self, key: &str, value: &str) -> Result<(), AppError>;
}

// infrastructure/json_store.rs, one adapter
pub struct JsonStore { path: PathBuf }

#[async_trait::async_trait]
impl Store for JsonStore {
    async fn save(&self, key: &str, value: &str) -> Result<(), AppError> {
        // write to `${path}.tmp` then atomic rename, never a half-written file
        atomic_write(&self.path, key, value).await
    }
    // ...
}
```

### Async tasks

Your long-running work (watchers, pollers, pipelines) runs on `tokio` tasks spawned from a
use-case. It talks over bounded channels and pushes results to your frontend via an
`EventSink` port. You hold a `StopToken` (an `Arc<AtomicBool>`) so your command layer can stop
them cleanly. You start what you can stop.

---

## IPC

You have two directions. Your frontend **calls** commands. Your backend **emits** events.

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

You namespace channels `domain://action`. Your backend emits via an `EventSink` adapter. Your
frontend subscribes through a typed wrapper.

```typescript
// src/api/events.ts
import { listen } from '@tauri-apps/api/event';
import type { NoteView } from '../types';

export const onNoteSaved = (cb: (note: NoteView) => void) =>
  listen<NoteView>('notes://saved', (e) => cb(e.payload));
```

### Shared shapes

`dto.rs` (`#[derive(Serialize)]`, `#[serde(rename_all = "camelCase")]`) ↔ `types.ts`.
They mirror each other field-for-field. You change them together.

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

Your `App.tsx` holds the active `tab` and composes the data layer once, passing it down.
Your `Workspace` switches on a `Tab` string union, no router library for a single-window app. Keep it plain until you need more.

### State management

You keep no Redux or Context-heavy store. You use **local hooks + module-level external stores** via
`useSyncExternalStore` for cross-cutting state (e.g. toasts). Your top-level hook composes
your data layer:

```typescript
function useApp() {
  // subscribe to backend events, keep a local view, expose actions
  const notes = useNotes();      // listens to notes://* , exposes save/delete
  return { notes };
}
```

- You keep one hook per backend domain. Each owns its events and the `invoke` calls.
- You persist small UI preferences in `localStorage` (namespaced keys like `app.selection`).
- Your API wrappers in `src/api/` are the only place that calls `invoke` / `listen`. You keep that door narrow.

---

## Design System

You use a reusable dark, glassmorphic system. Your tokens live in `index.css` (`@theme`). Your accent is
violet by default. You swap `--color-primary` for any brand and the rest follows.

### Window shell (`tauri.conf.json`)

You go frameless (`decorations: false`), e.g. `1180×760`, min `960×640`, centered, resizable,
opaque background `#080810`. Your custom `Titlebar` provides the drag region (`data-tauri-drag-region`)
and Minimize and Close controls via `getCurrentWindow()`.

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
| `--shadow-sm/md/lg/glow` |, | elevation + accent glow |

You tint text via white opacity. Primary `~95%`. Secondary `70%`. Muted `45%`. You keep that scale honest.

### Typography

You use a geometric sans (e.g. **Plus Jakarta Sans**, weights 300-700) as `--font-sans`. Your recurring
label micro-style is `text-[10px] font-medium uppercase tracking-wider text-white/40`. You use it the same way every time.

### Surfaces & shape

You build glassmorphism from translucent fills (`bg-white/2`) and hairline borders (`border-white/5-10`) with
`backdrop-blur-xl`. You use panels `rounded-2xl`, cards and inputs `rounded-lg` and `rounded-xl`, and
pills `rounded-full`. Your `GlassPanel` primitive (`rounded-2xl border-white/8 bg-white/2
backdrop-blur-xl`) is your base surface.

### Iconography

You use `lucide-react`, sized consistently (16-20px), tinted to your text opacity scale. Your window and
installer icons live in `src-tauri/icons/`. You keep icons quiet and consistent.

### Interaction polish (`index.css`)

- You set global `user-select: none` for app feel. You re-enable on inputs, `textarea`, and
  `contenteditable`.
- You use `:focus-visible` for your accent ring (`0 0 0 2px rgba(139,92,246,0.5)`). You suppress it for mouse
  focus.
- You use custom thin scrollbars (white 10%, 20% on hover). You disable `img` drag.

### Motion

| Where | Tech | Behavior |
|---|---|---|
| Dialogs | framer-motion | `scale 0.96→1` + `opacity 0→1` over a dimmed backdrop |
| Toasts | framer-motion | slide-up fade + `layout` reflow of the stack |
| Charts | recharts | area draws over ~400ms linear |
| Hover/nav/buttons | Tailwind | `transition-colors duration-150` |

**Reduced motion is non-negotiable.** You set a global `@media (prefers-reduced-motion: reduce)`
rule that forces near-zero durations. Any `requestAnimationFrame` canvas effect of yours must check
`matchMedia('(prefers-reduced-motion: reduce)')` and bail. You respect your user.

---

## Error Handling

You work in three layers, each translating to the next (`../standards/Principles.md` §5, and `skills/engineering/errors/SKILL.md`
for user copy). You keep each layer honest:

**Rust, one typed error enum**

```rust
#[derive(Debug, thiserror::Error)]
pub enum AppError {
    #[error("validation: {0}")] Validation(String),
    #[error("storage: {0}")]    Storage(String),
    #[error("network: {0}")]    Network(String),
}
```

Your domain and use-cases return `Result<T, AppError>` with context. Your commands map it at the
boundary with `.map_err(|e| e.to_string())`. Your frontend receives a string, never a panic. A
panic crashes your webview, so you **never `unwrap()` in a command path**.

**Frontend, render vs async errors**

- **Render errors** → an `ErrorBoundary` (class component) shows fallback UI. You contain the render failure.
- **Async / IPC errors** → boundaries do not catch these. You `try/catch` the `invoke`. You put the
  message in state. You surface it as a toast or inline, translated for your user, not the
  raw `AppError` string.

```typescript
try {
  await saveNote(id, body);
} catch {
  toast('Couldn’t save your note. Try again in a moment.', 'error');
}
```

---

## Testing

**Rust, unit-test the pure layers**

Your `domain/` has no I/O, so it tests directly. Your use-cases test against **fake adapters**
implementing the ports, with no real files, no network, and no Tauri.

```rust
#[cfg(test)]
mod tests {
    use super::*;

    struct FakeStore;
    #[async_trait::async_trait]
    impl Store for FakeStore {
        async fn load(&self, _: &str) -> Result<Option<String>, AppError> { Ok(None) }
        async fn save(&self, _: &str, _: &str) -> Result<(), AppError> { Ok(()) }
    }

    #[tokio::test]
    async fn saves_a_valid_note() {
        let notes = Notes::new(Arc::new(FakeStore));
        assert!(notes.save("1", "hello").await.is_ok());
    }
}
```

You run with `cargo test`. You keep tests **fast and self-validating** (`../standards/Principles.md` §9.2). Slow tests lie to you. Fast tests tell the truth.

**Frontend, logic, not chrome**

You test hooks and pure utils with Vitest. You **stub the Tauri API** so nothing hits IPC:

```typescript
vi.mock('@tauri-apps/api/core', () => ({ invoke: vi.fn() }));
```

You leave the thin `api/` wrappers and visual chrome to manual checks in `tauri dev`. You look at what you cannot automate.

---

## Configuration

Your config splits across `tauri.conf.json`, your Rust backend, and per-user data. You keep them
distinct. Mixing them will hurt you.

### `tauri.conf.json`

- **Window**, size, min size, `decorations: false`, background color. You state it plainly.
- **CSP**, you lock it down. You set `default-src 'self'`. You allow `data:` and `asset:` for images, your
  font host for styles, and `connect-src 'self' ipc: http://ipc.localhost` for IPC. Your
  webview talks **only IPC**. You make outbound HTTP from Rust (`reqwest`), which is not
  subject to the webview CSP.
- **Bundle**, you set a reverse-DNS `identifier` (e.g. `dev.you.app`) and targets (msi, nsis,
  deb, appimage, dmg).

### Secrets & env

Your API keys and tokens live in your **Rust** process, read from the environment at run time, **never bundled into the webview**, where any user can read them. You expose only results over
IPC. You commit a `.env.example`. You gitignore your real `.env`.

### Per-user data

You persist under `app_data_dir()` (via `tauri::Manager::path`), never next to the binary
(which may be read-only). You write atomically (`.tmp` plus rename) and you ignore malformed files
with a warning rather than crashing. Your small UI prefs can stay in your webview
`localStorage`.

---

## Summary

- **Rust owns the app. The webview renders it.** You keep no business logic in React.
- **Hexagonal backend**, your pure `domain/`, your use-cases and ports in `application/`, your adapters in
  `infrastructure/`, your thin `commands/`. You inject `Arc<dyn Trait>` for testability.
- **Typed IPC**, your `dto.rs` ↔ `types.ts`, kept in lockstep, with namespaced `domain://` events.
- **One `AppError` enum** mapped to `String` at the command boundary. You never call `unwrap()` in a
  command.
- **Design system** in `@theme` tokens, dark glassmorphism, swappable accent, mandatory
  reduced-motion support. You honor it.
- **You lock the CSP**, you keep secrets and HTTP in Rust, you persist under `app_data_dir()` with
  atomic writes.

---

## Project Prompt

You build a Tauri v2 desktop app with React and TypeScript in the webview and Rust in the backend.
You follow the structure and rules above. Where they disagree with your defaults, this file
wins. You obey it.

You read `../standards/Principles.md` alongside this file before starting. You know your standards before you cut.

**Architecture**
- You keep a hexagonal Rust backend with pure `domain/`, use-cases and ports in `application/`, adapters in
  `infrastructure/`, and thin `commands/`
- Your dependencies point inward. You cross boundaries as `Arc<dyn Trait>`
- Your webview stays a thin view. All real work lives in Rust

**IPC**
- You keep typed DTOs in `dto.rs` mirrored by `types.ts`
- You keep thin `#[command]` handlers with namespaced `domain://` events
- You isolate all `invoke` and `listen` calls in `src/api/`

**Error Handling**
- You keep one `AppError` enum (`thiserror`) mapped to `String` at the command boundary
- You never call `unwrap()` on a command path
- You use `ErrorBoundary` for render errors and state plus toasts for async and IPC errors

**Security**
- You keep a strict CSP. Your webview talks only IPC
- Your outbound HTTP and secrets stay in Rust, never in the webview
- You keep per-user data under `app_data_dir()`, written atomically

### Setup

```bash
npm create tauri-app@latest          # React + TypeScript template
cd my-app
npm install
npm run tauri dev                    # Vite (:1420) + Rust app, hot-reload
```

### Deliverables

1. You deliver a complete project following the structure above
2. You deliver a hexagonal Rust backend (domain, application plus ports, infrastructure, commands)
3. You deliver `AppState` wiring adapters at startup
4. You deliver typed IPC with `dto.rs` ↔ `types.ts` and namespaced events
5. You deliver a React shell (Titlebar, Sidebar, Workspace) with hook-based state
6. You deliver design-system tokens in `index.css` plus a `GlassPanel` primitive
7. You deliver an `AppError` enum plus `ErrorBoundary` plus toast feedback
8. You deliver a locked-down `tauri.conf.json` (window, CSP, bundle)
9. You deliver a README with setup and build instructions
10. You deliver Rust unit tests for domain plus use-cases and frontend hook tests

### Validation Checklist

- [ ] You verify commands from project AGENTS.md / README run (or you list honest manual checks)
- [ ] You commit no secrets. Your env examples use placeholders only
- [ ] Your functions stay small and single-purpose. You extract when a second concern appears (see Principles / skills/engineering/craft/SKILL.md)
- [ ] You keep no business logic in the webview or in command handlers
- [ ] You use no `unwrap()` and no `expect()` on a command path
- [ ] Every IPC payload of yours is a typed DTO mirrored in `types.ts`
- [ ] You lock down the CSP. You keep no secrets in the webview
- [ ] You keep per-user data under `app_data_dir()`, written atomically
- [ ] You respect `prefers-reduced-motion`
- [ ] You unit-test domain plus use-cases with fake adapters
- [ ] Names match domain and local convention (skills/engineering/craft/SKILL.md)
- [ ] `cargo clippy` and `tsc` stay clean

### Pre-Delivery

```bash
cargo fmt --check && cargo clippy -- -D warnings   # Rust clean
cargo test                                         # backend tests pass
npm run build                                      # tsc + vite build, no errors
npm test                                           # frontend tests pass
npm run tauri build                                # production bundles
```
