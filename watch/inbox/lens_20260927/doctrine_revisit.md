# Doctrine revisit — ribs / memweave / memlance / memlang / driving

- **class:** LENS · **writer:** doctrine-revisit lane (ZCode) · **operator order:** 2026-09-27 "we need to revisit our ribs, memweave, memlance, memlang and driving"
- **method:** every claim below cites a file read this session, in full or in the named part. No summaries trusted. Nothing outside this file was modified.

---

## 1. RIB

**WHAT (its own bytes).** Two rib doctrines live in `memory/rib/`:
- `memory/rib/RIB_DOCTRINE_CANONICAL.md` (2026-08-14): a rib is "a deterministic instruction set, anchored on shared cryptographic primitives"; "the relation (the frozen spec) is what persists; the model is interchangeable; the chain is the ground truth."
- `memory/rib/RIB_MD_RECORD_20260921.md` (newest file in the dir, 2026-09-21): the everything-md law — every durable prompt/receipt/decision is an md file on disk, prompts are filed beside outputs before dispatch, every write gets a register event, records are open-append one-item-never-rewritten, and the law is metered by `tools/md_record_audit.py` ("Prose about compliance is heat").

A third rib meaning is operational: the **frozen/warmed RIB boot unit** — `watch/inbox/FRESH_BOOT_20260926.rib.json` (schema renderman_ask.v1) names `mag/rib_cache.py FROZEN_RIB` as "the precached system prefix. This file is only the tail," matching AGENTS.md's "strong asks = frozen RIB (system+bootloader+manifest+verkle tip)."

**WIRED.** Yes, three ways: (a) `mag/rib_cache.py` FROZEN_RIB is cited as the live system prefix by `FRESH_BOOT_20260926.rib.json`; (b) `tools/seed_rib.py` builds/verifies the seed carrier (`watch/inbox/SEED_RIB_FORMAT_v0_20260926.md` §5); (c) the md-record law's register (`watch/inbox/index_events.jsonl`, 4,437 log lines per `DRIFT_PATROL_20260927.md`) is the tracked-write spine the whole inbox rides on.

**48H-PRACTICE.** The rib energy went to the **carrier**, not the doctrine-card store: QUEUE.md rows B2-180/B2-181/B2-153 (read in `watch/inbox/burn_wave_20260926/QUEUE.md` lines 273-276) landed the SEED-RIB format v0, a seed-mcp server (371 lines, falsifier "cold session … 10/10 COLD JOIN PASS"), and the external steal dig; `RACTOR_PANEL_20260926.md` adjudicated the carrier ("The estate's seed carrier form is decided: the SEED-RIB carrier is a sealed directory", 43 files / 94,789 bytes, `ractor_panel_20260926/seedrib.final.md`). Meanwhile `memory/rib/` itself has **no landing newer than 2026-09-21** (dir listing: newest mtime Sep 21 13:18) — zero rib cards in the burn wave — and the burn wave's QUEUE/ractor practice never writes rib cards; it writes checkbox rows + receipts.

**VERDICT: LOAD-BEARING, with one stale wing.** The rib as portable frozen kernel + its md-record/open-append law is the load-bearing core (every 48h receipt obeys it). The `memory/rib/` doctrine-card directory itself is STALE — the law it declared got absorbed into register/receipt practice and the seed-rib kernel, and new doctrine now lands as inbox receipts instead of rib cards.
**Amendment:** declare the fork on bytes — `memory/rib/` is the historical card store (fold pointer into the seed-rib kernel's doctrine role per `SEED_RIB_FORMAT_v0` §1), and new rib-class doctrine lands as registered receipts; run `tools/md_record_audit.py` (the rib's own meter) to prove the dir is still tracked.

---

## 2. MEMWEAVE

**WHAT (its own bytes).** `.agents/skills/memweave/SKILL.md`: "models perform on STRUCTURES better than on prose describing the same content"; memory is woven as addressable structures riding the RIB kernel as TAIL, never mutating the kernel; each seat loads only the structure it needs. Falsifier: "if prose matches structure, the weave is ceremony — cut it." `mag/memweave.py` (docstring, read) grounds it operationally: decompose → flock parallel cheap pods → consensus → shade seams → build line-by-line → "fold to memory: verkle fold + ledger (the weave persists)." `mag/mem_weave_distributor.py` (docstring, read): generalize doctor-rightsize EVERYWHERE — fold any oversized system into content-addressed consumable pieces. Doctrinal source: `memory/rib/DOCTRINE_MEMWEAVE_20260810.md` (present in dir listing).

**WIRED.** Yes. `mem_weave_distributor` is imported by `mag/steal_tools.py` and `mag/work_register.py` (grep over `mag/`); siblings `gpu_memweave.py`, `grok_weave.py`, `mindweave_eval.py`, `mag/memweave.py` all present in `mag/`.

