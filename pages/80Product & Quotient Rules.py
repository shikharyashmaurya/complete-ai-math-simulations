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

st.set_page_config(page_title="80 · Product & Quotient Rules", page_icon="✖️", layout="wide")

H_FD = 1e-5  # central-difference step


def _everywhere(x):
    return np.ones_like(np.asarray(x, dtype=float), dtype=bool)


# label -> (f, f', LaTeX of f, LaTeX of f', domain mask)
FUNCS = {
    "x²": (lambda x: x**2, lambda x: 2 * x, r"x^2", r"2x", _everywhere),
    "x³ − 2x": (lambda x: x**3 - 2 * x, lambda x: 3 * x**2 - 2, r"x^3-2x", r"3x^2-2", _everywhere),
    "x² + 1": (lambda x: x**2 + 1, lambda x: 2 * x, r"x^2+1", r"2x", _everywhere),
    "sin x": (np.sin, np.cos, r"\sin x", r"\cos x", _everywhere),
    "cos x": (np.cos, lambda x: -np.sin(x), r"\cos x", r"-\sin x", _everywhere),
    "eˣ": (np.exp, np.exp, r"e^{x}", r"e^{x}", _everywhere),
    "ln x": (np.log, lambda x: 1 / x, r"\ln x", r"\tfrac{1}{x}", lambda x: np.asarray(x) > 0),
}


def ev(fn, x):
    with np.errstate(all="ignore"):
        return np.asarray(fn(np.asarray(x, dtype=float)), dtype=float)


def num(v, prec=4):
    return f"{v + 0.0:.{prec}f}"


def par(v, prec=4):
    return f"({num(v, prec)})"


def dark(fig, height=380, **kw):
    fig.update_layout(template="plotly_dark", plot_bgcolor="#0d1321", paper_bgcolor="#070a13", height=height,
                      margin=dict(l=10, r=10, t=40, b=10), legend=dict(orientation="h", y=-0.15), **kw)
    return fig


def section_intuition():
    st.title("✖️ Page 80: Product & Quotient Rules")
    st.markdown(
        r"""
The power rule (Page 45) and the chain rule (Page 46) handle powers and layers. But models constantly **multiply** and
**divide** changing quantities: a gate times a signal ($\sigma(a)\cdot\tanh(b)$ in an LSTM), an exponential divided by a
sum (softmax), a vector divided by its length (normalization).

The trap: $(f\,g)' \neq f'\,g'$. If a rectangle has width $f$ and height $g$, nudging $x$ grows **both** sides, and the
area gains *two strips* — one for each side — plus a tiny corner that vanishes in the limit:
"""
    )
    st.latex(r"(f\,g)' = f'\,g + f\,g' \qquad\qquad \left(\frac{f}{g}\right)' = \frac{f'\,g - f\,g'}{g^2}\quad (g \neq 0)")


