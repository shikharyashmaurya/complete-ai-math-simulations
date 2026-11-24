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
    
    operation = st.radio("Select Operation:", ["Addition (A + B)", "Subtraction (A - B)"], key="p02_operation")
    
    st.markdown("**Set Vector A (First Leg):**")
    ax = st.slider("A x-component", -5, 5, 3, key="p02_ax")
    ay = st.slider("A y-component", -5, 5, 4, key="p02_ay")
    
    st.markdown("**Set Vector B (Second Leg):**")
    bx = st.slider("B x-component", -5, 5, 4, key="p02_bx")
    by = st.slider("B y-component", -5, 5, -2, key="p02_by")
    
    # Handle Subtraction logic (A - B is just A + (-B))
    if "Subtraction" in operation:
        calc_bx, calc_by = -bx, -by
        op_sign = "-"
        st.info("💡 **Subtraction Tip:** Subtracting a vector is the same as adding its opposite. Watch Vector B flip! "
                "At the end of the timeline you will also see the second picture: A - B is the arrow from the tip of B to the tip of A.")
    else:
        calc_bx, calc_by = bx, by
        op_sign = "+"

    st.markdown("---")
    st.subheader("⏱️ Simulation Timeline")
    st.markdown("Drag the slider to watch the **Tip-to-Tail** connection happen.")
    # The animation slider!
    time_step = st.slider("Scrub time to animate", 0.0, 1.0, 0.0, step=0.05, key="p02_time_step")

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
    if time_step >= 1.0 - 1e-9:
        res_x, res_y = ax + calc_bx, ay + calc_by
        if res_x != 0 or res_y != 0:
            fig.add_annotation(
                x=res_x, y=res_y, ax=0, ay=0,
                xref="x", yref="y", axref="x", ayref="y",
                showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=4, arrowcolor="green"
            )
            fig.add_trace(go.Scatter(x=[res_x/2], y=[res_y/2], mode="text", text=["<b>Resultant</b>"], textfont=dict(color="green", size=16), showlegend=False))
        else:
            # A zero-length arrow has no direction, so mark the origin instead of drawing a stray arrowhead
            fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers+text", marker=dict(size=16, color="green", symbol="circle-open"),
                                     text=["<b>Resultant = zero vector</b>"], textposition="bottom center",
                                     textfont=dict(color="green", size=14), showlegend=False))

        # Add a dashed line to show component connection
        fig.add_trace(go.Scatter(
            x=[0, res_x, res_x], 
            y=[0, 0, res_y], 
            mode="lines", 
            line=dict(color="gray", width=2, dash="dot"),
            name="X/Y Components"
        ))

        # Second picture of subtraction: A - B is also the arrow from the tip of B to the tip of A
        if "Subtraction" in operation and (res_x != 0 or res_y != 0):
            fig.add_annotation(
                x=ax, y=ay, ax=bx, ay=by,
                xref="x", yref="y", axref="x", ayref="y",
                showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=2, arrowcolor="rgba(0, 128, 0, 0.45)"
            )
            fig.add_trace(go.Scatter(x=[(ax + bx) / 2], y=[(ay + by) / 2], mode="text",
                                     text=["A - B (tip of B → tip of A)"],
                                     textfont=dict(color="rgba(0, 128, 0, 0.7)", size=12), showlegend=False))

    # Graph Formatting
    fig.update_layout(
        title="Drone Radar (XY Coordinate Space)",
        xaxis=dict(range=[-10, 10], zeroline=True, zerolinewidth=2, zerolinecolor='black', gridcolor='lightgray', dtick=1),
        yaxis=dict(range=[-10, 10], zeroline=True, zerolinewidth=2, zerolinecolor='black', gridcolor='lightgray', dtick=1),
        height=700,
        plot_bgcolor="white",
        showlegend=False
    )

    # Force square aspect ratio so vectors don't look stretched
    fig.update_yaxes(scaleanchor="x", scaleratio=1)

    st.plotly_chart(fig, width="stretch")