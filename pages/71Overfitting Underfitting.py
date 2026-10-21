import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Overfitting & Underfitting", layout="wide", initial_sidebar_state="expanded")

st.title("🎭 Overfitting & Underfitting")
st.markdown("### The Goldilocks Problem of Machine Learning")
st.markdown("Imagine teaching a student for an exam. **Underfitting** is like reading only chapter titles; **overfitting** is like memorizing practice questions. These are useful analogies for patterns in training and held-out performance, not guarantees based on model size alone.")

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

# Fixed local generators so the points stay repeatable without changing NumPy's global RNG.
rng_train = np.random.default_rng(42)
rng_val = np.random.default_rng(100)
n_samples = 30

# Training data
X_train = np.sort(rng_train.random(n_samples))
y_train = true_function(X_train) + rng_train.normal(0, noise_level, n_samples)

# Validation data (used to compare model complexities; reserve a separate test set for final evaluation)
X_val = np.sort(rng_val.random(n_samples))
y_val = true_function(X_val) + rng_val.normal(0, noise_level, n_samples)

# Model Fitting
poly = np.polynomial.Polynomial.fit(X_train, y_train, degree)

# Generate smooth points for plotting curves
X_plot = np.linspace(0, 1, 200)
y_plot_true = true_function(X_plot)
y_plot_pred = poly(X_plot)

# Calculate Errors
train_pred = poly(X_train)
val_pred = poly(X_val)
train_mse = np.mean((y_train - train_pred)**2)
val_mse = np.mean((y_val - val_pred)**2)

# Determine state
if degree < 3:
    state = "Lower Complexity"
    state_color = "#3498db"
    desc = "This low-degree model may be too simple to capture the pattern; compare its training and validation errors for this noise setting."
elif 3 <= degree <= 5:
    state = "Moderate Complexity"
    state_color = "#2ecc71"
    desc = "Degrees 3–5 often work well for this seeded toy dataset, but the best fit depends on the sample and noise. Compare the measured errors."
else:
    state = "Higher Complexity"
    state_color = "#e74c3c"
    desc = "Higher degrees can fit noise and generalize worse, but this is a tendency rather than a guarantee. Compare training and validation errors."

# Display Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div style='background-color: {state_color}20; padding: 20px; border-radius: 10px; border-left: 5px solid {state_color}; height: 100%;'>"
                f"<h3 style='color: {state_color}; margin: 0;'>{state}</h3>"
                f"<p style='margin-top: 10px;'>{desc}</p></div>", unsafe_allow_html=True)
with col2:
    st.metric("Training Error (MSE)", f"{train_mse:.4f}", delta="Higher degree" if degree > 5 else None, delta_color="off")
with col3:
    st.metric("Validation Error (MSE)", f"{val_mse:.4f}", delta="Above 1.0" if val_mse > 1.0 else None, delta_color="off")

st.markdown("<br>", unsafe_allow_html=True)

# Plotly Graph for Visualization
fig = go.Figure()

# True function
fig.add_trace(go.Scatter(x=X_plot, y=y_plot_true, mode='lines', name='True Pattern (Hidden)', line=dict(color='rgba(255, 255, 255, 0.4)', width=4, dash='dash')))

# Model prediction
fig.add_trace(go.Scatter(x=X_plot, y=y_plot_pred, mode='lines', name=f'Fitted Model (Degree {degree})', line=dict(color=state_color, width=5)))

# Training Data
fig.add_trace(go.Scatter(x=X_train, y=y_train, mode='markers', name='Training Data', marker=dict(color='white', size=12, line=dict(color='#2c3e50', width=2))))

# Validation Data
fig.add_trace(go.Scatter(x=X_val, y=y_val, mode='markers', name='Validation Data', marker=dict(color='#f39c12', size=10, symbol='star', line=dict(color='#2c3e50', width=1))))

fig.update_layout(
    title="Model Prediction vs Ground Truth",
    xaxis_title="Input (x)",
    yaxis_title="Output (y)",
    yaxis=dict(range=[min(float(np.min(y_train)), float(np.min(y_val)), float(np.min(y_plot_pred))) - 0.5, max(float(np.max(y_train)), float(np.max(y_val)), float(np.max(y_plot_pred))) + 0.5]),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    template="plotly_dark",
    margin=dict(l=0, r=0, t=50, b=0),
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("🧠 What's going on mathematically?")
st.markdown("""
When you increase the **polynomial degree**, you give the model more "wiggle room" (more parameters). In exact least-squares arithmetic, training error cannot increase for nested polynomial model classes; numerical fitting can affect the displayed estimates.
- **Degree 1 (Line):** $y = w_1x + b$. It may be too rigid for a curved pattern (**Underfitting**).
- **Degree 3-5 (Curve):** Often enough flexibility for this example, though the useful range changes with the data and noise.
- **Higher degrees:** More flexibility can produce unstable-looking curves and overfit, but degree alone does not guarantee perfect interpolation or poor held-out performance.

When a model fits training data much better than held-out data, that gap is evidence of **Overfitting**. A separate final test set is still needed for an unbiased final evaluation.
""")

st.markdown("---")
st.subheader("📊 The Complexity Trade-off Curve")
st.markdown("Look at how errors change as model complexity increases. Training error is non-increasing for nested least-squares polynomial models in exact arithmetic; validation error often—but not always—forms a U-shape.")

# Precompute errors for degrees 1 to 20
degrees = np.arange(1, 21)
train_errors_list = []
val_errors_list = []

for d in degrees:
    p = np.polynomial.Polynomial.fit(X_train, y_train, d)
    train_errors_list.append(np.mean((y_train - p(X_train))**2))
    val_errors_list.append(np.mean((y_val - p(X_val))**2))

fig_err = go.Figure()
fig_err.add_trace(go.Scatter(x=degrees, y=train_errors_list, mode='lines+markers', name='Training Error', line=dict(color='white', width=3)))
fig_err.add_trace(go.Scatter(x=degrees, y=val_errors_list, mode='lines+markers', name='Validation Error', line=dict(color='#f39c12', width=3)))

# Add a vertical line for current degree
fig_err.add_vline(x=degree, line_width=3, line_dash="dash", line_color=state_color, annotation_text=f"Current: {degree}", annotation_position="top right")

max_y = max(max(train_errors_list), max(val_errors_list), 0.1) * 1.1
fig_err.update_layout(
    xaxis_title="Polynomial Degree (Model Complexity)",
    yaxis_title="Mean Squared Error (MSE)",
    yaxis=dict(range=[0, max_y]),
    template="plotly_dark",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=0, r=0, t=50, b=0),
    hovermode="x unified"
)
st.plotly_chart(fig_err, use_container_width=True)