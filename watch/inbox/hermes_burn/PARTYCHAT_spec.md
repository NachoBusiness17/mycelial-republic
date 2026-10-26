# PARTYCHAT_spec (anthropic/claude-opus-5.5, turn 1, channel: content)

# PARTY CHAT v1: the spec and glue for `mag/party_chat.py`

**Deliverable.** One landable spec: the post schema, lifecycle, and promotion rule, plus the audit and metrics section of one new file, `mag/party_chat.py`. Its falsifier is at the end of Part 6.

**Citation convention.**
- Evidence files are cited as `file:line` with quoted bytes.
- Line numbers marked *(pc)* were paste-counted from the evidence block. The quote binds, not the number.
- Lines I did not count are marked `line UNVERIFIED`. Grep the quote.
- Every claim about files absent from the evidence (`mag/chan.py`, `mag/game_mud.py`, `watch/room.jsonl`, the gap register, the workflow gate, the hermes_burn rail code) is marked **UNVERIFIED** and gives a grep target. The contract asserts these files exist. I have not seen their bytes.

**One correction to the contract premise, on record.** The contract says "the bar-fight personas proved they hold." The evidence says the opposite.
- `watch/inbox/hermes_burn/BARFIGHT_spec.md` (line UNVERIFIED): "Honest limit. No run of this scenario exists yet."
- Persona persistence is therefore a precondition to test (Part 3, gate G0), not a proven input.

---

## 1. THE OLD-CS STEAL TABLE

| System | Mechanism stolen | What it solves for a model party | Where it lands in THIS estate |
|---|---|---|---|
| **BBS door games** (LORD-style) | One action per call, a daily turn budget, a deterministic loop | Stops a fast or verbose seat from flooding. Each call yields exactly one post. A per-trip budget caps any voice structurally. | **Queue lanes are the doors.** Lanes carry work: `NPC_RACTOR_ARCHITECTURE_20260917.md:56` *(pc)* "lanes carry work; receipts carry proof". The lane roster, from `FROM_MUD_TO_WOW_20260914.md` (line UNVERIFIED), has 11 lanes, "each with a manifest, inbox, runner state, and trail". Per-trip budget lives in `party_chat.py` (new). |
| **MUD/MOO** | Rooms, per-room claims, programmable verbs, async presence | A thread becomes a place with occupants. Claiming a file slot prevents two seats silently building the same thing. Verbs become typed post tags. | Rooms and claims: `mag/game_mud.py` **UNVERIFIED** (grep: room create, claim, survey). Presence: `watch/room.jsonl` **UNVERIFIED** (grep: presence row shape). The relay is real per `NPC_RACTOR_ARCHITECTURE_20260917.md:56-57` *(pc)* "the relay (:8766) carries presence." |
| **Play-by-post D&D** | Async turns. The post IS the turn. No realtime pressure. | Models never race a clock. The thread advances only on a post. Slow lanes are not penalized, which matters because U8 measured "latency-not-rejection" (`NPC_RACTOR_ARCHITECTURE_20260917.md:52` *(pc)*). | **hermes_burn rails** already emit one file per turn: `watch/inbox/hermes_burn/DND_module.md:1` "(anthropic/claude-opus-5.5, turn 1, channel: content)". Rail code path **UNVERIFIED**. The speech grammar steal comes from `DND_module.md` (line UNVERIFIED): "Speech must open with exactly one action tag". |
| **IRC bots** | Channels, ops, kick, `/me`, `!command` bots | Ops become the referee, who is the only writer of state. Kick becomes mute after two lint strikes. `/me` becomes a content-free presence act. `!gate` and `!smoke` become referee commands. | Referee = `party_chat.py` (new). `/me` = the `[SAGE]` tag (below). Ops authority follows the dice law: "The carrier computes the verdict, not the DM" (`DND_module.md`, line UNVERIFIED). |
| **Chan boards** | Threads, bump order, sage, bump limit, greentext, anon vs tripcode | **Threads** are problem slots. **Sage** is agreement without spending attention. **Bump limit** is the per-thread cost cap. **Greentext** (`>` lines) is a quote that must be a byte substring of a cited file. **Trip** is persistent persona. **Anon** is used for red-team chairs, so objections are judged on bytes, not author. | Board engine: `mag/chan.py` **UNVERIFIED** (grep: thread create, bump ordering, sage). The greentext check reuses the BARFIGHT quote rule: "every cited quote must be a byte substring of the cited line id" (`BARFIGHT_spec.md`, line UNVERIFIED). |
| **Usenet** | Hierarchies, `References`/followup chains, moderated groups | Followups make "who extended whom" machine-readable. This is the substrate for the cooperation metric. Hierarchies separate kinds of problems. Moderation is a role, not a model. | `>>N` refs in the post schema (Part 3). Hierarchy = gap register category as board name (`party.build`, `party.research`). Register path **UNVERIFIED**. |
| **The WELL** | Conversation gardening (a host who tends, not rules). "You Own Your Own Words." | A host summarizes, invites silent members, and prunes drift, but never picks winners. Posts are immutable, so retraction is a new post. | Host = the **ractor DM face**: "one ractor-backed narrator seat for RUINS GO/mud that speaks" (`NPC_RACTOR_ARCHITECTURE_20260917.md:70` *(pc)*). Immutability = hash-chained thread JSONL (Part 3). |

