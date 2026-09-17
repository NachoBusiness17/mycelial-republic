
"use strict";
const D = JSON.parse(document.getElementById('deck-data').textContent);
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const chip = (t, cls) => `<span class="chip ${cls}">${esc(t)}</span>`;

function kpi(k, v, cls) {
  return `<div class="kpi"><div class="k">${esc(k)}</div><div class="v ${cls || 'small'}">${v}</div></div>`;
}

function standingWave() {
  const g = D.ledgers.grounding, ix = D.ledgers.index, w = D.wave, cp = D.context_pack;
  const vCls = g.verify_ok ? 'good' : 'bad';
  return `<section id="standing-wave"><h2>STANDING WAVE <span class="n">// era 003 · THE POUR</span></h2>
  <div class="strip">
    ${kpi('GROUNDING WAVE VERIFY', `<span class="${vCls}">${esc(g.verify_line)}</span>`)}
    ${kpi('GROUNDING ROWS', g.rows)}
    ${kpi('WAVE RECEIPTS INDEXED', w.receipts_indexed == null ? '?' : w.receipts_indexed)}
    ${kpi('INDEX HEALTH (the F)', ix.ok === true ? '<span class="good">OK</span>' : ix.ok === false ? '<span class="bad">NOT OK</span>' : '<span class="warn">UNKNOWN</span>',
         ix.ok ? 'good' : 'bad')}
    ${kpi('INDEX ERRORS', ix.errors == null ? esc(ix.error || '?') : ix.errors, ix.errors ? 'bad' : '')}
    ${kpi('GIT TIP', esc((D.git[0] || '?').split(' ')[0]))}
    ${kpi('CONTEXT PACK', `tip ${esc(cp.tip)} · leaves ${cp.leaves == null ? '?' : cp.leaves}`)}
  </div>
  <div class="src">sources: ${g.path} · watch/inbox/wave_20260916/WAVE_STATE_20260916.md · watch/inbox/INDEX.json · memory/context_pack_latest.md · git log -5</div>
  <ul style="margin-top:10px">${D.git.map(l => `<li class="wrap">${esc(l)}</li>`).join('')}</ul></section>`;
}

function programs() {
  return `<section id="programs"><h2>PROGRAMS <span class="n">// six</span></h2><div class="grid cards">` +
    D.programs.map(p => `<div class="card"><h3>${esc(p.title)}${chip(p.gate, 'gate')}</h3>
      <div class="st">${esc(p.status)}</div><p>${esc(p.detail)}</p>
      <ul>${p.facts.map(f => `<li>${esc(f)}</li>`).join('')}</ul>
      <div class="src">sources: ${p.sources.map(s => esc(s)).join(' · ')}</div></div>`).join('') +
    '</div></section>';
}

function lanes() {
  const order = {LIVE: 0, STALE: 1, 'NO-RUNNER': 2, DORMANT: 3};
  const rows = D.lanes.slice().sort((a, b) => (order[a.state] - order[b.state]) || a.name.localeCompare(b.name));
  const live = rows.filter(l => l.state === 'LIVE').length;
  return `<section id="lanes"><h2>LIVE LANES <span class="n">// ${live}/${rows.length} live</span></h2>
  <table><tr><th>LANE</th><th>STATE</th><th>LAST RUN</th><th>RESULT</th><th>TRAIL</th><th>LAST EVENT</th></tr>` +
    rows.map(l => `<tr><td class="lane"><span class="dot" style="background:${l.color}"></span>${esc(l.name)}</td>
      <td>${chip(l.state, l.state === 'LIVE' ? 'ok' : l.state === 'STALE' ? 'gate' : 'bad')}</td>
      <td>${esc(l.last_run) + (l.age_days == null ? '' : ` <span class="src">(+${l.age_days}d)</span>`)}</td>
      <td class="wrap">${esc(l.last_result)}</td>
      <td>${l.trail_rows} rows</td><td class="wrap">${esc(l.last_event)}</td></tr>`).join('') +
    '</table><div class="src">sources: queue/lanes/*/runner_state.json + trail.jsonl · LIVE = ran within 24h, STALE ≤ 3d, DORMANT older</div></section>';
}

function receipts() {
  return `<section id="receipts"><h2>RECEIPTS <span class="n">// latest ${D.receipts.length} by mtime</span></h2>
  <table><tr><th>WHEN</th><th>RECEIPT</th><th>STATUS</th></tr>` +
    D.receipts.map(r => `<tr><td>${esc(r.date)}</td><td><a class="wrap" href="../../${esc(r.path)}">${esc(r.name)}</a><div class="src wrap">${esc(r.title)}</div></td>
      <td class="wrap">${esc(r.status) || '<span class="src">—</span>'}</td></tr>`).join('') +
    '</table><div class="src">links resolve from file:// (repo-relative ../../watch/…); when served from /static the paths are still the canonical locations</div></section>';
}

