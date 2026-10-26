# GSTD COMPUTE POOL: the three-body DePIN

## What this is

The estate's own machines pooled into a shared compute network. The water
computer spec made real: three tanks (desktop, laptop, phone), one pipe
(tailscale mesh), one dispatcher (the desktop), and the law that unused
CPU-hours are Starved events.

## The bodies

| body | tailnet IP | CPU | RAM | runs | status |
|---|---|---|---|---|---|
| desktop-7c70ksc | 100.96.161.76 | AMD Ryzen 7 3800XT 8c/16t | Ollama (17 models) + main seat | ONLINE |
| bob (laptop) | 100.125.103.60 | TBD (need specs) | TBD | ZCode, Python | ONLINE but SSH needs key auth |
| pixel-11-pro | 100.79.122.101 | Tensor G5 8c | 16GB+ | Termux + Python (needs install) | ONLINE but no SSH server |

## Setup (10 min per body, one time)

### Bob (laptop)
1. On the desktop: ssh-keygen -t ed25519 (if no key exists)
2. Copy the pubkey to Bob: type %USERPROFILE%\.ssh\id_ed25519.pub | ssh bob@100.125.103.60 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
3. Test: ssh bob@100.125.103.60 "echo connected && nproc"

### Pixel 11 Pro
1. Install Termux from F-Droid (not Play Store - F-Droid has the current version)
2. In Termux: pkg update && pkg install openssh python
3. In Termux: mkdir -p ~/.ssh
4. Copy the desktop's pubkey: from the desktop, run:
   type %USERPROFILE%\.ssh\id_ed25519.pub | clip
   then paste into Termux: echo "<paste>" >> ~/.ssh/authorized_keys
5. In Termux: sshd (starts the SSH server on port 8022)
6. Test from desktop: ssh -p 8022 100.79.122.101 "echo connected"

## The dispatcher

Once both bodies accept SSH, the desktop routes work units:

- EXTRACTION jobs -> whichever body has the lightest load
- SUMMARIZATION jobs -> the desktop (biggest model)
- CLASSIFICATION jobs -> the Pixel (fast, low-power, always with you)
- CODE REVIEW -> Bob (if it has a bigger CPU)
- FALLBACK -> desktop local (if no remote body is reachable)

## What this enables

Three CPUs pooling into one compute budget. The laptop processes salons
while the desktop runs the mine. The Pixel classifies drift pairs while
you walk around. The water computer spec: three tanks, one pipe, no
Starved events because the dispatcher routes around dead bodies.
