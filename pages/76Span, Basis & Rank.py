import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.nav import safe_page_link  # noqa: E402
from common.linalg2d import det2  # noqa: E402
from common.mathutils import fmt_num  # noqa: E402

st.set_page_config(page_title="76 · Span, Basis & Rank", page_icon="🧭", layout="wide")

C1_COLOR, C2_COLOR, W_COLOR, CLOUD_COLOR = "#38bdf8", "#fb923c", "#4ade80", "#a78bfa"
CLOUD_POINTS, CLOUD_FRAMES = 400, 10

LAB1_DEFAULTS = {"p76_v1x": 2.0, "p76_v1y": 1.0, "p76_v2x": -1.0, "p76_v2y": 1.5, "p76_c1": 1.0, "p76_c2": 1.0}
LAB1_PRESETS = {
    "Skewed basis": (2.0, 1.0, -1.0, 1.5),
    "Standard basis (î, ĵ)": (1.0, 0.0, 0.0, 1.0),
    "Parallel (dependent)": (2.0, 1.0, -1.0, -0.5),
    "Nearly parallel": (2.0, 1.0, 2.0, 1.1),
    "One zero vector": (1.5, 0.5, 0.0, 0.0),
}
VEC3_KEYS = [f"p76_u{i}{ax}" for i in (1, 2, 3) for ax in "xyz"]
VEC3_PRESETS = {
    "Three independent": (1.0, 0.0, 0.5, 0.0, 1.0, 0.5, 0.5, 0.5, 1.5),
    "Third lies in the plane of the first two": (1.0, 0.0, 0.5, 0.0, 1.0, 0.5, 1.0, 1.0, 1.0),
    "All on one line": (1.0, 0.5, 0.5, -2.0, -1.0, -1.0, 2.0, 1.0, 1.0),
}
NULL_KEYS = [f"p76_a{r}{c}" for r in range(3) for c in range(3)]
NULL_PRESETS = {
    "Rank 2 (col3 = col1 + col2)": (1, 2, 3, 0, 1, 1, 1, 0, 1),
    "Full rank": (2, 0, 1, 1, 3, 0, 0, 1, 1),
    "Rank 1 (all rows parallel)": (1, 2, -1, 2, 4, -2, -3, -6, 3),
    "Zero matrix": (0, 0, 0, 0, 0, 0, 0, 0, 0),
}


def bmat(M, prec=2):
    M = np.atleast_2d(np.asarray(M, dtype=float))
    rows = [" & ".join(fmt_num(v, prec) for v in row) for row in M]
    return r"\begin{bmatrix}" + r" \\ ".join(rows) + r"\end{bmatrix}"


def default_tol(M):
    """NumPy's matrix_rank default: sigma_max * max(m, n) * machine epsilon."""
    s = np.linalg.svd(M, compute_uv=False)
    return float(s.max() * max(M.shape) * np.finfo(float).eps) if s.size else 0.0


def null_space(M, tol=None):
    """Orthonormal basis (as columns) of {x : Mx = 0}, read off the SVD M = U S Vᵀ."""
    _, s, vt = np.linalg.svd(M, full_matrices=True)
    tol = default_tol(M) if tol is None else tol
    rank = int(np.sum(s > tol))
    return vt[rank:].T, rank, s


def span_word(rank, dim):
    if rank == 0:
        return "just the origin {0}"
    if rank == dim:
        return "the whole plane ℝ²" if dim == 2 else "all of ℝ³"
    return "a line through the origin" if rank == 1 else "a plane through the origin"


def arrow(fig, start, end, color, name, width=4):
    fig.add_trace(
        go.Scatter(
            x=[start[0], end[0]], y=[start[1], end[1]], mode="lines+markers", name=name,
            line=dict(color=color, width=width),
            marker=dict(symbol="arrow", size=[0, 15], angleref="previous", color=color),
        )
    )


def square_layout(fig, lim, height=520, title=None):
    fig.update_layout(
        title=title, height=height, margin=dict(l=10, r=10, t=50 if title else 20, b=10),
        xaxis=dict(range=[-lim, lim], zeroline=True, scaleanchor="y", scaleratio=1),
        yaxis=dict(range=[-lim, lim], zeroline=True),
        legend=dict(orientation="h", yanchor="bottom", y=1.0, x=0),
    )


