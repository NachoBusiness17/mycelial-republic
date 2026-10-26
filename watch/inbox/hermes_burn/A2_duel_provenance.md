# A2_duel_provenance (anthropic/claude-opus-5.5, turn 1)

# Provenance Envelope Spec: Duel Self-Contamination Closure (Q30 / Q32)

**Deliverable:** one spec with patch hunks for `tools/duel_harness.py`, `tools/ask_bank.py`, one new verifier `tools/duel_verify.py`, and one new registry `configs/model_registry.json`.

**Citation rule.** The evidence arrived without line numbers, so every `file:line` below is **UNVERIFIED**. Each anchor instead quotes the exact bytes, so `grep -nF '<quote>' <file>` resolves it. Wherever a claim depends on a file not present in the evidence, it is marked UNVERIFIED.

---

## 0. Ground truth: what the bytes show today

| # | Claim | Anchor (quoted bytes) |
|---|---|---|
| G1 | Raw response bytes are discarded at parse time. No digest is possible after the fact. | `tools/duel_harness.py:call` `return json.load(r)` |
| G2 | `fire()` throws away everything except content and cost, including `id`, `model` echo, and `system_fingerprint`. | `tools/duel_harness.py:fire` `return content, cost` |
| G3 | The duel row has no response id, no model echo, no request or response digest, no weights field, and no task digest. | `tools/duel_harness.py:run_duel` row literal: `"ask_id": ask_id,` ... `"b_headers": count_headers(b_text),` |
| G4 | Retro contenders come from burn rows keyed only by `id`/`model`/`content`/`cost_usd`. No origin field exists. | `tools/duel_harness.py:load_pair` `if row.get("id") in (a_id, b_id):` and `run_duel` call `a_row["model"], b_row["model"]` |
| G5 | The rejudge provenance gate is length-only. Same-length, different-byte text passes. | `tools/duel_harness.py:run_rejudge` `if want is not None and len(text) != want:` |
| G6 | Contestant and judge share one gateway. | `ALLOWED_HOST = "inference-api.nousresearch.com"`, plus AJ1: "Both judges route through the same Nous gateway" |
| G7 | Self-judge confound is admitted. | AJ1: "glm-prime judged duels whose glm-side texts were authored by GLM-5.3 (this account's session model, per W8 provenance)" |
| G8 | The W8 series driver is absent, so the 6-0 row's authorship cannot be decided from bytes. | `tools/w8_series_duel.py (MISSING)` |
| G9 | The hidden half can be derived from tracked bytes. The generator is tracked, ask ids are formatted deterministically, and the split rule is a published deterministic sort. | `tools/ask_bank.py` `"ask_id": f"ab{VERSION}-{mat['key']}-{shape}"`, `return sorted(entries, key=lambda e: sha_text(e["ask_id"]))`, docstring `The generator itself is tracked code` |
| G10 | The draw ledger does not record whether an ask was drawn before. That information is only implicit in `drawn.count`. | `tools/ask_bank.py:cmd_draw` `entry = min(rows, key=lambda e: (drawn.count(e["ask_id"]),` and the append dict `"note": note or ""})` |
| G11 | The duel row carries no link to the draw. D6's "ask was the hidden draw" cannot be decided from `duels.jsonl` bytes. | G3 row literal has no `draw_id`/task hash. D6 driver `d6_askbank_duel.py` is not in evidence (UNVERIFIED). |

### Correction to the contract premise: D6 is evidence, not proof

D6's own text says: "One draw at n=3 proves nothing about the models in general".

**Conditions of the D6 measurement:**
- **Instrument:** `fireworks/ember-1` blind judge via the Nous gateway, streaming SSE.
- **Moment:** 2026-09-30.
- **Context:** n=3 per arm. Slot swap alternated by parity.

**Confounds in the contrast arm (V1):**
- It used different material.
- It carried "a disclosed ask-mismatch handicap" on glm.

The 3-0 / 0-3 inversion is consistent with contamination. It is equally consistent with a material effect or the handicap. Quarantining all visible-ask verdicts is still the correct policy. The justification is not that contamination is proven. It is that nothing in the bytes (G3, G11) can clear those verdicts.

---

## 1. Provenance envelope

### 1a. Duel ledger row (`logs/duel/duels.jsonl`)

