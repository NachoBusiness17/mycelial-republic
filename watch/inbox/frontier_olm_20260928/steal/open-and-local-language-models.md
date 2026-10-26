# Steal card: open-and-local-language-models (round 2 revision, 2026-09-29)

Round-2 changelog (defects fixed per review):
1. The 97,865-row scrape is now cited instead of asserted: watch/inbox/frontier_olm_20260928/lens/corpus.md:15, five-way breakdown sums exactly (72,329 + 14,468 + 5,297 + 4,118 + 1,653 = 97,865). The sibling sweep had marked the figure OWED-unlocated (watch/inbox/frontier_olm_20260928/sweep/open-and-local-language-models-arxiv.md:70 and :107); this citation resolves that debt.
2. The estate holding is credited and the false claim withdrawn: watch/MODEL_VAULT_MANIFEST_20260831.md already holds the model-license law for vault rows and already tiers the fleet. The new work is scoped to runtime-config wiring plus quantizer propagation.
3. The probe is rescoped to named files and the full declared roster (round 1 covered 3 models; the rosters declare 5 distinct tags plus 2 more declared models).
4. The overlap claim is restated against a fresh re-run with named exclusions; round 1's blanket zero-hit line is corrected.

## The find

The Register, 2026-09-15, "Open weights are not open source: Why AI's favorite label is under dispute"
https://www.theregister.com/columnists/2026/09/15/open-weights-are-not-open-source-why-ais-favorite-label-is-under-dispute/5295436

Authorship (Steven J. Vaughan-Nichols) and the standfirst quote verified live by the round-2 reviewer's fetch. This card's own WebFetch (2026-09-29) verified the quote verbatim: "Downloading a model is increasingly easy. Understanding how it was made, or changing a system at its root, is another matter"

Verified against the live article (WebFetch, 2026-09-29):
1. Bruce Perens denounced the OSAID in 2024, later calling it "not Open Source" and accusing the OSI of "Openwashing".
2. Bradley Kuhn (Software Freedom Conservancy) and Richard Fontana (Red Hat) called for the OSAID to be repealed.
3. Linux Foundation's Mike Dolan submitted the OpenMDW (Open Model, Data, and Weights) license to the OSI; contributors listed from Amazon, Meta, IBM, Microsoft, Nvidia.

OWED: whether OSI approved OpenMDW since submission. OWED: per-tag upstream mapping of ollama tag gemma4:latest (configs/seat_playbook.yaml:19); the vault tiers the Gemma family as a family but the tag-to-upstream mapping is not re-verified. OWED: license text of nomic-embed-text, the one roster model the vault does not cover.

## Overlap (restated, re-run 2026-09-29, exclusions named)

- OpenMDW: 2 tracked-file hits, both this workflow's own output (memory/trajectory/steps.jsonl; watch/inbox/frontier_olm_20260928/sweep/open-and-local-language-models-hn.md). Perens: the same 2.
- OSAID: 10 hits, the same 2 textual plus 8 binary or base64 coincidences (catalog/receipt_fts.sqlite, dashboard/static/bad_apple_field.html and its deploy/dist/site copies, je5.txt, memory/corpus/ai_canon/chapters/dlb_representation.html, watch/inbox/bad_apple/frames_embed.txt).
- The generic phrase "open-weight" matches 111 tracked files, 85 after pathspec-excluding this run's two artifact trees (watch/inbox/frontier_olm_20260928, memory/trajectory). The phrase is pre-existing estate vocabulary (watch/MODEL_VAULT_MANIFEST_20260831.md, watch/inbox/ENGRAM_OPEN_WEIGHTS_20260911.md, memory/steal/HF_VS_SELF_VS_LEAKED_20260810.md all match).
- Novelty is therefore precise: the OSAID-denunciation and OpenMDW-at-OSI licensing frame is new; the words "open weights" are not. Round 1's "all four greps zero hits" is corrected: it was true for OpenMDW/OSAID/Perens at run time against the then-tracked tree, but the open-weight term printed nothing in round 1 only because that compound command's output was partially eaten by shell mangling; today's re-run of the same grep matches 111 files. The frame-level novelty claim survives; the blanket phrasing is withdrawn.

## The estate already holds the law (round-2 correction)

Archival law on file: watch/MODEL_VAULT_MANIFEST_20260831.md:3-5 states "License recorded per row"; :23 defines passports as identity, license, and hash per model; :48 states "A copy without its hash and license is not archival, it's hoarding" over models.jsonl passport fields. Fleet tiers on file: :11 rows Qwen2.5 family (0.5B to 32B incl. coder) as Apache-2.0, with its Why column mapping the estate's ollama qwen-desk and 2.5-coder lanes into that row; :12 rows Gemma family (2B/4B desk variants) as "Gemma Terms (redistributable)", janitor lanes always-on. Acquisition law on file from this same sweep: sweep/open-and-local-language-models-arxiv.md:74 concludes license text must be read per release, not per family, with a quantcheck-style acceptance gate for pulled GGUFs.

