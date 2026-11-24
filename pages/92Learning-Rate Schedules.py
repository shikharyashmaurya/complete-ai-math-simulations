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
from common.mathutils import sigmoid  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="92 · Learning-Rate Schedules", page_icon="📉", layout="wide")

SCHEDULES = ["Constant", "Step decay", "Exponential", "Cosine", "Warmup + cosine", "1-cycle", "Inverse √t (Transformer)"]
COLORS = dict(zip(SCHEDULES, ["#f87171", "#fbbf24", "#a3e635", "#38bdf8", "#c084fc", "#fb923c", "#2dd4bf"]))
N_DATA = 400


# ---------------------------------------------------------------- schedules
def schedule(name, T, eta_max, warmup, min_ratio, every, gamma, pct):
    """η(t) for t = 0 … T−1 (η(t) is the rate used for update t)."""
    t = np.arange(T, dtype=float)
    eta_min = eta_max * min_ratio
    W = max(1, min(warmup, T // 2))
    if name == "Constant":
        return np.full(T, eta_max)
    if name == "Step decay":
        return eta_max * gamma ** np.floor(t / every)
    if name == "Exponential":
        return eta_max * min_ratio ** (t / max(T - 1, 1))
    if name == "Cosine":
        return eta_min + 0.5 * (eta_max - eta_min) * (1 + np.cos(np.pi * t / max(T - 1, 1)))
    if name == "Warmup + cosine":
        cos = eta_min + 0.5 * (eta_max - eta_min) * (1 + np.cos(np.pi * (t - W) / max(T - 1 - W, 1)))
        return np.where(t < W, eta_max * (t + 1) / W, cos)
    if name == "1-cycle":  # PyTorch OneCycleLR defaults: div_factor 25, final_div_factor 1e4, cosine annealing
        p = max(1, int(round(pct * T)))
        lo = eta_max / 25
        final = lo / 1e4
        up = lo + (eta_max - lo) * 0.5 * (1 - np.cos(np.pi * t / p))
        down = final + (eta_max - final) * 0.5 * (1 + np.cos(np.pi * (t - p) / max(T - 1 - p, 1)))
        return np.where(t < p, up, down)
    s = t + 1  # inverse square root: linear warmup to η_max at step W, then ∝ 1/√t
    return eta_max * np.minimum(s / W, np.sqrt(W / s))


# ---------------------------------------------------------------- tiny model: logistic regression
@st.cache_data(show_spinner=False)
def make_data(seed):
    rng = np.random.default_rng(seed)
    y = rng.integers(0, 2, N_DATA).astype(float)
    centers = np.where(y[:, None] == 1, [1.0, 0.5], [-1.0, -0.5])
    X = centers + rng.normal(size=(N_DATA, 2)) * [1.2, 1.0]
    X = np.c_[np.ones(N_DATA), X]
    # Exact optimum by Newton's method (the classes overlap, so it exists).
    w = np.zeros(3)
    for _ in range(50):
        p = sigmoid(X @ w)
        hess = (X * (p * (1 - p))[:, None]).T @ X / N_DATA
        w = w - np.linalg.solve(hess + 1e-12 * np.eye(3), X.T @ (p - y) / N_DATA)
    p = sigmoid(X @ w)
    hess = (X * (p * (1 - p))[:, None]).T @ X / N_DATA
    big_l = np.linalg.eigvalsh(X.T @ X / (4 * N_DATA)).max()  # σ'(z) ≤ 1/4, so this bounds the curvature everywhere
    return X, y, w, full_loss(w[None, :], X, y)[0], big_l, np.linalg.eigvalsh(hess).max()


def full_loss(W, X, y):
    """Mean logistic loss for every row of W (stable: log(1+e^z) − y z)."""
    Z = W @ X.T
    return np.mean(np.logaddexp(0, Z) - y * Z, axis=1)


@st.cache_data(show_spinner=False)
def train_all(T, eta_max, warmup, min_ratio, every, gamma, pct, batch, seed):
    X, y, _w, l_star, _l, _h = make_data(seed)
    rng = np.random.default_rng(seed + 1000)
    batches = rng.integers(0, N_DATA, size=(T, batch))  # identical mini-batches for every schedule
    out = {}
    for name in SCHEDULES:
        etas = schedule(name, T, eta_max, warmup, min_ratio, every, gamma, pct)
        w = np.zeros(3)
        hist = np.empty((T + 1, 3))
        hist[0] = w
        for t in range(T):
            xb, yb = X[batches[t]], y[batches[t]]
            w = w - etas[t] * xb.T @ (sigmoid(xb @ w) - yb) / batch
            hist[t + 1] = w
        out[name] = np.maximum(full_loss(hist, X, y) - l_star, 1e-12)
    return out


# ---------------------------------------------------------------- page sections
def intuition():
    st.title("📉 Learning-Rate Schedules — Big Steps First, Small Steps Later")
    st.markdown(
        r"""
One fixed learning rate is a compromise. **Early** in training you are far from any minimum and want big steps.
**Late** in training, with mini-batch noise (page 56), big steps make the weights rattle around the minimum: the loss
stops improving at a **noise floor** whose height is proportional to η. A **schedule** $\eta(t)$ gets both:
- **decay** (step, exponential, cosine…) lowers the noise floor at the end;
- **warmup** starts with tiny steps, because the start of training is where the loss is often the most curved
  and the optimizer statistics are the least reliable — remember page 53: a step is stable only if $\eta < 2/\lambda$.
"""
    )


def schedule_lab():
    st.header("🧪 Lab 1 — Seven schedules")
    c1, c2, c3, c4 = st.columns(4)
    eta_max = c1.select_slider("Peak rate η_max", [0.1, 0.2, 0.5, 1.0, 2.0, 3.0, 5.0, 8.0, 12.0, 20.0], 2.0, key="p92_eta")
    T = c2.slider("Total steps T", 100, 2000, 600, 50, key="p92_T")
    warmup = c3.slider("Warmup steps W", 1, 300, 30, 1, key="p92_W")
    min_ratio = c4.select_slider("Final rate η_min / η_max", [0.001, 0.01, 0.05, 0.1, 0.2], 0.01, key="p92_min")
    c1, c2, c3, c4 = st.columns(4)
    every = c1.slider("Step decay: every … steps", 10, 1000, 200, 10, key="p92_every")
    gamma = c2.slider("Step decay: factor γ", 0.05, 0.9, 0.1, 0.05, key="p92_gamma")
    pct = c3.slider("1-cycle: fraction rising", 0.05, 0.9, 0.3, 0.05, key="p92_pct")
    log_y = c4.toggle("Log scale for η", value=False, key="p92_log")
    if warmup > T // 2:
        st.caption(f"Warmup is capped at T/2 = {T // 2} steps.")
    seed = st.session_state.setdefault("p92_seed", 92)
    _X, _y, _w, _ls, big_l, lam_star = make_data(seed)
    shown = st.multiselect("Schedules to show", SCHEDULES, SCHEDULES, key="p92_show")
    params = (T, eta_max, warmup, min_ratio, every, gamma, pct)
    fig = go.Figure()
    for name in shown:
        fig.add_trace(go.Scatter(y=schedule(name, *params), mode="lines", name=name, line=dict(color=COLORS[name], width=2)))
    fig.add_hline(y=2 / big_l, line_dash="dot", line_color="#e2e8f0",
                  annotation_text=f"2/L = {2 / big_l:.2f} (full-batch GD always descends below this)")
    fig.update_layout(height=380, margin=dict(l=10, r=10, t=30, b=10), xaxis_title="step t", yaxis_title="η(t)",
                      yaxis_type="log" if log_y else "linear", legend=dict(orientation="h", y=1.15))
    if not shown:
        st.info("Select at least one schedule to plot.")
    else:
        st.plotly_chart(fig, width="stretch")
    with st.expander("Formulas (t = 0 … T−1)"):
        st.latex(r"\text{step: } \eta_{\max}\,\gamma^{\lfloor t/s\rfloor}\qquad \text{exponential: } \eta_{\max}\,r^{\,t/(T-1)},\ r = \eta_{\min}/\eta_{\max}")
        st.latex(r"\text{cosine: } \eta_{\min} + \tfrac12(\eta_{\max}-\eta_{\min})\big(1+\cos\tfrac{\pi t}{T-1}\big)\qquad "
                 r"\text{warmup: } \eta_{\max}\tfrac{t+1}{W}\ \ (t<W),\ \text{then cosine over the rest}")
        st.latex(r"\text{inverse-}\sqrt{t}:\ \eta_{\max}\min\!\Big(\tfrac{t+1}{W},\ \sqrt{\tfrac{W}{t+1}}\Big) \quad"
                 r"\big(\text{Transformer: } d_{\text{model}}^{-1/2}\min(\text{step}^{-1/2},\ \text{step}\cdot W^{-3/2})\big)")
        st.latex(r"\text{1-cycle: cosine from } \tfrac{\eta_{\max}}{25} \text{ up to } \eta_{\max} \text{ over the rising fraction, then cosine down to } \tfrac{\eta_{\max}}{25\cdot 10^4}")
    return params, seed, big_l, lam_star


def worked_example(params):
    st.header("🔢 Worked example — η at a few checkpoints")
    T, eta_max, warmup, min_ratio = params[:4]
    checkpoints = sorted({0, min(max(1, min(warmup, T // 2)), T - 1), T // 4, T // 2, 3 * T // 4, T - 1})
    table = {"t": checkpoints}
    for name in SCHEDULES:
        etas = schedule(name, *params)
        table[name] = [f"{etas[c]:.4g}" for c in checkpoints]
    st.dataframe(pd.DataFrame(table), hide_index=True, width="stretch")
    W = max(1, min(warmup, T // 2))
    t = T // 2
    eta_min = eta_max * min_ratio
    value = schedule("Warmup + cosine", *params)[t]
    st.latex(
        rf"\eta({t}) = \eta_{{\min}} + \tfrac12(\eta_{{\max}}-\eta_{{\min}})\Big(1+\cos\frac{{\pi({t}-{W})}}{{{T}-1-{W}}}\Big)"
        rf"= {eta_min:.4g} + \tfrac12({eta_max:g}-{eta_min:.4g})\big(1+\cos({np.pi * (t - W) / max(T - 1 - W, 1):.3f})\big) = {value:.4g}"
    )


def training_lab(params, seed, big_l, lam_star):
    st.header("🏋️ Lab 2 — Train the same tiny model under every schedule")
    st.markdown(
        r"""Logistic regression (bias + 2 features, 400 seeded points with overlapping classes) trained by mini-batch SGD.
Every schedule sees **exactly the same mini-batches**, so differences come only from $\eta(t)$. We plot the
**excess loss** $L(w_t) - L(w^{\star})$ where $w^{\star}$ is the exact optimum (found with Newton's method)."""
    )
    c1, c2 = st.columns([3, 1])
    batch = c1.select_slider("Mini-batch size B (smaller = noisier)", [1, 2, 4, 8, 16, 32, 64, 400], 4, key="p92_batch")
    if c2.button("🎲 Resample data & batches", key="p92_resample"):
        st.session_state["p92_seed"] = seed + 1
        st.rerun()
    curves = train_all(*params, batch, seed)
    fig = go.Figure()
    for name, curve in curves.items():
        fig.add_trace(go.Scatter(y=curve, mode="lines", name=name, line=dict(color=COLORS[name], width=1.5)))
    fig.update_layout(height=420, margin=dict(l=10, r=10, t=30, b=10), yaxis_type="log", xaxis_title="step t",
                      yaxis_title="excess loss L(w_t) − L(w*)", legend=dict(orientation="h", y=1.12))
    st.plotly_chart(fig, width="stretch")
    T = params[0]
    tail = max(1, T // 10)
    rows = [{"schedule": n, "final excess loss": c[-1], f"mean over last {tail} steps": c[-tail:].mean(),
             "largest one-step rise": max(float(np.max(np.diff(c))), 0.0)}
            for n, c in curves.items()]
    df = pd.DataFrame(rows).sort_values(f"mean over last {tail} steps")
    st.dataframe(df.style.format({c: "{:.2e}" for c in df.columns if c != "schedule"}), hide_index=True, width="stretch")
    st.caption(
        f"Curvature check (page 53): this loss is never more curved than L = λ_max(XᵀX)/(4N) = {big_l:.3f}, so full-batch GD "
        f"decreases the loss for any η < 2/L = {2 / big_l:.2f}. At the optimum the curvature is only λ_max(H*) = {lam_star:.3f} "
        f"(2/λ = {2 / lam_star:.1f}): flatter regions tolerate larger steps. Mini-batches add noise on top, which is what the decay fights."
    )
    if params[1] > 2 / big_l:
        st.warning(f"η_max = {params[1]:g} is above 2/L = {2 / big_l:.2f}: a step is no longer guaranteed to lower the loss, so it can jump up "
                   "while η is near its peak. Schedules that decay recover once η drops; the constant one cannot.")


def noise_floor_tab():
    st.markdown(
        r"""Take the simplest noisy problem: $f(w) = \tfrac12\lambda w^2$ with gradient estimates $\lambda w + \sigma\xi_t$.
Constant-η SGD $w_{t+1} = (1-\eta\lambda)w_t - \eta\sigma\xi_t$ never settles; its variance stops at
$V = \frac{\eta\sigma^2}{\lambda(2-\eta\lambda)}$, so the **excess loss floor** is
$$\mathbb{E}\big[\tfrac12\lambda w^2\big] = \frac{\eta\,\sigma^2}{2\,(2-\eta\lambda)} \;\approx\; \frac{\eta\sigma^2}{4}\quad(\text{for small }\eta\lambda).$$
Halving η halves the floor — that is the whole point of decaying the rate."""
    )
    c1, c2, c3 = st.columns(3)
    eta = c1.slider("η", 0.01, 2.5, 0.4, 0.01, key="p92_nf_eta")
    lam = c2.slider("Curvature λ", 0.5, 3.0, 1.0, 0.1, key="p92_nf_lam")
    sigma = c3.slider("Gradient noise σ", 0.1, 3.0, 1.0, 0.1, key="p92_nf_sigma")
    if eta * lam >= 2:
        st.error(f"η·λ = {eta * lam:.2f} ≥ 2: even without noise the iterates blow up (η < 2/λ = {2 / lam:.2f} is required). Lower η.")
        return
    seed = st.session_state.setdefault("p92_seed", 92)
    T, chains = 1500, 400
    t = np.arange(T, dtype=float)
    runs = {"constant η": np.full(T, eta), "constant η/2": np.full(T, eta / 2),
            "cosine from η to η/100": eta / 100 + 0.5 * (eta - eta / 100) * (1 + np.cos(np.pi * t / (T - 1)))}
    fig = go.Figure()
    rows = []
    for (name, etas), color in zip(runs.items(), ["#f87171", "#fbbf24", "#38bdf8"]):
        rng = np.random.default_rng(seed)  # same noise for all three runs
        w = np.full(chains, 3.0)
        loss = np.empty(T)
        for i in range(T):
            w = (1 - etas[i] * lam) * w - etas[i] * sigma * rng.standard_normal(chains)
            loss[i] = np.mean(0.5 * lam * w**2)
        fig.add_trace(go.Scatter(y=loss, mode="lines", name=name, line=dict(color=color)))
        theory = etas[-1] * sigma**2 / (2 * (2 - etas[-1] * lam))
        rows.append({"run": name, "η at the end": f"{etas[-1]:.4g}", "measured loss (last 300 steps, 400 chains)": f"{loss[-300:].mean():.4f}",
                     "floor formula at final η": f"{theory:.4f}" if name != "cosine from η to η/100" else f"{theory:.4f} (only if η changes slowly)"})
        if name == "constant η":
            fig.add_hline(y=theory, line_dash="dot", line_color=color, annotation_text="ησ²/(2(2−ηλ))")
    fig.update_layout(height=340, margin=dict(l=10, r=10, t=30, b=10), yaxis_type="log", xaxis_title="step t",
                      yaxis_title="mean excess loss ½λw²", legend=dict(orientation="h", y=1.15))
    st.plotly_chart(fig, width="stretch")
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    st.caption("The cosine run moves fast while η is big and then sinks below the constant-η floors as η shrinks; "
               "at the very end it lags slightly above its own tiny-η floor because w needs time ≈ 1/(ηλ) to equilibrate.")


def warmup_tab():
    st.markdown(
        r"""**Why warmup?** Use a toy loss whose curvature is high at the start and low near the minimum:
$f(w) = \tfrac12 a w^2 + \tfrac14 w^4$ with $a = 1$. A gradient step multiplies $w$ by exactly
$1 - \eta\,(a + w^2)$, so $|w|$ **grows** whenever $\eta\,(a + w^2) > 2$ — page 53's rule with curvature
$k(w) = a + w^2$ (for a quadratic, $k$ is just λ). Starting at $w_0$, a constant rate must obey
$\eta < 2/(a + w_0^2)$, far smaller than the $\eta < 2/a$ that is fine near the minimum. Warmup ramps η up while $w$
moves into the flat region."""
    )
    c1, c2, c3 = st.columns(3)
    w0 = c1.slider("Start w₀", 0.5, 4.0, 3.0, 0.1, key="p92_wu_w0")
    eta_max = c2.slider("Target rate η_max", 0.05, 1.9, 0.5, 0.05, key="p92_wu_eta")
    W = c3.slider("Warmup steps", 1, 100, 20, 1, key="p92_wu_W")
    a, T = 1.0, 120
    limit0 = 2 / (a + w0**2)
    runs = {}
    for name, etas in [("constant η_max", np.full(T, eta_max)),
                       (f"linear warmup over {W} steps", eta_max * np.minimum(1.0, np.arange(1, T + 1) / W))]:
        w = w0
        ws, risk = [w0], []
        for e in etas:
            risk.append(e * (a + w * w))
            w = w * (1 - e * (a + w * w))
            if not np.isfinite(w) or abs(w) > 1e6:
                break
            ws.append(w)
        runs[name] = (np.array(ws), np.array(risk), etas)
    left, right = st.columns(2)
    with left:
        fig = go.Figure()
        for (name, (ws, _r, _e)), color in zip(runs.items(), ["#f87171", "#38bdf8"]):
            fig.add_trace(go.Scatter(y=np.maximum(np.abs(ws), 1e-16), mode="lines+markers", name=name, line=dict(color=color), marker=dict(size=4)))
        fig.update_layout(height=330, margin=dict(l=10, r=10, t=30, b=10), yaxis_type="log", xaxis_title="step t",
                          yaxis_title="|w_t| (log)", legend=dict(orientation="h", y=1.15))
        st.plotly_chart(fig, width="stretch")
    with right:
        fig = go.Figure()
        for (name, (_w, risk, _e)), color in zip(runs.items(), ["#f87171", "#38bdf8"]):
            fig.add_trace(go.Scatter(y=np.minimum(risk, 50), mode="lines+markers", name=name, line=dict(color=color), marker=dict(size=4)))
        fig.add_hline(y=2, line_dash="dot", annotation_text="η·k(w) = 2: above this |w| grows")
        fig.update_layout(height=330, margin=dict(l=10, r=10, t=30, b=10), xaxis_title="step t", yaxis_title="η_t · (a + w_t²)",
                          legend=dict(orientation="h", y=1.15))
        st.plotly_chart(fig, width="stretch")
    k1, k2, k3 = st.columns(3)
    for col, (name, (ws, risk, _e)) in zip((k1, k2), runs.items()):
        diverged = len(ws) < T + 1
        col.metric(name, "diverged 💥" if diverged else f"|w| = {abs(ws[-1]):.1e}",
                   help=f"largest η·k(w) seen: {risk.max():.2f}" if risk.size else None)
    k3.metric("Constant-rate limit at the start 2/(a + w₀²)", f"{limit0:.3f}")
    st.caption("Constant η diverges exactly when η_max > 2/(a + w₀²) (equality just bounces between ±w₀). "
               "Deep networks show the same pattern: the early loss surface is sharp and the weights quickly move to flatter regions, "
               "and Adam's v̂ is still a poor estimate during the first steps.")


def lr_finder_tab(seed, big_l):
    st.markdown(
        r"""**Learning-rate finder** (range test): run a short training where η grows exponentially every step, record the
(smoothed) loss and look where it falls fastest and where it explodes. A common rule picks a peak rate about 10× below
the blow-up point. Here: 200 mini-batch steps (B = 16) on the logistic-regression model, η from $10^{-3}$ to $10^{2}$."""
    )
    X, y, _w, l_star, _l, _h = make_data(seed)
    rng = np.random.default_rng(seed + 7)
    K = 200
    etas = 1e-3 * 1e5 ** (np.arange(K) / (K - 1))
    w = np.zeros(3)
    smooth, avg = [], 0.0
    for k, e in enumerate(etas):
        b = rng.integers(0, N_DATA, 16)
        z = X[b] @ w
        avg = 0.9 * avg + 0.1 * np.mean(np.logaddexp(0, z) - y[b] * z)
        smooth.append(avg / (1 - 0.9 ** (k + 1)))
        w = w - e * X[b].T @ (sigmoid(z) - y[b]) / 16
    smooth = np.array(smooth)
    best = int(np.argmin(smooth))
    fig = go.Figure(go.Scatter(x=etas, y=smooth, mode="lines", name="smoothed mini-batch loss", line=dict(color="#38bdf8")))
    fig.add_vline(x=etas[best], line_dash="dot", annotation_text=f"lowest loss at η ≈ {etas[best]:.2g}")
    fig.add_vline(x=2 / big_l, line_dash="dash", line_color="#fbbf24", annotation_text="2/L", annotation_position="bottom right")
    fig.add_hline(y=l_star, line_dash="dot", line_color="#64748b", annotation_text="optimal loss L*")
    fig.update_layout(height=330, margin=dict(l=10, r=10, t=30, b=10), xaxis_type="log", xaxis_title="η (growing every step)",
                      yaxis_title="smoothed loss")
    st.plotly_chart(fig, width="stretch")
    st.caption(f"Suggested peak ≈ {etas[best] / 10:.2g} … {etas[best]:.2g}. The test is noisy (try 🎲 Resample in Lab 2): it gives a ballpark, not an exact optimum.")


def ai_connection():
    st.header("🤖 Where this shows up in AI")
    st.markdown(
        r"""
- **LLM pretraining = linear warmup + cosine decay** (with AdamW, page 91). GPT-3 warmed up over the first 375M tokens and
  decayed with a cosine to 10% of the peak; LLaMA used 2,000 warmup steps and a cosine down to 10%. Some newer runs use
  "warmup–stable–decay": a long constant phase and a short final decay.
- **The original Transformer** used the inverse-square-root schedule with 4,000 warmup steps:
  $\eta = d_{\text{model}}^{-1/2}\min(\text{step}^{-1/2},\ \text{step}\cdot 4000^{-3/2})$.
- **ResNet-era CNNs** used step decay (÷10 at fixed epochs) with SGD + momentum; **1-cycle** (Smith) trains many vision
  models in fewer epochs and is built into PyTorch as `OneCycleLR`.
- **Learning-rate finders** (Smith's range test, popularised by fastai) pick η_max before a long run.
- Why decay matters: mini-batch noise sets a loss floor ∝ η. Why warmup matters: early curvature is high (and Adam's
  statistics are unreliable), so the η < 2/λ rule allows only small steps at first.
"""
    )


def takeaways():
    st.header("✅ Key takeaways")
    st.success("Schedule η(t): warm up while the loss is sharp, run near the peak while far from the minimum, decay to shrink the SGD noise floor.")
    st.markdown(
        r"""
- Constant-η SGD stalls at an excess loss ≈ ησ²/4 — decay lowers it.
- A step is stable only if η < 2/λ for the *current* curvature; warmup respects this when early curvature is large.
- Warmup + cosine (LLMs), inverse √t (original Transformer), step decay & 1-cycle (CNNs) are all variations on the same idea.
"""
    )
    c1, c2 = st.columns(2)
    with c1:
        safe_page_link("pages/91RMSProp & Adam.py", "← Previous: RMSProp & Adam")
    with c2:
        safe_page_link("pages/57Information & Surprise.py", "Next: Information & Surprise →")


def main():
    intuition()
    params, seed, big_l, lam_star = schedule_lab()
    worked_example(params)
    training_lab(params, seed, big_l, lam_star)
    st.header("🔬 Deeper labs")
    tab1, tab2, tab3 = st.tabs(["Why decay: the noise floor", "Why warmup: an instability demo", "Learning-rate finder"])
    with tab1:
        noise_floor_tab()
    with tab2:
        warmup_tab()
    with tab3:
        lr_finder_tab(seed, big_l)
    ai_connection()
    takeaways()


main()
