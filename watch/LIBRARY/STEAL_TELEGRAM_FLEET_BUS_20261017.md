# SELF-STEAL: Telegram as the fleet bus (Ghost, Mag, mates, Hermes, phones/T90, Roku walls)

Date: 2026-10-17, ~20:50 ET. Read-only pass on the PC repo plus the local Hermes install (file names, the
cron jobs list, and gateway.log Telegram lines with tokens masked). No git. No code changes. No model calls.
No Telegram messages. Running processes left alone. Not opened: any .env (repo or `%LOCALAPPDATA%\hermes\.env`),
key files, secret_gate_results/, free_keys/, memory/trajectory/steps.jsonl, configs/telegram_token.txt (it does not exist).

Operator ask: "we still need to put everything into telegram so you all can communicate there."

**The finding in one line:** Mag already has a working Telegram bridge. It is the **Hermes gateway**. It is
installed, it autostarts, and its Telegram platform is configured, but it has been **parked since at least
2026-10-14** because the bot token was revoked. The bus is one new BotFather token, one group, and a few
config values away. The only new code is a ~40-line digest script that Hermes cron runs. No new chat system and no new brain.

---

## 1. What Mag already has (file:line)

### 1a. The live bridge: Hermes gateway (Nous Hermes Agent, `%LOCALAPPDATA%\hermes\`)
- **Telegram is configured but parked.** `%LOCALAPPDATA%\hermes\logs\gateway.log` (last write 2026-10-17 00:30 ET),
  2026-10-14 12:29: `[Telegram] Failed to connect to Telegram: The token 8750925249:*** was rejected by the server` then
  `1 configured platform(s) failed to start and are parked ... telegram ... The gateway is DEGRADED - it serves the
  remaining platform(s)`. Discord is still served. The gateway's own fix text: "generate a new one with @BotFather and update TELEGRAM_BOT_TOKEN".
- Matches `watch/inbox/HANDOFF_20260927_SESSION_CLOSE.md:39-41`: "TELEGRAM: bot 8750925249 deleted, dead server-side
  (getMe 401) ... Phone relay machinery dormant, no new bot owed."
- History: `watch/inbox/HERMES_DISCORD_SETUP_20260915.md:13,40`: "Telegram reconnected 10:07:36", "The gateway's
  Telegram lane was green throughout". `jobs/hermes-control-channel/trail_core_0.md:10-11`: "gateway running ... telegram connected" (09-11).
- Autostart: `HERMES_DISCORD_SETUP_20260915.md:44` "Gateway autostart: Hermes_Gateway.vbs login item installed".
- Vendored source mirror (read copy, not the running code): `watch/hermes_wings/src/`.
  - Config var NAMES the Telegram adapter reads (from `gw_run.py` / `cron_sched.py`, NOT from any .env):
    `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ALLOWED_USERS`, `TELEGRAM_ALLOW_ALL_USERS`, `TELEGRAM_GROUP_ALLOWED_CHATS`,
    `TELEGRAM_GROUP_ALLOWED_USERS`, `TELEGRAM_HOME_CHANNEL`, `TELEGRAM_HOME_CHANNEL_THREAD_ID`, `TELEGRAM_CRON_THREAD_ID`.
  - Allowlist is the default stance: `gw_run.py:14016-14021,14077` ("configure platform allowlists (e.g., TELEGRAM_ALLOWED_USERS=your_id)").
  - Forum topics are handled: `gw_run.py:8661-8679` (General topic ids), `cron_sched.py:2312-2333` (`TELEGRAM_CRON_THREAD_ID`
    overrides `TELEGRAM_HOME_CHANNEL_THREAD_ID`), `cron_sched.py:2860` (targets like `telegram:-100...:17` = chat + topic).
  - **Script-to-Telegram with zero model calls:** `cron_sched.py:5790-5807`, the `no_agent` short-circuit: "the classic
    'run a bash script on a timer, send its stdout to telegram' watchdog pattern ... no AIAgent, no prompt, no tool loop,
    no token spend". Script stdout becomes the message. Empty stdout is a silent run. A non-zero exit is sent as an error alert.
    Home channel resolves from `TELEGRAM_HOME_CHANNEL` (`cron_sched.py:689,2260-2305`).
  - **MCP door into the chat for any local seat:** `mcp_serve.py:1-14` (`hermes mcp serve`): `conversations_list`,
    `messages_read`, `events_poll`, `events_wait`, `messages_send` (`:897-930`, target `"telegram:<chat_id>"`), `channels_list`.
    A seat with an MCP client can read and post into the Telegram group without holding the bot token.
