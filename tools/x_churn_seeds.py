"""x_churn_seeds — semantic adjacency churn: feed the estate's known posts to the
SD-seat Grok CLI as seeds, harvest similar/adjacent posts by the same author, expand
one bounded round, dedupe against the inventory, vxtwitter-pull new posts, grade hits.
Operator method (2026-09-23 night): feed it the posts you have, ask for similar and
adjacent. Two rounds, bounded. SSRF law on the vxtwitter door.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from mag import lite_guard  # noqa: E402

GROK_EXE = r"C:\Users\foste\.grok\bin\grok.exe"
SD_HOME = r"C:\Users\foste\.grok-sd"
OUT_MD = ROOT / "watch" / "inbox" / "X_ANCHOR_MAP_SEEDS_20260923.md"
OUT_JSONL = ROOT / "state" / "fuel" / "x_churn_seed_hits.jsonl"
ID_RE = re.compile(r"x\.com/NachoQuixotic/status/(\d{18,20})")
HANDLE = "NachoQuixotic"

# Seeds: the estate's known posts, chosen for family diversity (one per ledger family).
SEEDS = [
    ("adrenochrome-thesis", "2026363093530587219",
     "Core claims from my Adrenochrome/MK stack. Sources so you can verify. No trust me BRO, "
     "check yourself. Ancient psychedelics democratized divine access, suppressed and twisted "
     "into control. Eleusinian kykeon: visionary barley brew; ergot (LSD precursor) hypothesis "
     "from Wasson/Hofmann/Ruck (1978). The Road to Eleusis PDF."),
    ("dutroux-belgium", "2025755256764719459",
     "Dutroux: Belgium's 1996 Epstein. The X-dossiers, Regina Louf testimony, the White March, "
     "and the cover-up playbook: police 'inept, inefficient and ill-equipped' by the parliament's "
     "own finding, witnesses discredited, prosecutors removed."),
    ("families-cave", "1986938246241145297",
     "Most of the world is small towns. Unseen families do not till. They farm the collective "
     "through parasitic bureaucracy, select flexible people, bind them with secrets, and activate "
     "them to set the town on itself. Consciousness itself is a force for change; the awakening is "
     "the threat they budget against."),
    ("adrenochrome-essay", "1898754266598113295",
     "The inverted sacrament essay: the ancient mysteries' sacrament inverted into a harvest. "
     "Eleusis to adrenochrome, shame as the chain that holds the powerful, the books in the cellar "
     "as the leverage that keeps them."),
    ("black-nobility", "1975958311624171607",
     "The Black Nobility manifesto: Jekyll Island as ritual, Rothschild proxies, the Federal "
     "Reserve's founding, Bretton Woods, and how fiat is the arithmetic of the same aristocracy "
     "that never left — monopoly translated out of official aristocracy into democracy."),
    ("bernays-cic", "1952379531991376246",
     "Bernays, Church, and the Censorship-Industrial Complex: xAI's policies as the modern "
     "echo of Bernays' engineered consent; Church's 'tyranny total in America' warning; the CIC "
     "hydra from DHS to Stanford; the Rubicon was crossed and almost nobody noticed."),
    ("apathy-consent", "1876647276996964607",
     "Apathy as consent: the cult-like network thrives because people are wrapped in their own "
     "bubbles. If they tell you what they're going to do and you don't object, you are a "
     "consenting party. These mystery cults thrive on us not caring; your attention is valuable."),
    ("church-smithmundt", "1878034897727623494",
     "Frank Church led the committee that exposed COINTELPRO and MKULTRA; he warned 'I know the "
     "capacity that is there to make tyranny total in America.' The Smith-Mundt Modernization Act "
     "let government-produced material flow to domestic audiences. The Rubicon was crossed and "
     "almost nobody was paying attention."),
    ("great-awakening", "1888898115131867151",
     "We inhabit a world meticulously crafted, the boundaries of thought policed by those with "
     "much to conceal. We are shadows on Plato's cave wall. The deep state is controlled by "
     "ancient dynasties using dark rituals, technology, media, and esoteric knowledge to keep "
     "the populace in eternal slumber. Believe nothing unless you can prove it with your own research."),
    ("five-track-machine", "2044802518354374923",
     "The five-track machine: break the mind, remove the threat, harvest the blackmail, control "
     "perception through drift and Rashomon crops, contain the leak through ridicule and limited "
     "files. The same sequence across JFK, Franklin, Belgium, Epstein collapses the coincidence floor."),
]

ANCHOR_SIGNALS = re.compile(
    r"(19\d\d|20\d\d)|("
    r"Smith-Mundt|Church|COINTELPRO|MKULTRA|Bernays|Ellul|Jung|Wasson|Hofmann|Ruck|Eleusis|"
    r"Epstein|Maxwell|Brunel|Dutroux|Franklin|Pike|Taxil|Margiotta|Illuminati|Bavarian|"
    r"Tartaria|Enoch|Dead Sea|adrenochrome|Huxley|loosh|Bohemian|Grove|Jekyll|Rothschild|Rockefeller|"
    r"Federal Reserve|Torture Report|Pentagon Papers|Family Jewels|Operation |CTIL|GEC|USAID|"
    r"blackmail|kompromat|trafficking)", re.I)

INVENTORY_FILES = [
    ROOT / "watch" / "inbox" / "ACCOUNT_VS_AUDIT_20260923.md",
    ROOT / "corpus" / "canon" / "founding_curriculum" / "FOUNDING_CURRICULUM.md",
    ROOT / "corpus" / "canon" / "x_canon_2025_pass3.md",
    ROOT / "corpus" / "canon" / "x_canon_2025_pass6.md",
    ROOT / "corpus" / "canon" / "receipts_dec2025_mar2026.md",
]


def known_ids() -> set:
    ids = set()
    for p in INVENTORY_FILES:
        if p.is_file():
            ids |= set(ID_RE.findall(p.read_text(encoding="utf-8", errors="replace")))
    return ids


def pull_post(pid: str) -> dict | None:
    pid = str(pid)
    if not re.fullmatch(r"\d{18,20}", pid):
        return None
    from mag import lite_guard
    url = f"https://api.vxtwitter.com/{HANDLE}/status/{pid}"
    if not lite_guard._safe_https_url(url):
        return None
    try:
        req = urllib.request.Request(url)
        with lite_guard._OPENER.open(req, timeout=20) as r:
            d = json.loads(r.read().decode())
        return {"id": pid, "date": d.get("date"), "text": (d.get("text") or "")[:600],
                "likes": d.get("likes"), "rts": d.get("retweets")}
    except Exception:
        return None


def run_cli_query(prompt: str, timeout: int = 480) -> str:
    env = dict(os.environ)
    env["GROK_HOME"] = SD_HOME
    proc = subprocess.Popen([GROK_EXE, "--output-format", "plain", prompt],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, errors="replace", env=env)
    timed_out = False
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        proc.kill()
        out, err = proc.communicate()
    out = (out or "") + "\n" + (err or "")
    if timed_out:
        out += "\n[TIMEOUT - partial output above]"
    return out


def seed_query(seed_name: str, seed_text: str) -> str:
    return (f"Here is a post by @{HANDLE}:\n\n\"{seed_text[:300]}\"\n\n"
            f"Find OTHER posts by @{HANDLE} (not this one) that are semantically similar "
            f"or thematically adjacent — same topics, same cited sources, same arguments, "
            f"same era. List up to 10: full status URL "
            f"(https://x.com/{HANDLE}/status/<id>), date, likes if visible, one-sentence gist. "
            f"Only real posts by this handle. No commentary.")


def main() -> dict:
    known = known_ids()
    log_rows = []

    # Round 1: each seed asks for its semantic neighborhood.
    found: dict[str, dict] = {}
    for name, pid, text in SEEDS:
        t0 = time.time()
        try:
            out = run_cli_query(seed_query(name, text))
        except Exception as e:
            log_rows.append({"round": 1, "seed": name,
                             "error": type(e).__name__ + ": " + str(e)[:80]})
            print(json.dumps(log_rows[-1]), flush=True)
            continue
        new = 0
        for cid in set(ID_RE.findall(out)):
            if cid != pid and cid not in known and cid not in found:
                post = pull_post(cid)
                if post and (post.get("text") or "").strip():
                    found[cid] = {"seed": name, **post}
                    new += 1
        log_rows.append({"round": 1, "seed": name, "new_hits": new,
                         "secs": round(time.time() - t0)})
        print(json.dumps(log_rows[-1]), flush=True)

    # Round 2: the top new hits become seeds (bounded expansion, 5 seats).
    round2_seeds = sorted(found.values(), key=lambda h: -(h.get("likes") or 0))[:5]
    for h in round2_seeds:
        t0 = time.time()
        out = run_cli_query(seed_query("expansion:" + h["id"], h["text"]))
        new = 0
        for cid in set(ID_RE.findall(out)):
            if cid != h["id"] and cid not in known and cid not in found:
                post = pull_post(cid)
                if post and (post.get("text") or "").strip():
                    found[cid] = {"seed": "expansion:" + h["id"], **post}
                    new += 1
        log_rows.append({"round": 2, "seed": h["id"], "new_hits": new,
                         "secs": round(time.time() - t0)})
        print(json.dumps(log_rows[-1]), flush=True)

    hits = [v for v in found.values() if ANCHOR_SIGNALS.search(v.get("text") or "")]
    for h in hits:
        OUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
        with OUT_JSONL.open("a", encoding="utf-8") as f:
            f.write(json.dumps(h) + "\n")

    md = [
        "# X ANCHOR MAP — seed-similarity churn (SD seat, 2 rounds)",
        "",
        f"2026-09-23 night · method: 10 known posts seeded, Grok asked for similar/adjacent, "
        f"top new hits expanded once · new posts: {len(found)} · anchor hits: {len(hits)}",
        "",
        "## Hits, by engagement",
        "",
    ]
    for h in sorted(hits, key=lambda h: -(h.get("likes") or 0)):
        md.append(f"- **{h['date']}** · {h['likes']} likes · RTs {h.get('rts')} · seed: {h['seed']}")
        md.append(f"  - https://x.com/{HANDLE}/status/{h['id']}")
        md.append(f"  - > {(h['text'] or '')[:220].replace(chr(10), ' ')}")
    md += ["", "## Churn log", "", json.dumps(log_rows, indent=1), "",
           "*Append-only. Anchors feed the conversion plan's re-ladder.*"]
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    return {"new_posts": len(found), "hits": len(hits), "file": str(OUT_MD)}


if __name__ == "__main__":
    print(json.dumps(main(), indent=1))
