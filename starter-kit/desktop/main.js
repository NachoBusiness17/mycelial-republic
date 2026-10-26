// starter-kit desktop v0: main process.
//
// Three duties, nothing else:
//   (a) run the kit installer script (../setup/install.ps1 | install.sh) and
//       stream its output lines to the INSTALL pane
//   (b) serve the kit's local surfaces (BOOT.md text via an allowlisted IPC
//       read; smith chart iframed straight from its local file)
//   (c) a Hermes chat handler that is an OFFLINE STUB to the plug
//       (starter-kit/integrations/hermes/hermes_client.py). It never opens a
//       socket in v0: the kit law is no live spend without an operator key,
//       and this process never holds one.
//
// Zero fetch: the window loads one local file, navigation is denied, no
// remote URL is ever loaded. Security shape per the Electron 41 checklist:
// contextIsolation + sandbox on, nodeIntegration off.
'use strict';

const { app, BrowserWindow, ipcMain } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const KIT_ROOT = path.resolve(__dirname, '..');
const SURFACES_DIR = path.join(__dirname, 'renderer', 'surfaces');

// surfaces:read allowlist: the only files the renderer may pull through IPC.
// Chromium blocks file:// fetch from a file:// page, so BOOT text rides this
// handle instead. No arbitrary reads.
const SURFACE_ALLOWLIST = new Set(['BOOT.md']);

let win = null;

function createWindow() {
  win = new BrowserWindow({
    width: 1280,
    height: 860,
    title: 'starter kit desk (v0)',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      webviewTag: false,
    },
  });
  // zero fetch in main form: one local file, no navigation, no popups.
  win.loadFile(path.join(__dirname, 'renderer', 'index.html'));
  win.webContents.setWindowOpenHandler(() => ({ action: 'deny' }));
  win.webContents.on('will-navigate', (e) => e.preventDefault());
}

// ---- (a) installer stream --------------------------------------------------

function installerCommand() {
  // Each platform gets the kit's own script, unmodified, cwd pinned to the
  // kit root (the scripts expect tools/kit_doctor.py relative to it).
  // ExecutionPolicy Bypass scopes this one spawn of the kit's own script.
  if (process.platform === 'win32') {
    const script = path.join(KIT_ROOT, 'setup', 'install.ps1');
    return { file: 'powershell.exe', args: ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', script] };
  }
  const script = path.join(KIT_ROOT, 'setup', 'install.sh');
  return { file: 'bash', args: [script] };
}

ipcMain.handle('installer:run', () => {
  if (!win || win.isDestroyed()) return { started: false, reason: 'no window' };
  const cmd = installerCommand();
  const script = cmd.args[cmd.args.length - 1];
  if (!fs.existsSync(script)) {
    return { started: false, reason: 'installer script not found: ' + script };
  }
  const child = spawn(cmd.file, cmd.args, { cwd: KIT_ROOT });
  const send = (line) => { if (win && !win.isDestroyed()) win.webContents.send('installer:output', line); };
  // line pump: forward complete lines from both channels as they arrive
  let buf = '';
  const pump = (chunk) => {
    buf += chunk.toString('utf8');
    let i;
    while ((i = buf.indexOf('\n')) >= 0) {
      send(buf.slice(0, i));
      buf = buf.slice(i + 1);
    }
  };
  child.stdout.on('data', pump);
  child.stderr.on('data', pump);
  child.on('error', (err) => send('[spawn error] ' + err.message));
  child.on('close', (code) => {
    if (buf) send(buf);
    send('[exit ' + code + ']');
  });
  return { started: true, command: cmd.file, script };
});

// ---- (b) local surfaces ----------------------------------------------------

ipcMain.handle('surfaces:read', (_e, name) => {
  if (typeof name !== 'string' || !SURFACE_ALLOWLIST.has(name)) {
    return { ok: false, reason: 'surface not allowlisted: ' + String(name) };
  }
  try {
    const text = fs.readFileSync(path.join(SURFACES_DIR, name), 'utf8');
    return { ok: true, name, text };
  } catch (err) {
    return { ok: false, reason: err.message };
  }
});

// ---- (c) hermes chat: stubbed to the plug, offline by design ---------------

ipcMain.handle('hermes:send', async (_e, text) => {
  const said = typeof text === 'string' ? text.slice(0, 500) : '';
  return {
    stub: true,
    echo: said,
    note: 'offline stub. the live fire leg lives in starter-kit/integrations/hermes/hermes_client.py; it refuses to run without an operator key, so this pane puts nothing on the wire in v0.',
  };
});

// ---- lifecycle -------------------------------------------------------------

app.whenReady().then(createWindow);
app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});
app.on('window-all-closed', () => app.quit());
