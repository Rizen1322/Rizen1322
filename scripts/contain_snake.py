"""Keep every animated snake segment within the contribution grid's bounds."""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = '{http://www.w3.org/2000/svg}'
TRANSLATE = re.compile(r'transform:translate\((-?[\d.]+)px,(-?[\d.]+)px\)')

def contain(path):
    source = path.read_text(encoding='utf-8')
    root = ET.fromstring(source)
    cells = [el for el in root.findall(SVG_NS+'rect') if 'c' in el.get('class', '').split()]
    segments = [el for el in root.findall(SVG_NS+'rect') if 's' in el.get('class', '').split()]
    if not cells or not segments:
        raise ValueError(f'Unrecognized snake SVG: {path}')
    # Platane's grid uses 16px slots. Derive the slot span from its cells.
    xs = sorted({float(el.get('x')) for el in cells})
    ys = sorted({float(el.get('y')) for el in cells})
    step = min(b-a for a, b in zip(xs, xs[1:]))
    inset = (step-12)/2
    left, top = xs[0]-inset, ys[0]-inset
    right, bottom = xs[-1]+12+inset, ys[-1]+12+inset
    changed = 0
    for segment in segments:
        ident = next(c for c in segment.get('class').split() if c != 's')
        x = float(segment.get('x'))
        y = float(segment.get('y'))
        width = float(segment.get('width'))
        height = float(segment.get('height'))
        minimum_x, maximum_x = left-x, right-x-width
        minimum_y, maximum_y = top-y, bottom-y-height
        # Retain the existing slot positions; move external detours onto the edge.
        minimum_x = max(0, minimum_x)
        minimum_y = max(0, minimum_y)
        maximum_x = int(maximum_x//step)*step
        maximum_y = int(maximum_y//step)*step
        def adjust(match):
            nonlocal changed
            old_x, old_y = map(float, match.groups())
            new_x = max(minimum_x, min(maximum_x, old_x))
            new_y = max(minimum_y, min(maximum_y, old_y))
            changed += (new_x, new_y) != (old_x, old_y)
            return f'transform:translate({new_x:g}px,{new_y:g}px)'
        # Each segment has a separate keyframes rule; don't alter cells or bars.
        pattern = re.compile(r'(@keyframes '+re.escape(ident)+r'\{)(.*?)(?=@keyframes|\.'+re.escape(ident)+r'\{)', re.S)
        source, matched = pattern.subn(lambda m: m.group(1)+TRANSLATE.sub(adjust, m.group(2)), source)
        if matched != 1:
            raise ValueError(f'Missing keyframes for {ident}')
    # Linear interpolation between bounded positions stays inside the grid.
    path.write_text(source, encoding='utf-8')
    print(f'{path.name}: constrained {changed} positions')

if __name__ == '__main__':
    for filename in sys.argv[1:]:
        contain(Path(filename))
