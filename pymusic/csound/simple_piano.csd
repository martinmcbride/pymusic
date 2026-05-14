<CsoundSynthesizer>
<CsOptions>
-odac
</CsOptions>

<CsInstruments>

sr     = 48000
ksmps  = 32
nchnls = 2
0dbfs  = 1

giSine ftgen 1, 0, 16384, 10, 1

instr Piano

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

; Twinkle-ish simple melody
;     start dur midi amp

i "Piano" 0.0  1.0 60 0.4
i "Piano" 1.0  1.0 60 0.4
i "Piano" 2.0  1.0 67 0.4
i "Piano" 3.0  1.0 67 0.4
i "Piano" 4.0  1.0 69 0.4
i "Piano" 5.0  1.0 69 0.4
i "Piano" 6.0  2.0 67 0.5

i "Piano" 8.0  1.0 65 0.4
i "Piano" 9.0  1.0 65 0.4
i "Piano" 10.0 1.0 64 0.4
i "Piano" 11.0 1.0 64 0.4
i "Piano" 12.0 1.0 62 0.4
i "Piano" 13.0 1.0 62 0.4
i "Piano" 14.0 2.0 60 0.5

e

</CsScore>
</CsoundSynthesizer>