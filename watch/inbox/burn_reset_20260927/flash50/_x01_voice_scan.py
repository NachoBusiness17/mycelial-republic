# x-01 voice-feature scan over mycelium x: nodes (@NachoQuixotic corpus).
# Read-only. Pure stdlib. No subprocess. Bodies are aggregated into stats,
# never printed whole to stdout; exemplars go to _x01_samples.txt for the
# operator's own repo reading, mirroring the sibling _f26 instrument style.
import json
import re
import random
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
NODES = ROOT / "memory" / "mycelium" / "nodes.jsonl"
OUT_STATS = Path(__file__).resolve().parent / "_x01_stats.json"
OUT_SAMPLES = Path(__file__).resolve().parent / "_x01_samples.txt"

EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U00002700-\U000027BF\U0001F000-\U0001F0FF\U00002600-\U000026FF]"
)
WORD_RE = re.compile(r"[a-z0-9']+")

STOP = set("""a an the and or but of to in on for with at by from as is are was were be been being
it its it's this that these those i you he she they we my your his her their our me him them us
do does did done not no yes so if then than too very just about into over under out up down off
what which who whom whose when where why how all any both each few more most other some such only
own same s t can will don should now has have had having would could ought im ive dont cant wont
thats youre youre gonna wanna gotta""".split())

REGISTER_PRIORITY = ["doctrine", "essay", "humor", "shitpost", "reply", "unclassified"]


def primary_register(voice_tags):
    for r in REGISTER_PRIORITY:
        if r in voice_tags:
            return r
    return voice_tags[0] if voice_tags else "none"


def pct(sorted_vals, p):
    if not sorted_vals:
        return 0
    idx = min(len(sorted_vals) - 1, int(p * (len(sorted_vals) - 1)))
    return sorted_vals[idx]


def analyze(rows):
    n = len(rows)
    if n == 0:
        return {"n": 0}
    chars = sorted(len(r["body"]) for r in rows)
    words_all = [len(WORD_RE.findall(r["body"].lower())) for r in rows]
    chars_s = sorted(chars)
    words_s = sorted(words_all)
    feats = Counter()
    totals = Counter()
    unigrams = Counter()
    bigrams = Counter()
    trigrams = Counter()
    openers = Counter()
    profanity_hits = Counter()
    PROFS = ["fuck", "shit", "bitch", "damn", "hell", "crap", "ass"]
    for r in rows:
        b = r["body"]
        low = b.lower()
        feats["emoji"] += 1 if EMOJI_RE.search(b) else 0
        feats["multiline"] += 1 if "\n" in b else 0
        feats["ends_period"] += 1 if b.rstrip().endswith(".") else 0
        feats["ends_any_punct"] += 1 if b.rstrip()[-1:] in ".!?" else 0
        feats["ends_question"] += 1 if b.rstrip().endswith("?") else 0
        feats["has_question"] += 1 if "?" in b else 0
        feats["has_exclaim"] += 1 if "!" in b else 0
        feats["starts_lower"] += 1 if b[:1].islower() else 0
        feats["starts_dig"] += 1 if b[:1].isdigit() else 0
        feats["starts_I"] += 1 if b.startswith("I ") or b.startswith("I'") else 0
        feats["has_lowercase_i"] += 1 if re.search(r"(?<![A-Za-z'])i(?![A-Za-z'])", b) else 0
        feats["has_you"] += 1 if re.search(r"\byou\b|\byou're\b|\byour\b", low) else 0
        feats["has_I"] += 1 if re.search(r"\bI\b", b) else 0
        feats["has_url"] += 1 if re.search(r"https?://|t\.co/", b) else 0
        feats["has_hashtag"] += 1 if "#" in b else 0
        feats["has_mention"] += 1 if "@" in b else 0
        feats["has_ellipsis"] += 1 if re.search(r"\.\.\.|…", b) else 0
        feats["has_emdash"] += 1 if re.search(r"—|―|――", b) else 0
        feats["has_endash"] += 1 if "–" in b else 0
        feats["has_hyphen"] += 1 if re.search(r"(\w)-(\w)", b) else 0
        feats["has_semicolon"] += 1 if ";" in b else 0
        feats["has_colon"] += 1 if ":" in b else 0
        feats["has_parens"] += 1 if "(" in b else 0
        feats["has_dquote"] += 1 if '"' in b else 0
        feats["has_scare_quotes"] += 1 if re.search(r'"[^"]{2,40}"', b) else 0
        feats["has_asterisk"] += 1 if "*" in b else 0
        feats["has_arrow"] += 1 if "->" in b or "→" in b else 0
        feats["not_but"] += 1 if re.search(r"\bnot\s[^.!?]{1,60}?\bbut\b", low) else 0
        feats["is_just"] += 1 if re.search(r"\b(is|are|was|were)\s+just\b", low) else 0
        feats["the_real"] += 1 if re.search(r"\bthe real\b", low) else 0
        feats["everyone"] += 1 if re.search(r"\b(everyone|everybody|nobody|no one)\b", low) else 0
        feats["literally"] += 1 if "literally" in low else 0
        feats["actually"] += 1 if "actually" in low else 0
        feats["lol_family"] += 1 if re.search(r"\b(lol|lmao|lmfao|rofl)\b", low) else 0
        feats["profane"] += 1 if any(p in low for p in PROFS) else 0
        for p in PROFS:
            if p in low:
                profanity_hits[p] += 1
        shout_words = [w for w in re.findall(r"[A-Z]{3,}[S]?", b)]
        feats["has_shout"] += 1 if any(w.isupper() and len(w) >= 3 for w in shout_words) else 0
        contr = len(re.findall(r"\b\w+'(t|s|re|ve|ll|d|m)\b", b))
        feats["_contractions"] += contr
        feats["_words"] += sum(words_all) if False else max(1, len(WORD_RE.findall(low)))
        opener = b.strip().split()
        if opener:
            openers[opener[0].lower()] += 1
        toks = WORD_RE.findall(low)
        for i, w in enumerate(toks):
            unigrams[w] += 1
            if i + 1 < len(toks):
                bigrams[(toks[i], toks[i + 1])] += 1
            if i + 2 < len(toks):
                trigrams[(toks[i], toks[i + 1], toks[i + 2])] += 1
    words_tot = max(1, feats["_words"])
    out = {
        "n": n,
        "char_mean": round(sum(chars) / n, 1),
        "char_p10": pct(chars_s, 0.10),
        "char_median": pct(chars_s, 0.50),
        "char_p90": pct(chars_s, 0.90),
        "char_max": chars_s[-1],
        "word_mean": round(sum(words_all) / n, 1),
        "word_p90": pct(words_s, 0.90),
        "contractions_per_100_words": round(100 * feats.pop("_contractions") / words_tot, 1),
        "feature_rates_pct": {
            k: round(100 * v / n, 1) for k, v in sorted(feats.items(), key=lambda kv: -kv[1])
        },
        "top_openers": openers.most_common(15),
        "top_unigrams_content": [(w, c) for w, c in unigrams.most_common(400) if w not in STOP][:35],
        "top_bigrams": [(a + " " + b, c) for (a, b), c in bigrams.most_common(400) if a not in STOP and b not in STOP][:25],
        "top_trigrams": [(" ".join(t), c) for t, c in trigrams.most_common(400) if not any(x in STOP for x in t)][:15],
        "profanity_hits": dict(profanity_hits.most_common()),
    }
    return out


