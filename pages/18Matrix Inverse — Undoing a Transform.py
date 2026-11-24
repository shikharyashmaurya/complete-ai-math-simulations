import functools
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from common import matrix_display  # noqa: E402
from common.linalg2d import det2, rotation_matrix, transform_points, unit_square  # noqa: E402
from common.nav import safe_page_link  # noqa: E402


st.set_page_config(page_title="Matrix Inverse — Undoing a Transform", layout="wide")

matrix_html = functools.partial(
    matrix_display.matrix_html, theme="slate", cell_style="plain", font_size=18, cell_padding="7px 14px", min_width=48
)


def rocket_shape():
    """A tiny asymmetric polygon so 'undo' is visibly nontrivial."""
    return np.array(
        [
            [0.0, 0.0],
            [0.35, 0.15],
            [0.2, 0.55],
            [0.5, 0.35],
            [0.55, 0.7],
            [0.25, 0.85],
            [0.0, 0.45],
            [0.0, 0.0],
        ],
        dtype=float,
    )


SINGULAR_TOL = 1e-8  # numerical tolerance: treat |det| below this as exactly 0
FRAGILE_DET = 0.05  # below this the inverse exists but has large entries


def try_inverse_2x2(M):
    d = det2(M)
    if abs(d) < SINGULAR_TOL:
        return None, d
    a, b = M[0, 0], M[0, 1]
    c, dd = M[1, 0], M[1, 1]
    inv = (1.0 / d) * np.array([[dd, -b], [-c, a]], dtype=float)
    return inv, d


def global_lim(*polys, pad=0.35):
    stack = np.vstack([p[:, :2] for p in polys if p.size])
    m = float(np.max(np.abs(stack))) if stack.size else 1.0
    return max(2.2, m + pad)


def style_axes(ax):
    ax.set_facecolor("#0f172a")
    ax.axhline(0, color="#64748b", linewidth=0.9)
    ax.axvline(0, color="#64748b", linewidth=0.9)
    ax.grid(alpha=0.2, color="#94a3b8", linestyle="--")
    ax.tick_params(colors="#cbd5e1")
    for spine in ax.spines.values():
        spine.set_color("#475569")


def draw_round_trip(M, Minv, shape_pts, show_ghost=True):
    """Three panels: original | after M | after M⁻¹ ∘ M (should match original)."""
    p0 = shape_pts.copy()
    p1 = transform_points(M, p0)
    p2 = transform_points(Minv, p1)

    lim = global_lim(p0, p1, p2)

    fig, axes = plt.subplots(1, 3, figsize=(14.2, 5.2))
    fig.patch.set_facecolor("#0b1020")

    specs = [
        ("1) Start", p0, "#38bdf8", "#0ea5e9", "Your shape lives here."),
        ("2) Apply M", p1, "#fb923c", "#ea580c", "Matrix M warps the plane."),
        ("3) Apply M⁻¹", p2, "#4ade80", "#16a34a", "Inverse sends you home."),
    ]

    for ax, (title, poly, fill, edge, caption) in zip(axes, specs):
        style_axes(ax)
        if show_ghost and title.startswith("2"):
            ax.fill(
                p0[:-1, 0],
                p0[:-1, 1],
                color="#334155",
                alpha=0.25,
                edgecolor="#64748b",
                linewidth=1.2,
                linestyle="--",
            )
        if show_ghost and title.startswith("3"):
            ax.fill(
                p1[:-1, 0],
                p1[:-1, 1],
                color="#7c2d12",
                alpha=0.18,
                edgecolor="#9a3412",
                linewidth=1.0,
                linestyle=":",
            )
        patch = mpatches.Polygon(
            poly[:, :2],
            closed=True,
            facecolor=fill,
            edgecolor=edge,
            linewidth=2.4,
            alpha=0.5,
        )
        ax.add_patch(patch)
        ax.plot(poly[:, 0], poly[:, 1], color=edge, lw=2.0)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_title(title, color="#f1f5f9", fontsize=12, pad=10)
        ax.text(0.02, 0.98, caption, transform=ax.transAxes, va="top", ha="left", color="#94a3b8", fontsize=9)

    err = float(np.max(np.abs(p2 - p0)))
    fig.suptitle(
        f"Round-trip error ‖M⁻¹(Mv) − v‖∞ = {err:.2e}  (floating-point dust)",
        color="#f8fafc",
        fontsize=13,
        fontweight="bold",
        y=1.03,
    )
    plt.tight_layout()
    return fig, err