def skew_grid(fig, v1, v2, n=3):
    t = np.array([-n, n], dtype=float)
    for k in range(-n, n + 1):
        for a, b, color in ((v1, v2, C1_COLOR), (v2, v1, C2_COLOR)):
            pts = np.outer(np.full(2, k), a) + np.outer(t, b)
            fig.add_trace(go.Scatter(x=pts[:, 0], y=pts[:, 1], mode="lines", showlegend=False, hoverinfo="skip",
                                     line=dict(color=color, width=1), opacity=0.25))


def apply_preset(keys, store_key):
    values = st.session_state[store_key]
    table = {"p76_preset2d": LAB1_PRESETS, "p76_preset3d": VEC3_PRESETS, "p76_preset_null": NULL_PRESETS}[store_key]
    if values in table:
        for k, v in zip(keys, table[values]):
            st.session_state[k] = float(v)


def init_state():
    for k, v in LAB1_DEFAULTS.items():
        st.session_state.setdefault(k, v)
    for k, v in zip(VEC3_KEYS, VEC3_PRESETS["Three independent"]):
        st.session_state.setdefault(k, v)
    for k, v in zip(NULL_KEYS, NULL_PRESETS["Rank 2 (col3 = col1 + col2)"]):
        st.session_state.setdefault(k, float(v))
    st.session_state.setdefault("p76_seed", 76)
    # Keep 3rd-row entries alive while the 2×3 shape hides them (Streamlit drops unrendered widget state).
    for k in NULL_KEYS:
        st.session_state[k] = st.session_state[k]


def render_intro():
    st.title("🧭 Span, Basis & Rank")
    st.markdown(
        """
        Give a robot two moves: *"walk along arrow **v₁**"* and *"walk along arrow **v₂**"*, each any number of times
        (negative = backwards, fractions allowed). **Which places can it reach?**

        - The set of all reachable places is the **span** of the arrows.
        - If no arrow is redundant, the arrows form a **basis** and every reachable place has *exactly one* recipe.
        - The **rank** counts how many *genuinely different directions* you have — the dimension of the span.

        Why AI cares: a weight matrix can only produce outputs inside the span of its columns, embedding tables
        are often close to low-rank, and redundant features (multicollinearity) make the "right" weights ambiguous.
        """
    )


def render_combination_lab():
    st.header("1) Linear combinations — what can c₁v₁ + c₂v₂ reach?")
    left, right = st.columns([1, 2], gap="large")
    with left:
        st.selectbox("Preset", ["Custom", *LAB1_PRESETS], key="p76_preset2d",
                     on_change=apply_preset, args=(list(LAB1_DEFAULTS)[:4], "p76_preset2d"))
        a, b = st.columns(2)
        v1 = np.array([a.slider("v₁ x", -3.0, 3.0, step=0.1, key="p76_v1x"),
                       b.slider("v₁ y", -3.0, 3.0, step=0.1, key="p76_v1y")])
        v2 = np.array([a.slider("v₂ x", -3.0, 3.0, step=0.1, key="p76_v2x"),
                       b.slider("v₂ y", -3.0, 3.0, step=0.1, key="p76_v2y")])
        c1 = a.slider("c₁", -3.0, 3.0, step=0.1, key="p76_c1")
        c2 = b.slider("c₂", -3.0, 3.0, step=0.1, key="p76_c2")
        show_grid = st.checkbox("Show the grid of integer combinations", value=True, key="p76_grid")
        if st.button("🎲 Resample random combinations", key="p76_resample"):
            st.session_state["p76_seed"] = int(np.random.default_rng(st.session_state["p76_seed"]).integers(1, 10**6))
    V = np.column_stack([v1, v2])
    w = c1 * v1 + c2 * v2

    rng = np.random.default_rng(st.session_state["p76_seed"])
    coeffs = rng.uniform(-3, 3, size=(CLOUD_POINTS, 2))
    cloud = coeffs @ V.T
    lim = max(3.0, float(np.abs(np.vstack([cloud, w, v1, v2])).max()) * 1.08)

    fig = go.Figure()
    if show_grid:
        skew_grid(fig, v1, v2)
    fig.add_trace(go.Scatter(x=cloud[:, 0], y=cloud[:, 1], mode="markers", name="random c₁v₁ + c₂v₂ (|cᵢ| ≤ 3)",
                             marker=dict(color=CLOUD_COLOR, size=5, opacity=0.55)))
    cloud_idx = len(fig.data) - 1
    arrow(fig, (0, 0), c1 * v1, C1_COLOR, "c₁v₁", width=3)
    arrow(fig, c1 * v1, w, C2_COLOR, "c₂v₂ (tip-to-tail)", width=3)
    arrow(fig, (0, 0), v1, C1_COLOR, "v₁", width=6)
    arrow(fig, (0, 0), v2, C2_COLOR, "v₂", width=6)
    fig.add_trace(go.Scatter(x=[w[0]], y=[w[1]], mode="markers", name="w = c₁v₁ + c₂v₂",
                             marker=dict(color=W_COLOR, size=14, symbol="star")))
    step = CLOUD_POINTS // CLOUD_FRAMES
    fig.frames = [go.Frame(data=[go.Scatter(x=cloud[: step * k, 0], y=cloud[: step * k, 1])], traces=[cloud_idx],
                           name=str(k)) for k in range(1, CLOUD_FRAMES + 1)]
    fig.update_layout(updatemenus=[dict(type="buttons", x=0, y=-0.08, xanchor="left", buttons=[dict(
        label="▶ Trace the reachable set", method="animate",
        args=[None, dict(frame=dict(duration=250, redraw=True), fromcurrent=False, mode="immediate")])])])
    square_layout(fig, lim, height=560)
    with right:
        st.plotly_chart(fig, width="stretch", key="p76_fig_comb")

    d = det2(V)
    rank = int(np.linalg.matrix_rank(V))
    m1, m2, m3 = st.columns(3)
    m1.metric("det[v₁ v₂]", fmt_num(d, 4))
    m2.metric("rank (NumPy default tol)", rank)
    m3.metric("span", span_word(rank, 2))
    st.latex(rf"w = {fmt_num(c1)}\,{bmat(v1.reshape(-1, 1))} + {fmt_num(c2)}\,{bmat(v2.reshape(-1, 1))}"
             rf" = {bmat(w.reshape(-1, 1))}")
    if rank == 2:
        st.success("Independent: the purple cloud fills the plane — enlarge |cᵢ| and you can hit **any** point.")
    elif rank == 1:
        st.warning("Dependent: one arrow is a multiple of the other (or zero). Every combination stays on one line.")
    else:
        st.error("Both arrows are zero: the only reachable point is the origin.")
    return V


