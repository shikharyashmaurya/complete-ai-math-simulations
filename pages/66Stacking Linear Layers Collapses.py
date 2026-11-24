import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.mathutils import fmt_num, sigmoid  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="66 · Stacking Linear Layers Collapses", page_icon="🥞", layout="wide")

ACTIVATIONS = ["None (purely linear)", "ReLU", "tanh"]
H_COLOR, V_COLOR = "#38bdf8", "#f472b6"


# ---------------------------------------------------------------- helpers
def bmat(a, prec=2):
    """LaTeX bmatrix; 1-D arrays are shown as column vectors."""
    a = np.asarray(a, dtype=float)
    if a.ndim == 1:
        a = a.reshape(-1, 1)
    rows = [" & ".join(fmt_num(v, prec) for v in row) for row in a]
    return r"\begin{bmatrix}" + r" \\ ".join(rows) + r"\end{bmatrix}"


def activate(z, name):
    if name == "ReLU":
        return np.maximum(z, 0.0)
    if name == "tanh":
        return np.tanh(z)
    return z


def make_layers(k, width, seed):
    """k weight matrices for dims 2 -> width -> ... -> width -> 2 (scaled ~1/sqrt(fan_in) so depth stays tame)."""
    rng = np.random.default_rng(seed)
    dims = [2] + [width] * (k - 1) + [2]
    weights, biases = [], []
    for fan_in, fan_out in zip(dims[:-1], dims[1:]):
        weights.append(rng.normal(0.0, 1.2 / np.sqrt(fan_in), size=(fan_out, fan_in)))
        biases.append(rng.normal(0.0, 0.3, size=fan_out))
    return weights, biases


def deep_forward(X, weights, biases, act):
    """Row-wise forward pass; the activation sits between layers (never after the last one)."""
    h = X
    for i, (W, b) in enumerate(zip(weights, biases)):
        h = h @ W.T + b
        if i < len(weights) - 1:
            h = activate(h, act)
    return h


def collapse(weights, biases):
    """W_eff = W_k ... W_1 and b_eff via b <- W_i b + b_i (the activation-free composition)."""
    W_eff = np.eye(2)
    b_eff = np.zeros(2)
    for W, b in zip(weights, biases):
        W_eff = W @ W_eff
        b_eff = W @ b_eff + b
    return W_eff, b_eff


def grid_lines(n_lines=9, n_pts=60, lim=2.0):
    """Horizontal and vertical grid lines as point arrays (one array per line)."""
    t = np.linspace(-lim, lim, n_pts)
    vals = np.linspace(-lim, lim, n_lines)
    horiz = [np.column_stack([t, np.full_like(t, v)]) for v in vals]
    vert = [np.column_stack([np.full_like(t, v), t]) for v in vals]
    return horiz, vert


def lines_trace(lines, color, name):
    xs, ys = [], []
    for pts in lines:
        xs.extend(pts[:, 0].tolist() + [None])
        ys.extend(pts[:, 1].tolist() + [None])
    return go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=color, width=1.6), name=name, hoverinfo="skip")


def square_range(arrays):
    pts = np.vstack(arrays)
    lo, hi = pts.min(axis=0), pts.max(axis=0)
    center = (lo + hi) / 2
    half = max(float(np.max(hi - lo)) / 2, 1e-3) * 1.12
    return [center[0] - half, center[0] + half], [center[1] - half, center[1] + half]


def grid_figure(horiz, vert, title, xr, yr):
    fig = go.Figure([lines_trace(horiz, H_COLOR, "horizontal lines"), lines_trace(vert, V_COLOR, "vertical lines")])
    fig.update_layout(
        title=title, template="plotly_dark", height=360, showlegend=False, margin=dict(l=10, r=10, t=45, b=10),
        xaxis=dict(range=xr, zeroline=False), yaxis=dict(range=yr, zeroline=False, scaleanchor="x", scaleratio=1),
    )
    return fig


