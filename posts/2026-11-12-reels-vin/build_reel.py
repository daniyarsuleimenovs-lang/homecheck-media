"""Reels 2026-11-12: «Машину проверяют по VIN. А квартиру?»
Голос — ElevenLabs Rina (voice_raw.mp3, 29,1 с, текст — voice.txt). Анимация кодом под паузы голоса,
субтитры вшиты, 1080x1920, 30 fps. Безопасные зоны Reels: текст и важное — y 270..1248, x 65..1015.
Запуск: python3 build_reel.py  -> reel.mp4, cover.jpg
"""
import base64, pathlib, subprocess, shutil, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
TPL = HERE.parents[1] / 'templates'
FONT = base64.b64encode((TPL / 'fonts' / 'BarlowCondensed-Bold.ttf').read_bytes()).decode()
FPS, DUR = 30, 29.9
sys.path.insert(0, str(TPL))
FRAMES = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / '_frames'

# Scenes follow the voice (silences detected with ffmpeg silencedetect).
SCENES = [0.0, 3.72, 7.43, 11.15, 15.42, 20.10, 26.15, DUR]
SUBS = [
    (0.00, 3.72, 'Перед покупкой машины проверяют её историю по VIN\u2011коду'),
    (3.72, 7.43, 'А квартиру за десятки миллионов часто берут вслепую'),
    (7.43, 11.15, 'Теперь квартиру тоже можно проверить — по адресу'),
    (11.15, 13.12, 'Нашли квартиру в объявлении'),
    (13.12, 15.42, 'введите её адрес на HomeCheck'),
    (15.42, 18.30, 'Увидите, когда и сколько раз её продавали,'),
    (18.30, 20.10, 'и сделки в этом доме'),
    (20.10, 23.70, 'HomeCheck сравнит её с похожими квартирами в том же доме'),
    (23.70, 26.15, 'и подскажет, о чём спросить продавца'),
    (26.15, DUR, 'Проверьте квартиру, как проверяете машину'),
]

def CAR():
    return """<svg viewBox="0 0 560 270" width="500" height="241">
<defs>
 <linearGradient id="cb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5AB0FF"/><stop offset="1" stop-color="#1768CE"/></linearGradient>
 <linearGradient id="cw" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F2F8FF"/><stop offset="1" stop-color="#9CCBFA"/></linearGradient>
 <radialGradient id="hl"><stop offset="0" stop-color="#FFE7A3"/><stop offset="1" stop-color="#FFE7A3" stop-opacity="0"/></radialGradient>
</defs>
<ellipse cx="280" cy="250" rx="250" ry="16" fill="#0B2545" opacity=".18"/>
<path d="M40 150 Q40 120 80 116 L150 110 L210 46 Q222 34 240 34 L360 34 Q380 34 394 48 L456 112 L500 118 Q530 124 530 156 L530 196 Q530 214 512 214 L58 214 Q40 214 40 196 Z" fill="url(#cb)"/>
<path d="M176 110 L222 56 Q228 50 238 50 L292 50 L292 110 Z" fill="url(#cw)"/>
<path d="M308 110 L308 50 L356 50 Q368 50 376 58 L424 110 Z" fill="url(#cw)"/>
<path d="M200 106 L236 58 L252 58 L214 106 Z" fill="#fff" opacity=".55"/>
<line x1="300" y1="116" x2="300" y2="200" stroke="#0F4FA8" stroke-width="3" opacity=".5"/>
<rect x="250" y="130" width="34" height="8" rx="4" fill="#0F4FA8" opacity=".6"/><rect x="330" y="130" width="34" height="8" rx="4" fill="#0F4FA8" opacity=".6"/>
<path d="M60 128 L520 128" stroke="#fff" stroke-width="4" opacity=".35"/>
<circle cx="520" cy="160" r="40" fill="url(#hl)"/>
<rect x="500" y="148" width="26" height="20" rx="6" fill="#FFD36B"/>
<rect x="40" y="150" width="20" height="22" rx="5" fill="#FF8A7A"/>
<g id="w1"><circle cx="140" cy="214" r="40" fill="#0B2545"/><circle cx="140" cy="214" r="22" fill="#CFE3F8"/><circle cx="140" cy="214" r="7" fill="#0B2545"/>
 <rect x="137" y="194" width="6" height="40" fill="#0B2545" opacity=".5" class="spoke"/></g>
<g id="w2"><circle cx="420" cy="214" r="40" fill="#0B2545"/><circle cx="420" cy="214" r="22" fill="#CFE3F8"/><circle cx="420" cy="214" r="7" fill="#0B2545"/>
 <rect x="417" y="194" width="6" height="40" fill="#0B2545" opacity=".5" class="spoke"/></g>
</svg>"""


