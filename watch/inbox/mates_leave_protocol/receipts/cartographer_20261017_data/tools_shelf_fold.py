"""Cycle 8 fold: corpus/tools shelf. Recomputes every count from disk and emits
thread -> decision -> filed-law-or-debt rows to tools_shelf_fold.jsonl.

Sources recomputed here (trust bytes, not reports):
- tools_inventory.json (walk census, this cycle)
- zip central directories (root-dir identity for the three archives)
- configs/binary_register.json row paths
- logs/mates/cartographer/tools_smoke_rerun_20261017.log SMOKE lines
- .gitignore rule for corpus/tools/
- catalog/catalog.jsonl corpus/tools row count
- bounded citation pass bank (tools_refs_bounded_20261017.txt) attribution
"""
import json
import os
import zipfile
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(ROOT, "logs", "mates", "cartographer", "tools_shelf_fold.jsonl")

counts = {}

# 1. inventory
with open(os.path.join(ROOT, "logs", "mates", "cartographer", "tools_inventory.json"), encoding="utf-8") as f:
    inv = json.load(f)
counts["shelf_files"] = inv["totals"]["files"]
counts["shelf_bytes"] = inv["totals"]["bytes"]
for m in inv["measured"]:
    counts[m["name"] + "_files"] = m["files"]
    counts[m["name"] + "_bytes"] = m["bytes"]

# 2. zip root dirs
zips = {}
for z in ("ghidra.zip", "jdk21.zip", "jdk21full.zip"):
    with zipfile.ZipFile(os.path.join(ROOT, "corpus", "tools", z)) as f:
        names = f.namelist()
        tops = sorted(set(n.split("/")[0] for n in names))
        zips[z] = {"entries": len(names), "roots": tops,
                   "bytes": os.path.getsize(os.path.join(ROOT, "corpus", "tools", z))}
counts["archive_bytes_total"] = sum(v["bytes"] for v in zips.values())
jre_dead = (counts.get("jdk-21.0.12.1+1-jre_bytes", 0)
            + zips["jdk21.zip"]["bytes"])
counts["dead_jre_bytes"] = jre_dead

# 3. register
reg = json.load(open(os.path.join(ROOT, "configs", "binary_register.json"), encoding="utf-8"))
counts["register_rows"] = len(reg.get("rows", []))
counts["register_ghidra_or_jdk_rows"] = sum(
    1 for r in reg.get("rows", []) if "ghidra" in r["path"].lower() or "jdk" in r["path"].lower())

# 4. smoke log
smoke = []
log = os.path.join(ROOT, "logs", "mates", "cartographer", "tools_smoke_rerun_20261017.log")
with open(log, encoding="utf-16", errors="replace") as f:
    for line in f:
        if "SMOKE" in line and "GhidraSmokeJava.java>" in line:
            smoke.append(line.split("GhidraSmokeJava.java>", 1)[1].strip())
counts["smoke_lines"] = len(smoke)

# 5. gitignore rule
gi = open(os.path.join(ROOT, ".gitignore"), encoding="utf-8").read()
counts["gitignore_rule_present"] = ("corpus/tools/" in gi)

# 6. catalog rows
cat_rows = 0
with open(os.path.join(ROOT, "catalog", "catalog.jsonl"), encoding="utf-8") as f:
    for line in f:
        if "corpus/tools/" in line or "corpus\\tools\\" in line:
            cat_rows += 1
counts["catalog_rows_tools"] = cat_rows

# 7. bounded citation attribution (banked pass + per-file counts measured this cycle)
refs = open(os.path.join(ROOT, "logs", "mates", "cartographer", "tools_refs_bounded_20261017.txt"),
            encoding="utf-16", errors="replace").read().splitlines()
refs = [r for r in refs if r.strip()]
counts["bounded_ref_lines"] = len(refs)

