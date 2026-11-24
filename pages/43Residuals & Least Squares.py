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
from common.mathutils import fmt_num, fmt_signed  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="43 · Residuals & Least Squares", page_icon="📏", layout="wide")

PRESETS = {
    "Good fit — straight trend, constant noise": "good",
    "Curvature — the truth bends (quadratic)": "curve",
    "Heteroscedasticity — noise grows with x": "hetero",
    "High-leverage outlier — one far-away point": "outlier",
    "Edge case — all x identical": "same_x",
}
PRESET_HINTS = {
    "good": "Residuals form a structureless horizontal band around 0: the straight line has captured everything except noise.",
    "curve": "A **U-shaped pattern**: the line is too high in the middle and too low at both ends. A straight line is the wrong model — add an $x^2$ feature (or use a non-linear model).",
    "hetero": r"A **funnel**: the spread of the residuals grows with the prediction. The slope is still unbiased, but its error bars from the usual formula are wrong; consider weighting or modelling $\log y$.",
    "outlier": "One point sits far to the right in $x$ (**high leverage**) and far from the trend. It drags the line towards itself, so its own residual looks *smaller* than it deserves — check Cook's distance in the *Leverage & influence* tab.",
    "same_x": "Every point has the same $x$, so the data say nothing about the slope.",
}
P = 2  # parameters in a simple linear fit: intercept and slope


def make_data(kind, n, noise, seed):
    rng = np.random.default_rng(seed)
    x = rng.uniform(0.0, 10.0, n)
    eps = rng.normal(0.0, 1.0, n)
    if kind == "curve":
        y = 0.15 * x**2 - 0.5 * x + 3.0 + noise * eps
    elif kind == "hetero":
        y = 2.0 + 0.8 * x + noise * (0.15 + 0.3 * x) * eps
    elif kind == "same_x":
        x = np.full(n, 5.0)
        y = 2.0 + 0.8 * x + noise * eps
    else:
        y = 2.0 + 0.8 * x + noise * eps
    if kind == "outlier" and n >= 1:
        x[-1], y[-1] = 25.0, 3.0  # the trend predicts about 22 here
    return x, y


def ols(x, y):
    """Closed-form simple least squares; returns (fit dict, None) or (None, reason)."""
    n = len(x)
    if n < 2:
        return None, "few"
    xbar, ybar = float(np.mean(x)), float(np.mean(y))
    sxx = float(np.sum((x - xbar) ** 2))
    if sxx <= 1e-12 * max(1.0, float(np.sum(x**2))):
        return None, "same_x"
    sxy = float(np.sum((x - xbar) * (y - ybar)))
    b1 = sxy / sxx
    b0 = ybar - b1 * xbar
    yhat = b0 + b1 * x
    e = y - yhat
    sse = float(np.sum(e**2))
    sst = float(np.sum((y - ybar) ** 2))
    ssr = float(np.sum((yhat - ybar) ** 2))
    h = 1.0 / n + (x - xbar) ** 2 / sxx
    return dict(n=n, xbar=xbar, ybar=ybar, sxx=sxx, sxy=sxy, b0=b0, b1=b1, yhat=yhat, e=e, sse=sse, sst=sst, ssr=ssr, h=h), None


def cooks_distance(fit):
    """D_i = e_i^2 / (p s^2) * h_i / (1 - h_i)^2, or None when s^2 is undefined/zero."""
    n, sse = fit["n"], fit["sse"]
    if n <= P or sse <= 1e-12 * max(1.0, fit["sst"]):
        return None
    s2 = sse / (n - P)
    one_minus_h = 1.0 - fit["h"]
    with np.errstate(divide="ignore", invalid="ignore"):
        d = fit["e"] ** 2 / (P * s2) * fit["h"] / one_minus_h**2
    return np.where(one_minus_h < 1e-12, np.inf, d)


def style(fig, title, xt, yt, height=380):
    fig.update_layout(
        template="plotly_dark", title=title, height=height, xaxis_title=xt, yaxis_title=yt,
        margin=dict(l=10, r=10, t=50, b=10), legend=dict(orientation="h", y=-0.22),
    )
    return fig


