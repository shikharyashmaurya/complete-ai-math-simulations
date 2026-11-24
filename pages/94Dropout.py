"""94 · Dropout — randomly silencing neurons to fight overfitting."""

import sys
from itertools import product
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.nav import safe_page_link  # noqa: E402

GRID_ROWS, GRID_COLS = 8, 12
N_TRAIN, N_VAL = 14, 200
HIDDEN = 48
STEPS = 1200
EVERY = 20
X_PLOT = np.linspace(-1.6, 1.6, 161)


def ensure_seed(key, default):
    if key not in st.session_state:
        st.session_state[key] = default
    return st.session_state[key]


def apply_dropout(h, mask, keep, train, inverted):
    """Output of a dropout layer; `keep` = 1 − p is the probability that a unit survives."""
    if train:
        return h * mask / keep if inverted else h * mask
    return h if inverted else h * keep


def target_fn(x):
    return np.sin(3.0 * x)


def make_data(seed, noise=0.3):
    rng = np.random.default_rng(seed)
    x = np.sort(rng.uniform(-1, 1, N_TRAIN))
    y = target_fn(x) + noise * rng.standard_normal(N_TRAIN)
    xv = rng.uniform(-1, 1, N_VAL)
    yv = target_fn(xv) + noise * rng.standard_normal(N_VAL)
    return x, y, xv, yv


def init_params(seed):
    rng = np.random.default_rng(seed)
    return [rng.standard_normal((1, HIDDEN)) * np.sqrt(2.0), np.zeros(HIDDEN),
            rng.standard_normal((HIDDEN, HIDDEN)) * np.sqrt(2.0 / HIDDEN), np.zeros(HIDDEN),
            rng.standard_normal((HIDDEN, 1)) * np.sqrt(1.0 / HIDDEN), np.zeros(1)]


def forward(params, x, keep=1.0, rng=None):
    """1 → 48 → 48 → 1 ReLU MLP with inverted dropout after each hidden layer (only if `rng` is given)."""
    w1, b1, w2, b2, w3, b3 = params
    x = x.reshape(-1, 1)
    z1 = x @ w1 + b1
    h1 = np.maximum(z1, 0.0)
    m1 = (rng.random(h1.shape) < keep) / keep if rng is not None else np.ones_like(h1)
    a1 = h1 * m1
    z2 = a1 @ w2 + b2
    h2 = np.maximum(z2, 0.0)
    m2 = (rng.random(h2.shape) < keep) / keep if rng is not None else np.ones_like(h2)
    a2 = h2 * m2
    return (a2 @ w3 + b3)[:, 0], (x, z1, m1, a1, z2, m2, a2)


@st.cache_data(show_spinner=False, max_entries=32)
def train(seed, p):
    """Full-batch training with Adam on the MSE; returns curves (eval-mode losses) and final parameters."""
    x, y, xv, yv = make_data(seed)
    params = init_params(seed + 7)
    m_state = [np.zeros_like(a) for a in params]
    v_state = [np.zeros_like(a) for a in params]
    rng = np.random.default_rng(seed + 99)
    keep = 1.0 - p
    lr, b1c, b2c = 0.01, 0.9, 0.999
    n = len(y)
    steps, tr_curve, va_curve = [], [], []
    for t in range(1, STEPS + 1):
        out, (xx, z1, m1, a1, z2, m2, a2) = forward(params, x, keep, rng if p > 0 else None)
        d = (2.0 * (out - y) / n)[:, None]
        w2, w3 = params[2], params[4]
        dz2 = (d @ w3.T) * m2 * (z2 > 0)
        dz1 = (dz2 @ w2.T) * m1 * (z1 > 0)
        grads = [xx.T @ dz1, dz1.sum(0), a1.T @ dz2, dz2.sum(0), a2.T @ d, d.sum(0)]
        for i, g in enumerate(grads):
            m_state[i] = b1c * m_state[i] + (1 - b1c) * g
            v_state[i] = b2c * v_state[i] + (1 - b2c) * g**2
            params[i] = params[i] - lr * (m_state[i] / (1 - b1c**t)) / (np.sqrt(v_state[i] / (1 - b2c**t)) + 1e-8)
        if t % EVERY == 0:
            steps.append(t)
            tr_curve.append(float(np.mean((forward(params, x)[0] - y) ** 2)))
            va_curve.append(float(np.mean((forward(params, xv)[0] - yv) ** 2)))
    return np.array(steps), np.array(tr_curve), np.array(va_curve), params


