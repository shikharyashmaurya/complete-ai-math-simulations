import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="91 · RMSProp & Adam", page_icon="🧭", layout="wide")

OPTIMIZERS = ["SGD", "Momentum", "AdaGrad", "RMSProp", "Adam"]
COLORS = {"SGD": "#f87171", "Momentum": "#fbbf24", "AdaGrad": "#a3e635", "RMSProp": "#c084fc", "Adam": "#38bdf8"}
LR_OPTIONS = [1e-4, 2e-4, 5e-4, 1e-3, 2e-3, 5e-3, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]
EPS_OPTIONS = [1e-8, 1e-6, 1e-4, 1e-2, 1e-1]
# name: (default lr for SGD/momentum, default lr for adaptive methods, default steps, plot box, start)
LANDSCAPES = {
    "Ill-conditioned bowl": (0.02, 0.1, 150, (-5, 5, -3, 3), (-4.0, 2.0)),
    "Rosenbrock banana": (1e-3, 0.05, 1000, (-2, 2, -1, 3), (-1.2, 1.0)),
    "Badly scaled features": (0.01, 0.1, 200, (-3, 3, -3, 3), (-2.0, -2.0)),
}
SCALE = 10.0  # feature scales s and 1/s in the badly scaled landscape


def make_landscape(name, kappa, angle):
    """(f, ∇f, minimiser) for the chosen 2-D test function."""
    if name == "Ill-conditioned bowl":
        th = np.deg2rad(angle)
        rot = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
        hess = rot @ np.diag([1.0, float(kappa)]) @ rot.T
        return (lambda p: 0.5 * np.einsum("...i,ij,...j->...", p, hess, p)), (lambda p: hess @ p), np.zeros(2)
    if name == "Rosenbrock banana":
        def f(p):
            return (1 - p[..., 0]) ** 2 + 100 * (p[..., 1] - p[..., 0] ** 2) ** 2

        def grad(p):
            return np.array([-2 * (1 - p[0]) - 400 * p[0] * (p[1] - p[0] ** 2), 200 * (p[1] - p[0] ** 2)])

        return f, grad, np.ones(2)

    # f = ½ s²(x−1)² + ½ (y−1)²/s²: the x-gradient is s⁴ = 10,000× "louder" than the y-gradient.
    def f(p):
        return 0.5 * SCALE**2 * (p[..., 0] - 1) ** 2 + 0.5 * (p[..., 1] - 1) ** 2 / SCALE**2

    def grad(p):
        return np.array([SCALE**2 * (p[0] - 1), (p[1] - 1) / SCALE**2])

    return f, grad, np.ones(2)


def optimize(opt, grad, x0, lr, steps, hp):
    """Full-batch run of one optimizer; returns the path (stops early if it blows up).

    SGD:      x ← x − η g
    Momentum: b ← β b + g,              x ← x − η b            (PyTorch convention)
    AdaGrad:  G ← G + g²,               x ← x − η g / (√G + ε)
    RMSProp:  s ← ρ s + (1−ρ) g²,        x ← x − η g / (√s + ε)
    Adam:     m ← β₁m + (1−β₁)g,  v ← β₂v + (1−β₂)g²,  x ← x − η m̂ / (√v̂ + ε)
    """
    x = np.array(x0, dtype=float)
    m = np.zeros(2)
    v = np.zeros(2)
    path = [x.copy()]
    for t in range(1, steps + 1):
        g = grad(x)
        if opt == "SGD":
            x = x - lr * g
        elif opt == "Momentum":
            m = hp["beta"] * m + g
            x = x - lr * m
        elif opt == "AdaGrad":
            v = v + g * g
            x = x - lr * g / (np.sqrt(v) + hp["eps"])
        elif opt == "RMSProp":
            v = hp["rho"] * v + (1 - hp["rho"]) * g * g
            x = x - lr * g / (np.sqrt(v) + hp["eps"])
        else:
            m = hp["b1"] * m + (1 - hp["b1"]) * g
            v = hp["b2"] * v + (1 - hp["b2"]) * g * g
            m_hat = m / (1 - hp["b1"] ** t)
            v_hat = v / (1 - hp["b2"] ** t)
            x = x - lr * m_hat / (np.sqrt(v_hat) + hp["eps"])
        if not np.all(np.isfinite(x)) or np.abs(x).max() > 1e6:
            break
        path.append(x.copy())
    return np.array(path)


