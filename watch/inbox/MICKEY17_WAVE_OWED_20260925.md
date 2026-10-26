# MICKEY-17 WAVE - OWED KNOCKDOWN - WAVE RECORD 2026-09-25

24 seats fired, one task each. Seat manifest, task ids, and finish lines are the
parent run's TASKS table (workflow `dwfrun-a07b67ac-f3d2-42f4-86e1-6cf7b7d33372`).
Artifact paths below are relative to the estate root
`C:/Users/foste/Documents/projects/local_sovereign_agent` and every one was
re-checked on disk this filing session: all 24 exist and are non-empty.

## Verifier's on-disk verdict

24/24 verified on disk (note: quote-audit-wide and grok-overflow were relative
paths, resolved against `C:/Users/foste/Documents/projects/local_sovereign_agent`);
missing: none.

## Seat table (task / ok / artifact / one-line summary)

| task | ok | artifact | one-line summary |
|---|---|---|---|
| mcp-pin | yes | tools/mcp_pin.py | MCP tool name+description+schema hash pinning with check_drift() reconnect alarm and a `__main__` self-test; fixture-built, no live MCP connections. |
| freshness-receipts | yes | tools/freshness_check.py | Extended in place: receipt(observed_at, source_hash) per tool result plus stale_claim() gate helper; self-test entry present. |
| fastsearch-probe | yes | watch/inbox/FASTSEARCH_STATIC_KEY_PROBE_20260925.md | VERDICT: NO. HERMES_API_KEY_1 exposes no Perplexity Fast Search and no /search-style route on the static-key surface; closes the owed probe (GO_LIST_EXECUTION_20260925.md:24). |
| a2a-probe | yes | watch/inbox/A2A_FIRST_PROBE_20260925.md | Verdict: PASS. First live A2A interop receipt: a2a-sdk client fetched and decoded a real public agent card into the official proto, $0 spent. |
| openjev-ab-prep | yes | watch/inbox/OPENJEV_AB_PROTOCOL_20260925.md + watch/openjev_ab/frozen30_20260925.jsonl + watch/openjev_ab/run_openjev_ab.py | Pre-registration, frozen 30-item identical test set (byte-deterministic freezer, sha256 on file), and mock-validated runner; zero model download and zero inference by scope. |
| deepseek-offpeak | yes | watch/inbox/DEEPSEEK_OFFPEAK_CACHE_RATIO_RECEIPT_20260925.md | Burn scheduler protocol now carries deepseek_windows and every stored 120x pro cache-ratio claim corrected to 30x, receipt with verification commands filed. |
| effort-tiers | yes | mag/lane_effort.py | The three Anthropic effort tiers encoded as lane budgets by fan-out width plus a value-per-token admission gate; self-test entry present. |
| freeze-sysprompt | yes | mag/context_pack.py | freeze_system_prompt() landed (mag/context_pack.py:367) for cache-stable system prefixes. |
| cache-figure-fix | yes | memory/research_polished/kv_cache_compaction.md | Stale 75% caching figure corrected to 90% / documented 30-minute window with the OpenAI 2026-09-22 source URL cited and an RQ6 vendor reference arm registered (line 15). |
| grok-repoint | yes | watch/XAI_GROK47_REPOINT_20260925.md | Seat repoint to grok--4-7 filed PLANNED, not wired: catalog probe ran this session, commented-ready config line plus ledger rows filed; wiring waits on a live key. |
| costout-receipt | yes | memory/research_polished/economics.md | Costed receipt (line 34): highest-volume recurring task at $0.00139/call real-bill LLM meter vs $0.20-0.30 agent and $1-4 human brackets, with honest gaps named. |
| memory-counterlaw | yes | watch/inbox/AGENT_MEMORY_COUNTERLAW_20260925.md | One-page operator draft: agent memory never leaves the box unless the user holds the keys; adoption is operator-gated, the file enacts nothing. |
| ephemeral-skills | yes | mag/skill_lifecycle.py + corpus/steal/ZCODE_REPO_STEAL_MAP_20260924.md | EPHEMERAL one-turn skill flag behind ADK_ENABLE_SKILL_LIFECYCLE, default off, with registry overlay in tools/__init__.py and the spec row filed (spec row :352 receipts self-test 21/21 and pytest 14 passed). |
| memsentry-tier | yes | mag/trust_gate.py | Ingest trust gate patched MemSentry-style: review-tier suspicions route to operator_inbox instead of silent exclusion, trust-score field in the register, audit check beside it (mag/trust_gate_audit_check.py). |
| wandr-selfeval | yes | tools/wandr_selfeval.py + tools/wandr_selfeval_task.json | WANDR-shaped claim(n)-to-field(m)-to-url(k) self-eval with soft/hard F1 scorer and the task JSON near WANDR medians. |
| write-stripped | yes | mag/write_strip.py + watch/inbox/WRITE_STRIP_FANOUT_20260926.md | Fan-out write-strip compiler landed runner-side (schema-level omission, not runtime veto); the ZCode-harness change stays spec-only exactly as scoped. |
| sonar-agentapi | yes | mag/perplexity_research.py | REMAP_PATH implemented behind a flag (Search API target at mag/perplexity_research.py:68); post-09-27 route ready, not live. |
| intervention-gate | yes | mag/intervention_gate.py | The 8x-recommended, 0x-built inject-vs-silent memory gate built minimal: gate fn, register, worked example, self-test entry. |
| organ-table | yes | watch/inbox/ORGAN_TABLE_20260925.md + watch/inbox/organ_table.json | Organ table v1 filed (schema organ_table.v1), the routing keystone ranked 1 of 512 OWED; classify step and route-event writer stay owed (receipt line 5). |
| w4-rerun | yes | watch/GAUNTLET_W4_RERUN_VERDICT_20260925.md + watch/gauntlet_w4_rerun_receipts.jsonl | VERDICT: PASS, preregistered criterion MET on n=50 valid tails per arm (+6pp warm-vs-cold, cachedTok 4864 on every warm row); 100-row receipts recounted independent of the harness. |
| quote-audit-wide | yes | watch/inbox/QUOTE_AUDIT_WIDE_20260925.md | Widened verbatim quote audit: 30/34 byte-exact (88.2%), all 34 resolve to real archive rows, zero fabricated quotes found; 4 non-clean units hand-adjudicated. |
| grok-overflow | yes | watch/inbox/GROK47_CLI_BURN_RECEIPT_20260925.md | One real fan-out-suitable chore executed through the grok CLI harness seat, EXECUTED, cost via the proxy self-reported total_cost_usd; Portal pricing was not the path taken and the receipt says so. |
| photon-rot-check | yes | watch/inbox/PHOTON_ROT_20260925.md | Verbatim-at-publish stays byte-unadjudicable (Wayback history is one contentless 204, archive.today 404); mutation finding upgraded with one correction: the 20% figure is present today, reworded. |
| x-leak-retry | yes | watch/inbox/X_LEAKS_WAYBACK_20260925.md | Wayback CDX retry landed real leaks: the Kratsios remark is new to the estate and the METR bias thread is organized; simonw captures 504'd (INCONCLUSIVE on that one target). |

