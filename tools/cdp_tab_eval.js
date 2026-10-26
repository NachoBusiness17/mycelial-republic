#!/usr/bin/env node
// cdp_tab_eval.js - attach to an EXISTING tab by URL substring and evaluate.
// Usage: node tools/cdp_tab_eval.js <port> <urlSubstring> <evalJs> [settleMs]
// Companion to cdp_eval.js (which opens fresh tabs); the SPA pages (x.com
// compose) live in their own tabs, so automation must attach, not reopen.
'use strict';
const http = require('http');

function jget(port, path, method) {
  return new Promise((res, rej) => {
    const r = http.request({ host: '127.0.0.1', port, path, method: method || 'GET' },
      a => { let b = ''; a.on('data', c => b += c);
        a.on('end', () => { try { res(JSON.parse(b)); } catch (e) { rej(new Error('bad json')); } }); });
    r.on('error', rej); r.end();
  });
}

(async () => {
  const [portS, urlSub, evalJs, settleS] = process.argv.slice(2);
  const port = Number(portS), settleMs = Number(settleS) || 2000;
  if (!port || !urlSub || !evalJs) {
    console.error('usage: node tools/cdp_tab_eval.js <port> <urlSubstring> <evalJs> [settleMs]');
    process.exit(2);
  }
  const tabs = await jget(port, '/json');
  const tab = tabs.filter(t => t.type === 'page' && t.url.includes(urlSub))
    .sort((a, b) => b.url.length - a.url.length)[0];
  if (!tab) { console.log('NO-TAB matching ' + urlSub + ' ; open pages: ' +
    tabs.filter(t => t.type === 'page').map(t => t.url.slice(0, 60)).join(' ;; ')); process.exit(3); }
  const ws = new WebSocket(tab.webSocketDebuggerUrl);
  let id = 0; const pend = {};
  const send = (m, p) => new Promise(res => { const i = ++id; pend[i] = res; ws.send(JSON.stringify({ id: i, method: m, params: p || {} })); });
  ws.onmessage = ev => { const m = JSON.parse(ev.data); if (m.id && pend[m.id]) { pend[m.id](m.result || m.error); delete pend[m.id]; } };
  await new Promise(res => { ws.onopen = res; });
  await send('Runtime.enable');
  const r = await send('Runtime.evaluate',
    { expression: evalJs, returnByValue: true, awaitPromise: true });
  if (r && r.exceptionDetails)
    console.log('EVAL-EXCEPTION: ' + (r.exceptionDetails.exceptionDescription || r.exceptionDetails.text));
  else
    console.log(JSON.stringify(r && r.result ? r.result.value : null));
  process.exit(0);
})().catch(e => { console.error('TAB-FAIL', e.message); process.exit(1); });
