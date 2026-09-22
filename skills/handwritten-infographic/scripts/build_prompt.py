#!/usr/bin/env python3
"""Validate an Explainer spec and build the image-generation prompt.

Standard library only. No API key, no network, no dependencies.

    python3 build_prompt.py spec.json --out-dir "How X Works"

Writes prompt.txt and checklist.md next to a copy of the spec, and prints the
lint report. Exits non-zero if the spec has errors.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import colorsys

# --------------------------------------------------------------------------
# Budgets (see reference/writing-rules.md)
# --------------------------------------------------------------------------

TITLE_MAX_CHARS = 28
BLURB_HEADING_MAX_CHARS = 22
CARD_HEADING_MAX_CHARS = 30  # longest in the published set: "ALL ENDPOINTS UPDATE TOGETHER"

BLURB_BODY_WORDS = (10, 18)
BLURB_BODY_HARD_MAX = 20
CARD_BODY_WORDS = (12, 26)
CARD_BODY_HARD_MAX = 30
SUBTITLE_WORDS = (5, 11)
SUBTITLE_HARD_MAX = 13
DRAW_WORDS = (8, 30)

INK = "#192635"
BACKGROUND = "#F7F8F8"
WARNING = "#C62828"

BANNED = [
    "seamless", "robust", "powerful", "cutting-edge", "cutting edge",
    "game-changer", "game changer", "revolutionary", "leverage", "synergy",
    "blazing", "effortless", "simply put", "at the end of the day",
    "in today's world", "in todays world", "it's important to note",
    "its important to note", "unlock", "supercharge", "next-level",
]

VAGUE_DRAW = [
    "an icon", "a nice", "something showing", "a graphic of", "an image of",
    "some kind of", "a symbol", "a logo of", "illustration of complexity",
]

HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")

    @property
    def ok(self) -> bool:
        return not self.errors


def words(text: str) -> int:
    return len([w for w in re.split(r"\s+", text.strip()) if w])


def check_banned(rep: Report, where: str, text: str) -> None:
    low = text.lower()
    for word in BANNED:
        if word in low:
            rep.error(where, f"banned marketing word {word!r}")


def check_body(rep: Report, where: str, text: str, lo: int, hi: int, hard: int) -> None:
    if not text or not text.strip():
        rep.error(where, "is empty")
        return
    n = words(text)
    if n > hard:
        rep.error(where, f"{n} words, hard cap is {hard} — the image model will drop text")
    elif n > hi:
        rep.warn(where, f"{n} words, budget is {lo}-{hi}")
    elif n < lo:
        rep.warn(where, f"only {n} words, budget is {lo}-{hi} — probably too thin to be useful")
    if not text.strip().endswith((".", "?", "!")):
        rep.warn(where, "does not end with a full stop")
    check_banned(rep, where, text)


def check_heading(rep: Report, where: str, text: str, cap: int, want_colon: bool = False) -> None:
    if not text or not text.strip():
        rep.error(where, "is empty")
        return
    stripped = text.strip()
    if len(stripped) > cap:
        rep.error(where, f"{len(stripped)} characters, cap is {cap} — it will not fit on one line")
    letters = [c for c in stripped if c.isalpha()]
    if letters and not all(c.isupper() for c in letters):
        rep.error(where, "must be ALL CAPS")
    if want_colon and not stripped.endswith(":"):
        rep.error(where, "must end with a colon")
    check_banned(rep, where, stripped)


def check_draw(rep: Report, where: str, text: str) -> None:
    if not text or not text.strip():
        rep.error(where, "missing — every card needs a scene to draw")
        return
    n = words(text)
    low = text.lower().strip()
    for vague in VAGUE_DRAW:
        if low.startswith(vague) or f" {vague} " in low:
            rep.error(
                where,
                f"{vague!r} is an icon name, not a scene — say what objects appear and where",
            )
            break
    if n < DRAW_WORDS[0]:
        rep.error(where, f"only {n} words — too vague to render, describe the actual scene")
    elif n > DRAW_WORDS[1]:
        rep.warn(where, f"{n} words — long scenes render as mush, keep one idea")


def check_accent(rep: Report, accent: str) -> None:
    if not HEX_RE.match(accent or ""):
        rep.error("accent", f"{accent!r} is not a 6-digit hex colour like #0B7A80")
        return
    r, g, b = (int(accent[i:i + 2], 16) / 255 for i in (1, 3, 5))
    hue, light, sat = colorsys.rgb_to_hls(r, g, b)
    deg = hue * 360
    if sat > 0.25 and (deg < 22 or deg > 340):
        rep.error(
            "accent",
            f"{accent} is red — red is reserved for the costs half, "
            "pick a neighbouring hue or the ink navy",
        )
    if light > 0.75:
        rep.warn("accent", f"{accent} is very light and will wash out against {BACKGROUND}")


def validate(spec: dict) -> Report:
    rep = Report()

    for key in ("title", "accent", "blurbs", "how", "costs"):
        if key not in spec:
            rep.error("spec", f"missing required key {key!r}")
    if rep.errors:
        return rep

    check_heading(rep, "title", spec["title"], TITLE_MAX_CHARS)
    check_accent(rep, spec["accent"])

    series = (spec.get("series") or "").strip()
    if series and not re.match(r"^\d+\s+OF\s+\d+$", series, re.I):
        rep.warn("series", f"{series!r} does not look like '2 OF 3'")

    blurbs = spec["blurbs"]
    for side in ("left", "right"):
        if side not in blurbs:
            rep.error("blurbs", f"missing {side!r} blurb")
            continue
        b = blurbs[side]
        check_heading(rep, f"blurbs.{side}.heading", b.get("heading", ""),
                      BLURB_HEADING_MAX_CHARS, want_colon=True)
        check_body(rep, f"blurbs.{side}.body", b.get("body", ""),
                   *BLURB_BODY_WORDS, BLURB_BODY_HARD_MAX)
        check_draw(rep, f"blurbs.{side}.draw", b.get("draw", ""))

    left_heading = blurbs.get("left", {}).get("heading", "").strip().upper()
    if left_heading and left_heading != "WHAT IT IS:":
        rep.warn("blurbs.left.heading",
                 f"{left_heading!r} — the left blurb is conventionally 'WHAT IT IS:'")

    seen_headings: dict[str, str] = {}

    for section, expected_n, label in (("how", 4, "how"), ("costs", 4, "costs")):
        sec = spec[section]
        subtitle = sec.get("subtitle", "")
        if not subtitle.strip():
            rep.error(f"{section}.subtitle", "is empty")
        else:
            n = words(subtitle)
            if n > SUBTITLE_HARD_MAX:
                rep.error(f"{section}.subtitle", f"{n} words, hard cap is {SUBTITLE_HARD_MAX}")
            elif not (SUBTITLE_WORDS[0] <= n <= SUBTITLE_WORDS[1]):
                rep.warn(f"{section}.subtitle", f"{n} words, budget is {SUBTITLE_WORDS[0]}-{SUBTITLE_WORDS[1]}")
            check_banned(rep, f"{section}.subtitle", subtitle)

        cards = sec.get("cards", [])
        if len(cards) != expected_n:
            rep.error(f"{section}.cards", f"has {len(cards)} cards, the layout needs exactly {expected_n}")
        for i, card in enumerate(cards):
            num = i + 1 if section == "how" else i + 5
            where = f"{section}.cards[{i}] (#{num})"
            check_heading(rep, f"{where}.heading", card.get("heading", ""), CARD_HEADING_MAX_CHARS)
            check_body(rep, f"{where}.body", card.get("body", ""),
                       *CARD_BODY_WORDS, CARD_BODY_HARD_MAX)
            check_draw(rep, f"{where}.draw", card.get("draw", ""))

            h = card.get("heading", "").strip().upper()
            if h:
                if h in seen_headings:
                    rep.error(f"{where}.heading", f"duplicates {seen_headings[h]}")
                seen_headings[h] = where

    costs_cards = spec["costs"].get("cards", [])
    if len(costs_cards) == 4:
        generic = [c for c in costs_cards
                   if "misconfigur" in c.get("body", "").lower()
                   and "misconfigur" in c.get("heading", "").lower()]
        if len(generic) > 1:
            rep.warn("costs", "more than one card is about misconfiguration — find a sharper trade-off")

    return rep


# --------------------------------------------------------------------------
# Prompt
# --------------------------------------------------------------------------

STYLE = """\
Create a hand-drawn educational infographic in the style of a senior engineer's
marker notes, scanned perfectly flat.

