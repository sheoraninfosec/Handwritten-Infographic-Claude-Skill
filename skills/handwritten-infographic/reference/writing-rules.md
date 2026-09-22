# Writing rules

The text is the product. The drawing is how it gets read.

## Voice

Plain, declarative, unhurried. A senior engineer explaining something to a
competent colleague who has not met it yet — not a vendor, not a teacher
talking down, not a thread-boy.

- Second person. "You" are the one paying the cost.
- Short sentences. Full stops over commas.
- Concrete over abstract. `under 4,000 lines` beats `a small codebase`.
  `UDP 500 and 4500` beats `specific ports`.
- State the thing. Do not announce that you are about to state it.
- British spelling (`behaviour`, `optimise`) — the published set uses it.
- No exclamation marks. No emoji. No rhetorical questions in card bodies.

### Banned words

They read as marketing and the linter flags them: `seamless`, `robust`,
`powerful`, `cutting-edge`, `game-changer`, `revolutionary`, `leverage`,
`synergy`, `blazing`, `effortless`, `simply put`, `at the end of the day`,
`in today's world`, `it's important to note`.

### The em dash

Fine in blurb bodies and card bodies where it carries a real aside. Not in
headings. Do not use it as a substitute for a full stop twice in one card.

## Word budgets

Tight on purpose. The image model drops characters when a card runs long, and a
dropped word in a technical claim makes it false rather than short.

| Field | Budget | Hard cap |
| --- | --- | --- |
| Title | 1–4 words | 28 characters |
| Blurb heading | 2–4 words + colon | 22 characters |
| Blurb body | 10–18 words, 3 lines | 20 words |
| Section 2 subtitle | 5–11 words | 13 words |
| Card heading | 2–4 words | 30 characters (2 lines) |
| Card body | 12–26 words, 3–5 lines | 30 words |
| `draw` scene | 8–30 words | — |

If a card will not fit the budget, the card is doing too much. Split the idea
or cut it — do not shrink the type.

## Finding the four costs

The costs half is what makes this format worth reading. Four reliable seams:

1. **What the design refuses to do.** A fixed cipher suite cannot be
   negotiated, so it also cannot be downgraded — and cannot be upgraded on one
   endpoint alone.
2. **What it pushes onto you.** No user accounts means you are now running key
   distribution and revocation by hand.
3. **Where it breaks in the real world.** UDP-only dies behind a filtering
   network. Nothing wrong with the protocol; you still cannot connect.
4. **What age or size costs.** A huge old specification means vendor
   interoperability is a coin flip and the negotiation surface is enormous.

Write costs as facts the reader inherits, not as warnings. `There is no TCP
fallback. If the network blocks UDP, you are simply not connecting.` — that is
the register. Not `Be careful, UDP can be blocked!`

A cost must be a real trade-off of this design, not a generic risk. "Can be
misconfigured" is true of everything and belongs in no spec unless the
configuration surface is itself the notable thing.

## The `draw` field

The single highest-leverage field in the spec. It is a scene description, and
the image model renders roughly what you describe.

**Good** — specific objects, spatial relationship, labels:

> A brick wall with two labelled pipes, `500` and `4500`, hitting it and
> stopping dead, each marked with a red ✗.

> A tall stack of paper labelled `OPENVPN + TLS LIB`, with a magnifying glass
> resting against it.

> A two-column table headed `PUBLIC KEY` and `ALLOWED IPS`, four rows, one row
> highlighted, an arrow leaving it toward a network port.

**Bad** — icon names, adjectives, no scene:

> A firewall icon.

> Something showing complexity.

> A nice illustration of key management.

Rules of thumb:

- Name the objects. Name what is written on them.
- Say where things sit relative to each other.
- Quote any text that must appear in the sketch, in backticks, exactly as it
  should read. Keep it to a few words — the model mangles long strings.
- One idea per sketch. A sketch that needs a paragraph will render as mush.
- Ask for hand-drawn marker line work; the global style note covers it, but a
  sketch that names a photo or a 3D render will fight the style.

## Titles

The title is the topic, not a sentence about the topic. `WIREGUARD`.
`OPENVPN`. `IKEV2 / IPSEC`. If the topic needs a verb to make sense, it is too
broad for one panel — narrow it.

Series panels share a title shape and differ only in the subject.
