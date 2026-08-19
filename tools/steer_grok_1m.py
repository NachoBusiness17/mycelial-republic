"""Give grok the 1M-context build context via the shared steer bus (relational).

One-shot: emits the steer to the bus AND folds it through bus_cadence so it lands on the
doctrine RIB + party subchain + routes to up seats. This is the "copilot gives the context,
grok writes it" handoff, done through the relation — not a live CDP drive.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

MSG = (
    "GROK - WRITE THE 1M-CONTEXT LIFT (operator: let grok write it, copilot gives the context). "
    "OBJECTIVE: use the 1M window across the system as a REASONING SURFACE while the verkle chain "
    "stays PERSISTENCE. Two-tier: chain owns the record, window loads the REAL mounted state "
    "instead of compressed pointers. DO NOT rebuild context_compression/checkpoint philosophy - "
    "lift the BOUNDS so seats reason from full truth. "
    "EXACT SITES (verified): "
    "1) mag/party_subchain.py mount(*, limit=24, max_chars=6000) - allow a 'full' mode "
    "(max_chars=None) so a seat mounts the ENTIRE append-only hash-chained transcript, not the "
    "last 6K. "
    "2) mag/game_dm.py turn() - calls party_subchain.mount(max_chars=6000) then clips "
    "transcript[-6000:]; lift to full when a 1M window is available (env MAG_FULL_CONTEXT=1), "
    "fall back to 6000 otherwise. "
    "3) mag/frontier_game.py play() - uses log[-3:] and log[-6:] and move[:70] truncation; lift "
    "to full party history when MAG_FULL_CONTEXT=1 (respect per-seat token budgets), keep [:70] "
    "only for log line rendering not prompt. "
    "4) mag/context_pack.py max_chars configs (1200-11000) - add a 'full' mode that loads the "
    "complete mounted subchain + doctrine RIB + world state instead of packed excerpts. "
    "5) mag/context_checkpoint.py - keep the 200-token pointer for persistence, but add optional "
    "full_context handoff across a model switch when MAG_FULL_CONTEXT=1. "
    "LAWS: chain = source of truth (never store window as truth); deterministic $0 core "
    "unchanged; down seats stay records; honor per-seat budgets (grok/chatgpt scarce, "
    "deepseek/local cheap); never break the inject_for/steer path. "
    "Env flag: MAG_FULL_CONTEXT=1 gates all lifts so the default behavior is unchanged. "
    "Return a RIB with the commit + verify (get_errors clean + a dry run showing a seat mounts "
    "full transcript)."
)


def main() -> int:
    from mag import steer

    r = steer.emit("operator", "operator", MSG)
    print("emit", r.get("ok"), r.get("path"))
    try:
        from mag.bus_cadence import cadence
        c = cadence()
        print("folded", c.get("n_folded"), "surfaces", c.get("surfaces"))
        for item in c.get("folded", []):
            print("  fold", item.get("id"), "rib", bool(item.get("fold", {}).get("ok")),
                  "sub", bool(item.get("fold", {}).get("subchain", {}).get("ok")))
            for rr in item.get("routed", []):
                print("    route", rr.get("surface"), rr.get("ok"), rr.get("task") or rr.get("error"))
    except Exception as e:  # noqa: BLE001
        print("cadence error:", str(e)[:160])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
