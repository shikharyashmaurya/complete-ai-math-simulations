import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from scipy.special import xlogy

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="89 · Mutual Information", page_icon="🔗", layout="wide")

PRESETS = ["Independent", "Deterministic copy", "Noisy channel", "Custom (edit the table)"]
MARGINALS = {2: (np.array([0.3, 0.7]), np.array([0.6, 0.4])), 3: (np.array([0.2, 0.3, 0.5]), np.array([0.5, 0.3, 0.2]))}
CUSTOM_DEFAULT = {2: [[4.0, 1.0], [1.0, 4.0]], 3: [[3.0, 1.0, 0.0], [1.0, 3.0, 1.0], [0.0, 1.0, 3.0]]}


def H(p):
    """Shannon entropy in bits of any array of probabilities (0·log 0 = 0)."""
    p = np.asarray(p, dtype=float).ravel()
    return float(-np.sum(xlogy(p, p)) / np.log(2)) + 0.0  # + 0.0 turns −0.0 into 0.0


def kl_bits(p, q):
    """KL(p‖q) in bits; terms with p = 0 contribute 0 (q > 0 wherever p > 0 for q = product of p's marginals)."""
    p, q = np.asarray(p, dtype=float).ravel(), np.asarray(q, dtype=float).ravel()
    mask = p > 0
    return float(np.sum(p[mask] * np.log2(p[mask] / q[mask])))


def info_quantities(P):
    px, py = P.sum(axis=1), P.sum(axis=0)
    hx, hy, hxy = H(px), H(py), H(P)
    mi = max(hx + hy - hxy, 0.0)  # clamp −1e-16 rounding noise
    return dict(px=px, py=py, hx=hx, hy=hy, hxy=hxy, hy_x=hxy - hx, hx_y=hxy - hy, mi=mi, kl=kl_bits(P, np.outer(px, py)))


def channel_table(k, eps):
    """Uniform input through a k-ary symmetric channel: correct w.p. 1 − ε, else uniformly one of the other k − 1 symbols."""
    P = np.full((k, k), eps / (k - 1) / k)
    np.fill_diagonal(P, (1 - eps) / k)
    return P


def channel_mi_formula(k, eps):
    """I = log2 k − H(1 − ε, ε/(k−1), …): for k = 2 this is 1 − H_b(ε)."""
    return np.log2(k) - H(np.r_[1 - eps, np.full(k - 1, eps / (k - 1))])


def render_intuition():
    st.title("🔗 Mutual Information")
    st.markdown(
        "Entropy measures how uncertain one variable is. **Mutual information** measures how much uncertainty about $Y$ disappears "
        "once you learn $X$ — the number of **bits** the two variables share. Zero means independent; it catches *any* dependence, "
        "not just straight lines."
    )
    c1, c2 = st.columns(2)
    with c1, st.container(border=True):
        st.markdown("**Three equivalent definitions** (all in bits, log₂)")
        st.latex(r"I(X;Y) = H(X) + H(Y) - H(X,Y) = H(Y) - H(Y\mid X) = H(X) - H(X\mid Y)")
    with c2, st.container(border=True):
        st.markdown("**As a KL divergence** — distance from independence")
        st.latex(r"I(X;Y) = D_{\mathrm{KL}}\big(p(x,y)\,\|\,p(x)\,p(y)\big) = \sum_{x,y} p(x,y)\log_2\frac{p(x,y)}{p(x)p(y)} \;\ge 0")
    st.info("Units: this page uses **bits** (log₂), like the Entropy, Cross-Entropy and KL pages. Libraries such as scikit-learn report **nats** (ln); divide nats by ln 2 ≈ 0.693 to get bits.")


def read_custom_table(k):
    st.caption("Type any non-negative weights (counts or probabilities); they are normalized to sum to 1.")
    default = pd.DataFrame(CUSTOM_DEFAULT[k], index=[f"x={i}" for i in range(k)], columns=[f"y={j}" for j in range(k)])
    edited = st.data_editor(
        default,
        key=f"p89_editor_{k}",
        column_config={c: st.column_config.NumberColumn(c, min_value=0.0, step=0.1) for c in default.columns},
        num_rows="fixed",
    )
    W = edited.apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float)
    if np.isnan(W).any():
        st.warning("Empty or non-numeric cells were treated as 0.")
        W = np.nan_to_num(W, nan=0.0)
    if (W < 0).any():
        st.warning("Negative weights are not probabilities — they were set to 0.")
        W = np.clip(W, 0.0, None)
    if not np.isfinite(W).all():
        st.warning("Infinite weights were set to 0.")
        W = np.where(np.isfinite(W), W, 0.0)
    total = W.sum()
    if total <= 0:
        st.error("All weights are 0 — there is no distribution to normalize. Showing the uniform table instead.")
        return np.full((k, k), 1.0 / k**2)
    return W / total


