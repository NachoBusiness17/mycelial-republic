# B2-105 Mistral lane surgery (2026-09-26)

## Verdict

ALREADY-LANDED, VERIFIED, CLOSED. Both arms of the brief were already on disk
when this lane opened: the repoint arm landed in B2-61 (configs/providers.yaml
default_model mistral-small-latest at :545, dormant :542, routing lists swept
:715-726) and the nameplate arm landed in B2-21 (mag/doctor.py:65 class map
names the 429 + x-ratelimit-*-limit 0 shape as the B2-04 mistral class,
header-fenced at :333-342). This lane's product is verification against live
bytes plus one live call per id, not a re-edit: yaml parse, estate load
(28 providers), doctor default path, and two one-token probes reproduce the
surgery's exact intended contrast. The queue row sat pre-checked [x] with no
receipt (the B2-238 disease); this landing earns the check.

## Evidence

- configs/providers.yaml:525-553 mistral block: nameplate "request-minute
  limit 0 for the on-file key, dormant 2026-09-26" (:526), dormant: true
  (:542), roster [mistral-small-latest] (:544), default_model:
  mistral-small-latest (:545), quota note carries both measured shapes (:553).
- Routing: B2-61 comment :715; yaml routing lists (6, :719-726) contain zero
  mistral hits (B2_105_verify_results.json routing_mistral_hits = {}).
- Estate: models.providers.load_providers() = 28 providers, mistral reads
  default_model mistral-small-latest, dormant true (same dict, byte-matches
  the yaml).
- Doctor default path (no probe env): mistral status DORMANT, probe
  none(dormant), detail "declared state, not probed, not an alarm"; zero
  issues mention mistral.
- mag/doctor.py nameplate: :65 "chat 429 + x-ratelimit *limit* = 0 ->
  QUOTA-DEAD (mistral: nameplate, 0 req/min)"; :333-342 zero-limit arm fences
  remaining/reset/used header substrings and names "nameplate lane (B2-04
  mistral class)".
- Live probes 2026-09-26 (B2_105_verify_results.json, key Mistral_API_KEY
  mixed case, prefix only, one 1-token call each, synthetic prompt):
  mistral-small-latest = 429, x-ratelimit-limit-req-minute: 0, code 1300,
  0.36s (the B2-04 zero-quota shape, byte-matches the B2-61 measurement);
  mistral-large-latest = 403 tier_not_allowed code 1910 "This model is not
  available in your subscription tier", 0.29s. The 403 rides the old id, not
  the lane: the surgery moved the default off it.
- Stale pointer, named: the brief cited configs/providers.yaml:473-488, which
  after B2-61's same-day edits is the z_ai3/z_ai4 region; the mistral block
  lives at 525-553. Recovered by grep; filed as a self-feed brief.

## Work done

1. Read B2_21_doctor_probe_20260926.md (the divergence that filed this brief)
   and B2_61_roster_purge_20260926.md + B2_61_verify.py/results (the landing
   it predated). Established both brief arms were already satisfied; no
   providers.yaml or mag/ byte needed changing, and re-editing landed work
   would be churn, so the lane verifies and closes.
2. Filed the shared-file claim on QUEUE.md at 18:45:16Z before any board edit.
3. Wrote B2_105_verify.py (four checks A-D) and ran it. Own defect found
   mid-run, honest: the first cut assumed load_providers() returns a list and
   reported estate "NOT FOUND in 3 providers" (it iterated dict keys); the
   dict shape gives 28 providers with mistral present, artifact patched. The
   doctor statuses shape (provider -> string) was likewise re-inspected before
   quoting.
4. Live probes D ran last, 2 calls, 2s apart, never printing key bytes.
5. Receipt, queue close (claim retire, pre-checked row earned, 2 self-feed
   briefs UNCHECKED), LEDGER row via .venv python json.dumps. Zero edits to
   mag/, tools/, tests/, configs/.

## Falsifier

Rerun watch/inbox/burn_wave_20260926/B2_105_verify.py: mistral-small-latest
must answer 429 with x-ratelimit-limit-req-minute: 0 (the nameplate shape) and
mistral-large-latest must answer 403 code 1910; the yaml and estate must read
default_model mistral-small-latest with dormant true; doctor default path must
read mistral DORMANT with zero issues. If small-latest answers 200 with
content while the lane still reads dormant, the operator has funded or
un-throttled the key and the GO flip defined in the yaml comment (:539-542,
drop dormant + re-add to routing) is due, not this surgery. If the estate and
yaml disagree on default_model, a concurrent lane edited the block mid-lane
and the claim law re-read applies before any further write.

## Bibliography closed

configs/providers.yaml (read only) · watch/inbox/burn_wave_20260926/
B2_105_verify.py + B2_105_verify_results.json (this lane's bytes) ·
B2_21_doctor_probe_20260926.md (divergence source) · B2_61_roster_purge_20260926.md
+ B2_61_verify.py + B2_61_verify_results.json (repoint landing) ·
B2_04_provider_health_20260926.md + B2_04_probe_results.json (original shapes) ·
mag/doctor.py (_classify_chat_failure, dormant fence) · models/providers.py
(load_providers) · QUEUE.md (claim 18:45:16Z, row close, self-feeds) ·
memory/burns/LEDGER.jsonl (row appended)
