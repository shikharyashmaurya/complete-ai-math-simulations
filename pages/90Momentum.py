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

st.set_page_config(page_title="90 · Momentum", page_icon="🎳", layout="wide")

X0 = np.array([-4.0, 1.5])  # start of every optimizer in the valley lab
TOL = 1e-6  # "converged" once f(x_t) <= TOL * f(x_0)
MAX_STEPS = 5000
COLORS = {"Gradient descent": "#f87171", "Heavy-ball momentum": "#38bdf8", "Nesterov momentum": "#a3e635"}


# ---------------------------------------------------------------- optimizers on f = ½(a x² + b y²)
def run_quadratic(method, lam, eta, beta, steps):
    """Iterates of GD / heavy-ball / Nesterov on f = ½ Σ λ_i x_i² (diagonal Hessian ``lam``).

    Heavy-ball:  v ← β v − η ∇f(x),        x ← x + v
    Nesterov:    v ← β v − η ∇f(x + β v),  x ← x + v
    Stops early (and returns the shorter path) once the iterate blows up.
    """
    x = X0.copy()
    v = np.zeros(2)
    path = [x.copy()]
    for _ in range(steps):
        if method == "Gradient descent":
            x = x - eta * lam * x
        elif method == "Heavy-ball momentum":
            v = beta * v - eta * lam * x
            x = x + v
        else:
            v = beta * v - eta * lam * (x + beta * v)
            x = x + v
        if not np.all(np.isfinite(x)) or np.abs(x).max() > 1e8:
            break
        path.append(x.copy())
    return np.array(path)


def quad_f(path, lam):
    return 0.5 * (path**2 @ lam)


def steps_to_tol(method, lam, eta, beta):
    path = run_quadratic(method, lam, eta, beta, MAX_STEPS)
    rel = quad_f(path, lam) / quad_f(X0[None, :], lam)[0]
    hit = np.nonzero(rel <= TOL)[0]
    return int(hit[0]) if hit.size else None


def rate(method, lam_values, eta, beta):
    """Asymptotic contraction factor per step = max spectral radius over the eigen-directions."""
    radii = []
    for lam in lam_values:
        h = eta * lam
        if method == "Gradient descent":
            radii.append(abs(1 - h))
            continue
        if method == "Heavy-ball momentum":
            coeffs = [1.0, -(1 + beta - h), beta]  # z² − (1+β−ηλ) z + β
        else:
            coeffs = [1.0, -(1 + beta) * (1 - h), beta * (1 - h)]  # z² − (1+β)(1−ηλ) z + β(1−ηλ)
        radii.append(np.abs(np.roots(coeffs)).max())
    return float(max(radii))


def predicted_steps(rho):
    """f ∝ ρ^(2t) asymptotically, so f/f0 ≤ TOL after about ln(TOL) / (2 ln ρ) steps."""
    if rho >= 1:
        return "never (ρ ≥ 1)"
    if rho <= 1e-12:
        return "≈ 1–2"
    return f"≈ {np.log(TOL) / (2 * np.log(rho)):.0f}"


def valley_figure(lam, paths):
    span_x, span_y = 5.0, 2.5
    gx = np.linspace(-span_x, span_x, 160)
    gy = np.linspace(-span_y, span_y, 120)
    xx, yy = np.meshgrid(gx, gy)
    zz = np.log10(0.5 * (lam[0] * xx**2 + lam[1] * yy**2) + 1e-2)
    fig = go.Figure(go.Contour(x=gx, y=gy, z=zz, colorscale="Viridis", showscale=False, ncontours=22,
                               opacity=0.75, hoverinfo="skip"))
    for name, path in paths.items():
        shown = np.clip(path, [-span_x, -span_y], [span_x, span_y])
        fig.add_trace(go.Scatter(x=shown[:, 0], y=shown[:, 1], mode="lines+markers", name=name,
                                 line=dict(color=COLORS[name], width=2), marker=dict(size=4)))
    fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers", name="minimum",
                             marker=dict(symbol="star", size=14, color="#fde047")))
    fig.update_layout(height=430, margin=dict(l=10, r=10, t=30, b=10), legend=dict(orientation="h", y=1.08),
                      xaxis=dict(range=[-span_x, span_x], title="x (shallow, curvature a)"),
                      yaxis=dict(range=[-span_y, span_y], title="y (steep, curvature b)"))
    return fig