def building(w=360, floors=8, cols=4, hi=None, uid='b', trees=True):
    """Volumetric building: lit front, shaded side, glass windows, warm lights, trees, shadow."""
    fh, pad, side = 64, 26, int(w * 0.22)
    h = floors * fh + 60
    W, H = w + side + 120, h + 70
    x0 = 60
    cw = (w - 2 * pad) / cols
    s = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}"><defs>',
         f'<linearGradient id="{uid}f" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#E6F0FC"/></linearGradient>',
         f'<linearGradient id="{uid}s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A9CCF2"/><stop offset="1" stop-color="#7FAEE3"/></linearGradient>',
         f'<linearGradient id="{uid}g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#CFE6FF"/><stop offset="1" stop-color="#6FAEF5"/></linearGradient>',
         f'<linearGradient id="{uid}y" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE59A"/><stop offset="1" stop-color="#FFB938"/></linearGradient>',
         f'<radialGradient id="{uid}t"><stop offset="0" stop-color="#7FD3A8"/><stop offset="1" stop-color="#3E9C70"/></radialGradient></defs>',
         f'<ellipse cx="{x0 + (w + side) / 2}" cy="{H - 22}" rx="{(w + side) / 2 + 40}" ry="20" fill="#0B2545" opacity=".14"/>',
         f'<path d="M{x0 + w} 30 L{x0 + w + side} 46 L{x0 + w + side} {h + 16} L{x0 + w} {h} Z" fill="url(#{uid}s)"/>',
         f'<rect x="{x0}" y="30" width="{w}" height="{h - 30}" fill="url(#{uid}f)"/>',
         f'<path d="M{x0 - 10} 18 L{x0 + w + 6} 18 L{x0 + w + side + 6} 34 L{x0 + w + side} 48 L{x0 + w} 34 L{x0 - 10} 34 Z" fill="#2D8CFF"/>']
    for r in range(floors):
        for c in range(cols):
            x, y = x0 + pad + c * cw + 8, 56 + r * fh
            lit = hi == (r, c) or (r * 7 + c * 3) % 11 == 0
            fill = f'url(#{uid}y)' if lit else f'url(#{uid}g)'
            if hi == (r, c):
                s.append(f'<rect x="{x - 10:.0f}" y="{y - 10}" width="{cw - 16 + 20:.0f}" height="62" rx="10" fill="#FFD36B" opacity=".45"/>')
            s.append(f'<rect x="{x:.0f}" y="{y}" width="{cw - 16:.0f}" height="42" rx="5" fill="{fill}"/>')
            s.append(f'<rect x="{x:.0f}" y="{y}" width="{(cw - 16) * .35:.0f}" height="42" rx="5" fill="#fff" opacity=".25"/>')
        s.append(f'<rect x="{x0}" y="{56 + r * fh + 48}" width="{w}" height="6" fill="#D5E6FA"/>')
        for k in range(3):
            s.append(f'<rect x="{x0 + w + 10 + k * side * .3:.0f}" y="{60 + r * fh + k * 2}" width="{side * .18:.0f}" height="36" rx="4" fill="#5F93D4" opacity=".7"/>')
    s.append(f'<rect x="{x0 + w / 2 - 34}" y="{h - 70}" width="68" height="70" rx="6" fill="#1F4E8C"/>')
    if trees:
        for tx, th in [(x0 - 20, 150), (x0 + w + side + 20, 130)]:
            s.append(f'<rect x="{tx - 5}" y="{h - th * .35}" width="10" height="{th * .35 + 16}" rx="5" fill="#2F5E3F"/>')
            s.append(f'<ellipse cx="{tx}" cy="{h - th * .6}" rx="{th * .26}" ry="{th * .36}" fill="url(#{uid}t)"/>')
    s.append('</svg>')
    return ''.join(s)


