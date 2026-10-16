# Valkyrie Architecture

> **Agent load:** You open Project Structure, Principles, Error Handling, Configuration, and Project Prompt / Validation first. That is your discipline. You open other sections only when your task needs them. You pair with the matching `languages/*` file and project `AGENTS.md`. Reviews: `skills/review/audit/SKILL.md`. Craft: `skills/engineering/craft/SKILL.md`. You prefer extending an existing repo over scaffolding a parallel tree. You respect what is there.

You keep a clean structure for your lightweight desktop app with Valkyrie. You keep it small. Small stays readable for you. Small stays honest for your team.

---

## What is Valkyrie?

Valkyrie is a CLI-driven desktop framework that uses the system WebView (webkit2gtk on Linux, Edge WebView2 on Windows) instead of bundling Chromium. Listen. You ship ~2 MB binaries instead of Electron's 150-300 MB. You chose that size difference. You live with what it costs you.

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
├── .env                # Environment variables
├── modules/
│   ├── state.js        # Shared reactive state
│   ├── ui.js           # Rendering helpers
│   ├── dialogs.js      # Native dialog wrappers
│   └── notifications.js # Native notification wrappers
└── styles/
    └── main.css        # Base styles
```

> No `main.js` or preload.js here. Valkyrie exposes a built-in `valkyrie` global to your WebView. You write no IPC bridge yourself. You use what you are given.

---

## Principles

**System WebView, not bundled Chromium**
You render in whatever WebView your OS provides. You test on your target platforms. What works in one WebView can surprise you in another. You do not assume. You check.

**valkyrie global is your API**
All your native calls go through `valkyrie.*`. You never try to access Node or OS APIs directly. You have one door. You use it. You stay inside it.

**Single HTML entry**
`index.html` is your shell. You keep it minimal. You drive everything from your JS modules. Your shell stays dumb. Your modules do the work.

**Callbacks for native events**
You assign `window.onFileOpen`, `window.onFolderOpen`, etc. before you trigger dialogs. You set the handler first. Then you ask. If you ask first, you miss the answer.

**Small, focused modules**
Each file owns one domain: state, dialogs, notifications, rendering. You keep one file to one job. That is how you stay honest.

**Environment config via .env**
Your secrets and config live in `.env`, not hard-coded in your JS. You keep them out of your code. Your code stays clean. Your secrets stay out of trouble.

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

Valkyrie injects a `valkyrie` object into every WebView page you own. These are the only native calls you get. You learn them. You stay inside them. Why stray outside what your platform supports?

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

**modules/state.js**
```javascript
class Store {
  constructor(initial = {}) {
    this.state = initial;
    this.listeners = new Map();
  }

  get(key) {
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
      const subs = this.listeners.get(key);
      this.listeners.set(key, subs.filter(cb => cb !== callback));
    };
  }

  notify(key, value) {
    (this.listeners.get(key) || []).forEach(cb => cb(value));
  }
}

export default new Store({ items: [], query: '' });
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

function alert(title, message) {
  valkyrie.dialog.showMessageBox({ title, message });
}

export { openFile, saveFile, openFolder, alert };
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

**modules/ui.js**
```javascript
function render(containerId, items, template) {
  const el = document.getElementById(containerId);
  el.innerHTML = items.map(template).join('');
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

export { render, show, hide, setText };
```

---

## App Bootstrap

**app.js**
```javascript
import state from './modules/state.js';
import { openFile, alert } from './modules/dialogs.js';
import { render } from './modules/ui.js';

function initSearch() {
  const input = document.getElementById('search');
  input.addEventListener('input', () => {
    const query = input.value.toLowerCase();
    state.set('query', query);
  });
}

function bindToolbar() {
  document.getElementById('open').onclick = openFile;
}

state.subscribe('items', (items) => {
  const query = state.get('query') || '';
  const filtered = items.filter(i => i.name.toLowerCase().includes(query));
  render('results', filtered, item => `<div class="item">${item.name}</div>`);
});

state.subscribe('openedFile', (path) => {
  // Load and process the file
  console.log('File opened:', path);
});

window.addEventListener('error', (e) => {
  alert('Error', e.message);
});

initSearch();
bindToolbar();
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

Your config lives in `.env`. Valkyrie injects it so you read it through `import.meta.env`.
You keep secrets out of committed source. You commit a `.env.example` with the keys. You gitignore
the real `.env`. Your teammates see what you need. They do not see your values.

**.env**
```
APP_NAME=MyApp
API_URL=https://api.example.com
DEBUG=false
```

You access them in your app via the `import.meta.env` object (Valkyrie handles .env injection).
You read each value once at startup. You do not reach into `import.meta.env` all over your
codebase. You read once. You keep it in one place.

---

## Platform Notes

| Feature       | Linux          | Windows          |
|---------------|----------------|------------------|
| Dialogs       | Zenity         | Win32            |
| Notifications | notify-send    | MessageBox       |
| Clipboard     | GTK            | Win32            |
| File Pickers  | Zenity         | Win32            |
| WebView       | webkit2gtk     | Edge WebView2    |

Your macOS support is experimental. You plan for that. You do not promise what you cannot prove.

---

## Cross-Compilation

```bash
# Install cross-compiler (Arch/Manjaro)
sudo pacman -S mingw-w64-gcc

