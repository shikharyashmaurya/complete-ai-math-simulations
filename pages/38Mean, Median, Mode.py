import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Mean, Median, Mode", layout="wide", page_icon="📊")

st.title("📊 38. Mean, Median, Mode")
st.markdown("### The Three Sisters of Statistics")
st.write("When we have a bunch of numbers, we often want to summarize them with a single value. But 'the center' can mean different things! **Drag the data points on the number line below** and watch how each metric responds live.")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("**Mean (The Balance Point)**\nThe mathematical average. Imagine the number line is a seesaw; the mean is where you'd place the fulcrum to balance it perfectly. It's highly sensitive to outliers. *Try dragging one point far to the right and watch the mean chase it!*")
   
with col2:
    st.info("**Median (The Middle Child)**\nThe exact middle value when you line up all the numbers in order. Half the numbers are bigger, half are smaller. It ignores extreme outliers. *Try dragging a point to the edge, and the median barely flinches.*")
   
with col3:
    st.info("**Mode (The Popular Vote)**\nThe most frequent value in the dataset. It's visually the highest stack of dots. There can be more than one mode, or no mode at all if every number is unique.")

html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
  body {
    margin: 0;
    padding: 0;
    background-color: transparent;
    color: white;
    font-family: 'Inter', system-ui, sans-serif;
    user-select: none;
    overflow: hidden;
  }
  #app {
    position: relative;
    width: 100%;
    height: 580px;
    background: linear-gradient(145deg, #111827, #1f2937);
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    display: flex;
    flex-direction: column;
    align-items: center;
    border: 1px solid rgba(255,255,255,0.1);
  }
  .dashboard {
    display: flex;
    gap: 30px;
    margin-top: 30px;
    z-index: 10;
  }
  .metric {
    background: rgba(255,255,255,0.03);
    padding: 15px 30px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
    min-width: 160px;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  }
  .metric .label {
    font-size: 14px;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 5px;
  }
  .metric .value {
    font-size: 36px;
    font-weight: 800;
  }
  #mean-val { color: #ef4444; } /* Red */
  #median-val { color: #06b6d4; } /* Cyan */
  #mode-val { color: #eab308; } /* Gold */
 
  .canvas-container {
    position: relative;
    flex-grow: 1;
    width: 100%;
    margin-top: 20px;
  }
  .axis {
    position: absolute;
    bottom: 100px;
    left: 8%;
    right: 8%;
    height: 4px;
    background: rgba(255,255,255,0.2);
    border-radius: 2px;
  }
  .tick {
    position: absolute;
    bottom: -30px;
    transform: translateX(-50%);
    color: #9ca3af;
    font-size: 14px;
    font-weight: 500;
  }
  .tick-mark {
    position: absolute;
    bottom: 0px;
    width: 2px;
    background: rgba(255,255,255,0.4);
    transform: translateX(-50%);
  }
 
  .point {
    position: absolute;
    width: 30px;
    height: 30px;
    background: radial-gradient(circle at 30% 30%, #a78bfa, #6366f1);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    cursor: grab;
    box-shadow: 0 4px 10px rgba(99, 102, 241, 0.4), inset 0 -3px 5px rgba(0,0,0,0.2);
    transition: left 0.4s cubic-bezier(0.2, 0.8, 0.2, 1), top 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
    z-index: 5;
    touch-action: none;
  }
  .point.dragging {
    transition: none;
    cursor: grabbing;
    transform: translate(-50%, -50%) scale(1.3);
    box-shadow: 0 15px 25px rgba(99, 102, 241, 0.6);
    z-index: 100;
  }
 
  .marker {
    position: absolute;
    transition: left 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
    transform: translateX(-50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    pointer-events: none;
  }
 
  /* Mean uses a triangle pointing UP, starting below the axis */
  #mean-marker {
    top: calc(100% - 100px); /* Top edge is exactly ON the axis */
    z-index: 2;
  }
  #mean-triangle {
    width: 0;
    height: 0;
    border-left: 14px solid transparent;
    border-right: 14px solid transparent;
    border-bottom: 24px solid #ef4444; /* Triangle points UP */
  }
  #mean-label {
    color: #ef4444;
    font-weight: bold;
    margin-top: 6px;
    background: rgba(239, 68, 68, 0.15);
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 14px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  }
 
  /* Median uses a vertical line going UP from the axis */
  #median-marker {
    bottom: 100px; /* Bottom edge is exactly ON the axis */
    height: 300px;
    border-left: 2px dashed #06b6d4;
    z-index: 1;
  }
  #median-label {
    position: absolute;
    top: -35px;
    background: rgba(6, 182, 212, 0.15);
    padding: 4px 10px;
    border-radius: 6px;
    color: #06b6d4;
    font-weight: bold;
    white-space: nowrap;
    font-size: 14px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  }
 
  .mode-highlight {
    position: absolute;
    bottom: 100px; /* Starts ON axis, grows UP */
    width: 38px;
    background: rgba(234, 179, 8, 0.15);
    border: 2px dashed rgba(234, 179, 8, 0.6);
    border-bottom: none;
    border-top-left-radius: 19px;
    border-top-right-radius: 19px;
    transform: translateX(-50%);
    transition: all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
    pointer-events: none;
    z-index: 0;
  }
 
  .array-display {
    position: absolute;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    font-family: 'Courier New', Courier, monospace;
    font-size: 16px;
    color: #d1d5db;
    background: rgba(0,0,0,0.4);
    padding: 10px 20px;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.05);
  }
