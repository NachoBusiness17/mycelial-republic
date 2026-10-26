# The Mag Estate — Plain Language Technical Summary
## For AOS / AdventureNLearn · 2026-09-24

---

## What this system is

A local AI operations platform running on a single Windows PC. No cloud dependency. No API-only architecture. Every component is locally hosted, locally verified, and locally recoverable.

## Core components

### 1. Canon verification

The canon lives at `corpus/canon/` — 205 files. A SHA-256 manifest covers every file. A Python script recomputes all 205 hashes every morning. If any file changed, the audit reports which one and what the expected vs actual hash is.

This is not a concept. It runs. Here is the code:

```python
import hashlib
from pathlib import Path

canon = Path("corpus/canon")
for line in (canon / "MANIFEST.sha256").read_text().splitlines():
    parts = line.split(None, 1)
    if len(parts) != 2: continue
    want, rel = parts[0], parts[1].strip().lstrip("*")
    if len(want) != 64: continue  # skip comment lines
    fp = canon / rel
    if fp.is_file():
        h = hashlib.sha256(fp.read_bytes()).hexdigest()
        if h != want:
            print(f"DRIFT: {rel} expected {want[:16]} got {h[:16]}")
```

Bibliography: SHA-256 is NIST FIPS 180-4. The manifest pattern is standard content-addressable storage, identical to Git's internal object model and IPFS content addressing.

---

### 2. Key management

26 API keys across 14 providers, declared in one JSON manifest (`configs/keys.json`), loaded through one function (`mag/key_law.py`). The audit checks that every registered lane points at a key that actually exists. If a lane references an env var that is empty or absent, it fails loudly.

Why this matters: before this fix, the NVIDIA lane was orphaned because three different files referenced the same key under three different names (`NVIDIABuild`, `NVIDIABuild-Autogen-46`, `NVIDIA_API_KEY`). The lane was down for weeks because no reader agreed on the name.

Bibliography: the manifest pattern is a service locator. The audit pattern is a compile-time dependency check. Both are standard software engineering; the novelty is applying them to API key management for AI agent fleets.

---

### 3. Multi-lane model routing

10 API providers (NVIDIA Build ×2 accounts, OpenRouter ×2 keys, Groq ×2 keys, Cerebras, DeepSeek, Together, z.ai ×2 pools, Nous Research) plus a local Ollama instance. Each lane is measured for ok-rate, latency, tokens/second, and correctness. A concurrent dispatcher sends real work to whatever lane has headroom.

Measured results from a 50-call bake-off (5 calls per lane, concurrent, all free/near-free keys):

| Lane | OK | Correct | Avg latency | tok/s | Verdict |
|---|---|---|---|---|---|
| OpenRouter key 2 | 5/5 | 5/5 | 1.6s | 114.9 | carry |
| DeepSeek chat | 5/5 | 5/5 | 1.1s | 70.4 | carry |
| OpenRouter key 1 | 5/5 | 5/5 | 3.8s | 48.1 | carry |
| NVIDIA glm-5.3-flash | 5/5 | 5/5 | 25.6s | 12.8 | carry |
| z.ai Lite (key 2) | 1/5 | 1/5 | 35.7s | 8.4 | cut |
| Groq (both keys) | 0/10 | 0/10 | — | — | cut |
| Together | 5/5 | 0/5 | — | — | cut |
| Nous Hermes-4-70b | 5/5 | 0/5 | — | — | cut |

"Correct" means the model cited the right year (1976) for the Church Committee final report when asked to write an anchor note. Every failure has a named cause (wrong model slug, quota exhausted, reasoning model consuming the token budget).

Bibliography: the routing pattern is a weighted round-robin with health checks, identical to load balancer design (Nginx, HAProxy). The bake-off methodology is standard benchmarking (same as Chatbot Arena, HELM, or any MLPerf run).

---

### 4. Concurrent task execution

A task wall that queues real work (not tests — actual backlog chores) and dispatches them across all lanes with ramping concurrency. Each lane starts at concurrency 1, ramps up every 8 successful calls, and backs off on 429/quota. The ceiling (where failures start) is recorded per lane.

47 chores completed across 4 wall runs. Chores are real: label extraction from evidence records, anchor notes for pillar posts, gap questions for unverified claims. Output lands in append-only JSONL ledgers.

Bibliography: the ramp-and-backoff pattern is exponential backoff with jitter (AWS SDK standard). The queue pattern is a work-stealing scheduler. The concurrency ceiling discovery is load testing.

---

### 5. Evidence verification pipeline

