# W2 draft order — mag/wow_player.py (player-file ledger, blueprint M2)

Write ONE complete Python 3.11 stdlib-only module. No external deps. Output ONLY the module
source, no fences, no commentary.

## The law you are implementing

A character is an append-only ledger, not a database row. Login is resume-from-ledger.
The anti-MySQL law made structural: state is the REPLAY of ledger rows through pure reducers;
the stored "traits" dict is only a materialized view, and load() must re-derive it from the
rows and refuse the file if the two disagree.

## Exact contract (do not deviate)

SCHEMA = "wow_player.v1"                      # the file schema string
STORE   = ROOT / "memory" / "runs" / "wow_player"   # one file per player: <player_id>.json
ROOT via the exact idiom from mag/wow_bones_session.py:
    try:
        from config import ROOT
    except Exception:
        ROOT = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(ROOT))

canonical(obj) -> str: json.dumps(obj, ensure_ascii=False, sort_keys=True,
separators=(",", ":")). THE ONLY serialization in the module — used for saving, hashing,
and canonical-state comparison.

player_id_for(name) -> "ply-" + sha256(f"{SCHEMA}:{name}".encode("utf-8")).hexdigest()[:12]
(secret-free salt = the schema string itself; deterministic, never a secret)

File shape (the dict written to disk):
    {"schema": SCHEMA,
     "player_id": "ply-xxxxxxxxxxxx",
     "name": str,
     "traits": {"room": str, "stamina_max": int, "inventory": [ <pack receipts: opaque dicts> ]},
     "ledger": [ {"n": int, "event": str, "data": {...}, "prev": hex64, "hash": hex64}, ... ]}

NO timestamps, NO wall clock, NO randomness, NO uuid4 anywhere in file content. "created"
fields are FORBIDDEN — determinism law. (hashlib/urllib for hashing are fine.)

Ledger rules:
- Genesis: row n=1, event="create", data={"room": ..., "stamina_max": ...},
  prev="0"*64.
- row["prev"] == previous row's hash.
- row["hash"] = sha256(canonical({"n": n, "event": event, "data": data, "prev": prev})
  .encode("utf-8")).hexdigest()
- Every mutation appends EXACTLY one row. Rows are never edited or removed once written.

Events (reducers are pure functions event -> view -> view):
- "create"     data {"room": str, "stamina_max": int}   (n=1 only)
- "move"       data {"to": str}                          -> view room = to
- "stamina"    data {"delta": int}                       -> view stamina_max += delta
- "grant_item" data {"item": {...}}                      -> appends to view inventory
- "spend_item" data {"item_id": str}                     -> does NOT mutate inventory rows;
    it appends a shadowing spend; the view is computed by replay: inventory = grants whose
    item_id has not been spent (spend removes the earliest unspent grant with that id).
- UNKNOWN_EVENT is typed-refused: apply() raises PlayerLedgerError("UNKNOWN_EVENT", ...).

API:
class PlayerLedgerError(Exception) with .reason attribute (str, uppercase typed reason).
class PlayerFile:
    - create(name, room="atrium", stamina_max=10) -> PlayerFile   (writes genesis row, saves)
    - apply(event, **data) -> dict   (appends one row, updates view, saves)
    - to_file() -> dict              (the exact file dict above)
    - canonical_state() -> str       (canonical(to_file()) — the byte-identity surface)
    - save() -> Path                 (canonical bytes, STORE/<player_id>.json)
    - @classmethod load(player_id) -> PlayerFile | None (None when file absent)
load() MUST: json-parse, check schema, verify chain, REPLAY all rows through reducers,
compare replayed view to stored traits — on any mismatch raise PlayerLedgerError with the
typed reason (see below). It must never silently trust the stored view.

verify_file(d) -> (ok: bool, reason: str). Typed reasons, checked IN THIS ORDER:
    "BAD_SCHEMA"   (not a dict / schema != SCHEMA / missing keys)
    "BAD_ID"       (player_id != player_id_for(name))
    "BAD_N"        (n not contiguous from 1)
    "BROKEN_CHAIN" (row prev != previous hash, or genesis prev != "0"*64)
    "TAMPERED"     (recomputed row hash != stored hash)
    "VIEW_MISMATCH" (replayed reducers != stored traits)
    ok is True with reason "OK" only when all pass.

Inventory append-only law at FILE level: grant rows and spend rows both live forever in the
ledger; only the replayed VIEW drops spent items. A test will assert tampering impossible
to see in row count: after grant+spend, len(ledger) == 3 and inventory view is empty.

CLI (argparse, style of mag/wow_bones_session.py main, all output via _emit = print(canonical)):
    python -m mag.wow_player create --name NAME [--room R] [--stamina N]
    python -m mag.wow_player apply   --player ply-... --event EVENT [--data JSON]
    python -m mag.wow_player show    --player ply-...
    python -m mag.wow_player verify  --player ply-...   (emit {"ok":..., "reason":...})
Module docstring at top: 8-15 lines explaining the law (ledger not row; resume-from-ledger;
no timestamps; schema wow_player.v1), same voice as mag/wow_bones_session.py.

## Self-check (do it, but do not trust it)

After writing, mentally trace: create -> move -> grant -> spend -> save -> load in a fresh
process, canonical_state() byte-identical. Flip one hash char -> TAMPERED. Report nothing
about your own quality — the editor runs the falsifiers.
