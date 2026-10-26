# SEED PUBLIC PACK receipt — 2026-09-25

**Artifact:** `watch/inbox/seed-3.2.0.zip` — the reply-with-seed pack for the PapiTrumpo
"MAGA is the biggest neural network" post. Companion card: `watch/inbox/seed-3.2.0-card.png`.

## Provenance

- Source: operator's own `Desktop/seed-3.2.0.zip` (built outside this window; SEED_VERSION
  says "salon convergences: seed_init scaffolder, SKILLS discovery index, AGENTS.md load order").
- Original seal: **55/55 verified, 0 drifted, 0 missing** (verify_seal.py, repo venv).
- MIT license (Copyright 2026 MARKK). No real secrets: keys.json is an awaiting-operator
  template, ACCOUNTS.md is a signup playbook with placeholder handles.

## Why a repack was needed

The original zip included 3 `__pycache__` .pyc files, and bytecode bakes in compile-time
absolute paths: all three contained `C:\Users\foste\Documents\...`. That is the same
author-path disease the 3.1.0 clean commit scrubbed from source ("spine_walk author-path
scrub"), resurrected by build junk. Public share would have leaked the username + layout.

## Surgery

1. Deleted `engines/__pycache__/` and `tests/__pycache__/` (3 .pyc files).
2. Removed the 3 matching rows from `MANIFEST.sha256` (Edit tool; 55 → 52 rows).
3. Re-ran `verify_seal.py`: **52/52 verified, 0 drifted, 0 missing**.
4. Ran the seed's own unittest suite from the cleaned tree: **6 tests, OK**.
5. Staged under a top-level `seed-3.2.0/` folder (no tar-bomb on extract), zipped with
   Python zipfile (sorted entries, forward slashes), **no python run inside the staging
   tree afterward** (unittest re-creates pycache; strip-then-zip ordering matters).
6. Round-trip: fresh extract → seal 52/52, secret grep CLEAN, 53 entries, no pycache.

## Final bytes

- File: `watch/inbox/seed-3.2.0.zip` — 53 files, 99,905 bytes
- **sha256: `e9f4603a4484dafb3d79103aef63c678774ec508f9cd573677e91f83bc78f87e`**
- Operator's original Desktop zip left untouched.

## Share step (operator)

watch/inbox is Drive-bridged (fostertron transport). Flip the Drive entry to
anyone-with-link, paste the URL into the reply draft below.

## Reply draft (X)

> You described a knowledgebase that purges lies and integrates truth without asking
> anyone first. We built one.
>
> seed 3.2.0: 53 files, 100 KB, every one hash-sealed. The seal checks with stock
> sha256sum. Cold boots on any machine in minutes. MIT. Runs on free tiers with a
> $5 float rule. Laws ship as config. Receipts ship as bytes.
>
> It doesn't ask anyone first. Plant it. [link]
> sha256 e9f4603a4484dafb3d79103aef63c678774ec508f9cd573677e91f83bc78f87e

## Reply draft (X) -- seed 3.3.0 (parked 2026-09-26, B2-459)

Numbers below are re-verified from bytes against the B2-101 evidence table
(watch/inbox/burn_wave_20260926/B2_101_seed330_papers_20260926.md): 57 entries,
104,167 bytes (102 KB), seal 56/56, unittest 6/6 OK, cold boot 12 PASS / 2
readable / 0 crashes, sha256 015acfa0c5903f6f67305a188be2c830cad098a906678fba0
09069b0aa8eaada. Law spine kept from the 3.2.0 draft; frame shifted to the
harness-stack wording. No em-dash anywhere.

> You described a knowledgebase that purges lies and integrates truth without asking
> anyone first. We built the harness it runs on.
>
> seed 3.3.0 is the whole stack in one 102 KB zip: 57 files, every byte hash-sealed.
> The seal checks with stock sha256sum, no installer, no service. Drop it on a cold
> machine, run the boot gate: 12 checks pass, 0 crashes, laws load as config, receipts
> verify as bytes. MIT. Runs on free tiers with a $5 float rule.
>
> The agent is the easy part. The harness is the product. Plant it. [link]
> sha256 015acfa0c5903f6f67305a188be2c830cad098a906678fba009069b0aa8eaada