New fields are additive and follow the "absent = null, readers must not break" law. The new `schema` value is `"duel/2"`.

```json
{
  "schema": "duel/2",
  "prov": {
    "a":     {"origin": "...", "response_id": "...", "response_model": "...",
              "requested_model": "...", "family": "...",
              "request_sha256": "...", "response_sha256": "...", "text_sha256": "...",
              "system_fingerprint": null,
              "weights_ref": {"level": "...", "value": "...", "source": "..."}},
    "b":     {"...same..."},
    "judge": {"...same, origin always fresh_api..."}
  },
  "judge_prompt_sha256": "...",
  "seat_model": "z-ai/glm-5.3-prime | null",
  "self_judge": false,
  "ask": {"ask_sha256": "...", "ask_draw_id": "v1h-0002 | null",
          "ask_visibility": "...", "bank_version": "v1 | null"},
  "prev_row_sha256": "...",
  "router_eligible": false
}
```

| Field | Capture method | Anchor it patches |
|---|---|---|
| `origin` | `fresh_api` = `fire()` ran in this process. `retro_api` = loaded from a burn row that itself carries `response_sha256` with a resolvable raw blob. `seat_authored` = a session model wrote the text (declared by the seat). `unknown` = legacy or no prov. `synthetic` = injected `caller` in tests. | `run_duel` `if a_text is None or b_text is None:` |
| `response_id` | `resp["id"]` from the OpenAI-compat body, or the first SSE chunk `id`. Treated as opaque: only presence and per-ledger uniqueness are checked. | G2 |
| `response_model` | `resp["model"]` echo. This is never treated as proof (see section 2). | G2 |
| `request_sha256` | sha256 of the exact `body` bytes posted. The key travels in a header, so it never enters the digest. | `call` `body = json.dumps({` ... `}).encode()` |
| `response_sha256` | sha256 of the raw HTTP body bytes (or the concatenated raw SSE stream). The blob is stored content-addressed at `logs/duel/raw/<sha>.json`. | G1 |
| `text_sha256` | sha256 of the content string (UTF-8). This replaces the length gate. | G5 |
| `system_fingerprint` | `resp.get("system_fingerprint")`. Usually null on proxies. Recorded, never required. | G2 |
| `weights_ref` | Per family, from the registry (table 1c). | new |
| `judge_prompt_sha256` | sha256 of the `jp` string. | `run_duel` `jp = judge_prompt(task, slot_a_text, slot_b_text, rubric, context)` |
| `seat_model` | env `MAG_SEAT_MODEL` (self-declared), else null. | new, mirrors `CORR_ENV` pattern |
| `self_judge` | True if `family(judge)` is in `{family(a), family(b), family(seat_model)}`. | G7 |
| `ask.*` | `ask_sha256` = sha256(task). `ask_draw_id` and `ask_visibility` are passed by the driver. Visibility classes are defined in section 3. | G11 |
| `prev_row_sha256` | sha256 of the previous ledger line's exact bytes. This is a hash chain, and it matches D6's gps `evidence_hash = sha256 of each exact banked duels.jsonl line`. | `run_duel` `f.write(json.dumps(row) + "\n")` |
| `router_eligible` | All of the following must hold: both contenders have origin in {fresh_api, retro_api}; `self_judge` is false; `ask_visibility` is in {hidden_first_draw}; verify passes. | new |

### 1b. Contender bank rows (burn jsonl, `d6_contenders.jsonl`)

These rows add the same per-contender block plus authorship fields. The existing keys `id`, `model`, `content`, and `cost_usd` (G4) stay as they are.

```json
{"id": "...", "model": "...", "content": "...", "cost_usd": 0.0,
 "prov": {"origin": "fresh_api", "response_id": "...", "response_model": "...",
          "request_sha256": "...", "response_sha256": "...", "text_sha256": "...",
          "weights_ref": {"level": "...", "value": "...", "source": "..."}},
 "seat_model": "...", "ts": "..."}
```

**Rule for Q32:** a contender row that lacks `prov.response_sha256` resolving to a raw blob is `origin: unknown`. It can never be promoted to `fresh_api` by a reader.

### 1c. `weights_ref` capture per family (`configs/model_registry.json`, new, tracked)

