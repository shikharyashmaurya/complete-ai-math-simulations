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
from common.mathutils import fmt_factor, fmt_num  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="55 · Convex Functions", page_icon="🥣", layout="wide")

DOMAIN = (-3.0, 3.0)
FUNCS = {
    "x² — parabola (convex)": "sq",
    "|x| — kink (convex, not differentiable at 0)": "abs",
    "eˣ — exponential (convex, no minimum!)": "exp",
    "x⁴ — flat bottom (convex, f''(0) = 0)": "quart",
    "softplus log(1 + eˣ) (convex)": "softplus",
    "sin x (not convex)": "sin",
    "x³ (not convex)": "cube",
    "x⁴ − 3x² + x — double well (not convex)": "well",
}
TOL = 1e-9


def f(kind, x):
    x = np.asarray(x, dtype=float)
    if kind == "sq":
        return x**2
    if kind == "abs":
        return np.abs(x)
    if kind == "exp":
        return np.exp(x)
    if kind == "quart":
        return x**4
    if kind == "softplus":
        return np.logaddexp(0.0, x)
    if kind == "sin":
        return np.sin(x)
    if kind == "cube":
        return x**3
    return x**4 - 3 * x**2 + x


def f2(kind, x):
    """Analytic second derivative (NaN where it does not exist)."""
    x = np.asarray(x, dtype=float)
    if kind == "sq":
        return np.full_like(x, 2.0)
    if kind == "abs":
        return np.where(x == 0, np.nan, 0.0)
    if kind == "exp":
        return np.exp(x)
    if kind == "quart":
        return 12 * x**2
    if kind == "softplus":
        s = 1.0 / (1.0 + np.exp(-x))
        return s * (1 - s)
    if kind == "sin":
        return -np.sin(x)
    if kind == "cube":
        return 6 * x
    return 12 * x**2 - 6


def worst_chord_violation(kind, n_grid=61):
    """Max over a grid of a, b, λ of f(λa + (1−λ)b) − [λf(a) + (1−λ)f(b)] (≤ 0 everywhere iff convex on the grid)."""
    g = np.linspace(*DOMAIN, n_grid)
    a, b, lam = np.meshgrid(g, g, np.linspace(0, 1, 11), indexing="ij")
    gap = f(kind, lam * a + (1 - lam) * b) - (lam * f(kind, a) + (1 - lam) * f(kind, b))
    idx = np.unravel_index(int(np.argmax(gap)), gap.shape)
    return float(gap[idx]), float(a[idx]), float(b[idx])


def style(fig, title, xt, yt, height=380):
    fig.update_layout(
        template="plotly_dark", title=title, height=height, xaxis_title=xt, yaxis_title=yt,
        margin=dict(l=10, r=10, t=50, b=10), legend=dict(orientation="h", y=-0.22),
    )
    return fig


def intuition():
    st.title("🥣 Page 55: Convex Functions")
    st.markdown(
        r"""
On page 54 the loss landscape had several valleys, and gradient descent could get stuck in the wrong one.
A **convex** function is the landscape where that *cannot* happen: it is a single bowl. Formally, $f$ is convex if the
straight line (**chord**) between any two points of its graph never dips below the graph:

$$f\big(\lambda a + (1-\lambda) b\big) \;\le\; \lambda f(a) + (1-\lambda) f(b) \qquad \text{for all } a, b \text{ and } \lambda\in[0,1].$$

Convexity is the property that turns "optimisation" from hopeful search into a **guarantee**: every local minimum is
global, and gradient descent with a small enough step provably gets there.
"""
    )


