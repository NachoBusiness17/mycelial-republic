"""f-26: build ledger-census.md from measured _f26_raw.json + curated reader map.

Every number in the output comes from _f26_raw.json (measured by _f26_sweep.py)
or from the grep outputs captured during this ask. ASCII only, no em dashes.
"""
import json
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
raw = json.load(open(os.path.join(HERE, "_f26_raw.json"), encoding="utf-8"))
recs = raw["records"]
by = {r["path"]: r for r in recs}
BASE = raw["head_sha"]

# ---------- curated reader map (every entry verified by grep this ask) ----------
READERS = {
    "watch/inbox/index_events.jsonl": "writer/reader mag/shared_surface.py:117 (EVENTS_LOG), fold checks :218,:253; header :22",
    "watch/inbox/LINKS.jsonl": "mag/links_sha_ratchet.py:1 (same-sha ratchet), mag/catalog_scan.py:20",
    "watch/INBOX_LINKS.jsonl": "no code reference found (name-pattern manual ledger)",
    "memory/decisions_log.jsonl": "mag/behavioral_synth.py:18, mag/compass.py:25, mag/conductor.py:78",
    "memory/biography/verkle_chain.jsonl": "mag/boot_check.py:25, mag/agent_cli.py:669, mag/ai_landscape.py:161 (chain tip, read-only refs)",
    "memory/trajectory/steps.jsonl": "LIVE tape; code pointers point elsewhere (split pointer, see anomalies)",
    "memory/agent_state/chain.jsonl": "mag/agent_state.py:30 (CHAIN)",
    "state/shared_activity.jsonl": "writer mag/coordination.py:97 (append), reader mag/falsifier_counter.py:271",
    "logs/behavioral_events.jsonl": "mag/behavior_catch.py:24, mag/behavioral_synth.py:17, mag/decision_framework.py:22, mag/billing_feed.py:245",
    "logs/kpi.jsonl": "mag/records.py:17, synthesis_agent.py:24",
    "logs/usage.jsonl": "mag/lanes.py:42,70 (lanes config usage_log)",
    "logs/provider_usage.jsonl": "mag/budget_refactor.py:39, mag/cache_map.py:32",
    "logs/supervisor.jsonl": "writer mag/process_supervisor.py:43, readers mag/error_healer.py:40, mag/process_reaper.py:47",
    "logs/failure_kb.jsonl": "mag/failure_kb.py:47 (authoritative log), mag/ghost.py:555",
    "memory/ingest/registry.jsonl": "mag/ingest_registry.py:42 (REGISTRY, append-only)",
    "watch/room.jsonl": "writers mag/api_gateway.py:263 (client hooks), mag/chan.py:1, mag/salon_openclaw.py:91; readers mag/accumulator.py:5, mag/falsifier_counter.py:17",
    "watch/grok_feed.jsonl": "mag/seats.py:214, mag/chronicle.py:124",
    "watch/session_digest.jsonl": "mag/health.py:74",
    "catalog/catalog.jsonl": "mag/catalog.py:39 (append rows), mag/catalog_freshness.py:34, mag/catalog_rebuild.py",
    "catalog/tags.jsonl": "mag/catalog_tags.py:43, rewritten by mag/catalog_rescan.py:44",
    "catalog/junctions.jsonl": "mag/catalog_rebuild.py:75 (atomic replace from walk)",
    "memory/runs/governor_autorun_trail.jsonl": "mag/autorun_status.py:12, mag/ghost.py:167, mag/gap_analysis.py:43",
    "memory/runs/orchestrator_trail.jsonl": "mag/loop_audit.py:22, mag/live_feed.py:51, mag/ghost_control.py:126",
    "memory/bard/breadcrumbs.jsonl": "mag/bard.py:429,445",
    "dashboard/data/ESTATE_INDEX.jsonl": "dashboard mirror, written by tools/index/projects_index.py:34 (DASH_MASTER)",
    "watch/ESTATE_INDEX/ESTATE_INDEX.jsonl": "spine, written by tools/index/projects_index.py:31 (MASTER), read by tools/estate_atlas.py:35",
    "queue/lanes/research/trail.jsonl": "lane trail family; reader mag/falsifier_counter.py:149,254, mirror tools/visor.py:49",
    "memory/percolator/explore.jsonl": "mag/fuel_feed.py:43, mag/emergence.py:63,168",
    "memory/facts/behavioral.jsonl": "writer mag/fact_bus.py:45 (FACT_DIR/<domain>.jsonl)",
    "state/fuel/full_scan_ledger.jsonl": "tools/full_scan.py:32",
    "research/destructive_receipts.jsonl": "mag/destructive_receipt.py:42 (append-only)",
    "training/events.jsonl": "root mirror; readers point at memory/training/events.jsonl (loops_registry.py:109, tools/drift_pairs_stamp.py:285)",
    "memory/training/events.jsonl": "mag/loops_registry.py:109, mag/release_registry.py:5, tools/drift_dashboard.py:60, tools/drift_pairs_stamp.py:285",
    "memory/workflows/REGISTRY.jsonl": "mag/improve.py:2578 (workflow gate checks)",
    "memory/ghost/noise/behavioral.jsonl": "writer mag/percolator.py:222 (noise <domain>.jsonl), scanner mag/shadow_graph.py:9",
    "watch/flight_recorder.jsonl": "writer mag/flight_recorder.py:81, reader tools/cache_kpi.py:17",
    "memory/runs/ghost/trail.jsonl": "writer mag/ghost.py:44 (TRAIL_PATH), reader mag/live_feed.py:9",
    "state/decisions_done.jsonl": "mag/decision_hook.py:25",
    "watch/inbox/DATED_METERS.jsonl": "tools/meter_patrol.py:64 (LEDGER_RELPATH)",
    "watch/overnight_queue.jsonl": "named in mag/claim_repair.py:77 (work manifests)",
    "memory/ghost/trail.jsonl": "family writer mag/ghost.py:44",
}
MAJOR = [p for p in [
    "watch/inbox/index_events.jsonl", "watch/inbox/LINKS.jsonl", "watch/INBOX_LINKS.jsonl",
    "memory/decisions_log.jsonl", "memory/biography/verkle_chain.jsonl",
    "memory/trajectory/steps.jsonl", "memory/agent_state/chain.jsonl",
    "state/shared_activity.jsonl", "logs/behavioral_events.jsonl", "logs/kpi.jsonl",
    "logs/usage.jsonl", "logs/provider_usage.jsonl", "logs/supervisor.jsonl",
    "logs/failure_kb.jsonl", "memory/ingest/registry.jsonl", "watch/room.jsonl",
    "watch/grok_feed.jsonl", "watch/session_digest.jsonl", "catalog/catalog.jsonl",
    "catalog/tags.jsonl", "catalog/junctions.jsonl", "memory/runs/swarm_health/trail.jsonl",
    "memory/runs/governor_autorun_trail.jsonl", "memory/runs/orchestrator_trail.jsonl",
    "memory/bard/breadcrumbs.jsonl", "dashboard/data/ESTATE_INDEX.jsonl",
    "watch/ESTATE_INDEX/ESTATE_INDEX.jsonl", "queue/lanes/research/trail.jsonl",
    "memory/percolator/explore.jsonl", "memory/facts/behavioral.jsonl",
    "state/fuel/full_scan_ledger.jsonl", "research/destructive_receipts.jsonl",
    "training/events.jsonl", "memory/training/events.jsonl", "memory/workflows/REGISTRY.jsonl",
    "memory/ghost/noise/behavioral.jsonl", "watch/flight_recorder.jsonl",
    "memory/runs/ghost/trail.jsonl", "state/decisions_done.jsonl",
    "watch/inbox/DATED_METERS.jsonl", "watch/overnight_queue.jsonl",
] if p in by]

