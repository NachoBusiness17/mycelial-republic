# LYRIC ARCHAEOLOGY: what the music-ai canon actually sings, and how it compresses a story

Lane: archaeology (division B), gala lyric-workover 2026-10-01.
Corpus: `C:/Users/foste/Desktop/music-ai` (110 mp3 files, 51 artists; artist map byte-checked by the
taxonomy lane: `watch/inbox/gala_20260925/music-ractor/lanes/taxonomy.check.txt`).
Method: 24 Genius lyric pages fetched live this session via WebFetch (22 in-folder tracks + 2
ask-named tracks absent from the folder; register in section 3). Every
structural number below (distinct-line counts, repetition counts, words per line, person, tense) comes
from those fetched pages as summarized by the fetcher. Short quotes are under 40 words each, copied
from the fetch output; the fetcher declined full-text transcription, so counts and structure are the
evidence, not verbatim full lyrics.
Sibling deliverables: audio layer `watch/inbox/music/STYLE_SPEC.md`, remix layer
`watch/inbox/music/remix-mechanics.md`, tag layer `watch/inbox/music/taxonomy.md`. This file is the
canon's lyric layer, same role for words that STYLE_SPEC is for sound.

## 0. Honest gaps, named up front

- The operator's 14-line riddle prose itself was NOT found on disk. Searched: `watch/inbox/`
  (including all gala_20260925 subfolders), `memory/`, `state/`, `queue/`, desktop music folder. The
  only hits for "14 lines" were false positives (`mag/self_audit.py`, 314 lines). The compression
  study therefore measures against the ask's own spec of the riddle: 14 lines, clock, stakes,
  reversal, exit line. If the riddle text exists only in the orchestrator's ask stream, the composer
  lane should diff this file's prescriptions against the actual text.
- Ask named Phoenix as a canon voice: no Phoenix track exists in the folder (taxonomy's 51-artist
  table has no Phoenix row). Phoenix was not fetched as folder evidence.
- Ask named "one more night": read as Daft Punk "One More Time" (not in the folder either; fetched
  anyway as ask-named canon, flagged below).
- Ask named "dance with trouble": could not map this to any folder track or canon track. Unresolved.
- Ask named "losing my edge" (LCD Soundsystem): NOT in the folder (LCD's 6 folder tracks are other
  songs). Fetched anyway as ask-named canon, flagged below.

## 1. THE LYRIC GRAMMAR (24 tracks fetched, 22 of them in-folder)

### 1.1 Themes: five things this genre sings about

1. **The night is the whole world.** The club, the party, the house, the after-party are complete
   settings; nothing outside them needs to exist. Evidence: TTHHEE PPAARRTTYY's three stanzas are
   prep, club, hotel after-party and nothing else; Daft Punk Is Playing at My House compresses an
   entire social order into one basement (bus, trailer, beer cases, furniture moved, neighbors
   unable to call police, jocks locked out); DVNO is one man vs one doorman; E Talking is one
   party's descent into estrangement.
2. **Repetition as ecstasy, sung about openly.** The canon is self-aware about looping: Over And
   Over's thesis line is "The joy of repetition really is in you" and the song loops; One More Time's
   title phrase appears 30+ times as the celebration itself; Around the World is one phrase 144
   times. The form is the content: a loop you love is a life you accept.
3. **Human vs machine, and the wish to be replaced.** HBFS is self-optimization as vocoder chant
   ("work it harder, make it better"); Strict Machine is a love song to a device that rewards
   obedience with euphoria (fetched bio: rat-brain stimulation experiments); Huarache Lights' refrain,
   repeated 12 times, asks to be swapped out for better-performing machines. The machine voice is not
   a threat in this canon, it is an aspiration and a fear at once.
4. **Losing yourself at 3am.** E Talking's chorus separates the speaker from his own behavior: he is
   not talking to the person, he is talking to the drug. Get Innocuous asks eight times whether
   normalizing yourself is the same as feeling alive. Losing My Edge dissolves a whole identity into
   credential lists that only prove the anxiety. Heartbeats refuses heaven's help for one night of
   forbidden intensity.
