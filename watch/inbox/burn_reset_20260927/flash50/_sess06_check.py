import io, re, sys
p = r"watch/inbox/burn_reset_20260927/flash50/sess-06.md"
t = io.open(p, encoding="utf-8").read()
# briefing line = the single line inside the first fenced block
m = re.search(r"```\n(.+?)\n```", t, re.S)
brief = m.group(1)
print("brief_chars=%d" % len(brief))
print("brief_le500=%s" % (len(brief) <= 500))
em = t.count("\u2014"); en = t.count("\u2013")
print("em_dash=%d en_dash=%d" % (em, en))
