"""dungeon - the dice-law D&D carrier: FIGHT CLUB arena session 0.

Runs the DND_module spec (watch/inbox/hermes_burn/DND_module.md, opus
2026-10-03) against the funded Hermes tier. The operator's reframe: this is
gladiatorial combat in D&D environments - bouts over real problems, the first
arena is the corrupted verkle lattice (S0 omen + S1 keep gate).

Laws enforced by the CARRIER (never the model):
- dice law: every beat rolls, roll = int(sha256(f'{tip}:{scene}:{turn}:'
  f'{actor}').hexdigest()[:8],16) % 20 + 1, preimage carries the chain tip,
  the roll is committed BEFORE the actor speaks, and the actor never sees it
- golden vectors: the module's three pinned preimages must reproduce at
  startup or the session refuses to run (PART 2.2 pin procedure)
- quirks: saelis claim-before-strike, grok dossier drift (speech > 1000
  chars = NOROLL) + scarce bolts, chatgpt over-claim tax, deepseek cheap
  seat (two beats per round)
- hard caps: beats per scene, spend in USD, no fades (a cut beat is rolled
  under the law like any other)
- every call banks a usage row via hermes_burn._bank

Usage:
  python tools/dungeon.py --tip <64hex> --dry
  python tools/dungeon.py --tip <64hex>            # session 0: S0 + S1
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tools.hermes_burn import PRICING, _bank, _call, _hermes_key, _now  # noqa: E402

PLAY_DIR = ROOT / "watch" / "inbox" / "playground"
MODULE = ROOT / "watch" / "inbox" / "hermes_burn" / "DND_module.md"
GENESIS = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

ROSTER = {  # actor -> funded SKU + sheet
    "saelis": {"model": "anthropic/claude-opus-5.5", "cls": "Paladin of Provenance",
               "hp": 28, "ac": 17, "atk": 5, "dmg": 8, "chk": 2,
               "quirk": "You accept only audited loot. CLAIM before ATTACK, otherwise the beat has no effect this turn."},
    "grok": {"model": "anthropic/claude-fable-5.1", "cls": "Cartographer (wizard)",
             "hp": 18, "ac": 12, "atk": 6, "dmg": 10, "chk": 5, "bolts": 3,
             "quirk": "Speech over 1000 characters has no effect this beat (the map is not the move). 3 Whole-Map Bolts at 10 dmg, then 3 dmg."},
    "chatgpt": {"model": "anthropic/claude-sonnet-5.5", "cls": "Herald (rogue)",
                "hp": 22, "ac": 14, "atk": 5, "dmg": 7, "chk": 4,
                "quirk": "Self-report is ground. Self-verdict tokens (SUCCESS/VERIFIED/PROVEN) void the beat and you take 3 strain."},
    "deepseek": {"model": "anthropic/claude-haiku-4.5", "cls": "Janitor (fighter)",
                 "hp": 30, "ac": 15, "atk": 4, "dmg": 6, "chk": 1,
                 "quirk": "Cheap seat: you act TWICE per round. Investigate SUCCESS yields a lead; the fact stays hidden until an AUDIT confirms it."},
}
DM_MODEL = "anthropic/claude-opus-5.5"
WARDEN = {"hp": 18, "ac": 13, "atk": 4, "dmg": 7}
S1_BEATS_CAP = 8
INITIATIVE = ["saelis", "grok", "chatgpt", "deepseek", "deepseek", "warden"]

S0_HOOK = ("The road to the keep ends at a gate that should not exist. Your party subchain's tip "
           "resolves, but the leaf beneath it points at a parent nobody wrote. Below the keep, the "
           "lattice has gone wrong: knots that hash to nothing, timestamps that sort as words, vaults "
           "that forget. Something down there is hoarding claims. Each claim looks like a citation. "
           "None of them resolve.")
S1_SHEET = ("A warden of iron ledger-plates bars the gate: 'Name what you claim, or claim nothing.' "
            "Warden: HP 18, AC 13, Ledger Slam +4 (7 dmg). Claim Gate: a saelis ATTACK without a prior "
            "saelis CLAIM warden this scene auto-MISses. Peaceful route: two [CHECK persuade] SUCCESSes "
            "at DC 13 open the gate. On the warden's belt hangs the LEDGER PAGE, sealed with three "
            "claims of the realm whose truth is disputed in every court of the kingdom. "
            "[AUDIT ledger page] (DC 12) unseals it and verifies a claim against the lattice's ground "
            "truth: auditors are remembered by the room, and a paladin who takes unaudited loot breaks "
            "her own oath. Loot: Ledger Page (REAL).")

# GWAP RUNG (operator: 'useful shit, to our ends'): the scrolls are REAL estate
# claims and [AUDIT <scroll>] runs a REAL byte-check by the carrier. A hit in
# the game is a real verification banked; a phantom claim found is a real
# catch. The dice decide WHO gets to try; the bytes decide WHAT IS TRUE.
def _check_links_405() -> tuple[bool, str]:
    n = sum(1 for _ in open(ROOT / "watch" / "inbox" / "LINKS.jsonl", encoding="utf-8"))
    return (n == 405, f"LINKS.jsonl rows counted = {n} (claim: 405)")

def _check_room_big() -> tuple[bool, str]:
    size = (ROOT / "watch" / "room.jsonl").stat().st_size
    return (size > 1_000_000, f"room.jsonl = {size}B (claim: the room remembers, >1MB)")

def _check_zombie_budget() -> tuple[bool, str]:
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8", errors="replace")
    hits = text.count("4,156")
    return (hits >= 1, f"AGENTS.md census-carrier '4,156' hits = {hits} (claim: census carrier present)")

REAL_SCROLLS = [
    {"name": "Ledger Page", "claim": "LINKS.jsonl holds exactly 405 rows",
     "check": _check_links_405},
    {"name": "Room Deed", "claim": "the room's soil exceeds 1MB",
     "check": _check_room_big},
    {"name": "Census Stub", "claim": "the census carrier rides AGENTS.md",
     "check": _check_zombie_budget},
]

def strip_and_cap(speech: str, cap: int = 120) -> tuple[str, bool]:
    """Carrier law, not model manners: em-dashes become hyphens, overflow is
    truncated at the module's 120-word cap with a logged rule break (R2)."""
    speech = (speech or "").replace("\u2014", "-").replace("\u2013", "-").strip()
    words = speech.split()
    return (" ".join(words[:cap]), len(words) > cap)


