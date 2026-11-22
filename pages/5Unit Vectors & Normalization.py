import math
import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Unit Vectors & Normalization", layout="wide")

st.title("🧮 Unit Vectors & Normalization")
st.markdown("""
**A unit vector is an arrow with a length of exactly $1$. But how do we turn *any* vector into length $1$? Let's see how normalization works, step by step!**
""")

# ==========================================
# 1. 2D VECTOR NORMALIZATION
# ==========================================

st.header("🔢 1. Start Simple: 2D Vector")
st.markdown("Pick a 2D vector. Watch how dividing by its length shrinks (or stretches) it to fit perfectly on the **unit circle**!")

col1, col2 = st.columns([2, 1])
with col2:
    x2 = st.slider("x component", -10.0, 10.0, 3.0, 0.1, key="x2")
    y2 = st.slider("y component", -10.0, 10.0, 4.0, 0.1, key="y2")
    step2 = st.slider(
        "Animation step (Original → Unit)",
        0.0, 1.0, 1.0, 0.05,
        key="step2",
        help="0 = original vector, 1 = normalized unit vector"
    )

mag2 = float(np.sqrt(x2**2 + y2**2))

with col1:
    fig2 = go.Figure()

    # Draw unit circle (r = 1)
    theta = np.linspace(0, 2 * np.pi, 200)
    fig2.add_trace(go.Scatter(
        x=np.cos(theta),
        y=np.sin(theta),
        mode='lines',
        line=dict(color='#10B981', width=2, dash='dash'),
        name='Unit circle (r = 1)',
        hoverinfo='skip'
    ))

    # Dynamic plot limits
    lim2 = max(abs(x2), abs(y2), 1.5) * 1.25
    lim2 = max(lim2, 2.0)

    if mag2 > 1e-9:
        ux2 = x2 / mag2
        uy2 = y2 / mag2

        # Original vector
        fig2.add_trace(go.Scatter(
            x=[0, x2], y=[0, y2],
            mode='lines+markers',
            line=dict(color='royalblue', width=4),
            marker=dict(size=8, color='royalblue'),
            name=f'Original v ({x2:.1f}, {y2:.1f}) |v|={mag2:.2f}',
            hovertemplate='Original v: (%{x:.2f}, %{y:.2f})<extra></extra>'
        ))

        # Triangle legs
        fig2.add_trace(go.Scatter(
            x=[0, x2, x2],
            y=[0, 0, y2],
            mode='lines',
            line=dict(color='#94A3B8', width=1.5, dash='dot'),
            name='Components',
            hoverinfo='skip'
        ))

        # Target unit vector landing point
        fig2.add_trace(go.Scatter(
            x=[ux2], y=[uy2],
            mode='markers',
            marker=dict(size=12, color='#10B981', symbol='circle-open', line=dict(width=3)),
            name=f'Unit spot ({ux2:.2f}, {uy2:.2f})',
            hovertemplate=f'Unit vector: ({ux2:.2f}, {uy2:.2f})<br>Length = 1.00<extra></extra>'
        ))

        # Interpolating arrow (from v to unit v)
        cx2 = x2 + step2 * (ux2 - x2)
        cy2 = y2 + step2 * (uy2 - y2)
        c_mag2 = float(np.sqrt(cx2**2 + cy2**2))

        fig2.add_trace(go.Scatter(
            x=[0, cx2], y=[0, cy2],
            mode='lines+markers',
            line=dict(color='orange', width=6),
            marker=dict(size=10, color='orange'),
            name=f'Arrow (length = {c_mag2:.2f})',
            hovertemplate=f'Arrow: ({cx2:.2f}, {cy2:.2f})<br>Length: {c_mag2:.2f}<extra></extra>'
        ))

    fig2.update_layout(
        xaxis=dict(range=[-lim2, lim2], zeroline=True, showgrid=True, scaleanchor="y", scaleratio=1),
        yaxis=dict(range=[-lim2, lim2], zeroline=True, showgrid=True),
        height=400,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    st.plotly_chart(fig2, width="stretch", alt="2D vector normalization on unit circle")

if mag2 > 1e-9:
    ux2 = x2 / mag2
    uy2 = y2 / mag2

    st.markdown("#### 📝 How to normalize this vector (step by step):")
    st.latex(r"\textbf{Step 1 (Length): } |\vec{v}| = \sqrt{x^2 + y^2} = \sqrt{%.2f^2 + %.2f^2} = \mathbf{%.2f}" % (x2, y2, mag2))
    st.latex(r"\textbf{Step 2 (Divide): } \hat{v} = \left(\frac{x}{|\vec{v}|}, \frac{y}{|\vec{v}|}\right) = \left(\frac{%.2f}{%.2f}, \frac{%.2f}{%.2f}\right) = \mathbf{(%.2f, %.2f)}" % (x2, mag2, y2, mag2, ux2, uy2))
    st.latex(r"\textbf{Step 3 (Verify): } |\hat{v}| = \sqrt{%.2f^2 + %.2f^2} = \mathbf{1.00}" % (ux2, uy2))

    if mag2 > 1.05:
        st.success(f"Original length was **{mag2:.2f}** (> 1), so dividing by {mag2:.2f} **shrank** it to **1.00**!")
    elif mag2 < 0.95:
        st.info(f"Original length was **{mag2:.2f}** (< 1), so dividing by {mag2:.2f} **stretched** it out to **1.00**!")
    else:
        st.success("Length is already **1.00**!")
else:
    st.warning("A zero vector (0, 0) has length 0, so dividing by 0 is undefined!")

st.divider()

# ==========================================
# 2. 3D VECTOR NORMALIZATION
# ==========================================

st.header("🔺 2. Level Up: 3D Vector")
st.markdown("Now add a z-component! Dividing by the 3D length places the arrow directly on the **unit sphere**.")

col3, col4 = st.columns([2, 1])
with col4:
    x3 = st.slider("x component (3D)", -10.0, 10.0, 2.0, 0.1, key="x3")
    y3 = st.slider("y component (3D)", -10.0, 10.0, 3.0, 0.1, key="y3")
    z3 = st.slider("z component (3D)", -10.0, 10.0, 6.0, 0.1, key="z3")
    step3 = st.slider(
        "Animation step (3D)",
        0.0, 1.0, 1.0, 0.05,
        key="step3",
        help="0 = original vector, 1 = normalized unit vector"
    )

mag3 = float(np.sqrt(x3**2 + y3**2 + z3**2))

with col3:
    fig3 = go.Figure()

    # Wireframe unit sphere rings (r = 1)
    t = np.linspace(0, 2 * np.pi, 80)
    fig3.add_trace(go.Scatter3d(
        x=np.cos(t), y=np.sin(t), z=np.zeros_like(t),
        mode='lines', line=dict(color='#10B981', width=3, dash='dash'),
        name='Unit sphere equator (r = 1)', hoverinfo='skip'
    ))
    fig3.add_trace(go.Scatter3d(
        x=np.cos(t), y=np.zeros_like(t), z=np.sin(t),
        mode='lines', line=dict(color='#10B981', width=2, dash='dot'),
        name='Unit sphere meridian', hoverinfo='skip'
    ))

    lim3 = max(abs(x3), abs(y3), abs(z3), 1.5) * 1.25
    lim3 = max(lim3, 2.0)

    if mag3 > 1e-9:
        ux3 = x3 / mag3
        uy3 = y3 / mag3
        uz3 = z3 / mag3

        # Original vector
        fig3.add_trace(go.Scatter3d(
            x=[0, x3], y=[0, y3], z=[0, z3],
            mode='lines+markers',
            line=dict(color='royalblue', width=5),
            marker=dict(size=6, color='royalblue'),
            name=f'Original v |v|={mag3:.2f}',
            hovertemplate=f'Original: ({x3:.2f}, {y3:.2f}, {z3:.2f})<extra></extra>'
        ))

        # Projections to floor
        fig3.add_trace(go.Scatter3d(
            x=[0, x3, x3], y=[0, y3, y3], z=[0, 0, z3],
            mode='lines',
            line=dict(color='#94A3B8', width=2, dash='dash'),
            name='Projections', hoverinfo='skip'
        ))

        # Current / normalized arrow
        cx3 = x3 + step3 * (ux3 - x3)
        cy3 = y3 + step3 * (uy3 - y3)
        cz3 = z3 + step3 * (uz3 - z3)
        c_mag3 = float(np.sqrt(cx3**2 + cy3**2 + cz3**2))

        fig3.add_trace(go.Scatter3d(
            x=[0, cx3], y=[0, cy3], z=[0, cz3],
            mode='lines+markers',
            line=dict(color='orange', width=7),
            marker=dict(size=7, color='orange'),
            name=f'Arrow (length = {c_mag3:.2f})',
            hovertemplate=f'Arrow: ({cx3:.2f}, {cy3:.2f}, {cz3:.2f})<extra></extra>'
        ))

    fig3.update_layout(
        scene=dict(
            xaxis=dict(range=[-lim3, lim3], title="x"),
            yaxis=dict(range=[-lim3, lim3], title="y"),
            zaxis=dict(range=[-lim3, lim3], title="z"),
            aspectmode='cube'
        ),
        height=420,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0)
    )
    st.plotly_chart(fig3, width="stretch", alt="3D vector normalization on unit sphere")

