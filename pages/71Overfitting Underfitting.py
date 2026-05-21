import streamlit as st
import numpy as np
import plotly.graph_objects as go
import warnings

st.set_page_config(page_title="Overfitting & Underfitting", layout="wide", initial_sidebar_state="expanded")

st.title("🎭 Overfitting & Underfitting")
st.markdown("### The Goldilocks Problem of Machine Learning")
st.markdown("Imagine teaching a student for an exam. **Underfitting** is like the student only reading the chapter titles—they learn too little to pass. **Overfitting** is like the student memorizing the exact practice questions word-for-word—they ace the practice but fail the real exam because they didn't learn the *underlying concepts*.")

st.markdown("---")

st.sidebar.header("🎛️ Model Controls")
st.sidebar.markdown("Adjust the complexity of your model to see how it fits the data.")

# Slider for polynomial degree
degree = st.sidebar.slider("Polynomial Degree (Complexity)", min_value=1, max_value=20, value=1, step=1,
                           help="Low degree = Simple model. High degree = Complex model.")
noise_level = st.sidebar.slider("Noise Level", 0.0, 1.0, 0.3, 0.1, help="How messy is the real world data?")

# Generate Data
def true_function(x):
    return np.cos(1.5 * np.pi * x)

# Fixed seed so the points don't jump around when changing degree
np.random.seed(42)
n_samples = 30

# Training data
X_train = np.sort(np.random.rand(n_samples))
y_train = true_function(X_train) + np.random.randn(n_samples) * noise_level

# Test data (New points from the same underlying distribution)
np.random.seed(100) # Different seed for test set
X_test = np.sort(np.random.rand(n_samples))
y_test = true_function(X_test) + np.random.randn(n_samples) * noise_level

# Model Fitting
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    coeffs = np.polyfit(X_train, y_train, degree)
    poly = np.poly1d(coeffs)

# Generate smooth points for plotting curves
X_plot = np.linspace(0, 1, 200)
y_plot_true = true_function(X_plot)
y_plot_pred = poly(X_plot)

# Calculate Errors
train_pred = poly(X_train)
test_pred = poly(X_test)
train_mse = np.mean((y_train - train_pred)**2)
test_mse = np.mean((y_test - test_pred)**2)

# Determine state
if degree < 3:
    state = "Underfitting 🧊"
    state_color = "#3498db"
    desc = "The model is **too simple**. It can't capture the underlying pattern of the data. Both training and test errors are high."
elif 3 <= degree <= 5:
    state = "Good Fit 🎯"
    state_color = "#2ecc71"
    desc = "The model has learned the **true pattern** without memorizing the noise. This is the sweet spot! Low training and test errors."
else:
    state = "Overfitting 🔥"
    state_color = "#e74c3c"
    desc = "The model is **too complex**. It's contorting itself to hit every single training point, including the random noise. The training error is tiny, but it fails completely on new data!"

# Display Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div style='background-color: {state_color}20; padding: 20px; border-radius: 10px; border-left: 5px solid {state_color}; height: 100%;'>"
                f"<h3 style='color: {state_color}; margin: 0;'>{state}</h3>"
                f"<p style='margin-top: 10px;'>{desc}</p></div>", unsafe_allow_html=True)
with col2:
    st.metric("Training Error (MSE)", f"{train_mse:.4f}", delta="Memorizing well" if degree > 5 else None, delta_color="inverse")
with col3:
    st.metric("Test Error (MSE)", f"{test_mse:.4f}", delta="Failing on new data!" if test_mse > 1.0 else None, delta_color="inverse")

st.markdown("<br>", unsafe_allow_html=True)

# Plotly Graph for Visualization
fig = go.Figure()

# True function
fig.add_trace(go.Scatter(x=X_plot, y=y_plot_true, mode='lines', name='True Pattern (Hidden)', line=dict(color='rgba(255, 255, 255, 0.4)', width=4, dash='dash')))

# Model prediction
fig.add_trace(go.Scatter(x=X_plot, y=y_plot_pred, mode='lines', name=f'Fitted Model (Degree {degree})', line=dict(color=state_color, width=5)))

# Training Data
fig.add_trace(go.Scatter(x=X_train, y=y_train, mode='markers', name='Training Data', marker=dict(color='white', size=12, line=dict(color='#2c3e50', width=2))))

# Test Data
fig.add_trace(go.Scatter(x=X_test, y=y_test, mode='markers', name='New Data (Test)', marker=dict(color='#f39c12', size=10, symbol='star', line=dict(color='#2c3e50', width=1))))

fig.update_layout(
    title="Model Prediction vs Ground Truth",
    xaxis_title="Input (x)",
    yaxis_title="Output (y)",
    yaxis=dict(range=[-2.5, 2.5]), # Fix y-axis so wild overfitting is obvious
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    template="plotly_dark",
    margin=dict(l=0, r=0, t=50, b=0),
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("🧠 What's going on mathematically?")
st.markdown("""
When you increase the **polynomial degree**, you give the model more "wiggle room" (more parameters). 
- **Degree 1 (Line):** $y = w_1x + b$. Only one wiggle. Too rigid (**Underfitting**).
- **Degree 3-5 (Curve):** $y = w_3x^3 + ... + b$. Enough wiggles to gracefully fit the true curve. (**Good Fit**).
- **Degree 15+ (Spaghetti):** $y = w_{15}x^{15} + ... + b$. Way too many wiggles! The model contorts itself into insane shapes just to perfectly hit every single training point, including the random noise.

When the model is perfectly hitting the training points but going crazy in between, that's **Overfitting**. The Test Error explodes because the new data points don't follow the noise!
""")

st.markdown("---")
st.subheader("📊 The Complexity Trade-off Curve")
st.markdown("Look at how the errors change as you give the model more power. The training error always goes down, but the test error eventually shoots up! This U-shape is a classic concept in Machine Learning.")

# Precompute errors for degrees 1 to 20
degrees = np.arange(1, 21)
train_errors_list = []
test_errors_list = []

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    for d in degrees:
        c = np.polyfit(X_train, y_train, d)
        p = np.poly1d(c)
        train_errors_list.append(np.mean((y_train - p(X_train))**2))
        test_errors_list.append(np.mean((y_test - p(X_test))**2))

fig_err = go.Figure()
fig_err.add_trace(go.Scatter(x=degrees, y=train_errors_list, mode='lines+markers', name='Training Error', line=dict(color='white', width=3)))
fig_err.add_trace(go.Scatter(x=degrees, y=test_errors_list, mode='lines+markers', name='Test Error', line=dict(color='#f39c12', width=3)))

# Add a vertical line for current degree
fig_err.add_vline(x=degree, line_width=3, line_dash="dash", line_color=state_color, annotation_text=f"Current: {degree}", annotation_position="top right")

# Cap y-axis for better visibility of the "sweet spot"
max_y = max(test_errors_list[0:7]) * 1.5 
fig_err.update_layout(
    xaxis_title="Polynomial Degree (Model Complexity)",
    yaxis_title="Mean Squared Error (MSE)",
    yaxis=dict(range=[0, min(10, max_y)]),
    template="plotly_dark",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=0, r=0, t=50, b=0),
    hovermode="x unified"
)
st.plotly_chart(fig_err, use_container_width=True)