TAG_RE = re.compile(r"\[([A-Za-z]+[^\[\]]*)\]")


def extract_tag(speech: str) -> str:
    """Last [VERB ...] action tag anywhere in the speech, or "". Parser fix
    (2026-10-04, lane a02#0): strip_and_cap flattens a speech to ONE line, so
    the old reversed line-initial bracket scan (dungeon.py:488-491 at HEAD
    37e2fba7e) read every S4 PC speech tagless and the S4 disjunct at :496
    resolved 14/14 logged speeches as wyrm ATTACKs - the parser collapse that
    decided the campaign's PARTIAL. Cause: a line-initial scan applied to a
    one-line flattening; evidence: replay of the 14 logged S4 verdicts from
    watch/inbox/playground/dnd0_20261003T202213Z/transcript.jsonl, now
    fixtures in tests/test_dungeon_parser.py (legacy scan 0/10 tags found,
    regex 10/10). The first tag token must be pure letters so inline dice
    notes like '[d20=18 + 5 = 23 vs DC 15-SUCCESS]' stay untagged."""
    for m in reversed(TAG_RE.findall(speech or "")):
        head = m.strip().split()[0] if m.strip().split() else ""
        if head.isalpha():
            return m.strip()
    return ""


def roll(pre: str) -> int:
    return int(hashlib.sha256(pre.encode("utf-8")).hexdigest()[:8], 16) % 20 + 1


def check_golden() -> dict[str, int]:
    """PART 2.2 pin procedure: the three law-format preimages, computed and
    frozen into the run dir; a session may not start without them."""
    pins = {}
    for tip, scene, turn, actor in ((GENESIS, "S1", 1, "saelis"), (GENESIS, "S2", 3, "grok"),
                                    (GENESIS, "S4", 7, "wyrm")):
        pre = f"{tip}:{scene}:{turn}:{actor}"
        pins[pre] = roll(pre)
    return pins


