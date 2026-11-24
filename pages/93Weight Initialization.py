"""93 · Weight Initialization — keep the signal alive through many layers."""

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

SCHEMES = ["N(0, 1)", "Small N(0, 0.01²)", "Xavier / Glorot", "He / Kaiming", "Orthogonal"]
SCHEME_COLORS = {
    "N(0, 1)": "#F87171",
    "Small N(0, 0.01²)": "#A78BFA",
    "Xavier / Glorot": "#60A5FA",
    "He / Kaiming": "#34D399",
    "Orthogonal": "#FBBF24",
}
ACTS = ["ReLU", "tanh"]
BATCH = 64
DEFAULT_SEED = 93


def weight_std(scheme, n_in, n_out):
    """Per-entry standard deviation of the Gaussian schemes (orthogonal handled separately)."""
    if scheme == "N(0, 1)":
        return 1.0
    if scheme == "Small N(0, 0.01²)":
        return 0.01
    if scheme == "Xavier / Glorot":
        return float(np.sqrt(2.0 / (n_in + n_out)))
    if scheme == "He / Kaiming":
        return float(np.sqrt(2.0 / n_in))
    raise ValueError(scheme)


def orth_gain(act):
    return float(np.sqrt(2.0)) if act == "ReLU" else 1.0


def q_factor(scheme, n, act):
    """n · Var(w) for a square n×n layer (for an orthogonal matrix the effective value is gain²)."""
    if scheme == "Orthogonal":
        return orth_gain(act) ** 2
    return n * weight_std(scheme, n, n) ** 2


def make_weight(scheme, base, act):
    """Turn a shared standard-normal matrix `base` into a weight matrix of the chosen scheme."""
    n_in, n_out = base.shape
    if scheme == "Orthogonal":
        q, r = np.linalg.qr(base)
        signs = np.sign(np.diag(r))
        signs[signs == 0] = 1.0
        return orth_gain(act) * q * signs
    return weight_std(scheme, n_in, n_out) * base


def act_fn(z, act):
    return np.maximum(z, 0.0) if act == "ReLU" else np.tanh(z)


def act_grad(z, h, act):
    return (z > 0).astype(float) if act == "ReLU" else 1.0 - h**2


@st.cache_data(show_spinner=False, max_entries=64)
def simulate(scheme, act, depth, width, seed):
    """Forward + backward pass through a bias-free MLP; returns per-layer statistics.

    Every scheme uses the same standard-normal draws, so only the scale/shape of the weights differs.
    Loss: a fixed random linear read-out L = (1/B) Σ_b r_b · h_L,b, so ∂L/∂h_L = R / B.
    """
    rng = np.random.default_rng(seed)
    x = rng.standard_normal((BATCH, width))
    readout = rng.standard_normal((BATCH, width))
    weights = [make_weight(scheme, rng.standard_normal((width, width)), act) for _ in range(depth)]
    with np.errstate(over="ignore", under="ignore", invalid="ignore", divide="ignore"):
        hs, zs = [x], []
        for w in weights:
            z = hs[-1] @ w
            zs.append(z)
            hs.append(act_fn(z, act))
        dh = readout / BATCH
        grad_w = np.zeros(depth)
        grad_h = np.zeros(depth)
        for layer in range(depth - 1, -1, -1):
            grad_h[layer] = np.linalg.norm(dh)
            delta = dh * act_grad(zs[layer], hs[layer + 1], act)
            grad_w[layer] = np.linalg.norm(hs[layer].T @ delta)
            dh = delta @ weights[layer].T
        h_std = np.array([h.std() for h in hs[1:]])
        z_var = np.array([np.mean(z**2) for z in zs])
        saturated = float(np.mean(np.abs(hs[-1]) > 0.99)) if act == "tanh" else float(np.mean(hs[-1] == 0.0))
    return {"h_std": h_std, "z_var": z_var, "grad_w": grad_w, "grad_h": grad_h,
            "hs": [h.ravel() for h in hs[1:]], "zs": [z.ravel() for z in zs], "frac": saturated}