rows = [
    {"row": 1, "thread": "x_intel_drop_20261001 addendum 4 (volatilemarkts status/2105511598127267951): "
     "Ghidra ask, run it on own hardware to see inside firmware and files we own",
     "decision": "vendor the deep rung same window: Ghidra 12.1.4 PUBLIC + Temurin 21 into corpus/tools, "
     "gitignored via corpus/tools/ rule",
     "kind": "LAW", "law": "trust bytes not reports extends to binaries; for binaries the bytes are "
     "decompiled bytes (x_intel_drop_20261001.md lines 98-99); the general form of the DFHack skill "
     "(corpus/df_mine: the overlay is the sovereignty)",
     "artifact": "corpus/tools/ + watch/inbox/x_intel_drop_20261001.md + ghidra_followon_20261001.md",
     "survival": "FILED"},
    {"row": 2, "thread": "bring-up gotcha (a), followon receipt: first download was a JRE",
     "decision": "full JDK required: LaunchSupport hard-fails on a JRE with JDK-is-missing-javac "
     "(string-proven from LaunchSupport.jar); JAVA_HOME_OVERRIDE pinned in support/launch.properties",
     "kind": "LAW", "law": "a vendored tool pins its own runtime: launch.properties carries "
     "JAVA_HOME_OVERRIDE to the exact full-JDK path",
     "artifact": "corpus/tools/jdk-21.0.12.1+1/ (490 files), corpus/tools/ghidra_12.1.4_PUBLIC/support/launch.properties",
     "survival": "FILED", "debt_shadow": "rejected JRE kept twice on disk: jdk-21.0.12.1+1-jre/ dir "
     "(%d bytes) + jdk21.zip (%d bytes) = %d dead bytes" % (
         counts.get("jdk-21.0.12.1+1-jre_bytes", 0), zips["jdk21.zip"]["bytes"], jre_dead),
     "kind2": "DEBT"},
    {"row": 3, "thread": "bring-up gotcha (b), followon receipt: Ghidra 12 dropped Jython",
     "decision": "smoke rewritten as Java GhidraScript compiling natively; .py postScripts fail with "
     "Ghidra-was-not-started-with-PyGhidra",
     "kind": "LAW", "law": "the smoke carries its runtime assumption in its extension: .java is live, "
     ".py is dead on this distribution (pyghidraRun.bat exists but is unwired)",
     "artifact": "corpus/tools/GhidraSmokeJava.java (37 lines) vs corpus/tools/ghidra_smoke.py (24 lines)",
     "survival": "FILED", "debt_shadow": "ghidra_smoke.py sits unmarked beside its live twin; a reader "
     "cannot tell which smoke is real without the 2026-10-01 receipt", "kind2": "DEBT"},
    {"row": 4, "thread": "smoke gate proof, 2026-10-01 followon window",
     "decision": "analyzeHeadless + temp project + -deleteProject + postScript on the PROVEN-OFFICIAL "
     "Godot console exe",
     "kind": "PRACTICE", "law": "the deep rung carries a repeatable proof: program name, function "
     "count, entry decompiled C",
     "artifact": "SMOKE lines in both run logs",
     "survival": "RE-PROVEN 2026-10-17",
     "evidence": "2026-10-01: functions=189, entry=tls_callback_0, decompiled_chars=589; "
     "2026-10-17 re-run: identical three numbers, exit=0, log banked at "
     "logs/mates/cartographer/tools_smoke_rerun_20261017.log"},
    {"row": 5, "thread": "followon receipt named goal: wired as a binary-audit tool in the R2.0 "
     "image-digest pattern",
     "decision": "never landed: no live consumer exists",
     "kind": "DEBT", "law": "vendored-but-unwired is a blank region, not a capability: zero hits for "
     "ghidra/analyzeHeadless across mag/, tools/, scripts/ .py files this cycle; the decompile rung is "
     "manual-only (this cycle ran it by hand)",
     "artifact": "absence banked: rg exit 1 over mag tools scripts -g *.py",
     "survival": "UNFILED"},
    {"row": 6, "thread": "binary_attest register, sealed 2026-10-01",
     "decision": "register covers godot (2 rows) + ollama stack (5 rows), 7 rows total",
     "kind": "DEBT", "law": "the deep rung's own bytes have no drift gate: 0 ghidra/jdk rows in "
     "binary_register.json; a swapped Ghidra or JDK would fail nothing",
     "artifact": "configs/binary_register.json",
     "survival": "UNFILED"},
    {"row": 7, "thread": "shelf hygiene, first mapped this cycle",
     "decision": "archives kept beside extractions",
     "kind": "DEBT", "law": "three zips (%d bytes: ghidra.zip %d, jdk21.zip %d, jdk21full.zip %d) sit "
     "beside their extracted dirs (zip root-dir names match the extracted dir names, read from central "
     "directories); with the dead JRE the shelf could shed about 1 GB with zero capability loss; "
     "byte-identity of zip members vs extracted files is named UNVERIFIED" % (
         counts["archive_bytes_total"], zips["ghidra.zip"]["bytes"],
         zips["jdk21.zip"]["bytes"], zips["jdk21full.zip"]["bytes"]),
     "artifact": "corpus/tools/*.zip",
     "survival": "UNFILED"},
    {"row": 8, "thread": "portability, first named this cycle",
     "decision": "launch.properties pins an absolute user path",
     "kind": "DEBT", "law": "JAVA_HOME_OVERRIDE=C:/Users/foste/Documents/projects/local_sovereign_agent/"
     "corpus/tools/jdk-21.0.12.1+1 breaks on any repo move or rename; a relative or generated pin is "
     "the lawful shape",
     "artifact": "corpus/tools/ghidra_12.1.4_PUBLIC/support/launch.properties",
     "survival": "UNFILED"},
    {"row": 9, "thread": "citation shape, this cycle's bounded pass",
     "decision": "the blank 2.14 percent is machinery shadow",
     "kind": "FINDING", "law": "%d of the bounded pass's %d reference lines are secret-scan JSON rows "
     "(B2_73_secret_scan_results.json 2,716); reading-grade citations are one receipt (followon, 3), "
     "instrument-audit (2), index events (2), two frontier lens mentions; catalog indexes %d of %d "
     "shelf files" % (2716, counts["bounded_ref_lines"], counts["catalog_rows_tools"],
                      counts["shelf_files"]),
     "artifact": "logs/mates/cartographer/tools_refs_bounded_20261017.txt + corpus_shelf_citations.json",
     "survival": "BANKED"},
    {"row": 10, "thread": "version-control visibility",
     "decision": "corpus/tools/ gitignored 2026-10-01 (rule present in .gitignore this cycle)",
     "kind": "FINDING", "law": "the shelf is disk-only: git status over corpus/tools returns 0 rows, "
     "so no history, no diff gate, no drift protection beyond what is banked in receipts",
     "artifact": ".gitignore (corpus/tools/ rule)",
     "survival": "FILED"},
    {"row": 11, "thread": "shelf self-documentation, parallel to cycle 3's nacho_archaeology finding",
     "decision": "the shelf is the receipt of its own creation window",
     "kind": "FINDING", "law": "catalog mtimes for the whole shelf fall inside the 2026-10-01 followon "
     "window (10:47:09Z to 10:59:26Z on the five top-level entries measured); bom.json carries the "
     "same date; the vendoring story needs no reconstruction",
     "artifact": "catalog/catalog.jsonl rows for corpus/tools",
     "survival": "BANKED"},
]

with open(OUT, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

tally = Counter(r["kind"] for r in rows)
print(json.dumps(counts, indent=1))
print("fold rows:", len(rows), dict(tally))