def intuition():
    st.title("🎲 Dropout")
    st.markdown("##### During training, randomly switch off neurons so that no neuron can rely on any other one.")
    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown(
            r"""
At every training step each hidden unit is **dropped** (set to 0) with probability $p$ and **kept** with
probability $1-p$. The network can never count on a particular partner neuron being present, so it learns
**redundant, robust features** instead of fragile co-adaptations that memorise the training set.

At test time we want a deterministic prediction, so dropout is switched **off** — and the activations must be
rescaled so their size matches what the next layer saw during training. Modern **inverted dropout** does the
rescaling during training: kept units are multiplied by $\frac{1}{1-p}$.
"""
        )
    with c2:
        with st.container(border=True):
            st.markdown("**Why it matters for AI**")
            st.markdown(
                "- One of the simplest and most widely used regularisers (AlexNet, BERT, the original Transformer).\n"
                "- Training with dropout ≈ training a huge ensemble of weight-sharing sub-networks.\n"
                "- Leaving it **on** at test time (MC dropout) gives a cheap uncertainty estimate."
            )


def mask_lab():
    st.header("1 · Lab: a dropout mask on a layer of activations")
    seed = ensure_seed("p94_mask_seed", 94)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        keep = st.slider("Keep probability 1 − p", 0.05, 1.0, 0.8, 0.05, key="p94_keep")
    with c2:
        mode = st.radio("Mode", ["Training (mask on)", "Evaluation (mask off)"], horizontal=True, key="p94_mode")
        inverted = st.checkbox("Inverted dropout (scale kept units by 1/(1 − p))", value=True, key="p94_inv")
    with c3:
        if st.button("🎲 Resample mask", key="p94_resample"):
            st.session_state["p94_mask_seed"] = int(np.random.default_rng(st.session_state["p94_mask_seed"]).integers(0, 10**6))
            seed = st.session_state["p94_mask_seed"]
    train_mode = mode.startswith("Training")
    p = 1.0 - keep
    h = np.random.default_rng(2024).gamma(2.0, 0.5, (GRID_ROWS, GRID_COLS))
    mask = (np.random.default_rng(seed).random(h.shape) < keep).astype(float)
    shown_mask = mask if train_mode else np.ones_like(mask)
    out = apply_dropout(h, mask, keep, train_mode, inverted)

    zmax = float(max(h.max(), out.max()))
    fig = make_subplots(rows=1, cols=3, subplot_titles=("activations h", "mask m (1 = keep)", "output of the dropout layer"),
                        horizontal_spacing=0.04)
    fig.add_trace(go.Heatmap(z=h, zmin=0, zmax=zmax, colorscale="Viridis", showscale=False), row=1, col=1)
    fig.add_trace(go.Heatmap(z=shown_mask, zmin=0, zmax=1, colorscale=[[0, "#111827"], [1, "#F9FAFB"]],
                             showscale=False, xgap=1, ygap=1), row=1, col=2)
    fig.add_trace(go.Heatmap(z=out, zmin=0, zmax=zmax, colorscale="Viridis", colorbar=dict(len=0.9)), row=1, col=3)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False, autorange="reversed")
    fig.update_layout(template="plotly_dark", height=300, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, width="stretch")

    n_units = h.size
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("units kept", f"{int(shown_mask.sum())} / {n_units}", f"expected {keep * n_units:.1f}" if train_mode else None,
              delta_color="off")
    m2.metric("drop probability p", f"{p:.2f}")
    m3.metric("mean of h", f"{h.mean():.4f}")
    m4.metric("mean of output", f"{out.mean():.4f}")
    if train_mode and not inverted:
        st.warning(f"Without the 1/(1 − p) scaling the training output is on average only {keep:.2f}× as large as h. "
                   "Classic dropout fixed this by multiplying by (1 − p) at test time instead.")
    if not train_mode:
        st.info("Evaluation mode: every unit is kept. Inverted dropout needs no change at test time (identity); "
                "the classic version multiplies by 1 − p instead. In PyTorch this is `model.eval()`.")
    return h, keep, inverted, seed