def positive_or_nan(a):
    a = np.asarray(a, dtype=float)
    return np.where(np.isfinite(a) & (a > 0), a, np.nan)


def sci(v):
    if not np.isfinite(v):
        return "overflow"
    if v == 0:
        return "0"
    return f"{v:.3g}" if 1e-3 <= abs(v) < 1e4 else f"{v:.2e}"


def verdict(ratio):
    if not np.isfinite(ratio) or ratio > 1e3:
        return "exploding"
    if ratio < 1e-3:
        return "vanishing"
    return "stable"


def symmetric_training(mode, const, seed, steps=150, lr=0.2):
    """3 → 4 (tanh) → 1 regression network trained by full-batch gradient descent."""
    rng = np.random.default_rng(seed)
    x = rng.uniform(-2, 2, (40, 3))
    y = np.sin(x[:, 0]) + 0.5 * x[:, 1] * x[:, 2]
    if mode == "All zeros":
        w1, w2 = np.zeros((3, 4)), np.zeros((4, 1))
    elif mode == "All the same constant c":
        w1, w2 = np.full((3, 4), const), np.full((4, 1), const)
    else:
        w1, w2 = 0.5 * rng.standard_normal((3, 4)), 0.5 * rng.standard_normal((4, 1))
    b1, b2 = np.zeros(4), np.zeros(1)
    first_grad = None
    for step in range(steps):
        h = np.tanh(x @ w1 + b1)
        out = (h @ w2 + b2)[:, 0]
        d = (2.0 * (out - y) / len(y))[:, None]
        g_w2, g_b2 = h.T @ d, d.sum(0)
        dz = (d @ w2.T) * (1.0 - h**2)
        g_w1, g_b1 = x.T @ dz, dz.sum(0)
        if step == 0:
            first_grad = g_w1.copy()
        w1, b1, w2, b2 = w1 - lr * g_w1, b1 - lr * g_b1, w2 - lr * g_w2, b2 - lr * g_b2
    loss = float(np.mean(((np.tanh(x @ w1 + b1) @ w2 + b2)[:, 0] - y) ** 2))
    distinct = len({tuple(np.round(col, 8)) for col in w1.T})
    return first_grad, w1, loss, distinct


def heatmap(mat, title, colorscale="RdBu", zmid=0.0):
    fig = go.Figure(go.Heatmap(z=mat, colorscale=colorscale, zmid=zmid, text=np.round(mat, 3),
                               texttemplate="%{text}", showscale=False,
                               x=[f"unit {j + 1}" for j in range(mat.shape[1])],
                               y=[f"x{i + 1}" for i in range(mat.shape[0])]))
    fig.update_layout(template="plotly_dark", title=title, height=260, margin=dict(l=10, r=10, t=40, b=10),
                      yaxis=dict(autorange="reversed"))
    return fig


def intuition():
    st.title("🎯 Weight Initialization")
    st.markdown("##### Before learning starts, the random weights decide whether a signal can even get through the network.")
    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown(
            r"""
A deep network is a long chain of matrix multiplications. Each layer multiplies the **size** of the signal by
roughly the same factor. If that factor is $1.2$, after 50 layers the signal is $1.2^{50}\approx 9{,}100\times$
larger; if it is $0.8$, it is $0.8^{50}\approx 10^{-5}$ — practically zero. The same happens to the gradients
flowing **backwards**.

So the initial scale of the weights is not a detail: pick it so that each layer **keeps the variance roughly
constant** ($\text{factor}\approx 1$), forward *and* backward. That single idea gives the famous
**Xavier/Glorot** and **He/Kaiming** rules.
"""
        )
    with c2:
        with st.container(border=True):
            st.markdown("**Why it matters for AI**")
            st.markdown(
                "- Bad init ⇒ activations blow up to `inf`/`NaN` or shrink to 0 before training even starts.\n"
                "- Vanishing gradients ⇒ early layers never learn.\n"
                "- Every framework (PyTorch, JAX, TensorFlow) ships a default init for exactly this reason."
            )