# Build Windows binary from Linux
valkyrie build --target=windows
```

Your first build downloads and compiles QuickJS and libuv for Windows. Your later builds use cached deps. You wait once. You build fast after that.

---

## Error Handling

```javascript
// Global error boundary in app.js
window.addEventListener('error', (e) => {
  valkyrie.dialog.showMessageBox({
    title: 'Unexpected Error',
    message: e.message
  });
});

window.addEventListener('unhandledrejection', (e) => {
  console.error('Unhandled rejection:', e.reason);
});

// Per-operation
async function loadFile(path) {
  try {
    const content = await fetchFile(path);
    state.set('content', content);
  } catch (err) {
    valkyrie.dialog.showMessageBox({ title: 'Load Failed', message: err.message });
  }
}
```

---

## Testing

You keep logic in pure modules so you can test them in plain Node/Bun without a WebView.
The `valkyrie` global is injected at runtime, so you **stub it** in your tests. Your `state`
store, your filtering, and your `ui` helpers should not touch it directly anyway. You keep them clean. Clean code is testable code.

```javascript
// state.test.js  (vitest / bun test)
import store from './modules/state.js';

test('subscribers fire on set', () => {
  const seen = [];
  store.subscribe('query', (v) => seen.push(v));
  store.set('query', 'hello');
  expect(seen).toEqual(['hello']);
});

test('unsubscribe stops updates', () => {
  const seen = [];
  const off = store.subscribe('query', (v) => seen.push(v));
  off();
  store.set('query', 'again');
  expect(seen).toEqual([]);
});
```

```javascript
// stub the injected global for any module that calls it
globalThis.valkyrie = {
  dialog: { showMessageBox: () => {} },
  notification: { show: () => {} },
};
```

You test the pure logic (state, filtering, formatting). You leave the thin `valkyrie.*` wrappers
to manual checks on each target platform. Their behavior differs by WebView anyway. You test what you can. You look at the rest with your own eyes.

---

## Summary

You write no main process or preload. Valkyrie handles that for you. That is work you do not own.
You use the `valkyrie` global for all your native calls. You have one door.
You assign callbacks before you trigger dialogs or clipboard reads. You set the handler first. Then you ask.
You keep modules small and single-purpose. You keep one file to one job.
You test on both Linux and Windows. WebView behavior differs. You believe it because you have seen it.
You use `.env` for configuration. You keep secrets out of your code.
You handle errors globally with `window.addEventListener('error'...)`. You catch it at the top.

---

## Project Prompt

Build a Valkyrie desktop app against the structure and rules above. No IPC plumbing, no preload files, just the `valkyrie` global and focused JS modules. Where the rules and your defaults disagree, this file wins. You obey this file.

Read `../standards/Principles.md` alongside this file before starting. You know your standards before you cut.

**Native API Usage**
- Dialogs: `valkyrie.dialog.*`
- Notifications: `valkyrie.notification.show(title, body)`
- Clipboard: `valkyrie.clipboard.writeText` / `valkyrie.clipboard.readText`
- Custom backend: `valkyrie.send({ command, data })`
- You always assign `window.on*` callbacks before triggering any dialog or clipboard read. Handler first. Then ask.

**State Management**
- You keep a centralized reactive store in `modules/state.js`. One place for your truth.
- You use a subscriber pattern with per-key subscriptions. Each key notifies its own listeners.
- You keep no global variables outside the store. Your store owns your state.

**Error Handling**
- You keep a global `window.addEventListener('error'...)` boundary. You catch it at the top.
- You use per-operation try/catch for async work. Each operation owns its failure.
- You show user-facing errors via `valkyrie.dialog.showMessageBox`. Your user hears it plain.

**Platform Awareness**
- Behavior differs between Linux (webkit2gtk) and Windows (Edge WebView2). You respect that gap.
- You test both platforms. You do not guess.
- macOS is experimental. You plan for that.

### Setup

```bash
valkyrie init my-app
cd my-app
npm install
valkyrie dev
```

### Deliverables

1. You ship `index.html`, your minimal shell with no logic.
2. You ship `app.js`, your bootstrap with event wiring and state subscriptions.
3. You ship `modules/state.js`, your reactive key-value store.
4. You ship `modules/dialogs.js`, your native dialog wrappers.
5. You ship `modules/clipboard.js`, your clipboard read and write wrappers.
6. You ship `modules/notifications.js`, your notification wrapper.
7. You ship `modules/ui.js`, your pure rendering helpers.
8. You ship `styles/main.css`, your clean base styles.
9. You ship `package.json` with dev, build, and package scripts.
10. You ship `.env` with documented variables.
11. You ship `README.md` with setup and build instructions.

### Validation Checklist

- [ ] You verify commands from project AGENTS.md / README run (or you list honest manual checks)
- [ ] You commit no secrets. Your env examples use placeholders only
- [ ] You keep no `valkyrie.*` calls outside dedicated wrapper modules
- [ ] You assign `window.on*` callbacks before every dialog and clipboard trigger
- [ ] Your functions stay small and single-purpose. You extract when a second concern appears (see Principles / skills/engineering/craft/SKILL.md)
- [ ] You keep no global variables (except `valkyrie`)
- [ ] All your modules use ES module syntax
- [ ] You keep a global error boundary in `app.js`
- [ ] You use natural, human naming throughout
- [ ] Your code works on both Linux and Windows
- [ ] You use `.env` for configuration

### Pre-Delivery

```bash
valkyrie build
valkyrie build --target=windows
valkyrie package
```
