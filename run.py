"""
run.py — entry point. Run this file only.
Uses JSON cache for slow data sources (GEM, ETRiS, CI) so repeated runs
take ~10s instead of ~2 minutes.
Cache files are stored in data_sources/cache/ and auto-invalidated when
source files change.
"""
import os, sys, json, time, webbrowser

FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA   = os.path.join(FOLDER, 'data_sources')
CACHE  = os.path.join(DATA, 'cache')
sys.path.insert(0, FOLDER)
os.makedirs(CACHE, exist_ok=True)

t0 = time.time()


def _cache_path(name):
    return os.path.join(CACHE, f'{name}.json')


def _longpath(p):
    """Add Windows long-path prefix to bypass 260-char limit."""
    if os.name == 'nt' and not p.startswith('\\\\?\\'):
        return '\\\\?\\' + os.path.abspath(p)
    return p


def _is_fresh(cache_file, *source_paths):
    """Return True if cache exists and is newer than all source paths."""
    if not os.path.exists(cache_file):
        return False
    cache_mtime = os.path.getmtime(cache_file)
    for src in source_paths:
        if not os.path.exists(src) and not os.path.exists(_longpath(src)):
            continue
        if os.path.isdir(src):
            for root, dirs, files in os.walk(_longpath(src)):
                depth = root.replace(_longpath(src), '').count(os.sep)
                if depth > 3:
                    dirs[:] = []  # don't recurse deeper
                    continue
                for f in files:
                    fp = os.path.join(root, f)
                    try:
                        if os.path.getmtime(fp) > cache_mtime:
                            return False
                    except OSError:
                        continue
        else:
            try:
                if os.path.getmtime(_longpath(src)) > cache_mtime:
                    return False
            except OSError:
                pass
    return True


def _load_cache(name):
    path = _cache_path(name)
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def _save_cache(name, data):
    path = _cache_path(name)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, separators=(',', ':'))
    print(f'    Cached to: {os.path.basename(path)}')


# ── Imports ──
print("Importing modules...")
from data_flood      import extract_flood
from data_wind       import extract_wind
from data_earthquake import EQ_DB
from data_ci         import extract_ci
from data_validate    import validate_eq_median_row, log_problems
from html_builder    import build_html
from page_explainer  import build_explainer

# Optional data sources - if their module isn't present in this checkout,
# skip them gracefully rather than failing the whole build. build_html
# already defaults each of these to an empty list.
try:
    from data_gem import extract_gem, GEM_PGA
except ImportError:
    print("  SKIP: data_gem.py not found")
    extract_gem, GEM_PGA = None, {}
try:
    from data_jrc import extract_jrc
except ImportError:
    print("  SKIP: data_jrc.py not found")
    extract_jrc = None
try:
    from data_etris import extract_etris
except ImportError:
    print("  SKIP: data_etris.py not found")
    extract_etris = None
try:
    from data_esrm import extract_esrm
except ImportError:
    print("  SKIP: data_esrm.py not found")
    extract_esrm = None
print(f"  Imports done in {time.time()-t0:.1f}s")

DASHBOARD = os.path.join(FOLDER, 'HAZUS_Dashboard.html')
INDEX     = os.path.join(FOLDER, 'index.html')

print("\nExtracting data...")

# ── HAZUS Flood (fast, no cache needed) ──
flood = []
flood_src = os.path.join(DATA, 'HAZUS_FLOOD_DAMAGE_REPORT.xlsx')
if os.path.exists(flood_src):
    flood = extract_flood(flood_src)
else:
    print("  SKIP: HAZUS_FLOOD_DAMAGE_REPORT.xlsx not found")

# ── HAZUS Wind (already reads from local cache file) ──
wind = extract_wind(os.path.join(DATA, 'HAZUS_WIND_DAMAGE_REPORT.xlsx'))

# ── GEM (slow XML parser — cache aggressively) ──
gem = []
gem_src = os.path.join(DATA, 'global_vulnerability_model-main')
gem_cache = _cache_path('gem')
if os.path.isdir(gem_src):
    if _is_fresh(gem_cache, gem_src):
        print(f"  GEM: loading from cache...")
        gem = _load_cache('gem')
        print(f"    {len(gem)} functions (cached)")
    else:
        gem = extract_gem(gem_src)
        _save_cache('gem', gem)
