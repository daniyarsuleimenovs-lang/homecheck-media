"""Изометрические иллюстрации Хайвилла в коде (SVG) по реальным фото и описаниям района:
ЖК с пирамидой Дворца мира и согласия на закате, башня с аркой-вывеской, ночной ряд башен,
квартира в разрезе, двор с фонтаном, ЖК зимой. Стилизация, не копия."""
import math
import random

C, S = math.cos(math.radians(30)), math.sin(math.radians(30))
BB = None
TH = {}


def theme(name):
    global CREAM, BRICK, WIN, LAWN, LIT, SNOW, CROWN, BOARD, PAVE
    TH['name'] = name
    BOARD = ('#FFFFFF', '#E3E9F2', '#CFD8E5')
    PAVE = '#E8DFD0'
    if name == 'night':
        CREAM, BRICK, WIN, LAWN = ('#5B6A86', '#45536E', '#36435B'), ('#6B4A4A', '#563B3C', '#47312F'), '#26324A', '#2F4A45'
        LIT, CROWN, BOARD, PAVE = .55, ('#6E7C96', '#56637C', '#4A566D'), ('#3A4A66', '#2A3850', '#22304A'), '#3C4A62'
    elif name == 'winter':
        CREAM, BRICK, WIN, LAWN = ('#F8F3EA', '#E6D8C4', '#D2C1A8'), ('#C98B73', '#B47660', '#9E6450'), '#7D9CC0', '#F3F7FC'
        LIT, CROWN, PAVE = 0, ('#FFFFFF', '#E9EEF5', '#D6DEEA'), '#DCE4EE'
    else:
        CREAM, BRICK, WIN, LAWN = ('#F4EBDD', '#E3D3BC', '#CDBA9F'), ('#C98B73', '#B47660', '#9E6450'), '#6E8FB5', '#CFE0C3'
        LIT, CROWN = (.15 if name == 'sunset' else 0), ('#B9A688', '#A8957A', '#97856B')
        if name == 'sunset':
            CREAM, WIN = ('#F8E6CF', '#EBCDAA', '#D4B08A'), '#7F8FB0'
    SNOW = name == 'winter'


theme('day')


def P(x, y, z, ox, oy, k):
    p = (ox + (x - y) * C * k, oy + (x + y) * S * k - z * k)
    if BB is not None:
        BB[0] = min(BB[0], p[0]); BB[1] = min(BB[1], p[1]); BB[2] = max(BB[2], p[0]); BB[3] = max(BB[3], p[1])
    return p


def poly(pts, fill, op=1):
    d = ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)
    return f'<polygon points="{d}" fill="{fill}" opacity="{op}" stroke="{fill}" stroke-width=".6" stroke-linejoin="round"/>'


def lit(c):
    return '#FFD27A' if c == WIN and random.random() < LIT else c


def box(x, y, z, w, d, h, top, left, right, o, win=None):
    p = lambda a, b, c: P(a, b, c, *o)
    out = [poly([p(x, y + d, z), p(x + w, y + d, z), p(x + w, y + d, z + h), p(x, y + d, z + h)], left),
           poly([p(x + w, y, z), p(x + w, y + d, z), p(x + w, y + d, z + h), p(x + w, y, z + h)], right),
           poly([p(x, y, z + h), p(x + w, y, z + h), p(x + w, y + d, z + h), p(x, y + d, z + h)], top)]
    if win:
        wc, fl, cl, cr = win
        for r in range(int(h / fl)):
            zz, hh = z + r * fl + fl * .35, fl * .45
            for c in range(cl):
                a = x + (c + .25) * w / cl; b = a + .5 * w / cl
                out.append(poly([p(a, y + d, zz), p(b, y + d, zz), p(b, y + d, zz + hh), p(a, y + d, zz + hh)], lit(wc)))
            for c in range(cr):
                a = y + (c + .25) * d / cr; b = a + .5 * d / cr
                out.append(poly([p(x + w, a, zz), p(x + w, b, zz), p(x + w, b, zz + hh), p(x + w, a, zz + hh)], lit(wc), .85))
    return ''.join(out)