def expectation_check(h, keep, inverted, seed):
    st.subheader("Does the rescaling really keep the expected activation?")
    n_masks = st.slider("number of random masks to average", 10, 5000, 2000, 10, key="p94_nmasks")
    rng = np.random.default_rng(seed + 1)
    masks = rng.random((n_masks, *h.shape)) < keep
    avg_inv = (masks * h).mean(axis=0) / keep
    avg_raw = (masks * h).mean(axis=0)
    avg = avg_inv if inverted else avg_raw
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=h.ravel(), y=avg_inv.ravel(), mode="markers", name="inverted: mean of m·h/(1−p)",
                             marker=dict(color="#34D399", size=7)))
    fig.add_trace(go.Scatter(x=h.ravel(), y=avg_raw.ravel(), mode="markers", name="no scaling: mean of m·h",
                             marker=dict(color="#F87171", size=7, symbol="x")))
    line = np.array([0, h.max()])
    fig.add_trace(go.Scatter(x=line, y=line, mode="lines", name="y = h", line=dict(color="white", dash="dash")))
    fig.add_trace(go.Scatter(x=line, y=keep * line, mode="lines", name="y = (1 − p)·h", line=dict(color="#F87171", dash="dot")))
    fig.update_layout(template="plotly_dark", height=360, xaxis_title="original activation h",
                      yaxis_title="average over masks", margin=dict(l=10, r=10, t=20, b=10))
    c1, c2 = st.columns([3, 2])
    c1.plotly_chart(fig, width="stretch")
    with c2:
        u = h[0, 0]
        var_one = u**2 * (1 - keep) / keep
        emp = masks[:, 0, 0] * u / keep
        st.latex(r"\mathbb{E}\!\left[\tfrac{m}{1-p}\,h\right]=\tfrac{(1-p)\,h}{1-p}=h,\qquad"
                 r"\mathrm{Var}\!\left[\tfrac{m}{1-p}\,h\right]=h^2\,\tfrac{p}{1-p}")
        st.latex(rf"h_{{1,1}}={u:.4f}:\;\; \text{{mean}}={emp.mean():.4f},\;\; "
                 rf"\text{{var}}={emp.var():.4f}\;\text{{vs}}\;{var_one:.4f}")
        err = np.abs(avg - h).max()
        expected_se = h.max() * np.sqrt((1 - keep) / keep / n_masks)
        st.metric("max |average − h| over the 96 units" + ("" if inverted else " (no scaling)"), f"{err:.4f}")
        st.caption(f"Monte-Carlo noise of an average of {n_masks} masks is about h·√(p/((1−p)·T)) ≤ {expected_se:.4f}; "
                   "more masks ⇒ the green points hug y = h. Without scaling they sit on y = (1 − p)·h.")


