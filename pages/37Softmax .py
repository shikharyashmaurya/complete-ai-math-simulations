import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Configure page
st.set_page_config(page_title="Softmax Function", page_icon="🧮", layout="wide")

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .math-font {
        font-family: 'Courier New', Courier, monospace;
        font-size: 1.2rem;
        color: #4A90E2;
    }
    .highlight-box {
        background-color: #f0f2f6;
        color: black;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        border-left: 5px solid #ff4b4b;
    }
    .insight-box {
        background-color: #e8f4f8;
        color: black;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        border-left: 5px solid #3498db;
    }
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted black;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧮 Softmax: Any Numbers → Probabilities")
st.markdown("""
Welcome to the magic of the **Softmax function**! In AI, neural networks often output raw, unconstrained numbers called **logits** (or raw scores).
These numbers can be positive, negative, massive, or tiny.

But to make decisions (e.g., "Is this image a Cat, Dog, or Car?"), we need **probabilities**—numbers between 0 and 1 that sum up to exactly 1.
**Softmax** is the elegant mathematical bridge that does exactly this.
""")

# Interactive Controls
st.sidebar.header("🎛️ Control the Raw Scores")
st.sidebar.markdown("Adjust the raw scores (logits) output by our hypothetical neural network:")

score_cat = st.sidebar.slider("Logit for 'Cat' 🐱", min_value=-10.0, max_value=10.0, value=2.0, step=0.1)
score_dog = st.sidebar.slider("Logit for 'Dog' 🐶", min_value=-10.0, max_value=10.0, value=-1.0, step=0.1)
score_car = st.sidebar.slider("Logit for 'Car' 🚗", min_value=-10.0, max_value=10.0, value=0.5, step=0.1)

st.sidebar.markdown("---")
st.sidebar.header("🌡️ Temperature (Optional)")
temperature = st.sidebar.slider(
    "Temperature (T)",
    min_value=0.1, max_value=5.0, value=1.0, step=0.1,
    help="Temperature controls how 'confident' or 'soft' the probabilities are. T=1 is standard Softmax. High T makes probabilities uniform, Low T makes it like argmax."
)

# Math behind Softmax
st.markdown("### The Formula")
if temperature == 1.0:
    st.latex(r"\text{Softmax}(z_i) = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}")
else:
    st.latex(r"\text{Softmax}(z_i) = \frac{e^{z_i / T}}{\sum_{j=1}^{K} e^{z_j / T}}")

# Calculations
z = np.array([score_cat, score_dog, score_car])
labels = ['Cat 🐱', 'Dog 🐶', 'Car 🚗']
colors = ['#FF9F43', '#10AC84', '#54A0FF']

# Step 1: Divide by Temp
z_t = z / temperature

# Step 2: Exponentiate
exp_z = np.exp(z_t)

# Step 3: Sum
sum_exp_z = np.sum(exp_z)

# Step 4: Normalize (Probabilities)
probs = exp_z / sum_exp_z

# Visualization: 3 Steps
col1, col2, col3 = st.columns(3)

def create_bar_chart(x_labels, y_values, title, y_title, colors, range_y=None):
    fig = go.Figure(data=[
        go.Bar(
            x=x_labels,
            y=y_values,
            marker_color=colors,
            text=[f"{v:.2f}" for v in y_values],
            textposition='auto'
        )
    ])
    fig.update_layout(
        title=title,
        yaxis_title=y_title,
        template="plotly_white",
        height=400,
        margin=dict(l=40, r=40, t=60, b=40),
    )
    if range_y:
        fig.update_yaxes(range=range_y)
    return fig

with col1:
    st.markdown("#### 1️⃣ Raw Scores (Logits)")
    st.markdown("Can be any number. Positives, negatives, anything.")
    fig1 = create_bar_chart(labels, z, "Raw Scores (z)", "Value", colors, range_y=[-10, 10])
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("#### 2️⃣ Exponentiate ($e^z$)")
    st.markdown("Makes everything **positive**. Exaggerates differences.")
    title_exp = "Exponentiated (e^z)" if temperature == 1.0 else f"Exponentiated (e^(z/{temperature}))"
    fig2 = create_bar_chart(labels, exp_z, title_exp, "Value", colors)
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    st.markdown("#### 3️⃣ Normalize")
    st.markdown("Divide by sum. Now they are between 0 & 1 and **sum to 1**.")
    fig3 = create_bar_chart(labels, probs, "Probabilities (Softmax)", "Probability", colors, range_y=[0, 1])
    st.plotly_chart(fig3, use_container_width=True)

# Step-by-step Math Breakdown Table
st.markdown("### 🧮 Step-by-Step Calculation Breakdown")

df_math = pd.DataFrame({
    "Class": labels,
    "Raw Score (z)": z,
    "z / T": z_t,
    "e^(z/T)": exp_z,
    "Probability (%)": probs * 100
})

if temperature == 1.0:
    df_math = df_math.drop(columns=["z / T"])
    df_math = df_math.rename(columns={"e^(z/T)": "e^z"})

# Format for display
df_display = df_math.copy()
for col in df_display.columns:
    if col != "Class" and col != "Probability (%)":
        df_display[col] = df_display[col].map("{:.2f}".format)
df_display["Probability (%)"] = df_display["Probability (%)"].map("{:.2f}%".format)

st.dataframe(df_display, use_container_width=True, hide_index=True)

st.markdown(f"""
<div class="highlight-box">
    <strong>💡 Notice the Normalization:</strong><br>
    Sum of all exponentiated values = <strong>{sum_exp_z:.2f}</strong><br>
    If we divide each exponentiated value by {sum_exp_z:.2f}, we get the final probabilities!
    The total probability is exactly <strong>100%</strong>.
</div>
""", unsafe_allow_html=True)

# Temperature explanation
st.markdown("---")
st.markdown("### 🌡️ What is the 'Temperature' Slider?")
col_t1, col_t2 = st.columns([2, 1])

with col_t1:
    st.markdown("""
    In many modern AI models (like ChatGPT), there's a setting called **Temperature**. It controls the "creativity" or "randomness" of the output by tweaking the Softmax function denominator.
   
    *   **Low Temperature (T < 1):** The model becomes very confident and "spiky". It amplifies the highest score and squashes the rest. It's more predictable but less creative. (Try `T = 0.1` in the sidebar!)
    *   **High Temperature (T > 1):** The model becomes "softer" and more uniform. The probabilities get closer together, meaning it might pick a slightly less likely word, leading to more creative (or sometimes nonsensical) answers! (Try `T = 5.0`!)
   
    *Go ahead, play with the Temperature slider in the sidebar and watch the probabilities chart change!*
    """)
   
with col_t2:
    st.markdown(f"""
    <div class="insight-box">
        <strong>Current T: {temperature}</strong><br>
        {"🔥 High: Soft & Uniform" if temperature > 1.0 else "❄️ Low: Sharp & Confident" if temperature < 1.0 else "⚖️ Standard Softmax"}
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 🧠 Why not just divide by the total sum?")
st.markdown("""
You might wonder: *If we just want them to sum to 1, why not just divide the raw scores by their sum?*
1. **Negative numbers:** If a logit is negative (e.g., -2), dividing by the sum gives a negative probability, which is impossible! Exponentiating ($e^x$) makes *everything* positive.
2. **Exaggerating differences:** The exponential function $e^x$ grows very fast. If one raw score is slightly higher than another (e.g., 2.0 vs 1.0), $e^x$ makes the gap much wider (7.39 vs 2.72). This helps the model "pick a winner" confidently!
""")

