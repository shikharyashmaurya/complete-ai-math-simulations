import streamlit as st
import streamlit.components.v1 as components
import numpy as np

st.set_page_config(page_title="KL Divergence — Gap Between Distributions", layout="wide")

def render_kl_divergence_lab():
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
  background: rgba(30, 41, 59, 0.45);
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
  background: rgba(6, 182, 212, 0.16);
  border-color: #06b6d4;
  color: #06b6d4;
  box-shadow: 0 0 12px rgba(6, 182, 212, 0.25);
}

.mbtn.active.reverse-kl {
  background: rgba(244, 114, 182, 0.16);
  border-color: #f472b6;
  color: #f472b6;
  box-shadow: 0 0 12px rgba(244, 114, 182, 0.25);
}

/* Custom Grid for presets */
.preset-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 6px;
  margin-top: 5px;
}
.preset-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 10px;
  padding: 8px 4px;
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
.preset-card .emoji { font-size: 18px; }
.preset-card .name { font-size: 10px; font-weight: 700; color: #e2e8f0; line-height: 1.1; }
.preset-card .desc { font-size: 8px; color: #94a3b8; }

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
  font-size: 13px;
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
  width: 15px;
  height: 15px;
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.1s;
}
input[type=range]::-webkit-slider-thumb:hover {
  transform: scale(1.25);
}

/* Colors for sliders */
input.p-slider::-webkit-slider-thumb { background: #06b6d4; box-shadow: 0 0 8px #06b6d4; }
input.q-slider::-webkit-slider-thumb { background: #fbbf24; box-shadow: 0 0 8px #fbbf24; }

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
  animation: shake 0.12s infinite alternate;
}
@keyframes shake {
  0% { transform: translate(1.5px, 1.5px) rotate(0deg); }
  100% { transform: translate(-1.5px, -1.5px) rotate(0.2deg); }
}

.options-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 5px;
}
.option-select {
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #f8fafc;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 6px;
  outline: none;
  cursor: pointer;
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
        <h2>KL Divergence Lab 🔬</h2>
        <p class="sub">Quantify the information gap between two probability distributions live! Toggle Forward or Reverse KL to watch sample droplets drop, waves ripple, and the asymmetry reveal itself.</p>
      </div>

      <!-- Presets Selector -->
      <div class="card">
        <div class="slabel-row" style="margin-bottom:2px;">
          <span>Select Distribution Preset</span>
        </div>
        <div class="preset-grid">
          <div class="preset-card active" id="preset-perfect" onclick="setPreset('perfect')">
            <span class="emoji">🎯</span>
            <span class="name">Twins</span>
            <span class="desc">D_KL = 0</span>
          </div>
          <div class="preset-card" id="preset-drift" onclick="setPreset('drift')">
            <span class="emoji">🌁</span>
            <span class="name">Slight Drift</span>
            <span class="desc">Moderate</span>
          </div>
          <div class="preset-card" id="preset-narrow" onclick="setPreset('narrow')">
            <span class="emoji">🔍</span>
            <span class="name">Narrow Q</span>
            <span class="desc">Exploded</span>
          </div>
          <div class="preset-card" id="preset-wide" onclick="setPreset('wide')">
            <span class="emoji">🛡️</span>
            <span class="name">Wide Q</span>
            <span class="desc">Safe Cover</span>
          </div>
          <div class="preset-card" id="preset-separated" onclick="setPreset('separated')">
            <span class="emoji">🌋</span>
            <span class="name">Separated</span>
            <span class="desc">Meltdown</span>
          </div>
        </div>
      </div>

      <!-- Parameters Sliders -->
      <div class="card">
        <div class="slabel-row" style="margin-bottom:6px;">
          <span style="color:#06b6d4;">Reality Target Distribution P(x)</span>
        </div>
        <div class="slider-container">
          <div class="slider-row">
            <div class="slabel-row">
              <span>Mean (μ_P)</span>
              <span class="sval" style="color: #06b6d4;" id="muP-val">0.0</span>
            </div>
            <input type="range" class="p-slider" id="muP-slider" min="-4.0" max="4.0" step="0.1" value="0.0" oninput="onMuPChange(this.value)">
          </div>
          <div class="slider-row">
            <div class="slabel-row">
              <span>Std Dev (σ_P)</span>
              <span class="sval" style="color: #06b6d4;" id="sigmaP-val">1.00</span>
            </div>
            <input type="range" class="p-slider" id="sigmaP-slider" min="0.3" max="2.5" step="0.05" value="1.0" oninput="onSigmaPChange(this.value)">
          </div>
        </div>
      </div>

      <div class="card">
        <div class="slabel-row" style="margin-bottom:6px;">
          <span style="color:#fbbf24;">Model Approximating Distribution Q(x)</span>
        </div>
        <div class="slider-container">
          <div class="slider-row">
            <div class="slabel-row">
              <span>Mean (μ_Q)</span>
              <span class="sval" style="color: #fbbf24;" id="muQ-val">1.0</span>
            </div>
            <input type="range" class="q-slider" id="muQ-slider" min="-4.0" max="4.0" step="0.1" value="1.0" oninput="onMuQChange(this.value)">
          </div>
          <div class="slider-row">
            <div class="slabel-row">
              <span>Std Dev (σ_Q)</span>
              <span class="sval" style="color: #fbbf24;" id="sigmaQ-val">1.00</span>
            </div>
            <input type="range" class="q-slider" id="sigmaQ-slider" min="0.3" max="2.5" step="0.05" value="1.0" oninput="onSigmaQChange(this.value)">
          </div>
        </div>
      </div>

      <!-- Simulation Options -->
      <div class="card">
        <div class="slabel-row" style="margin-bottom:6px;">
          <span>Interactive Monte Carlo Sampler</span>
        </div>
        <div class="mode-row" style="margin-bottom: 8px;">
          <button class="mbtn active" id="btn-forward-kl" onclick="setSimulationMode('forward')">Forward KL: D_KL(P || Q)</button>
          <button class="mbtn" id="btn-reverse-kl" onclick="setSimulationMode('reverse')">Reverse KL: D_KL(Q || P)</button>
        </div>
        <div class="options-row">
          <span class="sub" style="font-weight:700;">Drop Rate:</span>
          <select class="option-select" id="select-rate" onchange="onRateChange(this.value)">
            <option value="none">⏸️ Paused</option>
            <option value="slow">🐢 Slow (2/s)</option>
            <option value="normal" selected>⚡ Normal (6/s)</option>
            <option value="fast">🚀 High-Speed (15/s)</option>
          </select>
        </div>
      </div>

      <!-- Retro Terminal Log -->
      <div class="terminal-log" id="log-box">
        <div class="log-line">> <span class="cyan">KL Divergence Laboratory successfully booted.</span></div>
      </div>
    </div>

    <!-- RIGHT PANEL: Animated Visualization Canvas -->
    <div class="panel-right">
      <div id="canvas-wrap">
        <canvas id="viz-canvas" width="620" height="520"></canvas>
      </div>
    </div>
  </div>
</div>

<script>
const canvas = document.getElementById('viz-canvas');
const ctx = canvas.getContext('2d');
const logBox = document.getElementById('log-box');
const canvasWrap = document.getElementById('canvas-wrap');

// High-DPI / Retina Canvas Scaling
const CANVAS_WIDTH = 620;
const CANVAS_HEIGHT = 520;
const dpr = Math.min(window.devicePixelRatio || 1, 2);
canvas.style.width = '100%';
canvas.style.height = 'auto';
canvas.width = CANVAS_WIDTH * dpr;
canvas.height = CANVAS_HEIGHT * dpr;
ctx.scale(dpr, dpr);
let animationFrame = null;

function requestDraw() {
  if (animationFrame === null) animationFrame = requestAnimationFrame(draw);
}

// State Variables
let muP = 0.0;
let sigmaP = 1.0;
let muQ = 1.0;
let sigmaQ = 1.0;

let simulationMode = 'forward'; // 'forward' = D_KL(P || Q), 'reverse' = D_KL(Q || P)
let dropRate = 'normal'; // 'none', 'slow', 'normal', 'fast'

let droplets = [];
let bubbles = [];
let sparks = [];
let sampleHistory = []; // last 100 samples
const maxHistorySize = 100;
let tick = 0;

// Coordinate Mapping Layout Constants
const plotXMin = 50;
const plotXMax = 460;
const plotWidth = plotXMax - plotXMin;

const plotYMin1 = 40;
const plotYMax1 = 200;
const plotHeight1 = plotYMax1 - plotYMin1;

const plotYMin2 = 270;
const plotYMax2 = 430;
const plotHeight2 = plotYMax2 - plotYMin2;
const plotYBaseline2 = 350; // midpoint of integrand graph

// Retro Terminal Logger
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

// Math Utility Functions
function gaussianLogPdf(x, mu, sigma) {
  const z = (x - mu) / sigma;
  return -0.5 * z * z - Math.log(sigma) - 0.5 * Math.log(2 * Math.PI);
}

function gaussianPdf(x, mu, sigma) {
  return Math.exp(gaussianLogPdf(x, mu, sigma));
}

function getKlDivergence(mu1, sigma1, mu2, sigma2) {
  // Analytical D_KL(N(mu1, sigma1^2) || N(mu2, sigma2^2)) in bits
  const s1_sq = sigma1 * sigma1;
  const s2_sq = sigma2 * sigma2;
  const term1 = Math.log(sigma2 / sigma1);
  const term2 = (s1_sq + Math.pow(mu1 - mu2, 2)) / (2 * s2_sq);
  const term3 = -0.5;
  const klNats = term1 + term2 + term3;
  return klNats / Math.LN2;
}

function getIntegrand(x, mu1, sigma1, mu2, sigma2) {
  // If simulation is Forward: P(x) * log2(P(x) / Q(x))
  // If simulation is Reverse: Q(x) * log2(Q(x) / P(x))
  const logP = gaussianLogPdf(x, muP, sigmaP);
  const logQ = gaussianLogPdf(x, muQ, sigmaQ);
  const logDensity = simulationMode === 'forward' ? logP : logQ;
  const density = Math.exp(logDensity);
  if (density === 0 || !Number.isFinite(density)) return 0;

  const logRatio = simulationMode === 'forward' ? logP - logQ : logQ - logP;
  if (!Number.isFinite(logRatio)) return 0;
  return density * logRatio / Math.LN2;
}

// Box-Muller Transform for Sampling
function sampleGaussian(mu, sigma) {
  let u1 = 0, u2 = 0;
  while (u1 === 0) u1 = Math.random();
  while (u2 === 0) u2 = Math.random();
  const z0 = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
  return z0 * sigma + mu;
}

// Coordinate mapping helpers
function mapX(val) {
  const pct = (val + 6) / 12; // domain [-6, 6]
  return plotXMin + pct * plotWidth;
}

function mapYPdf(val) {
  // Cap at height 1.2 for layout
  const pct = Math.min(1.2, val) / 1.2;
  return plotYMax1 - pct * plotHeight1;
}

function mapYIntegrand(val) {
  // val range roughly [-1.0, 3.0]
  if (val >= 0) {
    const pct = Math.min(3.0, val) / 3.0;
    return plotYBaseline2 - pct * (plotYBaseline2 - plotYMin2);
  } else {
    const pct = Math.max(-1.0, val) / -1.0;
    return plotYBaseline2 + pct * (plotYMax2 - plotYBaseline2);
  }
}

// Particles & Droplets Physics Classes
class Droplet {
  constructor(startX, startY, sampledX, value) {
    this.x = startX;
    this.y = startY;
    this.sampledX = sampledX;
    this.value = value;
    this.vy = 2.5 + Math.random() * 2.0;
    this.state = 'dropping'; // 'dropping' or 'flying'
    this.size = 3.5 + Math.random() * 1.5;
  }
  
  update(targetX, targetY) {
    if (isNaN(this.x) || isNaN(this.y)) {
      return true; // remove immediately
    }
    if (this.state === 'dropping') {
      this.y += this.vy;
      if (this.y >= plotYBaseline2) {
        this.state = 'flying';
        // Spawn floating text bubble
        if (bubbles.length < 100) {
          bubbles.push(new Bubble(this.x, plotYBaseline2 - 8, this.value));
        }
      }
    } else if (this.state === 'flying') {
      const dx = targetX - this.x;
      const dy = targetY - this.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 10 || isNaN(dist) || dist > 1000) {
        return true; // Hit target or out of bounds / NaN
      }
      const speed = 7.0;
      this.x += (dx / dist) * speed;
      this.y += (dy / dist) * speed;
    }
    return false;
  }
  
  draw(c, color) {
    c.save();
    c.beginPath();
    c.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    c.fillStyle = color;
    c.shadowBlur = 6;
    c.shadowColor = color;
    c.fill();
    c.restore();
  }
}

class Bubble {
  constructor(x, y, val) {
    this.x = x;
    this.y = y;
    this.val = val;
    this.text = (val >= 0 ? "+" : "") + val.toFixed(1);
    this.vy = -0.7 - Math.random() * 0.5;
    this.alpha = 1.0;
    this.color = val >= 2.0 ? '#ef4444' : (val >= 0 ? '#06b6d4' : '#10b981');
  }
  
  update() {
    if (isNaN(this.x) || isNaN(this.y)) {
      this.alpha = 0;
      return;
    }
    this.y += this.vy;
    this.alpha -= 0.02;
  }
  
  draw(c) {
    c.save();
    c.globalAlpha = this.alpha;
    c.fillStyle = this.color;
    c.font = 'bold 9px monospace';
    c.textAlign = 'center';
    c.fillText(this.text, this.x, this.y);
    c.restore();
  }
}

class Spark {
  constructor(x, y, color) {
    this.x = x;
    this.y = y;
    const angle = Math.random() * Math.PI * 2;
    const speed = 1.0 + Math.random() * 3.5;
    this.vx = Math.cos(angle) * speed;
    this.vy = Math.sin(angle) * speed - 0.5;
    this.size = 1.0 + Math.random() * 2.0;
    this.life = 15 + Math.random() * 20;
    this.maxLife = this.life;
    this.color = color;
  }
  
  update() {
    if (isNaN(this.x) || isNaN(this.y)) {
      this.life = 0;
      return;
    }
    this.x += this.vx;
    this.y += this.vy;
    this.vy += 0.06; // gravity
    this.life--;
  }
  
  draw(c) {
    const alpha = Math.max(0, this.life / this.maxLife);
    c.save();
    c.globalAlpha = alpha;
    c.beginPath();
    c.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    c.fillStyle = this.color;
    c.shadowBlur = 4;
    c.shadowColor = this.color;
    c.fill();
    c.restore();
  }
}

// Preset Handler
function setPreset(name) {
  sampleHistory = []; // Clear empirical average history
  
  const cards = document.querySelectorAll('.preset-card');
  cards.forEach(c => c.classList.remove('active'));
  document.getElementById(`preset-${name}`).classList.add('active');
  
  if (name === 'perfect') {
    muP = 0.0; sigmaP = 1.0;
    muQ = 0.0; sigmaQ = 1.0;
    addLog("Twins Loaded. D_KL = 0.00. Identical distributions have zero extra coding surprise!", "info");
  } else if (name === 'drift') {
    muP = -0.8; sigmaP = 1.0;
    muQ = 0.8; sigmaQ = 1.0;
    addLog("Slight Drift Loaded. Standard variance, simple mean shift. Notice the symmetric D_KL behavior.", "info");
  } else if (name === 'narrow') {
    muP = 0.0; sigmaP = 1.4;
    muQ = 0.0; sigmaQ = 0.5;
    addLog("Narrow Q (Tail Blind). Model misses Reality's wide tails. Infinitely penalizing Forward KL!", "warn");
  } else if (name === 'wide') {
    muP = 0.0; sigmaP = 0.5;
    muQ = 0.0; sigmaQ = 1.4;
    addLog("Wide Q (Safe Cover). Model covers Reality safely. Forward KL is small; Reverse KL is large.", "gold");
  } else if (name === 'separated') {
    muP = -2.3; sigmaP = 0.7;
    muQ = 2.3; sigmaQ = 0.7;
    addLog("Separated Worlds. Extremely poor overlap. Massive information gap in both directions!", "warn");
  }
  
  updateSlidersUI();
  updatePresetHighlights();
  requestDraw();
}

// Manual Sliders State Synchronizers
function onMuPChange(val) {
  muP = parseFloat(val);
  sampleHistory = [];
  document.getElementById('muP-val').innerText = muP.toFixed(1);
  updatePresetHighlights();
  requestDraw();
}
function onSigmaPChange(val) {
  sigmaP = parseFloat(val);
  sampleHistory = [];
  document.getElementById('sigmaP-val').innerText = sigmaP.toFixed(2);
  updatePresetHighlights();
  requestDraw();
}
function onMuQChange(val) {
  muQ = parseFloat(val);
  sampleHistory = [];
  document.getElementById('muQ-val').innerText = muQ.toFixed(1);
  updatePresetHighlights();
  requestDraw();
}
function onSigmaQChange(val) {
  sigmaQ = parseFloat(val);
  sampleHistory = [];
  document.getElementById('sigmaQ-val').innerText = sigmaQ.toFixed(2);
  updatePresetHighlights();
  requestDraw();
}

function updateSlidersUI() {
  document.getElementById('muP-slider').value = muP;
  document.getElementById('muP-val').innerText = muP.toFixed(1);
  document.getElementById('sigmaP-slider').value = sigmaP;
  document.getElementById('sigmaP-val').innerText = sigmaP.toFixed(2);
  
  document.getElementById('muQ-slider').value = muQ;
  document.getElementById('muQ-val').innerText = muQ.toFixed(1);
  document.getElementById('sigmaQ-slider').value = sigmaQ;
  document.getElementById('sigmaQ-val').innerText = sigmaQ.toFixed(2);
}

function updatePresetHighlights() {
  const isPerfect = Math.abs(muP - 0.0) < 0.05 && Math.abs(sigmaP - 1.0) < 0.05 && Math.abs(muQ - 0.0) < 0.05 && Math.abs(sigmaQ - 1.0) < 0.05;
  const isDrift = Math.abs(muP - (-0.8)) < 0.05 && Math.abs(sigmaP - 1.0) < 0.05 && Math.abs(muQ - 0.8) < 0.05 && Math.abs(sigmaQ - 1.0) < 0.05;
  const isNarrow = Math.abs(muP - 0.0) < 0.05 && Math.abs(sigmaP - 1.4) < 0.05 && Math.abs(muQ - 0.0) < 0.05 && Math.abs(sigmaQ - 0.5) < 0.05;
  const isWide = Math.abs(muP - 0.0) < 0.05 && Math.abs(sigmaP - 0.5) < 0.05 && Math.abs(muQ - 0.0) < 0.05 && Math.abs(sigmaQ - 1.4) < 0.05;
  const isSeparated = Math.abs(muP - (-2.3)) < 0.05 && Math.abs(sigmaP - 0.7) < 0.05 && Math.abs(muQ - 2.3) < 0.05 && Math.abs(sigmaQ - 0.7) < 0.05;
  
  const cards = document.querySelectorAll('.preset-card');
  cards.forEach(c => c.classList.remove('active'));
  
  if (isPerfect) document.getElementById('preset-perfect').classList.add('active');
  else if (isDrift) document.getElementById('preset-drift').classList.add('active');
  else if (isNarrow) document.getElementById('preset-narrow').classList.add('active');
  else if (isWide) document.getElementById('preset-wide').classList.add('active');
  else if (isSeparated) document.getElementById('preset-separated').classList.add('active');
}

// Controller functions
function setSimulationMode(mode) {
  simulationMode = mode;
  sampleHistory = [];
  
  const btnF = document.getElementById('btn-forward-kl');
  const btnR = document.getElementById('btn-reverse-kl');
  
  btnF.classList.toggle('active', mode === 'forward');
  btnR.classList.toggle('active', mode === 'reverse');
  btnR.classList.toggle('reverse-kl', mode === 'reverse');
  
  addLog(`Switched to ${mode === 'forward' ? 'Forward' : 'Reverse'} KL. Sampling active distribution...`, 'cyan');
  requestDraw();
}

function onRateChange(val) {
  dropRate = val;
  sampleHistory = [];
  addLog(`Droplet drop rate changed to: ${val}`, 'cyan');
  requestDraw();
}

// Spark explosion
function triggerSparks(x, y, color) {
  if (sparks.length < 300) {
    for (let i = 0; i < 6; i++) {
      sparks.push(new Spark(x, y, color));
    }
  }
}

// PRIMARY CANVAS RENDER METHODS
function drawAxesAndGrid() {
  // Upper Graph Grid
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.03)';
  ctx.lineWidth = 1;
  for (let hVal = 0.2; hVal <= 1.0; hVal += 0.2) {
    const yPos = mapYPdf(hVal);
    ctx.beginPath();
    ctx.moveTo(plotXMin, yPos);
    ctx.lineTo(plotXMax, yPos);
    ctx.stroke();
    
    // Label y-axis
    ctx.fillStyle = '#475569';
    ctx.font = '8px monospace';
    ctx.textAlign = 'right';
    ctx.fillText(hVal.toFixed(1), plotXMin - 6, yPos + 3);
  }
  
  // Lower Graph Grid
  for (let vVal of [-0.5, 1.0, 2.0]) {
    const yPos = mapYIntegrand(vVal);
    ctx.beginPath();
    ctx.moveTo(plotXMin, yPos);
    ctx.lineTo(plotXMax, yPos);
    ctx.stroke();
    
    ctx.fillStyle = '#475569';
    ctx.font = '8px monospace';
    ctx.textAlign = 'right';
    ctx.fillText((vVal >= 0 ? "+" : "") + vVal.toFixed(1), plotXMin - 6, yPos + 3);
  }
  
  // Baselines
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
  ctx.lineWidth = 1;
  
  ctx.beginPath();
  ctx.moveTo(plotXMin, plotYMax1);
  ctx.lineTo(plotXMax, plotYMax1);
  ctx.stroke();
  
  ctx.beginPath();
  ctx.moveTo(plotXMin, plotYBaseline2);
  ctx.lineTo(plotXMax, plotYBaseline2);
  ctx.stroke();
  
  // Draw x-axis tick marks
  ctx.fillStyle = '#64748b';
  ctx.font = '9px monospace';
  ctx.textAlign = 'center';
  for (let v = -6; v <= 6; v += 2) {
    const cx = mapX(v);
    
    // Upper ticks
    ctx.fillText(v, cx, plotYMax1 + 10);
    ctx.beginPath();
    ctx.moveTo(cx, plotYMax1);
    ctx.lineTo(cx, plotYMax1 + 4);
    ctx.stroke();
    
    // Lower ticks
    ctx.fillText(v, cx, plotYBaseline2 + 10);
    ctx.beginPath();
    ctx.moveTo(cx, plotYBaseline2);
    ctx.lineTo(cx, plotYBaseline2 + 4);
    ctx.stroke();
  }
}

