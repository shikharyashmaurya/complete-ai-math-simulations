import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.mathutils import fmt_num, softmax  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="82 · Jacobian & Hessian", page_icon="📈", layout="wide")

EPS_FD = 1e-5  # central-difference step
COLORS = {"true": "#38bdf8", "lin": "#fb923c", "e1": "#34d399", "e2": "#f472b6", "v": "#facc15", "gd": "#e2e8f0"}


def mat_tex(m, prec=3):
    rows = [" & ".join(fmt_num(v, prec) for v in row) for row in np.atleast_2d(m)]
    return r"\begin{bmatrix}" + r" \\ ".join(rows) + r"\end{bmatrix}"


def vec_tex(v, prec=3):
    return mat_tex(np.asarray(v, dtype=float).reshape(-1, 1), prec)


# ---------------------------------------------------------------- Jacobian presets (R² → R²)
LIN_A = np.array([[1.2, 0.6], [-0.4, 0.9]])


def _soft2(a, b):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    m = np.maximum(a, b)
    ea, eb = np.exp(a - m), np.exp(b - m)
    return ea / (ea + eb), eb / (ea + eb)


def _soft2_jac(a, b):
    p = softmax([a, b])
    return np.diag(p) - np.outer(p, p)


JAC_PRESETS = {
    "Linear map  f = A·(x, y)": dict(
        f=lambda x, y: (LIN_A[0, 0] * x + LIN_A[0, 1] * y, LIN_A[1, 0] * x + LIN_A[1, 1] * y),
        J=lambda x, y: LIN_A.copy(),
        formula=r"f(x,y)=\begin{bmatrix}1.2x+0.6y\\-0.4x+0.9y\end{bmatrix}",
        jac=r"J=A=\begin{bmatrix}1.2&0.6\\-0.4&0.9\end{bmatrix}\ \text{(the same everywhere)},\quad \det J=1.32",
    ),
    "Polar → Cartesian  (r, θ) ↦ (r cos θ, r sin θ)": dict(
        f=lambda r, t: (r * np.cos(t), r * np.sin(t)),
        J=lambda r, t: np.array([[np.cos(t), -r * np.sin(t)], [np.sin(t), r * np.cos(t)]]),
        formula=r"f(r,\theta)=\begin{bmatrix}r\cos\theta\\ r\sin\theta\end{bmatrix}",
        jac=r"J=\begin{bmatrix}\cos\theta&-r\sin\theta\\ \sin\theta&r\cos\theta\end{bmatrix},\quad \det J=r",
    ),
    "Nonlinear warp  (x² − y², 2xy)": dict(
        f=lambda x, y: (x * x - y * y, 2 * x * y),
        J=lambda x, y: np.array([[2 * x, -2 * y], [2 * y, 2 * x]]),
        formula=r"f(x,y)=\begin{bmatrix}x^2-y^2\\ 2xy\end{bmatrix}\quad(\text{complex squaring } z\mapsto z^2)",
        jac=r"J=\begin{bmatrix}2x&-2y\\ 2y&2x\end{bmatrix},\quad \det J=4(x^2+y^2)",
    ),
    "Softmax over 2 logits  (z₁, z₂) ↦ (p₁, p₂)": dict(
        f=_soft2,
        J=_soft2_jac,
        formula=r"f(z_1,z_2)=\begin{bmatrix}p_1\\p_2\end{bmatrix}=\frac{1}{e^{z_1}+e^{z_2}}\begin{bmatrix}e^{z_1}\\e^{z_2}\end{bmatrix}",
        jac=r"J=\operatorname{diag}(p)-pp^\top=p_1p_2\begin{bmatrix}1&-1\\-1&1\end{bmatrix},\quad \det J=0",
    ),
}


def numeric_jacobian(f, p, eps=EPS_FD):
    J = np.zeros((2, 2))
    for j in range(2):
        e = np.zeros(2)
        e[j] = eps
        plus, minus = np.array(f(*(p + e)), dtype=float), np.array(f(*(p - e)), dtype=float)
        J[:, j] = (plus - minus) / (2 * eps)
    return J


def square_lines(p, h, n_lines=5, n_pts=41):
    ts, offs = np.linspace(-h, h, n_pts), np.linspace(-h, h, n_lines)
    lines = []
    for c in offs:
        lines.append((p[0] + ts, np.full_like(ts, p[1] + c)))
        lines.append((np.full_like(ts, p[0] + c), p[1] + ts))
    return lines


