import streamlit as st
import streamlit.components.v1 as components
import numpy as np

st.set_page_config(page_title="Entropy — Average Uncertainty", layout="wide")

def render_entropy_lab():
    html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{
  font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  background:#0f172a;
  color:#f8fafc;
  overflow:hidden;
  padding:15px;
}
.outer-container{
  display:flex;
  flex-direction:column;
  gap:16px;
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
  gap:12px;
}
.panel-right{
  flex:1.4;
  display:flex;
  flex-direction:column;
  gap:10px;
}
.card {
  background: rgba(30, 41, 59, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 16px;
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

/* Mode Switcher */
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
  background: rgba(167, 139, 250, 0.16);
  border-color: #a78bfa;
  color: #a78bfa;
  box-shadow: 0 0 12px rgba(167, 139, 250, 0.2);
}

/* Custom Grid for presets */
.preset-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
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
  background: #a78bfa;
  box-shadow: 0 0 8px #a78bfa;
  cursor: pointer;
  transition: transform 0.1s;
}
input[type=range]::-webkit-slider-thumb:hover {
  transform: scale(1.2);
}

/* Action Buttons */
.action-row {
  display: flex;
  gap: 10px;
  margin-top: 6px;
}
.trigger-btn {
  flex: 1.5;
  background: linear-gradient(135deg, #818cf8, #a78bfa);
  color: #0f172a;
  border: none;
  padding: 11px;
  border-radius: 10px;
  font-weight: 800;
  font-size: 13px;
  letter-spacing: 0.5px;
  cursor: pointer;
  text-transform: uppercase;
  transition: all 0.2s;
  box-shadow: 0 4px 15px rgba(167, 139, 250, 0.3);
}
.trigger-btn:hover {
  filter: brightness(1.1);
  box-shadow: 0 6px 20px rgba(167, 139, 250, 0.45);
  transform: translateY(-1px);
}
.auto-btn {
  flex: 1;
  background: rgba(78, 205, 196, 0.12);
  color: #4ECDC4;
  border: 1px solid rgba(78, 205, 196, 0.4);
  padding: 11px;
  border-radius: 10px;
  font-weight: 800;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
}
.auto-btn:hover {
  background: rgba(78, 205, 196, 0.25);
  color: #fff;
}
.auto-btn.active {
  background: #4ECDC4;
  color: #0f172a;
  box-shadow: 0 0 12px rgba(78, 205, 196, 0.4);
}

/* Log box */
.terminal-log {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 12px;
  font-family: monospace;
  font-size: 11px;
  color: #4ade80;
  height: 100px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.log-line { line-height: 1.3; }
.log-line span.cyan { color: #22d3ee; }
.log-line span.gold { color: #facc15; }
.log-line span.rose { color: #fb7185; }

/* Canvas Visualizer wrapper */
#canvas-wrap {
  position: relative;
  background: rgba(30, 41, 59, 0.2);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.4);
  overflow: hidden;
  width: 100%;
}
canvas {
  display: block;
  width: 100%;
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
        <h2>Shannon's Entropy Lab 🌀</h2>
        <p class="sub">Explore how average uncertainty (entropy) changes across binary systems and complex 4-state systems!</p>
      </div>

      <!-- Mode Selector -->
      <div class="card">
        <div class="mode-row">
          <button class="mbtn active" id="mode-coin" onclick="switchMode('coin')">🪙 Binary Coin</button>
          <button class="mbtn" id="mode-weather" onclick="switchMode('weather')">🌦️ Weather (4-State)</button>
        </div>
      </div>

      <!-- Presets and Sliders -->
      <div class="card">
        <h3 id="panel-title" style="font-size:12px; text-transform:uppercase; letter-spacing:1px; color:#94a3b8; margin-bottom:8px;">Coin Bias Presets</h3>
        
        <!-- COIN PRESETS -->
        <div class="preset-grid" id="coin-presets">
          <div class="preset-card active" onclick="setCoinP(0.5, this)">
            <span class="emoji">🪙</span>
            <span class="name">Fair Coin</span>
            <span class="desc">50% H / 50% T</span>
          </div>
          <div class="preset-card" onclick="setCoinP(0.75, this)">
            <span class="emoji">⚖️</span>
            <span class="name">Mild Bias</span>
            <span class="desc">75% H / 25% T</span>
          </div>
          <div class="preset-card" onclick="setCoinP(1.0, this)">
            <span class="emoji">🧲</span>
            <span class="name">Fully Loaded</span>
            <span class="desc">100% H / 0% T</span>
          </div>
        </div>

        <!-- WEATHER PRESETS -->
        <div class="preset-grid" id="weather-presets" style="display:none;">
          <div class="preset-card active" onclick="setWeatherP([0.25, 0.25, 0.25, 0.25], this)">
            <span class="emoji">🌀</span>
            <span class="name">Pure Chaos</span>
            <span class="desc">25% Each</span>
          </div>
          <div class="preset-card" onclick="setWeatherP([0.9, 0.03, 0.05, 0.02], this)">
            <span class="emoji">☀️</span>
            <span class="name">Sahara Sun</span>
            <span class="desc">90% Sunny</span>
          </div>
          <div class="preset-card" onclick="setWeatherP([0.1, 0.5, 0.3, 0.1], this)">
            <span class="emoji">⛈️</span>
            <span class="name">Tropical Storm</span>
            <span class="desc">50% Rain / 30% Cloud</span>
          </div>
        </div>

        <!-- SLIDERS CONTAINER -->
        <div class="slider-container" id="sliders-wrap">
          <!-- Will update dynamically between coin/weather inputs -->
        </div>

        <!-- Action Row -->
        <div class="action-row">
          <button class="trigger-btn" id="trigger-btn" onclick="triggerSimulation()">Toss Coin 🪙</button>
          <button class="auto-btn" id="auto-btn" onclick="toggleAuto()">⚡ AUTO</button>
        </div>
      </div>

      <!-- Retro Terminal Log -->
      <div class="terminal-log" id="log-box">
        <div class="log-line">> <span class="cyan">Entropy Synthesizer Booted successfully.</span> Mode: Binary Coin.</div>
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
const triggerBtn = document.getElementById('trigger-btn');
const autoBtn = document.getElementById('auto-btn');

// App States
let currentMode = 'coin'; // 'coin' or 'weather'
let coinP = 0.5; // p(Heads)
let weatherP = [0.25, 0.25, 0.25, 0.25]; // [Sunny, Rainy, Cloudy, Snowy]
const weatherColors = ['#facc15', '#3b82f6', '#06b6d4', '#a78bfa'];
const weatherLabels = ['Sunny ☀️', 'Rainy 🌧️', 'Cloudy ☁️', 'Snowy ❄️'];

// Law of Large Numbers Stats
const MAX_CHART_POINTS = 500;
let coinSampleCount = 0;
let coinCumulativeSurprise = 0;
let weatherSampleCount = 0;
let weatherCumulativeSurprise = 0;
let runningAverageSurprise = [];
let weatherRunningAvgSurprise = [];

// Simulation animations
let coinAnimationTick = 0;
let coinAnimationState = 'idle'; // 'idle', 'flipping', 'settling'
let coinResult = 1; // 1 = H, 0 = T
let weatherChamberActive = false;
let weatherChamberTick = 0;
let weatherResultIdx = 0;
let activeParticles = [];

// Auto simulation loop
let autoInterval = null;

// safe math helper
function log2(p) {
  if (p <= 0) return 0;
  return Math.log2(p);
}

function getBinaryEntropy(p) {
  if (p <= 0 || p >= 1) return 0;
  return -p * log2(p) - (1-p) * log2(1-p);
}

function getWeatherEntropy() {
  let ent = 0;
  for (let i = 0; i < 4; i++) {
    if (weatherP[i] > 0) {
      ent -= weatherP[i] * log2(weatherP[i]);
    }
  }
  return ent;
}

function appendChartPoint(history, value) {
  history.push(value);
  if (history.length > MAX_CHART_POINTS) history.shift();
}

// Particle Class for visual effects inside Storm Chamber
class WeatherParticle {
  constructor(type, xRange, yRange) {
    this.type = type; // 'sun', 'rain', 'cloud', 'snow'
    this.x = xRange.min + Math.random() * (xRange.max - xRange.min);
    this.y = yRange.min + Math.random() * (yRange.max - yRange.min);
    this.vx = (Math.random() - 0.5) * 1.5;
    this.vy = 1 + Math.random() * 2;
    this.size = 1.5 + Math.random() * 3.5;
    this.alpha = 0.8 + Math.random() * 0.2;
    this.life = 60 + Math.random() * 60;
    this.maxLife = this.life;
    
    if (type === 'sun') {
      this.vy = 0;
      this.vx = 0;
      this.size = 2 + Math.random() * 6;
      this.angle = Math.random() * Math.PI * 2;
      this.rotSpeed = (Math.random() - 0.5) * 0.05;
    } else if (type === 'cloud') {
      this.vx = 0.3 + Math.random() * 0.6;
      this.vy = 0;
      this.size = 15 + Math.random() * 20;
    } else if (type === 'snow') {
      this.vy = 0.6 + Math.random() * 0.8;
      this.vx = (Math.random() - 0.5) * 0.8;
    }
  }

  update(bounds) {
    this.x += this.vx;
    this.y += this.vy;
    this.life--;
    
    if (this.type === 'rain') {
      if (this.y > bounds.yMax - 5) {
        this.y = bounds.yMin;
        this.x = bounds.xMin + Math.random() * (bounds.xMax - bounds.xMin);
      }
    } else if (this.type === 'snow') {
      if (this.y > bounds.yMax - 5) {
        this.y = bounds.yMin;
        this.x = bounds.xMin + Math.random() * (bounds.xMax - bounds.xMin);
      }
    } else if (this.type === 'cloud') {
      if (this.x > bounds.xMax + this.size) {
        this.x = bounds.xMin - this.size;
      }
    } else if (this.type === 'sun') {
      this.angle += this.rotSpeed;
    }
  }

  draw(c) {
    c.save();
    c.globalAlpha = Math.max(0, this.alpha * (this.life / this.maxLife));
    if (this.type === 'rain') {
      c.strokeStyle = '#60a5fa';
      c.lineWidth = 1.5;
      c.beginPath();
      c.moveTo(this.x, this.y);
      c.lineTo(this.x + this.vx, this.y + 6);
      c.stroke();
    } else if (this.type === 'snow') {
      c.fillStyle = '#e2e8f0';
      c.beginPath();
      c.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      c.fill();
    } else if (this.type === 'cloud') {
      c.fillStyle = 'rgba(203, 213, 225, 0.15)';
      c.beginPath();
      c.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      c.arc(this.x + this.size*0.7, this.y - this.size*0.2, this.size*0.8, 0, Math.PI * 2);
      c.arc(this.x - this.size*0.7, this.y - this.size*0.2, this.size*0.8, 0, Math.PI * 2);
      c.fill();
    } else if (this.type === 'sun') {
      c.fillStyle = 'rgba(253, 224, 71, 0.4)';
      c.beginPath();
      c.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      c.fill();
      
      // Draw rays
      c.strokeStyle = 'rgba(253, 224, 71, 0.2)';
      c.lineWidth = 2;
      for (let i = 0; i < 8; i++) {
        const rayAngle = this.angle + (i / 8) * Math.PI * 2;
        c.beginPath();
        c.moveTo(this.x + Math.cos(rayAngle)*this.size, this.y + Math.sin(rayAngle)*this.size);
        c.lineTo(this.x + Math.cos(rayAngle)*(this.size + 8), this.y + Math.sin(rayAngle)*(this.size + 8));
        c.stroke();
      }
    }
    c.restore();
  }
}

// Switch between Coin and Weather modes
function switchMode(mode) {
  if (currentMode === mode) return;
  stopAuto();
  currentMode = mode;
  
  // Highlight correct buttons
  document.getElementById('mode-coin').classList.toggle('active', mode === 'coin');
  document.getElementById('mode-weather').classList.toggle('active', mode === 'weather');
  
  // Toggle presets
  document.getElementById('coin-presets').style.display = mode === 'coin' ? 'grid' : 'none';
  document.getElementById('weather-presets').style.display = mode === 'weather' ? 'grid' : 'none';
  
  // Update header text
  document.getElementById('panel-title').innerText = mode === 'coin' ? 'Coin Bias Presets' : 'Weather Presets';
  document.getElementById('trigger-btn').innerText = mode === 'coin' ? 'Toss Coin 🪙' : 'Generate Weather 🌦️';

  // Build appropriate sliders
  buildSliders();
  
  // Reset logs and animation state
  logBox.innerHTML = '';
  activeParticles = [];
  coinAnimationState = 'idle';
  weatherChamberActive = false;

  if (mode === 'coin') {
    addLog("Switched to Binary Coin Mode. Total uncertainty peaks at p=0.5.", "cyan");
    // Trigger active state on fair coin preset
    const cards = document.querySelectorAll('#coin-presets .preset-card');
    cards.forEach((c, idx) => c.classList.toggle('active', idx === 0));
    coinP = 0.5;
  } else {
    addLog("Switched to 4-State Weather Forecasting. Proportional normalization is active.", "cyan");
    const cards = document.querySelectorAll('#weather-presets .preset-card');
    cards.forEach((c, idx) => c.classList.toggle('active', idx === 0));
    weatherP = [0.25, 0.25, 0.25, 0.25];
  }
}

// Log writer
function addLog(text, type = 'info') {
  const line = document.createElement('div');
  line.className = 'log-line';
  let spanClass = 'cyan';
  if (type === 'warn') spanClass = 'rose';
  if (type === 'gold') spanClass = 'gold';
  
  line.innerHTML = `> <span class="${spanClass}">${text}</span>`;
  logBox.appendChild(line);
  logBox.scrollTop = logBox.scrollHeight;
  
  while (logBox.children.length > 5) {
    logBox.removeChild(logBox.firstChild);
  }
}

// Generate Sliders
function buildSliders() {
  const container = document.getElementById('sliders-wrap');
  container.innerHTML = '';
  
  if (currentMode === 'coin') {
    const row = document.createElement('div');
    row.className = 'slider-row';
    row.innerHTML = `
      <div class="slabel-row">
        <span>Probability of Heads: p(Heads)</span>
        <span class="sval" style="color: #a78bfa;" id="coin-p-val">0.50</span>
      </div>
      <input type="range" id="coin-slider" min="0.0" max="1.0" step="0.01" value="${coinP}" oninput="onCoinSliderChange(this.value)">
      <div style="display:flex; justify-content:space-between; font-size:10px; color:#64748b;">
        <span>Certain Tails (p=0)</span>
        <span>Fair Coin (p=0.5)</span>
        <span>Certain Heads (p=1.0)</span>
      </div>
    `;
    container.appendChild(row);
  } else {
    for (let i = 0; i < 4; i++) {
      const row = document.createElement('div');
      row.className = 'slider-row';
      row.innerHTML = `
        <div class="slabel-row">
          <span>p(${weatherLabels[i]})</span>
          <span class="sval" style="color: ${weatherColors[i]};" id="weather-p-val-${i}">${(weatherP[i]*100).toFixed(0)}%</span>
        </div>
        <input type="range" id="weather-slider-${i}" min="0.0" max="1.0" step="0.01" value="${weatherP[i]}" oninput="onWeatherSliderChange(${i}, this.value)">
      `;
      container.appendChild(row);
    }
  }
}

// Preset Adjustments
function setCoinP(p, element) {
  coinP = p;
  document.getElementById('coin-slider').value = p;
  document.getElementById('coin-p-val').innerText = p.toFixed(2);
  
  // Highlight active preset card
  const cards = document.querySelectorAll('#coin-presets .preset-card');
  cards.forEach(c => c.classList.remove('active'));
  element.classList.add('active');
  
  const ent = getBinaryEntropy(p);
  addLog(`Preset applied. p(Heads) = ${p.toFixed(2)}. Entropy: ${ent.toFixed(3)} bits.`, 'info');
}

function setWeatherP(arr, element) {
  weatherP = [...arr];
  for (let i = 0; i < 4; i++) {
    document.getElementById(`weather-slider-${i}`).value = weatherP[i];
    document.getElementById(`weather-p-val-${i}`).innerText = `${(weatherP[i]*100).toFixed(0)}%`;
  }
  
  const cards = document.querySelectorAll('#weather-presets .preset-card');
  cards.forEach(c => c.classList.remove('active'));
  element.classList.add('active');
  
  const ent = getWeatherEntropy();
  addLog(`Preset applied. Entropy H(X) = ${ent.toFixed(3)} bits.`, 'info');
}

// Real-world dynamic slider change callback
function onCoinSliderChange(val) {
  coinP = parseFloat(val);
  document.getElementById('coin-p-val').innerText = coinP.toFixed(2);
  
  // Deactivate preset card highlights unless it matches perfectly
  const cards = document.querySelectorAll('#coin-presets .preset-card');
  cards.forEach(c => c.classList.remove('active'));
}

// Complex multi-slider proportional normalization
function onWeatherSliderChange(changedIdx, val) {
  const newValue = parseFloat(val);
  
  let restSum = 0;
  for (let i = 0; i < 4; i++) {
    if (i !== changedIdx) restSum += weatherP[i];
  }
  
  const remaining = 1.0 - newValue;
  
  if (restSum > 0.0001) {
    for (let i = 0; i < 4; i++) {
      if (i !== changedIdx) {
        weatherP[i] = (weatherP[i] / restSum) * remaining;
      }
    }
  } else {
    // Divide equally among the remaining 3
    for (let i = 0; i < 4; i++) {
      if (i !== changedIdx) {
        weatherP[i] = remaining / 3.0;
      }
    }
  }
  weatherP[changedIdx] = newValue;
  
  // Clamp check to ensure sum is mathematically exactly 1.0
  let sum = weatherP.reduce((a,b)=>a+b, 0);
  if (Math.abs(sum - 1.0) > 0.000001) {
    // Distribute error
    const err = (1.0 - sum) / 4.0;
    for (let i = 0; i < 4; i++) weatherP[i] += err;
  }
  
  // Update slider positions & labels
  for (let i = 0; i < 4; i++) {
    // Clamp between 0 and 1
    weatherP[i] = Math.max(0, Math.min(1, weatherP[i]));
    document.getElementById(`weather-slider-${i}`).value = weatherP[i];
    document.getElementById(`weather-p-val-${i}`).innerText = `${(weatherP[i]*100).toFixed(0)}%`;
  }
  
  const cards = document.querySelectorAll('#weather-presets .preset-card');
  cards.forEach(c => c.classList.remove('active'));
}

// Single Action Trigger
function triggerSimulation() {
  if (currentMode === 'coin') {
    // Setup coin flip physics animation
    coinAnimationState = 'flipping';
    coinAnimationTick = 0;
    
    // Choose outcome based on coinP
    const rand = Math.random();
    coinResult = rand < coinP ? 1 : 0; // 1 = Heads, 0 = Tails
    
    // Log details
    const pOut = coinResult === 1 ? coinP : (1 - coinP);
    const surprise = pOut <= 0 ? 0 : -log2(pOut);
    coinCumulativeSurprise += surprise;
    coinSampleCount++;
    appendChartPoint(runningAverageSurprise, coinCumulativeSurprise / coinSampleCount);
    
  } else {
    // Setup weather storm chamber activation
    weatherChamberActive = true;
    weatherChamberTick = 0;
    
    // Weighted random selection
    const rand = Math.random();
    let cumulative = 0;
    let chosenIdx = 0;
    for (let i = 0; i < 4; i++) {
      cumulative += weatherP[i];
      if (rand <= cumulative) {
        chosenIdx = i;
        break;
      }
    }
    weatherResultIdx = chosenIdx;
    
    // Spawn corresponding chamber particles
    activeParticles = [];
    const particleType = ['sun', 'rain', 'cloud', 'snow'][chosenIdx];
    const particleCount = chosenIdx === 0 ? 8 : (chosenIdx === 1 ? 50 : (chosenIdx === 2 ? 6 : 40));
    
    const bounds = { xMin: 320, xMax: 575, yMin: 220, yMax: 470 };
    for (let i = 0; i < particleCount; i++) {
      activeParticles.push(new WeatherParticle(
        particleType, 
        { min: bounds.xMin + 5, max: bounds.xMax - 5 },
        { min: bounds.yMin + 5, max: bounds.yMax - 5 }
      ));
    }
    
    // Log details
    const pOut = weatherP[chosenIdx];
    const surprise = pOut <= 0 ? 0 : -log2(pOut);
    weatherCumulativeSurprise += surprise;
    weatherSampleCount++;
    appendChartPoint(weatherRunningAvgSurprise, weatherCumulativeSurprise / weatherSampleCount);
    
    // Print to retro log
    const typeLabel = weatherLabels[chosenIdx];
    if (surprise === 0) {
      addLog(`Result: ${typeLabel} (p=${(pOut*100).toFixed(0)}%). Surprise: 0 bits (Yawns).`, 'info');
    } else if (surprise < 2.0) {
      addLog(`Result: ${typeLabel} (p=${(pOut*100).toFixed(0)}%). Surprise: ${surprise.toFixed(2)} bits.`, 'cyan');
    } else if (surprise < 4.0) {
      addLog(`Result: ${typeLabel} (p=${(pOut*100).toFixed(0)}%). Rare! Surprise: ${surprise.toFixed(2)} bits!`, 'gold');
    } else {
      addLog(`Result: ${typeLabel} (p=${(pOut*100).toFixed(0)}%). UNBELIEVABLE! Surprise: ${surprise.toFixed(2)} bits!!!`, 'warn');
    }
  }
}

// Continuous auto runner
function toggleAuto() {
  if (autoInterval) {
    stopAuto();
  } else {
    autoBtn.innerText = "⏸ PAUSE";
    autoBtn.classList.add('active');
    autoInterval = setInterval(() => {
      triggerSimulation();
    }, 150);
  }
}

function stopAuto() {
  if (autoInterval) {
    clearInterval(autoInterval);
    autoInterval = null;
    autoBtn.innerText = "⚡ AUTO";
    autoBtn.classList.remove('active');
  }
}

// Drawing helper functions
function drawGrid(xMin, xMax, yMin, yMax, cols, rows, style = 'rgba(255,255,255,0.03)') {
  ctx.strokeStyle = style;
  ctx.lineWidth = 1;
  const gw = xMax - xMin;
  const gh = yMax - yMin;
  for (let i = 1; i < cols; i++) {
    const x = xMin + (i / cols) * gw;
    ctx.beginPath(); ctx.moveTo(x, yMin); ctx.lineTo(x, yMax); ctx.stroke();
  }
  for (let i = 1; i < rows; i++) {
    const y = yMin + (i / rows) * gh;
    ctx.beginPath(); ctx.moveTo(xMin, y); ctx.lineTo(xMax, y); ctx.stroke();
  }
}

function drawAxes(xMin, xMax, yMin, yMax, style = 'rgba(255,255,255,0.15)') {
  ctx.strokeStyle = style;
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(xMin, yMin - 5);
  ctx.lineTo(xMin, yMax);
  ctx.lineTo(xMax + 5, yMax);
  ctx.stroke();
}

// MAIN RENDER LOOP (60fps)
function draw() {
  // Clear Frame
  ctx.fillStyle = '#0f172a';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  
  if (currentMode === 'coin') {
    // ==========================================
    // DRAW COIN FLIP MODE
    // ==========================================
    
    // --- 1. LEFT PANEL: Binary Entropy Curve ---
    const cxMin = 40, cxMax = 260, cyMin = 120, cyMax = 280;
    const cw = cxMax - cxMin, ch = cyMax - cyMin;
    
    // Header
    ctx.fillStyle = '#94a3b8';
    ctx.font = 'bold 11px sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText("BINARY ENTROPY FUNCTION H(p)", cxMin, cyMin - 40);
    
    ctx.fillStyle = '#64748b';
    ctx.font = '9px sans-serif';
    ctx.fillText("H(p) = -p log₂ p - (1-p) log₂ (1-p)", cxMin, cyMin - 24);

    drawGrid(cxMin, cxMax, cyMin, cyMax, 4, 4);
    drawAxes(cxMin, cxMax, cyMin, cyMax);

    // Labels
    ctx.fillStyle = '#64748b';
    ctx.font = 'bold 9px monospace';
    ctx.textAlign = 'center';
    ctx.fillText("p=0", cxMin, cyMax + 12);
    ctx.fillText("p=0.5", cxMin + cw*0.5, cyMax + 12);
    ctx.fillText("p=1.0", cxMax, cyMax + 12);
    
    ctx.textAlign = 'right';
    ctx.textBaseline = 'middle';
    ctx.fillText("1.0 bit", cxMin - 8, cyMin);
    ctx.fillText("0.5", cxMin - 8, cyMin + ch*0.5);
    ctx.fillText("0", cxMin - 8, cyMax);
    
    // Plot H(p) curve
    ctx.beginPath();
    ctx.lineWidth = 2.5;
    const curveGrad = ctx.createLinearGradient(cxMin, 0, cxMax, 0);
    curveGrad.addColorStop(0, '#fb7185'); // Loaded coin (0 bits)
    curveGrad.addColorStop(0.5, '#a78bfa'); // Maximum uncertainty (1 bit)
    curveGrad.addColorStop(1, '#fb7185');
    ctx.strokeStyle = curveGrad;
    
    let first = true;
    for (let x = cxMin; x <= cxMax; x++) {
      const p = (x - cxMin) / cw;
      const h = getBinaryEntropy(p);
      const y = cyMax - h * ch;
      if (first) { ctx.moveTo(x, y); first = false; }
      else { ctx.lineTo(x, y); }
    }
    ctx.stroke();
    
    // Draw current active dot on curve
    const activeH = getBinaryEntropy(coinP);
    const activeX = cxMin + coinP * cw;
    const activeY = cyMax - activeH * ch;
    
    ctx.setLineDash([3, 3]);
    ctx.strokeStyle = 'rgba(167, 139, 250, 0.4)';
    ctx.beginPath();
    ctx.moveTo(activeX, activeY);
    ctx.lineTo(activeX, cyMax); // vertical down to axis
    ctx.moveTo(activeX, activeY);
    ctx.lineTo(cxMin, activeY); // horizontal left to axis
    ctx.stroke();
    ctx.setLineDash([]);
    
    ctx.beginPath();
    ctx.arc(activeX, activeY, 6, 0, Math.PI*2);
    ctx.fillStyle = '#fff';
    ctx.strokeStyle = '#a78bfa';
    ctx.lineWidth = 2.5;
    ctx.shadowColor = '#a78bfa';
    ctx.shadowBlur = 8;
    ctx.fill();
    ctx.stroke();
    ctx.shadowBlur = 0;
    
    // Active readouts
    ctx.fillStyle = '#cbd5e1';
    ctx.font = 'bold 11px monospace';
    ctx.textAlign = 'left';
    ctx.fillText(`H(X) = ${activeH.toFixed(3)} bits`, cxMin, cyMax + 30);
    
    // --- 2. RIGHT PANEL: Coin Tossing Chamber & Cylinder ---
    const rxCenter = 440, ryCenter = 160, rRadius = 45;
    
    ctx.fillStyle = '#94a3b8';
    ctx.font = 'bold 11px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText("COIN TOSS CHAMBER", rxCenter, ryCenter - 75);

    // Draw Glass Tube Cylinder
    ctx.strokeStyle = 'rgba(255,255,255,0.08)';
    ctx.lineWidth = 2;
    ctx.fillStyle = 'rgba(0,0,0,0.3)';
    ctx.beginPath();
    ctx.ellipse(rxCenter, ryCenter - 55, rRadius, 10, 0, 0, Math.PI*2);
    ctx.ellipse(rxCenter, ryCenter + 55, rRadius, 10, 0, 0, Math.PI*2);
    ctx.stroke();
    ctx.fill();
    
    ctx.beginPath();
    ctx.moveTo(rxCenter - rRadius, ryCenter - 55);
    ctx.lineTo(rxCenter - rRadius, ryCenter + 55);
    ctx.moveTo(rxCenter + rRadius, ryCenter - 55);
    ctx.lineTo(rxCenter + rRadius, ryCenter + 55);
    ctx.stroke();

    // Physics Animation for Toss
    let coinScaleY = 1.0;
    let coinHeightOffset = 0;
    
    if (coinAnimationState === 'flipping') {
      coinAnimationTick += 0.2;
      coinHeightOffset = -Math.sin((coinAnimationTick/5) * Math.PI) * 45;
      coinScaleY = Math.cos(coinAnimationTick * 1.5);
      
      if (coinAnimationTick >= 5) {
        coinAnimationState = 'settling';
        coinAnimationTick = 0;
      }
    } else if (coinAnimationState === 'settling') {
      coinAnimationTick += 0.25;
      coinHeightOffset = 0;
      // Oscillate scale slightly to damp bounce
      coinScaleY = 1.0 + Math.sin(coinAnimationTick * 1.5) * 0.15 * Math.exp(-coinAnimationTick * 0.4);
      
      if (coinAnimationTick >= 6) {
        coinAnimationState = 'idle';
        // Add log when done tossing
        const outLabel = coinResult === 1 ? 'HEADS 🪙' : 'TAILS 👥';
        const pOut = coinResult === 1 ? coinP : (1 - coinP);
        const surprise = pOut <= 0 ? 0 : -log2(pOut);
        
        if (surprise === 0) {
          addLog(`Result: ${outLabel} (p=${pOut.toFixed(2)}). Surprise: 0 bits (No new info).`, 'info');
        } else if (surprise <= 1.0001) {
          addLog(`Result: ${outLabel} (p=${pOut.toFixed(2)}). Surprise: ${surprise.toFixed(2)} bits.`, 'cyan');
        } else if (surprise <= 3.0) {
          addLog(`Result: ${outLabel} (p=${pOut.toFixed(2)}). Rare outcome! Surprise: ${surprise.toFixed(2)} bits!`, 'gold');
        } else {
          addLog(`Result: ${outLabel} (p=${pOut.toFixed(2)}). UNBELIEVABLE! Surprise: ${surprise.toFixed(2)} bits!!!`, 'warn');
        }
      }
    }

    // Render Coin inside glass cylinder
    const coinY = ryCenter + coinHeightOffset;
    ctx.save();
    ctx.translate(rxCenter, coinY);
    ctx.scale(1.0, Math.abs(coinScaleY));
    
    // Outline & Face
    ctx.beginPath();
    ctx.arc(0, 0, 24, 0, Math.PI*2);
    ctx.fillStyle = coinResult === 1 ? '#f59e0b' : '#94a3b8'; // Gold vs Silver
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 1.8;
    ctx.fill();
    ctx.stroke();
    
    // Label on Coin face
    ctx.fillStyle = coinResult === 1 ? '#78350f' : '#334155';
    ctx.font = '900 11px monospace';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(coinResult === 1 ? "HEADS" : "TAILS", 0, 0);
    ctx.restore();

    // --- 3. BOTTOM GRAPH: Law of Large Numbers (Surprise Convergence) ---
    const gxMin = 40, gxMax = 550, gyMin = 360, gyMax = 460;
    const gw = gxMax - gxMin, gh = gyMax - gyMin;
    
    ctx.fillStyle = '#94a3b8';
    ctx.font = 'bold 11px sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText("CONVERGENCE: RUNNING SURPRISE AVERAGE vs ENTROPY", gxMin, gyMin - 24);
    
    ctx.fillStyle = '#64748b';
    ctx.font = '9px sans-serif';
    ctx.fillText(`Showing latest ${runningAverageSurprise.length} of ${coinSampleCount} trials; running mean uses all trials.`, gxMin, gyMin - 11);

    drawGrid(gxMin, gxMax, gyMin, gyMax, 5, 2);
    drawAxes(gxMin, gxMax, gyMin, gyMax);
    
    ctx.fillStyle = '#64748b';
    ctx.font = 'bold 9px monospace';
    ctx.textAlign = 'left';
    ctx.fillText(`Trial #${coinSampleCount ? coinSampleCount - runningAverageSurprise.length + 1 : 1}`, gxMin, gyMax + 12);
    ctx.textAlign = 'right';
    ctx.fillText(`Trial #${Math.max(10, coinSampleCount)}`, gxMax, gyMax + 12);
    
    ctx.textBaseline = 'middle';
    ctx.fillText("1.0", gxMin - 8, gyMin);
    ctx.fillText("0.0", gxMin - 8, gyMax);

    // Draw theoretical target entropy line (dashed purple)
    ctx.save();
    ctx.setLineDash([5, 4]);
    ctx.strokeStyle = '#a78bfa';
    ctx.lineWidth = 2;
    const targetY = gyMax - activeH * gh;
    ctx.beginPath();
    ctx.moveTo(gxMin, targetY);
    ctx.lineTo(gxMax, targetY);
    ctx.stroke();
    ctx.restore();
    
    // Draw running average line (glowing green/turquoise)
    if (runningAverageSurprise.length > 0) {
      ctx.beginPath();
      ctx.strokeStyle = '#4ECDC4';
      ctx.lineWidth = 2.5;
      
      const count = runningAverageSurprise.length;
      for (let i = 0; i < count; i++) {
        const val = runningAverageSurprise[i];
        const gx = gxMin + (i / Math.max(1, count - 1)) * gw;
        const gy = gyMax - Math.min(1.0, val) * gh;
        if (i === 0) ctx.moveTo(gx, gy);
        else ctx.lineTo(gx, gy);
      }
      ctx.stroke();
      
      // Node at the end
      const lastX = gxMax;
      const lastY = gyMax - Math.min(1.0, runningAverageSurprise[count - 1]) * gh;
      ctx.beginPath();
      ctx.arc(lastX, lastY, 4, 0, Math.PI*2);
      ctx.fillStyle = '#fff';
      ctx.strokeStyle = '#4ECDC4';
      ctx.lineWidth = 1.5;
      ctx.fill();
      ctx.stroke();
    }

  } else {
    // ==========================================
    // DRAW WEATHER 4-STATE MODE
    // ==========================================
    
    // --- 1. LEFT PANEL: Probability & Surprise Side-by-Side ---
    const wX = 40, wY = 90, barHeight = 22, barSpacing = 48;
    
    ctx.fillStyle = '#94a3b8';
    ctx.font = 'bold 11px sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText("PROBABILITY DISTRIBUTION vs SURPRISE (SHOCK VALUE)", wX, wY - 15);

    for (let i = 0; i < 4; i++) {
      const p = weatherP[i];
      const surprise = p <= 0.0001 ? 10 : -log2(p); // clamp extreme surprise to 10 bits
      const rowY = wY + i * barSpacing;
      
      // State Label
      ctx.fillStyle = '#e2e8f0';
      ctx.font = 'bold 10px sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText(weatherLabels[i], wX, rowY - 5);
      
      // --- Column A: Probability Bar ---
      const pBarWidth = 100;
      ctx.fillStyle = 'rgba(255,255,255,0.03)';
      ctx.fillRect(wX, rowY, pBarWidth, barHeight);
      ctx.strokeStyle = 'rgba(255,255,255,0.08)';
      ctx.strokeRect(wX, rowY, pBarWidth, barHeight);
      
      ctx.fillStyle = weatherColors[i];
      ctx.fillRect(wX, rowY, p * pBarWidth, barHeight);
      
      ctx.fillStyle = '#fff';
      ctx.font = 'bold 9px monospace';
      ctx.fillText(`${(p*100).toFixed(0)}%`, wX + 6, rowY + barHeight/2 + 3);
      
      // --- Column B: Surprise Bar (Logarithmic scale, 0 to 6 bits) ---
      const sX = wX + 130;
      const sBarMaxWidth = 100;
      ctx.fillStyle = 'rgba(255,255,255,0.03)';
      ctx.fillRect(sX, rowY, sBarMaxWidth, barHeight);
      ctx.strokeStyle = 'rgba(255,255,255,0.08)';
      ctx.strokeRect(sX, rowY, sBarMaxWidth, barHeight);
      
      // Draw surprise filling (outward, higher surprise = longer bar)
      const fillW = Math.min(6, surprise) / 6 * sBarMaxWidth;
      // Gradient glow
      const sGrad = ctx.createLinearGradient(sX, 0, sX + fillW, 0);
      sGrad.addColorStop(0, 'rgba(255,255,255,0.1)');
      sGrad.addColorStop(1, weatherColors[i]);
      
      ctx.fillStyle = sGrad;
      ctx.fillRect(sX, rowY, fillW, barHeight);
      
      // Draw border highlight
      ctx.strokeStyle = weatherColors[i];
      ctx.lineWidth = 1;
      ctx.strokeRect(sX, rowY, fillW, barHeight);
      
      // Value label
      ctx.fillStyle = '#cbd5e1';
      ctx.font = 'bold 9px monospace';
      ctx.fillText(`${surprise.toFixed(2)} bits`, sX + 6, rowY + barHeight/2 + 3);
    }
    
    const weatherEntropy = getWeatherEntropy();
    ctx.fillStyle = '#f1f5f9';
    ctx.font = '900 13px monospace';
    ctx.textAlign = 'left';
    ctx.fillText(`Average Surprise H(X) = ${weatherEntropy.toFixed(3)} bits`, wX, wY + 4 * barSpacing + 10);
    
    ctx.fillStyle = '#64748b';
    ctx.font = 'italic 10px sans-serif';
    ctx.fillText("Entropy drops to 0 when one weather becomes 100% certain!", wX, wY + 4 * barSpacing + 26);

    // --- 2. RIGHT PANEL: Entropy Balance Scale & Storm Chamber ---
    const scaleX = 450, scaleY = 100;
    
    // Draw pivots and beam of scale
    ctx.fillStyle = '#94a3b8';
    ctx.font = 'bold 11px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText("ENTROPY EQUILIBRIUM", scaleX, scaleY - 30);
    
    // Pivot triangle
    ctx.fillStyle = '#334155';
    ctx.beginPath();
    ctx.moveTo(scaleX, scaleY);
    ctx.lineTo(scaleX - 10, scaleY + 20);
    ctx.lineTo(scaleX + 10, scaleY + 20);
    ctx.fill();
    
    // Tilt calculation based on center of gravity of probability
    // Sunny (-2.0), Rainy (-0.6), Cloudy (0.6), Snowy (2.0)
    let tilt = (weatherP[0] * -1.5) + (weatherP[1] * -0.5) + (weatherP[2] * 0.5) + (weatherP[3] * 1.5);
    // Smooth damp/clamp tilt
    const maxTiltAngle = Math.PI / 8;
    const beamAngle = tilt * maxTiltAngle;
    
    ctx.save();
    ctx.translate(scaleX, scaleY);
    ctx.rotate(beamAngle);
    
    // Main beam
    ctx.strokeStyle = '#475569';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(-75, 0);
    ctx.lineTo(75, 0);
    ctx.stroke();
    
    // Hanging pans/indicators at Sunny, Rainy, Cloudy, Snowy horizontal offsets
    const offsets = [-75, -25, 25, 75];
    for (let i = 0; i < 4; i++) {
      ctx.fillStyle = weatherColors[i];
      // Size proportional to probability
      const panSize = 4 + weatherP[i] * 12;
      ctx.beginPath();
      ctx.arc(offsets[i], 12, panSize, 0, Math.PI*2);
      ctx.fill();
      
      // Hanging wire
      ctx.strokeStyle = 'rgba(255,255,255,0.1)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(offsets[i], 0);
      ctx.lineTo(offsets[i], 12);
      ctx.stroke();
    }
    ctx.restore();

    // --- 3. STORM CHAMBER & PARTICLES ---
    const bounds = { xMin: 320, xMax: 575, yMin: 200, yMax: 320 };
    const bw = bounds.xMax - bounds.xMin, bh = bounds.yMax - bounds.yMin;
    
    // Glass cylinder box
    ctx.fillStyle = 'rgba(0, 0, 0, 0.4)';
    ctx.fillRect(bounds.xMin, bounds.yMin, bw, bh);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
    ctx.lineWidth = 2.5;
    ctx.strokeRect(bounds.xMin, bounds.yMin, bw, bh);
    
    // Center glow for trigger
    ctx.fillStyle = '#475569';
    ctx.font = 'bold 9px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText("STORM SIMULATION CHAMBER", bounds.xMin + bw/2, bounds.yMin + 18);
    
    // Update and draw particles
    for (let i = activeParticles.length - 1; i >= 0; i--) {
      const p = activeParticles[i];
      p.update(bounds);
      p.draw(ctx);
    }

    // --- 4. BOTTOM GRAPH: Law of Large Numbers (Surprise Convergence) ---
    const wgxMin = 40, wgxMax = 550, wgyMin = 370, wgyMax = 470;
    const wgw = wgxMax - wgxMin, wgh = wgyMax - wgyMin;
    
    ctx.fillStyle = '#94a3b8';
    ctx.font = 'bold 11px sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText("CONVERGENCE: RUNNING SURPRISE AVERAGE vs ENTROPY", wgxMin, wgyMin - 24);
    
    ctx.fillStyle = '#64748b';
    ctx.font = '9px sans-serif';
    ctx.fillText(`Showing latest ${weatherRunningAvgSurprise.length} of ${weatherSampleCount} trials; running mean uses all trials.`, wgxMin, wgyMin - 11);

    drawGrid(wgxMin, wgxMax, wgyMin, wgyMax, 5, 2);
    drawAxes(wgxMin, wgxMax, wgyMin, wgyMax);
    
    ctx.fillStyle = '#64748b';
    ctx.font = 'bold 9px monospace';
    ctx.textAlign = 'left';
    ctx.fillText(`Trial #${weatherSampleCount ? weatherSampleCount - weatherRunningAvgSurprise.length + 1 : 1}`, wgxMin, wgyMax + 12);
    ctx.textAlign = 'right';
    ctx.fillText(`Trial #${Math.max(10, weatherSampleCount)}`, wgxMax, wgyMax + 12);
    
    ctx.textBaseline = 'middle';
    ctx.fillText("4.0", wgxMin - 8, wgyMin);
    ctx.fillText("0.0", wgxMin - 8, wgyMax);

    // Draw theoretical target entropy line (dashed purple)
    ctx.save();
    ctx.setLineDash([5, 4]);
    ctx.strokeStyle = '#a78bfa';
    ctx.lineWidth = 2;
    const wTargetY = wgyMax - (weatherEntropy / 4.0) * wgh; // Scale to 4.0 bits max height
    ctx.beginPath();
    ctx.moveTo(wgxMin, wTargetY);
    ctx.lineTo(wgxMax, wTargetY);
    ctx.stroke();
    ctx.restore();
    
    // Draw running average line (glowing green/turquoise)
    if (weatherRunningAvgSurprise.length > 0) {
      ctx.beginPath();
      ctx.strokeStyle = '#4ECDC4';
      ctx.lineWidth = 2.5;
      
      const count = weatherRunningAvgSurprise.length;
      for (let i = 0; i < count; i++) {
        const val = weatherRunningAvgSurprise[i];
        const gx = wgxMin + (i / Math.max(1, count - 1)) * wgw;
        const gy = wgyMax - Math.min(4.0, val) / 4.0 * wgh;
        if (i === 0) ctx.moveTo(gx, gy);
        else ctx.lineTo(gx, gy);
      }
      ctx.stroke();
      
      // Node at the end
      const lastX = wgxMax;
      const lastY = wgyMax - Math.min(4.0, weatherRunningAvgSurprise[count - 1]) / 4.0 * wgh;
      ctx.beginPath();
      ctx.arc(lastX, lastY, 4, 0, Math.PI*2);
      ctx.fillStyle = '#fff';
      ctx.strokeStyle = '#4ECDC4';
      ctx.lineWidth = 1.5;
      ctx.fill();
      ctx.stroke();
    }
  }

  drawAnimationFrameId = requestAnimationFrame(draw);
}

// Initialization
let drawAnimationFrameId;
buildSliders();
draw();
window.addEventListener('pagehide', () => {
  stopAuto();
  cancelAnimationFrame(drawAnimationFrameId);
}, { once: true });

</script>
</body>
</html>
"""
    components.html(html_code, height=670, scrolling=False)


def main():
    st.title("🌀 Page 58: Entropy — Average Uncertainty")

    st.markdown(
        """
        In [Page 57: Information & Surprise](file:///d:/physics-simulation/pages/57Information%20&%20Surprise.py), we explored **surprise** ($I(p) = -\\log_2(p)$) — a concept that measures the shock of a *single* event occurring. 
        
        But what if you are looking at a system with **multiple possible outcomes** (like forecasting the weather or predicting the next token in a ChatGPT generation)? How do you measure the **overall predictability or average uncertainty** of the entire system?
        
        This is where **Shannon Entropy ($H$)** comes in! Entropy is simply the **expected value (average)** of surprise across all possible outcomes.
        """
    )

    st.divider()
    
    col1, col2 = st.columns([1.1, 0.9])
    
    with col1:
        st.subheader("The Mathematics of Average Uncertainty 🧮")
        st.markdown(
            r"""
            For a system $X$ with $n$ possible outcomes, each with probability $p_i$, the overall entropy $H(X)$ is defined as:
            
            $$H(X) = \sum_{i=1}^n p_i I(p_i) = -\sum_{i=1}^n p_i \log_2(p_i)$$
            
            * **Unit:** **Bits** (or Shannons). A system with $1\text{ bit}$ of entropy has the same uncertainty as a perfect 50/50 coin flip.
            * **The Weighted Average:** Notice how we multiply the surprise $-\log_2(p_i)$ by its probability $p_i$. A highly rare event has massive surprise, but because it happens so rarely, it contributes very little to the **average** surprise!
            * **Binary Entropy (2-State):** If there are only two outcomes (Heads with probability $p$, and Tails with $1-p$), the formula simplifies to:
              $$H(p) = -p \log_2(p) - (1-p) \log_2(1-p)$$
            """
        )
        
    with col2:
        st.subheader("Interactive Insights 💡")
        st.info("🤷 **Maximum Entropy:** Occurs when all outcomes are equally likely (uniform distribution). There is complete chaos; prediction is impossible.")
        st.success("🎯 **Minimum Entropy ($H=0$):** Occurs when one outcome is 100% guaranteed. There is zero uncertainty, meaning the system is completely predictable.")
        st.warning("📉 **The Curve shape:** For binary outcomes, the curve peaks precisely at $p=0.5$ ($H = 1\text{ bit}$) and drops down to $0$ on both sides. Adding certainty drops entropy!")

    st.divider()
    st.markdown("### 🧪 Shannon's Entropy Laboratory Sandbox")
    st.markdown(
        "Choose a mode below to experiment with average uncertainty! Drag the **sliders** to adjust the probabilities live. "
        "Click **Toss Coin** / **Generate Weather** (or toggle **AUTO**) to simulate draws and observe how the running average surprise (green) **smooths out and converges** to the theoretical entropy (dashed purple) via the Law of Large Numbers!"
    )
    
    render_entropy_lab()

    st.divider()
    st.subheader("🤖 Bridge to AI: Why Neural Networks Love Low Entropy")
    st.markdown(
        r"""
        In machine learning, entropy is the ultimate compass. Here is why it rules the AI landscape:
        
        #### 1. Information Gain in Decision Trees 🌳
        When a Decision Tree (like ID3) decides how to split your dataset (e.g. splitting email by "Has Link" to detect Spam), it calculates the **Information Gain**:
        $$\text{Information Gain} = H(\text{Parent}) - H(\text{Children})$$
        The tree chooses the split that **maximizes Information Gain** — which is just a fancy way of saying it wants to **reduce entropy (uncertainty)** as much as possible, splitting data into clean, predictable categories!
        
        #### 2. Entropy Regularization in Reinforcement Learning 🤖
        When training an RL agent (like a robot learning to walk), we don't want it to lock into one strategy too early and get stuck. 
        We add an **entropy bonus** to its loss function:
        $$\text{Loss} = \text{Policy Loss} - \alpha \cdot H(\pi)$$
        This penalizes the agent for being too certain too quickly, forcing it to keep exploring new actions because **higher entropy = more exploratory freedom**!
        
        #### 3. The Core of Cross-Entropy Loss 🎯
        When training classifiers, **Cross-Entropy** measures the difference between the true distribution (which usually has $H=0$ since the label is certain) and the model's predicted distribution. Minimizing cross-entropy is equivalent to shrinking the model's uncertainty, pushing the model's prediction closer to certainty.
        """
    )
    
    st.divider()
    st.markdown(
        '<div style="color:#94a3b8;font-size:0.95rem;">Page 58 — you\'ve mastered how entropy gauges average uncertainty across a system. But what happens when we compare a predicted distribution against real-world labels? Next: we discover the cornerstone penalty of classifier training — <b>Cross-Entropy (Page 59)</b>!</div>',
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