def icon(kind, size=64):
    g = ('<svg viewBox="0 0 64 64" width="%d" height="%d"><defs><linearGradient id="ig%s" x1="0" y1="0" x2="1" y2="1">'
         '<stop offset="0" stop-color="#5AB0FF"/><stop offset="1" stop-color="#1768CE"/></linearGradient></defs>'
         '<rect width="64" height="64" rx="18" fill="url(#ig%s)"/>') % (size, size, kind, kind)
    body = {
        'car': '<path d="M14 38 L18 28 Q20 24 24 24 L40 24 Q44 24 46 28 L50 38 Z" fill="#fff"/><rect x="12" y="36" width="40" height="10" rx="4" fill="#fff"/><circle cx="22" cy="47" r="4" fill="#1768CE"/><circle cx="42" cy="47" r="4" fill="#1768CE"/>',
        'home': '<path d="M14 32 L32 17 L50 32 L50 48 L14 48 Z" fill="#fff"/><rect x="28" y="36" width="8" height="12" fill="#1768CE"/>',
        'pin': '<path d="M32 14 C24.5 14 19 19.6 19 26.6 C19 35.5 32 50 32 50 C32 50 45 35.5 45 26.6 C45 19.6 39.5 14 32 14Z" fill="#fff"/><circle cx="32" cy="26.6" r="5" fill="#1768CE"/>',
        'chart': '<rect x="16" y="34" width="7" height="14" rx="2" fill="#fff"/><rect x="28" y="26" width="7" height="22" rx="2" fill="#fff"/><rect x="40" y="18" width="7" height="30" rx="2" fill="#FFD36B"/>',
        'chat': '<path d="M14 18 H50 Q52 18 52 20 V40 Q52 42 50 42 H28 L20 49 V42 H14 Q12 42 12 40 V20 Q12 18 14 18Z" fill="#fff"/><circle cx="24" cy="30" r="3" fill="#1768CE"/><circle cx="32" cy="30" r="3" fill="#1768CE"/><circle cx="40" cy="30" r="3" fill="#1768CE"/>',
    }[kind]
    return g + body + '</svg>'


CHECK = '<svg viewBox="0 0 24 24" width="44" height="44"><circle cx="12" cy="12" r="12" fill="#2DB57A"/><path d="M6.5 12.5 L10.5 16 L17.5 8.5" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
MAG = '<svg viewBox="0 0 120 120" width="150" height="150"><circle cx="50" cy="50" r="36" fill="#fff" fill-opacity=".35" stroke="#0B2545" stroke-width="12"/><line x1="76" y1="76" x2="108" y2="108" stroke="#0B2545" stroke-width="16" stroke-linecap="round"/><path d="M30 38 Q36 26 50 24" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round"/></svg>'

