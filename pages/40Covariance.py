import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Covariance", layout="wide", page_icon="📈")

st.title("📈 40. Covariance")
st.markdown("### How Do Two Variables Move Together?")
st.write("Covariance measures the **joint variability** of two variables. It tells us whether they tend to move in the same direction, opposite directions, or have zero linear co-variation. Zero covariance alone does not imply independence.")
st.markdown("#### The Formula")
st.markdown("**Population Covariance:**")
st.latex(r"\text{Cov}(X, Y) = \frac{1}{N} \sum_{i=1}^{N} (x_i - \mu_X)(y_i - \mu_Y)")

st.markdown("**Sample Covariance:**")
st.latex(r"\text{Cov}(X, Y) = \frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})")

st.markdown("#### Visualizing the Formula")
st.markdown("""
- **Green Zones (+):** When $X$ and $Y$ are both above average, or both below average, their product is positive. These points **increase** covariance.
- **Red Zones (-):** When one is above average and the other is below, their product is negative. These points **decrease** covariance.
""")
st.write("**Rotate the point cloud below** to see how changing the shape of the data impacts the balance between these zones, resulting in positive, negative, or zero covariance!")

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
    height: 600px;
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
    min-width: 220px;
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
  #cov-val { transition: color 0.3s; }
 
  .controls {
    margin-top: 20px;
    display: flex;
    align-items: center;
    gap: 15px;
    background: rgba(0,0,0,0.2);
    padding: 10px 25px;
    border-radius: 20px;
  }
  .controls label {
    font-size: 14px;
    color: #cbd5e1;
    font-weight: bold;
  }
  input[type=range] {
    width: 300px;
    accent-color: #3b82f6;
    cursor: pointer;
  }
 
  .canvas-container {
    position: relative;
    flex-grow: 1;
    width: 100%;
    margin-top: 15px;
    margin-bottom: 15px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  canvas {
    background: #0f172a;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
  }
</style>
</head>
<body>
<div id="app">
  <div class="dashboard">
    <div class="metric"><div class="label">Covariance (X, Y)</div><div class="value" id="cov-val">0.00</div></div>
    <div class="metric"><div class="label">Relationship</div><div class="value" id="rel-val" style="font-size:26px; padding-top:8px;">Zero</div></div>
  </div>
 
  <div class="controls">
    <label>Rotate Cloud:</label>
    <input type="range" id="angle-slider" min="0" max="180" value="45">
    <span id="angle-display" style="width: 45px; text-align:right; font-family:monospace; font-size:16px;">45°</span>
  </div>
 
  <div class="canvas-container">
    <canvas id="plot" width="600" height="380"></canvas>
  </div>
</div>

<script>
  const canvas = document.getElementById('plot');
  const ctx = canvas.getContext('2d');
  const slider = document.getElementById('angle-slider');
  const covValEl = document.getElementById('cov-val');
  const relValEl = document.getElementById('rel-val');
  const angleDispEl = document.getElementById('angle-display');
 
  const NUM_POINTS = 250;
  let basePoints = [];
 
  // Box-Muller transform for normal distribution
  function randn_bm() {
      let u = 0, v = 0;
      while(u === 0) u = Math.random();
      while(v === 0) v = Math.random();
      return Math.sqrt( -2.0 * Math.log( u ) ) * Math.cos( 2.0 * Math.PI * v );
  }

  // Create an elongated cloud horizontally (strong variance in X, small in Y)
  for (let i = 0; i < NUM_POINTS; i++) {
    let x = randn_bm() * 2.0;
    let y = randn_bm() * 0.4;
    basePoints.push({x, y});
  }

  function drawAndCalculate() {
    let angleDeg = parseInt(slider.value);
    angleDispEl.innerText = angleDeg + '°';
    let angleRad = angleDeg * Math.PI / 180;
   
    // Rotate points
    let points = basePoints.map(p => {
      return {
        x: p.x * Math.cos(angleRad) - p.y * Math.sin(angleRad),
        y: p.x * Math.sin(angleRad) + p.y * Math.cos(angleRad)
      };
    });
   
    // Mean is roughly 0 by generation, but let's be precise
    let sumX = 0, sumY = 0;
    points.forEach(p => { sumX += p.x; sumY += p.y; });
    let meanX = sumX / NUM_POINTS;
    let meanY = sumY / NUM_POINTS;
   
    // Calculate Covariance
    let cov = 0;
    points.forEach(p => {
      cov += (p.x - meanX) * (p.y - meanY);
    });
    cov = cov / (NUM_POINTS - 1);
   
    // UI Update
    let covStr = cov.toFixed(2);
    if (cov > 0) covStr = '+' + covStr;
    covValEl.innerText = covStr;
   
    if (cov > 0.5) {
      covValEl.style.color = '#10b981'; // Green
      relValEl.innerText = 'Positive';
      relValEl.style.color = '#10b981';
    } else if (cov < -0.5) {
      covValEl.style.color = '#ef4444'; // Red
      relValEl.innerText = 'Negative';
      relValEl.style.color = '#ef4444';
    } else {
      covValEl.style.color = '#9ca3af'; // Gray
      relValEl.innerText = 'Zero / None';
      relValEl.style.color = '#9ca3af';
    }
   
    // --- DRAWING ---
    ctx.clearRect(0, 0, canvas.width, canvas.height);
   
    let cx = canvas.width / 2;
    let cy = canvas.height / 2;
    let scale = 50; // Pixels per unit
   
    // Draw contribution quadrants relative to the sample means
    let meanCx = Math.max(0, Math.min(canvas.width, cx + meanX * scale));
    let meanCy = Math.max(0, Math.min(canvas.height, cy - meanY * scale));
    // Top-Right & Bottom-Left (Positive Contribution)
    ctx.fillStyle = 'rgba(16, 185, 129, 0.08)';
    ctx.fillRect(meanCx, 0, canvas.width - meanCx, meanCy); // TR
    ctx.fillRect(0, meanCy, meanCx, canvas.height - meanCy); // BL
   
    // Top-Left & Bottom-Right (Negative Contribution)
    ctx.fillStyle = 'rgba(239, 68, 68, 0.08)';
    ctx.fillRect(0, 0, meanCx, meanCy); // TL
    ctx.fillRect(meanCx, meanCy, canvas.width - meanCx, canvas.height - meanCy); // BR
   
    // Draw Axes
    ctx.beginPath();
    ctx.moveTo(0, cy);
    ctx.lineTo(canvas.width, cy);
    ctx.moveTo(cx, 0);
    ctx.lineTo(cx, canvas.height);
    ctx.strokeStyle = 'rgba(255,255,255,0.3)';
    ctx.lineWidth = 1;
    ctx.stroke();
   
    // Axis Labels
    ctx.fillStyle = 'rgba(255,255,255,0.6)';
    ctx.font = '14px Inter, sans-serif';
    ctx.fillText("X", canvas.width - 20, cy - 10);
    ctx.fillText("Y", cx + 10, 20);
   
    // Draw Points
    points.forEach(p => {
      let px = cx + p.x * scale;
      let py = cy - p.y * scale; // Invert Y for canvas
     
      // Covariance contributions depend on deviations from both sample means.
      let color = '';
      if (((p.x - meanX) > 0 && (p.y - meanY) > 0) ||
          ((p.x - meanX) < 0 && (p.y - meanY) < 0)) {
         color = 'rgba(16, 185, 129, 0.9)'; // Greenish for positive contribution
      } else {
         color = 'rgba(239, 68, 68, 0.9)'; // Reddish for negative contribution
      }
     
      // If covariance is close to zero, make them all purplish to show randomness
      if (Math.abs(cov) < 0.5) {
        // Transition to neutral color
        let mix = Math.abs(cov) / 0.5; // 0 to 1
        ctx.globalAlpha = 0.4 + 0.6 * mix;
      } else {
        ctx.globalAlpha = 1.0;
      }
     
      ctx.beginPath();
      ctx.arc(px, py, 4, 0, 2*Math.PI);
      ctx.fillStyle = color;
      ctx.fill();
     
      // Small stroke for clarity
      ctx.lineWidth = 0.5;
      ctx.strokeStyle = 'rgba(0,0,0,0.5)';
      ctx.stroke();
    });
    ctx.globalAlpha = 1.0;
   
    // Draw Trend Line
    let varX = 0;
    points.forEach(p => { varX += Math.pow(p.x - meanX, 2); });
    varX = varX / (NUM_POINTS - 1);
   
    if (Math.abs(cov) > 0.5) {
      let slope = cov / varX;
      let x1 = -5, x2 = 5;
      let y1 = meanY + slope * (x1 - meanX);
      let y2 = meanY + slope * (x2 - meanX);
     
      ctx.beginPath();
      ctx.moveTo(cx + x1 * scale, cy - y1 * scale);
      ctx.lineTo(cx + x2 * scale, cy - y2 * scale);
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)';
      ctx.lineWidth = 3;
      ctx.setLineDash([8, 8]);
      ctx.stroke();
      ctx.setLineDash([]);
    }
  }
 
  slider.addEventListener('input', drawAndCalculate);
  drawAndCalculate(); // Init

</script>
</body>
</html>
"""

components.html(html_code, height=650)
