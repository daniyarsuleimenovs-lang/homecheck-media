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
    city_mag = svg_to_image(il.city(seed=7, magnifier=True), 1080, 900, pg)
    city_a = svg_to_image(il.city(seed=11), 1080, 900, pg)
    city_b = svg_to_image(il.city(seed=3, mirror=True), 1080, 900, pg)

    def ill(img, h):
        return data_uri(treat(img, h, **ILLUS))

    def photo(name, h, top=None):
        return data_uri(treat(Image.open(PH / name), h, top=top, **PHOTO))

    S = {}
    # 1. Cover — illustration
    S['01_oblozhka_illustr'] = slide(logo(64) + '<div class="box" style="top:200px">'
        '<h1 class="t">Почему нашим данным можно доверять</h1>'
        '<span class="p acc">Листайте →</span></div>', img=ill(city_mag, 680), img_h=680)
    # 2. Text — photo
    S['02_tekst_foto'] = slide(logo(64) + '<div class="box" style="top:200px">'
        '<h2 class="t">Это не объявления</h2>'
        '<p class="p">Мы берём цены из <b>зарегистрированных сделок</b>. Это то, за сколько квартиры реально купили.</p></div>',
        img=photo('astana-baiterek.jpg', 640), img_h=640)
    # 3. List — low city strip
    S['03_spisok'] = slide(logo(64) + '<div class="box" style="top:200px">'
        '<h2 class="t">О чём спросить продавца</h2>'
        '<ul class="l"><li>Почему продаёте квартиру?</li><li>Как давно она продаётся?</li><li>Когда делали ремонт?</li><li>Были ли перепланировки?</li></ul>'
        '<p class="lb">Сохраните, пригодится на просмотре.</p></div>', img=ill(city_b, 330), img_h=330)
    # 4. Number — low city strip
    S['04_cifra'] = slide(logo(64) + '<div class="box" style="top:250px;gap:28px">'
        '<p class="lb">Сделки с жильём в Казахстане, апрель 2026</p>'
        '<p class="num">35 154</p>'
        '<p class="p">сделки купли-продажи жилья за один месяц.</p>'
        '<p class="lb">Источник: Бюро национальной статистики</p></div>', img=ill(city_a, 380), img_h=380)
    # 5. Comparison — illustration
    S['05_sravnenie_illustr'] = slide(logo(64) + '<div class="box" style="top:200px;gap:36px">'
        '<h2 class="t">Пример: 3-комн., 78&nbsp;м²</h2>'
        '<div><p class="lb">Объявление</p><p class="t">41 млн ₸</p></div>'
        '<div><p class="lb">Похожие квартиры в доме</p><p class="t">37–39 млн ₸</p></div></div>',
        img=ill(city_a, 600), img_h=600)
    # 6. Final — illustration
    S['06_final_illustr'] = slide(logo(64) + '<div class="box" style="top:200px">'
        '<h2 class="t">Проверьте квартиру до покупки</h2>'
        '<p class="p">Введите адрес на <b>homecheck.kz</b></p></div>',
        img=ill(city_b, 720), img_h=720)

    for name, html in S.items():
        render(html, OUT / f'{name}.jpg', pg)

    # 7. Story (9:16): text inside safe zone (top 270, bottom 384)
    story = slide(logo(300) + '<div class="box" style="top:430px">'
        '<p class="lb">Новый пост</p>'
        '<h1 class="t">Почему нашим данным можно доверять</h1>'
        '<span class="p acc">Смотрите в профиле</span></div>', h=1920, img=ill(city_mag, 900), img_h=900)
    render(story, OUT / '07_storis.jpg', pg, h=1920)
    # 8. Reels cover (9:16): important content inside the central 3:4 zone (y 240..1680)
    reel = slide(logo(304) + '<div class="box" style="top:440px">'
        '<h1 class="t">Квартиру продают второй раз за год</h1>'
        '<p class="p">Что это может значить</p></div>', h=1920, img=ill(city_a, 920), img_h=920)
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
