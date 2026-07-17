"""
html_builder.py  (~450 lines — HTML only)
Assembles dashboard HTML. JS logic is in separate files:
  js_utils.py  — shared utilities (chart, copy, toast, tooltips)
  js_flood.py  — flood curve 1 and 2 logic
  js_wind.py   — wind curve 1 and 2 logic
  js_eq.py     — earthquake curve 1 and 2 logic
"""
from js_utils import get_utils_js
from js_flood import get_flood_js
from js_wind  import get_wind_js
from js_eq    import get_eq_js
from js_gem   import get_gem_js
from js_jrc   import get_jrc_js
from js_etris  import get_etris_js
from js_esrm   import get_esrm_js
from js_ci     import get_ci_js
from js_wizard import get_wizard_js
from js_wizard  import get_wizard_js

def build_html(flood_json: str, wind_json: str, eq_json: str, gem_json: str = '[]', jrc_json: str = '[]', gem_pga_json: str = '[]', etris_json: str = '[]', esrm_json: str = '[]', ci_json: str = '[]') -> str:
    parts = []

    parts.append('''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">\n<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">\n<meta http-equiv="Pragma" content="no-cache">\n<meta http-equiv="Expires" content="0">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vulnerability Function Explorer</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --wtw:#7F35B2;--wtw-deep:#48086F;--wtw-light:#F3EAF9;--wtw-mid:#C89FDC;
  --onyx:#2F2C31;--onyx2:#5A5660;--onyx3:#949096;
  --bg:#FFFFFF;--bg2:#F8F5FB;--bg3:#EDE6F4;--border:#DDD5E8;
  --r:7px;--rl:12px;
  --slight:#1A7340;--moderate:#C47D00;--extensive:#C0321A;--complete:#48086F;
}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
     background:var(--bg2);color:var(--onyx);font-size:14px;min-height:100vh}
.topbar{background:#0f2350;padding:0 32px;display:flex;align-items:center;height:58px;position:sticky;top:0;z-index:100;box-shadow:0 1px 0 rgba(255,255,255,.08),0 4px 16px rgba(0,0,0,.3);overflow-x:auto}
.brand{font-size:14px;font-weight:700;color:#fff;letter-spacing:-.3px;margin-right:28px;white-space:nowrap;flex-shrink:0}
.brand span{color:#9fc0ff}
.nav-tabs{display:flex;height:100%;align-items:center;gap:2px;flex:1}
── */
.topbar{background:#0f2350;padding:0 32px;display:flex;align-items:center;
        height:56px;position:sticky;top:0;z-index:100;
        box-shadow:0 1px 0 rgba(255,255,255,.08),0 4px 16px rgba(0,0,0,.3);
        gap:0;overflow-x:auto}
        box-shadow:0 1px 0 rgba(255,255,255,.08),0 4px 16px rgba(0,0,0,.3);
        gap:0;overflow-x:auto}
.brand{font-size:14px;font-weight:700;color:#fff;letter-spacing:-.3px;margin-right:28px;white-space:nowrap;flex-shrink:0}
.brand span{color:#9fc0ff}
.nav-tabs{display:flex;height:100%;align-items:center;gap:2px;flex:1}
.nav-tab{padding:0 18px;font-size:14px;font-weight:500;border:none;background:none;color:rgba(255,255,255,.55);cursor:pointer;border-bottom:3px solid transparent;transition:color .2s,border-color .2s;height:100%;white-space:nowrap;text-decoration:none;display:inline-flex;align-items:center;border-radius:0}
.nav-tab:hover{color:rgba(255,255,255,.9);background:rgba(255,255,255,.04)}
.nav-tab.active{color:#fff;border-bottom-color:#9fc0ff;background:none;font-weight:600}
.nav-sep{width:1px;height:18px;background:rgba(255,255,255,.15);margin:0 4px;flex-shrink:0}
.page{display:none;padding:28px 32px;max-width:1440px;margin:0 auto}
.page.active{display:block}
.page-title{font-size:20px;font-weight:700;color:var(--wtw-deep);margin-bottom:4px}
.page-sub{font-size:13px;color:var(--onyx2);margin-bottom:22px;line-height:1.5}
.filters{background:var(--bg);border:1px solid var(--border);border-radius:var(--rl);
         padding:20px;margin-bottom:20px;
         display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:16px;align-items:start}
.fg{display:flex;flex-direction:column}
.fg label{font-size:11px;font-weight:700;letter-spacing:.6px;text-transform:uppercase;color:var(--onyx3);margin-bottom:3px}
.fg .hint{font-size:11px;color:var(--onyx3);margin-bottom:6px;line-height:1.4}
.fg select{width:100%;padding:8px 10px;border:1.5px solid var(--border);border-radius:var(--r);
           background:var(--bg);color:var(--onyx);font-size:13px;outline:none;cursor:pointer;transition:border-color .15s}
.fg select:focus{border-color:var(--wtw);box-shadow:0 0 0 3px var(--wtw-light)}
.cmp-section{background:var(--bg);border:1px solid var(--border);border-radius:var(--rl);
             padding:18px 20px;margin-bottom:20px}
.cmp-toggle{display:flex;align-items:center;gap:9px;font-size:13px;font-weight:600;
            color:var(--onyx2);cursor:pointer;user-select:none}
.cmp-toggle input[type=checkbox]{width:18px;height:18px;accent-color:var(--wtw);cursor:pointer}
.cmp-toggle.on{color:var(--wtw)}
.cmp2-wrap{display:none;margin-top:18px;padding-top:16px;border-top:2px solid #c900ac}
.cmp2-label{font-size:12px;font-weight:700;color:#c900ac;letter-spacing:.5px;
            text-transform:uppercase;margin-bottom:12px;display:flex;align-items:center;gap:8px}
.cmp2-badge{display:inline-flex;align-items:center;justify-content:center;
            width:20px;height:20px;border-radius:50%;background:#c900ac;color:#fff;
            font-size:11px;font-weight:700;flex-shrink:0}
.cmp2-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:16px}
.cmp-legend{display:flex;gap:20px;flex-wrap:wrap;padding:10px 18px;
            background:var(--bg2);border-top:1px solid var(--border);font-size:12px;color:var(--onyx2)}
.cl-item{display:flex;align-items:center;gap:7px;font-weight:500}
.cl-dot{width:28px;height:3px;border-radius:2px;flex-shrink:0}
.tbl-tabs{display:flex;border-bottom:1px solid var(--border)}
.tbl-tab{padding:8px 18px;font-size:12px;font-weight:600;border:none;background:none;
         color:var(--onyx3);cursor:pointer;border-bottom:3px solid transparent;transition:all .15s}
.tbl-tab.active{color:var(--wtw);border-bottom-color:var(--wtw);background:var(--wtw-light)}
.tbl-tab .dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:5px}
.wind-unit-row{display:flex;align-items:center;gap:14px;margin-bottom:14px;flex-wrap:wrap}
.wlabel{font-size:11px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;color:var(--onyx3);white-space:nowrap}
.unit-switch{display:inline-flex;border:1.5px solid var(--border);border-radius:100px;overflow:hidden}
.us-btn{padding:5px 14px;font-size:12px;font-weight:600;border:none;background:none;
        color:var(--onyx2);cursor:pointer;transition:all .15s;white-space:nowrap}
.us-btn.active{background:var(--wtw);color:#fff}
.us-btn:hover:not(.active){background:var(--bg3)}
.grid{display:grid;grid-template-columns:1fr 330px;gap:20px;align-items:start}
.card{background:var(--bg);border:1px solid var(--border);border-radius:var(--rl);overflow:hidden}
.card-hdr{padding:16px 20px;border-bottom:1px solid var(--border);background:linear-gradient(135deg,var(--bg),var(--bg2))}
.card-title{font-size:13px;font-weight:700;line-height:1.5;color:var(--wtw-deep)}
.card-sub{font-size:12px;color:var(--onyx2);margin-top:3px}
.card-body{padding:16px 20px}
.chart-wrap{position:relative;height:340px}
.meta-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:14px 16px;border-bottom:1px solid var(--border)}
.mi{background:var(--bg2);border-radius:var(--r);padding:9px 11px;border-left:3px solid var(--wtw)}
.mi-l{font-size:10px;color:var(--onyx3);font-weight:700;text-transform:uppercase;letter-spacing:.5px}
.mi-v{font-size:12px;font-weight:700;margin-top:2px;color:var(--onyx)}
.tbl-hdr{padding:11px 16px;display:flex;justify-content:space-between;align-items:center;
         border-bottom:1px solid var(--border);background:var(--bg2)}
.tbl-label{font-size:11px;font-weight:700;color:var(--onyx2);text-transform:uppercase;letter-spacing:.5px}
.copy-btn{font-size:12px;padding:7px 18px;border:none;border-radius:6px;background:var(--wtw);
          color:#fff;cursor:pointer;font-weight:700;transition:background .2s,transform .1s;min-width:110px;text-align:center}
.copy-btn:hover{background:var(--wtw-deep)}
.copy-btn.ok{background:#1A7340;transform:scale(1.05)}
.copy-btn.err{background:#C0321A}
.toast{position:fixed;bottom:32px;right:32px;font-size:13px;font-weight:700;
       padding:14px 24px;border-radius:8px;color:#fff;box-shadow:0 6px 24px rgba(0,0,0,.3);
       opacity:0;transform:translateY(12px);transition:opacity .25s,transform .25s;pointer-events:none;z-index:99999}
.toast.show{opacity:1;transform:translateY(0)}
.tbl-wrap{max-height:440px;overflow-y:auto}
table{width:100%;border-collapse:collapse;font-size:12px}
thead th{padding:8px 14px;text-align:right;background:var(--bg2);font-weight:700;
         color:var(--wtw-deep);font-size:10px;text-transform:uppercase;letter-spacing:.5px;
         position:sticky;top:0;border-bottom:1px solid var(--border)}
thead th:first-child{text-align:left}
tbody td{padding:6px 14px;border-bottom:1px solid var(--bg3);text-align:right}
tbody td:first-child{text-align:left;font-weight:600;color:var(--wtw-deep)}
tbody tr:hover td{background:var(--wtw-light)}
tbody tr:last-child td{border-bottom:none}
.legend-row{display:flex;flex-wrap:wrap;gap:14px;padding:14px 20px;
            border-top:1px solid var(--border);background:var(--bg2)}
.li{display:flex;align-items:center;gap:7px;font-size:12px;color:var(--onyx2);font-weight:500}
.ld{width:28px;height:3px;border-radius:2px}
.tbl-hdr-row{padding:11px 16px;display:flex;justify-content:space-between;align-items:center;
             border-bottom:1px solid var(--border);background:var(--bg2);gap:8px;flex-wrap:wrap}
.btn-row{display:flex;gap:8px;align-items:center}
.icon-btn{font-size:11px;padding:6px 12px;border:1.5px solid var(--border);border-radius:6px;
          background:none;color:var(--onyx2);cursor:pointer;font-weight:600;transition:all .15s;
          display:flex;align-items:center;gap:5px;white-space:nowrap}
.icon-btn:hover{background:var(--bg3);border-color:var(--wtw);color:var(--wtw)}
.reset-btn{font-size:11px;padding:5px 12px;border:1.5px solid var(--border);border-radius:6px;
           background:none;color:var(--onyx3);cursor:pointer;font-weight:600;transition:all .15s}
.reset-btn:hover{border-color:#C0321A;color:#C0321A;background:#fff0f0}
.match-count{font-size:11px;color:var(--onyx3);font-style:italic}
.wz-steps{display:flex;gap:0;margin-bottom:28px;flex-wrap:wrap}
.wz-step{font-size:12px;font-weight:600;color:var(--g3);padding:7px 16px;
  background:var(--bg2);border:1px solid var(--border);cursor:default;
  border-right:none;white-space:nowrap}
.wz-step:first-child{border-radius:7px 0 0 7px}
.wz-step:last-child{border-radius:0 7px 7px 0;border-right:1px solid var(--border)}
.wz-step-active{background:var(--plum);color:#fff;border-color:var(--plum)}
.wz-section{margin-bottom:24px}
.wz-section-label{font-size:11px;font-weight:700;color:var(--g3);letter-spacing:.5px;
  text-transform:uppercase;margin-bottom:10px}
.wz-peril-grid{display:flex;gap:10px;flex-wrap:wrap}
.wz-peril-btn{padding:9px 20px;border:2px solid var(--border);border-radius:8px;
  background:var(--bg);font-size:13px;font-weight:600;cursor:pointer;
  color:var(--g2);transition:all .15s}
.wz-peril-btn:hover{border-color:var(--plum);color:var(--plum)}
.wz-peril-btn.active{color:#fff;border-color:transparent}
.wz-select{width:100%;max-width:420px;padding:8px 12px;
  border:1px solid var(--border);border-radius:7px;font-size:13px;
  color:var(--onyx);background:var(--bg);font-family:inherit}
.wz-result-row{display:flex;align-items:flex-start;justify-content:space-between;
  gap:16px;padding:14px 16px;border:1px solid var(--border);border-radius:9px;
  margin-bottom:10px;background:var(--bg);transition:box-shadow .15s}
.wz-result-row:hover{box-shadow:0 2px 10px rgba(0,0,0,.08)}
.wz-res-left{flex:1}
.wz-res-db{font-size:11px;font-weight:700;letter-spacing:.4px;
  text-transform:uppercase;margin-bottom:3px}
.wz-res-label{font-size:13px;font-weight:600;color:var(--onyx);margin-bottom:4px}
.wz-res-note{font-size:12px;color:var(--g3);line-height:1.5}
.wz-go{background:var(--plum);color:#fff;border:none;border-radius:6px;
  padding:8px 16px;font-size:12px;font-weight:700;cursor:pointer;
  white-space:nowrap;transition:opacity .15s;align-self:center}
.wz-go:hover{opacity:.85}
.wz-none{color:var(--g3);font-size:14px;padding:32px 0;text-align:center}
.wz-res-title{font-size:12px;color:var(--g3);margin-bottom:12px;font-weight:600}
.hazus-attr{text-align:center;padding:10px 24px;font-size:11px;color:#5A5660}
</style></head><body>
<div class="toast" id="toast"></div>
<div class="topbar">
  <div class="brand">Vulnerability <span>Explorer</span></div>
    <div class="nav-tabs">
    <a class="nav-tab" href="index.html">About</a>
    <button class="nav-tab" onclick="show('wizard',this)" data-tab="wizard">Curve Finder</button>
    <div class="nav-sep"></div>
    <button class="nav-tab active" onclick="show('flood',this)" data-tab="flood">Flood Vulnerability</button>
    <button class="nav-tab" onclick="show('wind',this)" data-tab="wind">Wind Vulnerability</button>
    <button class="nav-tab" onclick="show('eq',this)" data-tab="eq">Earthquake Fragility</button>
    <div class="nav-sep"></div>
    <button class="nav-tab" onclick="show('gem',this)" data-tab="gem">GEM Global EQ</button>
    <button class="nav-tab" onclick="show('esrm',this)" data-tab="esrm">ESRM20 Europe EQ</button>
    <button class="nav-tab" onclick="show('jrc',this)" data-tab="jrc">JRC Global Flood</button>
    <button class="nav-tab" onclick="show('etris',this)" data-tab="etris">ETRiS Tsunami</button>
    <button class="nav-tab" onclick="show('ci',this)" data-tab="ci">Critical Infrastructure</button>
  </div>
</div>
''')
    parts.append('''
<div id="page-wizard" class="page">
  <div class="page-title">Curve Finder</div>
  <div class="page-sub">Answer the questions below to find matching vulnerability and fragility functions. Click any result to open that database tab directly.</div>

  <div class="wz-section" id="wz-s1">
    <div class="wz-section-label">Step 1 &mdash; Select peril</div>
    <div class="wz-peril-grid">
      <button class="wz-peril-btn" id="wz-p-flood"      onclick="wzSelectPeril('Flood')">Flood</button>
      <button class="wz-peril-btn" id="wz-p-earthquake" onclick="wzSelectPeril('Earthquake')">Earthquake</button>
      <button class="wz-peril-btn" id="wz-p-wind"       onclick="wzSelectPeril('Wind')">Wind</button>
      <button class="wz-peril-btn" id="wz-p-tsunami"    onclick="wzSelectPeril('Tsunami')">Tsunami</button>
      <button class="wz-peril-btn" id="wz-p-landslide"  onclick="wzSelectPeril('Landslide')">Landslide</button>
    </div>
  </div>

  <div class="wz-section" id="wz-s2" style="display:none">
    <div class="wz-section-label">Step 2 &mdash; Occupancy</div>
    <select class="wz-select" id="wz-occ" onchange="wzPickOcc()">
      <option value="">Select occupancy...</option>
    </select>
  </div>

  <div class="wz-section" id="wz-s3" style="display:none">
    <div class="wz-section-label">Step 3 &mdash; Structural type</div>
    <select class="wz-select" id="wz-struct" onchange="wzPickStruct()">
      <option value="">Select structural type...</option>
    </select>
  </div>

  <div class="wz-section" id="wz-s4" style="display:none">
    <div class="wz-section-label">Step 4 &mdash; Height class</div>
    <select class="wz-select" id="wz-height" onchange="wzPickHeight()">
      <option value="">Select height...</option>
    </select>
  </div>

  <div style="margin-bottom:16px" id="wz-s2" style="display:none">
    <button class="reset-btn" onclick="wzReset()">Start over</button>
  </div>

  <div id="wz-results" style="display:none"></div>
</div>''')


    # ── FLOOD ──
    parts.append('''
<div id="page-flood" class="page active">
  <div class="page-title">Flood Vulnerability</div>
  <div class="page-sub">Hazus 6.1 &mdash; depth-damage vulnerability functions. Damage ratio (0 to 1) vs flood depth. Source: FEMA Hazus 6.1.</div>
  <div class="filters">
    <div class="fg"><label>Category</label><div class="hint">Broad building use type</div>
      <select id="fl-cat" onchange="flFilter()">
        <option value="">All categories</option>
        <option value="Residential">Residential</option><option value="Commercial">Commercial</option>
        <option value="Industrial">Industrial</option><option value="Agricultural">Agricultural</option>
        <option value="Government">Government</option><option value="Education">Education</option>
        <option value="Religion">Religion</option>
      </select></div>
    <div class="fg"><label>Occupancy code</label><div class="hint">Specific building subtype</div>
      <select id="fl-occ" onchange="flFilter()"><option value="">All occupancies</option></select></div>
    <div class="fg"><label>Damage type</label><div class="hint">What is being damaged</div>
      <select id="fl-dtype" onchange="flFilter()">
        <option value="">All types</option>
        <option value="structure">Structure (building fabric)</option>
        <option value="contents">Contents (furniture / equipment)</option>
        <option value="inventory">Inventory (commercial stock)</option>
      </select></div>
    <div class="fg"><label>Function ID (FnID)</label><div class="hint">Unique Hazus curve identifier</div>
      <select id="fl-fnid" onchange="flDraw()"></select></div>
    <div class="fg" style="justify-content:flex-end;padding-top:20px">
      <span class="match-count" id="fl-match"></span>
      <button class="reset-btn" onclick="flReset()">Reset filters</button>
    </div>
  </div>
  <div class="cmp-section">
    <label class="cmp-toggle" id="fl-cmp-lbl">
      <input type="checkbox" id="fl-cmp-chk" onchange="flCmpToggle()">
      Compare mode &mdash; overlay a second function on the chart
    </label>
    <div class="cmp2-wrap" id="fl-cmp2-wrap">
      <div class="cmp2-label"><span class="cmp2-badge">2</span>Curve 2 &mdash; independent selection</div>
      <div class="cmp2-grid">
        <div class="fg"><label>Category</label><div class="hint">Broad building use type</div>
          <select id="fl-cat2" onchange="flFilter2()">
            <option value="">All categories</option>
            <option value="Residential">Residential</option><option value="Commercial">Commercial</option>
            <option value="Industrial">Industrial</option><option value="Agricultural">Agricultural</option>
            <option value="Government">Government</option><option value="Education">Education</option>
            <option value="Religion">Religion</option>
          </select></div>
        <div class="fg"><label>Occupancy code</label><div class="hint">Specific building subtype</div>
          <select id="fl-occ2" onchange="flFilter2()"><option value="">All occupancies</option></select></div>
        <div class="fg"><label>Damage type</label><div class="hint">What is being damaged</div>
          <select id="fl-dtype2" onchange="flFilter2()">
            <option value="">All types</option>
            <option value="structure">Structure (building fabric)</option>
            <option value="contents">Contents (furniture / equipment)</option>
            <option value="inventory">Inventory (commercial stock)</option>
          </select></div>
        <div class="fg"><label>Function ID (FnID)</label><div class="hint">Unique Hazus curve identifier</div>
          <select id="fl-fnid2" onchange="flDraw2()"></select></div>
      </div>
    </div>
  </div>
  <div class="grid">
    <div class="card">
      <div class="card-hdr">
        <div class="card-title" id="fl-ct">Select a function ID to display</div>
        <div class="card-sub" id="fl-cs"></div>
      </div>
      <div class="card-body">
        <div class="unit-switch" style="margin-bottom:14px">
          <button class="us-btn active" onclick="flUnit('m',this)">Metres</button>
          <button class="us-btn" onclick="flUnit('ft',this)">Feet</button>
        </div>
        <div class="chart-wrap"><canvas id="fl-c"></canvas></div>
        <span id="fl-title" style="display:none"></span>
      </div>
      <div class="cmp-legend" id="fl-cmp-leg" style="display:none"></div>
    </div>
    <div>
      <div class="card" style="margin-bottom:14px"><div class="meta-grid" id="fl-meta"></div></div>
      <div class="card">
        <div class="tbl-tabs" id="fl-tbl-tabs" style="display:none">
          <button class="tbl-tab active" onclick="flShowTbl(1,this)"><span class="dot" style="background:#7F35B2"></span>Curve 1</button>
          <button class="tbl-tab" onclick="flShowTbl(2,this)"><span class="dot" style="background:#c900ac"></span>Curve 2</button>
        </div>
        <div class="tbl-hdr-row">
          <span class="tbl-label">Data values</span>
          <div class="btn-row">
            <button class="icon-btn" onclick="exportPNG('fl-c','fl-title')">Save chart</button>
            <button class="copy-btn" id="fl-copy" onclick="flCopy()">Copy data</button>
          </div>
        </div>
        <div class="tbl-wrap"><table>
          <thead id="fl-thead"><tr><th>Depth (m)</th><th>Depth (ft)</th><th>Damage ratio</th><th>Damage (%)</th></tr></thead>
          <tbody id="fl-tbody"></tbody>
        </table></div>
      </div>
    </div>
  </div>
</div>''')

    # ── WIND ──
    parts.append('''
<div id="page-wind" class="page">
  <div class="page-title">Wind Vulnerability</div>
  <div class="page-sub">Hazus 6.1 &mdash; 39 specific building types. Damage ratio vs wind speed. Native: 3-second peak gust at 10 m, open terrain. 1-minute derived using factor 1.28.</div>
  <div class="filters">
    <div class="fg"><label>Material</label><div class="hint">Construction material</div>
      <select id="wi-mat" onchange="wiFilter()"><option value="">All materials</option></select></div>
    <div class="fg"><label>Occupancy</label><div class="hint">Building use category</div>
      <select id="wi-occ" onchange="wiFilter()"><option value="">All occupancies</option></select></div>
    <div class="fg"><label>Height</label><div class="hint">Number of storeys</div>
      <select id="wi-ht" onchange="wiFilter()"><option value="">All heights</option></select></div>
    <div class="fg"><label>Building type (SBT)</label><div class="hint">Specific building type code</div>
      <select id="wi-sbt" onchange="wiDraw()"></select></div>
    <div class="fg"><label>Damage type</label><div class="hint">What is being damaged</div>
      <select id="wi-dtype" onchange="wiDraw()">
        <option value="structure">Structure (building fabric)</option>
        <option value="contents">Contents (furniture / equipment)</option>
        <option value="downtime">Downtime (business interruption)</option>
      </select></div>
    <div class="fg" style="justify-content:flex-end;padding-top:20px">
      <span class="match-count" id="wi-match"></span>
      <button class="reset-btn" onclick="wiReset()">Reset filters</button>
    </div>
  </div>
  <div class="cmp-section">
    <label class="cmp-toggle" id="wi-cmp-lbl">
      <input type="checkbox" id="wi-cmp-chk" onchange="wiCmpToggle()">
      Compare mode &mdash; overlay a second function on the chart
    </label>
    <div class="cmp2-wrap" id="wi-cmp2-wrap">
      <div class="cmp2-label"><span class="cmp2-badge">2</span>Curve 2 &mdash; independent selection</div>
      <div class="cmp2-grid">
        <div class="fg"><label>Material</label><div class="hint">Construction material</div>
          <select id="wi-mat2" onchange="wiFilter2()"><option value="">All materials</option></select></div>
        <div class="fg"><label>Occupancy</label><div class="hint">Building use category</div>
          <select id="wi-occ2" onchange="wiFilter2()"><option value="">All occupancies</option></select></div>
        <div class="fg"><label>Height</label><div class="hint">Number of storeys</div>
          <select id="wi-ht2" onchange="wiFilter2()"><option value="">All heights</option></select></div>
        <div class="fg"><label>Building type (SBT)</label><div class="hint">Specific building type code</div>
          <select id="wi-sbt2" onchange="wiDraw2()"></select></div>
        <div class="fg"><label>Damage type</label><div class="hint">What is being damaged</div>
          <select id="wi-dtype2" onchange="wiDraw2()">
            <option value="structure">Structure (building fabric)</option>
            <option value="contents">Contents (furniture / equipment)</option>
            <option value="downtime">Downtime (business interruption)</option>
          </select></div>
      </div>
    </div>
  </div>
  <div class="grid">
    <div class="card">
      <div class="card-hdr">
        <div class="card-title" id="wi-ct">Select a building type to display</div>
        <div class="card-sub" id="wi-cs"></div>
      </div>
      <div class="card-body">
        <div class="wind-unit-row">
          <span class="wlabel">Averaging period</span>
          <div class="unit-switch" id="wi-avg-sw">
            <button class="us-btn active" onclick="wiAvg('3s',this)">3-second gust</button>
            <button class="us-btn" onclick="wiAvg('1min',this)">1-minute sustained</button>
          </div>
          <span class="wlabel">Unit</span>
          <div class="unit-switch" id="wi-spd-sw">
            <button class="us-btn active" onclick="wiSpd('ms',this)">m/s</button>
            <button class="us-btn" onclick="wiSpd('kmh',this)">km/h</button>
            <button class="us-btn" onclick="wiSpd('mph',this)">mph</button>
          </div>
        </div>
        <div class="chart-wrap"><canvas id="wi-c"></canvas></div>
        <span id="wi-title" style="display:none"></span>
      </div>
      <div class="cmp-legend" id="wi-cmp-leg" style="display:none"></div>
    </div>
    <div>
      <div class="card" style="margin-bottom:14px"><div class="meta-grid" id="wi-meta"></div></div>
      <div class="card">
        <div class="tbl-tabs" id="wi-tbl-tabs" style="display:none">
          <button class="tbl-tab active" onclick="wiShowTbl(1,this)"><span class="dot" style="background:#48086F"></span>Curve 1</button>
          <button class="tbl-tab" onclick="wiShowTbl(2,this)"><span class="dot" style="background:#c900ac"></span>Curve 2</button>
        </div>
        <div class="tbl-hdr-row">
          <span class="tbl-label">Data values</span>
          <div class="btn-row">
            <button class="icon-btn" onclick="exportPNG('wi-c','wi-title')">Save chart</button>
            <button class="copy-btn" id="wi-copy" onclick="wiCopy()">Copy data</button>
          </div>
        </div>
        <div class="tbl-wrap"><table>
          <thead id="wi-thead"><tr><th>3-sec gust (m/s)</th><th>1-min (m/s)</th><th>km/h</th><th>mph</th><th>Damage ratio</th><th>Damage (%)</th></tr></thead>
          <tbody id="wi-tbody"></tbody>
        </table></div>
      </div>
    </div>
  </div>
</div>''')

    # ── EARTHQUAKE ──
    parts.append('''
<div id="page-eq" class="page">
  <div class="page-title">Earthquake Fragility</div>
  <div class="page-sub">Hazus-MH &mdash; lognormal fragility vulnerability functions. Probability of reaching each damage state vs PGA. Beta = 0.64. Source: Hazus-MH Technical Manual Table 5.16a-d.</div>
  <div class="filters">
    <div class="fg"><label>Material</label><div class="hint">Construction material</div>
      <select id="eq-mat" onchange="eqFilter()">
        <option value="">All materials</option>
        <option>Wood</option><option>Steel</option><option>Concrete</option>
        <option>Masonry</option><option>Manufactured</option>
      </select></div>
    <div class="fg"><label>Height class</label><div class="hint">Number of storeys</div>
      <select id="eq-ht" onchange="eqFilter()">
        <option value="">All heights</option>
        <option value="Low-Rise">Low-Rise (1-3 storeys)</option>
        <option value="Mid-Rise">Mid-Rise (4-7 storeys)</option>
        <option value="High-Rise">High-Rise (8+ storeys)</option>
        <option value="All">All heights</option>
        <option value="Single">Single storey</option>
      </select></div>
    <div class="fg"><label>Building type</label><div class="hint">Hazus structural classification</div>
      <select id="eq-bldg" onchange="eqDraw()"></select></div>
    <div class="fg"><label>Design level</label><div class="hint">Seismic code era and zone</div>
      <select id="eq-code" onchange="eqDraw()">
        <option value="H">High Code -- post-1975, high seismicity</option>
        <option value="M">Moderate Code -- post-1975, moderate seismicity</option>
        <option value="L">Low Code -- post-1975, low seismicity</option>
        <option value="P">Pre-Code -- pre-1941 or zone 0-1</option>
      </select></div>
    <div class="fg" style="justify-content:flex-end;padding-top:20px">
      <span class="match-count" id="eq-match"></span>
      <button class="reset-btn" onclick="eqReset()">Reset filters</button>
    </div>
  </div>
  <div class="cmp-section">
    <label class="cmp-toggle" id="eq-cmp-lbl">
      <input type="checkbox" id="eq-cmp-chk" onchange="eqCmpToggle()">
      Compare mode &mdash; overlay a second building type on the chart
    </label>
    <div class="cmp2-wrap" id="eq-cmp2-wrap">
      <div class="cmp2-label"><span class="cmp2-badge">2</span>Curve 2 &mdash; independent selection</div>
      <div class="cmp2-grid">
        <div class="fg"><label>Material</label><div class="hint">Construction material</div>
          <select id="eq-mat2" onchange="eqFilter2()">
            <option value="">All materials</option>
            <option>Wood</option><option>Steel</option><option>Concrete</option>
            <option>Masonry</option><option>Manufactured</option>
          </select></div>
        <div class="fg"><label>Height class</label><div class="hint">Number of storeys</div>
          <select id="eq-ht2" onchange="eqFilter2()">
            <option value="">All heights</option>
            <option value="Low-Rise">Low-Rise (1-3 storeys)</option>
            <option value="Mid-Rise">Mid-Rise (4-7 storeys)</option>
            <option value="High-Rise">High-Rise (8+ storeys)</option>
            <option value="All">All heights</option>
            <option value="Single">Single storey</option>
          </select></div>
        <div class="fg"><label>Building type</label><div class="hint">Hazus structural classification</div>
          <select id="eq-bldg2" onchange="eqDraw2()"></select></div>
        <div class="fg"><label>Design level</label><div class="hint">Seismic code era and zone</div>
          <select id="eq-code2" onchange="eqDraw2()">
            <option value="H">High Code -- post-1975, high seismicity</option>
            <option value="M">Moderate Code -- post-1975, moderate seismicity</option>
            <option value="L">Low Code -- post-1975, low seismicity</option>
            <option value="P">Pre-Code -- pre-1941 or zone 0-1</option>
          </select></div>
      </div>
    </div>
  </div>
  <div class="grid">
    <div class="card">
      <div class="card-hdr">
        <div class="card-title" id="eq-ct">Select building type and design level</div>
        <div class="card-sub" id="eq-cs"></div>
      </div>
      <div class="card-body">
        <div class="unit-switch" style="margin-bottom:14px">
          <button class="us-btn active" onclick="eqUnit('g',this)">PGA (g)</button>
          <button class="us-btn" onclick="eqUnit('ms2',this)">PGA (m/s&#178;)</button>
        </div>
        <div class="chart-wrap"><canvas id="eq-c"></canvas></div>
        <span id="eq-title" style="display:none"></span>
      </div>
      <div class="legend-row" id="eq-leg"></div>
      <div class="cmp-legend" id="eq-cmp-leg" style="display:none"></div>
    </div>
    <div>
      <div class="card" style="margin-bottom:14px"><div class="meta-grid" id="eq-meta"></div></div>
      <div class="card">
        <div class="tbl-tabs" id="eq-tbl-tabs" style="display:none">
          <button class="tbl-tab active" onclick="eqShowTbl(1,this)"><span class="dot" style="background:#48086F"></span>Curve 1</button>
          <button class="tbl-tab" onclick="eqShowTbl(2,this)"><span class="dot" style="background:#c900ac"></span>Curve 2</button>
        </div>
        <div class="tbl-hdr-row">
          <span class="tbl-label">Data values</span>
          <div class="btn-row">
            <button class="icon-btn" onclick="exportPNG('eq-c','eq-title')">Save chart</button>
            <button class="copy-btn" id="eq-copy" onclick="eqCopy()">Copy data</button>
          </div>
        </div>
        <div class="tbl-wrap"><table>
          <thead id="eq-thead"><tr><th>PGA (g)</th><th>PGA (m/s&#178;)</th><th>Slight</th><th>Moderate</th><th>Extensive</th><th>Complete</th></tr></thead>
          <tbody id="eq-tbody"></tbody>
        </table></div>
      </div>
    </div>
  </div>
</div>''')

    parts.append('''
<div id="page-gem" class="page">
  <div class="page-title">GEM Global Earthquake Vulnerability Functions</div>
  <div class="page-sub">Global Earthquake Model Foundation &mdash; 54,940 functions across 215 countries. PGA vs mean loss ratio. Licence: CC BY-NC-SA 4.0. Cite: Martins &amp; Silva (2023).</div>
  <div class="filters">
    <div class="fg"><label>Region</label><div class="hint">World region</div>
      <select id="gem-region" onchange="gemOnRegion()"><option value="">All regions</option></select></div>
    <div class="fg"><label>Country</label><div class="hint">Filter by country</div>
      <select id="gem-country" onchange="gemOnCountry()"><option value="">All countries</option></select></div>
    <div class="fg"><label>Material</label><div class="hint">Construction material</div>
      <select id="gem-mat" onchange="gemOnMat()"><option value="">All materials</option></select></div>
    <div class="fg"><label>Occupancy</label><div class="hint">Building use</div>
      <select id="gem-occ" onchange="gemFilter()"><option value="">All occupancies</option></select></div>
    <div class="fg"><label>Loss type</label><div class="hint">Damage component</div>
      <select id="gem-lt" onchange="gemFilter()">
        <option value="structural">Structural</option>
        <option value="contents">Contents</option>
      </select></div>
    <div class="fg"><label>Search functions</label><div class="hint">Type taxonomy, country or material</div>
      <input id="gem-search" type="text" placeholder="e.g. CR Italy structural"
        style="width:100%;padding:7px 10px;border:1px solid var(--border);border-radius:6px;
               font-size:13px;color:var(--onyx);background:var(--bg)"
        oninput="gemSearch(this.value)"></div>
    <div class="fg" style="justify-content:flex-end;padding-top:20px">
      <span class="match-count" id="gem-match"></span>
      <button class="reset-btn" onclick="gemReset()">Reset filters</button>
    </div>
  </div>
  <div style="padding:0 0 16px 0">
    <label style="font-size:11px;font-weight:700;color:var(--g3);letter-spacing:.5px;text-transform:uppercase">
      Function <span id="gem-match-inline" style="font-weight:400;text-transform:none"></span>
    </label>
    <select id="gem-func" onchange="gemDraw()"
      style="width:100%;margin-top:4px;padding:6px 8px;border:1px solid var(--border);
             border-radius:6px;font-size:12px;font-family:inherit;color:var(--onyx);
             background:var(--bg);height:140px" size="8"></select>
  </div>
  <div class="cmp-section">
    <label class="cmp-toggle" id="gem-cmp-lbl">
      <input type="checkbox" id="gem-cmp-chk" onchange="gemCmpToggle()">
      Compare mode &mdash; overlay a second function on the chart
    </label>
    <div class="cmp2-wrap" id="gem-cmp2-wrap">
      <div class="cmp2-label"><span class="cmp2-badge">2</span>Curve 2 &mdash; independent selection</div>
      <div class="cmp2-grid">
        <div class="fg"><label>Region</label><div class="hint">World region</div>
          <select id="gem-region2" onchange="gemOnRegion2()"><option value="">All regions</option></select></div>
        <div class="fg"><label>Country</label><div class="hint">Filter by country</div>
          <select id="gem-country2" onchange="gemOnCountry2()"><option value="">All countries</option></select></div>
        <div class="fg"><label>Material</label><div class="hint">Construction material</div>
          <select id="gem-mat2" onchange="gemOnMat2()"><option value="">All materials</option></select></div>
        <div class="fg"><label>Occupancy</label><div class="hint">Building use</div>
          <select id="gem-occ2" onchange="gemFilter2()">
            <option value="">All occupancies</option>
            <option value="Residential">Residential</option>
            <option value="Commercial">Commercial</option>
            <option value="Industrial">Industrial</option>
          </select></div>
        <div class="fg"><label>Loss type</label><div class="hint">Damage component</div>
          <select id="gem-lt2" onchange="gemFilter2()">
            <option value="structural">Structural</option>
            <option value="contents">Contents</option>
          </select></div>
        <div class="fg"><label>Function</label><div class="hint">Type to search taxonomy</div>
          <input id="gem-search2" type="text" placeholder="Search taxonomy..."
            style="width:100%;padding:6px 10px;border:1px solid var(--border);border-radius:6px;
                   font-size:13px;color:var(--onyx);background:var(--bg);margin-bottom:4px"
            oninput="gemSearch2(this.value)">
          <select id="gem-func2" onchange="gemDraw2()" size="4"
            style="width:100%;height:auto;min-height:60px"></select></div>
      </div>
    </div>
  </div>
  <div class="grid">
    <div class="card">
      <div class="card-hdr"><div class="card-title" id="gem-ct">Select a function</div>
        <div class="card-sub" id="gem-cs"></div></div>
      <div class="card-body">
        <div class="unit-switch" style="margin-bottom:14px">
          <button class="us-btn active" onclick="gemUnit('g',this)">PGA (g)</button>
          <button class="us-btn" onclick="gemUnit('ms2',this)">PGA (m/s&#178;)</button>
        </div>
        <div class="chart-wrap"><canvas id="gem-c"></canvas></div>
      </div>
    </div>
    <div>
      <div class="card" style="margin-bottom:14px"><div class="meta-grid" id="gem-meta" style="grid-template-columns:repeat(auto-fill,minmax(160px,1fr))"></div></div>
      <div class="card">
        <div class="cmp-legend" id="gem-cmp-leg" style="display:none"></div>
        <div class="tbl-tabs" id="gem-tbl-tabs" style="display:none">
          <button class="tbl-tab active" onclick="gemShowTbl(1,this)"><span class="dot" style="background:#0D7377"></span>Curve 1</button>
          <button class="tbl-tab" onclick="gemShowTbl(2,this)"><span class="dot" style="background:#c900ac"></span>Curve 2</button>
        </div>
        <div class="tbl-hdr-row"><span class="tbl-label">Data values</span>
          <div class="btn-row">
            <button class="icon-btn" onclick="exportPNG('gem-c','gem-ct')">Save chart</button>
            <button class="copy-btn" id="gem-copy" onclick="gemCopy()">Copy data</button>
          </div></div>
        <div class="tbl-wrap"><table>
          <thead id="gem-thead"><tr><th>PGA (g)</th><th>PGA (m/s&#178;)</th><th>Mean loss ratio</th><th>Loss (%)</th></tr></thead>
          <tbody id="gem-tbody"></tbody>
        </table></div>
      </div>
    </div>
  </div>
</div>''')

    parts.append('''
<div id="page-jrc" class="page">
  <div class="page-title">JRC Global Flood Depth-Damage Functions</div>
  <div class="page-sub">EU Joint Research Centre &mdash; globally consistent depth-damage curves for 6 continents and 5 asset classes. Cite: Huizinga et al. (2017), EUR 28552 EN.</div>
  <div class="filters">
    <div class="fg"><label>Asset class</label><div class="hint">Type of asset</div>
      <select id="jrc-asset" onchange="jrcDraw()"></select></div>
    <div class="fg"><label>Continent</label><div class="hint">Geographic region</div>
      <select id="jrc-continent" onchange="jrcDraw()"></select></div>
    <div class="fg" style="justify-content:flex-end;padding-top:20px">
      <span class="match-count" id="jrc-match"></span>
    </div>
  </div>
  <div class="cmp-section">
    <label class="cmp-toggle" id="jrc-cmp-lbl">
      <input type="checkbox" id="jrc-cmp-chk" onchange="jrcCmpToggle()">
      Compare mode &mdash; overlay a second function on the chart
    </label>
    <div class="cmp2-wrap" id="jrc-cmp2-wrap">
      <div class="cmp2-label"><span class="cmp2-badge">2</span>Curve 2 &mdash; independent selection</div>
      <div class="cmp2-grid">
        <div class="fg"><label>Asset class</label><div class="hint">Type of asset</div>
          <select id="jrc-asset2" onchange="jrcDraw2()"></select></div>
        <div class="fg"><label>Continent</label><div class="hint">Geographic region</div>
          <select id="jrc-continent2" onchange="jrcDraw2()"></select></div>
      </div>
    </div>
  </div>
  <div class="grid">
    <div class="card">
      <div class="card-hdr"><div class="card-title" id="jrc-ct">Select asset class and continent</div>
        <div class="card-sub" id="jrc-cs"></div></div>
      <div class="card-body">
        <div class="unit-switch" style="margin-bottom:14px">
          <button class="us-btn active" onclick="jrcUnit('m',this)">Metres</button>
          <button class="us-btn" onclick="jrcUnit('ft',this)">Feet</button>
        </div>
        <div class="chart-wrap"><canvas id="jrc-c"></canvas></div>
      </div>
    </div>
    <div>
      <div class="card" style="margin-bottom:14px"><div class="meta-grid" id="jrc-meta"></div></div>
      <div class="card">
        <div class="cmp-legend" id="jrc-cmp-leg" style="display:none"></div>
        <div class="tbl-tabs" id="jrc-tbl-tabs" style="display:none">
          <button class="tbl-tab active" onclick="jrcShowTbl(1,this)"><span class="dot" style="background:#0369A1"></span>Curve 1</button>
          <button class="tbl-tab" onclick="jrcShowTbl(2,this)"><span class="dot" style="background:#c900ac"></span>Curve 2</button>
        </div>
        <div class="tbl-hdr-row"><span class="tbl-label">Data values</span>
          <div class="btn-row">
            <button class="icon-btn" onclick="exportPNG('jrc-c','jrc-ct')">Save chart</button>
            <button class="copy-btn" id="jrc-copy" onclick="jrcCopy()">Copy data</button>
          </div></div>
        <div class="tbl-wrap"><table>
          <thead id="jrc-thead"><tr><th>Depth (m)</th><th>Depth (ft)</th><th>Mean damage ratio</th><th>Damage (%)</th></tr></thead>
          <tbody id="jrc-tbody"></tbody>
        </table></div>
      </div>
    </div>
  </div>
</div>''')

    parts.append('''
<div id="page-etris" class="page">
  <div class="page-title">ETRiS Tsunami Vulnerability Curves</div>
  <div class="page-sub">European Tsunami Risk Service &mdash; 165 empirical vulnerability curves from 6 historical tsunami events. Flow depth vs damage ratio with 16th, median and 84th percentile bands. Licence: CC BY 4.0. Cite: Jalayer et al. (2023).</div>
  <div class="filters">
    <div class="fg"><label>Event</label><div class="hint">Tsunami event</div>
      <select id="etris-event" onchange="etrisEventChange()"></select></div>
    <div class="fg"><label>Building type</label><div class="hint">Structural classification</div>
      <select id="etris-bldg" onchange="etrisRender()"></select></div>
    <div class="fg"><label>Model</label><div class="hint">Regression fit (3 models per curve)</div>
      <select id="etris-model" onchange="etrisRender()">
        <option value="M1">M1</option>
        <option value="M2" selected>M2</option>
        <option value="M3">M3</option>
      </select></div>
    <div class="fg" style="justify-content:flex-end;padding-top:20px">
      <span class="match-count" id="etris-match"></span>
      <button class="reset-btn" onclick="etrisReset()">Reset filters</button>
    </div>
  </div>
  <div class="cmp-section">
    <label class="cmp-toggle" id="etris-cmp-lbl">
      <input type="checkbox" id="etris-cmp-chk" onchange="etrisCmpToggle()">
      Compare mode &mdash; overlay a second function on the chart
    </label>
    <div class="cmp2-wrap" id="etris-cmp2-wrap">
      <div class="cmp2-label"><span class="cmp2-badge">2</span>Curve 2 &mdash; independent selection</div>
      <div class="cmp2-grid">
        <div class="fg"><label>Event</label><div class="hint">Tsunami event</div>
          <select id="etris-event2" onchange="etrisEventChange2()"></select></div>
        <div class="fg"><label>Building type</label><div class="hint">Structural classification</div>
          <select id="etris-bldg2" onchange="etrisRender2()"></select></div>
        <div class="fg"><label>Model</label><div class="hint">Regression fit</div>
          <select id="etris-model2" onchange="etrisRender2()">
            <option value="M1">M1</option>
            <option value="M2" selected>M2</option>
            <option value="M3">M3</option>
          </select></div>
      </div>
    </div>
  </div>
  <div class="grid">
    <div class="card">
      <div class="card-hdr"><div class="card-title" id="etris-ct">Select an event and building type</div>
        <div class="card-sub" id="etris-cs"></div></div>
      <div class="card-body">
        <div class="unit-switch" style="margin-bottom:14px">
          <button class="us-btn active" onclick="etrisUnit('m',this)">Metres</button>
          <button class="us-btn" onclick="etrisUnit('ft',this)">Feet</button>
        </div>
        <div class="chart-wrap"><canvas id="etris-c"></canvas></div>
      </div>
    </div>
    <div>
      <div class="card" style="margin-bottom:14px"><div class="meta-grid" id="etris-meta" style="grid-template-columns:repeat(auto-fill,minmax(160px,1fr))"></div></div>
      <div class="card">
        <div class="cmp-legend" id="etris-cmp-leg" style="display:none"></div>
        <div class="tbl-tabs" id="etris-tbl-tabs" style="display:none">
          <button class="tbl-tab active" onclick="etrisShowTbl(1,this)"><span class="dot" style="background:#0D7377"></span>Curve 1</button>
          <button class="tbl-tab" onclick="etrisShowTbl(2,this)"><span class="dot" style="background:#c900ac"></span>Curve 2</button>
        </div>
        <div class="tbl-hdr-row"><span class="tbl-label">Data values</span>
          <div class="btn-row">
            <button class="icon-btn" onclick="exportPNG('etris-c','etris-ct')">Save chart</button>
            <button class="copy-btn" id="etris-copy" onclick="etrisCopy()">Copy data</button>
          </div></div>
        <div class="tbl-wrap"><table>
          <thead id="etris-thead"><tr><th>Depth (m)</th><th>Median</th><th>16th pct</th><th>84th pct</th><th>Median (%)</th></tr></thead>
          <tbody id="etris-tbody"></tbody>
        </table></div>
      </div>
    </div>
  </div>
</div>''')

    parts.append('''
<div id="page-esrm" class="page">
  <div class="page-title">ESRM20 European Seismic Fragility Functions</div>
  <div class="page-sub">European Seismic Risk Model 2020 &mdash; 511 lognormal fragility functions for European building typologies. Probability of reaching each damage state vs intensity measure. Licence: CC BY 4.0. Cite: Crowley et al. (2021), EFEHR Technical Report 002.</div>
  <div class="filters">
    <div class="fg"><label>Material</label><div class="hint">Construction material</div>
      <select id="esrm-mat" onchange="esrmFilter()"><option value="">All materials</option></select></div>
    <div class="fg"><label>System</label><div class="hint">Structural system</div>
      <select id="esrm-sys" onchange="esrmFilter()"><option value="">All systems</option></select></div>
    <div class="fg"><label>Height</label><div class="hint">Number of storeys</div>
      <select id="esrm-hgt" onchange="esrmFilter()"><option value="">All heights</option></select></div>
    <div class="fg"><label>Ductility</label><div class="hint">Seismic design ductility class</div>
      <select id="esrm-duc" onchange="esrmFilter()">
        <option value="">All ductility classes</option>
        <option value="High ductility">High ductility</option>
        <option value="Medium ductility">Medium ductility</option>
        <option value="Low ductility">Low ductility</option>
      </select></div>
    <div class="fg"><label>Intensity measure</label><div class="hint">Override recommended IMT</div>
      <select id="esrm-imt" onchange="esrmDraw()">
        <option value="">Recommended (per typology)</option>
        <option value="PGA">PGA</option>
        <option value="SA(0.3)">SA(0.3s)</option>
        <option value="SA(0.6)">SA(0.6s)</option>
        <option value="SA(1.0)">SA(1.0s)</option>
      </select></div>
    <div class="fg"><label>Typology</label><div class="hint">Building typology code</div>
      <select id="esrm-func" onchange="esrmDraw()"></select></div>
    <div class="fg" style="justify-content:flex-end;padding-top:20px">
      <span class="match-count" id="esrm-match"></span>
      <button class="reset-btn" onclick="esrmReset()">Reset filters</button>
    </div>
  </div>
  <div id="esrm-imt-note" style="font-size:12px;color:var(--g3);padding:4px 0 12px 4px"></div>
  <div class="cmp-section">
    <label class="cmp-toggle" id="esrm-cmp-lbl">
      <input type="checkbox" id="esrm-cmp-chk" onchange="esrmCmpToggle()">
      Compare mode &mdash; overlay a second typology on the chart
    </label>
    <div class="cmp2-wrap" id="esrm-cmp2-wrap">
      <div class="cmp2-label"><span class="cmp2-badge">2</span>Curve 2 &mdash; independent selection <span id="esrm-imt2-note" style="font-size:11px;color:#9fc0ff;margin-left:8px;font-weight:400"></span></div>
      <div class="cmp2-grid">
        <div class="fg"><label>Material</label><div class="hint">Construction material</div>
          <select id="esrm-mat2" onchange="esrmFilter2()"><option value="">All materials</option></select></div>
        <div class="fg"><label>System</label><div class="hint">Structural system</div>
          <select id="esrm-sys2" onchange="esrmFilter2()"><option value="">All systems</option></select></div>
        <div class="fg"><label>Height</label><div class="hint">Number of storeys</div>
          <select id="esrm-hgt2" onchange="esrmFilter2()"><option value="">All heights</option></select></div>
        <div class="fg"><label>Ductility</label><div class="hint">Seismic design ductility class</div>
          <select id="esrm-duc2" onchange="esrmFilter2()">
            <option value="">All ductility classes</option>
            <option value="High ductility">High ductility</option>
            <option value="Medium ductility">Medium ductility</option>
            <option value="Low ductility">Low ductility</option>
          </select></div>
        <div class="fg"><label>Typology</label><div class="hint">Building typology code</div>
          <select id="esrm-func2" onchange="esrmDraw2()"></select></div>
      </div>
    </div>
  </div>
  <div class="grid">
    <div class="card">
      <div class="card-hdr">
        <div class="card-title" id="esrm-ct">Select a building typology</div>
        <div class="card-sub" id="esrm-cs"></div>
      </div>
      <div class="card-body">
        <div class="chart-wrap"><canvas id="esrm-c"></canvas></div>
      </div>
      <div class="legend-row" id="esrm-leg"></div>
      <div class="cmp-legend" id="esrm-cmp-leg" style="display:none"></div>
    </div>
    <div>
      <div class="card" style="margin-bottom:14px"><div class="meta-grid" id="esrm-meta" style="grid-template-columns:repeat(auto-fill,minmax(160px,1fr))"></div></div>
      <div class="card">
        <div class="tbl-tabs" id="esrm-tbl-tabs" style="display:none">
          <button class="tbl-tab active" onclick="esrmShowTbl(1,this)"><span class="dot" style="background:#48086F"></span>Curve 1</button>
          <button class="tbl-tab" onclick="esrmShowTbl(2,this)"><span class="dot" style="background:#c900ac"></span>Curve 2</button>
        </div>
        <div class="tbl-hdr-row"><span class="tbl-label">Data values</span>
          <div class="btn-row">
            <button class="icon-btn" onclick="exportPNG('esrm-c','esrm-ct')">Save chart</button>
            <button class="copy-btn" id="esrm-copy" onclick="esrmCopy()">Copy data</button>
          </div></div>
        <div class="tbl-wrap"><table>
          <thead id="esrm-thead"><tr><th>IM</th><th>Slight</th><th>Moderate</th><th>Extensive</th><th>Complete</th></tr></thead>
          <tbody id="esrm-tbody"></tbody>
        </table></div>
      </div>
    </div>
  </div>
</div>''')

    parts.append('''
<div id="page-ci" class="page">
  <div class="page-title">Critical Infrastructure Vulnerability</div>
  <div class="page-sub">Nirandjan et al. (2024) &mdash; 594 fragility and vulnerability curves for energy, transport, water, waste, telecom and health &amp; education infrastructure. Covering flood, earthquake, wind and landslide hazards. Licence: CC BY 4.0.</div>
  <div class="filters">
    <div class="fg"><label>Hazard</label><div class="hint">Natural hazard type</div>
      <select id="ci-hazard" onchange="ciOnHazard()"><option value="">All hazards</option></select></div>
    <div class="fg"><label>CI system</label><div class="hint">Infrastructure sector</div>
      <select id="ci-system" onchange="ciOnSystem()"><option value="">All CI systems</option></select></div>
    <div class="fg"><label>Asset type</label><div class="hint">Infrastructure asset</div>
      <select id="ci-asset" onchange="ciOnAsset()"><option value="">All asset types</option></select></div>
    <div class="fg"><label>Curve</label><div class="hint">Select specific curve</div>
      <select id="ci-func" onchange="ciDraw()"></select></div>
    <div class="fg" style="justify-content:flex-end;padding-top:20px">
      <span class="match-count" id="ci-match"></span>
      <button class="reset-btn" onclick="ciReset()">Reset filters</button>
    </div>
  </div>
  <div id="ci-im-note" style="font-size:12px;color:var(--g3);padding:4px 0 12px 4px"></div>
  <div class="cmp-section">
    <label class="cmp-toggle" id="ci-cmp-lbl">
      <input type="checkbox" id="ci-cmp-chk" onchange="ciCmpToggle()">
      Compare mode &mdash; overlay a second curve on the chart
    </label>
    <div class="cmp2-wrap" id="ci-cmp2-wrap">
      <div class="cmp2-label"><span class="cmp2-badge">2</span>Curve 2 &mdash; independent selection</div>
      <div class="cmp2-grid">
        <div class="fg"><label>Hazard</label><div class="hint">Natural hazard type</div>
          <select id="ci-hazard2" onchange="ciFilter2()"><option value="">All hazards</option></select></div>
        <div class="fg"><label>CI system</label><div class="hint">Infrastructure sector</div>
          <select id="ci-system2" onchange="ciFilter2()"><option value="">All CI systems</option></select></div>
        <div class="fg"><label>Asset type</label><div class="hint">Infrastructure asset</div>
          <select id="ci-asset2" onchange="ciFilter2()"><option value="">All asset types</option></select></div>
        <div class="fg"><label>Curve</label><div class="hint">Select specific curve</div>
          <select id="ci-func2" onchange="ciDraw2()"></select></div>
      </div>
    </div>
  </div>
  <div class="grid">
    <div class="card">
      <div class="card-hdr"><div class="card-title" id="ci-ct">Select a hazard and asset type</div>
        <div class="card-sub" id="ci-cs"></div></div>
      <div class="card-body">
        <div class="unit-switch" id="ci-unit-wrap" style="margin-bottom:14px;display:none">
          <!-- populated dynamically by JS based on hazard -->
        </div>
        <div id="ci-wind-note" style="font-size:11px;color:var(--g3);margin-bottom:8px;display:none">
          Wind speed: 10-minute mean at 10 m above ground (V10m)
        </div>
        <div class="chart-wrap"><canvas id="ci-c"></canvas></div>
        <div class="legend-row" id="ci-ds-leg" style="display:none"></div>
      </div>
    </div>
    <div>
      <div class="card" style="margin-bottom:14px"><div class="meta-grid" id="ci-meta" style="grid-template-columns:repeat(auto-fill,minmax(160px,1fr))"></div></div>
      <div class="card">
        <div class="cmp-legend" id="ci-cmp-leg" style="display:none"></div>
        <div class="tbl-tabs" id="ci-tbl-tabs" style="display:none">
          <button class="tbl-tab active" onclick="ciShowTbl(1,this)"><span class="dot" style="background:#7F35B2"></span>Curve 1</button>
          <button class="tbl-tab" onclick="ciShowTbl(2,this)"><span class="dot" style="background:#c900ac"></span>Curve 2</button>
        </div>
        <div class="tbl-hdr-row"><span class="tbl-label">Data values</span>
          <div class="btn-row">
            <button class="icon-btn" onclick="exportPNG('ci-c','ci-ct')">Save chart</button>
            <button class="copy-btn" id="ci-copy" onclick="ciCopy()">Copy data</button>
          </div></div>
        <div class="tbl-wrap"><table>
          <thead id="ci-thead"><tr><th>IM</th><th>Value</th><th>%</th></tr></thead>
          <tbody id="ci-tbody"></tbody>
        </table></div>
      </div>
    </div>
  </div>
</div>''')

    parts.append('''
<div id="page-wizard" class="page">
  <div class="page-title">Vulnerability Curve Finder</div>
  <div class="page-sub">Select your hazard, asset type and region to find the most appropriate vulnerability functions available in this tool.</div>

  <div class="filters" style="margin-bottom:0">
    <div class="fg">
      <label>1. Peril</label>
      <div class="hint">Natural hazard type</div>
      <select id="wiz-peril" onchange="wizStep1()">
        <option value="">Select a peril...</option>
        <option value="Flood">Flood</option>
        <option value="Earthquake">Earthquake</option>
        <option value="Wind">Wind</option>
        <option value="Tsunami">Tsunami</option>
        <option value="Landslide">Landslide</option>
      </select>
    </div>
    <div class="fg" id="wiz-asset-wrap" style="opacity:.4;pointer-events:none">
      <label>2. Asset class</label>
      <div class="hint">Type of exposed asset</div>
      <select id="wiz-asset" onchange="wizStep2()">
        <option value="">Select asset class...</option>
      </select>
    </div>
    <div class="fg" id="wiz-region-wrap" style="opacity:.4;pointer-events:none">
      <label>3. Region</label>
      <div class="hint">Geographic area of interest</div>
      <select id="wiz-region" onchange="wizStep3()">
        <option value="">Select region...</option>
      </select>
    </div>
  </div>

  <div id="wiz-results" style="margin-top:24px"></div>
</div>''')

    parts.append('''
<footer class="hazus-attr">
  <p>Powered by FEMA HAZUS 6.1 (public domain)</p>
</footer>''')

    # Data injection

    # All JS as a raw string - no f-string brace issues
    data_script = (
        '\n<script>\nconst FLOOD=' + flood_json +
        ';\nconst WIND='  + wind_json  +
        ';\nconst EQ='    + eq_json    +
        ';\nconst GEM='   + gem_json   +
        ';\nconst JRC='   + jrc_json   +
        ';\nconst GEM_PGA=' + gem_pga_json + ';\nconst ETRIS=' + etris_json + ';\nconst ESRM=' + esrm_json + ';\nconst CI=' + ci_json + ';\nfunction metaEl(el,items){return meta(el,items);}\n</script>'
    )

    js_block = (
        '\n<script>\n' +
        get_utils_js() + '\n' +
        get_flood_js() + '\n' +
        get_wind_js()  + '\n' +
        get_eq_js()    + '\n' +
        get_gem_js()   + '\n' +
        get_jrc_js()   + '\n' +
        get_etris_js()   + '\n' +
        get_esrm_js()  + '\n' +
        get_ci_js()    + '\n' +
        get_wizard_js() +
        '\n</script>\n</body>\n</html>'
    )

    return ''.join(parts) + data_script + js_block
