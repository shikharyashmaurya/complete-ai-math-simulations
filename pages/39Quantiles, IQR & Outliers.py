import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sklearn.preprocessing import RobustScaler, StandardScaler

st.set_page_config(page_title="39 · Quantiles, IQR & Outliers", page_icon="📦", layout="wide")

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.nav import safe_page_link  # noqa: E402

PRESETS = [
    "Symmetric — normal",
    "Right-skewed — log-normal (latencies, incomes)",
    "Left-skewed — exam scores near a ceiling",
    "Heavy-tailed — Student t (df = 2)",
    "Flat — uniform (no tails)",
]
METHODS = ["linear", "lower", "higher", "nearest", "midpoint", "inverted_cdf", "hazen", "weibull", "median_unbiased"]
STEPS = ["1 · Sort the data", "2 · Median", "3 · Quartiles → box", "4 · Tukey fences", "5 · Whiskers & outliers"]
BASE_LATENCIES = [42, 45, 47, 48, 50, 51, 53, 55, 58]
C = {"data": "#38bdf8", "median": "#06b6d4", "box": "#a78bfa", "mean": "#ef4444", "fence": "#fbbf24",
     "out": "#f87171", "z": "#fb923c", "ok": "#4ade80"}


def style(fig, title, height=380):
    fig.update_layout(
        title=title, height=height, template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=40), legend=dict(orientation="h", y=-0.22),
    )
    return fig


def bump_seed():
    st.session_state["p39_seed"] = st.session_state.get("p39_seed", 0) + 1


def make_data(preset, n, seed):
    rng = np.random.default_rng(3900 + 1000 * seed + PRESETS.index(preset))
    if preset == PRESETS[0]:
        return rng.normal(50, 10, n)
    if preset == PRESETS[1]:
        return rng.lognormal(3.5, 0.6, n)
    if preset == PRESETS[2]:
        return 100 - rng.gamma(2.0, 6.0, n)
    if preset == PRESETS[3]:
        return 50 + 5 * rng.standard_t(2, n)
    return rng.uniform(0, 100, n)


def tukey(x, k=1.5, method="linear"):
    q1, med, q3 = np.quantile(x, [0.25, 0.5, 0.75], method=method)
    iqr = q3 - q1
    lf, uf = q1 - k * iqr, q3 + k * iqr
    inside = x[(x >= lf) & (x <= uf)]
    # Whiskers reach the most extreme data points still inside the fences.
    w_lo, w_hi = (inside.min(), inside.max()) if inside.size else (med, med)
    return dict(q1=q1, med=med, q3=q3, iqr=iqr, lf=lf, uf=uf, w_lo=w_lo, w_hi=w_hi, out=(x < lf) | (x > uf))


def z_scores(x):
    sd = x.std()  # ÷n, like StandardScaler
    return np.zeros_like(x) if sd == 0 else (x - x.mean()) / sd


# ---------------------------------------------------------------- lab 1: five-number summary & box plot
def box_figure(x, t, step, jitter):
    fig = go.Figure()
    order = np.argsort(np.argsort(x))
    show_out = step >= 4
    colors = np.where(t["out"], C["out"], C["data"]) if show_out else order
    fig.add_trace(go.Scatter(x=x, y=0.75 + jitter, mode="markers", name="data",
                             marker=dict(color=colors, colorscale="Viridis", size=6, opacity=0.8),
                             hovertemplate="%{x:.2f}<extra></extra>"))
    if step >= 1:
        fig.add_shape(type="line", x0=t["med"], x1=t["med"], y0=-0.3, y1=1.05, line=dict(color=C["median"], width=3))
        fig.add_annotation(x=t["med"], y=1.12, text=f"median {t['med']:.2f}", showarrow=False, font=dict(color=C["median"]))
    if step >= 2:
        fig.add_shape(type="rect", x0=t["q1"], x1=t["q3"], y0=-0.25, y1=0.25, line=dict(color=C["box"], width=2),
                      fillcolor="rgba(167,139,250,0.25)")
        for name, v in (("Q1", t["q1"]), ("Q3", t["q3"])):
            fig.add_annotation(x=v, y=-0.38, text=f"{name} {v:.2f}", showarrow=False, font=dict(color=C["box"]))
    if step >= 3:
        for name, v in (("lower fence", t["lf"]), ("upper fence", t["uf"])):
            fig.add_shape(type="line", x0=v, x1=v, y0=-0.45, y1=1.05, line=dict(color=C["fence"], dash="dash"))
            fig.add_annotation(x=v, y=-0.55, text=f"{name} {v:.2f}", showarrow=False, font=dict(color=C["fence"]))
    if step >= 4:
        for a, b in ((t["w_lo"], t["q1"]), (t["q3"], t["w_hi"])):
            fig.add_shape(type="line", x0=a, x1=b, y0=0, y1=0, line=dict(color=C["box"], width=2))
        for v in (t["w_lo"], t["w_hi"]):
            fig.add_shape(type="line", x0=v, x1=v, y0=-0.12, y1=0.12, line=dict(color=C["box"], width=2))
        outs = x[t["out"]]
        if outs.size:
            fig.add_trace(go.Scatter(x=outs, y=np.zeros(outs.size), mode="markers", name="outliers",
                                     marker=dict(color=C["out"], size=9, symbol="circle-open", line=dict(width=2))))
    fig.update_yaxes(visible=False, range=[-0.7, 1.25])
    fig.update_xaxes(title="value")
    return style(fig, "Box plot, built step by step", 400)