function drawPdfCurves() {
  ctx.save();
  
  // P(x) Curve - CYAN
  ctx.beginPath();
  ctx.moveTo(mapX(-6), plotYMax1);
  for (let xVal = -6; xVal <= 6; xVal += 0.05) {
    const p = gaussianPdf(xVal, muP, sigmaP);
    ctx.lineTo(mapX(xVal), mapYPdf(p));
  }
  ctx.lineTo(mapX(6), plotYMax1);
  ctx.closePath();
  ctx.fillStyle = 'rgba(6, 182, 212, 0.14)';
  ctx.fill();
  
  ctx.strokeStyle = '#06b6d4';
  ctx.lineWidth = 2.5;
  ctx.shadowBlur = 8;
  ctx.shadowColor = '#06b6d4';
  ctx.stroke();
  ctx.shadowBlur = 0;
  
  // Q(x) Curve - AMBER
  ctx.beginPath();
  ctx.moveTo(mapX(-6), plotYMax1);
  for (let xVal = -6; xVal <= 6; xVal += 0.05) {
    const q = gaussianPdf(xVal, muQ, sigmaQ);
    ctx.lineTo(mapX(xVal), mapYPdf(q));
  }
  ctx.lineTo(mapX(6), plotYMax1);
  ctx.closePath();
  ctx.fillStyle = 'rgba(251, 191, 36, 0.12)';
  ctx.fill();
  
  ctx.strokeStyle = '#fbbf24';
  ctx.lineWidth = 2.5;
  ctx.shadowBlur = 8;
  ctx.shadowColor = '#fbbf24';
  ctx.stroke();
  ctx.shadowBlur = 0;
  
  // Draw peak mean lines
  ctx.setLineDash([3, 3]);
  ctx.lineWidth = 1;
  
  ctx.strokeStyle = 'rgba(6, 182, 212, 0.5)';
  ctx.beginPath();
  ctx.moveTo(mapX(muP), mapYPdf(gaussianPdf(muP, muP, sigmaP)));
  ctx.lineTo(mapX(muP), plotYMax1);
  ctx.stroke();
  
  ctx.strokeStyle = 'rgba(251, 191, 36, 0.5)';
  ctx.beginPath();
  ctx.moveTo(mapX(muQ), mapYPdf(gaussianPdf(muQ, muQ, sigmaQ)));
  ctx.lineTo(mapX(muQ), plotYMax1);
  ctx.stroke();
  
  // Labels
  ctx.fillStyle = '#06b6d4';
  ctx.font = 'bold 9px monospace';
  ctx.textAlign = 'center';
  ctx.fillText(`μ_P=${muP.toFixed(1)}`, mapX(muP), plotYMax1 - 4);
  
  ctx.fillStyle = '#fbbf24';
  ctx.fillText(`μ_Q=${muQ.toFixed(1)}`, mapX(muQ), plotYMax1 - 14);
  
  ctx.restore();
}

