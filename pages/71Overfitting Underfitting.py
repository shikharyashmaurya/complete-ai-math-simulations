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

st.set_page_config(page_title="Overfitting & Underfitting", layout="wide", initial_sidebar_state="expanded")

st.title("🎭 Overfitting & Underfitting")
st.markdown("### The Goldilocks Problem of Machine Learning")
st.markdown("Imagine teaching a student for an exam. **Underfitting** is like reading only chapter titles; **overfitting** is like memorizing practice questions. These are useful analogies for patterns in training and held-out performance, not guarantees based on model size alone.")

st.markdown("---")

st.sidebar.header("🎛️ Model Controls")
st.sidebar.markdown("Adjust the complexity of your model to see how it fits the data.")

# Slider for polynomial degree
degree = st.sidebar.slider("Polynomial Degree (Complexity)", min_value=1, max_value=20, value=1, step=1, key="p71_degree",
                           help="Low degree = Simple model. High degree = Complex model.")
noise_level = st.sidebar.slider("Noise Level", 0.0, 1.0, 0.3, 0.1, key="p71_noise", help="How messy is the real world data?")

# Generate Data
def true_function(x):
    return np.cos(1.5 * np.pi * x)

# Fixed local generators so the points stay repeatable without changing NumPy's global RNG.
rng_train = np.random.default_rng(42)
rng_val = np.random.default_rng(100)
rng_test = np.random.default_rng(7)
n_samples = 30

# Training data
X_train = np.sort(rng_train.random(n_samples))
y_train = true_function(X_train) + rng_train.normal(0, noise_level, n_samples)

# Validation data (used to compare model complexities, i.e. to pick the degree)
X_val = np.sort(rng_val.random(n_samples))
y_val = true_function(X_val) + rng_val.normal(0, noise_level, n_samples)

# Test data (never used for any choice; only for the final check of the chosen degree)
X_test = np.sort(rng_test.random(n_samples))
y_test = true_function(X_test) + rng_test.normal(0, noise_level, n_samples)

# Model Fitting (Polynomial.fit rescales x internally, which keeps high-degree fits well conditioned)
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

# Errors for every degree (also used to label the current model from the measured validation curve)
degrees = np.arange(1, 21)
train_errors_list = []
val_errors_list = []
fits = {}
for d in degrees:
    p = np.polynomial.Polynomial.fit(X_train, y_train, d)
    fits[int(d)] = p
    train_errors_list.append(np.mean((y_train - p(X_train))**2))
    val_errors_list.append(np.mean((y_val - p(X_val))**2))

best_degree = int(degrees[int(np.argmin(val_errors_list))])
best_val_mse = float(np.min(val_errors_list))
test_mse_best = float(np.mean((y_test - fits[best_degree](X_test))**2))
near_best = val_mse <= 1.1 * best_val_mse + 1e-3

# Determine state from the measured validation errors (not from fixed degree thresholds)
if near_best:
    state = "Near the Validation Sweet Spot"
    state_color = "#2ecc71"
    desc = (f"Validation error is within 10% of the best value found (degree {best_degree}, MSE {best_val_mse:.4f}) "
            "for this sample and noise level.")
elif degree < best_degree:
    state = "Lower Complexity (Underfitting Side)"
    state_color = "#3498db"
    desc = (f"Validation error is higher than at degree {best_degree}. This simpler model likely misses part of the pattern.")
else:
    state = "Higher Complexity (Overfitting Side)"
    state_color = "#e74c3c"
    desc = (f"Validation error is higher than at degree {best_degree}. The extra flexibility is likely fitting noise "
            "and wiggling between (and beyond) the training points.")

# Display Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div style='background-color: {state_color}20; padding: 20px; border-radius: 10px; border-left: 5px solid {state_color}; height: 100%;'>"
                f"<h3 style='color: {state_color}; margin: 0;'>{state}</h3>"
                f"<p style='margin-top: 10px;'>{desc}</p></div>", unsafe_allow_html=True)
with col2:
    st.metric("Training Error (MSE)", f"{train_mse:.4f}")
with col3:
    st.metric("Validation Error (MSE)", f"{val_mse:.4f}",
              help=f"With noise level σ = {noise_level:.1f}, even the true pattern has an expected MSE of σ² = {noise_level**2:.2f}.")

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