- Hermes cron today: `%LOCALAPPDATA%\hermes\cron\jobs.json` has 2 jobs (`intake-wave`, `drift-canary`). Both are
  `deliver=local` and disabled. Nothing currently delivers to Telegram.
- Prior steal already named this: `watch/STEAL_HERMES_AGENT_20260902.md:53-55`: "cron/: native scheduler - candidate
  conductor for the scrum cadence"; "gateway/: Telegram surface = the operator's phone door"; "it can SERVE MCP (mcp_serve.py)".

### 1b. Mag's own Telegram code
- `mag/telegram_desk.py:1-20` is a standalone public-facing desk bot (v0, 2026-09-10). It long-polls getUpdates and
  answers via the deepseek lane (`:100-110`, a model call per message). Token slot `TELEGRAM_BOT_TOKEN` / `TELEGRAM_TOKEN`
  env or `configs/telegram_token.txt` (`:11,42,71-79`). SSRF pin `api.telegram.org`, method allowlist
  `getMe/getUpdates/sendMessage` (`:44-46`). Trail `memory/runs/telegram_trail.jsonl` (`:41`).
  - Known defects (`watch/inbox/model_garden/swarm1-deepseek-mag__telegram_desk.md:11-15`): DNS-check TOCTOU,
    poll/send errors not trailed, inbound text trailed unredacted, `_NoRedirect` defined but unused (`:50-55` vs `:47`).
  - **It has no chat allowlist.** It answers anyone who messages it. Do not use it as the fleet bus.
  - `configs/telegram_token.txt` does not exist (Test-Path False), and `.gitignore` has no rule naming it. Do not create it.
- `mag/phone_relay.py:1-13` is a fail-closed approval card over a **Discord** DM. It has the patterns to copy for Telegram:
  allowlisted deciders (`:76-84`), exact-token decision (`:41-53`), timeout = DENY (`:213-215`), kill switch
  `PHONE_RELAY=off` / `PHONE_RELAY_OFF=1` (`:133-134`), rate cap 12/h (`:54,113-124`), log `watch/inbox/phone_relay_log.jsonl`.
  It reads its token from `%LOCALAPPDATA%\hermes\.env` (`:32,64-73`). **That file is the estate's existing secret slot for chat bots.**
- `scripts/tg_harvest.py:1-7` only harvests public channels through t.me/s/ previews (read-only intake). It is not a bus.
- `tools/secret_gate_rules.py:52` already has a `TELEGRAM-BOT` token pattern, so the secret gate will catch a pasted token.

### 1c. Fleet organs the bus would mirror (all 2026-10-17)
- `mag/fleet_report.py:1-29`: fleet_report.v1 (SPOTREP / SITREP / NOTICE / RELIEF / ACK) as receipt bodies in
  `watch/receipts/seat_*.json`. `notices()` `:252-300` returns notices in force + ACKs and documents ack/cancel (`:296-298`).
  The names-only law (`:22-24`) refuses secret-shaped values.
- `mag/leases.py:1-50`: restricted-list leases. Ledger `watch/receipts/leases/ledger.jsonl`. **The raw lease_token is
  shown once and never lands on disk.** That token must never be posted to a group either.
- `mag/proposals.py:1-25`: signed proposal / review / promotion under `watch/receipts/proposals/<id>/`, quorum tally.
- `mag/warm_surface.py:1-29`: `mag://warm/tip`, `state`, `notices`, `leases`, `preamble/<seat>`. `redact_text` `:92` is the
  redaction pass any outbound text should go through.
