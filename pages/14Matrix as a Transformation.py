import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


st.set_page_config(page_title="Matrix as a Transformation", layout="wide")


def rotation_matrix(theta_deg):
    t = np.deg2rad(theta_deg)
    return np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]], dtype=float)


def transform_points(M, points):
    return (M @ points.T).T


def unit_square():
    return np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]], dtype=float)


def matrix_html(M, title, precision=2):
    html = f"""
    <div style="padding:12px;border:1px solid #334155;border-radius:12px;background:#0f172a22;margin-bottom:12px;">
      <h4 style="margin:0 0 8px 0;color:#e2e8f0;">{title}</h4>
      <table style="border-collapse:collapse;font-size:18px;color:#f8fafc;">
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


def preset_matrix(preset):
    if preset == "Identity (no change)":
        return np.eye(2)
    if preset == "Rotation 45°":
        t = np.deg2rad(45.0)
        return np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
    if preset == "Stretch X, Squash Y":
        return np.array([[1.5, 0.0], [0.0, 0.5]])
    if preset == "Shear X":
        return np.array([[1.0, 1.0], [0.0, 1.0]])
    if preset == "Reflection (y = x)":
        return np.array([[0.0, 1.0], [1.0, 0.0]])
    if preset == "Collapse to line (Singular)":
        return np.array([[1.0, 1.0], [1.0, 1.0]])
    return np.eye(2)


def draw_scene(M, grid_limit=5, density=1):
    fig, ax = plt.subplots(figsize=(8.0, 8.0))
    fig.patch.set_facecolor("#0b1020")
    ax.set_facecolor("#0f172a")

    # Original grid
    for x in np.arange(-grid_limit, grid_limit + 0.01, density):
        ax.plot([x, x], [-grid_limit, grid_limit], color="#334155", lw=0.8, alpha=0.5)
        ax.plot([-grid_limit, grid_limit], [x, x], color="#334155", lw=0.8, alpha=0.5)

    # Transformed grid
    for x in np.arange(-grid_limit, grid_limit + 0.01, density):
        yvals = np.array([-grid_limit, grid_limit], dtype=float)
        pts_v = np.column_stack([np.full_like(yvals, x), yvals])
        t_pts_v = transform_points(M, pts_v)
        ax.plot(t_pts_v[:, 0], t_pts_v[:, 1], color="#0ea5e9", lw=1.2, alpha=0.4)

        xvals = np.array([-grid_limit, grid_limit], dtype=float)
        pts_h = np.column_stack([xvals, np.full_like(xvals, x)])
        t_pts_h = transform_points(M, pts_h)
        ax.plot(t_pts_h[:, 0], t_pts_h[:, 1], color="#0ea5e9", lw=1.2, alpha=0.4)

    # Unit Square Original
    sq = unit_square()
    ax.fill(sq[:, 0], sq[:, 1], color="#1e3a5f", alpha=0.4, edgecolor="#38bdf8", lw=1.5)
    
    # Unit Square Transformed
    t_sq = transform_points(M, sq)
    ax.fill(t_sq[:, 0], t_sq[:, 1], color="#7c2d12", alpha=0.6, edgecolor="#fb923c", lw=2.0)

    # Basis vectors Original
    e1 = np.array([1.0, 0.0])
    e2 = np.array([0.0, 1.0])
    ax.arrow(0, 0, e1[0], e1[1], color="#94a3b8", width=0.03, head_width=0.15, length_includes_head=True, alpha=0.8)
    ax.arrow(0, 0, e2[0], e2[1], color="#94a3b8", width=0.03, head_width=0.15, length_includes_head=True, alpha=0.8)
    
    # Basis vectors Transformed
    te1 = M @ e1
    te2 = M @ e2
    ax.arrow(0, 0, te1[0], te1[1], color="#22c55e", width=0.04, head_width=0.2, length_includes_head=True)
    ax.arrow(0, 0, te2[0], te2[1], color="#a78bfa", width=0.04, head_width=0.2, length_includes_head=True)

    ax.axhline(0, color="#64748b", lw=1.2)
    ax.axvline(0, color="#64748b", lw=1.2)
    
    # Limits logic
    raw_vals = np.array([
        [grid_limit, grid_limit],
        [grid_limit, -grid_limit],
        [-grid_limit, grid_limit],
        [-grid_limit, -grid_limit],
    ], dtype=float)
    transformed_corners = transform_points(M, raw_vals)
    max_abs = max(grid_limit, float(np.max(np.abs(transformed_corners))) + 1.5)
    lim = min(20.0, max_abs + 1.0)
    
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(False)
    
    for spine in ax.spines.values():
        spine.set_color("#475569")
    ax.tick_params(colors="#cbd5e1")
    ax.set_title("Space-Time Grid Warp", color="#f8fafc", fontsize=14, pad=15)
    
    return fig


def render_intro():
    st.title("Page 14: Matrix as a Transformation")
    st.markdown(
        """
        Welcome to the **Space-Time Grid Warp Station**.

        **A Matrix is a Transformation of Space**
        Instead of thinking of a matrix as just a grid of numbers, think of it as a set of instructions that morphs the entire plane. 
        When you multiply a vector by a matrix, you are teleporting that point to a new location: `x_new = M @ x`.
        
        The columns of a 2x2 matrix tell you exactly where the standard basis vectors (î and ĵ) land. Because the transformation is **linear**, grid lines remain straight and parallel, and the origin stays fixed. Once you know where î and ĵ land, the rest of the grid follows along!

        Use controls to rotate, stretch, squash, and shear the world below.
        """
    )


def render_legend():
    st.markdown(
        """
        **Map Legend**  
        🟦 **Original Space**: Gray grid, gray arrows (î, ĵ), blue unit square.  
        🟧 **Transformed Space**: Cyan grid, Green (Mî) & Purple (Mĵ) arrows, orange parallelogram.  
        """
    )


def render_matrix_card(M):
    st.markdown(matrix_html(M, "Current Matrix M"), unsafe_allow_html=True)
    det = float(np.linalg.det(M))
    area_text = "flips orientation + scales area" if det < 0 else "scales area"
    st.info(f"**det(M) = {det:.3f}**  \n\n{area_text} by |det| = {abs(det):.3f}")
    if abs(det) < 1e-6:
        st.warning("det(M) is near 0: space squashed into a lower dimension!")


def render_playground():
    st.header("1) Transformation Controls")
    
    mode = st.radio(
        "Build matrix from:",
        ["Geometric Controls (Rotate, Scale, Shear)", "Direct Entries (2x2)"],
        horizontal=True
    )
    
    if mode == "Geometric Controls (Rotate, Scale, Shear)":
        st.markdown("Build your matrix by combining fundamental transformations.")
        geom_mode = st.radio(
            "Transformation Type:",
            ["Combo (All)", "Rotation Only", "Scale Only", "Shear Only"],
            horizontal=True
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            angle = st.slider("Rotation (deg)", -180, 180, 30, 5, disabled=(geom_mode not in ["Combo (All)", "Rotation Only"]))
        with col2:
            sx = st.slider("Scale X", -3.0, 3.0, 1.2, 0.1, disabled=(geom_mode not in ["Combo (All)", "Scale Only"]))
            sy = st.slider("Scale Y", -3.0, 3.0, 0.8, 0.1, disabled=(geom_mode not in ["Combo (All)", "Scale Only"]))
        with col3:
            shx = st.slider("Shear X", -2.0, 2.0, 0.6, 0.1, disabled=(geom_mode not in ["Combo (All)", "Shear Only"]))
            shy = st.slider("Shear Y", -2.0, 2.0, 0.2, 0.1, disabled=(geom_mode not in ["Combo (All)", "Shear Only"]))

        r = rotation_matrix(angle) if geom_mode in ["Combo (All)", "Rotation Only"] else np.eye(2)
        s = np.array([[sx, 0.0], [0.0, sy]], dtype=float) if geom_mode in ["Combo (All)", "Scale Only"] else np.eye(2)
        h = np.array([[1.0, shx], [shy, 1.0]], dtype=float) if geom_mode in ["Combo (All)", "Shear Only"] else np.eye(2)
        
        M = h @ r @ s
    else:
        preset = st.radio(
            "Quick Vibe",
            ["Identity (no change)", "Rotation 45°", "Stretch X, Squash Y", "Shear X", "Reflection (y = x)", "Collapse to line (Singular)"],
            horizontal=True
        )
        base = preset_matrix(preset)
        
        if "d14_preset" not in st.session_state:
            st.session_state.d14_preset = preset
            st.session_state.d14_a = float(base[0, 0])
            st.session_state.d14_b = float(base[0, 1])
            st.session_state.d14_c = float(base[1, 0])
            st.session_state.d14_d = float(base[1, 1])

        if preset != st.session_state.d14_preset:
            st.session_state.d14_preset = preset
            st.session_state.d14_a = float(base[0, 0])
            st.session_state.d14_b = float(base[0, 1])
            st.session_state.d14_c = float(base[1, 0])
            st.session_state.d14_d = float(base[1, 1])
            
        r1c1, r1c2, r2c1, r2c2 = st.columns(4)
        with r1c1:
            a = st.slider("a (top-left)", -3.0, 3.0, key="d14_a")
        with r1c2:
            b = st.slider("b (top-right)", -3.0, 3.0, key="d14_b")
        with r2c1:
            c = st.slider("c (bottom-left)", -3.0, 3.0, key="d14_c")
        with r2c2:
            d = st.slider("d (bottom-right)", -3.0, 3.0, key="d14_d")
            
        M = np.array([[a, b], [c, d]], dtype=float)
        
    return M


def render_point_mission(M):
    st.header("2) Coordinate Teleporter Mission")
    st.markdown("Pick any point. Watch where the matrix sends it.")
    
    c1, c2, c3 = st.columns([1, 1, 1.5])
    with c1:
        px = st.slider("Point x", -5.0, 5.0, 2.0, 0.5)
    with c2:
        py = st.slider("Point y", -5.0, 5.0, 1.0, 0.5)
        
    p = np.array([px, py], dtype=float)
    p2 = M @ p
    
    with c3:
        st.markdown(
            f"""
            <div style="padding:15px;background:#0f172a;border-radius:10px;border:1px solid #334155;">
                <div style="color:#94a3b8;font-size:14px;margin-bottom:5px;">Transformed Point (x', y')</div>
                <div style="color:#38bdf8;font-size:24px;font-weight:bold;">({p2[0]:.2f}, {p2[1]:.2f})</div>
            </div>
            """, unsafe_allow_html=True
        )

    st.latex(rf"\begin{{bmatrix}} {M[0,0]:.2f} & {M[0,1]:.2f} \\ {M[1,0]:.2f} & {M[1,1]:.2f} \end{{bmatrix}} \begin{{bmatrix}} {px:.2f} \\ {py:.2f} \end{{bmatrix}} = \begin{{bmatrix}} {p2[0]:.2f} \\ {p2[1]:.2f} \end{{bmatrix}}")


def main():
    render_intro()
    
    st.sidebar.header("Transformation Lab")
    st.sidebar.markdown(
        """
        **Mission:** Grasp the grid!
        - Switch between Geometric and Direct Matrix controls.
        - Watch how basis vectors (î, ĵ) define the whole grid.
        """
    )
    
    M = render_playground()
    
    st.divider()
    
    col1, col2 = st.columns([1.5, 1.0], gap="large")
    with col1:
        fig = draw_scene(M, grid_limit=5, density=1)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    with col2:
        render_matrix_card(M)
        st.markdown("<br>", unsafe_allow_html=True)
        render_legend()
        
    st.divider()
    render_point_mission(M)
    st.divider()
    
    st.markdown(
        """
        ### Recap
        - A `2x2` matrix transforms the entire plane, not just one point.
        - Columns of `M` are exactly where the basis vectors (î, ĵ) land.
        - `det(M)` tells you the area scaling factor.
        - This is the fundamental math powering computer graphics and neural network layers.
        """
    )


if __name__ == "__main__":
    main()
