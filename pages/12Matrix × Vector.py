
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


st.set_page_config(page_title="Matrix x Vector", layout="wide")

CARD_STYLE = dict(theme="lab", cell_style="fill", precision=2, font_size=19, cell_padding="8px 12px")


def matrix_html(matrix, title, highlight=None, color="#38bdf8"):
    return matrix_display.matrix_html(matrix, title, highlight, color, min_width=42, **CARD_STYLE)


def vector_html(vector, title, highlight=None, color="#f97316"):
    return matrix_display.vector_html(vector, title, highlight, color, min_width=72, **CARD_STYLE)


def row_dot_product_steps(A, x, reveal_rows):
    y = A @ x
    shown = np.full_like(y, np.nan, dtype=float)
    for i in range(reveal_rows):
        shown[i] = y[i]
    return y, shown


def make_matrix(rows, cols, seed):
    return np.random.default_rng(seed).integers(-4, 6, size=(rows, cols)).astype(float)


def make_vector(size, seed):
    return np.random.default_rng(seed).integers(-4, 6, size=(size,)).astype(float)


def render_intro():
    st.title("Page 12: Matrix x Vector")
    st.markdown(
        """
        Welcome to the **Input Cannon**:  
        You fire one vector `x` into a matrix machine `A`, and out comes a new vector `y`.

        ### Core idea
        - `A` has shape `(rows, cols)`
        - `x` has shape `(cols,)`
        - output `y = A x` has shape `(rows,)`

        Every output entry is:
        `y_i = dot(row_i_of_A, x)`
        """
    )


def render_main_visual(A, x):
    st.header("1) Fire the Vector Through the Matrix")
    rows, cols = A.shape

    reveal_rows = st.slider(
        "Reveal output rows solved so far",
        min_value=0,
        max_value=rows,
        value=min(1, rows),
        key="p12_reveal_rows",
    )
    y_full, y_partial = row_dot_product_steps(A, x, reveal_rows)

    left, mid, right = st.columns([1.4, 0.6, 1.0], vertical_alignment="top")
    with left:
        if reveal_rows > 0:
            selected = reveal_rows - 1
            highlight = [(selected, j) for j in range(cols)]
            st.markdown(matrix_html(A, "Matrix A", highlight, "#22c55e"), unsafe_allow_html=True)
        else:
            st.markdown(matrix_html(A, "Matrix A"), unsafe_allow_html=True)
    with mid:
        st.markdown(vector_html(x, "Input Vector x", list(range(cols))), unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;font-size:36px;padding:12px;'>→</div>", unsafe_allow_html=True)
    with right:
        hi = [reveal_rows - 1] if reveal_rows > 0 else []
        st.markdown(vector_html(y_partial, "Output Vector y = A x (? = not solved yet)", hi, "#a78bfa"),
                    unsafe_allow_html=True)

    if reveal_rows == 0:
        st.info("Move the slider to solve each output entry one row at a time.")
        return

    i = reveal_rows - 1
    # Use × (not *): pairs of * would be swallowed by Markdown as italics
    terms = [f"({fmt_factor(A[i, j])} × {fmt_factor(x[j])})" for j in range(cols)]
    explanation = " + ".join(terms)
    st.success(
        f"Latest solved output: y[{i+1}] = row_{i+1}(A) · x = {explanation} = {y_full[i] + 0.0:.2f}"
    )
    st.code("Rule: y_i = Σ_j A[i, j] × x[j]", language="text")

    with st.expander("See full multiplication result"):
        st.write("`y = A @ x`")
        st.write(np.round(y_full, 3))


def render_shape_story(A):
    st.header("2) Shape Story (Why dimensions must match)")
    rows, cols = A.shape
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(
            f"""
            ### The Rule of Dimensions
            For matrix multiplication to work, the **number of columns in the matrix** must exactly match the **number of elements (rows) in the vector**.

            Let's look at our current shapes:
            - Matrix `A`: **{rows} rows × {cols} columns**
            - Vector `x`: **{cols} rows × 1 column**
            - Output `y`: **{rows} rows × 1 column**
            
            The "inner dimensions" (the `{cols}` columns of A and `{cols}` rows of x) match!
            """
        )
    with col2:
        st.info(
            """
            💡 **Why?**  
            Because when we multiply, we pair up each element of a matrix row with an element of the vector. 
            If a row has 3 elements, the vector *must* have 3 elements to pair with them!
            """
        )
        with st.expander(f"🚫 What if x had {cols + 1} entries instead of {cols}?"):
            bad_x = np.ones(cols + 1)
            try:
                A @ bad_x
            except ValueError as err:
                st.error(f"NumPy refuses: `{err}`")
            st.caption(
                f"Each row of A has only {cols} numbers, so the last entry of x has no partner. "
                f"The product A x only exists when x has exactly {cols} entries."
            )
    
    st.markdown("### Visualizing the Shape Transformation")
    st.latex(r"\underbrace{A_{m \times n}}_{\text{Matrix}} \cdot \underbrace{x_{n \times 1}}_{\text{Vector}} \rightarrow \underbrace{y_{m \times 1}}_{\text{Output Vector}}")
    st.markdown(
        """
        Notice how the $n$ dimensions "cancel out", leaving us with an output of size $m \\times 1$. 
        Think of the matrix as a machine that transforms a vector of size $n$ into a new vector of size $m$.
        """
    )



def main():
    render_intro()
    st.sidebar.header("Matrix x Vector Controls")

    rows = st.sidebar.select_slider("Rows in matrix A", options=[2, 3, 4, 5], value=3, key="p12_rows")
    cols = st.sidebar.select_slider("Columns in matrix A / size of x", options=[2, 3, 4, 5], value=3, key="p12_cols")
    regen = st.sidebar.button("Generate new A and x", key="p12_regen")

    # Seeded generation: same A and x on every rerun until the shape changes or the button is pressed
    if "p12_seed" not in st.session_state:
        st.session_state.p12_seed = 0
    if regen:
        st.session_state.p12_seed += 1

    if regen or st.session_state.get("p12_shape") != (rows, cols):
        seed = st.session_state.p12_seed
        st.session_state.p12_A = make_matrix(rows, cols, seed=[seed, rows, cols, 0])
        st.session_state.p12_x = make_vector(cols, seed=[seed, rows, cols, 1])
        st.session_state.p12_shape = (rows, cols)

    A = st.session_state.p12_A
    x = st.session_state.p12_x

    st.sidebar.markdown(
        """
        ### Mission Brief
        - Each output entry is one **row dot product**
        - Matrix changes the vector into a new space
        - This is the engine inside neural layers
        """
    )

    render_main_visual(A, x)
    st.divider()
    render_shape_story(A)

    st.markdown(
        """
        ---
        ### Recap
        - Matrix x vector is a machine: input vector in, output vector out.
        - Every output number comes from one row of `A` dotted with `x`.
        - This operation is exactly what a neural network layer does before activation.
        """
    )


if __name__ == "__main__":
    main()

