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
from common.mathutils import fmt_factor, fmt_num, softmax  # noqa: E402

st.set_page_config(page_title="98 · Attention", page_icon="🎯", layout="wide")

SENTENCES = ["the cat sat on the mat", "time flies like an arrow", "she gave him the book", "the animal was too tired"]
VOCAB = sorted({w for s in SENTENCES for w in s.split()})


# ---------------------------------------------------------------- maths helpers
def positional_encoding(n_pos, d):
    pos = np.arange(n_pos)[:, None]
    omega = 1.0 / 10000 ** (np.arange(0, d, 2) / d)
    pe = np.zeros((n_pos, d))
    pe[:, 0::2] = np.sin(pos * omega)
    pe[:, 1::2] = np.cos(pos * omega)
    return pe


def build_params(seed, d_model):
    """Seeded toy token embeddings plus single-head and two-head projection matrices."""
    rng = np.random.default_rng(seed)
    emb = rng.normal(size=(len(VOCAB), d_model))
    s = 1.0 / np.sqrt(d_model)
    single = {name: rng.normal(size=(d_model, d_model)) * s for name in ("Wq", "Wk", "Wv", "Wo")}
    dh = d_model // 2
    heads = [{name: rng.normal(size=(d_model, dh)) * s for name in ("Wq", "Wk", "Wv")} for _ in range(2)]
    wo_multi = rng.normal(size=(2 * dh, d_model)) / np.sqrt(2 * dh)
    return emb, single, heads, wo_multi


def attention(x, wq, wk, wv, scale=True, causal=False, temp=1.0):
    """Scaled dot-product attention softmax(QKᵀ/√d_k / T) V, keeping every intermediate for the step-through."""
    q, k, v = x @ wq, x @ wk, x @ wv
    d_k = wq.shape[1]
    raw = q @ k.T
    scaled = raw / np.sqrt(d_k) if scale else raw.copy()
    logits = scaled / temp
    mask = np.triu(np.ones(raw.shape, dtype=bool), k=1) if causal else np.zeros(raw.shape, dtype=bool)
    logits = np.where(mask, -np.inf, logits)  # the diagonal is never masked, so every row keeps a finite max
    weights = softmax(logits, axis=-1)
    return dict(Q=q, K=k, V=v, raw=raw, scaled=scaled, logits=logits, mask=mask, A=weights, H=weights @ v, d_k=d_k)


def entropy_rows(p):
    return -np.sum(np.where(p > 0, p * np.log(np.where(p > 0, p, 1.0)), 0.0), axis=-1)


def attention_heatmap(weights, labels, title, height=420):
    fig = go.Figure(go.Heatmap(z=weights, x=labels, y=labels, zmin=0, zmax=1, colorscale="Viridis", text=np.round(weights, 2), texttemplate="%{text}", colorbar=dict(thickness=10)))
    fig.update_yaxes(autorange="reversed", title="query (row)")
    fig.update_xaxes(title="key (column)", side="top")
    fig.update_layout(title=title, height=height, margin=dict(l=10, r=10, t=70, b=10))
    return fig


# ---------------------------------------------------------------- page sections
def intuition():
    st.title("🎯 Attention — Every Token Asks, Every Token Answers")
    st.markdown(
        r"""
In "the cat sat on the **mat**", to understand *mat* a model should look back at *sat* and *on*. **Attention**
lets every token build its new representation as a **weighted average of all the other tokens**, with weights it
computes on the fly:

* each token emits a **query** $q$ ("what am I looking for?"), a **key** $k$ ("what do I contain?") and a
  **value** $v$ ("what do I pass on?") — three linear maps of its embedding, $Q = XW_Q,\ K = XW_K,\ V = XW_V$;
* the match between query $i$ and key $j$ is a **dot product** (page 6), turned into weights by **softmax** (page 37);
* the output for token $i$ is $\sum_j a_{ij} v_j$.
"""
    )
    st.latex(r"\operatorname{Attention}(Q,K,V) = \operatorname{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V")
    st.markdown("This single formula is the heart of every transformer — GPT, Llama, BERT, ViT, Whisper.")


