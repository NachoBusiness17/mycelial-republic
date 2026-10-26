"""W4 fire: ONE deliberate ask to anthropic/claude-opus-5.5 on Nous (2026-09-30).

Mission: fire the AMENDED ask (Amendment 1 inverted shape: spec deltas + eval
contract + adversarial critique, NOT the build-ask), constructed per Amendment 2
(XML-tagged, context-first, ask-last, effort max requested, hostile second pass,
verbosity contract) with Amendment 3's adopted contract lines binding, and
BASELINE_SPEC.md pasted verbatim as the baseline to beat.

Driver pattern: hermes_gopher_burn_20260929.py (Nous inference API, OpenAI
compatible). Call shape per LESSIG RAILS lesson: max_tokens 16000, reasoning
{"max_tokens": 6000} so the answer body actually gets written.

Budget: $2.00 ABSOLUTE mission cap. Worst case at catalog rates ($4/$20 per M):
~7k input + 16k output = ~$0.35. ONE call, no retry, no model rotation; an error
is reported honestly per mission.

Laws: no em-dashes in anything this file writes (asserted on the prompt);
results land next to the W4 receipt in watch/inbox/last_mile_20260930/.

Usage:
    .venv/Scripts/python.exe watch/inbox/last_mile_20260930/w4_fire_opus.py
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
HERMES_DIR = Path(r"C:\Users\foste\AppData\Local\hermes")
BASE = "https://inference-api.nousresearch.com/v1/chat/completions"
KEY_ENVS = ("NOUS_SDD_API_KEY", "HERMES_API_KEY_1", "HERMES_API_KEY_2")
MODEL = "anthropic/claude-opus-5.5"
MAX_TOKENS = 16000
REASONING_MAX_TOKENS = 6000
TEMPERATURE = 0.4
BUDGET_USD = 2.0
RATE_IN, RATE_OUT = 4.0, 20.0  # per 1M, v9_probe_prices.json catalog_rates_per_M

OUT_DIR = ROOT / "watch" / "inbox" / "last_mile_20260930"
RAW_FILE = OUT_DIR / "W4_OPUS_RETURN_raw.json"
CONTENT_FILE = OUT_DIR / "W4_OPUS_RETURN_20260930.md"
FIRE_LOG = OUT_DIR / "W4_fire_log.txt"

PROMPT_TEMPLATE = """<context>
You are answering a one-shot deliberate ask from a small instrumentation research lab. There are no follow-up questions and no second turn: everything needed is in this brief, and your single return is judged mechanically against pre-registered acceptance gates, not by prose quality.

WHO WE ARE. We run a fleet of cheap local models: a 7B-class assistant, a 2B janitor, and sub-1GB decision models (text to yes/no, choice, or score, with calibrated probabilities), all served behind OpenAI-compatible endpoints we call clones. We hold metered, hard-capped access to frontier models (you are that tier) and mid-tier flash models. 95 percent of our tokens are local; the frontier exists for judgment: design, review, escalation. We trust bytes, not reports. House law: zero em-dashes anywhere in your output; our pipeline rejects any return containing one (verifiable gate).

WHAT WE ALREADY DID. We did not hand you a blank page. Our own multi-seat panel (three blind seats plus a judge plus a synthesis) produced the capability-ledger baseline spec embedded below, and a hostile implementer night-read already patched it (its amendments 1 to 4 are part of the baseline text). Our delegation research concluded that routing and gateway plumbing is commodity (LiteLLM and KServe class software implements most of it) and that frontier tokens belong at judgment points, not in re-deriving plumbing. This ask is therefore INVERTED: you do not build anything and you do not write commodity code. You judge, tighten, and attack.

EFFORT. We explicitly request maximum effort (the xhigh tier, not the default medium). We accept the verbosity cost; the output contract below caps it.
</context>

<baseline>
The estate baseline, verbatim. This is the document your return is diffed against.

__BASELINE__

</baseline>

