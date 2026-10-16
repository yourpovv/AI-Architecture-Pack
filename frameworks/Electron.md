# Electron Architecture

> **Agent load:** Open Project Structure, Principles, Error Handling, Configuration, and Project Prompt / Validation first. Open other sections only when the task needs them. Read the project's `AGENTS.md`. Coding standards come from `../standards/Clean-Code/`. For reviews use `skills/review/audit/SKILL.md`; for craft use `skills/engineering/craft/SKILL.md`. Prefer extending an existing repo over scaffolding a parallel tree.

Structure for an Electron desktop app. Main-process examples are CommonJS; renderer examples
are ES modules, because the renderer runs without Node integration.

---

## Project Structure

```
project/
├── src/
│   ├── main.js          # Main process
│   ├── preload.js       # IPC bridge
│   ├── storage.js       # File/database I/O
│   └── ui/
│       ├── index.html   # Main window
│       ├── app.js       # Renderer entry
│       ├── styles.css   # Base styles
│       └── modules/
│           ├── state.js     # Shared state
│           ├── search.js    # Features
│           └── settings.js
├── assets/
│   └── icons/
└── dist/                # Build output
```

---

## Principles

**Separate processes**
The main process owns the system (files, OS, network). The renderer owns the UI. Never mix
the two.

**Explicit IPC**
Processes talk through namespaced channels (`domain:action`). Node.js is never exposed to the
renderer. The main process validates every IPC payload, because the renderer is an untrusted
boundary.

**Single responsibility**
Each module does one thing and has one reason to change (Clean-Code `solid/01`).

**No globals**
Pass dependencies explicitly. A module's needs should be visible in its imports and
parameters.

**Clean up resources**
Remove listeners and close files and connections on exit.

---

## Main Process

**main.js**
```javascript
const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const storage = require('./storage');
const { requireItem, requireId } = require('./validation');

let window;

function createWindow() {
  window = new BrowserWindow({
    width: 1100,
    height: 700,
    frame: false,
    backgroundColor: '#1a1a1a',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  window.loadFile('src/ui/index.html');

  window.on('closed', () => {
    window = null;
  });
}

app.whenReady().then(() => {
  storage.init(path.join(app.getPath('userData'), 'data.json'));
  createWindow();
});

app.on('window-all-closed', () => {
  storage.close();
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

ipcMain.on('window:minimize', () => window?.minimize());
ipcMain.on('window:maximize', () => {
  window?.isMaximized() ? window.unmaximize() : window.maximize();
});
ipcMain.on('window:close', () => window?.close());

ipcMain.handle('storage:list', () => storage.list());
ipcMain.handle('storage:add', (event, item) => storage.add(requireItem(item)));
ipcMain.handle('storage:remove', (event, id) => storage.remove(requireId(id)));
```

---

## Storage Layer

A missing data file is the normal first run, so it starts empty. A file that exists but cannot
be read or parsed is a failure: throw with context instead of replacing the user's data with
an empty list (Clean-Code 34).

**storage.js**
```javascript
const fs = require('fs');

let dataPath;
let items = [];

function init(path) {
  dataPath = path;
  items = fs.existsSync(dataPath) ? readItems() : [];
}

function readItems() {
  try {
    return JSON.parse(fs.readFileSync(dataPath, 'utf-8'));
  } catch (cause) {
    throw new Error(`storage.init: could not read ${dataPath}`, { cause });
  }
}

function list() {
  return [...items];
}

function add(item) {
  items.push(item);
  write();
  return item;
}

function remove(id) {
  items = items.filter(item => item.id !== id);
  write();
}

function write() {
  fs.writeFileSync(dataPath, JSON.stringify(items, null, 2));
}

function close() {
  write();
}

module.exports = { init, list, add, remove, close };
```

---

## Preload Bridge

**preload.js**
```javascript
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  window: {
    minimize: () => ipcRenderer.send('window:minimize'),
    maximize: () => ipcRenderer.send('window:maximize'),
    close: () => ipcRenderer.send('window:close')
  },

  storage: {
    list: () => ipcRenderer.invoke('storage:list'),
    add: (item) => ipcRenderer.invoke('storage:add', item),
    remove: (id) => ipcRenderer.invoke('storage:remove', id)
  }
});
```

---

## Renderer Process

### State Management

**modules/state.js**
```javascript
class State {
  constructor() {
    this.items = [];
    this.listeners = [];
  }

  replaceAll(items) {
    this.items = items;
    this.notify();
  }

  all() {
    return [...this.items];
  }

  add(item) {
    this.items.push(item);
    this.notify();
  }

  remove(id) {
    this.items = this.items.filter(item => item.id !== id);
    this.notify();
  }

  onChange(callback) {
    this.listeners.push(callback);
    return () => {
      this.listeners = this.listeners.filter(listener => listener !== callback);
    };
  }

  notify() {
    this.listeners.forEach(callback => callback(this.all()));
  }
}

export default new State();
```

