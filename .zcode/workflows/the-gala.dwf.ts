/* zcode-workflow
description: "THE GALA - the estate's self-steal + owed-work battery engine
  (amended from mickey17-v2 lineage). Three divisions ride one ballroom:
  A heads testify (mine fresh systems for laws, one LINKS row each),
  B the owed waltz (handoff work with byte finish lines, deadline first),
  C gravedigger (fossil handoffs get superseded receipts, no deletions).
  Wave-protocol laws dogfooded: receipt-per-attempt, lane fallback not queue
  death, refire-once, byte-check promotions, fold-by-counting-script."
whenToUse: "On an operator burn order. Pass slug + lanes ([{id, division,
  what, start, finish, evidence}]) with B lanes first (deadline order).
  Width rides max_concurrency on the run, NOT in asks - babystep ladder:
  probe 1-wide, then 3-wide, retune in place only when the evening is clean."
args:
  slug:
    type: string
    description: Run slug, e.g. gala-rung0 - names the lanes archive subdir
    required: true
  lanes:
    type: json
    description: "Array of {id, division (A|B|C), what, start, finish, evidence} - one lane per entry, B deadline-first"
    required: true
  width:
    type: number
    description: Informational lane count for the header log (actual width is the run's max_concurrency)
    required: false
    default: 3
*/
// max_concurrency: 3 (fan-out width law default; matches this script's own babystep ladder, probe 1-wide then 3-wide; ractor R1 fleet amendment 2026-10-05; declaration stamp, the firer still sets it at run time)
// judge-model: groq/compound-mini (B2-206 firing contract: the dwf facade has no per-subagent model, so the FIRER must set subagent_model groq/compound-mini at CreateWorkflow/AmendWorkflow time; cross-family from the GLM/zai session family per B2-60 D2)
// source-fetched: 2026-09-26 (t80: G6 dated-stamp amendment per t69 G6_STAMP_RE; receipt mentions in this script point at watch/inbox/; digests registered before this line are historical, the fresh gate row carries the live digest)
interface GalaRow {
  /** Short name of the law/steal mined. */
  law: string;
  /** One sentence: the claim worth keeping. */
  claim: string;
  /** VERBATIM quote, <=40 words, byte-copied from an estate file. */
  quote: string;
  /** Absolute estate path the quote was copied from. */
  source: string;
  /** One concrete one-seat-one-sitting action + landing spot. */
  steal: string;
  /** One falsifier: what observation would kill this law. */
  falsifier: string;
  /** high | medium | low */
  leverage: string;
}
interface GalaLaneOut {
  lane: string;
  division: string;
  ok: boolean;
  /** One sentence: what happened, gaps included, honestly. */
  note: string;
  /** Division A only: mined rows. */
  rows: GalaRow[];
  /** Byte checks actually run: command + exit + evidence file path. */
  checks: { command: string; exit: number; evidence: string }[];
  /** "no" or the decision this lane changed, named. */
  decision_changed: string;
  /** Absolute path of the lane JSON written to the archive. */
  artifact: string;
}
interface CheckFile {
  lane: string;
  /** Per-row verdicts: quote must entail claim. */
  supports: { claim: string; supports: string; reason: string }[];
  counts: Record<string, number>;
}
interface DeepCheck {
  row_key: string;
  verdict: "verified" | "unconfirmed" | "crashed";
  evidence: string;
}
interface FoldInfo {
  scoreboard: string;
  decision_ledger: string;
  parade: boolean;
  top_laws: { law: string; why: string }[];
}
interface ReviewVerdict {
  decision: "ACCEPT" | "REVISE";
  bullets: string[];
}
interface FilerInfo { verdict: string; links_appended: number }
interface WorkflowReport {
  conclusion: string;
  findings: { where: string; what: string; evidence: string; status: string; severity: string }[];
  verified: string[];
  notCovered: string[];
}

const ESTATE = "C:/Users/foste/Documents/projects/local_sovereign_agent";
const GALA_ROOT = ESTATE + "/watch/inbox/gala_20260925";
const SLUG = String(args.slug || "rung");
const LANES = GALA_ROOT + "/" + SLUG + "/lanes";
const FOLD_SH = GALA_ROOT + "/fold_gate.sh";