def intuition():
    st.title("📏 Page 43: Residuals & Least Squares")
    st.markdown(
        r"""
A fitted line makes a prediction $\hat y_i = b_0 + b_1 x_i$ for every data point. What it **misses** is the
**residual**

$$e_i = y_i - \hat y_i \qquad(\text{positive: point above the line, negative: below}).$$

**Least squares** picks the $b_0, b_1$ that make the **sum of squared residuals** $\text{SSE}=\sum_i e_i^2$ as small as
possible. On page 42 the line "chased" your clicks; here we open the hood: the exact formula, what the leftover
residuals tell you about your model, and why a single far-away point can hijack the fit.
"""
    )
    st.info(
        "Why it matters for AI: residuals are the raw error signal of every regression model. Plotting them is the fastest "
        "way to find out *how* a model is wrong — missing curvature, noise that changes with the input, or a few points that dominate training."
    )


def fit_lab():
    st.header("🧪 Lab: fit a line, then interrogate the residuals")
    st.session_state.setdefault("p43_seed", 43)
    c1, c2, c3, c4 = st.columns([2.4, 1, 1, 0.8])
    preset_label = c1.selectbox("Data scenario", list(PRESETS), key="p43_preset")
    n = c2.slider("Points n", 1, 100, 30, key="p43_n")
    noise = c3.slider("Noise σ", 0.0, 3.0, 1.0, 0.1, key="p43_noise")
    c4.write("")
    if c4.button("🎲 Resample", key="p43_resample"):
        st.session_state["p43_seed"] += 1
    kind = PRESETS[preset_label]
    x, y = make_data(kind, n, noise, st.session_state["p43_seed"])
    fit, reason = ols(x, y)

    if fit is None:
        fig = go.Figure(go.Scatter(x=x, y=y, mode="markers", marker=dict(size=9, color="#4ECDC4"), name="data"))
        st.plotly_chart(style(fig, "Data (no unique least-squares line)", "x", "y"), width="stretch")
        if reason == "few":
            st.warning(
                f"Only n = {n} point. Infinitely many lines pass through a single point, so the slope is undefined. "
                "Least squares needs at least 2 points with **different** x values."
            )
        else:
            st.warning(
                r"All x values are identical, so $S_{xx}=\sum (x_i-\bar x)^2 = 0$ and the slope $b_1 = S_{xy}/S_{xx} = 0/0$ is **undefined**. "
                r"Equivalently $\det(X^\top X) = n\,S_{xx} = 0$: the normal equations are singular and every line through "
                rf"$(\bar x, \bar y) = ({fmt_num(float(np.mean(x)))}, {fmt_num(float(np.mean(y)))})$ has the same SSE."
            )
        return None

    tabs = st.tabs(["Fit & residuals", "Residual plot (diagnostics)", "Leverage & influence", "R² decomposition", "Normal equations & checks"])
    with tabs[0]:
        tab_fit(x, y, fit)
    with tabs[1]:
        tab_residual_plot(fit, kind)
    with tabs[2]:
        tab_leverage(x, y, fit)
    with tabs[3]:
        tab_r2(x, y, fit)
    with tabs[4]:
        tab_normal_equations(x, y, fit)
    return x, y, fit


def tab_fit(x, y, fit):
    show_res = st.toggle("Draw residuals as vertical segments", value=True, key="p43_show_res")
    xs = np.linspace(float(x.min()), float(x.max()), 2)
    fig = go.Figure()
    if show_res:
        seg_x = np.repeat(x, 3)
        seg_y = np.column_stack([y, fit["yhat"], np.full_like(y, np.nan)]).ravel()
        seg_x[2::3] = np.nan
        fig.add_trace(go.Scatter(x=seg_x, y=seg_y, mode="lines", line=dict(color="#FF6B6B", width=1.5), name="residual eᵢ"))
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", marker=dict(size=8, color="#4ECDC4"), name="data"))
    fig.add_trace(go.Scatter(x=xs, y=fit["b0"] + fit["b1"] * xs, mode="lines", line=dict(color="#FFD166", width=3), name="least-squares line"))
    fig.add_trace(go.Scatter(x=[fit["xbar"]], y=[fit["ybar"]], mode="markers", marker=dict(size=14, symbol="x", color="white"), name="(x̄, ȳ)"))
    st.plotly_chart(style(fig, f"ŷ = {fmt_num(fit['b0'])} {fmt_signed(fit['b1'])}·x", "x", "y"), width="stretch")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Slope b₁", fmt_num(fit["b1"], 3))
    m2.metric("Intercept b₀", fmt_num(fit["b0"], 3))
    m3.metric("SSE = Σeᵢ²", fmt_num(fit["sse"], 3))
    m4.metric("Σeᵢ (always 0)", f"{fit['e'].sum():.1e}")