def centroid(poly):
    """Mean of the vertices, ignoring the repeated closing vertex."""
    return poly[:-1].mean(axis=0)


def draw_rewind_arrow_story(M, Minv, shape_pts):
    """Single axes: shape → M → M⁻¹ as a comic strip with curved arrows."""
    p0 = shape_pts
    p1 = transform_points(M, p0)
    p2 = transform_points(Minv, p1)
    lim = global_lim(p0, p1, p2, pad=0.8)

    fig, ax = plt.subplots(figsize=(8.2, 7.0))
    fig.patch.set_facecolor("#0b1020")
    style_axes(ax)

    def draw_poly(poly, fc, ec, lw=2.0, alpha=0.45):
        ax.fill(poly[:-1, 0], poly[:-1, 1], fc=fc, ec=ec, lw=lw, alpha=alpha)
        ax.plot(poly[:, 0], poly[:, 1], color=ec, lw=lw - 0.2)

    draw_poly(p0, "#1e3a5f", "#38bdf8", alpha=0.35)
    draw_poly(p1, "#7c2d12", "#fb923c", alpha=0.4)
    draw_poly(p2, "#14532d", "#4ade80", lw=2.6, alpha=0.32)

    c0, c1, c2 = centroid(p0), centroid(p1), centroid(p2)
    ax.annotate(
        "",
        xy=(c1[0], c1[1]),
        xytext=(c0[0], c0[1]),
        arrowprops=dict(arrowstyle="->", color="#fbbf24", lw=2.2, connectionstyle="arc3,rad=0.25"),
    )
    ax.text(
        (c0[0] + c1[0]) / 2 + 0.15,
        (c0[1] + c1[1]) / 2 + 0.2,
        "M",
        color="#fde68a",
        fontsize=14,
        fontweight="bold",
    )

    ax.annotate(
        "",
        xy=(c2[0], c2[1]),
        xytext=(c1[0], c1[1]),
        arrowprops=dict(arrowstyle="->", color="#a78bfa", lw=2.2, connectionstyle="arc3,rad=-0.28"),
    )
    ax.text(
        (c1[0] + c2[0]) / 2 - 0.35,
        (c1[1] + c2[1]) / 2 - 0.15,
        "M⁻¹",
        color="#ddd6fe",
        fontsize=14,
        fontweight="bold",
    )

    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title("All three snapshots at once (like a rewind diagram)", color="#e2e8f0", fontsize=12, pad=12)
    plt.tight_layout()
    return fig


def draw_basis_round_trip(M, Minv):
    """Show standard basis arrows: M sends them out, M⁻¹ pulls them back."""
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.4))
    fig.patch.set_facecolor("#0b1020")

    e1 = np.array([1.0, 0.0])
    e2 = np.array([0.0, 1.0])
    u1, u2 = M @ e1, M @ e2
    lim = global_lim(
        np.vstack([[0, 0], e1, e2, u1, u2]),
        pad=0.5,
    )

    for ax, title in zip(axes, ["Forward: apply M", "Undo: apply M⁻¹"]):
        style_axes(ax)
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal", adjustable="box")
        ax.set_title(title, color="#e2e8f0", fontsize=12)

    ax_f, ax_b = axes

    ax_f.arrow(0, 0, e1[0], e1[1], color="#94a3b8", width=0.02, head_width=0.12, length_includes_head=True)
    ax_f.arrow(0, 0, e2[0], e2[1], color="#94a3b8", width=0.02, head_width=0.12, length_includes_head=True)
    ax_f.arrow(0, 0, u1[0], u1[1], color="#22c55e", width=0.025, head_width=0.14, length_includes_head=True)
    ax_f.arrow(0, 0, u2[0], u2[1], color="#a78bfa", width=0.025, head_width=0.14, length_includes_head=True)
    ax_f.text(e1[0] * 0.5, e1[1] * 0.5, "î", color="#cbd5e1", fontsize=11)
    ax_f.text(e2[0] * 0.5, e2[1] * 0.5, "ĵ", color="#cbd5e1", fontsize=11)
    ax_f.text(u1[0] * 0.52, u1[1] * 0.52, "Mî", color="#86efac", fontsize=10)
    ax_f.text(u2[0] * 0.52, u2[1] * 0.52, "Mĵ", color="#ddd6fe", fontsize=10)

    ax_b.arrow(0, 0, u1[0], u1[1], color="#22c55e", width=0.02, head_width=0.12, alpha=0.45, length_includes_head=True)
    ax_b.arrow(0, 0, u2[0], u2[1], color="#a78bfa", width=0.02, head_width=0.12, alpha=0.45, length_includes_head=True)
    b1, b2 = Minv @ u1, Minv @ u2
    ax_b.arrow(0, 0, b1[0], b1[1], color="#38bdf8", width=0.028, head_width=0.14, length_includes_head=True)
    ax_b.arrow(0, 0, b2[0], b2[1], color="#f472b6", width=0.028, head_width=0.14, length_includes_head=True)
    ax_b.text(b1[0] * 0.55, b1[1] * 0.55, "î again", color="#7dd3fc", fontsize=10, fontweight="bold")
    ax_b.text(b2[0] * 0.55, b2[1] * 0.55, "ĵ again", color="#fbcfe8", fontsize=10, fontweight="bold")

    plt.tight_layout()
    return fig


