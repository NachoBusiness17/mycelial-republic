# MICKEY17 EDGE-MINING WAVE -- COLLECTION LEDGER (2026-10-18)
**Status:** In Progress (5 miners launched to width)  
**Protocol:** Standing Wave Protocol (2026-09-18)  
**Class:** receipt  

5 concurrent Mickey 17 edge-miners launched over 5 active estate and vessel surfaces (operator order: "do wave protocol in this window launch to width and just keep mickey 17'ing").

This ledger files findings as agents return. Improvements ranked at close.

---

## MINER MANIFEST
- **Miner 1:** `Mickey17-01` (`3bde0902-d519-4fc0-ae1e-40da90d92937`) -- Voice Vessel Persistence & Auth (Cold-start state loss, rate limiting, PIN brute force).
- **Miner 2:** `Mickey17-02` (`50a0386e-3af0-49cd-8e6e-8fb94034d40d`) -- Fleet Archive Wire & Relay (HTTP client bridge, 5TB archive search, SSRF/token security).
- **Miner 3:** `Mickey17-03` (`4ea0544d-1e26-4fdb-8a09-e8be42e35461`) -- Empir3 Bridge & Life-Ops Triage (Offline daemon resilience, invoice injection guard, spend cap).
- **Miner 4:** `Mickey17-04` (`ebb83577-af0f-4a63-a8ce-02124c4f4ae1`) -- Queue Refuel & ORG_SYSTEM_V2 Pours (Drained queue refuel, F1-F5 falsifiers, CURRENT.md refresh).
- **Miner 5:** `Mickey17-05` (`a1849f7b-02e2-4d52-acf2-4115134f9f4e`) -- The Room & Full-Width Surface (Broken trails, canvas scaling on ultrawide/mobile, interactive write-path).

---

## RETURNS PENDING
*(Ledger updates as each miner returns with byte-verified findings.)*

## RETURN 1/5 -- Estate Queue & ORG_SYSTEM_V2 Pours (Miner 4: ebb83577)

- **The Drained Autonomous Queue Seam:** All autonomous tasks in `queue/todo.md` marked complete (`[x]`); only 4 manual operator/studio tasks remain. Fleet is idling without active build orders.
- **The 4-Day Freeze Seam:** `state/CURRENT.md` frozen at `2026-10-14T05:30:00Z` talking about Foundations Week GSTD soak (which completed Oct 15). `_sync_current()` in `mag/seat.py` is bypassed by standalone scripts and subagents.
- **The Crown Disconnect Seam:** `state/SOAK_BEACON_20261016.md` claims Hermes has no funded credits, whereas `memory/rib/RIB_BOB_PRIMARY_20261017.md` confirms active OpenRouter paid key with 1000 free-model requests/day.
- **Concrete Seeding Spec:** 5 Pours defined (Pour 1: Claims seed F1, Pour 2: Claim drift patrol F1, Pour 3: Canon beacon F2, Pour 4: Mag mode F3, Pour 5: Contract widening F4, plus Organ 5 Consumer Law F5).

## RETURN 2/5 -- Voice Vessel Persistence & Auth (Miner 1: 3bde0902)

- **The Cold-Start Memory Eviction Seam:** Learned seat corrections and jargon only existed in heap memory (`SEATS_CACHE`), wiped on serverless spin-down and forcibly wiped every 60 seconds by cache invalidation in `seat_manager.js`. Consent state (`PENDING_INVARIANT`) was held in module global, dropping Renee's "Yes" on warm container rotation.
- **PIN Brute-Force & Token Exfiltration Seam:** `api/auth.js` had zero rate limiting or lockout. An attacker could brute-force the 10,000 PIN space in ~90 seconds. Crucially, a successful PIN hit returned `token: matchedSeat.passkey`, leaking the master access token to the browser.
- **LLM Rate-Limit & Hanging Request Seam:** No `AbortController` timeout on OpenRouter fetches; hanging requests hit Vercel 10s/15s lambda timeout. 429 rate-limits were silently swallowed without fallback alerting.
- **Audio TTS Prosody Glitch:** `sanitizeForVoice()` did not strip unicode `\u2014` or `\u2013`, causing mobile Safari and Chrome speech synthesis to awkwardly pronounce "em dash".
- **Concrete Fixes Landed:** `/tmp/seat_corrections_{seatId}.json` persistent disk cache with auto-merge, sliding-window IP lockout (5 fails / 15 min + 600ms penalty), `AbortController` 4.5s timeouts with explicit 429 handling, and audio-prosody dash stripping.

---

## RETURN 3/5 -- Fleet Archive Wire & Relay Seam (Miner 2: 50a0386e)

