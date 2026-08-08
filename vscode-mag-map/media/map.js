// MAG Framework Map — webview client.
// Regroups the framework BY FUNCTION, with curated descriptions and
// hover tooltips that show an example card of how each entry is used.
(function () {
  const vscode = acquireVsCodeApi();
  let all = [];
  let groups = [];
  let state = { search: "", group: "" };

  const listEl = document.getElementById("list");
  const rootEl = document.getElementById("mh-root");
  const statsEl = document.getElementById("stats");
  const countEl = document.getElementById("f-count");
  const searchEl = document.getElementById("search");
  const kindEl = document.getElementById("kind");
  const refreshEl = document.getElementById("refresh");
  const tipEl = document.getElementById("tip");
  const srcEl = document.getElementById("f-source");

  function esc(s) {
    return String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  }

  function groupMeta(id) {
    return groups.find((g) => g.id === id) || { id, icon: "▪", label: id, blurb: "" };
  }

  function filtered() {
    const q = state.search.trim().toLowerCase();
    return all.filter((it) => {
      if (state.group && it.group !== state.group) return false;
      if (!q) return true;
      return (
        it.name.toLowerCase().includes(q) ||
        (it.help || "").toLowerCase().includes(q) ||
        (it.desc || "").toLowerCase().includes(q) ||
        (it.example || "").toLowerCase().includes(q) ||
        (it.file || "").toLowerCase().includes(q)
      );
    });
  }

  function populateKind() {
    kindEl.innerHTML = "";
    const none = document.createElement("option");
    none.value = "";
    none.textContent = "all functions";
    kindEl.appendChild(none);
    for (const g of groups) {
      const o = document.createElement("option");
      o.value = g.id;
      o.textContent = `${g.icon} ${g.label} — ${g.blurb}`;
      kindEl.appendChild(o);
    }
  }

  function render() {
    const items = filtered();
    const buckets = {};
    for (const it of items) {
      (buckets[it.group] = buckets[it.group] || []).push(it);
    }
    const order = groups.map((g) => g.id);
    listEl.innerHTML = "";
    for (const id of order) {
      const bucket = buckets[id];
      if (!bucket) continue;
      const meta = groupMeta(id);
      const label = document.createElement("div");
      label.className = "group-label";
      label.innerHTML =
        `<span class="gi">${meta.icon}</span> <span class="gl">${esc(meta.label)}</span>` +
        `<span class="gb">— ${esc(meta.blurb)}</span> <span class="gc">${bucket.length}</span>`;
      listEl.appendChild(label);
      for (const it of bucket) listEl.appendChild(card(it));
    }
    if (!items.length) {
      const d = document.createElement("div");
      d.className = "empty";
      d.textContent = "nothing matches — try another filter";
      listEl.appendChild(d);
    }
    const counts = {};
    for (const it of all) counts[it.group] = (counts[it.group] || 0) + 1;
    statsEl.innerHTML =
      groups
        .filter((g) => counts[g.id])
        .map((g) => `<span><b>${counts[g.id]}</b> ${g.icon}${g.label}</span>`)
        .join("") || "";
    countEl.textContent = `${items.length} / ${all.length} commands`;
  }

  function showTip(it, ev) {
    const meta = groupMeta(it.group);
    let html = `<div class="tip-head">${meta.icon} ${esc(meta.label)} · <code>${esc(it.name)}</code></div>`;
    html += `<div class="tip-desc">${esc(it.desc || it.help || "")}</div>`;
    if (it.example) {
      html += `<div class="tip-label">example</div><pre class="tip-example">${esc(it.example)}</pre>`;
    }
    if (it.file) {
      html += `<div class="tip-file">${esc(it.file)}${it.line ? ":" + it.line : ""}</div>`;
    }
    tipEl.innerHTML = html;
    tipEl.hidden = false;
    positionTip(ev);
  }

  function positionTip(ev) {
    const pad = 12;
    const tw = tipEl.offsetWidth || 320;
    const th = tipEl.offsetHeight || 160;
    let x = ev.clientX + 14;
    let y = ev.clientY + 14;
    if (x + tw > window.innerWidth - pad) x = ev.clientX - tw - 14;
    if (y + th > window.innerHeight - pad) y = window.innerHeight - th - pad;
    if (x < pad) x = pad;
    if (y < pad) y = pad;
    tipEl.style.left = x + "px";
    tipEl.style.top = y + "px";
  }

  function hideTip() {
    tipEl.hidden = true;
  }

  function card(it) {
    const el = document.createElement("div");
    el.className = "card";
    const meta = groupMeta(it.group);

    const chip = document.createElement("span");
    chip.className = `kind-chip chip-${it.group}`;
    chip.textContent = `${meta.icon} ${meta.label}`;
    chip.title = meta.label;

    const body = document.createElement("div");
    body.className = "card-body";
    body.innerHTML = `<div class="card-name"><code>${esc(it.name)}</code></div><div class="card-help">${esc(it.help)}</div>`;

    const actions = document.createElement("div");
    actions.className = "card-actions";

    if (it.run) {
      const run = document.createElement("button");
      run.className = "btn btn-run";
      run.title = "run in terminal";
      run.textContent = "▶";
      run.addEventListener("click", (e) => {
        e.stopPropagation();
        vscode.postMessage({ type: "run", cmd: it.run });
      });
      actions.appendChild(run);
    }
    if (it.file) {
      const open = document.createElement("button");
      open.className = "btn";
      open.title = "open file";
      open.textContent = "⧉";
      open.addEventListener("click", (e) => {
        e.stopPropagation();
        vscode.postMessage({ type: "open", file: it.file, line: it.line });
      });
      actions.appendChild(open);
    }

    el.appendChild(chip);
    el.appendChild(body);
    el.appendChild(actions);

    el.addEventListener("mouseenter", (e) => showTip(it, e));
    el.addEventListener("mousemove", (e) => positionTip(e));
    el.addEventListener("mouseleave", hideTip);

    el.addEventListener("dblclick", () => {
      if (it.run) vscode.postMessage({ type: "run", cmd: it.run });
    });
    return el;
  }

  searchEl.addEventListener("input", () => {
    state.search = searchEl.value;
    render();
  });
  kindEl.addEventListener("change", () => {
    state.group = kindEl.value;
    render();
  });
  refreshEl.addEventListener("click", () => vscode.postMessage({ type: "ready" }));

  window.addEventListener("message", (ev) => {
    const msg = ev.data;
    if (msg.type === "data") {
      all = msg.data.items || [];
      groups = msg.data.groups || [];
      rootEl.textContent = msg.data.root || "";
      srcEl.textContent = msg.source === "framework" ? "framework" : "offline scan";
      srcEl.className = "mf-src " + (msg.source === "framework" ? "on" : "off");
      populateKind();
      render();
    }
  });

  vscode.postMessage({ type: "ready" });
})();
