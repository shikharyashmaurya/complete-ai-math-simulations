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
from common.mathutils import sigmoid, softmax  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="79 · Limits & Continuity", page_icon="🎯", layout="wide")

INF = float("inf")
DNE = None  # one-sided limit that does not exist at all (not even ±∞)


def _f_sinc(x):
    return np.sin(x) / x


def _f_hole(x):
    return (x**2 - 1) / (x - 1)


# label -> function, point a, one-sided limits, f(a) (None = undefined), plot window / y-limits, explanation
PRESETS = {
    "Removable hole: sin(x)/x at a = 0": dict(
        f=_f_sinc, a=0.0, tex=r"f(x)=\frac{\sin x}{x}", left=1.0, right=1.0, fa=None,
        window=(-10.0, 10.0), ylim=(-0.5, 1.3), kind="removable",
        why=r"Squeeze: for $0<|x|<\pi/2$, $\cos x \le \frac{\sin x}{x} \le 1$, and both bounds $\to 1$. "
            r"$f(0)$ is $\frac{0}{0}$ — undefined — but the limit is $1$.",
    ),
    "Removable hole: (x²−1)/(x−1) at a = 1": dict(
        f=_f_hole, a=1.0, tex=r"f(x)=\frac{x^2-1}{x-1}", left=2.0, right=2.0, fa=None,
        window=(-2.0, 4.0), ylim=(-1.0, 5.0), kind="removable",
        why=r"For $x \ne 1$: $\frac{x^2-1}{x-1} = \frac{(x-1)(x+1)}{x-1} = x+1$, a line with one point punched out. "
            r"The limit is $1+1 = 2$ even though $f(1)$ is undefined.",
    ),
    "Jump: step H(x) at a = 0": dict(
        f=lambda x: np.where(x >= 0, 1.0, 0.0), a=0.0, tex=r"H(x)=\begin{cases}0 & x<0\\ 1 & x\ge 0\end{cases}",
        left=0.0, right=1.0, fa=1.0, window=(-2.0, 2.0), ylim=(-0.5, 1.5), kind="jump",
        why=r"From the left $H$ is constantly $0$, from the right constantly $1$: both one-sided limits exist but differ.",
    ),
    "Jump: sign(x) at a = 0": dict(
        f=np.sign, a=0.0, tex=r"\operatorname{sign}(x)", left=-1.0, right=1.0, fa=0.0,
        window=(-2.0, 2.0), ylim=(-1.5, 1.5), kind="jump",
        why=r"Left limit $-1$, right limit $+1$, and $\operatorname{sign}(0)=0$ is a third value. No two-sided limit.",
    ),
    "Infinite: 1/x at a = 0": dict(
        f=lambda x: 1.0 / x, a=0.0, tex=r"f(x)=\frac{1}{x}", left=-INF, right=INF, fa=None,
        window=(-3.0, 3.0), ylim=(-10.0, 10.0), kind="infinite",
        why=r"$\frac{1}{h}$ grows without bound: $\to +\infty$ from the right, $\to -\infty$ from the left.",
    ),
    "Infinite: 1/x² at a = 0": dict(
        f=lambda x: 1.0 / x**2, a=0.0, tex=r"f(x)=\frac{1}{x^2}", left=INF, right=INF, fa=None,
        window=(-3.0, 3.0), ylim=(-1.0, 20.0), kind="infinite",
        why=r"Both sides blow up to $+\infty$. We write $\lim = +\infty$, but that is a way of saying "
            r"*no finite limit exists*.",
    ),
    "Oscillating: sin(1/x) at a = 0": dict(
        f=lambda x: np.sin(1.0 / x), a=0.0, tex=r"f(x)=\sin\!\left(\frac{1}{x}\right)", left=DNE, right=DNE,
        fa=None, window=(-0.5, 0.5), ylim=(-1.3, 1.3), kind="oscillating",
        why=r"At $x = \frac{1}{\pi/2 + 2\pi k}$ the value is $1$, at $x = \frac{1}{3\pi/2 + 2\pi k}$ it is $-1$ — "
            r"both sequences $\to 0$. The function never settles, not even on one side.",
    ),
    "Continuous: x² at a = 2": dict(
        f=lambda x: x**2, a=2.0, tex=r"f(x)=x^2", left=4.0, right=4.0, fa=4.0,
        window=(-1.0, 4.0), ylim=(-1.0, 17.0), kind="continuous",
        why=r"Polynomials are continuous: $\lim_{x\to 2} x^2 = 2^2 = 4 = f(2)$ — you may just plug in.",
    ),
}

