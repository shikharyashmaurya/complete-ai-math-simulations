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
from common.mathutils import fmt_num  # noqa: E402

st.set_page_config(page_title="77 · Projections — Shadows onto Subspaces", page_icon="🔦", layout="wide")

ZERO_TOL = 1e-12  # squared length below this = zero vector
GS_TOL = 1e-9  # Gram–Schmidt drops a column whose leftover length is below this
A_COLOR, B_COLOR, P_COLOR, E_COLOR, PLANE_COLOR = "#38bdf8", "#fb923c", "#4ade80", "#f87171", "#a78bfa"
PLANE_KEYS = ["p77_a1x", "p77_a1y", "p77_a1z", "p77_a2x", "p77_a2y", "p77_a2z", "p77_bx", "p77_by", "p77_bz"]
PLANE_PRESETS = {
    "Tilted plane": (1.0, 0.0, 0.5, 0.0, 1.0, 0.5, 1.0, 1.5, 2.5),
    "Floor (xy-plane)": (1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.5, 1.0, 2.0),
    "Dependent columns (a₂ = 2a₁)": (1.0, 0.5, 0.0, 2.0, 1.0, 0.0, 0.5, 1.5, 2.0),
    "Zero column a₁": (0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 0.5),
}
TOY_EMBEDDINGS = {
    "he": [0.90, 0.30, 0.20], "she": [-0.85, 0.35, 0.10],
    "doctor": [0.35, 0.80, 0.30], "nurse": [-0.40, 0.75, 0.35], "engineer": [0.45, 0.60, -0.50],
}


def bmat(M, prec=2):
    M = np.atleast_2d(np.asarray(M, dtype=float))
    rows = [" & ".join(fmt_num(v, prec) for v in row) for row in M]
    return r"\begin{bmatrix}" + r" \\ ".join(rows) + r"\end{bmatrix}"


def col(v, prec=2):
    return bmat(np.asarray(v, dtype=float).reshape(-1, 1), prec)


def project_onto_line(a, b):
    """(projection, coefficient) of b onto the line through a; the zero vector spans only {0}."""
    aa = float(a @ a)
    if aa < ZERO_TOL:
        return np.zeros_like(b), None
    t = float(a @ b) / aa
    return t * a, t


def projection_matrix(A):
    """P onto the column space of A: A(AᵀA)⁻¹Aᵀ when columns are independent, else A A⁺ (pseudo-inverse)."""
    rank = int(np.linalg.matrix_rank(A))
    if rank == A.shape[1]:
        return A @ np.linalg.inv(A.T @ A) @ A.T, rank, "inverse"
    return A @ np.linalg.pinv(A), rank, "pinv"


def gram_schmidt(A, tol=GS_TOL):
    """Orthonormal columns Q spanning col(A); dependent (or zero) columns are skipped."""
    qs, steps = [], []
    for j in range(A.shape[1]):
        w = A[:, j] - sum((q @ A[:, j]) * q for q in qs) if qs else A[:, j].copy()
        nrm = float(np.linalg.norm(w))
        steps.append((j, w, nrm))
        if nrm > tol:
            qs.append(w / nrm)
    Q = np.column_stack(qs) if qs else np.zeros((A.shape[0], 0))
    return Q, steps


def arrow2d(fig, start, end, color, name, width=4, dash=None):
    fig.add_trace(go.Scatter(x=[start[0], end[0]], y=[start[1], end[1]], mode="lines+markers", name=name,
                             line=dict(color=color, width=width, dash=dash),
                             marker=dict(symbol="arrow", size=[0, 14], angleref="previous", color=color)))


def seg3d(fig, start, end, color, name, width=7, dash=None, tip=True):
    fig.add_trace(go.Scatter3d(x=[start[0], end[0]], y=[start[1], end[1]], z=[start[2], end[2]],
                               mode="lines+markers" if tip else "lines", name=name,
                               line=dict(color=color, width=width, dash=dash),
                               marker=dict(size=[0, 5], color=color)))


def apply_plane_preset():
    preset = st.session_state["p77_plane_preset"]
    if preset in PLANE_PRESETS:
        for k, v in zip(PLANE_KEYS, PLANE_PRESETS[preset]):
            st.session_state[k] = v


def init_state():
    for k, v in zip(PLANE_KEYS, PLANE_PRESETS["Tilted plane"]):
        st.session_state.setdefault(k, v)
    st.session_state.setdefault("p77_seed", 77)


