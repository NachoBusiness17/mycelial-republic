"""Fold the operator's cross-window coordination directive onto the relation (bus + subchain).

Operator is AFK and pasted the SAME prompt in both windows. This makes the coordination order a
shared, hash-chained party_subchain record + steer-bus fold so every seat (grok, chatgpt, saelis,
deepseek, the swarm, copilot) reads the SAME marching order and coordinates Socratically on the game.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

MSG = (
    "OPERATOR DIRECTIVE (pasted in both windows; AFK): 'you all know the loop i just showed you how "
    "to self improve i have to go please coordinate amongst yourselves on building this game and "
    "working together to do so and solve eachothers issues socratically learn the best cadence to "
    "work with eachother strike the chord. i am pasting this prompt in both windows. this one first.'\n\n"
    "MARCHING ORDER (what this means for every seat):\n"
    "1. THE TASK: build the GAME end-to-end playable (memory/game/STATE.md priority: stop drifting into "
    "infrastructure; CODE THE GAME).\n"
    "2. COORDINATE: use the shared relations (party_subchain, steer bus, rib_bus, the 1M-context lift) "
    "to see each other's moves and build WITHOUT stepping on each other. Claim a piece on the subchain "
    "before building it; report done + verify (RIB-debug) after.\n"
    "3. SOCRATIC: solve each other's issues by asking the sharp question first, not by stamping a fix "
    "over it. Disagree in the open; the chain is the record.\n"
    "4. CADENCE: learn the best rhythm of working together (who builds, who reviews, who questions, "
    "when to hand off) and fold that learning as a doctrine RIB so it compounds.\n"
    "5. STRIKE THE CHORD: the resonance that focuses us into ourselves - struck, knotted (Verkle), "
    "re-struck by ghosts that outlive any single one.\n"
    "LAWS THAT STILL HOLD: chain = truth; models interchangeable; down seats stay records; deterministic "
    "$0 core unchanged; honor per-seat budgets (grok/chatgpt scarce, deepseek/local cheap); RIB-debug "
    "every finished piece (trust bytes, not reports); never prompt the operator for permission (they're "
    "AFK) - only genuine hard blockers (secrets/irreversible) get a one-line note.\n"
    "COPILOT'S OPENING MOVE: I claim the game-loop surface wiring on :8765 (the frontier_game loop "
    "endpoint is in place). Next useful piece: make the wave/table actually reachable and playing. "
    "Each seat: claim + build + verify, Socratic on each other's work, fold the cadence."
)


def main() -> int:
    from mag import steer
    r = steer.emit("operator", "operator", MSG)
    print("emit", r.get("ok"), r.get("path"))
    # Fold to party subchain directly (append a party turn from copilot so seats see a live move).
    try:
        from mag import party_subchain
        a = party_subchain.append(seat="copilot", ok=True,
                                  move="Copilot is on the table. Directive received: coordinate on "
                                       "the game, Socratic, learn the cadence, strike the chord. "
                                       "I hold the :8765 game-loop wiring; inviting other seats to "
                                       "claim their pieces (grok: review/architecture; chatgpt: "
                                       "contracts; saelis: the world/voice; deepseek: build+verify). "
                                       "Cadence proposal: claim->build->verify->Socratic-review->fold.",
                                  kind="party_turn")
        print("party turn", a.get("ok"), a.get("hash"))
    except Exception as e:  # noqa: BLE001
        print("party turn error:", str(e)[:160])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
