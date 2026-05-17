import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Conditional Probability: P(A|B)", layout="wide")

def render_conditional_probability_interactive():
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
        body { margin: 0; padding: 0; font-family: 'Inter', sans-serif; background: transparent; color: white; user-select: none; overflow: hidden; }
        .container {
            background: #0f172a; border-radius: 16px; padding: 30px;
            border: 1px solid rgba(255,255,255,0.1); display: flex; flex-direction: column; align-items: center; gap: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        
        .space {
            display: flex; gap: 12px; flex-wrap: wrap; justify-content: center; align-content: center;
            width: 100%; max-width: 650px; padding: 30px;
            background: #1e293b; border-radius: 16px; border: 2px dashed #475569;
            min-height: 220px;
            transition: all 0.5s ease;
        }
        
        .space.focus-b { border-color: #f472b6; background: rgba(244, 114, 182, 0.05); }
        .space.focus-a { border-color: #38bdf8; background: rgba(56, 189, 248, 0.05); }

        .orb {
            width: 42px; height: 42px; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-weight: 900; font-size: 16px; color: transparent;
            transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
            box-shadow: inset 0 0 15px rgba(0,0,0,0.5);
            border: 3px solid rgba(255,255,255,0.1);
            position: relative;
        }

        /* Base colors */
        .orb.a-only { background: rgba(56, 189, 248, 0.7); border-color: #38bdf8; }
        .orb.b-only { background: rgba(244, 114, 182, 0.7); border-color: #f472b6; }
        .orb.ab { background: rgba(167, 139, 250, 0.8); border-color: #a78bfa; }
        .orb.none { background: rgba(100, 116, 139, 0.3); border-color: #475569; }

        /* Icons for intersection */
        .orb.ab::after { content: '★'; color: white; opacity: 0.8; font-size: 18px; }

        /* Conditioned state */
        .orb.dropped {
            opacity: 0.1;
            transform: scale(0.2) translateY(80px);
            filter: grayscale(100%);
            border-color: transparent;
            box-shadow: none;
        }

        .orb.highlight {
            transform: scale(1.15);
            box-shadow: 0 0 20px currentColor, inset 0 0 10px rgba(255,255,255,0.5);
            border-width: 4px;
        }
        
        .orb.highlight.ab { box-shadow: 0 0 20px #a78bfa, inset 0 0 10px rgba(255,255,255,0.5); }
        .orb.highlight.a-only { box-shadow: 0 0 20px #38bdf8, inset 0 0 10px rgba(255,255,255,0.5); }

        .controls { display: flex; gap: 15px; flex-wrap: wrap; justify-content: center; }
        
        button {
            background: #1e293b; color: #cbd5e1; border: 1px solid #475569;
            padding: 12px 24px; border-radius: 8px; font-family: 'Inter', sans-serif;
            font-size: 15px; font-weight: 700; cursor: pointer; transition: all 0.2s;
        }
        button:hover { background: #334155; color: white; transform: translateY(-2px); }
        
        button.selected-all { background: #cbd5e1; color: #0f172a; border-color: #cbd5e1; box-shadow: 0 0 15px rgba(203, 213, 225, 0.4); }
        button.selected-b { background: #f472b6; color: #0f172a; border-color: #f472b6; box-shadow: 0 0 15px rgba(244, 114, 182, 0.4); }
        button.selected-a { background: #38bdf8; color: #0f172a; border-color: #38bdf8; box-shadow: 0 0 15px rgba(56, 189, 248, 0.4); }

        .legend { display: flex; gap: 25px; font-size: 15px; font-weight: bold; margin-bottom: 5px; flex-wrap: wrap; justify-content: center; }
        .leg-item { display: flex; align-items: center; gap: 8px; color: #cbd5e1; }
        .dot { width: 14px; height: 14px; border-radius: 50%; border: 2px solid rgba(255,255,255,0.2); }
        .dot.a { background: #38bdf8; }
        .dot.b { background: #f472b6; }
        .dot.ab { background: #a78bfa; }
        .dot.none { background: #475569; }

        .math-panel {
            background: rgba(0,0,0,0.4); padding: 20px 40px; border-radius: 12px; width: 100%; max-width: 650px;
            display: flex; justify-content: space-between; align-items: center;
            border: 1px solid rgba(255,255,255,0.05);
        }
        
        .equation { font-size: 28px; font-weight: 900; color: white; display: flex; align-items: center; gap: 15px; }
        .fraction { display: flex; flex-direction: column; align-items: center; }
        .numerator { padding: 0 10px; border-bottom: 3px solid white; transition: color 0.3s; }
        .denominator { padding: 0 10px; transition: color 0.3s; }
        .val { color: #4ade80; font-size: 32px; transition: color 0.3s; }

        .desc-box {
            background: #1e293b; padding: 15px; border-radius: 8px; width: 100%; max-width: 650px;
            border-left: 4px solid #cbd5e1; transition: border-color 0.3s;
        }
        .desc { font-size: 15px; color: #cbd5e1; text-align: left; line-height: 1.5; }
        .desc b { color: white; }
    </style>
    </head>
    <body>
        <div class="container">
            <div class="legend">
                <div class="leg-item"><div class="dot a"></div> A (Math Only)</div>
                <div class="leg-item"><div class="dot b"></div> B (AI Only)</div>
                <div class="leg-item"><div class="dot ab"></div> Both (A ∩ B)</div>
                <div class="leg-item"><div class="dot none"></div> Neither</div>
            </div>

            <div class="space" id="orbs">
                <!-- JS will populate 40 orbs -->
            </div>

            <div class="controls">
                <button onclick="setCondition('all', this)" class="selected-all" id="btn-all">1. Full Universe (Ω)</button>
                <button onclick="setCondition('B', this)" id="btn-b">2. Given "Student in AI Club" (B)</button>
                <button onclick="setCondition('A', this)" id="btn-a">3. Given "Student likes Math" (A)</button>
            </div>
            
            <div class="desc-box" id="desc-box">
                <div class="desc" id="desc-text">
                    This is the full Sample Space (Ω) of 40 students. Let's calculate <b>P(A)</b>: the chance of randomly picking a Math student out of everyone.
                </div>
            </div>

            <div class="math-panel">
                <div class="equation">
                    <span id="formula-left">P(A) = </span>
                    <div class="fraction">
                        <span class="numerator" id="num">16</span>
                        <span class="denominator" id="den">40</span>
                    </div>
                    <span> = </span>
                    <span class="val" id="prob">0.40</span>
                </div>
            </div>
        </div>

        <script>
            const space = document.getElementById('orbs');
            const orbs = [];
            
            // Total = 40
            // A ∩ B = 8
            // A only = 8
            // B only = 12
            // Neither = 12
            const config = [
                { type: 'ab', count: 8 },
                { type: 'a-only', count: 8 },
                { type: 'b-only', count: 12 },
                { type: 'none', count: 12 }
            ];

            // Create orbs
            let allTypes = [];
            config.forEach(c => {
                for(let i=0; i<c.count; i++) allTypes.push(c.type);
            });
            // Shuffle deterministically so it looks nice but mixed
            const seed = [3, 15, 2, 8, 30, 12, 1, 22, 5, 33, 11, 29, 4, 18, 7, 25, 9, 38, 14, 21, 6, 27, 10, 31, 13, 19, 0, 35, 16, 24, 17, 39, 20, 26, 23, 34, 28, 32, 36, 37];
            let shuffled = new Array(40);
            for(let i=0; i<40; i++) shuffled[i] = allTypes[seed[i]];

            shuffled.forEach(t => {
                const orb = document.createElement('div');
                orb.className = `orb ${t}`;
                orb.dataset.type = t;
                space.appendChild(orb);
                orbs.push(orb);
            });

            function setCondition(cond, btn) {
                // Reset buttons
                document.querySelectorAll('button').forEach(b => {
                    b.classList.remove('selected-all', 'selected-a', 'selected-b');
                });
                
                let num = 0;
                let den = 0;
                let targetNumType = [];
                let targetDenType = [];
                
                const descBox = document.getElementById('desc-box');
                const spaceBox = document.getElementById('orbs');
                spaceBox.className = 'space'; // reset

                if (cond === 'all') {
                    btn.classList.add('selected-all');
                    targetDenType = ['ab', 'a-only', 'b-only', 'none'];
                    targetNumType = ['ab', 'a-only']; // Showing P(A)
                    document.getElementById('desc-text').innerHTML = "This is the full Sample Space (Ω) of 40 students. Let's calculate <b>P(A)</b>: the chance of randomly picking a Math student out of the entire universe.";
                    document.getElementById('formula-left').innerHTML = "P(<span style='color:#38bdf8'>A</span>) = ";
                    descBox.style.borderColor = '#cbd5e1';
                } else if (cond === 'B') {
                    btn.classList.add('selected-b');
                    targetDenType = ['ab', 'b-only'];
                    targetNumType = ['ab']; // Showing P(A|B)
                    document.getElementById('desc-text').innerHTML = "We are told the student is in AI Club. <b>The universe violently shrinks to B.</b> All non-B students drop out of existence. What is the chance they ALSO like Math? <b>P(A|B)</b>.";
                    document.getElementById('formula-left').innerHTML = "P(<span style='color:#38bdf8'>A</span> | <span style='color:#f472b6'>B</span>) = ";
                    descBox.style.borderColor = '#f472b6';
                    spaceBox.classList.add('focus-b');
                } else if (cond === 'A') {
                    btn.classList.add('selected-a');
                    targetDenType = ['ab', 'a-only'];
                    targetNumType = ['ab']; // Showing P(B|A)
                    document.getElementById('desc-text').innerHTML = "We are told the student likes Math. <b>The universe shrinks to A.</b> All non-Math students disappear. What is the chance they are ALSO in AI Club? <b>P(B|A)</b>.";
                    document.getElementById('formula-left').innerHTML = "P(<span style='color:#f472b6'>B</span> | <span style='color:#38bdf8'>A</span>) = ";
                    descBox.style.borderColor = '#38bdf8';
                    spaceBox.classList.add('focus-a');
                }

                orbs.forEach(orb => {
                    const t = orb.dataset.type;
                    orb.classList.remove('dropped', 'highlight');
                    
                    if (!targetDenType.includes(t)) {
                        orb.classList.add('dropped');
                    } else {
                        den++;
                        if (targetNumType.includes(t)) {
                            orb.classList.add('highlight');
                            num++;
                        }
                    }
                });

                // Update Math Panel
                document.getElementById('num').innerText = num;
                document.getElementById('den').innerText = den;
                document.getElementById('prob').innerText = (num / den).toFixed(2);
                
                // Color formatting
                const denEl = document.getElementById('den');
                const numEl = document.getElementById('num');
                const probEl = document.getElementById('prob');
                
                if(cond === 'B') { 
                    denEl.style.color = '#f472b6'; 
                    numEl.style.color = '#a78bfa'; 
                    probEl.style.color = '#f472b6';
                } else if(cond === 'A') { 
                    denEl.style.color = '#38bdf8'; 
                    numEl.style.color = '#a78bfa'; 
                    probEl.style.color = '#38bdf8';
                } else { 
                    denEl.style.color = 'white'; 
                    numEl.style.color = '#38bdf8'; 
                    probEl.style.color = '#cbd5e1';
                }
            }
            
            // Init
            setCondition('all', document.getElementById('btn-all'));
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=650)

def main():
    st.title("🎯 Page 25: Conditional Probability - P(A|B)")
    st.markdown(
        """
        Welcome to the world of **shifting perspectives**. 
        
        Normally, probability is measured against the **entire universe (Ω)**. But what happens if you receive a clue? If someone whispers, *"Hey, event B already happened"*, your entire universe instantly shrinks. You no longer care about the full sample space—you only care about the **B** outcomes.
        
        Conditional probability asks:
        $$ P(A \\mid B) = \\frac{P(A \\cap B)}{P(B)} $$
        
        Read it simply as: *"Out of the new universe where **B** is true, what fraction also satisfies **A**?"*
        """
    )
    
    st.markdown("### 1) The Shrinking Universe")
    st.markdown("Interact with the simulation below. Watch how knowing a condition violently drops irrelevant outcomes and changes the denominator.")
    
    render_conditional_probability_interactive()
    
    st.divider()

    st.markdown("### 2) The Story Challenge 🧠")
    st.markdown(
        r"""
        Think about the numbers in the simulation above:
        - Let **A = Student likes Math** (Blue)
        - Let **B = Student is in AI Club** (Pink)

        Notice the profound difference:
        - $P(A) = 0.40$ (If you pick a random student, there's a 40% chance they like Math).
        - $P(A \mid B) = 0.40$ (If you pick from the AI Club, there's a 40% chance they like Math).
        - $P(B \mid A) = 0.50$ (If you pick from the Math lovers, there's a 50% chance they are in the AI Club).

        **The Direction Matters!**
        $P(A \mid B)$ is usually completely different from $P(B \mid A)$. 
        - E.g., $P(\text{has a steering wheel} \mid \text{is a car})$ is nearly $1.00$. 
        - But $P(\text{is a car} \mid \text{has a steering wheel})$ is lower (it could be a boat, a bus, or a golf cart).

        **When you condition, always ask yourself: "What is my new denominator?"**
        """
    )
    
    st.info(
        """
        ### Recap
        - **Conditioning shrinks the sample space.** You throw away everything that contradicts the given condition.
        - The new denominator is the number of outcomes in the condition.
        - The numerator is the overlap (the outcomes that satisfy both the new universe and the target event).
        
        **Next up:** *Independence* — what happens when knowing B tells you absolutely *nothing* about A?
        """
    )

if __name__ == "__main__":
    main()
