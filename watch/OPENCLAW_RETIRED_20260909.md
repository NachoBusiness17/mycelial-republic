# OPENCLAW RETIRED — 2026-09-09 (operator GO: "retire it")

*Filed by the zcode seat. Backup-first honored. Reversible in one command.*

## What was retired

The whole outside-door stack, parked behind compose profile `retired-openclaw`:

- **mag-openclaw** — the OpenClaw gateway (Node, 18789): the pre-hermes body for
  driving agents; multi-provider plugin surface (zai/deepseek/groq/cohere/cerebras/
  perplexity/codex/llama-cpp); talked to the host eye.
- **mag-openclaw-tailscale** — the sidecar that WAS the phone door (tailnet surface,
  no host ports by design).
- **cloudflared-openclaw** — the Cloudflare edge connector (was profile-gated off);
  moved with the stack because it `depends_on: openclaw: service_healthy`.

## Why (tri-state)

- **SUPPORTED: the internal loop is fully covered without it.** Hermes runs the
  workers, tavern (`steer --resume`), and repo-writing agents; the cage senses and
  flash lanes run the bulk. The week's record (09-02→09-09) shows ZERO openclaw
  traffic — nothing used the door.
- **SUPPORTED: it was a running cost with no caller.** Crash-loop #20+ since the
  update: 7 plugins stuck on capability consent, and the plugin installs themselves
  were timing out on npm egress — two gates deep even with the operator GO.
- **UNPROVEN (the honest residue): whether we ever want the outside door.** Nothing
  this arc recruited an external hand. If that day comes, resurrection is one command.

## Sacred-cow framing (not legacy shit)

This was the external-door DRAFT, and the draft taught us things the next door keeps:

1. **The governed PATCHES queue** (`queue/handoff/openclaw/PATCHES`: external writes
   land as JSON, host applies) — the fair-use firewall pattern for any future
   recruited hands, however they arrive.
2. **No host ports, ever** — the door was reachable only through its authenticated
   sidecar. The successor phone door keeps the law: cloudflared named tunnel +
   Access, one operator login, loopback law intact.
3. **Identity persists** — both named volumes kept
   (`..._mag_openclaw_data`, `..._mag_openclaw_tailscale`). The body is retired,
   not destroyed.

## Receipts

- Compose backup BEFORE edits: `docker-compose.yml.bak-openclaw-retire` (12,182 B).
- `docker compose config --quiet` → VALID after the three profile insertions.
- Containers stopped + removed: mag-openclaw, mag-openclaw-tailscale.
- Census after: mag-sovereign / mag-worker / mag-redis, ALL healthy, 24h uptime
  untouched — nothing else noticed. F1 control-plane dark by design (window to 09-13).
- Volumes retained: `local_sovereign_agent_mag_openclaw_{data,tailscale}`.

## Resurrect / succeed

- **Bring the door back:** `docker compose --profile retired-openclaw up -d openclaw tailscale-openclaw`
  (repair after update would still need capability-consent + container egress GO for npm).
- **Phone door instead:** host cloudflared is installed (2026.8.2) — quick tunnel =
  30s public-by-URL; named tunnel + Access = the permanent one-login door.

## Census note for the next boot reader

Running state is now **3 containers** (+ F1 control-plane deliberately stopped).
THAT IS THE INTENDED STATE. Idle containers are not the fleet's pulse; files are.
Do not restart anything without operator GO. See also `SEVEN_DAY_RECAP_20260909.md`.
