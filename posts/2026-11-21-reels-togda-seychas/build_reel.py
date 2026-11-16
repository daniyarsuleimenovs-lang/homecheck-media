"""Reels «Тогда и сейчас» (сб 21.11.2026). Без голоса: смысл в надписях, музыка — при публикации или отдельным треком.
Иллюстрации — ChatGPT (команда, 16.11.2026), метка ИИ. 1080x1920, 30 fps.
Сверху «ТОГДА» (родители, начало 2000-х), снизу «СЕЙЧАС» (дочь) — нижняя половина выезжает через секунду.
Текст — только в безопасной зоне Reels (270…1248 px по вертикали)."""
import sys, pathlib, subprocess, shutil
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'templates'))
from playwright.sync_api import sync_playwright
from render import FONT_LOGO_URI, data_uri
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
FPS, DUR = 30, 22.0
HOOK, SC, FIN = 2.2, 4.2, 19.0
img = lambda n: data_uri(Image.open(HERE / 'src' / f'{n}.jpg'))

SCENES = [
    ('t1', '22%', 'Узнавали у&nbsp;соседки, за&nbsp;сколько ушла квартира на&nbsp;третьем',
     's1', '18%', 'Смотрим реальные цены сделок в&nbsp;доме'),
    ('t2', '20%', '«Хозяин был один, всё хорошо» — со&nbsp;слов продавца',
     's2', '45%', 'Видим, сколько раз квартиру продавали'),
    ('t3', '25%', '«Нормальная цена» — сказал дядя, который покупал в&nbsp;2005-м',
     's3', '28%', 'Видим, как менялись цены в&nbsp;доме'),
    ('t4', '18%', 'Чисто в&nbsp;подъезде — значит, дом хороший',
     's4', '35%', 'Знаем, как часто здесь перепродают квартиры и&nbsp;что пишут жильцы'),
]

CSS = f"""
@font-face{{font-family:'Barlow Condensed';font-weight:700;src:url('{FONT_LOGO_URI}')}}
*{{box-sizing:border-box}} body{{margin:0;background:#FBF3E8}}
#v{{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:Inter,sans-serif;background:#FBF3E8}}
.layer{{position:absolute;inset:0;opacity:0}}
.bar{{position:absolute;left:0;width:1080px;height:210px;padding:24px 70px 0}}
.chip{{display:inline-block;border-radius:999px;padding:6px 20px;font-size:28px;font-weight:800;letter-spacing:.08em;color:#fff}}
.cap{{margin-top:12px;font-size:44px;line-height:1.22;font-weight:700}}
.ph{{position:absolute;left:0;width:1080px;overflow:hidden}}
.ph img{{width:1080px;height:1080px;object-fit:cover;transform-origin:50% 30%}}
.then .bar{{background:#EADBC6}} .then .chip{{background:#7A5B45}} .then .cap{{color:#3A2C22}}
.now .bar{{background:#E6F0FC}} .now .chip{{background:#1768CE}} .now .cap{{color:#0B2545}}
.logo{{font-family:'Barlow Condensed';font-weight:700;line-height:1}}
.logo .h{{color:#12253E}} .logo .c{{color:#049BE1}}
"""


def scene(i, t, tp, tc, s, sp, sc):
    return (f'<div class="layer" id="sc{i}">'
            f'<div class="then" id="T{i}" style="position:absolute;left:0;top:0;width:1080px">'
            f'<div class="bar" style="top:240px"><span class="chip">ТОГДА</span><div class="cap">{tc}</div></div>'
            f'<div class="ph" style="top:450px;height:510px"><img id="TI{i}" src="{img(t)}" style="margin-top:calc(-1 * (1080px - 510px) * {float(tp[:-1]) / 100})"></div></div>'
            f'<div class="now" id="S{i}" style="position:absolute;left:0;top:0;width:1080px">'
            f'<div class="bar" style="top:968px"><span class="chip">СЕЙЧАС</span><div class="cap">{sc}</div></div>'
            f'<div class="ph" style="top:1178px;height:742px"><img id="SI{i}" src="{img(s)}" style="margin-top:calc(-1 * (1080px - 742px) * {float(sp[:-1]) / 100})"></div></div>'
            f'</div>')


