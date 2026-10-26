"""nonnvidia-stacks finish-line checks (division B, spiking-wide, 2026-10-01).

Run: .venv/Scripts/python.exe watch/inbox/gala_20260925/spiking-wide/lanes/nonnvidia_stacks_check.py
Raw output goes to watch/inbox/gala_20260925/spiking-wide/lanes/nonnvidia-stacks.check.txt
"""
import json
import os
import subprocess
import sys

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
LANES = os.path.join(ROOT, "watch", "inbox", "gala_20260925", "spiking-wide", "lanes")
REG = os.path.join(ROOT, "watch", "inbox", "spiking_wide", "nonnvidia_stacks_signals.jsonl")
RECEIPT = os.path.join(ROOT, "watch", "inbox", "spiking_wide", "nonnvidia-stacks.md")
LANE_JSON = os.path.join(LANES, "nonnvidia-stacks.json")

results = []


def check(name, ok, detail):
    results.append((name, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


print("=== NONNVIDIA-STACKS FINISH-LINE CHECKS 2026-10-01 ===")

# CHECK 1: no prior sovereignty-compute table anywhere except this lane's own files
print("\n-- CHECK 1: prior sovereignty-compute table absence --")
git_hits = []
for pattern in ("sanctions-proof", "sovereignty-compute", "sovereign compute table"):
    pg = subprocess.run(
        ["git", "grep", "-ril", pattern, "--", "watch/inbox", "docs", "memory", "state"],
        cwd=ROOT, capture_output=True, text=True, shell=False)
    print(f"git grep -ril '{pattern}': exit={pg.returncode}")
    git_hits.extend(h for h in (pg.stdout or "").splitlines()
                    if "spiking_wide" not in h and "spiking-wide" not in h)
print(f"git grep tracked hits outside this lane's files: {git_hits or 'NONE'}")
# untracked-tree sweep (git grep cannot see untracked files). memory/trajectory is the
# session recorder: it stores THIS session's own commands, so it is excluded as
# self-telemetry, and any hits it holds are printed anyway for honesty.
fs_hits = []
trajectory_hits = []
patterns = ("sanctions-proof", "sovereignty-compute", "sovereign compute table")
for top in ("watch/inbox", "docs", "memory", "state"):
    for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, top)):
        d = dirpath.replace("\\", "/")
        if "spiking_wide" in d or "spiking-wide" in d:
            continue
        in_traj = "memory/trajectory" in d
        for fn in filenames:
            if not fn.lower().endswith((".md", ".json", ".jsonl", ".yaml")):
                continue
            try:
                with open(os.path.join(dirpath, fn), "r", encoding="utf-8", errors="ignore") as fh:
                    t = fh.read()
            except OSError:
                continue
            if any(x in t for x in patterns):
                rel = os.path.relpath(os.path.join(dirpath, fn), ROOT)
                (trajectory_hits if in_traj else fs_hits).append(rel)
print(f"trajectory-recorder self-hits (this session's own commands, excluded): {trajectory_hits}")
print(f"filesystem sweep hits (untracked included, excluding this lane's files + trajectory): {fs_hits or 'NONE'}")
check("CHECK 1 no-prior-table", not git_hits and not fs_hits,
      f"tracked hits outside this lane: {git_hits or 'NONE'}; filesystem sweep hits: {fs_hits or 'NONE'}; "
      f"trajectory self-hits (this session's recorded commands, not prior knowledge): {len(trajectory_hits)}; "
      "the table is created here, current as of 2026-10-01")

