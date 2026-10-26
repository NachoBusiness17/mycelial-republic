# grokbot-resonance lane: byte-verify mined quotes are verbatim substrings of estate files
# run: .venv/Scripts/python.exe <this file>; exit 0 = all quotes byte-present
import sys, io

ROOT = r"C:/Users/foste/Documents/projects/local_sovereign_agent"

Q = [
    (
        "Q1 convergence-compression (dash-free span)",
        ROOT + "/watch/inbox/GROKBOT_ANDROID_CONVERGENCE_20260921.md",
        "The diagram's contribution\nis not novelty; it is COMPRESSION: it names the three places our surface is\nfragmented or broken.",
    ),
    (
        "Q2 broker-unification",
        ROOT + "/watch/inbox/GROKBOT_ANDROID_CONVERGENCE_20260921.md",
        "orchestrator + effect_broker + covenant + evidence\n   register under one owner with one contract. The diagram's \"owns task state,\n   permissions, budgets and evidence\" is the spec line. Largest delta; needs a\n   design pass, not a hack.",
    ),
    (
        "Q3 android-loop",
        ROOT + "/watch/inbox/GROKBOT_ANDROID_CONVERGENCE_20260921.md",
        "MagRemote exists; the submit\u2192broker\u2192back-brief leg is\n   broken by the update and netlify auth is owed. Fixing this converts the diagram\n   from proposal to standing organ.",
    ),
    (
        "Q4 harnesses-with-jobs (dash-free span)",
        ROOT + "/watch/FLEET_STRUCTURE_20260901.md",
        "**harnesses with jobs**: dedicated seat, named role, standing budget, standing job, durable handoff.",
    ),
    (
        "Q5 hireable-workers",
        ROOT + "/watch/INTAKE_GROKBOT_BLAST_RADIUS_20260904.md",
        "\"SpaceXAI\" shipped five hireable Grok Bot workers for $200/month; docs state all five run on ONE computer",
    ),
]

fail = 0
for name, path, quote in Q:
    with io.open(path, "r", encoding="utf-8") as f:
        text = f.read()
    ok = quote in text
    words = len(quote.replace("\n", " ").split(" "))
    print("%s %s (%d whitespace-tokens) source=%s" % ("BYTE-OK  " if ok else "BYTE-FAIL", name, words, path))
    if not ok:
        fail += 1

print("QUOTE-CHECK fail-count=%d" % fail)
sys.exit(1 if fail else 0)
