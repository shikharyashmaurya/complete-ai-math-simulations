import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math

# Page setup
st.set_page_config(
    page_title="65: Activation Functions Compared - Curves & Derivatives",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Cyberpunk & Glassmorphic CSS Styling
st.markdown("""
<style>
    /* Dark Theme Base Adjustments */
    .stApp {
        background: #0b0f19 !important;
        color: #f1f5f9 !important;
    }
    
    /* Target standard Streamlit text elements for high contrast */
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: #cbd5e1 !important;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #f8fafc !important;
    }
    
    /* Premium Tab Styling */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        border-bottom: 2px solid transparent !important;
    }
    button[data-baseweb="tab"] p {
        color: #94a3b8 !important;
        font-size: 1.05rem !important;
        transition: color 0.2s ease, font-weight 0.2s ease !important;
    }
    button[data-baseweb="tab"]:hover p {
        color: #f8fafc !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        border-bottom-color: #38bdf8 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #38bdf8 !important;
        font-weight: bold !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"], [data-testid="stSidebar"] div, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        background-color: #0d1321 !important;
        color: #cbd5e1 !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 {
        color: #38bdf8 !important;
    }
    
    /* Custom Card Styling */
    .custom-card {
        background: rgba(17, 24, 39, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(12px);
    }
    
    .custom-card, .custom-card p, .custom-card li, .custom-card span {
        color: #cbd5e1 !important;
    }
    
    .custom-card h1, .custom-card h2, .custom-card h3, .custom-card h4, .custom-card h5, .custom-card h6 {
        color: #f8fafc !important;
    }
    
    .card-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 12px;
        color: #38bdf8 !important;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Highlights */
    .cyan-highlight {
        background: rgba(6, 182, 212, 0.18) !important;
        color: #22d3ee !important;
        padding: 2px 8px;
        border-radius: 4px;
        font-family: monospace;
        font-weight: bold;
    }
    
    .pink-highlight {
        background: rgba(236, 72, 153, 0.18) !important;
        color: #f472b6 !important;
        padding: 2px 8px;
        border-radius: 4px;
        font-family: monospace;
        font-weight: bold;
    }
    
    .green-highlight {
        background: rgba(34, 197, 94, 0.18) !important;
        color: #4ade80 !important;
        padding: 2px 8px;
        border-radius: 4px;
        font-family: monospace;
        font-weight: bold;
    }

    .amber-highlight {
        background: rgba(245, 158, 11, 0.18) !important;
        color: #fbbf24 !important;
        padding: 2px 8px;
        border-radius: 4px;
        font-family: monospace;
        font-weight: bold;
    }
    
    /* Glow Badges */
    .glow-badge-cyan {
        background: linear-gradient(135deg, #0891b2 0%, #0e7490 100%);
        color: #0b0f19 !important;
        font-weight: 800;
        padding: 6px 12px;
        border-radius: 30px;
        box-shadow: 0 0 15px rgba(6, 182, 212, 0.4);
        display: inline-block;
    }
    
    .glow-badge-pink {
        background: linear-gradient(135deg, #db2777 0%, #be185d 100%);
        color: #0b0f19 !important;
        font-weight: 800;
        padding: 6px 12px;
        border-radius: 30px;
        box-shadow: 0 0 15px rgba(236, 72, 153, 0.4);
        display: inline-block;
    }
    
    .glow-badge-green {
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
        color: #0b0f19 !important;
        font-weight: 800;
        padding: 6px 12px;
        border-radius: 30px;
        box-shadow: 0 0 15px rgba(34, 197, 94, 0.4);
        display: inline-block;
    }

    .glow-badge-amber {
        background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
        color: #0b0f19 !important;
        font-weight: 800;
        padding: 6px 12px;
        border-radius: 30px;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.4);
        display: inline-block;
    }
    
    /* Premium Button Styling */
    div.stButton > button {
        background-color: #1e293b !important;
        color: #38bdf8 !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2) !important;
    }
    
    div.stButton > button:hover {
        background-color: #38bdf8 !important;
        color: #0b0f19 !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.4) !important;
        transform: translateY(-2px) !important;
    }
</style>
""", unsafe_allow_html=True)


# Mathematical Functions & Derivatives
def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -20.0, 20.0)))

def sigmoid_derivative(z):
    s = sigmoid(z)
    return s * (1.0 - s)

def tanh_val(z):
    return np.tanh(z)

def tanh_derivative(z):
    return 1.0 - np.tanh(z)**2

def relu(z):
    return np.maximum(0.0, z)

def relu_derivative(z):
    return np.where(z > 0.0, 1.0, 0.0)

def leaky_relu(z, alpha=0.1):
    return np.where(z > 0.0, z, alpha * z)

def leaky_relu_derivative(z, alpha=0.1):
    return np.where(z > 0.0, 1.0, alpha)


# Initializing Session State variables if not present
if "global_z" not in st.session_state:
    st.session_state.global_z = 1.0
if "backprop_act" not in st.session_state:
    st.session_state.backprop_act = "Sigmoid"
if "z_lock" not in st.session_state:
    st.session_state.z_lock = True
if "z1" not in st.session_state:
    st.session_state.z1 = 2.0
if "z2" not in st.session_state:
    st.session_state.z2 = 2.0
if "z3" not in st.session_state:
    st.session_state.z3 = 2.0
if "grad_init" not in st.session_state:
    st.session_state.grad_init = 10.0

# Dynamic callbacks to set presets
def set_preset_z(val):
    st.session_state.global_z = val