def square_boundary(p, h, n=200):
    """Counter-clockwise boundary of the square [p ± h]."""
    t = np.linspace(-h, h, n, endpoint=False)
    xs = np.concatenate([p[0] + t, np.full(n, p[0] + h), p[0] - t, np.full(n, p[0] - h)])
    ys = np.concatenate([np.full(n, p[1] - h), p[1] + t, np.full(n, p[1] + h), p[1] - t])
    return xs, ys


def shoelace(xs, ys):
    return 0.5 * float(np.sum(xs * np.roll(ys, -1) - np.roll(xs, -1) * ys))


def jacobian_lab():
    st.header("2 · Lab A — The Jacobian: the best local *linear* map")
    c = st.columns(4)
    name = c[0].selectbox("Vector function f : ℝ² → ℝ²", list(JAC_PRESETS), key="p82_jac_preset")
    x0 = c[1].slider("x₀ (first input; r for polar)", -2.0, 2.0, 0.8, 0.05, key="p82_jac_x")
    y0 = c[2].slider("y₀ (second input; θ in rad for polar)", -2.0, 2.0, 0.5, 0.05, key="p82_jac_y")
    h = c[3].slider("Half-width h of the grid square", 0.02, 0.6, 0.25, 0.01, key="p82_jac_h")
    spec, p = JAC_PRESETS[name], np.array([x0, y0])
    f, J = spec["f"], spec["J"](x0, y0)
    fp = np.array(f(x0, y0), dtype=float)
    st.latex(spec["formula"] + r"\qquad " + spec["jac"])

    lin = lambda xs, ys: (fp[0] + J[0, 0] * (xs - x0) + J[0, 1] * (ys - y0), fp[1] + J[1, 0] * (xs - x0) + J[1, 1] * (ys - y0))  # noqa: E731
    dom, img = go.Figure(), go.Figure()
    max_err = 0.0
    for i, (xs, ys) in enumerate(square_lines(p, h)):
        dom.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color="#94a3b8", width=1), showlegend=False))
        tu, tv = f(xs, ys)
        lu, lv = lin(xs, ys)
        max_err = max(max_err, float(np.max(np.hypot(tu - lu, tv - lv))))
        img.add_trace(go.Scatter(x=tu, y=tv, mode="lines", line=dict(color=COLORS["true"], width=2),
                                 name="true image f(square)", legendgroup="t", showlegend=i == 0))
        img.add_trace(go.Scatter(x=lu, y=lv, mode="lines", line=dict(color=COLORS["lin"], width=2, dash="dash"),
                                 name="linear approx. f(p) + J·Δ", legendgroup="l", showlegend=i == 0))
    for k, col in ((0, COLORS["e1"]), (1, COLORS["e2"])):
        d = np.zeros(2)
        d[k] = h
        dom.add_trace(go.Scatter(x=[x0, x0 + d[0]], y=[y0, y0 + d[1]], mode="lines+markers", line=dict(color=col, width=4),
                                 name=f"h·e{k + 1}"))
        jd = J @ d
        img.add_trace(go.Scatter(x=[fp[0], fp[0] + jd[0]], y=[fp[1], fp[1] + jd[1]], mode="lines+markers",
                                 line=dict(color=col, width=4), name=f"J·(h·e{k + 1}) = h·column {k + 1}"))
    dom.add_trace(go.Scatter(x=[x0], y=[y0], mode="markers", marker=dict(size=10, color="#facc15"), name="p"))
    img.add_trace(go.Scatter(x=[fp[0]], y=[fp[1]], mode="markers", marker=dict(size=10, color="#facc15"), name="f(p)"))
    for fig, title in ((dom, "Input space: square around p"), (img, "Output space: its image")):
        fig.update_layout(title=title, height=430, margin=dict(l=10, r=10, t=40, b=10),
                          legend=dict(orientation="h", y=-0.12), yaxis=dict(scaleanchor="x", scaleratio=1))
    cl, cr = st.columns(2)
    cl.plotly_chart(dom, width="stretch")
    cr.plotly_chart(img, width="stretch")

    bx, by = square_boundary(p, h)
    area_ratio = round(shoelace(*f(bx, by)) / (2 * h) ** 2, 12) + 0.0
    detJ = round(float(np.linalg.det(J)), 12) + 0.0  # rounding hides -1e-18 noise (softmax)
    J_num = numeric_jacobian(f, p)
    fd_err = float(np.max(np.abs(J_num - J)))
    m = st.columns(4)
    m[0].metric("det J(p) (local area factor)", fmt_num(detJ, 4))
    m[1].metric("signed area(f(square)) / area(square)", fmt_num(area_ratio, 4), help="Shoelace formula on the mapped boundary.")
    m[2].metric("max ‖f − linear approx.‖ on the grid", f"{max_err:.2e}", help="Shrinks like h² — halve h and it drops ≈ 4×.")
    m[3].metric("max |J_analytic − J_numeric|", f"{fd_err:.1e}")
    st.caption(
        "The area ratio is the *average* of det J over the square (change of variables), so it approaches det J(p) as h → 0. "
        "A negative determinant means the image is mirrored (orientation flips); det J = 0 squashes the square onto a curve. "
        "The orange dashed grid is a perfect parallelogram — that is what 'J is the best linear approximation' looks like."
    )
    if abs(detJ) < 1e-12:
        st.warning("det J = 0 here: the map is locally **not invertible** — a 2-D patch collapses to (almost) a line. "
                   "For softmax this is always true, since p₁ + p₂ = 1: shifting both logits equally changes nothing.")
    return dict(name=name, p=p, fp=fp, J=J, J_num=J_num, det=detJ, h=h, fd_err=fd_err)