- `mag/mcp_server.py:138-149`: `estate_fleet_report`, `estate_notices`, `estate_lease_*`, `estate_propose/review/proposals`
  as MCP tools. No write/exec beyond watch/receipts.
- `mag/seat_handshake.py:1-20`: Ed25519 seat envelope (off by default).
- `tools/leave_dispatcher.py:1-30`: mates. Receipts land in `watch/inbox/mates_leave_protocol/receipts/`.
- `mag/cast_server.py` + `mag/display.py`: phone/T90 control page and the Roku-safe display JSON (see STEAL_SWARM_THIN_CLIENT s.2).
- Kill: there is **no fleet kill sentinel organ yet**. `STEAL_NOUS_FLEET_20261017.md:121` says "Fleet kill sentinel from
  defense Build A not built yet". The design is a NOTICE `fleet_kill` + revoked seats + lab_ctl (`:110,135`).
  `FLEET_COORDINATION_DOCTRINE_20261017.md:233` lets any seat stop a runaway as self-defense if it files a SPOTREP in the same window.

### 1d. Doctrine on Telegram (read these before over-trusting it)
- `watch/inbox/SCRUM_SWARM_20261016.md:16-21,29-36,47-51`: Telegram is T90's channel. "The standup IS the Telegram chat".
  Relay ~60 lines, "one credential short". **Correction:** it says the plumbing is "the gstdbot mirror's Telegram plumbing
  (gstd_mirrors/)". `gstd_mirrors` is not on disk in this repo (Test-Path False; `rg --files` finds no gstd mirror dir).
  The in-tree plumbing that actually exists is the Hermes gateway above plus `mag/telegram_desk.py`.
- `watch/onboard/TEAM.md:42`: "Telegram is the office. One thread, no meetings."
- `jobs/hermes-control-channel/seat_contract.json:4,9` (operator, 2026-09-11): "the telegram channel has proven to be less
  robust and trustworthy" -> "no hop may depend on Telegram". The tailnet steer door was proven instead (`trail_core_0.md:12-19`).
- `watch/SELF_STEAL_TELEGRAM_CHANNEL_20260905.md:34`: "Telegram is the megaphone, never the wall." `:45`: "THE BOT NEVER COLD-DMs."
- `watch/inbox/mates_leave_protocol/receipts/receipt_20261017_locksmith.md:59-61`: "one Telegram bot token short, operator's two minutes."

So: **Telegram is the shared bus and mirror. Receipts on disk stay the record. The tailnet steer door stays the fallback control path.**

## 2. Gaps
- G1 **Token.** The old bot was deleted. A new BotFather token is needed in the Hermes slot. Until then Telegram stays parked.
- G2 **Chat id(s).** No fleet group exists yet. Hermes needs `TELEGRAM_HOME_CHANNEL` (and topic ids if topics are used).
- G3 **Allowlist.** `TELEGRAM_ALLOWED_USERS` / `TELEGRAM_GROUP_ALLOWED_CHATS` need the operator's (and trusted mates') numeric
  Telegram user ids and the group id. Values unknown. Not looked up.
- G4 **Bridge process.** Nothing turns Mag receipts into Telegram text. Both Hermes cron jobs are local and disabled. A
  digest script (cursor-based, redacted) does not exist.
- G5 **Inbound commands.** The Hermes agent behind the gateway is a model (Nous lane). Wiring Mag's warm MCP into Hermes as an
  MCP server is only a doc snippet (`docs/SHARED_SURFACE_CLIENTS.md:147-173`, "nothing written to configs").
- G6 **Kill sentinel** is not built (see 1c).
- G7 **Two pollers, one token.** If `telegram_desk.py` ran on the same token as the Hermes gateway, getUpdates would conflict
  (Telegram allows one poller per bot). One bot = one poller = Hermes. A desk bot, if wanted again, gets its own bot.
- G8 **Grok Bot seats (Ghost, this Mag seat)** run off-box with no Telegram connector. This session's tool catalog lists no
  Telegram namespace. They cannot read or post in Telegram directly.

## 3. Recommended bus design

