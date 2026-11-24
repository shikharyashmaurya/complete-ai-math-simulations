import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from scipy import stats

st.set_page_config(page_title="84 · Joint & Marginal Distributions", page_icon="🎲", layout="wide")

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.nav import safe_page_link  # noqa: E402

WEATHER = ["☀️ Sunny", "☁️ Cloudy", "🌧️ Rainy"]
ACTIVITY = ["🚶 Walk", "🏋️ Gym", "🎬 Movie"]
DEFAULT_COUNTS = np.array([[30.0, 10.0, 5.0], [12.0, 10.0, 8.0], [3.0, 9.0, 13.0]])
MAX_COUNT = 1000.0
INDEP_TOL = 1e-9


def cell_key(i, j):
    return f"p84_c_{i}_{j}"


def init_state():
    for i in range(3):
        for j in range(3):
            st.session_state.setdefault(cell_key(i, j), float(DEFAULT_COUNTS[i, j]))
    st.session_state.setdefault("p84_seed", 84)


def reset_counts():
    for i in range(3):
        for j in range(3):
            st.session_state[cell_key(i, j)] = float(DEFAULT_COUNTS[i, j])


def make_independent():
    """Replace the table by the outer product of its marginals (same total, same margins)."""
    counts = read_counts()
    total = counts.sum()
    if total <= 0:
        return
    indep = np.outer(counts.sum(axis=1), counts.sum(axis=0)) / total
    if indep.max() > MAX_COUNT:  # rescaling keeps every probability, just fits the input range
        indep *= MAX_COUNT / indep.max()
    for i in range(3):
        for j in range(3):
            st.session_state[cell_key(i, j)] = float(indep[i, j])


def read_counts():
    return np.array([[float(st.session_state.get(cell_key(i, j), 0.0)) for j in range(3)] for i in range(3)])


def heatmap(z, text, title, colorscale="Blues", zmid=None):
    fig = go.Figure(
        go.Heatmap(
            z=z,
            x=ACTIVITY,
            y=WEATHER,
            text=text,
            texttemplate="%{text}",
            colorscale=colorscale,
            zmid=zmid,
            hoverongaps=False,
            showscale=False,
        )
    )
    fig.update_layout(template="plotly_dark", title=title, height=320, margin=dict(l=10, r=10, t=50, b=10))
    fig.update_yaxes(autorange="reversed")
    return fig


def fmt_cells(m, prec=3):
    return [["undefined" if np.isnan(v) else f"{v:.{prec}f}" for v in row] for row in m]


def render_intro():
    st.title("🎲 Page 84: Joint & Marginal Distributions")
    st.markdown("### One table, many questions: *how often together*, *how often at all*, *how often given*.")
    with st.container(border=True):
        st.markdown(
            r"""
**Intuition.** Keep a diary for 100 days of two things: the **weather** $X$ and what you **did** $Y$.
Counting every *(weather, activity)* pair gives the **joint distribution** $P(X=x, Y=y)$ — the full story.
Everything else is a view of that table:

* **Marginal** $P(X=x)=\sum_y P(x,y)$ — add up a row and forget about the activity.
* **Conditional** $P(Y=y\mid X=x)=P(x,y)/P(x)$ — zoom into one row and re-normalize it.
* **Independence** — the table is *exactly* the product of its margins: $P(x,y)=P(x)\,P(y)$ in every cell.

Generative AI models *are* joint distributions: a model of $p(\text{image},\text{caption})$ can be
marginalized ("any image") or conditioned ("an image **given** this caption").
"""
        )


