import sys
from pathlib import Path

import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.assets import load_lab  # noqa: E402

st.set_page_config(page_title="The Gradient — Steepest Climb", layout="wide")

def render_lab():
    st.iframe(load_lab("p48_gradient"), height=800)

def main():
    st.title("🧭 Page 48: The Gradient — Steepest Climb")

    st.markdown("""
    On Page 47 you learned to slice a surface in **one direction at a time** — each slice giving a partial derivative.
    Now: **what if you combine ALL the partial derivatives into a single arrow?**

    That arrow is the **Gradient** — written **∇f** — and it always points in the direction of **steepest ascent**.
    Its magnitude tells you **how steep** that steepest climb is.

    $$\\nabla f(x,y) = \\left[\\frac{\\partial f}{\\partial x},\\ \\frac{\\partial f}{\\partial y}\\right]$$
    """)

    st.divider()
    st.markdown("### 🗺️ The Gradient Compass Lab")
    st.markdown(
        "Move the **X/Y sliders** (or **click the map**) to place your point. "
        "The **dashed arrows** show each partial derivative component; the **solid orange arrow** is the gradient — their vector sum. "
        "Press **⬆ Ascend** to follow +∇f uphill or **⬇ Descend** to follow −∇f downhill — the status line tells you why the climber stopped "
        "(flat point, edge of the map, or step limit). **🧗 Clean Map** hides the arrow field so the path is easier to see."
    )

    render_lab()

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔑 Key Intuitions")
        st.markdown(r"""
- **∇f is a vector**, not a number — it has both direction and magnitude
- **Direction** = steepest uphill at that point
- **Magnitude** |∇f| = how steep the steepest slope is
- At a **minimum or maximum**, ∇f = **0** (flat — nowhere to go)
- But ∇f = **0** does **not** guarantee a min or max: at a **saddle point** (try Descend on the Saddle from a point with y = 0) the gradient also vanishes
- **−∇f** points **downhill** — this is gradient descent!
        """)

    with col2:
        st.markdown("### 🧮 How It's Built")
        st.info("The gradient is just the vector of ALL partial derivatives stacked together.")
        st.markdown(r"""
**Example:** $f(x,y) = x^2 + y^2$

$$\frac{\partial f}{\partial x} = 2x, \quad \frac{\partial f}{\partial y} = 2y$$

$$\boxed{\nabla f = [2x,\ 2y]}$$

At point $(1, 2)$: $\nabla f = [2, 4]$, magnitude $= \sqrt{4+16} = \sqrt{20} \approx 4.47$
        """)

    st.divider()
    st.markdown("### 🤖 Bridge to AI: The Gradient IS the Engine")
    st.markdown(r"""
    In a neural network, the loss function $L$ depends on **millions of weights** $w_1, w_2, \dots, w_n$.

    The gradient of the loss tells the network **which direction to adjust every single weight** to reduce error the fastest:

    $$\nabla_{\mathbf{w}} L = \left[\frac{\partial L}{\partial w_1},\ \frac{\partial L}{\partial w_2},\ \dots,\ \frac{\partial L}{\partial w_n}\right]$$

    **Gradient Descent** (Page 52) simply says: *"Walk in the direction of $-\nabla L$"* — downhill on the loss landscape.

    Everything you just saw on the map — arrows pointing uphill, the climber following them — is **exactly** what happens during AI training, just in millions of dimensions!
    """)

    st.divider()
    st.markdown(
        '<div style="color:#94a3b8;font-size:.95rem;">Page 48 — The gradient assembles all partial derivatives into a single compass. Next: the area under a curve — Integrals!</div>',
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
