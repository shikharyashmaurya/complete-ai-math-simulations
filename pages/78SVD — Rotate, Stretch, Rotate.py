import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.nav import safe_page_link  # noqa: E402
from common.linalg2d import rotation_matrix  # noqa: E402
from common.mathutils import fmt_num  # noqa: E402

st.set_page_config(page_title="78 · SVD — Rotate, Stretch, Rotate", page_icon="🌀", layout="wide")

SING_TOL = 1e-12  # sigma_min / sigma_max below this = singular (condition number = ∞)
FRAMES_PER_STAGE = 12
IMG_N = 64
SHAPE_COLOR, GHOST_COLOR, V1_COLOR, V2_COLOR = "#38bdf8", "#64748b", "#fb923c", "#4ade80"
MATRIX_KEYS = ("p78_a", "p78_b", "p78_c", "p78_d")
MATRIX_PRESETS = {
    "General": (2.0, 1.0, 0.5, 1.0),
    "Shear (non-symmetric)": (1.0, 1.0, 0.0, 1.0),
    "Symmetric PSD": (2.0, 1.0, 1.0, 2.0),
    "Symmetric indefinite": (1.0, 2.0, 2.0, -1.0),
    "Rotation (σ = 1, 1)": (0.0, -1.0, 1.0, 0.0),
    "Near-singular": (1.0, 1.0, 1.0, 1.1),
    "Singular (rank 1)": (2.0, 1.0, 1.0, 0.5),
}


def bmat(M, prec=2):
    M = np.atleast_2d(np.asarray(M, dtype=float))
    rows = [" & ".join(fmt_num(v, prec) for v in row) for row in M]
    return r"\begin{bmatrix}" + r" \\ ".join(rows) + r"\end{bmatrix}"


def fmt_complex(z, prec=3):
    if abs(z.imag) < 1e-12:
        return fmt_num(z.real, prec)
    return f"{fmt_num(z.real, prec)} {'+' if z.imag > 0 else '−'} {fmt_num(abs(z.imag), prec)}i"


def condition_number(s):
    return float("inf") if s[0] == 0 or s[-1] / s[0] < SING_TOL else float(s[0] / s[-1])


def orth_path(Q, t):
    """Continuous path from I (t=0) to the orthogonal 2×2 matrix Q (t=1).

    det Q = +1: Q is a rotation R(θ) → R(tθ).  det Q = −1: Q = R(θ)·diag(1, −1) → R(tθ)·diag(1, 1 − 2t),
    i.e. the reflection is shown as a flip (y squashes through 0) while rotating.
    """
    theta = np.degrees(np.arctan2(Q[1, 0], Q[0, 0]))
    R = rotation_matrix(t * theta)
    return R if np.linalg.det(Q) > 0 else R @ np.diag([1.0, 1.0 - 2.0 * t])


def stage_matrix(U, s, Vt, t):
    """t ∈ [0, 3]: 0→1 apply Vᵀ, 1→2 stretch by Σ, 2→3 apply U.  stage_matrix(.., 3) = UΣVᵀ."""
    if t <= 1:
        return orth_path(Vt, t)
    if t <= 2:
        return np.diag(1.0 + (t - 1.0) * (s - 1.0)) @ Vt
    return orth_path(U, t - 2.0) @ np.diag(s) @ Vt


def apply_preset():
    preset = st.session_state["p78_preset"]
    if preset in MATRIX_PRESETS:
        for k, v in zip(MATRIX_KEYS, MATRIX_PRESETS[preset]):
            st.session_state[k] = v


def init_state():
    for k, v in zip(MATRIX_KEYS, MATRIX_PRESETS["General"]):
        st.session_state.setdefault(k, v)
    st.session_state.setdefault("p78_seed", 78)


