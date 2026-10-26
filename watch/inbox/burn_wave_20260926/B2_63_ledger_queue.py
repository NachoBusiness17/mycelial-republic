# B2-63 ledger append + self-feed appender. Run with .venv/Scripts/python.exe.
# json.dumps only, no heredoc, per the lane contract.
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

ROW = {
    "ts": "2026-09-26T00:00:00Z",
    "slug": "B2-63-gemini-auth-shape",
    "verdict": "LANDED",
    "landing": "watch/inbox/burn_wave_20260926/B2_63_gemini_auth_20260926.md",
    "one_line": (
        "gemini auth shape identified byte-level: the AQ.Ab8... key is a Vertex "
        "express-mode key, permanently 401 on generativelanguage in every carriage "
        "(B2_04_probe_results2.json gemini_native_diag, call carried both Bearer and "
        "x-goog-api-key), but it AUTHENTICATES on the native aiplatform endpoint via "
        "x-goog-api-key header and ?key= param, answering 403 PERMISSION_DENIED 'Agent "
        "Platform API has not been used in project 1055073037365 or it is disabled' "
        "(B2_63_vertex_probe_results.json, 2 minimal calls, 0 tokens); GO card filed: "
        "operator enables aiplatform on that project + mag grows a native gemini lane "
        "kind (doctor.py:383 speaks openai_compat only), or mints an AI Studio AIza key "
        "which plugs into the existing lane unchanged; providers.yaml gemini lane "
        "annotated with the dated verdict, no behavior change; self-feeds B2-194/195/196"
    ),
}


def main():
    row = dict(ROW)
    row["ts"] = __import__("datetime").datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    path = os.path.join(REPO, "memory", "burns", "LEDGER.jsonl")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print("LEDGER row appended:", row["ts"], row["slug"])

    queue = os.path.join(HERE, "QUEUE.md")
    briefs = [
        "- [ ] B2-194 Native gemini lane kind for the express key: once the operator enables aiplatform.googleapis.com on project 1055073037365 (GO card in B2-63 receipt), add kind gemini_native to mag speaking POST aiplatform/v1/publishers/google/models/{model}:generateContent with x-goog-api-key, keep openai_compat lanes untouched, doctor deep-probe support per kind; falsifier = 200 with candidates[0].content from B2_63_vertex_probe.py rerun; pointers watch/inbox/burn_wave_20260926/B2_63_gemini_auth_20260926.md + mag/doctor.py:383.",
        "- [ ] B2-195 Express-mode quota lane block: if the aiplatform enable lands, write the measured express quotas into providers.yaml gemini quota (docs table says Gemini models max 10 requests/min inside a 90-day free window whose start date is unknown from here) and record the first-200 timestamp as the observable clock anchor; pointers watch/inbox/burn_wave_20260926/B2_63_gemini_auth_20260926.md + docs.cloud.google.com express-mode overview.",
        "- [ ] B2-196 keys.json gemini role truth: configs/keys.json gemini_1/google_1 say role legacy + status active for an AQ.* express key that cannot serve the lane it is named for (401 on generativelanguage generation, byte-proven); align role/auth_class fields with the B2-63 verdict (express_vertex vs ai_studio) so the B2-134 keys audit does not re-lie; pointers configs/keys.json gemini_1 + watch/inbox/burn_wave_20260926/B2_63_gemini_auth_20260926.md.",
    ]
    with open(queue, "a", encoding="utf-8") as f:
        for b in briefs:
            f.write(b + "\n")
    print("QUEUE self-feeds appended:", len(briefs))


if __name__ == "__main__":
    main()
