"""Изометрические иллюстрации Хайвилла в коде (SVG) по реальным фото: ЖК целиком, башня с аркой-вывеской,
двор с фонтаном и обелиском, ряд башен. Стилизация, не копия."""
import math
C, S = math.cos(math.radians(30)), math.sin(math.radians(30))
BB = None  # bbox tracker

def P(x, y, z, ox, oy, k):
    p = (ox + (x - y) * C * k, oy + (x + y) * S * k - z * k)
    if BB is not None:
        BB[0] = min(BB[0], p[0]); BB[1] = min(BB[1], p[1]); BB[2] = max(BB[2], p[0]); BB[3] = max(BB[3], p[1])
    return p

def poly(pts, fill, op=1):
    d = ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)
    return f'<polygon points="{d}" fill="{fill}" opacity="{op}" stroke="{fill}" stroke-width=".6" stroke-linejoin="round"/>'

def box(x, y, z, w, d, h, top, left, right, o, win=None):
    ox, oy, k = o
    p = lambda a, b, c: P(a, b, c, ox, oy, k)
    out = [poly([p(x, y + d, z), p(x + w, y + d, z), p(x + w, y + d, z + h), p(x, y + d, z + h)], left),
           poly([p(x + w, y, z), p(x + w, y + d, z), p(x + w, y + d, z + h), p(x + w, y, z + h)], right),
           poly([p(x, y, z + h), p(x + w, y, z + h), p(x + w, y + d, z + h), p(x, y + d, z + h)], top)]
    if win:
        wc, fl, cl, cr = win
        for r in range(int(h / fl)):
            zz, hh = z + r * fl + fl * .35, fl * .45
            for c in range(cl):
                a = x + (c + .25) * w / cl; b = a + .5 * w / cl
                out.append(poly([p(a, y + d, zz), p(b, y + d, zz), p(b, y + d, zz + hh), p(a, y + d, zz + hh)], wc))
            for c in range(cr):
                a = y + (c + .25) * d / cr; b = a + .5 * d / cr
                out.append(poly([p(x + w, a, zz), p(x + w, b, zz), p(x + w, b, zz + hh), p(x + w, a, zz + hh)], wc, .85))
    return ''.join(out)

def tree(x, y, r, o, z=0):
    ox, oy, k = o
    cx, cy = P(x, y, z, ox, oy, k); P(x, y, z + 1.6 + 2 * r, ox, oy, k)
    return (f'<ellipse cx="{cx:.1f}" cy="{cy + 2:.1f}" rx="{r * k * .9:.1f}" ry="{r * k * .45:.1f}" fill="#000" opacity=".12"/>'
            f'<rect x="{cx - .25 * k:.1f}" y="{cy - 1.6 * k:.1f}" width="{.5 * k:.1f}" height="{1.6 * k:.1f}" fill="#7A5B45"/>'
            f'<circle cx="{cx:.1f}" cy="{cy - (1.6 + r) * k:.1f}" r="{r * k:.1f}" fill="#4F9A6B"/>'
            f'<circle cx="{cx - r * k * .3:.1f}" cy="{cy - (1.6 + r * 1.25) * k:.1f}" r="{r * k * .55:.1f}" fill="#71B988"/>')

def pine(x, y, h, o):
    ox, oy, k = o
    cx, cy = P(x, y, 0, ox, oy, k); P(x, y, h, ox, oy, k)
    w = h * .32 * k
    return (f'<ellipse cx="{cx:.1f}" cy="{cy + 2:.1f}" rx="{w * .8:.1f}" ry="{w * .4:.1f}" fill="#000" opacity=".12"/>'
            f'<polygon points="{cx:.1f},{cy - h * k:.1f} {cx - w:.1f},{cy - h * .25 * k:.1f} {cx + w:.1f},{cy - h * .25 * k:.1f}" fill="#3F7F5A"/>'
            f'<polygon points="{cx:.1f},{cy - h * k:.1f} {cx:.1f},{cy - h * .25 * k:.1f} {cx + w:.1f},{cy - h * .25 * k:.1f}" fill="#356F4E"/>'
            f'<rect x="{cx - .2 * k:.1f}" y="{cy - h * .25 * k:.1f}" width="{.4 * k:.1f}" height="{h * .25 * k:.1f}" fill="#7A5B45"/>')

def person(x, y, o, c='#1768CE'):
    ox, oy, k = o
    cx, cy = P(x, y, 0, ox, oy, k); P(x, y, 2.2, ox, oy, k)
    return (f'<ellipse cx="{cx:.1f}" cy="{cy + 1:.1f}" rx="{.6 * k:.1f}" ry="{.3 * k:.1f}" fill="#000" opacity=".15"/>'
            f'<rect x="{cx - .35 * k:.1f}" y="{cy - 1.7 * k:.1f}" width="{.7 * k:.1f}" height="{1.7 * k:.1f}" rx="{.35 * k:.1f}" fill="{c}"/>'
            f'<circle cx="{cx:.1f}" cy="{cy - 2.05 * k:.1f}" r="{.38 * k:.1f}" fill="#E8B89A"/>')

