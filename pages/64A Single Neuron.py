import math
import sys
from pathlib import Path

import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from common.assets import load_lab  # noqa: E402
from common.mathutils import sigmoid  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="A Single Neuron", layout="wide")


def render_neuron_lab():
    html_code = load_lab("p64_neuron")
    st.iframe(html_code, height="content")


# ---------------------------------------------------------------------------
# Case study (merged from the former "64A Single Neuron2" page): a cat detector
# ---------------------------------------------------------------------------
CAT_FEATURES = ("📐 Ear pointiness (x₁)", "🐱 Whisker length (x₂)", "🔊 Barking volume (x₃)")
CAT_ACTIVATIONS = ("Sigmoid", "Binary Step", "ReLU", "Tanh")

CAT_ANIMALS = {
    "🐱 Siamese Cat": {
        "x": (1.0, 1.0, 0.0),
        "is_cat": True,
        "desc": "Pointy ears, long whiskers, no barking — a textbook cat.",
    },
    "🐶 Golden Retriever": {
        "x": (0.1, 0.2, 1.0),
        "is_cat": False,
        "desc": "Floppy ears, barely any whiskers, loud bark. Should NOT trigger the detector.",
    },
    "🐰 Fluffy Bunny": {
        "x": (1.0, 0.9, 0.0),
        "is_cat": False,
        "desc": "Pointy ears, long whiskers, silent — on these three features it looks almost exactly like a cat.",
    },
    "🦁 Majestic Lion": {
        "x": (0.8, 1.0, 0.0),
        "is_cat": True,
        "desc": "A big cat: slightly rounder ears, great whiskers, no barking. Should fire.",
    },
    "🤖 Robo-Dog": {
        "x": (0.9, 0.1, 0.8),
        "is_cat": False,
        "desc": "Pointy metal ears, but it barks — the negative barking weight should shut it down.",
    },
}

CAT_DESIGNS = {
    "start": {"label": "① Starting design", "w": (4.0, 5.0, -8.0), "b": -3.0},
    "bias_only": {"label": "② Bias-only fix", "w": (4.0, 5.0, -8.0), "b": -8.7},
    "reweighted": {"label": "③ Re-weighted fix", "w": (0.0, 10.0, -8.0), "b": -9.5},
}


def _set_design(key):
    design = CAT_DESIGNS[key]
    for i, wi in enumerate(design["w"], start=1):
        st.session_state[f"p64_w{i}"] = wi
    st.session_state.p64_b = design["b"]


def _load_animal(name):
    """Full preset: the animal's features plus a reset to the starting neuron design."""
    for i, xi in enumerate(CAT_ANIMALS[name]["x"], start=1):
        st.session_state[f"p64_x{i}"] = xi
    _set_design("start")
    st.session_state.p64_act = "Sigmoid"


def _init_cat_state():
    if "p64_x1" not in st.session_state:
        _load_animal("🐱 Siamese Cat")
    for key, default in (
        ("p64_x2", 1.0), ("p64_x3", 0.0), ("p64_w1", 4.0), ("p64_w2", 5.0),
        ("p64_w3", -8.0), ("p64_b", -3.0), ("p64_act", "Sigmoid"),
    ):
        st.session_state.setdefault(key, default)
    if st.session_state.p64_act not in CAT_ACTIVATIONS:
        st.session_state.p64_act = "Sigmoid"


def neuron_forward(xs, ws, b, activation):
    z = sum(xi * wi for xi, wi in zip(xs, ws)) + b
    if activation == "Sigmoid":
        a = float(sigmoid(z))
    elif activation == "Binary Step":
        a = 1.0 if z >= 0 else 0.0
    elif activation == "ReLU":
        a = max(0.0, z)
    else:
        a = math.tanh(z)
    return z, a


ACT_FORMULA = {
    "Sigmoid": ("σ", "1 / (1 + e^(−z))", "probability-like (0–1) but NOT a calibrated confidence"),
    "Binary Step": ("step", "1 if z ≥ 0 else 0", "a hard 0/1 vote — the 1958 perceptron's rule"),
    "ReLU": ("ReLU", "max(0, z)", "an unbounded score ≥ 0, not a probability"),
    "Tanh": ("tanh", "(e^z − e^(−z)) / (e^z + e^(−z))", "a score between −1 and 1, not a probability"),
}


