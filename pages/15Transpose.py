import numpy as np
import streamlit as st


st.set_page_config(page_title="Transpose - Rows Become Columns", layout="wide")


def make_matrix(rows, cols, low=-9, high=10):
    return np.random.randint(low, high, size=(rows, cols)).astype(float)


def matrix_html(matrix, title, highlight=None, color="#22d3ee", precision=1):
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
                f"min-width:42px;background:{bg};'>{matrix[i, j]:.{precision}f}</td>"
            )
        html += "</tr>"
    html += "</table></div>"
    return html


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
    row_idx = st.selectbox("Pick a row from A", options=list(range(1, A.shape[0] + 1)))
    i = row_idx - 1

    row_vals = A[i, :]
    col_vals = AT[:, i]

    left, right = st.columns(2)
    with left:
        highlights = [(i, j) for j in range(A.shape[1])]
        st.markdown(matrix_html(A, f"A (highlight row {row_idx})", highlights, "#22c55e"), unsafe_allow_html=True)
    with right:
        highlights_t = [(j, i) for j in range(AT.shape[0])]
        st.markdown(
            matrix_html(AT, f"A^T (matching column {row_idx})", highlights_t, "#a78bfa"),
            unsafe_allow_html=True,
        )

    st.code(
        f"Row {row_idx} in A  = {np.array2string(row_vals, precision=1)}\n"
        f"Col {row_idx} in A^T = {np.array2string(col_vals, precision=1)}",
        language="text",
    )
    if np.allclose(row_vals, col_vals):
        st.success("Perfect match. That is exactly what transpose does.")


def render_index_explorer(A):
    st.header("3) Index Explorer: (i, j) -> (j, i)")
    AT = A.T
    c1, c2 = st.columns(2)
    with c1:
        i = st.number_input("Pick i (row in A)", min_value=1, max_value=A.shape[0], value=1, step=1)
    with c2:
        j = st.number_input("Pick j (col in A)", min_value=1, max_value=A.shape[1], value=1, step=1)
    i0, j0 = int(i - 1), int(j - 1)

    val = A[i0, j0]
    trans_val = AT[j0, i0]

    st.latex(rf"A_{{{int(i)},{int(j)}}} = {val:.0f} \quad \Rightarrow \quad (A^T)_{{{int(j)},{int(i)}}} = {trans_val:.0f}")
    if abs(val - trans_val) < 1e-9:
        st.success("Value preserved, only its address changed.")
    else:
        st.error("Something is off. This should not happen.")


def main():
    render_intro()

    st.sidebar.header("Transpose Controls")
    rows = st.sidebar.select_slider("Rows in A", options=[2, 3, 4, 5], value=3)
    cols = st.sidebar.select_slider("Cols in A", options=[2, 3, 4, 5], value=4)
    regen = st.sidebar.button("Generate new matrix")

    shape_key = (rows, cols)
    if "transpose_A" not in st.session_state or "transpose_shape" not in st.session_state:
        st.session_state.transpose_A = make_matrix(rows, cols)
        st.session_state.transpose_shape = shape_key

    if regen or st.session_state.transpose_shape != shape_key:
        st.session_state.transpose_A = make_matrix(rows, cols)
        st.session_state.transpose_shape = shape_key

    A = st.session_state.transpose_A
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

