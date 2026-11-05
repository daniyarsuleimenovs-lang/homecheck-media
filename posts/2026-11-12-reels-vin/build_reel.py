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
    (11.15, 13.12, 'Нашли квартиру в объявлении —'),
    (13.12, 15.42, 'введите её адрес на HomeCheck'),
    (15.42, 18.30, 'Увидите, когда и сколько раз её продавали,'),
    (18.30, 20.10, 'и сделки в этом доме'),
    (20.10, 23.70, 'HomeCheck сравнит её с похожими квартирами в том же доме'),
    (23.70, 26.15, 'и подскажет, о чём спросить продавца'),
    (26.15, DUR, 'Проверьте квартиру, как проверяете машину'),
]

CAR = '''<svg viewBox="0 0 520 240" width="520" height="240">
<rect x="20" y="120" width="480" height="80" rx="34" fill="#2D8CFF"/>
<path d="M120 124 L175 52 Q185 40 200 40 L330 40 Q345 40 356 52 L420 124 Z" fill="#2D8CFF"/>
<path d="M150 120 L190 64 L258 64 L258 120 Z M276 120 L276 64 L338 64 L385 120 Z" fill="#DDEEFF"/>
<rect x="30" y="150" width="40" height="18" rx="6" fill="#FFC94D"/>
<rect x="450" y="150" width="40" height="18" rx="6" fill="#FF8A7A"/>
<circle cx="130" cy="200" r="38" fill="#0B2545"/><circle cx="130" cy="200" r="16" fill="#8EC2FA"/>
<circle cx="390" cy="200" r="38" fill="#0B2545"/><circle cx="390" cy="200" r="16" fill="#8EC2FA"/>
</svg>'''


def building(w=360, floors=8, cols=4, hi=None):
    fh, pad = 62, 26
    h = floors * fh + 40
    cw = (w - 2 * pad) / cols
    s = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
         f'<rect x="0" y="16" width="{w}" height="{h-16}" fill="#FFFFFF"/>',
         f'<rect x="-8" y="4" width="{w+16}" height="18" rx="5" fill="#2D8CFF"/>']
    for r in range(floors):
        for c in range(cols):
            x, y = pad + c * cw + 8, 40 + r * fh
            col = '#FFC94D' if hi == (r, c) else ('#FFC94D' if (r * 7 + c * 3) % 11 == 0 else '#8EC2FA')
            s.append(f'<rect x="{x:.0f}" y="{y}" width="{cw-16:.0f}" height="40" rx="4" fill="{col}"/>')
    s.append('</svg>')
    return ''.join(s)


CHECK = '<svg viewBox="0 0 24 24" width="44" height="44"><circle cx="12" cy="12" r="12" fill="#2D8CFF"/><path d="M6.5 12.5 L10.5 16 L17.5 8.5" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PIN = '<svg viewBox="0 0 24 24" width="48" height="48"><path d="M12 2 C7.6 2 4.5 5.3 4.5 9.4 C4.5 14.6 12 22 12 22 C12 22 19.5 14.6 19.5 9.4 C19.5 5.3 16.4 2 12 2Z" fill="#2D8CFF"/><circle cx="12" cy="9.4" r="3" fill="#fff"/></svg>'