def preset_matrix(preset, wild_seed=18):
    if preset == "Identity (nothing to undo)":
        return np.eye(2)
    if preset == "Gentle zoom":
        return np.array([[1.35, 0.0], [0.0, 1.35]])
    if preset == "Shear + stretch":
        return np.array([[1.15, 0.75], [0.0, 0.9]])
    if preset == "Rotate 40°":
        return rotation_matrix(40.0)
    if preset == "Mirror-ish (det < 0)":
        return np.array([[0.9, 0.4], [0.5, -0.6]])
    if preset == "Wild card":
        rng = np.random.default_rng(wild_seed)
        base = rng.uniform(-1.1, 1.1, size=(2, 2))
        if abs(np.linalg.det(base)) < 0.2:
            base = base + 0.45 * np.eye(2)
        # Round to the sliders' 0.01 step so the sliders show exactly this matrix.
        return np.round(base, 2)
    return np.eye(2)


def render_playground():
    st.header("Lab controls")
    preset = st.radio(
        "Pick a transform vibe",
        [
            "Identity (nothing to undo)",
            "Gentle zoom",
            "Shear + stretch",
            "Rotate 40°",
            "Mirror-ish (det < 0)",
            "Wild card",
        ],
        horizontal=True,
        key="p18_preset_radio",
    )

    st.session_state.setdefault("p18_wild_seed", 18)
    reroll = False
    if preset == "Wild card":
        reroll = st.button("🎲 New wild card", key="p18_reroll")
        if reroll:
            st.session_state.p18_wild_seed += 1

    if reroll or st.session_state.get("p18_preset") != preset:
        base = preset_matrix(preset, st.session_state.p18_wild_seed)
        st.session_state.p18_preset = preset
        for k, v in zip(("p18_a", "p18_b", "p18_c", "p18_d"), base.ravel()):
            st.session_state[k] = float(v)

    st.markdown("Fine-tune entries (switching preset refreshes defaults):")
    r1c1, r1c2, r2c1, r2c2 = st.columns(4)
    with r1c1:
        a = st.slider("a", -3.0, 3.0, key="p18_a")
    with r1c2:
        b = st.slider("b", -3.0, 3.0, key="p18_b")
    with r2c1:
        c = st.slider("c", -3.0, 3.0, key="p18_c")
    with r2c2:
        d = st.slider("d", -3.0, 3.0, key="p18_d")

    return np.array([[a, b], [c, d]], dtype=float)


def render_intro():
    st.title("Page 18: Matrix Inverse — The Great Undo")
    st.markdown(
        """
        Think of a matrix **M** as a **space machine**: every point gets teleported somewhere else.

        The **inverse** `M⁻¹` is the **rewind button** — *if it exists*:

        > Apply **M**, then apply **M⁻¹**, and you are back where you started.  
        > Same story the other way: `M @ M⁻¹ = I` and `M⁻¹ @ M = I`.

        This page is basically **Ctrl+Z** for linear transformations — with pictures.
        """
    )
    st.latex(r"M^{-1} M = I \quad\text{and}\quad M M^{-1} = I")