```json
{"z-ai/glm-5.3-prime":    {"family": "glm",    "open_weights": true,
                           "published_ref": "<hf-repo>@<commit-sha>", "echo_re": "^z-ai/glm-5\\.3-prime(-\\d{8})?$"},
 "qwen/qwen3.8-max-prime":{"family": "qwen",   "open_weights": true,  "published_ref": "<UNVERIFIED>", "echo_re": "..."},
 "google/gemini-3.8-flash":{"family": "gemini","open_weights": false, "published_ref": null, "echo_re": "..."},
 "fireworks/ember-1":     {"family": "ember",  "open_weights": "UNVERIFIED", "published_ref": null, "echo_re": "..."},
 "local/<judge>.gguf":    {"family": "<fam>",  "open_weights": true,  "local_path": "models/<file>.gguf"}}
```

| `level` | When used | What it binds |
|---|---|---|
| `local_hashed` | Judge runs locally. The sha256 of the weights file is computed at call time. | Weights to verdict. This is the only level that binds. |
| `published_ref` | Open-weight family served by Nous. The value comes from the registry's `published_ref`. | Nothing to the server. It records which weights the slug **claims**. |
| `declared` | The provider exposes a fingerprint or revision field. | Provider assertion only, unsigned. |
| `unattestable` | Closed weights (gemini, grok; ember is UNVERIFIED). | Nothing. |
| `provider_signed` | Reserved for the protocol change in section 2c. | Weights digest to request and response, under a provider key. |

---

## 2. The binding: what the OpenAI-compat response can and cannot prove

### 2a. What the response returns

| Response field | Semantics | Proves |
|---|---|---|
| `id` (`chatcmpl-...`/`gen-...`) | Minted by the gateway, opaque. | That a gateway produced a reply with this label. It is retrievable later **only if** the gateway offers lookup by id. A Nous lookup endpoint is UNVERIFIED. |
| `model` | String echoed by the same party serving the weights. | Nothing about weights. A swap is free and invisible: the gateway can alias, route, or substitute and echo any string. |
| `system_fingerprint` | OpenAI's backend-config marker, optional, often null via proxies. | A provider assertion of config epoch. It is unsigned and does not identify weights. |
| `usage.cost` | Provider-metered. | The billing claim only. |
| TLS session | Host identity `inference-api.nousresearch.com`. | Which host you talked to. It says nothing about which weights ran behind it. |

**Honest bottom line for Q30:** no field of an OpenAI-compat response, alone or combined, proves which weights ran. If one party serves both contestant and judge, it can swap weights undetectably at the byte level. The envelope in section 1 does not solve this. What it does is make every later claim **forgery rather than omission**. Raw blobs, digests, and the hash chain mean a lie must be actively constructed and must stay consistent with the gps `evidence_hash` cross-ledger join.

### 2b. What the envelope does prove (estate-side)

- **Request integrity:** `request_sha256` plus the stored `jp` lets anyone recompute that the judge saw exactly these bytes.
- **Response integrity:** `response_sha256` lets anyone confirm the stored blob is unchanged since write time, and that `text_sha256` derives from it.
- **Ledger integrity:** `prev_row_sha256` means any edit to a banked row breaks the chain from that row forward.
- **What it does not prove:** that the raw blob came from the network. A seat can fabricate a self-consistent raw JSON. Section 2c closes this gap.

### 2c. Protocol changes that close the gap, ranked by landability

1. **Local judge (landable today, closes the judge side of Q30).**
   - Run the judge on local open weights (llama.cpp `.gguf`).
   - Record `weights_ref.level = local_hashed` with the sha256 of the file on disk, hashed at process start and re-hashed after the call.
   - This removes Nous from the judge path entirely, so "provider serves both" no longer holds.
   - Contestants stay at `published_ref` or `unattestable`. That is acceptable because a contestant swap only corrupts the *attribution* of a verdict, not the judging.
2. **Provider lookup by `response_id` (request to Nous, UNVERIFIED availability).**
   - A GET endpoint that returns `{model, created, usage}` for an id.
   - This defeats a seat fabricating `fresh_api` rows (Q32). It does not defeat the provider itself.
3. **Provider-signed receipts (request to Nous).**
   - An Ed25519 signature over canonical JSON `{request_sha256, response_sha256, response_id, model, weights_digest, created}`, with a published key.
   - This yields `level: provider_signed`. It binds the provider's claim, so a swap becomes a signed lie rather than a silent one.
