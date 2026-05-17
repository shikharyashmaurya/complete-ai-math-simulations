import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Sample Space & Probability", layout="wide")

def render_sample_space_interactive():
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
        body { margin: 0; padding: 0; font-family: 'Inter', sans-serif; background: transparent; color: white; user-select: none; }
        .container {
            background: #0f172a; border-radius: 16px; padding: 30px;
            border: 1px solid rgba(255,255,255,0.1);
            display: flex; flex-direction: column; align-items: center; gap: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        
        .title { color: #94a3b8; text-transform: uppercase; letter-spacing: 2px; font-size: 14px; font-weight: bold; }
        
        .space { display: flex; gap: 20px; flex-wrap: wrap; justify-content: center; }
        
        .orb {
            width: 80px; height: 80px; border-radius: 20px;
            background: #1e293b; display: flex; align-items: center; justify-content: center;
            font-size: 32px; font-weight: 900; color: #64748b;
            border: 2px solid #334155; transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 10px 15px rgba(0,0,0,0.2);
        }
        
        .orb.active {
            background: #0284c7; color: white;
            border-color: #38bdf8;
            box-shadow: 0 0 25px rgba(56, 189, 248, 0.6), inset 0 0 10px rgba(255,255,255,0.3);
            transform: translateY(-10px) scale(1.05);
        }

        .controls { display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; }
        
        button {
            background: #1e293b; color: #cbd5e1; border: 1px solid #475569;
            padding: 10px 20px; border-radius: 8px; font-family: 'Inter', sans-serif;
            font-weight: 700; cursor: pointer; transition: all 0.2s;
        }
        
        button:hover { background: #334155; color: white; }
        button.selected { background: #38bdf8; color: #0f172a; border-color: #38bdf8; box-shadow: 0 0 15px rgba(56, 189, 248, 0.4); }

        .math-panel {
            background: rgba(0,0,0,0.4); padding: 20px; border-radius: 12px; width: 100%; max-width: 600px;
            display: flex; justify-content: space-between; align-items: center;
            border: 1px solid rgba(255,255,255,0.05);
        }
        
        .math-stat { display: flex; flex-direction: column; align-items: center; gap: 5px; }
        .math-label { color: #94a3b8; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; }
        .math-val { font-size: 24px; font-weight: 900; color: #fbbf24; }
        
        .equation { font-size: 28px; font-weight: 900; color: white; display: flex; align-items: center; gap: 10px; }
        .fraction { display: flex; flex-direction: column; align-items: center; font-size: 24px; }
        .numerator { padding: 0 5px; border-bottom: 3px solid white; }
        .denominator { padding: 0 5px; }
    </style>
    </head>
    <body>
        <div class="container">
            <div class="title">The Universe of Outcomes: Ω = {1, 2, 3, 4, 5, 6}</div>
            
            <div class="space" id="orbs">
                <div class="orb" data-val="1">1</div>
                <div class="orb" data-val="2">2</div>
                <div class="orb" data-val="3">3</div>
                <div class="orb" data-val="4">4</div>
                <div class="orb" data-val="5">5</div>
                <div class="orb" data-val="6">6</div>
            </div>

            <div class="controls">
                <button onclick="setEvent('even', this)">Even {2,4,6}</button>
                <button onclick="setEvent('odd', this)">Odd {1,3,5}</button>
                <button onclick="setEvent('prime', this)">Prime {2,3,5}</button>
                <button onclick="setEvent('high', this)">At least 5 {5,6}</button>
                <button onclick="setEvent('all', this)" class="selected">Whole Space Ω</button>
            </div>
            
            <div class="math-panel">
                <div class="math-stat">
                    <span class="math-label">Event Size |A|</span>
                    <span class="math-val" id="size-a">6</span>
                </div>
                <div class="equation">
                    <span>P(A) = </span>
                    <div class="fraction">
                        <span class="numerator" id="num">6</span>
                        <span class="denominator">6</span>
                    </div>
                    <span> = </span>
                    <span style="color:#4ade80" id="prob">1.00</span>
                </div>
            </div>
        </div>

        <script>
            const events = {
                'even': [2, 4, 6],
                'odd': [1, 3, 5],
                'prime': [2, 3, 5],
                'high': [5, 6],
                'all': [1, 2, 3, 4, 5, 6]
            };

            function setEvent(evName, btn) {
                // Update buttons
                document.querySelectorAll('button').forEach(b => b.classList.remove('selected'));
                btn.classList.add('selected');

                const targetSet = events[evName];
                let count = 0;

                // Update orbs
                document.querySelectorAll('.orb').forEach(orb => {
                    const val = parseInt(orb.getAttribute('data-val'));
                    if (targetSet.includes(val)) {
                        orb.classList.add('active');
                        count++;
                    } else {
                        orb.classList.remove('active');
                    }
                });

                // Update Math
                document.getElementById('size-a').innerText = count;
                document.getElementById('num').innerText = count;
                document.getElementById('prob').innerText = (count / 6).toFixed(2);
            }
            
            // Init
            setEvent('all', document.querySelector('.controls button:last-child'));
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=450)

def render_venn_interactive():
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
        body { margin: 0; padding: 0; font-family: 'Inter', sans-serif; background: transparent; color: white; user-select: none; }
        .container {
            background: #0f172a; border-radius: 16px; padding: 30px;
            border: 1px solid rgba(255,255,255,0.1); display: flex; flex-direction: column; align-items: center; gap: 20px;
        }
        
        .selectors { display: flex; gap: 40px; width: 100%; justify-content: center; }
        .selector-group { display: flex; flex-direction: column; gap: 10px; align-items: center; }
        .selector-group select {
            background: #1e293b; color: white; border: 1px solid #475569; padding: 10px; border-radius: 8px;
            font-family: 'Inter'; font-weight: bold; cursor: pointer; outline: none;
        }
        
        .venn-container {
            position: relative; width: 400px; height: 300px; margin-top: 20px;
            display: flex; justify-content: center; align-items: center;
        }
        
        .circle {
            position: absolute; width: 220px; height: 220px; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            mix-blend-mode: screen; transition: all 0.5s ease;
            box-shadow: inset 0 0 30px rgba(0,0,0,0.5);
        }
        
        .circle-A { background: rgba(56, 189, 248, 0.4); border: 4px solid #38bdf8; left: 40px; }
        .circle-B { background: rgba(244, 114, 182, 0.4); border: 4px solid #f472b6; right: 40px; }
        
        .label-A { position: absolute; top: -30px; left: 80px; color: #38bdf8; font-weight: 900; font-size: 20px; }
        .label-B { position: absolute; top: -30px; right: 80px; color: #f472b6; font-weight: 900; font-size: 20px; }
        
        .number {
            position: absolute; width: 36px; height: 36px; background: #0f172a;
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            font-weight: 900; border: 2px solid #cbd5e1; z-index: 10;
            transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        }
        
        .math-bar {
            background: rgba(0,0,0,0.4); padding: 15px 30px; border-radius: 12px;
            display: flex; gap: 20px; border: 1px solid rgba(255,255,255,0.05); margin-top: 10px;
            flex-wrap: wrap; justify-content: center;
        }
        .stat { display: flex; gap: 10px; font-size: 16px; font-weight: bold; }
        .stat .val { color: #fbbf24; }
        .stat-inter .val { color: #c084fc; } /* Blend of blue and pink */
        .stat-union .val { color: #4ade80; }
        
    </style>
    </head>
    <body>
        <div class="container">
            <div class="selectors">
                <div class="selector-group">
                    <span style="color:#38bdf8; font-weight:bold;">Event A</span>
                    <select id="sel-A" onchange="updateVenn()">
                        <option value="even">Even {2,4,6}</option>
                        <option value="low">≤ 3 {1,2,3}</option>
                        <option value="prime">Prime {2,3,5}</option>
                    </select>
                </div>
                <div class="selector-group">
                    <span style="color:#f472b6; font-weight:bold;">Event B</span>
                    <select id="sel-B" onchange="updateVenn()">
                        <option value="odd">Odd {1,3,5}</option>
                        <option value="high">≥ 4 {4,5,6}</option>
                        <option value="prime">Prime {2,3,5}</option>
                    </select>
                </div>
            </div>
            
            <div class="venn-container">
                <div class="circle circle-A"></div>
                <div class="circle circle-B"></div>
                <div class="label-A">Set A</div>
                <div class="label-B">Set B</div>
                
                <div class="number" id="n1">1</div>
                <div class="number" id="n2">2</div>
                <div class="number" id="n3">3</div>
                <div class="number" id="n4">4</div>
                <div class="number" id="n5">5</div>
                <div class="number" id="n6">6</div>
            </div>
            
            <div class="math-bar">
                <div class="stat">|A| = <span class="val" id="count-A">3</span></div>
                <div class="stat">|A<sup>c</sup>| = <span class="val" id="count-Ac" style="color:#94a3b8;">3</span></div>
                <div class="stat">|B| = <span class="val" id="count-B">3</span></div>
                <div class="stat">|B<sup>c</sup>| = <span class="val" id="count-Bc" style="color:#94a3b8;">3</span></div>
                <div class="stat stat-inter">|A ∩ B| = <span class="val" id="count-inter">0</span></div>
                <div class="stat stat-union">|A ∪ B| = <span class="val" id="count-union">6</span></div>
            </div>
        </div>

        <script>
            const sets = {
                'even': [2, 4, 6],
                'odd': [1, 3, 5],
                'low': [1, 2, 3],
                'high': [4, 5, 6],
                'prime': [2, 3, 5]
            };
            
            // Pre-defined positions to look random but structured
            const posA = [{x:-50, y:-40}, {x:-80, y:30}, {x:-30, y:60}];
            const posB = [{x:50, y:-40}, {x:80, y:30}, {x:30, y:60}];
            const posInter = [{x:0, y:-30}, {x:0, y:20}, {x:0, y:70}];
            const posOut = [{x:-150, y:-100}, {x:150, y:-100}, {x:0, y:-130}, {x:-150, y:100}, {x:150, y:100}, {x:0, y:140}];

            function updateVenn() {
                const valA = document.getElementById('sel-A').value;
                const valB = document.getElementById('sel-B').value;
                const A = sets[valA];
                const B = sets[valB];
                
                let countA = 0, countB = 0, countInter = 0, countUnion = 0;
                let idxA = 0, idxB = 0, idxInter = 0, idxOut = 0;

                for (let i = 1; i <= 6; i++) {
                    const el = document.getElementById('n' + i);
                    const inA = A.includes(i);
                    const inB = B.includes(i);
                    
                    let targetPos;
                    let color = "#cbd5e1";
                    let bg = "#0f172a";

                    if (inA && inB) {
                        countA++; countB++; countInter++; countUnion++;
                        targetPos = posInter[idxInter++];
                        bg = "#c084fc"; color = "white"; // purple for intersection
                    } else if (inA) {
                        countA++; countUnion++;
                        targetPos = posA[idxA++];
                        bg = "#0ea5e9"; color = "white"; // blue for A
                    } else if (inB) {
                        countB++; countUnion++;
                        targetPos = posB[idxB++];
                        bg = "#ec4899"; color = "white"; // pink for B
                    } else {
                        targetPos = posOut[idxOut++];
                    }
                    
                    el.style.transform = `translate(${targetPos.x}px, ${targetPos.y}px)`;
                    el.style.background = bg;
                    el.style.borderColor = color;
                    el.style.color = color;
                }
                
                document.getElementById('count-A').innerText = countA;
                document.getElementById('count-Ac').innerText = 6 - countA;
                document.getElementById('count-B').innerText = countB;
                document.getElementById('count-Bc').innerText = 6 - countB;
                document.getElementById('count-inter').innerText = countInter;
                document.getElementById('count-union').innerText = countUnion;
            }
            
            // Init
            updateVenn();
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=520)

def render_2d_space_interactive():
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
        body { margin: 0; padding: 0; font-family: 'Inter', sans-serif; background: transparent; color: white; user-select: none; }
        .container {
            background: #0f172a; border-radius: 16px; padding: 30px;
            border: 1px solid rgba(255,255,255,0.1); display: flex; flex-direction: column; align-items: center; gap: 20px;
        }
        
        .header { display: flex; gap: 20px; align-items: center; justify-content: space-between; width: 100%; max-width: 600px;}
        .slider-container { display: flex; flex-direction: column; gap: 5px; flex-grow: 1; }
        input[type=range] { width: 100%; cursor: pointer; accent-color: #fbbf24; }
        
        .stat-box {
            background: #1e293b; padding: 15px 25px; border-radius: 12px; border: 1px solid #334155;
            display: flex; flex-direction: column; align-items: center; min-width: 150px;
        }
        .stat-label { color: #94a3b8; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; }
        .stat-val { font-size: 24px; font-weight: 900; color: #fbbf24; }

        .grid-container {
            display: grid; grid-template-columns: auto repeat(6, 50px); grid-template-rows: auto repeat(6, 50px);
            gap: 4px; align-items: center; justify-items: center;
        }
        
        .axis-label { color: #94a3b8; font-weight: bold; font-size: 18px; }
        .axis-y { writing-mode: vertical-rl; transform: rotate(180deg); grid-row: 2 / span 6; grid-column: 1; margin-right: 10px; color: #38bdf8; }
        .axis-x { grid-column: 2 / span 6; grid-row: 1; margin-bottom: 10px; color: #f472b6; }
        
        .cell {
            width: 100%; height: 100%; background: #1e293b; border-radius: 8px;
            display: flex; align-items: center; justify-content: center;
            font-weight: bold; color: #64748b; font-size: 18px; transition: all 0.2s;
            border: 1px solid transparent; cursor: pointer; position: relative;
        }
        
        .cell:hover { background: #334155; color: white; border-color: #94a3b8; transform: scale(1.1); z-index: 10; }
        
        /* The magical heatmap colors */
        .c-2 { background: #4a044e; color: #fdf4ff; }
        .c-3 { background: #701a75; color: #fdf4ff; }
        .c-4 { background: #86198f; color: #fdf4ff; }
        .c-5 { background: #a21caf; color: #fdf4ff; }
        .c-6 { background: #c026d3; color: #fdf4ff; }
        .c-7 { background: #d946ef; color: white; }
        .c-8 { background: #e879f9; color: #4a044e; }
        .c-9 { background: #f0abfc; color: #4a044e; }
        .c-10 { background: #f5d0fe; color: #4a044e; }
        .c-11 { background: #fae8ff; color: #4a044e; }
        .c-12 { background: #fdf4ff; color: #4a044e; }
        
        .cell.highlight {
            border-color: #fbbf24; border-width: 3px; box-shadow: 0 0 15px rgba(251, 191, 36, 0.6);
            transform: scale(1.1); z-index: 5;
        }
        .cell.dimmed { opacity: 0.2; filter: grayscale(100%); }
        
        /* Tooltip */
        .tooltip {
            position: absolute; bottom: 110%; background: black; color: white; padding: 4px 8px;
            border-radius: 4px; font-size: 12px; pointer-events: none; opacity: 0; transition: opacity 0.2s;
            white-space: nowrap; z-index: 20;
        }
        .cell:hover .tooltip { opacity: 1; }

    </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="slider-container">
                    <div style="display:flex; justify-content:space-between; color:#cbd5e1; font-weight:bold;">
                        <span>Highlight Sum: <span id="sum-val" style="color:#fbbf24;font-size:20px;">7</span></span>
                    </div>
                    <input type="range" id="sum-slider" min="2" max="12" value="7" oninput="updateGrid()">
                </div>
                
                <div class="stat-box">
                    <span class="stat-label">Ways to make sum</span>
                    <span class="stat-val" id="ways-val">6</span>
                </div>
                
                <div class="stat-box">
                    <span class="stat-label">Probability</span>
                    <span class="stat-val" id="prob-val" style="color:#4ade80;">16.67%</span>
                </div>
            </div>
            
            <div class="grid-container" id="grid">
                <div class="axis-label axis-y">Die 1 (Coral) →</div>
                <div class="axis-label axis-x">Die 2 (Cyan) →</div>
                <!-- Generated via JS -->
            </div>
        </div>

        <script>
            const grid = document.getElementById('grid');
            
            // Generate Grid
            for (let i = 1; i <= 6; i++) {
                for (let j = 1; j <= 6; j++) {
                    const sum = i + j;
                    const cell = document.createElement('div');
                    cell.className = `cell c-${sum}`;
                    cell.innerText = sum;
                    cell.setAttribute('data-sum', sum);
                    cell.style.gridRow = i + 1;
                    cell.style.gridColumn = j + 1;
                    
                    const tooltip = document.createElement('div');
                    tooltip.className = 'tooltip';
                    tooltip.innerHTML = `(${i}, ${j}) = ${sum}`;
                    cell.appendChild(tooltip);
                    
                    grid.appendChild(cell);
                }
            }
            
            function updateGrid() {
                const targetSum = parseInt(document.getElementById('sum-slider').value);
                document.getElementById('sum-val').innerText = targetSum;
                
                let ways = 0;
                document.querySelectorAll('.cell').forEach(cell => {
                    const s = parseInt(cell.getAttribute('data-sum'));
                    if (s === targetSum) {
                        cell.classList.add('highlight');
                        cell.classList.remove('dimmed');
                        ways++;
                    } else {
                        cell.classList.remove('highlight');
                        cell.classList.add('dimmed');
                    }
                });
                
                document.getElementById('ways-val').innerText = ways;
                const prob = (ways / 36) * 100;
                document.getElementById('prob-val').innerText = prob.toFixed(2) + '%';
            }
            
            // Init
            updateGrid();
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=600)

def main():
    st.title("🎲 Page 23: Sample Space & Basic Probability")
    st.markdown(
        """
        Probability begins with mapping out the universe. Before you can ask "how likely is it?", you must ask **"what is possible?"**
        
        That complete list of everything that could possibly happen is called the **Sample Space (${\Omega}$)**. 
        For a single fair six-sided die, ${\Omega} = \{1, 2, 3, 4, 5, 6\}$. 

        An **Event (A)** is simply a subset of that universe. When all atoms in the universe are equally likely, finding the probability is just counting:
        $$ P(A) = \\frac{|A|}{|{\Omega}|} = \\frac{\\text{Number of winning outcomes}}{\\text{Total possible outcomes}} $$
        """
    )
    
    st.markdown("### 1) The Universe of Outcomes")
    st.markdown("Interact with the atoms below. Select an **Event** to watch the subset light up and see the probability calculated live.")
    
    render_sample_space_interactive()
    
    st.divider()

    st.markdown("### 2) Intersections, Unions & Complements (Venn Lab)")
    st.markdown(
        """
        Events can be combined using set theory operations:
        - **Complement ($A^c$)**: Everything NOT in A. The leftovers. $|A^c| = |\Omega| - |A|$.
        - **Intersection ($A \cap B$)**: The overlap. Outcomes that live in **both** A and B.
        - **Union ($A \cup B$)**: The merge. Outcomes that live in A, **or** B, **or both**.
        
        Play with the dropdowns to see how different events share atoms. Notice how $|A \cup B| = |A| + |B| - |A \cap B|$.
        """
    )
    
    render_venn_interactive()
    
    st.divider()

    st.markdown("### 3) 2D Sample Space: Rolling Two Dice")
    st.markdown(
        """
        When you roll **two dice**, the universe expands. It is no longer 6 atoms, it is the **Cartesian Product**: a 6x6 grid of **36 ordered pairs**.
        
        Use the slider to highlight a target sum. See how sums like **7** carve out a long diagonal with 6 different ways to win, while extreme sums like **2** or **12** have only 1 way to win.
        """
    )
    
    render_2d_space_interactive()
    
    st.info(
        """
        ### Recap
        - **Sample Space (Ω):** The absolute truth of all possible outcomes.
        - **Events:** Subsets of Ω that we care about.
        - **Counting is Probability:** If outcomes are equally likely, math reduces to simply counting glowing orbs.
        
        **Next up:** *Complement, Union, Intersection* — diving deeper into set theory operations before we hit Conditional Probability.
        """
    )

if __name__ == "__main__":
    main()
