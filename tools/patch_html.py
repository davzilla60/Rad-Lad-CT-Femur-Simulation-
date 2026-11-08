"""One-off: turn the forked wrist.html into femur.html (CT femur). Run once from the project root."""
import re, sys

P = "femur.html"
s = open(P, encoding="utf-8").read()


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n < 1:
        sys.exit("NOT FOUND: " + old[:80])
    if count == 1 and n > 1:
        sys.exit("AMBIGUOUS (%d): %s" % (n, old[:80]))
    s = s.replace(old, new)


def block(start, end, new):
    """replace from `start` (inclusive) up to `end` (exclusive)"""
    global s
    a = s.index(start); b = s.index(end, a)
    s = s[:a] + new + s[b:]


# ---------------------------------------------------------------- head / css / static html
rep("<title>The Scanogram — CT Wrist Simulator</title>", "<title>The Scanogram — CT Femur Simulator</title>")
rep('/* ===== "Superman Scanned" achievement / marker ===== */', '/* ===== "Slice of the Thigh" achievement / marker ===== */')
rep("""/* "S" mark */
  content:'S';""", """/* "F" mark */
  content:'F';""")
rep("<!-- ================= THE SCANOGRAM · CT WRIST ================= -->", "<!-- ================= THE SCANOGRAM · CT FEMUR ================= -->")
block('        <!-- patient set-up: CT room, prone "superman" -->', '        <!-- DFOV + scan-range planning box -->', '''        <!-- patient set-up: CT room, supine feet first -->
        <div class="scg-room scg-hidden" id="scgRoom">
          <div class="scg-room3d" id="scgRoom3d" aria-label="3-D view: patient lying supine, feet first toward the CT gantry"></div>
          <div class="scg-roomcap"><b>PATIENT ON THE TABLE</b><span id="scgRoomStep">supine, feet first</span></div>
          <svg class="scg-roomsvg" viewBox="0 0 600 600" preserveAspectRatio="xMidYMid meet" aria-label="Patient lying supine, feet first toward the CT gantry">
            <rect x="0" y="452" width="600" height="148" fill="#0e110d"/>
            <line x1="0" y1="452" x2="600" y2="452" stroke="#2c3a22" stroke-width="2"/>
            <path d="M120 452 L150 370 L330 370 L360 452 Z" fill="#2a3227"/>
            <rect x="130" y="358" width="210" height="16" rx="5" fill="#363f33"/>
            <g class="scg-couch" id="scgCouch">
              <rect x="0" y="334" width="420" height="20" rx="8" fill="#2a3127"/>
              <rect x="0" y="330" width="420" height="7" rx="3.5" fill="#55604f"/>
              <rect x="6" y="318" width="54" height="12" rx="5" fill="#cdd5c8"/>
              <ellipse cx="34" cy="304" rx="24" ry="16" fill="#cf9a7c" stroke="#7d5a43"/>
              <path d="M58 300 C 90 286, 170 284, 200 296 L 200 330 L 58 330 Z" fill="#8fb3c9" stroke="#3f5a6a"/>
              <path d="M196 300 C 260 296, 330 300, 372 306 L 372 330 L 196 330 Z" fill="#a9b6a1" stroke="#6f7d68"/>
              <path d="M372 312 L 392 314 L 396 286 L 406 286 L 404 330 L 372 330 Z" fill="#5d6f7d" stroke="#3a4650"/>
              <text x="200" y="348" fill="#9fe7b8" font-size="10" font-family="ui-monospace,monospace" letter-spacing="2" text-anchor="middle">FEET FIRST &#9654;</text>
            </g>
            <g>
              <path d="M450 284 V148 q0 -30 30 -30 h50 q30 0 30 30 V284 Z" fill="#dfe5dc" stroke="#7f8a7a" stroke-width="1.5"/>
              <path d="M450 352 V434 q0 30 30 30 h50 q30 0 30 -30 V352 Z" fill="#dfe5dc" stroke="#7f8a7a" stroke-width="1.5"/>
              <rect x="450" y="284" width="110" height="68" fill="rgba(10,14,9,.55)" stroke="#5c6758" stroke-width="1.2"/>
              <text x="505" y="420" fill="#56604f" font-size="10" font-family="Trebuchet MS,sans-serif" letter-spacing="3" text-anchor="middle">GANTRY</text>
            </g>
            <g class="scg-laser">
              <line x1="505" y1="262" x2="505" y2="292" stroke="#ff5a4f" stroke-width="2"/>
              <circle cx="505" cy="292" r="3" fill="#ff5a4f"/>
            </g>
            <text x="300" y="58" fill="#dfe7d6" font-size="15" font-family="Trebuchet MS,sans-serif" letter-spacing="4" text-anchor="middle">SUPINE &#183; FEET FIRST</text>
            <text x="300" y="80" fill="#8ba07d" font-size="10.5" font-family="ui-monospace,monospace" text-anchor="middle">legs straight &#8212; the thigh travels into the gantry first</text>
          </svg>
        </div>

''')
rep('<span class="scg-eh-tag" id="scgTopTag">distal</span>', '<span class="scg-eh-tag" id="scgTopTag">proximal</span>')
rep('<span class="scg-eh-tag" id="scgBotTag">proximal</span>', '<span class="scg-eh-tag" id="scgBotTag">distal</span>')
rep('<!-- "SUPERMAN SCANNED" MARKER -->', '<!-- "SLICE OF THE THIGH" MARKER -->')
rep('<div class="scg-ach-title">Superman Scanned</div>', '<div class="scg-ach-title">Slice of the Thigh</div>')
rep('<div class="scg-ach-sub">CT Wrist · 100%</div>', '<div class="scg-ach-sub">CT Femur · 100%</div>')
rep('Share your <strong>Superman Scanned</strong> Marker', 'Share your <strong>Slice of the Thigh</strong> Marker')
rep('<div class="scg-sub">CT Wrist — position the patient, plan the range and DFOV, choose the reconstruction</div>',
    '<div class="scg-sub">CT Femur — position the patient, plan the range and DFOV, choose the reconstruction</div>')
rep('alt="PA scanogram preview"', 'alt="AP scanogram preview"')
rep('''      Imaging adapted from the KU Leuven multimodal CT dataset of cadaveric wrist joints (Quintiens et al., 2024), specimen 1, <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="noopener">CC BY-SA 4.0</a> — full credits and changes are listed on the results screen.</div>''',
    '''      Imaging adapted from the HFValid collection (Aldieri et al., University of Bologna, 2023), subject Pat001 — real, de-identified CT, <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">CC BY 4.0</a> — full credits and changes are listed on the results screen.</div>''')
rep('<script src="room3d.js?v=6"></script>', '<script src="room3d.js?v=1"></script>')

