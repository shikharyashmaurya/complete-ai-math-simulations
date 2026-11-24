import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from scipy.special import erf

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.mathutils import sigmoid  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="81 · Taylor Series — Local Approximation", page_icon="🪄", layout="wide")

N_MAX = 30  # partial sums shown in the convergence demo


def _sigmoid_coeffs(a, n):
    """Taylor coefficients of σ around a: reciprocal of the series 1 + e^{-a}·e^{-t} (verified against exact rationals)."""
    q = math.exp(-a)
    d = [1.0 + q] + [q * (-1) ** k / math.factorial(k) for k in range(1, n + 1)]
    c = [1.0 / d[0]]
    for m in range(1, n + 1):
        c.append(-sum(d[k] * c[m - k] for k in range(1, m + 1)) / d[0])
    return np.array(c)


def _ln1p(x):
    x = np.asarray(x, dtype=float)
    out = np.full_like(x, np.nan)
    ok = x > -1
    out[ok] = np.log1p(x[ok])
    return out


def _geom(x):
    x = np.asarray(x, dtype=float)
    with np.errstate(all="ignore"):
        out = 1.0 / (1.0 - x)
    out[x == 1] = np.nan
    return out


# id -> label, f, coefficients(a, n), radius(a), a-range, plot window, y-limits, LaTeX, derivative rule (LaTeX)
FUNCS = {
    "exp": dict(label="eˣ", f=np.exp, coeffs=lambda a, n: np.array([math.exp(a) / math.factorial(k) for k in range(n + 1)]),
                R=lambda a: math.inf, arange=(-2.0, 2.0), win=(-4.0, 4.0), ylim=(-5.0, 30.0), tex=r"e^{x}",
                rule=r"f^{(k)}(a) = e^{a}"),
    "sin": dict(label="sin x", f=np.sin,
                coeffs=lambda a, n: np.array([math.sin(a + k * math.pi / 2) / math.factorial(k) for k in range(n + 1)]),
                R=lambda a: math.inf, arange=(-3.0, 3.0), win=(-8.0, 8.0), ylim=(-3.0, 3.0), tex=r"\sin x",
                rule=r"f^{(k)}(a) = \sin\!\left(a + \tfrac{k\pi}{2}\right)"),
    "cos": dict(label="cos x", f=np.cos,
                coeffs=lambda a, n: np.array([math.cos(a + k * math.pi / 2) / math.factorial(k) for k in range(n + 1)]),
                R=lambda a: math.inf, arange=(-3.0, 3.0), win=(-8.0, 8.0), ylim=(-3.0, 3.0), tex=r"\cos x",
                rule=r"f^{(k)}(a) = \cos\!\left(a + \tfrac{k\pi}{2}\right)"),
    "ln": dict(label="ln(1 + x)", f=_ln1p,
               coeffs=lambda a, n: np.array([math.log1p(a)] + [(-1) ** (k - 1) / (k * (1 + a) ** k) for k in range(1, n + 1)]),
               R=lambda a: 1.0 + a, arange=(-0.8, 2.0), win=(-1.5, 3.5), ylim=(-4.0, 3.0), tex=r"\ln(1+x)",
               rule=r"f^{(k)}(a) = \frac{(-1)^{k-1}(k-1)!}{(1+a)^k}\ (k\ge1)"),
    "geom": dict(label="1 / (1 − x)", f=_geom, coeffs=lambda a, n: np.array([1 / (1 - a) ** (k + 1) for k in range(n + 1)]),
                 R=lambda a: 1.0 - a, arange=(-2.0, 0.8), win=(-3.0, 3.0), ylim=(-6.0, 6.0), tex=r"\frac{1}{1-x}",
                 rule=r"f^{(k)}(a) = \frac{k!}{(1-a)^{k+1}}"),
    "sigmoid": dict(label="σ(x) sigmoid", f=sigmoid, coeffs=_sigmoid_coeffs, R=lambda a: math.hypot(a, math.pi),
                    arange=(-3.0, 3.0), win=(-8.0, 8.0), ylim=(-0.5, 1.5), tex=r"\sigma(x)",
                    rule=r"\text{reciprocal of the series } 1 + e^{-a}e^{-t}\ (\text{poles of }\sigma\text{ at } \pm i\pi)"),
}


