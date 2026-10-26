"""B2-78 denominator recount instrument (2026-09-26).

Re-derives every number cited by RESEARCH_GAP_ANALYSIS_20260918.md from ledger
bytes. Read-only. Emits one JSON blob to stdout (also saved next to this file).

Instruments named:
  * coverage header counts: tools/research.py research_stats shape
    (LINKS.jsonl line count, memory/lenses/corpus_index.json count field)
  * domain pass: keyword lists in DOMAIN_KEYS below, applied to
    canonical+title+note of each LINKS row, computed twice:
    seed-era subset (ts date <= 2026-09-18, validation vs seed numbers)
    and current bytes (the refreshed denominator).
  * union drive: raw.jsonl / queue.jsonl / state.json full recount.
"""
from __future__ import annotations
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent")
LINKS = REPO / "watch/inbox/LINKS.jsonl"
CORPUS_INDEX = REPO / "memory/lenses/corpus_index.json"
RAW = REPO / "watch/inbox/union_fullsend_20260917/raw.jsonl"
QUEUE = REPO / "watch/inbox/union_fullsend_20260917/queue.jsonl"
STATE = REPO / "watch/inbox/union_fullsend_20260917/state.json"
OUT = REPO / "watch/inbox/burn_wave_20260926/B2_78_denominator_recount.json"

SEED_CUTOFF = "2026-09-18"  # analysis date; rows stamped on/before are the seed-era subset

# Keyword lists for the domain pass (case-insensitive substring over
# canonical + title + note). Named here because the seed did not persist lists.
DOMAIN_KEYS = {
    "x-social/intel": None,  # special: canonical contains x.com or twitter.com
    "fleet-history": ["fleet"],
    "retrieval": ["retrieval", "rag", "embedding", "vector store", "fts", "search eval", "corpus search"],
    "finetune": ["finetune", "fine-tune", "lora", "qlora", "training run", "training pdf"],
    "mesh": ["mesh", "a2a", "agent2agent", "autogen", "camel", "mcp", "agent comms", "inter-agent"],
    "games": ["game", "dungeon", "2d6", "roblox", "gamelog", "playtest"],
    "prompt-cache": ["prompt cache", "caching", "kv cache", "invalidation", "context reuse", "cache hit"],
    "security/keys": ["secret", "credential", "api key", "key rotation", "gitleaks", "key-scan", "sanitiz"],
    "steering/persuasion": ["steering", "priming", "persuasion", "in-context learning", "icl", "prime"],
    "esoteric": ["esoteric", "occult", "tarot", "qabalah", "hermetic"],
    "windows/storage": ["junction", "reparse", "mft", "ntfs", "windows storage", "hardlink", "symlink"],
    "swarm/orchestration": ["swarm", "orchestr", "fanout", "fan-out", "retry budget", "circuit breaker", "backoff"],
}


def load_jsonl(path: Path):
    rows = []
    bad = 0
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                bad += 1
    return rows, bad


def row_date(row) -> str:
    ts = str(row.get("ts") or "")
    m = re.match(r"(\d{4}-\d{2}-\d{2})", ts)
    return m.group(1) if m else ""


def domain_counts(rows):
    """Return per-domain counts: (seed_era, current, current_event_rows_excluded)."""
    out = {}
    for dom, keys in DOMAIN_KEYS.items():
        seed_n = 0
        cur_n = 0
        for r in rows:
            canon = str(r.get("canonical") or "")
            title = str(r.get("title") or "")
            note = str(r.get("note") or "")
            hay = (canon + " " + title + " " + note).lower()
            if dom == "x-social/intel":
                hit = ("x.com/" in canon) or ("twitter.com/" in canon)
            else:
                hit = any(k in hay for k in keys)
            if not hit:
                continue
            d = row_date(r)
            if d and d <= SEED_CUTOFF:
                seed_n += 1
            cur_n += 1
        out[dom] = {"seed_era": seed_n, "current": cur_n}
    return out


