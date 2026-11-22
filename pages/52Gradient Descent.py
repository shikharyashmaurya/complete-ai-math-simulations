import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Gradient Descent — Walking Downhill", layout="wide")

def render_gd_lab():
    html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:sans-serif;background:#0f172a;color:#fff;padding:16px;overflow-x:hidden;}
.wrap{max-width:1200px;margin:0 auto;display:flex;flex-direction:column;gap:16px;}
.row{display:flex;gap:16px;}
.card{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:14px;}
.col-l{flex:1;display:flex;flex-direction:column;gap:12px;min-width:320px;}
.col-r{flex:2;display:flex;flex-direction:column;gap:12px;}
h2{font-size:22px;font-weight:900;margin-bottom:2px;background:linear-gradient(90deg, #38bdf8, #10b981);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.sub{font-size:12px;color:#94a3b8;line-height:1.5;margin-bottom:8px;}
.lbl{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#94a3b8;margin-bottom:6px;}
.func-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;}
.fbtn{background:rgba(255,255,255,0.05);color:#cbd5e1;border:1px solid rgba(255,255,255,.1);padding:8px;border-radius:8px;font-weight:700;cursor:pointer;font-size:11px;text-align:center;transition:.2s;}
.fbtn:hover{background:rgba(255,255,255,.1);}
.fbtn.active{background:rgba(56,189,248,.2);border-color:#38bdf8;color:#38bdf8;box-shadow:0 0 10px rgba(56,189,248,.2);}
canvas{border-radius:12px;border:1px solid rgba(255,255,255,.08);display:block;width:100%;background:#1e293b;}
.mbox{background:rgba(0,0,0,.3);border-radius:10px;padding:12px;border:1px solid rgba(255,255,255,.06);display:flex;flex-direction:column;gap:8px;}
.mr{display:flex;justify-content:space-between;align-items:center;}
.meq{font-family:monospace;font-size:13px;font-weight:bold;}
.mv{font-family:monospace;font-size:15px;font-weight:900;background:rgba(0,0,0,.5);padding:2px 8px;border-radius:5px;font-variant-numeric:tabular-nums;}
.sep{border-top:1px dashed rgba(255,255,255,.12);padding-top:8px;}
input[type=range]{width:100%;height:5px;background:rgba(255,255,255,.1);border-radius:3px;outline:none;-webkit-appearance:none;margin-bottom:10px;}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;background:#38bdf8;box-shadow:0 0 8px #38bdf8;cursor:pointer;}
.sl{display:flex;justify-content:space-between;font-size:12px;font-weight:700;margin-bottom:6px;}
.sv{font-size:14px;font-weight:900;font-variant-numeric:tabular-nums;}
.action-btn{background:#10b981;color:#0f172a;border:none;padding:10px;border-radius:8px;font-weight:800;cursor:pointer;width:100%;font-size:12px;letter-spacing:1px;transition:.2s;margin-top:4px;text-transform:uppercase;}
.action-btn:hover{background:#059669;transform:translateY(-1px);}
.action-btn.secondary{background:rgba(255,255,255,0.05);color:#fff;border:1px solid rgba(255,255,255,0.1);margin-top:8px;}
.hint{font-size:10px;color:#64748b;text-align:center;margin-top:8px;text-transform:uppercase;letter-spacing:0.5px;}
.toast{position:absolute;top:20px;right:20px;background:rgba(16,185,129,0.9);color:#fff;padding:8px 16px;border-radius:8px;font-size:12px;font-weight:bold;opacity:0;transition:opacity 0.3s;pointer-events:none;z-index:100;}
</style>
</head>
<body>
<div class="toast" id="toast">TARGET REACHED! 🎯</div>
<div class="wrap">
 <div class="row">
  <div class="col-l">
   <div class="card">
    <h2>Downhill Walker 🏔️</h2>
    <p class="sub">AI doesn't "know" the bottom. It feels the slope and takes a step downhill. This is Gradient Descent.</p>
   </div>
   
   <div class="card">
    <div class="lbl">Terrain Topology</div>
    <div class="func-grid" id="fbtns">
     <button class="fbtn active" data-f="bowl">Convex Bowl</button>
     <button class="fbtn" data-f="complex">Lumpy Terrain</button>
    </div>
   </div>

   <div class="card">
    <div class="lbl">Training Configuration</div>
    <div style="font-size: 13px; color: #38bdf8; font-weight: 700; margin-bottom: 10px;">
        Learning Rate: <span style="background: rgba(56, 189, 248, 0.1); padding: 2px 6px; border-radius: 4px;">0.15 (Fixed)</span>
    </div>
    <p class="sub" style="font-size: 10px; margin-top: -5px;">We'll explore how changing this affects learning on Page 53.</p>
    
    <button class="action-btn" id="runBtn">▶ START TRAINING</button>
    <button class="action-btn secondary" id="resetBtn">🔄 RESET POSITION</button>
    <div class="hint">Click on the Topo Map to teleport</div>
   </div>

   <div class="mbox">
    <div class="mr"><span class="meq" style="color:#a78bfa">Loss f(w1, w2)</span><span class="mv" style="color:#a78bfa" id="lossVal">0.00</span></div>
    <div class="sep">
     <div class="mr"><span class="meq" style="color:#fb923c">Gradient ∇f (Uphill)</span><span class="mv" style="color:#fb923c" id="gVal">[0,0]</span></div>
    <div class="mr"><span class="meq" style="color:#10b981">Descent −∇f (Downhill)</span><span class="mv" style="color:#10b981" id="dgVal">[0,0]</span></div>
    <div class="sep">
     <div class="mr"><span class="meq" style="color:#38bdf8">Steps Taken</span><span class="mv" style="color:#38bdf8" id="stepVal">0</span></div>
    </div>
   </div>
  </div>

  <div class="col-r">
   <div style="display:flex; gap:12px;">
    <div style="flex:1;">
     <div class="lbl">1. Topographic Map (Birds-eye)</div>
     <canvas id="cvs2d" width="400" height="400"></canvas>
    </div>
    <div style="flex:1.2;">
     <div class="lbl">2. 3D Perspective View</div>
     <canvas id="cvs3d" width="480" height="400"></canvas>
    </div>
   </div>
   <div class="card" style="padding:10px; font-size:11px; color:#94a3b8; display:flex; justify-content:space-around;">
    <span><b style="color:#fb923c">--</b> Gradient (Uphill)</span>
    <span><b style="color:#10b981">→</b> Descent Step (Downhill)</span>
    <span><b style="color:#10b981">●</b> Path</span>
   </div>
  </div>
 </div>
</div>

<script>
const funcs = {
  bowl: {
    f: (x, y) => 0.3*(x*x + y*y) - 1.5,
    dx: (x, y) => 0.6*x,
    dy: (x, y) => 0.6*y
  },
  complex: {
    f: (x, y) => 0.2*(x*x + y*y) + 0.5*Math.sin(x*3)*Math.cos(y*3) + 0.3*Math.cos(x*1.5) - 1.0,
    dx: (x, y) => 0.4*x + 1.5*Math.cos(x*3)*Math.cos(y*3) - 0.45*Math.sin(x*1.5),
    dy: (x, y) => 0.4*y - 1.5*Math.sin(x*3)*Math.sin(y*3)
  }
};

const LR = 0.15; // Fixed for this page
let curF = 'bowl';
let ball = { x: 2.5, y: 2.0 };
let path = [];
let steps = 0;
let running = false;
let rotX = 0.6, rotZ = 0.7;

const c2 = document.getElementById('cvs2d'), ctx2 = c2.getContext('2d');
const c3 = document.getElementById('cvs3d'), ctx3 = c3.getContext('2d');
const runBtn = document.getElementById('runBtn');
const toast = document.getElementById('toast');
const gValEl = document.getElementById('gVal');
const dgValEl = document.getElementById('dgVal');

const R = 3.5, PAD = 30;

// Coordinate mapping
function w2s(x, y) {
  return {
    sx: PAD + (x + R) / (2 * R) * (c2.width - 2 * PAD),
    sy: PAD + (R - y) / (2 * R) * (c2.height - 2 * PAD)
  };
}
function s2w(sx, sy) {
  return {
    x: (sx - PAD) / (c2.width - 2 * PAD) * (2 * R) - R,
    y: R - (sy - PAD) / (c2.height - 2 * PAD) * (2 * R)
  };
}

// 3D Projection
function project(x, z, y) {
  let x1 = x * Math.cos(rotZ) - z * Math.sin(rotZ);
  let z1 = x * Math.sin(rotZ) + z * Math.cos(rotZ);
  let y1 = y * Math.cos(rotX) - z1 * Math.sin(rotX);
  let z2 = y * Math.sin(rotX) + z1 * Math.cos(rotX);
  return {
    x: c3.width/2 + x1 * 65,
    y: c3.height/2 - y1 * 65,
    depth: z2
  };
}

function heatColor(v) {
  const t = Math.max(0, Math.min(1, (v + 2) / 4.5));
  if (t < 0.3) return `hsl(217, 91%, ${20 + t * 100}%)`;
  else if (t < 0.7) return `hsl(${217 - (t-0.3)*400}, 91%, 60%)`;
  else return `hsl(${45 - (t-0.7)*150}, 91%, 50%)`;
}

function draw() {
  const fn = funcs[curF];
  
  // -- 2D DRAW --
  ctx2.clearRect(0,0,c2.width,c2.height);
  ctx2.fillStyle='#1e293b'; ctx2.fillRect(0,0,c2.width,c2.height);
  
  // Heatmap background
  const res = 5;
  for(let i=PAD; i<c2.width-PAD; i+=res) {
    for(let j=PAD; j<c2.height-PAD; j+=res) {
      const {x, y} = s2w(i, j);
      ctx2.fillStyle = heatColor(fn.f(x, y));
      ctx2.fillRect(i, j, res, res);
    }
  }
  
  // Contours (simplified)
  ctx2.strokeStyle = 'rgba(255,255,255,0.1)'; ctx2.lineWidth = 1;
  for(let l=-2; l<=2; l+=0.5) {
    for(let i=PAD; i<c2.width-PAD; i+=8) {
      for(let j=PAD; j<c2.height-PAD; j+=8) {
        const {x, y} = s2w(i, j);
        if(Math.abs(fn.f(x,y) - l) < 0.05) ctx2.strokeRect(i, j, 1, 1);
      }
    }
  }

  // Path on 2D
  if(path.length > 1) {
    ctx2.beginPath();
    const s0 = w2s(path[0].x, path[0].y);
    ctx2.moveTo(s0.sx, s0.sy);
    for(let i=1; i<path.length; i++) {
      const s = w2s(path[i].x, path[i].y);
      ctx2.lineTo(s.sx, s.sy);
    }
    ctx2.strokeStyle = '#10b981'; ctx2.lineWidth = 2; ctx2.stroke();
  }

  // Ball & Vectors on 2D
  const curS = w2s(ball.x, ball.y);
  const dx = fn.dx(ball.x, ball.y), dy = fn.dy(ball.x, ball.y);
  const vScale = 0.5;
  
  // gradient (uphill)
  const sg2 = w2s(ball.x + dx*vScale, ball.y + dy*vScale);
  ctx2.beginPath(); ctx2.moveTo(curS.sx, curS.sy); ctx2.lineTo(sg2.sx, sg2.sy);
  ctx2.strokeStyle='#fb923c'; ctx2.lineWidth=1; ctx2.setLineDash([2,2]); ctx2.stroke(); ctx2.setLineDash([]);
  
  // descent step (downhill - negative gradient)
  const sd2 = w2s(ball.x - dx*vScale, ball.y - dy*vScale);
  ctx2.beginPath(); ctx2.moveTo(curS.sx, curS.sy); ctx2.lineTo(sd2.sx, sd2.sy);
  ctx2.strokeStyle='#10b981'; ctx2.lineWidth=3; ctx2.stroke();
  
  // arrowhead for descent
  const da = Math.atan2(sd2.sy - curS.sy, sd2.sx - curS.sx);
  ctx2.beginPath(); ctx2.moveTo(sd2.sx, sd2.sy);
  ctx2.lineTo(sd2.sx - 10*Math.cos(da-0.4), sd2.sy - 10*Math.sin(da-0.4));
  ctx2.lineTo(sd2.sx - 10*Math.cos(da+0.4), sd2.sy - 10*Math.sin(da+0.4));
  ctx2.closePath(); ctx2.fillStyle='#10b981'; ctx2.fill();

  ctx2.beginPath(); ctx2.arc(curS.sx, curS.sy, 6, 0, Math.PI*2);
  ctx2.fillStyle='#fff'; ctx2.shadowBlur=10; ctx2.shadowColor='#fff'; ctx2.fill(); ctx2.shadowBlur=0;

  // -- 3D DRAW --
  ctx3.clearRect(0,0,c3.width,c3.height);
  ctx3.fillStyle='#1e293b'; ctx3.fillRect(0,0,c3.width,c3.height);
  
  const N = 25;
  const step = (2*R)/N;
  const polys = [];
  for(let i=0; i<N; i++) {
    for(let j=0; j<N; j++) {
      const x0 = -R + i*step, x1 = x0 + step;
      const z0 = -R + j*step, z1 = z0 + step;
      const y00 = fn.f(x0, z0), y10 = fn.f(x1, z0), y01 = fn.f(x0, z1), y11 = fn.f(x1, z1);
      const p00 = project(x0, z0, y00), p10 = project(x1, z0, y10), p01 = project(x0, z1, y01), p11 = project(x1, z1, y11);
      polys.push({
        pts: [p00, p10, p11, p01],
        depth: (p00.depth+p10.depth+p01.depth+p11.depth)/4,
        color: heatColor((y00+y10+y01+y11)/4)
      });
    }
  }
  polys.sort((a,b)=>b.depth-a.depth);
  polys.forEach(p=>{
    ctx3.beginPath(); ctx3.moveTo(p.pts[0].x, p.pts[0].y);
    for(let i=1; i<4; i++) ctx3.lineTo(p.pts[i].x, p.pts[i].y);
    ctx3.closePath(); ctx3.fillStyle=p.color; ctx3.fill();
    ctx3.strokeStyle='rgba(0,0,0,0.1)'; ctx3.stroke();
  });

  // Path in 3D
  if(path.length > 1) {
    ctx3.beginPath();
    const p0 = project(path[0].x, path[0].y, path[0].z);
    ctx3.moveTo(p0.x, p0.y);
    for(let i=1; i<path.length; i++) {
      const p = project(path[i].x, path[i].y, path[i].z);
      ctx3.lineTo(p.x, p.y);
    }
    ctx3.strokeStyle='rgba(255,255,255,0.4)'; ctx3.lineWidth=1.5; ctx3.stroke();
  }

  // Ball in 3D
  const pb = project(ball.x, ball.y, fn.f(ball.x, ball.y));
  ctx3.beginPath(); ctx3.arc(pb.x, pb.y - 8, 7, 0, Math.PI*2);
  const grad = ctx3.createRadialGradient(pb.x-2, pb.y-10, 1, pb.x, pb.y-8, 7);
  grad.addColorStop(0, '#fff'); grad.addColorStop(1, '#38bdf8');
  ctx3.fillStyle=grad; ctx3.shadowBlur=15; ctx3.shadowColor='#38bdf8'; ctx3.fill(); ctx3.shadowBlur=0;
  
  // UI Updates
  document.getElementById('lossVal').innerText = (fn.f(ball.x, ball.y) + 1.5).toFixed(3);
  gValEl.innerText = `[${dx.toFixed(2)}, ${dy.toFixed(2)}]`;
  dgValEl.innerText = `[${(-dx).toFixed(2)}, ${(-dy).toFixed(2)}]`;
  document.getElementById('stepVal').innerText = steps;
}

function step() {
  if(!running) return;
  const fn = funcs[curF];
  const dx = fn.dx(ball.x, ball.y), dy = fn.dy(ball.x, ball.y);
  
  path.push({x: ball.x, y: ball.y, z: fn.f(ball.x, ball.y)});
  if(path.length > 100) path.shift();
  
  ball.x -= LR * dx;
  ball.y -= LR * dy;
  steps++;
  
  const mag = Math.sqrt(dx*dx + dy*dy);
  if(mag < 0.01) {
    running = false;
    runBtn.innerText = "▶ START TRAINING";
    toast.style.opacity = 1;
    setTimeout(()=>toast.style.opacity=0, 2000);
  }
  
  draw();
  if(running) requestAnimationFrame(step);
}

// Events
c2.addEventListener('mousedown', e => {
  const rect = c2.getBoundingClientRect();
  const scale = c2.width / rect.width;
  const {x, y} = s2w((e.clientX - rect.left)*scale, (e.clientY - rect.top)*scale);
  ball = {x, y}; path = []; steps = 0; running = false;
  runBtn.innerText = "▶ START TRAINING";
  draw();
});

runBtn.addEventListener('click', () => {
  running = !running;
  runBtn.innerText = running ? "⏸ PAUSE" : "▶ START TRAINING";
  if(running) step();
});

document.getElementById('resetBtn').addEventListener('click', () => {
  ball = { x: (Math.random()-0.5)*5, y: (Math.random()-0.5)*5 };
  path = []; steps = 0; running = false;
  runBtn.innerText = "▶ START TRAINING";
  draw();
});

document.querySelectorAll('.fbtn').forEach(b => {
  b.addEventListener('click', e => {
    document.querySelectorAll('.fbtn').forEach(x => x.classList.remove('active'));
    e.target.classList.add('active');
    curF = e.target.dataset.f;
    ball = {x: 2.5, y: 2.0}; path = []; steps = 0; running = false;
    runBtn.innerText = "▶ START TRAINING";
    draw();
  });
});

// 3D Rotation dragging
let isDragging = false, lastX, lastY;
c3.addEventListener('mousedown', e => { isDragging=true; lastX=e.clientX; lastY=e.clientY; });
window.addEventListener('mousemove', e => {
  if(!isDragging) return;
  rotZ += (e.clientX - lastX) * 0.01;
  rotX += (e.clientY - lastY) * 0.01;
  rotX = Math.max(0.1, Math.min(Math.PI/2-0.1, rotX));
  lastX = e.clientX; lastY = e.clientY;
  draw();
});
window.addEventListener('mouseup', () => isDragging=false);

draw();
</script>
</body>
</html>
"""
    components.html(html_code, height=900, scrolling=False)

def main():
    st.markdown("""
        <style>
            .main-header {
                font-family: sans-serif;
                background: linear-gradient(90deg, #38bdf8, #10b981);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 3.2rem;
                font-weight: 900;
                margin-bottom: 0;
            }
            .sub-header {
                font-family: sans-serif;
                font-size: 1.2rem;
                color: #94a3b8;
                margin-bottom: 1.5rem;
            }
            .highlight-yellow { color: #FFD166; font-weight: 700; }
            .highlight-teal { color: #4ECDC4; font-weight: 700; }
            .highlight-orange { color: #fb923c; font-weight: 700; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-header">Gradient Descent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Optimization: The Engine of Machine Learning</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5])

    with col1:
        with st.container(border=True):
            st.markdown("### 🧭 The Negative Compass")
            st.markdown(
                r"On Page 48, you saw the Gradient ($\nabla f$) — it points directly **uphill**."
            )
            st.markdown(
                r"**Gradient Descent** is simply the :green[**Negative**] of the gradient ($-\nabla f$). "
                r"By walking the opposite direction, we are guaranteed to go downhill toward the minimum."
            )

        with st.container(border=True):
            st.markdown("### 📐 The Descent Step")
            st.markdown("Every training iteration, we update the weights:")
            st.latex(r"\mathbf{w}_{next} = \mathbf{w}_{old} - \eta \cdot \nabla f")
            st.markdown(r"Where $\eta$ is the **Learning Rate** — your stride length.")
        
        st.info("💡 **Interactive:** Click anywhere on the **Topographic Map** to teleport the ball to a new starting position. Notice how it always seeks the deepest blue!")

    with col2:
        render_gd_lab()

    st.divider()

    # Deep Dive
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("### 🏹 Vector Components")
        st.markdown(r"""
        The gradient isn't just one arrow; it's the sum of two partial derivatives.
        - <span class="highlight-yellow">Yellow Dash</span>: Slope in $w_1$
        - <span class="highlight-teal">Teal Dash</span>: Slope in $w_2$
        - <span class="highlight-orange">Orange Arrow</span>: Combined steepest direction.
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("### 👟 Fixed Learning Rate η")
        st.markdown("""
        For now, we use a fixed learning rate of **0.15**.
        
        This determines how "big" our steps are. If it's too large, we might skip over the valley; if it's too small, we'll crawl forever.
        """)
        
    with c3:
        st.markdown("### 🕳️ Local Minima")
        st.markdown("""
        Switch to **Lumpy Terrain**. In complex AI models, the ball can get trapped in "fake" valleys. This is one of the hardest challenges in Deep Learning!
        """)

    st.divider()
    st.markdown("### 🤖 Bridge to AI: Training in Millions of Dimensions")
    st.markdown("""
    While we visualize **2 weights** here, a real Transformer model has **billions**. 
    The math remains identical:
    1. Calculate the **partial derivative** for every single weight.
    2. Combine them into one massive **gradient vector**.
    3. Take a tiny step **downhill**.
    
    This simple "walking downhill" process is exactly how ChatGPT, Midjourney, and self-driving cars learn.
    """)

    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #64748b; font-size: 0.8rem;">Page 52 — Gradient Descent. Next: <b>Learning Rate — Step Size Matters</b></div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
