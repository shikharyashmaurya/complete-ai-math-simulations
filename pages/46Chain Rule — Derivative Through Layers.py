import sys
from pathlib import Path

import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.assets import load_lab  # noqa: E402

st.set_page_config(page_title="Chain Rule", layout="wide")

def render_chain_rule_lab():
    st.iframe(load_lab("p46_chain_rule"), height=800)

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
            It stretches by $3 \\times 2 = 6$ times. You simply **multiply the rates**.
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
        
        To train the network, we need to know how tweaking a single Weight at the beginning affects the final Loss at the end. We do this using an algorithm called **Backpropagation**, which is the Chain Rule applied systematically, backwards through the network. We calculate the local slope at each layer and multiply them together along the path from the Loss back to the Weight (and when a weight influences the Loss through several paths, the contributions from each path are added up).
        """
    )
    
    st.divider()
    st.markdown(
        """
        <div style="color:#94a3b8; font-size:0.95rem;">
        Page 46 — you now know how to differentiate through layers. Up next: Partial Derivatives—what happens when there are multiple inputs?
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
