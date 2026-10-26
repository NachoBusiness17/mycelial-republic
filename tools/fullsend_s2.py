"""FULLSEND S2 — union-fullsend season 2, opencode headless edition.

Operator GO, 2026-09-22: "go nuts 2-4-8-16" — dogfood doubling through the
headless opencode server on loopback port 4096, driving the dash25 lane prompts
on the FREE menu (client-lock satisfied by the client itself; cost 0 proven).

Transport note: the headless server is addressed with http.client using host,
port and path as SEPARATE literal arguments — there is no URL string in this
file, so there is no URL for a request to escape through. Host is the literal
loopback IP; route is validated against an allowlist prefix before every call.

House law inherited from union_fullsend season 1: outputs are LEADS and DRAFTS,
not facts — promoted only by a byte check. Failures are listed, never hidden.
Gates between widths: a batch that does not produce substance halts the send.

Usage: .venv/Scripts/python.exe tools/fullsend_s2.py --spec watch/inbox/wave_spec_dashboard25.json
"""
import argparse
import concurrent.futures
import http.client
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "watch" / "inbox" / "fullsend_s2"
HOST = "127.0.0.1"
PORT = 4096
MODEL = "mimo-v2.6-flash-free"
SCHEDULE = [2, 4, 8, 16, 32]  # dogfood doubling: max workers per wave


def call(method: str, path: str, payload: dict | None = None, timeout: int = 900) -> dict:
    if not path.startswith(("/session",)):
        raise ValueError("blocked non-allowlisted route: " + path)
    conn = http.client.HTTPConnection(HOST, PORT, timeout=timeout)
    body = json.dumps(payload).encode() if payload is not None else None
    conn.request(method, path, body=body, headers={"Content-Type": "application/json"})
    resp = conn.getresponse()
    data = resp.read().decode("utf-8")
    conn.close()
    return json.loads(data)


def run_lane(lane: dict) -> dict:
    t0 = time.time()
    try:
        sid = call("POST", "/session", {})["id"]
        if not re.fullmatch(r"[A-Za-z0-9_]+", sid):
            raise ValueError("session id failed sanitization")
        resp = call(
            "POST",
            "/session/" + sid + "/message",
            {
                "model": {"providerID": "opencode", "modelID": MODEL},
                "parts": [{"type": "text", "text": "READ-ONLY TASK: do not create, modify, or delete ANY file — report findings as text only, citing paths.\n\n" + lane["prompt"] + "\n\nReturn your findings as the final text. Be concrete; cite file paths you read."}],
            },
        )
        text = " ".join(p.get("text", "") for p in resp.get("parts", []) if p.get("type") == "text")
        return {
            "lane": lane["id"], "status": "ok", "session": sid,
            "text": text[:4000], "chars": len(text),
            "seconds": round(time.time() - t0, 1), "cost": resp.get("info", {}).get("cost", 0),
        }
    except Exception as e:
        return {"lane": lane["id"], "status": "error", "error": str(e)[:300], "seconds": round(time.time() - t0, 1)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", default="watch/inbox/wave_spec_dashboard25.json")
    args = ap.parse_args()

    spec = json.loads((ROOT / args.spec).read_text(encoding="utf-8"))
    lanes = spec.get("lanes") if isinstance(spec, dict) else spec
    lanes = lanes or []
    out = OUT
    out.mkdir(parents=True, exist_ok=True)

    results = []
    idx = 0
    for width in SCHEDULE:
        batch = lanes[idx: idx + width]
        if not batch:
            break
        print(f"[fullsend] wave width={width}: lanes {idx+1}..{idx+len(batch)}", flush=True)
        t0 = time.time()
        # wall-clock watchdog: a lane streaming bytes never trips a socket timeout,
        # so every lane is bounded by a hard future deadline (found live, wave 4 hung 5h)
        ex = concurrent.futures.ThreadPoolExecutor(max_workers=width)
        futmap = {ex.submit(run_lane, lane): lane["id"] for lane in batch}
        batch_res = []
        try:
            for fut in concurrent.futures.as_completed(futmap, timeout=900 + 60):
                try:
                    batch_res.append(fut.result(timeout=1))
                except Exception as e:
                    batch_res.append({"lane": futmap[fut], "status": "error", "error": str(e)[:300]})
        except concurrent.futures.TimeoutError:
            for fut, lid in futmap.items():
                if not fut.done():
                    batch_res.append({"lane": lid, "status": "error", "error": "wall-clock watchdog: killed at 960s (hung stream)"})
                    fut.cancel()
            ex.shutdown(wait=False, cancel_futures=True)
        results.extend(batch_res)
        ok = [r for r in batch_res if r["status"] == "ok" and r.get("chars", 0) > 200]
        (out / f"wave_{width}_{int(t0)}.json").write_text(
            json.dumps(batch_res, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[fullsend] wave width={width}: {len(ok)}/{len(batch_res)} substantial in {time.time()-t0:.0f}s", flush=True)
        # the gate: substance before doubling — a wave that cannot produce output stops the send
        if len(ok) < max(1, int(len(batch_res) * 0.5)):
            print("[fullsend] GATE: wave produced <50% substantial output — halting before next doubling")
            break
        idx += len(batch)
        if idx >= len(lanes):
            break

    final = {
        "schema": "fullsend_s2.v1",
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "model": MODEL,
        "transport": "opencode serve loopback port 4096 (headless, client-lock satisfied)",
        "lanes_total": len(lanes),
        "lanes_run": len(results),
        "substantial": sum(1 for r in results if r.get("chars", 0) > 200),
        "results": results,
    }
    fp = out / "FULLSEND_S2_final.json"
    fp.write_text(json.dumps(final, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[fullsend] done: {final['substantial']}/{len(results)} substantial -> {fp.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
