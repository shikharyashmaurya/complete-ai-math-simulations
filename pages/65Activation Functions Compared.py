import sys
from pathlib import Path

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from common.mathutils import sigmoid  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

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
    
    /* Base text colours. No !important and no blanket `span` rule, so that the
       highlight classes and inline style="color: ..." badges keep their colours. */
    .stMarkdown, .stMarkdown p, .stMarkdown li {
        color: #cbd5e1;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #f8fafc;
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
    
    /* Sidebar Styling (background on the container only, so slider tracks keep their colours) */
    [data-testid="stSidebar"] {
        background-color: #0d1321;
    }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: #cbd5e1;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 {
        color: #38bdf8;
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
    
    .custom-card, .custom-card p, .custom-card li {
        color: #cbd5e1;
    }
    
    .custom-card h1, .custom-card h2, .custom-card h3, .custom-card h4, .custom-card h5, .custom-card h6 {
        color: #f8fafc;
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
LEAKY_ALPHA = 0.1
SATURATION_THRESHOLD = 0.05  # sigmoid/tanh derivative below this counts as "saturated" everywhere on this page

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
    # ReLU is not differentiable at z = 0; we use the common convention f'(0) = 0.
    return np.where(z > 0.0, 1.0, 0.0)

def leaky_relu(z, alpha=LEAKY_ALPHA):
    return np.where(z > 0.0, z, alpha * z)

def leaky_relu_derivative(z, alpha=LEAKY_ALPHA):
    # Not differentiable at z = 0 either; we use f'(0) = alpha.
    return np.where(z > 0.0, 1.0, alpha)


# Session state. Keys are prefixed with "p65_" because st.session_state is shared by all pages
# (pages 4 and 5 use a widget key named "z3"). Widgets get their initial value from these keys
# only (no value= argument), which avoids Streamlit's "default value + Session State" warning.
P65_DEFAULTS = {
    "p65_global_z": 1.0,
    "p65_wave_type": "Sine Wave",
    "p65_wave_freq": 2,
    "p65_wave_amp": 2.0,
    "p65_noise_seed": 42,
    "p65_selected_signals": ["Sigmoid", "tanh", "ReLU"],
    "p65_backprop_act": "Sigmoid",
    "p65_grad_init": 10.0,
    "p65_z_lock": True,
    # Non-widget stores: they survive while the corresponding slider is hidden by the lock toggle.
    "p65_zc_store": 2.0,
    "p65_z_store": [2.0, 2.0, 2.0],
}
for _key, _val in P65_DEFAULTS.items():
    st.session_state.setdefault(_key, list(_val) if isinstance(_val, list) else _val)

# Callbacks
def set_preset_z(val):
    st.session_state.p65_global_z = val

def resample_noise():
    st.session_state.p65_noise_seed += 1

def store_common_z():
    st.session_state.p65_zc_store = st.session_state.p65_zc

def store_layer_z(idx):
    st.session_state.p65_z_store[idx] = st.session_state[f"p65_z{idx + 1}"]

def on_lock_toggle():
    # Unlocking continues from the common value, so the diagram does not jump.
    if not st.session_state.p65_z_lock:
        common = st.session_state.p65_zc_store
        st.session_state.p65_z_store = [common, common, common]
        for i in range(3):
            st.session_state[f"p65_z{i + 1}"] = common
    else:
        st.session_state.p65_zc = st.session_state.p65_zc_store

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
    step=0.1,
    key="p65_global_z"
)
global_z = round(float(global_z), 6)  # avoid float artefacts such as 1e-17 at the kink z = 0

st.sidebar.markdown("##### 📍 Quick Presets")
preset_cols = st.sidebar.columns(2)
with preset_cols[0]:
    st.button("Zero Center (z=0)", on_click=set_preset_z, args=(0.0,), width="stretch", key="p65_preset_0")
    st.button("Active Positive (z=2)", on_click=set_preset_z, args=(2.0,), width="stretch", key="p65_preset_2")
with preset_cols[1]:
    st.button("Deep Saturation (z=5)", on_click=set_preset_z, args=(5.0,), width="stretch", key="p65_preset_5")
    st.button("Deep Negative (z=-3)", on_click=set_preset_z, args=(-3.0,), width="stretch", key="p65_preset_m3")

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Tab 2: Wave Sandbox")
wave_type = st.sidebar.selectbox(
    "Input Signal Shape",
    options=["Sine Wave", "Square Wave", "Triangle Wave", "Random Noise"],
    key="p65_wave_type"
)
wave_freq = st.sidebar.slider(
    "Signal Frequency (cycles over the 10 s window)", min_value=1, max_value=5, step=1, key="p65_wave_freq",
    help="All four signal shapes use the same period: 10 / frequency seconds."
)
wave_amp = st.sidebar.slider("Signal Amplitude", min_value=1.0, max_value=4.0, step=0.5, key="p65_wave_amp")
if wave_type == "Random Noise":
    st.sidebar.button("🎲 Resample noise", on_click=resample_noise, width="stretch", key="p65_resample_noise")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏃‍♂️ Tab 3: Backprop Race")
backprop_act = st.sidebar.selectbox(
    "Test Activation Engine",
    options=["Sigmoid", "tanh", "ReLU", "Leaky ReLU"],
    key="p65_backprop_act"
)

grad_init = st.sidebar.slider(
    "Starting Gradient (Error)",
    min_value=1.0,
    max_value=20.0,
    step=1.0,
    key="p65_grad_init"
)

z_lock = st.sidebar.checkbox(
    "Lock Inputs (z₁ = z₂ = z₃)",
    key="p65_z_lock",
    on_change=on_lock_toggle,
    help="Locks input z values for all layers to see compounding effects easily. Unlocking starts every layer at the common value."
)

if z_lock:
    st.session_state.setdefault("p65_zc", st.session_state.p65_zc_store)
    z1_val = st.sidebar.slider(
        "Common Input z", min_value=-5.0, max_value=5.0, step=0.5, key="p65_zc", on_change=store_common_z
    )
    z1 = z1_val
    z2 = z1_val
    z3 = z1_val
else:
    _layer_z = []
    for _i, _label in enumerate(["Layer 1 Input (z₁)", "Layer 2 Input (z₂)", "Layer 3 Input (z₃)"]):
        st.session_state.setdefault(f"p65_z{_i + 1}", st.session_state.p65_z_store[_i])
        _layer_z.append(st.sidebar.slider(
            _label, min_value=-5.0, max_value=5.0, step=0.5, key=f"p65_z{_i + 1}",
            on_change=store_layer_z, args=(_i,)
        ))
    z1, z2, z3 = _layer_z

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
            Mathematically, a 100-layer network of affine maps is equivalent to a single affine map:
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
            Below, we compare the activation profiles (<i>f(z)</i>) and their respective derivative profiles (<i>f′(z)</i>) side-by-side. 
            Adjust the <b>Global Probe slider (<i>z</i>)</b> in the sidebar to scan along the curves and watch the live coordinate values update!
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
            yaxis=dict(range=[min(np.min(y_sig), np.min(y_tanh), np.min(y_relu), np.min(y_leaky)) - 0.2, max(np.max(y_sig), np.max(y_tanh), np.max(y_relu), np.max(y_leaky)) + 0.2], showgrid=True, gridcolor="rgba(255,255,255,0.05)", zeroline=True, zerolinecolor="rgba(255,255,255,0.15)"),
            margin=dict(l=40, r=20, t=50, b=40),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(13,19,33,0.7)")
        )
        st.plotly_chart(fig_act, width="stretch")

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
        st.plotly_chart(fig_deriv, width="stretch")

    # Live Mathematical Verification Cards
    st.markdown("### 🎚️ Live Probe Calculations at $z = %.2f$" % global_z)
    
    col_sig_card, col_tanh_card, col_relu_card, col_leaky_card = st.columns(4)

    if global_z > 0:
        relu_note = "⚡ <b>Linear Flow:</b> Positive input. Gradient is a perfect 1.0. This avoids gradient saturation!"
        leaky_note = "⚡ <b>Linear Flow:</b> Positive input. Perfect 1.0 gradient flow."
    elif global_z == 0:
        relu_note = ("📍 <b>At the kink (z = 0):</b> ReLU has no derivative here. This page uses the common convention "
                     "f'(0) = 0, so no gradient passes for this exact input.")
        leaky_note = ("📍 <b>At the kink (z = 0):</b> output is 0; this page uses the convention f'(0) = 0.1, "
                      "the same slope as the negative side.")
    else:
        relu_note = ("💤 <b>Inactive at this z:</b> negative input, so the output is 0.0 and the gradient is 0.0. "
                     "No update flows back through this unit <i>for this input</i>. A unit is called a "
                     "<b>dead ReLU</b> only if it is inactive for <i>every</i> input it sees.")
        leaky_note = ("🏥 <b>Leaking:</b> Negative input, but the derivative is 0.1 (not zero!). This 'leak' lets a "
                      "small gradient through, so the unit can still learn and recover.")
    
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
                {"💤 <b>Saturated:</b> The derivative is tiny, so almost no gradient flows back through this neuron and its weights barely update." if dp_sig < SATURATION_THRESHOLD else "⚡ <b>Active:</b> The gradient is flowing, but the sigmoid derivative (the gradient multiplier) never exceeds 0.25, reached at z = 0."}
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
                {"💤 <b>Saturated:</b> Highly confident node, but the derivative has shriveled, so its weights barely update." if dp_tanh < SATURATION_THRESHOLD else "⚡ <b>Strong Gradient:</b> Zero-centered output helps. Peak gradient at z=0 is a solid 1.0!"}
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
                f'(z) = 1 if z > 0 else 0<br>
                <span style="font-size: 0.8rem; color: #94a3b8;">(at the kink z = 0 we use the convention f'(0) = 0)</span><br><br>
                <strong>Gradient f'({global_z:.2f}):</strong><br>
                f' = <span class="green-highlight">{dp_relu:.1f}</span>
            </div>
            <p style="margin-top: 15px; font-size: 0.85rem; color: #94a3b8; line-height: 1.4;">
                {relu_note}
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
                f'(z) = 1 if z > 0 else 0.1<br>
                <span style="font-size: 0.8rem; color: #94a3b8;">(at the kink z = 0 we use the convention f'(0) = 0.1)</span><br><br>
                <strong>Gradient f'({global_z:.2f}):</strong><br>
                f' = <span class="amber-highlight">{dp_leaky:.2f}</span>
            </div>
            <p style="margin-top: 15px; font-size: 0.85rem; color: #94a3b8; line-height: 1.4;">
                {leaky_note}
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
            In this sandbox, we generate an input signal wave (<i>z</i>) and feed it directly into our activation functions. 
            Watch how the shape of the wave is warped, squashed, and clipped!
            Use the controls in the <b>sidebar (Tab 2: Wave Sandbox)</b> to change the signal type, frequency, and amplitude.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate wave signal. Every shape uses the same period (10 / wave_freq s), so "frequency"
    # means the same thing for all of them: wave_freq full cycles in the 10-second window.
    t = np.linspace(0, 10, 500)
    phase = 2.0 * np.pi * wave_freq * t / 10.0
    
    if wave_type == "Sine Wave":
        raw_signal = wave_amp * np.sin(phase)
    elif wave_type == "Square Wave":
        raw_signal = wave_amp * np.sign(np.sin(phase))
    elif wave_type == "Triangle Wave":
        raw_signal = wave_amp * (2.0 / np.pi) * np.arcsin(np.sin(phase))
    else: # Random Noise: a noisy sine; noise level scales with the amplitude slider
        rng = np.random.default_rng(st.session_state.p65_noise_seed)
        raw_signal = wave_amp * np.sin(phase) + rng.normal(0.0, 0.2 * wave_amp, len(t))
        
    # Process through activations
    sig_signal = sigmoid(raw_signal)
    tanh_signal = tanh_val(raw_signal)
    relu_signal = relu(raw_signal)
    leaky_signal = leaky_relu(raw_signal)
    
    selected_signals = st.multiselect(
        "⚡ Toggle Outputs to Overlay",
        options=["Sigmoid", "tanh", "ReLU", "Leaky ReLU"],
        key="p65_selected_signals",
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
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.03)", range=[float(np.min(raw_signal)) - 0.2, float(np.max(raw_signal)) + 0.2])
        )
        st.plotly_chart(fig_input, width="stretch")
        
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
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.03)", range=[float(min(np.min(raw_signal), np.min(sig_signal), np.min(tanh_signal), np.min(relu_signal), np.min(leaky_signal))) - 0.2, float(max(np.max(raw_signal), np.max(sig_signal), np.max(tanh_signal), np.max(relu_signal), np.max(leaky_signal))) + 0.2])
        )
        st.plotly_chart(fig_output, width="stretch")

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
            This demo is a <b>simplified scalar chain with every connection weight fixed at 1</b>, so each backward step multiplies the error signal by just the <b>activation derivative</b>.
            <br>
            In a general network, each step also multiplies by the corresponding layer weight (or weight matrix); small activation derivatives can still shrink gradients, but the diagram's derivative-only product is not the full gradient for arbitrary weights.
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
        
    d1_act, d2_act, d3_act = float(d1_act), float(d2_act), float(d3_act)

    # Simplified scalar chain: all inter-layer weights are fixed at 1.
    # A general scalar chain also multiplies each step by its connection weight.
    # Flow logic:
    G3 = grad_init
    G2 = G3 * d3_act
    G1 = G2 * d2_act
    G0 = G1 * d1_act

    # Verdicts use the transmitted FRACTION G/G3 (the product of derivatives), so they do not depend
    # on the starting-gradient slider.
    r2, r1, r0 = d3_act, d3_act * d2_act, d3_act * d2_act * d1_act
    VANISHED_RATIO = 0.999e-3  # below ~0.1 % (just under, so Leaky ReLU's 0.1³ floor counts as severe, not vanished)
    SEVERE_RATIO = 0.05        # less than 5 % survives
    HEALTHY_RATIO = 0.5        # at least half survives

    # Format values for display (scientific notation keeps tiny-but-nonzero values distinguishable from 0)
    def clean_format(val):
        if val == 0:
            return "0"
        if abs(val) < 0.001:
            return f"{val:.2e}"
        return f"{val:.4f}"

    def pct_format(ratio):
        pct = ratio * 100.0
        if pct == 0:
            return "0 %"
        if pct < 0.01:
            return f"{pct:.2e} %"
        return f"{pct:.2f} %"

    def link_style(ratio):
        thickness = max(1.5, min(8.0, ratio * 8.0))
        if ratio < VANISHED_RATIO:
            return thickness, "#475569", "none"
        if ratio < SEVERE_RATIO:
            return thickness, "#f87171", "none"
        return thickness, "#eab308", "url(#glow-gold)"

    # Define connection line properties
    # Link 3 (incoming, right)
    t3 = 8
    c3 = "#eab308" # Glowing Gold
    g3 = "url(#glow-gold)"
    t2, c2, g2 = link_style(r2)  # Link 2 (between L3 and L2)
    t1, c1, g1 = link_style(r1)  # Link 1 (between L2 and L1)
    t0, c0, g0 = link_style(r0)  # Link 0 (exit, left)

    # Node warnings (same saturation threshold as the Tab 1 cards)
    def node_warning(d):
        if backprop_act in ["Sigmoid", "tanh"]:
            return "❄️ SATURATED" if d < SATURATION_THRESHOLD else ""
        return "💤 INACTIVE (f′ = 0)" if d == 0 else ""

    node3_warning = node_warning(d3_act)
    node2_warning = node_warning(d2_act)
    node1_warning = node_warning(d1_act)
        
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
                    /* Negative offset moves dashes toward each line's END point. All lines below are
                       drawn right-to-left, so particles travel leftward, i.e. in the backprop direction. */
                    to {{ stroke-dashoffset: -20; }}
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
        {f'<line x1="605" y1="150" x2="470" y2="150" stroke="#fef08a" stroke-width="2" class="flow-g2" filter="{g2}"/>' if r2 > VANISHED_RATIO else ""}

        <!-- Link 1 (Layer 2 Node to Layer 1 Node) -->
        <line x1="380" y1="150" x2="245" y2="150" stroke="{c1}" stroke-width="{t1}" opacity="0.8"/>
        {f'<line x1="380" y1="150" x2="245" y2="150" stroke="#fef08a" stroke-width="2" class="flow-g1" filter="{g1}"/>' if r1 > VANISHED_RATIO else ""}

        <!-- Link 0 (Layer 1 Node to Exit) -->
        <line x1="155" y1="150" x2="50" y2="150" stroke="{c0}" stroke-width="{t0}" opacity="0.8"/>
        {f'<line x1="155" y1="150" x2="50" y2="150" stroke="#fef08a" stroke-width="2" class="flow-g0" filter="{g0}"/>' if r0 > VANISHED_RATIO else ""}

        <!-- GRADIENT VALUE BUBBLES -->
        <rect x="715" y="110" width="70" height="20" rx="5" fill="#1e293b" stroke="#eab308" stroke-width="1.5"/>
        <text x="750" y="124" fill="#fef08a" font-size="11" font-weight="bold" text-anchor="middle">G₃ = {G3:.1f}</text>
        
        <rect x="510" y="110" width="75" height="20" rx="5" fill="#1e293b" stroke="{c2}" stroke-width="1.5"/>
        <text x="547" y="124" fill="#f8fafc" font-size="11" font-weight="600" text-anchor="middle">G₂ = {clean_format(G2)}</text>
        
        <rect x="285" y="110" width="75" height="20" rx="5" fill="#1e293b" stroke="{c1}" stroke-width="1.5"/>
        <text x="322" y="124" fill="#f8fafc" font-size="11" font-weight="600" text-anchor="middle">G₁ = {clean_format(G1)}</text>
        
        <rect x="65" y="110" width="75" height="20" rx="5" fill="#1e293b" stroke="{c0}" stroke-width="1.5"/>
        <text x="102" y="124" fill="#fef08a" font-size="11" font-weight="bold" text-anchor="middle">G₀ = {clean_format(G0)}</text>

        <!-- NEURON NODES (CHAIN OF 3) -->
        <!-- Layer 3 Neuron -->
        <circle cx="650" cy="150" r="45" fill="#0f172a" stroke="{act_theme_color}" stroke-width="3.5" filter="{ 'url(#' + act_theme_glow + ')' if d3_act >= SATURATION_THRESHOLD else 'none' }"/>
        <text x="650" y="132" fill="#cbd5e1" font-size="10.5" font-weight="bold" text-anchor="middle">LAYER 3</text>
        <text x="650" y="152" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="middle">z₃ = {z3:+.1f}</text>
        <text x="650" y="172" fill="{act_theme_color}" font-size="11" font-weight="900" text-anchor="middle">f'(z₃) = {d3_act:.3f}</text>
        {f'<text x="650" y="215" fill="#f87171" font-size="10" font-weight="bold" text-anchor="middle">{node3_warning}</text>' if node3_warning else ""}

        <!-- Layer 2 Neuron -->
        <circle cx="425" cy="150" r="45" fill="#0f172a" stroke="{act_theme_color}" stroke-width="3.5" filter="{ 'url(#' + act_theme_glow + ')' if d2_act >= SATURATION_THRESHOLD else 'none' }"/>
        <text x="425" y="132" fill="#cbd5e1" font-size="10.5" font-weight="bold" text-anchor="middle">LAYER 2</text>
        <text x="425" y="152" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="middle">z₂ = {z2:+.1f}</text>
        <text x="425" y="172" fill="{act_theme_color}" font-size="11" font-weight="900" text-anchor="middle">f'(z₂) = {d2_act:.3f}</text>
        {f'<text x="425" y="215" fill="#f87171" font-size="10" font-weight="bold" text-anchor="middle">{node2_warning}</text>' if node2_warning else ""}

        <!-- Layer 1 Neuron -->
        <circle cx="200" cy="150" r="45" fill="#0f172a" stroke="{act_theme_color}" stroke-width="3.5" filter="{ 'url(#' + act_theme_glow + ')' if d1_act >= SATURATION_THRESHOLD else 'none' }"/>
        <text x="200" y="132" fill="#cbd5e1" font-size="10.5" font-weight="bold" text-anchor="middle">LAYER 1</text>
        <text x="200" y="152" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="middle">z₁ = {z1:+.1f}</text>
        <text x="200" y="172" fill="{act_theme_color}" font-size="11" font-weight="900" text-anchor="middle">f'(z₁) = {d1_act:.3f}</text>
        {f'<text x="200" y="215" fill="#f87171" font-size="10" font-weight="bold" text-anchor="middle">{node1_warning}</text>' if node1_warning else ""}

        <!-- FLOW DIRECTION INDICATORS (BACKWARD ARROWS ON TOP) -->
        <path d="M 450,40 L 400,40" stroke="#fef08a" stroke-width="2.5" fill="none" marker-end="url(#arrow)" />
        <text x="425" y="28" fill="#fef08a" font-size="11" font-weight="900" text-anchor="middle">ERROR FLOW DIRECTION (BACKPROP)</text>
        <text x="425" y="282" fill="#94a3b8" font-size="11" font-weight="bold" text-anchor="middle">SIMPLIFIED SCALAR CHAIN · INTER-LAYER WEIGHTS FIXED AT 1</text>
        
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
            <div class="card-title">🏁 Backprop Race Verdict · Unit-Weight Toy Chain</div>
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
                    <td style="padding:10px 5px; font-weight:600;">Gradient Transmission (weights = 1)</td>
                    <td style="padding:10px 5px; font-weight:700;">{pct_format(r0)}</td>
                </tr>
            </table>
            <p style="margin:10px 5px 0; color:#94a3b8; font-size:0.9rem;">
                Here G₂ = G₃ × f′(z₃), G₁ = G₂ × f′(z₂), and G₀ = G₁ × f′(z₁). A general network also multiplies each step by the corresponding connection weight (or weight matrix).
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_v2:
        # Verdict is based on the transmitted fraction r0 = G0 / G3, not on the absolute G0
        def verdict_badge_html(color, glow_rgba, text):
            return (f"<span style='background:{color}; color:#0b0f19; font-weight:800; padding:6px 12px; "
                    f"border-radius:30px; box-shadow: 0 0 15px {glow_rgba}; display:inline-block;'>{text}</span>")

        shrink_reasons = {
            "Sigmoid": "Sigmoid's derivative is at most <b>0.25</b> (reached only at z = 0), so a 3-layer chain keeps at most "
                       "0.25 × 0.25 × 0.25 ≈ <b>1.6 %</b> of the error, even in the best case.",
            "tanh": "tanh's derivative is 1 at z = 0 but drops quickly as |z| grows (f′(1) ≈ 0.42, f′(2) ≈ 0.07), "
                    "and the per-layer factors multiply.",
            "Leaky ReLU": "Every layer whose input is not positive multiplies the gradient by α = 0.1 instead of 1. "
                          "The gradient never becomes exactly zero, so these units can still learn, but several such "
                          "layers still shrink it a lot (two layers keep 1 %, three keep 0.1 %).",
            "ReLU": "ReLU's derivative is exactly 1 for positive inputs and exactly 0 otherwise.",
        }
        kept = f"The error signal went from <b>{grad_init:.1f}</b> to <b>{clean_format(G0)}</b> ({pct_format(r0)} kept). "

        if r0 == 0:
            verdict_style = "border: 2px solid #ef4444; background: rgba(239, 68, 68, 0.08);"
            verdict_badge = verdict_badge_html("#ef4444", "rgba(239, 68, 68, 0.4)", "⛔ GRADIENT BLOCKED (exactly 0)")
            reason = ("At least one layer input is <b>negative or zero</b>. ReLU's derivative there is exactly 0 "
                      "(at the kink z = 0 we use the convention f′(0) = 0), so the chain rule multiplies the whole "
                      "gradient by 0 and the earlier layers receive nothing <i>for this input</i>. If a unit stays in "
                      "that region for <i>every</i> input in the data it never updates again: the <b>dead ReLU problem</b>.")
        elif r0 < VANISHED_RATIO:
            verdict_style = "border: 2px solid #ef4444; background: rgba(239, 68, 68, 0.08);"
            verdict_badge = verdict_badge_html("#ef4444", "rgba(239, 68, 68, 0.4)", "⚠️ GRADIENT VANISHED")
            reason = kept + ("Your neuron inputs sit in the <b>saturation zones</b> (deep positive or deep negative), where "
                             "the Sigmoid/tanh derivatives are extremely close to zero. Multiplying three of them leaves "
                             "virtually nothing for Layer 1. This is the classic <b>vanishing gradient problem</b>.")
        elif r0 < SEVERE_RATIO:
            verdict_style = "border: 2px solid #f59e0b; background: rgba(245, 158, 11, 0.08);"
            verdict_badge = verdict_badge_html("#f59e0b", "rgba(245, 158, 11, 0.4)", "⚠️ SEVERE VANISHING GRADIENT")
            reason = kept + shrink_reasons[backprop_act] + " Layer 1 learns far more slowly than Layer 3."
        elif r0 < HEALTHY_RATIO:
            verdict_style = "border: 2px solid #facc15; background: rgba(250, 204, 21, 0.06);"
            verdict_badge = verdict_badge_html("#facc15", "rgba(250, 204, 21, 0.4)", "🟡 GRADIENT WEAKENED")
            reason = kept + shrink_reasons[backprop_act]
        else:
            verdict_style = "border: 2px solid #22c55e; background: rgba(34, 197, 94, 0.08);"
            verdict_badge = verdict_badge_html("#22c55e", "rgba(34, 197, 94, 0.4)", "⚡ GRADIENT HEALTHY")
            reason = kept + ("At least half of the error reaches the early weights because every derivative multiplier "
                             "stays close to 1 (ReLU/Leaky ReLU with positive inputs, or tanh near z = 0). "
                             "Sigmoid can never get here: its derivative is at most 0.25.")
            
        st.markdown(f"""
        <div class="custom-card" style="{verdict_style} height: 100%;">
            {verdict_badge}
            <h4 style="margin-top: 15px; color:#f8fafc;">What is happening here?</h4>
            <p style="font-size: 1.05rem; line-height: 1.6; color: #cbd5e1; margin-bottom: 0;">{reason}</p>
        </div>
        """, unsafe_allow_html=True)

