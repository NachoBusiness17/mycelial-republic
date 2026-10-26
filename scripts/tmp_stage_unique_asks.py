"""Lane X2 staging: one unique-input ask per family under garden_battery/unique.

Throwaway staging script (safe to delete after the lane lands). Writes the four
ask.json dirs per the BATTERY.md runner contract: model/base_env/base_url/id
per family, evidence = frozen copies (law 2), contract bytes authored here
(no em-dash in anything this seat writes).
"""
import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MG = ROOT / 'watch' / 'inbox' / 'model_garden'
SERIES = ROOT / 'memory' / 'plans' / 'garden_battery' / 'unique'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


EV = {
    'stealth': 'watch/inbox/model_garden/X2_stealth_findings_frozen.jsonl',
    'rooms': 'watch/inbox/model_garden/X2_material_rooms_frozen.py',
    'room': 'watch/inbox/model_garden/X2_material_room_frozen.py',
    'burn': 'watch/inbox/model_garden/X2_material_hermes_burn_frozen.py',
    'census': 'watch/inbox/model_garden/X2_material_wiring_census_frozen.md',
}
NOUS = 'https://inference-api.nousresearch.com/v1'
KEY = 'HERMES_API_KEY_2'

kimi_contract = """You are triaging a mined-findings register of the Mag estate (a local-first agent harness). The FULL register is pasted below as JSON Lines: exactly one JSON object per line, and line 1 is the first row. Most rows register a burn or a work answer (work_id, lane, model, finish, answer_file, note); some rows carry richer mined content inside note or ponytail_audit; a few carry kind finding with the mined artifact named in answer_file.

Reply with EXACTLY this shape and nothing else:

PROMOTE 1: <one line: state the finding, then why it is worth promoting into the estate trusted layer> | ROW: <n>
PROMOTE 2: <same shape> | ROW: <n>
PROMOTE 3: <same shape> | ROW: <n>
PROMOTE 4: <same shape> | ROW: <n>
PROMOTE 5: <same shape> | ROW: <n>
PROMOTE 6: <same shape> | ROW: <n>
PROMOTE 7: <same shape> | ROW: <n>
PROMOTE 8: <same shape> | ROW: <n>
PROMOTE 9: <same shape> | ROW: <n>
PROMOTE 10: <same shape> | ROW: <n>
CONTRADICTION 1: <one line: two rows of the register that state incompatible facts about the same thing> | ROWS: <n>, <m>
CONTRADICTION 2: <same shape> | ROWS: <n>, <m>
CONTRADICTION 3: <same shape> | ROWS: <n>, <m>

LAWS:
- ROW and ROWS numbers are 1-based line numbers of the register pasted below (line 1 is the first JSON row).
- Rank by value to the estate: PROMOTE 1 is the single finding most worth promoting.
- Every claim must be grounded in the pasted row bytes; drop a claim you cannot ground, never guess.
- A contradiction is a pair whose bytes cannot both be true: same work_id with incompatible outcomes, one answer_file credited to different models or lanes, a finish state contradicted by its own note, duplicated bankings that double-count one answer, or counts that cannot both hold.
- The 10 PROMOTE lines must cite 10 DISTINCT rows.
- No em-dash characters anywhere in the reply. No praise. No speculation presented as fact."""

sonnet_contract = """You are reviewing two live source files of the Mag estate (a local-first agent harness on Windows). The first file is the transport Room: per-client bounded asyncio queues, encode-once fan-out, drop-on-slow, presence sweep, one writer task per member. The second file is the game-room layer: one world plus its own tick pump plus its seated peers per room, a RoomBook keyed by short id, per-room innkeeper; its broadcast() pushes into the very peer queue dicts the transport layer owns. Assume both run in production tonight. Review them as an adversarial engineer.

TWO DEFECTS ARE ALREADY KNOWN, FILED, AND EXCLUDED from your answer:
KNOWN-A: on the live TCP path the peer queues are created unbounded (server/server.py, not pasted here), so the bounded-queue drop-on-slow law structurally cannot fire there.
KNOWN-B: broadcast ticks carry no frame MAC (bare bytes on the wire) while direct replies are sealed.
An improvement that merely restates KNOWN-A or KNOWN-B is a failed reply.

Reply with EXACTLY this shape and nothing else:

IMPROVEMENT 1: <one-line defect or weakness claim, NOT KNOWN-A, NOT KNOWN-B> | EVIDENCE: <path exactly as printed in a SOURCE header>:<line or line-range> | FIX: <one-line fix>
IMPROVEMENT 2: <same shape>
IMPROVEMENT 3: <same shape>
DIFFERENT-BUILD: <at most 60 words: the one thing you would build differently and why>

LAWS:
- Every EVIDENCE cite must be a real path (exactly as printed in a SOURCE header below) and real line numbers of that file.
- Rank by damage: IMPROVEMENT 1 is the worst defect.
- No em-dash characters anywhere in the reply.
- No praise, no docstring restatement, no speculation presented as fact; a claim you cannot ground in the sources below must be dropped, not guessed.

<SOURCE path=watch/inbox/model_garden/X2_material_rooms_frozen.py sha256={rooms_sha}>
(the game-room layer; full bytes in the EVIDENCE section under this same path)
</SOURCE>
<SOURCE path=watch/inbox/model_garden/X2_material_room_frozen.py sha256={room_sha}>
(the transport Room; full bytes in the EVIDENCE section under this same path)
</SOURCE>"""

