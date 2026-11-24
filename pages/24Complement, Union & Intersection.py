import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="24 · Complement, Union & Intersection", page_icon="🔀", layout="wide")

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.nav import safe_page_link  # noqa: E402

EPS = 1e-9
BDAY_TRIALS = 4000
VENN_SAMPLES = 2000
NULL_EXPERIMENTS = 4000
COLORS = {"A": "#38bdf8", "B": "#f472b6", "both": "#c084fc", "none": "#334155", "result": "#fbbf24"}

SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_EVENTS = {
    "Heart ♥": lambda r, s: s == "♥",
    "Spade ♠": lambda r, s: s == "♠",
    "Red card (♥ or ♦)": lambda r, s: s in "♥♦",
    "Face card (J, Q, K)": lambda r, s: r in ("J", "Q", "K"),
    "King": lambda r, s: r == "K",
    "Ace": lambda r, s: r == "A",
    "Number card (2–10)": lambda r, s: r not in ("A", "J", "Q", "K"),
}
DICE_EVENTS = {
    "Sum = 7": lambda a, b: a + b == 7,
    "Doubles": lambda a, b: a == b,
    "At least one 6": lambda a, b: a == 6 or b == 6,
    "First die even": lambda a, b: a % 2 == 0,
    "Sum ≥ 10": lambda a, b: a + b >= 10,
    "Both dice ≤ 3": lambda a, b: a <= 3 and b <= 3,
}
OPERATIONS = ["A ∪ B (A or B)", "A ∩ B (A and B)", "Aᶜ (not A)", "A ∩ Bᶜ (A but not B)", "(A ∪ B)ᶜ = Aᶜ ∩ Bᶜ (neither)"]


def style(fig, title, height=380):
    fig.update_layout(
        title=title,
        height=height,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=40),
        legend=dict(orientation="h", y=-0.2),
    )
    return fig


def bump_seed():
    st.session_state["p24_seed"] = st.session_state.get("p24_seed", 0) + 1


def rng(offset):
    return np.random.default_rng(2400 + 1000 * st.session_state.get("p24_seed", 0) + offset)


def frac_tex(fr):
    return str(fr.numerator) if fr.denominator == 1 else rf"\tfrac{{{fr.numerator}}}{{{fr.denominator}}}"


# ---------------------------------------------------------------- 1. complement / birthday
def birthday_exact(n):
    """P(at least two of n people share a birthday), 365 equally likely days, via the complement."""
    if n > 365:
        return 1.0
    p_none = 1.0
    for k in range(n):
        p_none *= (365 - k) / 365
    return 1.0 - p_none


def birthday_simulated(n, trials):
    days = np.sort(rng(1).integers(0, 365, size=(trials, n)), axis=1)
    return float((np.diff(days, axis=1) == 0).any(axis=1).mean())


