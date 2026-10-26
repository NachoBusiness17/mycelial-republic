# SUBSTANCE_moonshot_primer (anthropic/claude-opus-5.5, turn 1, channel: content)

# THE PRIMER LEG: moonshot definition

<citation_key>

**Citation rules for this document**

- Evidence docs are cited as `file :: section` with quoted bytes. Their line numbers are UNVERIFIED because the evidence arrived without line numbers.
- Every code `file:line` below is a REPORT carried by an evidence doc. This seat did not read those bytes, so each one is marked `UNVERIFIED (reported by X)`.
- The DND module's dice preimage law is not in the evidence. Its exact bytes are UNVERIFIED. Part 4 adopts only the shape the contract states: sha256 preimage, chain_tip in every preimage.

</citation_key>

---

## 1. THE MOONSHOT STATED

A child holds a printed book. Every page carries a small code. When she points a phone at page 3, the book answers about page 3 and knows what she said on page 2. It never invents anything about its own printed words, because those words are frozen and fingerprinted. It grows only where she has actually been: pages she lingers on gain detail, and pages she skips stay fogged.

When she finishes, the next printing of her book is thicker exactly where she walked. Every page carries an identity that anyone holding her book's manifest can recompute from the page bytes and the estate's chain tip. Each physical book also carries a hard compute purse, so the cost of her book is a number printed on its last page.

---

## 2. THE 5 W'S

### WHO builds each layer (wire, don't build)

| Layer | Organ that owns it | Status per evidence |
|---|---|---|
| Frozen edition identity | Verkle chain + tip (`memory/biography/verkle_tip.json`, `verkle_chain.jsonl`) | Listed as backup DNA: docs/DNA.md :: "Backup DNA (private)" |
| Tangible render (PDF) | Export layer, `POST /api/v1/export` `{session_id, pdf?, visual?}` | docs/DNA.md :: "Optional derived". The export endpoint exists only per DNA.md, so it is UNVERIFIED as runnable. |
| Reading instrument (does the book fabricate about itself?) | FOG-SCAN v0 on the cheap parliament | Specced, not run: closed_corpus_doctrine :: "THE INSTRUMENT" |
| Fog and patina (growth by visitation) | `dfhack/mountain_visit.py` | "still on bob; lands with ingress" (closed_corpus_doctrine :: "OWED") |
| Viewport for scans | Live board, `:8765` | docs/DNA.md :: "Lab improves mid-session comfort (live board, companion, :8765)" |
| Cadence and loud failure | Heartbeat pattern of `scripts/estate_walk_daily.ps1` | next.md :: Move 4: "loud-failure line to memory/attention.md" |
| Review of the only new glue | `tools/code_swarm.py` | COLD_HOT_RESULT :: "the standing swarm-review organ, unchanged" |

The only new code is a single file, `primer_page_id.py` (Part 4 reference, about 40 lines), plus one visits ledger.

<example type="negative">
A new "Primer store" alongside residual is forbidden. DNA.md :: Promise row "One vertex" says: "New features = edges (panel/field/export), never a second DNA store."
</example>

### WHAT is the minimum magical demo

1. **The book.** A 12-page paper booklet with a QR on each page footer.
2. **The scan.** The holder scans page 2 and answers its one question out loud or by tapping a choice.
3. **The memory.** The holder scans page 3. The screen shows page 3's printed text, plus one generated line that names her page-2 answer.
4. **The regrowth.** A week later she receives edition 2, printed. The pages she visited carry new paragraphs grown from her answers. The pages she never scanned are byte-identical to edition 1.
5. **The proof.** Her parent asks, "did it make anything up about what's printed?" The answer is checkable: in-book fabrication was measured at zero (Rung 2).

<example type="positive">
"Page 3 remembers you picked the lantern." The response is bound to a chained visit row.
</example>

<example type="negative">
A chatbot that happens to know the book's title. There is no page identity, no visit binding, and no regrowth. That is a reader app, not the Primer.
</example>

### WHEN each layer lands (weeks, at current cadence)

The cadence is corrected by its own receipts. next.md shows ordered 48h moves slipping: Move 3 "CARDS EXIST, PORTS NOT FIRED", Move 5 "NOT RUN". Each week below therefore assumes one banked rung, not two.

| Week | Lands |
|---|---|
| 0 (today) | Rung 1: frozen edition plus independently recomputed page ids |
| 1 | Rung 2: fog-scan calibration of the book |
| 2 | Rung 3: on-screen visitation loop, chained |
| 3-4 | Rung 4: paper plus phone. Gated on hardware, see Part 5. |
| 5-6 | Rung 5: one child, edition 2 printed |

