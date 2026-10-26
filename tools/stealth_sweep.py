"""stealth_sweep — burn the free wall daily: live-fire OpenRouter's :free and :stealth
models on a real scored chore, keep the winners (2026-09-24, operator: "we need to use
this compute everyday").

One run = MODELS_PER_RUN models (cursor advances through the catalog across runs, so
repeated daily runs eventually cover the whole free wall, then re-score it).
Chore + scoring: same anchor-note bar as model_bakeoff (correct = cites 1976).
Both OpenRouter keys alternate; modest concurrency. SSRF law: every outbound URL
passes lite_guard._safe_https_url; redirects refused via lite_guard._OPENER.
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from models.env_load import load_dotenv
load_dotenv()
from mag import lite_guard  # noqa: E402
from mag import claritas  # noqa: E402

LEDGER = ROOT / "state" / "fuel" / "stealth_ledger.jsonl"
REPORT = ROOT / "watch" / "inbox" / "STEALTH_SWEEP_LATEST.md"
MODELS_PER_RUN = 40
CONCURRENCY = 6
URL = "https://openrouter.ai/api/v1/chat/completions"
PROMPT = ("A verified receipt: the Church Committee issued its Final Report (S. Rep. 94-755) "
          "in April 1976, exposing COINTELPRO (2,000+ covert actions) and SHAMROCK (~150,000 "
          "telegrams/month copied). In exactly two sentences, write an anchor note for this "
          "receipt that a public post could quote. Include the year 1976.")


def keys() -> list[str]:
    out = []
    for e in ("OPENROUTER_API_KEY", "OPENROUTER_API_KEY_2"):
        k = (os.environ.get(e, "") or "").strip()
        if k:
            out.append(k)
    return out


def _fetch(url: str, headers: dict, timeout: int, data: bytes | None = None) -> str:
    """The one outbound door: https-only, public-host validated, redirects refused."""
    if not lite_guard._safe_https_url(url):
        raise RuntimeError(f"SSRF guard rejected url: {url}")
    req = urllib.request.Request(url, data=data, headers=headers)
    with lite_guard._OPENER.open(req, timeout=timeout) as r:
        return r.read().decode()


def catalog(ks: list[str]) -> list[dict]:
    data = json.loads(_fetch("https://openrouter.ai/api/v1/models",
                             {"Authorization": f"Bearer {ks[0]}"}, 30))
    rows = data.get("data", []) if isinstance(data, dict) else data
    out = []
    for m in rows:
        mid = m.get("id", "")
        if mid.endswith(":free") or "stealth" in mid:
            out.append({"id": mid, "ctx": m.get("context_length", 0)})
    return sorted(out, key=lambda x: x["id"])


def call(model: str, ks: list[str], idx: int) -> dict:
    k = ks[idx % len(ks)]
    msgs = [{"role": "system", "content": claritas.face_for(model)},
            {"role": "user", "content": PROMPT}]
    body = json.dumps({"model": model, "messages": msgs, "max_tokens": 900}).encode()
    hdrs = {"Authorization": f"Bearer {k}", "Content-Type": "application/json",
            "User-Agent": "mag-estate-stealth-sweep/1.0"}
    t0 = time.time()
    try:
        out = json.loads(_fetch(URL, hdrs, 60, data=body))
        ms = round((time.time() - t0) * 1000)
        msg = (out.get("choices") or [{}])[0].get("message", {}) or {}
        content = (msg.get("content") or "").strip()
        usage = out.get("usage", {}) or {}
        ctoks = usage.get("completion_tokens", 0) or 0
        correct = ("1976" in content) and len(content) > 60
        hollow = (not content) and ctoks > 0  # reasoning burned the budget, no answer
        row = {"model": model, "ok": bool(content), "correct": correct, "ms": ms,
               "tok_s": round(ctoks / (ms / 1000), 1) if ms and ctoks else 0,
               "reply_head": content[:110], "hollow": hollow, "err": ""}
    except Exception as e:  # noqa: BLE001
        row = {"model": model, "ok": False, "correct": False, "ms": round((time.time() - t0) * 1000),
               "tok_s": 0, "reply_head": "", "err": f"{type(e).__name__}: {str(e)[:110]}"}
    row["ts"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return row


def main() -> None:
    ks = keys()
    if not ks:
        print("no openrouter keys"); return
    cat = catalog(ks)
    stealth = [m["id"] for m in cat if "stealth" in m["id"]]
    free = [m["id"] for m in cat if m["id"].endswith(":free")]
    # cursor: resume where the last run stopped, wrap at end
    done = set()
    if LEDGER.is_file():
        for line in LEDGER.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                r = json.loads(line)
                err = r.get("err", "") or ""
                hard = "403" in err or "404" in err  # gated/gone: done for this cycle
                if r.get("ok") or hard:
                    done.add(r.get("model", ""))
            except Exception:
                pass
    pool = [m for m in (stealth + free) if m not in done] or (stealth + free)
    batch = pool[:MODELS_PER_RUN]
    print(f"catalog: {len(stealth)} stealth, {len(free)} free; done {len(done)}; firing {len(batch)}")

    results: list[dict] = []
    from concurrent.futures import as_completed
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
        futs = {ex.submit(call, m, ks, i): m for i, m in enumerate(batch)}
        for n, fut in enumerate(as_completed(futs), 1):
            row = fut.result()
            results.append(row)
            flag = "CORRECT" if row["correct"] else ("ok" if row["ok"] else f"FAIL {row['err'][:40]}")
            print(f"  [{n}/{len(batch)}] {row['model']}: {flag} {row['ms']}ms {row['tok_s']}tok/s")
            with LEDGER.open("a", encoding="utf-8") as f:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")

    good = [r for r in results if r["correct"]]
    good.sort(key=lambda r: r["tok_s"], reverse=True)
    lines = [
        f"# Stealth sweep — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%MZ')}",
        "",
        f"Fired {len(results)} of the free wall ({len(stealth)} stealth / {len(free)} free total, "
        f"{len(done)} scored before this run). Correct on the anchor chore: **{len(good)}**.",
        "",
        "| model | ms | tok/s | reply head |",
        "|---|---|---|---|",
    ]
    for r in good:
        lines.append(f"| {r['model']} | {r['ms']} | {r['tok_s']} | {r['reply_head'][:70]} |")
    fails = [r for r in results if not r["ok"]]
    if fails:
        lines += ["", f"## Fails ({len(fails)})", ""]
        for r in fails[:12]:
            lines.append(f"- {r['model']}: {r['err'][:100]}")
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    try:
        from tools.md_record_seal import autoseal_file
        autoseal_file(REPORT)
        mined = REPORT.parent / "STEALTH_MINED_FINDINGS.jsonl"
        if mined.exists():
            autoseal_file(mined)
    except Exception:
        pass
    print(f"\nCORRECT: {len(good)}/{len(results)} — report: {REPORT}")


if __name__ == "__main__":
    main()
