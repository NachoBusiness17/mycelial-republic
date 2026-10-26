#!/usr/bin/env node
// x_web_stage.js - stage posts on the logged-in x.com session: schedule
// natively (calendar picker) or save as draft. Nothing auto-sends.
// Usage:
//   node tools/x_web_stage.js probe <port>                     - dump composer + picker testids
//   node tools/x_web_stage.js reply <port> <tweetId> <textfile> <YYYY-MM-DDTHH:MM> [mode]
//   node tools/x_web_stage.js solo  <port> <textfile> <YYYY-MM-DDTHH:MM> [mode]
// mode: schedule (default) | draft. Receipt: CHURCH_CAMPAIGN_POSTED_20261018.md
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
  const [cmd, portS, mode, tweetId, textfile, when] = process.argv.slice(2);
  const port = Number(portS);
  if (cmd === 'probe') {
    // a2 = url to open
    const target = await jget(port, '/json/new?' + encodeURIComponent(a2), 'PUT');
    const ws = new WebSocket(target.webSocketDebuggerUrl);
    let id = 0; const pend = {};
    const send = (m, p) => new Promise(res => { const i = ++id; pend[i] = res; ws.send(JSON.stringify({ id: i, method: m, params: p || {} })); });
    ws.onmessage = ev => { const m = JSON.parse(ev.data); if (m.id && pend[m.id]) { pend[m.id](m.result || m.error); delete pend[m.id]; } };
    await new Promise(res => { ws.onopen = res; });
    await send('Page.enable'); await send('Runtime.enable');
    const evl = async (e, w) => { const r = await send('Runtime.evaluate', { expression: e, returnByValue: true, awaitPromise: true }); if (w) await new Promise(s => setTimeout(s, w)); return r && r.result ? r.result.value : null; };
    await new Promise(res => setTimeout(res, 8000));
    const reply = await evl('(()=>{const b=document.querySelector("article [data-testid=\\"reply\\"]");if(b){b.click();return true}return false})()', 1500);
    const typed = await evl('(()=>{const b=document.querySelector(\'[data-testid="tweetTextarea_0"]\');if(!b)return false;b.focus();document.execCommand("insertText",false,"probe text");return true})()', 800);
    const sched = await evl('(()=>{const b=[...document.querySelectorAll(\'[aria-label*="chedule" i],[data-testid*="sched" i]\')][0];if(b){b.click();return b.getAttribute("aria-label")||b.getAttribute("data-testid")}return null})()', 1500);
    const ids = await evl('[...document.querySelectorAll("[data-testid]")].map(e=>e.getAttribute("data-testid")).filter(t=>/date|time|confirm|sched/i.test(t)).slice(0,40)');
    const sels = await evl('JSON.stringify([...document.querySelectorAll("select")].map(s=>({id:(s.id||s.getAttribute("id")||"?"),n:s.options.length,opts:[...s.options].slice(0,3).map(o=>o.value+"|"+o.text)})))', 500);
    const inputs = await evl('[...document.querySelectorAll("input,select,[role=\\"combobox\\"]")].map(e=>({tag:e.tagName,id:e.id,testid:e.getAttribute("data-testid"),placeholder:e.placeholder||e.getAttribute("placeholder")||"",label:e.getAttribute("aria-label")||""})).slice(0,20)');
    console.log(JSON.stringify({ reply, typed, sched, ids, sels, inputs }, null, 1));
    process.exit(0);
  }
  // stage: node tools/x_web_stage.js stage <port> <mode reply|solo> <tweetId|-> <textfile> <YYYY-MM-DDTHH:MM>
  if (cmd === 'stage') {
    const tweetIdArg = tweetId === '-' ? '' : tweetId;
    const text = fs.readFileSync(textfile, 'utf-8').trim();
    if (!mode || !text || !when) { console.error('stage args missing'); process.exit(2); }
    const [d, t] = when.split('T');
    const [Y, M, D] = d.split('-');
    let [hh, mm] = t.split(':').map(s => String(parseInt(s, 10)));
    const ampm = Number(hh) >= 12 ? 'pm' : 'am';
    const h12 = String(Number(hh) % 12 === 0 ? 12 : Number(hh) % 12);
    const url = mode === 'reply'
      ? 'https://x.com/NachoQuixotic/status/' + tweetIdArg
      : 'https://x.com/compose/post';
    const target = await jget(port, '/json/new?' + encodeURIComponent(url), 'PUT');
    const ws = new WebSocket(target.webSocketDebuggerUrl);
    let id = 0; const pend = {};
    const send = (m, p) => new Promise(res => { const i = ++id; pend[i] = res; ws.send(JSON.stringify({ id: i, method: m, params: p || {} })); });
    ws.onmessage = ev => { const m = JSON.parse(ev.data); if (m.id && pend[m.id]) { pend[m.id](m.result || m.error); delete pend[m.id]; } };
    await new Promise(res => { ws.onopen = res; });
    await send('Page.enable'); await send('Runtime.enable');
    const evl = async (e, w) => {
      const r = await send('Runtime.evaluate', { expression: e, returnByValue: true, awaitPromise: true });
      if (w) await new Promise(s => setTimeout(s, w));
      if (r && r.exceptionDetails)
        throw new Error('page exception: ' + (r.exceptionDetails.exceptionDescription || r.exceptionDetails.text));
      return r && r.result ? r.result.value : null;
    };
    await new Promise(res => setTimeout(res, 9000));
    if (mode === 'reply') {
      const ok = await evl('(()=>{const b=document.querySelector("article [data-testid=\\"reply\\"]");if(b){b.click();return true}return false})()', 1500);
      if (!ok) throw new Error('reply button not found');
    }
    const typed = await evl('(()=>{const b=document.querySelector(\'[data-testid="tweetTextarea_0"]\');if(!b)return false;b.focus();document.execCommand("insertText",false,' + JSON.stringify(text) + ');return true})()', 800);
    if (!typed) throw new Error('composer not found');
    const sched = await evl('(()=>{const b=[...document.querySelectorAll(\'[aria-label*="chedule" i]\')][0];if(b){b.click();return true}return false})()', 1500);
    if (!sched) throw new Error('schedule control not found');
    // set the six native selects (React: native value setter + change event)
    const setSel = (idx, val) =>
      '(()=>{const s=document.getElementById("SELECTOR_' + idx + '");if(!s)return false;' +
      'const vs=Object.getOwnPropertyDescriptor(s.__proto__,"value").set;vs.call(s,' + JSON.stringify(val) + ');' +
      's.dispatchEvent(new Event("change",{bubbles:true}));return s.value===' + JSON.stringify(val) + '})()';
    for (const [idx, val] of [[1, String(Number(M))], [2, String(Number(D))], [3, Y], [4, h12], [5, mm], [6, ampm]]) {
      let ok = false;
      for (let attempt = 0; attempt < 4 && !ok; attempt++) {
        await evl('(()=>{const s=document.getElementById("SELECTOR_' + idx + '");return s? s.options.length : 0})()', 1200);
        ok = await evl(setSel(idx, val), 250);
      }
      if (!ok) throw new Error('SELECTOR_' + idx + ' did not take value ' + val);
    }
    const confirmed = await evl('(()=>{const b=document.querySelector(\'[data-testid="scheduledConfirmationPrimaryAction"]\');if(b&&!b.disabled){b.click();return true}return false})()', 2500);
    if (!confirmed) throw new Error('confirm button not found or disabled');
    const toast = await evl('(()=>{const t=document.body.innerText;return {scheduled: t.includes("scheduled"), count: (t.match(/scheduled/gi)||[]).length}})()', 500);
    console.log('STAGED ' + when + ' mode=' + mode + ' toast=' + JSON.stringify(toast));
    await jget(port, '/json/close/' + target.id).catch(() => {});
    process.exit(0);
  }
})().catch(e => { console.error('STAGE-FAIL', e.message); process.exit(1); });