def section_rectangle():
    st.header("1) Why two strips? The growing rectangle")
    c1, c2 = st.columns(2)
    x = c1.slider("x", 0.0, 2.0, 1.0, 0.1, key="p80_rx")
    dx = c2.slider("Δx (nudge)", 0.01, 1.0, 0.5, 0.01, key="p80_rdx")
    f = lambda t: 1 + t  # noqa: E731
    g = lambda t: 1 + t**2 / 2  # noqa: E731
    fx, gx = f(x), g(x)
    df, dg = f(x + dx) - fx, g(x + dx) - gx
    st.latex(rf"f(x) = 1 + x = {num(fx, 2)}\ \text{{(width)}},\qquad g(x) = 1 + \tfrac{{x^2}}{{2}} = {num(gx, 3)}\ \text{{(height)}}")

    fig = go.Figure()
    shapes = [
        (0, 0, fx, gx, "#38bdf8", f"f·g = {fx * gx:.3f}"),
        (fx, 0, fx + df, gx, "#FFD166", f"g·Δf = {gx * df:.3f}"),
        (0, gx, fx, gx + dg, "#4ECDC4", f"f·Δg = {fx * dg:.3f}"),
        (fx, gx, fx + df, gx + dg, "#fb7185", f"Δf·Δg = {df * dg:.4f}"),
    ]
    for x0, y0, x1, y1, color, label in shapes:
        fig.add_trace(go.Scatter(x=[x0, x1, x1, x0, x0], y=[y0, y0, y1, y1, y0], fill="toself", mode="lines",
                                 line=dict(color=color, width=1), fillcolor=color, opacity=0.55, name=label))
    dark(fig, height=420, xaxis_title="width f", yaxis_title="height g")
    fig.update_xaxes(range=[0, 4.2])
    fig.update_yaxes(range=[0, 5.7], scaleanchor="x", scaleratio=1)

    col_p, col_t = st.columns([1.2, 1])
    col_p.plotly_chart(fig, width="stretch")
    with col_t:
        dA = f(x + dx) * g(x + dx) - fx * gx
        st.latex(rf"\Delta A = g\,\Delta f + f\,\Delta g + \Delta f\,\Delta g = {num(gx * df)} + {num(fx * dg)} + {num(df * dg)} = {num(dA)}")
        exact = 1 * gx + fx * x
        rows = []
        for d in sorted({1.0, 0.1, 0.01, 0.001, dx}, reverse=True):
            dfd, dgd = f(x + d) - fx, g(x + d) - gx
            rows.append({"Δx": f"{d:g}", "ΔA/Δx": f"{(f(x + d) * g(x + d) - fx * gx) / d:.6f}",
                         "strips/Δx": f"{(gx * dfd + fx * dgd) / d:.6f}", "corner/Δx": f"{dfd * dgd / d:.6f}"})
        st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
        st.success(rf"As Δx → 0 the corner/Δx column → 0 and ΔA/Δx → f′g + fg′ = 1·{gx:.3f} + {fx:.2f}·{x:g} = **{exact:.6f}**.")
    st.caption("The corner is a product of two small changes (second order), so even after dividing by Δx it still vanishes.")