def controls():
    c1, c2, c3 = st.columns([2, 2, 1])
    sentence = c1.selectbox("Sentence", SENTENCES, key="p98_sentence")
    d_model = c2.slider("d_model (embedding size)", 4, 16, 8, step=2, key="p98_dmodel")
    with c3:
        st.write("")
        if st.button("🎲 Resample weights", key="p98_resample"):
            st.session_state["p98_seed"] = st.session_state["p98_seed"] + 1
    t1, t2, t3, t4 = st.columns(4)
    use_pe = t1.toggle("Add positional encoding", value=True, key="p98_pe")
    causal = t2.toggle("Causal mask (GPT-style)", value=False, key="p98_causal")
    scale = t3.toggle("Divide by √d_k", value=True, key="p98_scale")
    temp = t4.slider("Temperature T", 0.1, 3.0, 1.0, step=0.1, key="p98_temp")
    tokens = sentence.split()
    emb, single, heads, wo_multi = build_params(st.session_state["p98_seed"], d_model)
    x = emb[[VOCAB.index(t) for t in tokens]]
    if use_pe:
        x = x + positional_encoding(len(tokens), d_model)
    labels = [f"{i}:{t}" for i, t in enumerate(tokens)]
    return dict(tokens=tokens, labels=labels, x=x, d_model=d_model, single=single, heads=heads, wo_multi=wo_multi, causal=causal, scale=scale, temp=temp, use_pe=use_pe)


def lab_map(cfg):
    p = cfg["single"]
    res = attention(cfg["x"], p["Wq"], p["Wk"], p["Wv"], cfg["scale"], cfg["causal"], cfg["temp"])
    left, right = st.columns([3, 2])
    with left:
        st.plotly_chart(attention_heatmap(res["A"], cfg["labels"], "Attention weights A (each row sums to 1)"), width="stretch")
    with right:
        row_err = float(np.max(np.abs(res["A"].sum(axis=1) - 1.0)))
        masked = res["A"][res["mask"]]
        manual = np.array([sum(res["A"][i, j] * res["V"][j] for j in range(len(cfg["tokens"]))) for i in range(len(cfg["tokens"]))])
        st.metric("max |row sum − 1|", f"{row_err:.1e}")
        st.metric("Masked (future) weights", f"{masked.size} cells, max = {masked.max() if masked.size else 0:.1f}")
        st.metric("Mean row entropy (nats)", f"{entropy_rows(res['A']).mean():.3f}", help=f"Uniform over {len(cfg['tokens'])} tokens would be ln n = {np.log(len(cfg['tokens'])):.3f}")
        checks_ok = row_err < 1e-12 and (masked.size == 0 or masked.max() == 0.0) and np.allclose(manual, res["H"]) and np.all(res["A"] >= 0)
        if checks_ok:
            st.success("✓ Rows sum to 1, all weights ≥ 0, masked cells are exactly 0, and A·V equals the explicit weighted sums.")
        else:
            st.error("A numerical check failed.")
        out = cfg["x"] + res["H"] @ p["Wo"]
        st.markdown(r"**Residual + output:** $\;Y = X + (AV)\,W_O$, shape " + f"{out.shape[0]} × {out.shape[1]}")
        st.dataframe(pd.DataFrame({"‖x‖": np.linalg.norm(cfg["x"], axis=1), "‖AV·W_O‖": np.linalg.norm(res["H"] @ p["Wo"], axis=1), "‖y‖": np.linalg.norm(out, axis=1)}, index=cfg["labels"]).round(3), width="stretch")
    st.caption(
        "Try: causal mask → the upper triangle turns to 0 and token 0 can only attend to itself. Low T → rows become one-hot (argmax); "
        "high T → rows approach uniform 1/n. The two copies of 'the' differ only through the positional encoding — switch it off and their rows become identical."
    )
    return res