KIND_TEXT = {
    "removable": "removable discontinuity (a hole you could fill)",
    "jump": "jump discontinuity",
    "infinite": "infinite (essential) discontinuity — a vertical asymptote",
    "oscillating": "oscillating (essential) discontinuity",
    "continuous": "continuous — no discontinuity",
}


def ev(f, x):
    with np.errstate(all="ignore"):
        return np.asarray(f(np.asarray(x, dtype=float)), dtype=float)


def fmt(v, digits=10):
    if v is None:
        return "undefined"
    if np.isnan(v):
        return "undefined"
    if np.isinf(v):
        return "+∞" if v > 0 else "−∞"
    return f"{v + 0.0:.{digits}g}"


def fmt_lim(v):
    return "does not exist (oscillates)" if v is DNE else fmt(v)


def limit_status(p):
    left, right = p["left"], p["right"]
    if left is DNE or right is DNE:
        return False, "does not exist — the values oscillate forever"
    if np.isinf(left) or np.isinf(right):
        if left == right:
            return False, f"no finite limit (both sides → {fmt(left)})"
        return False, "does not exist — the two sides run off to different infinities"
    if left != right:
        return False, f"does not exist — left limit {fmt(left)} ≠ right limit {fmt(right)}"
    return True, f"exists and equals {fmt(left)}"


def dark(fig, height=380, **kw):
    fig.update_layout(template="plotly_dark", plot_bgcolor="#0d1321", paper_bgcolor="#070a13", height=height,
                      margin=dict(l=10, r=10, t=40, b=10), legend=dict(orientation="h", y=-0.15), **kw)
    return fig


def section_intuition():
    st.title("🎯 Page 79: Limits & Continuity")
    st.markdown(
        r"""
On **Page 44** the derivative was defined as the slope the secants *approach* as $h \to 0$ — we never plugged
in $h = 0$ because $\frac{0}{0}$ is meaningless. That word *approach* is a **limit**:

> $\lim_{x\to a} f(x) = L$ means: you can make $f(x)$ as close to $L$ as you like by taking $x$ close
> enough to $a$ (but $x \neq a$). What happens **at** $a$ itself is irrelevant.

A limit can fail in three ways: the two sides disagree (**jump**), the values run off to infinity (**blow-up**), or
they never settle (**oscillation**). A function is **continuous** at $a$ when the limit exists *and* equals $f(a)$.

**Why AI cares:** every gradient is a limit, every finite-difference gradient check is a *numerical* limit,
ReLU has a kink where the limit defining $f'(0)$ fails, and `argmax` is the $T \to 0$ limit of softmax.
"""
    )


