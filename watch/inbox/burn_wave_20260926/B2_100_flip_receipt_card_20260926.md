# B2-100 post-flip receipt card - 2026-09-26 (TEMPLATE, NOT EXECUTED)

Status: EXECUTION OPENED BY B2-447 (2026-09-26T23:0xZ). The burn-wave GO IS on file (watch/inbox/OPERATOR_GO.jsonl 2026-09-26T19:39:00Z, gate burn-wave-20260926); a seed-flip-specific GO is NOT separately on file, and step 3 (browser upload signed in as fostertron@gmail.com, share Anyone-with-the-link) is OPERATOR-HANDS-ONLY: no lane may perform it. E0 re-run and matched. E3-E8 remain unrun (they require the drive_file_id that only exists after the operator upload). Fields below stay <FILL> until their command's real output exists. No fabrication. The five sections below are the fixed receipt sections; this same file becomes the real receipt when the <FILL> fields carry real command outputs.

## Verdict

- flip_state: NOT_EXECUTED (template filed 2026-09-26T18:39:24Z; the [x] on the B2-100 board row names THIS template landing, not a flip)
- pre_flip_hash_gate: e9f4603a4484dafb3d79103aef63c678774ec508f9cd573677e91f83bc78f87e (re-run by B2-447 at execution-open time, 2026-09-26T23:05Z window: output equal, gate green)
- operator_go: PARTIAL. Burn-wave GO on file: watch/inbox/OPERATOR_GO.jsonl row {schema operator_go.v1, ts 2026-09-26T19:39:00Z, gate burn-wave-20260926}. Seed-flip-specific GO: NOT on file. Operator browser step (B2-23 card steps 1-4): NOT performed (operator-hands-only). E2-E8 therefore never run, per this card's own gate.
- flip_executed_at: <FILL:UTC time, drive.google.com, signed in as fostertron@gmail.com>
- drive_file_id: <FILL:the URL segment after /d/>
- download_sha256: <FILL:E4 output; MUST equal e9f4603a4484dafb3d79103aef63c678774ec508f9cd573677e91f83bc78f87e>
- curl_status: <FILL:HTTP code printed by E3; expect 200>
- manifest_check: <FILL:E5 tail; expect 52 OK>
- verdict_after_all_pass: LANDED, flip proof complete, Drive URL row registered in watch/inbox/INDEX.json, shipped bytes proven unchanged in transit, X reply link cleared to paste.

## Evidence

Local bytes verified against the shipped seal BEFORE this template was filed, by this lane, on 2026-09-26:

    E0  .venv\Scripts\python.exe -c "import hashlib;print(hashlib.sha256(open(r'watch\inbox\seed-3.2.0.zip','rb').read()).hexdigest())"

    E0 actual output: e9f4603a4484dafb3d79103aef63c678774ec508f9cd573677e91f83bc78f87e

That output equals (a) the sha256 on the watch/inbox/INDEX.json seed-3.2.0.zip row (E9F4603A... uppercase form), (b) watch/inbox/SEED_PUBLIC_PACK_20260925.md line 35, and (c) the hash gate named in the B2-23 card Pre-flight. Cross-checks already on file: INDEX seed row class artifact; card png renders seal 52/52; pack manifest 52/52 verified, 0 drifted, 0 missing.

Everything below this line is PREPARED, NOT RUN.

## Work done

Post-GO execution order, exact commands. Scratch files stay out of watch/inbox and are never registered.

1. GO gate: re-confirm the operator GO exists and note where it is recorded (<FILL:pointer>). No GO: stop here, nothing below runs.
2. Hash gate, re-run E0. Output must equal e9f4603a4484dafb3d79103aef63c678774ec508f9cd573677e91f83bc78f87e. Any other output: STOP, file as owed, never upload different bytes, never re-zip.
3. Operator browser flip per watch/inbox/burn_wave_20260926/B2_23_seed_flip_card_20260926.md steps 1 to 4: upload ONLY watch\inbox\seed-3.2.0.zip (My Drive, New, File upload); Share, General access Anyone with the link, Role Viewer; copy link; record drive_file_id from the /d/ segment.
4. Anonymous proof (fetch as a signed-out third party):
       E3  curl -sL -w "HTTP %{http_code}\n" "https://drive.google.com/uc?export=download&id=<drive_file_id>" -o seed_flip_check.zip
       E4  .venv\Scripts\python.exe -c "import hashlib;print(hashlib.sha256(open('seed_flip_check.zip','rb').read()).hexdigest())"
       E5  deep check named by the B2-23 card: unzip seed_flip_check.zip, run sha256sum -c MANIFEST.sha256 inside seed-3.2.0/ (expect 52 lines OK)
   seed_flip_check.zip is scratch evidence for E4 and E5 only: never placed in watch\inbox, never INDEX registered, never erased-before-filing its outputs into this card.
