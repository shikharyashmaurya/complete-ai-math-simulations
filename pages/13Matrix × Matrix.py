import numpy as np
import streamlit as st


st.set_page_config(page_title="Matrix x Matrix", layout="wide")


def matrix_html(matrix, title, highlight=None, color="#38bdf8"):
    rows, cols = matrix.shape
    highlight = highlight or []
    html = f"""
    <div style="padding:12px;border:1px solid #334155;border-radius:12px;background:#0f172a22;">
      <h4 style="margin:0 0 8px 0;">{title}</h4>
      <table style="border-collapse:collapse;font-size:18px;">
    """
    for i in range(rows):
        html += "<tr>"
        for j in range(cols):
            bg = color if (i, j) in highlight else "transparent"
            html += (
                f"<td style='border:1px solid #475569;padding:7px 10px;text-align:center;"
                f"min-width:42px;background:{bg};'>{matrix[i, j]:.2f}</td>"
            )
        html += "</tr>"
    html += "</table></div>"
    return html


def extract_row_as_matrix(A, i):
    return A[i : i + 1, :]


def extract_col_as_matrix(B, j):
    return B[:, j : j + 1]


def dot_terms(A, B, i, j):
    return [A[i, k] * B[k, j] for k in range(A.shape[1])]


def solve_order(step, rows, cols):
    solved = []
    for idx in range(step):
        r = idx // cols
        c = idx % cols
        if r < rows:
            solved.append((r, c))
    return solved


def make_matrix(rows, cols, low=-4, high=7):
    return np.random.randint(low, high, size=(rows, cols)).astype(float)


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
        st.error("Access denied. Inner dimensions do not match.")

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
    )
    solved = solve_order(step, out_rows, out_cols)
    partial = np.full_like(C, np.nan)
    for r, c in solved:
        partial[r, c] = C[r, c]
    shown = np.where(np.isnan(partial), 0.0, partial)

    if solved:
        i, j = solved[-1]
    else:
        i, j = 0, 0

    row_hi = [(i, k) for k in range(A.shape[1])]
    col_hi = [(k, j) for k in range(B.shape[0])]
    out_hi = solved

    left, mid, right = st.columns([1.25, 1.25, 1.1], vertical_alignment="top")
    with left:
        st.markdown(matrix_html(A, "Matrix A (row selected)", row_hi, "#22c55e"), unsafe_allow_html=True)
    with mid:
        st.markdown(matrix_html(B, "Matrix B (column selected)", col_hi, "#a78bfa"), unsafe_allow_html=True)
    with right:
        st.markdown(matrix_html(shown, "Output C = A @ B (partial)", out_hi, "#f59e0b"), unsafe_allow_html=True)

    if step == 0:
        st.info("Move the slider to start producing cells in C one by one.")
        return

    terms = dot_terms(A, B, i, j)
    expression = " + ".join([f"({A[i, k]:.2f}*{B[k, j]:.2f})" for k in range(A.shape[1])])
    st.success(
        f"Latest cell solved: C[{i+1},{j+1}] = row_{i+1}(A) · col_{j+1}(B) = "
        f"{expression} = {sum(terms):.2f}"
    )
    st.code("Rule: C[i, j] = Σ_k A[i, k] * B[k, j]", language="text")

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
        row_pick = st.selectbox("Pick output row", options=list(range(1, out_rows + 1)))
    with c2:
        col_pick = st.selectbox("Pick output column", options=list(range(1, out_cols + 1)))

    i = row_pick - 1
    j = col_pick - 1
    terms = dot_terms(A, B, i, j)

    st.markdown("### Dot Product Breakdown")
    for k, term in enumerate(terms, start=1):
        st.write(f"- Term {k}: A[{i+1},{k}] * B[{k},{j+1}] = {A[i, k-1]:.2f} * {B[k-1, j]:.2f} = {term:.2f}")
    st.info(f"Final value: C[{row_pick},{col_pick}] = {sum(terms):.2f}")

    with st.expander("Reveal full output matrix C"):
        st.write(np.round(C, 3))


def main():
    render_intro()
    st.sidebar.header("Matrix x Matrix Controls")

    m = st.sidebar.select_slider("Rows of A (m)", options=[2, 3, 4], value=3)
    n = st.sidebar.select_slider("Cols of A / Rows of B (n)", options=[2, 3, 4, 5], value=3)
    p = st.sidebar.select_slider("Cols of B (p)", options=[2, 3, 4], value=3)
    regen = st.sidebar.button("Generate new matrices")

    shape_key = (m, n, p)
    if "mxm_A" not in st.session_state or "mxm_shape" not in st.session_state:
        st.session_state.mxm_A = make_matrix(m, n)
        st.session_state.mxm_B = make_matrix(n, p)
        st.session_state.mxm_shape = shape_key

    if regen or st.session_state.mxm_shape != shape_key:
        st.session_state.mxm_A = make_matrix(m, n)
        st.session_state.mxm_B = make_matrix(n, p)
        st.session_state.mxm_shape = shape_key

    A = st.session_state.mxm_A
    B = st.session_state.mxm_B

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