CANVAS
- Exactly 1024 x 1536 pixels. Portrait, 2:3. All content fits inside with no
  cropping and no overflow.
- Background is flat off-white {bg}. Not pure white. Absolutely no paper
  texture, grain, noise, vignette, shadow or physical-surface feel. Treat it as
  a clean digital canvas.

STYLE
- Every line is hand-drawn with markers: slightly imperfect, energetic, clean.
- Headings are marker-drawn block capitals. Body text is casual handwriting,
  legible, slightly uneven. Nothing uses a clean digital typeface.
- Illustrations are rough hand-drawn sketches with flat colour fills. Not
  clipart, not flat vector icons, not 3D renders, not photographs.
- No whiteboard frame, no sticky notes, no coloured card backgrounds behind
  text, no drop shadows, no banner bars behind headings.

COLOUR
- Ink (title, body text, outlines): {ink}
- Accent (section 1 heading and rule, numbered circles, blurb headings): {accent}
- Warning (section 2 heading and rule, cost card headings, warning triangles): {warning}
- Illustrations may use the real brand colours of whatever they depict.

TEXT ACCURACY — THIS MATTERS MORE THAN THE ART
- Render every piece of text below EXACTLY as written. Do not paraphrase,
  shorten, translate or improvise text.
- Spell technical terms character by character as given.
- Do not add any text, label, caption or watermark that is not specified below.
- Every numbered item must show its number. The numbers run 1 to 8 continuously
  across both sections and never restart.