# ---------------------------------------------------------------- script: header, constants, geometry, rendering
block('/* ---------------------------------------------------------------\n   THE SCANOGRAM — CT wrist simulator', '/* =============================================================\n   CONSOLE LOG', r'''/* ---------------------------------------------------------------
   THE SCANOGRAM — CT femur simulator
   Patient set-up (supine, feet first: arms + feet) → AP + lateral scanogram → scan range + DFOV box →
   reconstruction (kernel, slice thickness) → axial / coronal / sagittal review rendered for those
   choices → percentage grade.  Imaging: HFValid collection Pat001 (CC BY 4.0), see tools/.
   --------------------------------------------------------------- */

var BASE = "./assets/";
var C = window.SCG_CALIB;
var SP = C.sp, PX = C.px, IMG_W = C.img_w, IMG_H = C.img_h, FX = C.field_x, FY = C.field_y;
var PAD = C.pad_ap, PADL = C.pad_lat;                 // air added lateral of the field on the AP / either side on the LAT scout
var SW = C.scout_w_mm, SWL = C.scout_lat_w_mm, SH = C.scout_h_mm;
var AX = C.ax, AX_N = AX.length, COR_Y = C.cor_y, SAG_X = C.sag_x;
var LM = C.landmarks;                                 // mm from the superior edge of the scanogram
var HU_LUT = C.hu_lut;
var PREVIEW_K;
function nearestAx(z){ var b=0; for(var k=1;k<AX_N;k++) if(Math.abs(AX[k].z-z)<Math.abs(AX[b].z-z)) b=k; return b; }
PREVIEW_K = nearestAx(LM.lt - 28);                     // intertrochanteric region: trabecular bone shows the kernel
function pad2(n){ return (n<10?"0":"")+n; }
function pad3(n){ return (n<10?"00":n<100?"0":"")+n; }

var PNG = { logo_full:1, logo_mark:1 };
var ASSETS = window.SCG_ASSETS || null;
function url(name){ return ASSETS ? ASSETS[name] : BASE + name + (PNG[name] ? ".png" : ".jpg"); }

/* ---- DOM ---- */
var $ = function(id){ return document.getElementById(id); };
var stage=$("scgStage"), vp=$("scgViewport"),
    img=$("scgImg"), imgB=$("scgImgB"),
    acqEl=$("scgAcq"), acqTitle=$("scgAcqTitle"), acqNum=$("scgAcqNum"),
    watermark=$("scgWatermark"), watermarkTx=$("scgWatermarkTx"),
    vpTL=$("scgVpTL"), vpBL=$("scgVpBL"), vpBR=$("scgVpBR"),
    railTitle=$("scgRailTitle"), railDesc=$("scgRailDesc"), railBody=$("scgRailBody"),
    cmds=$("scgCmds"), cliForm=$("scgCliForm"), cli=$("scgCli"),
    logEl=$("scgLog"), phaseChip=$("scgPhaseChip"),
    titleEl=$("scgTitle"), startBtn=$("scgStart"),
    resultEl=$("scgResult"), room=$("scgRoom"),
    stackUI=$("scgStackUI"), stackSlider=$("scgStackSlider"), winBtns=$("scgWinBtns"),
    pip=$("scgPip"), pipImg=$("scgPipImg"), pipBox=$("scgPipBox"),
    fovEl=$("scgFov"), fovCap=$("scgFovCap"), topTag=$("scgTopTag"), botTag=$("scgBotTag"),
    fovTopH=$("scgFovTop"), fovBotH=$("scgFovBot"), fovLeftH=$("scgFovLeft"), fovRightH=$("scgFovRight"),
    fovMaskT=$("scgFovMaskT"), fovMaskB=$("scgFovMaskB"), fovMaskL=$("scgFovMaskL"), fovMaskR=$("scgFovMaskR"),
    orientEl=$("scgOrient"),
    achWrap=$("scgAch"), achLogo=$("scgAchLogo");

/* ---- brand ---- */
$("scgMarkMini").innerHTML =
  '<img class="scg-mark-ic" src="'+url("logo_mark")+'" alt="Rad-Lad">'+
  '<div class="scg-mark-tx"><b>THE&nbsp;SCANOGRAM&nbsp;·&nbsp;CT&nbsp;FEMUR</b><span>Rad-Lad&nbsp;·&nbsp;Illuminate&nbsp;the&nbsp;Invisible</span></div>';
$("scgLogoBig").src = url("logo_full");
$("scgTitleScoutAp").src  = url("scout_ap");
$("scgTitleScoutLat").src = url("scout_lat");
achLogo.src = url("logo_mark");

function playAchievement(){
  achWrap.classList.remove("is-playing");
  void achWrap.offsetWidth;
  achWrap.classList.add("is-playing");
}
$("scgAchReplay").addEventListener("click", playAchievement);

/* =============================================================
   STATE
   ============================================================= */
var BOX0 = { x0:0.03, x1:0.97, y0:0.205, y1:0.82 };   // starts below the femoral head, short of the knee, DFOV far too wide
function freshState(){
  return {
    phase:"title",
    arms:null, armsFirst:null, feet:null, feetFirst:null,   // set-up answers (first attempt of each is graded)
    loaded:false, loading:false,
    box:{ x0:BOX0.x0, x1:BOX0.x1, y0:BOX0.y0, y1:BOX0.y1 }, boxConfirmed:false,
    kernel:"bone", thick:1,
    plane:"ax", win:"bone", stackK:0, lo:0, hi:0, list:[],
    imgNat:{w:1,h:1}, score:null
  };
}
var S = freshState();

/* =============================================================
   GEOMETRY  (box fractions of the AP scout: x across SW mm, y down SH mm from the iliac wing)
   ============================================================= */
function topMm(){ return S.box.y0*SH; }
function botMm(){ return S.box.y1*SH; }
function lenMm(){ return botMm()-topMm(); }
function dfov(){ return (S.box.x1-S.box.x0)*SW; }
function cxMm(){ return (S.box.x0+S.box.x1)/2*SW; }
function rangeKs(){
  var ks=[]; for(var k=0;k<AX_N;k++){ if(AX[k].z>=topMm() && AX[k].z<=botMm()) ks.push(k); }
  if(!ks.length) ks=[nearestAx((topMm()+botMm())/2)];
  return ks;
}
/* tissue that a unilateral femur study must contain over the range (x: scout mm, y: AP mm from the front of
   the field); the AP recon centre is auto-centred on it */
function extent(){
  var e=[1e9,-1e9,1e9,-1e9];
  rangeKs().forEach(function(k){ var x=AX[k].ext; if(!x) return;
    e[0]=Math.min(e[0],x[0]); e[1]=Math.max(e[1],x[1]); e[2]=Math.min(e[2],x[2]); e[3]=Math.max(e[3],x[3]); });
  if(e[0]>e[1]) e=[80,220,50,210];
  return { x0:e[0], x1:e[1], y0:e[2], y1:e[3], w:e[1]-e[0], d:e[3]-e[2], cy:(e[2]+e[3])/2 };
}
function clipMm(){
  var e=extent(), w=dfov(), x0=S.box.x0*SW, x1=S.box.x1*SW;
  var l=Math.max(0, x0-e.x0), r=Math.max(0, e.x1-x1), ap=Math.max(0, e.d-w);
  return { l:l, r:r, ap:ap, total:l+r+ap };
}
function needW(){ var e=extent(); return Math.max(e.w, e.d); }

/* coverage judgements (mm from the superior edge) */
function proxOK(){ return topMm() <= LM.head_top - 6; }          // above the acetabular roof: the whole hip joint
function proxHead(){ return topMm() <= LM.head_ctr; }             // at least the femoral head
function distOK(){ return botMm() >= LM.condyle_bot + 3; }        // knee joint line + top of the tibial plateau
function distCond(){ return botMm() >= LM.knee_ctr; }             // at least most of the condyles
function pelvisOver(){ return topMm() < LM.head_top - 24; }       // runs on up into the pelvis
function dfovSnug(){ var c=clipMm(); return c.total<=1 && dfov() <= needW()+30; }
function planIdeal(){ return proxOK() && !pelvisOver() && distOK() && dfovSnug(); }
function zLabel(mm){
  if(mm < LM.head_top-12) return "iliac wing";
  if(mm < LM.head_top) return "acetabular roof";
  if(mm < LM.head_ctr+14) return "femoral head";
  if(mm < LM.lt-18) return "femoral neck / trochanters";
  if(mm < LM.lt+15) return "lesser trochanter";
  if(mm < 170) return "proximal shaft";
  if(mm < 290) return "mid shaft";
  if(mm < LM.knee_ctr-55) return "distal shaft";
  if(mm < LM.knee_ctr-20) return "distal metaphysis";
  if(mm < LM.condyle_bot) return "femoral condyles";
  return "knee joint / tibial plateau";
}

/* =============================================================
   IMAGE DECODING — HU recovered from the JPEG LUT
   ============================================================= */
var BYTE2HU = new Float32Array(256);
(function(){
  for(var b=0;b<256;b++){
    for(var i=1;i<HU_LUT.length;i++) if(b<=HU_LUT[i][1] || i===HU_LUT.length-1){
      var a=HU_LUT[i-1], c=HU_LUT[i];
      BYTE2HU[b] = a[0] + (b-a[1])*(c[0]-a[0])/(c[1]-a[1]); break;
    }
  }
})();
var cache = {};
var dcv = document.createElement("canvas"), dcx = dcv.getContext("2d", { willReadFrequently:true });
function loadHU(name, cb){
  if(cache[name]){ cb(cache[name]); return; }
  var im = new Image();
  im.onload = function(){
    var w=im.naturalWidth, h=im.naturalHeight;
    dcv.width=w; dcv.height=h; dcx.drawImage(im,0,0);
    var d=dcx.getImageData(0,0,w,h).data, out=new Float32Array(w*h);
    for(var i=0,j=0;i<out.length;i++,j+=4) out[i]=BYTE2HU[d[j]];
    cache[name]={ hu:out, w:w, h:h }; cb(cache[name]);
  };
  im.onerror = function(){ cb(null); };
  im.src = url(name);
}
function loadMany(names, cb){
  var out=new Array(names.length), left=names.length;
  names.forEach(function(n,i){ loadHU(n, function(r){ out[i]=r; if(--left===0) cb(out); }); });
}
/* separable gaussian (soft-tissue kernel) */
function gaussBlur(a, w, h, sigma){
  var r=Math.ceil(sigma*2.5), k=[], s=0, i, x, y;
  for(i=-r;i<=r;i++){ var v=Math.exp(-i*i/(2*sigma*sigma)); k.push(v); s+=v; }
  for(i=0;i<k.length;i++) k[i]/=s;
  var t=new Float32Array(a.length), o=new Float32Array(a.length);
  for(y=0;y<h;y++){ var row=y*w; for(x=0;x<w;x++){ var acc=0; for(i=-r;i<=r;i++){ var xx=x+i; xx=xx<0?0:(xx>=w?w-1:xx); acc+=a[row+xx]*k[i+r]; } t[row+x]=acc; } }
  for(y=0;y<h;y++){ for(x=0;x<w;x++){ var acc2=0; for(i=-r;i<=r;i++){ var yy=y+i; yy=yy<0?0:(yy>=h?h-1:yy); acc2+=t[yy*w+x]*k[i+r]; } o[y*w+x]=acc2; } }
  return o;
}
/* vertical box blur (thick axial slices seen on a reformat) */
function zBlur(a, w, h, n){
  if(n<2) return a;
  var o=new Float32Array(a.length), half=n/2;
  for(var x=0;x<w;x++){
    for(var y=0;y<h;y++){
      var y0=Math.max(0,Math.round(y-half)), y1=Math.min(h-1,Math.round(y+half)), s=0;
      for(var yy=y0;yy<=y1;yy++) s+=a[yy*w+x];
      o[y*w+x]=s/(y1-y0+1);
    }
  }
  return o;
}
function gauss(){ var u=1-Math.random(), v=Math.random(); return Math.sqrt(-2*Math.log(u))*Math.cos(6.2832*v); }
var WINDOWS = { bone:[450,1800], soft:[50,400] };
function toCanvas(hu, w, h, win){
  var c=document.createElement("canvas"); c.width=w; c.height=h;
  var g=c.getContext("2d"), id=g.createImageData(w,h), d=id.data, lo=win[0]-win[1]/2, W=win[1];
  for(var i=0,j=0;i<hu.length;i++,j+=4){ var v=(hu[i]-lo)/W*255; v=v<0?0:(v>255?255:v); d[j]=d[j+1]=d[j+2]=v; d[j+3]=255; }
  g.putImageData(id,0,0);
  return c;
}
/* arms by the side: the hands and forearms lie beside the hips and upper thighs, in the beam - simulated
   beam-hardening streaks and noise over that part of the range (fading out down the thigh) */
function armF(mm){ return mm<110 ? 1 : mm>175 ? 0 : (175-mm)/65; }
function armArtefact(hu, w, h, axial, zmm){
  var o=new Float32Array(hu.length), cx=w*0.5, cy=h*0.5, i, x, y, f=axial ? armF(zmm) : 0;
  var band = axial ? null : new Float32Array(h);
  if(band) for(y=0;y<h;y++) band[y]=30*gauss()*armF(y*PX);
  if(axial && f<=0) return hu;
  for(y=0;y<h;y++){
    var fy = axial ? f : armF(y*PX);
    for(x=0;x<w;x++){
      i=y*w+x; var v=hu[i];
      if(axial){
        var dx=x-cx, dy=y-cy, th=Math.atan2(dy,dx), r=Math.sqrt(dx*dx+dy*dy);
        // dark streaks running side to side (hand to hand), bright shoulders between them
        v += f*(-90*Math.pow(Math.max(0,Math.abs(Math.cos(th))),8) + 40*Math.sin(th*13+0.6)) * Math.min(1, r/60);
      } else v += band[y];
      o[i]=v + 40*fy*gauss();
    }
  }
  return o;
}
/* kernel: the source is a standard reconstruction; a soft-tissue kernel is modelled as a 0.8 mm gaussian */
function applyKernel(hu, w, h, pxmm){
  return S.kernel==="soft" ? gaussBlur(hu, w, h, 0.8/pxmm) : hu;
}

/* ---- axial: thickness by averaging the 2 mm native slices, DFOV crop/resample into a 512 matrix ---- */
function axWeights(){
  if(S.thick>=5) return [[-2,0.25],[-1,1],[0,1],[1,1],[2,0.25]];
  if(S.thick>=3) return [[-1,0.25],[0,1],[1,0.25]];
  return [[0,1]];
}
function renderAxial(k, cb){
  var ws=axWeights().filter(function(p){ return k+p[0]>=0 && k+p[0]<AX_N; });
  loadMany(ws.map(function(p){ return "ax_"+pad3(k+p[0]); }), function(sl){
    if(sl.some(function(s){ return !s; })){ cb(null); return; }
    var n=IMG_W*IMG_H, hu=new Float32Array(n), tw=0, i;
    ws.forEach(function(p,j){ tw+=p[1]; for(i=0;i<n;i++) hu[i]+=sl[j].hu[i]*p[1]; });
    for(i=0;i<n;i++) hu[i]/=tw;
    if(S.arms==="side") hu=armArtefact(hu, IMG_W, IMG_H, true, AX[k].z);
    hu=applyKernel(hu, IMG_W, IMG_H, SP);
    cb(dfovCanvas(toCanvas(hu, IMG_W, IMG_H, WINDOWS[S.win])));
  });
}
function dfovCanvas(nat){
  var w=dfov(), e=extent(), N=512, sc=N/w;
  var x0=cxMm()-w/2, y0=e.cy-w/2;
  var c=document.createElement("canvas"); c.width=c.height=N;
  var g=c.getContext("2d"); g.fillStyle="#000"; g.fillRect(0,0,N,N);
  g.imageSmoothingEnabled=true; g.imageSmoothingQuality="high";
  var px=w/N;
  if(px > SP*1.05){                       // DFOV coarser than the native grid: go through a matrix-sized buffer
    var m=document.createElement("canvas"); m.width=Math.round(FX/px); m.height=Math.round(FY/px);
    m.getContext("2d").drawImage(nat,0,0,m.width,m.height);
    g.imageSmoothingEnabled=false;
    g.drawImage(m, (PAD-x0)*sc, (0-y0)*sc, FX*sc, FY*sc);
  } else g.drawImage(nat, (PAD-x0)*sc, (0-y0)*sc, FX*sc, FY*sc);
  return c;
}
/* ---- reformats: planes from the volume, cropped to the prescribed range and DFOV ---- */
function renderMPR(plane, i, cb){
  loadHU((plane==="cor"?"cor_":"sag_")+pad2(i), function(r){
    if(!r){ cb(null); return; }
    var hu=zBlur(r.hu, r.w, r.h, S.thick>=1 ? S.thick/PX : 0);
    if(S.arms==="side") hu=armArtefact(hu, r.w, r.h, false);
    hu=applyKernel(hu, r.w, r.h, PX);
    var nat=toCanvas(hu, r.w, r.h, WINDOWS[S.win]);
    var w=dfov(), e=extent(), a0, natW;
    if(plane==="cor"){ a0=cxMm()-w/2-PAD; natW=FX; }               // native column mm (0 = lateral field edge)
    else { a0=e.cy-w/2; natW=FY; }                                  // sagittal: anterior on the left
    var px=Math.max(PX, w/512), cw=Math.round(w/px), ch=Math.round(lenMm()/px);
    var c=document.createElement("canvas"); c.width=cw; c.height=ch;
    var g=c.getContext("2d"); g.fillStyle="#000"; g.fillRect(0,0,cw,ch);
    g.imageSmoothingQuality="high";
    var s=1/px;
    g.drawImage(nat, (0-a0)*s, (0-topMm())*s, natW*s, SH*s);
    cb(c);
  });
}

''')