def section_explorer():
    st.header("2) Rule explorer — exact rule vs. numerical derivative")
    c1, c2, c3, c4 = st.columns([1, 1, 1, 1.3])
    op = c1.radio("Operation", ["Product f·g", "Quotient f/g"], key="p80_op")
    fname = c2.selectbox("f(x)", list(FUNCS), index=0, key="p80_f")
    gname = c3.selectbox("g(x)", list(FUNCS), index=3, key="p80_g")
    x = c4.slider("x", -3.0, 3.0, 1.0, 0.05, key="p80_x")
    f, fp, ftex, fptex, fdom = FUNCS[fname]
    g, gp, gtex, gptex, gdom = FUNCS[gname]
    product = op.startswith("Product")

    def h(t):
        F, G = ev(f, t), ev(g, t)
        with np.errstate(all="ignore"):
            return F * G if product else F / G

    def h_rule(t):
        F, Fp, G, Gp = ev(f, t), ev(fp, t), ev(g, t), ev(gp, t)
        with np.errstate(all="ignore"):
            return Fp * G + F * Gp if product else (Fp * G - F * Gp) / G**2

    if product:
        st.latex(rf"(f g)'(x) = f'g + fg' = \left({fptex}\right)\left({gtex}\right) + \left({ftex}\right)\left({gptex}\right)")
    else:
        st.latex(rf"\left(\frac{{f}}{{g}}\right)'(x) = \frac{{f'g - fg'}}{{g^2}} = "
                 rf"\frac{{\left({fptex}\right)\left({gtex}\right) - \left({ftex}\right)\left({gptex}\right)}}{{\left({gtex}\right)^2}}")

    xx = np.linspace(-3, 3, 1201)
    valid = fdom(xx) & gdom(xx)
    hv, dv = h(xx), h_rule(xx)
    for arr in (hv, dv):
        arr[~valid | ~np.isfinite(arr) | (np.abs(arr) > 25)] = np.nan
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xx, y=hv, mode="lines", name="h(x)", line=dict(color="#38bdf8", width=3)))
    fig.add_trace(go.Scatter(x=xx, y=dv, mode="lines", name="h′(x) by the rule", line=dict(color="#FFD166", width=2)))

    info = dict(ok=False, op=op, fname=fname, gname=gname, x=x, ftex=ftex, gtex=gtex, fptex=fptex, gptex=gptex)
    problems = []
    if not (bool(fdom(x)) and bool(gdom(x))):
        problems.append(f"x = {x:g} is outside the domain: ln x needs x > 0.")
    elif not product and abs(float(ev(g, x))) < 1e-12:
        problems.append(f"g({x:g}) = 0, so f/g (and its derivative) is undefined — division by zero.")
    if problems:
        st.error(problems[0])
    else:
        F, Fp, G, Gp = (float(ev(fn, x)) for fn in (f, fp, g, gp))
        rule = float(h_rule(x))
        lo, hi = x - H_FD, x + H_FD
        stencil_ok = bool(fdom(lo)) and bool(gdom(lo))
        if not product:
            stencil_ok = stencil_ok and np.sign(float(ev(g, lo))) == np.sign(float(ev(g, hi))) != 0
        fd = (float(h(hi)) - float(h(lo))) / (2 * H_FD) if stencil_ok else float("nan")
        info.update(ok=True, F=F, Fp=Fp, G=G, Gp=Gp, rule=rule, fd=fd, hval=float(h(x)))
        fig.add_trace(go.Scatter(x=[x], y=[float(h(x))], mode="markers", name="h(x₀)", marker=dict(size=11, color="#38bdf8")))
        if abs(rule) <= 25:
            fig.add_trace(go.Scatter(x=[x - 0.6, x + 0.6], y=[float(h(x)) - 0.6 * rule, float(h(x)) + 0.6 * rule],
                                     mode="lines", name="tangent", line=dict(color="#a78bfa", dash="dash")))
        m = st.columns(4)
        m[0].metric("Rule h′(x)", f"{rule:.8g}")
        m[1].metric(f"Central diff (h = {H_FD:g})", "n/a" if np.isnan(fd) else f"{fd:.8g}")
        m[2].metric("|rule − numeric|", "n/a" if np.isnan(fd) else f"{abs(rule - fd):.2e}")
        m[3].metric("Wrong guess f′·g′" if product else "Wrong guess f′/g′",
                    f"{Fp * Gp:.6g}" if product else ("÷0" if Gp == 0 else f"{Fp / Gp:.6g}"))
        if not product and abs(G) < 1e-2:
            st.warning(f"g(x) = {G:.2e} is close to 0: h and h′ are huge and sensitive — a pole is nearby.")
        if np.isnan(fd):
            st.warning("The central-difference stencil x ± h leaves the domain or crosses g = 0, so no numeric check here.")
    dark(fig, height=380, xaxis_title="x", yaxis_title="value")
    st.plotly_chart(fig, width="stretch")
    st.caption("Gaps in the curves: outside the domain (ln x for x ≤ 0), near a zero of g (quotient), or |value| > 25 (clipped).")
    return info


def section_worked(info):
    st.header("3) Worked example — from your explorer settings")
    if not info["ok"]:
        st.info("Move x into the domain (and away from g(x) = 0) above to see the step-by-step numbers.")
        return
    x, F, Fp, G, Gp = info["x"], info["F"], info["Fp"], info["G"], info["Gp"]
    st.markdown(f"**f(x) = {info['fname']}, g(x) = {info['gname']}, x = {x:g}**")
    st.latex(rf"f({x:g}) = {num(F)},\quad f'({x:g}) = {num(Fp)},\quad g({x:g}) = {num(G)},\quad g'({x:g}) = {num(Gp)}")
    if info["op"].startswith("Product"):
        st.latex(rf"(fg)'({x:g}) = {par(Fp)}{par(G)} + {par(F)}{par(Gp)} = {num(Fp * G)} + {par(F * Gp)} = {num(info['rule'], 6)}")
    else:
        st.latex(rf"\left(\tfrac{{f}}{{g}}\right)'({x:g}) = \frac{{{par(Fp)}{par(G)} - {par(F)}{par(Gp)}}}{{{par(G)}^2}}"
                 rf" = \frac{{{num(Fp * G - F * Gp)}}}{{{num(G * G)}}} = {num(info['rule'], 6)}")
    if not np.isnan(info["fd"]):
        st.latex(rf"\text{{check: }}\frac{{h(x+10^{{-5}}) - h(x-10^{{-5}})}}{{2\cdot 10^{{-5}}}} = {info['fd']:.8f}"
                 rf"\quad\Rightarrow\quad |\text{{error}}| = {abs(info['fd'] - info['rule']):.1e}")
    st.caption("Central-difference error is O(h²) ≈ 1e−10 plus round-off — agreement to ~8 digits confirms the rule.")