function ledgers() {
  const L = D.ledgers, l5 = L.links.last5.map(r => `<li class="wrap">${esc(r.ts || '')} <a href="${esc(r.url)}">${esc(r.url)}</a></li>`).join('');
  return `<section id="ledgers"><h2>LEDGERS <span class="n">// counts + claim statuses</span></h2><div class="grid cards">
    <div class="card"><h3>LINKS LEDGER</h3><p><span class="v" style="font-size:20px;color:var(--hi)">${L.links.rows}</span> rows</p>
      <ul>${l5}</ul><div class="src">${esc(L.links.path)}</div></div>
    <div class="card"><h3>GROUNDING WAVE</h3><p><span class="v" style="font-size:20px;color:var(--hi)">${L.grounding.rows}</span> rows · verify: <span class="${L.grounding.verify_ok ? 'good' : 'bad'}">${esc(L.grounding.verify_line)}</span></p>
      <ul><li>chain broken at row 122 (prev-hash mismatch) — repair lane owed</li></ul><div class="src">${esc(L.grounding.path)}</div></div>
    <div class="card"><h3>SHARED SURFACE INDEX</h3><ul>
      <li>ok: <span class="${L.index.ok ? 'good' : 'bad'}">${L.index.ok == null ? 'unknown' : L.index.ok}</span></li>
      <li>files ${L.index.files == null ? '?' : L.index.files} · indexed ${L.index.indexed == null ? '?' : L.index.indexed} · unindexed ${L.index.unindexed == null ? '?' : L.index.unindexed}</li>
      <li>errors <span class="bad">${L.index.errors == null ? '?' : L.index.errors}</span> · warnings ${L.index.warnings == null ? '?' : L.index.warnings}</li>
    </ul><div class="src">${esc(L.index.path)}</div></div>
    <div class="card"><h3>SAMPLER CLAIM</h3><p>${chip('CONDITIONAL-REFUTED', 'gate')}</p>
      <ul><li>probe: ρ +0.167, n=8, p=0.70 — wrong-signed</li>
      <li>replicate: ρ +0.327, n=36, p=0.052 — past the +0.3 line, but a graze</li>
      <li>U5 witness: refutation CONDITIONAL on formal closure receipt (threshold provenance + variable definitions filed together)</li>
      <li>salon_50 = 39/50 answered, NOT 50/50 (fossil, 55 occurrences in the wild)</li></ul>
      <div class="src">watch/inbox/physical_computing/PHYSICAL_COMPUTING_PACK_20260916.md §6 · WAVE_STATE §3</div></div>
  </div></section>`;
}

function surfaces() {
  return `<section id="surfaces"><h2>SURFACES <span class="n">// ${D.surfaces.length + D.games.length} linked · existence-checked at build</span></h2>
  <div class="grid cards">` +
    D.games.map(g => `<div class="card"><h3>${esc(g.name)}</h3><p>${esc(g.desc)}</p>
      <div class="src"><a href="${esc(g.href)}">open ${esc(g.href)}</a>${g.exists ? '' : ' <span class="bad">MISSING</span>'}</div></div>`).join('') +
    D.surfaces.map(s => `<div class="card"><h3>${esc(s.name)}</h3><p>${esc(s.desc)}</p>
      <div class="src"><a href="${esc(s.href)}">open ${esc(s.href)}</a>${s.exists ? '' : ' <span class="bad">MISSING</span>'}</div></div>`).join('') +
    '</div><div class="src">relative links work from file:// and from /static/deck.html</div></section>';
}

function nextStones() {
  const cls = k => k === 'OPERATOR-GATE' ? 'bad' : k === 'GEN-2' ? 'gate' : k === 'CLOSURE' ? 'gate' : 'ok';
  return `<section id="next-stones"><h2>NEXT STONES <span class="n">// gen-2 requeue + operator gates</span></h2>
  <table><tr><th>KIND</th><th>ITEM</th><th>ASK</th></tr>` +
    D.next_stones.map(s => `<tr><td>${chip(s.kind, cls(s.kind))}</td><td class="wrap">${esc(s.item)}</td><td class="wrap">${esc(s.ask)}</td></tr>`).join('') +
    '</table><div class="src">sources: WAVE_STATE_20260916.md §4 + program receipts</div></section>';
}

const SECTIONS = [
  ['standing-wave', 'STANDING WAVE', standingWave],
  ['programs', 'PROGRAMS', programs],
  ['lanes', 'LIVE LANES', lanes],
  ['receipts', 'RECEIPTS', receipts],
  ['ledgers', 'LEDGERS', ledgers],
  ['surfaces', 'SURFACES', surfaces],
  ['next-stones', 'NEXT STONES', nextStones],
];
document.getElementById('main').innerHTML = SECTIONS.map(s => s[2]()).join('');
document.getElementById('nav').innerHTML = SECTIONS.map(s => `<a href="#${s[0]}">${s[1]}</a>`).join('');
