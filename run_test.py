"""
run_test.py — generates HAZUS_Test.html with ONLY:
  About / HAZUS Flood / HAZUS Wind / HAZUS Earthquake / Utility Fragility
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
from data_utility    import extract_utility
from html_builder    import build_html

print("Loading HAZUS data...")
flood = extract_flood(os.path.join(DATA, 'HAZUS_FLOOD_DAMAGE_REPORT.xlsx'))
wind  = extract_wind(os.path.join(DATA,  'HAZUS_WIND_DAMAGE_REPORT.xlsx'))
utility = extract_utility(os.path.join(DATA, 'hazus_4.2sp3_section8_utility_fragility.csv'))
print(f"  Flood: {len(flood)} | Wind: {len(wind)} | EQ: {len(EQ_DB)} types | Utility: {len(utility)} curves")

d = lambda x: json.dumps(x, separators=(',',':'))
html = build_html(d(flood), d(wind), d(EQ_DB), '[]','[]','[]','[]','[]','[]', d(utility))

def find_div_close(html, start_after_open_tag):
    """Given position right after an opening <div ...> tag, return index just
    past the matching closing </div>, correctly handling nested divs."""
    depth = 1
    pos = start_after_open_tag
    while depth > 0:
        nxt_open  = html.find('<div', pos)
        nxt_close = html.find('</div>', pos)
        if nxt_close == -1:
            raise ValueError("Could not find matching closing div")
        if nxt_open != -1 and nxt_open < nxt_close:
            depth += 1
            pos = nxt_open + 4
        else:
            depth -= 1
            pos = nxt_close + len('</div>')
    return pos

# ── Locate the topbar (brand + nav-tabs) and keep only Flood/Wind/EQ/Utility tabs ──
topbar_marker = '<div class="topbar">'
ts = html.find(topbar_marker)
te = find_div_close(html, ts + len(topbar_marker))
topbar_html = html[ts:te]
for tab in ['gem', 'esrm', 'jrc', 'etris', 'ci', 'wizard']:
    topbar_html = re.sub(
        r'<(?:button|a)[^>]*data-tab="' + tab + r'"[^>]*>.*?</(?:button|a)>',
        '', topbar_html, flags=re.DOTALL
    )
# Remove the "About" tab entirely (no standalone about page in this build)
topbar_html = re.sub(
    r'<a class="nav-tab"[^>]*>About</a>\s*', '', topbar_html
)

# ── Keep only the Flood/Wind/EQ/Utility page divs (drop GEM/JRC/etc, no wrapper div exists) ──
search_start = te
all_page_starts = sorted(
    m.start() for m in re.finditer(r'<div id="page-\w+"', html[search_start:])
)
all_page_starts = [p + search_start for p in all_page_starts]
footer_pos = html.find('<footer', search_start)
boundary = footer_pos if footer_pos > 0 else html.find('<script>', search_start)

pages_html = ''
for tab in ['flood', 'wind', 'eq', 'util']:
    s = html.find(f'<div id="page-{tab}"', search_start, boundary)
    if s < 0:
        continue
    later = [p for p in all_page_starts if p > s]
    e = later[0] if later else boundary
    pages_html += html[s:e].rstrip() + '\n'

# ── Reassemble: everything up to topbar, filtered topbar, pages, then footer/script/tail ──
html = html[:ts] + topbar_html + '\n' + pages_html + html[boundary:]

# ── Save ──
out = os.path.join(FOLDER, 'HAZUS_Test.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

size = os.path.getsize(out) / 1024 / 1024
print(f"\nSaved: {out}  ({size:.1f} MB)")
print("Pages:", sorted(set(re.findall(r'id="page-(\w+)"', html))))
print("Tabs:",  sorted(set(re.findall(r'data-tab="(\w+)"', html))))

webbrowser.open('file:///' + out.replace(os.sep, '/'))