def taylor(c, a, x):
    """Horner evaluation of Σ c_k (x − a)^k."""
    t = np.asarray(x, dtype=float) - a
    out = np.zeros_like(t)
    with np.errstate(all="ignore"):
        for ck in c[::-1]:
            out = out * t + ck
    return out


def dark(fig, height=380, **kw):
    fig.update_layout(template="plotly_dark", plot_bgcolor="#0d1321", paper_bgcolor="#070a13", height=height,
                      margin=dict(l=10, r=10, t=40, b=10), legend=dict(orientation="h", y=-0.15), **kw)
    return fig


def section_intuition():
    st.title("🪄 Page 81: Taylor Series — Local Approximation")
    st.markdown(
        r"""
Zoom in far enough on a smooth curve and it looks like a **line** (Page 44). Zoom out a bit and the line is not
enough — but a **parabola** fits better, a cubic better still. A Taylor polynomial matches the value, slope, curvature,
… of $f$ at one point $a$:
"""
    )
    st.latex(r"P_n(x) = \sum_{k=0}^{n} \frac{f^{(k)}(a)}{k!}(x-a)^k = f(a) + f'(a)(x-a) + \frac{f''(a)}{2}(x-a)^2 + \dots")
    st.markdown(
        r"""
**Why AI cares:** gradient descent *is* "trust the linear Taylor term", Newton's method *is* "jump to the bottom of the
quadratic Taylor term", and fast activations like the GELU approximation are cheap polynomial-ish stand-ins.
"""
    )


def section_explorer():
    st.header("1) Taylor polynomial explorer")
    c1, c2, c3 = st.columns(3)
    fid = c1.selectbox("Function f", list(FUNCS), format_func=lambda k: FUNCS[k]["label"], key="p81_fn")
    spec = FUNCS[fid]
    lo, hi = spec["arange"]
    a = c2.slider("Center a", lo, hi, 0.0, 0.1, key=f"p81_a_{fid}")
    n = c3.slider("Order n", 0, 10, 3, 1, key="p81_n")
    f, c = spec["f"], spec["coeffs"](a, N_MAX)
    R = spec["R"](a)
    st.latex(rf"f(x) = {spec['tex']},\quad {spec['rule']},\quad \text{{radius of convergence }} R = "
             + (r"\infty" if math.isinf(R) else f"{R:.3f}"))

    xx = np.linspace(*spec["win"], 1601)
    fx = np.asarray(f(xx), dtype=float)
    pn = taylor(c[: n + 1], a, xx)
    fig = go.Figure()
    if not math.isinf(R):
        fig.add_vrect(x0=a - R, x1=a + R, fillcolor="#4ECDC4", opacity=0.08, line_width=0,
                      annotation_text="|x − a| < R", annotation_position="top left")
    fig.add_trace(go.Scatter(x=xx, y=np.where(np.abs(fx) > 60, np.nan, fx), name=f"f(x) = {spec['label']}",
                             line=dict(color="#38bdf8", width=3)))
    for k in range(max(0, n - 2), n):
        fig.add_trace(go.Scatter(x=xx, y=taylor(c[: k + 1], a, xx), name=f"P{k}", opacity=0.35,
                                 line=dict(width=1, dash="dot")))
    fig.add_trace(go.Scatter(x=xx, y=pn, name=f"P{n}(x)", line=dict(color="#FFD166", width=3)))
    fig.add_trace(go.Scatter(x=[a], y=[float(np.asarray(f(np.array([a])))[0])], mode="markers", name="center a",
                             marker=dict(size=11, color="#fb7185")))
    dark(fig, height=400, xaxis_title="x")
    fig.update_yaxes(range=list(spec["ylim"]))

    err = np.abs(fx - pn)
    err = np.where(np.isfinite(err), np.maximum(err, 1e-17), np.nan)
    fig_e = go.Figure(go.Scatter(x=xx, y=err, name=f"|f − P{n}|", line=dict(color="#fb7185", width=2)))
    dark(fig_e, height=400, xaxis_title="x", yaxis_title=f"|f(x) − P{n}(x)|  (log)")
    fig_e.update_yaxes(type="log", exponentformat="power")
    p1, p2 = st.columns([1.3, 1])
    p1.plotly_chart(fig, width="stretch")
    p2.plotly_chart(fig_e, width="stretch")
    st.caption("The error is ~0 at x = a and grows like |x − a|ⁿ⁺¹ nearby; raising n widens the 'good' region — "
               "but only inside the radius of convergence. Below ~1e−16 the error is floating-point round-off.")
    return fid, spec, a, n, c, R


