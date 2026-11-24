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
    <p>Earlier (Overfitting & Underfitting) we saw that a flexible model can <strong>overfit</strong> by fitting the noise in its training data. Overfit models often do this with very large weights that nearly cancel each other out.</p>
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
st.markdown(r"Imagine a single weight $w$. The data wants $w$ to be around **2.0** to minimize the error. But the Regularization Penalty wants $w$ to be exactly **0.0**. Watch who wins as you increase $\lambda$!")

col1, col2 = st.columns([1, 2])

with col1:
    reg_type_1d = st.radio("Choose Penalty Type (1D):", ["L1 (Absolute Value: |w|)", "L2 (Squared Value: w²)"], key="p74_rad1")
    lambda_1d = st.slider("Regularization Strength (λ)", min_value=0.0, max_value=6.0, value=1.0, step=0.1, key="p74_lam1")
    
    st.markdown(r"""
    **Observation:**
    - **L1** creates a sharp V-shaped penalty. Here the best weight is $w^* = \max(0,\ 2 - \lambda/2)$, so it hits **exactly 0** once $\lambda \ge 4$.
    - **L2** creates a smooth U-shaped penalty. Here $w^* = 2/(1+\lambda)$: it shrinks smoothly toward 0 but never reaches exactly 0.
    """)

with col2:
    w = np.linspace(-1.5, 3.5, 400)
    data_loss = (w - 2)**2
    
    is_l1 = "L1" in reg_type_1d
    penalty = np.abs(w) if is_l1 else w**2
    total_loss = data_loss + lambda_1d * penalty
    
    # Exact minimiser of (w - 2)^2 + λ·penalty(w) (closed form, no grid error)
    opt_w = max(0.0, 2.0 - lambda_1d / 2.0) if is_l1 else 2.0 / (1.0 + lambda_1d)
        
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
    st.plotly_chart(fig1, width="stretch")

st.markdown(f"<div class='card' style='text-align: center; padding: 1rem;'>Current Optimal Weight: <span style='font-size: 1.8rem; color: #FBBF24; font-weight: bold;'>{opt_w:.2f}</span></div>", unsafe_allow_html=True)


st.markdown("---")
# ---------------------------------------------------------
# SECTION 2: 2D Visualization
# ---------------------------------------------------------
st.markdown("### 2. The 2D Landscape: Why L1 causes Sparsity 🏔️")
st.markdown("Now let's look at a model with **two weights** ($w_1$ and $w_2$). The red contours represent the Data Loss (like a bowl). The cyan shape is the \"Penalty Budget\": every weight pair with the same penalty as the final answer. The final weights sit where the lowest red contour that still reaches the budget just **touches** it (dashed yellow contour).")

# Data loss E(w) = ½ (w - c)ᵀ H (w - c), i.e. (w1-3)² + 2(w2-1.5)² + 1.5(w1-3)(w2-1.5)
H_2D = np.array([[2.0, 1.5], [1.5, 4.0]])
C_2D = np.array([3.0, 1.5])


def data_loss_2d(wv):
    d = np.asarray(wv, dtype=float) - C_2D
    return 0.5 * d @ H_2D @ d


def solve_2d(lam, l1):
    """Exact minimiser of E(w) + lam * penalty(w)."""
    if not l1:
        # Ridge: H(w - c) + 2·lam·w = 0
        return np.linalg.solve(H_2D + 2.0 * lam * np.eye(2), H_2D @ C_2D)
    # Lasso: the optimum satisfies the stationarity equations of one sign pattern
    # (each weight negative, zero or positive), so solving every pattern and keeping the
    # best objective gives the exact global minimum of this convex problem.
    hc = H_2D @ C_2D
    best_w, best_obj = np.zeros(2), data_loss_2d(np.zeros(2))
    for s1 in (-1, 0, 1):
        for s2 in (-1, 0, 1):
            signs = np.array([s1, s2], dtype=float)
            support = signs != 0
            if not support.any():
                continue
            cand = np.zeros(2)
            cand[support] = np.linalg.solve(H_2D[np.ix_(support, support)], hc[support] - lam * signs[support])
            obj = data_loss_2d(cand) + lam * np.abs(cand).sum()
            if obj < best_obj - 1e-12:
                best_w, best_obj = cand, obj
    return best_w


# λ at which the Lasso solution first sets each weight to 0 (derived from the KKT conditions)
L1_W1_ZERO = 6.9   # for λ ≥ 6.9: w1 = 0, w2 = (10.5 - λ) / 4
L1_ALL_ZERO = 10.5  # for λ ≥ 10.5: both weights are 0

col3, col4 = st.columns([1, 2])

