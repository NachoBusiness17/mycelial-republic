# estate-filer: append tonight's GALA music-ractor LINKS rows to memory/corpus/LINKS.jsonl
# law: sequential single-writer append only; dedupe by src against existing rows first;
#      whole-ledger re-parse after append; ASCII only, no em/en dashes (ensure_ascii=True).
import json
import sys
from pathlib import Path

ROOT = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent")
LINKS = ROOT / "memory/corpus/LINKS.jsonl"
TS = "2026-10-01T11:33:00Z"

ROWS = [
    {
        "ts": TS,
        "id": "GALA-music-ractor-audio-dna",
        "kind": "gala",
        "slug": "music-ractor",
        "src": "watch/inbox/gala_20260925/music-ractor/lanes/audio-dna.json",
        "author": "gala lane audio-dna (music-ractor, division B)",
        "title": "Closes the folder-style question for music-ai: downstream generation/conditioning can now target the measured spec (full-scale master, RMS ~-12 dBFS, low-end-heavy 0.62, ~125 BPM folded club tempo) instead of assumed values",
        "load_bearing": [
            "110 files ffprobed, 0 errors; 30 tracks sampled stratified round-robin across 30 artists, all decoded clean to 8000Hz mono",
            "folder median spec: RMS -12.2 dBFS, crest 12.0 dB, ZCR 1416.4/s, low-end ratio 0.618",
            "decoded peaks proven pinned at full scale 1.000000",
            "raw bpm median 64.95 with folded view 125.0 BPM club tempo, octave-alias verified",
        ],
        "decision_changed": "Closes the folder-style question for music-ai: any downstream generation/conditioning now targets the measured spec (full-scale master, RMS ~-12 dBFS, low-end-heavy 0.62, ~125 BPM folded tempo) instead of assumed values; replaces guesswork, nothing superseded.",
        "lane": "gala-20260925/music-ractor/B",
        "note": "checks: audio_dna_scan.py exit 0 + peak-pinning/folded-BPM verify exit 0 (lanes/audio-dna.check.txt); receipt watch/inbox/music/audio-dna.md; deterministic, $0, all local, no listening",
    },
    {
        "ts": TS,
        "id": "GALA-music-ractor-style-synthesis",
        "kind": "gala",
        "slug": "music-ractor",
        "src": "watch/inbox/gala_20260925/music-ractor/lanes/style-synthesis.json",
        "author": "gala lane style-synthesis (music-ractor, division B)",
        "title": "cutters' style target: dashboard/static/suno cutters now cut from watch/inbox/music/STYLE_SPEC.md, one facet per generation (filter-disco 124, electro-punch 127, vocoder-pop 122 BPM) inside the measured 115-130 band, mastered warm/dark (centroid 900-1200 Hz, sub-160 share 0.4-0.5, RMS near -12 dBFS), with recipe re-verification as the cut gate",
        "load_bearing": [
            "110/110 profiled, 0 failures: RMS median -12.35 dBFS, peak 0 dBFS on 97/110, ZCR median 1272/s, sub-160 share median 0.47, centroid median 1070 Hz, folded BPM median 124.0 (strong-confidence 125.0), folded p25/p75 115.5/129.75",
            "three independent measured sources agree on the 124-125 folded tempo (this census, sibling 30-track sample, prior 52-track run within +/-2 BPM or an octave relation on 46 of 52)",
            "3 Suno style facets 675/635/601 chars, all under 900, zero artist names, zero em-dashes, numerics re-derived from the profile JSON",
            "finish-line check 25/25 PASS, exit 0",
        ],
        "decision_changed": "cutters' style target: dashboard/static/suno cutters now have a standing spec (watch/inbox/music/STYLE_SPEC.md); cuts should be generated one-facet-at-a-time at the facet BPM (A 124, B 127, C 122) inside the 115-130 band, mastered warm/dark (centroid 900-1200 Hz, sub-160 share 0.4-0.5, RMS near -12 dBFS), and a cut that passes tempo but reads bright/thin is off-canon",
        "lane": "gala-20260925/music-ractor/B",
        "note": "deliverable watch/inbox/music/STYLE_SPEC.md; checks: profile.py exit 0, check.py 25/25 PASS exit 0 (lanes/style-synthesis.check.txt), git status snapshot lanes/style-synthesis.gitstatus.txt; honest gaps: raw BPM octave-ambiguous on 30/110 rows (fold law stated, not hidden), no Suno generation run in-lane; ratchet not required, no mag/ or tools/ files touched",
    },
    {
        "ts": TS,
        "id": "GALA-music-ractor-taxonomy",
        "kind": "gala",
        "slug": "music-ractor",
        "src": "watch/inbox/gala_20260925/music-ractor/lanes/taxonomy.json",
        "author": "gala lane taxonomy (music-ractor, division B)",
        "title": "remixer-lives-in-comma-and-title-never-TPE4",
        "load_bearing": [
            "remixer-lives-in-comma-and-title-never-TPE4: remix credits encode only in the TIT2 suffix and the TPE1 comma pair; TPE4 empty 0/110 (0.0%)",
            "edges-first-nodes-second: batch 2026-08-05 bought the remix network (10/54, 18.5% remix-class share), batch 2026-10-01 backfilled original depth around a fixed 13-artist core",
            "80-20-hub-graph: ORIGINAL 87 (79.1%) vs 16 cross-artist remix-class (14.5%); Justice and Soulwax hold hub positions on both sides of the edge",
            "truncated-kind-word-edge-loss: the tagger truncates kind words in-frame (TIT2 'NY Excuse - Justice Remi'); parsers need the trailing-Remi normalization or they drop the Justice to Soulwax edge silently",
        ],
        "decision_changed": "Closes the curation-direction question for the music-ai folder: batch 2026-08-05 bought the remix network and batch 2026-10-01 backfilled original catalog depth around a fixed 13-artist core, so any later style model for this corpus should train on remix edges and hub degrees, not flat per-artist track lists.",
        "lane": "gala-20260925/music-ractor/B",
        "note": "110/110 MP3s mined with mutagen 1.48.1, 0 unreadable, 51 artists, 17-edge remix graph from 13 remixers covering all 8 the ask named; check taxonomy_scan.py exit 0, check md5 edc85e0d2d82715bd5948d3d721c7111, grep 'Unknown Album' = 5; receipt watch/inbox/music/taxonomy.md; 3 classifier defects caught and fixed in-lane; ratchet not run, no mag/ or tools/ code touched",
    },
    {
        "ts": TS,
        "id": "GALA-music-ractor-cutter-disco",
        "kind": "gala",
        "slug": "music-ractor",
        "src": "watch/inbox/gala_20260925/music-ractor/lanes/cutter-disco.json",
        "author": "gala lane cutter-disco (music-ractor, division B)",
        "title": "trust-bytes-liturgy (CUT 1: TRUST BYTES)",
        "load_bearing": [
            "trust-bytes-liturgy (CUT 1: TRUST BYTES): the evidence law in chorus form at 107 BPM with the folder's bass-forward end; lyrics are new words over mined register, every echoed doctrine line cited in the pack's ECHOES block",
            "green-is-a-moment (CUT 2): the perishability doctrine at the folder's median beat read (62.5/63.2 half-time, presented 126 BPM half-time feel); the hook doubles as the census law in one line",
            "no-sacred-cows-mic-drop (CUT 3): the window's two sacred-cow rulings, the gate self-exam finding, and the honest non-answer at 112 BPM with the spoken outro as the mic drop",
        ],
        "decision_changed": "Closes the filter-disco facet's cut-pack debt: Suno generation is unblocked with 3 paste-ready byte-checked packs, and creative lanes are shown to bind to the same finish-line discipline as repair lanes (byte-verified DNA numbers against audio-dna.md, no fabricated quotes, ECHOES citations, ASCII and no-dash law).",
        "lane": "gala-20260925/music-ractor/B",
        "note": "3 paste-ready byte-checked Suno packs (TRUST BYTES / GREEN IS A MOMENT / THE SMIRK KEY); finish battery 36 checks 0 FAIL exit 0 (lanes/cutter-disco.check.txt) after two byte-exactness fixes caught by run 1 (286.93 -> 286.9275) and two honesty fixes before run 1 (Hot Chip -9.45 is not the folder's loudest RMS row: row 24 reads -7.48, row 14 -9.62); artifact watch/inbox/music/cutter-disco_cuts.md; ratchet NOT RUN and not owed, watch/inbox records only",
    },
    {
        "ts": TS,
        "id": "GALA-music-ractor-cutter-electro",
        "kind": "gala",
        "slug": "music-ractor",
        "src": "watch/inbox/gala_20260925/music-ractor/lanes/cutter-electro.json",
        "author": "gala lane cutter-electro (music-ractor, division B)",
        "title": "loudness-doctrine-descendant",
        "load_bearing": [
            "loudness-doctrine-descendant: the operator's Casino post is the founding receipt of the loudness doctrine and the electro-punch facet is its numeric descendant: the facet lives where crest collapses (7.48-9.62 dB) and the decoded peak pins at 0.0 dBFS",
        ],
        "decision_changed": "the electro-punch facet now has a named numeric target band for generation and verification (rms -7.48 to -11.32 dBFS first-90s, crest ceiling 7.5-9.6 dB at the wall, folded 122-128 bpm, peak pinned 0.0 dBFS): Suno outputs from these packs are falsifiable against the same ffprobe recipe instead of taste",
        "lane": "gala-20260925/music-ractor/B",
        "note": "3 CUT packs (ONE BUG MANY JACKETS / GREEN IS PERISHABLE / THE CASINO) triangulating 6 distinct byte-verified folder tracks, none repeated; check battery 28 checks 0 failed exit 0 (lanes/cutter-electro.check.txt); n=9 subset medians recomputed (lanes/electro_subset_calc.txt: rms -11.32, crest 11.32, zcr 1693.1/s, low 0.5941, folded 127.0); style-string char counts corrected from guessed 451/455/434 to measured 369/382/370 before the battery ran; finish watch/inbox/music/cutter-electro_cuts.md; ratchet not run and not owed",
    },
    {
        "ts": TS,
        "id": "GALA-music-ractor-remix-mechanics",
        "kind": "gala",
        "slug": "music-ractor",
        "src": "watch/inbox/gala_20260925/music-ractor/lanes/remix-mechanics.json",
        "author": "gala lane remix-mechanics (music-ractor, division B)",
        "title": "form-operator law",
        "load_bearing": [
            "form-operator law: cross-artist remixes rewrite song form (duration delta median +15.6%, range -50.2% to +121.5%) while self-versions stay within 2.5%; duration delta is the cheapest remix-versus-remaster discriminator",
            "brightness ratchet: high-band energy ratio rises in 8 of 8 transformation pairs (median +33.9%, min +17.2%) while both self-versions sit at 0.0% and -10.0%",
            "two schools of dynamics: wall-school remixes compress (Sebastian -12.09 dB, Justice -3.53 dB) and shape-school remixes restore (Soulwax +13.68 dB, Classixx +8.2 dB); 14.14 dB apart on the same source",
            "electro-ification operator: MSTRKRFT D.A.N.C.E. band swap low +73.8%, mid -57.0%, high +49.6% (removes the mid, pays in sub and sizzle)",
            "distortion swap law: Justice NY Excuse leaves structure untouched (dur +2.6%, folded bpm 1.004) and re-voices it (zcr +54.0%, high +70.1%, low -38.1%, dyn -3.53 dB)",
            "the chop operator: Sebastian halves form (-50.2%), nearly doubles onset density (+49.9%), adds +3.02 dB and crushes 12.09 dB of dynamics",
            "tempo anchor law: folded bpm ratio 0.847-1.326 across all 10 pairs (cross-artist median 1.07); the one invariant remixers do not spend",
            "the floor law: self-versions move only length and loudness; the dup_suspect triple fired on zero rows; below this floor a remix claim is a reissue or a re-rip",
            "energy-delta mastering confound: RMS deltas below roughly 4 dB are not attributable to arrangement; the Animal pair's +12.8 dB is proven rip confound (original peak -11.17 dBFS)",
            "replicate-the-transform law: the only invariant across all 10 pairs is folded tempo near unity; a faithful replica of transformed art is typed by its delta operator, not by similarity to the source",
        ],
        "decision_changed": "no",
        "lane": "gala-20260925/music-ractor/B",
        "note": "10 pairs done of 10 planned, 28 files decoded full length, 0 measurement errors, 0 dup_suspect rows; check remix_scan.py exit 0, 5-check verify exit 0 (first attempt exit 1 on a lane-own filter bug, fixed, both facts in the receipt), all 10 row quotes byte-checked against cited sources (lanes/remix-mechanics.quotes.txt); receipt watch/inbox/music/remix-mechanics.md + raw watch/inbox/music/remix_mechanics.json",
    },
]