def render_discrete_lab():
    st.header("🧪 Lab 1 — A discrete joint table")
    st.markdown("Edit the day counts (decimals allowed). Everything below is recomputed from this table.")

    cols = st.columns([1.2, 1, 1, 1])
    cols[0].markdown("**Weather \\ Activity**")
    for j, name in enumerate(ACTIVITY):
        cols[j + 1].markdown(f"**{name}**")
    for i, wname in enumerate(WEATHER):
        cols = st.columns([1.2, 1, 1, 1])
        cols[0].markdown(f"**{wname}**")
        for j in range(3):
            cols[j + 1].number_input(
                f"{wname} & {ACTIVITY[j]}",
                min_value=0.0,
                max_value=MAX_COUNT,
                step=1.0,
                format="%.2f",
                key=cell_key(i, j),
                label_visibility="collapsed",
            )

    b1, b2, _ = st.columns([1, 1, 2])
    b1.button("🔗 Make independent (outer product of marginals)", key="p84_make_indep", on_click=make_independent)
    b2.button("↩️ Reset example table", key="p84_reset", on_click=reset_counts)

    counts = read_counts()
    total = counts.sum()
    if total <= 0:
        st.warning("All counts are zero — a probability table needs at least one observation. Enter some counts.")
        return None

    joint = counts / total
    px = joint.sum(axis=1)
    py = joint.sum(axis=0)
    with np.errstate(invalid="ignore", divide="ignore"):
        y_given_x = np.where(px[:, None] > 0, joint / px[:, None], np.nan)
        x_given_y = np.where(py[None, :] > 0, joint / py[None, :], np.nan)
    product = np.outer(px, py)
    diff = joint - product
    max_diff = float(np.abs(diff).max())

    t1, t2, t3 = st.tabs(["Joint & marginals", "Conditionals", "Independence check"])
    with t1:
        c1, c2 = st.columns([2, 1])
        with c1:
            st.plotly_chart(heatmap(joint, fmt_cells(joint), f"Joint P(X, Y)  (N = {total:g} days)"), width="stretch")
        with c2:
            table = pd.DataFrame(joint, index=WEATHER, columns=ACTIVITY)
            table["P(X) row sum"] = px
            table.loc["P(Y) col sum"] = list(py) + [joint.sum()]
            st.dataframe(table.style.format("{:.3f}"), width="stretch")
            st.caption("Margins are written in the *margins* of the table — that is where the name comes from.")
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Marginal P(X = weather)", "Marginal P(Y = activity)"))
        fig.add_trace(go.Bar(x=WEATHER, y=px, marker_color="#38bdf8", text=[f"{v:.3f}" for v in px]), 1, 1)
        fig.add_trace(go.Bar(x=ACTIVITY, y=py, marker_color="#f59e0b", text=[f"{v:.3f}" for v in py]), 1, 2)
        fig.update_layout(template="plotly_dark", height=300, showlegend=False, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig, width="stretch")

    with t2:
        cond_on = st.radio(
            "Condition on", ["Weather X (normalize rows)", "Activity Y (normalize columns)"],
            horizontal=True, key="p84_cond_on",
        )
        if cond_on.startswith("Weather"):
            st.plotly_chart(
                heatmap(y_given_x, fmt_cells(y_given_x), "P(Y | X): each ROW sums to 1", "Greens"), width="stretch"
            )
            empty = [WEATHER[i] for i in range(3) if px[i] == 0]
        else:
            st.plotly_chart(
                heatmap(x_given_y, fmt_cells(x_given_y), "P(X | Y): each COLUMN sums to 1", "Purples"),
                width="stretch",
            )
            empty = [ACTIVITY[j] for j in range(3) if py[j] == 0]
        if empty:
            st.warning(f"Conditioning on an event with probability 0 is undefined: {', '.join(empty)}.")
        st.markdown(r"Conditioning = keep one slice of the joint table and divide by its total: $P(y\mid x)=P(x,y)/P(x)$.")

    with t3:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(heatmap(product, fmt_cells(product), "P(X)·P(Y)  (what independence predicts)"),
                            width="stretch")
        with c2:
            st.plotly_chart(
                heatmap(diff, [[f"{v:+.3f}" for v in row] for row in diff], "P(X,Y) − P(X)P(Y)", "RdBu", zmid=0),
                width="stretch",
            )
        st.metric("Largest cell gap  max |P(x,y) − P(x)P(y)|", f"{max_diff:.4f}")
        if max_diff < INDEP_TOL:
            st.success("Every cell satisfies P(x,y) = P(x)P(y): weather and activity are **independent**. "
                       "Every conditional row now equals the marginal P(Y).")
        else:
            st.info("At least one cell breaks P(x,y) = P(x)P(y), so X and Y are **dependent**: knowing the weather "
                    "changes the odds of each activity. Press *Make independent* to keep the same margins but "
                    "remove the dependence.")
    return joint, px, py


