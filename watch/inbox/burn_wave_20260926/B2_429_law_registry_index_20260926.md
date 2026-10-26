# B2-429 receipt: register the law registry in the shared-surface index (2026-09-26, lane SW-03)

## Verdict

LANDED via the dated re-seal route, with the direct route's impossibility filed as a design fact. The brief's primary ask (add memory/law/registry.json itself as an INDEX item) is BLOCKED BY LAW, not by accident: the B2-147 writer guard in scripts/index_fold_host.mjs refuses any path with "no inbox-relative form" (two live refusal runs recorded below), and memory/law/registry.json is a live code-owned artifact (mag/law.py REGISTRY, mag/lattice_logic.py consumer) that cannot be moved into the inbox without breaking its owner. The brief's own alternative (--living-open OR a dated re-seal convention) is the route taken: watch/inbox/law_registry_seal.json (REGISTER, living-open) now sits ON the shared surface as a first-class sealed item carrying source path, sha256 de002c829c62ede7..., byte count, all 11 law ids, and the re-seal convention command. Post-add verify line recorded: "verify: 1034 hash-clean, 11 living-ok, 2 living-open, 15 mismatched, 0 missing (of 1062 active items)" with law_registry_seal.json listed LIVING OPEN, log-carried integrity. The falsifier's hole (verify reporting the law registry missing while receipts cite it) is closed: 0 missing, and the registry's sealed state is now fold-covered.

## Evidence file:line quotes

- Refusal run 1 (from watch/inbox): "ERROR: file does not exist: memory/law/registry.json" (the writer resolves against the inbox root).
- Refusal run 2 (repo-relative attempt): "ERROR: add: refusing to append an unresolvable event: normalized path ../../memory/law/registry.json has no inbox-relative form (B2-147 writer guard)".
- scripts/index_fold_host.mjs B2-147 comment: "the writer guard must normalize and classify with the exact bytes the fold will use, never a drifting copy" and the guard's refusal of outside forms (the law that blocks the direct route; B2-157's phantom-item history is why it must stay).
- mag/law.py:21,46: "Store: memory/law/registry.json + memory/law/enforcement_trail.jsonl" / "REGISTRY = LAW_DIR / \"registry.json\"" (the live owner; moving the file breaks the owner).
- Successful add line: "add: appended seq 1790455923203524097 for law_registry_seal.json -> 1062 active items".
- Post-add verify line (this lane): "LIVING OPEN (no byte seal, log-carried integrity): ...\\watch\\inbox\\law_registry_seal.json" and "verify: 1034 hash-clean, 11 living-ok, 2 living-open, 15 mismatched, 0 missing, 0 living-unverified (of 1062 active items)".
- watch/inbox/INDEX.json (post-add): item "law_registry_seal.json", class REGISTER, living True.
- watch/inbox/law_registry_seal.json: "source_path": "memory/law/registry.json", "source_sha256": "de002c829c62ede7...", "law_count": 11, plus the re-seal convention command and the touch-law note (drift is staleness, not tampering).

## Work done

- Verified the brief's premise against bytes: INDEX items with path memory/law/registry.json = 0 (the 2 raw grep hits are purpose text on the B2-50 LAW13 and B2-163 LAW12 rows).
- Attempted the official direct add twice (both refusals quoted above); identified the blocking law (B2-147 writer guard) and the owning constraint (mag/law.py owns the path), and chose the brief's named alternative instead of weakening the guard or moving the file.
- Filed watch/inbox/law_registry_seal.json: seal of the live registry (sha256, byte count, all 11 law ids, sealed_ts, writer) with the dated re-seal convention written INTO the artifact (re-seal command for any registry change) and the B2-237 framing (drift = staleness, never tampering).
- Registered it through the official add path with INDEX_WRITER=zcode-b2-429-law-registry, class REGISTER, --living-open; ran the post-add verify and recorded the summary line and the item's LIVING OPEN state.
- Pre-existing verify noise disclosed: 15 mismatched items (QUEUE.md and friends) reflect the concurrent-lane edit cadence of the wave against their seals, not this lane's change; 0 missing.

## Falsifier

Kill conditions: (a) a registry change without a re-seal: sha256 in law_registry_seal.json no longer matches memory/law/registry.json bytes (detectable by recomputing; the convention line inside the seal names the repair), (b) the seal item vanishing from the fold (verify's 0-missing line regresses; the item is log-carried so deletion is an invalidate event, visible), (c) someone "fixing" the B2-147 guard to admit outside paths casually (the guard's phantom-item history, B2-157, is the counter-receipt; any such extension needs the LIVING_HASH_LAW spec amended first, and this receipt is the filed demand for that lane). The original falsifier "verify reports memory/law/registry.json missing while receipts cite registry rows" is dead in its current form: verify now covers a REGISTER item bound to the registry's bytes by seal, and reports 0 missing.

## Bibliography closed

- scripts/index_fold_host.mjs (help output, B2-147 guard comments, add/verify runs)
- watch/inbox/INDEX.json (post-add item read; pre-add absence verified)
- memory/law/registry.json (owner check via mag/law.py:21,46; bytes hashed for the seal; 11 laws)
- mag/lattice_logic.py:37 (registry consumer, "law" family path)
- watch/inbox/LIVING_HASH_LAW_20260926.md (living-open shape, sections consulted)
- watch/inbox/law_registry_seal.json (new seal artifact)
- watch/inbox/burn_wave_20260926/B2_50 and B2_163 INDEX rows (the purpose-text-only citations the brief named)