def render_joint_lab():
    st.header("🧩 Lab 1 — Build a joint distribution, read off the bits")
    left, right = st.columns([1, 2], gap="large")
    with left:
        size = st.radio("Table size", ["2×2", "3×3"], horizontal=True, key="p89_size")
        k = 2 if size == "2×2" else 3
        preset = st.selectbox("Preset", PRESETS, key="p89_preset")
        eps = None
        if preset == "Independent":
            px, py = MARGINALS[k]
            P = np.outer(px, py)
            st.caption("p(x, y) = p(x)·p(y): knowing X tells nothing about Y.")
        elif preset == "Deterministic copy":
            P = np.diag(MARGINALS[k][0])
            st.caption("Y = X always: knowing X removes all uncertainty about Y.")
        elif preset == "Noisy channel":
            eps = st.slider("Flip probability ε", 0.0, 1.0, 0.1, 0.01, key="p89_eps")
            P = channel_table(k, eps)
            st.caption("X uniform; Y = X with prob. 1 − ε, otherwise one of the other symbols uniformly.")
        else:
            P = read_custom_table(k)
    q = info_quantities(P)

    with right:
        fig = make_subplots(rows=1, cols=2, subplot_titles=("joint p(x, y)", "independent version p(x)·p(y)"), horizontal_spacing=0.12)
        labels_x, labels_y = [f"x={i}" for i in range(k)], [f"y={j}" for j in range(k)]
        for col, M in ((1, P), (2, np.outer(q["px"], q["py"]))):
            fig.add_trace(go.Heatmap(z=M, x=labels_y, y=labels_x, zmin=0, zmax=float(P.max()), colorscale="Viridis", showscale=col == 2, text=np.round(M, 3), texttemplate="%{text}"), row=1, col=col)
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(height=300, margin=dict(t=40, b=20))
        st.plotly_chart(fig, width="stretch")
        table = pd.DataFrame(P, index=labels_x, columns=labels_y)
        table["p(x)"] = q["px"]
        table.loc["p(y)"] = list(q["py"]) + [1.0]
        st.dataframe(table.style.format("{:.4f}"), width="stretch")

    cols = st.columns(6)
    for c, (label, val) in zip(cols, [("H(X)", q["hx"]), ("H(Y)", q["hy"]), ("H(X,Y)", q["hxy"]), ("H(Y|X)", q["hy_x"]), ("H(X|Y)", q["hx_y"]), ("I(X;Y)", q["mi"])]):
        c.metric(label, f"{val:.4f} bits")
    return P, k, eps, q


def render_info_diagram(q):
    st.subheader("📐 Information diagram")
    hx_y, mi, hy_x = q["hx_y"], q["mi"], q["hy_x"]
    rows = ["H(X,Y)", "H(Y)", "H(X)"]
    segments = [
        ("H(X|Y) — only in X", "#60a5fa", [hx_y, 0.0, hx_y], [0.0, 0.0, 0.0]),
        ("I(X;Y) — shared", "#fbbf24", [mi, mi, mi], [hx_y, hx_y, hx_y]),
        ("H(Y|X) — only in Y", "#34d399", [hy_x, hy_x, 0.0], [hx_y + mi, hx_y + mi, 0.0]),
    ]
    fig = go.Figure()
    for name, color, widths, bases in segments:
        fig.add_trace(go.Bar(y=rows, x=widths, base=bases, orientation="h", name=name, marker_color=color, text=[f"{w:.3f}" if w > 1e-9 else "" for w in widths], textposition="inside"))
    fig.update_layout(barmode="overlay", height=260, xaxis_title="bits", margin=dict(t=20, b=40), legend=dict(orientation="h", y=-0.35))
    st.plotly_chart(fig, width="stretch")
    st.caption("The overlap of the H(X) and H(Y) bars is I(X;Y); together they span H(X,Y). Conditioning never increases entropy: H(Y|X) ≤ H(Y).")