def lab_scaling():
    st.subheader("Why divide by √d_k?")
    st.markdown(
        r"If the components of $q$ and $k$ are independent with mean 0 and variance 1, each product $q_ik_i$ has variance "
        r"$\mathbb E[q_i^2]\,\mathbb E[k_i^2] = 1$, and the $d_k$ products are independent, so"
    )
    st.latex(r"\operatorname{Var}(q\cdot k) = \sum_{i=1}^{d_k}\operatorname{Var}(q_i k_i) = d_k \quad\Longrightarrow\quad \operatorname{Var}\!\left(\frac{q\cdot k}{\sqrt{d_k}}\right) = 1")
    e = st.slider("d_k = 2^e  (choose e)", 1, 9, 6, key="p98_dexp")
    d_sel = 2 ** e
    rng = np.random.default_rng(0)
    ds = 2 ** np.arange(1, 10)
    rows = []
    n_keys, n_q = 8, 400
    for d in ds:
        q = rng.normal(size=(n_q, d))
        k = rng.normal(size=(n_q, n_keys, d))
        dots = np.einsum("nd,nkd->nk", q, k)
        p_raw, p_sc = softmax(dots, axis=-1), softmax(dots / np.sqrt(d), axis=-1)
        rows.append(dict(d=int(d), var=dots.var(), var_scaled=(dots / np.sqrt(d)).var(), max_raw=p_raw.max(axis=1).mean(), max_scaled=p_sc.max(axis=1).mean(), example_raw=p_raw[0], example_scaled=p_sc[0]))
    df = pd.DataFrame(rows)
    left, right = st.columns(2)
    with left:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["d"], y=df["var"], mode="markers+lines", name="Var(q·k) — measured", line=dict(color="#f59e0b")))
        fig.add_trace(go.Scatter(x=df["d"], y=df["d"], mode="lines", name="theory: d_k", line=dict(dash="dot", color="#e2e8f0")))
        fig.add_trace(go.Scatter(x=df["d"], y=df["var_scaled"], mode="markers+lines", name="Var(q·k/√d_k) — measured", line=dict(color="#22d3ee")))
        fig.update_layout(title=f"Variance check ({n_q * n_keys} random pairs per d)", xaxis_type="log", yaxis_type="log", xaxis_title="d_k", height=380, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig, width="stretch")
    with right:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=df["d"], y=df["max_raw"], mode="markers+lines", name="unscaled", line=dict(color="#f59e0b")))
        fig2.add_trace(go.Scatter(x=df["d"], y=df["max_scaled"], mode="markers+lines", name="scaled by 1/√d_k", line=dict(color="#22d3ee")))
        fig2.add_hline(y=1 / n_keys, line_dash="dot", annotation_text="uniform 1/8")
        fig2.update_layout(title=f"Average largest softmax weight over {n_keys} keys", xaxis_type="log", xaxis_title="d_k", yaxis=dict(range=[0, 1.05]), height=380, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig2, width="stretch")
    sel = df[df["d"] == d_sel].iloc[0]
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=[f"k{j}" for j in range(n_keys)], y=sel["example_raw"], name="softmax(q·k)", marker_color="#f59e0b"))
    fig3.add_trace(go.Bar(x=[f"k{j}" for j in range(n_keys)], y=sel["example_scaled"], name="softmax(q·k/√d_k)", marker_color="#22d3ee"))
    fig3.update_layout(barmode="group", title=f"One query vs {n_keys} keys at d_k = {d_sel}", yaxis=dict(range=[0, 1.05]), height=320, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig3, width="stretch")
    m1, m2 = st.columns(2)
    m1.metric(f"Measured Var(q·k) at d_k = {d_sel}", f"{sel['var']:.1f}", f"theory {d_sel}", delta_color="off")
    m2.metric("Measured Var after scaling", f"{sel['var_scaled']:.2f}", "theory 1", delta_color="off")
    st.info(
        "Without scaling, the logits' spread grows like √d_k, so softmax **saturates**: one weight → 1, the rest → 0. "
        "Saturated softmax has near-zero gradients for the losing keys, so training stalls. Dividing by √d_k keeps the logits at unit scale for any head size."
    )


def lab_heads(cfg):
    st.subheader("Multi-head attention — two heads, two patterns")
    dh = cfg["d_model"] // 2
    st.markdown(f"Each head projects to its own d_head = d_model / 2 = **{dh}** dimensions with its own $W_Q, W_K, W_V$, so it can attend by a different criterion.")
    results = [attention(cfg["x"], h["Wq"], h["Wk"], h["Wv"], cfg["scale"], cfg["causal"], cfg["temp"]) for h in cfg["heads"]]
    cols = st.columns(2)
    for idx, (col, res) in enumerate(zip(cols, results)):
        col.plotly_chart(attention_heatmap(res["A"], cfg["labels"], f"Head {idx + 1}", height=380), width="stretch")
    a1, a2 = results[0]["A"], results[1]["A"]
    concat = np.hstack([r["H"] for r in results])
    out = cfg["x"] + concat @ cfg["wo_multi"]
    m1, m2, m3 = st.columns(3)
    m1.metric("Mean |A₁ − A₂| per cell", f"{np.abs(a1 - a2).mean():.3f}")
    m2.metric("Queries whose top key differs", f"{int(np.sum(a1.argmax(1) != a2.argmax(1)))} / {len(cfg['tokens'])}")
    m3.metric("Output shape after concat · W_O + residual", f"{out.shape[0]} × {out.shape[1]}")
    st.latex(rf"\text{{MultiHead}}(X) = \big[\,A_1V_1 \;\big|\; A_2V_2\,\big]\,W_O,\qquad ({len(cfg['tokens'])}\times{dh}\ \big|\ {len(cfg['tokens'])}\times{dh}) \to {len(cfg['tokens'])}\times{2 * dh} \to {len(cfg['tokens'])}\times{cfg['d_model']}")
    st.caption("Heads here have random (seeded) weights; in trained models heads specialise — previous-token heads, induction heads, heads tracking syntax or coreference.")


