CONTEXT — gate v3, the spectral classifier (classifier-first)

The salon verdict (hyperspectral_salon_20260903c, folded today):
- Middle column, not the cube: band-SELECTED multispectral (8-10 bands), classifier-first.
- Inversion resolved: the article renders spectra to GENERATE data; the fleet needs the
  inverse — bands as INPUTS, gate v3 as the CLASSIFIER. The Room draws bands that feed it.
- Build order step 0 (the falsifier): BEFORE any band spend, measure whether fleet events
  already carry discriminative signatures on EXISTING metadata. If no divergence signal,
  gate v3's premise fails cheaply.

What "bands" could already exist in fleet metadata (candidates to audit):
- watch/overnight_churn.py gate v2 heads list ("I'll help", "I'm sorry", ...) — the
  original spectral library, 7 hand-picked wavelengths.
- ractor_board.jsonl rows: {organ, kind, title, detail, status, evidence, ts}.
- room.jsonl, bay_share.jsonl {from, wing, top}, intake register.jsonl
  {ts, status, kind, url, note}, salon_receipts/*.json {lane, chars, secs, gate}.
- 47 fleet invariants as the candidate band registry (the "spectral library").
- Provenance fields already on events: seat, lane, session id, shape, gate verdict, chars.

Rightsize questions:
- What is the minimal classifier v0 that is still honest? (hash/fingerprint distance?
  embedding cosine? n-gram overlap vs the invariant library? Simplest that discriminates.)
- Which 3-5 "bands" (metadata fields) carry the most discrimination per byte?
- What does the falsifier test look like as a ONE-SCRIPT run on existing jsonl today?
- What should explicitly NOT be built yet (rendering pipelines, per-band Room shaders)?
- Pass/fail: what measured number makes gate v3 worth wiring into churn + salon gates?