def main():
    rows = []
    seen_ids = set()
    total_nodes = 0
    empty_body = 0
    for line in open(NODES, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        if not r.get("id", "").startswith("x:"):
            continue
        total_nodes += 1
        m = r.get("meta") or {}
        sid = str(m.get("status_id") or r["id"])
        body = (r.get("body") or "").strip()
        if not body or len(body) < 5:
            empty_body += 1
            continue
        if sid in seen_ids:
            continue
        seen_ids.add(sid)
        voice = [str(v) for v in (m.get("voice") or [])]
        eng = m.get("engagement") if isinstance(m.get("engagement"), dict) else {}
        rows.append(
            {
                "body": body,
                "register": primary_register(voice),
                "voice_all": voice,
                "likes": eng.get("likes", 0),
                "replies": eng.get("replies", 0),
                "sid": sid,
                "has_engagement": bool(eng),
                "pilot": m.get("pilot", ""),
            }
        )
    stats = {
        "total_x_nodes": total_nodes,
        "bodies_analyzed": len(rows),
        "empty_or_id_only": empty_body,
        "dedup_skipped": total_nodes - empty_body - len(rows),
        "registers": {k: sum(1 for r in rows if r["register"] == k) for k in REGISTER_PRIORITY},
        "overall": analyze(rows),
        "by_register": {},
    }
    for reg in REGISTER_PRIORITY:
        sub = [r for r in rows if r["register"] == reg]
        stats["by_register"][reg] = analyze(sub)
    # engagement-weighted: likes by register (only rows that carry engagement)
    eng_rows = [r for r in rows if r["has_engagement"]]
    likes_by_reg = defaultdict(list)
    for r in eng_rows:
        likes_by_reg[r["register"]].append(r["likes"])
    stats["engagement"] = {
        "rows_with_engagement": len(eng_rows),
        "mean_likes_by_register": {
            k: round(sum(v) / len(v), 1) for k, v in likes_by_reg.items() if v
        },
        "median_likes_by_register": {
            k: pct(sorted(v), 0.5) for k, v in likes_by_reg.items() if v
        },
    }
    # exemplars: top-liked, long essays, random shitposts, random replies
    random.seed(42)
    picks = []
    picks += sorted(eng_rows, key=lambda r: -r["likes"])[:20]
    essays = sorted(
        [r for r in rows if r["register"] == "essay"], key=lambda r: -len(r["body"])
    )
    picks += essays[:15]
    picks += random.sample([r for r in rows if r["register"] == "shitpost"], min(25, sum(1 for r in rows if r["register"] == "shitpost")))
    picks += random.sample([r for r in rows if r["register"] == "reply"], min(25, sum(1 for r in rows if r["register"] == "reply")))
    picks += random.sample([r for r in rows if r["register"] == "doctrine"], min(15, sum(1 for r in rows if r["register"] == "doctrine")))
    picks += random.sample([r for r in rows if r["register"] == "humor"], min(10, sum(1 for r in rows if r["register"] == "humor")))
    with open(OUT_SAMPLES, "w", encoding="utf-8") as f:
        for r in picks:
            f.write(
                f"=== {r['register']} likes={r['likes']} sid={r['sid']} len={len(r['body'])}\n{r['body']}\n\n"
            )
    with open(OUT_STATS, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in stats.items() if k not in ("overall", "by_register")}, indent=1)[:1200])
    print("OVERALL:", json.dumps(stats["overall"], indent=1)[:3000])
    for reg in REGISTER_PRIORITY:
        print(f"REG {reg}:", json.dumps(stats["by_register"][reg])[:900])
    print("wrote", OUT_STATS.name, "and", OUT_SAMPLES.name)


if __name__ == "__main__":
    main()
