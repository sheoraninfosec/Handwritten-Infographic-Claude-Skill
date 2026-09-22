# Proofread checklist — IKEV2 / IPSEC

Check the generated image against every line before using it. Image models
fail at text in predictable ways, and the costs half is where numbers go
missing.

## Structure

- [ ] Title reads exactly `IKEV2 / IPSEC`
- [ ] Series line reads exactly `3 OF 3`
- [ ] The topic name appears **once**, in the title block only
- [ ] Section 1 heading reads `HOW IT WORKS`
- [ ] Section 2 heading reads `WHAT IT COSTS YOU`
- [ ] Numbers 1 2 3 4 5 6 7 8 are all present, in order, none missing
- [ ] Cards 5-8 each have a warning triangle **and** a number
- [ ] No arrows between cards or between sections
- [ ] Background is flat off-white with no paper texture

## Text, card by card

- [ ] **Left blurb** heading `WHAT IT IS:`
      - [ ] body: Two protocols working together, already built into the device in your pocket.
- [ ] **Right blurb** heading `WHY IT PERSISTS:`
      - [ ] body: It survives switching from mobile data to Wi-Fi without dropping the tunnel.
- [ ] **Card 1** number visible, heading `TWO PROTOCOLS, NOT ONE`
      - [ ] body: IKEv2 negotiates the keys. IPsec ESP actually carries the data. Most people say one and mean both.
- [ ] **Card 2** number visible, heading `LIVES IN THE KERNEL`
      - [ ] body: ESP is handled by the operating system's own network stack, so throughput stays high.
- [ ] **Card 3** number visible, heading `MOBIKE FOR ROAMING`
      - [ ] body: A dedicated extension lets the tunnel survive an address change without renegotiating from scratch.
- [ ] **Card 4** number visible, heading `ALREADY ON YOUR DEVICE`
      - [ ] body: Built into iOS, macOS, Windows and Android. No third-party client to install or trust.
- [ ] **Card 5** number visible, heading `FIXED PORTS`
      - [ ] body: UDP 500 and 4500, and nowhere else to go. Trivial for a network to block deliberately.
- [ ] **Card 6** number visible, heading `A HUGE NEGOTIATION SURFACE`
      - [ ] body: Many options, several of them historically weak, and plenty of ways to configure it badly.
- [ ] **Card 7** number visible, heading `NAT IS AWKWARD`
      - [ ] body: ESP has no port numbers of its own, so it has to be wrapped in UDP just to survive a home router.
- [ ] **Card 8** number visible, heading `IMPLEMENTATIONS VARY`
      - [ ] body: The specification is enormous, so quality and interoperability differ sharply between vendors.

## Spelling of technical terms

- [ ] `3DES`
- [ ] `4G`
- [ ] `5G`
- [ ] `AES-128`
- [ ] `ESP`
- [ ] `IKEV2`
- [ ] `IKEv2`
- [ ] `RC4`
- [ ] `SHA-1`
- [ ] `UDP`
- [ ] `iOS`
- [ ] `macOS`

## If something is wrong

Re-roll with the failing card's text pasted verbatim at the end of the
prompt as an explicit correction, for example:

> Card 7 must show the number 7 and the heading exactly as: ...

That is usually enough. Regenerating the whole image unchanged rarely is.