4. **TEE remote attestation.** An attestation quote over the weights digest and the request digest. This is the only approach that binds weights against a dishonest provider. It is out of scope for this estate.

### 2d. Detection layer (not proof): behavioral canary

- **Method:**
  - Run a daily fixed canary set: 8 prompts, `temperature: 0`, `max_tokens: 64`, per slug.
  - Store the outputs.
  - Flag `weights_epoch_suspect` when token-level similarity to the previous epoch drops below a threshold calibrated on 7 days of same-slug runs.
- **Why a threshold and not hashes:** batched serving is nondeterministic even at temperature 0, so exact-hash comparison would false-positive (see N6).
- **What a flag triggers:** epoch partitioning of verdict rows, not a FAIL.

---

## 3. Upgrade path for the hidden bank: from "prevented" to "detectable post-hoc"

### 3a. The premise is weaker than D6 states

"Provably unseen" holds only against model pretraining. It does not hold against anything with repo read access, because the hidden half can be rebuilt from tracked code (G9). That includes every seat:

- `build_entries` renders bodies from the tracked `SHAPES`/`MATERIALS`.
- `split_order` is deterministic.
- The `split_rule` string is printed into the tracked manifest.

Separately, every hidden draw that is fired is exposed to the provider. Prevention is therefore not achievable. Detection is.

### 3b. Minimal change 1: the draw row records exposure

Patch `tools/ask_bank.py:cmd_draw` at the append anchored by `"note": note or ""})`:

```python
    text, _ = read_material(root, entry["material_path"])
    rendered = render(entry, text)
    prior = drawn.count(entry["ask_id"])
    append_jsonl(hidden_dir(root) / "draws.jsonl", {
        "draw_id": draw_id, "ask_id": entry["ask_id"], "half": half,
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "note": note or "",
        "prior_draws_of_ask": prior,
        "rendered_sha256": sha_text(rendered),
        "body_sha256": sha_text(entry["body"]),
        "derivable_from_tracked": True})   # v1: generator + split rule tracked (G9)
    if reveal:
        print(f"[ask_bank {man['version_id']} draw {draw_id} "
              f"{entry['ask_id']}]", file=sys.stderr)
        print(rendered)
```

The existing `text, _ = read_material(...)` inside `if reveal:` moves above the append. Output bytes are unchanged.

### 3c. Minimal change 2: the duel row links to its draw

`ask.ask_sha256` (section 1a) must equal the draw's `rendered_sha256`. The driver passes `ask_draw_id`.

`ask_visibility` is computed by the verifier, never by the driver:

| Class | Rule |
|---|---|
| `hidden_first_draw` | The `ask_sha256` matches a hidden draw with `prior_draws_of_ask == 0`, and the bank was not derivable at draw time. |
| `hidden_derivable` | Same as above, but `derivable_from_tracked` is true. This covers all of v1, D6 included. |
| `hidden_redraw` | The match has `prior_draws_of_ask > 0`. |
| `train` | Matches a train-half draw. |
| `plain_sight` | No draw matches. This covers all W8, LW9, and V1 rows. |
| `unknown` | Legacy row without `ask_sha256`. All 76 current rows fall here. |

### 3d. Minimal change 3: `ask_bank.py exposure` subcommand

- For each hidden entry, take 64-char shingles of `body`.
- Search `git ls-files` contents and `logs/duel/raw/*` contestant outputs for those shingles.
- Any hit dated after the draw `ts` marks the ask `exposed_at=<path>`, which demotes the class.
- **Exit codes** mirror `verify`: 0 clean, 1 exposure found, 2 cannot check.

### 3e. Making the bank genuinely hidden (v2)

- Add a per-bank secret salt at `hidden/salt.bin` (gitignored).
- Change the split to `sha256(salt + ask_id)`.
- Add angles drawn from a gitignored file.

After this, `derivable_from_tracked` becomes false. This is a later change and is not required for detection.

### 3f. Post-hoc contamination statistic (what makes D6-style claims testable)

- For each contender pair, compute the win rate per `ask_visibility` class.
- Flag `contamination_signal` when the `plain_sight` and `hidden_*` rates differ by a two-proportion test at p<0.05.
- **Reporting conditions:** the judge slug, its `weights_ref.level`, and the date range.
- At D6's n=3 per arm, Fisher's exact test on 3-0 vs 0-3 gives p=0.10 (two-sided). That is not significant, which matches D6's own caveat.