def tree(x, y, r, o, z=0):
    ox, oy, k = o
    cx, cy = P(x, y, z, *o); P(x, y, z + 1.6 + 2 * r, *o)
    night = TH['name'] == 'night'
    c1 = '#C9D6E3' if SNOW else ('#2E5A48' if night else '#4F9A6B')
    c2 = '#FFFFFF' if SNOW else ('#3C6E58' if night else '#71B988')
    return (f'<ellipse cx="{cx:.1f}" cy="{cy + 2:.1f}" rx="{r * k * .9:.1f}" ry="{r * k * .45:.1f}" fill="#000" opacity=".12"/>'
            f'<rect x="{cx - .25 * k:.1f}" y="{cy - 1.6 * k:.1f}" width="{.5 * k:.1f}" height="{1.6 * k:.1f}" fill="#7A5B45"/>'
            f'<circle cx="{cx:.1f}" cy="{cy - (1.6 + r) * k:.1f}" r="{r * k:.1f}" fill="{c1}"/>'
            f'<circle cx="{cx - r * k * .3:.1f}" cy="{cy - (1.6 + r * 1.25) * k:.1f}" r="{r * k * .55:.1f}" fill="{c2}"/>')


def pine(x, y, h, o):
    ox, oy, k = o
    cx, cy = P(x, y, 0, *o); P(x, y, h, *o)
    w = h * .32 * k
    a, b = ('#3F7F5A', '#356F4E')
    out = (f'<ellipse cx="{cx:.1f}" cy="{cy + 2:.1f}" rx="{w * .8:.1f}" ry="{w * .4:.1f}" fill="#000" opacity=".12"/>'
           f'<polygon points="{cx:.1f},{cy - h * k:.1f} {cx - w:.1f},{cy - h * .25 * k:.1f} {cx + w:.1f},{cy - h * .25 * k:.1f}" fill="{a}"/>'
           f'<polygon points="{cx:.1f},{cy - h * k:.1f} {cx:.1f},{cy - h * .25 * k:.1f} {cx + w:.1f},{cy - h * .25 * k:.1f}" fill="{b}"/>'
           f'<rect x="{cx - .2 * k:.1f}" y="{cy - h * .25 * k:.1f}" width="{.4 * k:.1f}" height="{h * .25 * k:.1f}" fill="#7A5B45"/>')
    return out


def person(x, y, o, c='#1768CE'):
    ox, oy, k = o
    cx, cy = P(x, y, 0, *o); P(x, y, 2.2, *o)
    return (f'<ellipse cx="{cx:.1f}" cy="{cy + 1:.1f}" rx="{.6 * k:.1f}" ry="{.3 * k:.1f}" fill="#000" opacity=".15"/>'
            f'<rect x="{cx - .35 * k:.1f}" y="{cy - 1.7 * k:.1f}" width="{.7 * k:.1f}" height="{1.7 * k:.1f}" rx="{.35 * k:.1f}" fill="{c}"/>'
            f'<circle cx="{cx:.1f}" cy="{cy - 2.05 * k:.1f}" r="{.38 * k:.1f}" fill="#E8B89A"/>')


def tower(x, y, z, w, d, h, o):
    out = box(x, y, z, w, d, h, *CREAM, o, win=(WIN, 1.0, 4, 3))
    out += box(x + w * .42, y + d - .01, z, w * .16, .3, h + 1.2, '#C9D3DE', '#A9B8C9', '#93A4B8', o)
    out += box(x + .5, y + .5, z + h, w - 1, d - 1, 1.6, *CREAM, o)
    out += box(x - .2, y - .2, z + h + 1.6, w + .4, d + .4, .45, *CROWN, o)
    out += box(x + w * .3, y + d * .3, z + h + 2.05, w * .4, d * .4, 1.2, *CREAM, o)
    return out


def board(w, d, o, lawn=None):
    s = box(-1, -1, -1.2, w + 2, d + 2, 1.2, *BOARD, o)
    s += poly([P(0, 0, 0, *o), P(w, 0, 0, *o), P(w, d, 0, *o), P(0, d, 0, *o)], LAWN if lawn is None else lawn)
    return s


def svg(parts, pad=18):
    x0, y0, x1, y1 = BB
    return (f'<svg viewBox="{x0 - pad:.0f} {y0 - pad:.0f} {x1 - x0 + 2 * pad:.0f} {y1 - y0 + 2 * pad:.0f}" '
            f'width="{x1 - x0 + 2 * pad:.0f}" height="{y1 - y0 + 2 * pad:.0f}" xmlns="http://www.w3.org/2000/svg">{"".join(parts)}</svg>')