def render_discrete_example(joint, px, py):
    st.header("🧮 Worked example — one cell, four probabilities")
    c1, c2 = st.columns(2)
    wi = c1.selectbox("Weather x", range(3), format_func=lambda i: WEATHER[i], key="p84_ex_w")
    aj = c2.selectbox("Activity y", range(3), format_func=lambda j: ACTIVITY[j], key="p84_ex_a")
    pxy, pxi, pyj = joint[wi, aj], px[wi], py[aj]
    st.latex(rf"P(x,y) = {pxy:.4f}, \qquad P(x)=\sum_{{y'}} P(x,y') = {pxi:.4f}, \qquad "
             rf"P(y)=\sum_{{x'}} P(x',y) = {pyj:.4f}")
    if pxi > 0:
        st.latex(rf"P(y\mid x) = \frac{{P(x,y)}}{{P(x)}} = \frac{{{pxy:.4f}}}{{{pxi:.4f}}} = {pxy / pxi:.4f}")
    else:
        st.latex(r"P(y\mid x)\ \text{is undefined because } P(x)=0")
    st.latex(rf"P(x)\,P(y) = {pxi:.4f}\times{pyj:.4f} = {pxi * pyj:.4f} \quad\text{{vs}}\quad P(x,y) = {pxy:.4f}")
    st.caption("Chain rule check: P(x,y) = P(x)·P(y|x) — the joint is always a marginal times a conditional.")


def covariance_from_widgets():
    c1, c2, c3 = st.columns(3)
    with c1:
        mx = st.slider("μx (mean of X)", -3.0, 3.0, 0.0, 0.1, key="p84_mx")
        my = st.slider("μy (mean of Y)", -3.0, 3.0, 0.0, 0.1, key="p84_my")
    with c2:
        sx = st.slider("σx (std of X)", 0.2, 3.0, 1.0, 0.1, key="p84_sx")
        sy = st.slider("σy (std of Y)", 0.2, 3.0, 1.5, 0.1, key="p84_sy")
    with c3:
        mode = st.radio("Set the dependence by", ["Correlation ρ", "Covariance σxy directly"], key="p84_mode")
        if mode.startswith("Correlation"):
            rho = st.slider("ρ (correlation)", -1.0, 1.0, 0.7, 0.05, key="p84_rho")
            sxy = rho * sx * sy
        else:
            sxy = st.number_input("σxy = Cov(X, Y)", -10.0, 10.0, 1.0, 0.1, key="p84_sxy")
    return mx, my, sx, sy, float(sxy)


