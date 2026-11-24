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
from common.mathutils import fmt_factor, fmt_num  # noqa: E402

st.set_page_config(page_title="97 · Embeddings", page_icon="🗺️", layout="wide")

DIMS = ["royalty", "gender (+male / −female)", "plural", "animal"]
SHORT = ["royalty", "gender", "plural", "animal"]
# Hand-crafted toy embedding: every coordinate has a meaning (real learned embeddings do not).
VOCAB = {
    "king": [0.95, 0.90, 0.0, 0.0],
    "queen": [0.95, -0.90, 0.0, 0.0],
    "man": [0.05, 0.90, 0.0, 0.0],
    "woman": [0.05, -0.90, 0.0, 0.0],
    "prince": [0.75, 0.80, 0.0, 0.0],
    "princess": [0.75, -0.80, 0.0, 0.0],
    "kings": [0.95, 0.90, 0.9, 0.0],
    "queens": [0.95, -0.90, 0.9, 0.0],
    "men": [0.05, 0.90, 0.9, 0.0],
    "women": [0.05, -0.90, 0.9, 0.0],
    "boy": [0.0, 0.70, 0.0, 0.0],
    "girl": [0.0, -0.70, 0.0, 0.0],
    "lion": [0.50, 0.60, 0.0, 0.95],
    "lioness": [0.50, -0.60, 0.0, 0.95],
    "stallion": [0.0, 0.80, 0.0, 0.90],
    "mare": [0.0, -0.80, 0.0, 0.90],
    "cat": [0.0, -0.05, 0.0, 0.90],
    "cats": [0.0, -0.05, 0.9, 0.90],
    "dog": [0.0, 0.05, 0.0, 0.90],
    "dogs": [0.0, 0.05, 0.9, 0.90],
    "crown": [0.90, 0.0, 0.0, 0.0],
}
WORDS = list(VOCAB)
E_CLEAN = np.array(list(VOCAB.values()), dtype=float)
EPS = 1e-12


# ---------------------------------------------------------------- maths helpers
def embeddings(noise, seed):
    """4-d toy table plus seeded Gaussian noise, and an 8-d 'learned-looking' version (rotated, extra noise dims)."""
    rng = np.random.default_rng(seed)
    e4 = E_CLEAN + noise * rng.normal(size=E_CLEAN.shape)
    extra = 0.05 * rng.normal(size=(len(WORDS), 4))
    q, _ = np.linalg.qr(rng.normal(size=(8, 8)))  # random orthogonal 8×8
    e8 = np.hstack([e4, extra]) @ q
    return e4, e8


def cosine_to_all(v, mat):
    norms = np.linalg.norm(mat, axis=1) * np.linalg.norm(v)
    return (mat @ v) / np.maximum(norms, EPS)  # guard: a zero vector gets similarity 0, not NaN


def top_k(v, mat, k, exclude=()):
    sims = cosine_to_all(v, mat)
    order = [i for i in np.argsort(-sims, kind="stable") if WORDS[i] not in exclude]
    return [(WORDS[i], float(sims[i])) for i in order[:k]]


def positional_encoding(n_pos, d):
    """Sinusoidal PE: PE[p, 2i] = sin(p / 10000^(2i/d)), PE[p, 2i+1] = cos(p / 10000^(2i/d))."""
    pos = np.arange(n_pos)[:, None]
    omega = 1.0 / 10000 ** (np.arange(0, d, 2) / d)
    pe = np.zeros((n_pos, d))
    pe[:, 0::2] = np.sin(pos * omega)
    pe[:, 1::2] = np.cos(pos * omega)
    return pe, omega


def pca(x):
    xc = x - x.mean(axis=0)
    _, s, vt = np.linalg.svd(xc, full_matrices=False)
    var = s ** 2 / max(len(x) - 1, 1)
    return xc @ vt.T, var, xc


