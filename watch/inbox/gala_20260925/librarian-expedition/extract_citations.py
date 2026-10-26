#!/usr/bin/env python
# cited-missing lane: extract primary-source citations from last-48h receipts.
# No em-dashes in emitted records (record law). Output pinned to archive lanes dir.
import os, re, json

ROOT = r"C:/Users/foste/Documents/projects/local_sovereign_agent"
INBOX = os.path.join(ROOT, "watch", "inbox")
LANES = os.path.abspath(os.path.join(INBOX, "gala_20260925", "librarian-expedition", "lanes"))

FILES = [
    ("48h_synth", os.path.join(INBOX, "48h_synth", "STORY.md")),
    ("48h_synth", os.path.join(INBOX, "48h_synth", "lattice.md")),
    ("48h_synth", os.path.join(INBOX, "48h_synth", "laws.md")),
    ("48h_synth", os.path.join(INBOX, "48h_synth", "measure.md")),
    ("48h_synth", os.path.join(INBOX, "48h_synth", "next.md")),
    ("48h_synth", os.path.join(INBOX, "48h_synth", "steals.md")),
    ("olm0930", os.path.join(INBOX, "frontier_olm_2026-09-30", "steal", "agent-memory-continuity.md")),
    ("olm0930", os.path.join(INBOX, "frontier_olm_2026-09-30", "steal", "kv-cache-context-engineering.md")),
    ("olm0930", os.path.join(INBOX, "frontier_olm_2026-09-30", "steal", "open-and-local-language-models via reddit.md")),
    ("olm0930", os.path.join(INBOX, "frontier_olm_2026-09-30", "steal", "open-and-local-language-models-x.md")),
    ("olm0930", os.path.join(INBOX, "frontier_olm_2026-09-30", "steal", "open-and-local-language-models.md")),
    ("olm0930", os.path.join(INBOX, "frontier_olm_2026-09-30", "steal", "quantization-compression.md")),
    ("olm1001", os.path.join(INBOX, "frontier_olm_2026-10-01", "steal", "kv-cache-context-engineering.md")),
    ("olm1001", os.path.join(INBOX, "frontier_olm_2026-10-01", "steal", "open-local-language-models via reddit.md")),
    ("olm1001", os.path.join(INBOX, "frontier_olm_2026-10-01", "steal", "open-local-language-models via x.md")),
    ("olm1001", os.path.join(INBOX, "frontier_olm_2026-10-01", "steal", "open-local-language-models.md")),
    ("olm1001", os.path.join(INBOX, "frontier_olm_2026-10-01", "steal", "quantization-compression.md")),
    ("olm1001", os.path.join(INBOX, "frontier_olm_2026-10-01", "DIGEST.md")),
    ("olm1001", os.path.join(INBOX, "frontier_olm_2026-10-01", "RECEIPT.md")),
    ("spiking", os.path.join(INBOX, "spiking_wide", "energy-frontier.md")),
    ("spiking", os.path.join(INBOX, "spiking_wide", "event-driven-resonance.md")),
    ("spiking", os.path.join(INBOX, "spiking_wide", "linear-family.md")),
    ("spiking", os.path.join(INBOX, "spiking_wide", "neuromorphic-hardware.md")),
    ("spiking", os.path.join(INBOX, "spiking_wide", "nonnvidia-stacks.md")),
    ("spiking", os.path.join(INBOX, "spiking_wide", "spikingbrain-deep.md")),
    ("spiking", os.path.join(INBOX, "spiking_wide", "upcycle-economics.md")),
    ("localfirst", os.path.join(INBOX, "localfirst", "adjacent.md")),
    ("localfirst", os.path.join(INBOX, "localfirst", "aida.md")),
    ("localfirst", os.path.join(INBOX, "localfirst", "atlas.md")),
    ("localfirst", os.path.join(INBOX, "localfirst", "lbrain.md")),
    ("localfirst", os.path.join(INBOX, "localfirst", "ownmem.md")),
    ("localfirst", os.path.join(INBOX, "localfirst", "pam.md")),
    ("localfirst", os.path.join(INBOX, "localfirst", "ragos.md")),
    ("localfirst", os.path.join(INBOX, "LOCALFIRST_MEMORY_LANDSCAPE_20261001.md")),
    ("drops", os.path.join(INBOX, "SPIKINGBRAIN_DROP_20261001.md")),
    ("drops", os.path.join(INBOX, "STRATA_DROP_20261001.md")),
    ("drops", os.path.join(INBOX, "DOUBLE_DROP_20261001.md")),
    ("drops", os.path.join(INBOX, "x_intel_drop_20261001.md")),
    ("drops", os.path.join(INBOX, "model_mating_paper_dig_20261001.md")),
    ("drops", os.path.join(INBOX, "ABLITERATUS_DROP_20260929.md")),
    ("ractor50", os.path.join(INBOX, "ractor50", "MCP_PARITY_R20_20261001.md")),
    ("ractor50", os.path.join(INBOX, "ractor50", "accuracy.md")),
    ("ractor50", os.path.join(INBOX, "ractor50", "communication.md")),
    ("ractor50", os.path.join(INBOX, "ractor50", "logic.md")),
    ("ractor50", os.path.join(INBOX, "ractor50", "mcp.md")),
    ("ractor50", os.path.join(INBOX, "ractor50", "operations.md")),
    ("ractor50", os.path.join(INBOX, "ractor50", "selfsteal.md")),
    ("ractor50", os.path.join(INBOX, "ractor50", "skills.md")),
]