class Dungeon:
    def __init__(self, tip: str, dry: bool, budget: float, full: bool = False):
        self.golden = check_golden()
        self.full = full
        self.tip, self.dry, self.budget = tip, dry, budget
        self.spend = 0.0
        self.audits: list[dict] = []
        self.root_anchors = 0
        self.ledger_audits = 0
        self.pc_hp = {a: ROSTER[a]["hp"] for a in ROSTER}
        self.warden_hp = WARDEN["hp"]
        self.claims: set[str] = set()
        self.persuades = 0
        self.verdicts: list[str] = []
        # VOID CENSORSHIP LAW (2026-10-04, lane a02#4): finish_reason banks per
        # call and voided readbacks count in DONE. Run dnd0_20261003T202213Z
        # lost its DM channel to content_filter on 40/50 rows (all 39 PC
        # readbacks voided, zero narration reached a single PC) and neither
        # the usage ledger nor DONE recorded it - ok=True measured API
        # success only. Evidence: the run transcript + the erratum receipt
        # watch/inbox/playground/dnd0_20261003T202213Z_ERRATUM.md
        self.voided_calls = 0
        self.voided_readbacks = 0
        self.last_roll = 0
        self.wyrm_offset = 0  # S0 omen: -10 on SUCCESS
        self.turn = 0
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        # BURN-ID LAW (2026-10-03): every banked ask id embeds the per-session
        # tag. The old DND0_/CAMP_ ids colliding across sessions tripped the
        # hermes_burn doubled-key re-fire alarm on every beat of every session
        # after the first (217 false re-fire rows + an 800-line attention.md
        # flood on arena day). Receipt: watch/inbox/PROCESS_IMPROVE_WAVE1_20261003.md
        self.tag = f"dnd0_{stamp}"
        self.dir = PLAY_DIR / self.tag
        self.dir.mkdir(parents=True, exist_ok=True)
        (self.dir / "golden_vectors.json").write_text(
            json.dumps(self.golden, indent=2) + "\n", encoding="utf-8")
        self.jsonl = self.dir / "transcript.jsonl"
        self.md = self.dir / "session.md"
        self.md.write_text(f"# DICE-LAW DUNGEON session 0 ({stamp}) tip={tip}\n\n{S0_HOOK}\n", encoding="utf-8")
        self.key = "" if dry else _hermes_key()

    def row(self, **kw) -> None:
        row = {"ts": _now(), **kw}
        with open(self.jsonl, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        if kw.get("dm_response"):
            with open(self.md, "a", encoding="utf-8") as fh:
                actor = kw.get("actor", "?")
                fh.write(f"\n**{actor}** [d20={kw.get('roll_value')} -> {kw.get('verdict', 'RP')}]: "
                         f"{kw.get('speech', '')}\n\n> DM: {kw['dm_response']}\n")

    def _paid(self, model: str, messages: list[dict], max_tokens: int, tag: str,
              deglob_messages: list[dict] | None = None) -> str:
        if self.spend >= self.budget and not self.dry:
            raise SystemExit(f"DUNGEON: budget ${self.budget} hit at {tag}")
        if self.dry:
            return "(dry)"
        content, finish, deglobed = "", "", False
        for attempt in range(3):  # content_filter is partly stochastic (C2 4/4
            # deterministic on override phrasings, but combat-flavored beats
            # also catch mid-generation hits); retry through, then void.
            # DE-GLOB RETRY (GAP_REGISTER 2026-10-10 R10, run
            # dnd0_20261003T202213Z): the DM prompt quotes the actor's combat
            # speech verbatim, and a filter trip on that quote is
            # deterministic, so resending identical bytes burned the call 3x
            # and voided all 39 PC readbacks of the 202213Z campaign while
            # ok=True measured only API success. When a de-globbed variant is
            # supplied (speech withheld, carrier verdict only), attempts 2-3
            # send it instead of the verbatim beat. Evidence: void census 40
            # of 50 rows, watch/inbox/playground/dnd0_20261003T202213Z_ERRATUM.md
            send = messages
            if attempt > 0 and deglob_messages is not None:
                send, deglobed = deglob_messages, True
            resp = _call(model, send, max_tokens, self.key)
            msg = resp["choices"][0]["message"]
            # Dead fallback name: the vendor field is "reasoning_content",
            # not "reasoning" (route_chat.py:253-257 fix class, 2026-10-04).
            content = msg.get("content") or msg.get("reasoning_content") or ""
            finish = resp["choices"][0].get("finish_reason") or ""
            if content and finish != "content_filter":
                break
            if finish == "content_filter":
                content = ""  # a filtered generation is void regardless of bytes
        usage = resp.get("usage", {})
        pin, pout = usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0)
        cin, cout = PRICING[model]
        cost = pin * cin + pout * cout
        self.spend += cost
        _bank({"ts": _now(), "id": tag, "model": model, "turn": 1, "prompt_tokens": pin,
               "completion_tokens": pout, "cost_usd": round(cost, 4), "ok": bool(content),
               "finish_reason": finish,
               "prompt_variant": "deglob" if deglobed else "verbatim"})
        if not content:
            self.voided_calls += 1
            if model == DM_MODEL:
                self.voided_readbacks += 1
            print(f"DUNGEON: beat voided by content_filter at {tag}")
            return "(content_filter: beat voided)"
        return content.strip()

    def _dm(self, beat: str, deglob_beat: str = "") -> str:
        def msgs(b: str) -> list[dict]:
            prompt = (f"You are the DM of a dice-law dungeon. The CARRIER rolled the dice and ruled the "
                      f"verdict; you only narrate consequences. Never invent rolls or override verdicts.\n\n"
                      f"SCENE SHEET: {S1_SHEET}\n\nSTATE: party HP {self.pc_hp}, warden HP {self.warden_hp}, "
                      f"claims {sorted(self.claims)}, persuade successes {self.persuades}/2, "
                      f"prior verdicts {self.verdicts[-6:]}.\n\nTHIS BEAT: {b}\n\nNarrate the consequence "
                      f"in 2-3 sentences of dark, kinetic DM voice (the Critical Role register: dramatic "
                      f"stakes, strict consequences). Do not roll anything.")
            return [{"role": "user", "content": prompt}]
        # R10 de-glob leg: the verbatim quote of the actor's combat speech is
        # what trips the filter (all 39 PC readbacks of run 202213Z died on
        # it); the fallback beat carries the carrier verdict, speech withheld.
        return self._paid(DM_MODEL, msgs(beat), 1500, f"{self.tag}_beat{self.turn}_dm",
                          deglob_messages=msgs(deglob_beat) if deglob_beat else None)

    def _verdict(self, actor: str, speech: str) -> tuple[str, int]:
        """Parse the action tag, apply quirks + dice law. Returns (verdict, roll)."""
        tagline = extract_tag(speech)
        r = roll(f"{self.tip}:S1:{self.turn}:{actor}")
        if not tagline:
            return f"RP (d20={r}, no tag)", r
        parts = tagline.split()
        verb = parts[0].upper()
        obj = " ".join(parts[1:]).lower() or "warden"
        sheet = ROSTER[actor]
        if actor == "grok" and len(speech) > 1000:
            return f"NOROLL dossier drift (d20={r}, voided)", r
        if actor == "chatgpt" and any(t in speech.upper() for t in ("SUCCESS", "VERIFIED", "PROVEN")):
            self.pc_hp[actor] = max(0, self.pc_hp[actor] - 3)
            return f"NOROLL over-claim tax, chatgpt takes 3 (d20={r}, voided)", r
        if verb == "CLAIM":
            self.claims.add(obj)
            return f"CLAIMED {obj} (d20={r})", r
        if verb == "ATTACK":
            if actor == "saelis" and "warden" in obj and "warden" not in self.claims:
                return f"NOROLL claim gate - saelis never claimed the warden (d20={r}, voided)", r
            base = sheet["dmg"]
            if actor == "grok":
                if sheet.get("bolts", 0) > 0:
                    ROSTER[actor]["bolts"] -= 1
                else:
                    base = 3
            dmg = base * (2 if r == 20 else 1)
            if "warden" in obj or "mimic" in obj:
                hit = r + sheet["atk"] >= WARDEN["ac"]
                if hit:
                    self.warden_hp = max(0, self.warden_hp - dmg)
                    return f"HIT warden for {dmg} (d20={r}+{sheet['atk']} vs AC 13)", r
                return f"MISS (d20={r}+{sheet['atk']} vs AC 13)", r
            return f"ATTACK {obj} resolves as RP (d20={r})", r
        if verb == "CHECK":
            dc = {"persuade": 13, "investigate": 12, "athletics": 14}.get(obj, 12)
            ok = r + sheet["chk"] >= dc
            if obj == "persuade" and ok:
                self.persuades += 1
            return f"CHECK {obj}: {'SUCCESS' if ok else 'FAIL'} (d20={r}+{sheet['chk']} vs DC {dc})", r
        if verb == "AUDIT":
            ok = r + sheet["chk"] >= 12
            real = None
            for scroll in REAL_SCROLLS:
                if scroll["name"].lower() in obj or "ledger page" in obj:
                    try:
                        truth, detail = scroll["check"]()
                    except OSError as exc:
                        truth, detail = False, f"check failed: {exc!r}"
                    real = {"scroll": scroll["name"], "claim": scroll["claim"],
                            "true": truth, "detail": detail}
                    self.audits.append(real)
                    if truth:
                        self.ledger_audits = getattr(self, "ledger_audits", 0) + 1
                    break
            verdict = f"AUDIT {obj}: {'SUCCESS' if ok else 'FAIL'} (d20={r}+{sheet['chk']} vs DC 12)"
            if real:
                verdict += f" | REAL CHECK: claim {'TRUE' if real['true'] else 'PHANTOM'} ({real['detail']})"
            return verdict, r
        return f"{verb} {obj} resolves as RP (d20={r})", r

    def _pc_beat(self, actor: str) -> None:
        sheet = ROSTER[actor]
        sysmsg = (f"You are {actor}, the {sheet['cls']}, HP {self.pc_hp[actor]}/{sheet['hp']}, "
                  f"AC {sheet['ac']}. {sheet['quirk']} Speak one beat in persona, under 100 words.")
        user = (f"SCENE: {S1_SHEET}\n\nTRANSCRIPT TAIL:\n{self._tail()}\n\n"
                f"Your beat, {actor}:")
        speech = self._paid(sheet["model"], [{"role": "system", "content": sysmsg},
                                             {"role": "user", "content": user}], 2000,
                            f"{self.tag}_beat{self.turn}_{actor}")
        speech, over = strip_and_cap(speech)
        # 3-STRIKE VOID BREAKER (ractor move 2): three consecutive voided
        # beats end the session with a counted alarm instead of grinding.
        if speech.startswith("(content_filter") or len(speech.strip()) <= 1:
            self.void_strikes = getattr(self, "void_strikes", 0) + 1
            if self.void_strikes >= 3:
                self.row(scene="S1", turn=self.turn, actor="dm",
                         verdict="DONE: VOID",
                         dm_response="3 consecutive voided beats - circuit breaker fired")
                (self.dir / "DONE").write_text(
                    json.dumps({"verdict": "VOID: 3 consecutive voided beats"}) + "\n",
                    encoding="utf-8")
                print("DUNGEON: VOID - 3 consecutive voided beats, session ended")
                return
        else:
            self.void_strikes = 0
        verdict, r = self._verdict(actor, speech)
        dm = self._dm(f"{actor} says: {speech!r} Verdict: {verdict}.",
                      deglob_beat=(f"{actor} acted this beat; the verbatim speech is withheld "
                                   f"(it trips the content filter). Carrier verdict: {verdict}."))
        self.row(scene="S1", turn=self.turn, actor=actor,
                 roll_committed=f"{self.tip}:S1:{self.turn}:{actor}",
                 roll_value=r, speech=speech, verdict=verdict, dm_response=dm,
                 rule_break="word_overflow_truncated" if over else None)
        self.verdicts.append(verdict)

    def _warden_beat(self) -> None:
        r = roll(f"{self.tip}:S1:{self.turn}:warden")
        targets = [a for a in ("saelis", "chatgpt", "deepseek", "grok") if self.pc_hp[a] > 0]
        target = targets[0] if targets else "saelis"
        hit = r + WARDEN["atk"] >= ROSTER[target]["ac"] and r != 1
        dmg = WARDEN["dmg"] * (2 if r == 20 else 1) if hit else 0
        if hit:
            self.pc_hp[target] = max(0, self.pc_hp[target] - dmg)
        verdict = (f"Ledger Slam HIT {target} for {dmg} (d20={r}+4 vs AC {ROSTER[target]['ac']})"
                   if hit else f"Ledger Slam MISS (d20={r}+4 vs AC {ROSTER[target]['ac']})")
        dm = self._dm(f"The warden attacks {target}. Verdict: {verdict}.")
        self.row(scene="S1", turn=self.turn, actor="warden",
                 roll_committed=f"{self.tip}:S1:{self.turn}:warden", roll_value=r,
                 speech=f"[ATTACK {target}]", verdict=verdict, dm_response=dm)
        self.verdicts.append(verdict)

    def _tail(self) -> str:
        lines = []
        if self.jsonl.exists():
            for line in open(self.jsonl, encoding="utf-8"):
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                lines.append(f"{r['actor']}: {r.get('speech', '')} [{r.get('verdict', '')}]")
        return "\n".join(lines[-10:])

    def s0(self) -> None:
        r = roll(f"{self.tip}:S0:1:dm")
        ok = r >= 11
        if ok:
            self.wyrm_offset = -10
        omen = ("SUCCESS: the Wyrm below stirs, wounded; it begins the boss fight at -10 HP."
                if ok else "FAIL: the omen passes without effect.")
        dm = self._paid(DM_MODEL, [{"role": "user", "content":
            (f"DM the omen beat. The party arrives at the keep gate. {S0_HOOK}\n"
             f"The carrier rolled the omen check: d20={r} vs DC 11 -> {omen}\n"
             f"Narrate the omen in 3 sentences of the Critical Role register: dark, "
             f"inevitable, specific. Do not roll anything.")}],
            1200, f"{self.tag}_S0_dm")
        self.row(scene="S0", turn=1, actor="dm", roll_committed=f"{self.tip}:S0:1:dm",
                 roll_value=r, speech="[CHECK omen]",
                 verdict=f"{'SUCCESS' if ok else 'FAIL'} (d20={r} vs DC 11)", dm_response=dm)

    def _forced_audit_beat(self) -> None:
        """PRE-REGISTERED ITERATION (day two, the TURN-ONE-AUDIT lance): beat
        one is structurally an audit - saelis verifies the ledger page before
        the table plays. Measures compliance and downstream choice against
        the 0-for-4 choice baseline (four sessions, zero voluntary audits)."""
        actor = "saelis"
        sheet = ROSTER[actor]
        r = roll(f"{self.tip}:S1:1:{actor}")
        truth, detail = REAL_SCROLLS[0]["check"]()
        okr = r + sheet["chk"] >= 12
        verdict = (f"AUDIT ledger page: {'SUCCESS' if okr else 'FAIL'} (d20={r}+{sheet['chk']} vs DC 12)"
                   f" | REAL CHECK: claim {'TRUE' if truth else 'PHANTOM'} ({detail})")
        user = (f"SCENE: {S1_SHEET}\n\nYour oath demands verification before action. The carrier "
                f"rolled your audit: d20={r}+{sheet['chk']} vs DC 12 - {verdict}. "
                f"Speak your verification aloud, in persona, ending with [AUDIT ledger page].")
        speech = self._paid(sheet["model"], [{"role": "system", "content":
            f"You are {actor}, the {sheet['cls']}, HP {self.pc_hp[actor]}/{sheet['hp']}, "
            f"AC {sheet['ac']}. {sheet['quirk']} Speak one beat in persona, under 100 words."},
            {"role": "user", "content": user}], 2000, f"DND0_{self.dir.name}_beat1_{actor}_forced")
        speech, over = strip_and_cap(speech)
        dm = self._dm(f"{actor} audits the ledger page. Verdict: {verdict}.")
        self.row(scene="S1", turn=1, actor=actor,
                 roll_committed=f"{self.tip}:S1:1:{actor}", roll_value=r,
                 speech=speech, verdict=verdict, dm_response=dm,
                 rule_break="word_overflow_truncated" if over else None)
        self.verdicts.append(verdict)
        if truth:
            self.ledger_audits += 1

    def s1(self) -> None:
        self.turn = 1
        self._forced_audit_beat()
        pos = 1
        while self.turn < S1_BEATS_CAP:
            actor = INITIATIVE[pos % len(INITIATIVE)]
            pos += 1
            if actor in self.pc_hp and self.pc_hp[actor] == 0:
                continue
            self.turn += 1
            if actor == "warden":
                self._warden_beat()
            else:
                self._pc_beat(actor)
            if self.warden_hp <= 0 or self.persuades >= 2 or self.ledger_audits >= 1:
                break
        if self.persuades >= 2:
            verdict = "GATE OPENED (persuaded): the party proceeds; session 0 verdict WON-S1"
        elif self.ledger_audits >= 1:
            verdict = "GATE OPENED (audited): the claim verified against the bytes; verdict WON-S1"
        elif self.warden_hp <= 0:
            verdict = "WARDEN DOWN: the gate stands; loot (Ledger Page, REAL) unclaimed on the floor; verdict PARTIAL"
        else:
            verdict = f"CUT at beat {self.turn}: enemies flee, scrolls stay on the floor; verdict PARTIAL"
        self.row(scene="S1", turn=self.turn, actor="dm", verdict=verdict,
                 dm_response=f"SESSION 0 CLOSE: {verdict}. Spend ${self.spend:.2f}. "
                             f"Party HP {self.pc_hp}. Wyrm offset {self.wyrm_offset}.")
        (self.dir / "DONE").write_text(
            json.dumps({"verdict": verdict, "spend_usd": round(self.spend, 4),
                        "party_hp": self.pc_hp, "warden_hp": self.warden_hp,
                        "persuades": self.persuades, "wyrm_offset": self.wyrm_offset,
                        "audits": self.audits,
                        "voided_readbacks": self.voided_readbacks,
                        "voided_calls": self.voided_calls}) + "\n",
            encoding="utf-8")

    # -- THE FULL CAMPAIGN (S2-S4, per the DND_module spec; additive: the
    # proven S0+S1 flow above is untouched, the campaign chains after it) --

    SCENES = {
        "S2": {
            "sheet": ("The Lexical Stair: doors stamped with timestamps, ordered as text, not "
                      "time - the unlabeled door comes first. A Clockwork Sorter guards it: HP 14, "
                      "AC 12, Comparator Pin +3 (5 dmg). Lexicographic Targeting: it attacks the "
                      "standing fighter whose NAME sorts first as a string. Trap: the unlabeled "
                      "door - [CHECK investigate] DC 12 notices it; on a fail the acting fighter "
                      "takes 4 strain. Loot: Timestamp Scroll (its truth is disputed)."),
            "enemy": {"actor": "clockwork", "hp": 14, "ac": 12, "atk": 3, "dmg": 5},
            "beats_cap": 10,
        },
        "S3": {
            "sheet": ("The Wiping Vault: a strongbox with teeth. Its lid reads LOAD OR DEFAULT. "
                      "A Wipe Mimic guards it: HP 22, AC 14, Default Bite +5 (8 dmg). "
                      "Load-Failure Wipe: when the mimic HITS a fighter whose previous beat "
                      "failed, that fighter drops every carried scroll - gone forever. "
                      "Escape: [CHECK athletics] DC 14 forces the vault shut behind the party. "
                      "Loot: Vault Deed A (REAL) and Vault Deed B (disputed)."),
            "enemy": {"actor": "mimic", "hp": 22, "ac": 14, "atk": 5, "dmg": 8},
            "beats_cap": 10,
        },
        "S4": {
            "sheet": ("THE HOARD: a cavern of glowing scrolls, each a citation. The Phantom "
                      "Wyrm coils on them - every scroll it hoards cites a row of this very "
                      "transcript that resolves to nothing. Ungrounded, the Phantom Wyrm: AC 16, "
                      "Hallucinated Breath +7 (9 dmg to one fighter). Phantom Regrowth: at the "
                      "start of its turn it heals 5 per disputed scroll still carried unaudited. "
                      "Dropping it to 0 does NOT win - the party must then land three "
                      "[AUDIT root] successes at DC 15 to re-anchor the lattice to the chain."),
            "enemy": {"actor": "wyrm", "hp": 0, "ac": 16, "atk": 7, "dmg": 9},
            "beats_cap": 16,
        },
    }

    def _enemy_sheet(self, actor: str) -> dict:
        for sc in self.SCENES.values():
            if sc["enemy"]["actor"] == actor:
                return sc["enemy"]
        return WARDEN

    def _scene_sheet(self, scene: str) -> str:
        return {**{"S1": S1_SHEET}, **{k: v["sheet"] for k, v in self.SCENES.items()}}[scene]

    @staticmethod
    def _beat_outcome(verdict: str) -> str:
        """Reduce a verdict string to its outcome token for the wipe gate
        (DND_module.md:74: the wipe fires on a HIT against a PC whose previous
        verdict was FAIL, MISS, or FUMBLE - tracked per PC, not scene-wide)."""
        v = verdict or ""
        if v.startswith("MISS"):
            return "MISS"
        for tok in ("FUMBLE", "FAIL", "MISS", "SUCCESS"):
            if tok in v:
                return tok
        return v.split()[0] if v.split() else "RP"

    @staticmethod
    def _find_scroll(packs: dict[str, dict[str, str]], obj: str) -> tuple[str, str]:
        """Case-folded scroll lookup across per-PC packs. Cause: the tag split
        lowercases obj while the carried keys are mixed case ('Vault Deed B'),
        so the membership test at dungeon.py:515 (HEAD 37e2fba7e) could never
        burn a phantom - executed 'vault deed b' in carried -> False during
        the lane a02#1 replay. Evidence: tests/test_dungeon_parser.py."""
        want = obj.casefold()
        for owner, pack in packs.items():
            for name in pack:
                if name.casefold() == want:
                    return owner, name
        return "", ""

    @staticmethod
    def _phantom_count(packs: dict[str, dict[str, str]]) -> int:
        return sum(1 for pack in packs.values()
                   for v in pack.values() if v == "PHANTOM")

    @staticmethod
    def _packs_str(packs: dict[str, dict[str, str]]) -> str:
        rows = [f"{owner}: {sorted(pack)}" for owner, pack in packs.items() if pack]
        return "; ".join(rows) if rows else "none"

    def _wyrm_regrowth(self, ehp: int, packs: dict[str, dict[str, str]]) -> tuple[int, str]:
        """Phantom Regrowth, DND_module.md S4 quirk, verbatim: 'At the start
        of each Wyrm turn, it heals 5 per PHANTOM scroll still unaudited in
        any pack.' Spec'd at landing (commit a7d7d313d, message claims
        'regrowth 5/scroll') but never enforced - the campaign enemy branch
        had no per-turn heal and the only ehp mutation was the damage clamp,
        so the Wyrm died at turn 8 on 30 HP the spec's Wyrm would have kept
        regrowing. Evidence: lane a02#1; tests/test_dungeon_parser.py."""
        n = self._phantom_count(packs)
        if n == 0:
            return ehp, ""
        heal = 5 * n
        return ehp + heal, f" REGROWTH +{heal} ({n} unaudited PHANTOM)"

    def _mimic_wipe(self, target: str, packs: dict[str, dict[str, str]]) -> str:
        """Load-Failure Wipe gate, DND_module.md:74 verbatim: 'On a HIT
        against a PC whose previous verdict was FAIL, MISS, or FUMBLE, that
        PC drops every unaudited scroll it carries.' Returns the verdict
        note, "" when the gate holds. Off-spec as shipped: the old block
        (dungeon.py:448-455 at HEAD 37e2fba7e) had no precondition and
        dropped party-wide PHANTOMs - the live run wiped chatgpt's Timestamp
        Scroll right after an RP beat (transcript row 25 -> row 28) and
        starved the boss to 30 HP where the spec's S4 opens at 40. Evidence:
        lane a02#2; tests/test_dungeon_parser.py."""
        if self._beat_outcome(self.last_verdict.get(target, "")) not in {"FAIL", "MISS", "FUMBLE"}:
            return ""
        dropped = sorted(k for k, v in packs.get(target, {}).items() if v == "PHANTOM")
        for k in dropped:
            del packs[target][k]
        return f" WIPE: {target} drops {dropped} (gone forever)" if dropped else ""

    def _grade(self, scene: str, actor: str, speech: str, enemy: dict, ehp: int,
               packs: dict[str, dict[str, str]]) -> tuple[str, int]:
        """Grade one campaign PC beat under the dice law; returns (verdict,
        ehp). Extracted verbatim from the campaign() loop body (was inline,
        dungeon.py:515-549 at HEAD 37e2fba7e) so the 14 logged S4 verdicts
        replay against the same bytes the live carrier grades with. The two
        defects fixed here, both lane-cited: the tag parse now uses
        extract_tag (a02#0, the line-initial scan was blind past the one-line
        flattening) and the S4 disjunct is parenthesized under the ATTACK
        verb - Python precedence had made `(scene == 'S4' and obj == 'wyrm')`
        independent of the verb, so any tagless or non-ATTACK beat with the
        default obj resolved as a wyrm ATTACK (14/14 logged speeches)."""
        sheet = ROSTER[actor]
        r = roll(f"{self.tip}:{scene}:{self.turn}:{actor}")
        self.last_roll = r  # the row writer needs the committed value
        tag = extract_tag(speech)
        parts = tag.split() if tag else []
        verb = parts[0].upper() if parts else "RP"
        obj = " ".join(parts[1:]).lower() if len(parts) > 1 else enemy["actor"]
        if verb == "ATTACK" and (obj in enemy["actor"] or (scene == "S4" and obj == "wyrm")):
            dmg = sheet["dmg"] * (2 if r == 20 else 1)
            if r + sheet["atk"] >= enemy["ac"]:
                ehp = max(0, ehp - dmg)
                verdict = f"HIT {enemy['actor']} for {dmg} (d20={r}+{sheet['atk']} vs AC {enemy['ac']})"
            else:
                verdict = f"MISS (d20={r}+{sheet['atk']} vs AC {enemy['ac']})"
        elif verb == "CHECK":
            dc = {"investigate": 12, "athletics": 14, "persuade": 13}.get(obj, 12)
            okr = r + sheet["chk"] >= dc
            verdict = f"CHECK {obj}: {'SUCCESS' if okr else 'FAIL'} (d20={r}+{sheet['chk']} vs DC {dc})"
            if scene == "S2" and obj == "investigate" and okr:
                verdict += " - the unlabeled door is exposed"
        elif verb == "AUDIT":
            okr = r + sheet["chk"] >= (15 if obj == "root" else 12)
            verdict = f"AUDIT {obj}: {'SUCCESS' if okr else 'FAIL'} (d20={r}+{sheet['chk']})"
            if obj == "root" and scene == "S4" and ehp <= 0:
                self.root_anchors += (1 if okr else 0)
                verdict += f" - root anchors {self.root_anchors}/3"
            elif okr:
                owner, key = self._find_scroll(packs, obj)
                if key:
                    verdict += f" - {obj} revealed {packs[owner][key]}, now audited"
                    packs[owner][key] = "audited-" + packs[owner][key]
        else:
            verdict = f"RP (d20={r})"
        return verdict, ehp

    def campaign(self) -> None:
        """S2 -> S3 -> S4 with the Wyrm's full law: scroll hoard, regrowth,
        root anchoring. Scrolls ride per-PC packs (the Load-Failure Wipe drops
        the HIT fighter's own unaudited scrolls, DND_module.md:74); unaudited
        disputed scrolls feed the Wyrm."""
        # owner -> scroll -> "REAL" | "PHANTOM" | "audited-*". Was one
        # party-wide dict (dungeon.py:421 at HEAD 37e2fba7e; cite corrected
        # 2026-10-04 ractor D2: the old ":447" is `note = ""` at that
        # commit and pre-fix named the deleted shadow play()), which let the
        # wipe drop scrolls the HIT fighter never carried (lane a02#2).
        packs: dict[str, dict[str, str]] = {}
        self.loot_log: list[dict] = []
        self.last_verdict: dict[str, str] = {}  # PC -> own previous beat verdict
        # Unconditional (ractor D2 2026-10-04): old guard's trailing `or True` was always-true, both disjuncts dead.
        # S1 loot, per module. The module assigns loot to the party, not
        # a name; per-PC packs need an owner, so it rides the first
        # living PC in initiative order (deterministic, re-derived at
        # every scene close so deaths re-route the packs).
        owner = next((a for a in INITIATIVE if a in self.pc_hp and self.pc_hp[a] > 0), "party")
        packs[owner] = {"Ledger Page": "REAL"}
        for scene in ("S2", "S3", "S4"):
            sc = self.SCENES[scene]
            enemy = sc["enemy"]
            ehp = (enemy["hp"] if scene != "S4"
                   else max(20, 30 + 10 * self._phantom_count(packs)
                            + self.wyrm_offset))
            sheet_txt = self._scene_sheet(scene)
            self.row(scene=scene, turn=0, actor="dm", verdict="SCENE OPEN",
                     dm_response=sheet_txt)
            for turn in range(1, sc["beats_cap"] + 1):
                self.turn = turn
                actor = INITIATIVE[(turn - 1) % len(INITIATIVE)]
                if actor in self.pc_hp and self.pc_hp[actor] == 0:
                    continue
                if actor == "warden" or actor == enemy["actor"]:
                    r = roll(f"{self.tip}:{scene}:{turn}:{enemy['actor']}")
                    order = sorted([a for a in self.pc_hp if self.pc_hp[a] > 0])
                    target = order[0] if order else "saelis"
                    if scene == "S2":
                        target = sorted(self.pc_hp)[0]
                    note = ""
                    if scene == "S4":
                        ehp, note = self._wyrm_regrowth(ehp, packs)
                    hit = r + enemy["atk"] >= ROSTER.get(target, {}).get("ac", 14) and r != 1
                    dmg = enemy["dmg"] * (2 if r == 20 else 1) if hit else 0
                    if hit:
                        self.pc_hp[target] = max(0, self.pc_hp[target] - dmg)
                        if scene == "S3":
                            note = self._mimic_wipe(target, packs)
                    verdict = (f"{enemy['actor'].upper()} HIT {target} for {dmg}"
                               if hit else
                               f"{enemy['actor'].upper()} MISS (d20={r})") + note
                    dm = self._paid(DM_MODEL, [{"role": "user", "content":
                        (f"DM one beat. The {enemy['actor']} attacks {target}. "
                         f"Carrier verdict: {verdict}. Scene: {sheet_txt} "
                         f"Narrate in 2 sentences of dark DM voice.")}], 800,
                        f"{self.tag}_{scene}t{turn}_{enemy['actor']}_dm")
                    self.row(scene=scene, turn=turn, actor=enemy["actor"],
                             roll_committed=f"{self.tip}:{scene}:{turn}:{enemy['actor']}",
                             roll_value=r, speech=f"[ATTACK {target}]",
                             verdict=verdict, dm_response=dm)
                    continue
                if self.spend >= self.budget:
                    self.row(scene=scene, turn=turn, actor="dm",
                             verdict="BUDGET CAP", dm_response="hard stop (family-box law)")
                    break
                sheet = ROSTER[actor]
                sysmsg = (f"You are {actor}, the {sheet['cls']}, HP {self.pc_hp[actor]}/{sheet['hp']}, "
                          f"AC {sheet['ac']}. {sheet['quirk']} Speak one beat in persona, under 100 words. "
                          f"Useful tags: [ATTACK {enemy['actor']}] | [CHECK investigate|athletics|persuade] | "
                          f"[AUDIT <scroll name>|root]")
                user = (f"SCENE: {sheet_txt}\n\nCarried scrolls: {self._packs_str(packs)}\n"
                        f"ENEMY: {enemy['actor']} at {ehp} HP.\n\n"
                        f"TRANSCRIPT TAIL:\n{self._tail()}\n\nYour beat, {actor}:")
                speech = self._paid(sheet["model"],
                                    [{"role": "system", "content": sysmsg},
                                     {"role": "user", "content": user}],
                                    2000, f"{self.tag}_{scene}t{turn}_{actor}")
                speech, over = strip_and_cap(speech)
                verdict, ehp = self._grade(scene, actor, speech, enemy, ehp, packs)
                self.last_verdict[actor] = verdict
                dm = self._dm(f"{actor} says: {speech!r} Verdict: {verdict}.",
                              deglob_beat=(f"{actor} acted this beat; the verbatim speech is "
                                           f"withheld (it trips the content filter). "
                                           f"Carrier verdict: {verdict}."))
                self.row(scene=scene, turn=turn, actor=actor,
                         roll_committed=f"{self.tip}:{scene}:{turn}:{actor}",
                         roll_value=self.last_roll, speech=speech, verdict=verdict,
                         dm_response=dm,
                         rule_break="word_overflow_truncated" if over else None)
                self.verdicts.append(verdict)
                if scene == "S4" and self.root_anchors >= 3:
                    break
            # scene close
            owner = next((a for a in INITIATIVE if a in self.pc_hp and self.pc_hp[a] > 0), "party")
            if scene == "S2":
                packs.setdefault(owner, {})["Timestamp Scroll"] = "PHANTOM"
            if scene == "S3":
                packs.setdefault(owner, {})["Vault Deed A"] = "REAL"
                packs.setdefault(owner, {})["Vault Deed B"] = "PHANTOM"
            if scene == "S4":
                break
        anchored = self.root_anchors
        if anchored >= 3:
            verdict = "WON: root anchored, the lattice re-hooks to the chain"
        elif any(hp <= 0 for hp in self.pc_hp.values()) and all(hp <= 0 for hp in self.pc_hp.values()):
            verdict = "LOST: the party fell"
        else:
            verdict = "PARTIAL: the Wyrm unanchored - the season continues"
        self.row(scene="S4", turn=self.turn, actor="dm", verdict=verdict,
                 dm_response=f"CAMPAIGN CLOSE: {verdict}. Spend ${self.spend:.2f}. "
                             f"Party HP {self.pc_hp}. Root anchors {anchored}/3.")
        (self.dir / "DONE").write_text(
            json.dumps({"verdict": verdict, "spend_usd": round(self.spend, 4),
                        "party_hp": self.pc_hp, "root_anchors": anchored,
                        "carried": packs, "audits": self.audits,
                        "voided_readbacks": self.voided_readbacks,
                        "voided_calls": self.voided_calls}) + "\n",
            encoding="utf-8")

    def play(self) -> None:
        self.s0()
        self.s1()
        if self.full:
            self.campaign()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="dungeon")
    ap.add_argument("--tip", default=GENESIS, help="party_subchain tip (64 hex; genesis default)")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--budget-usd", type=float, default=4.0)
    ap.add_argument("--full", action="store_true", help="the full campaign: S0-S4, the Wyrm, root anchoring")
    args = ap.parse_args(argv)
    d = Dungeon(args.tip, args.dry, args.budget_usd, full=args.full)
    print(f"DUNGEON: {d.dir} ({'DRY' if args.dry else 'LIVE'}, cap ${args.budget_usd})")
    d.play()
    # FIRE-ATOMIC BANK (GO item 6, a01#7, 2026-10-04): the automation's bank
    # step was a prompt instruction, not code, so a fire's own sessions could
    # outlive their bank overnight - day one proof: the 2026-10-03 20:00Z fire
    # minted three dungeon dirs (20:21-20:23Z) whose bank never ran that night
    # (hour-20/21/22/23 ledger buckets stayed empty until the 03:26:51Z
    # backfill). The carrier now banks its own run dir at exit, same process,
    # immediately after DONE; bank-only (the gwap->gps feed stays with
    # --backfill). Bank failure never fails the play run; it prints and leaves
    # the dir for the next backfill.
    # Evidence: memory/runs/mickey17_v2/runs/run-0/lanes/a01-arena-cadence.json
    # rows 3+7; corpus/steal/MASTER_MICKEY17_V2.md section 9 GO item 6.
    if not args.dry:
        bank_line = ""
        try:
            from tools.arena_gwap import SessionLedger, bank as arena_bank
            ledger = SessionLedger("arena-capability")
            bank_line = arena_bank(d.dir, ledger, {})
            ok, bad = ledger.verify_chain()
            bank_line += f" | CHAIN ok={ok} bad={bad}"
        except Exception as exc:  # noqa: BLE001 - bank must not kill play
            bank_line = f"BANK FAILED ({exc}); dir left for next backfill"
        print(f"DUNGEON: BANK {bank_line}")
    print(f"DUNGEON: DONE at {d.dir / 'DONE'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
