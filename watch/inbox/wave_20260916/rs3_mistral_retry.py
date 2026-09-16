"""RS one-offs: restore lane diversity after the driver's rotations.
1) RS3 (player one) on mistral-min8 with the random_seed fix (probe 422 was a seed-param bug).
2) RS2 (mud veteran) on cerebras-qwen with max_tokens raised to 4000 (reasoning channel
   burned the 2000 budget -> empty_content; D22 warned reasoning models need generous budget).
Both free-tier, taped, never raise. Run AFTER the main driver finished.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import rs_salon_witness_driver as drv  # noqa: E402


def run_one(witness_id: str, lane_id: str, tag: str, max_tokens_override=None) -> None:
    charters = json.load(open(os.path.join(HERE, "rs_witness_charters.json"), encoding="utf-8"))
    w = next(c for c in charters if c["id"] == witness_id)
    prompt = f"{drv.BRIEF}\n\n---\n\n{w['charter']}\n\n{drv.COMMON_TAIL}"
    if max_tokens_override is not None:
        base, model, key_name, host, _mt, timeout = drv.LANES[lane_id]
        drv.LANES[lane_id] = (base, model, key_name, host, max_tokens_override, timeout)
    rec = drv.dispatch(lane_id, prompt, w["temperature"], f"{witness_id}:{tag}")
    out = os.path.join(HERE, "rs_witness_posts", f"{witness_id}.{tag}.md")
    with open(out, "w", encoding="utf-8") as fh:
        if rec.get("ok"):
            fh.write(f"# {w['seat']}\n\n- lane: {rec['lane']} ({rec['model']}) [diversity retry]\n"
                     f"- temperature: {rec['temperature']}\n- usage: {rec.get('usage')}\n\n"
                     f"{rec['answer']}\n")
            print(f"[{tag}] OK <- {lane_id} ({rec['chars']} chars)", flush=True)
        else:
            fh.write(f"# {w['seat']}\n\nretry failed: {rec.get('error')} "
                     f"{rec.get('detail', '')[:200]}\n")
            print(f"[{tag}] FAILED: {rec.get('error')}", flush=True)


def main() -> None:
    run_one("RS3_player_one", "mistral-min8", "mistral")
    run_one("RS2_mud_veteran", "cerebras-qwen", "cerebras", max_tokens_override=4000)


if __name__ == "__main__":
    main()
