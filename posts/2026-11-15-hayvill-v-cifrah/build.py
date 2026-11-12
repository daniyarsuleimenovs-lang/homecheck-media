"""Пост «ЖК в цифрах»: Хайвилл, Астана. Реальные фото ЖК (команда, 13.11.2026) + метки с данными на фасаде.
Цифры пока «XX» — заполним данными команды. Тексты строк — черновик до согласования."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'templates'))
from playwright.sync_api import sync_playwright
from render import FONT_LOGO_URI, render, data_uri
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / 'src'
NAVY, BLUE, YEL = '#0B2545', '#1768CE', '#FFC94D'
img = lambda n: data_uri(Image.open(SRC / n))

CSS = f"""
@font-face{{font-family:'Barlow Condensed';font-weight:700;src:url('{FONT_LOGO_URI}')}}
*{{box-sizing:border-box}} body{{margin:0}}
.s{{position:relative;width:1080px;height:1350px;overflow:hidden;font-family:Inter,sans-serif;color:{NAVY};
   background:linear-gradient(180deg,#DCEBFB 0%,#C9DFF6 100%)}}
.bg{{position:absolute;inset:0;width:1080px;height:1350px;object-fit:cover}}
.fade{{position:absolute;left:0;top:0;width:1080px;height:640px;background:linear-gradient(180deg,rgba(220,235,251,.97) 0%,rgba(220,235,251,.9) 45%,rgba(220,235,251,0) 100%)}}
.fade2{{position:absolute;left:0;top:0;width:1080px;height:800px;background:linear-gradient(180deg,rgba(220,235,251,.96) 0px,rgba(220,235,251,.93) 540px,rgba(220,235,251,0) 800px)}}
.logo{{position:absolute;left:80px;top:64px;font-family:'Barlow Condensed';font-size:64px;font-weight:700;line-height:1;z-index:5}}
.logo .h{{color:#12253E}} .logo .c{{color:#049BE1}}
.box{{position:absolute;left:80px;top:200px;width:920px;display:flex;flex-direction:column;z-index:4}}
.t{{margin:0;font-size:84px;line-height:1.06;font-weight:800;letter-spacing:-.025em}}
.big{{margin:0;font-size:104px;line-height:1.02;font-weight:800;letter-spacing:-.03em}}
.p{{margin:22px 0 0;font-size:46px;line-height:1.28;color:#1F3A5F}}
.p b{{font-weight:800;color:{NAVY}}}
.num{{display:flex;align-items:baseline;gap:22px;margin-top:22px}}
.num .n{{font-size:180px;line-height:.9;font-weight:800;color:{BLUE};letter-spacing:-.04em}}
.num .u{{font-size:46px;line-height:1.15;font-weight:700;color:{NAVY}}}
.col{{position:absolute;left:80px;top:200px;bottom:80px;width:920px;display:flex;flex-direction:column}}
.col .box{{position:static;width:auto}}
.photo{{flex:1;min-height:0;margin-top:48px;width:920px;border-radius:40px;object-fit:cover;
        box-shadow:0 30px 70px rgba(11,37,69,.22)}}
.tag{{position:absolute;z-index:6;background:#fff;border-radius:26px;padding:18px 26px 20px;box-shadow:0 20px 50px rgba(11,37,69,.28)}}
.tag .n{{font-size:60px;line-height:1;font-weight:800;color:{BLUE};letter-spacing:-.02em}}
.tag .l{{font-size:36px;line-height:1.15;font-weight:600;color:#2F4566;margin-top:6px;white-space:nowrap}}
.pin{{position:absolute;z-index:6;width:30px;height:30px;margin:-15px 0 0 -15px;border-radius:50%;background:#fff;border:8px solid {BLUE};
      box-shadow:0 0 0 12px rgba(255,255,255,.45),0 6px 16px rgba(11,37,69,.35)}}
"""

def logo():
    return '<span class="logo"><span class="h">Home</span><span class="c">Check.kz</span></span>'

def page(inner):
    return (f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
            f'<div class="s">{logo()}{inner}</div></body></html>')

def tag(x, y, n, l, px, py):
    """Card at (x,y) with a pin on the facade at (px,py) and a connecting line."""
    return (f'<svg style="position:absolute;left:0;top:0;z-index:5" width="1080" height="1350">'
            f'<line x1="{x}" y1="{y}" x2="{px}" y2="{py}" stroke="#fff" stroke-width="5" stroke-linecap="round"/></svg>'
            f'<div class="pin" style="left:{px}px;top:{py}px"></div>'
            f'<div class="tag" style="left:{x}px;top:{y}px;transform:translate({"-100%" if x > 540 else "0"},-50%)">'
            f'<div class="n">{n}</div><div class="l">{l}</div></div>')

def bigtag(x, y, n, l, px, py):
    """Large data card centred-left at (x,y), pinned to the facade at (px,py)."""
    return (f'<svg style="position:absolute;left:0;top:0;z-index:5" width="1080" height="1350">'
            f'<line x1="{x - 40 if x > 700 else x + 40}" y1="{y}" x2="{px}" y2="{py}" stroke="#fff" stroke-width="6" stroke-linecap="round"/></svg>'
            f'<div class="pin" style="left:{px}px;top:{py}px"></div>'
            f'<div class="tag" style="left:{x}px;top:{y}px;transform:translate({"-100%" if x > 700 else "0"},-50%);padding:26px 36px 30px;border-radius:34px">'
            f'<div class="n" style="font-size:132px;letter-spacing:-.04em">{n}</div><div class="l" style="font-size:40px;margin-top:4px">{l}</div></div>')

def data_slide(bg, title, line, n, unit, x, y, px, py, fade=600):
    return page(f'<img class="bg" src="{img(bg)}"><div class="fade2"></div>'
                f'<div class="box"><h2 class="t">{title}</h2><p class="p">{line}</p></div>'
                + bigtag(x, y, n, unit, px, py))

SLIDES = [
    page(f'<img class="bg" src="{img("cover.jpg")}"><div class="fade" style="height:540px;opacity:.92"></div>'
         f'<div class="box"><h1 class="big">ЖК «Хайвилл» в&nbsp;цифрах</h1><p class="p"><b>Что показывают реальные сделки →</b></p></div>'
         + tag(80, 640, 'XX', 'сделок за год', 470, 700)
         + tag(1000, 820, 'XX тыс. ₸', 'за м² по сделкам', 560, 870)
         + tag(80, 990, '+XX%', 'цена за год', 420, 1010)),
    data_slide('b2.jpg', 'Сколько квартир продали за&nbsp;год?', 'Чем больше сделок, тем точнее понятна цена квартир в&nbsp;этом ЖК',
               'XX', 'сделок за год', 80, 930, 640, 760),
    data_slide('b3.jpg', 'Сколько стоит метр по&nbsp;сделкам?', 'Ориентир, с&nbsp;которым можно сравнить цену квартиры здесь',
               'XX тыс. ₸', 'за м² по сделкам', 80, 960, 700, 820),
    data_slide('b4.jpg', 'Как изменилась цена за&nbsp;год?', 'Так меняется стоимость жилья в&nbsp;этом ЖК',
               '+XX%', 'цена за год', 520, 960, 330, 800),
    data_slide('b5.jpg', 'Как часто здесь перепродают?', 'Частые перепродажи — повод узнать историю конкретной квартиры',
               'XX%', 'квартир<br>перепродавали', 1000, 1080, 880, 860),
    page(f'<img class="bg" src="{img("b6.jpg")}"><div class="fade" style="height:560px;opacity:.85"></div>'
         f'<div class="box"><h2 class="big">Узнайте данные своего ЖК</h2>'
         f'<p class="p"><b>Введите адрес на <span style="color:{BLUE}">homecheck.kz</span></b></p></div>'),
]

if __name__ == '__main__':
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        for k, html in enumerate(SLIDES, 1):
            render(html, HERE / f'{k:02d}.jpg', pg)
        b.close()
    print('ok')