def _start(name, seed):
    global BB
    theme(name); random.seed(seed)
    BB = [1e9, 1e9, -1e9, -1e9]


def _complex(s, o, dx=0):
    s.append(box(1 + dx, 1, 0, 18, 5, 2.2, *BRICK, o, win=('#F3D9B0', 1.1, 9, 2)))
    s.append(box(14 + dx, 6, 0, 5, 12, 2.2, *BRICK, o, win=('#F3D9B0', 1.1, 2, 6)))
    T = [(2, 1.5, 2.2, 4.2, 3.6, 15), (8, 1.5, 2.2, 4.2, 3.6, 21), (14.5, 1.5, 2.2, 4, 3.6, 17), (14.8, 7.5, 2.2, 3.8, 4, 23), (14.8, 13.3, 2.2, 3.8, 4, 13)]
    for t in sorted(T, key=lambda t: t[0] + t[1]):
        s.append(tower(t[0] + dx, *t[1:], o))


def complex_(name='day'):
    """Весь ЖК: стилобат, пять башен, двор с фонтаном."""
    _start(name, 1); o = (450, 300, 13.0); ox, oy, k = o
    s = [board(20, 20, o)]
    s.append(poly([P(9, 0, .01, *o), P(11, 0, .01, *o), P(11, 20, .01, *o), P(9, 20, .01, *o)], PAVE))
    s.append(poly([P(0, 9, .01, *o), P(20, 9, .01, *o), P(20, 11, .01, *o), P(0, 11, .01, *o)], PAVE))
    _complex(s, o)
    cx, cy = P(9.5, 14, 0, *o)
    s.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{2.2 * k:.0f}" ry="{1.1 * k:.0f}" fill="{"#E9EFF7" if SNOW else "#9CC7EC"}" stroke="{PAVE}" stroke-width="6"/>')
    tp = P(9.5, 14, 6, *o)
    s.append(f'<polygon points="{cx - 7:.0f},{cy:.0f} {cx + 7:.0f},{cy:.0f} {tp[0]:.0f},{tp[1]:.0f}" fill="#B47660"/>')
    items = [(3, 9, 1.3), (6, 13, 1.5), (3, 16, 1.2), (7, 18, 1.4), (12, 17, 1.3), (5, 7.5, 1.0), (18.5, 19, 1.1), (1.5, 12, 1.1)]
    for tx, ty, r in sorted(items, key=lambda t: t[0] + t[1]):
        s.append(pine(tx, ty, 4.5, o) if SNOW else tree(tx, ty, r, o))
    if SNOW:
        s.append(person(8, 16, o, '#E5484D')); s.append(person(8.8, 16.6, o, '#1768CE'))
    return svg(s)


def pyramid(x, y, b, h, o):
    p = lambda a, c, z: P(a, c, z, *o)
    ax = p(x + b / 2, y + b / 2, h)
    L, R = ('#C7D3DD', '#AEBCC9') if TH['name'] != 'night' else ('#4E6A8C', '#3D5677')
    out = poly([p(x, y + b, 0), p(x + b, y + b, 0), ax], L) + poly([p(x + b, y, 0), p(x + b, y + b, 0), ax], R)
    for f in (.25, .5, .75):
        z = h * f; sh = b * f / 2
        a, m, c = p(x + sh, y + b - sh, z), p(x + b - sh, y + b - sh, z), p(x + b - sh, y + sh, z)
        out += f'<polyline points="{a[0]:.1f},{a[1]:.1f} {m[0]:.1f},{m[1]:.1f} {c[0]:.1f},{c[1]:.1f}" fill="none" stroke="#FFFFFF" stroke-opacity=".55" stroke-width="2"/>'
    sh = b * .85 / 2
    out += poly([p(x + sh, y + b - sh, h * .85), p(x + b - sh, y + b - sh, h * .85), ax], '#F2D48B')
    out += poly([p(x + b - sh, y + sh, h * .85), p(x + b - sh, y + b - sh, h * .85), ax], '#E3C273')
    return out


