# RUNNERS: per-device one-pagers (2026-10-11)

The still-open item in LOOP_CLOSED.md: "Cross-device consensus RUNNERS: t90/bob
hold payment identities; their harness executions wait on python/Termux installs
(the coldest-vertex law says the phone run is the final proof of portability)."
These three one-pagers close it. Each is paste-ready: install, run, bank.

## Facts every device relies on (verified tonight, 2026-10-11)

- Ollama is live on the desktop's tailnet IP: `curl http://100.96.161.76:11434/api/tags`
  answered 15 models, including all five of the consensus run
  consensus-20261011T000937Z: gemma:2b, deepseek-r1:1.5b, qwen2.5:3b-instruct,
  gemma2:2b-instruct-q5_K_M, qwen-desk:latest.
- The harness is ONE stdlib-only file: `tools/consensus_harness.py`. No pip
  installs. No repo needed. Python 3.9+ suffices.
- Bare-device proof (tonight): the single file copied alone into an empty
  directory tree (no repo, no estate data) ran against 100.96.161.76, used its
  built-in fixture task bank (8 tasks, 8 distinct truths), exit 0, and
  self-banked its receipts under
  `watch/inbox/gstd_perimeter_build_20261010/runs/20261011T023240Z/`.
- Closed-perimeter law is enforced in code: `--host http://example.com:11434`
  was refused tonight with exit 2, "host resolves outside the closed perimeter
  (172.66.147.243); this tool reaches loopback/LAN/tailnet only". Only
  loopback, RFC1918 LAN, and Tailscale 100.64/10 hosts are reachable.
- Desktop banking door: OpenSSH sshd is Running on desktop-7c70ksc port 22
  (verified service state tonight). scp into it works with the operator's
  Windows account (foste). Auth was not exercised by the writer of this page;
  if scp auth is not set up, use the Taildrop/paste fallbacks named per device.
- Git route (durable, later): the repo is public
  (github.com/NachoBusiness17/mycelial-republic, 644 KB) BUT
  `tools/consensus_harness.py` is UNTRACKED as of tonight (git status), so a
  clone does NOT carry the harness until the coordinator commits it. Tonight's
  route is the single-file copy below; after the commit lands, `git clone`
  replaces it.
- Paste-line proof (tonight, desktop): the exact five-model command below was
  executed verbatim against http://100.96.161.76:11434 (the estate venv python
  standing in for `python`, since bare python on the desktop is Hermes by the
  repo's env law): exit 0, run consensus-20261011T022831Z, 14 tasks, 10
  distinct truths, consensus_rate 0.8571 vs dead-salmon 0.1539, verdict
  STRUCTURE, receipts banked at
  watch/inbox/gstd_perimeter_build_20261010/runs/20261011T022831Z/.

## The paste line (identical on all three devices; only the python launcher varies)

```
python tools/consensus_harness.py --host http://100.96.161.76:11434 --models gemma:2b,deepseek-r1:1.5b,qwen2.5:3b-instruct,gemma2:2b-instruct-q5_K_M,qwen-desk:latest
```

Exit 0 = run banked (rates are data, not pass/fail). Exit 2 = cannot run (host
refused, or fewer than 2 models). Runtime: 22 tasks x 5 models, minutes, and
the models all execute on the desktop; the device is dispatcher + judge +
receipt filer (CPU-light, the coldest-vertex job class from SPEC.md).

The receipt to bank is the run directory the harness itself writes:
`watch/inbox/gstd_perimeter_build_20261010/runs/<UTC timestamp>/` containing
`summary.json` (the headline: rates + verdict), `consensus_ledger.jsonl` (one
row per model, the learning ledger), `receipt.jsonl` (per-task answers, the
honesty file). Bank = get that directory onto the estate desktop, then append
one line to the table at the bottom of this page.

---

## A. bob (Windows 10 laptop, tailnet 100.125.103.60, wallet UQAW3wO8TwzoBuOjA-XwCivj80eKhRzGAWl_PgkzUUUlbe5m)

1. Join check (bob already runs Tailscale; it shows online in the tailnet):

```
tailscale status
ping 100.96.161.76
```

2. Install Python (winget is on updated Windows 10; if absent, download the
   python.org 3.12 installer and tick "Add python.exe to PATH"):

```
winget install -e --id Python.Python.3.12
py -3 --version
```

3. Get the harness (single file). On the DESKTOP run:

```
tailscale file cp tools\consensus_harness.py bob:
```

Accept the Taildrop on bob; the file lands in Downloads. Then on bob:

```
mkdir %USERPROFILE%\gstd\tools
copy "%USERPROFILE%\Downloads\consensus_harness.py" "%USERPROFILE%\gstd\tools\"
cd %USERPROFILE%\gstd
py -3 tools\consensus_harness.py --host http://100.96.161.76:11434 --models gemma:2b,deepseek-r1:1.5b,qwen2.5:3b-instruct,gemma2:2b-instruct-q5_K_M,qwen-desk:latest
```

The file must sit in a folder named `tools` (one level under the folder you
run from): the harness banks its receipts relative to its own parent
directory, so `%USERPROFILE%\gstd` becomes the receipt root.

