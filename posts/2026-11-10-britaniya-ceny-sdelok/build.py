"""Post 2026-11-10: «В Британии цену квартиры проверяют по реальным сделкам» (опыт мира).
Картинки сгенерированы в ChatGPT (src/01-05.png), текст и логотип — шаблоном.
У картинок почти белое небо — перекрашиваем его в фирменный #BBD6F2 (белый фон команде не подходит):
заливка от верхнего края по пикселям, близким к цвету неба, с мягким краем.
Дальше как в посте 07.11: картинка на весь слайд, при необходимости сдвигается вниз.
Заголовок обложки — 84 px вместо 100: на 100 px он занимает 5 строк и вытесняет картинку (осознанное отступление)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'templates'))
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
from playwright.sync_api import sync_playwright
from render import *

OUT = pathlib.Path(__file__).resolve().parent
BOX = '<div class="box" style="top:200px">'
GAP = 40
BG = np.array(BG_RGB, float)
SCALE = {}

INNER = [
    logo(64) + '<div class="box" style="top:200px;gap:36px">' + '<h1 class="t" style="font-size:84px">В Британии цену квартиры проверяют по реальным сделкам</h1><span class="p acc">Листайте →</span></div>',
    logo(64) + BOX + '<h2 class="t">Hometrack, с&nbsp;1999&nbsp;года</h2>'
      '<p class="p">Британская компания, которая проверяет цены жилья <b>по&nbsp;данным о реальных сделках</b>.</p></div>',
    logo(64) + '<div class="box" style="top:200px;gap:28px">'
      '<p class="num">1,4&nbsp;млн</p>'
      '<p class="p">одобрений ипотеки в год в&nbsp;Британии. Почти в каждом цену сверяют с данными Hometrack.</p></div>',
    logo(64) + BOX + '<h2 class="t">Что это даёт покупателю</h2>'
      '<ul class="l"><li>Цена проверена по сделкам, а&nbsp;не на глаз</li><li>Переплату видно до сделки</li><li>Решение опирается на факты</li></ul></div>',
    logo(64) + BOX + '<h2 class="t">Теперь это есть в&nbsp;Казахстане</h2>'
      '<p class="p">HomeCheck сравнивает квартиру <b>с реальными сделками в&nbsp;том же доме</b>.</p></div>',
]


def recolor_sky(img, tol=22):
    a = np.asarray(img.convert('RGB')).astype(float)
    sky = a[5:40].reshape(-1, 3).mean(0)
    close = np.abs(a - sky).sum(2) < tol
    lab, _ = ndimage.label(close)
    top = set(np.unique(lab[0])) - {0}
    m = np.isin(lab, list(top)).astype(np.uint8) * 255
    m = np.asarray(Image.fromarray(m).filter(ImageFilter.GaussianBlur(1.5))).astype(float)[..., None] / 255
    # keep the sky's own light shading, shifted to the brand colour
    out = a * (1 - m) + (BG + (a - sky)) * m
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))


def scene_top(img):
    a = np.asarray(img).astype(int)
    sky = a[5:40].reshape(-1, 3).mean(0)
    rows = (np.abs(a - sky).sum(2) > 40).mean(1)
    return int(np.argmax(rows > 0.01))


def fit(img, text_bottom, scale=1.0):
    img = img.convert('RGB').resize((1080, round(img.size[1] * 1080 / img.size[0])), Image.LANCZOS)
    if scale != 1.0:
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


if __name__ == '__main__':
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        for k, inner in enumerate(INNER, 1):
            pg.set_viewport_size({'width': 1080, 'height': 1350}); pg.set_content(slide(inner))
            pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(100)
            bottom = pg.evaluate("Math.max(...[...document.querySelectorAll('.box')].map(e => e.getBoundingClientRect().bottom))")
            src = recolor_sky(Image.open(OUT / 'src' / f'{k:02d}.png'))
            bg, shift = fit(src, bottom, SCALE.get(k, 1.0))
            print(k, 'text bottom', int(bottom), 'shift', shift)
            render(slide(inner, img=data_uri(bg), img_h=1350), OUT / f'{k:02d}.jpg', pg)
        b.close()
    print('ok')