const ALL: { id: string; division: string; what: string; start: string; finish: string; evidence: string }[] =
  Array.isArray(args.lanes) ? (args.lanes as { id: string; division: string; what: string; start: string; finish: string; evidence: string }[]) : [];
if (ALL.length === 0) {
  throw new Error("no lanes passed");
}
// Deadline law: B (owed waltz) dances before A (heads) and C (graves), in the
// order the operator stacked them. Stable sort, control flow only - never ask text.
const ORDER: Record<string, number> = { B: 0, A: 1, C: 2 };
const TARGETS = ALL.slice().sort((a, b) => (ORDER[a.division] ?? 9) - (ORDER[b.division] ?? 9));

// The gala leaderboard, live while the run goes (dashboard is for the watcher).
artifact.board("gala", {
  title: "THE GALA " + SLUG + " - live scoreboard",
  key: "lane",
  status: "status",
  columns: ["dancing", "danced", "buried", "failed"],
  cardTitle: "lane",
  detail: [{ field: "division", label: "Div" }, { field: "note", label: "Note" }]
});
artifact.table("steals", {
  title: "Steals mined tonight (live)",
  columns: [
    { field: "lane", label: "Lane" },
    { field: "law", label: "Law" },
    { field: "steal", label: "Steal" },
    { field: "leverage", label: "Leverage" }
  ],
  key: "law"
});

const LAWS =
  "The record laws bind you: never fabricate - no invented quotes, paths, numbers, or verdicts; " +
  "and no em-dashes in anything you write for the record. A check you did not run is a claim, " +
  "not a verdict: run the command, save the raw output, cite the file. Negative results are " +
  "first-class. If a check is impossible or instructions contradict, say so plainly instead of faking.";

const LANE_SYS =
  "You are one lane of THE GALA, the estate's self-steal + owed-work battery. " + LAWS + " " +
  "You write ONLY your own lane file in the archive, INCREMENTALLY (Write tool, not heredocs), " +
  "so a mid-flight kill costs nothing already banked. If your lane file already exists, read it " +
  "first and finish the gap, never redo banked work.";

function divisionAsk(t: { id: string; division: string; what: string; start: string; finish: string; evidence: string }, refire: boolean, killReason: string): string {
  const head = refire
    ? "REFIRE (this lane died once: " + killReason + "). Same lane, one rewrite: take a different route. If it dies again you will be buried - file what you have.\n"
    : "";
  const common =
    head + "LANE: " + t.id + " (division " + t.division + ")\nARCHIVE: write your lane JSON to " + LANES + "/" + t.id + ".json " +
    "(mkdir -p the parent). Return the typed GalaLaneOut, artifact = that path.\n\n";
  if (t.division === "A") {
    return common +
      "HEAD TESTIMONY: " + t.what + "\nStart from: " + (t.start || "the estate grep below") + "\n" +
      (t.evidence ? "Prior byte evidence already on disk (read it first): " + t.evidence + "\n" : "") +
      "1. VERIFY: run this head's own check yourself via bash (its gate, tests, or parser), save raw output to " + LANES + "/" + t.id + ".check.txt, cite it in checks[]. The verdict is the exit code, not your opinion.\n" +
      "2. MINE up to 5 rows: {law, claim, quote (VERBATIM <=40 words byte-copied from an estate file, cite the absolute path), steal (one seat one sitting + landing spot), falsifier, leverage}. No byte-checked quote, no row.\n" +
      "3. ESTATE GREP >= 2 dirs: " + ESTATE + "/corpus/steal and " + ESTATE + "/memory/corpus - a zero-hit grep is a finding, record it.\n" +
      "4. DECISION LEDGER: name one decision this head's truth changes (or \"no\" if none - an honest no is a row, a fake yes is a lie).\n" +
      "5. Write the lane JSON incrementally; return the typed GalaLaneOut.";
  }
  if (t.division === "B") {
    return common +
      "THE OWED WALTZ: " + t.what + "\nStart from: " + (t.start || "read the pointers above") + "\n" +
      "FINISH LINE (byte-checked, absolute paths): " + (t.finish || "the lane's own receipt file") + "\n" +
      "1. Do the owed work. Edit only what the work needs.\n" +
      "2. Run the finish-line command(s), save raw output to " + LANES + "/" + t.id + ".check.txt, cite it in checks[].\n" +
      "3. If you touched code under mag/ or tools/: run " + ESTATE + "/.venv/Scripts/python.exe tools/violation_ratchet.py check --changed and cite the exit.\n" +
      "4. DECISION LEDGER: name the decision this dance closes or changes (or \"no\").\n" +
      "5. Write the lane JSON incrementally; return the typed GalaLaneOut (rows may be empty).";
  }
  return common +
    "GRAVEDIGGER: " + t.what + "\nStart from: " + (t.start || "the files named above") + "\n" +
    "1. Read the named handoff files. Declare each superseded/absorbed/fossil WITH the evidence pointer that justifies the burial (what superseded it, when).\n" +
    "2. Write one receipt per grave to " + ESTATE + "/watch/inbox/GALA_GRAVE_" + t.id + ".md (deletions are operator-gated: receipts only, touch nothing).\n" +
    "3. Write the lane JSON; return the typed GalaLaneOut (rows may be empty, finish = the grave receipts).";
}

