import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Piecewise Functions", layout="wide")

def render_stitch_lab():
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
        body { margin: 0; overflow: hidden; font-family: 'Inter', sans-serif; background: #0f172a; color: white; }
        #canvas-container { width: 100%; height: 750px; position: relative; border-radius: 16px; overflow: hidden; border: 1px solid rgba(255,255,255,0.1); }
        #ui-layer {
            position: absolute; top: 20px; right: 20px; bottom: 20px;
            background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(12px);
            padding: 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.15);
            width: 320px; box-shadow: 0 20px 40px rgba(0,0,0,0.5); z-index: 10;
            display: flex; flex-direction: column; overflow-y: auto;
        }
        
        /* Custom Scrollbar for UI */
        #ui-layer::-webkit-scrollbar { width: 6px; }
        #ui-layer::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 3px; }
        
        .section-title { font-size: 14px; font-weight: 900; color: #fff; text-transform: uppercase; letter-spacing: 1px; margin: 15px 0 10px 0; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 5px; }
        .section-title:first-child { margin-top: 0; }
        
        .slider-group { margin-bottom: 12px; }
        .slider-group label { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 4px; font-weight: 700; color: #cbd5e1; }
        input[type="range"] { 
            width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; outline: none; -webkit-appearance: none;
        }
        input[type="range"]::-webkit-slider-thumb { -webkit-appearance: none; width: 16px; height: 16px; border-radius: 50%; cursor: pointer; }
        
        /* Thumb colors */
        #a-slider::-webkit-slider-thumb, #b-slider::-webkit-slider-thumb { background: #fbbf24; box-shadow: 0 0 10px #fbbf24; }
        .lane-a::-webkit-slider-thumb { background: #38bdf8; box-shadow: 0 0 10px #38bdf8; }
        .lane-b::-webkit-slider-thumb { background: #f472b6; box-shadow: 0 0 10px #f472b6; }
        .lane-c::-webkit-slider-thumb { background: #a78bfa; box-shadow: 0 0 10px #a78bfa; }
        #x-slider::-webkit-slider-thumb { background: #4ade80; box-shadow: 0 0 10px #4ade80; }
        
        .val-display { font-variant-numeric: tabular-nums; font-weight: 900; }
        
        .info-box {
            background: rgba(0,0,0,0.3); border-radius: 8px; padding: 12px; margin-top: 15px;
            font-size: 13px; font-family: monospace; color: #94a3b8;
        }
        .info-box div { margin-bottom: 6px; display: flex; justify-content: space-between; }
        .info-box div:last-child { margin-bottom: 0; }
        
        .jump-val { font-weight: 900; }
        .jump-good { color: #4ade80; }
        .jump-bad { color: #fb7185; }

        .instructions {
            position: absolute; bottom: 20px; left: 20px; pointer-events: none;
            background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(8px);
            padding: 12px 20px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);
            color: #94a3b8; font-size: 13px; font-weight: bold; display: flex; gap: 15px;
        }
        .instructions span { display: flex; align-items: center; gap: 6px; }
        .kbd { background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px; color: white; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    </head>
    <body>
    <div id="canvas-container">
        <div class="instructions">
            <span><span class="kbd">Left Click</span> Rotate</span>
            <span><span class="kbd">Right Click</span> Pan</span>
            <span><span class="kbd">Scroll</span> Zoom</span>
        </div>
        <div id="ui-layer">
            <div class="section-title">Breakpoints (Gates)</div>
            <div class="slider-group">
                <label><span>Gate a</span> <span id="a-val" class="val-display" style="color:#fbbf24">-2.0</span></label>
                <input type="range" id="a-slider" min="-8" max="0" step="0.1" value="-2.0">
            </div>
            <div class="slider-group">
                <label><span>Gate b</span> <span id="b-val" class="val-display" style="color:#fbbf24">2.0</span></label>
                <input type="range" id="b-slider" min="0" max="8" step="0.1" value="2.0">
            </div>

            <div class="section-title" style="color:#38bdf8">Lane A (x < a)</div>
            <div class="slider-group">
                <label><span>m₁ (slope)</span> <span id="m1-val" class="val-display">0.5</span></label>
                <input type="range" id="m1-slider" class="lane-a" min="-3" max="3" step="0.1" value="0.5">
            </div>
            <div class="slider-group">
                <label><span>b₁ (intercept)</span> <span id="b1-val" class="val-display">2.0</span></label>
                <input type="range" id="b1-slider" class="lane-a" min="-5" max="5" step="0.1" value="2.0">
            </div>

            <div class="section-title" style="color:#f472b6">Lane B (a ≤ x < b)</div>
            <div class="slider-group">
                <label><span>m₂ (slope)</span> <span id="m2-val" class="val-display">-1.0</span></label>
                <input type="range" id="m2-slider" class="lane-b" min="-3" max="3" step="0.1" value="-1.0">
            </div>
            <div class="slider-group">
                <label><span>b₂ (intercept)</span> <span id="b2-val" class="val-display">-1.0</span></label>
                <input type="range" id="b2-slider" class="lane-b" min="-5" max="5" step="0.1" value="-1.0">
            </div>

            <div class="section-title" style="color:#a78bfa">Lane C (x ≥ b)</div>
            <div class="slider-group">
                <label><span>m₃ (slope)</span> <span id="m3-val" class="val-display">1.5</span></label>
                <input type="range" id="m3-slider" class="lane-c" min="-3" max="3" step="0.1" value="1.5">
            </div>
            <div class="slider-group">
                <label><span>b₃ (intercept)</span> <span id="b3-val" class="val-display">-6.0</span></label>
                <input type="range" id="b3-slider" class="lane-c" min="-5" max="5" step="0.1" value="-6.0">
            </div>

            <div class="section-title" style="color:#4ade80">Probe</div>
            <div class="slider-group">
                <label><span>x-probe</span> <span id="x-val" class="val-display">0.0</span></label>
                <input type="range" id="x-slider" min="-10" max="10" step="0.1" value="0.0">
            </div>
            
            <div class="info-box">
                <div><span>Jump at a:</span> <span id="jump-a" class="jump-val">0.00</span></div>
                <div><span>Jump at b:</span> <span id="jump-b" class="jump-val">0.00</span></div>
                <div style="margin-top: 10px; border-top: 1px solid #334155; padding-top: 5px;"><span>Output y:</span> <span id="y-val" class="jump-val" style="color:#4ade80">0.00</span></div>
            </div>
        </div>
    </div>
    
    <script>
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x0f172a, 0.02);
        
        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 100);
        camera.position.set(0, 5, 25);
        
        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        container.appendChild(renderer.domElement);
        
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.maxDistance = 50;
        
        // Environment
        const grid = new THREE.GridHelper(40, 40, 0x334155, 0x1e293b);
        grid.position.z = -0.1;
        grid.rotation.x = Math.PI / 2;
        scene.add(grid);
        
        // Axes
        const axisMat = new THREE.LineBasicMaterial({ color: 0x94a3b8, linewidth: 2 });
        const xAxis = new THREE.Line(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(-20, 0, 0), new THREE.Vector3(20, 0, 0)]), axisMat);
        const yAxis = new THREE.Line(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0, -20, 0), new THREE.Vector3(0, 20, 0)]), axisMat);
        scene.add(xAxis); scene.add(yAxis);
        
        // Create line segments
        function createLineMesh(color) {
            const mesh = new THREE.Mesh(new THREE.BufferGeometry(), new THREE.MeshBasicMaterial({ color: color, transparent: true, opacity: 0.9 }));
            const glow = new THREE.Mesh(new THREE.BufferGeometry(), new THREE.MeshBasicMaterial({ color: color, transparent: true, opacity: 0.2, side: THREE.BackSide }));
            scene.add(mesh); scene.add(glow);
            return { mesh, glow };
        }
        
        const laneA = createLineMesh(0x38bdf8);
        const laneB = createLineMesh(0xf472b6);
        const laneC = createLineMesh(0xa78bfa);
        
        // Gates (Vertical lines)
        const gateMat = new THREE.LineDashedMaterial({ color: 0xebbf24, dashSize: 0.5, gapSize: 0.3, linewidth: 2 });
        const gateA = new THREE.Line(new THREE.BufferGeometry(), gateMat);
        const gateB = new THREE.Line(new THREE.BufferGeometry(), gateMat);
        scene.add(gateA); scene.add(gateB);
        
        // Background Panels for lanes
        const panelGeo = new THREE.PlaneGeometry(1, 40);
        const panelA = new THREE.Mesh(panelGeo, new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.05, side: THREE.DoubleSide }));
        const panelB = new THREE.Mesh(panelGeo, new THREE.MeshBasicMaterial({ color: 0xf472b6, transparent: true, opacity: 0.05, side: THREE.DoubleSide }));
        const panelC = new THREE.Mesh(panelGeo, new THREE.MeshBasicMaterial({ color: 0xa78bfa, transparent: true, opacity: 0.05, side: THREE.DoubleSide }));
        panelA.position.z = -0.2; panelB.position.z = -0.2; panelC.position.z = -0.2;
        scene.add(panelA); scene.add(panelB); scene.add(panelC);

        // Probe
        const probeMesh = new THREE.Mesh(new THREE.SphereGeometry(0.4, 32, 32), new THREE.MeshBasicMaterial({ color: 0x4ade80 }));
        const probeGlow = new THREE.Mesh(new THREE.SphereGeometry(0.8, 32, 32), new THREE.MeshBasicMaterial({ color: 0x4ade80, transparent: true, opacity: 0.3 }));
        probeMesh.add(probeGlow);
        scene.add(probeMesh);
        
        const probeDropMat = new THREE.LineDashedMaterial({ color: 0x4ade80, dashSize: 0.3, gapSize: 0.15, linewidth: 2 });
        const probeDropLine = new THREE.Line(new THREE.BufferGeometry(), probeDropMat);
        scene.add(probeDropLine);

        // UI Logic
        const els = {
            a: document.getElementById('a-slider'), b: document.getElementById('b-slider'),
            m1: document.getElementById('m1-slider'), b1: document.getElementById('b1-slider'),
            m2: document.getElementById('m2-slider'), b2: document.getElementById('b2-slider'),
            m3: document.getElementById('m3-slider'), b3: document.getElementById('b3-slider'),
            x: document.getElementById('x-slider')
        };
        const vals = {
            a: document.getElementById('a-val'), b: document.getElementById('b-val'),
            m1: document.getElementById('m1-val'), b1: document.getElementById('b1-val'),
            m2: document.getElementById('m2-val'), b2: document.getElementById('b2-val'),
            m3: document.getElementById('m3-val'), b3: document.getElementById('b3-val'),
            x: document.getElementById('x-val')
        };
        const jumpA = document.getElementById('jump-a');
        const jumpB = document.getElementById('jump-b');
        const yVal = document.getElementById('y-val');

        function updateTubeGeometry(lineObj, startX, startY, endX, endY) {
            const path = new THREE.LineCurve3(new THREE.Vector3(startX, startY, 0), new THREE.Vector3(endX, endY, 0));
            if(lineObj.mesh.geometry) lineObj.mesh.geometry.dispose();
            if(lineObj.glow.geometry) lineObj.glow.geometry.dispose();
            lineObj.mesh.geometry = new THREE.TubeGeometry(path, 1, 0.15, 8, false);
            lineObj.glow.geometry = new THREE.TubeGeometry(path, 1, 0.4, 8, false);
        }

        function updateMath() {
            // Force a < b
            if (parseFloat(els.a.value) >= parseFloat(els.b.value)) {
                if (document.activeElement === els.a) els.b.value = (parseFloat(els.a.value) + 0.1).toFixed(1);
                else els.a.value = (parseFloat(els.b.value) - 0.1).toFixed(1);
            }
            
            const a = parseFloat(els.a.value); const b = parseFloat(els.b.value);
            const m1 = parseFloat(els.m1.value); const b1 = parseFloat(els.b1.value);
            const m2 = parseFloat(els.m2.value); const b2 = parseFloat(els.b2.value);
            const m3 = parseFloat(els.m3.value); const b3 = parseFloat(els.b3.value);
            const x = parseFloat(els.x.value);
            
            // Update UI text
            Object.keys(els).forEach(k => vals[k].innerText = parseFloat(els[k].value).toFixed(1));
            
            // Calc intersections and jumps
            const y1_a = m1 * a + b1; const y2_a = m2 * a + b2;
            const y2_b = m2 * b + b2; const y3_b = m3 * b + b3;
            
            const jA = Math.abs(y2_a - y1_a);
            const jB = Math.abs(y3_b - y2_b);
            
            jumpA.innerText = jA.toFixed(2);
            jumpA.className = 'jump-val ' + (jA < 0.05 ? 'jump-good' : 'jump-bad');
            jumpB.innerText = jB.toFixed(2);
            jumpB.className = 'jump-val ' + (jB < 0.05 ? 'jump-good' : 'jump-bad');
            
            // Update Geometries
            updateTubeGeometry(laneA, -20, m1 * -20 + b1, a, y1_a);
            updateTubeGeometry(laneB, a, y2_a, b, y2_b);
            updateTubeGeometry(laneC, b, y3_b, 20, m3 * 20 + b3);
            
            // Gates
            gateA.geometry.setFromPoints([new THREE.Vector3(a, -20, 0), new THREE.Vector3(a, 20, 0)]);
            gateB.geometry.setFromPoints([new THREE.Vector3(b, -20, 0), new THREE.Vector3(b, 20, 0)]);
            gateA.computeLineDistances(); gateB.computeLineDistances();
            
            // Panels
            panelA.scale.set(a - (-20), 1, 1); panelA.position.set(-20 + (a - (-20))/2, 0, -0.2);
            panelB.scale.set(b - a, 1, 1); panelB.position.set(a + (b - a)/2, 0, -0.2);
            panelC.scale.set(20 - b, 1, 1); panelC.position.set(b + (20 - b)/2, 0, -0.2);
            
            // Probe
            let y = 0; let activeColor = 0xffffff;
            laneA.mesh.material.opacity = 0.3; laneB.mesh.material.opacity = 0.3; laneC.mesh.material.opacity = 0.3;
            laneA.glow.visible = false; laneB.glow.visible = false; laneC.glow.visible = false;

            if (x < a) { 
                y = m1 * x + b1; activeColor = 0x38bdf8; 
                laneA.mesh.material.opacity = 1; laneA.glow.visible = true;
            }
            else if (x >= a && x < b) { 
                y = m2 * x + b2; activeColor = 0xf472b6; 
                laneB.mesh.material.opacity = 1; laneB.glow.visible = true;
            }
            else { 
                y = m3 * x + b3; activeColor = 0xa78bfa; 
                laneC.mesh.material.opacity = 1; laneC.glow.visible = true;
            }
            
            yVal.innerText = y.toFixed(2);
            probeMesh.position.set(x, y, 0);
            probeMesh.material.color.setHex(activeColor);
            probeGlow.material.color.setHex(activeColor);
            
            probeDropLine.geometry.setFromPoints([new THREE.Vector3(x, 0, 0), new THREE.Vector3(x, y, 0)]);
            probeDropLine.computeLineDistances();
            probeDropLine.material.color.setHex(activeColor);
        }

        Object.values(els).forEach(el => el.addEventListener('input', updateMath));
        updateMath();
        
        // Animation Loop
        const clock = new THREE.Clock();
        function animate() {
            requestAnimationFrame(animate);
            controls.update();
            const time = clock.getElapsedTime();
            probeGlow.scale.setScalar(1 + 0.15 * Math.sin(time * 6));
            renderer.render(scene, camera);
        }
        animate();
        
        window.addEventListener('resize', () => {
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        });
    </script>
    </body>
    </html>
    """
    components.html(html_code, height=770)

def render_relu_visualizer():
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
        body { margin: 0; padding: 0; background: transparent; font-family: 'Inter', sans-serif; display: flex; justify-content: center; align-items: center; color: white;}
        
        .container {
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            background: #0f172a; padding: 30px; border-radius: 20px; width: 100%; max-width: 900px;
            border: 1px solid rgba(255,255,255,0.05); box-shadow: inset 0 0 40px rgba(0,0,0,0.5);
        }

        .controls {
            display: flex; gap: 20px; margin-bottom: 30px; background: rgba(0,0,0,0.3); padding: 15px 25px; border-radius: 12px;
        }
        
        button {
            background: #1e293b; color: #cbd5e1; border: 1px solid #334155; padding: 8px 16px; border-radius: 6px;
            font-family: 'Inter', sans-serif; font-weight: bold; cursor: pointer; transition: all 0.2s;
        }
        button:hover { background: #334155; color: white; }
        button.active { background: #4ade80; color: #0f172a; border-color: #4ade80; }
        
        .viz-area {
            display: flex; width: 100%; align-items: center; justify-content: space-between; gap: 20px;
        }

        .graph {
            width: 300px; height: 300px; position: relative; border-left: 2px solid #64748b; border-bottom: 2px solid #64748b;
        }
        
        .line-segment {
            position: absolute; height: 4px; border-radius: 2px; transform-origin: left center;
        }
        
        .flow-path {
            flex-grow: 1; height: 100px; position: relative; display: flex; flex-direction: column; justify-content: center;
        }
        
        .pipe { height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; position: relative; overflow: hidden; margin: 20px 0; }
        .data-particle {
            position: absolute; top: 0; left: 0; height: 100%; width: 20px; border-radius: 4px;
            animation: flow 2s infinite linear;
        }
        
        @keyframes flow { 0% { left: -20px; opacity: 0; } 10% { opacity: 1; } 90% { opacity: 1; } 100% { left: 100%; opacity: 0; } }
        
        .relu-box {
            background: #1e293b; border: 2px solid #fbbf24; border-radius: 12px; padding: 20px; text-align: center;
            box-shadow: 0 0 20px rgba(251, 191, 36, 0.2); z-index: 2; position: relative;
        }
        .relu-box h3 { margin: 0 0 10px 0; color: #fbbf24; }
        .relu-box .formula { font-family: monospace; font-size: 18px; color: #cbd5e1; }
        
        .label { font-size: 12px; color: #94a3b8; font-weight: bold; text-transform: uppercase; margin-bottom: 5px;}
        
        #x-input { width: 100%; -webkit-appearance: none; background: rgba(255,255,255,0.1); height: 6px; border-radius: 3px; outline: none; margin-top: 15px;}
        #x-input::-webkit-slider-thumb { -webkit-appearance: none; width: 16px; height: 16px; border-radius: 50%; background: #38bdf8; cursor: pointer; }
        
        .val-display { font-size: 24px; font-weight: 900; font-variant-numeric: tabular-nums; }
        .in-val { color: #38bdf8; }
        .out-val { color: #4ade80; }
        
        .dead-val { color: #ef4444; text-decoration: line-through; }
        
        .explanation { margin-top: 25px; color: #94a3b8; font-size: 14px; text-align: center; max-width: 600px; line-height: 1.5; }
    </style>
    </head>
    <body>
        <div class="container">
            <div class="controls">
                <button id="btn-relu" class="active">ReLU</button>
                <button id="btn-leaky">Leaky ReLU</button>
                <button id="btn-abs">Absolute Value</button>
            </div>
            
            <div class="viz-area">
                <div style="width: 150px; text-align: center;">
                    <div class="label">Input (x)</div>
                    <div id="disp-in" class="val-display in-val">-2.5</div>
                    <input type="range" id="x-input" min="-5" max="5" step="0.1" value="-2.5">
                </div>
                
                <div class="flow-path">
                    <div class="pipe">
                        <div id="particle-in" class="data-particle" style="background: #38bdf8; animation-duration: 1.5s;"></div>
                    </div>
                </div>
                
                <div class="relu-box" id="activation-box">
                    <h3 id="box-title">ReLU</h3>
                    <div class="formula" id="box-formula">max(0, x)</div>
                </div>
                
                <div class="flow-path">
                    <div class="pipe" id="pipe-out">
                        <div id="particle-out" class="data-particle" style="background: #4ade80; animation-duration: 1.5s; animation-delay: 1.5s;"></div>
                    </div>
                </div>
                
                <div style="width: 150px; text-align: center;">
                    <div class="label">Output (y)</div>
                    <div id="disp-out" class="val-display out-val">0.0</div>
                </div>
            </div>
            
            <div class="explanation" id="exp-text">
                ReLU is the simplest piecewise function: a hinge at 0. If the input is negative, the signal is <strong>blocked (output 0)</strong>. If positive, it passes through perfectly unchanged. This cheap trick gives neural networks their superpower.
            </div>
        </div>
        
        <script>
            let mode = 'relu';
            const btnRelu = document.getElementById('btn-relu');
            const btnLeaky = document.getElementById('btn-leaky');
            const btnAbs = document.getElementById('btn-abs');
            const xInput = document.getElementById('x-input');
            const dispIn = document.getElementById('disp-in');
            const dispOut = document.getElementById('disp-out');
            const particleOut = document.getElementById('particle-out');
            const pipeOut = document.getElementById('pipe-out');
            const boxTitle = document.getElementById('box-title');
            const boxFormula = document.getElementById('box-formula');
            const expText = document.getElementById('exp-text');
            const actBox = document.getElementById('activation-box');
            
            function update() {
                const x = parseFloat(xInput.value);
                let y = 0;
                dispIn.innerText = x.toFixed(1);
                
                if(mode === 'relu') {
                    y = Math.max(0, x);
                    boxTitle.innerText = 'ReLU'; boxFormula.innerText = 'max(0, x)';
                    expText.innerHTML = 'ReLU is the simplest piecewise function: a hinge at 0. If the input is negative, the signal is <strong style="color:#ef4444">blocked (output 0)</strong>. If positive, it passes through perfectly unchanged. This cheap trick gives neural networks their superpower.';
                    actBox.style.borderColor = '#fbbf24'; boxTitle.style.color = '#fbbf24';
                } else if (mode === 'leaky') {
                    y = x < 0 ? 0.1 * x : x;
                    boxTitle.innerText = 'Leaky ReLU'; boxFormula.innerText = 'x < 0 ? 0.1x : x';
                    expText.innerHTML = 'Leaky ReLU lets a tiny fraction of the negative signal through. This prevents "dead neurons" that get stuck outputting 0 forever during training, while still providing the necessary non-linearity.';
                    actBox.style.borderColor = '#a78bfa'; boxTitle.style.color = '#a78bfa';
                } else {
                    y = Math.abs(x);
                    boxTitle.innerText = 'Absolute Value'; boxFormula.innerText = '|x|';
                    expText.innerHTML = 'The Absolute Value function reflects negative inputs. It is two lines (y=x and y=-x) stitched at 0. Piecewise doesn\\'t just mean "turning off", it means swapping rules!';
                    actBox.style.borderColor = '#f472b6'; boxTitle.style.color = '#f472b6';
                }
                
                dispOut.innerText = y.toFixed(1);
                
                // Animation Logic
                if (mode === 'relu' && x <= 0) {
                    dispOut.className = 'val-display dead-val';
                    particleOut.style.display = 'none';
                    pipeOut.style.opacity = '0.2';
                } else {
                    dispOut.className = 'val-display out-val';
                    particleOut.style.display = 'block';
                    pipeOut.style.opacity = '1';
                    
                    // Color code output based on if it was modified
                    if (y === x) { dispOut.style.color = '#38bdf8'; particleOut.style.background = '#38bdf8'; }
                    else { dispOut.style.color = '#4ade80'; particleOut.style.background = '#4ade80'; }
                }
            }
            
            function setMode(m) {
                mode = m;
                btnRelu.className = m === 'relu' ? 'active' : '';
                btnLeaky.className = m === 'leaky' ? 'active' : '';
                btnAbs.className = m === 'abs' ? 'active' : '';
                update();
            }
            
            btnRelu.addEventListener('click', () => setMode('relu'));
            btnLeaky.addEventListener('click', () => setMode('leaky'));
            btnAbs.addEventListener('click', () => setMode('abs'));
            xInput.addEventListener('input', update);
            
            update();
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=450)

def render_xor_piecewise_lab():
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
        body { margin: 0; font-family: 'Inter', sans-serif; background: #0f172a; color: white; overflow: hidden; }
        .container { display: flex; flex-direction: column; height: 100vh; padding: 20px; box-sizing: border-box; gap: 15px;}
        .vis-row { display: flex; gap: 20px; flex: 1; min-height: 0; justify-content: center; align-items: flex-start; }
        .panel { background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; padding: 15px; display: flex; flex-direction: column; align-items: center; width: 220px;}
        .final-panel { width: 320px; border-color: rgba(74, 222, 128, 0.3); background: rgba(74, 222, 128, 0.05); }
        .panel-title { font-size: 15px; font-weight: bold; margin-bottom: 10px; color: #e2e8f0; text-align: center; }
        canvas { background: #1e293b; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        .small-cvs { width: 150px; height: 150px; }
        .large-cvs { width: 250px; height: 250px; }
        .controls { display: flex; flex-direction: column; gap: 10px; width: 100%; margin-top: 15px; }
        .slider-group { display: flex; flex-direction: column; }
        .slider-group label { font-size: 12px; color: #cbd5e1; display: flex; justify-content: space-between; margin-bottom: 4px; font-variant-numeric: tabular-nums; font-weight: 600; }
        input[type=range] { -webkit-appearance: none; width: 100%; background: rgba(255,255,255,0.15); height: 6px; border-radius: 3px; outline: none; }
        input[type=range]::-webkit-slider-thumb { -webkit-appearance: none; width: 14px; height: 14px; border-radius: 50%; background: #38bdf8; cursor: pointer; }
        .final-panel input[type=range]::-webkit-slider-thumb { background: #4ade80; }
        .math-text { font-family: monospace; font-size: 13px; color: #94a3b8; margin-top: 10px; text-align: center; background: rgba(0,0,0,0.5); padding: 5px 10px; border-radius: 6px; width: 100%; box-sizing: border-box; }
        .legend { display: flex; gap: 20px; justify-content: center; font-size: 13px; font-weight: bold; margin-top: 5px;}
        .leg-item { display: flex; align-items: center; gap: 6px; }
        .dot { width: 12px; height: 12px; border-radius: 50%; }
        .btn-row { display: flex; gap: 15px; justify-content: center; margin-top: 10px; }
        button { background: #1e293b; color: white; border: 1px solid #4ade80; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 14px; transition: 0.2s; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }
        button:hover { background: #4ade80; color: #0f172a; transform: translateY(-1px); }
        .btn-fails { border-color: #fb7185; color: #fb7185; }
        .btn-fails:hover { background: #fb7185; color: white; }
    </style>
    </head>
    <body>
        <div class="container">
            <div class="vis-row">
                <!-- Panel 1 -->
                <div class="panel">
                    <div class="panel-title" style="color: #38bdf8;">Slice 1 (ReLU)</div>
                    <canvas id="c1" class="small-cvs" width="150" height="150"></canvas>
                    <div class="math-text" id="math1">h₁</div>
                    <div class="controls">
                        <div class="slider-group"><label><span>w₁₁ (x)</span> <span id="v-w11">1.0</span></label><input type="range" id="w11" min="-2" max="2" step="0.1" value="1"></div>
                        <div class="slider-group"><label><span>w₁₂ (y)</span> <span id="v-w12">1.0</span></label><input type="range" id="w12" min="-2" max="2" step="0.1" value="1"></div>
                        <div class="slider-group"><label><span>b₁ (bias)</span> <span id="v-b1">-0.5</span></label><input type="range" id="b1" min="-2" max="2" step="0.1" value="-0.5"></div>
                    </div>
                </div>
                
                <!-- Panel 2 -->
                <div class="panel">
                    <div class="panel-title" style="color: #f472b6;">Slice 2 (ReLU)</div>
                    <canvas id="c2" class="small-cvs" width="150" height="150"></canvas>
                    <div class="math-text" id="math2">h₂</div>
                    <div class="controls">
                        <div class="slider-group"><label><span>w₂₁ (x)</span> <span id="v-w21">1.0</span></label><input type="range" id="w21" min="-2" max="2" step="0.1" value="1"></div>
                        <div class="slider-group"><label><span>w₂₂ (y)</span> <span id="v-w22">1.0</span></label><input type="range" id="w22" min="-2" max="2" step="0.1" value="1"></div>
                        <div class="slider-group"><label><span>b₂ (bias)</span> <span id="v-b2">-1.5</span></label><input type="range" id="b2" min="-2" max="2" step="0.1" value="-1.5"></div>
                    </div>
                </div>
                
                <!-- Final Panel -->
                <div class="panel final-panel">
                    <div class="panel-title" style="color: #4ade80;">Final Piecewise Output</div>
                    <canvas id="c3" class="large-cvs" width="250" height="250"></canvas>
                    <div class="math-text" id="math3" style="color: #4ade80;">y</div>
                    <div class="controls">
                        <div class="slider-group"><label><span>v₁ (weight of Slice 1)</span> <span id="v-v1">1.0</span></label><input type="range" id="v1" min="-4" max="4" step="0.1" value="1"></div>
                        <div class="slider-group"><label><span>v₂ (weight of Slice 2)</span> <span id="v-v2">-3.0</span></label><input type="range" id="v2" min="-4" max="4" step="0.1" value="-3"></div>
                        <div class="slider-group"><label><span>c (final bias)</span> <span id="v-c">-0.1</span></label><input type="range" id="c" min="-2" max="2" step="0.1" value="-0.1"></div>
                    </div>
                </div>
            </div>
            
            <div class="legend">
                <div class="leg-item"><div class="dot" style="background: #38bdf8;"></div> Class + (Different)</div>
                <div class="leg-item"><div class="dot" style="background: #f472b6;"></div> Class − (Same)</div>
            </div>
            <div class="btn-row">
                <button id="btn-solve">🎯 Auto-Solve XOR</button>
                <button id="btn-linear" class="btn-fails">❌ Force Linear (Fails)</button>
            </div>
        </div>

        <script>
            const P1 = document.getElementById('c1').getContext('2d');
            const P2 = document.getElementById('c2').getContext('2d');
            const P3 = document.getElementById('c3').getContext('2d');
            
            const els = ['w11','w12','b1','w21','w22','b2','v1','v2','c'];
            const inputs = {};
            const vals = {};
            els.forEach(id => {
                inputs[id] = document.getElementById(id);
                vals[id] = document.getElementById('v-'+id);
                inputs[id].addEventListener('input', draw);
            });
            
            document.getElementById('btn-solve').addEventListener('click', () => {
                setVals({w11:1, w12:1, b1:-0.5, w21:1, w22:1, b2:-1.5, v1:1, v2:-3, c:-0.1});
            });
            
            document.getElementById('btn-linear').addEventListener('click', () => {
                setVals({w11:1, w12:1, b1:-0.5, w21:0, w22:0, b2:0, v1:1, v2:0, c:-0.5});
            });
            
            function setVals(obj) {
                for(let k in obj) {
                    inputs[k].value = obj[k];
                }
                draw();
            }

            const points = [
                [0, 0, -1], [1, 1, -1],
                [1, 0,  1], [0, 1,  1]
            ];

            const bgR = 30, bgG = 41, bgB = 59; // #1e293b
            const blR = 56, blG = 189, blB = 248; // #38bdf8
            const pkR = 244, pkG = 114, pkB = 182; // #f472b6
            const wtR = 255, wtG = 255, wtB = 255;
            
            const lerp = (a, b, t) => a + (b - a) * t;

            function drawHeatmap(ctx, width, height, isFinal, calcFunc) {
                const imgData = ctx.createImageData(width, height);
                const data = imgData.data;
                
                for(let py=0; py<height; py++) {
                    for(let px=0; px<width; px++) {
                        const x = (px / width) * 2.0 - 0.5;
                        const y = ((height - py) / height) * 2.0 - 0.5;
                        
                        const val = calcFunc(x, y);
                        
                        let r, g, b;
                        let t = Math.min(1, Math.abs(val));
                        
                        if(!isFinal) {
                            r = lerp(bgR, wtR, t);
                            g = lerp(bgG, wtG, t);
                            b = lerp(bgB, wtB, t);
                        } else {
                            if(val > 0) {
                                r = lerp(bgR, blR, t);
                                g = lerp(bgG, blG, t);
                                b = lerp(bgB, blB, t);
                            } else {
                                r = lerp(bgR, pkR, t);
                                g = lerp(bgG, pkG, t);
                                b = lerp(bgB, pkB, t);
                            }
                        }
                        
                        const idx = (py * width + px) * 4;
                        data[idx] = r; data[idx+1] = g; data[idx+2] = b; data[idx+3] = 255;
                    }
                }
                ctx.putImageData(imgData, 0, 0);

                // Draw points
                points.forEach(p => {
                    const px = (p[0] + 0.5) / 2.0 * width;
                    const py = height - (p[1] + 0.5) / 2.0 * height;
                    
                    ctx.beginPath();
                    ctx.arc(px, py, isFinal ? 6 : 5, 0, 2*Math.PI);
                    ctx.fillStyle = p[2] === 1 ? '#38bdf8' : '#f472b6';
                    ctx.fill();
                    ctx.lineWidth = 2;
                    ctx.strokeStyle = '#0f172a';
                    ctx.stroke();
                    
                    // White halo for visibility
                    ctx.beginPath();
                    ctx.arc(px, py, isFinal ? 7 : 6, 0, 2*Math.PI);
                    ctx.lineWidth = 1;
                    ctx.strokeStyle = 'rgba(255,255,255,0.3)';
                    ctx.stroke();
                });
            }

            function draw() {
                const w11 = parseFloat(inputs.w11.value);
                const w12 = parseFloat(inputs.w12.value);
                const b1 = parseFloat(inputs.b1.value);
                const w21 = parseFloat(inputs.w21.value);
                const w22 = parseFloat(inputs.w22.value);
                const b2 = parseFloat(inputs.b2.value);
                const v1 = parseFloat(inputs.v1.value);
                const v2 = parseFloat(inputs.v2.value);
                const c = parseFloat(inputs.c.value);

                els.forEach(id => { vals[id].innerText = parseFloat(inputs[id].value).toFixed(1); });
                
                document.getElementById('math1').innerText = `h₁ = max(0, ${w11.toFixed(1)}x + ${w12.toFixed(1)}y + ${b1.toFixed(1)})`;
                document.getElementById('math2').innerText = `h₂ = max(0, ${w21.toFixed(1)}x + ${w22.toFixed(1)}y + ${b2.toFixed(1)})`;
                document.getElementById('math3').innerText = `y = ${v1.toFixed(1)}h₁ ${v2 < 0 ? '-' : '+'} ${Math.abs(v2).toFixed(1)}h₂ ${c < 0 ? '-' : '+'} ${Math.abs(c).toFixed(1)}`;

                const calcH1 = (x, y) => Math.max(0, w11*x + w12*y + b1);
                const calcH2 = (x, y) => Math.max(0, w21*x + w22*y + b2);
                const calcY = (x, y) => v1 * calcH1(x, y) + v2 * calcH2(x, y) + c;

                drawHeatmap(P1, 150, 150, false, calcH1);
                drawHeatmap(P2, 150, 150, false, calcH2);
                drawHeatmap(P3, 250, 250, true, calcY);
            }
            
            draw();
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=680)

def main():
    st.title("🧩 Page 22: Piecewise Functions — Patchwork Lines")
    st.markdown(
        """
        Until now, one formula ruled the whole **x**-axis. **Piecewise** means: *different linear recipes on different strips*,
        then **sew** them together at **breakpoints** (the **gates** or **kinks**). Neural nets adore this trick.
        
        Deep Learning is built on piecewise functions. By combining millions of small linear pieces, a neural network can approximate any curve imaginable.
        """
    )

    st.markdown("### 1) The Stitch Lab")
    st.markdown("Imagine a highway with **three toll zones**. Same vehicle (**x**), but the **pricing rule** changes when you cross a gate. Drag the sliders inside the 3D lab to build a continuous curve from three separate lines. **Tip: Left click and drag to rotate the 3D view.**")
    
    render_stitch_lab()
    
    st.info(
        "**Continuity cheat-code:** The graph is continuous when the jump at a gate is exactly `0.00`. If you align all the pieces perfectly without any jumps, you've created a **CPWL (Continuous Piecewise Linear)** curve — the native language of modern deep neural networks."
    )
    
    st.divider()
    
    st.markdown("### 2) ReLU & The Star Lineup")
    st.markdown("**ReLU (Rectified Linear Unit)** is the celebrity of piecewise functions because it is incredibly cheap to compute, enforces sparsity, and is easy to reason about piece-by-piece.")
    
    render_relu_visualizer()
    
    st.success(
        "**Headline:** Piecewise functions are how we let a model stay **mostly linear locally** while acting **wildly non-linear globally** — ReLU is the simplest nontrivial stitch you can hide inside a giant net."
    )
    
    st.divider()
    
    st.markdown("### 3) Beating the Straight-Line Trap (Solving XOR)")
    st.markdown("On the last page, a single straight line failed to separate the XOR points. Here is how **piecewise functions** solve it. We combine two lines (Slice 1 and Slice 2, both using ReLU) to bend the decision boundary and perfectly trap the blue points in the middle!")
    
    render_xor_piecewise_lab()

    st.divider()
    st.markdown(
        f"""
        <div style="color:#94a3b8; font-size:0.95rem;">
        Page 22 — you can “sew” sophisticated behavior from humble lines. Next up in your curriculum: probability starts treating inputs as **random**
        instead of **deterministic** — new flavor, same love for structure.
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
