# s2-22 composer: renders inbox-genre-census.md from _s2_22_raw.json (census of record:
# full snapshot moment 2026-09-28T20:23:59-04:00 plus merged mem/registry passes).
import json, os, datetime, collections

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "_s2_22_raw.json")
OUT = os.path.join(HERE, "inbox-genre-census.md")

with open(RAW, encoding="utf-8") as f:
    data = json.load(f)
rows = data["rows"]
s = data["summary"]
xtab = data["xtab"]
clash = data["xtab_clash_samples"]

CUTOFF = "2026-09-14"  # 14 days back from 2026-09-28
FINDING_KEEP_SIGS = ("CENSUS", "MAP", "AUDIT", "DECODE", "INVENTORY", "GAP")

def verdict(r):
    canonical = r["ext_refs"] > 0 or r["reg_ref"] > 0
    cls = r["class"]
    recent = bool(r["fdate"]) and r["fdate"] >= CUTOFF
    if cls == "law":
        return "KEEP" if canonical else "PROMOTE"
    if cls == "receipt":
        return "KEEP" if canonical else "ARCHIVE"
    if cls == "shitpost":
        return "KEEP" if canonical else "ARCHIVE"
    if cls == "brief":
        if canonical:
            return "KEEP"
        return "REVIEW" if recent else "ARCHIVE"
    if cls == "finding":
        if canonical:
            return "KEEP"
        if recent or any(k in r["stem"].upper() for k in FINDING_KEEP_SIGS):
            return "REVIEW"
        return "ARCHIVE"
    return "REVIEW"  # other

def dq(t):
    # normalize em/en dashes in QUOTED file titles so the banked census itself carries
    # none; verbatim heading bytes live in the source files and in _s2_22_raw.json
    return (t or "").replace("\u2014", "-").replace("\u2013", "-").replace("\u2012", "-")

for r in rows:
    r["refs"] = r["ext_refs"] + r.get("mem_refs", 0)
    r["verdict"] = verdict(r)
    r["h1"] = dq(r["h1"])

L = []
A = L.append

A("# inbox genre census - every markdown file in watch/inbox/ (s2-22)")
A("")
A("Item: s2-22 (flash50, burn_reset_20260927) - banked 2026-09-28 by seat f2-s2-22.")
A("Twin files (byte-identical): `watch/inbox/burn_reset_20260927/flash50/inbox-genre-census.md`")
A("and `watch/inbox/burn_reset_20260927/flash50/s2-22.md`.")
A("")
A("## Census of record and drift")
A("")
A("The inbox is a live shared surface; sibling lanes landed files while this census ran.")
A("Every number below is from the snapshot of record unless a moment is named:")
A("")
A("- opening walk (first command of the ask, ~19:35 EDT): 2,270 md / 12,322 total files / 190 dirs / 6,385,219,826 bytes")
A("- draft instrument 19:43:12: 2,277 md; rerun 19:47:44: 2,279 md")
A("- **snapshot of record 2026-09-28T20:23:59-04:00: 2,385 md / 24,228,864 md bytes / 2,198 git-tracked**")
A("- drift over the run: +115 md in ~49 min (about 2.3 md/min), mostly burn_reset_20260927 sibling seats")
A("")
A("The ask said \"watch/inbox/ (6000+ files)\". Verified split: the 6000+ holds for ALL")
A("inbox files (12,322 at the opening walk); markdown specifically is 2,385 at the snapshot.")
A("")
A("## Instruments")
A("")
A("- `flash50/_s2_22_census.py`: walk + git facts (ls-files tracked set, log --diff-filter=A birth dates) + classification (its first reference pass, `git grep -oI -F -f stems`, was superseded - see Method 5b)")
A("- `flash50/_s2_22_memrefs.py` (v2, the reference instrument of record): both reference passes in LINE MODE with exact python substring attribution - canonical `git grep -n -I -F -f stems` over the T1 roots (9,731 matching lines) and ripgrep line-mode over memory/+watch/ - plus the INDEX.json registry cross-tab")
A("- raw per-file rows: `flash50/_s2_22_raw.json` (2,385 rows: rel, size, mtime, fdate, git_add, tracked, class, ext_refs, ref_by, mem_refs, reg_ref)")
A("")