def render_continuous_lab():
    st.header("🧪 Lab 2 — Continuous: the bivariate Gaussian")
    mx, my, sx, sy, sxy = covariance_from_widgets()
    cov = np.array([[sx**2, sxy], [sxy, sy**2]])
    eig = np.linalg.eigvalsh(cov)
    det = float(np.linalg.det(cov))

    c1, c2 = st.columns([1, 1])
    with c1:
        st.latex(rf"\Sigma = \begin{{bmatrix}} \sigma_x^2 & \sigma_{{xy}} \\ \sigma_{{xy}} & \sigma_y^2 \end{{bmatrix}}"
                 rf"= \begin{{bmatrix}} {sx**2:.3f} & {sxy:.3f} \\ {sxy:.3f} & {sy**2:.3f} \end{{bmatrix}}")
    with c2:
        st.latex(rf"\det\Sigma = {det:.4f}, \quad \lambda_{{1,2}} = {eig[0]:.4f},\ {eig[1]:.4f}")
    if eig[0] < -1e-12:
        st.error(
            f"Not a valid covariance matrix: it has a negative eigenvalue ({eig[0]:.4f}), i.e. det Σ < 0. "
            f"A covariance must be positive semi-definite, which here means |σxy| ≤ σx·σy = {sx * sy:.2f} "
            "(equivalently |ρ| ≤ 1). Lower |σxy| to continue."
        )
        return
    rho = sxy / (sx * sy)
    singular = eig[0] <= 1e-10 * eig[1]
    st.caption(f"Implied correlation ρ = σxy / (σx σy) = {rho:.3f}. See pages 40 (Covariance) and 41 (Pearson).")

    s1, s2, s3 = st.columns([2, 2, 1])
    n = s1.slider("Number of samples", 100, 5000, 1500, 100, key="p84_n")
    z0 = s2.slider("Slice position y₀ (in σy from μy)", -2.5, 2.5, 1.0, 0.1, key="p84_z0")
    if s3.button("🎲 Resample", key="p84_resample"):
        st.session_state["p84_seed"] += 1
    y0 = my + z0 * sy

    rng = np.random.default_rng(st.session_state["p84_seed"])
    vals, vecs = np.linalg.eigh(cov)
    root = vecs * np.sqrt(np.clip(vals, 0.0, None))  # works for singular Σ too (no Cholesky needed)
    samples = np.array([mx, my]) + rng.standard_normal((n, 2)) @ root.T

    xs = np.linspace(mx - 3.5 * sx, mx + 3.5 * sx, 160)
    ys = np.linspace(my - 3.5 * sy, my + 3.5 * sy, 160)
    fig = make_subplots(
        rows=2, cols=2, column_widths=[0.78, 0.22], row_heights=[0.22, 0.78],
        shared_xaxes=True, shared_yaxes=True, horizontal_spacing=0.02, vertical_spacing=0.02,
    )
    fig.add_trace(go.Histogram(x=samples[:, 0], histnorm="probability density", nbinsx=40,
                               marker_color="#38bdf8", opacity=0.6, name="samples of X"), 1, 1)
    fig.add_trace(go.Scatter(x=xs, y=stats.norm.pdf(xs, mx, sx), line=dict(color="#e2e8f0"),
                             name="marginal N(μx, σx²)"), 1, 1)
    fig.add_trace(go.Histogram(y=samples[:, 1], histnorm="probability density", nbinsy=40,
                               marker_color="#f59e0b", opacity=0.6, name="samples of Y"), 2, 2)
    fig.add_trace(go.Scatter(x=stats.norm.pdf(ys, my, sy), y=ys, line=dict(color="#e2e8f0"),
                             name="marginal N(μy, σy²)", showlegend=False), 2, 2)
    if not singular:
        gx, gy = np.meshgrid(xs, ys)
        dens = stats.multivariate_normal(mean=[mx, my], cov=cov).pdf(np.dstack([gx, gy]))
        fig.add_trace(go.Contour(x=xs, y=ys, z=dens, colorscale="Viridis", showscale=False, opacity=0.75,
                                 contours=dict(coloring="lines"), line=dict(width=2), name="joint density"), 2, 1)
    fig.add_trace(go.Scatter(x=samples[:, 0], y=samples[:, 1], mode="markers", name="joint samples",
                             marker=dict(size=3, color="#94a3b8", opacity=0.45)), 2, 1)
    fig.add_trace(go.Scatter(x=[xs[0], xs[-1]], y=[y0, y0], mode="lines", name="slice y = y₀",
                             line=dict(color="#ef4444", dash="dash", width=2)), 2, 1)
    fig.update_layout(template="plotly_dark", height=560, bargap=0.02, margin=dict(l=10, r=10, t=30, b=10),
                      legend=dict(orientation="h", y=1.08))
    fig.update_xaxes(title_text="x", row=2, col=1)
    fig.update_yaxes(title_text="y", row=2, col=1)
    st.plotly_chart(fig, width="stretch")
    st.caption("Top / right: the marginals are just the joint cloud projected onto each axis — "
               "for a Gaussian they are N(μx, σx²) and N(μy, σy²) whatever ρ is.")

    render_conditional_slice(mx, my, sx, sy, rho, cov, y0, samples, singular)


