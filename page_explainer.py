"""
page_explainer.py — generates index.html (About / landing page)
"""

def build_explainer() -> str:
    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vulnerability Function Explorer — About</title>
<meta name="description" content="Browse, compare and export building vulnerability functions from HAZUS, GEM, JRC and ETRiS. Flood, wind, earthquake and tsunami. Free, interactive.">
<meta name="keywords" content="HAZUS vulnerability functions, depth damage functions, fragility curves, catastrophe modelling, GEM global vulnerability, JRC flood, ETRiS tsunami, FEMA HAZUS, insurance risk">
<meta name="author" content="Arash Nassirpour">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --wtw:#7F35B2;--deep:#48086F;--light:#F3EAF9;--mid:#C89FDC;
  --onyx:#2F2C31;--g2:#5A5660;--g3:#949096;
  --bg:#fff;--bg2:#F8F5FB;--border:#DDD5E8;
}
html{scroll-behavior:smooth}
body{font-family:'Inter',sans-serif;background:var(--bg);color:var(--onyx);-webkit-font-smoothing:antialiased}

/* NAV */
.topbar{background:#48086F;padding:0 32px;display:flex;align-items:center;
        height:58px;position:sticky;top:0;z-index:100;
        box-shadow:0 1px 0 rgba(255,255,255,.08),0 4px 16px rgba(0,0,0,.3);overflow-x:auto}
