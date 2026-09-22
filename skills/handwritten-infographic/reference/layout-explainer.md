# The Explainer layout

Reverse-engineered from three published panels (WireGuard, OpenVPN,
IKEv2/IPsec). Measurements are for a **1024 × 1536** canvas (2:3 portrait).

## Canvas

| Property | Value |
| --- | --- |
| Size | 1024 × 1536 px |
| Aspect | 2:3 portrait |
| Background | `#F7F8F8` — off-white, very slightly cool. **Not pure white.** |
| Texture | None. Flat digital. No paper grain, no vignette, no shadow, no scan artefacts. |
| Margins | ~40 px left and right, ~30 px top |

The look is "a senior engineer's marker notes, scanned perfectly flat" — the
line work is hand-drawn, the surface is not.

## Palette

| Role | Colour | Notes |
| --- | --- | --- |
| Ink — title, headings, body | `#192635` | Dark navy, near-black. Everything that is not accent or warning. |
| Accent | topic's brand hex | Section 1 heading, rules, numbered circles, blurb headings, arrows. |
| Warning | `#C62828` | Section 2 heading, cost-card headings, warning triangles, ✗ marks. |
| Background | `#F7F8F8` | |

Measured accents from the published set: WireGuard `#0B7A80`, OpenVPN
`#CF5E16`, IKEv2 `#0047CF`.

**The accent is never red or red-orange** — the costs half owns that end of the
spectrum, and the contrast between the two halves is the whole point. If the
technology's brand colour is red (Redis, Oracle, Ruby), shift the accent to a
neighbouring hue, or use the ink navy, and leave the warning colour alone.

Illustrations may use full brand colours inside themselves (a green Android
robot, a blue Windows logo) — the palette governs structure, not sketch
content.

## Typography

| Element | Treatment |
| --- | --- |
| Title | Very large, bold, ALL CAPS, heavy marker, ink navy, centred |
| Series line | Small caps under the title, e.g. `2 OF 3`, ink navy |
| Section heading | Large, bold, ALL CAPS, hand-drawn marker, accent or warning colour, centred, underlined with a hand-drawn rule |
| Section subtitle | One line, sentence case, ink navy, centred, small |
| Blurb heading | Medium, ALL CAPS, accent colour, **ends with a colon**, underlined |
| Card heading | Medium, ALL CAPS, 1–2 lines. Ink navy in section 1; warning colour in section 2 |
| Body text | Casual handwritten marker, sentence case, ink navy, slightly imperfect |

Body text is handwritten throughout. Headings are marker-drawn block capitals.
Nothing is a clean digital typeface.

## Zones, top to bottom

### 1. Title block (y ≈ 20–140)

- Title, ALL CAPS, centred.
- Optional series line beneath (`1 OF 3`).
- A full-width horizontal rule in the **accent** colour beneath, inset ~60 px
  each side. Hand-drawn, slightly uneven.

### 2. Two intro blurbs (y ≈ 150–460)

Left and right halves. Each is, top to bottom:

1. A spot illustration (~130 px tall) — a small scene, not an icon.
2. A heading in accent colour, ALL CAPS, ending with a colon, underlined.
3. Three lines of handwritten body text.

Left heading is always `WHAT IT IS:`. Right heading is topic-specific and
answers why the thing persists: `WHY IT WON:`, `WHY IT SURVIVES:`,
`WHY IT PERSISTS:`.

**Leave a large gap (~60–80 px) between the blurbs and the first section
heading.** They must read as two separate zones, not one flowing block.

### 3. Section 1 — `HOW IT WORKS` (y ≈ 480–1000)

- Heading in the accent colour, underlined.
- Subtitle: **`Four design decisions that define the protocol.`** — this line is
  fixed across the series for protocol topics. For non-protocol topics, swap the
  last noun (`…that define the system.`) and keep the shape.
- Four cards in a row, numbered **1–4** in hand-drawn accent-coloured circles
  (outline style, number inside).

Each card: number + heading, then body text, then a sketch. The sketch may sit
above the body text instead — the published set varies this per card and it
still reads. Do not vary it more than once per section.

### 4. Section 2 — `WHAT IT COSTS YOU` (y ≈ 1010–1500)

- Heading in the **warning** colour, underlined. Same size as section 1.
- Subtitle is **topic-specific** and names the price being paid:
  - WireGuard: `The trade-offs that come with being this small.`
  - OpenVPN: `The price of all that flexibility.`
  - IKEv2: `The price of a very large and very old specification.`
- Four cards, numbered **5–8**, continuing section 1's count.
- Each number is preceded by a **warning triangle** (⚠) in the warning colour,
  and written as `5.` with a trailing period.
- Card headings are in the warning colour, not ink navy.

**The numbering runs 1 → 8 across both sections.** It does not restart. This is
the single most common thing the image model breaks; the checklist exists for
it.

### 5. Byline (bottom right, y ≈ 1490)

Name in small caps, ink navy, optionally followed by a LinkedIn glyph. Set
`byline` in the spec; omit the field to leave it off.

## Arrows

Arrows connect steps **within** a section only. There is no arrow from card 4
to card 5 — the section heading is the break. No card has two outgoing arrows.
All arrows use the accent colour, except in the costs half where they use the
warning colour.

Most cards have no arrows at all; arrows belong inside a card's sketch (a
packet moving to a wall), not between cards. Do not draw a 1→2→3→4 chain across
the row unless the concepts really are sequential.

## What the layout forbids

- No title text inside the drawing area. The title belongs in the title block
  only. If the image model draws the topic name again above the first section,
  the render is wrong.
- No whiteboard frame, no sticky notes, no coloured card backgrounds, no
  drop shadows, no banner headers behind headings.
- No paper texture or physical-surface feel.
- No decorative filler icons. Every sketch explains something.
