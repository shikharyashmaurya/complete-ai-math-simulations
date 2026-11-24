import sys
from pathlib import Path

import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from common.assets import load_lab  # noqa: E402

st.set_page_config(page_title="Eigenvalues — How Much Do They Stretch?", layout="wide")


def render_stretch_lab():
    html_code = load_lab("p62_eigenvalues")
    st.iframe(html_code, height=920)


def main():
    st.title("📏 Page 62: Eigenvalues — How Much Do They Stretch?")

    st.markdown(
        """
        On the previous page you met **eigenvectors** — special directions that don't rotate when a matrix hits them.
        The companion number sitting next to each one is the **eigenvalue** $\\lambda$ (lambda).

        It answers one clean question: *along this direction, how much does the matrix stretch, squash, or flip the arrow?*

        $$\\mathbf{A}\\mathbf{v} = \\lambda \\mathbf{v}$$

        - $\\lambda > 1$ → the vector **grows**
        - $0 < \\lambda < 1$ → it **shrinks** toward the origin
        - $\\lambda = 1$ → same length, same direction
        - $\\lambda < 0$ → it **flips** to the opposite side *and* scales by $|\\lambda|$ (so $\\lambda = -1.8$ flips **and** grows)
        - $\\lambda = 0$ → the direction **collapses** to zero

        In short: the **sign** of $\\lambda$ says whether the direction is kept or flipped; the **size** $|\\lambda|$ says whether it grows ($|\\lambda| > 1$) or shrinks ($|\\lambda| < 1$).
        """
    )

    st.divider()
    render_stretch_lab()
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔢 Reading λ at a Glance")
        st.info("The eigenvalue is a **scalar stretch factor** along an eigenvector direction — nothing more mysterious than that.")
        st.markdown(
            r"""
| Condition | What happens to $\mathbf{v}$ | Real-world vibe |
|-----------|-------------------------------|-------------------|
| $\lambda > 1$ | Stretches outward | Amplifier 🔊 |
| $\lambda = 1$ | Unchanged | Identity pass-through |
| $0 < \lambda < 1$ | Shrinks inward | Dampener 🔇 |
| $\lambda < 0$ | Flips + scales by $\lvert\lambda\rvert$ | Mirror + zoom 🪞 |
| $\lambda = 0$ | Collapses to $\mathbf{0}$ | Information destroyed |

**Key ratio:** when $\mathbf{v}$ points along an eigenvector,
$$\frac{\|\mathbf{A}\mathbf{v}\|}{\|\mathbf{v}\|} = |\lambda|$$

The sign of $\lambda$ tells you whether the output points the same way ($+$) or backward ($-$).
"""
        )

    with col2:
        st.markdown("### 🧮 Computing λ for a 2×2 Matrix")
        st.success("Same characteristic equation from Page 61 — now we care about the roots $\\lambda_1, \\lambda_2$.")
        st.markdown(
            r"""
For $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}$:

$$\det(A - \lambda I) = 0 \implies \lambda^2 - (a+d)\lambda + (ad-bc) = 0$$

**Example — diagonal stretch matrix:**
$$A = \begin{bmatrix} 2 & 0 \\ 0 & 0.5 \end{bmatrix}$$

Eigenvalues: $\lambda_1 = 2$, $\lambda_2 = 0.5$ (read straight off the diagonal!)

- Horizontal arrows grow **2×**
- Vertical arrows shrink to **half**

Try **2D Matrix View** in the lab — drag $\lambda_1$ and $\lambda_2$ sliders and watch the unit circle become an axis-aligned ellipse whose **semi-axes** (half-width and half-height) are exactly $|\lambda_1|$ and $|\lambda_2|$.
"""
        )

    st.divider()

    st.markdown("### 🎬 Three Scenarios to Try in the Lab")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 🟢 λ = 2 (Grow)")
        st.write("Set λ = 2 in **1D λ Slider** mode. Align the yellow arrow with the green eigen-direction. Notice ‖Av‖ ≈ **twice** ‖v‖ (exactly 2× when v lies exactly on the axis).")
    with c2:
        st.markdown("#### 🟣 λ = 0.4 (Shrink)")
        st.write("Pick the shrink preset and align v with the green axis. The pink output arrow is only 40% as long — the transformation is **squeezing** that direction.")
    with c3:
        st.markdown("#### 🔴 λ = −1.8 (Flip + Grow)")
        st.write("Negative λ sends Av to the **opposite side** of the origin while stretching it. This is how reflection matrices get eigenvalue −1.")

    st.divider()

    st.markdown("### 🤖 Bridge to AI: Why λ Sizes Matter")
    a1, a2, a3 = st.columns(3)
    with a1:
        st.markdown("#### 📉 PCA — Keep the Big λ Directions")
        st.write(
            "PCA ranks eigenvectors of the (centered) covariance matrix by their eigenvalues (variance). "
            "Large λ = lots of spread = usually worth keeping. "
            "Dropping tiny-λ directions loses little variance, so it's a good compression trade-off — "
            "but low variance doesn't automatically mean noise: a small direction can still matter for a "
            "prediction task, and feature scaling changes which directions look big."
        )
    with a2:
        st.markdown("#### 🧠 Gradient Stability")
        st.write(
            "Backprop multiplies one Jacobian per layer. "
            "For the **same** matrix applied over and over (e.g. an RNN's recurrent weights), "
            "eigenvalues with |λ| > 1 make the product **explode** and |λ| < 1 make it **vanish**. "
            "For a general stack of different layers, the stretch per step is set by **singular values**, "
            "not eigenvalues — a matrix with all eigenvalues below 1 can still stretch some vectors a lot. "
            "Good initialization (orthogonal, He, Xavier) keeps those stretch factors near 1."
        )
    with a3:
        st.markdown("#### 🕸️ PageRank's Dominant λ")
        st.write(
            "The web-surfer matrix has a largest eigenvalue λ₁ = 1. "
            "Its eigenvector is the steady-state visit distribution — "
            "the ranking score Google famously used."
        )

    st.divider()
    st.markdown(
        '<div style="text-align:center;color:#94a3b8;font-size:13px;">'
        "Page 62 — eigenvalues tell you *how much* each special direction stretches. "
        "Next Up: Page 63 — PCA Intuition: Finding the Best Angle ➔"
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