# Interactive Summary & Review Challenge
sigmoid_chain_at_4 = grad_init * float(sigmoid_derivative(4.0)) ** 3
leaky_chain_negative = grad_init * LEAKY_ALPHA ** 3
st.markdown("---")
st.markdown(f"""
<div class="custom-card">
    <h3 style="color: #38bdf8; margin-top: 0;">🎓 Quick Challenge Zone!</h3>
    <p style="font-size: 1.05rem; line-height: 1.6; color: #cbd5e1; margin-bottom: 15px;">
        Let's put your new intuition to the test! Try completing these three laboratory tasks using the controls in the sidebar:
    </p>
    <ul style="line-height: 1.8; color: #cbd5e1; margin-bottom: 0;">
        <li><b>Challenge 1: The Sigmoid Freeze ❄️</b><br>
            Set the <b>Common Input z</b> to <b>+4.0</b> (using Lock Inputs) under the <b>Sigmoid</b> engine. Go to Tab 3. 
            Notice how tiny the derivatives are (f′(4) ≈ 0.018), and see how the incoming error of {grad_init:g} shrinks to about {sigmoid_chain_at_4:.1e}. 
            This is a major reason sigmoid is rarely used in the hidden layers of deep networks.
        </li>
        <li><b>Challenge 2: ReLU Block vs. Leaky Leak 🧟‍♂️</b><br>
            In Tab 3, select the <b>ReLU</b> engine and set <b>Common Input z</b> to <b>-1.0</b>. 
            The error enters at Layer 3 and is cut to exactly <b>0</b> right there (f′ = 0 for negative inputs), so nothing reaches Layers 2 and 1. 
            Now switch the engine to <b>Leaky ReLU</b>. The gradient is no longer exactly zero: each layer passes 10 %, so
            G₀ = {grad_init:g} × 0.1³ = {leaky_chain_negative:.4f} (0.1 % kept). 
            The leak keeps the units trainable, but it does not undo the shrinkage: the verdict still reads <b>severe vanishing gradient</b>.
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
safe_page_link("pages/66Stacking Linear Layers Collapses.py", "Next: 66 · Stacking Linear Layers Collapses", icon="➡️")