# ---------------------------------------------------------------- sections
def render_intro():
    st.title("🥞 Stacking Linear Layers Collapses")
    st.markdown(
        "Stack ten sheets of glass that each **stretch, rotate and shift** the picture behind them. "
        "Looking through all ten at once, you just see **one** stretch-rotate-shift. Linear layers behave exactly "
        "like that: however many you stack, the whole tower is equivalent to **a single linear layer**."
    )
    with st.container(border=True):
        st.markdown("**The one-line proof** (two layers; repeat it for more):")
        st.latex(r"W^{2}\big(W^{1}x+b^{1}\big)+b^{2} \;=\; \underbrace{(W^{2}W^{1})}_{W_{\text{new}}}\,x"
                 r"\;+\;\underbrace{(W^{2}b^{1}+b^{2})}_{b_{\text{new}}}")
    st.info(
        "Why it matters for AI: depth only buys expressive power when something **non-linear** (ReLU, GELU, tanh…) "
        "sits between the matrix multiplications. Without it, a 100-layer network is a fancy way to write one matrix."
    )


def render_collapse_lab(seed):
    st.header("🧪 Lab 1 — Stack k linear layers, then collapse them")
    c1, c2, c3 = st.columns(3)
    with c1:
        k = st.slider("Number of layers k", 1, 10, 4, key="p66_k")
    with c2:
        width = st.select_slider("Hidden width (neurons per hidden layer)", options=[1, 2, 3, 4, 6], value=3,
                                 key="p66_width", help="Width 1 is a bottleneck: everything is squeezed through one number.")
    with c3:
        act = st.radio("Between layers put…", ACTIVATIONS, key="p66_act", horizontal=False)

    weights, biases = make_layers(k, width, seed)
    W_eff, b_eff = collapse(weights, biases)
    horiz, vert = grid_lines()
    all_pts = np.vstack(horiz + vert)
    deep_out = deep_forward(all_pts, weights, biases, act)
    coll_out = all_pts @ W_eff.T + b_eff
    max_diff = float(np.max(np.abs(deep_out - coll_out)))
    scale = max(1.0, float(np.max(np.abs(coll_out))))
    matches = max_diff <= 1e-12 * scale

    n = len(horiz[0])
    split = lambda out: [out[i * n:(i + 1) * n] for i in range(len(horiz) + len(vert))]  # noqa: E731
    deep_lines, coll_lines = split(deep_out), split(coll_out)
    xr, yr = square_range([deep_out, coll_out])

    g1, g2, g3 = st.columns(3)
    with g1:
        st.plotly_chart(grid_figure(horiz, vert, "Input grid x ∈ [−2, 2]²", [-2.3, 2.3], [-2.3, 2.3]), width="stretch")
    with g2:
        title = f"Deep net: {k} layer(s)" + ("" if act == ACTIVATIONS[0] or k == 1 else f" with {act}")
        st.plotly_chart(grid_figure(deep_lines[:len(horiz)], deep_lines[len(horiz):], title, xr, yr), width="stretch")
    with g3:
        st.plotly_chart(grid_figure(coll_lines[:len(horiz)], coll_lines[len(horiz):],
                                    "Collapsed map W_eff·x + b_eff", xr, yr), width="stretch")

    m1, m2, m3 = st.columns(3)
    m1.metric("max |deep − collapsed| over the grid", f"{max_diff:.2e}")
    ranks = [int(np.linalg.matrix_rank(W)) for W in weights]
    rank_eff = int(np.linalg.matrix_rank(W_eff))
    m2.metric("rank(W_eff)", rank_eff, help="≤ the smallest rank of any factor (and ≤ the narrowest width).")
    m3.metric("Parameters in the stack vs collapsed", f"{sum(W.size + b.size for W, b in zip(weights, biases))} vs 6")

    if k == 1:
        st.info("With k = 1 there is no hidden layer, so there is nowhere to put an activation: the net *is* one linear map.")
    elif act == ACTIVATIONS[0]:
        if matches:
            st.success(f"Outputs agree to within 10⁻¹² (relative to the output scale): the {k}-layer stack **is** one "
                       "2×2 matrix plus a bias. Straight, parallel, evenly spaced grid lines stay that way.")
        else:
            st.warning(f"Difference {max_diff:.2e} is above 10⁻¹² — only floating-point round-off can cause this.")
    else:
        st.error(f"With {act} between layers the two pictures differ by up to {max_diff:.2f}: the grid **bends and folds** "
                 "in the deep net, which no single matrix can do. The collapse is broken — that is the whole point of activations.")

    left, right = st.columns(2)
    with left:
        st.markdown("**The single equivalent layer (ignoring activations):**")
        st.latex(r"W_{\text{eff}} = W^{%d}\cdots W^{1} = %s,\qquad b_{\text{eff}} = %s" % (k, bmat(W_eff, 3), bmat(b_eff, 3)))
        st.caption("Built left to right with W ← Wᵢ·W and b ← Wᵢ·b + bᵢ.")
    with right:
        rows = [{"layer": i + 1, "shape": f"{W.shape[0]}×{W.shape[1]}", "rank": r} for i, (W, r) in enumerate(zip(weights, ranks))]
        st.dataframe(rows, hide_index=True, width="stretch")
    with st.container(border=True):
        st.markdown(
            rf"**Rank note (bottleneck).** $\operatorname{{rank}}(AB)\le\min(\operatorname{{rank}}A,\operatorname{{rank}}B)$, "
            rf"so here $\operatorname{{rank}}(W_\text{{eff}}) = {rank_eff} \le \min_i \operatorname{{rank}}(W^i) = {min(ranks)}$. "
            "Set the hidden width to **1**: every point is squeezed through one number, so the output grid collapses "
            "onto a **line** (rank 1) — depth can never recover the lost dimension."
        )


