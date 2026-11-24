import functools
import sys
from pathlib import Path

import numpy as np
import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from common.mathutils import close_enough, fmt_factor, fmt_num, fmt_signed  # noqa: E402
from common.matrix_display import matrix_html, partial_matrix, row_major_cells  # noqa: E402


st.set_page_config(page_title="Matrix Addition & Scalar Multiplication", layout="wide")

matrix_to_html = functools.partial(
    matrix_html, theme="lab", cell_style="fill", precision=1, font_size=20, cell_padding="8px 12px", min_width=46
)


def build_random_matrix(rows, cols, seed, low=-5, high=9):
    return np.random.default_rng(seed).integers(low, high, size=(rows, cols)).astype(float)


def render_intro():
    st.title("Page 11: Matrix Addition & Scalar Multiplication")
    st.markdown(
        """
        Welcome to the **Number Grid Lab**.
        Today we learn two superpowers:
        - **Matrix Addition**: add matching cells (same row, same column).
        - **Scalar Multiplication**: multiply every cell by one number.

        Imagine each matrix as a game map of scores.  
        Addition combines two maps.  
        Scalar multiplication turns the volume up or down on the same map.
        """
    )


def render_addition_section(A, B):
    st.header("1) Matrix Addition: Cell-by-Cell")
    rows, cols = A.shape
    total_cells = rows * cols
    C = A + B

    step = st.slider(
        "Animation step (how many cells solved so far)",
        min_value=0,
        max_value=total_cells,
        value=min(2, total_cells),
        key="p11_add_step",
    )
    solved = row_major_cells(step, rows, cols)
    partial = partial_matrix(C, solved)

    left, mid, right = st.columns([1, 0.25, 1], vertical_alignment="top")
    with left:
        st.markdown(matrix_to_html(A, "Matrix A", solved, "#22c55e"), unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;font-size:34px;'>+</div>", unsafe_allow_html=True)
        st.markdown(matrix_to_html(B, "Matrix B", solved, "#a78bfa"), unsafe_allow_html=True)
    with mid:
        st.markdown("<div style='text-align:center;font-size:42px;padding-top:80px;'>=</div>", unsafe_allow_html=True)
    with right:
        st.markdown(
            matrix_to_html(partial, "A + B (partial, ? = not solved yet)", solved, "#f59e0b"),
            unsafe_allow_html=True,
        )

    if solved:
        r, c = solved[-1]
        st.success(
            f"Latest solved cell: C[{r+1},{c+1}] = A[{r+1},{c+1}] + B[{r+1},{c+1}] "
            f"= {fmt_num(A[r,c], 1)} {fmt_signed(B[r,c], 1)} = {fmt_num(C[r,c], 1)}"
        )
    else:
        st.info("Move the slider to start solving matrix addition, one cell at a time.")

    st.code("Rule: (A + B)[i, j] = A[i, j] + B[i, j]", language="text")


def render_scalar_section(A):
    st.header("2) Scalar Multiplication: Stretch or Flip")
    scalar = st.slider("Choose scalar k", min_value=-4.0, max_value=4.0, value=1.5, step=0.5, key="p11_scalar")
    kA = scalar * A

    total_cells = A.size
    step = st.slider(
        "Reveal cells in kA",
        min_value=0,
        max_value=total_cells,
        value=min(3, total_cells),
        key="p11_scalar_step",
    )
    solved = row_major_cells(step, *A.shape)
    partial = partial_matrix(kA, solved)

    col1, col2 = st.columns(2, vertical_alignment="top")
    with col1:
        st.markdown(matrix_to_html(A, "Original Matrix A", solved, "#38bdf8"), unsafe_allow_html=True)
    with col2:
        st.markdown(
            matrix_to_html(partial, f"Scaled Matrix kA (k={scalar:.1f}, ? = not solved yet)", solved, "#f97316"),
            unsafe_allow_html=True,
        )

    if solved:
        r, c = solved[-1]
        st.success(
            f"Latest solved cell: (kA)[{r+1},{c+1}] = k × A[{r+1},{c+1}] "
            f"= {fmt_num(scalar, 1)} × {fmt_factor(A[r,c], 1)} = {fmt_num(kA[r,c], 1)}"
        )

    if close_enough(scalar, 0.0):
        meaning = "squashes every cell to 0"
    elif close_enough(abs(scalar), 1.0):
        meaning = "flips every sign (same sizes)" if scalar < 0 else "leaves every cell unchanged"
    else:
        size_change = "stretches" if abs(scalar) > 1 else "shrinks"
        meaning = f"flips sign + {size_change}" if scalar < 0 else size_change
    st.info(f"When k = {scalar:.1f}, every cell gets scaled the same way: **{meaning}**.")
    st.code("Rule: (kA)[i, j] = k × A[i, j]", language="text")


def main():
    render_intro()

    st.sidebar.header("Matrix Controls")
    rows = st.sidebar.select_slider("Rows", options=[2, 3, 4], value=3, key="p11_rows")
    cols = st.sidebar.select_slider("Columns", options=[2, 3, 4], value=3, key="p11_cols")
    regenerate = st.sidebar.button("Generate new random matrices", key="p11_regenerate")

    # Matrices come from a seed kept in session_state: the same numbers on every rerun until the
    # shape changes or the user presses the button.
    if "p11_seed" not in st.session_state:
        st.session_state.p11_seed = 0
    if regenerate:
        st.session_state.p11_seed += 1

    if regenerate or st.session_state.get("p11_shape") != (rows, cols):
        seed = st.session_state.p11_seed
        st.session_state.p11_A_matrix = build_random_matrix(rows, cols, seed=[seed, rows, cols, 0])
        st.session_state.p11_B_matrix = build_random_matrix(rows, cols, seed=[seed, rows, cols, 1])
        st.session_state.p11_shape = (rows, cols)

    A = st.session_state.p11_A_matrix
    B = st.session_state.p11_B_matrix

    st.sidebar.markdown(
        """
        ### Mission Brief
        - Same shape required for `A + B`
        - Add matching cells only
        - Multiply every cell for `kA`
        """
    )

    render_addition_section(A, B)
    st.divider()
    render_scalar_section(A)

    st.markdown(
        """
        ---
        ### Recap
        - Matrix addition combines two equal-size grids, cell by cell.
        - Scalar multiplication rescales every entry of one grid by the same number.
        - These two operations are core building blocks for neural network computations.
        """
    )


if __name__ == "__main__":
    main()