cls_order = ["receipt", "finding", "brief", "law", "shitpost", "other"]
A("## Genre classes (snapshot of record)")
A("")
A("Classification is rule-based (rules quoted in Method); the ask's five genres plus an")
A("explicit `other` residue. Number first, rule after.")
A("")
A("| class | files | share | bytes | defined as |")
A("|---|---|---|---|---|")
rulemap = {
    "receipt": "numbered burn id (B2-/FW-/W#-/Q-NN/THE50) or RECEIPT/BURN/CLOSE/verdict/checkpoint/salon markers or `## Verdict` or bank:/status: banked",
    "finding": "research deliverable signatures (CENSUS, ANALYSIS, DECODE, FOLD, THEORY, LENS, STEAL, PLAYBOOK, DIGEST, THREAD, UNPACK, SOURCE, STUDY, MAP, RESEARCH, SURVEY, NOTES, REVIEW, PROBE, DEEP-)",
    "brief": "BRIEF/HANDOFF/ONBOARD/PROMPT/DISPATCH/ASK_/NEXT-WINDOW/ORDER_/MEMO in stem, or banked queue ask under burn_reset queue/",
    "law": "word-boundary LAW/LAWS/RIB/CLIPPY/CONSTITUTION/MAXIM in stem, or `# law`-style heading, or law-candidate",
    "shitpost": "explicit markers: SHITPOST/WHIM stem, shitpost/roast/dream/vision-verbatim in first heading, or the operator journal group",
    "other": "none of the above after a stage-2 heading pass",
}
for c in cls_order:
    n = s["class_counts"][c]
    A("| %s | %d | %.1f%% | %s | %s |" % (c, n, 100.0 * n / s["md_total"],
                                          format(s["class_bytes"][c], ","), rulemap[c]))
A("")

A("## When written (three clocks)")
A("")
A("| clock | coverage | min | max | note |")
A("|---|---|---|---|---|")
A("| filename date | %d of %d (%.1f%%) | %s | %s | regex 2026MMDD / 2026-MM-DD in stem |"
  % (s["fdated"], s["md_total"], 100.0 * s["fdated"] / s["md_total"],
     s["fdate_min"], s["fdate_max"]))
A("| git first-add | %d tracked md (%.1f%%) | %s | %s | log --diff-filter=A per path |"
  % (s["git_dated"], 100.0 * s["git_dated"] / s["md_total"],
     s["git_add_min"], s["git_add_max"]))
A("| mtime | all | %s | %s | mutable; max is the live write edge |" % (s["mtime_min"], s["mtime_max"]))
A("")
A("By filename month (undated = no date in stem):")
A("")
A("| month | files |")
A("|---|---|")
undated = s["md_total"] - s["fdated"]
for m, n in s["by_month"].items():
    A("| %s | %d |" % (m, n))
A("| (undated) | %d |" % undated)
A("")
A("Two clocks disagree on the past: 29 files carry July/August filename dates but the")
A("inbox only entered git history on 2026-09-14 (git first-add min), and mtimes reach back")
A("only to 2026-08-31 06:31. For those the filename date is the only birth claim; it is")
A("self-declared, not byte-proven.")
A("")
A("Newest-dated oddity: two files stamped 2026-09-29 are pytest basetemp fixtures a sibling")
A("lane (s2-19) captured inside flash50 at `_s219_basetemp/test_commit_chain_and_load0/agent_state/versions/`")
A("(UTC stamps reading as tomorrow in local time). flash50 is hosting another lane's test temp tree.")
A("")