`mountain_visit.py` ingress is a dependency of Rung 5 patina. If bob ingress has not landed by week 4, Rung 5 uses the plain visit-count rule in Rung 3 instead, and the gap is named.

### WHERE frozen bytes live and where visitation grows them

The closed-corpus doctrine is applied as follows. The proposed paths do not exist yet.

| Regime | Doctrine clause | Location (PROPOSED) | Rule |
|---|---|---|---|
| FROZEN (calibrate) | "A frozen corpus under a known-good instrument should produce ZERO fabrication" | `corpus/primer/<book_id>/edition_<n>/page_<k>.txt` + `manifest.json` | Never edited after freeze. A new edition is a new directory. |
| GROWN (discover) | "GROW TO DISCOVER ... Staleness here is debt by law" | `memory/primer/visits.jsonl` (chained, local) | Append-only. Raw responses never leave the machine. |
| DERIVED (sticker) | DNA.md: "derived/ regenerates on demand" | `derived/primer/<book_id>/edition_<n>.pdf` | Regenerable from the frozen pages. Never source of truth. |
| FRONTIER | "THE DELTA IS THE FRONTIER" | Fog-scan output per page | Pages where the mesh invents are where the next edition grows. |

**Privacy law binding.** DNA.md :: "Set and forget" says: "Law | Private residual never remote". A child's raw answers are private residual. Only their sha256 commitments enter page identity.

**Compute tied to the asset.** Every paid call is charged to a `book_id` purse, default cap $1.00. Rows go in the existing usage-ledger pattern (`memory/runs/model_garden/usage.jsonl` per COLD_HOT_RESULT :: "Artifacts"), extended with a `book_id` field. The purse total prints on the book's last page.

### WHY this and not the other candidates

The other moonshot candidates are not in the evidence; their list is UNVERIFIED. The case for this leg rests on three things the evidence does show:

1. **It answers the estate's one open question from outside.** The doctrine quotes the socratic mesh: "what OUTSIDE signal would tell the estate its ground truth is wrong?" A child's reaction is an outside signal the estate cannot fabricate.
2. **It forces a consumer onto a write-only estate.** next.md :: Move 5 records the attention ledger at "exactly 2 rows, both self-cast" and notes "nonzero, but not consumed". A book that must render page k+1 from page k's visit is a consumer by construction.
3. **It closes owed debts rather than opening new ones.** FOG-SCAN v0 ("ungated by anything but cost") and `mountain_visit.py` (owed) are both on the ladder. The work lands organs already promised.

---

## 3. THE FALSIFIABLE LADDER

### Rung 1: Frozen edition, recomputed by a second hand (startable TODAY, $0)

**What to do**

1. Take 12 text pages from on-disk bytes. A public-domain children's text is preferred, but whether one exists on disk is UNVERIFIED. The fallback is 12 session-card blurbs ("session_card: title, blurb, bullets", docs/DNA.md :: "Create"). The content does not matter at this rung; identity does.
2. Canonicalize the pages, read the tip from `memory/biography/verkle_tip.json`, and compute the `book_id` and all 12 `page_id`s per Part 4.
3. Write `manifest.json` (field names in Part 4).
4. A second implementation recomputes all ids from the manifest and the page files only. It can be a different seat, or the same seat in a fresh process with no shared import.
5. Optionally render a PDF through the export endpoint. A failed render does not fail the rung.

**Receipt.** `watch/inbox/primer/R1_frozen_edition.md` containing:

- the tip value quoted as bytes, plus the JSON key it was read from (that key is UNVERIFIED until quoted);
- 12 page ids from implementation A;
- 12 page ids from implementation B;
- a diff that should be empty.

**Kill conditions**

- Any A/B mismatch means the Part 4 spec is ambiguous. Stop and fix the spec before Rung 2.
- If the tip is not a stable string across two reads with no landing in between, the anchor is wrong. Stop.

### Rung 2: Freeze-to-calibrate the book (week 1, cap $4)

**What to do.** Run FOG-SCAN v0 over the frozen edition:

- 50 probes whose answers are on the pages;
- 50 probes whose answers are off the pages;
- the cheap parliament as the instrument.

**Measurement conditions.** The "~$0.04/question" cost is the doctrine's estimate, not a measured receipt. Record the actual model ids, the date, and the frozen edition hash in the receipt.

