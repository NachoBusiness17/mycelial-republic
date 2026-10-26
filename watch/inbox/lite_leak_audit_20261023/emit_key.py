import sys
sys.path.insert(0, r"C:\Users\foste\Documents\projects\local_sovereign_agent")
from tools.secret_guard.guard import load_secret
k = load_secret(r"C:\Users\foste\Documents\projects\local_sovereign_agent\.env", "ZAI_API_KEY_Lite", caller="lite_leak_audit_20261023")
sys.stdout.buffer.write(k.encode("utf-8") + b"\n")
sys.stdout.buffer.flush()