ARXIV = re.compile(r"arxiv\.org/(?:abs|pdf|html)/([0-9]{4}\.[0-9]{4,5})(?:v[0-9]+)?", re.I)
GH    = re.compile(r"github\.com/([A-Za-z0-9_.\-]+)/([A-Za-z0-9_.\-]+)", re.I)
# bare arXiv id: YYMM.NNNNN with month 01-12 validated (2609.33180, 2310.10158 ...)
BARE  = re.compile(r"(?<![\w.])2[0-9](0[1-9]|1[0-2])\.[0-9]{4,5}(?![.\d])")

out = []
INBOX_NORM = os.path.normcase(os.path.normpath(INBOX))
for group, path in FILES:
    apath = os.path.abspath(path)
    if not os.path.normcase(os.path.normpath(apath)).startswith(INBOX_NORM) or not os.path.isfile(apath):
        out.append({"group": group, "path": apath, "error": "missing-file"})
        continue
    with open(apath, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    for lineno, line in enumerate(lines, 1):
        for m in ARXIV.finditer(line):
            out.append({"group": group, "file": apath, "line": lineno,
                        "kind": "arxiv", "value": m.group(1)})
        for m in GH.finditer(line):
            out.append({"group": group, "file": apath, "line": lineno,
                        "kind": "github", "value": f"{m.group(1)}/{m.group(2)}"})
        for m in BARE.finditer(line):
            val = m.group(0)
            # skip if already covered by an explicit arxiv.org match on this line
            if any(r["line"] == lineno and r["kind"] == "arxiv" and r["value"] == val for r in out):
                continue
            out.append({"group": group, "file": apath, "line": lineno,
                        "kind": "arxiv-bare", "value": val})

seen = set()
dedup = []
for r in out:
    if "error" in r:
        dedup.append(r); continue
    k = (r["group"], r["file"], r["line"], r["kind"], r["value"])
    if k not in seen:
        seen.add(k); dedup.append(r)

groups = {}
for r in dedup:
    groups[r.get("group")] = groups.get(r.get("group"), 0) + 1
print(json.dumps({"total_rows": len(dedup), "by_group": groups,
                  "errors": [r for r in dedup if "error" in r]}, indent=2))
outpath = os.path.join(LANES, "citations_raw.json")
with open(outpath, "w", encoding="utf-8") as f:
    json.dump(dedup, f, indent=1)
print("wrote", outpath)
