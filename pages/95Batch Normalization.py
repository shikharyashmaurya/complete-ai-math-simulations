"""95 · Batch Normalization — re-centre and re-scale every layer's inputs."""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.nav import safe_page_link  # noqa: E402

EPS_OPTIONS = [1e-8, 1e-5, 1e-3, 1e-1, 1.0]
BATCH_SIZES = [2, 4, 8, 16, 32, 64, 128, 256]
N_STEPS = 300


def ensure_seed():
    if "p95_seed" not in st.session_state:
        st.session_state["p95_seed"] = 95
    return st.session_state["p95_seed"]


def batch_norm(x, eps, axis=0):
    """Normalise with the batch (biased) mean and variance along `axis`."""
    mu = x.mean(axis=axis, keepdims=True)
    var = x.var(axis=axis, keepdims=True)
    return (x - mu) / np.sqrt(var + eps), mu, var


def rms_norm(x, eps, axis=-1):
    rms = np.sqrt(np.mean(x**2, axis=axis, keepdims=True) + eps)
    return x / rms, rms


def deep_scales(depth, gain, use_bn, seed, width=64, batch=64, eps=1e-5):
    """Std of the input to every ReLU in a bias-free MLP whose weights are He-init × gain."""
    rng = np.random.default_rng(seed)
    h = rng.standard_normal((batch, width))
    stds = []
    with np.errstate(over="ignore", invalid="ignore", under="ignore"):
        for _ in range(depth):
            z = h @ (gain * np.sqrt(2.0 / width) * rng.standard_normal((width, width)))
            if use_bn:
                z = batch_norm(z, eps)[0]
            stds.append(float(z.std()))
            h = np.maximum(z, 0.0)
    return np.array(stds)


def intuition():
    st.title("📏 Batch Normalization")
    st.markdown("##### Standardise each feature using the statistics of the current mini-batch, then let the network re-scale it.")
    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown(
            r"""
On the *Z-scores* page we standardised data once, before training. **Batch Normalization** (Ioffe & Szegedy, 2015)
does it **inside** the network, for every layer and every mini-batch: for each feature, subtract the batch mean and
divide by the batch standard deviation. Then two learnable numbers per feature, $\gamma$ (scale) and $\beta$ (shift),
give the network back the freedom to choose whatever mean and spread work best.

The result: activations stay at a sensible scale no matter how deep the network or how badly scaled the weights are,
which lets you train faster with larger learning rates.
"""
        )
    with c2:
        with st.container(border=True):
            st.markdown("**Why it matters for AI**")
            st.markdown(
                "- Made very deep CNNs (ResNet) practical to train.\n"
                "- Its cousins **LayerNorm** and **RMSNorm** sit in every transformer block.\n"
                "- It behaves differently in training and inference — a classic source of bugs."
            )


