#!/usr/bin/env python3
"""Fold library sub-shelf census into the map + law rows.

Reads logs/mates/cartographer/library_subshelf_citations.json (recomputed
counts, never hand-typed) and attaches curated class/note/verdict fields
authored from the 2026-10-15 session reads.
Outputs:
  logs/mates/cartographer/library_subshelf_map.jsonl  (1 row per sub-shelf)
  logs/mates/cartographer/library_lawfold.jsonl       (thread -> decision -> filed-or-debt)
"""
import io, json, os, sys

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
CEN = os.path.join(ROOT, r"logs\mates\cartographer\library_subshelf_citations.json")
MAP = os.path.join(ROOT, r"logs\mates\cartographer\library_subshelf_map.jsonl")
LAW = os.path.join(ROOT, r"logs\mates\cartographer\library_lawfold.jsonl")

# class + verdict + note per sub-shelf; notes name what was verified this session
NOTES = {
 ".mimosa": ("MACHINERY", "HYGIENE_DEBT",
   "hook-state and hook-status session JSONs (867+503 bytes) parked inside the indexed corpus; machinery cache, not content; sibling droppings also inside wakers_20260906"),
 "_quarantine": ("QUARANTINE", "HEALTHY",
   "5 misprovenance texts isolated with the reason in the filename: MANGLED-CYRILLIC patents md+txt, WRONG Blavatsky Secret Doctrine, 2 asked_X_actually_Y swaps (Boulger/Henty, Bellamy); 0 cited; isolation worked"),
 "ai-engineering-from-scratch": ("COURSE_MIRROR", "REFERENCE_BLANK",
   "5,458 files, 2.77 percent cited; course mirror"),
 "anthropic-courses": ("COURSE_MIRROR", "REFERENCE_BLANK",
   "258 files, 6.20 percent; course mirror"),
 "claritas": ("ESTATE_CARGO", "PARTIAL",
   "41 files, 60,434 bytes, 17.07 percent; nested repo/ mirror; namesake of mag/claritas.py (name verified kin, contents not deep-read this cycle)"),
 "evennia": ("CODE_SNAPSHOT", "REFERENCE_BLANK",
   "MUD/MU* creation system (README head read); 1,713 files, 12.73 percent; game-estate kin"),
 "hf-agents-course": ("COURSE_MIRROR", "REFERENCE_BLANK",
   "476 files, 4.83 percent"),
 "human-atlas": ("CODE_SNAPSHOT", "REFERENCE_BLANK",
   "interactive 3D anatomy explorer, React/Three.js over BodyParts3D (README head read); 147 files, 2.04 percent"),
 "image-blaster": ("CODE_SNAPSHOT", "ESTATE_KIN",
   "170 files, 2.94 percent; kin of the vendored image-blaster engine behind the image-blast skill (name kin, not byte-linked this cycle)"),
 "ingersoll_lockwood": ("PD_TEXTS_UNMANIFESTED", "PROVENANCE_DEBT",
   "3 Gutenberg texts (Baron Trump x2, 1900 Last President) + README, operator-directed import 2026-09-20, README carries verified-structure notes; absent from MANIFEST.sha256"),
 "interference-search": ("RESEARCH_CARGO", "PARTIAL",
   "parallel-branch reasoning research repo: explicit states, environment-executed moves, merge-on-same-state, trained judge prunes (README head read); 104 files, 26.92 percent"),
 "jev_steal_library": ("ESTATE_CARGO", "LANDED",
   "Jev persona-eval harness mapping (Noul/Score/Choice primitives onto persona-conditioning scoring) + consolidated bibliography 108,926 bytes; 2 of 3 files cited"),
 "kev": ("CODE_SNAPSHOT", "PARTIAL",
   "Jev-style decision model prototype: Qwen2.5-0.5B + LoRA, prefill-only, pointer readout (AGENTS.md head read); 978 files, 10.33 percent; 57,058 of its 60,229 reference instances are one generated file (watch/inbox/burn_wave_20260926/B2_73_secret_scan_results.json), not reading traffic"),
 "lmcache-src": ("CODE_SNAPSHOT", "REFERENCE_BLANK",
   "LMCache KV-cache layer source; 2,586 files, 17.98 percent; estate-cache-relevant"),
 "mixar": ("CODE_SNAPSHOT", "REFERENCE_BLANK",
   "GPL-3.0 project, Adeveda Enterprises (README/SPDX header read); 3,703 files, 19.07 percent"),
 "mod-playerbots": ("CODE_SNAPSHOT", "REFERENCE_BLANK",
   "CMaNGOS playerbots (README head read); 5,077 files, 7.48 percent; game-estate kin"),
 "ms-agents-beginners": ("COURSE_MIRROR", "REFERENCE_BLANK",
   "AI Agents for Beginners course (README head read); 10,265 files, 0.57 percent"),
 "ms-genai-beginners": ("COURSE_MIRROR", "REFERENCE_BLANK",
   "Generative AI for Beginners, 21 lessons (README head read); 12,203 files, 0.31 percent, the single largest blank sub-shelf"),
 "openai-cookbook": ("COURSE_MIRROR", "REFERENCE_BLANK",
   "openai cookbook mirror (README head read); 15,452 files, 0.98 percent, the largest sub-shelf by file count"),
 "pd_african_caribbean": ("PD_TEXTS", "MANIFESTED_UNREAD",
   "3 files, in MANIFEST.sha256, 0.00 percent cited"),
 "pd_child_development": ("PD_TEXTS_UNMANIFESTED", "PROVENANCE_DEBT",
   "7 txt files, absent from MANIFEST.sha256; 185.71 percent proxy rate is basename collision inflation, reported not hidden"),
 "pd_computing_history": ("PD_TEXTS_UNMANIFESTED", "PROVENANCE_DEBT",
   "4 txt files, absent from MANIFEST.sha256; 125 percent proxy rate is collision inflation, reported not hidden"),
 "pd_counter_enlightenment": ("PD_TEXTS", "MANIFESTED_UNREAD",
   "7 files (Origin of Species, Meditations, Leviathan, City of God et al), in MANIFEST.sha256, 0.00 percent cited"),
 "pd_east_asian": ("PD_TEXTS", "MANIFESTED_UNREAD",
   "7 files (Art of War, Bushido, Marco Polo), in MANIFEST.sha256, 0.00 percent cited"),
 "pd_maths_history": ("PD_TEXTS", "MANIFESTED_UNREAD",
   "Cajori History of Mathematics + README (README out of manifest scope by its own header); 0.00 percent cited"),
 "pd_oldbooks": ("PD_TEXTS", "MANIFESTED_UNREAD",
   "6 files, in MANIFEST.sha256, 0.00 percent cited"),
 "pd_physical_compute": ("PD_TEXTS_UNMANIFESTED", "MINED",
   "82 txt + 72 pdf, DTIC differential-analyzer corpus; 100 percent REALLY cited: docs/report_v1/sources/receipts/pc_dtic-ada593830-differential-analyzer-1942.md and watch/ESTATE_INDEX/ESTATE_INDEX.jsonl name its files (distinctive basenames, collision implausible); absent from MANIFEST.sha256"),
 "pd_scifi": ("PD_TEXTS", "MANIFESTED_UNREAD",
   "28 files, in MANIFEST.sha256, 0.00 percent cited"),
 "pd_siege_castle_fiction": ("PD_TEXTS_UNMANIFESTED", "PROVENANCE_DEBT",
   "18 txt files, absent from MANIFEST.sha256; 100 percent proxy rate credit NOT verified to a naming surface this cycle, collision possible, reported not hidden"),
 "pd_south_asian": ("PD_TEXTS", "MANIFESTED_UNREAD",
   "5 files, in MANIFEST.sha256, 0.00 percent cited"),
 "ractor_starter": ("ESTATE_CARGO", "LANDED",
   "ractor persona seed dirs: aristophanes, bernays, debord, diogenes, euler, freud, goldbach, greer, heraclitus_parmenides, innis et al (top level listed); 113 files, 4.42 percent"),
 "second-brain-os": ("CODE_SNAPSHOT", "REFERENCE_BLANK",
   "AI second-brain knowledge base project (README head read); 304 files, 6.91 percent"),
 "wakers_20260906": ("ARCHIVE_MIXED", "PARTIAL",
   "Stapledon (Last and First Men, Star Maker), Ouspensky Tertium Organum 1922 epub, Hall encoding/decoding 1973 CCCS pdf, Nag Hammadi texts, own MANIFEST.md 36,154 bytes; 52 files, 5.77 percent; also holds .mimosa hook droppings whose session id matches the knowledge_debt pod's sess_ab77d0d1 json"),
 "wakers_20260906_knowledge_debt": ("RESTRICTED_DEBT", "LANDED_WITH_DRIFT",
   "KNOWLEDGE DEBT BOOK: 7 in-copyright scans registered as debt lines with buy-back list, RAG/personal-only rule, never-redistribute rule, byte-verified 243,413,163 bytes across 7 PDFs (matches census exactly); DOC-DRIFT: its MANIFEST_RESTRICTED header names corpus/library/wakers_20260906_restricted which does not exist on disk (shelf renamed to _knowledge_debt per its own header)"),
 "web_sources_20261001": ("ARCHIVE", "LANDED",
   "3 flattened web captures (budget.html, deepswe.html, jevals_readme.md), path-mangled filenames, all 3 cited"),
 "wotlk-db": ("DATASET", "REFERENCE_BLANK",
   "CMaNGOS WotLK content database (README head read); 258 files, 262,112,710 bytes, 0.39 percent; game-estate kin"),
 "zcode-zai-org": ("CODE_SNAPSHOT", "REFERENCE_BLANK",
   "nested repo/ mirror, 7,090 files, 4.94 percent"),
}