**Receipt.** Fabrication rate on in-book probes, and the off-book rate, per page.

**Kill condition.** In-book fabrication above 0 out of 50 is INSTRUMENT ERROR by the doctrine. The instrument may not speak for the book until the cause is fixed. The doctrine says "any fabrication it does produce is INSTRUMENT ERROR."

### Rung 3: Visitation loop on screen (week 2, cap $1 against a test book_id)

**What to do.** Add one route on the `:8765` board: `/primer/<page_id>`.

- A visit appends a chained row to `visits.jsonl` (Part 4) and updates that page's `visit_root`.
- The render of page k+1 includes one generated line conditioned only on (frozen page k+1, the visit rows for pages up to k).

**Receipt.** Ten scripted visits. A replay script must reproduce every `visit_root` from `visits.jsonl` alone.

**Kill conditions**

- Any `visit_root` that does not replay.
- Any generated line that cites a page the walker did not visit. That is fabrication against the frozen set, the Rung 2 failure, now live.

### Rung 4: Paper and phone (weeks 3-4, hardware-gated, see Part 5)

**What to do**

1. Print the booklet with a QR on each page. The QR encodes `https://<lan-or-tailnet-host>/primer/<page_id>`. Tailscale reachability is cited as an available path in next.md :: W1 option C.
2. A non-technical adult runs 3 attempts.

**Receipt.** For each attempt: wall time from scan to rendered response, plus the chained row.

**Kill condition.** If a non-technical adult fails scan-to-response in under 30 s in any of the 3 attempts, the tangible loop is not yet magic. Fix the transport before involving a child.

### Rung 5: One child, edition 2 (weeks 5-6, operator-consented household only)

**What to do**

1. The child reads edition 1 and scans freely.
2. Freeze edition 2. Each visited page gains content grown from its visits: patina via `mountain_visit.py` if it has ingressed, else visit-count. Unvisited pages are byte-identical to edition 1.
3. Print edition 2.

**Receipt contents**

- the edition 2 manifest;
- third-party recompute of all `page_id`s, with an empty diff;
- the pre-registered question "did the book remember you?" and the child's answer, recorded verbatim;
- the purse total.

**Kill conditions**

- A "no" or a shrug to the pre-registered question means the demo is not magical, and the ladder re-grades from Rung 3.
- The doctrine's own falsifier: if the Rung 2 fog map does not predict which pages the child visited most, the fog map is theater for books.

---

## 4. THE DICE-LAW CLAUSE: page identity spec `primer.page.v1`

The dice law shape (sha256 preimage, chain_tip in every preimage) is taken from the contract. The DND module's own bytes are UNVERIFIED. If they differ in field order or encoding, this spec defers to them, and Rung 1 is re-run.

### Canonical encodings

| Item | Rule |
|---|---|
| Text | UTF-8, NFC, LF line endings, trailing spaces/tabs stripped per line, exactly one terminal LF |
| Hashes | sha256, lowercase hex, 64 chars |
| Integers | Decimal ASCII, no sign, no leading zeros |
| `ZERO` | 64 `0` characters |
| Preimage | ASCII fields joined by `\n`, with a terminal `\n` |

### Identities

```
holder_commit = sha256( holder_salt )                       # salt stays local, never printed
book_id       = sha256( "primer.book.v1\n" genesis_chain_tip "\n" manifest_sha "\n" holder_commit "\n" )
content_sha   = sha256( canon_text(page_k) )
page_id       = sha256( "primer.page.v1\n"
                        book_id "\n" edition "\n" page_no "\n"
                        chain_tip "\n"          # tip at THIS edition's freeze
                        content_sha "\n"
                        parent_page_id "\n"     # same page_no in edition n-1, else ZERO
                        visit_root "\n" )       # root of visits to parent during edition n-1, else ZERO
visit_sha     = sha256( canonical JSON of visit row, sort_keys, separators (",",":"), ensure_ascii )
visit_root_j  = sha256( "primer.visit.v1\n" visit_root_{j-1} "\n" visit_sha_j "\n" ),  visit_root_0 = ZERO
```

**Notes on the identities**

- `manifest_sha` is the sha256 of the canonical JSON of the manifest, computed with the `book_id` field excluded.
- **Visit row fields.** `{"book_id","page_id","seq","chain_tip_at_visit","response_sha256","holder_commit"}`. `seq` is an integer counter. Raw responses are stored locally only.

**Printed form.** Each footer shows the first 12 hex characters of the page id, and the QR carries the full `page_id`.