def batch_lab(seed):
    st.header("1 · Lab: normalise one feature over a batch")
    st.latex(r"\mu_B=\frac1B\sum_{i=1}^{B}x_i,\quad \sigma_B^2=\frac1B\sum_{i=1}^{B}(x_i-\mu_B)^2,\quad "
             r"\hat x_i=\frac{x_i-\mu_B}{\sqrt{\sigma_B^2+\varepsilon}},\quad y_i=\gamma\,\hat x_i+\beta")
    c1, c2, c3 = st.columns(3)
    with c1:
        shift = st.slider("incoming mean (shift)", -5.0, 5.0, 3.0, 0.5, key="p95_shift")
        scale = st.slider("incoming std (scale)", 0.1, 5.0, 2.0, 0.1, key="p95_scale")
    with c2:
        batch = st.slider("batch size B", 2, 256, 32, key="p95_batch")
        eps = st.selectbox("ε (numerical safety)", EPS_OPTIONS, index=1, key="p95_eps", format_func=lambda e: f"{e:g}")
    with c3:
        gamma = st.slider("γ (learnable scale)", -3.0, 3.0, 1.0, 0.1, key="p95_gamma")
        beta = st.slider("β (learnable shift)", -3.0, 3.0, 0.0, 0.1, key="p95_beta")
        undo = st.checkbox("Set γ = √(σ²_B+ε), β = μ_B (undo the normalisation)", key="p95_undo")
        if st.button("🎲 Resample batch", key="p95_resample"):
            st.session_state["p95_seed"] = int(np.random.default_rng(st.session_state["p95_seed"]).integers(0, 10**6))
            seed = st.session_state["p95_seed"]
    x = shift + scale * np.random.default_rng(seed).standard_normal(batch)
    x_hat, mu, var = batch_norm(x, eps)
    mu, var = float(mu[0]), float(var[0])
    if undo:
        gamma, beta = float(np.sqrt(var + eps)), mu
    y = gamma * x_hat + beta

    fig = make_subplots(rows=1, cols=3, subplot_titles=("incoming x", "normalised x̂", "output y = γx̂ + β"))
    for col, (vals, color) in enumerate(((x, "#F87171"), (x_hat, "#60A5FA"), (y, "#34D399")), start=1):
        fig.add_trace(go.Histogram(x=vals, nbinsx=30, marker_color=color, showlegend=False), row=1, col=col)
        fig.add_vline(x=float(vals.mean()), line=dict(color="white", dash="dash"), row=1, col=col)
    fig.update_layout(template="plotly_dark", height=300, margin=dict(l=10, r=10, t=40, b=10), bargap=0.05)
    st.plotly_chart(fig, width="stretch")
    m = st.columns(5)
    m[0].metric("μ_B", f"{mu:.4f}", f"true mean {shift:g}", delta_color="off")
    m[1].metric("σ_B", f"{np.sqrt(var):.4f}", f"true std {scale:g}", delta_color="off")
    m[2].metric("mean of x̂", f"{x_hat.mean():.2e}")
    m[3].metric("variance of x̂", f"{x_hat.var():.6f}", f"σ²_B/(σ²_B+ε) = {var / (var + eps):.6f}", delta_color="off")
    m[4].metric("mean / std of y", f"{y.mean():.3f} / {y.std():.3f}")
    if undo:
        st.success("With γ = √(σ²_B+ε) and β = μ_B the layer outputs exactly its input (max |y − x| = "
                   f"{np.abs(y - x).max():.1e}). So BN never *removes* representational power: the network can learn to undo it.")
    else:
        st.caption("x̂ always has mean 0 and variance σ²_B/(σ²_B+ε) ≈ 1 whatever shift/scale you choose; γ and β then set "
                   "the output mean to β and the std to |γ|·std(x̂). Try a tiny incoming std with ε = 1 to see ε matter.")
    return x, x_hat, y, mu, var, eps, gamma, beta, shift, scale, batch


def worked_example(x, x_hat, y, mu, var, eps, gamma, beta):
    st.header("2 · Worked example (first values of the batch above)")
    k = min(5, len(x))
    st.dataframe(pd.DataFrame({"x_i": x[:k], "x_i − μ_B": x[:k] - mu, "x̂_i": x_hat[:k], "y_i = γx̂_i + β": y[:k]}).round(4),
                 hide_index=True, width="stretch")
    st.latex(rf"\hat x_1=\frac{{{x[0]:.4f}-({mu:.4f})}}{{\sqrt{{{var:.4f}+{eps:g}}}}}=\frac{{{x[0] - mu:.4f}}}{{{np.sqrt(var + eps):.4f}}}"
             rf"={x_hat[0]:.4f},\qquad y_1={gamma:.3f}\cdot({x_hat[0]:.4f})+({beta:.3f})={y[0]:.4f}")


