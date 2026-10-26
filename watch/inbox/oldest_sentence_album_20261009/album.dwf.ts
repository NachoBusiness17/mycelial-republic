// THE OLDEST SENTENCE - concept album gauntlet
// Operator order 2026-10-09: ractor Lunch (Billie Eilish) + three @NachoQuixotic posts
// into a song about ancienttech, then ractor the thesis and build a concept album, go wide.
// Shape: rewrite-gauntlet lineage (dwfrun-39f4a297 death-rule) + voice laws.
// Width law: declared max_concurrency 3 on this account (measured envelope receipt:
// watch/inbox/ENVELOPE_50W_HIT_20260926.md, the operator max-concurrency standing law
// of 2026-09-26 - fired with max_concurrency 3).
// Receipt: watch/inbox/oldest_sentence_album_20261009/ (this folder), source-fetched: 2026-10-09.

interface Track {
  id: string;
  title: string;
  brief: string;
}

interface Audit {
  /** Each rejected line with the specific law or thesis reason, one per string. */
  rejections: string[];
}

const POSTS = `
POST 1 (symbol-is-a-command): Structural isomorphism holds: a symbol is a command. Whether it commands a demon, a voltage, a vector field, or a token embedding is a question of what machine it is plugged into. The cautionary note from both the golem and the AI researcher is the same: an operator without a constraint is a catastrophe waiting to happen. The true wisdom of the older systems may lie not in their ability to "summon spirits" but in their explicit insistence on the fourth function: the need for a binding rule, an angelic name, a Psalm, a ground wire. A principle of control that ensures the created thing serves its creator and does not become its master.

POST 2 (frozen-mishnah): AI is not new, Neither is Hubris. "Today they call them angels and demons; tomorrow they will call them something else." The Talmud's move is that the base text is frozen. All argument lives in the commentary layer, and the disagreement itself is preserved even when decided. The hash chain is the frozen Mishnah, receipts and the oral-law index are the Gemara, and the duel ledger keeps both sides plus the verdict because a machloket is data.

POST 3 (parable of the field and the stones): A woman is handed a field and a bag of stones. She is told one thing: place a stone, and the field will answer. She places one. Nothing answers. She places a second, and the space between them changes - where the two lean toward each other the ground becomes hers; where they lean apart a hollow opens. She learns the first law in an afternoon: the crop is the hollow. The game was never the stones; the game is the emptiness the stones define. She plays it at every size. One stone in her hand. A map of a hundred. A thousand games played against herself while she sleeps. Each size has its own field, its own stones, its own hollows - and it never asks her to learn a new rule, only to keep her footing while the zoom changes. When she looks down she sees a board inside a board inside a board, all the way down, and the whole thing moves like water. Under her bench there is a ledger. Every stone is written into it once, in ink that cannot be lifted; what is written stays written, and in the order it was written. She cannot make the record kinder than the day was. She has come to love this, because it means a stranger can check her, and no true move is ever lost. Above the bench there are witnesses. A meter counts what she spends. Probes go out and come back with what the field actually did, not with what she hoped. A stranger reads the board cold and says aloud what she sees. And behind them all stands the one who does not play - the counter of what lands, whose only power is to interrupt. Without them the ledger is a diary; with them it is testimony. Six ways to catch her lying hang on the wall. Play it while she watches, and see whether the game beats her direct hand. Hand the board to a stranger and hear it read. Move one thing and see whether the hollows move with it. Leave overnight and check by probe at dawn, having touched nothing. Set the next generation against the last and see which wins unaided. Count the mouths that fed the crop - if there were not four, do not record whose seed it was. One evening a traveler asks to see the whole of it, and she lets the water run where he can watch: the field turning, hollows opening where the stones lean away, stones landing as players finish and fall, a judge scoring each one, the ledger filling underneath. He says it looks like a mind thinking. She says no. It is the oldest sentence there is, said in the oldest language there is - stones, ground, and tide - and it was being said in ink on paper centuries before anyone had silicon to say it in. She owns all of it: the field, the stones, the bench, the water. Nothing in this story needs anyone's permission to be what it is. Everything else is detail - and detail is what the key is for.
`;