with col3:
    reg_type_2d = st.radio("Choose Penalty Type (2D):", ["L1 (Lasso) - Diamond", "L2 (Ridge) - Circle"], key="p74_rad2")
    lambda_2d = st.slider("Regularization Strength (λ)", min_value=0.0, max_value=12.0, value=2.0, step=0.5, key="p74_lam2")
    
    st.markdown(rf"""
    **What to watch for:**
    - Increase $\lambda$ to shrink the "Penalty Budget" (cyan shape pulls inwards).
    - **L1** is a diamond with pointy corners on the axes. For this bowl, small $\lambda$ still gives two non-zero weights
      (the contour touches a diamond *edge*). From $\lambda \ge {L1_W1_ZERO}$ it touches a **corner**, so $w_1$ is **exactly 0**,
      and from $\lambda \ge {L1_ALL_ZERO}$ both weights are 0. Corners stick out, so they are hit far more often than with a circle.
    - Notice it is $w_1$ (the larger unregularized weight) that is dropped first: the tilted bowl means the two weights are correlated,
      and the cheapest way to cut the penalty is to let $w_2$ take over.
    - **L2** is a circle (smooth): the contour touches it at a generic point, so the weights shrink but never become exactly 0 here.
    """)

with col4:
    # Grid only for drawing the background contours
    w1_range = np.linspace(-1.5, 4.5, 201)
    w2_range = np.linspace(-1.5, 4.5, 201)
    W1, W2 = np.meshgrid(w1_range, w2_range)
    
    # Tilted ellipse for data loss: with L1 the solution reaches the w2-axis (w1 = 0) for large λ
    W1_c = W1 - 3.0
    W2_c = W2 - 1.5
    E = W1_c**2 + 2*W2_c**2 + 1.5*W1_c*W2_c
    
    is_l1_2d = "L1" in reg_type_2d
    w_opt = solve_2d(lambda_2d, is_l1_2d)
    w1_opt, w2_opt = (float(v) + 0.0 for v in np.round(w_opt, 12))
        
    p_opt = abs(w1_opt) + abs(w2_opt) if is_l1_2d else w1_opt**2 + w2_opt**2
    e_opt = float(data_loss_2d([w1_opt, w2_opt]))
    
    fig2 = go.Figure()
    
    # Data Loss Contours (Background)
    fig2.add_trace(go.Contour(
        x=w1_range, y=w2_range, z=E,
        colorscale='Reds_r', opacity=0.6, showscale=False,
        contours=dict(start=0, end=15, size=1.5, showlines=True),
        hoverinfo='skip'
    ))
    
    # The data-loss contour through the final weights (tangent to the budget shape)
    if e_opt > 1e-9:
        A = H_2D / 2.0
        R = np.linalg.cholesky(A)  # A = R Rᵀ
        t = np.linspace(0, 2 * np.pi, 200)
        unit = np.vstack([np.cos(t), np.sin(t)])
        ell = C_2D[:, None] + np.sqrt(e_opt) * np.linalg.solve(R.T, unit)
        fig2.add_trace(go.Scatter(x=ell[0], y=ell[1], mode='lines', line=dict(color='#FBBF24', width=2, dash='dash'),
                                  name='Touching data-loss contour', hoverinfo='skip'))
    
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
    st.plotly_chart(fig2, width="stretch")
    if is_l1_2d and lambda_2d > 0:
        if w1_opt == 0.0 and w2_opt == 0.0:
            st.caption(f"λ = {lambda_2d:.1f} ≥ {L1_ALL_ZERO}: the penalty wins completely — both weights are exactly 0.")
        elif w1_opt == 0.0 or w2_opt == 0.0:
            st.caption(f"λ = {lambda_2d:.1f}: the solution sits on a diamond **corner** — one weight is exactly 0 (sparse).")
        else:
            st.caption(f"λ = {lambda_2d:.1f}: the contour touches a diamond **edge**, so both weights are still non-zero. "
                       f"Increase λ to {L1_W1_ZERO} or more to see a corner solution.")

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
            <li><strong>Effect:</strong> Can set many weights to exactly <strong>0</strong> (once λ is large enough).</li>
            <li><strong>Superpower: Feature Selection!</strong> With many features of which most are useless, L1 tends to set many of their weights to exactly zero. Caveat: among strongly correlated features it may keep one somewhat arbitrarily and drop the others.</li>
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
            <li><strong>Superpower: General Stability!</strong> When you want to keep all features but just don't want the model to rely too heavily on any single one. Very common in Neural Networks, where it is closely related to "Weight Decay" (identical for plain SGD; for Adam, use decoupled weight decay, i.e. AdamW).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)