def lab_cost():
    st.subheader("Cost: the n × n score matrix, and the KV cache")
    c1, c2 = st.columns(2)
    e = c1.slider("Sequence length n = 2^e", 7, 17, 12, key="p98_nexp")
    n = 2 ** e
    d_model, heads, layers = 4096, 32, 32
    c2.markdown(f"Model shape (Llama-2-7B-like): d_model = {d_model}, {heads} heads, {layers} layers, fp16.")
    score_bytes = n * n * heads * 2
    flops = 4 * n * n * d_model * layers  # QKᵀ and A·V: 2·n²·d each, per layer
    kv_bytes = 2 * n * d_model * layers * 2
    m1, m2, m3 = st.columns(3)
    m1.metric(f"Score matrices, 1 layer (n = {n:,})", f"{score_bytes / 2**30:,.2f} GiB")
    m2.metric("Attention FLOPs (all layers)", f"{flops:.2e}")
    m3.metric("KV cache for n tokens", f"{kv_bytes / 2**30:,.2f} GiB")
    ns = 2 ** np.arange(7, 18)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ns, y=ns * ns * heads * 2 / 2**30, mode="lines+markers", name="score matrix O(n²)", line=dict(color="#f472b6")))
    fig.add_trace(go.Scatter(x=ns, y=2 * ns * d_model * layers * 2 / 2**30, mode="lines+markers", name="KV cache O(n)", line=dict(color="#22d3ee")))
    fig.add_vline(x=n, line_dash="dot", line_color="#f59e0b")
    fig.update_layout(xaxis_type="log", yaxis_type="log", xaxis_title="n tokens", yaxis_title="GiB", height=360, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig, width="stretch")
    st.markdown(
        "Doubling n **quadruples** the score matrix. During generation the model caches every past token's **K and V** (the *KV cache*), "
        "so each new token computes only its own query and one row of scores — O(n·d) per step instead of recomputing O(n²·d). "
        "FlashAttention avoids storing the n × n matrix at all by computing softmax in tiles."
    )