def adam_trace(grad, x0, lr, steps, hp, coord):
    """Per-step Adam internals for one coordinate, plus the step an un-bias-corrected Adam would take."""
    b1, b2, eps = hp["b1"], hp["b2"], hp["eps"]
    x = np.array(x0, dtype=float)
    m = np.zeros(2)
    v = np.zeros(2)
    rows = []
    for t in range(1, steps + 1):
        g = grad(x)
        m = b1 * m + (1 - b1) * g
        v = b2 * v + (1 - b2) * g * g
        m_hat, v_hat = m / (1 - b1**t), v / (1 - b2**t)
        step = lr * m_hat / (np.sqrt(v_hat) + eps)
        raw = lr * m / (np.sqrt(v) + eps)
        rows.append({"t": t, "g": g[coord], "m": m[coord], "v": v[coord], "m̂": m_hat[coord], "v̂": v_hat[coord],
                     "step η·m̂/(√v̂+ε)": step[coord], "step / η": step[coord] / lr,
                     "no bias correction: step / η": raw[coord] / lr})
        x = x - step
        if not np.all(np.isfinite(x)) or np.abs(x).max() > 1e6:
            break
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- page sections
def intuition():
    st.title("🧭 RMSProp & Adam — A Step Size for Every Parameter")
    st.markdown(
        r"""
SGD and momentum use **one learning rate for every parameter**. But in a real network some weights see huge
gradients (a frequently used embedding, the last layer) and others tiny ones (rare features, deep layers).
A rate small enough for the loud parameters is painfully slow for the quiet ones (page 53's $\eta < 2/\lambda$ is
set by the **steepest** direction).

**Adaptive methods** divide each parameter's gradient by a running estimate of *its own* gradient size, so
every coordinate moves at a comparable pace. The family grew in three steps:
"""
    )
    c1, c2, c3 = st.columns(3)
    with c1, st.container(border=True):
        st.markdown("**AdaGrad** (2011) — sum of all squared gradients")
        st.latex(r"G_t = G_{t-1} + g_t^2,\quad x_{t+1} = x_t - \frac{\eta\, g_t}{\sqrt{G_t}+\varepsilon}")
        st.caption("Great for sparse features, but G only grows, so the step keeps shrinking — it can stall.")
    with c2, st.container(border=True):
        st.markdown("**RMSProp** (2012) — *running average* of squared gradients")
        st.latex(r"s_t = \rho\, s_{t-1} + (1-\rho)\, g_t^2,\quad x_{t+1} = x_t - \frac{\eta\, g_t}{\sqrt{s_t}+\varepsilon}")
        st.caption("Forgets old gradients (window ≈ 1/(1−ρ) steps), so the step does not die out.")
    with c3, st.container(border=True):
        st.markdown("**Adam** (2015) — momentum + RMSProp + bias correction")
        st.latex(r"\begin{aligned} m_t &= \beta_1 m_{t-1} + (1-\beta_1) g_t \\ v_t &= \beta_2 v_{t-1} + (1-\beta_2) g_t^2 \\ "
                 r"\hat m_t &= \frac{m_t}{1-\beta_1^t},\ \ \hat v_t = \frac{v_t}{1-\beta_2^t} \\ "
                 r"x_{t+1} &= x_t - \eta\,\frac{\hat m_t}{\sqrt{\hat v_t}+\varepsilon} \end{aligned}")
    st.caption("All squares, roots and divisions are element-wise: every parameter gets its own denominator.")


