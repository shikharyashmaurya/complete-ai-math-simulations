import sys
from pathlib import Path

import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.assets import load_lab  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="Local vs Global Minimum", layout="wide")

def render_lab():
    st.iframe(load_lab("p54_local_global_minimum"), height=850)


def main():
    st.title("🏔️ Page 54: Local vs Global Minimum")

    st.markdown(
        """
        In an ideal convex bowl, gradient descent with a suitable step size can reach a global minimum from any starting point.

        Many AI objectives are **non-convex**, with bumps, ridges, and multiple valleys. Local minima are one possible challenge, alongside saddle points, flat regions, and unstable step sizes.
        This page shows those ideas with simplified toy surfaces.
        """
    )

    st.divider()

    col1, col2 = st.columns([1, 2.5])

    with col1:
        st.markdown("### 🕳️ Local vs. 🏆 Global")
        st.write("**Local Minimum:** A point that is lower than all its immediate neighbors, but not the lowest point in the entire landscape.")
        st.write("**Global Minimum:** The absolute lowest point possible. This is where we want our AI to end up.")

        st.info("**The Starting Point Matters!** Depending on where you initialize your weights (the ball), you might get trapped in a local dip forever.")

        st.markdown("### How to escape?")
        st.write("1. **Higher Learning Rate:** Can sometimes jump over small bumps, but here it more often just bounces back and forth or diverges. Try η ≥ 0.2 and watch the Outcome badge.")
        st.write("2. **Momentum:** Like a real ball, it uses speed to roll uphill briefly. (Not in this lab; try the Momentum slider on the Stochastic Gradient Descent page.)")
        st.write("3. **Better Initialization:** Start closer to the 'right' valley. On 'The Secret', the deep well is narrow, so only nearby starts find it.")

    with col2:
        render_lab()

    st.divider()

    st.markdown("### 🧠 The Conceptual Breakdown")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 1. Optimization is Greedy")
        st.write("Gradient Descent only looks at the **immediate slope**. It's like walking in a fog; you only see the next step. Wherever the ground is flat (zero gradient), it stops, whether that's a local minimum or a saddle point, even if a deeper valley is just one hill away. On nearly flat plateaus it slows to a crawl.")

    with c2:
        st.markdown("#### 2. Saddle Points")
        st.write("In many high-dimensional neural-network settings, **Saddle Points** and flat regions can matter more during optimization than poor local minima. A saddle is a point that is a minimum in some directions and a maximum in others.")

    with c3:
        st.markdown("#### 3. Why convexity is a luxury")
        st.write("Ordinary least-squares linear regression has a convex objective, so every local minimum is global (though the solution need not be unique). Neural-network objectives are generally non-convex.")

    st.divider()
    st.markdown(
        '<div style="color:#94a3b8;font-size:0.95rem;">Page 54 — you\'ve seen the traps of the landscape. Next: <b>Convex Functions (Page 55)</b> — the one shape of landscape with no traps at all, and how to recognize it!</div>',
        unsafe_allow_html=True,
    )
    safe_page_link("pages/55Convex Functions.py", "Next: 55 · Convex Functions", icon="➡️")


if __name__ == "__main__":
    main()