# ---------------------------------------------------------------- stability map (cached: it is a grid sweep)
@st.cache_data(show_spinner=False)
def stability_map(n_beta=67, n_h=91, steps=1600, window=1200):
    """Spectral radius of heavy-ball on f = ½λx², in theory (roots) and measured by simulation."""
    betas = np.linspace(0.0, 0.99, n_beta)
    hs = np.linspace(0.025, 4.5, n_h)
    bb, hh = np.meshgrid(betas, hs, indexing="ij")
    c = 1 + bb - hh
    disc = np.sqrt((c * c - 4 * bb).astype(complex))
    rho_theory = np.maximum(np.abs((c + disc) / 2), np.abs((c - disc) / 2))
    # Simulate x_{t+1} = (1+β−ηλ) x_t − β x_{t−1}, renormalising every step so nothing overflows,
    # and average the log growth over the last `window` steps.
    x, xp, acc = np.ones_like(bb), np.zeros_like(bb), np.zeros_like(bb)
    for t in range(steps):
        x, xp = c * x - bb * xp, x
        norm = np.hypot(x, xp)
        if t >= steps - window:
            acc += np.log(norm)
        x, xp = x / norm, xp / norm
    rho_sim = np.exp(acc / window)
    return betas, hs, rho_theory, rho_sim


# ---------------------------------------------------------------- bumpy 1-D landscape
DIP_C, DIP_A, DIP_S = -2.0, 0.6, 0.5


def bumpy_f(x):
    return 0.05 * (x - 3) ** 2 - DIP_A * np.exp(-((x - DIP_C) ** 2) / (2 * DIP_S**2))


def bumpy_df(x):
    return 0.1 * (x - 3) + DIP_A * (x - DIP_C) / DIP_S**2 * np.exp(-((x - DIP_C) ** 2) / (2 * DIP_S**2))


BARRIER_X = -1.082  # local maximum separating the shallow dip (x ≈ −1.78) from the global minimum (x = 3)


def run_bumpy(eta, beta, sigma, seed, n_runs, steps=600, x0=-6.0):
    """Heavy-ball on the bumpy curve with Gaussian gradient noise; all seeded runs at once (vectorised)."""
    rng = np.random.default_rng(seed)
    x = np.full(n_runs, x0)
    v = np.zeros(n_runs)
    path = [x.copy()]
    for _ in range(steps):
        g = bumpy_df(x) + sigma * rng.standard_normal(n_runs)
        v = beta * v - eta * g
        x = np.clip(x + v, -50, 50)
        path.append(x.copy())
    return np.array(path)


# ---------------------------------------------------------------- page sections
def intuition():
    st.title("🎳 Momentum — Rolling Instead of Stepping")
    st.markdown(
        r"""
Plain gradient descent (page 52) has **no memory**: every step looks only at the slope *right here*.
In a long, narrow valley that is a disaster. The steep walls dominate the gradient, so the walker bounces
from wall to wall (**zig-zag**) while crawling along the gentle valley floor.

**Momentum** gives the walker a velocity, like a heavy ball:
- slopes that **keep pointing the same way** (along the valley floor) add up, so the ball speeds up;
- slopes that **flip sign every step** (across the valley) cancel out, so the zig-zag is damped.
"""
    )
    c1, c2 = st.columns(2)
    with c1, st.container(border=True):
        st.markdown("**Heavy-ball (Polyak) momentum**")
        st.latex(r"v_{t+1} = \beta\, v_t - \eta\,\nabla f(x_t), \qquad x_{t+1} = x_t + v_{t+1}")
        st.caption("Equivalently x_{t+1} = x_t − η∇f(x_t) + β(x_t − x_{t−1}): a gradient step plus a fraction β of the last move.")
    with c2, st.container(border=True):
        st.markdown("**Nesterov momentum** (look ahead, then compute the gradient)")
        st.latex(r"v_{t+1} = \beta\, v_t - \eta\,\nabla f(x_t + \beta v_t), \qquad x_{t+1} = x_t + v_{t+1}")
        st.caption("The gradient is measured where the velocity is about to carry you, which brakes earlier before an overshoot.")


