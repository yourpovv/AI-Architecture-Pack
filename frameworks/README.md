# frameworks/ index

Framework conventions. Each file covers what its framework changes; the language-agnostic
coding standard always comes from [`../standards/Clean-Code/`](../standards/Clean-Code/README.md),
which wins on any conflict. A framework file decides structure, idiom, and syntax only.

| File | Use it for | Code examples in |
|---|---|---|
| **[React-Tailwind.md](./React-Tailwind.md)** | Web UI: components, custom hooks, state, Tailwind patterns | TypeScript |
| **[Tauri.md](./Tauri.md)** | Desktop apps with a Rust backend and a web frontend. Small binaries, real system access | Rust + TypeScript |
| **[Electron.md](./Electron.md)** | Desktop apps that want the whole Chromium runtime. Main process, preload bridge, IPC | JavaScript |
| **[Valkyrie.md](./Valkyrie.md)** | Desktop apps on the system WebView. Roughly 2 MB binaries instead of Electron's 150 to 300 MB | JavaScript |
| **[Dear-ImGui.md](./Dear-ImGui.md)** | Native tool UIs: profilers, editors, overlays, control panels. Immediate mode with a hand-drawn widget kit | C++ |

## Choosing a desktop framework

| You want | Take |
|---|---|
| Native performance, small binary, Rust backend | Tauri |
| Node APIs in the main process and a mature plugin ecosystem | Electron |
| The smallest possible binary and a CLI-driven build | Valkyrie |
| A native tool UI that owns its frame loop | Dear ImGui |

Before starting a Tauri app, read the **House style vs minimal** section near the top of
`Tauri.md`. It decides how opinionated the generated app will be, so make that call
deliberately at the start.

## After shipping

`../prompts/reviews/Tauri-QC.md` is the one framework-specific review prompt in this pack. The
rest of `../prompts/reviews/` is stack-neutral and applies to every framework here.

## Adding a framework

1. Copy the closest existing file rather than starting from a blank page.
2. State in the first paragraph which language the code examples use.
3. Keep the **Agent load** blockquote at the top so the reader knows where to start.
4. Cover only what the framework changes. Coding rules belong in `../standards/Clean-Code/`;
   repeating them here lets the two drift apart.
5. Add a row to the table above. A file missing from the index never gets loaded.
