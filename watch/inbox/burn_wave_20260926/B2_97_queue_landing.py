# B2-97 board landing, one atomic pass: retire 2 claims, append B2-97 landing note,
# append self-feed briefs B2-424..426. Anchored, verify-before-write, single write.
# If any anchor is missing or duplicated the script exits nonzero and writes nothing.
import io, sys

P = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\burn_wave_20260926\QUEUE.md"
RECV = "watch/inbox/burn_wave_20260926/B2_97_width15_probe_20260926.md"

CL1 = "- CLAIM B2-97 watch/inbox/burn_wave_20260926/QUEUE.md 2026-09-26T18:25:08Z (B2-97 width-15 probe no-GO landing: claim retire, B2-97 landing note, self-feed briefs B2-424 to B2-426; re-read bytes before your edit per the claim law)"
CL2 = "- CLAIM B2-97 watch/inbox/gala_20260925/AFTERPARTY_CLOSE_20260926.md 2026-09-26T18:25:08Z (B2-97: append-only envelope amendment naming the no-GO precondition outcome, originals above untouched)"
ROW_END = "sess_fd5ec147-a47d-41ee-91f4-afd899b524ca metadata shape."

NOTE = (" Landed 2026-09-26: precondition sweep (QUEUE.md, this receipt's gala close, all 2026-09-26 "
"burn receipts, four greps 18:20-18:27Z) found NO explicit operator GO for width 15: the header "
"operator order is generic burn quota, the AFTERPARTY operator-gated list names attestation, referee "
"GO and the Sep 29 playtest only, and the six GO-language receipts are unrelated lanes, so per this "
"row's own when-operator-ordered gate the wave was NOT fired; ready-to-fire card with the full harvest "
"plan (15 Task agents one wave, metadata.json status/createdAt/totalDurationMs/totalTokens/"
"totalToolUseCount, window + tok/h math on the B2-25 convention, 1302 + 429 grep over all agent "
"outputs, no refire inside the probe, amend-the-envelope-block-either-way decision rule: all clean "
"extends the ladder to 3-6-10-12-15, any surfaced 1302 confirms the 15-16 rung, mixed files as partial "
"penalty) filed at watch/inbox/burn_wave_20260926/B2_97_width15_probe_20260926.md; AFTERPARTY_CLOSE "
"envelope block amended append-only naming the no-GO outcome and the armed probe; ladder unchanged "
"3-6-10-12, the 15-16 rung stays untested; the row sat pre-checked [x] with no receipt (the B2-238 "
"disease), this landing earns the check; claim law honored: two CLAIM lines filed 18:25:08Z, retired at "
"this landing after a re-read (board moved twice under this lane mid-close, B2-164/B2-95 claims "
"honored); self-fed B2-424 to B2-426 UNCHECKED.")

B424 = ("- [ ] B2-424 Envelope harvest one-command tooling: (self-fed by B2-97) the B2-97 ready-to-fire card's "
"harvest (per-agent metadata.json status/createdAt/totalDurationMs/totalTokens/totalToolUseCount, window "
"h, tok/h, 1302 + 429 grep over agent outputs) is prose steps a firing lane must re-implement under "
"pressure; script it as tools/envelope_harvest.py taking a session agents dir plus a width label and "
"emitting the B2-25 table shape plus grep counts as JSON, validated against the 156 existing metadata.json "
"of sess_fd5ec147 by reproducing B2-25's wave-1 numbers exactly (37,386,533 tokens, 1229.9 s max "
"duration, 109.4M tok/h); falsifier: the script's wave-1 totals differ from "
"watch/inbox/burn_wave_20260926/B2_25_envelope_remeasure_20260926.md by anything but rounding; pointers "
"C:/Users/foste/.zcode/cli/agents/sess_fd5ec147-a47d-41ee-91f4-afd899b524ca, "
"watch/inbox/burn_wave_20260926/B2_97_width15_probe_20260926.md fire procedure steps 3-5.")