def valley_lab():
    st.header("🧪 Lab 1 — The narrow valley race")
    st.markdown(
        r"""The loss is the ill-conditioned bowl $f(x,y) = \tfrac12\,(a\,x^2 + b\,y^2)$ with $a = 1$ and
$b = \kappa$, so the **condition number** $\kappa = \lambda_{\max}/\lambda_{\min} = b/a$ says how much steeper
the walls are than the floor. The step size is set as $\eta\,\lambda_{\max}$: plain GD is stable only for
$\eta\,\lambda_{\max} < 2$ (the $\eta < 2/\lambda$ rule from page 53). All three optimizers start at $(-4,\ 1.5)$."""
    )
    c1, c2, c3, c4 = st.columns(4)
    kappa = c1.slider("Condition number κ = b / a", 1, 200, 50, key="p90_kappa")
    h_max = c2.slider("Step size η·λ_max", 0.05, 4.0, 1.3, 0.05, key="p90_hmax")
    beta = c3.slider("Momentum β", 0.0, 0.99, 0.9, 0.01, key="p90_beta")
    steps = c4.slider("Steps shown", 5, 300, 80, 5, key="p90_steps")
    lam = np.array([1.0, float(kappa)])
    eta = h_max / lam.max()
    st.caption(f"η = {h_max:.2f} / {kappa} = {eta:.4g}.  GD limit 2/λ_max = {2 / lam.max():.4g};  "
               f"heavy-ball limit 2(1+β)/λ_max = {2 * (1 + beta) / lam.max():.4g};  "
               f"Nesterov limit 2(1+β)/((1+2β)λ_max) = {2 * (1 + beta) / ((1 + 2 * beta) * lam.max()):.4g}.")

    methods = list(COLORS)
    paths = {m: run_quadratic(m, lam, eta, beta, steps) for m in methods}
    left, right = st.columns([3, 2])
    with left:
        st.plotly_chart(valley_figure(lam, paths), width="stretch")
    with right:
        f0 = quad_f(X0[None, :], lam)[0]
        fig = go.Figure()
        for name, path in paths.items():
            rel = np.maximum(quad_f(path, lam) / f0, 1e-300)
            fig.add_trace(go.Scatter(y=rel, mode="lines", name=name, line=dict(color=COLORS[name])))
        fig.add_hline(y=TOL, line_dash="dot", annotation_text="tolerance 1e-6")
        fig.update_layout(height=430, margin=dict(l=10, r=10, t=30, b=10), yaxis_type="log",
                          xaxis_title="step t", yaxis_title="f(x_t) / f(x_0)", legend=dict(orientation="h", y=1.08))
        st.plotly_chart(fig, width="stretch")

    for name, path in paths.items():
        if len(path) < steps + 1:
            st.error(f"**{name} diverged** after {len(path) - 1} steps — the step size is outside its stability region.")

    # Steps-to-tolerance table: your settings vs the textbook-optimal settings.
    mu, big_l = lam.min(), lam.max()
    eta_gd_opt = 2 / (mu + big_l)
    eta_hb_opt = 4 / (np.sqrt(big_l) + np.sqrt(mu)) ** 2
    beta_hb_opt = ((np.sqrt(kappa) - 1) / (np.sqrt(kappa) + 1)) ** 2
    rows = []
    for name in methods:
        rho = rate(name, lam, eta, beta)
        hit = steps_to_tol(name, lam, eta, beta)
        rows.append({"optimizer": name, "η": f"{eta:.4g}", "β": "—" if name == "Gradient descent" else f"{beta:.2f}",
                     "rate ρ (theory)": f"{rho:.4f}", "predicted steps": predicted_steps(rho),
                     "simulated steps to f/f₀ ≤ 1e-6": str(hit) if hit is not None else f"> {MAX_STEPS}"})
    for name, e, b in [("GD, optimal η = 2/(μ+L)", eta_gd_opt, 0.0), ("Heavy-ball, optimal η and β", eta_hb_opt, beta_hb_opt)]:
        method = "Gradient descent" if name.startswith("GD") else "Heavy-ball momentum"
        rho = rate(method, lam, e, b)
        hit = steps_to_tol(method, lam, e, b)
        rows.append({"optimizer": name, "η": f"{e:.4g}", "β": "—" if b == 0 else f"{b:.3f}",
                     "rate ρ (theory)": f"{rho:.4f}", "predicted steps": predicted_steps(rho),
                     "simulated steps to f/f₀ ≤ 1e-6": str(hit) if hit is not None else f"> {MAX_STEPS}"})
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    st.caption(
        rf"Theory: tuned GD contracts by $(\kappa-1)/(\kappa+1) = {(kappa - 1) / (kappa + 1):.4f}$ per step, tuned heavy-ball by "
        rf"$(\sqrt\kappa-1)/(\sqrt\kappa+1) = {(np.sqrt(kappa) - 1) / (np.sqrt(kappa) + 1):.4f}$ — the number of steps scales like "
        r"$\kappa$ for GD but only like $\sqrt{\kappa}$ with momentum. ρ is the largest root magnitude over both eigen-directions; "
        r"'predicted steps' uses only the asymptotic rate, so it is rough when the start is dominated by the fast direction or when roots repeat."
    )
    return lam, eta, beta