def chord_lab():
    st.header("🧪 Lab 1: the chord test, Jensen and the second derivative")
    name = st.selectbox("Function", list(FUNCS), key="p55_func")
    kind = FUNCS[name]
    xs = np.linspace(*DOMAIN, 401)
    t1, t2, t3 = st.tabs(["Chord test", "Jensen's inequality", "Second-derivative test"])
    with t1:
        c1, c2, c3 = st.columns(3)
        a = c1.slider("Point a", -3.0, 3.0, -2.0, 0.1, key="p55_a")
        b = c2.slider("Point b", -3.0, 3.0, 2.5, 0.1, key="p55_b")
        lam = c3.slider("Weight λ on a", 0.0, 1.0, 0.3, 0.05, key="p55_lam")
        m = lam * a + (1 - lam) * b
        fm, chord = float(f(kind, m)), lam * float(f(kind, a)) + (1 - lam) * float(f(kind, b))
        lams = np.linspace(0, 1, 201)
        mix = lams * a + (1 - lams) * b
        gap = f(kind, mix) - (lams * f(kind, a) + (1 - lams) * f(kind, b))
        bad = gap > TOL * max(1.0, float(np.max(np.abs(f(kind, mix)))))
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=xs, y=f(kind, xs), mode="lines", line=dict(color="#4ECDC4", width=3), name="f(x)"))
        fig.add_trace(go.Scatter(x=[a, b], y=[f(kind, a), f(kind, b)], mode="lines+markers", line=dict(color="#FFD166", width=2), marker=dict(size=10), name="chord"))
        if bad.any():
            fig.add_trace(go.Scatter(x=mix[bad], y=f(kind, mix[bad]), mode="markers", marker=dict(size=5, color="#FF6B6B"), name="graph ABOVE chord (violation)"))
        fig.add_trace(go.Scatter(x=[m, m], y=[fm, chord], mode="lines+markers", line=dict(color="white", dash="dot"), marker=dict(size=9, symbol=["circle", "diamond"]), name="f(mix) vs chord"))
        st.plotly_chart(style(fig, f"{name}: chord between a = {fmt_num(a, 1)} and b = {fmt_num(b, 1)}", "x", "f(x)"), width="stretch")
        st.latex(
            rf"f(\lambda a+(1-\lambda)b) = f({fmt_num(m, 3)}) = {fmt_num(fm, 4)} \;\;" + (r"\le" if fm <= chord + TOL * max(1.0, abs(chord)) else r"\mathbf{>}")
            + rf"\;\; \lambda f(a)+(1-\lambda)f(b) = {fmt_num(lam, 2)}\cdot{fmt_factor(float(f(kind, a)), 3)} + {fmt_num(1 - lam, 2)}\cdot{fmt_factor(float(f(kind, b)), 3)} = {fmt_num(chord, 4)}"
        )
        if abs(a - b) < 1e-12:
            st.info("a = b: the chord shrinks to a single point and the inequality holds with equality. Move the sliders apart.")
        worst, wa, wb = worst_chord_violation(kind)
        if worst > TOL:
            st.error(f"Not convex on [−3, 3]: the worst chord found (a = {fmt_num(wa, 1)}, b = {fmt_num(wb, 1)}) lies {fmt_num(worst, 3)} below the graph. Try those values.")
        else:
            st.success("Scanned 61 × 61 pairs (a, b) × 11 weights λ on [−3, 3]: no chord ever dips below the graph — consistent with convexity.")
    with t2:
        jensen_tab(kind, name, xs)
    with t3:
        second_derivative_tab(kind, name, xs)


