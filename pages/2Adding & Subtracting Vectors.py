import streamlit as st
import plotly.graph_objects as go

# --- Page Config ---
st.set_page_config(page_title="Adding & Subtracting Vectors", layout="wide")

# --- Title and Intro ---
st.title("Adding & Subtracting Vectors")
st.markdown("""
Welcome to the Navigation Console! You are programming a space drone. 
The drone receives movement commands as **Vectors**. 
* **Vector A** is the first flight path.
* **Vector B** is the second flight path.

Let's see what happens when we combine them using the **Tip-to-Tail** method!
""")
st.divider()

# --- Layout ---
col1, col2 = st.columns([1.5, 1])

# --- Controls (Column 2) ---
with col2:
    st.subheader("🎛️ Flight Controls")
    
    operation = st.radio("Select Operation:", ["Addition (A + B)", "Subtraction (A - B)"])
    
    st.markdown("**Set Vector A (First Leg):**")
    ax = st.slider("A x-component", -5, 5, 3, key="ax")
    ay = st.slider("A y-component", -5, 5, 4, key="ay")
    
    st.markdown("**Set Vector B (Second Leg):**")
    bx = st.slider("B x-component", -5, 5, 4, key="bx")
    by = st.slider("B y-component", -5, 5, -2, key="by")
    
    # Handle Subtraction logic (A - B is just A + (-B))
    if "Subtraction" in operation:
        calc_bx, calc_by = -bx, -by
        op_sign = "-"
        st.info("💡 **Subtraction Tip:** Subtracting a vector is the same as adding its opposite. Watch Vector B flip!")
    else:
        calc_bx, calc_by = bx, by
        op_sign = "+"

    st.markdown("---")
    st.subheader("⏱️ Simulation Timeline")
    st.markdown("Drag the slider to watch the **Tip-to-Tail** connection happen.")
    # The animation slider!
    time_step = st.slider("Scrub time to animate", 0.0, 1.0, 0.0, step=0.05)

    # Component-wise Math Display
    st.markdown("---")
    st.subheader("🧮 The Math (Component-wise)")
    st.markdown("The visual geometry perfectly matches the algebra. We just add (or subtract) the matching rows!")
    
    # Using Streamlit LaTeX for the matrix math
    latex_math = f"""
    \\begin{{bmatrix}} {ax} \\\\ {ay} \\end{{bmatrix}} 
    {op_sign} 
    \\begin{{bmatrix}} {bx} \\\\ {by} \\end{{bmatrix}} 
    = 
    \\begin{{bmatrix}} {ax + calc_bx} \\\\ {ay + calc_by} \\end{{bmatrix}}
    """
    st.latex(latex_math)

# --- Visualization (Column 1) ---
with col1:
    fig = go.Figure()

    # Base Grid / Origin marker
    fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=10, color='black'), name="Home Base"))

    # Vector A (Always starts at origin)
    fig.add_annotation(
        x=ax, y=ay, ax=0, ay=0,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=3, arrowcolor="blue"
    )
    # Label for Vector A
    fig.add_trace(go.Scatter(x=[ax/2], y=[ay/2], mode="text", text=["<b>Vector A</b>"], textfont=dict(color="blue", size=14), showlegend=False))

    # Vector B (Animation Logic)
    # Starts at origin, moves to tip of A based on 'time_step'
    start_x = 0 + (ax * time_step)
    start_y = 0 + (ay * time_step)
    end_x = start_x + calc_bx
    end_y = start_y + calc_by

    fig.add_annotation(
        x=end_x, y=end_y, ax=start_x, ay=start_y,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=3, arrowcolor="orange"
    )
    # Label for Vector B
    b_label = "<b>-Vector B</b>" if "Subtraction" in operation else "<b>Vector B</b>"
    fig.add_trace(go.Scatter(x=[start_x + calc_bx/2], y=[start_y + calc_by/2], mode="text", text=[b_label], textfont=dict(color="orange", size=14), showlegend=False))

    # Show the original Vector B faded if in subtraction mode
    if "Subtraction" in operation:
        fig.add_annotation(
            x=bx, y=by, ax=0, ay=0,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2, arrowcolor="rgba(255, 165, 0, 0.3)"
        )
        fig.add_trace(go.Scatter(x=[bx/2], y=[by/2], mode="text", text=["<b>Vector B</b>"], textfont=dict(color="rgba(255, 165, 0, 0.5)", size=14), showlegend=False))

    # Resultant Vector C (Only show when time_step is complete)
    if time_step == 1.0:
        fig.add_annotation(
            x=ax+calc_bx, y=ay+calc_by, ax=0, ay=0,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=4, arrowcolor="green"
        )
        fig.add_trace(go.Scatter(x=[(ax+calc_bx)/2], y=[(ay+calc_by)/2], mode="text", text=["<b>Resultant</b>"], textfont=dict(color="green", size=16), showlegend=False))
        
        # Add a dashed line to show component connection
        fig.add_trace(go.Scatter(
            x=[0, ax+calc_bx, ax+calc_bx], 
            y=[0, 0, ay+calc_by], 
            mode="lines", 
            line=dict(color="gray", width=2, dash="dot"),
            name="X/Y Components"
        ))

    # Graph Formatting
    fig.update_layout(
        title="Drone Radar (XY Coordinate Space)",
        xaxis=dict(range=[-10, 10], zeroline=True, zerolinewidth=2, zerolinecolor='black', gridcolor='lightgray', dtick=1),
        yaxis=dict(range=[-10, 10], zeroline=True, zerolinewidth=2, zerolinecolor='black', gridcolor='lightgray', dtick=1),
        width=700,
        height=700,
        plot_bgcolor="white",
        showlegend=False
    )

    # Force square aspect ratio so vectors don't look stretched
    fig.update_yaxes(scaleanchor="x", scaleratio=1)

    st.plotly_chart(fig, use_container_width=True)