def xor_data(n_per, spread, seed):
    rng = np.random.default_rng(seed + 1000)
    centers = np.array([[0, 0], [1, 1], [0, 1], [1, 0]], dtype=float)
    labels = np.array([0, 0, 1, 1])
    X = np.vstack([c + rng.normal(0, spread, size=(n_per, 2)) for c in centers])
    y = np.repeat(labels, n_per).astype(float)
    return X, y


def adam_train(params, grad_fn, steps=1500, lr=0.05):
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    for t in range(1, steps + 1):
        grads = grad_fn(params)
        for i, g in enumerate(grads):
            m[i] = 0.9 * m[i] + 0.1 * g
            v[i] = 0.999 * v[i] + 0.001 * g * g
            params[i] = params[i] - lr * (m[i] / (1 - 0.9 ** t)) / (np.sqrt(v[i] / (1 - 0.999 ** t)) + 1e-8)
    return params


@st.cache_data(show_spinner=False)
def train_linear(X, y):
    Xc = X - 0.5

    def grads(p):
        w, b = p
        d = (sigmoid(Xc @ w + b) - y) / len(y)
        return [Xc.T @ d, np.array(d.sum())]

    return adam_train([np.zeros(2), np.array(0.0)], grads)


@st.cache_data(show_spinner=False)
def train_relu(X, y, width, seed):
    rng = np.random.default_rng(seed + 7)
    Xc = X - 0.5
    params = [rng.normal(0, 1.0, (2, width)), rng.normal(0, 0.1, width), rng.normal(0, 1 / np.sqrt(width), width), np.array(0.0)]

    def grads(p):
        W1, b1, w2, b2 = p
        z1 = Xc @ W1 + b1
        h = np.maximum(z1, 0)
        d = (sigmoid(h @ w2 + b2) - y) / len(y)
        dz1 = np.outer(d, w2) * (z1 > 0)
        return [Xc.T @ dz1, dz1.sum(axis=0), h.T @ d, np.array(d.sum())]

    return adam_train(params, grads)