4. Bank the receipt. The run landed in
   `%USERPROFILE%\gstd\watch\inbox\gstd_perimeter_build_20261010\runs\<ts>\`.
   Zip it and push it to the estate (Windows 10 ships tar and the OpenSSH
   client; the desktop sshd is Running):

```
cd %USERPROFILE%\gstd
tar -a -c -f %TEMP%\bob-run.zip watch\inbox\gstd_perimeter_build_20261010\runs\<ts>
scp %TEMP%\bob-run.zip foste@100.96.161.76:Documents/projects/local_sovereign_agent/watch/inbox/gstd_perimeter_build_20261010/runs/
```

Fallback if scp auth is not set up: `tailscale file cp %TEMP%\bob-run.zip desktop-7c70ksc:`
(bob is Windows, so it has the Tailscale CLI).

5. Security baseline (bob is the W10 coldest vertex): run the join-day checks
   in SECURITY_BASELINE_W10.md on the machine and file the pass/fail lines as
   `watch/inbox/gstd_perimeter_build_20261010/laptop_join.md` (the receipt
   that baseline names). A mesh node that files receipts must be trustworthy
   before it files them.

6. Append one line to the banked-runs table at the bottom of this page
   (device, run_id, consensus_rate, verdict). That line plus the run directory
   IS the receipt; no claim without it.

## B. t90 (Android tablet, tailnet 100.72.38.3, online tonight, wallet UQBrE6BRPvZkBH47rHGfL7TmepeakX--unodq9I_K6f7BA3p)

1. Install Termux from F-Droid or the GitHub releases page
   (github.com/termux/termux-app/releases; the Play Store build is stale).
   Open it once, then:

```
pkg update -y && pkg install -y python openssh curl
python --version
```

2. Tailnet: the Tailscale Android app already joins t90 (100.72.38.3, online
   in tonight's tailnet status). Termux traffic rides that VPN with zero
   setup. Verify from Termux:

```
curl -s http://100.96.161.76:11434/api/tags | head -c 80
```

3. Get the harness. On the DESKTOP run:

```
tailscale file cp tools\consensus_harness.py t90:
```

Accept on t90 (save to Downloads). Then in Termux:

```
termux-setup-storage
mkdir -p ~/gstd/tools
cp ~/storage/downloads/consensus_harness.py ~/gstd/tools/
cd ~/gstd
python tools/consensus_harness.py --host http://100.96.161.76:11434 --models gemma:2b,deepseek-r1:1.5b,qwen2.5:3b-instruct,gemma2:2b-instruct-q5_K_M,qwen-desk:latest
```

`termux-setup-storage` is one-time (grant the storage permission when Android
asks). The `tools` folder rule is the same as bob's: receipts bank relative
to the harness's parent directory.

4. Bank the receipt (zip + scp, same door as bob):

```
cd ~/gstd
tar -czf ~/t90-run.tgz watch/inbox/gstd_perimeter_build_20261010/runs/<ts>
scp ~/t90-run.tgz foste@100.96.161.76:Documents/projects/local_sovereign_agent/watch/inbox/gstd_perimeter_build_20261010/runs/
```

Zero-dependency fallback (the Android Tailscale app cannot push Taildrop, so
if scp auth is unavailable): `cat` the run's summary.json in Termux, select
and copy it, and paste it on the desktop into
`watch/inbox/gstd_perimeter_build_20261010/runs/<ts>.summary.pasted.json`.
The ledger can follow the same way; it is small. Receipts-before-claims is
satisfied the moment the bytes land on the estate.

5. Append the banked-runs table line. Done.

## C. pixel (Android phone, tailnet name pixel-11-pro, 100.79.122.101, already joined; offline 2h at write time, wake it)

This is the coldest vertex: LOOP_CLOSED names the phone run "the final proof
of portability". Same recipe as t90 with two differences:

1. Wake the phone and open the Tailscale app once so it reconnects (its
   address 100.79.122.101 is already in the tailnet from a previous join;
   tonight's status shows it offline, last seen 2h ago). Then install Termux
   and packages exactly as t90 step 1.

2. The phone runs from the BARE tree: no estate LINKS data will exist under
   `~/gstd`, so the harness automatically uses its built-in fixture task bank
   (8 tasks, 8 distinct truths). That fallback is not a guess; it was proven
   tonight from a bare directory tree on the desktop: run
   consensus-20261011T023240Z, exit 0, verdict STRUCTURE, receipts self-banked.

Get the harness the same way (desktop: `tailscale file cp
tools\consensus_harness.py pixel-11-pro:`), then in Termux:

```
pkg update -y && pkg install -y python openssh curl
termux-setup-storage
mkdir -p ~/gstd/tools
cp ~/storage/downloads/consensus_harness.py ~/gstd/tools/
cd ~/gstd
python tools/consensus_harness.py --host http://100.96.161.76:11434 --models gemma:2b,deepseek-r1:1.5b,qwen2.5:3b-instruct,gemma2:2b-instruct-q5_K_M,qwen-desk:latest
```

Bank and table-line exactly as t90 step 4 and 5.

## Laws that hold on every device

- Key law: no seed phrases, no API keys on the devices, ever. The device
  wallets already exist and their mnemonics live only in `contracts/.env` on
  the desktop (gitignored, never printed). A runner device needs ZERO
  credentials: it calls an allowlisted HTTP host and files bytes.
- Closed perimeter: the harness refuses any host outside loopback, LAN
  RFC1918, and Tailscale CGNAT (proven tonight, exit 2). Point it at nothing
  else; nothing else will run.
- Wallet law note (from LOOP_CLOSED): these are TESTNET-ONLY keys, zero real
  value, burnable.

## Banked runs (append one line per device run; no claim without a line)

| device | run_id | consensus_rate | verdict | banked at (estate path) |
|---|---|---|---|---|
| desktop-7c70ksc (paste-line proof, 5 models, defaults) | consensus-20261011T022831Z | 0.8571 | STRUCTURE | watch/inbox/gstd_perimeter_build_20261010/runs/20261011T022831Z/ |
| desktop-7c70ksc (bare-tree single-file smoke, fixtures, 2 models) | consensus-20261011T023240Z | 0.375 | STRUCTURE | bare-tree proof under a temp copy; the identical bytes are the untracked repo file |
