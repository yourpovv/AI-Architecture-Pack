# frameworks/ index

These are your framework conventions. They do not stand alone. You always load a
[`../languages/*`](../languages/README.md) file with them. Your language rules come first. They are the foundation. These rules sit on top of that foundation. You read both. You follow both.

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
start. Why does that choice matter? It decides how opinionated your generated UI will be. You make that call early. You do not drift into it.

## After you ship

`../prompts/reviews/Tauri-QC.md` is your one framework-specific review prompt in this pack.
Everything else under `../prompts/reviews/` is stack-neutral. A good review is a habit. It is not a phase. You use those reviews here too.

## Adding a framework

1. You copy the closest existing file. You do not start from a blank page. You build on what your team already trusts.
2. You state which language file yours assumes in your first paragraph. You make that debt plain. Your reader should see the pairing at once.
3. You keep the **Agent load** blockquote at the top. It tells your reader where to start. You respect your reader's time.
4. You cover what your framework changes. You do not repeat what your language already covers. Duplication lets your two layers drift apart. You keep one truth in one place.
5. You add a row to the table above. You keep the index honest. If it is not in the index, your teammate will not find it.
