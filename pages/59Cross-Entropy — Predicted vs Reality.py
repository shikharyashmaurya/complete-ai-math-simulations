import streamlit as st
import streamlit.components.v1 as components
import numpy as np

st.set_page_config(page_title="Cross-Entropy — Predicted vs Reality", layout="wide")

def render_cross_entropy_lab():
    html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{
  font-family:'Inter',sans-serif;
  background:#0f172a;
  color:#f8fafc;
  overflow:hidden;
  padding:10px;
}
.outer-container{
  display:flex;
  flex-direction:column;
  gap:10px;
  max-width:1150px;
  margin:0 auto;
}
.app-layout{
  display:flex;
  flex-direction:row;
  gap:20px;
}
.panel-left{
  flex:1.1;
  display:flex;
  flex-direction:column;
  gap:8px;
}
.panel-right{
  flex:1.4;
  display:flex;
  flex-direction:column;
  gap:8px;
}
.card {
  background: rgba(30, 41, 59, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 10px 14px;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(8px);
}
h2 {
  font-size: 20px;
  font-weight: 800;
  color: #f1f5f9;
  letter-spacing: -0.5px;
  margin-bottom: 4px;
}
.sub {
  font-size: 13px;
  color: #94a3b8;
  line-height: 1.4;
}

/* Tab/Switch Design */
.mode-row {
  display: flex;
  gap: 8px;
}
.mbtn {
  flex: 1;
  background: rgba(255, 255, 255, 0.05);
  color: #cbd5e1;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 10px 4px;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
  transition: .2s;
  font-size: 12px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}
.mbtn:hover {
  background: rgba(255, 255, 255, 0.1);
}
.mbtn.active {
  background: rgba(129, 140, 248, 0.16);
  border-color: #818cf8;
  color: #818cf8;
  box-shadow: 0 0 12px rgba(129, 140, 248, 0.2);
}

/* Custom Grid for presets */
.preset-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  margin-top: 5px;
}
.preset-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 10px;
  padding: 8px 6px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}
