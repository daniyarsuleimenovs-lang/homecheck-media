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
ILL = {n: f() for n, f in iso.SCENES.items()}
SKY = {'cover': 'linear-gradient(180deg,#FFB98C 0%,#FFE3C4 60%,#FFF3E2 100%)', 'gate': 'linear-gradient(180deg,#BFDCFA 0%,#EAF4FF 100%)',
       'skyline': 'radial-gradient(60% 50% at 70% 15%,#2C4C82 0%,rgba(44,76,130,0) 70%),linear-gradient(180deg,#0A1A36 0%,#1E3866 100%)',
       'apartment': 'linear-gradient(180deg,#FFE9A8 0%,#FFF6DA 100%)', 'courtyard': 'linear-gradient(180deg,#BFE6C9 0%,#EEF9F1 100%)',
       'winter': 'linear-gradient(180deg,#CFDCEC 0%,#F4F8FD 100%)'}

CSS = f"""
@font-face{{font-family:'Barlow Condensed';font-weight:700;src:url('{FONT_LOGO_URI}')}}
*{{box-sizing:border-box}} body{{margin:0}}
.s{{position:relative;width:1080px;height:1350px;overflow:hidden;font-family:Inter,sans-serif;color:#fff;
   background:radial-gradient(70% 45% at 85% 100%,rgba(45,140,255,.30) 0%,rgba(45,140,255,0) 70%),linear-gradient(170deg,#0F2E57 0%,#0B2545 55%,#081B33 100%)}}
.logo{{position:absolute;left:80px;top:60px;font-family:'Barlow Condensed';font-size:58px;font-weight:700;line-height:1}}
.logo .h{{color:#fff}} .logo .c{{color:#049BE1}}
.stage{{position:absolute;left:80px;width:920px;border-radius:44px;overflow:hidden;
        display:flex;align-items:center;justify-content:center;box-shadow:0 30px 70px rgba(0,0,0,.35)}}
.stage svg{{width:auto;height:auto}}
.col{{position:absolute;left:80px;width:920px}}
.t{{margin:0;font-size:76px;line-height:1.08;font-weight:800;letter-spacing:-.025em}}
.n{{font-size:140px;line-height:.95;font-weight:800;letter-spacing:-.04em}}
.n i{{font-style:normal;color:{YEL}}}
.p,.u{{font-size:40px;line-height:1.3;font-weight:500;color:#C9D8EC;margin:0}}
.u{{font-weight:700;color:#fff;letter-spacing:0}}
.r{{font-size:40px;font-weight:700;color:{BLUE};margin:0 0 14px}}
.ph{{color:#FFC94D;opacity:.75}}
"""

def page(inner):
    return (f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="s">'
            f'<span class="logo"><span class="h">Home</span><span class="c">Check.kz</span></span>{inner}</div></body></html>')

def stage(name, top, h, maxh):
    return f'<div class="stage" style="top:{top}px;height:{h}px;background:{SKY[name]}">{ILL[name].replace("<svg ", f"<svg preserveAspectRatio='xMidYMid meet' style='height:{maxh}px;width:860px' ", 1)}</div>'

def fact(ill, title, num, unit, line):
    return page(stage(ill, 150, 540, 500)
                + f'<div class="col" style="top:740px"><h2 class="t">{title}</h2>'
                f'<div style="display:flex;align-items:baseline;gap:20px;margin-top:22px"><span class="n"><i>{num}</i></span><span class="u">{unit}</span></div>'
                f'<p class="p" style="margin-top:18px">{line}</p></div>')

S1 = page(stage('cover', 150, 760, 700)
          + f'<div class="col" style="top:960px">'
            f'<h1 class="n" style="margin:0">{NAME}</h1><p class="p" style="margin-top:22px">Что о нём говорят реальные сделки →</p></div>')

S2 = fact('gate', 'Сколько стоит метр на&nbsp;самом деле', 'XX', 'тыс. ₸ за м²',
          'Средняя цена по&nbsp;зарегистрированным сделкам в&nbsp;ЖК')
S3 = fact('skyline', 'Как держит цену', '+XX%', 'за год',
          f'В среднем по Астане — +XX%. <span class="ph">[Дорожает быстрее города]</span>')
S4 = fact('apartment', 'Что здесь покупают чаще всего', 'XX–XX', 'м²',
          f'В среднем за XX млн ₸. <span class="ph">[Самый ходовой формат в&nbsp;ЖК]</span>')
S5 = fact('courtyard', 'Как долго здесь живут', 'X', 'лет',
          f'Столько в среднем владеют квартирой до&nbsp;продажи. <span class="ph">[Здесь живут подолгу]</span>')

rows = ''.join(
    f'<div style="display:flex;align-items:center;gap:28px;padding:34px 0;border-top:2px solid rgba(255,255,255,.15)">'
    f'<span style="flex:none;width:72px;height:72px;border-radius:50%;background:{YEL};display:flex;align-items:center;justify-content:center;font-size:40px;font-weight:700;color:#0B2545">{i}</span>'
    f'<span class="ph" style="font-size:40px;font-weight:700">{t}</span></div>'
    for i, t in enumerate(['[Дорожает быстрее города]', '[Живут подолгу]', '[Чаще всего берут 60–80 м²]'], 1))
S6 = page(stage('winter', 150, 420, 390)
          + f'<div class="col" style="top:620px"><h2 class="t">Коротко о&nbsp;Хайвилле</h2>'
            f'<div style="margin-top:30px">{rows}</div></div>')

S7 = page(stage('cover', 150, 760, 700)
          + f'<div class="col" style="top:950px"><h2 class="t">А что сделки говорят о&nbsp;вашем ЖК?</h2>'
            f'<p class="p" style="margin-top:22px">Введите название или адрес на&nbsp;<b style="color:{YEL}">homecheck.kz</b></p></div>')

SLIDES = [S1, S2, S3, S4, S5, S6, S7]

if __name__ == '__main__':
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        for k, html in enumerate(SLIDES, 1):
            render(html, HERE / f'{k:02d}.jpg', pg)
        b.close()
    print('ok')