def ensemble_lab(keep):
    st.header("2 · Dropout as an ensemble of 2ⁿ sub-networks")
    n_grid = GRID_ROWS * GRID_COLS
    st.markdown(
        rf"Each mask selects a **sub-network** that shares weights with all others. A layer with $n$ droppable units has "
        rf"$2^n$ of them — for the 96-unit grid above that is $2^{{96}}\approx {2.0**n_grid:.2e}$. Each training step "
        r"trains one random sub-network; evaluation mode with rescaled weights approximates the **average** of all of them."
    )
    rng = np.random.default_rng(7)
    x = rng.gamma(2.0, 0.5, 10)
    w_lin = rng.standard_normal(10)
    w_hid = rng.standard_normal((10, 8)) / np.sqrt(10)
    w_out = rng.standard_normal(8)
    masks = np.array(list(product([0.0, 1.0], repeat=10)))
    probs = keep ** masks.sum(1) * (1 - keep) ** (10 - masks.sum(1))
    dropped = masks * x / keep
    lin_ens = float(probs @ (dropped @ w_lin))
    lin_eval = float(x @ w_lin)
    relu_ens = float(probs @ (np.maximum(dropped @ w_hid, 0.0) @ w_out))
    relu_eval = float(np.maximum(x @ w_hid, 0.0) @ w_out)
    st.markdown(
        r"Exact check with **all $2^{10}=1024$ masks** on a 10-input toy (inverted dropout on the inputs, weighted by "
        r"$P(m)=(1-p)^{|m|}\,p^{\,10-|m|}$):"
    )
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown(r"**Linear model** $y=w\cdot\tilde x$")
            a, b = st.columns(2)
            a.metric("ensemble average Σ P(m)·y(m)", f"{lin_ens:.6f}")
            b.metric("evaluation mode y(x)", f"{lin_eval:.6f}")
            st.caption("Identical (up to rounding): the expectation passes straight through a linear map.")
    with c2:
        with st.container(border=True):
            st.markdown(r"**With a ReLU hidden layer** $y=v\cdot\mathrm{ReLU}(W\tilde x)$")
            a, b = st.columns(2)
            a.metric("ensemble average", f"{relu_ens:.6f}")
            b.metric("evaluation mode", f"{relu_eval:.6f}", f"{relu_eval - relu_ens:+.4f}", delta_color="off")
            st.caption("No longer equal: for non-linear nets evaluation mode is only an approximation of the ensemble "
                       "(the 'weight-scaling inference rule'). It is exact when p = 0.")


def overfit_lab():
    st.header("3 · Lab: does dropout reduce overfitting?")
    st.markdown(
        rf"{N_TRAIN} noisy training points from $y=\sin(3x)+\varepsilon$, $\varepsilon\sim\mathcal N(0,0.3^2)$, and "
        rf"{N_VAL} validation points. A 1 → {HIDDEN} → {HIDDEN} → 1 ReLU MLP is trained for {STEPS} full-batch Adam steps "
        "twice: without dropout and with dropout after both hidden layers. Losses are measured in evaluation mode."
    )
    seed = ensure_seed("p94_data_seed", 1)
    c1, c2 = st.columns([1, 3])
    with c1:
        p = st.slider("dropout probability p (2nd run)", 0.1, 0.7, 0.3, 0.05, key="p94_p_train")
        if st.button("🎲 Resample data & init", key="p94_data_resample"):
            st.session_state["p94_data_seed"] = int(np.random.default_rng(st.session_state["p94_data_seed"]).integers(0, 10**6))
            seed = st.session_state["p94_data_seed"]
    steps, tr0, va0, params0 = train(seed, 0.0)
    _, tr1, va1, params1 = train(seed, round(p, 2))
    x, y, xv, yv = make_data(seed)
    with c1:
        st.metric("final val MSE, no dropout", f"{va0[-1]:.3f}", f"train {tr0[-1]:.3f}", delta_color="off")
        st.metric(f"final val MSE, dropout p={p:.2f}", f"{va1[-1]:.3f}", f"train {tr1[-1]:.3f}", delta_color="off")
        st.caption("Noise floor: the best possible val MSE is ≈ 0.3² = 0.09.")
    fig = make_subplots(rows=1, cols=2, subplot_titles=("MSE during training (log scale)", "fitted functions"))
    for curve, name, color, dash in ((tr0, "train · no dropout", "#F87171", "dot"), (va0, "val · no dropout", "#F87171", "solid"),
                                     (tr1, f"train · p={p:.2f}", "#34D399", "dot"), (va1, f"val · p={p:.2f}", "#34D399", "solid")):
        fig.add_trace(go.Scatter(x=steps, y=np.maximum(curve, 1e-8), mode="lines", name=name,
                                 line=dict(color=color, dash=dash)), row=1, col=1)
    fig.add_trace(go.Scatter(x=X_PLOT, y=target_fn(X_PLOT), mode="lines", name="true sin(3x)",
                             line=dict(color="white", dash="dash")), row=1, col=2)
    fig.add_trace(go.Scatter(x=X_PLOT, y=forward(params0, X_PLOT)[0], mode="lines", name="fit · no dropout",
                             line=dict(color="#F87171")), row=1, col=2)
    fig.add_trace(go.Scatter(x=X_PLOT, y=forward(params1, X_PLOT)[0], mode="lines", name=f"fit · p={p:.2f}",
                             line=dict(color="#34D399")), row=1, col=2)
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", name="training points", marker=dict(color="#FBBF24", size=9)),
                  row=1, col=2)
    fig.update_yaxes(type="log", row=1, col=1)
    fig.update_yaxes(range=[-2.5, 2.5], row=1, col=2)
    fig.update_xaxes(title_text="step", row=1, col=1)
    fig.update_xaxes(title_text="x", row=1, col=2)
    fig.update_layout(template="plotly_dark", height=420, margin=dict(l=10, r=10, t=40, b=10))
    with c2:
        st.plotly_chart(fig, width="stretch")
    st.caption("Typical picture: without dropout the training loss goes to ≈0 while validation loss climbs (memorised noise). "
               "Dropout keeps training loss higher and the fit smoother. With only 14 points results vary by seed — resample "
               "a few times; dropout is a regulariser, not a guarantee, and too large p underfits.")
    return seed, round(p, 2), params1