STEP_NOTES = [
    "Every dot is one data point (colour = rank after sorting). Quantiles are all about **positions in the sorted list**.",
    "The **median** (50th percentile) splits the sorted data into two equal halves.",
    "**Q1** (25th) and **Q3** (75th percentiles) bound the middle 50% of the data — that's the **box**. Its width is the **IQR = Q3 − Q1**.",
    "Tukey's **fences** sit k·IQR beyond the box (k = 1.5 is the classic choice; 3 marks “far out” points).",
    "**Whiskers** stretch to the most extreme points *inside* the fences; anything beyond is flagged as an **outlier**.",
]


def render_box_lab():
    st.header("1) Quantiles, the five-number summary and the box plot")
    st.markdown(
        r"""
        The **p-quantile** $Q(p)$ is the value below which a fraction $p$ of the data lies (the **100p-th percentile**).
        $Q(0.5)$ is the median, $Q(0.25)$ and $Q(0.75)$ are the quartiles **Q1** and **Q3**.
        The **five-number summary** is *min, Q1, median, Q3, max*, and the **IQR** $= Q3 - Q1$ is the width of the middle half.
        """
    )
    c = st.columns([2, 2, 1.4, 1.4, 1])
    preset = c[0].selectbox("Dataset", PRESETS, key="p39_preset")
    n = c[1].slider("Sample size n", 10, 1000, 200, 10, key="p39_n")
    k = c[2].slider("Fence multiplier k", 0.5, 3.0, 1.5, 0.25, key="p39_k")
    method = c[3].selectbox("Interpolation", METHODS, key="p39_method", help="numpy's default is 'linear'")
    c[4].button("🎲 Resample", key="p39_resample", on_click=bump_seed)

    seed = st.session_state.get("p39_seed", 0)
    x = make_data(preset, n, seed)
    t = tukey(x, k, method)
    z = z_scores(x)
    m = st.columns(6)
    for col, (label, v) in zip(m, [("min", x.min()), ("Q1", t["q1"]), ("median", t["med"]), ("Q3", t["q3"]),
                                    ("max", x.max()), ("IQR", t["iqr"])]):
        col.metric(label, f"{v:.2f}")

    step = STEPS.index(st.select_slider("Build the box plot", STEPS, value=STEPS[-1], key="p39_step"))
    jitter = np.random.default_rng(39 + seed).uniform(-0.2, 0.2, n)
    tab1, tab2 = st.tabs(["📦 Box plot", "📊 Histogram + quartiles"])
    with tab1:
        st.plotly_chart(box_figure(x, t, step, jitter), width="stretch")
        st.markdown(STEP_NOTES[step])
    with tab2:
        fig = go.Figure(go.Histogram(x=x, nbinsx=40, marker_color=C["data"], opacity=0.75, name="data"))
        for name, v, col, dash in (("Q1", t["q1"], C["box"], "dot"), ("median", t["med"], C["median"], "solid"),
                                   ("Q3", t["q3"], C["box"], "dot"), ("mean", x.mean(), C["mean"], "dash")):
            fig.add_vline(x=v, line_color=col, line_dash=dash, annotation_text=name, annotation_font_color=col)
        st.plotly_chart(style(fig, "Histogram with quartiles and mean"), width="stretch")

    bowley = (t["q3"] + t["q1"] - 2 * t["med"]) / t["iqr"] if t["iqr"] > 0 else float("nan")
    n_iqr, n_z = int(t["out"].sum()), int((np.abs(z) > 3).sum())
    s1, s2, s3 = st.columns(3)
    s1.metric("Outliers (Tukey, k·IQR)", f"{n_iqr} ({n_iqr / n:.1%})")
    s2.metric("Outliers (|z| > 3)", f"{n_z} ({n_z / n:.1%})")
    s3.metric("Quartile skewness (Q3+Q1−2·median)/IQR", "undefined (IQR = 0)" if np.isnan(bowley) else f"{bowley:+.3f}")
    gap = (x.mean() - t["med"]) / x.std() if x.std() > 0 else 0.0
    st.caption(
        f"Mean {x.mean():.2f} vs median {t['med']:.2f} (gap {gap:+.2f} SD) — a long right tail drags the mean above "
        "the median, a long left tail drags it below; symmetric data keep them close. "
        "For perfectly normal data, Tukey's 1.5·IQR fences sit at ±2.698σ and flag about 0.70% of points; "
        "|z| > 3 flags about 0.27%. Skewed or heavy-tailed data flag many more — often correctly."
    )
    with st.expander("Interpolation methods — why Q1 can differ between tools"):
        st.markdown(
            r"""
            With $n$ sorted values $x_{(1)} \le \dots \le x_{(n)}$, the p-quantile usually falls *between* two of them.
            numpy's default **linear** method (also pandas, R type 7, Excel `PERCENTILE.INC`) uses position
            $h = 1 + (n-1)p$ and interpolates: $Q(p) = x_{(\lfloor h \rfloor)} + (h - \lfloor h \rfloor)\,(x_{(\lfloor h \rfloor + 1)} - x_{(\lfloor h \rfloor)})$.
            Other conventions (`weibull` = Excel `PERCENTILE.EXC`, `inverted_cdf` = the ECDF inverse, …) pick
            slightly different positions. Differences vanish as $n$ grows, but matter for small samples — try n = 10.
            """
        )
        table = pd.DataFrame(
            {meth: np.quantile(x, [0.25, 0.5, 0.75], method=meth) for meth in METHODS}, index=["Q1", "median", "Q3"]
        ).T
        table["IQR"] = table["Q3"] - table["Q1"]
        st.dataframe(table.round(3), width="stretch")
    return x, preset


