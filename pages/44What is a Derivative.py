import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="What is a Derivative?", layout="wide")

def render_derivative_lab():
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
        body { margin: 0; font-family: 'Inter', sans-serif; background: #0f172a; color: white; overflow: hidden; display: flex; justify-content: center; align-items: center; padding: 20px;}
        .container { display: flex; flex-direction: row; gap: 40px; width: 100%; max-width: 1100px; padding: 30px; background: rgba(255,255,255,0.03); border-radius: 24px; border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 20px 40px rgba(0,0,0,0.4); }
        
        .controls { flex: 1; display: flex; flex-direction: column; justify-content: center; gap: 15px; }
        .viz { flex: 1.2; display: flex; justify-content: center; align-items: center; position: relative;}
        canvas { background: #1e293b; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.05); }
        
        .title { font-size: 28px; font-weight: 900; color: #f8fafc; margin-bottom: 8px; }
        .desc { font-size: 15px; color: #94a3b8; line-height: 1.6; }
        
        .slider-group { background: rgba(0,0,0,0.2); padding: 15px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); }
        .slider-label { display: flex; justify-content: space-between; font-size: 16px; font-weight: 700; margin-bottom: 10px; color: #cbd5e1;}
        
        input[type="range"] { width: 100%; height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; outline: none; -webkit-appearance: none; margin-bottom: 10px;}
        input[type="range"]::-webkit-slider-thumb { -webkit-appearance: none; width: 24px; height: 24px; border-radius: 50%; cursor: pointer; transition: background 0.2s, box-shadow 0.2s; }
        
        #x-slider::-webkit-slider-thumb { background: #a78bfa; box-shadow: 0 0 10px #a78bfa; }
        #h-slider::-webkit-slider-thumb { background: #FFD166; box-shadow: 0 0 10px #FFD166; }
        
        .val-display { font-variant-numeric: tabular-nums; font-size: 20px; font-weight: 900; }
        
        .stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 10px; }
        .stat-box { background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); text-align: center; }
        .stat-name { font-size: 13px; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
        .stat-value { font-size: 24px; font-weight: 900; font-variant-numeric: tabular-nums; }
        
        .status-box { padding: 15px; border-radius: 10px; font-weight: 700; text-align: center; font-size: 16px; transition: all 0.3s; margin-top: 5px;}
        .status-secant { background: rgba(255, 209, 102, 0.15); color: #FFD166; border: 1px solid rgba(255, 209, 102, 0.3); }
        .status-tangent { background: rgba(78, 205, 196, 0.2); color: #4ECDC4; border: 1px solid #4ECDC4; box-shadow: 0 0 20px rgba(78, 205, 196, 0.4); }
        
        .math-eq { font-family: monospace; font-size: 18px; color: #cbd5e1; text-align: center; margin-top: 10px; padding: 12px; background: rgba(0,0,0,0.3); border-radius: 8px; }
        .auto-btn { background: rgba(78, 205, 196, 0.2); color: #4ECDC4; border: 1px solid rgba(78, 205, 196, 0.5); padding: 10px; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.2s; width: 100%; margin-top: 15px;}
        .auto-btn:hover { background: rgba(78, 205, 196, 0.4); }
    </style>
    </head>
    <body>
        <div class="container">
            <div class="controls">
                <div>
                    <div class="title">The Shrinking Interval 🔬</div>
                    <div class="desc">A line needs two points. But what if we want the slope at exactly <strong>one</strong> point? Shrink the gap ($h$) to zero and watch the Secant line morph into the Tangent line.</div>
                </div>
                
                <div class="slider-group">
                    <div class="slider-label">
                        <span>Base Point (x)</span>
                        <span id="x-val" class="val-display" style="color: #a78bfa;">0.00</span>
                    </div>
                    <input type="range" id="x-slider" min="-6" max="6" step="0.1" value="2">
                    
                    <div class="slider-label" style="margin-top: 20px;">
                        <span>Interval Size (h)</span>
                        <span id="h-val" class="val-display" style="color: #FFD166;">3.00</span>
                    </div>
                    <input type="range" id="h-slider" min="0" max="6" step="0.01" value="3">
                    <button class="auto-btn" id="auto-btn">✨ Auto-Shrink to Zero</button>
                </div>
                
                <div id="status" class="status-box status-secant">Average Rate of Change (Secant)</div>
                
                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="stat-name">Rise (Δy)</div>
                        <div class="stat-value" id="dy-val" style="color: #fb7185;">0.00</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-name">Run (Δx)</div>
                        <div class="stat-value" id="dx-val" style="color: #38bdf8;">0.00</div>
                    </div>
                </div>
                
                <div class="math-eq" id="eq">Slope = Δy / Δx = <span style="color:#FFD166; font-weight:bold;" id="slope-val">0.00</span></div>
            </div>
            
            <div class="viz">
                <canvas id="cvs" width="480" height="480"></canvas>
            </div>
        </div>
        
        <script>
            const cvs = document.getElementById('cvs');
            const ctx = cvs.getContext('2d');
            
            const xSlider = document.getElementById('x-slider');
            const hSlider = document.getElementById('h-slider');
            const autoBtn = document.getElementById('auto-btn');
            
            const xValDisp = document.getElementById('x-val');
            const hValDisp = document.getElementById('h-val');
            const dyValDisp = document.getElementById('dy-val');
            const dxValDisp = document.getElementById('dx-val');
            const slopeValDisp = document.getElementById('slope-val');
            const statusBox = document.getElementById('status');
            const eqBox = document.getElementById('eq');
            
            // Function: f(x) = 0.2 * x^2 - 2
            function f(x) {
                return 0.2 * x * x - 2;
            }
            
            // Coordinate System Configuration
            const rangeX = 8; // -8 to 8
            const rangeY = 8; // -6 to 10
            const cx = cvs.width / 2;
            const cy = cvs.height / 2 + 50; // shift down slightly
            const scale = cvs.width / (rangeX * 2);
            
            function toScreen(x, y) {
                return { px: cx + x * scale, py: cy - y * scale };
            }
            
            let autoShrinkInterval = null;
            
            autoBtn.addEventListener('click', () => {
                if (autoShrinkInterval) {
                    clearInterval(autoShrinkInterval);
                    autoShrinkInterval = null;
                    autoBtn.innerText = "✨ Auto-Shrink to Zero";
                    return;
                }
                autoBtn.innerText = "⏸️ Pause Shrink";
                autoShrinkInterval = setInterval(() => {
                    let h = parseFloat(hSlider.value);
                    if (h <= 0.01) {
                        hSlider.value = 0;
                        clearInterval(autoShrinkInterval);
                        autoShrinkInterval = null;
                        autoBtn.innerText = "✨ Auto-Shrink to Zero";
                    } else {
                        // easing shrink
                        h -= Math.max(0.02, h * 0.05);
                        if(h < 0) h = 0;
                        hSlider.value = h;
                    }
                    draw();
                }, 30);
            });
            
            xSlider.addEventListener('input', draw);
            hSlider.addEventListener('input', draw);
            
            function draw() {
                let baseX = parseFloat(xSlider.value);
                let h = parseFloat(hSlider.value);
                
                const isTangent = h < 0.02;
                if(isTangent) h = 0.001; // Avoid division by zero, snap to tangent
                
                let targetX = baseX + h;
                
                let baseY = f(baseX);
                let targetY = f(targetX);
                
                let dy = targetY - baseY;
                let dx = targetX - baseX;
                let slope = dy / dx;
                
                // Update UI
                xValDisp.innerText = baseX.toFixed(2);
                hValDisp.innerText = isTangent ? "0.00" : h.toFixed(2);
                
                dyValDisp.innerText = isTangent ? "dy" : dy.toFixed(2);
                dxValDisp.innerText = isTangent ? "dx" : dx.toFixed(2);
                
                if (isTangent) {
                    slopeValDisp.innerText = slope.toFixed(2);
                    statusBox.className = 'status-box status-tangent';
                    statusBox.innerHTML = 'Instantaneous Rate of Change (Derivative)';
                    eqBox.innerHTML = `Slope = dy / dx = <span style="color:#4ECDC4; font-weight:bold;">${slope.toFixed(2)}</span>`;
                } else {
                    slopeValDisp.innerText = slope.toFixed(2);
                    statusBox.className = 'status-box status-secant';
                    statusBox.innerHTML = 'Average Rate of Change (Secant)';
                    eqBox.innerHTML = `Slope = Δy / Δx = <span style="color:#FFD166; font-weight:bold;">${slope.toFixed(2)}</span>`;
                }
                
                // Clear Canvas
                ctx.clearRect(0, 0, cvs.width, cvs.height);
                
                // Draw Grid
                ctx.strokeStyle = 'rgba(255,255,255,0.05)';
                ctx.lineWidth = 1;
                ctx.beginPath();
                for(let i = -10; i <= 10; i++) {
                    let p1 = toScreen(i, -10);
                    let p2 = toScreen(i, 15);
                    ctx.moveTo(p1.px, p1.py); ctx.lineTo(p2.px, p2.py);
                    p1 = toScreen(-10, i);
                    p2 = toScreen(10, i);
                    ctx.moveTo(p1.px, p1.py); ctx.lineTo(p2.px, p2.py);
                }
                ctx.stroke();
                
                // Draw Axes
                ctx.strokeStyle = 'rgba(255,255,255,0.2)';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(0, cy); ctx.lineTo(cvs.width, cy); // X axis
                ctx.moveTo(cx, 0); ctx.lineTo(cx, cvs.height); // Y axis
                ctx.stroke();
                
                // Draw Function Curve
                ctx.beginPath();
                for(let x = -rangeX; x <= rangeX; x += 0.1) {
                    let p = toScreen(x, f(x));
                    if (x === -rangeX) ctx.moveTo(p.px, p.py);
                    else ctx.lineTo(p.px, p.py);
                }
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)';
                ctx.lineWidth = 3;
                ctx.stroke();
                
                // Draw Secant / Tangent Line
                let lineExt = 15; // extend line in both directions
                let p1 = toScreen(baseX - lineExt, baseY - slope * lineExt);
                let p2 = toScreen(baseX + lineExt, baseY + slope * lineExt);
                
                ctx.beginPath();
                ctx.moveTo(p1.px, p1.py);
                ctx.lineTo(p2.px, p2.py);
                
                if (isTangent) {
                    ctx.strokeStyle = '#4ECDC4';
                    ctx.lineWidth = 3;
                    ctx.shadowColor = '#4ECDC4';
                    ctx.shadowBlur = 10;
                } else {
                    ctx.strokeStyle = '#FFD166';
                    ctx.lineWidth = 2;
                    ctx.shadowBlur = 0;
                }
                ctx.stroke();
                ctx.shadowBlur = 0; // reset
                
                // Draw Triangle for Rise and Run (only if not tangent)
                if (!isTangent) {
                    let pBase = toScreen(baseX, baseY);
                    let pTarget = toScreen(targetX, targetY);
                    let pCorner = toScreen(targetX, baseY);
                    
                    ctx.beginPath();
                    ctx.moveTo(pBase.px, pBase.py);
                    ctx.lineTo(pCorner.px, pCorner.py);
                    ctx.lineTo(pTarget.px, pTarget.py);
                    ctx.strokeStyle = 'rgba(255, 255, 255, 0.4)';
                    ctx.lineWidth = 2;
                    ctx.setLineDash([5, 5]);
                    ctx.stroke();
                    ctx.setLineDash([]);
                    
                    // Draw Points
                    ctx.beginPath();
                    ctx.arc(pTarget.px, pTarget.py, 6, 0, Math.PI * 2);
                    ctx.fillStyle = '#FFD166';
                    ctx.fill();
                    ctx.strokeStyle = '#000';
                    ctx.lineWidth = 1.5;
                    ctx.stroke();
                }
                
                // Draw Base Point
                let pBase = toScreen(baseX, baseY);
                ctx.beginPath();
                ctx.arc(pBase.px, pBase.py, isTangent ? 8 : 6, 0, Math.PI * 2);
                ctx.fillStyle = isTangent ? '#4ECDC4' : '#a78bfa';
                ctx.fill();
                ctx.strokeStyle = '#000';
                ctx.lineWidth = 1.5;
                ctx.stroke();
            }
            
            draw();
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=800)


def main():
    st.title("🎢 Page 44: What is a Derivative?")
    
    st.markdown(
        """
        Calculus sounds intimidating, but it is ultimately the mathematics of **Change**. 
        
        Imagine you are driving a car. Measuring your average speed over an hour is easy: `Distance / Time`. 
        But what if you wanted to know your *exact* speed at a single, frozen microscopic instant in time? 
        If no time passes (Time = 0), then no distance is traveled (Distance = 0). You get `0 / 0`, which breaks mathematics.
        
        This is the paradox that **the Derivative** solves.
        """
    )
    
    st.divider()

    st.markdown("### 1) The Shrinking Interval")
    st.markdown("To find the slope at exactly one point, we start with **two** points (a secant line) and slowly shrink the distance ($h$) between them to zero. The moment they merge, we have the true slope at a single point (a tangent line).")
    
    render_derivative_lab()
    
    st.info(
        "**Visual Intuition:** Notice how the `Δy` (Rise) and `Δx` (Run) both vanish as $h$ approaches 0. But their *ratio* (the slope) stabilizes into a perfect number. That perfectly stable number is the **Derivative**!"
    )
    
    st.divider()
    
    st.markdown("### 2) The Magic Formula")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(
            """
            Here is the formal definition of a derivative you see in textbooks. Don't be afraid, you just animated it above!
            
            **The Formula:**
            $$ f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h} $$
            
            Let's break it down:
            * $f(x+h) - f(x)$ is just the **Rise** (Δy).
            * $h$ is just the **Run** (Δx).
            * $\\lim_{h \\to 0}$ means "shrink $h$ until it's practically zero."
            """
        )
        
    with col2:
        st.markdown(
            """
            **What does the number mean?**
            * **Positive Slope (+)**: The curve is pointing uphill.
            * **Negative Slope (-)**: The curve is pointing downhill.
            * **Zero Slope (0)**: The curve is completely flat (you are at the bottom of a valley or top of a hill!).
            """
        )
        
    st.divider()
    
    st.markdown("### 3) Bridge to AI: Why do we care?")
    st.markdown(
        """
        In Machine Learning, we want to find the lowest possible error (Loss) for our model. Imagine you are blindfolded on a bumpy mountain (the Loss Landscape) and you want to walk to the bottom valley.
        
        How do you know which way to step? You feel the ground under your feet. If the ground slopes upwards in front of you, you take a step backward. 
        
        The **Derivative** tells the AI exactly how steep the ground is, and in what direction. Without derivatives, Neural Networks would have no idea how to "learn" from their mistakes!
        """
    )
    
    st.divider()
    st.markdown(
        f"""
        <div style="color:#94a3b8; font-size:0.95rem;">
        Page 44 — you just unlocked Calculus. Up next: what happens when we don't have to calculate the limit every single time? Welcome to Derivative Rules!
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