def jensen_tab(kind, name, xs):
    st.markdown(
        r"""
The chord inequality with many points and weights is **Jensen's inequality**: for convex $f$ and any random variable $X$,
$$f(\mathbb E[X]) \;\le\; \mathbb E[f(X)].$$
Below, $X$ is uniform over $K$ sampled points. The average of the points $(x_i, f(x_i))$ (★) lies inside their convex hull, which sits above a convex graph.
"""
    )
    st.session_state.setdefault("p55_seed", 55)
    c1, c2, c3, c4 = st.columns([1, 1, 1, 0.8])
    k = c1.slider("Number of points K", 1, 50, 6, key="p55_k")
    mu = c2.slider("Centre", -2.0, 2.0, 0.5, 0.1, key="p55_mu_j")
    sd = c3.slider("Spread", 0.0, 1.5, 1.0, 0.1, key="p55_sd")
    c4.write("")
    if c4.button("🎲 Resample", key="p55_resample"):
        st.session_state["p55_seed"] += 1
    rng = np.random.default_rng(st.session_state["p55_seed"])
    pts = np.clip(mu + sd * rng.standard_normal(k), *DOMAIN)
    fx = f(kind, pts)
    xbar, ef, fe = float(pts.mean()), float(fx.mean()), float(f(kind, pts.mean()))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=f(kind, xs), mode="lines", line=dict(color="#4ECDC4", width=3), name="f(x)"))
    fig.add_trace(go.Scatter(x=pts, y=fx, mode="markers", marker=dict(size=9, color="#FFD166"), name="(xᵢ, f(xᵢ))"))
    fig.add_trace(go.Scatter(x=[xbar], y=[ef], mode="markers", marker=dict(size=16, symbol="star", color="white"), name="(E[X], E[f(X)])"))
    fig.add_trace(go.Scatter(x=[xbar], y=[fe], mode="markers", marker=dict(size=12, color="#FF6B6B"), name="(E[X], f(E[X]))"))
    st.plotly_chart(style(fig, f"Jensen on {name}", "x", "f(x)"), width="stretch")
    gap = ef - fe
    m1, m2, m3 = st.columns(3)
    m1.metric("f(E[X])", fmt_num(fe, 4))
    m2.metric("E[f(X)]", fmt_num(ef, 4))
    m3.metric("Jensen gap E[f(X)] − f(E[X])", fmt_num(gap, 4), "≥ 0 ✓" if gap >= -TOL else "< 0: f is not convex here", delta_color="normal" if gap >= -TOL else "inverse")
    if k == 1 or sd == 0:
        st.caption("With a single distinct value there is no randomness: E[f(X)] = f(E[X]) and the gap is exactly 0.")
    st.caption("In AI: Jensen gives KL ≥ 0 (page 60) and the evidence lower bound (ELBO) of VAEs, since log is concave: log E[·] ≥ E[log ·].")


def second_derivative_tab(kind, name, xs):
    st.markdown(
        r"""
For a twice-differentiable $f$ on an interval: **$f$ is convex ⇔ $f''(x) \ge 0$ everywhere** (the slope never decreases).
$f''>0$ everywhere is enough for *strict* convexity but not required: $x^4$ is strictly convex although $f''(0)=0$.
"""
    )
    d2 = f2(kind, xs)
    neg = np.where(d2 < -TOL, d2, np.nan)
    fig = go.Figure()
    fig.add_hline(y=0, line=dict(color="white", dash="dot"))
    fig.add_trace(go.Scatter(x=xs, y=d2, mode="lines", line=dict(color="#a78bfa", width=3), name="f''(x)"))
    fig.add_trace(go.Scatter(x=xs, y=neg, mode="lines", fill="tozeroy", line=dict(color="#FF6B6B"), name="f'' < 0 (concave part)"))
    st.plotly_chart(style(fig, f"Second derivative of {name}", "x", "f''(x)", height=320), width="stretch")
    probe = np.linspace(-2.9, 2.9, 7)
    h = 1e-3
    fd = (f(kind, probe + h) - 2 * f(kind, probe) + f(kind, probe - h)) / h**2
    st.dataframe(pd.DataFrame({"x": probe, "analytic f''(x)": f2(kind, probe), "finite difference": fd}).round(4), width="stretch", hide_index=True)
    if kind == "abs":
        st.info("|x| has f'' = 0 away from 0 and no second derivative at the kink — the f'' test does not apply there, but the chord test still proves convexity.")