def lab():
    st.header("🧪 Lab 1 — Race on three landscapes")
    c1, c2, c3 = st.columns([2, 1, 1])
    name = c1.radio("Landscape", list(LANDSCAPES), horizontal=True, key="p91_land")
    lr_sgd_default, lr_ad_default, steps_default, box, x0 = LANDSCAPES[name]
    tag = ["bowl", "rosen", "scales"][list(LANDSCAPES).index(name)]
    kappa, angle = 25, 0
    if name == "Ill-conditioned bowl":
        kappa = c2.slider("Condition number κ", 1, 100, 25, key="p91_kappa")
        angle = c3.select_slider("Rotate the bowl (°)", [0, 15, 30, 45], 0, key="p91_angle")
        st.markdown(r"$f = \tfrac12\, p^\top R\,\mathrm{diag}(1,\kappa)\,R^\top p$ — rotating mixes the steep and shallow directions across both coordinates.")
    elif name == "Rosenbrock banana":
        st.markdown(r"$f = (1-x)^2 + 100\,(y-x^2)^2$ — a curved, flat-bottomed valley; minimum at $(1, 1)$.")
    else:
        st.markdown(rf"$f = \tfrac12\,{SCALE:.0f}^2 (x-1)^2 + \tfrac12\,(y-1)^2/{SCALE:.0f}^2$ — like two features whose scales differ "
                    r"by 100×: $\partial f/\partial x$ is $10^4$ times larger than $\partial f/\partial y$. Minimum at $(1,1)$.")

    c1, c2, c3 = st.columns(3)
    lr_sgd = c1.select_slider("η for SGD & Momentum", LR_OPTIONS, lr_sgd_default, key=f"p91_lr_sgd_{tag}")
    lr_ad = c2.select_slider("η for AdaGrad / RMSProp / Adam", LR_OPTIONS, lr_ad_default, key=f"p91_lr_ad_{tag}")
    steps = c3.slider("Steps", 10, 2000, steps_default, 10, key=f"p91_steps_{tag}")
    with st.expander("Hyper-parameters (β, ρ, β₁, β₂, ε)"):
        h1, h2, h3, h4, h5 = st.columns(5)
        hp = {
            "beta": h1.slider("Momentum β", 0.0, 0.99, 0.9, 0.01, key="p91_beta"),
            "rho": h2.slider("RMSProp ρ", 0.5, 0.999, 0.9, 0.001, key="p91_rho"),
            "b1": h3.slider("Adam β₁", 0.0, 0.99, 0.9, 0.01, key="p91_b1"),
            "b2": h4.select_slider("Adam β₂", [0.9, 0.95, 0.99, 0.999, 0.9999], 0.999, key="p91_b2"),
            "eps": h5.select_slider("ε", EPS_OPTIONS, 1e-8, format_func=lambda e: f"{e:.0e}", key="p91_eps"),
        }
    chosen = st.multiselect("Optimizers", OPTIMIZERS, OPTIMIZERS, key="p91_opts")
    f, grad, x_star = make_landscape(name, kappa, angle)
    if not chosen:
        st.warning("Pick at least one optimizer to race.")
        return name, f, grad, x0, lr_ad, hp

    paths = {o: optimize(o, grad, x0, lr_sgd if o in ("SGD", "Momentum") else lr_ad, steps, hp) for o in chosen}
    x_lo, x_hi, y_lo, y_hi = box
    gx, gy = np.linspace(x_lo, x_hi, 150), np.linspace(y_lo, y_hi, 120)
    grid = np.stack(np.meshgrid(gx, gy), axis=-1)
    fig = go.Figure(go.Contour(x=gx, y=gy, z=np.log10(f(grid) + 1e-3), colorscale="Viridis", showscale=False,
                               ncontours=25, opacity=0.75, hoverinfo="skip"))
    for o, path in paths.items():
        shown = np.clip(path, [x_lo, y_lo], [x_hi, y_hi])
        fig.add_trace(go.Scatter(x=shown[:, 0], y=shown[:, 1], mode="lines+markers", name=o,
                                 line=dict(color=COLORS[o], width=2), marker=dict(size=3)))
    fig.add_trace(go.Scatter(x=[x_star[0]], y=[x_star[1]], mode="markers", name="minimum",
                             marker=dict(symbol="star", size=14, color="#fde047")))
    fig.update_layout(height=450, margin=dict(l=10, r=10, t=30, b=10), xaxis_range=[x_lo, x_hi], yaxis_range=[y_lo, y_hi],
                      legend=dict(orientation="h", y=1.08), xaxis_title="x", yaxis_title="y")
    loss_fig = go.Figure()
    rows = []
    for o, path in paths.items():
        losses = f(path)
        loss_fig.add_trace(go.Scatter(y=np.maximum(losses, 1e-16), mode="lines", name=o, line=dict(color=COLORS[o])))
        diverged = len(path) < steps + 1
        hit = np.nonzero(losses < 1e-6)[0]
        rows.append({"optimizer": o, "η": f"{lr_sgd if o in ('SGD', 'Momentum') else lr_ad:g}",
                     "final f": "diverged" if diverged else f"{losses[-1]:.2e}",
                     "distance to minimum": "—" if diverged else f"{np.linalg.norm(path[-1] - x_star):.3g}",
                     "first step with f < 1e-6": str(hit[0]) if hit.size else "not reached"})
    loss_fig.update_layout(height=450, margin=dict(l=10, r=10, t=30, b=10), yaxis_type="log", xaxis_title="step",
                           yaxis_title="f (log scale, floored at 1e-16)", legend=dict(orientation="h", y=1.08))
    left, right = st.columns([3, 2])
    left.plotly_chart(fig, width="stretch")
    right.plotly_chart(loss_fig, width="stretch")
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    with st.container(border=True):
        st.markdown(
            """**What to look for**
- *Badly scaled features*: SGD must keep η below 2/100 for the loud x-direction, so the quiet y-direction barely moves.
  RMSProp/Adam divide each gradient by its own size and walk almost straight to (1, 1).
- *Bowl*: with rotation 0° the stretch is axis-aligned and the adaptive methods fix it. Rotate to 45°: now **both**
  coordinates see a mix of steep and shallow, the per-coordinate denominators can no longer undo it, and the advantage
  shrinks or even reverses.
- *Rosenbrock*: plain SGD crawls along the curved valley floor; momentum and Adam make real progress.
- AdaGrad shares the adaptive η here; its denominator only grows, so its steps shrink like 1/√t and it stalls
  (it typically needs a larger η, e.g. 0.5–1).
- RMSProp with a constant η does not settle exactly: its steps stay ≈ η in size, so it hovers around the minimum."""
        )
    for o, path in paths.items():
        if len(path) < steps + 1:
            st.error(f"**{o}** diverged after {len(path) - 1} steps — lower its learning rate.")
    return name, f, grad, x0, lr_ad, hp