# ---------------------------------------------------------------- page sections
def intuition():
    st.title("🗺️ Embeddings — Words as Points in Space")
    st.markdown(
        r"""
A neural network can only multiply numbers, but its input is often a **token** — a word, sub-word, product id or
user id. An **embedding** gives every token its own learned vector: a row in a big table $E$ with one row per
vocabulary item and $d$ columns. Training nudges the rows so that tokens used in similar ways end up **close
together** — "king" near "queen", "cat" near "dog".

Once tokens are points, geometry becomes meaning: **cosine similarity** measures relatedness, and **directions**
can encode concepts (a "gender" direction, a "plural" direction). Below we use a tiny, *hand-made* table whose 4
coordinates are interpretable — **royalty, gender, plural, animal** — so you can see why the tricks work, and where they break.
"""
    )


def lab_lookup(e4):
    st.subheader("An embedding layer is a lookup table")
    word = st.selectbox("Token", WORDS, key="p97_lookup_word")
    i = WORDS.index(word)
    one_hot = np.zeros(len(WORDS))
    one_hot[i] = 1.0
    via_matmul = one_hot @ e4
    via_lookup = e4[i]
    left, right = st.columns([3, 2])
    with left:
        fig = go.Figure(go.Heatmap(z=e4, x=SHORT, y=WORDS, colorscale="RdBu", zmid=0, colorbar=dict(thickness=10)))
        fig.add_shape(type="rect", x0=-0.5, x1=len(SHORT) - 0.5, y0=i - 0.5, y1=i + 0.5, line=dict(color="#f59e0b", width=3))
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(title=f"Embedding table E ({len(WORDS)} × {len(SHORT)}) — row '{word}' highlighted", height=520, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig, width="stretch")
    with right:
        st.markdown(f"**One-hot vector** for '{word}' (length {len(WORDS)}, a single 1 at index {i}):")
        st.code("[" + ", ".join("1" if v else "0" for v in one_hot) + "]", language=None)
        st.dataframe(pd.DataFrame({"one-hot × E": via_matmul, f"E[{i}] (lookup)": via_lookup}, index=SHORT).round(4), width="stretch")
        if np.array_equal(via_matmul, via_lookup):
            st.success("✓ Exactly equal: multiplying by a one-hot vector just selects one row.")
        st.caption(f"So frameworks skip the {len(WORDS)}×{len(SHORT)} matrix product and index the row directly — O(d) instead of O(V·d) work.")


def lab_space(e4):
    st.subheader("Embedding space & nearest neighbours")
    c1, c2, c3, c4 = st.columns(4)
    word = c1.selectbox("Query word", WORDS, index=WORDS.index("king"), key="p97_query")
    k = c2.slider("Top-k neighbours", 1, 10, 5, key="p97_k")
    xa = c3.selectbox("x-axis", SHORT, index=0, key="p97_xaxis")
    ya = c4.selectbox("y-axis", SHORT, index=1, key="p97_yaxis")
    three_d = st.toggle("3D view (z = plural)", value=False, key="p97_3d")
    neigh = top_k(e4[WORDS.index(word)], e4, k, exclude=(word,))
    neigh_words = {w for w, _ in neigh}
    colours = ["#f59e0b" if w == word else "#22d3ee" if w in neigh_words else "#64748b" for w in WORDS]
    xi, yi = SHORT.index(xa), SHORT.index(ya)
    left, right = st.columns([3, 2])
    with left:
        if three_d:
            fig = go.Figure(go.Scatter3d(x=e4[:, xi], y=e4[:, yi], z=e4[:, 2], text=WORDS, mode="markers+text", marker=dict(size=5, color=colours)))
            fig.update_layout(scene=dict(xaxis_title=xa, yaxis_title=ya, zaxis_title="plural"), height=520, margin=dict(l=0, r=0, t=30, b=0))
        else:
            fig = go.Figure(go.Scatter(x=e4[:, xi], y=e4[:, yi], text=WORDS, mode="markers+text", textposition="top center", marker=dict(size=10, color=colours)))
            fig.update_layout(xaxis_title=xa, yaxis_title=ya, height=520, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig, width="stretch")
        if xa == ya:
            st.warning("x and y show the same dimension, so every point sits on the diagonal — pick two different axes.")
        st.caption("Orange = query, cyan = its top-k neighbours by cosine similarity in the full 4-d space (a 2-D view can hide or fake closeness).")
    with right:
        st.dataframe(pd.DataFrame(neigh, columns=["neighbour", "cosine similarity"]).round(3), hide_index=True, width="stretch")
        st.latex(r"\cos(\mathbf u, \mathbf v) = \frac{\mathbf u \cdot \mathbf v}{\lVert \mathbf u\rVert\,\lVert \mathbf v\rVert}")