def hessian_lab():
    st.header("🧪 Lab 2: convexity in 2D — the Hessian must be PSD")
    st.markdown(
        r"""
For $f(\mathbf v) = \tfrac12 \mathbf v^\top H \mathbf v$ the Hessian is the constant matrix $H$. In any dimension, a twice-differentiable
$f$ is convex ⇔ its Hessian is **positive semidefinite** (all eigenvalues $\ge 0$) everywhere: the curvature is non-negative
in *every* direction. Choose the eigenvalues (curvatures along the two principal axes) and rotate the axes.
"""
    )
    c1, c2, c3 = st.columns(3)
    l1 = c1.slider("Eigenvalue λ₁", -3.0, 3.0, 2.0, 0.5, key="p55_l1")
    l2 = c2.slider("Eigenvalue λ₂", -3.0, 3.0, 0.5, 0.5, key="p55_l2")
    theta = c3.slider("Rotation of axes (°)", 0, 180, 30, 5, key="p55_theta")
    th = np.deg2rad(theta)
    R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    H = R @ np.diag([l1, l2]) @ R.T
    ev = np.linalg.eigvalsh(H)
    lo, hi = float(ev[0]), float(ev[1])
    lo, hi = (0.0 if abs(lo) < TOL else lo), (0.0 if abs(hi) < TOL else hi)
    if lo > 0:
        shape, verdict = "Bowl", "✅ strictly convex (H positive definite) — one unique minimum"
    elif lo == 0 and hi > 0:
        shape, verdict = "Trough / valley", "✅ convex but not strictly (H PSD and singular) — a whole line of minima"
    elif lo == 0 and hi == 0:
        shape, verdict = "Flat plane", "✅ convex (and concave) — every point is a minimum"
    elif lo < 0 < hi:
        shape, verdict = "Saddle", "❌ not convex — downhill in one direction, uphill in the other"
    elif hi == 0:
        shape, verdict = "Ridge", "❌ not convex (concave ridge) — a line of maxima"
    else:
        shape, verdict = "Dome", "❌ not convex (concave) — a maximum, no minimum"
    g = np.linspace(-2, 2, 41)
    X, Y = np.meshgrid(g, g)
    Z = 0.5 * (H[0, 0] * X**2 + 2 * H[0, 1] * X * Y + H[1, 1] * Y**2)
    fig = go.Figure(go.Surface(x=X, y=Y, z=Z, colorscale="Viridis", showscale=False))
    fig.update_layout(template="plotly_dark", title=f"{shape}: f(v) = ½ vᵀHv", height=440, margin=dict(l=0, r=0, t=40, b=0))
    left, right = st.columns([1.4, 1])
    left.plotly_chart(fig, width="stretch")
    with right:
        st.latex(rf"H = \begin{{bmatrix}} {fmt_num(H[0, 0], 3)} & {fmt_num(H[0, 1], 3)} \\ {fmt_num(H[1, 0], 3)} & {fmt_num(H[1, 1], 3)} \end{{bmatrix}}")
        st.latex(rf"\text{{eig}}(H) = {fmt_num(lo, 3)},\; {fmt_num(hi, 3)}")
        det, tr = float(np.linalg.det(H)), float(np.trace(H))
        st.latex(rf"\det H = {fmt_num(det, 3)} = \lambda_1\lambda_2,\quad \operatorname{{tr}} H = {fmt_num(tr, 3)} = \lambda_1+\lambda_2")
        st.caption("2×2 PSD check without eigenvalues: H₁₁ ≥ 0, H₂₂ ≥ 0 and det H ≥ 0.")
        st.markdown(f"**{shape}** — {verdict}")


