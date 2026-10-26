# DUEL2_train_08 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# Falsification pass: docs/ref/CORE_MEMORY_PROTOCOL.md

## 1. Status: the material body was not delivered (UNVERIFIED)

The CONTRACT gives only the path, the sha256, and a truncated first line:

> `You are a falsification engineer. Below is the full text of docs/ref/CORE_MEMORY_PROTOCOL.md (CORE MEMORY PROTOCOL, the `

No protocol text follows it, so I have no bytes to cite. Under the estate laws, any claim I made about what the protocol says would be uncitable and therefore UNVERIFIED. I will not invent protocol clauses and then "falsify" them.

- **Known:** the path, the expected sha256 (`f014e1bda26ec92d4b4f5704d2fb9bf73826d1db8add609ff99a21693e107977`), and the truncated first line above.
- **Unknown:** every normative claim, line number, and numeric threshold in the document.
- **Instrument and moment:** this assessment rests on the prompt as received at answer time, with no file access. It says nothing about the file on disk.

## 2. Deliverable: a landable falsification harness

A seat with the file can apply this as-is. It does three things:

1. Refuses to run unless the bytes match the contract hash.
2. Extracts every falsifiable claim with its `file:line` and quoted bytes.
3. Emits a verdict table skeleton that cannot be filled in without naming instrument, moment, and context.

### 2.1 `tools/coremem_claims.py`

```python
#!/usr/bin/env python3
"""Extract falsifiable claims from CORE_MEMORY_PROTOCOL.md with file:line."""
import hashlib, re, sys, json

EXPECT = "f014e1bda26ec92d4b4f5704d2fb9bf73826d1db8add609ff99a21693e107977"
path = sys.argv[1] if len(sys.argv) > 1 else "docs/ref/CORE_MEMORY_PROTOCOL.md"

raw = open(path, "rb").read()
got = hashlib.sha256(raw).hexdigest()
if got != EXPECT:
    sys.stderr.write(f"HASH MISMATCH: expected {EXPECT} got {got}\n")
    sys.exit(2)

KINDS = [
    ("normative", re.compile(r"\b(MUST NOT|MUST|SHALL NOT|SHALL|NEVER|ALWAYS)\b")),
    ("quantified", re.compile(r"\b(exactly|only|at most|at least|every|never|always)\b", re.I)),
    ("numeric", re.compile(r"\d")),
    ("reference", re.compile(r"`[^`]+\.(md|py|sh|json|toml|yaml)[^`]*`|\b\w+\.\w+:\d+\b")),
]

out = []
for n, line in enumerate(raw.decode("utf-8").splitlines(), 1):
    kinds = [k for k, rx in KINDS if rx.search(line)]
    if kinds:
        out.append({"cite": f"{path}:{n}", "kinds": kinds, "quote": line})

for row in out:
    print(json.dumps(row, ensure_ascii=False))
sys.stderr.write(f"{len(out)} candidate claims\n")
```

### 2.2 Verdict row (every claim gets one, no blanks allowed)

```
cite:        docs/ref/CORE_MEMORY_PROTOCOL.md:<N>
quote:       "<exact bytes>"
claim_type:  normative | quantified | numeric | reference
attack:      <the concrete input, state, or sequence that would break it>
instrument:  <command or tool that runs the attack>
moment:      <commit sha / timestamp / process state when run>
context:     <env, flags, data size, concurrency, who is the actor>
observed:    <raw output, quoted>
verdict:     HOLDS | FALSIFIED | UNTESTABLE-AS-WRITTEN | UNVERIFIED
```

### 2.3 Attack classes to apply to each extracted claim

For any memory protocol, run each class against each claim:

1. **Reference rot:** every cited file, symbol, or `file:line` must resolve. Check with `grep -n` or `sed -n 'Np'` against the commit named in `moment`.
2. **Unfalsifiable wording:** a "MUST" with no observable consequence is UNTESTABLE-AS-WRITTEN. That verdict is itself a finding.
3. **Ordering and concurrency:** if a rule implies write-then-read, test two writers and a crash between steps.
4. **Boundary numbers:** for every threshold, test N-1, N, N+1.
5. **Contradiction pairs:** find two claims that cannot both hold, and cite both lines.
6. **Absence claims** ("never", "only"): search for a counterexample in the repo. A clean grep is a verdict only if the query and scope are stated.

### 2.4 Worked examples of row quality

These are illustrative only. They are not claims about the real document.

**Negative (rejected):**
```
claim: "Memory writes are durable."   verdict: HOLDS
```
This has no cite, no instrument, no moment, and no context. It violates "a verdict without its conditions is not a verdict."

**Positive (accepted shape):**
```
cite:       <file>:<N>   quote: "<bytes>"
attack:     kill -9 between append and fsync
instrument: tools/crashtest.sh --writers 1
moment:     commit <sha>, 2025-xx-xx
context:    ext4, local disk, single process
observed:   "<last 3 output lines>"
verdict:    FALSIFIED
```

## 3. Falsifier for this deliverable

The harness is wrong or useless if either of these happens:

- Run on a file whose sha256 equals the contract hash, it emits **zero** candidate claims. A protocol document with no normative or numeric statements would contradict the premise of the ask.
- A reviewer finds a normative sentence in the file, by `grep -nE 'MUST|SHALL|NEVER|ALWAYS'`, that the extractor did not list.

## 4. What I need to complete the falsification

Paste the full file body, or run the script and return its JSON lines. I will then produce filled verdict rows with real `file:line` citations. Until then, every verdict about the protocol's content is **UNVERIFIED**.
