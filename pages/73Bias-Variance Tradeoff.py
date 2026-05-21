import streamlit as st
import numpy as np
import plotly.graph_objects as go

def draw_dartboard(bias, variance, num_darts=30, seed_val=None, show_labels=True):
    """Draws a dartboard with darts scattered based on bias and variance."""
    if seed_val is not None:
        np.random.seed(seed_val)
        
    # Angle for the bias offset (fixed to top-right for consistent visualization)
    angle = np.pi / 4
    center_x = bias * np.cos(angle)
    center_y = bias * np.sin(angle)
    
    # Generate dart coordinates
    darts_x = np.random.normal(center_x, variance, num_darts)
    darts_y = np.random.normal(center_y, variance, num_darts)
    
    fig = go.Figure()
    
    # Dartboard colors and radii
    colors = ['#E74C3C', '#ECF0F1', '#E74C3C', '#ECF0F1', '#34495E']
    radii = [2, 4, 6, 8, 10]
    
    for radius, color in zip(reversed(radii), reversed(colors)):
        fig.add_shape(
            type="circle",
            x0=-radius, y0=-radius, x1=radius, y1=radius,
            fillcolor=color,
            line_color="#2C3E50",
            line_width=1 if color != '#34495E' else 3,
            opacity=1.0
        )
        
    # Bullseye
    fig.add_shape(
        type="circle",
        x0=-0.5, y0=-0.5, x1=0.5, y1=0.5,
        fillcolor="#F1C40F",
        line_color="#2C3E50",
        line_width=1
    )
    
    # True Target marker
    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode='markers',
        marker=dict(size=8, color='black', symbol='cross'),
        name='True Target',
        hoverinfo='name'
    ))
    
    # Darts
    fig.add_trace(go.Scatter(
        x=darts_x, y=darts_y,
        mode='markers',
        marker=dict(
            size=12,
            color='#2980B9',
            line=dict(width=2, color='white'),
            symbol='circle'
        ),
        name='Model Predictions',
        hoverinfo='none'
    ))
    
    if show_labels:
        # Bias arrow (from center to the center of the darts)
        if bias > 0.5:
            fig.add_annotation(
                x=center_x, y=center_y,
                ax=0, ay=0,
                xref='x', yref='y', axref='x', ayref='y',
                showarrow=True,
                arrowhead=2,
                arrowsize=1.5,
                arrowwidth=3,
                arrowcolor="#F39C12",
                opacity=0.9
            )
            fig.add_annotation(
                x=center_x/2, y=center_y/2,
                text="Bias",
                showarrow=False,
                font=dict(color="#F39C12", size=16, weight="bold"),
                xshift=-25, yshift=25
            )

        # Variance circle (indicating the spread)
        fig.add_shape(
            type="circle",
            x0=center_x - variance*1.5, y0=center_y - variance*1.5,
            x1=center_x + variance*1.5, y1=center_y + variance*1.5,
            fillcolor="rgba(0,0,0,0)",
            line_color="#3498DB",
            line_width=3,
            line_dash="dot",
            opacity=0.8
        )
        fig.add_annotation(
            x=center_x, y=center_y + variance*1.5,
            text="Variance",
            showarrow=False,
            font=dict(color="#3498DB", size=16, weight="bold"),
            yshift=15
        )

    fig.update_layout(
        xaxis=dict(range=[-13, 13], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[-13, 13], showgrid=False, zeroline=False, showticklabels=False),
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    
    return fig

def draw_tradeoff_curve(complexity):
    """Draws the Bias-Variance tradeoff curve."""
    x = np.linspace(1, 10, 200)
    
    # Simulated values for pedagogical purposes
    bias = 80 * np.exp(-0.6 * (x - 1))
    variance = 1.0 * ((x - 1) ** 2)
    total_error = bias + variance + 10 # 10 is irreducible error
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x, y=bias, mode='lines', 
        name='Bias² (Assumptions)', 
        line=dict(color='#E74C3C', width=4)
    ))
    
    fig.add_trace(go.Scatter(
        x=x, y=variance, mode='lines', 
        name='Variance (Sensitivity)', 
        line=dict(color='#3498DB', width=4)
    ))
    
    fig.add_trace(go.Scatter(
        x=x, y=total_error, mode='lines', 
        name='Total Error', 
        line=dict(color='#9B59B6', width=5, dash='dash')
    ))
    
    # Calculate current values based on slider
    curr_bias = 80 * np.exp(-0.6 * (complexity - 1))
    curr_var = 1.0 * ((complexity - 1) ** 2)
    curr_total = curr_bias + curr_var + 10
    
    # Vertical line indicating current position
    fig.add_shape(
        type="line", 
        x0=complexity, y0=0, x1=complexity, y1=100, 
        line=dict(color="white", width=2, dash="dot")
    )
    
    # Markers for current values
    fig.add_trace(go.Scatter(
        x=[complexity]*3, 
        y=[curr_bias, curr_var, curr_total], 
        mode='markers', 
        marker=dict(size=14, color=['#E74C3C', '#3498DB', '#9B59B6'], line=dict(width=2, color='white')),
        showlegend=False
    ))
    
    # Highlight the sweet spot
    sweet_spot = x[np.argmin(total_error)]
    min_error = np.min(total_error)
    
    fig.add_shape(
        type="rect", 
        x0=sweet_spot-0.5, y0=0, x1=sweet_spot+0.5, y1=100, 
        fillcolor="#F1C40F", opacity=0.15, line_width=0, layer="below"
    )
    
    fig.add_annotation(
        x=sweet_spot, y=min_error - 5,
        text="✨ Sweet Spot ✨",
        showarrow=False,
        font=dict(color="#F1C40F", size=14, weight="bold")
    )
    
    # Descriptive zone labels
    fig.add_annotation(x=2.5, y=90, text="⬅️ UNDERFITTING", showarrow=False, font=dict(color="#E74C3C", size=14, weight="bold"), opacity=0.7)
    fig.add_annotation(x=8.5, y=90, text="OVERFITTING ➡️", showarrow=False, font=dict(color="#3498DB", size=14, weight="bold"), opacity=0.7)
    
    fig.update_layout(
        xaxis_title="<b>Model Complexity</b> ➔",
        yaxis_title="<b>Error</b> ➔",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0.5, 10.5]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 100]),
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="center", x=0.5
        )
    )
    
    return fig