def worked_example(lam, eta, beta):
    st.header("🔢 Worked example — two heavy-ball steps with your numbers")
    x = X0.copy()
    v = np.zeros(2)
    lines = []
    for t in range(2):
        g = lam * x
        v_new = beta * v - eta * g
        x_new = x + v_new
        lines.append(
            r"\begin{aligned}"
            rf"\nabla f(x_{t}) &= ({g[0]:.3f},\ {g[1]:.3f}) \\ "
            rf"v_{t + 1} &= {beta:.2f}\,({v[0]:.3f},\ {v[1]:.3f}) - {eta:.4g}\,({g[0]:.3f},\ {g[1]:.3f}) = ({v_new[0]:.3f},\ {v_new[1]:.3f}) \\ "
            rf"x_{t + 1} &= x_{t} + v_{t + 1} = ({x_new[0]:.3f},\ {x_new[1]:.3f})"
            r"\end{aligned}"
        )
        x, v = x_new, v_new
    st.markdown(rf"Gradient $\nabla f(x,y) = (a\,x,\ b\,y) = ({lam[0]:.0f}\,x,\ {lam[1]:.0f}\,y)$, start $x_0 = (-4,\ 1.5)$, $v_0 = 0$.")
    for line in lines:
        st.latex(line)
    st.caption("Step 1 is an ordinary gradient step (v₀ = 0). From step 2 on, β times the previous move is added: "
               "in x the two terms point the same way and add up; in y the new gradient points back, so the two terms partly cancel.")


def ewa_tab():
    st.markdown(
        r"""Unroll the velocity: $v_{t} = -\eta \sum_{k\ge 0} \beta^{k}\, \nabla f(x_{t-1-k})$. Momentum is an
**exponentially weighted average** of past gradients (times $\tfrac{1}{1-\beta}$). The normalised average
$m_t = \beta m_{t-1} + (1-\beta) g_t$ gives weight $(1-\beta)\beta^k$ to the gradient from $k$ steps ago,
so it effectively remembers the last $\approx \frac{1}{1-\beta}$ steps."""
    )
    c1, c2, c3 = st.columns(3)
    beta = c1.slider("β for the average", 0.0, 0.99, 0.9, 0.01, key="p90_ewa_beta")
    amp = c2.slider("Zig-zag amplitude A", 0.0, 3.0, 2.0, 0.1, key="p90_ewa_amp")
    sigma = c3.slider("Noise σ", 0.0, 2.0, 0.5, 0.1, key="p90_ewa_sigma")
    seed = st.session_state.setdefault("p90_seed", 90)
    t = np.arange(200)
    rng = np.random.default_rng(seed)
    g = 1.0 + amp * (-1.0) ** t + sigma * rng.standard_normal(t.size)
    m = np.zeros_like(g)
    for i in range(t.size):
        m[i] = (beta * m[i - 1] if i else 0.0) + (1 - beta) * g[i]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=g, mode="lines", name="raw gradient g_t = 1 + A(−1)^t + noise", line=dict(color="#94a3b8", width=1)))
    fig.add_trace(go.Scatter(x=t, y=m, mode="lines", name="average m_t", line=dict(color="#38bdf8", width=3)))
    fig.add_hline(y=1.0, line_dash="dot", annotation_text="consistent part = 1")
    fig.update_layout(height=320, margin=dict(l=10, r=10, t=30, b=10), xaxis_title="step t", legend=dict(orientation="h", y=1.12))
    st.plotly_chart(fig, width="stretch")

    window = 1 / (1 - beta)
    n_win = max(1, int(round(window)))
    # Alternating component left in m: project the tail of m (after the start-up transient) on (−1)^t.
    tail = slice(150, 200)
    measured = abs(np.mean((m[tail] - np.mean(m[tail])) * (-1.0) ** t[tail])) if amp > 0 else 0.0
    theory = amp * (1 - beta) / (1 + beta)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Effective window 1/(1−β)", f"{window:.1f} steps")
    k2.metric(f"Weight on last {n_win} steps", f"{1 - beta**n_win:.1%}", help="1 − β^n; tends to 1 − 1/e ≈ 63% as β → 1")
    k3.metric("Zig-zag left (theory A(1−β)/(1+β))", f"{theory:.3f}")
    k4.metric("Zig-zag left (measured, seeded)", f"{measured:.3f}")
    st.caption(
        r"The constant part survives the averaging untouched while the alternating part shrinks by $(1-\beta)/(1+\beta)$ "
        r"— exactly what happens to the along-valley and across-valley gradients. Without the $(1-\beta)$ factor "
        r"(heavy-ball), a constant gradient builds a terminal velocity $\eta g/(1-\beta)$: the effective step is "
        r"$\eta/(1-\beta)$, i.e. **10×** for β = 0.9. Small differences between the two zig-zag metrics come from the noise."
    )
    if st.button("🎲 Resample noise", key="p90_resample"):
        st.session_state["p90_seed"] = seed + 1
        st.rerun()