def section_sigmoid():
    st.header("4) The famous one: σ′ = σ(1 − σ) via the quotient rule")
    c1, c2 = st.columns([1, 1.3])
    with c1:
        st.latex(r"\sigma(x) = \frac{1}{1+e^{-x}} = \frac{f}{g},\quad f = 1,\ f' = 0,\quad g = 1+e^{-x},\ g' = -e^{-x}")
        st.latex(r"\sigma'(x) = \frac{0\cdot g - 1\cdot(-e^{-x})}{(1+e^{-x})^2} = \frac{1}{1+e^{-x}}\cdot\frac{e^{-x}}{1+e^{-x}} = \sigma(x)\,\bigl(1-\sigma(x)\bigr)")
        x = st.slider("x", -8.0, 8.0, 1.0, 0.1, key="p80_sx")
        e = np.exp(-x)
        quot = e / (1 + e) ** 2
        s = float(sigmoid(x))
        fd = (float(sigmoid(x + H_FD)) - float(sigmoid(x - H_FD))) / (2 * H_FD)
        st.latex(rf"\frac{{e^{{-x}}}}{{(1+e^{{-x}})^2}} = \frac{{{e:.5g}}}{{{(1 + e) ** 2:.5g}}} = {quot:.8f}")
        st.latex(rf"\sigma(1-\sigma) = {s:.6f}\cdot{1 - s:.6f} = {s * (1 - s):.8f}")
        st.latex(rf"\text{{central difference}} = {fd:.8f}")
    with c2:
        xx = np.linspace(-8, 8, 801)
        sx = sigmoid(xx)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=xx, y=sx, name="σ(x)", line=dict(color="#38bdf8", width=3)))
        fig.add_trace(go.Scatter(x=xx, y=sx * (1 - sx), name="σ′(x) = σ(1−σ)", line=dict(color="#FFD166", width=3)))
        fig.add_trace(go.Scatter(x=[x, x], y=[s, s * (1 - s)], mode="markers", name="at x",
                                 marker=dict(size=10, color="#fb7185")))
        dark(fig, height=360, xaxis_title="x")
        st.plotly_chart(fig, width="stretch")
        st.info("σ′ peaks at **0.25** (x = 0) and is tiny for |x| ≳ 5 — through each sigmoid layer the σ′ factor alone "
                "shrinks the backward signal at least 4× (vanishing gradients). Bonus: the backward pass reuses σ from the "
                "forward pass — no extra exp.")
    st.markdown(r"Same trick for $\tanh = \frac{\sinh}{\cosh}$: $\tanh' = \frac{\cosh^2 - \sinh^2}{\cosh^2} = 1 - \tanh^2$.")