"""

LAYOUT_HEAD = """\

=== LAYOUT, TOP TO BOTTOM ===

1. TITLE BLOCK
Centred, very large bold ALL-CAPS marker lettering in {ink}:

    {title}
"""

LAYOUT_RULE = """\
Beneath it, a hand-drawn horizontal rule in {accent} spanning most of the width.

2. TWO INTRO BLURBS, side by side
Each has a sketch on top, then a heading, then three lines of handwritten body
text. Leave a large gap (about 70 px of empty space) between this zone and the
section heading below it, so they read as two separate zones.
"""


def blurb_block(side: str, b: dict, accent: str) -> str:
    return (
        f"\nLEFT BLURB\n" if side == "left" else "\nRIGHT BLURB\n"
    ) + (
        f"  Sketch: {b['draw'].strip()}\n"
        f"  Heading (ALL CAPS, {accent}, underlined): {b['heading'].strip()}\n"
        f"  Body: {b['body'].strip()}\n"
    )


def section_block(sec: dict, colour: str, start: int, triangles: bool) -> str:
    lines = [
        f"  Heading (large, bold, ALL CAPS, {colour}, centred, underlined with a hand-drawn rule):",
        f"    {sec['heading'].strip()}",
        f"  Subtitle (one line, sentence case, centred, ink):",
        f"    {sec['subtitle'].strip()}",
        "",
        "  Four cards in a row. Each card: the number, then the heading, then the",
        "  body text, then the sketch below it.",
        "",
    ]
    for i, card in enumerate(sec["cards"]):
        num = start + i
        if triangles:
            marker = (f"a warning triangle in {colour}, then the number "
                      f"\"{num}.\" with a full stop")
            head_colour = colour
        else:
            marker = f"the number \"{num}\" inside a hand-drawn outline circle in {colour}"
            head_colour = "ink"
        lines += [
            f"  CARD {num}",
            f"    Number: {marker}",
            f"    Heading (ALL CAPS, {head_colour}): {card['heading'].strip()}",
            f"    Body: {card['body'].strip()}",
            f"    Sketch: {card['draw'].strip()}",
            "",
        ]
    return "\n".join(lines)


FOOTER = """\
=== RULES THE RENDER MUST OBEY ===

- Do NOT draw the topic name anywhere except the title block at the very top.
  No second title, no heading repeating the subject above a section.
- Numbering is 1, 2, 3, 4 in section 1 and 5, 6, 7, 8 in section 2. It does not
  restart at 1. Every one of the eight cards shows its number.
- Arrows only ever appear inside a card's own sketch. Never draw an arrow
  between two cards, and never between the two sections.
