"""Re-apply zcode-sw-08 landings erased from QUEUE.md by a concurrent
whole-file restore (the B2-343 disease). Landing re-applied from the durable
LEDGER + receipts; nothing re-executed. Run once."""
import re

p = 'watch/inbox/burn_wave_20260926/QUEUE.md'
b = open(p, encoding='utf-8', newline='').read()
nl = '\r\n' if b.count('\r\n') > (b.count('\n') - b.count('\r\n')) else '\n'

landed = {
 'B2-170': ("Imprint/deck links denominator: scripts/build_fleet_imprint.py:292 counts 332 rows as canonical rows and scripts/build_deck.py:139 likewise, but only 280 are links after the B2-28 split; report links and events as separate denominators; pointers scripts/build_fleet_imprint.py:289-299 + scripts/build_deck.py:130-139 + watch/inbox/EVENTS.jsonl.",
   " Landed 2026-09-26 (284 link + 53 event + 1 marker of 338 lines, both surfaces split, live-run verified; also names B2-28 falsifier (d) fired at LINKS.jsonl:333-334): receipt watch/inbox/burn_wave_20260926/B2_170_imprint_deck_denominator_20260926.md"),
 'B2-172': ("image-drop schema card: LINKS.jsonl:256 (canonical image-drop:fibonacci_determinants_plate_20260918.png, url local path, sha256 = file bytes, proven 2026-09-26) is an undocumented third schema inside the link ledger; document it or move the class to its own register per the B2-28 split law, with a verifier that re-hashes the file; pointer watch/inbox/burn_wave_20260926/B2_26_links_sha_backfill_20260926.md evidence block.",
   " Landed 2026-09-26 (register watch/inbox/IMAGE_DROPS.jsonl created, verify-images re-hash CLI live OK 1 row, 4 test pins, suite 35 passed): receipt watch/inbox/burn_wave_20260926/B2_172_image_drop_schema_20260926.md"),
 'B2-137': ("Register the vault pack: ESSENTIALS_PACK_VAULT_20260926.tar.gz.enc (22,120,192 bytes, sha256 prefix ada2f62926f432ed4ea01fdc per memory/trajectory/steps.jsonl:22168) was named unindexed by the B2-18 verify (watch/inbox/burn_wave_20260926/B2_18_stone2b_20260926.md); compute the full sha256 from bytes and append the INDEX.json artifact row per the shared surface contract. (renumbered from B2-135, collided with the Grok Ask 4 lane)",
   " Landed 2026-09-26 (independent from-bytes rehash: full sha ADA2F629..587C87 over 22120192 bytes matches the standing INDEX row and the B2-146 register event; no duplicate row needed): receipt watch/inbox/burn_wave_20260926/B2_137_vault_pack_register_20260926.md"),
 'B2-141': ("Grok Ask 4 scope freeze: the packet \"about 20 files\" line now faces 52 BURN_*/SEED_SALON_* files in watch/inbox (37 dated 20260925, 14 dated 20260926, none 09-24), so an unfired audit burns the seat window on post-packet filings; bind the audit to the 20260925 set and park the 14 new files as a second-wave ask; pointers watch/inbox/GROK_LANE_PACKET_20260925.md:32 + watch/inbox census 2026-09-26.",
   " Landed 2026-09-26 (frozen 39x20260925, parked 34, census re-measured 73 live, pre-drafted Ask 4b in the card): receipt watch/inbox/GROK_ASK4_SCOPE_FREEZE_20260926.md"),
 'B2-153': ("External steal dig for SEED-RIB: the best existing ideas for kilobyte-reconstructible estates and self-describing agent structures (reproducible-build manifests, Nix derivations, git bundles, model cards, agent cards, MCP registries, stego seeds per Fauvel, called-shot compression per Mr Pool); verdict per idea steal/vacuous with citations; what we invent that nobody has.",
   " Landed 2026-09-26 (9 idea classes verdicted, 7 steal-in-part with citations, 2 unverified-internal named as owed, delta owned in the card): receipt watch/inbox/burn_wave_20260926/B2_153_seedrib_steal_dig_20260926.md"),
 'B2-286': ("model-null hole in chat_provider: z_ai2/z_ai3 carry no default_model key so provider_default_model returns None (models/providers.py:164) and a bare live call sent model null and got HTTP 200 with empty content + empty usage (B2-62 first probe: ok=True, text='', model=None, usage={}); give z_ai2/z_ai3 default_model or make chat_provider refuse a null model with a named error; falsifier = chat_provider('z_ai3', ..., tier=T2) without model returns a named error instead of a 200-empty; pointers models/providers.py:164 + configs/providers.yaml z_ai2/z_ai3.",
   " Landed 2026-09-26 (refuse arm at both chat paths, free_local carve-out; falsifier pinned: bare z_ai3 call returns null_model_refused with zero wire traffic; 17+50 pytest passed): receipt watch/inbox/burn_wave_20260926/B2_286_null_model_refuse_20260926.md"),
 'B2-318': ("Pytest-named script self-tests in tests/ never execute under pytest: (self-fed by B2-247) the B2-247 gap names tests/ack_reaper_test.py (21 hand-run checks) and tests/lesson_gate_test.py (22 hand-run checks) as zero-collect candidates: both are standalone self-test scripts that the census counts as candidates but that contribute zero pytest items and zero CI signal, so a regression in scripts/ack_reaper.py or scripts/lesson_gate.py lands with no pytest failure anywhere; either port both batteries to pytest test modules (thin def test_* wrappers over the existing check functions so the checks finally execute in pytest -q) or rename them out of the python_files pattern so the census stops counting dead candidates; falsifier: mutate a scream threshold in scripts/ack_reaper.py and run pytest -q, today zero items fail while the hand-run battery catches it; pointers tests/ack_reaper_test.py, tests/lesson_gate_test.py, watch/inbox/burn_wave_20260926/B2_247_collect_gap_20260926.md.",
   " Landed 2026-09-26 (port arm: single collect_checks() battery per script, 45 wrapper items green, hand-run mode unchanged; falsifier fired live: threshold mutation now fails 3 pytest items, restored byte-clean): receipt watch/inbox/burn_wave_20260926/B2_318_pytest_port_batteries_20260926.md"),
 'B2-386': ("Higher-fidelity refetch for the 33881-group thumbs: (self-fed by B2-88) the 262-row group recovered at 4727 bytes per message (web preview thumbnail render) while the export metadata records 33881 for the same underlying image, so the full-size preview asset the export measured is still not on disk and the fetched bytes may be a re-encode or a replaced channel image (identity honest-limit in the receipt Verdict); probe the higher-fidelity surface (telesco.pe file URL size variants, t.me embed endpoints, or a fresh Telegram Desktop public export of MrPool_Q when one becomes available) and land any exact-33881-byte hit as a NEW dated register row superseding the 2026-09-26 row for that cite, never overwriting landed rows; falsifier: a fetched file at exactly 33881 bytes for one of the 262 cites fails to land a superseding row, or a lane edits the existing 2026-09-26 register rows in place; pointers watch/inbox/mrpool_export/media_recovered_register_20260926.jsonl (source_url, provenance), watch/inbox/burn_wave_20260926/B2_88_metadata_fetch_20260926.md Verdict honest-limit paragraph.",
   " Landed 2026-09-26 (all four arms probed live, every surface serves the same 4727-byte render, no 33881 hit so no supersede owed, register untouched): receipt watch/inbox/burn_wave_20260926/B2_386_refetch_probe_20260926.md"),
 'B2-291': ("Estate MCP on docker (operator question 2026-09-26: our docker can serve mcp, does that do anything): design + wire the estate MCP server (mag/mcp_server.py + B2-151 seed tools) into the running docker stack (mag-sovereign/worker/redis) as a always-on service so every MCP client the operator touches (ZCode, VS Code, Claude-class clients, cold agents) can call corpus/grounding/seed/join tools without file-lock contention; loopback/auth law per the armC assert precedent, read-only tools first; falsifier: a second MCP client session calls corpus_search + seed fetch through docker concurrently with this seat and both return clean.",
   " Landed 2026-09-26 (service healthy on 127.0.0.1:8766, archivist read-only 17 tools, two concurrent sessions through docker both clean on corpus_search; seed_fetch arm filed owed, B2-151 citation named mis-cite): receipt watch/inbox/burn_wave_20260926/B2_291_estate_mcp_docker_20260926.md"),
 'B2-295': ("openrouter :free rotation build-out: 17 :free ids are live in today's catalog (B2_61_verify_results.json openrouter_catalog.free_ids) but only cohere/north-mini-code:free is chat-verified; qwen3.8-27b:free proved catalog-presence is not liveness (429 upstream shared pool); build a verify-then-add rotation where each candidate id earns its providers.yaml line with one live chat gate first; pointers configs/providers.yaml openrouter block + watch/inbox/burn_wave_20260926/B2_61_verify_results.json.",
   " Landed 2026-09-26 (gate tool + live runs on file; 3 ids earned lines, cohere re-proven, 429/403 ids stay lineless with named comments): receipt watch/inbox/burn_wave_20260926/B2_295_openrouter_free_rotation_20260926.md"),
 'B2-297': ("living-downgrade detector: a plain `add` re-register legally drops the living flag (last-register-wins, LIVING_HASH_LAW_20260926.md section 5), so one stale whole-file refresh silently reverts LINKS.jsonl/QUEUE.md/phone_relay_log.jsonl to a shape that hard-fails on the next append; add a validate warning in mag/shared_surface.py items loop when one of the three known living paths folds to an item without item.living; pointers mag/shared_surface.py:224-258 + watch/inbox/LIVING_HASH_LAW_20260926.md sections 4-5",
   " Landed 2026-09-26 (watchlist + warning + counter, 23 tests pass; FIRED LIVE: QUEUE.md registration already carries no living flag, re-register owed to fold owner): receipt watch/inbox/burn_wave_20260926/B2_297_living_downgrade_detector_20260926.md"),
}

erasure = (" (row re-applied 2026-09-26 by zcode-sw-08: a concurrent whole-file board restore "
           "erased the landed row, the B2-343 disease; re-applied from the durable LEDGER + "
           "receipt, nothing re-executed)")

applied = []
for bid, (body, note) in landed.items():
    rcpt = note.split('receipt ')[1]
    mm = re.search(r'- \[.\] ' + bid + r' .*$', b, re.M)
    if mm:
        row = mm.group(0)
        if rcpt in row:
            applied.append(bid + ':already')
            continue
        new = row
        if new.startswith('- [ ]'):
            new = '- [x]' + new[5:]
        new = new + note + erasure
        b = b[:mm.start()] + new + b[mm.end():]
        applied.append(bid + ':note-reapplied')
    else:
        new = '- [x] ' + bid + ' ' + body + note + erasure
        mm2 = re.search(r'## Open\r?\n', b)
        j = mm2.end()
        b = b[:j] + new + nl + b[j:]
        applied.append(bid + ':row-refiled')

open(p, 'w', encoding='utf-8', newline='').write(b)
print(applied)
