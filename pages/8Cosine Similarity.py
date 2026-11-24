import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cosine Similarity", layout="wide")

st.title("Cosine Similarity — Angle as Agreement")

st.write("""
Cosine similarity measures how much two vectors agree based on the angle between them.
- When they point the same way (0°), similarity is 1 (perfect agreement).
- When perpendicular (90°), it's 0 (no agreement).
- When opposite (180°), it's -1 (total disagreement).

Unlike the plain dot product, cosine similarity **ignores length**: change the lengths below and watch the
dot product move while the cosine similarity stays put.
""")

# Sliders for the angle and the two lengths
angle_deg = st.slider("Rotate the second vector (degrees)", 0, 180, 0, step=5, key="p08_angle")
len_col1, len_col2 = st.columns(2)
with len_col1:
    len1 = st.slider("Length of Vector 1", 0.5, 3.0, 1.0, step=0.5, key="p08_len1")
with len_col2:
    len2 = st.slider("Length of Vector 2", 0.5, 3.0, 1.0, step=0.5, key="p08_len2")
angle_rad = np.radians(angle_deg)

v1 = len1 * np.array([1.0, 0.0])  # Fixed direction pointing right
v2 = len2 * np.array([np.cos(angle_rad), np.sin(angle_rad)])  # Rotating vector

# Full formula: divide the dot product by both lengths (both lengths are >= 0.5, so no division by zero)
dot_value = float(np.dot(v1, v2))
cos_sim = dot_value / (np.linalg.norm(v1) * np.linalg.norm(v2))

m1, m2 = st.columns(2)
m1.metric("Dot product v1 · v2 (depends on length)", f"{dot_value:.3f}")
m2.metric("Cosine similarity (length-free)", f"{cos_sim:.3f}")

# Display cosine value with fun message
if cos_sim > 0.9:
    st.success(f"Cosine Similarity: {cos_sim:.3f} — They totally agree! 🤝")
elif cos_sim > 0.1:
    st.info(f"Cosine Similarity: {cos_sim:.3f} — Some agreement.")
elif cos_sim > -0.1:
    st.warning(f"Cosine Similarity: {cos_sim:.3f} — Neutral, no strong opinion.")
else:
    st.error(f"Cosine Similarity: {cos_sim:.3f} — They disagree! 😠")

# Plot the vectors
fig, ax = plt.subplots(figsize=(6, 6))
ax.quiver(0, 0, v1[0], v1[1], angles='xy', scale_units='xy', scale=1, color='blue', width=0.01, label='Vector 1 (Fixed)')
ax.quiver(0, 0, v2[0], v2[1], angles='xy', scale_units='xy', scale=1, color='red', width=0.01, label='Vector 2 (Rotating)')

# Add angle arc for visualization (radius 0.4 so it stays inside even the shortest arrows)
if angle_deg > 0:
    theta_vals = np.linspace(0, angle_rad, 100)
    x_arc = 0.4 * np.cos(theta_vals)
    y_arc = 0.4 * np.sin(theta_vals)
    ax.plot(x_arc, y_arc, color='green', linestyle='--', linewidth=1, label=f'Angle: {angle_deg}°')

lim = max(len1, len2) * 1.2
ax.set_xlim(-lim, lim)
ax.set_ylim(-0.3 * lim, lim)
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.grid(True, alpha=0.3)
ax.legend(loc='lower left')
ax.set_aspect('equal')

plot_col, _ = st.columns([1, 1])
with plot_col:
    st.pyplot(fig)
plt.close(fig)

st.write("**Formula:**")
st.latex(r"\text{Cosine Similarity} = \frac{\mathbf{v}_1 \cdot \mathbf{v}_2}{\|\mathbf{v}_1\|\,\|\mathbf{v}_2\|} = \cos(\theta)")
st.latex(
    r"= \frac{%.2f}{%.2f \times %.2f} = %.3f"
    % (dot_value, np.linalg.norm(v1), np.linalg.norm(v2), cos_sim)
)
st.write(r"For unit vectors (both lengths = 1), the denominator is 1, so it's just the dot product: $\cos(\theta)$.")
st.caption("Cosine similarity is undefined if either vector is the zero vector (you would divide by 0), "
           "which is why the length sliders start at 0.5.")