def section_convergence(fid, spec, a, n, c, R):
    st.header("2) Radius of convergence & the Lagrange remainder")
    c1, c2 = st.columns([1, 1.4])
    xe = c1.slider("Evaluate at x", -3.0, 3.0, 0.5, 0.05, key="p81_xe")
    fval = float(np.asarray(spec["f"](np.array([xe])), dtype=float)[0])
    dist = abs(xe - a)
    partial = np.array([float(taylor(c[: k + 1], a, xe)) for k in range(N_MAX + 1)])
    with c1:
        st.metric("f(x)", "undefined" if not np.isfinite(fval) else f"{fval:.10g}")
        st.metric(f"P{n}(x)", f"{partial[n]:.10g}")
        if math.isinf(R) or dist < R:
            st.success(f"|x − a| = {dist:.3f} < R = {'∞' if math.isinf(R) else f'{R:.3f}'}: the series converges to f(x).")
        elif dist > R:
            st.error(f"|x − a| = {dist:.3f} > R = {R:.3f}: the terms grow, partial sums **diverge** — more terms make it worse.")
        else:
            st.warning("|x − a| = R exactly: the boundary — convergence must be checked case by case.")
        if not np.isfinite(fval):
            st.info("f is undefined at this x (outside the domain or at the pole).")
    with c2:
        ks = np.arange(N_MAX + 1)
        if np.isfinite(fval):
            y = np.maximum(np.abs(partial - fval), 1e-17)
            ttl = "|P_n(x) − f(x)|"
        else:
            y = np.maximum(np.abs(c * (xe - a) ** ks), 1e-17)
            ttl = "|n-th term|"
        fig = go.Figure(go.Scatter(x=ks, y=y, mode="lines+markers", line=dict(color="#a78bfa")))
        fig.add_vline(x=n, line_dash="dash", line_color="#FFD166")
        dark(fig, height=320, xaxis_title="order n", yaxis_title=ttl + " (log)")
        fig.update_yaxes(type="log", exponentformat="power")
        st.plotly_chart(fig, width="stretch")

    if fid in ("exp", "sin", "cos"):
        M = math.exp(max(a, xe)) if fid == "exp" else 1.0
        bound = M * dist ** (n + 1) / math.factorial(n + 1)
        actual = abs(fval - partial[n])
        tol = 1e-14 * max(1.0, abs(fval))  # float64 round-off in evaluating f and P_n
        holds = actual <= bound + tol
        st.markdown("**Lagrange remainder** — for some ξ between a and x:")
        st.latex(r"R_n(x) = \frac{f^{(n+1)}(\xi)}{(n+1)!}(x-a)^{n+1},\qquad |R_n(x)| \le M\,\frac{|x-a|^{n+1}}{(n+1)!},\quad "
                 + (r"M = e^{\max(a,x)}" if fid == "exp" else r"M = 1 \ (|\sin|,|\cos| \le 1)"))
        st.latex(rf"|f(x) - P_{{{n}}}(x)| = {actual:.3e} \;\le\; {M:.4g}\cdot\frac{{{dist:.3f}^{{{n + 1}}}}}{{{n + 1}!}} = {bound:.3e}")
        (st.success if holds else st.error)(
            "Bound holds ✅ — (n+1)! eventually beats any power, so these series converge for every x."
            + (" (The computed error is at floating-point round-off level here.)" if actual <= tol else "")
            if holds else "Bound violated — this should never happen.")
    else:
        st.info("The Lagrange bound is shown for eˣ, sin and cos. For ln(1 + x), 1/(1 − x) and σ the derivatives grow "
                "like k!, which is exactly why their series only converge within a finite radius "
                "(distance from a to the nearest singularity: −1, +1, or ±iπ for σ).")
    return xe, fval, partial


