# Essentials pack restore (ESSENTIALS_PACK_<date>.tar.gz.enc)

One encrypted file. Any machine with OpenSSL or Git Bash restores it.

## Decrypt (passphrase is in your password manager / pack key file)

    openssl enc -d -aes-256-cbc -pbkdf2 -in ESSENTIALS_PACK_20260926.tar.gz.enc | tar -xzf -

(Windows with Git Bash: same command. If you only have the .enc and no key,
the pack is worthless: the key lives OUTSIDE the machine on purpose.)

## What is inside

Code (mag, tools, scripts, githooks, roblox, tests), configs + .env (working
keys), docs, queue, state, research, training ledgers, corpus receipts
(steal, founding_law, lore, prose, library), canon podcast transcripts,
memory (briefs, corpus text canon, vault incl. journal pages, burns,
workflows, improve, trajectory, percolator, press, spore seeds), watch/inbox
(receipts, ledgers, seed zip; Mr Pool media excluded, ledger kept).

Excluded on purpose: .git (7.4G history lives in the Drive mirror per
TWO_MACHINE_SYNC_20260919.md when that lands), .venv (rebuildable), .mimosa,
memory/ghost, biography backups, memory/runs debris, all media corpora.

## Boot on a cold machine

    powershell -ExecutionPolicy Bypass -File .\scripts\ensure_venv.ps1
    mag.cmd doctor
    python -m mag.hermes_warm_boot        (use .venv\Scripts\python.exe)
    mag.cmd context-pack

Then read: watch/inbox/RECAP_7D_20260926.md, memory/briefs/latest.md,
queue/todo.md, AGENTS.md.

## Custody law

Three copies minimum, one off the Drive account entirely. The pack is only
as good as the key's home: password manager first, paper second, chat
transcript never as the only copy. Refresh weekly (dispatcher automation)
or after any landmark day.