canon_union = sum(1 for r in rows if r["ext_refs"] > 0 or r["reg_ref"] > 0)
mem_only = sum(1 for r in rows if r.get("mem_refs", 0) > 0 and not (r["ext_refs"] > 0 or r["reg_ref"] > 0))
A("## Referenced by anything (three instruments, two tiers)")
A("")
A("| instrument | scope | files with >=1 ref | share |")
A("|---|---|---|---|")
A("| T1 canonical roots git grep | docs, queue, state, configs, mag, tools, scripts, githooks, tests, corpus/steal, roblox/docs, .agents, memory/{rib,briefs,improve,workflows,boot}, memory/attention.md, memory/live_from_grok.md, 5 top-level md (tracked files only) | %d | %.1f%% |"
  % (s["ext_ref_files"], 100.0 * s["ext_ref_files"] / s["md_total"]))
A("| T1 INDEX.json registry | stem named in the derived registry (read %s after this pass re-read it live: %s items from index_events.jsonl) | %d | %.1f%% |"
  % ("2026-09-28T20:31 EDT", format(s["registry_items"], ","), s["reg_ref_files"],
     100.0 * s["reg_ref_files"] / s["md_total"]))
A("| T2 memory+watch rg pass | ripgrep line-mode -n -F -f stems over memory/ + watch/ minus watch/inbox minus archival memory/corpus (gitignore-respecting, binaries skipped); %s match lines, python substring attribution | %d | %.1f%% |"
  % (format(s.get("mem_pass_lines", 0), ","),
     s["mem_ref_files"], 100.0 * s["mem_ref_files"] / s["md_total"]))
A("| T1 union (canonical bar) | canonical roots OR registry | %d | %.1f%% |"
  % (canon_union, 100.0 * canon_union / s["md_total"]))
A("| T2 log-mention only | mem_refs > 0 but NOT canonically referenced | %d | %.1f%% |"
  % (mem_only, 100.0 * mem_only / s["md_total"]))
A("| zero anywhere | none of the three | %d | %.1f%% |" % (s["zero_ref_any"],
                                                           100.0 * s["zero_ref_any"] / s["md_total"]))
A("")
zrows = [r for r in rows if not (r["ext_refs"] or r["reg_ref"] or r.get("mem_refs", 0))]
if zrows:
    A("The %d true orphans (zero on all three instruments), named:" % len(zrows))
    A("")
    for r in zrows:
        A("- %s (%s)" % (r["rel"], (r["h1"] or "(no heading)")[:90]))
    A("")
A("The promotion bar is T1: a session log in memory/ citing a receipt is a mention, not an")
A("anchoring in the permanent record. T2 is reported because the ask says \"referenced by")
A("anything\" - and on that literal bar only %d md files in the inbox are true orphans."
  % s["zero_ref_any"])
A("")
A("Top referencing files (canonical pass, by number of distinct inbox md stems they name):")
A("")
A("| referencing file | inbox md stems named |")
A("|---|---|")
for name, n in list(s["ref_by_top"].items())[:15]:
    A("| %s | %d |" % (name, n))
A("")

A("## Cross-tab against the registry's own taxonomy")
A("")
top_regs = sorted(s["registry_classes"].items(), key=lambda kv: -kv[1])[:6]
A("INDEX.json items carry a `class` field of their own (event-log intake taxonomy, %d distinct"
  % len(s["registry_classes"]))
A("values at read time; top: %s). For the %d of %d inbox md that match a registry item by"
  % (", ".join("%s %d" % (k, v) for k, v in top_regs), s["xtab_matched"], s["md_total"]))
A("basename, exact-label agreement is %d (%.1f%%) - the two taxonomies are different"
  % (s["xtab_agree"], 100.0 * s["xtab_agree"] / s["xtab_matched"]))
A("instruments, not errata: the registry labels intake events (BACKFILL = folded from the")
A("log), this census labels genre. Registry classes for my %d law files: %s."
  % (s["class_counts"]["law"],
     ", ".join("%s %d" % (k, v) for k, v in sorted(xtab.get("law", {}).items(), key=lambda kv: -kv[1]))))
A("The registry records the landing event; the census records what the file is.")
A("")

