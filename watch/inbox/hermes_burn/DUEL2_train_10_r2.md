# DUEL2_train_10_r2 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# Falsification pass: docs/ref/MCP_MANIFEST_SPEC.md v0.1

<citation_convention>
The evidence block carries no line numbers, so file:line is UNVERIFIED for every claim below. Each citation is therefore a section number plus quoted bytes, and each quote resolves to the pasted text. Sections or clauses the document names but does not contain (lane contract clause 8, clause 1, lane charter clause 5) are UNVERIFIED and are not relied on.
</citation_convention>

<central_claims>
- **CLAIM-A (byte-stable per epoch):** §3.2 "Between epochs, NOTHING in `tools` (names, descriptions, schemas, order, tier, quota) may change." §2 "byte-stability is a hard requirement".
- **CLAIM-B (quota bound):** §5 "lane budget minus outstanding charges >= `quota.per_call`, else the call is refused". Purpose, per the GO: "or their eyes eat the judgment lanes' 5h pool". The claim is that weights bound judgment-pool drain.
- **CLAIM-C (the pin pins):** §8.3 "Mismatch or missing → REFUSE SPAWN (fail-close)". §8.6 "the adapter surface simply does not expose it". §9 casts the `mcp_whitelist:` line as the consumer-side pin.
</central_claims>

---

## CLAIM-A predicates

<predicate id="A1" name="canonical form is under-specified">
- **Quote:** §2 "Canonical JSON (sorted keys, no trailing whitespace, LF endings)". §3.1 "sha256 over the canonical `tools` array, first 16 hex chars".
- **Experiment:** Take one `tools` array (the §2 example tool). Serialize it with 4 conformant canonicalizers:
  - (i) Python `json.dumps(sort_keys=True, separators=(',',':'), ensure_ascii=False)`
  - (ii) the same with `ensure_ascii=True`
  - (iii) `jq -S .` (default indent 2)
  - (iv) `jq -S -c .`

  Hash each result and take the first 16 hex characters.
- **PASS:** exactly 1 distinct `epoch_sha256_16` across all conformant serializers, or the spec names one serializer.
- **FAIL:** more than 1 distinct value. The spec constrains key order, trailing whitespace and line endings, but not separators, indent, unicode escaping, number rendering (`1.2` vs `1.20`) or final newline.
- **Conditions:** instrument is a hash script run offline, once, at spec-review time. Context is any host, since the test needs no live system.
- **Expected today:** fires. Nothing in the document picks separators or escaping.
</predicate>

<predicate id="A2" name="the hash does not cover the whole file">
- **Quote:** §3.1 hash is over the `tools` array only. The `server` block (`endpoint_ref`, `auth_ref`, `official`, `notes`) and `epoch` sit outside it. §8.3 says "Verify the pack file's canonical hash".
- **Experiment:** Take
