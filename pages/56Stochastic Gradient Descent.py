import sys
from pathlib import Path

import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from common.assets import load_lab  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="Stochastic Gradient Descent", layout="wide")

def render_sgd_lab():
    html_code = load_lab("p56_sgd")
    st.iframe(html_code, height=760)

def main():
    st.title("🏃 Page 56: Stochastic Gradient Descent")
    
    st.markdown("""
    In the previous pages, the ball always followed the **exact gradient** of the whole loss surface. In machine learning, that loss is an
    **average over every training example**, and real AI models are trained on **billions of images or words**.
    Calculating the exact gradient over everything at once (Full Batch) for every single step is far too slow and takes too much memory.
    
    Enter **Stochastic Gradient Descent (SGD)**: The "Drunken Walker" that saves the day.
    """)
    
    st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("The Concept")
        st.write("""
        Instead of asking every training example which way is down, we pick a **random small group** (a "Mini-batch") and average *their* answers.
        
        - **Full Batch**: Perfectly smooth, direct path. But every step is very "heavy" (uses all the data).
        - **SGD**: Noisy and jumpy, because each mini-batch gives a slightly different gradient. But every step is very "light" and fast.
        
        **Why the noise can help:** That jumpiness can sometimes shake the ball out of small, shallow local minima that trap a perfectly smooth optimizer.
        It is not a guarantee: with large batches (little noise) SGD usually gets stuck too, and too much noise keeps it from settling down.
        """)
        
    with col2:
        st.subheader("The Math 🧮")
        st.latex(r"w_{t+1} = w_t - \eta \cdot \frac{1}{N}\sum_{i=1}^{N} \nabla \ell_i(w_t)")
        st.caption("Full-batch GD averages the gradients of all N training examples.")
        
        st.latex(r"w_{t+1} = w_t - \eta \cdot \frac{1}{B}\sum_{i \in \mathcal{B}_t} \nabla \ell_i(w_t)")
        st.caption("SGD averages the gradients of a random mini-batch 𝓑ₜ of B examples. On average it points the same way as the full gradient (it is unbiased), but each estimate is noisy.")

    st.divider()
    
    st.markdown("### 🧪 The SGD Race Laboratory")
    st.info(
        "💡 The lab uses a real (synthetic) dataset of **64 training examples**, each with its own little loss surface. "
        "The map shows their average. **Click anywhere on the map** to teleport both optimizers to a new starting point. "
        "From the default start, full batch stays stuck in the dip near (−3.5, −4.2). At batch size 4, SGD shakes free roughly half the time; "
        "at 1–2 it almost always escapes, and at 8+ it usually stays stuck too. Turn on **⚖️ Equal compute** to compare progress per example processed rather than per step."
    )
    
    render_sgd_lab()
    
    st.divider()
    
    # Key takeaways
    st_cols = st.columns(3)
    with st_cols[0]:
        st.info("🚀 **Speed**")
        st.write("Each SGD step only touches a small chunk of data, so for the same compute it takes many more steps and starts learning almost immediately, without waiting for the whole dataset.")
    with st_cols[1]:
        st.warning("🎲 **Noise**")
        st.write("The noise acts like a 'shake' that can sometimes help escape poor local minima. It can be a feature, not just a bug, but too much of it keeps the optimizer jittering around the bottom.")
    with st_cols[2]:
        st.success("⚖️ **Mini-Batch**")
        st.write("Most training uses a middle ground: often 32–512 examples for vision models, and up to millions of tokens per batch for large language models, to balance stability and speed.")

    st.divider()
    st.markdown(
        '<div style="color:#94a3b8;font-size:0.95rem;">Page 56 — you\'ve seen how "shaking" the optimizer with mini-batch noise can help it find better solutions. Next: the optimization story continues with <b>Momentum (Page 90)</b> — giving the walker inertia so it rolls through noise and narrow valleys!</div>',
        unsafe_allow_html=True,
    )
    prev_col, next_col = st.columns(2)
    with prev_col:
        safe_page_link("pages/55Convex Functions.py", "Previous: 55 · Convex Functions", icon="⬅️")
    with next_col:
        safe_page_link("pages/90Momentum.py", "Next: 90 · Momentum", icon="➡️")

if __name__ == "__main__":
    main()