---

## 4. Patch hunks: `tools/duel_harness.py`

```python
# after imports
RAW_DIR = ROOT / "logs" / "duel" / "raw"
SEAT_ENV = "MAG_SEAT_MODEL"
REGISTRY = ROOT / "configs" / "model_registry.json"

def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

# call(): replace `with urllib.request.urlopen(req, timeout=300) as r: return json.load(r)`
    with urllib.request.urlopen(req, timeout=300) as r:
        raw = r.read()
    resp = json.loads(raw)
    resp["_prov"] = {"request_sha256": _sha(body), "response_sha256": _sha(raw), "_raw": raw}
    return resp

# new: fire_prov (fire() becomes a wrapper: `return fire_prov(...)[:2]`, so callers keep (content, cost))
def fire_prov(model, prompt, keys, tag, caller=call, max_tokens=CONTENDER_TOKENS):
    ...same loop as fire...
            p = resp.pop("_prov", None)
            if p is None:  # injected test caller
                raw = json.dumps(resp, sort_keys=True).encode()
                p = {"request_sha256": None, "response_sha256": _sha(raw), "_raw": raw}
                origin = "synthetic"
            else:
                origin = "fresh_api"
            RAW_DIR.mkdir(parents=True, exist_ok=True)
            (RAW_DIR / (p["response_sha256"] + ".json")).write_bytes(p["_raw"])
            prov = {"origin": origin, "response_id": resp.get("id"),
                    "response_model": resp.get("model"), "requested_model": model,
                    "family": family_of(model),
                    "request_sha256": p["request_sha256"],
                    "response_sha256": p["response_sha256"],
                    "text_sha256": _sha(content.encode("utf-8")),
                    "system_fingerprint": resp.get("system_fingerprint"),
                    "weights_ref": weights_ref(model)}
            return content, cost, prov
```

**In `run_duel`:**
- New keyword arguments: `a_prov=None, b_prov=None, ask_draw_id=None`.
- In live mode, use `fire_prov`.
- In retro mode, set `a_prov = a_prov or {"origin": "unknown", "text_sha256": _sha(a_text.encode())}` (likewise for b).
- The judge always goes through `fire_prov`.
- The row gains the section 1a fields.
- `prev_row_sha256` is the sha256 of the last non-empty line of `out_path`, or `None` when the ledger is empty.

**In `main()`:** in retro mode, pass `a_prov=a_row.get("prov")` and `b_prov=b_row.get("prov")`.

**In `run_rejudge`:** add this gate after the existing `_chars` loop:

```python
    for side, text in (("a", a_text), ("b", b_text)):
        want = ((orig.get("prov") or {}).get(side) or {}).get("text_sha256")
        if want is not None and hashlib.sha256(text.encode("utf-8")).hexdigest() != want:
            raise ValueError(f"answer drift on {orig.get('ask_id')}: {side} text_sha256 mismatch")
```

### New `tools/duel_verify.py` checks

Exit codes: 0 ok, 1 FAIL, 2 cannot verify.

| ID | Check | Result if violated |
|---|---|---|
| V1 | Hash chain: each `prev_row_sha256` matches the prior line's bytes. | FAIL |
| V2 | For each `prov.*`, the raw blob exists and `sha256(blob) == response_sha256`. | FAIL. A missing blob is CANNOT. |
| V3 | `sha256(blob.choices[0].message.content) == text_sha256` | FAIL |
| V4 | `blob.id == response_id` and `blob.model == response_model` | FAIL |
| V5 | `response_model` matches `registry[requested_model].echo_re` and `family_of(response_model) == family`. A family mismatch is FAIL. An echo variant inside `echo_re` passes with a note. | FAIL on family mismatch |
| V6 | `response_id` is unique across the ledger, judge entries included. | FAIL |
| V7 | `weights_ref` equals `registry[requested_model]` as of the registry's git revision at the row's `ts`. | FAIL |
| V8 | `ask_visibility` is recomputed from draws (section 3c). A row-claimed value that differs from the recomputed one is FAIL. | FAIL |
| V9 | `judge_prompt_sha256` equals the recomputed `judge_prompt(...)` when task and texts are available. | FAIL |
| V10 | `router_eligible` equals the recomputed rule. | FAIL |

