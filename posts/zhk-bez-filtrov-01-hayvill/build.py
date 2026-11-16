"""Рубрика «Разбор ЖК», №1 — Хайвилл. Иллюстрации ЖК в коде (iso.py) по реальным фото команды.
Строгая типографика: заголовок 76, цифра 140, текст 40. Цифры — XX, выводы в [скобках] — черновик под данные."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'templates'))
from playwright.sync_api import sync_playwright
from render import FONT_LOGO_URI, render
import iso

HERE = pathlib.Path(__file__).resolve().parent
NAVY, BLUE, YEL = '#0B2545', '#1768CE', '#FFC94D'
NAME, NUM = 'Хайвилл', 1
ILL = {n: f() for n, f in [('complex', iso.complex_), ('gate', iso.gate), ('courtyard', iso.courtyard), ('skyline', iso.skyline)]}

CSS = f"""
@font-face{{font-family:'Barlow Condensed';font-weight:700;src:url('{FONT_LOGO_URI}')}}
*{{box-sizing:border-box}} body{{margin:0}}
.s{{position:relative;width:1080px;height:1350px;overflow:hidden;font-family:Inter,sans-serif;color:{NAVY};background:#FFFFFF}}
.logo{{position:absolute;left:80px;top:60px;font-family:'Barlow Condensed';font-size:58px;font-weight:700;line-height:1}}
.logo .h{{color:#12253E}} .logo .c{{color:#049BE1}}
.stage{{position:absolute;left:80px;width:920px;border-radius:44px;overflow:hidden;
        background:radial-gradient(70% 60% at 50% 100%,#FFF3CF 0%,rgba(255,243,207,0) 70%),linear-gradient(180deg,#CFE4FB 0%,#EEF6FF 100%);
        display:flex;align-items:center;justify-content:center}}
.stage svg{{width:auto;height:auto}}
.col{{position:absolute;left:80px;width:920px}}
.t{{margin:0;font-size:76px;line-height:1.08;font-weight:800;letter-spacing:-.025em}}
.n{{font-size:140px;line-height:.95;font-weight:800;letter-spacing:-.04em}}
.n i{{font-style:normal;background:linear-gradient(transparent 60%,{YEL} 60%,{YEL} 90%,transparent 90%);padding:0 4px}}
.p,.u{{font-size:40px;line-height:1.3;font-weight:500;color:#24384F;margin:0}}
.u{{font-weight:700;color:{NAVY};letter-spacing:0}}
.r{{font-size:40px;font-weight:700;color:{BLUE};margin:0 0 14px}}
.ph{{color:#A9740A}}
"""

def page(inner):
    return (f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="s">'
            f'<span class="logo"><span class="h">Home</span><span class="c">Check.kz</span></span>{inner}</div></body></html>')

def stage(name, top, h, maxh):
    return f'<div class="stage" style="top:{top}px;height:{h}px">{ILL[name].replace("<svg ", f"<svg preserveAspectRatio='xMidYMid meet' style='height:{maxh}px;width:860px' ", 1)}</div>'

def fact(ill, title, num, unit, line):
    return page(stage(ill, 150, 540, 500)
                + f'<div class="col" style="top:730px"><p class="r">Разбор ЖК · №{NUM}</p><h2 class="t">{title}</h2>'
                f'<div style="display:flex;align-items:baseline;gap:20px;margin-top:22px"><span class="n"><i>{num}</i></span><span class="u">{unit}</span></div>'
                f'<p class="p" style="margin-top:18px">{line}</p></div>')

S1 = page(stage('complex', 150, 720, 680)
          + f'<div class="col" style="top:910px"><p class="r">Разбор ЖК · №{NUM}</p>'
            f'<h1 class="n" style="margin:0">{NAME}</h1><p class="p" style="margin-top:22px">Что о нём говорят реальные сделки →</p></div>')

S2 = fact('gate', 'Сколько стоит метр на&nbsp;самом деле', 'XX', 'тыс. ₸ за м²',
          'Средняя цена по&nbsp;зарегистрированным сделкам в&nbsp;ЖК')
S3 = fact('skyline', 'Как держит цену', '+XX%', 'за год',
          f'В среднем по Астане — +XX%. <span class="ph">[Дорожает быстрее города]</span>')
S4 = fact('complex', 'Что здесь покупают чаще всего', 'XX–XX', 'м²',
          f'В среднем за XX млн ₸. <span class="ph">[Самый ходовой формат в&nbsp;ЖК]</span>')
S5 = fact('courtyard', 'Как долго здесь живут', 'X', 'лет',
          f'Столько в среднем владеют квартирой до&nbsp;продажи. <span class="ph">[Здесь живут подолгу]</span>')

rows = ''.join(
    f'<div style="display:flex;align-items:center;gap:28px;padding:34px 0;border-top:3px solid #E6EEF8">'
    f'<span style="flex:none;width:72px;height:72px;border-radius:50%;background:{YEL};display:flex;align-items:center;justify-content:center;font-size:40px;font-weight:700">{i}</span>'
    f'<span class="ph" style="font-size:40px;font-weight:700">{t}</span></div>'
    for i, t in enumerate(['[Дорожает быстрее города]', '[Живут подолгу]', '[Чаще всего берут 60–80 м²]'], 1))
S6 = page(stage('skyline', 150, 420, 380)
          + f'<div class="col" style="top:610px"><p class="r">Разбор ЖК · №{NUM}</p><h2 class="t">Коротко о&nbsp;Хайвилле</h2>'
            f'<div style="margin-top:30px">{rows}</div></div>')

S7 = page(stage('complex', 150, 720, 680)
          + f'<div class="col" style="top:910px"><h2 class="t">А что сделки говорят о&nbsp;вашем ЖК?</h2>'
            f'<p class="p" style="margin-top:22px">Введите название или адрес на&nbsp;<b style="color:{BLUE}">homecheck.kz</b></p></div>')

SLIDES = [S1, S2, S3, S4, S5, S6, S7]

if __name__ == '__main__':
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        for k, html in enumerate(SLIDES, 1):
            render(html, HERE / f'{k:02d}.jpg', pg)
        b.close()
    print('ok')
