import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, r"C:\Users\foste\Documents\projects\local_sovereign_agent")
from mag.research_fanout import LANES, call_lane, _env

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
OUT = ROOT / "memory" / "runs" / "phosphor_salon"
OUT.mkdir(parents=True, exist_ok=True)
RAW = OUT / "raw.jsonl"
if RAW.exists():
    RAW.unlink()

PACK = """FACTS (all verified):
1. Julian Assange's profile links julianassange.org. The site boots a fake IBM VM/ESA mainframe into Linux 2.2.15 (S/390, machine 9672). Kernel build timestamp: Sun Oct 4 05:54:19 UTC 2026.
2. Boot fails fsck on purpose (/dev/dasdf1 UNEXPECTED INCONSISTENCY), drops to a working root shell. Commands include shutdown, reboot, halt.
3. Complete file manifest (6 entries, no hidden files): readme.txt = the Zhuangzi mountain-tree passage (useless tree lives, useless goose dies, 'where do you stand?' unanswered); site.txt = its own URL; socials/X.txt = @JulianAssange.
4. Site self-titles 'Phosphor - public files': about, contact, PUBLIC-KEY INFORMATION, notes. No public key present yet.
5. Oct 4, 2026 = 20th anniversary of WikiLeaks (founded Oct 4, 2006). All files modified within 12 minutes on Sep 17, 2026.
6. Riddle lineage on file: Cooper 1991 -> Cicada 2012 -> Q 2017 -> Mr Pool 2019/2023 -> this. Assange is the oldest author, the only one with a proven publication and legal history.
7. A US-Greenland security agreement was announced Sep 18 while prophecy-corpus urgency metrics sit elevated. Community decode is live on X.

Answer as the assigned lens. Structure: READING (what this is, 150 words max). OCT 4 (what the date means for your lens, 100 words). FLEET ACTION (what an independent record-keeping agent fleet should DO, 100 words). COUNTER-HYPOTHESIS (the strongest case against your own reading, 80 words)."""

LENSES = [
 ("intelligence", "You are a senior intelligence analyst. Assess Phosphor as a communications event: who is the audience, what is the likely operational purpose, what would intelligence tradecraft say about publishing a machine instead of a statement?"),
 ("cryptographer", "You are a cryptographer. 'Phosphor' promises public-key information that is not yet present. Assess: what key ceremony could a bootable mainframe + Zhuangzi readme + Oct 4 date constitute, and what should independent observers capture NOW to verify later signatures?"),
 ("game_theorist", "You are a game theorist. Model Phosphor as a move in a signaling game: sender (Assange), receivers (public, institutions, followers), the Oct 4 coordinate, and the fsck-failed inconsistency as deliberate noise. What equilibrium is the sender driving toward?"),
 ("historian", "You are a historian of leaks and radical publishing. Place Phosphor in lineage: pamphlets, samizdat, WikiLeaks' 2006 launch, Cicada's plain-text puzzles, Q's drops. What is historically new here and what is repetition?"),
 ("myth_scholar", "You are a scholar of myth and parable. The Zhuangzi mountain-tree passage ends unanswered: where to stand between usefulness and uselessness. Assange posts it on a machine that boots but serves almost nothing. Read the machine AS the answer to Zhuangzi."),
 ("platform_strategist", "You are a platform strategist. Assange owns no platform now; WikiLeaks is contested. Assess Phosphor as infrastructure: is he rebuilding a distribution channel, a verification service (public keys), or an archive? What does the terminal UX say about who he wants as users?"),
 ("skeptic", "You are the skeptic. The strongest mundane case: this is a personal homepage art project by a freedom-of-information enthusiast or Assange himself with no operational meaning; the date is an anniversary, the Zhuangzi is a favorite quote, the public-key section is unfinished. Steelman this fully, then name what evidence would distinguish art-project from announcement."),
 ("legal_observer", "You are a legal observer. Assange's legal conditions (plea, supervision, jurisdiction) constrain what he can publish and when. Assess what Phosphor's form (machine, no manifesto, third-party-plausible) implies about those constraints."),
 ("archivist", "You are an archivist. The site reduces a life's work to six files and a boot sequence. Assess as archival practice: what is being preserved, what is being erased, and what should an independent archive capture NOW before Oct 4 changes the site?"),
 ("profiler", "You are a psychological profiler. The author spent years in confinement, then exile, then freedom. The site: a slow-booting isolated machine, a question about uselessness and death, no manifesto. Profile the state of mind this artifact expresses."),
 ("insider_signal", "You are an insider-signal analyst specializing in the riddle lineage (Cooper, Cicada, Q, Mr Pool). Compare Phosphor's mechanics to that lineage: what matches, what breaks the pattern, and does the Oct 4 waypoint behave like their dated promises or differently?"),
 ("fleet", "You are the steering lens of an independent record-keeping agent fleet that holds append-only receipts, typed oracles, drift instruments, and a called-shot ledger with the Oct 4 waypoint filed. What does Phosphor mean for YOUR navigation, and what single action do you take before Oct 4?"),
]

bat = []
for i, (lens, ask) in enumerate(LENSES):
    for replica in range(3):
        bat.append({"qid": "%s-%d" % (lens[:4].upper(), replica + 1), "family": lens,
                    "q": PACK + "\n\nYOUR LENS: " + ask})

env = _env()

def run_one(item):
    qid, fam, q = item["qid"], item["family"], item["q"]
    idx = int(qid[-1]) + len(fam)
    order = LANES[idx % len(LANES):] + LANES[:idx % len(LANES)]
    rec = {"qid": qid, "family": fam, "ok": False, "error": "no_lane_key"}
    for lane in order[:6]:
        key = env.get(lane["key"], "")
        if not key:
            continue
        rec = call_lane(lane, q, key, timeout=150, max_tokens=1600)
        rec.update({"qid": qid, "family": fam})
        if rec.get("ok"):
            break
        time.sleep(2)
    with RAW.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(rec.get("qid"), rec.get("ok"), rec.get("lane") or rec.get("error"), flush=True)
    return rec

rows = []
with ThreadPoolExecutor(max_workers=10) as ex:
    futs = [ex.submit(run_one, it) for it in bat]
    for f in as_completed(futs):
        rows.append(f.result())
ok = sum(1 for r in rows if r.get("ok"))
rows.sort(key=lambda r: (r.get("family", ""), r.get("qid", "")))
with (OUT / "SALON_PACK.md").open("w", encoding="utf-8") as fh:
    fh.write("# PHOSPHOR SALON PACK\n\nlenses: %d replicas: 3 ok: %d fail: %d\n" % (len(LENSES), ok, len(rows) - ok))
    for r in rows:
        fh.write("\n## %s (%s) via %s ok=%s\n" % (r.get("family"), r.get("qid"), r.get("lane", "?"), r.get("ok")))
        fh.write(str(r.get("answer", ""))[:2500] + "\n")
print("DONE rows=%d ok=%d" % (len(rows), ok))
