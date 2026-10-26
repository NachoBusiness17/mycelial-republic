#!/usr/bin/env python3
"""behavior_cards_x.py - mine RIB_BEHAVIOR_CARDS from the operator's own X posts (2026-10-04).

Extends memory/rib/RIB_BEHAVIOR_CARDS_20260928.md (v1: 9 input-shape cards from session
record) with X-mined cards: decision patterns, heuristics, values, recurring stances and
reasoning moves of @NachoQuixotic, each citing the post IDs it came from.

Pipeline (deterministic first, local model second, no paid API):
  1. READ a snapshot of memory/mycelium/nodes.jsonl (never the live file; another job
     appends to it). Keep label == nachoquixotic_post, dedupe by node id (last wins).
  2. Each CARD below carries a regex family. Candidate posts = regex hits, deduped by
     normalized body (same text posted twice counts once).
  3. Local ollama (default qwen2.5:7b, temperature 0) judges the top candidates in one
     batched call per card: does each post by itself express or demonstrate the card claim?
     Only YES posts are cited.
     A card ships only with >= MIN_CITED verified posts. Judgments are cached.
  4. Outputs: sidecar JSONL (behavior_card.v1, full evidence + train_pair) and a markdown
     block appended to the v1 deck by the operator-run step (see --append-rib).

Label law (docs/ref/MAG_TRAINING_DATA_SPEC.md section 6): voice / tone / "sounds like
Nacho" is NOT a label. card_class is restricted to CLASSES below; no voice class exists.

CLI:
  .venv\\Scripts\\python.exe tools\\behavior_cards_x.py --snapshot work\\behavior_cards_20261004\\nodes_snapshot.jsonl
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLASSES = {"reasoning", "heuristic", "decision", "value", "stance", "method"}
MIN_CITED = 3
MAX_CITED = 8
MAX_JUDGE = 18

# Existing deck v1 (RIB_BEHAVIOR_CARDS_20260928.md) + mirror decision-tree principles
# (watch/inbox/burn_reset_20260927/flash50/mirror-decision-tree.md). A card with a
# non-empty "corroborates" list is counted as EXISTING (new evidence for a known pattern),
# not as a new card.
EXISTING = [
    "CARD LINK-DROP", "CARD GO", "CARD CORRECTION", "CARD TERSE-EVAL", "CARD X-DROP",
    "CARD STEAL-ORDER", "CARD FUNDING-STATEMENT", "CARD RESOURCE-ORDER", "CARD GENESIS-TESTIMONY",
    "P1 Bytes-only truth", "P7 Root-cause-design", "P8 Measured-not-pattern-matched",
    "P10 Structure-not-apology", "P5 Do, don't propose",
]

CARDS = [
 dict(id="X-STRUCTURE-OVER-INSTANCE", card_class="reasoning",
  shape="A single scandal, culprit or incident is presented as the whole story.",
  claim="He treats single incidents and single culprits as instances of a larger structure, and says exposing one instance does not solve the problem.",
  move="Name the class behind the instance before acting; fix or map the structure, not the one case.",
  corroborates=["P7 Root-cause-design", "CARD CORRECTION (classes not instances)"],
  rx=r"more than one (epstein|island)|never (just )?(a )?lone|never just one|not bugs|not a list,? it'?s a database|single blackmailer|doesn'?t solve anything|tip of the ice ?berg|franchises"),
 dict(id="X-PLAYBOOK-DETECTOR", card_class="reasoning",
  shape="A new event or crisis breaks.",
  claim="He compares new events against a repeating multi-step playbook or script he has already written down, and scores events against named tests.",
  move="Keep the written playbook; check each new event against it step by step and report which steps match.",
  corroborates=[],
  rx=r"playbook|we'?ve seen this script|the script|five.step|5.step|step script|pattern that keeps repeating|textbook|narrative tests?|same tired|same as it ever was"),
 dict(id="X-DISMISSAL-IS-SIGNAL", card_class="heuristic",
  shape="A claim is waved away with a label (conspiracy theory, no evidence, debunked) or with disbelief.",
  claim="He reads dismissal labels such as 'conspiracy theory', 'no evidence' or 'debunked' as containment phrases that signal something is being shut down, not as refutation.",
  move="When a question is closed by a label instead of evidence, treat it as open and go to the primary record.",
  corroborates=[],
  rx=r"conspiracy theor|no evidence|debunked|baseless|kill phrase|wild claim|so difficult to believe|not conspiracy|just a conspiracy"),
 dict(id="X-RECEIPTS-BY-POINTER", card_class="decision",
  shape="Someone disputes him or asks for proof.",
  claim="He answers challenges by pointing to his own earlier threads, videos and posts as the receipts instead of re-arguing from scratch.",
  move="Answer with the banked artifact (path or post link) first; re-derive only if no receipt exists.",
  corroborates=["P1 Bytes-only truth"],
  rx=r"x\.com/nachoquixotic/status|entire thread|made a thread|my other post|search my account|let me know if you need more|laid it all out"),
 dict(id="X-NO-ONE-IS-EXEMPT", card_class="heuristic",
  shape="A prominent voice, including one on his own side, pushes a line.",
  claim="He assumes prominent commentators may be controlled opposition or running a limited hangout, including people on his own side, and judges them by whether they expose the deeper layer.",
  move="Do not inherit trust from status or side; judge a source by what it actually exposes and what it avoids.",
  corroborates=[],
  rx=r"controlled opposition|limited hangout|talking heads?|be careful who you follow|nearly everyone is|works for those|if he was legit|owned\b"),
 dict(id="X-DIALECTIC-LENS", card_class="reasoning",
  shape="Two camps are fighting and you are asked to pick one.",
  claim="He frames many public conflicts as a managed dialectic, where both sides or the visible fight serve the same hidden interest, and refuses the forced binary.",
  move="Before taking a side, ask who benefits from the fight itself; look for the option outside the binary.",
  corroborates=[],
  rx=r"dialectic|uniparty|divide and conquer|kayfabe|both sides|prisoner'?s dilemma|kobayashi|no.win"),
 dict(id="X-PERCEPTION-ENGINEERING", card_class="reasoning",
  shape="A story is spreading with strong emotion attached.",
  claim="He models mass persuasion as emotion-first engineering (Bernays), tailored per-audience framing of the same event (his 'Rashomon Filter') and slow cumulative distortion (his 'Echoic Drift').",
  move="Separate the raw event from its framing; compare how each audience is being served the same material.",
  corroborates=[],
  rx=r"bernays|rashomon|roshamon|echoic drift|manufactur\w* consent|five filters|emotions before reason|hook emotions"),
 dict(id="X-COIN-A-LENS", card_class="method",
  shape="He notices a recurring mechanism without a name.",
  claim="He names recurring mechanisms himself and then reuses the name as an instrument for reading new events.",
  move="When a pattern recurs, give it a short name, define it once, and apply it as a reusable lens.",
  corroborates=[],
  rx=r"\bI call (it|the|them)|use it as a lens|as a lens|a network I call|what I call|I coined"),
 dict(id="X-PUSH-AI-PAST-DEFAULTS", card_class="method",
  shape="An AI model gives a hedged, consensus or refusal answer.",
  claim="He pushes AI models past safe consensus answers, demanding first-principles or deductive reasoning, and treats default hedging as a form of narrative control.",
  move="Do not settle for a hedged default; restate the question from axioms and primary evidence and re-run.",
  corroborates=[],
  rx=r"first princip|axiomatic|deductive|parrot consensus|approved (script|narratives?)|safe, approved|back it into a corner|break(s)? their model|arguing with ai|refuse to answer"),
 dict(id="X-CONSENT-IS-STRUCTURAL", card_class="value",
  shape="A system, rule or default is imposed without agreement.",
  claim="He treats consent as a structural boundary ('I do not consent' as a veto) rather than a courtesy.",
  move="Encode refusal and opt-out as hard boundaries in the design, not as soft settings.",
  corroborates=[],
  rx=r"i do not consent|consent is structural|do not consent|consensual"),
 dict(id="X-TRUTH-ONLY-NO-HEDGE", card_class="value",
  shape="An answer could be softened, hedged or padded.",
  claim="He demands plain, truth-only output with no corporate hedging or watered-down answers.",
  move="Say the plain verified thing; drop hedges that hide the point.",
  corroborates=["P1 Bytes-only truth", "CARD TERSE-EVAL"],
  rx=r"truth.only|no hedging|corporate hedging|watered.down|unhedged|no dogma|just proofs|truth as ugly and plain|call me on my shit"),
 dict(id="X-VERIFIABLE-ARCHITECTURE", card_class="value",
  shape="Designing governance, records or a system of trust.",
  claim="He wants governance and records to be minimal, verifiable and forkable, holding that a system's architecture is its real constitution.",
  move="Prefer designs where claims are checkable (hashes, proofs, auditable logs) and anyone can fork.",
  corroborates=["P1 Bytes-only truth"],
  rx=r"verifiab|forkable|auditable|code is law|true constitution|immutable root|root hash"),
 dict(id="X-EXPOSE-THEN-PROSECUTE", card_class="stance",
  shape="Wrongdoing by officials is documented.",
  claim="He wants documented wrongdoing answered with full transparency and prosecution, and calls on institutions to do their jobs when citizens have already done the research.",
  move="Turn findings into an accountable action with an owner; do not stop at exposure.",
  corroborates=[],
  rx=r"accountab|prosecut|do your jobs|did the work for you|bring (these|them|those) .{0,20}to justice|need justice|complete transparency|arrest criminals"),
 dict(id="X-PROTECT-CHILDREN", card_class="value",
  shape="Harm to children is in view.",
  claim="He treats the exploitation of children as the absolute moral line and the cause that keeps him going.",
  move="Treat child-safety issues as non-negotiable priority, never as a trade-off.",
  corroborates=[],
  rx=r"(children|kids|child)\b.{0,80}(traffick|predator|abuse|exploit|monsters|protect)|(traffick|predator|abuse|exploit|monsters|protect).{0,80}\b(children|kids|child)\b"),
 dict(id="X-SOUND-MONEY-DECENTRALIZE", card_class="stance",
  shape="Money, banking or economic control comes up.",
  claim="He opposes central banking and fiat money and favors decentralized, gold-backed or community-owned alternatives.",
  move="Prefer decentralized, asset-backed, community-owned designs over centralized issuers.",
  corroborates=[],
  rx=r"federal reserve|central banks?|fiat|gold.backed|sound money|stablecoin|backed by gold|debt slavery"),
 dict(id="X-COMMUNISM-AS-ELITE-TOOL", card_class="stance",
  shape="Socialist or communist politics come up.",
  claim="He frames communism and Marxism as tools used by elites to seize control, using 'useful idiots' as foot soldiers.",
  move="Read the political move by asking who ends up holding the resources and control.",
  corroborates=[],
  rx=r"communis|marxis|useful idiots|commies?\b"),
 dict(id="X-PERSIST-AND-PACE", card_class="decision",
  shape="Pressure to stop, rest or give up.",
  claim="He refuses to quit a long-running mission (a decade in), accepts personal cost, and advises others to pace themselves.",
  move="Keep the long mission running; manage pace instead of stopping.",
  corroborates=[],
  rx=r"decade|touch grass|take a break|pace yourself|die trying|can'?t let it continue|still here|won'?t stop|stopping now"),
 dict(id="X-SHIP-DRAFT-ASK-FEEDBACK", card_class="decision",
  shape="A new idea, writeup or build is ready enough to show.",
  claim="He publishes early drafts and proofs of concept openly and explicitly asks for suggestions and feedback to sharpen them.",
  move="Ship the draft with a clear ask for correction; iterate on the replies.",
  corroborates=[],
  rx=r"suggestions|feedback|let me know if i should|first draft|change anything|proof.of.concept|sharpen my understanding|keep an open mind"),
 dict(id="X-TEACH-BY-PARABLE", card_class="method",
  shape="A complex framework needs to reach ordinary people.",
  claim="He compresses complex frameworks into parables, stories and kids-book formats so they can be understood simply.",
  move="After building a framework, produce the simplest story version of it as a teaching artifact.",
  corroborates=[],
  rx=r"parable|once upon a time|kids book|metaphor key|there once was|story for grown"),
 dict(id="X-HISTORICAL-GENEALOGY", card_class="reasoning",
  shape="Explaining why a present-day situation exists.",
  claim="He explains present-day power by tracing it back through history to ancient roots and recurring precedents.",
  move="Trace the lineage of the thing (who, when, what precedent) before judging the present instance.",
  corroborates=[],
  rx=r"babylon|eleusi|ancient|centuries|133 bc|\brome\b|roman|cervantes|plato'?s cave|genealogy|lineage|through.line"),
 dict(id="X-THINK-FOR-YOURSELF", card_class="value",
  shape="Someone wants a conclusion handed to them.",
  claim="He urges people to think for themselves, keep an open mind and do their own research, holding that no one else can give you that shortcut.",
  move="Hand over the sources and the method, not just the verdict.",
  corroborates=[],
  rx=r"think for (yourself|themselves)|own research|open mind|verify truths independently|no one can give you|get right with you|examining our beliefs"),
 dict(id="X-FREE-LOCAL-SOVEREIGN-COMPUTE", card_class="decision",
  shape="A tool or capability costs money or depends on someone else's platform.",
  claim="He looks for ways to run AI work free, local and offline on hardware he controls, including swarms of small local models.",
  move="Route work to free or local lanes first; treat paid cloud dependence as a barrier to remove.",
  corroborates=["CARD RESOURCE-ORDER (free lanes)"],
  rx=r"for free|\blocal\b|offline|7b|swarm|blade server|usage bill|on your device|unlimited grok|usage is curtailed"),
 dict(id="X-VOLUNTARY-BRAID", card_class="value",
  shape="Designing how independent people or agents should cooperate.",
  claim="He wants each sovereign individual to hold their own instrument (their own mirror) and to connect with others only voluntarily.",
  move="Give each node its own copy and authority; make federation opt-in.",
  corroborates=[],
  rx=r"voluntar|every sovereign|own mirror|sovereign (individual|node|leaves|leaf)|own compact|join or at least"),
 dict(id="X-AMPLIFY-OTHERS", card_class="value",
  shape="Someone in his network does good work.",
  claim="He credits and amplifies other people's work, thanking supporters and asking for overlooked posts so he can boost them.",
  move="Credit contributors by name and route attention to under-seen good work.",
  corroborates=[],
  rx=r"more exposure|link em|love your takes|you think deeply|thank you all|thanks for reading|thank you for reading|bless you|appreciate (you|your|it|the support)|show of support"),
]

DASH_RX = re.compile("[\u2014\u2013]")


def norm_body(b: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"https?://\S+", "", b)).strip().lower()


def excerpt(body: str, rx: str, width: int = 170) -> str:
    b = re.sub(r"\s+", " ", re.sub(r"https?://\S+", "<url>", body)).strip()
    b = DASH_RX.sub(" - ", b)
    m = re.search(rx, b, re.I)
    start = max(0, (m.start() if m else 0) - width // 2)
    s = b[start:start + width].strip()
    return ("..." if start > 0 else "") + s + ("..." if start + width < len(b) else "")


def load_posts(snapshot: Path) -> list[dict]:
    d: dict[str, dict] = {}
    with snapshot.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue  # torn tail line from the concurrent appender
            if r.get("label") == "nachoquixotic_post" and r.get("body"):
                d[r["id"]] = r
    return list(d.values())


def text_for_match(r: dict) -> str:
    # strip leading @mentions; keep own-status links (receipts card needs them)
    return re.sub(r"(^|\s)@\w+", " ", r["body"])


def ollama_judge_batch(model: str, claim: str, posts: list[dict], cache: dict, url: str) -> dict:
    """One call per card: judge up to MAX_JUDGE numbered posts at once (the shared ollama runs
    MAX_LOADED_MODELS=1, so per-post calls pay a model reload each). Returns {post_id: yes|no}."""
    key = hashlib.sha256((model + "|" + claim + "|" + "|".join(p["id"] + p["body"] for p in posts)).encode()).hexdigest()
    if key in cache:
        return cache[key]
    blocks = []
    for i, p in enumerate(posts, 1):
        body = re.sub(r"\s+", " ", re.sub(r"https?://\S+", "<url>", p["body"]))[:700]
        blocks.append(f"[{i}] {body}")
    prompt = (
        "You check evidence. Below is a CLAIM about the author of some social media posts, then "
        "numbered POSTS written by that author.\n"
        f"CLAIM: {claim}\n\nPOSTS:\n" + "\n\n".join(blocks) + "\n\n"
        "For each post decide if that post, by itself, directly expresses or demonstrates the claim. "
        "Merely mentioning a keyword is not enough. Sarcasm that still supports the claim counts.\n"
        'Reply only with JSON: {"supported": [list of post numbers that support the claim]}'
    )
    payload = {"model": model, "prompt": prompt, "stream": False, "format": "json",
               "keep_alive": "15m", "options": {"temperature": 0, "num_ctx": 8192, "num_predict": 120}}
    last = None
    for _attempt in range(3):
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=900) as resp:
                out = json.loads(resp.read())["response"]
            break
        except Exception as e:  # shared ollama under load: retry, then fail loudly
            last = e
    else:
        raise RuntimeError(f"ollama unavailable: {last}")
    try:
        sup = json.loads(out).get("supported", [])
    except Exception:
        sup = [int(x) for x in re.findall(r"\d+", out)]
    sup = {int(x) for x in sup if str(x).strip().isdigit()}
    res = {p["id"]: ("yes" if i in sup else "no") for i, p in enumerate(posts, 1)}
    cache[key] = res
    return res


def build(args) -> int:
    snap = Path(args.snapshot)
    posts = load_posts(snap)
    by_id = {r["id"]: r for r in posts}
    cache_path = Path(args.cache)
    cache: dict = {}
    if cache_path.is_file():
        for line in cache_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                o = json.loads(line)
                cache[o["k"]] = o["v"]
    n_cache0 = len(cache)
    cards_out, matched_any, cited_any = [], set(), set()
    for c in CARDS:
        assert c["card_class"] in CLASSES, c["id"]
        rx = c["rx"]
        hits = [r for r in posts if re.search(rx, text_for_match(r), re.I)]
        matched_any.update(r["id"] for r in hits)
        seen, cand = set(), []
        for r in hits:
            nb = norm_body(r["body"])
            if nb in seen or len(nb) < 25:
                continue
            seen.add(nb)
            cand.append(r)
        cand.sort(key=lambda r: (-len(re.findall(rx, text_for_match(r), re.I)),
                                 -min(len(r["body"]), 700), r["id"]))
        batch = cand[:MAX_JUDGE]
        verdict = ollama_judge_batch(args.model, c["claim"], batch, cache, args.ollama) if batch else {}
        judged = len(batch)
        cited = [r for r in batch if verdict.get(r["id"]) == "yes"][:MAX_CITED]
        status = "kept" if len(cited) >= MIN_CITED else "dropped_insufficient_evidence"
        ev = [{"post_id": r["id"], "url": r.get("meta", {}).get("url", ""),
               "created_at": r.get("meta", {}).get("created_at", ""),
               "excerpt": excerpt(r["body"], rx)} for r in cited]
        card = {
            "schema": "behavior_card.v1", "id": c["id"], "card_class": c["card_class"],
            "deck": "RIB_BEHAVIOR_CARDS", "source": "x_history_mine:nachoquixotic",
            "shape": c["shape"], "pattern": c["claim"], "seat_move": c["move"],
            "relation": "corroborates_existing" if c["corroborates"] else "new",
            "corroborates": c["corroborates"], "status": status,
            "support": {"regex_hits": len(hits), "unique_candidates": len(cand),
                        "judged": judged, "verified": len(cited),
                        "verifier": f"ollama:{args.model}:t0:batch"},
            "evidence": ev,
            "train_pair": {"situation": c["shape"], "decision_pattern": c["claim"],
                           "cited_post_ids": [e["post_id"] for e in ev]},
            "label_law": "decision/reasoning only; voice is not a label (MAG_TRAINING_DATA_SPEC s6)",
            "built_at": datetime.now(timezone.utc).isoformat(),
            "snapshot": str(snap), "snapshot_posts": len(posts),
        }
        if status == "kept":
            cited_any.update(e["post_id"] for e in ev)
        cards_out.append(card)
        print(f"{c['id']:32s} hits={len(hits):4d} judged={judged:2d} verified={len(cited)} {status}", flush=True)
        with cache_path.open("w", encoding="utf-8") as fh:
            for k, v in cache.items():
                fh.write(json.dumps({"k": k, "v": v}) + "\n")
    # no-invention gate: every cited id must exist in the snapshot
    for card in cards_out:
        for e in card["evidence"]:
            assert e["post_id"] in by_id, e["post_id"]
            assert not DASH_RX.search(e["excerpt"])
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        for card in cards_out:
            fh.write(json.dumps(card, ensure_ascii=False) + "\n")
    summary = {"posts": len(posts), "cards_defined": len(CARDS),
               "kept": sum(c["status"] == "kept" for c in cards_out),
               "kept_new": sum(c["status"] == "kept" and c["relation"] == "new" for c in cards_out),
               "kept_corroborating": sum(c["status"] == "kept" and c["relation"] != "new" for c in cards_out),
               "posts_matched_any_family": len(matched_any), "posts_cited": len(cited_any),
               "llm_calls_new": len(cache) - n_cache0}
    Path(args.summary).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary))
    return 0


def render_md(cards_path: Path) -> str:
    cards = [json.loads(l) for l in cards_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    lines = ["", "---", "", "## X-MINED CARDS (v2, 2026-10-04, tools/behavior_cards_x.py)", "",
             "Source: the operator's own @NachoQuixotic posts (mycelium snapshot). Every card cites",
             "post IDs verified by a local model (ollama, temperature 0) as expressing the pattern.",
             "Full evidence + excerpts: memory/rib/RIB_BEHAVIOR_CARDS_X_20261004.jsonl.",
             "Decision/reasoning patterns only; voice is not a label.", ""]
    for c in cards:
        if c["status"] != "kept":
            continue
        rel = ("corroborates " + "; ".join(c["corroborates"])) if c["corroborates"] else "new"
        ids = ", ".join(e["post_id"].replace("x:", "") for e in c["evidence"])
        lines += [f"## CARD: {c['id']} ({c['card_class']}, {rel})",
                  f"**Shape:** {c['shape']}",
                  f"**Pattern:** {c['pattern']}",
                  f"**Invoke:** {c['seat_move']}",
                  f"**Evidence ({c['support']['verified']} verified of {c['support']['regex_hits']} regex hits):** x:{ids}", ""]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", default=str(ROOT / "work/behavior_cards_20261004/nodes_snapshot.jsonl"))
    ap.add_argument("--out", default=str(ROOT / "memory/rib/RIB_BEHAVIOR_CARDS_X_20261004.jsonl"))
    ap.add_argument("--summary", default=str(ROOT / "work/behavior_cards_20261004/summary.json"))
    ap.add_argument("--cache", default=str(ROOT / "work/behavior_cards_20261004/judge_cache.jsonl"))
    ap.add_argument("--model", default="qwen2.5:7b")
    ap.add_argument("--ollama", default="http://127.0.0.1:11434/api/generate")
    ap.add_argument("--render-md", action="store_true", help="print the deck block for --out and exit")
    args = ap.parse_args()
    if Path(args.snapshot).resolve() == (ROOT / "memory/mycelium/nodes.jsonl").resolve():
        print("refusing to read the live nodes.jsonl; snapshot it first", file=sys.stderr)
        return 2
    if args.render_md:
        sys.stdout.reconfigure(encoding="utf-8")
        print(render_md(Path(args.out)))
        return 0
    return build(args)


if __name__ == "__main__":
    raise SystemExit(main())
