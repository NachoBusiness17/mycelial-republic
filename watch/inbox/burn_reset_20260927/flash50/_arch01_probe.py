"""arch-01 instrument: mag/context_pack.py render probe + source region scans.

Read-only except: (a) PACK_OFFLOAD.jsonl rows appended by the pack's own
designed offload emitter during live renders, (b) residual_census.json cache
touches are avoided via fast=True. No subprocess. ASCII only.
Usage:
  python _arch01_probe.py            # full probe, dumps _arch01_out.json
  python _arch01_probe.py dashscan <path>   # em/en dash scan of a file
"""
import json
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
if not (ROOT / "mag" / "context_pack.py").is_file():
    ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))

RENDER_KEYS = [
    "compass_framework", "checkpoint_restore", "resonance_cards", "token_note",
    "layers", "commands", "quantized_laws", "doctrine", "directives",
    "behavioral_excerpt", "coordination_excerpt", "zeitgeist_excerpt",
    "proven_moves", "solved_excerpt", "subchain_full", "world_state",
    "live_tail", "attention_tail", "todo_open", "open_loops", "run_trail",
    "agent_state", "continuity", "resonance_l0e", "mirror_voice_excerpt",
    "clue_chain_excerpt", "build_excerpt", "scope_excerpt", "skills_excerpt",
    "ijl_skills", "brief", "bonds", "health", "models", "bonds_meta",
    "dirac_loops", "full_context",
]


def dashscan(path: str) -> None:
    text = Path(path).read_text(encoding="utf-8")
    em = text.count("\u2014")
    en = text.count("\u2013")
    print(f"dashscan {path}: em={em} en={en} total={em + en}")


def count_offload(off: Path) -> int:
    if not off.is_file():
        return 0
    return sum(1 for l in off.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip())