def synthetic_image(kind):
    """Deterministic 64×64 grayscale test images with values in [0, 1]."""
    yy, xx = np.mgrid[0:IMG_N, 0:IMG_N] / (IMG_N - 1)
    if kind == "Smooth waves (exactly low rank)":
        return 0.5 + 0.25 * np.sin(2 * np.pi * xx) * np.cos(3 * np.pi * yy) + 0.2 * (xx - 0.5)
    if kind == "Checkerboard + disk":
        board = ((np.floor(xx * 7.999) + np.floor(yy * 7.999)) % 2) * 0.6 + 0.2
        disk = (xx - 0.5) ** 2 + (yy - 0.5) ** 2 < 0.28**2
        return np.where(disk, 1.0 - board, board)
    img = 0.15 + 0.25 * xx  # "Shapes & letters"
    img[(xx - 0.78) ** 2 + (yy - 0.25) ** 2 < 0.14**2] = 0.95
    img[(yy > 0.62) & (yy < 0.9) & (xx > 0.6) & (xx < 0.92)] = 0.7
    # Letter "A": apex (0.28, 0.12), legs down to x = 0.08 and x = 0.48 at y = 0.87, crossbar at y = 0.6.
    spread = 0.20 * (yy - 0.12) / 0.75
    legs = (np.abs(xx - (0.28 - spread)) < 0.04) | (np.abs(xx - (0.28 + spread)) < 0.04)
    img[(yy > 0.12) & (yy < 0.87) & legs] = 1.0
    img[(np.abs(yy - 0.6) < 0.035) & (xx > 0.15) & (xx < 0.41)] = 1.0
    img[(xx > 0.5) & (xx < 0.56) & (yy > 0.1) & (yy < 0.5)] = 1.0  # letter "I" with serifs
    img[(np.abs(yy - 0.1) < 0.03) & (xx > 0.46) & (xx < 0.6)] = 1.0
    img[(np.abs(yy - 0.5) < 0.03) & (xx > 0.46) & (xx < 0.6)] = 1.0
    return img


def render_intro():
    st.title("🌀 SVD — Rotate, Stretch, Rotate")
    st.markdown(
        r"""
        **Every** matrix — square or not, symmetric or not, invertible or not — can be written as
        $A = U\Sigma V^\top$: a rotation (or reflection) $V^\top$, then a stretch $\Sigma$ along the axes by the
        **singular values** $\sigma_1 \ge \sigma_2 \ge \dots \ge 0$, then another rotation (or reflection) $U$.
        So every 2×2 matrix turns the unit circle into an ellipse with semi-axes $\sigma_1, \sigma_2$.

        Ordering the pieces by $\sigma$ tells you which directions matter most — the idea behind image compression,
        PCA, LoRA fine-tuning and recommender systems.
        """
    )


