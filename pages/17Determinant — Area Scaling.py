import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import streamlit as st


st.set_page_config(page_title="Determinant — Area Scaling", layout="wide")


def det2(M):
    return float(M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0])


def polygon_area(verts):
    """Shoelace formula; verts (n,2) closed or open."""
    x = verts[:, 0]
    y = verts[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


def unit_square():
    return np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]], dtype=float)


def transform_points(M, pts):
    return (M @ pts[:, :2].T).T


def matrix_html(M, title, precision=2):
    html = f"""
    <div style="padding:12px;border:1px solid #334155;border-radius:12px;background:#0f172a22;">
      <h4 style="margin:0 0 8px 0;">{title}</h4>
      <table style="border-collapse:collapse;font-size:18px;">
    """
    for i in range(2):
        html += "<tr>"
        for j in range(2):
            html += (
                f"<td style='border:1px solid #475569;padding:7px 14px;text-align:center;"
                f"min-width:48px;'>{M[i, j]:.{precision}f}</td>"
            )
        html += "</tr>"
    html += "</table></div>"
    return html


def draw_determinant_story(M, show_grid=True):
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.8))
    fig.patch.set_facecolor("#0b1020")

    sq_closed = unit_square()
    par = transform_points(M, sq_closed)

    d = det2(M)
    abs_area = polygon_area(par[:-1])

    lim = max(3.0, float(np.max(np.abs(par))) * 1.35 + 0.5)

    for ax, title, poly, fill_color, edge_color in zip(
        axes,
        ["Before: the unit square (area = 1)", "After: the parallelogram"],
        [sq_closed, par],
        ["#1e3a5f", "#7c2d12" if d < 0 else "#14532d"],
        ["#38bdf8", "#fb923c" if d < 0 else "#4ade80"],
    ):
        ax.set_facecolor("#0f172a")
        ax.axhline(0, color="#64748b", linewidth=0.9)
        ax.axvline(0, color="#64748b", linewidth=0.9)
        if show_grid:
            ax.grid(alpha=0.22, color="#94a3b8", linestyle="--")
        patch = mpatches.Polygon(
            poly[:, :2],
            closed=True,
            facecolor=fill_color,
            edgecolor=edge_color,
            linewidth=2.4,
            alpha=0.55,
        )
        ax.add_patch(patch)
        ax.plot(poly[:, 0], poly[:, 1], color=edge_color, lw=2.2)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlim(-0.15, lim)
        ax.set_ylim(-0.15, lim)
        ax.set_title(title, color="#e2e8f0", fontsize=12, pad=10)
        ax.tick_params(colors="#cbd5e1")
        for spine in ax.spines.values():
            spine.set_color("#475569")

    ax0, ax1 = axes
    ax0.annotate(
        "1×1 tile\n(area 1)",
        xy=(0.5, 0.5),
        ha="center",
        va="center",
        color="#bae6fd",
        fontsize=11,
        fontweight="bold",
    )

    c1, c2 = M[:, 0], M[:, 1]
    ax1.arrow(0, 0, c1[0], c1[1], color="#22c55e", width=0.02, length_includes_head=True, head_width=0.12)
    ax1.arrow(0, 0, c2[0], c2[1], color="#a78bfa", width=0.02, length_includes_head=True, head_width=0.12)
    ax1.text(c1[0] * 0.55, c1[1] * 0.55, "col 1", color="#86efac", fontsize=10)
    ax1.text(c2[0] * 0.55, c2[1] * 0.55, "col 2", color="#ddd6fe", fontsize=10)

    sign_note = " (orientation flipped!)" if d < 0 else ""
    fig.suptitle(
        f"Determinant det(M) = {d:.3f}  →  |area| = {abs_area:.3f}{sign_note}",
        color="#f8fafc",
        fontsize=14,
        fontweight="bold",
        y=1.02,
    )
    plt.tight_layout()
    return fig, d, abs_area


