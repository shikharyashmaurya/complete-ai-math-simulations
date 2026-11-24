import functools
import sys
from pathlib import Path

import numpy as np
import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from common import matrix_display  # noqa: E402
from common.mathutils import fmt_factor  # noqa: E402
from common.matrix_display import partial_matrix, row_major_cells  # noqa: E402


st.set_page_config(page_title="Matrix x Matrix", layout="wide")

matrix_html = functools.partial(
    matrix_display.matrix_html, theme="lab", cell_style="fill", precision=2, font_size=18, cell_padding="7px 10px", min_width=42
)


def extract_row_as_matrix(A, i):
    return A[i : i + 1, :]


def extract_col_as_matrix(B, j):
    return B[:, j : j + 1]


def dot_terms(A, B, i, j):
    return [A[i, k] * B[k, j] for k in range(A.shape[1])]


def make_matrix(rows, cols, seed, low=-4, high=7):
    return np.random.default_rng(seed).integers(low, high, size=(rows, cols)).astype(float)


def render_intro():
    st.title("Page 13: Matrix x Matrix")
    st.markdown(
        """
        Welcome to the **Matrix Factory**.  
        One matrix `A` and one matrix `B` enter the machine, and a new matrix `C = A @ B` comes out.

        ### Core idea
        - `A` shape: `(m, n)`
        - `B` shape: `(n, p)`
        - Output `C` shape: `(m, p)`

        Every output cell is:
        **row of A dot column of B**
        """
    )


def render_shape_gate(A, B):
    st.header("1) Shape Gate: Can These Matrices Multiply?")
    m, n = A.shape
    n2, p = B.shape
    ok = n == n2

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("A shape", f"{m} x {n}")
    with c2:
        st.metric("B shape", f"{n2} x {p}")
    with c3:
        st.metric("Inner dimensions", f"{n} and {n2}")

    st.latex(r"A_{m \times n} \cdot B_{n \times p} = C_{m \times p}")
    if ok:
        st.success("Access granted. Inner dimensions match, so multiplication is valid.")
    else:
        st.error(
            f"Access denied. Inner dimensions do not match: each row of A has {n} numbers, but each column of B "
            f"has {n2}, so a row and a column cannot be paired up for a dot product. "
            "Set **Rows of B** equal to **Cols of A** in the sidebar to continue."
        )
        bad_left, bad_right = st.columns(2)
        with bad_left:
            st.markdown(matrix_html(A, f"A ({m} x {n}): rows have {n} numbers", [(0, k) for k in range(n)], "#22c55e"),
                        unsafe_allow_html=True)
        with bad_right:
            st.markdown(matrix_html(B, f"B ({n2} x {p}): columns have {n2} numbers", [(k, 0) for k in range(n2)],
                                    "#f87171"), unsafe_allow_html=True)

    return ok


def render_main_factory(A, B):
    st.header("2) Row-Dot-Column Spotlight")
    C = A @ B
    out_rows, out_cols = C.shape
    total_cells = out_rows * out_cols

    step = st.slider(
        "Factory progress (how many output cells are solved)",
        min_value=0,
        max_value=total_cells,
        value=min(1, total_cells),
        key="p13_step",
    )
    solved = row_major_cells(step, out_rows, out_cols)
    partial = partial_matrix(C, solved)

    if solved:
        i, j = solved[-1]
        row_hi = [(i, k) for k in range(A.shape[1])]
        col_hi = [(k, j) for k in range(B.shape[0])]
    else:
        # Nothing solved yet: do not spotlight any row/column
        i, j = 0, 0
        row_hi, col_hi = [], []
    out_hi = solved

    left, mid, right = st.columns([1.25, 1.25, 1.1], vertical_alignment="top")
    with left:
        st.markdown(matrix_html(A, "Matrix A (row selected)", row_hi, "#22c55e"), unsafe_allow_html=True)
    with mid:
        st.markdown(matrix_html(B, "Matrix B (column selected)", col_hi, "#a78bfa"), unsafe_allow_html=True)
    with right:
        st.markdown(matrix_html(partial, "Output C = A @ B (? = not solved yet)", out_hi, "#f59e0b"),
                    unsafe_allow_html=True)

    if step == 0:
        st.info("Move the slider to start producing cells in C one by one.")
        return

    terms = dot_terms(A, B, i, j)
    # Use × (not *): pairs of * would be swallowed by Markdown as italics
    expression = " + ".join([f"({fmt_factor(A[i, k])} × {fmt_factor(B[k, j])})" for k in range(A.shape[1])])
    st.success(
        f"Latest cell solved: C[{i+1},{j+1}] = row_{i+1}(A) · col_{j+1}(B) = "
        f"{expression} = {sum(terms) + 0.0:.2f}"
    )
    st.code("Rule: C[i, j] = Σ_k A[i, k] × B[k, j]", language="text")

    sub1, sub2 = st.columns(2)
    with sub1:
        st.markdown(
            matrix_html(extract_row_as_matrix(A, i), f"Row {i+1} of A", [(0, k) for k in range(A.shape[1])], "#22c55e"),
            unsafe_allow_html=True,
        )
    with sub2:
        st.markdown(
            matrix_html(extract_col_as_matrix(B, j), f"Column {j+1} of B", [(k, 0) for k in range(B.shape[0])], "#a78bfa"),
            unsafe_allow_html=True,
        )


