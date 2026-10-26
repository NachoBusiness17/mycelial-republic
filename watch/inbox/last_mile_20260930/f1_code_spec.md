Write ONE Python 3.11 file (standard library only, no third-party imports) implementing a small CLI tool called duelsum. It summarizes a JSONL ledger of model-duel rows.

INPUT: run as `python <yourfile> <path-to-jsonl>`. Each non-blank line of the file is a JSON object with these fields:

- ask_id: string
- a_model: string
- b_model: string
- winner: "A", "B", "TIE", or "UNPARSED"
- criteria: list of objects {"criterion": string, "a": int, "b": int} (may be missing, null, or empty)
- a_chars: int
- b_chars: int

A line is VALID only if it parses as JSON and contains non-missing a_model, b_model, winner, a_chars, b_chars. Invalid lines (unparseable JSON, or missing any of those five fields) are skipped from every metric.

OUTPUT CONTRACT (stdout, exact grammar, no other output, no logging, exit code 0 always):

1. For each distinct (a_model, b_model) pair that has at least one valid row, pairs sorted ascending by (a_model, b_model), one line:
   WINS|<a_model>|<b_model>|<count of that pair's valid rows with winner A>|<count with winner B>|<count with winner TIE>
   Rows with winner UNPARSED count toward none of these three.
2. For each pair, same ordering, one line:
   AVGCHARS|<a_model>|<mean of a_chars>|<b_model>|<mean of b_chars>
   Means are over ALL valid rows of the pair including UNPARSED rows. Print each mean with exactly one digit after the decimal point (for example 116.7 or 150.0).
3. One line, only if at least one valid row anywhere has a non-empty criteria list:
   CRITAGREE|<number of individual criteria entries where a equals b>|<total number of criteria entries>|<ratio printed with exactly two digits after the decimal point, e.g. 0.50 or 0.67>
4. Always exactly one final line:
   ROWS|<number of valid rows>

EDGE CASE: if the path is missing, unreadable, or the file has zero valid rows: print ONLY the line `ROWS|0` and exit 0 (no WINS, AVGCHARS, or CRITAGREE lines).

WORKED EXAMPLE. Given this file:

{"ask_id": "d1", "a_model": "m-a", "b_model": "m-b", "winner": "A", "criteria": [{"criterion": "cov", "a": 5, "b": 4}], "a_chars": 100, "b_chars": 200}
{"ask_id": "d2", "a_model": "m-a", "b_model": "m-b", "winner": "TIE", "criteria": [{"criterion": "cov", "a": 3, "b": 3}], "a_chars": 200, "b_chars": 200}
{"ask_id": "d3", "a_model": "m-a", "b_model": "m-b", "winner": "UNPARSED", "a_chars": 50, "b_chars": 50}

the complete and only output must be:

WINS|m-a|m-b|1|0|1
AVGCHARS|m-a|116.7|m-b|150.0
CRITAGREE|1|2|0.50
ROWS|3

The tool will also be run on hidden fixtures exercising: empty file, unparseable lines, rows missing required fields, empty/missing criteria, UNPARSED winners, and multiple model pairs with pair-ordering requirements.

OUTPUT FORMAT of your reply: reply with ONLY the complete Python file content, no prose before or after, no markdown fences. The file must be directly runnable.