What is genuinely missing, all re-run 2026-09-29:
- Runtime configs: `git grep -in "license" -- configs/lanes.yaml configs/lanes_vast_rtx8000.yaml configs/seat_playbook.yaml configs/lora_pipeline.yaml configs/improve.yaml` exit 1, zero hits. The running fleet has no tier receipt at the point of use: configs/lanes.yaml:31-40 assigns clerk/router/orchestrator/voice to gemma:2b, desk_orchestrator/desk_conductor/critic/biographer to qwen-desk:latest, worker to qwen2.5-coder:7b, embed to nomic-embed-text; configs/lanes_vast_rtx8000.yaml:11-16 declares the second roster adding qwen2.5:32b. 17 files under configs/ match gemma|qwen|ollama by content (`git grep -ilE "gemma|qwen|ollama" -- configs | wc -l` returned 17).
- Quantizer propagation: `grep -ic "license"` over tools/thought_quantizer.py, mag/context_pack.py, mag/verb.py returned 0, 0, 0. Compiled rows in memory/corpus/quantized_thought/ carry sources, count_verdict, and status provenance but no tier, so distilled instructions inherit no reuse class.
- Derived artifact: configs/lora_pipeline.yaml:4 fine-tunes google/gemma-2-2b-it, :27 trains on memory/training/sovereign_training_data.jsonl, :29 emits ghost-adapter with no license row, while the compass claims disk sovereignty and forkable-no-permission operation (docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md:195 and :199). The article names exactly this conflation: weights on your disk is not open source.

## The steal (mechanism)

Wire the vault's license law to the point of use. The find supplies the tier vocabulary the moment needs (open-source vs open-weights vs custom-restricted, with OSAID contested by its own community and OpenMDW pending at OSI); the vault already holds the fleet's tiers; this sweep already holds the per-release reading rule. The steal is the missing third wire: a `license:{tier,name,source_url}` row per declared model in the runtime configs, tiers inherited from the vault's starting ledger (Qwen tags = Apache-2.0 per vault :11; gemma:2b, gemma4, and the LoRA base = Gemma Terms per vault :12; nomic-embed-text fetched fresh as the vault gap), then propagated by tools/thought_quantizer.py as a `license_tier` field on compiled rows in memory/corpus/quantized_thought/, consumed by mag/context_pack.py and mag/verb.py so packs carry an honest reuse class. Text-layer rule: any estate text claiming "open source" about the stack cites a tier receipt or downgrades to "open weights". The organ law generalizes cleanly onto this: mag/organ_map.py:732, "a claim advances only when its corresponding evidence exists; unknown stays unknown".

## Estate map

Feeds the sovereign mirror (self-hosted local model stack) and the quantizer:
- Sovereign mirror, point of use: configs/lanes.yaml:31-40 and configs/lanes_vast_rtx8000.yaml:11-16 gain the license rows; configs/seat_playbook.yaml:16-19 (ollama_gemma4) likewise.
- Quantizer: tools/thought_quantizer.py emits license_tier on compiled rows; consumers mag/context_pack.py and mag/verb.py propagate it into packs.
- Fine-tune surface: configs/lora_pipeline.yaml:4,27,29 gains a derived-artifact tier row (Gemma Terms derivative), closing the compass line-199 gap for ghost-adapter.

## Probe (falsifiable, cheap, scoped, this week)

Claim to falsify: "the running fleet's configs carry no license rows and the vault's tiers are not wired to them." Half already ran and confirmed it: the git grep above returned zero hits across all five config files (exit 1, 2026-09-29). The week's repair: wire license rows for every distinct declared tag, 5 in the two roster files (gemma:2b, qwen-desk:latest, qwen2.5-coder:7b, qwen2.5:32b, nomic-embed-text) plus gemma4:latest and the LoRA base google/gemma-2-2b-it where declared, sourcing Qwen and Gemma tiers from vault :11-:12 and fetching nomic-embed-text's license text fresh rather than guessed. The probe passes when the same git grep returns at least one license row per distinct tag, each with a source_url, no row claims open-source without an SPDX or OSI identifier, and thought_quantizer.py output rows carry license_tier. It falsifies the port if any tag cannot be tiered from its actual license text, or if a vault family label contradicts a tag's upstream terms (for example gemma4:latest resolving to terms the "Gemma Terms (redistributable)" family label misstates); any such failure is itself a real finding about the sovereign stack.