if mag3 > 1e-9:
    ux3 = x3 / mag3
    uy3 = y3 / mag3
    uz3 = z3 / mag3

    st.latex(r"|\vec{v}| = \sqrt{x^2 + y^2 + z^2} = \sqrt{%.2f^2 + %.2f^2 + %.2f^2} = %.2f" % (x3, y3, z3, mag3))
    st.latex(r"\hat{v} = \left(\frac{x}{|\vec{v}|}, \frac{y}{|\vec{v}|}, \frac{z}{|\vec{v}|}\right) = \mathbf{(%.2f, %.2f, %.2f)}" % (ux3, uy3, uz3))
    st.success(f"The 3D unit vector is **({ux3:.2f}, {uy3:.2f}, {uz3:.2f})** with magnitude **1.00**")
else:
    st.warning("A zero vector (0, 0, 0) has length 0, so dividing by 0 is undefined!")

st.divider()

# ==========================================
# 3. ANY NUMBER OF DIMENSIONS!
# ==========================================

st.header("🌈 3. Any Number of Dimensions!")
st.markdown("""
Type in a list of numbers (your vector), and see it normalized instantly. Try 4D, 5D, or word embeddings!
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
    magN = float(np.linalg.norm(vec))
    if not np.isfinite(magN):
        raise ValueError("The vector magnitude is outside the supported numeric range.")

    if magN > 1e-9:
        unitN = vec / magN
        st.latex(r"|\vec{v}| = \sqrt{" + " + ".join([f"{v:.2f}^2" for v in vec]) + f"}} = {magN:.2f}")
        st.latex(r"\hat{v} = \frac{\vec{v}}{" + f"{magN:.2f}" + r"} = \mathbf{[" + ", ".join([f"{u:.2f}" for u in unitN]) + "]}")
        st.success(f"Unit Vector: **{np.round(unitN, 2).tolist()}** (Length = {float(np.linalg.norm(unitN)):.2f})")
    else:
        st.warning("Zero vector cannot be normalized (division by zero).")
except ValueError:
    st.error("Enter up to 100 finite numeric components separated by commas.")

st.divider()

# ==========================================
# 4. FUN CHALLENGE!
# ==========================================

st.header("🎲 Fun Challenge!")
st.markdown("""
Guess whether normalizing this random vector will **shrink** it or **stretch** it!
""")

if 'rand_norm_vec' not in st.session_state:
    dim = np.random.randint(2, 5)
    st.session_state.rand_norm_vec = np.random.uniform(-5.0, 5.0, size=dim).round(1)

if st.button("New Random Vector"):
    dim = np.random.randint(2, 5)
    st.session_state.rand_norm_vec = np.random.uniform(-5.0, 5.0, size=dim).round(1)

rand_vec = st.session_state.rand_norm_vec
st.write(f"Random vector: `{rand_vec.tolist()}`")

guess = st.radio("Will normalization shrink or stretch it?", ["Shrink it (length > 1)", "Stretch it (length < 1)"])
if st.button("Check My Answer"):
    actual_len = float(np.linalg.norm(rand_vec))
    is_shrink = actual_len > 1.0

    if (guess.startswith("Shrink") and is_shrink) or (guess.startswith("Stretch") and not is_shrink):
        st.balloons()
        st.success(f"Correct! Length is **{actual_len:.2f}**, so dividing by {actual_len:.2f} {'shrinks' if is_shrink else 'stretches'} it to 1.00!")
    else:
        st.warning(f"Not quite! The length is **{actual_len:.2f}**, which is {'greater' if is_shrink else 'less'} than 1.0, so it {'shrinks' if is_shrink else 'stretches'}.")

st.divider()

# ==========================================
# 5. WHY DOES THIS MATTER?
# ==========================================

st.header("🤔 Why Does This Matter?")
st.markdown("""
* **Pure direction without scale:** Normalizing removes the size of the vector while keeping its exact direction.
* **Cosine similarity in AI:** When comparing embeddings in AI (like search queries and documents), normalizing them first makes cosine similarity simply equal to the dot product!
* **Stops exploding numbers:** In deep neural networks, normalizing vectors (like LayerNorm in Transformers) prevents numbers from blowing up to infinity or vanishing to zero.
""")
