import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Chain Rule", layout="wide")

def render_chain_rule_lab():
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body { margin: 0; font-family: sans-serif; background: #0f172a; color: white; overflow: hidden; display: flex; justify-content: center; align-items: center; padding: 20px;}
        .container { display: flex; flex-direction: row; gap: 30px; width: 100%; max-width: 1200px; padding: 30px; background: rgba(255,255,255,0.03); border-radius: 24px; border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 20px 40px rgba(0,0,0,0.4); }
        
        .controls { flex: 1; display: flex; flex-direction: column; justify-content: center; gap: 15px; }
        .viz { flex: 1.5; display: flex; flex-direction: column; gap: 12px; position: relative;}
        
        .canvas-wrapper { position: relative; width: 100%; border-radius: 12px; overflow: hidden; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
        .canvas-label { position: absolute; top: 8px; left: 12px; font-weight: 800; font-size: 14px; background: rgba(0,0,0,0.7); padding: 4px 8px; border-radius: 6px; backdrop-filter: blur(4px); }
        canvas { background: #1e293b; width: 100%; display: block; }
        
        .title { font-size: 28px; font-weight: 900; color: #f8fafc; margin-bottom: 5px; }
        .desc { font-size: 15px; color: #94a3b8; line-height: 1.5; }
        
        .func-selector { display: grid; grid-template-columns: 1fr; gap: 8px; margin-top: 5px; }
        .func-btn { background: rgba(255,255,255,0.05); color: #cbd5e1; border: 1px solid rgba(255,255,255,0.1); padding: 12px; border-radius: 10px; font-weight: 600; cursor: pointer; transition: 0.2s; text-align: left; font-size: 14px;}
        .func-btn:hover { background: rgba(255,255,255,0.1); }
        .func-btn.active { background: rgba(167, 139, 250, 0.2); border-color: #a78bfa; color: #a78bfa; box-shadow: 0 0 15px rgba(167, 139, 250, 0.3); }
        
        .slider-group { background: rgba(0,0,0,0.2); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); margin-top: 5px;}
        .slider-label { display: flex; justify-content: space-between; font-size: 14px; font-weight: 700; margin-bottom: 10px; color: #cbd5e1;}
        
        input[type="range"] { width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; outline: none; -webkit-appearance: none; margin-bottom: 15px;}
        input[type="range"]::-webkit-slider-thumb { -webkit-appearance: none; width: 22px; height: 22px; border-radius: 50%; cursor: pointer; transition: background 0.2s, box-shadow 0.2s; background: #FFD166; box-shadow: 0 0 10px #FFD166; }
        
        .val-display { font-variant-numeric: tabular-nums; font-size: 18px; font-weight: 900; }
        
        .auto-btn { background: rgba(78, 205, 196, 0.2); color: #4ECDC4; border: 1px solid rgba(78, 205, 196, 0.5); padding: 12px; border-radius: 8px; font-weight: 800; cursor: pointer; transition: 0.2s; width: 100%; text-transform: uppercase; letter-spacing: 1px; font-size: 13px;}
        .auto-btn:hover { background: rgba(78, 205, 196, 0.4); box-shadow: 0 0 15px rgba(78, 205, 196, 0.3);}
        
        .math-box { display: flex; flex-direction: column; gap: 8px; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); text-align: left; }
        .math-row { display: flex; justify-content: space-between; align-items: center; }
        .math-eq { font-family: monospace; font-size: 16px; font-weight: bold; }
        .math-val { font-family: monospace; font-size: 18px; font-weight: bold; background: rgba(0,0,0,0.5); padding: 4px 10px; border-radius: 6px; font-variant-numeric: tabular-nums;}
        
        .final-row { margin-top: 5px; padding-top: 15px; border-top: 1px dashed rgba(255,255,255,0.2); display: flex; justify-content: space-between; align-items: center;}
        .final-eq { font-family: monospace; font-size: 18px; font-weight: bold; color: #4ECDC4;}
        .final-val { font-family: monospace; font-size: 24px; font-weight: 900; color: #4ECDC4; background: rgba(78, 205, 196, 0.1); padding: 4px 12px; border-radius: 6px; border: 1px solid rgba(78, 205, 196, 0.3); font-variant-numeric: tabular-nums;}
    </style>
    </head>
    <body>
        <div class="container">
            <div class="controls">
                <div>
                    <div class="title">The Chain Explorer 🔗</div>
                    <div class="desc">Sweep <b>x</b> to see how its change cascades through the inner function <b>g(x)</b> and multiplies through the outer function <b>f(g)</b>.</div>
                </div>
                
                <div class="func-selector" id="func-btns">
                    <button class="func-btn active" data-type="power">Power: f(g) = 0.2g², g(x) = 0.5x² - 2</button>
                    <button class="func-btn" data-type="sin">Wave: f(g) = 3sin(g), g(x) = 2x</button>
                    <button class="func-btn" data-type="gauss">Gauss: f(g) = 4e^g, g(x) = -0.5x²</button>
                </div>
                
                <div class="slider-group">
                    <div class="slider-label">
                        <span>Input x</span>
                        <span id="x-val" class="val-display" style="color: #FFD166;">0.00</span>
                    </div>
                    <input type="range" id="x-slider" min="-4" max="4" step="0.05" value="1">
                    <button class="auto-btn" id="auto-btn">✨ Auto-Sweep</button>
                </div>
                
                <div class="math-box">
                    <div style="font-size: 12px; color: #a78bfa; font-weight: bold; text-transform: uppercase;">1. Inner Slope</div>
                    <div class="math-row">
                        <span class="math-eq" id="g-eq" style="color: #a78bfa;">g'(x) = x</span>
                        <span class="math-val" id="g-val" style="color: #a78bfa;">0.00</span>
                    </div>
                    
                    <div style="font-size: 12px; color: #FFD166; font-weight: bold; text-transform: uppercase; margin-top: 5px;">2. Outer Slope</div>
                    <div class="math-row">
                        <span class="math-eq" id="f-eq" style="color: #FFD166;">f'(g) = 0.4g</span>
                        <span class="math-val" id="f-val" style="color: #FFD166;">0.00</span>
                    </div>
                    
                    <div class="final-row">
                        <span class="final-eq">df/dx = f'(g) × g'(x)</span>
                        <span class="final-val" id="df-val">0.00</span>
                    </div>
                </div>
            </div>
            
            <div class="viz">
                <div class="canvas-wrapper">
                    <div class="canvas-label" style="color: #a78bfa;">Inner: g(x)</div>
                    <canvas id="cvs-g" width="600" height="180"></canvas>
                </div>
                <div class="canvas-wrapper">
                    <div class="canvas-label" style="color: #FFD166;">Outer: f(g) <span style="font-weight:normal; font-size:12px; color:#94a3b8; margin-left:10px;">(x-axis is g)</span></div>
                    <canvas id="cvs-f" width="600" height="180"></canvas>
                </div>
                <div class="canvas-wrapper">
                    <div class="canvas-label" style="color: #4ECDC4;">Composite: f(g(x))</div>
                    <canvas id="cvs-comp" width="600" height="180"></canvas>
                </div>
            </div>
        </div>
        
        <script>
            const cvsG = document.getElementById('cvs-g');
            const ctxG = cvsG.getContext('2d');
            const cvsF = document.getElementById('cvs-f');
            const ctxF = cvsF.getContext('2d');
            const cvsComp = document.getElementById('cvs-comp');
            const ctxComp = cvsComp.getContext('2d');
            
            const xSlider = document.getElementById('x-slider');
            const autoBtn = document.getElementById('auto-btn');
            const funcBtns = document.querySelectorAll('.func-btn');
            
            const xValDisp = document.getElementById('x-val');
            const gEqDisp = document.getElementById('g-eq');
            const gValDisp = document.getElementById('g-val');
            const fEqDisp = document.getElementById('f-eq');
            const fValDisp = document.getElementById('f-val');
            const dfValDisp = document.getElementById('df-val');
            
            const funcs = {
                'power': {
                    g: x => 0.5 * x * x - 2,
                    dg: x => x,
                    f: g => 0.2 * g * g,
                    df: g => 0.4 * g,
                    comp: x => 0.2 * Math.pow(0.5 * x * x - 2, 2),
                    str_dg: "g'(x) = x",
                    str_df: "f'(g) = 0.4g"
                },
                'sin': {
                    g: x => 2 * x,
                    dg: x => 2,
                    f: g => 3 * Math.sin(g),
                    df: g => 3 * Math.cos(g),
                    comp: x => 3 * Math.sin(2 * x),
                    str_dg: "g'(x) = 2",
                    str_df: "f'(g) = 3cos(g)"
                },
                'gauss': {
                    g: x => -0.5 * x * x,
                    dg: x => -x,
                    f: g => 4 * Math.exp(g),
                    df: g => 4 * Math.exp(g),
                    comp: x => 4 * Math.exp(-0.5 * x * x),
                    str_dg: "g'(x) = -x",
                    str_df: "f'(g) = 4e^g"
                }
            };
            
            let currentType = 'power';
            let autoInterval = null;
            let autoDirection = 1;
            
            const rangeX = 6;
            const rangeY = 5;
            const w = cvsG.width;
            const h = cvsG.height;
            const cx = w / 2;
            const cy = h / 2;
            const scaleX = w / (rangeX * 2);
            const scaleY = h / (rangeY * 2);
            
            function toScreen(x, y) {
                return { px: cx + x * scaleX, py: cy - y * scaleY };
            }
            
            funcBtns.forEach(btn => {
                btn.addEventListener('click', (e) => {
                    funcBtns.forEach(b => b.classList.remove('active'));
                    e.currentTarget.classList.add('active');
                    currentType = e.currentTarget.dataset.type;
                    updateEq();
                    draw();
                });
            });
            
            function updateEq() {
                const fn = funcs[currentType];
                gEqDisp.innerText = fn.str_dg;
                fEqDisp.innerText = fn.str_df;
            }
            
            xSlider.addEventListener('input', () => {
                stopAuto();
                draw();
            });
            
            function stopAuto() {
                if (autoInterval) {
                    clearInterval(autoInterval);
                    autoInterval = null;
                    autoBtn.innerText = "✨ Auto-Sweep";
                }
            }
            window.addEventListener('pagehide', stopAuto);
            
            autoBtn.addEventListener('click', () => {
                if (autoInterval) {
                    stopAuto();
                } else {
                    autoBtn.innerText = "⏸️ Pause Sweep";
                    xSlider.value = -4; 
                    autoInterval = setInterval(() => {
                        let x = parseFloat(xSlider.value);
                        x += 0.03 * autoDirection;
                        if (x > 4) { x = 4; autoDirection = -1; }
                        if (x < -4) { x = -4; autoDirection = 1; }
                        xSlider.value = x;
                        draw();
                    }, 20);
                }
            });
            
            function drawGrid(ctx) {
                ctx.clearRect(0, 0, w, h);
                ctx.strokeStyle = 'rgba(255,255,255,0.05)';
                ctx.lineWidth = 1;
                ctx.beginPath();
                for(let i = -10; i <= 10; i++) {
                    let p1 = toScreen(i, -10);
                    let p2 = toScreen(i, 10);
                    ctx.moveTo(p1.px, p1.py); ctx.lineTo(p2.px, p2.py);
                    p1 = toScreen(-10, i);
                    p2 = toScreen(10, i);
                    ctx.moveTo(p1.px, p1.py); ctx.lineTo(p2.px, p2.py);
                }
                ctx.stroke();
                
                ctx.strokeStyle = 'rgba(255,255,255,0.2)';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(0, cy); ctx.lineTo(w, cy); // X axis
                ctx.moveTo(cx, 0); ctx.lineTo(cx, h); // Y axis
                ctx.stroke();
            }
            
            function drawFunction(ctx, fn, color) {
                ctx.beginPath();
                for(let x = -rangeX; x <= rangeX; x += 0.05) {
                    let y = fn(x);
                    let p = toScreen(x, y);
                    if (x === -rangeX) ctx.moveTo(p.px, p.py);
                    else ctx.lineTo(p.px, p.py);
                }
                ctx.strokeStyle = color;
                ctx.lineWidth = 3;
                ctx.shadowColor = color;
                ctx.shadowBlur = 8;
                ctx.stroke();
                ctx.shadowBlur = 0;
            }
            
            function drawTangent(ctx, x, y, slope, color) {
                let lineExt = 1.5; 
                let p1 = toScreen(x - lineExt, y - slope * lineExt);
                let p2 = toScreen(x + lineExt, y + slope * lineExt);
                ctx.beginPath();
                ctx.moveTo(p1.px, p1.py);
                ctx.lineTo(p2.px, p2.py);
                ctx.strokeStyle = '#fff';
                ctx.lineWidth = 2;
                ctx.setLineDash([5, 5]);
                ctx.stroke();
                ctx.setLineDash([]);
                
                let pBase = toScreen(x, y);
                ctx.beginPath();
                ctx.arc(pBase.px, pBase.py, 6, 0, Math.PI * 2);
                ctx.fillStyle = color;
                ctx.fill();
                ctx.strokeStyle = '#fff';
                ctx.lineWidth = 2;
                ctx.stroke();
                
                // Draw slope value near point
                ctx.fillStyle = '#fff';
                ctx.font = "bold 13px monospace";
                ctx.fillText(`m=${slope.toFixed(2)}`, pBase.px + 12, pBase.py - 12);
            }
            
            function draw() {
                const x = parseFloat(xSlider.value);
                const fn = funcs[currentType];
                
                const g_val = fn.g(x);
                const dg_val = fn.dg(x);
                
                const f_val = fn.f(g_val);
                const df_val = fn.df(g_val);
                
                const comp_val = fn.comp(x);
                const dcomp_val = dg_val * df_val;
                
                // UI updates
                xValDisp.innerText = x.toFixed(2);
                gValDisp.innerText = dg_val.toFixed(2);
                fValDisp.innerText = df_val.toFixed(2);
                dfValDisp.innerText = dcomp_val.toFixed(2);
                
                // Canvas G
                drawGrid(ctxG);
                drawFunction(ctxG, fn.g, '#a78bfa');
                drawTangent(ctxG, x, g_val, dg_val, '#a78bfa');
                
                // Canvas F (Input is g_val)
                drawGrid(ctxF);
                drawFunction(ctxF, fn.f, '#FFD166');
                drawTangent(ctxF, g_val, f_val, df_val, '#FFD166');
                
                // Canvas Comp
                drawGrid(ctxComp);
                drawFunction(ctxComp, fn.comp, '#4ECDC4');
                drawTangent(ctxComp, x, comp_val, dcomp_val, '#4ECDC4');
            }
            
            updateEq();
            draw();
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=750)

def main():
    st.title("🧅 Page 46: Chain Rule — Derivative Through Layers")
    
    st.markdown(
        """
        You've mastered the **Power Rule** and **Constant Rule** for simple functions. But what happens when functions get nested inside each other, like Russian nesting dolls? 
        
        When we have a function inside another function—written as $f(g(x))$—we use the **Chain Rule**. 
        Think of it as peeling an onion: to see how a change in the deep center ($x$) affects the very outer layer ($f$), you have to multiply the rates of change as you peel outwards.
        """
    )
    
    st.divider()

    st.markdown("### 1) The Chain Explorer 🔗")
    st.markdown("Play with the simulator below. Trace how a small change travels through the inner function, then feeds into the outer function. Notice how the final derivative slope is exactly the **product of the two individual derivative slopes**.")
    
    render_chain_rule_lab()
    
    st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### The Formula")
        st.info("**Rule:** If $y = f(g(x))$, then $\\frac{dy}{dx} = f'(g(x)) \\cdot g'(x)$")
        st.markdown(
            """
            **The Intuition:**
            Imagine a factory with two machines. 
            * **Machine G** takes an input and stretches it by 3x.
            * **Machine F** takes an input and stretches it by 2x.
            
            If you feed an input through both machines, how much does it stretch?
            It stretches by $3 \\times 2 = 6x$. You simply **multiply the rates**.
            """
        )
        
    with col2:
        st.markdown("### Peeling the Onion")
        st.success("**Example:** $y = \\sin(x^2)$")
        st.markdown(
            """
            Let's break it down into layers:
            * **Inner Layer $g(x)$**: $x^2$. Its derivative is $2x$.
            * **Outer Layer $f(g)$**: $\\sin(g)$. Its derivative is $\\cos(g)$.
            
            **Multiply them together:**
            $y' = \\cos(g) \\cdot 2x$
            
            **Plug the inner layer back in:**
            $y' = \\cos(x^2) \\cdot 2x$
            """
        )
        
    st.divider()
    
    st.markdown("### 🤖 Bridge to AI: Why does this matter?")
    st.markdown(
        """
        The Chain Rule is arguably the **most important mathematical equation in Deep Learning**.
        
        A Neural Network is essentially a massive, nested function: 
        `Loss(Layer3(Layer2(Layer1(Weights))))`.
        
        To train the network, we need to know how tweaking a single Weight at the beginning affects the final Loss at the end. We do this using an algorithm called **Backpropagation**, which is literally just the Chain Rule applied hundreds of times backwards through the network. We calculate the local slope at each layer and multiply them all together!
        """
    )
    
    st.divider()
    st.markdown(
        f"""
        <div style="color:#94a3b8; font-size:0.95rem;">
        Page 46 — you now know how to differentiate through layers. Up next: Partial Derivatives—what happens when there are multiple inputs?
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