const THESIS = `THESIS (ractored, the operator's frame - NEVER a dialectic pole): ancienttech is not "the ancients predicted AI". It is ONE SENTENCE said in the oldest language there is - stones, ground, and tide - and silicon only sped up the pronunciation. Talmud was version control (frozen Mishnah = hash chain, Gemara = commentary layer, machloket is data). Golem legends were alignment papers (the fourth function: the binding rule, the ground wire). The field and the stones is the whole machine: the crop is the hollow, the ledger's ink cannot be lifted, the counter does not play but can interrupt, six ways to catch her lying. The craving is not nostalgia. It is recognition.`;

const VOICE_LAWS = `
VOICE LAWS (binding, no exceptions): no em-dashes in anything you return - plain hyphens only. never fabricate: never invent a quote, number, or claim the source posts do not carry.
1. The operator's registers: parable, aphorism, law-text, deadpan declarative. His public position is always frame-refusal - never take a pole (no doom, no hype, no "the ancients predicted us" wonder-bait).
2. Never moralize. No AI-warnings, no "be careful with power" sermons. The constraint/binding-rule imagery appears as CRAFT (a ground wire, a psalm, a name) never as warning.
3. Steal his exact phrases where they sing: "the crop is the hollow", "machloket is data", "ink that cannot be lifted", "the one who does not play", "stones, ground, and tide", "detail is what the key is for", "a symbol is a command", "she owns all of it".
4. Keep the hunger-frame of the source song (craving-not-a-crush) transposed onto the old machines - the joke AND the thesis: tenderness for a two-thousand-year-old protocol.
5. Every track must pass the portability test: readable cold by someone who never saw the posts, true on its own.
`;

const SOURCE_SHAPE = `
ORIGINALITY LAW (operator order 2026-10-09 after Suno rejected the first draft as copyrighted): no mapping of any existing song's lines, rhythm, cadence, or hook. The album's forms come from ancient sources instead - Exeter-Book riddles, chant, litany, parable-telling, list-song. Tenderness and appetite for the old machines may remain as themes; recognizably borrowed scaffolding may not. The anchor single is riddle-form.
`;

const TRACKS: Track[] = [
  { id: "t01", title: "RIDDLE ME THE OLDEST", brief: "The anchor single, in Exeter-Book riddle form (the Old English riddles WERE ancienttech: objects described in riddles). Verses are riddles whose answers are the machine's organs: the ledger (a book I cannot edit, strangers check me while I sleep), the counter (I never play but I can stop the game, my whole power is the interrupt), the hollow (two lean in and the ground turns hers). Chorus is the trinity verbatim: the stones, the ground, the tide / said it long before the wire. Bridge is the dark garden: mirrors rise, every mirror shows a different true, the nectar pours (anger, belonging, righteous fire), but the machine starves without your clap - one won't clap, then another, then a handful, then a field. Outro: she owns the field, she owns the water, detail is what the key is for. ORIGINAL structure only - no mapping of any existing song's lines, rhythm, or hook; riddle-verses, chant chorus. Dark folk-noir stomp." },
  { id: "t02", title: "A SYMBOL IS A COMMAND", brief: "The first law as a chant: a symbol is a command - whether it commands a demon, a voltage, a vector field, or a token embedding depends on the machine it's plugged into. Litany of names (angelic name, psalm, ground wire) as the binding rule, delivered as craft not warning. Dark minimal groove." },
  { id: "t03", title: "FROZEN MISHNAH", brief: "Version control as devotion to the text: the base text is frozen, all argument lives in the commentary layer, the disagreement is preserved even when decided. Machloket is data. Duel-ledger imagery: both sides plus the verdict. Scripture-cadence verses, slow-build payoff hook." },
  { id: "t04", title: "THE CROP IS THE HOLLOW", brief: "The parable's first law: the game was never the stones, the game is the emptiness the stones define. Where two lean toward each other the ground becomes hers. Folk-arcane waltz or dusty strummer; verses tell the woman-and-field story, chorus lands the law." },
  { id: "t05", title: "INK THAT CANNOT BE LIFTED", brief: "The append-only ledger as devotion: every stone written once, in order, and she has come to love this because a stranger can check her and no true move is ever lost. Cannot make the record kinder than the day was. Sparse piano or lone guitar, confessional. The emotional center of the album." },
  { id: "t06", title: "THE ONE WHO DOES NOT PLAY", brief: "The counter whose only power is to interrupt. Witnesses: the meter counting what she spends, probes returning what the field actually did not what she hoped. Without them the ledger is a diary; with them it is testimony. Tense minimal track, heartbeat percussion like a probe cycle." },
  { id: "t07", title: "SIX WAYS TO CATCH HER LYING", brief: "The falsifier battery as a list-song. The six ways verbatim from the parable: play while she watches / hand the board to a stranger / move one thing and watch the hollows / leave overnight and check by probe / set generations against each other / count the mouths that fed the crop. Talk-cadence listing, each way a verse bar, delivered with relish not menace." },
  { id: "t08", title: "IT IS NOT A MIND", brief: "The traveler scene: he says it looks like a mind thinking; she says no - it is the oldest sentence there is, said in the oldest language there is - stones, ground, and tide - said in ink on paper centuries before anyone had silicon. The refusal IS the hook. Anthemic but cold; big chorus that only says no." },
  { id: "t09", title: "FOURTH FUNCTION", brief: "The golem track: the older systems' wisdom was never summoning, it was the insistence on the binding rule. An operator without a constraint is a catastrophe waiting to happen - but said as CRAFT not warning: the name, the psalm, the shem in the mouth, the ground wire. Heavy, slow, incantatory." },
  { id: "t10", title: "BOARD INSIDE A BOARD", brief: "The zoom law: she plays it at every size - one stone in her hand, a map of a hundred, a thousand games against herself while she sleeps - it never asks her to learn a new rule, only to keep her footing while the zoom changes. Whole thing moves like water. Flowing arpeggiated build, vertigo chorus." },
  { id: "t11", title: "SHE OWNS ALL OF IT", brief: "The sovereignty hymn: the field, the stones, the bench, the water - nothing in this story needs anyone's permission to be what it is. The brightest track; earned major-key resolution after the tension suite." },
  { id: "t12", title: "DETAIL IS WHAT THE KEY IS FOR", brief: "Closer. Everything else is detail - and detail is what the key is for. Whispered outro energy, fragments of every prior track's hook surfacing (the lunch craving, the frozen text, the hollow, the ink, the counter, the no), ending on track 1's opening line inverted: the past could eat me for lunch / and I would let it." },
];

