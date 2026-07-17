"""
run_test.py — generates HAZUS_Test.html with ONLY:
  About / HAZUS Flood / HAZUS Wind / HAZUS Earthquake
No GEM, no ETRiS, no ESRM, no JRC, no CI, no Curve Finder.
Runs in ~5 seconds.
"""
import os, sys, json, re, webbrowser

FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA   = os.path.join(FOLDER, 'data_sources')
sys.path.insert(0, FOLDER)

from data_flood      import extract_flood
from data_wind       import extract_wind
from data_earthquake import EQ_DB
from html_builder    import build_html

print("Loading HAZUS data...")
flood = extract_flood(os.path.join(DATA, 'HAZUS_FLOOD_DAMAGE_REPORT.xlsx'))
wind  = extract_wind(os.path.join(DATA,  'HAZUS_WIND_DAMAGE_REPORT.xlsx'))
print(f"  Flood: {len(flood)} | Wind: {len(wind)} | EQ: {len(EQ_DB)} types")

d = lambda x: json.dumps(x, separators=(',',':'))
html = build_html(d(flood), d(wind), d(EQ_DB), '[]','[]','[]','[]','[]','[]')

# ── Keep only the nav-tabs bar (filtered to About/Flood/Wind/EQ) ──
nav_marker = '<div class="nav-tabs">'
ns = html.find(nav_marker)
# walk forward counting div depth to find the TRUE closing </div> for nav-tabs
depth = 1
pos = ns + len(nav_marker)
while depth > 0:
    nxt_open  = html.find('<div', pos)
    nxt_close = html.find('</div>', pos)
    if nxt_close == -1:
        raise ValueError("Could not find closing tag for nav-tabs div")
    if nxt_open != -1 and nxt_open < nxt_close:
        depth += 1
        pos = nxt_open + 4
    else:
        depth -= 1
        pos = nxt_close + len('</div>')
ne = pos
nav_html = html[ns:ne]
for tab in ['gem', 'esrm', 'jrc', 'etris', 'ci', 'wizard']:
    nav_html = re.sub(
        r'<(?:button|a)[^>]*data-tab="' + tab + r'"[^>]*>.*?</(?:button|a)>',
        '', nav_html, flags=re.DOTALL
    )

# ── Strip non-HAZUS pages from content, keep filtered nav ──
content_marker = '<div class="content">'
cs = html.find(content_marker) + len(content_marker)
ce = html.rfind('</div>', 0, html.find('<script>', cs))

pages_html = ''
for tab in ['flood','wind','eq']:
    s = html.find(f'<div id="page-{tab}"', cs, ce)
    if s < 0: continue
    others = [html.find(f'<div id="page-{t}"', s+1, ce)
              for t in ['wind','eq','gem','jrc','etris','esrm','ci','wizard']
              if html.find(f'<div id="page-{t}"', s+1, ce) > 0]
    ftr = html.find('<footer', s, ce)
    if ftr > 0: others.append(ftr)
    e = min(others) if others else ce
    pages_html += html[s:e].rstrip() + '\n'

html = html[:cs] + '\n' + nav_html + '\n' + pages_html + html[ce:]

# ── Save ──
out = os.path.join(FOLDER, 'HAZUS_Test.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

size = os.path.getsize(out) / 1024 / 1024
print(f"\nSaved: {out}  ({size:.1f} MB)")
print("Pages:", sorted(set(re.findall(r'id="page-(\w+)"', html))))
print("Tabs:",  sorted(set(re.findall(r'data-tab="(\w+)"', html))))

webbrowser.open('file:///' + out.replace(os.sep, '/'))
