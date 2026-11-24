import sys
from pathlib import Path

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.nav import safe_page_link  # noqa: E402

# Configure page
st.set_page_config(page_title="Learning Curves", page_icon="📈", layout="wide")

# Custom CSS (theme-neutral: readable on dark and light themes)
st.markdown("""
<style>
    .main-header {
        font-family: 'Inter', sans-serif;
        font-size: 42px;
        font-weight: 800;
        color: inherit;
        margin-bottom: 0px;
    }
    .sub-header {
        font-family: 'Inter', sans-serif;
        font-size: 20px;
        color: #94A3B8;
        margin-top: -10px;
        margin-bottom: 30px;
    }
    .concept-card {
        background: rgba(148, 163, 184, 0.10);
        color: inherit;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(148, 163, 184, 0.35);
        margin-bottom: 24px;
    }
    .metric-card {
        background: rgba(148, 163, 184, 0.10);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid rgba(148, 163, 184, 0.35);
        margin-bottom: 15px;
    }
    .status-box {
        padding: 20px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 18px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .status-underfit { background-color: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; }
    .status-learning { background-color: #E0F2FE; color: #0369A1; border: 1px solid #BAE6FD; }
    .status-sweetspot { background-color: #DCFCE7; color: #166534; border: 1px solid #BBF7D0; }
    .status-overfit { background-color: #FEE2E2; color: #991B1B; border: 1px solid #FECACA; }
    
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        font-family: monospace;
        color: inherit;
    }
    .metric-label {
        font-size: 14px;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)


def trailing_mean(values, window=3):
    """Trailing moving average; the first points average over what is available (like min_periods=1)."""
    csum = np.cumsum(np.insert(values, 0, 0.0))
    idx = np.arange(1, len(values) + 1)
    start = np.maximum(idx - window, 0)
    return (csum[idx] - csum[start]) / (idx - start)


# Generate Data
@st.cache_data
def generate_curve_data(capacity, epochs=100):
    rng = np.random.default_rng(42) # Consistent noise without changing NumPy's global RNG.
    x = np.arange(1, epochs + 1)
    
    # Base dynamics based on capacity (1 to 10)
    decay_rate = 0.015 * capacity + 0.01
    asymptote = max(0.05, 1.4 - 0.15 * capacity)
    
    # Training loss goes down
    train_loss = 2.8 * np.exp(-decay_rate * x) + asymptote
    
    # Validation loss: slightly slower decay plus a small baseline gap that grows with capacity.
    # A simple (underfitting) model has a SMALL gap: it does about equally badly on both sets.
    base_gap = 0.02 + 0.012 * capacity
    val_loss = 2.9 * np.exp(-decay_rate * x * 0.85) + asymptote + base_gap
    
    # Overfitting penalty for high capacity
    if capacity > 4:
        overfit_start = max(10, 100 - (capacity - 4) * 12)
        penalty_factor = 0.00015 * (capacity - 4)
        
        penalty = np.zeros(epochs)
        mask = x > overfit_start
        penalty[mask] = penalty_factor * (x[mask] - overfit_start) ** 2
        val_loss += penalty
        
    # Add noise
    train_loss += rng.normal(0, 0.015, size=epochs)
    val_loss += rng.normal(0, 0.02, size=epochs)
    
    # Smooth them slightly for better visuals while keeping some noise
    train_loss = trailing_mean(train_loss, window=3)
    val_loss = trailing_mean(val_loss, window=3)
    
    # Ensure they don't go below 0
    train_loss = np.maximum(train_loss, 0.01)
    val_loss = np.maximum(val_loss, 0.01)
    
    return x, train_loss, val_loss


def online_early_stopping(val_loss, upto_epoch, patience):
    """Early stopping that only uses validation losses observed up to `upto_epoch`.

    Returns (best_epoch_so_far, stop_epoch or None).
    """
    best_val = np.inf
    best_epoch = 1
    for epoch in range(1, upto_epoch + 1):
        v = val_loss[epoch - 1]
        if v < best_val:
            best_val = v
            best_epoch = epoch
        elif epoch - best_epoch >= patience:
            return best_epoch, epoch
    return best_epoch, None

# Title Section
st.markdown('<div class="main-header">📈 Learning Curves</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Training Loss vs Validation Loss: Spotting the Gap</div>', unsafe_allow_html=True)
st.caption("These curves are synthetic illustrations of common patterns, not measurements from training a real model.")

with st.container():
    st.markdown("""
    <div class="concept-card">
        <p style="margin-bottom: 10px; font-size: 16px;">
            When training a neural network, we track two crucial numbers over time (Epochs):
        </p>
        <ul style="font-size: 16px; margin-bottom: 0px;">
            <li><strong style="color: #3b82f6;">Training Loss:</strong> Mistakes made on the data the model is actively learning from.</li>
            <li><strong style="color: #ef4444;">Validation Loss:</strong> Mistakes made on held-out data used to monitor and select a model. Keep a separate test set for a final evaluation.</li>
        </ul>
        <p style="margin-top: 10px; margin-bottom: 0px; font-size: 16px;">
            A model's goal isn't just to memorize training data—it's to <strong>generalize</strong>. If training loss falls while validation loss rises, that can signal overfitting, though the curves alone do not prove the cause.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Layout
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("### 🎛️ Controls")
    
    capacity = st.slider(
        "🧠 Model Capacity",
        min_value=1, max_value=10, value=7, key="p75_capacity",
        help="1 = lower capacity (may underfit)\n10 = higher capacity (may overfit)"
    )
    
    if capacity <= 3:
        st.caption("Status: Low Capacity (Simple Model)")
    elif capacity <= 6:
        st.caption("Status: Medium Capacity (Balanced)")
    else:
        st.caption("Status: High Capacity (Complex Model)")
        
    st.divider()
    
    current_epoch = st.slider(
        "⏱️ Training Epoch",
        min_value=1, max_value=100, value=60, key="p75_epoch",
        help="Drag to step through time and watch the curves evolve."
    )
    patience = st.slider(
        "⏳ Early-Stopping Patience (epochs)",
        min_value=1, max_value=30, value=10, key="p75_patience",
        help="Stop once validation loss has not improved for this many epochs, then restore the best weights seen so far."
    )
    show_hindsight = st.checkbox(
        "Reveal hindsight minimum (all 100 epochs)", value=False, key="p75_hindsight",
        help="For comparison only: the epoch with the lowest validation loss over the WHOLE run. "
             "A real training run cannot know this while it is still training."
    )
    
    # Generate data
    x, train_loss, val_loss = generate_curve_data(capacity, epochs=100)
    
    # Early stopping using ONLY the validation losses observed up to the current epoch
    best_epoch, stop_epoch = online_early_stopping(val_loss, current_epoch, patience)
    epochs_since_best = current_epoch - best_epoch
    hindsight_epoch = int(x[np.argmin(val_loss)])
    
    # Current values
    curr_train = train_loss[current_epoch - 1]
    curr_val = val_loss[current_epoch - 1]
    gap = curr_val - curr_train
    best_gap = val_loss[best_epoch - 1] - train_loss[best_epoch - 1]
    
    st.markdown("### 📊 Current Metrics")
    
    metric_html = f"""
    <div class="metric-card">
        <div class="metric-label" style="color: #3b82f6;">Training Loss</div>
        <div class="metric-value">{curr_train:.3f}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label" style="color: #ef4444;">Validation Loss</div>
        <div class="metric-value">{curr_val:.3f}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label" style="color: #8B5CF6;">Generalization Gap (Val − Train)</div>
        <div class="metric-value" style="color: #A78BFA;">{gap:.3f}</div>
    </div>
    """
    st.markdown(metric_html, unsafe_allow_html=True)

with col2:
    # Determine Status (uses only information available at the current epoch)
    if capacity <= 3 and current_epoch > 20:
        status = "underfit"
        status_msg = ("📉 Underfitting: both losses are still high and close together (small gap). "
                      "The model is too simple to fit even the training data well.")
    elif stop_epoch is not None and curr_val > val_loss[best_epoch - 1] + 0.05 and gap > best_gap + 0.05:
        status = "overfit"
        status_msg = (f"🚨 OVERFITTING: since epoch {best_epoch} training loss kept falling while validation loss rose and the gap widened. "
                      f"Early stopping (patience {patience}) stopped at epoch {stop_epoch} and restored epoch {best_epoch}.")
    elif stop_epoch is not None:
        status = "sweetspot"
        status_msg = (f"🎯 Early stopping triggered at epoch {stop_epoch}: no validation improvement for {patience} epochs. "
                      f"Restore the weights from epoch {best_epoch} (best validation loss seen so far).")
    elif epochs_since_best >= 3:
        status = "learning"
        status_msg = (f"⏳ Validation loss hasn't improved for {epochs_since_best} epochs (best so far: epoch {best_epoch}). "
                      f"Early stopping waits {patience} epochs before giving up.")
    else:
        status = "learning"
        status_msg = "🔄 Learning... validation loss is still improving."

    st.markdown(f'<div class="status-box status-{status}">{status_msg}</div>', unsafe_allow_html=True)
    st.write("") # Spacer

    # Plotly Chart
    plot_y_max = max(3.5, float(np.max(train_loss)), float(np.max(val_loss))) * 1.08
    fig = go.Figure()
    
    # Train Loss Trace
    fig.add_trace(go.Scatter(
        x=x[:current_epoch], 
        y=train_loss[:current_epoch],
        mode='lines',
        line=dict(color='#3b82f6', width=4),
        name='Training Loss'
    ))
    
    # Validation Loss Trace with Fill
    fig.add_trace(go.Scatter(
        x=x[:current_epoch], 
        y=val_loss[:current_epoch],
        mode='lines',
        fill='tonexty',
        fillcolor='rgba(239, 68, 68, 0.15)', # Light red gap
        line=dict(color='#ef4444', width=4),
        name='Validation Loss'
    ))
    
    # Add a marker for the current epoch
    fig.add_trace(go.Scatter(
        x=[current_epoch, current_epoch],
        y=[train_loss[current_epoch-1], val_loss[current_epoch-1]],
        mode='markers',
        marker=dict(color=['#3b82f6', '#ef4444'], size=10, line=dict(color='white', width=2)),
        showlegend=False
    ))
    
    # Early-stopping markers: only drawn once stopping has actually been triggered (both epochs are in the past)
    if stop_epoch is not None:
        fig.add_shape(
            type="line",
            x0=best_epoch, x1=best_epoch,
            y0=0,          y1=plot_y_max,
            line=dict(color="#22c55e", width=2, dash="dash"),
        )
        fig.add_annotation(
            x=best_epoch, y=plot_y_max * 0.9,
            text=f"Best epoch {best_epoch} (restored)",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#22c55e",
            arrowsize=1,
            arrowwidth=2,
            font=dict(color="#22c55e", size=12, family="Inter")
        )
        fig.add_shape(
            type="line",
            x0=stop_epoch, x1=stop_epoch,
            y0=0,          y1=plot_y_max,
            line=dict(color="#94A3B8", width=1, dash="dot"),
        )
        fig.add_annotation(
            x=stop_epoch, y=plot_y_max * 0.78,
            text=f"Stopped (patience {patience})",
            showarrow=False,
            xanchor="left", xshift=4,
            font=dict(color="#94A3B8", size=11, family="Inter")
        )
    
    if show_hindsight:
        fig.add_shape(
            type="line",
            x0=hindsight_epoch, x1=hindsight_epoch,
            y0=0,               y1=plot_y_max,
            line=dict(color="#F59E0B", width=2, dash="dashdot"),
        )
        fig.add_annotation(
            x=hindsight_epoch, y=plot_y_max * 0.66,
            text=f"Hindsight min: epoch {hindsight_epoch}",
            showarrow=False,
            xanchor="left", xshift=4,
            font=dict(color="#F59E0B", size=11, family="Inter")
        )
    
    fig.update_layout(
        template="plotly_dark",
        xaxis=dict(
            title="Epochs (Time)",
            range=[0, 105],
            gridcolor='rgba(255,255,255,0.08)',
            zeroline=False,
            title_font=dict(size=14, family="Inter")
        ),
        yaxis=dict(
            title="Loss (Error)",
            range=[0, plot_y_max],
            gridcolor='rgba(255,255,255,0.08)',
            zeroline=False,
            title_font=dict(size=14, family="Inter")
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            bgcolor="rgba(0, 0, 0, 0.5)",
            bordercolor="rgba(255,255,255,0.15)",
            borderwidth=1,
            font=dict(family="Inter", size=14)
        ),
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, width="stretch", config={'displayModeBar': False})
    if show_hindsight:
        st.caption(f"Hindsight minimum = epoch {hindsight_epoch}; online early stopping (patience {patience}) "
                   + (f"restored epoch {best_epoch}." if stop_epoch is not None else "has not stopped yet at this epoch.")
                   + " The difference shows why the hindsight minimum is not something a real training run can use.")

st.markdown("""
### 🧠 Intuition Check
* **What is the "Gap"?** The shaded area between the two lines is the **generalization gap** (validation loss − training loss): how much worse the model does on held-out data than on the data it trained on. The validation loss itself is our estimate of the *generalization error*.
* **Early Stopping:** Training stops once the validation loss has not improved for *patience* epochs, and the weights from the best epoch seen so far are restored. It only uses validation results observed so far — try a small patience with noisy curves to see it stop too early, or reveal the hindsight minimum to compare.
* **Model Capacity:** Try setting the capacity to 2. Notice how neither loss ever gets very low, and the two curves stay close together? That small gap with high losses is the signature of **underfitting**: the model just isn't flexible enough to learn the patterns in the data.
""")

st.markdown("**Next up:** the Neural Networks section continues with the tricks that make deep networks trainable — starting with *Weight Initialization*.")
safe_page_link("pages/93Weight Initialization.py", "Next: 93 · Weight Initialization", icon="➡️")