A("## Promotion verdicts")
A("")
A("Verdict rule (applied per file, stated before the counts): canonically referenced (T1:")
A("canonical roots or INDEX registry) -> KEEP. A T2-only log mention does not KEEP a file.")
A("Canonically unreferenced: law -> PROMOTE (a law outside the permanent record is the one")
A("class where promotion is the failure mode); brief -> REVIEW if filename-dated within")
A("14 days else ARCHIVE; finding -> REVIEW if within 14 days or a census/map/audit/decode/")
A("inventory/gap signature, else ARCHIVE; receipt -> ARCHIVE (the work is in commits; the")
A("receipt's value is already folded); shitpost -> ARCHIVE; other -> REVIEW (unjudged).")
A("")
vc = collections.Counter(r["verdict"] for r in rows)
A("| verdict | files | share |")
A("|---|---|---|")
for v in ("KEEP", "PROMOTE", "REVIEW", "ARCHIVE"):
    A("| %s | %d | %.1f%% |" % (v, vc[v], 100.0 * vc[v] / s["md_total"]))
A("")

promotes = [r for r in rows if r["verdict"] == "PROMOTE"]
A("### PROMOTE list (%d): canonically unreferenced laws" % len(promotes))
A("")
A("Every one, named (rel | dated | h1):")
A("")
for r in sorted(promotes, key=lambda r: r["rel"]):
    A("- %s | %s | %s" % (r["rel"], r["fdate"] or r["mtime"][:10], (r["h1"] or "(no heading)")[:110]))
A("")

reviews = [r for r in rows if r["verdict"] == "REVIEW" and r["class"] in ("finding", "brief")]
reviews.sort(key=lambda r: -r["size"])
A("### REVIEW shortlist (top 30 of %d unreferenced recent/census findings+briefs, by bytes)" % len(reviews))
A("")
for r in reviews[:30]:
    A("- %s | %d B | %s | %s" % (r["rel"], r["size"], r["fdate"] or r["mtime"][:10],
                                 (r["h1"] or "(no heading)")[:100]))
A("")

others = [r for r in rows if r["class"] == "other"]
A("### OTHER residue (all %d, named)" % len(others))
A("")
for r in sorted(others, key=lambda r: r["rel"]):
    A("- %s | %s" % (r["rel"], (r["h1"] or "(no heading)")[:100]))
A("")

shits = [r for r in rows if r["class"] == "shitpost"]
A("### SHITPOST/whim class (all %d, named)" % len(shits))
A("")
for r in sorted(shits, key=lambda r: r["rel"]):
    A("- %s | %s" % (r["rel"], (r["h1"] or "(no heading)")[:100]))
A("")

laws = [r for r in rows if r["class"] == "law"]
lref = sum(1 for r in laws if r["ext_refs"] > 0 or r["reg_ref"] > 0)
A("### Law class detail (all %d)" % len(laws))
A("")
A("%d of %d law files are canonically referenced (KEEP); the %d unreferenced ones are the"
  % (lref, len(laws), len(laws) - lref))
A("PROMOTE list above.")
A("")
A("| law file | dated | refs | verdict |")
A("|---|---|---|---|")
for r in sorted(laws, key=lambda r: r["rel"]):
    A("| %s | %s | e%d/m%d/r%d | %s |" % (r["rel"], r["fdate"] or r["mtime"][:10],
                                          r["ext_refs"], r.get("mem_refs", 0), r["reg_ref"],
                                          r["verdict"]))
A("")

A("## Verdict by class")
A("")
A("| class | KEEP | PROMOTE | REVIEW | ARCHIVE | of which log-mention-only |")
A("|---|---|---|---|---|---|")
for c in cls_order:
    cv = collections.Counter(r["verdict"] for r in rows if r["class"] == c)
    lo = sum(1 for r in rows if r["class"] == c and r.get("mem_refs", 0) > 0
             and not (r["ext_refs"] > 0 or r["reg_ref"] > 0))
    A("| %s | %d | %d | %d | %d | %d |" % (c, cv["KEEP"], cv["PROMOTE"], cv["REVIEW"],
                                           cv["ARCHIVE"], lo))
A("")

