"""Пост «Две похожие квартиры в соседних домах» (пн 23.11.2026). Рубрика «Люди и ситуации».
Иллюстрации — ChatGPT (команда), героиня та же, что в Reels «Тогда и сейчас»; метка ИИ.
Цифры условные (дома без названий); пометку «Пример» команда убрала 16.11.2026. Фирменная палитра: А — жёлтый, Б — синий. Типографика: 76 / 120 / 40."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'templates'))
from playwright.sync_api import sync_playwright
from render import FONT_LOGO_URI, render, data_uri
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
NAVY, BLUE, YEL, CREAM = '#0B2545', '#1768CE', '#FFC94D', '#EAF4FF'
TERRA = NAVY
COL = {'А': YEL, 'Б': BLUE}
NUM = {'А': NAVY, 'Б': BLUE}
FG = {'А': NAVY, 'Б': '#FFFFFF'}
TINT = {'А': '#FFF3D1', 'Б': '#D6E7FB'}
IMG = {n: data_uri(Image.open(HERE / 'src' / f'{n}.jpg')) for n in
       ['houses', 'flat_a', 'flat_b', 'house_a', 'house_b', 'cafe', 'balcony']}

CSS = f"""
@font-face{{font-family:'Barlow Condensed';font-weight:700;src:url('{FONT_LOGO_URI}')}}
*{{box-sizing:border-box}} body{{margin:0}}
.s{{position:relative;width:1080px;height:1350px;overflow:hidden;font-family:Inter,sans-serif;color:{NAVY};background:radial-gradient(80% 50% at 85% 0%,#FFFFFF 0%,rgba(255,255,255,0) 60%),linear-gradient(180deg,#F2F8FF 0%,#DCEBFB 100%)}}
.logo{{position:absolute;left:80px;top:60px;font-family:'Barlow Condensed';font-size:58px;font-weight:700;line-height:1;z-index:5}}
.logo .h{{color:#12253E}} .logo .c{{color:#049BE1}}
.ex{{position:absolute;right:80px;top:66px;z-index:5;font-size:30px;font-weight:700;color:#5B6B80;background:rgba(255,255,255,.8);border-radius:999px;padding:6px 20px}}
.col{{position:absolute;left:80px;width:920px;z-index:4}}
.t{{margin:0;font-size:76px;line-height:1.08;font-weight:800;letter-spacing:-.025em}}
.p{{font-size:40px;line-height:1.3;font-weight:500;color:#33465E;margin:0}}
.b{{font-weight:700;color:{NAVY}}}
.lab{{font-size:40px;font-weight:700;margin:0 0 10px}}
.badge{{display:inline-flex;align-items:center;justify-content:center;width:84px;height:84px;border-radius:50%;color:#fff;font-size:48px;font-weight:800}}
.card{{border-radius:36px;overflow:hidden;position:relative}}
.n{{font-size:120px;line-height:.95;font-weight:800;letter-spacing:-.04em}}
"""


def page(inner, ex=False):
    return (f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="s">'
            f'<span class="logo"><span class="h">Home</span><span class="c">Check.kz</span></span>'
            f'{inner}</div></body></html>')


def badge(k, size=84, fs=48):
    return f'<span class="badge" style="background:{COL[k]};color:{FG[k]};width:{size}px;height:{size}px;font-size:{fs}px">{k}</span>'


# 1 — обложка: картинка на весь слайд, текст в небе, метки А и Б на домах
S1 = page(f'<img src="{IMG["houses"]}" style="position:absolute;inset:0;width:1080px;height:1350px;object-fit:cover">'
          f'<div class="col" style="top:170px"><h1 class="t">Две похожие квартиры. Какую выберете?</h1>'
          f'<p class="p b" style="margin-top:22px">Листайте →</p></div>'
          f'<div style="position:absolute;left:150px;top:520px;z-index:4">{badge("А", 100, 56)}</div>'
          f'<div style="position:absolute;left:840px;top:520px;z-index:4">{badge("Б", 100, 56)}</div>')

# 2 — две квартиры рядом
def flat(k, img, rows):
    r = ''.join(f'<p class="p" style="padding:14px 0;border-top:2px solid rgba(11,37,69,.08)">{x}</p>' for x in rows)
    return (f'<div style="width:440px"><div style="display:flex;align-items:center;gap:18px;margin-bottom:18px">{badge(k, 64, 36)}<span class="p b">Квартира {k}</span></div>'
            f'<div class="card" style="height:400px"><img src="{IMG[img]}" style="width:100%;height:100%;object-fit:cover"></div><div style="margin-top:14px">{r}</div></div>')

S2 = page(f'<div class="col" style="top:170px"><h2 class="t">Обе — за&nbsp;40&nbsp;млн&nbsp;₸</h2>'
          f'<p class="p" style="margin-top:14px">64&nbsp;м², 2&nbsp;комнаты</p></div>'
          f'<div class="col" style="top:430px;display:flex;justify-content:space-between">'
          + flat('А', 'flat_a', ['<b class=b>5</b> этаж', 'Вид <b class=b>во двор</b>', 'Ремонт <b class=b>5&nbsp;лет назад</b>'])
          + flat('Б', 'flat_b', ['<b class=b>11</b> этаж', 'Вид <b class=b>на парк</b>', '<b class=b>Свежий</b> ремонт'])
          + '</div>', ex=True)

# 3 — ваш выбор
S3 = page(f'<div class="col" style="top:170px;display:flex;justify-content:space-between">'
          + ''.join(f'<div style="width:440px"><div style="display:flex;justify-content:center;margin-bottom:22px">{badge(k, 120, 72)}</div>'
                    f'<div class="card" style="height:440px"><img src="{IMG[i]}" style="width:100%;height:100%;object-fit:cover"></div></div>'
                    for k, i in [('А', 'flat_a'), ('Б', 'flat_b')])
          + '</div>'
          f'<div class="col" style="top:820px"><h2 class="t">Ваш выбор?</h2>'
          f'<p class="p" style="margin-top:22px">Напишите в&nbsp;комментариях: <b style="color:#C98F00">А</b> или <b style="color:{BLUE}">Б</b></p>'
          f'<p class="p b" style="margin-top:14px">Теперь посмотрим на&nbsp;сделки →</p></div>')


# 4–7 — сравнения
def versus(section, title, a, b, line, thumbs=('house_a', 'house_b')):
    def side(k, v, th):
        n, u = v
        return (f'<div class="card" style="width:440px;background:{TINT[k]};padding:0 0 34px">'
                f'<div style="height:230px;position:relative"><img src="{IMG[th]}" style="width:100%;height:100%;object-fit:cover"></div>'
                f'<div style="padding:24px 30px 0"><div style="display:flex;align-items:center;gap:14px;margin-bottom:14px">{badge(k, 56, 32)}<span class="p b">{"Дом" if th.startswith("house") else "Квартира"} {k}</span></div>'
                f'<div class="n" style="color:{NUM[k]}">{n}</div>'
                f'<p class="p b" style="margin-top:12px">{u}</p></div></div>')
    return page(f'<div class="col" style="top:170px"><h2 class="t">{title}</h2></div>'
                f'<div class="col" style="top:400px;display:flex;justify-content:space-between;align-items:stretch">{side("А", a, thumbs[0])}{side("Б", b, thumbs[1])}</div>'
                f'<p class="p col" style="top:1080px">{line}</p>', ex=True)


S4 = versus('', 'Цена метра в&nbsp;доме', ('590', 'тыс. ₸ за м²'), ('520', 'тыс. ₸ за м²'),
            'За&nbsp;Б просят больше, чем обычно платят в&nbsp;её доме')
S5 = versus('', 'Как растут цены', ('+9%', 'за год'), ('+2%', 'за год'),
            'Дом А дорожает, Б — почти нет')
S6 = versus('Сначала — дома', 'Как часто здесь перепродают', ('1 из 20', 'квартир за год'), ('1 из 7', 'квартир за год'),
            'Если в&nbsp;доме часто продают, стоит узнать почему')
S7 = versus('', 'Как часто продавали квартиру', ('7 лет', 'один владелец'), ('2', 'продажи за&nbsp;3&nbsp;года'),
            'Б часто меняет хозяев', thumbs=('flat_a', 'flat_b'))

# 8 — что получается
S8 = page(f'<img src="{IMG["cafe"]}" style="position:absolute;left:0;top:0;width:1080px;height:640px;object-fit:cover;object-position:50% 0%">'
          f'<div style="position:absolute;left:0;top:0;width:1080px;height:200px;z-index:2;background:linear-gradient(180deg,rgba(242,248,255,.9),rgba(242,248,255,0))"></div>'
          f'<div style="position:absolute;left:0;top:420px;width:1080px;height:230px;z-index:2;background:linear-gradient(180deg,rgba(230,241,253,0),#E6F1FD)"></div>'
          f'<div class="col" style="top:600px"><h2 class="t">Что получается</h2>'
          f'<div style="display:flex;gap:26px;margin-top:34px;align-items:flex-start">{badge("А", 72, 40)}'
          f'<p class="p" style="flex:1">Цена в&nbsp;рынке, понятная история</p></div>'
          f'<div style="display:flex;gap:26px;margin-top:30px;align-items:flex-start">{badge("Б", 72, 40)}'
          f'<p class="p" style="flex:1">Дороже рынка — <b class=b>есть вопросы к&nbsp;продавцу</b></p></div></div>')

# 9 — финал: картинка на весь слайд, текст в небе
S9 = page(f'<img src="{IMG["balcony"]}" style="position:absolute;inset:0;width:1080px;height:1350px;object-fit:cover;object-position:50% 50%">'
          f'<div style="position:absolute;left:0;top:0;width:1080px;height:640px;z-index:2;background:linear-gradient(180deg,rgba(242,248,255,.95) 0%,rgba(242,248,255,.85) 60%,rgba(242,248,255,0) 100%)"></div>'
          f'<div class="col" style="top:170px"><h2 class="t">Выбирайте квартиру не&nbsp;только глазами</h2>'
          f'<p class="p b" style="margin-top:22px">Сравните дом и&nbsp;квартиру по&nbsp;данным на&nbsp;<span style="color:{BLUE}">homecheck.kz</span></p></div>')

SLIDES = [S1, S2, S3, S4, S5, S7, S8, S9]

if __name__ == '__main__':
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        for k, html in enumerate(SLIDES, 1):
            render(html, HERE / f'{k:02d}.jpg', pg)
        b.close()
    print('ok')