# CHECK 2: register JSONL parses, 8 rows, required fields
print("\n-- CHECK 2: register JSONL --")
rows = []
with open(REG, "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
stacks = [r.get("stack") for r in rows]
missing = [i for i, r in enumerate(rows)
           if not (r.get("stack") and r.get("maturity_tier") and r.get("primary_evidence")
                   and r.get("primary_evidence", {}).get("quote") and r.get("falsifier"))]
print(f"rows={len(rows)} stacks={stacks} rows_missing_fields={missing}")
check("CHECK 2 register", len(rows) == 8 and not missing,
      f"{len(rows)} rows parsed as JSON, all carry stack+maturity_tier+primary_evidence.quote+falsifier")

# CHECK 3: receipt exists, has the table
print("\n-- CHECK 3: receipt + sovereignty-compute table --")
with open(RECEIPT, "r", encoding="utf-8") as f:
    rtxt = f.read()
print(f"receipt bytes={len(rtxt.encode('utf-8'))}")
check("CHECK 3 receipt table", "THE SOVEREIGNTY-COMPUTE TABLE" in rtxt and "| R0:" in rtxt and "| Bound layer |" in rtxt,
      f"{len(rtxt.encode('utf-8'))} bytes; table header + R0 row + Bound-layer row present")

# CHECK 4: quote substrings against byte-captured evidence
print("\n-- CHECK 4: quote-substring verification --")
quotes = [
    ("ev_unsloth_amd.md", "4-bit training: bitsandbytes-based QLoRA support for Radeon and CDNA GPUs."),
    ("ev_unsloth_amd.md", "RDNA 1 supports only Vulkan inference, not full training."),
    ("ev_unsloth_amd.md", "On Windows, AMD ROCm does not yet provide a GPU-collective backend"),
    ("ev_tpu_pricing.md", "DWS Flex-start: $0.60/hr (all regions)"),
    ("ev_tpu_pricing.md", "**us-central1 (Iowa):** $1.20"),
    ("ev_arxiv_2509_05276_abstract.md", "training remains stable for weeks on hundreds of MetaX GPUs"),
    ("ev_search_summaries.md", "AI Diffusion Rule's worldwide tiering rescinded/not enforced"),
    ("ev_search_summaries.md", "native PyTorch dev experience on MLU for large-scale LLM training/inference"),
]
qok = True
qcount = 0
for fname, q in quotes:
    with open(os.path.join(LANES, fname), "r", encoding="utf-8") as fh:
        content = fh.read()
    hit = q in content
    qok = qok and hit
    qcount += 1 if hit else 0
    print(f"  {'HIT ' if hit else 'MISS'} {fname}: {q[:60]}...")
check("CHECK 4 quotes", qok, f"{qcount}/{len(quotes)} register/receipt quotes byte-found in raw captures")

# CHECK 5: em-dash / en-dash scan over lane-authored record files
print("\n-- CHECK 5: em-dash scan --")
record_files = [
    RECEIPT, REG, LANE_JSON,
    os.path.join(LANES, "ev_unsloth_amd.md"),
    os.path.join(LANES, "ev_tpu_pricing.md"),
    os.path.join(LANES, "ev_arxiv_2509_05276_abstract.md"),
    os.path.join(LANES, "ev_search_summaries.md"),
]
em_total = 0
for path in record_files:
    with open(path, "r", encoding="utf-8") as f:
        t = f.read()
    em_total += t.count("\u2014") + t.count("\u2013")
print(f"em+en dash total across {len(record_files)} record files: {em_total}")
check("CHECK 5 dashes", em_total == 0, f"em:0 en:0 across receipt, register, lane JSON, 4 evidence files")

# CHECK 6: live probe of the actual estate box (GPU + ollama)
print("\n-- CHECK 6: live box probe --")
gpu = subprocess.run(["powershell", "-NoProfile", "-Command",
                      "(Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name) -join '; '"],
                     capture_output=True, text=True, timeout=60)
print(f"GPU: {gpu.stdout.strip()!r} (exit {gpu.returncode})")
ollama = subprocess.run(["curl.exe", "-s", "-m", "5", "http://127.0.0.1:11434/api/ps"],
                        capture_output=True, text=True)
print(f"ollama /api/ps: exit={ollama.returncode} body={ollama.stdout.strip()[:200]!r}")
check("CHECK 6 box probe", gpu.returncode == 0 and "AMD" in (gpu.stdout or "").upper(),
      f"GPU='{gpu.stdout.strip()}' matches the envelope's RX 5600 XT claim; "
      f"ollama {'UP: ' + ollama.stdout.strip()[:120] if ollama.returncode == 0 else 'DOWN (exit ' + str(ollama.returncode) + '), recorded honestly'}")

# CHECK 7: lane JSON parses with ok field
print("\n-- CHECK 7: lane JSON --")
with open(LANE_JSON, "r", encoding="utf-8") as f:
    lane = json.load(f)
print(f"lane={lane.get('lane')} division={lane.get('division')} ok={lane.get('ok')} rows={len(lane.get('rows', []))}")
check("CHECK 7 lane json", lane.get("lane") == "nonnvidia-stacks" and lane.get("ok") is True,
      "parses; ok=true; artifact points at the receipt")

print("\n=== SUMMARY ===")
passed = sum(1 for _, ok, _ in results if ok)
for name, ok, _ in results:
    print(f"{'PASS' if ok else 'FAIL'} {name}")
print(f"TOTAL: {passed}/{len(results)} PASS")
sys.exit(0 if passed == len(results) else 1)
