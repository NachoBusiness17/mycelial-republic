# RECEIPT — WAKERS INGEST (clean tier), 2026-09-06

Executed: `watch/INTAKE_WAKERS_CURRICULUM_20260906.md` (the policy) →
`corpus/library/wakers_20260906/` (50 files, 21,017,903 bytes ≈ 20.0 MiB).
Full per-file record with sha256: `corpus/library/wakers_20260906/MANIFEST.md`.

## What was pulled (count, bytes)

| # | item | files | bytes | license basis | jurisdiction |
|---|---|---|---|---|---|
| 1 | Ouspensky, Tertium Organum (Eng. trans. 1922) | 1 (EPUB, validated) | 905,617 | PD-US (pre-1928 translation); Global Grey redistributor | PD-US — training-eligible |
| 2 | Stapledon, Star Maker (1937) | 1 | 536,129 | PD-AU (PG-AU edition) | PD-CA/AU; US in-copyright to 2033 — do not weights-train on US surface |
| 3 | Stapledon, Last and First Men (1930) | 1 | 704,410 | PD-AU (PG-AU edition) | PD-CA/AU; also PD-US since 2026-01-01 (95y) |
| 4 | Stuart Hall, Encoding and Decoding (1973 CCCS paper) | 1 (21-page PDF scan) | 17,899,570 | University of Birmingham's own ePapers repository (rights-holder release) | Open scholarly release — RAG/citation pending license-read |
| 5 | Nag Hammadi Library translations | 46 (HTML→text) | ~972,000 | Openly posted scholarly translations, gnosis.org (Gnostic Society Library) | RAG/citation pending license-read |
| | **TOTAL** | **50** | **21,017,903** | | |

## Source notes (what actually worked)

- **Tertium Organum:** sacred-texts.com (primary) blocked by Cloudflare JS challenge on
  non-browser fetch (strike 1); Global Grey EPUB pulled as the one allowed alternate.
  Valid EPUB, 94 zip entries. PG-US has no Tertium Organum (checked catalog — no records).
- **Stapledon:** PG-AU author page gave exact text URLs; both downloaded clean (200).
- **Hall:** epapers.bham.ac.uk/2962/ — the canonical university item. PDF verified as the
  genuine 1973 paper (page 1 text reads the CCCS/Council of Europe Colloquy title block;
  21 pages). NOT a scan from a copyrighted collection.
- **Nag Hammadi:** 46/46 posted translations pulled from gnosis.org and converted to text,
  source URL stamped inside every file header. Tripartite Tractate needed the exact
  `.htm` link from the codex index (first guess 404'd; recovered, not a failure).
- **Claremont CGL Online:** ATTEMPTED as ordered. Old cdm4 URL 301s; live successor at
  ccdl.claremont.edu/digital/collection/nha. It hosts codex IMAGES/Coptic transcriptions —
  a scan corpus, not clean text — so NOT pulled; clean text tier covered by gnosis.org. Logged.
- **Berkeley Foucault lectures (1980-83):** archive.org pull FAILED — the `ucberkeley_mm`
  collection returns ZERO items and no Berkeley-creator Foucault items exist anywhere on IA
  (searched three ways). Per the intake card's uncertainty rule → RECORD-ONLY: the official
  source is UC's own Michel Foucault Audio Archive, guides.lib.berkeley.edu/mfaa (streaming).
- **LibriVox:** Star Maker — no catalog entry at all. Last and First Men — catalog entry
  id 22767 EXISTS (Stapledon, 18 sections) but every section has an empty file URL: a project
  stub, no audio published. Nothing pulled, honestly logged.

## RECORD-ONLY (borrow doors, no download)

- Ellul, The Technological Society — IA controlled lending: archive.org/details/technologicalsoc00ellu
- Gurdjieff, In Search of the Miraculous — IA controlled lending: archive.org/details/insearchofmiracu0000pdou_k0a3
- Jung CW abstracts (Rothgeb, vols 1-18) — jungpage.org/learn/resources/jung-s-collected-works-abstracts
- Foucault Berkeley lectures — guides.lib.berkeley.edu/mfaa (official UC streaming)

## REJECTED (never touched)

- Monoskop in-copyright PDFs — piracy door, closed by train-clean law (LEGAL_MEMO_002).
- The IA community "full PDF" uploads of the 1964 Ellul translation
  (jacques-ellul-the-technological-society_2/_3, folkscanomy copy) — pirate uploads; named
  for the record, zero bytes fetched. The intake card's DISPUTED verdict on "Ellul FREE" is upheld.
- Post-1928 copyrighted translation mirrors (incl. CW volume PDFs on third-party sites).

## Falsifiers

1. Every downloaded file has sha256 + source URL + license basis — PASS (50/50 in MANIFEST.md).
2. Zero files pulled from the rejected category — PASS.
3. Every FAILED/RECORD-ONLY row has a reason — PASS.
4. Total disk usage — 21,017,903 bytes, 50 files.

## The honest line

PD texts (Tertium Organum, Last and First Men, Star Maker within PD-CA/AU) are
training-eligible — with Star Maker jurisdiction-tagged OFF the US weights-training surface
until 2033. The openly-released scholarly tier (Hall CCCS paper, 46 Nag Hammadi translations)
is RAG/citation-use only pending a license-read — no weights training yet. Ellul, Gurdjieff,
Jung CW, and the Berkeley Foucault audio stay borrow-only/record-only. The PAID tier
(McLuhan, Foucault texts, Baudrillard, Jung CW + Red Book) awaits the Operator's wallet
ruling at the art-and-necessity bar — Red Book and Jung CW remain the strongest candidates.

## SEAT VERIFICATION (independent re-run, 2026-09-06)

Seat re-counted the shelf: 50 files exactly, manifest rows present, and the
Tertium Organum sha256 recomputed from bytes — **matches the manifest**
(8c6b292e9035b89d…). Falsifier claims hold. One jurisdiction CORRECTION the
ingester made to the seat's intake card, adopted: **Last and First Men is
PD-US since 2026-01-01** (cleaner than the card assumed); Star Maker remains
US-in-copyright to 2033 and stays jurisdiction-tagged OFF the US weights
surface. Status update superseding the "honest line" above: the PAID tier
ruling was MADE by the Operator same-day ("we'll buy it when we save the world,
we need the data now") — the in-copyright titles landed as the **KNOWLEDGE DEBT
BOOK** at `corpus/library/wakers_20260906_knowledge_debt/` (7 PDFs verified,
Gutenberg Galaxy two-strike FAILED with U Toronto Press named as the buy-back),
manifest re-cut as MANIFEST_KNOWLEDGE_DEBT.md with every row tagged owed. The
two shelves are separated by design: clean tier training-eligible, debt tier
RAG/personal-use until paid. VERDICT: PASS.
