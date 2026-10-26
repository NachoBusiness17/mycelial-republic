"""secret_guard - code-level enforcement of Nacho's 'just don't touch secrets' rule.

API (in-process only):
    load_secret(path, name, caller)  -> str   value stays in this process
    export_secret(...)               -> always raises SecretExportDenied
    request_transfer(name, dest, caller) -> bool (TTY + fresh nonce, else False)
    payload_hits(data)               -> list of sha8 fingerprints found in data
    install_hook()                   -> sys.addaudithook guard (opt-in MAG_SECRET_GUARD=1)

Limits: this is an in-repo guard. A process with a raw shell (PowerShell, cmd, a
python without the hook) can bypass it. Real enforcement needs OS-level controls;
see tools/secret_guard/README.md.
"""
from tools.secret_guard.guard import (  # noqa: F401
    SecretExportDenied, SecretAccessDenied, load_secret, export_secret,
    request_transfer, payload_hits, is_secret_path, fingerprints, sha8,
)
from tools.secret_guard.hook import install_hook  # noqa: F401