rep("""    var e=extent(), w=dfov(), l=(PAD+FIELD-(e.cy+w/2))/SW;   // lateral: volar (+y) on the left
    pipBox.style.top=(S.box.y0*100)+"%"; pipBox.style.height=((S.box.y1-S.box.y0)*100)+"%";
    pipBox.style.left=(l*100)+"%"; pipBox.style.width=(w/SW*100)+"%";""",
"""    var e=extent(), w=dfov(), l=(PADL+e.cy-w/2)/SWL;            // lateral: anterior on the left
    pipBox.style.top=(S.box.y0*100)+"%"; pipBox.style.height=((S.box.y1-S.box.y0)*100)+"%";
    pipBox.style.left=(l*100)+"%"; pipBox.style.width=(w/SWL*100)+"%";""")

# ---------------------------------------------------------------- commands / help
rep('label:"LOAD PATIENT · HEAD FIRST"', 'label:"LOAD PATIENT · FEET FIRST"')
rep("""  if(c.needs==="canLoad")  return !!S.pos && !S.loaded && !S.loading;""", """  if(c.needs==="canLoad")  return !!S.arms && !!S.feet && !S.loaded && !S.loading;""")
rep("""(c.id==="load"&&S.pos)""", """(c.id==="load"&&S.arms&&S.feet)""")
rep("""    log("workflow: choose the position (prone | supine | side) → load → scout → plan: drag the box from the metacarpal bases to the distal radial metaphysis, edges snug to the wrist → confirm → kernel / thickness → scan → review.","sys");
    log("extras: shift l / shift r (plan) · kernel <bone|soft> · thick <0.6|3|5> · plane <ax|cor|sag> · window <bone|soft> (review)","sys");""",
"""    log("workflow: set up the arms (chest | side) and the feet (taped | relaxed) → load → scout → plan: drag the box from above the acetabular roof to below the knee joint, edges snug to the thigh → confirm → kernel / thickness → scan → review.","sys");
    log("extras: shift l / shift r (plan) · kernel <bone|soft> · thick <1|3|5> · plane <ax|cor|sag> · window <bone|soft> (review)","sys");""")
