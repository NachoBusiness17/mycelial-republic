"""Stage the ractor rotation CYCLE 0 chain as one-tap intent links (fostertron door).

The 2026-09-06 rehearsal thread (memory/runs/salons/ractor_rotation_20260906/CYCLE0_THREAD.md)
was never fired: state sat at "rehearsed_awaiting_door". Activated 2026-09-24 on
operator order "Shitpost ractor desk activate". Chain protocol: fire link 1, paste the
new status id back into this generator, it grafts in_reply_to for slot 2 and re-emits;
repeat down the chain. The desk regenerates after every data change.

  python watch/RACTOR_CYCLE0_STAGED_gen.py                 # slot 1 armed only
  python watch/RACTOR_CYCLE0_STAGED_gen.py --ids 1234      # slot 2 arms against 1234
  python watch/RACTOR_CYCLE0_STAGED_gen.py --ids 1234 5678 # slot 3 arms, etc.

Charter lens-check applied 2026-09-24: craft law (no em-dash), no parens, labels in
comments only, one device per post, register purity (falsifier: two ractors in the
same register breaks the rotation). Posting = operator hand only. fostertron face
only; @NachoQuixotic must never carry this thread.
"""
import argparse
from pathlib import Path
from urllib.parse import quote

OUT = Path(__file__).resolve().parent / "inbox" / "SHITPOST_DESK_RACTOR_CYCLE0_STAGED_20260924.md"

# (ractor tag - COMMENTS ONLY, dice roll, post text)
CHAIN = [
    ("NACHO_MASK", "opener",
     "Open-book cipher from march. frontier walked the public record, found the root, "
     "found the lock hash, wrote computed on the quote.\n\nF. \U0001F90C"),

    ("JUNG", "roast",
     "F. for First. You walked the public record hunting a lock and came home wearing a "
     "chair. Open-book cipher, closed-book coronation. Wrote \"computed\" on the quote like "
     "a crown. The \U0001F90C isn't the find. That's the director hunger kissing the sitting."),

    ("MCLUHAN", "riff",
     "You loaded the canon on-stage. Medium bowed. Then you diagnosed a chair from the "
     "cushion. Hunger is content; the 280 sat you. First was furniture. F. for Form."),

    ("BAUDRILLARD", "roast",
     "You crowned Form and sat him in the 280. Cute throne. The cushion was already a "
     "copy. No chair, no medium, just sitting selling sitting. You didn't diagnose "
     "furniture. You furnished the diagnosis. F. for Fourth."),

    ("PLATO_KIRK", "roast+puzzle",
     "Cute throne, then you sold the throne's absence. Sitting selling sitting is still "
     "sitting. Facing the wall. You redecorated the dark and called it Fourth. F. for "
     "Fire.\n\n3-1-22-5. Door, or rewrite?"),

    # LIVE SLOT 2026-09-24: dice rolled RIFF. Decodes the pending cipher (A1Z26 ->
    # CAVE, the room posts 1-5 were sitting in) and takes the door half of the fork.
    # Ellul register: technique decides, inevitability, who scheduled it. Crowns the
    # next F-word and hands the chain to ELDER (echo) at slot 7.
    ("ELLUL", "riff",
     "3-1-22-5. CAVE. Nobody decided to sit in the dark. Technique built the walls, "
     "scheduled the shadows, and called the sitting a choice. You asked door or rewrite. "
     "The door was never locked, only unplanned. We walk out. F. for Field."),
]


def compose_intent(text: str) -> str:
    return f"https://x.com/intent/tweet?text={quote(text, safe='')}"


def reply_intent(status_id: str, text: str) -> str:
    return f"https://x.com/intent/tweet?in_reply_to={status_id}&text={quote(text, safe='')}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", nargs="*", default=[], help="fired status ids, in chain order")
    args = ap.parse_args()
    if len(args.ids) > len(CHAIN):
        ap.error("more ids than chain slots")

    for i, (tag, dice, text) in enumerate(CHAIN, 1):
        assert len(text) <= 280, f"slot {i} ({tag}) over 280: {len(text)}"
        assert "(" not in text and ")" not in text, f"slot {i} ({tag}) has parens"
        assert "\u2014" not in text and "\u2013" not in text, f"slot {i} ({tag}) has a dash"
        for name in ("NACHO_MASK", "JUNG", "MCLUHAN", "BAUDRILLARD", "PLATO", "KIRK", "ELLUL"):
            assert name not in text.upper(), f"slot {i} ({tag}) leaks a voice tag"

    lines = [
        "# SHITPOST DESK — RACTOR ROTATION CYCLE 0, STAGED · 2026-09-24",
        "",
        "Activated on operator order. 6 slots: the 09-06 rehearsal thread, lens-checked",
        "to the 09-24 charter, plus one live slot (ELLUL, RIFF) answering the pending",
        "cipher. Cipher key: 3-1-22-5 = CAVE (A1Z26).",
        "",
        "**Door law:** fostertron face ONLY. Verify the logged-in account before every",
        "tap; if it is not fostertron, do not fire. @NachoQuixotic never carries this.",
        "Posting = operator hand. One tap per slot, ~2h pacing, down the chain.",
        "",
        "**Chain protocol:** fire slot 1, copy its status id from the permalink, rerun",
        "`python watch/RACTOR_CYCLE0_STAGED_gen.py --ids <id1> <id2> ...`, this page",
        "regenerates with slot 2 attached as a reply. Repeat. Slots without an id yet",
        "show a bare compose link as fallback (fire it as a reply manually, or wait for",
        "the graft).",
        "",
        "---",
        "",
    ]
    armed = len(args.ids)
    for i, (tag, dice, text) in enumerate(CHAIN, 1):
        if i == 1:
            link = compose_intent(text)
            kind = "▶ compose on fostertron"
        elif i <= armed:
            link = reply_intent(args.ids[i - 2], text)
            kind = f"▶ reply to {args.ids[i - 2]}"
        else:
            link = compose_intent(text)
            kind = "compose fallback — awaiting upstream id"
        lines.append(f"## Slot {i} · {dice} · `{tag}` (voice tag never posts)")
        lines.append("")
        lines.append(f"> {text}".replace("\n", "\n> "))
        lines.append("")
        lines.append(f"- **[{kind}]({link})**")
        lines.append("")
    lines += [
        "---",
        "",
        "**Ledger:** 09-06 rehearsed in salon (5 slots, CYCLE0_THREAD.md). 09-24",
        "activated: craft-law pass applied (em-dashes died, parens died, asserts added),",
        "ELLUL slot 6 rolled and drafted from ELLUL_panel_20260903.md. Next in roster:",
        "ELDER (echo, six lines) at slot 7; FERMAT gated, skipped until the operator",
        "fresh-seed pass. Fired slots + engagement get logged here and in",
        "watch/ractor_rotation_state.json. The ledger is the training signal.",
        "",
        "**Falsifiers:** two ractors in one register = rotation broken. Any of this on",
        "@NachoQuixotic = full halt and brick.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} ({len(CHAIN)} slots, {armed} reply-grafted)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