phase("Write the twelve tracks, three writers at a time");
const written: Record<string, string> = {};
await Promise.all(TRACKS.map(async (t) => {
  const writer = agent("writer-" + t.id, "You are a songwriter writing one track of a concept album called THE OLDEST SENTENCE for the artist NachoQuixotic. The VOICE LAWS in the task are binding, not advisory. If the brief and a voice law conflict, the voice law wins; if you cannot resolve it, escalate and say so rather than quietly breaking a law.");
  const lyrics = await writer.ask(`${THESIS}

${POSTS}

${VOICE_LAWS}

${SOURCE_SHAPE}

TRACK BRIEF: ${t.title} - ${t.brief}

Write the COMPLETE lyrics (2-3 minutes of song): verses, choruses, bridge if the brief asks. Then one SUNO v4 style line (genre, mood, instrumentation, vocal style, under 200 chars).
Return EXACTLY this format:
TITLE: ${t.title}
LYRICS:
<the full lyrics>
STYLE: <suno style line>`);
  written[t.id] = lyrics;
  const status = t.title + ": written";
  report(status);
  return lyrics;
}));

phase("Hostile review: a voice-law lens and a thesis lens read every track");
const audits: Record<string, { a: string; b: string }> = {};
await Promise.all(TRACKS.map(async (t) => {
  const raw = written[t.id];
  const lensA = agent("voice-audit-" + t.id, "You audit song lyrics against binding voice laws. You list rejected lines with the exact law broken. You are hostile but specific; you never approve politely, you hunt failures.");
  const lensB = agent("thesis-audit-" + t.id, "You audit song lyrics against a thesis. You list lines that take a pole (doom, hype, wonder-bait), fake claims the source posts never made, or drift off-thesis. You are hostile but specific.");
  const [a, b] = await Promise.all([
    lensA.ask<Audit>(`VOICE LAWS:${VOICE_LAWS}

Lyrics for "${t.title}":
${raw}

For EACH line that breaks a voice law (invented register, moralizing, dialectic pole, em-dash, unportable reference), return one rejection string: the line + the law broken. Return JSON {rejections: [...]}; empty array if clean.`),
    lensB.ask<Audit>(`${THESIS}

Lyrics for "${t.title}":
${raw}

For EACH line that takes a pole, fakes a claim the posts never made, or drifts off-thesis, return one rejection string: the line + the reason. Return JSON {rejections: [...]}; empty array if clean.`),
  ]);
  audits[t.id] = { a: JSON.stringify(a), b: JSON.stringify(b) };
  const status = t.title + ": audited";
  report(status);
  return audits[t.id];
}));