LAW_ROWS = [
 {"row_type": "LAW", "thread": "wakers_20260906_knowledge_debt",
  "decision": "acquire in-copyright curriculum as declared scan debt: RAG/personal only, never redistribute, never weights-training, buy-back list per row (operator ruling 2026-09-06)",
  "filed": "LANDED: MANIFEST_KNOWLEDGE_DEBT.md in the pod; byte-verified 243,413,163 bytes across 7 PDFs matches this cycle's census exactly",
  "debt": "MANIFEST_RESTRICTED header names corpus/library/wakers_20260906_restricted, a path that no longer exists (shelf renamed); Test-Path False 2026-10-15"},
 {"row_type": "LAW", "thread": "corpus/library/MANIFEST.sha256",
  "decision": "hash-register every landed public-domain text with source URL, tier, jurisdiction",
  "filed": "LANDED for 57 texts across 7 pd pods (counted from the file, 64-hex rows)",
  "debt": "4 later pd pods plus ingersoll_lockwood are unmanifested: 114 plain-text PD works + 72 PD PDFs outside the register (per-pod counts recomputed from disk this cycle); _quarantine's 5 are out by design"},
 {"row_type": "PRACTICE", "thread": "corpus/library/_quarantine",
  "decision": "quarantine misprovenance acquisitions instead of deleting or shelving them",
  "filed": "LANDED: 5 files, reason in each filename (MANGLED-CYRILLIC, WRONG, 2x asked/actually)",
  "debt": None},
 {"row_type": "LAW", "thread": "pd_physical_compute (differential analyzers)",
  "decision": "mine DTIC differential-analyzer history corpus for docs/report_v1",
  "filed": "LANDED: docs/report_v1/sources/receipts cite pod files; watch/ESTATE_INDEX/ESTATE_INDEX.jsonl carries them",
  "debt": "pod itself absent from MANIFEST.sha256 (114-text debt row above covers it)"},
 {"row_type": "FINDING", "thread": "the 7 manifested pd pods",
  "decision": "the founding library (58 texts: equiano, uncle tom, douglass, origin, meditations, leviathan, art of war, 28 scifi, et al)",
  "filed": "UNREAD: 0.00 percent citation proxy on all 7 pods, 0 of 58 files ever referenced by a live surface",
  "debt": None},
 {"row_type": "FINDING", "thread": "the course/code mirror mass",
  "decision": "mirror external course and code bodies into the estate",
  "filed": "REFERENCE_BLANK by design: 5 course giants alone are 50,468 files (ms-genai 12,203 + ms-agents 10,265 + openai-cookbook 15,452 + ai-eng 5,458 + zcode-zai-org 7,090); library never-cited total 63,867 of 66,716 files",
  "debt": "blank mass is dominated by mirrors, so library's 4.27 percent is a floor, not a shame metric; the actionable blanks are the manifested-unread 58 and the unmanifested 186"},
 {"row_type": "FINDING", "thread": "kev (Jev decision-model prototype)",
  "decision": "snapshot the kev Qwen2.5-0.5B decision-model repo into the corpus",
  "filed": "LANDED with 10.33 percent basename citation",
  "debt": "refhit caveat for future shelf audits: 57,058 of kev's 60,229 reference instances come from one generated secret-scan JSON; refhit columns can be dominated by machine artifacts"},
 {"row_type": "HYGIENE", "thread": ".mimosa machinery in the indexed world",
  "decision": "hook machinery parked session-state dirs inside corpus/library/.mimosa and corpus/library/wakers_20260906/.mimosa",
  "filed": None,
  "debt": "cache in the durable surface; the shared-surface contract makes corpus durable and cache disposable, so these belong in cache roots; 3 files, 2,720 bytes total, operator-scale trivial"},
]