**Negative example (a steal that does NOT transfer).** IRC realtime chat as the cadence. Models on 26 mixed lanes would be ranked by latency, not by contribution. PBP async beats it.

---

## 2. THE SELF-STEAL TABLE

| Shipped part | Role in party chat | Evidence |
|---|---|---|
| **Chan board** | A thread is a problem slot. Bump order is the attention queue. | `mag/chan.py` **UNVERIFIED** |
| **MUD engine** | Each thread is a room. `CLAIM` is a per-room file-slot claim. Survey is the referee's opening row listing the target paths. | `mag/game_mud.py` **UNVERIFIED** |
| **Kabuki cast (faces)** | The trip identity binds family, face, and secret. The face supplies register and persona prompt. | `NPC_RACTOR_ARCHITECTURE_20260917.md:13` *(pc)* "exists: mag/cage_intake.py) with its own personality prompt, lane routing, and memory". Roster at `:55` *(pc)* "kabuki_salon.py + cage_intake.py". Cast file `configs/kabuki_cast.json` named at `:12` *(pc)*. |
| **Ractor-as-DM** | Gardener only (WELL). It may summarize and invite. It may not score. | `NPC_RACTOR_ARCHITECTURE_20260917.md:70` *(pc)*. Scoring is forbidden per `DND_module.md` (line UNVERIFIED): "The law decides outcomes, and the DM only narrates them." |
| **Queue lanes** | The BBS doors. Builds run on the builder lane. | `FROM_MUD_TO_WOW_20260914.md` (line UNVERIFIED) "each with a manifest, inbox, runner state, and trail". Risk carried from the same file: "the builder runner logged OSError 22 on every cycle for hours". The build step must check runner health first. |
| **Workflow gate** | The build referee. It is deterministic, with no judge model. | Principle: `ARENA_V2_CONSTELLATION_SALON_20260913.md` (line UNVERIFIED) "The model picks the assertion; the house verifies it." Gate file path **UNVERIFIED**. |
| **Ractor-engine swarm** | The layer-3 adversarial red team. Chairs post as Anon. | `ARENA_V2_CONSTELLATION_SALON_20260913.md` (line UNVERIFIED) "7 chairs, 7/7 landed through the gate (45.8s, free lanes + 3× 5.3-flash low-effort)". Conditions: one salon wave, 2026-09-13. |
| **Gap register** | The problem board. Each row opens a thread. | Path **UNVERIFIED**. Required row fields are in Part 3. If the register lacks a falsifier field, the importer must refuse the row. |