function supportsAsk(t: { id: string }, rows: GalaRow[]): string {
  return (
    "Tier-1 supports-check (mechanical, textual entailment only). Lane " + t.id + " rows:\n" +
    JSON.stringify(rows.map((r) => ({ claim: r.claim, quote: r.quote }))) + "\n\n" +
    "For EVERY row judge: does the quote text, as written, entail the claim? A byte-perfect quote that does not " +
    "entail its claim is supports:\"no\". Do NOT re-read the estate; this is textual entailment only (tier 2 " +
    "does the byte-check). Write the CheckFile as JSON to " + LANES + "/" + t.id + ".checks.json so verdicts " +
    "persist for the recount, then return it. Never edit any other file."
  );
}

function deepAsk(laneId: string, r: GalaRow): string {
  return (
    "Tier-2 deep verifier - MECHANICAL ONLY. Do not trust this row.\n" +
    "Alleged quote: \"" + r.quote + "\"\nAlleged source file: " + r.source + "\n\n" +
    "grep -F for the quote text inside the file (allow whitespace normalization only; read the file if grep " +
    "misses on line wrapping). Then judge whether the file's context supports the claim. Return the typed " +
    "DeepCheck with row_key \"" + laneId + ": " + r.law + "\". Never edit any file."
  );
}

log("THE GALA " + SLUG + ": " + String(TARGETS.length) + " lanes (" +
    String(TARGETS.filter((t) => t.division === "B").length) + " waltz, " +
    String(TARGETS.filter((t) => t.division === "A").length) + " heads, " +
    String(TARGETS.filter((t) => t.division === "C").length) + " graves). Doorman holds the width; the journal is the width receipt.");

const refired: string[] = [];
const buried: string[] = [];
const laneOut: GalaLaneOut[] = [];
const laneChecks: CheckFile[] = [];

// G4 salvage: every landed lane is reported the moment it banks.
function bankLane(t: { id: string; division: string }, r: GalaLaneOut, status: string): void {
  laneOut.push(r);
  const it = { lane: t.id, division: t.division, ok: r.ok, note: String(r.note || "").slice(0, 120) };
  report(it);
  report({ lane: t.id, division: t.division, status: status, note: String(r.note || "").slice(0, 110) }, "gala");
  for (const row of (r.rows || []).filter((x) => x.leverage !== "low").slice(0, 3)) {
    report({ lane: t.id, law: row.law, steal: row.steal, leverage: row.leverage, claim: row.claim }, "steals");
  }
}

async function runLane(t: { id: string; division: string; what: string; start: string; finish: string; evidence: string }, refire: boolean, killReason: string): Promise<GalaLaneOut> {
  return await agent("gala-" + t.id + (refire ? "-refire" : ""), { system: LANE_SYS })
    .ask<GalaLaneOut>(divisionAsk(t, refire, killReason));
}

