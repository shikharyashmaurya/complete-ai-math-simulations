import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Learning Rate — Step Size Matters", layout="wide")

def render_lr_lab():
    html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Inter',sans-serif;background:#0f172a;color:#fff;padding:16px;overflow:hidden;}
.wrap{max-width:1100px;margin:0 auto;display:flex;flex-direction:column;gap:20px;}
.top-row{display:flex;gap:20px;}
.controls{flex:1;display:flex;flex-direction:column;gap:12px;min-width:300px;}
.viz-col{flex:2;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);border-radius:20px;padding:20px;position:relative;}
.card{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:16px;}
h2{font-size:24px;font-weight:900;margin-bottom:4px;background:linear-gradient(90deg, #f472b6, #fb923c);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.sub{font-size:13px;color:#94a3b8;line-height:1.5;}
.lbl{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#94a3b8;margin-bottom:8px;display:block;}

.btn-group{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:12px;}
.pbtn{background:rgba(255,255,255,0.05);color:#cbd5e1;border:1px solid rgba(255,255,255,0.1);padding:10px 5px;border-radius:10px;font-weight:700;cursor:pointer;font-size:12px;transition:.2s;text-align:center;}
.pbtn:hover{background:rgba(255,255,255,0.1);}
.pbtn.active[data-lr="small"]{background:rgba(56,189,248,.2);border-color:#38bdf8;color:#38bdf8;}
.pbtn.active[data-lr="good"]{background:rgba(16,185,129,.2);border-color:#10b981;color:#10b981;}
.pbtn.active[data-lr="huge"]{background:rgba(244,114,182,.2);border-color:#f472b6;color:#f472b6;}

.slider-wrap{margin-top:10px;}
input[type=range]{width:100%;height:6px;background:rgba(255,255,255,0.1);border-radius:3px;outline:none;-webkit-appearance:none;margin-bottom:15px;}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:20px;height:20px;border-radius:50%;background:#fb923c;box-shadow:0 0 10px rgba(251,146,60,0.5);cursor:pointer;}

.action-row{display:flex;gap:10px;margin-top:10px;}
.act-btn{flex:1;padding:12px;border-radius:10px;font-weight:800;cursor:pointer;font-size:12px;letter-spacing:1px;text-transform:uppercase;transition:.2s;border:none;}
#runBtn{background:#fb923c;color:#0f172a;}
#runBtn:hover{background:#f97316;transform:translateY(-1px);}
#resetBtn{background:rgba(255,255,255,0.05);color:#fff;border:1px solid rgba(255,255,255,0.1);}
#resetBtn:hover{background:rgba(255,255,255,0.1);}

.stat-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:15px;}
.stat-box{background:rgba(0,0,0,0.2);padding:12px;border-radius:10px;border:1px solid rgba(255,255,255,0.05);}
.stat-val{font-family:monospace;font-size:18px;font-weight:900;display:block;margin-top:4px;}

canvas{display:block;width:100%;height:450px;background:transparent;cursor:crosshair;}
.legend{display:flex;justify-content:center;gap:20px;margin-top:15px;font-size:12px;color:#94a3b8;}
.leg-item{display:flex;align-items:center;gap:6px;}
.dot{width:10px;height:10px;border-radius:50%;}

#status-msg{position:absolute;top:30px;right:30px;padding:10px 20px;border-radius:12px;font-weight:800;font-size:14px;opacity:0;transition:0.3s;}
.msg-diverge{background:rgba(244,114,182,0.9);color:#fff;box-shadow:0 0 20px rgba(244,114,182,0.4);}
.msg-converge{background:rgba(16,185,129,0.9);color:#fff;box-shadow:0 0 20px rgba(16,185,129,0.4);}
</style>
</head>
<body>
<div id="status-msg">DIVERGING! ⚠️</div>
<div class="wrap">
  <div class="top-row">
    <div class="controls">
      <div class="card">
        <h2>The Goldilocks Dilemma 🐻</h2>
        <p class="sub">The Learning Rate (η) is the most important knob in AI. It controls how far we jump down the hill at every step.</p>
      </div>

      <div class="card">
        <span class="lbl">Choose your Pace</span>
        <div class="btn-group" id="lbtns">
          <button class="pbtn" data-lr="small" data-val="0.02">🐌 SLOW</button>
          <button class="pbtn active" data-lr="good" data-val="0.15">✅ GOOD</button>
          <button class="pbtn" data-lr="huge" data-val="1.05">💥 CHAOS</button>
        </div>
        <div class="slider-wrap">
          <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
            <span class="lbl" style="margin:0;">Custom Rate η</span>
            <span id="lrValDisp" style="font-weight:900;color:#fb923c;font-family:monospace;">0.150</span>
          </div>
          <input type="range" id="lrSlider" min="0.001" max="1.1" step="0.001" value="0.15">
        </div>
      </div>

      <div class="card">
        <div class="action-row">
          <button class="act-btn" id="runBtn">▶ START RACE</button>
          <button class="act-btn" id="resetBtn">🔄 RESET</button>
        </div>
        <p class="sub" style="font-size:10px;margin-top:10px;text-align:center;">Click the curve to set a new starting position!</p>
      </div>

      <div class="stat-grid">
        <div class="stat-box">
          <span class="lbl">Current Loss</span>
          <span class="stat-val" id="lossVal" style="color:#f472b6;">0.000</span>
        </div>
        <div class="stat-box">
          <span class="lbl">Total Steps</span>
          <span class="stat-val" id="stepVal" style="color:#38bdf8;">0</span>
        </div>
      </div>
    </div>

    <div class="viz-col">
      <span class="lbl" style="position:absolute;top:20px;left:20px;">Loss Landscape: f(x) = x²</span>
      <canvas id="mainCvs"></canvas>
      <div class="legend">
        <div class="leg-item"><div class="dot" style="background:#fb923c;"></div> Current Step</div>
        <div class="leg-item"><div class="dot" style="background:rgba(255,255,255,0.2); border:1px dashed #fff;"></div> Previous Path</div>
        <div class="leg-item"><div class="dot" style="background:#10b981;"></div> Minimum (Goal)</div>
      </div>
    </div>
  </div>
</div>

<script>
const cvs = document.getElementById('mainCvs');
const ctx = cvs.getContext('2d');
const lrSlider = document.getElementById('lrSlider');
const lrValDisp = document.getElementById('lrValDisp');
const runBtn = document.getElementById('runBtn');
const resetBtn = document.getElementById('resetBtn');
const lossValEl = document.getElementById('lossVal');
const stepValEl = document.getElementById('stepVal');
const statusMsg = document.getElementById('status-msg');

let lr = 0.15;
let ballX = -4.0;
let path = [];
let steps = 0;
let running = false;
let diverged = false;

// Function: f(x) = x^2, df(x) = 2x
const f = (x) => x*x;
const df = (x) => 2*x;

const RANGE = 6;
const PAD = 50;

function resize() {
  cvs.width = Math.min(cvs.clientWidth, 1200);
  cvs.height = Math.min(cvs.clientHeight, 450);
  draw();
}

function w2s(x, y) {
  return {
    sx: PAD + (x + RANGE) / (2 * RANGE) * (cvs.width - 2 * PAD),
    sy: (cvs.height - PAD) - (y / (RANGE*RANGE)) * (cvs.height - 2 * PAD)
  };
}

function s2w(sx, sy) {
  return {
    x: (sx - PAD) / (cvs.width - 2 * PAD) * (2 * RANGE) - RANGE,
    y: ( (cvs.height - PAD) - sy ) / (cvs.height - 2 * PAD) * (RANGE * RANGE)
  };
}

function draw() {
  ctx.clearRect(0, 0, cvs.width, cvs.height);
  
  // Draw Curve
  ctx.beginPath();
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
  ctx.lineWidth = 3;
  for (let i = -RANGE; i <= RANGE; i += 0.1) {
    const p = w2s(i, f(i));
    if (i === -RANGE) ctx.moveTo(p.sx, p.sy);
    else ctx.lineTo(p.sx, p.sy);
  }
  ctx.stroke();

  // Draw Minimum
  const goal = w2s(0, 0);
  ctx.beginPath();
  ctx.arc(goal.sx, goal.sy, 5, 0, Math.PI*2);
  ctx.fillStyle = '#10b981';
  ctx.shadowBlur = 15;
  ctx.shadowColor = '#10b981';
  ctx.fill();
  ctx.shadowBlur = 0;

  // Draw Path
  if (path.length > 0) {
    ctx.beginPath();
    ctx.setLineDash([5, 5]);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.4)';
    ctx.lineWidth = 1.5;
    const p0 = w2s(path[0], f(path[0]));
    ctx.moveTo(p0.sx, p0.sy);
    for (let i = 1; i < path.length; i++) {
      const p = w2s(path[i], f(path[i]));
      ctx.lineTo(p.sx, p.sy);
    }
    ctx.stroke();
    ctx.setLineDash([]);
    
    // Path points
    path.forEach((px, idx) => {
      const p = w2s(px, f(px));
      ctx.beginPath();
      ctx.arc(p.sx, p.sy, 3, 0, Math.PI*2);
      ctx.fillStyle = 'rgba(255,255,255,0.3)';
      ctx.fill();
    });
  }

  // Draw Ball
  if (!diverged) {
    const b = w2s(ballX, f(ballX));
    ctx.beginPath();
    ctx.arc(b.sx, b.sy, 10, 0, Math.PI*2);
    const grad = ctx.createRadialGradient(b.sx-3, b.sy-3, 2, b.sx, b.sy, 10);
    grad.addColorStop(0, '#fff');
    grad.addColorStop(1, '#fb923c');
    ctx.fillStyle = grad;
    ctx.shadowBlur = 20;
    ctx.shadowColor = '#fb923c';
    ctx.fill();
    ctx.shadowBlur = 0;
    
    // Gradient Arrow
    const slope = df(ballX);
    const arrowLen = Math.min(1.5, Math.abs(slope)) * (slope > 0 ? -1 : 1) * 30;
    ctx.beginPath();
    ctx.moveTo(b.sx, b.sy);
    ctx.lineTo(b.sx + arrowLen, b.sy);
    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 2;
    ctx.stroke();
  }

  // Update UI
  lossValEl.innerText = f(ballX).toFixed(4);
  stepValEl.innerText = steps;
}

let stepTimeout = null;
let stepFrame = null;
let statusTimeout = null;

function stopRace() {
  running = false;
  if (stepTimeout !== null) {
    clearTimeout(stepTimeout);
    stepTimeout = null;
  }
  if (stepFrame !== null) {
    cancelAnimationFrame(stepFrame);
    stepFrame = null;
  }
}

function step() {
  stepFrame = null;
  if (!running || diverged) return;

  path.push(ballX);
  const grad = df(ballX);
  ballX = ballX - lr * grad;
  steps++;

  if (Math.abs(ballX) > RANGE * 2) {
    diverged = true;
    running = false;
    runBtn.innerText = "▶ START RACE";
    showStatus("DIVERGED! 💥", "msg-diverge");
  } else if (Math.abs(grad) < 0.001) {
    running = false;
    runBtn.innerText = "▶ START RACE";
    showStatus("CONVERGED! 🎯", "msg-converge");
  }

  draw();
  if (running) stepTimeout = setTimeout(() => {
    stepTimeout = null;
    stepFrame = requestAnimationFrame(step);
  }, 100);
}

function showStatus(txt, cls) {
  statusMsg.innerText = txt;
  statusMsg.className = cls;
  statusMsg.style.opacity = 1;
  if (statusTimeout !== null) clearTimeout(statusTimeout);
  statusTimeout = setTimeout(() => {
    statusMsg.style.opacity = 0;
    statusTimeout = null;
  }, 3000);
}

runBtn.addEventListener('click', () => {
  if (diverged) {
    reset();
  }
  if (running) {
    stopRace();
  } else {
    running = true;
  }
  runBtn.innerText = running ? "⏸ PAUSE" : "▶ START RACE";
  if (running) step();
});

function reset() {
  stopRace();
  ballX = -4.0 + (Math.random() * 2);
  path = [];
  steps = 0;
  running = false;
  diverged = false;
  runBtn.innerText = "▶ START RACE";
  draw();
}

resetBtn.addEventListener('click', reset);

lrSlider.addEventListener('input', (e) => {
  lr = parseFloat(e.target.value);
  lrValDisp.innerText = lr.toFixed(3);
  document.querySelectorAll('.pbtn').forEach(b => b.classList.remove('active'));
  draw();
});

document.querySelectorAll('.pbtn').forEach(btn => {
  btn.addEventListener('click', (e) => {
    document.querySelectorAll('.pbtn').forEach(b => b.classList.remove('active'));
    e.target.classList.add('active');
    lr = parseFloat(e.target.dataset.val);
    lrSlider.value = lr;
    lrValDisp.innerText = lr.toFixed(3);
    draw();
  });
});

cvs.addEventListener('mousedown', (e) => {
  stopRace();
  runBtn.innerText = "▶ START RACE";
  const rect = cvs.getBoundingClientRect();
  const {x} = s2w(e.clientX - rect.left, e.clientY - rect.top);
  ballX = Math.max(-RANGE, Math.min(RANGE, x));
  path = [];
  steps = 0;
  diverged = false;
  draw();
});

window.addEventListener('resize', resize);
window.addEventListener('pagehide', () => {
  stopRace();
  if (statusTimeout !== null) clearTimeout(statusTimeout);
});
resize();
</script>
</body>
</html>
"""
    components.html(html_code, height=600, scrolling=False)

def main():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap');
            .main-header {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(90deg, #f472b6, #fb923c);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 3.2rem;
                font-weight: 900;
                margin-bottom: 0;
            }
            .sub-header {
                font-family: 'Inter', sans-serif;
                font-size: 1.2rem;
                color: #94a3b8;
                margin-bottom: 2rem;
            }
            .stat-card {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 1.5rem;
                height: 100%;
            }
            .lr-tag {
                padding: 4px 10px;
                border-radius: 6px;
                font-size: 0.8rem;
                font-weight: 800;
                text-transform: uppercase;
                margin-bottom: 10px;
                display: inline-block;
            }
            .tag-small { background: rgba(56, 189, 248, 0.15); color: #38bdf8; }
            .tag-good { background: rgba(16, 185, 129, 0.15); color: #10b981; }
            .tag-huge { background: rgba(244, 114, 182, 0.15); color: #f472b6; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-header">Learning Rate</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Optimization #53: Finding the Perfect Stride</p>', unsafe_allow_html=True)

    st.markdown("""
    In Gradient Descent, the **Gradient** tells us which direction is downhill. But it doesn't tell us **how far** to walk. 
    That stride length is the **Learning Rate (η)**.
    """)

    render_lr_lab()

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown('<span class="lr-tag tag-small">η = 0.01 (Small)</span>', unsafe_allow_html=True)
        st.markdown("### 🐌 The Slug")
        st.write("Safe but incredibly slow. It takes thousands of steps to reach the bottom. In real AI, this would waste days of electricity.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown('<span class="lr-tag tag-good">η = 0.15 (Optimal)</span>', unsafe_allow_html=True)
        st.markdown("### ✅ The Athlete")
        st.write("Efficient and purposeful. It takes large enough steps to move quickly, but small enough to settle into the minimum without bouncing.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown('<span class="lr-tag tag-huge">η = 1.05 (Huge)</span>', unsafe_allow_html=True)
        st.markdown("### 💥 The Chaos")
        st.write("Overconfident. The steps are so large that the ball overshoots the valley, landing higher on the other side. This leads to **Divergence**.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    st.markdown("### 🤖 Bridge to AI: Why Experts Hate Static Rates")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("""
        Finding the perfect learning rate is so hard that modern AI models don't just pick one number. They use **Schedules** and **Optimizers**:
        
        1. **LR Schedulers**: Start fast (high η) to explore, then slow down (low η) as you get close to the bottom to "fine-tune."
        2. **Adaptive Optimizers (Adam)**: Every single weight in the neural network gets its own individual learning rate that adjusts automatically based on how much it has moved recently.
        
        **The Math:**
        If $\\eta$ is too high, the update $\\mathbf{w} - \\eta \\nabla L$ actually increases the loss.
        Mathematically, we want $\\eta < \\frac{2}{\\lambda_{max}}$ where $\\lambda$ is the curvature, but since we can't easily calculate that, we experiment!
        """)
    
    with c2:
        st.success("💡 **Pro Tip:** If your loss is NaN or infinity during training, your Learning Rate is likely too high! Try dividing it by 10.")

    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #64748b; font-size: 0.8rem;">Page 53 — Learning Rate. Next: <b>Local vs Global Minimum — Getting Stuck</b></div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
