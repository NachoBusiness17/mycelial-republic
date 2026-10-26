# T90 IGNITION KIT - Termux bootstrap, then the desktop drives everything

**State:** t90 (100.72.38.3, Android tablet) is alive on the tailnet at 15ms RTT but has ZERO listening doors (probed 22/2222/8022/5555/11434 - all closed). Termux is the door; everything after the paste is remote-driven from the desktop.

**Step 1 (one-time, hands on the tablet): install Termux from F-Droid** (NOT the Play Store version - it is dead). Link: https://f-droid.org/en/packages/com.termux/ - install, open it once, grant storage if prompted.

**Step 2 (one paste into the Termux terminal on the tablet):**

```bash
pkg update -y && pkg install python openssh -y
mkdir -p ~/.ssh ~/gstd
echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINvEjDBH+8nNAUYWVpdpCGEKqWSjpZEveWL/MQpEZk72 estate-to-bob' >> ~/.ssh/authorized_keys
sshd
echo IGNITED - sshd on port 8022
```

That installs python + sshd, installs the estate's public key, and starts the ssh door (Termux sshd = port 8022). The same keypair the estate already holds (estate_to_bob) authenticates - no password setup needed.

**Step 3 (automatic, desktop-driven):** tell the estate "t90 pasted" - from then on the desktop drives the rung remotely:

```
ssh -i C:\Users\foste\.ssh\estate_to_bob -p 8022 t90@100.72.38.3 "<commands>"
```

- ship the harness: `scp -P 8022 -i ...estate_to_bob tools\consensus_harness.py t90@100.72.38.3:gg/harness.py` (Termux home = /data/data/com.termux/files/home)
- run the battery: `ssh ... "python gg/harness.py --host http://100.96.161.76:11434 --models gemma:2b,deepseek-r1:1.5b,qwen2.5:3b-instruct"` - zero models, zero credentials on the tablet; it calls the desktop's ollama over the tailnet and files bytes.
- pull the summary, settle through v6: T90's wallet (UQBrE6BR...BA3p, 0.49 TON, reputation 0 -> 1) earns its first 25 GSTD and the lattice flips the third cell.

**Why the tablet matters:** it is the portability proof. A phone-class device running certified consensus work for on-chain payment is the demo that the Republic runs anywhere - the family box proves it at home; the tablet proves it in a pocket.

**Falsifier:** the kit dies if the paste errors (F-Droid Termux version mismatch, storage prompt hangs) - in which case the error text comes back to the estate and the kit gets corrected, appended here, same law.
