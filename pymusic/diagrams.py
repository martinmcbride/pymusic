# Author:  Martin McBride
# Created: 2026-05-16
# Copyright (C) 2026, Martin McBride
# License: MIT
from generativepy.color import Color, BookColorScheme
from generativepy.drawing import make_image, setup
from generativepy.geometry import Transform, Line, Circle, Ellipse, Text
from genpygoodies.geomutils import LN

from notes import *

FONT = "DejaVu Sans"

cs = BookColorScheme()

FONT_SIZE = 30

STAFF_TOP = 60
STAFF_LEFT = 40
STAFF_STEP = 30
STAFF_RIGHT = 1600

LABELS = ("A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#")
NOTES =  (C2, D2, E2, F2, G2, A3 , B3, C3, D3, E3, F3, G3, A4 , B4, C4, D4, E4, F4, G4, A5 , B5, C5, D5, E5, F5, G5, A6)

A0 = 21
As0 = 22
B0 = 23
C0 = 24
Cs0 = 25
D0 = 26
Ds0 = 27
E0 = 28
F0 = 29
Fs0 = 30
G0 = 31
Gs0 = 32


def draw_staff(ctx, title):
    for i in range(5):
        Line(ctx).of_start_end((STAFF_LEFT, STAFF_TOP + i * STAFF_STEP), (STAFF_RIGHT, STAFF_TOP + i * STAFF_STEP)).stroke(LN(cs.BLACK))

    for i in range(6, 11):
        Line(ctx).of_start_end((STAFF_LEFT, STAFF_TOP + i * STAFF_STEP), (STAFF_RIGHT, STAFF_TOP + i * STAFF_STEP)).stroke(LN(cs.BLACK))

    Text(ctx).of(title, ((STAFF_LEFT+STAFF_RIGHT)/2, 400)).size(40).font(FONT).align_center().align_middle().fill(cs.BLACK)


def get_note_name(midi_value : int, sharps : tuple):
    n = midi_value - 21
    a = n // 12
    b = n % 12
    if b in sharps:
        b += 1
    return LABELS[b] + str(a)

def draw_notes(ctx, sharps):
    for i, n in enumerate(NOTES[::-1]):
        centre = (STAFF_LEFT + i*STAFF_STEP*2, STAFF_TOP+(i - 2)*STAFF_STEP/2)
        Ellipse(ctx).of_center_radius(centre, STAFF_STEP, STAFF_STEP/2).fill(cs.WHITE).stroke(LN(cs.BLACK))
        Text(ctx).of(get_note_name(n, sharps), centre).size(20).font(FONT).align_center().align_middle().fill(cs.BLACK)

# Draw staff and tab notation diagrams

def staff_for_key(filename : str, title : str, sharps):
    # sharps is an array of all teh motes tthat are sharp in the given key. Notes are numbered from A as 0
    # A  A#  B   C  C#  D  D#  E   F  F#  G  G#
    # 0  1   2   3  4   5  6   7   8  9   10 11
    def draw(ctx, width, height, fn, frame_count):
        setup(ctx, width, height,  background=Color(1))

        draw_staff(ctx, title)
        draw_notes(ctx, sharps)

    make_image(filename, draw, 1700, 500)



staff_for_key("key-c-major.png", "Key C Major", [])
staff_for_key("key-a-major.png", "Key A Major", [3, 8, 10])