import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Loss Landscape — Hills and Valleys", layout="wide")

def render_3d_landscape():
    html_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
        
        body { margin: 0; background-color: #0f172a; color: white; font-family: 'Outfit', sans-serif; overflow: hidden; }
        #container { width: 100vw; height: 100vh; position: relative; display: flex; justify-content: center; align-items: center; }
        canvas { cursor: move; border-radius: 16px; background: #0f172a; }
        
        .ui-overlay {
            position: absolute;
            top: 20px;
            left: 20px;
            z-index: 10;
            pointer-events: none;
        }
        
        .card {
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 20px;
            width: 280px;
            pointer-events: auto;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }
        
        h1 { margin: 0; font-size: 1.5rem; font-weight: 800; color: #f8fafc; }
        p { font-size: 0.85rem; color: #94a3b8; line-height: 1.4; margin: 8px 0 16px 0; }
        
        .control-group { margin-bottom: 12px; }
        .label-row { display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 0.8rem; font-weight: 600; }
        .val { color: #38bdf8; font-family: monospace; }
        
        input[type=range] {
            width: 100%;
            -webkit-appearance: none;
            background: rgba(255, 255, 255, 0.1);
            height: 4px;
            border-radius: 2px;
            outline: none;
        }
        
        input[type=range]::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 16px;
            height: 16px;
            background: #38bdf8;
            border-radius: 50%;
            cursor: pointer;
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
        }
        
        .legend {
            position: absolute;
            bottom: 20px;
            right: 20px;
            display: flex;
            flex-direction: column;
            gap: 6px;
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(12px);
            padding: 12px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            font-size: 0.7rem;
        }
        
        .legend-item { display: flex; align-items: center; gap: 8px; }
        .color-box { width: 10px; height: 10px; border-radius: 2px; }
        
        .btn-group { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
        .mode-btn {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #94a3b8;
            padding: 8px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.7rem;
            font-weight: 700;
            transition: all 0.2s;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .mode-btn.active {
            background: rgba(56, 189, 248, 0.2);
            border-color: #38bdf8;
            color: #38bdf8;
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.2);
        }
        
        .stats {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
        }
        
        .loss-display {
            font-size: 2rem;
            font-weight: 800;
            color: #38bdf8;
            text-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
            margin: 4px 0;
        }
        
        .loss-label {
            font-size: 0.65rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: #64748b;
        }

        .hint {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 0.75rem;
            color: #475569;
            pointer-events: none;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
    </style>
</head>
<body>
    <div id="container">
        <canvas id="canvas"></canvas>
        
        <div class="ui-overlay">
            <div class="card">
                <h1>Loss Explorer ⛰️</h1>
                <p>A "Mountain" represents error. Lower altitude = Better AI.</p>
                
                <div class="control-group">
                    <div class="label-row"><span>Topography</span></div>
                    <div class="btn-group">
                        <button class="mode-btn active" id="btn-convex">Convex</button>
                        <button class="mode-btn" id="btn-nonconvex">Complex</button>
                    </div>
                </div>
                
                <div class="control-group">
                    <div class="label-row"><span>Weight $w_1$</span><span class="val" id="w1-val">0.00</span></div>
                    <input type="range" id="w1-slider" min="-3" max="3" step="0.05" value="1.5">
                </div>
                
                <div class="control-group">
                    <div class="label-row"><span>Weight $w_2$</span><span class="val" id="w2-val">0.00</span></div>
                    <input type="range" id="w2-slider" min="-3" max="3" step="0.05" value="1.5">
                </div>
                
                <div class="stats">
                    <div class="loss-label">Current Altitude (Loss)</div>
                    <div class="loss-display" id="loss-val">0.00</div>
                </div>
            </div>
        </div>
        
        <div class="hint">Drag to Rotate | Scroll to Zoom</div>

        <div class="legend">
            <div class="legend-item"><div class="color-box" style="background: #ef4444;"></div> Peaks (High Loss)</div>
            <div class="legend-item"><div class="color-box" style="background: #eab308;"></div> Slopes</div>
            <div class="legend-item"><div class="color-box" style="background: #3b82f6;"></div> Valleys (Low Loss)</div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const w1Slider = document.getElementById('w1-slider');
        const w2Slider = document.getElementById('w2-slider');
        const w1Val = document.getElementById('w1-val');
        const w2Val = document.getElementById('w2-val');
        const lossVal = document.getElementById('loss-val');
        const btnConvex = document.getElementById('btn-convex');
        const btnNonConvex = document.getElementById('btn-nonconvex');

        let width, height;
        let rotationX = 0.6;
        let rotationZ = 0.7;
        let zoom = 60;
        let mode = 'convex';
        
        // Interaction state
        let isDragging = false;
        let lastMouseX, lastMouseY;

        function resize() {
            width = window.innerWidth;
            height = window.innerHeight;
            canvas.width = width * window.devicePixelRatio;
            canvas.height = height * window.devicePixelRatio;
            canvas.style.width = width + 'px';
            canvas.style.height = height + 'px';
            ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
        }

        window.addEventListener('resize', resize);
        resize();

        // Mathematical Surfaces
        function getLoss(x, z) {
            if (mode === 'convex') {
                return (x*x + z*z) * 0.3 - 1.5;
            } else {
                return (x*x + z*z) * 0.2 + 
                       (Math.sin(x * 3) * Math.cos(z * 3)) * 0.8 + 
                       (Math.cos(x * 1.5)) * 0.5 - 1.0;
            }
        }

        // Projection Engine
        function project(x, y, z) {
            // Rotate around Z axis
            let x1 = x * Math.cos(rotationZ) - z * Math.sin(rotationZ);
            let z1 = x * Math.sin(rotationZ) + z * Math.cos(rotationZ);
            
            // Rotate around X axis
            let y1 = y * Math.cos(rotationX) - z1 * Math.sin(rotationX);
            let z2 = y * Math.sin(rotationX) + z1 * Math.cos(rotationX);
            
            return {
                x: width / 2 + x1 * zoom,
                y: height / 2 - y1 * zoom,
                depth: z2
            };
        }

        function getColor(y) {
            // Map y range (approx -2 to 3) to 0-1
            const t = Math.max(0, Math.min(1, (y + 2) / 5));
            if (t < 0.3) {
                // Deep blue to light blue
                return `hsl(217, 91%, ${20 + t * 100}%)`;
            } else if (t < 0.7) {
                // Blue to yellow
                return `hsl(${217 - (t-0.3)*400}, 91%, 60%)`;
            } else {
                // Yellow to red
                return `hsl(${45 - (t-0.7)*150}, 91%, 50%)`;
            }
        }

        function draw() {
            ctx.clearRect(0, 0, width, height);
            
            const N = 40;
            const R = 3.5;
            const step = (2 * R) / N;
            
            const polygons = [];
            
            // Generate grid polygons
            for (let i = 0; i < N; i++) {
                for (let j = 0; j < N; j++) {
                    const x0 = -R + i * step;
                    const z0 = -R + j * step;
                    const x1 = x0 + step;
                    const z1 = z0 + step;
                    
                    const y00 = getLoss(x0, z0);
                    const y10 = getLoss(x1, z0);
                    const y01 = getLoss(x0, z1);
                    const y11 = getLoss(x1, z1);
                    
                    const p00 = project(x0, y00, z0);
                    const p10 = project(x1, y10, z0);
                    const p01 = project(x0, y01, z1);
                    const p11 = project(x1, y11, z1);
                    
                    const avgY = (y00 + y10 + y01 + y11) / 4;
                    const avgDepth = (p00.depth + p10.depth + p01.depth + p11.depth) / 4;
                    
                    polygons.push({
                        points: [p00, p10, p11, p01],
                        depth: avgDepth,
                        color: getColor(avgY),
                        y: avgY
                    });
                }
            }
            
            // Sort by depth (Painter's Algorithm)
            polygons.sort((a, b) => b.depth - a.depth);
            
            // Render Surface
            polygons.forEach(p => {
                ctx.beginPath();
                ctx.moveTo(p.points[0].x, p.points[0].y);
                ctx.lineTo(p.points[1].x, p.points[1].y);
                ctx.lineTo(p.points[2].x, p.points[2].y);
                ctx.lineTo(p.points[3].x, p.points[3].y);
                ctx.closePath();
                
                ctx.fillStyle = p.color;
                ctx.fill();
                
                // Subtle mesh lines
                ctx.strokeStyle = 'rgba(0,0,0,0.1)';
                ctx.lineWidth = 0.5;
                ctx.stroke();
            });

            // Draw current point (The Ball)
            const w1 = parseFloat(w1Slider.value);
            const w2 = parseFloat(w2Slider.value);
            const l = getLoss(w1, w2);
            const pb = project(w1, l, w2);
            
            // Ball shadow/glow on surface
            ctx.beginPath();
            ctx.ellipse(pb.x, pb.y + 2, 8, 4, 0, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(0,0,0,0.3)';
            ctx.fill();
            
            // The Ball
            const pulse = Math.sin(Date.now() * 0.005) * 2;
            ctx.beginPath();
            ctx.arc(pb.x, pb.y - 10 - pulse, 6, 0, Math.PI * 2);
            const grad = ctx.createRadialGradient(pb.x - 2, pb.y - 12 - pulse, 1, pb.x, pb.y - 10 - pulse, 6);
            grad.addColorStop(0, '#fff');
            grad.addColorStop(1, '#38bdf8');
            ctx.fillStyle = grad;
            ctx.shadowColor = '#38bdf8';
            ctx.shadowBlur = 15;
            ctx.fill();
            ctx.shadowBlur = 0;
            
            // Update UI
            w1Val.textContent = w1.toFixed(2);
            w2Val.textContent = w2.toFixed(2);
            lossVal.textContent = (l + 2).toFixed(2); // Offset to keep it positive for intuition
            
            requestAnimationFrame(draw);
        }

        // Event Listeners
        canvas.addEventListener('mousedown', e => {
            isDragging = true;
            lastMouseX = e.clientX;
            lastMouseY = e.clientY;
        });

        window.addEventListener('mousemove', e => {
            if (!isDragging) return;
            const dx = e.clientX - lastMouseX;
            const dy = e.clientY - lastMouseY;
            rotationZ += dx * 0.01;
            rotationX += dy * 0.01;
            rotationX = Math.max(0.1, Math.min(Math.PI / 2 - 0.1, rotationX));
            lastMouseX = e.clientX;
            lastMouseY = e.clientY;
        });

        window.addEventListener('mouseup', () => isDragging = false);
        
        canvas.addEventListener('wheel', e => {
            e.preventDefault();
            zoom -= e.deltaY * 0.05;
            zoom = Math.max(20, Math.min(150, zoom));
        }, { passive: false });

        btnConvex.addEventListener('click', () => {
            mode = 'convex';
            btnConvex.classList.add('active');
            btnNonConvex.classList.remove('active');
        });

        btnNonConvex.addEventListener('click', () => {
            mode = 'nonconvex';
            btnNonConvex.classList.add('active');
            btnConvex.classList.remove('active');
        });

        draw();
    </script>
</body>
</html>
"""
    components.html(html_code, height=700, scrolling=False)

def main():
    # Hero Section
    st.markdown("""
        <style>
            .main-header {
                font-family: 'Outfit', sans-serif;
                background: linear-gradient(90deg, #38bdf8, #818cf8);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 3rem;
                font-weight: 800;
                margin-bottom: 0;
            }
            .sub-header {
                font-size: 1.2rem;
                color: #94a3b8;
                margin-bottom: 2rem;
            }
            .info-card {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1rem;
            }
            .highlight {
                color: #38bdf8;
                font-weight: 700;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-header">Loss Landscape</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">The Topography of Intelligence</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5])

    with col1:
        st.markdown("""
        ### What is this?
        In AI, we don't just "calculate" the answer. We **search** for it.
        
        Imagine every possible setting of your AI's weights ($w_1, w_2$) as a coordinate on a map. For every coordinate, we calculate the **Loss** (error). 
        
        - **Peaks (Red)**: High error. The model is guessing wildly.
        - **Valleys (Blue)**: Low error. The model is getting closer to the truth.
        
        ### The Goal
        Training an AI is like being a hiker lost in a foggy mountain range at night. You can't see the bottom, but you can feel the **slope** under your feet.
        """)
        
        st.info("💡 **Try it:** Switch to 'Lumpy Terrain' to see why deep learning is hard! There are many 'fake' bottoms (local minima) that can trap your model.")

    with col2:
        render_3d_landscape()

    st.divider()

    # Educational Sections
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("### 🏹 The Global Minimum")
        st.markdown("""
        This is the "Holy Grail." It's the lowest possible point on the entire landscape. If your model reaches this point, it has found the best possible weights for the data.
        """)
        
    with c2:
        st.markdown("### 🕳️ Local Minima")
        st.markdown("""
        In complex models, the landscape is "lumpy." You might find a small valley that looks like the bottom, but there's a much deeper one elsewhere. Getting stuck here is a common AI problem.
        """)
        
    with c3:
        st.markdown("### 🎢 Curvature")
        st.markdown("""
        Some valleys are narrow (steep walls), others are broad. Steep walls mean small changes in weights cause huge changes in loss. Flat regions mean the AI might wander aimlessly.
        """)

    st.divider()

    # Bridge to AI
    st.markdown("### 🤖 Bridge to AI: From 3D to Million-D")
    
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.markdown("""
        In this visualization, we only have **2 Weights** ($w_1$ and $w_2$), so we can see it in 3D. 
        
        But a modern LLM (like GPT-4) has **hundreds of billions** of weights. The "landscape" exists in a billion-dimensional space!
        """)
        
    with col_b:
        st.warning("⚠️ **Reality Check**: We can't actually 'see' a billion-dimensional mountain. Instead, we use **Math (Gradients)** as our eyes to feel which way is 'down' in every direction simultaneously.")

    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #64748b; font-size: 0.8rem;">Page 51 — Understanding the terrain is the first step. Next: <b>Gradient Descent — Walking Downhill</b></div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
