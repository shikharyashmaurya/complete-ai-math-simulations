import sys
from pathlib import Path

import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.assets import load_lab  # noqa: E402

st.set_page_config(page_title="Derivative Rules", layout="wide")

def render_derivative_rules_lab():
    st.iframe(load_lab("p45_derivative_rules"), height=800)


def main():
    st.title("🧮 Page 45: Derivative Rules (Power & Constant)")
    
    st.markdown(
        """
        Calculating the derivative using the limit definition (shrinking $h$ to zero) every single time would be exhausting. 
        Fortunately, mathematicians noticed **patterns**. 
        
        By spotting these patterns, we created "shortcut rules" to find derivatives instantly. Let's build the intuition for the two most fundamental rules: the **Constant Rule** and the **Power Rule**.
        """
    )
    
    st.divider()

    st.markdown("### 1) The Discovery Lab 🔬")
    st.markdown("Play with the simulator below. Your goal is to see how the slope (tangent line) of the original function maps exactly to the height of the derivative function.")
    
    render_derivative_rules_lab()
    
    st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### The Constant Rule")
        st.info("**Rule:** If $f(x) = C$, then $f'(x) = 0$")
        st.markdown(
            """
            **The Intuition:**
            A constant function is just a flat, horizontal line. If you are walking on flat ground, you are neither going up nor down. 
            
            Your slope (rate of change) is exactly **zero** everywhere. 
            
            * **Example:** $f(x) = 5 \\implies f'(x) = 0$
            """
        )
        
    with col2:
        st.markdown("### The Power Rule")
        st.success("**Rule:** If $f(x) = x^n$, then $f'(x) = n \\cdot x^{n-1}$")
        st.markdown(
            """
            **The Intuition:**
            When you traced the Quadratic $f(x) = 0.5x^2 - 2$, the painted slope was the straight line $f'(x) = x$.
            When you traced the Cubic $f(x) = 0.1x^3$, the painted slope was the parabola $f'(x) = 0.3x^2$.
            
            **The Pattern:** You bring the exponent down to the front, and subtract 1 from the exponent.
            
            * **Example:** $f(x) = x^3 \\implies f'(x) = 3x^2$
            * **Example:** $f(x) = x^{10} \\implies f'(x) = 10x^9$
            """
        )
        
    st.markdown("### 🧩 Two Helper Rules (used in the lab)")
    st.markdown(
        """
        The lab's functions have coefficients and added constants, so two more shortcuts are at work:
        
        * **Constant Multiple Rule:** $(c \\cdot f)' = c \\cdot f'$. So $(0.5x^2)' = 0.5 \\cdot 2x = x$ and $(0.1x^3)' = 0.1 \\cdot 3x^2 = 0.3x^2$.
        * **Sum Rule:** $(f + g)' = f' + g'$. So $(0.5x^2 - 2)' = x + 0 = x$ — the $-2$ only shifts the curve up/down and disappears (Constant Rule).
        * **Linear:** $(1.5x)' = 1.5 \\cdot 1 \\cdot x^0 = 1.5$ — a constant slope, which is why the painted line is flat.
        """
    )
        
    st.divider()
    
    st.markdown("### 🤖 Bridge to AI: Why does this matter?")
    st.markdown(
        """
        When you train a Neural Network, you define a **Loss Function** (which measures how wrong the AI is) and you want to find the minimum of that function.
        
        Most Loss Functions (like Mean Squared Error) use powers, e.g., $Loss = (Prediction - Reality)^2$. 
        
        To minimize it, the AI needs to find the derivative. Thanks to the **Power Rule**, the computer doesn't need to calculate infinite limits! It just uses the shortcut $2 \\times (Prediction - Reality)$ — the slope of the loss with respect to the *prediction* — and instantly knows which direction is downhill. (Carrying that slope back to the model's weights needs one more tool: the Chain Rule, next page.) **Calculus rules are the engine that makes AI fast.**
        """
    )
    
    st.divider()
    st.markdown(
        """
        <div style="color:#94a3b8; font-size:0.95rem;">
        Page 45 — you now know the shortcuts. But what happens when we stack functions inside each other? That's the core of Deep Learning. Up next: The Chain Rule!
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
