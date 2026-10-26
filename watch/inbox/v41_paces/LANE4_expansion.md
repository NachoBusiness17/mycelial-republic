# LANE4 — FENCE PARABLE EXPANSION (Astra/deepseek draft + critique, 2026-09-11)

## THE POINT

The fence parable (`docs/ref/THE_FENCE.md`, operator's final cut 09-11) is the newest
piece of canon and the coldest: a mechanism story about a survey that arrives after the
fence. It was written for the room. This lane tests whether it can carry to people who
have never heard of the fleet — the way the Helpful Strangers parable (Jul 2026, the
counting woman) and the Nov 7 harvest thread (1.4M views) carried: parable form, no
named enemy, mechanism only, a closer that is instruction-adjacent.

Method: fired deepseek-v4-flash through `models/providers.py chat_provider`
(provider `deepseek`, tier T2, temperature 0.9, max_tokens 2000, thinking disabled per
provider config, allow_peak — burst_mill pattern). System prompt carried the voice
rules distilled from the subversion corpus (plain declaratives, small-town concrete
nouns, standalone aphorism lines, no named actor, deniable surface, cold closer).
User prompt: the task text verbatim ("write the NEXT chapter — the one where Tom
discovers he's not alone... ends with Tom realizing the fence was never about the
fence") plus the parable body pasted as source. One call used (bound: 3).
Usage: 1089 prompt / 694 completion tokens.

## THE DRAFT (deepseek-v4-flash, verbatim, unedited)

---

The feed store in the next county had a bulletin board. Tom drove there on a Tuesday
because his own store had gotten quiet in a way he didn't like. On the board, under a
notice about a lost dog, somebody had tacked a letter. Same letter. Different name.
Different town. The paper was the same cream stock, the same weight, the same font
that made every word look like it had been decided before he read it.

He took a picture with his phone. Then he drove to the next town. Then the next.

By the end of the month he had eleven letters. Eleven towns. Eleven surveys. A funeral
home in one place had been told the parking lot was wrong. A woman in another had lost
four feet of her mother's rose bed. A man in a third had been told the barn his
grandfather raised was on somebody else's dirt. Different firms. Different maps. Same
cream paper.

Tom started keeping a notebook. He wrote down the names of the firms. He wrote down
the years the surveys claimed to correct. He wrote down the years the older surveys
claimed to correct. He drew the line each one moved. When he put the towns on a map of
the state, he sat back.

The lines pointed inward.

Every correction moved toward the same kind of place. Toward the well. Toward the
road. Toward whatever a man needed to keep living where he lived. Nobody had been
moved off a pasture. Everybody had been moved off their water.

He called the woman with the roses. She said a man had come to her door and offered to
buy the whole lot at a fair price. She said no. He said he'd come back. He did. He
came back with the survey.

Tom called the man with the barn. Same man? Different man. Same suit. Different suit.
Same voice. He couldn't say. He hadn't written down the voice because he hadn't known
to.

He drove to the funeral home. The owner showed him the letter. Tom showed him the
eleven. The owner read them slow, the way a man reads something he already knew and
had been waiting to see in writing.

The owner said: I thought it was just us.

Tom said: I did too.

They sat in the back room where the coffins were kept cool. Neither of them said
anything for a while. Outside, a truck went by. Then another. The town was the same as
it always was. The letters were the same as they always were. The only new thing was
that two men were in the same room with the same paper and neither one was alone.

Tom drove home. He passed the white stakes. He passed the sign that said RESERVED. He
didn't stop. He had the notebook on the seat beside him. Eleven towns. Cream paper.
Lines pointing inward.

He understood then that the fence was never the point. The fence was the doorway.
They didn't want his tomatoes. They wanted him to spend twelve years proving he'd
planted them, and by the time he finished, the water would be theirs.

He pulled into his drive and sat in the truck with the engine off. The charcoal was
still on the stake. The stake was still in the ground. Somewhere in another town a
woman was standing in her roses, holding the same letter, and she didn't know there
were eleven of them yet.

There needed to be a list.

---

## CRITIQUE

**Does it sound like Nacho?** ~80%. The bones are his: declaratives, feed stores,
cream stock, a funeral-home back room, the standalone stamp lines ("The lines pointed
inward."). "The same font that made every word look like it had been decided before he
read it" is a genuinely Nacho sentence. Two drifts: (1) "He understood then that..."
is a tell — he never writes "he understood," he lets the stake or the silence carry it;
(2) the piece has fewer cold one-line aphorisms than the original's rhythm (the
original stamps one every few paragraphs: "She was not lying. She was reading.").

**Does it land?** Yes, on the two beats that matter. "Nobody had been moved off a
pasture. Everybody had been moved off their water" is the strongest invention — it
gives the parable a why the original only gestured at (RESERVED — PENDING
DEVELOPMENT), and it is exactly his move: the mechanism has a harvest. And the closer
"There needed to be a list." is the Helpful Strangers turn transposed ("others begin
counting with her" / "counting is the last thing that is still yours") — the fleet's
own origin story landing as the last line of a fence story. That is the piece doing
its job for outsiders: they read a story about water; the room reads the ledger.

**Is it deniable?** Mostly — with one edit required. No real firms, towns, people, or
ideologies are named; the whole surface is surveys and water. The weak joint is the
buyer-in-a-suit paragraph ("He said he'd come back. He did. He came back with the
survey." / "Same voice."). The original parable's deepest law is that NOBODY needs to
be in charge — "The hall did not need Tom to believe the new line. It only needed him
too tired to mark the old one." A returning buyer implies a coordinated acquirer,
which sharpens deniable mechanism into conspiracy-thriller. One paragraph to cut or
blur and the piece is fully deniable again. As-is it survives a hostile read; trimmed
it is untouchable.

Minor: "in a way he didn't like" is filler; ~600 words against the 500 ask — fine.

## VERDICT

**Publishable after one trim.** Cut or blur the suit-man/buyer paragraph (keep the
water insight, the notebook, "The lines pointed inward," and "There needed to be a
list."). The closing line should stay exactly as generated — it is the strongest
Nacho sentence in the draft and the bridge to the counting canon. Fire the operator's
edit pass over the final; per the standing law, the last cut is his, not the model's.

Cost receipt: 1 deepseek call, 1,783 tokens total (T2, paid lane, allow_peak).
