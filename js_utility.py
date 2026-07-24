def get_utility_js():
    return r"""
/* ===== HAZUS UTILITY FRAGILITY ===== */
function utilNormCDF(x){
  var a1=0.254829592,a2=-0.284496736,a3=1.421413741,a4=-1.453152027,a5=1.061405429,p=0.3275911;
  var sign=x<0?-1:1,ax=Math.abs(x)/Math.SQRT2,t=1/(1+p*ax);
  var poly=t*(a1+t*(a2+t*(a3+t*(a4+t*a5))));
  return 0.5*(1+sign*(1-poly*Math.exp(-ax*ax)));
}
function utilFrag(pga,med,beta){
  return (pga<=0||med<=0||beta<=0)?0:utilNormCDF(Math.log(pga/med)/beta);
}
function utilGetById(id){return UTIL.find(function(r){return r.id===id;})||null;}
function utilStateColor(name){
  if(name==='Slight') return WC.slight;
  if(name==='Moderate') return WC.moderate;
  if(name==='Extensive') return WC.extensive;
  if(name==='Complete') return WC.complete;
  return '#7c3aed';
}
function utilChoiceLabel(r){
  return r.code+' — '+r.facility+' ('+r.anchoring+', '+r.size+')';
}
function utilFillSelect(id,rows,current){
  var sel=document.getElementById(id);sel.innerHTML='';
  rows.forEach(function(r){sel.add(new Option(utilChoiceLabel(r),r.id));});
  if(current&&rows.some(function(r){return r.id===current;})) sel.value=current;
}
function utilFilter(){
  var sys=document.getElementById('util-system').value;
  var fac=document.getElementById('util-facility').value;
  var anc=document.getElementById('util-anchoring').value;
  var rows=UTIL.filter(function(r){
    return (!sys||r.system===sys)&&(!fac||r.facility===fac)&&(!anc||r.anchoring===anc);
  });
  var cur=document.getElementById('util-curve').value;
  utilFillSelect('util-curve',rows,cur);
  var mc=document.getElementById('util-match');if(mc)mc.textContent=rows.length+' curve'+(rows.length===1?'':'s')+' match';
  utilDraw();
}
function utilReset(){
  document.getElementById('util-system').value='';
  document.getElementById('util-facility').value='';
  document.getElementById('util-anchoring').value='';
  utilFilter();
}
function utilUnit(u,btn){
  utilUM=u;
  document.querySelectorAll('#page-util .unit-switch .us-btn').forEach(function(b){b.classList.remove('active');});
  btn.classList.add('active');
  utilRenderChart();
}
function utilPgaSeries(rec){
  var maxMed=Math.max.apply(null,rec.states.map(function(s){return s.median_g;}));
  var maxX=Math.min(3.0,Math.max(1.5,maxMed*2.2));
  var xs=[];for(var x=0;x<=maxX+1e-9;x+=0.01) xs.push(parseFloat(x.toFixed(3)));
  return xs;
}
function utilBuildRow(pga,states){
  var cols=states.map(function(s){
    return '<td>'+(utilFrag(pga,s.median_g,s.beta)*100).toFixed(1)+'%</td>';
  }).join('');
  return '<tr><td>'+pga.toFixed(2)+'</td><td>'+(pga*G).toFixed(3)+'</td>'+cols+'</tr>';
}
function utilFillTbl(rec){
  var thead=document.getElementById('util-thead');
  var h='<tr><th>PGA (g)</th><th>PGA (m/s&#178;)</th>'+rec.states.map(function(s){return '<th>'+s.name+'</th>';}).join('')+'</tr>';
  thead.innerHTML=h;
  var rows=utilPgaSeries(rec).map(function(p){return utilBuildRow(p,rec.states);}).join('');
  document.getElementById('util-tbody').innerHTML=rows;
}
function utilMetaRows(rec){
  var items=[['System',rec.system],['Facility',rec.facility],['Code',rec.code],['Table',rec.table],['Size',rec.size],['Anchoring',rec.anchoring]];
  rec.states.forEach(function(s){
    items.push([s.name+' median',s.median_g.toFixed(2)+' g / '+(s.median_g*G).toFixed(2)+' m/s²']);
    items.push([s.name+' beta',s.beta.toFixed(2)]);
  });
  return items;
}
function utilDraw(){
  var id=document.getElementById('util-curve').value;
  var rec=utilGetById(id);if(!rec)return;
  utilR1=id;
  var title=rec.facility+' — '+rec.code+' — '+rec.anchoring;
  document.getElementById('util-ct').textContent=title;
  document.getElementById('util-cs').textContent=rec.system+' | '+rec.size+' | Table '+rec.table;
  document.getElementById('util-title').textContent=title;
  meta(document.getElementById('util-meta'),utilMetaRows(rec));
  utilFillTbl(utilTC===2&&utilR2?utilGetById(utilR2)||rec:rec);
  utilRenderChart();
}
function utilRenderChart(){
  if(!utilR1) return;
  var r1=utilGetById(utilR1);if(!r1) return;
  var xs=utilPgaSeries(r1),ms2=utilUM==='ms2';
  var labels=xs.map(function(p){return ms2?(p*G).toFixed(2):p.toFixed(3);});
  var datasets=r1.states.map(function(s){
    return{label:s.name,data:xs.map(function(p){return parseFloat(utilFrag(p,s.median_g,s.beta).toFixed(5));}),
      borderColor:utilStateColor(s.name),backgroundColor:'transparent',borderWidth:2.5,pointRadius:0,tension:0,borderDash:[]};
  });
  if(utilCmp&&utilR2){
    var r2=utilGetById(utilR2);
    if(r2){
      r2.states.forEach(function(s){
        datasets.push({label:s.name+' C2',data:xs.map(function(p){return parseFloat(utilFrag(p,s.median_g,s.beta).toFixed(5));}),
          borderColor:utilStateColor(s.name),backgroundColor:'transparent',borderWidth:1.5,pointRadius:0,tension:0,borderDash:[6,3]});
      });
    }
  }
  utilChart=mkChart('util-c',labels,datasets,
    ms2?'Peak ground acceleration (m/s²)':'Peak ground acceleration (g)',
    'Probability of reaching damage state',utilChart);

  document.getElementById('util-leg').innerHTML=r1.states.map(function(s){
    return '<div class="li"><div class="ld" style="background:'+utilStateColor(s.name)+'"></div>'+s.name+
      ' — median '+s.median_g.toFixed(2)+' g, β='+s.beta.toFixed(2)+'</div>';
  }).join('');

  var cmpLeg=document.getElementById('util-cmp-leg');
  if(utilCmp&&utilR2){
    var r2=utilGetById(utilR2);
    if(r2){
      cmpLeg.style.display='flex';
      cmpLeg.innerHTML='<div class="cl-item"><div class="cl-dot" style="background:'+WC.slight+'"></div>Curve 1 (solid): '+r1.code+' — '+r1.anchoring+'</div>'+
                       '<div class="cl-item"><div class="cl-dot" style="background:'+WC.slight+';opacity:.5"></div>Curve 2 (dashed): '+r2.code+' — '+r2.anchoring+'</div>';
      return;
    }
  }
  cmpLeg.style.display='none';
}
function utilCmpToggle(){
  utilCmp=document.getElementById('util-cmp-chk').checked;
  document.getElementById('util-cmp-lbl').classList.toggle('on',utilCmp);
  document.getElementById('util-cmp2-wrap').style.display=utilCmp?'block':'none';
  document.getElementById('util-tbl-tabs').style.display='none';
  if(!utilCmp){utilR2=null;utilRenderChart();}
  else{utilFilter2();}
}
function utilFilter2(){
  var sys=document.getElementById('util-system2').value;
  var fac=document.getElementById('util-facility2').value;
  var anc=document.getElementById('util-anchoring2').value;
  var rows=UTIL.filter(function(r){
    return (!sys||r.system===sys)&&(!fac||r.facility===fac)&&(!anc||r.anchoring===anc);
  });
  var cur=document.getElementById('util-curve2').value;
  utilFillSelect('util-curve2',rows,cur);
  if(rows.length) utilDraw2();
}
function utilDraw2(){
  var id=document.getElementById('util-curve2').value;
  if(!id){utilR2=null;document.getElementById('util-tbl-tabs').style.display='none';utilRenderChart();return;}
  utilR2=id;
  document.getElementById('util-tbl-tabs').style.display='flex';
  utilRenderChart();
}
function utilShowTbl(n,btn){
  utilTC=n;
  document.querySelectorAll('#util-tbl-tabs .tbl-tab').forEach(function(b){b.classList.remove('active');});
  btn.classList.add('active');
  var id=n===1?utilR1:utilR2;
  var rec=utilGetById(id);if(rec)utilFillTbl(rec);
}
function utilCopy(){
  var h=[...document.getElementById('util-thead').querySelectorAll('th')].map(function(t){return t.textContent.trim();}).join('\t');
  var r=[...document.getElementById('util-tbody').querySelectorAll('tr')].map(function(row){
    return [...row.querySelectorAll('td')].map(function(c){return c.textContent.trim();}).join('\t');
  }).join('\n');
  copyText('Hazus Utility Fragility Functions\nSelection: '+document.getElementById('util-ct').textContent+'\n\n'+h+'\n'+r,'util-copy');
}
function utilInit(){
  if(!UTIL||!UTIL.length)return;
  var systems=[...new Set(UTIL.map(function(r){return r.system;}))].sort();
  var facilities=[...new Set(UTIL.map(function(r){return r.facility;}))].sort();
  var anchorings=[...new Set(UTIL.map(function(r){return r.anchoring;}))].sort();
  function fill(id,vals){var el=document.getElementById(id);vals.forEach(function(v){el.add(new Option(v,v));});}
  fill('util-system',systems);fill('util-facility',facilities);fill('util-anchoring',anchorings);
  fill('util-system2',systems);fill('util-facility2',facilities);fill('util-anchoring2',anchorings);
  utilFilter();
}
"""

