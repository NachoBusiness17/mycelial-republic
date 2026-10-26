# Phone Relay — approvals from anywhere · 2026-09-24

**Trigger:** operator, away from the box: "its fucking trash that i cant approve
this shit from my phone." GO issued for the build same turn.

**What exists now:** `mag/phone_relay.py` (commit `3ed4dd2c9`) — an approval
relay over the private Mag↔operator Discord DM. Any seat, script, or gate calls:

```
python mag/phone_relay.py ask "promote X?" --timeout 600   # exit 0 approve / 1 deny
python mag/phone_relay.py test                             # lane self-test
```

**The law it enforces (fail-closed everywhere):**
- timeout = DENY — silence never approves
- only `DISCORD_ALLOWED_USERS` may decide, and only in the DM — never a shared
  channel (Adam sits in the guild; the guild lane is disqualified by design)
- pinned host `discord.com` over https, redirects refused, proper bot UA
- kill switch: `PHONE_RELAY=off` → every ask denies immediately
- rate cap 12 asks/hour; every ask/reply/test logged to
  `watch/inbox/phone_relay_log.jsonl`; token never logged (last4 only)

**Receipts from the build (three faults found and fixed live):**
1. `api.discord.com` is NODATA worldwide since today — no A, no AAAA, no HTTPS
   record at Cloudflare's own authority (verified via DoH on 1.1.1.1). The box's
   DNS was fine (`example.com` resolved; only discord names failed). First
   sticky-IP workaround pinned gateway peers → Cloudflare 1016 (wrong zone).
   Fix: `discord.com` is the documented alternative REST base — works.
2. The 09-15 DM channel id is dead (404 Unknown Channel 10003). Fix: the relay
   now self-heals — opens a fresh DM with each allowed user, caches the channel
   id in `state/phone_relay_channel.json`, revalidates on every use.
3. Self-test passed end-to-end: posted message `1552807422299603006` to the DM
   and read it back; token last4 `1CrM` (the 09-15 rotation) confirmed live.

**Live-fire receipt (honest):** the card went out at 18:22 local, sat 10
minutes, and **timed out to DENY** — exactly the fail-closed law executing on
real silence. No reply, no reaction during the window. Proven live: delivery
(DM), polling, timeout-deny. Still unproven: the operator-reply→decision link
(needs his thumb; he was on Discord in the same DM earlier that evening, so the
lane reaches him — the test just didn't catch him engaged). Lesson bought and
fixed same night (`67b36a147`): **reactions on the card now count as
decisions** — the phone-native gesture is a tap, not a typed reply, and the
first parser was deaf to it. Next real approval proves the last link.

**Phase 2 (not built tonight — needs the box idle of experiments):**
- PreToolUse hook in ZCode that routes *dangerous-class* Bash commands (push,
  delete, spend, schtask changes) through `phone_relay.ask` instead of the
  desktop dialog — combined with yolo permission mode on away-sessions this
  makes the whole box remote-governable: routine work runs free, dangerous
  work lands in his pocket.
- Workflow-submission confirmations are ZCode-core UI and can't be hooked from
  the estate; the compensating control is the same yolo+relay pairing.

**Honest limit:** the relay approves things the estate asks about. It does not
(click and cannot click) ZCode's native desktop dialogs. Phase 2 is the
architectural closure of that gap.
