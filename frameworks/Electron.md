# Electron Architecture

> **Agent load:** You open Project Structure, Principles, Error Handling, Configuration, and Project Prompt / Validation first. That is your discipline. You open other sections only when your task needs them. You pair this with the matching `languages/*` file and your project `AGENTS.md`. For reviews you use `skills/review/audit/SKILL.md`. For craft you use `skills/engineering/craft/SKILL.md`. You prefer extending an existing repo over scaffolding a parallel tree. Respect what is there.

You keep a clean structure for your Electron desktop app. Clean means you can find things. Clean means your teammate can too.

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
Your main process owns the system. Your renderer owns the UI. Never mix the two. Ask where each line belongs. Put it there.

**Explicit IPC**
You talk through namespaced channels. You never expose Node.js to your renderer. That boundary is your protection.

**Single responsibility**
Each module does one thing. One reason to change. That is how you stay honest.

**No globals**
You pass dependencies explicitly. No hidden globals. What a module needs, you hand it.

**Clean up resources**
You remove listeners. You close files on exit. A craftsman leaves nothing running behind him.

---

## Main Process

**main.js**
```javascript
const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const storage = require('./storage');

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
  storage.init();
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

ipcMain.handle('storage:getAll', () => storage.getAll());
ipcMain.handle('storage:save', (event, data) => storage.save(data));
ipcMain.handle('storage:delete', (event, id) => storage.delete(id));
```

---

## Storage Layer

**storage.js**
```javascript
const fs = require('fs');
const path = require('path');

const DATA_PATH = path.join(app.getPath('userData'), 'data.json');

let data = [];

function init() {
  try {
    const file = fs.readFileSync(DATA_PATH, 'utf-8');
    data = JSON.parse(file);
  } catch {
    data = [];
    save();
  }
}

function getAll() {
  return data;
}

function save(item) {
  data.push(item);
  write();
  return item;
}

function deleteById(id) {
  data = data.filter(item => item.id !== id);
  write();
}

function write() {
  fs.writeFileSync(DATA_PATH, JSON.stringify(data, null, 2));
}

function close() {
  write();
}

module.exports = { init, getAll, save, delete: deleteById, close };
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
    getAll: () => ipcRenderer.invoke('storage:getAll'),
    save: (data) => ipcRenderer.invoke('storage:save', data),
    delete: (id) => ipcRenderer.invoke('storage:delete', id)
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
    this.data = [];
    this.listeners = [];
  }
  
  set(newData) {
    this.data = newData;
    this.notify();
  }
  
  get() {
    return this.data;
  }
  
  add(item) {
    this.data.push(item);
    this.notify();
  }
  
  remove(id) {
    this.data = this.data.filter(item => item.id !== id);
    this.notify();
  }
  
  onChange(callback) {
    this.listeners.push(callback);
  }
  
  notify() {
    this.listeners.forEach(callback => callback(this.data));
  }
}

module.exports = new State();
```

### Feature Module

**modules/search.js**
```javascript
const state = require('./state');

class Search {
  constructor() {
    this.input = null;
    this.results = null;
  }
  
  init() {
    this.input = document.getElementById('search');
    this.results = document.getElementById('results');
    
    this.input.addEventListener('input', () => this.handleSearch());
  }
  
  handleSearch() {
    const query = this.input.value.toLowerCase();
    const items = state.get();
    
    const filtered = items.filter(item =>
      item.name.toLowerCase().includes(query)
    );
    
    this.render(filtered);
  }
  
  render(items) {
    this.results.innerHTML = items
      .map(item => `<div class="item">${item.name}</div>`)
      .join('');
  }
}

module.exports = new Search();
```

### App Entry

**app.js**
```javascript
const state = require('./modules/state');
const search = require('./modules/search');

async function init() {
  const data = await window.api.storage.getAll();
  state.set(data);
  
  search.init();
  bindWindowControls();
}

function bindWindowControls() {
  document.getElementById('minimize').onclick = () => {
    window.api.window.minimize();
  };
  
  document.getElementById('maximize').onclick = () => {
    window.api.window.maximize();
  };
  
  document.getElementById('close').onclick = () => {
    window.api.window.close();
  };
}

init();
```

---

## UI

**index.html**
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
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
  
  <script src="app.js"></script>
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
ipcMain.handle('data:fetch', async () => {
  return await fetchData();
});

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

// Preload
contextBridge.exposeInMainWorld('api', {
  onDataUpdate: (callback) => {
    ipcRenderer.on('data:updated', (event, data) => callback(data));
  }
});