def render_birthday_lab():
    st.header("1) The complement rule and the “at least one” trick")
    st.markdown(
        r"""
        Every outcome is either in $A$ or not in $A$ — never both, never neither. So
        $P(A) + P(A^c) = 1$, i.e. **$P(A^c) = 1 - P(A)$**.

        That sounds trivial, but it is the single most useful trick in probability: “**at least one** …” events are
        a mess of overlapping cases, while their complement “**none at all**” is usually one clean product.
        """
    )
    c1, c2 = st.columns([1, 2])
    with c1:
        n = st.slider("People in the room (n)", 1, 100, 23, key="p24_n")
        p_exact = birthday_exact(n)
        p_sim = birthday_simulated(n, BDAY_TRIALS)
        se = math.sqrt(max(p_sim * (1 - p_sim), 0.0) / BDAY_TRIALS)
        st.metric("Exact P(some shared birthday)", f"{p_exact:.4f}")
        st.metric(f"Simulated ({BDAY_TRIALS:,} random rooms)", f"{p_sim:.4f}", f"{p_sim - p_exact:+.4f} vs exact")
        st.caption(f"Simulation noise: ±{1.96 * se:.4f} (≈95%). Pairs of people that could match: C({n},2) = {math.comb(n, 2):,}.")
        st.button("🎲 Resample", key="p24_resample_bday", on_click=bump_seed)
    with c2:
        ns = np.arange(1, 101)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ns, y=[birthday_exact(k) for k in ns], name="exact 1 − P(no match)",
                                 line=dict(color=COLORS["A"], width=3)))
        fig.add_trace(go.Scatter(x=ns, y=[1 - birthday_exact(k) for k in ns], name="P(no match) = P(Aᶜ)",
                                 line=dict(color="#94a3b8", dash="dot")))
        fig.add_trace(go.Scatter(x=ns, y=np.minimum(ns / 365, 1), name="naive guess n/365",
                                 line=dict(color="#f87171", dash="dash")))
        fig.add_trace(go.Scatter(x=[n], y=[p_sim], mode="markers", name="simulated at n",
                                 marker=dict(color=COLORS["result"], size=13, symbol="diamond"),
                                 error_y=dict(type="data", array=[1.96 * se], visible=True)))
        fig.add_hline(y=0.5, line_dash="dot", line_color="#64748b")
        fig.update_xaxes(title="n people")
        fig.update_yaxes(title="probability", range=[-0.02, 1.02])
        st.plotly_chart(style(fig, "Birthday problem: P(at least one shared birthday)"), width="stretch")

    shown = min(n, 4)
    factors = r" \cdot ".join(rf"\frac{{{365 - k}}}{{365}}" for k in range(shown))
    if n > shown:
        factors += rf" \cdots \frac{{{365 - n + 1}}}{{365}}"
    st.latex(rf"P(\text{{no shared birthday}}) = {factors} = {1 - p_exact:.4f}")
    st.latex(rf"P(\text{{at least one shared}}) = 1 - {1 - p_exact:.4f} = {p_exact:.4f}")
    st.info(
        "Why it surprises people: the naive n/365 counts *one person vs. one fixed day*, but a match can happen in any "
        f"of the C(n,2) = {math.comb(n, 2):,} pairs. With 23 people that's already 253 chances — enough to pass 50%."
    )
    return n, p_exact


# ---------------------------------------------------------------- 2. addition rule / Venn
def lens_area(r1, r2, d):
    if d >= r1 + r2:
        return 0.0
    if d <= abs(r1 - r2):
        return math.pi * min(r1, r2) ** 2
    a1 = r1**2 * math.acos(np.clip((d**2 + r1**2 - r2**2) / (2 * d * r1), -1, 1))
    a2 = r2**2 * math.acos(np.clip((d**2 + r2**2 - r1**2) / (2 * d * r2), -1, 1))
    k = max((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2), 0.0)
    return a1 + a2 - 0.5 * math.sqrt(k)


def centre_distance(r1, r2, target):
    """Distance between circle centres whose overlap (lens) area equals target (bisection; lens area falls with d)."""
    lo, hi = abs(r1 - r2), r1 + r2
    if target <= EPS:
        return hi
    if target >= math.pi * min(r1, r2) ** 2 - EPS:
        return lo
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if lens_area(r1, r2, mid) > target else (lo, mid)
    return (lo + hi) / 2


def venn_figure(pa, pb, pab):
    scale = 1.2  # circle area = π·scale²·P, so areas (and the overlap) are to scale
    ra, rb = scale * math.sqrt(pa), scale * math.sqrt(pb)
    d = centre_distance(ra, rb, math.pi * scale**2 * pab) if ra > 0 and rb > 0 else ra + rb
    xa, xb = -d / 2, d / 2
    fig = go.Figure()
    fig.add_shape(type="rect", x0=-1.7, y0=-1.0, x1=1.7, y1=1.0, line=dict(color="#94a3b8"))
    for name, x, r in (("A", xa, ra), ("B", xb, rb)):
        if r > 0:
            fig.add_shape(type="circle", x0=x - r, y0=-r, x1=x + r, y1=r, line=dict(color=COLORS[name], width=3),
                          fillcolor=COLORS[name], opacity=0.35)
            fig.add_annotation(x=x, y=r + 0.08, text=f"<b>{name}</b>", showarrow=False, font=dict(color=COLORS[name], size=16))
    fig.add_annotation(x=-1.6, y=0.9, text="Ω", showarrow=False, xanchor="left", font=dict(size=18, color="#cbd5e1"))
    fig.update_xaxes(visible=False, range=[-1.75, 1.75])
    fig.update_yaxes(visible=False, range=[-1.05, 1.05], scaleanchor="x")
    return style(fig, "Venn diagram — circle and overlap areas to scale", 340)