HTML = f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>
@font-face{{font-family:'Barlow Condensed';font-weight:700;src:url(data:font/ttf;base64,{FONT})}}
*{{box-sizing:border-box}} body{{margin:0}}
#s{{position:relative;width:1080px;height:1920px;overflow:hidden;background:linear-gradient(180deg,#D7E9FC 0%,#BBD6F2 48%,#A9CCF2 100%);font-family:Inter,sans-serif;color:#0B2545}}
.glow{{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,.75),rgba(255,255,255,0) 70%)}}
.logo{{position:absolute;left:80px;top:300px;font-family:'Barlow Condensed';font-size:72px;font-weight:700;line-height:1}}
.logo .h{{color:#12253E}} .logo .c{{color:#049BE1}}
.sc{{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0}}
.card{{position:absolute;background:linear-gradient(180deg,#FFFFFF 0%,#F6FAFF 100%);border:1.5px solid rgba(45,140,255,.14);border-radius:34px;box-shadow:0 26px 60px rgba(11,37,69,.18),0 4px 10px rgba(11,37,69,.06);padding:34px 40px}}
.hd{{display:flex;align-items:center;gap:20px;margin:0 0 20px}}
.ct{{font-size:44px;font-weight:800;margin:0;white-space:nowrap}}
.row{{display:flex;align-items:center;gap:20px;font-size:40px;margin:16px 0}}
.lb{{font-size:30px;color:#2F4566}}
.ex{{position:absolute;right:80px;top:312px;font-size:30px;font-weight:700;color:#2F4566;background:rgba(255,255,255,.85);border-radius:999px;padding:8px 22px}}
#sub{{position:absolute;left:80px;width:920px;top:1040px;height:200px;display:flex;align-items:flex-end}}
#sub span{{display:inline-block;background:rgba(11,37,69,.92);color:#fff;font-size:52px;font-weight:700;line-height:1.25;padding:16px 28px;border-radius:22px;box-shadow:0 12px 30px rgba(11,37,69,.25)}}
.big{{font-size:100px;font-weight:800;line-height:1.05;letter-spacing:-.025em}}
.bubble{{position:absolute;background:#fff;border-radius:26px;padding:18px 26px;font-size:34px;box-shadow:0 14px 30px rgba(11,37,69,.14)}}
</style></head><body><div id="s">
<div class="glow" id="g1" style="left:-200px;top:200px;width:800px;height:800px"></div>
<div class="glow" id="g2" style="left:600px;top:700px;width:700px;height:700px;opacity:.7"></div>
<img id="sky" src="SKYLINE" style="position:absolute;left:0;bottom:0;width:1080px;height:640px">
<span class="logo" id="logo"><span class="h">Home</span><span class="c">Check.kz</span></span>

<div class="sc" id="s1">
  <div id="car" style="position:absolute;left:20px;top:660px">{CAR()}</div>
  <div class="card" id="vin" style="left:540px;top:420px;width:475px;padding:34px 34px">
    <div class="hd">{icon('car', 60)}<p class="ct">История авто</p></div>
    <div class="row" id="v1">{CHECK}<span>Владельцы</span></div>
    <div class="row" id="v2">{CHECK}<span>Пробег</span></div>
    <div class="row" id="v3">{CHECK}<span>ДТП</span></div>
  </div>
</div>

<div class="sc" id="s2">
  <div id="bld" style="position:absolute;left:250px;top:440px">{building(380, 8, 4, uid='b2')}</div>
  <div id="q" style="position:absolute;left:690px;top:390px">
    <svg viewBox="0 0 220 220" width="220" height="220"><path d="M110 10 C170 10 210 48 210 100 C210 152 170 190 110 190 C96 190 84 188 72 184 L30 208 L42 168 C22 150 10 126 10 100 C10 48 50 10 110 10Z" fill="#0B2545"/>
    <text x="110" y="140" text-anchor="middle" font-family="Inter" font-weight="800" font-size="120" fill="#FFD36B">?</text></svg></div>
</div>

<div class="sc" id="s3">
  <div class="card" id="c3a" style="left:120px;top:500px;width:840px"><div class="hd">{icon('car', 72)}<p class="ct">История авто</p></div>
    <div class="row">{CHECK}<span>Проверено по VIN&#8209;коду</span></div></div>
  <div class="card" id="c3b" style="left:120px;top:500px;width:840px"><div class="hd">{icon('home', 72)}<p class="ct">История квартиры</p></div>
    <div class="row">{icon('pin', 44)}<span>Проверка по адресу</span></div></div>
  <div id="mag3" style="position:absolute;left:760px;top:690px">{MAG}</div>
</div>

<div class="sc" id="s4">
  <div id="phone" style="position:absolute;left:80px;top:410px;width:400px;height:640px;background:linear-gradient(160deg,#1F4E8C,#0B2545);border-radius:56px;padding:20px;box-shadow:0 30px 60px rgba(11,37,69,.3)">
    <div style="background:#fff;border-radius:38px;height:100%;padding:22px;position:relative;overflow:hidden">
      <div style="position:absolute;left:50%;top:10px;width:110px;height:24px;margin-left:-55px;background:#0B2545;border-radius:12px"></div>
      <div style="margin-top:30px;height:230px;border-radius:22px;background:linear-gradient(180deg,#D7E9FC,#A9CCF2);overflow:hidden;display:flex;justify-content:center;align-items:flex-end">{building(150, 4, 3, uid='b4', trees=False)}</div>
      <p style="font-size:34px;font-weight:800;margin:20px 0 6px">2-комн., 52 м²</p>
      <p style="font-size:28px;color:#2F4566;margin:0 0 18px">Объявление</p>
      <div id="addr" style="font-size:28px;background:#EAF3FF;border-radius:16px;padding:12px 14px;display:flex;gap:10px;align-items:center">{icon('pin', 40)}<span>Адрес квартиры</span></div>
    </div>
  </div>
  <div id="chip" style="position:absolute;left:110px;top:900px;font-size:28px;background:#FFE7A3;border-radius:16px;padding:12px 16px;display:flex;gap:10px;align-items:center;box-shadow:0 12px 26px rgba(11,37,69,.2);opacity:0">{icon('pin', 40)}<span>Адрес квартиры</span></div>
  <div class="card" id="field" style="left:560px;top:560px;width:460px;padding:30px">
    <p style="font-family:'Barlow Condensed';font-size:56px;font-weight:700;margin:0 0 20px"><span style="color:#12253E">Home</span><span style="color:#049BE1">Check.kz</span></p>
    <div style="border:3px solid #2D8CFF;border-radius:18px;padding:18px 16px;font-size:30px;min-height:84px;white-space:nowrap;overflow:hidden;background:#F6FAFF"><span id="typed"></span><span id="caret" style="color:#2D8CFF">|</span></div>
  </div>
</div>

<div class="sc" id="s5">
  <span class="ex">Пример</span>
  <div class="card" id="h1" style="left:80px;top:430px;width:920px">
    <div class="hd">{icon('home', 64)}<p class="ct">История квартиры</p></div>
    <div class="row"><span style="font-size:72px;font-weight:800;color:#1768CE">2 раза</span><span class="lb" style="font-size:36px">продавали</span></div>
    <div style="display:flex;align-items:center;margin-top:18px">
      <div class="dot" style="width:34px;height:34px;border-radius:50%;background:#2D8CFF;box-shadow:0 0 0 8px rgba(45,140,255,.18)"></div><div style="flex:1;height:8px;border-radius:4px;background:linear-gradient(90deg,#2D8CFF,#8EC2FA)"></div>
      <div style="width:34px;height:34px;border-radius:50%;background:#2D8CFF;box-shadow:0 0 0 8px rgba(45,140,255,.18)"></div><div style="flex:1;height:8px;border-radius:4px;background:linear-gradient(90deg,#8EC2FA,#FFD36B)"></div>
      <div style="width:34px;height:34px;border-radius:50%;background:#FFC94D;box-shadow:0 0 0 8px rgba(255,201,77,.25)"></div></div>
    <div style="display:flex;justify-content:space-between;font-size:28px;color:#2F4566;margin-top:14px"><span>Продажа</span><span>Продажа</span><span>Сейчас</span></div>
  </div>
  <div class="card" id="h2" style="left:80px;top:860px;width:920px;padding:28px 40px">
    <div class="row" style="margin:0">{icon('chart', 64)}<span style="font-size:72px;font-weight:800;color:#1768CE">63</span><span style="font-size:40px">сделки в доме</span></div>
  </div>
</div>

<div class="sc" id="s6">
  <span class="ex">Пример</span>
  <div class="card" id="k1" style="left:80px;top:410px;width:920px">
    <div class="hd">{icon('chart', 60)}<p class="ct">Похожие квартиры в доме</p></div>
    <div style="display:flex;gap:18px;align-items:flex-end;height:130px">
      <div class="bar" style="flex:1;height:62%;background:linear-gradient(#B9D9FB,#8EC2FA);border-radius:12px"></div><div class="bar" style="flex:1;height:80%;background:linear-gradient(#B9D9FB,#8EC2FA);border-radius:12px"></div>
      <div class="bar" style="flex:1;height:100%;background:linear-gradient(#5AB0FF,#1768CE);border-radius:12px;box-shadow:0 0 0 6px rgba(45,140,255,.18)"></div><div class="bar" style="flex:1;height:72%;background:linear-gradient(#B9D9FB,#8EC2FA);border-radius:12px"></div>
      <div class="bar" style="flex:1;height:88%;background:linear-gradient(#B9D9FB,#8EC2FA);border-radius:12px"></div></div>
  </div>
  <div class="card" id="k2" style="left:80px;top:720px;width:920px;background:linear-gradient(180deg,#FFFFFF,#FFF8E6)">
    <div class="hd">{icon('chat', 60)}<p class="ct">О чём спросить продавца</p></div>
    <div class="row" id="q1" style="font-size:36px;background:#EAF3FF;border-radius:20px;padding:14px 20px;margin:12px 0">Почему продаёте через год после покупки?</div>
    <div class="row" id="q2" style="font-size:36px;background:#EAF3FF;border-radius:20px;padding:14px 20px;margin:12px 0">Почему в доме часто перепродают?</div>
  </div>
</div>

<div class="sc" id="s7">
  <div style="position:absolute;left:80px;top:470px;width:720px">
    <p class="big" style="margin:0 0 36px">Проверьте квартиру до покупки</p>
    <p style="font-size:64px;font-weight:800;color:#1768CE;margin:0">homecheck.kz</p>
  </div>
  <div id="fb" style="position:absolute;left:700px;top:560px;transform-origin:center bottom">{building(200, 6, 3, hi=(2, 1), uid='b7', trees=False)}</div>
  <div id="mag7" style="position:absolute;left:740px;top:640px">{MAG}</div>
</div>

<div id="sub"><span id="subt"></span></div>
</div>
<script>
const SC={SCENES}, SUBS={[list(s) for s in SUBS]};
const cl=x=>Math.max(0,Math.min(1,x)), ease=x=>{{x=cl(x);return x*x*(3-2*x)}};
const back=x=>{{x=cl(x);const c=1.6;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)}};
const seg=(t,a,b)=>ease((t-a)/(b-a)), pop=(t,a,b)=>back((t-a)/(b-a));
const $=id=>document.getElementById(id);
function op(el,v){{el.style.opacity=v}}
function tr(el,s){{el.style.transform=s}}
function setT(t){{
  for(let i=1;i<=7;i++){{const a=SC[i-1],b=SC[i];const fi=i==1?1:seg(t,a-0.15,a+0.2),fo=i==7?1:1-seg(t,b-0.2,b+0.15);op($('s'+i),Math.min(fi,fo))}}
  tr($('g1'),`translate(${{40*Math.sin(t*.35)}}px,${{30*Math.cos(t*.3)}}px)`); tr($('g2'),`translate(${{-40*Math.sin(t*.3)}}px,${{25*Math.sin(t*.4)}}px)`);
  tr($('sky'),`translateX(${{-8*t}}px) scale(1.05)`);
  // S1
  const d=seg(t,0,0.9); tr($('car'),`translateX(${{-640*(1-d)}}px) translateY(${{3*Math.sin(t*18)*(1-d)}}px)`);
  document.querySelectorAll('#car .spoke').forEach((e,k)=>{{const cx=k?420:140;e.setAttribute('transform',`rotate(${{-720*d}} ${{cx}} 214)`)}});
  op($('vin'),seg(t,0.5,1.0)); tr($('vin'),`scale(${{pop(t,0.5,1.0)*0.15+0.85}})`);
  ['v1','v2','v3'].forEach((id,k)=>{{op($(id),seg(t,1.1+k*0.5,1.4+k*0.5)); tr($(id),`translateX(${{30*(1-seg(t,1.1+k*0.5,1.4+k*0.5))}}px)`)}});
  // S2
  tr($('bld'),`translateY(${{140*(1-seg(t,3.6,4.5))}}px)`); op($('bld'),seg(t,3.6,4.2));
  const p=pop(t,4.6,5.2); tr($('q'),`scale(${{Math.max(0,p)}}) rotate(${{4*Math.sin(t*3)}}deg)`); op($('q'),cl((t-4.6)/0.2));
  // S3
  const f=seg(t,8.0,8.7); tr($('c3a'),`perspective(1200px) rotateY(${{90*f}}deg)`); op($('c3a'),f<1?1:0);
  const g=seg(t,8.7,9.4); tr($('c3b'),`perspective(1200px) rotateY(${{-90*(1-g)}}deg)`); op($('c3b'),g>0?1:0);
  op($('mag3'),seg(t,9.4,9.8)); tr($('mag3'),`translate(${{-60*seg(t,9.4,10.8)}}px,${{-20*Math.sin(t*2)}}px)`);
  // S4
  op($('phone'),seg(t,11.1,11.6)); tr($('phone'),`translateY(${{60*(1-seg(t,11.1,11.7))}}px)`);
  op($('field'),seg(t,12.3,12.8)); tr($('field'),`scale(${{0.85+0.15*pop(t,12.3,12.9)}})`);
  const m=seg(t,12.6,13.4); op($('chip'),t>12.5&&t<13.5?1:0);
  tr($('chip'),`translate(${{m*520}}px,${{-m*240 - 120*Math.sin(m*Math.PI)}}px) scale(${{1-0.15*m}})`);
  const txt='Адрес квартиры'; const n=Math.floor(txt.length*cl((t-13.4)/0.8)); $('typed').textContent=txt.slice(0,n);
  op($('caret'),(Math.floor(t*2.5)%2)?1:0.15);
  // S5
  tr($('h1'),`translateY(${{70*(1-seg(t,15.5,16.1))}}px)`); op($('h1'),seg(t,15.5,16.1));
  tr($('h2'),`translateY(${{70*(1-seg(t,18.2,18.8))}}px)`); op($('h2'),seg(t,18.2,18.8));
  // S6
  op($('k1'),seg(t,20.2,20.8)); tr($('k1'),`translateY(${{70*(1-seg(t,20.2,20.8))}}px)`);
  document.querySelectorAll('#k1 .bar').forEach((e,k)=>tr(e,`scaleY(${{seg(t,20.5+k*0.12,21.0+k*0.12)}})`));
  document.querySelectorAll('#k1 .bar').forEach(e=>e.style.transformOrigin='bottom');
  op($('k2'),seg(t,23.5,24.1)); tr($('k2'),`translateY(${{70*(1-seg(t,23.5,24.1))}}px)`);
  op($('q1'),seg(t,24.0,24.4)); tr($('q1'),`translateX(${{40*(1-seg(t,24.0,24.4))}}px)`);
  op($('q2'),seg(t,24.7,25.1)); tr($('q2'),`translateX(${{40*(1-seg(t,24.7,25.1))}}px)`);
  // S7
  tr($('fb'),`scale(${{0.9+0.1*pop(t,26.3,27.0)}})`);
  op($('mag7'),seg(t,26.9,27.3)); tr($('mag7'),`translate(${{20*Math.sin(t*1.6)}}px,${{12*Math.cos(t*1.6)}}px)`);
  const s=SUBS.find(x=>t>=x[0]&&t<x[1]); $('subt').textContent=s?s[2]:''; $('sub').style.opacity=s?1:0;
}}
window.setT=setT;
</script></body></html>'''


def skyline(page):
    """Bottom city strip with a transparent faded top, so it blends into the gradient background."""
    import io, render as RR, illustrations as il
    from PIL import Image, ImageEnhance
    img = RR.svg_to_image(il.city(h=640, seed=9), 1080, 640, page).convert('RGB')
    img = Image.blend(ImageEnhance.Color(img).enhance(0.9), Image.new('RGB', img.size, (0xA9, 0xCC, 0xF2)), 0.15)
    a = Image.new('L', img.size, 255); px = a.load()
    for y in range(360):
        k = y / 360; v = int(255 * k * k * (3 - 2 * k))
        for x in range(1080): px[x, y] = v
    img.putalpha(a)
    buf = io.BytesIO(); img.save(buf, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()


def cover(page, out, base):
    html = base.replace('<div id="sub">', '<div id="sub" style="display:none">')
    page.set_content(html); page.evaluate('document.fonts.ready')
    page.evaluate('''() => { document.querySelectorAll('.sc').forEach(e => e.style.opacity = 0); 
      const c = document.createElement('div');
      c.innerHTML = `<div style="position:absolute;left:80px;top:440px;width:920px">
        <p style="font-size:100px;font-weight:800;line-height:1.05;letter-spacing:-.025em;margin:0">Машину проверяют по VIN. А квартиру?</p></div>`;
      document.getElementById('s').appendChild(c); }''')
    page.evaluate('''() => { const car = document.getElementById('car').cloneNode(true);
      car.style.cssText = 'position:absolute;left:40px;top:1240px;transform:scale(.8);transform-origin:left top';
      const b = document.getElementById('bld').cloneNode(true);
      b.style.cssText = 'position:absolute;left:520px;top:900px;opacity:1;transform:scale(.9);transform-origin:left top';
      document.getElementById('s').append(car, b); }''')
    page.screenshot(path=str(out), type='jpeg', quality=92)


if __name__ == '__main__':
    if FRAMES.exists(): shutil.rmtree(FRAMES)
    FRAMES.mkdir(parents=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        HTML_ = HTML.replace('SKYLINE', skyline(pg))
        pg.set_viewport_size({'width': 1080, 'height': 1920})
        pg.set_content(HTML_); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(200)
        n = round(DUR * FPS)
        for i in range(n):
            pg.evaluate(f'setT({i / FPS:.4f})')
            pg.screenshot(path=str(FRAMES / f'{i:04d}.png'))
        cover(pg, HERE / 'cover.jpg', HTML_)
        b.close()
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(FRAMES / '%04d.png'),
                    '-i', str(HERE / 'voice_raw.mp3'),
                    '-filter_complex', '[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,apad[a]',
                    '-map', '0:v', '-map', '[a]', '-t', str(DUR),
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
                    '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-movflags', '+faststart', str(HERE / 'reel.mp4')], check=True)
    print('ok')