### Feature Module

Render untrusted strings with `textContent`, never by interpolating them into `innerHTML`.

**modules/search.js**
```javascript
import state from './state.js';

let input;
let results;

export function initSearch() {
  input = document.getElementById('search');
  results = document.getElementById('results');
  input.addEventListener('input', showMatchingItems);
}

function showMatchingItems() {
  const query = input.value.toLowerCase();
  const matching = state.all().filter(item => item.name.toLowerCase().includes(query));
  results.replaceChildren(...matching.map(toRow));
}

function toRow(item) {
  const row = document.createElement('div');
  row.className = 'item';
  row.textContent = item.name;
  return row;
}
```

### App Entry

**app.js**
```javascript
import state from './modules/state.js';
import { initSearch } from './modules/search.js';

init();

async function init() {
  state.replaceAll(await window.api.storage.list());
  initSearch();
  bindWindowControls();
}

function bindWindowControls() {
  document.getElementById('minimize').onclick = () => window.api.window.minimize();
  document.getElementById('maximize').onclick = () => window.api.window.maximize();
  document.getElementById('close').onclick = () => window.api.window.close();
}
```

---

## UI

**index.html**
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'">
  <title>App</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="titlebar">
    <div class="title">App</div>
    <div class="controls">
      <button id="minimize">−</button>
      <button id="maximize">□</button>
      <button id="close">×</button>
    </div>
  </div>

  <div class="content">
    <input type="text" id="search" placeholder="Search...">
    <div id="results"></div>
  </div>

  <script type="module" src="app.js"></script>
</body>
</html>
```

**styles.css**
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
  overflow: hidden;
}

.titlebar {
  height: 32px;
  background: #0d0d0d;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 12px;
  -webkit-app-region: drag;
}

.controls {
  display: flex;
  gap: 8px;
  -webkit-app-region: no-drag;
}

.controls button {
  width: 32px;
  height: 24px;
  border: none;
  background: transparent;
  color: #e0e0e0;
  cursor: pointer;
  font-size: 16px;
}

.controls button:hover {
  background: #2a2a2a;
}

.content {
  padding: 20px;
}

#search {
  width: 100%;
  padding: 10px;
  background: #2a2a2a;
  border: 1px solid #3a3a3a;
  color: #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
}

#results {
  margin-top: 20px;
}

.item {
  padding: 12px;
  background: #2a2a2a;
  border-radius: 4px;
  margin-bottom: 8px;
}

.item:hover {
  background: #3a3a3a;
  cursor: pointer;
}
```

---

## IPC Patterns

**Request-response**

```javascript
// Main
ipcMain.handle('data:fetch', () => fetchData());

// Renderer
const data = await window.api.data.fetch();
```

**Send-only**

```javascript
// Main
ipcMain.on('window:minimize', () => {
  mainWindow.minimize();
});

// Renderer
window.api.window.minimize();
```

**Broadcast to renderer**

```javascript
// Main
mainWindow.webContents.send('data:updated', newData);

// Preload: return an unsubscribe function so the renderer can clean up
contextBridge.exposeInMainWorld('api', {
  onDataUpdate: (callback) => {
    const listener = (event, data) => callback(data);
    ipcRenderer.on('data:updated', listener);
    return () => ipcRenderer.removeListener('data:updated', listener);
  }
});

// Renderer
const stopListening = window.api.onDataUpdate((data) => state.replaceAll(data));
```

---

## Error Handling

Failures cross the IPC boundary once. The main process adds context and rethrows; the renderer
owns the user-facing message (`skills/engineering/errors/SKILL.md`).

**Main process**

```javascript
ipcMain.handle('storage:add', (event, item) => {
  try {
    return storage.add(requireItem(item));
  } catch (cause) {
    throw new Error(`storage:add failed for item ${item?.id}`, { cause });
  }
});
```

**Renderer process**

```javascript
async function addItem(item) {
  try {
    state.add(await window.api.storage.add(item));
  } catch (error) {
    console.error('addItem failed:', error);
    showError(
      "Your item wasn't saved",
      'The app could not write to its data file. Check that the disk has free space, then try again.'
    );
  }
}
```

---

## Testing

Keep tests repeatable: point storage at a temporary file, never at the real user-data folder
(Clean-Code `unit-tests/06`).

**Main process test**

