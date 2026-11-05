"""Post 2026-11-07: «Почему нашим данным можно доверять» (витрина, закрепить).
v2: картинки сгенерированы в ChatGPT (src/01-06.png), текст и логотип — шаблоном.
Картинка занимает весь слайд; если текст доходит до сцены, картинка сдвигается вниз,
а сверху достраивается её же небо. Картинки не приглушаем: пост закреплённый, он ярче остальных."""
import sys, pathlib, io
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'templates'))
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
from render import *

OUT = pathlib.Path(__file__).resolve().parent
BOX = '<div class="box" style="top:200px">'
GAP = 40  # min space between text and the scene

INNER = [
    logo(64) + BOX + '<h1 class="t">Почему нашим данным можно доверять</h1><span class="p acc">Листайте →</span></div>',
    logo(64) + BOX + '<h2 class="t">Данные из госрегистрации</h2>'
      '<p class="p">Каждая продажа квартиры регистрируется государством. <b>На этих записях построены наши данные.</b></p></div>',
    logo(64) + '<div class="box" style="top:200px;gap:28px">'
      '<p class="num">≈33&nbsp;000</p>'
      '<p class="p">сделок с жильём в среднем регистрируют в Казахстане каждый месяц в 2026 году</p>'
      '<p class="lb">Источник: Бюро национальной статистики</p></div>',
    logo(64) + BOX + '<h2 class="t">Сравниваем с этим же домом</h2>'
      '<p class="p">Не со средней ценой по городу, а <b>с похожими квартирами в&nbsp;том же доме</b>.</p></div>',
    logo(64) + BOX + '<h2 class="t">Без личных данных</h2>'
      '<p class="p">Мы не показываем, кто продавал и покупал квартиру, — <b>только сделки, цены и даты</b>.</p></div>',
    logo(64) + BOX + '<h2 class="t">Узнайте главное до покупки</h2>'
      '<p class="p">Введите адрес на <b>homecheck.kz</b> и посмотрите историю квартиры до&nbsp;сделки.</p></div>',
]


def scene_top(img):
    a = np.asarray(img).astype(int)
    sky = a[5:40].reshape(-1, 3).mean(0)
    rows = (np.abs(a - sky).sum(2) > 40).mean(1)
    return int(np.argmax(rows > 0.01))


SCALE = {4: 0.85, 6: 0.85}  # isolated object on plain sky: shrink instead of cutting off the lower floor


def fit(img, text_bottom, scale=1.0):
    """1080x1350 background: image scaled to width, shifted down if the text reaches the scene."""
    img = img.convert('RGB').resize((1080, round(img.size[1] * 1080 / img.size[0])), Image.LANCZOS)
    if scale != 1.0:  # shrink and extend edges with the image's own border pixels
        w, h = round(1080 * scale), round(img.size[1] * scale)
        small = np.asarray(img.resize((w, h), Image.LANCZOS))
        l = (1080 - w) // 2
        img = Image.fromarray(np.pad(small, ((img.size[1] - h, 0), (l, 1080 - w - l), (0, 0)), mode='edge'))
    img = img.crop((0, img.size[1] - 1350, 1080, img.size[1])) if img.size[1] > 1350 else img
    shift = max(0, int(text_bottom + GAP - scene_top(img)))
    if shift:
        sky = img.crop((0, 0, 1080, 1)).resize((1080, shift))
        out = Image.new('RGB', (1080, 1350))
        out.paste(sky, (0, 0)); out.paste(img.crop((0, 0, 1080, 1350 - shift)), (0, shift))
        img = out
    return img, shift


with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    for k, inner in enumerate(INNER, 1):
        pg.set_viewport_size({'width': 1080, 'height': 1350}); pg.set_content(slide(inner))
        pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(100)
        bottom = pg.evaluate("Math.max(...[...document.querySelectorAll('.box')].map(e => e.getBoundingClientRect().bottom))")
        bg, shift = fit(Image.open(OUT / 'src' / f'{k:02d}.png'), bottom, SCALE.get(k, 1.0))
        print(k, 'text bottom', int(bottom), 'shift', shift)
        render(slide(inner, img=data_uri(bg), img_h=1350), OUT / f'{k:02d}.jpg', pg)
    b.close()
print('ok')