def render_cat_case_study():
    _init_cat_state()

    st.markdown(
        "Design a **cat-detector neuron** with three hand-made features. "
        "Each animal button is a *full preset*: it loads the animal's features **and** resets the neuron "
        "to the starting design (w = [4, 5, −8], b = −3, sigmoid) so results are reproducible. "
        "The design buttons then change only the weights and bias."
    )

    st.markdown("##### Step 1 — pick an animal")
    animal_cols = st.columns(len(CAT_ANIMALS))
    for idx, (name, info) in enumerate(CAT_ANIMALS.items()):
        with animal_cols[idx]:
            st.button(
                name, key=f"p64_animal_{idx}", help=info["desc"], width="stretch",
                on_click=_load_animal, args=(name,),
            )

    st.markdown("##### Step 2 — pick (or tweak) a neuron design")
    design_cols = st.columns(len(CAT_DESIGNS))
    for idx, (key, design) in enumerate(CAT_DESIGNS.items()):
        with design_cols[idx]:
            w_txt = ", ".join(f"{v:g}" for v in design["w"])
            st.button(
                design["label"], key=f"p64_design_{key}", width="stretch",
                help=f"w = [{w_txt}], b = {design['b']:g}",
                on_click=_set_design, args=(key,),
            )

    left, right = st.columns([1, 1.4], gap="large")
    with left:
        st.markdown("**Inputs (features)**")
        for i, label in enumerate(CAT_FEATURES, start=1):
            st.slider(label, 0.0, 1.0, step=0.05, key=f"p64_x{i}")
        st.markdown("**Weights and bias**")
        for i, label in enumerate(("w₁ on ears", "w₂ on whiskers", "w₃ on barking"), start=1):
            st.slider(label, -10.0, 10.0, step=0.5, key=f"p64_w{i}")
        st.slider("Bias b", -15.0, 15.0, step=0.1, key="p64_b")
        st.selectbox("Activation f", CAT_ACTIVATIONS, key="p64_act")

    xs = tuple(float(st.session_state[f"p64_x{i}"]) for i in (1, 2, 3))
    ws = tuple(float(st.session_state[f"p64_w{i}"]) for i in (1, 2, 3))
    b = float(st.session_state.p64_b)
    activation = st.session_state.p64_act
    z, a = neuron_forward(xs, ws, b, activation)
    fires = z >= 0
    symbol, formula, meaning = ACT_FORMULA[activation]
    matched = next(
        (n for n, info in CAT_ANIMALS.items() if all(abs(u - v) < 1e-6 for u, v in zip(xs, info["x"]))),
        None,
    )

    with right:
        st.markdown("**Step-by-step forward pass**")
        products = [xi * wi + 0.0 for xi, wi in zip(xs, ws)]  # + 0.0 turns -0.0 into 0.0
        breakdown = (
            "z = " + " + ".join(f"({xi:.2f})({wi:+.1f})" for xi, wi in zip(xs, ws)) + f" + ({b:+.1f})\n"
            "  = " + " ".join(f"{p:+.2f}" for p in products) + f" {b:+.2f}\n"
            f"  = {z:+.4f}\n\n"
            f"a = {symbol}(z) = {formula}\n"
            f"  = {a:.4f}\n\n"
            f"decision rule: z ≥ 0  →  {'FIRES (cat)' if fires else 'SILENT (not a cat)'}"
        )
        st.code(breakdown, language=None)
        st.caption(f"Output a is {meaning}. The decision on this page always uses z ≥ 0.")

        if matched is not None:
            truth = CAT_ANIMALS[matched]["is_cat"]
            correct = truth == fires
            verdict = (
                f"**{matched}** — neuron says **{'CAT' if fires else 'NOT A CAT'}**; "
                f"truth: **{'cat' if truth else 'not a cat'}** → {'✅ correct' if correct else '❌ wrong'}."
            )
            (st.success if correct else st.error)(verdict)
            st.caption(CAT_ANIMALS[matched]["desc"])
        else:
            st.info(f"Custom animal — neuron says **{'CAT' if fires else 'NOT A CAT'}**.")
        st.caption("This is a toy rule on three made-up features, not a validated real-world cat classifier.")

    st.markdown("#### 💡 Why bias alone can't fix the Bunny")
    start_w = CAT_DESIGNS["start"]["w"]
    ranking = sorted(
        ((sum(xi * wi for xi, wi in zip(info["x"], start_w)), name) for name, info in CAT_ANIMALS.items()),
        reverse=True,
    )
    rank_txt = " > ".join(f"{name} {score:+.1f}" for score, name in ranking)
    st.markdown(
        f"With the starting weights $\\mathbf{{w}} = (4, 5, -8)$ the dot products rank the animals as: {rank_txt}.\n\n"
        "The bias adds the **same** number to every animal, so it only slides the cut-off along this ranking — "
        "it can never reorder it. Because the Bunny (+8.5) scores *above* the Lion (+8.2), any bias that lets the "
        "Lion through ($b \\ge -8.2$) also lets the Bunny through, and any bias that rejects the Bunny "
        "($b < -8.5$, e.g. the bias-only fix $b = -8.7$) also rejects the Lion. "
        "To separate them we must change the **weights**: with $\\mathbf{w} = (0, 10, -8)$ only whiskers and barking matter, "
        "the Siamese and Lion score 10 and the Bunny 9, and $b = -9.5$ splits them."
    )

    designs = [(d["label"], d["w"], d["b"]) for d in CAT_DESIGNS.values()]
    designs.append(("Your sliders", ws, b))
    header = "| Animal | Truth | " + " | ".join(f"{lbl} (b = {bb:g})" for lbl, _, bb in designs) + " |"
    sep = "|---|---|" + "---|" * len(designs)
    rows = [header, sep]
    for name, info in CAT_ANIMALS.items():
        cells = []
        for _, dw, db in designs:
            zz = sum(xi * wi for xi, wi in zip(info["x"], dw)) + db
            ok = (zz >= 0) == info["is_cat"]
            cells.append(f"z = {zz:+.2f} {'✅' if ok else '❌'}")
        rows.append(f"| {name} | {'cat' if info['is_cat'] else 'not cat'} | " + " | ".join(cells) + " |")
    st.markdown("\n".join(rows))
    st.caption(
        "✅ = the neuron's decision (z ≥ 0 → cat) matches the truth. The re-weighted fix only wins by ±0.5 "
        "because the Bunny differs from a cat by just 0.1 in whisker length — better *features* (e.g. 'hops?') "
        "would separate them far more robustly than any choice of weights."
    )


