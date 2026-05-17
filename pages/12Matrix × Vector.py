
import numpy as np
import streamlit as st


st.set_page_config(page_title="Matrix x Vector", layout="wide")


def matrix_html(matrix, title, highlight=None, color="#38bdf8"):
    rows, cols = matrix.shape
    highlight = highlight or []
    html = f"""
    <div style="padding:12px;border:1px solid #334155;border-radius:12px;background:#0f172a22;">
      <h4 style="margin:0 0 8px 0;">{title}</h4>
      <table style="border-collapse:collapse;font-size:19px;">
    """
    for i in range(rows):
        html += "<tr>"
        for j in range(cols):
            bg = color if (i, j) in highlight else "transparent"
            html += (
                f"<td style='border:1px solid #475569;padding:8px 12px;text-align:center;"
                f"min-width:42px;background:{bg};'>{matrix[i, j]:.2f}</td>"
            )
        html += "</tr>"
    html += "</table></div>"
    return html


def vector_html(vector, title, highlight=None, color="#f97316"):
    highlight = highlight or []
    html = f"""
    <div style="padding:12px;border:1px solid #334155;border-radius:12px;background:#0f172a22;">
      <h4 style="margin:0 0 8px 0;">{title}</h4>
      <table style="border-collapse:collapse;font-size:19px;">
    """
    for i, value in enumerate(vector):
        bg = color if i in highlight else "transparent"
        html += (
            "<tr>"
            f"<td style='border:1px solid #475569;padding:8px 12px;text-align:center;"
            f"min-width:72px;background:{bg};'>{value:.2f}</td>"
            "</tr>"
        )
    html += "</table></div>"
    return html


def row_dot_product_steps(A, x, reveal_rows):
    y = A @ x
    shown = np.full_like(y, np.nan, dtype=float)
    for i in range(reveal_rows):
        shown[i] = y[i]
    return y, shown


def make_matrix(rows, cols):
    return np.random.randint(-4, 6, size=(rows, cols)).astype(float)


def make_vector(size):
    return np.random.randint(-4, 6, size=(size,)).astype(float)


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
    y = A @ x

    reveal_rows = st.slider(
        "Reveal output rows solved so far",
        min_value=0,
        max_value=rows,
        value=min(1, rows),
    )
    y_full, y_partial = row_dot_product_steps(A, x, reveal_rows)
    shown = np.where(np.isnan(y_partial), 0.0, y_partial)

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
        st.markdown(vector_html(shown, "Output Vector y = A x", hi, "#a78bfa"), unsafe_allow_html=True)

    if reveal_rows == 0:
        st.info("Move the slider to solve each output entry one row at a time.")
        return

    i = reveal_rows - 1
    terms = [f"({A[i, j]:.2f}*{x[j]:.2f})" for j in range(cols)]
    explanation = " + ".join(terms)
    st.success(
        f"Latest solved output: y[{i+1}] = row_{i+1}(A) · x = {explanation} = {y_full[i]:.2f}"
    )
    st.code("Rule: y_i = Σ_j A[i, j] * x[j]", language="text")

    with st.expander("See full multiplication result"):
        st.write("`y = A @ x`")
        st.write(np.round(y, 3))


def render_shape_story(A, x):
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

    rows = st.sidebar.select_slider("Rows in matrix A", options=[2, 3, 4, 5], value=3)
    cols = st.sidebar.select_slider("Columns in matrix A / size of x", options=[2, 3, 4, 5], value=3)
    regen = st.sidebar.button("Generate new A and x")

    if "mxv_A" not in st.session_state or "mxv_shape" not in st.session_state:
        st.session_state.mxv_A = make_matrix(rows, cols)
        st.session_state.mxv_x = make_vector(cols)
        st.session_state.mxv_shape = (rows, cols)

    if regen or st.session_state.mxv_shape != (rows, cols):
        st.session_state.mxv_A = make_matrix(rows, cols)
        st.session_state.mxv_x = make_vector(cols)
        st.session_state.mxv_shape = (rows, cols)

    A = st.session_state.mxv_A
    x = st.session_state.mxv_x

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
    render_shape_story(A, x)

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