def main() -> None:
    out = {}
    src_path = ROOT / "mag" / "context_pack.py"
    src = src_path.read_text(encoding="utf-8")
    lines = src.splitlines()
    out["file_lines"] = len(lines)
    out["file_bytes"] = src_path.stat().st_size
    out["repo_root"] = str(ROOT)

    # Region key scans: quoted-key occurrences per region. Render region =
    # format_context_pack_text + format_agent_preamble (lines 993..end).
    assemble_region = "\n".join(lines[:992])
    render_region = "\n".join(lines[992:])
    out["key_hits_assemble_region"] = {
        k: len(re.findall('"' + re.escape(k) + '"', assemble_region)) for k in RENDER_KEYS}
    out["key_hits_render_region"] = {
        k: len(re.findall('"' + re.escape(k) + '"', render_region)) for k in RENDER_KEYS}

    obj = ROOT / "memory" / "boot" / "CURRENT_OBJECTIVE.md"
    out["objective_chars"] = (
        len(obj.read_text(encoding="utf-8", errors="replace").strip()) if obj.is_file() else None)

    off = ROOT / "watch" / "inbox" / "PACK_OFFLOAD.jsonl"
    out["offload_rows_before"] = count_offload(off)

    rib = ROOT / "memory" / "rib"
    rib_files = sorted(rib.glob("*.md")) if rib.is_dir() else []
    out["rib_file_count"] = len(rib_files)
    out["rib_first3"] = [p.name for p in rib_files[:3]]
    out["rib_last3"] = [p.name for p in rib_files[-3:]]

    qrep = ROOT / "memory" / "corpus" / "quantized_thought" / "compile_report.json"
    qflash = ROOT / "memory" / "corpus" / "quantized_thought" / "instructions_flash.jsonl"
    out["quant_flash_rows"] = (
        sum(1 for l in qflash.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip())
        if qflash.is_file() else 0)
    if qrep.is_file():
        try:
            out["quant_report"] = json.loads(qrep.read_text(encoding="utf-8"))
        except ValueError:
            out["quant_report"] = "unparseable"
    else:
        out["quant_report"] = None

    from mag.context_pack import MODE_CONFIG, build_context_pack, evolving_tail, format_agent_preamble, format_context_pack_text

    out["budgets"] = {m: MODE_CONFIG[m]["max_chars"] for m in MODE_CONFIG}
    out["modes"] = {}
    modes = ["janitor", "route", "build", "audit", "plan", "full"]
    for m in modes:
        before = count_offload(off)
        t0 = time.time()
        pack = build_context_pack(mode=m, fast=True)
        t_build = time.time() - t0
        t0 = time.time()
        text = format_context_pack_text(pack, mode=m)
        t_render = time.time() - t0
        after = count_offload(off)
        stages = []
        if after > before:
            for l in off.read_text(encoding="utf-8", errors="replace").splitlines()[before:after]:
                if l.strip():
                    try:
                        stages.append(json.loads(l).get("stage"))
                    except ValueError:
                        stages.append("unparseable")
        fields = ["brief", "bonds", "doctrine", "quantized_laws", "coordination_excerpt",
                  "behavioral_excerpt", "directives", "continuity", "agent_state",
                  "zeitgeist_excerpt", "skills_excerpt", "ijl_skills", "proven_moves",
                  "solved_excerpt", "attention_tail", "live_tail", "compass_framework",
                  "checkpoint_restore"]
        doctrine = pack.get("doctrine") or ""
        rec = {
            "budget": pack.get("pack_max_chars"),
            "assembled_json_bytes": len(json.dumps(pack, ensure_ascii=False, default=str)),
            "rendered_chars": len(text),
            "build_s": round(t_build, 2),
            "render_s": round(t_render, 2),
            "offload_rows_emitted": after - before,
            "stages_fired": stages,
            "doctrine_entries": sum(1 for ln in doctrine.splitlines() if ln.startswith("- ")),
            "driving_ladder_in_doctrine": "DRIVING_LADDER" in doctrine,
            "field_lens": {k: len(str(pack.get(k) or "")) for k in fields},
            "has_compiled_laws": "Compiled laws" in text,
            "has_objective": "Current objective" in text,
            "has_task_brief": "### Brief" in text,
            "text_tail": text[-120:],
        }
        out["modes"][m] = rec

    # Downstream tails probed on the full-mode render.
    full_pack = None
    pre = count_offload(off)
    full_pack = build_context_pack(mode="full", fast=True)
    full_text = format_context_pack_text(full_pack, mode="full")
    tail = evolving_tail(pack_text=full_text)
    pre_amble = format_agent_preamble(full_pack)
    out["downstream_full"] = {
        "evolving_tail_chars": len(tail),
        "evolving_tail_clipped": tail.rstrip().endswith("(tail clipped)"),
        "preamble_chars": len(pre_amble),
        "preamble_clipped": "(preamble clipped)" in pre_amble,
        "offload_rows_from_downstream": count_offload(off) - pre,
    }

    out["offload_rows_after"] = count_offload(off)
    dump = HERE / "_arch01_out.json"
    dump.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: out[k] for k in
                      ["file_lines", "file_bytes", "offload_rows_before", "offload_rows_after",
                       "rib_file_count", "objective_chars", "quant_flash_rows", "budgets"]},
                     indent=2))
    print("key_hits_render_region_zero:",
          sorted(k for k, v in out["key_hits_render_region"].items() if v == 0))
    for m in modes:
        r = out["modes"][m]
        print(f"mode={m} budget={r['budget']} assembled~{r['assembled_json_bytes']}B "
              f"rendered={r['rendered_chars']} stages={r['stages_fired']} "
              f"laws={r['has_compiled_laws']} obj={r['has_objective']} brief={r['has_task_brief']} "
              f"rib_entries={r['doctrine_entries']}/{out['rib_file_count']} "
              f"ladder_in_rib={r['driving_ladder_in_doctrine']} tail={r['text_tail']!r}")
    print("downstream_full:", json.dumps(out["downstream_full"]))
    print(f"out dumped: {dump}")


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "dashscan":
        dashscan(sys.argv[2])
    else:
        main()