def render_cell_explorer(A, B):
    st.header("3) Choose Any Output Cell")
    C = A @ B
    out_rows, out_cols = C.shape

    c1, c2 = st.columns(2)
    with c1:
        row_pick = st.selectbox("Pick output row", options=list(range(1, out_rows + 1)), key="p13_row_pick")
    with c2:
        col_pick = st.selectbox("Pick output column", options=list(range(1, out_cols + 1)), key="p13_col_pick")

    i = row_pick - 1
    j = col_pick - 1
    terms = dot_terms(A, B, i, j)

    st.markdown("### Dot Product Breakdown")
    for k, term in enumerate(terms, start=1):
        st.write(
            f"- Term {k}: A[{i+1},{k}] × B[{k},{j+1}] = {fmt_factor(A[i, k-1])} × {fmt_factor(B[k-1, j])} "
            f"= {term + 0.0:.2f}"
        )
    st.info(f"Final value: C[{row_pick},{col_pick}] = {sum(terms) + 0.0:.2f}")

    with st.expander("Reveal full output matrix C"):
        st.write(np.round(C, 3))


def main():
    render_intro()
    st.sidebar.header("Matrix x Matrix Controls")

    m = st.sidebar.select_slider("Rows of A (m)", options=[2, 3, 4], value=3, key="p13_m")
    n = st.sidebar.select_slider("Cols of A (n)", options=[2, 3, 4, 5], value=3, key="p13_n")
    n_b = st.sidebar.select_slider(
        "Rows of B (must equal Cols of A — try a mismatch!)", options=[2, 3, 4, 5], value=3, key="p13_n_b"
    )
    p = st.sidebar.select_slider("Cols of B (p)", options=[2, 3, 4], value=3, key="p13_p")
    regen = st.sidebar.button("Generate new matrices", key="p13_regen")

    # Seeded generation: same A and B on every rerun until a shape changes or the button is pressed
    if "p13_seed" not in st.session_state:
        st.session_state.p13_seed = 0
    if regen:
        st.session_state.p13_seed += 1

    shape_key = (m, n, n_b, p)
    if regen or st.session_state.get("p13_shape") != shape_key:
        seed = st.session_state.p13_seed
        st.session_state.p13_A = make_matrix(m, n, seed=[seed, m, n, 0])
        st.session_state.p13_B = make_matrix(n_b, p, seed=[seed, n_b, p, 1])
        st.session_state.p13_shape = shape_key

    A = st.session_state.p13_A
    B = st.session_state.p13_B

    st.sidebar.markdown(
        """
        ### Mission Brief
        - A row meets B column
        - One dot product makes one output cell
        - Repeat for all cells in C
        """
    )

    can_multiply = render_shape_gate(A, B)
    if not can_multiply:
        return

    st.divider()
    render_main_factory(A, B)
    st.divider()
    render_cell_explorer(A, B)

    st.markdown(
        """
        ---
        ### Recap
        - Matrix x matrix multiplication builds each output cell from a row-dot-column.
        - Shape check is non-negotiable: inner dimensions must match.
        - This is the core operation that powers deep learning layers.
        """
    )


if __name__ == "__main__":
    main()