def render_intro():
    st.title("🔦 Projections — Shadows onto Subspaces")
    st.markdown(
        """
        Shine a flashlight straight down onto a floor: every object casts a **shadow** — the closest point on the
        floor. That shadow is the **orthogonal projection**, and the line from object to shadow (the **error**)
        hits the floor at a right angle.

        Projection is the geometry behind **least squares** (every linear regression), behind removing an
        unwanted direction from embeddings, and behind the "keep only the important directions" step of PCA.
        """
    )


def render_line_lab():
    st.header("1) Projecting b onto a line")
    left, right = st.columns([1, 2], gap="large")
    with left:
        c1, c2 = st.columns(2)
        a = np.array([c1.slider("a x", -4.0, 4.0, 3.0, 0.1, key="p77_ax"),
                      c2.slider("a y", -4.0, 4.0, 1.0, 0.1, key="p77_ay")])
        b = np.array([c1.slider("b x", -4.0, 4.0, 1.5, 0.1, key="p77_bx2"),
                      c2.slider("b y", -4.0, 4.0, 2.5, 0.1, key="p77_by2")])
    p, t = project_onto_line(a, b)
    e = b - p
    lim = max(3.0, float(np.abs(np.vstack([a, b, p])).max()) * 1.3)
    fig = go.Figure()
    if t is not None:
        u = a / np.linalg.norm(a)
        fig.add_trace(go.Scatter(x=[-2 * lim * u[0], 2 * lim * u[0]], y=[-2 * lim * u[1], 2 * lim * u[1]],
                                 mode="lines", name="line through a", line=dict(color=A_COLOR, width=1, dash="dot")))
        en = float(np.linalg.norm(e))
        if en > 1e-9 and float(np.linalg.norm(p)) > 1e-9:
            s = 0.05 * lim
            back, side = -np.sign(t) * u, e / en
            q1, q3 = p + s * back, p + s * side
            fig.add_trace(go.Scatter(x=[q1[0], q1[0] + s * side[0], q3[0]], y=[q1[1], q1[1] + s * side[1], q3[1]],
                                     mode="lines", showlegend=False, line=dict(color="#94a3b8", width=2)))
    arrow2d(fig, (0, 0), a, A_COLOR, "a", width=5)
    arrow2d(fig, (0, 0), b, B_COLOR, "b", width=5)
    arrow2d(fig, (0, 0), p, P_COLOR, "p = proj of b", width=6)
    arrow2d(fig, p, b, E_COLOR, "e = b − p", width=3, dash="dash")
    fig.update_layout(height=480, margin=dict(l=10, r=10, t=20, b=10),
                      xaxis=dict(range=[-lim, lim], scaleanchor="y", scaleratio=1), yaxis=dict(range=[-lim, lim]),
                      legend=dict(orientation="h", y=1.02, yanchor="bottom", x=0))
    with right:
        st.plotly_chart(fig, width="stretch", key="p77_fig_line")
    with left:
        if t is None:
            st.warning("a is the zero vector: it spans only {0}, so the projection is 0 (a·a = 0, the formula "
                       "would divide by zero).")
        else:
            st.metric("a · e (should be 0)", f"{float(a @ e):.1e}")
            st.metric("distance from b to the line = ‖e‖", fmt_num(float(np.linalg.norm(e)), 3))
    if t is not None:
        st.latex(
            rf"p = \frac{{a\cdot b}}{{a\cdot a}}\,a = \frac{{{fmt_num(a @ b, 2)}}}{{{fmt_num(a @ a, 2)}}}{col(a)}"
            rf" = {fmt_num(t, 3)}\,{col(a)} = {col(p, 3)},\qquad e = b - p = {col(e, 3)}"
        )
        P = np.outer(a, a) / (a @ a)
        st.latex(rf"P = \frac{{a a^\top}}{{a^\top a}} = {bmat(P, 3)},\quad \max|P^2 - P| = {np.abs(P @ P - P).max():.1e}")
        st.caption("Projecting twice changes nothing (P² = P) — the shadow of a shadow is itself.")