def render_tolerance_lab(V):
    st.header("2) Independence test — determinant vs numerical rank")
    st.markdown(
        r"""
        In exact math, two 2-D vectors are dependent **iff** $\det[v_1\ v_2] = 0$. Computers use floating point, so
        "zero" becomes "smaller than a tolerance". `np.linalg.matrix_rank` counts singular values
        $\sigma_i > \text{tol}$; the default is $\text{tol} = \sigma_{\max}\cdot\max(m,n)\cdot\varepsilon_{\text{machine}}$
        with $\varepsilon \approx 2.2\times10^{-16}$ — just above rounding noise.
        """
    )
    v_small = np.array([0.1, 0.7])
    exact = np.column_stack([v_small, 3 * v_small])
    st.markdown(
        f"Example: $v_1=(0.1, 0.7)$ and $v_2 = 3v_1$ — dependent on paper. Computed in floats, the determinant is "
        f"`{det2(exact):.3e}` (rounding dust, not 0), yet `matrix_rank` correctly reports "
        f"**{np.linalg.matrix_rank(exact)}**. Testing `det == 0` would wrongly call them independent."
    )
    tol = st.select_slider("Your tolerance for 'zero' (applied to the vectors from lab 1)",
                           options=[1e-12, 1e-8, 1e-4, 1e-2, 0.1, 0.5, 1.0], value=1e-8,
                           format_func=lambda t: f"{t:g}", key="p76_tol")
    s = np.linalg.svd(V, compute_uv=False)
    c1, c2, c3 = st.columns(3)
    c1.metric("singular values σ₁, σ₂", f"{fmt_num(s[0], 4)}, {fmt_num(s[1], 4)}")
    c2.metric("rank with default tol", int(np.linalg.matrix_rank(V)), help=f"default tol = {default_tol(V):.2e}")
    c3.metric(f"rank with tol = {tol:g}", int(np.linalg.matrix_rank(V, tol=tol)))
    st.caption(
        "Try the **Nearly parallel** preset: σ₂ is small but non-zero. With a tiny tolerance the vectors count as "
        "independent; with tol ≥ σ₂ they count as dependent. A huge tolerance hides real structure, a tiny one "
        "treats noise as information — real data needs a tolerance matched to its noise level."
    )


