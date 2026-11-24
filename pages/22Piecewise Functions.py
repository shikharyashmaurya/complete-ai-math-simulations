import streamlit as st
import sys
from pathlib import Path

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.assets import load_lab  # noqa: E402

st.set_page_config(page_title="Piecewise Functions", layout="wide")

def render_stitch_lab():
    html_code = load_lab("p22_stitch_lab")
    st.iframe(html_code, height=770)

def render_relu_visualizer():
    html_code = load_lab("p22_relu_visualizer")
    st.iframe(html_code, height=450)

def render_xor_piecewise_lab():
    html_code = load_lab("p22_xor_piecewise_lab")
    st.iframe(html_code, height=680)

def main():
    st.title("🧩 Page 22: Piecewise Functions — Patchwork Lines")
    st.markdown(
        """
        Until now, one formula ruled the whole **x**-axis. **Piecewise** means: *different linear recipes on different strips*,
        then **sew** them together at **breakpoints** (the **gates** or **kinks**). Neural nets adore this trick.
        
        Deep Learning is built on piecewise functions. By combining many small linear pieces, a ReLU network can approximate any
        *continuous* function on a bounded input range as closely as you like — given enough pieces (the *universal approximation* idea).
        """
    )

    st.markdown("### 1) The Stitch Lab")
    st.markdown("Imagine a highway with **three toll zones**. Same vehicle (**x**), but the **pricing rule** changes when you cross a gate. Drag the sliders inside the 3D lab to build a continuous curve from three separate lines. **Tip: Left click and drag to rotate the 3D view.**")
    
    render_stitch_lab()
    
    st.info(
        "**Continuity cheat-code:** The graph is continuous when the jump at a gate reads `0.00` (green). The jump is signed: "
        "**right piece minus left piece**, so `+` means the curve steps *up* as you cross the gate and `−` means it steps *down*. "
        "Stuck? Press **Snap continuous** — it solves $b_2 = (m_1 - m_2)\\,a + b_1$ and $b_3 = (m_2 - m_3)\\,b + b_2$ for you. "
        "If you align all the pieces without any jumps, you've created a **CPWL (Continuous Piecewise Linear)** curve — the native language of ReLU networks."
    )
    
    st.divider()
    
    st.markdown("### 2) ReLU & The Star Lineup")
    st.markdown("**ReLU (Rectified Linear Unit)** is the celebrity of piecewise functions because it is incredibly cheap to compute, produces sparse activations (many exact zeros), and is easy to reason about piece-by-piece.")
    
    render_relu_visualizer()
    
    st.success(
        "**Headline:** Piecewise functions are how we let a model stay **mostly linear locally** while acting **wildly non-linear globally** — ReLU is the simplest nontrivial stitch you can hide inside a giant net."
    )
    
    st.divider()
    
    st.markdown("### 3) Beating the Straight-Line Trap (Solving XOR)")
    st.markdown("On the last page, a single straight line failed to separate the XOR points. Here is how **piecewise functions** solve it. We combine two ReLU slices whose kinks sit on two parallel lines; subtracting the second slice folds the output back down, so the positive region becomes a **band** that traps the blue points in the middle while both pink corners fall outside it. (With the auto-solved weights the margins are small, ±0.1 at the pink corners — try nudging `c`.)")
    
    render_xor_piecewise_lab()

    st.divider()
    st.markdown(
        """
        <div style="color:#94a3b8; font-size:0.95rem;">
        Page 22 — you can “sew” sophisticated behavior from humble lines. Next up in your curriculum: probability starts treating inputs as <b>random</b>
        instead of <b>deterministic</b> — new flavor, same love for structure.
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