def complex_pyramid(name='sunset'):
    """ЖК на закате, рядом пирамида Дворца мира и согласия."""
    _start(name, 3); o = (450, 300, 11.0)
    s = [board(32, 20, o)]
    s.append(poly([P(20.5, 0, .01, *o), P(22, 0, .01, *o), P(22, 20, .01, *o), P(20.5, 20, .01, *o)], '#C9CED6'))
    _complex(s, o)
    s.append(pyramid(23.5, 5, 8, 9, o))
    for tx, ty, r in sorted([(3, 9, 1.3), (6, 13, 1.5), (3, 16, 1.2), (7, 18, 1.4), (11, 15, 1.3), (24, 16, 1.1), (27, 16.5, 1.2), (30, 3, 1.0), (30, 15, 1.1)], key=lambda t: t[0] + t[1]):
        s.append(tree(tx, ty, r, o))
    return svg(s)


def gate(name='day'):
    """Башня и тёмная арка-мост с вывеской HIGHVILL ASTANA."""
    _start(name, 2); o = (450, 300, 14.0); ox, oy, k = o
    s = [board(16, 12, o, lawn=PAVE)]
    s.append(box(3, .5, 0, 9, 7, 3, *BRICK, o, win=('#F3D9B0', 1.2, 6, 4)))
    s.append(tower(4.5, 1, 3, 6, 5, 22, o))
    for tx, ty, r in [(1, 3, 1.2), (14.5, 2, 1.3), (15, 6, 1.0)]:
        s.append(tree(tx, ty, r, o))
    dark = ('#4A5566', '#2E3846', '#3B4656')
    s.append(box(1, 9, 0, 1.6, 2, 6, *dark, o))
    s.append(box(13, 9, 0, 1.6, 2, 6, *dark, o))
    s.append(box(.5, 9, 6, 14.6, 2, 2.6, *dark, o))
    a = P(2.2, 11, 6.9, *o)
    s.append(f'<text transform="matrix({C:.3f},{S:.3f},0,1,{a[0]:.1f},{a[1]:.1f})" font-family="Inter" font-weight="800" '
             f'font-size="{1.25 * k:.1f}" letter-spacing="2" fill="#F2F2F2">HIGHVILL ASTANA</text>')
    s.append(person(7, 12.5, o, '#FFC94D')); s.append(person(8.3, 12.2, o))
    return svg(s)


def courtyard(name='day'):
    """Двор: фонтан с обелиском, аркада, сосны, люди."""
    _start(name, 4); o = (450, 300, 13.0); ox, oy, k = o
    s = [board(18, 18, o, lawn='#D6E6CC')]
    s.append(poly([P(4, 8.5, .01, *o), P(14, 8.5, .01, *o), P(14, 16, .01, *o), P(4, 16, .01, *o)], '#EDE4D4'))
    s.append(tower(1, .5, 0, 5.5, 4.5, 17, o))
    s.append(tower(10.5, .5, 0, 6, 4.5, 21, o))
    s.append(box(0, 5.2, 0, 18, 2.2, 4, *BRICK, o))
    for i in range(6):
        ax = 1 + i * 2.8
        s.append(poly([P(ax, 7.4, 0, *o), P(ax + 1.6, 7.4, 0, *o), P(ax + 1.6, 7.4, 2.2, *o), P(ax + .8, 7.4, 3, *o), P(ax, 7.4, 2.2, *o)], '#7E4A3A'))
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


def skyline(name='night'):
    """Ночной ряд башен вдоль улицы, свет в окнах."""
    _start(name, 5); o = (450, 300, 12.0)
    s = [board(26, 8, o)]
    s.append(poly([P(0, 6, .01, *o), P(26, 6, .01, *o), P(26, 8, .01, *o), P(0, 8, .01, *o)], PAVE))
    s.append(box(.5, .5, 0, 25, 4.5, 2, *BRICK, o, win=('#F3D9B0', 1.0, 12, 2)))
    for x, h in [(1, 14), (6.2, 22), (11.4, 17), (16.6, 25), (21.6, 12)]:
        s.append(tower(x, 1, 2, 4, 3.6, h, o))
    for i in range(7):
        cx, cy = P(1.5 + i * 3.8, 7, 0, *o)
        s.append(f'<line x1="{cx:.0f}" y1="{cy:.0f}" x2="{cx:.0f}" y2="{cy - 40:.0f}" stroke="#8C98AE" stroke-width="3"/>'
                 f'<circle cx="{cx:.0f}" cy="{cy - 42:.0f}" r="6" fill="#FFD27A"/><circle cx="{cx:.0f}" cy="{cy - 42:.0f}" r="16" fill="#FFD27A" opacity=".25"/>')
    return svg(s)