# ---------------------------------------------------------------- Hessian presets (scalar f(x, y))
def _rb_hess(x, y):
    return np.array([[2 - 400 * y + 1200 * x * x, -400 * x], [-400 * x, 200.0]])


HESS_PRESETS = {
    "Bowl  x² + 0.8xy + 1.5y²": dict(
        f=lambda x, y: x * x + 0.8 * x * y + 1.5 * y * y,
        g=lambda x, y: np.array([2 * x + 0.8 * y, 0.8 * x + 3 * y]),
        H=lambda x, y: np.array([[2.0, 0.8], [0.8, 3.0]]),
        crit=(0.0, 0.0), tex=r"f=x^2+0.8xy+1.5y^2", log=False,
    ),
    "Saddle  x² − y²": dict(
        f=lambda x, y: x * x - y * y,
        g=lambda x, y: np.array([2 * x, -2 * y]),
        H=lambda x, y: np.array([[2.0, 0.0], [0.0, -2.0]]),
        crit=(0.0, 0.0), tex=r"f=x^2-y^2", log=False,
    ),
    "Rosenbrock  (1 − x)² + 100(y − x²)²": dict(
        f=lambda x, y: (1 - x) ** 2 + 100 * (y - x * x) ** 2,
        g=lambda x, y: np.array([-2 * (1 - x) - 400 * x * (y - x * x), 200 * (y - x * x)]),
        H=_rb_hess,
        crit=(1.0, 1.0), tex=r"f=(1-x)^2+100(y-x^2)^2", log=True,
    ),
    "Quartic  x⁴ + y⁴": dict(
        f=lambda x, y: x**4 + y**4,
        g=lambda x, y: np.array([4 * x**3, 4 * y**3]),
        H=lambda x, y: np.array([[12 * x * x, 0.0], [0.0, 12 * y * y]]),
        crit=(0.0, 0.0), tex=r"f=x^4+y^4", log=False,
    ),
}


def classify(lam, gnorm):
    scale = max(1.0, float(np.max(np.abs(lam))))
    tiny = 1e-9 * scale
    if gnorm > 1e-9:
        if np.all(lam > tiny):
            return "not critical", "∇f ≠ 0, so this is not a critical point. Both eigenvalues > 0: the surface curves **up** in every direction here (locally convex)."
        if np.all(lam < -tiny):
            return "not critical", "∇f ≠ 0, so this is not a critical point. Both eigenvalues < 0: the surface curves **down** in every direction (locally concave)."
        return "not critical", "∇f ≠ 0, so this is not a critical point. The curvature is mixed or flat in some direction here."
    if np.any(np.abs(lam) <= tiny):
        return "inconclusive", "∇f = 0 but an eigenvalue is 0: the second-derivative test is **inconclusive** — higher-order terms decide."
    if np.all(lam > 0):
        return "local minimum", "∇f = 0 and both eigenvalues > 0: a **local minimum**."
    if np.all(lam < 0):
        return "local maximum", "∇f = 0 and both eigenvalues < 0: a **local maximum**."
    return "saddle point", "∇f = 0 and the eigenvalues have opposite signs: a **saddle point**."


def newton_step(H, g):
    """Return (step, note). Falls back to the pseudo-inverse when H is (near-)singular."""
    lam = np.linalg.eigvalsh(H)
    if np.min(np.abs(lam)) <= 1e-10 * max(1.0, float(np.max(np.abs(lam)))):
        return -np.linalg.pinv(H, rcond=1e-10) @ g, "singular"
    return -np.linalg.solve(H, g), "ok"


