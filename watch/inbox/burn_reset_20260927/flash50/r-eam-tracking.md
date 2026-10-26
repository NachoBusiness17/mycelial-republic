# ITEM r-eam-tracking: Public tracking of US military EAM broadcasts - what is verifiably public vs attributed folklore

- Item id: r-eam-tracking
- Banked: 2026-09-28 by gopher flash50 (research ask)
- Method: all findings below were fetched or run during this ask. Tools used: WebSearch (backend rate-limited 429 repeatedly; every search result used is marked as a snippet sighting), WebFetch, the web_reader MCP tool, and `curl` via the Bash tool (Wayback Machine + CDX API). Anything I could not open or verify is listed in the OWED section, not papered over.

## 1. The system itself: officially public

**Official USAF acknowledgment (verbatim, recovered this session).** The live `grandforks.af.mil` site blocked direct fetches (Akamai "Access Denied" page saved at `/tmp/gf_af.html`, 379 bytes). The Wayback snapshot `web/20251213044556` of `https://www.grandforks.af.mil/About-Us/Units/` (fetched this session via `curl -sL https://web.archive.org/web/2025/https://www.grandforks.af.mil/About-Us/Units/`) states, in the 319th Operations Group section:

> "The 319th RW is one of two locations operating the High Frequency Global Communications System (HFGCS) that transmits and monitors signals and Emergency Action Messages globally for senior leader communications up to the President of the United States, and all DoD agencies. HFGCS signals can penetrate oceans, pass through hurricane walls, and signals can extend to the surface of the moon making this system the primary means of communication for U.S. contingencies and can transmit in severely degraded and hostil[e]..."

This is the load-bearing public fact: the USAF itself publicly says the network exists, carries Emergency Action Messages, and serves senior-leader comms up to the President. A search-result snippet (grandforks.af.mil Units page, dated 2025-07-12 in the snippet) carried the same sentence, corroborating the snapshot.

**Wikipedia HFGCS article** (fetched 2026-09-28): USAF single-sideband shortwave transmitter network, remotely controlled from Andrews AFB and Grand Forks AFB; known as GHFS before 2002-10-01; primary voice frequencies 4724.0, 8992.0, 11175.0, 15016.0 kHz USB plus MARS 13927.0 and Canadian 11232.0; stations use "<name> Global" callsigns (Andrews, Offutt, Croughton, Andersen, Ascension, Diego Garcia, Elmendorf, Hickam, Lajes, Lincoln Receiver Site/"West Coast", Puerto Rico, Sigonella, Yokota; Thule, Keflavik, Loring, MacDill, Scott, McClellan, Bayonne closed); "The HFGCS also carries Emergency Action Messages (EAMs)"; "A higher priority code for orders is a Skyking Message, which is a time sensitive message for orders"; Force Direction Messages (FDMs) are "impossible to distinguish them from EAMs when read"; the article is categorized under U.S. nuclear command and control and cites a single reference ("The HF-GCS and Emergency Action Messages", numbers-stations.com, October 2014) plus Larry Van Horn (2009) further reading.

**Wikipedia Emergency Action Message article** (fetched 2026-09-28): EAM is "a preformatted message that directs nuclear-capable forces to execute specific Major Attack Options (MAOs) or Limited Attack Options (LAOs)"; issued from the National Military Command Center, or Site R, E-4B, or E-6 Mercury aircraft; EAMs "use cryptographic protocols (including such methods as digital signatures) to authenticate the messages"; Skyking messages ("Foxtrot Broadcasts") share the network and can interrupt an EAM. Honesty note: the article carries maintenance banners (needs more citations, flagged 2007-11; may be out-of-date, flagged 2012-07), so its specifics (SIOP to OPLAN 8044 to OPLAN 8010-12) are the weakest tier of the public record even though the core picture matches the USAF's own page.

## 2. The hobbyist catalog layer: verifiably public as documentation, but hobbyist-authored