A("## Method and limits")
A("")
A("1. Classification is heuristic on stem + first 4 KB (heading line first). The exact rule")
A("   chain, in order: numbered burn id (B2-/FW-/W#-/Q-NN/THE50 prefixes; verdict or receipt")
A("   text in first 600 B -> receipt, queue-grouped without verdict -> brief/ask, else")
A("   receipt) > word-boundary LAW/LAWS/RIB/CLIPPY/CONSTITUTION/MAXIM > brief signatures >")
A("   explicit shitpost markers on the first heading > finding signatures > receipt markers")
A("   > stage-2 heading pass > lane fallback (mickey/, burn_reset work/flash50, burn_wave/,")
A("   wave_20260916/, physical_computing/ -> receipt) > other. Known noise, accepted and")
A("   counted in `other` (%d files): concept notes and templates with no signature words." % s["class_counts"]["other"])
A("2. Reference scan 1 (T1) is `git grep -n -I -F -f stems.txt` over TRACKED files in the")
A("   pathspecs listed above; untracked reference surfaces are not scanned (except")
A("   INDEX.json, read directly). Stem match is exact substring on the matched line: a stem")
A("   inside a longer token counts (longer and shorter stems on the same line are both")
A("   credited).")
A("3. Generic-named files (readme/license/changelog/index/todo/notes stems, case-insensitive)")
A("   are resolved by full `watch/inbox/<rel>` needle instead of bare stem, to avoid false")
A("   positives from the word itself.")
A("4. Registry cross-tab matches by basename; 0 duplicate-basename conflicts were found")
A("   across the %d registry items." % s["registry_items"])
A("5. The memory+watch rg pass is gitignore-respecting and substring-based; a T2-only file is")
A("   mentioned in logs but anchored nowhere canonical. Zero-ref means zero in ALL THREE")
A("   instruments, a lower bound on true orphanhood, not an equality.")
A("5b. Instrument defect found and fixed during this census: ripgrep 15.2.0 `-o` with a")
A("   2,379-pattern `-f` file silently drops matches (a stem found by single-pattern -e and")
A("   by line-mode was never emitted by the multi-pattern -o run; first surfaced as 3")
A("   spot-check zero-ref files that repo-wide grep DID find in catalog/ and memory/).")
A("   All reference numbers above come from the re-run line-mode passes with exact python")
A("   substring attribution (canonical git grep -n -F: 9,731 lines; rg line-mode: %s lines);"
  % format(s.get("mem_pass_lines", 0), ","))
A("   the earlier -o numbers (416/2,211/93) are superseded and were never banked.")
A("6. INDEX.json was re-read live by the second instrument (%s items vs 1,415 at the first")
A("   pass 20:27 EDT): the registry itself is derived live from index_events.jsonl; reg_ref")
A("   flags in the raw rows are from the later read.")
A("7. File contents were read only to 4 KB per file (head + heading extraction). No whole-file")
A("   read pass was made; genre calls below the heading are unverified.")
A("8. The %d untracked md files have no git birth date; their clocks are filename date + mtime only."
  % (s["md_total"] - s["tracked_md"]))
A("9. Self-exclusion: the twin outputs (s2-22.md, inbox-genre-census.md) and the")
A("   instrument files (_s2_22_*.py/json/txt) are excluded from the md rows by name at the census moment.")
A("10. Quoted heading text in the named lists is dash-normalized (em/en to hyphen) so this")
A("   banked file carries zero em/en dashes; the verbatim heading bytes live in the source")
A("   files and in _s2_22_raw.json.")
A("")

A("## Per-file appendix (%d rows)" % s["md_total"])
A("")
A("Format: `rel | class | dated(filename/git) | refs ext+mem / reg | bytes | verdict`.")
A("")
for r in sorted(rows, key=lambda r: r["rel"]):
    dated = r["fdate"] or (r["git_add"] if r["git_add"] else "nodate")
    A("%s | %s | %s | %d+%d/%d | %d | %s" % (r["rel"], r["class"], dated, r["ext_refs"],
                                             r.get("mem_refs", 0), r["reg_ref"], r["size"],
                                             r["verdict"]))

text = "\n".join(L) + "\n"
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(text)
print("wrote", OUT, len(text), "chars")
