"""run_openjev_ab.py - openjev A/B runner (GO row 9, MICKEY17_V2; night-window lane).

Scores the FROZEN 30-item judge set (watch/openjev_ab/frozen30_20260925.jsonl)
under two arms and files the comparison. The set hash is verified before any
call is made; a mutated set refuses to run.

  Arm A (current judge): the estate's lane-runner verifier seat, verbatim:
      mag/lane_runner.flash_call -> glm-5.3-flash via the Z.ai Lite key
      (LAW-058 pin-check + lite_guard pacing + thought bank all inherited by
      import). Judge prompt is the fixed string below; output parsed as strict
      JSON {"supports": "yes"|"no", "confidence": 0..1, "reason": str}.

  Arm B (challenger): openjev qwen3.5-4b-nli-v5 served by the checkpoint repo's
      own SGLang package (serve_sglang.sh, sglang 0.5.19 line). This runner
      speaks the client wire contract directly (stdlib urllib, no new deps):
      POST {base}/classify  body {"text": ["Premise: {p}\\nHypothesis: {h}"]}
      -> [{"embedding": [contradiction, entailment, neutral] logits}]
      softmax -> P(yes) = P(entailment); label = yes iff P(yes) >= 0.5.

Laws honored by this script:
  - NO model download, NO local inference happen at prep time. Arm B needs the
    night window to serve the checkpoint first; until then arm B is infra-down
    and is reported as infra-down (never substituted with another model).
  - Family-box window guard: real arm-B calls are refused outside 23:00-09:00
    local unless --force (the refusal is itself receipted).
  - Honest failure: transport deaths are retried ONCE, then recorded as
    infra-fail rows. A parse miss is recorded, never guessed.
  - prior_judge fields never enter any prompt (leak-proof by construction).

Usage (from repo root):
  ./.venv/Scripts/python.exe watch/openjev_ab/run_openjev_ab.py --selftest
  ./.venv/Scripts/python.exe watch/openjev_ab/run_openjev_ab.py --arms a
  ./.venv/Scripts/python.exe watch/openjev_ab/run_openjev_ab.py --arms both --arm-b-url http://127.0.0.1:30000

Outputs land in watch/openjev_ab/results/<utcstamp>/ :
  rows.jsonl   one row per item per arm (raw + parsed)
  summary.json metrics vs the pre-registered bars in the protocol
  receipt.md   the human-readable night receipt
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
import time
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FROZEN = ROOT / "watch" / "openjev_ab" / "frozen30_20260925.jsonl"
SET_SHA256_EXPECTED = "8e0b6da1f283a3011b68c8a277d6fac91ec4a865ec56d387d84a339c92cb856d"
RESULTS_DIR = ROOT / "watch" / "openjev_ab" / "results"

ARM_B_TEMPLATE = "Premise: {premise}\nHypothesis: {hypothesis}"
CON, ENT, NEU = 0, 1, 2
DECISION_THRESHOLD = 0.5          # pre-registered: yes iff P(entailment) >= 0.5
ESCALATION_MARGIN = 0.15          # |p-0.5| below this escalates
ESCALATION_CONF = 0.70            # arm-A confidence below this escalates

# Pre-registered bars (OPENJEV_AB_PROTOCOL_20260925.md, section 6): the A/B
# verdict is computed here, mechanically, from these exact numbers.
PASS_AGREEMENT = 24 / 30          # >= 0.80 raw agreement arm A vs arm B
PASS_KAPPA = 0.60
PASS_NONINFERIOR_PP = 10.0        # arm B vs prior >= arm A vs prior - 10pp
PARTIAL_AGREEMENT = 18 / 30       # 0.60..0.79 -> meter-only adoption

ARM_A_SYSTEM = (
    "You are the estate's verdict seat. Answer only from the material given. "
    "Output strict JSON and nothing else.")
ARM_A_USER_TMPL = (
    "PREMISE (verbatim source quote):\n"
    "\"\"\"{premise}\"\"\"\n\n"
    "HYPOTHESIS (claim):\n"
    "\"\"\"{hypothesis}\"\"\"\n\n"
    "Question: {question}\n"
    "Options: no, yes.\n"
    "Rubric:\n"
    "no: {rubric_no}\n"
    "yes: {rubric_yes}\n\n"
    "Reply with strict JSON exactly: "
    '{{"supports": "yes" or "no", "confidence": 0.0 to 1.0, '
    '"reason": "at most 40 words"}}')


def sha(s: str) -> str:
    import hashlib
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def load_frozen() -> list[dict]:
    if not FROZEN.is_file():
        raise SystemExit(f"frozen set missing: {FROZEN}")
    text = FROZEN.read_text(encoding="utf-8")
    got = sha(text)
    if got != SET_SHA256_EXPECTED:
        raise SystemExit(
            f"FROZEN SET HASH MISMATCH: file {got[:16]}.. != expected "
            f"{SET_SHA256_EXPECTED[:16]}.. - refusing to score a mutated set. "
            "Re-run watch/openjev_ab/freeze_frozen30.py and re-pin the hash in "
            "the protocol instead of scoring drifted items.")
    rows = [json.loads(l) for l in text.splitlines() if l.strip()]
    for r in rows:
        blob = json.dumps(
            {"state": r["state"], "question": r["question"],
             "options": r["options"], "rubric": r["rubric"]},
            sort_keys=True, ensure_ascii=False)
        if sha(blob) != r["item_sha256"]:
            raise SystemExit(f"item hash mismatch: {r['item_id']}")
    if len(rows) != 30:
        raise SystemExit(f"expected 30 items, file has {len(rows)}")
    return rows


# --------------------------------------------------------------------- arm A
def parse_json_blob(raw: str) -> dict | None:
    if not raw:
        return None
    m = re.search(r"\{.*\}", raw, re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
    except Exception:
        return None
    if d.get("supports") not in ("yes", "no"):
        return None
    try:
        d["confidence"] = float(d.get("confidence"))
    except Exception:
        d["confidence"] = None
    return d


def run_arm_a(items: list[dict]) -> list[dict]:
    sys.path.insert(0, str(ROOT))
    from mag.lane_runner import flash_call  # the current judge door, verbatim
    out = []
    for it in items:
        user = ARM_A_USER_TMPL.format(
            premise=it["state"]["premise"], hypothesis=it["state"]["hypothesis"],
            question=it["question"], rubric_no=it["rubric"]["no"],
            rubric_yes=it["rubric"]["yes"])
        t0 = time.monotonic()
        err = None
        try:
            raw = flash_call(ARM_A_SYSTEM, user, max_tokens=1536)
        except Exception as e:  # noqa: BLE001 - honest infra row, not a crash
            raw, err = "", f"{type(e).__name__}: {e}"
        dt = round(time.monotonic() - t0, 3)
        parsed = parse_json_blob(raw) if raw else None
        out.append({
            "item_id": it["item_id"], "arm": "a",
            "prompt": user, "raw": raw, "error": err, "latency_s": dt,
            "supports": (parsed or {}).get("supports"),
            "confidence": (parsed or {}).get("confidence"),
            "reason": (parsed or {}).get("reason"),
            "parse_ok": parsed is not None,
        })
        print(f"A {it['item_id']} supports={out[-1]['supports']} "
              f"conf={out[-1]['confidence']} {dt}s "
              f"{'ERR:' + str(err) if err else ''}", flush=True)
    return out


# --------------------------------------------------------------------- arm B
def _post_classify(url: str, text: str, timeout: int = 120) -> list[float]:
    """Returns the raw [contradiction, entailment, neutral] logits."""
    body = json.dumps({"text": [text]}).encode("utf-8")
    req = urllib.request.Request(
        url.rstrip("/") + "/classify", data=body,
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        out = json.loads(r.read())
    rec = out[0] if isinstance(out, list) else out
    emb = rec["embedding"]
    if not isinstance(emb, list) or len(emb) != 3:
        raise ValueError(f"/classify embedding must be 3 logits, got: {emb!r}")
    return [float(x) for x in emb]


def softmax3(z: list[float]) -> list[float]:
    m = max(z)
    e = [pow(2.718281828459045, x - m) for x in z]
    s = sum(e)
    return [x / s for x in e]


def run_arm_b(items: list[dict], base_url: str) -> list[dict]:
    out = []
    for it in items:
        text = ARM_B_TEMPLATE.format(
            premise=it["state"]["premise"].strip(),
            hypothesis=it["state"]["hypothesis"].strip())
        t0 = time.monotonic()
        logits = probs = None
        err = None
        for attempt in (1, 2):  # transport death: retry once, then record
            try:
                logits = _post_classify(base_url, text)
                probs = softmax3(logits)
                break
            except Exception as e:  # noqa: BLE001
                err = f"{type(e).__name__}: {e}"
                if attempt == 1:
                    time.sleep(2.0)
        dt = round(time.monotonic() - t0, 3)
        if probs is None:
            out.append({"item_id": it["item_id"], "arm": "b", "prompt": text,
                        "raw": None, "error": err, "latency_s": dt,
                        "supports": None, "p_con": None, "p_ent": None,
                        "p_neu": None, "margin": None, "parse_ok": False})
            print(f"B {it['item_id']} INFRA-FAIL {err} {dt}s", flush=True)
            continue
        p_yes = probs[ENT]
        margin = abs(p_yes - DECISION_THRESHOLD)
        out.append({
            "item_id": it["item_id"], "arm": "b", "prompt": text,
            "raw": {"logits_con_ent_neu": logits, "probs_con_ent_neu": probs},
            "error": None, "latency_s": dt,
            "supports": "yes" if p_yes >= DECISION_THRESHOLD else "no",
            "p_con": probs[CON], "p_ent": probs[ENT], "p_neu": probs[NEU],
            "margin": round(margin, 4), "parse_ok": True,
        })
        print(f"B {it['item_id']} supports={out[-1]['supports']} "
              f"p_ent={p_yes:.4f} {dt}s", flush=True)
    return out


# ------------------------------------------------------------------- metrics
def kappa(a: list[str], b: list[str]) -> float:
    n = len(a)
    if n == 0:
        return 0.0
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    pe = 0.0
    for c in set(a) | set(b):
        rm = sum(1 for x in a if x == c) / n
        cm = sum(1 for y in b if y == c) / n
        pe += rm * cm
    if pe >= 1.0:
        return 1.0 if po >= 1.0 else 0.0
    return (po - pe) / (1.0 - pe)


def summarize(items, rows_a, rows_b) -> dict:
    prior = {i["item_id"]: i["prior_judge"]["supports"] for i in items}
    la = {r["item_id"]: r for r in rows_a}
    lb = {r["item_id"]: r for r in rows_b}
    ids = [i["item_id"] for i in items]
    va = [la[i]["supports"] for i in ids]
    vb = [lb[i]["supports"] for i in ids]
    vp = [prior[i] for i in ids]
    both = all(v is not None for v in va) and all(v is not None for v in vb)
    agree = sum(1 for x, y in zip(va, vb) if x == y and x is not None and y is not None)
    pairable = sum(1 for x, y in zip(va, vb) if x is not None and y is not None)
    ma = sum(1 for x, y in zip(va, vp) if x == y)
    mb = sum(1 for x, y in zip(vb, vp) if x == y)
    marg_ok = [lb[i]["margin"] for i in ids if lb[i]["margin"] is not None]
    escal = []
    for i in ids:
        why = []
        if la[i]["supports"] and lb[i]["supports"] and la[i]["supports"] != lb[i]["supports"]:
            why.append("arm-disagreement")
        if la[i]["confidence"] is not None and la[i]["confidence"] < ESCALATION_CONF:
            why.append("arm-a-low-confidence")
        if lb[i]["margin"] is not None and lb[i]["margin"] < ESCALATION_MARGIN:
            why.append("arm-b-low-margin")
        if la[i]["supports"] is None or lb[i]["supports"] is None:
            why.append("arm-infra-or-parse-fail")
        if why:
            escal.append({"item_id": i, "why": why,
                          "arm_a": la[i]["supports"], "arm_b": lb[i]["supports"],
                          "prior": prior[i]})
    infra_a = sum(1 for r in rows_a if r["supports"] is None)
    infra_b = sum(1 for r in rows_b if r["supports"] is None)
    agree_rate = (agree / pairable) if pairable else 0.0
    verdict = {
        "adopt_candidate": bool(
            both and pairable == 30 and infra_b == 0 and infra_a == 0
            and agree_rate >= PASS_AGREEMENT
            and kappa([x or "?" for x in va], [x or "?" for x in vb]) >= PASS_KAPPA
            and (100.0 * mb / 30) >= (100.0 * ma / 30) - PASS_NONINFERIOR_PP),
        "meter_only": bool(
            both and infra_b == 0 and PARTIAL_AGREEMENT <= agree_rate < PASS_AGREEMENT),
    }
    return {
        "n_items": len(ids),
        "arm_a_valid": 30 - infra_a - sum(1 for r in rows_a if r["supports"] and not r["parse_ok"]),
        "arm_b_infra_fails": infra_b,
        "agreement_raw": agree,
        "pairable": pairable,
        "agreement_rate": round(agree_rate, 4),
        "kappa_arm_a_vs_b": round(kappa([x or "?" for x in va], [x or "?" for x in vb]), 4),
        "arm_a_vs_prior": f"{ma}/30 ({100.0 * ma / 30:.1f}%)",
        "arm_b_vs_prior": f"{mb}/30 ({100.0 * mb / 30:.1f}%)",
        "arm_b_margin_mean": round(statistics.fmean(marg_ok), 4) if marg_ok else None,
        "arm_b_margin_min": round(min(marg_ok), 4) if marg_ok else None,
        "arm_a_latency_mean_s": round(statistics.fmean(
            [r["latency_s"] for r in rows_a if r["error"] is None]), 3) if rows_a else None,
        "arm_b_latency_mean_s": round(statistics.fmean(
            [r["latency_s"] for r in rows_b if r["error"] is None]), 3) if rows_b else None,
        "escalations": escal,
        "verdict": verdict,
    }


# --------------------------------------------------------------------- mock
class _MockClassify(BaseHTTPRequestHandler):
    def log_message(self, *a):  # silence
        pass

    def do_POST(self):  # noqa: N802
        ln = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(ln) or b"{}")
        texts = body.get("text", [])
        # deterministic pseudo-model: label flips on the premise's middle byte,
        # with three distinct confidence regimes so margins/kappa are exercised.
        outs = []
        for t in texts:
            h = sum(t.encode("utf-8"))
            if h % 3 == 0:
                z = [0.2, 2.2, 0.1]     # confident yes
            elif h % 3 == 1:
                z = [2.2, 0.2, 0.1]     # confident no
            else:
                z = [0.9, 1.0, 0.8]     # near-threshold
            outs.append({"embedding": z})
        resp = json.dumps(outs).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(resp)))
        self.end_headers()
        self.wfile.write(resp)


def mock_arm_a(_system: str, user: str, max_tokens: int = 1536) -> str:
    h = sum(user.encode("utf-8"))
    if h % 3 == 0:
        sup, conf = "yes", 0.9
    elif h % 3 == 1:
        sup, conf = "no", 0.9
    else:
        sup, conf = ("yes", 0.55) if h % 2 else ("no", 0.55)
    return json.dumps({"supports": sup, "confidence": conf,
                       "reason": "mock arm-a response (selftest, no API call)"})


# --------------------------------------------------------------------- main
def in_night_window() -> bool:
    h = datetime.now().astimezone().hour
    return h >= 23 or h < 9


def main() -> int:
    sys.path.insert(0, str(ROOT))  # repo root: mag/ becomes importable
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=["a", "b", "both"], default="both")
    ap.add_argument("--arm-b-url", default="http://127.0.0.1:30000",
                    help="base URL of the SGLang openjev server (serve_sglang.sh)")
    ap.add_argument("--selftest", action="store_true",
                    help="mock both arms end to end: zero network, zero inference")
    ap.add_argument("--force", action="store_true",
                    help="run outside the 23:00-09:00 family-box window (receipted)")
    args = ap.parse_args()

    items = load_frozen()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir = RESULTS_DIR / ("selftest" if args.selftest else stamp)
    outdir.mkdir(parents=True, exist_ok=True)

    if args.selftest:
        import threading
        srv = HTTPServer(("127.0.0.1", 0), _MockClassify)
        port = srv.server_address[1]
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        base_url = f"http://127.0.0.1:{port}"
        rows_a = run_arm_a_mock(items)
        rows_b = run_arm_b(items, base_url)
        srv.shutdown()
    else:
        if ("b" in args.arms) and not in_night_window() and not args.force:
            print("REFUSED: outside the 23:00-09:00 family-box night window and "
                  "--force not given. Arm B serves the local GPU lane; arm A may "
                  "be run alone with --arms a. Receipted, nothing scored.",
                  flush=True)
            (outdir / "receipt.md").write_text(
                f"# openjev A/B - refused at {stamp}\n\n"
                "Outside the family-box night window; --force not given. "
                "No inference was run.\n", encoding="utf-8")
            return 4
        rows_a = run_arm_a(items) if "a" in args.arms else []
        rows_b = (run_arm_b(items, args.arm_b_url)
                  if "b" in args.arms else [])

    with (outdir / "rows.jsonl").open("w", encoding="utf-8", newline="\n") as f:
        for r in rows_a + rows_b:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    summary = summarize(items, rows_a, rows_b)
    summary["run"] = {"selftest": args.selftest, "arms": args.arms,
                      "frozen_set_sha256": SET_SHA256_EXPECTED, "ts": stamp}
    (outdir / "summary.json").write_text(
        json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
    lines = [
        "# openjev A/B receipt", "",
        f"- run: {'SELFTEST (mock arms, zero inference)' if args.selftest else stamp}",
        f"- frozen set: {FROZEN.name} (sha256 {SET_SHA256_EXPECTED[:16]}.., verified)",
        f"- arms scored: {summary['pairable']} pairable of {summary['n_items']} items",
        f"- agreement A vs B: {summary['agreement_raw']}/{summary['pairable']} "
        f"(kappa {summary['kappa_arm_a_vs_b']})",
        f"- arm A vs prior tier-1: {summary['arm_a_vs_prior']}; "
        f"arm B vs prior tier-1: {summary['arm_b_vs_prior']}",
        f"- arm B infra fails: {summary['arm_b_infra_fails']}",
        f"- escalations: {len(summary['escalations'])} items "
        "(disagreements, low confidence, low margin, infra)",
        f"- verdict: adopt_candidate={summary['verdict']['adopt_candidate']} "
        f"meter_only={summary['verdict']['meter_only']} "
        "(bars pre-registered in OPENJEV_AB_PROTOCOL_20260925.md section 6)", "",
        "Escalation queue (operator adjudication at the fold gate):",
    ]
    for e in summary["escalations"]:
        lines.append(f"- {e['item_id']}: {', '.join(e['why'])} "
                     f"(a={e['arm_a']} b={e['arm_b']} prior={e['prior']})")
    (outdir / "receipt.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=1)[:2000])
    print(f"results: {outdir}")
    return 0


def run_arm_a_mock(items: list[dict]) -> list[dict]:
    """Patch the judge door with the mock responder for the selftest only,
    restoring the real one afterwards. No network, no tokens, no inference."""
    import mag.lane_runner as lr
    real = lr.flash_call
    lr.flash_call = mock_arm_a
    try:
        return run_arm_a(items)
    finally:
        lr.flash_call = real


if __name__ == "__main__":
    raise SystemExit(main())