def tab_residual_plot(fit, kind):
    yhat, e, n = fit["yhat"], fit["e"], fit["n"]
    fig = go.Figure()
    fig.add_hline(y=0, line=dict(color="white", dash="dot"))
    fig.add_trace(go.Scatter(x=yhat, y=e, mode="markers", marker=dict(size=8, color="#FF6B6B"), name="residuals"))
    order = np.argsort(yhat)
    curvature_share = None
    if len(np.unique(np.round(yhat, 12))) >= 3 and fit["sse"] > 1e-12 * max(1.0, fit["sst"]):
        coef = np.polyfit(yhat, e, 2)
        trend = np.polyval(coef, yhat)
        curvature_share = 1.0 - float(np.sum((e - trend) ** 2)) / fit["sse"]
        fig.add_trace(go.Scatter(x=yhat[order], y=trend[order], mode="lines", line=dict(color="#FFD166", dash="dash"), name="quadratic trend of residuals"))
    spread_ratio = None
    if n >= 10:
        bins = np.array_split(order, 5)
        centers = [float(np.mean(yhat[b])) for b in bins]
        sds = [float(np.std(e[b])) for b in bins]
        fig.add_trace(go.Scatter(x=centers, y=[2 * s for s in sds], mode="lines+markers", line=dict(color="#a78bfa"), name="±2·SD per bin"))
        fig.add_trace(go.Scatter(x=centers, y=[-2 * s for s in sds], mode="lines+markers", line=dict(color="#a78bfa"), showlegend=False))
        if sds[0] > 1e-12:
            spread_ratio = sds[-1] / sds[0]
    st.plotly_chart(style(fig, "Residuals vs fitted values", "fitted ŷ", "residual e = y − ŷ"), width="stretch")
    c1, c2 = st.columns(2)
    c1.metric("Residual variance explained by a curve", "—" if curvature_share is None else f"{100 * curvature_share:.0f}%")
    c2.metric("Spread ratio (top bin SD / bottom bin SD)", "—" if spread_ratio is None else fmt_num(spread_ratio))
    st.caption("Rules of thumb, not formal tests: a large curve share hints at non-linearity, a spread ratio far from 1 hints at heteroscedasticity (needs n ≥ 10).")
    st.success(PRESET_HINTS[kind])


def tab_leverage(x, y, fit):
    n, h = fit["n"], fit["h"]
    st.markdown(
        r"""
**Leverage** $h_{ii} = \frac1n + \frac{(x_i-\bar x)^2}{S_{xx}}$ measures how far a point's $x$ is from the crowd — it is the
weight of $y_i$ in its own prediction $\hat y_i$. Leverages always sum to the number of parameters ($p=2$), so the average is $2/n$.
**Influence** needs both leverage *and* a large residual. **Cook's distance**
$D_i = \frac{e_i^2}{p\,s^2}\cdot\frac{h_{ii}}{(1-h_{ii})^2}$ (with $s^2 = \text{SSE}/(n-2)$) measures how much *all* predictions move when point $i$ is deleted.
"""
    )
    d = cooks_distance(fit)
    i_top = int(np.argmax(h)) if d is None else int(np.nanargmax(np.where(np.isinf(d), 1e300, d)))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", marker=dict(size=7 + 30 * h / h.max(), color=h, colorscale="Viridis", showscale=True, colorbar=dict(title="hᵢᵢ")), name="data (size = leverage)"))
    xs = np.linspace(float(x.min()), float(x.max()), 2)
    fig.add_trace(go.Scatter(x=xs, y=fit["b0"] + fit["b1"] * xs, mode="lines", line=dict(color="#FFD166", width=3), name="fit with all points"))
    keep = np.arange(n) != i_top
    refit, _ = ols(x[keep], y[keep])
    if refit is not None:
        fig.add_trace(go.Scatter(x=xs, y=refit["b0"] + refit["b1"] * xs, mode="lines", line=dict(color="#4ECDC4", dash="dash", width=2), name=f"fit without point #{i_top}"))
    st.plotly_chart(style(fig, "Which point is pulling the line?", "x", "y"), width="stretch")
    c1, c2, c3 = st.columns(3)
    c1.metric("Σ hᵢᵢ (= p = 2)", fmt_num(float(h.sum()), 6))
    c2.metric(f"Max leverage (point #{int(np.argmax(h))})", fmt_num(float(h.max()), 3), f"avg {fmt_num(2 / n, 3)}", delta_color="off")
    if refit is not None:
        c3.metric(f"Slope without point #{i_top}", fmt_num(refit["b1"], 3), fmt_num(refit["b1"] - fit["b1"], 3), delta_color="off")
    else:
        c3.metric(f"Slope without point #{i_top}", "undefined")
    table = pd.DataFrame({"x": x, "y": y, "residual e": fit["e"], "leverage h": h})
    if d is None:
        st.info("Cook's distance needs n > 2 and SSE > 0 (otherwise s² = SSE/(n−2) is undefined or zero). Showing leverage only.")
        table = table.sort_values("leverage h", ascending=False)
    else:
        table["Cook's D"] = d
        table = table.sort_values("Cook's D", ascending=False)
        flagged = int(np.sum(d > 4 / n))
        st.caption(f"Common rule of thumb: inspect points with D > 4/n = {fmt_num(4 / n, 3)} — {flagged} point(s) here. High leverage alone (2p/n = {fmt_num(4 / n, 3)}) is not a problem if the point follows the trend.")
    st.dataframe(table.head(6).round(4), width="stretch")