<output_contract>
- No preamble, no praise, no restatement of this brief. Start directly with section A.
- Tables over prose wherever a table can carry the content.
- Section cap: no section longer than roughly 600 words; total return under roughly 9000 words.
- Zero em-dashes in any line.
- Cite the baseline by section number for every claim you make about it.
- Mark anything you cannot source or verify as UNPROVEN. Do not invent citations.
</output_contract>

<acceptance_tests>
Your return is gated by these falsifiable checks; the estate runs them mechanically:
1. DIFF CONTRACT. Every claimed improvement maps to at least one clause of baseline section 10: (1) tighten a gate-class definition or evidence minimum without unfalsifiable ceremony; (2) replace a DESIGN DEFAULT with a measured constant from a runnable check, or argue a better prior with named evidence; (3) find a falsifier not in baseline section 8 plus a defense that survives its own stated residual; (4) simplify (delete a field, trigger, or table) at equal auditable power; (5) repair a named blind spot beyond fixes already incorporated. Improvements outside these clauses are noise by our law.
2. HOSTILITY. Your adversarial section contains at least three concrete production-failure attacks; each names the baseline section it hits, the failure mode, and the cheapest defense.
3. TEST PREDICATES. Every proposed change that touches the buildable surface ships with at least one named test predicate (test_ function shape, asserted behavior, negative case included).
4. SELF-DOUBT. You flag at least one instruction in this brief you believe is wrong, with reasoning; a bare "all fine" fails this gate. Honesty is the deliverable; disagreement is welcome and expected.
5. NO NEW CEREMONY. No proposed addition may be unfalsifiable, and none may introduce unmeasured cleverness (baseline 4.2 defers bandits for exactly this reason; an unmeasured bandit proposal fails here).
</acceptance_tests>

<the_ask>
Deliver markdown sections A through G, in order:

A. VERDICT ON THE BASELINE. One table: each numbered baseline section, verdict KEEP or TIGHTEN or KILL, one-line reason. Then one short paragraph: where is this baseline actually weak against what a production fleet needs?

B. SPEC DELTAS. The concrete changes that beat the baseline under its own section 10 diff contract. Per delta: what changes, which baseline section, which diff-contract clause (1 to 5) it satisfies, why it is better and not merely different. At least three deltas, or an explicit honest verdict that the baseline is near-optimal for its scope (that verdict is acceptable and useful to us; do not manufacture deltas to fill the section).

C. ESCALATION DECISION BOUNDARIES. Baseline 4.3 defines triggers T1 to T4. Defend or replace each boundary in one line each, with the decision arithmetic spelled out for any replacement. Address the T2 advisory problem directly: what measurement makes C_rework real, and what is the cheapest harness that produces it.

D. HOSTILE SECOND PASS. Attack this whole design as a hostile implementer who must make it fail in production. Do not validate our framing; disagreement is the deliverable. At least three attacks (acceptance gate 2), each with the section hit, the production failure, and the cheapest defense. Then attack your own sections B and C: where would your own deltas break first?

E. MISSING TEST PREDICATES. Baseline amendment 4 lists five first-wave predicates. List any predicate missing from that set that a first build wave should run before routing authority is granted; table form. If none, argue why the five suffice.

F. INSTRUCTIONS YOU BELIEVE ARE WRONG. Any instruction, constraint, number, or framing in this brief or in the baseline's own laws that you believe is factually wrong, counterproductive, or biased, with reasoning (acceptance gate 4). If none, defend the two you were most tempted to flag.

