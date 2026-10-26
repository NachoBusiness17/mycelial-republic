#!/usr/bin/env node
// x_web_reply.js - post a reply through the logged-in x.com web UI via CDP.
// Usage: node tools/x_web_reply.js <port> <tweetId> <textfile> [settleMs]
// Drives the real DOM: reply button, composer, execCommand insert, submit.
// The human session belongs to the operator; this tool only presses the
// buttons once the session exists. Receipt:
// watch/inbox/CHURCH_CAMPAIGN_DISPATCH_20261018.md
'use strict';
const http = require('http');
const fs = require('fs');

function jget(port, path, method) {
  return new Promise((res, rej) => {
    const r = http.request({ host: '127.0.0.1', port, path, method: method || 'GET' },
      a => { let b = ''; a.on('data', c => b += c);
        a.on('end', () => { try { res(JSON.parse(b)); } catch (e) { rej(new Error('bad json: ' + b.slice(0, 100))); } }); });
    r.on('error', rej); r.end();
  });
}

(async () => {
  const [portS, tweetId, textfile, settleS] = process.argv.slice(2);
  const port = Number(portS), settleMs = Number(settleS) || 9000;
  const text = fs.readFileSync(textfile, 'utf-8').trim();
  if (!port || !tweetId || !text) {
    console.error('usage: node tools/x_web_reply.js <port> <tweetId> <textfile> [settleMs]');
    process.exit(2);
  }
  const target = await jget(port, '/json/new?' +
    encodeURIComponent('https://x.com/NachoQuixotic/status/' + tweetId), 'PUT');
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
  const evl = async (expr, waitMs) => {
    const r = await send('Runtime.evaluate',
      { expression: expr, returnByValue: true, awaitPromise: true });
    if (waitMs) await new Promise(res => setTimeout(res, waitMs));
    if (r && r.exceptionDetails)
      throw new Error('page exception: ' + (r.exceptionDetails.exceptionDescription || r.exceptionDetails.text));
    return r && r.result ? r.result.value : null;
  };
  await new Promise(res => setTimeout(res, settleMs));
  const login = await evl(
    '(()=>{const s=document.querySelector(\'[data-testid="SideNav_AccountSwitcher_Button"]\');return !!s})()');
  if (!login) {
    console.log('NOT-LOGGED-IN: the session is not live yet; nothing posted.');
    await jget(port, '/json/close/' + target.id).catch(() => {});
    process.exit(3);
  }
  const replyBtn = await evl(
    '(()=>{const b=document.querySelector(\'article [data-testid="reply"]\');if(b){b.click();return true}return false})()', 1500);
  if (!replyBtn) throw new Error('reply button not found');
  const typed = await evl(
    '(()=>{const b=document.querySelector(\'[data-testid="tweetTextarea_0"]\');if(!b)return false;b.focus();document.execCommand("insertText",false,' +
    JSON.stringify(text) + ');return true})()', 800);
  if (!typed) throw new Error('composer not found');
  const submitted = await evl(
    '(()=>{const b=document.querySelector(\'[data-testid="tweetButtonInline"]\')||document.querySelector(\'[data-testid="tweetButton"]\');if(b&&!b.disabled){b.click();return true}return false})()', 4000);
  if (!submitted) throw new Error('submit button disabled or missing');
  const toast = await evl('document.body.innerText.includes("posted") || document.body.innerText.includes("Your post")');
  console.log('POSTED via web UI. toast=' + JSON.stringify(toast));
  await jget(port, '/json/close/' + target.id).catch(() => {});
  process.exit(0);
})().catch(e => { console.error('REPLY-FAIL', e.message); process.exit(1); });
