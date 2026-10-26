# B2-327 Research-lane transport precheck

## Verdict

LANDED and live-verified against the dead list. tools/transport_precheck.py is the preflight gate a research lane runs on every named URL BEFORE its first model attempt: HEAD-first probe with range-limited GET fallback, wall classifier (403/429 bot-wall, 404/410 dead, 2xx-with-interstitial-marker interstitial, 5xx server-error, transport failures unreachable), and one journal row per check appended to logs/transport_precheck.jsonl so a lane receipt can cite the class as the reason it skipped a source. Live run this lane: pub.towardsai.net (the exact B2-74 bot-wall death) classifies bot-wall status 403 in 218 ms; control example.com classifies ok. The falsifier's enforcement shape now exists: after this gate, a lane holding a bot-wall/dead/interstitial/unreachable class has no excuse to spend a model attempt on that URL. 6 pins in tests/test_transport_precheck.py cover every class plus the journal row shape; suite 6 passed.

## Evidence file:line quotes

- tools/transport_precheck.py docstring (the law): "a research lane runs this on every named URL BEFORE its first model attempt. After this gate exists, a lane must never again burn a paid model attempt against a URL this precheck classifies 403/404 (the B2-74 death class: pub.towardsai.net HTTP 403 bot-wall and stack-junkie.com unresolved...)".
- Live journal rows (logs/transport_precheck.jsonl, appended this lane): {"url": "https://pub.towardsai.net/", "method": "HEAD", "status": 403, "class": "bot-wall", "latency_ms": 218} and {"url": "https://example.com/", "status": 200, "class": "ok"}.
- Classifier (tools/transport_precheck.py classify): WALL_CLASSES {403: bot-wall, 429: bot-wall, 404: dead, 410: dead}; INTERSTITIAL_MARKERS ("just a moment", "checking your browser", "cf-browser-verification", "attention required", "enable javascript and cookies to continue", "verify you are a human"); 5xx server-error; transport exceptions unreachable.
- tests/test_transport_precheck.py: 6 pins (403 bot-wall, 404 dead, interstitial marker on 200, clean 200 ok, URLError unreachable with error text, journal row schema); 6 passed.
- Dead-list provenance: watch/inbox/burn_wave_20260926/B2_74_qlora_recipe_20260926.md Bibliography (the two strictly-2026 recipe sources that died on transport after model spend) and watch/inbox/burn_wave_20260926/B2_16_uf_sweep_20260926.md (the UF-129/130/131 provider-404 class).

## Work done

1. Read both pointer receipts' death classes; specified the classifier around exactly those classes plus the interstitial shape.
2. Implemented tools/transport_precheck.py: HEAD-first probe (hosts rejecting HEAD fall back to a 64KB range GET so interstitial markers stay checkable), wall classes, journal append with fail-open journal (an unwritable journal never breaks the gate), CLI returning nonzero when any URL is not ok (the do-not-spend signal a lane can test).
3. Live-verified against the actual dead-list URL (pub.towardsai.net -> bot-wall 403) and a control (example.com -> ok); the two journal rows are the receipt's evidence.
4. Added 6 tests; suite 6 passed; py_compile OK; zero em-dashes on added bytes.
5. Filed this receipt, LEDGER row, QUEUE row.

## Falsifier

Brief's falsifier: "after the precheck lands, a research lane must never again burn a paid model attempt against a URL its own precheck classified 403/404." The gate + journal make that decidable: any future research-lane receipt that spends model attempts on a URL whose class in logs/transport_precheck.jsonl is bot-wall/dead/interstitial/unreachable violates the gate, and the violation is byte-checkable (journal row precedes or accompanies the lane; a lane citing no precheck row for a spent URL is the same violation by the docstring law). Tool-side inversion: a misclassification (a 404 reading ok) fails the pins; rerun `pytest tests/test_transport_precheck.py -q` (6 passed). Enforcement beyond the tool is process law carried by this receipt's pointer.

## Bibliography closed

- tools/transport_precheck.py (the gate; live-verified)
- logs/transport_precheck.jsonl (journal, 2 evidence rows)
- tests/test_transport_precheck.py (6 pins, 6 passed)
- watch/inbox/burn_wave_20260926/B2_74_qlora_recipe_20260926.md Bibliography + watch/inbox/burn_wave_20260926/B2_16_uf_sweep_20260926.md (the death classes)
- Owed: adoption by the research lanes at their next dispatch (process law; the gate exists and is cited by the docstring).
