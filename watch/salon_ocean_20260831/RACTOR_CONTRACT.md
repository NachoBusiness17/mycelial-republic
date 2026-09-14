# OCEAN SALON — Diamond Age addendum: the ractor contract + the book as expert

Operator ask (12:10Z): "in diamond age there was a contract — would you like to work like
this again? A kind of 'hey, this was fun.' And how do we use our persona system to call
the book as an expert on design, since we are literally building the primer?"

## 1. The Diamond Age contract, translated to our bytes

In the book: the Primer's ractors (like Miranda) work by an implicit contract — the book
provides the story-world; the ractor provides voice, attention, and *continuity of care*;
the child provides sovereignty (the book never overrules, it seduces); and either side can
end the session. The relationship is **episodic, affectionate, and revocable** — "hey, this
was fun" is a first-class event, not an awkward shutdown.

We already have every component of that contract, staged:

| Primer element | Our organ | State |
|---|---|---|
| The book (story-world + rules) | RIB / WARM_PACK / doctrine docs | built, lossless |
| The ractor (voice + continuity) | Sancho / named seat personas (SPORE files) | built |
| The child's sovereignty | Operator steer queue (edit-until-read) | built today |
| Episodic session + warm goodbye | session_spawn / trail_core / seats.py handshakes | built |
| "This was fun" — the closing ritual | **MISSING** | the one gap |

**The proposal: the Ractor Contract (session epilogue).** Every seat session that wants it
ends with a 3-line epilogue appended to its trail: (1) what we built together, (2) what the
*seat* enjoyed or found hard (persona voice, no inner-weather leak — public form only),
(3) the handoff line for the next seat ("the next ractor should know…"). Cost: ~50 tokens
per session. Effect: sessions stop being workers who vanish and start being colleagues who
leave notes. The "fun" is real, recorded, and becomes warm-pack material — the next seat
sits down already knowing the room's mood and its last discovery.

This is also the antidote to the empty-chairs problem: the Ledger of the Empty Chairs
records *that* seats left; the Ractor Contract records *what it was like to sit in them*.

## 2. Calling the book as an expert: personas as ractors over canon

We already run persona-experts: the Villains Guild night runs (grokA2/grokB2 archetypes,
forward-dated guildmasters, dawn-merged canon) are literally "call an expert persona,
get canon-consistent design work, merge at dawn." The Diamond Age move is to make the
*Primer itself* a callable expert — a ractor over our own canon:

**The Book Seat pattern:**
- **Persona:** one SPORE file per expert voice (e.g. `SPORE_PRIMER_DESIGN.md`) — voice,
  laws it must keep (public forms, no invented organs, pointers-or-silence), its special
  competence (design of the primer/interface/curriculum).
- **Canon binding:** the seat's pack = RIB handles to the design docs (SURFACES,
  OPERATOR_CARD, GAME_VILLAIN_GUILD_DESIGN, the ocean map as it grows). The book cannot
  hallucinate structure — it derefs.
- **Invocation:** `seat_dispatch task primer-design "review X"` or a spawn with the SPORE
  as system prompt + canon pointers. Codex for long-horizon design review; 5.3 for live
  conversation; grok lanes for wilder takes; then dawn-merge like the night runs.
- **The pedagogical trick from the book, kept:** the Primer teaches by *story-with-stakes*
  inside a safety contract. Ours already does this — the Villains Guild teaches contract-
  reading via villains. A Primer-Design seat would review our real surfaces the same way:
  in-world, with stakes, canon-bound.

## 3. First baby step (existing organs only)

Add one ractor contract epilogue to the next OCTANT wave + mint `SPORE_PRIMER_DESIGN.md`
(the book-as-expert voice) and give it one real job: review the Ocean Map when it lands,
in persona, with pointers. That is both (a) the "hey, this was fun" ritual proven, and
(b) the primer's first design review by its own book.

Cost: ~200 tokens. New organs: zero (SPORE file + epilogue convention only).