**Priyom.org HFGCS page** (`https://priyom.org/military-stations/united-states/hfgcs`, fetched 2026-09-28): 13 ground stations remotely controlled from Andrews' Network Control Station; voice USB on 4724, 8992, 11175, 15016 kHz with "The main frequency is 11175 during the day, or 4724 during the night"; describes the EAM format as broadcast ("All stations, all stations, this is <callsign>...", first six characters then "Stand by" three times, "Message follows", message read, "I say again", repeat, "out", length "usually 30 characters"); Skyking format ("Skyking, skyking, do not answer", codeword, time "each spelled separately", two-letter authentication, "I say again" repetition) with codewords claimed to be "names of popular rock bands and movie titles"; test counts "multiple times daily"; the ALE network (3137 through 23337 kHz list, station addresses ADW/OFF etc., "NW1 = E-4 Nightwatch") and SIPRNet HF (3113 through 27870 kHz, MIL-STD-188-110A data mode).

**The reference Wikipedia itself cites**, "The HF-GCS" on numbers-stations.com, was recovered via Wayback (live site 404s at the Wikipedia-cited path; Wayback says "The Wayback Machine has not archived that URL" for `.../the-hf-gcs-and-emergency-action-messages/`; the article lives at `http://www.numbers-stations.com/hf-gcs`, snapshot `web/20150127070731`, fetched this session). It adds: EAMs "begin with a 6 letter header with a purpose that has not been publicly released" repeated 3 times; "A typical EAM message is 30 characters"; endings "Mainsail Out" or station-specific ("Offutt out"); Skyking "begins with the reader stating 'Skyking Skyking do not answer', and then a 3 letter trigraph... and ends with a 2 letter authentication string"; lists 16 HF-GCS sites.