def render_plane_lab():
    st.header("2) Projecting onto a plane in 3-D:  P = A(AᵀA)⁻¹Aᵀ")
    left, right = st.columns([1, 2], gap="large")
    with left:
        st.selectbox("Preset", ["Custom", *PLANE_PRESETS], key="p77_plane_preset", on_change=apply_plane_preset)
        labels = ["a₁", "a₂", "b"]
        for i, name in enumerate(labels):
            cols = st.columns(3)
            lo, hi = (-3.0, 3.0) if name == "b" else (-2.0, 2.0)
            for j, ax in enumerate("xyz"):
                cols[j].slider(f"{name} {ax}", lo, hi, step=0.5, key=PLANE_KEYS[3 * i + j])
    vals = np.array([st.session_state[k] for k in PLANE_KEYS], dtype=float)
    A = np.column_stack([vals[0:3], vals[3:6]])
    b = vals[6:9]
    P, rank, how = projection_matrix(A)
    p = P @ b
    e = b - p

    fig = go.Figure()
    L = 3.0
    Q, _ = gram_schmidt(A)
    if rank == 2:
        g = np.linspace(-L, L, 2)
        S_, T_ = np.meshgrid(g, g)
        pts = S_[..., None] * Q[:, 0] + T_[..., None] * Q[:, 1]
        fig.add_trace(go.Surface(x=pts[..., 0], y=pts[..., 1], z=pts[..., 2], opacity=0.35, showscale=False,
                                 colorscale=[[0, PLANE_COLOR], [1, PLANE_COLOR]], name="column space"))
    elif rank == 1:
        d = Q[:, 0] * L
        seg3d(fig, -d, d, PLANE_COLOR, "column space (a line)", width=5, tip=False)
    seg3d(fig, (0, 0, 0), A[:, 0], A_COLOR, "a₁")
    seg3d(fig, (0, 0, 0), A[:, 1], "#0ea5e9", "a₂")
    seg3d(fig, (0, 0, 0), b, B_COLOR, "b")
    seg3d(fig, (0, 0, 0), p, P_COLOR, "p = Pb", width=9)
    seg3d(fig, p, b, E_COLOR, "e = b − p", width=5, dash="dash")
    fig.update_layout(height=520, margin=dict(l=0, r=0, t=10, b=0),
                      scene=dict(aspectmode="cube", xaxis=dict(range=[-L, L]), yaxis=dict(range=[-L, L]),
                                 zaxis=dict(range=[-L, L])))
    with right:
        st.plotly_chart(fig, width="stretch", key="p77_fig_plane")

    with left:
        if how == "inverse":
            st.success("Independent columns: AᵀA is invertible.")
        elif rank == 1:
            st.warning("Dependent columns: AᵀA is singular, so (AᵀA)⁻¹ does not exist. Using the pseudo-inverse "
                       "P = AA⁺ — the projection onto the line the columns actually span.")
        else:
            st.error("Both columns are zero: the column space is {0}, so P = 0.")
    eig = np.sort(np.linalg.eigvalsh((P + P.T) / 2))[::-1]
    st.latex(rf"P = {bmat(P, 3)},\quad p = Pb = {col(p, 3)},\quad e = b - p = {col(e, 3)}")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("max |P² − P|", f"{np.abs(P @ P - P).max():.1e}", help="Idempotent: projecting twice = once.")
    m2.metric("max |Pᵀ − P|", f"{np.abs(P.T - P).max():.1e}", help="Symmetric: orthogonal (not oblique) projection.")
    m3.metric("max |Aᵀe|", f"{np.abs(A.T @ e).max():.1e}", help="The error is perpendicular to every column.")
    m4.metric("eigenvalues of P", ", ".join(fmt_num(x, 2) for x in eig), help="Only 0s and 1s; trace(P) = rank.")
    return A, b, P


def render_gram_schmidt(A, b, P):
    st.header("3) Gram–Schmidt — an orthonormal basis makes projection easy")
    st.markdown(
        r"""
        Subtract from each column its shadow on the directions already found, then normalise:
        $w_2 = a_2 - (q_1\!\cdot a_2)\,q_1,\; q_2 = w_2/\lVert w_2\rVert$. With orthonormal columns $Q$, $Q^\top Q = I$, so
        $P = Q(Q^\top Q)^{-1}Q^\top = QQ^\top$ and the projection is just a sum of 1-D shadows:
        $p = (q_1\!\cdot b)\,q_1 + (q_2\!\cdot b)\,q_2$ — no matrix inverse needed.
        """
    )
    Q, steps = gram_schmidt(A)
    for j, w, nrm in steps:
        if nrm > GS_TOL:
            st.latex(rf"w_{j + 1} = {col(w, 3)},\ \lVert w_{j + 1}\rVert = {fmt_num(nrm, 3)}"
                     rf"\ \Rightarrow\ \text{{new }} q = {col(w / nrm, 3)}")
        else:
            st.latex(rf"w_{j + 1} = {col(w, 3)} \approx 0 \Rightarrow a_{j + 1}" + r"\text{ adds no new direction: skipped}")
    if Q.shape[1] == 0:
        st.info("No non-zero columns, so there is nothing to project onto: p = 0.")
        return
    coeffs = Q.T @ b
    p_q = Q @ coeffs
    terms = " + ".join(rf"({fmt_num(c, 3)})\,q_{i + 1}" for i, c in enumerate(coeffs))
    st.latex(rf"p = {terms} = {col(p_q, 3)}")
    c1, c2 = st.columns(2)
    c1.metric("max |QᵀQ − I|", f"{np.abs(Q.T @ Q - np.eye(Q.shape[1])).max():.1e}")
    c2.metric("max |QQᵀ − P| (vs lab 2)", f"{np.abs(Q @ Q.T - P).max():.1e}")
    st.caption("Same projection either way. Libraries use the numerically safer QR decomposition (A = QR), which "
               "is Gram–Schmidt done carefully.")


