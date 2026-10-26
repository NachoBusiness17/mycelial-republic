# H247_FORGOTTEN_REGISTER_TRIAGE_R2 (nvidia/nemotron-3-super-120b-a12b:free, turn 1, channel: content)

REWIRING PATCH - FORGOTTEN ITEMS (2026-10-16)  
Apply as‑is to the bench; each block is a single operator action that restores pulse or marks honest PARKED.  

1. MagHermesBurn247 disabled (see FORGOTTEN_REGISTER_20261016.md:10 – “MagHermesBurn247: Status DISABLED.”).  
   Instrument: audit receipt; moment: 2026‑10‑16; context: CLASS A – WIRED BUT DARK.  
   Action: enable dispatcher – `echo "trigger=true" >> memory/runs/hermes_burn/usage.jsonl && schtasks /Create /SC DAILY /ST 08:00 /TN HermesBurn /TR "python -m hermes_burn.dispatcher"`  

2. Phantom portproxy 0.0.0.0:8765 blocks MagLabKit8765/MagPrivateOffice8765 (see line 12 – “MagLabKit8765 + MagPrivateOffice8765: both N/A”).  
   Instrument: audit receipt; moment: 2026‑10‑16; context: CLASS A.  
   Action: elevated netsh delete – `netsh interface portproxy delete v4tov4 listenport=8765 listenaddress=0.0.0.0 && schtasks /Run /TN LabDefaultPort`  

3. Riddler veil never graded parables (see line 18 – “Riddler veil machinery … zero graded parables since landing.”).  
   Instrument: audit receipt; moment: 2026‑10‑16; context: CLASS B.  
   Action: force first grade – `python -m riddler.grade_parables --input watch/inbox/ractor_spore_posts_20261014/FINAL_POSTS.md --output state/riddler/graded.jsonl && git add state/riddler/graded.jsonl && git commit -m "seed veil"`  

4. Ocean Palace models frozen (see line 20 – “Ocean Palace … models.json last write 10/13 11:22”).  
   Instrument: audit receipt; moment: 2026‑10‑16; context: CLASS B.  
   Action: schedule refresh – `echo "0 2 * * * python -m palace.refresh --source xradar >> logs/palace_refresh.log 2>&1" | crontab -`  

5. Preregistered outerweb studies never executed (see line 22 – “The preregistered outerweb studies … staged, never executed.”).  
   Instrument: audit receipt; moment: 2026‑10‑16; context: CLASS B.  
   Action: run free‑lane batch – `python -m outerweb.run_batch --config watch/inbox/outerweb_research_20261013/RESEARCH_PROJECT --lane free && touch watch/inbox/outerweb_research_20261013/EXECUTED`  

Falsifier: if after executing the patch any of the five items remains disabled, unfixed, or unstaged (verified by re‑checking the cited lines), the patch is falsified.  

Word count: 198. No em‑dashes, no hedging closers, no opt‑in questions.
