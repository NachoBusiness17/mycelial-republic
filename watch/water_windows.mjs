#!/usr/bin/env node
/**
 * water_windows.mjs — the watercomputer window clock (v0)
 *
 * Operator vision (11:33Z): countdowns for every quota/window so the mycelial
 * network knows its own limits — when windows are used up, when they free again.
 * Watercomputer style: deterministic, $0, wall-clock + receipts only.
 *
 * Windows tracked (each = reservoir with level + refill rule):
 *  - deepseek offpeak : open 18:00-09:00 Beijing weekdays + all weekend; half price; closes at 09:00 BJ
 *  - zai_half_price   : operator receipt 08-31: 50% off until 2026-09-09
 *  - groq_oss         : 30 RPM / 1K RPD / 200K TPD org (resets daily ~00:00 UTC)
 *  - cerebras         : 5 RPM / 30K TPM / 1M TPD (resets daily)
 *  - or_free          : 50 RPD at <$10 balance, 1000 RPD at >=$10 (resets daily 00:00 UTC)
 *  - zai_credits      : $20 added 08-31 (burn-down, no refill)
 *
 * Usage:
 *   node water_windows.mjs now          -> table with countdowns
 *   node water_windows.mjs json         -> machine-readable
 *   node water_windows.mjs add <id> <burn>  -> record spend against a depletable (zai_credits)
 */
const MS_H = 3600e3, MS_D = 86400e3;
const now = new Date();
const ZAI_HALF_END = new Date("2026-09-09T00:00:00Z");
const ZAI_CREDITS_START_USD = 20.0;

// Burn ledger for depletables (zai_credits), persisted to /board/water_ledger.jsonl
import { readFileSync, writeFileSync, existsSync, appendFileSync } from "node:fs";
const LEDGER = "/board/water_ledger.jsonl";
const burn = existsSync(LEDGER)
  ? readFileSync(LEDGER, "utf8").split("\n").filter(Boolean).map(l => JSON.parse(l))
  : [];
const spent = (id) => burn.filter(b => b.id === id).reduce((s, b) => s + (b.amount || 0), 0);

// deepseek offpeak: Beijing time
const BJ_OFF = 8 * MS_H;
const bj = new Date(now.getTime() + BJ_OFF);
const bjH = bj.getUTCHours(), bjDay = bj.getUTCDay(); // 0=Sun..6=Sat
const weekend = bjDay === 0 || bjDay === 6;
const peak = !weekend && ((bjH >= 9 && bjH < 12) || (bjH >= 14 && bjH < 18));
let offpeakOpen, closesAt;
if (weekend) {
  offpeakOpen = true;
  // closes Monday 09:00 BJ
  const daysToMon = (8 - bjDay) % 7 || 7;
  closesAt = new Date(now.getTime() + daysToMon * MS_D + (9 - bjH) * MS_H - bj.getUTCMinutes() * 60e3);
} else if (peak) {
  offpeakOpen = false;
  closesAt = bjH < 12
    ? new Date(now.getTime() + (12 - bjH) * MS_H - bj.getUTCMinutes() * 60e3) // lunch gap opens
    : new Date(now.getTime() + (24 - bjH + 9) * MS_H - bj.getUTCMinutes() * 60e3); // next day 09:00
} else {
  offpeakOpen = true;
  closesAt = bjH >= 18
    ? new Date(now.getTime() + (33 - bjH) * MS_H - bj.getUTCMinutes() * 60e3) // 09:00 next day
    : bjH < 9
      ? new Date(now.getTime() + (9 - bjH) * MS_H - bj.getUTCMinutes() * 60e3)
      : new Date(now.getTime() + (14 - bjH) * MS_H - bj.getUTCMinutes() * 60e3); // lunch gap 12-14
}
const fmt = (ms) => {
  const h = Math.floor(ms / MS_H), m = Math.floor((ms % MS_H) / 60e3);
  return `${h}h ${String(m).padStart(2, "0")}m`;
};
const rows = [
  { id: "deepseek_offpeak", state: offpeakOpen ? "OPEN" : "PEAK(2x)", next: offpeakOpen ? `closes in ${fmt(closesAt - now)}` : `opens in ${fmt(closesAt - now)}`, note: "half price window (weekend = all open)" },
  { id: "zai_half_price", state: now < ZAI_HALF_END ? "OPEN" : "ENDED", next: now < ZAI_HALF_END ? `ends in ${fmt(ZAI_HALF_END - now)}` : "expired", note: "50% off all z.ai API till 09-09" },
  { id: "zai_credits", state: "BURN", next: `$${(ZAI_CREDITS_START_USD - spent("zai_credits")).toFixed(2)} left of $${ZAI_CREDITS_START_USD}`, note: "no refill — spend ledger only counts what we record" },
  { id: "grok_a", state: "DESKTOP", next: "idle seat — hook-tracked", note: "grok TUI lane 1 (nacho); quota resets in subscription window" },
  { id: "grok_b", state: "DESKTOP", next: "idle seat — hook-tracked", note: "grok TUI lane 2 (sd) = grok2 alias" },
  { id: "chatgpt_codex", state: "DESKTOP", next: "idle seat — codex exec", note: "long-horizon seat; jobs/codex-* contracts (reconcile-doctrine staged)" },
  { id: "zcode", state: "DESKTOP", next: "hands-off till 09-02 12:52Z", note: "coding-plan CLI 1310 — conservation law until 2026-09-02" },
  { id: "deepseek_direct", state: "HOST", next: "peak-guard active", note: "mag.providers deepseek lane; offpeak.v1 enforced" },
  { id: "ollama_local", state: "HOST", next: "always on (electricity)", note: "mag-ollama container, T0 tier" },
  { id: "groq_oss", state: "POLLED", next: "resets ~00:00 UTC daily", note: "30 RPM / 1K RPD / 200K TPD — cage cannot read usage; poll from host or trust deferrals" },
  { id: "cerebras", state: "POLLED", next: "resets 00:00 UTC daily", note: "5 RPM / 30K TPM / 1M TPD" },
  { id: "or_free", state: "POLLED", next: "resets 00:00 UTC daily", note: "50 RPD (<$10 bal) / 1000 RPD (>=10)" },
];

if (process.argv[2] === "json") { console.log(JSON.stringify({ as_of: now.toISOString(), rows }, null, 2)); process.exit(0); }
if (process.argv[2] === "add") {
  const [, id, amt, note] = process.argv.slice(2);
  appendFileSync(LEDGER, JSON.stringify({ ts: now.toISOString(), id, amount: parseFloat(amt), note: note || "" }) + "\n");
  console.log(`burned ${amt} on ${id}`);
  process.exit(0);
}
console.log(`WATER WINDOWS — ${now.toISOString()} (all times UTC; BJ = +8h)`);
for (const r of rows) console.log(`${r.id.padEnd(18)} ${r.state.padEnd(9)} ${r.next.padEnd(28)} ${r.note}`);
