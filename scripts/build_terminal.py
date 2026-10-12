"""Render a terminal window with exact text and a looping typing animation."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'assets'
W, H = 1000, 484
FONT = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 26)
SMALL = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 18)
BG, TEXT, BLUE = '#0e121a', '#dde3ed', '#a4b5cf'

base = Image.new('RGB', (W, H), '#0d1117')
d = ImageDraw.Draw(base)
# Window edge and a single active terminal tab.
d.rounded_rectangle((6, 6, W-7, H-7), radius=16, fill=BG, outline='#374354', width=2)
d.rounded_rectangle((8, 8, W-9, 68), radius=14, fill='#1a202b')
d.rectangle((8, 49, W-9, 68), fill='#1a202b')
d.rounded_rectangle((25, 22, 302, 68), radius=9, fill=BG)
d.rectangle((25, 58, 302, 70), fill=BG)
d.text((43, 29), '>_', font=SMALL, fill=BLUE)
d.text((83, 29), 'rizen@github', font=SMALL, fill='#d4dbe7')
d.line((277, 36, 284, 43), fill='#8491a5', width=1)
d.line((284, 36, 277, 43), fill='#8491a5', width=1)
d.text((327, 28), '+', font=SMALL, fill='#8491a5')
d.line((864, 38, 878, 38), fill='#8491a5', width=1)
d.rectangle((911, 32, 922, 43), outline='#8491a5')
d.line((959, 32, 970, 43), fill='#8491a5')
d.line((970, 32, 959, 43), fill='#8491a5')
d.line((24, 440, W-25, 440), fill='#202a38')
d.text((35, 454), '~/projects', font=SMALL, fill='#73839b')
d.text((805, 454), 'UTF-8  /  EN', font=SMALL, fill='#73839b')

def prompt(draw, y, command='', cursor=False):
    x = 37
    for segment, color in [('rizen@github', BLUE), (':~', '#9eabbf'), ('$ ', '#cf7779'), (command, TEXT)]:
        draw.text((x, y), segment, font=FONT, fill=color)
        x += draw.textlength(segment, font=FONT)
    if cursor:
        draw.rectangle((int(x)+2, y+3, int(x)+15, y+28), fill=BLUE)

def frame(cmd1='', lines=0, cmd2=None, current=0, final=False, cursor=True):
    im = base.copy()
    draw = ImageDraw.Draw(im)
    prompt(draw, 94, cmd1, cursor=cursor and lines==0 and cmd2 is None)
    output = ['Left 4 Dead 2 / Sven Co-op / IWBTCoop', 'The Outlast Trials / Hearts of Iron IV']
    for i in range(lines):
        draw.text((68, 145+i*35), output[i], font=FONT, fill='#bac8db')
    if cmd2 is not None:
        prompt(draw, 233, cmd2, cursor=cursor and current==0 and not final)
    if current >= 1:
        draw.text((68, 284), 'Making whatever I feel like.', font=FONT, fill=TEXT)
    if current >= 2:
        draw.text((68, 319), 'Hoping it pays.', font=FONT, fill='#cf7779')
    if final:
        prompt(draw, 390, cursor=cursor)
    return im

frames, durations = [], []
def add(im, ms):
    frames.append(im)
    durations.append(ms)

add(frame(), 600)
for n in range(1, len('games')+1):
    add(frame('games'[:n]), 100)
add(frame('games', lines=1), 550)
add(frame('games', lines=2), 700)
add(frame('games', 2, ''), 400)
for n in range(1, len('currently')+1):
    add(frame('games', 2, 'currently'[:n]), 90)
add(frame('games', 2, 'currently', 1), 550)
add(frame('games', 2, 'currently', 2), 550)
for n in range(12):
    add(frame('games', 2, 'currently', 2, final=True, cursor=n%2==0), 500)
frames[0].save(OUT/'terminal.gif', save_all=True, append_images=frames[1:], duration=durations, loop=0, optimize=True, disposal=1)
frame('games', 2, 'currently', 2, final=True).save(OUT/'terminal.png', optimize=True)