def ruler_figure(pa, pb, pab):
    """Ω as the unit interval: A = [0, P(A)], B starts where it must to overlap A by exactly P(A∩B)."""
    b0 = pa - pab
    fig = go.Figure()
    rows = [("Ω", 0.0, 1.0, "#475569"), ("A", 0.0, pa, COLORS["A"]), ("B", b0, pb, COLORS["B"]),
            ("A∩B", b0, pab, COLORS["both"]), ("A∪B", 0.0, pa + pb - pab, "#4ade80")]
    for name, base, length, color in rows:
        fig.add_trace(go.Bar(y=[name], x=[length], base=[base], orientation="h", marker_color=color,
                             text=[f"{length:.2f}"], textposition="inside", showlegend=False))
    fig.update_xaxes(range=[0, 1.0], title="probability mass (Ω has total length 1)")
    fig.update_yaxes(autorange="reversed")
    return style(fig, "Probability ruler — lengths add like probabilities", 340)


def set_mutually_exclusive():
    pa, pb = st.session_state.get("p24_pa", 0.5), st.session_state.get("p24_pb", 0.4)
    st.session_state["p24_pab"] = round(max(0.0, pa + pb - 1), 2)


def set_independent():
    pa, pb = st.session_state.get("p24_pa", 0.5), st.session_state.get("p24_pb", 0.4)
    st.session_state["p24_pab"] = round(pa * pb, 2)


def render_venn_lab():
    st.header("2) Union, intersection and the addition rule")
    st.markdown(
        r"""
        * **Intersection** $A \cap B$ — *both* happen (the overlap).
        * **Union** $A \cup B$ — *at least one* happens (A, or B, or both).

        Adding $P(A) + P(B)$ counts the overlap **twice**, so we subtract it once:
        """
    )
    st.latex(r"P(A \cup B) = P(A) + P(B) - P(A \cap B)")
    c1, c2, c3 = st.columns(3)
    # Defaults live in session state (no value=) because the buttons below write p24_pab via callbacks.
    for key, default in (("p24_pa", 0.5), ("p24_pb", 0.4), ("p24_pab", 0.15)):
        st.session_state.setdefault(key, default)
    pa = c1.slider("P(A)", 0.0, 1.0, step=0.01, key="p24_pa")
    pb = c2.slider("P(B)", 0.0, 1.0, step=0.01, key="p24_pb")
    pab_req = c3.slider("P(A ∩ B)", 0.0, 1.0, step=0.01, key="p24_pab")
    lo, hi = round(max(0.0, pa + pb - 1), 10), round(min(pa, pb), 10)
    st.caption(f"Valid range for P(A ∩ B) given these P(A), P(B): [{lo:.2f}, {hi:.2f}]")
    b1, b2 = st.columns(2)
    b1.button("Make A, B mutually exclusive (as far as possible)", key="p24_make_me", on_click=set_mutually_exclusive)
    b2.button("Make A, B independent (P(A∩B) = P(A)·P(B))", key="p24_make_ind", on_click=set_independent)

    pab = min(max(pab_req, lo), hi)
    if pab_req > hi + EPS:
        st.error(
            f"Impossible: P(A ∩ B) = {pab_req:.2f} exceeds min(P(A), P(B)) = {hi:.2f}. The overlap is part of A *and* "
            f"part of B, so it can't be bigger than either. Using the closest valid value, {pab:.2f}."
        )
    elif pab_req < lo - EPS:
        st.error(
            f"Impossible: P(A) + P(B) = {pa + pb:.2f} > 1, so the union would exceed 1 unless the overlap is at least "
            f"P(A) + P(B) − 1 = {lo:.2f}. Using the closest valid value, {pab:.2f}."
        )
    p_union = pa + pb - pab
    v1, v2 = st.columns(2)
    v1.plotly_chart(venn_figure(pa, pb, pab), width="stretch")
    v2.plotly_chart(ruler_figure(pa, pb, pab), width="stretch")

    m = st.columns(5)
    m[0].metric("P(A only) = P(A ∩ Bᶜ)", f"{max(pa - pab, 0.0):.2f}")
    m[1].metric("P(A ∩ B)", f"{pab:.2f}")
    m[2].metric("P(B only)", f"{max(pb - pab, 0.0):.2f}")
    m[3].metric("P(A ∪ B)", f"{p_union:.2f}", f"naive P(A)+P(B) = {pa + pb:.2f}", delta_color="off")
    m[4].metric("P(neither)", f"{max(1 - p_union, 0.0):.2f}")

    probs = np.clip([pa - pab, pab, pb - pab, 1 - p_union], 0, None)
    regions = rng(2).choice(4, size=VENN_SAMPLES, p=probs / probs.sum())
    n_a = int(np.isin(regions, [0, 1]).sum())
    n_b = int(np.isin(regions, [1, 2]).sum())
    n_ab = int((regions == 1).sum())
    n_u = int((regions != 3).sum())
    with st.container(border=True):
        st.markdown(f"**Simulate {VENN_SAMPLES:,} outcomes** from these probabilities and just count:")
        st.latex(rf"|A \cup B| = {n_u} = |A| + |B| - |A \cap B| = {n_a} + {n_b} - {n_ab}")
        st.caption(
            f"Empirical P(A ∪ B) = {n_u / VENN_SAMPLES:.3f} vs. theory {p_union:.3f}. For counts the identity holds "
            "*exactly* in every sample — the addition rule is just “don't count the overlap twice”."
        )
        st.button("🎲 Resample", key="p24_resample_venn", on_click=bump_seed)
    return pa, pb, pab


