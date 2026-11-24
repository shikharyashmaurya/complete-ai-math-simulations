import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from scipy import stats

st.set_page_config(page_title="85 · Poisson & Exponential Distributions", page_icon="⏱️", layout="wide")

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.nav import safe_page_link  # noqa: E402

N_MEMORY = 200_000


def kmax_for(lam):
    """Upper k that captures all but a negligible tail of Poisson(lam)."""
    return int(np.ceil(lam + 6 * np.sqrt(lam) + 6))


def poisson_mode_text(lam):
    if abs(lam - round(lam)) < 1e-9 and round(lam) >= 1:
        return f"{round(lam) - 1} and {round(lam)} (tie, λ is an integer)"
    return f"{int(np.floor(lam))}"


def normal_approx_pmf(ks, lam):
    """Continuity-corrected N(λ, λ) probabilities for k = 0, 1, ...; k = 0 absorbs the negative tail."""
    sd = np.sqrt(lam)
    upper = stats.norm.cdf((ks + 0.5 - lam) / sd)
    lower = np.where(ks == 0, 0.0, stats.norm.cdf((ks - 0.5 - lam) / sd))
    return upper - lower


def render_intro():
    st.title("⏱️ Page 85: Poisson & Exponential Distributions")
    st.markdown("### Counting rare events — and waiting for the next one.")
    with st.container(border=True):
        st.markdown(
            r"""
**Intuition.** Requests hit an LLM server at random moments, on average $\lambda$ per second. No single moment is
special, and arrivals don't coordinate. Two natural questions then have famous answers:

* **How many** arrive in one second? $\;K\sim\text{Poisson}(\lambda)$, $\;P(K=k)=\dfrac{\lambda^k e^{-\lambda}}{k!}$.
* **How long** until the next one? $\;T\sim\text{Exponential}(\lambda)$, $\;P(T>t)=e^{-\lambda t}$.

They are two views of one **Poisson process**. The Poisson is what a Binomial becomes when you have *many* chances
($n\to\infty$), each *rare* ($p=\lambda/n$).
"""
        )


def render_pmf_lab():
    st.header("🧪 Lab 1 — The Poisson PMF")
    c1, c2 = st.columns([1, 2])
    with c1:
        lam = st.slider("λ (average count per window)", 0.1, 60.0, 4.0, 0.1, key="p85_lam")
        show_normal = st.checkbox("Overlay normal approximation N(λ, λ)", value=True, key="p85_normal")
    ks = np.arange(kmax_for(lam) + 1)
    pmf = stats.poisson.pmf(ks, lam)
    mean_num = float(np.sum(ks * pmf))
    var_num = float(np.sum((ks - mean_num) ** 2 * pmf))
    with c1:
        st.metric("Mean Σ k·P(k)", f"{mean_num:.4f}", help="Computed from the plotted PMF; theory says exactly λ.")
        st.metric("Variance Σ (k−mean)²·P(k)", f"{var_num:.4f}", help="Theory: also exactly λ.")
        st.caption(f"Mode = {poisson_mode_text(lam)} · P(K = 0) = e^(−λ) = {np.exp(-lam):.4f}")

    tv = None
    fig = make_subplots(rows=1, cols=2, column_widths=[0.6, 0.4], subplot_titles=("PMF P(K = k)", "CDF P(K ≤ k)"))
    fig.add_trace(go.Bar(x=ks, y=pmf, marker_color="#38bdf8", name="Poisson(λ)",
                         hovertemplate="k=%{x}<br>P=%{y:.5f}<extra></extra>"), 1, 1)
    fig.add_trace(go.Scatter(x=ks, y=stats.poisson.cdf(ks, lam), mode="lines", line_shape="hv",
                             line=dict(color="#38bdf8"), name="CDF"), 1, 2)
    if show_normal:
        approx = normal_approx_pmf(ks, lam)
        tail = stats.poisson.sf(ks[-1], lam) + stats.norm.sf((ks[-1] + 0.5 - lam) / np.sqrt(lam))
        tv = 0.5 * (float(np.abs(pmf - approx).sum()) + tail)
        fig.add_trace(go.Scatter(x=ks, y=approx, mode="markers+lines", name="N(λ, λ), continuity-corrected",
                                 line=dict(color="#f59e0b", dash="dot")), 1, 1)
    fig.update_layout(template="plotly_dark", height=380, margin=dict(l=10, r=10, t=40, b=10),
                      legend=dict(orientation="h", y=-0.15))
    fig.update_yaxes(range=[0, 1.02], row=1, col=2)
    with c2:
        st.plotly_chart(fig, width="stretch")

    if tv is not None:
        verdict = "good" if tv < 0.02 else ("rough" if tv < 0.08 else "poor")
        st.info(f"Total variation distance Poisson ↔ normal approximation: **{tv:.4f}** ({verdict}). "
                "Small λ: the PMF is skewed and piled up near 0, so a symmetric bell fits badly. "
                "Large λ: mean = variance = λ and the shape becomes Gaussian (CLT — a Poisson(λ) is a sum of "
                "λ independent Poisson(1) counts).")
    return lam