.brand{font-size:14px;font-weight:700;color:#fff;letter-spacing:-.3px;margin-right:28px;white-space:nowrap;flex-shrink:0}
.brand span{color:#C89FDC}
.nav-tabs{display:flex;height:100%;align-items:center;gap:2px;flex:1}
.nav-tab{padding:0 18px;font-size:14px;font-weight:500;border:none;background:none;color:rgba(255,255,255,.55);cursor:pointer;border-bottom:3px solid transparent;transition:color .2s,border-color .2s;height:100%;white-space:nowrap;text-decoration:none;display:inline-flex;align-items:center;border-radius:0}
.nav-tab:hover{color:rgba(255,255,255,.9);background:rgba(255,255,255,.04)}
.nav-tab.active{color:#fff;border-bottom-color:#C89FDC;background:none;font-weight:600}
.nav-sep{width:1px;height:18px;background:rgba(255,255,255,.15);margin:0 4px;flex-shrink:0}

/* HERO */
.hero{background:linear-gradient(150deg,#48086F 0%,#1a0535 100%);
      padding:64px 32px 56px;text-align:center}
.hero h1{font-size:clamp(32px,5vw,52px);font-weight:800;color:#fff;
         line-height:1.15;letter-spacing:-1px;margin-bottom:16px}
.hero h1 span{color:#C89FDC}
.hero p{font-size:16px;color:rgba(255,255,255,.65);max-width:580px;
        margin:0 auto;line-height:1.65}

/* PAGE — same max-width and padding as dashboard */
.page{max-width:1440px;margin:0 auto;padding:28px 32px 80px}

h2{font-size:20px;font-weight:700;color:var(--deep);margin:48px 0 16px;letter-spacing:-.3px}
h2:first-of-type{margin-top:0}
p{font-size:15px;color:var(--g2);line-height:1.7;margin-bottom:16px}

/* SOURCE CARDS — 4 columns to match dashboard layout */
.sources{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin:24px 0}
.src{background:var(--bg2);border:1px solid var(--border);border-radius:10px;
     padding:20px;border-top:3px solid}
.src.hazus{border-top-color:#7F35B2}
.src.gem{border-top-color:#0D7377}
.src.jrc{border-top-color:#0369A1}
.src.etris{border-top-color:#0D9488}
.src-label{font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px}
.src.hazus .src-label{color:#7F35B2}
.src.gem   .src-label{color:#0D7377}
.src.jrc   .src-label{color:#0369A1}
.src.etris .src-label{color:#0D9488}
.src h3{font-size:14px;font-weight:700;color:var(--deep);margin-bottom:8px}
.src p{font-size:13px;color:var(--g2);margin-bottom:10px;line-height:1.55}
.src-meta{font-size:11px;color:var(--g3)}
.src-meta span{display:block;margin-top:2px}

/* FEATURE TILES */
.features{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin:24px 0}
.feat{background:var(--bg2);border:1px solid var(--border);border-radius:8px;
      padding:14px 16px;font-size:14px;color:var(--g2);display:flex;gap:10px;align-items:flex-start}
.feat svg{flex-shrink:0;margin-top:2px}
.feat strong{color:var(--onyx);display:block;margin-bottom:3px;font-size:13px}

/* FAQ */
.faq{margin:24px 0;display:grid;gap:2px}
.faq-item{background:var(--bg2);border:1px solid var(--border);border-radius:8px;overflow:hidden}
.faq-q{width:100%;text-align:left;font-size:14px;font-weight:600;color:var(--deep);
       padding:14px 18px;background:none;border:none;cursor:pointer;
       display:flex;justify-content:space-between;align-items:center;gap:12px}
.faq-q:hover{background:var(--light)}
.faq-a{font-size:13px;color:var(--g2);line-height:1.65;padding:0 18px 14px;display:none}
.faq-a.open{display:block}
.arr{transition:transform .2s;color:var(--wtw);flex-shrink:0}
.arr.open{transform:rotate(180deg)}

footer{text-align:center;padding:28px 32px 24px;font-size:12px;color:#5A5660;border-top:1px solid var(--border);margin-top:40px}

@media(max-width:900px){
  .sources{grid-template-columns:repeat(2,1fr)}
  .page{padding:24px 20px 60px}
}
@media(max-width:600px){
  .sources{grid-template-columns:1fr}
  .topbar{padding:0 16px}
  .features{grid-template-columns:1fr}
}
</style>
</head>
<body>

<div class="topbar">
  <div class="brand">Vulnerability <span>Explorer</span></div>
    <div class="nav-tabs">
    <a class="nav-tab active" href="index.html">About</a>
    <a class="nav-tab" href="HAZUS_Dashboard.html?tab=wizard">Curve Finder</a>
    <div class="nav-sep"></div>
    <a class="nav-tab" href="HAZUS_Dashboard.html?tab=flood">HAZUS Flood</a>
    <a class="nav-tab" href="HAZUS_Dashboard.html?tab=wind">HAZUS Wind</a>
    <a class="nav-tab" href="HAZUS_Dashboard.html?tab=eq">HAZUS Earthquake</a>
    <div class="nav-sep"></div>
    <a class="nav-tab" href="HAZUS_Dashboard.html?tab=gem">GEM Global EQ</a>
    <a class="nav-tab" href="HAZUS_Dashboard.html?tab=esrm">ESRM20 Europe EQ</a>
    <a class="nav-tab" href="HAZUS_Dashboard.html?tab=jrc">JRC Global Flood</a>
    <a class="nav-tab" href="HAZUS_Dashboard.html?tab=etris">ETRiS Tsunami</a>
    <a class="nav-tab" href="HAZUS_Dashboard.html?tab=ci">Critical Infrastructure</a>
  </div>
</div>

<div class="hero">
  <h1>Vulnerability Function<br><span>Explorer</span></h1>
  <p>A vulnerability function converts hazard intensity into a damage ratio &mdash; the economic engine of every catastrophe model. This tool gives direct access to six open-source databases covering flood, wind, earthquake, tsunami, European seismic risk and critical infrastructure.</p>
</div>

<div class="page">

<h2>Data sources</h2>
<div class="sources">
  <div class="src hazus">
    <div class="src-label">HAZUS</div>
    <h3>FEMA Hazus 6.1</h3>
    <p>US standard for natural hazard loss estimation. Depth-damage functions for flood, damage functions for wind and hurricane, and lognormal fragility curves for earthquake.</p>
    <div class="src-meta">
      <span>Flood &middot; Wind &middot; Earthquake</span>
      <span>Public domain (FEMA)</span>
    </div>
  </div>
  <div class="src gem">
    <div class="src-label">GEM</div>
    <h3>Global Earthquake Model</h3>
    <p>Analytically derived vulnerability functions covering 3,500+ building typologies across 215 countries. The most comprehensive open global earthquake vulnerability dataset available.</p>
    <div class="src-meta">
      <span>Global earthquake &middot; 215 countries</span>
      <span>CC BY-NC-SA 4.0 &middot; Martins &amp; Silva (2023)</span>
    </div>
  </div>
  <div class="src esrm" style="border-top-color:#7C3AED">
    <div class="src-label" style="color:#7C3AED">ESRM20</div>
    <h3>European Seismic Risk Model 2020</h3>
    <p>Lognormal fragility functions for 511 European building typologies. Four damage states (Slight, Moderate, Extensive, Complete) with the recommended intensity measure per typology.</p>
    <div class="src-meta">
      <span>European earthquake &middot; 511 typologies</span>
      <span>CC BY 4.0 &middot; Crowley et al. (2021)</span>
    </div>
  </div>
  <div class="src jrc">
    <div class="src-label">JRC</div>
    <h3>EU Joint Research Centre</h3>
    <p>Globally consistent flood depth-damage curves for 5 asset classes across 6 continents. The standard reference for pan-European and global flood risk assessment.</p>
    <div class="src-meta">
      <span>Global flood &middot; 6 continents</span>
      <span>CC BY 4.0 &middot; Huizinga et al. (2017)</span>
    </div>
  </div>
  <div class="src etris">
    <div class="src-label">ETRiS</div>
    <h3>European Tsunami Risk Service</h3>
    <p>Empirical vulnerability curves from six historical tsunami events including Japan 2011, Sri Lanka 2004, Chile 2010 and Sulawesi 2018. Three regression fits with percentile bands.</p>
    <div class="src-meta">
      <span>Tsunami &middot; 6 events</span>
      <span>CC BY 4.0 &middot; Jalayer et al. (2023)</span>
    </div>
  </div>
  <div class="src" style="border-top-color:#B45309">
    <div class="src-label" style="color:#B45309">CI VULNERABILITY</div>
    <h3>Critical Infrastructure (Nirandjan 2024)</h3>
    <p>Fragility and vulnerability curves for energy, transport, water, waste, telecom and health &amp; education infrastructure across flood, earthquake, wind and landslide hazards. Covers 594 base curves with uncertainty bands.</p>
    <div class="src-meta">
      <span>594 curves &middot; 4 hazards &middot; 6 CI sectors</span>
      <span>CC BY 4.0 &middot; Nirandjan et al. (2024), NHESS</span>
    </div>
  </div>
</div>

<h2>What you can do</h2>
<div class="features">
  <div class="feat">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#7F35B2" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
    <div><strong>Filter and browse</strong>Narrow functions by material, occupancy, country, design level and loss type.</div>
  </div>
  <div class="feat">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#7F35B2" stroke-width="2.5"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
    <div><strong>Compare two curves</strong>Overlay any two functions on the same chart with fully independent filter sets.</div>
  </div>
  <div class="feat">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#7F35B2" stroke-width="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
    <div><strong>Export chart as PNG</strong>Download any chart with the selection title, ready for reports.</div>
  </div>
  <div class="feat">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#7F35B2" stroke-width="2.5"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
    <div><strong>Copy data</strong>Copy the full data table to clipboard. In compare mode both curves are included side by side.</div>
  </div>
  <div class="feat">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#7F35B2" stroke-width="2.5"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
    <div><strong>Switch units</strong>Flood depth in m or ft, wind speed in m/s, km/h or mph, PGA in g or m/s&sup2;.</div>
  </div>
  <div class="feat">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#7F35B2" stroke-width="2.5"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
    <div><strong>Browser-based</strong>Runs entirely in your browser. No software installation or account required.</div>
  </div>
</div>

<h2>Frequently asked questions</h2>
<div class="faq">
  <div class="faq-item">
    <button class="faq-q" onclick="toggle(this)">What is a vulnerability function?
      <svg class="arr" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
    </button>
    <div class="faq-a">A mathematical relationship between hazard intensity (depth, speed, acceleration) and damage ratio, the fraction of a building\'s replacement value that is destroyed. Vulnerability functions are the economic engine of every catastrophe model.</div>
  </div>
  <div class="faq-item">
    <button class="faq-q" onclick="toggle(this)">What is the difference between a vulnerability function and a fragility curve?
      <svg class="arr" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
    </button>
    <div class="faq-a">A vulnerability function gives the mean damage ratio at each intensity level, used for flood and wind. A fragility curve gives the probability of reaching or exceeding a damage state threshold, used for earthquake. Both types are in this tool.</div>
  </div>
  <div class="faq-item">
    <button class="faq-q" onclick="toggle(this)">Can I use HAZUS functions outside the US?
      <svg class="arr" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
    </button>
    <div class="faq-a">With caution. HAZUS was calibrated on US construction stock. For international applications the GEM earthquake functions covering 215 countries and JRC flood functions covering 6 continents are more appropriate starting points.</div>
  </div>
  <div class="faq-item">
    <button class="faq-q" onclick="toggle(this)">What wind speed convention does HAZUS use?
      <svg class="arr" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
    </button>
    <div class="faq-a">3-second peak gust at 10 m above ground in open terrain. The tool also shows 1-minute sustained speeds and converts to km/h and mph automatically.</div>
  </div>
</div>

</div>

<footer>
  <p>&copy; 2026 Arash Nassirpour. All rights reserved.</p>
  <p style="margin-top:6px;font-size:11px;opacity:.6">
    FEMA HAZUS 6.1 (public domain) &middot;
    GEM Global Vulnerability Model, Martins &amp; Silva (2023) (CC BY-NC-SA 4.0) &middot;
    JRC Global Flood Depth-Damage Functions, Huizinga et al. (2017) (CC BY 4.0) &middot;
    ETRiS Tsunami Vulnerability Curves, Jalayer et al. (2023) (CC BY 4.0) &middot;
    CI Physical Vulnerability Database, Nirandjan et al. (2024) (CC BY 4.0) &middot;
    ESRM20, Crowley et al. (2021) (CC BY 4.0)
  </p>
</footer>

<script>
function toggle(btn){
  var a=btn.nextElementSibling;
  var arr=btn.querySelector(\'.arr\');
  var open=a.classList.contains(\'open\');
  document.querySelectorAll(\'.faq-a\').forEach(function(el){el.classList.remove(\'open\');});
  document.querySelectorAll(\'.arr\').forEach(function(el){el.classList.remove(\'open\');});
  if(!open){a.classList.add(\'open\');arr.classList.add(\'open\');}
}
</script>
</body>
</html>'''
