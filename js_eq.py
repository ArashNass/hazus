def get_eq_js():
    return r"""
/* ===== EARTHQUAKE CURVE 1 ===== */
function normCDF(x){
  var a1=0.254829592,a2=-0.284496736,a3=1.421413741,a4=-1.453152027,a5=1.061405429,p=0.3275911;
  var sign=x<0?-1:1,ax=Math.abs(x)/Math.SQRT2,t=1/(1+p*ax);
  var poly=t*(a1+t*(a2+t*(a3+t*(a4+t*a5))));
  return 0.5*(1+sign*(1-poly*Math.exp(-ax*ax)));
}
function frag(pga,med,beta){var m=med/100;return(pga<=0||m<=0)?0:normCDF(Math.log(pga/m)/beta);}

function eqFilter(){
  var mat=document.getElementById('eq-mat').value;
  var ht=document.getElementById('eq-ht').value;
  var codes=Object.keys(EQ).filter(function(k){return(!mat||EQ[k].material===mat)&&(!ht||EQ[k].height===ht);});
  var sel=document.getElementById('eq-bldg');
  var cur=sel.value;sel.innerHTML='';
  codes.forEach(function(k){sel.add(new Option(k+' \u2014 '+EQ[k].name+' ('+EQ[k].height+')',k));});
  if(codes.indexOf(cur)>=0)sel.value=cur;
  var mc=document.getElementById('eq-match');if(mc)mc.textContent=codes.length+' type'+(codes.length===1?'':'s')+' match';
  eqDraw();
}

function eqReset(){
  document.getElementById('eq-mat').value='';
  document.getElementById('eq-ht').value='';
  eqFilter();
}

function eqUnit(u,btn){
  eqUM=u;
  document.querySelectorAll('#page-eq .unit-switch .us-btn').forEach(function(b){b.classList.remove('active');});
  btn.classList.add('active');
  eqRenderChart();
}

function eqFillTbl(bldg,code){
  var params=EQ[bldg]&&EQ[bldg][code];if(!params)return;
  var beta=0.64,pgas=[],dsn=['Slight','Moderate','Extensive','Complete'];
  for(var i=0;i<=300;i+=10)pgas.push(parseFloat((i*0.005).toFixed(3)));
  document.getElementById('eq-tbody').innerHTML=pgas.map(function(p){
    return '<tr><td>'+p.toFixed(2)+'</td><td>'+(p*G).toFixed(3)+'</td>'+
      dsn.map(function(_,j){return '<td>'+(frag(p,params[j],beta)*100).toFixed(1)+'%</td>';}).join('')+'</tr>';
  }).join('');
}

function eqDraw(){
  var bldg=document.getElementById('eq-bldg').value;
  var code=document.getElementById('eq-code').value;
  if(!bldg||!EQ[bldg])return;
  eqB1=bldg;eqC1=code;
  var db=EQ[bldg],params=db[code];
  var cl={H:'High Code',M:'Moderate Code',L:'Low Code',P:'Pre-Code'};
  document.getElementById('eq-cs').textContent=db.name+'  |  '+db.height+'  |  Beta = 0.64';
  if(!params){
    document.getElementById('eq-ct').textContent=bldg+' \u2014 '+cl[code]+' \u2014 Not applicable in Hazus';
    document.getElementById('eq-tbody').innerHTML='<tr><td colspan="6" style="text-align:center;color:var(--onyx3);padding:24px;font-style:italic">This combination does not exist in Hazus</td></tr>';
    meta(document.getElementById('eq-meta'),[['Building',bldg],['Design level',cl[code]],['Status','N/A'],['Reason','Not possible at this design level']]);
    document.getElementById('eq-leg').innerHTML='';
    if(eqChart){eqChart.destroy();eqChart=null;}return;
  }
  var eqTitle=bldg+' \u2014 '+db.name+' \u2014 '+cl[code];
  document.getElementById('eq-ct').textContent=eqTitle;
  document.getElementById('eq-title').textContent=eqTitle;
  meta(document.getElementById('eq-meta'),[
    ['Building',bldg],['Height class',db.height],['Design level',cl[code]],
    ['Slight median',params[0]+'%g / '+(params[0]/100*G).toFixed(2)+' m/s\u00b2'],
    ['Moderate median',params[1]+'%g / '+(params[1]/100*G).toFixed(2)+' m/s\u00b2'],
    ['Extensive median',params[2]+'%g / '+(params[2]/100*G).toFixed(2)+' m/s\u00b2'],
    ['Complete median',params[3]+'%g / '+(params[3]/100*G).toFixed(2)+' m/s\u00b2']]);
  eqFillTbl(eqTC===2&&eqB2?eqB2:eqB1, eqTC===2&&eqC2?eqC2:eqC1);
  eqRenderChart();
}

function eqRenderChart(){
  if(!eqB1||!eqC1||!EQ[eqB1]||!EQ[eqB1][eqC1])return;
  var beta=0.64,pgas=[];for(var i=0;i<=300;i++)pgas.push(parseFloat((i*0.005).toFixed(3)));
  var dsn=['Slight','Moderate','Extensive','Complete'];
  var dsc=[WC.slight,WC.moderate,WC.extensive,WC.complete];
  var ms2=eqUM==='ms2';
  var labels=pgas.map(function(p){return ms2?(p*G).toFixed(2):p.toFixed(3);});
  var p1=EQ[eqB1][eqC1];
  var datasets=dsn.map(function(name,j){
    return{label:name,data:pgas.map(function(p){return parseFloat(frag(p,p1[j],beta).toFixed(5));}),
      borderColor:dsc[j],backgroundColor:'transparent',borderWidth:2.5,pointRadius:0,tension:0,borderDash:[]};
  });
  if(eqCmp&&eqB2&&eqC2&&EQ[eqB2]&&EQ[eqB2][eqC2]){
    var p2=EQ[eqB2][eqC2];
    dsn.forEach(function(name,j){
      datasets.push({label:name+' C2',data:pgas.map(function(p){return parseFloat(frag(p,p2[j],beta).toFixed(5));}),
        borderColor:dsc[j],backgroundColor:'transparent',borderWidth:1.5,pointRadius:0,tension:0,borderDash:[6,3]});
    });
  }
  // Add vertical median lines as custom plugin data
  var medianPlugin={
    id:'medians',
    afterDraw:function(chart){
      if(!eqCmp||(!eqB2)){
        // Draw median lines for curve 1
        dsn.forEach(function(name,j){
          var medG=p1[j]/100;
          var medX=ms2?(medG*G):medG;
          var xScale=chart.scales.x;
          var yScale=chart.scales.y;
          var xPx=xScale.getPixelForValue(ms2?medX.toFixed(2):medX.toFixed(3));
          if(xPx<xScale.left||xPx>xScale.right)return;
          var ctx2=chart.ctx;
          ctx2.save();
          ctx2.beginPath();
          ctx2.setLineDash([4,4]);
          ctx2.strokeStyle=dsc[j];
          ctx2.lineWidth=1.2;
          ctx2.globalAlpha=0.7;
          ctx2.moveTo(xPx,yScale.top);
          ctx2.lineTo(xPx,yScale.bottom);
          ctx2.stroke();
          ctx2.restore();
        });
      }
    }
  };
  // Register plugin temporarily
  Chart.register(medianPlugin);
  eqChart=mkChart('eq-c',labels,datasets,
    ms2?'Peak ground acceleration (m/s\u00b2)':'Peak ground acceleration (g)',
    'Probability of reaching damage state',eqChart);
  setTimeout(function(){Chart.unregister(medianPlugin);},0);
  var cl={H:'High Code',M:'Moderate Code',L:'Low Code',P:'Pre-Code'};
  document.getElementById('eq-leg').innerHTML=dsn.map(function(n,j){
    return '<div class="li"><div class="ld" style="background:'+dsc[j]+'"></div>'+n+' -- '+p1[j]+'%g / '+(p1[j]/100*G).toFixed(2)+' m/s\u00b2</div>';
  }).join('');
  var cmpLeg=document.getElementById('eq-cmp-leg');
  if(eqCmp&&eqB2&&eqC2&&EQ[eqB2]&&EQ[eqB2][eqC2]){
    cmpLeg.style.display='flex';
    cmpLeg.innerHTML='<div class="cl-item"><div class="cl-dot" style="background:'+dsc[0]+'"></div>Curve 1 (solid): '+eqB1+' \u2014 '+cl[eqC1]+'</div>'+
      '<div class="cl-item"><div class="cl-dot" style="background:'+dsc[0]+';opacity:.5"></div>Curve 2 (dashed): '+eqB2+' \u2014 '+cl[eqC2]+'</div>';
  }else{cmpLeg.style.display='none';}
}

/* ===== EARTHQUAKE CURVE 2 (completely independent) ===== */
function eqCmpToggle(){
  eqCmp=document.getElementById('eq-cmp-chk').checked;
  document.getElementById('eq-cmp-lbl').classList.toggle('on',eqCmp);
  document.getElementById('eq-cmp2-wrap').style.display=eqCmp?'block':'none';
  document.getElementById('eq-tbl-tabs').style.display='none';
  if(!eqCmp){eqB2=null;eqC2=null;eqRenderChart();}
  else{eqFilter2();}
}

function eqFilter2(){
  var mat=document.getElementById('eq-mat2').value;
  var ht=document.getElementById('eq-ht2').value;
  var codes=Object.keys(EQ).filter(function(k){return(!mat||EQ[k].material===mat)&&(!ht||EQ[k].height===ht);});
  var sel2=document.getElementById('eq-bldg2');
  var cur=sel2.value;sel2.innerHTML='';
  codes.forEach(function(k){sel2.add(new Option(k+' \u2014 '+EQ[k].name+' ('+EQ[k].height+')',k));});
  if(codes.indexOf(cur)>=0)sel2.value=cur;
  if(codes.length)eqDraw2();
}

function eqDraw2(){
  var b2=document.getElementById('eq-bldg2').value;
  var c2=document.getElementById('eq-code2').value||'H';
  if(!b2){eqB2=null;eqC2=null;document.getElementById('eq-tbl-tabs').style.display='none';eqRenderChart();return;}
  eqB2=b2;eqC2=c2;
  document.getElementById('eq-tbl-tabs').style.display='flex';
  eqRenderChart();
}

function eqShowTbl(n,btn){
  eqTC=n;
  document.querySelectorAll('#eq-tbl-tabs .tbl-tab').forEach(function(b){b.classList.remove('active');});
  btn.classList.add('active');
  var b=n===1?eqB1:eqB2,c=n===1?eqC1:eqC2;if(b&&c)eqFillTbl(b,c);
}

function eqCopy(){
  var cl={H:'High Code',M:'Moderate Code',L:'Low Code',P:'Pre-Code'};
  if(eqCmp&&eqB1&&eqB2&&eqC1&&eqC2&&EQ[eqB1][eqC1]&&EQ[eqB2]&&EQ[eqB2][eqC2]){
    var p1=EQ[eqB1][eqC1],p2=EQ[eqB2][eqC2];
    var dsn=['Slight','Moderate','Extensive','Complete'];
    var hdr='Earthquake Vulnerability Function Comparison - Hazus-MH\nLognormal fragility Beta=0.64\nCurve 1: '+eqB1+' \u2014 '+cl[eqC1]+'\nCurve 2: '+eqB2+' \u2014 '+cl[eqC2];
    var hRow='PGA (g)\tPGA (m/s\u00b2)\t'+dsn.map(function(d){return d+' C1\t'+d+' C2';}).join('\t');
    var pgas=[];for(var i=0;i<=300;i+=10)pgas.push(parseFloat((i*0.005).toFixed(3)));
    var rows=pgas.map(function(p){
      return p.toFixed(2)+'\t'+(p*G).toFixed(3)+'\t'+
        dsn.map(function(_,j){return (frag(p,p1[j],0.64)*100).toFixed(1)+'%\t'+(frag(p,p2[j],0.64)*100).toFixed(1)+'%';}).join('\t');
    }).join('\n');
    copyText(hdr+'\n\n'+hRow+'\n'+rows,'eq-copy');
  }else{
    var h=[...document.getElementById('eq-thead').querySelectorAll('th')].map(function(t){return t.textContent.trim();}).join('\t');
    var r=[...document.getElementById('eq-tbody').querySelectorAll('tr')].map(function(r){return [...r.querySelectorAll('td')].map(function(c){return c.textContent.trim();}).join('\t');}).join('\n');
    copyText('Earthquake Vulnerability Functions - Hazus-MH\nLognormal fragility Beta=0.64\nSelection: '+document.getElementById('eq-ct').textContent+'\n\n'+h+'\n'+r,'eq-copy');
  }
}
"""