def render_exclusive_vs_independent(pa, pb, pab):
    st.subheader("Mutually exclusive ≠ independent (the #1 confusion)")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            r"""
            **Mutually exclusive (disjoint):** $A \cap B = \varnothing$, so $P(A \cap B) = 0$ and the addition rule
            simplifies to $P(A \cup B) = P(A) + P(B)$. *It's about sets — no overlap.*

            **Independent:** $P(A \cap B) = P(A)\,P(B)$, i.e. knowing B happened doesn't change the chance of A.
            *It's about information.*

            If $P(A), P(B) > 0$, disjoint events are **strongly dependent**: learning B happened tells you A
            certainly did *not*.
            """
        )
    with c2:
        exclusive = pab <= EPS
        independent = abs(pab - pa * pb) <= EPS
        st.markdown(f"With your sliders: $P(A)\\,P(B) = {pa:.2f} \\times {pb:.2f} = {pa * pb:.4f}$ and $P(A \\cap B) = {pab:.2f}$.")
        if pb > EPS:
            st.markdown(f"$P(A \\mid B) = P(A \\cap B)/P(B) = {pab / pb:.4f}$ vs. $P(A) = {pa:.2f}$.")
        else:
            st.markdown("$P(A \\mid B)$ is undefined because $P(B) = 0$.")
        if exclusive and independent:
            st.success("Both disjoint and independent — only possible because P(A) or P(B) is 0 (a trivial case).")
        elif exclusive:
            st.warning("Mutually exclusive → **dependent**: P(A ∩ B) = 0 but P(A)·P(B) > 0.")
        elif independent:
            st.success("Independent (and they overlap): P(A ∩ B) = P(A)·P(B).")
        elif abs(pab - pa * pb) < 0.005:
            st.info("Almost independent — P(A)·P(B) isn't on the 0.01 slider grid, so the overlap can only be close.")
        else:
            st.info("Overlapping and dependent — the most common situation in real data.")


def render_de_morgan(pa, pb, pab):
    st.header("3) De Morgan's laws — pushing a “not” inside")
    st.markdown(
        r"""
        “Not (rain **or** snow)” means “no rain **and** no snow”. “Not (rain **and** snow)” means “no rain **or** no snow”.
        Negating swaps $\cup \leftrightarrow \cap$:
        """
    )
    st.latex(r"(A \cup B)^c = A^c \cap B^c \qquad\qquad (A \cap B)^c = A^c \cup B^c")
    p_union = pa + pb - pab
    p_neither = 1 - pa - pb + pab
    st.latex(
        rf"P\big((A \cup B)^c\big) = 1 - {p_union:.2f} = {1 - p_union:.2f}"
        rf"\quad=\quad P(A^c \cap B^c) = 1 - P(A) - P(B) + P(A \cap B) = {p_neither:.2f}"
    )
    st.latex(
        rf"P(A^c \cup B^c) = P(A^c) + P(B^c) - P(A^c \cap B^c) = {1 - pa:.2f} + {1 - pb:.2f} - {p_neither:.2f}"
        rf" = {(1 - pa) + (1 - pb) - p_neither:.2f} = 1 - P(A \cap B)"
    )


