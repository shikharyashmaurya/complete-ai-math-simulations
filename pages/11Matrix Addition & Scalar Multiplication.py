import numpy as np
import streamlit as st


st.set_page_config(page_title="Matrix Addition & Scalar Multiplication", layout="wide")


def matrix_to_html(matrix, title, highlight=None, color="#60a5fa"):
    rows, cols = matrix.shape
    html = f"""
    <div style="padding:12px;border:1px solid #334155;border-radius:12px;background:#0f172a22;">
      <h4 style="margin:0 0 8px 0;">{title}</h4>
      <table style="border-collapse:collapse;font-size:20px;">
    """
    for i in range(rows):
        html += "<tr>"
        for j in range(cols):
            bg = "transparent"
            if highlight is not None and (i, j) in highlight:
                bg = color
            html += (
                f"<td style='border:1px solid #475569;padding:8px 12px;text-align:center;"
                f"min-width:46px;background:{bg};'>{matrix[i, j]:.1f}</td>"
            )
        html += "</tr>"
    html += "</table></div>"
    return html


def build_random_matrix(rows, cols, low=-5, high=9):
    return np.random.randint(low, high, size=(rows, cols)).astype(float)


def step_coordinates(step, rows, cols):
    coords = []
    for idx in range(step):
        r = idx // cols
        c = idx % cols
        if r < rows:
            coords.append((r, c))
    return coords


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
        key="add_step",
    )
    solved = step_coordinates(step, rows, cols)

    partial = np.full_like(C, np.nan)
    for r, c in solved:
        partial[r, c] = C[r, c]

    left, mid, right = st.columns([1, 0.25, 1], vertical_alignment="top")
    with left:
        st.markdown(matrix_to_html(A, "Matrix A", solved, "#22c55e"), unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;font-size:34px;'>+</div>", unsafe_allow_html=True)
        st.markdown(matrix_to_html(B, "Matrix B", solved, "#a78bfa"), unsafe_allow_html=True)
    with mid:
        st.markdown("<div style='text-align:center;font-size:42px;padding-top:80px;'>=</div>", unsafe_allow_html=True)
    with right:
        shown = np.where(np.isnan(partial), 0.0, partial)
        st.markdown(
            matrix_to_html(shown, "A + B (partial)", solved, "#f59e0b"),
            unsafe_allow_html=True,
        )

    if solved:
        r, c = solved[-1]
        st.success(
            f"Latest solved cell: C[{r+1},{c+1}] = A[{r+1},{c+1}] + B[{r+1},{c+1}] "
            f"= {A[r,c]:.1f} + {B[r,c]:.1f} = {C[r,c]:.1f}"
        )
    else:
        st.info("Move the slider to start solving matrix addition, one cell at a time.")

    st.code("Rule: (A + B)[i, j] = A[i, j] + B[i, j]", language="text")


def render_scalar_section(A):
    st.header("2) Scalar Multiplication: Stretch or Flip")
    scalar = st.slider("Choose scalar k", min_value=-4.0, max_value=4.0, value=1.5, step=0.5)
    kA = scalar * A

    total_cells = A.size
    step = st.slider(
        "Reveal cells in kA",
        min_value=0,
        max_value=total_cells,
        value=min(3, total_cells),
        key="scalar_step",
    )
    solved = step_coordinates(step, *A.shape)

    partial = np.full_like(kA, np.nan)
    for r, c in solved:
        partial[r, c] = kA[r, c]
    shown = np.where(np.isnan(partial), 0.0, partial)

    col1, col2 = st.columns(2, vertical_alignment="top")
    with col1:
        st.markdown(matrix_to_html(A, "Original Matrix A", solved, "#38bdf8"), unsafe_allow_html=True)
    with col2:
        st.markdown(
            matrix_to_html(shown, f"Scaled Matrix kA (k={scalar:.1f})", solved, "#f97316"),
            unsafe_allow_html=True,
        )

    if solved:
        r, c = solved[-1]
        st.success(
            f"Latest solved cell: (kA)[{r+1},{c+1}] = k * A[{r+1},{c+1}] "
            f"= {scalar:.1f} * {A[r,c]:.1f} = {kA[r,c]:.1f}"
        )

    meaning = "flips sign + stretches" if scalar < 0 else "stretches/shrinks"
    st.info(f"When k = {scalar:.1f}, every cell gets scaled the same way: **{meaning}**.")
    st.code("Rule: (kA)[i, j] = k * A[i, j]", language="text")


def main():
    render_intro()

    st.sidebar.header("Matrix Controls")
    rows = st.sidebar.select_slider("Rows", options=[2, 3, 4], value=3)
    cols = st.sidebar.select_slider("Columns", options=[2, 3, 4], value=3)
    regenerate = st.sidebar.button("Generate new random matrices")

    if "A_matrix" not in st.session_state or "B_matrix" not in st.session_state:
        st.session_state.A_matrix = build_random_matrix(rows, cols)
        st.session_state.B_matrix = build_random_matrix(rows, cols)
        st.session_state.shape = (rows, cols)

    if regenerate or st.session_state.get("shape") != (rows, cols):
        st.session_state.A_matrix = build_random_matrix(rows, cols)
        st.session_state.B_matrix = build_random_matrix(rows, cols)
        st.session_state.shape = (rows, cols)

    A = st.session_state.A_matrix
    B = st.session_state.B_matrix

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