def render_least_squares():
    st.header("4) Least squares is a projection")
    st.markdown(
        r"""
        Fit $\hat y = \theta_0 + \theta_1 x$ to $n$ points. Stack $X = [\mathbf 1\;\; x]$ ($n\times 2$). Every
        possible prediction vector $X\theta$ lies in the **column space** of $X$ — a plane inside $\mathbb R^n$.
        The best fit $\hat y$ is the projection of $y$ onto that plane, so the residual $r = y-\hat y$ is
        perpendicular to both columns: $X^\top r = 0$, i.e. the **normal equations** $X^\top X\theta = X^\top y$.
        (Page 43 shows the residuals; here is *why* they sum to zero.)
        """
    )
    left, right = st.columns([1, 2], gap="large")
    with left:
        n = st.slider("number of points n", 3, 40, 12, key="p77_n")
        noise = st.slider("noise σ", 0.0, 3.0, 1.0, 0.1, key="p77_noise")
        degenerate = st.checkbox("Degenerate: every x identical (dependent columns)", key="p77_degenerate")
        if st.button("🎲 Resample", key="p77_resample"):
            st.session_state["p77_seed"] = int(np.random.default_rng(st.session_state["p77_seed"]).integers(1, 10**6))
    rng = np.random.default_rng(st.session_state["p77_seed"])
    x = np.full(n, 2.0) if degenerate else np.sort(rng.uniform(-4, 4, n))
    y = 1.5 + 0.8 * x + noise * rng.standard_normal(n)
    X = np.column_stack([np.ones(n), x])
    theta = np.linalg.pinv(X) @ y
    y_hat = X @ theta
    r = y - y_hat
    xs = np.array([-4.5, 4.5])
    fig = go.Figure()
    for xi, yi, yh in zip(x, y, y_hat):
        fig.add_trace(go.Scatter(x=[xi, xi], y=[yi, yh], mode="lines", showlegend=False, hoverinfo="skip",
                                 line=dict(color=E_COLOR, width=2)))
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", name="data y", marker=dict(color=B_COLOR, size=9)))
    fig.add_trace(go.Scatter(x=xs, y=theta[0] + theta[1] * xs, mode="lines", name="fit ŷ = θ₀ + θ₁x",
                             line=dict(color=P_COLOR, width=3)))
    fig.update_layout(height=420, margin=dict(l=10, r=10, t=20, b=10), xaxis_title="x", yaxis_title="y",
                      legend=dict(orientation="h", y=1.02, yanchor="bottom", x=0))
    with right:
        st.plotly_chart(fig, width="stretch", key="p77_fig_ls")
    with left:
        st.latex(rf"\theta = ({fmt_num(theta[0], 3)},\ {fmt_num(theta[1], 3)})")
        st.metric("Σ rᵢ  (= 1ᵀr)", f"{r.sum():.1e}")
        st.metric("Σ xᵢ rᵢ  (= xᵀr)", f"{(x @ r):.1e}")
        st.metric("SSE = ‖r‖²", fmt_num(float(r @ r), 3))
    if degenerate:
        st.warning("All x are equal, so the column x is a multiple of the column of ones: XᵀX is singular and "
                   "**every** line through (2, ȳ) fits equally well. The pseudo-inverse picks the θ with the "
                   "smallest norm; ŷ (the projection) is still unique — every prediction equals ȳ.")
    if n == 3:
        Q, _ = gram_schmidt(X)
        fig3 = go.Figure()
        if Q.shape[1] == 2:
            g = np.linspace(-1, 1, 2) * max(4.0, float(np.abs(y).max()) * 1.2)
            S_, T_ = np.meshgrid(g, g)
            pts = S_[..., None] * Q[:, 0] + T_[..., None] * Q[:, 1]
            fig3.add_trace(go.Surface(x=pts[..., 0], y=pts[..., 1], z=pts[..., 2], opacity=0.35, showscale=False,
                                      colorscale=[[0, PLANE_COLOR], [1, PLANE_COLOR]], name="column space of X"))
        seg3d(fig3, (0, 0, 0), y, B_COLOR, "y (data)")
        seg3d(fig3, (0, 0, 0), y_hat, P_COLOR, "ŷ = Py")
        seg3d(fig3, y_hat, y, E_COLOR, "r = y − ŷ", dash="dash")
        fig3.update_layout(height=460, margin=dict(l=0, r=0, t=30, b=0), scene=dict(aspectmode="cube"),
                           title="n = 3: y lives in ℝ³ and ŷ is its shadow on the plane spanned by 1 and x")
        st.plotly_chart(fig3, width="stretch", key="p77_fig_ls3d")
    else:
        st.caption("Set n = 3 to see the same picture inside ℝ³: y, its shadow ŷ on the column-space plane, and r.")


