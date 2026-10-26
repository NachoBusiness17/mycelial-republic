# BOB IGNITION KIT - one paste on bob opens the remote door

**The door:** bob's SSH (port 22) is open, the estate's keypair (`estate_to_bob` / `estate_to_bob.pub`) is cut and the private half lives on the desktop. The ONLY missing piece: bob's sshd doesn't know the public key. Windows OpenSSH on Windows checks `C:\ProgramData\ssh\administrators_authorized_keys` for administrator accounts (a普通 user's `~\.ssh\authorized_keys` is ignored for admins - the classic Windows sshd gotcha).

**The one paste (admin PowerShell on bob):**

```powershell
$key = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINvEjDBH+8nNAUYWVpdpCGEKqWSjpZEveWL/MQpEZk72 estate-to-bob'
$authKeyPath = 'C:\ProgramData\ssh\administrators_authorized_keys'
Add-Content -Path $authKeyPath -Value $key
icacls $authKeyPath /inheritance:r /grant 'SYSTEM:F' /grant 'BUILTIN\Administrators:F'
Restart-Service sshd
```

Then from the desktop, the door is tested with:

```
ssh -i C:\Users\foste\.ssh\estate_to_bob foste@100.125.103.60 "echo door-open && hostname"
```

(username = bob's Windows account name - try `foste` first, matching the desktop; the paste above must be run in an ADMIN PowerShell on bob.)

**After the door opens, the ignition sequence (from the desktop, ssh-driven):**

1. `ssh -i ~/.ssh/estate_to_bob foste@100.125.103.60 "python --version"` - if missing: `winget install Python.Python.3.12` (or the paste-line fallback).
2. Copy the harness: `scp -i ~/.ssh/estate_to_bob C:\Users\foste\Documents\projects\local_sovereign_agent\tools\consensus_harness.py foste@100.125.103.60:C:/Users/foste/consensus_harness.py`
3. Run the battery remotely: `ssh -i ~/.ssh/estate_to_bob foste@100.125.103.60 "python C:/Users/foste/consensus_harness.py --host http://100.96.161.76:11434 --models gemma:2b,deepseek-r1:1.5b,qwen2.5:3b-instruct"` - bob needs ZERO models and ZERO credentials: it calls the desktop's ollama over the tailnet and files bytes. (The coldest-vertex law: the runner is headless.)
4. The run's summary lands back via `scp`, the drain credits bob's wallet (UQAW3wO8...), bob's reputation accrues on-chain, and the lattice flips BOB: COLD -> HOT.

**Falsifier:** the door claim dies if the paste runs and the ssh still says Permission denied - in which case bob's sshd is running a different authorized_keys path (check `sshd_config` `AuthorizedKeysFile` on bob) and the kit gets corrected, appended here, same law.
