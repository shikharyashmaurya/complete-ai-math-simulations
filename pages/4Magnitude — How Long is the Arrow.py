import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

st.set_page_config(page_title="Vector Magnitude: How Long is the Arrow?", layout="wide")

st.title("🧮 Magnitude — How Long is the Arrow?")
st.markdown("""
**The length of a vector is its *magnitude*. But how do we *see* it? Let's build the formula, step by step!**
""")

st.header("🔢 1. Start Simple: 2D Vector")
st.markdown("Pick a 2D vector. Drag the sliders and watch the arrow and its length!")

col1, col2 = st.columns([2, 1])
with col2:
	x2 = st.slider("x component", -10.0, 10.0, 3.0, 0.1, key="x2")
	y2 = st.slider("y component", -10.0, 10.0, 4.0, 0.1, key="y2")

with col1:
	fig, ax = plt.subplots(figsize=(4,4))
	ax.quiver(0, 0, x2, y2, angles='xy', scale_units='xy', scale=1, color='royalblue', width=0.01)
	ax.set_xlim(-11, 11)
	ax.set_ylim(-11, 11)
	ax.set_aspect('equal')
	ax.grid(True, linestyle='--', alpha=0.5)
	ax.plot([0, x2], [0, 0], 'k--', lw=1)
	ax.plot([x2, x2], [0, y2], 'k--', lw=1)
	ax.text(x2/2, -1, f"x = {x2}", ha='center', color='darkred')
	ax.text(x2+0.5, y2/2, f"y = {y2}", va='center', color='darkgreen')
	ax.plot(x2, y2, 'o', color='orange')
	plt.tight_layout()
	st.pyplot(fig)
	plt.close(fig)

mag2 = np.sqrt(x2**2 + y2**2)
st.latex(r"|\vec{v}| = \sqrt{x^2 + y^2} = \sqrt{{%.2f}^2 + {%.2f}^2} = %.2f" % (x2, y2, mag2))
st.success(f"The magnitude is **{mag2:.2f}**")

st.divider()

st.header("🔺 2. Level Up: 3D Vector")
st.markdown("Now add a z-component! Drag all three sliders and see the 3D arrow and its length.")

col3, col4 = st.columns([2, 1])
with col4:
	x3 = st.slider("x component (3D)", -10.0, 10.0, 2.0, 0.1, key="x3")
	y3 = st.slider("y component (3D)", -10.0, 10.0, 2.0, 0.1, key="y3")
	z3 = st.slider("z component (3D)", -10.0, 10.0, 5.0, 0.1, key="z3")

with col3:
	fig3 = plt.figure(figsize=(5,5))
	ax3 = fig3.add_subplot(111, projection='3d')
	ax3.quiver(0, 0, 0, x3, y3, z3, color='royalblue', arrow_length_ratio=0.1, linewidth=2)
	ax3.set_xlim([-11, 11])
	ax3.set_ylim([-11, 11])
	ax3.set_zlim([-11, 11])
	ax3.set_xlabel('x')
	ax3.set_ylabel('y')
	ax3.set_zlabel('z')
	ax3.scatter([x3], [y3], [z3], color='orange', s=60)
	ax3.plot([0, x3], [0, y3], [0, 0], 'k--', lw=1)
	ax3.plot([x3, x3], [y3, y3], [0, z3], 'k--', lw=1)
	ax3.plot([0, x3], [0, 0], [0, 0], 'k:', lw=1)
	ax3.plot([x3, x3], [0, y3], [0, 0], 'k:', lw=1)
	ax3.plot([x3, x3], [y3, y3], [0, z3], 'k:', lw=1)
	ax3.view_init(elev=30, azim=45)
	st.pyplot(fig3)
	plt.close(fig3)

mag3 = np.sqrt(x3**2 + y3**2 + z3**2)
st.latex(r"|\vec{{v}}| = \sqrt{{x^2 + y^2 + z^2}} = \sqrt{{%.2f}^2 + {%.2f}^2 + {%.2f}^2} = %.2f" % (x3, y3, z3, mag3))
st.success(f"The magnitude is **{mag3:.2f}**")

st.divider()

st.header("🌈 3. Any Number of Dimensions!")
st.markdown("""
Type in a list of numbers (your vector), and see its magnitude instantly. Try 4D, 5D, or more!
""")

vec_str = st.text_input("Enter vector components, separated by commas", "3, 4, 12")
try:
	if len(vec_str) > 2048:
		raise ValueError("The vector input is too long.")
	components = [float(x.strip()) for x in vec_str.split(",")]
	if len(components) > 100:
		raise ValueError("A vector can contain at most 100 components.")
	if not np.isfinite(components).all():
		raise ValueError("Vector components must be finite.")
	vec = np.array(components)
	magN = np.linalg.norm(vec)
	if not np.isfinite(magN):
		raise ValueError("The vector magnitude is outside the supported numeric range.")
	st.latex(r"|\vec{{v}}| = \sqrt{{{}}} = {:.2f}".format(
		' + '.join([f"{v:.2f}^2" for v in vec]), magN))
	st.success(f"Magnitude: **{magN:.2f}** for vector {vec}")
except ValueError:
	st.error("Enter up to 100 finite numeric components separated by commas.")

st.divider()

st.header("🎲 Fun Challenge!")
st.markdown("""
Guess the magnitude! Try to estimate the length of a random vector before revealing the answer. Can you get close?
""")

if 'rand_vec' not in st.session_state or st.button("New Random Vector"):
	st.session_state.rand_vec = np.random.randint(-9, 10, size=np.random.randint(2, 6))

rand_vec = st.session_state.rand_vec
st.write(f"Random vector: {rand_vec}")
guess = st.number_input("Your guess for the magnitude:", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
if st.button("Check My Guess"):
	actual = np.linalg.norm(rand_vec)
	diff = abs(actual - guess)
	if diff < 0.1:
		st.balloons()
		st.success(f"Spot on! The magnitude is {actual:.2f}.")
	elif diff < 1.0:
		st.info(f"Very close! The magnitude is {actual:.2f}.")
	else:
		st.warning(f"Not quite. The magnitude is {actual:.2f}. Try again!")

st.divider()

st.header("🤔 Why Does This Matter?")
st.markdown("""
* The magnitude tells us **how big** a vector is — whether it's a force, a velocity, or a data point in AI!
* In machine learning, the length of a vector can mean the brightness of an image, the energy of a signal, or the confidence of a prediction.
* It's the Pythagorean theorem, supercharged for any number of dimensions!
""")
