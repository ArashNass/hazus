def get_utils_js():
    return r"""
const G=9.80665,GF=1.28;
const C1F='#0d9488',C1W='#0f766e',C2='#c900ac';
const WC={slight:'#1A7340',moderate:'#C47D00',extensive:'#C0321A',complete:'#334155'};
const OCC={RES1:'Single family home',RES2:'Mobile home',RES3:'Multi-family',RES4:'Hotel/motel',
  RES5:'Dormitory',RES6:'Nursing home',COM1:'Retail trade',COM2:'Wholesale trade',
  COM3:'Personal services',COM4:'Professional services',COM5:'Banks/financial',COM6:'Hospital',
  COM7:'Medical clinic',COM8:'Entertainment',COM9:'Parking',COM10:'Other commercial',
  IND1:'Heavy industrial',IND2:'Light industrial',IND3:'Food/chemicals',IND4:'Metals/minerals',
  IND5:'High tech',IND6:'Construction',AGR1:'Agriculture',REL1:'Church/place of worship',
  GOV1:'Government services',GOV2:'Emergency response',EDU1:'Schools K-12',
  EDU2:'Colleges/universities',COM:'Commercial',EDU:'Education',INDX:'Industrial'};

let flChart=null,wiChart=null,eqChart=null,utilChart=null;
let flUM='m',wiAM='3s',wiSM='ms',eqUM='g',utilUM='g';
let flCmp=false,flR1=null,flR2=null,flTC=1;
let wiCmp=false,wiR1=null,wiR2=null,wiTC=1;
let eqCmp=false,eqB1=null,eqC1=null,eqB2=null,eqC2=null,eqTC=1;
let utilCmp=false,utilR1=null,utilR2=null,utilTC=1;

function show(id,btn){
  document.querySelectorAll('.nav-tab').forEach(function(t){t.classList.remove('active');});
  document.querySelectorAll('.page').forEach(function(p){p.classList.remove('active');});
  btn.classList.add('active');
  document.getElementById('page-'+id).classList.add('active');
  if(id==='eq' &&!eqChart)  eqFilter();
  if(id==='util'&&typeof utilInit==='function'&&!utilR1) utilInit();
  if(id==='gem'&&typeof gemFilter==='function') gemFilter();
  if(id==='jrc'  &&typeof jrcDraw  ==='function') jrcDraw();
  if(id==='etris'&&typeof etrisInit==='function')  etrisInit();
  if(id==='esrm' &&typeof esrmFilter==='function') esrmFilter();
  if(id==='ci'   &&typeof ciFilter   ==='function') ciFilter();
  if(id==='wizard'&&typeof wzInit     ==='function') wzInit();
  /* wizard has no init needed */
  /* Update URL with current tab — only when not a file:// origin */
  try{
    if(window.location.protocol!=='file:'){
      var url=new URL(window.location.href);
      url.searchParams.set('tab',id);
      window.history.replaceState({},'',url);
    }
  }catch(e){}
}
// Deep link: read ?tab=X from URL on page load
window.addEventListener('DOMContentLoaded',function(){
  var params=new URLSearchParams(window.location.search);
  var tab=params.get('tab');
  if(tab){
    var btn=document.querySelector('[data-tab="'+tab+'"]');
    if(btn)btn.click();
  }
});
function meta(el,items){
  el.innerHTML=items.map(function(p){
    return '<div class="mi"><div class="mi-l">'+p[0]+'</div><div class="mi-v">'+(p[1]||'&mdash;')+'</div></div>';
  }).join('');
}
var _tt=null;
function showToast(msg,ok){
  var el=document.getElementById('toast');
  el.textContent=msg;el.style.background=ok?'#1A7340':'#C0321A';
  el.classList.add('show');clearTimeout(_tt);
  _tt=setTimeout(function(){el.classList.remove('show');},2800);
}
function copyText(text,btnId){
  var btn=document.getElementById(btnId);
  function onOK(){btn.textContent='Copied!';btn.classList.add('ok');showToast('Data copied to clipboard',true);setTimeout(function(){btn.textContent='Copy data';btn.classList.remove('ok');},2400);}
  function onErr(){btn.textContent='Failed';btn.classList.add('err');showToast('Copy failed',false);setTimeout(function(){btn.textContent='Copy data';btn.classList.remove('err');},2400);}
  var ta=document.createElement('textarea');ta.value=text;ta.setAttribute('readonly','');
  ta.style.cssText='position:fixed;top:-9999px;left:-9999px;opacity:0;';
  document.body.appendChild(ta);ta.focus();ta.select();ta.setSelectionRange(0,99999);
  var ok=false;try{ok=document.execCommand('copy');}catch(e){ok=false;}
  document.body.removeChild(ta);
  if(ok){onOK();}else if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(text).then(onOK).catch(onErr);}else{onErr();}
}
function mkChart(id,labels,datasets,xTitle,yTitle,existing){
  if(existing)existing.destroy();
  return new Chart(document.getElementById(id).getContext('2d'),{
    type:'line',data:{labels:labels,datasets:datasets},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{
        legend:{display:false},
        tooltip:{
          mode:'index',intersect:false,
          callbacks:{
            label:function(ctx){
              return ' '+ctx.dataset.label+': '+(ctx.parsed.y*100).toFixed(2)+'%';
            }
          },
          backgroundColor:'rgba(15,118,110,.92)',
          titleColor:'#fff',bodyColor:'#fff',
          borderColor:'#5eead4',borderWidth:1,
          padding:10,cornerRadius:6
        }
      },
      scales:{
        x:{title:{display:true,text:xTitle,font:{size:12,weight:'600'},color:'#0f766e'},
           ticks:{maxTicksLimit:12,color:'#5A5660'},grid:{color:'#e6f4f1'}},
        y:{title:{display:true,text:yTitle,font:{size:12,weight:'600'},color:'#0f766e'},
           min:0,max:1,ticks:{callback:function(v){return(v*100).toFixed(0)+'%';},color:'#5A5660'},
           grid:{color:'#e6f4f1'}}
      },
      hover:{mode:'index',intersect:false},
      animation:{duration:200}}
  });
}

/* ===== UTILITIES ===== */

// Export chart as PNG
function exportPNG(canvasId, titleId) {
  var canvas = document.getElementById(canvasId);
  var title = titleId ? (document.getElementById(titleId)||{textContent:''}).textContent : '';
  var exp = document.createElement('canvas');
  exp.width  = canvas.width;
  exp.height = canvas.height + (title ? 40 : 0);
  var ctx = exp.getContext('2d');
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0,0,exp.width,exp.height);
  if(title){
    ctx.font = '600 13px -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif';
    ctx.fillStyle = '#0f766e';
    ctx.fillText(title.slice(0,120), 12, 26);
    ctx.drawImage(canvas,0,40);
  } else {
    ctx.drawImage(canvas,0,0);
  }
  var a = document.createElement('a');
  a.href = exp.toDataURL('image/png');
  a.download = (canvasId==='fl-c'?'flood':canvasId==='wi-c'?'wind':canvasId==='util-c'?'utility':'earthquake')+'_vulnerability.png';
  a.click();
}

// Remember selections across tab switches
var _saved = {};
"""