def render_conditional_slice(mx, my, sx, sy, rho, cov, y0, samples, singular):
    st.subheader("✂️ Conditional slice  p(x | y = y₀)")
    cond_mean = mx + rho * sx / sy * (y0 - my)
    cond_var = sx**2 * (1 - rho**2)
    st.latex(rf"\mathbb{{E}}[X\mid Y=y_0] = \mu_x + \rho\frac{{\sigma_x}}{{\sigma_y}}(y_0-\mu_y) = {mx:.2f} + "
             rf"({rho:.3f})\frac{{{sx:.2f}}}{{{sy:.2f}}}({y0:.2f} - {my:.2f}) = {cond_mean:.4f}")
    st.latex(rf"\operatorname{{Var}}[X\mid Y=y_0] = \sigma_x^2(1-\rho^2) = {cond_var:.4f}")

    band = 0.1 * sy
    near = samples[np.abs(samples[:, 1] - y0) < band, 0]
    if singular:
        st.warning("|ρ| = 1: Σ is singular (PSD but not invertible). All mass lies on a line, there is no density, "
                   f"and knowing y fixes x exactly: x = {cond_mean:.3f}, conditional variance 0.")
        return

    xs = np.linspace(mx - 4 * sx, mx + 4 * sx, 2001)
    raw = stats.multivariate_normal(mean=[mx, my], cov=cov).pdf(np.column_stack([xs, np.full_like(xs, y0)]))
    area = np.trapezoid(raw, xs)
    num_mean = num_var = float("nan")
    if area > 0:
        slice_pdf = raw / area
        num_mean = float(np.trapezoid(xs * slice_pdf, xs))
        num_var = float(np.trapezoid((xs - num_mean) ** 2 * slice_pdf, xs))
    else:
        slice_pdf = np.zeros_like(xs)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=stats.norm.pdf(xs, mx, sx), name="marginal p(x)",
                             line=dict(color="#e2e8f0", dash="dot")))
    fig.add_trace(go.Scatter(x=xs, y=slice_pdf, name="slice p(x, y₀) / p(y₀)", line=dict(color="#ef4444", width=3)))
    if near.size >= 2:
        fig.add_trace(go.Histogram(x=near, histnorm="probability density", nbinsx=25, opacity=0.45,
                                   marker_color="#ef4444", name=f"samples with |y − y₀| < {band:.2f}"))
    fig.add_vline(x=cond_mean, line_color="#22c55e", annotation_text="formula mean")
    fig.update_layout(template="plotly_dark", height=340, margin=dict(l=10, r=10, t=30, b=10), xaxis_title="x")
    st.plotly_chart(fig, width="stretch")

    m1, m2, m3 = st.columns(3)
    m1.metric("Formula conditional mean", f"{cond_mean:.4f}")
    m2.metric("Numerical mean of the normalized slice", f"{num_mean:.4f}", f"{num_mean - cond_mean:+.1e}")
    if near.size >= 10:
        m3.metric(f"Mean of {near.size} nearby samples", f"{near.mean():.3f}")
    else:
        m3.metric("Nearby samples", f"{near.size}", help="Too few samples near y₀ — add samples or move y₀ inward.")
    st.caption(f"Numerical variance of the slice = {num_var:.4f} vs formula {cond_var:.4f}. The slice is narrower than "
               "the marginal whenever ρ ≠ 0: observing Y removes a fraction ρ² of X's variance.")


def render_ai_connection():
    st.header("🤖 AI / ML connection")
    c1, c2, c3 = st.columns(3)
    with c1, st.container(border=True):
        st.markdown(
            r"""**Generative models learn $p(x, y)$.** A text-to-image model is a conditional $p(\text{image}\mid
\text{prompt})$; a language model factors the joint over tokens by the chain rule
$p(w_1,\dots,w_n)=\prod_t p(w_t\mid w_{<t})$ — conditionals all the way down."""
        )
    with c2, st.container(border=True):
        st.markdown(
            r"""**Naive Bayes** assumes features are *conditionally independent* given the class:
$p(x_1,\dots,x_d\mid c)=\prod_i p(x_i\mid c)$ — the "make independent" button, applied per class.
It replaces a huge joint table by $d$ small ones; cheap, but wrong when features co-vary."""
        )
    with c3, st.container(border=True):
        st.markdown(
            r"""**Multivariate Gaussians** are everywhere: a **VAE** encoder outputs $\mu$ and a (diagonal)
$\Sigma$ for $q(z\mid x)$; a **Gaussian mixture model** clusters with full covariances; Gaussian processes
predict with exactly the conditional-mean formula above."""
        )


def render_takeaways():
    st.header("✅ Key takeaways")
    st.markdown(
        r"""
* The **joint** $P(x,y)$ holds all the information; **marginals** sum it out, **conditionals** slice and re-normalize it.
* $P(x,y)=P(x)\,P(y\mid x)$ always; **independence** is the special case $P(y\mid x)=P(y)$, i.e. the table is an outer product.
* Two tables can share the *same margins* yet have very different dependence — margins alone never reveal it.
* For a bivariate Gaussian, marginals and conditionals are Gaussian; $\mathbb E[X\mid y_0]$ moves linearly in $y_0$
  with slope $\rho\,\sigma_x/\sigma_y$, and a valid $\Sigma$ must be positive semi-definite ($|\rho|\le 1$).
"""
    )
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        safe_page_link("pages/26Independence.py", "⬅️ Previous: 26 · Independence")
    with c2:
        safe_page_link("pages/40Covariance.py", "📎 Related: 40 · Covariance")
    with c3:
        safe_page_link("pages/41Pearson Correlation.py", "📎 Related: 41 · Pearson Correlation")
    with c4:
        safe_page_link("pages/85Poisson & Exponential Distributions.py", "➡️ Next: 85 · Poisson & Exponential")


def main():
    init_state()
    render_intro()
    result = render_discrete_lab()
    if result is not None:
        render_discrete_example(*result)
    st.divider()
    render_continuous_lab()
    st.divider()
    render_ai_connection()
    render_takeaways()


main()