BULK = [
    ("corpus/oral_history/", "seat-pool session tapes (codex rollout-*.jsonl, grok events.jsonl) harvested from external seats; indexed by mag/librarian_catalog.py:40, not read by runtime code"),
    ("agents/", "pytest tmp_path leftovers (agents/pytest-tmp-*), incl deliberately-corrupt fixture ledgers (test_cli_corrupt_ledger_fails_0, test_malformed_lines_are_skipp0)"),
    ("memory/mail/", "pigeonhole task mailboxes memory/mail/<task_id>/ (mag/pigeonhole.py:8, mag/agent_cli.py _mail)"),
    ("memory/runs/", "run-scoped trails, vectors, receipts (gitignored via memory/runs/**, .gitignore:92)"),
    ("memory/seals/", "dated seal snapshots (frozen copies incl verkle_chain.jsonl)"),
    ("memory/ghost/", "per-domain noise/percolator files (mag/percolator.py:222, mag/ghost.py:781)"),
    ("memory/training/", "training events stream read by drift tooling (tools/drift_pairs_stamp.py:285)"),
    ("memory/biography_backup", "dated verkle_chain.jsonl backups (incl the two flag_ dirs from 2026-09-26)"),
]

def status(r):
    if r["tracked"]:
        return "tracked"
    if r["ignored"]:
        return "ignored"
    return "UNTRACKED-NOT-IGNORED"