Legacy rows with no `schema` produce verdict `UNKNOWN`. They are reported but are neither FAIL nor eligible.

---

## 5. Test plan (`tests/test_duel_provenance.py`, all offline via injected `caller`)

### Positive: tampering must FAIL

| ID | Setup | Expected |
|---|---|---|
| P1 | Bank a row, then edit `prov.judge.weights_ref.value` in place. | V1 chain break at that row plus V7 registry mismatch, so FAIL. |
| P2 | Overwrite the raw blob with one changed byte. | V2 FAIL |
| P3 | Rejudge with a same-length text that has one character swapped (`"abc"` to `"abd"`). | The current length gate passes (G5). The new `text_sha256` gate raises `ValueError`. |
| P4 | Contender row with `origin: fresh_api` and no raw blob. | V2 CANNOT, exit 2, so not eligible. |
| P5 | The fake response echoes `qwen/qwen3.8-max-prime` for a request to `z-ai/glm-5.3-prime`. | V5 family mismatch, so FAIL. This is the visible weights-swap case. |
| P6 | `MAG_SEAT_MODEL=z-ai/glm-5.3-prime` with judge `z-ai/glm-5.3-prime`. This reproduces AJ1's confound (G7). | `self_judge: true`, `router_eligible: false` |
| P7 | The row claims `ask_visibility: hidden_first_draw`, but the draw has `prior_draws_of_ask: 1`. | V8 FAIL |
| P8 | Two rows share a `response_id`, simulating a duplicated or forged reply. | V6 FAIL |
| P9 | A hidden body shingle is written into a tracked file after the draw `ts`. | `ask_bank.py exposure` exits 1. |

### Negative: legitimate churn must NOT false-positive

| ID | Setup | Expected |
|---|---|---|
| N1 | Request `z-ai/glm-5.3-prime`, echo `z-ai/glm-5.3-prime-20261001`. | V5 passes with note `model_echo_drift`. Exit 0. |
| N2 | The id format changes from `chatcmpl-...` to `gen-...` between calls. | Pass. Ids are opaque, and only presence and uniqueness are checked. |
| N3 | `system_fingerprint` absent or null. | Pass. Recorded as null, and the level is unchanged. |
| N4 | The 76 legacy rows with no `schema`. | Verdict `UNKNOWN`, exit 0, and readers do not raise. |
| N5 | The registry `published_ref` is bumped in a commit dated before the row's `ts`. | V7 uses the revision at `ts`, so it passes. Rows are partitioned by epoch. |
| N6 | Canary outputs at temperature 0 differ by a few tokens across days. | Similarity stays above the calibrated threshold, so there is no `weights_epoch_suspect`. |
| N7 | Attempt 1 hits HTTP 500, then attempt 2 succeeds with a new id via the next key. | Only the attempt-2 prov is banked, and V6 passes. |
| N8 | Material checked out with CRLF. | No drift. This existing semantics is pinned by `read_material`: "a git autocrlf checkout flip must never fake drift". |
| N9 | The same hidden ask is drawn twice by design, with a recorded note. | The second row is classified `hidden_redraw`. That is a pass, not a FAIL. |

---

## 6. Falsifier

**The spec is falsified if either of the following happens:**

- **(a) Undetected tampering.** Any of P1 to P9 exits 0 against a ledger tampered as described.
- **(b) False positives on churn.** Over 7 consecutive days of real gateway traffic, with the registry unchanged and no provider weight change announced, `duel_verify.py` exits 1 on any row whose only difference is a model echo inside `echo_re`, an id-format change, or a null fingerprint.

**Conditions:**
- **Instrument:** `duel_verify.py` at the landing commit.
- **Context:** Nous gateway, ember-1 judge or local judge.
- **Moment:** a 7-day window starting at landing.

**Scope limit, stated so it cannot be mistaken for a claim:** passing both checks does **not** show that Nous served the claimed weights. Per section 2a, only `local_hashed`, `provider_signed`, or TEE levels can show that. A seat that fabricates a self-consistent raw blob also passes estate-side verification. Only provider lookup or a signed receipt (section 2c, items 2 and 3) can catch that case.
