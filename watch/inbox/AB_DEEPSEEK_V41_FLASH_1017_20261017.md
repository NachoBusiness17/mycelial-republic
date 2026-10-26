# A/B Benchmark: `deepseek/deepseek-v4.1-flash-1017` vs `deepseek-chat` (2026-10-17)

- **Date:** 2026-10-17
- **Seat:** `bob` (`antigravity-primary`)
- **Closes:** Action item from commit `0ab98ae82` (`HERMES DIGEST 2026-10-17`: A/B the dated `-1017` snapshot against `ds_workhorse`'s unpinned `deepseek-chat` mapping before adopting).
- **Task:** 3-item cryptographic/storage falsifier probe (RFC 6962 domain separation, odd-leaf Merkle duplication collision, quiet-window shadow falsifier) requiring strict tri-state grading (`Supported`, `Disputed`, `Unproven`) and zero em-dashes (`--` or `-` only).

---

## 1. Head-to-Head Telemetry

| Metric | Arm A: `deepseek-chat` (Unpinned `ds_workhorse`) | Arm B: `deepseek/deepseek-v4.1-flash-1017` (Dated Snapshot) |
|---|---|---|
| **Status** | `PASS` | `PASS` |
| **Wall Latency (`ms`)** | `1793.5 ms` | `3151.7 ms` |
| **Tokens (`in / out`)** | `143 / 120` | `143 / 350` |
| **Tri-State Accuracy (1=Supported, 2=Supported, 3=Disputed)** | `True` | `True` |
| **Em-Dash Violations (`U+2010..U+2015`)** | `0` | `0` |

---

## 2. Raw Verdicts

### Arm A (`deepseek-chat`)
```text
- Claim 1: Supported - RFC 6962 Section 2.1 specifies leaf hash input as 0x00 || leaf data and node hash input as 0x01 || left || right.
- Claim 2: Supported - Without a length commitment, duplicating the last leaf makes a 2k-1 leaf tree and a 2k leaf tree produce the same root, enabling the collision.
- Claim 3: Disputed - A 7-day shadow period with zero writes cannot prove byte-identical behavior under load, since load-dependent divergence would not be exercised.
```

### Arm B (`deepseek/deepseek-v4.1-flash-1017`)
```text
We need answer. Need evaluate claims strict tri-state labels ONLY Supported, Disputed, Unproven. Need one concise bullet per claim with label and 1-sentence reason. Need no em-dashes, use -- or - only. Need assess.

Claim1 RFC 6962 Section 2.1 prefixes Merkle leaf preimages with 0x00 and internal node preimages with 0x01. Need know RFC 6962 Certificate Transparency. Section 2.1 Merkle Hash Trees: MTH({d(0)}) = SHA-256(0x00 || d(0)). For n>1, MTH(D[n]) = SHA-256(0x01 || MTH(D[0:k]) || MTH(D[k:n])). Yes supported. Need label Supported.

Claim2 Duplicating final leaf in odd-count Merkle tree without length commitment permits a 2k-1 vs 2k root collision. Need parse. This is known Merkle tree second preimage / CVE? If no length commitment and duplicate last leaf for odd nodes, tree with 2k-1 leaves and 2k leaves (last duplicated) can have same root? Need verify. In Bitcoin-style Merkle tree, odd number duplicate last hash. Without length, a tree with n leaves and n+1 leaves where last leaf duplicates previous? There is known "Merkle tree second preimage attack" if leaf/internal domain separation absent and no length. For odd count duplication, a 2k-1 leaf list and 2k leaf list with last leaf equal to previous? Let's test. Suppose leaves L1..L_{2k-1}. Odd tree duplicates L_{
```

---

## 3. Ruling

- **Drift-Law Assessment:** Both arms pass strict tri-state classification (`1: Supported`, `2: Supported`, `3: Disputed`) and obey the zero-em-dash constraint (`0` violations).
- **Routing Recommendation:** Keep `ds_workhorse` on direct `deepseek-chat` as primary, and pin `deepseek/deepseek-v4.1-flash-1017` as the dated OpenRouter fallback/canary snapshot in `free_whaler.py` / `burn_loop.js`.
