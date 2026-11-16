"""Изометрическая миниатюра ЖК в коде (SVG). Стилизация под Хайвилл: светлые башни с «шапками»,
красно-коричневый стилобат, деревья. Не фото и не точная копия — узнаваемый образ."""
import math
C, S = math.cos(math.radians(30)), math.sin(math.radians(30))

def P(x, y, z, ox, oy, k):
    return (ox + (x - y) * C * k, oy + (x + y) * S * k - z * k)

def poly(pts, fill, stroke='none', sw=0, op=1):
    d = ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)
    return f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}" stroke-linejoin="round"/>'

def box(x, y, z, w, d, h, top, left, right, ox, oy, k, win=None):
    """Box with origin corner (x,y,z). left face = y-facing (x varies), right face = x-facing (y varies)."""
    p = lambda a, b, c: P(a, b, c, ox, oy, k)
    out = []
    # left face: y = y+d, x from x..x+w
    out.append(poly([p(x, y + d, z), p(x + w, y + d, z), p(x + w, y + d, z + h), p(x, y + d, z + h)], left))
    # right face: x = x+w, y from y..y+d
    out.append(poly([p(x + w, y, z), p(x + w, y + d, z), p(x + w, y + d, z + h), p(x + w, y, z + h)], right))
    out.append(poly([p(x, y, z + h), p(x + w, y, z + h), p(x + w, y + d, z + h), p(x, y + d, z + h)], top))
    if win:
        wc, fl, cols_l, cols_r = win
        rows = int(h / fl)
        for r in range(rows):
            zz = z + r * fl + fl * .35
            hh = fl * .45
            for c in range(cols_l):
                a = x + (c + .25) * w / cols_l; b = a + .5 * w / cols_l
                out.append(poly([p(a, y + d, zz), p(b, y + d, zz), p(b, y + d, zz + hh), p(a, y + d, zz + hh)], wc))
            for c in range(cols_r):
                a = y + (c + .25) * d / cols_r; b = a + .5 * d / cols_r
                out.append(poly([p(x + w, a, zz), p(x + w, b, zz), p(x + w, b, zz + hh), p(x + w, a, zz + hh)], wc, op=.85))
    return ''.join(out)

def tree(x, y, z, r, ox, oy, k):
    cx, cy = P(x, y, z, ox, oy, k)
    return (f'<ellipse cx="{cx:.1f}" cy="{cy + 2:.1f}" rx="{r * k * .9:.1f}" ry="{r * k * .45:.1f}" fill="#000" opacity=".12"/>'
            f'<rect x="{cx - .25 * k:.1f}" y="{cy - 1.6 * k:.1f}" width="{.5 * k:.1f}" height="{1.6 * k:.1f}" fill="#7A5B45"/>'
            f'<circle cx="{cx:.1f}" cy="{cy - (1.6 + r) * k:.1f}" r="{r * k:.1f}" fill="#5E9C76"/>'
            f'<circle cx="{cx - r * k * .3:.1f}" cy="{cy - (1.6 + r * 1.25) * k:.1f}" r="{r * k * .55:.1f}" fill="#78B58D"/>')

def tower(x, y, z, w, d, h, ox, oy, k):
    cream_t, cream_l, cream_r = '#F4EBDD', '#E3D3BC', '#CDBA9F'
    out = box(x, y, z, w, d, h, cream_t, cream_l, cream_r, ox, oy, k, win=('#6E8FB5', 1.0, 4, 3))
    # grey-blue stair stripe on left face
    out += box(x + w * .42, y + d - .01, z, w * .16, .3, h + 1.2, '#C9D3DE', '#A9B8C9', '#93A4B8', ox, oy, k)
    # crown: setback block + roof slab
    out += box(x + .5, y + .5, z + h, w - 1, d - 1, 1.6, '#EFE4D3', '#D9C7AE', '#C3AE91', ox, oy, k)
    out += box(x - .2, y - .2, z + h + 1.6, w + .4, d + .4, .45, '#B9A688', '#A8957A', '#97856B', ox, oy, k)
    out += box(x + w * .3, y + d * .3, z + h + 2.05, w * .4, d * .4, 1.2, '#E9DDCB', '#CDB99C', '#B8A386', ox, oy, k)
    return out

