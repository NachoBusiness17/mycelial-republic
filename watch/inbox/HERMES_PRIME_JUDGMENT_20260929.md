# HERMES GLM-5.3-PRIME JUDGMENT 2026-09-29

Paid run: z-ai/glm-5.3-prime via inference-api.nousresearch.com (NOUS_SDD_API_KEY, the funded tier). Usage: {"prompt_tokens": 304, "completion_tokens": 6277, "total_tokens": 6581, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 5121, "image_tokens": 0, "audio_tokens": 0}, "cost": 0.0560888, "cost_details": {"source": "openrouter_list", "floor_applied": false, "rate_source": "openrouter_catalog"}}

---

Ordering logic: exposure that compounds hourly first, then the perishable green baseline, then value extraction while the safety net is fresh, then the systemic fix, then verification of claims that are only hours old.

**1. Rotate the xAI key → scrub every history copy → only then snapshot anything.**
- **Why it wins:** It's the only item whose cost of delay grows by the hour, and it's minutes of work. A scraped key doesn't just burn budget — it can get the account killed, which severs the mine's fuel line, which starves every future find. All four other moves assume that account stays alive. Sequencing is the whole point: backing up the recovery pack *before* scrubbing exports the leak off-machine.
- **Probe:** One API call with the old key must 401. A repo-wide plus history grep for the old key string must return only tombstones. Either failing means the rotation is theater.
- **Failure mode:** Rotating at a bad seam — mid-mine-run, or with the old key living in a CI secret, container image, or shell history on another box you didn't grep. The leak survives the rotation.

**2. Freeze the green commit as the recovery pack and ship it off-machine — restore-tested.**
- **Why it wins:** 2,568 hermetic green is a perishable state; the next commit begins the entropy. Tagging and snapshotting now converts a transient milestone into a permanent floor: every future breakage has a known-good restore point. It's also the only move that survives the machine dying. An hour of work against total-loss exposure beats every value-creating move on expected value.
- **Probe:** Restore onto a clean volume, run the suite out-of-repo, count. Anything under 2,568 means the pack is incomplete — fix the pack, not the test.
- **Failure mode:** Backup-as-decoration: shipped, encrypted, never restore-tested. Also snapshotting a dirty working tree so the pack doesn't match the tag, and storing the decryption key on the same machine.

**3. Steal-map the top ~12 finds, one eval each — not all 123.**
- **Why it wins:** Banked finds are decaying inventory: unmapped, they don't compound and go stale as frontier models move. The green suite is what makes a batch landing cheap — regressions surface instantly — so this is the safest 48-hour window you will ever have for it. Mapping all 123 produces shallow noise with eval starvation. And this is where the abliteration capital goes instead: the probe already showed refusals are capability-shaped, so abliterating buys nothing — write the re-raise criteria, archive it, spend zero further.
- **Probe:** Map the single highest-leverage find first, run its before/after eval. If the first three mapped finds move zero evals, the mine is producing decorative text — halt and re-grade the mine before touching find four.
- **Failure mode:** Knowledge theater — finds filed into docs instead of changing runtime behavior. Secondary: find-stacking that quietly erodes suite determinism, so "green" starts meaning luck.

**4. Build the heartbeat; resurrect the renderer as its first customer, not its patient.**
- **Why it wins:** The estate has now fossilized the same way twice — things without cadence die. Hand-fixing the bake once just re-fossels it next month. One scheduler owning the bake, the watchlist poll, the driver drain, and a nightly suite run protects every lane you'll ever add. The renderer is the demo; the cadence layer is the asset.
- **Probe:** Wire the bake to tonight's heartbeat. Tomorrow: bake output exists, heartbeat log shows nonzero duration. If the heartbeat fires and the bake fails, you've converted a silent fossil into a loud scheduled failure — which is the win condition for this move.
- **Failure mode:** Cadence nobody reads — runs posting into a void. The dead-man's switch is non-negotiable: silence must page. Fold in a drain-rate gauge on the driver so runaway spend surfaces as a heartbeat anomaly, not a bank statement.

**5. Injection-test the freshly-wired loops end-to-end, through the MCP bridge.**
- **Why it wins:** "Wired" is a topology claim, not a throughput claim, and both loops landed in the same four-commit burst as everything else. The watchlist is upstream of the mine's replenishment — if it silently yields zero rows, the mine starves while looking alive, and you won't notice for weeks. Routing the injection through the bridge soak-tests all six newly-serving tools in the same motion. Building new lanes on unverified ones is exactly how you got 19 fossils.
- **Probe:** Inject a synthetic statement attributed to a watchlist name; it must surface as a find within one poll cycle. For the market: run N interactions, confirm the ledger is nonzero *and consumed* — a downstream run whose inputs changed. Write-only telemetry passes the first check and fails the estate.
- **Failure mode:** Green on synthetic, dead on real — dedupe keys that collide and drop genuine items, poll windows that miss actual publication cadence, market entries nothing reads.

Deliberate non-moves for these 48 hours: no abliteration beyond its re-raise criteria, no full 123 mapping, no hand-fix of the bake. Moves 1→2 are same-day and strictly ordered; 3 rides the window while the suite is green; 4 and 5 are parallel and cheap.