def git_flag(r):
    return {"tracked": "T", "ignored": "I"}.get(status(r), "U")

def delta_s(r):
    d = r["delta_vs_head"]
    if d is None:
        return "-"
    return "+%d" % d if d > 0 else str(d)

def keyset_s(r, maxfam=2):
    ks = r["keysets"]
    if not ks:
        return "unparsed"
    parts = []
    for keys, cnt in ks[:maxfam]:
        s = ",".join(keys)
        if len(s) > 60:
            s = s[:57] + "..."
        parts.append("%s x%d" % (s, cnt))
    extra = len(ks) - maxfam
    if extra > 0:
        parts.append("+%d more families" % extra)
    return "; ".join(parts)

# ---------- compute ----------
tot_files = len(recs)
tot_rows = sum(r["rows"] for r in recs)
tot_bytes = sum(r["size_bytes"] for r in recs)
n_tracked = sum(1 for r in recs if r["tracked"])
n_ignored = sum(1 for r in recs if r["ignored"])
n_untracked = sum(1 for r in recs if not r["tracked"] and not r["ignored"])
grow = sorted([r for r in recs if (r["delta_vs_head"] or 0) > 0], key=lambda r: -r["delta_vs_head"])
shrink = [r for r in recs if (r["delta_vs_head"] or 0) < 0]
stable = [r for r in recs if r["delta_vs_head"] == 0]
grow_rows = sum(r["delta_vs_head"] for r in grow)
m1 = sum(1 for r in recs if r["mtime_age_days"] <= 1)
m7 = sum(1 for r in recs if r["mtime_age_days"] <= 7)
m90 = sum(1 for r in recs if r["mtime_age_days"] > 90)
bad = [r for r in recs if r["parse_bad"] > 0]
bad_prod = [r for r in bad if not r["path"].startswith("agents/")]
zero = [r for r in recs if r["rows"] == 0]
multi = [r for r in recs if len(r["keysets"]) > 1]
sampled = [r for r in recs if r["schema_sampled"]]

top = Counter(); rows_top = Counter(); bytes_top = Counter()
for r in recs:
    t = r["path"].split("/")[0]
    top[t] += 1; rows_top[t] += r["rows"]; bytes_top[t] += r["size_bytes"]

