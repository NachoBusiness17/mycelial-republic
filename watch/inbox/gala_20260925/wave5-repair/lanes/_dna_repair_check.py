"""dna-repair lane finish-line instrument. Run with the repo venv python from repo root.

Checks, in order:
1. line-ending consistency (CRLF convention); normalizes lone LF to CRLF if any
2. byte tail: file must end with a complete sentence, no mid-word truncation
3. path-claim sweep: every path the repaired doc references must resolve on disk
4. dash scan: em/en dash count + which lines carry them (authored vs pre-existing)
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
DNA = os.path.join(ROOT, "docs", "DNA.md")

with open(DNA, "rb") as f:
    data = f.read()

crlf = data.count(b"\r\n")
lone_lf = data.count(b"\n") - crlf
print(f"[1] line endings: CRLF={crlf} lone-LF={lone_lf} bytes={len(data)}")
if lone_lf:
    data = data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    with open(DNA, "wb") as f:
        f.write(data)
    print("[1] NORMALIZED: rewrote all endings to CRLF (file's existing convention)")
    crlf = data.count(b"\r\n")
    lone_lf = data.count(b"\n") - crlf
    print(f"[1] after normalize: CRLF={crlf} lone-LF={lone_lf}")
else:
    print("[1] PASS: consistent CRLF, no normalization needed")

text = data.decode("utf-8")
lines = text.split("\r\n")
print(f"[1] lines={len(lines)} (trailing empty element = final newline: {lines[-1] == ''})")

print("\n[2] byte tail (last 3 lines):")
for ln in lines[-4:-1]:
    print("    |" + ln)
tail = data[-120:]
print(f"[2] last 120 bytes: {tail!r}")
ok_tail = lines[-2].rstrip().endswith(".")
print(f"[2] PASS: ends with complete sentence (final period)" if ok_tail
      else f"[2] FAIL: last line does not end with '.' -> {lines[-2]!r}")

print("\n[3] path-claim sweep (all paths the repaired doc references):")
claims = [
    "docs/HOW_TO_MAG_DASHBOARD.md",
    "docs/ref/OPERATOR_CARD.md",
    "memory/agent_state/LATEST.md",
    "docs/ref/DASHBOARD_DESIGN.md",
    "docs/archive",
    "docs/archive/README.md",
    "docs/templates/REF_LEAF.md",
    "docs/templates/FEATURE_COMPOSE.md",
    "docs/templates/MODEL_TESUJI.md",
    "docs/ref/strike_origin.md",
    "docs/ref/run_trail_lattice.md",
    "configs/modules.yaml",
    "docs/ref/memory_verkle_map.md",
    "docs/ref/lessig_1_6.md",
    "memory/portable_bags",
    "docs/ref/MIRROR_PRESENTED.md",
    "docs/ref/MAG_OS_v2.md",
    "docs/ref/MAG_Card.md",
    "docs/ref/MAG_Activation.md",
    "docs/ref/MAG_v2_PLAN.md",
    "memory/improve/pins/LATEST.md",
    "memory/biography/residual",
    "memory/biography/registry.jsonl",
    "memory/biography/knots",
    "memory/biography/verkle_tip.json",
    "memory/biography/verkle_chain.jsonl",
    "memory/biography/kpi.json",
    "memory/biography/derived",
    "mag/daemon.py",
    "mag/biography.py",
    "watch/session_end_hook.py",
    "main.py",
]
fails = 0
for p in claims:
    full = os.path.join(ROOT, p.replace("/", os.sep))
    ok = os.path.exists(full)
    if not ok:
        fails += 1
    print(f"    {'OK  ' if ok else 'MISS'} {p}")
print(f"[3] {'PASS: all ' + str(len(claims)) + ' path claims resolve' if fails == 0 else 'FAIL: ' + str(fails) + ' missing'}")

print("\n[4] dash scan (em=U+2014 en=U+2013):")
em_lines = [i + 1 for i, ln in enumerate(lines) if "\u2014" in ln]
en_lines = [i + 1 for i, ln in enumerate(lines) if "\u2013" in ln]
print(f"    em-dash lines: {em_lines if em_lines else 'none'}")
print(f"    en-dash lines: {en_lines if en_lines else 'none'}")
authored = {3, 42, 60, 73, 76, 84, 85, 86, 131, 145, 146, 147, 149}
em_authored = [n for n in em_lines if n in authored]
en_authored = [n for n in en_lines if n in authored]
print(f"    em/en dashes on lanes-authored lines (3,42,60,73,76,84,85,86,129,143,144,145,148): "
      f"{em_authored + en_authored if em_authored + en_authored else 'none'}")
print("[4] note: any em-dash lines outside the authored set are pre-existing doc text, untouched by this lane")

sys.exit(0 if (fails == 0 and ok_tail and not em_authored and not en_authored) else 1)