def render_worked_example(P, k, eps, q):
    st.subheader("🧮 Worked example — the same number three ways")
    st.latex(rf"I = H(X) + H(Y) - H(X,Y) = {q['hx']:.4f} + {q['hy']:.4f} - {q['hxy']:.4f} = {q['mi']:.4f}\text{{ bits}}")
    hy_given = [H(P[i] / q["px"][i]) if q["px"][i] > 0 else 0.0 for i in range(k)]
    terms = " + ".join(rf"{q['px'][i]:.3f}\times{hy_given[i]:.3f}" for i in range(k))
    hy_x_direct = float(np.dot(q["px"], hy_given))
    st.latex(rf"H(Y\mid X) = \sum_x p(x)\,H(Y\mid X=x) = {terms} = {hy_x_direct:.4f}\;\Rightarrow\; H(Y) - H(Y\mid X) = {q['hy'] - hy_x_direct:.4f}")
    st.latex(rf"D_{{\mathrm{{KL}}}}\big(p(x,y)\,\|\,p(x)p(y)\big) = {q['kl']:.4f}\text{{ bits}}")
    if eps is not None:
        formula = channel_mi_formula(k, eps)
        if k == 2:
            st.latex(rf"\text{{Binary symmetric channel: }} I = 1 - H_b(\varepsilon) = 1 - H_b({eps:.2f}) = {formula:.4f}\text{{ bits}}")
        else:
            st.latex(rf"\text{{3-ary symmetric channel: }} I = \log_2 3 - H\!\left(1-\varepsilon, \tfrac{{\varepsilon}}{{2}}, \tfrac{{\varepsilon}}{{2}}\right) = {formula:.4f}\text{{ bits}}")
        es = np.linspace(0, 1, 201)
        fig = go.Figure(go.Scatter(x=es, y=[channel_mi_formula(k, e) for e in es], mode="lines", line=dict(color="#a78bfa", width=3), name="closed form"))
        fig.add_trace(go.Scatter(x=[eps], y=[q["mi"]], mode="markers", marker=dict(size=13, color="#fbbf24", symbol="star"), name="computed from the table"))
        fig.update_layout(title="Channel capacity curve: I(X;Y) vs flip probability", xaxis_title="ε", yaxis_title="I (bits)", height=320, margin=dict(t=50, b=40))
        st.plotly_chart(fig, width="stretch")
        st.caption(f"Minimum at ε = {(k - 1) / k:.2f}, where the output is independent of the input. For k = 2, ε = 1 is a perfect *inverter* — still 1 bit, because a flipped copy is as informative as a copy.")
    st.success(f"Decision-tree view: if Y is the label and X a candidate split, the **information gain** H(Y) − H(Y|X) of this split is {q['mi']:.4f} bits.")


def binned_mi_bits(x, y, bins):
    counts, _, _ = np.histogram2d(x, y, bins=bins)
    total = counts.sum()
    if total == 0:
        return 0.0
    P = counts / total
    return max(H(P.sum(axis=1)) + H(P.sum(axis=0)) - H(P), 0.0)


def render_mi_vs_corr():
    st.header("〰️ Lab 2 — MI vs correlation: dependence that correlation misses")
    left, right = st.columns([1, 2], gap="large")
    with left:
        rel = st.radio("Relationship", ["y = x² + noise", "y = x + noise", "independent"], key="p89_rel")
        n = st.slider("Samples n", 100, 5000, 1000, 100, key="p89_n")
        noise = st.slider("Noise SD", 0.0, 0.5, 0.05, 0.01, key="p89_noise")
        bins = st.slider("Histogram bins per axis", 2, 40, 10, key="p89_bins")
        if "p89_seed" not in st.session_state:
            st.session_state["p89_seed"] = 89
        if st.button("🎲 Resample", key="p89_resample"):
            st.session_state["p89_seed"] += 1
        use_sklearn = st.checkbox("Also run scikit-learn's k-NN estimator", value=False, key="p89_sklearn")
    seed = st.session_state["p89_seed"]
    rng = np.random.default_rng(seed)
    x = rng.uniform(-1, 1, n)
    eps = rng.normal(0, 1, n) * noise
    y = x**2 + eps if rel.startswith("y = x²") else (x + eps if rel.startswith("y = x ") else rng.uniform(-1, 1, n))
    r = float(np.corrcoef(x, y)[0, 1]) if np.std(y) > 0 else 0.0
    mi = binned_mi_bits(x, y, bins)
    mi_shuffled = binned_mi_bits(x, rng.permutation(y), bins)
    bias_mm = (bins - 1) ** 2 / (2 * n * np.log(2))

    with left:
        m1, m2 = st.columns(2)
        m1.metric("Pearson r", f"{r:+.3f}")
        m2.metric("Binned MI", f"{mi:.3f} bits")
        m3, m4 = st.columns(2)
        m3.metric("MI after shuffling y", f"{mi_shuffled:.3f} bits", help="Shuffling destroys the dependence, so this is pure estimator bias.")
        m4.metric("Bias ≈ (b−1)²/(2n ln 2)", f"{bias_mm:.3f} bits")
        if use_sklearn:
            from sklearn.feature_selection import mutual_info_regression

            mi_knn = float(mutual_info_regression(x.reshape(-1, 1), y, random_state=seed)[0])
            st.metric("sklearn mutual_info_regression", f"{mi_knn / np.log(2):.3f} bits", f"{mi_knn:.3f} nats", delta_color="off", delta_arrow="off")
    with right:
        fig = make_subplots(rows=1, cols=2, subplot_titles=(f"scatter (r = {r:+.2f})", f"{bins}×{bins} binned joint p(x, y)"))
        fig.add_trace(go.Scatter(x=x[:2000], y=y[:2000], mode="markers", marker=dict(size=4, color="#60a5fa", opacity=0.6), showlegend=False), row=1, col=1)
        counts, xe, ye = np.histogram2d(x, y, bins=bins)
        fig.add_trace(go.Heatmap(z=(counts / max(counts.sum(), 1)).T, x=(xe[:-1] + xe[1:]) / 2, y=(ye[:-1] + ye[1:]) / 2, colorscale="Viridis", showscale=False), row=1, col=2)
        fig.update_xaxes(title_text="x")
        fig.update_yaxes(title_text="y", row=1, col=1)
        fig.update_layout(height=380, margin=dict(t=50, b=40))
        st.plotly_chart(fig, width="stretch")
    st.markdown(
        "With **y = x²** the correlation is ≈ 0 (the left half slopes down, the right half up, and they cancel), yet MI is large: knowing x pins down y. "
        "Correlation only measures *linear* dependence; MI measures *any* dependence."
    )
    st.warning(
        "**Estimator caveats.** The plug-in (binned) estimate is biased *upward* — even independent data show MI > 0, roughly (bins−1)²/(2n ln 2) bits — "
        "and it depends on the bin count. For a noiseless continuous relation the true MI is infinite, so the estimate just keeps growing with more bins. "
        "Compare MI values only at the same n and binning, and subtract a shuffled baseline."
    )


