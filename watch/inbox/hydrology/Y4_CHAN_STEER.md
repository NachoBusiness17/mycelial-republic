# Y4 - chan.py check_steer: the public square reads the STEER channel (2026-09-29)

## Coverage gap 10, batch 2 lane 4/12
The mates were not the only steerable surface. The play face (mag/chan.py, the
Primer public square on watch/room.jsonl) now has its own mouth on the operator
channel.

## Landed
- `mag/chan.py` :: `check_steer(target, path=None) -> dict` — calls
  `tools.steer_read.read(target)` and shapes the operative row as a greentext
  card (`>steer from the operator (via):\n>...`) the board prepends to its next
  output (card above the OP; one mouth, operator's word first). Additive only:
  no existing verb rewired, room.jsonl untouched, lazy `from tools import
  steer_read` so the board still paints without the toolbelt.
- Contract teeth held on this face:
  - anti-forgery — operative row marked `proposal` is an ask, not an order;
    proposals-only channel yields `card: ""`, board paints as usual;
  - latest-wins — an older order does not resurface when the newest applicable
    row is a proposal;
  - missing channel → `ok: False` with empty card (dark lane, not silent);
    malformed rows stay the reader's stderr report, never widened here.
- `tests/test_chan.py` amended (+5): seed row (`st_20260930_seed_1`, mate
  "all", hand-edit) returned when target matches; scoped row matches its target
  only; proposals-only → empty; latest-proposal suppresses older order; missing
  channel → ok False. Live STEER.md never touched — seed row copied verbatim
  into tmp channels (same convention as tests/test_steer.py).

## Test receipts (real counts, `.venv/Scripts/python.exe -m pytest -q`)
- `tests/test_chan.py` alone: **12 passed** (7 pre-existing + 5 new) in 0.60s.
- steer suite `tests/test_steer.py tests/test_steer_bridge.py
  tests/test_steer_sign.py tests/test_seat_steer.py`: **23 passed** in 5.93s.
- Combined single run (both bullets' files at once): **35 passed** in 6.07s.

No commit (lane contract). Seed row operative for every target until the
operator lands a newer applicable row.