# ---------------------------------------------------------------- lab 2: robustness
def render_robustness_lab():
    st.header("2) Robustness: drag one outlier")
    st.markdown(
        "Ten API response times (ms). Nine are fixed; **you control the tenth**. Watch which statistics panic."
    )
    c1, c2 = st.columns(2)
    xv = c1.slider("Tenth latency (ms)", 0, 1000, 150, key="p39_x")
    zthr = c2.slider("z-score threshold", 2.0, 3.5, 3.0, 0.1, key="p39_zthr")
    data = np.array(BASE_LATENCIES + [xv], dtype=float)
    t = tukey(data)
    mean, sd = data.mean(), data.std()
    z_x = 0.0 if sd == 0 else (xv - mean) / sd
    out_iqr, out_z = bool(t["out"][-1]), abs(z_x) > zthr

    m = st.columns(6)
    m[0].metric("mean", f"{mean:.2f}")
    m[1].metric("median", f"{t['med']:.2f}")
    m[2].metric("SD (÷n)", f"{sd:.2f}")
    m[3].metric("IQR", f"{t['iqr']:.2f}")
    m[4].metric("Tukey 1.5·IQR", "🚩 outlier" if out_iqr else "inside fences", f"fences [{t['lf']:.2f}, {t['uf']:.2f}]", delta_color="off")
    m[5].metric(f"|z| > {zthr:.1f}", "🚩 outlier" if out_z else "not flagged", f"z = {z_x:+.3f}", delta_color="off")

    fig = go.Figure()
    fig.add_trace(go.Bar(y=["Tukey fences"], x=[t["uf"] - t["lf"]], base=[t["lf"]], orientation="h",
                         marker_color="rgba(74,222,128,0.35)", name="inside Tukey fences"))
    fig.add_trace(go.Bar(y=[f"mean ± {zthr:.1f}·SD"], x=[2 * zthr * sd], base=[mean - zthr * sd], orientation="h",
                         marker_color="rgba(251,146,60,0.35)", name=f"|z| ≤ {zthr:.1f}"))
    for row in ("Tukey fences", f"mean ± {zthr:.1f}·SD"):
        fig.add_trace(go.Scatter(x=data, y=[row] * data.size, mode="markers", showlegend=False,
                                 marker=dict(color=[C["data"]] * 9 + [C["fence"]], size=[9] * 9 + [15],
                                             line=dict(color="white", width=1))))
    fig.add_vline(x=mean, line_color=C["mean"], line_dash="dash", annotation_text="mean", annotation_font_color=C["mean"])
    fig.add_vline(x=t["med"], line_color=C["median"], annotation_text="median", annotation_position="bottom right",
                  annotation_font_color=C["median"])
    fig.update_layout(barmode="overlay")
    fig.update_xaxes(title="latency (ms) — gold dot is yours")
    st.plotly_chart(style(fig, "The z-band stretches to swallow the outlier; the fences don't move", 330), width="stretch")

    sweep = np.arange(0, 1001, 5, dtype=float)
    stats = {"mean": [], "SD": [], "median": [], "IQR": []}
    for v in sweep:
        d = np.array(BASE_LATENCIES + [v])
        q1, med, q3 = np.quantile(d, [0.25, 0.5, 0.75])
        stats["mean"].append(d.mean())
        stats["SD"].append(d.std())
        stats["median"].append(med)
        stats["IQR"].append(q3 - q1)
    fig2 = go.Figure()
    for name, col, dash in (("mean", C["mean"], "solid"), ("SD", C["z"], "dash"), ("median", C["median"], "solid"), ("IQR", C["box"], "dash")):
        fig2.add_trace(go.Scatter(x=sweep, y=stats[name], name=name, line=dict(color=col, dash=dash, width=3)))
    fig2.add_vline(x=xv, line_color=C["fence"], line_dash="dot")
    fig2.update_xaxes(title="value of the tenth latency")
    fig2.update_yaxes(title="statistic", type="log")
    st.plotly_chart(style(fig2, "Mean & SD grow without limit; median & IQR stay put (log scale)", 360), width="stretch")
    st.warning(
        r"""
        **The masking effect.** The outlier inflates the SD it is measured against. With population SD, no point can
        ever have $|z| > \sqrt{n-1}$ (Samuelson's inequality); here $n = 10$, so $|z| < 3$ always — the classic
        $|z|>3$ rule **can never flag a single outlier in 10 points**, however absurd. Tukey's fences use the median
        half of the data, so the outlier can't hide. (Page 35 introduced z-scores; they assume roughly normal data.)
        """
    )
    st.markdown(
        "**Breakdown point** — the fraction of data you must corrupt to drag a statistic arbitrarily far: "
        "mean & SD **0%** (one point is enough), IQR **25%**, median **50%**."
    )
    return data, t, xv