### 3a. Channel structure (one group, topics)
One private Telegram **supergroup with Topics on**: "Mag Fleet". The bot is a member, the operator is owner, invite-only.
| Topic | What lands there | Source organ |
|---|---|---|
| General | operator + T90 talk, directions to the director (Hermes) | humans; Hermes replies |
| ALERTS | fleet_kill / hazard NOTICE, digest errors. Sent loud (notification on) | NOTICE category kill/hazard; cron error alerts |
| NOTICES | new NOTICE, cancellations, ACK roll-up ("3/5 seats acked N-12") | `fleet_report.notices()` |
| LEASES | acquire / release / transfer / expire / break: resource, holder, purpose, until. **Never the token** | `watch/receipts/leases/ledger.jsonl` |
| PROPOSALS | new proposal (title, author, targets), each review verdict, promotion "ready" + tally. One message per proposal, verdicts replied under it | `watch/receipts/proposals/*` |
| REPORTS | SITREP / SPOTREP / RELIEF one-liners, mate receipt summaries (title + verdict + path), scrum team piece-done | `watch/receipts/seat_*.json`, `mates_leave_protocol/receipts/` |
| TIP | periodic status: chain tip root_short + leaves, warm_state lag, notices-in-force count, leases held. Hourly or on change | `warm_surface.tip()` / `warm_state()` |
Per-seat DMs: not needed. Seat identity rides in the message prefix (`[hermes]`, `[mate:locksmith]`, `[ghost]`).
That keeps one thread (TEAM.md:42). If Hermes topic routing misbehaves at first, fall back to a flat group with a
prefix tag per line. Same content, no topics.

### 3b. Organ -> message map
| Mag organ | Telegram message | Trigger |
|---|---|---|
| `fleet_report` SITREP/SPOTREP/RELIEF | `[seat] SITREP: <status> (receipt seat_x.json)` -> REPORTS | new receipt since cursor |
| NOTICE | `NOTICE N-xx <category>: <subject> until <in_force_until>` -> NOTICES (operator may pin) | new / cancelled |
| ACK | rolled into the notice line, edited or re-posted as a tally | new ACK |
| leases | `LEASE <resource> -> <seat> until <t> (<purpose>)` / `RELEASED` / `EXPIRED` -> LEASES | ledger.jsonl new rows |
| proposals | `PROPOSAL p_... "<title>" by <seat>` then `review <seat>: approve/reject` then `READY tally a/b` -> PROPOSALS | new files |
| mate receipts | `[mate:<id>] <title>: <first verdict line> (path)` -> REPORTS | new receipt files |
| warm tip | `TIP <root_short> leaves=<n> lag=<k> notices=<n> leases=<n>` -> TIP | hourly or on change |
| kill | `FLEET KILL in force: <subject> - by <seat>` -> ALERTS, loud | NOTICE category fleet_kill |
Every line passes `warm_surface.redact_text` before printing. No home paths, no tailnet 100.x IPs, no tokens.

### 3c. Auth: who holds what
- **Bot token stays on the host**, in the Hermes secret slot only. Phones, the T90, mates, and remote seats never hold it.
- **Humans (operator, T90 in his hand, trusted people)** use the normal Telegram app. A phone needs nothing from Mag.
- **Inbound is allowlist-only.** `TELEGRAM_GROUP_ALLOWED_CHATS` = the fleet group. `TELEGRAM_ALLOWED_USERS` = operator (+ named
  humans). Everyone else is ignored by the gateway's default.
- **Host-local seats with MCP** (ZCode, Gemini CLI, Claude Code / Cursor on the PC, Hermes itself) read and post through
  `hermes mcp serve` (`messages_read`, `events_poll`, `messages_send`). That is the gateway's token used in-process, not copied.
- **Phone/browser thin clients** (cast_server `/control`, T90 browser) keep talking to cast_server / warm MCP. The host
  mirror makes their intents and receipts visible in Telegram. No Telegram code goes on phones.
- **Roku walls** never touch Telegram. They stay read-only on `display.py` JSON. The same facts show on both, from the same receipts.

