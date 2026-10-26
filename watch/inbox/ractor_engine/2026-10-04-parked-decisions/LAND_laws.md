# LAND_laws - law-amendments lane receipt (ractor rank-3 verdict, D3 surfaces)

Landed 2026-10-04. Source carrier:
watch/inbox/ractor_engine/2026-10-04-parked-decisions/SYNTHESIS.md (read
first, as ordered). Laws held: repo venv only, no em-dashes, bytes before
prose, no git commit, blocked sub-items filed not fabricated.

## Files touched (per-file diff summary)

1. watch/inbox/model_garden/PRIORS.md (task path "queue/PRIORS.md" does not
   exist; the SYNTHESIS names this path, row 8 sits at line 25):
   - Row 8 Status cell appended (original text intact):
     " + POST-DATUM 2026-10-04 amendment banked below the table
     (parked-decision D3, carrier-enforced)".
   - New section after the table, before section B: "### Row 8 POST-DATUM
     amendment ..." carrying the SYNTHESIS:99-117 merged carrier text
     VERBATIM (byte-diffed: `diff` of the stripped block vs the landed
     block returns empty, VERBATIM MATCH) plus a land-note whose line cites
     are sed-verified at landing (see verification log; the verbatim text's
     own :204/:238-249 cites are SYNTHESIS-moment lines, kept unmodified).
   - Closes the D3 row per the verdict: thinking posture settled by the d4
     measurement + the 5-3 hostile pass.

2. queue/STANDING_RAILS.md:
   - Law 1 gained the depth clause (indented continuation, numbering
     intact): two-value depth enum {mechanical, design} + refused
     otherwise, carrier-sent thinking:{type:disabled} on mechanical
     (omission is not the off state), design as the only enabled path
     (capability-attested, 32K+ budgets), and response-side auditability
     (depth + thinking_sent + reasoning_tokens banked). Cites
     mag/route_chat.py (function-anchored: route_chat ValueError,
     wire_thinking, the bank row) and
     watch/inbox/go_wave_20261004/d4_thinking_probe.md. Function anchors
     chosen over line numbers because the module was moving under this
     edit (wire sitting active).
   - One registered-debt bullet appended at the end of REGISTERED DEBTS
     (after the 39/39 Delta Register bullet; that bullet and the self-call
     bullet above it are byte-untouched): the hermes_burn thinking-rail
     debt, naming the one-hop drop (plan_call computed thinking_control,
     the request carried only {model, messages, max_tokens}), the $0.464
     double-burn carrier (usage.jsonl:1151-1152), the wire merge that
     landed 2026-10-04, and migration to route_chat per the self-call debt
     as the standing cure.
   - Lines 49-50 (39/39 delta) NOT modified, per order. AGENTS.md census
     bullet untouched (not in ownership).