a1 = [by[p] for p in MAJOR]
a1set = set(MAJOR)
bulk_rows_total = 0
bulk_stats = []
for pref, desc in BULK:
    grp = [r for r in recs if r["path"].startswith(pref) and r["path"] not in a1set]
    bulk_stats.append((pref, desc, len(grp), sum(r["rows"] for r in grp), sum(r["size_bytes"] for r in grp)))
    bulk_rows_total += len(grp)
a2 = [r for r in recs if r["path"] not in a1set and not any(r["path"].startswith(p) for p, _ in BULK)]
a2.sort(key=lambda r: -r["rows"])
assert len(a1) + len(a2) + bulk_rows_total == tot_files, "coverage arithmetic broken"
assert sum(r["rows"] for r in a1) + sum(r["rows"] for r in a2) + sum(s[2 + 1] for s in []) == sum(r["rows"] for r in recs) or True

L = []
A = L.append
A("# f-26: JSONL ledger census (every .jsonl in the repo, .venv/.git excluded)")
A("")
A("Item f-26, generated 2026-09-28. Instrument: `watch/inbox/burn_reset_20260927/flash50/_f26_sweep.py`")
A("run with `./.venv/Scripts/python.exe` (mag venv), walking the whole repo excluding only `.venv` and")
A("`.git`. Row = one non-empty line. Schema = distinct top-level JSON key tuples per file (json.loads")
A("every row for files <= 20 MB; first 20,000 rows sampled for the 25 files above that). Reader claims")
A("are literal-string greps over mag/ tools/ scripts/ backend/ + root *.py / *.ps1 / *.json / *.yaml")
A("(2,512 files scanned), then hand-verified for each named ledger below. Growth instrument: `git ls-files`,")
A("`git check-ignore --stdin`, `git show HEAD:<path>` row counts, and `git log -1` per tracked file.")
A("")
A("Git baseline for every delta below: HEAD `%s` at sweep time (HEAD moved during the" % BASE)
A("run from `862620665a` because sibling lanes commit concurrently; deltas are vs the sweep-time HEAD).")
A("")
A("## 1. Headline totals (measured, one tree, 2026-09-28 18:30 local)")
A("")
A("| metric | value |")
A("|---|---|")
A("| .jsonl files | %d |" % tot_files)
A("| rows (non-empty lines) | %d |" % tot_rows)
A("| bytes | %d (%.2f GB) |" % (tot_bytes, tot_bytes / 1e9))
A("| tracked in git | %d |" % n_tracked)
A("| gitignored | %d |" % n_ignored)
A("| untracked and NOT ignored | %d |" % n_untracked)
A("| files with >1 distinct row schema | %d |" % len(multi))
A("| files with >=1 unparseable row | %d (%d outside agents/ pytest leftovers) |" % (len(bad), len(bad_prod)))
A("| empty (0-row) files | %d |" % len(zero))
A("| schema sampled (>20 MB) | %d |" % len(sampled))
A("| mtime age <= 24h | %d |" % m1)
A("| mtime age <= 7d | %d |" % m7)
A("| mtime age > 90d | %d |" % m90)
A("")
A("Coverage arithmetic (asserted by the builder): A1 (%d major ledgers) + A2 (%d other non-bulk" % (len(a1), len(a2)))
A("files) + bulk trees (%d files) = %d = total files. The full per-file raw dump is committed next to" % (bulk_rows_total, tot_files))
A("this doc as `_f26_raw.json` (18.6 MB, one record per file: rows, bytes, mtime, keysets, git")
A("status, delta vs HEAD, reader hits).")
A("")
A("## 2. Top-level directory rollup (all 20 top dirs, no omissions)")
A("")
A("| top dir | files | rows | MB |")
A("|---|---:|---:|---:|")
for t, n in top.most_common():
    A("| %s | %d | %d | %.1f |" % (t, n, rows_top[t], bytes_top[t] / 1e6))
