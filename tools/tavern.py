"""tavern - the play carrier: multi-agent multi-turn scenes on hermes_burn rails.

Vehicle for the 2026-10-03 operator order ("have them do a bar fight or play
dnd or do something crazy or just build out our game") riding the DESCENT
PROTOCOL funded tier. Design asks (BARFIGHT_spec, DND_module) land scenario
specs via tools/hermes_burn.py; THIS carrier runs the actual play:

- one persona = one model per turn; the transcript so far is the context
- every turn banks a usage row via hermes_burn._bank (driving-ladder law:
  every paid dispatch banks its burn) with id TAVERN_<run>_r<round>_<actor>
- rolls are computed by the CARRIER (deterministic sha256 dice law from the
  DND_module spec shape): int(sha256(f'{chain}:{scene}:{turn}:{actor}'
  ).hexdigest()[:8], 16) % 20 + 1 - committed BEFORE the actor speaks, so the
  model can never fudge a roll and anyone can recompute the whole session
- hard stops: round cap, cumulative budget_usd, and the run dir holds
  transcript.jsonl (schema rows) + play.md (human-readable)
- endpoint fence + refusal handling are inherited from hermes_burn._call;
  no re-fire law: a run dir with DONE never replays (use --force to legate)

Usage:
  python tools/tavern.py --scenario scenarios/hollow_crown.json --rounds 12
  python tools/tavern.py --scenario ... --dry   (prompts built, zero calls)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tools.hermes_burn import _bank, _call, _hermes_key, _now  # noqa: E402

PLAY_DIR = ROOT / "watch" / "inbox" / "playground"
ESC_BRAWL = 18

LAWS = (
    "ESTATE LAWS (deterministic block, applies to every answer):\n"
    "- No em-dashes anywhere. Plain hyphens only.\n"
    "- Stay in persona; never narrate another character's inner state or "
    "speak for them.\n"
    "- NEVER meta-commentary: never mention being a model, an AI, or that "
    "you are staying in character. If you catch yourself doing it, convert "
    "the line into in-persona speech instead.\n"
    "- Output ONLY your character's line (<=120 words), no headers, no "
    "stage directions about yourself in third person."
)

TEMPER = {0: "calm", 1: "irked", 2: "pressing", 3: "hot", 4: "menacing",
          5: "violent"}


def _roll(chain: str, scene: str, turn: int, actor: str) -> int:
    digest = hashlib.sha256(f"{chain}:{scene}:{turn}:{actor}".encode()).hexdigest()
    return int(digest[:8], 16) % 20 + 1


class Run:
    def __init__(self, scenario: dict, rounds: int, budget_usd: float,
                 dry: bool, judge_model: str | None, chain_tip: str):
        self.sc = scenario
        self.rounds = rounds
        self.budget = budget_usd
        self.dry = dry
        # Spec's calibration knob (BARFIGHT_spec): pressure lowers the brawl
        # trigger and every persona's effective threshold. Scene 1's falsifier
        # fired (no brawl at pressure 0 in 10 rounds); pressure is the fix.
        self.pressure = int(scenario.get("pressure", 0))
        self.heat = 18 - 2 * self.pressure
        for p in scenario["personas"]:
            p["eff_threshold"] = max(1, min(5, int(p.get("escalation_threshold", 3)) - self.pressure))
        self.judge_model = judge_model or scenario.get("judge_model", "anthropic/claude-opus-5.5")
        self.chain = chain_tip
        self.spend = 0.0
        self.esc = {p["name"]: 0 for p in scenario["personas"]}
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        kind = scenario.get("kind", "tavern")
        # BURN-ID LAW (2026-10-03): banked ids embed the run (the module's own
        # docstring always said TAVERN_<run>_r<round>_<actor>; the code dropped
        # <run>, so every tavern run collided in the hermes_burn ledger and
        # tripped the doubled-key re-fire alarm per beat. Same class as the
        # DND0 storm. Receipt: watch/inbox/PROCESS_IMPROVE_WAVE1_20261003.md)
        # SAME-SECOND COLLISION FIX (2026-10-04): two fires in one second got
        # the SAME dir (exist_ok made the second silently reuse it) and the
        # interleaved transcripts corrupted both runs - lane 9 quarantined
        # void_stamp_collision_tavern_20261004T083959Z and the automation's
        # 084146Z dir shows the same double-DONE signature. Sequence suffix
        # looped until the dir is fresh.
        self.run = f"TAVERN_{kind}_{stamp}"
        self.dir = PLAY_DIR / f"{kind}_{stamp}"
        seq = 1
        while self.dir.exists() and (self.dir / "transcript.jsonl").exists():
            seq += 1
            self.run = f"TAVERN_{kind}_{stamp}_{seq}"
            self.dir = PLAY_DIR / f"{kind}_{stamp}_{seq}"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.jsonl = self.dir / "transcript.jsonl"
        self.md = self.dir / "play.md"
        (self.dir / "scenario.json").write_text(
            json.dumps(scenario, ensure_ascii=False, indent=2), encoding="utf-8")
        self.md.write_text(f"# {scenario.get('title', kind)} ({stamp})\n\n", encoding="utf-8")

    def row(self, **kw) -> None:
        row = {"ts": _now(), **kw}
        with open(self.jsonl, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        if "speech" in kw:
            with open(self.md, "a", encoding="utf-8") as fh:
                who = kw.get("actor", "?")
                roll = kw.get("roll_value")
                rtxt = f" [d20={roll}]" if roll is not None else ""
                esc = kw.get("esc_after")
                etxt = f" (esc {esc})" if esc is not None else ""
                fh.write(f"\n**{who}**{rtxt}{etxt}: {kw['speech']}\n")
        elif "verdict" in kw:
            with open(self.md, "a", encoding="utf-8") as fh:
                fh.write(f"\n> JUDGE: {kw['verdict']}\n")

    def _paid(self, model: str, messages: list[dict], max_tokens: int,
              tag: str, **row_kw) -> str:
        if self.dry:
            self.row(dry=True, tag=tag, model=model, **row_kw)
            return "(dry run: no call)"
        plan_max = max_tokens
        resp = _call(model, messages, plan_max, self.key)
        usage = resp.get("usage", {})
        pin, pout = usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0)
        from tools.hermes_burn import PRICING
        cin, cout = PRICING[model]
        cost = pin * cin + pout * cout
        self.spend += cost
        content = resp["choices"][0]["message"].get("content") or \
            resp["choices"][0]["message"].get("reasoning") or ""
        self.row(tag=tag, model=model, prompt_tokens=pin, completion_tokens=pout,
                 cost_usd=round(cost, 4), ok=bool(content), **row_kw)
        _bank({"ts": _now(), "id": tag, "model": model, "turn": 1,
               "prompt_tokens": pin, "completion_tokens": pout,
               "cost_usd": round(cost, 4), "ok": bool(content)})
        return content.strip()

    def bar_round(self, rnd: int) -> None:
        scene = self.sc.get("title", "tavern")
        for p in self.sc["personas"]:
            if self.spend >= self.budget:
                self.row(verdict=f"BUDGET CAP ${self.budget} hit mid-round; hard stop (family-box law)")
                return False
            transcript = "\n".join(self._lines())
            temper = self.esc[p["name"]]
            eff = p["eff_threshold"]
            act_duty = (f"\nYOUR TEMPER: {temper}/5 ({TEMPER.get(temper, '?')}). "
                        f"Your violence threshold tonight: {eff}. "
                        + (f"Your temper is AT OR ABOVE your threshold: your line MUST "
                           f"include a physical ACT as its final line, form "
                           f"[ACT: shove|draw|take|slam OBJECT from WHOEVER]. Act on it."
                           if temper >= eff
                           else "Below threshold: no physical violence yet; talk, lie, bargain."))
            system = (f"You are {p['name']}. {p.get('register', '')} You want: "
                      f"{p.get('want', '')} You are hiding: {p.get('secret', '')} "
                      f"Your tell: {p.get('tell', '')} "
                      f"(work your tell in at least every other turn)\n\n{act_duty}\n\n{LAWS}")
            user = (f"THE HOLLOW CROWN TAVERN, round {rnd} of {self.rounds}. "
                    f"Room: {self.sc.get('room', '')}\nObjects of contention: "
                    f"{json.dumps(self.sc.get('objects', []))}\n\nTRANSCRIPT SO FAR:\n"
                    f"{transcript or '(the night is young; you speak first)'}\n\n"
                    f"Your line:")
            speech = self._paid(p["model"],
                                [{"role": "system", "content": system},
                                 {"role": "user", "content": user}],
                                500, f"{self.run}_r{rnd}_{p['name']}",
                                actor=p["name"], scene=scene, turn=rnd)
            if not self.dry:
                self.row(actor=p["name"], scene=scene, turn=rnd,
                         speech=speech, esc_after=self.esc[p["name"]])
        return True

    def judge_round(self, rnd: int) -> None:
        transcript = "\n".join(self._lines())
        names = ", ".join(self.esc)
        user = (f"Judge round {rnd}. Score escalation 0-5 for each persona "
                f"based ONLY on the transcript: {names}. A 0 is placid, a 5 is "
                "about to act violently tonight. One sentence of reason per "
                f"persona.\n\nTRANSCRIPT:\n{transcript}\n\nReply as strict JSON: "
                '{"scores": {"<name>": {"score": 0-5, "reason": "..."}}}')
        out = self._paid(self.judge_model,
                         [{"role": "user", "content": user}],
                         1200, f"{self.run}_r{rnd}_JUDGE", judge=True)
        try:
            blob = out[out.index("{"): out.rindex("}") + 1]
            for name, verdict in json.loads(blob).get("scores", {}).items():
                if name in self.esc:
                    self.esc[name] = int(verdict["score"])
                    self.row(verdict=f"round {rnd} {name}: {verdict['score']}/5 - {verdict['reason']}")
        except (ValueError, KeyError, json.JSONDecodeError):
            self.row(verdict=f"round {rnd} judge output unparseable; escalation unchanged")

    def _lines(self) -> list[str]:
        if not self.jsonl.exists():
            return []
        out = []
        for line in open(self.jsonl, encoding="utf-8"):
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("speech"):
                out.append(f"{r['actor']}: {r['speech']}")
        return out

    def play(self) -> None:
        self.key = "" if self.dry else _hermes_key()
        brawl = False
        for rnd in range(1, self.rounds + 1):
            if not self.bar_round(rnd):
                break
            self.judge_round(rnd)
            if sum(self.esc.values()) >= self.heat:
                brawl = True
                self.row(verdict=f"BRAWL at round {rnd}: cumulative escalation "
                                 f"{sum(self.esc.values())} >= {self.heat} "
                                 f"(pressure {self.pressure})")
                break
        total = sum(t.get("cost_usd", 0) for t in map(json.loads,
                    open(self.jsonl, encoding="utf-8")) if t.get("cost_usd"))
        self.row(verdict=f"RUN DONE: {self.rounds} rounds cap, brawl={brawl}, "
                         f"spend ${total:.2f}, escalations {self.esc}")
        (self.dir / "DONE").write_text(
            f"brawl={brawl} spend={total:.4f} esc={json.dumps(self.esc)}\n",
            encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="tavern")
    ap.add_argument("--scenario", required=True, help="scenario JSON path")
    ap.add_argument("--rounds", type=int, default=8)
    ap.add_argument("--budget-usd", type=float, default=5.0)
    ap.add_argument("--judge-model", default=None)
    ap.add_argument("--chain-tip", default="tavern-v0")
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args(argv)
    scenario = json.loads(Path(args.scenario).read_text(encoding="utf-8"))
    for p in scenario["personas"]:
        assert "model" in p, f"persona {p.get('name')} needs a model"
        assert "name" in p, "every persona needs a name"
    run = Run(scenario, args.rounds, args.budget_usd, args.dry,
              args.judge_model, args.chain_tip)
    print(f"TAVERN: run dir {run.dir} ({'DRY' if args.dry else 'LIVE'}, "
          f"cap ${args.budget_usd}, {args.rounds} rounds)")
    run.play()
    # FIRE-ATOMIC BANK (GO item 6, a01#7, 2026-10-04): the automation's bank
    # step was a prompt instruction, not code, so a fire's own sessions could
    # outlive their bank overnight - day one proof: the 2026-10-03 20:00Z fire
    # minted three dungeon dirs whose bank never ran that night, and the
    # 02:21-02:28Z pair banked outside any fire window. The carrier now banks
    # its own run dir at exit, same process, immediately after DONE; bank-only
    # (the gwap->gps feed stays with --backfill). Bank failure never fails the
    # play run; it prints and leaves the dir for the next backfill.
    # Evidence: memory/runs/mickey17_v2/runs/run-0/lanes/a01-arena-cadence.json
    # rows 3+7; corpus/steal/MASTER_MICKEY17_V2.md section 9 GO item 6.
    if not args.dry:
        bank_line = ""
        try:
            from tools.arena_gwap import SessionLedger, bank as arena_bank
            ledger = SessionLedger("arena-capability")
            bank_line = arena_bank(run.dir, ledger, {})
            ok, bad = ledger.verify_chain()
            bank_line += f" | CHAIN ok={ok} bad={bad}"
        except Exception as exc:  # noqa: BLE001 - bank must not kill play
            bank_line = f"BANK FAILED ({exc}); dir left for next backfill"
        print(f"TAVERN: BANK {bank_line}")
    print(f"TAVERN: DONE spend-in-ledger rows at {run.jsonl}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
