import sys
from pathlib import Path

import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.assets import load_lab  # noqa: E402

st.set_page_config(page_title="Gradient Descent — Walking Downhill", layout="wide")

def render_gd_lab():
    st.iframe(load_lab("p52_gradient_descent"), height=640)

def main():
    st.markdown("""
        <style>
            .p52-header {
                background: linear-gradient(90deg, #38bdf8, #10b981);
                -webkit-background-clip: text;
                background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 3.2rem;
                font-weight: 900;
                margin-bottom: 0;
            }
            .p52-subheader {
                font-size: 1.2rem;
                color: #94a3b8;
                margin-bottom: 1.5rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="p52-header">Gradient Descent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="p52-subheader">Optimization: The Engine of Machine Learning</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5])

    with col1:
        with st.container(border=True):
            st.markdown("### 🧭 The Negative Compass")
            st.markdown(
                r"On Page 48, you saw the Gradient ($\nabla f$) — it points directly **uphill**."
            )
            st.markdown(
                r"**Gradient Descent** walks along the :green[**Negative**] of the gradient ($-\nabla f$), the steepest-downhill direction. "
                r"With a small enough step size, each step is guaranteed to lower the loss "
                r"(here $\eta = 0.15$ is small enough for both terrains), but it only leads to *a* nearby dip, not necessarily the deepest one."
            )

        with st.container(border=True):
            st.markdown("### 📐 The Descent Step")
            st.markdown("Every training iteration, we update the weights:")
            st.latex(r"\mathbf{w}_{next} = \mathbf{w}_{old} - \eta \cdot \nabla f")
            st.markdown(r"Where $\eta$ is the **Learning Rate** — your stride length.")
        
        st.info("💡 **Interactive:** Click anywhere on the **Topographic Map** to teleport the ball to a new starting position. On the **Convex Bowl** it always reaches the deepest blue; on **Lumpy Terrain** it often stops in whichever dip is closest.")

    with col2:
        render_gd_lab()

    st.divider()

    # Deep Dive
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("### 🏹 Vector Components")
        st.markdown(r"""
        The gradient is a vector made of the two partial derivatives, $\nabla f = [\partial f/\partial w_1,\ \partial f/\partial w_2]$ (see the readout in the lab).
        - :orange[**Orange dashed line**]: the gradient $\nabla f$, the combined steepest *uphill* direction.
        - :green[**Green arrow**]: $-\nabla f$, the direction of the next descent step.
        - **White contour lines**: points with equal loss; the gradient always crosses them at a right angle.
        """)
        
    with c2:
        st.markdown("### 👟 Fixed Learning Rate η")
        st.markdown("""
        For now, we use a fixed learning rate of **0.15**.
        
        This determines how "big" our steps are. If it's too large, we might skip over the valley; if it's too small, we'll crawl forever.
        """)
        
    with c3:
        st.markdown("### 🕳️ Local Minima")
        st.markdown("""
        Switch to **Lumpy Terrain**. From the default start the ball settles in a shallow dip, not the deepest one (the toast tells you which).
        In real, very high-dimensional models, saddle points and flat regions are often a bigger obstacle than bad local minima.
        """)

    st.divider()
    st.markdown("### 🤖 Bridge to AI: Training in Millions of Dimensions")
    st.markdown("""
    While we visualize **2 weights** here, a real Transformer model has **billions**. 
    The core math is the same:
    1. Calculate the **partial derivative** for every single weight (via backpropagation).
    2. Combine them into one massive **gradient vector**.
    3. Take a tiny step **downhill**.
    
    Modern models such as ChatGPT are trained with refined versions of this walk-downhill idea: gradients estimated on mini-batches of data (Page 56) and optimizers like Adam (Page 91).
    """)

    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #64748b; font-size: 0.8rem;">Page 52 — Gradient Descent. Next: <b>Learning Rate — Step Size Matters</b></div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