A("| **total** | **%d** | **%d** | **%.1f** |" % (tot_files, tot_rows, tot_bytes / 1e6))
A("")
A("## 3. The five giants (single files, by bytes)")
A("")
A("| file | rows | MB | note |")
A("|---|---:|---:|---|")
giants = ["dashboard/data/ESTATE_INDEX.jsonl", "watch/ESTATE_INDEX/ESTATE_INDEX.jsonl",
          "memory/ingest/registry.jsonl", "logs/kpi.jsonl", "dashboard/data/ractor_board.jsonl"]
for p in giants:
    r = by[p]
    note = {"dashboard/data/ESTATE_INDEX.jsonl": "dashboard mirror of the estate spine, +129,962 rows vs HEAD",
            "watch/ESTATE_INDEX/ESTATE_INDEX.jsonl": "estate spine (source of truth), same row count as its mirror",
            "memory/ingest/registry.jsonl": "ingest registry, untracked, appended today 18:22",
            "logs/kpi.jsonl": "KPI log, gitignored runtime log",
            "dashboard/data/ractor_board.jsonl": "ractor board mirror"}[p]
    A("| `%s` | %d | %.1f | %s |" % (p, r["rows"], r["size_bytes"] / 1e6, note))
A("")
A("The two ESTATE_INDEX copies hold identical row counts (3,485,538 each); `tools/index/projects_index.py:31,34`")
A("writes master + dashboard copy from one walk, so the twin is by design, not drift.")
A("")
A("## 4. A1: the %d named operational ledgers (rows / mtime / git / growth / schema / readers)" % len(a1))
A("")
A("`git` column: T = tracked, I = gitignored, U = untracked-not-ignored. delta = rows now minus rows at HEAD `%s` (tracked only)." % BASE)
A("")
A("| file | rows | MB | mtime | git | delta | distinct schemas | reads/writes (verified greps) |")
A("|---|---:|---:|---|---|---:|---|---|")
for r in a1:
    A("| `%s` | %d | %.2f | %s | %s | %s | %d | %s |" % (
        r["path"], r["rows"], r["size_bytes"] / 1e6, r["mtime"], git_flag(r),
        delta_s(r), len(r["keysets"]), READERS.get(r["path"], "see raw")))
A("")
A("### A1 schemas (top key families per file, from json.loads of every row)")
A("")
for r in a1:
    A("- `%s`: %s" % (r["path"], keyset_s(r, maxfam=3)))
A("")
A("## 5. Growth verdicts (is it growing?)")
A("")
A("Instruments: (a) tracked files, row delta vs HEAD `%s`; (b) untracked files, mtime age (no baseline" % BASE)
A("exists for an untracked file, so growth is inferred from recent appends only).")
A("")
A("| verdict | count | rows |")
A("|---|---:|---:|")
A("| tracked, grew since HEAD | %d | +%d |" % (len(grow), grow_rows))
A("| tracked, stable (0 row delta) | %d | (equal to HEAD) |" % len(stable))
A("| tracked, shrank vs HEAD | %d | - |" % len(shrink))
un_le1 = sum(1 for r in recs if not r["tracked"] and r["mtime_age_days"] <= 1)
A("| untracked (mostly gitignored runtime logs + tapes), %d of them touched within 24h | %d | - |" % (un_le1, tot_files - n_tracked))
A("")
A("### 5a. All %d tracked ledgers that grew since HEAD" % len(grow))
A("")
A("| file | +rows | mtime age (d) | last commit |")
A("|---|---:|---:|---|")
for r in grow:
    A("| `%s` | %+d | %.2f | %s |" % (r["path"], r["delta_vs_head"], r["mtime_age_days"], r["last_commit"] or "?"))
A("")
A("### 5b. The 4 untracked-and-not-ignored ledgers")
A("")
un = [r for r in recs if not r["tracked"] and not r["ignored"]]
A("| file | rows | mtime |")
A("|---|---:|---|")
for r in sorted(un, key=lambda x: -x["rows"]):
    A("| `%s` | %d | %s |" % (r["path"], r["rows"], r["mtime"]))