def overshoot_tab():
    st.markdown(
        r"""On a single direction with curvature $\lambda$, heavy-ball follows
$x_{t+1} = (1+\beta-\eta\lambda)\,x_t - \beta\,x_{t-1}$. Its roots are complex (the ball **rings**) once
$\beta > (1-\sqrt{\eta\lambda})^2$, and they then have magnitude $\sqrt\beta$: large β means slow, wobbly decay."""
    )
    h = st.slider("η·λ for this direction", 0.01, 1.0, 0.05, 0.01, key="p90_os_h")
    betas = [0.0, 0.5, 0.9, 0.99]
    crit = (1 - np.sqrt(h)) ** 2
    fig = go.Figure()
    rows = []
    for b, color in zip(betas, ["#f87171", "#fbbf24", "#38bdf8", "#c084fc"]):
        x = [1.0, 1.0 - h]  # x_0 = 1, first step is a plain gradient step
        for _ in range(150):
            x.append((1 + b - h) * x[-1] - b * x[-2])
        x = np.array(x)
        fig.add_trace(go.Scatter(y=x, mode="lines", name=f"β = {b}", line=dict(color=color)))
        hit = np.nonzero(np.abs(x) < 1e-3)[0]
        settle = next((i for i in range(len(x)) if np.all(np.abs(x[i:]) < 1e-3)), None)
        rows.append({"β": b, "sign changes (overshoots)": int(np.sum(np.diff(np.sign(x[np.abs(x) > 1e-12])) != 0)),
                     "first |x| < 1e-3": str(hit[0]) if hit.size else "> 150",
                     "stays below 1e-3 from step": str(settle) if settle is not None else "> 150",
                     "root magnitude": f"{rate('Heavy-ball momentum', [1.0], h, b):.3f}"})
    fig.add_hline(y=0, line_color="#64748b")
    fig.update_layout(height=330, margin=dict(l=10, r=10, t=30, b=10), xaxis_title="step t", yaxis_title="x_t", legend=dict(orientation="h", y=1.12))
    st.plotly_chart(fig, width="stretch")
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    st.info(f"Critical damping for η·λ = {h:.2f} is β = (1 − √(ηλ))² = {crit:.3f}: the fastest non-ringing setting for this one direction. "
            "β = 0.99 keeps overshooting for a long time — too much momentum is like a ball on ice.")