// Envelope hold (operations lane ractor50, 2026-09-30; law: AFTERPARTY_CLOSE_20260926
// B2-476 contract item 2 - "even a clean width takes 1302s until the window decays;
// hold fires ~10 min on 1302"). A lane death carrying the rate-limit shape means the
// window is mid-burst: the immediate refire the old code ran dies into the same burst
// (the 50-wide storm dwfrun-15738edf and the ~15-width afterparty deaths are the record),
// so hold ~10 min once before the single allowed refire. A hold spawn failure or timeout
// degrades to the old immediate refire, logged - worst case is the status quo.
async function rateLimitHold(killReason: string): Promise<void> {
  if (!/1302|429|rate.?limit/i.test(killReason)) return;
  try {
    await world.run("powershell", ["-NoProfile", "-Command", "Start-Sleep -Seconds 600"], { timeoutMs: 660000 });
    log("Rate-limit-shaped lane death; held ~10 min before refire (B2-476 rolling-throughput law).");
  } catch {
    log("Rate-limit hold spawn failed or timed out; refiring immediately (degraded, logged).");
  }
}

async function laneWithTiers(t: { id: string; division: string; what: string; start: string; finish: string; evidence: string }): Promise<void> {
  let res: GalaLaneOut | null = null;
  try {
    res = await runLane(t, false, "");
  } catch (e) {
    await rateLimitHold(String(e));
    try {
      refired.push(t.id);
      res = await runLane(t, true, String(e).slice(0, 140));
    } catch (e2) {
      buried.push(t.id + " (" + String(e2).slice(0, 100) + ")");
      report({ lane: t.id, division: t.division, status: "buried", note: String(e2).slice(0, 110) }, "gala");
      return;
    }
  }
  if (!res || res.ok === false) {
    if (res && ((res.rows || []).length > 0 || (res.checks || []).length > 0)) {
      bankLane(t, res, "danced");
    } else {
      refired.push(t.id);
      try {
        const r2 = await runLane(t, true, res && res.note ? res.note.slice(0, 140) : "empty result");
        if (r2 && ((r2.rows || []).length > 0 || (r2.checks || []).length > 0)) { bankLane(t, r2, "danced"); } else { buried.push(t.id); report({ lane: t.id, division: t.division, status: "failed", note: "empty on refire" }, "gala"); }
      } catch {
        buried.push(t.id);
        report({ lane: t.id, division: t.division, status: "failed", note: "refire crashed" }, "gala");
      }
    }
    return;
  }
  bankLane(t, res, "danced");
  const rows: GalaRow[] = Array.isArray(res.rows) ? res.rows : [];
  if (t.division === "A" && rows.length > 0) {
    try {
      const c = await agent("supports-" + t.id, { system: "Mechanical tier-1 checker. Textual entailment only. Persist the verdict file exactly as instructed." })
        .ask<CheckFile>(supportsAsk(t, rows));
      laneChecks.push(c);
    } catch {
      laneChecks.push({ lane: t.id, supports: [], counts: { crashed: rows.length } });
    }
  }
}

phase("Doors open: heads testify, the waltz dances, graves get dug");
await Promise.all(TARGETS.map((t) => laneWithTiers(t)));
const okLanes = laneOut.filter((l) => l.ok).length;
const changed = laneOut.filter((l) => String(l.decision_changed || "no") !== "no");
log("Ballroom count: " + String(okLanes) + "/" + String(TARGETS.length) + " lanes danced; refired " +
    String(refired.length) + ", buried " + String(buried.length) + "; decisions changed: " + String(changed.length) + ".");

