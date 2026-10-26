"""m16-traject quote probe: byte-verbatim subspan checks for the 5 mined quotes
plus the width-note line. Reads source bytes, counts exact UTF-8 occurrences,
and reports em-dash (U+2014) count inside each subspan. Raw output is appended
to m16-traject.check.txt by the invoking shell command."""
from pathlib import Path

PROBES = [
    ("q1", r"C:/Users/foste/Desktop/New folder/traject.txt",
     "it's all training data. We're learning for free. This is fucking incredible data if we treat it as such."),
    ("q2", r"C:/Users/foste/Desktop/New folder/traject-chinesedebug.txt",
     "The same weakness recurs at every scale: the record is append-only but nothing declares its own death. Sediment needs a pulse."),
    ("q3", r"C:/Users/foste/Desktop/New folder/traject-chinesedebug.txt",
     "three strata (Nov-04, Jan-05 body, Mar-09) and the 1.3M number are still claims wearing receipt clothes; fetch them before calling the canon closed."),
    ("q4", r"C:/Users/foste/Desktop/New folder/traject.txt",
     'python.exe launched, got "-File" as an option, printed usage to stderr (captured now), exited.'),
    ("q5", r"C:/Users/foste/Desktop/New folder/traject.txt",
     "122.4M in \u2192 0.5M out = 240:1. That's the re-feed tax live, today, on the free plan."),
    ("q6", r"C:/Users/foste/Desktop/New folder/traject-chinesedebug.txt",
     "haha 20 seems to be the limit"),
]

for name, path, needle in PROBES:
    data = Path(path).read_bytes()
    nb = needle.encode("utf-8")
    n = data.count(nb)
    verdict = "VERBATIM" if n >= 1 else "MISSING"
    print(f"{name}: count={n} emdash_in_subspan={needle.count(chr(0x2014))} "
          f"subspan_bytes={len(nb)} verdict={verdict} file={path}")
