# B2-37 ledger row + QUEUE self-feed (2026-09-26).
# Laws: json.dumps only, never heredoc; .venv python; no em-dashes.
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
LEDGER = os.path.join(REPO, "memory", "burns", "LEDGER.jsonl")
QUEUE = os.path.join(HERE, "QUEUE.md")

row = {
    "ts": "2026-09-26T08:52:00Z",
    "slug": "B2-37-provider-health-close-20260926",
    "verdict": (
        "closed, no rebuild: watch/inbox/PROVIDER_HEALTH_20260926.md exists "
        "(landed by B2-04, 6140 bytes 07:38) and its scoreboard reproduces from "
        "B2_04_probe_results.json + B2_04_probe_results2.json: all 8 lane token "
        "sums hand-recomputed (489+801+808+822+540+180+1801+1449 = 6890 = the "
        "md's 6586 estate + 304 z_ai alive), dead-lane statuses byte-verified "
        "(cerebras 402 x3 empty, nvidia 410 x3 + 404 function-not-found body, "
        "gemini 401 native API-key mode, mistral 429 limit-req-minute 0), quotes "
        "verified (groq 1776 hallucination results.json:96, cohere count 13 "
        "results.json:916, zai-lite 1305 body results2.json:274); 3 errata named: "
        "md:17 nous cell wrongly says no rate headers exposed (results.json:608-623 "
        "records the full x-ratelimit set 50 req/500k tok, 2100/6M 1h), the "
        "openrouter /key dollars 4.608/0.7377 and the gemini Bearer 401 quote have "
        "no JSON bytes on disk (probe2.py report() drops the /key body; no Bearer "
        "retry scripted), console-only"
    ),
    "landing": "watch/inbox/burn_wave_20260926/B2_37_provider_health_close_20260926.md",
    "one_line": (
        "Receipt verified against probe bytes claim by claim: totals and dead-lane "
        "statuses all match, one scoreboard erratum (nous headers exposed after all) "
        "plus two console-only figures filed onward as B2-127..B2-129"
    ),
}

with open(LEDGER, "a", encoding="utf-8") as f:
    f.write(json.dumps(row, ensure_ascii=False) + "\n")
print("LEDGER appended:", row["slug"])

briefs = [
    "- [ ] B2-127 PROVIDER_HEALTH nous cell erratum: the scoreboard row at "
    "watch/inbox/PROVIDER_HEALTH_20260926.md:17 says \"no rate headers exposed\" but "
    "B2_04_probe_results.json:608-623 records the full nous x-ratelimit set (50 req/min, "
    "500k tok/min, 2100/h, 6M/h); fix the one cell to cite the measured headers and keep "
    "the 0 x 429 sub-claim.",
    "- [ ] B2-128 Persist openrouter /key bodies: B2_04_probe2.py:186-187 fetches /key but "
    "report() (B2_04_probe2.py:96-99) stores only choices content, empty for /key, so the "
    "$4.608 and $0.7377 usage figures in B2_04_provider_health_20260926.md:19-20 have no "
    "JSON bytes on disk; add a body capture for keymeta calls and re-GET both /key endpoints.",
    "- [ ] B2-129 Capture the gemini Bearer 401: PROVIDER_HEALTH_20260926.md:24 quotes 401 "
    "\"invalid authentication credentials\" as Bearer but neither B2_04_probe_results.json "
    "nor B2_04_probe_results2.json holds it (only the native 401 at "
    "B2_04_probe_results2.json:64-74); script the Bearer-mode retry so both auth-mode error "
    "bodies are persisted next run.",
]

with open(QUEUE, "r", encoding="utf-8") as f:
    q = f.read()
if q and not q.endswith("\n"):
    q += "\n"
q += "\n".join(briefs) + "\n"
with open(QUEUE, "w", encoding="utf-8") as f:
    f.write(q)
print("QUEUE appended:", len(briefs), "briefs")
