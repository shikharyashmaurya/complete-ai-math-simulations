import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math

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
def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -15.0, 15.0)))

def relu(z):
    return np.maximum(0.0, z)

def softmax(z):
    shift_z = z - np.max(z)
    exps = np.exp(shift_z)
    return exps / np.sum(exps)

# Animal / Planet Brain presets dictionary
PRESETS = {
    "🌌 Goldilocks Zone Brain": {
        "desc": "Perfectly tuned to classify planets as habitable ONLY if they have moderate temperatures and moderate gravity.",
        "w1": [[2.5, 0.0], [0.0, 2.5], [-2.0, -2.0]],
        "b1": [-1.0, -1.0, 1.5],
        "w2": [[3.0, 3.0, 4.0], [-3.0, -3.0, -3.0]],
        "b2": [-3.5, 3.5],
        "act": "tanh"
    },
    "🪐 Gravity Cautious Brain": {
        "desc": "Extremely strict filter. Any planet with high gravity is immediately flagged as barren, regardless of temperature.",
        "w1": [[0.5, -4.5], [1.5, -2.5], [-0.5, 0.5]],
        "b1": [0.5, -0.5, 0.0],
        "w2": [[2.0, 1.0, -2.0], [-2.0, -2.0, 2.0]],
        "b2": [1.0, -1.0],
        "act": "ReLU"
    },
    "❄️ Frozen Oceans Brain": {
        "desc": "Tuned to identify frozen worlds that could host underground liquid oceans (low temperature, moderate gravity).",
        "w1": [[-4.0, 0.5], [0.5, 3.0], [1.0, -1.5]],
        "b1": [1.0, -0.5, -0.5],
        "w2": [[4.0, -2.0, 3.0], [-4.0, 2.0, -3.0]],
        "b2": [-1.5, 1.5],
        "act": "Sigmoid"
    },
    "🎲 Random Brain": {
        "desc": "A chaotic mesh of random weights to explore how networks behave before training happens.",
        "w1": [[-1.2, 1.8], [2.1, -0.7], [-1.5, -1.9]],
        "b1": [0.5, -0.8, 1.2],
        "w2": [[-1.4, 2.3, -0.9], [1.2, -1.8, 1.5]],
        "b2": [-0.5, 0.5],
        "act": "tanh"
    }
}

# Initializing Session State
if "x1" not in st.session_state:
    st.session_state.x1 = 0.5
if "x2" not in st.session_state:
    st.session_state.x2 = -0.3
if "act_func" not in st.session_state:
    st.session_state.act_func = "tanh"

# Set preset weights into state
if "w1" not in st.session_state:
    p = PRESETS["🌌 Goldilocks Zone Brain"]
    st.session_state.w1 = p["w1"]
    st.session_state.b1 = p["b1"]
    st.session_state.w2 = p["w2"]
    st.session_state.b2 = p["b2"]
    st.session_state.act_func = p["act"]

# Callbacks to update sliders from presets
def load_preset(preset_name):
    p = PRESETS[preset_name]
    st.session_state.w1 = p["w1"]
    st.session_state.b1 = p["b1"]
    st.session_state.w2 = p["w2"]
    st.session_state.b2 = p["b2"]
    st.session_state.act_func = p["act"]

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
    value=st.session_state.x1,
    step=0.1,
    key="x1",
    help="-2.0 represents freezing cold; +2.0 represents scorching hot."
)