def section_limit_table():
    st.header("1) Approaching a point from both sides")
    c1, c2 = st.columns([1, 1])
    with c1:
        name = st.selectbox("Preset", list(PRESETS), key="p79_preset")
    with c2:
        logh = st.slider("log₁₀ h  (step size toward a)", -8.0, 0.0, -2.0, 0.5, key="p79_logh")
    zoom = st.toggle("Zoom the plot to [a − 3h, a + 3h]", value=False, key="p79_zoom")
    p = PRESETS[name]
    f, a, h = p["f"], p["a"], 10.0**logh
    st.latex(p["tex"] + rf",\qquad a = {fmt(a)},\qquad h = 10^{{{logh:g}}}")

    exps = [e for e in range(0, int(np.floor(logh)) - 1, -1) if e >= logh]
    hs = sorted({10.0**e for e in exps} | {h}, reverse=True)
    rows = [{"h": f"{hh:.1e}", "x = a − h": fmt(a - hh), "f(a − h)": fmt(float(ev(f, a - hh))),
             "x = a + h": fmt(a + hh), "f(a + h)": fmt(float(ev(f, a + hh)))} for hh in hs]

    left_v, right_v = float(ev(f, a - h)), float(ev(f, a + h))
    col_t, col_p = st.columns([1, 1.2])
    with col_t:
        st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
        m1, m2 = st.columns(2)
        m1.metric("f(a − h)", fmt(left_v, 8))
        m2.metric("f(a + h)", fmt(right_v, 8))
    with col_p:
        lo, hi = (a - 3 * h, a + 3 * h) if zoom else p["window"]
        n = 40001 if (p["kind"] == "oscillating" or zoom) else 4001
        xl = np.linspace(lo, a, n, endpoint=False)
        xr = np.linspace(a, hi, n + 1)[1:]
        fig = go.Figure()
        for xs, show in ((xl, True), (xr, False)):
            fig.add_trace(go.Scatter(x=xs, y=ev(f, xs), mode="lines", line=dict(color="#38bdf8", width=2),
                                     name="f(x)", showlegend=show))
        for side, val in (("left", p["left"]), ("right", p["right"])):
            if val is not DNE and np.isfinite(val):
                fig.add_trace(go.Scatter(x=[a], y=[val], mode="markers", name=f"{side} limit",
                                         marker=dict(size=13, color="#070a13", line=dict(color="#FFD166", width=2))))
        if p["fa"] is not None:
            fig.add_trace(go.Scatter(x=[a], y=[p["fa"]], mode="markers", name="f(a)",
                                     marker=dict(size=10, color="#4ECDC4")))
        fig.add_trace(go.Scatter(x=[a - h, a + h], y=[left_v, right_v], mode="markers", name="f(a ± h)",
                                 marker=dict(size=10, color="#fb7185", symbol="diamond")))
        dark(fig, xaxis_title="x", yaxis_title="f(x)")
        if not zoom:
            fig.update_yaxes(range=list(p["ylim"]))
        st.plotly_chart(fig, width="stretch")
        if zoom and logh <= -7 and name.startswith("Removable hole: (x"):
            st.caption("At h ≈ 1e−8 the wiggles are floating-point round-off in x² − 1, not mathematics.")

    exists, text = limit_status(p)
    with st.container(border=True):
        a1, a2, a3 = st.columns(3)
        a1.metric("Left limit  x → a⁻", fmt_lim(p["left"]))
        a2.metric("Right limit  x → a⁺", fmt_lim(p["right"]))
        a3.metric("f(a)", fmt(p["fa"]))
        (st.success if exists else st.error)(f"Two-sided limit {text}.")
        st.markdown("**Why:** " + p["why"])
    return name, p, h


