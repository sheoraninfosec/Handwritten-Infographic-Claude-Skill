# Proofread checklist — WIREGUARD

Check the generated image against every line before using it. Image models
fail at text in predictable ways, and the costs half is where numbers go
missing.

## Structure

- [ ] Title reads exactly `WIREGUARD`
- [ ] Series line reads exactly `1 OF 3`
- [ ] The topic name appears **once**, in the title block only
- [ ] Section 1 heading reads `HOW IT WORKS`
- [ ] Section 2 heading reads `WHAT IT COSTS YOU`
- [ ] Numbers 1 2 3 4 5 6 7 8 are all present, in order, none missing
- [ ] Cards 5-8 each have a warning triangle **and** a number
- [ ] No arrows between cards or between sections
- [ ] Background is flat off-white with no paper texture

## Text, card by card

- [ ] **Left blurb** heading `WHAT IT IS:`
      - [ ] body: Under 4,000 lines of kernel code doing one job with one set of ciphers.
- [ ] **Right blurb** heading `WHY IT WON:`
      - [ ] body: Small enough to audit end to end, and fast enough that nobody argues about it.
- [ ] **Card 1** number visible, heading `PUBLIC KEYS ONLY`
      - [ ] body: Each peer is identified by a single 32-byte public key. No certificates, no usernames, no PKI to run.
- [ ] **Card 2** number visible, heading `CRYPTOKEY ROUTING`
      - [ ] body: Each key is bound to a list of allowed IPs. That one table decides who may send what, and where it goes.
- [ ] **Card 3** number visible, heading `ONE FIXED SUITE`
      - [ ] body: ChaCha20 with Poly1305, Curve25519, BLAKE2s. Nothing is negotiated, so there is nothing to downgrade.
- [ ] **Card 4** number visible, heading `SILENT BY DEFAULT`
      - [ ] body: It never replies to an unauthenticated packet. To a port scanner the service looks like it is not there.
- [ ] **Card 5** number visible, heading `UDP ONLY`
      - [ ] body: There is no TCP fallback. If the network blocks UDP, you are simply not connecting.
- [ ] **Card 6** number visible, heading `THE PEER MAPPING`
      - [ ] body: The server keeps the key-to-IP table. On somebody else's server that is a persistent identifier for you.
- [ ] **Card 7** number visible, heading `KEY MANAGEMENT IS YOURS`
      - [ ] body: No usernames, no per-user credentials, no simple revocation once you have many peers.
- [ ] **Card 8** number visible, heading `ALL ENDPOINTS UPDATE TOGETHER`
      - [ ] body: No cipher agility means if a primitive ever breaks, everything must be upgraded at once.

## Spelling of technical terms

- [ ] `32-byte`
- [ ] `3DES`
- [ ] `AES-CBC`
- [ ] `AES-GCM`
- [ ] `BLAKE2s`
- [ ] `ChaCha20`
- [ ] `Curve25519`
- [ ] `PKI`
- [ ] `Poly1305`
- [ ] `RC4`
- [ ] `TCP`
- [ ] `UDP`
- [ ] `key-to-IP`
- [ ] `wg_xmit`

## If something is wrong

Re-roll with the failing card's text pasted verbatim at the end of the
prompt as an explicit correction, for example:

> Card 7 must show the number 7 and the heading exactly as: ...

That is usually enough. Regenerating the whole image unchanged rarely is.