rep("""  if(S.phase==="setup" && (t==="prone"||t==="superman"||t==="supine"||t==="side")){
    choosePos(t==="superman"?"prone":(t==="supine"?"overhead":t)); return;
  }""", """  if(S.phase==="setup" && (t==="chest"||t==="side")){ chooseArms(t); return; }
  if(S.phase==="setup" && (t==="taped"||t==="relaxed")){ chooseFeet(t); return; }""")
rep("""(tv===0.6||tv===3||tv===5)""", """(tv===1||tv===3||tv===5)""")
rep("""log("usage (reconstruction): thick 0.6 | thick 3 | thick 5","sys");""", """log("usage (reconstruction): thick 1 | thick 3 | thick 5","sys");""")

# ---------------------------------------------------------------- set-up content + render
block("var POS = {", "function render(){", r'''var ARMS = {
  chest:{ label:"ARMS FOLDED ON THE CHEST", desc:"Hands resting on the chest, well above the hips.", short:"arms on the chest", ok:true,
          cap:"ARMS FOLDED ON THE CHEST" },
  side: { label:"ARMS BY THE SIDE", desc:"Arms resting along the body, hands beside the hips.", short:"arms by the side", ok:false,
          cap:"ARMS BY THE SIDE" }
};
var FEET = {
  taped:  { label:"FEET TOGETHER · TURNED IN · TAPED", desc:"Legs straight, feet rotated inward ~15° and taped together with a pad between them.", short:"feet taped, turned in", ok:true,
            cap:"FEET TURNED IN AND TAPED" },
  relaxed:{ label:"FEET RELAXED", desc:"Legs straight, feet left to fall outward naturally.", short:"feet relaxed", ok:false,
            cap:"FEET RELAXED (TURNED OUT)" }
};
function checks(){
  return [
    "Request checked: <b>RIGHT</b> femur · fall from standing, painful thigh — query femoral fracture, include the hip and knee",
    "Metal removed from the waist down · pockets emptied · gown on",
    "Supine, <b>feet first</b>, legs straight, centred on the table",
    S.arms==="chest" ? "Arms folded on the chest — clear of the hips" : S.arms==="side" ? "Arms resting by the side — hands beside the hips" : "Arms: choose",
    S.feet==="taped" ? "Feet rotated inward ~15° and taped together · foam pad between the ankles" : S.feet==="relaxed" ? "Feet relaxed, falling outward" : "Feet: choose",
    "Lasers on the knee joint · table zeroed · right thigh centred in the bore"
  ];
}
function setRoomCaption(){
  var cap=room.querySelector(".scg-roomcap b");
  cap.textContent = "SUPINE · FEET FIRST"+(S.arms ? " · "+ARMS[S.arms].cap : "");
  $("scgRoomStep").textContent = S.feet ? FEET[S.feet].cap.toLowerCase() : "arms by the side, feet relaxed — set up the arms and the feet";
}
''')
block('  if(S.phase==="setup"){', '  else if(S.phase==="topo"){', r'''  if(S.phase==="setup"){
    railTitle.textContent="Patient set-up";
    railDesc.textContent="CT right femur · plain bone";
    var CH=checks(), done = S.loaded ? CH.length : (S.loading ? S.checkN||0 : 3);
    var choice=function(set, cur, attr){ return '<div class="scg-choice">'+Object.keys(set).map(function(k){
          return '<button type="button" data-'+attr+'="'+k+'" class="'+(cur===k?"is-on":"")+'"><b>'+set[k].label+'</b><span>'+set[k].desc+'</span></button>';
        }).join('')+'</div>'; };
    railBody.innerHTML = (S.loaded || S.loading ? "" :
        '<div class="scg-hint">The patient is lying <b>supine, feet first</b>. Where should the <b>arms</b> go?</div>'+choice(ARMS, S.arms, "a")+
        '<div class="scg-hint">And the <b>feet</b>?'+((S.arms||S.feet)?" You can change either before loading — your first choice of each is the one graded.":"")+'</div>'+choice(FEET, S.feet, "f"))+
      ((S.arms && S.feet) || S.loading || S.loaded ? '<div class="scg-check">'+CH.map(function(c,i){
          return '<div class="'+(i<done?"is-done":"")+'"><i>'+(i<done?"✓":"○")+'</i><span>'+c+'</span></div>';
        }).join('')+'</div>'+
        '<div class="scg-hint">'+(S.loaded ? "Right thigh centred in the bore. Command: <b>scout</b>"
          : S.loading ? "Table moving…" : "Command: <b>load</b> — moves the table feet first until the knee reaches the lasers.")+'</div>' : "");
    Array.prototype.forEach.call(railBody.querySelectorAll(".scg-choice button"),function(b){
      b.onclick=function(){ if(b.dataset.a){ logCmd(b.dataset.a); chooseArms(b.dataset.a); } else { logCmd(b.dataset.f); chooseFeet(b.dataset.f); } };
    });
    vpTL.textContent=""; vpBL.textContent=""; vpBR.textContent="";
  }
''')
rep("""        ["Projections","PA + lateral"],
        ["Technique","80 kV · 20 mA"],
        ["Position",POS[S.pos].scout],
        ["Purpose","Plan the range and the DFOV"]
      ])+'<div class="scg-hint">Low-dose projection radiographs of the hand and forearm.</div>';""",
"""        ["Projections","AP + lateral"],
        ["Technique","120 kV · 35 mA"],
        ["Position","Supine · feet first"],
        ["Purpose","Plan the range and the DFOV"]
      ])+'<div class="scg-hint">Low-dose projection radiographs from the pelvis to the knee.</div>';""")