def section_epsilon_delta():
    st.header("2) ε–δ: making “close enough” precise")
    st.markdown(
        r"""
The formal definition turns *approaching* into a challenge game: **you** pick a tolerance $\varepsilon > 0$ around
$L$; I must answer with a $\delta > 0$ such that **every** $x$ with $0<|x-a|<\delta$ lands inside $(L-\varepsilon, L+\varepsilon)$.
"""
    )
    st.latex(r"\lim_{x\to a} f(x) = L \iff \forall \varepsilon>0\ \exists \delta>0:\ 0<|x-a|<\delta \Rightarrow |f(x)-L|<\varepsilon")
    c1, c2, c3, c4 = st.columns(4)
    fn = c1.selectbox("Function", ["Linear f(x) = 3x + 1", "Quadratic f(x) = x²"], key="p79_ed_fn")
    a = c2.slider("Point a", -2.0, 2.0, 1.0, 0.1, key="p79_ed_a")
    eps = c3.slider("Tolerance ε", 0.01, 2.0, 0.5, 0.01, key="p79_ed_eps")
    mult = c4.slider("Your δ as a multiple of δ*", 0.25, 2.0, 1.0, 0.05, key="p79_ed_mult")

    if fn.startswith("Linear"):
        f = lambda x: 3 * x + 1  # noqa: E731
        d_star = eps / 3
        derivation = rf"|f(x)-L| = 3|x-a| < \varepsilon \iff |x-a| < \tfrac{{\varepsilon}}{{3}} \;\Rightarrow\; \delta^* = \tfrac{{{eps:g}}}{{3}} = {d_star:.5f}"
    else:
        f = lambda x: x**2  # noqa: E731
        d_star = np.sqrt(a * a + eps) - abs(a)
        derivation = (rf"|x^2-a^2| < (|a|+\delta)^2 - a^2 \le \varepsilon \iff \delta \le \sqrt{{a^2+\varepsilon}}-|a|"
                      rf" \;\Rightarrow\; \delta^* = \sqrt{{{a * a:.2f}+{eps:g}}}-{abs(a):.2f} = {d_star:.5f}")
    L = float(f(a))
    delta = mult * d_star
    xs = a + delta * np.linspace(-1, 1, 20001)[1:-1]
    gaps = np.abs(f(xs) - L)
    worst_i = int(np.argmax(gaps))
    ok = gaps[worst_i] < eps
    st.latex(derivation)

    W = 2.5 * max(delta, d_star)
    xx = np.linspace(a - W, a + W, 1201)
    inside = np.abs(xx - a) < delta
    fig = go.Figure()
    fig.add_hrect(y0=L - eps, y1=L + eps, fillcolor="#4ECDC4", opacity=0.15, line_width=0)
    fig.add_vrect(x0=a - delta, x1=a + delta, fillcolor="#FFD166", opacity=0.12, line_width=0)
    fig.add_trace(go.Scatter(x=xx, y=f(xx), mode="lines", name="f(x)", line=dict(color="#64748b", width=2)))
    fig.add_trace(go.Scatter(x=xx[inside], y=f(xx[inside]), mode="lines", name="f on (a−δ, a+δ)",
                             line=dict(color="#4ECDC4" if ok else "#fb7185", width=4)))
    fig.add_trace(go.Scatter(x=[a], y=[L], mode="markers", name="(a, L)", marker=dict(size=10, color="#a78bfa")))
    dark(fig, height=360, xaxis_title="x", yaxis_title="f(x)")
    c_plot, c_res = st.columns([1.4, 1])
    c_plot.plotly_chart(fig, width="stretch")
    with c_res:
        st.metric("Largest admissible δ*", f"{d_star:.5f}")
        st.metric("Your δ", f"{delta:.5f}")
        st.metric("max |f(x) − L| on the interval", f"{gaps[worst_i]:.5f}", delta=f"ε = {eps:g}", delta_color="off")
        if ok:
            st.success(f"δ = {delta:.5f} works: all 20 000 sampled x stay inside the ε-band.")
        else:
            st.error(f"δ too big: x = {xs[worst_i]:.5f} gives |f(x) − L| = {gaps[worst_i]:.5f} ≥ ε.")
    st.caption("Shrink ε → δ* shrinks too. A limit exists exactly when this game can be won for every ε > 0.")


def section_continuity(name, p):
    st.header("3) Continuity — no pen lifting")
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown(r"$f$ is **continuous at $a$** when all three hold:")
        st.latex(r"\text{(i) } f(a) \text{ defined}\quad \text{(ii) } \lim_{x\to a} f(x) \text{ exists}\quad \text{(iii) } \lim_{x\to a} f(x) = f(a)")
        exists, _ = limit_status(p)
        checks = [p["fa"] is not None, exists, exists and p["fa"] is not None and p["fa"] == p["left"]]
        st.markdown(f"**Your preset:** {name}")
        for label, good in zip(["f(a) defined", "limit exists", "limit = f(a)"], checks):
            st.markdown(f"{'✅' if good else '❌'} {label}")
        st.info(f"Verdict: **{KIND_TEXT[p['kind']]}**.")
    with c2:
        st.markdown(
            r"""
| Type | Picture | One-sided limits | Example |
|---|---|---|---|
| Removable | hole | equal, finite | $\frac{\sin x}{x}$ at 0 |
| Jump | step | finite, different | step, $\operatorname{sign}$ |
| Infinite | asymptote | $\pm\infty$ | $\frac{1}{x}$ at 0 |
| Oscillating | wild wiggle | do not exist | $\sin\frac{1}{x}$ at 0 |

A removable hole can be *repaired*: defining $f(0) = 1$ for $\frac{\sin x}{x}$ gives the smooth `sinc` function.
"""
        )


