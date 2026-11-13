"""Пост «Узнаёте этот ЖК? Atlant-6» (макет команды HomeCheck_Atlant6.pdf, 13.11.2026).
Перевёрстан в третьем стиле (как «История квартиры»): тексты, структура и цифры — без изменений."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'templates'))
from playwright.sync_api import sync_playwright
from render import FONT_LOGO_URI, render, data_uri
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
NAVY, BLUE, BRIGHT, YEL, LAB = '#0B2545', '#1768CE', '#2D8CFF', '#FFC94D', '#2F4566'
img = lambda n: data_uri(Image.open(HERE / 'src' / n))
N = 6

CSS = f"""
@font-face{{font-family:'Barlow Condensed';font-weight:700;src:url('{FONT_LOGO_URI}')}}
*{{box-sizing:border-box}} body{{margin:0}}
.s{{position:relative;width:1080px;height:1350px;overflow:hidden;font-family:Inter,sans-serif;color:{NAVY}}}
.dark{{background:radial-gradient(70% 50% at 85% 75%,rgba(45,140,255,.45) 0%,rgba(45,140,255,0) 70%),linear-gradient(170deg,#0F2E57 0%,#0B2545 60%,#081B33 100%);color:#fff}}
.paper{{background-color:#EAF2FC;background-image:linear-gradient(#D9E6F6 2px,transparent 2px),linear-gradient(90deg,#D9E6F6 2px,transparent 2px);background-size:90px 90px;background-position:-20px -20px}}
.logo{{position:absolute;left:80px;top:64px;font-family:'Barlow Condensed';font-size:64px;font-weight:700;line-height:1}}
.logo .h{{color:#12253E}} .logo .c{{color:#049BE1}} .dark .logo .h{{color:#fff}}
.t{{position:absolute;left:80px;top:180px;width:920px;margin:0;font-size:84px;line-height:1.06;font-weight:800;letter-spacing:-.025em}}
.card{{position:absolute;left:80px;width:920px;background:#fff;border-radius:40px;box-shadow:0 30px 70px rgba(11,37,69,.16),0 4px 12px rgba(11,37,69,.06)}}
.foot{{position:absolute;left:80px;width:920px;margin:0;font-size:44px;line-height:1.3;font-weight:700}}
.btn{{position:absolute;left:80px;width:920px;background:{YEL};border-radius:28px;padding:26px 36px;font-size:38px;font-weight:800;color:{NAVY}}}
.steps{{position:absolute;left:80px;right:80px;bottom:64px;display:flex;align-items:center;gap:12px}}
.steps i{{display:block;width:56px;height:10px;border-radius:5px;background:#C9DBF1}}
.steps i.on{{background:{BLUE}}}
.dark .steps i{{background:rgba(255,255,255,.22)}} .dark .steps i.on{{background:#fff}}
.steps span{{margin-left:auto;font-size:28px;font-weight:600;color:{LAB}}} .dark .steps span{{color:rgba(255,255,255,.7)}}
.chip{{display:inline-block;background:{YEL};border-radius:18px;padding:8px 20px;font-weight:800;color:{NAVY}}}
"""

def page(cls, k, inner):
    steps = ''.join(f'<i class="{"on" if j <= k else ""}"></i>' for j in range(1, N + 1))
    return (f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
            f'<div class="s {cls}"><span class="logo"><span class="h">Home</span><span class="c">Check.kz</span></span>{inner}'
            f'<div class="steps">{steps}<span>{k}/{N}</span></div></div></body></html>')

def bars(a, b, la, lb, chip, top_label=None):
    """Two-bar chart card body: values a (light) and b (blue)."""
    H = 270; mx = max(a, b)
    def col(v, lab, light, chip=''):
        h = H * v / mx
        return (f'<div style="width:380px;display:flex;flex-direction:column;align-items:center">'
                f'<div style="height:{H + 70}px;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;width:100%">'
                f'<div style="display:flex;align-items:center;gap:18px;margin-bottom:14px"><span style="font-size:52px;font-weight:800">{v}</span>{chip}</div>'
                f'<div style="width:100%;height:{h:.0f}px;border-radius:24px 24px 8px 8px;background:{"#BBD6F2" if light else BLUE}"></div></div>'
                f'<div style="align-self:flex-start;margin-top:22px;font-size:32px;line-height:1.25;font-weight:700">{lab}</div></div>')
    tl = (f'<div style="position:absolute;left:520px;top:40px;font-size:30px;font-weight:700;color:{LAB}">{top_label}</div>' if top_label else '')
    return (f'<div style="position:relative;padding:40px 60px 44px">'
            f'<div style="font-size:30px;font-weight:700;color:{LAB}">Цена за м², тыс. ₸</div>{tl}'
                        f'<div style="display:flex;justify-content:space-between;margin-top:10px">{col(a, la, True)}{col(b, lb, False, f'<span class=chip style=font-size:40px>{chip}</span>')}</div></div>')

def sub(t):
    return f'<span style="display:block;font-size:28px;font-weight:500;color:{LAB};margin-top:6px">{t}</span>'

def phone():
    return (f'<div style="position:absolute;left:610px;top:520px;width:390px;height:700px;transform:rotate(-4deg);'
            f'background:linear-gradient(160deg,#1F4E8C,#0B2545);border-radius:64px;padding:18px;box-shadow:0 50px 90px rgba(0,0,0,.4)">'
            f'<div style="background:#F6FAFF;border-radius:48px;height:100%;padding:70px 30px 30px;position:relative;color:{NAVY}">'
            f'<div style="position:absolute;left:50%;top:18px;width:120px;height:28px;margin-left:-60px;background:#0B2545;border-radius:14px"></div>'
            f'<div style="font-family:Barlow Condensed;font-size:40px;font-weight:700;margin-bottom:36px"><span style="color:#12253E">Home</span><span style="color:#049BE1">Check.kz</span></div>'
            f'<div style="font-size:38px;font-weight:800;line-height:1.15;margin-bottom:30px">Проверьте<br>ЖК бесплатно</div>'
            f'<div style="border:4px solid {BRIGHT};border-radius:22px;padding:18px 16px;font-size:24px;white-space:nowrap;color:{LAB};background:#fff">ЖК, улица или адрес</div>'
            f'<div style="margin-top:20px;background:{BLUE};color:#fff;border-radius:22px;padding:22px;text-align:center;font-size:32px;font-weight:800">Проверить</div>'
            f'</div></div>')

def stat(n, l, s, extra=''):
    return (f'<div style="padding:28px 36px"><div style="font-size:64px;line-height:1;font-weight:800;color:{BLUE};letter-spacing:-.03em;white-space:nowrap">{n}</div>'
            f'<div style="font-size:30px;font-weight:700;margin-top:12px;line-height:1.2">{l}</div>{sub(s)}{extra}</div>')

S1 = page('dark', 1,
    '<h1 class="t" style="top:170px">Узнаёте этот ЖК?</h1>'
    f'<div style="position:absolute;left:80px;top:272px;font-size:76px;font-weight:800;color:{YEL};letter-spacing:-.02em">Atlant-6</div>'
    '<div style="position:absolute;left:80px;top:372px;font-size:36px;color:#CFE0F5">Кунаева, 5 · Астана</div>'
    f'<div style="position:absolute;left:80px;top:450px;width:920px;height:600px;border-radius:40px;overflow:hidden;box-shadow:0 40px 80px rgba(0,0,0,.4)">'
    f'<img src="{img("collage.jpg")}" style="width:100%;height:100%;object-fit:cover;object-position:50% 30%">'
    '<div style="position:absolute;left:28px;bottom:28px;background:rgba(11,37,69,.75);color:#fff;border-radius:14px;padding:8px 18px;font-size:26px;font-weight:600">Коллаж</div></div>'
    '<p class="foot" style="top:1090px;color:#fff">Давайте проверим нашумевший дом на&nbsp;HomeCheck.kz.</p>')

S2 = page('paper', 2,
    '<h2 class="t">Что известно о доме</h2>'
    '<div class="card" style="top:330px">'
    '<div style="display:flex;gap:32px;align-items:center;padding:36px 40px;border-bottom:3px solid #E3ECF7">'
    f'<img src="{img("house.jpg")}" style="width:170px;height:170px;border-radius:26px;object-fit:cover;object-position:40% 40%">'
    '<div><div style="font-size:50px;font-weight:800">Atlant-6</div><div style="font-size:32px;color:#2F4566;margin:6px 0 14px">Кунаева, 5 · Астана</div>'
    f'<span style="background:#E3EEFC;color:{BLUE};border-radius:14px;padding:8px 18px;font-size:28px;font-weight:700">2024 · год постройки</span></div></div>'
    '<div style="display:grid;grid-template-columns:1fr 1fr">'
    + f'<div style="border-right:3px solid #E3ECF7;border-bottom:3px solid #E3ECF7">{stat("60", "продаж всего", "фев. 2025 — июль 2026")}</div>'
    + f'<div style="border-bottom:3px solid #E3ECF7">{stat("16", "продаж в 2026 году", "январь–июль 2026")}</div>'
    + f'<div style="border-right:3px solid #E3ECF7">{stat("900 тыс. ₸", "средняя цена сделок за&nbsp;м²", "январь–июль 2026")}</div>'
    + stat("+12,3%", "рост цены за м² за год", "Средний рост по&nbsp;ЖК Астаны",
           f'<span style="display:block;font-size:28px;font-weight:800;color:{NAVY}">+13,0% за год</span>')
    + '</div></div>'
    '<div class="btn" style="top:1100px;font-size:34px">Профиль ЖК на HomeCheck.kz — бесплатно</div>')

S3 = page('paper', 3,
    '<h2 class="t">Цена в объявлении и&nbsp;цены сделок</h2>'
    '<div class="card" style="top:400px">'
    + bars(1000, 900, f'Объявление<br>в этом доме{sub("ноябрь 2026")}', f'По сделкам<br>в этом доме{sub("январь–июль 2026")}', '-10%')
    + '</div><p class="foot" style="top:1070px">Средняя цена сделок в доме на&nbsp;10% ниже этого объявления.</p>')

S4 = page('paper', 4,
    '<h2 class="t">Сравним с ценами по&nbsp;Астане</h2>'
    '<div class="card" style="top:400px">'
    + bars(618, 900, f'Астана: объявления{sub("октябрь 2026")}', f'Atlant-6: сделки{sub("январь–июль 2026")}', '+46%', 'Цена в ЖК')
    + '</div><p class="foot" style="top:1070px;font-size:40px">900 тыс. ₸/м² — по сделкам дома.<br>618 тыс. ₸/м² — по объявлениям Астаны.</p>')

LOCK = (f'<svg width="22" height="26" viewBox="0 0 22 26" style="margin-right:10px"><rect x="2" y="11" width="18" height="13" rx="3" fill="none" stroke="{LAB}" stroke-width="2.6"/>'
        f'<path d="M6 11V7a5 5 0 0 1 10 0v4" fill="none" stroke="{LAB}" stroke-width="2.6"/></svg>')
ROWS = [('40–60 м²', 'июль 2026', None), ('60–80 м²', 'июнь 2026', 1), ('200–220 м²', 'июнь 2026', 1), ('120–140 м²', 'июнь 2026', 1), ('160–180 м²', 'май 2026', 1)]
rows = ''.join(
    f'<div style="display:flex;justify-content:space-between;align-items:center;padding:14px 0;border-top:3px solid #E3ECF7">'
    f'<div><div style="font-size:36px;font-weight:800">{a}</div>{sub(d)}</div>'
    + (f'<div style="font-size:34px;font-weight:800;color:{BLUE}">900 тыс. ₸/м²</div>' if not lk else
       f'<div style="display:flex;align-items:center;background:#EAF2FC;border-radius:999px;padding:12px 26px;font-size:28px;font-weight:700;color:{LAB}">{LOCK}в отчёте</div>')
    + '</div>' for a, d, lk in ROWS)
S5 = page('paper', 5,
    '<h2 class="t">Сделки в этом доме</h2>'
    f'<div class="card" style="top:310px;padding:28px 44px 10px"><div style="font-size:32px;font-weight:800;padding-bottom:18px">Зарегистрированные продажи</div>{rows}</div>'
    '<p class="foot" style="top:1015px;font-size:42px">Полный отчёт по каждой квартире — на&nbsp;HomeCheck.kz</p>'
    '<div class="btn" style="top:1150px">Посмотреть историю квартиры</div>')

items = ''.join(f'<div style="display:flex;gap:22px;align-items:flex-start;margin-top:44px"><span style="flex:none;width:22px;height:22px;border-radius:50%;background:{YEL};margin-top:14px"></span>'
                f'<span style="font-size:42px;line-height:1.2;font-weight:700">{t}</span></div>'
                for t in ['Сколько квартир<br>продавали', 'Какие цены были<br>в сделках', 'Как часто<br>перепродавали'])
S6 = page('dark', 6,
    f'<h2 class="t" style="top:170px">Проверьте ЖК<br><span style="color:{YEL}">бесплатно</span></h2>'
    '<div style="position:absolute;left:80px;top:420px;font-size:38px;font-weight:700">На HomeCheck.kz можно узнать:</div>'
    f'<div style="position:absolute;left:80px;top:500px;width:520px">{items}</div>' + phone()
    + '<div style="position:absolute;left:80px;bottom:120px;width:520px;font-size:28px;line-height:1.35;color:rgba(255,255,255,.75)">Историю конкретной квартиры можно проверить в&nbsp;отдельном отчёте.</div>')

SLIDES = [S1, S2, S3, S4, S5, S6]

if __name__ == '__main__':
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        for k, html in enumerate(SLIDES, 1):
            render(html, HERE / f'{k:02d}.jpg', pg)
        b.close()
    print('ok')
