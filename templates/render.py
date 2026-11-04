"""HomeCheck social slide templates: HTML per slide type -> PNG/JPG via Playwright.

Rules live in the project doc «HomeCheck — Соцсети», section «Шаблон».
Feed 1080x1350 (4:5, required by Instagram API autopublishing), vertical 1080x1920.
"""
import base64, io, os, pathlib
from PIL import Image, ImageEnhance
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
FONT_LOGO = HERE / 'fonts' / 'BarlowCondensed-Bold.ttf'
FONT_LOGO_URI = 'data:font/ttf;base64,' + base64.b64encode(FONT_LOGO.read_bytes()).decode()
BG_RGB = (0xBB, 0xD6, 0xF2)

# Image treatments: photos are washed more than illustrations (illustrations are lighter to begin with).
PHOTO = dict(wash=0.45, sat=0.60, fade=320)
ILLUS = dict(wash=0.30, sat=0.70, fade=320)

CSS = f"""
@font-face{{font-family:'Barlow Condensed';font-weight:700;src:url('{FONT_LOGO_URI}')}}
body{{margin:0}}
.s{{position:relative;overflow:hidden;background:#BBD6F2;color:#0B2545;font-family:Inter,sans-serif}}
.logo{{position:absolute;left:80px;font-family:'Barlow Condensed',sans-serif;font-size:72px;font-weight:700;line-height:1}}
.logo .h{{color:#12253E}} .logo .c{{color:#049BE1}}
.box{{position:absolute;left:80px;width:920px;display:flex;flex-direction:column;gap:44px}}
.t{{margin:0;font-size:100px;line-height:1.05;font-weight:800;letter-spacing:-0.025em}}
.p{{margin:0;font-size:56px;line-height:1.3;font-weight:400}}
.p b{{font-weight:800}}
.lb{{margin:0;font-size:40px;line-height:1.3;color:#2F4566}}
.num{{margin:0;font-size:200px;line-height:1;font-weight:800;letter-spacing:-0.03em}}
.acc{{color:#1768CE;font-weight:800}}
.img{{position:absolute;left:0;bottom:0;width:1080px;display:block}}
ul.l{{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:22px}}
ul.l li{{font-size:56px;line-height:1.25;padding-left:56px;position:relative}}
ul.l li:before{{content:'';position:absolute;left:0;top:26px;width:24px;height:24px;border-radius:50%;background:#2D8CFF}}
"""
# Text style sizes: title 100 / text 56 / label 40 / number 200. Logo 72 (not counted).


def treat(img, height, wash, sat, fade, top=None):
    """Scale to 1080 wide, crop a bottom strip (or from `top`), wash into bg, fade the top edge."""
    w, h = img.size
    s = img.convert('RGB').resize((1080, round(h * 1080 / w)), Image.LANCZOS)
    t = s.size[1] - height if top is None else top
    s = s.crop((0, t, 1080, t + height))
    s = ImageEnhance.Color(s).enhance(sat)
    bg = Image.new('RGB', s.size, BG_RGB)
    s = Image.blend(s, bg, wash)
    mask = Image.new('L', s.size, 255)
    px = mask.load()
    for y in range(min(fade, height)):
        k = y / fade
        a = int(255 * (k * k * (3 - 2 * k)))
        for x in range(1080):
            px[x, y] = a
    return Image.composite(s, bg, mask)


def data_uri(img):
    buf = io.BytesIO()
    img.save(buf, 'JPEG', quality=90)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


def svg_to_image(svg, w, h, page):
    page.set_viewport_size({'width': w, 'height': h})
    page.set_content(f'<html><body style="margin:0">{svg}</body></html>')
    return Image.open(io.BytesIO(page.screenshot(clip={'x': 0, 'y': 0, 'width': w, 'height': h})))


def logo(top):
    return f'<span class="logo" style="top:{top}px"><span class="h">Home</span><span class="c">Check.kz</span></span>'


def slide(inner, h=1350, img=None, img_h=0):
    pic = f'<img class="img" style="height:{img_h}px" src="{img}">' if img else ''
    return (f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body><div class="s" style="width:1080px;height:{h}px">{pic}{inner}</div></body></html>')


def render(html, path, page, h=1350):
    page.set_viewport_size({'width': 1080, 'height': h})
    page.set_content(html)
    page.evaluate('document.fonts.ready')
    page.wait_for_timeout(150)
    png = page.screenshot(clip={'x': 0, 'y': 0, 'width': 1080, 'height': h})
    Image.open(io.BytesIO(png)).convert('RGB').save(path, quality=92)


def compose(inner, src, treatment, page, h=1350, overlap=120, top=None):
    """Image fills everything below the text: it starts `overlap` px above the bottom of the text block,
    so the faded top of the picture sits under the last lines and no empty background band remains."""
    page.set_viewport_size({'width': 1080, 'height': h})
    page.set_content(slide(inner, h=h))
    page.evaluate('document.fonts.ready')
    page.wait_for_timeout(100)
    bottom = page.evaluate("Math.max(...[...document.querySelectorAll('.box')].map(e => e.getBoundingClientRect().bottom))")
    img_h = int(h - bottom + overlap)
    if callable(src):  # illustration drawn for the exact strip height
        src = src(img_h)
    return slide(inner, h=h, img=data_uri(treat(src, img_h, top=top, **treatment)), img_h=img_h)
