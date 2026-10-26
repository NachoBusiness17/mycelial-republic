# SECRET GATE STEAL ADDENDUM 2026-09-27: purge scan status + interim purge targets

Class: RECEIPT · Writer: zcode seat · Addendum to
watch/inbox/SECRET_GATE_STEAL_LANDED_20260927.md (filed separately to keep the
landed receipt's INDEX seal intact).

## History scan status at addendum time

ALIVE and grinding, not dead: git.exe PID 41628 at 1.69 GB memory running
`git log -p --no-color -U0 --all` over the 6.11 GiB pack, python.exe PID
13164 at 290 MB streaming its stdout through the rule engine. A full-history
diff pass over this repo is a tens-of-minutes-to-hours job; the results file
watch/inbox/secret_gate_results/history_*.json lands on completion and is the
authoritative purge list. (The empty launcher output file was a scare, not a
death: the tool prints only at the end.)

## Interim purge targets (proven tonight, usable before the scan lands)

These carry the operator GO gate: rotate anything live FIRST, strip SECOND.

1. memory/tls/lan.key — PRIVATE-KEY-BLOCK critical, committed since August,
   blob present in .git packs and Mag-backup.git across 39 refs. Rotation
   owed (regenerate the LAN TLS pair), then strip.
2. corpus/library/openai-cookbook/gpt_action_box.ipynb:929 — the
   PRIVATE-KEY-BLOCK the 2026-09-26 run actually recorded (the pack's
   evidence misattributed it to lan.key; both exist, this is the second).
   Harvested corpus material: redact or remove.
3. memory/trajectory/steps.jsonl:1994 — Telegram bot token, DEAD since the
   operator deleted bot 8750925249 (getMe 401 verified 2026-09-27). No
   rotation needed; strip for scanner hygiene.
4. The 19 corpus files carrying the harvested .env dump (B2-73 receipt
   family) — other people's credential material the estate should not
   possess; redact-on-harvest law queued, strip in the same pass.
5. mag/lab_episode.py:117 — OpenAI-shaped literal, probable skill-ID false
   positive, STILL OWED the operator's two-minute read before it joins
   either the strip list or the accepted-baseline list.

## Falsifier

The full history scan may name MORE targets (older paths renamed or deleted
since, secrets in history that no longer exist in the tree). The interim list
above is the tree-proven subset; history_*.json supersedes it on landing.