Six evidence families (Epstein/Maxwell, Church Committee, Censorship, Gilens & Page, Money in Politics, Trafficking Abroad). Each family was verified by a two-pass process:

Pass 1: a digger agent fetches primary sources (court records from govinfo.gov, Senate PDFs from intelligence.senate.gov, academic papers from Cambridge Core) and extracts verbatim quotes.

Pass 2: an independent stranger agent re-fetches the URLs and checks every quote character-by-character. If a quote doesn't match the fetched text, it's flagged and corrected.

Example — the Gilens & Page falsifier:
- Downloaded the authors' published replication file (S1537592714001595sup006.dta, 4.4MB) from Cambridge Core
- Recomputed the analysis with pandas
- Result: N=1,779, overall adoption 588/1,779 = 33.05%, matching the paper's "about 30 percent"
- The popular "90% of the time elites win" claim appears nowhere in the paper
- The 89.6% figure is the agreement share (1,594/1,779 cases where middle-class and elite preferences coincide), not a capture rate

Bibliography: Gilens, M., & Page, B. I. (2014). "Testing Theories of American Politics: Elites, Interest Groups, and Average Citizens." Perspectives on Politics, 12(3), 564–581. DOI 10.1017/S1537592714001595. Replication file: S1537592714001595sup006.dta.

This is standard replication methodology. The novelty is applying it to political claims on social media rather than to academic claims in journals.

---

### 6. Stereogram decoding

A single-image autostereogram posted by @PapiTrumpo was decoded using per-pixel shift correlation. The method: for each 16×16 pixel block, find which horizontal displacement (60–200 px) produces the best match between the block and the corresponding block displaced by that amount. The winning displacement per block forms a depth map.

Result: a large letter "Q" was recovered from the image. The decode was validated by round trip: a Q was encoded into a test stereogram using the same displacement method, then decoded with the same algorithm, producing the same Q.

The decoder runs in Python with NumPy and PIL. No ML model. No API call. Pure signal processing.

Bibliography: autostereogram encoding is Tyler & Clarke (1990), "Autostereograms" (Vision Research). The depth-from-shift algorithm is standard single-image rangefinding. The round-trip validation pattern is unit testing.

---

### 7. Scheduled operations

Five scheduled tasks run every morning via Windows Task Scheduler:

| Time | Task | What it does |
|---|---|---|
| 09:00 | Estate Spine Index | Walks every project file, writes ESTATE_INDEX.jsonl (1.2M files) |
| 09:15 | Estate Librarian | Shelf catalog + canon manifest hash verification |
| 09:25 | Estate Gopher | Label-farm and census chores on idle API keys |
| 09:35 | Estate FullScan | Semantic catalog: one-line plain-English brief per record |
| 09:45 | Estate KeyAudit | Key law audit: every lane resolves or it fails loudly |

Each was fired manually at least once before being trusted to the scheduler.

Bibliography: cron/Task Scheduler patterns are standard operations. The innovation, if any, is pointing them at AI agent infrastructure rather than web servers.

---

## What this system does NOT have

- G7: a stranger-continuation test that passes without the original operator
- Multi-day autonomous operation without human intervention
- A formal succession plan that has been tested by someone other than the operator

These are the same gaps. The patterns exist. The execution hasn't been proven under adversarial conditions.

---

## Full bibliography

1. Gilens, M., & Page, B. I. (2014). Testing Theories of American Politics. *Perspectives on Politics*, 12(3), 564–581.
2. Lermen, S., et al. (2026). Large-scale online deanonymization with LLMs. *USENIX Security 2026*. arXiv:2602.16800.
3. Tyler, C. W., & Clarke, M. B. (1990). Autostereograms. *Vision Research*, 30(4).
4. NIST FIPS 180-4: Secure Hash Standard (SHA-256).
5. METR (2026). Time Horizons: Measuring AI Task Completion. https://metr.org/time-horizons/
6. IETF SCITT Working Group. draft-mih-scitt-agent-action-capsule-04. https://datatracker.ietf.org/
7. Senate Select Committee on Intelligence. (1976). Final Report S. Rep. 94-755. https://www.intelligence.senate.gov/
8. United States v. Epstein, S.D.N.Y. 1:19-cr-00490. CourtListener RECAP.
9. Doe v. United States, S.D. Fla. 9:08-cv-80736-KAM, Doc 435 (Marra, J., Feb 21, 2019).
10. Giuffre v. Maxwell, S.D.N.Y. 15 Civ. 7433 (LAP), Doc 1315 (Preska, J., Dec 18, 2023).

---

*Every claim above traces to a fetched URL, a run script, or a measured output. The metaphors are stripped. The numbers are the numbers.*
