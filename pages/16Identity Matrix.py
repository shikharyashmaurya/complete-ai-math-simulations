import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from common.matrix_display import matrix_html  # noqa: E402


st.set_page_config(page_title="Identity Matrix - The Perfect Do-Nothing Machine", layout="wide")


def make_identity(n):
    return np.eye(n)


def draw_vector_lab(v, transformed):
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor("#0b1020")
    ax.set_facecolor("#0f172a")

    max_abs = max(np.max(np.abs(v)), np.max(np.abs(transformed)), 1.0)
    lim = float(max_abs + 1.5)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.axhline(0, color="#64748b", linewidth=1)
    ax.axvline(0, color="#64748b", linewidth=1)
    ax.grid(alpha=0.25, color="#94a3b8", linestyle="--")

    x1, y1 = v[0], v[1]
    x2, y2 = transformed[0], transformed[1]
    ax.quiver(0, 0, x1, y1, angles="xy", scale_units="xy", scale=1, color="#22d3ee", width=0.008)
    ax.quiver(0, 0, x2, y2, angles="xy", scale_units="xy", scale=1, color="#f97316", width=0.004)

    ax.scatter([x1], [y1], color="#22d3ee", s=55)
    ax.scatter([x2], [y2], color="#f97316", s=35)

    ax.text(x1 + 0.2, y1 + 0.2, "v (original)", color="#67e8f9", fontsize=10)
    ax.text(x2 + 0.2, y2 - 0.5, "I·v (after identity)", color="#fdba74", fontsize=10)

    ax.set_title("2D Vector: Before vs After Identity", color="#e2e8f0", pad=10)
    ax.tick_params(colors="#cbd5e1")
    for spine in ax.spines.values():
        spine.set_color("#64748b")
    return fig


def draw_radar(values):
    labels = ["Position", "Direction", "Length", "Angle", "Components"]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    vals = np.array(values)

    angles_closed = np.concatenate([angles, [angles[0]]])
    vals_closed = np.concatenate([vals, [vals[0]]])

    fig = plt.figure(figsize=(4.5, 4.5))
    fig.patch.set_facecolor("#0b1020")
    ax = plt.subplot(111, polar=True)
    ax.set_facecolor("#0f172a")

    ax.plot(angles_closed, vals_closed, color="#34d399", linewidth=2)
    ax.fill(angles_closed, vals_closed, color="#34d399", alpha=0.25)
    ax.set_xticks(angles)
    ax.set_xticklabels(labels, color="#cbd5e1", fontsize=9)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["25%", "50%", "75%", "100%"], color="#94a3b8", fontsize=8)
    ax.set_ylim(0, 1.05)
    ax.set_title("What Stayed Same?", color="#e2e8f0", pad=12)
    return fig


def render_intro():
    st.title("Page 16: Identity Matrix - The Perfect Do-Nothing Machine")
    st.markdown(
        """
        Imagine a magical machine that **looks active** but changes absolutely nothing.
        That machine is the **identity matrix**.

        For any vector `v`, multiplying by identity gives the same vector:
        """
    )
    st.latex(r"I_n v = v")
    st.info("Identity is the matrix version of multiplying by 1.")


def render_identity_builder(n):
    st.header("1) Build the Identity")
    I = make_identity(n)
    st.markdown("Identity has `1`s on the main diagonal and `0`s everywhere else.")
    st.markdown(matrix_html(I, f"I_{n}", highlight=[(i, i) for i in range(n)], color="#22c55e", precision=0), unsafe_allow_html=True)
    return I


DEFAULT_V = [3.0, -2.0, 1.5, 0.5, -1.0, 2.5]


def render_vector_experiment(I):
    st.header("2) Vector Teleporter (That Goes Nowhere)")
    st.markdown("Pick a vector. Send it through `I`. Watch how nothing changes.")

    n = I.shape[0]
    v = np.zeros(n)
    cols = st.columns(3)
    for k in range(n):
        with cols[k % 3]:
            v[k] = st.slider(f"v[{k + 1}]", -8.0, 8.0, DEFAULT_V[k], 0.5, key=f"p16_v{k + 1}")
    transformed = I @ v

    left, right = st.columns([1.15, 1])
    with left:
        fig = draw_vector_lab(v[:2], transformed[:2])
        st.pyplot(fig, width="stretch")
        plt.close(fig)
        if n > 2:
            st.caption(f"The picture shows only the first 2 of {n} components; the panel on the right checks all {n}.")
    with right:
        st.code(
            f"v        = {np.array2string(v, precision=1)}\n"
            f"I @ v    = {np.array2string(transformed, precision=1)}\n"
            f"v - I @ v= {np.array2string(v - transformed, precision=1)}",
            language="text",
        )
        if np.allclose(v, transformed):
            st.success("No change at all. Identity passes the vector untouched.")
    return v


