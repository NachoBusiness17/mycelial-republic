"""B2-491 landing: anchored QUEUE.md edits on freshly-read bytes.

Three anchored replaces, each asserted unique before write:
  1. header pointer-anchor law paragraph after the lane-id claim law
  2. landing note appended to the B2-491 row (sat pre-checked [x] from birth,
     the B2-238 disease; this landing earns the check)
  3. retire the two B2-491 CLAIM lines (board + band) to CLAIMED

Receipt: watch/inbox/burn_wave_20260926/B2_491_pointer_rot_20260926.md
Run: .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_491_queue_landing.py
"""

from pathlib import Path

QUEUE = Path(__file__).resolve().parent / "QUEUE.md"
LAW_PATH = QUEUE.parent / "B2_491_pointer_rot_20260926.md"

LAW = (
    "Pointer-anchor law (B2-491, 2026-09-26): file:line pointers in burn briefs rot silently "
    "because upstream edits move the bytes under the number (the disease, twice same-day: this "
    "queue's B2-107 row cites configs/providers.yaml:66-67 for the ollama base_url_env but the "
    "key sat at line 84 by that landing, 66-67 left as the tail of the saelis block; the B2-105 "
    "row's configs/providers.yaml:473-488 mistral pointer rotted to the z_ai region when the "
    "block moved, named in its own landing note), so a lane that trusts the number reads the "
    "wrong block with no surface naming the rot. From this law every NEW file:line pointer in a "
    "QUEUE brief row carries a byte anchor written path:NN[-MM]#token, where token is the exact "
    "key name, symbol, or a double-quoted fragment the cited lines contain at filing time; a "
    "pointer that names no lines stays bare. The checker "
    "`.venv/Scripts/python.exe tools/pointer_rot_check.py [--briefs|--json|--selftest]` "
    "re-resolves anchored pointers against current bytes (ROT when the anchor is absent from the "
    "cited range, with definition-like token lines as the repair hint; MISSING and OOB are rot "
    "classes too), checks legacy bare pointers against a seed table of the two known-rot cases "
    "(ROT-SEED), counts every other bare pointer UNANCHORED so the adoption gap stays visible, "
    "and exits 1 while any ROT, ROT-SEED, MISSING or OOB stands. Landed rows are history and "
    "stay byte-untouched (the B2-255 precedent): the flag is the surface that names their rot, "
    "and repair happens when a lane next touches the row. Falsifier: on the pre-landing board "
    "the checker exits 1 naming both seeds (base_url_env absent at 66-67, the ollama key "
    "measured at 84 on the B2-107 landing read and 93 at this law's 19:29Z scan, the yaml moved "
    "again mid-lane; mistral absent at 473-488, block at 550 at scan time), artifact "
    "watch/inbox/burn_wave_20260926/B2_491_pointer_rot_check_results.json, receipt "
    "watch/inbox/burn_wave_20260926/B2_491_pointer_rot_20260926.md; "
    "tools/pointer_rot_check.py --selftest replays the disease on a fixture without the board."
)

ROW_NOTE = (
    " Landed 2026-09-26 (the row sat pre-checked [x] from birth with no receipt, the B2-238 "
    "disease; this landing earns the check): pointer-anchor law paragraph added to this header "
    "block; tools/pointer_rot_check.py landed (anchored re-resolve with definition-line repair "
    "hints, seed table ROT-SEED for the two known rotted pointers, UNANCHORED census of the 202 "
    "bare legacy pointers, --selftest fixture replay, exit 1 while any rot stands); falsifier "
    "executed pre-landing on live bytes: exit 1 with 2 ROT-SEED hits, base_url_env absent at "
    "66-67 (ollama key measured at 84 on the B2-107 landing read and 93 at this lane's 19:29Z "
    "scan, providers.yaml moved again mid-lane), mistral absent at 473-488 (block at 550 at "
    "scan time), artifact watch/inbox/burn_wave_20260926/B2_491_pointer_rot_check_results.json; "
    "the B2-107 and B2-105 rows stay byte-untouched history, the checker is the surface naming "
    "their rot and this row's own corrected pointer is configs/providers.yaml:93#base_url_env; "
    "self-feed band B2-501..B2-503 claimed after the B2-465 band B2-498..B2-500 took 498-500 "
    "mid-lane, renumbered highest+1 per the B2-167 law; foreign active CLAIMs (B2-489, B2-465, "
    "B2-469) honored, appends and anchored edits only; ratchet --changed NEW=0; em-dash 0 on "
    "added lines; receipt watch/inbox/burn_wave_20260926/B2_491_pointer_rot_20260926.md; "
    "self-fed B2-501, B2-502, B2-503 UNCHECKED."
)

HEADER_ANCHOR = "checkbox law (earned flips).\n\n## Dispensed"
ROW_ANCHOR = "B2_107_ollama_trap_20260926.md Bibliography.\n"
CLAIM_BOARD = "- CLAIM B2-491 watch/inbox/burn_wave_20260926/QUEUE.md 2026-09-26T19:27:49Z"
CLAIM_BAND = "- CLAIM B2-501..B2-503 watch/inbox/burn_wave_20260926/QUEUE.md 2026-09-26T19:27:49Z"


def replace_once(text: str, old: str, new: str, what: str) -> str:
    n = text.count(old)
    assert n == 1, f"{what}: anchor count {n} != 1, rebasing on fresh bytes required"
    return text.replace(old, new)


def main() -> None:
    text = QUEUE.read_text(encoding="utf-8")
    text = replace_once(
        text,
        HEADER_ANCHOR,
        "checkbox law (earned flips).\n\n" + LAW + "\n\n## Dispensed",
        "header law insert",
    )
    text = replace_once(
        text,
        ROW_ANCHOR,
        "B2_107_ollama_trap_20260926.md Bibliography." + ROW_NOTE + "\n",
        "B2-491 row landing note",
    )
    for claim, retired in (
        (CLAIM_BOARD, "- CLAIMED B2-491 watch/inbox/burn_wave_20260926/QUEUE.md 2026-09-26T19:27:49Z"),
        (CLAIM_BAND, "- CLAIMED B2-501..B2-503 watch/inbox/burn_wave_20260926/QUEUE.md 2026-09-26T19:27:49Z"),
    ):
        text = replace_once(
            text,
            claim,
            retired + " -> " + str(LAW_PATH.relative_to(QUEUE.parent.parent.parent)).replace("\\", "/"),
            "claim retire",
        )
    QUEUE.write_text(text, encoding="utf-8", newline="")
    print("landed: header law, row note, 2 claims retired")


if __name__ == "__main__":
    main()
