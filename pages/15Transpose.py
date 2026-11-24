import sys
from pathlib import Path

import numpy as np
import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from common.matrix_display import matrix_html  # noqa: E402


st.set_page_config(page_title="Transpose - Rows Become Columns", layout="wide")


def make_matrix(rows, cols, seed, low=-9, high=10):
    rng = np.random.default_rng(seed)
    return rng.integers(low, high, size=(rows, cols)).astype(float)


def render_intro():
    st.title("Page 15: Transpose - Flip the Matrix")
    st.markdown(
        """
        Welcome to the **Matrix Mirror Room**.

        A transpose is a clean flip across the main diagonal:
        - every row becomes a column
        - every column becomes a row

        Core rule:
        """
    )
    st.latex(r"(A^T)_{ij} = A_{ji}")


def render_shape_story(A):
    st.header("1) Shape Swap")
    r, c = A.shape
    st.markdown("Transpose swaps dimensions like a magic card trick.")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Rows in A", r)
    with c2:
        st.metric("Cols in A", c)
    with c3:
        st.metric("Shape of A^T", f"{c} x {r}")
    st.info(f"If A is {r} x {c}, then A^T is {c} x {r}.")


def render_row_column_mapping(A):
    st.header("2) Row-to-Column Teleport")
    AT = A.T
    row_idx = st.selectbox("Pick a row from A", options=list(range(1, A.shape[0] + 1)), key="p15_row_pick")
    i = row_idx - 1

    row_vals = A[i, :]
    col_vals = AT[:, i]

    left, right = st.columns(2)
    with left:
        highlights = [(i, j) for j in range(A.shape[1])]
        st.markdown(matrix_html(A, f"A (highlight row {row_idx})", highlights, "#22c55e", precision=0), unsafe_allow_html=True)
    with right:
        highlights_t = [(j, i) for j in range(AT.shape[0])]
        st.markdown(
            matrix_html(AT, f"A^T (matching column {row_idx})", highlights_t, "#a78bfa", precision=0),
            unsafe_allow_html=True,
        )

    st.code(
        f"Row {row_idx} in A  = {np.array2string(row_vals.astype(int))}\n"
        f"Col {row_idx} in A^T = {np.array2string(col_vals.astype(int))}",
        language="text",
    )
    st.success("Same numbers, same order: row i of A is read top-to-bottom as column i of A^T.")


def render_index_explorer(A):
    st.header("3) Index Explorer: (i, j) -> (j, i)")
    AT = A.T
    c1, c2 = st.columns(2)
    with c1:
        i = st.number_input("Pick i (row in A)", min_value=1, max_value=A.shape[0], value=1, step=1, key=f"p15_i_{A.shape[0]}")
    with c2:
        j = st.number_input("Pick j (col in A)", min_value=1, max_value=A.shape[1], value=1, step=1, key=f"p15_j_{A.shape[1]}")
    i0, j0 = int(i - 1), int(j - 1)

    val = A[i0, j0]
    trans_val = AT[j0, i0]

    st.latex(rf"A_{{{int(i)},{int(j)}}} = {val:.0f} \quad \Rightarrow \quad (A^T)_{{{int(j)},{int(i)}}} = {trans_val:.0f}")
    st.success(f"Value preserved, only its address changed: ({int(i)}, {int(j)}) → ({int(j)}, {int(i)}).")


def render_double_flip(A):
    st.header("4) Flip Twice = Back Home")
    st.markdown("Transposing swaps every address `(i, j) → (j, i)`. Do it again and every entry walks back: `(A^T)^T = A`.")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(matrix_html(A, f"A ({A.shape[0]} x {A.shape[1]})", precision=0), unsafe_allow_html=True)
    with c2:
        st.markdown(matrix_html(A.T, f"A^T ({A.shape[1]} x {A.shape[0]})", precision=0), unsafe_allow_html=True)
    with c3:
        st.markdown(matrix_html(A.T.T, f"(A^T)^T ({A.shape[0]} x {A.shape[1]})", precision=0), unsafe_allow_html=True)
    st.latex(r"(A^T)^T = A")


def main():
    render_intro()

    st.sidebar.header("Transpose Controls")
    rows = st.sidebar.select_slider("Rows in A", options=[2, 3, 4, 5], value=3, key="p15_rows")
    cols = st.sidebar.select_slider("Cols in A", options=[2, 3, 4, 5], value=4, key="p15_cols")
    regen = st.sidebar.button("Generate new matrix", key="p15_regen")

    st.session_state.setdefault("p15_seed", 15)
    if regen:
        st.session_state.p15_seed += 1
    # Deterministic: the same (shape, seed) always yields the same matrix.
    A = make_matrix(rows, cols, seed=st.session_state.p15_seed)
    AT = A.T

    c1, c2 = st.columns(2, vertical_alignment="top")
    with c1:
        st.markdown(matrix_html(A, "Matrix A", precision=0), unsafe_allow_html=True)
    with c2:
        st.markdown(matrix_html(AT, "Transpose A^T", precision=0), unsafe_allow_html=True)

    st.sidebar.markdown(
        """
        ### Mission Notes
        - Flip across main diagonal
        - Row i of A = Column i of A^T
        - Doing transpose twice gives original matrix
        """
    )

    st.divider()
    render_shape_story(A)
    st.divider()
    render_row_column_mapping(A)
    st.divider()
    render_index_explorer(A)
    st.divider()
    render_double_flip(A)

    st.markdown(
        """
        ---
        ### Recap
        - Transpose does not change values, only where they live.
        - Shape swaps from `(r, c)` to `(c, r)`.
        - Rule to remember forever: `(A^T)_{ij} = A_{ji}`.
        - Bonus fact: `(A^T)^T = A`.
        """
    )


if __name__ == "__main__":
    main()