def render_matrix_neutral(I):
    st.header("3) Identity Is the Number 1 for Matrices")
    n = I.shape[0]
    st.markdown("Multiplying any square matrix `A` by `I` — on the left **or** on the right — gives `A` back.")
    st.latex(r"A\,I = I\,A = A")

    st.session_state.setdefault("p16_seed", 16)
    if st.button("New random A", key="p16_new_A"):
        st.session_state.p16_seed += 1
    A = np.random.default_rng(st.session_state.p16_seed).integers(-5, 6, size=(n, n)).astype(float)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(matrix_html(A, "A", precision=0), unsafe_allow_html=True)
    with c2:
        st.markdown(matrix_html(I @ A, "I @ A", precision=0), unsafe_allow_html=True)
    with c3:
        st.markdown(matrix_html(A @ I, "A @ I", precision=0), unsafe_allow_html=True)
    if np.allclose(I @ A, A) and np.allclose(A @ I, A):
        st.success("I @ A = A @ I = A — identity is the neutral element of matrix multiplication.")


def render_proof_panel(I):
    st.header("4) Why It Works (Row Dot Product View)")
    n = I.shape[0]
    st.markdown("Each output component is one row of `I` dotted with vector `v`.")

    row_pick = st.selectbox("Inspect row of I", options=list(range(1, n + 1)), key="p16_row_pick")
    k = row_pick - 1
    basis_row = I[k]

    st.markdown(
        matrix_html(
            I,
            f"I_{n} (highlight row {row_pick})",
            highlight=[(k, j) for j in range(n)],
            color="#a78bfa",
            precision=0,
        ),
        unsafe_allow_html=True,
    )

    terms = [rf"{int(basis_row[j])}\cdot v_{{{j + 1}}}" for j in range(n)]
    st.latex(rf"(Iv)_{{{row_pick}}} = " + " + ".join(terms))
    st.latex(rf"(Iv)_{{{row_pick}}} = v_{{{row_pick}}}")
    st.caption(
        f"Row {row_pick} has a single 1 at position {row_pick}, so it selects exactly v_{row_pick}."
    )


def preservation_scores(v, w, tol=1e-9):
    """Scores in [0, 1] comparing w = I @ v with v (1 = perfectly preserved)."""
    nv, nw = float(np.linalg.norm(v)), float(np.linalg.norm(w))
    position = 1.0 - min(1.0, float(np.linalg.norm(w - v)) / max(nv, tol))
    if nv < tol and nw < tol:
        direction = angle = length = 1.0
    elif nv < tol or nw < tol:
        direction = angle = length = 0.0
    else:
        cos = float(np.clip(np.dot(v, w) / (nv * nw), -1.0, 1.0))
        direction = max(0.0, cos)
        angle = 1.0 - float(np.arccos(cos)) / np.pi
        length = min(nv, nw) / max(nv, nw)
    components = float(np.mean(np.isclose(v, w, atol=tol)))
    return [position, direction, length, angle, components]


def render_no_change_score(I, v):
    st.header("5) Identity Scoreboard")
    st.markdown("How much does identity preserve the vector's properties? (Measured live on your vector `v` vs `I @ v`.)")
    scores = preservation_scores(v, I @ v)
    fig = draw_radar(scores)
    st.pyplot(fig, width="content")
    plt.close(fig)
    pct = 100.0 * float(np.mean(scores))
    if pct > 99.999:
        st.success("Score: 100% unchanged. Identity is mathematically invisible.")
    else:
        st.info(f"Average preservation score: {pct:.1f}%")


def render_recap():
    st.markdown(
        """
        ---
        ### Recap
        - Identity matrix is the neutral element of matrix multiplication.
        - Multiplying a vector by identity keeps every component the same.
        - Geometrically: no rotation, no scaling, no shear, no flip.
        - Practical meaning: it is the "do nothing" transform.
        """
    )


def main():
    render_intro()

    st.sidebar.header("Identity Controls")
    n = st.sidebar.select_slider("Dimension of identity matrix", options=[2, 3, 4, 5, 6], value=3, key="p16_n")
    st.sidebar.markdown(
        """
        ### Mission
        Prove that identity matrix:
        - keeps vectors unchanged
        - keeps geometry unchanged
        - acts like number 1 for matrices
        """
    )

    I = render_identity_builder(n)
    st.divider()
    v = render_vector_experiment(I)
    st.divider()
    render_matrix_neutral(I)
    st.divider()
    render_proof_panel(I)
    st.divider()
    render_no_change_score(I, v)
    st.divider()
    render_recap()


if __name__ == "__main__":
    main()