function drawIntegrandBars() {
  const step = 0.08;
  const barWidth = 2.0;
  ctx.save();
  
  for (let xVal = -6; xVal <= 6; xVal += step) {
    const val = getIntegrand(xVal, muP, sigmaP, muQ, sigmaQ);
    const cx = mapX(xVal);
    const cy = mapYIntegrand(val);
    
    const color = val >= 0 ? '#ef4444' : '#10b981'; // positive surprise is red/coral; negative surprise reduction is emerald
    
    // Core bar
    ctx.strokeStyle = color;
    ctx.lineWidth = barWidth;
    ctx.beginPath();
    ctx.moveTo(cx, plotYBaseline2);
    ctx.lineTo(cx, cy);
    ctx.stroke();
    
    // Extra backing glow
    ctx.strokeStyle = val >= 0 ? 'rgba(239, 68, 68, 0.12)' : 'rgba(16, 185, 129, 0.12)';
    ctx.lineWidth = barWidth * 2;
    ctx.beginPath();
    ctx.moveTo(cx, plotYBaseline2);
    ctx.lineTo(cx, cy);
    ctx.stroke();
  }
  ctx.restore();
}

function drawLiquidTanks(klPQ, klQP) {
  const tkW = 34;
  const tkH = 220;
  const tkY = 100;
  
  const tanks = [
    { x: 495, val: klPQ, colorStart: '#06b6d4', colorEnd: '#10b981', label: 'FORWARD D_KL', sub: 'P || Q (Reality ➔ Model)' },
    { x: 555, val: klQP, colorStart: '#a78bfa', colorEnd: '#f472b6', label: 'REVERSE D_KL', sub: 'Q || P (Model ➔ Reality)' }
  ];
  
  tanks.forEach((tk, idx) => {
    // 1. Frame Backing
    ctx.fillStyle = 'rgba(255, 255, 255, 0.02)';
    ctx.fillRect(tk.x, tkY, tkW, tkH);
    
    // Glass boundary
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
    ctx.lineWidth = 2.5;
    ctx.strokeRect(tk.x, tkY, tkW, tkH);
    
    // 2. Compute Fluid Fill Pct (Cap at 8.0 bits max height)
    const fillPct = Math.min(8.0, tk.val) / 8.0;
    const fluidH = fillPct * tkH;
    const surfaceY = tkY + tkH - fluidH;
    
    if (fluidH > 0.5) {
      ctx.save();
      // Wave shader algorithm
      ctx.beginPath();
      ctx.moveTo(tk.x + 1.5, surfaceY);
      
      for (let tx = 0; tx <= tkW - 3; tx++) {
        // Sine wave ripple based on time (tick)
        const waveJitter = Math.sin(tick * 0.07 + tx * 0.25) * 2.2 * Math.min(1.0, fillPct * 5.0);
        ctx.lineTo(tk.x + 1.5 + tx, surfaceY + waveJitter);
      }
      ctx.lineTo(tk.x + tkW - 1.5, tkY + tkH);
      ctx.lineTo(tk.x + 1.5, tkY + tkH);
      ctx.closePath();
      
      // Dynamic colors based on values: normal -> warning -> meltdown
      let gradient = ctx.createLinearGradient(tk.x, surfaceY, tk.x, tkY + tkH);
      if (tk.val < 3.0) {
        gradient.addColorStop(0, tk.colorStart);
        gradient.addColorStop(1, tk.colorEnd);
      } else if (tk.val < 6.0) {
        gradient.addColorStop(0, '#f59e0b');
        gradient.addColorStop(1, '#d97706');
      } else {
        // Exploded / Meltdown flashing color
        const meltPulse = Math.sin(tick * 0.15) * 0.2 + 0.8;
        gradient.addColorStop(0, `rgba(239, 68, 68, ${meltPulse})`);
        gradient.addColorStop(1, 'rgba(127, 29, 29, 0.9)');
      }
      
      ctx.fillStyle = gradient;
      ctx.fill();
      ctx.restore();
      
      // Floating bubbles inside fluid
      ctx.fillStyle = 'rgba(255, 255, 255, 0.22)';
      for (let b = 0; b < 2; b++) {
        const bx = tk.x + 4 + ((tick + b * 25) % (tkW - 8));
        const by = tkY + tkH - ((tick * 0.4 + b * 50) % fluidH);
        ctx.beginPath();
        ctx.arc(bx, by, 1 + (b % 2), 0, Math.PI * 2);
        ctx.fill();
      }
    }
    
    // Crack overlay if highly stressed
    if (tk.val > 5.5) {
      ctx.save();
      ctx.strokeStyle = tk.val > 7.2 ? 'rgba(239, 68, 68, 0.45)' : 'rgba(255, 255, 255, 0.2)';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      // Lighting bolts representing cracked glass
      ctx.moveTo(tk.x, tkY + 50);
      ctx.lineTo(tk.x + tkW/2, tkY + 65);
      ctx.lineTo(tk.x + tkW, tkY + 58);
      ctx.moveTo(tk.x + tkW, tkY + 120);
      ctx.lineTo(tk.x + tkW/3, tkY + 138);
      ctx.lineTo(tk.x + 2, tkY + 130);
      ctx.stroke();
      ctx.restore();
    }
    
    // 3. Texts and Titles
    // Value on top (Glow if active/stressed)
    ctx.textAlign = 'center';
    ctx.textBaseline = 'bottom';
    
    const displayVal = tk.val > 15.0 ? "Inf 🌋" : tk.val.toFixed(2);
    ctx.font = '900 13px monospace';
    
    if (tk.val > 5.5) {
      ctx.fillStyle = '#ef4444';
      ctx.shadowBlur = 6;
      ctx.shadowColor = '#ef4444';
    } else {
      ctx.fillStyle = idx === 0 ? '#06b6d4' : '#f472b6';
    }
    ctx.fillText(displayVal, tk.x + tkW/2, tkY - 8);
    ctx.shadowBlur = 0;
    
    // Label below
    ctx.fillStyle = '#94a3b8';
    ctx.font = 'bold 8px sans-serif';
    ctx.textBaseline = 'top';
    ctx.fillText(idx === 0 ? "FORWARD" : "REVERSE", tk.x + tkW/2, tkY + tkH + 6);
    ctx.font = 'normal 7px sans-serif';
    ctx.fillStyle = '#64748b';
    ctx.fillText(idx === 0 ? "D_KL(P||Q)" : "D_KL(Q||P)", tk.x + tkW/2, tkY + tkH + 15);
  });
}

