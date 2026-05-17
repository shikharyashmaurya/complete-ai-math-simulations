import streamlit as st
import streamlit.components.v1 as components
import numpy as np

st.set_page_config(page_title="Integral as Area", layout="wide")

def render_integral_lab():
    html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Inter',sans-serif;background:#0f172a;color:white;padding:10px;overflow:hidden;}
.outer{display:flex;flex-direction:row;gap:20px;max-width:1200px;margin:0 auto;height:650px;}
.controls{flex:0.8;display:flex;flex-direction:column;gap:12px;}
.viz-col{flex:2;display:flex;flex-direction:column;gap:12px;position:relative;}
.card{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:14px;padding:16px;}
h2{font-size:20px;font-weight:900;color:#f8fafc;margin-bottom:4px;}
.sub{font-size:12px;color:#94a3b8;line-height:1.4;}
.clabel{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;color:#94a3b8;display:flex;justify-content:space-between;}
.func-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;}
.fbtn{background:rgba(255,255,255,0.05);color:#cbd5e1;border:1px solid rgba(255,255,255,0.1);padding:10px 6px;border-radius:9px;font-weight:700;cursor:pointer;transition:.2s;text-align:center;font-size:12px;}
.fbtn:hover{background:rgba(255,255,255,0.1);}
.fbtn.active{background:rgba(34,211,238,0.2);border-color:#22d3ee;color:#22d3ee;box-shadow:0 0 12px rgba(34,211,238,0.3);}

input[type=range]{width:100%;height:6px;background:rgba(255,255,255,0.1);border-radius:3px;outline:none;-webkit-appearance:none;margin-bottom:8px;}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;background:#22d3ee;cursor:pointer;box-shadow:0 0 8px #22d3ee;}

.stats{background:rgba(0,0,0,0.3);border-radius:12px;padding:16px;border:1px solid rgba(255,255,255,0.06);display:flex;flex-direction:column;gap:10px;}
.stat-row{display:flex;justify-content:space-between;align-items:center;padding:4px 0;}
.stat-label{font-size:12px;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:0.5px;}
.stat-val{font-family:'JetBrains Mono', monospace;font-size:19px;font-weight:900;color:#22d3ee;text-shadow: 0 0 10px rgba(34,211,238,0.3);}
.error-val{color:#f43f5e;font-size:11px;font-weight:800;background:rgba(244,63,94,0.1);padding:2px 8px;border-radius:20px;}

canvas{border-radius:14px;background:#0f172a;border:1px solid rgba(255,255,255,0.08);width:100%;height:100%;box-shadow: inset 0 0 40px rgba(0,0,0,0.5);}
.cvs-wrap{flex:1;position:relative;background: #0f172a; border-radius:14px; padding:2px;}

.math-card{font-family:'Inter', sans-serif; font-weight:800; text-align:center;font-size:16px;padding:12px;background:rgba(34,211,238,0.1);border:1px solid rgba(34,211,238,0.3);color:#22d3ee; border-radius:10px;}
</style>
</head>
<body>
<div class="outer">
  <div class="controls">
    <div class="card">
      <h2 style="display:flex; align-items:center; gap:8px;">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#22d3ee" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
        The Area Lab
      </h2>
      <p class="sub">Integrals measure the total accumulated "stuff" under a curve. Watch how thin slices build the whole!</p>
    </div>

    <div class="card">
      <div class="clabel">Select Function</div>
      <div class="func-grid" id="fbtns">
        <button class="fbtn active" data-f="quadratic">y = x²</button>
        <button class="fbtn" data-f="sine">y = sin(x) + 1.2</button>
        <button class="fbtn" data-f="bell">Gaussian (Bell)</button>
        <button class="fbtn" data-f="sigmoid">Sigmoid σ(x)</button>
      </div>
    </div>

    <div class="card">
      <div class="clabel"><span>Range [a, b]</span><span id="range-val" style="color:#22d3ee">-2.0 to 2.0</span></div>
      <div style="display:flex; gap:10px; margin-bottom:12px;">
        <input type="range" id="range-a" min="-4" max="0" step="0.1" value="-2">
        <input type="range" id="range-b" min="0" max="4" step="0.1" value="2">
      </div>
      
      <div class="clabel"><span>Precision (n slices)</span><span id="n-val" style="color:#22d3ee">10</span></div>
      <input type="range" id="range-n" min="1" max="100" step="1" value="10">
    </div>

    <div class="stats">
      <div class="stat-row">
        <span class="stat-label">Riemann Sum</span>
        <span class="stat-val" id="sum-val">0.000</span>
      </div>
      <div class="stat-row" style="border-top: 1px solid rgba(255,255,255,0.05); padding-top:8px;">
        <span class="stat-label">Calculus Exact</span>
        <span class="stat-val" id="true-val" style="color:#f8fafc">0.000</span>
      </div>
      <div class="stat-row" style="justify-content: flex-end; margin-top:4px;">
         <span class="error-val" id="err-val">ERROR: 0.0%</span>
      </div>
    </div>

    <div class="math-card" id="math-display">
      ∫ x² dx
    </div>
  </div>

  <div class="viz-col">
    <div class="cvs-wrap">
      <canvas id="main-cvs"></canvas>
    </div>
    <div class="card" style="padding:10px; font-size:11px; color:#94a3b8; text-align:center; background:transparent; border:none;">
       <span style="color:#22d3ee; font-weight:bold;">PRO TIP:</span> Drag the precision slider to see the rectangles converge to the smooth curve!
    </div>
  </div>
</div>

<script>
const canvas = document.getElementById('main-cvs');
const ctx = canvas.getContext('2d');

const funcs = {
  quadratic: {
    f: x => x*x,
    F: x => (x*x*x)/3,
    label: "∫ x² dx",
    yRange: [0, 16]
  },
  sine: {
    f: x => Math.sin(x) + 1.2,
    F: x => -Math.cos(x) + 1.2*x,
    label: "∫ (sin(x) + 1.2) dx",
    yRange: [0, 2.5]
  },
  bell: {
    f: x => Math.exp(-x*x),
    // erf approximation or just numerical for true
    F: x => {
      // Numerical integration for Gaussian is better for display
      return null; 
    },
    label: "∫ e^(-x²) dx",
    yRange: [0, 1.2]
  },
  sigmoid: {
    f: x => 1 / (1 + Math.exp(-x)),
    F: x => Math.log(1 + Math.exp(x)),
    label: "∫ σ(x) dx",
    yRange: [0, 1.2]
  }
};

let currentF = 'quadratic';
let a = -2, b = 2, n = 10;

function resize() {
  const rect = canvas.parentElement.getBoundingClientRect();
  canvas.width = rect.width * devicePixelRatio;
  canvas.height = rect.height * devicePixelRatio;
  canvas.style.width = rect.width + 'px';
  canvas.style.height = rect.height + 'px';
  ctx.scale(devicePixelRatio, devicePixelRatio);
  draw();
}

function getTrueIntegral(fa, fb) {
  const f = funcs[currentF];
  if (f.F) {
    return f.F(fb) - f.F(fa);
  } else {
    // Numerical fallback for Bell
    let sum = 0;
    const steps = 1000;
    const dx = (fb - fa) / steps;
    for (let i = 0; i < steps; i++) {
      sum += f.f(fa + i * dx + dx/2) * dx;
    }
    return sum;
  }
}

function draw() {
  const w = canvas.width / devicePixelRatio;
  const h = canvas.height / devicePixelRatio;
  ctx.clearRect(0, 0, w, h);

  const fn = funcs[currentF];
  
  // Coordinate system
  const xMin = -5, xMax = 5;
  const [yMin, yMax] = fn.yRange;
  
  const toSX = x => (x - xMin) / (xMax - xMin) * w;
  const toSY = y => h - (y - yMin) / (yMax - yMin) * h;

  // Grid
  ctx.strokeStyle = 'rgba(255,255,255,0.05)';
  ctx.lineWidth = 1;
  for(let x=xMin; x<=xMax; x++) {
    ctx.beginPath(); ctx.moveTo(toSX(x), 0); ctx.lineTo(toSX(x), h); ctx.stroke();
  }
  for(let y=yMin; y<=yMax; y += (yMax-yMin)/10) {
    ctx.beginPath(); ctx.moveTo(0, toSY(y)); ctx.lineTo(w, toSY(y)); ctx.stroke();
  }

  // Axes
  ctx.strokeStyle = 'rgba(255,255,255,0.2)';
  ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(toSX(0), 0); ctx.lineTo(toSX(0), h); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(0, toSY(0)); ctx.lineTo(w, toSY(0)); ctx.stroke();

  // Draw Riemann Rectangles
  const dx = (b - a) / n;
  let riemannSum = 0;

  ctx.lineWidth = 1;
  for (let i = 0; i < n; i++) {
    const xLeft = a + i * dx;
    const xMid = xLeft + dx/2;
    const val = fn.f(xMid);
    riemannSum += val * dx;

    const sx = toSX(xLeft);
    const sw = toSX(xLeft + dx) - sx;
    const sy = toSY(val);
    const sh = toSY(0) - sy;

    // Gradient-like fill
    const grad = ctx.createLinearGradient(sx, sy, sx, toSY(0));
    grad.addColorStop(0, 'rgba(34, 211, 238, 0.6)');
    grad.addColorStop(1, 'rgba(34, 211, 238, 0.1)');
    
    ctx.fillStyle = grad;
    ctx.fillRect(sx, sy, sw, sh);
    ctx.strokeStyle = 'rgba(34, 211, 238, 0.8)';
    ctx.strokeRect(sx, sy, sw, sh);
  }

  // Draw smooth curve
  ctx.beginPath();
  ctx.strokeStyle = '#f8fafc';
  ctx.lineWidth = 3;
  for (let sx = 0; sx < w; sx++) {
    const x = xMin + (sx / w) * (xMax - xMin);
    const y = fn.f(x);
    const sy = toSY(y);
    if (sx === 0) ctx.moveTo(sx, sy);
    else ctx.lineTo(sx, sy);
  }
  ctx.stroke();

  // Update UI
  document.getElementById('sum-val').innerText = riemannSum.toFixed(4);
  const trueI = getTrueIntegral(a, b);
  document.getElementById('true-val').innerText = trueI.toFixed(4);
  const err = Math.abs((riemannSum - trueI) / (trueI || 1)) * 100;
  document.getElementById('err-val').innerText = `Error: ${err.toFixed(2)}%`;
  document.getElementById('range-val').innerText = `${a.toFixed(1)} to ${b.toFixed(1)}`;
  document.getElementById('n-val').innerText = n;
  document.getElementById('math-display').innerText = fn.label;
}

// Controls
document.getElementById('range-a').addEventListener('input', (e) => {
  a = parseFloat(e.target.value);
  draw();
});
document.getElementById('range-b').addEventListener('input', (e) => {
  b = parseFloat(e.target.value);
  draw();
});
document.getElementById('range-n').addEventListener('input', (e) => {
  n = parseInt(e.target.value);
  draw();
});

document.querySelectorAll('.fbtn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.fbtn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentF = btn.dataset.f;
    draw();
  });
});

window.addEventListener('resize', resize);
setTimeout(resize, 100);

</script>
</body>
</html>
"""
    components.html(html_code, height=700, scrolling=False)

def main():
    st.markdown("<h1 style='text-align: center; color: #22d3ee;'>📉 Page 49: Integral as Area</h1>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="background: rgba(34, 211, 238, 0.05); padding: 20px; border-radius: 15px; border-left: 5px solid #22d3ee; margin-bottom: 25px;">
        If <b>Derivatives</b> are about breaking things down into tiny slopes, 
        <b>Integrals</b> are about building them back up into a total quantity.
        <br><br>
        The most intuitive way to see an integral is as the <b>Area under a curve</b>. 
        Think of it as adding up an infinite number of infinitely thin rectangles.
        </div>
        """, unsafe_allow_html=True
    )

    col_main, col_sidebar = st.columns([3, 1])

    with col_main:
        st.markdown("### 🧪 The Riemann Sum Laboratory")
        st.markdown("Experiment with how we approximate the area using rectangles. As you increase the number of slices (**n**), the approximation gets closer and closer to the 'True' mathematical value.")
        render_integral_lab()

    with col_sidebar:
        st.markdown("### 📝 Key Concepts")
        st.info("**1. Riemann Sum**\nApproximating area by summing rectangles. More rectangles = better accuracy.")
        st.success("**2. The Fundamental Theorem**\nIntegration is the inverse of differentiation. If $F'(x) = f(x)$, then $\int_a^b f(x) dx = F(b) - F(a)$.")
        st.warning("**3. Limits**\nThe definite integral is defined as the limit of the sum as $n \\to \\infty$.")

    st.divider()
    
    # AI Bridge Section
    st.markdown("### 🤖 Bridge to AI: Why Integrals Matter")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("#### 🎲 Probability Density")
        st.write("In AI, we deal with continuous probabilities. The probability of a value falling in a range $[a, b]$ is the **area** under the probability curve.")
        st.latex(r"P(a \leq X \leq b) = \int_a^b p(x) dx")
        
    with c2:
        st.markdown("#### 📏 Expectation")
        st.write("To find the 'Average' (Expected Value) of a continuous variable, we integrate the value weighted by its probability.")
        st.latex(r"E[X] = \int_{-\infty}^{\infty} x \cdot p(x) dx")
        
    with c3:
        st.markdown("#### 🌊 Information Theory")
        st.write("Entropy and KL Divergence (used to compare models) are essentially integrals measuring the 'surprise' or 'gap' between distributions.")
        st.latex(r"H(P) = -\int P(x) \log P(x) dx")

    st.divider()
    st.markdown(
        '<div style="color:#94a3b8;font-size:0.95rem;text-align:center;">Page 49 — You\'ve visualized the core of calculus. Next: Section 8 — Optimization, where we use these tools to train AI!</div>',
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
