"""
Page 21 — Why non-linearity?
Motivation: some patterns cannot be sliced by a single straight line (classification view).
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import streamlit as st


st.set_page_config(page_title="Why Non-linearity?", layout="wide")

BG = "#0b1020"
PANEL = "#0f172a"
INK = "#e2e8f0"
MUTED = "#94a3b8"
ACC_A = "#38bdf8"
ACC_B = "#f472b6"
ACC_LINE = "#fbbf24"
ACC_BAD = "#fb7185"
ACC_GOOD = "#4ade80"


def _style_axes(ax) -> None:
    ax.set_facecolor(PANEL)
    ax.tick_params(colors=MUTED)
    for spine in ax.spines.values():
        spine.set_color("#475569")
    ax.grid(alpha=0.22, color="#64748b", linestyle="--")


def xor_dataset() -> tuple[np.ndarray, np.ndarray]:
    X = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]], dtype=float)
    y = np.array([-1.0, 1.0, 1.0, -1.0], dtype=float)
    return X, y


def ring_dataset(rng: np.random.Generator, n_each: int = 140) -> tuple[np.ndarray, np.ndarray]:
    """Inner blob (+1) vs outer ring (-1) — no single line separates both classes."""
    t_in = rng.uniform(0.0, 2.0 * np.pi, size=n_each)
    r_in = rng.uniform(0.0, 0.32, size=n_each)
    X_in = np.column_stack([r_in * np.cos(t_in), r_in * np.sin(t_in)])

    t_out = rng.uniform(0.0, 2.0 * np.pi, size=n_each)
    r_out = rng.uniform(0.62, 1.05, size=n_each)
    X_out = np.column_stack([r_out * np.cos(t_out), r_out * np.sin(t_out)])

    X = np.vstack([X_in, X_out])
    y = np.concatenate([np.ones(n_each), -np.ones(n_each)])
    return X, y


def predict_linear(X: np.ndarray, w: np.ndarray, b: float) -> np.ndarray:
    s = X @ w + b
    return np.where(s >= 0.0, 1.0, -1.0)


def best_line_bruteforce(
    X: np.ndarray,
    y: np.ndarray,
    b_min: float,
    b_max: float,
    b_step: float,
) -> tuple[int, float, int]:
    """Exhaustive search over every setting the sliders can make (integer angle in degrees,
    bias on the slider grid). Minimizes misclassifications; ties go to the line with the
    largest margin, so the answer never runs straight through a data point.
    Returns (theta_deg, b, errors) — exactly reproducible with the sliders."""
    bs = np.round(np.arange(b_min, b_max + b_step / 2, b_step), 2)
    best = (10**9, -np.inf, 0, 0.0)  # (errors, margin, theta_deg, b)
    for th_deg in range(-180, 180):
        th = np.deg2rad(th_deg)
        proj = X @ np.array([np.cos(th), np.sin(th)])
        S = proj[:, None] + bs[None, :]  # (n_points, n_biases)
        pred = np.where(S >= 0.0, 1.0, -1.0)
        errs = np.sum(pred != y[:, None], axis=0)
        margins = np.min(np.abs(S), axis=0)
        k = int(np.lexsort((-margins, errs))[0])
        cand = (int(errs[k]), float(margins[k]), th_deg, float(bs[k]))
        if cand[0] < best[0] or (cand[0] == best[0] and cand[1] > best[1] + 1e-12):
            best = cand
    return best[2], best[3], best[0]


def draw_classifier_panel(
    ax,
    X: np.ndarray,
    y: np.ndarray,
    w: np.ndarray,
    b: float,
    title: str,
    xlim: tuple[float, float],
    ylim: tuple[float, float],
    show_heatmap: bool,
) -> int:
    _style_axes(ax)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("feature 1", color=INK, fontsize=11)
    ax.set_ylabel("feature 2", color=INK, fontsize=11)
    ax.set_title(title, color=INK, fontsize=12, pad=10)

    pred = predict_linear(X, w, b)
    n_wrong = int(np.sum(pred != y))

    if show_heatmap:
        gx = np.linspace(xlim[0], xlim[1], 220)
        gy = np.linspace(ylim[0], ylim[1], 220)
        Gx, Gy = np.meshgrid(gx, gy)
        Z = Gx * w[0] + Gy * w[1] + b
        # custom two-tone colormap: negative vs positive side of the half-plane
        # negative side -> pink team (class -), positive side -> blue team (class +)
        cmap = LinearSegmentedColormap.from_list("half", ["#5b1e3a", "#1e3a5f"], N=256)
        ax.contourf(Gx, Gy, Z, levels=[-1e9, 0.0, 1e9], cmap=cmap, alpha=0.55)
        ax.contour(Gx, Gy, Z, levels=[0.0], colors=[ACC_LINE], linewidths=2.6, linestyles="-")

    # decision boundary line segment across view (robust clipping)
    x0, x1 = xlim
    y0, y1 = ylim
    # w0 x + w1 y + b = 0  =>  y = -(w0 x + b)/w1 if w1 != 0
    eps = 1e-9
    xs = np.linspace(x0, x1, 400)
    if abs(w[1]) > eps:
        ys = -(w[0] * xs + b) / w[1]
        mask = (ys >= y0) & (ys <= y1)
        ax.plot(xs[mask], ys[mask], color=ACC_LINE, lw=3.0, zorder=3, label="decision boundary")
    elif abs(w[0]) > eps:
        xv = -b / w[0]
        if x0 <= xv <= x1:
            ax.axvline(xv, color=ACC_LINE, lw=3.0, zorder=3, label="decision boundary")

    # points
    for lab, name, c_edge in [(1.0, "class +", ACC_A), (-1.0, "class −", ACC_B)]:
        m = y == lab
        if not np.any(m):
            continue
        wrong = pred[m] != y[m]
        ax.scatter(
            X[m, 0],
            X[m, 1],
            s=95 if X.shape[0] < 30 else 38,
            facecolor=c_edge,
            edgecolor=INK,
            linewidths=1.1,
            alpha=0.95,
            label=name,
            zorder=5,
        )
        if np.any(wrong):
            ax.scatter(
                X[m, 0][wrong],
                X[m, 1][wrong],
                s=220 if X.shape[0] < 30 else 120,
                facecolor="none",
                edgecolor=ACC_BAD,
                linewidths=2.4,
                zorder=6,
            )

    ax.legend(loc="upper right", facecolor="#1e293b", edgecolor="#475569", labelcolor=INK, fontsize=9)
    return n_wrong


def render_intro():
    st.title("Page 21: Why Non-linearity? — The Straight-Line Ceiling")
    st.markdown(
        """
        You already know **linear** rules: tweak **w**, slide **b**, and you get a **flat** decision boundary — a **single straight cut** through space.

        This page is a tiny **escape room**: can that one straight cut ever win? Spoiler for two classic shapes: **nope**. That frustration is exactly why neural nets reach for **bends** (ReLU, sigmoid, stacks of layers…) later.
        """
    )


def main():
    render_intro()

    st.sidebar.header("Playbook")
    st.sidebar.markdown(
        """
        **Try this**
        - Spin **angle** and **bias** until your eyes hurt — on **XOR** and **rings**, the yellow line is still “too straight”.
        - Hit **Best straight line (grid search)** to watch the computer try every slider setting and keep the *least bad* line — often still embarrassingly wrong.
        - Toggle **Paint the half-planes** to see the classifier’s “two-color world”.

        **Why it matters for AI**
        - A plain **linear** model is secretly drawing **one hyperplane** between classes.
        - Real data often needs **curved** or **piecewise** boundaries — that is the advertisement for **non-linear activations** and **depth** (coming soon in your path).
        """
    )

    tab_xor, tab_rings, tab_recap = st.tabs(["Mission A — XOR (four stubborn corners)", "Mission B — Donuts vs dots", "Recap & teaser"])

    with tab_xor:
        st.markdown(
            """
            **XOR vibe:** “same or different?” — the **blue** team wants coordinates that **disagree** (0, 1) and (1, 0).
            The **pink** team wants coordinates that **agree** (0, 0) and (1, 1).

            Try to separate them with **one** infinite laser divider. If your brain itches, good — that itch has a name: **non-linear separability**.
            """
        )

        c1, c2 = st.columns((1.05, 2.0), gap="large")
        with c1:
            st.subheader("Twiddle the laser")
            # Button must run *before* sliders: Streamlit disallows mutating a widget's session_state after it exists.
            st.session_state.setdefault("p21_xor_theta", 35)
            st.session_state.setdefault("p21_xor_b", -0.35)
            if st.button("Best straight line (grid search)", key="p21_xor_best"):
                Xx_btn, yy_btn = xor_dataset()
                th_best, b_best, err_best = best_line_bruteforce(Xx_btn, yy_btn, -2.2, 2.2, 0.05)
                st.session_state["p21_xor_theta"] = th_best
                st.session_state["p21_xor_b"] = b_best
                st.session_state["p21_xor_best_msg"] = (
                    f"Brute-force over every slider setting says: **{err_best}** mistake(s) is the best you can do with one line here."
                )
            if "p21_xor_best_msg" in st.session_state:
                st.success(st.session_state["p21_xor_best_msg"])
            theta_deg = st.slider("angle of normal vector (°)", -180, 180, step=1, key="p21_xor_theta")
            b_xor = st.slider("bias b (slides the line)", -2.2, 2.2, step=0.05, key="p21_xor_b")
            paint_xor = st.toggle("Paint the half-planes", value=True, key="p21_xor_paint")

        th = np.deg2rad(float(theta_deg))
        w = np.array([np.cos(th), np.sin(th)], dtype=float)

        Xx, yy = xor_dataset()

        with c2:
            st.subheader("Battlefield")
            fig, ax = plt.subplots(figsize=(10.2, 6.0))
            fig.patch.set_facecolor(BG)
            wrong = draw_classifier_panel(
                ax,
                Xx,
                yy,
                w,
                b_xor,
                "XOR lab — one straight boundary",
                (-0.55, 1.55),
                (-0.55, 1.55),
                paint_xor,
            )
            plt.tight_layout()
            st.pyplot(fig, width="stretch")
            plt.close(fig)

        st.metric("Misclassified points", f"{wrong} / 4")

        st.info(
            "Those **red halos** are honest mistakes: the line picked a side, and the point disagreed. On XOR, **some** halo traffic is unavoidable — not because you are bad at sliders, because the task is **not line-separable**: the best single line still leaves **1** of the 4 points wrong (e.g. cut off one corner) — try the grid-search button."
        )

    with tab_rings:
        st.markdown(
            """
            **Donut drama:** one class lives **near the origin**, the other lives in a **thick ring** around it.
            A straight cut can chop a chunk out, but it cannot politely separate **hole** from **halo** without casualties.
            """
        )
        seed = st.number_input("Scatter seed (new point noise)", min_value=0, max_value=99999, value=21, step=1, key="p21_ring_seed")
        rng = np.random.default_rng(int(seed))
        Xr, yr = ring_dataset(rng, n_each=160)

        c1, c2 = st.columns((1.05, 2.0), gap="large")
        with c1:
            st.subheader("Twiddle the laser")
            st.session_state.setdefault("p21_ring_theta", 125)
            st.session_state.setdefault("p21_ring_b", 0.0)
            if st.button("Best straight line (grid search)", key="p21_ring_best"):
                th_best, b_best, err_best = best_line_bruteforce(Xr, yr, -1.4, 1.4, 0.05)
                st.session_state["p21_ring_theta"] = th_best
                st.session_state["p21_ring_b"] = b_best
                st.session_state["p21_ring_best_msg"] = (
                    f"Even the computer’s best line leaves **{err_best}** wrong out of {Xr.shape[0]} — geometry beats optimism."
                )
                st.session_state["p21_ring_best_seed"] = int(seed)
            if st.session_state.get("p21_ring_best_seed") != int(seed):
                # The stored result belongs to a different point cloud: drop it.
                st.session_state.pop("p21_ring_best_msg", None)
            if "p21_ring_best_msg" in st.session_state:
                st.warning(st.session_state["p21_ring_best_msg"])
            theta_deg2 = st.slider("angle of normal vector (°)", -180, 180, step=1, key="p21_ring_theta")
            b_ring = st.slider("bias b", -1.4, 1.4, step=0.05, key="p21_ring_b")
            paint_ring = st.toggle("Paint the half-planes", value=True, key="p21_ring_paint")

        th2 = np.deg2rad(float(theta_deg2))
        w2 = np.array([np.cos(th2), np.sin(th2)], dtype=float)

        with c2:
            st.subheader("Battlefield")
            fig, ax = plt.subplots(figsize=(10.2, 6.0))
            fig.patch.set_facecolor(BG)
            wrong2 = draw_classifier_panel(
                ax,
                Xr,
                yr,
                w2,
                b_ring,
                "Ring lab — still one straight boundary",
                (-1.25, 1.25),
                (-1.25, 1.25),
                paint_ring,
            )
            plt.tight_layout()
            st.pyplot(fig, width="stretch")
            plt.close(fig)

        st.caption("Halos mark misclassified samples — watch them bloom when the line slices through the donut.")

        st.metric("Misclassified samples", f"{wrong2} / {Xr.shape[0]}")

    with tab_recap:
        st.markdown(
            """
            ### Recap in one breath
            - **Linear classifiers** = **one hyperplane** → **two half-spaces**. Powerful, fast, interpretable — but **topologically polite**.
            - Some toy datasets are **tiny** yet **already rude** to half-spaces (XOR is the poster child).
            - When the real world throws **curved** or **nested** structure at you, **non-linearity** is not spice — it is **oxygen**.

            ### Teaser (your curriculum’s next stops)
            - **Piecewise** vibes → ReLU-shaped building blocks.
            - **Stacking** layers → folding space so that what was tangled in **x** becomes separable in a **new** representation.

            **Next page:** *Piecewise Functions* — stitching regions so the graph can finally **kink**.
            """
        )

        with st.expander("Optional micro-proof (why XOR hates one line)", expanded=False):
            st.markdown(
                r"""
                Label points in $\{\,0,1\,\}^2$ with XOR signs: **+1** on $(0,1)$ and $(1,0)$; **−1** on $(0,0)$ and $(1,1)$.
                For the score $s(x,y)=w_1x+w_2y+b$, the two positive labels require $s(1,0)\ge 0$ and $s(0,1)\ge 0$, while the negative labels require $s(0,0)<0$ and $s(1,1)<0$.
                But $s(1,0)+s(0,1)=s(0,0)+s(1,1)=w_1+w_2+2b$, so the same sum would have to be both $\ge 0$ and $<0$ — a contradiction.
                Hence **no** single thresholded line separates all four — at least **1** point is always wrong (and 1 is achievable: cut off a single corner). Time to invite a **bendy** friend.
                """
            )

    st.divider()
    st.markdown(
        f"""
        <div style="color:{MUTED}; font-size:0.95rem;">
        Page 21 — part of your “Functions → Probability” bridge. If linear models feel like rulers, non-linear models are origami: same paper, wilder shapes.
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
