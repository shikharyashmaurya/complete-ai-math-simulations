import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Scalar Multiplication", layout="wide")

st.title("Scalar Multiplication: Stretch, Shrink, Flip")
st.markdown(
    """
    Scalar multiplication is how we make a vector longer, shorter, or reverse its direction.
    Multiply every component of a vector by the same number, and the arrow always stays on the same line
    through the origin: a positive number keeps its direction, a negative number reverses it, and zero collapses it to the origin.
    """
)

st.write("## Play with the scalar and the base vector")

col1, col2 = st.columns([1, 1])
with col1:
    k = st.slider("Scalar k", -3.0, 3.0, 1.0, 0.1, key="p03_k")
    vx = st.slider("Vector x component", -4, 4, 2, key="p03_vx")
    vy = st.slider("Vector y component", -4, 4, 1, key="p03_vy")

with col2:
    st.markdown("**What happens when you change k?**")
    st.markdown(
        "- If `k > 1`, the arrow stretches away from the origin.\n"
        "- If `k == 1`, nothing changes.\n"
        "- If `0 < k < 1`, the arrow shrinks toward the origin.\n"
        "- If `k == 0`, the vector collapses to the origin.\n"
        "- If `k < 0`, the arrow flips and points in the opposite direction "
        "(it also stretches if `k < -1` and shrinks if `-1 < k < 0`)."
    )

v = np.array([vx, vy], dtype=float)
v_scaled = k * v

fig, ax = plt.subplots(figsize=(5, 5))
ax.axhline(0, color="#999999", linewidth=1)
ax.axvline(0, color="#999999", linewidth=1)
# Draw k·v first and v on top (thinner), so v stays visible when k = 1 and the two arrows coincide
ax.quiver(0, 0, v_scaled[0], v_scaled[1], angles='xy', scale_units='xy', scale=1, color='#ff7f0e', width=0.03,
          label="k·v")
ax.quiver(0, 0, v[0], v[1], angles='xy', scale_units='xy', scale=1, color='#1f77b4', width=0.012, label="v")
if np.allclose(v_scaled, 0):
    ax.plot(0, 0, 'o', color='#ff7f0e', markersize=10, label="k·v = 0 (zero vector)")
# Axis limits grow with the vectors so the scaled arrow never leaves the plot (|k·v| can reach 12 per axis)
lim = max(6.0, float(np.max(np.abs(np.concatenate([v, v_scaled])))) * 1.15)
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)
ax.set_aspect('equal', 'box')
ax.grid(True, linestyle='--', alpha=0.4)
ax.set_title(f"v = ({vx}, {vy}),  k·v = ({v_scaled[0]:.1f}, {v_scaled[1]:.1f})")
ax.legend(loc='upper left')

st.pyplot(fig)
plt.close(fig)

st.write("## The formula behind it")
st.latex(r"\mathbf{v} = \begin{pmatrix} x \\ y \end{pmatrix}")
st.latex(r"k \mathbf{v} = k \begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} kx \\ ky \end{pmatrix}")

st.write(
    "### Why this is so special for vectors"
)
st.write(
    "Scalar multiplication treats the arrow like a rubber band attached to the origin. "
    "The arrow always stays on the same line through the origin: only its length changes, "
    "and a negative k additionally reverses its direction (k = 0 squashes it to the zero vector). "
    "That is why we can think of data like images or word embeddings as arrows in space: "
    "scaling by a positive number changes how large their effect is without changing their direction."
)

st.write("## Try a few experiments")
st.write(
    "- Set `k` to `2` and watch the orange arrow double in length.\n"
    "- Set `k` to `0.5` and watch it shrink to half.\n"
    "- Set `k` to `-1` and watch it flip to the other side."
)
