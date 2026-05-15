<CsoundSynthesizer>
<CsOptions>
-odac
</CsOptions>

<CsInstruments>

sr     = {sample_rate}
ksmps  = 32
nchnls = {channels}
0dbfs  = 1

giSine ftgen 1, 0, 16384, 10, 1

instr 1

    ; p4 = MIDI note
    ; p5 = amplitude

    iFreq = cpsmidinn(p4)
    iAmp  = p5

    ; Envelope
    aEnv  linsegr 0, 0.01, 1, 0.2, 0.5, 1.5, 0

    ; Simple piano-like tone:
    ; fundamental + harmonics
    a1 oscili iAmp * 0.7, iFreq,     giSine
    a2 oscili iAmp * 0.2, iFreq * 2, giSine
    a3 oscili iAmp * 0.1, iFreq * 3, giSine

    ; Slight brightness decay
    aTone = (a1 + a2 + a3) * aEnv

    ; Gentle lowpass filter
    aFilt tone aTone, 4000

    ; Stereo output
    outs aFilt, aFilt

endin

</CsInstruments>

<CsScore>

t 0 120

{score}

e

</CsScore>
</CsoundSynthesizer>