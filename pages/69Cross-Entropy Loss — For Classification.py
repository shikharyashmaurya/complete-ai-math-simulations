import streamlit as st
import numpy as np
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
    Cross-Entropy measures <strong>surprise</strong> (the "surprisal" −ln p of the true answer). If the model is 99% confident it's a Dog, and it <i>is</i> a Dog, the surprise is near zero. But if the model is 99% confident it's a Cat, and it's actually a Dog, the penalty EXPLODES! 💥
</div>
""", unsafe_allow_html=True)

st.divider()

st.header("1. The Core Idea: Penalizing False Confidence")
st.markdown("Imagine our model is trying to classify an image. We already know the TRUE answer is a **Dog**. How does the loss change based on the model's prediction?")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown("### Model's Prediction")
    st.markdown("Adjust the slider to see how the penalty changes.")
    p_dog = st.slider("Probability it's a Dog (True Class)", min_value=0.01, max_value=0.99, value=0.50, step=0.01, key="p69_p_dog")
    
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
    
    st.markdown(r"""
    **The Formula (for one example):**
    $$ \text{Loss} = -\ln(\text{Probability of TRUE Class}) $$

    This is the general cross-entropy with a one-hot target written compactly:

    - **Binary** (label $y \in \{0, 1\}$, predicted $p = P(y=1)$):
      $\; L = -\big[\,y \ln p + (1-y)\ln(1-p)\,\big]$
    - **Multi-class** (one-hot $y_k$, predicted $p_k$):
      $\; L = -\sum_k y_k \ln p_k$

    Only the term for the true class survives, which gives $-\ln(p_{\text{true}})$.
    """)
    st.caption("Since ln(0) is undefined, real libraries clip probabilities to a tiny ε or compute the loss directly from "
               "logits (log-softmax). This slider stops at 0.01 for the same reason.")

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
    
    # Dotted drop-line from the current point to the x-axis
    fig1.add_trace(go.Scatter(
        x=[p_dog, p_dog],
        y=[0, loss],
        mode='lines',
        line=dict(color=color, width=2, dash='dot'),
        showlegend=False,
        hoverinfo='skip'
    ))

    fig1.update_layout(
        title="Cross-Entropy Curve: y = −ln(x)",
        xaxis_title="Predicted Probability of True Class",
        yaxis_title="Penalty (Loss)",
        template="plotly_dark",
        height=450,
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis=dict(range=[0, 1.05]),
        yaxis=dict(range=[0, 5])
    )
    st.plotly_chart(fig1, width="stretch")


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
    true_label = st.radio("What is the ACTUAL image?", ["Dog", "Cat", "Bird"], index=0, key="p69_true_label")
    
    st.markdown("Set the model's raw scores (**logits**). Like a real classifier, we turn them into probabilities that sum to 100% with the **softmax** function: $p_k = e^{z_k} / \\sum_j e^{z_j}$.")
    raw_dog = st.slider("Dog score (logit)", -5.0, 5.0, 2.0, step=0.1, key="p69_logit_dog")
    raw_cat = st.slider("Cat score (logit)", -5.0, 5.0, 1.0, step=0.1, key="p69_logit_cat")
    raw_bird = st.slider("Bird score (logit)", -5.0, 5.0, 0.3, step=0.1, key="p69_logit_bird")
    
    logits = np.array([raw_dog, raw_cat, raw_bird])
    exp_logits = np.exp(logits - logits.max())  # subtract max for numerical stability
    p_dog_mc, p_cat_mc, p_bird_mc = exp_logits / exp_logits.sum()
    
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
    st.plotly_chart(fig2, width="stretch")
    
    st.markdown(f"""
    <div style="background-color: #2b2b3b; padding: 20px; border-radius: 10px; text-align: center; color: white;">
        <h3 style="margin:0;">Loss Calculation</h3>
        <p style="font-size: 1.2rem; margin:10px 0;">The model predicted the true class (<b>{true_label}</b>) with <b>{p_true*100:.1f}%</b> probability.</p>
        <p style="font-family: monospace; font-size: 1.5rem; color: #ff4b4b; margin:0;">Loss = -ln({p_true:.5g}) = <b>{ce_loss_mc:.4f}</b></p>
    </div>
    """, unsafe_allow_html=True)


st.divider()

st.header("3. Why Cross-Entropy is better than MSE for Classification")
st.markdown("""
Why can't we just use Mean Squared Error (MSE)? Look at what happens when the model is completely, terribly wrong (Predicted True Class Prob = 0.01).
""")

comp_col1, comp_col2, comp_col3 = st.columns(3)

with comp_col1:
    st.markdown(r"""
    **Mean Squared Error (MSE)**
    - True-class term only: $(1 - p)^2$
    - If p = 0.01: $(1 - 0.01)^2 \approx 0.98$
    - Bounded: at most **1** for this term (at most **2** for full one-hot MSE $\sum_k (y_k - p_k)^2$).
    - The penalty for being disastrously wrong stays small.
    """)

with comp_col2:
    st.markdown(r"""
    **Cross-Entropy**
    - Formula: $-\ln(p)$
    - If p = 0.01: $-\ln(0.01) \approx 4.6$
    - Penalty **grows without bound** as the probability approaches 0.
    - Its gradient stays large when the model is confidently wrong (see below).
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
    st.plotly_chart(fig3, width="stretch")

st.markdown("#### The real reason: the learning signal (gradient)")
grad_col1, grad_col2 = st.columns([1.2, 1])
with grad_col1:
    st.markdown(r"""
    Classifiers produce $p$ from a raw score $z$ with a sigmoid (or softmax): $p = \sigma(z)$.
    Training follows the gradient with respect to $z$. For a true label $y = 1$:

    - **MSE:** $\dfrac{\partial}{\partial z}(1-p)^2 = -2\,p\,(1-p)^2$
    - **Cross-Entropy:** $\dfrac{\partial}{\partial z}\big(-\ln p\big) = p - 1$

    At $p = 0.01$ (confidently wrong): MSE gives a gradient of only about $-0.02$, while
    cross-entropy gives $-0.99$ — roughly **50× stronger**. The sigmoid "flattens" MSE's
    signal exactly when the model needs it most; cross-entropy cancels that flattening.
    """)
with grad_col2:
    p_grad = np.linspace(0.001, 0.999, 300)
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=p_grad, y=np.abs(p_grad - 1), mode='lines', name='|∂CE/∂z|', line=dict(color='#ff4b4b')))
    fig4.add_trace(go.Scatter(x=p_grad, y=np.abs(2 * p_grad * (1 - p_grad) ** 2), mode='lines', name='|∂MSE/∂z|', line=dict(color='#4444ff')))
    fig4.update_layout(
        title="Gradient size vs. true-class probability",
        xaxis_title="True Class Probability p",
        yaxis_title="|gradient w.r.t. logit z|",
        template="plotly_dark",
        height=280,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
    )
    st.plotly_chart(fig4, width="stretch")

st.success("🎉 **Takeaway:** Cross-Entropy loss acts as an amplifier for mistakes. It gives the model a tiny slap on the wrist when it's slightly off, but drops an anvil on it when it's confidently wrong!")