data_min = min(float(np.min(y_train)), float(np.min(y_val)))
data_max = max(float(np.max(y_train)), float(np.max(y_val)))
y_lo, y_hi = data_min - 1.0, data_max + 1.0
curve_clipped = bool(np.min(y_plot_pred) < y_lo or np.max(y_plot_pred) > y_hi)

fig.update_layout(
    title="Model Prediction vs Ground Truth",
    xaxis_title="Input (x)",
    yaxis_title="Output (y)",
    # Keep the axis on the data; a wild high-degree curve would otherwise squash every point flat.
    yaxis=dict(range=[y_lo, y_hi]),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    template="plotly_dark",
    margin=dict(l=0, r=0, t=50, b=0),
    hovermode="x unified"
)

st.plotly_chart(fig, width="stretch")
if curve_clipped:
    st.caption(f"⚠️ The fitted curve leaves the plotted range (it reaches {np.min(y_plot_pred):.1f} … {np.max(y_plot_pred):.1f}); "
               "the y-axis is kept on the data so the points stay readable. Such swings typically happen between "
               "training points and near the edges, where the model must extrapolate.")

st.markdown("---")
st.subheader("🧠 What's going on mathematically?")
st.markdown(f"""
When you increase the **polynomial degree**, you give the model more "wiggle room" (more parameters). In exact least-squares arithmetic, training error cannot increase for nested polynomial model classes; numerical fitting can affect the displayed estimates.
- **Degree 1 (Line):** $y = w_1x + b$. It may be too rigid for a curved pattern (**Underfitting**).
- **Middle degrees:** For the current sample and noise level, the lowest validation error is at **degree {best_degree}**. The best degree changes with the data and noise.
- **Higher degrees:** More flexibility can produce unstable-looking curves and overfit, but degree alone does not guarantee perfect interpolation or poor held-out performance.

When a model fits training data much better than held-out data, that gap is evidence of **Overfitting**.
""")

st.markdown("---")
st.subheader("📊 The Complexity Trade-off Curve")
st.markdown("Look at how errors change as model complexity increases. Training error is non-increasing for nested least-squares polynomial models in exact arithmetic; validation error often—but not always—forms a U-shape. The y-axis is **logarithmic** so both small and huge errors stay visible.")

plot_floor = 1e-6  # log axis cannot show 0; tiny errors (e.g. with zero noise) are drawn at this floor
fig_err = go.Figure()
fig_err.add_trace(go.Scatter(x=degrees, y=np.maximum(train_errors_list, plot_floor), mode='lines+markers', name='Training Error', line=dict(color='white', width=3)))
fig_err.add_trace(go.Scatter(x=degrees, y=np.maximum(val_errors_list, plot_floor), mode='lines+markers', name='Validation Error', line=dict(color='#f39c12', width=3)))

# Add a vertical line for current degree
fig_err.add_vline(x=degree, line_width=3, line_dash="dash", line_color=state_color, annotation_text=f"Current: {degree}", annotation_position="top right")
fig_err.add_vline(x=best_degree, line_width=2, line_dash="dot", line_color="#2ecc71", annotation_text=f"Lowest validation: {best_degree}", annotation_position="bottom right")

fig_err.update_layout(
    xaxis_title="Polynomial Degree (Model Complexity)",
    yaxis_title="Mean Squared Error (MSE, log scale)",
    yaxis=dict(type="log"),
    template="plotly_dark",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=0, r=0, t=50, b=0),
    hovermode="x unified"
)
st.plotly_chart(fig_err, width="stretch")

st.markdown("---")
st.subheader("🧪 Final Check on a Separate Test Set")
st.markdown(f"""
We used the **validation** set to *choose* the degree (degree **{best_degree}**). Because it influenced that choice,
its error ({best_val_mse:.4f}) tends to be optimistic. A third, untouched **test** set gives a fair final estimate:
""")
tcol1, tcol2 = st.columns(2)
with tcol1:
    st.metric(f"Validation MSE (degree {best_degree}, used for selection)", f"{best_val_mse:.4f}")
with tcol2:
    st.metric(f"Test MSE (degree {best_degree}, never used for choices)", f"{test_mse_best:.4f}")
st.caption("The test set is only looked at once, after the degree has been chosen. "
           "If you kept tuning until the test error looked good, it would become a second validation set.")

st.markdown("**Next up:** how to split data into train / validation / test sets properly — and what goes wrong when you don't.")
safe_page_link("pages/72Train, Validation & Test Splits.py", "Next: 72 · Train, Validation & Test Splits", icon="➡️")