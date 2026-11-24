import sys
from pathlib import Path

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from common.mathutils import sigmoid, softmax  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

# Page setup
st.set_page_config(
    page_title="67: Neural Network as Matrix Layers - Space Warping Engine",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper function to render multi-line HTML without Markdown code-block parsing issues
def render_html(html_str):
    cleaned = "\n".join([line.strip() for line in html_str.split("\n")])
    st.markdown(cleaned, unsafe_allow_html=True)

# Custom Cyberpunk & Glassmorphic CSS Styling
render_html("""
<style>
    /* Dark Theme Base Adjustments */
    .stApp {
        background: #0b0f19 !important;
        color: #f1f5f9 !important;
    }
    
    /* Base text colours. No !important and no blanket `span` rule, so that the
       highlight classes and inline style="color: ..." legends keep their colours. */
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
    
    /* Color Highlights */
    .cyan-highlight {
        background: rgba(6, 182, 212, 0.15) !important;
        color: #22d3ee !important;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: monospace;
        font-weight: bold;
    }
    
    .pink-highlight {
        background: rgba(236, 72, 153, 0.15) !important;
        color: #f472b6 !important;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: monospace;
        font-weight: bold;
    }
    
    .green-highlight {
        background: rgba(34, 197, 94, 0.15) !important;
        color: #4ade80 !important;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: monospace;
        font-weight: bold;
    }
    
    .gold-highlight {
        background: rgba(234, 179, 8, 0.15) !important;
        color: #fbbf24 !important;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: monospace;
        font-weight: bold;
    }

    .red-highlight {
        background: rgba(239, 68, 68, 0.15) !important;
        color: #fca5a5 !important;
        padding: 2px 6px;
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

    .glow-badge-gold {
        background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
        color: #0b0f19 !important;
        font-weight: 800;
        padding: 6px 12px;
        border-radius: 30px;
        box-shadow: 0 0 15px rgba(234, 179, 8, 0.4);
        display: inline-block;
    }
    
    /* LaTeX-style Matrix Box */
    .matrix-container {
        display: inline-flex;
        align-items: center;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        margin: 5px 10px;
    }
    
    .matrix-brackets {
        display: inline-flex;
        border-left: 3px solid #cbd5e1;
        border-right: 3px solid #cbd5e1;
        border-radius: 6px;
        padding: 4px 6px;
        background: rgba(0, 0, 0, 0.2);
    }
    
    .matrix-grid {
        display: grid;
        gap: 6px 12px;
        text-align: center;
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
""")

# Helper functions for calculations
def relu(z):
    return np.maximum(0.0, z)

ACTIVATIONS = {"tanh": np.tanh, "Sigmoid": sigmoid, "ReLU": relu}

# Planet Brain presets. All values sit on the sliders' 0.5 grid and inside their bounds
# (weights within ±5, biases within ±3). Each description was checked against the
# decision map this network actually produces on the input square [-2, 2] x [-2, 2].
PRESETS = {
    "🌌 Goldilocks Zone Brain": {
        "desc": (
            "Habitable ONLY for moderate temperature AND moderate gravity: the habitable pocket is the "
            "hexagon |x₁| ≤ 1 and |x₁| + 1.5·|x₂| ≤ 2 (so |x₂| ≤ 1.33 at most). Each ReLU unit is an 'alarm': "
            "h₁ fires for hot/heavy, h₂ for hot/light, h₃ for cold planets, and every alarm votes 'barren'."
        ),
        "w1": [[2.0, 3.0], [2.0, -3.0], [-2.0, 0.0]],
        "b1": [0.0, 0.0, 0.0],
        "w2": [[-0.5, -0.5, -1.0], [0.5, 0.5, 1.0]],
        "b2": [2.0, -2.0],
        "act": "ReLU"
    },
    "🪐 Gravity Cautious Brain": {
        "desc": (
            "Gravity-first filter: every low-gravity planet (x₂ ≲ −0.2) is habitable at any temperature. "
            "Above that, the cut-off slants: the heavier the planet, the hotter it must be to pass "
            "(at x₂ = +2 only x₁ ≳ 1 survives), so heavy, cold worlds are barren; very hot planets pass at any gravity."
        ),
        "w1": [[0.5, -4.5], [1.5, -2.5], [-0.5, 0.5]],
        "b1": [0.5, -0.5, 0.0],
        "w2": [[2.0, 1.0, -2.0], [-2.0, -2.0, 2.0]],
        "b2": [1.0, -1.0],
        "act": "ReLU"
    },
    "❄️ Frozen Oceans Brain": {
        "desc": (
            "Favors cold worlds (possible ice-covered oceans): every planet with x₁ ≲ 0 is habitable at any gravity, "
            "and so is every low-gravity planet (x₂ ≲ −0.2). Only warm, higher-gravity worlds come out barren."
        ),
        "w1": [[-4.0, 0.5], [0.5, 3.0], [1.0, -1.5]],
        "b1": [1.0, -0.5, -0.5],
        "w2": [[4.0, -2.0, 3.0], [-4.0, 2.0, -3.0]],
        "b2": [-1.5, 1.5],
        "act": "Sigmoid"
    },
    "🎲 Untrained Brain": {
        "desc": (
            "Arbitrary, untrained weights (fixed so the lesson is reproducible). Its decision is essentially one "
            "tilted boundary: only hot planets (x₁ ≳ 0.1 at x₂ = −2, x₁ ≳ 1.1 at x₂ = +2) are called "
            "habitable. Training would be needed to make it useful."
        ),
        "w1": [[-1.0, 2.0], [2.0, -0.5], [-1.5, -2.0]],
        "b1": [0.5, -1.0, 1.0],
        "w2": [[-1.5, 2.5, -1.0], [1.0, -2.0, 1.5]],
        "b2": [-0.5, 0.5],
        "act": "tanh"
    }
}
DEFAULT_PRESET = "🌌 Goldilocks Zone Brain"

# All session keys are prefixed with "p67_" because st.session_state is shared by every page
# (pages 4 and 5 also use a widget key named "x2").
W1_KEYS = [[f"p67_w1_{r}{c}" for c in (1, 2)] for r in (1, 2, 3)]
B1_KEYS = [f"p67_b1_{r}" for r in (1, 2, 3)]
W2_KEYS = [[f"p67_w2_{r}{c}" for c in (1, 2, 3)] for r in (1, 2)]
B2_KEYS = [f"p67_b2_{r}" for r in (1, 2)]
SUB = {1: "₁", 2: "₂", 3: "₃"}


def preset_state(preset_name):
    """Map every widget key to the value defined by the given preset."""
    p = PRESETS[preset_name]
    state = {"p67_act": p["act"]}
    for r, row in enumerate(W1_KEYS):
        for c, key in enumerate(row):
            state[key] = float(p["w1"][r][c])
    for r, key in enumerate(B1_KEYS):
        state[key] = float(p["b1"][r])
    for r, row in enumerate(W2_KEYS):
        for c, key in enumerate(row):
            state[key] = float(p["w2"][r][c])
    for r, key in enumerate(B2_KEYS):
        state[key] = float(p["b2"][r])
    return state


def load_preset(preset_name):
    for key, val in preset_state(preset_name).items():
        st.session_state[key] = val
    st.session_state.p67_preset = preset_name


# Initialize session state (widget keys are re-seeded if Streamlit dropped them after a page switch)
st.session_state.setdefault("p67_x1", 0.5)
st.session_state.setdefault("p67_x2", -0.3)
if "p67_preset" not in st.session_state:
    load_preset(DEFAULT_PRESET)
else:
    for _key, _val in preset_state(st.session_state.p67_preset).items():
        st.session_state.setdefault(_key, _val)

# Sidebar configuration
st.sidebar.markdown("""
<div style="text-align: center; padding-bottom: 10px;">
    <h2 style="color: #38bdf8; margin-bottom: 0;">🛠️ Network Architecture</h2>
    <p style="color: #94a3b8; font-size: 0.9rem;">Interactive Planet Habitation Scanner</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 📥 Input Features (Planet Characteristics)")
st.sidebar.caption("Provide characteristics of the scanned planet to feed into the input vector X.")

x1_slider = st.sidebar.slider(
    "Temperature Index (x₁)",
    min_value=-2.0,
    max_value=2.0,
    step=0.1,
    key="p67_x1",
    help="-2.0 represents freezing cold; +2.0 represents scorching hot."
)

x2_slider = st.sidebar.slider(
    "Gravity Index (x₂)",
    min_value=-2.0,
    max_value=2.0,
    step=0.1,
    key="p67_x2",
    help="-2.0 represents microgravity; +2.0 represents crushing gravity."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ Layer 1 Matrix Controller")
st.sidebar.caption("Configure the 3×2 Weight Matrix W¹ and 3×1 Bias vector b¹ for the Hidden Layer.")

# W1 controls: row r = hidden neuron h_r, column c = input feature x_c
st.sidebar.markdown("##### Weight Matrix W¹ (Dimension 3 × 2)")
col1, col2 = st.sidebar.columns(2)
for c, (col, feat) in enumerate(((col1, "temp"), (col2, "grav")), start=1):
    with col:
        for r in (1, 2, 3):
            st.slider(f"w¹{SUB[r]}{SUB[c]} ({feat} → h{SUB[r]})", -5.0, 5.0, step=0.5, key=W1_KEYS[r - 1][c - 1])

# b1 controls
st.sidebar.markdown("##### Bias Vector b¹ (Dimension 3 × 1)")
for r, col in enumerate(st.sidebar.columns(3), start=1):
    with col:
        st.slider(f"b¹{SUB[r]}", -3.0, 3.0, step=0.5, key=B1_KEYS[r - 1])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ Layer 2 Matrix Controller")
st.sidebar.caption("Configure the 2×3 Weight Matrix W² and 2×1 Bias vector b² for the Output Layer.")

# W2 controls: row r = output class, column c = hidden neuron h_c
st.sidebar.markdown("##### Weight Matrix W² (Dimension 2 × 3)")
for c, col in enumerate(st.sidebar.columns(3), start=1):
    with col:
        st.slider(f"w²₁{SUB[c]} (h{SUB[c]} → habitable)", -5.0, 5.0, step=0.5, key=W2_KEYS[0][c - 1])
        st.slider(f"w²₂{SUB[c]} (h{SUB[c]} → barren)", -5.0, 5.0, step=0.5, key=W2_KEYS[1][c - 1])

# b2 controls
st.sidebar.markdown("##### Bias Vector b² (Dimension 2 × 1)")
col_b2_1, col_b2_2 = st.sidebar.columns(2)
with col_b2_1:
    st.slider("b²₁ (hab)", -3.0, 3.0, step=0.5, key=B2_KEYS[0])
with col_b2_2:
    st.slider("b²₂ (bar)", -3.0, 3.0, step=0.5, key=B2_KEYS[1])

# Main header
st.title("Page 67: Neural Network as Matrix Layers")
st.subheader("W¹X + b¹ → g(z) → W²A¹ + b² → Softmax | Feedforward Math & Space Warping 🌌")

render_html("""
<div class="custom-card">
    <h3>👋 Stacking Neurons: From Dot Products to Matrix Equations</h3>
    <p style="font-size: 1.1rem; line-height: 1.6; color: #cbd5e1;">
        In past simulations, we built a single neuron. But real AI systems don't calculate one dot product at a time. 
        They process entire groups of neurons simultaneously by packing their connections into <b>Weight Matrices (W)</b> 
        and <b>Bias Vectors (b)</b>!
    </p>
    <p style="font-size: 1.05rem; line-height: 1.6; color: #cbd5e1; margin-bottom: 0;">
        A neural network layer applies an <b>affine transformation</b> followed by an <b>Activation Function</b>:
        <span class="cyan-highlight">A = g(WX + b)</span>. 
        Stacking layers is just feeding the output of one matrix transformation directly into the next! Below, we visualize 
        exactly how mathematical variables flow through layers and geometrically warp space to make deep learning possible.
    </p>
</div>
""")

# Render presets
st.markdown("##### 🪐 Load a Preconfigured Brain Design (each preset loads a full set of weights and biases)")
preset_cols = st.columns(len(PRESETS))
for idx, (p_name, p_val) in enumerate(PRESETS.items()):
    with preset_cols[idx]:
        st.button(
            p_name, width="stretch", help=p_val["desc"], key=f"p67_preset_btn_{idx}",
            on_click=load_preset, args=(p_name,),
        )

# Select Activation Function
act_func = st.selectbox(
    "🔬 Choose Hidden Layer Activation Function (g)",
    options=list(ACTIVATIONS),
    key="p67_act",
    help="Determines the warping profile applied to the hidden neurons."
)

# Core Forward Pass Computations
X = np.array([x1_slider, x2_slider])
W1_arr = np.array([[st.session_state[k] for k in row] for row in W1_KEYS])
b1_arr = np.array([st.session_state[k] for k in B1_KEYS])
W2_arr = np.array([[st.session_state[k] for k in row] for row in W2_KEYS])
b2_arr = np.array([st.session_state[k] for k in B2_KEYS])

# Tell the learner which preset is active, or that the weights were customized
active_preset = st.session_state.p67_preset
_current = {k: st.session_state[k] for k in preset_state(active_preset)}
if _current == preset_state(active_preset):
    st.info(f"**Active preset: {active_preset}.** {PRESETS[active_preset]['desc']}")
else:
    st.info(
        f"**Custom weights** (started from {active_preset}). The preset description no longer applies; "
        "check Tab 3 to see what this network actually predicts."
    )

# Layer 1: W¹ (3×2) @ X (2,) + b¹ (3,) -> Z¹ (3,)
Z1 = W1_arr @ X + b1_arr
A1 = ACTIVATIONS[act_func](Z1)

# Layer 2: W² (2×3) @ A¹ (3,) + b² (2,) -> Z² (2,)
Z2 = W2_arr @ A1 + b2_arr
Y = softmax(Z2, axis=0)

# Visualizing results
habitable_pct = Y[0] * 100
barren_pct = Y[1] * 100

# Core Tabs Setup
tab_math, tab_network, tab_warp = st.tabs([
    "🧮 Tab 1: The Feedforward Factory",
    "🌐 Tab 2: The Pulsing Synapse Network",
    "🌀 Tab 3: The Space-Warping Grid"
])

# ==========================================
# TAB 1: THE FEEDFORWARD FACTORY
# ==========================================
with tab_math:
    render_html("""
    <div style="margin-top: 15px; margin-bottom: 25px;">
        <h3>🧮 Live Forward Pass Matrix Mathematics</h3>
        <p style="color: #cbd5e1; font-size: 1.05rem; line-height: 1.6;">
            Watch the raw arithmetic unfold in real time! As you adjust weights in the sidebar, these equations update live. 
            Notice how dimensions multiply perfectly: a <span class="cyan-highlight">3×2</span> matrix times a <span class="cyan-highlight">2×1</span> vector yields a <span class="cyan-highlight">3×1</span> hidden vector.
        </p>
    </div>
    """)
    
    # Custom matrix visualization HTML generators
    def html_vector_2d(vec, color="#22d3ee"):
        return f"""
        <div class="matrix-container">
            <div class="matrix-brackets">
                <div class="matrix-grid" style="grid-template-columns: 1fr;">
                    <div style="color: {color};">{vec[0]:.2f}</div>
                    <div style="color: {color};">{vec[1]:.2f}</div>
                </div>
            </div>
        </div>
        """
        
    def html_matrix_3x2(mat):
        return f"""
        <div class="matrix-container">
            <div class="matrix-brackets">
                <div class="matrix-grid" style="grid-template-columns: 1fr 1fr;">
                    <div style="color: #c084fc;">{mat[0][0]:+.1f}</div> <div style="color: #c084fc;">{mat[0][1]:+.1f}</div>
                    <div style="color: #c084fc;">{mat[1][0]:+.1f}</div> <div style="color: #c084fc;">{mat[1][1]:+.1f}</div>
                    <div style="color: #c084fc;">{mat[2][0]:+.1f}</div> <div style="color: #c084fc;">{mat[2][1]:+.1f}</div>
                </div>
            </div>
        </div>
        """

    def html_vector_3d(vec, color="#38bdf8"):
        return f"""
        <div class="matrix-container">
            <div class="matrix-brackets">
                <div class="matrix-grid" style="grid-template-columns: 1fr;">
                    <div style="color: {color};">{vec[0]:.3f}</div>
                    <div style="color: {color};">{vec[1]:.3f}</div>
                    <div style="color: {color};">{vec[2]:.3f}</div>
                </div>
            </div>
        </div>
        """

    def html_matrix_2x3(mat):
        return f"""
        <div class="matrix-container">
            <div class="matrix-brackets">
                <div class="matrix-grid" style="grid-template-columns: 1fr 1fr 1fr;">
                    <div style="color: #f472b6;">{mat[0][0]:+.1f}</div> <div style="color: #f472b6;">{mat[0][1]:+.1f}</div> <div style="color: #f472b6;">{mat[0][2]:+.1f}</div>
                    <div style="color: #f472b6;">{mat[1][0]:+.1f}</div> <div style="color: #f472b6;">{mat[1][1]:+.1f}</div> <div style="color: #f472b6;">{mat[1][2]:+.1f}</div>
                </div>
            </div>
        </div>
        """

    step1, step2 = st.columns(2, gap="large")
    
    with step1:
        st.markdown("#### ⚡ Step 1: Input Vector (X)")
        render_html(f"""
        <div class="custom-card" style="border-left: 5px solid #06b6d4; height: 90%;">
            <p>Features of our scanned planet:</p>
            <div style="text-align: center; margin: 15px 0;">
                <span style="font-family: monospace; font-size: 1.1rem; color: #a5f3fc;">X = </span>
                {html_vector_2d(X)}
                <div style="font-size: 0.85rem; color: #94a3b8; margin-top: 10px;">
                    x₁ (Temp) = <span class="cyan-highlight">{X[0]:+.2f}</span><br>
                    x₂ (Grav) = <span class="cyan-highlight">{X[1]:+.2f}</span>
                </div>
            </div>
        </div>
        """)
        
        st.markdown("#### 🚀 Step 2: Hidden Linear Mapping (Z¹ = W¹X + b¹)")
        render_html(f"""
        <div class="custom-card" style="border-left: 5px solid #c084fc; height: 92%;">
            <p>Multiplying Input by the 3×2 Weight Matrix, then adding 3×1 Bias vector:</p>
            <div style="text-align: center; margin: 15px 0; display: flex; justify-content: center; align-items: center; flex-wrap: wrap;">
                <span style="font-family: monospace; font-size: 1.1rem; color: #e9d5ff;">Z¹ = </span>
                {html_matrix_3x2(W1_arr)}
                <span style="font-family: monospace; font-size: 1.2rem; margin: 0 5px;">·</span>
                {html_vector_2d(X)}
                <span style="font-family: monospace; font-size: 1.2rem; margin: 0 5px;">+</span>
                {html_vector_3d(b1_arr, "#cbd5e1")}
                <span style="font-family: monospace; font-size: 1.1rem; margin: 0 10px; color: #38bdf8;">=</span>
                {html_vector_3d(Z1, "#38bdf8")}
            </div>
            <div style="background: rgba(0,0,0,0.3); padding: 12px; border-radius: 8px; font-family: monospace; font-size: 0.85rem; border: 1px solid rgba(255,255,255,0.05);">
                <strong>Detailed calculation:</strong><br>
                z¹₁ = ({W1_arr[0][0]:+.1f}·{X[0]:.2f}) + ({W1_arr[0][1]:+.1f}·{X[1]:.2f}) + {b1_arr[0]:+.1f} = <span class="cyan-highlight">{Z1[0]:+.3f}</span><br>
                z¹₂ = ({W1_arr[1][0]:+.1f}·{X[0]:.2f}) + ({W1_arr[1][1]:+.1f}·{X[1]:.2f}) + {b1_arr[1]:+.1f} = <span class="cyan-highlight">{Z1[1]:+.3f}</span><br>
                z¹₃ = ({W1_arr[2][0]:+.1f}·{X[0]:.2f}) + ({W1_arr[2][1]:+.1f}·{X[1]:.2f}) + {b1_arr[2]:+.1f} = <span class="cyan-highlight">{Z1[2]:+.3f}</span>
            </div>
        </div>
        """)

    with step2:
        st.markdown(f"#### 🧬 Step 3: Activation Warping (A¹ = {act_func}(Z¹))")
        render_html(f"""
        <div class="custom-card" style="border-left: 5px solid #22c55e; height: 90%;">
            <p>Applying the activation function <b>{act_func}</b> element-wise to squeeze signals:</p>
            <div style="text-align: center; margin: 15px 0; display: flex; justify-content: center; align-items: center;">
                <span style="font-family: monospace; font-size: 1.1rem; color: #bbf7d0;">A¹ = g( </span>
                {html_vector_3d(Z1, "#38bdf8")}
                <span style="font-family: monospace; font-size: 1.1rem; margin: 0 5px; color: #bbf7d0;">) = </span>
                {html_vector_3d(A1, "#4ade80")}
            </div>
            <div style="background: rgba(0,0,0,0.3); padding: 12px; border-radius: 8px; font-family: monospace; font-size: 0.85rem; border: 1px solid rgba(255,255,255,0.05);">
                <strong>Applying function profiles:</strong><br>
                g({Z1[0]:+.3f}) = <span class="green-highlight">{A1[0]:.3f}</span><br>
                g({Z1[1]:+.3f}) = <span class="green-highlight">{A1[1]:.3f}</span><br>
                g({Z1[2]:+.3f}) = <span class="green-highlight">{A1[2]:.3f}</span>
            </div>
        </div>
        """)
        
        st.markdown("#### 🏁 Step 4 & 5: Output (Z² = W²A¹ + b²) & Softmax")
        render_html(f"""
        <div class="custom-card" style="border-left: 5px solid #fbbf24; height: 92%;">
            <p>1. Multiplying Hidden activations by Output matrix, then adding biases:</p>
            <div style="text-align: center; margin: 15px 0; display: flex; justify-content: center; align-items: center; flex-wrap: wrap;">
                <span style="font-family: monospace; font-size: 1.1rem; color: #fbcfe8;">Z² = </span>
                {html_matrix_2x3(W2_arr)}
                <span style="font-family: monospace; font-size: 1.2rem; margin: 0 5px;">·</span>
                {html_vector_3d(A1, "#4ade80")}
                <span style="font-family: monospace; font-size: 1.2rem; margin: 0 5px;">+</span>
                {html_vector_2d(b2_arr, "#cbd5e1")}
                <span style="font-family: monospace; font-size: 1.1rem; margin: 0 10px; color: #f472b6;">=</span>
                {html_vector_2d(Z2, "#f472b6")}
            </div>
            <p>2. Squash raw scores through <b>Softmax</b> to yield final class probabilities:</p>
            <div style="text-align: center; margin: 15px 0; display: flex; justify-content: center; align-items: center;">
                <span style="font-family: monospace; font-size: 1.1rem; color: #fde047;">Y = Softmax( </span>
                {html_vector_2d(Z2, "#f472b6")}
                <span style="font-family: monospace; font-size: 1.1rem; margin: 0 5px; color: #fde047;">) = </span>
                <div class="matrix-container">
                    <div class="matrix-brackets">
                        <div class="matrix-grid" style="grid-template-columns: 1fr;">
                            <div style="color: #fbbf24; font-weight: 900;">{Y[0]:.4f} (Hab)</div>
                            <div style="color: #fca5a5;">{Y[1]:.4f} (Bar)</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """)

    # Diagnostic Output display
    st.markdown("### 📊 Scanning Verdict")
    if Y[0] >= 0.5:
        render_html(f"""
        <div style="background: rgba(34, 197, 94, 0.1); border: 2px solid #22c55e; border-radius: 12px; padding: 20px; box-shadow: 0 0 15px rgba(34,197,94,0.2);">
            <span class="glow-badge-cyan">🪐 HABITABLE PLANET DETECTED!</span>
            <p style="margin-top: 12px; color: #d1fae5; font-size: 1.1rem; line-height: 1.6;">
                Under the selected weights, softmax assigns <b>{habitable_pct:.1f}%</b> probability to the habitable class (and {barren_pct:.1f}% to barren). These illustrative outputs are not calibrated real-world confidence or evidence of habitability.
            </p>
        </div>
        """)
    else:
        render_html(f"""
        <div style="background: rgba(239, 68, 68, 0.1); border: 2px solid #ef4444; border-radius: 12px; padding: 20px; box-shadow: 0 0 15px rgba(239,68,68,0.2);">
            <span class="glow-badge-gold">💀 BARREN WASTELAND DETECTED!</span>
            <p style="margin-top: 12px; color: #fee2e2; font-size: 1.1rem; line-height: 1.6;">
                Under the selected weights, softmax assigns <b>{barren_pct:.1f}%</b> probability to the barren class (and {habitable_pct:.1f}% to habitable). These illustrative outputs are not calibrated real-world confidence or evidence about a planet.
            </p>
        </div>
        """)

# ==========================================
# TAB 2: THE PULSING SYNAPSE NETWORK
# ==========================================
with tab_network:
    render_html("""
    <div style="margin-top: 15px; margin-bottom: 25px;">
        <h3>🌐 Data Flow Visualization: Live Neural Circuit</h3>
        <p style="color: #cbd5e1; font-size: 1.05rem; line-height: 1.6;">
            A visual representation of the scanned features flowing through the network layers. 
            <b>Line thickness</b> shows the size of the weight |w|. <b>Line color</b> shows the sign of the signal actually sent along it,
            the contribution w·(input): <span style="color: #06b6d4; font-weight: bold;">cyan = pushes the next neuron up (excitatory)</span>,
            <span style="color: #ef4444; font-weight: bold;">red = pushes it down (inhibitory)</span>,
            <span style="color: #94a3b8; font-weight: bold;">gray = (almost) nothing transmitted</span>.
            A negative weight times a negative input is therefore cyan. Moving particles show |w·input|: faster = larger contribution,
            no particles = zero contribution (for example a ReLU neuron that outputs 0).
        </p>
    </div>
    """)

    # Edge styling is driven by the contribution w * signal, not by the weight alone
    def get_weight_svg_props(w, signal):
        contribution = w * signal
        if abs(contribution) < 0.05:
            color = "#475569"
        else:
            color = "#06b6d4" if contribution > 0 else "#ef4444"

        thick = max(1.5, min(8.5, abs(w) * 1.5))
        flow_speed = max(0.4, min(4.0, 2.0 / abs(contribution))) if abs(contribution) > 0.01 else 4.0
        flowing = abs(contribution) > 0.05
        return color, thick, flow_speed, flowing

    c11, t11, s11, f11 = get_weight_svg_props(W1_arr[0][0], X[0])
    c12, t12, s12, f12 = get_weight_svg_props(W1_arr[0][1], X[1])
    c21, t21, s21, f21 = get_weight_svg_props(W1_arr[1][0], X[0])
    c22, t22, s22, f22 = get_weight_svg_props(W1_arr[1][1], X[1])
    c31, t31, s31, f31 = get_weight_svg_props(W1_arr[2][0], X[0])
    c32, t32, s32, f32 = get_weight_svg_props(W1_arr[2][1], X[1])

    c_o11, t_o11, s_o11, f_o11 = get_weight_svg_props(W2_arr[0][0], A1[0])
    c_o12, t_o12, s_o12, f_o12 = get_weight_svg_props(W2_arr[0][1], A1[1])
    c_o13, t_o13, s_o13, f_o13 = get_weight_svg_props(W2_arr[0][2], A1[2])
    c_o21, t_o21, s_o21, f_o21 = get_weight_svg_props(W2_arr[1][0], A1[0])
    c_o22, t_o22, s_o22, f_o22 = get_weight_svg_props(W2_arr[1][1], A1[1])
    c_o23, t_o23, s_o23, f_o23 = get_weight_svg_props(W2_arr[1][2], A1[2])

    def get_glow_filter(val):
        if val > 0.5: return "url(#glow-cyan)"
        if val < -0.5: return "url(#glow-red)"
        return "none"

    svg_content = f"""
    <svg viewBox="0 0 850 400" width="100%" height="100%" style="background:#0e1626; border-radius:16px; border:1px solid rgba(255,255,255,0.05); box-shadow: inset 0 0 40px rgba(0,0,0,0.5);">
        <defs>
            <filter id="glow-cyan" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="6" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
            <filter id="glow-gold" x="-30%" y="-30%" width="160%" height="160%">
                <feGaussianBlur stdDeviation="10" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
            <filter id="glow-red" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="6" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
            
            <style>
                @keyframes pulse-flow-rev {{
                    to {{ stroke-dashoffset: -20; }}
                }}
                .flow-11 {{ stroke-dasharray: 6 5; animation: pulse-flow-rev {s11:.2f}s linear infinite; }}
                .flow-12 {{ stroke-dasharray: 6 5; animation: pulse-flow-rev {s12:.2f}s linear infinite; }}
                .flow-21 {{ stroke-dasharray: 6 5; animation: pulse-flow-rev {s21:.2f}s linear infinite; }}
                .flow-22 {{ stroke-dasharray: 6 5; animation: pulse-flow-rev {s22:.2f}s linear infinite; }}
                .flow-31 {{ stroke-dasharray: 6 5; animation: pulse-flow-rev {s31:.2f}s linear infinite; }}
                .flow-32 {{ stroke-dasharray: 6 5; animation: pulse-flow-rev {s32:.2f}s linear infinite; }}
                
                .flow-o11 {{ stroke-dasharray: 6 5; animation: pulse-flow-rev {s_o11:.2f}s linear infinite; }}
                .flow-o12 {{ stroke-dasharray: 6 5; animation: pulse-flow-rev {s_o12:.2f}s linear infinite; }}
                .flow-o13 {{ stroke-dasharray: 6 5; animation: pulse-flow-rev {s_o13:.2f}s linear infinite; }}
                .flow-o21 {{ stroke-dasharray: 6 5; animation: pulse-flow-rev {s_o21:.2f}s linear infinite; }}
                .flow-o22 {{ stroke-dasharray: 6 5; animation: pulse-flow-rev {s_o22:.2f}s linear infinite; }}
                .flow-o23 {{ stroke-dasharray: 6 5; animation: pulse-flow-rev {s_o23:.2f}s linear infinite; }}
            </style>
        </defs>

        <g stroke="rgba(255,255,255,0.02)" stroke-width="1">
            <line x1="0" y1="80" x2="850" y2="80" />
            <line x1="0" y1="200" x2="850" y2="200" />
            <line x1="0" y1="320" x2="850" y2="320" />
            <line x1="120" y1="0" x2="120" y2="400" />
            <line x1="425" y1="0" x2="425" y2="400" />
            <line x1="730" y1="0" x2="730" y2="400" />
        </g>

        <path d="M 120,130 L 425,70" fill="none" stroke="{c11}" stroke-width="{t11}" opacity="0.75"/>
        {'<path d="M 120,130 L 425,70" fill="none" stroke="#67e8f9" stroke-width="2.5" class="flow-11" />' if f11 else ""}
        
        <path d="M 120,130 L 425,200" fill="none" stroke="{c21}" stroke-width="{t21}" opacity="0.75"/>
        {'<path d="M 120,130 L 425,200" fill="none" stroke="#67e8f9" stroke-width="2.5" class="flow-21" />' if f21 else ""}
        
        <path d="M 120,130 L 425,330" fill="none" stroke="{c31}" stroke-width="{t31}" opacity="0.75"/>
        {'<path d="M 120,130 L 425,330" fill="none" stroke="#67e8f9" stroke-width="2.5" class="flow-31" />' if f31 else ""}

        <path d="M 120,270 L 425,70" fill="none" stroke="{c12}" stroke-width="{t12}" opacity="0.75"/>
        {'<path d="M 120,270 L 425,70" fill="none" stroke="#67e8f9" stroke-width="2.5" class="flow-12" />' if f12 else ""}
        
        <path d="M 120,270 L 425,200" fill="none" stroke="{c22}" stroke-width="{t22}" opacity="0.75"/>
        {'<path d="M 120,270 L 425,200" fill="none" stroke="#67e8f9" stroke-width="2.5" class="flow-22" />' if f22 else ""}
        
        <path d="M 120,270 L 425,330" fill="none" stroke="{c32}" stroke-width="{t32}" opacity="0.75"/>
        {'<path d="M 120,270 L 425,330" fill="none" stroke="#67e8f9" stroke-width="2.5" class="flow-32" />' if f32 else ""}

        <path d="M 425,70 L 730,130" fill="none" stroke="{c_o11}" stroke-width="{t_o11}" opacity="0.75"/>
        {'<path d="M 425,70 L 730,130" fill="none" stroke="#fed7aa" stroke-width="2.5" class="flow-o11" />' if f_o11 else ""}
        <path d="M 425,70 L 730,270" fill="none" stroke="{c_o21}" stroke-width="{t_o21}" opacity="0.75"/>
        {'<path d="M 425,70 L 730,270" fill="none" stroke="#fed7aa" stroke-width="2.5" class="flow-o21" />' if f_o21 else ""}

        <path d="M 425,200 L 730,130" fill="none" stroke="{c_o12}" stroke-width="{t_o12}" opacity="0.75"/>
        {'<path d="M 425,200 L 730,130" fill="none" stroke="#fed7aa" stroke-width="2.5" class="flow-o12" />' if f_o12 else ""}
        <path d="M 425,200 L 730,270" fill="none" stroke="{c_o22}" stroke-width="{t_o22}" opacity="0.75"/>
        {'<path d="M 425,200 L 730,270" fill="none" stroke="#fed7aa" stroke-width="2.5" class="flow-o22" />' if f_o22 else ""}

        <path d="M 425,330 L 730,130" fill="none" stroke="{c_o13}" stroke-width="{t_o13}" opacity="0.75"/>
        {'<path d="M 425,330 L 730,130" fill="none" stroke="#fed7aa" stroke-width="2.5" class="flow-o13" />' if f_o13 else ""}
        <path d="M 425,330 L 730,270" fill="none" stroke="{c_o23}" stroke-width="{t_o23}" opacity="0.75"/>
        {'<path d="M 425,330 L 730,270" fill="none" stroke="#fed7aa" stroke-width="2.5" class="flow-o23" />' if f_o23 else ""}

        <circle cx="120" cy="130" r="28" fill="#111827" stroke="#22d3ee" stroke-width="3" filter="url(#glow-cyan)"/>
        <text x="120" y="125" fill="#f8fafc" font-size="9" font-weight="bold" text-anchor="middle">TEMP (x₁)</text>
        <text x="120" y="141" fill="#22d3ee" font-size="12" font-weight="900" text-anchor="middle">{X[0]:+.1f}</text>

        <circle cx="120" cy="270" r="28" fill="#111827" stroke="#22d3ee" stroke-width="3" filter="url(#glow-cyan)"/>
        <text x="120" y="265" fill="#f8fafc" font-size="9" font-weight="bold" text-anchor="middle">GRAV (x₂)</text>
        <text x="120" y="281" fill="#22d3ee" font-size="12" font-weight="900" text-anchor="middle">{X[1]:+.1f}</text>

        <circle cx="425" cy="70" r="26" fill="#111827" stroke="#a78bfa" stroke-width="3" filter="{get_glow_filter(A1[0])}"/>
        <text x="425" y="65" fill="#f1f5f9" font-size="9" font-weight="bold" text-anchor="middle">h₁</text>
        <text x="425" y="78" fill="#a78bfa" font-size="11" font-weight="900" text-anchor="middle">{A1[0]:.2f}</text>
        <text x="425" y="110" fill="#c084fc" font-size="9.5" font-weight="bold" text-anchor="middle">b¹₁={b1_arr[0]:+.1f}</text>

        <circle cx="425" cy="200" r="26" fill="#111827" stroke="#a78bfa" stroke-width="3" filter="{get_glow_filter(A1[1])}"/>
        <text x="425" y="195" fill="#f1f5f9" font-size="9" font-weight="bold" text-anchor="middle">h₂</text>
        <text x="425" y="208" fill="#a78bfa" font-size="11" font-weight="900" text-anchor="middle">{A1[1]:.2f}</text>
        <text x="425" y="240" fill="#c084fc" font-size="9.5" font-weight="bold" text-anchor="middle">b¹₂={b1_arr[1]:+.1f}</text>

        <circle cx="425" cy="330" r="26" fill="#111827" stroke="#a78bfa" stroke-width="3" filter="{get_glow_filter(A1[2])}"/>
        <text x="425" y="325" fill="#f1f5f9" font-size="9" font-weight="bold" text-anchor="middle">h₃</text>
        <text x="425" y="338" fill="#a78bfa" font-size="11" font-weight="900" text-anchor="middle">{A1[2]:.2f}</text>
        <text x="425" y="370" fill="#c084fc" font-size="9.5" font-weight="bold" text-anchor="middle">b¹₃={b1_arr[2]:+.1f}</text>

        <circle cx="730" cy="130" r="32" fill="#111827" stroke="{ '#eab308' if habitable_pct >= 50.0 else '#475569' }" stroke-width="3.5" filter="{ 'url(#glow-gold)' if habitable_pct >= 50.0 else 'none' }"/>
        <text x="730" y="122" fill="#f8fafc" font-size="9" font-weight="bold" text-anchor="middle">HABITABLE</text>
        <text x="730" y="139" fill="{ '#facc15' if habitable_pct >= 50.0 else '#94a3b8' }" font-size="13" font-weight="900" text-anchor="middle">{habitable_pct:.1f}%</text>
        <text x="730" y="176" fill="#cbd5e1" font-size="9" font-weight="bold" text-anchor="middle">b²₁={b2_arr[0]:+.1f}</text>

        <circle cx="730" cy="270" r="32" fill="#111827" stroke="{ '#f87171' if barren_pct > 50.0 else '#475569' }" stroke-width="3.5" filter="{ 'url(#glow-red)' if barren_pct > 50.0 else 'none' }"/>
        <text x="730" y="262" fill="#f8fafc" font-size="9" font-weight="bold" text-anchor="middle">BARREN</text>
        <text x="730" y="279" fill="{ '#fca5a5' if barren_pct > 50.0 else '#94a3b8' }" font-size="13" font-weight="900" text-anchor="middle">{barren_pct:.1f}%</text>
        <text x="730" y="316" fill="#cbd5e1" font-size="9" font-weight="bold" text-anchor="middle">b²₂={b2_arr[1]:+.1f}</text>
    </svg>
    """
    
    render_html(svg_content)

# ==========================================
# TAB 3: THE SPACE-WARPING GRID
# ==========================================
with tab_warp:
    render_html("""
    <div style="margin-top: 15px; margin-bottom: 25px;">
        <h3>🌀 Visualizing Space Warping: How Networks Untangle Data</h3>
        <p style="color: #cbd5e1; font-size: 1.05rem; line-height: 1.6;">
            A single straight line can only cut the input square into two half-planes. A bounded "Goldilocks" pocket
            (moderate temperature <b>and</b> moderate gravity, barren on every side) cannot be produced that way.
            Load the <b>🌌 Goldilocks Zone Brain</b> preset to see a 2-layer network carve out exactly such a closed pocket.
            <br>
            How? <b>W¹ maps the flat 2D grid onto a flat plane sitting inside 3D hidden space</b> (a 3×2 matrix cannot fill all of 3D),
            and the <b>activation function bends and creases</b> that plane. The output layer then needs only one flat cut in the bent 3D space.
            The colors below are this network's actual predictions on a finite grid; for custom weights nothing guarantees a useful separation.
        </p>
    </div>
    """)

    # Calculate grid of points (21×21, step 0.2, so the ±1 boundaries fall on grid points)
    grid_size = 21
    u = np.linspace(-2.0, 2.0, grid_size)
    v = np.linspace(-2.0, 2.0, grid_size)
    U, V = np.meshgrid(u, v)

    # Inputs as columns: shape (2, N)
    inputs_flat = np.vstack([U.ravel(), V.ravel()])

    # Batched forward pass: W¹ (3×2) @ (2×N) + b¹ broadcast over columns
    Z1_grid = W1_arr @ inputs_flat + b1_arr[:, np.newaxis]
    A1_grid = ACTIVATIONS[act_func](Z1_grid)
    Z2_grid = W2_arr @ A1_grid + b2_arr[:, np.newaxis]
    Y_grid = softmax(Z2_grid, axis=0)

    habitable_scores = Y_grid[0, :]
    is_habitable = habitable_scores >= 0.5
    class_styles = [
        (is_habitable, "Predicted habitable", "#facc15"),
        (~is_habitable, "Predicted barren", "#fca5a5"),
    ]
    st.caption(
        f"{int(is_habitable.sum())} of {is_habitable.size} grid points ({is_habitable.mean() * 100:.0f}%) "
        "are predicted habitable by the current weights."
    )

    col_2d, col_3d = st.columns(2, gap="large")

    with col_2d:
        fig_2d = go.Figure()
        for mask, label, color in class_styles:
            fig_2d.add_trace(go.Scatter(
                x=inputs_flat[0, mask], y=inputs_flat[1, mask], mode="markers",
                marker=dict(color=color, size=8, line=dict(color="#0f172a", width=1.5)),
                name=label, customdata=habitable_scores[mask],
                hovertemplate="Temp (x₁): %{x:.2f}<br>Grav (x₂): %{y:.2f}<br>P(habitable): %{customdata:.3f}<extra></extra>"
            ))
        fig_2d.add_trace(go.Scatter(
            x=[x1_slider], y=[x2_slider], mode="markers",
            marker=dict(color="#22d3ee", size=18, symbol="star", line=dict(color="#ffffff", width=2)),
            name="Scanned Planet"
        ))
        fig_2d.update_layout(
            title=dict(text="📥 <b>2D Input Coordinates (Planet Space)</b>", font=dict(color="#f8fafc", size=15)),
            xaxis_title="Temperature (x₁)", yaxis_title="Gravity (x₂)",
            template="plotly_dark", plot_bgcolor="#0d1321", paper_bgcolor="#070a13",
            xaxis=dict(range=[-2.2, 2.2]), yaxis=dict(range=[-2.2, 2.2]),
            margin=dict(l=30, r=20, t=50, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_2d, width="stretch")

    with col_3d:
        fig_3d = go.Figure()
        for mask, label, color in class_styles:
            fig_3d.add_trace(go.Scatter3d(
                x=A1_grid[0, mask], y=A1_grid[1, mask], z=A1_grid[2, mask], mode="markers",
                marker=dict(color=color, size=5, line=dict(color="#0f172a", width=1)),
                name=label, customdata=habitable_scores[mask],
                hovertemplate="h₁: %{x:.2f}<br>h₂: %{y:.2f}<br>h₃: %{z:.2f}<br>P(habitable): %{customdata:.3f}<extra></extra>"
            ))
        fig_3d.add_trace(go.Scatter3d(
            x=[A1[0]], y=[A1[1]], z=[A1[2]], mode="markers",
            marker=dict(color="#22d3ee", size=12, symbol="diamond", line=dict(color="#ffffff", width=2)),
            name="Scanned planet (hidden layer)"
        ))
        activations = np.concatenate([A1_grid.ravel(), A1])
        activation_min = float(np.min(activations))
        activation_max = float(np.max(activations))
        activation_pad = max(0.1, (activation_max - activation_min) * 0.08)
        ax_range = [activation_min - activation_pad, activation_max + activation_pad]
        fig_3d.update_layout(
            title=dict(text="📤 <b>Warped 3D Hidden Space (A¹ = g(W¹X+b¹))</b>", font=dict(color="#f8fafc", size=15)),
            template="plotly_dark", paper_bgcolor="#070a13",
            scene=dict(
                xaxis=dict(title="Neuron h₁", range=ax_range),
                yaxis=dict(title="Neuron h₂", range=ax_range),
                zaxis=dict(title="Neuron h₃", range=ax_range),
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
            ),
            margin=dict(l=0, r=0, t=50, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_3d, width="stretch")

# Collapsed network without activation: W²(W¹X + b¹) + b² = (W²W¹)X + (W²b¹ + b²)
W_new = W2_arr @ W1_arr
b_new = W2_arr @ b1_arr + b2_arr

st.markdown("---")
render_html(f"""
<div class="custom-card">
    <h3 style="color: #38bdf8; margin-top: 0;">💡 Lesson Recap: Non-Linearity</h3>
    <p>
        If we removed the activation function, the network would collapse into a single affine map (Page 66 explores this collapse interactively):
        <span class="gold-highlight">Z² = W²(W¹X + b¹) + b² = (W²W¹)X + (W²b¹ + b²) = W_new · X + b_new</span>.
        <br>
        With the current sliders: W_new = [[{W_new[0][0]:+.2f}, {W_new[0][1]:+.2f}], [{W_new[1][0]:+.2f}, {W_new[1][1]:+.2f}]]
        and b_new = [{b_new[0]:+.2f}, {b_new[1]:+.2f}]. One 2×2 matrix and one bias: a single straight decision line.
        <br><br>
        Without activation, space is stretched but remains perfectly flat. The 3D sheet would be rigid, and no closed pocket could be carved out.
        <b>Non-linear activations allow space to bend, providing the flexibility modern networks need to solve complex problems!</b>
    </p>
</div>
""")
safe_page_link("pages/66Stacking Linear Layers Collapses.py", "Previous: 66 · Stacking Linear Layers Collapses", icon="⬅️")