x2_slider = st.sidebar.slider(
    "Gravity Index (x₂)",
    min_value=-2.0,
    max_value=2.0,
    value=st.session_state.x2,
    step=0.1,
    key="x2",
    help="-2.0 represents microgravity; +2.0 represents crushing gravity."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ Layer 1 Matrix Controller")
st.sidebar.caption("Configure the 3×2 Weight Matrix W¹ and 3×1 Bias vector b¹ for the Hidden Layer.")

w1 = st.session_state.w1
b1 = st.session_state.b1

# W1 controls
st.sidebar.markdown("##### Weight Matrix W¹ (Dimension 3 × 2)")
col1, col2 = st.sidebar.columns(2)
with col1:
    w1_11 = st.slider("w¹₁₁ (temp → h₁)", -5.0, 5.0, float(w1[0][0]), 0.5)
    w1_21 = st.slider("w¹₂₁ (temp → h₂)", -5.0, 5.0, float(w1[1][0]), 0.5)
    w1_31 = st.slider("w¹₃₁ (temp → h₃)", -5.0, 5.0, float(w1[2][0]), 0.5)
with col2:
    w1_12 = st.slider("w¹₁₂ (grav → h₁)", -5.0, 5.0, float(w1[0][1]), 0.5)
    w1_22 = st.slider("w¹₂₂ (grav → h₂)", -5.0, 5.0, float(w1[1][1]), 0.5)
    w1_32 = st.slider("w¹₃₂ (grav → h₃)", -5.0, 5.0, float(w1[2][1]), 0.5)

# b1 controls
st.sidebar.markdown("##### Bias Vector b¹ (Dimension 3 × 1)")
col_b1_1, col_b1_2, col_b1_3 = st.sidebar.columns(3)
with col_b1_1:
    b1_1 = st.slider("b¹₁", -3.0, 3.0, float(b1[0]), 0.5)
with col_b1_2:
    b1_2 = st.slider("b¹₂", -3.0, 3.0, float(b1[1]), 0.5)
with col_b1_3:
    b1_3 = st.slider("b¹₃", -3.0, 3.0, float(b1[2]), 0.5)

# Save sliders back to session state to prevent sync lags
st.session_state.w1 = [[w1_11, w1_12], [w1_21, w1_22], [w1_31, w1_32]]
st.session_state.b1 = [b1_1, b1_2, b1_3]

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ Layer 2 Matrix Controller")
st.sidebar.caption("Configure the 2×3 Weight Matrix W² and 2×1 Bias vector b² for the Output Layer.")

w2 = st.session_state.w2
b2 = st.session_state.b2

# W2 controls
st.sidebar.markdown("##### Weight Matrix W² (Dimension 2 × 3)")
col_w2_1, col_w2_2, col_w2_3 = st.sidebar.columns(3)
with col_w2_1:
    w2_11 = st.slider("w²₁₁ (h₁ → habitable)", -5.0, 5.0, float(w2[0][0]), 0.5)
    w2_21 = st.slider("w²₂₁ (h₁ → barren)", -5.0, 5.0, float(w2[1][0]), 0.5)
with col_w2_2:
    w2_12 = st.slider("w²₁₂ (h₂ → habitable)", -5.0, 5.0, float(w2[0][1]), 0.5)
    w2_22 = st.slider("w²₂₂ (h₂ → barren)", -5.0, 5.0, float(w2[1][1]), 0.5)
with col_w2_3:
    w2_13 = st.slider("w²₁₃ (h₃ → habitable)", -5.0, 5.0, float(w2[0][2]), 0.5)
    w2_23 = st.slider("w²₂₃ (h₃ → barren)", -5.0, 5.0, float(w2[1][2]), 0.5)

# b2 controls
st.sidebar.markdown("##### Bias Vector b² (Dimension 2 × 1)")
col_b2_1, col_b2_2 = st.sidebar.columns(2)
with col_b2_1:
    b2_1 = st.slider("b²₁ (hab)", -3.0, 3.0, float(b2[0]), 0.5)
with col_b2_2:
    b2_2 = st.slider("b²₂ (bar)", -3.0, 3.0, float(b2[1]), 0.5)

# Update state
st.session_state.w2 = [[w2_11, w2_12, w2_13], [w2_21, w2_22, w2_23]]
st.session_state.b2 = [b2_1, b2_2]

# Main header
st.title("Page 67: Neural Network as Matrix Layers")
st.subheader("W¹X + b¹ → g(z) → W²A¹ + b² → Softmax | Feedforward Math & Space Warping 🌌")

render_html("""
<div class="custom-card">
    <h3>👋 Stacking Neurons: From Dot Products to Matrix Equations</h3>
    <p style="font-size: 1.1rem; line-height: 1.6; color: #cbd5e1;">
        In past simulations, we built a single neuron. But real AI systems don't calculate one dot product at a time. 
        They process entire groups of neurons simultaneously by packeting their connections into <b>Weight Matrices (W)</b> 
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
st.markdown("##### 🪐 Step 1: Select a Preconfigured Brain Design (presets load customized weight weights)")
preset_cols = st.columns(len(PRESETS))
for idx, (p_name, p_val) in enumerate(PRESETS.items()):
    with preset_cols[idx]:
        if st.button(p_name, use_container_width=True, help=p_val["desc"]):
            load_preset(p_name)
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Select Activation Function
st.session_state.act_func = st.selectbox(
    "🔬 Choose Hidden Layer Activation Function (g)",
    options=["tanh", "Sigmoid", "ReLU"],
    index=["tanh", "Sigmoid", "ReLU"].index(st.session_state.act_func),
    help="Determines the warping profile applied to the hidden neurons."
)

# Core Forward Pass Computations
X = np.array([x1_slider, x2_slider])
W1_arr = np.array(st.session_state.w1)
b1_arr = np.array(st.session_state.b1)
W2_arr = np.array(st.session_state.w2)
b2_arr = np.array(st.session_state.b2)

# Layer 1
Z1 = np.dot(W1_arr, X) + b1_arr
if st.session_state.act_func == "tanh":
    A1 = np.tanh(Z1)
elif st.session_state.act_func == "Sigmoid":
    A1 = sigmoid(Z1)
else: # ReLU
    A1 = relu(Z1)

# Layer 2
Z2 = np.dot(W2_arr, A1) + b2_arr
Y = softmax(Z2)

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
    def html_vector_2d(vec, color="cyan-highlight"):
        return f"""
        <div class="matrix-container">
            <div class="matrix-brackets">
                <div class="matrix-grid" style="grid-template-columns: 1fr;">
                    <div style="color: #22d3ee;">{vec[0]:.2f}</div>
                    <div style="color: #22d3ee;">{vec[1]:.2f}</div>
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
        st.markdown(f"#### 🧬 Step 3: Activation Warping (A¹ = {st.session_state.act_func}(Z¹))")
        render_html(f"""
        <div class="custom-card" style="border-left: 5px solid #22c55e; height: 90%;">
            <p>Applying the activation function <b>{st.session_state.act_func}</b> element-wise to squeeze signals:</p>
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
            <p>1. Multipling Hidden activations by Output matrix, then adding biases:</p>
            <div style="text-align: center; margin: 15px 0; display: flex; justify-content: center; align-items: center; flex-wrap: wrap;">
                <span style="font-family: monospace; font-size: 1.1rem; color: #fbcfe8;">Z² = </span>
                {html_matrix_2x3(W2_arr)}
                <span style="font-family: monospace; font-size: 1.2rem; margin: 0 5px;">·</span>
                {html_vector_3d(A1, "#4ade80")}
                <span style="font-family: monospace; font-size: 1.2rem; margin: 0 5px;">+</span>
                {html_vector_2d(b2_arr)}
                <span style="font-family: monospace; font-size: 1.1rem; margin: 0 10px; color: #f472b6;">=</span>
                {html_vector_2d(Z2)}
            </div>
            <p>2. Squash raw scores through <b>Softmax</b> to yield final class probabilities:</p>
            <div style="text-align: center; margin: 15px 0; display: flex; justify-content: center; align-items: center;">
                <span style="font-family: monospace; font-size: 1.1rem; color: #fde047;">Y = Softmax( </span>
                {html_vector_2d(Z2)}
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
            Connections are color-coded: <span style="color: #06b6d4; font-weight: bold;">Cyan represents positive weights (exciting)</span> 
            and <span style="color: #ef4444; font-weight: bold;">Red represents negative weights (inhibiting)</span>. 
            Pulsing particles show active electrical current—watch them go slow, fast, or freeze entirely when activations drop to zero!
        </p>
    </div>
    """)

    # Dynamic line colors, thicknesses and speeds for SVG rendering
    def get_weight_svg_props(w, act_val):
        color = "#06b6d4" if w > 0 else "#ef4444"
        if abs(w) < 0.1:
            color = "#475569"
        
        thick = max(1.5, min(8.5, abs(w) * 1.5))
        flow_speed = 3.0
        if abs(w) > 0.01 and act_val > 0.01:
            flow_speed = max(0.4, min(4.0, 2.0 / (abs(w) * act_val)))
        
        flowing = act_val > 0.05 and abs(w) > 0.1
        return color, thick, flow_speed, flowing

    c11, t11, s11, f11 = get_weight_svg_props(W1_arr[0][0], max(0, X[0]))
    c12, t12, s12, f12 = get_weight_svg_props(W1_arr[0][1], max(0, X[1]))
    c21, t21, s21, f21 = get_weight_svg_props(W1_arr[1][0], max(0, X[0]))
    c22, t22, s22, f22 = get_weight_svg_props(W1_arr[1][1], max(0, X[1]))
    c31, t31, s31, f31 = get_weight_svg_props(W1_arr[2][0], max(0, X[0]))
    c32, t32, s32, f32 = get_weight_svg_props(W1_arr[2][1], max(0, X[1]))

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
        {f'<path d="M 120,130 L 425,70" fill="none" stroke="#67e8f9" stroke-width="2.5" class="flow-11" />' if f11 else ""}
        
        <path d="M 120,130 L 425,200" fill="none" stroke="{c21}" stroke-width="{t21}" opacity="0.75"/>
        {f'<path d="M 120,130 L 425,200" fill="none" stroke="#67e8f9" stroke-width="2.5" class="flow-21" />' if f21 else ""}
        
        <path d="M 120,130 L 425,330" fill="none" stroke="{c31}" stroke-width="{t31}" opacity="0.75"/>
        {f'<path d="M 120,130 L 425,330" fill="none" stroke="#67e8f9" stroke-width="2.5" class="flow-31" />' if f31 else ""}

        <path d="M 120,270 L 425,70" fill="none" stroke="{c12}" stroke-width="{t12}" opacity="0.75"/>
        {f'<path d="M 120,270 L 425,70" fill="none" stroke="#67e8f9" stroke-width="2.5" class="flow-12" />' if f12 else ""}
        
        <path d="M 120,270 L 425,200" fill="none" stroke="{c22}" stroke-width="{t22}" opacity="0.75"/>
        {f'<path d="M 120,270 L 425,200" fill="none" stroke="#67e8f9" stroke-width="2.5" class="flow-22" />' if f22 else ""}
        
        <path d="M 120,270 L 425,330" fill="none" stroke="{c32}" stroke-width="{t32}" opacity="0.75"/>
        {f'<path d="M 120,270 L 425,330" fill="none" stroke="#67e8f9" stroke-width="2.5" class="flow-32" />' if f32 else ""}

        <path d="M 425,70 L 730,130" fill="none" stroke="{c_o11}" stroke-width="{t_o11}" opacity="0.75"/>
        {f'<path d="M 425,70 L 730,130" fill="none" stroke="#fed7aa" stroke-width="2.5" class="flow-o11" />' if f_o11 else ""}
        <path d="M 425,70 L 730,270" fill="none" stroke="{c_o21}" stroke-width="{t_o21}" opacity="0.75"/>
        {f'<path d="M 425,70 L 730,270" fill="none" stroke="#fed7aa" stroke-width="2.5" class="flow-o21" />' if f_o21 else ""}

        <path d="M 425,200 L 730,130" fill="none" stroke="{c_o12}" stroke-width="{t_o12}" opacity="0.75"/>
        {f'<path d="M 425,200 L 730,130" fill="none" stroke="#fed7aa" stroke-width="2.5" class="flow-o12" />' if f_o12 else ""}
        <path d="M 425,200 L 730,270" fill="none" stroke="{c_o22}" stroke-width="{t_o22}" opacity="0.75"/>
        {f'<path d="M 425,200 L 730,270" fill="none" stroke="#fed7aa" stroke-width="2.5" class="flow-o22" />' if f_o22 else ""}

        <path d="M 425,330 L 730,130" fill="none" stroke="{c_o13}" stroke-width="{t_o13}" opacity="0.75"/>
        {f'<path d="M 425,330 L 730,130" fill="none" stroke="#fed7aa" stroke-width="2.5" class="flow-o13" />' if f_o13 else ""}
        <path d="M 425,330 L 730,270" fill="none" stroke="{c_o23}" stroke-width="{t_o23}" opacity="0.75"/>
        {f'<path d="M 425,330 L 730,270" fill="none" stroke="#fed7aa" stroke-width="2.5" class="flow-o23" />' if f_o23 else ""}

        <circle cx="120" cy="130" r="28" fill="#111827" stroke="#22d3ee" stroke-width="3" filter="url(#glow-cyan)"/>
        <text x="120" y="125" fill="#f8fafc" font-size="9" font-weight="bold" text-anchor="middle">TEMP (x₁)</text>
        <text x="120" y="141" fill="#22d3ee" font-size="12" font-weight="black" text-anchor="middle">{X[0]:+.1f}</text>

        <circle cx="120" cy="270" r="28" fill="#111827" stroke="#22d3ee" stroke-width="3" filter="url(#glow-cyan)"/>
        <text x="120" y="265" fill="#f8fafc" font-size="9" font-weight="bold" text-anchor="middle">GRAV (x₂)</text>
        <text x="120" y="281" fill="#22d3ee" font-size="12" font-weight="black" text-anchor="middle">{X[1]:+.1f}</text>

        <circle cx="425" cy="70" r="26" fill="#111827" stroke="#a78bfa" stroke-width="3" filter="{get_glow_filter(A1[0])}"/>
        <text x="425" y="65" fill="#f1f5f9" font-size="9" font-weight="bold" text-anchor="middle">h₁</text>
        <text x="425" y="78" fill="#a78bfa" font-size="11" font-weight="black" text-anchor="middle">{A1[0]:.2f}</text>
        <text x="425" y="110" fill="#c084fc" font-size="9.5" font-weight="bold" text-anchor="middle">b¹₁={b1_arr[0]:+.1f}</text>

        <circle cx="425" cy="200" r="26" fill="#111827" stroke="#a78bfa" stroke-width="3" filter="{get_glow_filter(A1[1])}"/>
        <text x="425" y="195" fill="#f1f5f9" font-size="9" font-weight="bold" text-anchor="middle">h₂</text>
        <text x="425" y="208" fill="#a78bfa" font-size="11" font-weight="black" text-anchor="middle">{A1[1]:.2f}</text>
        <text x="425" y="240" fill="#c084fc" font-size="9.5" font-weight="bold" text-anchor="middle">b¹₂={b1_arr[1]:+.1f}</text>

        <circle cx="425" cy="330" r="26" fill="#111827" stroke="#a78bfa" stroke-width="3" filter="{get_glow_filter(A1[2])}"/>
        <text x="425" y="325" fill="#f1f5f9" font-size="9" font-weight="bold" text-anchor="middle">h₃</text>
        <text x="425" y="338" fill="#a78bfa" font-size="11" font-weight="black" text-anchor="middle">{A1[2]:.2f}</text>
        <text x="425" y="370" fill="#c084fc" font-size="9.5" font-weight="bold" text-anchor="middle">b¹₃={b1_arr[2]:+.1f}</text>

        <circle cx="730" cy="130" r="32" fill="#111827" stroke="{ '#eab308' if habitable_pct >= 50.0 else '#475569' }" stroke-width="3.5" filter="{ 'url(#glow-gold)' if habitable_pct >= 50.0 else 'none' }"/>
        <text x="730" y="122" fill="#f8fafc" font-size="9" font-weight="bold" text-anchor="middle">HABITABLE</text>
        <text x="730" y="139" fill="{ '#facc15' if habitable_pct >= 50.0 else '#94a3b8' }" font-size="13" font-weight="black" text-anchor="middle">{habitable_pct:.1f}%</text>
        <text x="730" y="176" fill="#cbd5e1" font-size="9" font-weight="bold" text-anchor="middle">b²₁={b2_arr[0]:+.1f}</text>

        <circle cx="730" cy="270" r="32" fill="#111827" stroke="{ '#f87171' if barren_pct > 50.0 else '#475569' }" stroke-width="3.5" filter="{ 'url(#glow-red)' if barren_pct > 50.0 else 'none' }"/>
        <text x="730" y="262" fill="#f8fafc" font-size="9" font-weight="bold" text-anchor="middle">BARREN</text>
        <text x="730" y="279" fill="{ '#fca5a5' if barren_pct > 50.0 else '#94a3b8' }" font-size="13" font-weight="black" text-anchor="middle">{barren_pct:.1f}%</text>
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
            Here is one way deep learning can help. A circular region is generally not separable by one straight line in the original 2D input space.
            <br>
            But watch what happens! Our <b>Weight Matrix W¹ projects the flat grid into a 3D coordinate space</b>, and the <b>activation function bends and creases</b> this projected sheet. 
            A learned hidden representation can make classes easier to separate, but the currently selected weights do not guarantee that outcome. The colors below show this network's actual predictions on a finite grid.
        </p>
    </div>
    """)

    # Calculate grid of points
    grid_size = 15
    u = np.linspace(-2.0, 2.0, grid_size)
    v = np.linspace(-2.0, 2.0, grid_size)
    U, V = np.meshgrid(u, v)
    
    # Flatten inputs
    inputs_flat = np.vstack([U.ravel(), V.ravel()]) 
    
    # Compute grid forward pass
    Z1_grid = np.dot(W1_arr, inputs_flat) + b1_arr[:, np.newaxis]
    
    if st.session_state.act_func == "tanh":
        A1_grid = np.tanh(Z1_grid)
    elif st.session_state.act_func == "Sigmoid":
        A1_grid = sigmoid(Z1_grid)
    else: # ReLU
        A1_grid = relu(Z1_grid)
        
    Z2_grid = np.dot(W2_arr, A1_grid) + b2_arr[:, np.newaxis]
    
    exps_grid = np.exp(Z2_grid - np.max(Z2_grid, axis=0))
    Y_grid = exps_grid / np.sum(exps_grid, axis=0)
    
    habitable_scores = Y_grid[0, :]
    predictions = (habitable_scores >= 0.5).astype(int)
    colors = np.where(predictions == 1, "#facc15", "#fca5a5")

    col_2d, col_3d = st.columns(2, gap="large")
    
    with col_2d:
        fig_2d = go.Figure()
        fig_2d.add_trace(go.Scatter(
            x=inputs_flat[0, :], y=inputs_flat[1, :], mode="markers",
            marker=dict(color=colors, size=8, line=dict(color="#0f172a", width=1.5)),
            name="Data Points", hovertemplate="Temp (x₁): %{x:.2f}<br>Grav (x₂): %{y:.2f}"
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
            margin=dict(l=30, r=20, t=50, b=40)
        )
        st.plotly_chart(fig_2d, use_container_width=True)

    with col_3d:
        fig_3d = go.Figure()
        fig_3d.add_trace(go.Scatter3d(
            x=A1_grid[0, :], y=A1_grid[1, :], z=A1_grid[2, :], mode="markers",
            marker=dict(color=colors, size=5, line=dict(color="#0f172a", width=1)),
            name="Hidden Activations"
        ))
        fig_3d.add_trace(go.Scatter3d(
            x=[A1[0]], y=[A1[1]], z=[A1[2]], mode="markers",
            marker=dict(color="#22d3ee", size=12, symbol="diamond", line=dict(color="#ffffff", width=2)),
            name="Scanned Active Layer"
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
            margin=dict(l=0, r=0, t=50, b=0)
        )
        st.plotly_chart(fig_3d, use_container_width=True)

st.markdown("---")
render_html("""
<div class="custom-card">
    <h3 style="color: #38bdf8; margin-top: 0;">💡 Lesson Recap: Non-Linearity</h3>
    <p>
        If we removed the activation function, the network would collapse into a single affine map:
        <span class="gold-highlight">Z² = W_new · X + b_new</span>.
        <br><br>
        Without activation, space is stretched but remains perfectly flat. The 3D sheet would be rigid, and the data would remain entangled. 
        <b>Non-linear activations allow space to bend, providing the flexibility modern networks need to solve complex problems!</b>
    </p>
</div>
""")