block('    var c=clipMm(), w=dfov(), nw=needW(), dOK=distalOK()&&!distalOver(), pOK=proxOK(), fOK=dfovSnug(), ok=planIdeal();',
      '    vpTL.textContent="SCANOGRAM · PA\\nplan range + DFOV";', r'''    var c=clipMm(), w=dfov(), nw=needW(), pOK=proxOK()&&!pelvisOver(), dOK=distOK(), fOK=dfovSnug(), ok=planIdeal();
    railTitle.textContent="Range + DFOV";
    railDesc.textContent="Box height = scan range · box width = display FOV";
    var hint = ok ? "Acetabular roof → tibial plateau, DFOV snug to the right thigh. Command: <b>confirm</b>"
      : !proxOK() ? (proxHead() ? "Top edge cuts through the <b>femoral head</b> — include the whole hip joint, up past the acetabular roof."
                                : "Top edge stops at the "+zLabel(topMm())+" — the <b>femoral head and neck</b> (the commonest fracture site) are not covered. Drag it up.")
      : pelvisOver() ? "The box runs well up into the <b>pelvis</b> — dose to the pelvic organs for no femoral information. Bring the top edge down to just above the acetabulum."
      : !distOK() ? (distCond() ? "Bottom edge stops in the <b>femoral condyles</b> — extend it through the knee joint to the top of the tibia."
                                : "Bottom edge stops at the "+zLabel(botMm())+" — the <b>knee joint</b> is not covered. Drag it down.")
      : c.total>1 ? "The DFOV <b>clips the thigh</b> ("+(c.l>1?"lateral side ":"")+(c.r>1?"medial side ":"")+(c.ap>1?"front–back depth ":"")+") — widen or shift the box."
      : "DFOV is much wider than the thigh — bigger pixels and a smaller femur on screen. Narrow the box to the soft tissues of the right thigh.";
    railBody.innerHTML=
      '<div class="scg-hint '+(ok?"is-ok":"is-warn")+'">'+hint+'</div>'+
      kvBlock([
        ["Top edge", '<b style="color:'+(pOK?"var(--accent)":"var(--warn)")+'">'+zLabel(topMm())+'</b>'],
        ["Bottom edge", '<b style="color:'+(dOK?"var(--accent)":"var(--warn)")+'">'+zLabel(botMm())+'</b>'],
        ["Range", lenMm().toFixed(0)+" mm"],
        ["DFOV", '<b style="color:'+(fOK?"var(--accent)":"var(--warn)")+'">'+w.toFixed(0)+" mm</b> · pixel "+(w/512).toFixed(2)+" mm"],
        ["Thigh needs", "≈ "+nw.toFixed(0)+" mm"+(c.total>1?' · <b style="color:var(--warn)">clipped '+c.total.toFixed(0)+' mm</b>':"")]
      ])+
      '<div class="scg-hint">Drag the top and bottom edges for the range and the side edges for the DFOV (512 matrix). The lateral inset shows the depth the square DFOV covers. Nudge with <b>top+/-</b>, <b>base+/-</b>, <b>fov+/-</b>, <b>shift l/r</b>.</div>';
''')
rep('''    vpTL.textContent="SCANOGRAM · PA\\nplan range + DFOV";
    vpBL.textContent="lateral inset ↗";
    vpBR.textContent="LEFT · 80 kV";''', '''    vpTL.textContent="SCANOGRAM · AP\\nplan range + DFOV";
    vpBL.textContent="lateral inset ↗";
    vpBR.textContent="RIGHT · 120 kV";''')
rep("""        [0.6,3,5].map(function(t)""", """        [1,3,5].map(function(t)""")
rep("""        ["Acquisition","120 kV · 0.6 mm collimation · pitch 0.8"],""", """        ["Acquisition","120 kV · 0.625 mm collimation · pitch 0.9"],""")
rep("""'<div class="scg-hint">The preview on the left is the carpus reconstructed with these settings. Coronal and sagittal reformats are built from the axial slices — their quality depends on the slice thickness.</div>';""",
    """'<div class="scg-hint">The preview on the left is the proximal femur (intertrochanteric region) reconstructed with these settings. Coronal and sagittal reformats are built from the axial slices — their quality depends on the slice thickness.</div>';""")