def main():
    st.title("🧠 Page 64: A Single Neuron")
    st.markdown(
        """
        A **neuron** is the smallest useful unit in a neural network — one decision-maker built from math you already know.

        It does exactly five things:

        1. **Receive** inputs $x_1, x_2, \\ldots, x_n$ (signals)
        2. **Weight** each input: multiply by $w_i$
        3. **Sum** everything — that's the **dot product** $\\mathbf{w} \\cdot \\mathbf{x}$
        4. **Shift** by a **bias** $b$
        5. **Activate** — pass the result through a (usually nonlinear) function to produce output $y$

        One neuron = one row of a matrix multiply, plus a bias, plus an activation function. That's the whole bridge from linear algebra to AI.
        """
    )

    st.divider()
    st.markdown("### 1) The Neuron Lab ⚡")
    st.markdown(
        "Pick a story preset, drag inputs and weights, choose an activation, then press **FIRE THE NEURON** "
        "to watch the signal flow. Switch modes to see the dot product as a projection or a waterfall of contributions. "
        "Every story uses the same decision rule: **yes when z ≥ 0** (equivalently σ(z) ≥ 0.5)."
    )
    render_neuron_lab()
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔢 The Math (One Line)")
        st.info("A neuron is a function: $y = f(\\mathbf{w} \\cdot \\mathbf{x} + b)$")
        st.markdown(
            r"""
**Step by step:**

| Step | Formula | Meaning |
|------|---------|---------|
| Weight | $w_i x_i$ | How much input $i$ matters (size of $\lvert w_i \rvert$) and in which direction (sign) |
| Sum | $z = \sum_i w_i x_i$ | Dot product $\mathbf{w}\cdot\mathbf{x}$ |
| Bias | $z \leftarrow z + b$ | Shift the decision boundary |
| Activate | $y = f(z)$ | Output (ReLU, sigmoid, tanh, …) |

With 3 inputs, $\mathbf{w}$ is a **row vector** and $\mathbf{x}$ is a **column vector** — same as **one row** of matrix $\times$ vector from Page 12.

Only the sigmoid output lies in $(0, 1)$ and *looks* like a probability — and even then it is not a calibrated confidence unless the neuron was trained (and checked) for that. ReLU outputs are unbounded; step outputs are just 0 or 1.
"""
        )

    with col2:
        st.markdown("### 🧬 Biology ↔ Math")
        st.success("Dendrites receive · Synapses weigh · Soma sums · Axon fires")
        st.markdown(
            """
| Biology | Math |
|---------|------|
| Signals arriving (dendrites) | Inputs $\\mathbf{x}$ |
| Synapse strength | Weights $\\mathbf{w}$ |
| Cell body (soma) integrates | Sum + bias $z$ |
| Fires an all-or-nothing spike down the axon | Activation $f(z)$ |

**Negative weights** mean “this input pushes *against* firing” (like inhibitory synapses).
**Bias** sets a built-in tendency: with $b > 0$ the neuron can fire even when all inputs are zero; with $b < 0$ it needs strong evidence.
"""
        )
        with st.expander("Where the analogy breaks"):
            st.markdown(
                "Artificial neurons are only *loosely inspired* by biology — not a one-to-one model of a real cell. "
                "A real neuron's action potential is all-or-nothing (closest to the **step** activation), "
                "it fires in time as a train of spikes, and its synapses change chemically. "
                "Sigmoid, tanh and ReLU produce graded numbers instead of spikes, and modern networks add "
                "operations (e.g. attention, normalization) with no direct biological counterpart."
            )

    st.divider()

    st.markdown("### 🎬 Three Things to Try")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### ⚡ Fire & Watch")
        st.write(
            "Press **FIRE THE NEURON** and follow the yellow pulse: "
            "each input lane → sum node → activation box → output. "
            "Thicker edges = larger $|w_i x_i|$."
        )
    with c2:
        st.markdown("#### 📊 Contributions Mode")
        st.write(
            "Switch to **Contributions** to see a waterfall: start at 0, add each $w_i x_i$, then the bias — "
            "the last bar is $z$. Green pushes up, red pulls down, and the main canvas names the biggest influence."
        )
    with c3:
        st.markdown("#### 🔢 Dot Product Mode")
        st.write(
            "Switch to **Dot Product** for a 2D slice ($x_1, x_2$ only): "
            "vector $\\mathbf{x}$, weight vector $\\mathbf{w}$ and the projection of $\\mathbf{x}$ onto $\\mathbf{w}$. "
            "Same geometry as Page 6 — now inside a neuron."
        )

    st.divider()
    st.markdown("### 2) Case Study: Build a Cat Detector 🐱")
    render_cat_case_study()

    st.divider()

    st.markdown("### 🤖 Bridge: From One Neuron to Networks")
    a1, a2, a3 = st.columns(3)
    with a1:
        st.markdown("#### 📐 Still Linear Algebra")
        st.write(
            "10 neurons in a layer = 10 rows of weights — a **10×n matrix** times your input vector. "
            "You already know how to do this from Pages 10–12."
        )
    with a2:
        st.markdown("#### 🎛️ Weights Are Learned")
        st.write(
            "Here you set weights by hand — the cat detector shows how fiddly that is. In training (Pages 50–56, 70), "
            "**gradient descent** nudges every $w_i$ and $b$ until predictions improve."
        )
    with a3:
        st.markdown("#### ➡️ Next: Activations")
        st.write(
            "This page previews ReLU, sigmoid and tanh. "
            "Page 65 compares them side by side, Page 66 shows why stacking linear layers **without** nonlinear "
            "activations collapses into a single affine map, and Page 67 builds whole networks from matrix layers."
        )

    st.divider()
    st.markdown(
        '<div style="text-align:center;color:#94a3b8;font-size:13px;">'
        "Page 64 — you can now read a neuron as dot product + bias + activation. "
        "Next Up: Page 65 — Activation Functions Compared ➔"
        "</div>",
        unsafe_allow_html=True,
    )
    safe_page_link("pages/65Activation Functions Compared.py", "Next: 65 · Activation Functions Compared", icon="➡️")


if __name__ == "__main__":
    main()
