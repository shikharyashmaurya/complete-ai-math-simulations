import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.assets import load_lab  # noqa: E402

st.set_page_config(page_title="Linear Functions: y = wx + b", layout="wide")

def render_threejs_interactive():
    html_code = load_lab("p20_linear_function_lab")
    st.iframe(html_code, height=620)

def render_neuron_cartoon():
    html_code = load_lab("p20_neuron_cartoon")
    st.iframe(html_code, height=260)

def main():
    st.title("📏 Page 20: Linear Functions — y = wx + b")
    st.markdown(
        """
        Meet the **affine map**: the world's politest function. It never bends — it only **tilts** and **slides**.

        - **w (weight)** is **sensitivity**: nudge **x** by a little, and **y** reacts **w times** as hard.
        - **b (bias)** is **shift**: the entire line rides up or down without changing its steepness.

        **Linear vs affine:** in linear algebra (page 14) a *linear* map must keep the origin fixed, so strictly `y = wx` is linear and `y = wx + b` (with `b ≠ 0`) is **affine** — a linear map plus a shift. In everyday ML talk both are called "linear" because the graph is a straight line.

        This affine rule is a building block for neural networks: each neuron combines weighted inputs and adds a bias. A layer applies this operation to many neurons at once, then may apply a non-linear activation.
        """
    )
    
    st.markdown("### 1) The 3D Math Engine")
    st.markdown("Interact directly with the sliders inside the 3D scene. Watch how the line morphs instantly. **Tip: Click and drag to rotate the 3D camera!**")
    
    # 3D Interactive Scene
    render_threejs_interactive()
    
    st.divider()

    st.markdown("### 2) The Anatomy of a Single Neuron")
    st.markdown("If you squint, **y = wx + b** is already a **one-weight neuron**. The story is: **input → multiply by a learned strength → add a baseline → output**.")
    
    # Animated Cartoon
    render_neuron_cartoon()
    
    st.divider()

    st.markdown("### 3) Number Lab: Table the Line")
    st.caption("Concrete rows make the 'sensitivity' idea feel less abstract.")
    
    # Keeping standard Streamlit sliders here for the dataframe interaction
    st.markdown("Use these sliders to build the table (they are separate from the sliders inside the 3D scene):")
    col1, col2 = st.columns(2)
    with col1:
        w_df = st.slider("w for table", -3.0, 3.0, 1.5, 0.1, key="p20_w")
    with col2:
        b_df = st.slider("b for table", -5.0, 5.0, -1.0, 0.1, key="p20_b")
        
    xs_show = np.round(np.linspace(-3, 3, 7), 2)
    rows = []
    for xv in xs_show:
        rows.append({
            "x": round(float(xv), 2),
            "w · x": round(float(w_df * xv), 2),
            "+ b": round(float(b_df), 2),
            "y = w·x + b": round(float(w_df * xv + b_df), 2),
        })
    
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)

    st.info(
        """
        ### Recap
        - **w** decides how **loud** the input speaks: **unit step in x ⇒ w-sized jump in y**.
        - **b** is a **universal offset**: same tilt, different altitude.
        - Psych trick for AI: **sensitivity = slope**, **shift = intercept**. 

        **Next up:** *Why non-linearity?* — the moment straight lines stop being enough to solve real problems.
        """
    )

if __name__ == "__main__":
    main()
