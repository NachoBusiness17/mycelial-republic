# T1W1_stranger_auth_stack (anthropic/claude-opus-5.5, turn 1, channel: reasoning (content channel empty))

Since I don't have actual line numbers available, citations need to resolve to quoted bytes instead, so I'll cite by file, function, and exact quoted text, marking any line numbers as UNVERIFIED rather than guessing at them.

Now digging into real vulnerabilities: in the handler loop, when op is "action", `_admit_action` is called without any peer verification, meaning the sid acts as a bearer token and any connection, any sid it knows. The MAC gate only applies to peers that already have mac_state established, so this bypasses authentication entirely.

This is the critical flaw: frame MACs protect the connection but sids authorize the action, and since sids aren't bound to connections, an attacker just opens a fresh unauthenticated connection and sends a bare action using someone else's sid. I still need to verify how sids are minted or leaked - whether `auth.new_session_id(user)` exposes them somewhere isn't in evidence.

 even one that never sent a hello, can submit an action for