def section_ai():
    st.header("5) AI / ML connection")
    t1, t2 = st.tabs(["Softmax Jacobian", "Normalization x / ‖x‖"])
    with t1:
        z = np.array([2.0, 1.0, 0.1])
        s = softmax(z)
        J = np.diag(s) - np.outer(s, s)
        Jfd = np.column_stack([(softmax(z + H_FD * np.eye(3)[j]) - softmax(z - H_FD * np.eye(3)[j])) / (2 * H_FD)
                               for j in range(3)])
        st.markdown(r"Each softmax output is a quotient $s_i = \frac{e^{z_i}}{\sum_k e^{z_k}}$. The quotient rule gives")
        st.latex(r"\frac{\partial s_i}{\partial z_j} = \frac{\delta_{ij} e^{z_i}\sum_k e^{z_k} - e^{z_i}e^{z_j}}{\left(\sum_k e^{z_k}\right)^2} = s_i(\delta_{ij} - s_j)")
        c1, c2 = st.columns(2)
        c1.markdown(f"z = {z.tolist()}, softmax = {np.round(s, 4).tolist()}")
        c1.dataframe(pd.DataFrame(J, columns=["∂/∂z₁", "∂/∂z₂", "∂/∂z₃"], index=["s₁", "s₂", "s₃"]).round(5), width="stretch")
        c2.metric("max |quotient rule − finite difference|", f"{np.abs(J - Jfd).max():.1e}")
        c2.markdown(r"Every column sums to 0 (probabilities always sum to 1), and the diagonal $s_i(1-s_i)$ is the sigmoid "
                    r"formula again. Cross-entropy backprop combines this with $-\log s_y$ into the clean $s - y$.")
    with t2:
        c1, c2 = st.columns(2)
        x1 = c1.slider("x₁", -5.0, 5.0, 3.0, 0.5, key="p80_nx1")
        x2 = c2.slider("x₂", -5.0, 5.0, 4.0, 0.5, key="p80_nx2")
        v = np.array([x1, x2])
        r = float(np.linalg.norm(v))
        st.markdown(r"With $r = \|x\|$ and $\partial r/\partial x_j = x_j / r$, the quotient rule on $u_i = x_i / r$ gives")
        st.latex(r"\frac{\partial u_i}{\partial x_j} = \frac{\delta_{ij}\, r - x_i\, x_j / r}{r^2} = \frac{\delta_{ij} - u_i u_j}{r}"
                 r"\quad\Longrightarrow\quad J = \frac{I - u u^\top}{\|x\|}")
        if r == 0:
            st.error("x = 0 has no direction: x/‖x‖ is 0/0, undefined. Real layers add a small ε: x/√(‖x‖² + ε).")
        else:
            u = v / r
            J = (np.eye(2) - np.outer(u, u)) / r

            def unit(w):
                return w / np.linalg.norm(w)

            Jfd = np.column_stack([(unit(v + H_FD * np.eye(2)[j]) - unit(v - H_FD * np.eye(2)[j])) / (2 * H_FD)
                                   for j in range(2)])
            st.latex(rf"\|x\| = {r:.4f},\quad u = ({u[0]:.4f}, {u[1]:.4f}),\quad J = \begin{{pmatrix}} {J[0, 0]:.4f} & {J[0, 1]:.4f}"
                     rf"\\ {J[1, 0]:.4f} & {J[1, 1]:.4f} \end{{pmatrix}},\quad J x = ({(J @ v)[0] + 0.0:.1e}, {(J @ v)[1] + 0.0:.1e})")
            st.metric("max |J − finite difference|", f"{np.abs(J - Jfd).max():.1e}")
            st.markdown(r"$Jx = 0$: scaling $x$ does not change $u$, so no gradient flows along $x$ — the derivative only "
                        r"rotates $u$. This scale invariance is what LayerNorm/RMSNorm and cosine-similarity heads exploit; "
                        r"the $1/\|x\|$ factor means tiny vectors get huge gradients (hence the ε).")


def section_takeaways():
    st.header("Key takeaways")
    st.markdown(
        r"""
- $(fg)' = f'g + fg'$: two strips of a growing rectangle; the corner $\Delta f\Delta g$ is second order and vanishes.
- $(f/g)' = (f'g - fg')/g^2$ — mind the **minus sign** and the domain: undefined where $g = 0$ (and $\ln$ needs $x > 0$).
- $\sigma' = \sigma(1-\sigma)$, $\tanh' = 1 - \tanh^2$, softmax $J = \mathrm{diag}(s) - ss^\top$ all fall out of the quotient rule.
- Always sanity-check a hand-derived gradient with a central difference — agreement to ~1e−8 is the standard.
"""
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        safe_page_link("pages/79Limits & Continuity.py", "Previous: Page 79 — Limits & Continuity", "⬅️")
    with c2:
        safe_page_link("pages/46Chain Rule — Derivative Through Layers.py", "See also: Page 46 — Chain Rule", "🔗")
    with c3:
        safe_page_link("pages/81Taylor Series — Local Approximation.py", "Next: Page 81 — Taylor Series", "➡️")


def main():
    section_intuition()
    st.divider()
    section_rectangle()
    st.divider()
    info = section_explorer()
    st.divider()
    section_worked(info)
    st.divider()
    section_sigmoid()
    st.divider()
    section_ai()
    st.divider()
    section_takeaways()


main()