def adam_internals(name, grad, x0, lr, hp):
    st.header("🔢 Inside Adam — the first steps, number by number")
    coord = st.radio("Coordinate", ["x", "y"], horizontal=True, key="p91_coord")
    idx = 0 if coord == "x" else 1
    df = adam_trace(grad, x0, lr, 60, hp, idx)
    b1, b2, eps = hp["b1"], hp["b2"], hp["eps"]
    g1 = df["g"].iloc[0]
    st.markdown(f"Landscape **{name}**, start {x0}, η = {lr:g}, β₁ = {b1}, β₂ = {b2}, ε = {eps:.0e}. At t = 1 (m₀ = v₀ = 0):")
    st.latex(
        rf"m_1 = (1-\beta_1)g_1 = {df['m'].iloc[0]:.4g},\quad v_1 = (1-\beta_2)g_1^2 = {df['v'].iloc[0]:.4g},\quad "
        rf"\hat m_1 = g_1 = {df['m̂'].iloc[0]:.4g},\quad \hat v_1 = g_1^2 = {df['v̂'].iloc[0]:.4g}"
    )
    st.latex(
        rf"\Delta_1 = \eta\,\frac{{\hat m_1}}{{\sqrt{{\hat v_1}}+\varepsilon}} = \eta\,\frac{{g_1}}{{|g_1|+\varepsilon}} "
        rf"= {df['step / η'].iloc[0]:.4f}\,\eta \;\approx\; \eta\cdot\mathrm{{sign}}(g_1)"
    )
    if abs(g1) < 10 * eps:
        st.warning("Here |g₁| is not much larger than ε, so the first step is much smaller than η — ε is doing real work.")
    ratio = (1 - b1) / np.sqrt(1 - b2)
    st.markdown(
        rf"Without bias correction the first step would be $\eta\,\frac{{(1-\beta_1)g_1}}{{\sqrt{{1-\beta_2}}\,|g_1|}} "
        rf"= \frac{{1-\beta_1}}{{\sqrt{{1-\beta_2}}}}\,\eta = {ratio:.3f}\,\eta$ — "
        + ("**too large**" if ratio > 1 else "**too small**")
        + r" (with the defaults β₁ = 0.9, β₂ = 0.999 it is 3.16 η). Both running averages start at 0 and are biased toward 0; "
        r"dividing by $1-\beta^t$ removes exactly that bias (for a constant gradient, $\hat m_t = g$ and $\hat v_t = g^2$ for every t)."
    )
    show = df.head(10).copy()
    st.dataframe(show.style.format({c: "{:.4g}" for c in show.columns if c != "t"}), hide_index=True, width="stretch")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["t"], y=df["step / η"].abs(), mode="lines+markers", name="|step| / η with bias correction",
                             line=dict(color="#38bdf8")))
    fig.add_trace(go.Scatter(x=df["t"], y=df["no bias correction: step / η"].abs(), mode="lines+markers",
                             name="|step| / η without bias correction", line=dict(color="#f87171", dash="dash")))
    fig.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=10), xaxis_title="step t", yaxis_title="|step| / η",
                      legend=dict(orientation="h", y=1.15))
    st.plotly_chart(fig, width="stretch")
    st.caption("The two curves only meet once 1 − β₂ᵗ ≈ 1, i.e. after a few multiples of 1/(1−β₂) steps "
               "(the runs also drift apart because the positions differ). Note the step size stays near η "
               "whatever the gradient size: Adam's step is set by η, not by |g|.")