def render_basis_lab(V):
    st.header("3) Basis & coordinates — the same point in a new language")
    v1, v2 = V[:, 0], V[:, 1]
    left, right = st.columns([1, 2], gap="large")
    with left:
        st.markdown("Use **v₁, v₂ from lab 1 as a basis**. Pick a target point **w** in standard coordinates:")
        wx = st.slider("w x", -5.0, 5.0, 3.0, 0.5, key="p76_wx")
        wy = st.slider("w y", -5.0, 5.0, 2.0, 0.5, key="p76_wy")
    w = np.array([wx, wy])
    rank = int(np.linalg.matrix_rank(V))
    fig = go.Figure()
    with left:
        if rank == 2:
            c = np.linalg.solve(V, w)
            st.latex(rf"\underbrace{{{bmat(V)}}}_{{B=[v_1\ v_2]}} c = {bmat(w.reshape(-1, 1))}"
                     rf"\;\Rightarrow\; c = B^{{-1}}w = {bmat(c.reshape(-1, 1), 3)}")
            st.success(f"Unique coordinates: w = {fmt_num(c[0], 3)}·v₁ + {fmt_num(c[1], 3)}·v₂. "
                       "In the new basis, w is written as (c₁, c₂).")
            st.caption(f"Check: Bc − w has max error {np.abs(V @ c - w).max():.1e}.")
        else:
            c = np.linalg.pinv(V) @ w
            closest = V @ c
            gap = float(np.linalg.norm(w - closest))
            if rank == 0:
                st.error("Both basis vectors are zero — they span only the origin, so they are not a basis.")
            elif gap < 1e-9:
                st.warning("v₁, v₂ are dependent but **w lies on their line**: infinitely many recipes work. "
                           f"The shortest one (pseudo-inverse) is c = ({fmt_num(c[0], 3)}, {fmt_num(c[1], 3)}).")
            else:
                st.error(f"v₁, v₂ are dependent and w is **off their line** — no recipe exists. The closest "
                         f"reachable point is ({fmt_num(closest[0])}, {fmt_num(closest[1])}), "
                         f"distance {fmt_num(gap, 3)} (see page 77 on projections).")
            w = closest
    lim = max(3.0, float(np.abs(np.vstack([V.T, w, [wx, wy], c[0] * v1])).max()) * 1.25)
    if rank == 2:
        skew_grid(fig, v1, v2, n=int(min(8, np.ceil(np.abs(c).max()) + 1)))
    arrow(fig, (0, 0), c[0] * v1, C1_COLOR, "c₁v₁", width=4)
    arrow(fig, c[0] * v1, c[0] * v1 + c[1] * v2, C2_COLOR, "c₂v₂", width=4)
    fig.add_trace(go.Scatter(x=[wx], y=[wy], mode="markers", name="target w",
                             marker=dict(color=W_COLOR, size=15, symbol="star")))
    square_layout(fig, lim, height=460, title="The skewed grid is the coordinate system of the new basis")
    with right:
        st.plotly_chart(fig, width="stretch", key="p76_fig_basis")


def render_span3d():
    st.header("4) Span in 3-D — line, plane or all of space")
    left, right = st.columns([1, 2], gap="large")
    with left:
        st.selectbox("Preset", ["Custom", *VEC3_PRESETS], key="p76_preset3d",
                     on_change=apply_preset, args=(VEC3_KEYS, "p76_preset3d"))
        k = st.radio("How many vectors?", [1, 2, 3], index=2, horizontal=True, key="p76_k3")
        vecs = []
        for i in range(3):
            cols = st.columns(3)
            vecs.append([cols[j].slider(f"u{i + 1} {ax}", -2.0, 2.0, step=0.5, key=VEC3_KEYS[3 * i + j],
                                        disabled=i >= k) for j, ax in enumerate("xyz")])
    U = np.array(vecs[:k], dtype=float)  # one vector per row
    _, s, vt = np.linalg.svd(U, full_matrices=True)
    rank = int(np.linalg.matrix_rank(U))
    fig = go.Figure()
    L = 3.0
    if rank == 1:
        d = vt[0] * L
        fig.add_trace(go.Scatter3d(x=[-d[0], d[0]], y=[-d[1], d[1]], z=[-d[2], d[2]], mode="lines",
                                   name="span (line)", line=dict(color=CLOUD_COLOR, width=8)))
    elif rank == 2:
        g = np.linspace(-L, L, 2)
        S_, T_ = np.meshgrid(g, g)
        P = S_[..., None] * vt[0] + T_[..., None] * vt[1]
        fig.add_trace(go.Surface(x=P[..., 0], y=P[..., 1], z=P[..., 2], opacity=0.4, showscale=False,
                                 colorscale=[[0, CLOUD_COLOR], [1, CLOUD_COLOR]], name="span (plane)"))
    elif rank == 3:
        corners = np.array([[x, y, z] for x in (-L, L) for y in (-L, L) for z in (-L, L)])
        fig.add_trace(go.Mesh3d(x=corners[:, 0], y=corners[:, 1], z=corners[:, 2], alphahull=0, opacity=0.08,
                                color=CLOUD_COLOR, name="span (all of ℝ³)"))
    for i, (u, color) in enumerate(zip(U, (C1_COLOR, C2_COLOR, W_COLOR))):
        fig.add_trace(go.Scatter3d(x=[0, u[0]], y=[0, u[1]], z=[0, u[2]], mode="lines+markers", name=f"u{i + 1}",
                                   line=dict(color=color, width=9), marker=dict(size=[0, 6], color=color)))
    fig.update_layout(height=520, margin=dict(l=0, r=0, t=10, b=0),
                      scene=dict(aspectmode="cube", xaxis=dict(range=[-L, L]), yaxis=dict(range=[-L, L]),
                                 zaxis=dict(range=[-L, L])))
    with right:
        st.plotly_chart(fig, width="stretch", key="p76_fig_span3d")
    with left:
        st.metric("rank = dim(span)", rank, help="Singular values: " + ", ".join(fmt_num(x, 3) for x in s))
        st.info(f"{k} vector(s) → span is **{span_word(rank, 3)}**." +
                (" Some vectors are redundant (dependent)." if rank < k else " No redundancy: they form a basis "
                 "of their span."))


