# Valkyrie Architecture

> **Agent load:** Open Project Structure, Principles, Error Handling, Configuration, and Project Prompt / Validation first. Open other sections only when the task needs them. Read the project's `AGENTS.md`. Coding standards come from `../standards/Clean-Code/`. Reviews: `skills/review/audit/SKILL.md`. Craft: `skills/engineering/craft/SKILL.md`. Prefer extending an existing repo over scaffolding a parallel tree.

Structure for a lightweight desktop app built with Valkyrie. Code examples are JavaScript ES
modules.

---

## What is Valkyrie?

Valkyrie is a CLI-driven desktop framework that uses the system WebView (webkit2gtk on Linux,
Edge WebView2 on Windows) instead of bundling Chromium. Binaries are around 2 MB instead of
Electron's 150-300 MB. The cost is that rendering depends on whichever WebView the OS provides.

| Framework | Binary Size |
|-----------|-------------|
| Electron  | 150-300 MB  |
| Tauri     | 10-20 MB    |
| Valkyrie  | ~2 MB       |

---

## Project Structure

```
my-app/
├── index.html          # Entry point / shell
├── app.js              # App bootstrap
├── package.json        # JS deps (if using npm ecosystem)
├── .env.example        # Documented config keys, placeholder values
├── modules/
│   ├── state.js        # Shared reactive state
│   ├── ui.js           # Rendering helpers
│   ├── dialogs.js      # Native dialog wrappers
│   ├── clipboard.js    # Native clipboard wrappers
│   └── notifications.js # Native notification wrappers
└── styles/
    └── main.css        # Base styles
```

> There is no `main.js` or `preload.js`. Valkyrie exposes a built-in `valkyrie` global to the
> WebView, so there is no IPC bridge to write.

---

## Principles

**System WebView, not bundled Chromium**
Rendering uses whatever WebView the OS provides, and behavior can differ between them. Test on
every target platform.

**The `valkyrie` global is the only native API**
All native calls go through `valkyrie.*`. There is no direct Node or OS access. Call it only
from the dedicated wrapper modules, so the rest of the app never touches the global
(Clean-Code 31).

**Single HTML entry**
`index.html` is a minimal shell. Everything is driven from JS modules.

**Assign callbacks before triggering native events**
Set `window.onFileOpen`, `window.onFolderOpen`, and the other handlers before opening a dialog
or reading the clipboard. A handler assigned afterwards can miss the result.

**Small, focused modules**
Each file owns one domain: state, dialogs, notifications, clipboard, rendering.

**Configuration via `.env`**
Secrets and config live in `.env`, never hard-coded in JS.

---

## CLI Reference

```bash
# Scaffold new project
valkyrie init my-app
cd my-app
npm install

# Development with hot reload
valkyrie dev

# Production build (current platform)
valkyrie build

# Cross-compile for Windows (from Linux, requires mingw-w64)
valkyrie build --target=windows

# Package for distribution
valkyrie package
```

---

## The valkyrie Global API

Valkyrie injects a `valkyrie` object into every WebView page. These are the only native calls
available.

### Dialogs

```javascript
// Message box
valkyrie.dialog.showMessageBox({ title: 'Info', message: 'Hello!' });

// Open file picker → fires window.onFileOpen(path)
valkyrie.dialog.showOpenDialog({});

// Open folder picker → fires window.onFolderOpen(path)
valkyrie.dialog.showOpenDialog({ folder: true });

// Save file picker → fires window.onFileSave(path)
valkyrie.dialog.showSaveDialog({});
```

### Notifications

```javascript
valkyrie.notification.show('Title', 'Body text');
```

### Clipboard

```javascript
valkyrie.clipboard.writeText('text to copy');
valkyrie.clipboard.readText(); // → fires window.onClipboardRead(text)
```

### Custom IPC

```javascript
// Send arbitrary payload to native backend
valkyrie.send({ command: 'custom', data: 'payload' });
```

### Callbacks (assign before triggering)