def myth_tab(hp):
    st.markdown(
        r"""**Myth:** *"Adam just takes steps of size η in the sign direction of the gradient."*
That is true for the very first step and roughly true when every recent gradient agrees. In general Adam divides a
**running average of gradients** by the **root of a running average of squared gradients**. For noisy gradients
$g_t = \mu + \sigma\xi_t$ this is about
$$\frac{\hat m_t}{\sqrt{\hat v_t}} \approx \frac{\mu}{\sqrt{\mu^2 + \sigma^2}},$$
a **signal-to-noise ratio**: consistent gradients get steps ≈ η, gradients that mostly flip sign get much smaller steps."""
    )
    seed = st.session_state.setdefault("p91_seed", 91)
    mu = st.slider("Signal μ (noise σ = 1)", 0.0, 3.0, 0.3, 0.05, key="p91_mu")
    b1, b2 = hp["b1"], hp["b2"]
    mus = np.round(np.linspace(0, 3, 31), 2)
    all_mu = np.append(mus, mu)
    rng = np.random.default_rng(seed)
    n_steps = 3000
    m = np.zeros(all_mu.size)
    v = np.zeros(all_mu.size)
    ratios = np.zeros((n_steps, all_mu.size))
    for t in range(1, n_steps + 1):
        g = all_mu + rng.standard_normal(all_mu.size)
        m = b1 * m + (1 - b1) * g
        v = b2 * v + (1 - b2) * g * g
        ratios[t - 1] = (m / (1 - b1**t)) / (np.sqrt(v / (1 - b2**t)) + hp["eps"])
    burn = n_steps // 3
    sim = ratios[burn:].mean(axis=0)
    left, right = st.columns(2)
    with left:
        fig = go.Figure(go.Scatter(y=ratios[:, -1], mode="lines", name="m̂/√v̂", line=dict(color="#38bdf8", width=1)))
        fig.add_hline(y=mu / np.sqrt(mu**2 + 1), line_dash="dot", annotation_text="μ/√(μ²+σ²)")
        fig.add_hline(y=1, line_color="#64748b", annotation_text="sign-descent would be ±1")
        fig.update_layout(height=320, margin=dict(l=10, r=10, t=30, b=10), xaxis_title="step t", yaxis_title="step / η",
                          title=f"μ = {mu:.2f}, σ = 1")
        st.plotly_chart(fig, width="stretch")
    with right:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=mus, y=mus / np.sqrt(mus**2 + 1), mode="lines", name="μ/√(μ²+1)", line=dict(color="#fde047")))
        fig.add_trace(go.Scatter(x=mus, y=sim[:-1], mode="markers", name="simulated mean of m̂/√v̂", marker=dict(color="#38bdf8")))
        fig.update_layout(height=320, margin=dict(l=10, r=10, t=30, b=10), xaxis_title="signal-to-noise μ/σ",
                          yaxis_title="average step / η", legend=dict(orientation="h", y=1.15))
        st.plotly_chart(fig, width="stretch")
    k1, k2 = st.columns(2)
    k1.metric("Average step / η (simulated)", f"{sim[-1]:.3f}")
    k2.metric("Prediction μ/√(μ²+σ²)", f"{mu / np.sqrt(mu**2 + 1):.3f}")
    st.caption(f"Averages over steps {burn}–{n_steps} with your β₁, β₂ (seed {seed}). With a short β₂ window (0.9) v̂ itself is noisy and the match is looser.")
    if st.button("🎲 Resample", key="p91_resample"):
        st.session_state["p91_seed"] = seed + 1
        st.rerun()