def render_singular_crisis(M):
    st.error(
        f"**No inverse today.** det(M) = 0 (|det| < {SINGULAR_TOL:g}, our floating-point tolerance), so the machine squashes 2D "
        "into a line (or a point). "
        "Many different starting points crash into the same output — so there is no unique 'undo' map."
    )
    d = det2(M)
    st.metric("det(M)", f"{d:.2e}")
    fig, ax = plt.subplots(figsize=(6.5, 6.0))
    fig.patch.set_facecolor("#0b1020")
    style_axes(ax)
    sq = unit_square()
    squashed = transform_points(M, sq)
    ax.fill(squashed[:-1, 0], squashed[:-1, 1], color="#450a0a", ec="#f87171", lw=2, alpha=0.55)
    ax.plot(squashed[:, 0], squashed[:, 1], color="#fca5a5", lw=2)
    lim = global_lim(squashed)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title("Unit square after M — collapsed ribbon", color="#fecaca", fontsize=12)
    st.pyplot(fig, width="stretch")
    plt.close(fig)


def main():
    render_intro()

    st.sidebar.header("Inverse rewind booth")
    st.sidebar.markdown(
        """
        **Try this:**
        - Pick a vibe, then torture the sliders.
        - Watch panel 3 snap back onto panel 1.
        - Slide `det(M)` toward 0 and feel the **undo** disappear.
        """
    )

    M = render_playground()
    st.divider()

    Minv, d = try_inverse_2x2(M)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("det(M)", f"{d:.4f}")
    with c2:
        if Minv is None:
            st.metric("M⁻¹ exists?", "No")
        else:
            st.metric("M⁻¹ exists?", "Yes")
    with c3:
        if Minv is not None:
            chk = M @ Minv
            off = float(np.max(np.abs(chk - np.eye(2))))
            st.metric("max |M·M⁻¹ − I| (entrywise)", f"{off:.1e}")

    if Minv is None:
        render_singular_crisis(M)
        st.stop()

    if abs(d) < FRAGILE_DET:
        st.warning(
            f"**Fragile undo.** |det(M)| = {abs(d):.4f} is tiny, so M⁻¹ has huge entries "
            f"(largest = {np.max(np.abs(Minv)):.1f}, condition number ≈ {np.linalg.cond(M):.0f}). "
            "The inverse exists mathematically, but small errors in Mv get magnified enormously on the way back."
        )

    st.subheader("Matrices side by side")
    mc1, mc2 = st.columns(2)
    with mc1:
        st.markdown(matrix_html(M, "M — the warp"), unsafe_allow_html=True)
    with mc2:
        st.markdown(matrix_html(Minv, "M⁻¹ — the rewind"), unsafe_allow_html=True)

    st.markdown(
        f"""
        **2×2 cheat sheet** (same as you would derive from `M M⁻¹ = I`):

        - `det(M) = ad − bc = {d:.5f}`
        - `M⁻¹ = (1/det) × [[d, −b], [−c, a]]`
        """
    )

    shape_choice = st.radio("Shape to warp", ["Unit square", "Little rocket (asymmetric)"], horizontal=True, key="p18_shape")
    shape_pts = unit_square() if shape_choice == "Unit square" else rocket_shape()

    st.header("1) Three-frame story")
    ghost = st.checkbox("Show faint ghosts (before vs after)", value=True, key="p18_ghost")
    fig1, _ = draw_round_trip(M, Minv, shape_pts, show_ghost=ghost)
    st.pyplot(fig1, width="stretch")
    plt.close(fig1)

    st.header("2) Comic-strip rewind (everything overlaid)")
    st.caption("Blue = start, orange = after M, green = after M⁻¹ — green should hug blue.")
    fig2 = draw_rewind_arrow_story(M, Minv, shape_pts)
    st.pyplot(fig2, width="stretch")
    plt.close(fig2)

    st.header("3) Basis arrows — machines are fully defined by where î and ĵ land")
    fig3 = draw_basis_round_trip(M, Minv)
    st.pyplot(fig3, width="stretch")
    plt.close(fig3)

    st.markdown(
        """
        ---
        ### Recap
        - **Inverse = undo** for an invertible linear map: `M⁻¹(Mv) = v`.
        - You only get an inverse when **det(M) ≠ 0** — otherwise information is crushed and rewinds are ambiguous.
        - Neural nets do not literally invert huge matrices for fun — but **solving** `Ax = b` and **change-of-basis** thinking
          are the same family of idea: *find the linear operation that reverses another one (when possible)*.

        **Next up:** *Span, Basis & Rank* — when det(M) = 0, which directions survive, and how many?
        """
    )
    safe_page_link("pages/76Span, Basis & Rank.py", "Next: 76 · Span, Basis & Rank", icon="➡️")


if __name__ == "__main__":
    main()