```javascript
window.onFileOpen     = (path) => { /* handle opened file */ };
window.onFolderOpen   = (path) => { /* handle opened folder */ };
window.onFileSave     = (path) => { /* handle save destination */ };
window.onClipboardRead = (text) => { /* handle clipboard contents */ };
```

---

## State Management

The store declares every key up front. Reading a key that was never declared is a programming
error, so it throws instead of returning `undefined` (Clean-Code 13).

**modules/state.js**
```javascript
class Store {
  constructor(initial) {
    this.state = { ...initial };
    this.listeners = new Map();
  }

  get(key) {
    if (!(key in this.state)) {
      throw new Error(`state.get: unknown key "${key}"`);
    }
    return this.state[key];
  }

  set(key, value) {
    this.state[key] = value;
    this.notify(key, value);
  }

  subscribe(key, callback) {
    if (!this.listeners.has(key)) {
      this.listeners.set(key, []);
    }
    this.listeners.get(key).push(callback);
    return () => {
      const subscribers = this.listeners.get(key);
      this.listeners.set(key, subscribers.filter(cb => cb !== callback));
    };
  }

  notify(key, value) {
    (this.listeners.get(key) ?? []).forEach(cb => cb(value));
  }
}

export default new Store({
  items: [],
  query: '',
  openedFile: '',
  openedFolder: '',
  savedPath: '',
});
```

---

## Dialog Module

**modules/dialogs.js**
```javascript
import state from './state.js';

function openFile() {
  window.onFileOpen = (path) => {
    state.set('openedFile', path);
  };
  valkyrie.dialog.showOpenDialog({});
}

function saveFile() {
  window.onFileSave = (path) => {
    state.set('savedPath', path);
  };
  valkyrie.dialog.showSaveDialog({});
}

function openFolder() {
  window.onFolderOpen = (path) => {
    state.set('openedFolder', path);
  };
  valkyrie.dialog.showOpenDialog({ folder: true });
}

function showMessage(title, message) {
  valkyrie.dialog.showMessageBox({ title, message });
}

export { openFile, saveFile, openFolder, showMessage };
```

---

## Notification Module

**modules/notifications.js**
```javascript
function notify(title, body) {
  valkyrie.notification.show(title, body);
}

export { notify };
```

---

## Clipboard Module

**modules/clipboard.js**
```javascript
function write(text) {
  valkyrie.clipboard.writeText(text);
}

function read(callback) {
  window.onClipboardRead = callback;
  valkyrie.clipboard.readText();
}

export { write, read };
```

---

## UI Helpers

Build DOM nodes with `textContent` rather than interpolating data into `innerHTML`, so file
names and other untrusted strings cannot inject markup.

**modules/ui.js**
```javascript
function renderList(containerId, items, toLabel) {
  const container = document.getElementById(containerId);
  const rows = items.map((item) => {
    const row = document.createElement('div');
    row.className = 'item';
    row.textContent = toLabel(item);
    return row;
  });
  container.replaceChildren(...rows);
}

function show(id) {
  document.getElementById(id).hidden = false;
}

function hide(id) {
  document.getElementById(id).hidden = true;
}

function setText(id, text) {
  document.getElementById(id).textContent = text;
}

export { renderList, show, hide, setText };
```

---

## App Bootstrap

**app.js**
```javascript
import state from './modules/state.js';
import { openFile, showMessage } from './modules/dialogs.js';
import { renderList } from './modules/ui.js';
import { loadFile } from './modules/files.js';

initSearch();
bindToolbar();
renderResultsOnChange();
loadOpenedFiles();
reportUncaughtErrors();

function initSearch() {
  const input = document.getElementById('search');
  input.addEventListener('input', () => {
    state.set('query', input.value.toLowerCase());
  });
}

function bindToolbar() {
  document.getElementById('open').onclick = openFile;
}

function renderResultsOnChange() {
  state.subscribe('items', (items) => {
    const query = state.get('query');
    const matching = items.filter(item => item.name.toLowerCase().includes(query));
    renderList('results', matching, item => item.name);
  });
}

function loadOpenedFiles() {
  state.subscribe('openedFile', loadFile);
}

function reportUncaughtErrors() {
  window.addEventListener('error', (event) => {
    console.error('Uncaught error:', event.error);
    showMessage('Something stopped working', 'The app hit an unexpected problem. Restart it, and if this keeps happening, send the log file to support.');
  });
}
```

