import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="L1 & L2 Regularization", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for dark modern aesthetic
st.markdown("""
<style>
    .main-title { font-size: 2.8rem; font-weight: 800; color: #60A5FA; margin-bottom: 0rem; }
    .subtitle { font-size: 1.3rem; color: #9CA3AF; margin-bottom: 2rem; }
    .card { background-color: #1F2937; color: #F3F4F6; padding: 1.5rem; border-radius: 0.75rem; margin-bottom: 1.5rem; border: 1px solid #374151; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
    .highlight { color: #FBBF24; font-weight: bold; }
    .l1-color { color: #34D399; font-weight: bold; }
    .l2-color { color: #60A5FA; font-weight: bold; }
    .math-formula { text-align: center; font-size: 1.4rem; background: rgba(0,0,0,0.2); color: #F3F4F6; padding: 15px; border-radius: 8px; border-left: 4px solid #F472B6; margin: 15px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">74. L1 & L2 Regularization</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Taming the weights: Adding a penalty to prevent overfitting</p>', unsafe_allow_html=True)

st.markdown("""
<div class="card">
    <p>In the previous lesson, we saw that a model can <strong>overfit</strong> by memorizing the training data perfectly. It often does this by assigning extremely large, crazy weights to certain features.</p>
    <p><strong>Regularization</strong> is a brilliant trick to prevent this. We change our goal: instead of just minimizing the prediction error, we also <strong>penalize</strong> the model for having large weights!</p>
    <div class="math-formula">
        Total Loss = Prediction Error + <span style="color:#F472B6; font-weight:bold;">λ</span> × Weight Penalty
    </div>
    <p>The parameter <strong style="color:#F472B6;">λ (Lambda)</strong> controls how strict we are. Let's explore the two most famous penalties: <span class="l1-color">L1 (Lasso)</span> and <span class="l2-color">L2 (Ridge)</span>.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SECTION 1: 1D Visualization
# ---------------------------------------------------------
st.markdown("### 1. The 1D Tug of War 🪢")
st.markdown("Imagine a single weight $w$. The data wants $w$ to be around **2.0** to minimize the error. But the Regularization Penalty wants $w$ to be exactly **0.0**. Watch who wins as you increase $\lambda$!")

col1, col2 = st.columns([1, 2])

with col1:
    reg_type_1d = st.radio("Choose Penalty Type (1D):", ["L1 (Absolute Value: |w|)", "L2 (Squared Value: w²)"], key="rad1")
    lambda_1d = st.slider("Regularization Strength (λ)", min_value=0.0, max_value=6.0, value=1.0, step=0.1, key="lam1")
    
    st.markdown("""
    **Observation:**
    - **L1** creates a sharp V-shaped penalty. Notice how it can drag the optimal weight **exactly to 0**.
    - **L2** creates a smooth U-shaped penalty. It shrinks the weight towards 0 smoothly, but rarely makes it exactly 0.
    """)

with col2:
    w = np.linspace(-1.5, 3.5, 400)
    data_loss = (w - 2)**2
    
    is_l1 = "L1" in reg_type_1d
    penalty = np.abs(w) if is_l1 else w**2
    total_loss = data_loss + lambda_1d * penalty
    
    min_idx = np.argmin(total_loss)
    opt_w = w[min_idx]
    
    # Snap to exactly 0 for L1 if it's analytically zero (to avoid grid resolution artifacts)
    if is_l1 and lambda_1d >= 4.0:
        opt_w = 0.0
        
    fig1 = go.Figure()
    # Data loss
    fig1.add_trace(go.Scatter(x=w, y=data_loss, mode='lines', name='Data Loss', line=dict(color='rgba(239, 68, 68, 0.6)', dash='dash')))
    # Penalty
    fig1.add_trace(go.Scatter(x=w, y=lambda_1d*penalty, mode='lines', name='Penalty', line=dict(color='rgba(59, 130, 246, 0.6)', dash='dash')))
    # Total loss
    fig1.add_trace(go.Scatter(x=w, y=total_loss, mode='lines', name='Total Loss', line=dict(color='#FBBF24', width=4)))
    
    # Minimum point
    min_loss_val = (opt_w-2)**2 + lambda_1d*(abs(opt_w) if is_l1 else opt_w**2)
    fig1.add_trace(go.Scatter(x=[opt_w], y=[min_loss_val], mode='markers', name='Best Weight',
                              marker=dict(color='white', size=14, line=dict(color='#FBBF24', width=3))))
    
    fig1.add_vline(x=0, line_width=2, line_dash="dot", line_color="rgba(255,255,255,0.4)")
    
    fig1.update_layout(
        template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="Weight Value (w)", yaxis_title="Loss",
        legend=dict(yanchor="top", y=0.95, xanchor="center", x=0.5, orientation="h"),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        height=350
    )
    st.plotly_chart(fig1, use_container_width=True)

st.markdown(f"<div class='card' style='text-align: center; padding: 1rem;'>Current Optimal Weight: <span style='font-size: 1.8rem; color: #FBBF24; font-weight: bold;'>{opt_w:.2f}</span></div>", unsafe_allow_html=True)


st.markdown("---")
# ---------------------------------------------------------
# SECTION 2: 2D Visualization
# ---------------------------------------------------------
st.markdown("### 2. The 2D Landscape: Why L1 causes Sparsity 🏔️")
st.markdown("Now let's look at a model with **two weights** ($w_1$ and $w_2$). The red contours represent the Data Loss (like a bowl). The blue shape is our \"Penalty Budget\". The final weights will be where the red bowl touches the smallest possible blue shape.")

col3, col4 = st.columns([1, 2])

with col3:
    reg_type_2d = st.radio("Choose Penalty Type (2D):", ["L1 (Lasso) - Diamond", "L2 (Ridge) - Circle"], key="rad2")
    lambda_2d = st.slider("Regularization Strength (λ)", min_value=0.0, max_value=12.0, value=2.0, step=0.5, key="lam2")
    
    st.markdown("""
    **What to watch for:**
    - Increase $\lambda$ to shrink the "Penalty Budget" (Blue shape pulls inwards).
    - Because **L1** is a diamond (pointy corners), the Data Loss bowl will almost always hit a corner first. A corner means one of the weights is **exactly 0**!
    - Because **L2** is a circle (smooth), it hits somewhere on the curve. Weights get small, but rarely zero.
    """)

with col4:
    # Finer grid and explicit 0.0 to ensure axis hits are perfectly calculated
    w1_range = np.sort(np.append(np.linspace(-1.5, 4.5, 200), [0.0]))
    w2_range = np.sort(np.append(np.linspace(-1.5, 4.5, 200), [0.0]))
    W1, W2 = np.meshgrid(w1_range, w2_range)
    
    # Tilted ellipse for data loss so it hits the w1 axis beautifully for L1
    W1_c = W1 - 3.0
    W2_c = W2 - 1.5
    E = W1_c**2 + 2*W2_c**2 + 1.5*W1_c*W2_c
    
    is_l1_2d = "L1" in reg_type_2d
    P = np.abs(W1) + np.abs(W2) if is_l1_2d else W1**2 + W2**2
    
    Total_Loss = E + lambda_2d * P
    
    min_idx = np.unravel_index(np.argmin(Total_Loss), Total_Loss.shape)
    w1_opt = W1[min_idx]
    w2_opt = W2[min_idx]
    
    # Snap to exactly 0 if extremely close (cleaner UI)
    if abs(w1_opt) < 0.05: w1_opt = 0.0
    if abs(w2_opt) < 0.05: w2_opt = 0.0
        
    p_opt = np.abs(w1_opt) + np.abs(w2_opt) if is_l1_2d else w1_opt**2 + w2_opt**2
    
    fig2 = go.Figure()
    
    # Data Loss Contours (Background)
    fig2.add_trace(go.Contour(
        x=w1_range, y=w2_range, z=E,
        colorscale='Reds_r', opacity=0.6, showscale=False,
        contours=dict(start=0, end=15, size=1.5, showlines=True),
        hoverinfo='skip'
    ))
    
    # Penalty Contour (Budget)
    if p_opt > 0.02:
        if is_l1_2d:
            # Diamond vertices
            cx, cy = [p_opt, 0, -p_opt, 0, p_opt], [0, p_opt, 0, -p_opt, 0]
            fig2.add_trace(go.Scatter(x=cx, y=cy, mode='lines', line=dict(color='cyan', width=3), name='Penalty Budget', hoverinfo='skip'))
            fig2.add_trace(go.Scatter(x=cx, y=cy, fill="toself", fillcolor="rgba(0, 255, 255, 0.1)", mode="none", showlegend=False, hoverinfo='skip'))
        else:
            # Circle
            theta = np.linspace(0, 2*np.pi, 100)
            r = np.sqrt(p_opt)
            cx, cy = r*np.cos(theta), r*np.sin(theta)
            fig2.add_trace(go.Scatter(x=cx, y=cy, mode='lines', line=dict(color='cyan', width=3), name='Penalty Budget', hoverinfo='skip'))
            fig2.add_trace(go.Scatter(x=cx, y=cy, fill="toself", fillcolor="rgba(0, 255, 255, 0.1)", mode="none", showlegend=False, hoverinfo='skip'))
            
    # Unregularized Optimum
    fig2.add_trace(go.Scatter(x=[3.0], y=[1.5], mode='markers', marker=dict(color='red', symbol='x', size=12), name='Unregularized (Data Only)'))
    
    # Regularized Optimum
    fig2.add_trace(go.Scatter(x=[w1_opt], y=[w2_opt], mode='markers', marker=dict(color='#FBBF24', symbol='star', size=18, line=dict(color='white', width=1)), name='Final Weights'))
    
    fig2.add_hline(y=0, line_width=2, line_color="rgba(255,255,255,0.4)")
    fig2.add_vline(x=0, line_width=2, line_color="rgba(255,255,255,0.4)")
    
    fig2.update_layout(
        template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="Weight 1 (w₁)", yaxis_title="Weight 2 (w₂)",
        xaxis=dict(range=[-1.5, 4.5], scaleanchor="y", scaleratio=1), # Equal aspect ratio is crucial here!
        yaxis=dict(range=[-1.5, 4.5]),
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99, bgcolor="rgba(0,0,0,0.6)"),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        height=500
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown(f"""
<div class='card' style='display: flex; justify-content: space-around; padding: 1rem;'>
    <div style='text-align: center;'>
        <p style='color: #9CA3AF; margin-bottom: 5px; font-size: 1.2rem;'>Final Weight 1</p>
        <p style='font-size: 1.8rem; color: #FBBF24; margin: 0; font-weight: bold;'>{w1_opt:.2f}</p>
    </div>
    <div style='text-align: center;'>
        <p style='color: #9CA3AF; margin-bottom: 5px; font-size: 1.2rem;'>Final Weight 2</p>
        <p style='font-size: 1.8rem; color: #FBBF24; margin: 0; font-weight: bold;'>{w2_opt:.2f}</p>
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown("---")
# ---------------------------------------------------------
# SECTION 3: Summary
# ---------------------------------------------------------
st.markdown("### 📝 Summary: Which one should I use?")
col5, col6 = st.columns(2)
with col5:
    st.markdown("""
    <div style='background-color: rgba(52, 211, 153, 0.1); padding: 1.5rem; border-radius: 0.5rem; border: 1px solid #34D399; height: 100%; color: #E5E7EB;'>
        <h4 style='color: #34D399; margin-top: 0;'>L1 Regularization (Lasso)</h4>
        <ul style='font-size: 1.1rem; line-height: 1.6;'>
            <li><strong>Shape:</strong> Diamond 🔶</li>
            <li><strong>Effect:</strong> Forces many weights to be exactly <strong>0</strong>.</li>
            <li><strong>Superpower: Feature Selection!</strong> If you have 1000 features and know most are useless, L1 will automatically delete the bad ones by setting their weights to zero.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
with col6:
    st.markdown("""
    <div style='background-color: rgba(96, 165, 250, 0.1); padding: 1.5rem; border-radius: 0.5rem; border: 1px solid #60A5FA; height: 100%; color: #E5E7EB;'>
        <h4 style='color: #60A5FA; margin-top: 0;'>L2 Regularization (Ridge)</h4>
        <ul style='font-size: 1.1rem; line-height: 1.6;'>
            <li><strong>Shape:</strong> Circle 🔵</li>
            <li><strong>Effect:</strong> Shrinks all weights to be small, but rarely exactly 0.</li>
            <li><strong>Superpower: General Stability!</strong> When you want to keep all features but just don't want the model to rely too heavily on any single one. Very common in Neural Networks (often called "Weight Decay").</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)