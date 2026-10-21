import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Independence", page_icon="🎲", layout="wide")

st.title("🎲 Independence: The Tale of Two Spinners")
st.markdown("### When knowing one thing tells you *nothing* about the other.")

st.info("""
**The Setup:** Imagine we have two separate spinners.
- **Spinner A** decides the Weather.
- **Spinner B** decides the Outfit.

**The Question:** Does knowing the result of Spinner A help you predict Spinner B?
""")

html_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            font-family: system-ui, sans-serif;
            background: transparent;
            color: #E0E0E0;
        }
        
        .dashboard {
            display: flex;
            flex-direction: column;
            gap: 25px;
            padding: 10px;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .controls {
            display: flex;
            gap: 15px;
            align-items: center;
            justify-content: center;
            background: rgba(30, 30, 30, 0.8);
            padding: 20px;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            flex-wrap: wrap;
        }
        
        button {
            background: #333;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        button:hover { background: #444; transform: translateY(-2px); box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
        button:active { transform: translateY(0); }
        
        .btn-spin { background: linear-gradient(135deg, #3B82F6, #2563EB); }
        .btn-spin:hover { background: linear-gradient(135deg, #4F8DF9, #1D4ED8); }
        .btn-spin:disabled { background: #1E3A8A; color: #6B7280; cursor: not-allowed; transform: none; box-shadow: none; opacity: 0.7; }
        
        .btn-reset { background: linear-gradient(135deg, #4B5563, #374151); }
        .btn-reset:hover { background: linear-gradient(135deg, #6B7280, #4B5563); }
        
        .toggle-container {
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 700;
            font-size: 18px;
            background: rgba(0, 0, 0, 0.3);
            padding: 12px 24px;
            border-radius: 30px;
            border: 2px solid #555;
            cursor: pointer;
            user-select: none;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .toggle-container.dependent {
            border-color: #EF4444;
            background: rgba(239, 68, 68, 0.1);
            box-shadow: 0 0 15px rgba(239, 68, 68, 0.3);
        }
        
        .spinners-area {
            display: flex;
            justify-content: space-between;
            gap: 40px;
            padding: 10px 0;
            position: relative;
        }
        
        .spinner-box {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
            background: rgba(30, 30, 30, 0.8);
            padding: 30px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            flex: 1;
            position: relative;
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            z-index: 2;
        }
        
        .spinner-box h3 {
            margin: 0;
            font-size: 24px;
            color: #FFF;
            letter-spacing: 0.5px;
        }
        
        .spinner-wrapper {
            position: relative;
            width: 260px;
            height: 260px;
            filter: drop-shadow(0 15px 20px rgba(0,0,0,0.4));
        }
        
        .pointer {
            position: absolute;
            top: -15px;
            left: 50%;
            transform: translateX(-50%);
            width: 32px;
            height: 44px;
            background: linear-gradient(180deg, #FFFFFF, #E0E0E0);
            clip-path: polygon(50% 100%, 0 0, 100% 0);
            z-index: 10;
            filter: drop-shadow(0 4px 6px rgba(0,0,0,0.5));
        }
        
        .spinner {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
            /* Transition set in JS dynamically, but we keep a base here */
            transition: transform 3s cubic-bezier(0.25, 0.1, 0.25, 1);
        }
        
        svg {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            transform: rotate(-90deg);
            overflow: visible;
        }
        
        .wheel-overlay {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            border-radius: 50%;
            background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 40%, rgba(0,0,0,0.4) 100%);
            box-shadow: inset 0 0 10px rgba(255,255,255,0.2), inset 0 0 20px rgba(0,0,0,0.8);
            pointer-events: none;
            z-index: 5;
        }
        
        .center-pin {
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            width: 30px; height: 30px;
            border-radius: 50%;
            background: #222;
            border: 3px solid #555;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            z-index: 6;
        }
        
        .slice {
            transition: stroke-dasharray 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        }
        
        .outcome-label {
            font-size: 26px;
            font-weight: 800;
            min-height: 34px;
            color: #FFF;
            text-shadow: 0 2px 10px rgba(0,0,0,0.5);
            background: rgba(0,0,0,0.4);
            padding: 8px 25px;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.05);
        }
        
        .stats-area {
            display: flex;
            gap: 20px;
        }
        
        .stat-card {
            flex: 1;
            background: rgba(30, 30, 30, 0.8);
            padding: 25px;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
            backdrop-filter: blur(10px);
            transition: transform 0.2s;
        }
        
        .stat-value {
            font-size: 46px;
            font-weight: 800;
            color: #FFF;
            margin: 15px 0 5px 0;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
            font-variant-numeric: tabular-nums;
        }
        .stat-title {
            font-size: 15px;
            color: #BBB;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 600;
        }
        
        .log-container {
            height: 120px;
            overflow-y: auto;
            background: rgba(15, 15, 15, 0.8);
            padding: 15px 20px;
            border-radius: 12px;
            border: 1px solid #333;
            font-family: 'Courier New', monospace;
            font-size: 15px;
            color: #A0A0A0;
            box-shadow: inset 0 2px 10px rgba(0,0,0,0.3);
        }
        .log-entry { margin-bottom: 6px; border-bottom: 1px dashed #333; padding-bottom: 6px;}
        .log-entry:last-child { border-bottom: none; }
        
        .highlight-sun { color: #FBBF24; font-weight: bold; }
        .highlight-rain { color: #60A5FA; font-weight: bold; }
        .highlight-tshirt { color: #F97316; font-weight: bold; }
        .highlight-coat { color: #C084FC; font-weight: bold; }
        
        .dependency-line {
            position: absolute;
            top: 50%;
            left: 100%;
            width: 40px;
            height: 8px;
            background: #333;
            z-index: 1;
            transform: translateY(-50%);
            overflow: hidden;
            border-radius: 4px;
            transition: background 0.3s;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.5);
        }
        .dependent-mode-active .dependency-line {
            background: #551111;
        }
        .dependency-line::after {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, #EF4444, #EF4444, transparent);
            opacity: 0;
            transition: opacity 0.3s;
        }
        .dependent-mode-active .dependency-line::after {
            opacity: 1;
            animation: flow 0.8s linear infinite;
        }
        @keyframes flow {
            100% { left: 100%; }
        }
        
        .legend {
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-top: -5px;
            font-size: 16px;
            font-weight: 600;
        }
        .legend-item { display: flex; align-items: center; gap: 8px; }
        .color-box { width: 18px; height: 18px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.3); }
        
        @keyframes pop {
            0% { transform: scale(1); }
            50% { transform: scale(1.08); }
            100% { transform: scale(1); }
        }
        .pop { animation: pop 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
        
        /* Custom Scrollbar for Log */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #111; border-radius: 4px; }
        ::-webkit-scrollbar-thumb { background: #444; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #555; }
    </style>
</head>
<body>

<div class="dashboard">
    <div class="controls">
        <div class="toggle-container" id="modeToggle" title="Click to toggle dependency">
            <span id="modeIcon">🔓</span> <span id="modeText">Independent Mode</span>
        </div>
        <button class="btn-spin" id="btnSpin1">Spin 1x</button>
        <button class="btn-spin" id="btnSpin10">Spin 10x</button>
        <button class="btn-spin" id="btnSpin100">Spin 100x</button>
        <button class="btn-reset" id="btnReset">Reset Stats</button>
    </div>
    
    <div class="spinners-area" id="spinnersArea">
        <div class="spinner-box">
            <h3>Spinner A: Weather</h3>
            <div class="spinner-wrapper">
                <div class="pointer"></div>
                <div class="spinner" id="spinner1">
                    <svg viewBox="0 0 100 100">
                        <circle r="25" cx="50" cy="50" fill="#3B82F6" /> <!-- Rainy (Blue) -->
                        <circle r="25" cx="50" cy="50" fill="transparent"
                                stroke="#FBBF24" stroke-width="50"
                                pathLength="100" stroke-dasharray="60 100" /> <!-- Sunny (Yellow) 60% -->
                    </svg>
                    <div class="wheel-overlay"></div>
                    <div class="center-pin"></div>
                </div>
            </div>
            <div class="legend">
                <div class="legend-item"><div class="color-box" style="background:#FBBF24"></div> Sunny (60%)</div>
                <div class="legend-item"><div class="color-box" style="background:#3B82F6"></div> Rainy (40%)</div>
            </div>
            <div class="outcome-label" id="outcome1">...</div>
            <div class="dependency-line"></div>
        </div>
        
        <div class="spinner-box">
            <h3>Spinner B: Outfit</h3>
            <div class="spinner-wrapper">
                <div class="pointer"></div>
                <div class="spinner" id="spinner2">
                    <svg viewBox="0 0 100 100">
                        <circle r="25" cx="50" cy="50" fill="#A855F7" /> <!-- Coat (Purple) -->
                        <circle r="25" cx="50" cy="50" fill="transparent"
                                stroke="#F97316" stroke-width="50"
                                pathLength="100" stroke-dasharray="50 100" 
                                id="spinner2-slice" class="slice" /> <!-- T-Shirt (Orange) -->
                    </svg>
                    <div class="wheel-overlay"></div>
                    <div class="center-pin"></div>
                </div>
            </div>
            <div class="legend" id="legend2">
                <div class="legend-item"><div class="color-box" style="background:#F97316"></div> T-Shirt (50%)</div>
                <div class="legend-item"><div class="color-box" style="background:#A855F7"></div> Coat (50%)</div>
            </div>
            <div class="outcome-label" id="outcome2">...</div>
        </div>
    </div>
    
    <div class="stats-area">
        <div class="stat-card" id="card-overall">
            <div class="stat-title">Overall P(T-Shirt)</div>
            <div class="stat-value" id="stat-overall" style="color:#F97316">--%</div>
            <div style="font-size:14px;color:#888" id="count-overall">0 spins</div>
        </div>
        <div class="stat-card" id="card-sun">
            <div class="stat-title">P(T-Shirt | Sunny)</div>
            <div class="stat-value" id="stat-sun" style="color:#FBBF24">--%</div>
            <div style="font-size:14px;color:#888" id="count-sun">0 sunny days</div>
        </div>
        <div class="stat-card" id="card-rain">
            <div class="stat-title">P(T-Shirt | Rainy)</div>
            <div class="stat-value" id="stat-rain" style="color:#60A5FA">--%</div>
            <div style="font-size:14px;color:#888" id="count-rain">0 rainy days</div>
        </div>
    </div>
    
    <div class="log-container" id="logBox">
        <div style="color:#666; font-style: italic;">Log history will appear here...</div>
    </div>
    <div style="text-align:center; font-size:12px; color:#888;">Log keeps the latest 100 events; older entries are removed.</div>
</div>

<script>
    let isDependent = false;
    let rot1 = 0;
    let rot2 = 0;
    
    let stats = {
        total: 0,
        sun: 0, rain: 0,
        tshirt: 0, coat: 0,
        sun_tshirt: 0, sun_coat: 0,
        rain_tshirt: 0, rain_coat: 0
    };
    let activeTimeouts = [];
    const MAX_LOG_ENTRIES = 100;

    function scheduleTimeout(callback, delay) {
        let timeoutId;
        timeoutId = setTimeout(() => {
            activeTimeouts = activeTimeouts.filter(id => id !== timeoutId);
            callback();
        }, delay);
        activeTimeouts.push(timeoutId);
    }
    
    const ui = {
        modeToggle: document.getElementById('modeToggle'),
        modeIcon: document.getElementById('modeIcon'),
        modeText: document.getElementById('modeText'),
        spinnersArea: document.getElementById('spinnersArea'),
        spinner1: document.getElementById('spinner1'),
        spinner2: document.getElementById('spinner2'),
        slice2: document.getElementById('spinner2-slice'),
        outcome1: document.getElementById('outcome1'),
        outcome2: document.getElementById('outcome2'),
        legend2: document.getElementById('legend2'),
        logBox: document.getElementById('logBox'),
        btnSpin1: document.getElementById('btnSpin1'),
        btnSpin10: document.getElementById('btnSpin10'),
        btnSpin100: document.getElementById('btnSpin100'),
        btnReset: document.getElementById('btnReset'),
        statOverall: document.getElementById('stat-overall'),
        statSun: document.getElementById('stat-sun'),
        statRain: document.getElementById('stat-rain'),
        cntOverall: document.getElementById('count-overall'),
        cntSun: document.getElementById('count-sun'),
        cntRain: document.getElementById('count-rain'),
        cardOverall: document.getElementById('card-overall'),
        cardSun: document.getElementById('card-sun'),
        cardRain: document.getElementById('card-rain'),
    };
    
    ui.modeToggle.addEventListener('click', () => {
        isDependent = !isDependent;
        if(isDependent) {
            ui.modeToggle.classList.add('dependent');
            ui.spinnersArea.classList.add('dependent-mode-active');
            ui.modeIcon.innerText = '🔗';
            ui.modeText.innerText = 'Dependent Mode';
            document.querySelector('.toggle-container').style.borderColor = '#EF4444';
        } else {
            ui.modeToggle.classList.remove('dependent');
            ui.spinnersArea.classList.remove('dependent-mode-active');
            ui.modeIcon.innerText = '🔓';
            ui.modeText.innerText = 'Independent Mode';
            document.querySelector('.toggle-container').style.borderColor = '#555';
        }
        updateSpinner2Visuals(50); // Reset to 50/50 when switching
        log("Switched to " + (isDependent ? "<strong style='color:#EF4444'>Dependent</strong>" : "<strong>Independent</strong>") + " mode. Notice how the stats respond differently now!");
    });
    
    function updateSpinner2Visuals(tshirtPct) {
        ui.slice2.setAttribute('stroke-dasharray', `${tshirtPct} 100`);
        ui.legend2.innerHTML = `
            <div class="legend-item"><div class="color-box" style="background:#F97316"></div> T-Shirt (${tshirtPct}%)</div>
            <div class="legend-item"><div class="color-box" style="background:#A855F7"></div> Coat (${100-tshirtPct}%)</div>
        `;
    }
    
    function setButtonsDisabled(disabled) {
        ui.btnSpin1.disabled = disabled;
        ui.btnSpin10.disabled = disabled;
        ui.btnSpin100.disabled = disabled;
        ui.modeToggle.style.pointerEvents = disabled ? 'none' : 'auto';
        ui.modeToggle.style.opacity = disabled ? '0.5' : '1';
    }
    
    function log(msg) {
        const div = document.createElement('div');
        div.className = 'log-entry';
        div.innerHTML = msg;
        ui.logBox.prepend(div);
        while (ui.logBox.children.length > MAX_LOG_ENTRIES) {
            ui.logBox.removeChild(ui.logBox.lastChild);
        }
    }
    
    function updateStats() {
        const pTshirt = stats.total > 0 ? (stats.tshirt / stats.total * 100).toFixed(1) : '--';
        const pTshirtSun = stats.sun > 0 ? (stats.sun_tshirt / stats.sun * 100).toFixed(1) : '--';
        const pTshirtRain = stats.rain > 0 ? (stats.rain_tshirt / stats.rain * 100).toFixed(1) : '--';
        
        ui.statOverall.innerText = pTshirt + '%';
        ui.statSun.innerText = pTshirtSun + '%';
        ui.statRain.innerText = pTshirtRain + '%';
        
        ui.cntOverall.innerText = stats.total + ' spins';
        ui.cntSun.innerText = stats.sun + ' sunny days';
        ui.cntRain.innerText = stats.rain + ' rainy days';
        
        // Trigger pop animation
        [ui.cardOverall, ui.cardSun, ui.cardRain].forEach(el => {
            el.classList.remove('pop');
            void el.offsetWidth; // trigger reflow
            el.classList.add('pop');
        });
    }
    
    function runSim(count, animate = false) {
        setButtonsDisabled(true);
        
        if (animate) {
            ui.outcome1.innerText = 'Spinning...';
            ui.outcome2.innerText = 'Waiting...';
            
            // Spin 1: Weather (60% Sun, 40% Rain)
            const isSun = Math.random() < 0.6;
            
            // Calculate target angle
            // Sun slice is 60% -> 216 deg. So Sun is [0, 216]. Rain is [216, 360].
            let targetAngle1;
            if(isSun) {
                const theta = 5 + Math.random() * (216 - 10);
                targetAngle1 = 360 - theta;
            } else {
                const theta = 216 + 5 + Math.random() * (144 - 10);
                targetAngle1 = 360 - theta;
            }
            
            rot1 += (360 * 5) + (targetAngle1 - (rot1 % 360));
            ui.spinner1.style.transition = 'transform 2.5s cubic-bezier(0.25, 0.1, 0.25, 1)';
            ui.spinner1.style.transform = `rotate(${rot1}deg)`;
            
            scheduleTimeout(() => {
                ui.outcome1.innerHTML = isSun ? '<span class="highlight-sun">☀️ Sunny</span>' : '<span class="highlight-rain">🌧️ Rainy</span>';
                
                let tshirtPct = 50;
                if(isDependent) {
                    tshirtPct = isSun ? 90 : 10;
                    updateSpinner2Visuals(tshirtPct);
                }
                
                // Wait for slice animation if dependent
                scheduleTimeout(() => {
                    ui.outcome2.innerText = 'Spinning...';
                    
                    const isTshirt = Math.random() < (tshirtPct / 100);
                    
                    let targetAngle2;
                    const tshirtDeg = tshirtPct * 3.6;
                    if(isTshirt) {
                        const theta = 5 + Math.random() * (tshirtDeg - 10);
                        targetAngle2 = 360 - theta;
                    } else {
                        const theta = tshirtDeg + 5 + Math.random() * (360 - tshirtDeg - 10);
                        targetAngle2 = 360 - theta;
                    }
                    
                    rot2 += (360 * 5) + (targetAngle2 - (rot2 % 360));
                    ui.spinner2.style.transition = 'transform 2.5s cubic-bezier(0.25, 0.1, 0.25, 1)';
                    ui.spinner2.style.transform = `rotate(${rot2}deg)`;
                    
                    scheduleTimeout(() => {
                        ui.outcome2.innerHTML = isTshirt ? '<span class="highlight-tshirt">👕 T-Shirt</span>' : '<span class="highlight-coat">🧥 Coat</span>';
                        recordStat(isSun, isTshirt);
                        
                        const wHtml = isSun ? '<span class="highlight-sun">☀️ Sunny</span>' : '<span class="highlight-rain">🌧️ Rainy</span>';
                        const oHtml = isTshirt ? '<span class="highlight-tshirt">👕 T-Shirt</span>' : '<span class="highlight-coat">🧥 Coat</span>';
                        log(`Result: ${wHtml} ➔ ${oHtml}`);
                        
                        updateStats();
                        setButtonsDisabled(false);
                    }, 2600);
                    
                }, isDependent ? 700 : 100); // Wait for the visual slice transition to complete
            }, 2600);
            
        } else {
            // Fast simulation without animation
            ui.spinner1.style.transition = 'none';
            ui.spinner2.style.transition = 'none';
            
            for(let i=0; i<count; i++) {
                const isSun = Math.random() < 0.6;
                let tshirtPct = 50;
                if(isDependent) tshirtPct = isSun ? 90 : 10;
                const isTshirt = Math.random() < (tshirtPct / 100);
                
                recordStat(isSun, isTshirt);
            }
            
            log(`Fast-forwarded ${count} spins. Check the updated statistics below!`);
            updateStats();
            
            // Randomly position the spinners visually to end somewhere
            rot1 += Math.random() * 360;
            rot2 += Math.random() * 360;
            ui.spinner1.style.transform = `rotate(${rot1}deg)`;
            ui.spinner2.style.transform = `rotate(${rot2}deg)`;
            
            ui.outcome1.innerText = 'Multiple Spins';
            ui.outcome2.innerText = 'Completed';
            
            setButtonsDisabled(false);
        }
    }
    
    function recordStat(isSun, isTshirt) {
        stats.total++;
        if(isSun) {
            stats.sun++;
            if(isTshirt) { stats.tshirt++; stats.sun_tshirt++; }
            else { stats.coat++; stats.sun_coat++; }
        } else {
            stats.rain++;
            if(isTshirt) { stats.tshirt++; stats.rain_tshirt++; }
            else { stats.coat++; stats.rain_coat++; }
        }
    }
    
    ui.btnSpin1.addEventListener('click', () => runSim(1, true));
    ui.btnSpin10.addEventListener('click', () => runSim(10, false));
    ui.btnSpin100.addEventListener('click', () => runSim(100, false));
    
    ui.btnReset.addEventListener('click', () => {
        activeTimeouts.forEach(timeoutId => clearTimeout(timeoutId));
        activeTimeouts = [];
        setButtonsDisabled(false);
        stats = {
            total: 0, sun: 0, rain: 0, tshirt: 0, coat: 0,
            sun_tshirt: 0, sun_coat: 0, rain_tshirt: 0, rain_coat: 0
        };
        updateStats();
        ui.logBox.innerHTML = '<div style="color:#666; font-style: italic;">Log history cleared...</div>';
        ui.outcome1.innerText = '...';
        ui.outcome2.innerText = '...';
        log("Stats have been reset.");
    });

</script>
</body>
</html>
"""

components.html(html_code, height=950, scrolling=False)

st.markdown("---")
st.markdown("### 🧠 The Core Insight")
st.markdown("""
- **Independent Events:** Knowing one outcome tells you nothing about the other. The probabilities stay exactly the same.
  - *Example in AI:* A pixel in the top-left corner of an image and a pixel in the bottom-right might be completely independent. Knowing one is black doesn't help guess the other.
- **Dependent Events:** Knowing one outcome changes the probabilities of the other. The "sample space" morphs based on new information.
  - *Example in AI:* Words in a sentence are highly dependent! If the previous word was "Eiffel", the next word is highly likely to be "Tower". This dependence is what makes Language Models work!
""")

st.success("""
**💡 Notice what happens in the lab:**
- In **Independent Mode**, `P(T-Shirt | Sunny)` and `P(T-Shirt | Rainy)` will roughly equal the overall `P(T-Shirt)`. Spinner A's result gives you absolutely no advantage in predicting Spinner B.
- In **Dependent Mode**, the conditional probabilities wildly diverge from the overall probability. Spinner A *directly informs* you about Spinner B!
""")