Count: 24/24 seats filed, 24/24 artifacts verified on disk.

## GO list (failed and still owed)

No seat failed: all 24 finish lines landed and the verifier found nothing missing.
Carry-forward OWED named by this wave's own receipts (not seat failures):

1. grok-repoint: the live repoint is still owed when the key/wiring is live; what
   landed is the receipted plan plus ready config line (watch/XAI_GROK47_REPOINT_20260925.md
   line 4: "Status: PLANNED, not wired").
2. organ-table: the classify step and route-event writer stay owed; exact hook
   point named with line evidence in watch/inbox/ORGAN_TABLE_20260925.md.
3. openjev execution: protocol, frozen set, and runner are filed; the real A/B runs
   in a night-window lane by design (family-box law). Execution is the owed half.
4. Doc sync owed: memory/research_polished/kv_cache_compaction.md lines 23 and 27
   still list freeze_system_prompt() as never built while mag/context_pack.py:367
   now defines it. Sync the polish library's owed-list.
5. Pre-wave carry-forwards still open from watch/inbox/GO_LIST_EXECUTION_20260925.md:
   grounding_wave.md full view resync, and wiring a caller so chores route through
   the nous lane (P2 "Still OWED (small)").
6. x-leak-retry next seat: 22 unexamined midas rows starting with the 7-tweet 09-21
   thread (receipt's "Steals" section 3), and the simonw 504'd captures stay
   INCONCLUSIVE, not negative.

## Commit message body

    mickey17 owed wave: 24/24 seats filed, verifier 24/24 verified on disk

    All 24 OWED-knockdown seats landed their finish lines; the verifier seat found
    nothing missing on disk. Highlights: W4 rerun fired and PASSED its
    preregistered criterion on n=50/arm (100-row receipts, independent recount);
    widened quote audit found zero fabricated quotes (30/34 byte-exact, 88.2%);
    organ table v1 filed (routing keystone, 1 of 512 OWED); first live A2A interop
    receipt; write-strip fan-out discharged runner-side; effort tiers, MCP pinning,
    freshness receipts, intervention gate, ephemeral skill lifecycle, trust-gate
    review tier, WANDR self-eval, sonar remap path all built; DeepSeek off-peak
    windows + 30x cache-ratio correction closed; grok overflow chore executed
    through the CLI seat with a cost receipt.

    Still owed (carry-forward, none failed): live grok-4-7 wiring, organ-table
    classify step + route-event writer, openjev night-window execution,
    kv_cache_compaction.md owed-list resync (freeze_system_prompt drift),
    grounding_wave.md view resync, nous-lane caller wiring, 22 unexamined midas
    Wayback rows.

    Wave record: watch/inbox/MICKEY17_WAVE_OWED_20260925.md
