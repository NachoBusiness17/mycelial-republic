# GALA MORNING AFTER - preregistered re-verify wave (T+24h, 2026-09-27)

Law: patience-shaped gaps are invisible to builders; the fixes must be proven to STAY
fixed. This wave is free and local (no plan tokens): run every check, compare to the
recorded expectation, file one receipt to watch/inbox/GALA_MORNING_AFTER_20260927.md.
Any drift = a finding, not a failure of the method.

Run from ESTATE root with .venv/Scripts/python.exe unless noted:

1. Fold gates: bash watch/inbox/gala_20260925/fold_gate.sh watch/inbox/gala_20260925/w1/lanes 6  (expect PASS)
   same for w2 with 10, w3 with 22.
2. LINKS count: gala rows in memory/corpus/LINKS.jsonl with kind=="gala" == 36, zero duplicate srcs.
3. seed: python seed/verify_seal.py  (expect 59/59) + pytest seed/tests/test_seed_laws.py -q (expect 6 pass)
4. ghost: pytest tests/ -k "ghost" -q  (expect 47 pass, 0 fail)
5. verkle: pytest tests/test_verkle_audit.py -q  (expect 5 pass)
6. mag organs: pytest on the five organ test files  (expect 52 pass)
7. ratchet full-scope: tools/violation_ratchet.py check  (expect the a15 snapshot: exit 1 with 9 NEW, or fewer if the closer registered by name; MORE = regression finding)
8. config_seal: tools/config_seal.py verify  (expect PASS if lanes/mag re-sealed at close; providers.yaml FAIL expected until operator attests)
9. mountain_check: bash tools/mountain_check  (expect PASS; afterparty t1a-t2 TypeErrors + candy cap should be in by then)
10. afterparty lanes: count afterparty/lanes/*.json, every one must parse, every check[] evidence file must exist non-zero.
11. supervisn: mag/lane_supervisor.py status (expect 8/8 UP) + schtasks state of MagImproveDaily (expect Ready if t8 ran).
12. FROZEN artifacts unchanged: sha256 of watch/inbox/method_card_exp/BATTERY_HELDOUT.md + GROUND_TRUTH_HELDOUT.md must equal today's values (held-out stays held-out).

Falsifier for the whole gala: if morning-after shows more than 2 drifted checks with no
named cause, the gala's fixes were parades and the receipt says so.