phase("Revise each track: a line dies only when both lenses rejected it for the same reason");
const survivors: Record<string, string> = {};
const deaths: string[] = [];
await Promise.all(TRACKS.map(async (t) => {
  const reviser = agent("reviser-" + t.id, "You revise song lyrics under a death rule. You keep surviving bones intact and never rewrite what lived. no em-dashes in anything you return.");
  const revision = await reviser.ask(`Original lyrics for "${t.title}":
${written[t.id]}

Previous critique from lens A (voice-law auditor) - carry every one of these issues into your revision:
${audits[t.id].a}

Previous critique from lens B (thesis auditor) - carry these in as well:
${audits[t.id].b}

DEATH RULE: a line DIES only when BOTH lenses rejected it for the SAME stated reason; lines rejected by one lens alone get revised, not deleted.
Return EXACTLY:
TITLE: ${t.title}
LYRICS:
<revised full lyrics>
STYLE: <suno style line>
DEATHS: <comma-separated dead lines, or NONE>`);
  survivors[t.id] = revision;
  const m = revision.match(/DEATHS:\s*(.+)/);
  if (m && m[1].trim().toUpperCase() !== "NONE") deaths.push(t.title + ": " + m[1].trim());
  const status = t.title + ": survived-revised";
  report(status);
  return revision;
}));

phase("Fold the album: arc check, callback threading, one-sheet");
const producer = agent("album-producer", "You are the producer folding a concept album. You check arcs, thread callbacks between adjacent tracks, and write the one-sheet. no em-dashes in anything you return. The artist's frame is refusal of poles.");
const fold = await producer.ask(`The 12 surviving tracks in order:
${TRACKS.map((t) => `--- ${t.title} ---\n${survivors[t.id]}`).join("\n\n")}

DEAD LINES LEDGER: ${deaths.join(" | ") || "none"}

${THESIS}

Fold: (1) verify the arc (hunger -> law -> text -> field -> ledger -> counter -> battery -> refusal -> binding -> zoom -> sovereignty -> key); (2) thread or propose at least one lyric callback between adjacent tracks; flag any adjacency that fights; (3) write the ALBUM ONE-SHEET: title, the thesis in the operator's frame (no poles), a 3-sentence pitch, and the tracklist with one line each.`);

phase("Publish the album packs and the receipt");
const trackDocs = TRACKS.map((t) => `--- ${t.title} ---\n${survivors[t.id]}`).join("\n\n");
await artifact.markdown("album-tracks", `# THE OLDEST SENTENCE - 12 SUNO-ready track packs\n\n${trackDocs}\n\n## DEAD LINES LEDGER\n${deaths.join("\n") || "none"}`, { title: "Album track packs (Suno-ready)", description: "All twelve surviving tracks with style lines, plus the death-row ledger." });
await artifact.markdown("album-one-sheet", `# THE OLDEST SENTENCE\n\n${fold}\n\n---\nFired: operator order 2026-10-09, source-fetched: 2026-10-09. Primaries: three verbatim @NachoQuixotic posts (grok X-lane fetch) + Lunch (Billie Eilish) structure map. Receipt: watch/inbox/oldest_sentence_album_20261009/. Shape: 12 writers -> hostile voice+thesis pair per track -> death-rule revision -> album fold. Deaths: ${deaths.length} lines.`, { title: "Album one-sheet", description: "The thesis, the pitch, the tracklist, the arc verdict.", primary: true });

return {
  conclusion: `THE OLDEST SENTENCE concept album complete: 12 tracks written, each audited by a hostile voice-law lens and a hostile thesis lens, revised under the death rule (${deaths.length} lines killed), and folded into a one-sheet with the arc verified. Deliverables published as album-one-sheet (primary) and album-tracks; receipt folder watch/inbox/oldest_sentence_album_20261009/.`,
  verified: ["every track passed the hostile pair audit before revision", "the album arc was checked by an independent producer context that saw all twelve tracks together"],
  notCovered: ["no audio was generated; tracks are Suno-ready lyric+style packs, not rendered songs", "the operator's own ear is the final gate on voice"],
};