// Renderer
window.api.onDataUpdate((data) => {
  console.log('Data updated:', data);
});
```

---

## Error Handling

**Main process**

```javascript
ipcMain.handle('storage:save', async (event, data) => {
  try {
    return await storage.save(data);
  } catch (err) {
    console.error('Save failed:', err);
    throw err;
  }
});
```

**Renderer process**

```javascript
async function saveData(data) {
  try {
    await window.api.storage.save(data);
    showSuccess('Saved');
  } catch (err) {
    showError('Save failed');
  }
}
```

---

## Testing

**Main process test**

```javascript
const { app } = require('electron');
const storage = require('./storage');

test('saves data correctly', async () => {
  storage.init();
  
  const item = { id: 1, name: 'Test' };
  storage.save(item);
  
  const all = storage.getAll();
  expect(all).toContainEqual(item);
  
  storage.close();
});
```

**Renderer test**

```javascript
const state = require('./modules/state');

test('state updates listeners', () => {
  const callback = jest.fn();
  state.onChange(callback);
  
  state.set([{ id: 1 }]);
  
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

You have two kinds of config in your desktop app. Keep them apart. Mixing them will hurt you:

- **Runtime mode**, you detect dev vs packaged with `app.isPackaged`, never `NODE_ENV`
  guesses. You drive log verbosity, dev tools, and update channels off it. One check. One truth.
- **User settings**, you persist in `app.getPath('userData')` (via `electron-store` or your
  storage layer), never next to the binary, which may be read-only. Respect the platform.

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

Your secrets (API keys, signing tokens) live in your **main** process from environment
variables at build/run time, never bundled into the renderer, where any user can read
them. You expose only the results over IPC.

---

## Summary

You separate your main and renderer processes strictly. No shortcuts.
You use contextIsolation and you disable nodeIntegration. That setting is your lock.
You namespace your IPC channels clearly. A name should say what it does.
You keep your modules small and focused. Small is testable. Small is honest.
You clean up your resources on exit. Leave the machine as you found it.
You use state management for your shared data. One place for the truth.

---

## Project Prompt

You build an Electron desktop app against the structure and rules above. Where they disagree
with your defaults, this file wins. Obey it.

You read `../standards/Principles.md` alongside this file before you start. Know your standards before you cut.

**Security (Non-Negotiable)**
- contextIsolation: true
- nodeIntegration: false
- Validate all IPC input on main process. Trust nothing from your renderer
- Namespace IPC channels: `domain:action`. The name tells the story

**IPC Patterns**
- Use invoke/handle for request-response. Ask, then answer
- Use send/on for fire-and-forget. No reply expected
- Clean error handling on both sides. Both ends own their failures

**Resource Management**
- Remove event listeners on cleanup. No loose ends
- Close database connections on exit. Close what you opened
- Save state before exit. Do not lose your user's work

### Setup

```bash
npm init -y
npm install electron
mkdir -p src/ui/modules assets/icons dist
```

### Deliverables

1. Complete project following architecture structure above. No missing pieces
2. Main process with system operations. It owns the system
3. Preload bridge with secure IPC. That bridge is your boundary
4. Renderer process with UI logic. It renders. It does not rule
5. Storage layer for persistence. Your data survives a restart
6. State management system. One truth for your UI
7. Custom window controls. Make them behave
8. package.json with build config. Your build stays repeatable
9. README with setup instructions. The next person thanks you

### Validation Checklist

- [ ] Verify commands from project AGENTS.md / README run (or honest manual checks listed)
- [ ] No secrets committed. Env examples use placeholders only

- [ ] Functions are small and single-purpose. Extract when a second concern appears (see Principles / skills/engineering/craft/SKILL.md)
- [ ] contextIsolation enabled. You leave it on
- [ ] nodeIntegration disabled. You leave it off
- [ ] No Node.js in renderer. Your renderer stays clean
- [ ] All IPC channels namespaced. Names tell the story
- [ ] Input validation on main process. You trust nothing
- [ ] Event listeners cleaned up. No loose ends
- [ ] Names match domain and local convention (skills/engineering/craft/SKILL.md)
- [ ] Resources freed properly. Close what you opened

### Security Checklist

- [ ] contextIsolation enabled. You leave it on
- [ ] nodeIntegration disabled. You leave it off
- [ ] webSecurity enabled. You leave it on
- [ ] No eval() or Function() in renderer. Your renderer stays clean
- [ ] CSP headers configured. Lock the door
- [ ] All IPC input validated. You trust nothing

### Pre-Delivery

```bash
npm run lint                  # no lint errors
npm test                      # main + renderer tests pass
npm start                     # launches; check the security checklist holds
npm run build                 # electron-builder packages without errors
```