5. INDEX Drive URL row registration (appends the register event and refolds INDEX.json in one step; last register wins so the seed-3.2.0.zip row stays bound to the real local bytes and the Drive url rides in the row purpose):
       run from watch\inbox (the fold's inbox-relative law, B2-157 check: a repo-relative watch\... path is outside-dropped; this lane's seq 1790447985229758001 and 1790447985229758002 were lost exactly that way and stand as log residue, corrected at 1790447985229758005 and 1790447985229758006)
       E6  cd watch\inbox && node ..\..\scripts\index_fold_host.mjs add seed-3.2.0.zip artifact "B2-100 flip proof: Drive mirror of shipped bytes, url https://drive.google.com/file/d/<drive_file_id>/view?usp=sharing, anonymous download sha256 <E4 output> equal to local seal, curl <E3 code>, manifest 52 OK, <UTC ts>"
   Run with INDEX_WRITER=B2-100-flip-receipt (or your lane writer) from that directory. Then confirm the row: grep the url into watch/inbox/INDEX.json.
5.5 POST-POSTING RE-CHECK (B2-448, 2026-09-26): the flip receipt is not final
       until the posted link is re-proved as a fresh anonymous download AFTER the
       X reply (or any surface) carries it - a silent Drive-side replace would
       otherwise serve bytes that no longer match the shipped seal while this
       card still says LANDED. Named step, output filed in this card:
       E5.5a  wait at least one minute after the share-state change, then
              curl -sL "https://drive.google.com/uc?export=download&id=<drive_file_id>" -o seed_recheck.zip
       E5.5b  .venv\Scripts\python.exe -c "import hashlib;print(hashlib.sha256(open('seed_recheck.zip','rb').read()).hexdigest())"
              must print e9f4603a4484dafb3d79103aef63c678774ec508f9cd573677e91f83bc78f87e
              (the shipped seal); file the output in this card next to E4.
       E5.5c  a delta hash is an INCIDENT: the posted link must be deleted or
              re-uploaded and this card amended with the delta named - never
              silently refreshed.
       Standing probe arm (optional, if the estate wants continuous proof):
       run E5.5a-b on a weekly schtask and file deltas the same way; not
       scheduled at landing because no link existed yet (B2-448 measured).
6. LEDGER row via .venv python json.dumps (one line, append):
       E7  .venv\Scripts\python.exe -c "import json;from datetime import datetime,timezone;row={'ts':datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),'slug':'B2-100-seed-flip-receipt-20260926','verdict':'<FILL:one sentence naming drive_file_id, download_sha256, curl_status>','landing':'watch/inbox/burn_wave_20260926/B2_100_flip_receipt_card_20260926.md','one_line':'<FILL:what the proof proves>'};f=open('memory/burns/LEDGER.jsonl','a',encoding='utf-8');f.write(json.dumps(row,ensure_ascii=True)+'\n');f.close()"
7. Fill every <FILL> in this card with the real outputs of E0, E3, E4, E5, E6, E7. No fabrication: a field without its command output on disk stays <FILL>. Then surface validate:
       E8  .venv\Scripts\python.exe -m mag.shared_surface validate
8. Board: append the flip landing note to the B2-100 row per the shared-file claim law (CLAIM line first, re-read, anchored edit) and self-feed 1 to 3 briefs UNCHECKED.

LEDGER row already filed for the TEMPLATE landing (this card, not the flip), slug B2-100-flip-receipt-template-20260926, timestamp 2026-09-26T18:39:24Z band.

## Falsifier

- This card falsifies itself if any <FILL> is found replaced while the naming command's output does not exist: that is fabrication, prune and re-file.
- download_sha256 differs from e9f4603a4484dafb3d79103aef63c678774ec508f9cd573677e91f83bc78f87e: bytes mutated in transit, STOP, do not paste the X reply link, file per the B2-23 card rollback (Share back to Restricted) and re-file this receipt.
- curl_status not 200, or E4 reads a sign-in HTML page instead of zip bytes: the share is not anonymous, fix General access and re-run E3 to E5.
- manifest_check not 52 OK: the Drive object is not the shipped pack, rollback to Restricted and re-upload the exact local bytes (never a re-zip).
- A flip landing claimed anywhere while operator_go is still <FILL>: the B2-238 disease, revert the claim and cite this line.

## Bibliography closed

watch/inbox/burn_wave_20260926/B2_23_seed_flip_card_20260926.md; watch/inbox/SEED_PUBLIC_PACK_20260925.md lines 34 to 41; watch/inbox/INDEX.json seed-3.2.0.zip row; watch/inbox/index_events.jsonl with scripts/index_fold_host.mjs (add, rebuild, verify; INDEX_WRITER env; last register wins); configs/events_key_schema.json (url key already registered, closed vocabulary); memory/burns/LEDGER.jsonl (row shape per the B2-15 pattern: ts, slug, verdict, landing, one_line, json.dumps ensure_ascii); watch/inbox/burn_wave_20260926/QUEUE.md header law block (claim law, self-feed law, B2-238 disease); watch/inbox/seed-3.2.0.zip bytes (E0 output above); self-fed brief B2-425 (canonical operator-GO surface).