def draw_column_vectors(M):
    fig, ax = plt.subplots(figsize=(5.2, 5.2))
    fig.patch.set_facecolor("#0b1020")
    ax.set_facecolor("#0f172a")
    lim = max(3.0, float(np.max(np.abs(M))) * 1.4 + 0.4)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.axhline(0, color="#64748b", lw=0.9)
    ax.axvline(0, color="#64748b", lw=0.9)
    ax.grid(alpha=0.2, color="#94a3b8", linestyle="--")

    u, v = M[:, 0], M[:, 1]
    ax.arrow(0, 0, u[0], u[1], color="#22c55e", width=0.025, length_includes_head=True, head_width=0.14)
    ax.arrow(0, 0, v[0], v[1], color="#a78bfa", width=0.025, length_includes_head=True, head_width=0.14)

    par = transform_points(M, unit_square())
    ax.fill(par[:-1, 0], par[:-1, 1], color="#f59e0b", alpha=0.25, edgecolor="#fbbf24", linewidth=2)
    ax.set_title("Columns span the parallelogram", color="#e2e8f0", fontsize=11)
    ax.set_aspect("equal", adjustable="box")
    ax.tick_params(colors="#cbd5e1")
    for spine in ax.spines.values():
        spine.set_color("#475569")
    plt.tight_layout()
    return fig


def render_intro():
    st.title("Page 17: Determinant — The Space Accountant")
    st.markdown(
        """
        Every **2×2 matrix** is a flatland machine: it stretches, shears, rotates, and sometimes **flips** the plane.

        Here is the secret headline:

        > **The determinant is how much area the machine multiplies by** — starting from the humble **unit square** (area = 1)
        > and watching it become a **parallelogram** whose area is **|det(M)|**.

        If the determinant is **negative**, the shape still has the same size — but the **orientation** is reversed
        (like looking in a mirror). That is why we keep the **sign** in `det(M)` and use **absolute value** for raw area.
        """
    )
    st.latex(r"\det\begin{pmatrix} a & b \\ c & d \end{pmatrix} = ad - bc")


def render_main_lab(M):
    st.header("1) Unit square → parallelogram")
    st.markdown(
        "The columns of `M` are where the basis arrows land. They **span** the output shape — "
        "so the area of that parallelogram is exactly what the determinant measures (up to sign)."
    )
    fig, d, abs_area = draw_determinant_story(M, show_grid=st.checkbox("Show light grid", value=True))
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("det(M) (signed)", f"{d:.4f}")
    with c2:
        st.metric("|det(M)|", f"{abs(d):.4f}")
    with c3:
        if abs(d) < 1e-9:
            st.metric("Story", "Collapsed!")
        elif d < 0:
            st.metric("Story", "Flipped space")
        else:
            st.metric("Story", "Pure stretch/shear")

    st.caption(
        f"Shoelace area of transformed polygon ≈ {abs_area:.6f} — matches |det| = {abs(d):.6f} "
        "(numerical check)."
    )


def render_recipe(M):
    st.header("2) Recipe bar: ad − bc")
    a, b, c, d = M[0, 0], M[0, 1], M[1, 0], M[1, 1]
    st.markdown(matrix_html(M, "Your matrix M"), unsafe_allow_html=True)
    st.markdown(
        f"""
        - **a × d** = `{a:.3f}` × `{d:.3f}` = **{a * d:.5f}**
        - **b × c** = `{b:.3f}` × `{c:.3f}` = **{b * c:.5f}**
        - **det** = {a * d:.5f} − {b * c:.5f} = **{det2(M):.5f}**
        """
    )


def render_vector_view(M):
    st.header("3) Column picture")
    col_left, col_right = st.columns([1.1, 1])
    with col_left:
        fig = draw_column_vectors(M)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    with col_right:
        st.markdown(
            """
            **Green** = first column (where `î` went).  
            **Purple** = second column (where `ĵ` went).

            The **unit square** becomes the parallelogram built from those two edges meeting at the origin.
            """
        )