rep('''    vpTL.textContent="PREVIEW · AXIAL CARPUS\\n"''', '''    vpTL.textContent="PREVIEW · AXIAL PROXIMAL FEMUR\\n"''')
rep("""    railDesc.textContent="Helical wrist scan in progress";""", """    railDesc.textContent="Helical femur scan in progress";""")
rep("""      ["Collimation","0.6 mm · pitch 0.8"],
      ["Direction","Distal → proximal"]
    ])+'<div class="scg-hint">“Keep your hand completely still…” Acquiring the wrist…</div>';""",
"""      ["Collimation","0.625 mm · pitch 0.9"],
      ["Direction","Knee → hip (feet first)"]
    ])+'<div class="scg-hint">“Keep your legs completely still…” Acquiring the femur…</div>';""")
rep("""        ["Series","Wrist · "+(S.kernel==="bone"?"bone":"soft-tissue")+" kernel · "+S.thick+" mm"],
        ["Axial", rangeKs().length+" images (every 1.5 mm)"],
        ["DFOV", dfov().toFixed(0)+" mm · pixel "+(Math.max(dfov()/512,SP)).toFixed(2)+" mm"],""",
"""        ["Series","Femur · "+(S.kernel==="bone"?"bone":"soft-tissue")+" kernel · "+S.thick+" mm"],
        ["Axial", rangeKs().length+" images (every 2 mm)"],
        ["DFOV", dfov().toFixed(0)+" mm · pixel "+(dfov()/512).toFixed(2)+" mm"],""")

# ---------------------------------------------------------------- set-up actions
block("/* =============================================================\n   PATIENT SET-UP (prone, head first, arm overhead)", "var THREE_URL", r'''/* =============================================================
   PATIENT SET-UP (supine, feet first: arms + feet)
   ============================================================= */
function poseChanged(){
  if(room3d) room3d.setPose({ arms:S.arms||"side", feet:S.feet||"relaxed" });
  setRoomCaption(); render();
}
function chooseArms(a){
  if(S.loaded || S.loading || S.arms===a) return;
  if(!S.armsFirst) S.armsFirst=a;
  S.arms=a;
  if(a==="chest") log("<b>arms folded on the chest</b>: well clear of the hips and upper thighs — no streaks from the hands or forearms.","ok");
  else log("with the arms by the side the <b>hands and forearms lie beside the hips</b> — right in the beam for the hip and proximal femur: streaks, noise and extra dose.","warn");
  poseChanged();
  if(S.arms && S.feet) log("Command: <b>load</b>"+(S.armsFirst!==a?"  (arms graded on your first choice)":""),"sys");
}
function chooseFeet(f){
  if(S.loaded || S.loading || S.feet===f) return;
  if(!S.feetFirst) S.feetFirst=f;
  S.feet=f;
  if(f==="taped") log("<b>feet turned in ~15° and taped</b>: corrects femoral anteversion so the neck lies flat in the coronal plane, and the legs cannot roll during the scan.","ok");
  else log("relaxed feet <b>fall outward</b>: the femur rotates externally — the neck is foreshortened on the coronal images, and the legs can drift between the scanogram and the scan.","warn");
  poseChanged();
  if(S.arms && S.feet) log("Command: <b>load</b>"+(S.feetFirst!==f?"  (feet graded on your first choice)":""),"sys");
}
''')
rep("""      room3d.setPose(S.pos || "side");               // the patient arrives supine, arms by the side""",
    """      room3d.setPose({ arms:S.arms||"side", feet:S.feet||"relaxed" });   // arrives arms by the side, feet relaxed""")
rep("""  log("CT LEFT wrist requested. The patient is on the table, supine with the arms by the side — choose how they should lie.","sys");""",
    """  log("CT RIGHT femur requested. The patient is on the table supine, feet first, arms by the side and feet relaxed — set up the arms and the feet.","sys");""")
block("function loadPatient(){", "/* =============================================================\n   SCANOGRAM", r'''function loadPatient(){
  if(S.loaded || S.loading || !S.arms || !S.feet) return;
  S.loading=true; S.checkN=3;
  var finish=function(){
    S.checkN=checks().length; S.loading=false; S.loaded=true;
    $("scgRoomStep").textContent="right thigh centred in the bore · table zeroed at the knee";
    log("right thigh at isocentre. Command: <b>scout</b>","ok");
    render();
  };
  if(room3d){
    var stepTx=$("scgRoomStep");
    log("table moving — feet first toward the gantry…","sys");
    render();
    room3d.play(function(step){
      if(step===1){ S.checkN=5; stepTx.textContent="table moving feet first — the feet and knees lead into the bore"; }
      if(step===2){ S.checkN=6; stepTx.textContent="landmark: knee joint at the gantry lasers · table zeroed"; log("lasers on — knee joint landmarked, table position zeroed.","sys"); }
      if(step===3){ stepTx.textContent="moving to scan position — mid-thigh at isocentre"; }
      render();
    }, finish);
    return;
  }
  room.classList.remove("is-in"); void room.offsetWidth; room.classList.add("is-in");
  log("table moving — feet first into the gantry…","sys");
  render();
  var iv=setInterval(function(){
    S.checkN++; render();
    if(S.checkN>=checks().length){ clearInterval(iv); finish(); }
  }, 1050);
}

''')
rep("""  log("acquiring scanogram — PA + lateral…","sys");""", """  log("acquiring scanogram — AP + lateral…","sys");""")
rep("""    acquireScout("scout_ap","PA", function(){""", """    acquireScout("scout_ap","AP", function(){""")
rep("""  vpTL.textContent="ACQUIRING SCANOGRAM · "+tag+"\\n80 kV · 20 mA";""", """  vpTL.textContent="ACQUIRING SCANOGRAM · "+tag+"\\n120 kV · 35 mA";""")
rep("""  log("plan the scan: the box height is the <b>range</b> (metacarpal bases → distal radial metaphysis), its width the <b>DFOV</b> — snug to the wrist. Then <b>confirm</b>.","sys");""",
    """  log("plan the scan: the box height is the <b>range</b> (above the acetabular roof → below the knee joint), its width the <b>DFOV</b> — snug to the right thigh. Then <b>confirm</b>.","sys");""")
rep("""    if(!distalOK()) log("caution: the metacarpal bases / CMC joints are not fully covered.","warn");
    if(distalOver()) log("caution: the range runs on into the fingers.","warn");
    if(!proxOK()) log("caution: the DRUJ / distal radius is not fully covered.","warn");
    if(clipMm().total>1) log("caution: the DFOV clips the wrist by "+clipMm().total.toFixed(0)+" mm.","warn");
    else if(!dfovSnug()) log("caution: the DFOV is much wider than the wrist.","warn");""",
"""    if(!proxOK()) log("caution: the hip joint is not fully covered.","warn");
    if(pelvisOver()) log("caution: the range runs on up into the pelvis.","warn");
    if(!distOK()) log("caution: the knee joint is not fully covered.","warn");
    if(clipMm().total>1) log("caution: the DFOV clips the thigh by "+clipMm().total.toFixed(0)+" mm.","warn");
    else if(!dfovSnug()) log("caution: the DFOV is much wider than the thigh.","warn");""")
rep("""  var seq=++previewSeq, k=Math.max(rangeKs()[0], Math.min(rangeKs()[rangeKs().length-1], CARPUS_K));""",
    """  var seq=++previewSeq, k=Math.max(rangeKs()[0], Math.min(rangeKs()[rangeKs().length-1], PREVIEW_K));""")
