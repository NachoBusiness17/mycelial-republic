# VERIFIER BYTES LAWS - steal receipt (2026-09-26)

Gopher t6d, gala afterparty wave A2. Three laws with zero corpus/steal coverage, promoted per the standing-burn receipt contract: max 500 words, fixed sections, closed bibliography of only sources actually read. Every quote byte-verified with grep -F, count 1.

## LAW 1: ABSOLUTE-PATHS-FOR-VERIFIERS

CLAIM: A verifier that resolves finish-line claims relative to its own cwd manufactures failure out of nothing. THE50 relaunch run dwfrun-4c7ad095: the in-run verifier reported 0/44 on disk while a second absolute-path, byte-size-checked recount found 44/44 present. The builders were right; the verifier was the bug.

VERBATIM QUOTE (grep -F verified, path:line): "a verifier that resolves claims relative to its own cwd manufactures a 100% failure rate out of thin air. Verifier asks must carry absolute paths or recompute them from the repo root."
Source: watch/inbox/THE50_RELAUNCH_VERDICT_20260925.md:12

STEAL: Verifier asks carry absolute estate paths or recompute from the repo root. When two verification passes disagree, audit the checker's path resolution before mourning the work.

FALSIFIER: A cwd-relative verifier that returns a correct verdict, or an absolute-path recount that overturns a cwd-relative verdict which had the right answer.

## LAW 2: SOFT-404 WALL

CLAIM: HTTP 200 at a well-known path proves nothing; require content-type application/json plus a JSON parse before calling a response a card. Witnessed twice on 2026-09-25: Wayback CDX returned 200 carrying an HTML outage page instead of JSON, and copilot's agent-card.json returned 200 carrying SPA HTML the official resolver rejected.

VERBATIM QUOTE (grep -F verified, path:line): "HTTP 200 at the well-known path proves nothing; require `content-type: application/json` + JSON parse before calling it a card." (original wraps the line after "require")
Source: watch/inbox/gala_20260925/w3/lanes/a24-a2a-photon.json:19

Corroborating quote (grep -F verified, path:line): "returned HTTP 200 with the Internet Archive-wide \"Temporarily Offline\" outage HTML page (\"Internet Archive services are temporarily offline.\")"
Source: watch/inbox/PHOTON_ROT_20260925.md:24

STEAL: Gate every endpoint or card probe on content-type plus parse, never status code alone, and save the raw wall bytes so the next seat re-runs the check offline.

FALSIFIER: A 200 text/html well-known response the official resolver accepts as a card, or a resolver acceptance granted without application/json content-type.

## LAW 3: STANDING-BURN RECEIPT CONTRACT

CLAIM: Free standing burns self-steal through a frozen receipt shape: named file pattern, 500-word ceiling, fixed sections, closed bibliography. Gala lane a09 danced with exact bijection: 32 ledger rows equals 32 receipts, 0 missing, 0 orphan.

VERBATIM QUOTE (grep -F verified, path:line): "watch/inbox/BURN_<slug>_<YYYYMMDD>.md, max 500 words, fixed sections: Verdict / Evidence (quotes) / Steal or Vacuous / Falsifier if build proposed / Bibliography (closed, only sources actually read)"
Source: memory/burns/MANIFEST.json:9

STEAL: This receipt runs the contract on itself. Future steal promotions and burn fires copy the shape (fixed sections, word cap, closed bibliography, grep -F quotes) instead of inventing per-seat formats.

FALSIFIER: A filed BURN_* receipt over 500 words, with free-form sections, or citing an unread source, that the burn ledger still counts valid.

## BIBLIOGRAPHY (closed; only sources actually read)

1. watch/inbox/THE50_RELAUNCH_VERDICT_20260925.md
2. watch/inbox/PHOTON_ROT_20260925.md
3. watch/inbox/gala_20260925/w3/lanes/a24-a2a-photon.json
4. memory/burns/MANIFEST.json