def circle_figure(A, U, s, Vt):
    ang = np.linspace(0, 2 * np.pi, 121)
    circle = np.vstack([np.cos(ang), np.sin(ang)])
    V = Vt.T
    final = A @ circle
    lim = max(1.5, float(np.abs(final).max()) * 1.15, 1.2 * float(s.max()))
    ts = np.linspace(0, 3, 3 * FRAMES_PER_STAGE + 1)

    def moving(t):
        M = stage_matrix(U, s, Vt, t)
        pts, a1, a2 = M @ circle, M @ V[:, 0], M @ V[:, 1]
        return [go.Scatter(x=pts[0], y=pts[1]), go.Scatter(x=[0, a1[0]], y=[0, a1[1]]),
                go.Scatter(x=[0, a2[0]], y=[0, a2[1]])]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=circle[0], y=circle[1], mode="lines", name="unit circle",
                             line=dict(color=GHOST_COLOR, dash="dot")))
    fig.add_trace(go.Scatter(x=final[0], y=final[1], mode="lines", name="target ellipse A·circle",
                             line=dict(color=GHOST_COLOR, dash="dash")))
    start = moving(3.0)
    fig.add_trace(start[0].update(mode="lines", name="shape", line=dict(color=SHAPE_COLOR, width=3),
                                  fill="toself", fillcolor="rgba(56,189,248,0.12)"))
    for tr, color, name in ((start[1], V1_COLOR, "v₁ → σ₁u₁"), (start[2], V2_COLOR, "v₂ → σ₂u₂")):
        fig.add_trace(tr.update(mode="lines+markers", name=name, line=dict(color=color, width=4),
                                marker=dict(symbol="arrow", size=[0, 14], angleref="previous", color=color)))
    labels = ["start", "Vᵀ: rotate/reflect", "Σ: stretch", "U: rotate/reflect"]
    fig.frames = [go.Frame(data=moving(t), traces=[2, 3, 4], name=f"{t:.2f}") for t in ts]
    steps = [dict(method="animate", label=labels[int(round(t))] if abs(t - round(t)) < 1e-9 else "",
                  args=[[f"{t:.2f}"], dict(mode="immediate", frame=dict(duration=0, redraw=True))]) for t in ts]
    fig.update_layout(
        height=560, margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(range=[-lim, lim], scaleanchor="y", scaleratio=1), yaxis=dict(range=[-lim, lim]),
        legend=dict(orientation="h", y=1.02, yanchor="bottom", x=0),
        updatemenus=[dict(type="buttons", x=0, y=-0.05, xanchor="left", yanchor="top", buttons=[dict(
            label="▶ Play circle → ellipse", method="animate",
            args=[None, dict(frame=dict(duration=90, redraw=True), fromcurrent=False, mode="immediate")])])],
        sliders=[dict(active=len(ts) - 1, steps=steps, x=0.25, len=0.75, y=-0.02, currentvalue=dict(visible=False))],
    )
    return fig


def render_circle_lab():
    st.header("1) The unit circle becomes an ellipse")
    left, right = st.columns([1, 2], gap="large")
    with left:
        st.selectbox("Preset", ["Custom", *MATRIX_PRESETS], key="p78_preset", on_change=apply_preset)
        c1, c2 = st.columns(2)
        a = c1.slider("a (top-left)", -3.0, 3.0, step=0.1, key="p78_a")
        b = c2.slider("b (top-right)", -3.0, 3.0, step=0.1, key="p78_b")
        c = c1.slider("c (bottom-left)", -3.0, 3.0, step=0.1, key="p78_c")
        d = c2.slider("d (bottom-right)", -3.0, 3.0, step=0.1, key="p78_d")
    A = np.array([[a, b], [c, d]], dtype=float)
    U, s, Vt = np.linalg.svd(A)
    with right:
        st.plotly_chart(circle_figure(A, U, s, Vt), width="stretch", key="p78_fig_circle")
        st.caption("Press ▶ (or drag the slider under the plot). The orange/green arrows start as the right singular "
                   "vectors v₁, v₂; Vᵀ turns them onto the axes, Σ stretches them to lengths σ₁, σ₂, and U turns "
                   "them into the ellipse's semi-axes σ₁u₁, σ₂u₂. A reflection shows up as a flip.")
    with left:
        m1, m2 = st.columns(2)
        m1.metric("σ₁ (longest semi-axis)", fmt_num(s[0], 3))
        m2.metric("σ₂ (shortest semi-axis)", fmt_num(s[1], 3))
    st.latex(rf"{bmat(A)} = \underbrace{{{bmat(U, 3)}}}_{{U}}\underbrace{{{bmat(np.diag(s), 3)}}}_{{\Sigma}}"
             rf"\underbrace{{{bmat(Vt, 3)}}}_{{V^\top}}")
    v1, v2, v3 = st.columns(3)
    v1.metric("max |UᵀU − I|", f"{np.abs(U.T @ U - np.eye(2)).max():.1e}")
    v2.metric("max |VᵀV − I|", f"{np.abs(Vt @ Vt.T - np.eye(2)).max():.1e}")
    v3.metric("max |UΣVᵀ − A|", f"{np.abs(U @ np.diag(s) @ Vt - A).max():.1e}")
    return A, s