rep("""  acqTitle.textContent="ACQUIRING WRIST";
  var cov=lenMm(), total=Math.round(cov/0.6), n=0;""", """  acqTitle.textContent="ACQUIRING FEMUR";
  var cov=lenMm(), total=Math.round(cov/0.625), n=0;""")

# ---------------------------------------------------------------- grading
block("function computeScore(){", "/* =============================================================\n   RESULT / REVIEW", r'''function computeScore(){
  var rows=[], total=0;
  // 1) set-up (20)
  var af=S.armsFirst, aPts = af==="chest" ? 10 : 0;
  rows.push({ kind: aPts?"ok":"bad", title:"Arms", pts:aPts, max:10,
    body: af==="chest" ? "Folded on the chest — the hands and forearms are well clear of the hips and upper thighs."
        : "By the side was your first choice: the hands and forearms lie beside the hips, in the beam for the hip joint and proximal femur — beam-hardening streaks, noise and extra dose." +
          (S.arms==="side" ? " You can see the streaks over the hip and upper thigh on these images." : "") });
  var ff=S.feetFirst, fPts0 = ff==="taped" ? 10 : 3;
  rows.push({ kind: ff==="taped"?"ok":"warn", title:"Feet", pts:fPts0, max:10,
    body: ff==="taped" ? "Turned in ~15° and taped: the femoral neck lies flat in the coronal plane (anteversion corrected) and the legs cannot roll between the scanogram and the scan."
        : "Relaxed feet was your first choice: the legs roll outward, so the femoral neck is foreshortened on coronal images and the limb can move after the scanogram. Turn the feet in ~15° and tape them." });
  // 2) coverage (35)
  var t=topMm(), b=botMm();
  var pPts = proxOK() ? 15 : (proxHead() ? 6 : 0);
  rows.push({ kind:proxOK()?"ok":(pPts?"warn":"bad"), title:"Proximal limit · hip", pts:pPts, max:15,
    body: proxOK() ? "Starts above the acetabular roof — the whole hip joint, femoral head and neck are included."
        : proxHead() ? "Cuts through the femoral head — the top of the head and the acetabular roof are missing."
        : "Starts at the "+zLabel(t)+" — the femoral head and neck, the commonest site of a fracture after a fall, are not covered." });
  var dPts = distOK() ? 15 : (distCond() ? 6 : 0);
  rows.push({ kind:distOK()?"ok":(dPts?"warn":"bad"), title:"Distal limit · knee", pts:dPts, max:15,
    body: distOK() ? "Runs through the knee joint to the top of the tibial plateau — both joints of the femur are included."
        : distCond() ? "Stops in the femoral condyles, "+Math.round(LM.condyle_bot+3-b)+" mm short of the knee joint — intra-articular extension would be missed."
        : "Stops at the "+zLabel(b)+" — the distal femur and knee joint are not covered." });
  var over = (LM.head_top-6) - t, oPts = pelvisOver() ? 0 : 5;
  rows.push({ kind:oPts?"ok":"warn", title:"Dose · range length ("+lenMm().toFixed(0)+" mm)", pts:oPts, max:5,
    body: !pelvisOver() ? "No scanning far above the hip joint — the pelvis is not irradiated needlessly."
        : "The range starts "+Math.round(over)+" mm above the acetabular roof — extra dose to the pelvis and its organs that adds nothing to a femur study." });
  // 3) DFOV (25)
  var c=clipMm(), w=dfov(), ex=w-needW(), fPts, fBody;
  if(c.total>4){ fPts=0; fBody="The DFOV clips "+c.total.toFixed(0)+" mm of the thigh ("+[c.l>1?"lateral side":"",c.r>1?"medial side":"",c.ap>1?"front–back depth":""].filter(Boolean).join(", ")+") — anatomy outside the box is simply not reconstructed."; }
  else if(c.total>1){ fPts=12; fBody="The DFOV just shaves the skin edge ("+c.total.toFixed(0)+" mm) — the femur is intact but the soft tissues are incomplete."; }
  else if(ex<=30){ fPts=25; fBody="DFOV "+w.toFixed(0)+" mm, snug to the right thigh: "+(w/512).toFixed(2)+" mm pixels — the finest display matrix for cortex and trabecular detail."; }
  else if(ex<=60){ fPts=15; fBody="DFOV "+w.toFixed(0)+" mm is "+ex.toFixed(0)+" mm wider than the thigh needs — bigger pixels ("+(w/512).toFixed(2)+" mm) and a smaller femur on screen."; }
  else { fPts=6; fBody="DFOV "+w.toFixed(0)+" mm is far wider than the thigh ("+(w/512).toFixed(2)+" mm pixels) — the 512 matrix is wasted on air."; }
  rows.push({ kind:fPts===25?"ok":(fPts?"warn":"bad"), title:"Display FOV", pts:fPts, max:25, body:fBody });
  // 4) reconstruction (20)
  var kPts = S.kernel==="bone" ? 10 : 3;
  rows.push({ kind:S.kernel==="bone"?"ok":"warn", title:"Kernel", pts:kPts, max:10,
    body: S.kernel==="bone" ? "Sharp bone kernel — crisp cortex and trabeculae."
        : "Soft-tissue kernel only — smoother and less noisy, but cortical breaks and trabecular detail blur. Reconstruct a bone-kernel series first (add soft tissue as an extra for haematoma or muscle)." });
  var tPts = S.thick===1 ? 10 : S.thick===3 ? 4 : 0;
  rows.push({ kind:tPts===10?"ok":(tPts?"warn":"bad"), title:"Slice thickness ("+S.thick+" mm)", pts:tPts, max:10,
    body: S.thick===1 ? "Thin slices — the coronal and sagittal reformats keep the detail along the length of the femur."
        : "Thick axial slices smear the reformats along the femur: "+(S.thick===5?"undisplaced neck and shaft fractures can vanish on the coronal and sagittal images.":"fine fracture lines lose definition on the coronal and sagittal images.") });
  rows.forEach(function(r){ total+=r.pts; });
  return { rows:rows, total:total };
}

''')
rep("""var DEFAULT_COR_Y = 58, DEFAULT_SAG_X = 98;            // carpus: scaphoid / capitate–lunate–radius column""",
    """var DEFAULT_COR_Y = 115, DEFAULT_SAG_X = 127;          // through the femoral shaft (AP mm from the front / scout mm)""")
rep("""  var target = p==="ax" ? CARPUS_K : null,""", """  var target = p==="ax" ? PREVIEW_K : null,""")
rep("""  var L = p==="ax" ? ["DORSAL","VOLAR","ULNAR","RADIAL"] : p==="cor" ? ["DISTAL","PROXIMAL","ULNAR","RADIAL"] : ["DISTAL","PROXIMAL","VOLAR","DORSAL"];""",
    """  var L = p==="ax" ? ["ANT","POST","R","L"] : p==="cor" ? ["SUP","INF","R","L"] : ["SUP","INF","ANT","POST"];""")
