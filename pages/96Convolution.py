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
from common.mathutils import fmt_factor, fmt_num  # noqa: E402

st.set_page_config(page_title="96 · Convolution", page_icon="🧩", layout="wide")

N_SIGNAL = 16
IMG = 16

KERNELS_1D = {
    "Smoothing — box [1, 1, 1]/3": np.full(3, 1 / 3),
    "Smoothing — box [1, 1, 1, 1, 1]/5": np.full(5, 0.2),
    "Smoothing — Gaussian-like [1, 2, 1]/4": np.array([1.0, 2.0, 1.0]) / 4,
    "Edge — difference [−1, 1]": np.array([-1.0, 1.0]),
    "Edge — central difference [−1, 0, 1]/2": np.array([-0.5, 0.0, 0.5]),
    "Spike detector [−1, 2, −1]": np.array([-1.0, 2.0, -1.0]),
}

KERNELS_2D = {
    "Identity": np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=float),
    "Box blur": np.full((3, 3), 1 / 9),
    "Gaussian blur": np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]], dtype=float) / 16,
    "Sharpen": np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=float),
    "Sobel x (vertical edges)": np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float),
    "Sobel y (horizontal edges)": np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=float),
    "Edge (Laplacian 8-neighbour)": np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], dtype=float),
}
FEATURE_MAP_KERNELS = ["Gaussian blur", "Sharpen", "Sobel x (vertical edges)", "Sobel y (horizontal edges)", "Edge (Laplacian 8-neighbour)"]


# ---------------------------------------------------------------- maths helpers
def output_length(n, k, pad, stride):
    """⌊(n + 2p − k)/s⌋ + 1, or 0 when the kernel does not fit even once."""
    if n + 2 * pad < k:
        return 0
    return (n + 2 * pad - k) // stride + 1


def correlate1d(x, k, pad, stride):
    """Deep-learning 'convolution' (cross-correlation): slide k over the zero-padded x, no flip."""
    xp = np.pad(np.asarray(x, dtype=float), pad)
    starts = list(range(0, len(xp) - len(k) + 1, stride))
    out = np.array([xp[s:s + len(k)] @ k for s in starts]) if starts else np.zeros(0)
    return out, xp, starts


def correlate2d_same(img, kernel):
    """3×3 (odd k) cross-correlation with zero 'same' padding, stride 1."""
    p = kernel.shape[0] // 2
    padded = np.pad(img, p)
    windows = np.lib.stride_tricks.sliding_window_view(padded, kernel.shape)
    return np.einsum("ijkl,kl->ij", windows, kernel), padded


def receptive_field(layers, k, stride):
    """Closed form r_L = r_{L-1} + (k − 1)·J_{L-1}, J_L = J_{L-1}·s, plus a brute-force check."""
    r, jump = 1, 1
    for _ in range(layers):
        r += (k - 1) * jump
        jump *= stride
    idx = {0}  # one output unit; walk back down to the input
    for _ in range(layers):
        idx = {i * stride + j for i in idx for j in range(k)}
    return r, max(idx) - min(idx) + 1