def tab_r2(x, y, fit):
    sst, ssr, sse = fit["sst"], fit["ssr"], fit["sse"]
    fig = go.Figure()
    fig.add_trace(go.Bar(y=["SST (total)"], x=[sst], orientation="h", marker_color="#94a3b8", name="SST = Σ(yᵢ−ȳ)²"))
    fig.add_trace(go.Bar(y=["SSR + SSE"], x=[ssr], orientation="h", marker_color="#4ECDC4", name="SSR = Σ(ŷᵢ−ȳ)² explained"))
    fig.add_trace(go.Bar(y=["SSR + SSE"], x=[sse], orientation="h", marker_color="#FF6B6B", name="SSE = Σeᵢ² unexplained"))
    fig.update_layout(barmode="stack")
    st.plotly_chart(style(fig, "Variance decomposition: SST = SSR + SSE", "sum of squares", "", height=300), width="stretch")
    if sst <= 1e-12:
        st.warning("All y values are equal (SST = 0): there is no variation to explain, so R² = 1 − SSE/SST is undefined.")
        return
    r2 = 1.0 - sse / sst
    r = float(np.corrcoef(x, y)[0, 1])
    st.latex(rf"R^2 = 1 - \frac{{\text{{SSE}}}}{{\text{{SST}}}} = 1 - \frac{{{fmt_num(sse, 3)}}}{{{fmt_num(sst, 3)}}} = {fmt_num(r2, 4)}, \qquad \text{{SSR}}+\text{{SSE}} = {fmt_num(ssr + sse, 3)} = \text{{SST}}")
    st.latex(rf"\text{{Simple regression only: }} R^2 = r_{{xy}}^2 = ({fmt_num(r, 4)})^2 = {fmt_num(r * r, 4)}")
    st.caption("R² is the share of the variation in y that the line accounts for. A high R² does **not** prove the model is right — the 'Curvature' scenario can still score well while its residuals show a clear pattern.")