def run_path(step_fn, p0, n):
    pts, status = [np.array(p0, dtype=float)], "ok"
    for _ in range(n):
        step, note = step_fn(pts[-1])
        if np.all(np.isfinite(step)) and np.linalg.norm(step) < 1e-12:
            break
        new = pts[-1] + step
        if not np.all(np.isfinite(new)) or np.linalg.norm(new) > 1e3:
            status = "diverged"
            break
        pts.append(new)
        if note == "singular":
            status = "singular"
    return np.array(pts), status


def hessian_lab():
    st.header("3 · Lab B — The Hessian: curvature, critical points and Newton's method")
    c = st.columns([1.4, 1, 1, 1])
    name = c[0].selectbox("Scalar function f(x, y)", list(HESS_PRESETS), key="p82_hess_preset")
    hx = c[1].slider("Point x", -2.0, 2.0, -1.0, 0.05, key="p82_hess_x")
    hy = c[2].slider("Point y", -2.0, 2.0, 1.0, 0.05, key="p82_hess_y")
    theta_deg = c[3].slider("Direction angle θ (°) of v", 0, 180, 30, 5, key="p82_hess_theta")
    c2 = st.columns([1.4, 2])
    snap = c2[0].toggle("Snap the point to the critical point", value=False, key="p82_hess_snap")
    eta = c2[1].select_slider("Gradient-descent learning rate η", options=[0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                              value=0.1, key="p82_hess_eta")
    spec = HESS_PRESETS[name]
    p = np.array(spec["crit"] if snap else (hx, hy), dtype=float)
    f, gfun, Hfun = spec["f"], spec["g"], spec["H"]
    fp, g, H = float(f(*p)), gfun(*p), Hfun(*p)
    lam, vecs = np.linalg.eigh(H)  # ascending eigenvalues, orthonormal eigenvectors (columns)
    th = np.radians(theta_deg)
    v = np.array([np.cos(th), np.sin(th)])
    curv = float(v @ H @ v)
    kind, msg = classify(lam, float(np.linalg.norm(g)))
    H_num = numeric_jacobian(lambda x, y: tuple(gfun(x, y)), p)  # Hessian = Jacobian of the gradient

    nstep, nnote = newton_step(H, g)
    gstep = -eta * g
    newton_pts, newton_status = run_path(lambda q: newton_step(Hfun(*q), gfun(*q)), p, 8)
    gd_pts, gd_status = run_path(lambda q: (-eta * gfun(*q), "ok"), p, 40)

    # ---- contour map
    ylo, yhi = (-1.2, 3.2) if spec["log"] else (-2.2, 2.2)
    ylo, yhi = min(ylo, p[1] - 0.3), max(yhi, p[1] + 0.3)
    xs, ys = np.linspace(-2.2, 2.2, 140), np.linspace(ylo, yhi, 140)
    X, Y = np.meshgrid(xs, ys)
    Z = f(X, Y)
    fig = go.Figure(go.Contour(x=xs, y=ys, z=np.log10(1 + Z) if spec["log"] else Z, colorscale="Viridis", ncontours=25,
                               colorbar=dict(title="log₁₀(1+f)" if spec["log"] else "f"), opacity=0.85))
    s = 0.7
    for k, col in ((0, COLORS["e1"]), (1, COLORS["e2"])):
        e = vecs[:, k]
        fig.add_trace(go.Scatter(x=[p[0] - s * e[0], p[0] + s * e[0]], y=[p[1] - s * e[1], p[1] + s * e[1]], mode="lines",
                                 line=dict(color=col, width=4), name=f"eigenvector e{k + 1} (λ{k + 1} = {lam[k]:.3g})"))
    fig.add_trace(go.Scatter(x=[p[0], p[0] + 0.5 * v[0]], y=[p[1], p[1] + 0.5 * v[1]], mode="lines+markers",
                             line=dict(color=COLORS["v"], width=3, dash="dot"), name="direction v"))
    fig.add_trace(go.Scatter(x=gd_pts[:, 0], y=gd_pts[:, 1], mode="lines+markers", marker=dict(size=4),
                             line=dict(color=COLORS["gd"], width=2), name=f"gradient descent (η = {eta})"))
    fig.add_trace(go.Scatter(x=newton_pts[:, 0], y=newton_pts[:, 1], mode="lines+markers", marker=dict(size=7, symbol="diamond"),
                             line=dict(color=COLORS["lin"], width=3), name="Newton  p ← p − H⁻¹∇f"))
    fig.add_trace(go.Scatter(x=[spec["crit"][0]], y=[spec["crit"][1]], mode="markers", marker=dict(size=14, symbol="star", color="white"),
                             name="critical point"))
    fig.add_trace(go.Scatter(x=[p[0]], y=[p[1]], mode="markers", marker=dict(size=11, color="#facc15"), name="p"))
    fig.update_layout(height=520, margin=dict(l=10, r=10, t=30, b=10), legend=dict(orientation="h", y=-0.1),
                      xaxis=dict(range=[-2.2, 2.2]), yaxis=dict(range=[ylo, yhi], scaleanchor="x", scaleratio=1))
    cl, cr = st.columns([1.3, 1])
    cl.plotly_chart(fig, width="stretch")

    # ---- curvature along every direction (Rayleigh quotient)
    thetas = np.linspace(0, np.pi, 181)
    dirs = np.stack([np.cos(thetas), np.sin(thetas)])
    curvs = np.einsum("in,ij,jn->n", dirs, H, dirs)
    cf = go.Figure(go.Scatter(x=np.degrees(thetas), y=curvs, mode="lines", line=dict(color=COLORS["true"]), name="vᵀHv"))
    for k, col in ((0, COLORS["e1"]), (1, COLORS["e2"])):
        cf.add_hline(y=lam[k], line=dict(color=col, dash="dash"), annotation_text=f"λ{k + 1} = {lam[k]:.3g}")
    cf.add_trace(go.Scatter(x=[theta_deg], y=[curv], mode="markers", marker=dict(size=12, color=COLORS["v"]), name="current v"))
    cf.update_layout(title="Curvature vᵀHv along direction θ", xaxis_title="θ (degrees)", height=250,
                     margin=dict(l=10, r=10, t=40, b=10), showlegend=False)
    cr.plotly_chart(cf, width="stretch")

    # ---- 1-D slice through p along v: true f vs second-order Taylor model
    t = np.linspace(-1.0, 1.0, 201)
    true_slice = f(p[0] + t * v[0], p[1] + t * v[1])
    quad_slice = fp + t * float(g @ v) + 0.5 * t * t * curv
    sf = go.Figure()
    sf.add_trace(go.Scatter(x=t, y=true_slice, mode="lines", line=dict(color=COLORS["true"], width=3), name="true f(p + t·v)"))
    sf.add_trace(go.Scatter(x=t, y=quad_slice, mode="lines", line=dict(color=COLORS["lin"], dash="dash", width=3),
                            name="quadratic model"))
    sf.update_layout(title="Slice along v: f vs f(p) + t∇f·v + ½t²vᵀHv", xaxis_title="t", height=250,
                     margin=dict(l=10, r=10, t=40, b=10), legend=dict(orientation="h", y=-0.3))
    cr.plotly_chart(sf, width="stretch")

    st.info(f"**Classification at p = ({fmt_num(p[0])}, {fmt_num(p[1])}):** {msg}")
    m = st.columns(5)
    m[0].metric("f(p)", f"{fp:.4g}")
    m[1].metric("‖∇f(p)‖", f"{np.linalg.norm(g):.4g}")
    m[2].metric("vᵀHv (curvature along v)", f"{curv:.4g}")
    abs_lam = np.sort(np.abs(lam))
    cond = abs_lam[1] / abs_lam[0] if abs_lam[0] > 1e-12 * max(1.0, abs_lam[1]) else float("inf")
    m[3].metric("condition number |λmax|/|λmin|", "∞ (singular)" if not np.isfinite(cond) else f"{cond:.4g}")
    m[4].metric("max |H − H_numeric|", f"{np.max(np.abs(H - H_num)):.1e}", help="Numeric Hessian = central differences of ∇f.")

    with st.expander("🔍 Second-order (quadratic) model vs the true surface in 3-D", expanded=False):
        r = 0.6
        u = np.linspace(-r, r, 31)
        DX, DY = np.meshgrid(u, u)
        ZT = f(p[0] + DX, p[1] + DY)
        ZQ = fp + g[0] * DX + g[1] * DY + 0.5 * (H[0, 0] * DX**2 + 2 * H[0, 1] * DX * DY + H[1, 1] * DY**2)
        f3 = go.Figure([go.Surface(x=p[0] + DX, y=p[1] + DY, z=ZT, colorscale="Viridis", showscale=False, name="true f"),
                        go.Surface(x=p[0] + DX, y=p[1] + DY, z=ZQ, colorscale=[[0, COLORS["lin"]], [1, COLORS["lin"]]],
                                   opacity=0.55, showscale=False, name="quadratic model")])
        f3.update_layout(height=460, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(f3, width="stretch")
        st.caption(f"Orange = quadratic model q(p+Δ) = f(p) + ∇fᵀΔ + ½ΔᵀHΔ, true surface coloured. "
                   f"Max gap on this ±{r} window: {np.max(np.abs(ZT - ZQ)):.3g} (zero for the quadratic bowl and saddle).")

    newton_msgs = {
        "ok": "H stayed invertible along the whole path.",
        "singular": "H was singular somewhere on the path, so the pseudo-inverse H⁺ was used (the step ignores the flat direction).",
        "diverged": "Newton's path blew up (|p| > 1000) and was stopped.",
    }
    end, gd_end = newton_pts[-1], gd_pts[-1]
    if len(newton_pts) == 1:
        newton_txt = "p is already a critical point (∇f = 0), so Newton does not move."
    else:
        newton_txt = (f"After {len(newton_pts) - 1} Newton step(s) it is at ({fmt_num(end[0], 3)}, {fmt_num(end[1], 3)}), "
                      f"f = {f(*end):.3g}. {newton_msgs[newton_status]}")
    gd_txt = ("**diverged** — η is too large for this curvature" if gd_status == "diverged"
              else f"ends at ({fmt_num(gd_end[0], 3)}, {fmt_num(gd_end[1], 3)}), f = {f(*gd_end):.3g}")
    st.markdown(
        f"**Newton vs gradient descent from p.** Newton jumps to the critical point of the *quadratic model*. {newton_txt}  \n"
        f"Gradient descent ({len(gd_pts) - 1} steps, η = {eta}) {gd_txt}."
    )
    if name.startswith("Saddle"):
        st.warning("**Newton is attracted to the saddle.** Its step solves ∇q = 0 for the quadratic model, and a saddle is exactly such a "
                   "point — so from *anywhere* one Newton step lands on (0, 0), even though f goes down forever along y. "
                   "Gradient descent instead slides off along the negative-curvature direction (unless it starts exactly on y = 0).")
    if nnote == "ok" and float(g @ nstep) > 0:
        st.caption("Here ∇f·Δ_Newton > 0: H is not positive definite, so the Newton step points **uphill**.")
    return dict(name=name, p=p, g=g, H=H, lam=lam, vecs=vecs, v=v, curv=curv, nstep=nstep, nnote=nnote, gstep=gstep,
                eta=eta, kind=kind, f=f)


def worked_example(jr, hr):
    st.header("4 · Worked example (live numbers)")
    c1, c2 = st.columns(2)
    with c1, st.container(border=True):
        st.markdown(f"**Jacobian of** {jr['name'].split('  ')[0]} **at p = ({fmt_num(jr['p'][0])}, {fmt_num(jr['p'][1])})**")
        st.latex(r"J_{ij}=\frac{\partial f_i}{\partial x_j}\;\Rightarrow\; J(p)=" + mat_tex(jr["J"], 4))
        st.latex(r"J_{\text{num}}[:,j]=\frac{f(p+\varepsilon e_j)-f(p-\varepsilon e_j)}{2\varepsilon}=" + mat_tex(jr["J_num"], 4))
        st.markdown(f"With ε = {EPS_FD:g} the two agree to {jr['fd_err']:.1e} (central differences have error ∝ ε²).")
        J = jr["J"]
        st.latex(rf"\det J = ({fmt_num(J[0, 0], 4)})({fmt_num(J[1, 1], 4)}) - ({fmt_num(J[0, 1], 4)})({fmt_num(J[1, 0], 4)}) = {fmt_num(jr['det'], 4)}")
        st.markdown(f"A tiny square of area A near p maps to a patch of area ≈ |det J|·A = {abs(jr['det']):.4g}·A.")
    with c2, st.container(border=True):
        H, g, lam = hr["H"], hr["g"], hr["lam"]
        a, b, d = H[0, 0], H[0, 1], H[1, 1]
        mid, rad = (a + d) / 2, np.sqrt(((a - d) / 2) ** 2 + b * b)
        st.markdown(f"**Hessian of {hr['name'].split('  ')[0].lower()} at p = ({fmt_num(hr['p'][0])}, {fmt_num(hr['p'][1])})**")
        st.latex(r"\nabla f=" + vec_tex(g, 4) + r",\quad H=\begin{bmatrix}f_{xx}&f_{xy}\\f_{yx}&f_{yy}\end{bmatrix}=" + mat_tex(H, 4))
        st.latex(rf"\lambda_{{1,2}}=\tfrac{{a+d}}{{2}}\mp\sqrt{{\left(\tfrac{{a-d}}{{2}}\right)^2+b^2}}={fmt_num(mid, 4)}\mp{fmt_num(rad, 4)}"
                 rf"\;\Rightarrow\;\lambda_1={fmt_num(lam[0], 4)},\ \lambda_2={fmt_num(lam[1], 4)}")
        v = hr["v"]
        st.latex(rf"v^\top H v = a v_x^2 + 2b\,v_xv_y + d v_y^2 = {fmt_num(hr['curv'], 4)}\quad(\lambda_1\le v^\top Hv\le\lambda_2),\ v=({fmt_num(v[0], 3)},{fmt_num(v[1], 3)})")
        if hr["nnote"] == "ok":
            st.latex(r"\Delta_{\text{Newton}}=-H^{-1}\nabla f=" + vec_tex(hr["nstep"], 4)
                     + r",\quad \Delta_{\text{GD}}=-\eta\nabla f=" + vec_tex(hr["gstep"], 4))
        else:
            st.latex(r"H\ \text{singular}\Rightarrow \Delta_{\text{Newton}}=-H^{+}\nabla f=" + vec_tex(hr["nstep"], 4)
                     + r",\quad \Delta_{\text{GD}}=-\eta\nabla f=" + vec_tex(hr["gstep"], 4))
        st.markdown(f"Verdict: **{hr['kind']}**.")


def ai_connection(hr):
    st.header("5 · Where this shows up in AI")
    st.markdown(
        r"""
- **Backprop is a chain of Jacobians.** A layer $y=f(x)$ has Jacobian $J=\partial y/\partial x$. Given the upstream gradient
  $\bar g=\partial L/\partial y$, backprop computes the **vector-Jacobian product** $\partial L/\partial x = J^\top\bar g$ —
  without ever building $J$ (for a 4096-wide layer $J$ would have 16.7 M entries; the VJP costs about as much as the forward pass).
- **Softmax** has the Jacobian $J=\operatorname{diag}(p)-pp^\top$. Verify it below, and see why the classic
  softmax + cross-entropy gradient collapses to $p-y$.
"""
    )
    c = st.columns([1, 1, 1, 1.2])
    z = np.array([c[i].slider(f"logit z{i + 1}", -4.0, 4.0, val, 0.1, key=f"p82_sm_z{i + 1}") for i, val in enumerate((2.0, 1.0, -0.5))])
    k = c[3].radio("True class y (one-hot)", [1, 2, 3], horizontal=True, key="p82_sm_class") - 1
    p = softmax(z)
    J = np.diag(p) - np.outer(p, p)
    J_num = np.zeros((3, 3))
    for j in range(3):
        e = np.zeros(3)
        e[j] = EPS_FD
        J_num[:, j] = (softmax(z + e) - softmax(z - e)) / (2 * EPS_FD)
    y = np.eye(3)[k]
    g_up = -y / max(p[k], 1e-300)  # ∂(−log p_k)/∂p
    vjp = J.T @ g_up
    cols = st.columns(3)
    cols[0].latex(r"p=" + vec_tex(p, 4) + r",\ J=\operatorname{diag}(p)-pp^\top=" + mat_tex(J, 4))
    cols[1].latex(r"J_{\text{num}}=" + mat_tex(J_num, 4))
    cols[2].latex(r"J^\top\bar g\ \text{with}\ \bar g=\frac{\partial(-\log p_y)}{\partial p}:\ " + vec_tex(vjp, 4) + r"=p-y=" + vec_tex(p - y, 4))
    ok = np.allclose(J, J_num, atol=1e-8) and np.allclose(vjp, p - y, atol=1e-12)
    (st.success if ok else st.error)(
        f"max |J − J_num| = {np.max(np.abs(J - J_num)):.1e} · each row sums to {np.max(np.abs(J.sum(axis=1))):.0e} (adding the same constant to all "
        f"logits changes nothing, so J·1 = 0 and J is singular) · J is symmetric · VJP equals p − y to {np.max(np.abs(vjp - p + y)):.0e}."
    )

    lam = hr["lam"]
    st.markdown(
        r"""
- **Hessian condition number ↔ learning rate.** Near a minimum, gradient descent on the quadratic model is stable only if
  $\eta<2/\lambda_{\max}$, and it crawls along the flattest direction at a rate set by $\kappa=\lambda_{\max}/\lambda_{\min}$.
  A badly conditioned Hessian (long narrow valleys like Rosenbrock) forces a tiny η — the reason for momentum, Adam and preconditioning.
"""
    )
    if np.all(lam > 1e-12):
        st.info(f"Current Hessian in Lab B: λmax = {lam[1]:.4g}, so stable GD needs η < 2/λmax = {2 / lam[1]:.4g}; "
                f"κ = {lam[1] / lam[0]:.4g}. Your η = {hr['eta']} is **{'stable' if hr['eta'] < 2 / lam[1] else 'too large'}** for this local curvature.")
    else:
        st.info("The Hessian in Lab B is not positive definite at the current point, so there is no stable-η bound to quote here "
                "(try the bowl, or snap Rosenbrock to its minimum: κ ≈ 2508).")
    safe_page_link("pages/53Learning Rate.py", "Revisit: 53 · Learning Rate", icon="⛰️")

    st.markdown(
        r"""
- **Sharp vs flat minima.** Two minima with the same loss can have very different top Hessian eigenvalues. Perturbing the
  weights by δ raises the loss by about $\tfrac12\lambda\delta^2$: flat minima (small λ) are robust to the noise of SGD and
  to the shift between training and test data, which is one explanation of why they often generalise better
  (and why methods like SAM explicitly seek them).
"""
    )
    w = np.linspace(-1, 1, 201)
    delta, lam_s, lam_f = 0.3, 20.0, 1.0
    sf = go.Figure([go.Scatter(x=w, y=0.5 * lam_s * w * w, name=f"sharp (λ = {lam_s:g}): +{0.5 * lam_s * delta**2:.2f} at δ = {delta}"),
                    go.Scatter(x=w, y=0.5 * lam_f * w * w, name=f"flat (λ = {lam_f:g}): +{0.5 * lam_f * delta**2:.3f} at δ = {delta}")])
    sf.add_vline(x=delta, line=dict(dash="dot", color="#94a3b8"))
    sf.update_layout(height=260, yaxis=dict(range=[0, 3]), xaxis_title="weight perturbation δ", yaxis_title="loss increase",
                     margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h", y=-0.35))
    st.plotly_chart(sf, width="stretch")


def main():
    st.title("📈 82 · Jacobian & Hessian")
    st.header("1 · Intuition")
    st.markdown(
        r"""
A derivative answers *"if I nudge the input, how does the output move?"* For many inputs and many outputs, the answer is a
**matrix**:

- The **Jacobian** $J$ of a vector function $f:\mathbb{R}^n\to\mathbb{R}^m$ stacks every partial derivative,
  $J_{ij}=\partial f_i/\partial x_j$. Zoom in far enough and any smooth map looks **linear**: $f(p+\Delta)\approx f(p)+J\Delta$.
  So everything you learned about matrices as transformations applies locally — in particular $|\det J|$ is the local
  **area scaling**.
- The **Hessian** $H$ of a scalar function is the Jacobian of its gradient, $H_{ij}=\partial^2 f/\partial x_i\partial x_j$
  (symmetric for smooth $f$). It measures **curvature**: $v^\top Hv$ is how fast the slope changes along a unit direction $v$,
  and its eigenvectors are the directions of strongest and weakest bending.

Why AI cares: backprop multiplies Jacobians (as vector-Jacobian products), and the Hessian of the loss decides which learning
rates work, why some valleys are slow, and why Newton-style optimisers are tempting but fragile.
"""
    )
    safe_page_link("pages/17Determinant — Area Scaling.py", "Refresher: 17 · Determinant — Area Scaling", icon="🧭")
    jr = jacobian_lab()
    hr = hessian_lab()
    worked_example(jr, hr)
    ai_connection(hr)

    st.header("6 · Key takeaways")
    st.success(
        "- **Jacobian** = matrix of first partials; it is the best linear approximation f(p+Δ) ≈ f(p) + JΔ, with error O(‖Δ‖²).\n"
        "- **det J** = local area (volume) scaling; det J = 0 means the map squashes space (e.g. softmax, since probabilities sum to 1).\n"
        "- **Hessian** = Jacobian of the gradient; vᵀHv is curvature along v, bounded by its smallest and largest eigenvalues.\n"
        "- At a critical point: all λ > 0 → minimum, all λ < 0 → maximum, mixed signs → saddle, any λ = 0 → inconclusive.\n"
        "- **Newton** (−H⁻¹∇f) jumps to the quadratic model's critical point — superb near a minimum, but attracted by saddles and undefined when H is singular.\n"
        "- In deep learning: backprop = vector-Jacobian products; Hessian conditioning limits η; flat minima tend to generalise better."
    )
    c1, c2 = st.columns(2)
    with c1:
        safe_page_link("pages/81Taylor Series — Local Approximation.py", "← Previous: 81 · Taylor Series — Local Approximation")
    with c2:
        safe_page_link("pages/83Automatic Differentiation.py", "Next: 83 · Automatic Differentiation →")


main()