def make_signal(name, seed):
    t = np.arange(N_SIGNAL)
    if name == "Noisy step":
        rng = np.random.default_rng(seed)
        return np.where(t >= N_SIGNAL // 2, 1.0, 0.0) + rng.normal(0.0, 0.15, N_SIGNAL)
    if name == "Sine wave":
        return np.sin(2 * np.pi * t / 8)
    x = np.linspace(0.0, 1.0, N_SIGNAL)
    x[4] += 1.0
    return x


def make_image(name):
    if name.startswith("Digit"):
        try:
            from sklearn.datasets import load_digits

            digit = load_digits().images[3] / 16.0  # the 8×8 "3"
            return np.kron(digit, np.ones((2, 2)))  # upscale to 16×16
        except Exception:
            pass  # fall back to the synthetic shapes below
    yy, xx = np.mgrid[0:IMG, 0:IMG]
    img = np.zeros((IMG, IMG))
    img[2:7, 2:7] = 1.0  # square
    img[(yy - 10.5) ** 2 + (xx - 10.5) ** 2 <= 3.2 ** 2] = 0.7  # disk
    rows = np.arange(7)
    img[rows, 15 - rows] = 1.0  # diagonal line
    img[12:14, 1:7] = 0.5  # horizontal bar
    return img


def heatmap(z, title, colorscale="gray", zmid=None, zmin=None, zmax=None, rect=None, marker=None, height=360):
    fig = go.Figure(go.Heatmap(z=z, colorscale=colorscale, zmid=zmid, zmin=zmin, zmax=zmax, colorbar=dict(thickness=10)))
    if rect is not None:
        r, c, half = rect
        fig.add_shape(type="rect", x0=c - half - 0.5, x1=c + half + 0.5, y0=r - half - 0.5, y1=r + half + 0.5, line=dict(color="#f59e0b", width=3))
    if marker is not None:
        fig.add_shape(type="rect", x0=marker[1] - 0.5, x1=marker[1] + 0.5, y0=marker[0] - 0.5, y1=marker[0] + 0.5, line=dict(color="#22d3ee", width=3))
    fig.update_yaxes(autorange="reversed", scaleanchor="x", constrain="domain")
    fig.update_xaxes(constrain="domain")
    fig.update_layout(title=title, height=height, margin=dict(l=10, r=10, t=40, b=10))
    return fig


# ---------------------------------------------------------------- page sections
def intuition():
    st.title("🧩 Convolution — One Small Filter, Slid Everywhere")
    st.markdown(
        r"""
A **convolution layer** takes a tiny set of weights — a *kernel* such as $[1, 2, 1]/4$ or a $3\times3$ grid —
and **slides it across the input**. At every position it computes the dot product of the kernel with the patch
underneath and writes one number into the output. The output is called a **feature map**: it lights up wherever
the input *looks like* the kernel (a blur, an edge, a spike…).

Why this matters for AI: images, audio and text have **local structure** (nearby pixels / samples belong together)
and **translation symmetry** (a cat is a cat in the top-left or the bottom-right). Re-using the *same* small kernel
everywhere bakes both facts into the network — far fewer parameters than a dense layer, and a detector that works at
every location.
"""
    )
    st.info(
        r"**Naming trap:** what deep-learning libraries call *convolution* is mathematically **cross-correlation** — "
        r"the kernel is **not flipped**. True convolution flips it first: $(x * k)[i] = \sum_j x[i-j]\,k[j]$. "
        r"Because kernels are *learned*, the network would simply learn the flipped version, so nobody bothers. "
        r"This page uses the deep-learning convention throughout and verifies the flip relation numerically."
    )


def lab_1d():
    st.subheader("1D sliding window — step through the output")
    c1, c2, c3 = st.columns(3)
    sig_name = c1.selectbox("Signal", ["Noisy step", "Sine wave", "Spike + ramp"], key="p96_signal")
    ker_name = c2.selectbox("Kernel", list(KERNELS_1D), key="p96_kernel1d")
    with c3:
        st.write("")
        if st.button("🎲 Resample noise", key="p96_resample"):
            st.session_state["p96_seed"] = st.session_state["p96_seed"] + 1
    k = KERNELS_1D[ker_name]
    x = make_signal(sig_name, st.session_state["p96_seed"])

    c4, c5 = st.columns(2)
    pad = c4.slider("Padding p (zeros on each side)", 0, 3, 0, key="p96_pad")
    stride = c5.slider("Stride s", 1, 3, 1, key="p96_stride")
    out, xp, starts = correlate1d(x, k, pad, stride)
    n_out = output_length(N_SIGNAL, len(k), pad, stride)

    # Keep the step slider inside the (possibly shrunken) output range.
    st.session_state.setdefault("p96_pos", 0)
    st.session_state["p96_pos"] = min(st.session_state["p96_pos"], max(n_out - 1, 0))
    i = st.slider("Output position i (move the window)", 0, max(n_out - 1, 1), key="p96_pos")
    i = min(i, n_out - 1)
    s0 = starts[i]
    window = xp[s0:s0 + len(k)]

    pos = np.arange(len(xp)) - pad  # padded index → original coordinate
    centres = np.array(starts) - pad + (len(k) - 1) / 2
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.12,
                        subplot_titles=("Input x (hollow = zero padding)", "Output y = x ⋆ k (plotted at window centre)"))
    is_pad = (pos < 0) | (pos >= N_SIGNAL)
    fig.add_trace(go.Scatter(x=pos[~is_pad], y=xp[~is_pad], mode="lines+markers", name="x", line=dict(color="#38bdf8")), row=1, col=1)
    fig.add_trace(go.Scatter(x=pos[is_pad], y=xp[is_pad], mode="markers", name="padding", marker=dict(symbol="circle-open", size=10, color="#94a3b8")), row=1, col=1)
    fig.add_vrect(x0=s0 - pad - 0.5, x1=s0 - pad + len(k) - 0.5, fillcolor="#f59e0b", opacity=0.25, line_width=0, row=1, col=1)
    fig.add_trace(go.Scatter(x=centres, y=out, mode="lines+markers", name="y", line=dict(color="#a78bfa")), row=2, col=1)
    fig.add_trace(go.Scatter(x=[centres[i]], y=[out[i]], mode="markers", name=f"y[{i}]", marker=dict(size=16, color="#f59e0b", symbol="diamond")), row=2, col=1)
    fig.update_layout(height=480, margin=dict(l=10, r=10, t=40, b=10), legend=dict(orientation="h", y=-0.08))
    st.plotly_chart(fig, width="stretch")

    terms = " + ".join(f"{fmt_factor(w)}\\cdot{fmt_factor(v)}" for w, v in zip(k, window))
    st.latex(rf"y[{i}] = \sum_{{j=0}}^{{{len(k) - 1}}} k_j\,\tilde x[{i}\cdot{stride} + j] = {terms} = {fmt_num(out[i], 3)}")
    st.caption(r"$\tilde x$ is the zero-padded signal; the window starts at padded index $i\cdot s$ = " + str(s0) + ".")

    m1, m2, m3 = st.columns(3)
    m1.metric("Formula ⌊(n + 2p − k)/s⌋ + 1", n_out)
    m2.metric("Windows actually slid", len(out))
    m3.metric("Signal n / kernel k", f"{N_SIGNAL} / {len(k)}")
    st.latex(rf"\left\lfloor \frac{{n + 2p - k}}{{s}} \right\rfloor + 1 = \left\lfloor \frac{{{N_SIGNAL} + 2\cdot{pad} - {len(k)}}}{{{stride}}} \right\rfloor + 1 = {n_out}")
    if n_out == len(out):
        st.success("✓ The output-length formula matches the number of window positions counted by the loop.")
    else:
        st.error("Output length mismatch — this should never happen.")

    # Verify against numpy: correlate(x, k) == convolve(x, flip(k)) for p = 0, s = 1.
    ours, _, _ = correlate1d(x, k, 0, 1)
    ref_corr = np.correlate(x, k, mode="valid")
    ref_conv = np.convolve(x, k[::-1], mode="valid")
    err = max(np.max(np.abs(ours - ref_corr)), np.max(np.abs(ours - ref_conv)))
    st.caption(f"Check (p = 0, s = 1): our sliding window vs `np.correlate(x, k)` and `np.convolve(x, flip(k))` — max |difference| = {err:.1e}.")


