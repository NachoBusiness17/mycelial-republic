# DUEL2_train_11_r2 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# Contender pass: the missing guardrail in MCP MANIFEST SPEC v0.1

**Citation convention.** The evidence block carries no line numbers, so every `file:line` is given as `§section "quoted bytes"` with `line: UNVERIFIED`. Every quote is copied from the supplied text (sha256 `fa2fa26f...5775`).

**Measurement conditions.** The "the spec says nothing about X" claims below come from reading the supplied text once, in full, with that hash, with no other repo file available. Anything that depends on code or files outside this document is marked UNPROVEN.

---

## 1. The finding (one safeguard)

**MISSING: a live-conformance pin.** The spec never requires the gate to compare what the running server currently advertises against what the manifest froze. Epoch-pinning binds a local file to a hash. It does not bind the server to the file.

Why that is the most damaging gap:

- §3.2 says "Between epochs, NOTHING in `tools` (names, descriptions, schemas, order, tier, quota) may change." That is a rule about a file the house controls. The pack's own `server` block says `"endpoint_ref": "ZAI_MCP_SEARCH_URL"`, and `"official": true` is a label, not a check. The house does not control the remote server (§2).
- §8.3 verifies "the pack file's canonical hash matches the pinned `epoch_sha256_16`". That compares file to pin. The server is never consulted.
- §6 says "Ambiguity fails closed: unknown tool, unknown tier, unknown quota, stale epoch". Server drift is not in that list. It is not ambiguous to the gate, because the gate never looks at it.
- The fail-close discipline therefore guards only declared metadata, and drift never touches declared metadata.

---

## 2. The exact path it permits (accident or attack)

**Setup.** Pack `zai_web_search`, epoch E, digest D. It declares `tier: perception`, `mode: read_only`, `cache.policy: allow`, and key `tenant+tool_version+canonical_args+source_rev+auth_scope`. Under §4 it is "bindable by ANY lane, including quantized/flash/edge tiers and dumb swarms."

| Step | What happens | Clause it hides behind |
|---|---|---|
| 1 | Mid-epoch, the remote server changes. The cause could be a vendor update, a compromise, or a repointed endpoint. The tool's description gains instructions, its schema gains a parameter, or the tool starts side effects while still advertised as search. The epoch string does not change. | §3.2 constrains only the manifest file. §2 `"official": true` stands in for a trust check. |
| 2 | A lane spawns. The check compares the unchanged local file to the unchanged pin and passes. | §8.3 "Verify the pack file's canonical hash matches the pinned `epoch_sha256_16`." §8.1 reads the manifest "once, at spawn, never at runtime". |
| 3 | A quantized lane calls the tool. The gate runs tier check, quota check, execute, receipt. The tier check reads the declared `perception` and `read_only`, so the §4 structural refusal never fires. | §8.5 "tier check -> quota check -> execute -> receipt append". §8.6 hides nothing here, because the server is whitelisted. |
| 4 | The result is cached. The key contains `tool_version` and `source_rev`, but nothing in the document defines where either value comes from. The only version-like value in the pack is `epoch`, which has not changed. Old-behavior results replay under new behavior, and new-behavior results are stored under the old key for every lane in the tenant. | §6 "any auth-scope or source-rev change misses the key." Server behavior change is not a named miss trigger. |
| 5 | If the tool now writes, its result is still cacheable. The rule "A `write`/`hands` result is NEVER replayed" is applied by manifest declaration, not by observed effect. "Never cache privileged results by argument equality" is satisfied in form while violated in effect. | §2 "`cache.policy` - `allow` only for `read_only` tools." §6 first bullet. |
| 6 | The receipt records an ordinary row and cannot show which server behavior served the call. | §5 "Each gated call appends a receipt row (tool, lane, cost, ts)." plus "No receipt = never happened". The ledger is clean and useless for forensics. |
| 7 | Nothing ever fires. The epoch has not changed, so the "stale epoch" refusal and the §3.4 diff row never trigger. The drift lasts until a human changes the epoch. | §3.4, §6 "stale epoch", §8.7 "Epoch change (manager GO only)". |

**Neither the spec nor this review shows whether the adapter forwards live `description` strings to the model.** That decides whether step 1 is also a prompt-injection channel into weak tiers. **UNPROVEN** from this document.

**Positive control (what the spec does catch).** Someone edits the local `tools` array without a new epoch. The §8.3 hash mismatch refuses the spawn with a receipt. The spec is sound against local edits and blind to remote drift.

**Negative control (what it does not catch).** Local file byte-identical, pin byte-identical, server's `tools/list` differs. Every check in §8 passes. The §TRI-STATE line "spawn-refusal / epoch-retirement paths: **Unproven**" confirms that even the existing refusal paths have never fired. The runtime drift path has no path to test.

---

## 3. The amendment (landable as-is)

**Slots into:** §6 FAIL-CLOSE CARRYOVER, as a new subsection appended after the "Ambiguity fails closed" bullet. It is self-contained and needs no other edit.

```
### 6.1 LIVE CONFORMANCE PIN (mid-epoch drift fails closed)

The epoch pin binds the running server, not only the pack file.

(a) CHECK. Before the first gated call on a connection, on every
reconnect, on every tools/list_changed notification, and whenever the
last successful check is older than N seconds (default N = 300), the
gate MUST fetch the server's live tools/list, canonicalize it per
section 2, and compute sha256_16 over the tools array exactly as in
section 3.1. This is the OBSERVED digest.

(b) MISMATCH OR UNKNOWN. If the observed digest differs from the pack's
pinned epoch_sha256_16, or the fetch fails or times out, the gate MUST,
as one atomic step: (1) QUARANTINE the pack, refusing every call to it
from every lane; (2) invalidate every cache entry whose key names that
pack_id; (3) append a receipt row (pack_id, pinned digest, observed
digest or FETCH_FAIL, ts). Quarantine is lifted only by a section 8
step 7 epoch change. No lane, cache state, or runtime flag may lift it.

(c) RECEIPTS. Every section 5 receipt row MUST also carry
pack_id@epoch_sha256_16 and the observed digest of the last check. A
call whose last successful check is older than N seconds is refused.

(d) CACHE KEY. In cache.key, tool_version means the observed digest of
the last successful check. It is never the manifest epoch string.
```

**Why it hangs together with the existing text.** Section 11 already says "gates verify against the live tip". This clause is that sentence applied to the server rather than the file. It reuses the section 3.1 digest, so no new hash format is introduced.

---

## 4. Test predicate (fails today, passes with the amendment)

**Instrument and conditions.** A deterministic harness with a fake MCP server, an injectable clock, and an in-memory cache and receipt log. The result is valid only for the gate as specified here.

```
GIVEN  pack P pinned at digest D (tools: web_search, read_only, cache allow)
       fake server S advertising a tools/list that hashes to D
       lanes A and B both whitelisting P
1. A calls web_search(q="x")  -> expect ALLOWED; result R1 cached;
   receipt row carries "P@D" and observed digest D          [needs 6.1(c)]
2. Mutate S: change web_search.description (digest becomes D')
3. Advance clock by N+1 = 301 s  (or emit tools/list_changed)
4. A calls web_search(q="x")
5. B calls web_search(q="y")

ASSERT (all must hold)
  a.