def main() -> int:
    raw_lines = LINKS.read_text(encoding="utf-8").splitlines()
    parsed = []
    for i, line in enumerate(raw_lines, 1):
        if not line.strip():
            continue
        parsed.append(json.loads(line))  # whole-ledger re-parse BEFORE append
    before = len(parsed)
    existing_srcs = {r.get("src") for r in parsed}
    dupes = [r["src"] for r in ROWS if r["src"] in existing_srcs]
    if dupes:
        print(f"DEDUPE BLOCK: {dupes} already present, nothing appended")
        return 1
    # belt-and-suspenders: any prior reference to the slug anywhere in the ledger
    slug_hits = [i for i, r in enumerate(parsed, 1)
                 if "music-ractor" in json.dumps(r, ensure_ascii=False)]
    with LINKS.open("a", encoding="utf-8", newline="\n") as f:
        for row in ROWS:
            blob = json.dumps(row, ensure_ascii=True)
            assert "\u2014" not in blob and "\u2013" not in blob, f"dash law violation in {row['id']}"
            f.write(blob + "\n")
    # whole-ledger re-parse AFTER append
    after_lines = LINKS.read_text(encoding="utf-8").splitlines()
    after = [json.loads(l) for l in after_lines if l.strip()]
    print(f"ledger {before} -> {len(after)} rows, appended {len(ROWS)}, "
          f"prior slug references: {len(slug_hits)}, re-parse OK")
    return 0

if __name__ == "__main__":
    sys.exit(main())
