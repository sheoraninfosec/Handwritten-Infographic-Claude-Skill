# Proofread checklist — OPENVPN

Check the generated image against every line before using it. Image models
fail at text in predictable ways, and the costs half is where numbers go
missing.

## Structure

- [ ] Title reads exactly `OPENVPN`
- [ ] Series line reads exactly `2 OF 3`
- [ ] The topic name appears **once**, in the title block only
- [ ] Section 1 heading reads `HOW IT WORKS`
- [ ] Section 2 heading reads `WHAT IT COSTS YOU`
- [ ] Numbers 1 2 3 4 5 6 7 8 are all present, in order, none missing
- [ ] Cards 5-8 each have a warning triangle **and** a number
- [ ] No arrows between cards or between sections
- [ ] Background is flat off-white with no paper texture

## Text, card by card

- [ ] **Left blurb** heading `WHAT IT IS:`
      - [ ] body: A tunnel built on the same TLS your browser already uses, running in userspace.
- [ ] **Right blurb** heading `WHY IT SURVIVES:`
      - [ ] body: It can sit on TCP 443 and become almost indistinguishable from normal web traffic.
- [ ] **Card 1** number visible, heading `TLS UNDERNEATH`
      - [ ] body: The tunnel is established with the same handshake your browser performs, through OpenSSL or mbedTLS.
- [ ] **Card 2** number visible, heading `CERTIFICATES AND USERS`
      - [ ] body: Full X.509 identity, optional username and password, and revocation lists for taking access away.
- [ ] **Card 3** number visible, heading `RUNS IN USERSPACE`
      - [ ] body: It is an ordinary program, not kernel code. Easy to port and sandbox, slower than a kernel datapath.
- [ ] **Card 4** number visible, heading `ANY TRANSPORT, ANY PORT`
      - [ ] body: UDP or TCP, on whichever port you choose, including 443 where it blends into HTTPS.
- [ ] **Card 5** number visible, heading `A LARGE ATTACK SURFACE`
      - [ ] body: Hundreds of thousands of lines once the TLS library is counted. More to audit and more to patch.
- [ ] **Card 6** number visible, heading `SLOWER`
      - [ ] body: Userspace processing and per-packet overhead leave it measurably behind kernel datapaths on throughput and latency.
- [ ] **Card 7** number visible, heading `EASY TO MISCONFIGURE`
      - [ ] body: A wide configuration surface and negotiated ciphers mean weak setups are entirely possible.
- [ ] **Card 8** number visible, heading `TCP OVER TCP`
      - [ ] body: Running it on TCP for stealth stacks one retransmission scheme on another and collapses under packet loss.

## Spelling of technical terms

- [ ] `HTTPS`
- [ ] `OpenSSL`
- [ ] `TCP`
- [ ] `TLS`
- [ ] `UDP`
- [ ] `X.509`
- [ ] `client.conf`
- [ ] `mbedTLS`
- [ ] `user2`

## If something is wrong

Re-roll with the failing card's text pasted verbatim at the end of the
prompt as an explicit correction, for example:

> Card 7 must show the number 7 and the heading exactly as: ...

That is usually enough. Regenerating the whole image unchanged rarely is.