def binom_poisson_tv(n, lam):
    """Exact TV distance between Binomial(n, λ/n) and Poisson(λ) (Poisson mass above n counted as a gap)."""
    ks = np.arange(n + 1)
    gap = np.abs(stats.binom.pmf(ks, n, lam / n) - stats.poisson.pmf(ks, lam)).sum()
    return 0.5 * float(gap + stats.poisson.sf(n, lam))


def render_limit_lab():
    st.header("🧪 Lab 2 — Poisson as the limit of Binomial(n, λ/n)")
    c1, c2 = st.columns(2)
    lam = c1.slider("λ = n·p (kept fixed)", 0.5, 10.0, 3.0, 0.5, key="p85_lam_b")
    n = c2.slider("n (number of tiny chances)", 10, 1000, 20, 10, key="p85_n")
    p = lam / n
    ks = np.arange(kmax_for(lam) + 1)
    tv = binom_poisson_tv(n, lam)
    bound = lam**2 / n

    c1, c2 = st.columns([3, 2])
    with c1:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=ks, y=stats.binom.pmf(ks, n, p), name=f"Binomial({n}, {p:.4f})",
                             marker_color="#a78bfa", opacity=0.75))
        fig.add_trace(go.Scatter(x=ks, y=stats.poisson.pmf(ks, lam), mode="markers+lines",
                                 name=f"Poisson({lam:g})", line=dict(color="#22c55e")))
        fig.update_layout(template="plotly_dark", height=360, xaxis_title="k", yaxis_title="probability",
                          margin=dict(l=10, r=10, t=30, b=10), legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig, width="stretch")
    with c2:
        grid = np.unique(np.geomspace(10, 1000, 30).astype(int))
        tvs = [binom_poisson_tv(int(m), lam) for m in grid]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=grid, y=tvs, mode="lines+markers", name="TV distance", line=dict(color="#a78bfa")))
        fig.add_trace(go.Scatter(x=grid, y=lam**2 / grid, mode="lines", name="Le Cam bound λ²/n",
                                 line=dict(color="#94a3b8", dash="dash")))
        fig.add_trace(go.Scatter(x=[n], y=[tv], mode="markers", marker=dict(size=13, color="#ef4444"), name="current n"))
        fig.update_layout(template="plotly_dark", height=360, margin=dict(l=10, r=10, t=30, b=10),
                          xaxis=dict(type="log", title="n"), yaxis=dict(type="log", title="TV distance"),
                          legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig, width="stretch")
    m1, m2, m3 = st.columns(3)
    m1.metric("p = λ / n", f"{p:.4f}")
    m2.metric("TV(Binomial, Poisson)", f"{tv:.5f}")
    m3.metric("Le Cam bound λ²/n", f"{bound:.5f}", "bound holds ✓" if tv <= bound else "bound violated ✗")
    st.caption(r"$\binom{n}{k}p^k(1-p)^{n-k}\to\frac{\lambda^k e^{-\lambda}}{k!}$: since $(1-\lambda/n)^n\to e^{-\lambda}$"
               r" and $\binom{n}{k}/n^k\to 1/k!$. The distance shrinks roughly like $1/n$ (slope −1 on the log-log plot).")


