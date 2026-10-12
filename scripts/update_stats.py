"""Render public GitHub repository statistics using only the standard library."""
import json
import os
from collections import Counter
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from urllib.request import Request, urlopen

USER = 'Rizen1322'
ROOT = Path(__file__).resolve().parents[1]

def api(path):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': USER+'-profile', 'X-GitHub-Api-Version': '2022-11-28'}
    if os.environ.get('GITHUB_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
    with urlopen(Request('https://api.github.com/'+path, headers=headers), timeout=30) as response:
        return json.load(response)

repos = []
page = 1
while True:
    batch = api(f'users/{USER}/repos?per_page=100&page={page}')
    repos.extend(batch)
    if len(batch) < 100:
        break
    page += 1
languages = Counter()
originals = [r for r in repos if not r['fork'] and r['name'] != USER]
for repo in originals:
    languages.update(api(f"repos/{USER}/{repo['name']}/languages"))
top = languages.most_common(4)
other = sum(languages.values()) - sum(count for _, count in top)
if other:
    top.append(('Other', other))
total = sum(languages.values())
colors = ['#9eafc9', '#7088a7', '#506580', '#bb4b4c', '#363f4e']
parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="800" height="270" viewBox="0 0 800 270" role="img" aria-labelledby="title desc">',
         '<title id="title">Public GitHub repositories and languages</title>',
         '<desc id="desc">Public repository count and received stars. Language shares are based on bytes in public non-fork repositories, excluding the profile repository.</desc>',
         '<rect x="1" y="1" width="798" height="268" rx="12" fill="#101114" stroke="#303641"/>']

def text(x, y, value, size=22, color='#aeb8c8', weight='400'):
    parts.append(f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(str(value))}</text>')

text(32, 42, 'Public GitHub', 24, '#eeeae3', '600')
text(32, 105, len(repos), 44, '#eeeae3', '600')
text(88, 101, 'repositories', 22)
text(430, 105, sum(r['stargazers_count'] for r in repos), 44, '#eeeae3', '600')
text(480, 101, 'received stars', 22)
parts.append('<path d="M32 127H768" stroke="#303641"/>')
text(32, 160, 'Languages by code size', 20)
x = 32
for i, (language, count) in enumerate(top):
    segment = 736 * count / total if total else 0
    parts.append(f'<rect x="{x:.2f}" y="177" width="{segment:.2f}" height="12" fill="{colors[i]}"/>')
    x += segment
x = 32
for i, (language, count) in enumerate(top):
    label = f'{language} {count/total*100:.1f}%'
    parts.append(f'<circle cx="{x+5}" cy="214" r="5" fill="{colors[i]}"/>')
    text(x+17, 221, label, 18)
    x += 155
stamp = datetime.now(timezone.utc).strftime('%Y-%m-%d')
text(32, 251, 'Public non-fork code · Updated '+stamp, 16, '#7e8899')
parts.append('</svg>')
(ROOT/'assets/github-stats.svg').write_text('\n'.join(parts), encoding='utf-8')

release = api(f'repos/{USER}/InstantReplay/releases/latest')
tag = escape(release['tag_name'])
badge_width = 90 + max(90, len(release['tag_name']) * 9 + 24)
badge = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{badge_width}" height="30" viewBox="0 0 {badge_width} 30" role="img" aria-labelledby="title">
<title id="title">Aura release {tag}</title>
<rect x=".5" y=".5" width="{badge_width-1}" height="29" rx="6" fill="#101114" stroke="#303641"/>
<path d="M85 1V29" stroke="#303641"/>
<text x="43" y="20" text-anchor="middle" font-family="Arial,sans-serif" font-size="13" fill="#aeb8c8">release</text>
<text x="{85+(badge_width-85)/2}" y="20" text-anchor="middle" font-family="Arial,sans-serif" font-size="13" font-weight="600" fill="#a4b5cf">{tag}</text>
</svg>'''
(ROOT/'assets/aura-release.svg').write_text(badge, encoding='utf-8')
