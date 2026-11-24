import sys
from pathlib import Path

import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from common.assets import load_lab  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="Eigenvectors — Vectors That Don't Rotate", layout="wide")


def render_sandbox():
    html_code = load_lab("p61_eigenvectors")
    st.iframe(html_code, height=900)


def main():
    st.title("🔬 Page 61: Eigenvectors — Vectors That Don't Rotate")

    st.markdown(
        """
        Imagine putting on a pair of magic 3D glasses that warp the universe. 
        Most items get rotated, stretched, and twisted into completely different orientations. 
        But if you look very closely, **there are often a few special directions that never bend or rotate off their line**. 
        They remain aligned on their original track—they only get scaled: stretched, squished, flipped to point backwards (negative scale), or even collapsed to zero.
        (Some transformations, like a pure rotation, have **no** such real directions at all.)

        In linear algebra, these special, steady-state directions are called **Eigenvectors** (from the German word *eigen*, meaning "own" or "characteristic"). 
        The factor by which they stretch is their corresponding **Eigenvalue** (denoted as $\\lambda$).
        """
    )

    st.divider()

    # Layout for Sandbox
    render_sandbox()

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🧮 The Core Eigenvector Formula")
        st.info(
            "Multiplying an **eigenvector** by a matrix is equivalent to simply scaling it by a scalar."
        )
        st.markdown(
            r"""
Let $A$ be a square $n \times n$ matrix, $\mathbf{v}$ be a non-zero vector, and $\lambda$ be a scalar:

$$A\mathbf{v} = \lambda \mathbf{v}$$

Where:
* $A$ is the **transformation matrix** (warps space).
* $\mathbf{v}$ is the **eigenvector** (direction that doesn't bend).
* $\lambda$ is the **eigenvalue** (how much the eigenvector stretches or flips).

#### How to Solve:
We can rewrite the equation by introducing the identity matrix $I$:
$$A\mathbf{v} - \lambda I \mathbf{v} = \mathbf{0}$$
$$(A - \lambda I)\mathbf{v} = \mathbf{0}$$

For a non-zero solution ($\mathbf{v} \neq \mathbf{0}$), the matrix $(A - \lambda I)$ must be singular (its determinant is zero):
$$\boxed{\det(A - \lambda I) = 0}$$

For a $2 \times 2$ matrix $A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}$ this determinant is a quadratic polynomial in $\lambda$:
$$\det\begin{bmatrix} a-\lambda & b \\ c & d-\lambda \end{bmatrix} = \lambda^2 - (a+d)\lambda + (ad - bc) = 0$$

This polynomial equation is called the **characteristic equation**! With trace $T = a+d$ and determinant $D = ad-bc$:
$$\lambda_{1,2} = \frac{T \pm \sqrt{T^2 - 4D}}{2}$$

* $T^2 - 4D > 0$: two different real eigenvalues → **two** eigenvector lines (e.g. Reflection, Pure Scale).
* $T^2 - 4D = 0$: one repeated eigenvalue → either $A = \lambda I$ (**every** direction is an eigenvector, e.g. Identity) or a *defective* matrix with only **one** eigenvector line (e.g. Shear).
* $T^2 - 4D < 0$: a complex-conjugate pair $\lambda = \alpha \pm \beta i$ → **no real** eigenvector; every real direction gets turned (e.g. Rotation). The eigenvectors exist, but only with complex entries.
"""
        )

    with col2:
        st.markdown("### 📝 Concrete Worked Example")
        st.success(
            "Let's solve for the eigenvalues and eigenvectors of a simple reflection preset matrix."
        )
        st.markdown(
            r"""
Let's find the eigenvectors of the reflection matrix:
$$A = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$$

**Step 1: Formulate the Characteristic Equation**
$$A - \lambda I = \begin{bmatrix} -\lambda & 1 \\ 1 & -\lambda \end{bmatrix}$$
$$\det(A - \lambda I) = (-\lambda)(-\lambda) - (1)(1) = \lambda^2 - 1 = 0$$
$$\implies \lambda_1 = 1, \quad \lambda_2 = -1$$

**Step 2: Find the Eigenvector for $\lambda_1 = 1$**
$$(A - 1I)\mathbf{v} = 0 \implies \begin{bmatrix} -1 & 1 \\ 1 & -1 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$$
$$-x + y = 0 \implies \mathbf{v_1} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$$
*(This line lies along $y = x$. Try selecting the Reflection preset in the Sandbox and check!)*

**Step 3: Find the Eigenvector for $\lambda_2 = -1$**
$$(A - (-1)I)\mathbf{v} = 0 \implies \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$$
$$x + y = 0 \implies \mathbf{v_2} = \begin{bmatrix} -1 \\ 1 \end{bmatrix}$$
*(This line lies along $y = -x$. Stretching by $-1$ flips it backwards!)*
"""
        )

    st.divider()

    st.markdown("### 🤖 Bridge to AI: Why Eigenvectors Rule Machine Learning")
    st.markdown(
        """
        You might wonder: *“Why does a vector that doesn't rotate matter for training artificial intelligence?”* 
        Eigenvectors are the core mathematical engine driving some of the most critical algorithms in AI and Data Science.
        """
    )

    col_ai1, col_ai2, col_ai3 = st.columns(3)

    with col_ai1:
        st.markdown("#### 📉 Dimensionality Reduction (PCA)")
        st.write(
            """
            In modern machine learning, datasets are huge and high-dimensional. 
            **PCA (Principal Component Analysis)** finds the directions of maximum spread in a data cloud. 
            These directions are exactly the **eigenvectors** of the data's covariance matrix! 
            By projecting the (centered) data onto the eigenvectors with the largest eigenvalues, we can compress, say, a 784-pixel image into a few dozen numbers that keep most of its variance — or into just 2 numbers for a rough visual map (which keeps only a fraction of the information).
            """
        )

    with col_ai2:
        st.markdown("#### 🕸️ Google's PageRank & Recommenders")
        st.write(
            """
            Google originally built its search engine by modeling the internet as a giant graph. 
            A user hopping randomly from page to page represents a transition matrix $P$. 
            The steady-state distribution (which websites are visited most often) is the **eigenvector** corresponding to the largest eigenvalue ($\\lambda = 1$) of this transition matrix. 
            This represents the core backbone of spectral recommendation engines!
            """
        )

    with col_ai3:
        st.markdown("#### 🧠 Neural Network Stability")
        st.write(
            """
            When backpropagating through a deep network, the gradient is multiplied layer after layer by Jacobians (transposed weight matrices times activation slopes). 
            For a **repeated** matrix (like a simple RNN's recurrent weights), eigenvalues with $|\\lambda| > 1$ make long products blow up (**exploding gradients**) and $|\\lambda| < 1$ make them fade (**vanishing gradients**). 
            In general, though, the size of each step is governed by **singular values** (how much a matrix can stretch *any* vector), not eigenvalues — a matrix whose eigenvalues are all small can still stretch some vectors a lot. 
            That's why careful initialization (e.g. orthogonal / He / Xavier) and normalization aim to keep these stretch factors close to $1$.
            """
        )

    st.divider()
    st.markdown(
        '<div style="text-align: center; color: #94a3b8; font-size: 13px;">'
        "Page 61 — Eigenvectors let you find invariant structures in spatial transformations. "
        "Next Up: Page 62 — Eigenvalues: How Much Do They Stretch? ➔"
        "</div>",
        unsafe_allow_html=True,
    )
    prev_col, next_col = st.columns(2)
    with prev_col:
        safe_page_link("pages/89Mutual Information.py", "Previous: 89 · Mutual Information", icon="⬅️")
        safe_page_link("pages/78SVD — Rotate, Stretch, Rotate.py", "Related: 78 · SVD — Rotate, Stretch, Rotate", icon="🔗")
    with next_col:
        safe_page_link("pages/62Eigenvalues — How Much Do They Stretch.py", "Next: 62 · Eigenvalues — How Much Do They Stretch", icon="➡️")


if __name__ == "__main__":
    main()