.preset-card:hover {
  background: rgba(255, 255, 255, 0.07);
  border-color: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
}
.preset-card.active {
  background: rgba(167, 139, 250, 0.12);
  border-color: #a78bfa;
  box-shadow: 0 0 12px rgba(167, 139, 250, 0.25);
}
.preset-card .emoji { font-size: 20px; }
.preset-card .name { font-size: 11px; font-weight: 700; color: #e2e8f0; }
.preset-card .desc { font-size: 9px; color: #94a3b8; }

/* Sliders */
.slider-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 5px;
}
.slider-row {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.slabel-row {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  font-weight: 700;
  color: #cbd5e1;
}
.sval {
  font-family: monospace;
  font-size: 14px;
  font-weight: 900;
}
input[type=range] {
  width: 100%;
  height: 5px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  outline: none;
  -webkit-appearance: none;
  cursor: pointer;
}
input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.1s;
}
input[type=range]::-webkit-slider-thumb:hover {
  transform: scale(1.25);
}

/* Class-specific slider colors */
input.cat-slider::-webkit-slider-thumb { background: #22d3ee; box-shadow: 0 0 8px #22d3ee; }
input.dog-slider::-webkit-slider-thumb { background: #fbbf24; box-shadow: 0 0 8px #fbbf24; }
input.rabbit-slider::-webkit-slider-thumb { background: #f472b6; box-shadow: 0 0 8px #f472b6; }

/* Retro Terminal Log */
.terminal-log {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 8px 12px;
  font-family: monospace;
  font-size: 11px;
  color: #4ade80;
  height: 80px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.log-line { line-height: 1.3; }
.log-line span.cyan { color: #22d3ee; }
.log-line span.gold { color: #facc15; }
.log-line span.rose { color: #fb7185; }
.log-line span.purple { color: #c084fc; }

/* Canvas Visualizer wrapper */
#canvas-wrap {
  position: relative;
  background: rgba(30, 41, 59, 0.25);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: inset 0 0 24px rgba(0, 0, 0, 0.5);
  overflow: hidden;
  width: 100%;
}
canvas {
  display: block;
  width: 100%;
}

.shake-heavy {
  animation: shake 0.15s infinite alternate;
}
@keyframes shake {
  0% { transform: translate(1px, 1px) rotate(0deg); }
  100% { transform: translate(-1px, -1px) rotate(0.2deg); }
}
</style>
</head>
<body>

<div class="outer-container">
  <div class="app-layout">
    <!-- LEFT PANEL: Controls, Presets, Sliders, Log -->
    <div class="panel-left">
      <!-- Title -->
      <div class="card">
        <h2>Cross-Entropy Lab 🌋</h2>
        <p class="sub">Compare reality (P) against model beliefs (Q) to see surprise penalties fly, cables overload, and the mathematical waste (KL Divergence) grow live!</p>
      </div>

      <!-- Reality Mode Selector -->
      <div class="card">
        <div class="slabel-row" style="margin-bottom:6px;">
          <span>Target Distribution Reality (P) Mode</span>
        </div>
        <div class="mode-row">
          <button class="mbtn active" id="p-mode-presets" onclick="switchPMode('preset')">🎯 Reality Presets</button>
          <button class="mbtn" id="p-mode-manual" onclick="switchPMode('manual')">🎛️ Manual Reality</button>
        </div>

        <!-- P PRESETS -->
        <div class="preset-grid" id="p-presets" style="margin-top: 8px;">
          <div class="preset-card active" onclick="setP([1.0, 0.0, 0.0], this, 'Pure Cat 🐱')">
            <span class="emoji">🐱</span>
            <span class="name">Pure Cat</span>
            <span class="desc">[1.0, 0.0, 0.0]</span>
          </div>
          <div class="preset-card" onclick="setP([0.0, 1.0, 0.0], this, 'Pure Dog 🐶')">
            <span class="emoji">🐶</span>
            <span class="name">Pure Dog</span>
            <span class="desc">[0.0, 1.0, 0.0]</span>
          </div>
          <div class="preset-card" onclick="setP([0.0, 0.0, 1.0], this, 'Pure Rabbit 🐰')">
            <span class="emoji">🐰</span>
            <span class="name">Pure Rabbit</span>
            <span class="desc">[0.0, 0.0, 1.0]</span>
          </div>
          <div class="preset-card" onclick="setP([0.8, 0.1, 0.1], this, 'Soft Label 🐾')">
            <span class="emoji">🐾</span>
            <span class="name">Fuzzy Target</span>
            <span class="desc">[0.8, 0.1, 0.1]</span>
          </div>
        </div>

        <!-- P SLIDERS (Shown in manual mode) -->
        <div class="slider-container" id="p-sliders-wrap" style="display:none; margin-top: 8px;">
          <!-- Active P Sliders will go here -->
        </div>
      </div>

      <!-- Prediction Q Presets and Sliders -->
      <div class="card">
        <div class="slabel-row" style="margin-bottom:6px;">
          <span>Model Prediction presets (Q)</span>
        </div>
        <div class="preset-grid" style="margin-bottom: 12px;">
          <div class="preset-card active" id="q-preset-perfect" onclick="setQPreset('perfect')">
            <span class="emoji">🎯</span>
            <span class="name">Perfect Fit</span>
            <span class="desc">Q = P (No waste)</span>
          </div>
          <div class="preset-card" id="q-preset-uniform" onclick="setQPreset('uniform')">
            <span class="emoji">🤷</span>
            <span class="name">Ignorance</span>
            <span class="desc">33% split each</span>
          </div>
          <div class="preset-card" id="q-preset-wrong" onclick="setQPreset('wrong')">
            <span class="emoji">💥</span>
            <span class="name">Confident Wrong</span>
            <span class="desc">Predict dog for Cat</span>
          </div>
          <div class="preset-card" id="q-preset-infinite" onclick="setQPreset('infinite')">
            <span class="emoji">🌋</span>
            <span class="name">Meltdown Limit</span>
            <span class="desc">Q(True) = 0.01%</span>
          </div>
        </div>

        <div class="slabel-row">
          <span>Model Beliefs (Q) Sliders</span>
          <span style="font-size:10px; color:#94a3b8; font-weight:normal;">Auto-normalizing to 100%</span>
        </div>
        <!-- Q SLIDERS -->
        <div class="slider-container" id="q-sliders-wrap">
          <!-- Active Q Sliders will go here -->
        </div>
      </div>

      <!-- Retro Terminal Log -->
      <div class="terminal-log" id="log-box">
        <div class="log-line">> <span class="cyan">Cross-Entropy Evaluator successfully booted.</span></div>
      </div>
    </div>

    <!-- RIGHT PANEL: Animated Visualization Canvas -->
    <div class="panel-right">
      <div id="canvas-wrap">
        <canvas id="viz-canvas" width="600" height="500"></canvas>
      </div>
    </div>
  </div>
</div>

<script>
const canvas = document.getElementById('viz-canvas');
const ctx = canvas.getContext('2d');
const logBox = document.getElementById('log-box');
const canvasWrap = document.getElementById('canvas-wrap');

// High-DPI / Retina Canvas Scaling for razor-sharp text and lines
const dpr = window.devicePixelRatio || 1;
canvas.style.width = '600px';
canvas.style.height = '500px';
canvas.width = 600 * dpr;
canvas.height = 500 * dpr;
ctx.scale(dpr, dpr);

// App States
let pMode = 'preset'; // 'preset' or 'manual'
let P = [1.0, 0.0, 0.0]; // Reality
let Q = [1.0, 0.0, 0.0]; // Model Predictions
let activePName = "Pure Cat 🐱";

// Spark particles for overload animations
let sparks = [];
let energyParticles = [];
let tick = 0;

// Log writer
function addLog(text, type = 'info') {
  const line = document.createElement('div');
  line.className = 'log-line';
  let spanClass = 'cyan';
  if (type === 'warn') spanClass = 'rose';
  if (type === 'gold') spanClass = 'gold';
  if (type === 'purple') spanClass = 'purple';
  
  line.innerHTML = `> <span class="${spanClass}">${text}</span>`;
  logBox.appendChild(line);
  logBox.scrollTop = logBox.scrollHeight;
  
  while (logBox.children.length > 5) {
    logBox.removeChild(logBox.firstChild);
  }
}

// Math utils
function log2(val) {
  if (val <= 0.000001) return -100; // avoid log(0) negative infinity
  return Math.log2(val);
}

function getShannonEntropy(arr) {
  let ent = 0;
  for (let i = 0; i < 3; i++) {
    if (arr[i] > 0.00001) {
      ent -= arr[i] * log2(arr[i]);
    }
  }
  return ent;
}

function getCrossEntropy(pArr, qArr) {
  let ce = 0;
  for (let i = 0; i < 3; i++) {
    if (pArr[i] > 0.00001) {
      const qVal = Math.max(0.0001, qArr[i]); // floor at 0.01%
      ce -= pArr[i] * log2(qVal);
    }
  }
  return ce;
}

// Spark Classes for Visualizer
class Spark {
  constructor(x, y, color) {
    this.x = x;
    this.y = y;
    const angle = Math.random() * Math.PI * 2;
    const speed = 1.0 + Math.random() * 4.0;
    this.vx = Math.cos(angle) * speed;
    this.vy = Math.sin(angle) * speed - 1.0;
    this.size = 1.5 + Math.random() * 2.5;
    this.life = 20 + Math.random() * 25;
    this.maxLife = this.life;
    this.color = color;
  }
  update() {
    this.x += this.vx;
    this.y += this.vy;
    this.vy += 0.08; // subtle gravity
    this.life--;
  }
  draw(c) {
    const alpha = Math.max(0, this.life / this.maxLife);
    c.save();
    c.globalAlpha = alpha;
    c.beginPath();
    c.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    c.fillStyle = this.color;
    c.shadowBlur = 6;
    c.shadowColor = this.color;
    c.fill();
    c.restore();
  }
}

class EnergyParticle {
  constructor(channelIdx, color) {
    this.channelIdx = channelIdx;
    this.color = color;
    this.progress = 0; // 0 to 1
  }
  update(speed) {
    this.progress += speed;
  }
  draw(c, startX, endX, y) {
    c.save();
    const curX = startX + this.progress * (endX - startX);
    c.beginPath();
    c.arc(curX, y, 4, 0, Math.PI * 2);
    c.fillStyle = this.color;
    c.shadowBlur = 8;
    c.shadowColor = this.color;
    c.fill();
    c.restore();
  }
}

// Switch between Preset P and Manual P modes
function switchPMode(mode) {
  if (pMode === mode) return;
  pMode = mode;
  
  document.getElementById('p-mode-presets').classList.toggle('active', mode === 'preset');
  document.getElementById('p-mode-manual').classList.toggle('active', mode === 'manual');
  
  document.getElementById('p-presets').style.display = mode === 'preset' ? 'grid' : 'none';
  document.getElementById('p-sliders-wrap').style.display = mode === 'manual' ? 'flex' : 'none';
  
  if (mode === 'manual') {
    activePName = "Custom Reality 🎛️";
    addLog("Reality editing unlocked. Watch how cross-entropy is always larger than Shannon Entropy!", "cyan");
  } else {
    // Re-trigger the active preset card
    const activeCard = document.querySelector('#p-presets .preset-card.active');
    if (activeCard) {
      activeCard.click();
    }
  }
  updatePresetHighlights();
}

// Adjust Reality P (Preset mode)
function setP(arr, element, name) {
  P = [...arr];
  activePName = name;
  
  // Highlight active preset card
  const cards = document.querySelectorAll('#p-presets .preset-card');
  cards.forEach(c => c.classList.remove('active'));
  if (element) element.classList.add('active');
  
  // Update sliders to reflect preset values
  updateSlidersUI();
  
  const hP = getShannonEntropy(P);
  addLog(`Reality Updated: ${name}. Entropy H(P) = ${hP.toFixed(3)} bits.`, 'info');
  updatePresetHighlights();
}

// Adjust Reality P (Manual Slider change)
function onPSliderChange(idx, val) {
  const newValue = parseFloat(val);
  let restSum = 0;
  for (let i = 0; i < 3; i++) {
    if (i !== idx) restSum += P[i];
  }
  
  const remaining = 1.0 - newValue;
  if (restSum > 0.0001) {
    for (let i = 0; i < 3; i++) {
      if (i !== idx) {
        P[i] = (P[i] / restSum) * remaining;
      }
    }
  } else {
    // distribute equally
    for (let i = 0; i < 3; i++) {
      if (i !== idx) P[i] = remaining / 2.0;
    }
  }
  P[idx] = newValue;
  
  // ensure exact sum to 1.0
  let sum = P.reduce((a, b) => a + b, 0);
  if (Math.abs(sum - 1.0) > 0.000001) {
    const err = (1.0 - sum) / 3.0;
    for (let i = 0; i < 3; i++) P[i] = Math.max(0, P[i] + err);
  }
  
  updateSlidersUI();
  updatePresetHighlights();
}

// Adjust Prediction Q (Manual Slider change with auto proportional normalization)
function onQSliderChange(idx, val) {
  const newValue = parseFloat(val);
  let restSum = 0;
  for (let i = 0; i < 3; i++) {
    if (i !== idx) restSum += Q[i];
  }
  
  const remaining = 1.0 - newValue;
  if (restSum > 0.0001) {
    for (let i = 0; i < 3; i++) {
      if (i !== idx) {
        Q[i] = (Q[i] / restSum) * remaining;
      }
    }
  } else {
    for (let i = 0; i < 3; i++) {
      if (i !== idx) Q[i] = remaining / 2.0;
    }
  }
  Q[idx] = newValue;
  
  // Clamp check
  let sum = Q.reduce((a, b) => a + b, 0);
  if (Math.abs(sum - 1.0) > 0.000001) {
    const err = (1.0 - sum) / 3.0;
    for (let i = 0; i < 3; i++) Q[i] = Math.max(0, Q[i] + err);
  }
  
  updateSlidersUI();
  updatePresetHighlights();
}

// Q Presets
function setQPreset(type) {
  if (type === 'perfect') {
    Q = [...P];
    addLog("Q reset to match Reality P. Cross-Entropy drops to its absolute minimum H(P)!", "info");
  } else if (type === 'uniform') {
    Q = [0.3333, 0.3333, 0.3334];
    addLog("Q set to Uniform Ignorance. Equal splits represent standard bias-free initialization.", "info");
  } else if (type === 'wrong') {
    // Find the largest P class and predict something else
    let maxIdx = P.indexOf(Math.max(...P));
    let targetWrong = (maxIdx + 1) % 3;
    let otherWrong = (maxIdx + 2) % 3;
    Q = [0.0, 0.0, 0.0];
    Q[targetWrong] = 0.98;
    Q[maxIdx] = 0.01;
    Q[otherWrong] = 0.01;
    addLog("Model is highly confident in the WRONG class! Watch the stress build up!", "warn");
  } else if (type === 'infinite') {
    // Extremely small probability on the main class
    let maxIdx = P.indexOf(Math.max(...P));
    let targetWrong = (maxIdx + 1) % 3;
    let otherWrong = (maxIdx + 2) % 3;
    Q = [0.0, 0.0, 0.0];
    Q[targetWrong] = 0.9999;
    Q[maxIdx] = 0.0001; // 0.01%
    Q[otherWrong] = 0.0;
    addLog("Model believes the true class has near-zero probability. Maximum stress explosion!", "warn");
  }
  updateSlidersUI();
  updatePresetHighlights();
}

// Highlight the active Q preset card if it matches exactly
function updatePresetHighlights() {
  const cardPerfect = document.getElementById('q-preset-perfect');
  const cardUniform = document.getElementById('q-preset-uniform');
  const cardWrong = document.getElementById('q-preset-wrong');
  const cardInfinite = document.getElementById('q-preset-infinite');
  
  [cardPerfect, cardUniform, cardWrong, cardInfinite].forEach(c => c.classList.remove('active'));
  
  const isPerfect = Math.abs(Q[0] - P[0]) < 0.01 && Math.abs(Q[1] - P[1]) < 0.01 && Math.abs(Q[2] - P[2]) < 0.01;
  const isUniform = Math.abs(Q[0] - 0.333) < 0.02 && Math.abs(Q[1] - 0.333) < 0.02;
  
  let maxIdx = P.indexOf(Math.max(...P));
  const isWrong = Q[maxIdx] < 0.02 && Math.max(...Q) > 0.95;
  const isInfinite = Q[maxIdx] < 0.001;

  if (isPerfect) cardPerfect.classList.add('active');
  else if (isInfinite) cardInfinite.classList.add('active');
  else if (isWrong) cardWrong.classList.add('active');
  else if (isUniform) cardUniform.classList.add('active');
}

// Generate HTML elements dynamically
function buildSliders() {
  // P Sliders
  const pContainer = document.getElementById('p-sliders-wrap');
  pContainer.innerHTML = '';
  const pColors = ['#22d3ee', '#fbbf24', '#f472b6'];
  const labels = ['🐱 Cat', '🐶 Dog', '🐰 Rabbit'];
  
  for (let i = 0; i < 3; i++) {
    const row = document.createElement('div');
    row.className = 'slider-row';
    row.innerHTML = `
      <div class="slabel-row">
        <span>Reality P(${labels[i]})</span>
        <span class="sval" style="color: ${pColors[i]};" id="p-val-${i}">0.00</span>
      </div>
      <input type="range" class="${i===0?'cat-slider':i===1?'dog-slider':'rabbit-slider'}" id="p-slider-${i}" min="0.0" max="1.0" step="0.01" value="${P[i]}" oninput="onPSliderChange(${i}, this.value)">
    `;
    pContainer.appendChild(row);
  }
  
  // Q Sliders
  const qContainer = document.getElementById('q-sliders-wrap');
  qContainer.innerHTML = '';
  for (let i = 0; i < 3; i++) {
    const row = document.createElement('div');
    row.className = 'slider-row';
    row.innerHTML = `
      <div class="slabel-row">
        <span>Prediction Q(${labels[i]})</span>
        <span class="sval" style="color: ${pColors[i]};" id="q-val-${i}">0.00</span>
      </div>
      <input type="range" class="${i===0?'cat-slider':i===1?'dog-slider':'rabbit-slider'}" id="q-slider-${i}" min="0.0" max="1.0" step="0.01" value="${Q[i]}" oninput="onQSliderChange(${i}, this.value)">
    `;
    qContainer.appendChild(row);
  }
  
  updateSlidersUI();
}

function updateSlidersUI() {
  const pColors = ['#22d3ee', '#fbbf24', '#f472b6'];
  for (let i = 0; i < 3; i++) {
    const pValEl = document.getElementById(`p-val-${i}`);
    const pSliderEl = document.getElementById(`p-slider-${i}`);
    if (pValEl) pValEl.innerText = `${(P[i]*100).toFixed(0)}%`;
    if (pSliderEl) pSliderEl.value = P[i];
    
    const qValEl = document.getElementById(`q-val-${i}`);
    const qSliderEl = document.getElementById(`q-slider-${i}`);
    if (qValEl) qValEl.innerText = `${(Q[i]*100).toFixed(0)}%`;
    if (qSliderEl) qSliderEl.value = Q[i];
  }
}

// DRAW GAUGE (Top Dial)
function drawGauge(cx, cy, r, ce, hp) {
  const startAngle = Math.PI * 0.92;
  const endAngle = Math.PI * 2.08;
  const maxBits = 10;
  
  // Backing arc
  ctx.beginPath();
  ctx.arc(cx, cy, r, startAngle, endAngle);
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
  ctx.lineWidth = 14;
  ctx.lineCap = 'round';
  ctx.stroke();
  
  // Section 1: Inevitable Entropy H(P) (In Purple)
  const hpRatio = Math.min(1.0, hp / maxBits);
  const hpAngle = startAngle + hpRatio * (endAngle - startAngle);
  if (hp > 0.01) {
    ctx.beginPath();
    ctx.arc(cx, cy, r, startAngle, hpAngle);
    ctx.strokeStyle = '#a78bfa'; // Purple
    ctx.lineWidth = 14;
    ctx.lineCap = 'round';
    ctx.stroke();
  }
  
  // Section 2: Waste overhead / KL Divergence (In Turquoise/Green)
  const ceRatio = Math.min(1.0, ce / maxBits);
  const ceAngle = startAngle + ceRatio * (endAngle - startAngle);
  if (ce > hp + 0.01) {
    ctx.beginPath();
    ctx.arc(cx, cy, r, hpAngle, ceAngle);
    ctx.strokeStyle = '#4ECDC4'; // Turquoise for waste
    ctx.lineWidth = 14;
    ctx.lineCap = 'round';
    ctx.stroke();
  }
  
  // Ticks and numbers
  ctx.fillStyle = '#64748b';
  ctx.font = 'bold 11px monospace';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  for (let i = 0; i <= maxBits; i += 2) {
    const angle = startAngle + (i / maxBits) * (endAngle - startAngle);
    const tx = cx + (r - 20) * Math.cos(angle);
    const ty = cy + (r - 20) * Math.sin(angle);
    ctx.fillText(i, tx, ty);
    
    ctx.beginPath();
    ctx.moveTo(cx + r * Math.cos(angle), cy + r * Math.sin(angle));
    ctx.lineTo(cx + (r - 6) * Math.cos(angle), cy + (r - 6) * Math.sin(angle));
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
    ctx.lineWidth = 1.5;
    ctx.stroke();
  }
  
  // Dashed boundary line at H(P)
  ctx.save();
  ctx.beginPath();
  ctx.setLineDash([4, 3]);
  ctx.moveTo(cx + (r - 18) * Math.cos(hpAngle), cy + (r - 18) * Math.sin(hpAngle));
  ctx.lineTo(cx + (r + 10) * Math.cos(hpAngle), cy + (r + 10) * Math.sin(hpAngle));
  ctx.strokeStyle = '#c084fc';
  ctx.lineWidth = 2.5;
  ctx.stroke();
  ctx.restore();
  
  // Label for H(P) marker
  if (hp > 0.05) {
    ctx.fillStyle = '#c084fc';
    ctx.font = 'bold 10px sans-serif';
    const lx = cx + (r + 14) * Math.cos(hpAngle);
    const ly = cy + (r + 14) * Math.sin(hpAngle);
    ctx.textAlign = Math.cos(hpAngle) > 0.05 ? 'left' : Math.cos(hpAngle) < -0.05 ? 'right' : 'center';
    ctx.textBaseline = Math.sin(hpAngle) > 0.05 ? 'top' : Math.sin(hpAngle) < -0.05 ? 'bottom' : 'middle';
    ctx.fillText(`H(P) = ${hp.toFixed(1)} bits`, lx, ly);
  }

  // Needle with heat jitter
  let needleAngle = ceAngle;
  if (ce > 6.0) {
    needleAngle += (ce - 5.0) * 0.015 * (Math.random() - 0.5);
  }
  ctx.beginPath();
  ctx.moveTo(cx, cy);
  ctx.lineTo(cx + (r - 6) * Math.cos(needleAngle), cy + (r - 6) * Math.sin(needleAngle));
  ctx.strokeStyle = ce > 7.0 ? '#ef4444' : '#fb7185';
  ctx.lineWidth = 4;
  ctx.lineCap = 'round';
  ctx.stroke();
  
  // Center Pin
  ctx.beginPath();
  ctx.arc(cx, cy, 7, 0, Math.PI * 2);
  ctx.fillStyle = '#1e293b';
  ctx.strokeStyle = '#fb7185';
  ctx.lineWidth = 2.5;
  ctx.fill();
  ctx.stroke();
  
  // Text reads under
  ctx.fillStyle = '#f1f5f9';
  ctx.font = '900 26px monospace';
  ctx.textAlign = 'center';
  const displayVal = ce > 20.0 ? "Infinity 🌋" : ce.toFixed(3);
  ctx.fillText(displayVal, cx, cy + 42);
  
  ctx.fillStyle = '#fb7185';
  ctx.font = 'bold 10px sans-serif';
  ctx.fillText("CROSS-ENTROPY H(P, Q) BITS", cx, cy + 56);
  
  // Small text for component details
  const klDiv = Math.max(0.0, ce - hp);
  ctx.fillStyle = '#94a3b8';
  ctx.font = '700 11px monospace';
  ctx.fillText(`Entropy H(P): ${hp.toFixed(2)} | Waste (KL): ${klDiv > 20 ? "Inf" : klDiv.toFixed(2)} bits`, cx, cy + 70);
  
  // Tag on top
  ctx.fillStyle = '#64748b';
  ctx.font = 'italic 12px sans-serif';
  ctx.fillText(activePName, cx, cy - r - 15);
}

// DRAW BAR CHART (Left and Right Columns)
function drawBars() {
  const rowY = [255, 315, 375];
  const barH = 20;
  const pColors = ['#06b6d4', '#d97706', '#ec4899'];
  const emojis = ['🐱', '🐶', '🐰'];
  const labels = ['CAT', 'DOG', 'RAB'];
  
  for (let i = 0; i < 3; i++) {
    const y = rowY[i];
    
    // Draw Left (Reality P)
    // Label
    ctx.fillStyle = '#94a3b8';
    ctx.font = 'bold 10px monospace';
    ctx.textAlign = 'right';
    ctx.fillText(`${labels[i]} ${emojis[i]}`, 75, y + 14);
    
    // Track backing
    ctx.fillStyle = 'rgba(255, 255, 255, 0.02)';
    ctx.fillRect(85, y, 90, barH);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
    ctx.lineWidth = 1;
    ctx.strokeRect(85, y, 90, barH);
    
    // Active P Bar
    const pW = P[i] * 90;
    if (pW > 0.5) {
      ctx.fillStyle = pColors[i];
      ctx.fillRect(85, y, pW, barH);
    }
    
    // Percentage text
    ctx.fillStyle = '#f8fafc';
    ctx.font = '900 10px monospace';
    ctx.textAlign = 'left';
    ctx.fillText(`${Math.round(P[i]*100)}%`, 180, y + 14);
    
    // --- CONNECTING CHANNEL CABLE ---
    const wireStartX = 210;
    const wireEndX = 390;
    const channelActive = P[i] > 0.001;
    
    ctx.save();
    if (!channelActive) {
      // Dimmest inactive thin wire
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.03)';
      ctx.lineWidth = 1;
      ctx.setLineDash([5, 4]);
      ctx.beginPath();
      ctx.moveTo(wireStartX, y + 10);
      ctx.lineTo(wireEndX, y + 10);
      ctx.stroke();
    } else {
      // Active channel
      const surprise = -log2(Math.max(0.0001, Q[i]));
      let wireColor = pColors[i];
      let thickness = 2.0 + P[i] * 2.5;
      
      // Wire stress effects
      let wireJitterY = 0;
      if (surprise > 3.0) {
        // Redden the wire
        const stressRatio = Math.min(1.0, (surprise - 3.0) / 7.0);
        wireColor = lerpColor(pColors[i], '#ef4444', stressRatio);
        
        // Heat vibration
        wireJitterY = Math.sin(tick * 0.7) * (surprise - 3.0) * 0.8;
        thickness += (surprise - 3.0) * 0.3;
      }
      
      // Draw wire glow
      ctx.shadowBlur = thickness * 2.5;
      ctx.shadowColor = wireColor;
      ctx.strokeStyle = wireColor;
      ctx.lineWidth = thickness;
      ctx.beginPath();
      ctx.moveTo(wireStartX, y + 10 + wireJitterY);
      ctx.lineTo(wireEndX, y + 10 + wireJitterY);
      ctx.stroke();
      ctx.shadowBlur = 0; // reset glow
      
      // Spawn energy particles flowing along active channel
      const baseFlowSpeed = 0.005 + (1.0 - Q[i]) * 0.015; // faster flow if surprise is high (panicked data transmission!)
      
      // Auto-trigger energy particles
      if (Math.random() < P[i] * 0.15) {
        energyParticles.push(new EnergyParticle(i, wireColor));
      }
      
      // Sparks if model is under stress on this class
      if (surprise > 3.0 && Math.random() < (surprise - 3.0) * 0.08) {
        const sx = wireStartX + Math.random() * (wireEndX - wireStartX);
        const sy = y + 10 + wireJitterY;
        for (let sIdx=0; sIdx < Math.floor(surprise - 2); sIdx++) {
          sparks.push(new Spark(sx, sy, wireColor));
        }
      }
      
      // Massive lightning flash inside cable if close to total meltdown
      if (surprise > 8.0 && Math.random() < 0.18) {
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        let curX = wireStartX;
        ctx.moveTo(curX, y + 10);
        while (curX < wireEndX) {
          curX += 8 + Math.random() * 15;
          const lightningJitter = (Math.random() - 0.5) * 8;
          ctx.lineTo(Math.min(wireEndX, curX), y + 10 + lightningJitter);
        }
        ctx.stroke();
      }
    }
    ctx.restore();
    
    // Draw Right (Predicted Q)
    // Track backing
    ctx.fillStyle = 'rgba(255, 255, 255, 0.02)';
    ctx.fillRect(420, y, 90, barH);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
    ctx.lineWidth = 1;
    ctx.strokeRect(420, y, 90, barH);
    
    // Active Q Bar
    const qW = Q[i] * 90;
    if (qW > 0.5) {
      // Glow predicted bar based on confidence
      ctx.fillStyle = pColors[i];
      ctx.fillRect(420, y, qW, barH);
    }
    
    // Percentage text
    ctx.fillStyle = '#f8fafc';
    ctx.font = '900 10px monospace';
    ctx.textAlign = 'right';
    ctx.fillText(`${Math.round(Q[i]*100)}%`, 410, y + 14);
    
    // Predicted label
    ctx.fillStyle = '#94a3b8';
    ctx.font = 'bold 10px monospace';
    ctx.textAlign = 'left';
    ctx.fillText(`Q(${labels[i]})`, 520, y + 14);
  }
}

// Hex color interpolator helper for wire stress
function lerpColor(c1, c2, weight) {
  // convert simple hex codes directly to RGB
  const hex = (x) => {
    const val = x.replace('#', '');
    return {
      r: parseInt(val.substring(0,2), 16),
      g: parseInt(val.substring(2,4), 16),
      b: parseInt(val.substring(4,6), 16)
    };
  };
  const rgb1 = hex(c1);
  const rgb2 = hex(c2);
  
  const r = Math.round(rgb1.r + weight * (rgb2.r - rgb1.r));
  const g = Math.round(rgb1.g + weight * (rgb2.g - rgb1.g));
  const b = Math.round(rgb1.b + weight * (rgb2.b - rgb1.b));
  
  return `rgb(${r},${g},${b})`;
}

// DRAW Dynamic Math Summation Breakdown at the bottom of the canvas
function drawMathSection(ce) {
  const rowY = [255, 315, 375];
  const pColors = ['#22d3ee', '#fbbf24', '#f472b6'];
  const labels = ['Cat', 'Dog', 'Rabbit'];
  
  // Total line
  ctx.fillStyle = '#cbd5e1';
  ctx.font = 'bold 11px monospace';
  ctx.textAlign = 'center';
  ctx.fillText("H(P, Q) = - [ P(Cat)log₂Q(Cat) + P(Dog)log₂Q(Dog) + P(Rabbit)log₂Q(Rabbit) ]", 300, 428);
  
  // active math terms
  let terms = [];
  for (let i = 0; i < 3; i++) {
    const pVal = P[i];
    const qVal = Q[i];
    const surprise = qVal <= 0.000001 ? 13.288 : -log2(qVal); // cap at 13.288 bits
    const contribution = pVal * surprise;
    
    // color coded string segments
    terms.push({
      pStr: pVal.toFixed(2),
      logStr: `log₂(${qVal.toFixed(2)})`,
      contribVal: contribution.toFixed(2),
      color: pColors[i]
    });
  }
  
  // Draw the three color-coded terms in columns
  ctx.font = '900 10px monospace';
  
  // Cat Term
  ctx.fillStyle = terms[0].color;
  ctx.textAlign = 'center';
  ctx.fillText(`${terms[0].pStr} × ${surpriseText(Q[0])} = ${terms[0].contribVal} bits`, 150, 452);
  ctx.font = 'normal 9px sans-serif';
  ctx.fillStyle = '#64748b';
  ctx.fillText("Cat Term Contribution", 150, 464);
  
  // Dog Term
  ctx.font = '900 10px monospace';
  ctx.fillStyle = terms[1].color;
  ctx.fillText(`${terms[1].pStr} × ${surpriseText(Q[1])} = ${terms[1].contribVal} bits`, 300, 452);
  ctx.font = 'normal 9px sans-serif';
  ctx.fillStyle = '#64748b';
  ctx.fillText("Dog Term Contribution", 300, 464);
  
  // Rabbit Term
  ctx.font = '900 10px monospace';
  ctx.fillStyle = terms[2].color;
  ctx.fillText(`${terms[2].pStr} × ${surpriseText(Q[2])} = ${terms[2].contribVal} bits`, 450, 452);
  ctx.font = 'normal 9px sans-serif';
  ctx.fillStyle = '#64748b';
  ctx.fillText("Rabbit Term Contribution", 450, 464);
  
  // Final sum breakdown line
  ctx.font = '900 12px monospace';
  ctx.fillStyle = '#f1f5f9';
  const displayCE = ce > 20.0 ? "Infinity (Meltdown!)" : `${ce.toFixed(2)} bits`;
  ctx.fillText(`Loss Total:  ${terms[0].contribVal} + ${terms[1].contribVal} + ${terms[2].contribVal} = ${displayCE}`, 300, 488);
}

function surpriseText(qVal) {
  if (qVal <= 0.0001) return "Inf";
  return (-log2(qVal)).toFixed(2);
}

// MAIN RENDER LOOP
function draw() {
  tick++;
  
  // Screen Shake effect under meltdown
  const ce = getCrossEntropy(P, Q);
  const hp = getShannonEntropy(P);
  
  const isMeltdown = ce > 7.0;
  canvasWrap.classList.toggle('shake-heavy', isMeltdown);
  
  // Clear
  ctx.fillStyle = '#0f172a';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  
  // Draw sci-fi backing guidelines
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.02)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(300, 200);
  ctx.lineTo(300, 410);
  ctx.stroke();
  
  // Update & Draw Energy Particles
  const rowY = [255, 315, 375];
  for (let i = energyParticles.length - 1; i >= 0; i--) {
    const ep = energyParticles[i];
    const surprise = -log2(Math.max(0.0001, Q[ep.channelIdx]));
    const speed = 0.01 + Math.min(0.04, surprise * 0.003); // faster particles under stress
    ep.update(speed);
    ep.draw(ctx, 210, 390, rowY[ep.channelIdx] + 10);
    if (ep.progress >= 1.0) {
      energyParticles.splice(i, 1);
    }
  }
  
  // Update & Draw Sparks
  for (let i = sparks.length - 1; i >= 0; i--) {
    const sp = sparks[i];
    sp.update();
    sp.draw(ctx);
    if (sp.life <= 0) {
      sparks.splice(i, 1);
    }
  }
  
  // Draw primary components
  drawGauge(300, 105, 68, ce, hp);
  drawBars();
  drawMathSection(ce);
  
  // Alert visual overlays if extreme
  if (isMeltdown && tick % 30 < 15) {
    ctx.fillStyle = 'rgba(239, 68, 68, 0.05)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = '#ef4444';
    ctx.font = 'bold 9px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText("⚠️ CRITICAL CROSS-ENTROPY MELTDOWN: OVERCONFIDENT WRONG PREDICTION ⚠️", 300, 220);
  }
  
  requestAnimationFrame(draw);
}

// Initialization
buildSliders();
draw();

</script>
</body>
</html>
"""
    components.html(html_code, height=790, scrolling=False)

def main():
    st.title("🌋 Page 59: Cross-Entropy — Predicted vs Reality")

    st.markdown(
        """
        In [Page 58: Entropy — Average Uncertainty](file:///d:/physics-simulation/pages/58Entropy%20%E2%80%94%20Average%20Uncertainty.py), we learned how to measure the **average uncertainty** ($H(P)$) of a real-world system. 
        But in Artificial Intelligence, we don't just sit back and watch reality. We make **predictions ($Q$)** using neural networks and cross-reference them with **reality ($P$)**.
        
        **Cross-Entropy ($H(P, Q)$)** is the ultimate penalty compass. It measures the **average surprise** you experience when you expect outcomes based on your prediction beliefs $Q$, but reality hits you with facts governed by $P$!
        """
    )

    st.divider()

    col1, col2 = st.columns([1.1, 0.9])

    with col1:
        st.subheader("The Mathematics of Surprise Mismatch 🧮")
        st.markdown(
            r"""
            For a target distribution $P$ (the true label probability) and predicted distribution $Q$ (the model's probabilities), the **Cross-Entropy** $H(P, Q)$ is defined as:
            
            $$H(P, Q) = -\sum_{i=1}^n P(x_i) \log_2(Q(x_i))$$
            
            * **Single-Label Classification (One-Hot):** If the true class is definitely a **Cat** (so $P(\text{Cat})=1$, and all others are $0$), the entire formula collapses down to exactly one term:
              $$H(P, Q) = -\log_2(Q(x_{\text{correct}}))$$
              This is exactly the **surprise of the correct class** under the model's prediction!
            * **Gibbs' Inequality:** Cross-Entropy is mathematically guaranteed to be **greater than or equal to** the Shannon Entropy of reality:
              $$H(P, Q) \ge H(P)$$
              The extra cost is called **Kullback-Leibler (KL) Divergence**:
              $$\underbrace{H(P, Q)}_{\text{Cross-Entropy}} = \underbrace{H(P)}_{\text{Inevitable Entropy}} + \underbrace{D_{KL}(P \parallel Q)}_{\text{Imperfect Coding Waste}}$$
            """
        )

    with col2:
        st.subheader("Interactive Lessons & Warnings 🌋")
        st.success("🎯 **The Optimal Ideal (No Waste):** When your predictions $Q$ align *perfectly* with reality $P$ ($Q = P$), the waste drops to exactly zero ($D_{KL} = 0$). The Cross-Entropy is minimized and matches $H(P)$!")
        st.info("🤷 **The Naive Ignorance baseline:** If a model initializes as a uniform split (33% each for 3 classes), its Cross-Entropy is a moderate, predictable $1.585\text{ bits}$ regardless of the true label.")
        st.error("💥 **The Confident Wrong Meltdown:** If you predict a class has near-zero probability (e.g. $Q(\text{Cat}) = 0.01\%$), but reality declares it is indeed a **Cat**, the surprise penalty $-\log_2(0.0001)$ explodes to **$13.29\text{ bits}$**! This heavily punishes overconfidence.")

    st.divider()
    st.markdown("### 🧪 The Cross-Entropy Meltdown Laboratory")
    st.markdown(
        "Experiment with reality $P$ and prediction $Q$ live! "
        "Use **Reality Mode** to select standard one-hot label states (like pure Cat) or soft targets (Label Smoothing). "
        "Drag the **Q sliders** to adjust model predictions. Watch how the **waste (KL Divergence)** region grows on the dial as predictions deviate, "
        "and witness a literal **Meltdown** when the network is highly confident in the wrong outcome!"
    )

    render_cross_entropy_lab()

    st.divider()
    st.subheader("🤖 Bridge to AI: Why Classifiers Love Cross-Entropy")
    st.markdown(
        r"""
        Cross-entropy is the standard loss function for training almost all deep learning classifiers (like ResNet, BERT, or GPT-4). Here is the deep engineering intuition:
        
        #### 1. Why Not Mean Squared Error (MSE) for Classification? 📉
        If we trained classifiers using squared error, when the network is confident and wrong, the derivatives of the sigmoid or softmax activation functions become extremely small (called **gradient saturation**). The model stops learning!
        
        Cross-entropy solves this. Because its value asymptotic-sweeps to **infinity** when $Q(\text{correct}) \to 0$, the mathematical gradient remains extremely strong:
        $$\frac{\partial H(P, Q)}{\partial z_i} = Q(x_i) - P(x_i)$$
        This gradient is incredibly elegant: it is simply the **prediction error** (prediction minus reality)! The larger the mistake, the harder the network is pushed to self-correct!
        
        #### 2. Label Smoothing: The Art of Preventative Humility 🐾
        In modern AI (e.g., training state-of-the-art vision models), we often prevent models from becoming overly confident by slightly "softening" target labels:
        $$P = [0.90, 0.05, 0.05] \quad \text{instead of} \quad [1.0, 0.0, 0.0]$$
        This is called **Label Smoothing**. As you saw in the laboratory, soft reality targets have an inherent entropy $H(P) > 0$. By forcing the target to be soft, the model is penalized if it drives its predictions $Q$ to extreme $100\%$ confidence! This acts as a powerful regularizer, leading to better generalization and preventing overfitting!
        """
    )

    st.divider()
    st.markdown(
        '<div style="color:#94a3b8;font-size:0.95rem;">Page 59 — you\'ve mastered how Cross-Entropy penalizes the distance between reality and expectation, and how it drives classification gradients. But what happens when we isolate just the "excess waste" component of this mismatch? Next: we zoom into the core distance metric of probability distributions — <b>KL Divergence (Page 60)</b>!</div>',
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