def simulate_process(rate, horizon, seed):
    rng = np.random.default_rng(seed)
    expected = rate * horizon
    size = int(expected + 10 * np.sqrt(expected) + 20)
    times = np.cumsum(rng.exponential(1.0 / rate, size))
    while times[-1] <= horizon:  # practically never, but never silently truncate the process
        times = np.concatenate([times, times[-1] + np.cumsum(rng.exponential(1.0 / rate, size))])
    return times[times < horizon]


def render_process_lab():
    st.header("🧪 Lab 3 — A Poisson process: counts and waiting times")
    c1, c2, c3 = st.columns([2, 2, 1])
    rate = c1.slider("Rate λ (events per minute)", 0.2, 10.0, 2.0, 0.1, key="p85_rate")
    horizon = c2.slider("Observation window T (minutes)", 5, 60, 30, 5, key="p85_T")
    if c3.button("🎲 Resample", key="p85_resample"):
        st.session_state["p85_seed"] += 1
    seed = st.session_state["p85_seed"]
    times = simulate_process(rate, horizon, seed)
    gaps = np.diff(np.concatenate([[0.0], times]))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=np.zeros_like(times), mode="markers", name="arrival",
                             marker=dict(symbol="line-ns-open", size=22, color="#38bdf8", line=dict(width=2))))
    for m in range(1, horizon):
        fig.add_vline(x=m, line_color="#334155", line_width=1)
    fig.update_layout(template="plotly_dark", height=150, showlegend=False, margin=dict(l=10, r=10, t=10, b=30),
                      xaxis=dict(range=[0, horizon], title="time (minutes)"), yaxis=dict(visible=False))
    st.plotly_chart(fig, width="stretch")
    st.caption(f"{times.size} arrivals in {horizon} minutes (expected λT = {rate * horizon:.1f}). Grid lines split "
               "the timeline into 1-minute windows.")

    per_minute = np.histogram(times, bins=np.arange(horizon + 1))[0]
    kk = np.arange(max(int(per_minute.max(initial=0)), kmax_for(rate)) + 1)
    freq = np.bincount(per_minute, minlength=kk.size)[: kk.size] / per_minute.size
    tt = np.linspace(0, 5 / rate, 300)

    fig = make_subplots(rows=1, cols=3, subplot_titles=(
        "Counts per minute vs Poisson(λ)", "Gaps between arrivals vs λe^(−λt)", "Exponential CDF & survival"))
    fig.add_trace(go.Bar(x=kk, y=freq, name="observed share of minutes", marker_color="#38bdf8", opacity=0.7), 1, 1)
    fig.add_trace(go.Scatter(x=kk, y=stats.poisson.pmf(kk, rate), mode="markers+lines", name="Poisson PMF",
                             line=dict(color="#22c55e")), 1, 1)
    if gaps.size:
        fig.add_trace(go.Histogram(x=gaps, histnorm="probability density", nbinsx=25, marker_color="#f59e0b",
                                   opacity=0.6, name="observed gaps"), 1, 2)
    fig.add_trace(go.Scatter(x=tt, y=rate * np.exp(-rate * tt), name="Exponential pdf", line=dict(color="#e2e8f0")), 1, 2)
    fig.add_trace(go.Scatter(x=tt, y=1 - np.exp(-rate * tt), name="CDF F(t) = 1 − e^(−λt)",
                             line=dict(color="#a78bfa")), 1, 3)
    fig.add_trace(go.Scatter(x=tt, y=np.exp(-rate * tt), name="survival S(t) = e^(−λt)",
                             line=dict(color="#ef4444")), 1, 3)
    if gaps.size:
        srt = np.sort(gaps)
        fig.add_trace(go.Scatter(x=srt, y=1 - np.arange(1, srt.size + 1) / srt.size, mode="lines", line_shape="hv",
                                 name="empirical survival", line=dict(color="#ef4444", dash="dot")), 1, 3)
    fig.add_vline(x=1 / rate, line_dash="dash", line_color="#94a3b8", row=1, col=3)
    fig.add_vline(x=np.log(2) / rate, line_dash="dot", line_color="#94a3b8", row=1, col=3)
    fig.update_xaxes(range=[0, 5 / rate], row=1, col=2)
    fig.update_xaxes(range=[0, 5 / rate], row=1, col=3)
    fig.update_layout(template="plotly_dark", height=380, margin=dict(l=10, r=10, t=40, b=10),
                      legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig, width="stretch")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Mean count / minute", f"{per_minute.mean():.3f}", help=f"Theory λ = {rate:.2f}")
    m2.metric("Variance of count / minute", f"{per_minute.var():.3f}", help=f"Theory λ = {rate:.2f}")
    if gaps.size:
        m3.metric("Mean gap (min)", f"{gaps.mean():.3f}", help=f"Theory 1/λ = {1 / rate:.3f}")
    else:
        m3.metric("Mean gap (min)", "no arrivals", help="Increase λ or T, or resample.")
    m4.metric("Median gap theory ln2/λ", f"{np.log(2) / rate:.3f}")
    st.caption("Dashed line: mean 1/λ; dotted line: median ln 2 / λ (the exponential is right-skewed, so median < mean).")
    return rate