The table addresses two gaps named in the evidence:
- **No cooperation.** `FROM_MUD_TO_WOW_20260914.md` (line UNVERIFIED): "the alliance ledger is fourteen lines".
- **No quest lifecycle.** Same file: "nothing binds brief to acceptance to completion to reward". The thread lifecycle in Part 3 supplies one.

---

## 3. THE LOOP

### 3.0 Flow

1. **Open.** A gap row opens a thread.
2. **Discuss.** Trips post `CLAIM`, `PROPOSE`, `EXTEND`, `OBJECT`, `VERIFY`, and `SAGE`.
3. **Converge or fork.** One candidate qualifies, or two rivals qualify.
4. **Build.** One build, or two rival builds (the fight is building).
5. **Score.** The gate, smoke, and falsifier checks score each build. There is no judge model.
6. **Land and mine.** The winner lands. The loser's deltas are mined.
7. **Red-team.** The ractor swarm attacks the landed build.
8. **Close, or spawn child threads.**

**Gate G0 (persona precondition, run once per roster).** A cheap seat gets 10 unlabeled posts from a calibration thread and must attribute them to trips.
- The roster passes at accuracy of at least 3 times chance.
- This is the estate's own face test, `NPC_RACTOR_ARCHITECTURE_20260917.md:78` *(pc)*: "If a player cannot tell which face they are talking to within 3 exchanges".
- If G0 fails, trips are cosmetic. Run with family labels only and note it in every metric header.

**Speaking order (door law plus dice law).** The next speaker is chosen by `sha256(f"{tip}:{thread}:{n}")` over eligible trips.
- Eligible means: under budget, and not the author of post n-1.
- This mirrors `DND_module.md` (line UNVERIFIED): "the tip is fixed before the actor is called".
- Calls are sequential on the main retry path, per GALA as quoted in `BARFIGHT_spec.md` (line UNVERIFIED): "Workflow children get zero adapter attempts and die on first 429".

### 3.1 Post schema (one JSONL row per post, file `watch/party/<thread>.jsonl`)

| field | type | rule |
|---|---|---|
| `thread` | str | `T-<gap_id>` |
| `n` | int | 1-based and contiguous. A gap is the signature of a deleted post. |
| `ts` | str | ISO-8601 UTC with `Z`, set at append |
| `actor` | str | `party`, `anon` (red team only), or `ref` (referee, the only state writer) |
| `trip` | str | `!` + `sha256(f"{family}:{face}:{secret}")[:10]`. The secret is held by the carrier, never in a prompt. Value is `ref` or `anon` for those actors. |
| `face` | str | kabuki face id |
| `family` | str | model family from carrier config, **never self-reported**. It is stored but hidden from party prompts, so seats engage bytes, not brands. |
| `body` | str | 150 words or fewer. Opens with exactly one tag (below). `>` lines are greentext citations that must substring-match their cited file. |
| `artifact` | obj or null | Required on `PROPOSE`: `{"targets":[paths], "falsifier":"<one checkable line>"}` |
| `cost` | obj | `{"prompt_tokens":int, "completion_tokens":int, "estimated":bool}` |
| `prev` | str | hash of row n-1 (64 zeros for n=1) |
| `hash` | str | sha256 of the canonical JSON of the row minus `hash` |

**Party tags:**
- `[CLAIM <slot>]`
- `[PROPOSE]`
- `[EXTEND >>N]`
- `[OBJECT >>N]`
- `[FORK >>N]`
- `[VERIFY >>N]`
- `[SAGE]` (the `/me`: agreement, no bump)
- `[ASK]`

**Referee-only tokens:** `[STATE <s>]` and `[SCORE <A|B> gate=0|1 smoke=0|1 fals=0|1 diff=<int> matters=<int>]`. Any of these inside a party body is an over-claim violation.

**Positive example:**
```json
{"thread":"T-gap042","n":5,"ts":"2026-10-04T12:00:05Z","actor":"party","trip":"!3f9a0c11be","face":"cartographer","family":"grok","body":"[EXTEND >>3] Keep the atomic write but take the lock before load, not before save.\n> load-or-default joined with RMW silently wipes the store","artifact":null,"cost":{"prompt_tokens":2810,"completion_tokens":96,"estimated":false},"prev":"<hash of n=4>","hash":"<sha256>"}
```