def local_global_section():
    st.header("🎯 Every local minimum of a convex function is global")
    st.markdown(
        r"""
**Why:** suppose $x^*$ is a local minimum but some $y$ has $f(y) < f(x^*)$. The chord inequality gives, for every small $t>0$,
$f(x^* + t(y-x^*)) \le (1-t)f(x^*) + t f(y) < f(x^*)$ — points arbitrarily close to $x^*$ are lower, contradicting "local minimum".
Below: plain gradient descent ($\eta = 0.1$, 300 steps) from 9 starting points on a convex and on a page-54-style non-convex curve.
"""
    )
    starts = np.linspace(-3.5, 3.5, 9)
    cases = {
        "Convex: log cosh(x − 1) + 0.1x²": (lambda x: np.log(np.cosh(x - 1)) + 0.1 * x**2, lambda x: np.tanh(x - 1) + 0.2 * x),
        "Non-convex: 0.1x⁴ − 0.8x² + 0.3x": (lambda x: 0.1 * x**4 - 0.8 * x**2 + 0.3 * x, lambda x: 0.4 * x**3 - 1.6 * x + 0.3),
    }
    cols = st.columns(2)
    xs = np.linspace(-3.8, 3.8, 300)
    for col, (title, (fun, grad)) in zip(cols, cases.items()):
        x = starts.copy()
        for _ in range(300):
            x = x - 0.1 * grad(x)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=xs, y=fun(xs), mode="lines", line=dict(color="#4ECDC4", width=3), name="f"))
        fig.add_trace(go.Scatter(x=starts, y=fun(starts), mode="markers", marker=dict(size=8, color="#94a3b8"), name="starts"))
        fig.add_trace(go.Scatter(x=x, y=fun(x), mode="markers", marker=dict(size=13, color="#FFD166", symbol="x"), name="where GD stops"))
        col.plotly_chart(style(fig, title, "x", "f(x)", height=320), width="stretch")
        ends = np.unique(np.round(x, 3))
        col.caption(f"Distinct end points: {', '.join(fmt_num(v, 3) for v in ends)} → f = {', '.join(fmt_num(float(fun(v)), 3) for v in ends)}")


def ml_examples():
    st.header("🤖 Convex and non-convex losses in machine learning")
    m = np.linspace(-3, 3, 301)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=m, y=(m <= 0).astype(float), mode="lines", line=dict(color="#94a3b8", dash="dot"), name="0–1 loss (not convex)"))
    fig.add_trace(go.Scatter(x=m, y=np.maximum(0, 1 - m), mode="lines", line=dict(color="#FFD166"), name="hinge max(0, 1 − m)"))
    fig.add_trace(go.Scatter(x=m, y=np.logaddexp(0, -m) / np.log(2), mode="lines", line=dict(color="#4ECDC4"), name="logistic log₂(1 + e⁻ᵐ)"))
    fig.add_trace(go.Scatter(x=m, y=(1 - m) ** 2, mode="lines", line=dict(color="#FF6B6B"), name="squared (1 − m)²"))
    fig.update_yaxes(range=[-0.2, 4.5])
    left, right = st.columns([1.1, 1])
    left.plotly_chart(style(fig, "Classification losses vs margin m = y·z (y = ±1)", "margin m", "loss", height=360), width="stretch")
    right.dataframe(
        pd.DataFrame(
            {
                "objective": ["MSE of linear regression", "Logistic loss (logistic regression)", "Hinge loss (linear SVM)", "L2 penalty ‖w‖²", "L1 penalty ‖w‖₁", "Neural-network loss"],
                "convex in the weights?": ["✅ Hessian 2XᵀX/n is PSD", "✅", "✅ (not differentiable at m = 1)", "✅ strongly convex", "✅ not strictly, kink at 0", "❌ in general"],
            }
        ),
        width="stretch", hide_index=True,
    )
    right.caption("A composition 'convex loss ∘ linear model' stays convex. Put a non-linear hidden layer in between and convexity is lost.")
    st.markdown(
        r"""
**A concrete proof that a tiny network is non-convex.** Take $\hat y = v_1\tanh(w_1x) + v_2\tanh(w_2x)$ and data generated by
$\theta_A = (w_1,w_2,v_1,v_2) = (2,-1,1,0.5)$, so $\text{MSE}(\theta_A)=0$. Swapping the two hidden units gives
$\theta_B = (-1,2,0.5,1)$ — the *same* function, so $\text{MSE}(\theta_B)=0$ too. A convex loss would have to be $\le 0$ on the whole chord between them:
"""
    )
    xs = np.linspace(-3, 3, 50)
    th_a, th_b = np.array([2.0, -1.0, 1.0, 0.5]), np.array([-1.0, 2.0, 0.5, 1.0])

    def net(th):
        return th[2] * np.tanh(th[0] * xs) + th[3] * np.tanh(th[1] * xs)

    target = net(th_a)
    s = np.linspace(0, 1, 101)
    loss = np.array([np.mean((net((1 - si) * th_a + si * th_b) - target) ** 2) for si in s])
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=s, y=loss, mode="lines", line=dict(color="#FF6B6B", width=3), name="MSE along the segment"))
    fig2.add_trace(go.Scatter(x=[0, 1], y=[loss[0], loss[-1]], mode="lines+markers", line=dict(color="#FFD166", dash="dash"), name="chord (= 0)"))
    st.plotly_chart(style(fig2, f"Loss at the midpoint = {fmt_num(float(loss[50]), 4)} > 0 = chord → not convex", "s  (θ = (1 − s)·θ_A + s·θ_B)", "MSE", height=320), width="stretch")