def kink_info(fn, x0):
    """f, left derivative, right derivative at x0 (exact)."""
    if fn.startswith("|x|"):
        return np.abs, (-1.0 if x0 <= 0 else 1.0), (1.0 if x0 >= 0 else -1.0)
    if fn.startswith("ReLU"):
        return (lambda x: np.maximum(0.0, x)), (1.0 if x0 > 0 else 0.0), (1.0 if x0 >= 0 else 0.0)
    if fn.startswith("x²"):
        return (lambda x: x**2), 2 * x0, 2 * x0
    s = float(sigmoid(x0))
    return (lambda x: np.logaddexp(0.0, x)), s, s


def section_kinks():
    st.header("4) Continuous ≠ differentiable")
    st.markdown(
        r"""
$|x|$ and $\mathrm{ReLU}(x)=\max(0,x)$ are continuous everywhere (no hole, no jump), yet at $0$ the limit that defines
$f'(0)=\lim_{h\to0}\frac{f(0+h)-f(0)}{h}$ **does not exist**: from the right the quotient is one number, from the left another.
Differentiable ⇒ continuous, but **not** the other way round.
"""
    )
    c1, c2, c3 = st.columns(3)
    fn = c1.selectbox("Function", ["|x|", "ReLU(x) = max(0, x)", "x² (smooth)", "softplus ln(1 + eˣ) (smooth ReLU)"],
                      key="p79_kink_fn")
    x0 = c2.slider("Point x₀", -1.0, 1.0, 0.0, 0.05, key="p79_kink_x0")
    logh = c3.slider("log₁₀ h", -6.0, 0.0, -1.0, 0.5, key="p79_kink_logh")
    h = 10.0**logh
    f, d_left, d_right = kink_info(fn, x0)
    f0 = float(f(x0))
    q_right = (float(f(x0 + h)) - f0) / h
    q_left = (f0 - float(f(x0 - h))) / h
    q_central = (float(f(x0 + h)) - float(f(x0 - h))) / (2 * h)

    m = st.columns(4)
    m[0].metric("Right quotient (f(x₀+h) − f(x₀))/h", f"{q_right:.6f}")
    m[1].metric("Left quotient (f(x₀) − f(x₀−h))/h", f"{q_left:.6f}")
    m[2].metric("Central difference", f"{q_central:.6f}")
    m[3].metric("Exact one-sided f′₋ / f′₊", f"{d_left:.4f} / {d_right:.4f}")

    xx = np.linspace(-1.5, 1.5, 1201)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xx, y=f(xx), mode="lines", name=fn, line=dict(color="#38bdf8", width=3)))
    tl = np.linspace(x0 - 0.8, x0, 50)
    tr = np.linspace(x0, x0 + 0.8, 50)
    fig.add_trace(go.Scatter(x=tl, y=f0 + d_left * (tl - x0), mode="lines", name=f"left tangent, slope {d_left:.3g}",
                             line=dict(color="#fb7185", dash="dash", width=3)))
    fig.add_trace(go.Scatter(x=tr, y=f0 + d_right * (tr - x0), mode="lines",
                             name=f"right tangent, slope {d_right:.3g}", line=dict(color="#FFD166", dash="dash", width=3)))
    fig.add_trace(go.Scatter(x=[x0 - h, x0, x0 + h], y=[float(f(x0 - h)), f0, float(f(x0 + h))], mode="markers",
                             name="x₀ − h, x₀, x₀ + h", marker=dict(size=9, color="#a78bfa")))
    dark(fig, height=360, xaxis_title="x", yaxis_title="f(x)")
    fig.update_yaxes(range=[-0.6, 2.3])
    st.plotly_chart(fig, width="stretch")

    if np.isclose(d_left, d_right):
        st.success(f"Differentiable at x₀ = {x0:g}: both one-sided limits equal {d_left:.4f}.")
    else:
        st.error(
            f"Not differentiable at x₀ = {x0:g}: left derivative {d_left:g} ≠ right derivative {d_right:g}. "
            f"Every slope in [{min(d_left, d_right):g}, {max(d_left, d_right):g}] is a **subgradient** "
            f"(a line through the kink that stays below the convex curve)."
        )
        st.warning(
            f"Notice the central difference reports {q_central:.4f} — it averages the two sides and *hides* the kink. "
            "Finite-difference gradient checks near ReLU kinks can therefore disagree with autograd."
        )
    if h > abs(x0) > 0 and not fn.startswith(("x²", "softplus")):
        st.caption("Here h is larger than |x₀|, so x₀ ± h straddles the kink at 0 — shrink h to see the true one-sided slopes.")


