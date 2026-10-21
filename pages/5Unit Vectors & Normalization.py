import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

st.set_page_config(page_title="Unit Vectors & Normalization", page_icon="🧮")

st.title("🧮 Unit Vectors & Normalization")
st.markdown("""
**How do you turn any vector into a length-1 arrow?**

Let's play with vectors and watch them shrink (or grow!) to become *unit vectors* — arrows of length 1, pointing in the same direction.
""")

st.markdown("---")

st.header("🎯 Pick Your Vector!")
col1, col2 = st.columns(2)
with col1:
	x = st.slider("X Component", -10.0, 10.0, 3.0, 0.1)
with col2:
	y = st.slider("Y Component", -10.0, 10.0, 4.0, 0.1)

vec = np.array([x, y])
mag = np.linalg.norm(vec)
if mag != 0:
	unit_vec = vec / mag
else:
	unit_vec = np.zeros_like(vec)

st.markdown(f"**Your vector:** $({x},\ {y})$  ")
st.markdown(f"**Magnitude:** $\\sqrt{{{x}^2 + {y}^2}} = {mag:.2f}$  ")
st.markdown(f"**Unit vector:** $({unit_vec[0]:.2f},\ {unit_vec[1]:.2f})$  ")

st.markdown("---")

st.header("🪄 Watch the Magic: Normalization Animation")

frames = 30
def interpolate_vec(start, end, t):
	return start + (end - start) * t

def plot_vector(ax, vec, color, label, alpha=1.0, zorder=1, width=0.08, head=0.25):
	ax.add_patch(FancyArrowPatch((0,0), vec, color=color, lw=3, arrowstyle=f'-|>,head_length={head},head_width=0.2',
								 mutation_scale=20, alpha=alpha, zorder=zorder))
	ax.text(vec[0]*1.1, vec[1]*1.1, label, color=color, fontsize=14, weight='bold', zorder=zorder+1)

def make_animation_frame(vec, unit_vec, step, frames=30):
	t = step / frames
	interp = interpolate_vec(vec, unit_vec, t)
	interp_mag = np.linalg.norm(interp)
	fig, ax = plt.subplots(figsize=(4,4))
	ax.set_xlim(-11, 11)
	ax.set_ylim(-11, 11)
	ax.axhline(0, color='grey', lw=1)
	ax.axvline(0, color='grey', lw=1)
	plot_vector(ax, vec, 'tab:blue', 'Original', alpha=0.3, zorder=1)
	plot_vector(ax, interp, 'tab:orange', 'Shrinking', alpha=0.9, zorder=2)
	plot_vector(ax, unit_vec, 'tab:green', 'Unit', alpha=0.5, zorder=0)
	ax.set_aspect('equal')
	ax.set_xticks([])
	ax.set_yticks([])
	ax.set_title(f"Length: {interp_mag:.2f}")
	fig.tight_layout()
	return fig

if mag > 0:
	step = st.slider("Animation Step", 0, frames, 0)
	fig = make_animation_frame(vec, unit_vec, step, frames)
	st.pyplot(fig)
	plt.close(fig)
	st.caption("Move the slider to watch your vector shrink (or grow) to length 1!")
else:
	st.warning("Pick a non-zero vector to see normalization in action!")

st.markdown("""
---
### 🤔 Why Normalize?
Unit vectors are everywhere in AI and math! They keep direction but lose scale — perfect for comparing directions, finding angles, and making sure things don't explode in size.
""")
