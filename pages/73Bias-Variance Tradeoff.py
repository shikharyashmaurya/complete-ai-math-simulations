import sys
from pathlib import Path

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="Bias-Variance Tradeoff", page_icon="🎯", layout="wide")

NOISE = 10  # irreducible error in the illustrative tradeoff curve


def curve_bias_sq(c):
    return 80 * np.exp(-0.6 * (c - 1))


def curve_variance(c):
    return 1.0 * ((c - 1) ** 2)


def draw_dartboard(bias, variance, num_darts=30, seed_val=None, show_labels=True):
    """Draws a dartboard with darts scattered based on bias (distance) and per-axis variance.

    Returns the figure and the dart coordinates.
    """
    rng = np.random.default_rng(seed_val)
        
    # Angle for the bias offset (fixed to top-right for consistent visualization)
    angle = np.pi / 4
    center_x = bias * np.cos(angle)
    center_y = bias * np.sin(angle)
    std_dev = np.sqrt(variance)
    
    # Generate dart coordinates
    darts_x = rng.normal(center_x, std_dev, num_darts)
    darts_y = rng.normal(center_y, std_dev, num_darts)
    
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
            x0=center_x - std_dev*1.5, y0=center_y - std_dev*1.5,
            x1=center_x + std_dev*1.5, y1=center_y + std_dev*1.5,
            fillcolor="rgba(0,0,0,0)",
            line_color="#3498DB",
            line_width=3,
            line_dash="dot",
            opacity=0.8
        )
        fig.add_annotation(
            x=center_x, y=center_y + std_dev*1.5,
            text="Variance",
            showarrow=False,
            font=dict(color="#3498DB", size=16, weight="bold"),
            yshift=15
        )

    board_limit = max(13, 10, abs(center_x) + 3 * std_dev, abs(center_y) + 3 * std_dev, float(np.max(np.abs(darts_x))) + 1, float(np.max(np.abs(darts_y))) + 1)
    fig.update_layout(
        xaxis=dict(range=[-board_limit, board_limit], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[-board_limit, board_limit], showgrid=False, zeroline=False, showticklabels=False),
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    
    return fig, darts_x, darts_y

def draw_tradeoff_curve(complexity):
    """Draws the Bias-Variance tradeoff curve."""
    x = np.linspace(1, 10, 200)
    
    # Simulated values for pedagogical purposes: Expected error = Bias² + Variance + Noise
    bias_sq = curve_bias_sq(x)
    variance = curve_variance(x)
    total_error = bias_sq + variance + NOISE
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x, y=bias_sq, mode='lines', 
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
        name='Total Error (Bias² + Variance + Noise)', 
        line=dict(color='#9B59B6', width=5, dash='dash')
    ))
    
    # Calculate current values based on slider
    curr_bias = curve_bias_sq(complexity)
    curr_var = curve_variance(complexity)
    curr_total = curr_bias + curr_var + NOISE
    
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
    
    *   **<span style='color:#E74C3C; font-weight:bold;'>Bias</span> (The "Inaccurate" Error):** The model makes strong assumptions and is too simple. It consistently misses the mark in the same direction, no matter which training data it sees. (Think: **Underfitting**)
    *   **<span style='color:#3498DB; font-weight:bold;'>Variance</span> (The "Inconsistent" Error):** The model is very flexible and sensitive. It can fit the random noise in its particular training set, so retraining it on a different sample of data gives noticeably different predictions. (Think: **Overfitting**)
    
    For squared error, the expected error splits exactly into **Bias² + Variance + Irreducible Noise**.
    Our goal is to find the **sweet spot** where their sum is smallest!
    """, unsafe_allow_html=True)

st.markdown("---")

# Use tabs to organize the experience logically
tab1, tab2 = st.tabs(["🕹️ The Dartboard Analogy", "⚖️ The Tradeoff Curve"])

with tab1:
    st.markdown("Imagine you are throwing darts at a board. The **bullseye is the true answer** for one fixed input. "
                "Each dart is the prediction for that input from the same kind of model **trained on a different random training set**. "
                "Bias is how far the *average* dart lands from the bullseye; variance is how much the darts scatter around their own average.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Adjust Your Throw")
        bias_val = st.slider("🎯 Bias (How far off-center?)", min_value=0.0, max_value=12.0, value=7.0, step=0.5, key="p73_bias",
                             help="Distance from the bullseye to the center of the dart cloud. Higher bias means the darts are consistently missing the bullseye.")
        var_val = st.slider("🌪️ Variance (How spread out?)", min_value=0.1, max_value=8.0, value=1.5, step=0.1, key="p73_variance",
                            help="Variance of the darts along each axis. Higher variance means the darts are scattered everywhere.")
        
        if st.button("🎲 Throw New Darts!", width="stretch", key="p73_throw"):
            st.session_state.p73_dart_seed = int(np.random.default_rng().integers(0, 100000))
            
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
        seed = st.session_state.get('p73_dart_seed', 42)
        fig1, darts_x, darts_y = draw_dartboard(bias_val, var_val, seed_val=seed)
        st.plotly_chart(fig1, width="stretch")

        # Measured decomposition for the darts actually thrown:
        # mean squared miss = (distance of the dart average from the bullseye)² + mean squared spread around that average
        mean_sq_miss = float(np.mean(darts_x**2 + darts_y**2))
        measured_bias_sq = float(np.mean(darts_x)**2 + np.mean(darts_y)**2)
        measured_spread = float(np.mean((darts_x - np.mean(darts_x))**2 + (darts_y - np.mean(darts_y))**2))
        m1, m2, m3 = st.columns(3)
        m1.metric("Avg squared miss", f"{mean_sq_miss:.2f}")
        m2.metric("Measured Bias²", f"{measured_bias_sq:.2f}")
        m3.metric("Measured Variance (spread)", f"{measured_spread:.2f}")
        st.caption(f"Avg squared miss = Measured Bias² + Measured Variance, exactly, for these {darts_x.size} darts. In expectation it is "
                   f"Bias² + 2 × per-axis variance = {bias_val**2:.2f} + {2 * var_val:.2f} = {bias_val**2 + 2 * var_val:.2f} "
                   "(two axes on a 2-D board).")

with tab2:
    st.markdown("In many model-selection settings, increasing complexity tends to reduce bias while increasing variance, but this is a common tradeoff—not a universal law or a strict rule that the two must change together. The curve below is illustrative.")
    
    complexity = st.slider("⚙️ Model Complexity", min_value=1.0, max_value=10.0, value=5.0, step=0.1, key="p73_complexity",
                           help="1 = Very Simple (e.g., straight line). 10 = Very Complex (e.g., squiggly polynomial).")
    
    col3, col4 = st.columns([2, 1.2])
    
    with col3:
        fig2 = draw_tradeoff_curve(complexity)
        st.plotly_chart(fig2, width="stretch")
        
    with col4:
        st.markdown(f"#### Dartboard at Complexity {complexity:.1f}")
        
        # Use the SAME values as the curve: the mean squared miss of the darts is Bias² + Variance,
        # so the dart-cloud offset is sqrt(Bias²) and the per-axis variance is Variance / 2 (two axes).
        curr_bias_sq = float(curve_bias_sq(complexity))
        curr_var = float(curve_variance(complexity))
        x_grid = np.linspace(1, 10, 200)
        sweet_spot = float(x_grid[np.argmin(curve_bias_sq(x_grid) + curve_variance(x_grid))])
        
        st.markdown(f"- **Bias²:** {curr_bias_sq:.1f}")
        st.markdown(f"- **Variance:** {curr_var:.1f}")
        st.markdown(f"- **Noise:** {NOISE} → **Total:** {curr_bias_sq + curr_var + NOISE:.1f}")
        if abs(complexity - sweet_spot) <= 0.5:
            st.success(f"Near the sweet spot (≈ {sweet_spot:.1f}): Bias² and Variance are balanced.")
        elif complexity < sweet_spot:
            st.error("Underfitting side: **Bias²** dominates the error.")
        else:
            st.warning("Overfitting side: **Variance** dominates the error.")
        
        # Draw a mini dartboard without labels for a cleaner look
        fig3, _, _ = draw_dartboard(np.sqrt(curr_bias_sq), curr_var / 2, num_darts=15, seed_val=42, show_labels=False)
        st.plotly_chart(fig3, width="stretch")

st.divider()
prev_col, next_col = st.columns(2)
with prev_col:
    safe_page_link("pages/72Train, Validation & Test Splits.py", "Previous: 72 · Train, Validation & Test Splits", icon="⬅️")
with next_col:
    safe_page_link("pages/74L1 & L2 Regularization.py", "Next: 74 · L1 & L2 Regularization", icon="➡️")