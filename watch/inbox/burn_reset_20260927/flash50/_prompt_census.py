#!/usr/bin/env python3
"""One-shot census for deep-prompt-compiler (flash50), 2026-09-28.
Measures (a) receipt-token evidence mass per prompt, (b) the thesis-level
DCE ceiling on the RIB at jaccard 0.45. Ephemeral diagnostic, not a tool."""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "tools"))
from prompt_compiler import tokens, jaccard, EMDASH_RE  # noqa: E402

BASE = Path(__file__).resolve().parents[4]
RX_TOKEN = re.compile(
    r"(?:[A-Za-z0-9_\-./\\]{3,}\.\w{2,4}\b|\b20\d{2}[-/]\d{2}[-/]\d{2}\b"
    r"|\b[a-f0-9]{8,64}\b|\b\d[\d,]{3,}\b)")

PROMPTS = {
    "clippy": BASE / "watch/inbox/burn_reset_20260927/flash50/_clippy_block.txt",
    "tide": BASE / "watch/inbox/burn_reset_20260927/queue/Q-022_tide_prompt_v1_baseline.txt",
    "rib-k8s": BASE / "memory/rib/RIB_EMERGENT_TOOLING_K8S_DEEP_DIVE_20260810.md",
}

for name, p in PROMPTS.items():
    t = EMDASH_RE.sub(" - ", p.read_text(encoding="utf-8"))
    spans = RX_TOKEN.findall(t)
    mass = sum(len(s) for s in spans)
    print("%s: receipt-token spans=%d, token chars=%d, share of doc=%.1f%%"
          % (name, len(spans), mass, 100 * mass / max(1, len(t))))

# thesis-level DCE ceiling on the RIB
rib = PROMPTS["rib-k8s"].read_text(encoding="utf-8")
lines = [EMDASH_RE.sub(" - ", l) for l in rib.splitlines()]
sents = [s.strip() for ln in lines
         for s in re.split(r"(?<=[.;])\s+", ln.strip()) if len(s.strip()) >= 60]
kept, removed = [], 0
for s in sents:
    tk = tokens(s)
    if any(jaccard(tk, tokens(k)) >= 0.45 for k in kept):
        removed += len(s)
    else:
        kept.append(s)
print("rib-k8s thesis-DCE at 0.45: %d/%d long sentences redundant, %d chars removable (%.1f%% of doc)"
      % (len(sents) - len(kept), len(sents), removed, 100 * removed / 12318))