---

## Entry Point

**index.html**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>App</title>
  <link rel="stylesheet" href="styles/main.css">
</head>
<body>
  <header class="toolbar">
    <button id="open">Open</button>
    <input type="text" id="search" placeholder="Search...">
  </header>

  <main class="content">
    <div id="results"></div>
  </main>

  <script type="module" src="app.js"></script>
</body>
</html>
```

---

## Styles

**styles/main.css**
```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: system-ui, -apple-system, sans-serif;
  background: #1a1a1a;
  color: #e0e0e0;
}

.toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 16px;
  background: #0d0d0d;
  border-bottom: 1px solid #2a2a2a;
}

.toolbar button {
  padding: 6px 14px;
  background: #2a2a2a;
  border: 1px solid #3a3a3a;
  color: #e0e0e0;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
}

.toolbar button:hover {
  background: #3a3a3a;
}

#search {
  flex: 1;
  padding: 6px 10px;
  background: #2a2a2a;
  border: 1px solid #3a3a3a;
  color: #e0e0e0;
  border-radius: 4px;
  font-size: 13px;
}

.content {
  padding: 20px;
}

.item {
  padding: 12px;
  background: #2a2a2a;
  border-radius: 4px;
  margin-bottom: 8px;
  cursor: pointer;
}

.item:hover {
  background: #3a3a3a;
}
```

---

## Configuration

Valkyrie injects `.env` values into `import.meta.env`. Commit a `.env.example` listing every
key with placeholder values, and gitignore the real `.env`.

**.env.example**
```
APP_NAME=MyApp
API_URL=https://api.example.com
DEBUG=false
```

Read each value once at startup in a single config module, and import that module everywhere
else. Do not reach into `import.meta.env` across the codebase (Clean-Code 14).

---

## Platform Notes

| Feature       | Linux          | Windows          |
|---------------|----------------|------------------|
| Dialogs       | Zenity         | Win32            |
| Notifications | notify-send    | MessageBox       |
| Clipboard     | GTK            | Win32            |
| File Pickers  | Zenity         | Win32            |
| WebView       | webkit2gtk     | Edge WebView2    |

macOS support is experimental. Do not promise it to users.

---

## Cross-Compilation

```bash
# Install cross-compiler (Arch/Manjaro)
sudo pacman -S mingw-w64-gcc

# Build Windows binary from Linux
valkyrie build --target=windows
```

The first build downloads and compiles QuickJS and libuv for Windows. Later builds use the
cached dependencies.

---

## Error Handling

Each operation that can fail owns its boundary: log the technical detail with context, and show
the user what happened, why, and what to do (`skills/engineering/errors/SKILL.md` Part B). Never
show a raw exception message to the user.

```javascript
// modules/files.js
import state from './state.js';
import { showMessage } from './dialogs.js';

export async function loadFile(path) {
  try {
    state.set('content', await readFileContents(path));
  } catch (cause) {
    console.error(`loadFile failed for ${path}:`, cause);
    showMessage(
      "Couldn't open the file",
      `${path} couldn't be read. Check that it still exists and that you have permission to open it, then try again.`
    );
  }
}
```

```javascript
// app.js: last-resort boundary for anything an operation did not handle
window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled rejection:', event.reason);
  showMessage('Something stopped working', 'An operation failed unexpectedly. Try again, and restart the app if it keeps happening.');
});
```

---

## Testing

Keep logic in pure modules so it can be tested in plain Node or Bun without a WebView. The
`valkyrie` global is injected at runtime, so stub it in tests. The store, filtering, and UI
helpers should not touch it at all.

```javascript
// state.test.js  (vitest / bun test)
import store from './modules/state.js';