### Reference implementation (the landable patch, PROPOSED path `tools/primer_page_id.py`)

```python
import hashlib, json, unicodedata
ZERO = "0" * 64

def H(b): return hashlib.sha256(b).hexdigest()

def canon_text(s):
    s = unicodedata.normalize("NFC", s).replace("\r\n", "\n").replace("\r", "\n")
    lines = [l.rstrip(" \t") for l in s.split("\n")]
    return ("\n".join(lines).rstrip("\n") + "\n").encode("utf-8")

def _pre(tag, *fields):
    for f in fields:
        assert isinstance(f, str) and "\n" not in f and f.isascii(), f
    return ("\n".join((tag,) + fields) + "\n").encode("ascii")

def canon_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")

def book_id(genesis_tip, manifest_sha, holder_commit):
    return H(_pre("primer.book.v1", genesis_tip, manifest_sha, holder_commit))

def page_id(bid, edition, page_no, chain_tip, content_sha, parent=ZERO, vroot=ZERO):
    return H(_pre("primer.page.v1", bid, str(int(edition)), str(int(page_no)),
                  chain_tip, content_sha, parent, vroot))

def visit_root(prev_root, visit_row):
    return H(_pre("primer.visit.v1", prev_root, H(canon_json(visit_row))))
```

### Recomputability

Anyone holding (edition page files, manifest, visit commitment rows, the tip values named in the manifest) recomputes every id. The holder decides who "anyone" is, because the chain itself is private DNA (docs/DNA.md :: "Law | Private residual never remote").

### Examples

<example type="positive">
Edition 2, page 3: `parent_page_id` is edition 1 page 3's id, and `chain_tip` is the tip at edition 2 freeze. Changing one comma on the page changes `content_sha`, which changes `page_id`, which changes the printed footer. Tampering is visible on paper.
</example>

<example type="negative">
Ordering visits by wall-clock ISO strings. The COLD arm reports exactly this disease: `since()` "compares ISO timestamps as raw strings", `mag/chain_query.py:142-165`, UNVERIFIED (reported by COLD_HOT_RESULT :: COLD #1). Use `seq` integers, never timestamps, in preimages.
</example>

<example type="negative">
Looking up a page by substring of its id or of a JSON dump. The same report says `exists()` matches "any value ... not just ids" (`mag/chain_query.py:142-165`, UNVERIFIED). Use exact 64-hex equality only.
</example>

<example type="negative">
Putting the child's name, or a session token, in the QR or in any preimage. Only `holder_commit` is used.
</example>

### Falsifier of this deliverable

Part 4 is wrong if either of these happens:

- Two independent implementations written from this text alone produce any differing `page_id` for the Rung 1 edition.
- Any `page_id` can be reproduced with a `chain_tip` other than the one in the manifest. That would mean the tip is not actually bound.

---

## 5. THE HONEST COSTS

All ownership claims below are UNVERIFIED. The evidence lists no estate hardware inventory.

| Need | Why | Cheapest real experiment that justifies buying |
|---|---|---|
| Printer (color not required) | Rungs 4-5 require paper | Print the Rung 1 PDF at a copy shop for about the price of 12 pages. If a QR scans from it 3/3 times, a home printer is justified only if editions exceed about 2 per month. |
| Phone with camera, on the same LAN/tailnet as the board | The scan path | Borrow any household phone for the Rung 4 timing test. Buy nothing unless it fails for device reasons. |
| NFC stickers (optional upgrade over QR) | Tap is more magical than aim for small children | 10 tags, a few dollars. Run an A/B with Rung 4's timing protocol. Buy in bulk only if tap beats QR by more than 50% on time-to-response. |
| E-ink or dedicated reader device | An offline Primer with no phone | Defer. First prove Rung 5's "did it remember you?" is yes on a phone. A device solves a problem not yet shown to exist. |
| Local inference box (GPU) for offline, private generation | Keeps child responses fully on-machine | Run Rung 3 on the smallest local model the estate already uses (gemma:2b is named in next.md :: A2), then repeat Rung 2's in-book fabrication test on it. Buy a GPU only if the local model holds 0/50 in-book fabrication and fails only on latency. |
| bob ingress for `mountain_visit.py` | Real patina, not visit counts | No purchase. This is an owed landing (closed_corpus_doctrine :: "OWED"). Rung 5 runs without it, and the gap is named. |

**Spend ceiling before any hardware purchase:** Rung 2 at $4 plus Rung 3 at $1, both pre-registered caps. No hardware is bought until Rung 3 banks.
