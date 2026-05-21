import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Cross-Entropy Loss", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for modern aesthetics
st.markdown("""
<style>
    .main-header {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 3rem;
        color: #ff4b4b;
        margin-bottom: 0rem;
        text-align: center;
    }
    .sub-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        color: #aaaaaa;
        text-align: center;
        margin-bottom: 2rem;
    }
    .concept-box {
        background-color: #1e1e2e;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #ff4b4b;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        color: white;
    }
    .highlight {
        color: #ff4b4b;
        font-weight: bold;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">Cross-Entropy Loss</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">The Penalty for False Confidence in Classification</div>', unsafe_allow_html=True)

st.markdown("""
<div class="concept-box">
    <strong>What is Cross-Entropy Loss?</strong><br>
    While Mean Squared Error (MSE) is great for guessing exact numbers (like predicting a house price), it doesn't work well for <strong>categories</strong> (like "Is this a Dog or a Cat?").<br>
    Cross-Entropy measures <strong>surprise</strong>. If the model is 99% confident it's a Dog, and it <i>is</i> a Dog, the surprise is near zero. But if the model is 99% confident it's a Cat, and it's actually a Dog, the penalty EXPLODES! 💥
</div>
""", unsafe_allow_html=True)

st.divider()

st.header("1. The Core Idea: Penalizing False Confidence")
st.markdown("Imagine our model is trying to classify an image. We already know the TRUE answer is a **Dog**. How does the loss change based on the model's prediction?")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown("### Model's Prediction")
    st.markdown("Adjust the slider to see how the penalty changes.")
    p_dog = st.slider("Probability it's a Dog (True Class)", min_value=0.01, max_value=0.99, value=0.50, step=0.01)
    
    loss = -np.log(p_dog)
    
    st.markdown("### Calculated Penalty (Loss)")
    if loss < 0.1:
        color = "#00ff00" # Green
        msg = "Perfect! Very low penalty."
    elif loss < 0.7:
        color = "#ffff00" # Yellow
        msg = "Not bad, but could be more confident."
    elif loss < 1.5:
        color = "#ffaa00" # Orange
        msg = "Needs improvement. Penalty is growing."
    else:
        color = "#ff0000" # Red
        msg = "HUGE PENALTY! Confidently wrong!"
        
    st.markdown(f'<div class="metric-value" style="color: {color};">{loss:.3f}</div>', unsafe_allow_html=True)
    st.markdown(f"*{msg}*")
    
    st.markdown("""
    **The Formula:**
    $$ \\text{Loss} = -\\ln(\\text{Probability of TRUE Class}) $$
    """)

with col2:
    # Plot -log(x) curve
    x_vals = np.linspace(0.001, 1.0, 200)
    y_vals = -np.log(x_vals)
    
    fig1 = go.Figure()
    # The curve
    fig1.add_trace(go.Scatter(
        x=x_vals, y=y_vals, 
        mode='lines', 
        name='Penalty Curve',
        line=dict(color='#4444ff', width=4)
    ))
    
    # The moving point
    fig1.add_trace(go.Scatter(
        x=[p_dog], y=[loss],
        mode='markers+text',
        name='Current Prediction',
        marker=dict(color=color, size=20, line=dict(color='white', width=2)),
        text=[f"Loss: {loss:.2f}"],
        textposition="top right",
        textfont=dict(size=16, color="white")
    ))
    
    # Fill under curve for emphasis
    fig1.add_trace(go.Scatter(
        x=np.concatenate([x_vals[x_vals <= p_dog], [p_dog]]),
        y=np.concatenate([y_vals[x_vals <= p_dog], [0]]),
        fill='tozeroy',
        fillcolor='rgba(255, 75, 75, 0.1)',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))

    fig1.update_layout(
        title="Cross-Entropy Curve: $y = -\\ln(x)$",
        xaxis_title="Predicted Probability of True Class",
        yaxis_title="Penalty (Loss)",
        template="plotly_dark",
        height=450,
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis=dict(range=[0, 1.05]),
        yaxis=dict(range=[0, 5])
    )
    st.plotly_chart(fig1, use_container_width=True)


st.divider()

st.header("2. Multi-Class Scenario: What about the other classes?")
st.markdown("""
In reality, the model predicts probabilities for *all* possible classes (which must sum to 100%).
Here is the secret of Cross-Entropy: **It only directly penalizes the probability given to the TRUE class!** 
The other probabilities only matter because if you give them a high score, you are stealing probability away from the true class.
""")

st.markdown("### The 'Is it a Dog, Cat, or Bird?' Game")

mc_col1, mc_col2 = st.columns([1, 2])

with mc_col1:
    true_label = st.radio("What is the ACTUAL image?", ["Dog", "Cat", "Bird"], index=0)
    
    st.markdown("Set the model's raw confidence (these will be normalized to sum to 100%):")
    raw_dog = st.slider("Raw Dog Confidence", 0.01, 10.0, 5.0, step=0.1)
    raw_cat = st.slider("Raw Cat Confidence", 0.01, 10.0, 2.0, step=0.1)
    raw_bird = st.slider("Raw Bird Confidence", 0.01, 10.0, 1.0, step=0.1)
    
    total = raw_dog + raw_cat + raw_bird
    p_dog_mc = raw_dog / total
    p_cat_mc = raw_cat / total
    p_bird_mc = raw_bird / total
    
    probs = {"Dog": p_dog_mc, "Cat": p_cat_mc, "Bird": p_bird_mc}
    p_true = probs[true_label]
    ce_loss_mc = -np.log(p_true)

with mc_col2:
    # Bar chart for probabilities
    fig2 = go.Figure()
    
    colors = ['#555555'] * 3
    labels = ["Dog", "Cat", "Bird"]
    values = [p_dog_mc, p_cat_mc, p_bird_mc]
    
    true_idx = labels.index(true_label)
    colors[true_idx] = '#ff4b4b' # Highlight true class
    
    fig2.add_trace(go.Bar(
        x=labels,
        y=values,
        marker_color=colors,
        text=[f"{v*100:.1f}%" for v in values],
        textposition='auto',
        name="Predictions"
    ))
    
    # Add target markers (0 for wrong, 1 for true)
    fig2.add_trace(go.Scatter(
        x=labels,
        y=[1 if l == true_label else 0 for l in labels],
        mode='markers',
        marker=dict(symbol='star', size=15, color='gold'),
        name="Target (Truth)"
    ))

    fig2.update_layout(
        title=f"Model Predictions (True Class: {true_label})",
        yaxis_title="Probability",
        yaxis=dict(range=[0, 1.1]),
        template="plotly_dark",
        height=350,
        margin=dict(l=40, r=40, t=60, b=40),
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown(f"""
    <div style="background-color: #2b2b3b; padding: 20px; border-radius: 10px; text-align: center; color: white;">
        <h3 style="margin:0;">Loss Calculation</h3>
        <p style="font-size: 1.2rem; margin:10px 0;">The model predicted the true class (<b>{true_label}</b>) with <b>{p_true*100:.1f}%</b> probability.</p>
        <p style="font-family: monospace; font-size: 1.5rem; color: #ff4b4b; margin:0;">Loss = -ln({p_true:.3f}) = <b>{ce_loss_mc:.3f}</b></p>
    </div>
    """, unsafe_allow_html=True)


st.divider()

st.header("3. Why Cross-Entropy is better than MSE for Classification")
st.markdown("""
Why can't we just use Mean Squared Error (MSE)? Look at what happens when the model is completely, terribly wrong (Predicted True Class Prob = 0.01).
""")

comp_col1, comp_col2, comp_col3 = st.columns(3)

with comp_col1:
    st.markdown("""
    **Mean Squared Error (MSE)**
    - Formula: $(1 - p)^2$
    - If p = 0.01: $(1 - 0.01)^2 = 0.98$
    - Max penalty is capped at **1.0**. 
    - The model isn't "punished" enough for being disastrously wrong.
    """)

with comp_col2:
    st.markdown("""
    **Cross-Entropy**
    - Formula: $-\\ln(p)$
    - If p = 0.01: $-\\ln(0.01) \\approx 4.6$
    - Penalty **shoots to infinity** as probability approaches 0.
    - Forces the model to rapidly correct its mistakes!
    """)

with comp_col3:
    # Mini plot comparing MSE and CE
    x_comp = np.linspace(0.01, 1.0, 100)
    mse_vals = (1 - x_comp)**2
    ce_vals = -np.log(x_comp)
    
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=x_comp, y=ce_vals, mode='lines', name='Cross-Entropy', line=dict(color='#ff4b4b')))
    fig3.add_trace(go.Scatter(x=x_comp, y=mse_vals, mode='lines', name='MSE', line=dict(color='#4444ff')))
    
    fig3.update_layout(
        title="CE vs MSE Penalty",
        xaxis_title="True Class Probability",
        yaxis_title="Penalty",
        template="plotly_dark",
        height=250,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
    )
    st.plotly_chart(fig3, use_container_width=True)

st.success("🎉 **Takeaway:** Cross-Entropy loss acts as an amplifier for mistakes. It gives the model a tiny slap on the wrist when it's slightly off, but drops an anvil on it when it's confidently wrong!")