def gd_lab():
    st.header("🧪 Lab 3: gradient descent's guarantee — η < 2/L")
    st.markdown(
        r"""
$f$ is **$L$-smooth** if its curvature never exceeds $L$ (for a twice-differentiable $f$: all Hessian eigenvalues $\le L$).
Then one GD step $x^+ = x - \eta\nabla f(x)$ satisfies the *descent lemma*
$f(x^+) \le f(x) - \eta\left(1 - \tfrac{L\eta}{2}\right)\|\nabla f(x)\|^2$, so the loss **always decreases when $0<\eta<2/L$**.
For convex $f$ and $\eta \le 1/L$: $\;f(x_k) - f^* \le \dfrac{\|x_0 - x^*\|^2}{2\eta k}$. If $f$ is also **$\mu$-strongly convex**
(curvature $\ge \mu > 0$), convergence is geometric. On page 53 the curvature was $\lambda = 2$, hence $\eta < 2/\lambda = 1$ — the same rule.
Test it on $f(x,y) = \tfrac12(Lx^2 + \mu y^2)$, started at $(2.5, 2.5)$:
"""
    )
    c1, c2, c3, c4 = st.columns(4)
    L_in = c1.slider("Smoothness L (steepest curvature)", 0.5, 10.0, 4.0, 0.5, key="p55_L")
    mu_in = c2.slider("Strong convexity μ (flattest curvature)", 0.0, 10.0, 1.0, 0.5, key="p55_mu")
    b1, b2 = c3.columns(2)
    b1.button("η = 1/L", key="p55_set_inv", on_click=_set_eta, args=("inv",))
    b2.button("η = 2/(L+μ)", key="p55_set_opt", on_click=_set_eta, args=("opt",))
    st.session_state.setdefault("p55_eta", 0.3)  # value lives in session state so the η buttons can set it
    eta = c3.slider("Learning rate η", 0.01, 1.5, step=0.01, key="p55_eta")
    iters = c4.slider("Iterations", 5, 80, 30, key="p55_iters")
    L, mu = max(L_in, mu_in), min(L_in, mu_in)
    if mu_in > L_in:
        st.caption(f"μ > L was chosen; by definition L is the larger curvature, so we use L = {fmt_num(L, 1)}, μ = {fmt_num(mu, 1)}.")
    p0 = np.array([2.5, 2.5])
    curv = np.array([L, mu])
    path, diverged = [p0], False
    for _ in range(iters):
        nxt = path[-1] * (1 - eta * curv)
        path.append(nxt)
        if np.max(np.abs(nxt)) > 1e6:
            diverged = True
            break
    path = np.array(path)
    fvals = 0.5 * (L * path[:, 0] ** 2 + mu * path[:, 1] ** 2)
    eL = eta * L
    if np.isclose(eL, 2.0):
        regime = "🏓 η = 2/L exactly: the steep coordinate flips sign forever and never converges."
    elif eL > 2.0:
        regime = f"💥 η > 2/L = {fmt_num(2 / L, 3)}: each step multiplies the steep coordinate by |1 − ηL| = {fmt_num(abs(1 - eL), 3)} > 1 — divergence."
    elif eL > 1.0 and not np.isclose(eL, 1.0):
        regime = f"〰️ 1/L < η < 2/L: overshoots and zig-zags across the valley, but still converges (|1 − ηL| = {fmt_num(abs(1 - eL), 3)} < 1)."
    elif np.isclose(eL, 1.0):
        regime = "🎯 η = 1/L: the steep coordinate reaches 0 in a single step."
    else:
        regime = f"🐢 η < 1/L: smooth, monotone approach (factor 1 − ηL = {fmt_num(1 - eL, 3)} per step)."
    (st.error if eL >= 2.0 or np.isclose(eL, 2.0) else st.success)(regime)

    g = np.linspace(-3.5, 3.5, 81)
    GX, GY = np.meshgrid(g, g)
    fig = go.Figure(go.Contour(x=g, y=g, z=0.5 * (L * GX**2 + mu * GY**2), colorscale="Viridis", showscale=False, contours=dict(coloring="lines")))
    fig.add_trace(go.Scatter(x=path[:, 0], y=path[:, 1], mode="lines+markers", line=dict(color="#FFD166"), marker=dict(size=6), name="GD path"))
    fig.update_xaxes(range=[-3.5, 3.5])
    fig.update_yaxes(range=[-3.5, 3.5])
    k = np.arange(len(fvals))
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=k, y=np.maximum(fvals, 1e-16), mode="lines+markers", line=dict(color="#FF6B6B"), name="f(x_k) − f*"))
    if eta <= 1.0 / L + 1e-12:
        kk = k[1:]
        fig2.add_trace(go.Scatter(x=kk, y=float(p0 @ p0) / (2 * eta * kk), mode="lines", line=dict(color="#4ECDC4", dash="dash"), name="bound ‖x₀−x*‖²/(2ηk)"))
    fig2.update_yaxes(type="log")
    l, r = st.columns(2)
    l.plotly_chart(style(fig, "Path on the contours of f", "x  (curvature L)", "y  (curvature μ)"), width="stretch")
    r.plotly_chart(style(fig2, "Loss gap per iteration (log scale)", "iteration k", "f(x_k) − f*"), width="stretch")

    rho = max(abs(1 - eta * L), abs(1 - eta * mu))
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Speed limit 2/L", fmt_num(2 / L, 3))
    m2.metric("Decrease factor η(1 − Lη/2)", fmt_num(eta * (1 - L * eta / 2), 3), "positive ⇒ guaranteed descent" if eL < 2 else "≤ 0 ⇒ no guarantee", delta_color="off")
    m3.metric("Contraction ρ = max|1 − η·curv|", fmt_num(rho, 3))
    m4.metric("Final f(x_k)", "diverged" if diverged else f"{fvals[-1]:.2e}")
    if mu > 0:
        kappa = L / mu
        st.caption(f"Condition number κ = L/μ = {fmt_num(kappa, 2)}. Best fixed step η* = 2/(L+μ) = {fmt_num(2 / (L + mu), 3)} gives ρ = (κ−1)/(κ+1) = {fmt_num((kappa - 1) / (kappa + 1), 3)}; with η = 1/L, f(x_k) − f* ≤ (1 − μ/L)ᵏ·(f(x₀) − f*).")
    else:
        st.caption("μ = 0: f does not depend on y, so y never moves — convex but not strongly convex; the loss still converges, but only along the x-direction.")
    worked_example(eta, L, mu, path, fvals)