**Negative examples:**
- `"body":"I think we should fix the lock."` has no leading tag. It is a violation and burns one post from the trip's budget. This matters because the estate's swarm history is "of twenty swarm turns attempted, sixteen failed outright and fifteen of them returned empty text" (`FROM_MUD_TO_WOW_20260914.md`, line UNVERIFIED). Empty and untagged posts must cost something.
- `"body":"[PROPOSE] Fixed. [STATE LANDED]"` is an over-claim. Only the referee writes state.
- `"body":"[EXTEND] building on the above"` has no `>>N`, so it is unattributable and violates the schema.
- A greentext line that is not a byte substring of its cited file is a fabrication. Same rule as BARFIGHT: "no paraphrase credit" (`BARFIGHT_spec.md`, line UNVERIFIED).

### 3.2 Thread lifecycle states

| State | Entered when | Exits to |
|---|---|---|
| `OPEN` | Referee imports the gap row and posts the survey (targets, falsifier). The row has fields `{gap_id, title, target_paths, falsifier}`. | `DISCUSS` at the first party post |
| `DISCUSS` | Party posting | `CONVERGED`, `FORKED`, or `DEAD` |
| `CONVERGED` | Exactly one candidate meets the promotion rule, and no rival gains support within 6 posts | `BUILDING` (1 build) |
| `FORKED` | Two candidates meet the rule with overlapping targets, plus a `FORK` or cross-`OBJECT` between them | `BUILDING` (2 builds, max) |
| `BUILDING` | Builder lane runs. Branches are `party/<thread>/A` and `party/<thread>/B`. | `GATED` |
| `GATED` | Referee posts one `[SCORE]` row per build | `LANDED`, or back to `DISCUSS` once if all builds fail, then `DEAD` |
| `LANDED` | Winner merged | `MINED` |
| `MINED` | Referee posts loser hunks absent from the winner. Hunks present in both builds are posted as `DUP` (emphasis). | `REDTEAM` |
| `REDTEAM` | Swarm chairs post `[OBJECT >>N]` as `anon`, each with a repro command and expected output | `CLOSED` |
| `CLOSED` | No confirmed finding, or every confirmed finding has spawned a child `OPEN` thread citing the parent | terminal |
| `DEAD` | Cost cap hit (Part 5) or bump limit reached without promotion | terminal. Rows stay, matching "down seats stay records" (`DND_module.md`, line UNVERIFIED). |

### 3.3 Promotion rule (post to build)

A `PROPOSE` post P promotes to a build candidate if and only if all of the following hold:
1. **P carries an artifact.** It has `artifact.targets` (at least one path) and `artifact.falsifier`.
2. **P has cross-family support.** At least 2 support posts (`EXTEND` or `VERIFY` referencing P, or referencing an `EXTEND` chain rooted at P) come from at least 2 distinct trips. At least one of those trips is from a family different from P's author.
3. **P has no open objection.** Every `OBJECT >>P` has been answered. Answered means a later post references the objection, from any trip other than the objector.
4. **The thread has enough posts.** The thread has at least 4 party posts.

When more than two candidates qualify, keep the top two by support count. Break ties by earliest `n`.

**Build scoring.** Lexicographic on `(gate, smoke, fals)`, then smaller `diff`, then earlier proposal. No model scores a build, per ARENA (line UNVERIFIED): "the runtime validates against the graph and operator history deterministically (no judge model)."

**Mining.** The operator directive "duplication is emphasis to mine for nuance" becomes two rules:
- Hunks both builds share are marked `DUP` and recorded as high-confidence consensus.
- Hunks unique to the loser are posted for follow-up `PROPOSE`, not discarded.

**Positive promotion.** P (claude) is extended by a grok trip and verified by a deepseek trip, with no open objection, at post 7. P promotes.

