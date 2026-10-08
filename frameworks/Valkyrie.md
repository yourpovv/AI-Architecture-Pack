# Valkyrie Architecture

> **Agent load:** You open Project Structure, Principles, Error Handling, Configuration, and Project Prompt / Validation first. That is your discipline. You open other sections only when your task needs them. You pair with the matching `languages/*` file and project `AGENTS.md`. Reviews: `skills/review/audit/SKILL.md`. Craft: `skills/engineering/craft/SKILL.md`. You prefer extending an existing repo over scaffolding a parallel tree. Respect what is there.

You keep a clean structure for your lightweight desktop app with Valkyrie. Small stays readable. Small stays honest.

---

## What is Valkyrie?

Valkyrie is a CLI-driven desktop framework that uses the system WebView (webkit2gtk on Linux, Edge WebView2 on Windows) instead of bundling Chromium. Listen. You ship ~2 MB binaries instead of Electron's 150-300 MB. That size difference is the tradeoff you chose.

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

> No `main.js` or preload.js here. Valkyrie exposes a built-in `valkyrie` global to your WebView. You write no IPC bridge yourself.

---

## Principles

**System WebView, not bundled Chromium**
You render in whatever WebView your OS provides. You test on your target platforms. What works in one WebView can surprise you in another.

**valkyrie global is your API**
All your native calls go through `valkyrie.*`. You never try to access Node or OS APIs directly. One door. Use it.

**Single HTML entry**
`index.html` is your shell. You keep it minimal. You drive everything from your JS modules.

**Callbacks for native events**
You assign `window.onFileOpen`, `window.onFolderOpen`, etc. before you trigger dialogs. Set the handler first. Then ask.

**Small, focused modules**
Each file owns one domain: state, dialogs, notifications, rendering. One file. One job.

**Environment config via .env**
Your secrets and config live in `.env`, not hard-coded in your JS. Keep them out of your code.

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

Valkyrie injects a `valkyrie` object into every WebView page you own. These are the only native calls you get. Learn them. Stay inside them.

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
the real `.env`.

**.env**
```
APP_NAME=MyApp
API_URL=https://api.example.com
DEBUG=false
```

You access them in your app via the `import.meta.env` object (Valkyrie handles .env injection).
You read each value once at startup. Do not reach into `import.meta.env` all over your
codebase. One read. One place.

---

## Platform Notes

| Feature       | Linux          | Windows          |
|---------------|----------------|------------------|
| Dialogs       | Zenity         | Win32            |
| Notifications | notify-send    | MessageBox       |
| Clipboard     | GTK            | Win32            |
| File Pickers  | Zenity         | Win32            |
| WebView       | webkit2gtk     | Edge WebView2    |

Your macOS support is experimental. Plan for that.

---

## Cross-Compilation

```bash
# Install cross-compiler (Arch/Manjaro)
sudo pacman -S mingw-w64-gcc

# Build Windows binary from Linux
valkyrie build --target=windows
```

Your first build downloads and compiles QuickJS and libuv for Windows. Your later builds use cached deps. Patience once. Speed after.

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
store, your filtering, and your `ui` helpers should not touch it directly anyway. Keep them clean.

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
to manual checks on each target platform. Their behavior differs by WebView anyway. Test what you can. Look at the rest.

---

## Summary

You write no main process or preload. Valkyrie handles that for you.
You use the `valkyrie` global for all your native calls. One door.
You assign callbacks before you trigger dialogs or clipboard reads. Handler first. Then ask.
You keep modules small and single-purpose. One file. One job.
You test on both Linux and Windows. WebView behavior differs. Believe it.
You use `.env` for configuration. Keep secrets out of your code.
You handle errors globally with `window.addEventListener('error'...)`. Catch it at the top.

---

## Project Prompt

Build a Valkyrie desktop app against the structure and rules above. No IPC plumbing, no preload files, just the `valkyrie` global and focused JS modules. Where the rules and your defaults disagree, this file wins.

Read `../standards/Principles.md` alongside this file before starting.

**Native API Usage**
- Dialogs: `valkyrie.dialog.*`
- Notifications: `valkyrie.notification.show(title, body)`
- Clipboard: `valkyrie.clipboard.writeText` / `valkyrie.clipboard.readText`
- Custom backend: `valkyrie.send({ command, data })`
- Always assign `window.on*` callbacks before triggering any dialog or clipboard read

**State Management**
- Centralized reactive store in `modules/state.js`
- Subscriber pattern with per-key subscriptions
- No global variables outside the store

**Error Handling**
- Global `window.addEventListener('error'...)` boundary
- Per-operation try/catch for async work
- Show user-facing errors via `valkyrie.dialog.showMessageBox`

**Platform Awareness**
- Behavior differs between Linux (webkit2gtk) and Windows (Edge WebView2)
- Test both platforms
- macOS is experimental

### Setup

```bash
valkyrie init my-app
cd my-app
npm install
valkyrie dev
```

### Deliverables

1. `index.html`, minimal shell, no logic
2. `app.js`, bootstrap, event wiring, state subscriptions
3. `modules/state.js`, reactive key-value store
4. `modules/dialogs.js`, native dialog wrappers
5. `modules/clipboard.js`, clipboard read/write wrappers
6. `modules/notifications.js`, notification wrapper
7. `modules/ui.js`, pure rendering helpers
8. `styles/main.css`, clean base styles
9. `package.json` with dev/build/package scripts
10. `.env` with documented variables
11. `README.md` with setup and build instructions

### Validation Checklist

- [ ] Verify commands from project AGENTS.md / README run (or honest manual checks listed)
- [ ] No secrets committed; env examples use placeholders only

- [ ] No `valkyrie.*` calls outside dedicated wrapper modules
- [ ] `window.on*` callbacks assigned before every dialog/clipboard trigger
- [ ] Functions are small and single-purpose; extract when a second concern appears (see Principles / skills/engineering/craft/SKILL.md)
- [ ] No global variables (except `valkyrie`)
- [ ] All modules use ES module syntax
- [ ] Global error boundary in `app.js`
- [ ] Natural, human naming throughout
- [ ] Works on both Linux and Windows
- [ ] `.env` used for configuration

### Pre-Delivery

```bash
valkyrie build
valkyrie build --target=windows
valkyrie package
```