def render_memoryless_lab(rate):
    st.header("🧪 Lab 4 — Memorylessness: the wait never 'gets due'")
    c1, c2 = st.columns(2)
    s = c1.slider("Already waited s (minutes)", 0.0, 5.0, 1.0, 0.1, key="p85_s")
    t = c2.slider("Wait at least t more (minutes)", 0.0, 5.0, 0.5, 0.1, key="p85_t")
    st.latex(rf"P(T>s+t\mid T>s)=\frac{{e^{{-\lambda(s+t)}}}}{{e^{{-\lambda s}}}}=e^{{-\lambda t}}"
             rf"=e^{{-{rate:.2f}\times{t:.2f}}}={np.exp(-rate * t):.4f}=P(T>t)")

    rng = np.random.default_rng(st.session_state["p85_seed"] + 10_000)
    draws = rng.exponential(1.0 / rate, N_MEMORY)
    survivors = draws[draws > s]
    b = 2.0 / rate  # Uniform(0, b) has the same mean 1/λ but is NOT memoryless

    def unif_sf(x):
        return max(0.0, 1.0 - x / b)

    m1, m2, m3 = st.columns(3)
    m1.metric("Formula e^(−λt)", f"{np.exp(-rate * t):.4f}")
    if survivors.size >= 50:
        m2.metric(f"Simulated P(T>s+t | T>s)  ({survivors.size:,} survivors)", f"{np.mean(survivors > s + t):.4f}")
    else:
        m2.metric("Simulated P(T>s+t | T>s)", "too few survivors",
                  help=f"Only {survivors.size} of {N_MEMORY:,} draws exceed s: e^(−λs) = {np.exp(-rate * s):.2e}.")
    m3.metric("Simulated P(T>t)", f"{np.mean(draws > t):.4f}")

    tt = np.linspace(0, 5 / rate, 300)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=tt, y=np.exp(-rate * tt), name="Exponential: S(t)", line=dict(color="#38bdf8", width=4)))
    fig.add_trace(go.Scatter(x=tt, y=np.exp(-rate * (s + tt)) / np.exp(-rate * s), name="Exponential: S(s+t)/S(s)",
                             line=dict(color="#f59e0b", dash="dash")))
    fig.add_trace(go.Scatter(x=tt, y=[unif_sf(x) for x in tt], name="Uniform(0, 2/λ): S(t)", line=dict(color="#a78bfa")))
    if unif_sf(s) > 0:
        fig.add_trace(go.Scatter(x=tt, y=[unif_sf(s + x) / unif_sf(s) for x in tt],
                                 name="Uniform: S(s+t)/S(s)", line=dict(color="#ef4444", dash="dash")))
    fig.add_vline(x=t, line_color="#94a3b8", line_dash="dot")
    fig.update_layout(template="plotly_dark", height=340, xaxis_title="additional wait t (minutes)",
                      yaxis_title="probability of waiting longer", margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig, width="stretch")
    if unif_sf(s) > 0:
        unif_text = f"{unif_sf(s + t) / unif_sf(s):.4f} vs P(T>t) = {unif_sf(t):.4f}"
    else:
        unif_text = "undefined — a Uniform(0, 2/λ) wait can never exceed s"
    st.caption(f"Exponential curves coincide for any s. For the same-mean Uniform(0, {b:.2f}) wait, "
               f"P(T>s+t | T>s) = {unif_text}: having waited changes the future — it is *not* memoryless.")


