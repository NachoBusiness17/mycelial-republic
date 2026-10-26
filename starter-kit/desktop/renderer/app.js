// starter-kit desktop v0 renderer logic. Talks only to window.kit (preload).
'use strict';

// ---- tabs ------------------------------------------------------------------
const tabs = [
  ['tab-install', 'pane-install'],
  ['tab-surfaces', 'pane-surfaces'],
  ['tab-hermes', 'pane-hermes'],
];
for (const [tabId, paneId] of tabs) {
  document.getElementById(tabId).addEventListener('click', () => {
    for (const [t, p] of tabs) {
      document.getElementById(t).classList.toggle('active', t === tabId);
      document.getElementById(p).classList.toggle('active', p === paneId);
    }
  });
}

// ---- (a) installer stream --------------------------------------------------
const installOut = document.getElementById('install-out');
let firstLine = true;
window.kit.onInstallerOutput((line) => {
  if (firstLine) {
    installOut.textContent = '';
    firstLine = false;
  }
  installOut.textContent += line + '\n';
  installOut.scrollTop = installOut.scrollHeight;
});

document.getElementById('run-install').addEventListener('click', async () => {
  installOut.textContent = '[spawning] ';
  firstLine = false;
  const res = await window.kit.runInstaller();
  if (!res.started) installOut.textContent += res.reason + '\n';
  else installOut.textContent += res.command + ' ' + res.script + '\n';
});

// ---- (b) surfaces ----------------------------------------------------------
const bootOut = document.getElementById('boot-out');
document.getElementById('load-boot').addEventListener('click', async () => {
  const res = await window.kit.readSurface('BOOT.md');
  bootOut.textContent = res.ok ? res.text : '[read failed] ' + res.reason;
});

// ---- (c) hermes chat stub --------------------------------------------------
const chatLog = document.getElementById('chat-log');
function addLine(cls, who, text) {
  const p = document.createElement('p');
  p.className = 'chat-line ' + cls;
  const who_ = document.createElement('span');
  who_.className = 'chat-who';
  who_.textContent = who + ' ';
  p.appendChild(who_);
  p.appendChild(document.createTextNode(text));
  chatLog.appendChild(p);
  chatLog.scrollTop = chatLog.scrollHeight;
}
document.getElementById('chat-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const input = document.getElementById('chat-in');
  const said = input.value.trim();
  if (!said) return;
  input.value = '';
  addLine('', 'you:', said);
  const res = await window.kit.sendChat(said);
  if (res && res.stub) addLine('chat-stub', 'hermes (stub):', res.note);
  else addLine('chat-stub', 'hermes:', '[unexpected response]');
});
addLine('chat-stub', 'hermes (stub):',
  'offline. the live plug is integrations/hermes/hermes_client.py; it needs an operator key, so v0 sends nothing on the wire.');