def lab_arithmetic(e4):
    st.subheader("Vector arithmetic:  a − b + c ≈ ?")
    c1, c2, c3, c4 = st.columns(4)
    a = c1.selectbox("a", WORDS, index=WORDS.index("king"), key="p97_a")
    b = c2.selectbox("− b", WORDS, index=WORDS.index("man"), key="p97_b")
    c = c3.selectbox("+ c", WORDS, index=WORDS.index("woman"), key="p97_c")
    exclude = c4.toggle("Exclude a, b, c from answers", value=True, key="p97_exclude")
    target = e4[WORDS.index(a)] - e4[WORDS.index(b)] + e4[WORDS.index(c)]
    ranked = top_k(target, e4, 5, exclude=(a, b, c) if exclude else ())
    left, right = st.columns([2, 3])
    with left:
        st.markdown(f"**{a} − {b} + {c}** = `[{', '.join(fmt_num(v) for v in target)}]`")
        st.dataframe(pd.DataFrame(ranked, columns=["candidate", "cosine"]).round(3), hide_index=True, width="stretch")
        if ranked:
            st.metric("Top answer", ranked[0][0], f"cos = {ranked[0][1]:.3f}")
    with right:
        ia, ib, ic = (WORDS.index(w) for w in (a, b, c))
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=e4[:, 0], y=e4[:, 1], text=WORDS, mode="markers+text", textposition="top center", marker=dict(color="#64748b"), name="words"))
        for (s, t), colour, name in (((ib, ic), "#22d3ee", f"{b} → {c}"), ((ia, None), "#f59e0b", f"{a} + ({c} − {b})")):
            start = e4[s, :2]
            end = e4[t, :2] if t is not None else target[:2]
            fig.add_annotation(x=end[0], y=end[1], ax=start[0], ay=start[1], xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=3, arrowwidth=2, arrowcolor=colour)
            fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines", line=dict(color=colour), name=name))
        fig.add_trace(go.Scatter(x=[target[0]], y=[target[1]], mode="markers", marker=dict(symbol="x", size=14, color="#f472b6"), name="result"))
        fig.update_layout(xaxis_title="royalty", yaxis_title="gender", height=420, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig, width="stretch")
    st.info(
        "**Caveats.** The analogy works perfectly here because the table was built with clean, parallel directions. "
        "Raise the noise slider to see it degrade. In real word2vec/GloVe embeddings the offsets are only roughly parallel, "
        "the answer is usually found only *after excluding the input words* (otherwise the nearest vector to "
        "king − man + woman is often 'king' itself), and many famous analogies fail or reflect biases in the training text."
    )


def lab_pca(e8):
    st.subheader("PCA view of an 8-d embedding")
    st.markdown(
        "Real embeddings are high-dimensional and their axes mean nothing on their own. Here the 4-d table is padded with 4 small "
        "noise dimensions and then **randomly rotated** in 8-d, so no single coordinate is interpretable — yet PCA recovers the structure."
    )
    proj, var, xc = pca(e8)
    ratio = var / max(var.sum(), EPS)
    left, right = st.columns([3, 2])
    with left:
        fig = go.Figure(go.Scatter(x=proj[:, 0], y=proj[:, 1], text=WORDS, mode="markers+text", textposition="top center", marker=dict(size=9, color="#38bdf8")))
        fig.update_layout(xaxis_title=f"PC1 ({ratio[0]:.0%} of variance)", yaxis_title=f"PC2 ({ratio[1]:.0%})", height=460, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig, width="stretch")
    with right:
        fig2 = go.Figure(go.Bar(x=[f"PC{i + 1}" for i in range(len(ratio))], y=ratio, marker_color="#a78bfa"))
        fig2.add_trace(go.Scatter(x=[f"PC{i + 1}" for i in range(len(ratio))], y=np.cumsum(ratio), mode="lines+markers", name="cumulative", line=dict(color="#f59e0b")))
        fig2.update_layout(title="Explained variance ratio", height=320, showlegend=False, margin=dict(l=10, r=10, t=40, b=10), yaxis=dict(range=[0, 1.05]))
        st.plotly_chart(fig2, width="stretch")
        st.metric("Variance kept by the first 4 PCs", f"{np.cumsum(ratio)[3]:.1%}")
        eig = np.sort(np.linalg.eigvalsh(np.cov(xc, rowvar=False)))[::-1]
        st.caption(f"Check: SVD variances vs eigenvalues of the covariance matrix — max |difference| = {np.max(np.abs(eig - var)):.1e}.")


