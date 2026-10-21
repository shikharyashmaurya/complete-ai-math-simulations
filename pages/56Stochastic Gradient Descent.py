import streamlit as st
import streamlit.components.v1 as components
import numpy as np

st.set_page_config(page_title="Stochastic Gradient Descent", layout="wide")

def render_sgd_lab():
    html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:sans-serif;background:#0f172a;color:white;overflow:hidden;}
.lab-container{display:flex;flex-direction:column;height:100vh;padding:20px;gap:20px;}
.header{display:flex;justify-content:space-between;align-items:center;}
.title-group h2{font-size:24px;font-weight:900;color:#f8fafc;margin:0;}
.title-group p{font-size:14px;color:#94a3b8;}

.main-layout{display:flex;flex:1;gap:20px;min-height:0;}
.sidebar{flex:0.35;display:flex;flex-direction:column;gap:15px;overflow-y:auto;padding-right:10px;}
.canvas-area{flex:1;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:16px;position:relative;overflow:hidden;cursor:crosshair;}

.card{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:15px;}
.label-row{display:flex;justify-content:space-between;margin-bottom:8px;font-size:13px;font-weight:700;}
.val-pill{background:rgba(0,0,0,0.3);padding:2px 8px;border-radius:5px;font-family:monospace;color:#a78bfa;}

input[type=range]{width:100%;height:6px;background:rgba(255,255,255,0.1);border-radius:3px;outline:none;-webkit-appearance:none;margin:10px 0;}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;background:#a78bfa;border-radius:50%;cursor:pointer;box-shadow:0 0 10px rgba(167,139,250,0.5);}

.btn-group{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
button{background:rgba(255,255,255,0.05);color:white;border:1px solid rgba(255,255,255,0.1);padding:10px;border-radius:8px;font-weight:700;cursor:pointer;transition:0.2s;font-size:13px;}
button:hover{background:rgba(255,255,255,0.1);border-color:rgba(255,255,255,0.2);}
button.primary{background:#a78bfa;color:#0f172a;border:none;}
button.primary:hover{background:#c4b5fd;}

.legend{display:flex;gap:15px;margin-top:10px;}
.leg-item{display:flex;align-items:center;gap:6px;font-size:12px;font-weight:600;}
.dot{width:10px;height:10px;border-radius:50%;}

.stats-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
.stat-box{background:rgba(0,0,0,0.2);padding:10px;border-radius:8px;border:1px solid rgba(255,255,255,0.05);}
.stat-label{font-size:10px;text-transform:uppercase;letter-spacing:1px;color:#64748b;margin-bottom:4px;}
.stat-val{font-size:16px;font-weight:900;font-family:monospace;}

#overlay{position:absolute;top:20px;right:20px;pointer-events:none;text-align:right;}
.mini-batch-viz{display:flex;gap:4px;margin-top:5px;}
.batch-dot{width:6px;height:6px;border-radius:50%;background:rgba(255,255,255,0.1);}
.batch-dot.active{background:#fbbf24;box-shadow:0 0 5px #fbbf24;}

/* Custom styles for specific optimizers */
.color-batch { color: #38bdf8; } /* Light Blue */
.color-sgd { color: #fb7185; }   /* Rose/Pink */
.bg-batch { background: #38bdf8; }
.bg-sgd { background: #fb7185; }

</style>
</head>
<body>
<div class="lab-container">
    <div class="header">
        <div class="title-group">
            <h2>SGD Race Lab 🏁</h2>
            <p>Stochastic vs. Batch Gradient Descent</p>
        </div>
        <div class="legend">
            <div class="leg-item"><div class="dot bg-batch"></div><span class="color-batch">Full Batch (Smooth)</span></div>
            <div class="leg-item"><div class="dot bg-sgd"></div><span class="color-sgd">SGD / Mini-Batch (Noisy)</span></div>
        </div>
    </div>

    <div class="main-layout">
        <div class="sidebar">
            <div class="card">
                <div class="label-row"><span>Learning Rate (η)</span><span id="lr-val" class="val-pill">0.05</span></div>
                <input type="range" id="lr-slider" min="0.01" max="0.3" step="0.01" value="0.08">
                
                <div class="label-row"><span>Batch Size</span><span id="batch-val" class="val-pill">8</span></div>
                <input type="range" id="batch-slider" min="1" max="64" step="1" value="8">
                <p style="font-size:11px; color:#64748b; margin-top:-5px;">1 = Pure SGD, 64 = Full Batch</p>
            </div>

            <div class="card">
                <div class="label-row"><span>Momentum</span><span id="mom-val" class="val-pill">0.0</span></div>
                <input type="range" id="mom-slider" min="0" max="0.95" step="0.05" value="0.5">
            </div>

            <div class="btn-group">
                <button id="reset-btn">Reset</button>
                <button id="play-btn" class="primary">Play</button>
            </div>

            <div class="stats-grid">
                <div class="stat-box">
                    <div class="stat-label">Batch Loss</div>
                    <div id="loss-batch" class="stat-val color-batch">0.00</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">SGD Loss</div>
                    <div id="loss-sgd" class="stat-val color-sgd">0.00</div>
                </div>
            </div>

            <div class="card" style="background:rgba(251,191,36,0.05); border-color:rgba(251,191,36,0.2);">
                <div class="stat-label" style="color:#fbbf24;">Current Mini-Batch</div>
                <div class="mini-batch-viz" id="batch-dots"></div>
                <p style="font-size:11px; color:#d97706; margin-top:8px; line-height:1.4;">
                    In SGD, we only look at a <b>subset</b> of data. This creates "noise" that makes the path jumpy, but it's much faster to calculate!
                </p>
            </div>
        </div>

        <div class="canvas-area" id="canvas-container">
            <canvas id="main-canvas"></canvas>
            <div id="overlay">
                <div style="font-size:10px; color:#64748b; text-transform:uppercase;">Landscape</div>
                <div style="font-size:14px; font-weight:800;">Non-Convex Valley</div>
            </div>
        </div>
    </div>
</div>

<script>
const canvas = document.getElementById('main-canvas');
const ctx = canvas.getContext('2d');
const container = document.getElementById('canvas-container');

// State
let width, height;
let isPlaying = false;
let lr = 0.08;
let batchSize = 8;
let momentum = 0.5;

// Optimization paths
let pathBatch = [];
let pathSGD = [];
let posBatch = {x: 0, y: 0};
let posSGD = {x: 0, y: 0};
let velBatch = {x: 0, y: 0};
let velSGD = {x: 0, y: 0};

// Function: A slightly non-convex landscape with a global min
function getLoss(x, y) {
    return 0.1 * (x*x + y*y) + 0.5 * (Math.sin(2*x) + Math.cos(2*y));
}

function getGrad(x, y) {
    const dx = 0.2 * x + Math.cos(2*x) * 1.0;
    const dy = 0.2 * y - Math.sin(2*y) * 1.0;
    return {dx, dy};
}

let landscapeCanvas = null;

function drawLandscape() {
    if (!landscapeCanvas) {
        landscapeCanvas = document.createElement('canvas');
    }
    landscapeCanvas.width = width;
    landscapeCanvas.height = height;
    const lctx = landscapeCanvas.getContext('2d');
    
    const step = 4;
    for(let x=0; x<width; x+=step) {
        for(let y=0; y<height; y+=step) {
            const world = screenToWorld(x, y);
            const loss = getLoss(world.wx, world.wy);
            // Color based on loss: deep blue to light blue
            const t = (loss + 1.5) / 5; // normalize
            const r = Math.floor(15 + t * 40);
            const g = Math.floor(23 + t * 60);
            const b = Math.floor(42 + t * 100);
            lctx.fillStyle = `rgb(${r},${g},${b})`;
            lctx.fillRect(x, y, step, step);
        }
    }
}

function resize() {
    width = container.clientWidth;
    height = container.clientHeight;
    canvas.width = width;
    canvas.height = height;
    landscapeCanvas = null; // force redraw
    drawLandscape();
}

function worldToScreen(wx, wy) {
    const scale = Math.min(width, height) / 10;
    return {
        x: width/2 + wx * scale,
        y: height/2 + wy * scale
    };
}

function screenToWorld(sx, sy) {
    const scale = Math.min(width, height) / 10;
    return {
        wx: (sx - width/2) / scale,
        wy: (sy - height/2) / scale
    };
}

function reset(wx = -4, wy = -4) {
    posBatch = {x: wx, y: wy};
    posSGD = {x: wx, y: wy};
    velBatch = {x: 0, y: 0};
    velSGD = {x: 0, y: 0};
    pathBatch = [{...posBatch}];
    pathSGD = [{...posSGD}];
    updateStats();
}

function step() {
    // 1. Batch Update (Perfect Gradient)
    const gB = getGrad(posBatch.x, posBatch.y);
    velBatch.x = momentum * velBatch.x - lr * gB.dx;
    velBatch.y = momentum * velBatch.y - lr * gB.dy;
    posBatch.x += velBatch.x;
    posBatch.y += velBatch.y;
    pathBatch.push({...posBatch});

    // 2. SGD Update (Noisy Gradient)
    const gReal = getGrad(posSGD.x, posSGD.y);
    // Noise level inversely proportional to sqrt(batchSize)
    const noiseLevel = 1.8 * (1 - (batchSize - 1) / 63); 
    const noiseX = (Math.random() - 0.5) * noiseLevel;
    const noiseY = (Math.random() - 0.5) * noiseLevel;
    
    const gS = {
        dx: gReal.dx + noiseX,
        dy: gReal.dy + noiseY
    };
    
    velSGD.x = momentum * velSGD.x - lr * gS.dx;
    velSGD.y = momentum * velSGD.y - lr * gS.dy;
    posSGD.x += velSGD.x;
    posSGD.y += velSGD.y;
    pathSGD.push({...posSGD});

    if(pathBatch.length > 500) {
        pathBatch.shift();
        pathSGD.shift();
    }
    
    updateStats();
    updateBatchDots();
}

function updateStats() {
    const lB = getLoss(posBatch.x, posBatch.y);
    const lS = getLoss(posSGD.x, posSGD.y);
    document.getElementById('loss-batch').innerText = lB.toFixed(3);
    document.getElementById('loss-sgd').innerText = lS.toFixed(3);
}

function updateBatchDots() {
    const container = document.getElementById('batch-dots');
    container.innerHTML = '';
    const total = 16;
    const activeCount = Math.max(1, Math.floor((batchSize/64) * total));
    for(let i=0; i<total; i++) {
        const dot = document.createElement('div');
        dot.className = 'batch-dot' + (i < activeCount ? ' active' : '');
        container.appendChild(dot);
    }
}

function draw() {
    // 1. Draw cached landscape
    if (landscapeCanvas) {
        ctx.drawImage(landscapeCanvas, 0, 0);
    } else {
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(0,0,width,height);
    }
    
    // Draw simple circles for "valleys"
    const center = worldToScreen(0,0);
    // Just a visual hint of the center/minimum
    ctx.beginPath();
    ctx.arc(center.x, center.y, 5, 0, Math.PI*2);
    ctx.fillStyle = 'rgba(255,255,255,0.1)';
    ctx.fill();

    // Draw Paths
    drawPath(pathBatch, '#38bdf8', 2);
    drawPath(pathSGD, '#fb7185', 2);

    // Draw Heads
    const pB = worldToScreen(posBatch.x, posBatch.y);
    ctx.beginPath();
    ctx.arc(pB.x, pB.y, 6, 0, Math.PI*2);
    ctx.fillStyle = '#38bdf8';
    ctx.shadowBlur = 10; ctx.shadowColor = '#38bdf8';
    ctx.fill();
    ctx.shadowBlur = 0;

    const pS = worldToScreen(posSGD.x, posSGD.y);
    ctx.beginPath();
    ctx.arc(pS.x, pS.y, 6, 0, Math.PI*2);
    ctx.fillStyle = '#fb7185';
    ctx.shadowBlur = 10; ctx.shadowColor = '#fb7185';
    ctx.fill();
    ctx.shadowBlur = 0;

    if(isPlaying) {
        step();
    }
    requestAnimationFrame(draw);
}

function drawPath(path, color, width) {
    if(path.length < 2) return;
    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';
    
    const start = worldToScreen(path[0].x, path[0].y);
    ctx.moveTo(start.x, start.y);
    for(let i=1; i<path.length; i++) {
        const p = worldToScreen(path[i].x, path[i].y);
        ctx.lineTo(p.x, p.y);
    }
    ctx.stroke();
    
    // Fade out tail
    ctx.globalAlpha = 0.3;
    ctx.stroke();
    ctx.globalAlpha = 1.0;
}

// Controls
document.getElementById('lr-slider').oninput = (e) => {
    lr = parseFloat(e.target.value);
    document.getElementById('lr-val').innerText = lr.toFixed(2);
};
document.getElementById('batch-slider').oninput = (e) => {
    batchSize = parseInt(e.target.value);
    document.getElementById('batch-val').innerText = batchSize;
};
document.getElementById('mom-slider').oninput = (e) => {
    momentum = parseFloat(e.target.value);
    document.getElementById('mom-val').innerText = momentum.toFixed(2);
};

document.getElementById('play-btn').onclick = (e) => {
    isPlaying = !isPlaying;
    e.target.innerText = isPlaying ? 'Pause' : 'Play';
    e.target.classList.toggle('primary', !isPlaying);
};

document.getElementById('reset-btn').onclick = () => {
    reset(-4, -4);
};

canvas.onclick = (e) => {
    const rect = canvas.getBoundingClientRect();
    const world = screenToWorld(e.clientX - rect.left, e.clientY - rect.top);
    reset(world.wx, world.wy);
};

// Init
window.addEventListener('resize', resize);
resize();
reset(-4, -4);
draw();

</script>
</body>
</html>
"""
    components.html(html_code, height=700, scrolling=False)

def main():
    st.title("🏃 Page 56: Stochastic Gradient Descent")
    
    st.markdown("""
    In the previous pages, we calculated the **exact gradient** using every single data point. In the real world, AI models are trained on **billions of images or words**. 
    Calculating the gradient for everything at once (Full Batch) is too slow and takes too much memory.
    
    Enter **Stochastic Gradient Descent (SGD)**: The "Drunken Walker" that saves the day.
    """)
    
    st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("The Concept")
        st.write("""
        Instead of looking at the whole mountain, we pick a **random small group** (a "Mini-batch") and ask them which way is down.
        
        - **Full Batch**: Perfectly smooth, direct path. But very "heavy".
        - **SGD**: Noisy and jumpy. But very "light" and fast.
        
        **Why the noise is good:** That jumpiness helps the ball "bounce" out of small, shallow local minima that might trap a perfectly smooth optimizer!
        """)
        
    with col2:
        st.subheader("The Math 🧮")
        st.latex(r"w_{t+1} = w_t - \eta \cdot \nabla L_{batch}(w_t)")
        st.caption("Standard GD uses the gradient of the entire dataset.")
        
        st.latex(r"w_{t+1} = w_t - \eta \cdot \nabla L_{subset}(w_t)")
        st.caption("SGD uses the gradient of a random subset (Mini-batch).")

    st.divider()
    
    st.markdown("### 🧪 The SGD Race Laboratory")
    st.info("💡 **Click anywhere on the map** to teleport both optimizers to a new starting point!")
    
    render_sgd_lab()
    
    st.divider()
    
    # Key takeaways
    st_cols = st.columns(3)
    with st_cols[0]:
        st.error("🚀 **Speed**")
        st.write("SGD processes data in small chunks, meaning the model starts learning almost immediately without waiting for the whole dataset.")
    with st_cols[1]:
        st.warning("🎲 **Noise**")
        st.write("The noise acting like a 'shake' that helps escape poor local minima. It's a feature, not a bug!")
    with st_cols[2]:
        st.success("⚖️ **Mini-Batch**")
        st.write("Most AI uses a middle ground (size 32, 64, or 128) to get the best of both worlds: stability and speed.")

    st.divider()
    st.markdown(
        '<div style="color:#94a3b8;font-size:0.95rem;">Page 56 — you\'ve seen why "shaking" the optimizer with noise actually helps find better solutions. Next: we leave the valley and enter the world of Information!</div>',
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