else:
    print("  SKIP: global_vulnerability_model-main not found")

# ── JRC (fast, no cache needed) ──
jrc = []
jrc_src = os.path.join(DATA, 'copy_of_global_flood_depth-damage_functions__30102017.xlsx')
if os.path.exists(jrc_src):
    jrc = extract_jrc(jrc_src)
else:
    print("  SKIP: JRC xlsx not found")

# ── ETRiS (medium, cache it) ──
etris = []
etris_src = os.path.join(DATA, 'etris_data_and_data_products-main')
etris_cache = _cache_path('etris')
if os.path.isdir(etris_src):
    if _is_fresh(etris_cache, etris_src):
        print(f"  ETRiS: loading from cache...")
        etris = _load_cache('etris')
        print(f"    {len(etris)} curves (cached)")
    else:
        etris = extract_etris(etris_src)
        _save_cache('etris', etris)
else:
    print("  SKIP: etris_data_and_data_products-main not found")

# ── ESRM20 (fast enough, no cache needed) ──
esrm = []
esrm_src = os.path.join(DATA, 'esrm20_fragility_various_IM_lognormal.xlsx')
if os.path.exists(esrm_src):
    esrm = extract_esrm(esrm_src)
else:
    print("  SKIP: esrm20_fragility_various_IM_lognormal.xlsx not found")

# ── CI Vulnerability (fast enough, no cache needed) ──
ci = []
ci_src = os.path.join(DATA, 'Critical Infrastructure - Nirandjan 2024')
if os.path.isdir(ci_src):
    ci = extract_ci(ci_src)
else:
    print("  SKIP: Critical Infrastructure - Nirandjan 2024 not found")

t1 = time.time()
print(f"\nData extraction: {t1-t0:.1f}s")

_eq_problems = []
for _code, _row in EQ_DB.items():
    _eq_problems.extend(validate_eq_median_row(_code, _row))
log_problems(_eq_problems, "HAZUS EQ median PGA table (data_earthquake.py)")
if _eq_problems:
    print(f"  WARNING: {len(_eq_problems)} problem(s) found in the static EQ_DB table \u2014 "
          f"see above. Building anyway; fix data_earthquake.py directly.")

print("Summary:")
print(f"  HAZUS flood  : {len(flood)} functions")
print(f"  HAZUS wind   : {len(wind)} functions")
print(f"  HAZUS EQ     : {len(EQ_DB)} building types")
print(f"  GEM EQ       : {len(gem)} functions")
print(f"  JRC flood    : {len(jrc)} curves")
print(f"  ETRiS tsunami: {len(etris)} curves")
print(f"  ESRM20 EQ    : {len(esrm)} functions")
print(f"  CI infra     : {len(ci)} curves")

# ── Generate dashboard ──
print("\nGenerating dashboard...")
d = lambda x: json.dumps(x, separators=(',', ':'))
html = build_html(
    flood_json   = d(flood),
    wind_json    = d(wind),
    eq_json      = d(EQ_DB),
    gem_json     = d(gem),
    jrc_json     = d(jrc),
    gem_pga_json = d(GEM_PGA),
    etris_json   = d(etris),
    esrm_json    = d(esrm),
    ci_json      = d(ci),
)
with open(DASHBOARD, 'w', encoding='utf-8') as fh:
    fh.write(html)
size = os.path.getsize(DASHBOARD) / 1024 / 1024
print(f"  Saved: {DASHBOARD}  ({size:.1f} MB)")

# ── Generate landing page ──
print("\nGenerating landing page...")
with open(INDEX, 'w', encoding='utf-8') as fh:
    fh.write(build_explainer())
print(f"  Saved: {INDEX}")

t2 = time.time()
print(f"\nTotal time: {t2-t0:.1f}s")
if not os.environ.get('CI'):
    print("Opening browser...")
    # Add timestamp to URL to force browser to reload fresh HTML (bypasses cache)
    import time as _time
    cache_bust = '?v=' + str(int(_time.time()))
    webbrowser.open('file:///' + INDEX.replace(os.sep, '/') + cache_bust)
