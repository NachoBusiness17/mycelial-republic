"""B2-521: the straggler cerebras consumers are gated on the B2-133 dormant flag.

CAUSE: B2-133 gated seven mag/ lane lists, but six more sites still hardcoded the
dormant cerebras lane: mag/swarm_worker.py DEFAULT_PROVIDER (every provider-less
swarm task), mag/_consensus_witness.py LANES (witness seat), mag/scale_salon.py
ALLOWED_BASES + cerebras-oss architect/writer rows, mag/ask_router.py LANE_TIERS
(free-tier-0 cost prior), mag/subscriptions.py free_lanes display row ("cerebras
85%"), mag/seat_corpus.py SEND_LAWS registry row.
EVIDENCE: configs/providers.yaml cerebras block carries dormant: true (B2-36,
card-gated 30-day trial, chat 402 no-credit) and
watch/inbox/burn_wave_20260926/B2_133_cerebras_purge_20260926.md (the helper law,
mag/dormant.py).

Law under test: no live path in those six files serves a currently dormant
provider; operator GO flips the flag and every gate restores its row with no code
edit (the premise assert below fires loudly on GO instead of rotting).
"""
import sys
import urllib.parse
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from mag import dormant  # noqa: E402


def test_no_straggler_serves_a_currently_dormant_provider():
    live = dormant.dormant_ids()
    assert "cerebras" in live, (
        "B2-521 premise gone: providers.yaml no longer flags cerebras dormant "
        "(operator GO landed?); the straggler gates then have no bite and this "
        "test may be retired")
    hosts = dormant.dormant_hosts()

    from mag import _consensus_witness, ask_router, seat_corpus  # noqa: E402
    from mag import scale_salon, subscriptions, swarm_worker  # noqa: E402

    # swarm default: the ZAI_LITE_LAW order gated to the first non-dormant carrier
    assert swarm_worker.DEFAULT_PROVIDER not in live
    assert swarm_worker.DEFAULT_PROVIDER == "groq"

    # consensus witness roster: no dormant provider id survives the gate
    assert not {ln[1] for ln in _consensus_witness.LANES} & live

    # scale salon: no dormant host in the SSRF allowlist, and no gopher/writer row
    # that resolves to a dormant base (cerebras-oss, and ids gone from LANES entirely)
    for base in scale_salon.ALLOWED_BASES:
        assert urllib.parse.urlparse(base).hostname not in hosts, base
    selectable = ({g[0] for g in scale_salon._GOPHERS}
                  | {w[0] for w in scale_salon.WRITER_LENSES})
    assert "cerebras-oss" not in selectable
    laned = {ln["id"]: ln for ln in scale_salon.LANES}
    for lane_id in selectable:
        lane = laned.get(lane_id)
        assert lane is not None, f"gopher/writer lane {lane_id} not in the gated LANES table"
        assert urllib.parse.urlparse(lane["base"]).hostname not in hosts, lane_id

    # ask router: no dormant provider keeps a free-tier cost prior
    assert not set(ask_router.LANE_TIERS) & live

    # subscriptions: the free_lanes row carries no dormant claim, name or key
    row = next(s for s in subscriptions.SUBSCRIPTIONS if s["id"] == "free_lanes")
    for pid in live:
        assert pid not in row["name"], pid
        assert pid not in row["note"], pid
    assert "CEREBAS_API_KEY" not in row["keys"]

    # seat corpus: the registry OpenClaw reads compiles no dormant drive-laws
    assert not set(seat_corpus.SEND_LAWS) & live