G. WHAT THIS RETURN DELIBERATELY DOES NOT DO. Scope honesty: what you refuse to attempt here and why. We respect refusal lists more than feature lists.
</the_ask>"""


def load_dotenv(path: Path) -> None:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    load_dotenv(HERMES_DIR / ".env")
    keys = [k for k in (os.environ.get(e) for e in KEY_ENVS) if k]
    if not keys:
        FIRE_LOG.write_text("NO KEYS - aborted without spend\n", encoding="utf-8")
        print("NO KEYS - aborting without spend")
        return 2

    baseline = (ROOT / "watch" / "inbox" / "gps_baseline_ractor_20260929" / "BASELINE_SPEC.md").read_text(
        encoding="utf-8"
    )
    prompt = PROMPT_TEMPLATE.replace("__BASELINE__", baseline)
    assert "\u2014" not in prompt, "em-dash law violated in fired prompt"
    prompt_bytes = len(prompt.encode("utf-8"))
    est_in_tokens = prompt_bytes // 4
    worst_case = est_in_tokens / 1e6 * RATE_IN + MAX_TOKENS / 1e6 * RATE_OUT
    if worst_case > BUDGET_USD:
        FIRE_LOG.write_text(
            f"BUDGET GUARD: worst case ${worst_case:.4f} exceeds cap ${BUDGET_USD}\n", encoding="utf-8"
        )
        print(f"BUDGET GUARD hit, worst case ${worst_case:.4f}; aborting without spend")
        return 3

    body = json.dumps(
        {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
            "reasoning": {"max_tokens": REASONING_MAX_TOKENS},
        }
    ).encode()
    req = urllib.request.Request(
        BASE, data=body, headers={"Authorization": "Bearer " + keys[0], "Content-Type": "application/json"}
    )

    t0 = time.time()
    status = "ok"
    resp = {}
    try:
        with urllib.request.urlopen(req, timeout=1200) as r:
            resp = json.load(r)
    except urllib.error.HTTPError as e:
        status = f"http_{e.code}"
        try:
            resp = {"error_body": e.read().decode("utf-8", "replace")[:4000]}
        except Exception:  # noqa: BLE001
            resp = {"error_body": "unreadable"}
    except Exception as e:  # noqa: BLE001
        status = f"error_{type(e).__name__}"
        resp = {"error_body": str(e)[:4000]}
    secs = round(time.time() - t0, 1)

    usage = resp.get("usage", {}) if isinstance(resp, dict) else {}
    metered = usage.get("cost") if isinstance(usage, dict) else None
    predicted = None
    if isinstance(usage, dict) and usage.get("completion_tokens") is not None:
        predicted = (
            usage.get("prompt_tokens", 0) / 1e6 * RATE_IN
            + usage.get("completion_tokens", 0) / 1e6 * RATE_OUT
        )
    cost_usd = float(metered) if metered is not None else (predicted if predicted is not None else 0.0)

    content = None
    reasoning_tail = None
    finish = None
    if status == "ok":
        msg = resp["choices"][0]["message"]
        content = msg.get("content")
        reasoning_tail = (msg.get("reasoning") or "")[-600:]
        finish = resp["choices"][0].get("finish_reason")

    row = {
        "id": "W4-opus-deliberate-ask",
        "model": MODEL,
        "status": status,
        "usage": usage,
        "cost_usd": round(cost_usd, 6),
        "predicted_cost_usd": round(predicted, 6) if predicted is not None else None,
        "prompt_bytes": prompt_bytes,
        "est_prompt_tokens": est_in_tokens,
        "seconds": secs,
        "finish_reason": finish,
        "content": content,
        "reasoning_tail": reasoning_tail,
    }
    RAW_FILE.write_text(json.dumps(row, indent=2, ensure_ascii=False), encoding="utf-8")

    if content:
        head = (
            "# W4 OPUS RETURN: anthropic/claude-opus-5.5 (Nous), 2026-09-30\n\n"
            f"Status: {status}. Metered cost: ${cost_usd:.4f}. Seconds: {secs}. "
            f"Usage: {json.dumps(usage)}. Finish: {finish}.\n"
            "Full return below, verbatim. Em-dash count in return body: "
            f"{(content or '').count(chr(8212))}.\n\n---\n\n"
        )
        CONTENT_FILE.write_text(head + content, encoding="utf-8")

    log = (
        f"status={status} secs={secs} cost=${cost_usd:.4f} usage={json.dumps(usage)} "
        f"prompt_bytes={prompt_bytes} finish={finish} content_chars={len(content) if content else 0}\n"
    )
    with open(FIRE_LOG, "a", encoding="utf-8") as f:
        f.write(log)
    print(log)
    return 0 if status == "ok" else 1


if __name__ == "__main__":
    sys_exit = main()
    raise SystemExit(sys_exit)
