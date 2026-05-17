import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Pearson Correlation", layout="wide")

def render_correlation_lab():
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
        body { margin: 0; font-family: 'Inter', sans-serif; background: #0f172a; color: white; overflow: hidden; display: flex; justify-content: center; align-items: center; padding: 20px;}
        .container { display: flex; flex-direction: row; gap: 40px; width: 100%; max-width: 1100px; padding: 30px; background: rgba(255,255,255,0.03); border-radius: 24px; border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 20px 40px rgba(0,0,0,0.4); }
        
        .controls { flex: 1; display: flex; flex-direction: column; justify-content: center; gap: 25px; }
        .viz { flex: 1.2; display: flex; justify-content: center; align-items: center; position: relative;}
        canvas { background: #1e293b; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.05); }
        
        .title { font-size: 28px; font-weight: 900; color: #f8fafc; margin-bottom: 12px; }
        .desc { font-size: 15px; color: #94a3b8; line-height: 1.6; }
        
        .slider-group { background: rgba(0,0,0,0.2); padding: 25px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); }
        .slider-label { display: flex; justify-content: space-between; font-size: 18px; font-weight: 700; margin-bottom: 20px; }
        
        input[type="range"] { width: 100%; height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; outline: none; -webkit-appearance: none; }
        input[type="range"]::-webkit-slider-thumb { -webkit-appearance: none; width: 28px; height: 28px; border-radius: 50%; background: #4ECDC4; cursor: pointer; box-shadow: 0 0 15px #4ECDC4; transition: background 0.2s, box-shadow 0.2s; }
        
        .val-display { font-variant-numeric: tabular-nums; color: #4ECDC4; font-size: 24px; }
        
        .status-box { padding: 15px; border-radius: 10px; font-weight: 700; text-align: center; font-size: 16px; transition: all 0.3s; margin-top: 15px;}
        .status-pos { background: rgba(78, 205, 196, 0.15); color: #4ECDC4; border: 1px solid rgba(78, 205, 196, 0.3); }
        .status-neg { background: rgba(255, 107, 107, 0.15); color: #FF6B6B; border: 1px solid rgba(255, 107, 107, 0.3); }
        .status-zero { background: rgba(148, 163, 184, 0.15); color: #94a3b8; border: 1px solid rgba(148, 163, 184, 0.3); }
        
        .math-eq { font-family: monospace; font-size: 16px; color: #cbd5e1; text-align: center; margin-top: 10px; padding: 10px; background: rgba(0,0,0,0.3); border-radius: 8px; }
    </style>
    </head>
    <body>
        <div class="container">
            <div class="controls">
                <div>
                    <div class="title">The Correlation Morph 🧪</div>
                    <div class="desc">Move the slider to smoothly shift the relationship between X and Y. Notice how the shape squashes into a perfect straight line as the correlation approaches +1.0 or -1.0.</div>
                </div>
                
                <div class="slider-group">
                    <div class="slider-label">
                        <span>Pearson r</span>
                        <span id="r-val" class="val-display">0.00</span>
                    </div>
                    <input type="range" id="r-slider" min="-1" max="1" step="0.01" value="0">
                    <div id="status" class="status-box status-zero">Zero Correlation. A random cloud.</div>
                </div>
                
                <div class="math-eq" id="eq">y = 0.00x + 1.00 × noise</div>
            </div>
            
            <div class="viz">
                <canvas id="cvs" width="450" height="450"></canvas>
            </div>
        </div>
        
        <script>
            const cvs = document.getElementById('cvs');
            const ctx = cvs.getContext('2d');
            const slider = document.getElementById('r-slider');
            const valDisplay = document.getElementById('r-val');
            const statusBox = document.getElementById('status');
            const eqBox = document.getElementById('eq');
            
            // Generate synthetic normal data using Box-Muller transform
            function randn_bm() {
                let u = 0, v = 0;
                while(u === 0) u = Math.random();
                while(v === 0) v = Math.random();
                return Math.sqrt( -2.0 * Math.log( u ) ) * Math.cos( 2.0 * Math.PI * v );
            }
            
            const numPoints = 400;
            const points = [];
            for(let i=0; i<numPoints; i++) {
                points.push({ bx: randn_bm(), by: randn_bm() });
            }
            
            function lerpColor(c1, c2, t) {
                const r = Math.round(c1[0] + (c2[0] - c1[0]) * t);
                const g = Math.round(c1[1] + (c2[1] - c1[1]) * t);
                const b = Math.round(c1[2] + (c2[2] - c1[2]) * t);
                return `rgb(${r},${g},${b})`;
            }
            
            const C_POS = [78, 205, 196]; // #4ECDC4
            const C_NEG = [255, 107, 107]; // #FF6B6B
            const C_ZERO = [148, 163, 184]; // #94a3b8
            
            function draw() {
                const r = parseFloat(slider.value);
                valDisplay.innerText = r > 0 ? '+' + r.toFixed(2) : r.toFixed(2);
                
                // Update UI based on r
                let thumbColor = '';
                if (r > 0.8) {
                    statusBox.className = 'status-box status-pos'; statusBox.innerText = 'Strong Positive: They move together.'; thumbColor = '#4ECDC4';
                } else if (r > 0.3) {
                    statusBox.className = 'status-box status-pos'; statusBox.innerText = 'Weak Positive: Loose upward trend.'; thumbColor = '#4ECDC4';
                } else if (r < -0.8) {
                    statusBox.className = 'status-box status-neg'; statusBox.innerText = 'Strong Negative: They move opposite.'; thumbColor = '#FF6B6B';
                } else if (r < -0.3) {
                    statusBox.className = 'status-box status-neg'; statusBox.innerText = 'Weak Negative: Loose downward trend.'; thumbColor = '#FF6B6B';
                } else {
                    statusBox.className = 'status-box status-zero'; statusBox.innerText = 'Zero Correlation: Random noise.'; thumbColor = '#94a3b8';
                }
                
                valDisplay.style.color = thumbColor;
                document.documentElement.style.setProperty('--thumb-col', thumbColor);
                
                // Math EQ
                const weightX = r;
                const weightNoise = Math.sqrt(1 - r*r);
                eqBox.innerHTML = `y = <span style="color:${thumbColor}; font-weight:bold;">${weightX.toFixed(2)}x</span> + ${weightNoise.toFixed(2)} × noise`;
                
                // Clear Canvas
                ctx.clearRect(0, 0, cvs.width, cvs.height);
                
                // Draw axes
                const cx = cvs.width / 2;
                const cy = cvs.height / 2;
                const scale = 50; // pixels per unit
                
                ctx.strokeStyle = 'rgba(255,255,255,0.1)';
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(0, cy); ctx.lineTo(cvs.width, cy); // X axis
                ctx.moveTo(cx, 0); ctx.lineTo(cx, cvs.height); // Y axis
                ctx.stroke();
                
                // Grid lines
                ctx.strokeStyle = 'rgba(255,255,255,0.05)';
                ctx.beginPath();
                for(let i=-4; i<=4; i++) {
                    ctx.moveTo(0, cy + i*scale); ctx.lineTo(cvs.width, cy + i*scale);
                    ctx.moveTo(cx + i*scale, 0); ctx.lineTo(cx + i*scale, cvs.height);
                }
                ctx.stroke();
                
                // Draw points
                for(let i=0; i<numPoints; i++) {
                    const bx = points[i].bx;
                    const by = points[i].by;
                    
                    const x = bx;
                    const y = weightX * bx + weightNoise * by;
                    
                    const px = cx + x * scale;
                    const py = cy - y * scale;
                    
                    // Determine color based on quadrant contribution to correlation
                    let prod = x * y;
                    let intensity = Math.min(1, Math.abs(prod) / 3);
                    let color = C_ZERO;
                    if(prod > 0) color = lerpColor(C_ZERO, C_POS, intensity);
                    if(prod < 0) color = lerpColor(C_ZERO, C_NEG, intensity);
                    
                    ctx.beginPath();
                    ctx.arc(px, py, 4.5, 0, 2*Math.PI);
                    ctx.fillStyle = color;
                    ctx.fill();
                    ctx.lineWidth = 0.5;
                    ctx.strokeStyle = 'rgba(0,0,0,0.6)';
                    ctx.stroke();
                }
                
                // Draw trendline
                ctx.beginPath();
                ctx.moveTo(cx - 4*scale, cy - (-4*r)*scale);
                ctx.lineTo(cx + 4*scale, cy - (4*r)*scale);
                ctx.strokeStyle = '#FFD166';
                ctx.lineWidth = 3;
                ctx.setLineDash([8, 6]);
                ctx.stroke();
                ctx.setLineDash([]);
            }
            
            slider.addEventListener('input', draw);
            
            const style = document.createElement('style');
            style.innerHTML = `input[type="range"]::-webkit-slider-thumb { background: var(--thumb-col, #4ECDC4) !important; box-shadow: 0 0 15px var(--thumb-col, #4ECDC4) !important; }`;
            document.head.appendChild(style);
            
            draw();
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=580)


def render_anscombe_gotcha():
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
        body { margin: 0; font-family: 'Inter', sans-serif; background: transparent; color: white; overflow: hidden; display: flex; justify-content: center; align-items: center;}
        .container { display: flex; flex-direction: row; gap: 40px; background: rgba(30, 41, 59, 0.5); padding: 30px 40px; border-radius: 20px; border: 1px solid rgba(251, 113, 133, 0.3); align-items: center; max-width: 800px;}
        .text-box { flex: 1; display: flex; flex-direction: column; justify-content: center;}
        .title { color: #fb7185; font-weight: 900; font-size: 22px; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;}
        .desc { font-size: 15px; color: #cbd5e1; line-height: 1.6;}
        .highlight { color: white; font-weight: bold; background: rgba(251, 113, 133, 0.2); padding: 2px 6px; border-radius: 4px;}
        canvas { background: #0f172a; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 10px 20px rgba(0,0,0,0.3);}
    </style>
    </head>
    <body>
        <div class="container">
            <div class="text-box">
                <div class="title">⚠️ The "Linear" Blindspot</div>
                <div class="desc">
                    Pearson Correlation <strong>only measures straight lines</strong>.<br><br>
                    Look at the graph. X and Y are perfectly related (it's a beautiful U-shape curve). If you know X, you can predict Y exactly.<br><br>
                    But the Pearson Correlation is <span class="highlight">exactly 0.00</span>. It looks at the curve, tries to draw a straight line, fails, and gives up. Never trust <code>r</code> without looking at your data!
                </div>
            </div>
            <div>
                <canvas id="cvs" width="280" height="280"></canvas>
            </div>
        </div>
        <script>
            const cvs = document.getElementById('cvs');
            const ctx = cvs.getContext('2d');
            
            const numPoints = 120;
            const points = [];
            for(let i=0; i<numPoints; i++) {
                const x = (Math.random() - 0.5) * 5.5; // -2.75 to 2.75
                const y = 0.5 * x * x - 2 + (Math.random() - 0.5) * 0.5;
                points.push({x, y});
            }
            
            const cx = cvs.width / 2;
            const cy = cvs.height / 2;
            const scale = 30;
            
            // axes
            ctx.strokeStyle = 'rgba(255,255,255,0.1)';
            ctx.beginPath();
            ctx.moveTo(0, cy); ctx.lineTo(cvs.width, cy);
            ctx.moveTo(cx, 0); ctx.lineTo(cx, cvs.height);
            ctx.stroke();
            
            // points
            points.forEach(p => {
                ctx.beginPath();
                ctx.arc(cx + p.x * scale, cy - p.y * scale, 4.5, 0, 2*Math.PI);
                ctx.fillStyle = '#a78bfa';
                ctx.fill();
                ctx.strokeStyle = '#000';
                ctx.lineWidth = 1;
                ctx.stroke();
            });
            
            // horizontal line fit
            ctx.beginPath();
            ctx.moveTo(20, cy); ctx.lineTo(cvs.width-20, cy);
            ctx.strokeStyle = '#fb7185';
            ctx.lineWidth = 3;
            ctx.setLineDash([6, 6]);
            ctx.stroke();
            
            // text r=0
            ctx.fillStyle = '#fb7185';
            ctx.font = 'bold 26px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('r = 0.00', cx, cy + 35);
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=360)


def main():
    st.title("📏 Page 41: Pearson Correlation — Covariance, Normalized.")
    
    st.markdown(
        """
        On the last page, we saw that **Covariance** tells us if two variables move together. But there's a fatal flaw: 
        its value depends on the *units* of the data. Measure height in millimeters instead of meters, and the covariance skyrockets, 
        even though the relationship is exactly the same!
        
        **Pearson Correlation (r)** fixes this by squashing the relationship into a perfect, universal scale from **-1.0 to +1.0**.
        """
    )
    
    st.divider()

    st.markdown("### 1) The Correlation Morph")
    st.markdown("Drag the slider to shift the correlation. Watch how the data cloud transforms from pure randomness (0) into perfect mathematical harmony (+1 or -1).")
    
    render_correlation_lab()
    
    st.info(
        "**Visual Intuition:** As you move towards `1.0` or `-1.0`, the 'noise' vanishes. In AI, when features have a correlation of `1.0`, they are completely redundant—the neural network only needs one of them!"
    )
    
    st.divider()
    
    st.markdown("### 2) The Mathematical Squasher")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(
            """
            How does the math squeeze Covariance into a perfect box? It divides by the spread (Standard Deviation, $\\sigma$) of both variables.
            
            **The Formula:**
            $$ r = \\frac{\\text{Covariance}(X, Y)}{\\sigma_X \\sigma_Y} $$
            
            By dividing out the scale, we strip away the units. What is left is the pure, naked truth of how tightly they are bound together.
            """
        )
        
    with col2:
        st.markdown(
            """
            **The Scale:**
            * **$r = 1$**: Perfect positive line. (e.g. Temperature in C vs Temperature in F)
            * **$r > 0.5$**: Strong positive trend. (e.g. Height vs Weight)
            * **$r = 0$**: No linear relationship.
            * **$r < -0.5$**: Strong negative trend. (e.g. Study time vs Video game time)
            * **$r = -1$**: Perfect negative line.
            """
        )
        
    st.divider()
    
    st.markdown("### 3) The Gotcha: Correlation is not everything")
    st.markdown("It is tempting to think that `r = 0` means two variables are completely independent. But remember its full name: the **Pearson Linear Correlation Coefficient**.")
    
    render_anscombe_gotcha()
    
    st.divider()
    st.markdown(
        f"""
        <div style="color:#94a3b8; font-size:0.95rem;">
        Page 41 — you just learned how to measure the pure strength of a linear relationship. Up next: what happens when we try to draw the "best" line through these clouds of data? Welcome to Scatter Plots & Lines of Best Fit!
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