HTML = (f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div id="v">'
        # hook
        f'<div class="layer" id="hook" style="display:flex;flex-direction:column;justify-content:center;padding:0 80px 300px">'
        f'<div class="logo" style="font-size:64px;margin-bottom:60px"><span class="h">Home</span><span class="c">Check.kz</span></div>'
        f'<div style="font-size:96px;line-height:1.08;font-weight:800;color:#0B2545;letter-spacing:-.025em">Как покупали квартиру <span style="color:#9A6B4C">тогда</span> и&nbsp;как <span style="color:#1768CE">сейчас</span></div></div>'
        + ''.join(scene(i, *s) for i, s in enumerate(SCENES))
        # final
        + f'<div class="layer" id="fin" style="display:flex;flex-direction:column;justify-content:center;padding:0 80px 300px">'
          f'<div style="font-size:84px;line-height:1.12;font-weight:800;color:#0B2545;letter-spacing:-.02em">'
          f'<span style="color:#9A6B4C">Тогда</span> покупали на&nbsp;слово.<br><span style="color:#1768CE">Сейчас</span> — по&nbsp;данным.</div>'
          f'<div class="logo" style="font-size:96px;margin-top:70px"><span class="h">Home</span><span class="c">Check.kz</span></div>'
          f'<div style="font-size:44px;font-weight:700;color:#33465E;margin-top:18px">Проверьте квартиру до&nbsp;покупки</div></div>'
        + '</div><script>'
        f'const HOOK={HOOK},SC={SC},FIN={FIN},DUR={DUR},N={len(SCENES)};'
        """
const cl=(x)=>Math.max(0,Math.min(1,x)); const ease=(x)=>1-Math.pow(1-cl(x),3);
function fade(u,len){ return cl(u/0.3)*cl((len-u)/0.3); }
function setT(t){
  document.getElementById('hook').style.opacity = t<HOOK ? cl((HOOK-t)/0.3)*cl(t/0.2+1) : 0;
  for(let i=0;i<N;i++){
    const s=HOOK+i*SC, u=t-s, el=document.getElementById('sc'+i);
    el.style.opacity = (u>=0 && u<SC) ? fade(u,SC) : 0;
    const a=ease(u/0.45), b=ease((u-0.9)/0.45);
    const T=document.getElementById('T'+i), S=document.getElementById('S'+i);
    T.style.transform=`translateY(${(1-a)*-50}px)`; T.style.opacity=a;
    S.style.transform=`translateY(${(1-b)*120}px)`; S.style.opacity=b;
    const k=1+0.06*cl(u/SC);
    document.getElementById('TI'+i).style.transform=`scale(${k})`;
    document.getElementById('SI'+i).style.transform=`scale(${1+0.06*cl((u-0.9)/SC)})`;
  }
  const f=t-FIN, fe=document.getElementById('fin');
  fe.style.opacity = f>=0 ? cl(f/0.4) : 0; fe.style.transform=`translateY(${(1-ease(f/0.6))*40}px)`;
}
setT(0);
</script></body></html>""")

if __name__ == '__main__':
    fr = HERE / 'frames'
    if fr.exists():
        shutil.rmtree(fr)
    fr.mkdir()
    n = int(DUR * FPS)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.set_content(HTML); pg.wait_for_timeout(300)
        for f in range(n):
            pg.evaluate(f'setT({f / FPS})')
            pg.screenshot(path=str(fr / f'{f:04d}.png'), clip={'x': 0, 'y': 0, 'width': 1080, 'height': 1920})
        pg.evaluate('setT(1.0)'); pg.screenshot(path=str(HERE / 'cover.png'))
        b.close()
    Image.open(HERE / 'cover.png').convert('RGB').save(HERE / 'cover.jpg', quality=92)
    (HERE / 'cover.png').unlink()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', str(fr / '%04d.png'),
                    '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', str(HERE / 'reel_silent.mp4')], check=True)
    shutil.rmtree(fr)
    print('ok')