def apartment():
    """Квартира в разрезе: гостиная с окном на башни."""
    _start('day', 6); o = (450, 300, 26.0)
    p = lambda a, b, c: P(a, b, c, *o)
    W, D, H = 12, 10, 7
    s = [box(-.4, -.4, -.5, W + .4, D + .4, .5, *BOARD, o)]
    s.append(poly([p(0, 0, 0), p(W, 0, 0), p(W, D, 0), p(0, D, 0)], '#E9D9C1'))
    for i in range(1, W):
        a, b = p(i, 0, 0), p(i, D, 0)
        s.append(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="#DCC8AB" stroke-width="2"/>')
    s.append(poly([p(0, 0, 0), p(W, 0, 0), p(W, 0, H), p(0, 0, H)], '#F3F7FC'))
    s.append(poly([p(0, 0, 0), p(0, D, 0), p(0, D, H), p(0, 0, H)], '#E4ECF6'))
    s.append(poly([p(5, 0, 1.6), p(10.5, 0, 1.6), p(10.5, 0, 6), p(5, 0, 6)], '#BFDDF7'))
    for a, hh in [(5.6, 3.2), (7.0, 3.9), (8.5, 3.0), (9.6, 3.6)]:
        s.append(poly([p(a, 0, 1.6), p(a + .9, 0, 1.6), p(a + .9, 0, 1.6 + hh), p(a, 0, 1.6 + hh)], '#E3D3BC'))
        s.append(poly([p(a - .1, 0, 1.6 + hh), p(a + 1.0, 0, 1.6 + hh), p(a + 1.0, 0, 1.9 + hh), p(a - .1, 0, 1.9 + hh)], '#B9A688'))
    a, b = p(7.75, 0, 1.6), p(7.75, 0, 6)
    s.append(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="#FFFFFF" stroke-width="6"/>')
    s.append(poly([p(5, 0, 1.6), p(10.5, 0, 1.6), p(10.5, .5, 1.6), p(5, .5, 1.6)], '#FFFFFF'))
    s.append(poly([p(0, 2.5, 3.2), p(0, 5, 3.2), p(0, 5, 5.2), p(0, 2.5, 5.2)], '#FFC94D'))
    s.append(poly([p(3, 3.5, .02), p(9, 3.5, .02), p(9, 8.5, .02), p(3, 8.5, .02)], '#BBD6F2'))
    s.append(box(.6, 3, 0, 2.4, 6, 1.4, '#2D5FA8', '#1F4E8F', '#2A58A0', o))
    s.append(box(.6, 3, 1.4, .8, 6, 1.4, '#2D5FA8', '#1F4E8F', '#2A58A0', o))
    s.append(box(5, 5, 0, 2.6, 1.8, .9, '#FFFFFF', '#E1D2BC', '#CDBDA6', o))
    s.append(box(10.4, 1, 0, 1, 1, 1.2, '#C98B73', '#B47660', '#9E6450', o))
    cx, cy = p(10.9, 1.5, 1.2)
    s.append(f'<circle cx="{cx:.0f}" cy="{cy - 30:.0f}" r="34" fill="#4F9A6B"/><circle cx="{cx - 14:.0f}" cy="{cy - 44:.0f}" r="20" fill="#71B988"/>')
    lx, ly = p(1.5, 9.2, 0); lt = p(1.5, 9.2, 4.6)
    s.append(f'<line x1="{lx:.0f}" y1="{ly:.0f}" x2="{lt[0]:.0f}" y2="{lt[1]:.0f}" stroke="#0B2545" stroke-width="5"/>'
             f'<polygon points="{lt[0] - 26:.0f},{lt[1] + 6:.0f} {lt[0] + 26:.0f},{lt[1] + 6:.0f} {lt[0] + 14:.0f},{lt[1] - 26:.0f} {lt[0] - 14:.0f},{lt[1] - 26:.0f}" fill="#FFC94D"/>')
    return svg(s)


SCENES = {'cover': complex_pyramid, 'gate': gate, 'skyline': skyline, 'apartment': apartment,
          'courtyard': courtyard, 'winter': lambda: complex_('winter')}

if __name__ == '__main__':
    import sys
    for n, f in SCENES.items():
        open(f'{sys.argv[1]}/{n}.svg', 'w').write(f())