def tab_normal_equations(x, y, fit):
    n = fit["n"]
    xtx = np.array([[n, x.sum()], [x.sum(), np.sum(x**2)]])
    xty = np.array([y.sum(), np.sum(x * y)])
    beta = np.linalg.solve(xtx, xty)
    st.markdown(r"Setting $\partial\,\text{SSE}/\partial b_0 = 0$ and $\partial\,\text{SSE}/\partial b_1 = 0$ gives the **normal equations** $X^\top X\,\beta = X^\top y$ with design matrix $X = [\mathbf 1 \;\; x]$:")
    st.latex(
        rf"\begin{{bmatrix}} {n} & {fmt_num(xtx[0, 1])} \\ {fmt_num(xtx[0, 1])} & {fmt_num(xtx[1, 1])} \end{{bmatrix}}"
        rf"\begin{{bmatrix}} b_0 \\ b_1 \end{{bmatrix}} = \begin{{bmatrix}} {fmt_num(xty[0])} \\ {fmt_num(xty[1])} \end{{bmatrix}}"
        rf"\;\Rightarrow\; b_0 = {fmt_num(beta[0], 4)},\; b_1 = {fmt_num(beta[1], 4)}"
    )
    cov = float(np.cov(x, y, ddof=1)[0, 1])
    var = float(np.var(x, ddof=1))
    st.latex(
        rf"b_1 = \frac{{S_{{xy}}}}{{S_{{xx}}}} = \frac{{\operatorname{{cov}}(x,y)}}{{\operatorname{{var}}(x)}} = \frac{{{fmt_num(cov, 4)}}}{{{fmt_num(var, 4)}}} = {fmt_num(cov / var, 4)},"
        rf"\qquad b_0 = \bar y - b_1 \bar x = {fmt_num(fit['ybar'], 3)} - {fmt_num(fit['b1'], 3)}\cdot {fmt_num(fit['xbar'], 3)} = {fmt_num(fit['b0'], 4)}"
    )
    e = fit["e"]
    checks = pd.DataFrame(
        {
            "property": ["Σ eᵢ = 0 (residuals orthogonal to the column of 1s)", "Σ xᵢ eᵢ = 0 (residuals orthogonal to x)", "line passes through (x̄, ȳ)", "mean of ŷ equals ȳ", "normal-equation solve = cov/var formula"],
            "value": [float(e.sum()), float(np.sum(x * e)), fit["b0"] + fit["b1"] * fit["xbar"] - fit["ybar"], float(fit["yhat"].mean() - fit["ybar"]), float(np.max(np.abs(beta - [fit["b0"], fit["b1"]])))],
        }
    )
    scale = max(1.0, float(np.max(np.abs(y))) * n, float(np.max(np.abs(x * y))) * n)
    checks["holds?"] = ["✅" if abs(v) <= 1e-9 * scale else "❌" for v in checks["value"]]
    st.dataframe(checks.assign(value=checks["value"].map(lambda v: f"{v:.2e}")), width="stretch", hide_index=True)
    st.caption(rf"cond(XᵀX) = {np.linalg.cond(xtx):.1f} — large values mean nearly identical x's and a fragile slope.")


def worked_example(x, y, fit):
    st.header("🔢 Worked example (live from the lab)")
    k = min(5, fit["n"])
    df = pd.DataFrame({"xᵢ": x[:k], "yᵢ": y[:k], "ŷᵢ = b₀ + b₁xᵢ": fit["yhat"][:k], "eᵢ = yᵢ − ŷᵢ": fit["e"][:k], "eᵢ²": fit["e"][:k] ** 2})
    st.dataframe(df.round(4), width="stretch", hide_index=True)
    x1, y1, yh1 = float(x[0]), float(y[0]), float(fit["yhat"][0])
    st.latex(rf"e_1 = y_1 - (b_0 + b_1 x_1) = {fmt_num(y1, 3)} - ({fmt_num(fit['b0'], 3)} {fmt_signed(fit['b1'], 3)}\cdot {fmt_num(x1, 3)}) = {fmt_num(y1 - yh1, 3)}")
    mse = fit["sse"] / fit["n"]
    st.latex(rf"\text{{SSE}} = \sum_{{i=1}}^{{{fit['n']}}} e_i^2 = {fmt_num(fit['sse'], 3)},\quad \text{{MSE}} = \frac{{\text{{SSE}}}}{{n}} = {fmt_num(mse, 4)},\quad \text{{RMSE}} = {fmt_num(float(np.sqrt(mse)), 4)}")