function drawDetailsPanel(klPQ, klQP) {
  // Empirical statistics box at bottom right
  const boxX = 495;
  const boxY = 370;
  const boxW = tkWidth = 94;
  const boxH = 60;
  
  ctx.save();
  ctx.fillStyle = 'rgba(15, 23, 42, 0.6)';
  ctx.fillRect(boxX, boxY, boxW, boxH);
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
  ctx.lineWidth = 1;
  ctx.strokeRect(boxX, boxY, boxW, boxH);
  
  ctx.fillStyle = '#cbd5e1';
  ctx.font = '900 8px monospace';
  ctx.textAlign = 'left';
  ctx.fillText("MONTE CARLO STATISTICS", boxX + 6, boxY + 12);
  
  // Calculate rolling average
  let empiricalAvg = 0.0;
  if (sampleHistory.length > 0) {
    const sum = sampleHistory.reduce((a, b) => a + b, 0);
    empiricalAvg = sum / sampleHistory.length;
  }
  
  ctx.font = '700 8px sans-serif';
  ctx.fillStyle = '#64748b';
  ctx.fillText(`Target: ${simulationMode === 'forward' ? 'P(x)' : 'Q(x)'}`, boxX + 6, boxY + 26);
  ctx.fillText(`Samples: ${sampleHistory.length}/100`, boxX + 6, boxY + 36);
  
  ctx.fillStyle = '#4ade80';
  ctx.font = '900 10px monospace';
  ctx.fillText(`Emp KL: ${empiricalAvg.toFixed(2)}`, boxX + 6, boxY + 49);
  ctx.restore();
}