```javascript
const os = require('os');
const path = require('path');
const fs = require('fs');
const storage = require('./storage');

function freshStorage() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'storage-'));
  storage.init(path.join(dir, 'data.json'));
}

test('lists an item after it is added', () => {
  freshStorage();
  const item = { id: 1, name: 'Test' };

  storage.add(item);

  expect(storage.list()).toContainEqual(item);
});

test('refuses to start from a corrupt data file', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'storage-'));
  const dataPath = path.join(dir, 'data.json');
  fs.writeFileSync(dataPath, '{not json');

  expect(() => storage.init(dataPath)).toThrow('could not read');
});
```

**Renderer test**

```javascript
import state from './modules/state.js';

test('notifies listeners when items are replaced', () => {
  const callback = jest.fn();
  state.onChange(callback);

  state.replaceAll([{ id: 1 }]);

  expect(callback).toHaveBeenCalledWith([{ id: 1 }]);
});
```

---

## Build Configuration

**package.json**
```json
{
  "name": "app",
  "version": "1.0.0",
  "main": "src/main.js",
  "scripts": {
    "start": "electron .",
    "build": "electron-builder"
  },
  "devDependencies": {
    "electron": "^28.0.0",
    "electron-builder": "^24.0.0"
  },
  "build": {
    "appId": "com.example.app",
    "files": ["src/**/*", "assets/**/*"],
    "directories": {
      "output": "dist"
    }
  }
}
```

---

## Configuration

A desktop app has two kinds of configuration. Keep them apart:

- **Runtime mode:** detect development vs packaged with `app.isPackaged`, never by guessing
  from `NODE_ENV`. Drive log verbosity, dev tools, and update channels from that one check.
- **User settings:** persist in `app.getPath('userData')` (via `electron-store` or the storage
  layer), never next to the binary, which may be read-only.

```javascript
// src/main/config.js
const { app } = require('electron');
const Store = require('electron-store');

const store = new Store({
  defaults: { theme: 'system', telemetry: false },
});

const config = {
  isDev: !app.isPackaged,
  userDataPath: app.getPath('userData'),
  get: (key) => store.get(key),
  set: (key, value) => store.set(key, value),
};

module.exports = { config };
```

Secrets (API keys, signing tokens) stay in the **main** process, loaded from environment
variables at build or run time. Never bundle them into the renderer, where any user can read
them. Expose only results over IPC.

---

## Summary

- Main and renderer processes are strictly separated.
- `contextIsolation` is on and `nodeIntegration` is off.
- IPC channels are namespaced as `domain:action`, and the main process validates every payload.
- Modules are small and focused.
- Resources are cleaned up on exit.
- Shared renderer data lives in one state module.

---

## Project Prompt

Build an Electron desktop app against the structure and rules above. This file decides
framework structure and idiom; coding standards come from `../standards/Clean-Code/`, which
wins on any conflict. Open the sections of `../standards/Principles.md` the task needs.

**Security (non-negotiable)**
- `contextIsolation: true`
- `nodeIntegration: false`
- Validate all IPC input in the main process; the renderer is untrusted
- Namespace IPC channels as `domain:action`

**IPC Patterns**
- `invoke`/`handle` for request-response
- `send`/`on` for fire-and-forget
- The main process adds context and rethrows; the renderer shows the user-facing message

**Resource Management**
- Remove event listeners on cleanup
- Close database connections on exit
- Save state before exit so the user's work survives

### Setup

```bash
npm init -y
npm install electron
mkdir -p src/ui/modules assets/icons dist
```

### Deliverables

1. A complete project following the structure above
2. A main process that owns system operations
3. A preload bridge exposing a minimal, secure IPC API
4. A renderer process with UI logic only
5. A storage layer for persistence
6. A renderer state module
7. Custom window controls
8. `package.json` with build config
9. A README with setup instructions

### Validation Checklist

- [ ] Verify commands from the project's AGENTS.md or README run (or honest manual checks are listed)
- [ ] No secrets committed; env examples use placeholders only
- [ ] Functions do one thing at one level of abstraction (Clean-Code 15, 27)
- [ ] `contextIsolation` enabled
- [ ] `nodeIntegration` disabled
- [ ] No Node.js in the renderer
- [ ] All IPC channels namespaced
- [ ] All IPC input validated in the main process
- [ ] Event listeners cleaned up
- [ ] Names match the domain and local convention (Clean-Code 06)
- [ ] Resources closed on exit

### Security Checklist

- [ ] `contextIsolation` enabled
- [ ] `nodeIntegration` disabled
- [ ] `webSecurity` enabled
- [ ] No `eval()` or `Function()` in the renderer
- [ ] Content Security Policy configured
- [ ] All IPC input validated
- [ ] Untrusted strings rendered with `textContent`, never `innerHTML`

### Pre-Delivery

```bash
npm run lint                  # no lint errors
npm test                      # main + renderer tests pass
npm start                     # launches; check the security checklist holds
npm run build                 # electron-builder packages without errors
```