block("  var sc=computeScore(); S.score=sc.total;", "  log(\"study complete", r'''  var sc=computeScore(); S.score=sc.total;
  var c=clipMm(), missHip=!proxHead(), missKnee=!distCond();
  watermark.classList.toggle("scg-hidden", !(c.total>4 || missHip || missKnee));
  if(c.total>4) watermarkTx.innerHTML="THIGH CLIPPED<br>BY THE DFOV";
  else if(missHip) watermarkTx.innerHTML="FEMORAL HEAD<br>NOT COVERED";
  else if(missKnee) watermarkTx.innerHTML="KNEE JOINT<br>NOT COVERED";

  var pct=sc.total, gcls = pct>=85 ? "" : pct>=60 ? "is-warn" : "is-bad";
  var verdict = pct===100 ? "Perfect study" : pct>=85 ? "Diagnostic femur CT" : pct>=60 ? "Diagnostic with limitations" : "Repeat recommended";
  var good = pct>=85;
  resultEl.classList.remove("scg-hidden");
  resultEl.innerHTML =
    '<div>'+
      '<h2 class="'+(good?"":"is-bad")+'">'+(good?"Hip to knee covered and sharply reconstructed":"Study limited by the set-up, plan or reconstruction")+'</h2>'+
      '<div class="scg-cap">Coronal reformat through the femur, built from <b>your</b> axial slices with your kernel, thickness and DFOV. Check the femoral head and neck, the trochanters, the cortex along the shaft and the condyles. This is a teaching scan from a research collection — no fracture is marked in the source data.</div>'+
      '<div class="scg-hero"><img id="scgHeroImg" alt="Coronal reformat of the femur with your reconstruction settings"><div class="scg-hero-lab">CORONAL REFORMAT · FEMUR\n'+(S.kernel==="bone"?"bone":"soft-tissue")+' kernel · '+S.thick+' mm · bone window</div><div class="scg-hero-hu">DFOV '+dfov().toFixed(0)+' mm\nrange '+lenMm().toFixed(0)+' mm</div></div>'+
    '</div>'+
    '<div class="scg-debrief">'+
      '<div class="scg-grade '+gcls+'"><b>'+pct+'%</b><span>'+verdict.toUpperCase()+'<br>'+ARMS[S.arms].short+' · '+FEET[S.feet].short+
        '<div class="scg-bar"><i style="width:'+pct+'%;background:'+(gcls?(gcls==="is-warn"?"var(--warn)":"var(--bad)"):"var(--accent)")+'"></i></div></span></div>'+
      sc.rows.map(function(r){ return drow(r.kind, r.title, r.body, r.pts+" / "+r.max); }).join('')+
      '<button class="scg-again" id="scgAgain">⟲ '+(pct===100?"Scan another way":"Try again")+'</button>'+
    '</div>'+
    '<div class="scg-credits">'+CREDITS+'</div>';
  $("scgAgain").onclick=function(){ logCmd("reset"); resetAll(); };

  var cl=planeList("cor");
  renderMPR("cor", defaultIndex("cor", cl), function(cv){ var h=$("scgHeroImg"); if(h && cv) h.src=cv.toDataURL("image/jpeg",0.92); });

''')
rep("""  if(perfect){ log("★ MARKER UNLOCKED — Superman Scanned","ok"); setTimeout(playAchievement, 60); }""",
    """  if(perfect){ log("★ MARKER UNLOCKED — Slice of the Thigh","ok"); setTimeout(playAchievement, 60); }""")
block("var CREDITS =", "/* ---- stack scrolling ---- */", r'''var CREDITS =
  '<b>Imaging credit.</b> Adapted from: Aldieri A, La Mattina AA, Szyszko JA, Baruffaldi F, Viceconti M. <i>HFValid collection: Hip-Fracture validation collection</i> [Dataset]. University of Bologna, AMS Acta, 2023, '+
  '<a href="https://doi.org/10.6092/unibo/amsacta/7277" target="_blank" rel="noopener">doi:10.6092/unibo/amsacta/7277</a> '+
  '(<a href="https://amsacta.unibo.it/id/eprint/7277/" target="_blank" rel="noopener">amsacta.unibo.it/id/eprint/7277</a>) — subject Pat001, calibrated CT of the right femur (0.70 mm pixels, 2 mm slices), '+
  'licensed <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">CC BY 4.0</a>. '+
  '<b>Changes made:</b> the AP and lateral scanograms are simulated projections through the CT volume (not acquired localisers), with the couch removed, padded with air and colour-tinted; the dataset’s field is cropped near the midline, so the scanogram shows the right side only and the cropped edge is faded; '+
  'axial images are the native 2 mm slices and coronal / sagittal reformats are 1.4 mm slabs every 3 mm with the 2 mm slice spacing interpolated to 0.7 mm, re-encoded as JPEG; '+
  'in your browser the images are cropped and resampled to the chosen DFOV, blurred to simulate a soft-tissue kernel, and averaged / smeared to simulate thicker slices — the source’s thinnest slices are 2 mm, so the “1 mm” series shows the native 2 mm data; '+
  'if the arms are left by the side, streaks and noise are added over the hip and upper thigh to simulate the hands in the beam. The arm and foot positions are simulated choices — the source scan was acquired for hip-replacement planning. '+
  'The patient position and request are fictional. The 3-D patient-positioning scene is original (built with three.js, MIT licence). Neither the dataset authors nor the University of Bologna endorse this simulator.';

''')
rep('''  vpBR.textContent="Im "+(i+1)+" / "+n+"\\n"+(S.win==="bone"?"WL 450 WW 1800":"WL 50 WW 400");
  vpTL.textContent="CT LEFT WRIST · "''', '''  vpBR.textContent="Im "+(i+1)+" / "+n+"\\n"+(S.win==="bone"?"WL 450 WW 1800":"WL 50 WW 400");
  vpTL.textContent="CT RIGHT FEMUR · "''')
rep('''"plane "+(SAG_X[S.stackK]-PAD).toFixed(0)+" mm";''', '''"plane "+(SAG_X[S.stackK]-PAD).toFixed(0)+" mm from lateral";''')
rep('''S.kernel==="bone"?"bone":"soft-tissue")+" kernel · "+S.thick+" mm";
  vpBL.textContent = S.plane==="ax" ? zLabel(AX[S.stackK].z) : S.plane==="cor" ? "depth "''', '''S.kernel==="bone"?"bone":"soft-tissue")+" kernel · "+S.thick+" mm";
  vpBL.textContent = S.plane==="ax" ? zLabel(AX[S.stackK].z) : S.plane==="cor" ? "depth "''')
block("function resetAll(){", "  resultEl.classList.add(\"scg-hidden\");", r'''function resetAll(){
  var a=S.arms, af=S.armsFirst, f=S.feet, ff=S.feetFirst;
  S = freshState();
  S.arms=a; S.armsFirst=af; S.feet=f; S.feetFirst=ff; S.loaded=true;   // patient stays on the table, set-up already graded
''')
rep("""  log("THE SCANOGRAM · CT wrist simulator","sys");""", """  log("THE SCANOGRAM · CT femur simulator","sys");""")
open(P, "w", encoding="utf-8").write(s)

left = [w for w in ["wrist", "Wrist", "WRIST", "carpus", "S.pos", "POS[", "FIELD", "distalOK", "superman", "Superman", "CARPUS"] if w in s]
print("leftovers:", left)
for w in left:
    for m in re.finditer(re.escape(w), s):
        ln = s.count("\n", 0, m.start()) + 1
        print(" ", w, ln, s.splitlines()[ln - 1].strip()[:110])
