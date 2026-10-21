import streamlit as st
import streamlit.components.v1 as components
import numpy as np

st.set_page_config(page_title="Information & Surprise", layout="wide")

def render_surprise_lab():
    html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{
  font-family:sans-serif;
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
.event-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  margin-top: 5px;
}
.event-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 10px;
  padding: 8px 6px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}
.event-card:hover {
  background: rgba(255, 255, 255, 0.07);
  border-color: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
}
.event-card.active {
  background: rgba(167, 139, 250, 0.12);
  border-color: #a78bfa;
  box-shadow: 0 0 12px rgba(167, 139, 250, 0.25);
}
.event-card .emoji {
  font-size: 22px;
}
.event-card .name {
  font-size: 11px;
  font-weight: 700;
  color: #e2e8f0;
}
.event-card .p-text {
  font-size: 10px;
  font-weight: 800;
  color: #818cf8;
}

/* Slider styling */
.slider-group {
  margin-top: 5px;
}
.slabel-row {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  font-weight: 700;
  color: #cbd5e1;
  margin-bottom: 6px;
}
.sval {
  font-family: monospace;
  font-size: 15px;
  font-weight: 900;
  color: #a78bfa;
}
input[type=range] {
  width: 100%;
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  outline: none;
  -webkit-appearance: none;
  cursor: pointer;
}
input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #a78bfa;
  box-shadow: 0 0 10px #a78bfa;
  cursor: pointer;
  transition: transform 0.1s;
}
input[type=range]::-webkit-slider-thumb:hover {
  transform: scale(1.15);
}