def render_ecdf_lab(x, preset):
    st.header("3) The ECDF — reading quantiles off a curve")
    st.markdown(
        r"""
        The **empirical CDF** $\hat F(v) = \frac{\#\{x_i \le v\}}{n}$ climbs by $1/n$ at each data point.
        A quantile is the **reverse lookup**: pick a height $p$ and read off the value. The step-function inverse is
        numpy's `inverted_cdf`; the default `linear` method instead joins the points $(x_{(i)}, \tfrac{i-1}{n-1})$ with straight lines.
        """
    )
    c1, c2 = st.columns([1, 2.4])
    with c1:
        p = st.slider("Quantile level p", 0.0, 1.0, 0.9, 0.01, key="p39_p")
        q_lin = float(np.quantile(x, p))
        q_inv = float(np.quantile(x, p, method="inverted_cdf"))
        st.metric(f"Q({p:.2f}) — linear (numpy default)", f"{q_lin:.3f}")
        st.metric(f"Q({p:.2f}) — inverted ECDF", f"{q_inv:.3f}")
        st.metric(f"F̂({q_lin:.2f}) = fraction ≤ Q", f"{np.mean(x <= q_lin):.3f}")
        p50, p95, p99 = np.quantile(x, [0.5, 0.95, 0.99])
        st.caption(f"p50 = {p50:.2f} · p95 = {p95:.2f} · p99 = {p99:.2f} — how latency SLOs are written.")
    with c2:
        s = np.sort(x)
        n = s.size
        step_x = np.concatenate([[s[0]], s])
        step_y = np.concatenate([[0.0], np.arange(1, n + 1) / n])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=step_x, y=step_y, mode="lines", line_shape="hv", name="ECDF F̂",
                                 line=dict(color=C["data"], width=2)))
        fig.add_trace(go.Scatter(x=s, y=np.linspace(0, 1, n), mode="lines", name="numpy 'linear' interpolation",
                                 line=dict(color=C["box"], dash="dot")))
        fig.add_trace(go.Scatter(x=[s[0], q_lin, q_lin], y=[p, p, 0], mode="lines+markers", name=f"lookup p = {p:.2f}",
                                 line=dict(color=C["fence"], width=2), marker=dict(size=[0, 10, 0])))
        fig.update_xaxes(title="value")
        fig.update_yaxes(title="cumulative fraction", range=[-0.02, 1.02])
        st.plotly_chart(style(fig, f"ECDF of “{preset.split(' — ')[0]}” data (n = {n})", 400), width="stretch")


