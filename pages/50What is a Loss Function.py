import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="What is a Loss Function?", layout="wide")

def render_lab():
    html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Inter',sans-serif;background:#0f172a;color:white;padding:20px;overflow:hidden;}
.outer{display:flex;flex-direction:column;gap:15px;max-width:1100px;margin:0 auto;}
.top-row{display:flex;flex-direction:row;gap:20px;}
.controls{flex:1;display:flex;flex-direction:column;gap:12px;}
.viz-col{flex:1.8;position:relative;background:rgba(255,255,255,0.02);border-radius:20px;border:1px solid rgba(255,255,255,0.08);padding:15px;display:flex;flex-direction:column;}
.card{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:16px;transition:0.3s;}
.card:hover{background:rgba(255,255,255,0.06);}
h2{font-size:22px;font-weight:900;color:#f8fafc;margin-bottom:4px;display:flex;align-items:center;gap:10px;}
.sub{font-size:13px;color:#94a3b8;line-height:1.5;}

.loss-meter-wrap{margin-top:10px;display:flex;flex-direction:column;gap:5px;}
.meter-label{font-size:11px;font-weight:800;text-transform:uppercase;color:#94a3b8;letter-spacing:1px;}
.meter-bg{width:100%;height:35px;background:rgba(255,255,255,0.05);border-radius:8px;position:relative;overflow:hidden;border:1px solid rgba(255,255,255,0.1);}
#meter-fill{height:100%;width:50%;background:linear-gradient(90deg, #10b981, #f59e0b, #ef4444);transition:0.3s cubic-bezier(0.17, 0.67, 0.83, 0.67);}
#loss-val{position:absolute;right:12px;top:50%;transform:translateY(-50%);font-weight:900;font-size:18px;text-shadow:0 2px 4px rgba(0,0,0,0.5);}

.mode-toggle{display:flex;background:rgba(255,255,255,0.05);border-radius:10px;padding:4px;gap:4px;}
.mbtn{flex:1;padding:10px;border-radius:8px;border:none;background:none;color:#94a3b8;font-weight:700;cursor:pointer;font-size:12px;transition:0.2s;}
.mbtn.active{background:#6366f1;color:white;box-shadow:0 4px 12px rgba(99, 102, 241, 0.3);}

.slabel{display:flex;justify-content:space-between;font-size:13px;font-weight:700;margin-bottom:4px;}
.sval{font-size:15px;font-weight:900;color:#6366f1;font-variant-numeric:tabular-nums;}
input[type=range]{width:100%;height:6px;background:rgba(255,255,255,0.1);border-radius:3px;outline:none;-webkit-appearance:none;margin-bottom:12px;}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;background:#6366f1;cursor:pointer;box-shadow:0 0 10px rgba(99, 102, 241, 0.5);}

canvas{border-radius:12px;cursor:crosshair;touch-action:none;display:block;max-width:100%;}
.badge{background:rgba(99, 102, 241, 0.15);color:#818cf8;padding:4px 10px;border-radius:99px;font-size:11px;font-weight:800;border:1px solid rgba(99, 102, 241, 0.3);}

.hint{font-size:11px;color:#64748b;margin-top:8px;font-style:italic;}
</style>
</head>
<body>
<div class="outer">
  <div class="top-row">
    <div class="controls">
      <div class="card">
        <h2>Penalty Box 🥊</h2>
        <p class="sub">The <b>Loss Function</b> is your "Regret Meter". It measures how far your prediction (the line) is from reality (the points).</p>
      </div>

      <div class="card">
        <div class="slabel"><span>Line Slope (Weight <i>w</i>)</span><span id="wv" class="sval">1.00</span></div>
        <input type="range" id="w-range" min="-3" max="3" step="0.05" value="1.0">
        
        <div class="slabel"><span>Line Shift (Bias <i>b</i>)</span><span id="bv" class="sval">0.00</span></div>
        <input type="range" id="b-range" min="-100" max="100" step="1" value="0">
      </div>

      <div class="card">
        <div class="meter-label">Loss Type</div>
        <div class="mode-toggle">
          <button class="mbtn active" id="btn-mse">MSE (Squared)</button>
          <button class="mbtn" id="btn-mae">MAE (Absolute)</button>
        </div>
        <p class="hint" id="mode-desc">MSE squares the errors, making big misses hurt way more than small ones!</p>
      </div>

      <div class="card">
        <div class="loss-meter-wrap">
          <div class="meter-label">Total Loss (The Goal: Minimize)</div>
          <div class="meter-bg">
            <div id="meter-fill"></div>
            <span id="loss-val">0</span>
          </div>
        </div>
      </div>
      
      <div class="card" style="display:flex; gap:10px; align-items:center; justify-content:center;">
          <button class="mbtn" style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1);" onclick="resetPoints()">🔄 Reset Data</button>
          <button class="mbtn" style="background:rgba(16, 185, 129, 0.1); color:#10b981; border:1px solid #10b981;" onclick="solveBestFit()">✨ Perfect Fit</button>
      </div>
    </div>

    <div class="viz-col">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
        <span class="badge">LIVE DATA PLAYGROUND</span>
        <span style="font-size:12px; color:#64748b;">Click/Drag to move points!</span>
      </div>
      <canvas id="main-canvas"></canvas>
    </div>
  </div>
</div>

<script>
const canvas = document.getElementById('main-canvas');
const ctx = canvas.getContext('2d');
const wRange = document.getElementById('w-range');
const bRange = document.getElementById('b-range');
const wvDisplay = document.getElementById('wv');
const bvDisplay = document.getElementById('bv');
const lossVal = document.getElementById('loss-val');
const meterFill = document.getElementById('meter-fill');
const btnMse = document.getElementById('btn-mse');
const btnMae = document.getElementById('btn-mae');
const modeDesc = document.getElementById('mode-desc');

let points = [];
let draggingPoint = null;
let lossType = 'MSE'; // MSE or MAE
let width, height;

function init() {
    resize();
    createPoints();
    render();
}

function resize() {
    const parent = canvas.parentElement;
    const oldWidth = width;
    const oldHeight = height;
    width = Math.max(1, Math.min(parent.clientWidth - 30, 1200));
    height = 420;
    canvas.width = width;
    canvas.height = height;
    canvas.style.width = width + 'px';
    if (points.length && oldWidth && oldHeight) {
        points.forEach(p => {
            p.x = p.x / oldWidth * width;
            p.y = p.y / oldHeight * height;
        });
    } else if (points.length) {
        createPoints();
    }
    if (points.length) render();
}

function createPoints() {
    points = [];
    const n = 10;
    const trueW = (Math.random() - 0.5) * 2;
    const trueB = (Math.random() - 0.5) * 100;
    for(let i=0; i<n; i++) {
        let rx = (i / (n-1)) * (width - 100) + 50;
        let ry = (rx - width/2) * trueW + (height/2 - trueB) + (Math.random()-0.5)*80;
        points.push({x: rx, y: ry, id: i});
    }
}

function resetPoints() {
    createPoints();
    render();
}

function solveBestFit() {
    // Linear regression formula
    let n = points.length;
    if (!n) return;
    let sumX = 0, sumY = 0, sumXY = 0, sumXX = 0;
    points.forEach(p => {
        let x = p.x - width/2;
        let y = height/2 - p.y;
        sumX += x; sumY += y;
        sumXY += x * y; sumXX += x * x;
    });
    const denominator = n * sumXX - sumX * sumX;
    let w = Math.abs(denominator) > 1e-9
        ? (n * sumXY - sumX * sumY) / denominator
        : 0;
    let b = (sumY - w * sumX) / n;
    
    wRange.value = w.toFixed(2);
    bRange.value = b.toFixed(0);
    render();
}

canvas.onmousedown = (e) => {
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    
    points.forEach(p => {
        const dx = p.x - mx;
        const dy = p.y - my;
        if(dx*dx + dy*dy < 400) draggingPoint = p;
    });
};

window.onmousemove = (e) => {
    if(!draggingPoint) return;
    const rect = canvas.getBoundingClientRect();
    draggingPoint.x = e.clientX - rect.left;
    draggingPoint.y = e.clientY - rect.top;
    render();
};

window.onmouseup = () => draggingPoint = null;
function render() {
    update();
    draw();
}

let totalLoss = 0;

wRange.addEventListener('input', render);
bRange.addEventListener('input', render);
window.addEventListener('resize', resize);
window.addEventListener('pagehide', () => {
    window.onmousemove = null;
    window.onmouseup = null;
});

function update() {
    wvDisplay.innerText = parseFloat(wRange.value).toFixed(2);
    bvDisplay.innerText = bRange.value;
    
    const w = parseFloat(wRange.value);
    const b = parseFloat(bRange.value);
    
    totalLoss = 0;
    points.forEach(p => {
        const x_coord = p.x - width/2;
        const pred_y_coord = x_coord * w + b;
        const actual_y_coord = height/2 - p.y;
        
        const error = actual_y_coord - pred_y_coord;
        if(lossType === 'MSE') {
            totalLoss += error * error;
        } else {
            totalLoss += Math.abs(error);
        }
    });
    
    totalLoss = totalLoss / points.length;
    
    lossVal.innerText = totalLoss.toFixed(0);
    
    // Scale meter fill
    let maxExpected = lossType === 'MSE' ? 10000 : 200;
    let percent = Math.min(100, (totalLoss / maxExpected) * 100);
    meterFill.style.width = percent + '%';
    
    // Color shift
    if(percent < 10) meterFill.style.background = '#10b981';
    else if(percent < 30) meterFill.style.background = '#f59e0b';
    else meterFill.style.background = '#ef4444';
}

function draw() {
    ctx.clearRect(0, 0, width, height);
    
    // Grid
    ctx.strokeStyle = 'rgba(255,255,255,0.03)';
    ctx.lineWidth = 1;
    for(let i=0; i<width; i+=40) {
        ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, height); ctx.stroke();
    }
    for(let i=0; i<height; i+=40) {
        ctx.beginPath(); ctx.moveTo(0, i); ctx.lineTo(width, i); ctx.stroke();
    }
    
    // Axes
    ctx.strokeStyle = 'rgba(255,255,255,0.1)';
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(width/2, 0); ctx.lineTo(width/2, height); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(0, height/2); ctx.lineTo(width, height/2); ctx.stroke();

    const w = parseFloat(wRange.value);
    const b = parseFloat(bRange.value);

    // Draw Error Bars / Rects
    points.forEach(p => {
        const x_coord = p.x - width/2;
        const pred_y_coord = x_coord * w + b;
        const pred_canvas_y = height/2 - pred_y_coord;
        
        const error = Math.abs(p.y - pred_canvas_y);
        
        if(lossType === 'MSE') {
            // Draw Squares for MSE
            ctx.fillStyle = 'rgba(239, 68, 68, 0.15)';
            ctx.strokeStyle = 'rgba(239, 68, 68, 0.4)';
            ctx.lineWidth = 1;
            let side = p.y < pred_canvas_y ? error : -error;
            ctx.fillRect(p.x, p.y, -side, side);
            ctx.strokeRect(p.x, p.y, -side, side);
        } else {
            // Draw Bars for MAE
            ctx.strokeStyle = '#ef4444';
            ctx.lineWidth = 2;
            ctx.setLineDash([4, 2]);
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p.x, pred_canvas_y);
            ctx.stroke();
            ctx.setLineDash([]);
        }
    });

    // Prediction Line
    ctx.strokeStyle = '#6366f1';
    ctx.lineWidth = 4;
    ctx.shadowColor = 'rgba(99, 102, 241, 0.5)';
    ctx.shadowBlur = 15;
    
    const x1 = -width/2;
    const y1 = x1 * w + b;
    const x2 = width/2;
    const y2 = x2 * w + b;
    
    ctx.beginPath();
    ctx.moveTo(0, height/2 - y1);
    ctx.lineTo(width, height/2 - y2);
    ctx.stroke();
    ctx.shadowBlur = 0;

    // Points
    points.forEach(p => {
        ctx.fillStyle = '#fff';
        ctx.beginPath();
        ctx.arc(p.x, p.y, 6, 0, Math.PI*2);
        ctx.fill();
        ctx.strokeStyle = '#6366f1';
        ctx.lineWidth = 2;
        ctx.stroke();
    });
}

btnMse.onclick = () => {
    lossType = 'MSE';
    btnMse.classList.add('active');
    btnMae.classList.remove('active');
    modeDesc.innerText = "MSE squares the errors, making big misses hurt way more than small ones!";
};

btnMae.onclick = () => {
    lossType = 'MAE';
    btnMae.classList.add('active');
    btnMse.classList.remove('active');
    modeDesc.innerText = "MAE takes the absolute distance. It's more 'fair' to outliers but harder to do calculus on.";
};

init();
</script>
</body>
</html>
"""
    components.html(html_code, height=550, scrolling=False)

def main():
    st.title("🥊 Page 50: What is a Loss Function?")
    
    st.markdown(
        """
        Welcome to the **Penalty Box**! In AI, a model's job is to make predictions. But models aren't perfect—they make mistakes.
        
        The **Loss Function** is a mathematical way of saying: *"How bad did I mess up?"*
        It takes all the mistakes, crushes them down into a **single number**, and handed it to us as a score. Lower is better!
        """
    )
    
    st.divider()
    
    render_lab()
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📏 Mean Absolute Error (MAE)")
        st.latex(r"L = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|")
        st.markdown(
            """
            **The Intuition:** Just measure the distance from the point to the line. 
            If you're off by 5 units, the "penalty" is 5.
            
            - **Pros:** Easy to explain, robust to outliers.
            - **Cons:** The "V-shape" (absolute value) is hard to use with calculus because the tip isn't smooth.
            """
        )
        
    with col2:
        st.markdown("### ⬛ Mean Squared Error (MSE)")
        st.latex(r"L = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2")
        st.markdown(
            """
            **The Intuition:** Imagine drawing a **literal square** for every error. The total Loss is the total area of those squares.
            
            - **Pros:** Huge penalties for big misses! Calculus loves squares ($x^2 \\to 2x$ is smooth).
            - **Cons:** One single "outlier" (a very wrong point) can explode the loss.
            """
        )
        
    st.divider()
    st.markdown("### 🕵️ Why 'Squared'?")
    st.info(
        """
        In the lab above, switch to **MSE** and move a single point far away. Watch the "Loss Meter" skyrocket! 
        Because we square the error, being off by **10** costs you **100**, while being off by **2** only costs **4**. 
        
        This forces the AI to prioritize fixing the "biggest" mistakes first. It also turns our "Loss Landscape" into a smooth bowl, which makes finding the bottom much easier—as we'll see in the next few pages!
        """
    )

    st.markdown(
        '<div style="color:#94a3b8;font-size:0.95rem;">Page 50 — you now understand how we quantify failure. Next: we turn these failure scores into a 3D landscape of Hills and Valleys!</div>',
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
