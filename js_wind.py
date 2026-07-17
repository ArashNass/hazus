def get_wind_js():
    return r"""
/* ===== WIND CURVE 1 ===== */
(function(){
  var mats=[...new Set(WIND.map(function(r){return r.material;}))].filter(Boolean).sort();
  var ms=document.getElementById('wi-mat');
  mats.forEach(function(m){ms.add(new Option(m,m));});
  wiFilter();
})();

function wiFilter(){
  var mat=document.getElementById('wi-mat').value;
  var occ=document.getElementById('wi-occ').value;
  var ht=document.getElementById('wi-ht').value;
  var dt=document.getElementById('wi-dtype').value;
  var f=WIND.filter(function(r){return(!mat||r.material===mat)&&(!occ||r.occupancy===occ)&&(!ht||r.height===ht)&&r.damage_type===dt;});
  var occs=[...new Set(f.map(function(r){return r.occupancy;}))].filter(Boolean).sort();
  var hts=[...new Set(f.map(function(r){return r.height;}))].filter(Boolean).sort();
  var os=document.getElementById('wi-occ'),hs=document.getElementById('wi-ht');
  var co=os.value,ch=hs.value;
  os.innerHTML='<option value="">All occupancies</option>';hs.innerHTML='<option value="">All heights</option>';
  occs.forEach(function(o){os.add(new Option(o,o));});hts.forEach(function(h){hs.add(new Option(h,h));});
  if(occs.indexOf(co)>=0)os.value=co;if(hts.indexOf(ch)>=0)hs.value=ch;
  var sbts=[...new Set(f.map(function(r){return r.sbt;}))].sort();
  var ss=document.getElementById('wi-sbt');
  var cs=ss.value;ss.innerHTML='';
  sbts.forEach(function(s){var g=(WIND.find(function(r){return r.sbt===s;})||{sbt_group:''}).sbt_group;ss.add(new Option(s+' \u2014 '+g,s));});
  if(sbts.indexOf(cs)>=0)ss.value=cs;
  var mc=document.getElementById('wi-match');if(mc)mc.textContent=sbts.length+' type'+(sbts.length===1?'':'s')+' match';
  if(sbts.length)wiDraw();
}

function wiReset(){
  document.getElementById('wi-mat').value='';
  document.getElementById('wi-occ').value='';
  document.getElementById('wi-ht').value='';
  document.getElementById('wi-dtype').value='structure';
  wiFilter();
}

function wiAvg(m,btn){wiAM=m;document.querySelectorAll('#wi-avg-sw .us-btn').forEach(function(b){b.classList.remove('active');});btn.classList.add('active');wiRenderChart();}
function wiSpd(m,btn){wiSM=m;document.querySelectorAll('#wi-spd-sw .us-btn').forEach(function(b){b.classList.remove('active');});btn.classList.add('active');wiRenderChart();}

function wiFillTbl(row){
  document.getElementById('wi-tbody').innerHTML=row.wind_ms.map(function(x,i){
    return '<tr><td>'+x.toFixed(1)+'</td><td>'+(x/GF).toFixed(1)+'</td><td>'+row.wind_kmh[i].toFixed(0)+'</td><td>'+row.wind_mph[i].toFixed(0)+'</td><td>'+row.damage[i].toFixed(4)+'</td><td>'+(row.damage[i]*100).toFixed(2)+'%</td></tr>';
  }).join('');
}

function wiDraw(){
  var sbt=document.getElementById('wi-sbt').value;
  var dt=document.getElementById('wi-dtype').value;
  var row=WIND.find(function(r){return r.sbt===sbt&&r.damage_type===dt;});
  if(!row)return;
  wiR1=row;
  var wiTitle=row.sbt+' \u2014 '+row.damage_type+' \u2014 '+row.sbt_group;
  document.getElementById('wi-ct').textContent=wiTitle;
  document.getElementById('wi-title').textContent=wiTitle;
  document.getElementById('wi-cs').textContent=row.description+'  |  3-second peak gust, 10 m, open terrain';
  meta(document.getElementById('wi-meta'),[
    ['SBT Code',row.sbt],['Damage type',row.damage_type],['Material',row.material],
    ['Occupancy',row.occupancy],['Height',row.height],['Wind speed basis','3-sec gust, 10 m, open terrain']]);
  wiFillTbl(wiTC===2&&wiR2?wiR2:wiR1);
  wiRenderChart();
}

function wiRenderChart(){
  if(!wiR1)return;
  var u1=wiAM==='1min';
  var labs,xT;
  if(wiSM==='kmh'){labs=wiR1.wind_ms.map(function(x){return u1?((x/GF)*3.6).toFixed(0):(x*3.6).toFixed(0);});xT=(u1?'1-minute sustained':'3-second peak gust')+' wind speed (km/h)';}
  else if(wiSM==='mph'){labs=wiR1.wind_ms.map(function(x){return u1?((x/GF)*2.237).toFixed(0):(x*2.237).toFixed(0);});xT=(u1?'1-minute sustained':'3-second peak gust')+' wind speed (mph)';}
  else{labs=wiR1.wind_ms.map(function(x){return u1?(x/GF).toFixed(1):x.toFixed(0);});xT=(u1?'1-minute sustained':'3-second peak gust')+' wind speed (m/s)';}
  var ds=[{label:'C1',data:wiR1.damage,borderColor:C1W,
    backgroundColor:wiCmp&&wiR2?'transparent':'rgba(15,118,110,.08)',
    borderWidth:2.5,pointRadius:0,pointBackgroundColor:C1W,tension:.3,fill:!(wiCmp&&wiR2)}];
  if(wiCmp&&wiR2){
    ds.push({label:'C2',data:wiR2.damage,borderColor:C2,
      backgroundColor:'transparent',borderWidth:2.5,pointRadius:0,pointBackgroundColor:C2,tension:.3,fill:false});
  }
  wiChart=mkChart('wi-c',labs,ds,xT,'Damage ratio',wiChart);
  var leg=document.getElementById('wi-cmp-leg');
  if(wiCmp&&wiR1&&wiR2){
    leg.style.display='flex';
    leg.innerHTML='<div class="cl-item"><div class="cl-dot" style="background:'+C1W+'"></div>Curve 1: '+wiR1.sbt+' \u2014 '+wiR1.damage_type+'</div>'+
      '<div class="cl-item"><div class="cl-dot" style="background:'+C2+'"></div>Curve 2: '+wiR2.sbt+' \u2014 '+wiR2.damage_type+'</div>';
  }else{leg.style.display='none';}
}

/* ===== WIND CURVE 2 (completely independent) ===== */
function wiCmpToggle(){
  wiCmp=document.getElementById('wi-cmp-chk').checked;
  document.getElementById('wi-cmp-lbl').classList.toggle('on',wiCmp);
  document.getElementById('wi-cmp2-wrap').style.display=wiCmp?'block':'none';
  document.getElementById('wi-tbl-tabs').style.display='none';
  if(!wiCmp){wiR2=null;wiRenderChart();}
  else{
    var mats=[...new Set(WIND.map(function(r){return r.material;}))].filter(Boolean).sort();
    var ms=document.getElementById('wi-mat2');
    if(ms.options.length<=1){mats.forEach(function(m){ms.add(new Option(m,m));});}
    wiFilter2();
  }
}

function wiFilter2(){
  var mat=document.getElementById('wi-mat2').value;
  var occ=document.getElementById('wi-occ2').value;
  var ht=document.getElementById('wi-ht2').value;
  var dt=document.getElementById('wi-dtype2').value||'structure';
  var f=WIND.filter(function(r){return(!mat||r.material===mat)&&(!occ||r.occupancy===occ)&&(!ht||r.height===ht)&&r.damage_type===dt;});
  var occs=[...new Set(f.map(function(r){return r.occupancy;}))].filter(Boolean).sort();
  var hts=[...new Set(f.map(function(r){return r.height;}))].filter(Boolean).sort();
  var os=document.getElementById('wi-occ2'),hs=document.getElementById('wi-ht2');
  var co=os.value,ch=hs.value;
  os.innerHTML='<option value="">All occupancies</option>';hs.innerHTML='<option value="">All heights</option>';
  occs.forEach(function(o){os.add(new Option(o,o));});hts.forEach(function(h){hs.add(new Option(h,h));});
  if(occs.indexOf(co)>=0)os.value=co;if(hts.indexOf(ch)>=0)hs.value=ch;
  var sbts=[...new Set(f.map(function(r){return r.sbt;}))].sort();
  var ss=document.getElementById('wi-sbt2');
  var cs=ss.value;ss.innerHTML='';
  sbts.forEach(function(s){var g=(WIND.find(function(r){return r.sbt===s;})||{sbt_group:''}).sbt_group;ss.add(new Option(s+' \u2014 '+g,s));});
  if(sbts.indexOf(cs)>=0)ss.value=cs;
  if(sbts.length)wiDraw2();
}

function wiDraw2(){
  var sbt2=document.getElementById('wi-sbt2').value;
  var dt=document.getElementById('wi-dtype2').value||'structure';
  if(!sbt2){wiR2=null;document.getElementById('wi-tbl-tabs').style.display='none';wiRenderChart();return;}
  var row=WIND.find(function(r){return r.sbt===sbt2&&r.damage_type===dt;});
  wiR2=row||null;
  document.getElementById('wi-tbl-tabs').style.display=wiR2?'flex':'none';
  wiRenderChart();
}

function wiShowTbl(n,btn){
  wiTC=n;
  document.querySelectorAll('#wi-tbl-tabs .tbl-tab').forEach(function(b){b.classList.remove('active');});
  btn.classList.add('active');
  var r=n===1?wiR1:wiR2;if(r)wiFillTbl(r);
}

function wiCopy(){
  if(wiCmp&&wiR1&&wiR2){
    var hdr='Wind Vulnerability Function Comparison - Hazus 6.1\n3-second peak gust at 10 m, open terrain\nCurve 1: '+wiR1.sbt+' \u2014 '+wiR1.sbt_group+' \u2014 '+wiR1.damage_type+'\nCurve 2: '+wiR2.sbt+' \u2014 '+wiR2.sbt_group+' \u2014 '+wiR2.damage_type;
    var hRow='3-sec gust (m/s)\t1-min (m/s)\tkm/h\tmph\tC1 Damage ratio\tC1 Damage (%)\tC2 Damage ratio\tC2 Damage (%)';
    var rows=wiR1.wind_ms.map(function(x,i){
      var c2=wiR2.damage[i]!=null?wiR2.damage[i]:null;
      return x.toFixed(1)+'\t'+(x/GF).toFixed(1)+'\t'+wiR1.wind_kmh[i].toFixed(0)+'\t'+wiR1.wind_mph[i].toFixed(0)+'\t'+wiR1.damage[i].toFixed(4)+'\t'+(wiR1.damage[i]*100).toFixed(2)+'%\t'+(c2!=null?c2.toFixed(4):'-')+'\t'+(c2!=null?(c2*100).toFixed(2)+'%':'-');
    }).join('\n');
    copyText(hdr+'\n\n'+hRow+'\n'+rows,'wi-copy');
  }else if(wiR1){
    var h=[...document.getElementById('wi-thead').querySelectorAll('th')].map(function(t){return t.textContent.trim();}).join('\t');
    var r=[...document.getElementById('wi-tbody').querySelectorAll('tr')].map(function(r){return [...r.querySelectorAll('td')].map(function(c){return c.textContent.trim();}).join('\t');}).join('\n');
    copyText('Wind Vulnerability Function - Hazus 6.1\n3-second peak gust at 10 m, open terrain\nSelection: '+document.getElementById('wi-ct').textContent+'\n\n'+h+'\n'+r,'wi-copy');
  }
}
"""