- Every sketch explains its card. No decorative filler icons.
- Reproduce all text exactly as specified. Add nothing.
"""


def build_prompt(spec: dict) -> str:
    accent = spec["accent"]
    parts = [STYLE.format(bg=BACKGROUND, ink=INK, accent=accent, warning=WARNING)]
    parts.append(LAYOUT_HEAD.format(ink=INK, title=spec["title"].strip()))

    series = (spec.get("series") or "").strip()
    if series:
        parts.append(f"Directly beneath the title, smaller, centred, in {INK}:\n\n    {series}\n")

    parts.append(LAYOUT_RULE.format(accent=accent))
    parts.append(blurb_block("left", spec["blurbs"]["left"], accent))
    parts.append(blurb_block("right", spec["blurbs"]["right"], accent))

    parts.append("\n3. SECTION ONE\n")
    parts.append(section_block(spec["how"], accent, 1, triangles=False))

    parts.append("\n4. SECTION TWO\n")
    parts.append(section_block(spec["costs"], WARNING, 5, triangles=True))

    byline = (spec.get("byline") or "").strip()
    if byline:
        parts.append(
            f"\n5. BYLINE\nBottom right corner, small ALL-CAPS lettering in {INK}:\n\n"
            f"    {byline}\n"
        )

    parts.append("\n" + FOOTER)
    return "\n".join(parts)


def build_checklist(spec: dict) -> str:
    out = [
        f"# Proofread checklist — {spec['title'].strip()}",
        "",
        "Check the generated image against every line before using it. Image models",
        "fail at text in predictable ways, and the costs half is where numbers go",
        "missing.",
        "",
        "## Structure",
        "",
        f"- [ ] Title reads exactly `{spec['title'].strip()}`",
    ]
    series = (spec.get("series") or "").strip()
    if series:
        out.append(f"- [ ] Series line reads exactly `{series}`")
    out += [
        "- [ ] The topic name appears **once**, in the title block only",
        f"- [ ] Section 1 heading reads `{spec['how']['heading'].strip()}`",
        f"- [ ] Section 2 heading reads `{spec['costs']['heading'].strip()}`",
        "- [ ] Numbers 1 2 3 4 5 6 7 8 are all present, in order, none missing",
        "- [ ] Cards 5-8 each have a warning triangle **and** a number",
        "- [ ] No arrows between cards or between sections",
        "- [ ] Background is flat off-white with no paper texture",
        "",
        "## Text, card by card",
        "",
    ]

    for side in ("left", "right"):
        b = spec["blurbs"][side]
        out.append(f"- [ ] **{side.title()} blurb** heading `{b['heading'].strip()}`")
        out.append(f"      - [ ] body: {b['body'].strip()}")

    for section, start in (("how", 1), ("costs", 5)):
        for i, card in enumerate(spec[section]["cards"]):
            num = start + i
            out.append(f"- [ ] **Card {num}** number visible, heading `{card['heading'].strip()}`")
            out.append(f"      - [ ] body: {card['body'].strip()}")

    terms = sorted(set(collect_terms(spec)))
    if terms:
        out += ["", "## Spelling of technical terms", ""]
        out += [f"- [ ] `{t}`" for t in terms]

    out += [
        "",
        "## If something is wrong",
        "",
        "Re-roll with the failing card's text pasted verbatim at the end of the",
        "prompt as an explicit correction, for example:",
        "",
        "> Card 7 must show the number 7 and the heading exactly as: ...",
        "",
        "That is usually enough. Regenerating the whole image unchanged rarely is.",
        "",
    ]
    return "\n".join(out)


# Candidate tokens: runs of letters/digits that may carry . - _ / inside them.
TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/-]*[A-Za-z0-9]")
CAMEL_RE = re.compile(r"[a-z][A-Z]")

# Short all-caps words that are ordinary English, not acronyms worth checking.
# Extend this for your own domain if a common word keeps appearing.
STOP_TERMS = {
    "AND", "ANY", "ALL", "ARE", "BY", "FOR", "HOW", "IS", "IT", "ITS", "NEW",
    "NO", "NOT", "OF", "OK", "OLD", "ON", "ONE", "OR", "OUT", "THE", "TO",
    "TWO", "WHAT", "WHY", "YOU", "YOUR", "IN", "AT", "AS", "SO", "UP", "WE",
}


def is_technical(token: str, allow_acronym: bool) -> bool:
    """True for tokens an image model is likely to mangle.

    Versioned and alphanumeric names, dotted or underscored identifiers,
    hyphenated compounds with an acronym or digit in them, and camelCase
    product names. Ordinary English words are not.
    """
    if token.upper() in STOP_TERMS:
        return False
    has_alpha = any(c.isalpha() for c in token)
    has_digit = any(c.isdigit() for c in token)

    # ChaCha20, Poly1305, Curve25519, BLAKE2s, 3DES, RC4, IKEv2, 4G
    if has_alpha and has_digit:
        return True
    # X.509, wg_xmit, client.conf, TCP/IP
    if has_alpha and any(c in "._/" for c in token):
        return True
    # AES-GCM and SHA-1 qualify; hand-drawn and per-user do not.
    if "-" in token:
        for part in token.split("-"):
            if any(c.isdigit() for c in part):
                return True
            if len(part) >= 2 and part.isupper():
                return True
        return False
    # OpenSSL, mbedTLS, WireGuard — a lowercase letter followed by an uppercase.
    if CAMEL_RE.search(token):
        return True
    # Bare acronyms (PKI, UDP, NAT, ESP, NIC, TLS, CIDR) only from body prose.
    # In headings and sketch labels everything is capitalised anyway, so the
    # rule would sweep up ordinary words like KEYS, AUDIT and SPACE.
    if allow_acronym and token.isupper() and 2 <= len(token) <= 5:
        return True
    return False


def collect_terms(spec: dict) -> list[str]:
    # (text, is_prose) — acronyms are only harvested from prose bodies.
    blobs: list[tuple[str, bool]] = []
    for side in ("left", "right"):
        b = spec["blurbs"].get(side, {})
        blobs += [(b.get("body", ""), True), (b.get("draw", ""), False)]
    for section in ("how", "costs"):
        for card in spec[section].get("cards", []):
            blobs += [
                (card.get("heading", ""), False),
                (card.get("body", ""), True),
                (card.get("draw", ""), False),
            ]
    found: list[str] = []
    for blob, is_prose in blobs:
        for token in TOKEN_RE.findall(blob):
            if is_technical(token, allow_acronym=is_prose):
                found.append(token)
    return found


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", help="path to spec.json")
    ap.add_argument("--out-dir", help="output folder (default: alongside the spec)")
    ap.add_argument("--lint-only", action="store_true", help="validate without writing files")
    args = ap.parse_args()

    try:
        with open(args.spec, encoding="utf-8") as fh:
            spec = json.load(fh)
    except FileNotFoundError:
        print(f"error: no such spec: {args.spec}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"error: {args.spec} is not valid JSON: {exc}", file=sys.stderr)
        return 2

    if spec.get("layout", "explainer") != "explainer":
        print(f"error: unknown layout {spec.get('layout')!r}; this skill ships 'explainer'",
              file=sys.stderr)
        return 2

    rep = validate(spec)

    for w in rep.warnings:
        print(f"  warn   {w}")
    for e in rep.errors:
        print(f"  ERROR  {e}", file=sys.stderr)

    if not rep.ok:
        print(f"\n{len(rep.errors)} error(s). Fix the spec and run again — "
              "a broken spec produces a broken image.", file=sys.stderr)
        return 1

    if args.lint_only:
        print(f"\nSpec is valid ({len(rep.warnings)} warning(s)).")
        return 0

    out_dir = args.out_dir or os.path.dirname(os.path.abspath(args.spec))
    os.makedirs(out_dir, exist_ok=True)

    prompt_path = os.path.join(out_dir, "prompt.txt")
    checklist_path = os.path.join(out_dir, "checklist.md")
    with open(prompt_path, "w", encoding="utf-8") as fh:
        fh.write(build_prompt(spec))
    with open(checklist_path, "w", encoding="utf-8") as fh:
        fh.write(build_checklist(spec))

    spec_copy = os.path.join(out_dir, "spec.json")
    if os.path.abspath(spec_copy) != os.path.abspath(args.spec):
        shutil.copyfile(args.spec, spec_copy)

    print(f"\nSpec is valid ({len(rep.warnings)} warning(s)).")
    print(f"  {prompt_path}")
    print(f"  {checklist_path}")
    print("\nCanvas: 1024 x 1536 (2:3 portrait).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