def bumpy_tab(seed):
    st.markdown(
        r"""A 1-D loss with a **shallow dip** at $x \approx -1.78$ (barrier only $0.12$ high) on the way to the global
minimum at $x = 3$: $\;f(x) = 0.05(x-3)^2 - 0.6\,e^{-(x+2)^2/0.5}$. Both optimizers start at $x_0 = -6$ and
see noisy gradients $\nabla f + \sigma\,\xi_t$ (seeded)."""
    )
    c1, c2, c3 = st.columns(3)
    eta = c1.slider("η", 0.01, 0.3, 0.1, 0.01, key="p90_b_eta")
    beta = c2.slider("β (momentum run)", 0.0, 0.99, 0.9, 0.01, key="p90_b_beta")
    sigma = c3.slider("Gradient noise σ", 0.0, 1.0, 0.3, 0.05, key="p90_b_sigma")
    gd = run_bumpy(eta, 0.0, sigma, seed, 1)[:, 0]
    mom = run_bumpy(eta, beta, sigma, seed, 1)[:, 0]
    xs = np.linspace(-7, 6, 400)
    left, right = st.columns(2)
    with left:
        fig = go.Figure(go.Scatter(x=xs, y=bumpy_f(xs), mode="lines", name="f(x)", line=dict(color="#e2e8f0")))
        for name, path, color in [("GD (β = 0)", gd, "#f87171"), (f"momentum β = {beta:.2f}", mom, "#38bdf8")]:
            p = np.clip(path, -7, 6)
            fig.add_trace(go.Scatter(x=p, y=bumpy_f(p), mode="markers", name=name, marker=dict(color=color, size=5, opacity=0.5)))
            fig.add_trace(go.Scatter(x=[p[-1]], y=[bumpy_f(p[-1])], mode="markers", showlegend=False,
                                     marker=dict(color=color, size=16, symbol="x")))
        fig.update_layout(height=330, margin=dict(l=10, r=10, t=30, b=10), xaxis_title="x", yaxis_title="f(x)", legend=dict(orientation="h", y=1.12))
        st.plotly_chart(fig, width="stretch")
    with right:
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=gd, mode="lines", name="GD", line=dict(color="#f87171")))
        fig.add_trace(go.Scatter(y=mom, mode="lines", name="momentum", line=dict(color="#38bdf8")))
        fig.add_hline(y=BARRIER_X, line_dash="dot", annotation_text="barrier")
        fig.update_layout(height=330, margin=dict(l=10, r=10, t=30, b=10), xaxis_title="step t", yaxis_title="x_t", legend=dict(orientation="h", y=1.12))
        st.plotly_chart(fig, width="stretch")
    rows = []
    for b in sorted({0.0, 0.5, 0.8, 0.9, 0.95, 0.99, round(beta, 2)}):
        final = run_bumpy(eta, b, sigma, seed, 40)[-1]
        rows.append({"β": b, "runs past the barrier after 600 steps (of 40 seeds)": f"{np.mean(final > BARRIER_X):.0%}",
                     "mean final f": f"{np.mean(bumpy_f(final)):.3f}"})
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    st.caption("Momentum carries enough speed over the small bump; with β = 0 the walker stops in the first dip. "
               "This is not a guarantee: momentum can also roll *out* of a good basin, and very large β (0.99) "
               "may still be sloshing around after 600 steps.")
    if st.button("🎲 Resample noise", key="p90_resample_b"):
        st.session_state["p90_seed"] = seed + 1
        st.rerun()