def miniature(W=900, H=760, k=13.0, ox=None, oy=None):
    ox = W / 2 if ox is None else ox
    oy = H * .40 if oy is None else oy
    s = [f'<svg viewBox="170 15 560 600" width="560" height="600" xmlns="http://www.w3.org/2000/svg">']
    # board shadow + board
    bx = lambda a, b, c: P(a, b, c, ox, oy, k)
    s.append(f'<ellipse cx="{ox:.0f}" cy="{oy + 20 * k * S * 2 + 1.2 * k + 6:.0f}" rx="{19 * k * C:.0f}" ry="{28}" fill="#0B2545" opacity=".10"/>')
    s.append(box(-1, -1, -1.2, 22, 22, 1.2, '#EDE6DA', '#D8CDBB', '#C6B9A4', ox, oy, k))
    # lawn + paths
    s.append(poly([bx(0, 0, 0), bx(20, 0, 0), bx(20, 20, 0), bx(0, 20, 0)], '#CFE0C3'))
    s.append(poly([bx(9, 0, .01), bx(11, 0, .01), bx(11, 20, .01), bx(9, 20, .01)], '#E8DFD0'))
    s.append(poly([bx(0, 9, .01), bx(20, 9, .01), bx(20, 11, .01), bx(0, 11, .01)], '#E8DFD0'))
    # podium (red-brown stylobate) along back and right
    s.append(box(1, 1, 0, 18, 5, 2.2, '#C98B73', '#B47660', '#9E6450', ox, oy, k, win=('#F3D9B0', 1.1, 9, 2)))
    s.append(box(14, 6, 0, 5, 12, 2.2, '#C98B73', '#B47660', '#9E6450', ox, oy, k, win=('#F3D9B0', 1.1, 2, 6)))
    # towers (draw back to front: sort by x+y)
    T = [(2, 1.5, 2.2, 4.2, 3.6, 15), (8, 1.5, 2.2, 4.2, 3.6, 21), (14.5, 1.5, 2.2, 4, 3.6, 17), (14.8, 7.5, 2.2, 3.8, 4, 23), (14.8, 13.3, 2.2, 3.8, 4, 13)]
    for t in sorted(T, key=lambda t: t[0] + t[1]):
        s.append(tower(*t, ox, oy, k))
    # fountain + trees front
    cx, cy = P(9.5, 14, 0, ox, oy, k)
    s.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{2.2 * k:.0f}" ry="{1.1 * k:.0f}" fill="#9CC7EC" stroke="#E8DFD0" stroke-width="6"/>')
    obel = [P(9.5, 14, 0, ox, oy, k), P(9.5, 14, 6, ox, oy, k)]
    s.append(f'<polygon points="{obel[0][0] - 7:.0f},{obel[0][1]:.0f} {obel[0][0] + 7:.0f},{obel[0][1]:.0f} {obel[1][0]:.0f},{obel[1][1]:.0f}" fill="#B47660"/>')
    trees = [(3, 9, 1.3), (6, 13, 1.5), (3, 16, 1.2), (7, 18, 1.4), (12, 17, 1.3), (12, 12.5, 1.1), (5, 7.5, 1.0), (18.5, 19, 1.1), (1.5, 12, 1.1), (10, 7.2, 1.0)]
    for tx, ty, r in sorted(trees, key=lambda t: t[0] + t[1]):
        s.append(tree(tx, ty, 0, r, ox, oy, k))
    s.append('</svg>')
    return ''.join(s)

if __name__ == '__main__':
    open('/tmp/claude-0/-home-claude/316e28d6-cc64-504b-83e1-3a131c4a553a/scratchpad/mini.svg', 'w').write(miniature())