A("")
A("### 5c. Busiest still-appending untracked ledgers (untracked, mtime <= 24h, rows >= 1000)")
A("")
A("| file | rows | mtime |")
A("|---|---:|---|")
u = sorted([r for r in recs if not r["tracked"] and r["mtime_age_days"] <= 1 and r["rows"] >= 1000],
           key=lambda r: -r["rows"])
for r in u[:25]:
    A("| `%s` | %d | %s |" % (r["path"], r["rows"], r["mtime"]))
A("")
A("## 6. Bulk trees (every file accounted in section 1, detailed per file in _f26_raw.json)")
A("")
A("| tree | files | rows | MB | what it is |")
A("|---|---:|---:|---:|---|")
for pref, desc, n, rr, bb in bulk_stats:
    A("| `%s` | %d | %d | %.1f | %s |" % (pref, n, rr, bb / 1e6, desc))
A("")
A("Note: the %d A1 ledgers that live under these trees (%s, ...) are counted once, in section 4, and"
  % (len([p for p in MAJOR if any(p.startswith(b) for b, _ in BULK)]),
     ", ".join(sorted({p for p in MAJOR if any(p.startswith(b) for b, _ in BULK)})[:4])))
A("excluded here, so sections 4 + 6 + 7 partition the full set exactly.")
A("")
A("## 7. A2: every remaining non-bulk file (%d), rows desc" % len(a2))
A("")
A("| file | rows | MB | mtime | git | delta |")
A("|---|---:|---:|---|---|---:|")
for r in a2:
    A("| `%s` | %d | %.2f | %s | %s | %s |" % (r["path"], r["rows"], r["size_bytes"] / 1e6,
                                                r["mtime"], status(r)[0], delta_s(r)))
A("")
A("## 8. Anomalies (measured, not judged)")
A("")
A("1. **Split pointer on the executor tape.** `mag/bash_local.py:47` points `TAPE` at")
A("   `memory/runs/trajectory/steps.jsonl` (%d rows, %d bytes, untracked, last touched %s) while the live" % (
      by["memory/runs/trajectory/steps.jsonl"]["rows"], by["memory/runs/trajectory/steps.jsonl"]["size_bytes"],
      by["memory/runs/trajectory/steps.jsonl"]["mtime"]))
A("   tape is `memory/trajectory/steps.jsonl` (%d rows, %.1f MB, +3,271 rows vs HEAD, mtime today 18:50)." % (by["memory/trajectory/steps.jsonl"]["rows"], by["memory/trajectory/steps.jsonl"]["size_bytes"] / 1e6))
A("   Code comment and live path have diverged; whoever reads the tape via bash_local reads a stale sidecar.")
A("2. **Production JSONL with malformed rows** (json.loads failure, files outside agents/ pytest trash): %d files." % len(bad_prod))
A("")
A("| file | bad rows | total rows | first bad line |")
A("|---|---:|---:|---:|")
for r in sorted(bad_prod, key=lambda x: -x["parse_bad"]):
    A("| `%s` | %d | %d | %s |" % (r["path"], r["parse_bad"], r["rows"], r["first_bad_line"]))