def recount_union():
    raw, raw_bad = load_jsonl(RAW)
    queue, queue_bad = load_jsonl(QUEUE)
    state = json.loads(STATE.read_text(encoding="utf-8"))

    total = len(raw)
    ok_rows = [r for r in raw if r.get("ok") is True]
    fail_rows = [r for r in raw if r.get("ok") is False]
    attempt_matrix = Counter((int(r.get("attempt") or 0), bool(r.get("ok"))) for r in raw)

    ids_touched = {str(r.get("subsystem")) for r in raw}
    ok_ids = {str(r.get("subsystem")) for r in ok_rows}
    never_ok = sorted(ids_touched - ok_ids)
    queue_ids = [str(q.get("id")) for q in queue]
    queue_id_set = set(queue_ids)

    ok_by_id = Counter(str(r.get("subsystem")) for r in ok_rows)
    multi_ok = {i: c for i, c in ok_by_id.items() if c > 1}
    top_offender = max(multi_ok.items(), key=lambda kv: kv[1]) if multi_ok else None

    # attempts per id (max attempt seen) for per-dig attempt stats
    attempts_by_id = defaultdict(int)
    for r in raw:
        attempts_by_id[str(r.get("subsystem"))] = max(attempts_by_id[str(r.get("subsystem"))], int(r.get("attempt") or 0))

    # token accounting on ok rows only (v1 records usage nowhere else)
    def usage(r):
        u = r.get("usage")
        return u if isinstance(u, dict) else None

    tok_total = tok_prompt = tok_completion = 0
    per_ok_tokens = {}
    for r in ok_rows:
        u = usage(r)
        if u:
            t = int(u.get("total_tokens") or 0)
            per_ok_tokens[str(r.get("subsystem")) + "#" + str(r.get("attempt"))] = t
            tok_total += t
            tok_prompt += int(u.get("prompt_tokens") or 0)
            tok_completion += int(u.get("completion_tokens") or 0)
    fail_with_usage = sum(1 for r in fail_rows if usage(r))

    # refire waste: tokens on ok rows beyond the first ok per id
    first_only_tokens = 0
    refire_tokens = 0
    seen_ok = set()
    for r in raw:
        if r.get("ok") is not True:
            continue
        uid = str(r.get("subsystem"))
        u = usage(r) or {}
        t = int(u.get("total_tokens") or 0)
        if uid in seen_ok:
            refire_tokens += t
        else:
            seen_ok.add(uid)
            first_only_tokens += t

    completed = len(ok_ids)
    mean_ok = tok_total / len(ok_rows) if ok_rows else 0
    all_in_per_dig = tok_total / completed if completed else 0
    floor_per_dig = first_only_tokens / completed if completed else 0
    max_row = max(per_ok_tokens.items(), key=lambda kv: kv[1]) if per_ok_tokens else None

    # failure taxonomy
    fail_tax = Counter()
    for r in fail_rows:
        err = str(r.get("error") or "")
        m = re.search(r"HTTP Error (\d+)", err) or re.search(r"(\d{3})", err)
        lane = str(r.get("lane") or r.get("model") or "?")
        code = m.group(1) if m else (err[:40] if err else "empty_content/none")
        fail_tax[f"{code}:{lane}"] += 1

    # queue integrity
    dup_queue = [i for i, c in Counter(queue_ids).items() if c > 1]
    no_rows = sorted(queue_id_set - ids_touched)

    # state vs bytes
    done = set(state.get("done") or [])
    done_not_ok = sorted(done - ok_ids)
    ok_not_done = sorted(ok_ids - done)

    # gap digs UF-124..UF-131 status
    gap = {}
    for n in range(124, 132):
        uid = f"UF-{n}"
        rows_for = [r for r in raw if str(r.get("subsystem")) == uid]
        gap[uid] = {
            "in_queue": uid in queue_id_set,
            "attempts": len(rows_for),
            "ok_rows": sum(1 for r in rows_for if r.get("ok") is True),
            "ok": uid in ok_ids,
            "in_state_done": uid in done,
        }

    return {
        "raw_rows": total,
        "raw_bad_lines": raw_bad,
        "ok_rows": len(ok_rows),
        "fail_rows": len(fail_rows),
        "row_ratio": round(len(ok_rows) / total, 4) if total else None,
        "attempt_matrix": {f"attempt{k[0]}|ok={k[1]}": v for k, v in sorted(attempt_matrix.items())},
        "unique_ids_touched": len(ids_touched),
        "queue_ids": len(queue_ids),
        "queue_dup_ids": dup_queue,
        "completed_ids": completed,
        "completion_ratio": round(completed / len(ids_touched), 4) if ids_touched else None,
        "never_ok_ids": never_ok,
        "queue_ids_with_no_rows": no_rows,
        "multi_ok_id_count": len(multi_ok),
        "multi_ok_top": top_offender,
        "tokens": {
            "recorded_on": "ok rows only (v1 records usage in call() ok path)",
            "total": tok_total,
            "prompt": tok_prompt,
            "completion": tok_completion,
            "ok_rows_with_usage": len(per_ok_tokens),
            "fail_rows_with_usage": fail_with_usage,
            "mean_per_ok_row": round(mean_ok, 1),
            "max_row": max_row,
            "first_completion_only_tokens": first_only_tokens,
            "refire_waste_tokens": refire_tokens,
            "refire_waste_pct_of_recorded": round(100 * refire_tokens / tok_total, 1) if tok_total else None,
            "all_in_tokens_per_completed_dig": round(all_in_per_dig, 1),
            "first_completion_floor_per_dig": round(floor_per_dig, 1),
        },
        "attempts_per_completed_dig": round(sum(attempts_by_id[i] for i in ok_ids) / completed, 3) if completed else None,
        "failure_taxonomy": dict(fail_tax.most_common()),
        "state_done_count": len(done),
        "state_done_missing_ok_row": done_not_ok,
        "ok_ids_missing_from_state": ok_not_done,
        "gap_digs_UF124_131": gap,
    }


