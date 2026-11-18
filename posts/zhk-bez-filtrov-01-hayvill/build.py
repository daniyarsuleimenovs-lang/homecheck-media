"""Разбор ЖК №1 — Хайвилл. Вариант В (16.11.2026): обложка и финал — иллюстрация на весь слайд, текст в небе;
слайды с цифрами — иллюстрация сверху перетекает в кремовый низ с текстом. Цвета из иллюстраций.
Иллюстрации — ChatGPT по реальным фото (команда). Строгая типографика: 76 / 140 / 40.
Цифры — XX, выводы в [скобках] — черновик под данные."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'templates'))
from playwright.sync_api import sync_playwright
from render import FONT_LOGO_URI, render, data_uri
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
NAVY, BLUE, TERRA, CREAM, SKY = '#0B2545', '#1768CE', '#B8613F', '#FBF2E6', '#DCEAF6'
NAME = 'Хайвил'
IMG = {n: data_uri(Image.open(HERE / 'src' / f'{n}.jpg')) for n in ['interior', 'towers', 'aerial', 'courtyard']}

CSS = f"""
@font-face{{font-family:'Barlow Condensed';font-weight:700;src:url('{FONT_LOGO_URI}')}}
*{{box-sizing:border-box}} body{{margin:0}}
.s{{position:relative;width:1080px;height:1350px;overflow:hidden;font-family:Inter,sans-serif;color:{NAVY};background:{CREAM}}}
.logo{{position:absolute;left:80px;top:60px;font-family:'Barlow Condensed';font-size:58px;font-weight:700;line-height:1;z-index:5}}
.logo .h{{color:#12253E}} .logo .c{{color:#049BE1}}
.img{{position:absolute;left:0;top:0;width:1080px;object-fit:cover}}
.col{{position:absolute;left:80px;width:920px;z-index:4}}
.t{{margin:0;font-size:76px;line-height:1.08;font-weight:800;letter-spacing:-.025em}}
.n{{font-size:140px;line-height:.95;font-weight:800;letter-spacing:-.04em;color:{BLUE}}}
.p,.u{{font-size:46px;line-height:1.28;font-weight:500;color:#33465E;margin:0}}
.u{{font-weight:700;color:{NAVY}}}
.ph{{color:{TERRA}}}
.tag{{position:absolute;z-index:6;background:#fff;border-radius:28px;padding:22px 30px 24px;box-shadow:0 20px 50px rgba(11,37,69,.25)}}
.pin{{position:absolute;z-index:6;width:30px;height:30px;margin:-15px 0 0 -15px;border-radius:50%;background:#fff;border:8px solid {BLUE};
      box-shadow:0 0 0 12px rgba(255,255,255,.45),0 6px 16px rgba(11,37,69,.35)}}
"""


def page(inner):
    return (f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="s">'
            f'<span class="logo"><span class="h">Home</span><span class="c">Check.kz</span></span>{inner}</div></body></html>')


def full(img, pos, fade_h):
    """Иллюстрация на весь слайд + мягкое осветление неба под текстом."""
    return (f'<img class="img" src="{IMG[img]}" style="height:1350px;object-position:{pos}">'
            f'<div style="position:absolute;left:0;top:0;width:1080px;height:{fade_h}px;z-index:2;'
            f'background:linear-gradient(180deg,rgba(220,234,246,.92) 0%,rgba(220,234,246,.75) 55%,rgba(220,234,246,0) 100%)"></div>')


def top(img, pos, h):
    """Иллюстрация сверху, плавно перетекает в кремовый низ."""
    return (f'<img class="img" src="{IMG[img]}" style="height:{h}px;object-position:{pos}">'
            f'<div style="position:absolute;left:0;top:0;width:1080px;height:200px;z-index:2;'
            f'background:linear-gradient(180deg,rgba(251,242,230,.9) 0%,rgba(251,242,230,.55) 45%,rgba(251,242,230,0) 100%)"></div>'
            f'<div style="position:absolute;left:0;top:{h - 260}px;width:1080px;height:260px;z-index:2;'
            f'background:linear-gradient(180deg,rgba(251,242,230,0) 0%,rgba(251,242,230,.85) 65%,{CREAM} 100%)"></div>')


def tag(x, y, n, l, px, py):
    return (f'<svg style="position:absolute;left:0;top:0;z-index:5" width="1080" height="1350">'
            f'<line x1="{x + 40}" y1="{y}" x2="{px}" y2="{py}" stroke="#fff" stroke-width="5" stroke-linecap="round"/></svg>'
            f'<div class="pin" style="left:{px}px;top:{py}px"></div>'
            f'<div class="tag" style="left:{x}px;top:{y}px;transform:translateY(-50%)">'
            f'<div style="font-size:64px;font-weight:800;color:{BLUE};line-height:1">{n}</div>'
            f'<div style="font-size:36px;font-weight:600;color:#33465E;margin-top:8px">{l}</div></div>')


def fact(img, pos, title, num, unit, line):
    return page(top(img, pos, 800)
                + f'<div class="col" style="top:700px"><h2 class="t">{title}</h2>'
                f'<div style="display:flex;align-items:baseline;gap:20px;margin-top:24px"><span class="n">{num}</span><span class="u">{unit}</span></div>'
                f'<p class="p" style="margin-top:20px">{line}</p></div>')


S1 = page(full('aerial', '50% 0%', 520)
          + f'<div class="col" style="top:170px"><h1 class="t" style="font-size:150px;line-height:1;letter-spacing:-.04em">{NAME}</h1>'
            f'<p class="p" style="margin-top:20px;color:{NAVY};font-weight:700;font-size:54px;line-height:1.2">Что о&nbsp;нём говорят реальные сделки →</p></div>'
          + tag(560, 1020, '≈650 тыс. ₸', 'за м² по сделкам', 470, 880))

S2 = fact('towers', '50% 12%', 'Сколько стоит метр на&nbsp;самом деле', '≈650', 'тыс. ₸ за м²',
          'Столько обычно платят за&nbsp;метр в&nbsp;реальных сделках. Ориентир, чтобы понять, не&nbsp;завышена ли цена квартиры')
S3 = fact('aerial', '50% 55%', 'Как меняются цены', '+9%', 'за год',
          'Цены в&nbsp;ЖК растут. Это общий тренд по&nbsp;ЖК, а&nbsp;не&nbsp;рост каждой отдельной квартиры')
S4 = fact('interior', '50% 60%', 'Что здесь покупают чаще всего', '60–80', 'м²',
          'Каждая пятая продажа. Обычно такая квартира стоит около 40,5&nbsp;млн&nbsp;₸')
S5 = fact('courtyard', '50% 88%', 'Сколько владеют до&nbsp;перепродажи', '≈5', 'лет',
          'Обычно квартиру перепродают примерно через 5&nbsp;лет. Если продают раньше — стоит спросить почему')

rows = ''.join(
    f'<div style="display:flex;align-items:center;gap:28px;padding:20px 0;border-top:2px solid #EADCC8">'
    f'<span style="flex:none;width:68px;height:68px;border-radius:50%;background:{TERRA};color:#fff;display:flex;align-items:center;justify-content:center;font-size:40px;font-weight:700">{i}</span>'
    f'<span style="font-size:42px;line-height:1.25;font-weight:600;color:{NAVY};text-wrap:balance">{t}</span></div>'
    for i, t in enumerate(['Дороже 650&nbsp;тыс.&nbsp;₸ за&nbsp;м²? Узнайте за&nbsp;что',
                           '60–80&nbsp;м² — проще всего сравнить цену',
                           'Цены растут — проверяйте конкретную квартиру',
                           'Продают раньше 5&nbsp;лет? Спросите почему'], 1))
S6 = page(top('towers', '50% 90%', 560)
          + f'<div class="col" style="top:500px"><h2 class="t">Что это значит для&nbsp;покупателя</h2><div style="margin-top:26px">{rows}</div></div>')

S7 = page(full('courtyard', '50% 100%', 560)
          + f'<div class="col" style="top:170px"><h2 class="t">А что сделки говорят о&nbsp;вашем ЖК?</h2>'
            f'<p class="p" style="margin-top:22px;color:{NAVY};font-weight:700">Введите название или адрес на&nbsp;<span style="color:{BLUE}">homecheck.kz</span></p></div>')

SLIDES = [S1, S2, S3, S4, S5, S6, S7]

if __name__ == '__main__':
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        for k, html in enumerate(SLIDES, 1):
            render(html, HERE / f'{k:02d}.jpg', pg)
        b.close()
    print('ok')