</style>
</head>
<body>
<div id="app">
  <div class="dashboard">
    <div class="metric"><div class="label">Mean</div><div class="value" id="mean-val">0</div></div>
    <div class="metric"><div class="label">Median</div><div class="value" id="median-val">0</div></div>
    <div class="metric"><div class="label">Mode</div><div class="value" id="mode-val">0</div></div>
  </div>
 
  <div class="canvas-container" id="canvas">
    <div class="array-display" id="array-display">[0]</div>
    <div class="axis" id="axis"></div>
    <div class="marker" id="mean-marker">
      <div id="mean-triangle"></div>
      <div id="mean-label">Mean</div>
    </div>
    <div class="marker" id="median-marker">
      <div id="median-label">Median</div>
    </div>
  </div>
</div>

<script>
  const MIN_VAL = 0;
  const MAX_VAL = 20;
  const POINT_SPACING = 35; // Vertical spacing for stacked dots
 
  let dataPoints = [];
  // Strategic initial values to clearly separate Mean, Median, Mode
  let initialVals = [2, 3, 3, 4, 6, 8, 14, 18, 18, 18, 19];
 
  const canvas = document.getElementById('canvas');
  const axis = document.getElementById('axis');
  let modeHighlights = [];
 
  // 1. Create Ticks on Axis
  for (let i = MIN_VAL; i <= MAX_VAL; i++) {
    let pct = (i - MIN_VAL) / (MAX_VAL - MIN_VAL) * 100;
   
    if (i % 2 === 0) {
      let tick = document.createElement('div');
      tick.className = 'tick';
      tick.style.left = pct + '%';
      tick.innerText = i;
      axis.appendChild(tick);
    }
   
    let mark = document.createElement('div');
    mark.className = 'tick-mark';
    mark.style.left = pct + '%';
    mark.style.height = (i % 2 === 0) ? '12px' : '6px';
    axis.appendChild(mark);
  }
 
  // 2. Create Mode Highlights
  for (let i = 0; i < 5; i++) { // Support showing up to 5 modes
    let mhl = document.createElement('div');
    mhl.className = 'mode-highlight';
    mhl.style.opacity = 0;
    canvas.appendChild(mhl);
    modeHighlights.push(mhl);
  }
 
  // Helper Math
  function getXFromVal(val) {
    const axisRect = axis.getBoundingClientRect();
    const canvasRect = canvas.getBoundingClientRect();
    if (axisRect.width === 0) return 0; // Guard for uninitialized
    const width = axisRect.width;
    const leftOffset = axisRect.left - canvasRect.left;
    return leftOffset + ((val - MIN_VAL) / (MAX_VAL - MIN_VAL)) * width;
  }
 
  function getValFromX(x) {
    const axisRect = axis.getBoundingClientRect();
    const canvasRect = canvas.getBoundingClientRect();
    const width = axisRect.width;
    const leftOffset = axisRect.left - canvasRect.left;
    let val = MIN_VAL + ((x - leftOffset) / width) * (MAX_VAL - MIN_VAL);
    return Math.max(MIN_VAL, Math.min(MAX_VAL, Math.round(val)));
  }
 
  // 3. Initialize Points
  initialVals.forEach((val, index) => {
    let el = document.createElement('div');
    el.className = 'point';
    canvas.appendChild(el);
   
    let point = { el: el, val: val, id: index, isDragging: false };
    dataPoints.push(point);
   
    // Drag Events
    el.addEventListener('pointerdown', (e) => {
      e.preventDefault();
      point.isDragging = true;
      el.classList.add('dragging');
      el.setPointerCapture(e.pointerId);
      el.style.zIndex = 100;
    });
   
    el.addEventListener('pointermove', (e) => {
      if (!point.isDragging) return;
     
      const canvasRect = canvas.getBoundingClientRect();
      let x = e.clientX - canvasRect.left;
      let y = e.clientY - canvasRect.top;
     
      // Update visual DOM position instantly
      el.style.left = x + 'px';
      el.style.top = y + 'px';
     
      // Update underlying mathematical value and re-layout others
      let newVal = getValFromX(x);
      if (newVal !== point.val) {
        point.val = newVal;
        updateStatsAndLayout();
      }
    });
   
    el.addEventListener('pointerup', (e) => {
      point.isDragging = false;
      el.classList.remove('dragging');
      el.releasePointerCapture(e.pointerId);
      el.style.zIndex = 5;
      updateStatsAndLayout();
    });
  });
 
  // 4. Core Logic: Math & Layout
  function updateStatsAndLayout() {
    let vals = dataPoints.map(p => p.val);
    vals.sort((a,b) => a - b);
   
    // --- MATH ---
    // Mean
    let sum = vals.reduce((a,b) => a+b, 0);
    let mean = sum / vals.length;
   
    // Median
    let median;
    let mid = Math.floor(vals.length / 2);
    if (vals.length % 2 === 0) {
      median = (vals[mid-1] + vals[mid]) / 2;
    } else {
      median = vals[mid];
    }
   
    // Mode
    let counts = {};
    vals.forEach(v => counts[v] = (counts[v] || 0) + 1);
    let maxCount = 0;
    for (let v in counts) {
      if (counts[v] > maxCount) maxCount = counts[v];
    }
    let modes = [];
    for (let v in counts) {
      if (counts[v] === maxCount) modes.push(Number(v));
    }
   
    // --- UI UPDATES ---
    document.getElementById('mean-val').innerText = mean.toFixed(1);
    document.getElementById('median-val').innerText = median;
   
    if (maxCount <= 1) {
      document.getElementById('mode-val').innerText = "None";
      modes = []; // clear to hide highlights
    } else {
      document.getElementById('mode-val').innerText = modes.join(', ');
    }
   
    document.getElementById('array-display').innerText = `Dataset: [${vals.join(', ')}]`;
   
    // Move Markers
    document.getElementById('mean-marker').style.left = getXFromVal(mean) + 'px';
    document.getElementById('median-marker').style.left = getXFromVal(median) + 'px';
   
    // Update Mode Highlights
    modeHighlights.forEach(mhl => mhl.style.opacity = 0);
    modes.forEach((modeVal, i) => {
      if (i < modeHighlights.length) {
        let mhl = modeHighlights[i];
        mhl.style.left = getXFromVal(modeVal) + 'px';
        mhl.style.height = (maxCount * POINT_SPACING + 10) + 'px';
        mhl.style.opacity = 1;
      }
    });
   
    // Layout Points (Stacking)
    let currentCounts = {};
    for (let i = MIN_VAL; i <= MAX_VAL; i++) currentCounts[i] = 0;
   
    const canvasHeight = canvas.getBoundingClientRect().height;
   
    dataPoints.forEach(p => {
      let count = currentCounts[p.val]++;
      if (!p.isDragging) {
        p.el.style.left = getXFromVal(p.val) + 'px';
       
        // Stack mechanics: 100px from bottom is axis.
        // Dot radius is 15px. Each stack level adds POINT_SPACING.
        let bottomOffset = 100 + 15 + count * POINT_SPACING;
        let topPx = canvasHeight - bottomOffset;
        p.el.style.top = topPx + 'px';
      }
    });
  }
 
  // 5. Lifecycle
  const ro = new ResizeObserver(() => {
    const rect = canvas.getBoundingClientRect();
    if (rect.width > 0 && rect.height > 0) {
      updateStatsAndLayout();
    }
  });
  ro.observe(document.getElementById('app'));
</script>
</body>
</html>
"""

components.html(html_code, height=620)

