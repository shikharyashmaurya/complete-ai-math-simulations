import sys
from pathlib import Path

import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from common.assets import load_lab  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="PCA Intuition — Finding the Best Angle", layout="wide")


def render_pca_lab():
    html_code = load_lab("p63_pca")
    st.iframe(html_code, height="content")


def main():
    st.title("📐 Page 63: PCA Intuition — Finding the Best Angle")

    st.markdown(
        """
        You have a **cloud of data points** in 2D — maybe two features per student, or two pixels near each other.
        PCA (Principal Component Analysis) asks a beautifully simple question:

        > *If I can only look along **one line** through the cloud, which angle shows the most spread — and which angle shows the least?*

        The direction of **maximum spread** is **PC1** (first principal component).
        The perpendicular direction is **PC2** — where the cloud is thinnest.

        That's it. No magic. You're just **rotating a ruler** until the data looks as wide as possible, then **squashing** everything onto that ruler for compression.
        """
    )

    st.divider()
    st.markdown("### 1) The PCA Angle Finder Lab 🔄")
    st.markdown(
        "Use **Sweep Angle** to rotate an axis and watch the spread meter rise and fall — the ruler starts 60° away from the best angle, so you have to hunt for the peak. "
        "Hit **Snap to Best Angle** when you're close — or switch to **True PCA Axes** to see the eigen-directions from the covariance matrix. "
        "Then try **Squash to 1D** and watch the cloud collapse onto PC1 (the lab reports how much variance is lost). "
        "**🎲 New random sample** draws a fresh cloud of the same shape."
    )
    render_pca_lab()
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📏 Spread = Variance Along a Line")
        st.info("Center the data, pick a unit direction $\\mathbf{u}$, project every point, measure spread.")
        st.markdown(
            r"""
For centered points $\mathbf{x}_i$ and unit axis $\mathbf{u} = (\cos\theta,\ \sin\theta)$:

$$\text{proj}_i = \mathbf{x}_i \cdot \mathbf{u}$$

$$\text{Var along } \mathbf{u} = \frac{1}{n-1}\sum_i (\mathbf{x}_i \cdot \mathbf{u})^2$$

Rotate $\theta$ from $0°$ to $180°$ — the curve in the lab is this function.
It **peaks** at PC1 and **bottoms out** at PC2 (perpendicular).
"""
        )

    with col2:
        st.markdown("### 🔗 Link to Eigenvalues (Pages 61–62)")
        st.success("PCA directions are eigenvectors of the **covariance matrix**. Eigenvalues = variance along those directions.")
        st.markdown(
            r"""
Covariance matrix of centered data:

$$\mathbf{C} = \frac{1}{n-1}\mathbf{X}^T\mathbf{X}$$

Solve $\mathbf{C}\mathbf{v} = \lambda \mathbf{v}$:

| Component | Meaning |
|-----------|---------|
| $\mathbf{v}_1$ (largest $\lambda_1$) | **PC1** — max spread |
| $\mathbf{v}_2$ (smallest $\lambda_2$) | **PC2** — min spread |

**% explained by PC1** $= \dfrac{\lambda_1}{\lambda_1 + \lambda_2}$ (in 2D; generalizes in higher dimensions)

**What squashing costs:** projecting onto PC1 throws away the PC2 coordinate, so the lost variance is exactly $\lambda_2$.
The mean squared reconstruction error is $\frac{1}{n}\sum_i (\mathbf{x}_i \cdot \mathbf{v}_2)^2 = \frac{n-1}{n}\lambda_2$ — shown live in the lab.
"""
        )

    st.divider()

    st.markdown("### 🎬 Three Things to Try")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 🔄 Auto-Sweep")
        st.write(
            "Press **Auto-Sweep** and watch the yellow dot ride the variance curve. "
            "The sweep only needs 0°–180°: a line at θ and at θ+180° is the same line, "
            "so a full 360° turn would just show the same PC1 peak twice."
        )
    with c2:
        st.markdown("#### ⭕ Round Cloud")
        st.write(
            "Switch to **Round Cloud**. The *true* spread is equal in every direction, "
            "but with only 90 random points the measured spread still varies — typically the best angle has "
            "about 1.3× the spread of the worst (sometimes 1.7×). That 'winner' is pure sampling noise: "
            "press **🎲 New random sample** and PC1 jumps to a completely different angle. "
            "PCA still runs, but squashing to 1D throws away almost half the variance."
        )
    with c3:
        st.markdown("#### 🗜️ Squash")
        st.write(
            "In **Squash to 1D**, points slide onto PC1. "
            "You keep most information when the cloud is elongated; you lose the thin direction (PC2)."
        )

    st.divider()

    st.markdown("### 🤖 Bridge to AI: Why PCA Matters")
    a1, a2, a3 = st.columns(3)
    with a1:
        st.markdown("#### 🖼️ Dimension Reduction")
        st.write(
            "A 28×28 image is 784 dimensions. "
            "PCA finds a smaller set of directions that capture most variance — "
            "compress before clustering or visualization."
        )
    with a2:
        st.markdown("#### 🧬 Feature Decorrelation")
        st.write(
            "Correlated inputs confuse some models. "
            "PCA produces uncorrelated components: in the PC coordinates the covariance matrix is diagonal "
            "(uncorrelated is weaker than independent — PCA only removes linear correlation), "
            "often making downstream learning easier."
        )
    with a3:
        st.markdown("#### 🧠 Beyond Classical PCA")
        st.write(
            "Autoencoders learn nonlinear versions of the same idea: "
            "find a compressed representation, then reconstruct. "
            "PCA is the linear ancestor of that whole family."
        )

    st.divider()
    st.markdown(
        '<div style="text-align:center;color:#94a3b8;font-size:13px;">'
        "Page 63 — you can now find the best angle through a point cloud and squash it to 1D. "
        "Next Up: Page 64 — A Single Neuron: weights, bias, and the dot product made biological ➔"
        "</div>",
        unsafe_allow_html=True,
    )
    rel_col, next_col = st.columns(2)
    with rel_col:
        safe_page_link("pages/78SVD — Rotate, Stretch, Rotate.py", "Related: 78 · SVD — how PCA is computed in practice", icon="🔗")
    with next_col:
        safe_page_link("pages/64A Single Neuron.py", "Next: 64 · A Single Neuron", icon="➡️")


if __name__ == "__main__":
    main()
