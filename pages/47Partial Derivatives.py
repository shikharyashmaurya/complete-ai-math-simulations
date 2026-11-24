import sys
from pathlib import Path

import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.assets import load_lab  # noqa: E402

st.set_page_config(page_title="Partial Derivatives", layout="wide")

def render_lab():
    st.iframe(load_lab("p47_partial_derivatives"), height=800)


def main():
    st.title("⛰️ Page 47: Partial Derivatives")

    st.markdown(
        """
        You've mastered derivatives for functions of **one variable**. But what if your function depends on **two variables** — like altitude on a map depending on both East/West ($x$) and North/South ($y$)?

        A **partial derivative** answers: *"If I only move in the x-direction and freeze y completely, how steep is the slope?"*
        It's just a regular derivative — with a twist: **pretend all other variables are constants**.
        """
    )

    st.divider()
    st.markdown("### 1) The 3D Slicer Lab 🔪")
    st.markdown(
        "Move the **X/Y sliders** to place your point on the surface. Switch to **∂/∂x slice** to freeze y and see the 2D curve you get — that curve's slope is the partial derivative in x. Same idea for y."
    )

    render_lab()

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### The Rule: $\\frac{\\partial f}{\\partial x}$")
        st.info("**Freeze all other variables. Differentiate normally in x.**")
        st.markdown(
            r"""
**Example:** $f(x, y) = x^2 + 3xy + y^2$

$$\frac{\partial f}{\partial x}: \quad x^2 \to 2x, \quad 3xy \to 3y, \quad y^2 \to 0$$

$$\boxed{\frac{\partial f}{\partial x} = 2x + 3y}$$
"""
        )

    with col2:
        st.markdown("### The Rule: $\\frac{\\partial f}{\\partial y}$")
        st.success("**Freeze all other variables. Differentiate normally in y.**")
        st.markdown(
            r"""
**Example:** $f(x, y) = x^2 + 3xy + y^2$

$$\frac{\partial f}{\partial y}: \quad x^2 \to 0, \quad 3xy \to 3x, \quad y^2 \to 2y$$

$$\boxed{\frac{\partial f}{\partial y} = 3x + 2y}$$
"""
        )

    st.divider()
    st.markdown("### 🤖 Bridge to AI: Why This is Everything")
    st.markdown(
        """
        A neural network has **millions of weights** — each one is a variable. The Loss function is a mountain in million-dimensional space.

        To find the bottom (minimum loss), the AI needs the slope in **every single weight's direction** — independently. That's a partial derivative for each weight!

        $$\\nabla_{\\mathbf{w}} L = \\left[\\frac{\\partial L}{\\partial w_1},\\ \\frac{\\partial L}{\\partial w_2},\\ \\dots,\\ \\frac{\\partial L}{\\partial w_n}\\right]$$

        This collection of all partial derivatives is called the **Gradient** — which is exactly what Page 48 is about!
        """
    )

    st.divider()
    st.markdown(
        '<div style="color:#94a3b8;font-size:0.95rem;">Page 47 — you can now slice multivariable surfaces along each axis. Next: combine all partials into a single uphill compass — The Gradient!</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