def _set_eta(mode):
    L_in, mu_in = st.session_state.get("p55_L", 4.0), st.session_state.get("p55_mu", 1.0)
    L, mu = max(L_in, mu_in), min(L_in, mu_in)
    value = 1.0 / L if mode == "inv" else 2.0 / (L + mu)
    st.session_state["p55_eta"] = float(np.clip(round(value, 2), 0.01, 1.5))


def worked_example(eta, L, mu, path, fvals):
    st.subheader("🔢 Worked example (live)")
    st.latex(r"\nabla f(x,y) = (Lx,\ \mu y) \;\Rightarrow\; x_{k+1} = (1-\eta L)\,x_k,\quad y_{k+1} = (1-\eta\mu)\,y_k")
    lines = []
    for i in range(min(3, len(path) - 1)):
        x0, y0 = path[i]
        x1, y1 = path[i + 1]
        lines.append(
            rf"x_{{{i + 1}}} = (1 - {fmt_num(eta, 2)}\cdot{fmt_num(L, 1)})\cdot{fmt_factor(x0, 4)} = {fmt_num(x1, 4)},\quad "
            rf"y_{{{i + 1}}} = (1 - {fmt_num(eta, 2)}\cdot{fmt_num(mu, 1)})\cdot{fmt_factor(y0, 4)} = {fmt_num(y1, 4)},\quad f = {fmt_num(fvals[i + 1], 4)}"
        )
    for line in lines:
        st.latex(line)