def mc_dropout_lab(seed, p, params):
    st.header("4 · MC dropout: uncertainty from stochastic forward passes")
    st.markdown(
        rf"Keep dropout **on** at prediction time (here $p={p:.2f}$, the trained dropout net above) and run $T$ forward "
        r"passes. The mean is the prediction; the spread is a rough uncertainty estimate (Gal & Ghahramani, 2016)."
    )
    t_passes = st.slider("number of stochastic passes T", 5, 300, 100, 5, key="p94_T")
    rng = np.random.default_rng(seed + 500)
    preds = np.array([forward(params, X_PLOT, 1.0 - p, rng)[0] for _ in range(t_passes)])
    mean, std = preds.mean(0), preds.std(0)
    x, y, _, _ = make_data(seed)
    fig = go.Figure()
    for k in range(min(15, t_passes)):
        fig.add_trace(go.Scatter(x=X_PLOT, y=preds[k], mode="lines", line=dict(color="rgba(167,139,250,0.25)", width=1),
                                 showlegend=k == 0, name="individual passes"))
    fig.add_trace(go.Scatter(x=np.r_[X_PLOT, X_PLOT[::-1]], y=np.r_[mean + 2 * std, (mean - 2 * std)[::-1]], fill="toself",
                             fillcolor="rgba(96,165,250,0.25)", line=dict(width=0), name="mean ± 2 std"))
    fig.add_trace(go.Scatter(x=X_PLOT, y=mean, mode="lines", name="MC mean", line=dict(color="#60A5FA", width=3)))
    fig.add_trace(go.Scatter(x=X_PLOT, y=forward(params, X_PLOT)[0], mode="lines", name="evaluation mode",
                             line=dict(color="#34D399", dash="dash")))
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", name="training points", marker=dict(color="#FBBF24", size=9)))
    fig.add_vrect(x0=-1.6, x1=-1.0, fillcolor="gray", opacity=0.12, line_width=0)
    fig.add_vrect(x0=1.0, x1=1.6, fillcolor="gray", opacity=0.12, line_width=0)
    fig.update_layout(template="plotly_dark", height=400, xaxis_title="x (shaded: outside the training range)",
                      yaxis=dict(range=[-3, 3]), margin=dict(l=10, r=10, t=20, b=10))
    st.plotly_chart(fig, width="stretch")
    inside = np.abs(X_PLOT) <= 1.0
    a, b = st.columns(2)
    a.metric("average std inside the data range [−1, 1]", f"{std[inside].mean():.3f}")
    b.metric("average std outside (extrapolation)", f"{std[~inside].mean():.3f}")
    st.caption("The spread usually grows where there is no data, but MC dropout is only an approximation: it can be "
               "over- or under-confident and depends strongly on p. Calibrate before trusting it.")


