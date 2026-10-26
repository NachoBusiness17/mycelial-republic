# FIRST BOOT — for a stranger holding this seed

You are holding a method, not a product. It is small on purpose. Here is your first hour.

0. **Verify the package:** `python verify_seal.py` — every file must check out.
   (Linux/macOS: `sha256sum -c MANIFEST.sha256` works too.)
1. **Read THE_METHOD.md** (one page, 11 laws). You will violate some of them in your first
   week. That is what the meters are for. See SETUP.md for requirements (Python 3.9+, matplotlib optional).
2. **Run the smith chart on nothing:** `python engines/estate_smith_chart.py --no-plot` —
   it will tell you honestly that you have no records yet (every organ prints DARK). That is
   your zero state. Gamma = 1 is normal.
3. **Declare your keys:** copy an entry in `configs/keys.json` per provider lane you use
   (a template entry with the schema is already there), put the actual keys in `.env` or your
   environment, then `python engines/key_law.py --audit` — it exits 0 when every live key is
   declared, and fails loud naming any key that is not.
4. **Index what you have:** `python engines/spine_walk.py <your-folder>` walks YOUR folder
   (pass the path; it defaults to where you run it) and writes one JSONL line per file, then
   `python engines/estate_atlas.py <your-folder>` turns that index into the atlas. The index
   regenerates — it is never hand-maintained.
5. **Start one record.** Markdown, append-only, receipted: who, when, where, evidence. A claim
   not in a record didn't happen.
6. **Schedule the cooker:** `python engines/cooker.py status` shows every free-lane reset and
   its countdown; `python engines/cooker.py fire --due` burns whatever has refilled. Put that
   command on an hourly timer (cron/schtasks) and your compute burns by default, not by willpower.
7. **Answer the daily question:** did the meters move? If a meter can't move, you built prose,
   not a meter. Delete it and build the meter.

The goal is not to reproduce the original estate. It is to grow YOUR estate under THESE laws.
The laws are the method; everything else is your version of it.