def relu_logit(X, params):
    W1, b1, w2, b2 = params
    return np.maximum((X - 0.5) @ W1 + b1, 0) @ w2 + b2


def handbuilt_logit(X):
    """s = ReLU(x1+x2) − 2·ReLU(x1+x2−1) is 0, 1, 1, 0 on the four XOR corners; logit = 8(s − ½)."""
    u = X[:, 0] + X[:, 1]
    return 8.0 * (np.maximum(u, 0) - 2 * np.maximum(u - 1, 0) - 0.5)


def region_figure(logit_fn, X, y, title):
    g = np.linspace(-0.6, 1.6, 110)
    gx, gy = np.meshgrid(g, g)
    P = sigmoid(logit_fn(np.column_stack([gx.ravel(), gy.ravel()]))).reshape(gx.shape)
    fig = go.Figure(go.Heatmap(x=g, y=g, z=P, zmin=0, zmax=1, colorscale=[[0, "#1e3a8a"], [0.5, "#334155"], [1, "#9d174d"]],
                               colorbar=dict(title="P(class 1)"), hovertemplate="x1=%{x:.2f}<br>x2=%{y:.2f}<br>P=%{z:.2f}<extra></extra>"))
    fig.add_trace(go.Contour(x=g, y=g, z=P, contours=dict(start=0.5, end=0.5, coloring="none"), line=dict(color="white", width=2),
                             showscale=False, hoverinfo="skip"))
    for cls, color, sym in ((0, "#60a5fa", "circle"), (1, "#f472b6", "x")):
        mask = y == cls
        fig.add_trace(go.Scatter(x=X[mask, 0], y=X[mask, 1], mode="markers", name=f"class {cls}",
                                 marker=dict(color=color, symbol=sym, size=7, line=dict(color="white", width=0.5))))
    fig.update_layout(title=title, template="plotly_dark", height=400, margin=dict(l=10, r=10, t=45, b=10),
                      xaxis=dict(range=[-0.6, 1.6]), yaxis=dict(range=[-0.6, 1.6], scaleanchor="x", scaleratio=1),
                      legend=dict(orientation="h", y=-0.12))
    return fig