def preset_matrix(preset):
    if preset == "Identity (no change)":
        return np.eye(2)
    if preset == "Uniform zoom":
        return np.array([[1.6, 0.0], [0.0, 1.6]])
    if preset == "Squeeze one axis":
        return np.array([[2.2, 0.0], [0.0, 0.45]])
    if preset == "Shear (book on a desk)":
        return np.array([[1.0, 0.9], [0.0, 1.0]])
    if preset == "Rotate 25°":
        t = np.deg2rad(25.0)
        return np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
    if preset == "Mirror world (flip)":
        return np.array([[1.0, 0.2], [0.6, -0.4]])
    if preset == "Near-singular (almost flat)":
        return np.array([[1.0, 0.95], [0.95, 0.9025]])
    rng = np.random.default_rng(17)
    base = rng.uniform(-1.2, 1.2, size=(2, 2))
    if abs(np.linalg.det(base)) < 0.15:
        base = base + 0.35 * np.eye(2)
    return base


def render_playground():
    st.header("4) Playground — presets + fine tuning")

    preset = st.radio(
        "Quick vibe",
        [
            "Identity (no change)",
            "Uniform zoom",
            "Squeeze one axis",
            "Shear (book on a desk)",
            "Rotate 25°",
            "Mirror world (flip)",
            "Near-singular (almost flat)",
            "Wild card",
        ],
        horizontal=True,
    )

    base = preset_matrix(preset)

    if "d17_preset" not in st.session_state:
        st.session_state.d17_preset = preset
        st.session_state.d17_a = float(base[0, 0])
        st.session_state.d17_b = float(base[0, 1])
        st.session_state.d17_c = float(base[1, 0])
        st.session_state.d17_d = float(base[1, 1])

    if preset != st.session_state.d17_preset:
        st.session_state.d17_preset = preset
        st.session_state.d17_a = float(base[0, 0])
        st.session_state.d17_b = float(base[0, 1])
        st.session_state.d17_c = float(base[1, 0])
        st.session_state.d17_d = float(base[1, 1])

    st.markdown("Tweak entries (preset above writes new defaults when you switch):")
    r1c1, r1c2, r2c1, r2c2 = st.columns(4)
    with r1c1:
        a = st.slider("a (top-left)", -3.0, 3.0, key="d17_a")
    with r1c2:
        b = st.slider("b (top-right)", -3.0, 3.0, key="d17_b")
    with r2c1:
        c = st.slider("c (bottom-left)", -3.0, 3.0, key="d17_c")
    with r2c2:
        d = st.slider("d (bottom-right)", -3.0, 3.0, key="d17_d")

    M = np.array(
        [[st.session_state.d17_a, st.session_state.d17_b], [st.session_state.d17_c, st.session_state.d17_d]],
        dtype=float,
    )
    return M


def render_trivia_challenge():
    st.header("5) Micro-challenge")
    st.markdown("Without touching sliders: if you **double both columns**, what happens to the area?")
    choice = st.selectbox(
        "Pick one",
        ["It doubles", "It stays 1", "It quadruples", "It becomes zero"],
        index=0,
    )
    if st.button("Reveal answer"):
        if choice == "It quadruples":
            st.success("Yes — each side doubles, so area scales like 2×2 = 4. Determinant scales the same way.")
        else:
            st.info(
                "Answer: **It quadruples.** Scaling the whole matrix by k multiplies det by k² in 2D — "
                "so doubling both columns (equivalently M → 2M) multiplies det by 4."
            )


def render_recap():
    st.markdown(
        """
        ---
        ### Recap
        - Start with the **unit square** (area 1). After `M`, it becomes a **parallelogram**.
        - **|det(M)|** is exactly the **area** of that parallelogram — the factor by which area scales.
        - **sign(det)** tells you whether orientation is preserved (**+**) or flipped (**−**).
        - **det = 0** means the parallelogram collapses to a line: the transform **squashes** 2D area to nothing.
        """
    )


def main():
    render_intro()
    st.sidebar.header("Determinant lab")
    st.sidebar.markdown(
        """
        **Mission:** watch area breathe.

        - Drag matrix entries in section 4.
        - Try a **negative** determinant and notice the **mirror** tint.
        - Slide toward **singular** to see the world **collapse** to a line.
        """
    )

    M = render_playground()
    st.divider()
    render_main_lab(M)
    st.divider()
    render_recipe(M)
    st.divider()
    render_vector_view(M)
    st.divider()
    render_trivia_challenge()
    render_recap()


if __name__ == "__main__":
    main()