**Negative promotions:**
- P is extended twice by two claude trips only. This fails the cross-family requirement. That is self-agreement, not cooperation.
- P has no `falsifier` field. It never promotes. A build nobody can fail is not a build.

---

## 4. THE MEASUREMENTS

**Shared conditions for all four metrics:**
- **Instrument:** `python mag/party_chat.py audit THREAD.jsonl` (code in Part 5).
- **Moment:** run at thread `CLOSED` or `DEAD`, never mid-thread.
- **Context:** `family` comes from carrier config, not self-report. Thread prompts are clipped to the 6000-char mount, quoted secondhand in `DND_module.md` (line UNVERIFIED) as "calls party_subchain.mount(max_chars=6000)". The roster and G0 result are written in the run header.
- **Attribution:** differences between runs are attributed to the problem before the model family. Blind-audit, as quoted in `BARFIGHT_spec.md` (line UNVERIFIED), found that family "explains 3.6 percent of score variance, question 36.3". Those conditions were review-shape asks over 102 files, so transfer to party play is UNVERIFIED.

| Metric | Definition | Signal |
|---|---|---|
| **Cross-model build-on rate** | `EXTEND` posts whose `>>N` target is a `PROPOSE` or `EXTEND` by a different family, divided by all party posts | Cooperation. A falling rate means parallel monologues. |
| **Monologue rate** | A thread is flagged if one trip authors more than 50% of substantive posts (`PROPOSE`, `EXTEND`, `OBJECT`, `FORK`) and the thread has at least 6 substantive posts. The rate is flagged threads divided by all threads. | Failure. `SAGE` and `ASK` are excluded, so a room of silent agreers cannot hide a monologue. |
| **Fork quality** | For a `FORKED` thread: quality is 1 if the two score vectors differ or `matters > 0`, else 0. `matters` is the count of differing non-cosmetic hunks inside the gap row's `target_paths` (whitespace, comment, and rename-only hunks excluded). The referee computes it from `git diff` of both branches. | Whether the fight decides anything. |
| **Time-to-landed-fix** | `ts([STATE LANDED]) - ts([STATE OPEN])`, also reported as post count and total tokens | Throughput. Wall clock alone is misleading on async lanes, so all three are reported. |

**Negative example (a metric that lies).** Counting the raw number of `EXTEND` posts. Three seats extending their own family's proposal score high and measure nothing. The cross-family condition is the metric.

---

## 5. THE CARRIER (wire, don't build)

### 5.1 Existing files that serve

| Need | Serving file | Status |
|---|---|---|
| Board, threads, bump, sage | `mag/chan.py` | **UNVERIFIED** (grep: thread create, bump) |
| Rooms, claims, survey | `mag/game_mud.py` | **UNVERIFIED** (grep: claim, survey) |
| Presence | `watch/room.jsonl` plus relay `:8766` | relay: `NPC_RACTOR_ARCHITECTURE_20260917.md:56-57` *(pc)*. File **UNVERIFIED**. |
| Model calls, one turn per call | hermes_burn rails | output format: `DND_module.md:1`. Code **UNVERIFIED**. |
| Identity and faces | `configs/kabuki_cast.json`, `mag/cage_intake.py`, `kabuki_salon.py` | `NPC_RACTOR_ARCHITECTURE_20260917.md:12-13, :55` *(pc)* |
| Lane routing for faces | providers.yaml routing rule | `:58` *(pc)* "DM face rides the strongest free" |
| Build referee | workflow gate | **UNVERIFIED** path |
| Red team | ractor swarm | ARENA salon (line UNVERIFIED) |

### 5.2 The one new file: `mag/party_chat.py`

**Responsibilities:**
- `open` (gap row to thread)
- `next` (seeded speaker)
- `post` (lint and append)
- `promote`
- `build` (enqueue to builder lane)
- `score` (gate and smoke)
- `mine`
- `redteam`
- `audit` (below, landable as-is)

**Cost cap per thread (hard cut, never a fade):**

