# B2-61 close: append the LEDGER row (json.dumps, never heredoc) and self-feed
# briefs to QUEUE.md under Open. Queue numbers are computed from the live file
# max at write time to avoid the concurrent-number race that just double-spent
# B2-194/195/196.
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
LEDGER = os.path.join(REPO, "memory", "burns", "LEDGER.jsonl")
QUEUE = os.path.join(HERE, "QUEUE.md")

ROW = {
    "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "slug": "B2-61-roster-purge",
    "verdict": "LANDED",
    "landing": "watch/inbox/burn_wave_20260926/B2_61_roster_purge_20260926.md",
    "one_line": (
        "providers.yaml roster purge landed config-only on live 2026-09-26 bytes, one "
        "verification call per change before writing (B2_61_verify.py, raw bodies in "
        "B2_61_verify_results.json): openrouter lost the three old :free ids from the "
        "live catalog (GET 200, 458 models, all three absent) and gained chat-verified "
        "cohere/north-mini-code:free (200 'ALIVE'; qwen3.8-27b:free rejected as repoint, "
        "live 429 upstream_provider_shared_pool); nvidia dormantring with the 18-id roster "
        "dropped (default id now 410 'end of life on 2026-09-21T08:00:00Z', B2-04 had 404 "
        "not-found-for-account); gemini dormantring with both ids dropped (2.0-flash 404 "
        "EOL naming gemini-3.8-flash, catalog 61 ids lacks both yaml ids, native 401 "
        "UNAUTHENTICATED; B2-63's concurrent auth comment preserved verbatim); mistral "
        "dormantring with default repointed to mistral-small-latest (mistral-large-latest "
        "403 tier_not_allowed code 1910 and catalog-absent, small-latest 429 "
        "x-ratelimit-limit-req-minute 0 code 1300 reproducing B2-04); nvidia/mistral/"
        "gemini pulled from prefer_order and all five routing lists because pick_provider "
        "(models/quota.py:382-397) never reads dormant; validation green: yaml.safe_load + "
        "estate load_providers 28 providers, doctor check_provider_endpoints shows all "
        "four DORMANT none(dormant), only alarm the pre-existing mlx stub; fact filed: "
        ".env spells the mistral key Mistral_API_KEY (mixed case), resolves only via "
        "Windows case-insensitive lookup; self-feeds B2-200/201/202"
    ),
}

BRIEFS = [
    (
        "B2-200 openrouter :free rotation build-out: 17 :free ids are live in today's "
        "catalog (B2_61_verify_results.json openrouter_catalog.free_ids) but only "
        "cohere/north-mini-code:free is chat-verified; qwen3.8-27b:free proved "
        "catalog-presence is not liveness (429 upstream shared pool); build a "
        "verify-then-add rotation where each candidate id earns its providers.yaml line "
        "with one live chat gate first; pointers configs/providers.yaml openrouter block "
        "+ watch/inbox/burn_wave_20260926/B2_61_verify_results.json."
    ),
    (
        "B2-201 mistral key-name case mismatch: .env spells it Mistral_API_KEY / "
        "Mistral_API_KEY_2 (mixed case, names only verified) while providers.yaml names "
        "MISTRAL_API_KEY, so the lane resolves only through Windows case-insensitive env "
        "lookup and would silently lose its key under WSL/docker; normalize the .env "
        "spelling or case-normalize in models/env_load.py, add a regression test; "
        "falsifier = an exact-case lookup run under WSL finds no mistral key; pointers "
        "models/env_load.py + configs/providers.yaml mistral block comment (B2-61)."
    ),
    (
        "B2-202 dormant-skip seam in pick_provider: models/quota.py:382-397 checks "
        "tier, key and budget but never the dormant flag, so any dormant lane with a "
        "key (cerebras, nvidia, gemini, mistral, saelis today) stays pickable and the "
        "only enforcement is hand-edited routing lists; add a dormant skip in the "
        "candidate loop with those five as fixtures plus a test; falsifier = "
        "pick_provider('default') returns a dormant provider when someone re-adds it to "
        "a routing list; pointers models/quota.py + mag/doctor.py:488-500."
    ),
]


def main():
    with open(LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps(ROW, ensure_ascii=False) + "\n")
    print("LEDGER row appended")

    with open(QUEUE, encoding="utf-8", errors="replace") as f:
        q = f.read()
    nums = [int(m) for m in re.findall(r"B2-(\d+)", q)]
    start = max(nums) + 1
    lines = [""] + [
        "- [ ] B2-%d %s" % (start + i, brief) for i, brief in enumerate(BRIEFS)
    ]
    if not q.endswith("\n"):
        lines.insert(0, "")
        lines.remove("")
    with open(QUEUE, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("QUEUE self-feed appended: B2-%d..B2-%d" % (start, start + len(BRIEFS) - 1))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
