"""Пост 14.11 «История одной квартиры». Новый стиль: продукт в центре — телефон с историей квартиры
на обложке, сквозной график продаж в белой карточке на слайдах 2–5 (подсвечено своё), финал — телефон с поиском.
Тексты — content.md (утверждены 12.11.2026). Цифры условные, пометка «Пример»."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'templates'))
from playwright.sync_api import sync_playwright
from render import FONT_LOGO_URI, render

OUT = pathlib.Path(__file__).resolve().parent
NAVY, BLUE, BRIGHT, YEL = '#0B2545', '#1768CE', '#2D8CFF', '#FFC94D'
SALES = [('апр 2020', 33), ('сен 2022', 36), ('июн 2024', 39), ('фев 2025', 40), ('ноя 2025', 42)]

CSS = f"""
@font-face{{font-family:'Barlow Condensed';font-weight:700;src:url('{FONT_LOGO_URI}')}}
*{{box-sizing:border-box}} body{{margin:0}}
.s{{position:relative;width:1080px;height:1350px;overflow:hidden;font-family:Inter,sans-serif;color:{NAVY}}}
.light{{background:radial-gradient(90% 60% at 80% 85%,#A9CCF2 0%,rgba(169,204,242,0) 70%),linear-gradient(180deg,#DCEBFB 0%,#C3DBF5 100%)}}
.blue{{background:radial-gradient(80% 60% at 85% 10%,#4BA3FF 0%,rgba(75,163,255,0) 60%),linear-gradient(160deg,#2D8CFF 0%,#1768CE 55%,#0F55B3 100%);color:#fff}}
.logo{{position:absolute;left:80px;top:64px;font-family:'Barlow Condensed';font-size:64px;font-weight:700;line-height:1}}
.logo .h{{color:#12253E}} .logo .c{{color:#049BE1}}
.blue .logo{{background:#fff;border-radius:999px;padding:12px 24px;left:70px}}
.ex{{position:absolute;right:80px;top:76px;font-size:30px;font-weight:700;color:#2F4566;background:rgba(255,255,255,.75);border-radius:999px;padding:8px 22px}}
.box{{position:absolute;left:80px;width:920px;display:flex;flex-direction:column;gap:26px}}
.t{{margin:0;font-size:84px;line-height:1.06;font-weight:800;letter-spacing:-.025em}}
.p{{margin:0;font-size:46px;line-height:1.28;color:#1F3A5F}}
.blue .p{{color:#fff}} .phone-in{{color:{NAVY}}}
.p b{{font-weight:800;color:{NAVY}}}
.dark{{background:radial-gradient(70% 50% at 85% 75%,rgba(45,140,255,.45) 0%,rgba(45,140,255,0) 70%),linear-gradient(170deg,#0F2E57 0%,#0B2545 60%,#081B33 100%);color:#fff}}
.dark .logo{{background:#fff;border-radius:999px;padding:12px 24px;left:70px}}
.dark .p{{color:#CFE0F5}}
.paper{{background-color:#F7FAFE;background-image:linear-gradient(#E6EEF8 2px,transparent 2px),linear-gradient(90deg,#E6EEF8 2px,transparent 2px);background-size:90px 90px;background-position:-20px -20px}}
.step{{position:absolute;left:80px;bottom:70px;display:flex;gap:12px}}
.step i{{display:block;width:56px;height:10px;border-radius:5px;background:#D3E2F4}}
.step i.on{{background:{BLUE}}}
.card{{position:absolute;left:80px;width:920px;background:#fff;border-radius:40px;box-shadow:0 30px 70px rgba(11,37,69,.18),0 4px 12px rgba(11,37,69,.06)}}
"""

def logo():
    return '<span class="logo"><span class="h">Home</span><span class="c">Check.kz</span></span>'

def page(cls, inner, ex=False):
    return (f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
            f'<div class="s {cls}">{logo()}{"<span class=ex>Пример</span>" if ex else ""}{inner}</div></body></html>')

def chart(mode):
    """Sales chart 840x430. mode: all | growth | gap | last."""
    W, H, L, R, T, B = 840, 470, 60, 60, 120, 90
    lo, hi = 30, 44
    xs = [L + i * (W - L - R) / (len(SALES) - 1) for i in range(len(SALES))]
    # time-proportional x positions look odd for the 9-month gap; use years for visual spacing
    ys = [T + (hi - v) / (hi - lo) * (H - T - B) for _, v in SALES]
    pts = ' '.join(f'{x:.0f},{y:.0f}' for x, y in zip(xs, ys))
    area = f'M{xs[0]:.0f},{H-B} L' + ' L'.join(f'{x:.0f},{y:.0f}' for x, y in zip(xs, ys)) + f' L{xs[-1]:.0f},{H-B} Z'
    dim = mode in ('gap', 'last')
    s = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="overflow:visible"><defs>'
         f'<linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BRIGHT}" stop-opacity="{.10 if dim else .28}"/><stop offset="1" stop-color="{BRIGHT}" stop-opacity="0"/></linearGradient></defs>',
         f'<line x1="{L}" y1="{H-B}" x2="{W-R}" y2="{H-B}" stroke="#DCE8F7" stroke-width="3"/>',
         f'<path d="{area}" fill="url(#ar)"/>',
         f'<polyline points="{pts}" fill="none" stroke="{BLUE if not dim else "#9DBFE9"}" stroke-width="{10 if mode=="growth" else 7}" stroke-linecap="round" stroke-linejoin="round"/>']
    if mode == 'growth':
        s.append(f'<g transform="translate({xs[2]-40},{ys[2]-150})"><rect width="210" height="84" rx="22" fill="{YEL}"/>'
                 f'<text x="105" y="57" text-anchor="middle" font-family="Inter" font-weight="800" font-size="46" fill="{NAVY}">+27%</text></g>')
    if mode == 'gap':
        x1, x2, y = xs[3], xs[4], min(ys[3], ys[4]) - 70
        s.append(f'<path d="M{x1:.0f} {y+20} V{y} H{x2:.0f} V{y+20}" fill="none" stroke="{NAVY}" stroke-width="5" stroke-linecap="round"/>'
                 f'<g transform="translate({(x1+x2)/2-95:.0f},{y-82})"><rect width="190" height="66" rx="18" fill="{YEL}"/>'
                 f'<text x="95" y="45" text-anchor="middle" font-family="Inter" font-weight="800" font-size="38" fill="{NAVY}">9 мес.</text></g>')
    if mode == 'last':
        s.append(f'<line x1="{L}" y1="{ys[4]:.0f}" x2="{xs[4]:.0f}" y2="{ys[4]:.0f}" stroke="{NAVY}" stroke-width="4" stroke-dasharray="12 12" opacity=".5"/>'
                 f'<g transform="translate({xs[4]-330:.0f},{ys[4]-110:.0f})"><rect width="270" height="76" rx="20" fill="{YEL}"/>'
                 f'<text x="135" y="52" text-anchor="middle" font-family="Inter" font-weight="800" font-size="42" fill="{NAVY}">42 млн ₸</text></g>')
    for i, ((lab, v), x, y) in enumerate(zip(SALES, xs, ys)):
        hl = (mode == 'gap' and i >= 3) or (mode == 'last' and i == 4) or mode in ('all', 'growth')
        r = 16 if hl else 11
        fill = '#fff' if hl else '#E6EFFA'
        stroke = BLUE if hl else '#9DBFE9'
        s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="7"/>')
        if mode == 'all':
            s.append(f'<text x="{x:.0f}" y="{y-34:.0f}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="34" fill="{NAVY}">{v}</text>')
        anchor = 'middle'
        lx = x
        s.append(f'<text x="{lx:.0f}" y="{H-B+50}" text-anchor="{anchor}" font-family="Inter" font-size="28" fill="#2F4566" opacity="{1 if hl else .6}">{lab}</text>')
    s.append('</svg>')
    return ''.join(s)

def chart_card(mode, top=640):
    sub = 'Продажи квартиры, млн ₸' if mode == 'all' else 'Продажи квартиры, млн ₸'
    return (f'<div class="card" style="top:{top}px;padding:36px 40px 20px">'
            f'<div style="font-size:32px;font-weight:700;color:#2F4566;margin-bottom:6px">{sub}</div>{chart(mode)}</div>')

def phone(inner, left, top, rot=-5, scale=1.0, w=470):
    return (f'<div style="position:absolute;left:{left}px;top:{top}px;width:{w}px;height:960px;transform:rotate({rot}deg) scale({scale});transform-origin:center;'
            f'background:linear-gradient(160deg,#1F4E8C,#0B2545);border-radius:70px;padding:20px;box-shadow:0 50px 90px rgba(11,37,69,.35)">'
            f'<div class="phone-in" style="background:#F6FAFF;border-radius:52px;height:100%;padding:70px 34px 30px;position:relative;overflow:hidden">'
            f'<div style="position:absolute;left:50%;top:18px;width:130px;height:30px;margin-left:-65px;background:#0B2545;border-radius:15px"></div>{inner}</div></div>')

def phone_history():
    rows = ''.join(
        f'<div style="display:flex;gap:18px;align-items:flex-start;padding:14px 0">'
        f'<div style="display:flex;flex-direction:column;align-items:center;width:22px"><div style="width:22px;height:22px;border-radius:50%;background:{YEL if i==0 else BRIGHT};box-shadow:0 0 0 6px {"rgba(255,201,77,.3)" if i==0 else "rgba(45,140,255,.18)"}"></div></div>'
        f'<div style="flex:1;display:flex;justify-content:space-between;font-size:28px;white-space:nowrap"><span style="color:#2F4566">{lab}</span><b style="font-weight:800">{v} млн ₸</b></div></div>'
        for i, (lab, v) in enumerate(reversed(SALES)))
    return ('<div style="font-family:Barlow Condensed;font-size:42px;font-weight:700;margin-bottom:22px"><span style="color:#12253E">Home</span><span style="color:#049BE1">Check.kz</span></div>'
            '<div style="font-size:26px;color:#2F4566">ул. Примерная, 12, кв. 47</div>'
            '<div style="font-size:42px;font-weight:800;margin:10px 0 18px">История квартиры</div>'
            f'<div style="background:#fff;border-radius:28px;padding:10px 24px;box-shadow:0 10px 26px rgba(11,37,69,.08)">{rows}</div>'
            '')
def phone_search():
    MINI = chart('all').replace('width="840" height="470"', 'width="400" height="205"')
    return ('<div style="font-family:Barlow Condensed;font-size:42px;font-weight:700;margin-bottom:40px"><span style="color:#12253E">Home</span><span style="color:#049BE1">Check.kz</span></div>'
            '<div style="font-size:44px;font-weight:800;line-height:1.15;margin-bottom:30px">История квартиры по адресу</div>'
            f'<div style="border:4px solid {BRIGHT};border-radius:24px;padding:22px 22px;font-size:30px;color:#2F4566;background:#fff">ЖК, улица или адрес</div>'
            f'<div style="margin-top:22px;background:{BLUE};color:#fff;border-radius:24px;padding:24px;text-align:center;font-size:34px;font-weight:800">Найти</div>'
            f'<div style="margin-top:40px">{MINI}</div>')

def text(title, line, top=200):
    return f'<div class="box" style="top:{top}px"><h2 class="t">{title}</h2><p class="p">{line}</p></div>'

def steps(n):
    return '<div class="step">' + ''.join(f'<i class="{"on" if k <= n else ""}"></i>' for k in range(1, 5)) + '</div>'

COVER_CARD = (f'<div style="position:absolute;left:80px;top:820px;width:360px;background:{YEL};border-radius:32px;padding:28px 32px;'
              f'box-shadow:0 24px 50px rgba(0,0,0,.3);color:{NAVY}">'
              f'<div style="font-size:32px;font-weight:600">Продавали</div><div style="font-size:96px;font-weight:800;line-height:1;letter-spacing:-.03em">5 раз</div>'
              f'<div style="font-size:32px;font-weight:600;margin-top:6px">с 2020 года</div></div>')

SLIDES = [
    page('dark', text('Что может рассказать история квартиры', '<b style="color:#fff">Разберём на одном примере →</b>', top=200) +
         phone(phone_history(), 500, 600, rot=-7, w=500) + COVER_CARD),
    page('paper', text('История одной квартиры', '5 продаж с 2020 года. Цена — от 33 до&nbsp;42&nbsp;млн&nbsp;₸') + chart_card('all', 640) + steps(1), ex=True),
    page('paper', text('Как менялись цены в&nbsp;доме?', '+27% за 6 лет. Жильё здесь дорожает — это важно, если решите продать') + chart_card('growth', 640) + steps(2), ex=True),
    page('paper', text('Когда её купили в&nbsp;последний раз?', '9 месяцев назад. Такая быстрая продажа — повод узнать причину до&nbsp;сделки') + chart_card('gap', 640) + steps(3), ex=True),
    page('paper', text('За сколько её купили?', 'За 42 млн ₸. Если сейчас просят больше, разберитесь за что, чтобы не переплатить') + chart_card('last', 640) + steps(4), ex=True),
    page('blue', text('Узнайте историю квартиры до&nbsp;покупки', 'Введите адрес на <b style="color:#FFC94D">homecheck.kz</b>') +
         phone(phone_search(), 305, 560, rot=0)),
]

if __name__ == '__main__':
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        for k, html in enumerate(SLIDES, 1):
            render(html, OUT / f'{k:02d}.jpg', pg)
        b.close()
    print('ok')