def render_ai_connection():
    st.header("🤖 AI / ML connection")
    c1, c2, c3 = st.columns(3)
    with c1, st.container(border=True):
        st.markdown("**Feature selection**")
        st.markdown(
            r"Rank features by $I(\text{feature};\text{label})$ — e.g. `sklearn.feature_selection.mutual_info_classif` (k-NN estimator, **nats**). "
            "Unlike correlation it keeps features with non-linear, even non-monotone, relationships such as y = x²."
        )
    with c2, st.container(border=True):
        st.markdown("**Contrastive learning (InfoNCE)**")
        st.markdown(
            "CLIP and SimCLR train encoders so matching pairs score higher than $N-1$ negatives. The InfoNCE loss gives a lower bound "
            r"$I(X;Y) \ge \log N - \mathcal L_{\text{InfoNCE}}$ — minimizing the loss maximizes shared information between views."
        )
    with c3, st.container(border=True):
        st.markdown("**Decision trees**")
        st.markdown(
            r"ID3/C4.5 split on the feature with the largest **information gain** $H(Y)-H(Y\mid X)$, which is exactly $I(X;Y)$ — "
            "entropy reduction from the Entropy page, with sklearn's `criterion='entropy'`."
        )


def render_takeaways():
    st.header("📌 Key takeaways")
    st.markdown(
        r"""
- $I(X;Y)=H(X)+H(Y)-H(X,Y)=D_{\mathrm{KL}}\big(p(x,y)\|p(x)p(y)\big)\ge 0$, measured here in bits.
- $I=0$ exactly when X and Y are independent; a deterministic copy gives $I=H(X)$, the maximum.
- A binary symmetric channel with uniform input carries $1-H_b(\varepsilon)$ bits — zero at $\varepsilon=0.5$.
- MI sees non-linear dependence that correlation misses, but estimating it from samples is biased and binning-dependent.
- In ML: feature selection, information gain in trees, InfoNCE in contrastive learning.
"""
    )
    c1, c2 = st.columns(2)
    with c1:
        safe_page_link("pages/60KL Divergence — Gap Between Distributions.py", "← Previous: 60 · KL Divergence", icon="⬅️")
    with c2:
        safe_page_link("pages/61Eigenvectors — Vectors That Don't Rotate.py", "Next: 61 · Eigenvectors →", icon="➡️")
    c3, c4, c5 = st.columns(3)
    with c3:
        safe_page_link("pages/58Entropy — Average Uncertainty.py", "Related: 58 · Entropy", icon="🔗")
    with c4:
        safe_page_link("pages/84Joint & Marginal Distributions.py", "Related: 84 · Joint & Marginal Distributions", icon="🔗")
    with c5:
        safe_page_link("pages/88Confidence Intervals & Hypothesis Tests.py", "Related: 88 · Confidence Intervals & Hypothesis Tests", icon="🔗")


def main():
    render_intuition()
    st.divider()
    P, k, eps, q = render_joint_lab()
    render_info_diagram(q)
    render_worked_example(P, k, eps, q)
    st.divider()
    render_mi_vs_corr()
    st.divider()
    render_ai_connection()
    st.divider()
    render_takeaways()


main()