phase("Count the ballroom: fold gate, then the fold");
// Cross-run fold mutex (2026-10-05, operator ask): concurrent workflow folds
// were colliding and erroring into retries. Acquire WAITS; on timeout (exit
// 4) proceed unlocked with shared appends via tools/ledger_lock.py. A script
// killed mid-fold clears at the 45-min stale-break.
const FOLD_GATE_PY = ESTATE + "/tools/fold_gate.py";
const FOLD_HOLDER = "the-gala:" + SLUG;
const foldGateAcq = await world.run("bash", ["-c", "\"" + ESTATE + "/.venv/Scripts/python.exe\" \"" + FOLD_GATE_PY + "\" acquire --holder \"" + FOLD_HOLDER + "\" --wait 900"], { timeoutMs: 960000 });
if (foldGateAcq.exitCode === 0) {
  log("Fold gate held by " + FOLD_HOLDER);
} else {
  log("Fold gate acquire exit " + String(foldGateAcq.exitCode) + " - proceeding UNLOCKED (timeout logged; shared appends only via tools/ledger_lock.py append)");
}
let gate = await world.run("bash", [FOLD_SH, LANES, String(TARGETS.length)], { timeoutMs: 300000 });
if (gate.exitCode !== 0) {
  log("Fold gate exited " + String(gate.exitCode) + " - one repair pass: " + (gate.stderr || gate.stdout || "no output").slice(0, 300));
  await agent("gate-repairer", { system: "You repair a counting-gate failure. Read the error, fix the DATA (missing/corrupt lane JSONs) so the tool exits 0; never weaken the tool's checks. Bash + Read are your tools." }).ask(
    "The GALA fold gate failed (exit " + String(gate.exitCode) + "). Script: " + FOLD_SH + " (args: lanes-dir expected-count). Archive: " + LANES + " - output tail:\n" +
    ((gate.stderr || gate.stdout || "none").slice(0, 2000)) + "\nDiagnose and repair so it exits 0."
  );
  gate = await world.run("bash", [FOLD_SH, LANES, String(TARGETS.length)], { timeoutMs: 300000 });
}
const gateClean = gate.exitCode === 0;
log("Fold gate exit " + String(gate.exitCode) + (gateClean ? "" : " - STILL FAILING, fold ships UNVERIFIED"));
const compact = JSON.stringify({
  danced: laneOut.map((l) => ({ lane: l.lane, division: l.division, ok: l.ok, decision: l.decision_changed, rows: (l.rows || []).length })),
  refired: refired,
  buried: buried
});
// Truncation lesson (operations lane ractor50, 2026-09-30): wave5-repair's fold
// scoreboard closing sentence arrived truncated in the run handoff and the tail was
// unrecoverable (watch/inbox/gala_20260925/wave5-repair_RECEIPT.md section 2), and
// ball-20260929 decision lines print "truncated at source". Caps below are raised so
// the gate sections and the fold JSON reach the fold and herald asks whole for
// gala-archive sizes; the receipt writer must never be the one who drops a tail.
const fold = await agent("folder", {
  system: "You fold gala archives into the scoreboard. Plain English. Your numbers come ONLY from the scripted gate sections; anything you bring yourself is tagged carried. Never average a contradiction."
}).ask<FoldInfo>(
  "The fold gate already counted the archive. Its sections (authoritative):\n" + gate.stdout.slice(0, 24000) + "\n\n" +
  "Run metadata: " + compact + "\n\n" +
  "Read " + LANES + " for full rows. Return: scoreboard (one line per division: danced/total + the standouts), " +
  "decision_ledger (every changed decision, or the word PARADE if none changed - say it plainly, the parade law binds), " +
  "top_laws (the 3 strongest mined laws with one why each - these are the ractor candidates), parade (boolean: zero decisions changed)."
);
const foldGateRel = await world.run("bash", ["-c", "\"" + ESTATE + "/.venv/Scripts/python.exe\" \"" + FOLD_GATE_PY + "\" release --holder \"" + FOLD_HOLDER + "\""], { timeoutMs: 120000 });
if (foldGateRel.exitCode !== 0) {
  log("Fold gate release exit " + String(foldGateRel.exitCode) + " - the 45-min stale-break will clear it if this holder died");
}

phase("Midnight reader walks the scoreboard");
const review = await agent("midnight-reader", {
  system: "Fresh reader. You have not seen this work. Judge the archive as a reader would. Do not fetch. At most 5 bullets."
}).ask<ReviewVerdict>(
  "Read " + LANES + " cold plus the fold metadata. Fixed form: (1) spot-check three quotes against their cited source paths - byte-match or not; " +
  "(2) is every claimed byte-check backed by a .check.txt on disk; (3) is the decision ledger honest (any decision_changed that names nothing real is a strike); " +
  "(4) are B-division finish lines actually met on disk; (5) did any lane claim another lane's work. Return ACCEPT or REVISE with at most 5 bullets."
);
if (review.decision === "REVISE") {
  await agent("fold-repairer", { system: "You apply review fixes to the archive. Edit tool only; change nothing else." }).ask(
    "Fix the gala archive at " + LANES + " per the midnight reader. Annotate struck claims, never delete rows.\n" +
    "Previous critique from the fresh reader (address every bullet):\n" + JSON.stringify(review.bullets)
  );
}

phase("File the ledger rows and hang the gala receipt");
const linksBlob = JSON.stringify(laneOut
  .filter((l) => (l.rows || []).length > 0 || String(l.decision_changed || "no") !== "no")
  .map((l) => ({ lane: l.lane, division: l.division, decision_changed: l.decision_changed, top: (l.rows || [])[0] || null })));