# Sidebar configuration
st.sidebar.markdown("""
<div style="text-align: center; padding-bottom: 10px;">
    <h2 style="color: #38bdf8; margin-bottom: 0;">🔬 Activation Controls</h2>
    <p style="color: #94a3b8; font-size: 0.9rem;">Interact with the Mathematical Models</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 🎚️ Global Probe ($z$)")
st.sidebar.caption("Shift the active input coordinate to examine exactly how each activation function and its gradient behaves.")

global_z = st.sidebar.slider(
    "Coordinate Probe Value (z)", 
    min_value=-6.0, 
    max_value=6.0, 
    value=st.session_state.global_z, 
    step=0.1,
    key="global_z"
)

st.sidebar.markdown("##### 📍 Quick Presets")
preset_cols = st.sidebar.columns(2)
with preset_cols[0]:
    st.button("Zero Center (z=0)", on_click=set_preset_z, args=(0.0,), use_container_width=True)
    st.button("Active Positive (z=2)", on_click=set_preset_z, args=(2.0,), use_container_width=True)
with preset_cols[1]:
    st.button("Deep Saturation (z=5)", on_click=set_preset_z, args=(5.0,), use_container_width=True)
    st.button("Deep Negative (z=-3)", on_click=set_preset_z, args=(-3.0,), use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Tab 2: Wave Sandbox")
wave_type = st.sidebar.selectbox(
    "Input Signal Shape",
    options=["Sine Wave", "Square Wave", "Triangle Wave", "Random Noise"],
    index=0
)
wave_freq = st.sidebar.slider("Signal Frequency", min_value=1, max_value=5, value=2, step=1)
wave_amp = st.sidebar.slider("Signal Amplitude", min_value=1.0, max_value=4.0, value=2.0, step=0.5)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏃‍♂️ Tab 3: Backprop Race")
backprop_act = st.sidebar.selectbox(
    "Test Activation Engine",
    options=["Sigmoid", "tanh", "ReLU", "Leaky ReLU"],
    index=["Sigmoid", "tanh", "ReLU", "Leaky ReLU"].index(st.session_state.backprop_act),
    key="backprop_act"
)

grad_init = st.sidebar.slider(
    "Starting Gradient (Error)",
    min_value=1.0,
    max_value=20.0,
    value=st.session_state.grad_init,
    step=1.0,
    key="grad_init"
)

z_lock = st.sidebar.checkbox(
    "Lock Inputs (z₁ = z₂ = z₃)",
    value=st.session_state.z_lock,
    key="z_lock",
    help="Locks input z values for all layers to see compounding effects easily."
)

if z_lock:
    z1_val = st.sidebar.slider("Common Input z", min_value=-5.0, max_value=5.0, value=2.0, step=0.5)
    z1 = z1_val
    z2 = z1_val
    z3 = z1_val
else:
    z1 = st.sidebar.slider("Layer 1 Input (z₁)", min_value=-5.0, max_value=5.0, value=st.session_state.z1, step=0.5, key="z1")
    z2 = st.sidebar.slider("Layer 2 Input (z₂)", min_value=-5.0, max_value=5.0, value=st.session_state.z2, step=0.5, key="z2")
    z3 = st.sidebar.slider("Layer 3 Input (z₃)", min_value=-5.0, max_value=5.0, value=st.session_state.z3, step=0.5, key="z3")

# Main Header Area
st.title("Page 65: Activation Functions Compared")
st.subheader("Sigmoid, tanh, ReLU, and Leaky ReLU | Curves, Derivatives, and Gradient Flow 🔬")

st.markdown(
    """
    <div class="custom-card">
        <h3>👋 The Non-Linear Engine of Deep Learning</h3>
        <p style="font-size: 1.1rem; line-height: 1.6; color: #cbd5e1; margin-bottom: 12px;">
            In our last lesson, we built a single neuron. But did you notice something? 
            Without an activation function, stacking millions of neurons is just multiplying linear numbers. 
            Mathematically, a 100-layer network of pure linear maps is completely equivalent to a single linear equation: 
            <span class="cyan-highlight">y = Wx + b</span>. It has zero "bendability"!
        </p>
        <p style="font-size: 1.05rem; line-height: 1.6; color: #cbd5e1; margin-bottom: 0;">
            Activation functions are the mathematical <b>warping engines</b> of AI. They introduce <b>non-linearity</b>, 
            allowing the network to bend, twist, and sculpt high-dimensional space to fit extremely complex data (like faces, voices, and text). 
            Equally important are their <b>derivatives (gradients)</b>. The derivative controls how fast our network can learn 
            during backpropagation. Let's compare the champions of deep learning side by side!
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Core Tabs Setup
tab_arena, tab_sandbox, tab_backprop = st.tabs([
    "📊 Tab 1: The Activation Arena", 
    "🌊 Tab 2: The Signal Sandbox", 
    "🏎️ Tab 3: The Great Backprop Race"
])

# ==========================================
# TAB 1: THE ACTIVATION ARENA
# ==========================================
with tab_arena:
    st.markdown("""
    <div style="margin-top: 15px; margin-bottom: 20px;">
        <p style="color: #cbd5e1; font-size: 1.05rem;">
            Below, we compare the activation profiles ($f(z)$) and their respective derivative profiles ($f'(z)$) side-by-side. 
            Adjust the <b>Global Probe slider ($z$)</b> in the sidebar to scan along the curves and watch the live coordinate values update!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate graphing data
    z_arr = np.linspace(-6.0, 6.0, 300)
    
    # Precompute outputs
    y_sig = sigmoid(z_arr)
    y_tanh = tanh_val(z_arr)
    y_relu = relu(z_arr)
    y_leaky = leaky_relu(z_arr)
    
    d_sig = sigmoid_derivative(z_arr)
    d_tanh = tanh_derivative(z_arr)
    d_relu = relu_derivative(z_arr)
    d_leaky = leaky_relu_derivative(z_arr)
    
    # Live values at probe z
    p_sig = sigmoid(global_z)
    p_tanh = tanh_val(global_z)
    p_relu = relu(global_z)
    p_leaky = leaky_relu(global_z)
    
    dp_sig = sigmoid_derivative(global_z)
    dp_tanh = tanh_derivative(global_z)
    dp_relu = relu_derivative(global_z)
    dp_leaky = leaky_relu_derivative(global_z)
    
    col_chart1, col_chart2 = st.columns(2, gap="medium")
    
    # Plot 1: Activation Functions
    with col_chart1:
        fig_act = go.Figure()
        
        # Add function traces
        fig_act.add_trace(go.Scatter(x=z_arr, y=y_sig, name="Sigmoid", line=dict(color="#06b6d4", width=3)))
        fig_act.add_trace(go.Scatter(x=z_arr, y=y_tanh, name="tanh", line=dict(color="#ec4899", width=3)))
        fig_act.add_trace(go.Scatter(x=z_arr, y=y_relu, name="ReLU", line=dict(color="#22c55e", width=3)))
        fig_act.add_trace(go.Scatter(x=z_arr, y=y_leaky, name="Leaky ReLU", line=dict(color="#f59e0b", width=3, dash="dash")))
        
        # Vertical reference line at global_z
        fig_act.add_shape(
            type="line", x0=global_z, y0=-2.0, x1=global_z, y1=6.0,
            line=dict(color="#f8fafc", width=1.5, dash="dot")
        )
        
        # Marker dots at probe coordinate
        fig_act.add_trace(go.Scatter(x=[global_z], y=[p_sig], mode="markers", marker=dict(color="#06b6d4", size=10, line=dict(color="#ffffff", width=1.5)), showlegend=False))
        fig_act.add_trace(go.Scatter(x=[global_z], y=[p_tanh], mode="markers", marker=dict(color="#ec4899", size=10, line=dict(color="#ffffff", width=1.5)), showlegend=False))
        fig_act.add_trace(go.Scatter(x=[global_z], y=[p_relu], mode="markers", marker=dict(color="#22c55e", size=10, line=dict(color="#ffffff", width=1.5)), showlegend=False))
        fig_act.add_trace(go.Scatter(x=[global_z], y=[p_leaky], mode="markers", marker=dict(color="#f59e0b", size=10, line=dict(color="#ffffff", width=1.5)), showlegend=False))
        
        fig_act.update_layout(
            title=dict(text="<b>Activation Functions</b> <i>f(z)</i>", font=dict(color="#f8fafc", size=16)),
            xaxis_title="Input Neuron Activation Score (z)",
            yaxis_title="Output Score a = f(z)",
            template="plotly_dark",
            plot_bgcolor="#0d1321",
            paper_bgcolor="#070a13",
            hovermode="x unified",
            xaxis=dict(range=[-6.0, 6.0], showgrid=True, gridcolor="rgba(255,255,255,0.05)", zeroline=True, zerolinecolor="rgba(255,255,255,0.15)"),
            yaxis=dict(range=[-2.1, 5.1], showgrid=True, gridcolor="rgba(255,255,255,0.05)", zeroline=True, zerolinecolor="rgba(255,255,255,0.15)"),
            margin=dict(l=40, r=20, t=50, b=40),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(13,19,33,0.7)")
        )
        st.plotly_chart(fig_act, use_container_width=True)

    # Plot 2: Derivative Functions
    with col_chart2:
        fig_deriv = go.Figure()
        
        # Add derivative traces
        fig_deriv.add_trace(go.Scatter(x=z_arr, y=d_sig, name="Sigmoid Derivative", line=dict(color="#06b6d4", width=3)))
        fig_deriv.add_trace(go.Scatter(x=z_arr, y=d_tanh, name="tanh Derivative", line=dict(color="#ec4899", width=3)))
        fig_deriv.add_trace(go.Scatter(x=z_arr, y=d_relu, name="ReLU Derivative", line=dict(color="#22c55e", width=3)))
        fig_deriv.add_trace(go.Scatter(x=z_arr, y=d_leaky, name="Leaky ReLU Derivative", line=dict(color="#f59e0b", width=3, dash="dash")))
        
        # Vertical reference line at global_z
        fig_deriv.add_shape(
            type="line", x0=global_z, y0=-0.1, x1=global_z, y1=1.2,
            line=dict(color="#f8fafc", width=1.5, dash="dot")
        )
        
        # Marker dots at probe coordinate
        fig_deriv.add_trace(go.Scatter(x=[global_z], y=[dp_sig], mode="markers", marker=dict(color="#06b6d4", size=10, line=dict(color="#ffffff", width=1.5)), showlegend=False))
        fig_deriv.add_trace(go.Scatter(x=[global_z], y=[dp_tanh], mode="markers", marker=dict(color="#ec4899", size=10, line=dict(color="#ffffff", width=1.5)), showlegend=False))
        fig_deriv.add_trace(go.Scatter(x=[global_z], y=[dp_relu], mode="markers", marker=dict(color="#22c55e", size=10, line=dict(color="#ffffff", width=1.5)), showlegend=False))
        fig_deriv.add_trace(go.Scatter(x=[global_z], y=[dp_leaky], mode="markers", marker=dict(color="#f59e0b", size=10, line=dict(color="#ffffff", width=1.5)), showlegend=False))
        
        fig_deriv.update_layout(
            title=dict(text="<b>Derivative Functions (Gradients)</b> <i>f'(z)</i>", font=dict(color="#f8fafc", size=16)),
            xaxis_title="Input Neuron Activation Score (z)",
            yaxis_title="Gradient Strength f'(z)",
            template="plotly_dark",
            plot_bgcolor="#0d1321",
            paper_bgcolor="#070a13",
            hovermode="x unified",
            xaxis=dict(range=[-6.0, 6.0], showgrid=True, gridcolor="rgba(255,255,255,0.05)", zeroline=True, zerolinecolor="rgba(255,255,255,0.15)"),
            yaxis=dict(range=[-0.15, 1.15], showgrid=True, gridcolor="rgba(255,255,255,0.05)", zeroline=True, zerolinecolor="rgba(255,255,255,0.15)"),
            margin=dict(l=40, r=20, t=50, b=40),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(13,19,33,0.7)")
        )
        st.plotly_chart(fig_deriv, use_container_width=True)

    # Live Mathematical Verification Cards
    st.markdown("### 🎚️ Live Probe Calculations at $z = %.2f$" % global_z)
    
    col_sig_card, col_tanh_card, col_relu_card, col_leaky_card = st.columns(4)
    
    with col_sig_card:
        st.markdown(f"""
        <div class="custom-card" style="border-top: 5px solid #06b6d4; height: 100%;">
            <span class="glow-badge-cyan">🧬 Sigmoid</span>
            <div style="margin-top: 15px; font-family: monospace; font-size: 0.95rem; line-height: 1.6;">
                <strong>Formula:</strong><br>
                f(z) = 1 / (1 + e⁻ᶻ)<br><br>
                <strong>At z = {global_z:+.2f}:</strong><br>
                f({global_z:.2f}) = <span class="cyan-highlight">{p_sig:.4f}</span><br><br>
                <strong>Derivative Formula:</strong><br>
                f'(z) = f(z) · (1 - f(z))<br><br>
                <strong>Gradient f'({global_z:.2f}):</strong><br>
                f' = <span class="cyan-highlight">{dp_sig:.4f}</span>
            </div>
            <p style="margin-top: 15px; font-size: 0.85rem; color: #94a3b8; line-height: 1.4;">
                {"💤 <b>Saturated:</b> The gradient is extremely small. The neuron is in a dead-zone where it stops learning!" if dp_sig < 0.05 else "⚡ <b>Active:</b> The gradient is active, allowing learning to occur, though maximum learning rate is capped at 0.25."}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_tanh_card:
        st.markdown(f"""
        <div class="custom-card" style="border-top: 5px solid #ec4899; height: 100%;">
            <span class="glow-badge-pink">💖 tanh</span>
            <div style="margin-top: 15px; font-family: monospace; font-size: 0.95rem; line-height: 1.6;">
                <strong>Formula:</strong><br>
                f(z) = tanh(z)<br><br>
                <strong>At z = {global_z:+.2f}:</strong><br>
                f({global_z:.2f}) = <span class="pink-highlight">{p_tanh:.4f}</span><br><br>
                <strong>Derivative Formula:</strong><br>
                f'(z) = 1 - f(z)²<br><br>
                <strong>Gradient f'({global_z:.2f}):</strong><br>
                f' = <span class="pink-highlight">{dp_tanh:.4f}</span>
            </div>
            <p style="margin-top: 15px; font-size: 0.85rem; color: #94a3b8; line-height: 1.4;">
                {"💤 <b>Saturated:</b> Highly confident node, but derivative has shriveled. It cannot update weights." if dp_tanh < 0.05 else "⚡ <b>Strong Gradient:</b> Zero-centered output helps. Peak gradient at z=0 is a solid 1.0!"}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_relu_card:
        st.markdown(f"""
        <div class="custom-card" style="border-top: 5px solid #22c55e; height: 100%;">
            <span class="glow-badge-green">🟢 ReLU</span>
            <div style="margin-top: 15px; font-family: monospace; font-size: 0.95rem; line-height: 1.6;">
                <strong>Formula:</strong><br>
                f(z) = max(0, z)<br><br>
                <strong>At z = {global_z:+.2f}:</strong><br>
                f({global_z:.2f}) = <span class="green-highlight">{p_relu:.4f}</span><br><br>
                <strong>Derivative Formula:</strong><br>
                f'(z) = 1 if z > 0 else 0<br><br>
                <strong>Gradient f'({global_z:.2f}):</strong><br>
                f' = <span class="green-highlight">{dp_relu:.1f}</span>
            </div>
            <p style="margin-top: 15px; font-size: 0.85rem; color: #94a3b8; line-height: 1.4;">
                {"💀 <b>Dead ReLU:</b> Input is negative. The output is 0.0, and the gradient is 0.0. This neuron cannot receive updates." if global_z <= 0 else "⚡ <b>Linear Flow:</b> Positive input. Gradient is a perfect 1.0. This avoids gradient saturation!"}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_leaky_card:
        st.markdown(f"""
        <div class="custom-card" style="border-top: 5px solid #f59e0b; height: 100%;">
            <span class="glow-badge-amber">🔶 Leaky ReLU</span>
            <div style="margin-top: 15px; font-family: monospace; font-size: 0.95rem; line-height: 1.6;">
                <strong>Formula (α=0.1):</strong><br>
                f(z) = max(0.1z, z)<br><br>
                <strong>At z = {global_z:+.2f}:</strong><br>
                f({global_z:.2f}) = <span class="amber-highlight">{p_leaky:.4f}</span><br><br>
                <strong>Derivative Formula:</strong><br>
                f'(z) = 1 if z > 0 else 0.1<br><br>
                <strong>Gradient f'({global_z:.2f}):</strong><br>
                f' = <span class="amber-highlight">{dp_leaky:.2f}</span>
            </div>
            <p style="margin-top: 15px; font-size: 0.85rem; color: #94a3b8; line-height: 1.4;">
                {"🏥 <b>Leaking:</b> Negative input, but derivative is 0.1 (not zero!). This 'leak' keeps the neuron alive so it can recover!" if global_z <= 0 else "⚡ <b>Linear Flow:</b> Positive input. Perfect 1.0 gradient flow."}
            </p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# TAB 2: THE SIGNAL SANDBOX
# ==========================================
with tab_sandbox:
    st.markdown("""
    <div style="margin-top: 15px; margin-bottom: 20px;">
        <h3>🌊 Signal Processing in Neurons</h3>
        <p style="color: #cbd5e1; font-size: 1.05rem; line-height: 1.6;">
            What does "non-linear mapping" look like when applied to a continuous stream of data? 
            In this sandbox, we generate an input signal wave ($z$) and feed it directly into our activation functions. 
            Watch how the shape of the wave is warped, squashed, and clipped!
            Use the controls in the <b>sidebar (Tab 2: Wave Sandbox)</b> to change the signal type, frequency, and amplitude.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate wave signal
    t = np.linspace(0, 10, 500)
    
    if wave_type == "Sine Wave":
        raw_signal = wave_amp * np.sin(wave_freq * t)
    elif wave_type == "Square Wave":
        raw_signal = wave_amp * np.sign(np.sin(wave_freq * t))
    elif wave_type == "Triangle Wave":
        raw_signal = wave_amp * (2.0 * np.abs(2.0 * (t * wave_freq / 10.0 - np.floor(t * wave_freq / 10.0 + 0.5))) - 1.0)
    else: # Random Noise
        np.random.seed(42)
        raw_signal = np.sin(wave_freq * t) * (wave_amp / 2) + np.random.normal(0, 0.4, len(t))
        
    # Process through activations
    sig_signal = sigmoid(raw_signal)
    tanh_signal = tanh_val(raw_signal)
    relu_signal = relu(raw_signal)
    leaky_signal = leaky_relu(raw_signal)
    
    selected_signals = st.multiselect(
        "⚡ Toggle Outputs to Overlay",
        options=["Sigmoid", "tanh", "ReLU", "Leaky ReLU"],
        default=["Sigmoid", "tanh", "ReLU"],
        help="Select which processed signals you want to display on the comparison graph."
    )
    
    col_w1, col_w2 = st.columns([1, 1.3], gap="medium")
    
    with col_w1:
        # Input Signal Chart
        fig_input = go.Figure()
        fig_input.add_trace(go.Scatter(x=t, y=raw_signal, name="Raw Signal (z)", line=dict(color="#cbd5e1", width=2.5)))
        
        # Horizontal reference at 0
        fig_input.add_shape(type="line", x0=0, y0=0, x1=10, y1=0, line=dict(color="rgba(255,255,255,0.2)", width=1))
        
        fig_input.update_layout(
            title=dict(text="📥 <b>Raw Input Signal</b> <i>z(t)</i>", font=dict(color="#cbd5e1")),
            xaxis_title="Time (t)",
            yaxis_title="Signal Amplitude (z)",
            template="plotly_dark",
            plot_bgcolor="#0d1321",
            paper_bgcolor="#070a13",
            margin=dict(l=30, r=20, t=40, b=30),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.03)"),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.03)", range=[-4.5, 4.5])
        )
        st.plotly_chart(fig_input, use_container_width=True)
        
    with col_w2:
        # Activated Signal Chart
        fig_output = go.Figure()
        
        # Always overlay the original signal in background
        fig_output.add_trace(go.Scatter(x=t, y=raw_signal, name="Original", line=dict(color="rgba(255,255,255,0.15)", width=1.5, dash="dash")))
        
        if "Sigmoid" in selected_signals:
            fig_output.add_trace(go.Scatter(x=t, y=sig_signal, name="Sigmoid", line=dict(color="#06b6d4", width=3)))
        if "tanh" in selected_signals:
            fig_output.add_trace(go.Scatter(x=t, y=tanh_signal, name="tanh", line=dict(color="#ec4899", width=3)))
        if "ReLU" in selected_signals:
            fig_output.add_trace(go.Scatter(x=t, y=relu_signal, name="ReLU", line=dict(color="#22c55e", width=3)))
        if "Leaky ReLU" in selected_signals:
            fig_output.add_trace(go.Scatter(x=t, y=leaky_signal, name="Leaky ReLU", line=dict(color="#f59e0b", width=2.5, dash="dot")))
            
        fig_output.update_layout(
            title=dict(text="📤 <b>Activated Output Signal</b> <i>a(t) = f(z(t))</i>", font=dict(color="#cbd5e1")),
            xaxis_title="Time (t)",
            yaxis_title="Output Score (a)",
            template="plotly_dark",
            plot_bgcolor="#0d1321",
            paper_bgcolor="#070a13",
            margin=dict(l=30, r=20, t=40, b=30),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.03)"),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.03)", range=[-4.5, 4.5])
        )
        st.plotly_chart(fig_output, use_container_width=True)

    # Explanation block of what is observed in Sandbox
    st.markdown("""
    <div class="custom-card">
        <h4>💡 Crucial Pedagogical Insights:</h4>
        <ul style="line-height: 1.8; color: #cbd5e1; margin-bottom: 0;">
            <li><b>The ReLU Scissors ✂️:</b> Notice that for <b>ReLU</b>, the bottom half of the wave (negative inputs) is cut completely, becoming a perfectly straight flat line at <span class="green-highlight">0.0</span>. This represents <b>rectification</b>. This simple operation makes ReLU very fast and sparse, but can kill signals completely.</li>
            <li><b>The Tanh Compression 🗜️:</b> Notice how <b>tanh</b> keeps the wave shape highly recognizable, but squeezes the peaks and valleys into flat saturation zones near <span class="pink-highlight">+1.0</span> and <span class="pink-highlight">-1.0</span>. This smooth distortion is perfect for maintaining centered signals, but locks up our gradients if the waves are too large.</li>
            <li><b>The Sigmoid Shift 🚀:</b> Notice how <b>Sigmoid</b> shifts the entire wave into the positive realm between <span class="cyan-highlight">0.0 and 1.0</span>, centering the baseline around <span class="cyan-highlight">0.5</span>. This shift makes it great for final output probabilities, but causes intermediate network layers to drift and saturate.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# TAB 3: THE GREAT BACKPROP RACE
# ==========================================
with tab_backprop:
    st.markdown("""
    <div style="margin-top: 15px; margin-bottom: 25px;">
        <h3>🏃‍♂️ Gradient Highway: Vanishing Gradient & Dead ReLU Visualized</h3>
        <p style="color: #cbd5e1; font-size: 1.05rem; line-height: 1.6;">
            Gradients are calculated during training using the <b>Chain Rule</b>. 
            As we move backward through layers of a neural network, the error signal is multiplied by the <b>derivative of the activation function</b> at each neuron!
            <br>
            If these derivatives are small (like in Sigmoid/tanh saturation), the gradient shrinks exponentially until early layers receive virtually nothing!
            Configure the test parameters in the <b>sidebar (Tab 3: Backprop Race)</b> to compare how error signals flow.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate gradients backward
    # Derivatives for current selected engine
    if backprop_act == "Sigmoid":
        d1_act, d2_act, d3_act = sigmoid_derivative(z1), sigmoid_derivative(z2), sigmoid_derivative(z3)
        act_theme_color = "#06b6d4"
        act_theme_glow = "glow-cyan"
    elif backprop_act == "tanh":
        d1_act, d2_act, d3_act = tanh_derivative(z1), tanh_derivative(z2), tanh_derivative(z3)
        act_theme_color = "#ec4899"
        act_theme_glow = "glow-pink"
    elif backprop_act == "ReLU":
        d1_act, d2_act, d3_act = relu_derivative(z1), relu_derivative(z2), relu_derivative(z3)
        act_theme_color = "#22c55e"
        act_theme_glow = "glow-green"
    else: # Leaky ReLU
        d1_act, d2_act, d3_act = leaky_relu_derivative(z1), leaky_relu_derivative(z2), leaky_relu_derivative(z3)
        act_theme_color = "#f59e0b"
        act_theme_glow = "glow-amber"
        
    # Flow logic:
    G3 = grad_init
    G2 = G3 * d3_act
    G1 = G2 * d2_act
    G0 = G1 * d1_act
    
    # Format values for display
    def clean_format(val):
        if abs(val) < 0.0001:
            return "0.0000"
        return f"{val:.4f}"
        
    # Define connection line properties
    # Link 3 (incoming, right)
    t3 = 8
    c3 = "#eab308" # Glowing Gold
    g3 = "url(#glow-gold)"
    
    # Link 2 (between L3 and L2)
    r2 = G2 / grad_init
    t2 = max(1.5, min(8.0, r2 * 8.0))
    if G2 < 0.001:
        c2, g2 = "#475569", "none"
    elif G2 < 0.2:
        c2, g2 = "#f87171", "none"
    else:
        c2, g2 = "#eab308", "url(#glow-gold)"
        
    # Link 1 (between L2 and L1)
    r1 = G1 / grad_init
    t1 = max(1.5, min(8.0, r1 * 8.0))
    if G1 < 0.001:
        c1, g1 = "#475569", "none"
    elif G1 < 0.2:
        c1, g1 = "#f87171", "none"
    else:
        c1, g1 = "#eab308", "url(#glow-gold)"
        
    # Link 0 (exit, left)
    r0 = G0 / grad_init
    t0 = max(1.5, min(8.0, r0 * 8.0))
    if G0 < 0.001:
        c0, g0 = "#475569", "none"
    elif G0 < 0.2:
        c0, g0 = "#f87171", "none"
    else:
        c0, g0 = "#eab308", "url(#glow-gold)"
        
    # Node freezing warnings
    node3_warning = ""
    node2_warning = ""
    node1_warning = ""
    
    if d3_act < 0.01:
        node3_warning = "❄️ SATURATED" if backprop_act in ["Sigmoid", "tanh"] else "💀 DEAD"
    if d2_act < 0.01:
        node2_warning = "❄️ SATURATED" if backprop_act in ["Sigmoid", "tanh"] else "💀 DEAD"
    if d1_act < 0.01:
        node1_warning = "❄️ SATURATED" if backprop_act in ["Sigmoid", "tanh"] else "💀 DEAD"
        
    # SVG Dimensions: 850 x 300
    svg_backprop = f"""
    <svg viewBox="0 0 850 300" width="100%" height="100%" style="background:#0e1626; border-radius:16px; border:1px solid rgba(255,255,255,0.05); box-shadow: inset 0 0 40px rgba(0,0,0,0.5);">
        <defs>
            <filter id="glow-gold" x="-30%" y="-30%" width="160%" height="160%">
                <feGaussianBlur stdDeviation="6" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
            <filter id="glow-cyan" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="6" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
            <filter id="glow-pink" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="6" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
            <filter id="glow-green" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="6" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
            <filter id="glow-amber" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="6" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
            
            <style>
                @keyframes pulse-flow-rev {{
                    to {{ stroke-dashoffset: 20; }}
                }}
                .flow-g3 {{
                    stroke-dasharray: 8 6;
                    animation: pulse-flow-rev 1.2s linear infinite;
                }}
                .flow-g2 {{
                    stroke-dasharray: 8 6;
                    animation: pulse-flow-rev 1.2s linear infinite;
                }}
                .flow-g1 {{
                    stroke-dasharray: 8 6;
                    animation: pulse-flow-rev 1.2s linear infinite;
                }}
                .flow-g0 {{
                    stroke-dasharray: 8 6;
                    animation: pulse-flow-rev 1.2s linear infinite;
                }}
            </style>
        </defs>

        <!-- BACKGROUND GRID -->
        <g stroke="rgba(255,255,255,0.02)" stroke-width="1">
            <line x1="0" y1="50" x2="850" y2="50" />
            <line x1="0" y1="100" x2="850" y2="100" />
            <line x1="0" y1="150" x2="850" y2="150" />
            <line x1="0" y1="200" x2="850" y2="200" />
            <line x1="0" y1="250" x2="850" y2="250" />
            <line x1="100" y1="0" x2="100" y2="300" />
            <line x1="200" y1="0" x2="200" y2="300" />
            <line x1="300" y1="0" x2="300" y2="300" />
            <line x1="425" y1="0" x2="425" y2="300" />
            <line x1="550" y1="0" x2="550" y2="300" />
            <line x1="650" y1="0" x2="650" y2="300" />
            <line x1="750" y1="0" x2="750" y2="300" />
        </g>

        <!-- BACKPROPAGATING CONNECTION PATHS (RIGHT TO LEFT) -->
        <!-- Link 3 (Entrance to Layer 3 Node) -->
        <line x1="800" y1="150" x2="695" y2="150" stroke="{c3}" stroke-width="{t3}" opacity="0.8"/>
        <line x1="800" y1="150" x2="695" y2="150" stroke="#fef08a" stroke-width="2.5" class="flow-g3" filter="{g3}"/>

        <!-- Link 2 (Layer 3 Node to Layer 2 Node) -->
        <line x1="605" y1="150" x2="470" y2="150" stroke="{c2}" stroke-width="{t2}" opacity="0.8"/>
        {f'<line x1="605" y1="150" x2="470" y2="150" stroke="#fef08a" stroke-width="2" class="flow-g2" filter="{g2}"/>' if G2 > 0.01 else ""}

        <!-- Link 1 (Layer 2 Node to Layer 1 Node) -->
        <line x1="380" y1="150" x2="245" y2="150" stroke="{c1}" stroke-width="{t1}" opacity="0.8"/>
        {f'<line x1="380" y1="150" x2="245" y2="150" stroke="#fef08a" stroke-width="2" class="flow-g1" filter="{g1}"/>' if G1 > 0.01 else ""}

        <!-- Link 0 (Layer 1 Node to Exit) -->
        <line x1="155" y1="150" x2="50" y2="150" stroke="{c0}" stroke-width="{t0}" opacity="0.8"/>
        {f'<line x1="155" y1="150" x2="50" y2="150" stroke="#fef08a" stroke-width="2" class="flow-g0" filter="{g0}"/>' if G0 > 0.01 else ""}

        <!-- GRADIENT VALUE BUBBLES -->
        <rect x="715" y="110" width="70" height="20" rx="5" fill="#1e293b" stroke="#eab308" stroke-width="1.5"/>
        <text x="750" y="124" fill="#fef08a" font-size="11" font-weight="bold" text-anchor="middle">G₃ = {G3:.1f}</text>
        
        <rect x="510" y="110" width="75" height="20" rx="5" fill="#1e293b" stroke="{c2}" stroke-width="1.5"/>
        <text x="547" y="124" fill="#f8fafc" font-size="11" font-weight="semibold" text-anchor="middle">G₂ = {clean_format(G2)}</text>
        
        <rect x="285" y="110" width="75" height="20" rx="5" fill="#1e293b" stroke="{c1}" stroke-width="1.5"/>
        <text x="322" y="124" fill="#f8fafc" font-size="11" font-weight="semibold" text-anchor="middle">G₁ = {clean_format(G1)}</text>
        
        <rect x="65" y="110" width="75" height="20" rx="5" fill="#1e293b" stroke="{c0}" stroke-width="1.5"/>
        <text x="102" y="124" fill="#fef08a" font-size="11" font-weight="bold" text-anchor="middle">G₀ = {clean_format(G0)}</text>

        <!-- NEURON NODES (CHAIN OF 3) -->
        <!-- Layer 3 Neuron -->
        <circle cx="650" cy="150" r="45" fill="#0f172a" stroke="{act_theme_color}" stroke-width="3.5" filter="{ 'url(#' + act_theme_glow + ')' if d3_act > 0.05 else 'none' }"/>
        <text x="650" y="132" fill="#cbd5e1" font-size="10.5" font-weight="bold" text-anchor="middle">LAYER 3</text>
        <text x="650" y="152" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="middle">z₃ = {z3:+.1f}</text>
        <text x="650" y="172" fill="{act_theme_color}" font-size="11" font-weight="black" text-anchor="middle">f'(z₃) = {d3_act:.3f}</text>
        {f'<text x="650" y="215" fill="#f87171" font-size="10" font-weight="bold" text-anchor="middle">{node3_warning}</text>' if node3_warning else ""}

        <!-- Layer 2 Neuron -->
        <circle cx="425" cy="150" r="45" fill="#0f172a" stroke="{act_theme_color}" stroke-width="3.5" filter="{ 'url(#' + act_theme_glow + ')' if d2_act > 0.05 else 'none' }"/>
        <text x="425" y="132" fill="#cbd5e1" font-size="10.5" font-weight="bold" text-anchor="middle">LAYER 2</text>
        <text x="425" y="152" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="middle">z₂ = {z2:+.1f}</text>
        <text x="425" y="172" fill="{act_theme_color}" font-size="11" font-weight="black" text-anchor="middle">f'(z₂) = {d2_act:.3f}</text>
        {f'<text x="425" y="215" fill="#f87171" font-size="10" font-weight="bold" text-anchor="middle">{node2_warning}</text>' if node2_warning else ""}

        <!-- Layer 1 Neuron -->
        <circle cx="200" cy="150" r="45" fill="#0f172a" stroke="{act_theme_color}" stroke-width="3.5" filter="{ 'url(#' + act_theme_glow + ')' if d1_act > 0.05 else 'none' }"/>
        <text x="200" y="132" fill="#cbd5e1" font-size="10.5" font-weight="bold" text-anchor="middle">LAYER 1</text>
        <text x="200" y="152" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="middle">z₁ = {z1:+.1f}</text>
        <text x="200" y="172" fill="{act_theme_color}" font-size="11" font-weight="black" text-anchor="middle">f'(z₁) = {d1_act:.3f}</text>
        {f'<text x="200" y="215" fill="#f87171" font-size="10" font-weight="bold" text-anchor="middle">{node1_warning}</text>' if node1_warning else ""}

        <!-- FLOW DIRECTION INDICATORS (BACKWARD ARROWS ON TOP) -->
        <path d="M 450,40 L 400,40" stroke="#fef08a" stroke-width="2.5" fill="none" marker-end="url(#arrow)" />
        <text x="425" y="28" fill="#fef08a" font-size="11" font-weight="black" text-anchor="middle">ERROR FLOW DIRECTION (BACKPROP)</text>
        
        <defs>
            <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 10 0 L 0 5 L 10 10 z" fill="#fef08a" />
            </marker>
        </defs>
    </svg>
    """
    
    # Render the SVG
    svg_clean = "\n".join([line.strip() for line in svg_backprop.split("\n")])
    st.markdown(svg_clean, unsafe_allow_html=True)
    
    # Real-time verdict summary table
    st.markdown("<br>", unsafe_allow_html=True)
    col_v1, col_v2 = st.columns([1.2, 1.8])
    
    with col_v1:
        st.markdown(f"""
        <div class="custom-card" style="height: 100%;">
            <div class="card-title">🏁 Backprop Race Verdict</div>
            <table style="width:100%; font-size:1.0rem; border-collapse:collapse; text-align:left; color:#cbd5e1;">
                <tr style="border-bottom:1px solid rgba(255,255,255,0.1); font-weight:bold; color:#f8fafc;">
                    <th style="padding:10px 5px;">Metric</th>
                    <th style="padding:10px 5px;">Value</th>
                </tr>
                <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                    <td style="padding:10px 5px; font-weight:600;">Selected Activation</td>
                    <td style="padding:10px 5px; color:{act_theme_color}; font-weight:bold;">{backprop_act}</td>
                </tr>
                <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                    <td style="padding:10px 5px; font-weight:600;">Incoming Gradient</td>
                    <td style="padding:10px 5px; color:#facc15; font-weight:700;">{grad_init:.1f}</td>
                </tr>
                <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                    <td style="padding:10px 5px; font-weight:600;">Final Gradient G₀</td>
                    <td style="padding:10px 5px; color:#facc15; font-weight:700;">{clean_format(G0)}</td>
                </tr>
                <tr>
                    <td style="padding:10px 5px; font-weight:600;">Gradient Transmission</td>
                    <td style="padding:10px 5px; font-weight:700;">{(G0 / grad_init * 100.0):.2f}%</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
    with col_v2:
        # Generate custom verdict based on output
        if G0 < 0.0001:
            verdict_style = "border: 2px solid #ef4444; background: rgba(239, 68, 68, 0.08);"
            verdict_badge = "<span style='background:#ef4444; color:#0b0f19; font-weight:800; padding:6px 12px; border-radius:30px; box-shadow: 0 0 15px rgba(239, 68, 68, 0.4); display:inline-block;'>⚠️ TOTAL GRADIENT BLOCK</span>"
            if backprop_act == "ReLU":
                reason = "One of your layer inputs is <b>negative or zero</b>! Because ReLU's derivative is absolute zero for negative values, the gradient hit a brick wall at that layer. This is the notorious <b>Dead ReLU problem</b>! Once a ReLU node dies, it can never learn again!"
            elif backprop_act == "Leaky ReLU":
                reason = "Wait! Even with Leaky ReLU, a small signal might be suppressed, but it should never be completely zero! Leaky ReLU preserves a 0.1 multiplier. Double check if inputs are extremely small."
            else:
                reason = "Your neuron inputs are set in the <b>saturation zones</b> (deep positive or deep negative). The derivatives of Sigmoid/tanh are extremely close to zero here. Stacking 3 layers completely extinguished the signal. This is the classic <b>Vanishing Gradient Problem</b>!"
        elif G0 < 0.1:
            verdict_style = "border: 2px solid #f59e0b; background: rgba(245, 158, 11, 0.08);"
            verdict_badge = "<span style='background:#f59e0b; color:#0b0f19; font-weight:800; padding:6px 12px; border-radius:30px; box-shadow: 0 0 15px rgba(245, 158, 11, 0.4); display:inline-block;'>⚠️ SEVERE VANISHING GRADIENT</span>"
            reason = f"The error signal shrunk from <b>{grad_init:.1f}</b> to <b>{G0:.4f}</b>! The early layer (Layer 1) receives almost no signal. Stacking activations with small derivatives (like Sigmoid's max of 0.25) multiplies them together: 0.25 × 0.25 × 0.25 = 0.015! The network will train at a snail's pace."
        else:
            verdict_style = "border: 2px solid #22c55e; background: rgba(34, 197, 94, 0.08);"
            verdict_badge = "<span style='background:#22c55e; color:#0b0f19; font-weight:800; padding:6px 12px; border-radius:30px; box-shadow: 0 0 15px rgba(34, 197, 94, 0.4); display:inline-block;'>⚡ GRADIENT HEALTHY</span>"
            reason = f"Excellent! The gradient is flowing nicely through all layers, leaving a healthy <b>{G0:.3f}</b> error signal for early weights. This occurs because the derivative multiplier remains strong (1.0 for ReLU/Leaky ReLU, or inputs are centered at 0 for Sigmoid/tanh where gradients are maximized)."
            
        st.markdown(f"""
        <div class="custom-card" style="{verdict_style} height: 100%;">
            {verdict_badge}
            <h4 style="margin-top: 15px; color:#f8fafc;">What is happening here?</h4>
            <p style="font-size: 1.05rem; line-height: 1.6; color: #cbd5e1; margin-bottom: 0;">{reason}</p>
        </div>
        """, unsafe_allow_html=True)

# Interactive Summary & Review Challenge
st.markdown("---")
st.markdown("""
<div class="custom-card">
    <h3 style="color: #38bdf8; margin-top: 0;">🎓 Quick Challenge Zone!</h3>
    <p style="font-size: 1.05rem; line-height: 1.6; color: #cbd5e1; margin-bottom: 15px;">
        Let's put your new intuition to the test! Try completing these three laboratory tasks using the controls in the sidebar:
    </p>
    <ul style="line-height: 1.8; color: #cbd5e1; margin-bottom: 0;">
        <li><b>Challenge 1: The Sigmoid Freeze ❄️</b><br>
            Set the <b>Common Input z</b> to <b>+4.0</b> (using Lock Inputs) under the <b>Sigmoid</b> engine. Go to Tab 3. 
            Notice how tiny the derivatives are, and see how the incoming error of {st.session_state.get('grad_init', 10.0)} vanishes to virtually zero. 
            This is why researchers stopped using Sigmoid inside deep networks!
        </li>
        <li><b>Challenge 2: The Dead ReLU Resurrection 🧟‍♂️</b><br>
            In Tab 3, select the <b>ReLU</b> engine and set <b>Common Input z</b> to <b>-1.0</b>. 
            Watch the gradient hit the very first layer and instantly drop to <b>0.0000</b> (Dead ReLU). 
            Now, switch the engine to <b>Leaky ReLU</b>. Notice how the gradient suddenly resurrects and leaks through! 
            The leak has successfully revived our deep network!
        </li>
        <li><b>Challenge 3: The Sine Wave Shaper 🌊</b><br>
            Go to Tab 2 (The Signal Sandbox), select a <b>Sine Wave</b> and tick only <b>ReLU</b> and <b>Leaky ReLU</b>. 
            Observe where the curves diverge. While ReLU chops the wave flat at 0.0, Leaky ReLU lets a tiny, scaled-down negative wave pass. 
            This represents the 0.1x leak in action!
        </li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 40px; padding: 20px; color: #64748b; font-size: 0.9rem; border-top: 1px solid rgba(255,255,255,0.05);">
    Page 65 of the AI Visualized Curriculum | Built with ❤️ to compare and master activation functions.
</div>
""", unsafe_allow_html=True)