// MAIN 60FPS GRAPHICS LOOP
function draw() {
  animationFrame = null;
  tick++;
  
  const klPQ = getKlDivergence(muP, sigmaP, muQ, sigmaQ);
  const klQP = getKlDivergence(muQ, sigmaQ, muP, sigmaP);
  const activeKL = simulationMode === 'forward' ? klPQ : klQP;
  
  // Screen shake if meltdown active
  const isMeltdown = activeKL > 5.5;
  canvasWrap.classList.toggle('shake-heavy', dropRate !== 'none' && isMeltdown && activeKL > 7.0);
  
  // 1. Clear Screen
  ctx.fillStyle = '#0f172a';
  ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
  
  // Draw sci-fi connector line linking plots
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.02)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(plotXMin + plotWidth / 2, plotYMax1);
  ctx.lineTo(plotXMin + plotWidth / 2, plotYMin2);
  ctx.stroke();
  
  // 2. Draw Elements
  drawAxesAndGrid();
  drawPdfCurves();
  drawIntegrandBars();
  drawLiquidTanks(klPQ, klQP);
  drawDetailsPanel(klPQ, klQP);
  
  // 3. Monte Carlo Droplet Spawner
  let spawnInterval = 99999;
  if (dropRate === 'slow') spawnInterval = 30;
  if (dropRate === 'normal') spawnInterval = 10;
  if (dropRate === 'fast') spawnInterval = 4;
  
  if (tick % spawnInterval === 0 && dropRate !== 'none') {
    if (droplets.length < 100) {
      // Box-Muller sample from distribution
      let xSampled = 0;
      if (simulationMode === 'forward') {
        xSampled = sampleGaussian(muP, sigmaP);
      } else {
        xSampled = sampleGaussian(muQ, sigmaQ);
      }
      
      const pVal = gaussianPdf(xSampled, muP, sigmaP);
      const qVal = gaussianPdf(xSampled, muQ, sigmaQ);
      
      // Surprise bits
      const logP = gaussianLogPdf(xSampled, muP, sigmaP);
      const logQ = gaussianLogPdf(xSampled, muQ, sigmaQ);
      const bits = (simulationMode === 'forward' ? logP - logQ : logQ - logP) / Math.LN2;
      
      // Spawn drop at correct curve height
      const visualX = Math.max(-5.9, Math.min(5.9, xSampled));
      const cx = mapX(visualX);
      const cy = mapYPdf(simulationMode === 'forward' ? pVal : qVal);
      droplets.push(new Droplet(cx, cy, xSampled, bits));
    }
  }
  
  // 4. Update & Draw Particles (Droplets, sparks, bubbles)
  const activeColor = simulationMode === 'forward' ? '#06b6d4' : '#f472b6';
  const targetX = simulationMode === 'forward' ? 512 : 572;
  const targetY = 100;
  
  // Safety caps to prevent array explosion under lag or high speeds
  if (droplets.length > 100) droplets.splice(0, droplets.length - 100);
  if (bubbles.length > 100) bubbles.splice(0, bubbles.length - 100);
  if (sparks.length > 300) sparks.splice(0, sparks.length - 300);
  
  // Droplets
  for (let i = droplets.length - 1; i >= 0; i--) {
    const ep = droplets[i];
    const reached = ep.update(targetX, targetY);
    ep.draw(ctx, activeColor);
    
    if (reached) {
      triggerSparks(targetX, targetY, activeColor);
      
      // Add contribution to Monte Carlo history
      sampleHistory.push(ep.value);
      if (sampleHistory.length > maxHistorySize) {
        sampleHistory.shift();
      }
      
      // Remove droplet
      droplets.splice(i, 1);
    }
  }
  
  // Bubbles
  for (let i = bubbles.length - 1; i >= 0; i--) {
    const bb = bubbles[i];
    bb.update();
    bb.draw(ctx);
    if (bb.alpha <= 0) {
      bubbles.splice(i, 1);
    }
  }
  
  // Sparks
  for (let i = sparks.length - 1; i >= 0; i--) {
    const sp = sparks[i];
    sp.update();
    sp.draw(ctx);
    if (sp.life <= 0) {
      sparks.splice(i, 1);
    }
  }
  
  // 5. Warning & Overlay Panel
  if (isMeltdown && tick % 32 < 16) {
    ctx.fillStyle = 'rgba(239, 68, 68, 0.04)';
    ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    
    ctx.fillStyle = '#ef4444';
    ctx.font = 'bold 9px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText("⚠️ D_KL STRESS DETECTED: HIGH INFORMATION LOSS / TAIL ZERO AVOIDANCE PENALTY ⚠️", plotXMin + plotWidth / 2, 20);
  }
  
  // Labels for Plots
  ctx.fillStyle = '#cbd5e1';
  ctx.font = 'bold 10px sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText("PROBABILITY DENSITY FUNCTIONS:  P(x) and Q(x)", plotXMin, 30);
  
  ctx.fillText("LOCAL KL DIVERGENCE CONTRIBUTION", plotXMin, 252);
  ctx.font = '9px sans-serif';
  ctx.fillStyle = '#ef4444';
  ctx.fillText("■ SURPRISE PENALTY", plotXMin + 230, 252);
  ctx.fillStyle = '#10b981';
  ctx.fillText("■ SURPLUS SURPRISE SAVING", plotXMin + 340, 252);
  
  if (dropRate !== 'none' || droplets.length || bubbles.length || sparks.length) requestDraw();
}