# --- Main App Execution ---

st.title("🎯 The Bias-Variance Tradeoff")
st.markdown("### Why finding the perfect machine learning model is like playing darts.")

with st.expander("📖 What are Bias and Variance? (Read First!)", expanded=False):
    st.markdown("""
    When we train an AI model, it tries to learn the patterns in our data. But it faces two main enemies:
    
    *   **<span style='color:#E74C3C; font-weight:bold;'>Bias</span> (The "Inaccurate" Error):** The model makes strong assumptions and is too simple. It consistently misses the mark because it didn't learn enough from the data. (Think: **Underfitting**)
    *   **<span style='color:#3498DB; font-weight:bold;'>Variance</span> (The "Inconsistent" Error):** The model is too complex and sensitive. It memorizes the training data perfectly, including the random noise, so its predictions jump all over the place on new data. (Think: **Overfitting**)
    
    Our goal is to find the **sweet spot** in between!
    """, unsafe_allow_html=True)

st.markdown("---")

# Use tabs to organize the experience logically
tab1, tab2 = st.tabs(["🕹️ The Dartboard Analogy", "⚖️ The Tradeoff Curve"])

with tab1:
    st.markdown("Imagine you are throwing darts at a board. The **bullseye is the true correct answer**. Your darts are the **model's predictions**.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Adjust Your Throw")
        bias_val = st.slider("🎯 Bias (How far off-center?)", min_value=0.0, max_value=12.0, value=7.0, step=0.5, 
                             help="Higher bias means the darts are consistently missing the bullseye.")
        var_val = st.slider("🌪️ Variance (How spread out?)", min_value=0.1, max_value=8.0, value=1.5, step=0.1,
                            help="Higher variance means the darts are scattered everywhere.")
        
        if st.button("🎲 Throw New Darts!", use_container_width=True):
            st.session_state.dart_seed = np.random.randint(0, 100000)
            
        st.markdown("---")
        
        # Analysis box based on user input
        if bias_val < 3.5 and var_val < 2.5:
            st.success("**🎯 Ideal Model!** \n\nLow Bias, Low Variance. You are hitting the bullseye consistently.")
        elif bias_val >= 3.5 and var_val < 2.5:
            st.error("**🧱 High Bias, Low Variance!** \n\nYou are consistently wrong. The model is too simple (**Underfitting**).")
        elif bias_val < 3.5 and var_val >= 2.5:
            st.warning("**🌪️ Low Bias, High Variance!** \n\nYou are scattered around the bullseye. The model is too sensitive to noise (**Overfitting**).")
        else:
            st.error("**💥 High Bias, High Variance!** \n\nYou are consistently wrong AND scattered. Back to the drawing board!")
            
    with col2:
        seed = st.session_state.get('dart_seed', 42)
        fig1 = draw_dartboard(bias_val, var_val, seed_val=seed)
        st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.markdown("In real life, you can't just set Bias and Variance independently. As you make a model more complex (adding more layers, fitting higher polynomials), **Bias decreases but Variance increases**.")
    
    complexity = st.slider("⚙️ Model Complexity", min_value=1.0, max_value=10.0, value=5.0, step=0.1,
                           help="1 = Very Simple (e.g., straight line). 10 = Very Complex (e.g., squiggly polynomial).")
    
    col3, col4 = st.columns([2, 1.2])
    
    with col3:
        fig2 = draw_tradeoff_curve(complexity)
        st.plotly_chart(fig2, use_container_width=True)
        
    with col4:
        st.markdown(f"#### Dartboard at Complexity {complexity:.1f}")
        
        # Map complexity to bias and variance for visual effect on the mini dartboard
        mapped_bias = 10 * np.exp(-0.5 * (complexity - 1))
        mapped_var = 0.5 + 0.08 * ((complexity - 1) ** 2)
        
        bias_label = "High" if mapped_bias > 4 else "Medium" if mapped_bias > 2 else "Low"
        var_label = "High" if mapped_var > 4 else "Medium" if mapped_var > 2 else "Low"
        
        st.markdown(f"- **Bias:** {bias_label} ({mapped_bias:.1f})")
        st.markdown(f"- **Variance:** {var_label} ({mapped_var:.1f})")
        
        # Draw a mini dartboard without labels for a cleaner look
        fig3 = draw_dartboard(mapped_bias, mapped_var, num_darts=15, seed_val=42, show_labels=False)
        st.plotly_chart(fig3, use_container_width=True)