.trigger-btn {
  background: linear-gradient(135deg, #818cf8, #a78bfa);
  color: #0f172a;
  border: none;
  padding: 12px;
  border-radius: 10px;
  font-weight: 800;
  font-size: 14px;
  letter-spacing: 0.5px;
  cursor: pointer;
  width: 100%;
  text-transform: uppercase;
  transition: all 0.2s;
  box-shadow: 0 4px 15px rgba(167, 139, 250, 0.3);
  margin-top: 10px;
}
.trigger-btn:hover {
  filter: brightness(1.1);
  box-shadow: 0 6px 20px rgba(167, 139, 250, 0.45);
  transform: translateY(-1px);
}
.trigger-btn:active {
  transform: translateY(1px);
}

/* Lab Console Log */
.terminal-log {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 12px;
  font-family: monospace;
  font-size: 11px;
  color: #4ade80;
  height: 115px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.log-line {
  line-height: 1.3;
}
.log-line span.cyan { color: #22d3ee; }
.log-line span.gold { color: #facc15; }
.log-line span.rose { color: #fb7185; }

/* Canvas Visualizer styling */
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

/* Shake classes applied dynamically */
.shake-light {
  animation: shakeLight 0.3s ease-in-out;
}
.shake-med {
  animation: shakeMed 0.5s ease-in-out;
}
.shake-heavy {
  animation: shakeHeavy 0.8s cubic-bezier(.36,.07,.19,.97) both;
}

@keyframes shakeLight {
  0%, 100% { transform: translate(0, 0); }
  25% { transform: translate(-1px, 1px); }
  50% { transform: translate(1px, -1px); }
  75% { transform: translate(-1px, -1px); }
}
@keyframes shakeMed {
  0%, 100% { transform: translate(0, 0); }
  10%, 90% { transform: translate(-2px, 2px); }
  30%, 70% { transform: translate(2px, -2px); }
  50% { transform: translate(-3px, -1px); }
}
@keyframes shakeHeavy {
  0%, 100% { transform: translate(0, 0); }
  10%, 90% { transform: translate(-4px, 4px) rotate(-0.5deg); }
  30%, 70% { transform: translate(5px, -3px) rotate(0.8deg); }
  50% { transform: translate(-6px, 1px) rotate(-1deg); }
  20%, 80% { transform: translate(3px, 3px) rotate(0.5deg); }
}
</style>
</head>
<body>

<div class="outer-container">
  <div class="app-layout">
    <!-- LEFT PANEL: Controls, Presets, and Log -->
    <div class="panel-left">
      <div class="card">
        <h2>Shannon's Shock-O-Meter ⚡</h2>
        <p class="sub">Adjust probability and trigger the event to see surprise transformed into physical spark energy and screen vibration!</p>
      </div>

      <div class="card">
        <div class="slabel-row">
          <span>Event Probability (p)</span>
          <span id="p-val" class="sval">0.5000</span>
        </div>
        <div class="slider-group">
          <!-- Fine steps to allow low probability slider dragging -->
          <input type="range" id="p-slider" min="0.0001" max="1.0" step="0.0001" value="0.5">
        </div>
        <div style="display:flex; justify-content:space-between; font-size:11px; color:#64748b; margin-top:5px;">
          <span>Rare (0.01%)</span>
          <span id="fraction-text">Chance: 1 in 2</span>
          <span>Certain (100%)</span>
        </div>
      </div>

      <div class="card">
        <h3 style="font-size:12px; text-transform:uppercase; letter-spacing:1px; color:#94a3b8; margin-bottom:8px;">Real-World Event Presets</h3>
        <div class="event-grid" id="presets">
          <div class="event-card" data-p="0.99999" data-name="☀️ Sunrise Tomorrow" data-desc="Practically guaranteed. Hearing this news yields 0 bits of information.">
            <span class="emoji">☀️</span>
            <span class="name">Sunrise</span>
            <span class="p-text">~100%</span>
          </div>
          <div class="event-card active" data-p="0.5" data-name="🪙 Fair Coin Flip" data-desc="Perfect 50/50 chance. Yields exactly 1.0 bit of surprise.">
            <span class="emoji">🪙</span>
            <span class="name">Coin Flip</span>
            <span class="p-text">50.0%</span>
          </div>
          <div class="event-card" data-p="0.0278" data-name="🎲 Double Sixes" data-desc="Rolling double sixes on two fair dice. Probability = 1/36 (~2.78%).">
            <span class="emoji">🎲</span>
            <span class="name">Double Sixes</span>
            <span class="p-text">2.78%</span>
          </div>
          <div class="event-card" data-p="0.0192" data-name="🃏 Ace of Spades" data-desc="Drawing the Ace of Spades from a standard deck. Probability = 1/52 (~1.92%).">
            <span class="emoji">🃏</span>
            <span class="name">Ace of Spades</span>
            <span class="p-text">1.92%</span>
          </div>
          <div class="event-card" data-p="0.001" data-name="⚡ Lightning Strike" data-desc="Being struck by lightning locally. Probability set to 0.1% for demonstration.">
            <span class="emoji">⚡</span>
            <span class="name">Lightning</span>
            <span class="p-text">0.10%</span>
          </div>
          <div class="event-card" data-p="0.0001" data-name="🎰 Grand Lottery" data-desc="Winning a major lottery jackpot. Extremely low probability (0.01%).">
            <span class="emoji">🎰</span>
            <span class="name">Lottery Win</span>
            <span class="p-text">0.01%</span>
          </div>
        </div>
        
        <button class="trigger-btn" id="trigger-btn">Trigger Event ⚡</button>
      </div>

      <div class="terminal-log" id="log-box">
        <div class="log-line">> <span class="cyan">Shock-O-Meter Console Online.</span> Ready for event triggers.</div>
      </div>
    </div>

    <!-- RIGHT PANEL: Animated Gauge, Spark Chamber, and Graph -->
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
const container = document.getElementById('canvas-wrap');

const pSlider = document.getElementById('p-slider');
const pValEl = document.getElementById('p-val');
const fractionTextEl = document.getElementById('fraction-text');
const triggerBtn = document.getElementById('trigger-btn');
const logBox = document.getElementById('log-box');
const presetCards = document.querySelectorAll('.event-card');

// Simulation State
let currentP = 0.5;
let currentEventName = "🪙 Fair Coin Flip";
let currentEventDesc = "Perfect 50/50 chance. Yields exactly 1.0 bit of surprise.";
let particles = [];
let flashAlpha = 0;
let flashColor = '#a78bfa';

// Bounds of the Spark Chamber inside the canvas (expanded to height 500)
const chamber = {
  xMin: 340,
  xMax: 570,
  yMin: 30,
  yMax: 280,
  xCenter: 455,
  yCenter: 155
};

// Particle Class
class Spark {
  constructor(x, y, p) {
    this.x = x;
    this.y = y;
    
    const bits = -Math.log2(p);
    const intensity = Math.min(bits / 12, 1.5);
    
    const speed = 1.5 + intensity * 7.5;
    const angle = Math.random() * Math.PI * 2;
    
    this.vx = Math.cos(angle) * speed * (0.5 + Math.random() * 0.8);
    this.vy = Math.sin(angle) * speed * (0.5 + Math.random() * 0.8) - (intensity * 1.5);
    
    this.size = 1.2 + Math.random() * (1 + intensity * 3.5);
    this.life = 25 + Math.random() * (20 + intensity * 50);
    this.maxLife = this.life;
    
    this.gravity = 0.12;
    this.bounce = 0.55 + Math.random() * 0.15;
    
    // Theme colors based on surprise bits
    if (bits < 0.1) {
      this.color = `hsla(200, 20%, 65%, ${Math.random()})`; // Gray/Dull
    } else if (bits < 2.0) {
      this.color = `hsla(180, 85%, 60%, ${Math.random()})`; // Turquoise
    } else if (bits < 6.0) {
      this.color = `hsla(270, 90%, 65%, ${Math.random()})`; // Neon Purple
    } else {
      this.color = `hsla(${35 + Math.random() * 20}, 100%, 60%, ${Math.random()})`; // Hot Gold/Orange
    }
  }

  update() {
    this.vy += this.gravity;
    this.x += this.vx;
    this.y += this.vy;
    
    // Spark Chamber Collisions
    if (this.x < chamber.xMin) {
      this.x = chamber.xMin;
      this.vx = -this.vx * this.bounce;
    }
    if (this.x > chamber.xMax) {
      this.x = chamber.xMax;
      this.vx = -this.vx * this.bounce;
    }
    if (this.y < chamber.yMin) {
      this.y = chamber.yMin;
      this.vy = -this.vy * this.bounce;
    }
    if (this.y > chamber.yMax) {
      this.y = chamber.yMax;
      this.vy = -this.vy * this.bounce;
      this.vx *= 0.95; // Ground friction
    }
    
    this.life--;
  }

  draw(c) {
    const alpha = Math.max(0, this.life / this.maxLife);
    c.beginPath();
    c.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    
    // Swap active transparency
    const hslBase = this.color.substring(0, this.color.lastIndexOf(','));
    c.fillStyle = `${hslBase}, ${alpha})`;
    
    if (this.size > 3) {
      c.shadowBlur = 6;
      c.shadowColor = c.fillStyle;
    }
    c.fill();
    c.shadowBlur = 0;
  }
}

// Write to terminal console
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

// Trigger CSS screen shake based on surprise
function triggerShake(bits) {
  container.classList.remove('shake-light', 'shake-med', 'shake-heavy');
  void container.offsetWidth; // Force CSS reflow
  
  if (bits >= 8) {
    container.classList.add('shake-heavy');
  } else if (bits >= 4) {
    container.classList.add('shake-med');
  } else if (bits >= 1) {
    container.classList.add('shake-light');
  }
}

// Generate the spark explosion
function spawnSparks() {
  const bits = -Math.log2(currentP);
  
  // Count grows quadratically for high surprise
  const count = Math.max(2, Math.floor(bits * bits * 0.9) + 2);
  
  for(let i = 0; i < count; i++) {
    particles.push(new Spark(chamber.xCenter, chamber.yCenter, currentP));
  }
  
  // Set Spark Chamber Flash
  flashAlpha = Math.min(0.85, bits / 12);
  if (bits < 0.1) {
    flashColor = 'rgba(148, 163, 184, 0.4)';
    addLog(`Common event occurred. Surprise: ${bits.toFixed(3)} bits. Boring.`, 'info');
  } else if (bits < 4.0) {
    flashColor = 'rgba(78, 205, 196, 0.6)';
    addLog(`Interesting event triggered! Surprise: ${bits.toFixed(3)} bits.`, 'info');
  } else if (bits < 8.0) {
    flashColor = 'rgba(167, 139, 250, 0.7)';
    addLog(`WOW! Rare event occurred! Surprise: ${bits.toFixed(3)} bits!`, 'gold');
  } else {
    flashColor = 'rgba(251, 191, 36, 0.9)';
    addLog(`HOLY SHANNON! Astronomical surprise: ${bits.toFixed(3)} bits!!!`, 'warn');
  }
  
  triggerShake(bits);
}

// Update value displays and fractions
function updateValues(val, isPreset = false) {
  currentP = parseFloat(val);
  pSlider.value = currentP;
  pValEl.innerText = currentP.toFixed(4);
  
  const inv = Math.round(1 / currentP);
  fractionTextEl.innerText = `Chance: 1 in ${inv.toLocaleString()}`;
  
  // Remove preset active tags if dragged
  if (!isPreset) {
    presetCards.forEach(c => {
      // Allow exact match to light up preset
      if (Math.abs(parseFloat(c.dataset.p) - currentP) < 0.0002) {
        c.classList.add('active');
        currentEventName = c.dataset.name;
        currentEventDesc = c.dataset.desc;
      } else {
        c.classList.remove('active');
      }
    });
    
    // Default custom event desc
    const bits = -Math.log2(currentP);
    if (!document.querySelector('.event-card.active')) {
      currentEventName = "🍀 Custom Event";
      currentEventDesc = `User-defined probability. Generates exactly ${bits.toFixed(3)} bits of surprise.`;
    }
  }
}

// Draw the Shock-O-Meter Dial Gauge (adjusted coordinates)
function drawGauge(bits) {
  const cx = 170;
  const cy = 155;
  const r = 90;
  const startAngle = Math.PI * 0.92;
  const endAngle = Math.PI * 2.08;
  
  // 1. Draw Gauge Arc Backing
  ctx.beginPath();
  ctx.arc(cx, cy, r, startAngle, endAngle);
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.06)';
  ctx.lineWidth = 14;
  ctx.lineCap = 'round';
  ctx.stroke();
  
  // 2. Draw Color Filled Track (Gradient from green to purple to gold/red)
  const arcGrad = ctx.createLinearGradient(cx - r, cy, cx + r, cy);
  arcGrad.addColorStop(0, '#4de880'); // Green
  arcGrad.addColorStop(0.3, '#22d3ee'); // Blue
  arcGrad.addColorStop(0.6, '#a78bfa'); // Purple
  arcGrad.addColorStop(1.0, '#fb7185'); // Rose/Pink
  
  // How much track to fill based on bits (0 to 10 scale)
  const fillRatio = Math.min(1.0, bits / 10);
  const fillEndAngle = startAngle + fillRatio * (endAngle - startAngle);
  
  if(bits > 0.01) {
    ctx.beginPath();
    ctx.arc(cx, cy, r, startAngle, fillEndAngle);
    ctx.strokeStyle = arcGrad;
    ctx.lineWidth = 14;
    ctx.lineCap = 'round';
    ctx.stroke();
  }
  
  // 3. Major Scale Ticks & Labels
  ctx.fillStyle = '#64748b';
  ctx.font = 'bold 10px monospace';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  
  for(let i = 0; i <= 10; i += 2) {
    const angle = startAngle + (i / 10) * (endAngle - startAngle);
    const tx = cx + (r - 20) * Math.cos(angle);
    const ty = cy + (r - 20) * Math.sin(angle);
    ctx.fillText(i, tx, ty);
    
    // Ticks
    const tickOuterX = cx + r * Math.cos(angle);
    const tickOuterY = cy + r * Math.sin(angle);
    const tickInnerX = cx + (r - 6) * Math.cos(angle);
    const tickInnerY = cy + (r - 6) * Math.sin(angle);
    
    ctx.beginPath();
    ctx.moveTo(tickInnerX, tickInnerY);
    ctx.lineTo(tickOuterX, tickOuterY);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
    ctx.lineWidth = 2;
    ctx.stroke();
  }
  
  // 4. Draw Needle with REDLINE Tachometer Shake if bits > 10
  let needleAngle = startAngle + fillRatio * (endAngle - startAngle);
  
  if (bits > 10) {
    const jitter = (bits - 10) * 0.018 * (Math.random() - 0.5);
    needleAngle += jitter;
  }
  
  ctx.beginPath();
  ctx.moveTo(cx, cy);
  const pointerX = cx + (r - 8) * Math.cos(needleAngle);
  const pointerY = cy + (r - 8) * Math.sin(needleAngle);
  ctx.lineTo(pointerX, pointerY);
  ctx.strokeStyle = bits >= 9.0 ? '#fb7185' : '#a78bfa';
  ctx.lineWidth = 3.5;
  ctx.lineCap = 'round';
  ctx.shadowColor = ctx.strokeStyle;
  ctx.shadowBlur = 8;
  ctx.stroke();
  ctx.shadowBlur = 0;
  
  // Center Pin
  ctx.beginPath();
  ctx.arc(cx, cy, 8, 0, Math.PI * 2);
  ctx.fillStyle = '#1e293b';
  ctx.strokeStyle = '#a78bfa';
  ctx.lineWidth = 3;
  ctx.fill();
  ctx.stroke();
  
  // 5. Large Text Readout underneath
  ctx.fillStyle = '#f1f5f9';
  ctx.font = '900 24px monospace';
  ctx.textAlign = 'center';
  ctx.fillText(bits.toFixed(3), cx, cy + 45);
  
  ctx.fillStyle = '#818cf8';
  ctx.font = 'bold 9px sans-serif';
  ctx.fillText("SURPRISE (BITS)", cx, cy + 62);
  
  // Description Tag
  ctx.fillStyle = '#64748b';
  ctx.font = 'italic 10px sans-serif';
  ctx.fillText(currentEventName, cx, cy - r - 15);
}

// Draw the curve graph (adjusted coordinates)
function drawGraph(p) {
  const xMin = 50;
  const xMax = 550;
  const yMin = 340;
  const yMax = 460;
  const gw = xMax - xMin;
  const gh = yMax - yMin;
  
  // Draw Background Grid
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.03)';
  ctx.lineWidth = 1;
  for(let i = 1; i <= 4; i++) {
    // X vertical grids
    const gx = xMin + (i / 5) * gw;
    ctx.beginPath(); ctx.moveTo(gx, yMin); ctx.lineTo(gx, yMax); ctx.stroke();
    // Y horizontal grids
    const gy = yMin + (i / 5) * gh;
    ctx.beginPath(); ctx.moveTo(xMin, gy); ctx.lineTo(xMax, gy); ctx.stroke();
  }
  
  // Graph Axes
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(xMin, yMin - 10);
  ctx.lineTo(xMin, yMax);
  ctx.lineTo(xMax + 10, yMax);
  ctx.stroke();
  
  // Labels
  ctx.fillStyle = '#64748b';
  ctx.font = 'bold 9px monospace';
  ctx.textAlign = 'center';
  ctx.fillText("p=0", xMin, yMax + 12);
  ctx.fillText("p=0.5", xMin + gw * 0.5, yMax + 12);
  ctx.fillText("p=1.0 (Certain)", xMax, yMax + 12);
  
  ctx.textAlign = 'right';
  ctx.textBaseline = 'middle';
  ctx.fillText("10 bits", xMin - 8, yMin);
  ctx.fillText("0 bits", xMin - 8, yMax);
  
  // Plot the curve: I(p) = -log2(p)
  ctx.beginPath();
  let first = true;
  for(let cx = xMin + 1; cx <= xMax; cx++) {
    // Map canvas X back to p
    const cp = (cx - xMin) / gw;
    const cbits = Math.min(10.0, -Math.log2(cp));
    
    // Map bits back to canvas Y
    const cy = yMax - (cbits / 10.0) * gh;
    
    if (first) {
      ctx.moveTo(cx, cy);
      first = false;
    } else {
      ctx.lineTo(cx, cy);
    }
  }
  
  // Smooth curve color
  const curveGrad = ctx.createLinearGradient(xMin, 0, xMax, 0);
  curveGrad.addColorStop(0, '#fb7185'); // Low p
  curveGrad.addColorStop(0.3, '#a78bfa'); // Med p
  curveGrad.addColorStop(1.0, '#4ECDC4'); // High p
  
  ctx.strokeStyle = curveGrad;
  ctx.lineWidth = 3;
  ctx.stroke();
  
  // Active glowing node coordinates
  const activeBits = Math.min(10.0, -Math.log2(p));
  const activeX = xMin + p * gw;
  const activeY = yMax - (activeBits / 10.0) * gh;
  
  // Draw Projections
  ctx.setLineDash([4, 4]);
  ctx.strokeStyle = 'rgba(167, 139, 250, 0.4)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(activeX, activeY);
  ctx.lineTo(activeX, yMax); // to x axis
  ctx.moveTo(activeX, activeY);
  ctx.lineTo(xMin, activeY); // to y axis
  ctx.stroke();
  ctx.setLineDash([]);
  
  // Draw Active point dot
  ctx.beginPath();
  ctx.arc(activeX, activeY, 6, 0, Math.PI * 2);
  ctx.fillStyle = '#fff';
  ctx.strokeStyle = activeBits >= 9.0 ? '#fb7185' : '#a78bfa';
  ctx.lineWidth = 2.5;
  ctx.shadowColor = ctx.strokeStyle;
  ctx.shadowBlur = 10;
  ctx.fill();
  ctx.stroke();
  ctx.shadowBlur = 0;
  
  // Print active surprise formula overlay
  ctx.fillStyle = '#cbd5e1';
  ctx.font = 'bold 11px monospace';
  ctx.textAlign = 'right';
  ctx.fillText(`I(${p.toFixed(4)}) = -log₂(${p.toFixed(4)}) = ${activeBits.toFixed(2)} bits`, xMax, yMin);
}

// Render Loop
function render() {
  // Clear screen
  ctx.fillStyle = '#0f172a';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  
  const currentBits = -Math.log2(currentP);
  
  // --- 1. SPARK CHAMBER DRAWING ---
  // Draw outer chamber glass container
  ctx.fillStyle = 'rgba(0, 0, 0, 0.4)';
  ctx.fillRect(chamber.xMin, chamber.yMin, chamber.xMax - chamber.xMin, chamber.yMax - chamber.yMin);
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
  ctx.lineWidth = 2.5;
  ctx.strokeRect(chamber.xMin, chamber.yMin, chamber.xMax - chamber.xMin, chamber.yMax - chamber.yMin);
  
  // Sci-fi targets inside chamber
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.035)';
  ctx.setLineDash([4, 4]);
  ctx.beginPath();
  ctx.arc(chamber.xCenter, chamber.yCenter, 45, 0, Math.PI * 2);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(chamber.xCenter, chamber.yMin + 20); ctx.lineTo(chamber.xCenter, chamber.yMax - 20);
  ctx.moveTo(chamber.xMin + 20, chamber.yCenter); ctx.lineTo(chamber.xMax - 20, chamber.yCenter);
  ctx.stroke();
  ctx.setLineDash([]);
  
  // Spawn Chamber Title
  ctx.fillStyle = '#475569';
  ctx.font = 'bold 9px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText("EVENT SPARK CHAMBER", chamber.xCenter, chamber.yMin + 15);
  
  // Spark Core Trigger Box in center
  ctx.beginPath();
  ctx.arc(chamber.xCenter, chamber.yCenter, 8, 0, Math.PI * 2);
  ctx.fillStyle = currentBits >= 9.0 ? 'rgba(251, 113, 133, 0.8)' : 'rgba(167, 139, 250, 0.8)';
  ctx.fill();
  
  // Chamber Flash animation overlay
  if (flashAlpha > 0) {
    ctx.fillStyle = flashColor.replace(/[^,]+(?=\))/, flashAlpha);
    ctx.fillRect(chamber.xMin + 1, chamber.yMin + 1, (chamber.xMax - chamber.xMin) - 2, (chamber.yMax - chamber.yMin) - 2);
    flashAlpha -= 0.04;
  }
  
  // Update and draw sparkles
  for (let i = particles.length - 1; i >= 0; i--) {
    const s = particles[i];
    s.update();
    s.draw(ctx);
    if (s.life <= 0) {
      particles.splice(i, 1);
    }
  }
  
  // --- 2. GAUGE & GRAPH ---
  drawGauge(currentBits);
  drawGraph(currentP);
  
  requestAnimationFrame(render);
}

// Presets grid click logic
presetCards.forEach(card => {
  card.addEventListener('click', () => {
    presetCards.forEach(c => c.classList.remove('active'));
    card.classList.add('active');
    
    currentEventName = card.dataset.name;
    currentEventDesc = card.dataset.desc;
    
    updateValues(card.dataset.p, true);
    
    // Auto trigger on preset clicks for immediate juicy response
    spawnSparks();
  });
});

// Slider inputs
pSlider.addEventListener('input', (e) => {
  updateValues(e.target.value, false);
});

// Button triggers
triggerBtn.addEventListener('click', () => {
  spawnSparks();
});

// Init and start loop
updateValues(0.5, true);
render();

</script>
</body>
</html>
"""
    components.html(html_code, height=670, scrolling=False)

def main():
    st.title("💡 Page 57: Information & Surprise")

    st.markdown(
        """
        Imagine you open the morning news and read:
        
        * **Headline A:** *"The Sun Rose this Morning!"*
        * **Headline B:** *"Snow Falls in the Sahara Desert!"*
        
        Which one catches your eye? Which one makes you double-check the source, text your friends, and scream *"No way!"*?
        
        Headline B, obviously. But why? Because **Headline A has a probability of 99.9999%** — it is completely certain and tells you nothing you didn't already know. **Headline B is extremely rare (0.01%)** — it carries massive shock value.
        
        In 1948, the father of modern communication, **Claude Shannon**, unlocked a beautiful mathematical truth that forms the bedrock of modern AI:
        
        $$\\text{Information} \\propto \\text{Surprise}$$
        
        Hearing that a 100% certain event occurred yields **zero information**. Hearing that a rare, low-probability event occurred yields **immense information**.
        """
    )

    st.divider()
    
    col1, col2 = st.columns([1.1, 0.9])
    
    with col1:
        st.subheader("The Math of Shock 🧮")
        st.markdown(
            """
            Shannon mathematically defined the self-information (or "surprise") of an event $x$ with probability $p$ as:
            
            $$I(p) = -\\log_2(p)$$
            
            * **Unit:** **Bits** (or Shannons). 1 bit represents the surprise of a perfect 50/50 choice.
            * **Why the Negative?** Since $p \\le 1$, $\\log_2(p)$ is negative. The negative sign flips it positive, ensuring that lower probability equals higher surprise!
            * **Why a Logarithm?** 
              Suppose you flip a coin ($p_1 = 0.5$) and roll a die ($p_2 = 1/6$). Their joint probability is $p_1 \\times p_2 = 1/12$. 
              
              But intuitively, the surprise you feel should be the **sum** of the two surprises:
              
              $$I(\\text{both}) = I(\\text{coin}) + I(\\text{die})$$
              
              The logarithm is the **only** function that turns multiplication (combining probabilities) into addition (adding surprises)!
              
              $$\\log(A \\cdot B) = \\log(A) + \\log(B)$$
            """
        )
        
    with col2:
        st.subheader("Properties of Surprise ⚡")
        st.info("🥱 **Certain Event ($p=1$):** $I(1) = -\\log_2(1) = 0$ bits of surprise.")
        st.success("🪙 **50/50 Event ($p=0.5$):** $I(0.5) = -\\log_2(0.5) = 1$ bit of surprise.")
        st.warning("🎲 **Rare Event ($p=0.01$):** $I(0.01) \\approx 6.64$ bits of surprise.")
        st.error("🤯 **Extreme Event ($p \\to 0$):** $I(p) \\to \\infty$ bits of surprise!")

    st.divider()
    st.markdown("### 🧪 Shannon's Shock-O-Meter Laboratory")
    st.markdown(
        "Click on a **preset event** below or drag the **probability slider** to see how surprise scales. "
        "Click **Trigger Event** to release sparks into the chamber. Notice how rare events generate massive kinetic energy and rattle the instruments!"
    )
    
    render_surprise_lab()

    st.divider()
    st.subheader("🤖 Bridge to AI: Why Neural Networks Hate Being Surprised")
    st.markdown(
        """
        In classification tasks (like teaching an AI to recognize Cats vs. Dogs), the model outputs a probability $p$ representing its confidence in the correct label.
        
        If the true image is a **Cat**:
        * **Scenario 1 (Confident & Correct):** The model predicts $p=0.99$ for Cat.
          $$\\text{Surprise} = -\\log_2(0.99) \\approx 0.014\\text{ bits}$$
          The model feels practically zero surprise. The loss is tiny.
          
        * **Scenario 2 (Confidently Wrong):** The model predicts $p=0.01$ for Cat (it was 99% sure it was a dog!).
          $$\\text{Surprise} = -\\log_2(0.01) \\approx 6.64\\text{ bits}$$
          The model is **shocked**! It got a massive shock penalty.
          
        This surprise calculation is exactly what we call **Cross-Entropy Loss**! Training a neural network is quite literally the process of **minimizing the model's surprise** when looking at training data.
        """
    )
    
    st.divider()
    st.markdown(
        '<div style="color:#94a3b8;font-size:0.95rem;">Page 57 — you\'ve experienced how single events spark surprise. But what is the <b>average</b> surprise across a whole landscape of possibilities? Next: we discover the core metric of uncertainty — <b>Entropy (Page 58)</b>!</div>',
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
