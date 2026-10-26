#!/usr/bin/env node
// cdp_eval.js - drive an existing CDP browser: open a URL, wait, evaluate JS, print result.
// Usage: node tools/cdp_eval.js <port> <url> <evalJs> [settleMs]
// The interaction-driver seat tool (posting replies, checking login state).
// Receipt: watch/inbox/CHURCH_CAMPAIGN_POSTED_20261018.md (the operator's
// order: post it yourself, headless browsers, no API keys).
'use strict';
const http = require('http');
const fs = require('fs');

function jget(port, path, method) {
  return new Promise((res, rej) => {
    const r = http.request({ host: '127.0.0.1', port, path, method: method || 'GET' },
      a => { let b = ''; a.on('data', c => b += c);
        a.on('end', () => { try { res(JSON.parse(b)); } catch (e) { rej(new Error('bad json: ' + b.slice(0, 120))); } }); });
    r.on('error', rej); r.end();
  });
}

(async () => {
  const [portS, url, evalJs, settleS] = process.argv.slice(2);
  const port = Number(portS), settleMs = Number(settleS) || 6000;
  if (!port || !url || !evalJs) {
    console.error('usage: node tools/cdp_eval.js <port> <url> <evalJs> [settleMs]');
    process.exit(2);
  }
  const target = await jget(port, '/json/new?' + encodeURIComponent(url), 'PUT');
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  let id = 0; const pend = {};
  const send = (method, params) => new Promise(res => {
    const i = ++id; pend[i] = res;
    ws.send(JSON.stringify({ id: i, method, params: params || {} }));
  });
  ws.onmessage = ev => {
    const m = JSON.parse(ev.data);
    if (m.id && pend[m.id]) { pend[m.id](m.result || m.error); delete pend[m.id]; }
  };
  await new Promise(res => { ws.onopen = res; });
  await send('Page.enable');
  await send('Runtime.enable');
  await new Promise(res => setTimeout(res, settleMs));
  const r = await send('Runtime.evaluate',
    { expression: evalJs, returnByValue: true, awaitPromise: true });
  if (r && r.exceptionDetails)
    console.log('EVAL-EXCEPTION: ' + JSON.stringify(r.exceptionDetails.exceptionDescription || r.exceptionDetails.text));
  else
    console.log(JSON.stringify(r && r.result ? r.result.value : null));
  await jget(port, '/json/close/' + target.id).catch(() => {});
  process.exit(0);
})().catch(e => { console.error('EVAL-FAIL', e.message); process.exit(1); });