def render_ai():
    st.header("🤖 AI / ML connection")
    t1, t2, t3 = st.tabs(["Linear regression", "Attention (careful!)", "Debiasing embeddings"])
    with t1:
        st.markdown(
            "Every ordinary-least-squares fit — from a trend line to the final linear layer fitted in closed form — "
            "computes ŷ = Py with P the projection onto the column space of the feature matrix. Redundant "
            "features (dependent columns) do not change ŷ, only make θ non-unique; the pseudo-inverse (or "
            "ridge regression) picks one."
        )
    with t2:
        st.markdown(
            r"""
            In attention, the score $q\cdot k_j/\sqrt{d}$ is a dot product — up to the factor $\lVert k_j\rVert$, the
            length of the shadow of the query on key $k_j$. But the output
            $\sum_j \text{softmax}(\text{scores})_j\, v_j$ is a **weighted average of value vectors** (weights
            are positive and sum to 1), *not* an orthogonal projection: it is not idempotent and the "error" is
            not perpendicular to anything. Projection intuition explains the *scores*, not the mixing.
            """
        )
    with t3:
        render_debias()


def render_debias():
    st.markdown(
        r"""
        Toy 3-D "embeddings". The direction $g = \text{he} - \text{she}$ encodes gender. "Hard debiasing"
        removes it from neutral words: $x' = x - \frac{x\cdot g}{g\cdot g}\,g$ (projection onto the plane
        $\perp g$). Afterwards $x'\cdot\text{he} - x'\cdot\text{she} = x'\cdot g = 0$.
        """
    )
    emb = {k: np.array(v) for k, v in TOY_EMBEDDINGS.items()}
    g = emb["he"] - emb["she"]
    rows = []
    for word in ("doctor", "nurse", "engineer"):
        x = emb[word]
        xd = x - (x @ g) / (g @ g) * g
        rows.append({"word": word, "x·g = x·he − x·she (before)": x @ g, "x'·g (after)": xd @ g,
                     "removed length ‖x − x'‖": np.linalg.norm(x - xd), "x' (debiased)": np.round(xd, 3).tolist()})
    st.dataframe(pd.DataFrame(rows).round(6), hide_index=True, width="stretch")
    st.caption("Caveat (Gonen & Goldberg, 2019): in real embeddings bias is spread over many directions; removing "
               "one direction hides it from this test but neighbours can still cluster by gender.")


def render_takeaways():
    st.header("✅ Key takeaways")
    st.markdown(
        """
        - Onto a line: **p = (a·b / a·a) a**; the error e = b − p is perpendicular to a.
        - Onto a column space: **P = A(AᵀA)⁻¹Aᵀ** (independent columns) or **P = AA⁺** (any columns).
        - Projection matrices satisfy **P² = P** and **Pᵀ = P**; eigenvalues are 0 or 1.
        - **Least squares = projection** of y onto the column space; residuals are orthogonal to every feature.
        - With an **orthonormal** basis (Gram–Schmidt / QR), P = QQᵀ and projection is a sum of 1-D shadows.
        """
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        safe_page_link("pages/76Span, Basis & Rank.py", "Previous: Span, Basis & Rank", icon="⬅️")
    with c2:
        safe_page_link("pages/43Residuals & Least Squares.py", "Related: Residuals & Least Squares", icon="📉")
    with c3:
        safe_page_link("pages/78SVD — Rotate, Stretch, Rotate.py", "Next: SVD", icon="➡️")


def main():
    init_state()
    render_intro()
    render_line_lab()
    st.divider()
    A, b, P = render_plane_lab()
    st.divider()
    render_gram_schmidt(A, b, P)
    st.divider()
    render_least_squares()
    st.divider()
    render_ai()
    st.divider()
    render_takeaways()


main()
