import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


st.set_page_config(page_title="Identity Matrix - The Perfect Do-Nothing Machine", layout="wide")


def matrix_html(matrix, title, highlight=None, color="#38bdf8", precision=1):
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


def render_vector_experiment(I):
    st.header("2) Vector Teleporter (That Goes Nowhere)")
    st.markdown("Pick a vector. Send it through `I`. Watch how nothing changes.")

    if I.shape[0] >= 2:
        c1, c2, c3 = st.columns(3)
        with c1:
            x = st.slider("v[1]", -8.0, 8.0, 3.0, 0.5)
        with c2:
            y = st.slider("v[2]", -8.0, 8.0, -2.0, 0.5)
        with c3:
            if I.shape[0] > 2:
                z = st.slider("v[3]", -8.0, 8.0, 1.5, 0.5)
            else:
                z = 0.0

        v = np.zeros(I.shape[0])
        v[0], v[1] = x, y
        if I.shape[0] > 2:
            v[2] = z
        transformed = I @ v

        left, right = st.columns([1.15, 1])
        with left:
            fig = draw_vector_lab(v[:2], transformed[:2])
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        with right:
            st.code(
                f"v        = {np.array2string(v, precision=1)}\n"
                f"I @ v    = {np.array2string(transformed, precision=1)}\n"
                f"v - I @ v= {np.array2string(v - transformed, precision=1)}",
                language="text",
            )
            if np.allclose(v, transformed):
                st.success("No change at all. Identity passes the vector untouched.")
    else:
        st.warning("Increase matrix size to at least 2 for the vector visual.")


def render_proof_panel(I):
    st.header("3) Why It Works (Row Dot Product View)")
    n = I.shape[0]
    st.markdown("Each output component is one row of `I` dotted with vector `v`.")

    row_pick = st.selectbox("Inspect row of I", options=list(range(1, n + 1)))
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

    terms = [f"{int(basis_row[j])}*v{j+1}" for j in range(n)]
    st.latex(rf"(Iv)_{{{row_pick}}} = " + " + ".join(terms))
    st.latex(rf"(Iv)_{{{row_pick}}} = v_{{{row_pick}}}")
    st.caption(
        f"Row {row_pick} has a single 1 at position {row_pick}, so it selects exactly v_{row_pick}."
    )


def render_no_change_score():
    st.header("4) Identity Scoreboard")
    st.markdown("How much does identity preserve the vector's properties?")
    fig = draw_radar([1, 1, 1, 1, 1])
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)
    st.success("Score: 100% unchanged. Identity is mathematically invisible.")


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
    n = st.sidebar.select_slider("Dimension of identity matrix", options=[2, 3, 4, 5, 6], value=3)
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
    render_vector_experiment(I)
    st.divider()
    render_proof_panel(I)
    st.divider()
    render_no_change_score()
    st.divider()
    render_recap()


if __name__ == "__main__":
    main()