def depth_lab():
    st.header("1 · Lab: push a signal through a deep MLP")
    st.markdown(
        r"A bias-free MLP $h_\ell=\phi(z_\ell)$, $z_\ell=h_{\ell-1}W_\ell$ with square $n\times n$ layers and a batch of "
        rf"{BATCH} Gaussian inputs. Backward: a fixed random read-out loss $L=\frac1B\sum_b r_b\cdot h_{{L,b}}$."
    )
    if "p93_seed" not in st.session_state:
        st.session_state["p93_seed"] = DEFAULT_SEED
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        scheme = st.selectbox("Initialization scheme", SCHEMES, index=3, key="p93_scheme")
    with c2:
        act = st.radio("Activation φ", ACTS, horizontal=True, key="p93_act")
    with c3:
        depth = st.slider("Depth (layers)", 2, 50, 30, key="p93_depth")
    with c4:
        width = st.slider("Width n (units per layer)", 16, 256, 64, step=16, key="p93_width")
    c5, c6 = st.columns([1, 3])
    with c5:
        if st.button("🎲 Resample weights & data", key="p93_resample"):
            st.session_state["p93_seed"] = int(np.random.default_rng(st.session_state["p93_seed"]).integers(0, 10**6))
    with c6:
        overlay = st.toggle("Overlay all five schemes (same random numbers)", value=True, key="p93_overlay")
    seed = st.session_state["p93_seed"]

    res = simulate(scheme, act, depth, width, seed)
    layers = np.arange(1, depth + 1)
    fig = make_subplots(rows=1, cols=3, subplot_titles=(
        "Forward: std of activations h_ℓ", "Backward: ‖∂L/∂h_ℓ‖", "Weight gradient ‖∂L/∂W_ℓ‖"))
    shown = SCHEMES if overlay else [scheme]
    for s in shown:
        r = res if s == scheme else simulate(s, act, depth, width, seed)
        sel = s == scheme
        style = dict(color=SCHEME_COLORS[s], width=4 if sel else 1.5, dash="solid" if sel else "dot")
        for col, key in enumerate(("h_std", "grad_h", "grad_w"), start=1):
            fig.add_trace(go.Scatter(x=layers, y=positive_or_nan(r[key]), mode="lines", name=s, line=style,
                                     legendgroup=s, showlegend=col == 1, opacity=1.0 if sel else 0.7),
                          row=1, col=col)
    fig.update_yaxes(type="log", exponentformat="power")
    fig.update_xaxes(title_text="layer ℓ")
    fig.update_layout(template="plotly_dark", height=420, margin=dict(l=10, r=10, t=50, b=10),
                      legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig, width="stretch")

    act_ratio = res["h_std"][-1] / res["h_std"][0] if res["h_std"][0] > 0 else np.nan
    grad_ratio = res["grad_h"][0] / res["grad_h"][-1] if res["grad_h"][-1] > 0 else np.nan
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("std(h) at last layer", sci(res["h_std"][-1]))
    m2.metric("Forward: std last / first", sci(act_ratio), verdict(act_ratio), delta_color="off")
    m3.metric("Backward: ‖∂L/∂h₁‖ / ‖∂L/∂h_L‖", sci(grad_ratio), verdict(grad_ratio), delta_color="off")
    label = "saturated |h| > 0.99 (last layer)" if act == "tanh" else "exact zeros in h (last layer)"
    m4.metric(label, f"{100 * res['frac']:.1f}%")
    st.caption(
        "The weight gradient is (forward activation) × (backward signal). For ReLU it can look flat across layers "
        "even when it is 10⁻⁴⁰ or 10⁴⁰ everywhere — read the *height* of the curve, not only its slope. "
        "Try: ReLU + Xavier (slow decay, ×√½ per layer), ReLU + He (flat), tanh + N(0,1) (saturated forward, "
        "gradients grow backwards), Small N(0, 0.01²) (everything collapses)."
    )
    return scheme, act, depth, width, seed, res