- **The Unbounded 5TB Filesystem Thrash:** `gateway.py` performed synchronous, single-threaded `os.walk` across 5TB on every query, blocking the Python runtime and exceeding `fleet_client.js`'s 3.5s timeout 100% of the time.
- **The Short Keyword Deletion Bug:** Naive tokenizer `len(term) > 3` discarded critical 2-3 letter words ("gas", "tax", "tub", "doc", "door", "pipe"), causing immediate empty string returns.
- **SSRF & Token Exposure Vectors:**
  1. Default `fetch` followed HTTP redirects, enabling credential forwarding.
  2. Trailing slash in `FLEET_GATEWAY_URL` caused `//api/v1/search` 404s.
  3. Hardcoded public fallback token (`sovereign_republic_secret_token_2026`).
  4. Timing attack on auth (`==` instead of `hmac.compare_digest`).
  5. Information disclosure in `/api/v1/health` leaking host paths.
  6. Inherited `do_HEAD` from `SimpleHTTPRequestHandler` exposed local files without auth.
- **Concrete Fixes Landed:** Threaded HTTP server (`ThreadingHTTPServer`), ChromaDB semantic search with bounded (< 400ms) lexical fallback, `redirect: 'error'` SSRF fence, `hmac.compare_digest` auth, and URL path normalization.

## RETURN 4/5 -- The Room & Full-Width Surface Integrity (Miner 5: a1849f7b)

- **The Trail Schema Mismatch Seam:** `room.html` checked `r.note` and `r.summary`, but all 11 trail files in `dashboard/static/trails/*.jsonl` use `{"ts", "actor", "event", "detail", "artifacts"}`. Consequence: 100% of trail entries dumped raw JSON strings.
- **The Missing Trail Seam:** `android_surface.jsonl` existed on disk with 13 records but was dropped from `TRAILS`.
- **The Vanishing Nav Seam:** `room.html` omitted `<script src="/static/nav.js"></script>`, causing the estate navigation bar to vanish on arrival.
- **Nav Label Collision:** `nav.js` had two items titled "The Room" (lines 33 and 103). Line 33 should be "Room Lightmap".
- **Smith Chart Ultrawide & Mobile Scaling Seams:**
  1. Ultrawide 21:9 locked aspect ratio caused canvas height to swell to 2360px, pushing the standing wave strip off-screen.
  2. Mobile portrait scaled text to 3.75px and marble to 5.2px; missing `touch-action: none` caused drags to trigger page scrolling.
  3. Contained 30 em-dashes (`\u2014`) across markup and canvas strings.
- **Concrete Fixes Landed:** Upgraded `room.html` with interactive dispatch dock, live 10s pulse, schema-aligned `fmt()`, `android_surface` restoration, and zero em-dashes. Patched `nav.js` to disambiguate "Room Lightmap".

---

## RETURN 5/5 -- Empir3 Bot & Life-Ops Contractor Triage (Miner 3: 4ea0544d)

- **The Synchronous Polling Hang Seam:** `bot.py` executed bridge commands synchronously inside `telegram_poll_loop()`. Unresponsive port 3006 calls blocked the main loop for 10s-15s, freezing polling across all chats.
- **The Keyword Collision & Injection Seam:** `renee_gateway.py` matched `"450"` inside the locksmith check, misclassifying a $450 plumbing invoice as a deadbolt repair. In addition, contractor invoice text had zero prompt injection defenses or delimiter isolation before reaching reasoning engines.
- **Spend Cap Enforcement Disconnect:** `empir3-agent-spec.json` declared no budget bounds while specifying Claude 3.5 Sonnet and ElevenLabs. If OpenRouter prepaid funds were exhausted, `dispatchLLM` cascaded into post-paid providers uncapped.
- **Telegram Entity Parse Crashes:** Invoices containing unescaped Markdown symbols (`_`, `*`, `[`, `` ` ``) crashed Telegram delivery with HTTP 400 Bad Request.
- **Concrete Fixes Landed:** ThreadPoolExecutor non-blocking worker pool, 2.5s fast timeout with circuit-breaker cooldown, `<invoice_content>` XML delimiter isolation against prompt injection, decoupled keyword matching, hard-stop 402 wallet shield in `chat.js`, and plain-text fallback for Telegram message formatting.

---

## CONCLUSION: ALL 5 MICKEY 17 EDGES RETURNED & HARDENED
1. **Estate Queue:** Refueled in `queue/todo.md` with P0 ORG_SYSTEM_V2 Pours 1-5 (F1-F5).
2. **Estate Truth:** Unfrozen `state/CURRENT.md` from Oct 14 freeze to live truth.
3. **Voice Vessel:** Sealed cold-start `/tmp` persistence, hardened PIN auth, and fixed audio prosody dashes.
4. **Fleet Relay:** Upgraded `gateway.py` to `ThreadingHTTPServer` with bounded search, constant-time HMAC, and SSRF redirect protection.
5. **The Room Surface:** Upgraded `room.html` with interactive dock, trail schema formatting, and nav restoration.
6. **Empir3 Life-Ops:** Hardened `bot.py`, `bridge_client.py`, and `renee_gateway.py` with non-blocking dispatch and injection shields.
