import sys
from pathlib import Path

import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.assets import load_lab  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="What is a Derivative?", layout="wide")

def render_derivative_lab():
    st.iframe(load_lab("p44_derivative"), height=860)


def main():
    st.title("🎢 Page 44: What is a Derivative?")
    
    st.markdown(
        """
        Calculus sounds intimidating, but it is ultimately the mathematics of **Change**. 
        
        Imagine you are driving a car. Measuring your average speed over an hour is easy: `Distance / Time`. 
        But what if you wanted to know your *exact* speed at a single, frozen microscopic instant in time? 
        If you literally let no time pass (Time = 0), no distance is traveled either (Distance = 0), and the formula gives `0 / 0` — which has no meaning.
        
        **The Derivative** sidesteps this: instead of plugging in zero time, it asks what value the ratio *approaches* as the time interval gets closer and closer to zero. That "approaches" is called a **limit**.
        """
    )
    
    st.divider()

    st.markdown("### 1) The Shrinking Interval")
    st.markdown("To find the slope at exactly one point, we start with **two** points (a secant line) and slowly shrink the distance ($h$) between them toward zero. We never actually set $h = 0$ (that would be `0 / 0`); instead we watch which value the secant slopes settle on. That limiting value is the true slope at a single point — the slope of the tangent line. Try approaching from the left too (negative $h$): you get the same limit.")
    
    render_derivative_lab()
    
    st.info(
        "**Visual Intuition:** Notice how the `Δy` (Rise) and `Δx` (Run) both vanish as $h$ approaches 0. But their *ratio* (the slope) stabilizes into a perfect number. That perfectly stable number is the **Derivative**!"
    )
    
    st.divider()
    
    st.markdown("### 2) The Magic Formula")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(
            """
            Here is the formal definition of a derivative you see in textbooks. Don't be afraid, you just animated it above!
            
            **The Formula:**
            $$ f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h} $$
            
            Let's break it down:
            * $f(x+h) - f(x)$ is just the **Rise** (Δy).
            * $h$ is just the **Run** (Δx).
            * $\\lim_{h \\to 0}$ means "the value the ratio approaches as $h$ gets arbitrarily close to 0" (from either side, without ever being exactly 0).
            """
        )
        
    with col2:
        st.markdown(
            """
            **What does the number mean?**
            * **Positive Slope (+)**: The curve is pointing uphill.
            * **Negative Slope (-)**: The curve is pointing downhill.
            * **Zero Slope (0)**: The curve is momentarily flat — often the bottom of a valley or top of a hill, but not always (e.g. $x^3$ is flat at $x = 0$ yet keeps climbing on both sides).
            """
        )
        
    st.divider()
    
    st.markdown("### 3) Bridge to AI: Why do we care?")
    st.markdown(
        """
        In Machine Learning, we want to find the lowest possible error (Loss) for our model. Imagine you are blindfolded on a bumpy mountain (the Loss Landscape) and you want to walk to the bottom valley.
        
        How do you know which way to step? You feel the ground under your feet. If the ground slopes upwards in front of you, you take a step backward. 
        
        The **Derivative** tells the AI exactly how steep the ground is, and in what direction. Without derivatives, Neural Networks would have no idea how to "learn" from their mistakes!
        """
    )
    
    st.divider()
    st.markdown(
        """
        <div style="color:#94a3b8; font-size:0.95rem;">
        Page 44 — you just unlocked Calculus. Up next: what happens when we don't have to calculate the limit every single time? Welcome to Derivative Rules!
        </div>
        """,
        unsafe_allow_html=True,
    )
    prev_col, next_col = st.columns(2)
    with prev_col:
        safe_page_link("pages/43Residuals & Least Squares.py", "Previous: 43 · Residuals & Least Squares", icon="⬅️")
    with next_col:
        safe_page_link("pages/45Derivative Rules (Power & Constant).py", "Next: 45 · Derivative Rules (Power & Constant)", icon="➡️")

if __name__ == "__main__":
    main()
