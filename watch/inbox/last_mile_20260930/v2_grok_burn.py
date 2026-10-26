#!/usr/bin/env python
"""v2 grok judgment burn (2026-09-30). Operator order (V2 lane, budget $1.00):
test Grok 4.7 on Nous as a judgment seat. Three asks: N1's anti-hagiography frame
on OCEAN.md, N6's adversarial-grade frame on FINAL_PIECE.md, and a novel ask on
TIE_IT_ALL_20260930.md ("what is this estate missing that nobody asked today?").

Pattern stolen byte-shape from watch/inbox/mates_leave_protocol/night_burn_20260930.py
(pinned host, SSRF guard, reasoning cap, usage.cost meter, checkpointed jsonl).
Listed price at run time: $2.00/M prompt, $6.00/M completion (models endpoint);
the operator's $0.77/M claim is tested against the metered blend below."""
from __future__ import annotations

import json
import os
import pathlib
import time
import urllib.error
import urllib.parse
import urllib.request

HERMES_DIR = r"C:\Users\foste\AppData\Local\hermes"
ALLOWED_HOST = "inference-api.nousresearch.com"  # pinned destination; the only host this script may touch
BASE = "https://" + ALLOWED_HOST + "/v1/chat/completions"
REPO = pathlib.Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
OUT = REPO / "watch" / "inbox" / "last_mile_20260930" / "v2_grok_raw.jsonl"
MODEL = "x-ai/grok-4.7"
BUDGET_USD = 1.00


def load_dotenv(path):
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())


load_dotenv(os.path.join(HERMES_DIR, ".env"))
KEYS = [k for k in (os.environ.get("NOUS_SDD_API_KEY"), os.environ.get("HERMES_API_KEY_1")) if k]


def read(rel, limit=13000):
    return (REPO / rel).read_text(encoding="utf-8", errors="replace")[:limit]


OCEAN = read(r"watch\inbox\operator_model\OCEAN.md")
FINAL = read(r"watch\inbox\mountain_climb_ractor_20260929\FINAL_PIECE.md")
TIE = read(r"watch\inbox\TIE_IT_ALL_20260930.md")

# LAWS verbatim from the night burn (N1/N6 comparability law)
LAWS = "Laws: no em-dashes. No praise, no preamble. Cite section names for claims about the pasted text. Mark uncertainty UNPROVEN. Disagreement is the deliverable; do not validate framing."

ASKS = [
    # N1 frame, verbatim, retargeted at nothing: same ask, new judge (cross-family agreement test)
    {"id": "V2a-grok-hostile-ocean", "task_shape": "adversarial-review",
     "prompt": "You are a hostile reviewer preventing hagiography. Attack this personality extraction: which ratings lean on flattery, which evidence is cherry-picked, what does the data NOT support? Then: the one rating you would change and why.\n\n<DOC>\n" + OCEAN + "\n</DOC>\n" + LAWS},
    # N6 frame, verbatim, new judge
    {"id": "V2b-grok-grade-final-piece", "task_shape": "adversarial-grading",
     "prompt": "You are an adversarial grader. Grade this essay (a synthesized 'thing we will build' statement): fabrication check (numbers must match internal citations), power score /10, the three weakest claims, and whether the three 'dumb rules' survive hostile reading.\n\n<DOC>\n" + FINAL + "\n</DOC>\n" + LAWS},
    # Novel judgment ask
    {"id": "V2c-grok-estate-blindspot", "task_shape": "judgment",
     "prompt": "This is a day-close synthesis of a self-hosted agent estate (five organs: game platform skeleton, work meter, operator model, mates propagation, water physics). What is this estate missing that nobody asked today? Name the three highest-leverage omissions; for each, cite the line in the document that exposes the gap, and write the one question the estate should be asking but is not. Rank the three by leverage.\n\n<DOC>\n" + TIE + "\n</DOC>\n" + LAWS},
]


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D102
        return None  # redirects refused: the pinned host is the only destination


def call(prompt, key):
    p = urllib.parse.urlparse(BASE)
    if p.scheme != "https" or p.hostname != ALLOWED_HOST:
        raise AssertionError("blocked: non-pinned destination")
    body = json.dumps({"model": MODEL, "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": 16000, "temperature": 0.4,
                       "reasoning": {"max_tokens": 6000}}).encode()  # LESSIG RAILS: cap reasoning or the answer never gets written
    req = urllib.request.Request(BASE, data=body, headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    opener = urllib.request.build_opener(_NoRedirect)
    with opener.open(req, timeout=300) as r:
        return json.load(r)


def main():
    if not KEYS:
        print("NO KEYS - aborting without spend")
        return
    spent = 0.0
    for g in ASKS:
        if spent >= BUDGET_USD:
            print("BUDGET CAP HIT before " + g["id"])
            break
        key = KEYS[hash(g["id"]) % len(KEYS)]
        try:
            t0 = time.time()
            resp = call(g["prompt"], key)
            msg = resp["choices"][0]["message"]
            usage = resp.get("usage", {})
            cost = float(usage.get("cost") or 0)
            spent += cost
            row = {"id": g["id"], "model": MODEL, "task_shape": g["task_shape"],
                   "usage": {k: usage.get(k) for k in ("prompt_tokens", "completion_tokens", "total_tokens")},
                   "cost_usd": round(cost, 4), "spent_so_far": round(spent, 4),
                   "finish": resp["choices"][0].get("finish_reason"), "seconds": round(time.time() - t0, 1),
                   "content": msg.get("content"), "reasoning_tail": (msg.get("reasoning") or "")[-300:]}
            with open(OUT, "a", encoding="utf-8") as f:
                f.write(json.dumps(row) + "\n")
            print(f"done {g['id']} ${cost:.4f} finish={row['finish']} secs={row['seconds']}")
        except urllib.error.HTTPError as e:
            print(f"HTTPERR {g['id']} {e.code}: {e.read()[:200]}")
        except Exception as e:
            print(f"err {g['id']}: {e}")
    print(f"BURN DONE spent=${spent:.4f} -> {OUT}")


if __name__ == "__main__":
    main()
