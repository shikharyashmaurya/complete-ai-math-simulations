import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="The Gradient — Steepest Climb", layout="wide")

def render_lab():
    html = """
<!DOCTYPE html>
<html>
<head>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Inter',sans-serif;background:#0f172a;color:#fff;padding:16px;}
.wrap{max-width:1100px;margin:0 auto;display:flex;flex-direction:column;gap:16px;}
.row{display:flex;gap:16px;}
.card{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:14px;}
.col-l{flex:1;display:flex;flex-direction:column;gap:12px;}
.col-r{flex:1.7;display:flex;flex-direction:column;gap:12px;}
h2{font-size:20px;font-weight:900;margin-bottom:2px;}
.sub{font-size:12px;color:#94a3b8;line-height:1.5;}
.lbl{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#94a3b8;margin-bottom:6px;}
.func-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;}
.fbtn{background:rgba(255,255,255,.05);color:#cbd5e1;border:1px solid rgba(255,255,255,.1);padding:7px 4px;border-radius:8px;font-weight:700;cursor:pointer;font-size:11px;text-align:center;transition:.2s;}
.fbtn:hover{background:rgba(255,255,255,.1);}
.fbtn.active{background:rgba(251,146,60,.2);border-color:#fb923c;color:#fb923c;box-shadow:0 0 10px rgba(251,146,60,.3);}
.mode-row{display:flex;gap:6px;}
.mbtn{flex:1;background:rgba(255,255,255,.05);color:#cbd5e1;border:1px solid rgba(255,255,255,.1);padding:8px;border-radius:8px;font-weight:700;cursor:pointer;font-size:11px;transition:.2s;}
.mbtn:hover{background:rgba(255,255,255,.1);}
.mbtn.active{background:rgba(56,189,248,.2);border-color:#38bdf8;color:#38bdf8;}
canvas{border-radius:12px;border:1px solid rgba(255,255,255,.08);display:block;width:100%;}
.mbox{background:rgba(0,0,0,.3);border-radius:10px;padding:12px;border:1px solid rgba(255,255,255,.06);display:flex;flex-direction:column;gap:8px;}
.mr{display:flex;justify-content:space-between;align-items:center;}
.meq{font-family:monospace;font-size:13px;font-weight:bold;}
.mv{font-family:monospace;font-size:15px;font-weight:900;background:rgba(0,0,0,.5);padding:2px 8px;border-radius:5px;}
.sep{border-top:1px dashed rgba(255,255,255,.12);padding-top:8px;}
input[type=range]{width:100%;height:5px;background:rgba(255,255,255,.1);border-radius:3px;outline:none;-webkit-appearance:none;margin-bottom:10px;}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;background:#fb923c;box-shadow:0 0 8px #fb923c;cursor:pointer;}
.sl{display:flex;justify-content:space-between;font-size:12px;font-weight:700;margin-bottom:6px;}
.sv{font-size:14px;font-weight:900;font-variant-numeric:tabular-nums;}
.go-btn{background:rgba(52,211,153,.15);color:#34d399;border:1px solid rgba(52,211,153,.4);padding:9px;border-radius:8px;font-weight:800;cursor:pointer;width:100%;font-size:11px;letter-spacing:1px;transition:.2s;margin-top:4px;}
.go-btn:hover{background:rgba(52,211,153,.3);}
</style>
</head>
<body>
<div class="wrap">
 <div class="row">
  <div class="col-l">
   <div class="card">
    <h2>🧭 Gradient Compass</h2>
    <p class="sub">The gradient ∇f combines ALL partial derivatives into one arrow — pointing in the steepest uphill direction. Its length = how steep.</p>
   </div>
   <div class="card">
    <div class="lbl">Surface</div>
    <div class="func-grid" id="fbs">
     <button class="fbtn active" data-f="bowl">Bowl<br>x²+y²</button>
     <button class="fbtn" data-f="saddle">Saddle<br>x²−y²</button>
     <button class="fbtn" data-f="wave">Wave<br>sin·cos</button>
    </div>
   </div>
   <div class="card">
    <div class="lbl">Mode</div>
    <div class="mode-row" id="mbs">
     <button class="mbtn active" data-m="field">Arrow Field</button>
     <button class="mbtn" data-m="climb">🧗 Climber</button>
    </div>
   </div>
   <div class="card">
    <div class="sl" style="color:#fb923c"><span>X</span><span id="xvl" class="sv">0.00</span></div>
    <input type="range" id="xsl" min="-3" max="3" step=".05" value="0.5">
    <div class="sl" style="color:#4ECDC4"><span>Y</span><span id="yvl" class="sv">0.00</span></div>
    <input type="range" id="ysl" min="-3" max="3" step=".05" value="0.5">
    <button class="go-btn" id="climbBtn">🧗 START CLIMB / DESCENT</button>
   </div>
   <div class="mbox">
    <div class="mr"><span class="meq" style="color:#a78bfa" id="feqL">f(x,y)</span><span class="mv" style="color:#a78bfa" id="fvL">0</span></div>
    <div class="sep">
     <div class="mr"><span class="meq" style="color:#FFD166">∂f/∂x</span><span class="mv" style="color:#FFD166" id="dxL">0</span></div>
    </div>
    <div class="mr"><span class="meq" style="color:#4ECDC4">∂f/∂y</span><span class="mv" style="color:#4ECDC4" id="dyL">0</span></div>
    <div class="sep">
     <div class="mr"><span class="meq" style="color:#fb923c">∇f</span><span class="mv" style="color:#fb923c" id="gL">[0,0]</span></div>
    </div>
    <div class="mr"><span class="meq" style="color:#f472b6">|∇f|</span><span class="mv" style="color:#f472b6" id="gmL">0</span></div>
   </div>
  </div>
  <div class="col-r">
   <div class="lbl">Topographic Gradient Map</div>
   <canvas id="cvs" width="680" height="600"></canvas>
  </div>
 </div>
</div>

<script>
const F={
 bowl:{f:(x,y)=>x*x+y*y,dx:(x,y)=>2*x,dy:(x,y)=>2*y,name:"x²+y²"},
 saddle:{f:(x,y)=>x*x-y*y,dx:(x,y)=>2*x,dy:(x,y)=>-2*y,name:"x²−y²"},
 wave:{f:(x,y)=>2*Math.sin(x)*Math.cos(y),dx:(x,y)=>2*Math.cos(x)*Math.cos(y),dy:(x,y)=>-2*Math.sin(x)*Math.sin(y),name:"2sin(x)cos(y)"}
};
let cur='bowl',mode='field';
let trail=[];
let climbing=false,climbDir=1,climbX=0,climbY=0,climbAnim=null;
const cvs=document.getElementById('cvs'),ctx=cvs.getContext('2d');
const xsl=document.getElementById('xsl'),ysl=document.getElementById('ysl');
const xvl=document.getElementById('xvl'),yvl=document.getElementById('yvl');
const R=3.2,PAD=40;

function stopClimb() {
 climbing=false;
 if(climbAnim!==null){cancelAnimationFrame(climbAnim);climbAnim=null;}
}

function w2s(x,y){
 return{sx:PAD+(x+R)/(2*R)*(cvs.width-2*PAD),sy:PAD+(R-y)/(2*R)*(cvs.height-2*PAD)};
}
function s2w(sx,sy){
 return{x:(sx-PAD)/(cvs.width-2*PAD)*(2*R)-R,y:R-(sy-PAD)/(cvs.height-2*PAD)*(2*R)};
}

function heatColor(v,mn,mx){
 let t=(v-mn)/(mx-mn+.001);t=Math.max(0,Math.min(1,t));
 // deep blue -> cyan -> green -> yellow -> red
 let r,g,b;
 if(t<.25){const s=t/.25;r=0;g=Math.round(s*200);b=Math.round(120+s*80);}
 else if(t<.5){const s=(t-.25)/.25;r=0;g=Math.round(200+s*55);b=Math.round(200-s*200);}
 else if(t<.75){const s=(t-.5)/.25;r=Math.round(s*255);g=255;b=0;}
 else{const s=(t-.75)/.25;r=255;g=Math.round(255-s*200);b=0;}
 return`rgb(${r},${g},${b})`;
}

function draw(){
 const fn=F[cur];
 const W=cvs.width,H=cvs.height;
 ctx.clearRect(0,0,W,H);
 ctx.fillStyle='#1e293b';ctx.fillRect(0,0,W,H);

 // Heatmap
 const res=3;
 let mn=Infinity,mx=-Infinity;
 for(let px=PAD;px<W-PAD;px+=res)for(let py=PAD;py<H-PAD;py+=res){
  const{x,y}=s2w(px,py);const v=fn.f(x,y);if(v<mn)mn=v;if(v>mx)mx=v;
 }
 for(let px=PAD;px<W-PAD;px+=res)for(let py=PAD;py<H-PAD;py+=res){
  const{x,y}=s2w(px,py);
  ctx.fillStyle=heatColor(fn.f(x,y),mn,mx);
  ctx.globalAlpha=.7;ctx.fillRect(px,py,res,res);ctx.globalAlpha=1;
 }

 // Contour lines
 const levels=12;
 for(let l=0;l<levels;l++){
  const target=mn+(mx-mn)*(l+1)/(levels+1);
  ctx.strokeStyle='rgba(255,255,255,.15)';ctx.lineWidth=.8;
  // marching squares simplified: scan rows
  for(let py=PAD;py<H-PAD;py+=8){
   for(let px=PAD;px<W-PAD;px+=8){
    const{x,y}=s2w(px,py);const{x:x2,y:y2}=s2w(px+8,py);
    const v1=fn.f(x,y),v2=fn.f(x2,y2);
    if((v1-target)*(v2-target)<0){
     ctx.fillStyle='rgba(255,255,255,.12)';ctx.fillRect(px,py,2,2);
    }
   }
  }
 }

 // Gradient arrows
 if(mode==='field'){
  const step=.5;
  for(let gx=-R+.25;gx<=R-.25;gx+=step){
   for(let gy=-R+.25;gy<=R-.25;gy+=step){
    const ddx=fn.dx(gx,gy),ddy=fn.dy(gx,gy);
    const mag=Math.sqrt(ddx*ddx+ddy*ddy);
    if(mag<.01)continue;
    const sc=Math.min(mag*.06,.035);
    const ax=ddx/mag*sc*(2*R),ay=ddy/mag*sc*(2*R);
    const{sx:sx1,sy:sy1}=w2s(gx,gy);
    const{sx:sx2,sy:sy2}=w2s(gx+ax,gy+ay);
    const alpha=Math.min(1,.3+mag*.15);
    // arrow color by magnitude
    const t=Math.min(1,mag/6);
    const cr=Math.round(251*t+100*(1-t)),cg=Math.round(146*t+200*(1-t)),cb=Math.round(60*t+255*(1-t));
    ctx.strokeStyle=`rgba(${cr},${cg},${cb},${alpha})`;
    ctx.lineWidth=1.5;
    ctx.beginPath();ctx.moveTo(sx1,sy1);ctx.lineTo(sx2,sy2);ctx.stroke();
    // arrowhead
    const ang=Math.atan2(sy2-sy1,sx2-sx1);const hl=6;
    ctx.beginPath();
    ctx.moveTo(sx2,sy2);
    ctx.lineTo(sx2-hl*Math.cos(ang-.4),sy2-hl*Math.sin(ang-.4));
    ctx.lineTo(sx2-hl*Math.cos(ang+.4),sy2-hl*Math.sin(ang+.4));
    ctx.closePath();ctx.fillStyle=`rgba(${cr},${cg},${cb},${alpha})`;ctx.fill();
   }
  }
 }

 // Climb trail
 if(trail.length>1){
  ctx.beginPath();
  for(let i=0;i<trail.length;i++){
   const{sx,sy}=w2s(trail[i][0],trail[i][1]);
   i===0?ctx.moveTo(sx,sy):ctx.lineTo(sx,sy);
  }
  ctx.strokeStyle='#34d399';ctx.lineWidth=3;
  ctx.shadowColor='#34d399';ctx.shadowBlur=10;
  ctx.stroke();ctx.shadowBlur=0;
  // dots
  for(let i=0;i<trail.length;i+=Math.max(1,Math.floor(trail.length/30))){
   const{sx,sy}=w2s(trail[i][0],trail[i][1]);
   ctx.beginPath();ctx.arc(sx,sy,2.5,0,Math.PI*2);ctx.fillStyle='#34d399';ctx.fill();
  }
  // end marker
  const last=trail[trail.length-1];
  const{sx:lx,sy:ly}=w2s(last[0],last[1]);
  ctx.beginPath();ctx.arc(lx,ly,6,0,Math.PI*2);
  ctx.fillStyle=climbDir>0?'#f472b6':'#34d399';
  ctx.shadowColor=climbDir>0?'#f472b6':'#34d399';ctx.shadowBlur=12;
  ctx.fill();ctx.shadowBlur=0;
  ctx.fillStyle='#fff';ctx.font='bold 10px Inter';ctx.textAlign='center';
  ctx.fillText(climbDir>0?'▲':'▼',lx,ly+3.5);
 }

 // Selected point + gradient vector
 const tx=parseFloat(xsl.value),ty=parseFloat(ysl.value);
 const{sx:px,sy:py}=w2s(tx,ty);
 const ddx=fn.dx(tx,ty),ddy=fn.dy(tx,ty);
 const gmag=Math.sqrt(ddx*ddx+ddy*ddy);

 // Partial derivative component arrows
 // ∂f/∂x arrow (yellow)
 const xScale=.12;
 const{sx:xx2,sy:xy2}=w2s(tx+ddx*xScale,ty);
 ctx.strokeStyle='#FFD166';ctx.lineWidth=2.5;ctx.setLineDash([4,3]);
 ctx.beginPath();ctx.moveTo(px,py);ctx.lineTo(xx2,xy2);ctx.stroke();ctx.setLineDash([]);
 // ∂f/∂y arrow (teal)
 const{sx:yx2,sy:yy2}=w2s(tx,ty+ddy*xScale);
 ctx.strokeStyle='#4ECDC4';ctx.lineWidth=2.5;ctx.setLineDash([4,3]);
 ctx.beginPath();ctx.moveTo(px,py);ctx.lineTo(yx2,yy2);ctx.stroke();ctx.setLineDash([]);

 // Gradient arrow (orange, solid)
 const{sx:gx2,sy:gy2}=w2s(tx+ddx*xScale,ty+ddy*xScale);
 ctx.strokeStyle='#fb923c';ctx.lineWidth=3;
 ctx.shadowColor='#fb923c';ctx.shadowBlur=8;
 ctx.beginPath();ctx.moveTo(px,py);ctx.lineTo(gx2,gy2);ctx.stroke();ctx.shadowBlur=0;
 // arrowhead
 const ga=Math.atan2(gy2-py,gx2-px);
 ctx.beginPath();ctx.moveTo(gx2,gy2);
 ctx.lineTo(gx2-10*Math.cos(ga-.35),gy2-10*Math.sin(ga-.35));
 ctx.lineTo(gx2-10*Math.cos(ga+.35),gy2-10*Math.sin(ga+.35));
 ctx.closePath();ctx.fillStyle='#fb923c';ctx.fill();

 // Point dot
 ctx.beginPath();ctx.arc(px,py,7,0,Math.PI*2);
 ctx.fillStyle='#fff';ctx.shadowColor='#fff';ctx.shadowBlur=14;
 ctx.fill();ctx.shadowBlur=0;

 // Labels on gradient arrow
 ctx.fillStyle='#fb923c';ctx.font='bold 11px Inter';ctx.textAlign='left';
 ctx.fillText('∇f',gx2+6,gy2-4);
 ctx.fillStyle='#FFD166';ctx.fillText('∂f/∂x',xx2+(xx2>px?4:-30),xy2-6);
 ctx.fillStyle='#4ECDC4';ctx.fillText('∂f/∂y',yx2+4,yy2+(yy2>py?14:-6));

 // Axis labels
 ctx.fillStyle='rgba(255,255,255,.4)';ctx.font='bold 11px Inter';
 ctx.textAlign='center';ctx.fillText('x →',W/2,H-8);
 ctx.save();ctx.translate(12,H/2);ctx.rotate(-Math.PI/2);ctx.fillText('y →',0,0);ctx.restore();

 // Legend
 ctx.fillStyle='rgba(0,0,0,.5)';
 ctx.fillRect(W-155,8,147,climbDir?72:58);
 ctx.strokeStyle='rgba(255,255,255,.1)';ctx.strokeRect(W-155,8,147,climbDir?72:58);
 ctx.font='bold 10px Inter';ctx.textAlign='left';
 ctx.fillStyle='#FFD166';ctx.fillText('--- ∂f/∂x component',W-145,24);
 ctx.fillStyle='#4ECDC4';ctx.fillText('--- ∂f/∂y component',W-145,38);
 ctx.fillStyle='#fb923c';ctx.fillText('━━ ∇f (gradient)',W-145,52);
 if(trail.length>0){ctx.fillStyle='#34d399';ctx.fillText('━━ climb trail',W-145,66);}

 // Update readouts
 xvl.innerText=tx.toFixed(2);yvl.innerText=ty.toFixed(2);
 document.getElementById('fvL').innerText=fn.f(tx,ty).toFixed(2);
 document.getElementById('dxL').innerText=ddx.toFixed(2);
 document.getElementById('dyL').innerText=ddy.toFixed(2);
 document.getElementById('gL').innerText='['+ddx.toFixed(2)+', '+ddy.toFixed(2)+']';
 document.getElementById('gmL').innerText=gmag.toFixed(3);
 document.getElementById('feqL').innerText='f = '+fn.name;
}

// Events
document.querySelectorAll('.fbtn').forEach(b=>b.addEventListener('click',e=>{
 document.querySelectorAll('.fbtn').forEach(x=>x.classList.remove('active'));
 e.currentTarget.classList.add('active');cur=e.currentTarget.dataset.f;
 trail=[];stopClimb();draw();
}));
document.querySelectorAll('.mbtn').forEach(b=>b.addEventListener('click',e=>{
 document.querySelectorAll('.mbtn').forEach(x=>x.classList.remove('active'));
 e.currentTarget.classList.add('active');mode=e.currentTarget.dataset.m;stopClimb();draw();
}));
xsl.addEventListener('input',()=>{trail=[];stopClimb();draw();});
ysl.addEventListener('input',()=>{trail=[];stopClimb();draw();});

// Click on canvas to set point
cvs.addEventListener('click',e=>{
 stopClimb();
 const rect=cvs.getBoundingClientRect();
 const scaleX=cvs.width/rect.width,scaleY=cvs.height/rect.height;
 const cx=(e.clientX-rect.left)*scaleX,cy=(e.clientY-rect.top)*scaleY;
 const{x,y}=s2w(cx,cy);
 if(x>=-R&&x<=R&&y>=-R&&y<=R){
  xsl.value=x.toFixed(2);ysl.value=y.toFixed(2);
  trail=[];draw();
 }
});

// Climber
document.getElementById('climbBtn').addEventListener('click',()=>{
 if(climbing){stopClimb();draw();return;}
 const fn=F[cur];
 climbX=parseFloat(xsl.value);climbY=parseFloat(ysl.value);
 trail=[[climbX,climbY]];climbing=true;
 // Determine direction: climb UP (positive gradient) or DOWN (negative gradient)
 // Toggle each click
 climbDir=climbDir>0?-1:1;
 let steps=0;
 function step(){
  if(!climbing)return;
  if(steps>=500){stopClimb();draw();return;}
  const ddx=fn.dx(climbX,climbY),ddy=fn.dy(climbX,climbY);
  const mag=Math.sqrt(ddx*ddx+ddy*ddy);
  if(mag<.005){climbing=false;draw();return;}
  const lr=.02;
  climbX+=climbDir*lr*ddx;climbY+=climbDir*lr*ddy;
  if(Math.abs(climbX)>R||Math.abs(climbY)>R){climbing=false;draw();return;}
  trail.push([climbX,climbY]);steps++;
  xsl.value=climbX.toFixed(2);ysl.value=climbY.toFixed(2);
  draw();
  climbAnim=requestAnimationFrame(step);
 }
 step();
});

window.addEventListener('pagehide',stopClimb);
draw();
</script>
</body>
</html>
"""
    components.html(html, height=750, scrolling=False)

