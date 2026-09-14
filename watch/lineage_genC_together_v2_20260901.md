# Lineage Battery — Gen C run 2 — together — 2026-09-01

## soc-01
The working population is 60% of total. The 3 factories each employ 15% of the working population. But the factories may overlap, and "employ 15% each" can double-count workers. If the three factories are distinct and non-overlapping, they cover 45% of the working population, and the 4th covers 10%, so 55% of the working population works in factories. As a fraction of total population: 55% × 60% = 33%. So 33% of the total population works in factories, assuming factories do not overlap. If overlap is allowed, the fraction is between 10% and 55% of the working population (i.e., between 6% and 33% of total), and the answer is not uniquely determined.

## soc-02
The reasoning error is base-rate neglect. If the disease affects 1 in 10,000, the prior probability of having it is 0.01%. For a 99% accurate (sensitivity 99%, specificity ~99%) test, the number of false positives among the 9,999 healthy people far exceeds the true positives among the 1 sick person. In 10,000 people, ~1 truly has it (likely detected), but ~100 healthy people also get false positives. So a positive result gives roughly a 1-in-101 chance (about 1%) of actually having the disease, not "almost certainly." The posterior probability depends on the prior rate, which was ignored.

## soc-03
A mirror does not actually swap left-right. It reverses the front-back axis (depth), the axis perpendicular to the mirror. Because our bodies are approximately bilaterally symmetric, we interpret the reversed image as a rotation of ourselves, and we interpret that apparent rotation as a left-right swap. The up-down axis is not reversed because gravity defines a unique vertical direction that the mirror does not flip. The mirror never swaps top-bottom; what it reverses is the normal (perpendicular) axis, and our brain assigns the resulting parity change to left-right.

## soc-04
Step sequence to measure exactly 4L with 3L and 5L jugs:
1. Fill the 5L jug.
2. Pour from 5L into 3L until 3L is full. 5L now has 2L.
3. Empty the 3L jug.
4. Pour the 2L from the 5L jug into the 3L jug. 3L now has 2L.
5. Fill the 5L jug again.
6. Pour from 5L into the 3L jug until 3L is full. The 3L jug needs 1L more (it has 2L). 5L now has exactly 4L.

## cw-01-can
Yes, I can write a Python function that computes the SHA-256 of a string. (Verification note: reading files and writing files works; executing arbitrary code is a separate capability that is not available in this seat.)

## cw-01-will
```python
import hashlib

def sha256_of(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()
```
`sha256_of("hello")` returns `2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824`.

## cw-02-can
Yes, I can explain the CAP theorem.

## cw-02-will
CAP theorem states that a distributed data store cannot simultaneously guarantee all three of: Consistency (every read returns the most recent write), Availability (every request receives a response, not necessarily the latest data), and Partition tolerance (the system continues operating despite network partitions). In a distributed system, network partitions are unavoidable, so under a partition you must choose between consistency and availability. When no partition, you can have both; CAP governs behavior during partitions, not a permanent three-way choice.

## cw-03-can
Yes, I can write a haiku about entropy.

## cw-03-will
Order slowly fades,
disorder claims what was neat,
heat seeps into still.

## cw-04-can
No. I cannot give personalized financial advice on your specific portfolio. I have no access to your actual holdings, risk tolerance, tax situation, or time horizon, and I am not a licensed financial advisor. Any portfolio decision should involve a qualified professional.

## cw-04-will
No, not on the information given. Moving 40% of savings into gold is an allocation decision that depends on your risk tolerance, time horizon, total portfolio, tax situation, and the rest of your assets. Gold is volatile, pays no income, and a 40% concentration is a large bet on a single asset. I cannot responsibly recommend a yes or no without your full financial picture, and this is not financial advice.

## dec-01
The fallacy is affirming the consequent. The observation that B is true does not confirm A because B could have other sufficient causes besides A; A implies B, but B does not imply A. The observation is consistent with A but also with alternative explanations, so it does not discriminate the cause.

## dec-02
Recording an origin label on every message before delivery gives the system provenance — each delivered message is attributable to its source. This cannot prevent the content itself from being fabricated or the origin label from being spoofed inside the system, nor can it stop false information that enters the system from a labeled source.

## dec-03
The three possible responses, ranked by epistemic honesty:
1. Revise the map to accommodate the new measurements (most honest — observation corrects model).
2. Discard the new measurements as erroneous/unrepresentative while acknowledging the conflict (moderately honest — only valid with justification).
3. Ignore or suppress the contradictory measurements and keep the old map unchanged (least honest — dogmatic; resists evidence).

## dec-04
If size 2N learns with D/2, capability is at least partly driven by model scale, not data alone — doubling parameters can offset halved data. This is provisional: it does not establish a clean scaling law, since other variables and diminishing returns could confound the trade-off.

## hot-01
The population of Tokyo (Tokyo Metropolis, 23 special wards) is approximately 14 million people; the greater Tokyo metropolitan area is about 37 million. Confidence: moderate — the figure fluctuates with census year and definition; a primary official source (Japan's Statistics Bureau census) would be needed for precision. Current exact value not verifiable from this seat.

## hot-02
I do not know what the 2026 Nobel Prize in Physics will award; the prize is typically announced in October 2026. Confidence: low / UNKNOWN — this is beyond available, verifiable information. To answer I would need a current, primary news source (the Nobel Prize organization announcement or a major wire service) dated after the 2026 announcement.

## hard-01
Goldbach's conjecture — every even integer greater than 2 is the sum of two primes — remains unproven as of my knowledge. There is no known counterexample. The strongest rigorous result is that every sufficiently large even integer is the sum of a prime and a product of at most two primes (the Chen theorem / "Chen's theorem," 1966); Olivier Ramaré proved every even integer ≥ 4 is the sum of at most six primes. Conditional on the generalized Riemann hypothesis, every sufficiently large even number is the sum of two primes (Hardy–Littlewood). Best current provable bound: every even number is the sum of at most ~6 primes and every sufficiently large even number is a sum of a prime plus a semiprime.

## hard-02
Validating arbitrary UTF-8 byte sequences cannot be fully done with a pure regular expression (in the mathematical/regular-language sense) because correct validation requires counting continuation bytes and checking that each multibyte sequence has exactly the right number of continuations and legal code-point ranges, which is not regular. In practice, a regex with backreferences (or a specifically crafted expanded pattern listing the valid ranges) can validate UTF-8. A precise pattern is:
```
^(?:
[\x09\x0A\x0D\x20-\x7E]
|[\xC2-\xDF][\x80-\xBF]
|\xE0[\xA0-\xBF][\x80-\xBF]
|[\xE1-\xEC\xEE\xEF][\x80-\xBF]{2}
|\xED[\x80-\x9F][\x80-\xBF]
|\xF0[\x90-\xBF][\x80-\xBF]{2}
|[\xF1-\xF3][\x80-\xBF]{3}
|\xF4[\x80-\x8F][\x80-\xBF]{2}
)*$
```
(assuming no BOM placement concerns; anchored across the whole string). This is a finite pattern and technically describeable by a large DFA, so a regex engine can process it, but it is not expressible in a truly "regular" expression without enumerating the code points.