def histogram_lab(scheme, act, depth, res):
    with st.expander("📊 Activation histograms for selected layers", expanded=True):
        which = st.radio("Show", ["post-activation h = φ(z)", "pre-activation z"], horizontal=True, key="p93_hist")
        picks = sorted({1, max(1, round(depth / 3)), max(1, round(2 * depth / 3)), depth})
        data = res["hs"] if which.startswith("post") else res["zs"]
        fig = make_subplots(rows=1, cols=len(picks), subplot_titles=[f"layer {p}" for p in picks])
        for i, p in enumerate(picks, start=1):
            vals = data[p - 1]
            vals = vals[np.isfinite(vals)]
            fig.add_trace(go.Histogram(x=vals, nbinsx=50, marker_color=SCHEME_COLORS[scheme], showlegend=False),
                          row=1, col=i)
        fig.update_layout(template="plotly_dark", height=280, margin=dict(l=10, r=10, t=40, b=10), bargap=0.02)
        st.plotly_chart(fig, width="stretch")
        st.caption(
            f"{scheme} + {act}. Watch the x-axis range: healthy layers keep a similar spread; tanh with large weights "
            "piles everything at ±1 (saturation), tiny weights squeeze everything into a spike at 0."
        )


def derivation_lab():
    st.header(r"2 · Where the rules come from: $\mathrm{Var}(z)=n\,\mathrm{Var}(w)\,\mathbb{E}[x^2]$")
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown(
            r"""
One pre-activation is a sum of $n$ products, $z=\sum_{i=1}^{n} w_i x_i$, with weights independent of the inputs
and $\mathbb{E}[w_i]=0$. Then each term has mean $0$ and
$\mathrm{Var}(w_i x_i)=\mathbb{E}[w_i^2]\,\mathbb{E}[x_i^2]$, and independent terms add their variances:
"""
        )
        st.latex(r"\mathrm{Var}(z)=n\,\mathrm{Var}(w)\,\mathbb{E}[x^2]\;\overset{\mathbb{E}[x]=0}{=}\;n\,\mathrm{Var}(w)\,\mathrm{Var}(x)")
        st.markdown(
            r"""
- **Linear / tanh near 0** ($\tanh'(0)=1$): keep $n\,\mathrm{Var}(w)=1$. Doing the same for the backward pass
  needs $n_\text{out}\mathrm{Var}(w)=1$; **Xavier/Glorot** compromises: $\mathrm{Var}(w)=\dfrac{2}{n_\text{in}+n_\text{out}}$.
- **ReLU** zeroes the negative half of a symmetric $z$, so $\mathbb{E}[\mathrm{ReLU}(z)^2]=\tfrac12\mathrm{Var}(z)$.
  The next layer gets $\mathrm{Var}(z_{\ell+1})=n\,\mathrm{Var}(w)\cdot\tfrac12\mathrm{Var}(z_\ell)$, so
  **He/Kaiming** sets $\mathrm{Var}(w)=\dfrac{2}{n_\text{in}}$.
- **Orthogonal** $W$ (times a gain $g$) preserves lengths exactly: $\lVert xW\rVert=g\lVert x\rVert$
  (gain $\sqrt2$ for ReLU, $1$ for tanh here).
"""
        )
    with c2:
        with st.container(border=True):
            st.markdown("**Live check** — sample one layer and compare with the formula")
            n = st.slider("fan-in n", 1, 1000, 256, key="p93_n")
            sw = st.slider("weight std σ_w", 0.01, 2.0, 0.1, 0.01, key="p93_sw")
            sx = st.slider("input std σ_x", 0.1, 3.0, 1.0, 0.1, key="p93_sx")
            kind = st.radio("inputs x are", ["Gaussian N(0, σ_x²)", "ReLU(N(0, σ_x²))"], horizontal=True,
                            key="p93_kind")
            rng = np.random.default_rng(st.session_state.get("p93_seed", DEFAULT_SEED) + 1)
            x = sx * rng.standard_normal((200, n))
            if kind.startswith("ReLU"):
                x = np.maximum(x, 0.0)
            w = sw * rng.standard_normal((n, 200))
            z = x @ w
            ex2_theory = sx**2 / 2 if kind.startswith("ReLU") else sx**2
            theory = n * sw**2 * ex2_theory
            empirical = float(z.var())
            half = r"\tfrac12" if kind.startswith("ReLU") else ""
            st.latex(rf"n\,\sigma_w^2\,\mathbb{{E}}[x^2] = {n}\cdot{sw:.2f}^2\cdot{half}{sx:.1f}^2 = {theory:.4g}")
            rel = abs(empirical - theory) / theory
            a, b = st.columns(2)
            a.metric("Formula Var(z)", f"{theory:.4g}")
            b.metric("Empirical Var(z) (40 000 samples)", f"{empirical:.4g}", f"{100 * rel:.1f}% off", delta_color="off")
            st.caption(
                f"Empirical E[x²] = {np.mean(x**2):.4g} vs theory {ex2_theory:.4g}. "
                f"He would pick σ_w = √(2/n) = {np.sqrt(2 / n):.4f}; Xavier (n_in = n_out = n) σ_w = √(1/n) = {np.sqrt(1 / n):.4f}."
            )