def worked_example(cfg, res):
    st.header("🧮 Worked example — one query, step by step")
    n = len(cfg["tokens"])
    st.session_state.setdefault("p98_query", n - 1)
    st.session_state["p98_query"] = min(st.session_state["p98_query"], n - 1)
    i = st.selectbox("Query token", list(range(n)), format_func=lambda j: cfg["labels"][j], key="p98_query")
    denom = np.sqrt(res["d_k"]) if cfg["scale"] else 1.0
    df = pd.DataFrame(
        {
            "① raw q·k": res["raw"][i],
            f"② ÷ {fmt_num(denom)}{' (√d_k)' if cfg['scale'] else ''} ÷ T={fmt_num(cfg['temp'], 1)}": np.where(res["mask"][i], np.nan, res["scaled"][i] / cfg["temp"]),
            "masked?": np.where(res["mask"][i], "−∞ (future)", ""),
            "③ softmax weight": res["A"][i],
        },
        index=cfg["labels"],
    )
    st.dataframe(df.round(4), width="stretch")
    j = int(np.argmax(res["A"][i]))
    q, k = res["Q"][i], res["K"][j]
    terms = " + ".join(f"{fmt_factor(a)}\\cdot{fmt_factor(b)}" for a, b in zip(q[:4], k[:4]))
    more = r" + \dots" if len(q) > 4 else ""
    st.latex(rf"q_{{{i}}}\cdot k_{{{j}}} = {terms}{more} = {fmt_num(res['raw'][i, j], 3)}")
    st.latex(rf"\frac{{{fmt_num(res['raw'][i, j], 3)}}}{{{fmt_num(denom, 3)}\times{fmt_num(cfg['temp'], 1)}}} = {fmt_num(res['logits'][i, j], 3)}")
    finite = ~res["mask"][i]
    logits = res["logits"][i][finite]
    z = np.exp(logits - logits.max())
    st.latex(rf"a_{{{i}{j}}} = \frac{{e^{{{fmt_num(res['logits'][i, j], 3)} - {fmt_num(logits.max(), 3)}}}}}{{\sum_{{j' \le \text{{allowed}}}} e^{{\ell_{{{i}j'}} - \max}}}} = \frac{{{fmt_num(np.exp(res['logits'][i, j] - logits.max()), 4)}}}{{{fmt_num(z.sum(), 4)}}} = {fmt_num(res['A'][i, j], 4)}")
    st.markdown(f"④ **Weighted sum of value rows** — output for '{cfg['tokens'][i]}' = Σⱼ aᵢⱼ vⱼ:")
    contrib = res["A"][i][:, None] * res["V"]
    vdf = pd.DataFrame(contrib, index=[f"{a:.3f} × v[{lab}]" for a, lab in zip(res["A"][i], cfg["labels"])], columns=[f"dim {c}" for c in range(contrib.shape[1])])
    vdf.loc["= output (sum)"] = contrib.sum(axis=0)
    st.dataframe(vdf.round(3), width="stretch")
    if np.allclose(contrib.sum(axis=0), res["H"][i]):
        st.success(f"✓ Matches row {i} of A·V. Weights sum to {res['A'][i].sum():.6f}.")


def ai_connection():
    st.header("🤖 Where this shows up in real models")
    st.markdown(
        r"""
- **Transformers / LLMs**: every layer of GPT, Llama and Mistral models runs multi-head attention (dozens of heads,
  d_head = 64–128) followed by an MLP, each wrapped in a residual connection — exactly the $X + \text{Attn}(X)W_O$ above.
- **Causal masking** makes decoder LLMs autoregressive: token *i* may only see tokens ≤ *i*, so training can predict
  every next token in parallel without cheating.
- **KV cache**: at inference the keys/values of past tokens are stored, which is why long contexts need lots of GPU
  memory; grouped-query attention (GQA) shares K/V across heads to shrink it.
- **Temperature** in attention is the same idea as sampling temperature (page 37); the √d_k factor is a fixed temperature chosen for stable training.
- **Caveat — attention ≠ explanation**: a large weight says where information was *read from* in one head of one layer,
  not why the model decided. Values, W_O, residual paths, MLPs and other heads all mix the signal, so attention maps
  are suggestive, not faithful explanations.
"""
    )


def takeaways():
    st.header("✅ Key takeaways")
    st.markdown(
        r"""
1. Attention = $\operatorname{softmax}(QK^\top/\sqrt{d_k})\,V$: dot-product scores → probabilities → weighted average of values.
2. Each row of the weight matrix is a probability distribution (non-negative, sums to 1).
3. $\operatorname{Var}(q\cdot k) = d_k$ for unit-variance components, so scaling by $\sqrt{d_k}$ prevents softmax saturation.
4. A causal mask sets future scores to $-\infty$ so their weights are exactly 0.
5. Multiple heads attend by different criteria; their outputs are concatenated and mixed by $W_O$, then added to the residual stream.
6. Cost grows as $O(n^2)$ in sequence length; the KV cache makes generation $O(n)$ per new token.
"""
    )
    c1, c2 = st.columns(2)
    with c1:
        safe_page_link("pages/97Embeddings.py", "Previous: 97 · Embeddings", "⬅️")
    with c2:
        safe_page_link("pages/67Neural Network as Matrix Layers.py", "Revisit: 67 · Neural Network as Matrix Layers", "🔁")


def main():
    st.session_state.setdefault("p98_seed", 0)
    intuition()
    st.header("🔬 Interactive labs")
    cfg = controls()
    tabs = st.tabs(["Attention map", "Why √d_k", "Two heads", "Cost & KV cache"])
    with tabs[0]:
        res = lab_map(cfg)
    with tabs[1]:
        lab_scaling()
    with tabs[2]:
        lab_heads(cfg)
    with tabs[3]:
        lab_cost()
    worked_example(cfg, res)
    ai_connection()
    takeaways()


main()