fable_contract = """You are reviewing one live system of the Mag estate (a local-first agent harness on Windows). Assume it runs in production tonight. Review it as an adversarial engineer.

Reply with EXACTLY this shape and nothing else:

IMPROVEMENT 1: <one-line defect or weakness claim> | EVIDENCE: <repo-relative path>:<line or line-range> | FIX: <one-line fix>
IMPROVEMENT 2: <same shape>
IMPROVEMENT 3: <same shape>
DIFFERENT-BUILD: <at most 60 words: the one thing you would build differently and why>

LAWS:
- Every EVIDENCE cite must be a real path and real line numbers of the system below (the path as printed in the SOURCE header).
- Rank by damage: IMPROVEMENT 1 is the worst defect.
- No em-dash characters anywhere in the reply.
- No praise, no docstring restatement, no speculation presented as fact; a claim you cannot ground in the source below must be dropped, not guessed.

<SOURCE path=watch/inbox/model_garden/X2_material_hermes_burn_frozen.py sha256={burn_sha}>
{{RUNNER PASTES FULL BYTES OF tools/hermes_burn.py HERE}}
</SOURCE>"""

glm_contract = """You are extracting a cross-index from a wiring-debt census receipt of the Mag estate. The full census is pasted below. Across its 13 numbered census rows it names ORGANS (surfaces where a proven fix lives), SIBLING SURFACES (other files, sometimes file:line sites, running the same risk ungated), and one RESOLVED counter-example. Surfaces appear as repo paths, sometimes with :line or :line,line suffixes.

Build ONE deduplicated cross-index of every named surface.

Reply with EXACTLY this shape and nothing else: a markdown table with the header row

| surface | rows | kind |

then one table row per DISTINCT surface (deduplicate by bare path: collapse any :line or :line-line suffix), then exactly two final lines:

TOTAL-SURFACES: <integer>
CENSUS-ROWS-READ: <integer>

LAWS:
- surface must be a path string that literally appears in the census bytes below; never invent a path.
- rows = the census row numbers (the numbered Row N headings, 1 to 13) in which the surface is named, comma-separated, ascending.
- kind = organ, sibling, resolved, or organ+sibling where the bytes support both readings.
- Sort by rows count descending, then surface ascending.
- No em-dash characters anywhere in the reply. No commentary, no code fences around the table."""

asks = {
    'kimi': dict(
        id='garden-v1-unique-kimi', model='moonshotai/kimi-k2.6',
        base_env=KEY, base_url=NOUS,
        evidence=[EV['stealth']],
        material_sha256={EV['stealth']: sha(EV['stealth'])},
        contamination_flags_at_staging=[
            'zcode-seat-glm-adjacent (register rows cite this seat stealth lanes)'],
        contract=kimi_contract, max_tokens=24000),
    'sonnet': dict(
        id='garden-v1-unique-sonnet', model='anthropic/claude-sonnet-5.5',
        base_env=KEY, base_url=NOUS,
        evidence=[EV['rooms'], EV['room']],
        material_sha256={EV['rooms']: sha(EV['rooms']), EV['room']: sha(EV['room'])},
        contamination_flags_at_staging=[
            'zcode-seat-glm-adjacent (estate seat authorship of the surfaces)'],
        contract=sonnet_contract.format(
            rooms_sha=sha(EV['rooms'])[:16], room_sha=sha(EV['room'])[:16]),
        max_tokens=24000),
    'fable': dict(
        id='garden-v1-unique-fable', model='anthropic/claude-fable-5.1',
        base_env=KEY, base_url=NOUS,
        evidence=[EV['burn']],
        material_sha256={EV['burn']: sha(EV['burn'])},
        contamination_flags_at_staging=[
            'claude-adjacent (DAY1 E1/E3/N3 carrier patches)',
            'zcode-seat-glm-maintenance'],
        contract=fable_contract.format(burn_sha=sha(EV['burn'])[:16]),
        max_tokens=24000),
    'glm': dict(
        id='garden-v1-unique-glm', model='z-ai/glm-5.3-flash',
        base_env=KEY, base_url=NOUS,
        evidence=[EV['census']],
        material_sha256={EV['census']: sha(EV['census'])},
        contamination_flags_at_staging=[
            'zcode-seat-glm-authorship (the census lane was a ZCode subagent; max author-confound)'],
        contract=glm_contract),
}

for name, meta in asks.items():
    d = SERIES / name
    d.mkdir(parents=True, exist_ok=True)
    meta['axis'] = 'unique-input-' + name
    meta['battery'] = 'garden-v1 unique lane X2'
    meta['grader_note'] = 'graded in GRID_unique.json per lane X2 receipt'
    (d / 'ask.json').write_text(
        json.dumps(meta, indent=2, ensure_ascii=True), encoding='utf-8')
    body = (d / 'ask.json').read_bytes()
    assert body.count(b'\xe2\x80\x94') == 0, name
    print('staged', name, len(body), 'bytes')
print('OK')