def section_worked(name, p, h):
    st.header("5) Worked example — your preset, live")
    f, a = p["f"], p["a"]
    lv, rv = float(ev(f, a - h)), float(ev(f, a + h))
    st.markdown(f"**{name}** with h = {h:.1e}:")
    st.latex(rf"f(a-h) = f({fmt(a - h, 12)}) = {fmt(lv)} \qquad f(a+h) = f({fmt(a + h, 12)}) = {fmt(rv)}")
    if p["kind"] in ("removable", "continuous"):
        L = p["left"]
        st.latex(rf"|f(a-h) - L| = {abs(lv - L):.3e}, \qquad |f(a+h) - L| = {abs(rv - L):.3e} \qquad (L = {fmt(L)})")
        if name.startswith("Removable hole: sin"):
            st.latex(rf"\text{{Taylor: }} \frac{{\sin h}}{{h}} \approx 1 - \frac{{h^2}}{{6}} = {1 - h * h / 6:.12f}")
        st.markdown("Both gaps shrink with h — the numerical evidence agrees with the algebra above.")
    elif p["kind"] == "jump":
        st.markdown(f"The gap |f(a+h) − f(a−h)| = **{abs(rv - lv):g}** never shrinks, however small h gets.")
    elif p["kind"] == "infinite":
        st.markdown(f"|f(a ± h)| ≈ {abs(rv):.3g}: divide h by 10 and the value grows ×{10 if 'x²' not in name else 100}.")
    else:
        st.markdown("Change h by a tiny amount and f(a ± h) jumps anywhere in [−1, 1]: there is no value to settle on.")