def render_null_space_lab():
    st.header("5) Rank & null space of a matrix — the rank–nullity theorem")
    st.markdown(
        r"""
        For $A$ with $n$ columns: $\text{rank}(A) + \dim N(A) = n$. The **null space** $N(A)=\{x : Ax = 0\}$ is
        every input the matrix crushes to zero. From the SVD $A = U\Sigma V^\top$, the rows of $V^\top$ whose
        singular value is (numerically) zero form an orthonormal basis of $N(A)$.
        """
    )
    left, right = st.columns([1, 2], gap="large")
    with left:
        shape = st.radio("Shape", ["2×3", "3×3"], index=1, horizontal=True, key="p76_shape")
        st.selectbox("Preset (3×3; 2×3 uses the first two rows)", ["Custom", *NULL_PRESETS], key="p76_preset_null",
                     on_change=apply_preset, args=(NULL_KEYS, "p76_preset_null"))
        m = 2 if shape == "2×3" else 3
        for r in range(m):
            cols = st.columns(3)
            for c in range(3):
                cols[c].number_input(f"a{r + 1}{c + 1}", -9.0, 9.0, step=1.0, key=NULL_KEYS[3 * r + c],
                                     format="%.0f")
    A = np.array([[st.session_state[NULL_KEYS[3 * r + c]] for c in range(3)] for r in range(m)], dtype=float)
    N, rank, s = null_space(A)
    nullity = N.shape[1]
    with left:
        c1, c2, c3 = st.columns(3)
        c1.metric("rank", rank)
        c2.metric("nullity", nullity)
        c3.metric("rank + nullity", rank + nullity, help="Always equals the number of columns, n = 3.")
    st.latex(rf"A = {bmat(A, 0)},\quad \sigma = ({', '.join(fmt_num(x, 3) for x in s)}),\quad"
             rf"{rank} + {nullity} = 3 \;\checkmark")
    if nullity:
        st.latex(r"\text{Null-space basis (columns): } " + bmat(N, 3) +
                 rf",\qquad \max|A\,N| = {np.abs(A @ N).max():.1e}")
    else:
        st.success("Nullity 0: only x = 0 maps to 0, so the columns are independent.")
    if m == 2:
        st.caption("A 2×3 matrix has rank ≤ 2, so its null space is at least a line: a wide matrix always loses "
                   "information.")

    fig = go.Figure()
    L = 2.5
    if nullity == 1:
        d = N[:, 0] * L
        fig.add_trace(go.Scatter3d(x=[-d[0], d[0]], y=[-d[1], d[1]], z=[-d[2], d[2]], mode="lines",
                                   name="null space (line)", line=dict(color="#f87171", width=9)))
    elif nullity == 2:
        g = np.linspace(-L, L, 2)
        S_, T_ = np.meshgrid(g, g)
        P = S_[..., None] * N[:, 0] + T_[..., None] * N[:, 1]
        fig.add_trace(go.Surface(x=P[..., 0], y=P[..., 1], z=P[..., 2], opacity=0.4, showscale=False,
                                 colorscale=[[0, "#f87171"], [1, "#f87171"]], name="null space (plane)"))
    elif nullity == 3:
        st.warning("A is the zero matrix: every vector is in the null space (nullity 3).")
    for i, row in enumerate(A):
        nrm = np.linalg.norm(row)
        if nrm > 0:
            r_ = row / nrm * L
            fig.add_trace(go.Scatter3d(x=[0, r_[0]], y=[0, r_[1]], z=[0, r_[2]], mode="lines+markers",
                                       name=f"row {i + 1} direction", line=dict(width=7),
                                       marker=dict(size=[0, 5])))
    fig.update_layout(height=460, margin=dict(l=0, r=0, t=10, b=0),
                      scene=dict(aspectmode="cube", xaxis=dict(range=[-L, L]), yaxis=dict(range=[-L, L]),
                                 zaxis=dict(range=[-L, L])))
    with right:
        st.plotly_chart(fig, width="stretch", key="p76_fig_null")
        st.caption("Row directions (scaled to equal length) are perpendicular to the red null space: "
                   "Ax = 0 means x has zero dot product with every row.")