def stability_tab(beta, h_max, h_min):
    st.markdown(
        r"""For one direction with curvature $\lambda$, heavy-ball is stable exactly when
$$0 \le \beta < 1 \quad\text{and}\quad 0 < \eta\lambda < 2(1+\beta), \qquad\text{i.e.}\quad \eta < \frac{2(1+\beta)}{\lambda}.$$
With $\beta=0$ this is page 53's $\eta < 2/\lambda$; momentum **widens** the stable range up to $\eta < 4/\lambda$.
The map shows the largest root magnitude $\rho$ (theory), and we check it by simulating 1,600 steps at every grid point."""
    )
    betas, hs, rho_t, rho_s = stability_map()
    agree = np.mean((rho_t < 1) == (rho_s < 1))
    fig = go.Figure(go.Heatmap(x=hs, y=betas, z=np.minimum(rho_t, 1.5), colorscale="RdYlGn_r", zmin=0, zmax=1.5,
                               colorbar=dict(title="ρ"), hovertemplate="ηλ=%{x:.2f}<br>β=%{y:.2f}<br>ρ=%{z:.3f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=2 * (1 + betas), y=betas, mode="lines", name="ηλ = 2(1+β)", line=dict(color="white", width=3, dash="dash")))
    fig.add_trace(go.Scatter(x=[h_max, h_min], y=[beta, beta], mode="markers+text", name="Lab 1 directions",
                             text=["λ_max", "λ_min"], textposition="top center",
                             marker=dict(size=12, color="#38bdf8", line=dict(color="white", width=2))))
    fig.update_layout(height=420, margin=dict(l=10, r=10, t=30, b=10), xaxis_title="η·λ", yaxis_title="β",
                      xaxis_range=[0, 4.5], legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig, width="stretch")
    c1, c2, c3 = st.columns(3)
    c1.metric("Grid points where simulation agrees with ηλ < 2(1+β)", f"{agree:.2%}")
    c2.metric("Max |ρ_theory − ρ_simulated|", f"{np.max(np.abs(rho_t - rho_s)):.4f}")
    stable = h_max < 2 * (1 + beta)
    c3.metric("Lab 1 heavy-ball", "stable" if stable else "unstable", help=f"η·λ_max = {h_max:.2f} vs limit 2(1+β) = {2 * (1 + beta):.2f}")
    st.caption(
        r"Nesterov's look-ahead buys smoother convergence but a *smaller* stable range: the same root test gives "
        r"$0 < \eta\lambda < \frac{2(1+\beta)}{1+2\beta}$ (≈ 1.36 for β = 0.9). Push Lab 1 to η·λ_max = 1.6 with β = 0.9 "
        r"and only the Nesterov run blows up."
    )


def ai_connection():
    st.header("🤖 Where this shows up in AI")
    st.markdown(
        r"""
- **SGD + momentum with β = 0.9** is the classic recipe for CNNs: ResNet on ImageNet was trained with
  SGD, momentum 0.9, learning rate 0.1 (decayed), weight decay $10^{-4}$. It is still a strong default for vision models.
- **PyTorch** writes it as `buf = β·buf + g`, `w -= lr·buf` (`torch.optim.SGD(params, lr, momentum=0.9, nesterov=False)`).
  That is the same algorithm as above with $v = -\eta\,\text{buf}$; `nesterov=True` switches on the look-ahead version.
- Because a consistent gradient is amplified by $1/(1-\beta)$, changing β also changes the **effective learning rate**
  $\eta/(1-\beta)$ — practitioners re-tune η when they change β.
- Mini-batch noise (page 56) is averaged by the same EWA, which is why momentum steadies SGD.
- **Adam** (next page) keeps exactly this kind of running average of gradients (its $\beta_1 = 0.9$) and adds a second
  running average of squared gradients to pick a step size per parameter.
"""
    )


def takeaways():
    st.header("✅ Key takeaways")
    st.success(
        "Momentum = gradient step + β × last move. It averages gradients over ≈ 1/(1−β) steps, damping zig-zags "
        "and accelerating along consistent directions."
    )
    st.markdown(
        r"""
- On a bowl with condition number $\kappa$, tuned GD needs $O(\kappa)$ steps, tuned momentum $O(\sqrt{\kappa})$.
- Heavy-ball is stable for $0 < \eta\lambda < 2(1+\beta)$ — wider than GD's $\eta\lambda < 2$.
- Too much β overshoots and rings (root magnitude $\sqrt\beta$); speed can carry you over small bumps — or past good minima.
"""
    )
    c1, c2 = st.columns(2)
    with c1:
        safe_page_link("pages/56Stochastic Gradient Descent.py", "← Previous: Stochastic Gradient Descent")
    with c2:
        safe_page_link("pages/91RMSProp & Adam.py", "Next: RMSProp & Adam →")


def main():
    intuition()
    lam, eta, beta = valley_lab()
    worked_example(lam, eta, beta)
    st.header("🔬 Deeper labs")
    tabs = st.tabs(["Exponentially weighted average", "Too much momentum", "Escaping a shallow dip", "Stability region"])
    with tabs[0]:
        ewa_tab()
    with tabs[1]:
        overshoot_tab()
    with tabs[2]:
        bumpy_tab(st.session_state.setdefault("p90_seed", 90))
    with tabs[3]:
        stability_tab(beta, eta * lam.max(), eta * lam.min())
    ai_connection()
    takeaways()


main()
