import sys
from pathlib import Path

import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.assets import load_lab  # noqa: E402

st.set_page_config(page_title="Loss Landscape — Hills and Valleys", layout="wide")

def render_3d_landscape():
    st.iframe(load_lab("p51_loss_landscape"), height=700)

def main():
    # Hero Section
    st.markdown("""
        <style>
            .p51-header {
                background: linear-gradient(90deg, #38bdf8, #818cf8);
                -webkit-background-clip: text;
                background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 3rem;
                font-weight: 800;
                margin-bottom: 0;
            }
            .p51-subheader {
                font-size: 1.2rem;
                color: #94a3b8;
                margin-bottom: 2rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="p51-header">Loss Landscape</h1>', unsafe_allow_html=True)
    st.markdown('<p class="p51-subheader">The Topography of Intelligence</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2.5])

    with col1:
        st.markdown("""
        ### What is this?
        In AI, we don't just "calculate" the answer. We **search** for it.
        
        Imagine every possible setting of two model parameters ($w_1, w_2$) as a coordinate on a map. For each coordinate, this toy example assigns an objective value (a loss need not be identical to raw prediction error).
        
        - **Peaks (Red)**: High error. The model is guessing wildly.
        - **Valleys (Blue)**: Low error. The model is getting closer to the truth.
        
        ### The Goal
        Training an AI is like being a hiker lost in a foggy mountain range at night. You can't see the bottom, but you can feel the **slope** under your feet.
        """)
        
        st.info("💡 **Try it:** Switch to 'Complex' to explore a non-convex toy objective with multiple dips (the same 'Lumpy Terrain' you'll walk down on Page 52). Non-convexity alone does not mean training must get trapped; real high-dimensional optimization can also be affected by saddle points and flat regions.")

    with col2:
        render_3d_landscape()

    st.divider()

    # Educational Sections
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("### 🏹 The Global Minimum")
        st.markdown("""
        This is the lowest objective value on the entire landscape. Reaching it minimizes this specified objective; it does not necessarily give unique weights or guarantee the best generalization.
        """)
        
    with c2:
        st.markdown("### 🕳️ Local Minima")
        st.markdown("""
        A non-convex objective can contain several valleys, and an optimizer may settle in a local one. In high dimensions, saddle points and flat regions can also affect optimization.
        """)
        
    with c3:
        st.markdown("### 🎢 Curvature")
        st.markdown("""
        Some valleys are narrow (steep walls), others are broad. Steep walls mean small changes in weights cause huge changes in loss. Flat regions mean the AI might wander aimlessly.
        """)

    st.divider()

    # Bridge to AI
    st.markdown("### 🤖 Bridge to AI: From 3D to Million-D")
    
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.markdown("""
        This visualization uses only **2 parameters** ($w_1$ and $w_2$), so we can see its objective surface in 3D. The vertical offset is arbitrary; only differences in objective value affect the shape.
        
        But modern large language models have **billions — often hundreds of billions —** of weights. Their "landscape" lives in a space with billions of dimensions!
        """)
        
    with col_b:
        st.warning("⚠️ **Reality Check**: We can't actually 'see' a billion-dimensional surface. Gradients give the local direction of steepest increase (so gradient descent steps in the opposite direction); they do not guarantee a global minimum.")

    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #64748b; font-size: 0.8rem;">Page 51 — Understanding the terrain is the first step. Next: <b>Gradient Descent — Walking Downhill</b></div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