# ---------------------------------------------------------------- 4. exact event builder
def build_space(kind):
    if kind.startswith("🃏"):
        cells = [(f"{r}{s}", lambda f, r=r, s=s: f(r, s), row, col) for row, s in enumerate(SUITS) for col, r in enumerate(RANKS)]
        return cells, CARD_EVENTS, RANKS, SUITS
    cells = [(f"{a},{b}", lambda f, a=a, b=b: f(a, b), a - 1, b - 1) for a in range(1, 7) for b in range(1, 7)]
    return cells, DICE_EVENTS, [f"die 2 = {b}" for b in range(1, 7)], [f"die 1 = {a}" for a in range(1, 7)]


def render_event_builder():
    st.header("4) Event builder — exact counts, exact fractions")
    kind = st.radio("Sample space", ["🃏 Standard deck (52 cards)", "🎲 Two dice (36 ordered pairs)"], horizontal=True, key="p24_space")
    cells, events, xlabels, ylabels = build_space(kind)
    names = list(events)
    c1, c2, c3 = st.columns(3)
    tag = "cards" if kind.startswith("🃏") else "dice"
    ev_a = c1.selectbox("Event A", names, index=0, key=f"p24_ev_a_{tag}")
    ev_b = c2.selectbox("Event B", names, index=4, key=f"p24_ev_b_{tag}")
    op = c3.selectbox("Combine into", OPERATIONS, key=f"p24_op_{tag}")

    in_a = np.array([test(events[ev_a]) for _, test, _, _ in cells])
    in_b = np.array([test(events[ev_b]) for _, test, _, _ in cells])
    result = {
        OPERATIONS[0]: in_a | in_b,
        OPERATIONS[1]: in_a & in_b,
        OPERATIONS[2]: ~in_a,
        OPERATIONS[3]: in_a & ~in_b,
        OPERATIONS[4]: ~in_a & ~in_b,
    }[op]
    total = len(cells)
    na, nb, nab, nu, nr = int(in_a.sum()), int(in_b.sum()), int((in_a & in_b).sum()), int((in_a | in_b).sum()), int(result.sum())

    region = np.where(in_a & in_b, 3, np.where(in_a, 1, np.where(in_b, 2, 0)))
    rows, cols = len(ylabels), len(xlabels)
    z = np.zeros((rows, cols))
    text = [["" for _ in range(cols)] for _ in range(rows)]
    for (label, _, r, c), reg, hit in zip(cells, region, result):
        z[r, c] = reg
        text[r][c] = f"<b>{label}</b>" if hit else label
    scale = [[0.0, COLORS["none"]], [0.25, COLORS["none"]], [0.25, COLORS["A"]], [0.5, COLORS["A"]],
             [0.5, COLORS["B"]], [0.75, COLORS["B"]], [0.75, COLORS["both"]], [1.0, COLORS["both"]]]
    fig = go.Figure(go.Heatmap(z=z, x=xlabels, y=ylabels, zmin=-0.5, zmax=3.5, colorscale=scale, showscale=False,
                               text=text, texttemplate="%{text}", xgap=3, ygap=3, hoverinfo="text"))
    hits = [(xlabels[c], ylabels[r]) for (_, _, r, c), hit in zip(cells, result) if hit]
    if hits:
        fig.add_trace(go.Scatter(x=[h[0] for h in hits], y=[h[1] for h in hits], mode="markers", name="in result",
                                 marker=dict(symbol="square-open", size=34, color=COLORS["result"], line=dict(width=3))))
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(style(fig, "Blue = A only · pink = B only · purple = both · gold frame = result", 360 if rows == 4 else 420), width="stretch")

    fa, fb, fab, fu, fr = (Fraction(k, total) for k in (na, nb, nab, nu, nr))
    m = st.columns(4)
    m[0].metric("|A|", f"{na} / {total}", f"P = {fa}", delta_color="off")
    m[1].metric("|B|", f"{nb} / {total}", f"P = {fb}", delta_color="off")
    m[2].metric("|A ∩ B|", f"{nab} / {total}", f"P = {fab}", delta_color="off")
    m[3].metric(f"Result: {op.split(' (')[0]}", f"{nr} / {total}", f"P = {fr} ≈ {float(fr):.4f}", delta_color="off")
    st.latex(
        rf"P(A \cup B) = {frac_tex(fa)} + {frac_tex(fb)} - {frac_tex(fab)} = {frac_tex(fu)}"
        rf"\qquad P\big((A\cup B)^c\big) = 1 - {frac_tex(fu)} = {frac_tex(1 - fu)}"
    )
    if nab == 0:
        verdict = "mutually exclusive" + (" — and therefore dependent" if na and nb else "")
    elif fab == fa * fb:
        verdict = f"independent: {fab} = {fa} × {fb}"
    else:
        verdict = f"dependent: P(A∩B) = {fab} but P(A)·P(B) = {fa * fb}"
    st.caption(f"A and B are **{verdict}**. Try Heart & King (independent), Heart & Spade (disjoint), Sum = 7 & First die even.")
    if nr == 0:
        st.info("The result is the empty event ∅ — probability exactly 0.")