CREAM = ('#F4EBDD', '#E3D3BC', '#CDBA9F')
BRICK = ('#C98B73', '#B47660', '#9E6450')
WIN = '#6E8FB5'

def tower(x, y, z, w, d, h, o):
    out = box(x, y, z, w, d, h, *CREAM, o, win=(WIN, 1.0, 4, 3))
    out += box(x + w * .42, y + d - .01, z, w * .16, .3, h + 1.2, '#C9D3DE', '#A9B8C9', '#93A4B8', o)
    out += box(x + .5, y + .5, z + h, w - 1, d - 1, 1.6, '#EFE4D3', '#D9C7AE', '#C3AE91', o)
    out += box(x - .2, y - .2, z + h + 1.6, w + .4, d + .4, .45, '#B9A688', '#A8957A', '#97856B', o)
    out += box(x + w * .3, y + d * .3, z + h + 2.05, w * .4, d * .4, 1.2, '#E9DDCB', '#CDB99C', '#B8A386', o)
    return out

def board(w, d, o, lawn='#CFE0C3'):
    ox, oy, k = o
    s = box(-1, -1, -1.2, w + 2, d + 2, 1.2, '#FFFFFF', '#E3E9F2', '#CFD8E5', o)
    s += poly([P(0, 0, 0, ox, oy, k), P(w, 0, 0, ox, oy, k), P(w, d, 0, ox, oy, k), P(0, d, 0, ox, oy, k)], lawn)
    return s

def svg(parts, pad=18):
    x0, y0, x1, y1 = BB
    return (f'<svg viewBox="{x0 - pad:.0f} {y0 - pad:.0f} {x1 - x0 + 2 * pad:.0f} {y1 - y0 + 2 * pad:.0f}" '
            f'width="{x1 - x0 + 2 * pad:.0f}" height="{y1 - y0 + 2 * pad:.0f}" xmlns="http://www.w3.org/2000/svg">{"".join(parts)}</svg>')

def _start():
    global BB
    BB = [1e9, 1e9, -1e9, -1e9]

def complex_():
    """Весь ЖК: стилобат, пять башен, двор с фонтаном."""
    _start(); o = (450, 300, 13.0); ox, oy, k = o
    s = [board(20, 20, o)]
    s.append(poly([P(9, 0, .01, *o), P(11, 0, .01, *o), P(11, 20, .01, *o), P(9, 20, .01, *o)], '#E8DFD0'))
    s.append(poly([P(0, 9, .01, *o), P(20, 9, .01, *o), P(20, 11, .01, *o), P(0, 11, .01, *o)], '#E8DFD0'))
    s.append(box(1, 1, 0, 18, 5, 2.2, *BRICK, o, win=('#F3D9B0', 1.1, 9, 2)))
    s.append(box(14, 6, 0, 5, 12, 2.2, *BRICK, o, win=('#F3D9B0', 1.1, 2, 6)))
    T = [(2, 1.5, 2.2, 4.2, 3.6, 15), (8, 1.5, 2.2, 4.2, 3.6, 21), (14.5, 1.5, 2.2, 4, 3.6, 17), (14.8, 7.5, 2.2, 3.8, 4, 23), (14.8, 13.3, 2.2, 3.8, 4, 13)]
    for t in sorted(T, key=lambda t: t[0] + t[1]):
        s.append(tower(*t, o))
    cx, cy = P(9.5, 14, 0, *o)
    s.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{2.2 * k:.0f}" ry="{1.1 * k:.0f}" fill="#9CC7EC" stroke="#E8DFD0" stroke-width="6"/>')
    tp = P(9.5, 14, 6, *o)
    s.append(f'<polygon points="{cx - 7:.0f},{cy:.0f} {cx + 7:.0f},{cy:.0f} {tp[0]:.0f},{tp[1]:.0f}" fill="#B47660"/>')
    for tx, ty, r in sorted([(3, 9, 1.3), (6, 13, 1.5), (3, 16, 1.2), (7, 18, 1.4), (12, 17, 1.3), (5, 7.5, 1.0), (18.5, 19, 1.1), (1.5, 12, 1.1)], key=lambda t: t[0] + t[1]):
        s.append(tree(tx, ty, r, o))
    return svg(s)