def batch_size_lab(shift, scale, batch, eps, seed):
    st.header("3 · Small batches ⇒ noisy statistics")
    rng = np.random.default_rng(seed + 1)
    n_batches = 400
    rows = []
    for b in BATCH_SIZES:
        xs = shift + scale * rng.standard_normal((n_batches, b))
        mus, sds = xs.mean(1), xs.std(1)
        rows.append((b, mus.std(), np.quantile(sds, 0.05), np.median(sds), np.quantile(sds, 0.95)))
    arr = np.array(rows)
    fig = make_subplots(rows=1, cols=2, subplot_titles=("spread of μ_B across batches", "σ_B across batches (5–95% band)"))
    fig.add_trace(go.Scatter(x=arr[:, 0], y=arr[:, 1], mode="markers+lines", name="measured std of μ_B",
                             line=dict(color="#60A5FA")), row=1, col=1)
    fig.add_trace(go.Scatter(x=arr[:, 0], y=scale / np.sqrt(arr[:, 0]), mode="lines", name="theory σ/√B",
                             line=dict(color="white", dash="dash")), row=1, col=1)
    fig.add_trace(go.Scatter(x=np.r_[arr[:, 0], arr[::-1, 0]], y=np.r_[arr[:, 4], arr[::-1, 2]], fill="toself",
                             fillcolor="rgba(52,211,153,0.25)", line=dict(width=0), name="σ_B 5–95%"), row=1, col=2)
    fig.add_trace(go.Scatter(x=arr[:, 0], y=arr[:, 3], mode="lines+markers", name="median σ_B",
                             line=dict(color="#34D399")), row=1, col=2)
    fig.add_hline(y=scale, line=dict(color="white", dash="dash"), row=1, col=2)
    fig.update_xaxes(type="log", title_text="batch size B", tickvals=BATCH_SIZES)
    fig.update_layout(template="plotly_dark", height=340, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, width="stretch")

    x0 = shift + scale
    mates = shift + scale * rng.standard_normal((n_batches, batch - 1))
    full = np.concatenate([np.full((n_batches, 1), x0), mates], axis=1)
    x0_hat = (x0 - full.mean(1)) / np.sqrt(full.var(1) + eps)
    c1, c2 = st.columns([2, 1])
    with c1:
        hist = go.Figure(go.Histogram(x=x0_hat, nbinsx=40, marker_color="#A78BFA"))
        hist.add_vline(x=1.0, line=dict(color="white", dash="dash"))
        hist.update_layout(template="plotly_dark", height=260, margin=dict(l=10, r=10, t=30, b=10),
                           title=f"x̂ of the same example x = μ + σ in {n_batches} different batches of size {batch}",
                           xaxis_title="x̂ (ideal value with exact statistics: 1)")
        st.plotly_chart(hist, width="stretch")
    with c2:
        st.metric("spread (std) of that example's x̂", f"{x0_hat.std():.3f}")
        st.caption("In training mode one example's output depends on which other examples share its batch. "
                   "This noise acts as a mild regulariser — and is harmful when B is tiny (B = 2 forces x̂ = ±1).")


def running_lab(shift, scale, batch, seed):
    st.header("4 · Training vs inference: running averages")
    st.markdown(
        r"At inference there may be a single example, so BN uses **running estimates** collected during training "
        r"(PyTorch convention, momentum $m$, default $0.1$):"
    )
    st.latex(r"\hat\mu\leftarrow(1-m)\,\hat\mu+m\,\mu_B,\qquad \hat\sigma^2\leftarrow(1-m)\,\hat\sigma^2+m\,\tfrac{B}{B-1}\sigma_B^2,"
             r"\qquad\text{start: }\hat\mu=0,\;\hat\sigma^2=1")
    c1, c2 = st.columns([1, 3])
    with c1:
        mom = st.slider("momentum m", 0.01, 1.0, 0.1, 0.01, key="p95_mom")
        drift = st.checkbox("feature distribution drifts (weights are still learning)", value=True, key="p95_drift")
    t = np.arange(1, N_STEPS + 1)
    true_mu = shift + (2.0 * np.exp(-t / 60.0) if drift else 0.0 * t)
    rng = np.random.default_rng(seed + 2)
    xs = true_mu[:, None] + scale * rng.standard_normal((N_STEPS, batch))
    mu_b = xs.mean(1)
    var_unbiased = xs.var(1) * batch / (batch - 1)
    run_mu, run_var = np.empty(N_STEPS), np.empty(N_STEPS)
    r_mu, r_var = 0.0, 1.0
    for i in range(N_STEPS):
        r_mu = (1 - mom) * r_mu + mom * mu_b[i]
        r_var = (1 - mom) * r_var + mom * var_unbiased[i]
        run_mu[i], run_var[i] = r_mu, r_var
    fig = make_subplots(rows=1, cols=2, subplot_titles=("mean", "variance"))
    fig.add_trace(go.Scatter(x=t, y=mu_b, mode="lines", name="batch μ_B", line=dict(color="rgba(248,113,113,0.5)")), row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=run_mu, mode="lines", name="running mean", line=dict(color="#FBBF24", width=3)), row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=true_mu, mode="lines", name="true mean", line=dict(color="white", dash="dash")), row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=var_unbiased, mode="lines", name="batch variance (unbiased)",
                             line=dict(color="rgba(96,165,250,0.5)")), row=1, col=2)
    fig.add_trace(go.Scatter(x=t, y=run_var, mode="lines", name="running variance", line=dict(color="#34D399", width=3)), row=1, col=2)
    fig.add_hline(y=scale**2, line=dict(color="white", dash="dash"), row=1, col=2)
    fig.update_xaxes(title_text="training step")
    fig.update_layout(template="plotly_dark", height=330, margin=dict(l=10, r=10, t=40, b=10))
    with c2:
        st.plotly_chart(fig, width="stretch")
    with c1:
        st.metric("final running mean", f"{run_mu[-1]:.3f}", f"true {true_mu[-1]:.3f}", delta_color="off")
        st.metric("final running variance", f"{run_var[-1]:.3f}", f"true {scale**2:.3f}", delta_color="off")
    st.caption(f"The running average forgets old batches at rate (1 − m) per step: an effective window of ≈ 1/m = {1 / mom:.0f} "
               "steps. Small m ⇒ smooth but lagging (and still biased toward the initial 0/1 early on); large m ⇒ noisy. "
               "Inference uses these fixed numbers, so `model.eval()` makes the output deterministic and batch-independent.")


