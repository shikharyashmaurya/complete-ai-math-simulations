import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Scatter Plot & Line of Best Fit", layout="wide")

def render_regression_lab():
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body { margin: 0; font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #0f172a; color: white; overflow: hidden; display: flex; justify-content: center; align-items: center; padding: 20px;}
        .container { display: flex; flex-direction: row; gap: 40px; width: 100%; max-width: 1200px; padding: 30px; background: rgba(255,255,255,0.03); border-radius: 24px; border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 20px 40px rgba(0,0,0,0.4); }
        
        .controls { flex: 1; display: flex; flex-direction: column; justify-content: center; gap: 20px; }
        .viz { flex: 1.5; display: flex; justify-content: center; align-items: center; position: relative;}
        canvas { background: #1e293b; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.05); cursor: crosshair; }
        
        .title { font-size: 28px; font-weight: 900; color: #f8fafc; margin-bottom: 8px; }
        .desc { font-size: 15px; color: #94a3b8; line-height: 1.6; }
        
        .stats-box { background: rgba(0,0,0,0.2); padding: 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); }
        .stat-row { display: flex; justify-content: space-between; margin-bottom: 12px; align-items: center;}
        .stat-row:last-child { margin-bottom: 0; }
        .stat-label { font-size: 16px; font-weight: 700; color: #cbd5e1; }
        .stat-val { font-variant-numeric: tabular-nums; font-size: 20px; font-weight: 900; }
        
        .eq-display { font-family: monospace; font-size: 20px; color: #FFD166; text-align: center; margin-top: 10px; padding: 15px; background: rgba(255, 209, 102, 0.1); border: 1px solid rgba(255, 209, 102, 0.3); border-radius: 8px; font-weight: bold;}
        
        .btn-group { display: flex; gap: 15px; margin-top: 10px; }
        button { flex: 1; padding: 12px; border-radius: 8px; border: none; font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; font-weight: 700; font-size: 14px; cursor: pointer; transition: all 0.2s; }
        .btn-clear { background: rgba(255, 107, 107, 0.2); color: #FF6B6B; border: 1px solid rgba(255, 107, 107, 0.4); }
        .btn-clear:hover { background: rgba(255, 107, 107, 0.3); }
        .btn-toggle { background: rgba(78, 205, 196, 0.2); color: #4ECDC4; border: 1px solid rgba(78, 205, 196, 0.4); }
        .btn-toggle:hover { background: rgba(78, 205, 196, 0.3); }
        .btn-toggle.active { background: #4ECDC4; color: #0f172a; }
        
        .instruction { font-size: 13px; color: #64748b; text-align: center; margin-top: 5px; font-style: italic; }
    </style>
    </head>
    <body>
        <div class="container">
            <div class="controls">
                <div>
                    <div class="title">The Chasing Line 🎯</div>
                    <div class="desc">Click on the canvas to drop data points. Watch how the "Line of Best Fit" instantly updates to minimize the total error (residuals) across all points.</div>
                </div>
                
                <div class="stats-box">
                    <div class="stat-row">
                        <span class="stat-label">Points (N)</span>
                        <span id="val-n" class="stat-val" style="color: #a78bfa;">0</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Slope (m)</span>
                        <span id="val-m" class="stat-val" style="color: #FFD166;">0.00</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Y-Intercept (b)</span>
                        <span id="val-b" class="stat-val" style="color: #FFD166;">0.00</span>
                    </div>
                    <div class="stat-row" style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1);">
                        <span class="stat-label">Total Error (MSE)</span>
                        <span id="val-mse" class="stat-val" style="color: #FF6B6B;">0.00</span>
                    </div>
                </div>
                
                <div class="eq-display" id="eq-box">y = 0.00x + 0.00</div>
                
                <div class="btn-group">
                    <button class="btn-toggle" id="btn-res">Show Errors (Residuals)</button>
                    <button class="btn-clear" id="btn-clear">Clear Points</button>
                </div>
                <div class="instruction">Click existing points to remove them. The latest 200 points are kept; adding another drops the oldest.</div>
            </div>
            
            <div class="viz">
                <canvas id="cvs" width="500" height="500"></canvas>
            </div>
        </div>
        
        <script>
            const cvs = document.getElementById('cvs');
            const ctx = cvs.getContext('2d');
            
            const btnClear = document.getElementById('btn-clear');
            const btnRes = document.getElementById('btn-res');
            
            const valN = document.getElementById('val-n');
            const valM = document.getElementById('val-m');
            const valB = document.getElementById('val-b');
            const valMSE = document.getElementById('val-mse');
            const eqBox = document.getElementById('eq-box');
            
            let points = [];
            const MAX_POINTS = 200;
            let showResiduals = false;
            
            // Coordinate System Configuration
            const range = 10; // -10 to 10
            const cx = cvs.width / 2;
            const cy = cvs.height / 2;
            const scale = cvs.width / (range * 2);
            
            function toScreen(x, y) {
                return { px: cx + x * scale, py: cy - y * scale };
            }
            function toData(px, py) {
                return { x: (px - cx) / scale, y: -(py - cy) / scale };
            }
            
            // Calculate OLS Regression
            function calculateRegression() {
                const n = points.length;
                if (n === 0) return { m: 0, b: 0, mse: 0 };
                if (n === 1) return { m: 0, b: points[0].y, mse: 0 };
                
                let sumX = 0, sumY = 0, sumXY = 0, sumXX = 0;
                for (let p of points) {
                    sumX += p.x;
                    sumY += p.y;
                    sumXY += p.x * p.y;
                    sumXX += p.x * p.x;
                }
                
                const meanX = sumX / n;
                const meanY = sumY / n;
                
                let num = 0;
                let den = 0;
                for(let p of points) {
                    num += (p.x - meanX) * (p.y - meanY);
                    den += (p.x - meanX) * (p.x - meanX);
                }
                
                const m = den === 0 ? 0 : num / den; // avoid div by zero if vertical line
                const b = meanY - m * meanX;
                
                // Calculate MSE
                let mse = 0;
                for(let p of points) {
                    const predY = m * p.x + b;
                    const error = p.y - predY;
                    mse += error * error;
                }
                mse /= n;
                
                return { m, b, mse };
            }
            
            function draw() {
                // Clear
                ctx.clearRect(0, 0, cvs.width, cvs.height);
                
                // Grid and Axes
                ctx.strokeStyle = 'rgba(255,255,255,0.05)';
                ctx.lineWidth = 1;
                ctx.beginPath();
                for(let i = -range; i <= range; i++) {
                    let p1 = toScreen(i, -range);
                    let p2 = toScreen(i, range);
                    ctx.moveTo(p1.px, p1.py); ctx.lineTo(p2.px, p2.py);
                    p1 = toScreen(-range, i);
                    p2 = toScreen(range, i);
                    ctx.moveTo(p1.px, p1.py); ctx.lineTo(p2.px, p2.py);
                }
                ctx.stroke();
                
                ctx.strokeStyle = 'rgba(255,255,255,0.2)';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(0, cy); ctx.lineTo(cvs.width, cy); // X axis
                ctx.moveTo(cx, 0); ctx.lineTo(cx, cvs.height); // Y axis
                ctx.stroke();
                
                const { m, b, mse } = calculateRegression();
                
                // Update UI Stats
                valN.innerText = points.length;
                if(points.length > 1) {
                    valM.innerText = m.toFixed(2);
                    valB.innerText = b > 0 ? "+" + b.toFixed(2) : b.toFixed(2);
                    valMSE.innerText = mse.toFixed(2);
                    eqBox.innerHTML = `y = <span style="color:white;">${m.toFixed(2)}x</span> ${b >= 0 ? '+' : '-'} <span style="color:white;">${Math.abs(b).toFixed(2)}</span>`;
                } else if (points.length === 1) {
                    valM.innerText = "0.00";
                    valB.innerText = b > 0 ? "+" + b.toFixed(2) : b.toFixed(2);
                    valMSE.innerText = "0.00";
                    eqBox.innerHTML = `y = <span style="color:white;">${b.toFixed(2)}</span>`;
                } else {
                    valM.innerText = "0.00";
                    valB.innerText = "0.00";
                    valMSE.innerText = "0.00";
                    eqBox.innerHTML = `y = 0.00x + 0.00`;
                }
                
                // Draw Residuals First (so they are under points and line)
                if (showResiduals && points.length > 0) {
                    ctx.beginPath();
                    for(let p of points) {
                        const predY = m * p.x + b;
                        const pScreen = toScreen(p.x, p.y);
                        const predScreen = toScreen(p.x, predY);
                        ctx.moveTo(pScreen.px, pScreen.py);
                        ctx.lineTo(predScreen.px, predScreen.py);
                    }
                    ctx.strokeStyle = '#FF6B6B';
                    ctx.lineWidth = 2;
                    ctx.setLineDash([5, 5]);
                    ctx.stroke();
                    ctx.setLineDash([]);
                }
                
                // Draw Line of Best Fit
                if (points.length > 0) {
                    const p1 = toScreen(-range, m * (-range) + b);
                    const p2 = toScreen(range, m * range + b);
                    
                    ctx.beginPath();
                    ctx.moveTo(p1.px, p1.py);
                    ctx.lineTo(p2.px, p2.py);
                    ctx.strokeStyle = '#FFD166';
                    ctx.lineWidth = 3;
                    // Glow effect
                    ctx.shadowColor = '#FFD166';
                    ctx.shadowBlur = 10;
                    ctx.stroke();
                    ctx.shadowBlur = 0; // reset
                }
                
                // Draw Points
                for(let p of points) {
                    const pScreen = toScreen(p.x, p.y);
                    ctx.beginPath();
                    ctx.arc(pScreen.px, pScreen.py, 6, 0, Math.PI * 2);
                    ctx.fillStyle = '#a78bfa';
                    ctx.fill();
                    ctx.strokeStyle = '#fff';
                    ctx.lineWidth = 1.5;
                    ctx.stroke();
                }
            }
            
            // Initial data for demo
            points.push({x: -4, y: -3});
            points.push({x: -2, y: -1});
            points.push({x: 1, y: 2});
            points.push({x: 3, y: 1});
            points.push({x: 5, y: 4});
            
            // Interaction
            cvs.addEventListener('mousedown', (e) => {
                const rect = cvs.getBoundingClientRect();
                const px = e.clientX - rect.left;
                const py = e.clientY - rect.top;
                const pData = toData(px, py);
                
                // Check if clicking existing point to remove
                let clickedExisting = false;
                for(let i=0; i<points.length; i++) {
                    const pScreen = toScreen(points[i].x, points[i].y);
                    const dist = Math.hypot(pScreen.px - px, pScreen.py - py);
                    if(dist < 10) { // 10px radius hit area
                        points.splice(i, 1);
                        clickedExisting = true;
                        break;
                    }
                }
                
                if(!clickedExisting) {
                    if(points.length >= MAX_POINTS) points.shift();
                    points.push(pData);
                }
                draw();
            });
            
            btnClear.addEventListener('click', () => {
                points = [];
                draw();
            });
            
            btnRes.addEventListener('click', () => {
                showResiduals = !showResiduals;
                if(showResiduals) {
                    btnRes.classList.add('active');
                    btnRes.innerText = "Hide Errors (Residuals)";
                } else {
                    btnRes.classList.remove('active');
                    btnRes.innerText = "Show Errors (Residuals)";
                }
                draw();
            });
            
            draw();
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=600)


def main():
    st.title("📈 Page 42: Scatter Plot & Line of Best Fit")
    
    st.markdown(
        """
        ### What is a Scatter Plot?
        A **Scatter Plot** is a simple but powerful graph that plots the values of two different variables along two axes, representing each piece of data as a single dot. 
        It allows us to instantly, visually see the relationship (or lack thereof) between two things—like *hours studied* versus *test scores*, or *square footage* versus *house price*.
        
        We know how to measure *if* two things are correlated in a scatter plot (Pearson $r$), but how do we actually **use** that relationship? 
        If we have a cloud of data points, how do we draw a line through them that best captures the trend?
        
        Welcome to **Linear Regression**. This is the first algorithm in our journey to AI. We are trying to build a tiny "model" 
        (a straight line) that summarizes the data.
        """
    )
    
    st.divider()

    st.markdown("### 1) The Interactive Scatter Plot Lab")
    st.markdown(
        "Drop some data points and watch the **Line of Best Fit** instantly recalculate to chase your points. "
        "Try making a straight line, a messy cloud, or putting an outlier far away."
    )
    
    render_regression_lab()
    
    st.info(
        "**Try This:** Turn on **'Show Errors'**. Notice those red vertical lines? Those are called **Residuals**. "
        "The line is trying its hardest to keep the total length of those red lines as small as possible."
    )
    
    st.divider()
    
    st.markdown("### 2) How does the Line know where to go?")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(
            """
            The line doesn't have a brain. It uses pure mathematics. 
            
            It evaluates itself using a **Loss Function**. In this case, it uses **Mean Squared Error (MSE)**. 
            For every point, it measures the vertical distance to the line (the error), squares that distance, and averages them.
            
            **The Goal:** Find the Slope ($m$) and Intercept ($b$) that give the absolute lowest possible MSE.
            """
        )
        
    with col2:
        st.markdown(
            """
            **Why Square the Errors?**
            1. **No cancelling out:** If we just added them, a +5 error above the line and a -5 error below the line would sum to 0. Squaring makes everything positive.
            2. **Punish big mistakes:** Squaring means an error of 1 is just 1, but an error of 5 becomes 25. The line gets heavily penalized for ignoring points completely!
            """
        )
        
    st.divider()
    
    st.markdown("### 3) Bridge to AI")
    st.markdown(
        """
        In Machine Learning, we call this **Training a Model**. 
        - The **Data Points** are our Training Data.
        - The **Line ($y = mx + b$)** is our Model.
        - The **Slope ($m$)** is our Weight.
        - The **Intercept ($b$)** is our Bias.
        
        When a Neural Network "learns", it is doing the exact same thing: adjusting its weights and biases to minimize its errors across the data!
        """
    )
    
    st.divider()
    
    st.markdown("### 4) The Danger of Outliers")
    st.markdown(
        """
        Because we use **Mean Squared Error (MSE)** to evaluate the line, *large* errors are squared and become *massive* penalties. 
        
        **Try it yourself in the lab above:** 
        1. Create a nice, tight diagonal line of data points.
        2. Drop a single point extremely far away in the opposite corner.
        
        Watch how the line violently swings to accommodate that one rogue point! This is why outliers are so dangerous in Machine Learning—models will often destroy a perfectly good trend just to avoid the massive MSE penalty of a single outlier.
        """
    )
    
    st.divider()
    st.markdown(
        f"""
        <div style="color:#94a3b8; font-size:0.95rem;">
        Page 42 & 43 — you just trained your first model and learned about the danger of outliers. Up next: stepping into the world of Calculus to measure change!
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