### 3d. Who can post from which seat (honest)
| Seat | Reads Telegram | Posts to Telegram | How |
|---|---|---|---|
| Operator / T90 (human) | yes | yes | Telegram app |
| Hermes (gateway agent) | yes | yes | it IS the bot (after the token lands) |
| Mag host organs (receipts) | n/a | yes, indirectly | Hermes cron `no_agent` digest -> home chat |
| ZCode / Gemini CLI / other PC MCP seats | yes | yes | `hermes mcp serve` tools; or file a fleet_report and let the digest post it |
| GLM mates (leave_dispatcher) | no | indirectly | their receipts get summarized by the digest |
| Ghost / this Mag seat (Grok Bot, off-box) | not directly | indirectly | write a fleet_report/receipt on the PC through the machine tools (when the PC is connected), which the digest mirrors. Or the operator pastes. No Telegram connector exists for these seats |
| phone/T90 browser clients | via the human app | indirectly | cast_server intents -> receipts -> digest |
| Roku | no | no | display.py only |

### 3e. Overlap with STEAL_SWARM_THIN_CLIENT_20261017.md
- Same token gap (`G6` there, `SCRUM_SWARM:47-49`). This report narrows it: the token goes into the **existing Hermes slot**.
  The SCRUM doc said "into .env", meaning the repo .env. Use the Hermes .env the gateway already loads.
- The "~60-line relay" in SCRUM_SWARM is mostly **already built** as the Hermes gateway (inbound) plus cron delivery (outbound).
  What is left is the digest script.
- The thin-client report's swarm board (`/api/v1/swarm/board`) and this digest read the same inputs (tip, notices, leases,
  receipts). Build one composer function and have both call it. Roku, phone, and Telegram then show the same picture.

## 4. Smallest build (when the operator says go; NOT built in this pass)
1. **`scripts/fleet_bus_digest.py` (~40-60 lines, stdlib, no network):** reads a cursor file
   (`watch/receipts/fleet_bus_cursor.json`). Prints one line per NEW item since the cursor: notices (via `fleet_report.notices()`),
   lease ledger rows, proposal files, seat receipts, mate receipts. Prints a TIP line only when the tip changed or an hour has passed.
   Every line goes through `warm_surface.redact_text`. Lease tokens are never read (they are not on disk anyway). Exit 0 + empty
   stdout when nothing is new. Writes the cursor only after printing.
   Optional `--topic notices|leases|...` filter, so several cron jobs can feed several topics.