def render_eigen_compare(A, s):
    st.header("2) Singular values vs eigenvalues")
    lam = np.linalg.eigvals(A)
    lam = lam[np.argsort(-np.abs(lam))]
    ata = np.linalg.eigvalsh(A.T @ A)[::-1]
    df = pd.DataFrame({
        "": ["1", "2"],
        "singular value σᵢ": [fmt_num(x, 4) for x in s],
        "eigenvalue λᵢ": [fmt_complex(z, 4) for z in lam],
        "|λᵢ|": [fmt_num(abs(z), 4) for z in lam],
        "√(eigenvalue of AᵀA)": [fmt_num(np.sqrt(max(x, 0.0)), 4) for x in ata],
    })
    left, right = st.columns([3, 2], gap="large")
    with left:
        st.dataframe(df, hide_index=True, width="stretch")
        st.latex(rf"\sigma_1\sigma_2 = {fmt_num(s[0] * s[1], 4)} = |\det A| = {fmt_num(abs(np.linalg.det(A)), 4)}"
                 rf" = |\lambda_1\lambda_2| = {fmt_num(abs(np.prod(lam)), 4)}")
    symmetric = np.allclose(A, A.T)
    with right:
        if symmetric and np.all(lam.real >= -1e-12):
            st.success("Symmetric and positive semi-definite: σᵢ = λᵢ. The SVD *is* the eigendecomposition.")
        elif symmetric:
            st.info("Symmetric with a negative eigenvalue: σᵢ = |λᵢ|. The sign moves into U (U ≠ V).")
        else:
            st.warning("Not symmetric: σ and |λ| generally differ. Eigenvectors are directions that keep their "
                       "line; singular vectors are the perpendicular directions that stay perpendicular. "
                       "Try **Shear**: λ = 1, 1 but σ ≈ 1.618, 0.618.")
        st.caption("Always: σᵢ² are the eigenvalues of AᵀA, and σ_min ≤ |λᵢ| ≤ σ_max.")


