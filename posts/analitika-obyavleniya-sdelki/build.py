"""Пост «Насколько цена в объявлении отражает стоимость квартиры?» — по файлу
HomeCheck_Post_and_Internal_Method_2026-11-08.pdf (стр. 1, данные проверены командой).
Стиль разнообразнее основного шаблона: цветные фоны из фирменной палитры, инфографика вместо иллюстраций.
Общие правила те же: Inter, логотип, не больше 3 стилей текста, 1080x1350, безопасные поля 80 px."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'templates'))
from playwright.sync_api import sync_playwright
from render import FONT_LOGO_URI, render

OUT = pathlib.Path(__file__).resolve().parent
NAVY, BLUE, BRIGHT, LIGHT, PALE, YEL = '#0B2545', '#1768CE', '#2D8CFF', '#BBD6F2', '#DCEBFB', '#FFC94D'

CSS = f"""
@font-face{{font-family:'Barlow Condensed';font-weight:700;src:url('{FONT_LOGO_URI}')}}
body{{margin:0}}
.s{{position:relative;width:1080px;height:1350px;overflow:hidden;font-family:Inter,sans-serif}}
.blue{{background:radial-gradient(120% 90% at 85% 10%,#2D8CFF 0%,#1768CE 55%,#0F55B3 100%);color:#fff}}
.light{{background:linear-gradient(180deg,#DCEBFB 0%,#BBD6F2 100%);color:{NAVY}}}
.logo{{position:absolute;left:80px;top:64px;font-family:'Barlow Condensed';font-size:64px;font-weight:700;line-height:1;padding:14px 26px;border-radius:999px;background:#fff}}
.logo .h{{color:#12253E}} .logo .c{{color:#049BE1}}
.light .logo{{background:rgba(255,255,255,.7)}}
.tag{{position:absolute;right:80px;top:88px;font-size:26px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;opacity:.85}}
.box{{position:absolute;left:80px;width:920px;display:flex;flex-direction:column;gap:40px}}
.t{{margin:0;font-size:92px;line-height:1.06;font-weight:800;letter-spacing:-.025em}}
.p{{margin:0;font-size:52px;line-height:1.3}}
.p b{{font-weight:800}}
.lb{{margin:0;font-size:38px;line-height:1.3;opacity:.8}}
.y{{color:{YEL}}} .bl{{color:{BLUE}}}
.card{{background:#fff;border-radius:36px;box-shadow:0 24px 60px rgba(11,37,69,.18);color:{NAVY}}}
"""

def logo():
    return '<span class="logo"><span class="h">Home</span><span class="c">Check.kz</span></span>'

def page(cls, inner, tag=''):
    return (f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body><div class="s {cls}">{logo()}' + (f'<span class="tag">{tag}</span>' if tag else '') + f'{inner}</div></body></html>')

def listing_cards():
    cards = []
    for i, (dx, dy, rot) in enumerate([(0, 40, -6), (210, 0, 3), (420, 50, -2)]):
        cards.append(f'''<div class="card" style="position:absolute;left:{dx}px;top:{dy}px;width:400px;padding:22px;transform:rotate({rot}deg)">
          <div style="height:140px;border-radius:22px;background:linear-gradient(180deg,#DCEBFB,#8EC2FA)"></div>
          <div style="height:26px;width:70%;background:#DCEBFB;border-radius:13px;margin:22px 0 14px"></div>
          <div style="font-size:46px;font-weight:800;color:{BLUE}">₸ ₸ ₸</div></div>''')
    return f'<div style="position:absolute;left:100px;bottom:40px;width:880px;height:330px">{"".join(cards)}</div>'

def stacks():
    def col(x, label, color):
        sheets = ''.join(f'<div style="position:absolute;left:{x + k*10}px;bottom:{k*14}px;width:300px;height:200px;border-radius:24px;background:{color};box-shadow:0 10px 24px rgba(11,37,69,.15)"></div>' for k in range(6))
        return sheets + f'<div style="position:absolute;left:{x}px;bottom:-80px;width:340px;text-align:center;font-size:40px;font-weight:800">{label}</div>'
    return (f'<div style="position:absolute;left:80px;bottom:200px;width:920px;height:300px">'
            f'{col(40, "≈500 объявлений", "#fff")}{col(520, "≈500 сделок", YEL)}'
            f'<div style="position:absolute;left:420px;top:60px;font-size:90px;font-weight:800;color:{BLUE}">=</div></div>')

def houses_bar():
    hs = []
    for k in range(10):
        c = YEL if k in (2, 6) else '#FFFFFF'
        op = 1 if k in (2, 6) else .55
        hs.append(f'<svg viewBox="0 0 64 64" width="84" height="84" style="opacity:{op}"><path d="M8 30 L32 10 L56 30 L56 56 L8 56 Z" fill="{c}"/><rect x="26" y="38" width="12" height="18" rx="2" fill="#1768CE"/></svg>')
    return f'<div style="position:absolute;left:80px;bottom:150px;width:920px;display:flex;justify-content:space-between">{"".join(hs)}</div>'

def compare(name, a, s, pct):
    hmax = 520
    ha, hs = hmax, round(hmax * s / a)
    bar = lambda h, color, lab, val, txt: (f'<div style="display:flex;flex-direction:column;align-items:center;justify-content:flex-end;width:330px">'
        f'<div style="font-size:56px;font-weight:800;margin-bottom:16px">{val}</div>'
        f'<div style="width:300px;height:{h}px;border-radius:28px 28px 0 0;background:{color}"></div>'
        f'<div style="font-size:40px;margin-top:18px;color:{txt}">{lab}</div></div>')
    return (f'<div class="box" style="top:220px;gap:20px"><h2 class="t">ЖК «{name}»</h2>'
            f'<p class="lb">Средняя цена за м², тыс. ₸</p></div>'
            f'<div style="position:absolute;left:100px;bottom:90px;display:flex;gap:40px;align-items:flex-end">'
            f'{bar(ha, "#FFFFFF", "Объявления", a, NAVY)}{bar(hs, BLUE, "Сделки", s, NAVY)}</div>'
            f'<div style="position:absolute;right:80px;bottom:{90 + 60 + hs + 120}px;background:{YEL};color:{NAVY};font-size:80px;font-weight:800;border-radius:28px;padding:18px 34px;box-shadow:0 16px 36px rgba(11,37,69,.2)">−{pct}%</div>')

def money():
    coins = ''.join(f'<div style="position:absolute;left:{x}px;bottom:{k*34}px;width:220px;height:60px;border-radius:50%;background:{YEL};box-shadow:inset 0 -10px 0 #E8A92E"></div>'
                    for x, n in [(120, 7), (420, 10), (720, 5)] for k in range(n))
    return f'<div style="position:absolute;left:40px;bottom:130px;width:1000px;height:420px">{coins}</div>'

def search():
    return (f'<div class="card" style="position:absolute;left:80px;bottom:200px;width:920px;padding:40px">'
            f'<div style="font-family:Barlow Condensed;font-size:64px;font-weight:700;margin-bottom:26px"><span style="color:#12253E">Home</span><span style="color:#049BE1">Check.kz</span></div>'
            f'<div style="border:4px solid {BRIGHT};border-radius:24px;padding:26px 30px;font-size:46px;color:#2F4566;display:flex;justify-content:space-between">'
            f'<span>Адрес или название ЖК</span><span style="color:{BLUE};font-weight:800">→</span></div></div>')

SLIDES = [
    page('blue', '<div class="box" style="top:300px"><h1 class="t">Насколько цена в&nbsp;объявлении отражает стоимость квартиры?</h1>'
         '<span class="p y" style="font-weight:800">Листайте →</span></div>' + houses_bar(), tag='Аналитика для покупателя'),
    page('light', '<div class="box" style="top:220px"><h2 class="t">Когда мы ищем квартиру, ориентируемся на цены объявлений</h2>'
         '<p class="p">Но этот ориентир складывается из сумм, которые <b>продавцы хотят получить</b>.</p></div>' + listing_cards()),
    page('light', '<div class="box" style="top:220px"><h2 class="t">А что показывают сделки?</h2>'
         '<p class="p">Мы сравнили цену за м² сопоставимых по площади квартир <b>в одном доме</b>.</p>'
         '<p class="lb">Астана, январь–февраль 2026. Обезличенные данные о сделках.</p></div>' + stacks()),
    page('blue', '<div class="box" style="top:250px;gap:24px"><p class="lb" style="opacity:.9">Средняя разница по домам</p>'
         '<p style="margin:0;font-size:260px;line-height:1;font-weight:800;letter-spacing:-.03em" class="y">≈16%</p>'
         '<p class="p">В отдельных домах наблюдался разрыв <b>около 30%</b>.</p></div>' + houses_bar()),
    page('light', compare('Жайна', 508, 426, 16)),
    page('light', compare('Аспан', 529, 466, 12)),
    page('blue', '<div class="box" style="top:250px"><h2 class="t">В пересчёте на квартиру — несколько миллионов&nbsp;₸</h2>'
         '<p class="lb" style="opacity:.9">На разницу могут влиять переговоры, комплектация и условия расчётов.</p></div>' + money()),
    page('light', '<div class="box" style="top:220px"><h2 class="t">Уже выбрали квартиру? Проверьте её в&nbsp;HomeCheck.kz</h2>'
         '</div>' + search()),
]

if __name__ == '__main__':
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        for k, html in enumerate(SLIDES, 1):
            render(html, OUT / f'{k:02d}.jpg', pg)
        b.close()
    print('ok')