test('notifies subscribers when a key is set', () => {
  const seen = [];
  store.subscribe('query', (value) => seen.push(value));
  store.set('query', 'hello');
  expect(seen).toEqual(['hello']);
});

test('stops notifying after unsubscribe', () => {
  const seen = [];
  const unsubscribe = store.subscribe('query', (value) => seen.push(value));
  unsubscribe();
  store.set('query', 'again');
  expect(seen).toEqual([]);
});

test('rejects reads of undeclared keys', () => {
  expect(() => store.get('missing')).toThrow('unknown key');
});
```

```javascript
// stub the injected global for any module that calls it
globalThis.valkyrie = {
  dialog: { showMessageBox: () => {} },
  notification: { show: () => {} },
};
```

Unit-test the pure logic (state, filtering, formatting). Check the thin `valkyrie.*` wrappers
manually on each target platform, since their behavior depends on the WebView.

---

## Summary

- No main process or preload: Valkyrie provides them.
- All native calls go through the `valkyrie` global, wrapped in dedicated modules.
- Callbacks are assigned before triggering dialogs or clipboard reads.
- Modules are small and single-purpose.
- Test on both Linux and Windows; WebView behavior differs.
- Configuration comes from `.env`, with a committed `.env.example`.
- Each operation owns its error boundary, with a global last-resort handler in `app.js`.

---

## Project Prompt

Build a Valkyrie desktop app against the structure and rules above: no IPC plumbing, no preload
files, just the `valkyrie` global and focused JS modules. This file decides framework structure
and idiom; coding standards come from `../standards/Clean-Code/`, which wins on any conflict.
Open the sections of `../standards/Principles.md` the task needs.

**Native API Usage**
- Dialogs: `valkyrie.dialog.*`
- Notifications: `valkyrie.notification.show(title, body)`
- Clipboard: `valkyrie.clipboard.writeText` / `valkyrie.clipboard.readText`
- Custom backend: `valkyrie.send({ command, data })`
- Always assign `window.on*` callbacks before triggering a dialog or clipboard read

**State Management**
- One centralized reactive store in `modules/state.js`, with every key declared up front
- Per-key subscriptions
- No global variables outside the store

**Error Handling**
- Each async operation owns a try/catch boundary that logs with context and shows a
  what / why / action message
- A global `error` and `unhandledrejection` boundary in `app.js` as the last resort
- User-facing messages go through `valkyrie.dialog.showMessageBox`, never as raw exception text

**Platform Awareness**
- Behavior differs between Linux (webkit2gtk) and Windows (Edge WebView2). Test both
- macOS is experimental

### Setup

```bash
valkyrie init my-app
cd my-app
npm install
valkyrie dev
```

### Deliverables

1. `index.html`: a minimal shell with no logic
2. `app.js`: bootstrap with event wiring and state subscriptions
3. `modules/state.js`: the reactive key-value store
4. `modules/dialogs.js`: native dialog wrappers
5. `modules/clipboard.js`: clipboard read and write wrappers
6. `modules/notifications.js`: the notification wrapper
7. `modules/ui.js`: pure rendering helpers
8. `styles/main.css`: base styles
9. `package.json` with dev, build, and package scripts
10. `.env.example` documenting every variable with placeholder values
11. `README.md` with setup and build instructions

### Validation Checklist

- [ ] Verify commands from the project's AGENTS.md or README run (or honest manual checks are listed)
- [ ] No secrets committed; `.env.example` uses placeholders only
- [ ] No `valkyrie.*` calls outside the dedicated wrapper modules
- [ ] `window.on*` callbacks assigned before every dialog and clipboard trigger
- [ ] Functions do one thing at one level of abstraction (Clean-Code 15, 27)
- [ ] No global variables except `valkyrie`
- [ ] All modules use ES module syntax
- [ ] Untrusted strings rendered with `textContent`, never `innerHTML`
- [ ] Names reveal intent (Clean-Code 06)
- [ ] Works on both Linux and Windows
- [ ] Configuration read once from `.env`

### Pre-Delivery

```bash
valkyrie build
valkyrie build --target=windows
valkyrie package
```