def lab_positional():
    st.subheader("Positional encoding — telling the model *where* a token is")
    st.latex(r"PE_{(p,\,2i)} = \sin\!\left(\frac{p}{10000^{2i/d}}\right),\qquad PE_{(p,\,2i+1)} = \cos\!\left(\frac{p}{10000^{2i/d}}\right)")
    c1, c2, c3 = st.columns(3)
    d = c1.slider("d_model", 8, 128, 64, step=8, key="p97_d")
    n_pos = c2.slider("Positions", 10, 100, 50, key="p97_npos")
    st.session_state.setdefault("p97_ref", 10)
    st.session_state["p97_ref"] = min(st.session_state["p97_ref"], n_pos - 1)
    ref = c3.slider("Reference position", 0, n_pos - 1, key="p97_ref")
    pe, omega = positional_encoding(n_pos, d)
    left, right = st.columns(2)
    with left:
        fig = go.Figure(go.Heatmap(z=pe, colorscale="RdBu", zmid=0, colorbar=dict(thickness=10)))
        fig.update_yaxes(autorange="reversed", title="position p")
        fig.update_xaxes(title="dimension")
        fig.update_layout(title="PE matrix: fast waves on the left, slow on the right", height=420, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig, width="stretch")
    with right:
        sims = pe @ pe[ref]
        fig2 = go.Figure(go.Scatter(x=np.arange(n_pos), y=sims, mode="lines+markers", line=dict(color="#22d3ee")))
        fig2.add_vline(x=ref, line_dash="dot", line_color="#f59e0b")
        fig2.update_layout(title=f"PE[{ref}] · PE[q] — peaks at q = {ref} (= d/2 = {d // 2})", xaxis_title="position q", height=420, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig2, width="stretch")
    gram = pe @ pe.T
    diff = np.arange(n_pos)[:, None] - np.arange(n_pos)[None, :]
    predicted = np.cos(diff[..., None] * omega).sum(axis=-1)
    st.latex(r"PE_p \cdot PE_q = \sum_i \left[\sin(\omega_i p)\sin(\omega_i q) + \cos(\omega_i p)\cos(\omega_i q)\right] = \sum_i \cos\big(\omega_i (p-q)\big)")
    st.success(
        f"✓ Checked on all {n_pos}×{n_pos} pairs: the dot product depends only on the offset p − q "
        f"(max |difference| from Σ cos(ωᵢ(p−q)) = {np.max(np.abs(gram - predicted)):.1e}), so nearby positions look similar and the model can read relative distance."
    )