def kernel_editor():
    """Preset selectbox that writes into nine editable number inputs."""

    def load_preset():
        kern = KERNELS_2D[st.session_state["p96_preset"]]
        for a in range(3):
            for b in range(3):
                st.session_state[f"p96_k{a}{b}"] = float(round(kern[a, b], 4))

    st.session_state.setdefault("p96_preset", "Sobel x (vertical edges)")
    if "p96_k00" not in st.session_state:
        load_preset()
    st.selectbox("Kernel preset (loads into the grid below — then edit freely)", list(KERNELS_2D), key="p96_preset", on_change=load_preset)
    kern = np.zeros((3, 3))
    for a in range(3):
        cols = st.columns(3)
        for b in range(3):
            kern[a, b] = cols[b].number_input(f"k[{a},{b}]", min_value=-10.0, max_value=10.0, step=0.1, format="%.4f", key=f"p96_k{a}{b}")
    if not np.allclose(kern, KERNELS_2D[st.session_state["p96_preset"]], atol=1e-4):
        st.caption("✏️ Kernel edited — it no longer equals the preset.")
    return kern


def lab_2d():
    st.subheader("2D convolution on a small image")
    left, right = st.columns([1, 2])
    with left:
        img_name = st.selectbox("Image (16×16)", ["Shapes (square, disk, line, bar)", "Digit 3 (sklearn 8×8, upscaled)"], key="p96_image")
        kern = kernel_editor()
        r = st.slider("Output row", 0, IMG - 1, 4, key="p96_row")
        c = st.slider("Output column", 0, IMG - 1, 2, key="p96_col")
    img = make_image(img_name)
    out, padded = correlate2d_same(img, kern)
    with right:
        a, b = st.columns(2)
        a.plotly_chart(heatmap(img, "Input (orange = 3×3 patch)", zmin=0, zmax=1, rect=(r, c, 1)), width="stretch")
        b.plotly_chart(heatmap(out, f"Feature map (cyan = output [{r},{c}])", colorscale="RdBu", zmid=0, marker=(r, c)), width="stretch")
        try:
            from scipy.signal import convolve2d, correlate2d

            err = max(np.max(np.abs(out - correlate2d(img, kern, mode="same"))), np.max(np.abs(out - convolve2d(img, kern[::-1, ::-1], mode="same"))))
            st.caption(f"Check: matches `scipy.signal.correlate2d(img, k)` and `convolve2d(img, flip(k))` — max |difference| = {err:.1e}.")
        except ImportError:
            st.caption("scipy not available — skipped the reference check.")

    st.markdown("**Feature maps** — the same image through several fixed kernels (a CNN layer learns dozens of these, one output channel each):")
    relu = st.toggle("Apply ReLU (keep only positive responses)", value=False, key="p96_relu")
    fig = make_subplots(rows=1, cols=len(FEATURE_MAP_KERNELS), subplot_titles=[n.split(" (")[0] for n in FEATURE_MAP_KERNELS], horizontal_spacing=0.02)
    for idx, name in enumerate(FEATURE_MAP_KERNELS):
        fmap, _ = correlate2d_same(img, KERNELS_2D[name])
        if relu:
            fmap = np.maximum(fmap, 0.0)
        fig.add_trace(go.Heatmap(z=fmap, colorscale="RdBu", zmid=0, showscale=False), row=1, col=idx + 1)
    fig.update_yaxes(autorange="reversed", showticklabels=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_layout(height=260, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, width="stretch")
    st.caption("Sobel x fires on vertical edges (left↔right brightness change), Sobel y on horizontal edges; the sign tells the direction of the change.")
    return img, kern, padded, out, r, c


def lab_sharing():
    st.subheader("Parameter sharing — conv layer vs dense layer")
    c1, c2, c3, c4 = st.columns(4)
    h = c1.slider("Image side H = W", 4, 224, 32, key="p96_h")
    cin = c2.slider("Input channels", 1, 64, 3, key="p96_cin")
    cout = c3.slider("Output channels", 1, 128, 16, key="p96_cout")
    k = c4.slider("Kernel size k", 1, 7, 3, step=2, key="p96_ksize")
    conv = k * k * cin * cout + cout
    dense = (h * h * cin) * (h * h * cout) + h * h * cout
    m1, m2, m3 = st.columns(3)
    m1.metric("Conv parameters  k²·Cin·Cout + Cout", f"{conv:,}")
    m2.metric("Dense parameters (same in/out size)", f"{dense:,}")
    m3.metric("Dense / conv", f"{dense / conv:,.0f}×")
    st.caption(f"Each conv weight is reused at all {h * h:,} positions ('same' padding, stride 1) — that reuse is *parameter sharing*.")

    st.subheader("Receptive field — stacking layers sees further")
    d1, d2, d3 = st.columns(3)
    layers = d1.slider("Stacked conv layers", 1, 12, 3, key="p96_layers")
    rk = d2.slider("Kernel size per layer", 2, 7, 3, key="p96_rf_k")
    rs = d3.radio("Stride per layer", [1, 2], horizontal=True, key="p96_rf_s")
    rf, rf_brute = receptive_field(layers, rk, rs)
    st.latex(r"r_\ell = r_{\ell-1} + (k-1)\,J_{\ell-1},\quad J_\ell = J_{\ell-1}\, s,\quad r_0 = J_0 = 1")
    e1, e2 = st.columns(2)
    e1.metric(f"Receptive field after {layers} layer(s) (formula)", rf)
    e2.metric("Brute force: input indices reaching one output", rf_brute)
    if rf == rf_brute:
        st.success("✓ Formula and brute-force index tracing agree.")
    depth = np.arange(1, 13)
    fig = go.Figure()
    for s, colour in ((1, "#38bdf8"), (2, "#f59e0b")):
        fig.add_trace(go.Scatter(x=depth, y=[receptive_field(int(d), rk, s)[0] for d in depth], mode="lines+markers", name=f"stride {s}", line=dict(color=colour)))
    fig.add_trace(go.Scatter(x=[layers], y=[rf], mode="markers", marker=dict(size=16, color="#f472b6", symbol="star"), name="your setting"))
    fig.update_layout(height=340, xaxis_title="layers", yaxis_title="receptive field (input samples)", yaxis_type="log", margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig, width="stretch")
    st.caption("Stride 1: grows linearly, L·(k−1)+1. Stride 2 (or pooling): the jump doubles each layer, so the field grows exponentially.")


def worked_example(img, kern, padded, out, r, c):
    st.header("🧮 Worked example — one output pixel by hand")
    patch = padded[r:r + 3, c:c + 3]
    prod = patch * kern
    st.markdown(f"Output location **[{r}, {c}]** (row/column sliders above). The 3×3 patch is centred on input pixel [{r}, {c}]; cells outside the image are zero padding.")
    cols = st.columns(3)
    for col, (name, mat) in zip(cols, (("Input patch", patch), ("Kernel k", kern), ("Patch ⊙ kernel", prod))):
        col.markdown(f"**{name}**")
        col.dataframe(pd.DataFrame(mat).round(3), width="stretch")
    terms = " + ".join(fmt_factor(v, 3) + r"\cdot" + fmt_factor(w, 3) for v, w in zip(patch.ravel(), kern.ravel()))
    st.latex(rf"y[{r},{c}] = \sum_{{a,b}} x_{{\text{{patch}}}}[a,b]\,k[a,b] = {terms}")
    st.latex(rf"y[{r},{c}] = {fmt_num(prod.sum(), 4)}")
    flipped = float(np.sum(patch * kern[::-1, ::-1]))
    if np.isclose(prod.sum(), out[r, c]):
        st.success(f"✓ Matches the feature map value {fmt_num(out[r, c], 4)}.")
    st.markdown(
        rf"A **true (flipped) convolution** at the same spot would use $k$ rotated by 180°, giving **{fmt_num(flipped, 4)}** "
        + ("— identical here because this kernel is symmetric under the flip." if np.allclose(kern, kern[::-1, ::-1]) else "— different, because this kernel is not symmetric (e.g. Sobel changes sign).")
    )


def ai_connection():
    st.header("🤖 Where this shows up in real models")
    st.markdown(
        """
- **CNNs for vision** (LeNet → AlexNet → ResNet → ConvNeXt): stacks of learned 3×3 kernels; early layers learn
  edge/blob detectors that look a lot like the Sobel and blur kernels above, deeper layers combine them into textures,
  parts and objects as the receptive field grows.
- **1D convolutions on audio and sequences**: WaveNet uses dilated causal 1D convs over raw audio samples; speech
  models such as wav2vec 2.0 and Whisper run a 1D conv front-end over waveforms / spectrograms before the transformer.
- **Conv stems in Vision Transformers**: ViT's "patchify" step is literally a convolution with kernel = stride = 16,
  turning a 224×224 image into 14×14 = 196 patch tokens; hybrid models put a small CNN stem in front for better
  low-level features.
- **Efficiency**: parameter sharing is why a ResNet-50 has ~25 M parameters instead of the trillions a dense layer
  on full-resolution images would need.
"""
    )


def takeaways():
    st.header("✅ Key takeaways")
    st.markdown(
        r"""
1. A conv layer slides one small kernel over the input and takes a dot product at every position → a feature map.
2. Output length: $\lfloor (n + 2p - k)/s \rfloor + 1$ — padding keeps size, stride shrinks it.
3. Deep-learning "convolution" is cross-correlation (no kernel flip); for learned kernels the difference is irrelevant.
4. Parameter sharing: $k^2 C_{in} C_{out} + C_{out}$ weights, independent of the image size.
5. Stacking layers grows the receptive field — linearly with stride 1, exponentially with stride 2 / pooling.
"""
    )
    c1, c2 = st.columns(2)
    with c1:
        safe_page_link("pages/95Batch Normalization.py", "Previous: 95 · Batch Normalization", "⬅️")
    with c2:
        safe_page_link("pages/97Embeddings.py", "Next: 97 · Embeddings", "➡️")


def main():
    st.session_state.setdefault("p96_seed", 0)
    intuition()
    st.header("🔬 Interactive labs")
    tab1, tab2, tab3 = st.tabs(["1D sliding window", "2D image filters", "Sharing & receptive field"])
    with tab1:
        lab_1d()
    with tab2:
        img, kern, padded, out, r, c = lab_2d()
    with tab3:
        lab_sharing()
    worked_example(img, kern, padded, out, r, c)
    ai_connection()
    takeaways()


main()