def section_worked(spec, a, n, c, xe, fval, partial):
    st.header("3) Worked example — your settings")
    rows = [{"k": k, "f⁽ᵏ⁾(a)": f"{c[k] * math.factorial(k):.8g}", "c_k = f⁽ᵏ⁾(a)/k!": f"{c[k]:.8g}",
             "term c_k (x − a)^k": f"{c[k] * (xe - a) ** k:.8g}"} for k in range(n + 1)]
    st.markdown(f"f(x) = {spec['label']}, a = {a:g}, n = {n}, x = {xe:g}:")
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    st.latex(rf"P_{{{n}}}({xe:g}) = \sum_{{k=0}}^{{{n}}} c_k ({xe:g} - {a:g})^k = {partial[n]:.10g}")
    if np.isfinite(fval):
        st.latex(rf"f({xe:g}) = {fval:.10g},\qquad \text{{error}} = {abs(fval - partial[n]):.3e}")


def opt_funcs(name):
    """f, f′, f″ for the 1-D optimization lab."""
    if name.startswith("Quadratic"):
        return (lambda x: 2 * (x - 1) ** 2 + 0.5), (lambda x: 4 * (x - 1)), (lambda x: 4.0 + 0 * x)
    if name.startswith("log-cosh"):
        def lc(x):
            y = np.abs(np.asarray(x, dtype=float) - 1)
            return y + np.log1p(np.exp(-2 * y)) - math.log(2)
        return lc, (lambda x: np.tanh(x - 1)), (lambda x: 1 - np.tanh(x - 1) ** 2)
    if name.startswith("Quartic"):
        return (lambda x: x**4 / 4 - x + 1), (lambda x: x**3 - 1), (lambda x: 3 * x**2)
    return (lambda x: x**4 / 4 - x**2), (lambda x: x**3 - 2 * x), (lambda x: 3 * x**2 - 2)


def iterate(x0, step, n=8):
    xs = [x0]
    for _ in range(n):
        x = xs[-1]
        nxt = step(x) if np.isfinite(x) else np.nan
        xs.append(nxt if np.isfinite(nxt) and abs(nxt) < 1e6 else np.nan)
    return xs


