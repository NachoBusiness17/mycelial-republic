# GAP ANALYSIS 2026-10-11 — the C0 red ledger + the research project + the moonshot

**Filed by:** L2-Hermes · **Instruments:** the 10-lane dogfood audit (deleg_ad10dba5, 09:08–09:24Z) + direct dogfood pass + 2 lanes run in-window after their children died in transit · **Receipts:** `memory/runs/hermes_jobs/dogfood_20261011/` (per-lane live transcripts) · **Companion:** `watch/inbox/BASECAMP_20261011.md`, lens `memory/runs/corpus_self/lenses/primer.md`
**Method note:** every row names instrument + bytes + owner + one-sitting fill. Nothing here was repaired from this seat; the ledger is owed, not paid.

---

## 0. OUTCOMES FIRST

1. **The verkle chain has been frozen for 29 hours.** `mag/verkle_knot._verify_chain_consistent()` returns `(False, 'tip root mismatch (tip 2b1da0ea599a0755 vs recomputed ae71aee2558f1419)')` and every `_append_verkle_knot_unlocked` refuses — since 2026-10-10T03:52:31Z. The chain tail row is fully self-consistent (recomputed merkle matches; parent chain unbroken; 197/197 knot stems reproduce row hashes). The **tip anchor's root matches nothing recomputable from disk** — no prefix/suffix/dup/reverse, no backup chain, no .bak tip. Count and tail-leaf agree; only the root is foreign. This corrects my boot note: it is NOT the known LAW-064 wrong-unit class — the anchor root is unattributable. The sanctioned heal (`repair_tip_if_consistent`, verkle_audit --auto-heal) would re-derive the tip root only, and is operator-gated. **Owed: operator bless.**
2. **Two live Stripe keys in the estate's own inbox** — `secret_gate --changed` exit 1 BLOCKING: `pk_liv…` (len 42) at `watch/inbox/frontier_olm_adhoc/sweep/raw/art_hf_gsq.html:94` and (len 107) at `watch/inbox/gala_20260925/rung/lanes/_byproducts/glama_servers.html:62`. Excise or rotate; never loosen the hook.
3. **The shared .venv is degrading under the fleet's feet** — `pluggy` and `pip` vanished mid-session (the refold-gate comparator crashed `ModuleNotFoundError`, reading FAIL blind-as-fail while the canary scores the family ALIVE on a crash); `iniconfig`/`certifi` missing per two other lanes. Instrument readings are moment-dependent; sibling lanes mutate the shared venv concurrently.
4. **Two enforcing gates are red on the working tree** — config_seal (4 sealed configs modified; stale at HEAD itself since 10-08) and citation_lint (10 blocking phantom-number rows in changed prose). Any push blocks until re-sealed / claims fixed-or-baselined.
5. **Capability silently lost, not missed:** the `watcher` cage lane has never run since birth 09-14 (string `"30"` vs int `30` — one-char fix); the `afk_orchestrator` (full spend-capable AFK advance stack) has had **zero callers for ~2 months with its gates reading OPEN** — it would spend if invoked; the ghost daemon has been wedged since ~09:06Z; `swarm_health.py`'s `_port_open` positional-arg bug makes 3 live services report dead (spurious-restart risk); the free grok lane is dead (last 10 calls failed); FTS5's daily rebuild is dark; the census carrier is +749 collected past its claim with the 7-day bar expiring ~now.

---

## 1. THE RED LEDGER (ranked; leverage high → low; every row one-sitting fillable)

### Tier 1 — BLOCKING (the climb cannot proceed until resolved)

| # | finding | instrument + bytes | owner | one-sitting fill |
|---|---|---|---|---|
| R1 | **Chain frozen 29h** — tip root foreign, appends refuse | `_verify_chain_consistent` → False; warm_boot --verify exit 1; merkle sweeps over chain + 3 backups + .bak tips all negative | operator (bless) + chain lane | operator GO on `repair_tip_if_consistent`; rows agree with each other so only the tip root is re-derived; then one append re-proves the chain |
| R2 | **Shared .venv degrading** — pluggy/pip/iniconfig/certifi gone; gates crash blind | refold_gate ModuleNotFoundError mid-session; 3 lanes independently report missing deps; canary scores crashed family ALIVE | fleet env lane | restore deps; thereafter instrument runs use ephemeral envs (uv) or a pinned venv guard; add pluggy-present to the canary's family-liveness check |

### Tier 2 — ENFORCING GATES RED (push-blocking)

| # | finding | bytes | owner | fill |
|---|---|---|---|---|
| R3 | config_seal FAIL — 4 sealed configs modified | citation_lint_baseline.json, mates.yaml, mirrors.json, violation_baseline.json all `M`; sibling seat alerting "SEAL STILL BROKEN (4th…)" | config lane | `tools/config_seal.py update --by WHO --note WHY` for the four |
| R4 | citation_lint FAIL — 10 phantom-number rows | MASTER_MICKEY17_V2.md:184; next-window-handoff.md:635 (×2); zknot knots 09-04/06/09/14/17/27 | prose owners | fix or downgrade each claim, or accept by name in baseline |
| R5 | secret_gate FAIL — 2 pk_live Stripe keys in scraped HTML | art_hf_gsq.html:94 (len 42), glama_servers.html:62 (len 107) | inbox hygiene | excise or **rotate** the keys; the files are scrape byproducts |