def norm_axes_lab(seed):
    st.header("5 · BatchNorm vs LayerNorm vs RMSNorm: which axis?")
    kind = st.radio("Normalisation", ["BatchNorm (each feature over the batch ↓)", "LayerNorm (each example over its features →)",
                                      "RMSNorm (divide each example by its RMS →)"], horizontal=True, key="p95_kind")
    rng = np.random.default_rng(seed + 3)
    n_b, n_f = 6, 8
    feat_scale = np.array([0.5, 1, 2, 4, 1, 3, 0.8, 1.5])
    feat_shift = np.array([2, -1, 0, 5, 1, -3, 0.5, 2])
    x = feat_shift + feat_scale * rng.standard_normal((n_b, n_f)) + rng.normal(0, 2, (n_b, 1))
    eps = 1e-5
    if kind.startswith("Batch"):
        out = batch_norm(x, eps, axis=0)[0]
    elif kind.startswith("Layer"):
        out = batch_norm(x, eps, axis=1)[0]
    else:
        out = rms_norm(x, eps, axis=1)[0]
    fig = make_subplots(rows=1, cols=2, subplot_titles=("before (rows = examples, columns = features)", "after"),
                        horizontal_spacing=0.06)
    for col, mat in ((1, x), (2, out)):
        lim = float(np.abs(mat).max())
        fig.add_trace(go.Heatmap(z=mat, zmin=-lim, zmax=lim, zmid=0, colorscale="RdBu", showscale=False,
                                 text=np.round(mat, 2), texttemplate="%{text}",
                                 x=[f"f{j + 1}" for j in range(n_f)], y=[f"ex{i + 1}" for i in range(n_b)]), row=1, col=col)
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(template="plotly_dark", height=330, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, width="stretch")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Column (feature) stats after**")
        st.dataframe(pd.DataFrame({"mean": out.mean(0), "std": out.std(0)}, index=[f"f{j + 1}" for j in range(n_f)]).T.round(3),
                     width="stretch")
    with c2:
        st.markdown("**Row (example) stats after**")
        rms = np.sqrt(np.mean(out**2, axis=1))
        st.dataframe(pd.DataFrame({"mean": out.mean(1), "std": out.std(1), "RMS": rms},
                                  index=[f"ex{i + 1}" for i in range(n_b)]).T.round(3), width="stretch")
    st.caption("BatchNorm: every **column** gets mean 0 / std 1 (depends on the other examples). LayerNorm: every **row** "
               "gets mean 0 / std 1 (each example on its own). RMSNorm: every row gets RMS 1 but its mean is not removed.")