5. **Time, aging, and death under the mirror ball.** All My Friends runs one night and one whole life
   on top of each other (aging, "this could be the last time", regret without repentance); Someone
   Great delivers a death by phone call and then watches the coffee and weather not change; Boy From
   School ends childhood in one line and never finds the way back; Heartbeats compresses a romance
   into a count: ten days.

What it sings about, in one line: being human at 3am, transformation under pressure (crystallize,
work it, replace me with a machine), repetition as the price and the payload, and losing yourself on
purpose.

### 1.2 Person and tense (measured across the 24 fetches)

- **Dominant mode: I/you, present tense.** 21 of the 22 in-folder tracks run on present tense as
  their frame; Around the World goes further and carries no pronoun at all. Evidence: DVNO (I vs the
  doorman, present), Ready For The Floor (I/we to you, anxious now), Crystalised (I/you, present
  throughout), Strict Machine (I to you-machine, all present), E Talking (you/I, present), D.A.N.C.E.
  (you the dancer, present), North American Scum (we Americans, present).
- **We/you for anthems.** One More Time ("we're gonna celebrate" mode), We Are Your Friends (first
  person plural to second person, all present), North American Scum.
- **Past tense is rare and load-bearing when it appears.** Heartbeats is predominantly past tense: the
  whole romance is a recollection, and that choice is what lets ten days fit in one line. All My
  Friends' choruses flash back ("spent the first five years" mode) against present verses. Boy From
  School puts school in past, street in present. Past tense = the flashback stamp, used once, not a
  storytelling frame.
- **Third person appears once in the 22 in-folder fetches: My Friend Dario.** The character-sketch
  mode. The narrator
  watches Dario speed and drink-drive and never intervenes; the distance IS the horror.

### 1.3 Hook construction (measured)

- **Hooks are tiny and looped enormous.** Around the World: 1 distinct phrase, 144 instances. We Are
  Your Friends: 4 distinct lines carrying ~60 printed lines. One More Time: 10 to 12 distinct lines,
  title phrase 30+ times. HBFS: 8 distinct phrases, ~55 to 60 line-repetitions. Get Innocuous: ~16
  unique lines, one refrain repeated 8 times. Over And Over: ~20 distinct lines of ~50. Strict
  Machine: ~14 distinct lines total, everything else is the loop. My Friend Dario: ~9 to 10 unique
  lines of ~20. We Share Our Mothers' Health: ~16 distinct stanzas-lines of ~60.
- **Word count per hook line: 2 to 8, with 4 as the sacred number.** One More Time's chorus block is
  exactly 4 words per line, 4 lines (fetched as an explicit symmetry note). Around the World's unit is
  3 words, twice per line. HBFS's full refrain lines run 4 to 6 words ("work is never over" closes
  nearly every cycle). Crystalised's lines run 4 to 8 words. Nothing fetched exceeds 8 words per line
  in hook position.
- **The hook is a command or a declaration, never a summary.** "One, two, three, four" plus "do the
  dance" (D.A.N.C.E.); "set 'em up" (Daft Punk Is Playing at My House); "go slow" (Crystalised);
  "work it harder" (HBFS); "come on" (We Are Your Friends); "say it now / do it now" (Ready For The
  Floor). The hook tells the room what to do or asserts a state; it never narrates what happened.
- **The hook can be wordless.** Crystalised's chorus is 4 lines of vocalization with no words at all.
- **The hook is (almost always) the title.** Every fetched track's dominant loop is its title or a
  fragment of it; Get Innocuous goes further and saves the title phrase for one single closing
  statement, the punchline position.

### 1.4 What the canon NEVER does (negative claims, bounded by the 22 fetches)

In the 22 fetched lyric sheets, zero instances were found of:

1. **Explaining.** No track states its thesis in the hook. The one candidate, Over And Over's
   repetition-is-joy line, is a declaration of feeling, not an argument; Get Innocuous's conformity
   critique lives in an ironic question, never a claim; North American Scum's stance is self-mocking
   confession, not a stated position. The canon shows a feeling and makes you do it; it never tells
   you what to think about it.