// Start visualizer
setPreset('drift');
window.addEventListener('pagehide', () => {
  if (animationFrame !== null) cancelAnimationFrame(animationFrame);
  animationFrame = null;
  canvasWrap.classList.remove('shake-heavy');
});

</script>
</body>
</html>
"""
    components.html(html_code, height=830, scrolling=False)

def main():
    st.title("🧩 Page 60: KL Divergence — Gap Between Distributions")

    st.markdown(
        """
        In [Page 59: Cross-Entropy — Predicted vs Reality](file:///d:/physics-simulation/pages/59Cross-Entropy%20%E2%80%94%20Predicted%20vs%20Reality.py), we observed how **Cross-Entropy** penalizes a neural network's incorrect prediction.
        But mathematically, Cross-Entropy consists of two parts: the inevitable natural entropy of reality $H(P)$, and an **excess coding waste** when we approximate reality using our model's beliefs $Q$.
        
        This excess waste — the actual gap between two probability distributions — is quantified by the **Kullback-Leibler (KL) Divergence** ($D_{KL}$).
        It measures exactly how many **extra bits** of information we waste, on average, if we encode data events from a true distribution $P$ using an imperfect code optimized for a predicted distribution $Q$.
        """
    )

    st.divider()

    col1, col2 = st.columns([1.1, 0.9])

    with col1:
        st.subheader("The Mathematics of Information Gap 🧮")
        st.markdown(
            r"""
            For two probability distributions, $P(x)$ (the target label or reality) and $Q(x)$ (the approximation or model predictions):
            
            * **Discrete Case:**
              $$D_{KL}(P \parallel Q) = \sum_{x} P(x) \log_2 \left( \frac{P(x)}{Q(x)} \right) \text{ bits}$$
              
            * **Continuous Case:**
              $$D_{KL}(P \parallel Q) = \int_{-\infty}^{\infty} P(x) \log_2 \left( \frac{P(x)}{Q(x)} \right) dx \text{ bits}$$
              
            * **Closed-Form for two Gaussians:** In our visualizer, we model two normal bell curves $P \sim \mathcal{N}(\mu_P, \sigma_P^2)$ and $Q \sim \mathcal{N}(\mu_Q, \sigma_Q^2)$. The analytical divergence is calculated exactly as:
              $$D_{KL}(P \parallel Q) = \frac{1}{\ln 2} \left[ \ln\left(\frac{\sigma_Q}{\sigma_P}\right) + \frac{\sigma_P^2 + (\mu_P - \mu_Q)^2}{2\sigma_Q^2} - \frac{1}{2} \right] \text{ bits}$$
              
            * **Gibbs' Inequality:** The KL divergence is mathematically guaranteed to be **non-negative**:
              $$D_{KL}(P \parallel Q) \ge 0$$
              It equals exactly $0$ if and only if $P = Q$ (distributions match perfectly).
            """
        )

    with col2:
        st.subheader("Why the Direction Matters: Asymmetry ⚖️")
        st.markdown(
            r"""
            KL Divergence is **not a true distance metric** because it is asymmetric:
            $$D_{KL}(P \parallel Q) \neq D_{KL}(Q \parallel P)$$
            
            This directionality creates two radically different optimization behaviors in deep learning:
            
            1. **Forward KL ($D_{KL}(P \parallel Q)$) — Zero-Avoiding / Mean-Seeking:**
               If $P(x) > 0$, we *must* have $Q(x) > 0$. If $Q(x) \to 0$ in a region where reality exists, the fraction $\frac{P(x)}{Q(x)}$ explodes, and the penalty sweeps to **infinity**! 
               Thus, a model optimizing Forward KL is forced to stretch and cover **every mode** of $P$, often producing fuzzy, averaged predictions.
               
            2. **Reverse KL ($D_{KL}(Q \parallel P)$) — Zero-Forcing / Mode-Seeking:**
               If reality has no data in a region ($P(x) \to 0$), the model $Q(x)$ is heavily penalized for placing any probability there. 
               To minimize this, $Q$ will shrink to zero wherever $P$ is zero. If $P$ has multiple distinct modes, $Q$ will pick just **one mode** and focus all its density there, completely ignoring the other modes to ensure a tight, sharp, high-confidence fit.
            """
        )

    st.divider()
    st.markdown("### 🧪 The KL Divergence Asymmetry & Sampling Laboratory")
    st.markdown(
        "Experiment with drifting normal distributions in real time! "
        "Select presets or drag the sliders to change the means ($\mu$) and standard deviations ($\sigma$) of reality $P$ and model $Q$. "
        "Watch how the **asymmetry** is reflected in the twin liquid columns, witness a local **Surprise Penalty** ribbon, "
        "and toggle the **Interactive Monte Carlo Sampler** to drop particle samples and see the empirical average converge to the analytical limit!"
    )

    render_kl_divergence_lab()

    st.divider()
    st.subheader("🤖 Bridge to AI: KL Divergence in Modern Deep Learning")
    st.markdown(
        r"""
        KL Divergence is a fundamental tool across the most advanced branches of modern Artificial Intelligence:
        
        #### 1. VAEs & Variational Inference: Forward KL 🔍
        In **Variational Autoencoders (VAEs)**, we want to map complex input data (like high-resolution faces) into a simple, continuous latent space (usually standard Gaussians $\mathcal{N}(0, I)$). 
        To force the encoder network's output distribution $Q(z|x)$ to resemble standard noise, we add a KL Divergence penalty to our loss function:
        $$\text{Loss} = \text{Reconstruction Error} + D_{KL}(Q(z|x) \parallel \mathcal{N}(0, I))$$
        This regularizes the latent space, keeping it smooth and continuous, allowing us to generate completely new, realistic images by sampling coordinates!
        
        #### 2. Reinforcement Learning from Human Feedback (RLHF): Stable Policy Alignment 🛡️
        When fine-tuning Large Language Models like GPT-4 or Claude to be helpful and safe, we train a **Reward Model** based on human feedback and optimize the language policy network ($Q$) using PPO. 
        However, if optimized aggressively, the model will find "hacks" in the reward function (called **reward hacking**), outputting gibberish or unsafe answers that exploit the evaluator.
        
        To prevent this catastrophic drift, engineers add a **Forward KL Divergence penalty** between the active training model $Q$ and the frozen base pre-trained model $P$:
        $$\text{Objective}(\theta) = \mathbb{E}_{x, y \sim D}[\text{Reward}(x, y)] - \beta \, D_{KL}(Q_\theta(y|x) \parallel P_{\text{base}}(y|x))$$
        This KL "anchor" acts as a protective leash, penalizing the training LLM if its vocabulary and probability distributions drift too far from the base model, maintaining the model's coherent grammar, factual integrity, and safety!
        """
    )

    st.divider()
    st.markdown(
        '<div style="color:#94a3b8;font-size:0.95rem;">Page 60 — you\'ve mastered how KL Divergence captures the information gap and asymmetry between probability distributions. By isolating excess surprise, you have unlocked the central metric of LLM safety and generative latents. Next: we plunge deeper into advanced Linear Algebra to find hidden axes of maximum variation — starting with the fascinating mechanics of <b>Eigenvectors & Eigenvalues (Page 61)</b>!</div>',
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
