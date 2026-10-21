import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Cosine Similarity — Angle as Agreement")

st.write("""
Cosine similarity measures how much two vectors agree based on the angle between them.
- When they point the same way (0°), similarity is 1 (perfect agreement).
- When perpendicular (90°), it's 0 (no agreement).
- When opposite (180°), it's -1 (total disagreement).
""")

# Slider for angle between vectors
angle_deg = st.slider("Rotate the second vector (degrees)", 0, 180, 0, step=5)
angle_rad = np.radians(angle_deg)

# Define vectors (unit vectors for simplicity)
v1 = np.array([1, 0])  # Fixed vector pointing right
v2 = np.array([np.cos(angle_rad), np.sin(angle_rad)])  # Rotating vector

# Calculate cosine similarity
cos_sim = np.dot(v1, v2)  # Since both are unit vectors, no need to divide

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

# Add angle arc for visualization
if angle_deg > 0:
    theta_vals = np.linspace(0, angle_rad, 100)
    x_arc = np.cos(theta_vals)
    y_arc = np.sin(theta_vals)
    ax.plot(x_arc, y_arc, color='green', linestyle='--', linewidth=1, label=f'Angle: {angle_deg}°')

ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.grid(True, alpha=0.3)
ax.legend()
ax.set_aspect('equal')

st.pyplot(fig)
plt.close(fig)

st.write("**Formula:**")
st.latex(r"\text{Cosine Similarity} = \frac{\mathbf{v}_1 \cdot \mathbf{v}_2}{\|\mathbf{v}_1\|\,\|\mathbf{v}_2\|}")
st.write(r"For unit vectors, it's just the dot product: $\cos(\theta)$.")