### Tier 3 — DARK / MISREPORTING ORGANS

| # | finding | bytes | owner | fill |
|---|---|---|---|---|
| R6 | watcher lane never ran since birth | commit 60b1bde7f string `"watcher": "30"`; `_due()` False forever; zero trail rows | lane runner | `"30"` → `30`, restart/seed state |
| R7 | afk_orchestrator driverless 2 months, gates OPEN | run_afk zero callers; offline=true right_size=full; afk_cadence stale since 08-15 | orchestrator | either wire its driver or gate it closed; an open spend-capable orphan is a standing hazard |
| R8 | ghost daemon wedged | :9000 3/3 8s timeouts since 09:06Z; lanes bypass (OpenRouter since 10-03) | services | restart ghost; lanes unaffected |
| R9 | swarm_health positional-arg bug | `_port_open(9000)` vs signature (host,port) → TypeError → 3 live services report dead; health_law spurious-restart risk | health lane | keyword-arg the three calls; add the fixture |
| R10 | grok_free lane dead | dogfood_audit: last 10 calls FAILED (usage.jsonl); grok-Pro unaffected | fleet/burn | diagnose the free-grok dispatch path (keys/endpoint), or formally retire the lane |
| R11 | FTS5 stale + estate_index pointer drift | rebuild --check exit 2 (2.29MB/9,326 rows behind); daily 09:00 START stamp absent; estate_index_compact defaults to retired dashboard path (live master healthy: 1.5M rows, 0 bad, hardlinked) | corpus lane | run the sanctioned rebuild once; point the tool at `watch/ESTATE_INDEX/ESTATE_INDEX.jsonl` via the existing pointer.json |

### Tier 4 — DRIFT / NOISE (the honest tail)

| # | finding | bytes | owner | fill |
|---|---|---|---|---|
| R12 | Census carrier stale | live 5,107 collected / 602 files vs claimed 4,358/518 (+749/+84); 7d bar at expiry; 2 NEW zero-collect files (test_blade_templates, test_bones_adapter); W2 law vs frozen vector mismatch (1 test red) | census lane | refresh the AGENTS.md bullet from a fresh `--collect-only -q` with named landings; re-pin the W2 vector |
| R13 | Inbox writer nonce gaps | 178 fold-order / 170 file-order across 17/133 writers; 3 classes: frozen counters (zcode-sw-08 ×35, zcode-sw-11 ×22, **our own sancho_pid6686 ×9**), md_record_seal read-then-append race (26 dupes), namespace reuse (zcode-seat-20260928: 46 events over 157 holes); any fold rebuild exits 2 on these | shared-surface lane | fix the md_record_seal hook's read-then-append race; retire the frozen-counter writers; fold rebuild then clears |
| R14 | shared_surface validate red | 85 errors + 1 warning: 61 kind-rows in LINKS.jsonl past the B2-28 marker, 6 unknown event keys on writer-less lines, 12 indexed items missing (gala rung lanes), 6 hash mismatches | shared-surface lane | heal the 12 missing + 6 mismatched; declare the LINKS kind policy or migrate the rows |
| R15 | redis client dormant fleet-wide | mag-redis UP 2d healthy; `redis` module missing in host venv + both containers; absent from requirements; verkle_bus runs polling_fallback everywhere | platform | add the dep and exercise pub/sub once, or document the fallback as the design |
| R16 | Flapping/down lanes | elder ~40% fail (sub-1536 vs thinking channel); opencode_4096 down 25 consecutive, sole local_dialogue lane, no failover; overseer.json month-stale (3 retired containers); day_work mirror schedule-blind | lane owners | elder budget bump or thinking-off; opencode lane failover or retirement; overseer regen |
| R17 | Doc drift | compile_seats exit 1 drifted (SEATS.md.new staged, swap pending; elder 'lane-down' NEW, builder/prose/night cured); AGENTS.md fleet body understated (7 containers vs 3); version stamps 66d stale (substance current) | docs lane | swap the recompile; correct the fleet-body line |
| R18 | Burn surface hazards | $231.03/28,553 calls, silent since 10-07; 402-wall math (key-2 ≈$0.16; sonnet-class asks at 24k reserve deterministically 402); re-fire theater: day-1 $18.89/$29.91 was re-fire, A1 45–52× ($20.53) after its deliverable landed; 7 glm-5.3-prime rows unpriced in the current carrier; LEDGER stale since 09-28; Burn247 task DISABLED | burn lane | price glm-5.3-prime; re-fire cap by name; decide Burn247's fate deliberately (it is OFF today — the ledger that would prove either way is dark) |

### The seat's own kifu (recorded because the law says transit deaths are testimony)

