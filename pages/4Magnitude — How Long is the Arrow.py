import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Vector Magnitude: How Long is the Arrow?", layout="wide")


def sq(value):
	"""LaTeX for value squared, with negatives in parentheses: (-3.00)^2 instead of the ambiguous -3.00^2."""
	value = float(value) + 0.0  # turns -0.0 into 0.0
	return f"({value:.2f})^2" if value < 0 else f"{value:.2f}^2"

st.title("🧮 Magnitude — How Long is the Arrow?")
st.markdown("""
**The length of a vector is its *magnitude*. But how do we *see* it? Let's build the formula, step by step!**
""")

st.header("🔢 1. Start Simple: 2D Vector")
st.markdown("Pick a 2D vector. Drag the sliders and watch the arrow and its length!")

col1, col2 = st.columns([2, 1])
with col2:
	x2 = st.slider("x component", -10.0, 10.0, 3.0, 0.1, key="p04_x2")
	y2 = st.slider("y component", -10.0, 10.0, 4.0, 0.1, key="p04_y2")

with col1:
	fig, ax = plt.subplots(figsize=(4,4))
	ax.quiver(0, 0, x2, y2, angles='xy', scale_units='xy', scale=1, color='royalblue', width=0.01)
	ax.set_xlim(-11, 11)
	ax.set_ylim(-11, 11)
	ax.set_aspect('equal')
	ax.grid(True, linestyle='--', alpha=0.5)
	ax.plot([0, x2], [0, 0], 'k--', lw=1)
	ax.plot([x2, x2], [0, y2], 'k--', lw=1)
	ax.text(x2/2, -1, f"x = {x2:.1f}", ha='center', color='darkred')
	ax.text(x2+0.5, y2/2, f"y = {y2:.1f}", va='center', color='darkgreen')
	ax.plot(x2, y2, 'o', color='orange')
	plt.tight_layout()
	st.pyplot(fig)
	plt.close(fig)

mag2 = np.sqrt(x2**2 + y2**2)
st.latex(r"|\vec{v}| = \sqrt{x^2 + y^2} = \sqrt{%s + %s} = %.2f" % (sq(x2), sq(y2), mag2))
st.success(f"The magnitude is **{mag2:.2f}**")

st.divider()

st.header("🔺 2. Level Up: 3D Vector")
st.markdown("Now add a z-component! Drag all three sliders and see the 3D arrow and its length.")

col3, col4 = st.columns([2, 1])
with col4:
	x3 = st.slider("x component (3D)", -10.0, 10.0, 2.0, 0.1, key="p04_x3")
	y3 = st.slider("y component (3D)", -10.0, 10.0, 2.0, 0.1, key="p04_y3")
	z3 = st.slider("z component (3D)", -10.0, 10.0, 5.0, 0.1, key="p04_z3")

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
	ax3.plot([0, x3], [0, 0], [0, 0], 'k:', lw=1)
	ax3.plot([x3, x3], [0, y3], [0, 0], 'k:', lw=1)
	ax3.plot([x3, x3], [y3, y3], [0, z3], 'k:', lw=1)
	ax3.view_init(elev=30, azim=45)
	st.pyplot(fig3)
	plt.close(fig3)

mag3 = np.sqrt(x3**2 + y3**2 + z3**2)
st.latex(r"|\vec{v}| = \sqrt{x^2 + y^2 + z^2} = \sqrt{%s + %s + %s} = %.2f" % (sq(x3), sq(y3), sq(z3), mag3))
st.success(f"The magnitude is **{mag3:.2f}**")

st.divider()

st.header("🌈 3. Any Number of Dimensions!")
st.markdown("""
Type in a list of numbers (your vector), and see its magnitude instantly. Try 4D, 5D, or more!
""")

vec_str = st.text_input("Enter vector components, separated by commas", "3, 4, 12", key="p04_vec_str")
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
	st.latex(r"|\vec{v}| = \sqrt{" + " + ".join(sq(v) for v in vec) + r"} = " + f"{magN:.2f}")
	st.success(f"Magnitude: **{magN:.2f}** for vector {vec.tolist()}")
except ValueError:
	st.error("Enter up to 100 finite numeric components separated by commas.")

st.divider()

st.header("🎲 Fun Challenge!")
st.markdown("""
Guess the magnitude! Try to estimate the length of a random vector before revealing the answer. Can you get close?
""")


def p04_draw_vector(draw_number):
	rng = np.random.default_rng(draw_number)
	return rng.integers(-9, 10, size=int(rng.integers(2, 6))).tolist()


if "p04_rand_vec" not in st.session_state:
	st.session_state.p04_rand_draws = 0
	st.session_state.p04_rand_vec = p04_draw_vector(0)

if st.button("New Random Vector", key="p04_new_vector"):
	st.session_state.p04_rand_draws += 1
	st.session_state.p04_rand_vec = p04_draw_vector(st.session_state.p04_rand_draws)

rand_vec = np.array(st.session_state.p04_rand_vec)
st.write(f"Random vector: `{rand_vec.tolist()}`")
guess = st.number_input("Your guess for the magnitude:", min_value=0.0, max_value=100.0, value=0.0, step=0.1,
						key="p04_guess")
if st.button("Check My Guess", key="p04_check_guess"):
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
* In machine learning, the length of a vector can mean the overall brightness of an image, the energy of a signal, or how large a model's weights have grown (which regularization keeps in check).
* It's the Pythagorean theorem, supercharged for any number of dimensions!
""")
