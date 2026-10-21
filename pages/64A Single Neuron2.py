import streamlit as st
import numpy as np
import math

# Page setup
st.set_page_config(
    page_title="64: A Single Neuron - The Biological Dot Product",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Cyberpunk & Glassmorphic CSS Styling
st.markdown(r"""
<style>
    /* Dark Theme Base Adjustments */
    .stApp {
        background: #0b0f19 !important;
        color: #f1f5f9 !important;
    }
   
    /* Target standard Streamlit text elements to ensure high contrast in Light and Dark themes */
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: #cbd5e1 !important;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #f8fafc !important;
    }
   
    /* Premium Tab Styling to ensure high readability */
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
   
    /* Premium Sidebar Styling to match laboratory theme and solve readability issues */
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
   
    /* Math Formula Highlight */
    .math-highlight {
        background: rgba(56, 189, 248, 0.18) !important;
        color: #38bdf8 !important;
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
   
    .pink-highlight {
        background: rgba(239, 68, 68, 0.18) !important;
        color: #fca5a5 !important;
        padding: 2px 8px;
        border-radius: 4px;
        font-family: monospace;
        font-weight: bold;
    }

    .purple-highlight {
        background: rgba(167, 139, 250, 0.18) !important;
        color: #c084fc !important;
        padding: 2px 8px;
        border-radius: 4px;
        font-family: monospace;
        font-weight: bold;
    }
   
    /* Custom Success/Failure Badges */
    .fire-badge {
        background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%);
        color: #0b0f19 !important;
        font-weight: 800;
        font-size: 1.1rem;
        padding: 8px 16px;
        border-radius: 30px;
        text-align: center;
        box-shadow: 0 0 20px rgba(234, 179, 8, 0.4);
        display: inline-block;
        margin-top: 10px;
    }
   
    .quiet-badge {
        background: rgba(71, 85, 105, 0.6) !important;
        color: #f1f5f9 !important;
        font-weight: 700;
        font-size: 1.1rem;
        padding: 8px 16px;
        border-radius: 30px;
        text-align: center;
        display: inline-block;
        margin-top: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
   
    /* Premium Streamlit Button Styling to ensure visibility and contrast */
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
   
    div.stButton > button:active {
        transform: translateY(0px) !important;
    }
</style>
""", unsafe_allow_html=True)

# Animal Presets Dictionary
PRESETS = {
    "🐱 Siamese Cat": {
        "ears": 1.0,
        "whiskers": 1.0,
        "barks": 0.0,
        "desc": "Perfect pointy ears, beautiful long whiskers, and zero barking! A classic textbook cat."
    },
    "🐶 Golden Retriever": {
        "ears": 0.1,
        "whiskers": 0.2,
        "barks": 1.0,
        "desc": "Floppy ears, almost no whiskers, and a loud bark. Should NOT trigger our Cat Detector!"
    },
    "🐰 Fluffy Bunny": {
        "ears": 1.0,
        "whiskers": 0.9,
        "barks": 0.0,
        "desc": "Pointy ears and long whiskers, but it doesn't bark! It might fool a naive neuron. We need a negative bias to filter it out!"
    },
    "🦁 Majestic Lion": {
        "ears": 0.8,
        "whiskers": 1.0,
        "barks": 0.0,
        "desc": "A wild big cat! Pointy ears, amazing whiskers, no dog barking. High inputs should trigger the neuron."
    },
    "🤖 Robo-Dog": {
        "ears": 0.9,
        "whiskers": 0.1,
        "barks": 0.8,
        "desc": "Sleek robot dog with pointy metal ears, but it still barks! A heavy negative weight on barking should shut down the signal."
    }
}

# Initializing Session State for interactive sliders
if "ears" not in st.session_state:
    st.session_state.ears = 0.8
if "whiskers" not in st.session_state:
    st.session_state.whiskers = 0.9
if "barks" not in st.session_state:
    st.session_state.barks = 0.1
if "w_ears" not in st.session_state:
    st.session_state.w_ears = 4.0
if "w_whiskers" not in st.session_state:
    st.session_state.w_whiskers = 5.0
if "w_barks" not in st.session_state:
    st.session_state.w_barks = -8.0
if "bias" not in st.session_state:
    st.session_state.bias = -3.0
if "activation" not in st.session_state:
    st.session_state.activation = "Sigmoid"

# Callbacks to update sliders via preset buttons
def load_preset(preset_name):
    data = PRESETS[preset_name]
    st.session_state.ears = data["ears"]
    st.session_state.whiskers = data["whiskers"]
    st.session_state.barks = data["barks"]

# Sidebar configuration
st.sidebar.markdown("""
<div style="text-align: center; padding-bottom: 10px;">
    <h2 style="color: #38bdf8; margin-bottom: 0;">🧠 Lab Controls</h2>
    <p style="color: #94a3b8; font-size: 0.9rem;">Configure Neuron Weights & Bias</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 🎛️ Synaptic Weights ($w_i$)")
st.sidebar.caption("How much the neuron values each trait. Positive weights excite the cell; negative weights suppress it.")

w_ears = st.sidebar.slider(
    "Weight: Pointy Ears (w₁)",
    min_value=-10.0,
    max_value=10.0,
    value=st.session_state.w_ears,
    step=0.5,
    key="w_ears",
    help="Positive value makes ears look like a Cat feature."
)

w_whiskers = st.sidebar.slider(
    "Weight: Whiskers (w₂)",
    min_value=-10.0,
    max_value=10.0,
    value=st.session_state.w_whiskers,
    step=0.5,
    key="w_whiskers",
    help="Positive value makes whiskers look like a Cat feature."
)

w_barks = st.sidebar.slider(
    "Weight: Barks (w₃)",
    min_value=-10.0,
    max_value=10.0,
    value=st.session_state.w_barks,
    step=0.5,
    key="w_barks",
    help="Negative value actively subtracts signal if the animal barks."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎚️ Activation Threshold (Bias $b$)")
st.sidebar.caption("The resting threshold. A negative bias makes the neuron selective and cautious. A positive bias makes it eager.")

bias = st.sidebar.slider(
    "Neuron Bias (b)",
    min_value=-15.0,
    max_value=15.0,
    value=st.session_state.bias,
    step=0.5,
    key="bias",
    help="Controls how high the input sum must be before the neuron fires."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Output Engine")
activation_name = st.sidebar.selectbox(
    "Activation Function (f)",
    options=["Binary Step", "Sigmoid", "ReLU"],
    index=["Binary Step", "Sigmoid", "ReLU"].index(st.session_state.activation),
    key="activation"
)

# Header Section
st.title("Page 64: A Single Neuron")
st.subheader("Inputs × Weights → Sum → + Bias → Activation | The Dot Product Made Biological 🧬")

st.markdown(
    """
    <div class="custom-card">
        <h3>👋 Welcome to the Neural Biome!</h3>
        <p style="font-size: 1.1rem; line-height: 1.6; color: #cbd5e1;">
            In computer science, we often talk about <b>vectors</b>, <b>dot products</b>, and <b>matrices</b> as abstract math.
            Artificial neurons use a simplified mathematical abstraction inspired by biological signaling; they are not a one-to-one model of a real cell.
            Neural networks combine many such computations, often with additional operations such as attention.
        </p>
        <p style="font-size: 1.05rem; line-height: 1.6; color: #94a3b8; margin-bottom: 0;">
            Below, you will design a <b>Cat-Detector Neuron</b>. You will feed it physical animal characteristics (inputs),
            set how important each characteristic is (weights), set its caution levels (bias), and choose how it reacts (activation).
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Biological vs Mathematical Analogy Tabs
analogy_tab, math_tab = st.tabs(["🧬 Biological vs. Artificial Analogy", "🧮 Step-by-Step Mathematical Formula"])

with analogy_tab:
    st.markdown("""
    <div style="margin-top: 15px;">
        <p style="color: #cbd5e1; font-size: 1.05rem;">
            Artificial neurons are loosely inspired by biological signaling, but this is an analogy rather than a one-to-one match:
        </p>
    </div>
    """, unsafe_allow_html=True)
   
    col_bio, col_art = st.columns(2)
    with col_bio:
        st.markdown("""
        <div class="custom-card" style="border-left: 4px solid #4ade80; height: 100%;">
            <h4 style="color: #4ade80; margin-top: 0;">🧬 Biological Neuron</h4>
            <ul style="line-height: 1.8; color: #cbd5e1;">
                <li><b>Dendrites:</b> Branches that receive incoming chemical signals from other cells.</li>
                <li><b>Synapses:</b> Connection junctions. Some synapses are strong (high neurotransmitters), others are weak.</li>
                <li><b>Soma (Cell Body):</b> Combines all incoming signals. If the electrical charge crosses a threshold, the cell activates.</li>
                <li><b>Action Potential:</b> An electrical spark that fires down the tube. It is either on or off!</li>
                <li><b>Axon:</b> The biological cable that transmits the output signal to the next neuron.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col_art:
        st.markdown("""
        <div class="custom-card" style="border-left: 4px solid #38bdf8; height: 100%;">
            <h4 style="color: #38bdf8; margin-top: 0;">🧮 Artificial Neuron (Perceptron)</h4>
            <ul style="line-height: 1.8; color: #cbd5e1;">
                <li><b>Inputs (<span class="green-highlight">xᵢ</span>):</b> Floating-point numbers representing features (e.g., ears=1.0, barking=0.0).</li>
                <li><b>Weights (<span class="purple-highlight">wᵢ</span>):</b> Multipliers representing synapse strength. Larger weight = more important feature.</li>
                <li><b>Summation & Bias (<span class="math-highlight">Σ xᵢwᵢ + b</span>):</b> The dot product of inputs and weights, shifted by a threshold (bias).</li>
                <li><b>Activation Function (<span class="math-highlight">f(z)</span>):</b> A function that transforms the pre-activation value (for example, sigmoid squashes it between 0 and 1).</li>
                <li><b>Output (<span class="math-highlight">a</span>):</b> The transformed score. A sigmoid output is probability-like, but a binary step is only 0/1 and a ReLU output is unbounded—not a confidence probability.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

with math_tab:
    st.markdown(r"""
    <div class="custom-card" style="margin-top: 15px;">
        <h4 style="color: #38bdf8; margin-top:0;">The Master Formula of AI</h4>
        <p style="font-size: 1.1rem; line-height: 1.6;">
            A neuron's entire process can be written in a single beautiful equation:
        </p>
        <div style="text-align: center; margin: 20px 0; padding: 15px; background: rgba(0,0,0,0.2); border-radius: 8px;">
            <span style="font-size: 1.8rem; font-family: 'Courier New', Courier, monospace; font-weight: bold; color: #e2e8f0;">
                a = <span style="color:#38bdf8;">f</span>( <span style="color:#4ade80;">x₁</span>·<span style="color:#c084fc;">w₁</span> + <span style="color:#4ade80;">x₂</span>·<span style="color:#c084fc;">w₂</span> + <span style="color:#4ade80;">x₃</span>·<span style="color:#c084fc;">w₃</span> + <span style="color:#fca5a5;">b</span> )
            </span>
        </div>
        <p style="font-size: 1.05rem; line-height: 1.6; color: #94a3b8;">
            In linear algebra terms, the sum of inputs multiplied by their weights is a <b>Dot Product</b> of two vectors!
            If we define $\mathbf{x} = [x_1, x_2, x_3]$ and $\mathbf{w} = [w_1, w_2, w_3]$, the equation simplifies elegantly to:
        </p>
        <div style="text-align: center; margin: 15px 0;">
            <span style="font-size: 1.5rem; font-family: 'Times New Roman'; color: #38bdf8;">
                a = f( <b>x</b> · <b>w</b> + b )
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Main Interactive Lab Area
st.header("🔬 The Cat-Detector Laboratory")

# Preset buttons
st.markdown("##### 🎮 Step 1: Select a Pre-configured Animal Preset (or customize below)")
preset_cols = st.columns(len(PRESETS))
for idx, (p_name, p_val) in enumerate(PRESETS.items()):
    with preset_cols[idx]:
        if st.button(p_name, use_container_width=True, help=p_val["desc"]):
            load_preset(p_name)
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
# Layout: Features (Left column) and Visualization (Right column)
left_col, right_col = st.columns([1, 1.8], gap="large")

with left_col:
    st.markdown("""
    <div style="background: rgba(56, 189, 248, 0.05); border: 1px solid rgba(56, 189, 248, 0.15); border-radius: 12px; padding: 16px; margin-bottom: 20px;">
        <h4 style="color: #38bdf8; margin: 0 0 8px 0; font-size: 1.1rem;">🧬 Current Animal Profile</h4>
        <p style="margin: 0; color: #cbd5e1; font-size: 0.95rem;">
            Adjust the sliders below to change the features of the subject being evaluated by the neuron.
        </p>
    </div>
    """, unsafe_allow_html=True)
   
    # Render Sliders tied directly to session_state
    ears = st.slider(
        "📐 Ear Pointiness (x₁)",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.ears,
        step=0.05,
        key="ears",
        help="0.0 = completely rounded, 1.0 = extremely pointy ears."
    )
   
    whiskers = st.slider(
        "🐱 Whisker Magnificence (x₂)",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.whiskers,
        step=0.05,
        key="whiskers",
        help="0.0 = completely hairless face, 1.0 = long magnificent whiskers."
    )
   
    barks = st.slider(
        "🔊 Barking Volume (x₃)",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.barks,
        step=0.05,
        key="barks",
        help="0.0 = quiet/meows, 1.0 = loud dog bark."
    )
   
    # Show active preset description if matching
    matched_preset = None
    for name, p in PRESETS.items():
        if abs(ears - p["ears"]) < 0.01 and abs(whiskers - p["whiskers"]) < 0.01 and abs(barks - p["barks"]) < 0.01:
            matched_preset = name
            break
           
    if matched_preset:
        st.markdown(f"""
        <div style="background: rgba(34, 197, 94, 0.1); border: 1px dashed rgba(34, 197, 94, 0.3); border-radius: 8px; padding: 12px; margin-top: 15px;">
            <strong style="color: #4ade80;">📍 Preset active: {matched_preset}</strong><br>
            <span style="font-size: 0.9rem; color: #cbd5e1;">{PRESETS[matched_preset]['desc']}</span>
        </div>
        """, unsafe_allow_html=True)

# Computations
# 1. Weighted Sum (z)
dot_product = (ears * w_ears) + (whiskers * w_whiskers) + (barks * w_barks)
z = dot_product + bias

# 2. Activation Function (a)
if activation_name == "Binary Step":
    activation_formula = "a = 1.0 if z ≥ 0 else 0.0"
    a = 1.0 if z >= 0 else 0.0
elif activation_name == "Sigmoid":
    activation_formula = "a = 1 / (1 + e⁻ᶻ)"
    a = 1.0 / (1.0 + math.exp(-np.clip(z, -20.0, 20.0)))
else: # ReLU
    activation_formula = "a = max(0, z)"
    a = max(0.0, z)

# Pre-format outputs to avoid f-string nested format parsing issues in templates
if activation_name == "Binary Step":
    a_formatted_6f = str(int(a))
    a_formatted_2f = str(int(a))
else:
    a_formatted_6f = f"{a:.6f}"
    a_formatted_2f = f"{a:.2f}"

# Firing Status
fires = False
if activation_name == "Sigmoid":
    fires = a >= 0.5
else:
    fires = a > 0.0

with right_col:
    # Build dynamic live SVG diagram
    # SVG Dimensions: 800 x 480
   
    # 1. Calculate color states
    # Input node opacity / colors
    ears_glow = int(100 + 155 * ears)
    whiskers_glow = int(100 + 155 * whiskers)
    barks_glow = int(100 + 155 * barks)
   
    ears_color = f"rgb(74, 222, 128)" if ears > 0.1 else "rgb(71, 85, 105)"
    whiskers_color = f"rgb(74, 222, 128)" if whiskers > 0.1 else "rgb(71, 85, 105)"
    barks_color = f"rgb(248, 113, 113)" if barks > 0.1 else "rgb(71, 85, 105)"
   
    # Weight paths: cyan for positive, red for negative
    def get_weight_color(w):
        if w > 0:
            return "rgb(6, 182, 212)" # Cyan
        elif w < 0:
            return "rgb(239, 68, 68)" # Coral red
        else:
            return "rgb(100, 116, 139)" # Slate grey
           
    w_ears_color = get_weight_color(w_ears)
    w_whiskers_color = get_weight_color(w_whiskers)
    w_barks_color = get_weight_color(w_barks)
   
    # Weight thickness
    w_ears_thick = max(1.5, min(10.0, abs(w_ears) * 1.0))
    w_whiskers_thick = max(1.5, min(10.0, abs(w_whiskers) * 1.0))
    w_barks_thick = max(1.5, min(10.0, abs(w_barks) * 1.0))
   
    # Soma glowing state
    soma_glow = "rgba(100, 116, 139, 0.2)"
    soma_border = "rgb(71, 85, 105)"
    if fires:
        soma_glow = "rgba(6, 182, 212, 0.25)"
        soma_border = "rgb(6, 182, 212)"
    else:
        soma_glow = "rgba(239, 68, 68, 0.2)"
        soma_border = "rgb(239, 68, 68)"
       
    # Axon / Firing state
    axon_color = "rgb(71, 85, 105)"
    axon_dash = "none"
    output_glow = "none"
    output_glow_color = "rgba(71, 85, 105, 0)"
   
    if fires:
        axon_color = "rgb(234, 179, 8)" # Glowing Gold
        axon_dash = "4"
        output_glow = "0px 0px 30px rgba(234, 179, 8, 0.8)"
        output_glow_color = "rgba(234, 179, 8, 0.5)"
       
    # Dynamic Dash array for biological pulse flow
    dash_ears = f"stroke-dasharray='8 4' stroke-dashoffset='{st.session_state.get('tick', 0)}'" if ears > 0 else ""
   
    svg_content = f"""
    <svg viewBox="0 0 850 480" width="100%" height="100%" style="background:#0e1626; border-radius:16px; border:1px solid rgba(255,255,255,0.05); box-shadow: inset 0 0 40px rgba(0,0,0,0.5);">
        <!-- Definitions for Glowing Effects -->
        <defs>
            <filter id="glow-cyan" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="8" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
            <filter id="glow-gold" x="-30%" y="-30%" width="160%" height="160%">
                <feGaussianBlur stdDeviation="15" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
            <filter id="glow-red" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="8" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
           
            <!-- Dynamic styling for flowing animation -->
            <style>
                @keyframes pulse-flow-fast {{
                    to {{ stroke-dashoffset: -20; }}
                }}
                @keyframes pulse-flow-med {{
                    to {{ stroke-dashoffset: -20; }}
                }}
                .flow-ears {{
                    stroke-dasharray: 8 6;
                    animation: pulse-flow-fast {2.0 / (ears + 0.01):.2f}s linear infinite;
                }}
                .flow-whiskers {{
                    stroke-dasharray: 8 6;
                    animation: pulse-flow-fast {2.0 / (whiskers + 0.01):.2f}s linear infinite;
                }}
                .flow-barks {{
                    stroke-dasharray: 8 6;
                    animation: pulse-flow-fast {2.0 / (barks + 0.01):.2f}s linear infinite;
                }}
                .flow-axon {{
                    stroke-dasharray: 10 8;
                    animation: pulse-flow-fast 1s linear infinite;
                }}
            </style>
        </defs>

        <!-- GRID BACKGROUND -->
        <g stroke="rgba(255,255,255,0.02)" stroke-width="1">
            <line x1="0" y1="80" x2="850" y2="80" />
            <line x1="0" y1="160" x2="850" y2="160" />
            <line x1="0" y1="240" x2="850" y2="240" />
            <line x1="0" y1="320" x2="850" y2="320" />
            <line x1="0" y1="400" x2="850" y2="400" />
            <line x1="100" y1="0" x2="100" y2="480" />
            <line x1="250" y1="0" x2="250" y2="480" />
            <line x1="400" y1="0" x2="400" y2="480" />
            <line x1="550" y1="0" x2="550" y2="480" />
            <line x1="700" y1="0" x2="700" y2="480" />
        </g>

        <!-- SYNAPSE LINKS (INPUTS TO SOMA) -->
        <!-- Link 1 (Pointy Ears) -->
        <path d="M 120,90 Q 250,90 380,240" fill="none" stroke="{w_ears_color}" stroke-width="{w_ears_thick}" opacity="0.8"/>
        {f'<path d="M 120,90 Q 250,90 380,240" fill="none" stroke="#67e8f9" stroke-width="2.5" class="flow-ears" />' if ears > 0.05 and abs(w_ears) > 0.1 else ""}

        <!-- Link 2 (Whiskers) -->
        <path d="M 120,240 L 380,240" fill="none" stroke="{w_whiskers_color}" stroke-width="{w_whiskers_thick}" opacity="0.8"/>
        {f'<path d="M 120,240 L 380,240" fill="none" stroke="#67e8f9" stroke-width="2.5" class="flow-whiskers" />' if whiskers > 0.05 and abs(w_whiskers) > 0.1 else ""}

        <!-- Link 3 (Barks) -->
        <path d="M 120,390 Q 250,390 380,240" fill="none" stroke="{w_barks_color}" stroke-width="{w_barks_thick}" opacity="0.8"/>
        {f'<path d="M 120,390 Q 250,390 380,240" fill="none" stroke="#fca5a5" stroke-width="2.5" class="flow-barks" />' if barks > 0.05 and abs(w_barks) > 0.1 else ""}

        <!-- SOMA TO AXON OUTPUT LINK -->
        <path d="M 460,240 L 730,240" fill="none" stroke="{axon_color}" stroke-width="6" />
        {f'<path d="M 460,240 L 730,240" fill="none" stroke="#fef08a" stroke-width="3" class="flow-axon" filter="url(#glow-gold)"/>' if fires else ""}

        <!-- DENDRITE INPUT NODES -->
        <!-- Ears Node -->
        <circle cx="120" cy="90" r="32" fill="#131e35" stroke="{ears_color}" stroke-width="3" filter="{ 'url(#glow-cyan)' if ears > 0.5 else 'none' }" />
        <text x="120" y="85" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="middle">EARS</text>
        <text x="120" y="102" fill="#4ade80" font-size="14" font-weight="black" text-anchor="middle">x₁={ears:.2f}</text>
       
        <!-- Whiskers Node -->
        <circle cx="120" cy="240" r="32" fill="#131e35" stroke="{whiskers_color}" stroke-width="3" filter="{ 'url(#glow-cyan)' if whiskers > 0.5 else 'none' }" />
        <text x="120" y="235" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="middle">WHISKERS</text>
        <text x="120" y="252" fill="#4ade80" font-size="14" font-weight="black" text-anchor="middle">x₂={whiskers:.2f}</text>

        <!-- Barks Node -->
        <circle cx="120" cy="390" r="32" fill="#131e35" stroke="{barks_color}" stroke-width="3" filter="{ 'url(#glow-red)' if barks > 0.5 else 'none' }" />
        <text x="120" y="385" fill="#f8fafc" font-size="12" font-weight="bold" text-anchor="middle">BARKS</text>
        <text x="120" y="402" fill="#f87171" font-size="14" font-weight="black" text-anchor="middle">x₃={barks:.2f}</text>

        <!-- WEIGHT LABELS ON LINES -->
        <g fill="#111827" font-size="12" font-weight="bold" text-anchor="middle">
            <!-- Ears weight label box -->
            <rect x="235" y="105" width="60" height="20" rx="6" fill="#1e293b" stroke="{w_ears_color}" stroke-width="1.5"/>
            <text x="265" y="119" fill="#e2e8f0">w₁ = {w_ears:+.1f}</text>

            <!-- Whiskers weight label box -->
            <rect x="235" y="230" width="60" height="20" rx="6" fill="#1e293b" stroke="{w_whiskers_color}" stroke-width="1.5"/>
            <text x="265" y="244" fill="#e2e8f0">w₂ = {w_whiskers:+.1f}</text>

            <!-- Barks weight label box -->
            <rect x="235" y="340" width="60" height="20" rx="6" fill="#1e293b" stroke="{w_barks_color}" stroke-width="1.5"/>
            <text x="265" y="354" fill="#e2e8f0">w₃ = {w_barks:+.1f}</text>
        </g>

        <!-- SOMA (CELL BODY - INTEGRATION UNIT) -->
        <circle cx="420" cy="240" r="62" fill="#0f172a" stroke="{soma_border}" stroke-width="4" filter="{ 'url(#glow-cyan)' if z >= 0 else 'url(#glow-red)' }"/>
       
        <!-- Soma text calculations -->
        <text x="420" y="210" fill="#94a3b8" font-size="11" font-weight="bold" text-anchor="middle">SOMA (CELL BODY)</text>
       
        <!-- Pre-activation formula and Dot Product -->
        <text x="420" y="230" fill="#e2e8f0" font-size="13" font-weight="medium" text-anchor="middle">x·w = {dot_product:+.2f}</text>
       
        <!-- Bias indicator -->
        <text x="420" y="248" fill="#fca5a5" font-size="13" font-weight="semibold" text-anchor="middle">b = {bias:+.1f}</text>
       
        <line x1="380" y1="258" x2="460" y2="258" stroke="rgba(255,255,255,0.15)" stroke-width="1"/>
       
        <!-- Total integrated voltage z -->
        <text x="420" y="278" fill="#38bdf8" font-size="17" font-weight="black" text-anchor="middle">z = {z:.2f}</text>

        <!-- BIAS DECORATOR POINTER -->
        <path d="M 420,178 L 420,135" stroke="#fca5a5" stroke-dasharray="3 3" stroke-width="1.5" />
        <rect x="375" y="110" width="90" height="25" rx="8" fill="#1e293b" stroke="#fca5a5" stroke-width="1"/>
        <text x="420" y="126" fill="#fca5a5" font-size="10.5" font-weight="bold" text-anchor="middle">Resting Bias (b)</text>

        <!-- AXON TRANSMISSION CABLE -->
        <text x="590" y="225" fill="{axon_color}" font-size="12" font-weight="bold" text-anchor="middle">AXON (CABLE)</text>

        <!-- ACTIVATED OUTPUT TERMINALS -->
        <circle cx="740" cy="240" r="38" fill="#0f172a" stroke="{axon_color}" stroke-width="4" filter="{ 'url(#glow-gold)' if fires else 'none' }" />
        <text x="740" y="225" fill="#94a3b8" font-size="10" font-weight="bold" text-anchor="middle">OUTPUT (a)</text>
       
        <!-- Activated output value formatted appropriately -->
        <text x="740" y="248" fill="{ '#facc15' if fires else '#94a3b8' }" font-size="19" font-weight="black" text-anchor="middle">
            {a_formatted_2f}
        </text>
       
        <!-- Status bubble underneath output -->
        <rect x="690" y="295" width="100" height="24" rx="12" fill="{ '#fef08a' if fires else '#1e293b' }" opacity="{ '0.9' if fires else '0.4' }" stroke="{ 'rgb(234, 179, 8)' if fires else 'rgba(255,255,255,0.1)' }" stroke-width="1.5"/>
        <text x="740" y="311" fill="{ '#0b0f19' if fires else '#94a3b8' }" font-size="10.5" font-weight="black" text-anchor="middle">
            { "⚡ FIRES!" if fires else "💤 SILENT" }
        </text>
    </svg>
    """
   
    svg_clean = "\n".join([line.strip() for line in svg_content.split("\n")])
    st.markdown(svg_clean, unsafe_allow_html=True)

# Step-by-Step Live Mathematical Calculation Breakdown
st.markdown("---")
st.header("🎚️ Live Output & Math Verification")

col_sum, col_act = st.columns(2)

with col_sum:
    st.markdown(f"""
    <div class="custom-card">
        <div class="card-title">🔍 Step 1: Pre-Activation Weighted Sum (z)</div>
        <p style="margin-bottom: 8px;">The neuron calculates the <b>Dot Product</b> of inputs and weights, then adds the <b>Bias</b>:</p>
        <div style="background: rgba(0,0,0,0.35); color: #f8fafc; padding: 12px; border-radius: 8px; font-family: monospace; font-size: 1rem; line-height: 1.8; border: 1px solid rgba(255,255,255,0.06);">
            z = (<span style="color:#4ade80;">x₁</span>·<span style="color:#c084fc;">w₁</span>) + (<span style="color:#4ade80;">x₂</span>·<span style="color:#c084fc;">w₂</span>) + (<span style="color:#4ade80;">x₃</span>·<span style="color:#c084fc;">w₃</span>) + <span style="color:#fca5a5;">b</span><br>
            z = (<span style="color:#4ade80;">{ears:.2f}</span> · <span style="color:#c084fc;">{w_ears:+.1f}</span>) + (<span style="color:#4ade80;">{whiskers:.2f}</span> · <span style="color:#c084fc;">{w_whiskers:+.1f}</span>) + (<span style="color:#4ade80;">{barks:.2f}</span> · <span style="color:#c084fc;">{w_barks:+.1f}</span>) + (<span style="color:#fca5a5;">{bias:+.1f}</span>)<br>
            z = <span style="color:#4ade80;">{ears*w_ears:+.2f}</span>  {whiskers*w_whiskers:+.2f}  {barks*w_barks:+.2f} <span style="color:#fca5a5;">{bias:+.2f}</span><br>
            <strong>z = <span style="color:#38bdf8; font-size: 1.15rem;">{z:.4f}</span></strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_act:
    # Set description of activation function response
    if activation_name == "Binary Step":
        desc = "<b>Binary Step (Threshold):</b> Fires a strict 1 if the input is positive, otherwise stays completely dead at 0. Historically, this is what the original 1958 Perceptron used!"
    elif activation_name == "Sigmoid":
        desc = "<b>Sigmoid:</b> Squashes the input score into a smooth, biological S-curve between 0 (0%) and 1 (100%). It represents the <i>probability</i> or confidence of the detection."
    else:
        desc = "<b>ReLU (Rectified Linear Unit):</b> The champion of modern deep learning. If positive, it passes the value straight through. If negative, it instantly zeroes out (sparse firing)."
       
    st.markdown(f"""
    <div class="custom-card">
        <div class="card-title">⚡ Step 2: Applying Activation Function (a)</div>
        <p style="margin-bottom: 8px;">The neuron feeds the integrated signal <span class="math-highlight">z = {z:.2f}</span> through the activation engine. Only sigmoid outputs are probability-like; ReLU scores are unbounded:</p>
        <div style="background: rgba(0,0,0,0.35); color: #f8fafc; padding: 12px; border-radius: 8px; font-family: monospace; font-size: 1rem; line-height: 1.8; margin-bottom: 12px; border: 1px solid rgba(255,255,255,0.06);">
            Engine Selected: <strong style="color: #38bdf8;">{activation_name}</strong><br>
            Formula: <span style="color: #c084fc;">{activation_formula}</span><br>
            Calculation: f({z:.4f}) = <br>
            <strong>Output a = <span style="color:#facc15; font-size: 1.25rem;">{a_formatted_6f}</span></strong>
        </div>
        <span style="font-size: 0.9rem; color: #94a3b8;">{desc}</span>
    </div>
    """, unsafe_allow_html=True)

# Interactive Diagnostic Verdict
st.markdown("### 📊 Diagnostic Verdict")
if fires:
    verdict_desc = f"🎉 <b>Positive under this demo's decision rule.</b> The pre-activation crossed the firing threshold; output <b>a = {a_formatted_2f}</b> is not necessarily a probability or calibrated confidence."
    st.markdown(f"""
    <div style="background: rgba(234, 179, 8, 0.1); border: 2px solid #eab308; border-radius: 12px; padding: 20px;">
        <span class="fire-badge">⚡ FIRES: CAT DETECTED</span>
        <p style="margin-top: 12px; color: #fef9c3; font-size: 1.1rem; line-height: 1.6;">{verdict_desc}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    verdict_desc = f"💤 <b>Negative under this demo's decision rule.</b> The pre-activation did not reach the firing threshold (output <b>a = {a_formatted_2f}</b>). This toy rule is not a validated real-world cat classifier."
    st.markdown(f"""
    <div style="background: rgba(71, 85, 105, 0.15); border: 1px solid rgba(255,255,255,0.15); border-radius: 12px; padding: 20px;">
        <span class="quiet-badge">💤 SILENT: NOT A CAT</span>
        <p style="margin-top: 12px; color: #f1f5f9; font-size: 1.1rem; line-height: 1.6;">{verdict_desc}</p>
    </div>
    """, unsafe_allow_html=True)

# Visualizing the Mathematics of the Threshold (Why Bias Matters)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="custom-card">
    <h3 style="color: #38bdf8; margin-top: 0;">💡 Student Exploration: Why do we need a Bias?</h3>
    <p style="font-size: 1.05rem; line-height: 1.6; color: #cbd5e1;">
        Try selecting the <b>🐰 Fluffy Bunny</b> preset. Notice that the Bunny has pointy ears (<span class="green-highlight">1.0</span>)
        and whiskers (<span class="green-highlight">0.9</span>), and does not bark (<span class="green-highlight">0.0</span>).
        If our bias was set to <span class="math-highlight">0.0</span>, the neuron would sum:
        <br><br>
        <span style="font-family: monospace; background: rgba(0,0,0,0.2); padding: 4px 8px; border-radius: 4px;">
            z = (1.0 · 4.0) + (0.9 · 5.0) + (0.0 · -8.0) = 4.0 + 4.5 = +8.5
        </span>
        <br><br>
        A score of <span class="math-highlight">+8.5</span> is extremely positive! The neuron would loudly claim the Bunny is a cat!
        To prevent this error, we adjust the <b>Bias ($b$)</b>. By setting a negative resting bias (e.g. <span class="pink-highlight">-5.0</span> or <span class="pink-highlight">-7.0</span>),
        we require the total traits to be exceptionally strong to overcome the negative "brake".
        This is why bias shifts the pre-activation score (and, for a monotone activation, the input threshold): it can make this demo's decision rule more selective or more permissive.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-top: 40px; padding: 20px; color: #64748b; font-size: 0.9rem; border-top: 1px solid rgba(255,255,255,0.05);">
    Page 64 of the AI Visualized Curriculum | Created with ❤️ to make mathematics biological and simple.
</div>
""", unsafe_allow_html=True)
