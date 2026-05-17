import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --- Page Configuration ---
st.set_page_config(page_title="Vectors: Data Has a Direction", layout="wide")

# --- Helper Functions ---
def create_smiley_image():
    """Creates a simple 28x28 pixel-art smiley face to mimic an MNIST digit."""
    img = np.zeros((28, 28))
    # Eyes
    img[8:12, 8:11] = 0.9
    img[8:12, 17:20] = 0.9
    # Mouth
    img[18:20, 8:20] = 0.7
    img[16:18, 6:8] = 0.6
    img[16:18, 20:22] = 0.6
    # Add a little "sensor noise" to make it look like real data
    noise = np.random.uniform(0, 0.1, (28, 28))
    return np.clip(img + noise, 0, 1)

# --- Main App Header ---
st.title("🧮 Vectors: From a Number to a Universe of Pixels")
st.markdown("""
Welcome to the foundation of AI! To a computer, **everything is a number**. But numbers rarely travel alone. 
Let's take a journey to see how a single solitary number evolves into the massive data structures that power modern Artificial Intelligence.
""")

st.divider()

# --- STEP 1: The Scalar and 1D Vector ---
st.header("1. The Scalar (0D) vs The 1D Vector 📏")
st.markdown("""
A **scalar** (0D) is just a fancy word for a single, regular number. It tells us *magnitude* (how much), but it has no *direction*. It's a point.

A **1D Vector**, on the other hand, is an arrow along a single line (like a number line). While it also holds just one number, it technically has a **direction** (left or right along that axis). 

*Programming Tip:* In AI, confusing a 0D scalar like `5` with a 1D list like `[5]` is a very common source of bugs!
""")

scalar_val = st.slider("Pick a number", min_value=-10.0, max_value=10.0, value=5.0, step=0.5)

col_scalar1, col_scalar2 = st.columns(2)
with col_scalar1:
    st.info(f"**0D Scalar:**\n\n $s = {scalar_val}$")
with col_scalar2:
    st.info(f"**1D Vector:**\n\n $v = \\begin{{bmatrix}} {scalar_val} \\end{{bmatrix}}$")

fig1 = go.Figure()

# 1D Vector (Arrow)
fig1.add_annotation(x=scalar_val, y=0.3, ax=0, ay=0.3, xref="x", yref="y", axref="x", ayref="y",
                    showarrow=True, arrowhead=3, arrowsize=2, arrowwidth=3, arrowcolor="cyan")
fig1.add_trace(go.Scatter(x=[scalar_val], y=[0.45], mode='text', 
                          text=["1D Vector (Arrow)"], textposition="middle center", textfont=dict(color="cyan")))

# 0D Scalar (Point)
fig1.add_trace(go.Scatter(x=[scalar_val], y=[-0.3], mode='markers+text', 
                          marker=dict(color='orange', size=15),
                          text=["0D Scalar (Point)"], textposition="bottom center", textfont=dict(color="orange")))

fig1.add_hline(y=0, line_width=1, line_color="gray", line_dash="dash")
fig1.update_xaxes(range=[-11, 11], zeroline=True, zerolinewidth=2, zerolinecolor='white')
fig1.update_yaxes(showticklabels=False, range=[-1, 1])
fig1.update_layout(height=250, margin=dict(l=20, r=20, t=20, b=20), showlegend=False)
st.plotly_chart(fig1, use_container_width=True)

st.divider()

# --- STEP 2: The 2D Vector ---
st.header("2. The 2D Vector (The Arrow) ↗️")
st.markdown("What if we need to describe something with *two* properties? Like a coordinate on a map (X, Y). Now, our data has a **direction** and a **length**. It becomes an arrow!")

col1, col2 = st.columns(2)
with col1:
    x_val = st.slider("X (Horizontal)", -10, 10, 4)
    y_val = st.slider("Y (Vertical)", -10, 10, 7)
    st.info(f"**Vector Notation:**\n\n $v = \\begin{{bmatrix}} {x_val} \\\\ {y_val} \\end{{bmatrix}}$")

with col2:
    fig2 = go.Figure()
    # Draw arrow
    fig2.add_annotation(x=x_val, y=y_val, ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y",
                        showarrow=True, arrowhead=3, arrowsize=2, arrowwidth=3, arrowcolor="cyan")
    fig2.update_xaxes(range=[-11, 11], zeroline=True, zerolinewidth=2, zerolinecolor='gray')
    fig2.update_yaxes(range=[-11, 11], zeroline=True, zerolinewidth=2, zerolinecolor='gray')
    fig2.update_layout(height=400, width=400, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig2, use_container_width=False)

