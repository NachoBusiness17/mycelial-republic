"""Receipts for the Lyapunov + dimension-lift decode (2026-09-21).

Source post: x.com/omarsar0/status/2102099298716660223 (text pasted by operator,
plus 4 images: coordinate-geometry sheet, coordinate-transforms sheet, calc
tables, and a worked contour integral by J. Chris Juravich dated 2026-09-20).

Pure stdlib. Run with the estate venv python, never bare python.
"""
import datetime
import math
from fractions import Fraction


def simpson(f, a, b, n=200000):
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += f(a + i * h) * (4 if i % 2 else 2)
    return s * h / 3


print("== RECEIPT 1: contour integral I = int_0^inf ln x/(6x^2+2x+20) dx ==")
# Split at 1, map the tail x=1/t; then x=e^{-u} on each [0,1] piece so the log
# singularity becomes a smooth decaying integrand.
def piece_lo(u):
    e = math.exp(-u)
    return (-u) * e / (6 * e * e + 2 * e + 20)


def piece_hi(u):
    e = math.exp(-u)
    return u * e / (20 * e * e + 2 * e + 6)


I_num = simpson(piece_lo, 0, 40) + simpson(piece_hi, 0, 40)
L = 0.5 * math.log(10 / 3)
theta = math.atan(math.sqrt(119))
I_sheet = theta / (2 * math.sqrt(119)) * math.log(10 / 3)          # sheet's box
I_alt = (math.sqrt(10 / 3) / 20) * L * math.acos(1 / (2 * math.sqrt(30))) / math.sqrt(1 - 1 / 120)
print(f"numeric quadrature  I = {I_num:.10f}")
print(f"sheet closed form   I = {I_sheet:.10f}")
print(f"independent closed  I = {I_alt:.10f}")
print(f"|numeric - sheet| = {abs(I_num - I_sheet):.2e}")


print()
print("== RECEIPT 2: lozenge TILINGS of the side-n hexagon (MacMahon) ==")
for n in range(1, 5):
    p = Fraction(1)
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            for k in range(1, n + 1):
                p *= Fraction(i + j + k - 1, i + j + k - 2)
    print(f"n={n}: tilings = {int(p)}   (n^3 would be {n**3})")


print()
print("== RECEIPT 3: rhombi of ALL sizes drawn in the side-n hexagon grid ==")
# Hexagon vertices (i,j): (0,0),(n,0),(n,n),(0,2n),(-n,2n),(-n,n). Convex, so a
# rhombus lies inside iff its 4 vertices do. Grid directions d1=(1,0),
# d2=(0,1), d3=(1,1) in (i,j) coords; a grid rhombus has side k along two
# distinct directions.
def inside(i, j, n):
    return 0 <= j <= 2 * n and -n <= i <= n and 0 <= i + j <= 2 * n


# The three 60-degree lattice directions in (i,j) coords are (1,0),(0,1),(-1,1);
# in Cartesian P(i,j)=(i+j/2, sqrt3*j/2) these are (1,0),(1/2,sqrt3/2),(-1/2,sqrt3/2).
# NOTE: (1,1) is NOT a grid direction (Cartesian length sqrt3, 30 degrees).
dirs = [(1, 0), (0, 1), (-1, 1)]
for n in range(1, 7):
    total = 0
    per_k = {}
    for a in range(3):
        for b in range(a + 1, 3):
            dA, dB = dirs[a], dirs[b]
            for k in range(1, n + 1):
                for i in range(-2 * n, 2 * n + 1):
                    for j in range(-2 * n, 2 * n + 1):
                        if (inside(i, j, n)
                                and inside(i + k * dA[0], j + k * dA[1], n)
                                and inside(i + k * dB[0], j + k * dB[1], n)
                                and inside(i + k * (dA[0] + dB[0]), j + k * (dA[1] + dB[1]), n)):
                            total += 1
                            per_k[k] = per_k.get(k, 0) + 1
    # closed form derived by hand for the pair ((1,0),(0,1)); same count per pair:
    # per-pair count(k) = m(3m+1) + (k+1)(2m+1) with m = n-k
    pred = sum(3 * (m * (3 * m + 1) + (n - m + 1) * (2 * m + 1)) for m in range(n))
    print(f"n={n}: counted {total:4d}  per-k {per_k}  |  closed-form {pred:4d}  n^3 = {n**3}")


print()
print("== RECEIPT 4: high-dim orthogonality, E|cos| = Gamma(d/2)/(sqrt(pi) Gamma((d+1)/2)) ==")
for d in (2, 3, 8, 64, 512, 4096):
    ex = math.exp(math.lgamma(d / 2) - math.lgamma((d + 1) / 2)) / math.sqrt(math.pi)
    print(f"d={d:5d}: E|cos| = {ex:.6f}   sqrt(2/(pi d)) = {math.sqrt(2 / (math.pi * d)):.6f}")


print()
print("== RECEIPT 5: damped pendulum, V = w^2 + 2(1-cos th) + eps*w*sin(th) ==")
c, eps = 0.4, 0.3


def Vdot(th, w):
    return (-2 * c * w * w + eps * w * w * math.cos(th)
            - eps * c * w * math.sin(th)
            - eps * w * math.sin(th) ** 2
            - eps * math.sin(th) ** 2)


def V(th, w):
    return w * w + 2 * (1 - math.cos(th)) + eps * w * math.sin(th)


mx = -1e9
mx_off = -1e9
arg_off = None
mnV = 1e9
N = 401
for i in range(N):
    th = -math.pi + 2 * math.pi * i / (N - 1)
    for j in range(N):
        w = -3 + 6 * j / (N - 1)
        vd = Vdot(th, w)
        v = V(th, w)
        if vd > mx:
            mx = vd
        # exclude ALL standing points of Vdot: the target equilibrium (0,0) and
        # the inverted one at (+/-pi, 0) — Vdot vanishes at both
        if (abs(th) > 0.05 and abs(w) > 0.05) and vd > mx_off:
            mx_off, arg_off = vd, (round(th, 3), round(w, 3))
        if v < mnV:
            mnV = v
print(f"c={c}, eps={eps}, grid {N}x{N} on [-pi,pi]x[-3,3]")
print(f"max Vdot (whole grid)        = {mx:.6f}   (0 only at the two equilibria)")
print(f"max Vdot (off equilibria)    = {mx_off:.6f} at (th,w)={arg_off}")
print(f"min V on grid                = {mnV:.6f}   (positive = valid energy)")
print("V(+/-pi, 0) =", V(math.pi, 0.0), " (the standing point is NOT the minimum)")


print()
print("== RECEIPT 6: source post id decoded as X snowflake ==")
sid = 2102099298716660223
ts_ms = (sid >> 22) + 1288834974657
print(datetime.datetime.utcfromtimestamp(ts_ms / 1000).strftime("%Y-%m-%d %H:%M:%S UTC"))