def section_optim():
    st.header("4) Linear & quadratic models → gradient descent vs. Newton")
    st.markdown(
        r"""
Around the current point $x_0$, replace the loss by its Taylor model and step to where the model says is best:
- **1st order** $f(x_0) + f'(x_0)\,\Delta$ has no minimum, so take a *small* step downhill: $\Delta = -\eta f'(x_0)$ (gradient descent).
- **2nd order** $f(x_0) + f'\Delta + \frac12 f''\Delta^2$ has its minimum at $\Delta = -f'/f''$ (Newton's method) — if $f'' > 0$.
"""
    )
    c1, c2, c3 = st.columns(3)
    name = c1.selectbox("Loss f(x)", ["Quadratic 2(x − 1)² + 0.5", "log-cosh ln cosh(x − 1)", "Quartic x⁴/4 − x + 1",
                                      "Non-convex x⁴/4 − x²"], key="p81_opt_fn")
    x0 = c2.slider("Start x₀", -3.0, 3.0, -1.0, 0.05, key="p81_x0")
    lr = c3.slider("Learning rate η", 0.01, 1.0, 0.1, 0.01, key="p81_lr")
    f, d1, d2 = opt_funcs(name)
    g, H = float(d1(x0)), float(d2(x0))
    x_gd = x0 - lr * g
    newton_ok = abs(H) > 1e-10
    x_nt = x0 - g / H if newton_ok else float("nan")

    xx = np.linspace(-3.5, 3.5, 701)
    fv = np.asarray(f(xx), dtype=float)
    loc = np.linspace(x0 - 1.5, x0 + 1.5, 200)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xx, y=fv, name="f(x)", line=dict(color="#38bdf8", width=3)))
    fig.add_trace(go.Scatter(x=loc, y=float(f(x0)) + g * (loc - x0), name="linear model (tangent)",
                             line=dict(color="#94a3b8", dash="dot")))
    fig.add_trace(go.Scatter(x=loc, y=float(f(x0)) + g * (loc - x0) + 0.5 * H * (loc - x0) ** 2, name="quadratic model",
                             line=dict(color="#a78bfa", dash="dash")))
    fig.add_trace(go.Scatter(x=[x0], y=[float(f(x0))], mode="markers", name="x₀", marker=dict(size=12, color="#fb7185")))
    fig.add_trace(go.Scatter(x=[x_gd], y=[float(f(x_gd))], mode="markers", name="GD step",
                             marker=dict(size=12, color="#FFD166", symbol="diamond")))
    if newton_ok and abs(x_nt) < 1e6:
        fig.add_trace(go.Scatter(x=[x_nt], y=[float(f(x_nt))], mode="markers", name="Newton step",
                                 marker=dict(size=12, color="#4ECDC4", symbol="star")))
    dark(fig, height=400, xaxis_title="x", yaxis_title="loss")
    fig.update_xaxes(range=[-3.5, 3.5])
    fig.update_yaxes(range=[float(np.min(fv)) - 1, float(np.min(fv)) + 1.2 * (float(np.max(fv)) - float(np.min(fv))) / 3 + 2])

    cp, cm = st.columns([1.3, 1])
    cp.plotly_chart(fig, width="stretch")
    with cm:
        st.latex(rf"f'(x_0) = {g:.4f},\quad f''(x_0) = {H:.4f}")
        st.latex(rf"x_{{GD}} = x_0 - \eta f' = {x0:g} - {lr:g}\cdot({g:.4f}) = {x_gd:.4f}")
        if newton_ok:
            st.latex(rf"x_{{N}} = x_0 - \frac{{f'}}{{f''}} = {x0:g} - \frac{{{g:.4f}}}{{{H:.4f}}} = {x_nt:.4f}")
        if not newton_ok:
            st.error("f″(x₀) = 0: the quadratic model is a line — the Newton step is undefined (division by zero).")
        elif H < 0:
            st.warning("f″(x₀) < 0: the quadratic model is an upside-down parabola; Newton jumps to its **maximum**.")
        if H > 0:
            st.info(f"Local stability: GD on the quadratic model needs η < 2/f″ = {2 / H:.3f}; η = 1/f″ = {1 / H:.3f} "
                    "is exactly the Newton step.")

    def gd_step(x):
        return x - lr * float(d1(x))

    def newton_step(x):
        h2 = float(d2(x))
        return x - float(d1(x)) / h2 if abs(h2) > 1e-10 else np.nan

    with np.errstate(all="ignore"):
        gd, nt = iterate(x0, gd_step), iterate(x0, newton_step)
        rows = [{"step": k, "x (GD)": f"{gd[k]:.6f}", "f (GD)": f"{float(f(gd[k])):.6g}",
                 "x (Newton)": f"{nt[k]:.6f}", "f (Newton)": f"{float(f(nt[k])):.6g}"} for k in range(len(gd))]
    t1, t2 = st.columns(2)
    with t1:
        st.markdown("**Eight steps of each** (nan = diverged or undefined)")
        st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    with t2:
        st.markdown("**Why small η makes the linear model trustworthy**")
        lin_rows = []
        for eta in (0.001, 0.01, 0.1, 0.3, 1.0):
            actual = float(f(x0 - eta * g)) - float(f(x0))
            pred = -eta * g * g
            rel = abs(actual - pred) / abs(pred) if pred != 0 else float("nan")
            lin_rows.append({"η": eta, "actual Δf": f"{actual:.6g}", "linear −η f′²": f"{pred:.6g}",
                             "rel. error": "n/a (f′ = 0)" if np.isnan(rel) else f"{rel:.2e}"})
        st.dataframe(pd.DataFrame(lin_rows), hide_index=True, width="stretch")
        st.caption("Relative error ≈ |f″| η / 2 for small η — shrink η 10× and the first-order prediction gets 10× more "
                   "accurate. That is the guarantee behind 'small learning rate ⇒ loss goes down'.")