def render_worked_example(lam):
    st.header("🧮 Worked example — will the server overflow?")
    st.markdown(f"Requests arrive at **λ = {lam:g} per second** (the Lab 1 slider). One GPU batch slot handles at "
                "most **c** requests per second.")
    c = st.slider("Capacity c (requests per second)", 0, 120, 8, 1, key="p85_c")
    p0 = np.exp(-lam)
    p1 = lam * np.exp(-lam)
    over = stats.poisson.sf(c, lam)
    st.latex(rf"P(K=0)=e^{{-{lam:g}}}={p0:.5f},\qquad P(K=1)=\frac{{{lam:g}^1 e^{{-{lam:g}}}}}{{1!}}={p1:.5f}")
    st.latex(rf"P(K>c)=1-\sum_{{k=0}}^{{{c}}}\frac{{{lam:g}^k e^{{-{lam:g}}}}}{{k!}}={over:.6f}")
    st.latex(rf"P(\text{{no request for 0.5 s}})=P(T>0.5)=e^{{-{lam:g}\times 0.5}}={np.exp(-0.5 * lam):.5f}")
    st.caption(f"So about {over * 3600:.1f} of the 3,600 one-second windows in an hour exceed capacity. "
               "Raising c a little above λ buys a lot: the Poisson tail decays faster than exponentially.")


def render_ai_connection():
    st.header("🤖 AI / ML connection")
    c1, c2, c3 = st.columns(3)
    with c1, st.container(border=True):
        st.markdown("**LLM serving & queues.** Request arrivals are modelled as a Poisson process; inter-arrival "
                    "times are exponential. Capacity planning, autoscaling and load-testing tools (e.g. a "
                    "`--request-rate` in serving benchmarks) sample arrivals exactly like Lab 3.")
    with c2, st.container(border=True):
        st.markdown(r"**Count data & Poisson regression.** Predict clicks, calls or defects with "
                    r"$\log\lambda=w^\top x$ (a GLM); the loss is the Poisson negative log-likelihood "
                    r"$\lambda-k\log\lambda$, available as `PoissonNLLLoss` in PyTorch.")
    with c3, st.container(border=True):
        st.markdown("**Rare events & word counts.** How often a rare token, fraud case or failure appears in a "
                    "window is ≈ Poisson (the Binomial limit). Survival / time-to-event models start from the "
                    "exponential hazard.")


def render_takeaways():
    st.header("✅ Key takeaways")
    st.markdown(
        r"""
* $\text{Poisson}(\lambda)$: $P(k)=\lambda^k e^{-\lambda}/k!$, with **mean = variance = λ**.
* It is the limit of $\text{Binomial}(n,\lambda/n)$ as $n\to\infty$ — many chances, each rare.
* In a Poisson process, counts per window are Poisson and **gaps are Exponential(λ)**: mean $1/\lambda$,
  CDF $1-e^{-\lambda t}$, survival $e^{-\lambda t}$.
* The exponential is **memoryless**: $P(T>s+t\mid T>s)=P(T>t)$. For large λ the Poisson looks Gaussian, $N(\lambda,\lambda)$.
"""
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        safe_page_link("pages/84Joint & Marginal Distributions.py", "⬅️ Previous: 84 · Joint & Marginal")
    with c2:
        safe_page_link("pages/32Binomial Distribution.py", "📎 Related: 32 · Binomial Distribution")
    with c3:
        safe_page_link("pages/86Beta Distribution — Beliefs about Probabilities.py", "➡️ Next: 86 · Beta Distribution")


def main():
    st.session_state.setdefault("p85_seed", 85)
    render_intro()
    lam = render_pmf_lab()
    st.divider()
    render_limit_lab()
    st.divider()
    rate = render_process_lab()
    st.divider()
    render_memoryless_lab(rate)
    st.divider()
    render_worked_example(lam)
    st.divider()
    render_ai_connection()
    render_takeaways()


main()