def render_worked_example(data, t, xv):
    st.header("4) Worked example — your ten latencies")
    s = np.sort(data)
    n = s.size
    st.markdown("Sorted: " + ", ".join(f"**{v:g}**" if v == xv else f"{v:g}" for v in s))

    def line(p, name):
        h = 1 + (n - 1) * p
        j = int(np.floor(h))
        frac = h - j
        lo, hi = s[j - 1], s[min(j, n - 1)]
        val = lo + frac * (hi - lo)
        st.latex(
            rf"{name}:\; h = 1 + {n - 1}\times{p} = {h:g},\quad x_{{({j})}} + {frac:g}\,(x_{{({min(j + 1, n)})}} - x_{{({j})}})"
            rf" = {lo:g} + {frac:g}\times({hi:g} - {lo:g}) = {val:g}"
        )

    line(0.25, "Q1")
    line(0.5, r"\text{median}")
    line(0.75, "Q3")
    st.latex(
        rf"\text{{IQR}} = {t['q3']:g} - {t['q1']:g} = {t['iqr']:g},\qquad"
        rf"\text{{fences}} = [{t['q1']:g} - 1.5\times{t['iqr']:g},\; {t['q3']:g} + 1.5\times{t['iqr']:g}] = [{t['lf']:g},\, {t['uf']:g}]"
    )
    mean, sd = data.mean(), data.std()
    z_x = 0.0 if sd == 0 else (xv - mean) / sd
    verdict = "outside → outlier" if (xv < t["lf"] or xv > t["uf"]) else "inside → not an outlier"
    st.latex(
        rf"\text{{Your point }} {xv}\text{{ is {verdict}.}}\qquad z = \frac{{{xv} - {mean:.2f}}}{{{sd:.2f}}} = {z_x:.3f}"
    )


