import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np

st.set_page_config(page_title="Linear Functions: y = wx + b", layout="wide")

def render_threejs_interactive():
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body { margin: 0; overflow: hidden; font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #0f172a; color: white; }
        #canvas-container { width: 100%; height: 600px; position: relative; border-radius: 16px; overflow: hidden; border: 1px solid rgba(255,255,255,0.1); }
        #ui-layer {
            position: absolute; top: 20px; right: 20px; 
            background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(12px);
            padding: 24px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.15);
            width: 320px; box-shadow: 0 20px 40px rgba(0,0,0,0.5); z-index: 10;
        }
        .slider-group { margin-bottom: 20px; }
        .slider-group label { display: flex; justify-content: space-between; font-size: 14px; margin-bottom: 8px; font-weight: 700; color: #cbd5e1; text-transform: uppercase; letter-spacing: 0.5px; }
        input[type="range"] { 
            width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; outline: none; 
            -webkit-appearance: none;
        }
        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none; width: 18px; height: 18px; border-radius: 50%; cursor: pointer;
        }
        #w-slider::-webkit-slider-thumb { background: #fbbf24; box-shadow: 0 0 10px #fbbf24; }
        #b-slider::-webkit-slider-thumb { background: #f472b6; box-shadow: 0 0 10px #f472b6; }
        #x-slider::-webkit-slider-thumb { background: #4ade80; box-shadow: 0 0 10px #4ade80; }
        
        .val-display { font-variant-numeric: tabular-nums; font-weight: 900; }
        #w-val { color: #fbbf24; }
        #b-val { color: #f472b6; }
        #x-val { color: #4ade80; }
        
        #equation-display { 
            font-size: 22px; font-weight: 900; text-align: center; margin-top: 20px; 
            padding: 15px; background: rgba(0,0,0,0.3); border-radius: 8px;
            letter-spacing: 1px;
        }
        
        .instructions {
            position: absolute; bottom: 20px; left: 20px; pointer-events: none;
            background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(8px);
            padding: 12px 20px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);
            color: #94a3b8; font-size: 13px; font-weight: bold; display: flex; gap: 15px;
        }
        .instructions span { display: flex; align-items: center; gap: 6px; }
        .kbd { background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px; color: white; }

        /* Loading state */
        #loader {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            font-size: 18px; color: #38bdf8; font-weight: bold; pointer-events: none;
            transition: opacity 0.5s;
        }
    </style>
    <script src="https://unpkg.com/three@0.128.0/build/three.min.js" integrity="sha384-CI3ELBVUz9XQO+97x6nwMDPosPR5XvsxW2ua7N1Xeygeh1IxtgqtCkGfQY9WWdHu" crossorigin="anonymous"></script>
    <script src="https://unpkg.com/three@0.128.0/examples/js/controls/OrbitControls.js" integrity="sha384-wagZhIFgY4hD+7awjQjR4e2E294y6J2HSnd8eTNc15ZubTeQeVRZwhQJ+W6hnBsf" crossorigin="anonymous"></script>
    </head>
    <body>
    <div id="canvas-container">
        <div id="loader">Initializing 3D Math Engine...</div>
        <div class="instructions">
            <span><span class="kbd">Left Click</span> Rotate</span>
            <span><span class="kbd">Right Click</span> Pan</span>
            <span><span class="kbd">Scroll</span> Zoom</span>
        </div>
        <div id="ui-layer" style="opacity: 0; transition: opacity 0.5s;">
            <div class="slider-group">
                <label><span>w (Sensitivity / Slope)</span> <span id="w-val" class="val-display">1.0</span></label>
                <input type="range" id="w-slider" min="-3" max="3" step="0.1" value="1.0">
            </div>
            <div class="slider-group">
                <label><span>b (Shift / Bias)</span> <span id="b-val" class="val-display">2.0</span></label>
                <input type="range" id="b-slider" min="-5" max="5" step="0.1" value="2.0">
            </div>
            <div class="slider-group">
                <label><span>x (Input Probe)</span> <span id="x-val" class="val-display">1.0</span></label>
                <input type="range" id="x-slider" min="-8" max="8" step="0.1" value="1.0">
            </div>
            <div id="equation-display">y = (1.0)x + (2.0) = 3.0</div>
        </div>
    </div>
    
    <script>
        // Init Scene
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x0f172a, 0.02);
        
        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 100);
        camera.position.set(5, 8, 25);
        
        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        container.appendChild(renderer.domElement);
        
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.maxDistance = 50;
        controls.target.set(0, 0, 0);
        
        // Environment
        const grid = new THREE.GridHelper(40, 40, 0x334155, 0x1e293b);
        grid.position.y = -0.01; // slightly below to avoid Z-fighting with axes
        scene.add(grid);
        
        // Cartesian Axes
        const axisMat = new THREE.LineBasicMaterial({ color: 0x94a3b8, linewidth: 2 });
        const xAxisGeo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(-20, 0, 0), new THREE.Vector3(20, 0, 0)]);
        const yAxisGeo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0, -20, 0), new THREE.Vector3(0, 20, 0)]);
        scene.add(new THREE.Line(xAxisGeo, axisMat));
        scene.add(new THREE.Line(yAxisGeo, axisMat));
        
        // The Line y = wx + b
        const tubeMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.9 });
        let tubeMesh = new THREE.Mesh();
        scene.add(tubeMesh);

        // Glow effect for line
        const glowMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.2, side: THREE.BackSide });
        let glowMesh = new THREE.Mesh();
        scene.add(glowMesh);
        
        // Update function for line geometry
        function createLineGeom(w, b) {
            const startPt = new THREE.Vector3(-20, w * -20 + b, 0);
            const endPt = new THREE.Vector3(20, w * 20 + b, 0);
            const path = new THREE.LineCurve3(startPt, endPt);
            
            const geo = new THREE.TubeGeometry(path, 1, 0.15, 8, false);
            const glowGeo = new THREE.TubeGeometry(path, 1, 0.4, 8, false);
            return { geo, glowGeo };
        }

        // Bias indicator (Vertical dotted line)
        const biasMat = new THREE.LineDashedMaterial({ color: 0xf472b6, dashSize: 0.4, gapSize: 0.2, linewidth: 2 });
        const biasGeo = new THREE.BufferGeometry();
        const biasLine = new THREE.Line(biasGeo, biasMat);
        scene.add(biasLine);
        
        // Intercept Marker
        const interceptGeo = new THREE.SphereGeometry(0.3, 16, 16);
        const interceptMat = new THREE.MeshBasicMaterial({ color: 0xf472b6 });
        const interceptMesh = new THREE.Mesh(interceptGeo, interceptMat);
        scene.add(interceptMesh);

        // Probe Objects
        const probeGeo = new THREE.SphereGeometry(0.5, 32, 32);
        const probeMat = new THREE.MeshBasicMaterial({ color: 0x4ade80 });
        const probeMesh = new THREE.Mesh(probeGeo, probeMat);
        scene.add(probeMesh);
        
        // Probe glow
        const probeGlowMat = new THREE.MeshBasicMaterial({ color: 0x4ade80, transparent: true, opacity: 0.3 });
        const probeGlow = new THREE.Mesh(new THREE.SphereGeometry(0.9, 32, 32), probeGlowMat);
        probeMesh.add(probeGlow);

        const probeDropMat = new THREE.LineDashedMaterial({ color: 0x4ade80, dashSize: 0.3, gapSize: 0.15, linewidth: 2 });
        const probeDropGeo = new THREE.BufferGeometry();
        const probeDropLine = new THREE.Line(probeDropGeo, probeDropMat);
        scene.add(probeDropLine);

        // UI Logic
        const wSlider = document.getElementById('w-slider');
        const bSlider = document.getElementById('b-slider');
        const xSlider = document.getElementById('x-slider');
        const wVal = document.getElementById('w-val');
        const bVal = document.getElementById('b-val');
        const xVal = document.getElementById('x-val');
        const eqDisplay = document.getElementById('equation-display');

        function updateMath() {
            const w = parseFloat(wSlider.value);
            const b = parseFloat(bSlider.value);
            const x = parseFloat(xSlider.value);
            const y = w * x + b;
            
            // Update labels
            wVal.innerText = w.toFixed(1);
            bVal.innerText = b.toFixed(1);
            xVal.innerText = x.toFixed(1);
            
            // Equation formatting
            const signB = b >= 0 ? '+' : '-';
            const absB = Math.abs(b).toFixed(1);
            eqDisplay.innerHTML = `y = (<span style="color:#fbbf24">${w.toFixed(1)}</span>)·x ${signB} <span style="color:#f472b6">${absB}</span> = <span style="color:#4ade80">${y.toFixed(1)}</span>`;
            
            // Update 3D Line
            const geoms = createLineGeom(w, b);
            tubeMesh.geometry.dispose();
            glowMesh.geometry.dispose();
            tubeMesh.geometry = geoms.geo;
            glowMesh.geometry = geoms.glowGeo;
            
            // Update Bias
            biasGeo.setFromPoints([new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, b, 0)]);
            biasLine.computeLineDistances();
            interceptMesh.position.set(0, b, 0);
            
            // Update Probe
            probeMesh.position.set(x, y, 0);
            probeDropGeo.setFromPoints([new THREE.Vector3(x, 0, 0), new THREE.Vector3(x, y, 0)]);
            probeDropLine.computeLineDistances();
        }

        wSlider.addEventListener('input', updateMath);
        bSlider.addEventListener('input', updateMath);
        xSlider.addEventListener('input', updateMath);
        
        // Initial Draw
        updateMath();
        
        // Remove loader and show UI
        document.getElementById('loader').style.opacity = '0';
        document.getElementById('ui-layer').style.opacity = '1';

        // Animation Loop
        const clock = new THREE.Clock();
        function animate() {
            requestAnimationFrame(animate);
            controls.update();
            
            const time = clock.getElapsedTime();
            probeGlow.scale.setScalar(1 + 0.15 * Math.sin(time * 4));
            
            renderer.render(scene, camera);
        }
        animate();
        
        // Resize Handler
        window.addEventListener('resize', () => {
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        });
    </script>
    </body>
    </html>
    """
    components.html(html_code, height=620)

def render_neuron_cartoon():
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body { margin: 0; padding: 0; background: transparent; font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; display: flex; justify-content: center; align-items: center; }
        
        .machine-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #0f172a;
            padding: 40px;
            border-radius: 20px;
            width: 100%;
            max-width: 800px;
            border: 1px solid rgba(255,255,255,0.05);
            box-shadow: inset 0 0 40px rgba(0,0,0,0.5);
            position: relative;
            overflow: hidden;
        }

        /* Animated grid background */
        .machine-container::before {
            content: '';
            position: absolute; top: 0; left: 0; right: 0; bottom: 0;
            background-size: 30px 30px;
            background-image: linear-gradient(to right, rgba(255,255,255,0.02) 1px, transparent 1px),
                              linear-gradient(to bottom, rgba(255,255,255,0.02) 1px, transparent 1px);
            z-index: 0;
        }

        .element {
            z-index: 10;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
        }

        .orb {
            width: 80px; height: 80px;
            border-radius: 50%;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            font-weight: 900; font-size: 24px;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
            color: #0b1020;
        }
        
        .label {
            margin-top: 12px;
            font-size: 14px;
            font-weight: 700;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .orb-input { background: #38bdf8; box-shadow: 0 0 20px rgba(56, 189, 248, 0.4); }
        .orb-output { background: #4ade80; box-shadow: 0 0 20px rgba(74, 222, 128, 0.4); }

        .box {
            background: #1e293b;
            border: 3px solid;
            border-radius: 12px;
            padding: 20px 30px;
            color: white;
            text-align: center;
            min-width: 120px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.5);
        }

        .box-w { border-color: #fbbf24; }
        .box-b { border-color: #f472b6; }

        .box-title { font-size: 14px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; font-weight: bold; }
        .box-val { font-size: 24px; font-weight: 900; }
        .box-w .box-val { color: #fbbf24; }
        .box-b .box-val { color: #f472b6; }

        .path {
            flex-grow: 1;
            height: 4px;
            background: rgba(255,255,255,0.1);
            position: relative;
            margin: 0 20px;
            border-radius: 2px;
            z-index: 5;
        }

        .path::after {
            content: '';
            position: absolute;
            right: -2px; top: -6px;
            border-top: 8px solid transparent;
            border-bottom: 8px solid transparent;
            border-left: 12px solid rgba(255,255,255,0.2);
        }

        /* Flow Animation Particles */
        .particle {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            width: 12px; height: 12px;
            border-radius: 50%;
            background: white;
            box-shadow: 0 0 10px white;
            opacity: 0;
            animation: flow 3s infinite linear;
        }

        .p1 { animation-delay: 0s; background: #38bdf8; }
        .p2 { animation-delay: 1.5s; background: #fbbf24; }

        @keyframes flow {
            0% { left: 0%; opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { left: 100%; opacity: 0; }
        }

        .math-symbol {
            font-size: 32px;
            font-weight: 900;
            color: #64748b;
            margin: 0 15px;
            z-index: 10;
        }

    </style>
    </head>
    <body>
        <div class="machine-container">
            <!-- Input -->
            <div class="element">
                <div class="orb orb-input">x</div>
                <div class="label">Input</div>
            </div>

            <div class="path">
                <div class="particle p1"></div>
            </div>

            <!-- Weight -->
            <div class="element">
                <div class="box box-w">
                    <div class="box-title">Multiply</div>
                    <div class="box-val">× w</div>
                </div>
                <div class="label">Sensitivity</div>
            </div>

            <div class="math-symbol">+</div>

            <!-- Bias -->
            <div class="element">
                <div class="box box-b">
                    <div class="box-title">Add</div>
                    <div class="box-val">+ b</div>
                </div>
                <div class="label">Shift</div>
            </div>

            <div class="path">
                <div class="particle p2"></div>
            </div>

            <!-- Output -->
            <div class="element">
                <div class="orb orb-output">y</div>
                <div class="label">Output</div>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(html_code, height=260)

def main():
    st.title("📏 Page 20: Linear Functions — y = wx + b")
    st.markdown(
        """
        Meet the **affine map**: the world's politest function. It never bends — it only **tilts** and **slides**.

        - **w (weight)** is **sensitivity**: nudge **x** by a little, and **y** reacts **w times** as hard.
        - **b (bias)** is **shift**: the entire line rides up or down without changing its steepness.

        This affine rule is a building block for neural networks: each neuron combines weighted inputs and adds a bias. A layer applies this operation to many neurons at once, then may apply a non-linear activation.
        """
    )
    
    st.markdown("### 1) The 3D Math Engine")
    st.markdown("Interact directly with the sliders inside the 3D scene. Watch how the line morphs instantly in 60FPS. **Tip: Click and drag to rotate the 3D camera!**")
    
    # 3D Interactive Scene
    render_threejs_interactive()
    
    st.divider()

    st.markdown("### 2) The Anatomy of a Single Neuron")
    st.markdown("If you squint, **y = wx + b** is already a **one-weight neuron**. The story is: **input → multiply by a learned strength → add a baseline → output**.")
    
    # Animated Cartoon
    render_neuron_cartoon()
    
    st.divider()

    st.markdown("### 3) Number Lab: Table the Line")
    st.caption("Concrete rows make the 'sensitivity' idea feel less abstract.")
    
    # Keeping standard Streamlit sliders here for the dataframe interaction
    st.markdown("Use these sliders to build the table:")
    col1, col2 = st.columns(2)
    with col1:
        w_df = st.slider("w for table", -3.0, 3.0, 1.5, 0.1, key="df_w")
    with col2:
        b_df = st.slider("b for table", -5.0, 5.0, -1.0, 0.1, key="df_b")
        
    xs_show = np.round(np.linspace(-3, 3, 7), 2)
    rows = []
    for xv in xs_show:
        rows.append({"x": float(xv), "w · x": float(w_df * xv), "+ b": float(b_df), "y = w·x + b": float(w_df * xv + b_df)})
    
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.info(
        """
        ### Recap
        - **w** decides how **loud** the input speaks: **unit step in x ⇒ w-sized jump in y**.
        - **b** is a **universal offset**: same tilt, different altitude.
        - Psych trick for AI: **sensitivity = slope**, **shift = intercept**. 

        **Next up:** *Why non-linearity?* — the moment straight lines stop being enough to solve real problems.
        """
    )

if __name__ == "__main__":
    main()