2. **Resolving the plot.** No arc ends in closure. Heartbeats ends by flipping its own conviction into
   a question; Losing My Edge trails off into a repeated interrogative; One Life Stand ends on "could
   this be"; E Talking ends on the same unresolved hook it opened with; TTHHEE PPAARRTTYY trails off
   at the hotel pool. Endings are returns to the loop, mutations of the loop, or fade-outs, never
   morals.
3. **Naming abstract emotions.** Grief is a phone call, coffee and weather (Someone Great); fear of
   aging is a plea to be replaced by machines (Huarache Lights); doom is a super mega car and a
   bottle before every trip (My Friend Dario); obsession is a burning home not left (Crystalised);
   love is pressure and crystallization, glaciers and tide. Stakes arrive as objects.
4. **Long sentences.** No fetched hook or verse line exceeds one clause; verse lines top out around 8
   words. Losing My Edge's name-check bridge is a list, not a paragraph.
5. **Epic past-tense storytelling.** Nobody sings "once upon a time" or narrates a finished story from
   above. The closest, Heartbeats, stays inside one person's memory of one affair; Dario stays inside
   one afternoon on loop.
6. **A villain.** Even the antagonist tracks (DVNO's doorman, Losing My Edge's "internet seekers") are
   walls or weather, not people to defeat. Losing My Edge's rivals are explicitly nice, which is the
   joke and the wound.

## 2. COMPRESSION STUDY: how the canon fits a whole story into 8 lines

### 2.1 The measured density band

The riddle spec (from the ask): a complete thriller, clock + stakes + reversal + exit line, in 14
lines. That is 4 beats in 14 lines = one beat per 3.5 lines. The canon's own measured band:

- Someone Great, verse 2 (8 lines): the entire call beat. The news arrives, and verse 3 (8 lines)
  carries the aftermath entirely as unchanged objects (coffee, weather, unfinished work). Two beats,
  16 lines, zero stated emotion.
- Heartbeats: 4 beats (the night and the promise, the escalation, ten days and the declaration, the
  doubt) in ~29 total lines but only ~16 unique lines = one beat per ~4 unique lines. The ten-day span
  is one line because the past tense and the count carry it.
- All My Friends, verse 3 (~8 lines): party-death AND the life-audit at once (drugs run out,
  conversation drags, and "a badly written film, minus the moral" does the theme's work in one
  simile).
- My Friend Dario: a complete character tragedy in ~9 to 10 unique lines. Car, speed, the drink
  before every trip, "Doesn't care, about to crash". The crash is never shown; the hook IS the exit
  line, and the loop means you hear the death forecast four times.
- Strict Machine: a whole relationship (desire, obedience, reward, control) in ~14 distinct lines,
  one metaphor, never varied.

Verdict: the riddle's 4 beats in 14 lines sits exactly inside the canon's measured band of one beat
per 3.5 to 4 lines. The form can hold the thriller. What it cannot hold is the thriller's usual
connective tissue: the canon has no room for explanation, backstory, or resolution, so all four beats
must arrive as scene.

### 2.2 The five compression devices (how the verses do it)

1. **Objects do narrative work.** The phone call, the coffee, the comfortable shoes, the borrowed PA,
   the car, the burning home. One object per beat, staged in one line, emotion never named. (Someone
   Great, TTHHEE PPAARRTTYY, My Friend Dario, Crystalised, Daft Punk Is Playing at My House.)
