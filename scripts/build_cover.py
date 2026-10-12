"""Compose the user's supplied Rei artwork with typography. No image generation."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
w, h = 1800, 620
cover = Image.new('RGB', (w, h), '#101114')
art = Image.open(root / 'assets/rei-original.png').convert('RGB')
art.thumbnail((680, h), Image.Resampling.LANCZOS)
cover.paste(art, (w-art.width, (h-art.height)//2))
d = ImageDraw.Draw(cover)
def text(x, y, value, size, color, bold=False, spacing=0):
    f = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf', size)
    for char in value:
        d.text((x,y), char, font=f, fill=color)
        x += d.textlength(char,font=f) + spacing

text(94, 70, 'Rizen1322 / GitHub', 24, '#9c9da6', spacing=1)
text(86, 190, 'RIZEN', 154, '#eeeae3', bold=True, spacing=8)
d.rectangle((95, 383, 160, 387), fill='#bb4b4c')
text(94, 427, 'Apps, mods & web projects', 29, '#b6b7c1')
cover.save(root/'assets/rei-cover.png',optimize=True)
