/* SEAT — the knot-centric ghost surface. Consumes the CURRENT ghost internals (not the
   crude old dashboard aggregates): sovereign (one call sees everything), ghost/control
   (the human-facing harness), health, chain (the verkle knot lattice), economy, and a
   reconcile view (desired vs actual). All SAME-ORIGIN (dashboard :8765 proxy), fast, no CORS.
   Resilient: every call has a timeout; a dead endpoint shows an honest error, never hangs. */
(function () {
  "use strict";
  const $ = (id) => document.getElementById(id);

  async function get(url, ms) {
    const ctl = new AbortController();
    const t = setTimeout(() => ctl.abort(), ms || 6000);
    try {
      const r = await fetch(url, { signal: ctl.signal, cache: "no-store" });
      if (!r.ok) throw new Error("HTTP " + r.status);
      return await r.json();
    } finally { clearTimeout(t); }
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g,
      (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }
  function pill(v) {
    if (v === true || /ok|up|online|healthy|pass|ready|true|running/i.test(v)) return '<span class="pill ok">ok</span>';
    if (/fail|down|offline|error|crash|bad|no|false|stale|degraded/i.test(v)) return '<span class="pill bad">' + esc(v) + "</span>";
    return '<span class="pill deg">' + esc(v) + "</span>";
  }
  function err(e) { return '<span class="err">✗ ' + esc(e.message || e) + "</span>"; }
  function kv(pairs) {
    return pairs.map(([k, v]) => '<div class="kv"><span class="k">' + esc(k) + "</span><span class=\"v\">" + v + "</span></div>").join("");
  }
  function setState(cls, txt) {
    const s = $("state"); s.className = cls; $("stateTxt").textContent = txt;
  }

  // ── Machine: the whole stack, one call (sovereign) ──
  function renderMachine(s) {
    const el = $("machine");
    if (!s) return (el.innerHTML = err("no sovereign payload"));
    const t = s.tokenomics || {}; const train = s.training || {}; const def = s.defense || {};
    const conn = s.connection || {}; const off = s.offense || {};
    el.innerHTML =
      '<div class="dot-row">' +
        '<span class="m">modules <b>' + esc(s.summary && s.summary.modules_online) + "/" + esc(s.summary && s.summary.modules_total) + "</b></span>" +
        '<span class="m">tokenomics <b>' + pill(t.status) + "</b></span>" +
        '<span class="m">training <b>' + pill(train.status) + "</b></span>" +
        '<span class="m">defense <b>' + pill(def.status) + "</b></span>" +
        '<span class="m">connection <b>' + pill(conn.status) + "</b></span>" +
        '<span class="m">preflight <b>' + esc(s.summary && s.summary.score) + "</b></span>" +
      "</div>" +
      kv([
        ["ghost :9000", esc(s.ghost_port)],
        ["frontier steal_now", esc((s.frontier || {}).steal_now)],
        ["top steal", esc((s.frontier || {}).top_steal || "—")],
        ["moa default", esc((((off || {}).moa || {}).default_models || []).join(", ") || "—")],
        ["routing", esc((((off || {}).routing || {}).models || []).join(", ") || "—")],
        ["boot", esc(s.boot_command || "—")],
      ]);
  }

  // ── Ghost · now: the human-facing control harness ──
  function renderGhost(g) {
    const el = $("ghost");
    if (!g) return (el.innerHTML = err("no ghost/control payload"));
    const scrum = g.scrum || {}; const rec = g.recurring || {};
    el.innerHTML = kv([
      ["scrum next", esc(scrum.next_title || "—")],
      ["backlog by status", esc((scrum.by_status && JSON.stringify(scrum.by_status)) || "—")],
      ["source", esc(g.source || "—")],
      ["recurring", "<span class='muted'>" + esc(JSON.stringify(rec).slice(0, 220)) + "</span>"],
    ]);
  }

  // ── Health ──
  function renderHealth(h) {
    const el = $("health");
    if (!h) return (el.innerHTML = err("no health payload"));
    const lanes = Array.isArray(h.lanes) ? h.lanes.join(", ") : (h.lanes != null ? esc(h.lanes) : "—");
    el.innerHTML = kv([
      ["ok", pill(h.ok)],
      ["status", esc(h.status || "?")],
      ["integral", pill(h.integral)],
      ["recording", pill(h.recording)],
      ["lanes", lanes],
    ]);
  }

  // ── Knot lattice: the verkle chain / tip (source-backed) ──
  function renderKnots(c) {
    const el = $("knots");
    if (!c) return (el.innerHTML = err("no chain payload"));
    const tip = c.tip || {}; const chain = c.chain || [];
    let html = kv([
      ["root", esc((tip.root || "").slice(0, 16) || "—")],
      ["n_leaves", esc(tip.n_leaves != null ? tip.n_leaves : "?")],
      ["last", esc(tip.last_filename || "—")],
    ]);
    if (chain.length) {
      html += "<br><table><tr><th>leaf</th><th>hash</th></tr>" +
        chain.slice(-10).map((k) => {
          const leaf = k.leaf || k.filename || k.name || "?";
          const hash = k.hash || k.leaf_hash || "";
          return "<tr><td><a href='/files/memory/biography/" + esc(leaf) + "'>" + esc(String(leaf).slice(0, 42)) + "</a></td>" +
                 "<td class='muted'>" + esc(String(hash).slice(0, 12)) + "</td></tr>";
        }).join("") + "</table>";
    } else {
      html += '<div class="empty">no knots in chain</div>';
    }
    el.innerHTML = html;
  }

  // ── Economy ──
  function renderEcon(e) {
    const el = $("econ");
    if (!e) return (el.innerHTML = err("no economy payload"));
    const t = e.tokenomics || e;
    el.innerHTML = kv([
      ["status", pill(t.status)],
      ["daily burn", esc(t.daily_burn != null ? t.daily_burn : "?")],
      ["monthly proj", esc(t.monthly_projection != null ? t.monthly_projection : "?")],
      ["trend", esc(t.trend || "?")],
      ["top arb", esc(t.top_arbitrage || "—")],
    ]);
  }

  // ── Reconcile: desired vs actual (the operator view) ──
  function renderReconcile(s, h) {
    const el = $("reconcile");
    const sum = s && s.summary;
    const desired = (sum && sum.modules_total) || 0;
    const actual = (sum && sum.modules_online) != null ? sum.modules_online : "?";
    const converged = (desired && actual === desired);
    el.innerHTML =
      '<div class="dot-row">' +
        '<span class="m">modules <b>' + esc(actual) + "/" + esc(desired) + "</b></span>" +
        '<span class="m">health <b>' + pill(h && h.ok) + "</b></span>" +
        '<span class="m">ready_to_boot <b>' + pill(sum && sum.ready_to_boot) + "</b></span>" +
      "</div>" +
      kv([
        ["desired modules", esc(desired)],
        ["actual online", esc(actual)],
        ["reconcile", converged ? '<span class="pill ok">converged</span>' : '<span class="pill deg">drifting</span>'],
        ["boot_command", esc((s && s.boot_command) || "—")],
      ]);
  }

  // ── Solved: what our history already holds (from internals) ──
  function renderSolved(s) {
    const el = $("solved");
    if (!s) return (el.innerHTML = err("no solved payload"));
    const tip = s.verkle_tip || {};
    const rows = (s.case_law || []).map((c) =>
      "<div class='kv'><span class='k'>" + esc(c.id || "") + "</span><span class='v'>" + esc((c.move || "").slice(0, 120)) + "</span></div>").join("");
    el.innerHTML =
      '<div class="dot-row">' +
        '<span class="m">case law <b>' + esc(s.n_case_law) + "</b></span>" +
        '<span class="m">rib maps <b>' + esc(s.n_rib) + "</b></span>" +
        '<span class="m">verkle leaves <b>' + esc(tip.n_leaves) + "</b></span>" +
      "</div>" +
      rows +
      '<div class="empty" style="margin-top:6px">' + esc(s.summary || "") + "</div>";
  }

  // ── Ecosystem: swarms + whole-ecosystem RIB (machine-readable, scannable) ──
  function renderEcosystem(e) {
    const el = $("ecosystem");
    if (!e) return (el.innerHTML = err("no ecosystem payload"));
    const sw = e.swarms || {};
    const roster = (sw.roster || []).map((r) =>
      '<span class="m" title="' + esc(r.status || "") + '">' + esc(r.name) +
      " " + (r.up ? '<span class="pill ok">up</span>' : '<span class="pill deg">down</span>') + "</span>"
    ).join("");
    const cost = e.cost || {};
    const sv = cost.saved_vs_projected || {};
    el.innerHTML =
      '<div class="dot-row">' + (roster || '<span class="m">no roster</span>') + "</div>" +
      kv([
        ["swarm up/down", esc((sw.summary && sw.summary.up) + "/" + (sw.summary && sw.summary.total)) || "?"],
        ["modules", esc(e.n_modules)],
        ["steal / knowledge", esc((e.steal || []).length)],
        ["skill_ledger", esc((e.ledgers || {}).skill_ledger)],
        ["memory_events", esc((e.ledgers || {}).memory_events)],
        ["memlang opcodes", esc(Object.keys(e.opcodes || {}).length)],
        ["tokens saved", esc(sv.tokens_saved != null ? sv.tokens_saved : "?")],
      ]) +
      '<div style="margin-top:8px;display:flex;gap:6px;flex-wrap:wrap">' +
        '<button class="btn" onclick="window.__scanEco()">scan (instant inference)</button>' +
      "</div>" +
      '<div id="eco-scan" class="empty" style="margin-top:6px"></div>';
  }

  async function scanEcosystem() {
    const el = document.getElementById("eco-scan");
    if (!el) return;
    el.innerHTML = "scanning…";
    try {
      const r = await fetch("/api/v1/ecosystem/scan", { signal: AbortSignal.timeout(8000), cache: "no-store" });
      const s = await r.json();
      if (!s || !s.ok) { el.innerHTML = err("scan failed"); return; }
      const inf = s.inference || {};
      const hand = s.handoffs || {};
      const handRow = Object.keys(hand).filter((k) => hand[k] && hand[k].ok).map((k) =>
        "<span class='m'><b>" + esc(k) + "</b>→" + esc(hand[k].anchor) + "</span>").join("");
      el.innerHTML =
        '<div class="dot-row">' +
          '<span class="m">swarms <b>' + esc(inf.swarms || "?") + "</b></span>" +
          '<span class="m">modules <b>' + esc(inf.n_modules) + "</b></span>" +
          '<span class="m">steal <b>' + esc(inf.n_steal) + "</b></span>" +
        "</div>" +
        '<div class="dot-row">memory handoffs: ' + (handRow || "<span class='m'>none</span>") + "</div>" +
        '<div class="empty" style="margin-top:4px">cost: ' + esc((s.cost && s.cost.note) || "") + "</div>";
    } catch (x) { el.innerHTML = err(x); }
  }
  window.__scanEco = scanEcosystem;

  async function load() {
    setState("deg", "loading machine…");
    // Fire all fetches; render EACH card as its own promise settles so the fast
    // internals (solved/health/economy) show immediately and the slow one-call
    // (sovereign) fills in when ready — never make the surface wait on the slowest.
    let settled = 0;
    const total = 7;
    const done = () => {
      settled++;
      if (settled >= total) setState("ok", "machine online");
      else setState("deg", "machine online (" + settled + "/" + total + " panes)");
    };
    get("/api/v1/solved", 6000).then(renderSolved).finally(done);
    get("/api/v1/health", 6000).then(renderHealth).finally(done);
    get("/api/v1/economy", 6000).then(renderEcon).finally(done);
    get("/api/v1/ghost/control", 6000).then(renderGhost).finally(done);
    get("/api/v1/chain", 6000).then(renderKnots).finally(done);
    get("/api/v1/ecosystem", 6000).then(renderEcosystem).finally(done);
    get("/api/v1/sovereign", 10000).then((s) => {
      renderMachine(s);
      renderReconcile(s, null);
    }).catch((e) => { $("machine").innerHTML = err(e); }).finally(done);
  }

  document.getElementById("refresh").onclick = load;
  document.getElementById("goHome").onclick = () => (location.href = "/?tab=home");
  load();
  setInterval(load, 10000);
})();