def recount_links():
    rows, bad = load_jsonl(LINKS)
    event_rows = [r for r in rows if r.get("kind")]
    link_rows = [r for r in rows if not r.get("kind")]
    seed_era = sum(1 for r in rows if row_date(r) and row_date(r) <= SEED_CUTOFF)
    seed_era_links = sum(1 for r in link_rows if row_date(r) and row_date(r) <= SEED_CUTOFF)
    idx = json.loads(CORPUS_INDEX.read_text(encoding="utf-8"))
    doms = domain_counts(rows)  # domain pass over all rows incl events (seed did not split)
    doms_links_only = domain_counts(link_rows)

    # named cluster checks the gap rows depend on
    def hay(r):
        return (str(r.get("canonical") or "") + " " + str(r.get("title") or "") + " " + str(r.get("note") or "")).lower()

    a2a = [r for r in rows if any(k in hay(r) for k in ["a2a", "agent2agent", "agent-to-agent"])]
    autogen = [r for r in rows if "autogen" in hay(r)]
    camel = [r for r in rows if "camel" in hay(r)]
    xidig_swarm = [str(r.get("id")) for r in rows if str(r.get("id") or "").startswith("XIDIG-SWARM")]
    xidig_win = [str(r.get("id")) for r in rows if str(r.get("id") or "").startswith("XIDIG-WIN")]
    qlora = [r for r in rows if "qlora" in hay(r)]

    return {
        "links_lines": len(rows),
        "links_bad_lines": bad,
        "event_kind_rows_in_links": len(event_rows),
        "link_rows_no_kind": len(link_rows),
        "rows_on_or_before_seed_date": seed_era,
        "link_rows_on_or_before_seed_date": seed_era_links,
        "rows_after_seed_date": len(rows) - seed_era,
        "packs_indexed": idx.get("count"),
        "domain_pass_seed_era_vs_current": doms,
        "domain_pass_links_only_current": {k: v["current"] for k, v in doms_links_only.items()},
        "a2a_rows": len(a2a),
        "a2a_examples": [str(r.get("id") or r.get("canonical"))[:90] for r in a2a[:5]],
        "autogen_rows": len(autogen),
        "camel_rows": len(camel),
        "xidig_swarm_ids": xidig_swarm,
        "xidig_win_ids": xidig_win,
        "qlora_rows": len(qlora),
    }


def main():
    out = {"generated": "2026-09-26", "lane": "B2-78", "seed_cutoff": SEED_CUTOFF,
           "union": recount_union(), "links": recount_links()}
    OUT.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
