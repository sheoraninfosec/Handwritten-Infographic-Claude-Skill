# Worked examples

Three complete specs ship in `examples/`, transcribed from published panels:

| Folder | Topic | Accent | What it demonstrates |
| --- | --- | --- | --- |
| `examples/wireguard` | WireGuard | `#0B7A80` | A small, opinionated design. Costs are all consequences of the smallness. |
| `examples/openvpn` | OpenVPN | `#CF5E16` | A flexible, old design. Costs are all consequences of the flexibility. |
| `examples/ikev2` | IKEv2 / IPsec | `#0047CF` | A huge specification. Costs are size, age and vendor drift. |

Run any of them to see the output:

```bash
python3 skills/handwritten-infographic/scripts/build_prompt.py \
  examples/wireguard/spec.json --out-dir /tmp/wg
```

## What the three have in common

The `HOW IT WORKS` subtitle is identical in all three —
`Four design decisions that define the protocol.` — because they are one
series. The `WHAT IT COSTS YOU` subtitle is different in each, because it names
the specific price that specific design pays:

- WireGuard — `The trade-offs that come with being this small.`
- OpenVPN — `The price of all that flexibility.`
- IKEv2 — `The price of a very large and very old specification.`

**The costs subtitle is where the panel's argument lives.** Write it after the
four cost cards, as a one-line summary of what they have in common. If they
have nothing in common, they are a list of complaints rather than an analysis,
and the panel is weaker for it.

## How the costs mirror the design

This is the pattern to copy. Each cost is the direct consequence of a decision
in the half above it, not an unrelated gripe.

| WireGuard decision | The cost it creates |
| --- | --- |
| One fixed cipher suite, nothing negotiated | No cipher agility — if a primitive breaks, every endpoint upgrades at once |
| Public keys only, no PKI | Key distribution and revocation are now your job |
| UDP only, minimal surface | No TCP fallback, so a filtering network simply stops you |
| Cryptokey routing table on the server | That table is a persistent identifier for you on someone else's box |

Build the same table for your topic before writing the spec. If a cost does not
trace back to a decision, replace it.

## A note on the IKEv2 panel

The published IKEv2 image has a real defect worth studying: in the costs half,
cards 5 and 8 lost their numbers entirely. The image shows a warning triangle,
then `6` and `7` on the middle two cards, and nothing on the outer two.

This is the single most common failure of this layout, and it is why
`checklist.md` exists and why the prompt repeats the numbering rule three
times. The warning triangle sits where the numeral goes and the model treats
them as alternatives. **Always check 5, 6, 7, 8 before shipping.**

The fix when it happens is a targeted re-roll, not a full regeneration: append
to the prompt an explicit correction naming the card, its number and its
heading verbatim.

## Adapting to a non-protocol topic

The layout is not VPN-specific. Swap the subtitle noun and the shape holds:

- A database engine — `Four design decisions that define the engine.`
- An authentication scheme — `Four design decisions that define the scheme.`
- A build tool, a queue, a filesystem, a consensus algorithm, a rate limiter.

The test for whether a topic fits: **can you name four real trade-offs?** If
not, pick a narrower topic. "Kubernetes" is too broad — four costs would be
generic. "Kubernetes scheduling" is the right size.