def main():
    st.title("🧭 Page 48: The Gradient — Steepest Climb")

    st.markdown("""
    On Page 47 you learned to slice a surface in **one direction at a time** — each slice giving a partial derivative.
    Now: **what if you combine ALL the partial derivatives into a single arrow?**

    That arrow is the **Gradient** — written **∇f** — and it always points in the direction of **steepest ascent**.
    Its magnitude tells you **how steep** that steepest climb is.

    $$\\nabla f(x,y) = \\left[\\frac{\\partial f}{\\partial x},\\ \\frac{\\partial f}{\\partial y}\\right]$$
    """)

    st.divider()
    st.markdown("### 🗺️ The Gradient Compass Lab")
    st.markdown(
        "Move the **X/Y sliders** (or **click the map**) to place your point. "
        "The **dashed arrows** show each partial derivative component; the **solid orange arrow** is the gradient — their vector sum. "
        "Switch to **🧗 Climber** mode and hit the green button to watch an agent follow the gradient uphill or downhill!"
    )

    render_lab()

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔑 Key Intuitions")
        st.markdown(r"""
- **∇f is a vector**, not a number — it has both direction and magnitude
- **Direction** = steepest uphill at that point
- **Magnitude** |∇f| = how steep the steepest slope is
- At a **minimum or maximum**, ∇f = **0** (flat — nowhere to go)
- **−∇f** points **downhill** — this is gradient descent!
        """)

    with col2:
        st.markdown("### 🧮 How It's Built")
        st.info("The gradient is just the vector of ALL partial derivatives stacked together.")
        st.markdown(r"""
**Example:** $f(x,y) = x^2 + y^2$

$$\frac{\partial f}{\partial x} = 2x, \quad \frac{\partial f}{\partial y} = 2y$$

$$\boxed{\nabla f = [2x,\ 2y]}$$

At point $(1, 2)$: $\nabla f = [2, 4]$, magnitude $= \sqrt{4+16} = \sqrt{20} \approx 4.47$
        """)

    st.divider()
    st.markdown("### 🤖 Bridge to AI: The Gradient IS the Engine")
    st.markdown(r"""
    In a neural network, the loss function $L$ depends on **millions of weights** $w_1, w_2, \dots, w_n$.

    The gradient of the loss tells the network **which direction to adjust every single weight** to reduce error the fastest:

    $$\nabla_{\mathbf{w}} L = \left[\frac{\partial L}{\partial w_1},\ \frac{\partial L}{\partial w_2},\ \dots,\ \frac{\partial L}{\partial w_n}\right]$$

    **Gradient Descent** (Page 52) simply says: *"Walk in the direction of $-\nabla L$"* — downhill on the loss landscape.

    Everything you just saw on the map — arrows pointing uphill, the climber following them — is **exactly** what happens during AI training, just in millions of dimensions!
    """)

    st.divider()
    st.markdown(
        '<div style="color:#94a3b8;font-size:.95rem;">Page 48 — The gradient assembles all partial derivatives into a single compass. Next: the area under a curve — Integrals!</div>',
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