st.divider()

# --- STEP 3: The 3D Vector ---
st.header("3. The 3D Vector (Taking up Space) 🧊")
st.markdown("Add a third number, and our arrow pops off the screen into 3D space. It's now a list of 3 numbers: `[X, Y, Z]`.")

col3, col4 = st.columns(2)
with col3:
    z_val = st.slider("Z (Depth)", -10, 10, 5)
    st.info(f"**Vector:**\n\n $v = \\begin{{bmatrix}} {x_val} \\\\ {y_val} \\\\ {z_val} \\end{{bmatrix}}$")

with col4:
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter3d(x=[0, x_val], y=[0, y_val], z=[0, z_val],
                                mode='lines+markers',
                                marker=dict(size=5, color='magenta'),
                                line=dict(color='magenta', width=5)))
    fig3.update_layout(scene=dict(xaxis=dict(range=[-10, 10]), 
                                  yaxis=dict(range=[-10, 10]), 
                                  zaxis=dict(range=[-10, 10])),
                       margin=dict(l=0, r=0, t=0, b=0), height=400)
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# --- STEP 4: N-Dimensional Vector ---
st.header("4. The N-Dimensional Vector (The List) 📜")
st.markdown("""
Here is where human brains break, but computers thrive. We can't draw a 4D, 10D, or 100D arrow. 
But a computer doesn't care about arrows. To a computer, **a vector is just a list of numbers**. 
Let's generate a 15-dimensional vector. It's no longer an arrow; it's a data profile!
""")

if st.button("🎲 Generate Random 15-Dim Vector"):
    n_dim_vector = np.random.randint(-50, 50, 15)
else:
    n_dim_vector = np.array([12, -4, 33, 0, -19, 45, 8, -22, 14, 5, -9, 27, 3, -41, 10])

st.code(f"v = {list(n_dim_vector)}", language="python")

# Visualize the array as a bar chart to show "magnitudes" of each dimension
fig4 = go.Figure(data=[go.Bar(y=n_dim_vector, marker_color='springgreen')])
fig4.update_layout(title="Visualizing a 15-Dimensional List", height=300, 
                   xaxis_title="Dimension Index (0 to 14)", yaxis_title="Value")
st.plotly_chart(fig4, use_container_width=True)

st.divider()

# --- STEP 5: The Grand Finale (Image as a Vector) ---
st.header("5. The Grand Finale: Images are just Long Vectors! 🖼️")
st.markdown("""
When you feed an image into a basic Neural Network, it doesn't have "eyes" to see a 2D square. 
Instead, it takes the grid of pixels and **unrolls** them into one incredibly long vector. 

Let's look at a 28×28 pixel grayscale image (like the ones in the famous MNIST dataset). 
**$28 \\times 28 = 784$**. Therefore, this image is just a **784-Dimensional Vector!**
""")

image_data = create_smiley_image()

col5, col6 = st.columns(2)

with col5:
    st.subheader("How We See It (28x28 Grid)")
    fig5 = go.Figure(data=go.Heatmap(z=np.flipud(image_data), colorscale='gray', showscale=False))
    fig5.update_layout(width=400, height=400, xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False), margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig5)

with col6:
    st.subheader("How AI Sees It (784x1 Vector)")
    # Flatten the image
    flattened_image = image_data.flatten()
    
    # We display it as a long, multi-column heatmap so it fits on screen, 
    # but we represent it visually as a continuous stream of data.
    reshaped_for_viewing = flattened_image.reshape(28, 28) # Kept square purely to fit on the screen without scrolling forever!
    
    st.markdown("We take the rows of the image and stack them end-to-end into a single line:")
    
    # Interactive slice viewer
    elements_to_show = st.slider("Drag to unroll more pixels into our list:", min_value=10, max_value=784, value=50, step=10)
    
    st.code(f"x = {np.round(flattened_image[:elements_to_show], 2).tolist()} ... [length: 784]", language="python")
    
    st.success("If an AI wants to learn this face, it's just looking for mathematical patterns inside that long list of 784 numbers!")