const filer = await agent("estate-filer", {
  system: "You file estate records. Sequential single-writer appends only; dedupe before appending; never fabricate; no em-dashes in filed text."
}).ask<FilerInfo>(
  "File tonight's GALA rows into memory/corpus/LINKS.jsonl (one LINKS row per lane that mined rows or changed a decision; kind 'gala', slug '" + SLUG + "', " +
  "src 'watch/inbox/gala_20260925/" + SLUG + "/lanes/<id>.json', title = the lane's top law or its changed decision; dedupe by src against existing rows first).\n" +
  "Lane summaries (read each lane JSON at " + LANES + " for full rows before writing):\n" + linksBlob.slice(0, 14000) + "\n\n" +
  "Then append ONE STATE entry to " + ESTATE + "/memories/session/next-window-handoff.md: slug '" + SLUG + "', danced count, decisions changed, B-division finish status, graves filed. " +
  "Return {verdict, links_appended}."
);
await agent("herald", {
  system: "You write gala receipts. Script numbers only; no em-dashes; never fabricate."
}).ask(
  "Write the run receipt to " + GALA_ROOT + "/" + SLUG + "_RECEIPT.md from these script-written sections (authoritative):\n" +
  gate.stdout.slice(0, 12000) + "\n\nMetadata: " + compact + "\nFold: " + JSON.stringify(fold).slice(0, 12000) +
  "\nReview: " + review.decision + " " + JSON.stringify(review.bullets) + "\nFiling: " + filer.verdict +
  "\nSections: header (slug, lane count, divisions), scoreboard, decision ledger (PARADE if the fold says so), refired + buried lists, review verdict, filing verdict."
);

try {
  await artifact.file("receipt", "watch/inbox/gala_20260925/" + SLUG + "_RECEIPT.md", { title: "THE GALA " + SLUG + " receipt", primary: true });
} catch {
  log("receipt publish fell back to fold summary - estate copy at " + GALA_ROOT + "/" + SLUG + "_RECEIPT.md");
}

const unconfirmed = laneOut.flatMap((l) => (l.rows || []).map((r) => ({ lane: l.lane, r: r })))
  .filter((x) => x.r.leverage === "high").slice(0, 12).map((x) => x);
const deepChecks: DeepCheck[] = await Promise.all(
  unconfirmed.map(async (x, i): Promise<DeepCheck> => {
    try {
      return await agent("deep-" + x.lane + "-" + String(i), { system: "Mechanical verifier: grep + read byte-check only. Never trust the row. Never edit files." }).ask<DeepCheck>(deepAsk(x.lane, x.r));
    } catch (e) {
      return { row_key: x.lane + ": crashed", verdict: "crashed", evidence: String(e).slice(0, 120) };
    }
  })
);

const unverified = deepChecks.filter((c) => c.verdict !== "verified");
return {
  conclusion: String(okLanes) + "/" + String(TARGETS.length) + " lanes danced (refired " + String(refired.length) +
    ", buried " + String(buried.length) + "); decisions changed: " + String(changed.length) +
    (fold.parade ? " - PARADE, say so" : "") + "; tier-2 verified " + String(deepChecks.length - unverified.length) + "/" + String(deepChecks.length) +
    " high-leverage rows; fold gate " + (gateClean ? "clean" : "FAILING") + "; review " + review.decision + "; filed: " + filer.verdict,
  findings: unverified.map((c) => ({ where: c.row_key, what: "high-leverage row not byte-confirmed", evidence: c.evidence, status: "unconfirmed", severity: "medium" })),
  verified: [
    "fold counts computed by " + FOLD_SH + " (exit " + String(gate.exitCode) + ") - numbers are script-written",
    "each lane's checks[] cite raw output saved under " + LANES,
    "tier-1 entailment verdicts persisted to <id>.checks.json; tier-2 byte-checks on high-leverage rows",
    "midnight reader verdict: " + review.decision,
    "LINKS rows appended single-writer by the filer: " + String(filer.links_appended)
  ],
  notCovered: [
    "medium/low rows carry tier-1 entailment only, no byte re-check",
    String(unverified.length) + " high-leverage rows unconfirmed/crashed - labeled, never used as support"
  ]
} as WorkflowReport;