def worked_example(e4):
    st.header("🧮 Worked example — the analogy by hand")
    a, b, c = (st.session_state.get(key, default) for key, default in (("p97_a", "king"), ("p97_b", "man"), ("p97_c", "woman")))
    va, vb, vc = (e4[WORDS.index(w)] for w in (a, b, c))
    target = va - vb + vc
    exclude = (a, b, c) if st.session_state.get("p97_exclude", True) else ()
    best = top_k(target, e4, 1, exclude=exclude)
    vec = lambda v: r"\begin{bmatrix}" + r"\\".join(fmt_num(x) for x in v) + r"\end{bmatrix}"  # noqa: E731
    st.latex(rf"\underbrace{{{vec(va)}}}_{{\text{{{a}}}}} - \underbrace{{{vec(vb)}}}_{{\text{{{b}}}}} + \underbrace{{{vec(vc)}}}_{{\text{{{c}}}}} = {vec(target)}")
    if not best:
        st.warning("Every word was excluded — nothing left to rank.")
        return
    w, sim = best[0]
    vw = e4[WORDS.index(w)]
    dot = float(target @ vw)
    na, nw = float(np.linalg.norm(target)), float(np.linalg.norm(vw))
    terms = " + ".join(f"{fmt_factor(x)}\\cdot{fmt_factor(y)}" for x, y in zip(target, vw))
    st.latex(rf"\mathbf t \cdot \mathbf e_{{\text{{{w}}}}} = {terms} = {fmt_num(dot, 3)}")
    if na < EPS or nw < EPS:
        st.warning("A zero-length vector has no direction, so cosine similarity is undefined (reported as 0).")
    else:
        st.latex(rf"\cos = \frac{{{fmt_num(dot, 3)}}}{{{fmt_num(na, 3)} \times {fmt_num(nw, 3)}}} = {fmt_num(sim, 3)}")
    st.markdown(f"Nearest word{' (inputs excluded)' if exclude else ''}: **{w}**. Uses the words and noise level chosen in the labs above.")


def ai_connection():
    st.header("🤖 Where this shows up in real models")
    st.markdown(
        """
- **Token embeddings in LLMs**: the first layer of GPT/Llama is exactly this lookup — a table of ~32k–200k rows ×
  d = 768…16 384 columns. Many models *tie* it to the output layer, so the logits are dot products with the same rows.
- **Positional information**: the original Transformer *adds* the sinusoidal PE above to the token embedding;
  modern LLMs mostly use RoPE, which rotates query/key pairs by the same angles ωᵢ·p so attention sees p − q directly.
- **Retrieval / RAG and semantic search**: documents and queries are embedded by a model and matched by cosine
  similarity (often in a vector database with approximate nearest-neighbour search) before the LLM answers.
- **Recommenders**: user and item ids get embeddings; a dot product scores how well they match.
- **Dimension trade-off**: larger d stores more distinctions but costs memory (V·d parameters) and compute; tricks
  like Matryoshka embeddings or PCA truncation keep the most important directions first.
"""
    )


def takeaways():
    st.header("✅ Key takeaways")
    st.markdown(
        r"""
1. An embedding layer is a learned table $E \in \mathbb R^{V\times d}$; one-hot $\times E$ = a row of $E$, so it is implemented as a lookup.
2. Similar tokens get nearby vectors; cosine similarity ranks neighbours regardless of vector length.
3. Directions can carry meaning (king − man + woman ≈ queen), but in real, noisy embeddings this is approximate and biased.
4. PCA gives a faithful low-dimensional view when a few directions hold most of the variance.
5. Sinusoidal positional encodings make $PE_p\cdot PE_q$ a function of $p-q$ only — a built-in notion of distance.
"""
    )
    c1, c2 = st.columns(2)
    with c1:
        safe_page_link("pages/96Convolution.py", "Previous: 96 · Convolution", "⬅️")
    with c2:
        safe_page_link("pages/98Attention.py", "Next: 98 · Attention", "➡️")


def main():
    st.session_state.setdefault("p97_seed", 0)
    intuition()
    st.header("🔬 Interactive labs")
    c1, c2 = st.columns([3, 1])
    noise = c1.slider("Noise added to every embedding (0 = clean hand-made table)", 0.0, 0.5, 0.0, step=0.05, key="p97_noise")
    with c2:
        st.write("")
        if st.button("🎲 Resample noise", key="p97_resample"):
            st.session_state["p97_seed"] = st.session_state["p97_seed"] + 1
    e4, e8 = embeddings(noise, st.session_state["p97_seed"])
    tabs = st.tabs(["Lookup table", "Space & neighbours", "Vector arithmetic", "PCA of 8-d", "Positional encoding"])
    with tabs[0]:
        lab_lookup(e4)
    with tabs[1]:
        lab_space(e4)
    with tabs[2]:
        lab_arithmetic(e4)
    with tabs[3]:
        lab_pca(e8)
    with tabs[4]:
        lab_positional()
    worked_example(e4)
    ai_connection()
    takeaways()


main()
