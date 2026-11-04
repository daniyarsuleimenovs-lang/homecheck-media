"""Flat illustrations for HomeCheck slides (style B), drawn as SVG.

Palette: one blue family + white + warm yellow window light + soft green trees.
Every scene is drawn for the bottom zone of a slide (full width, ground at the bottom)
and is then processed like photos (see treat() in render.py).
"""
import random

NAVY = '#0B2545'
MID = '#1F4E8C'
BLUE = '#2D8CFF'
LBLUE = '#8EC2FA'
PALE = '#A9CCF2'
BG = '#BBD6F2'
WHITE = '#FFFFFF'
TINT = '#EAF3FF'
YEL = '#FFC94D'
GREEN = '#4FA67F'
GREEN2 = '#6CBF96'


class _Svg:
    def __init__(self, w, h):
        self.w, self.h, self.parts = w, h, []

    def add(self, s):
        self.parts.append(s)

    def done(self, mirror=False):
        body = '\n'.join(self.parts)
        if mirror:
            body = f'<g transform="translate({self.w},0) scale(-1,1)">{body}</g>'
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}"><rect width="{self.w}" height="{self.h}" fill="{BG}"/>'
                f'{body}</svg>')


def _windows(s, rnd, x, top, w, h, style):
    """Varied window patterns so buildings don't look identical."""
    if style == 'grid':
        ww, wh, gx, gy = 34, 40, 18, 30
    elif style == 'wide':
        ww, wh, gx, gy = 62, 34, 16, 34
    elif style == 'tall':
        ww, wh, gx, gy = 26, 56, 20, 22
    else:  # ribbon: horizontal glass bands
        y = top + 28
        while y + 30 < top + h - 20:
            s.add(f'<rect x="{x+14}" y="{y}" width="{w-28}" height="26" rx="3" fill="{LBLUE}"/>')
            for k in range(3):
                if rnd.random() < 0.25:
                    lx = x + 14 + rnd.randint(0, max(1, w - 70))
                    s.add(f'<rect x="{lx}" y="{y}" width="40" height="26" rx="3" fill="{YEL}"/>')
            y += 56
        return
    cols = max(2, (w - 24) // (ww + gx))
    span = cols * ww + (cols - 1) * gx
    x0 = x + (w - span) // 2
    y = top + 26
    while y + wh < top + h - 30:
        for c in range(cols):
            col = YEL if rnd.random() < 0.10 else LBLUE
            wx = x0 + c * (ww + gx)
            s.add(f'<rect x="{wx}" y="{y}" width="{ww}" height="{wh}" rx="3" fill="{col}"/>')
            if style in ('grid', 'tall'):
                s.add(f'<rect x="{wx + ww//2 - 1}" y="{y}" width="3" height="{wh}" fill="{WHITE}" opacity="0.7"/>')
        y += wh + gy


def _building(s, rnd, x, w, h, ground, body=WHITE, style='grid', balconies=False, core=False):
    top = ground - h
    s.add(f'<rect x="{x}" y="{top}" width="{w}" height="{h}" fill="{body}"/>')
    s.add(f'<rect x="{x-6}" y="{top-8}" width="{w+12}" height="12" rx="3" fill="{BLUE}"/>')
    _windows(s, rnd, x, top, w, h, style)
    if balconies:
        y = top + 66
        while y < ground - 40:
            s.add(f'<rect x="{x-8}" y="{y}" width="{w//2}" height="14" rx="2" fill="{BLUE}"/>')
            y += 70
    if core:
        s.add(f'<rect x="{x + w//2 - 20}" y="{top + 20}" width="40" height="{h - 20}" fill="{MID}"/>')
    return top


def _tree(s, x, ground, h, color):
    s.add(f'<rect x="{x-4}" y="{ground - h*0.4:.0f}" width="8" height="{h*0.4:.0f}" rx="4" fill="{MID}"/>')
    s.add(f'<ellipse cx="{x}" cy="{ground - h*0.62:.0f}" rx="{h*0.22:.0f}" ry="{h*0.34:.0f}" fill="{color}"/>')


def city(w=1080, h=900, seed=7, mirror=False, magnifier=False):
    """Panorama of a residential quarter; optional magnifier over the main building."""
    rnd = random.Random(seed)
    s = _Svg(w, h)
    ground = h - 40
    k = max(0.55, (h - 40) / 860)  # scene designed for h=900; building heights follow the strip height
    x = 0
    while x < w:  # far skyline
        bw, bh = rnd.randint(70, 130), int(rnd.randint(160, 300) * k)
        s.add(f'<rect x="{x}" y="{ground-bh}" width="{bw}" height="{bh}" fill="{PALE}"/>')
        x += bw + rnd.randint(0, 12)
    # Front row: layout varies with the seed (widths, heights, window styles), so scenes in one post differ.
    plan, gaps, x = [], [], rnd.randint(-30, 20)
    while x < w - 60:
        bw = rnd.randint(140, 250)
        bh = rnd.randint(360, 640)
        plan.append((x, bw, bh, rnd.choice([WHITE, WHITE, TINT]), rnd.choice(['grid', 'wide', 'tall', 'ribbon']),
                     rnd.random() < 0.45, rnd.random() < 0.3))
        gap = rnd.randint(24, 70)
        gaps.append(x + bw + gap // 2)
        x += bw + gap
    main = max(plan, key=lambda b: b[2] if 520 < b[0] + b[1] // 2 < 960 else 0)
    main_top = None
    for bx, bw, bh, body, style, balc, core in plan:
        top = _building(s, rnd, bx, bw, int(bh * k), ground, body, style, balc, core)
        if (bx, bw) == main[:2]:
            main_top, main_cx = top, bx + bw // 2
    for tx in gaps:
        if rnd.random() < 0.8:
            _tree(s, tx, ground, rnd.randint(110, 170), rnd.choice([GREEN, GREEN2]))
    s.add(f'<rect x="0" y="{ground}" width="{w}" height="40" fill="{PALE}"/>')
    if magnifier:
        cx, cy, r = main_cx, main_top + int(230 * min(k, 1.4)), 100
        s.add(f'<defs><clipPath id="lens"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath></defs>')
        s.add(f'<g clip-path="url(#lens)"><rect x="{cx-r}" y="{cy-r}" width="{2*r}" height="{2*r}" fill="{WHITE}"/>')
        for dx, dy, col in [(-80, -78, LBLUE), (6, -78, YEL), (-80, 8, LBLUE), (6, 8, LBLUE)]:
            s.add(f'<rect x="{cx+dx}" y="{cy+dy}" width="74" height="70" rx="6" fill="{col}"/>')
        s.add('</g>')
        s.add(f'<line x1="{cx+72}" y1="{cy+72}" x2="{cx+160}" y2="{cy+160}" stroke="{NAVY}" stroke-width="32" stroke-linecap="round"/>')
        s.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{NAVY}" stroke-width="22"/>')
    return s.done(mirror)
