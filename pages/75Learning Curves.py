import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Configure page
st.set_page_config(page_title="Learning Curves", page_icon="📈", layout="wide")

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .main-header {
        font-family: 'Inter', sans-serif;
        font-size: 42px;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 0px;
    }
    .sub-header {
        font-family: 'Inter', sans-serif;
        font-size: 20px;
        color: #64748B;
        margin-top: -10px;
        margin-bottom: 30px;
    }
    .concept-card {
        background: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #E2E8F0;
        margin-bottom: 24px;
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
        font-family: 'monospace';
    }
    .metric-label {
        font-size: 14px;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# Generate Data
@st.cache_data
def generate_curve_data(capacity, epochs=100):
    np.random.seed(42) # Consistent noise
    x = np.arange(1, epochs + 1)
    
    # Base dynamics based on capacity (1 to 10)
    decay_rate = 0.015 * capacity + 0.01
    asymptote = max(0.05, 1.4 - 0.15 * capacity)
    
    # Training loss goes down
    train_loss = 2.8 * np.exp(-decay_rate * x) + asymptote
    
    # Validation loss base
    val_loss = 2.9 * np.exp(-decay_rate * x * 0.85) + asymptote + 0.15
    
    # Overfitting penalty for high capacity
    if capacity > 4:
        overfit_start = max(10, 100 - (capacity - 4) * 12)
        penalty_factor = 0.00015 * (capacity - 4)
        
        penalty = np.zeros(epochs)
        mask = x > overfit_start
        penalty[mask] = penalty_factor * (x[mask] - overfit_start) ** 2
        val_loss += penalty
        
    # Add noise
    train_loss += np.random.normal(0, 0.015, size=epochs)
    val_loss += np.random.normal(0, 0.02, size=epochs)
    
    # Smooth them slightly for better visuals while keeping some noise
    train_loss = pd.Series(train_loss).rolling(window=3, min_periods=1).mean().values
    val_loss = pd.Series(val_loss).rolling(window=3, min_periods=1).mean().values
    
    # Ensure they don't go below 0
    train_loss = np.maximum(train_loss, 0.01)
    val_loss = np.maximum(val_loss, 0.01)
    
    return x, train_loss, val_loss

# Title Section
st.markdown('<div class="main-header">📈 Learning Curves</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Training Loss vs Validation Loss: Spotting the Gap</div>', unsafe_allow_html=True)

with st.container():
    st.markdown("""
    <div class="concept-card">
        <p style="margin-bottom: 10px; font-size: 16px;">
            When training a neural network, we track two crucial numbers over time (Epochs):
        </p>
        <ul style="font-size: 16px; margin-bottom: 0px;">
            <li><strong style="color: #3b82f6;">Training Loss:</strong> Mistakes made on the data the model is actively learning from.</li>
            <li><strong style="color: #ef4444;">Validation Loss:</strong> Mistakes made on <em>new, unseen</em> data. This is the true test!</li>
        </ul>
        <p style="margin-top: 10px; margin-bottom: 0px; font-size: 16px;">
            A model's goal isn't just to memorize training data—it's to <strong>generalize</strong>. If training loss goes down but validation loss goes up, the model is memorizing noise (Overfitting).
        </p>
    </div>
    """, unsafe_allow_html=True)

# Layout
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("### 🎛️ Controls")
    
    capacity = st.slider(
        "🧠 Model Capacity",
        min_value=1, max_value=10, value=7,
        help="1 = Very Simple Model (Underfits)\n10 = Very Complex Model (Overfits easily)"
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
        min_value=1, max_value=100, value=60,
        help="Drag to step through time and watch the curves evolve."
    )
    
    # Generate data
    x, train_loss, val_loss = generate_curve_data(capacity, epochs=100)
    
    # Find min val loss for analysis
    min_val_idx = np.argmin(val_loss)
    min_val_epoch = x[min_val_idx]
    
    # Current values
    curr_train = train_loss[current_epoch - 1]
    curr_val = val_loss[current_epoch - 1]
    gap = curr_val - curr_train
    
    st.markdown("### 📊 Current Metrics")
    
    metric_html = f"""
    <div style="background: white; padding: 15px; border-radius: 12px; border: 1px solid #E2E8F0; margin-bottom: 15px;">
        <div class="metric-label" style="color: #3b82f6;">Training Loss</div>
        <div class="metric-value" style="color: #1E293B;">{curr_train:.3f}</div>
    </div>
    <div style="background: white; padding: 15px; border-radius: 12px; border: 1px solid #E2E8F0; margin-bottom: 15px;">
        <div class="metric-label" style="color: #ef4444;">Validation Loss</div>
        <div class="metric-value" style="color: #1E293B;">{curr_val:.3f}</div>
    </div>
    <div style="background: white; padding: 15px; border-radius: 12px; border: 1px solid #E2E8F0; margin-bottom: 15px;">
        <div class="metric-label" style="color: #8B5CF6;">The Gap (Generalization Error)</div>
        <div class="metric-value" style="color: #8B5CF6;">{gap:.3f}</div>
    </div>
    """
    st.markdown(metric_html, unsafe_allow_html=True)

with col2:
    # Determine Status
    if capacity <= 3 and current_epoch > 20:
        status = "underfit"
        status_msg = "📉 Underfitting: Both losses are high. The model is too simple to learn the patterns."
    elif current_epoch < min_val_epoch - 5:
        status = "learning"
        status_msg = "🔄 Learning... Both losses are decreasing nicely."
    elif abs(current_epoch - min_val_epoch) <= 5:
        status = "sweetspot"
        status_msg = "🎯 Sweet Spot! Validation loss is at its lowest. Best time to stop training!"
    elif current_epoch > min_val_epoch + 5 and gap > 0.2:
        status = "overfit"
        status_msg = "🚨 OVERFITTING DETECTED! Training loss drops, but validation loss goes up. The gap is widening!"
    else:
        status = "learning"
        status_msg = "🔄 Training in progress..."

    st.markdown(f'<div class="status-box status-{status}">{status_msg}</div>', unsafe_allow_html=True)
    st.write("") # Spacer

    # Plotly Chart
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
    
    # Add vertical line for sweet spot if we passed it and we are overfitting
    if status == "overfit" or status == "sweetspot":
        fig.add_shape(
            type="line",
            x0=min_val_epoch, x1=min_val_epoch,
            y0=0, y1=4,
            line=dict(color="#166534", width=2, dash="dash"),
        )
        fig.add_annotation(
            x=min_val_epoch, y=3.5,
            text="Early Stopping Point",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#166534",
            arrowsize=1,
            arrowwidth=2,
            font=dict(color="#166534", size=12, family="Inter")
        )
    
    fig.update_layout(
        xaxis=dict(
            title="Epochs (Time)",
            range=[0, 105],
            gridcolor='rgba(0,0,0,0.05)',
            zeroline=False,
            title_font=dict(size=14, family="Inter")
        ),
        yaxis=dict(
            title="Loss (Error)",
            range=[0, 3.5],
            gridcolor='rgba(0,0,0,0.05)',
            zeroline=False,
            title_font=dict(size=14, family="Inter")
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="rgba(0,0,0,0.1)",
            borderwidth=1,
            font=dict(family="Inter", size=14)
        ),
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.markdown("""
### 🧠 Intuition Check
* **What is the "Gap"?** The area shaded in red between the two lines represents the generalization error. It shows how much worse the model performs on unseen data compared to the data it memorized.
* **Early Stopping:** Notice the dashed green line when you increase the epochs on a high-capacity model? That's the ideal moment to stop training. Any further, and the model starts memorizing noise!
* **Model Capacity:** Try setting the capacity to 2. Notice how neither loss ever gets very low? The model just isn't smart enough to learn the complex patterns in the data.
""")