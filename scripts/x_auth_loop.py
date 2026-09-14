"""x_auth_loop — standing-door OAuth for the @GroundingWave surface.

Re-arms the authorization flow every 10 minutes until the operator approves.
Runs unattended: tap the URL whenever it suits — the token banks itself on
callback and the loop exits. Log: memory/runs/x_oauth/auth_flow_live.log
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # repo root for mag.*

from mag import x_oauth as x

DEADLINE_HOURS = 6
WINDOW_S = 600


def main() -> None:
    t0 = time.time()
    attempt = 0
    while time.time() - t0 < DEADLINE_HOURS * 3600:
        attempt += 1
        d = x.start()
        if not d.get("ok"):
            print(f"[attempt {attempt}] start failed: {d}", flush=True)
            time.sleep(60)
            continue
        print(f"[attempt {attempt}] AUTH URL: {d['authorize_url']}", flush=True)
        t1 = time.time()
        while not x._captured.get("code") and time.time() - t1 < WINDOW_S:
            time.sleep(1)
        code = x._captured.get("code", "")
        if code:
            print("[callback captured] exchanging...", flush=True)
            print(x.complete(code), flush=True)
            print("TOKEN STORED — the door did its job. Go tell the operator.", flush=True)
            return
        print(f"[attempt {attempt}] window lapsed — re-arming", flush=True)
        x._captured.clear()


if __name__ == "__main__":
    main()