def ai_connection():
    st.header("🧠 Why this matters in real models")
    c1, c2 = st.columns(2)
    with c1.container(border=True):
        st.markdown(
            r"""
**Convex models come with guarantees.** Linear/logistic regression, linear SVMs and LASSO/ridge are convex: any solver that
reaches a point with zero (sub)gradient has found a global optimum, results are reproducible, and the learning-rate rule
$\eta < 2/L$ (with $L$ the largest Hessian eigenvalue) is a real speed limit. Adding an L2 penalty $\tfrac{\alpha}{2}\|w\|^2$ adds $\alpha$
to every curvature — it makes the problem **strongly convex** and better conditioned.
"""
        )
    with c2.container(border=True):
        st.markdown(
            r"""
**Deep networks are non-convex** (the unit-swap argument above works for any layer), yet we still train them with the same
tools. The convex theory explains *local* behaviour: near a minimum the loss looks like a quadratic bowl, its sharpest curvature
$L$ caps the stable learning rate, and a large condition number $L/\mu$ means slow progress — the motivation for momentum and Adam (pages 90–91).
"""
        )


def takeaways():
    st.header("✅ Key takeaways")
    st.markdown(
        r"""
- **Convex** = every chord lies on or above the graph: $f(\lambda a+(1-\lambda)b) \le \lambda f(a)+(1-\lambda)f(b)$; Jensen: $f(\mathbb E X)\le \mathbb E f(X)$.
- Twice differentiable: convex ⇔ $f''\ge 0$ (1D) ⇔ Hessian PSD (all eigenvalues $\ge 0$). Bowl = PD, trough = PSD singular, saddle/ridge/dome = not convex.
- Every local minimum of a convex function is global (but a minimum may not exist, e.g. $e^x$, or may not be unique).
- For $L$-smooth convex $f$, gradient descent with $0<\eta<2/L$ decreases the loss every step; $\eta\le 1/L$ gives $O(1/k)$, strong convexity gives geometric convergence.
- MSE for linear models, logistic, hinge, L1/L2 are convex; neural-network losses are not.
"""
    )
    c1, c2 = st.columns(2)
    with c1:
        safe_page_link("pages/54Local vs Global Minimum.py", "Previous: Page 54 — Local vs Global Minimum", icon="⬅️")
    with c2:
        safe_page_link("pages/56Stochastic Gradient Descent.py", "Next: Page 56 — Stochastic Gradient Descent", icon="➡️")


def main():
    intuition()
    chord_lab()
    hessian_lab()
    local_global_section()
    ml_examples()
    gd_lab()
    ai_connection()
    takeaways()


main()