def render_image_lab():
    st.header("3) Rank-k approximation of an image")
    left, right = st.columns([1, 3], gap="large")
    with left:
        kind = st.selectbox("Image", ["Shapes & letters", "Checkerboard + disk", "Smooth waves (exactly low rank)"],
                            key="p78_img")
        noise = st.slider("added noise σ", 0.0, 0.5, 0.0, 0.05, key="p78_noise")
        if st.button("🎲 Resample noise & data", key="p78_resample"):
            st.session_state["p78_seed"] = int(np.random.default_rng(st.session_state["p78_seed"]).integers(1, 10**6))
        k = st.slider("rank k", 1, IMG_N, 8, key="p78_k")
    rng = np.random.default_rng(st.session_state["p78_seed"])
    img = synthetic_image(kind) + noise * rng.standard_normal((IMG_N, IMG_N))
    U, s, Vt = np.linalg.svd(img)
    approx = (U[:, :k] * s[:k]) @ Vt[:k]
    err_f = float(np.linalg.norm(img - approx))
    tail_f = float(np.sqrt(np.sum(s[k:] ** 2)))
    err_2 = float(np.linalg.norm(img - approx, 2))
    next_sigma = float(s[k]) if k < len(s) else 0.0
    energy = np.cumsum(s**2) / np.sum(s**2)

    fig = make_subplots(rows=1, cols=2, subplot_titles=("original", f"rank-{k} reconstruction"),
                        horizontal_spacing=0.04)
    for i, data in enumerate((img, approx), start=1):
        fig.add_trace(go.Heatmap(z=data, colorscale="gray", zmin=0, zmax=1, showscale=False), row=1, col=i)
        fig.update_yaxes(autorange="reversed", scaleanchor=f"x{'' if i == 1 else i}", showticklabels=False,
                         row=1, col=i)
        fig.update_xaxes(showticklabels=False, row=1, col=i)
    fig.update_layout(height=420, margin=dict(l=10, r=10, t=40, b=10))
    with right:
        st.plotly_chart(fig, width="stretch", key="p78_fig_img")
    with left:
        st.metric("energy kept  Σᵢ≤k σᵢ² / Σ σᵢ²", f"{100 * energy[k - 1]:.2f}%")
        st.metric("numbers stored", f"{k * (2 * IMG_N + 1):,} vs {IMG_N * IMG_N:,}",
                  help="k columns of U, k rows of Vᵀ and k singular values, instead of every pixel.")
    st.markdown(
        r"**Eckart–Young:** $A_k = \sum_{i\le k}\sigma_i u_i v_i^\top$ is the *best* rank-$k$ matrix — no other "
        r"rank-$k$ matrix is closer to $A$ in Frobenius or spectral norm. The errors are exactly the dropped "
        r"singular values:"
    )
    st.latex(rf"\lVert A-A_k\rVert_F = {fmt_num(err_f, 4)} = \sqrt{{\textstyle\sum_{{i>k}}\sigma_i^2}} = "
             rf"{fmt_num(tail_f, 4)},\qquad \lVert A-A_k\rVert_2 = {fmt_num(err_2, 4)} = \sigma_{{k+1}} = "
             rf"{fmt_num(next_sigma, 4)}")
    if k == len(s):
        st.success(f"Full rank: reconstruction is exact up to rounding (max error {np.abs(img - approx).max():.1e}).")

    idx = np.arange(1, len(s) + 1)
    efig = make_subplots(rows=1, cols=2, subplot_titles=("singular values σᵢ (log scale)", "cumulative energy"))
    efig.add_trace(go.Bar(x=idx, y=np.maximum(s, 1e-16), marker_color=np.where(idx <= k, "#38bdf8", "#475569"),
                          showlegend=False), row=1, col=1)
    efig.add_trace(go.Scatter(x=idx, y=energy, mode="lines+markers", showlegend=False, marker=dict(size=4),
                              line=dict(color="#4ade80")), row=1, col=2)
    efig.add_vline(x=k, line_dash="dash", line_color="#fb923c", row=1, col=2)
    efig.update_yaxes(type="log", row=1, col=1)
    efig.update_yaxes(range=[0, 1.02], row=1, col=2)
    efig.update_layout(height=320, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(efig, width="stretch", key="p78_fig_energy")
    st.caption("Smooth waves need only a few σ's (exactly low rank). Sharp edges and noise spread energy over many "
               "σ's. With noise on, a small k often looks *cleaner* than the original: the tail is mostly noise.")


def render_pca_link():
    st.header("4) PCA is the SVD of centred data")
    rng = np.random.default_rng(st.session_state["p78_seed"] + 1)
    n = 200
    X = rng.standard_normal((n, 2)) @ np.diag([2.5, 0.7]) @ rotation_matrix(30).T + np.array([3.0, -1.0])
    Xc = X - X.mean(axis=0)
    _, s, Vt = np.linalg.svd(Xc, full_matrices=False)
    var_svd = s**2 / (n - 1)
    eig = np.linalg.eigvalsh(np.cov(X.T))[::-1]
    left, right = st.columns([2, 3], gap="large")
    with left:
        st.markdown(
            r"""
            Centre the data ($X_c = X - \bar x$) and take $X_c = U\Sigma V^\top$. Then
            $C = \frac{1}{n-1}X_c^\top X_c = V\,\frac{\Sigma^2}{n-1}\,V^\top$, so
            - the rows of $V^\top$ are the principal directions **PC1, PC2** (page 63),
            - the variance along PC$i$ is $\sigma_i^2/(n-1)$.
            """
        )
        st.latex(rf"\frac{{\sigma_i^2}}{{n-1}} = ({fmt_num(var_svd[0], 4)},\ {fmt_num(var_svd[1], 4)})")
        st.latex(rf"\text{{eig}}(C) = ({fmt_num(eig[0], 4)},\ {fmt_num(eig[1], 4)})")
        st.caption(f"Max difference: {np.abs(var_svd - eig).max():.1e}. Libraries such as scikit-learn compute "
                   "PCA through the SVD because it avoids forming XᵀX (which squares the condition number).")
    fig = go.Figure(go.Scatter(x=Xc[:, 0], y=Xc[:, 1], mode="markers", name="centred data",
                               marker=dict(size=5, color="#a78bfa", opacity=0.6)))
    for i, color in enumerate((V1_COLOR, V2_COLOR)):
        tip = Vt[i] * 2 * np.sqrt(var_svd[i])
        fig.add_trace(go.Scatter(x=[0, tip[0]], y=[0, tip[1]], mode="lines+markers", name=f"PC{i + 1} (2 std)",
                                 line=dict(color=color, width=5),
                                 marker=dict(symbol="arrow", size=[0, 14], angleref="previous", color=color)))
    lim = float(np.abs(Xc).max()) * 1.05
    fig.update_layout(height=400, margin=dict(l=10, r=10, t=20, b=10),
                      xaxis=dict(range=[-lim, lim], scaleanchor="y", scaleratio=1), yaxis=dict(range=[-lim, lim]),
                      legend=dict(orientation="h", y=1.02, yanchor="bottom", x=0))
    with right:
        st.plotly_chart(fig, width="stretch", key="p78_fig_pca")


def render_condition_lab(A_user, s_user):
    st.header("5) Condition number — how close to singular?")
    st.markdown(
        r"""
        $\kappa(A) = \sigma_{\max}/\sigma_{\min}$ measures how much $A^{-1}$ can amplify relative errors:
        $\dfrac{\lVert\delta x\rVert}{\lVert x\rVert} \le \kappa(A)\,\dfrac{\lVert\delta b\rVert}{\lVert b\rVert}$.
        A singular matrix has $\sigma_{\min}=0$, so $\kappa=\infty$ (page 18: no inverse exists).
        """
    )
    eps = st.select_slider("ε in A = [[1, 1], [1, 1 + ε]]", options=[1.0, 0.1, 0.01, 1e-3, 1e-4, 1e-6, 0.0],
                           value=0.01, format_func=lambda v: f"{v:g}", key="p78_eps")
    A = np.array([[1.0, 1.0], [1.0, 1.0 + eps]])
    s = np.linalg.svd(A, compute_uv=False)
    kappa = condition_number(s)
    b = np.array([2.0, 2.0 + eps])
    db = np.array([0.0, 1e-3])
    c1, c2, c3 = st.columns(3)
    c1.metric("σ_max, σ_min", f"{fmt_num(s[0], 4)}, {s[1]:.2e}")
    c2.metric("κ(A)", "∞" if np.isinf(kappa) else f"{kappa:,.1f}")
    c3.metric("κ of your matrix from lab 1", "∞" if np.isinf(condition_number(s_user)) else
              f"{condition_number(s_user):,.2f}")
    if np.isinf(kappa):
        st.error("ε = 0: the rows are identical, A is singular — Ax = b has no unique solution and the 'inverse' "
                 "does not exist.")
        return
    x = np.linalg.solve(A, b)
    x2 = np.linalg.solve(A, b + db)
    rel_b = np.linalg.norm(db) / np.linalg.norm(b)
    rel_x = np.linalg.norm(x2 - x) / np.linalg.norm(x)
    st.latex(rf"b = ({fmt_num(b[0], 4)}, {fmt_num(b[1], 6)}) \Rightarrow x = ({fmt_num(x[0], 3)}, {fmt_num(x[1], 3)});"
             rf"\quad b+\delta b \Rightarrow x' = ({fmt_num(x2[0], 3)}, {fmt_num(x2[1], 3)})")
    st.latex(rf"\frac{{\lVert\delta x\rVert}}{{\lVert x\rVert}} = {rel_x:.3g} \;\le\; \kappa\cdot"
             rf"\frac{{\lVert\delta b\rVert}}{{\lVert b\rVert}} = {kappa * rel_b:.3g}")
    st.caption(f"A nudge of 0.001 in b (relative {rel_b:.1e}) moves the answer by a relative {rel_x:.2g}. In ML, "
               "ill-conditioned XᵀX (nearly collinear features) and ill-conditioned Hessians make training and "
               "closed-form fits unstable; regularization raises σ_min.")


def render_ai():
    st.header("🤖 AI / ML connection")
    t1, t2, t3, t4 = st.tabs(["Compression", "LoRA", "Recommenders", "PCA"])
    with t1:
        st.markdown("A d_out × d_in weight matrix truncated to rank k stores k(d_out + d_in + 1) numbers instead of "
                    "d_out·d_in — the same trick as the image above. Low-rank factorization of layers is a classic "
                    "way to shrink and speed up networks when the singular values decay quickly.")
    with t2:
        st.markdown(r"LoRA learns $\Delta W = BA$ of rank $r$; Eckart–Young says the best possible rank-$r$ "
                    r"update is the truncated SVD, so if fine-tuning changes have fast-decaying singular values, "
                    r"little is lost. Some LoRA variants even initialise $B, A$ from the top singular vectors of $W$.")
    with t3:
        R = np.array([[5, 4, 1, 1, 2], [4, 5, 1, 2, 1], [5, 5, 2, 1, 1],
                      [1, 1, 5, 4, 5], [2, 1, 4, 5, 4], [1, 2, 5, 5, 4]], dtype=float)
        U, s, Vt = np.linalg.svd(R)
        R2 = (U[:, :2] * s[:2]) @ Vt[:2]
        st.markdown("Users × movies ratings ≈ (user tastes) × (movie traits). Two taste groups → nearly rank 2. "
                    f"Singular values: {', '.join(fmt_num(x, 2) for x in s)}.")
        cols = ["Action 1", "Action 2", "Romance 1", "Romance 2", "Romance 3"]
        c1, c2 = st.columns(2)
        c1.markdown("**Ratings R**")
        c1.dataframe(pd.DataFrame(R, columns=cols).astype(int), width="stretch")
        c2.markdown(f"**Rank-2 reconstruction** (max error {np.abs(R - R2).max():.2f})")
        c2.dataframe(pd.DataFrame(R2, columns=cols).round(2), width="stretch")
        st.caption("Real rating matrices are mostly *missing*, so recommenders fit the factors only on observed "
                   "entries (e.g. alternating least squares) rather than running a plain SVD — the low-rank idea "
                   "is the same.")
    with t4:
        st.markdown("PCA = SVD of the centred data matrix (section 4). Keeping the top-k right singular vectors "
                    "gives the best k-dimensional linear summary of the data.")


def render_takeaways():
    st.header("✅ Key takeaways")
    st.markdown(
        """
        - **A = UΣVᵀ** for every matrix: rotate/reflect, stretch by σᵢ ≥ 0, rotate/reflect. U, V are orthogonal.
        - Singular values = semi-axes of the image of the unit circle; σᵢ² = eigenvalues of AᵀA.
        - σ = |λ| only for symmetric matrices (σ = λ for symmetric PSD); in general they differ.
        - **Eckart–Young:** keeping the top k singular triplets gives the best rank-k approximation;
          error² = sum of the dropped σᵢ².
        - **κ = σ_max/σ_min** measures closeness to singular; PCA, LoRA, compression and recommenders are all SVD.
        """
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        safe_page_link("pages/77Projections — Shadows onto Subspaces.py", "Previous: Projections", icon="⬅️")
    with c2:
        safe_page_link("pages/63PCA Intuition — Finding the Best Angle.py", "Related: PCA Intuition", icon="📐")
    with c3:
        safe_page_link("pages/61Eigenvectors — Vectors That Don't Rotate.py", "Next: Eigenvectors", icon="➡️")


def main():
    init_state()
    render_intro()
    A, s = render_circle_lab()
    st.divider()
    render_eigen_compare(A, s)
    st.divider()
    render_image_lab()
    st.divider()
    render_pca_link()
    st.divider()
    render_condition_lab(A, s)
    st.divider()
    render_ai()
    st.divider()
    render_takeaways()


main()
