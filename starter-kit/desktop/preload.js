// starter-kit desktop v0: preload.
// The only bridge between the sandboxed renderer and the main process.
// Exposes exactly four functions; the renderer never sees Node.
'use strict';

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('kit', {
  // (a) installer: fire once, then subscribe to streamed lines
  runInstaller: () => ipcRenderer.invoke('installer:run'),
  onInstallerOutput: (cb) => {
    const listener = (_e, line) => cb(line);
    ipcRenderer.on('installer:output', listener);
    return () => ipcRenderer.removeListener('installer:output', listener);
  },
  // (b) surfaces: allowlisted local file text (BOOT.md)
  readSurface: (name) => ipcRenderer.invoke('surfaces:read', name),
  // (c) hermes chat: stubbed to the plug, offline in v0
  sendChat: (text) => ipcRenderer.invoke('hermes:send', text),
});
