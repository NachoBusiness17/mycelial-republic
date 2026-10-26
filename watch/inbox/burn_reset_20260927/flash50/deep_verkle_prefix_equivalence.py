"""deep-verkle-formal: property check that _merkle_prefix_roots is byte-exact
equivalent to recomputing _merkle_root over every prefix, on adversarial
shapes (powers of two, powers minus one, odd lengths, single leaf)."""
import random
import sys

sys.path.insert(0, r"C:\Users\foste\Documents\projects\local_sovereign_agent")
from mag.verkle_knot import _merkle_prefix_roots, _merkle_root, _h

rng = random.Random(20260928)
lengths = sorted({1, 2, 3, 4, 7, 8, 15, 16, 17, 31, 33, 63, 64}
                 | {rng.randint(1, 200) for _ in range(12)})
fails = 0
for n in lengths:
    hashes = [_h(bytes([rng.randrange(256) for _ in range(8)]) + str(i).encode())
              for i in range(n)]
    pref = _merkle_prefix_roots(hashes)
    for k in range(1, n + 1):
        if pref[k - 1] != _merkle_root(hashes[:k]):
            fails += 1
            print("MISMATCH at n=", n, "prefix k=", k)
            break
print("shapes_tested:", len(lengths), "lengths:", lengths)
print("prefix_equivalence_failures:", fails)
empty = _merkle_prefix_roots([])
print("empty_prefix_roots:", empty)
print("empty_root_sentinel:", _h(b"empty"))