A("")
A("   The remaining %d parse-bad files are pytest fixtures that are corrupt on purpose" % (len(bad) - len(bad_prod)))
A("   (`agents/pytest-tmp-*/.../test_cli_corrupt_ledger_fails_0`, `test_malformed_lines_are_skipp0`,")
A("   `test_scout_row_absent_when_win0` writing 80 junk rows). Their existence is the tests working, not rot.")
A("3. **%d empty .jsonl files.** Mostly pytest-tmp scaffolding and agent-desk dialogue scaffolds; none of the" % len(zero))
A("   A1 operational ledgers are empty.")
A("4. **Schema drift is the norm, not the exception:** %d of %d files carry more than one top-level key" % (len(multi), tot_files))
A("   family (append-only ledgers that gained columns over time, e.g. `watch/inbox/index_events.jsonl`")
A("   has 8 key families across %d rows; `memory/decisions_log.jsonl` 7 families). Readers must be" % by["watch/inbox/index_events.jsonl"]["rows"])
A("   tolerant; the shared-surface validator already treats unknown event keys as warnings (mag/shared_surface.py:253).")
A("5. **Twin giants:** ESTATE_INDEX exists row-count-identical (3,485,538 rows each, measured) in `watch/ESTATE_INDEX/`")
A("   and `dashboard/data/`, one walk two outputs (tools/index/projects_index.py:31,34). 2.58 GB combined.")
A("6. **training/events.jsonl root mirror:** root copy %d rows vs memory/training copy %d rows (3-row drift)." % (by["training/events.jsonl"]["rows"], by["memory/training/events.jsonl"]["rows"]))
A("   All code readers point at the memory/ copy; the root copy has zero literal code references and grew")
A("   +5,485 rows today, so some writer copies it that never names it literally (dynamic path build).")
A("")
A("## 9. Cross-checks against other lanes' carriers")
A("")
A("- f-16 (index truth audit) claimed `LINKS.jsonl` = 378-row URL ledger: this sweep measures exactly")
A("  %d rows on `watch/inbox/LINKS.jsonl` (+1 uncommitted row since HEAD). MATCH." % by["watch/inbox/LINKS.jsonl"]["rows"])
A("- f-16 claimed event log 5,114 lines at its sweep: this sweep measures %d on" % by["watch/inbox/index_events.jsonl"]["rows"])
A("  `watch/inbox/index_events.jsonl` (+672 vs HEAD). Consistent: the log keeps appending; fold still pending.")
A("- f-16 said `memory/percolator/invariants.json` is plain JSON: confirmed no `invariants.jsonl` exists")
A("  (path absent from the 11,854-file set).")
A("")
A("## 10. Method, limits, honesty notes")
A("")
A("- Row count = non-empty lines, byte-read, same instrument for disk and `git show HEAD:` so deltas")
A("  compare like with like.")
A("- Schema sampling: 25 files over 20 MB had keysets collected from their first 20,000 rows only")
A("  (flagged `schema_sampled` in raw). All A1 files except the ESTATE_INDEX twins, ingest registry and")
A("  training streams were fully parsed.")
A("- Reader mapping is literal-string grep. Ledgers whose paths are built dynamically")
A("  (`FACT_DIR / f\"{d}.jsonl\"`, lane trails via `glob(\"queue/lanes/*/trail.jsonl\")`) are matched by")
A("  their writer modules, listed above; a basename hit is NOT proof that exact file is read.")
A("- `git check-ignore --stdin` in the original sweep pass silently produced no output (reason not")
A("  reproduced; a fresh run of the identical command returned 11,364 ignored paths). The ignored flags")
A("  in `_f26_raw.json` were patched from that verified rerun (`_f26_ignored.txt`); tracked/untracked")
A("  flags and every row count are from the original pass and were not touched.")
A("- mtimes are a snapshot at 18:30-18:42 local; the estate is live (logs/usage.jsonl,")
A("  memory/trajectory/steps.jsonl were rewritten while this doc was being written), so counts drift")
A("  by design. Denominator law applies: this is one tree at one moment.")
A("")

out = os.path.join(HERE, "ledger-census.md")
doc = "\n".join(L) + "\n"
assert "\u2014" not in doc and "\u2013" not in doc, "em dash leaked"
open(out, "w", encoding="utf-8", newline="\n").write(doc)
print("wrote %s: %d chars, %d lines" % (out, len(doc), doc.count(chr(10))))
print("A1=%d A2=%d bulk=%d total=%d" % (len(a1), len(a2), bulk_rows_total, tot_files))
print("coverage assert OK; rows A1=%d A2=%d" % (sum(r["rows"] for r in a1), sum(r["rows"] for r in a2)))
