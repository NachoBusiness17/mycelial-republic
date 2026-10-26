# TETHERED LINK STEAL 2026-09-25

External steal: surviving wide agent fan-outs on a phone-tethered link, and why
"sessions" die with fake subscription errors. Filed after the operator reported
crashing out with session timeouts and subscription errors ever since the Tree
Doctrine workflow started, from the tethered phone.

## What actually broke (bytes, not reports)

- Tree Doctrine 50-wide dig `dwfrun-15738edf` dispatched 50 diggers at 18:59Z on
  `account:zai-individual-coding-plan` (GLM-5.3-Flash, `api.z.ai/api/anthropic`).
- z.ai answered `429, code 1302 "Rate limit reached for requests"` (1,838 log
  lines today). Example payload kept verbatim in the log: `statusCode 429,
  reason rate_limited, statusMessage "[1302][Rate limit reached for requests]
  [202609260427121cb0abc314a54859]"`, `querySource workflow_child`.
- Retry asymmetry found in the adapter: main-session requests get
  `maxAttempts 11`; workflow-child requests get `maxAttempts 0, maxRetries 0`.
  Every 429 or dropped stream fails a digger on its first attempt.
- Hourly `model.network.failed` counts: 50 at 18:xx, 135 at 19:xx, 90 at 20:xx.
  The dig started 18:59Z. Failed stream durations cluster at 71 to 80 seconds:
  connection opens, carrier NAT kills the idle link, the client idle timeout
  fires. Sub-second failures (849 ms) are moments the tether was fully down.
- `Session not found` gateway errors at 20:14 to 20:22Z are the client trying to
  rehydrate sessions after their owning window died on the flapping link. That
  is the "session timeout" the operator sees.
- No 1309 ("GLM Coding Plan package has expired") anywhere in today's log. The
  "subscription error" is the 1302 rate-limit family rendered by the client, not
  billing. Two `CERT_HAS_EXPIRED` hits logged as a minor watch item.

## How others solve it (the steal)

1. z.ai documents the real envelope: rate and concurrency limits are tied to
   plan tier (Max > Pro > Lite), Lite is recommended one project at a time,
   concurrency is dynamically higher off-peak, and the plan is licensed only for
   officially supported tools. A 50-wide fan-out is far outside the Lite
   envelope by design, not by accident.
2. The unstable-network pattern (detect network loss, save in-flight state,
   auto-resume, used by Claude Code runners on WiFi drops and hotspot switches)
   is already native here: the workflow journal imports finished work as cache
   on amend. Amend, never rerun from zero.
3. The keepalive school: USB tethering over hotspot, keep the phone powered and
   screen on, and put long-lived streams behind something that holds the
   connection (proxy with TCP keepalive and long read timeouts). Carrier-grade
   NAT kills idle streams within minutes regardless of vendor.

## Laws adopted

- **Width law:** on the coding-plan account, dispatch fan-outs at
  `max_concurrency` 3 or less. 50-wide is an off-peak, dedicated-account luxury.
- **Off-peak law:** heavy digs ride off-peak windows (z.ai raises concurrency
  off-peak dynamically; GLM-5.3-Flash quota multiplier 0.4x off-peak vs 1.2x
  peak per the plan notice).
- **Owner law:** a running workflow can only be re-capped from the session that
  owns it (`workflow_run_not_retunable` from a sibling session, verified
  2026-09-25). Start long digs from the window that will hold the leash.
- **Tether law:** USB tether, phone powered, screen on. Expect NAT to kill idle
  streams. Resume, never rewind.
- **Retry law:** workflow children get zero adapter retries, so the width cap is
  the retry strategy. Keep width under the plan cap and the runner throttle
  stays quiet.

## Owed

- The live dig `dwfrun-15738edf` can only be re-capped by its owning window:
  amend it with `max_concurrency 3`. The harness rate-limit throttle currently
  has it at width 1, so it crawls but also still sporadically contests the
  account with the operator's foreground session.
- Chunked dispatch (waves of 3) inside the saved dig script so future runs are
  safe by construction. Gate first (`tools/workflow_gate.py`), then amend.
- Owed link: the "Detect network loss, save in-flight state, and auto-resume"
  GitHub item (seen in search 2026-09-25, full URL unresolved, not fabricated;
  filed per the no-fabrication law).

## Sources (all verified live 2026-09-25)

- z.ai usage policy, tier limits and off-peak concurrency:
  https://docs.z.ai/devpack/usage-policy
- z.ai API error codes (1302 rate limit, 1309 plan expired, quota reset):
  https://docs.z.ai/api-reference/api-code
- z.ai plan notice, off-peak quota multipliers:
  https://docs.z.ai/devpack/notice/usage-revision
- z.ai concurrency concept (limits vary by user/plan, excess requests fail):
  https://docs.z.ai/guides/overview/concept-param
- z.ai devpack FAQ (supported-tools restriction):
  https://docs.z.ai/devpack/faq
- OpenClaw Z.AI provider guide, third-party confirmation of 1302/1305 meanings:
  https://goddaehee.com

## Amendment 2026-09-26 (B2-435, shape-law correction of the Width Law above)

The "Width law" above stated the cap generically ("dispatch fan-outs at
max_concurrency 3 or less"), which reads as applying to Task-agent dispatch.
The gala envelope re-measure falsified that reading: the cap lives on the
workflow-child dispatch shape, not on Task agents -- Task agents ride the
main-session retry path (maxAttempts 11 + driver backoff) and measured clean
at widths 3, 6, 10 and 12 with width 10 banking 109.4M tok/h and zero
surfaced 1302s. This receipt stands as the 09-25 record of what was adopted
that night (registered frozen, not rewritten); the operative law is the
AGENTS.md "Fan-out width law (dispatch shape is the retry strategy)" bullet
as amended by B2-99, with the proven-width table in
watch/inbox/gala_20260925/AFTERPARTY_CLOSE_20260926.md (B2-476 amendment) and
watch/inbox/burn_wave_20260926/B2_443_dwf_error_census_20260926.md.
Snapshot copies of this file under
memory/runs/quote_audit_wide_20260925/snapshot/ inherit this correction by
reference and stay byte-frozen as audit artifacts.