HTML = f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>
@font-face{{font-family:'Barlow Condensed';font-weight:700;src:url(data:font/ttf;base64,{FONT})}}
*{{box-sizing:border-box}} body{{margin:0}}
#s{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#BBD6F2;font-family:Inter,sans-serif;color:#0B2545}}
.logo{{position:absolute;left:80px;top:300px;font-family:'Barlow Condensed';font-size:72px;font-weight:700;line-height:1}}
.logo .h{{color:#12253E}} .logo .c{{color:#049BE1}}
.sc{{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0}}
.card{{position:absolute;background:#fff;border-radius:28px;box-shadow:0 18px 40px rgba(11,37,69,.16);padding:34px 40px}}
.ct{{font-size:44px;font-weight:800;margin:0 0 18px}}
.row{{display:flex;align-items:center;gap:20px;font-size:40px;margin:14px 0}}
.lb{{font-size:30px;color:#2F4566}}
.ex{{position:absolute;right:120px;top:312px;font-size:30px;font-weight:700;color:#2F4566;background:#fff;border-radius:999px;padding:8px 22px}}
#sub{{position:absolute;left:80px;width:920px;top:1040px;height:200px;display:flex;align-items:flex-end}}
#sub span{{display:inline-block;background:#0B2545;color:#fff;font-size:52px;font-weight:700;line-height:1.25;padding:16px 28px;border-radius:22px}}
.big{{font-size:100px;font-weight:800;line-height:1.05;letter-spacing:-.025em}}
</style></head><body><div id="s">
<span class="logo" id="logo"><span class="h">Home</span><span class="c">Check.kz</span></span>

<div class="sc" id="s1">
  <div id="car" style="position:absolute;left:40px;top:600px;transform-origin:left top">{CAR}</div>
  <div class="card" id="vin" style="left:600px;top:420px;width:400px">
    <p class="ct">История авто</p>
    <div class="row" id="v1">{CHECK}<span>Владельцы</span></div>
    <div class="row" id="v2">{CHECK}<span>Пробег</span></div>
    <div class="row" id="v3">{CHECK}<span>ДТП</span></div>
  </div>
</div>

<div class="sc" id="s2">
  <div id="bld" style="position:absolute;left:360px;top:470px">{building(360, 8, 4)}</div>
  <div id="q" style="position:absolute;left:640px;top:400px;width:190px;height:190px;border-radius:50%;background:#0B2545;color:#fff;font-size:130px;font-weight:800;display:flex;align-items:center;justify-content:center">?</div>
</div>

<div class="sc" id="s3">
  <div class="card" id="c3a" style="left:140px;top:500px;width:800px"><p class="ct">История авто</p><div class="row">{CHECK}<span>Проверено по VIN‑коду</span></div></div>
  <div class="card" id="c3b" style="left:140px;top:500px;width:800px"><p class="ct">История квартиры</p>
    <div class="row">{PIN}<span>Проверка по адресу</span></div></div>
</div>

<div class="sc" id="s4">
  <div id="phone" style="position:absolute;left:90px;top:420px;width:380px;height:600px;background:#0B2545;border-radius:48px;padding:22px">
    <div style="background:#fff;border-radius:30px;height:100%;padding:22px">
      <div style="height:200px;border-radius:18px;background:linear-gradient(#8EC2FA,#DDEEFF)"></div>
      <p style="font-size:34px;font-weight:800;margin:20px 0 8px">2-комн., 52 м²</p>
      <p style="font-size:28px;color:#2F4566;margin:0 0 18px">Объявление</p>
      <div id="addr" style="font-size:30px;background:#EAF3FF;border-radius:14px;padding:14px 16px;display:flex;gap:10px;align-items:center">{PIN.replace('48','34')}<span>Адрес квартиры</span></div>
    </div>
  </div>
  <div id="arrow" style="position:absolute;left:490px;top:690px;font-size:90px;font-weight:800;color:#1768CE">→</div>
  <div class="card" id="field" style="left:590px;top:560px;width:420px;padding:30px">
    <p style="font-family:'Barlow Condensed';font-size:52px;font-weight:700;margin:0 0 20px"><span style="color:#12253E">Home</span><span style="color:#049BE1">Check.kz</span></p>
    <div style="border:3px solid #2D8CFF;border-radius:16px;padding:18px 16px;font-size:28px;min-height:80px;white-space:nowrap;overflow:hidden"><span id="typed"></span><span id="caret" style="color:#2D8CFF">|</span></div>
  </div>
</div>

<div class="sc" id="s5">
  <span class="ex">Пример</span>
  <div class="card" id="h1" style="left:100px;top:440px;width:880px">
    <p class="ct">История квартиры</p>
    <div class="row"><span style="font-size:64px;font-weight:800;color:#1768CE">2 раза</span><span class="lb">продавали</span></div>
    <div style="display:flex;align-items:center;gap:0;margin-top:14px">
      <div style="width:26px;height:26px;border-radius:50%;background:#2D8CFF"></div><div style="flex:1;height:6px;background:#8EC2FA"></div>
      <div style="width:26px;height:26px;border-radius:50%;background:#2D8CFF"></div><div style="flex:1;height:6px;background:#8EC2FA"></div>
      <div style="width:26px;height:26px;border-radius:50%;background:#FFC94D"></div></div>
  </div>
  <div class="card" id="h2" style="left:100px;top:790px;width:880px">
    <div class="row" style="margin:0"><span style="font-size:64px;font-weight:800;color:#1768CE">63</span><span style="font-size:40px">сделки в доме</span></div>
  </div>
</div>

<div class="sc" id="s6">
  <span class="ex">Пример</span>
  <div class="card" id="k1" style="left:100px;top:420px;width:880px">
    <p class="ct">Похожие квартиры в доме</p>
    <div style="display:flex;gap:16px;align-items:flex-end;height:120px">
      <div style="flex:1;height:70%;background:#8EC2FA;border-radius:10px"></div><div style="flex:1;height:85%;background:#8EC2FA;border-radius:10px"></div>
      <div style="flex:1;height:100%;background:#2D8CFF;border-radius:10px"></div><div style="flex:1;height:78%;background:#8EC2FA;border-radius:10px"></div>
      <div style="flex:1;height:90%;background:#8EC2FA;border-radius:10px"></div></div>
  </div>
  <div class="card" id="k2" style="left:100px;top:720px;width:880px">
    <p class="ct">О чём спросить продавца</p>
    <div class="row" id="q1" style="font-size:36px"><span style="color:#2D8CFF;font-weight:800">?</span><span>Почему продаёте через год после покупки?</span></div>
    <div class="row" id="q2" style="font-size:36px"><span style="color:#2D8CFF;font-weight:800">?</span><span>Почему в доме часто перепродают?</span></div>
  </div>
</div>

<div class="sc" id="s7">
  <div style="position:absolute;left:80px;top:470px;width:920px">
    <p class="big" style="margin:0 0 40px">Проверьте квартиру до покупки</p>
    <p style="font-size:64px;font-weight:800;color:#1768CE;margin:0">homecheck.kz</p>
  </div>
</div>

<img id="sky" src="SKYLINE" style="position:absolute;left:0;bottom:0;width:1080px;height:640px">
<div id="sub"><span id="subt"></span></div>
</div>
<script>
const SC={SCENES}, SUBS={[list(s) for s in SUBS]};
const cl=x=>Math.max(0,Math.min(1,x)), ease=x=>{{x=cl(x);return x*x*(3-2*x)}};
const seg=(t,a,b)=>ease((t-a)/(b-a));
const $=id=>document.getElementById(id);
function op(el,v){{el.style.opacity=v}}
function tr(el,s){{el.style.transform=s}}
function setT(t){{
  for(let i=1;i<=7;i++){{const a=SC[i-1],b=SC[i];const fi=i==1?1:seg(t,a-0.15,a+0.2),fo=i==7?1:1-seg(t,b-0.2,b+0.15);op($('s'+i),Math.min(fi,fo))}}
  // S1: car drives in, checks appear
  tr($('car'),`translateX(${{-600*(1-seg(t,0,0.8))}}px)`);
  op($('vin'),seg(t,0.4,0.9)); ['v1','v2','v3'].forEach((id,k)=>op($(id),seg(t,1.0+k*0.55,1.3+k*0.55)));
  // S2: building rises, question mark pops
  tr($('bld'),`translateY(${{120*(1-seg(t,3.6,4.4))}}px)`); op($('bld'),seg(t,3.6,4.2));
  const p=seg(t,4.6,5.1); tr($('q'),`scale(${{0.4+0.6*p+0.06*Math.sin(t*5)*p}})`); op($('q'),p);
  // S3: car card flips into apartment card
  const f=seg(t,8.0,8.8); tr($('c3a'),`rotateY(${{90*f}}deg)`); op($('c3a'),1-f);
  const g=seg(t,8.8,9.5); tr($('c3b'),`rotateY(${{-90*(1-g)}}deg)`); op($('c3b'),g);
  // S4: phone, address chip flies, typing in HomeCheck field
  op($('phone'),seg(t,11.1,11.6)); op($('arrow'),seg(t,12.4,12.9)); op($('field'),seg(t,12.6,13.2));
  tr($('addr'),`translateX(${{0}}px)`); $('addr').style.background = t>12.4&&t<13.4?'#FFE7A3':'#EAF3FF';
  const txt='Адрес квартиры'; const n=Math.floor(txt.length*cl((t-13.3)/0.9)); $('typed').textContent=txt.slice(0,n);
  op($('caret'),(Math.floor(t*2.5)%2)?1:0.15);
  // S5
  tr($('h1'),`translateY(${{60*(1-seg(t,15.5,16.1))}}px)`); op($('h1'),seg(t,15.5,16.1));
  tr($('h2'),`translateY(${{60*(1-seg(t,18.2,18.8))}}px)`); op($('h2'),seg(t,18.2,18.8));
  // S6
  op($('k1'),seg(t,20.2,20.8)); tr($('k1'),`translateY(${{60*(1-seg(t,20.2,20.8))}}px)`);
  op($('k2'),seg(t,23.5,24.1)); tr($('k2'),`translateY(${{60*(1-seg(t,23.5,24.1))}}px)`);
  op($('q1'),seg(t,24.0,24.4)); op($('q2'),seg(t,24.7,25.1));
  // subtitles
  const s=SUBS.find(x=>t>=x[0]&&t<x[1]); $('subt').textContent=s?s[2]:''; $('sub').style.opacity=s?1:0;
}}
window.setT=setT;
</script></body></html>'''


def skyline(page):
    import render as RR, illustrations as il
    img = RR.svg_to_image(il.city(h=640, seed=9), 1080, 640, page)
    return RR.data_uri(RR.treat(img, 640, **RR.ILLUS))


def cover(page, out, base):
    html = base.replace('<div id="sub">', '<div id="sub" style="display:none">')
    page.set_content(html); page.evaluate('document.fonts.ready')
    page.evaluate('''() => { document.querySelectorAll('.sc').forEach(e => e.style.opacity = 0); document.getElementById('sky').style.display = 'none';
      const c = document.createElement('div');
      c.innerHTML = `<div style="position:absolute;left:80px;top:440px;width:920px">
        <p style="font-size:100px;font-weight:800;line-height:1.05;letter-spacing:-.025em;margin:0">Машину проверяют по VIN. А квартиру?</p></div>`;
      document.getElementById('s').appendChild(c); }''')
    page.evaluate('''() => { const car = document.getElementById('car').cloneNode(true);
      car.style.cssText = 'position:absolute;left:80px;top:1180px;transform:scale(.85);transform-origin:left top';
      const b = document.getElementById('bld').cloneNode(true);
      b.style.cssText = 'position:absolute;left:640px;top:1020px;opacity:1';
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
