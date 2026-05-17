import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dot Product — Algebraic View", layout="wide")

st.title("Dot Product — Algebraic View")
st.write(
    "The dot product is the algebraic handshake between two vectors: "
    "multiply matching coordinates, then add the results. "
    "This page shows the exact step-by-step calculation and connects it back to the geometric picture."
)

st.write("---")

with st.container():
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Choose two vectors")
        a0 = st.slider("a₁ (x of vector a)", -5, 5, 2)
        a1 = st.slider("a₂ (y of vector a)", -5, 5, 1)
        b0 = st.slider("b₁ (x of vector b)", -5, 5, 1)
        b1 = st.slider("b₂ (y of vector b)", -5, 5, 2)

        a = np.array([a0, a1], dtype=float)
        b = np.array([b0, b1], dtype=float)

        st.markdown("**Vector a:**")
        st.latex(r"\mathbf{a} = \begin{pmatrix} %d \\ %d \end{pmatrix}" % (a0, a1))
        st.markdown("**Vector b:**")
        st.latex(r"\mathbf{b} = \begin{pmatrix} %d \\ %d \end{pmatrix}" % (b0, b1))

    with col2:
        st.subheader("Algebraic calculation")
        st.latex(r"\mathbf{a} \cdot \mathbf{b} = a_1 b_1 + a_2 b_2")
        st.write("Multiply each matching component, then add the results:")
        st.write(f"{a0} × {b0} + {a1} × {b1}")
        dot = a0 * b0 + a1 * b1
        st.write(f"= {a0 * b0} + {a1 * b1}")
        st.markdown(f"**Dot product = {dot}**")

        st.write("")
        st.subheader("Component-wise product")
        component_products = np.array([a0 * b0, a1 * b1])
        st.table(
            {
                "Component": ["a₁ × b₁", "a₂ × b₂"],
                "Value": component_products,
            }
        )

st.write("---")

st.subheader("Visual intuition")

col3, col4 = st.columns([1, 1])
with col3:
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.axvline(0, color="gray", linewidth=0.8)
    ax.quiver(0, 0, a[0], a[1], angles="xy", scale_units="xy", scale=1, color="tab:blue", label="a")
    ax.quiver(0, 0, b[0], b[1], angles="xy", scale_units="xy", scale=1, color="tab:orange", label="b")
    if np.linalg.norm(a) > 1e-6:
        a_hat = a / np.linalg.norm(a)
        proj_length = np.dot(b, a_hat)
        projection = proj_length * a_hat
        ax.quiver(
            0,
            0,
            projection[0],
            projection[1],
            angles="xy",
            scale_units="xy",
            scale=1,
            color="tab:green",
            alpha=0.7,
            label="projection of b onto a",
        )
        ax.plot([projection[0], b[0]], [projection[1], b[1]], color="gray", linestyle="--", alpha=0.7)
    ax.set_aspect("equal")
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.legend(loc="upper left")
    ax.set_title("Vectors and projection")
    st.pyplot(fig)

with col4:
    st.markdown(
        "The algebraic dot product gives the same answer as the geometric idea of how much of b points in the direction of a."
    )
    length_a = np.linalg.norm(a)
    length_b = np.linalg.norm(b)
    if length_a > 1e-6 and length_b > 1e-6:
        cos_theta = dot / (length_a * length_b)
        cos_theta = np.clip(cos_theta, -1.0, 1.0)
        angle_deg = np.degrees(np.arccos(cos_theta))
        st.latex(r"\mathbf{a} \cdot \mathbf{b} = \|\mathbf{a}\|\,\|\mathbf{b}\|\cos\theta")
        st.write(f"|a| = {length_a:.2f}, |b| = {length_b:.2f}")
        st.write(f"cos(θ) = {cos_theta:.2f}")
        st.write(f"θ ≈ {angle_deg:.1f}°")
    else:
        st.write("One of the vectors is zero length, so the direction-based geometric interpretation is degenerate.")

st.write("---")

st.subheader("What the numbers mean")
st.write(
    "If each matching component points in the same direction, it contributes a positive amount. "
    "If a component of one vector goes the opposite way, that direction subtracts from the total. "
    "If the dot product is zero, the vectors are perpendicular — they do not agree in any coordinate direction."
)

st.write("### Quick rules")
st.write(
    "- Positive dot product = vectors are somewhat aligned (acute angle).\n"
    "- Zero dot product = vectors are perpendicular.\n"
    "- Negative dot product = vectors point against each other (obtuse angle)."
)

st.write("---")

st.subheader("Beyond 2D")
st.write(
    "The same algebraic rule works for 3D, 4D, or any n-dimensional vector: "
    "multiply each pair of matching entries and add them all up. "
    "That is the most useful version for computers and neural networks."
)
st.latex(r"\mathbf{a} \cdot \mathbf{b} = a_1 b_1 + a_2 b_2 + \cdots + a_n b_n")