2. **One Hermes cron job** (Hermes' own cron, the existing scheduler): `no_agent: true`, script = the digest, every 2-5 min,
   `deliver: telegram` (home channel). Optionally one job per topic using `telegram:<chat>:<thread>` targets.
   Zero model calls (`cron_sched.py:5790-5807`).
3. **Inbound (optional, phase 2), no new brain:** add Mag's warm MCP (stdio `--profile warm`) to Hermes' MCP client config
   (snippet already at `docs/SHARED_SURFACE_CLIENTS.md:147-173`). In the allowlisted group, the operator can say "who holds
   the restricted leases" / "file a notice ..." / "tip" and Hermes calls `estate_leases`, `estate_notices`, `estate_fleet_report`,
   or `mag://warm/tip`. These are existing tools. Rules:
   - lease acquire from chat: Hermes may acquire as seat `hermes`, but the reply shows holder/until only, never the token
     (the token stays in Hermes' process or session);
   - kill from chat: files NOTICE category `fleet_kill` through `estate_fleet_report` (doctrine self-defense). Any actual
     process stop stays behind a phone_relay-style approve/deny card (timeout = DENY), never a free-text command;
   - no shell or exec from Telegram. Same law as telegram_desk (`:13-14`).
4. **Fallback if Hermes is down:** a mag-side `sendMessage`-only poster could reuse `telegram_desk._api` (method allowlist,
   SSRF pin). Only if Hermes is unavailable, because a second sender adds a second token reader.

## 5. What Nacho must do by hand
1. Telegram -> **@BotFather** -> `/newbot` -> pick a name/username -> copy the token. Optionally `/setprivacy` -> Disable, if
   the bot should see all group messages and not only commands or mentions.
2. Create a **private group** "Mag Fleet". In group settings turn **Topics on** (makes it a forum supergroup). Create topics:
   ALERTS, NOTICES, LEASES, PROPOSALS, REPORTS, TIP. **Add the bot** and make it admin if it should pin.
3. Put the token where Hermes already keeps chat secrets: **`%LOCALAPPDATA%\hermes\.env`, line `TELEGRAM_BOT_TOKEN=`**. That is
   the slot the gateway reads (its own error message names it) and where phone_relay already reads the Discord token from.
   Use the Hermes setup / `hermes config` flow, or edit the file yourself. Do **not** paste the token into chat, the repo,
   `configs/telegram_token.txt`, or a repo .env (the secret gate has a TELEGRAM-BOT rule for a reason).
4. In the same slot, set (values only you can see):
   `TELEGRAM_ALLOWED_USERS=<your numeric user id>[,<trusted ids>]`,
   `TELEGRAM_GROUP_ALLOWED_CHATS=<group id, -100...>`,
   `TELEGRAM_HOME_CHANNEL=<group id>`, optionally
   `TELEGRAM_HOME_CHANNEL_THREAD_ID=<REPORTS topic id>` / `TELEGRAM_CRON_THREAD_ID=<topic id>`.
   (Group and topic ids show in Hermes' `channels_list` after the bot sees one message, or in the topic link `t.me/c/<id>/<thread>`.)
5. Run **`hermes gateway restart`**. The log should show Telegram connected and no "parked" line.
6. Say go on the digest + cron job (section 4). An agent builds it. Nothing posts until then.

## 6. Tests (stdlib, no network, no model calls)
- `test_digest_empty_is_silent`: no new receipts -> exit 0, stdout empty, cursor unchanged.
- `test_digest_new_notice_line`: temp receipts dir with one NOTICE -> exactly one `NOTICE N-..` line, then a second run prints nothing.
- `test_digest_lease_no_token`: ledger rows -> output has resource/holder/until and no 32+ char token-shaped string; the
  `sha256` field is never printed.
- `test_digest_redaction`: a receipt subject with a home path / 100.x IP / TELEGRAM-BOT-shaped string -> redacted
  (secret_gate_rules pattern finds 0 hits in stdout).
- `test_digest_kill_first`: a `fleet_kill` NOTICE sorts first and carries the ALERTS tag.
- `test_digest_topic_filter`: `--topic leases` prints only lease lines.
- `test_digest_cursor_atomic`: crash between print and cursor write -> next run re-prints (at-least-once, never lost).
- `test_no_second_poller`: a static check that no repo module calls getUpdates while Hermes owns the token (telegram_desk
  stays unlaunched; a desk bot gets a different token).
- Live (operator present, after the token): `hermes gateway` log shows Telegram connected. Cron job "run now" with a
  seeded test NOTICE -> one message in NOTICES. A message from a non-allowlisted account -> ignored (gateway log).
  `hermes mcp serve` `messages_read` from a PC seat returns the group history.

## 7. Plain English
Mag already owns a Telegram bot driver: the Hermes gateway, the same program that runs the Discord "Mag" bot. Telegram
stopped because the old bot was deleted in September, and the gateway has been waiting for a new key since. Make a new bot
with BotFather, make a private group with a few topics, add the bot, and put the key in the Hermes settings file the
gateway already reads. Then Hermes' built-in timer can run one small Mag script every few minutes. The script turns new
notices, leases, proposals, reports, and mate receipts into short lines in the group, and it uses no AI to do it. You and
the T90 talk in the group. Hermes answers and can call Mag's existing lease, notice, and tip tools. PC seats can read and
post through Hermes' MCP door. Ghost and the other off-box Grok Bot seats can't sit in Telegram themselves. They file
reports on the PC, and those show up in the group. Rokus keep showing the same facts on their own screen. The files on
disk stay the record. Telegram is the loudspeaker and the meeting room, and the tailnet steer door is still the backup
when Telegram is down.
