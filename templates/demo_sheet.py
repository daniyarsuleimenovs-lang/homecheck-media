"""Template sheet: every slide type on demo text. Every slide has an image (photo or illustration)."""
import sys, pathlib
from PIL import Image
from playwright.sync_api import sync_playwright
from render import *
import illustrations as il

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'sheet_out')
OUT.mkdir(exist_ok=True)
PH = HERE.parent / 'assets' / 'photos'

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    def scene(**kw):
        return lambda hh: svg_to_image(il.city(h=hh, **kw), 1080, hh, pg)
    city_mag = scene(seed=7, magnifier=True)
    city_a = scene(seed=11)
    city_b = scene(seed=3, mirror=True)

    def I(inner, src, h=1350):
        return compose(inner, src, ILLUS, pg, h=h)

    def F(inner, name, h=1350):
        return compose(inner, Image.open(PH / name), PHOTO, pg, h=h)

    S = {}
    # 1. Cover — illustration
    S['01_oblozhka_illustr'] = I(logo(64) + '<div class="box" style="top:200px">'
        '<h1 class="t">Почему нашим данным можно доверять</h1>'
        '<span class="p acc">Листайте →</span></div>', city_mag)
    # 2. Text — photo
    S['02_tekst_foto'] = F(logo(64) + '<div class="box" style="top:200px">'
        '<h2 class="t">Это не объявления</h2>'
        '<p class="p">Мы берём цены из <b>зарегистрированных сделок</b>. Это то, за сколько квартиры реально купили.</p></div>',
        'astana-baiterek.jpg')
    # 3. List
    S['03_spisok'] = I(logo(64) + '<div class="box" style="top:200px">'
        '<h2 class="t">О чём спросить продавца</h2>'
        '<ul class="l"><li>Почему продаёте квартиру?</li><li>Как давно она продаётся?</li><li>Когда делали ремонт?</li><li>Были ли перепланировки?</li></ul>'
        '<p class="lb">Сохраните, пригодится на просмотре.</p></div>', city_b)
    # 4. Number — low city strip
    S['04_cifra'] = I(logo(64) + '<div class="box" style="top:250px;gap:28px">'
        '<p class="lb">Сделки с жильём в Казахстане, апрель 2026</p>'
        '<p class="num">35 154</p>'
        '<p class="p">сделки купли-продажи жилья за один месяц.</p>'
        '<p class="lb">Источник: Бюро национальной статистики</p></div>', city_a)
    # 5. Comparison — illustration
    S['05_sravnenie_illustr'] = I(logo(64) + '<div class="box" style="top:200px;gap:36px">'
        '<h2 class="t">Пример: 3-комн., 78&nbsp;м²</h2>'
        '<div><p class="lb">Объявление</p><p class="t">41 млн ₸</p></div>'
        '<div><p class="lb">Похожие квартиры в доме</p><p class="t">37–39 млн ₸</p></div></div>',
        city_a)
    # 6. Final — illustration
    S['06_final_illustr'] = I(logo(64) + '<div class="box" style="top:200px">'
        '<h2 class="t">Проверьте квартиру до покупки</h2>'
        '<p class="p">Введите адрес на <b>homecheck.kz</b></p></div>',
        city_b)

    for name, html in S.items():
        render(html, OUT / f'{name}.jpg', pg)

    # 7. Story (9:16): text inside safe zone (top 270, bottom 384)
    story = I(logo(300) + '<div class="box" style="top:430px">'
        '<p class="lb">Новый пост</p>'
        '<h1 class="t">Почему нашим данным можно доверять</h1>'
        '<span class="p acc">Смотрите в профиле</span></div>', city_mag, h=1920)
    render(story, OUT / '07_storis.jpg', pg, h=1920)
    # 8. Reels cover (9:16): important content inside the central 3:4 zone (y 240..1680)
    reel = I(logo(304) + '<div class="box" style="top:440px">'
        '<h1 class="t">Квартиру продают второй раз за год</h1>'
        '<p class="p">Что это может значить</p></div>', city_a, h=1920)
    render(reel, OUT / '08_oblozhka_reels.jpg', pg, h=1920)

    # 9. Highlight covers: icon centered (Instagram crops a circle from the middle)
    icons = {
        'kak_rabotaet': '<path d="M40 92 L100 40 L160 92 V160 H40Z" fill="#0B2545"/><rect x="88" y="112" width="24" height="48" fill="#2D8CFF"/>',
        'dannye': '<rect x="40" y="110" width="28" height="50" rx="4" fill="#0B2545"/><rect x="86" y="80" width="28" height="80" rx="4" fill="#0B2545"/><rect x="132" y="50" width="28" height="110" rx="4" fill="#2D8CFF"/>',
        'voprosy': '<path d="M70 72 C70 45 130 45 130 72 C130 95 100 96 100 120" fill="none" stroke="#0B2545" stroke-width="20" stroke-linecap="round"/><circle cx="100" cy="154" r="12" fill="#2D8CFF"/>',
    }
    for k, (name, svg) in enumerate(icons.items()):
        html = ('<!doctype html><html><body style="margin:0"><div style="width:1080px;height:1920px;background:#BBD6F2;'
                'display:flex;align-items:center;justify-content:center">'
                f'<svg width="560" height="560" viewBox="0 0 200 200">{svg}</svg></div></body></html>')
        render(html, OUT / f'09_aktualnoe_{name}.jpg', pg, h=1920)
    b.close()
print('ok')
