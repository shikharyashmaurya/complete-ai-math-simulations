import sys
from pathlib import Path

import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.assets import load_lab  # noqa: E402

st.set_page_config(page_title="Learning Rate — Step Size Matters", layout="wide")

def render_lr_lab():
    st.iframe(load_lab("p53_learning_rate"), height=700)

def main():
    st.markdown("""
        <style>
            .p53-header {
                background: linear-gradient(90deg, #f472b6, #fb923c);
                -webkit-background-clip: text;
                background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 3.2rem;
                font-weight: 900;
                margin-bottom: 0;
            }
            .p53-subheader {
                font-size: 1.2rem;
                color: #94a3b8;
                margin-bottom: 2rem;
            }
            .p53-tag {
                padding: 4px 10px;
                border-radius: 6px;
                font-size: 0.8rem;
                font-weight: 800;
                text-transform: uppercase;
                margin-bottom: 10px;
                display: inline-block;
            }
            .p53-tag-small { background: rgba(56, 189, 248, 0.15); color: #38bdf8; }
            .p53-tag-good { background: rgba(16, 185, 129, 0.15); color: #10b981; }
            .p53-tag-huge { background: rgba(244, 114, 182, 0.15); color: #f472b6; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="p53-header">Learning Rate</h1>', unsafe_allow_html=True)
    st.markdown('<p class="p53-subheader">Optimization #53: Finding the Perfect Stride</p>', unsafe_allow_html=True)

    st.markdown("""
    In Gradient Descent, the **Gradient** tells us which direction is downhill. But it doesn't tell us **how far** to walk. 
    That stride length is the **Learning Rate (η)**.
    """)

    render_lr_lab()

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown('<span class="p53-tag p53-tag-small">η = 0.02 (Small)</span>', unsafe_allow_html=True)
            st.markdown("### 🐌 The Slug")
            st.write("Safe but slow: each step only removes 4% of the distance to the bottom, so it needs about 220 steps here (vs. about 25 for η = 0.15). In real AI, a learning rate that is too small wastes hours or days of compute.")

    with col2:
        with st.container(border=True):
            st.markdown('<span class="p53-tag p53-tag-good">η = 0.15 (Good)</span>', unsafe_allow_html=True)
            st.markdown("### ✅ The Athlete")
            st.write("A safe, solid choice: large enough steps to move quickly, small enough to settle into the minimum without bouncing. "
                     "For this exact parabola the fastest choice is η = 0.5 (🎯 ONE JUMP), but real loss surfaces are not perfect parabolas, so practitioners usually stay safely below the limit.")

    with col3:
        with st.container(border=True):
            st.markdown('<span class="p53-tag p53-tag-huge">η = 1.05 (Huge)</span>', unsafe_allow_html=True)
            st.markdown("### 💥 The Chaos")
            st.write("Overconfident. The steps are so large that the ball overshoots the valley, landing higher on the other side. This leads to **Divergence**. "
                     "Between η = 0.5 and 1 (🏓 BOUNCY) it still converges, but zig-zags across the valley; at exactly η = 1 it bounces forever.")

    st.divider()

    st.markdown("### 🤖 Bridge to AI: Why Experts Hate Static Rates")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(r"""
        Finding the perfect learning rate is so hard that modern AI models don't just pick one number. They use **Schedules** and **Optimizers**:
        
        1. **LR Schedulers**: Usually a short warm-up, then larger steps early on, then gradually smaller steps (lower η) as training gets close to the bottom, to "fine-tune."
        2. **Adaptive Optimizers (Adam)**: Every single weight gets its own effective step size. Adam keeps running averages of each weight's recent gradients and squared gradients, and divides the step by the typical gradient size, so weights with consistently large or noisy gradients take smaller steps.
        
        **The Math:**
        For the bowl in the lab, $f(x) = x^2$, each update is $x_{new} = x - \eta \cdot 2x = (1 - 2\eta)\,x$.
        It shrinks toward 0 only if $|1 - 2\eta| < 1$, i.e. $\eta < \frac{2}{\lambda}$ with curvature $\lambda = f''(x) = 2$, so $\eta < 1$. That's why CHAOS (1.05) explodes.
        For a general loss near a minimum, $\lambda_{max}$ is the largest eigenvalue of the Hessian (the steepest curvature), and $\eta < \frac{2}{\lambda_{max}}$ is a *local* stability rule. It is exact only for quadratic bowls.
        Above that limit, updates can actually increase the loss. Since $\lambda_{max}$ is expensive to compute for big models, we experiment!
        """)
    
    with c2:
        st.success("💡 **Pro Tip:** If your loss is NaN or infinity during training, your Learning Rate is likely too high! Try dividing it by 10.")

    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #64748b; font-size: 0.8rem;">Page 53 — Learning Rate. Next: <b>Local vs Global Minimum — Getting Stuck</b></div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
