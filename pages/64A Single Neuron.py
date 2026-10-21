import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="A Single Neuron", layout="wide")


def render_neuron_lab():
    html_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:sans-serif;background:#0f172a;color:#f8fafc;padding:10px;overflow-x:hidden;}
.outer{max-width:1240px;margin:0 auto;display:flex;flex-direction:column;gap:16px;}
.title-card{background:rgba(30,41,59,0.55);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:16px 22px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;}
.title-card h2{font-size:22px;font-weight:900;background:linear-gradient(135deg,#fbbf24,#f472b6,#38bdf8);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.mode-toggle{display:flex;gap:6px;background:rgba(0,0,0,0.25);padding:4px;border-radius:10px;border:1px solid rgba(255,255,255,0.05);flex-wrap:wrap;}
.mbtn{background:transparent;color:#94a3b8;border:none;padding:8px 12px;font-size:11px;font-weight:700;border-radius:8px;cursor:pointer;transition:.2s;}
.mbtn:hover{color:#e2e8f0;}
.mbtn.active{background:#1e293b;color:#fbbf24;box-shadow:0 2px 10px rgba(0,0,0,0.3);border:1px solid rgba(251,191,36,0.3);}
.mbtn[data-m="math"].active{color:#38bdf8;border-color:rgba(56,189,248,0.3);}
.mbtn[data-m="contrib"].active{color:#34d399;border-color:rgba(52,211,153,0.3);}
.main-grid{display:grid;grid-template-columns:1fr 1.45fr;gap:20px;}
@media(max-width:920px){.main-grid{grid-template-columns:1fr;}}
.panel{background:rgba(30,41,59,0.35);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:18px;display:flex;flex-direction:column;gap:14px;}
.lbl{font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:1.5px;color:#94a3b8;margin-bottom:6px;}
.preset-grid{display:grid;grid-template-columns:1fr;gap:8px;}
.pbtn{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:#cbd5e1;padding:12px 14px;border-radius:12px;font-size:12px;font-weight:700;cursor:pointer;text-align:left;transition:.2s;line-height:1.4;}
.pbtn:hover{background:rgba(255,255,255,0.08);}
.pbtn.active{background:rgba(251,191,36,0.1);border-color:#fbbf24;color:#fde68a;box-shadow:0 0 16px rgba(251,191,36,0.15);}
.pbtn small{display:block;font-weight:600;color:#64748b;margin-top:3px;font-size:10px;}
.pbtn.active small{color:#a8a29e;}
.slider-box{background:rgba(0,0,0,0.2);border-radius:12px;padding:12px 14px;border:1px solid rgba(255,255,255,0.04);margin-bottom:8px;}
.srow{display:flex;justify-content:space-between;font-size:11px;font-weight:700;color:#94a3b8;margin-bottom:5px;}
.srow .val{font-family:monospace;font-weight:900;font-size:15px;}
input[type=range]{width:100%;height:6px;background:rgba(255,255,255,0.1);border-radius:3px;outline:none;-webkit-appearance:none;}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;cursor:pointer;}
.in-sl::-webkit-slider-thumb{background:#4ade80;box-shadow:0 0 8px #4ade80;}
.w-sl::-webkit-slider-thumb{background:#fbbf24;box-shadow:0 0 8px #fbbf24;}
.b-sl::-webkit-slider-thumb{background:#f472b6;box-shadow:0 0 8px #f472b6;}
.act-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;}
.abtn{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:#cbd5e1;padding:9px 6px;border-radius:10px;font-size:11px;font-weight:800;cursor:pointer;transition:.2s;}
.abtn:hover{background:rgba(255,255,255,0.08);}
.abtn.active{background:rgba(56,189,248,0.12);border-color:#38bdf8;color:#7dd3fc;}
.pipeline{background:rgba(0,0,0,0.28);border-radius:12px;padding:14px;border:1px solid rgba(255,255,255,0.05);font-family:monospace;font-size:12px;line-height:1.7;}
.pipe-step{padding:6px 0;border-bottom:1px dashed rgba(255,255,255,0.06);}
.pipe-step:last-child{border:none;}
.pipe-step.dim{color:#64748b;}
.pipe-step.hot{color:#fde68a;font-weight:800;}
.pipe-step.out{color:#34d399;font-weight:900;font-size:14px;}
.metric-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
.metric{background:rgba(0,0,0,0.22);border-radius:12px;padding:12px;text-align:center;border:1px solid rgba(255,255,255,0.04);}
.metric.full{grid-column:1/-1;}
.metric .mt{font-size:10px;font-weight:800;text-transform:uppercase;color:#64748b;letter-spacing:1px;}
.metric .mv{font-size:22px;font-weight:900;font-family:monospace;margin-top:4px;}
.metric .ms{font-size:10px;color:#94a3b8;margin-top:2px;}
.fire-btn{width:100%;background:linear-gradient(135deg,rgba(251,191,36,0.2),rgba(244,114,182,0.2));color:#fde68a;border:1px solid rgba(251,191,36,0.4);padding:13px;border-radius:12px;font-weight:900;font-size:14px;cursor:pointer;transition:.2s;letter-spacing:0.5px;}
.fire-btn:hover{transform:translateY(-1px);box-shadow:0 6px 20px rgba(251,191,36,0.2);}
.fire-btn.on{background:rgba(244,114,182,0.15);color:#fbcfe8;border-color:rgba(244,114,182,0.5);}
.canvas-col{display:flex;flex-direction:column;gap:10px;}
.status-banner{text-align:center;padding:10px 14px;border-radius:10px;font-weight:700;font-size:13px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.05);color:#94a3b8;line-height:1.45;transition:.25s;}
.status-banner.fire{background:rgba(251,191,36,0.1);border-color:rgba(251,191,36,0.35);color:#fde68a;}
canvas{background:#090d16;border:2px solid rgba(255,255,255,0.08);border-radius:16px;display:block;width:100%;box-shadow:0 8px 32px rgba(0,0,0,0.35);}
.mini-row{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
.mini-lbl{font-size:10px;font-weight:700;text-transform:uppercase;color:#64748b;margin-bottom:4px;text-align:center;}
.legend{display:flex;gap:14px;flex-wrap:wrap;justify-content:center;font-size:11px;padding:8px 12px;border-radius:20px;background:rgba(0,0,0,0.15);border:1px solid rgba(255,255,255,0.04);}
.leg{display:flex;align-items:center;gap:6px;}
.leg-dot{width:10px;height:10px;border-radius:50%;}
</style>
</head>
<body>
<div class="outer">
  <div class="title-card" style="display:flex">
    <h2>🧠 ONE NEURON — The Smallest Decision Maker</h2>
    <div class="mode-toggle" id="mode-btns">
      <button class="mbtn active" data-m="flow" onclick="setMode('flow')">⚡ Signal Flow</button>
      <button class="mbtn" data-m="math" onclick="setMode('math')">🔢 Dot Product</button>
      <button class="mbtn" data-m="contrib" onclick="setMode('contrib')">📊 Contributions</button>
    </div>
  </div>

  <div class="main-grid">
    <div class="panel">
      <div>
        <div class="lbl">Pick a Story (Preset)</div>
        <div class="preset-grid" id="preset-btns">
          <button class="pbtn active" data-p="study" onclick="loadPreset('study',this)">
            📚 Will I study tonight?
            <small>Tiredness · Homework load · Coffee boost</small>
          </button>
          <button class="pbtn" data-p="spam" onclick="loadPreset('spam',this)">
            📧 Is this email spam?
            <small>ALL CAPS ratio · !!! marks · Unknown sender</small>
          </button>
          <button class="pbtn" data-p="game" onclick="loadPreset('game',this)">
            🎮 Should I play outside?
            <small>Weather · Homework done · Friend invited</small>
          </button>
        </div>
      </div>

      <div id="input-sliders"></div>

      <div>
        <div class="lbl">Weights (importance of each input)</div>
        <div id="weight-sliders"></div>
      </div>

      <div class="slider-box">
        <div class="srow"><span style="color:#f472b6">Bias b</span><span class="val" id="b-val" style="color:#f472b6">0.00</span></div>
        <input type="range" class="b-sl" id="bias-sl" min="-3" max="3" step="0.1" value="0" oninput="onBias()">
        <div style="font-size:10px;color:#64748b;margin-top:6px">Shifts the decision threshold — like needing extra motivation when tired.</div>
      </div>

      <div>
        <div class="lbl">Activation (squash z into output)</div>
        <div class="act-grid" id="act-btns">
          <button class="abtn" data-a="relu" onclick="setAct('relu',this)">ReLU</button>
          <button class="abtn active" data-a="sigmoid" onclick="setAct('sigmoid',this)">Sigmoid</button>
          <button class="abtn" data-a="step" onclick="setAct('step',this)">Step</button>
          <button class="abtn" data-a="linear" onclick="setAct('linear',this)">Linear</button>
        </div>
      </div>

      <div class="metric-grid">
        <div class="metric">
          <div class="mt">Pre-activation z</div>
          <div class="mv" id="z-val" style="color:#38bdf8">0.00</div>
          <div class="ms">w·x + b</div>
        </div>
        <div class="metric">
          <div class="mt">Output y</div>
          <div class="mv" id="y-val" style="color:#34d399">0.00</div>
          <div class="ms" id="y-label">activation(z)</div>
        </div>
        <div class="metric full">
          <div class="mt" id="decision-label">Decision</div>
          <div class="mv" id="dec-val" style="color:#fbbf24;font-size:18px">—</div>
        </div>
      </div>

      <button class="fire-btn" id="fire-btn" onclick="toggleFire()">⚡ FIRE THE NEURON</button>

      <div class="pipeline" id="pipeline"></div>
    </div>

    <div class="canvas-col">
      <div class="status-banner" id="status">Adjust inputs & weights, then press FIRE to watch the signal travel.</div>
      <canvas id="cvs" width="720" height="420"></canvas>
      <div class="mini-row">
        <div>
          <div class="mini-lbl">Activation curve (z → y)</div>
          <canvas id="cvs-act" width="340" height="140"></canvas>
        </div>
        <div>
          <div class="mini-lbl" id="mini2-lbl">Weighted contributions</div>
          <canvas id="cvs-mini" width="340" height="140"></canvas>
        </div>
      </div>
      <div class="legend">
        <div class="leg"><div class="leg-dot" style="background:#4ade80"></div> Inputs x</div>
        <div class="leg"><div class="leg-dot" style="background:#fbbf24"></div> Weights w</div>
        <div class="leg"><div class="leg-dot" style="background:#f472b6"></div> Bias b</div>
        <div class="leg"><div class="leg-dot" style="background:#38bdf8"></div> Sum z</div>
        <div class="leg"><div class="leg-dot" style="background:#34d399"></div> Output y</div>
      </div>
    </div>
  </div>
</div>

<script>
const PRESETS = {
  study: {
    labels: ['Tiredness', 'Homework hrs', 'Coffee cups'],
    inputs: [0.7, 0.5, 0.2],
    weights: [-1.8, 1.4, 0.9],
    bias: -0.3,
    inMin: [0,0,0], inMax: [1,3,3],
    decision: (y) => y > 0.5 ? 'Yes — hit the books! 📖' : 'Nah — couch wins 🛋️',
    thresh: 0.5
  },
  spam: {
    labels: ['CAPS ratio', '!!! count', 'Unknown sender'],
    inputs: [0.6, 0.4, 0.8],
    weights: [2.2, 1.5, 1.8],
    bias: -1.2,
    inMin: [0,0,0], inMax: [1,5,1],
    decision: (y) => y > 0.5 ? 'Spam folder 🗑️' : 'Inbox ✅',
    thresh: 0.5
  },
  game: {
    labels: ['Nice weather', 'Homework done', 'Friend invited'],
    inputs: [0.8, 0.3, 0.9],
    weights: [1.2, -1.5, 2.0],
    bias: 0.2,
    inMin: [0,0,0], inMax: [1,1,1],
    decision: (y) => y > 0.5 ? 'Go play! ⚽' : 'Stay in & grind 💻',
    thresh: 0.5
  }
};

const INPUT_NAMES = ['x₁', 'x₂', 'x₃'];
const WEIGHT_NAMES = ['w₁', 'w₂', 'w₃'];
const COLORS = { in: '#4ade80', w: '#fbbf24', b: '#f472b6', z: '#38bdf8', y: '#34d399' };

let preset = 'study';
let mode = 'flow';
let act = 'sigmoid';
let firing = false;
let fireT = 0;
let fireAnim = null;

const x = [0.7, 0.5, 0.2];
const w = [-1.8, 1.4, 0.9];
let bias = -0.3;

const cvs = document.getElementById('cvs');
const ctx = cvs.getContext('2d');
const cAct = document.getElementById('cvs-act');
const ctxA = cAct.getContext('2d');
const cMini = document.getElementById('cvs-mini');
const ctxM = cMini.getContext('2d');

function sigmoid(z) { return 1 / (1 + Math.exp(-z)); }
function relu(z) { return Math.max(0, z); }
function step(z) { return z >= 0 ? 1 : 0; }
function linear(z) { return z; }

function activate(z) {
  if (act === 'relu') return relu(z);
  if (act === 'sigmoid') return sigmoid(z);
  if (act === 'step') return step(z);
  return linear(z);
}

function actName() {
  if (act === 'relu') return 'ReLU';
  if (act === 'sigmoid') return 'σ';
  if (act === 'step') return 'Step';
  return 'Linear';
}

function dotSum() {
  let s = 0;
  for (let i = 0; i < 3; i++) s += w[i] * x[i];
  return s;
}

function zVal() { return dotSum() + bias; }

function buildSliders() {
  const p = PRESETS[preset];
  const inDiv = document.getElementById('input-sliders');
  const wDiv = document.getElementById('weight-sliders');
  inDiv.innerHTML = '<div class="lbl">Inputs (signals arriving)</div>';
  wDiv.innerHTML = '';
  for (let i = 0; i < 3; i++) {
    const mn = p.inMin[i], mx = p.inMax[i];
    inDiv.innerHTML += `
      <div class="slider-box">
        <div class="srow"><span style="color:#4ade80">${p.labels[i]} (${INPUT_NAMES[i]})</span>
        <span class="val" id="x${i}-val" style="color:#4ade80">${x[i].toFixed(2)}</span></div>
        <input type="range" class="in-sl" id="x${i}-sl" min="${mn}" max="${mx}" step="${(mx-mn)/20 || 0.05}" value="${x[i]}"
          oninput="onInput(${i})">
      </div>`;
    wDiv.innerHTML += `
      <div class="slider-box">
        <div class="srow"><span style="color:#fbbf24">${WEIGHT_NAMES[i]} on ${p.labels[i]}</span>
        <span class="val" id="w${i}-val" style="color:#fbbf24">${w[i].toFixed(2)}</span></div>
        <input type="range" class="w-sl" id="w${i}-sl" min="-3" max="3" step="0.1" value="${w[i]}"
          oninput="onWeight(${i})">
      </div>`;
  }
  document.getElementById('bias-sl').value = bias;
  document.getElementById('b-val').textContent = bias.toFixed(2);
}

function loadPreset(name, btn) {
  preset = name;
  const p = PRESETS[name];
  for (let i = 0; i < 3; i++) { x[i] = p.inputs[i]; w[i] = p.weights[i]; }
  bias = p.bias;
  document.querySelectorAll('.pbtn').forEach(b => b.classList.remove('active'));
  const activeBtn = btn || document.querySelector(`.pbtn[data-p="${name}"]`);
  if (activeBtn) activeBtn.classList.add('active');
  buildSliders();
  updateAll();
}

function onInput(i) {
  x[i] = parseFloat(document.getElementById(`x${i}-sl`).value);
  document.getElementById(`x${i}-val`).textContent = x[i].toFixed(2);
  updateAll();
}
function onWeight(i) {
  w[i] = parseFloat(document.getElementById(`w${i}-sl`).value);
  document.getElementById(`w${i}-val`).textContent = w[i].toFixed(2);
  updateAll();
}
function onBias() {
  bias = parseFloat(document.getElementById('bias-sl').value);
  document.getElementById('b-val').textContent = bias.toFixed(2);
  updateAll();
}

function setAct(a, btn) {
  act = a;
  document.querySelectorAll('.abtn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  updateAll();
}

function setMode(m) {
  mode = m;
  document.querySelectorAll('#mode-btns .mbtn').forEach(b => {
    b.classList.toggle('active', b.dataset.m === m);
  });
  document.getElementById('mini2-lbl').textContent =
    m === 'math' ? 'Dot product as projection (2D slice)' :
    m === 'contrib' ? 'Each wᵢxᵢ contribution' : 'Weighted contributions';
  draw();
}

function toggleFire() {
  firing = !firing;
  const btn = document.getElementById('fire-btn');
  btn.textContent = firing ? '⏹ STOP' : '⚡ FIRE THE NEURON';
  btn.classList.toggle('on', firing);
  if (firing) {
    fireT = 0;
    if (fireAnim) cancelAnimationFrame(fireAnim);
    animateFire();
  }
}

function animateFire() {
  if (!firing) return;
  fireT += 0.025;
  if (fireT >= 1) fireT = 0;
  draw();
  fireAnim = requestAnimationFrame(animateFire);
}

function updatePipeline(z, y) {
  const terms = [];
  for (let i = 0; i < 3; i++) terms.push(`(${w[i].toFixed(2)})(${x[i].toFixed(2)})`);
  const sum = dotSum();
  const p = PRESETS[preset];
  const dec = p.decision(y);
  document.getElementById('pipeline').innerHTML = `
    <div class="pipe-step">① Multiply: ${terms.join(' + ')}</div>
    <div class="pipe-step hot">② Sum (dot product): ${sum.toFixed(3)}</div>
    <div class="pipe-step">③ Add bias: ${sum.toFixed(3)} + (${bias.toFixed(2)}) = <b style="color:#38bdf8">${z.toFixed(3)}</b></div>
    <div class="pipe-step">④ ${actName()}(z) = <b style="color:#34d399">${y.toFixed(3)}</b></div>
    <div class="pipe-step out">⑤ ${dec}</div>`;
}

function updateAll() {
  const z = zVal();
  const y = activate(z);
  document.getElementById('z-val').textContent = z.toFixed(2);
  document.getElementById('y-val').textContent = y.toFixed(2);
  document.getElementById('y-label').textContent = actName() + '(z)';
  const p = PRESETS[preset];
  document.getElementById('dec-val').textContent = p.decision(y);
  updatePipeline(z, y);
  if (!firing) draw();
}

function drawNeuronFlow(progress) {
  const W = cvs.width, H = cvs.height;
  ctx.clearRect(0, 0, W, H);

  const inX = 70, sumX = 340, actX = 500, outX = 640;
  const inYs = [90, 210, 330];
  const sumY = 210;

  // Title
  ctx.fillStyle = '#64748b';
  ctx.font = 'bold 11px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('FORWARD PASS', W/2, 28);

  function node(x, y, r, color, label, sub) {
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fillStyle = color + '22';
    ctx.fill();
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.5;
    ctx.stroke();
    ctx.fillStyle = '#f8fafc';
    ctx.font = 'bold 14px monospace';
    ctx.textAlign = 'center';
    ctx.fillText(label, x, y + 5);
    if (sub) {
      ctx.fillStyle = '#94a3b8';
      ctx.font = '600 10px sans-serif';
      ctx.fillText(sub, x, y + r + 16);
    }
  }

  function edge(x1, y1, x2, y2, color, alpha, label, pulse) {
    ctx.globalAlpha = alpha;
    ctx.strokeStyle = color;
    ctx.lineWidth = 2 + Math.abs(label) * 0.3;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    const cx = (x1 + x2) / 2;
    ctx.quadraticCurveTo(cx, y1, x2, y2);
    ctx.stroke();
    if (pulse !== undefined && pulse >= 0) {
      const t = Math.max(0, Math.min(1, pulse));
      const px = x1 + (x2 - x1) * t;
      const py = y1 + (y2 - y1) * t;
      ctx.beginPath();
      ctx.arc(px, py, 7, 0, Math.PI * 2);
      ctx.fillStyle = '#fde68a';
      ctx.fill();
      ctx.shadowColor = '#fde68a';
      ctx.shadowBlur = 12;
    }
    ctx.shadowBlur = 0;
    if (label !== undefined && Math.abs(label) > 0.01) {
      ctx.fillStyle = color;
      ctx.font = 'bold 11px monospace';
      ctx.textAlign = 'center';
      ctx.fillText(label.toFixed(2), cx, (y1 + y2) / 2 - 8);
    }
    ctx.globalAlpha = 1;
  }

  const p = PRESETS[preset];
  const z = zVal();
  const y = activate(z);
  const prog = progress || 0;

  // Edges inputs → sum
  for (let i = 0; i < 3; i++) {
    const contrib = w[i] * x[i];
    const pulse = firing ? Math.max(0, Math.min(1, (prog - i * 0.2) * 2)) : -1;
    const alpha = 0.35 + Math.min(1, Math.abs(contrib) / 3) * 0.5;
    edge(inX + 28, inYs[i], sumX - 32, sumY, COLORS.w, alpha, contrib, pulse);
  }

  // sum → activation
  const p2 = firing ? Math.max(0, Math.min(1, (prog - 0.65) * 3)) : -1;
  edge(sumX + 32, sumY, actX - 36, sumY, COLORS.z, 0.7, z, p2);

  // bias arrow into sum
  ctx.fillStyle = COLORS.b;
  ctx.font = 'bold 12px monospace';
  ctx.textAlign = 'center';
  ctx.fillText(`b=${bias.toFixed(2)}`, sumX, sumY - 52);
  ctx.beginPath();
  ctx.moveTo(sumX, sumY - 42);
  ctx.lineTo(sumX, sumY - 30);
  ctx.strokeStyle = COLORS.b;
  ctx.lineWidth = 2;
  ctx.stroke();

  // activation → output
  const p3 = firing ? Math.max(0, Math.min(1, (prog - 0.85) * 5)) : -1;
  edge(actX + 36, sumY, outX - 28, sumY, COLORS.y, 0.8, y, p3);

  // Input nodes
  for (let i = 0; i < 3; i++) {
    node(inX, inYs[i], 28, COLORS.in, x[i].toFixed(2), p.labels[i]);
    ctx.fillStyle = COLORS.w;
    ctx.font = 'bold 11px monospace';
    ctx.textAlign = 'right';
    ctx.fillText(`w=${w[i].toFixed(1)}`, inX - 38, inYs[i] + 4);
  }

  // Sum
  node(sumX, sumY, 34, COLORS.z, 'Σ', 'weighted sum');
  ctx.fillStyle = '#38bdf8';
  ctx.font = 'bold 13px monospace';
  ctx.fillText(`z=${z.toFixed(2)}`, sumX, sumY + 52);

  // Activation box
  ctx.fillStyle = 'rgba(56,189,248,0.08)';
  ctx.strokeStyle = '#38bdf8';
  ctx.lineWidth = 2;
  roundRect(actX - 40, sumY - 38, 80, 76, 12);
  ctx.fill();
  ctx.stroke();
  ctx.fillStyle = '#7dd3fc';
  ctx.font = 'bold 12px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText(actName(), actX, sumY - 6);
  ctx.font = '10px sans-serif';
  ctx.fillStyle = '#94a3b8';
  ctx.fillText('activation', actX, sumY + 10);

  // Output
  node(outX, sumY, 30, COLORS.y, y.toFixed(2), 'output y');

  // Mode overlays
  if (mode === 'math') {
    ctx.fillStyle = 'rgba(15,23,42,0.85)';
    ctx.fillRect(12, 44, 200, 72);
    ctx.fillStyle = '#38bdf8';
    ctx.font = 'bold 12px monospace';
    ctx.textAlign = 'left';
    ctx.fillText('w · x = Σ wᵢxᵢ', 22, 68);
    ctx.fillStyle = '#94a3b8';
    ctx.font = '11px monospace';
    ctx.fillText(`${dotSum().toFixed(2)} + b = ${z.toFixed(2)}`, 22, 88);
    ctx.fillStyle = '#64748b';
    ctx.font = '10px sans-serif';
    ctx.fillText('Same as one row of', 22, 106);
    ctx.fillText('matrix × vector!', 22, 120);
  }
}

function roundRect(x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.lineTo(x + w - r, y);
  ctx.quadraticCurveTo(x + w, y, x + w, y + r);
  ctx.lineTo(x + w, y + h - r);
  ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  ctx.lineTo(x + r, y + h);
  ctx.quadraticCurveTo(x, y + h, x, y + h - r);
  ctx.lineTo(x, y + r);
  ctx.quadraticCurveTo(x, y, x + r, y);
  ctx.closePath();
}

function drawActivationCurve() {
  const W = cAct.width, H = cAct.height;
  ctxA.clearRect(0, 0, W, H);
  const pad = 24;
  const zNow = zVal();
  const yNow = activate(zNow);

  ctxA.strokeStyle = 'rgba(255,255,255,0.08)';
  ctxA.lineWidth = 1;
  ctxA.beginPath();
  ctxA.moveTo(pad, H/2);
  ctxA.lineTo(W - pad, H/2);
  ctxA.moveTo(W/2, pad);
  ctxA.lineTo(W/2, H - pad);
  ctxA.stroke();

  ctxA.strokeStyle = '#38bdf8';
  ctxA.lineWidth = 2.5;
  ctxA.beginPath();
  for (let i = 0; i <= 200; i++) {
    const z = -4 + (8 * i) / 200;
    const y = activate(z);
    const px = pad + (i / 200) * (W - 2 * pad);
    const py = H - pad - ((y + 0.5) / (act === 'linear' ? 5 : 1.5)) * (H - 2 * pad);
    if (i === 0) ctxA.moveTo(px, py);
    else ctxA.lineTo(px, py);
  }
  ctxA.stroke();

  const px = pad + ((zNow + 4) / 8) * (W - 2 * pad);
  const py = H - pad - ((yNow + 0.5) / (act === 'linear' ? 5 : 1.5)) * (H - 2 * pad);
  ctxA.fillStyle = '#fde68a';
  ctxA.beginPath();
  ctxA.arc(px, py, 7, 0, Math.PI * 2);
  ctxA.fill();
  ctxA.fillStyle = '#94a3b8';
  ctxA.font = '10px sans-serif';
  ctxA.textAlign = 'center';
  ctxA.fillText('your z', px, py - 12);
}

function drawMini() {
  const W = cMini.width, H = cMini.height;
  ctxM.clearRect(0, 0, W, H);
  const pad = 28;
  const contribs = [0, 1, 2].map(i => w[i] * x[i]);
  const maxC = Math.max(0.5, ...contribs.map(Math.abs));

  if (mode === 'math') {
    // 2D: show w vector and x vector, projection
    const ox = W * 0.35, oy = H * 0.55;
    const scale = 38;
    const xv = [x[0], x[1]], wv = [w[0], w[1]];
    const xLen = Math.hypot(xv[0], xv[1]) || 1;
    const wLen = Math.hypot(wv[0], wv[1]) || 1;
    const dot = xv[0] * wv[0] + xv[1] * wv[1];
    const proj = (dot / (wLen * wLen)) * wv;

    function arrow(x1, y1, x2, y2, col, lbl) {
      ctxM.strokeStyle = col;
      ctxM.fillStyle = col;
      ctxM.lineWidth = 2.5;
      ctxM.beginPath();
      ctxM.moveTo(x1, y1);
      ctxM.lineTo(x2, y2);
      ctxM.stroke();
      ctxM.font = 'bold 10px monospace';
      ctxM.fillText(lbl, x2 + 6, y2);
    }
    arrow(ox, oy, ox + xv[0] * scale, oy - xv[1] * scale, COLORS.in, 'x');
    arrow(ox, oy, ox + wv[0] * scale * 0.7, oy - wv[1] * scale * 0.7, COLORS.w, 'w');
    arrow(ox, oy, ox + proj[0] * scale * 0.7, oy - proj[1] * scale * 0.7, '#fde68a', 'proj');
    ctxM.fillStyle = '#94a3b8';
    ctxM.font = '10px sans-serif';
    ctxM.fillText('x₁,x₂ slice of dot product', pad, 18);
    return;
  }

  const barW = (W - 2 * pad) / 3 - 12;
  for (let i = 0; i < 3; i++) {
    const bx = pad + i * (barW + 12);
    const h = (contribs[i] / maxC) * (H - 2 * pad) * 0.85;
    const baseY = H - pad;
    ctxM.fillStyle = contribs[i] >= 0 ? 'rgba(52,211,153,0.7)' : 'rgba(248,113,113,0.7)';
    if (h >= 0) ctxM.fillRect(bx, baseY - h, barW, h);
    else ctxM.fillRect(bx, baseY, barW, -h);
    ctxM.fillStyle = '#94a3b8';
    ctxM.font = '10px monospace';
    ctxM.textAlign = 'center';
    ctxM.fillText(WEIGHT_NAMES[i] + 'x' + (i + 1), bx + barW / 2, H - 8);
    ctxM.fillStyle = '#f8fafc';
    ctxM.font = 'bold 11px monospace';
    ctxM.fillText(contribs[i].toFixed(2), bx + barW / 2, baseY - h - (h >= 0 ? 8 : -14));
  }
}

function draw() {
  const prog = firing ? fireT : 1;
  drawNeuronFlow(prog);
  drawActivationCurve();
  drawMini();
  const z = zVal();
  const y = activate(z);
  const st = document.getElementById('status');
  if (firing) {
    st.className = 'status-banner fire';
    st.textContent = 'Signal traveling: inputs → multiply → sum → +bias → activation → output';
  } else {
    st.className = 'status-banner';
    st.textContent = `z = ${z.toFixed(2)} → y = ${activate(z).toFixed(2)} · ${PRESETS[preset].decision(y)}`;
  }
}

buildSliders();
loadPreset('study', document.querySelector('.pbtn.active'));
</script>
</body>
</html>
"""
    components.html(html_code, height=920, scrolling=True)


def main():
    st.title("🧠 Page 64: A Single Neuron")
    st.markdown(
        """
        A **neuron** is the smallest useful unit in a neural network — one decision-maker built from math you already know.

        It does exactly five things:

        1. **Receive** inputs $x_1, x_2, \\ldots, x_n$ (signals)
        2. **Weight** each input: multiply by $w_i$
        3. **Sum** everything — that's the **dot product** $\\mathbf{w} \\cdot \\mathbf{x}$
        4. **Shift** by a **bias** $b$
        5. **Activate** — squash the result through a nonlinear function to produce output $y$

        One neuron = one row of a matrix multiply, plus a bias, plus a squashing function. That's the whole bridge from linear algebra to AI.
        """
    )

    st.divider()
    st.markdown("### 1) The Neuron Lab ⚡")
    st.markdown(
        "Pick a story preset, drag inputs and weights, choose an activation, then press **FIRE THE NEURON** "
        "to watch the signal flow. Switch modes to see the dot product view or per-input contributions."
    )
    render_neuron_lab()
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔢 The Math (One Line)")
        st.info("A neuron is a function: $y = f(\\mathbf{w} \\cdot \\mathbf{x} + b)$")
        st.markdown(
            r"""
**Step by step:**

| Step | Formula | Meaning |
|------|---------|---------|
| Weight | $w_i x_i$ | How much input $i$ matters |
| Sum | $z = \sum_i w_i x_i$ | Dot product $\mathbf{w}\cdot\mathbf{x}$ |
| Bias | $z \leftarrow z + b$ | Shift the decision boundary |
| Activate | $y = f(z)$ | Nonlinear output (ReLU, sigmoid, …) |

With 3 inputs, $\mathbf{w}$ is a **row vector** and $\mathbf{x}$ is a **column vector** — same as **one row** of matrix $\times$ vector from Page 12.
"""
        )

    with col2:
        st.markdown("### 🧬 Biology ↔ Math")
        st.success("Dendrites receive · Synapses weigh · Soma sums · Axon fires")
        st.markdown(
            """
| Biology | Math |
|---------|------|
| Signals arriving | Inputs $\\mathbf{x}$ |
| Synapse strength | Weights $\\mathbf{w}$ |
| Cell body integrates | Sum + bias $z$ |
| Fires or stays quiet | Activation $f(z)$ |

**Negative weights** mean “this input pushes *against* firing.”
**Bias** means the neuron can fire even when all inputs are zero — a built-in tendency.
"""
        )

    st.divider()

    st.markdown("### 🎬 Three Things to Try")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### ⚡ Fire & Watch")
        st.write(
            "Press **FIRE THE NEURON** and follow the yellow pulse: "
            "each input lane → sum node → activation box → output. "
            "Thicker edges = larger $|w_i x_i|$."
        )
    with c2:
        st.markdown("#### 📊 Contributions Mode")
        st.write(
            "Switch to **Contributions** to see each $w_i x_i$ as a bar — "
            "green pushes the sum up, red pulls it down. "
            "The dot product is just adding these bars."
        )
    with c3:
        st.markdown("#### 🔢 Dot Product Mode")
        st.write(
            "Switch to **Dot Product** for a 2D slice: "
            "vector $\\mathbf{x}$ projected onto $\\mathbf{w}$. "
            "Same geometry as Page 6 — now inside a neuron."
        )

    st.divider()

    st.markdown("### 🤖 Bridge: From One Neuron to Networks")
    a1, a2, a3 = st.columns(3)
    with a1:
        st.markdown("#### 📐 Still Linear Algebra")
        st.write(
            "10 neurons in a layer = 10 rows of weights — a **10×n matrix** times your input vector. "
            "You already know how to do this from Pages 10–12."
        )
    with a2:
        st.markdown("#### 🎛️ Weights Are Learned")
        st.write(
            "Here you set weights by hand. In training (Pages 50–56, 70), "
            "**gradient descent** nudges every $w_i$ and $b$ until predictions improve."
        )
    with a3:
        st.markdown("#### ➡️ Next: Activations")
        st.write(
            "This page previews ReLU & sigmoid. "
            "Page 65 compares them side by side — and Page 66 shows why stacking layers **without** nonlinear activations still gives one big linear map."
        )

    st.divider()
    st.markdown(
        '<div style="text-align:center;color:#94a3b8;font-size:13px;">'
        "Page 64 — you can now read a neuron as dot product + bias + activation. "
        "Next Up: Page 65 — Activation Functions Compared ➔"
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