def render_ai():
    st.header("🤖 AI / ML connection")
    t1, t2, t3 = st.tabs(["Embedding dimensions", "Low-rank structure (LoRA)", "Redundant features"])
    with t1:
        st.markdown(
            """
            A 768-dimensional sentence embedding lives in ℝ⁷⁶⁸, but a collection of embeddings often has most of
            its variance in far fewer directions — its *numerical* rank (singular values above a noise-level
            tolerance) is much smaller than 768. That is why PCA (page 63) or SVD (page 78) can shrink embeddings
            for search indexes with little loss. A linear layer `y = Wx` can only output vectors in the
            **column space** of `W`: if `W` has rank r, all outputs live in an r-dimensional subspace.
            """
        )
    with t2:
        r = st.slider("LoRA rank r", 1, 64, 8, key="p76_lora_r")
        d = 4096
        full, lora = d * d, 2 * d * r
        st.markdown(
            rf"""
            LoRA fine-tunes a big model by learning an update $\Delta W = BA$ with $B\in\mathbb{{R}}^{{d\times r}}$,
            $A\in\mathbb{{R}}^{{r\times d}}$, so $\text{{rank}}(\Delta W)\le r$. For a ${d}\times{d}$ layer:
            a full update has **{full:,}** parameters, LoRA with r = {r} has $2dr$ = **{lora:,}**
            (**{100 * lora / full:.2f}%**). The bet: the useful change lives in a low-dimensional subspace.
            """
        )
    with t3:
        st.markdown(
            r"""
            If feature 3 = feature 1 + feature 2 (e.g. *total price = base + tax*), the data matrix $X$ has a
            non-trivial **null space**: adding any null-space vector to the weights changes nothing in the
            predictions $Xw$. Then $X^\top X$ is singular, least squares has no unique answer, and nearly
            dependent features (**multicollinearity**) make the fitted weights wildly unstable. Fixes: drop
            redundant features, use the pseudo-inverse (page 77), or add L2 regularization (page 74).
            """
        )


def render_takeaways():
    st.header("✅ Key takeaways")
    st.markdown(
        """
        - **Span** = every linear combination; in ℝ² it is a point, a line or the whole plane.
        - **Independent** vectors have no redundancy; in 2-D: det ≠ 0 ⇔ rank 2.
        - **Basis** = independent + spanning ⇒ every vector has *unique* coordinates, found by solving Bc = w.
        - **Rank** = number of independent directions = number of non-zero singular values (above a tolerance).
        - **Rank–nullity**: rank + dim(null space) = number of columns.
        """
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        safe_page_link("pages/18Matrix Inverse — Undoing a Transform.py", "Previous: Matrix Inverse", icon="⬅️")
    with c2:
        safe_page_link("pages/63PCA Intuition — Finding the Best Angle.py", "Related: PCA Intuition", icon="📐")
    with c3:
        safe_page_link("pages/77Projections — Shadows onto Subspaces.py", "Next: Projections", icon="➡️")


def main():
    init_state()
    render_intro()
    V = render_combination_lab()
    st.divider()
    render_tolerance_lab(V)
    st.divider()
    render_basis_lab(V)
    st.divider()
    render_span3d()
    st.divider()
    render_null_space_lab()
    st.divider()
    render_ai()
    st.divider()
    render_takeaways()


main()
