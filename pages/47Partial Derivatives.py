import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Partial Derivatives", layout="wide")

def render_lab():
    html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Inter',sans-serif;background:#0f172a;color:white;padding:20px;}
.outer{display:flex;flex-direction:column;gap:20px;max-width:1100px;margin:0 auto;}
.top{display:flex;flex-direction:row;gap:20px;}
.controls{flex:1;display:flex;flex-direction:column;gap:14px;}
.viz-col{flex:1.6;display:flex;flex-direction:column;gap:12px;}
.card{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:14px;padding:16px;}
h2{font-size:22px;font-weight:900;color:#f8fafc;margin-bottom:4px;}
.sub{font-size:13px;color:#94a3b8;line-height:1.5;}
.func-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;}
.fbtn{background:rgba(255,255,255,0.05);color:#cbd5e1;border:1px solid rgba(255,255,255,0.1);padding:8px 4px;border-radius:9px;font-weight:700;cursor:pointer;transition:.2s;text-align:center;font-size:12px;}
.fbtn:hover{background:rgba(255,255,255,0.1);}
.fbtn.active{background:rgba(167,139,250,.2);border-color:#a78bfa;color:#a78bfa;box-shadow:0 0 12px rgba(167,139,250,.3);}
.mode-row{display:flex;gap:8px;}
.mbtn{flex:1;background:rgba(255,255,255,0.05);color:#cbd5e1;border:1px solid rgba(255,255,255,0.1);padding:9px 4px;border-radius:8px;font-weight:700;cursor:pointer;transition:.2s;font-size:12px;}
.mbtn:hover{background:rgba(255,255,255,0.1);}
.mbtn[data-m="both"].active{background:rgba(167,139,250,.2);border-color:#a78bfa;color:#a78bfa;}
.mbtn[data-m="x"].active{background:rgba(255,209,102,.2);border-color:#FFD166;color:#FFD166;}
.mbtn[data-m="y"].active{background:rgba(78,205,196,.2);border-color:#4ECDC4;color:#4ECDC4;}
.slabel{display:flex;justify-content:space-between;font-size:13px;font-weight:700;margin-bottom:8px;}
.sval{font-size:16px;font-weight:900;font-variant-numeric:tabular-nums;}
input[type=range]{width:100%;height:6px;background:rgba(255,255,255,0.1);border-radius:3px;outline:none;-webkit-appearance:none;margin-bottom:12px;}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:20px;height:20px;border-radius:50%;cursor:pointer;}
#xs::-webkit-slider-thumb{background:#FFD166;box-shadow:0 0 8px #FFD166;}
#ys::-webkit-slider-thumb{background:#4ECDC4;box-shadow:0 0 8px #4ECDC4;}
.mbox{background:rgba(0,0,0,.3);border-radius:12px;padding:14px;border:1px solid rgba(255,255,255,.06);display:flex;flex-direction:column;gap:10px;}
.mrow{display:flex;justify-content:space-between;align-items:center;}
.meq{font-family:monospace;font-size:14px;font-weight:bold;}
.mval{font-family:monospace;font-size:17px;font-weight:900;background:rgba(0,0,0,.5);padding:3px 9px;border-radius:6px;font-variant-numeric:tabular-nums;}
.sep{border-top:1px dashed rgba(255,255,255,.15);padding-top:10px;}
canvas{border-radius:12px;border:1px solid rgba(255,255,255,.08);display:block;width:100%;}
.clabel{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;color:#94a3b8;}
.cvs-wrap{display:flex;flex-direction:column;}
.auto-btn{background:rgba(78,205,196,.15);color:#4ECDC4;border:1px solid rgba(78,205,196,.4);padding:10px;border-radius:8px;font-weight:800;cursor:pointer;width:100%;font-size:12px;letter-spacing:1px;transition:.2s;}
.auto-btn:hover{background:rgba(78,205,196,.3);}
</style>
</head>
<body>
<div class="outer">
  <div class="top">
    <div class="controls">
      <div class="card">
        <h2>The 3D Slicer 🔪</h2>
        <p class="sub">Pick a surface, slice it in one direction. The slice reveals a 2D curve — and its slope is the partial derivative!</p>
      </div>
      <div class="card">
        <div class="clabel">Surface Function</div>
        <div class="func-grid" id="fbtns">
          <button class="fbtn active" data-t="bowl">Bowl<br>x²+y²</button>
          <button class="fbtn" data-t="saddle">Saddle<br>x²−y²</button>
          <button class="fbtn" data-t="wave">Wave<br>sin+cos</button>
        </div>
      </div>
      <div class="card">
        <div class="clabel">Slice Direction</div>
        <div class="mode-row" id="mbtns">
          <button class="mbtn active" data-m="both">Full 3D</button>
          <button class="mbtn" data-m="x">∂/∂x slice</button>
          <button class="mbtn" data-m="y">∂/∂y slice</button>
        </div>
      </div>
      <div class="card">
        <div class="slabel" style="color:#FFD166"><span>X Position</span><span id="xv" class="sval" style="color:#FFD166">0.00</span></div>
        <input type="range" id="xs" min="-3" max="3" step="0.05" value="1">
        <div class="slabel" style="color:#4ECDC4"><span>Y Position</span><span id="yv" class="sval" style="color:#4ECDC4">0.00</span></div>
        <input type="range" id="ys" min="-3" max="3" step="0.05" value="1">
        <button class="auto-btn" id="abtn">✨ AUTO-SWEEP</button>
      </div>
      <div class="mbox">
        <div class="mrow"><span class="meq" id="feq" style="color:#a78bfa">f(x,y)</span><span class="mval" id="fv" style="color:#a78bfa">0.00</span></div>
        <div class="sep">
          <div class="mrow"><span class="meq" id="dxeq" style="color:#FFD166">∂f/∂x</span><span class="mval" id="dxv" style="color:#FFD166">0.00</span></div>
        </div>
        <div class="mrow"><span class="meq" id="dyeq" style="color:#4ECDC4">∂f/∂y</span><span class="mval" id="dyv" style="color:#4ECDC4">0.00</span></div>
      </div>
    </div>

    <div class="viz-col">
      <div class="cvs-wrap">
        <div class="clabel">3D Surface View (Isometric Projection)</div>
        <canvas id="cvs3d" width="640" height="420"></canvas>
      </div>
      <div style="display:flex;gap:12px;">
        <div class="cvs-wrap" style="flex:1">
          <div class="clabel" style="color:#FFD166">X-Slice: fix y, vary x → ∂f/∂x</div>
          <canvas id="cvsx" width="300" height="160"></canvas>
        </div>
        <div class="cvs-wrap" style="flex:1">
          <div class="clabel" style="color:#4ECDC4">Y-Slice: fix x, vary y → ∂f/∂y</div>
          <canvas id="cvsy" width="300" height="160"></canvas>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
const funcs = {
  bowl:{
    f:(x,y)=>0.25*(x*x+y*y)-1.5,
    dx:(x,y)=>0.5*x, dy:(x,y)=>0.5*y,
    sf:"f(x,y) = 0.25x² + 0.25y²", sdx:"∂f/∂x = 0.5x", sdy:"∂f/∂y = 0.5y"
  },
  saddle:{
    f:(x,y)=>0.25*(x*x-y*y),
    dx:(x,y)=>0.5*x, dy:(x,y)=>-0.5*y,
    sf:"f(x,y) = 0.25x² − 0.25y²", sdx:"∂f/∂x = 0.5x", sdy:"∂f/∂y = −0.5y"
  },
  wave:{
    f:(x,y)=>1.5*Math.sin(x)+1.5*Math.cos(y),
    dx:(x,y)=>1.5*Math.cos(x), dy:(x,y)=>-1.5*Math.sin(y),
    sf:"f(x,y) = 1.5sin(x) + 1.5cos(y)", sdx:"∂f/∂x = 1.5cos(x)", sdy:"∂f/∂y = −1.5sin(y)"
  }
};

let curF='bowl', curM='both', autoInv=null, autoDir=1;
const xs=document.getElementById('xs'), ys=document.getElementById('ys');
const xv=document.getElementById('xv'), yv=document.getElementById('yv');
const fvEl=document.getElementById('fv'), feqEl=document.getElementById('feq');
const dxvEl=document.getElementById('dxv'), dxeqEl=document.getElementById('dxeq');
const dyvEl=document.getElementById('dyv'), dyeqEl=document.getElementById('dyeq');
const abtn=document.getElementById('abtn');

const c3=document.getElementById('cvs3d'), ctx3=c3.getContext('2d');
const cx2=document.getElementById('cvsx'), ctxX=cx2.getContext('2d');
const cy2=document.getElementById('cvsy'), ctxY=cy2.getContext('2d');

// Isometric projection
const ISO = { ax: Math.cos(Math.PI/6), ay: Math.sin(Math.PI/6) };
const SCALE = 52, YSCALE = 40;
const OX = c3.width/2, OY = c3.height*0.55;

function iso(mx, mz, my) {
  // mx=world-x, mz=world-z (depth), my=height
  const px = OX + (mx - mz) * ISO.ax * SCALE;
  const py = OY - (mx + mz) * ISO.ay * SCALE - my * YSCALE;
  return {px, py};
}

function drawSurface3D() {
  ctx3.clearRect(0,0,c3.width,c3.height);
  // dark bg
  ctx3.fillStyle='#1e293b';
  ctx3.fillRect(0,0,c3.width,c3.height);

  const fn=funcs[curF];
  const tx=parseFloat(xs.value), ty=parseFloat(ys.value);
  const tz=fn.f(tx,ty);
  const sdx=fn.dx(tx,ty), sdy=fn.dy(tx,ty);
  const N=28, R=3.0, step=2*R/N;

  // Draw grid surface (back to front for painter's algo)
  for(let i=N-1;i>=0;i--) {
    for(let j=N-1;j>=0;j--) {
      const x0=-R+j*step, x1=x0+step;
      const z0=-R+i*step, z1=z0+step;
      const y00=fn.f(x0,z0), y10=fn.f(x1,z0);
      const y01=fn.f(x0,z1), y11=fn.f(x1,z1);
      const p00=iso(x0,z0,y00), p10=iso(x1,z0,y10);
      const p01=iso(x0,z1,y01), p11=iso(x1,z1,y11);
      const avgY=(y00+y10+y01+y11)/4;

      // Color: purple base, modulated by height
      const t=Math.max(0,Math.min(1,(avgY+2)/4));

      // Slice highlight
      const onXslice = curM==='x' && Math.abs((z0+z1)/2 - ty) < step*1.5;
      const onYslice = curM==='y' && Math.abs((x0+x1)/2 - tx) < step*1.5;

      let r,g,b,a=0.85;
      if(onXslice){r=255;g=209;b=102;a=0.95;}
      else if(onYslice){r=78;g=205;b=196;a=0.95;}
      else {
        r=Math.round(100+t*80); g=Math.round(80+t*60); b=Math.round(200+t*55);
        if(curM!=='both') a=0.25;
      }

      ctx3.beginPath();
      ctx3.moveTo(p00.px,p00.py);
      ctx3.lineTo(p10.px,p10.py);
      ctx3.lineTo(p11.px,p11.py);
      ctx3.lineTo(p01.px,p01.py);
      ctx3.closePath();
      ctx3.fillStyle=`rgba(${r},${g},${b},${a})`;
      ctx3.fill();
      ctx3.strokeStyle='rgba(0,0,0,0.15)';
      ctx3.lineWidth=0.5;
      ctx3.stroke();
    }
  }

  // Draw X-slice curve (vary x, fix y=ty)
  if(curM==='x'||curM==='both') {
    ctx3.beginPath();
    for(let j=0;j<=N*2;j++){
      const x=-R+j*(2*R/(N*2));
      const y=fn.f(x,ty);
      const p=iso(x,ty,y);
      j===0?ctx3.moveTo(p.px,p.py):ctx3.lineTo(p.px,p.py);
    }
    ctx3.strokeStyle='#FFD166'; ctx3.lineWidth=3;
    ctx3.shadowColor='#FFD166'; ctx3.shadowBlur=10;
    ctx3.stroke(); ctx3.shadowBlur=0;

    // X-tangent line
    const d=1.8;
    const p1=iso(tx-d,ty,tz-d*sdx), p2=iso(tx+d,ty,tz+d*sdx);
    ctx3.beginPath(); ctx3.moveTo(p1.px,p1.py); ctx3.lineTo(p2.px,p2.py);
    ctx3.strokeStyle='#fff'; ctx3.lineWidth=2.5;
    ctx3.setLineDash([6,4]); ctx3.stroke(); ctx3.setLineDash([]);
  }

  // Draw Y-slice curve (vary y, fix x=tx)
  if(curM==='y'||curM==='both') {
    ctx3.beginPath();
    for(let i=0;i<=N*2;i++){
      const z=-R+i*(2*R/(N*2));
      const y=fn.f(tx,z);
      const p=iso(tx,z,y);
      i===0?ctx3.moveTo(p.px,p.py):ctx3.lineTo(p.px,p.py);
    }
    ctx3.strokeStyle='#4ECDC4'; ctx3.lineWidth=3;
    ctx3.shadowColor='#4ECDC4'; ctx3.shadowBlur=10;
    ctx3.stroke(); ctx3.shadowBlur=0;

    // Y-tangent line
    const d=1.8;
    const p1=iso(tx,ty-d,tz-d*sdy), p2=iso(tx,ty+d,tz+d*sdy);
    ctx3.beginPath(); ctx3.moveTo(p1.px,p1.py); ctx3.lineTo(p2.px,p2.py);
    ctx3.strokeStyle='#fff'; ctx3.lineWidth=2.5;
    ctx3.setLineDash([6,4]); ctx3.stroke(); ctx3.setLineDash([]);
  }

  // Point
  const pp=iso(tx,ty,tz);
  ctx3.beginPath();
  ctx3.arc(pp.px,pp.py,7,0,Math.PI*2);
  ctx3.fillStyle='#fff';
  ctx3.shadowColor='#fff'; ctx3.shadowBlur=15;
  ctx3.fill(); ctx3.shadowBlur=0;
}

// --- 2D slice canvases ---
function draw2D(cvs, ctx, color, label, xArr, yArr, px, py, slope) {
  const W=cvs.width, H=cvs.height;
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='#1e293b';
  ctx.fillRect(0,0,W,H);

  const pad=28;
  const yw=H-pad*2, xw=W-pad*2;

  // find range
  let mnY=Infinity,mxY=-Infinity;
  for(const v of yArr){if(v<mnY)mnY=v;if(v>mxY)mxY=v;}
  mnY-=0.5; mxY+=0.5;
  const mnX=xArr[0], mxX=xArr[xArr.length-1];

  function sc(mx,my){
    return {
      sx: pad+(mx-mnX)/(mxX-mnX)*xw,
      sy: pad+(1-(my-mnY)/(mxY-mnY))*yw
    };
  }

  // grid
  ctx.strokeStyle='rgba(255,255,255,0.04)';
  ctx.lineWidth=1;
  for(let i=0;i<=4;i++){
    const y=mnY+i*(mxY-mnY)/4;
    const {sx:x0,sy:y0}=sc(mnX,y);
    const {sx:x1}=sc(mxX,y);
    ctx.beginPath(); ctx.moveTo(x0,y0); ctx.lineTo(x1,y0); ctx.stroke();
  }

  // axes
  ctx.strokeStyle='rgba(255,255,255,0.2)';
  ctx.lineWidth=1.5;
  const origin0=sc(mnX,0), origin1=sc(mxX,0);
  ctx.beginPath(); ctx.moveTo(origin0.sx,origin0.sy); ctx.lineTo(origin1.sx,origin1.sy); ctx.stroke();

  // curve
  ctx.beginPath();
  for(let i=0;i<xArr.length;i++){
    const {sx,sy}=sc(xArr[i],yArr[i]);
    i===0?ctx.moveTo(sx,sy):ctx.lineTo(sx,sy);
  }
  ctx.strokeStyle=color; ctx.lineWidth=2.5;
  ctx.shadowColor=color; ctx.shadowBlur=8;
  ctx.stroke(); ctx.shadowBlur=0;

  // tangent
  const ext=0.8*(mxX-mnX)/2;
  const t1=sc(px-ext, py-slope*ext), t2=sc(px+ext, py+slope*ext);
  ctx.beginPath(); ctx.moveTo(t1.sx,t1.sy); ctx.lineTo(t2.sx,t2.sy);
  ctx.strokeStyle='rgba(255,255,255,0.7)'; ctx.lineWidth=1.8;
  ctx.setLineDash([5,4]); ctx.stroke(); ctx.setLineDash([]);

  // point
  const {sx:bx,sy:by}=sc(px,py);
  ctx.beginPath(); ctx.arc(bx,by,5,0,Math.PI*2);
  ctx.fillStyle=color;
  ctx.shadowColor=color; ctx.shadowBlur=12;
  ctx.fill(); ctx.shadowBlur=0;

  // slope label
  ctx.fillStyle='rgba(255,255,255,0.9)';
  ctx.font='bold 12px monospace';
  ctx.fillText(`slope=${slope.toFixed(2)}`, bx+8, by-8);
}

function update() {
  const fn=funcs[curF];
  const tx=parseFloat(xs.value), ty=parseFloat(ys.value);
  const tz=fn.f(tx,ty);
  const sdx=fn.dx(tx,ty), sdy=fn.dy(tx,ty);

  xv.innerText=tx.toFixed(2); yv.innerText=ty.toFixed(2);
  feqEl.innerText=fn.sf; fvEl.innerText=tz.toFixed(2);
  dxeqEl.innerText=fn.sdx; dxvEl.innerText=sdx.toFixed(2);
  dyeqEl.innerText=fn.sdy; dyvEl.innerText=sdy.toFixed(2);

  // dim/highlight math
  const xDim = curM==='y' ? '0.3' : '1';
  const yDim = curM==='x' ? '0.3' : '1';
  dxeqEl.style.opacity=xDim; dxvEl.style.opacity=xDim;
  dyeqEl.style.opacity=yDim; dyvEl.style.opacity=yDim;

  drawSurface3D();

  // Build 2D slice data
  const N=80, R=3.0;
  const xArrX=[], yArrX=[];
  for(let i=0;i<=N;i++){const x=-R+i*2*R/N; xArrX.push(x); yArrX.push(fn.f(x,ty));}
  draw2D(cx2,ctxX,'#FFD166','x',xArrX,yArrX,tx,tz,sdx);

  const xArrY=[], yArrY=[];
  for(let i=0;i<=N;i++){const y=-R+i*2*R/N; xArrY.push(y); yArrY.push(fn.f(tx,y));}
  draw2D(cy2,ctxY,'#4ECDC4','y',xArrY,yArrY,ty,tz,sdy);
}

// Events
document.querySelectorAll('.fbtn').forEach(b=>{
  b.addEventListener('click', e=>{
    document.querySelectorAll('.fbtn').forEach(x=>x.classList.remove('active'));
    e.target.classList.add('active');
    curF=e.target.dataset.t;
    update();
  });
});
document.querySelectorAll('.mbtn').forEach(b=>{
  b.addEventListener('click', e=>{
    document.querySelectorAll('.mbtn').forEach(x=>x.classList.remove('active'));
    e.target.classList.add('active');
    curM=e.target.dataset.m;
    update();
  });
});
xs.addEventListener('input', ()=>{stopAuto();update();});
ys.addEventListener('input', ()=>{stopAuto();update();});

function stopAuto(){
  if(autoInv){clearInterval(autoInv);autoInv=null;abtn.innerText='✨ AUTO-SWEEP';}
}
abtn.addEventListener('click',()=>{
  if(autoInv){stopAuto();}
  else{
    abtn.innerText='⏸ PAUSE';
    autoInv=setInterval(()=>{
      let x=parseFloat(xs.value)+0.04*autoDir;
      if(x>3){x=3;autoDir=-1;}
      if(x<-3){x=-3;autoDir=1;}
      xs.value=x; update();
    },30);
  }
});

update();
</script>
</body>
</html>
"""
    components.html(html_code, height=780, scrolling=False)


def main():
    st.title("⛰️ Page 47: Partial Derivatives")

    st.markdown(
        """
        You've mastered derivatives for functions of **one variable**. But what if your function depends on **two variables** — like altitude on a map depending on both East/West ($x$) and North/South ($y$)?

        A **partial derivative** answers: *"If I only move in the x-direction and freeze y completely, how steep is the slope?"*
        It's just a regular derivative — with a twist: **pretend all other variables are constants**.
        """
    )

    st.divider()
    st.markdown("### 1) The 3D Slicer Lab 🔪")
    st.markdown(
        "Move the **X/Y sliders** to place your point on the surface. Switch to **∂/∂x slice** to freeze y and see the 2D curve you get — that curve's slope is the partial derivative in x. Same idea for y."
    )

    render_lab()

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### The Rule: $\\frac{\\partial f}{\\partial x}$")
        st.info("**Freeze all other variables. Differentiate normally in x.**")
        st.markdown(
            r"""
**Example:** $f(x, y) = x^2 + 3xy + y^2$

$$\frac{\partial f}{\partial x}: \quad x^2 \to 2x, \quad 3xy \to 3y, \quad y^2 \to 0$$

$$\boxed{\frac{\partial f}{\partial x} = 2x + 3y}$$
"""
        )

    with col2:
        st.markdown("### The Rule: $\\frac{\\partial f}{\\partial y}$")
        st.success("**Freeze all other variables. Differentiate normally in y.**")
        st.markdown(
            r"""
**Example:** $f(x, y) = x^2 + 3xy + y^2$

$$\frac{\partial f}{\partial y}: \quad x^2 \to 0, \quad 3xy \to 3x, \quad y^2 \to 2y$$

$$\boxed{\frac{\partial f}{\partial y} = 3x + 2y}$$
"""
        )

    st.divider()
    st.markdown("### 🤖 Bridge to AI: Why This is Everything")
    st.markdown(
        """
        A neural network has **millions of weights** — each one is a variable. The Loss function is a mountain in million-dimensional space.

        To find the bottom (minimum loss), the AI needs the slope in **every single weight's direction** — independently. That's a partial derivative for each weight!

        $$\\nabla_{\\mathbf{w}} L = \\left[\\frac{\\partial L}{\\partial w_1},\\ \\frac{\\partial L}{\\partial w_2},\\ \\dots,\\ \\frac{\\partial L}{\\partial w_n}\\right]$$

        This collection of all partial derivatives is called the **Gradient** — which is exactly what Page 48 is about!
        """
    )

    st.divider()
    st.markdown(
        '<div style="color:#94a3b8;font-size:0.95rem;">Page 47 — you can now slice multivariable surfaces in any direction. Next: combine all partials into a single uphill compass — The Gradient!</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
