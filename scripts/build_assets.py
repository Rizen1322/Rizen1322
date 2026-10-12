"""Build the profile artwork. Requires Pillow; uses standard Windows fonts."""
from pathlib import Path
from math import sin, pi
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)
FONT_DIR = Path('C:/Windows/Fonts')
BG = '#0c0c14'
INK = '#f1eef9'
MUTED = '#aaa7bb'
RED = '#ff485c'
PURPLE = '#b49aff'
GREEN = '#b9ef78'

def font(size, mono=False):
    return ImageFont.truetype(str(FONT_DIR / ('consola.ttf' if mono else 'arialbd.ttf')), size)

def txt(d, xy, text, size, color=INK, mono=False):
    d.text(xy, text, fill=color, font=font(size, mono))

def base(w, h):
    im = Image.new('RGB', (w, h), BG)
    d = ImageDraw.Draw(im)
    for x in range(0, w, 40):
        d.line((x, 0, x, h), fill='#171722')
    for y in range(0, h, 40):
        d.line((0, y, w, y), fill='#171722')
    d.rectangle((0, 0, w-1, h-1), outline='#34313f')
    return im, d

def hero(t=0):
    im, d = base(1200, 390)
    d.rectangle((0, 0, 11, 390), fill=RED)
    txt(d, (42, 27), 'RIZEN1322 / PERSONAL PROJECTS', 19, PURPLE, True)
    d.line((42, 66, 1157, 66), fill='#3c334c', width=1)
    txt(d, (38, 84), 'RIZEN', 133)
    txt(d, (46, 241), 'WINDOWS APPS / GAME MODS / WEB', 22, PURPLE, True)
    txt(d, (46, 284), 'Приложения для Windows, моды и веб-проекты.', 20, MUTED, True)
    txt(d, (46, 350), 'REPOSITORIES  03', 16, MUTED, True)
    txt(d, (915, 350), 'EN / RU', 16, MUTED, True)
    # An original geometric mecha mask, drawn as a technical blueprint.
    cx, cy = 980, 194
    for radius, col in [(133, '#3e344f'), (111, '#292439')]:
        d.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), outline=col, width=2)
    d.line((824, cy, 1136, cy), fill='#44344c')
    d.line((cx, 77, cx, 321), fill='#44344c')
    d.polygon([(892,145),(908,91),(949,131),(980,75),(1011,131),(1052,91),(1068,145),(1047,249),(980,304),(913,249)], fill='#1b172b', outline=PURPLE, width=3)
    d.polygon([(980,75),(997,136),(980,177),(963,136)], fill=RED)
    d.polygon([(916,171),(970,187),(953,207),(923,194)], fill=GREEN)
    d.polygon([(1044,171),(990,187),(1007,207),(1037,194)], fill=GREEN)
    d.line((980,181,980,269), fill=PURPLE, width=3)
    d.line((931,225,980,269,1029,225), fill=RED, width=3)
    d.polygon([(913,249),(940,244),(954,277)], fill='#584079')
    d.polygon([(1047,249),(1020,244),(1006,277)], fill='#584079')
    # Scan stays inside the blueprint and never crosses the main text.
    scan_y = int(88 + (t % 1) * 228)
    d.line((845,scan_y,1115,scan_y), fill='#6a507e', width=2)
    for i in range(21):
        x = 660+i*8
        height = int(9 + 17*(1+sin(i*.5+t*2*pi))/2)
        d.rectangle((x,378-height,x+3,378), fill=PURPLE if i%4 else RED)
    for x in range(40,1200,28):
        d.polygon([(x,386),(x+17,386),(x+21,389),(x+4,389)],fill=RED)
    return im

frames = [hero(i/48) for i in range(48)]
frames[0].save(ASSETS/'header.gif', save_all=True, append_images=frames[1:], duration=100, loop=0, optimize=True, disposal=2)
hero(.35).save(ASSETS/'header.png')

def card(filename, number, title, sub, stack, accent, kind):
    im,d = base(1200,168)
    d.rectangle((0,0,8,168),fill=accent)
    txt(d,(35,23),number,21,accent,True)
    txt(d,(88,17),title,37)
    txt(d,(89,70),sub,21,MUTED,True)
    txt(d,(89,124),stack,17,accent,True)
    # Separate pictograms for recording, two runtimes, and a storefront.
    if kind=='record':
        d.rounded_rectangle((1035,37,1142,127),radius=12,outline=accent,width=3)
        d.ellipse((1066,58,1112,104),outline=accent,width=3)
        d.ellipse((1080,72,1098,90),fill=accent)
        d.line((1022,143,1155,143),fill=accent,width=3)
    elif kind=='bridge':
        d.polygon([(1036,63),(1068,44),(1100,63),(1100,100),(1068,119),(1036,100)],outline=accent,width=3)
        d.line((1036,63,1068,81,1100,63),fill=accent,width=3)
        d.line((1068,81,1068,119),fill=accent,width=3)
        d.line((1114,80,1155,80),fill=RED,width=3)
        d.line((1144,69,1155,80,1144,91),fill=RED,width=3)
    else:
        d.rectangle((1043,65,1141,130),outline=accent,width=3)
        d.polygon([(1035,65),(1050,37),(1134,37),(1149,65)],outline=accent,width=3)
        d.rectangle((1077,91,1105,130),outline=accent,width=3)
        for x in range(1056,1140,20):
            d.line((x,38,x,65),fill=accent,width=2)
    im.save(ASSETS/filename)

card('aura.png','01','Aura / InstantReplay','Save the last minutes of play with a hotkey.','C# / .NET / Windows / NVENC',PURPLE,'record')
card('l4d2-minecraft.png','02','L4D2 x Minecraft','Minecraft blocks and items inside Left 4 Dead 2.','Java / Fabric / Python / Source / ReShade',RED,'bridge')
card('skillmart.png','03','Skillmart','A small marketplace for digital services.','Web / HTML',GREEN,'store')

im,d=base(1200,64)
d.rectangle((0,0,8,64),fill=RED)
txt(d,(35,19),'ACTIVITY / АКТИВНОСТЬ',20,PURPLE,True)
d.line((365,32,1150,32),fill='#453550',width=2)
im.save(ASSETS/'activity.png')