def section_ai():
    st.header("6) AI / ML connection")
    t1, t2, t3 = st.tabs(["ReLU kinks & subgradients", "Finite differences are numerical limits", "Softmax: T → 0 gives argmax"])
    with t1:
        st.markdown(
            r"""
- **ReLU** is continuous but not differentiable at $0$. Frameworks simply *choose* a subgradient: PyTorch and JAX use
  $\mathrm{ReLU}'(0) = 0$ (any value in $[0, 1]$ would be valid). Since an input hitting exactly $0.0$ is rare, this choice almost never matters.
- **L1 regularization** $\lambda|w|$ has the same kink at $w = 0$; its subgradient interval $[-\lambda, \lambda]$ is exactly why
  L1 pushes weights to *exactly* zero (sparsity).
- Smooth stand-ins (softplus, GELU, SiLU) remove the kink when a well-defined derivative everywhere is desired.
"""
        )
    with t2:
        st.markdown(
            r"""
Gradient checking replaces the limit $h \to 0$ by a small *fixed* $h$. Too large $h$ → truncation error
(forward $\approx \frac{h}{2}|f''|$, central $\approx \frac{h^2}{6}|f'''|$); too small $h$ → floating-point round-off
($\approx \epsilon_{\text{mach}}/h$). Below: $f = \sin$ at $x = 1$, exact $f'(1) = \cos 1$.
"""
        )
        hs = 10.0 ** np.linspace(-16, 0, 161)
        exact = np.cos(1.0)
        fwd = np.maximum(np.abs((np.sin(1.0 + hs) - np.sin(1.0)) / hs - exact), 1e-17)
        cen = np.maximum(np.abs((np.sin(1.0 + hs) - np.sin(1.0 - hs)) / (2 * hs) - exact), 1e-17)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hs, y=fwd, mode="lines", name="forward difference", line=dict(color="#fb7185")))
        fig.add_trace(go.Scatter(x=hs, y=cen, mode="lines", name="central difference", line=dict(color="#4ECDC4")))
        dark(fig, height=340, xaxis_title="h", yaxis_title="|error|")
        fig.update_xaxes(type="log")
        fig.update_yaxes(type="log")
        st.plotly_chart(fig, width="stretch")
        st.caption(
            f"Best h here: forward ≈ {hs[np.argmin(fwd)]:.0e} (error {fwd.min():.1e}), central ≈ {hs[np.argmin(cen)]:.0e} "
            f"(error {cen.min():.1e}). That is why gradient checks use central differences with h ≈ 1e−5 … 1e−6."
        )
        safe_page_link("pages/44What is a Derivative.py", "Revisit Page 44: the derivative as a limit", "🔬")
    with t3:
        c1, c2 = st.columns([1, 1.4])
        logT = c1.slider("log₁₀ temperature T", -2.0, 1.0, 0.0, 0.05, key="p79_logT")
        tie = c1.checkbox("Make a tie for the largest logit", value=False, key="p79_tie")
        z = np.array([2.0, 1.0, 0.5, 2.0 if tie else 1.5])
        T = 10.0**logT
        probs = softmax(z / T)
        c1.latex(rf"\operatorname{{softmax}}(z/T)_i = \frac{{e^{{z_i/T}}}}{{\sum_j e^{{z_j/T}}}},\quad T = {T:.3g}")
        c1.markdown(f"Logits z = {z.tolist()}")
        fig = go.Figure(go.Bar(x=[f"class {i}" for i in range(4)], y=probs, marker_color="#a78bfa",
                               text=[f"{q:.3f}" for q in probs], textposition="outside"))
        dark(fig, height=320, yaxis_title="probability")
        fig.update_yaxes(range=[0, 1.1])
        c2.plotly_chart(fig, width="stretch")
        winners = np.flatnonzero(z == z.max())
        limit = np.zeros(4)
        limit[winners] = 1.0 / len(winners)
        st.markdown(
            rf"As $T \to 0^+$ softmax → **{limit.tolist()}** (one-hot `argmax`, or split evenly over tied maxima); "
            rf"as $T \to \infty$ → uniform **{[0.25] * 4}**. Greedy decoding in LLMs is the $T \to 0$ limit of sampling."
        )


def section_takeaways():
    st.header("Key takeaways")
    st.markdown(
        r"""
- $\lim_{x\to a} f(x)$ describes what $f$ **approaches**, never what it *is* at $a$; check both one-sided limits.
- Limits fail by **jump**, **blow-up** or **oscillation**; a removable hole still has a limit.
- **Continuous** = limit exists and equals $f(a)$. **Differentiable** is stronger: $|x|$ and ReLU are continuous with a kink.
- Numerical derivatives are limits with finite $h$ — pick $h$ to balance truncation against round-off.
"""
    )
    c1, c2 = st.columns(2)
    with c1:
        safe_page_link("pages/49Integral as Area.py", "Previous: Page 49 — Integral as Area", "⬅️")
    with c2:
        safe_page_link("pages/80Product & Quotient Rules.py", "Next: Page 80 — Product & Quotient Rules", "➡️")


def main():
    section_intuition()
    st.divider()
    name, p, h = section_limit_table()
    st.divider()
    section_epsilon_delta()
    st.divider()
    section_continuity(name, p)
    st.divider()
    section_kinks()
    st.divider()
    section_worked(name, p, h)
    st.divider()
    section_ai()
    st.divider()
    section_takeaways()


main()
