# moto_cron — Moto-as-cron bridge

Broken-screen **Moto G 5G 2024** (Termux + Tailscale) acts as a small job runner.
This folder is the **PC-side** inbox + watcher. Moto scripts are staged under `stage/` until SSH key auth works.

## Status (2026-10-23 America/New_York)

| Check | Result |
|-------|--------|
| `tailscale ping 100.102.34.118` | OK — pong ~115ms via LAN |
| SSH `:8022` | Host key learned (ED25519); **Permission denied (publickey,...)** for all existing PC keys |
| End-to-end probe/fetch | **Blocked** — no authorized key / possibly wrong Termux user (OpenSSH defaulted to `foste`) |

Moto `sshd` / `authorized_keys` / port **8022** were **not** modified (per brief).

### Smallest operator step

On the Moto (Termux local session or any already-working shell), authorize this PC key and note the username:

```bash
whoami
mkdir -p ~/.ssh && chmod 700 ~/.ssh
# append once (do not wipe existing keys):
echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICGYeyr7t0MbOt3U2OQzxdIwkb9tG2NpEX2IPDgFonlq foste@DESKTOP-7C70KSC' >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

Then from the PC (replace `USER` with Termux `whoami`):

```powershell
ssh -p 8022 -i $env:USERPROFILE\.ssh\id_ed25519 -o IdentitiesOnly=yes USER@100.102.34.118 "echo ok; whoami"
```

Pub key fingerprint: `SHA256:g7IiwK5m26rbhNaJFibsPEYZRP6YIIvT9EV1+Q4sNnw` (`id_ed25519.pub`, foste@DESKTOP-7C70KSC).

After auth works, push staged tree:

```powershell
powershell -File watch\inbox\moto_cron\stage\push_to_moto.ps1 -User USER
```

## Folder layout

```
watch/inbox/moto_cron/
  moto_flags.json          # FLAG -> notify seat
  moto_watch.py            # check / pull / watch / submit
  inbox.jsonl              # created at runtime (pulled results + alerts)
  README.md
  stage/
    push_to_moto.ps1
    moto-cron/
      bin/poller.sh
      bin/heartbeat.sh
      bin/start.sh
      termux-boot-moto-cron.sh
      jobs/ running/ done/ failed/ logs/   # empty placeholders
```

On the Moto after push: `~/moto-cron/{jobs,running,done,failed,logs,bin}` plus `heartbeat`, `outbox.log`, pidfiles.

## Flag vocabulary

| FLAG | Meaning | Default notify (`moto_flags.json`) |
|------|---------|--------------------------------------|
| `FLAG_FETCH` | `curl -sL` payload URL → save body; summary = http\|size\|sha256 | `ghost` |
| `FLAG_PROBE` | ping + curl reachability of payload host | `water_governor` |
| `FLAG_RENDER` | **stub** — write payload text to a file | `mag` |
| `FLAG_SHELL` | run payload under bash, timeout 300s | `ghost` |

Job manifest (`jobs/<name>.job`) — simple `KEY=VALUE` lines:

```
FLAG=FLAG_PROBE
PAYLOAD=100.96.161.76
NOTIFY=water_governor
ID=probe001
```

Result files: `done/<FLAG>__<ID>__<UTC>.result` (or `failed/`). One-line notes append to `~/moto-cron/outbox.log`.

## PC watcher

```powershell
cd C:\Users\foste\Documents\projects\local_sovereign_agent
python watch\inbox\moto_cron\moto_watch.py --user USER check
python watch\inbox\moto_cron\moto_watch.py --user USER pull
python watch\inbox\moto_cron\moto_watch.py --user USER watch
python watch\inbox\moto_cron\moto_watch.py --user USER submit FLAG_PROBE 100.96.161.76
python watch\inbox\moto_cron\moto_watch.py --user USER submit FLAG_FETCH https://example.com
```

- `check`: Tailscale ping; SSH-read `~/moto-cron/heartbeat`; alert to `inbox.jsonl` if unreachable or heartbeat age > 20 minutes.
- `pull`: new `done/*.result` + `outbox.log` bytes → `inbox.jsonl` tagged with notify from flags map / manifest.
- `submit`: writes manifest and `scp` into `~/moto-cron/jobs/`.

## Proposed scheduled task (NOT registered — approve first)

Exact command for Nacho to approve:

```bat
schtasks /Create /TN "MotoCronWatch" /SC MINUTE /MO 5 /TR "python C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\moto_cron\moto_watch.py --user USER watch" /F
```

Replace `USER` with Termux username. Run elevated if needed. **Do not create until SSH auth works.**

## Keep-alive (on Moto)

- `bin/start.sh` — idempotent; pidfiles; `termux-wake-lock` if present; `pkg install curl` only if missing.
- `~/.termux/boot/moto-cron.sh` — installed **only if** `~/.termux/boot` already exists (Termux:Boot); otherwise noted as skipped.

## Planned E2E tests (after auth + push)

1. `FLAG_PROBE` payload `100.96.161.76`
2. `FLAG_FETCH` payload `https://example.com`

Then `python moto_watch.py --user USER watch` and inspect `inbox.jsonl` + heartbeat.

## Redundancy / jump

- Direct PC->Moto SSH (Tailscale `100.102.34.118:8022`, user `u0_a467`, key `id_ed25519`) is primary.
- Bob laptop also has working key `pixel_lane` -> same Moto user (second path).
- `moto_watch.py` defaults `--jump bob` (PC `~/.ssh/config` Host `bob`). If direct SSH fails, it retries with `ProxyJump=bob`. Set `MOTO_JUMP=` empty to disable.
- Grok Bot lists machine **moto g 5G - 2024** as registered but **not connected** — no install attempted.

