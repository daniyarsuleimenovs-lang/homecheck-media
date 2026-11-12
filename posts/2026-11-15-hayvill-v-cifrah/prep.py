"""Подготовка фото Хайвилла (фото команды, разрешены к публикации). Оригиналы в репозиторий не кладём:
на фото 4 есть люди и вывеска магазина — в кадрах их нет. Небо перекрашиваем в фирменный голубой."""
import sys, pathlib
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from scipy import ndimage

SRC = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path('/mnt/user-data/attachments/316e28d6-cc64-504b-83e1-3a131c4a553a')
OUT = pathlib.Path(__file__).resolve().parent / 'src'
P1, P2, P3, P4 = (SRC / f for f in ['21017347-image.jpg', 'dc2a8e1f-image.jpg', 'd6f5ca72-image.jpg', '5dc13d67-image.jpg'])
TOP, BOT = np.array([0xBB, 0xD6, 0xF2], float), np.array([0xDC, 0xEB, 0xFB], float)

def grade(img, c=1.08, s=1.12):
    return ImageEnhance.Color(ImageEnhance.Contrast(img.convert('RGB')).enhance(c)).enhance(s)

def recolor_sky(img, tol=34):
    a = np.asarray(img).astype(float)
    sky = np.median(a[:12].reshape(-1, 3), 0)
    close = np.abs(a - sky).sum(2) < tol
    lab, _ = ndimage.label(close)
    top = set(np.unique(lab[:3])) - {0}
    m = np.isin(lab, list(top)).astype(np.uint8) * 255
    m = np.asarray(Image.fromarray(m).filter(ImageFilter.GaussianBlur(2))).astype(float)[..., None] / 255
    h = a.shape[0]
    grad = (TOP + (BOT - TOP) * (np.arange(h)[:, None, None] / h)).repeat(a.shape[1], 1)
    out = a * (1 - m) + (grad + (a - sky) * .6) * m
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))

def card(path, box, size=(920, 510), sky=True, g=True):
    im = Image.open(path).convert('RGB').crop(box)
    im = grade(im) if g else im
    im = im.resize(size, Image.LANCZOS)
    return recolor_sky(im) if sky else im

if __name__ == '__main__':
    # cover: tower + sign, 4:5
    cov = grade(Image.open(P1).crop((0, 220, 1449, 220 + 1811))).resize((1080, 1350), Image.LANCZOS)
    recolor_sky(cov).save(OUT / 'cover.jpg', quality=92)
    # final: obelisk with HIGHVILL ASTANA, 4:5
    fin = grade(Image.open(P2).crop((0, 120, 1449, 120 + 1811))).resize((1080, 1350), Image.LANCZOS)
    recolor_sky(fin).save(OUT / 'final.jpg', quality=92)
    # full-bleed backgrounds for slides 2-6 (v2, 13.11). Low-res photos are upscaled with EDSR beforehand (UP dir)
    def full(im, box, g=True, sky=False):
        im = im.convert('RGB').crop(box)
        im = grade(im) if g else im
        im = im.resize((1080, 1350), Image.LANCZOS)
        return recolor_sky(im) if sky else im
    UP = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else None
    if UP:
        full(Image.open(UP / 'p6.png'), (600, 0, 1800, 1500), g=False).save(OUT / 'b2.jpg', quality=92)   # fountain, summer
        full(Image.open(UP / 'p3.png'), (0, 0, 1474, 1842), g=False).save(OUT / 'b4.jpg', quality=92)      # sunny towers
        full(Image.open(UP / 'p5.png'), (275, 0, 1600, 1656), g=False).save(OUT / 'b6.jpg', quality=92)    # street, clouds
    full(Image.open(P4), (520, 0, 1680, 1450), sky=True).save(OUT / 'b3.jpg', quality=92)                   # gate, no shop/people
    full(Image.open(P2), (0, 0, 1449, 1811), sky=True).save(OUT / 'b5.jpg', quality=92)                     # towers + obelisk
    # cards 920x510 (≈1.8:1)
    card(P3, (0, 300, 828, 300 + 459), g=False).save(OUT / 'c2.jpg', quality=92)        # sunny towers
    card(P4, (440, 140, 1640, 140 + 666)).save(OUT / 'c3.jpg', quality=92)               # gate + pine, no people/shop
    card(P2, (0, 0, 1449, 805)).save(OUT / 'c4.jpg', quality=92)                         # tower tops
    card(P4, (1456, 0, 2576, 622)).save(OUT / 'c5.jpg', quality=92)                     # towers on the right, above the people
    print('ok')
