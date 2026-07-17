def get_flood_js():
    return r"""
/* ===== FLOOD CURVE 1 ===== */
(function(){
  var occs=[...new Set(FLOOD.map(function(r){return r.occupancy.trim();}))].filter(Boolean).sort();
  var os=document.getElementById('fl-occ');
  occs.forEach(function(o){var d=OCC[o]||'';os.add(new Option(d?o+' \u2014 '+d:o,o));});
  flFilter();
})();

function flFilter(){
  var occ=document.getElementById('fl-occ').value;
  var cat=document.getElementById('fl-cat').value;
  var dt=document.getElementById('fl-dtype').value;
  var f=FLOOD.filter(function(r){
    var ro=r.occupancy.trim(),rc=r.category.trim();
    var cm=!cat||rc===cat||rc.toLowerCase().indexOf(cat.toLowerCase().slice(0,4))>=0;
    return(!occ||ro===occ)&&cm&&(!dt||r.damage_type===dt);
  });
  var ids=[...new Set(f.map(function(r){return r.fn_id;}))].sort(function(a,b){return +a-+b;});
  var sel=document.getElementById('fl-fnid');
  sel.innerHTML='';
  ids.forEach(function(i){sel.add(new Option(i,i));});
  var mc=document.getElementById('fl-match');if(mc)mc.textContent=ids.length+' function'+(ids.length===1?'':'s')+' match';
  if(ids.length)flDraw();
}

function flReset(){
  document.getElementById('fl-cat').value='';
  document.getElementById('fl-occ').value='';
  document.getElementById('fl-dtype').value='';
  flFilter();
}

function flUnit(u,btn){
  flUM=u;
  document.querySelectorAll('#page-flood .unit-switch .us-btn').forEach(function(b){b.classList.remove('active');});
  btn.classList.add('active');
  flRenderChart();
}

function flFillTbl(row){
  document.getElementById('fl-tbody').innerHTML=row.depth_m.map(function(x,i){
    return '<tr><td>'+x.toFixed(2)+'</td><td>'+(x/0.3048).toFixed(2)+'</td><td>'+
      row.damage[i].toFixed(4)+'</td><td>'+(row.damage[i]*100).toFixed(2)+'%</td></tr>';
  }).join('');
}

function flDraw(){
  var fnid=document.getElementById('fl-fnid').value;
  var dt=document.getElementById('fl-dtype').value;
  var row=FLOOD.find(function(r){return String(r.fn_id)===String(fnid)&&(!dt||r.damage_type===dt);});
  if(!row)return;
  flR1=row;
  var occ=row.occupancy.trim(),desc=OCC[occ]||'';
  var flTitle='FnID '+row.fn_id+' \u2014 '+row.damage_type+' \u2014 '+occ+(desc?' ('+desc+')':'');
  document.getElementById('fl-ct').textContent=flTitle;
  document.getElementById('fl-title').textContent=flTitle;
  document.getElementById('fl-cs').textContent=row.description;
  meta(document.getElementById('fl-meta'),[
    ['Function ID',String(row.fn_id)],['Damage type',row.damage_type],
    ['Occupancy code',occ],['Occupancy',desc||'\u2014'],
    ['Source',row.source],['Flood types',row.flood_types]]);
  flFillTbl(flTC===2&&flR2?flR2:flR1);
  flRenderChart();
}

function flRenderChart(){
  if(!flR1)return;
  var ft=flUM==='ft';
  var labels=flR1.depth_m.map(function(x){return ft?(x/0.3048).toFixed(1):x.toFixed(2);});
  var ds=[{label:'C1',data:flR1.damage,borderColor:C1F,
    backgroundColor:flCmp&&flR2?'transparent':'rgba(13,148,136,.08)',
    borderWidth:2.5,pointRadius:0,pointBackgroundColor:C1F,tension:.3,fill:!(flCmp&&flR2)}];
  if(flCmp&&flR2){
    ds.push({label:'C2',data:flR2.damage,borderColor:C2,
      backgroundColor:'transparent',borderWidth:2.5,pointRadius:0,pointBackgroundColor:C2,tension:.3,fill:false});
  }
  flChart=mkChart('fl-c',labels,ds,ft?'Flood depth (ft)':'Flood depth (m)','Damage ratio',flChart);
  var leg=document.getElementById('fl-cmp-leg');
  if(flCmp&&flR1&&flR2){
    leg.style.display='flex';
    leg.innerHTML='<div class="cl-item"><div class="cl-dot" style="background:'+C1F+'"></div>Curve 1: FnID '+flR1.fn_id+' \u2014 '+flR1.occupancy.trim()+' \u2014 '+flR1.damage_type+'</div>'+
      '<div class="cl-item"><div class="cl-dot" style="background:'+C2+'"></div>Curve 2: FnID '+flR2.fn_id+' \u2014 '+flR2.occupancy.trim()+' \u2014 '+flR2.damage_type+'</div>';
  }else{leg.style.display='none';}
}

/* ===== FLOOD CURVE 2 (completely independent) ===== */
function flCmpToggle(){
  flCmp=document.getElementById('fl-cmp-chk').checked;
  document.getElementById('fl-cmp-lbl').classList.toggle('on',flCmp);
  document.getElementById('fl-cmp2-wrap').style.display=flCmp?'block':'none';
  document.getElementById('fl-tbl-tabs').style.display='none';
  if(!flCmp){flR2=null;flRenderChart();}
  else{flFilter2();}
}

function flFilter2(){
  var occ=document.getElementById('fl-occ2').value;
  var cat=document.getElementById('fl-cat2').value;
  var dt=document.getElementById('fl-dtype2').value;
  var occs=[...new Set(FLOOD.map(function(r){return r.occupancy.trim();}))].filter(Boolean).sort();
  var os=document.getElementById('fl-occ2');
  var co=os.value;
  os.innerHTML='<option value="">All occupancies</option>';
  occs.forEach(function(o){var d=OCC[o]||'';os.add(new Option(d?o+' \u2014 '+d:o,o));});
  if(occs.indexOf(co)>=0)os.value=co;
  var f=FLOOD.filter(function(r){
    var ro=r.occupancy.trim(),rc=r.category.trim();
    var cm=!cat||rc===cat||rc.toLowerCase().indexOf(cat.toLowerCase().slice(0,4))>=0;
    return(!occ||ro===occ)&&cm&&(!dt||r.damage_type===dt);
  });
  var ids=[...new Set(f.map(function(r){return r.fn_id;}))].sort(function(a,b){return +a-+b;});
  var sel2=document.getElementById('fl-fnid2');
  sel2.innerHTML='';
  ids.forEach(function(i){sel2.add(new Option(i,i));});
  if(ids.length)flDraw2();
}

function flDraw2(){
  var fnid2=document.getElementById('fl-fnid2').value;
  var dt=document.getElementById('fl-dtype2').value;
  if(!fnid2){flR2=null;document.getElementById('fl-tbl-tabs').style.display='none';flRenderChart();return;}
  var row=FLOOD.find(function(r){return String(r.fn_id)===String(fnid2)&&(!dt||r.damage_type===dt);});
  if(!row&&dt){row=FLOOD.find(function(r){return String(r.fn_id)===String(fnid2);});}
  flR2=row||null;
  document.getElementById('fl-tbl-tabs').style.display=flR2?'flex':'none';
  flRenderChart();
}

function flShowTbl(n,btn){
  flTC=n;
  document.querySelectorAll('#fl-tbl-tabs .tbl-tab').forEach(function(b){b.classList.remove('active');});
  btn.classList.add('active');
  var r=n===1?flR1:flR2;if(r)flFillTbl(r);
}

function flCopy(){
  if(flCmp&&flR1&&flR2){
    var hdr='Flood Vulnerability Function Comparison - Hazus 6.1\nCurve 1: FnID '+flR1.fn_id+' \u2014 '+flR1.occupancy.trim()+' \u2014 '+flR1.damage_type+'\nCurve 2: FnID '+flR2.fn_id+' \u2014 '+flR2.occupancy.trim()+' \u2014 '+flR2.damage_type;
    var hRow='Depth (m)\tDepth (ft)\tC1 Damage ratio\tC1 Damage (%)\tC2 Damage ratio\tC2 Damage (%)';
    var rows=flR1.depth_m.map(function(x,i){
      var c2=flR2.damage[i]!=null?flR2.damage[i]:null;
      return x.toFixed(2)+'\t'+(x/0.3048).toFixed(2)+'\t'+flR1.damage[i].toFixed(4)+'\t'+(flR1.damage[i]*100).toFixed(2)+'%\t'+(c2!=null?c2.toFixed(4):'-')+'\t'+(c2!=null?(c2*100).toFixed(2)+'%':'-');
    }).join('\n');
    copyText(hdr+'\n\n'+hRow+'\n'+rows,'fl-copy');
  }else if(flR1){
    var h=[...document.getElementById('fl-thead').querySelectorAll('th')].map(function(t){return t.textContent.trim();}).join('\t');
    var r=[...document.getElementById('fl-tbody').querySelectorAll('tr')].map(function(r){return [...r.querySelectorAll('td')].map(function(c){return c.textContent.trim();}).join('\t');}).join('\n');
    copyText('Flood Vulnerability Function - Hazus 6.1\nSelection: '+document.getElementById('fl-ct').textContent+'\n\n'+h+'\n'+r,'fl-copy');
  }
}
"""