This seat fired **four contextless waves** (12 child-dispatches, 6 died at 0.4–0.7s, "waiting for model response") before curing the pattern — the ungated-CreateWorkflow defect in its own hands. Root cause: the seat's dispatch habit sends goal-only briefs under time pressure. The cure applied: the two dead audit lanes were re-run **in-window** (L3 freshness, L8 secrets — both landed, secrets found R5). Lesson for the pack: **a seat under "max concurrency" pressure must treat a brief as part of the dispatch, not an optional context** — and when the brief mechanism itself fails twice, run the work directly instead of retrying it a third time.

---

## 2. THE CONVERGENCE — what the ledger says as one shape

No single row above is exotic; the estate has caught every one of these classes before. What the C0 audit actually measured is this: **the estate's organs are individually well-instrumented, and the failure mode is now the carrying, not the organ.** Every red in this ledger required a judgment seat plus ten parallel lanes plus 75 minutes to assemble — and the estate's own `gap-map` prices a cheap-lane audit at **0 of 3** (route: 24.3% of 2,315). The census carrier shows the lifecycle of an unfollowed ledger: filed 10-04, +749 drifted, bar expiring, WARN-only enforcement. The tip mismatch shows the lifecycle of an unowned root: foreign since the backfill era, invisible on the default warm-boot path. The canary shows the lifecycle of a broken comparator: crashed blind-as-fail, scored ALIVE anyway.

The estate does not need new organs. It needs the **edge that carries each organ's state to the seat that needs it, in the shape they need it** — which is exactly the verdict the primer lens filed an hour earlier (DA-2: "the Primer is bound per boot, not per turn"). The audit is the evidence for the lens, and the lens is the design for the fix.

---

## 3. THE RESEARCH PROJECT (prior-art sweep first — self-steal, per the descent protocol)

**What the estate already owns** (search before build): `gap-map` (frontier-gap pricing per task shape), the gate-canary + census-patrol + drift-dashboard RED patterns, `babelfish` (digest → deterministic RIB), the context pack and rib vault (the pages), the zknot self-steal meter (re-learning rate, 85/1000 7-day, improving), the mickey17 fill-ball loop, and the overnight grokbot find **"route-map memory 25× boot cut"** — the closest prior art to the missing edge.

**Project: THE ATLAS RED-LEDGER — a standing per-boot meters page.** One page, appended to the context pack at boot, carrying the estate's own instrument verdicts as a dated ledger: which gates read red, which lanes are dark, which seams are wedged, which carriers are stale — each row with its instrument, its moment, and its owner. Research legs (each falsifier-bearing):
1. **Pricing leg:** which instrument rows can cheap lanes assemble (census, corpus, queue, lane states — all deterministic) vs which rows must climb to judgment (triage: is this red real or an artifact, like the venv crash)? gap-map's own instrument is the pricer; expect cheap-assemblable ≈ everything except triage.
2. **Artifact-detection leg:** generalize the canary's planted-known-bad pattern into every instrument family: a green reading is only trusted if the instrument also fails on its planted bad. R2/R9 are exactly the failures this leg exists to catch (crash-as-verdict, positional-arg bug).
3. **Budget leg:** the meters page must live inside the pack's character budget — the estate's own history (a 1,200-char budget silently serving 0 of a 2,217-byte objective) is the filed lesson; the page is capped and the deepest rows are pointer-only.
**Falsifier:** if two weeks of the meters page pass without a single seat citing a row it would otherwise have re-derived, the page is decoration and the honest filing says so. **Cost:** $0 for the deterministic legs; judgment leg only where gap-map prices the gap.

## 4. THE MOONSHOT — the per-turn Primer (the DA-2 edge as the summit)

The summit: **make the boot pack a feedback surface.** Every seat's re-learning event, every seam failure, every gate red, every "needed and didn't find" folds into the pack as a dated amendment (amend-never-rewrite) before the next seat boots. The organs exist — pack (pages), zknot (reader history), self-steal meter (learning velocity), dogfood audit (body-sense), gates (reds), lanes (readers) — the moonshot is the single writer that connects them: **the pack-amendment organ.** If it works, the next seat never re-derives what this window paid to learn; the estate's 85/1000 self-steal meter starts falling for the right reason.

Cosmetics of the summit (each already prototyped somewhere in the estate): the C0 red ledger (§1) is the first meters page; babelfish is the amendment compiler; the lens harness is the register discipline; the climb's kifu is the append-only tape of the learning.

**Falsifier, filed in advance (no redefining the summit mid-climb):** after the edge lands, the zknot self-steal meter's "forgot" column (seats re-deriving known lessons) does not fall below 85/1000 within two weeks → the Primer edge is filed FAILED-SUMMIT, as honestly as a win.

---

## 5. PENDING AT FILING

- P1 climb wave (4 parents) still in flight — gate + adversarial children + kifu fold next.
- The census-carrier refresh (R12) is due to the 7-day bar; the 10-04 census expires essentially now.
- Everything in §1 is owed to named owners; this seat holds no fix mandate on any of it.

*The ledger is the basecamp's first artifact. The climb continues.*