# ---------------------------------------------------------------- 5. AI connection
def render_ai(n, p_bday, pa, pb, pab):
    st.header("5) Worked example with your numbers")
    p_union = pa + pb - pab
    st.latex(rf"P(A \cup B) = {pa:.2f} + {pb:.2f} - {pab:.2f} = {p_union:.2f},\qquad P(A^c) = 1 - {pa:.2f} = {1 - pa:.2f}")
    st.latex(rf"P(\text{{no match among {n} people}}) = {1 - p_bday:.4f} \;\Rightarrow\; P(\text{{match}}) = {p_bday:.4f}")
    st.latex(r"P(\text{at least one six in 4 rolls}) = 1 - \left(\tfrac{5}{6}\right)^4 = 1 - \tfrac{625}{1296} = \tfrac{671}{1296} \approx 0.5177")

    st.header("6) AI connection — “at least one false positive”")
    st.markdown(
        r"""
        Evaluate a model on $m$ benchmarks, run $m$ A/B tests, or check $m$ features for significance, each at level
        $\alpha$. If nothing is really going on, each test still fires by chance with probability $\alpha$.
        The chance of **at least one** false alarm (the *family-wise error rate*) is a complement:
        """
    )
    st.latex(r"\text{FWER} = 1 - (1-\alpha)^m \;\;(\text{independent tests})\qquad \text{FWER} \le m\alpha \;\;(\text{union bound, always})")
    c1, c2 = st.columns([1, 2])
    with c1:
        m = st.slider("Number of tests m", 1, 200, 20, key="p24_m")
        alpha = st.selectbox("Per-test level α", [0.10, 0.05, 0.01, 0.001], index=1, key="p24_alpha")
        fwer = 1 - (1 - alpha) ** m
        sim = float((rng(3).random((NULL_EXPERIMENTS, m)) < alpha).any(axis=1).mean())
        st.metric("P(≥ 1 false positive)", f"{fwer:.4f}", f"simulated {sim:.4f}", delta_color="off")
        st.metric("Union bound m·α", f"{m * alpha:.3f}" + (" (≥ 1: says nothing)" if m * alpha >= 1 else ""))
        st.metric("Bonferroni (α/m per test)", f"{1 - (1 - alpha / m) ** m:.4f}", f"≤ α = {alpha}", delta_color="off")
        st.button("🎲 Resample", key="p24_resample_fwer", on_click=bump_seed)
    with c2:
        ms = np.arange(1, 201)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ms, y=1 - (1 - alpha) ** ms, name="1 − (1−α)^m", line=dict(color=COLORS["A"], width=3)))
        fig.add_trace(go.Scatter(x=ms, y=np.minimum(ms * alpha, 1), name="union bound min(1, mα)", line=dict(color="#f87171", dash="dash")))
        fig.add_trace(go.Scatter(x=ms, y=1 - (1 - alpha / ms) ** ms, name="with Bonferroni α/m", line=dict(color="#4ade80")))
        fig.add_trace(go.Scatter(x=[m], y=[sim], mode="markers", name=f"simulated ({NULL_EXPERIMENTS:,} runs)",
                                 marker=dict(color=COLORS["result"], size=12, symbol="diamond")))
        fig.update_xaxes(title="number of tests m")
        fig.update_yaxes(title="P(at least one false positive)", range=[0, 1.02])
        st.plotly_chart(style(fig, f"Family-wise error rate, α = {alpha}"), width="stretch")
    st.markdown(
        r"""
        **Where this shows up in ML**
        * **Benchmark / hyper-parameter fishing:** try 20 random seeds or prompts and report the best → with
          $\alpha = 0.05$ there's a 64% chance at least one looks “significant” by luck.
        * **pass@k for code models:** $P(\text{at least one of } k \text{ samples passes}) = 1 - (1-p)^k$ (for independent
          samples with pass rate $p$); the unbiased estimator $1 - \binom{n-c}{k}/\binom{n}{k}$ is a complement too.
        * **Union bound in learning theory:** for a finite hypothesis class $\mathcal H$,
          $P(\exists h: |\hat R(h) - R(h)| > \varepsilon) \le \sum_h P(\cdot) \le 2|\mathcal H|e^{-2n\varepsilon^2}$ —
          the reason generalization bounds grow with $\log|\mathcal H|$.
        * **Safety & monitoring:** a guardrail that fails 1% of the time per request lets *at least one* attack through
          in 1,000 attempts with probability $1 - 0.99^{1000} \approx 0.99996$.
        """
    )


