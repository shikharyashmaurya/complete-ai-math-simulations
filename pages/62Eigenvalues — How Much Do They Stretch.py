import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Eigenvalues — How Much Do They Stretch?", layout="wide")


def render_stretch_lab():
    html_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Inter',sans-serif;background:#0f172a;color:#f8fafc;padding:10px;overflow-x:hidden;}
.outer{max-width:1200px;margin:0 auto;display:flex;flex-direction:column;gap:16px;}
.title-card{background:rgba(30,41,59,0.5);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:16px 24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;}
.title-card h2{font-size:22px;font-weight:800;background:linear-gradient(135deg,#38bdf8,#a78bfa,#f472b6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.mode-toggle{display:flex;gap:6px;background:rgba(0,0,0,0.25);padding:4px;border-radius:10px;border:1px solid rgba(255,255,255,0.05);}
.tbtn{background:transparent;color:#94a3b8;border:none;padding:8px 14px;font-size:12px;font-weight:700;border-radius:8px;cursor:pointer;transition:.2s;}
.tbtn.active{background:#1e293b;color:#38bdf8;box-shadow:0 2px 10px rgba(0,0,0,0.3);border:1px solid rgba(56,189,248,0.2);}
.main-grid{display:grid;grid-template-columns:1fr 1.25fr;gap:20px;}
@media(max-width:900px){.main-grid{grid-template-columns:1fr;}}
.panel{background:rgba(30,41,59,0.35);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:20px;display:flex;flex-direction:column;gap:14px;}
.lbl{font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:1.5px;color:#94a3b8;margin-bottom:4px;}
.preset-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;}
.pbtn{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:#cbd5e1;padding:10px 6px;border-radius:10px;font-size:11px;font-weight:700;cursor:pointer;text-align:center;transition:.2s;line-height:1.3;}
.pbtn:hover{background:rgba(255,255,255,0.08);}
.pbtn.active{box-shadow:0 0 12px rgba(56,189,248,0.25);}
.pbtn[data-cat="grow"].active{background:rgba(34,197,94,0.15);border-color:#22c55e;color:#4ade80;}
.pbtn[data-cat="same"].active{background:rgba(56,189,248,0.15);border-color:#38bdf8;color:#7dd3fc;}
.pbtn[data-cat="shrink"].active{background:rgba(167,139,250,0.15);border-color:#a78bfa;color:#c4b5fd;}
.pbtn[data-cat="flip"].active{background:rgba(244,63,94,0.15);border-color:#f43f5e;color:#fb7185;}
.pbtn[data-cat="zero"].active{background:rgba(100,116,139,0.2);border-color:#64748b;color:#94a3b8;}
.lambda-sliders{display:flex;flex-direction:column;gap:12px;background:rgba(0,0,0,0.15);padding:14px;border-radius:12px;border:1px solid rgba(255,255,255,0.04);}
.srow{display:flex;justify-content:space-between;font-size:12px;font-weight:700;color:#94a3b8;margin-bottom:4px;}
.srow .val{font-family:monospace;font-weight:900;font-size:15px;}
input[type=range]{width:100%;height:5px;background:rgba(255,255,255,0.1);border-radius:3px;outline:none;-webkit-appearance:none;}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;cursor:pointer;}
#sl-l1::-webkit-slider-thumb{background:#4ade80;box-shadow:0 0 8px #4ade80;}
#sl-l2::-webkit-slider-thumb{background:#c4b5fd;box-shadow:0 0 8px #c4b5fd;}
#sl-lambda::-webkit-slider-thumb{background:#38bdf8;box-shadow:0 0 8px #38bdf8;}
.badge-row{display:flex;gap:8px;flex-wrap:wrap;}
.badge{padding:6px 12px;border-radius:20px;font-size:11px;font-weight:800;letter-spacing:0.5px;border:1px solid transparent;transition:.3s;opacity:0.35;}
.badge.on{opacity:1;transform:scale(1.05);}
.badge.grow{background:rgba(34,197,94,0.15);border-color:#22c55e;color:#4ade80;}
.badge.shrink{background:rgba(167,139,250,0.15);border-color:#a78bfa;color:#c4b5fd;}
.badge.flip{background:rgba(244,63,94,0.15);border-color:#f43f5e;color:#fb7185;}
.badge.same{background:rgba(56,189,248,0.15);border-color:#38bdf8;color:#7dd3fc;}
.stretch-meter{background:rgba(0,0,0,0.25);border-radius:12px;padding:14px;border:1px solid rgba(255,255,255,0.05);}
.meter-track{position:relative;height:28px;background:linear-gradient(90deg,#f43f5e 0%,#64748b 35%,#38bdf8 50%,#22c55e 100%);border-radius:14px;margin:10px 0 6px;overflow:visible;}
.meter-needle{position:absolute;top:-6px;width:4px;height:40px;background:#fff;border-radius:2px;box-shadow:0 0 12px #fff;transform:translateX(-50%);transition:left .15s ease;}
.meter-labels{display:flex;justify-content:space-between;font-size:10px;font-weight:700;color:#64748b;}
.ratio-box{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
.ratio-card{background:rgba(0,0,0,0.2);border-radius:10px;padding:12px;text-align:center;border:1px solid rgba(255,255,255,0.04);}
.ratio-title{font-size:10px;font-weight:800;text-transform:uppercase;color:#64748b;letter-spacing:1px;}
.ratio-val{font-size:22px;font-weight:900;font-family:monospace;margin-top:4px;}
.ratio-sub{font-size:11px;color:#94a3b8;margin-top:2px;}
.math-eq{background:rgba(0,0,0,0.25);border-radius:12px;padding:14px;text-align:center;font-size:17px;font-weight:700;font-family:monospace;}
.math-eq .lam{color:#38bdf8;font-weight:900;font-size:22px;}
.math-eq .v{color:#fbbf24;}
.math-eq .av{color:#f472b6;}
.action-btn{width:100%;background:rgba(56,189,248,0.12);color:#38bdf8;border:1px solid rgba(56,189,248,0.35);padding:11px;border-radius:12px;font-weight:800;font-size:13px;cursor:pointer;transition:.2s;}
.action-btn:hover{background:rgba(56,189,248,0.22);}
.action-btn.active{background:rgba(244,63,94,0.12);color:#f43f5e;border-color:rgba(244,63,94,0.4);}
.canvas-wrap{position:relative;display:flex;flex-direction:column;gap:10px;}
.status-banner{width:100%;text-align:center;padding:10px;border-radius:10px;font-weight:800;font-size:13px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.05);color:#94a3b8;transition:.2s;}
.status-banner.highlight{background:rgba(56,189,248,0.12);border-color:#38bdf8;color:#7dd3fc;}
canvas{background:#090d16;border:2px solid rgba(255,255,255,0.08);border-radius:16px;display:block;width:100%;max-width:100%;box-shadow:0 8px 32px rgba(0,0,0,0.3);}
.legend{display:flex;gap:14px;flex-wrap:wrap;justify-content:center;font-size:11px;background:rgba(0,0,0,0.15);padding:8px 14px;border-radius:20px;border:1px solid rgba(255,255,255,0.04);}
.leg-item{display:flex;align-items:center;gap:6px;}
.leg-dot{width:12px;height:3px;border-radius:2px;}
.mini-canvas-row{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
.mini-label{font-size:10px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:4px;text-align:center;}
</style>
</head>
<body>
<div class="outer">
  <div class="title-card">
    <h2>📏 EIGENVALUE STRETCH LAB</h2>
    <div class="mode-toggle">
      <button class="tbtn active" id="mode-1d" onclick="setMode('1d')">1D λ Slider</button>
      <button class="tbtn" id="mode-2d" onclick="setMode('2d')">2D Matrix View</button>
    </div>
  </div>

  <div class="main-grid">
    <div class="panel">
      <div id="ctrl-1d">
        <div class="lbl">λ Presets — What happens to v?</div>
        <div class="preset-grid" id="presets-1d">
          <button class="pbtn" data-cat="grow" onclick="setLambda1d(2.0,this)">λ = 2<br><small>Grows 2×</small></button>
          <button class="pbtn active" data-cat="same" onclick="setLambda1d(1.0,this)">λ = 1<br><small>Unchanged</small></button>
          <button class="pbtn" data-cat="shrink" onclick="setLambda1d(0.4,this)">λ = 0.4<br><small>Shrinks</small></button>
          <button class="pbtn" data-cat="flip" onclick="setLambda1d(-1.0,this)">λ = −1<br><small>Flips!</small></button>
          <button class="pbtn" data-cat="flip" onclick="setLambda1d(-1.8,this)">λ = −1.8<br><small>Flip + Grow</small></button>
          <button class="pbtn" data-cat="zero" onclick="setLambda1d(0.0,this)">λ = 0<br><small>Collapse</small></button>
        </div>
        <div class="lambda-sliders">
          <div class="srow"><span>λ (eigenvalue)</span><span class="val" id="val-lambda" style="color:#38bdf8">1.00</span></div>
          <input type="range" id="sl-lambda" min="-2.5" max="2.5" step="0.05" value="1.0" oninput="onLambdaSlider()">
        </div>
      </div>

      <div id="ctrl-2d" style="display:none">
        <div class="lbl">Matrix Presets (diagonal stretch)</div>
        <div class="preset-grid" id="presets-2d">
          <button class="pbtn active" data-cat="grow" onclick="setMatrix2d(2,1.2,this)">Big + Small<br>λ₁=2, λ₂=1.2</button>
          <button class="pbtn" data-cat="shrink" onclick="setMatrix2d(0.5,0.3,this)">Both Shrink<br>λ₁=0.5, λ₂=0.3</button>
          <button class="pbtn" data-cat="flip" onclick="setMatrix2d(-1.5,0.8,this)">Flip X<br>λ₁=−1.5</button>
          <button class="pbtn" data-cat="flip" onclick="setMatrix2d(1.2,-1.2,this)">Flip Y<br>λ₂=−1.2</button>
          <button class="pbtn" data-cat="grow" onclick="setMatrix2d(2.5,2.5,this)">Uniform Grow<br>λ=2.5</button>
          <button class="pbtn" data-cat="zero" onclick="setMatrix2d(0,1,this)">Collapse X<br>λ₁=0</button>
        </div>
        <div class="lambda-sliders">
          <div class="srow"><span style="color:#4ade80">λ₁ (horizontal axis)</span><span class="val" id="val-l1" style="color:#4ade80">2.00</span></div>
          <input type="range" id="sl-l1" min="-2.5" max="2.5" step="0.05" value="2.0" oninput="onMatrixSlider()">
          <div class="srow"><span style="color:#c4b5fd">λ₂ (vertical axis)</span><span class="val" id="val-l2" style="color:#c4b5fd">1.20</span></div>
          <input type="range" id="sl-l2" min="-2.5" max="2.5" step="0.05" value="1.2" oninput="onMatrixSlider()">
        </div>
      </div>

      <div class="badge-row">
        <span class="badge grow" id="bd-grow">λ &gt; 1 GROWS</span>
        <span class="badge same" id="bd-same">λ = 1 SAME</span>
        <span class="badge shrink" id="bd-shrink">0 &lt; λ &lt; 1 SHRINKS</span>
        <span class="badge flip" id="bd-flip">λ &lt; 0 FLIPS</span>
      </div>

      <div class="stretch-meter">
        <div class="lbl" style="margin-bottom:0">Stretch-O-Meter (|λ|)</div>
        <div class="meter-track">
          <div class="meter-needle" id="needle" style="left:50%"></div>
        </div>
        <div class="meter-labels"><span>0</span><span>0.5</span><span>1</span><span>1.5</span><span>2+</span></div>
      </div>

      <div class="ratio-box">
        <div class="ratio-card">
          <div class="ratio-title">‖v‖ (before)</div>
          <div class="ratio-val" id="len-before" style="color:#fbbf24">1.00</div>
          <div class="ratio-sub">input length</div>
        </div>
        <div class="ratio-card">
          <div class="ratio-title">‖Av‖ (after)</div>
          <div class="ratio-val" id="len-after" style="color:#f472b6">1.00</div>
          <div class="ratio-sub" id="ratio-text">ratio = 1.00</div>
        </div>
      </div>

      <div class="math-eq" id="eq-display">
        <span class="av">Av</span> = <span class="lam" id="eq-lam">1.00</span><span class="v">v</span>
      </div>

      <button class="action-btn" id="pulse-btn" onclick="togglePulse()">▶ PULSE λ (watch it breathe)</button>
    </div>

    <div class="canvas-wrap">
      <div class="status-banner" id="status">Drag the yellow arrow — when aligned with an eigen-direction, ‖Av‖/‖v‖ = |λ|</div>
      <canvas id="cvs" width="580" height="480"></canvas>
      <div class="mini-canvas-row" id="mini-row" style="display:none">
        <div>
          <div class="mini-label" style="color:#4ade80">λ₁ axis stretch</div>
          <canvas id="cvs-mini1" width="260" height="100"></canvas>
        </div>
        <div>
          <div class="mini-label" style="color:#c4b5fd">λ₂ axis stretch</div>
          <canvas id="cvs-mini2" width="260" height="100"></canvas>
        </div>
      </div>
      <div class="legend">
        <div class="leg-item"><span class="leg-dot" style="background:#fbbf24"></span>v (input)</div>
        <div class="leg-item"><span class="leg-dot" style="background:#f472b6"></span>Av (output)</div>
        <div class="leg-item"><span class="leg-dot" style="border-top:2px dashed #4ade80;background:transparent;width:14px"></span>eigen-direction</div>
        <div class="leg-item"><span class="leg-dot" style="background:rgba(56,189,248,0.5)"></span>unit circle → ellipse</div>
      </div>
    </div>
  </div>
</div>

<script>
let mode = '1d';
let lambda1d = 1.0;
let l1 = 2.0, l2 = 1.2;
let vx = 1.4, vy = 0.9;
let pulseOn = false;
let pulseT = 0;
let particles = [];

const cvs = document.getElementById('cvs');
const ctx = cvs.getContext('2d');
const OX = cvs.width / 2, OY = cvs.height / 2, SCALE = 68;

function setMode(m) {
  mode = m;
  document.getElementById('mode-1d').classList.toggle('active', m === '1d');
  document.getElementById('mode-2d').classList.toggle('active', m === '2d');
  document.getElementById('ctrl-1d').style.display = m === '1d' ? 'block' : 'none';
  document.getElementById('ctrl-2d').style.display = m === '2d' ? 'flex' : 'none';
  document.getElementById('ctrl-2d').style.flexDirection = 'column';
  document.getElementById('ctrl-2d').style.gap = '14px';
  document.getElementById('mini-row').style.display = m === '2d' ? 'grid' : 'none';
  draw();
}

function setLambda1d(val, btn) {
  lambda1d = val;
  document.getElementById('sl-lambda').value = val;
  document.getElementById('val-lambda').textContent = val.toFixed(2);
  document.querySelectorAll('#presets-1d .pbtn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  updateBadges(lambda1d);
  draw();
}

function setMatrix2d(a, b, btn) {
  l1 = a; l2 = b;
  document.getElementById('sl-l1').value = a;
  document.getElementById('sl-l2').value = b;
  document.getElementById('val-l1').textContent = a.toFixed(2);
  document.getElementById('val-l2').textContent = b.toFixed(2);
  document.querySelectorAll('#presets-2d .pbtn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  draw();
}

function onLambdaSlider() {
  lambda1d = parseFloat(document.getElementById('sl-lambda').value);
  document.getElementById('val-lambda').textContent = lambda1d.toFixed(2);
  document.querySelectorAll('#presets-1d .pbtn').forEach(b => b.classList.remove('active'));
  updateBadges(lambda1d);
  draw();
}

function onMatrixSlider() {
  l1 = parseFloat(document.getElementById('sl-l1').value);
  l2 = parseFloat(document.getElementById('sl-l2').value);
  document.getElementById('val-l1').textContent = l1.toFixed(2);
  document.getElementById('val-l2').textContent = l2.toFixed(2);
  document.querySelectorAll('#presets-2d .pbtn').forEach(b => b.classList.remove('active'));
  draw();
}

function updateBadges(lam) {
  document.getElementById('bd-grow').classList.toggle('on', lam > 1.02);
  document.getElementById('bd-same').classList.toggle('on', Math.abs(lam - 1) < 0.02);
  document.getElementById('bd-shrink').classList.toggle('on', lam > 0.02 && lam < 0.98);
  document.getElementById('bd-flip').classList.toggle('on', lam < -0.02);
  const needle = document.getElementById('needle');
  const pct = Math.min(100, Math.max(0, (Math.abs(lam) / 2.5) * 100));
  needle.style.left = pct + '%';
}

function togglePulse() {
  pulseOn = !pulseOn;
  const btn = document.getElementById('pulse-btn');
  if (pulseOn) {
    btn.classList.add('active');
    btn.textContent = '⏸ STOP PULSE';
    animatePulse();
  } else {
    btn.classList.remove('active');
    btn.textContent = '▶ PULSE λ (watch it breathe)';
  }
}

function animatePulse() {
  if (!pulseOn) return;
  pulseT += 0.03;
  const wave = Math.sin(pulseT) * 1.8;
  if (mode === '1d') {
    const newL = wave;
    document.getElementById('sl-lambda').value = newL;
    onLambdaSlider();
  } else {
    document.getElementById('sl-l1').value = 1.5 + Math.sin(pulseT) * 1.2;
    document.getElementById('sl-l2').value = 1.0 + Math.cos(pulseT * 0.7) * 1.0;
    onMatrixSlider();
  }
  requestAnimationFrame(animatePulse);
}

function transform(x, y) {
  if (mode === '1d') {
    return { wx: lambda1d * x, wy: y };
  }
  return { wx: l1 * x, wy: l2 * y };
}

function getEigenInfo() {
  if (mode === '1d') {
    return [
      { vx: 1, vy: 0, lambda: lambda1d, color: '#4ade80' },
      { vx: 0, vy: 1, lambda: 1.0, color: '#64748b' }
    ];
  }
  return [
    { vx: 1, vy: 0, lambda: l1, color: '#4ade80' },
    { vx: 0, vy: 1, lambda: l2, color: '#c4b5fd' }
  ];
}

function classifyLambda(l) {
  if (l < -0.02) return { text: 'λ < 0 — direction FLIPS backward!', cls: 'flip' };
  if (l > 1.02) return { text: 'λ > 1 — vector GROWS along this axis', cls: 'grow' };
  if (l > 0.98 && l < 1.02) return { text: 'λ ≈ 1 — length stays the same', cls: 'same' };
  if (l > 0.02) return { text: '0 < λ < 1 — vector SHRINKS toward origin', cls: 'shrink' };
  if (Math.abs(l) < 0.02) return { text: 'λ ≈ 0 — collapsed to a point!', cls: 'zero' };
  return { text: '', cls: '' };
}

function drawArrow(x1, y1, x2, y2, color, thick, dashed) {
  const fx = OX + x1*SCALE, fy = OY - y1*SCALE;
  const tx = OX + x2*SCALE, ty = OY - y2*SCALE;
  const dx = tx-fx, dy = ty-fy, len = Math.sqrt(dx*dx+dy*dy);
  if (len < 4) return;
  ctx.save();
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  ctx.lineWidth = thick || 3;
  if (dashed) ctx.setLineDash([6,4]);
  ctx.beginPath();
  ctx.moveTo(fx, fy);
  ctx.lineTo(tx, ty);
  ctx.stroke();
  const ang = Math.atan2(dy, dx);
  const hl = 11;
  ctx.beginPath();
  ctx.moveTo(tx, ty);
  ctx.lineTo(tx - hl*Math.cos(ang-Math.PI/6), ty - hl*Math.sin(ang-Math.PI/6));
  ctx.lineTo(tx - hl*Math.cos(ang+Math.PI/6), ty - hl*Math.sin(ang+Math.PI/6));
  ctx.closePath();
  ctx.fill();
  ctx.restore();
}

function drawUnitCircleTransformed() {
  if (mode !== '2d') return;
  ctx.save();
  ctx.beginPath();
  const steps = 64;
  for (let i = 0; i <= steps; i++) {
    const t = (i/steps) * Math.PI * 2;
    const cx = Math.cos(t), cy = Math.sin(t);
    const px = OX + l1*cx*SCALE, py = OY - l2*cy*SCALE;
    if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
  }
  ctx.strokeStyle = 'rgba(56,189,248,0.35)';
  ctx.lineWidth = 2;
  ctx.setLineDash([]);
  ctx.stroke();
  ctx.setLineDash([4,4]);
  ctx.strokeStyle = 'rgba(255,255,255,0.12)';
  ctx.beginPath();
  for (let i = 0; i <= steps; i++) {
    const t = (i/steps) * Math.PI * 2;
    const px = OX + Math.cos(t)*SCALE, py = OY - Math.sin(t)*SCALE;
    if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
  }
  ctx.stroke();
  ctx.restore();
}

function drawMiniBars() {
  const c1 = document.getElementById('cvs-mini1');
  const c2 = document.getElementById('cvs-mini2');
  if (!c1) return;
  [ [c1, l1, '#4ade80', 'λ₁'], [c2, l2, '#c4b5fd', 'λ₂'] ].forEach(([cv, lam, col, label]) => {
    const cx = cv.getContext('2d');
    const w = cv.width, h = cv.height;
    cx.clearRect(0,0,w,h);
    cx.fillStyle = '#090d16';
    cx.fillRect(0,0,w,h);
    const mid = h/2;
    cx.fillStyle = 'rgba(255,255,255,0.08)';
    cx.fillRect(20, mid-8, w-40, 16);
    const barW = Math.min(w-60, Math.abs(lam)/2.5 * (w-60));
    const startX = lam >= 0 ? w/2 - 20 : w/2 - 20 - barW;
    cx.fillStyle = col;
    cx.fillRect(startX, mid-12, barW, 24);
    cx.fillStyle = '#94a3b8';
    cx.font = 'bold 11px Inter,sans-serif';
    cx.fillText(label + ' = ' + lam.toFixed(2), 8, 16);
    const cls = classifyLambda(lam);
    cx.fillStyle = lam < 0 ? '#fb7185' : lam > 1 ? '#4ade80' : lam < 1 ? '#c4b5fd' : '#7dd3fc';
    cx.fillText(cls.text.split('—')[0].trim(), 8, h-8);
  });
}

function spawnParticles(x, y, col) {
  for (let i = 0; i < 5; i++) {
    particles.push({ x, y, vx: (Math.random()-0.5)*3, vy: (Math.random()-0.5)*3, a: 1, col });
  }
}

function draw() {
  const { wx, wy } = transform(vx, vy);
  const lenV = Math.sqrt(vx*vx + vy*vy);
  const lenW = Math.sqrt(wx*wx + wy*wy);
  const ratio = lenV > 0.01 ? lenW / lenV : 0;

  ctx.clearRect(0, 0, cvs.width, cvs.height);

  ctx.strokeStyle = 'rgba(255,255,255,0.04)';
  ctx.lineWidth = 1;
  for (let i = -5; i <= 5; i++) {
    ctx.beginPath(); ctx.moveTo(OX+i*SCALE, 0); ctx.lineTo(OX+i*SCALE, cvs.height); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(0, OY-i*SCALE); ctx.lineTo(cvs.width, OY-i*SCALE); ctx.stroke();
  }
  ctx.strokeStyle = 'rgba(255,255,255,0.2)';
  ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(OX,0); ctx.lineTo(OX,cvs.height); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(0,OY); ctx.lineTo(cvs.width,OY); ctx.stroke();

  drawUnitCircleTransformed();

  const eigs = getEigenInfo();
  let alignedIdx = -1, alignedLam = null;
  const vAng = Math.atan2(vy, vx);

  for (let i = 0; i < eigs.length; i++) {
    const ev = eigs[i];
    let evAng = Math.atan2(ev.vy, ev.vx);
    let diff = Math.abs(vAng - evAng) % Math.PI;
    if (diff > Math.PI/2) diff = Math.PI - diff;
    const isAligned = diff < 0.08;
    if (isAligned) { alignedIdx = i; alignedLam = ev.lambda; }

    ctx.save();
    ctx.setLineDash([5,5]);
    ctx.strokeStyle = isAligned ? ev.color : 'rgba(255,255,255,0.15)';
    ctx.lineWidth = isAligned ? 2.5 : 1;
    ctx.beginPath();
    ctx.moveTo(OX - ev.vx*800, OY + ev.vy*800);
    ctx.lineTo(OX + ev.vx*800, OY - ev.vy*800);
    ctx.stroke();
    ctx.restore();

    const ghostLen = 2.2;
    const gx = ev.vx * ghostLen, gy = ev.vy * ghostLen;
    const sx = gx * ev.lambda, sy = gy * ev.lambda;
    ctx.globalAlpha = 0.25;
    drawArrow(0, 0, gx, gy, ev.color, 1.5, true);
    drawArrow(0, 0, sx, sy, ev.color, 2, false);
    ctx.globalAlpha = 1;

    ctx.fillStyle = ev.color;
    ctx.font = 'bold 11px Inter,sans-serif';
    ctx.fillText('λ'+(i+1)+'='+ev.lambda.toFixed(2), OX+ev.vx*2.5*SCALE+6, OY-ev.vy*2.5*SCALE-4);
  }

  drawArrow(0, 0, wx, wy, '#f472b6', 4, false);
  drawArrow(0, 0, vx, vy, '#fbbf24', 3.5, false);

  ctx.beginPath();
  ctx.arc(OX+vx*SCALE, OY-vy*SCALE, 7, 0, Math.PI*2);
  ctx.fillStyle = '#fff';
  ctx.strokeStyle = '#fbbf24';
  ctx.lineWidth = 2;
  ctx.fill();
  ctx.stroke();

  for (let p of particles) {
    p.x += p.vx; p.y += p.vy; p.a -= 0.04;
    if (p.a <= 0) continue;
    ctx.globalAlpha = p.a;
    ctx.fillStyle = p.col;
    ctx.beginPath();
    ctx.arc(p.x, p.y, 3, 0, Math.PI*2);
    ctx.fill();
  }
  particles = particles.filter(p => p.a > 0);
  ctx.globalAlpha = 1;

  if (alignedIdx >= 0) {
    spawnParticles(OX+vx*SCALE, OY-vy*SCALE, eigs[alignedIdx].color);
  }

  const displayLam = mode === '1d' ? lambda1d : (alignedLam !== null ? alignedLam : null);
  document.getElementById('len-before').textContent = lenV.toFixed(2);
  document.getElementById('len-after').textContent = lenW.toFixed(2);

  const status = document.getElementById('status');
  if (alignedIdx >= 0 && displayLam !== null) {
    const cls = classifyLambda(displayLam);
    status.className = 'status-banner highlight';
    status.textContent = '✓ On eigen-direction! ' + cls.text + '  ‖Av‖/‖v‖ = ' + Math.abs(displayLam).toFixed(2);
    document.getElementById('ratio-text').textContent = 'ratio ≈ |λ| = ' + Math.abs(displayLam).toFixed(2);
    updateBadges(displayLam);
    document.getElementById('eq-lam').textContent = displayLam.toFixed(2);
  } else {
    status.className = 'status-banner';
    status.textContent = mode === '1d'
      ? 'Drag v onto the horizontal (green) axis — λ stretches it; vertical axis stays λ = 1'
      : 'Align v with green (λ₁) or purple (λ₂) axis to see pure stretch';
    document.getElementById('ratio-text').textContent = 'ratio = ' + ratio.toFixed(2) + ' (mixed directions)';
    if (mode === '1d') updateBadges(lambda1d);
    else updateBadges((Math.abs(l1)+Math.abs(l2))/2);
    document.getElementById('eq-lam').textContent = mode === '1d' ? lambda1d.toFixed(2) : '?';
  }

  drawMiniBars();
}

function loop() {
  draw();
  requestAnimationFrame(loop);
}
loop();

let dragging = false;
cvs.addEventListener('mousedown', e => {
  const r = cvs.getBoundingClientRect();
  const mx = e.clientX - r.left, my = e.clientY - r.top;
  const px = OX + vx*SCALE, py = OY - vy*SCALE;
  if (Math.hypot(mx-px, my-py) < 22) dragging = true;
});
cvs.addEventListener('mousemove', e => {
  if (!dragging) return;
  const r = cvs.getBoundingClientRect();
  vx = (e.clientX - r.left - OX) / SCALE;
  vy = -(e.clientY - r.top - OY) / SCALE;
  const m = Math.hypot(vx, vy);
  if (m > 3.5) { vx = vx/m*3.5; vy = vy/m*3.5; }
  if (m < 0.15) { vx = 0.2; vy = 0; }
});
window.addEventListener('mouseup', () => dragging = false);

cvs.addEventListener('touchstart', e => {
  if (e.touches.length !== 1) return;
  const r = cvs.getBoundingClientRect();
  const mx = e.touches[0].clientX - r.left, my = e.touches[0].clientY - r.top;
  const px = OX + vx*SCALE, py = OY - vy*SCALE;
  if (Math.hypot(mx-px, my-py) < 28) { dragging = true; e.preventDefault(); }
});
cvs.addEventListener('touchmove', e => {
  if (!dragging || e.touches.length !== 1) return;
  const r = cvs.getBoundingClientRect();
  vx = (e.touches[0].clientX - r.left - OX) / SCALE;
  vy = -(e.touches[0].clientY - r.top - OY) / SCALE;
  const m = Math.hypot(vx, vy);
  if (m > 3.5) { vx = vx/m*3.5; vy = vy/m*3.5; }
  e.preventDefault();
});
cvs.addEventListener('touchend', () => dragging = false);

setMode('1d');
</script>
</body>
</html>
"""
    components.html(html_code, height=820, scrolling=False)


def main():
    st.title("📏 Page 62: Eigenvalues — How Much Do They Stretch?")

    st.markdown(
        """
        On the previous page you met **eigenvectors** — special directions that don't rotate when a matrix hits them.
        The companion number sitting next to each one is the **eigenvalue** $\\lambda$ (lambda).

        It answers one clean question: *along this direction, how much does the matrix stretch, squash, or flip the arrow?*

        $$\\mathbf{A}\\mathbf{v} = \\lambda \\mathbf{v}$$

        - $\\lambda > 1$ → the vector **grows**
        - $0 < \\lambda < 1$ → it **shrinks** toward the origin
        - $\\lambda = 1$ → same length, same direction
        - $\\lambda < 0$ → it **flips** to the opposite side *and* scales by $|\\lambda|$
        - $\\lambda = 0$ → the direction **collapses** to zero
        """
    )

    st.divider()
    render_stretch_lab()
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔢 Reading λ at a Glance")
        st.info("The eigenvalue is a **scalar stretch factor** along an eigenvector direction — nothing more mysterious than that.")
        st.markdown(
            r"""
| Condition | What happens to $\mathbf{v}$ | Real-world vibe |
|-----------|-------------------------------|-------------------|
| $\lambda > 1$ | Stretches outward | Amplifier 🔊 |
| $\lambda = 1$ | Unchanged | Identity pass-through |
| $0 < \lambda < 1$ | Shrinks inward | Dampener 🔇 |
| $\lambda < 0$ | Flips + scales by $\|\lambda\|$ | Mirror + zoom 🪞 |
| $\lambda = 0$ | Collapses to $\mathbf{0}$ | Information destroyed |

**Key ratio:** when $\mathbf{v}$ points along an eigenvector,
$$\frac{\|\mathbf{A}\mathbf{v}\|}{\|\mathbf{v}\|} = |\lambda|$$

The sign of $\lambda$ tells you whether the output points the same way ($+$) or backward ($-$).
"""
        )

    with col2:
        st.markdown("### 🧮 Computing λ for a 2×2 Matrix")
        st.success("Same characteristic equation from Page 61 — now we care about the roots $\\lambda_1, \\lambda_2$.")
        st.markdown(
            r"""
For $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}$:

$$\det(A - \lambda I) = 0 \implies \lambda^2 - (a+d)\lambda + (ad-bc) = 0$$

**Example — diagonal stretch matrix:**
$$A = \begin{bmatrix} 2 & 0 \\ 0 & 0.5 \end{bmatrix}$$

Eigenvalues: $\lambda_1 = 2$, $\lambda_2 = 0.5$ (read straight off the diagonal!)

- Horizontal arrows grow **2×**
- Vertical arrows shrink to **half**

Try **2D Matrix View** in the lab — drag $\lambda_1$ and $\lambda_2$ sliders and watch the unit circle become an axis-aligned ellipse whose width and height are exactly $|\lambda_1|$ and $|\lambda_2|$.
"""
        )

    st.divider()

    st.markdown("### 🎬 Three Scenarios to Try in the Lab")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 🟢 λ = 2 (Grow)")
        st.write("Set λ = 2 in **1D λ Slider** mode. Align the yellow arrow with the green eigen-direction. Notice ‖Av‖ is exactly **twice** ‖v‖.")
    with c2:
        st.markdown("#### 🟣 λ = 0.4 (Shrink)")
        st.write("Pick the shrink preset. The pink output arrow barely peeks out — the transformation is **squeezing** that direction.")
    with c3:
        st.markdown("#### 🔴 λ = −1.8 (Flip + Grow)")
        st.write("Negative λ sends Av to the **opposite side** of the origin while stretching it. This is how reflection matrices get eigenvalue −1.")

    st.divider()

    st.markdown("### 🤖 Bridge to AI: Why λ Sizes Matter")
    a1, a2, a3 = st.columns(3)
    with a1:
        st.markdown("#### 📉 PCA — Keep the Big λ Directions")
        st.write(
            "PCA ranks eigenvectors by their eigenvalues (variance). "
            "Large λ = lots of spread = worth keeping. "
            "Tiny λ directions are mostly noise — safe to drop for compression."
        )
    with a2:
        st.markdown("#### 🧠 Gradient Stability")
        st.write(
            "Stacking layers multiplies Jacobians. "
            "If weight matrices have eigenvalues > 1 everywhere, signals **explode**. "
            "If all λ < 1, they **vanish**. "
            "Good initialization keeps λ near 1."
        )
    with a3:
        st.markdown("#### 🕸️ PageRank's Dominant λ")
        st.write(
            "The web-surfer matrix has a largest eigenvalue λ₁ = 1. "
            "Its eigenvector is the steady-state visit distribution — "
            "the ranking score Google famously used."
        )

    st.divider()
    st.markdown(
        '<div style="text-align:center;color:#94a3b8;font-size:13px;">'
        "Page 62 — eigenvalues tell you *how much* each special direction stretches. "
        "Next Up: Page 63 — PCA Intuition: Finding the Best Angle ➔"
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
