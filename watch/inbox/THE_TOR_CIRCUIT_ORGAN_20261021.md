# THE TOR CIRCUIT ORGAN (2026-10-21)

Operator, on the paranoid-mode stack: "i love the tor per convo." Built,
verified, and wired the same hour.

## What shipped

- **Tor 15.0.26 Expert Bundle** downloaded from dist.torproject.org and
  running on this box: SOCKS 127.0.0.1:9050, Control 127.0.0.1:9051,
  cookie auth, bootstrap 100% (tools/tor/ - gitignored, binaries never
  in-tree per the gala precedent).
- **`tools/tor_circuits.py`**: the circuit organ. Raw control protocol
  (cookie AUTHENTICATE, GETINFO bootstrap, SIGNAL NEWNYM - no stem
  dependency), plus `socks_for(conversation_id)`: the per-conversation
  endpoint generator. 4 tests.
- **hermes_burn wire-in**: HERMES_BURN_PROXY=socks5://127.0.0.1:9050 (+
  HERMES_BURN_PROXY_USER per conversation) routes the boundary carrier's
  whole transport through a circuit. Default OFF - the wire is direct until
  isolation is wanted.

## The verification (by bytes)

SOCKS username isolation (Tor's IsolateSOCKSAuth, default-on) gives each
conversation its own persistent circuit:

- conversation A: exit 80.67.172.162 - STABLE across repeated calls
- conversation B: exit 185.220.101.14 - different exit
- per_conversation_isolation: TRUE

This is exactly the semantics the same-book program needs: isolated from
every other conversation, consistent within itself. NEWNYM (global rotate)
is kept as the secondary tool; username isolation is the primary mechanism
because NEWNYM is global and Tor may reuse clean circuits after rotation
(beat 1: same-exit false negative taught this).

## Scope (honest)

Keyless lanes only. Authenticated lanes (sk- keys, OpenRouter accounts) are
identity-linked regardless of circuit - Tor adds nothing there. Local shelf
never leaves the box. The organ carries NO HTTP traffic; it owns the control
channel and the credential contract. Carriers consume the SOCKS endpoint.

## The reading-round payoff

The same-book independence requirement ("never let readers see each other's
answers") is now enforced at the WIRE: every reading round rotates its
conversation credential, so no lane can correlate the experiment's
dispatches by IP - and no exit relay sees two rounds from the same circuit.
Blind means blind at every layer.

## Standing state

- tor.exe: running (PID on 9050/9051), gitignored, restartable via the
  torrc in tools/tor/tor/.
- The cron keeps sweeping; the fleet keeps writing; this organ joins the
  clocks (rotate per conversation = the consumer's contract).

Falsifier: if two conversations with distinct credentials EVER land on the
same exit for the same destination, the isolation claim is false - the
verify command re-runs this check on demand.