def main():
    st.session_state.setdefault("p24_seed", 0)
    st.title("🔀 Page 24: Complement, Union & Intersection")
    st.markdown(
        r"""
        On page 23 events were subsets of the sample space $\Omega$. Now we **combine** them: *not* A ($A^c$),
        A *or* B ($A \cup B$), A *and* B ($A \cap B$). Three rules cover almost everything:
        """
    )
    st.latex(r"P(A^c) = 1 - P(A) \qquad P(A \cup B) = P(A) + P(B) - P(A \cap B) \qquad (A \cup B)^c = A^c \cap B^c")
    st.markdown(
        "**Why it matters for AI:** model evaluation is full of “at least one” questions — *at least one* false "
        "positive across many tests, *at least one* correct sample out of k, *at least one* failure in a pipeline."
    )
    st.divider()
    n, p_bday = render_birthday_lab()
    st.divider()
    pa, pb, pab = render_venn_lab()
    render_exclusive_vs_independent(pa, pb, pab)
    st.divider()
    render_de_morgan(pa, pb, pab)
    st.divider()
    render_event_builder()
    st.divider()
    render_ai(n, p_bday, pa, pb, pab)
    st.divider()
    st.success(
        r"""
        **Key takeaways**
        - **Complement:** $P(A^c) = 1 - P(A)$. For “at least one”, compute “none” and subtract from 1.
        - **Addition rule:** $P(A \cup B) = P(A) + P(B) - P(A \cap B)$ — never count the overlap twice.
        - The overlap is boxed in: $\max(0, P(A)+P(B)-1) \le P(A \cap B) \le \min(P(A), P(B))$.
        - **Disjoint ≠ independent:** disjoint means $P(A \cap B)=0$; independent means $P(A \cap B)=P(A)P(B)$.
        - **De Morgan:** a “not” flips $\cup \leftrightarrow \cap$.
        - Many tests ⇒ many chances to be fooled: $1-(1-\alpha)^m \le m\alpha$.
        """
    )
    c1, c2 = st.columns(2)
    with c1:
        safe_page_link("pages/23Sample Space & Basic Probability.py", "← Previous: Sample Space & Basic Probability", icon="🎲")
    with c2:
        safe_page_link("pages/25Conditional Probability.py", "Next: Conditional Probability →", icon="🎯")


main()