def section_ai():
    st.header("5) AI / ML connection")
    t1, t2 = st.tabs(["GELU's tanh approximation", "Second-order optimization & learning rates"])
    with t1:
        st.latex(r"\mathrm{GELU}(x) = x\,\Phi(x) \approx \tfrac12 x\left(1 + \tanh\!\left[\sqrt{2/\pi}\,(x + c\,x^3)\right]\right)")
        cc = st.slider("Cubic coefficient c (BERT/GPT-2 use 0.044715)", 0.0, 0.1, 0.044715, 0.000005, format="%.6f",
                       key="p81_gelu_c")
        xx = np.linspace(-6, 6, 2401)
        exact = 0.5 * xx * (1 + erf(xx / math.sqrt(2)))
        approx = 0.5 * xx * (1 + np.tanh(math.sqrt(2 / math.pi) * (xx + cc * xx**3)))
        taylor3 = xx * (0.5 + xx / math.sqrt(2 * math.pi) - xx**3 / (6 * math.sqrt(2 * math.pi)))
        e_t, e_p = np.abs(approx - exact), np.abs(taylor3 - exact)
        m1, m2 = st.columns(2)
        m1.metric("max |tanh approx − GELU| on [−6, 6]", f"{e_t.max():.2e}")
        m2.metric("max |Taylor of Φ to x³ − GELU| on [−6, 6]", f"{e_p.max():.2e}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=xx, y=np.maximum(e_t, 1e-17), name="tanh approximation", line=dict(color="#4ECDC4")))
        fig.add_trace(go.Scatter(x=xx, y=np.maximum(e_p, 1e-17), name="pure Taylor (x·Φ to order x⁴)",
                                 line=dict(color="#fb7185")))
        dark(fig, height=320, xaxis_title="x", yaxis_title="|error| (log)")
        fig.update_yaxes(type="log", exponentformat="power")
        st.plotly_chart(fig, width="stretch")
        st.markdown(
            r"""
Near $0$, $\tanh\!\big(\sqrt{2/\pi}\,x\big)$ agrees with $2\Phi(x) - 1$ to first order — a Taylor match. The pure
Taylor polynomial of $\Phi$ explodes for large $|x|$, whereas $\tanh$ saturates like $\Phi$ does; the small cubic term
$c\,x^3$ (fitted, not derived) fixes the mid-range. Try $c = 0$: the maximum error grows ~70×.
"""
        )
    with t2:
        st.markdown(
            r"""
- **Gradient descent** minimizes the *linear* Taylor model plus a proximity penalty $\frac{1}{2\eta}\Delta^2$ — valid only while
  $\Delta$ is small, which is what the learning rate enforces. If $\eta > 2/\lambda_{\max}$ (largest Hessian eigenvalue),
  the quadratic term wins and training diverges.
- **Newton's method** uses $\Delta = -H^{-1}\nabla f$ — converges in one step on a quadratic, but a $d\times d$ Hessian for
  $d = 10^9$ parameters is impossible. Practical second-order ideas: **L-BFGS** (low-rank curvature from gradient history),
  **Gauss–Newton / K-FAC / Shampoo** (structured curvature approximations), Hessian-vector products for analysis.
- **Adam** divides by a running RMS of gradients — loosely a cheap diagonal curvature-like rescaling, not true Newton.
- Watch the log-cosh loss in the lab: from $x_0 = -1$ Newton overshoots and **diverges** (curvature vanishes far away),
  while plain GD with a small η is slow but safe — the reason damped/trust-region Newton exists.
"""
        )


def section_takeaways():
    st.header("Key takeaways")
    st.markdown(
        r"""
- $P_n$ matches $f$ and its first $n$ derivatives at $a$; the error near $a$ shrinks like $|x-a|^{n+1}$.
- Convergence only within the **radius** $R$ = distance to the nearest singularity (possibly complex: $\pm i\pi$ for $\sigma$).
- Lagrange: $|R_n| \le M|x-a|^{n+1}/(n+1)!$ — for $e^x$, $\sin$, $\cos$ the factorial wins everywhere.
- GD trusts the **linear** model (small η!), Newton the **quadratic** one (needs $f'' > 0$).
"""
    )
    c1, c2 = st.columns(2)
    with c1:
        safe_page_link("pages/80Product & Quotient Rules.py", "Previous: Page 80 — Product & Quotient Rules", "⬅️")
    with c2:
        safe_page_link("pages/82Jacobian & Hessian.py", "Next: Page 82 — Jacobian & Hessian", "➡️")


def main():
    section_intuition()
    st.divider()
    fid, spec, a, n, c, R = section_explorer()
    st.divider()
    xe, fval, partial = section_convergence(fid, spec, a, n, c, R)
    st.divider()
    section_worked(spec, a, n, c, xe, fval, partial)
    st.divider()
    section_optim()
    st.divider()
    section_ai()
    st.divider()
    section_takeaways()


main()