def projection_lab():
    st.header("📐 Geometric view: least squares is a projection")
    st.markdown(
        r"""
Stack the $n$ targets into one vector $y\in\mathbb R^n$. Every possible prediction $Xb = b_0\mathbf 1 + b_1 x$ lives in the
**plane spanned by the columns** $\mathbf 1$ and $x$. Least squares picks the point $\hat y$ in that plane closest to $y$ —
the **orthogonal projection** $\hat y = X(X^\top X)^{-1}X^\top y$ — so the residual $e = y-\hat y$ is **perpendicular** to the
plane. That is exactly why $\sum e_i = e\cdot\mathbf 1 = 0$ and $\sum x_i e_i = e\cdot x = 0$. With $n=3$ we can draw it:
$x = (1, 2, 4)$, you choose $y$.
"""
    )
    c = st.columns(3)
    yv = np.array([c[i].slider(f"y{i + 1}", -3.0, 5.0, v, 0.1, key=f"p43_y{i + 1}") for i, v in enumerate((1.0, 3.5, 2.0))])
    X = np.column_stack([np.ones(3), np.array([1.0, 2.0, 4.0])])
    beta = np.linalg.solve(X.T @ X, X.T @ yv)
    yhat = X @ beta
    e = yv - yhat
    s, t = np.meshgrid(np.linspace(-2, 4, 2), np.linspace(-1.5, 1.5, 2))
    plane = s[..., None] * X[:, 0] + t[..., None] * X[:, 1]
    fig = go.Figure()
    fig.add_trace(go.Surface(x=plane[..., 0], y=plane[..., 1], z=plane[..., 2], opacity=0.35, showscale=False, colorscale=[[0, "#4ECDC4"], [1, "#4ECDC4"]], name="column space"))
    for vec, start, color, name in ((yv, np.zeros(3), "white", "y"), (yhat, np.zeros(3), "#FFD166", "ŷ (projection)"), (yv, yhat, "#FF6B6B", "e = y − ŷ")):
        pts = np.vstack([start, vec])
        fig.add_trace(go.Scatter3d(x=pts[:, 0], y=pts[:, 1], z=pts[:, 2], mode="lines+markers", line=dict(color=color, width=7), marker=dict(size=3), name=name))
    fig.update_layout(template="plotly_dark", height=460, margin=dict(l=0, r=0, t=30, b=0), scene=dict(xaxis_title="point 1", yaxis_title="point 2", zaxis_title="point 3", aspectmode="cube"))
    st.plotly_chart(fig, width="stretch")
    st.latex(
        rf"\hat y = ({fmt_num(yhat[0], 3)}, {fmt_num(yhat[1], 3)}, {fmt_num(yhat[2], 3)}),\; e = ({fmt_num(e[0], 3)}, {fmt_num(e[1], 3)}, {fmt_num(e[2], 3)}),\;"
        rf"e\cdot\mathbf 1 = {e.sum():.1e},\; e\cdot x = {float(e @ X[:, 1]):.1e}"
    )
    hat = X @ np.linalg.solve(X.T @ X, X.T)
    st.caption(f"The diagonal of the projection ('hat') matrix H = X(XᵀX)⁻¹Xᵀ is the leverage: ({', '.join(fmt_num(v, 3) for v in np.diag(hat))}), summing to {fmt_num(float(np.trace(hat)), 3)} = p.")
    safe_page_link("pages/77Projections — Shadows onto Subspaces.py", "More on projections: Page 77 — Projections — Shadows onto Subspaces", icon="🔦")


def ai_connection():
    st.header("🤖 Where this shows up in AI")
    c1, c2, c3 = st.columns(3)
    with c1.container(border=True):
        st.markdown(
            r"""
**The simplest neural network.** A single neuron with no activation, $\hat y = w x + b$, trained with MSE loss *is*
linear regression. Least squares solves it in one shot via the normal equations; gradient descent (pages 52–56) reaches
the same $w, b$ step by step — and that is the only option once the model is non-linear.
"""
        )
    with c2.container(border=True):
        st.markdown(
            r"""
**Residual analysis = model debugging.** Plot errors against predictions, inputs, or data slices (time, region,
user group). A pattern means the model is missing structure; a funnel means it is more uncertain in some regions;
a handful of huge errors often turns out to be mislabeled or high-leverage data.
"""
        )
    with c3.container(border=True):
        st.markdown(
            r"""
**"Residual connections" (ResNets, Transformers) are a *different* idea.** A block outputs $x + F(x)$, so its layers
only need to learn the *residual* $F(x) = H(x) - x$ between desired output and input. They share the word "what is left
over", not the least-squares machinery.
"""
        )


def takeaways():
    st.header("✅ Key takeaways")
    st.markdown(
        r"""
- A residual is $e_i = y_i - \hat y_i$; least squares minimises $\sum e_i^2$, giving $b_1 = S_{xy}/S_{xx} = \operatorname{cov}(x,y)/\operatorname{var}(x)$ and $b_0 = \bar y - b_1\bar x$.
- With an intercept, residuals always sum to 0 and are orthogonal to $x$: the fit is a **projection** onto the column space of $X$.
- $R^2 = 1-\text{SSE}/\text{SST}$ is the explained share of variance — useful, but read the **residual plot** to see *how* the model fails.
- Points far out in $x$ have high **leverage**; with a large residual they become **influential** (large Cook's distance).
- No unique fit exists with $n<2$ or identical $x$'s ($X^\top X$ singular).
"""
    )
    c1, c2 = st.columns(2)
    with c1:
        safe_page_link("pages/42Scatter Plot & Line of Best Fit.py", "Previous: Page 42 — Scatter Plot & Line of Best Fit", icon="⬅️")
    with c2:
        safe_page_link("pages/44What is a Derivative.py", "Next: Page 44 — What is a Derivative", icon="➡️")


def main():
    intuition()
    result = fit_lab()
    if result is not None:
        worked_example(*result)
    projection_lab()
    ai_connection()
    takeaways()


main()