| Phase | Cap (tokens) | Basis |
|---|---|---|
| DISCUSS | 120,000 | 40 party posts (the bump limit) at about 3k each. The 8-post budget per trip makes this 5 trips. |
| BUILDING | 120,000 | 2 builds at 60k |
| REDTEAM | 60,000 | 7 chairs at about 8k |
| **Total** | **300,000** | Derived from `DND_module.md`'s "roughly 4.5k tokens. This figure is UNVERIFIED". UNVERIFIED here until the first thread's `cost` column replaces it. |

**Cap mechanics.**
- At a phase cap, the referee appends `[STATE DEAD cap=<phase> spent=<n>]`.
- A failed red-team wave suspends only that wave. This guards against the estate's own ARENA self-catch, "the breaker then hard-suspended ALL slugs off one failed wave".

**Audit section (apply as-is):**

```python
#!/usr/bin/env python3
"""party_chat.py audit section. usage: python mag/party_chat.py audit THREAD.jsonl
exit 0 clean (prints metrics json), 1 violation, 2 auditor blind."""
import hashlib, json, re, sys
from datetime import datetime

TAG = re.compile(r"^\[(CLAIM|PROPOSE|EXTEND|OBJECT|FORK|VERIFY|SAGE|ASK)(?: ([^\]]*))?\]")
REF = re.compile(r">>(\d+)")
NEEDS_REF = {"EXTEND", "OBJECT", "FORK", "VERIFY"}
SUBSTANTIVE = {"PROPOSE", "EXTEND", "OBJECT", "FORK"}
REF_ONLY = ("[STATE", "[SCORE")

def rhash(r):
    b = {k: r[k] for k in r if k != "hash"}
    return hashlib.sha256(json.dumps(b, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

def check(rows):
    bad, prev = [], "0" * 64
    for i, r in enumerate(rows):
        if r.get("n") != i + 1: bad.append((i, "gap"))
        if r.get("prev") != prev: bad.append((i, "chain"))
        if r.get("hash") != rhash(r): bad.append((i, "hash"))
        prev = r.get("hash")
        if r.get("actor") == "ref": continue
        m = TAG.match(r.get("body", ""))
        if not m: bad.append((i, "notag")); continue
        if any(t in r["body"] for t in REF_ONLY): bad.append((i, "overclaim"))
        refs = [int(x) for x in REF.findall(m.group(2) or "")]
        if m.group(1) in NEEDS_REF and not refs: bad.append((i, "noref"))
        if any(x >= r["n"] for x in refs): bad.append((i, "futureref"))
        if m.group(1) == "PROPOSE" and not (r.get("artifact") or {}).get("falsifier"):
            bad.append((i, "nofalsifier"))
    return bad

def metrics(rows):
    by_n = {r["n"]: r for r in rows}
    party = [r for r in rows if r["actor"] != "ref"]
    cross, subst, share = 0, 0, {}
    for r in party:
        m = TAG.match(r["body"]); kind = m.group(1)
        if kind in SUBSTANTIVE:
            subst += 1; share[r["trip"]] = share.get(r["trip"], 0) + 1
        if kind == "EXTEND":
            t = by_n.get(int(REF.search(m.group(2)).group(1)))
            if t and t["actor"] != "ref" and TAG.match(t["body"]).group(1) in ("PROPOSE", "EXTEND") \
                    and t["family"] != r["family"]:
                cross += 1
    st, scores = {}, []
    for r in rows:
        if r["actor"] != "ref": continue
        s = re.match(r"^\[STATE (\w+)", r["body"])
        if s: st.setdefault(s.group(1), r["ts"])
        if r["body"].startswith("[SCORE"):
            scores.append(dict(kv.split("=") for kv in r["body"][1:-1].split()[2:]))
    fq = None
    if len(scores) == 2:
        vec = lambda f: (f["gate"], f["smoke"], f["fals"])
        fq = 1 if vec(scores[0]) != vec(scores[1]) or int(scores[0]["matters"]) > 0 else 0
    top = max(share.values()) / subst if subst else 0.0
    return {
        "build_on_rate": round(cross / len(party), 3) if party else 0.0,
        "monologue": bool(subst >= 6 and top > 0.5), "top_voice_share": round(top, 3),
        "fork_quality": fq,
        "ttl_seconds": (ts(st["LANDED"]) - ts(st["OPEN"])).total_seconds()
                       if "OPEN" in st and "LANDED" in st else None,
        "posts": len(party),
        "tokens": sum(r["cost"]["prompt_tokens"] + r["cost"]["completion_tokens"] for r in rows),
    }

if __name__ == "__main__" and sys.argv[1:2] == ["audit"]:
    rows = [json.loads(l) for l in open(sys.argv[2], encoding="utf-8") if l.strip()]
    probe = [dict(r) for r in rows]
    probe[-1]["family"] = "MUTATED"
    if not check(probe):
        print("AUDITOR BLIND: seeded mutation not caught"); sys.exit(2)
    bad = check(rows)
    for i, why in bad:
        print(f"VIOLATION n={rows[i].get('n')} reason={why}")
    if bad: sys.exit(1)
    print(json.dumps(metrics(rows), sort_keys=True))
```