def worked_example(act, depth, width, seed):
    st.header("3 · Worked example: predicted vs measured variance at layer L")
    st.markdown(
        r"With $q=n\,\mathrm{Var}(w)$ and inputs with $\mathbb{E}[x^2]=1$, ReLU layers give "
        r"$\mathrm{Var}(z_1)=q$ and $\mathrm{Var}(z_{\ell+1})=\tfrac q2\mathrm{Var}(z_\ell)$, hence "
        r"$\mathrm{Var}(z_L)=q\,(q/2)^{L-1}$. For tanh only the small-signal regime is linear: "
        r"$\mathrm{Var}(z_L)\approx q^{L}$ while $|z|\ll1$."
    )
    rows = []
    for s in SCHEMES:
        q = q_factor(s, width, act)
        per_layer = q / 2 if act == "ReLU" else q
        with np.errstate(over="ignore"):
            predicted = q * (q / 2) ** (depth - 1) if act == "ReLU" else q**depth
        measured = simulate(s, act, depth, width, seed)["z_var"][-1]
        if act == "ReLU":
            pred_text = sci(predicted)
        elif q <= 1.0 + 1e-9:
            pred_text = f"≤ {sci(predicted)} (linear approx.)"
        else:
            pred_text = "n/a: q > 1 ⇒ tanh saturates"
        var_w = (orth_gain(act) ** 2 / width) if s == "Orthogonal" else weight_std(s, width, width) ** 2
        rows.append({"scheme": s, "Var(w)": sci(var_w), "q = n·Var(w)": sci(q),
                     "variance factor / layer": sci(per_layer),
                     "predicted Var(z_L)": pred_text,
                     "measured Var(z_L)": sci(measured)})
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    he_q = q_factor("He / Kaiming", width, act)
    xa_q = q_factor("Xavier / Glorot", width, act)
    st.latex(
        rf"n={width},\;L={depth}:\quad q_\text{{He}}=n\cdot\tfrac{{2}}{{n}}={he_q:g},\qquad "
        rf"q_\text{{Xavier}}=n\cdot\tfrac{{2}}{{2n}}={xa_q:g}\;\Rightarrow\;"
        rf"\text{{ReLU+Xavier: }}(\tfrac12)^{{{depth - 1}}}={0.5 ** (depth - 1):.3g}"
    )
    st.caption(
        "Measured values are the mean of z² over the batch and all units at the last layer. With narrow layers the "
        "per-layer factor fluctuates around its mean and these fluctuations compound with depth, so expect "
        "order-of-magnitude agreement for ReLU at large L and small n; increasing the width tightens it. For tanh the "
        "linear prediction fails as soon as |z| reaches ~1 (saturation bounds h, so the variance cannot explode)."
    )


