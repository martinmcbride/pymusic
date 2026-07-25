<CsoundSynthesizer>
<CsOptions>
-odac -d
</CsOptions>
<CsInstruments>

sr     = {sample_rate}
ksmps  = 32
nchnls = {channels}
0dbfs  = 1

; ============================================================
;  Instrument 1 — Plucked Acoustic Guitar
;  p4 = amplitude (0-1)
;  p5 = pitch midi
;  p6 = pluck position (0.1 = near bridge, 0.5 = middle)
; ============================================================
instr 1
    iamp   = p5
    ifreq  = cpsmidinn(p4)
    ipluck = p6

    ; --- Karplus-Strong plucked string ---
    ; pluck: kamp, kcps, icps, ifn, imeth
    ;   imeth=1 → simple averaging (natural decay)
    aplk   pluck iamp, ifreq, ifreq, 0, 1

    ; --- Pluck-position comb filter ---
    ; Creates the characteristic spectral notches of where the string is plucked
    idel   = ipluck / ifreq
    adel   delay aplk, idel
    acomb  = aplk - adel

    ; --- Body resonance (two resonant band-pass filters) ---
    ; Approximates the Helmholtz + top-plate modes of a guitar body
    abody1 reson acomb, 110, 80, 1     ; ~110 Hz body resonance
    abody2 reson acomb, 220, 120, 1    ; ~220 Hz top-plate resonance
    abody  = acomb + 0.3*abody1 + 0.2*abody2

    ; --- Amplitude envelope (gentle attack, natural exponential release) ---
    aenv   expsegr 1, p3, 0.3, 0.4, 0.001
    aout   = abody * aenv * 0.6

    ; --- Stereo output with slight width ---
    outs   aout, aout
endin

</CsInstruments>

<CsScore>
; -------------------------------------------------------------
; p1  p2(start)  p3(dur)  p4(pitch)  p5(amp)  p6(pluck-pos)
; pluck-pos 0.1 near bridge, 0.5 middle
; -------------------------------------------------------------

t 0 {bpm}
{score}

e
</CsScore>
</CsoundSynthesizer>