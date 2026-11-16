"""Рубрика «ЖК без фильтров», №1 — Хайвилл. Свой вид рубрики: тёплый светлый фон, миниатюра ЖК (iso.py),
карточки-«досье». Цифры — XX (ждём данные команды), выводы в [скобках] — черновик под цифры."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'templates'))
from playwright.sync_api import sync_playwright
from render import FONT_LOGO_URI, render
from iso import miniature

HERE = pathlib.Path(__file__).resolve().parent
NAVY, BLUE, YEL, LAB, BG = '#0B2545', '#1768CE', '#FFC94D', '#5B6B80', '#F6F1E8'
NAME, NUM = 'Хайвилл', 1
N = 7

CSS = f"""
@font-face{{font-family:'Barlow Condensed';font-weight:700;src:url('{FONT_LOGO_URI}')}}
*{{box-sizing:border-box}} body{{margin:0}}
.s{{position:relative;width:1080px;height:1350px;overflow:hidden;font-family:Inter,sans-serif;color:{NAVY};
   background:radial-gradient(80% 55% at 50% 78%,#FFFFFF 0%,rgba(255,255,255,0) 70%),{BG}}}
.logo{{position:absolute;left:80px;top:64px;font-family:'Barlow Condensed';font-size:58px;font-weight:700;line-height:1}}
.logo .h{{color:#12253E}} .logo .c{{color:#049BE1}}
.badge{{position:absolute;right:80px;top:66px;background:{NAVY};color:#fff;border-radius:999px;padding:12px 26px;font-size:28px;font-weight:700;letter-spacing:.02em}}
.badge b{{color:{YEL};font-weight:800}}
.lab{{font-size:30px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:{LAB}}}
.t{{margin:14px 0 0;font-size:80px;line-height:1.06;font-weight:800;letter-spacing:-.025em}}
.card{{background:#fff;border:3px solid #E9DFCF;border-radius:36px;box-shadow:0 24px 60px rgba(70,50,20,.08)}}
.big{{font-size:150px;line-height:.95;font-weight:800;letter-spacing:-.045em}}
.mark{{background:linear-gradient(transparent 62%,{YEL} 62%,{YEL} 92%,transparent 92%);padding:0 6px}}
.p{{font-size:44px;line-height:1.28;color:#24384F;margin:0}}
.foot{{position:absolute;left:80px;right:80px;bottom:64px;display:flex;justify-content:space-between;font-size:28px;font-weight:600;color:{LAB}}}
.ph{{color:#B07A00}}
"""

def page(inner, k, foot=True, count=True):
    f = (f'<div class="foot"><span>ЖК {NAME} · Астана</span><span>{k}/{N if count else ""}</span></div>'.replace(f'{k}/</span>', '</span>') if foot else '')
    return (f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="s">'
            f'<span class="logo"><span class="h">Home</span><span class="c">Check.kz</span></span>'
            f'<span class="badge">ЖК без фильтров · <b>№{NUM}</b></span>{inner}{f}</div></body></html>')

def mini(x, y, w):
    svg = miniature()
    return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px">{svg.replace("<svg ", f"<svg style=width:{w}px;height:auto ", 1)}</div>'

def head(label, title, top=210):
    return f'<div style="position:absolute;left:80px;top:{top}px;width:920px"><div class="lab">{label}</div><h2 class="t">{title}</h2></div>'

def fact(k, label, title, body, line):
    return page(f'<div style="position:absolute;left:80px;top:210px;width:920px;display:flex;flex-direction:column">'
                f'<div class="lab">{label}</div><h2 class="t">{title}</h2>'
                f'<div class="card" style="margin-top:56px;padding:56px 60px 60px">{body}</div>'
                f'<p class="p" style="margin-top:48px;width:600px">{line}</p></div>' + mini(700, 960, 300), k, count=False)

def bars(a, b):
    def col(name, v, h, c):
        return (f'<div style="width:330px;display:flex;flex-direction:column;align-items:center">'
                f'<div style="font-size:64px;font-weight:800;margin-bottom:14px">{v}</div>'
                f'<div style="width:100%;height:{h}px;border-radius:24px 24px 8px 8px;background:{c}"></div>'
                f'<div style="margin-top:20px;font-size:34px;font-weight:700">{name}</div></div>')
    return (f'<div style="display:flex;justify-content:space-around;align-items:flex-end;height:330px">'
            f'{col(NAME, a, 210, BLUE)}{col("Астана", b, 140, "#D9CDB8")}</div>')

S1 = page(
    f'<div style="position:absolute;left:80px;top:190px;width:920px"><div class="lab">Что о нём говорят реальные сделки</div>'
    f'<h1 style="margin:8px 0 0;font-size:150px;line-height:1;font-weight:800;letter-spacing:-.045em">{NAME}</h1></div>'
    + mini(130, 400, 820)
    + f'<div style="position:absolute;left:80px;bottom:130px;font-size:40px;font-weight:700">Листайте →</div>', 1)

S2 = fact(2, 'Факт 1 · цена', 'Сколько стоит метр на&nbsp;самом деле',
          f'<div class="big"><span class="mark">XX</span> <span style="font-size:80px">тыс. ₸</span></div>'
          f'<div style="font-size:40px;font-weight:700;margin-top:26px">средняя цена м² по&nbsp;сделкам</div>',
          'Это то, сколько платят за метр в&nbsp;этом ЖК по&nbsp;зарегистрированным сделкам.')

S3 = fact(3, 'Факт 2 · динамика', 'Как держит цену',
          bars('+XX%', '+XX%') + f'<div style="font-size:30px;color:{LAB};margin-top:26px;text-align:center">изменение цены м² за год</div>',
          f'<span class="ph">[Дорожает быстрее, чем в среднем по&nbsp;Астане]</span>')

S4 = fact(4, 'Факт 3 · спрос', 'Что здесь покупают чаще всего',
          f'<div class="big"><span class="mark">XX–XX</span> <span style="font-size:80px">м²</span></div>'
          f'<div style="font-size:40px;font-weight:700;margin-top:26px">в среднем за&nbsp;XX млн ₸</div>',
          f'<span class="ph">[Самый ходовой формат в&nbsp;ЖК — такие квартиры продают чаще всего]</span>')

S5 = fact(5, 'Факт 4 · жильцы', 'Как долго здесь живут',
          f'<div class="big"><span class="mark">X</span> <span style="font-size:80px">лет</span></div>'
          f'<div style="font-size:40px;font-weight:700;margin-top:26px">в среднем владеют квартирой до&nbsp;продажи</div>',
          f'<span class="ph">[Здесь живут подолгу — квартиры редко меняют хозяев]</span>')

chips = ''.join(
    f'<div class="card" style="display:flex;align-items:center;gap:30px;padding:36px 44px;margin-top:28px">'
    f'<span style="flex:none;width:76px;height:76px;border-radius:50%;background:{YEL};display:flex;align-items:center;justify-content:center;font-size:40px;font-weight:800">{i}</span>'
    f'<span class="ph" style="font-size:48px;font-weight:800">{t}</span></div>'
    for i, t in enumerate(['[Дорожает быстрее города]', '[Живут подолгу]', '[Чаще берут 60–80 м²]'], 1))
S6 = page(head('Итог', f'{NAME} в&nbsp;трёх словах') + f'<div style="position:absolute;left:80px;top:470px;width:920px">{chips}</div>', 6)

S7 = page(head('Ваш ЖК', 'Узнайте характер своего ЖК')
          + '<p class="p" style="position:absolute;left:80px;top:450px;width:920px"><b>Введите название или адрес на&nbsp;<span style="color:#1768CE">homecheck.kz</span></b></p>'
          + mini(250, 560, 580), 7)

SLIDES = [S1, S2, S3, S4, S5, S6, S7]

if __name__ == '__main__':
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        for k, html in enumerate(SLIDES, 1):
            render(html, HERE / f'{k:02d}.jpg', pg)
        b.close()
    print('ok')
