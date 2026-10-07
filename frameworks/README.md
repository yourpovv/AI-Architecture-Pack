# frameworks/ index

These are your framework conventions. They sit on top of a language file. You always load a
[`../languages/*`](../languages/README.md) file as well, because these rules assume your language
rules are already in play.

| File | Use it for | Pair with |
|---|---|---|
| **[React-Tailwind.md](./React-Tailwind.md)** | Web UI: components, custom hooks, state, Tailwind patterns | `TypeScript.md` |
| **[Tauri.md](./Tauri.md)** | Desktop apps with a Rust backend and a web frontend. Small binaries, real system access | `TypeScript.md` |
| **[Electron.md](./Electron.md)** | Desktop apps where you want the whole Chromium runtime. Main process, preload bridge, IPC | `TypeScript.md` |
| **[Valkyrie.md](./Valkyrie.md)** | Desktop apps on the system WebView. Roughly 2 MB binaries instead of Electron's 150 to 300 MB | `TypeScript.md` |
| **[Dear-ImGui.md](./Dear-ImGui.md)** | Native tool UIs: profilers, editors, overlays, control panels. Immediate mode with a hand-drawn widget kit | `Cpp.md` |

## Choosing a desktop framework

| You want | Take |
|---|---|
| Native performance, small binary, Rust backend | Tauri |
| Node APIs in the main process and a mature plugin ecosystem | Electron |
| The smallest possible binary and a CLI-driven build | Valkyrie |

You read `Tauri.md` and its **house style vs minimal** near the top before you
start. Why? It decides how opinionated your generated UI will be.

## After you ship

`../prompts/reviews/Tauri-QC.md` is your one framework-specific review prompt in this pack.
Everything else under `../prompts/reviews/` is stack-neutral. You can use those reviews here too.

## Adding a framework

1. You copy the closest existing file.
2. You state which language file yours assumes in your first paragraph.
3. You keep the **Agent load** blockquote at the top.
4. You cover what your framework changes, not what your language already covers. Duplication
   between layers is how your two layers drift apart.
5. You add a row to the table above.