Verifiability lesson from cross-comparison: the catalogs disagree at the edges (Wikipedia lists 4 primary voice frequencies; numbers-stations.com lists 7 including 6712 Croughton, 6739, 13200; Priyom's day/night split is an additional claim). The invariant core (8992 + 11175 USB, EAM + Skyking + test counts as the traffic types, worldwide USAF net run from Andrews) agrees across all three independent hobbyist sources and matches the official USAF sentence. Format details above are observer-derived folklore-adjacent facts: publicly documented, but with no official confirmation of any format claim, and the header's meaning is explicitly "not publicly released".

## 3. The logging community layer: verifiably public

- **eam.watch** (fetched 2026-09-28): a live community EAM/Skyking tracking site ("Copyright 2026 Eam.Watch", "Version 3.3.5") with navigation for Messages, Automated Recordings, Skyking Messages, Charts, a Discord invite (`discord.gg/YaK4vK8`) and Discord-tied login. Automated recordings plus community submissions; creator identity not stated anywhere I could read (OWED).
- **UDXF, Utility DXers Forum** (`https://groups.io/g/UDXF`, fetched 2026-09-28): 4,166 members, 64,000+ topics; description verbatim: "The Utility DXers Forum - UDXF is centered around the exchange of news and information relating to 'utility' radio stations and signals, below 30 MHz", explicitly excluding broadcast/pirate/amateur topics. The group page itself never says "EAM" - it is the general utility-logging institution behind decades of EAM log posts, an inference from its scope, not a quoted claim.
- **NEET INTEL Substack** (`https://neetintel.substack.com`, fetched 2026-09-28): an active named (pseudonymous) HFGCS-monitoring publication. Sitemap check via `curl` located the 2022 retrospective; archive lists 2026 posts including "30 Character EAMs Have a Format After All" (2026-09-08), "HFGCS Summary Report for June 2026" (2026-07-02), "HFGCS Callsigns: Observations, documentations, rules, tips, and tricks" (2026-08-08).
- **Legacy print hobbyist press** (search-result snippets from worldradiohistory.com archives, sightings only): Monitoring Times / Utility World columns logging EAMs by callsign on 8992/11175 going back years (e.g., 2007-03 "Chivalrus-US military, with a 28-character EAM"; 2008-05 "Gas Tube... three 28-character EAMs, simulcasting on 8992 and 11175").
- **Listening infrastructure**: University of Twente WebSDR named as the community's monitoring venue in the NEET INTEL retrospective; KiwiSDR/WebSDR networks are what make global listening trivial. (I did not open the Twente SDR itself this session; the retrospective citation is the receipt for its community role.)

## 4. The legal layer: verifiable statute, interpretive application

18 U.S.C. 2511(2)(g)(i), quoted verbatim from law.cornell.edu (fetched 2026-09-28): it is not unlawful "to intercept or access an electronic communication made through an electronic communication system that is configured so that such electronic communication is readily accessible to the general public." Caveat: whether plain-voice US military HF broadcasts count as "readily accessible to the general public" under this clause is an interpretation the hobby community relies on; I found no court ruling on point this session (OWED). That the question is live even inside the community is documented: the NEET INTEL retrospective reports community figures insisting "recording EAMs was illegal", a claim he disputes.

## 5. Attributed folklore: real signals, unverifiable readings

1. **EAM volume as a war thermometer.** Community channels (DEFCON Warning System community forum, Facebook HFGCS groups, 4chan /skg/ threads - all search-result sightings this session, not opened) treat EAM/Skyking counts as a readiness signal. The strongest on-the-record counter and caution is NEET INTEL's retrospective (fetched, dated 2026-01-22): "I noted hearing 30 Emergency Action Messages (EAMs) broadcasting on the HFGCS" within days of starting; "I personally suspected there was no correlation between the quantity of EAMs broadcast on the HFGCS and geopolitical events"; and even on the invasion-day traffic, "I could not make a conclusion with certainty." No public dataset validates any event-correlation claim; eam.watch Charts exist but no published validation of a volume-to-event mapping was found.
2. **Content readings.** Any claim to know what a specific EAM "said" is folklore. The message content is encrypted (Wikipedia EAM article: cryptographic authentication; NEET INTEL 2026-09-08 post, preview fetched: "These messages are encrypted and the report does not try to decrypt them" - the hobbyist state of the art is external statistical structure analysis, with a paywalled paper titled "30-Character HFGCS Broadcast Messages Are Not Uniform Ciphertext: Field Structure and a Dated Format Revision"). One concrete folklore sighting: a Facebook post surfaced in search results this session (URL not captured, Facebook requires login; snippet only) claiming a 246-character EAM carried "a code phrase relayed to the British prime minister" - an interpretive claim riding a real log with no verifiable basis.
3. **"EAMs are one-time-pad encrypted."** Documented as a community claim in the NEET retrospective (the "experts" on the Twente chatbox and eam.watch Discord "insisted EAMs use one-time pads"); the author disputes it; neither side is publicly verifiable (OWED both ways). The 2026 statistical-structure claim (non-uniform ciphertext) argues against ideal OTP, but it is a paywalled hobbyist analysis, not official.
4. **Skyking = launch order.** Contradicted by every public catalog: Skyking is a higher-priority time-sensitive format, "do not answer" is standard one-way procedure, and the format is documented carrying routine test and administrative traffic; no public document ties Skyking specifically to nuclear launch. The tropes survive because the codeword system (Priyom: "names of popular rock bands and movie titles") is legible but unexplained.
5. **DEFCON linkage.** DEFCON levels are not officially published; the "DEFCON Warning System" is a private fan project whose forum correlates EAM logs with speculative readiness levels. No verifiable mapping exists.
6. **"Doomsday radio" conflation.** The "Doomsday" branding belongs primarily to Russia's UVB-76 "Buzzer" lore (which did get mainstream pickup around 2022-02, per search sightings including Facebook/Economic Times headlines); US EAM monitoring gets the same aesthetic applied but I found no mainstream outlet verifying a US EAM surge claim. Coverage of the 2022 invasion period that I could verify on the US side stayed in community lanes (NEET INTEL, forums) plus adjacent non-EAM shortwave items (KB6NU 2022-03-29 post about a Maine couple listening to Ukraine-related HF - checked and excluded from EAM claims as out of scope).

## 6. What is verifiably public (summary)

- HFGCS exists, is USAF-operated, carries EAMs, serves Presidential/senior-leader comms (official USAF page, quoted verbatim above).
- Frequencies, station callsigns, message formats, schedules, ALE and SIPRNet channel lists: publicly cataloged by at least three independent hobbyist sources (Wikipedia, Priyom, numbers-stations.com archive), mutually consistent on the core, divergent on details, officially unconfirmed.
- Listening is trivially possible (WebSDR/KiwiSDR) and logging is institutionalized (UDXF, eam.watch, NEET INTEL, decades of print columns).
- The US legal basis for receiving is an excerptable statute whose application to this case is community interpretation, not settled law (no case found).

## 7. What is NOT verifiable (folklore or OWED)

- Any specific EAM's meaning or any "code phrase" claim (folklore).
- EAM-volume-to-event causal or correlational claims (unvalidated; contradicted in part by the most rigorous public monitor on record).
- OTP encryption claim (community dispute, unverifiable publicly).
- Skyking-as-launch and DEFCON mappings (no public support).
- eam.watch operator identity (OWED).
- The verbatim official DoD definition of EAM from the Nuclear Matters Handbook: primary sources unreachable this session (`acq.osd.mil` TLS failure from this egress; DOE media PDFs unsupported by the fetch tool; lasg.org glossary 404). Search snippets surfaced the handbook's glossary containing "emergency action message (EAM)" (LASG mirror of the 2011 edition) and DOE document text "emergency action messages; identify nuclear targets..." (energy.gov/media/364613 snippet), but I could not open either document directly, so the official definition is verified only at snippet distance (OWED).
- Mainstream (non-community) reporting that specifically verifies US EAM surge claims during 2022 or later crises: not found in multiple searches this session (searches repeatedly 429-rate-limited, so this is bounded by tooling, stated as OWED rather than a negative fact).

## 8. Sources and access log (all accessed 2026-09-28)

| # | Source | How accessed | Status |
|---|--------|--------------|--------|
| 1 | grandforks.af.mil/About-Us/Units/ (Wayback web/20251213044556) | curl -sL | Fetched; official HFGCS+EAM sentence quoted |
| 2 | grandforks.af.mil live | curl (browser UA) | Blocked: Akamai Access Denied |
| 3 | en.wikipedia.org/wiki/High_Frequency_Global_Communications_System | WebFetch | Fetched |
| 4 | en.wikipedia.org/wiki/Emergency_Action_Message | WebFetch | Fetched |
| 5 | priyom.org/military-stations/united-states/hfgcs | WebFetch | Fetched |
| 6 | priyom.org root + /military-stations | WebFetch | Fetched (HFGCS page located) |
| 7 | numbers-stations.com/hf-gcs (Wayback web/20150127070731) | curl + python text extraction | Fetched |
| 8 | numbers-stations.com/the-hf-gcs-and-emergency-action-messages/ | curl (live + Wayback availability + CDX) | 404 live; "not archived" at that exact path |
| 9 | eam.watch (root + /skyking-messages) | WebFetch | Fetched (nav shell; data behind JS) |
| 10 | groups.io/g/UDXF | WebFetch | Fetched |
| 11 | neetintel.substack.com/p/neet-intel-retrospective-2022 | WebFetch + curl sitemap | Fetched |
| 12 | neetintel.substack.com/p/30-character-eams-have-a-format-after | WebFetch | Fetched (paywalled preview) |
| 13 | law.cornell.edu/uscode/text/18/2511 | WebFetch | Fetched |
| 14 | swling.com blog EAM search | WebFetch | Fetched (two 2015 posts located) |
| 15 | kb6nu.com blog search | WebFetch | Fetched (2022-03-29 post; out of EAM scope) |
| 16 | fas.org site search | WebFetch | Ran; zero results for "emergency action message" |
| 17 | archive.org availability/CDX APIs, web.archive.org fetches | curl | Ran (one 429, then clean) |
| 18 | Facebook groups, DEFCON Warning System community forum, worldradiohistory.com, @Spy_Stations, energy.gov/media/364613, lasg.org, udxs.org, Rumble 2022 video | WebSearch snippets only | Sightings; not opened; treated as attributed claims |
