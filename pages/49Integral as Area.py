import sys
from pathlib import Path

import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.assets import load_lab  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="Integral as Area", layout="wide")

def render_integral_lab():
    st.iframe(load_lab("p49_integral_area"), height=800)

def main():
    st.markdown("<h1 style='text-align: center; color: #22d3ee;'>📉 Page 49: Integral as Area</h1>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="background: rgba(34, 211, 238, 0.05); padding: 20px; border-radius: 15px; border-left: 5px solid #22d3ee; margin-bottom: 25px;">
        If <b>Derivatives</b> are about breaking things down into tiny slopes, 
        <b>Integrals</b> are about building them back up into a total quantity.
        <br><br>
        The most intuitive way to see an integral is as the <b>Area under a curve</b>. 
        Think of it as adding up an infinite number of infinitely thin rectangles.
        </div>
        """, unsafe_allow_html=True
    )

    col_main, col_sidebar = st.columns([3, 1])

    with col_main:
        st.markdown("### 🧪 The Riemann Sum Laboratory")
        st.markdown(
            "Experiment with how we approximate the area using rectangles. As you increase the number of slices (**n**), the approximation gets closer and closer to the exact value $F(b) - F(a)$. "
            "Switch the **sample point** between Left, Midpoint and Right: left/right sums shrink their error roughly like $1/n$, the midpoint sum like $1/n^2$. "
            "Try **y = sin(x) (signed area)**: rectangles below the x-axis count as *negative* area.")
        render_integral_lab()

    with col_sidebar:
        st.markdown("### 📝 Key Concepts")
        st.info("**1. Riemann Sum**\n\nApproximating area by summing rectangles (height taken at the left edge, midpoint or right edge of each slice). More rectangles = better accuracy.")
        st.success(r"**2. The Fundamental Theorem**" "\n\n" r"Integration is the inverse of differentiation. If $F'(x) = f(x)$, then $\int_a^b f(x)\,dx = F(b) - F(a)$.")
        st.warning("**3. Limits**\n\nThe definite integral is defined as the limit of the sum as $n \\to \\infty$.")

    st.divider()
    
    # AI Bridge Section
    st.markdown("### 🤖 Bridge to AI: Why Integrals Matter")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("#### 🎲 Probability Density")
        st.write("In AI, we deal with continuous probabilities. The probability of a value falling in a range $[a, b]$ is the **area** under the probability curve.")
        st.latex(r"P(a \leq X \leq b) = \int_a^b p(x) dx")
        
    with c2:
        st.markdown("#### 📏 Expectation")
        st.write("To find the 'Average' (Expected Value) of a continuous variable, we integrate the value weighted by its probability.")
        st.latex(r"E[X] = \int_{-\infty}^{\infty} x \cdot p(x) dx")
        
    with c3:
        st.markdown("#### 🌊 Information Theory")
        st.write("Entropy and KL Divergence (used to compare models) are essentially integrals measuring the 'surprise' or 'gap' between distributions.")
        st.latex(r"H(p) = -\int p(x) \log p(x)\, dx")

    st.divider()
    st.markdown(
        '<div style="color:#94a3b8;font-size:0.95rem;text-align:center;">Page 49 — You\'ve visualized the core of calculus. Next: Calculus continues with <b>Limits & Continuity (Page 79)</b> — the rigorous footing under every derivative you have taken — before Optimization puts these tools to work training AI!</div>',
        unsafe_allow_html=True,
    )
    safe_page_link("pages/79Limits & Continuity.py", "Next: 79 · Limits & Continuity", icon="➡️")

if __name__ == "__main__":
    main()