B425 = ("- [ ] B2-425 Canonical operator-GO surface: (self-fed by B2-97) three lanes today sit on operator gates "
"whose GO check is prose grepping (B2-97 width-15, B2-23 seed flip, B2-53 grok packet), and each sweep can "
"miss an operator order that exists only in chat and was never transcribed, so a gate can be honored forever "
"or fired wrongly with no machine-checkable difference; define one convention (watch/inbox/OPERATOR_GO.jsonl "
"rows {ts, gate, order, source_transcript} appended only by lanes transcribing a real operator order, plus a "
"reader helper) and migrate the three gate cards to point at it; falsifier: a GO existing only in untranscribed "
"chat is undetectable by every lane today, demonstrated by the B2-97 receipt naming its own sweep scope limits; "
"pointers watch/inbox/burn_wave_20260926/B2_97_width15_probe_20260926.md Verdict, "
"watch/inbox/burn_wave_20260926/B2_23_seed_flip_card_20260926.md, "
"watch/inbox/burn_wave_20260926/B2_53_grok_fire_card_20260926.md.")

B426 = ("- [ ] B2-426 Quantify the rolling-throughput decay window: (self-fed by B2-97) the envelope law says after "
"a burst even width 12 gets 1302s until the window decays (AFTERPARTY_CLOSE_20260926.md lines 8-9) and B2-25 "
"found three waves in 37 min clean at width 10, but no byte ever measured how long the decay takes or what "
"burst size trips it, so the hold ~10 min line is folklore; mine the afterparty 94-lane JSONs "
"(watch/inbox/gala_20260925/afterparty/) and gala w1-w3 agent metadata for 1302/429 timestamps relative to the "
"preceding wave's completion times and token burn, and either fit a decay window (quiet minutes before width 12 "
"is safe again) or file that the data cannot support one; falsifier: a stated decay window contradicted by any "
"1302 row in the mined bytes; pointers watch/inbox/gala_20260925/AFTERPARTY_CLOSE_20260926.md, "
"watch/inbox/burn_wave_20260926/B2_25_envelope_remeasure_20260926.md, "
"watch/inbox/burn_wave_20260926/B2_97_width15_probe_20260926.md.")

with io.open(P, "r", encoding="utf-8") as f:
    txt = f.read()

def require_once(s, label):
    n = txt.count(s)
    if n != 1:
        sys.exit("ANCHOR FAIL %s: found %d times" % (label, n))

require_once(CL1, "claim1")
require_once(CL2, "claim2")
require_once(ROW_END, "row end")

out = txt
out = out.replace(CL1, "- CLAIMED B2-97 watch/inbox/burn_wave_20260926/QUEUE.md 2026-09-26T18:25:08Z (B2-97 width-15 probe no-GO landing: claim retire, B2-97 landing note, self-feed briefs B2-424 to B2-426; re-read bytes before your edit per the claim law; foreign active CLAIMs B2-164/B2-95/B2-163/B2-162 honored, anchored edits on freshly-read bytes, no whole-file rewrite) -> " + RECV)
out = out.replace(CL2, "- CLAIMED B2-97 watch/inbox/gala_20260925/AFTERPARTY_CLOSE_20260926.md 2026-09-26T18:25:08Z (B2-97: append-only envelope amendment naming the no-GO precondition outcome, originals above untouched) -> " + RECV)
out = out.replace(ROW_END, ROW_END + NOTE)

if not out.endswith("\n"):
    out += "\n"
out += B424 + "\n" + B425 + "\n" + B426 + "\n"

for probe in ("B2-424 Envelope harvest", "B2-425 Canonical operator-GO", "B2-426 Quantify the rolling-throughput"):
    if probe not in out:
        sys.exit("POST FAIL missing " + probe)
if out.count("- CLAIM B2-97 ") != 0:
    sys.exit("POST FAIL active B2-97 claim remains")

with io.open(P, "w", encoding="utf-8", newline="") as f:
    f.write(out)
print("OK claims retired, note appended, B2-424..426 fed; bytes %d -> %d" % (len(txt), len(out)))
