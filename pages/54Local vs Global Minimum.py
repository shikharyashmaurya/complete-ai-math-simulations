import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Local vs Global Minimum", layout="wide")

def render_lab():
    html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Inter',sans-serif;background:#0f172a;color:white;padding:10px;overflow-x:hidden;}
.outer{display:flex;flex-direction:column;gap:15px;width:100%;margin:0 auto;}
.top{display:flex;flex-direction:row;gap:15px;flex-wrap:wrap;}
.controls{flex:1;min-width:300px;display:flex;flex-direction:column;gap:12px;}
.viz-col{flex:1.8;min-width:400px;display:flex;flex-direction:column;gap:12px;}
.card{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:14px;padding:16px;}
h2{font-size:22px;font-weight:900;color:#f8fafc;margin-bottom:4px;}
.sub{font-size:13px;color:#94a3b8;line-height:1.5;}
.clabel{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;color:#94a3b8;}
canvas{border-radius:12px;border:1px solid rgba(255,255,255,.08);display:block;background:#1e293b;width:100%;height:auto;}
.btn-group{display:flex;gap:8px;}
.btn{flex:1;background:rgba(255,255,255,0.05);color:#cbd5e1;border:1px solid rgba(255,255,255,0.1);padding:10px;border-radius:9px;font-weight:700;cursor:pointer;transition:.2s;font-size:12px;text-align:center;}
.btn:hover{background:rgba(255,255,255,0.1);}
.btn.active{background:rgba(167,139,250,.2);border-color:#a78bfa;color:#a78bfa;}
.btn.primary{background:#6366f1;color:white;border:none;}
.btn.primary:hover{background:#4f46e5;}
.status-box{background:rgba(0,0,0,.3);border-radius:12px;padding:14px;border:1px solid rgba(255,255,255,.06);display:flex;flex-direction:column;gap:10px;}
.status-row{display:flex;justify-content:space-between;align-items:center;}
.val{font-family:monospace;font-size:16px;font-weight:900;font-variant-numeric:tabular-nums;}
.badge{padding:4px 8px;border-radius:6px;font-size:10px;font-weight:800;text-transform:uppercase;}
.badge-local{background:rgba(239,68,68,0.2);color:#ef4444;border:1px solid rgba(239,68,68,0.4);}
.badge-global{background:rgba(34,197,94,0.2);color:#22c55e;border:1px solid rgba(34,197,94,0.4);}
.badge-stuck{background:rgba(234,179,8,0.2);color:#eab308;border:1px solid rgba(234,179,8,0.4);}
input[type=range]{width:100%;height:6px;background:rgba(255,255,255,0.1);border-radius:3px;outline:none;-webkit-appearance:none;margin-bottom:8px;}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;background:#a78bfa;cursor:pointer;box-shadow:0 0 8px #a78bfa;}
</style>
</head>
<body>
<div class="outer">
  <div class="top">
    <div class="controls">
      <div class="card">
        <h2>The Optimization Trap 🕳️</h2>
        <p class="sub">AI training is like rolling a ball down a mountain to find the lowest valley. But sometimes, you get stuck in a "local" dip before reaching the real "global" bottom.</p>
      </div>
      
      <div class="card">
        <div class="clabel">Landscape Selection</div>
        <div class="btn-group" id="l-btns">
          <button class="btn active" data-l="twins">The Twins</button>
          <button class="btn" data-l="bumps">Bumpy Road</button>
          <button class="btn" data-l="hidden">The Secret</button>
        </div>
      </div>

      <div class="card">
        <div class="clabel">Learning Rate (Step Size)</div>
        <input type="range" id="lr" min="0.01" max="0.5" step="0.01" value="0.1">
        <div class="status-row"><span class="sub">Current Step</span><span class="val" id="lrv">0.10</span></div>
      </div>

      <div class="btn-group">
        <button class="btn primary" id="run-btn">▶ RUN DESCENT</button>
        <button class="btn" id="reset-btn">🔄 RANDOM RESET</button>
      </div>

      <div class="status-box">
        <div class="status-row">
          <span class="clabel" style="margin:0">Current Altitude (Loss)</span>
          <span class="val" id="loss-v" style="color:#a78bfa">--</span>
        </div>
        <div class="status-row">
          <span class="clabel" style="margin:0">Outcome</span>
          <span id="outcome-badge" class="badge">Waiting...</span>
        </div>
      </div>
      
      <div class="card">
        <p class="sub" style="font-style:italic">Tip: Click on the <b>2D Map</b> below to drop the ball at a new starting point!</p>
      </div>
    </div>

    <div class="viz-col">
      <div style="display:flex;flex-direction:column;gap:8px;">
        <div class="clabel">3D Landscape View</div>
        <canvas id="cvs3d" width="680" height="400"></canvas>
      </div>
      <div style="display:flex;gap:12px;">
        <div style="flex:1;display:flex;flex-direction:column;gap:8px;">
          <div class="clabel">2D Topographic Map</div>
          <canvas id="cvs2d" width="330" height="260"></canvas>
        </div>
        <div style="flex:1;display:flex;flex-direction:column;gap:8px;">
          <div class="clabel">Loss History</div>
          <canvas id="cvs-loss" width="330" height="260"></canvas>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
const cvs3 = document.getElementById('cvs3d'), ctx3 = cvs3.getContext('2d');
const cvs2 = document.getElementById('cvs2d'), ctx2 = cvs2.getContext('2d');
const cvsl = document.getElementById('cvs-loss'), ctxl = cvsl.getContext('2d');

const lrSlider = document.getElementById('lr'), lrv = document.getElementById('lrv');
const runBtn = document.getElementById('run-btn'), resetBtn = document.getElementById('reset-btn');
const lossV = document.getElementById('loss-v'), outcomeBadge = document.getElementById('outcome-badge');

let curL = 'twins', ball = {x: 2.5, y: 2.5, path: []}, isRunning = false;

const landscapes = {
  twins: {
    f: (x,y) => {
      const g1 = -6 * Math.exp(-((x-1.8)**2 + (y-1.8)**2)/1.2);
      const g2 = -9 * Math.exp(-((x+2)**2 + (y+2)**2)/2.5);
      const bowl = 0.08 * (x*x + y*y);
      return g1 + g2 + bowl + 8;
    },
    df: (x,y) => {
      const e1 = Math.exp(-((x-1.8)**2 + (y-1.8)**2)/1.2);
      const e2 = Math.exp(-((x+2)**2 + (y+2)**2)/2.5);
      const dx = (12/1.2)*(x-1.8)*e1 + (18/2.5)*(x+2)*e2 + 0.16*x;
      const dy = (12/1.2)*(y-1.8)*e1 + (18/2.5)*(y+2)*e2 + 0.16*y;
      return {dx, dy};
    },
    global: {x: -2, y: -2, z: 0.8}
  },
  bumps: {
    f: (x,y) => {
      const g1 = -10 * Math.exp(-(x*x + y*y)/10);
      const bumps = -0.8 * (Math.cos(x*2.5) + Math.cos(y*2.5));
      const bowl = 0.05 * (x*x + y*y);
      return g1 + bumps + bowl + 11;
    },
    df: (x,y) => {
      const e1 = Math.exp(-(x*x + y*y)/10);
      const dx = (20/10)*x*e1 + 0.8*2.5*Math.sin(x*2.5) + 0.1*x;
      const dy = (20/10)*y*e1 + 0.8*2.5*Math.sin(y*2.5) + 0.1*y;
      return {dx, dy};
    },
    global: {x: 0, y: 0, z: 0.5}
  },
  hidden: {
    f: (x,y) => {
      const g1 = -7 * Math.exp(-((x-2.5)**2 + (y+2.5)**2)/1.0);
      const g2 = -12 * Math.exp(-((x+2.8)**2 + (y-2.8)**2)/0.8);
      const bowl = 0.04 * (x*x + y*y);
      return g1 + g2 + bowl + 12;
    },
    df: (x,y) => {
      const e1 = Math.exp(-((x-2.5)**2 + (y+2.5)**2)/1.0);
      const e2 = Math.exp(-((x+2.8)**2 + (y-2.8)**2)/0.8);
      const dx = 14*(x-2.5)*e1 + (24/0.8)*(x+2.8)*e2 + 0.08*x;
      const dy = 14*(y+2.5)*e1 + (24/0.8)*(y-2.8)*e2 + 0.08*y;
      return {dx, dy};
    },
    global: {x: -2.8, y: 2.8, z: 0.5}
  }
};

// Isometric projection helpers
const ISO = { ax: Math.cos(Math.PI/6), ay: Math.sin(Math.PI/6) };
const SCALE = 50, YSCALE = 18;
const OX = cvs3.width/2, OY = cvs3.height*0.55;

function iso(mx, mz, my) {
  const px = OX + (mx - mz) * ISO.ax * SCALE;
  const py = OY - (mx + mz) * ISO.ay * SCALE - my * YSCALE;
  return {px, py};
}

function draw3D() {
  ctx3.clearRect(0,0,cvs3.width,cvs3.height);
  const L = landscapes[curL];
  const N = 30, R = 4.5, step = 2*R/N;
  
  // Grid
  for(let i=N-1; i>=0; i--) {
    for(let j=N-1; j>=0; j--) {
      const x0 = -R+j*step, x1 = x0+step;
      const z0 = -R+i*step, z1 = z0+step;
      const y00 = L.f(x0,z0), y10 = L.f(x1,z0);
      const y01 = L.f(x0,z1), y11 = L.f(x1,z1);
      const p00 = iso(x0,z0,y00), p10 = iso(x1,z0,y10);
      const p01 = iso(x0,z1,y01), p11 = iso(x1,z1,y11);
      const avgY = (y00+y10+y01+y11)/4;

      const t = Math.max(0, Math.min(1, (avgY-2)/10));
      ctx3.beginPath();
      ctx3.moveTo(p00.px, p00.py); ctx3.lineTo(p10.px, p10.py);
      ctx3.lineTo(p11.px, p11.py); ctx3.lineTo(p01.px, p01.py);
      ctx3.closePath();
      
      const r = Math.round(50 + t*100), g = Math.round(50 + t*80), b = Math.round(150 + t*100);
      ctx3.fillStyle = `rgba(${r},${g},${b},0.8)`;
      ctx3.fill();
      ctx3.strokeStyle = 'rgba(0,0,0,0.1)';
      ctx3.lineWidth = 0.5;
      ctx3.stroke();
    }
  }

  // Path
  if(ball.path.length > 1) {
    ctx3.beginPath();
    for(let i=0; i<ball.path.length; i++){
      const p = iso(ball.path[i].x, ball.path[i].y, L.f(ball.path[i].x, ball.path[i].y));
      i===0?ctx3.moveTo(p.px, p.py):ctx3.lineTo(p.px, p.py);
    }
    ctx3.strokeStyle = '#fff'; ctx3.lineWidth = 2; ctx3.setLineDash([4,4]); ctx3.stroke(); ctx3.setLineDash([]);
  }

  // Ball
  const bZ = L.f(ball.x, ball.y);
  const bp = iso(ball.x, ball.y, bZ);
  ctx3.beginPath();
  ctx3.arc(bp.px, bp.py, 8, 0, Math.PI*2);
  ctx3.fillStyle = '#fff'; ctx3.shadowColor = '#fff'; ctx3.shadowBlur = 15;
  ctx3.fill(); ctx3.shadowBlur = 0;
}

function draw2D() {
  ctx2.clearRect(0,0,cvs2.width,cvs2.height);
  const L = landscapes[curL];
  const R = 4.5, W = cvs2.width, H = cvs2.height;
  
  const sc = (x,y) => ({sx: (x+R)/(2*R)*W, sy: (1-(y+R)/(2*R))*H});
  
  // Simple heatmap
  const step = 0.4;
  for(let x=-R; x<R; x+=step) {
    for(let y=-R; y<R; y+=step) {
      const z = L.f(x,y);
      const t = Math.max(0, Math.min(1, (z-2)/10));
      const r = Math.round(30+t*70), g = Math.round(30+t*60), b = Math.round(100+t*80);
      ctx2.fillStyle = `rgb(${r},${g},${b})`;
      ctx2.fillRect((x+R)/(2*R)*W, (1-(y+step+R)/(2*R))*H, step/(2*R)*W, step/(2*R)*H);
    }
  }

  // Path
  if(ball.path.length > 1) {
    ctx2.beginPath();
    for(let i=0; i<ball.path.length; i++){
      const p = sc(ball.path[i].x, ball.path[i].y);
      i===0?ctx2.moveTo(p.sx, p.sy):ctx2.lineTo(p.sx, p.sy);
    }
    ctx2.strokeStyle = 'rgba(255,255,255,0.6)'; ctx2.lineWidth = 1.5; ctx2.stroke();
  }

  // Ball
  const bp = sc(ball.x, ball.y);
  ctx2.beginPath(); ctx2.arc(bp.sx, bp.sy, 6, 0, Math.PI*2);
  ctx2.fillStyle = '#a78bfa'; ctx2.strokeStyle='#fff'; ctx2.lineWidth=2;
  ctx2.fill(); ctx2.stroke();
}

function drawLoss() {
  ctxl.clearRect(0,0,cvsl.width,cvsl.height);
  const W = cvsl.width, H = cvsl.height, pad=30;
  
  ctxl.strokeStyle='rgba(255,255,255,0.1)'; ctxl.lineWidth=1;
  ctxl.beginPath(); ctxl.moveTo(pad, H-pad); ctxl.lineTo(W-pad, H-pad); ctxl.stroke();
  ctxl.beginPath(); ctxl.moveTo(pad, pad); ctxl.lineTo(pad, H-pad); ctxl.stroke();
  
  if(ball.path.length < 2) return;
  
  const L = landscapes[curL];
  const losses = ball.path.map(p => L.f(p.x, p.y));
  const maxL = Math.max(...losses, 15), minL = 0;
  
  ctxl.beginPath();
  for(let i=0; i<losses.length; i++) {
    const sx = pad + (i/Math.max(losses.length-1, 50)) * (W-2*pad);
    const sy = (H-pad) - (losses[i]-minL)/(maxL-minL) * (H-2*pad);
    i===0?ctxl.moveTo(sx, sy):ctxl.lineTo(sx, sy);
  }
  ctxl.strokeStyle='#a78bfa'; ctxl.lineWidth=2.5; ctxl.stroke();
}

function updateStatus() {
  const L = landscapes[curL];
  const z = L.f(ball.x, ball.y);
  lossV.innerText = z.toFixed(3);
  
  const distToGlobal = Math.sqrt((ball.x-L.global.x)**2 + (ball.y-L.global.y)**2);
  const grad = L.df(ball.x, ball.y);
  const gradMag = Math.sqrt(grad.dx**2 + grad.dy**2);

  if(gradMag < 0.05) {
    if(distToGlobal < 0.5) {
      outcomeBadge.innerText = "Global Minimum Found! 🎉";
      outcomeBadge.className = "badge badge-global";
    } else {
      outcomeBadge.innerText = "Stuck in Local Minimum! 🕳️";
      outcomeBadge.className = "badge badge-local";
    }
  } else if(isRunning) {
    outcomeBadge.innerText = "Descending...";
    outcomeBadge.className = "badge badge-stuck";
  } else {
    outcomeBadge.innerText = "Ready to Drop";
    outcomeBadge.className = "badge";
  }
}

function step() {
  if(!isRunning) return;
  const L = landscapes[curL];
  const lr = parseFloat(lrSlider.value);
  const g = L.df(ball.x, ball.y);
  
  ball.x -= lr * g.dx;
  ball.y -= lr * g.dy;
  ball.path.push({x: ball.x, y: ball.y});
  
  const gradMag = Math.sqrt(g.dx**2 + g.dy**2);
  if(gradMag < 0.01 || ball.path.length > 200) {
    isRunning = false;
    runBtn.innerText = "▶ RUN DESCENT";
  }
  
  draw3D(); draw2D(); drawLoss(); updateStatus();
  if(isRunning) requestAnimationFrame(step);
}

// Events
lrSlider.oninput = () => { lrv.innerText = parseFloat(lrSlider.value).toFixed(2); };

runBtn.onclick = () => {
  if(isRunning) { isRunning = false; runBtn.innerText = "▶ RUN DESCENT"; }
  else { isRunning = true; runBtn.innerText = "⏸ PAUSE"; step(); }
};

resetBtn.onclick = () => {
  isRunning = false; runBtn.innerText = "▶ RUN DESCENT";
  const R = 3.5;
  ball.x = (Math.random() * 2 * R) - R;
  ball.y = (Math.random() * 2 * R) - R;
  ball.path = [{x: ball.x, y: ball.y}];
  draw3D(); draw2D(); drawLoss(); updateStatus();
};

cvs2.onclick = (e) => {
  const rect = cvs2.getBoundingClientRect();
  const mx = e.clientX - rect.left, my = e.clientY - rect.top;
  const R = 4.5;
  ball.x = (mx/cvs2.width)*2*R - R;
  ball.y = (1 - my/cvs2.height)*2*R - R;
  ball.path = [{x: ball.x, y: ball.y}];
  isRunning = false; runBtn.innerText = "▶ RUN DESCENT";
  draw3D(); draw2D(); drawLoss(); updateStatus();
};

document.querySelectorAll('[data-l]').forEach(b => {
  b.onclick = (e) => {
    document.querySelectorAll('[data-l]').forEach(x => x.classList.remove('active'));
    e.target.classList.add('active');
    curL = e.target.dataset.l;
    ball = {x: 2.5, y: 2.5, path: [{x: 2.5, y: 2.5}]};
    isRunning = false; runBtn.innerText = "▶ RUN DESCENT";
    draw3D(); draw2D(); drawLoss(); updateStatus();
  };
});

// Init
ball.path.push({x: ball.x, y: ball.y});
draw3D(); draw2D(); drawLoss(); updateStatus();
</script>
</body>
</html>
"""
    components.html(html_code, height=850, scrolling=False)


def main():
    st.title("🏔️ Page 54: Local vs Global Minimum")

    st.markdown(
        """
        In a perfect world, our loss function would be a nice, smooth bowl (convex). No matter where you start, you'd always roll straight to the bottom.

        But real-world AI models are **messy**. Their loss landscapes are full of bumps, ridges, and multiple valleys.
        This introduces a major headache: **The Local Minimum.**
        """
    )

    st.divider()

    col1, col2 = st.columns([1, 2.5])

    with col1:
        st.markdown("### 🕳️ Local vs. 🏆 Global")
        st.write("**Local Minimum:** A point that is lower than all its immediate neighbors, but not the lowest point in the entire landscape.")
        st.write("**Global Minimum:** The absolute lowest point possible. This is where we want our AI to end up.")

        st.info("**The Starting Point Matters!** Depending on where you initialize your weights (the ball), you might get trapped in a local dip forever.")

        st.markdown("### How to escape?")
        st.write("1. **Higher Learning Rate:** Might 'jump' over small bumps.")
        st.write("2. **Momentum:** Like a real ball, it uses speed to roll uphill briefly.")
        st.write("3. **Better Initialization:** Start closer to the 'right' valley.")

    with col2:
        render_lab()

    st.divider()

    st.markdown("### 🧠 The Conceptual Breakdown")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 1. Optimization is Greedy")
        st.write("Gradient Descent only looks at the **immediate slope**. It's like walking in a fog; you only see the next step. If that step is 'flat', you stop, even if a deeper valley is just one hill away.")

    with c2:
        st.markdown("#### 2. Saddle Points")
        st.write("In high dimensions (AI has millions), true local minima are actually rare! Instead, we often hit **Saddle Points**—flat areas that are minima in one direction but maxima in another.")

    with c3:
        st.markdown("#### 3. Why convexity is a luxury")
        st.write("Simple Linear Regression is convex (guaranteed best answer). Deep Neural Networks are non-convex. We trade the guarantee of the 'perfect' answer for the power to learn complex patterns.")

    st.divider()
    st.markdown(
        '<div style="color:#94a3b8;font-size:0.95rem;">Page 54 — you\'ve seen the traps of the landscape. Next: Convex Functions — why they are the "easy mode" of optimization!</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
