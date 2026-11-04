"""Post 2026-11-07: «Почему нашим данным можно доверять» (витрина, закрепить)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'templates'))
from PIL import Image
from playwright.sync_api import sync_playwright
from render import *
import illustrations as il

OUT = pathlib.Path(__file__).resolve().parent
PH = HERE.parent / 'assets' / 'photos'
BOX = '<div class="box" style="top:200px">'

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    def scene(**kw):
        return lambda hh: svg_to_image(il.city(h=hh, **kw), 1080, hh, pg)
    I = lambda inner, src, h=1350: compose(inner, src, ILLUS, pg, h=h)
    F = lambda inner, name, h=1350: compose(inner, Image.open(PH / name), PHOTO, pg, h=h)
    S = [
        I(logo(64) + BOX + '<h1 class="t">Почему нашим данным можно доверять</h1>'
          '<span class="p acc">Листайте →</span></div>', scene(seed=7, magnifier=True)),
        F(logo(64) + BOX + '<h2 class="t">Это не объявления</h2>'
          '<p class="p">Мы берём цены из <b>зарегистрированных сделок</b>: за сколько квартиры реально купили.</p></div>',
          'astana-khan-shatyr.jpg'),
        I(logo(64) + '<div class="box" style="top:250px;gap:28px">'
          '<p class="lb">Сделки с жильём регистрирует государство</p>'
          '<p class="num">27 096</p>'
          '<p class="p">сделок с квартирами за сентябрь 2026 в&nbsp;Казахстане</p>'
          '<p class="lb">Источник: Бюро национальной статистики</p></div>', scene(seed=11)),
        I(logo(64) + BOX + '<h2 class="t">Сравниваем с этим же домом</h2>'
          '<p class="p">Не со средней ценой по городу, а <b>с похожими квартирами в том же доме</b>.</p></div>',
          scene(seed=3, mirror=True)),
        F(logo(64) + BOX + '<h2 class="t">Проверьте нас на своей квартире</h2>'
          '<p class="p">Введите адрес, где живёте, и мы покажем, <b>когда вы её купили</b>.</p>'
          '<p class="lb">Если сделка есть в наших данных</p></div>', 'astana-panorama.jpg'),
        I(logo(64) + BOX + '<h2 class="t">Проверьте квартиру до покупки</h2>'
          '<p class="p">Введите адрес на <b>homecheck.kz</b></p></div>', scene(seed=21)),
    ]
    for k, html in enumerate(S, 1):
        render(html, OUT / f'{k:02d}.jpg', pg)
    b.close()
print('ok')