def render_ai(x, data):
    st.header("5) AI connection")
    st.markdown("#### Robust scaling: `RobustScaler` vs `StandardScaler`")
    st.markdown(
        r"`StandardScaler` computes $(x-\bar x)/\sigma$; `RobustScaler` computes $(x - \text{median})/\text{IQR}$ "
        "(scikit-learn's default `quantile_range=(25, 75)`, numpy linear quantiles). Same ten latencies as above:"
    )
    std = StandardScaler().fit_transform(data.reshape(-1, 1)).ravel()
    rob = RobustScaler().fit_transform(data.reshape(-1, 1)).ravel()
    df = pd.DataFrame({"latency (ms)": data, "StandardScaler": std, "RobustScaler": rob})
    c1, c2 = st.columns([2, 1])
    c1.dataframe(df.round(3), width="stretch", height=390)
    with c2:
        st.metric("Spread of the 9 normal points — StandardScaler", f"{np.ptp(std[:9]):.3f}")
        st.metric("Spread of the 9 normal points — RobustScaler", f"{np.ptp(rob[:9]):.3f}")
        st.caption(
            "Drag the tenth latency up: with StandardScaler the nine ordinary points collapse towards one value "
            "(the model can no longer tell them apart); RobustScaler keeps their scale fixed."
        )

    st.markdown("#### Percentile clipping (winsorizing)")
    pct = st.slider("Clip the dataset from section 1 to the [100 − c, c] percentiles, c =", 90.0, 100.0, 99.0, 0.5, key="p39_clip")
    lo, hi = np.quantile(x, [1 - pct / 100, pct / 100])
    clipped = np.clip(x, lo, hi)
    k1, k2, k3 = st.columns(3)
    k1.metric("Clip range", f"[{lo:.2f}, {hi:.2f}]")
    k2.metric("Values changed", f"{int((clipped != x).sum())} of {x.size}")
    k3.metric("SD before → after", f"{x.std():.2f} → {clipped.std():.2f}")
    st.markdown(
        """
        * **Data cleaning:** IQR filters drop sensor glitches and logging errors before training — but check before
          deleting: in fraud or anomaly detection the “outliers” *are* the signal.
        * **Gradient clipping:** adaptive schemes (e.g. AutoClip) clip each step's gradient norm at a running percentile of
          past norms instead of a hand-tuned constant, taming rare exploding steps.
        * **Quantization:** INT8 calibration often picks the activation range by a high percentile (e.g. 99.99%) rather than
          the max, so one huge activation doesn't waste the 256 available levels.
        * **Quantile normalization / `QuantileTransformer`:** map each feature through its ECDF to a uniform or normal shape;
          ranks survive, outliers lose their leverage.
        * **Evaluation:** p95/p99 latency, and **quantile (pinball) loss** for models that predict intervals instead of means.
        """
    )


def main():
    st.session_state.setdefault("p39_seed", 0)
    st.title("📦 Page 39: Quantiles, IQR & Outliers")
    st.markdown(
        """
        On page 38 the **median** stayed calm while the **mean** chased outliers. Quantiles generalise the median:
        instead of “the middle”, ask for the value 25%, 90% or 99% of the way through the sorted data.
        They describe **spread** (IQR), **shape** (skew) and **tails** (p99) without being bullied by a few wild values.

        **Why it matters for AI:** real data is messy — mis-logged sensor values, bots, typos. Quantile-based tools
        (robust scaling, IQR filtering, percentile clipping) keep a single bad value from wrecking training.
        """
    )
    st.divider()
    x, preset = render_box_lab()
    st.divider()
    data, t, xv = render_robustness_lab()
    st.divider()
    render_ecdf_lab(x, preset)
    st.divider()
    render_worked_example(data, t, xv)
    st.divider()
    render_ai(x, data)
    st.divider()
    st.success(
        r"""
        **Key takeaways**
        - $Q(p)$ is the value with a fraction $p$ of the data below it; numpy's default interpolates linearly between sorted points.
        - Five-number summary = min, Q1, median, Q3, max; **IQR = Q3 − Q1** is the spread of the middle half.
        - Tukey's rule flags points outside $[Q1 - 1.5\,\text{IQR},\; Q3 + 1.5\,\text{IQR}]$.
        - Median & IQR are **robust**; mean & SD can be dragged anywhere by one point — and |z| can even mask the outlier.
        - In ML: RobustScaler, IQR filtering, percentile clipping and quantile transforms all build on these ideas.
        """
    )
    c1, c2 = st.columns(2)
    with c1:
        safe_page_link("pages/38Mean, Median, Mode.py", "← Previous: Mean, Median, Mode", icon="📊")
    with c2:
        safe_page_link("pages/40Covariance.py", "Next: Covariance →", icon="📈")
    safe_page_link("pages/35Z-Scores & Standardization.py", "Revisit: Z-Scores & Standardization (page 35)", icon="📏")


main()
