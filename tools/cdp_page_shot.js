#!/usr/bin/env node
// cdp_page_shot.js — screenshot any URL through the estate's bridge Chrome
// (CDP port 9222, the empir3 headless bridge). Zero deps: node >= 22 built-in
// WebSocket. The visual-verifier seat tool: render the thing, look at the
// bytes, never claim a page works off a parse check alone.
//
// Usage: node tools/cdp_page_shot.js <url> <out.png> [settleMs] [evalJs] [vw] [vh]
//   url may be http(s) or file://
//   evalJs: JS to evaluate in the page before the shot (race buttons, states)
//   vw/vh: viewport size (default 990x1320)
// Prints JS exceptions + console errors from the page before the shot.
//
// Built 2026-10-18 for the standing-wave strip falsifier
// (dashboard/static/smith_chart.html v1.2); receipt:
// watch/inbox/SMITH_STRIP_EULER_WAVE_20261018.md
'use strict';
const http = require('http');
const fs = require('fs');

const CDP_HOST = '127.0.0.1', CDP_PORT = 9222;

function jget(path, method) {
  return new Promise((res, rej) => {
    const r = http.request({ host: CDP_HOST, port: CDP_PORT, path, method: method || 'GET' },
      a => { let b = ''; a.on('data', c => b += c);
        a.on('end', () => { try { res(JSON.parse(b)); } catch (e) { rej(new Error('bad json from ' + path + ': ' + b.slice(0, 120))); } }); });
    r.on('error', rej); r.end();
  });
}

(async () => {
  const [url, out, settleArg, evalJs, vwArg, vhArg] = process.argv.slice(2);
  const settleMs = Number(settleArg) || 1500;
  const vw = Number(vwArg) || 990, vh = Number(vhArg) || 1320;
  if (!url || !out) {
    console.error('usage: node tools/cdp_page_shot.js <url> <out.png> [settleMs=1500] [evalJs] [vw=990] [vh=1320]');
    process.exit(2);
  }
  const target = await jget('/json/new?' + encodeURIComponent(url), 'PUT');
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  let id = 0; const pend = {};
  const send = (method, params) => new Promise(res => {
    const i = ++id; pend[i] = res;
    ws.send(JSON.stringify({ id: i, method, params: params || {} }));
  });
  const pageErrors = [];
  ws.onmessage = ev => {
    const m = JSON.parse(ev.data);
    if (m.method === 'Runtime.exceptionThrown')
      pageErrors.push('EXCEPTION: ' + JSON.stringify(m.params.exceptionDetails.exceptionDescription || m.params.exceptionDetails.text));
    if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error')
      pageErrors.push('CONSOLE.ERROR: ' + m.params.args.map(a => a.value || a.description || '').join(' '));
    if (m.id && pend[m.id]) { pend[m.id](m.result || m.error); delete pend[m.id]; }
  };
  await new Promise(res => { ws.onopen = res; });
  await send('Page.enable');
  await send('Runtime.enable');
  await send('Emulation.setDeviceMetricsOverride',
    { width: vw, height: vh, deviceScaleFactor: 1, mobile: false });
  await new Promise(res => setTimeout(res, settleMs));
  if (evalJs){
    const r = await send('Runtime.evaluate', { expression: evalJs, returnByValue: true });
    if (r && r.exceptionDetails)
      console.log('EVAL-EXCEPTION: ' + JSON.stringify(r.exceptionDetails.exceptionDescription || r.exceptionDetails.text));
    await new Promise(res => setTimeout(res, 700));
  }
  const shot = await send('Page.captureScreenshot', { format: 'png' });
  if (!shot || !shot.data) { console.error('SHOT-FAIL: no screenshot data', JSON.stringify(shot)); process.exit(1); }
  fs.writeFileSync(out, Buffer.from(shot.data, 'base64'));
  pageErrors.forEach(e => console.log(e));
  console.log('SHOT-OK ' + out + ' target=' + target.id + ' pageErrors=' + pageErrors.length);
  await jget('/json/close/' + target.id).catch(() => {});
  process.exit(0);
})().catch(e => { console.error('SHOT-FAIL', e.message); process.exit(1); });