def main():
    with open(CEN, "r", encoding="utf-8") as f:
        cen = json.load(f)
    subs = {r["subshelf"].replace("corpus/library/", ""): r for r in cen["library_subshelves"]}
    missing = [k for k in subs if k not in NOTES]
    extra = [k for k in NOTES if k not in subs]
    if missing or extra:
        print("MISMATCH missing:", missing, "extra:", extra)
        sys.exit(2)
    rows = []
    for name in sorted(subs):
        r = subs[name]
        cls, verdict, note = NOTES[name]
        rows.append({"subshelf": "corpus/library/" + name, "class": cls, "verdict": verdict,
                     "files": r["files"], "bytes": r["bytes"],
                     "distinct_cited_proxy": r["distinct_cited_proxy"],
                     "citation_rate_pct": r["citation_rate_pct"],
                     "reference_instances": r["reference_instances"],
                     "note": note})
    with open(MAP, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(LAW, "w", encoding="utf-8") as f:
        for r in LAW_ROWS:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    # recomputed headline counts
    lib_files = sum(r["files"] for r in rows)
    cited = sum(r["distinct_cited_proxy"] for r in rows)
    never = lib_files - cited
    giant5 = sum(subs[s]["files"] for s in ["ms-genai-beginners","ms-agents-beginners",
                "openai-cookbook","ai-engineering-from-scratch","zcode-zai-org"])
    manifested = sum(subs[s]["files"] for s in ["pd_african_caribbean","pd_counter_enlightenment",
                "pd_east_asian","pd_maths_history","pd_oldbooks","pd_scifi","pd_south_asian"])
    unmanifested_txt = 7+4+18+82+3
    print("map rows:", len(rows), "law rows:", len(LAW_ROWS))
    print("library sub-shelf files:", lib_files, "(plus MANIFEST.sha256 loose = shelf 66,716)")
    print("cited proxy:", cited, "never-cited:", never)
    print("course-giant-5 files:", giant5)
    print("manifested pod files:", manifested, "unmanifested txt:", unmanifested_txt, "+ 72 pdf")
    print("wrote", MAP)
    print("wrote", LAW)

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    main()