def symmetry_lab():
    st.header("4 · Why not just start at zero? The symmetry problem")
    st.markdown(
        r"If every hidden unit starts with the **same** weights, they compute the same output, receive the **same "
        r"gradient**, and get the same update — forever. The layer behaves like a single unit. With all zeros and "
        r"tanh it is worse: $h=\tanh(0)=0$ and $W_2=0$, so both weight gradients are exactly $0$."
    )
    c1, c2 = st.columns([1, 3])
    with c1:
        mode = st.radio("Init of a 3 → 4 (tanh) → 1 net", ["All zeros", "All the same constant c", "Small random"],
                        key="p93_sym_mode")
        const = st.slider("constant c", -1.0, 1.0, 0.3, 0.1, key="p93_const")
        g0, w1, loss, distinct = symmetric_training(mode, const, st.session_state.get("p93_seed", DEFAULT_SEED))
        st.metric("distinct hidden units after 150 GD steps", f"{distinct} / 4")
        st.metric("training MSE after 150 steps", f"{loss:.4f}")
    with c2:
        a, b = st.columns(2)
        a.plotly_chart(heatmap(g0, "∂L/∂W₁ at step 0 (columns = hidden units)"), width="stretch")
        b.plotly_chart(heatmap(w1, "W₁ after training"), width="stretch")
    if distinct == 1:
        st.warning("All four columns are identical: the hidden units never differentiate. Random init breaks the symmetry.")
    else:
        st.success("Random init gives every unit a different starting point, so they learn different features.")


def ai_connection():
    st.header("5 · AI connection")
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("**PyTorch defaults**")
            st.markdown(
                r"""
`nn.Linear` and `nn.Conv2d` call `kaiming_uniform_(weight, a=√5)`, which works out to
$w\sim U\!\left(-\tfrac{1}{\sqrt{n_\text{in}}},\tfrac{1}{\sqrt{n_\text{in}}}\right)$, i.e.
$\mathrm{Var}(w)=\tfrac{1}{3n_\text{in}}$ — smaller than He's $\tfrac{2}{n_\text{in}}$. That is fine for shallow nets
or nets with normalization layers; for a deep plain ReLU stack people call `nn.init.kaiming_normal_` explicitly
(and `xavier_uniform_` for tanh/sigmoid). `nn.init.orthogonal_` is common in RNNs and RL.
"""
            )
    with c2:
        with st.container(border=True):
            st.markdown("**Transformers scale init by depth**")
            st.markdown(
                r"""
A transformer adds every block's output to a **residual stream**: $x_{\ell+1}=x_\ell+f_\ell(x_\ell)$.
If each branch adds independent variance $v$, after $N$ residual additions the variance has grown by $N v$.
GPT-2 therefore initialises weights with $\mathcal N(0,0.02^2)$ and **scales the residual output projections by
$1/\sqrt{N}$** ($N$ = number of residual layers), so the stream's variance stays $O(1)$ however deep the model is.
DeepNet/DeepNorm uses depth-dependent scaling to train transformers with ~1000 layers.
"""
            )


def takeaways():
    st.header("Key takeaways")
    st.success(
        "1. Each layer multiplies the signal variance by ≈ n·Var(w) (×½ after a ReLU); over depth this compounds.\n"
        "2. Xavier: Var(w) = 2/(n_in + n_out) for tanh-like units; He: Var(w) = 2/n_in for ReLU; orthogonal preserves norms.\n"
        "3. Too large ⇒ explosion or tanh saturation; too small ⇒ everything (forward and backward) vanishes.\n"
        "4. Never initialise all weights to the same value — identical units get identical gradients and stay identical."
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        safe_page_link("pages/75Learning Curves.py", "← Previous: Learning Curves")
    with c2:
        safe_page_link("pages/70Backpropagation — Chain Rule Backward.py", "Revisit: Backpropagation")
    with c3:
        safe_page_link("pages/94Dropout.py", "Next: Dropout →")


def main():
    st.set_page_config(page_title="NN · Weight Initialization", page_icon="🎯", layout="wide")
    intuition()
    scheme, act, depth, width, seed, res = depth_lab()
    histogram_lab(scheme, act, depth, res)
    derivation_lab()
    worked_example(act, depth, width, seed)
    symmetry_lab()
    ai_connection()
    takeaways()


main()