**48H-PRACTICE.** The law is practiced constantly even where the word is absent: the burn wave's every artifact is a structure (typed QUEUE rows with pointers and falsifiers; `RACTOR_PANEL_20260926.md` cards table; seed-rib entries with roles+seals). The Mickey17 gopher fan-out named in AGENTS.md's gate law is the same decompose/flock shape. No 48h receipt names "memweave" directly, and no fresh MINDSWEAVE-style adversarial eval of structure-vs-prose has rerun.

**VERDICT: LOAD-BEARING** — it is the operating style of the fleet's asks, wired in code, and its falsifier discipline is intact.
**Amendment:** owe one fresh falsifier run (structure-fed vs prose-fed seat on a same-task basis) — the original proof is 2026-08-10 (`RIB_MEMWEAVE_MINDWEAVE_TESTED_20260810.md` era) and the law says unproven laws decay.

---

## 3. MEMLANCE

**WHAT (its own bytes).** `.agents/skills/memlance/SKILL.md`: a fresh operator coinage, interpreted live — "a single, targeted memory thrust across the agent mesh"; procedure AIM → FORGE (one self-true artifact) → THROW (plant where the target's BOOT reads) → WITNESS (unprompted citation, plant_ts/hit_ts) → TALLY (hit-rate). Its own header stamps it "**Unproven until a lance lands and is witnessed**," and its falsifier: "run five lances; if fewer than two produce unprompted citation/enactment, the lance concept is Disputed as steering — it is just filing."

**WIRED.** A DIFFERENT artifact shares the name: `mag/ghost_memlance.py` (docstring, read) is "ghostlance's shape for MEMORY-STATE intelligence" — a deterministic, $0, anti-hallucination memory-state selector (index/select/trace_state/verify over real disk bytes), with callers `mag/agent_corpus.py`, `mag/ask_router.py`, `mag/autonomous_research.py`, `mag/ghost_server.py`, `mag/game_campaign.py`, `mag/frontier_salon.py`, `mag/dogfood_audit.py` (grep). The SKILL's lance procedure itself: **NONE** — no caller, no tool.

**48H-PRACTICE.** Zero lance receipts. Grep for `memlance|plant_ts|hit_ts` across `watch/inbox/` returns only pre-September-era files (CODEX_TASK_003_20260901, FLEET_KNOWLEDGE_GRAPH_20260917, SKILL_FORGE_20260918); the apparent hits in 09-26/27 files (`BURN_third-way-game_20260927_c.md`, GAMEDIG veins) are substring false positives — "ba**lance**" in "economy balance design" and "free**lance**" (verified by line-level grep: no memlance context). The skill's own witness ledger is empty.

**VERDICT: STALE (as steering) + NAME COLLISION.** The skill-coinage is an untested interpretation still marked unproven by its own bytes, with no landed lance ever; `ghost_memlance.py` is separately alive and wired but is a grounding selector, not the lance.
**Amendment:** either run the five-lance falsifier (five WANTS/chan-row seeds, witness ledger with plant_ts/hit_ts) or demote the coinage; and disambiguate the name — rename the skill's concept or the module so "memlance" means one thing.

---

## 4. MEMLANG

**WHAT (its own bytes).** `mag/memlang.py` (docstring, read in full head): "the shared-verkle-invariant TRIGGER LANGUAGE" — a COMPACT BINARY TOKEN (magic `MEM1`, version, opcode, 32-byte sha256 anchor into shared verkle state, params) that triggers an action without spelling the instruction; "only an agent holding the shared map can decode it." Schema memlang.v1, CLI `python -m mag.memlang compile|decode|resolve|trigger`. `mag/compiler_lang.py` (head, read) expands it: "memlang -> a COMPACT BINARY TOKEN (the language expands: new anchor+spec)" at line 141-149. NOTE: memlang does **not** live in `.agents/skills/chan/SKILL.md` — chan is the imageboard play face (`python -m mag.chan`, soil `watch/room.jsonl`), no memlang content; the skill-level references are `.agents/skills/memweave/SKILL.md` ("feed STRUCTURES (memlang), not prose") and `.agents/skills/frontier-researcher/SKILL.md`.

**WIRED.** Yes, broadly: `from mag import memlang` / compile_token callers include `mag/compiler_lang.py`, `mag/ghost.py`, `mag/error_healer.py`, `mag/ecosystem_surface.py`, `mag/attractor_tools.py`, `mag/bernaise.py`, `mag/gpu_memweave.py`, `mag/mem_ollama.py`, `mag/partner_puppet.py` (grep over `mag/`+`tools/`).

**48H-PRACTICE.** No burn-wave receipt in the 48h window exercises a memlang token (the steering/seed-rib/census receipts read this session never mention one). The wiring is historical-structural, not currently firing in receipts.

**VERDICT: LOAD-BEARING in code, TERMINOLOGY DRIFT in docs.** The module is real, imported, and versioned; but the skill prose uses "memlang" loosely to mean "addressable structures," which is memweave's law, not the token language — two meanings under one word.
**Amendment:** pin the word: memlang = the memlang.v1 binary token language (mag/memlang.py); edit the memweave skill's frontmatter wording at next touch to say "structures (memweave law)" instead of "(memlang)", and land one fresh roundtrip receipt (`python -m mag.memlang roundtrip`) to prove the trigger path still fires on this chain.

---

## 5. DRIVING (steering)

**WHAT (its own bytes).** The current doctrine is the **drift-pair law**, canonized in `watch/inbox/BURN_steering-theory_20260927.md`: `tools/drift.py` (2026-09-18) is "the verdict organ" — verdicts VACUOUS/ALIGNED/DRIFTING/INVERTED/INSUFFICIENT (+ FRAGILE-ALIGNED stamped downstream by `drift_pairs_stamp.py`'s aging guard, per drift.py docstring read in full) computed as corr(delta-M, delta-R); law string: "a rate metric answers 'is it moving'; only corr(delta-M, delta-R) answers 'is it moving north'." `tools/probe20_run.py` (2026-09-26, docstring read) is "the series runner for the steering drift pairs": append-only cycle rows in `memory/runs/probe20/`, noise floor 0.1 closing the one-flip VACUOUS escape, GBNF TRUE|FALSE grammar against a local llama-server in --live. Canon pairs: A = verdict-token logprob margin vs correct/20; B = escalate-rate vs overturn-rate. The receipt's own steal line: "Any future steering claim that names no drift pair is vacuous by this receipt." Earlier steering surfaces (`RACTOR_STEERING_SURFACE_20260922.md`, `ELDER_SANCHO_STEERING_SURFACE_20260922.md`, `HERMES_STEERING_20260907.md` — present in inbox listing) predate this law.

**WIRED.** Yes at the instrument layer: `tools/drift.py`, `tools/probe20_run.py`, `tools/drift_pairs_stamp.py`, `tools/drift_dashboard.py` all exist in `tools/` (listing); `watch/inbox/PROBE20_steering_v1.jsonl` carries the version-hashed 20-task registry. NOT wired at the data layer: `memory/runs/probe20/` **exists and is empty** (ls this session: created Sep 26 17:52, zero files), and `--live` "exits 3 LIVE-UNREACHABLE" with "no fallback margin, no synthetic rows" (BURN_steering-theory_20260927.md evidence).

**48H-PRACTICE.** Advanced, on the instrument side, honestly: `BURN_steering-theory_20260927_b.md` ("live instrument readout", verdict green) fired drift_check on real `memory/runs/gps_50/raw.jsonl` bytes (two DRIFTING verdicts with real correlations 0.1807/0.4538 — then correctly disqualified as non-findings since answer_chars is not a truth referent), confirmed the runner's noise-floor override fired exactly as pre-registered, and closed with the self-indictment: "the fleet currently has a verified needle with no map rows under it." So the 48th-hour practice *advanced the doctrine and contradicted nothing* — while leaving the doctrine's actual subject (real steering series) uncollected. (Distinguish `DRIFT_PATROL_20260927.md` — that is the fold-integrity cron, a different drift, read to confirm.)

**VERDICT: LOAD-BEARING doctrine / PRACTICE GAP.** The law is fresh (canonized 09-26/27), byte-verified, and falsifiable — but zero real cycle rows exist, so no steering claim in the fleet can currently satisfy the law it just adopted.
**Amendment:** collect the first real pair-A rows — bring up the local llama-server, run `probe20_run.py --live` for ≥5 cycles (min_points 5 per the registry meta row), and file the first drift-pair verdict receipt; until then every "we are steering" statement is, by the fleet's own new law, vacuous.

---

## Verdict roll-up

| artifact | verdict | one-line amendment |
|---|---|---|
| RIB | LOAD-BEARING (kernel+md-law); `memory/rib/` card store STALE | Declare the fork: rib cards fold into seed-rib/register practice; run md_record_audit to prove tracking |
| MEMWEAVE | LOAD-BEARING | Owed: one fresh structure-vs-prose falsifier run (proof is 48d old) |
| MEMLANCE | STALE as steering (skill untested, zero lances); `ghost_memlance.py` separately WIRED | Run the five-lance falsifier or demote; fix the name collision |
| MEMLANG | LOAD-BEARING in code / terminology drift in docs | Pin memlang = the memlang.v1 token language; land a roundtrip receipt |
| DRIVING | LOAD-BEARING doctrine / PRACTICE GAP (zero series rows) | Fire `probe20_run.py --live` ≥5 cycles and file the first real drift-pair verdict |

**Single most important amendment:** collect the first real drift-pair rows (driving, practice gap) — the steering-theory receipts themselves proved the instrument pair honest and then named the hole: "a verified needle with no map rows under it"; filling it is the only amendment that converts this week's doctrine from law into measurement.