def gate():
    """Башня и тёмная арка-мост с вывеской HIGHVILL ASTANA (фото 1)."""
    _start(); o = (450, 300, 14.0); ox, oy, k = o
    s = [board(16, 12, o, lawn='#E8DFD0')]
    s.append(box(3, 0.5, 0, 9, 7, 3, *BRICK, o, win=('#F3D9B0', 1.2, 6, 4)))
    s.append(tower(4.5, 1, 3, 6, 5, 22, o))
    # bridge: two legs + span in front (y ~ 9..11)
    for tx, ty, r in [(1, 3, 1.2), (14.5, 2, 1.3), (15, 6, 1.0)]:
        s.append(tree(tx, ty, r, o))
    dark = ('#4A5566', '#2E3846', '#3B4656')
    s.append(box(1, 9, 0, 1.6, 2, 6, *dark, o))
    s.append(box(13, 9, 0, 1.6, 2, 6, *dark, o))
    s.append(box(0.5, 9, 6, 14.6, 2, 2.6, *dark, o))
    # sign text on the left face (y = 11), along x
    a = P(2.2, 11, 6.9, *o)
    s.append(f'<text transform="matrix({C:.3f},{S:.3f},0,1,{a[0]:.1f},{a[1]:.1f})" font-family="Inter" font-weight="800" '
             f'font-size="{1.25 * k:.1f}" letter-spacing="2" fill="#F2F2F2">HIGHVILL ASTANA</text>')
    s.append(person(7, 12.5, o, '#FFC94D')); s.append(person(8.3, 12.2, o))
    return svg(s)

def courtyard():
    """Двор: фонтан с обелиском, аркады, деревья, люди (фото 2 и фонтан)."""
    _start(); o = (450, 300, 13.0); ox, oy, k = o
    s = [board(18, 18, o, lawn='#D6E6CC')]
    s.append(poly([P(4, 8.5, .01, *o), P(14, 8.5, .01, *o), P(14, 16, .01, *o), P(4, 16, .01, *o)], '#EDE4D4'))
    s.append(tower(1, 0.5, 0, 5.5, 4.5, 17, o))
    s.append(tower(10.5, 0.5, 0, 6, 4.5, 21, o))
    s.append(box(0, 5.2, 0, 18, 2.2, 4, *BRICK, o))
    for i in range(6):
        ax = 1 + i * 2.8
        pts = [P(ax, 7.4, 0, *o), P(ax + 1.6, 7.4, 0, *o), P(ax + 1.6, 7.4, 2.2, *o), P(ax + .8, 7.4, 3, *o), P(ax, 7.4, 2.2, *o)]
        s.append(poly(pts, '#7E4A3A'))
    cx, cy = P(9, 12.2, 0, *o)
    s.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{3.2 * k:.0f}" ry="{1.6 * k:.0f}" fill="#9CC7EC" stroke="#E1D6C3" stroke-width="8"/>')
    for dx in (-2.4, -1.4, 1.4, 2.4):
        s.append(f'<path d="M{cx + dx * k:.0f} {cy - 2:.0f} Q{cx + dx * k * .5:.0f} {cy - 4.5 * k:.0f} {cx + dx * k * .15:.0f} {cy - .6 * k:.0f}" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity=".95"/>')
    tp = P(9, 12.2, 8, *o)
    s.append(f'<polygon points="{cx - 10:.0f},{cy:.0f} {cx + 10:.0f},{cy:.0f} {tp[0]:.0f},{tp[1]:.0f}" fill="#B47660"/>')
    s.append(f'<polygon points="{cx:.0f},{cy:.0f} {cx + 10:.0f},{cy:.0f} {tp[0]:.0f},{tp[1]:.0f}" fill="#9E6450"/>')
    items = [(2, 10, 'p'), (2, 15, 'p'), (16, 10, 'p'), (16.2, 15.5, 'p'), (5.5, 17.2, 't'), (13, 17.2, 't')]
    for x, y, t in sorted(items, key=lambda a: a[0] + a[1]):
        s.append(pine(x, y, 6, o) if t == 'p' else tree(x, y, 1.1, o))
    s.append(person(6.2, 13.8, o, '#FFC94D')); s.append(person(6.9, 14.4, o)); s.append(person(12.2, 10.6, o, '#0B2545'))
    return svg(s)

def skyline():
    """Ряд башен вдоль улицы (фото 3): разные высоты и короны."""
    _start(); o = (450, 300, 12.0); ox, oy, k = o
    s = [board(26, 8, o, lawn='#D6E6CC')]
    s.append(poly([P(0, 6, .01, *o), P(26, 6, .01, *o), P(26, 8, .01, *o), P(0, 8, .01, *o)], '#C9CED6'))
    s.append(box(0.5, 0.5, 0, 25, 4.5, 2, *BRICK, o, win=('#F3D9B0', 1.0, 12, 2)))
    for x, h in [(1, 14), (6.2, 22), (11.4, 17), (16.6, 25), (21.6, 12)]:
        s.append(tower(x, 1, 2, 4, 3.6, h, o))
    for i in range(7):
        s.append(tree(1.5 + i * 3.8, 5.5, 1.0, o))
    return svg(s)

if __name__ == '__main__':
    import sys
    out = sys.argv[1]
    for n, f in [('complex', complex_), ('gate', gate), ('courtyard', courtyard), ('skyline', skyline)]:
        open(f'{out}/{n}.svg', 'w').write(f())