2. **Dialogue as time-stamp.** One line of speech marks a whole scene: the promise in Heartbeats'
   first verse, the doorman's denial in DVNO, "say you like it / say you need it" as an accusation
   refrain (We Share Our Mothers' Health), the invitation in We Are Your Friends. Speech is quoted
   flat, present tense, no attribution tags.
3. **Numbers are the clock.** "One, two, three, four" (D.A.N.C.E.); "ten days" (Heartbeats); "hour
   after hour" and the never-over loop (HBFS); "one more time" and "don't stop" (One More Time); the
   alphabet line (D.A.N.C.E.). The canon counts instead of explaining duration; a number plus a
   repeated line IS a clock.
4. **The reversal is a single-word mutation inside an identical loop.** This is the sharpest
   mechanism found. Over And Over's chorus repeats verbatim except its last line, swapping "when I
   feel this way" for "when you look this way": the whole perspective flips in one word. Heartbeats'
   final chorus changes "wouldn't" to a questioning "would": conviction becomes doubt in one word.
   HBFS's intro builds the full sentences out of fragments: the assembly order itself is the
   transformation. The canon never announces a turn; it mutates one word and lets the loop carry the
   shock.
5. **The exit line is the shortest line and it loops.** "go slow" (2 words, x5, Crystalised); "work is
   never over" (4 words, closes nearly every HBFS cycle); "Downtown" (1 word, Daft Punk Is Playing at
   My House); the title phrase stated exactly once at the end (Get Innocuous). Exit lines are 1 to 4
   words, placed where the loop restarts, so the song ends by becoming the beginning.

### 2.3 What the 14-line rewrite must obey (the form law, derived from the measurements)

1. Person: I/you, present tense throughout. At most ONE past-tense line, used as the flashback or
   time-stamp stamp (Heartbeats license).
2. Line length: 4 to 8 words, one clause each. No sentence spans two lines.
3. Hook: an instruction or a count, 1 to 4 words per line; 4-word symmetry is the strongest shape
   (One More Time law). The hook must be singable as a command to the room.
4. The 14 lines split as three 4-line blocks plus a 2-line exit, or four 3-to-4-line beats: clock,
   stakes, reversal, exit. One beat per 3.5 to 4 lines is the measured density band; do not exceed it.
5. Clock: a number or a count in a repeated line (one, two, three, four / ten days / hour after hour
   mode). Never state that time is running out; let the count accelerate or the repeated line wear.
6. Stakes: one object per beat, staged flat, emotion never named. The stake is what the object will
   cost, shown not said.
7. Reversal: ONE word changes inside an otherwise identical repeated line (feel/look law, would law).
   No new sentence may announce the turn.
8. Exit line: 1 to 4 words, loop-ready, placed so the end is a beginning.
9. Never explain, never resolve, never moralize, never name the emotion, never introduce a villain
   with a face. The riddle's wit must live in the objects and the one-word flip, exactly as the canon
   hides its theses inside commands.

### 2.4 Calibration honesty

The riddle (per its spec) fits MORE distinct plot per line than any single canon hook: 4 thriller
beats in 14 lines vs the canon's habit of 1 or 2 beats stretched across a whole song's unique
material. The reconciliation is repetition: the canon buys density on paper by repeating on the
clock. A 14-line riddle read on the page is a 3-minute track when its lines 2, 6 and 10 are the same
line except one word. The rewrite should therefore mark which lines are the loop: the reader who
never hears the loop reads a thriller; the reader who does hears a canon track.

## 3. Evidence register (all fetched live this session via WebFetch, genius.com)

In-folder tracks (20): Around the World (Daft Punk), Harder Better Faster Stronger (Daft Punk),
D.A.N.C.E. (Justice), DVNO (Justice), We Are Your Friends (Justice vs Simian), TTHHEE PPAARRTTYY
(Justice ft Uffie), All My Friends (LCD Soundsystem), Someone Great (LCD Soundsystem), Daft Punk Is
Playing at My House (LCD Soundsystem), North American Scum (LCD Soundsystem), Get Innocuous! (LCD
Soundsystem), Ready For The Floor (Hot Chip), Over And Over (Hot Chip), Boy From School (Hot Chip),
Huarache Lights (Hot Chip), One Life Stand (Hot Chip), Crystalised (The xx), Heartbeats (The Knife),
We Share Our Mothers' Health (The Knife), Strict Machine (Goldfrapp), E Talking (Soulwax), My Friend
Dario (Vitalic).

Ask-named, folder-absent, fetched anyway (2): Losing My Edge (LCD Soundsystem), One More Time (Daft
Punk).

Per-track key measured facts (distinct lines, repetitions, person/tense, arc) are recorded in
`watch/inbox/gala_20260925/lyric-workover/lanes/archaeology.check.txt` alongside the byte-checks.