def worked_example(keep):
    st.header("5 · Worked example")
    p = 1.0 - keep
    n = GRID_ROWS * GRID_COLS
    st.markdown("For one unit with activation $h=2$ and the keep probability chosen in Lab 1:")
    st.latex(rf"p={p:.2f},\;1-p={keep:.2f}:\quad \tilde h=\begin{{cases}}\dfrac{{2}}{{{keep:.2f}}}={2 / keep:.4f} & \text{{prob. }}{keep:.2f}"
             rf"\\[4pt] 0 & \text{{prob. }}{p:.2f}\end{{cases}}")
    st.latex(rf"\mathbb{{E}}[\tilde h]={keep:.2f}\cdot{2 / keep:.4f}+{p:.2f}\cdot 0={keep * (2 / keep):.4f}=h,\qquad"
             rf"\mathrm{{Var}}[\tilde h]=2^2\cdot\frac{{{p:.2f}}}{{{keep:.2f}}}={4 * p / keep:.4f}")
    st.latex(rf"\text{{kept units in a {n}-unit layer}}\sim\mathrm{{Binomial}}({n},{keep:.2f}):\;"
             rf"\text{{mean}}={n * keep:.1f},\;\text{{std}}=\sqrt{{{n}\cdot{keep:.2f}\cdot{p:.2f}}}={np.sqrt(n * keep * p):.2f}")


def ai_connection():
    st.header("6 · AI connection")
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.markdown("**Dropout in transformers**")
            st.markdown(
                "The original Transformer used p = 0.1 on each sub-layer output before it is added to the residual stream "
                "(**residual dropout**) and on the embeddings. BERT/GPT-2-style code also applies **attention dropout** to "
                "the softmax attention weights, randomly cutting query→key links."
            )
    with c2:
        with st.container(border=True):
            st.markdown("**Variants**")
            st.markdown(
                "**DropConnect** drops individual *weights* instead of activations. **Stochastic depth / DropPath** drops "
                "whole residual blocks (common in vision transformers). `nn.Dropout` in PyTorch is inverted dropout and "
                "is disabled by `model.eval()`."
            )
    with c3:
        with st.container(border=True):
            st.markdown("**Why big LLMs use little dropout**")
            st.markdown(
                "Pre-training sees each token roughly once on trillions of tokens, so there is little to overfit, and the "
                "noise slows learning. PaLM reports pre-training without dropout and LLaMA-style models set it to 0; "
                "dropout returns when fine-tuning on small datasets."
            )


def takeaways():
    st.header("Key takeaways")
    st.success(
        "1. Training: keep each unit with probability 1 − p; inverted dropout divides kept units by 1 − p so E[h̃] = h.\n"
        "2. Evaluation: dropout is off (identity) — remember `model.eval()`.\n"
        "3. It trains an implicit ensemble of 2ⁿ weight-sharing sub-networks; eval mode approximates their average.\n"
        "4. It reduces overfitting on small data; MC dropout (leaving it on) gives a rough uncertainty estimate."
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        safe_page_link("pages/93Weight Initialization.py", "← Previous: Weight Initialization")
    with c2:
        safe_page_link("pages/71Overfitting Underfitting.py", "Revisit: Overfitting & Underfitting")
    with c3:
        safe_page_link("pages/95Batch Normalization.py", "Next: Batch Normalization →")


def main():
    st.set_page_config(page_title="NN · Dropout", page_icon="🎲", layout="wide")
    intuition()
    h, keep, inverted, seed = mask_lab()
    expectation_check(h, keep, inverted, seed)
    ensemble_lab(keep)
    seed_d, p, params = overfit_lab()
    mc_dropout_lab(seed_d, p, params)
    worked_example(keep)
    ai_connection()
    takeaways()


main()
