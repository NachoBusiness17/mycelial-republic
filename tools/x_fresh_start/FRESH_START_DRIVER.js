// ═══════════════════════════════════════════════════════════════════════════
// X FRESH START DRIVER — backup the social graph, then cull it. dfhack-style:
// runs INSIDE your logged-in x.com page, uses the page's own cookies. Your
// session, your hand, your machine. The seat never sees credentials.
//
// HOW TO RUN (5 steps, do it in a FRESH browser profile — not your daily one):
//   1. Open a new browser profile, log into x.com as @NachoQuixotic.
//   2. Go to  https://x.com/NachoQuixotic  (any page on x.com works).
//   3. Press F12 → Console tab. Paste this whole file. Press Enter.
//   4. Phase 1 auto-runs: walks your full Following list → downloads
//      nacho_following_backup_<date>.json  (KEEP THIS FILE — it is the record).
//   5. Phase 2 auto-runs after backup: unfollows everyone (or mutes — see
//      FLAGS). Progress checkpoints in localStorage; survives reload; if X
//      throttles, it cools down and resumes on its own. Close the tab to stop.
//
// FLAGS (set BEFORE pasting, e.g.  var KEEP = ["elonmusk","X"]; then paste):
//   var KEEP = ["handle1","handle2"]  → never touch these (the desk's keep-list)
//   var MUTE_ONLY = true              → mute instead of unfollow (instant clean
//                                       timeline, zero risk, unfollow later)
//   var PACE_MS = 2200                → avg ms between actions (default ~2.2s)
//
// HONEST RISK (one line): bulk unfollowing is ToS-gray — X may soft-throttle
// (driver handles it) and, if abused for weeks, could flag the account. Pace
// is deliberately human-ish. MUTE_ONLY is the zero-risk sibling.
// ═══════════════════════════════════════════════════════════════════════════

(async () => {
  const KEEP = window.KEEP || [];
  const MUTE_ONLY = window.MUTE_ONLY || false;
  const PACE_MS = window.PACE_MS || 2200;
  const ME = "NachoQuixotic";
  const sleep = (ms) => new Promise(r => setTimeout(r, ms));
  const jitter = () => PACE_MS * (0.7 + Math.random() * 0.9);
  const log = (...a) => console.log("%c[FRESH]", "color:#f59e0b;font-weight:bold", ...a);

  // The page's own auth: ct0 cookie IS the CSRF token; cookies carry the session.
  const CSRF = (document.cookie.match(/ct0=([^;]+)/) || [])[1];
  if (!CSRF) { console.error("No ct0 cookie — are you logged into x.com in THIS profile?"); return; }
  const H = { "x-csrf-token": CSRF, "content-type": "application/x-www-form-urlencoded" };
  const get = (u) => fetch(u, { headers: H, credentials: "include" }).then(r => r.json().then(j => ({ status: r.status, j })));
  const post = (u, body) => fetch(u, { method: "POST", headers: H, credentials: "include", body }).then(r => r.json().then(j => ({ status: r.status, j }))).catch(e => ({ status: 0, j: {} }));

  // ── PHASE 1: BACKUP — walk friends/list.json until cursor 0 ──────────────
  log("PHASE 1: backing up the social graph…");
  let graph = [], cursor = -1, guard = 0;
  while (cursor !== 0 && guard++ < 100) {
    const r = await get(`/i/api/1.1/friends/list.json?screen_name=${ME}&count=200&cursor=${cursor}&skip_status=1&include_user_entities=0`);
    if (r.status !== 200) { console.error("Backup fetch failed", r.status, r.j); return; }
    const users = r.j.users || [];
    graph.push(...users.map(u => ({ handle: u.screen_name, name: u.name, id: u.id_str, followers: u.followers_count })));
    cursor = r.j.next_cursor;
    log(`  backed up ${graph.length} (cursor ${cursor})`);
    await sleep(700);
  }
  const blob = new Blob([JSON.stringify({ backed_up_at: new Date().toISOString(), me: ME, count: graph.length, following: graph }, null, 1)], { type: "application/json" });
  const a = Object.assign(document.createElement("a"), { href: URL.createObjectURL(blob), download: `nacho_following_backup_${new Date().toISOString().slice(0, 10)}.json` });
  a.click();
  log(`PHASE 1 DONE: ${graph.length} follows backed up + downloaded. KEEP THIS FILE.`);

  if (MUTE_ONLY) log(`FLAGS: MUTE_ONLY — nobody gets unfollowed, only muted.`); else log(`FLAGS: UNFOLLOW. Keep-list: ${KEEP.length}`);
  if (!confirm(`Backup downloaded (${graph.length} follows).\n\nAbout to ${MUTE_ONLY ? "MUTE" : "UNFOLLOW"} everyone${KEEP.length ? ` except ${KEEP.length} kept` : ""}.\nContinue?`)) { log("Aborted by operator after backup. Graph is safe."); return; }

  // ── PHASE 2: CULL — paced destroy loop, checkpointed, throttle-aware ─────
  const done = new Set(JSON.parse(localStorage.getItem("freshstart_done") || "[]"));
  const save = () => localStorage.setItem("freshstart_done", JSON.stringify([...done]));
  const ep = MUTE_ONLY ? "/i/api/1.1/mutes/users/create.json" : "/i/api/1.1/friendships/destroy.json";
  let n = 0, cooldowns = 0;
  for (const u of graph) {
    if (done.has(u.id) || KEEP.includes(u.handle)) continue;
    const r = await post(ep, `user_id=${u.id}`);
    if (r.status === 429 || r.status === 403) {
      cooldowns++;
      if (cooldowns > 6) { log("Throttled 7x — stopping. Run again later (progress saved).", r.j); break; }
      log(`Throttle (${r.status}) — cooling 10 min… (${cooldowns}/6)`);
      await sleep(10 * 60 * 1000);
      continue;
    }
    done.add(u.id); n++;
    if (n % 25 === 0) { save(); log(`${MUTE_ONLY ? "muted" : "unfollowed"} ${n} (latest @${u.handle})`); }
    await sleep(jitter());
  }
  save();
  log(`PHASE 2 DONE: ${n} ${MUTE_ONLY ? "muted" : "unfollowed"} this run, ${done.size} total. Backup file + localStorage hold everything.`);
  log("Fresh start complete. Re-follow the keep-list from the desk audit whenever ready.");
})();