def deep_lab(seed):
    st.header("6 · Deep network: activation scale with and without BN")
    c1, c2 = st.columns([1, 3])
    with c1:
        depth = st.slider("depth", 2, 50, 30, key="p95_depth")
        gain = st.slider("weight scale (× He init)", 0.5, 1.5, 1.2, 0.05, key="p95_gain")
    no_bn = deep_scales(depth, gain, False, seed)
    with_bn = deep_scales(depth, gain, True, seed)
    scaled_bn = deep_scales(depth, 3.0 * gain, True, seed)
    layers = np.arange(1, depth + 1)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=layers, y=np.where(no_bn > 0, no_bn, np.nan), mode="lines+markers", name="no BN",
                             line=dict(color="#F87171")))
    fig.add_trace(go.Scatter(x=layers, y=with_bn, mode="lines+markers", name="with BN", line=dict(color="#34D399")))
    fig.update_yaxes(type="log", title_text="std of the input to each ReLU", exponentformat="power")
    fig.update_xaxes(title_text="layer")
    fig.update_layout(template="plotly_dark", height=340, margin=dict(l=10, r=10, t=20, b=10))
    with c2:
        st.plotly_chart(fig, width="stretch")
    with c1:
        st.metric("no BN: std at last layer", f"{no_bn[-1]:.3g}", f"theory √2·gain^L = {np.sqrt(2.0) * gain ** depth:.3g}", delta_color="off")
        st.metric("with BN: std at last layer", f"{with_bn[-1]:.4f}")
        st.caption(f"Scale invariance: tripling all weights changes the BN curve by at most "
                   f"{np.abs(scaled_bn - with_bn).max():.1e} — BN(aWx) = BN(Wx) for a > 0 (up to ε).")
    st.markdown(
        r"Without BN each ReLU layer multiplies the variance by $\text{gain}^2$ (He init has gain 1), so the std behaves "
        r"like $\sqrt2\,\text{gain}^{\ell}$ (unit-variance inputs give $\mathrm{Var}(z_1)=2\,\text{gain}^2$). With BN every layer re-standardises, so the scale is pinned at $\approx1$ regardless "
        r"of depth or weight scale."
    )
    with st.container(border=True):
        st.markdown("**Why does BN help? (state of understanding)**")
        st.markdown(
            "- The original paper motivated BN by reducing **internal covariate shift** — the change of each layer's input "
            "distribution as earlier layers learn.\n"
            "- Santurkar et al. (2018, *How Does Batch Normalization Help Optimization?*) found that BN networks train well "
            "even when noise is deliberately injected to *create* distribution shift, and that BN does not necessarily "
            "reduce the shift. They argued instead that BN makes the **loss landscape smoother** (gradients change more "
            "predictably), allowing larger learning rates.\n"
            "- Other contributing explanations: the scale invariance above (an automatic effective learning-rate schedule) "
            "and the regularising noise of batch statistics. There is no single settled answer; treat 'reduces covariate "
            "shift' as the historical motivation, not an established mechanism."
        )


def ai_connection():
    st.header("7 · AI connection")
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.markdown("**LayerNorm / RMSNorm in transformers**")
            st.markdown(r"LayerNorm normalises each token vector over its $d$ features — no batch dependence, identical in "
                        r"training and inference, fine for batch size 1 and variable sequence lengths. **RMSNorm** "
                        r"(Zhang & Sennrich, 2019) drops the mean-centring and $\beta$:")
            st.latex(r"\mathrm{RMSNorm}(x)=\frac{x}{\sqrt{\frac1d\sum_{j=1}^{d}x_j^2+\varepsilon}}\odot g")
            st.markdown("It is cheaper and works as well in practice; LLaMA, Mistral and Gemma use it (pre-norm placement).")
    with c2:
        with st.container(border=True):
            st.markdown("**BatchNorm in CNNs**")
            st.markdown("For images BN keeps one (γ, β) pair per **channel** and averages over the batch *and* all spatial "
                        "positions (N × H × W values). `Conv → BN → ReLU` is the standard ResNet block; at inference BN can "
                        "even be folded into the preceding convolution's weights.")
    with c3:
        with st.container(border=True):
            st.markdown("**Small-batch issues**")
            st.markdown("Detection/segmentation models often fit only 1–2 images per GPU, so batch statistics become "
                        "noisy (Lab 3). Fixes: **SyncBN** (stats across GPUs), **GroupNorm** (normalise groups of channels "
                        "per example), or freezing BN statistics when fine-tuning. Train/eval mismatch from forgetting "
                        "`model.eval()` is a classic bug.")


def takeaways():
    st.header("Key takeaways")
    st.success(
        "1. BN: x̂ = (x − μ_B)/√(σ²_B + ε), then y = γx̂ + β — learnable γ, β can even undo the normalisation.\n"
        "2. Batch statistics are noisy for small B (std of μ_B = σ/√B); training-mode outputs depend on batch-mates.\n"
        "3. Inference uses running averages (momentum), so `model.eval()` changes BN's behaviour.\n"
        "4. LayerNorm/RMSNorm normalise each example over its features — the standard in transformers."
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        safe_page_link("pages/94Dropout.py", "← Previous: Dropout")
    with c2:
        safe_page_link("pages/35Z-Scores & Standardization.py", "Revisit: Z-Scores & Standardization")
    with c3:
        safe_page_link("pages/96Convolution.py", "Next: Convolution →")


def main():
    st.set_page_config(page_title="NN · Batch Normalization", page_icon="📏", layout="wide")
    seed = ensure_seed()
    intuition()
    x, x_hat, y, mu, var, eps, gamma, beta, shift, scale, batch = batch_lab(seed)
    seed = st.session_state["p95_seed"]
    worked_example(x, x_hat, y, mu, var, eps, gamma, beta)
    batch_size_lab(shift, scale, batch, eps, seed)
    running_lab(shift, scale, batch, seed)
    norm_axes_lab(seed)
    deep_lab(seed)
    ai_connection()
    takeaways()


main()