def adamw_tab():
    st.markdown(
        r"""With plain SGD, an L2 penalty $\tfrac{\lambda}{2}\|w\|^2$ and **weight decay** are the same thing:
$w \leftarrow w - \eta(g + \lambda w) = (1-\eta\lambda)\,w - \eta g$. In Adam they are **not**:

- **Adam + L2** adds $\lambda w$ to the gradient, so it also gets divided by $\sqrt{\hat v}$: weights with large gradient
  history are barely decayed, weights with tiny gradients are decayed hard.
- **AdamW** (Loshchilov & Hutter) *decouples* the decay: $w \leftarrow w - \eta\big(\tfrac{\hat m}{\sqrt{\hat v}+\varepsilon} + \lambda w\big)$,
  so every weight shrinks by the same factor $(1-\eta\lambda)$ per step, whatever its gradient scale.

Demo: two weights that the data does **not** need (their gradients are pure zero-mean noise) start at 1.
Weight A gets loud noise (σ = 10), weight B quiet noise (σ = 0.1). Ideal regularisation shrinks both alike."""
    )
    c1, c2 = st.columns(2)
    wd = c1.slider("λ (weight decay / L2 strength)", 0.0, 0.5, 0.1, 0.01, key="p91_wd")
    lr = c2.select_slider("η", [1e-3, 2e-3, 5e-3, 0.01, 0.02], 0.01, key="p91_wd_lr")
    seed = st.session_state.setdefault("p91_seed", 91)
    n_seeds, n_steps = 20, 2000
    sig = np.array([10.0, 0.1])
    curves = {}
    for mode in ("Adam + L2", "AdamW"):
        rng = np.random.default_rng(seed)
        w = np.ones((n_seeds, 2))
        m = np.zeros_like(w)
        v = np.zeros_like(w)
        hist = [np.abs(w).mean(axis=0)]
        for t in range(1, n_steps + 1):
            g = sig * rng.standard_normal(w.shape)
            if mode == "Adam + L2":
                g = g + wd * w
            m = 0.9 * m + 0.1 * g
            v = 0.999 * v + 0.001 * g * g
            step = (m / (1 - 0.9**t)) / (np.sqrt(v / (1 - 0.999**t)) + 1e-8)
            if mode == "AdamW":
                step = step + wd * w
            w = w - lr * step
            hist.append(np.abs(w).mean(axis=0))
        curves[mode] = np.array(hist)
    t = np.arange(n_steps + 1)
    fig = go.Figure()
    styles = {"Adam + L2": "dash", "AdamW": "solid"}
    for mode, hist in curves.items():
        fig.add_trace(go.Scatter(x=t, y=hist[:, 0], mode="lines", name=f"{mode}: A (σ = 10)", line=dict(color="#f87171", dash=styles[mode])))
        fig.add_trace(go.Scatter(x=t, y=hist[:, 1], mode="lines", name=f"{mode}: B (σ = 0.1)", line=dict(color="#38bdf8", dash=styles[mode])))
    fig.add_trace(go.Scatter(x=t, y=(1 - lr * wd) ** t, mode="lines", name="(1 − ηλ)ᵗ", line=dict(color="#fde047", dash="dot")))
    fig.update_layout(height=360, margin=dict(l=10, r=10, t=30, b=10), xaxis_title="step", yaxis_title="mean |w| over 20 seeded runs",
                      legend=dict(orientation="h", y=1.2))
    st.plotly_chart(fig, width="stretch")
    rows = [{"method": mode, "|A| at end (σ = 10)": f"{hist[-1, 0]:.3f}", "|B| at end (σ = 0.1)": f"{hist[-1, 1]:.3f}"} for mode, hist in curves.items()]
    rows.append({"method": "pure decay (1 − ηλ)^T", "|A| at end (σ = 10)": f"{(1 - lr * wd) ** n_steps:.3f}", "|B| at end (σ = 0.1)": f"{(1 - lr * wd) ** n_steps:.3f}"})
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    st.caption("AdamW shrinks A and B alike; they end slightly above (1 − ηλ)ᵀ because the noisy Adam steps keep jiggling them "
               "(mean |w| includes that jitter). Adam + L2 hardly regularises the loud weight A and crushes the quiet weight B to its noise level. "
               "In PyTorch, `Adam(weight_decay=λ)` is the L2 version; `AdamW(weight_decay=λ)` is decoupled.")