def render_xor_lab(seed):
    st.header("🧪 Lab 2 — XOR: a deep linear net vs one hidden ReLU layer")
    st.markdown(
        r"Any stack of linear layers collapses to $W_\text{eff}x+b_\text{eff}$, so its decision boundary "
        r"$W_\text{eff}x+b_\text{eff}=0$ is **one straight line**, whatever the depth. We therefore fit the best line directly "
        "(logistic regression). One hidden layer **with ReLU** can carve out a band instead."
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        n_per = st.slider("Points per corner", 5, 50, 20, key="p66_xor_n")
    with c2:
        spread = st.slider("Cluster spread σ", 0.02, 0.30, 0.12, 0.02, key="p66_xor_spread")
    with c3:
        relu_mode = st.radio("Hidden ReLU layer", ["Hand-built (2 units)", "Trained (Adam, numpy)"], key="p66_relu_mode")
    width = st.slider("Hidden units (trained net)", 2, 16, 6, key="p66_relu_width",
                      help="Only used by the trained net; the hand-built net always has 2 units.")

    X, y = xor_data(n_per, spread, seed)
    w_lin, b_lin = train_linear(X, y)
    lin_logit = lambda Z: (Z - 0.5) @ w_lin + b_lin  # noqa: E731
    if relu_mode.startswith("Hand"):
        nl_logit = handbuilt_logit
    else:
        p_relu = train_relu(X, y, width, seed)
        nl_logit = lambda Z: relu_logit(Z, p_relu)  # noqa: E731
    acc_lin = float(np.mean((lin_logit(X) > 0) == (y == 1)))
    acc_nl = float(np.mean((nl_logit(X) > 0) == (y == 1)))

    a, b = st.columns(2)
    with a:
        st.plotly_chart(region_figure(lin_logit, X, y, "Deep LINEAR net ≡ one line"), width="stretch")
        st.metric("Training accuracy (linear)", f"{acc_lin:.0%}")
    with b:
        st.plotly_chart(region_figure(nl_logit, X, y, f"1 hidden ReLU layer ({relu_mode.split(' (')[0].lower()})"), width="stretch")
        st.metric("Training accuracy (ReLU)", f"{acc_nl:.0%}")
    st.caption("No line can get more than 3 of the 4 XOR corners right (≤ 75 % on the clean corners). The hand-built net uses "
               r"s = ReLU(x₁+x₂) − 2·ReLU(x₁+x₂−1), which is 0, 1, 1, 0 on (0,0), (0,1), (1,0), (1,1).")
    acc_hand = float(np.mean((handbuilt_logit(X) > 0) == (y == 1)))
    if not relu_mode.startswith("Hand") and acc_nl < acc_hand - 0.05:
        st.warning(f"This training run got stuck ({acc_nl:.0%} vs {acc_hand:.0%} for the hand-built net): dead ReLUs or a bad "
                   "start. The *capacity* is there, so try more hidden units or 🎲 Resample — with only 2 units gradient "
                   "descent often lands in a 75 % local minimum.")


def render_worked_example(seed):
    st.header("🔢 Worked example — a 2 → 3 → 2 linear net, computed both ways")
    rng = np.random.default_rng(seed + 500)
    W1 = rng.integers(-2, 3, size=(3, 2)).astype(float)
    b1 = rng.integers(-2, 3, size=3).astype(float)
    W2 = rng.integers(-2, 3, size=(2, 3)).astype(float)
    b2 = rng.integers(-2, 3, size=2).astype(float)
    c1, c2 = st.columns(2)
    with c1:
        x1 = st.slider("x₁", -3.0, 3.0, 1.0, 0.5, key="p66_x1")
    with c2:
        x2 = st.slider("x₂", -3.0, 3.0, -0.5, 0.5, key="p66_x2")
    x = np.array([x1, x2])
    st.latex(rf"W^1={bmat(W1, 0)},\; b^1={bmat(b1, 0)},\quad W^2={bmat(W2, 0)},\; b^2={bmat(b2, 0)},\quad x={bmat(x)}")

    h = W1 @ x + b1
    y_layer = W2 @ h + b2
    W_new = W2 @ W1
    b_new = W2 @ b1 + b2
    y_coll = W_new @ x + b_new
    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.markdown("**Path A — layer by layer**")
            st.latex(rf"h = W^1x+b^1 = {bmat(h)}")
            st.latex(rf"y = W^2h+b^2 = {bmat(y_layer)}")
    with right:
        with st.container(border=True):
            st.markdown("**Path B — collapse first**")
            st.latex(rf"W_\text{{new}} = W^2W^1 = {bmat(W_new, 0)},\quad b_\text{{new}} = W^2b^1+b^2 = {bmat(b_new, 0)}")
            st.latex(rf"y = W_\text{{new}}x + b_\text{{new}} = {bmat(y_coll)}")
    diff = float(np.max(np.abs(y_layer - y_coll)))
    r1, r2, rn = (int(np.linalg.matrix_rank(M)) for M in (W1, W2, W_new))
    st.success(f"Both paths give the same y (max difference {diff:.1e}). The 3-neuron stack uses 17 parameters "
               "but the function is still just a 2×2 matrix and a bias (6 numbers).")
    st.markdown(rf"Ranks: $\operatorname{{rank}}W^1={r1}$, $\operatorname{{rank}}W^2={r2}$, "
                rf"$\operatorname{{rank}}W_\text{{new}}={rn}\le\min({r1},{r2})$.")


def render_ai_connection(seed):
    st.header("🤖 AI / ML connection")
    st.markdown(
        r"""
- **Every hidden layer needs a non-linearity.** A Transformer MLP block is `Linear → GELU/SwiGLU → Linear`;
  delete the GELU and the two big matrices merge into one, wasting the hidden width.
- **Intentional linear factorizations are useful, though.** Attention scores use
  $q^\top k = (W_Q x)^\top (W_K x') = x^\top W_Q^\top W_K\, x'$: two stacked linear maps with **no** activation,
  i.e. a deliberately **low-rank** ($\le d_\text{head}$) bilinear form.
- **Linear attention** drops the softmax so $(\phi(Q)\phi(K)^\top)V$ can be re-associated as $\phi(Q)(\phi(K)^\top V)$,
  turning cost quadratic in sequence length into linear — associativity of linear maps at work.
- **LoRA** fine-tunes a frozen $W$ via $W + BA$ with thin $B\in\mathbb R^{d\times r}$, $A\in\mathbb R^{r\times d}$.
  Because $B(Ax)$ is a linear stack, after training it **collapses** into one matrix $W' = W+BA$: zero extra inference cost.
"""
    )
    c1, c2 = st.columns(2)
    with c1:
        d = st.select_slider("Layer width d", options=[64, 256, 1024, 4096, 8192], value=4096, key="p66_lora_d")
    with c2:
        r = st.slider("LoRA rank r", 1, 64, 8, key="p66_lora_r")
    full, lora = d * d, 2 * d * r
    small_d = 8
    rng = np.random.default_rng(seed + 900)
    B = rng.normal(size=(small_d, min(r, small_d)))
    A = rng.normal(size=(min(r, small_d), small_d))
    m1, m2, m3 = st.columns(3)
    m1.metric("Full update d²", f"{full:,}")
    m2.metric("LoRA params 2·d·r", f"{lora:,}", delta=f"{lora / full:.2%} of full", delta_color="off")
    m3.metric(f"rank(BA) on a {small_d}×{small_d} check", int(np.linalg.matrix_rank(B @ A)),
              help=f"Never more than min(r, {small_d}) — the bottleneck rule from Lab 1.")


def render_takeaways():
    st.header("✅ Key takeaways")
    st.markdown(
        "1. $W^2(W^1x+b^1)+b^2=(W^2W^1)x+(W^2b^1+b^2)$: any number of linear layers equals **one** linear layer.\n"
        "2. The collapsed map keeps straight lines straight and parallel lines parallel; activations bend and fold space.\n"
        "3. Rank of a product ≤ smallest rank of its factors — a narrow layer is a permanent bottleneck.\n"
        "4. A linear net of any depth draws one straight boundary, so it cannot solve XOR; one hidden ReLU layer can.\n"
        r"5. Linear stacks are still handy *on purpose*: low-rank factorizations (LoRA, $W_Q^\top W_K$), mergeable adapters."
    )
    c1, c2 = st.columns(2)
    with c1:
        safe_page_link("pages/65Activation Functions Compared.py", "← Previous: Activation Functions Compared")
    with c2:
        safe_page_link("pages/67Neural Network as Matrix Layers.py", "Next: Neural Network as Matrix Layers →")


def main():
    st.session_state.setdefault("p66_seed", 66)
    render_intro()
    top = st.columns([4, 1])
    with top[1]:
        if st.button("🎲 Resample weights & data", key="p66_resample"):
            st.session_state["p66_seed"] += 1
    seed = int(st.session_state["p66_seed"])
    top[0].caption(f"Random seed: {seed} — all weights and data below are reproducible from it.")
    render_collapse_lab(seed)
    st.divider()
    render_xor_lab(seed)
    st.divider()
    render_worked_example(seed)
    st.divider()
    render_ai_connection(seed)
    st.divider()
    render_takeaways()


main()