3. watch/inbox/go_wave_20261004/ds_workhorse.md:
   - Item 6 gained the ERRATUM immediately under its heading, VERBATIM from
     SYNTHESIS:139-147 with the corrected tools/ds_workhorse.py:64 cite
     (byte-diffed: VERBATIM MATCH), plus a provenance line naming the
     NIGHT_CLOSE pattern. The original item 6 text (the "uncapped,
     thinking-off, file-backed" run block) sits below the correction,
     unmodified, as ordered.

4. corpus/steal/MASTER_MICKEY17_V2.md: NOT TOUCHED. Blocker B1 below: the
   ordered ":29 cite in the accuracy row" does not exist in that file.

## Verification log (commands run this sitting, repo venv / sed)

- `sed -n '25,32p' tools/ds_workhorse.py` + `grep -n MODEL tools/ds_workhorse.py`
  -> `MODEL = "deepseek-chat"` is at tools/ds_workhorse.py:64; :29 is
  docstring prose (the hollow-batch fix comment region). The accuracy.md
  :29 cite is wrong, :64 is right, as the verdict said.
- `sed -n '90,96p' tools/ds_workhorse.py` -> explicit
  `"thinking": {"type": "disabled"}` at tools/ds_workhorse.py:93.
- venv read of memory/runs/hermes_burn/usage.jsonl lines 1151-1152 ->
  glm-5.3-prime ct 16000 rt 15998 cost 0.2502604 / ct 14759 rt 9826 cost
  0.2137336; sum 0.4639940 (the $0.464 double burn, as banked).
- `grep -n disable_thinking configs/providers.yaml` -> :223, :371, :401;
  `sed -n '217,225p'` -> the openrouter/auto ignores-disabled-key note at
  :219-223.
- mag/route_chat.py (read twice; the module MOVED between reads, the wire
  sitting is landing code in the same window): at landing moment
  `grep -n` gives DESIGN_MIN_TOKENS 32000 at :131, def wire_thinking at
  :134 (mechanical unconditional disabled; design gated on capability
  attestation + DESIGN_MIN_TOKENS), depth enum ValueError at :193-196,
  wire_thinking wired at :266, bank row with depth/thinking_sent/
  reasoning_tokens at :308-310. The carrier-enforced wire and the
  closed-loop bank the verdict demands are LIVE in code as of this
  sitting.
- tools/hermes_burn.py: the one-hop drop the verdict names is already
  FIXED by the wire sitting: `_build_body` at :106-118 merges the plan
  (extra_body), `_call` passes plan.extra_body at :356-358 via plan_call.
  The debt line therefore records defect + landed fix + migration cure,
  never a live false claim.
- `sed -n '44,53p' queue/STANDING_RAILS.md` -> self-call bullet at :46-48
  and the 39/39 bullet at :49-53, both left byte-identical.
- accuracy.md:99 and accuracy.md:64 (ractor lens receipt) -> the wrong
  tools/ds_workhorse.py:29 cite lives ONLY there and in
  break-accuracy.md:77.
- Verbatim proof: `diff` of SYNTHESIS:99-117 (blockquote markers
  stripped) vs the landed PRIORS block -> empty; same for
  SYNTHESIS:139-147 vs the landed ERRATUM -> empty. Both printed VERBATIM
  MATCH.
- Em-dash scan over all three written files: `grep -c` -> 0 occurrences.

## Blockers (filed, not fabricated)

- B1: "fix the WRONG :29 cite in corpus/steal/MASTER_MICKEY17_V2.md
  accuracy row" - NOT FOUND, so not done. Repo-wide grep for
  ds_workhorse.py:29 hits only the ractor lens receipts (accuracy.md:64,
  accuracy.md:99, break-accuracy.md:77); MASTER_MICKEY17_V2.md (237 lines)
  contains zero occurrences of "accuracy" and zero ".py:29" cites (its
  nearest rows, D3/D4 at :166-178, cite PRIORS.md:25 and
  tools/ds_workhorse.py:55-56 - different claims, lane-moment
  attributions, outside this order). The corrected :64 erratum is landed
  where accuracy.md itself aimed it: ds_workhorse.md item 6. Fixing the
  lens receipts' :29 (accuracy.md, break-accuracy.md) is owed to whoever
  owns the fold receipts; break-logic.md:110 already flags the error.
- B2: task path "queue/PRIORS.md" does not exist; the real file is
  watch/inbox/model_garden/PRIORS.md (SYNTHESIS names it). Landed there.
- B3: mag/route_chat.py changed under this sitting (wire sitting active):
  the SYNTHESIS-moment cites inside the verbatim amendment (:204,
  :238-249) no longer name those lines on today's tree. Kept verbatim per
  the order; the land-note in PRIORS carries the sed-verified
  landing-moment lines.
- B4: not done by order: code changes (tests/test_route_chat_depth.py
  pins, inference_budget), any commit, any touch of STANDING_RAILS 39/39
  lines or the AGENTS.md census bullet.

Law-amendments lane, 2026-10-04. No spend: desk edits only.