def ai_connection():
    st.header("🤖 Where this shows up in AI")
    st.markdown(
        r"""
- **AdamW is the default optimizer for transformers.** PyTorch defaults: `AdamW(lr=1e-3, betas=(0.9, 0.999), eps=1e-8, weight_decay=0.01)`.
- **LLM pretraining usually lowers β₂ to 0.95** (GPT-3, LLaMA, many others), with weight decay ≈ 0.1 and gradient clipping at 1.0.
  A shorter second-moment memory (≈ 20 steps instead of ≈ 1000) lets $\hat v$ react quickly when gradient magnitudes jump,
  instead of dividing a sudden large gradient by a stale small $\sqrt{\hat v}$ and taking a huge step (a common source of loss spikes).
- **ε** (10⁻⁸ by default; some large models use 10⁻⁶ – 10⁻⁵) sets the gradient size below which Adam stops normalising
  and behaves like SGD with rate η/ε. In low precision (fp16/bf16) a too-small ε can be numerically fragile.
- **Why AdamW for LLMs**: weight decay acts as intended (uniform shrinking, independent of gradient scale), and the best λ
  depends less on η. Biases and LayerNorm gains are commonly excluded from decay.
- **Memory**: Adam keeps two extra numbers (m, v) per parameter. For a 7-billion-parameter model in fp32 that is
  2 × 7·10⁹ × 4 bytes = **56 GB** just for optimizer state — one reason for sharded optimizers and 8-bit Adam variants.
- Vision CNNs often still use SGD + momentum 0.9 (page 90); transformers are hard to train with it, largely because
  gradient scales differ hugely between parameter groups — exactly the "badly scaled features" landscape above.
"""
    )


def takeaways():
    st.header("✅ Key takeaways")
    st.success("Adaptive optimizers give every parameter its own step size by dividing by the RMS of its recent gradients. "
               "Adam = momentum (β₁) + RMSProp (β₂) + bias correction.")
    st.markdown(
        r"""
- AdaGrad's sum only grows (steps die out); RMSProp/Adam use running averages that forget.
- Bias correction fixes the zero-initialised averages; without it the first Adam step would be off by the factor $\frac{1-\beta_1}{\sqrt{1-\beta_2}}$ (with the defaults and a steady gradient: 3.16× too big at t = 1 and ≈ 6.5× at t = 10).
- Adam's step ≈ η × (signal-to-noise of the gradient), not η × sign(g) in general.
- Per-coordinate scaling fixes axis-aligned badly-scaled problems, not rotated ill-conditioning.
- Use **AdamW** (decoupled weight decay), not Adam + L2, when you want weight decay.
"""
    )
    c1, c2 = st.columns(2)
    with c1:
        safe_page_link("pages/90Momentum.py", "← Previous: Momentum")
    with c2:
        safe_page_link("pages/92Learning-Rate Schedules.py", "Next: Learning-Rate Schedules →")


def main():
    intuition()
    name, _f, grad, x0, lr_ad, hp = lab()
    adam_internals(name, grad, x0, lr_ad, hp)
    st.header("🔬 Deeper labs")
    tab1, tab2 = st.tabs(["Myth: Adam is sign descent", "AdamW vs Adam + L2"])
    with tab1:
        myth_tab(hp)
    with tab2:
        adamw_tab()
    ai_connection()
    takeaways()


main()
