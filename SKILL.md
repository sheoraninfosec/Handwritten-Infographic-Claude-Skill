---
name: handwritten-infographic
description: "Turn a technical topic into a hand-drawn notebook-style explainer infographic that shows BOTH how the thing works and what it costs you. Produces a validated content spec and a copy-paste image-generation prompt (for Designer, ChatGPT, Gemini, Midjourney or any image model), plus a proofread checklist for catching dropped text and broken numbering. Use whenever the user wants a handwritten or hand-drawn infographic, a notebook-style explainer, a 'how X works' poster with trade-offs, a LinkedIn carousel panel, or says 'infographic', 'hand-drawn diagram', 'handwritten notes style', 'explainer image', 'sketch-note', 'visual explainer'. Also use when they name a topic and ask to 'explain it visually' or 'make a poster about it'."
---

# Handwritten Infographic — the Explainer layout

Turn one topic into a hand-drawn, notebook-style explainer image.

The format's whole argument is that **an honest explainer has two halves**. Most
infographics only sell the thing. This one always pairs `HOW IT WORKS` with
`WHAT IT COSTS YOU`, numbered continuously 1 to 8, so the reader gets the
trade-offs in the same glance as the pitch.

You do not render the image. You produce:

1. `spec.json` — the validated content
2. `prompt.txt` — a copy-paste prompt for any image model
3. `checklist.md` — what to proofread in the returned image

All three go in the output folder. **A run is not finished until all three
exist.** Create a todo per step so the checklist is not skipped — it is the part
that catches the image model's mistakes.

## The one rule that matters

**Never ship four upsides and four upsides.** Cards 1–4 explain the design.
Cards 5–8 are what it costs the reader: limits, risks, work they inherit,
things that break. If a topic seems to have no costs, you have not thought
about it hard enough — every design decision trades something away. Write the
costs first if it helps.

## Workflow

### Step 1: Settle the topic and the angle

Ask the user for the topic if they have not given one. Then decide, without
asking unless it is genuinely ambiguous:

- **The accent colour.** The technology's own brand colour, as a hex. Look it
  up rather than guessing. Generic topics with no brand → `#0B7A80` (teal).
  Never use red as the accent — red is reserved for the costs half.
- **Series position.** If the user is making a set ("do the three VPN
  protocols"), each image gets `1 OF 3`, `2 OF 3`, `3 OF 3` under the title.
  One-offs omit it.
- **The right-hand blurb heading.** `WHAT IT IS:` is always the left one. The
  right one is topic-specific and states why the thing persists in the world:
  `WHY IT WON:`, `WHY IT SURVIVES:`, `WHY IT PERSISTS:`, `WHY IT SPREAD:`.

Read `reference/layout-explainer.md` now if you have not built this layout
before in this session — it has the exact geometry, palette and typography.

### Step 2: Research the content

The audience is working engineers. Every claim must be technically accurate and
specific enough to be checkable — real numbers, real cipher names, real port
numbers, real limits. Vague claims are the failure mode.

If the topic is current (a version, a default, a deprecation), verify it rather
than relying on recall. If a fact cannot be verified, do not put a number on it.

### Step 3: Write the spec

Copy `templates/spec.template.json` and fill it in. Read
`reference/writing-rules.md` for the voice and the word budgets — they are
tight on purpose, because the image model drops text when a card runs long.

Every card needs a `draw` field describing a **specific scene**, not an icon
name. "A brick wall with a labelled UDP pipe shattering against it" works.
"A firewall icon" does not — the model will produce a generic sticker and the
card will explain nothing.

### Step 4: Build the prompt

```bash
python3 scripts/build_prompt.py spec.json --out-dir "<output folder>"
```

Pure standard library, no dependencies, no API key. It:

- **lints** the spec — word budgets, heading lengths, numbering 1–8, banned
  hype words, missing `draw` scenes, red accents — and refuses to build on
  errors so a broken spec never reaches the image model
- writes `prompt.txt`, the full image prompt
- writes `checklist.md`, the per-card proofread list

Fix every error it reports and re-run. Warnings are advisory; use judgement.

### Step 5: Hand it over

Give the user `prompt.txt` to paste into their image model, and tell them the
canvas is **1024 × 1536**. If their tool takes an aspect ratio instead, it is
**2:3**.

### Step 6: Proofread the result

When the user comes back with the generated image, **look at it against
`checklist.md`** before saying anything positive about it. Image models fail
at text in specific, predictable ways:

- **Dropped numbers.** The costs half is where this happens — the warning
  triangle competes with the numeral and the model drops one. Check that 5, 6,
  7 and 8 are all present and in order.
- **Misspelled technical terms.** Cipher names, protocol names and product
  names get mangled.
- **Invented text.** The model adds labels that were not in the spec.
- **A title on the drawing.** The prompt forbids it, but it creeps back.

Report what is wrong specifically ("card 7 lost its number; ChaCha20 is spelled
ChaCha2O"). Offer a targeted re-roll: regenerate with the failing card's text
repeated verbatim at the end of the prompt, which is the fix that usually
works.

Never tell the user an image is correct without having checked it against the
checklist.

## Output folder

```
<topic>/
├── spec.json       ← the content, validated
├── prompt.txt      ← paste this into the image model
└── checklist.md    ← proofread the result against this
```

## Reference files

- `reference/layout-explainer.md` — geometry, palette, typography, zone by zone
- `reference/writing-rules.md` — voice, word budgets, banned words, how to find costs
- `reference/worked-examples.md` — three complete specs to match against
- `templates/spec.template.json` — the skeleton to copy
