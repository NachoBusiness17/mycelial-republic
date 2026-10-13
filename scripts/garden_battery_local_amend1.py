"""garden_battery_local_amend1 - amendment 1 for series local-20261001-a.

Two fixes applied to the landed artifacts:
1. convergence roll-up recomputed with DISTINCT-model sets per (path,
   50-line bucket); the first pass counted one model citing a bucket three
   times as overlap. Result: zero cross-model clusters exist (every
   resolving cite is gemma4; gemma2 cite rows all failed CITES-RESOLVE).
2. receipt re-rendered from the amended GRID (scores, throughput,
   identical-bytes proof, clusters, quant probe, ledger totals).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRID_PATH = ROOT / "watch/inbox/model_garden/GRID_local-20261001-a.json"


def recompute_convergence(g: dict) -> dict:
    conv = {}
    for model, items in g["grid"].items():
        for item, row in items.items():
            resolve_ok = (row.get("checks", {}).get("CITES-RESOLVE") == 1)
            for c in row.get("cites", []):
                if c["raw_or_path"] == "UNPARSED" or not c["nums"]:
                    continue
                key = f"{c['raw_or_path']}:{(min(c['nums']) - 1) // 50}"
                e = conv.setdefault(item, {}).setdefault(
                    key, {"models": [], "resolved": set(), "unresolved": set()})
                if model not in e["models"]:
                    e["models"].append(model)
                (e["resolved"] if resolve_ok else e["unresolved"]).add(model)
    out = {}
    for item, clusters in conv.items():
        rows = []
        for key, e in sorted(clusters.items()):
            if len(e["models"]) >= 2:
                verdict = ("lane-local overlap (distinct local models, same "
                           "lane; NOT cross-family convergence)")
            else:
                verdict = "model-unique evidence"
            if e["unresolved"] and not e["resolved"]:
                verdict += (" [citing row failed CITES-RESOLVE: "
                            "hallucination-risk cite]")
            rows.append({"key": key, "models": e["models"], "verdict": verdict})
        out[item] = rows
    return out


def render_receipt(g: dict) -> str:
    lines = []
    lines.append("# GARDEN BATTERY lane-local run local-20261001-a (receipt, amended)")
    lines.append("")
    lines.append("Instrument: lane-local-script (scripts/garden_battery_local.py + "
                 "scripts/garden_battery_local_refire.py). Canonical runner "
                 "tools/model_garden.py NOT used for firing: its SSRF/https fence "
                 "refuses the loopback endpoint by design. Fence NOT weakened. "
                 "Ask construction byte-matches model_garden.run_ask (system block "
                 "single-sourced from tools.hermes_burn._system_for, contract, "
                 "appended EVIDENCE sections, same closing line). Budget $0, zero "
                 "paid calls, 23 fires total, all local.")
    lines.append("")
    lines.append("Deviations and run incidents, all honest:")
    lines.append("- direct calls to ollama OpenAI-compat http://127.0.0.1:11434/v1 "
                 "with a browser UA; runtime ctx 8192 measured for all three models.")
    lines.append("- max_tokens 2048 local vs 12000 staged for remote families "
                 "(request param, not ask bytes; at the measured 11-28 tok/s, "
                 "12000 risks hours per rambling fire).")
    lines.append("- staging moved under the run twice (sibling family lane): "
                 "18:11:05 staged B6/B8 with ASK_TEXT.md evidence, 18:20:31 "
                 "reverted to the evidence-less spec shape. First pass fired "
                 "gemma2 B6/B8 on with-evidence bytes and errored gemma4 B6/B8 + "
                 "gemma:2b B6 on preflight; the refire amendment re-fired B6/B8 "
                 "for ALL models on the pinned post-revert staging (contracts "
                 "byte-verified identical, ask.json snapshotted under "
                 "lanelocal/local-20261001-a/ask_snapshot).")
    lines.append("- first-pass bug fixed by amendment: error rows graded the empty "
                 "string and banked vacuous passes (NO-FENCE / NO-TRAILING-WS on "
                 "a blank reply); DNF rows now carry 0 with an ERROR marker.")
    lines.append("- first-pass bug fixed by amendment: model tags contain colons, "
                 "so raw reply dumps landed in NTFS alternate data streams; all "
                 "18 recovered to sanitized filenames, slug fixed for future runs.")
    lines.append("- B7 prompts exceeded ctx: server kept the tail (prompt_tokens "
                 "4098-4099 observed against an ~11k-token ask); identical "
                 "truncation for every model, noted per row.")
    lines.append("- convergence roll-up recomputed with distinct-model sets; the "
                 "first pass counted one model triple-citing a bucket as overlap.")
    lines.append("")
    lines.append("## Scores (score_norm = checks_passed / checks_total)")
    lines.append("")
    lines.append("| model | B1 | B2 | B3 | B4 | B5 | B6 | B7 | B8 | mean |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for model, items in g["grid"].items():
        cells = []
        for item in ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8"]:
            r = items.get(item)
            if r:
                cells.append(f"{r['score_norm']:.2f} ({r['checks_passed']}/{r['checks_total']})")
            else:
                cells.append("-")
        vals = [r["score_norm"] for r in items.values()]
        lines.append(f"| {model} | " + " | ".join(cells) + f" | {sum(vals) / len(vals):.2f} |")
    lines.append("")
    lines.append("## Throughput (completion tokens / wall seconds, prompt processing included; local CPU)")
    lines.append("")
    lines.append("| model | item | tok/s | wall s | prompt tok | finish |")
    lines.append("|---|---|---|---|---|---|")
    for model, items in g["grid"].items():
        for item in ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8"]:
            r = items.get(item)
            if r:
                pt = r["notes"].split("prompt_tokens=")[-1].split(";")[0]
                lines.append(f"| {model} | {item} | {r['tok_s']} | {r['latency_s']} | {pt} | {r['finish']} |")
    lines.append("")
    lines.append("gemma2 Q5_K_M range 4.3-49.4 tok/s; gemma4 range 15.1-41.2 tok/s; "
                 "gemma:2b Q4_0 4.7-21.7 tok/s on its two probes.")
    lines.append("")
    lines.append("## Identical-bytes proof (user-message sha256 per item; all models identical)")
    lines.append("")
    for item, shas in sorted(g["ask_body_shas"].items()):
        uniq = set(shas.values())
        verdict = "IDENTICAL" if len(uniq) == 1 else "DIVERGENT (investigate)"
        lines.append(f"- {item}: {verdict} " + "; ".join(f"{m}={s[:16]}" for m, s in sorted(shas.items())))
    lines.append("")
    lines.append("## Evidence clusters (lane-local only; no cross-family convergence claimed)")
    lines.append("")
    for item, clusters in g["convergence"].items():
        for c in clusters:
            lines.append(f"- {item} {c['key']}: {', '.join(c['models'])} ({c['verdict']})")
    lines.append("")
    lines.append("Finding: every resolving cite is gemma4; gemma2 Q5_K_M emitted "
                 "praise or summaries with garbled and hallucinated cites (its "
                 "descent_driver.sh:183-186 cite is out of range for a ~40-line "
                 "file). Zero cross-model buckets: no convergent defect candidate "
                 "from this lane. gemma4 B3 (4/5) is the strongest review cell: "
                 "real atomic-rename and exit-code claims on descent_driver.sh "
                 "lines 13-22, failed only DISTINCT-EVIDENCE by triple-citing one "
                 "40-line file.")
    lines.append("")
    lines.append("## Quant probe: Q5_K_M scut vs its old Q4_0 self (gemma:2b)")
    lines.append("")
    lines.append("| item | gemma2:2b-instruct-q5_K_M | gemma:2b (Q4_0) | winner |")
    lines.append("|---|---|---|---|")
    for item in ["B6", "B7"]:
        a = g["grid"]["gemma2:2b-instruct-q5_K_M"][item]
        b = g["grid"]["gemma:2b"][item]
        if a["score_norm"] > b["score_norm"]:
            w = "Q5_K_M"
        elif b["score_norm"] > a["score_norm"]:
            w = "Q4_0"
        else:
            w = "tie"
        lines.append(f"| {item} | {a['score_norm']:.2f} ({a['checks_passed']}/{a['checks_total']}) "
                     f"| {b['score_norm']:.2f} ({b['checks_passed']}/{b['checks_total']}) | {w} |")
    lines.append("")
    lines.append("Byte answer: NO clean win. B6 (format law): the old Q4_0 self "
                 "BEATS the new Q5_K_M scut, 2/6 vs 0/6 (Q4_0 emits two of the "
                 "three byte-exact lines; Q5_K_M emits a fenced B1..B7 list with "
                 "trailing whitespace). B7 (long-context): Q5_K_M edges Q4_0, 1/4 "
                 "vs 0/4 (it alone names B2-552, inside a format-violating "
                 "ramble). Confounder, named: this is NOT one base model at two "
                 "quants; gemma:2b is family gemma 3B Q4_0 while gemma2:2b-"
                 "instruct-q5_K_M is family gemma2 2.6B Q5_K_M. The comparison is "
                 "new scut vs old scut as deployed, not a pure quantization delta.")
    lines.append("")
    lines.append("## Ledger (memory/runs/model_garden/usage.jsonl, channel=lane-local-script)")
    lines.append("")
    lines.append("- gemma2:2b-instruct-q5_K_M: 10 fires, 26208 prompt tok, 2467 completion tok, $0.00")
    lines.append("- gemma4:latest: 10 fires, 25648 prompt tok, 11909 completion tok, $0.00")
    lines.append("- gemma:2b: 3 fires, 4360 prompt tok, 640 completion tok, $0.00")
    lines.append("")
    lines.append("Raw replies: watch/inbox/model_garden/lanelocal/local-20261001-a/ "
                 "(attempt-1 dumps kept as *.attempt1.md where the amendment "
                 "re-fired; em-dash bytes, if a model emitted any, are sanitized "
                 "with a marker, and the NO-EM-DASH check banks the byte truth).")
    return "\n".join(lines) + "\n"


def main() -> None:
    g = json.loads(GRID_PATH.read_text(encoding="utf-8"))
    g["convergence"] = recompute_convergence(g)
    g.setdefault("amendments", []).append({
        "ts": "2026-10-01T22:40:00Z",
        "what": ("convergence roll-up recomputed with distinct-model sets per "
                 "(path, 50-line bucket); the first pass counted one model "
                 "citing a bucket three times as overlap; no cross-model "
                 "cluster exists: every resolving cite is gemma4, every gemma2 "
                 "cite row failed CITES-RESOLVE")})
    GRID_PATH.write_text(json.dumps(g, indent=2, ensure_ascii=False) + "\n",
                         encoding="utf-8")
    print("grid patched")
    receipt = ROOT / "watch/inbox/model_garden/GRID_local-20261001-a_RECEIPT.md"
    text = render_receipt(g)
    receipt.write_text(text, encoding="utf-8")
    assert b"\xe2\x80\x94" not in text.encode("utf-8"), "em-dash in receipt"
    print("receipt rendered, em-dash free,", len(text.encode('utf-8')), "bytes")


if __name__ == "__main__":
    main()