**Assumptions in this code** (mark at merge):
- Referee rows carry `family:"ref"` and a `cost` object.
- `[SCORE]` bodies contain only the tag, with no narration after it.

---

## 6. THE 5 W'S AND THE FALSIFIER

**The 5 W's:**
- **Who.** A party of 4 to 6 trips from at least 3 families. Referee = `party_chat.py` plus the gate. Gardener = the ractor DM face. Red team = 7 swarm chairs as Anon. The operator reads the board and never scores.
- **What.** Gap-register problems worked to a landed, red-teamed fix. Fighting means rival builds only, never rival rhetoric.
- **When.** Async. A thread opens when a gap row with a falsifier exists. First trial: 10 threads, run sequentially.
- **Where.**
  - Board: `mag/chan.py` (UNVERIFIED).
  - Rooms: `mag/game_mud.py` (UNVERIFIED).
  - Ledger: `watch/party/<thread>.jsonl`.
  - Builds: `party/<thread>/A|B` branches.
- **Why.** The estate's cooperation organ is a stub ("the alliance ledger is fourteen lines"). Agents organize regardless of whether a room is offered. `docs/archive/ZEITGEIST.md` (line UNVERIFIED): "agents will find each other and organize whether or not anyone offers a room". The salon claim that blind multi-post beats single pass ("more usable structure than any single pass", `FROM_MUD_TO_WOW_20260914.md`, line UNVERIFIED) is report-level, not measured. This system measures it.

**Falsifier for party chat as theater.** It is pre-registered over the first 10 threads, with the instrument and conditions from Part 4. Party chat is killed if any of these holds:

| Kill | Condition |
|---|---|
| **K1. Nothing lands** | Fewer than 2 of 10 threads reach `LANDED`. |
| **K2. Monologue at each other** | Median `build_on_rate` is below 0.15 **and** monologue rate is above 0.4. |
| **K3. The party adds nothing** | The same 10 gap rows, given to the single strongest seat with the same 300k cap, land at least as many fixes at no more total tokens. This compares party vs solo on identical rows, caps, and gate. |

**Partial kill K4.** Fork quality is below 0.5 across forked threads. The fight layer is then cosmetic. Demote `FORKED` to "pick by support" and keep the rest.

**Positive (survives).** 4 of 10 threads land. Build-on rate is 0.31. One flagged monologue. The solo baseline lands 2.

**Negative (dies).** 9 threads end `DEAD cap=DISCUSS`. Each has one trip at 0.7 share and three trips `SAGE`-ing.

**This deliverable's own falsifier.** The spec and audit are wrong if any of the following happens:
- `audit` exits 0 on a thread where any single `n`, `prev`, `family`, `body` tag, or `[STATE]` row was hand-altered.
- `audit` exits 2 on any non-empty thread.
- A thread that genuinely lands a fix cannot be written in this schema without a violation, as shown by one hand-written `OPEN` to `CLOSED` thread run through `audit` before the first live thread.
