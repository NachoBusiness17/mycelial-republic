"""PROPOSED (not installed): drop as .venv/Lib/site-packages/sitecustomize.py, or add a
.pth line, ONLY with Nacho's OK. Activates only when MAG_SECRET_GUARD=1.

    import os, sys
    if os.environ.get("MAG_SECRET_GUARD") == "1":
        sys.path.insert(0, r"C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent")
        from tools.secret_guard import install_hook
        install_hook()
"""
