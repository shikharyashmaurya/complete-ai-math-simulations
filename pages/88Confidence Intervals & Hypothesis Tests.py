import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from scipy import stats

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="88 · Confidence Intervals & Hypothesis Tests", page_icon="🧪", layout="wide")

MU, SIGMA = 50.0, 10.0
POPULATIONS = ["Normal (μ = 50, σ = 10)", "Skewed: 40 + Exponential (μ = 50, σ = 10)"]
N_EXPERIMENTS = 3000
N_TESTS = 20


def _seed(name, default):
    key = f"p88_seed_{name}"
    if key not in st.session_state:
        st.session_state[key] = default
    return st.session_state[key]


def _bump_seed(name):
    st.session_state[f"p88_seed_{name}"] += 1


def draw_population(rng, kind, size):
    if kind == POPULATIONS[0]:
        return rng.normal(MU, SIGMA, size)
    return 40.0 + rng.exponential(10.0, size)


def two_prop_z(xa, xb, n):
    """Pooled two-proportion z-test (equal arm sizes n). Returns (z, two-sided p, SE); works on arrays."""
    xa, xb = np.asarray(xa, dtype=float), np.asarray(xb, dtype=float)
    pooled = (xa + xb) / (2 * n)
    se = np.sqrt(pooled * (1 - pooled) * 2.0 / n)
    diff = (xb - xa) / n
    z = np.divide(diff, se, out=np.zeros_like(diff), where=se > 0)  # all-0 or all-1 conversions: no evidence, z = 0
    return z, 2 * stats.norm.sf(np.abs(z)), se


def power_formula(pa, pb, n, alpha):
    """Normal-approximation power of the two-sided pooled two-proportion z-test (both rejection tails)."""
    n = np.asarray(n, dtype=float)
    zc = stats.norm.isf(alpha / 2)
    pbar = (pa + pb) / 2
    se0 = np.sqrt(2 * pbar * (1 - pbar) / n)
    se1 = np.sqrt((pa * (1 - pa) + pb * (1 - pb)) / n)
    delta = pb - pa
    if np.all(se1 == 0):
        return np.where(np.abs(delta) > 0, 1.0, 0.0) * np.ones_like(n)
    return stats.norm.cdf((delta - zc * se0) / se1) + stats.norm.cdf((-delta - zc * se0) / se1)


def render_intuition():
    st.title("🧪 Confidence Intervals & Hypothesis Tests")
    st.markdown(
        "You measured a sample — a mean, a conversion rate, a model's accuracy. A different sample would have given a different number. "
        "**How much of what you see is signal, and how much is sampling noise?** Confidence intervals give a range of plausible values; "
        "hypothesis tests ask whether the data are surprising if *nothing* is going on."
    )
    c1, c2 = st.columns(2)
    with c1, st.container(border=True):
        st.markdown("**Confidence interval for a mean** (t-interval)")
        st.latex(r"\bar x \;\pm\; t_{n-1,\,1-\alpha/2}\,\frac{s}{\sqrt n}")
    with c2, st.container(border=True):
        st.markdown("**Hypothesis test** — p-value")
        st.latex(r"p = P\big(\text{a result at least this extreme} \mid H_0 \text{ true}\big)")
    st.markdown("**Why it matters for AI:** a new model scores +0.5% on a benchmark. Real improvement or lucky test set? This page gives you the tools to decide.")


def render_ci_lab():
    st.header("📊 Lab 1 — Sampling distribution & confidence intervals")
    left, right = st.columns([1, 2], gap="large")
    with left:
        pop = st.selectbox("Population", POPULATIONS, key="p88_pop")
        n = st.slider("Sample size n", 2, 100, 10, key="p88_n")
        conf = st.slider("Confidence level", 0.80, 0.99, 0.95, 0.01, key="p88_conf")
        st.button("🎲 Resample all experiments", key="p88_resample", on_click=_bump_seed, args=("ci",))
    rng = np.random.default_rng(_seed("ci", 88))
    samples = draw_population(rng, pop, (N_EXPERIMENTS, n))
    xbar = samples.mean(axis=1)
    s = samples.std(axis=1, ddof=1)
    t_crit = float(stats.t.ppf(1 - (1 - conf) / 2, df=n - 1))
    half = t_crit * s / np.sqrt(n)
    lo, hi = xbar - half, xbar + half
    covers = (lo <= MU) & (MU <= hi)

    with left:
        st.metric("SD of x̄ across experiments", f"{xbar.std(ddof=1):.3f}", f"theory σ/√n = {SIGMA / np.sqrt(n):.3f}", delta_color="off", delta_arrow="off")
    with right:
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=xbar, histnorm="probability density", nbinsx=60, name=f"x̄ of {N_EXPERIMENTS} samples", marker_color="#60a5fa", opacity=0.75))
        grid = np.linspace(xbar.min(), xbar.max(), 300)
        fig.add_trace(go.Scatter(x=grid, y=stats.norm.pdf(grid, MU, SIGMA / np.sqrt(n)), name="CLT: N(μ, σ²/n)", line=dict(color="#fbbf24", width=3)))
        fig.add_vline(x=MU, line_dash="dash", line_color="#f472b6", annotation_text="μ = 50")
        fig.update_layout(title=f"Sampling distribution of the mean (n = {n})", xaxis_title="sample mean x̄", yaxis_title="density", height=330, margin=dict(t=50, b=40), legend=dict(orientation="h", y=-0.25))
        st.plotly_chart(fig, width="stretch")

    st.subheader(f"🎯 Coverage: 100 intervals at {conf:.0%} confidence")
    k = 100
    hit = int(covers[:k].sum())
    c1, c2 = st.columns([2, 1], gap="large")
    with c1:
        fig = go.Figure()
        for flag, color, name in ((True, "#34d399", "contains μ"), (False, "#f87171", "misses μ")):
            idx = np.flatnonzero(covers[:k] == flag)
            xs = np.column_stack([lo[idx], hi[idx], np.full(idx.size, np.nan)]).ravel()
            ys = np.repeat(idx, 3).astype(float)
            fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=color, width=2), name=f"{name} ({idx.size})"))
        fig.add_trace(go.Scatter(x=xbar[:k], y=np.arange(k), mode="markers", marker=dict(size=4, color="#e2e8f0"), name="x̄"))
        fig.add_vline(x=MU, line_dash="dash", line_color="#fbbf24")
        fig.update_layout(height=480, xaxis_title="value", yaxis_title="experiment #", margin=dict(t=20, b=40), legend=dict(orientation="h", y=-0.12))
        st.plotly_chart(fig, width="stretch")
    with c2:
        st.metric("Intervals containing μ (of 100)", f"{hit}", f"expected ≈ {conf * 100:.0f}", delta_color="off", delta_arrow="off")
        st.metric(f"Coverage over all {N_EXPERIMENTS} experiments", f"{covers.mean():.1%}", f"nominal {conf:.0%}", delta_color="off", delta_arrow="off")
        if pop != POPULATIONS[0] and n < 20:
            st.caption("Skewed population + small n: the t-interval assumes normal data, so true coverage falls a little below nominal. The CLT repairs this as n grows.")
        st.warning(
            "**Common misinterpretation:** “there is a 95% probability that μ is in *this* interval.” No — μ is fixed; each interval either contains it or not. "
            "The 95% describes the **procedure**: in the long run, 95% of intervals built this way capture μ."
        )
    return samples[0], conf


def render_ci_worked(sample, conf):
    st.subheader("🧮 Worked example — experiment #0")
    n = sample.size
    xbar, s = float(sample.mean()), float(sample.std(ddof=1))
    se = s / np.sqrt(n)
    t_crit = float(stats.t.ppf(1 - (1 - conf) / 2, df=n - 1))
    z_crit = float(stats.norm.ppf(1 - (1 - conf) / 2))
    st.latex(
        rf"\bar x = {xbar:.3f},\quad s = {s:.3f},\quad \frac{{s}}{{\sqrt{{{n}}}}} = {se:.3f},\quad t_{{{n - 1},\,{1 - (1 - conf) / 2:.3f}}} = {t_crit:.3f}"
    )
    st.latex(rf"\text{{{conf:.0%} CI}} = {xbar:.3f} \pm {t_crit:.3f}\times{se:.3f} = [{xbar - t_crit * se:.3f},\; {xbar + t_crit * se:.3f}]".replace("%", r"\%"))
    st.caption(f"Using the normal z = {z_crit:.3f} instead of t = {t_crit:.3f} would make the interval {100 * (1 - z_crit / t_crit):.1f}% narrower — too narrow for small n, because s itself is noisy. t → z as n grows.")

    st.markdown("**The same data as a one-sample t-test.** Is the mean different from a hypothesised value μ₀?")
    mu0 = st.slider("Null value μ₀", 30.0, 70.0, 50.0, 0.5, key="p88_mu0")
    res = stats.ttest_1samp(sample, mu0)
    t_stat = (xbar - mu0) / se
    inside = xbar - t_crit * se <= mu0 <= xbar + t_crit * se
    c1, c2, c3 = st.columns(3)
    c1.metric("t = (x̄ − μ₀)/(s/√n)", f"{t_stat:.3f}", f"scipy: {float(res.statistic):.3f}", delta_color="off", delta_arrow="off")
    c2.metric("two-sided p-value", f"{float(res.pvalue):.4f}")
    c3.metric(f"μ₀ inside the {conf:.0%} CI?", "yes" if inside else "no")
    st.info(f"Duality: μ₀ lies outside the {conf:.0%} CI exactly when p < {1 - conf:.2f}. Here p {'<' if res.pvalue < 1 - conf else '≥'} {1 - conf:.2f} and μ₀ is {'outside' if not inside else 'inside'} the interval.")


def render_ab_lab():
    st.header("🅰️🅱️ Lab 2 — A/B test with a two-proportion z-test")
    left, right = st.columns([1, 2], gap="large")
    with left:
        pa = st.slider("Baseline conversion rate p_A", 0.01, 0.50, 0.10, 0.01, key="p88_pa")
        lift = st.slider("True lift of B (percentage points)", -5.0, 5.0, 1.0, 0.25, key="p88_lift")
        n = st.select_slider("Users per arm n", [100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000], 2000, key="p88_ab_n")
        alpha = st.selectbox("Significance level α", [0.01, 0.05, 0.10], index=1, key="p88_alpha")
        st.button("🎲 Rerun the experiment", key="p88_resample_ab", on_click=_bump_seed, args=("ab",))
    pb = float(np.clip(pa + lift / 100, 0.0, 1.0))
    rng = np.random.default_rng(_seed("ab", 880))
    xa, xb = int(rng.binomial(n, pa)), int(rng.binomial(n, pb))
    z, p_val, se = (float(v) for v in two_prop_z(xa, xb, n))
    zc = float(stats.norm.isf(alpha / 2))

    with left:
        if pb != pa + lift / 100:
            st.caption(f"p_B clipped to {pb:.2f}.")
        st.markdown(f"A: **{xa}/{n}** = {xa / n:.2%}  ·  B: **{xb}/{n}** = {xb / n:.2%}")
    with right:
        span = max(4.5, min(abs(z) + 1.0, 12.0))
        x = np.linspace(-span, span, 801)
        y = stats.norm.pdf(x)
        fig = go.Figure(go.Scatter(x=x, y=y, mode="lines", line=dict(color="#e2e8f0", width=2), name="null N(0, 1)"))
        az = min(abs(z), span)
        for side in (-1, 1):
            xs = np.linspace(az, span, 200) * side
            fig.add_trace(go.Scatter(x=xs, y=stats.norm.pdf(xs), fill="tozeroy", mode="lines", line=dict(color="#f87171"), fillcolor="rgba(248,113,113,0.45)", showlegend=side == 1, name=f"p-value area = {p_val:.4f}"))
        for side in (-1, 1):
            fig.add_vline(x=side * zc, line_dash="dash", line_color="#fbbf24")
        fig.add_vline(x=z, line_color="#60a5fa", line_width=3, annotation_text=f"observed z = {z:.2f}")
        fig.update_layout(title=f"Null distribution of z; dashed = critical values ±{zc:.2f} (α = {alpha})", xaxis_title="z", yaxis_title="density", height=360, margin=dict(t=50, b=40), legend=dict(orientation="h", y=-0.25))
        st.plotly_chart(fig, width="stretch")

    st.subheader("🧮 Worked example")
    pooled = (xa + xb) / (2 * n)
    st.latex(
        rf"\hat p = \frac{{{xa}+{xb}}}{{2\cdot{n}}} = {pooled:.4f},\quad SE = \sqrt{{\hat p(1-\hat p)\tfrac{{2}}{{n}}}} = {se:.5f},\quad "
        rf"z = \frac{{\hat p_B - \hat p_A}}{{SE}} = \frac{{{xb / n:.4f} - {xa / n:.4f}}}{{{se:.5f}}} = {z:.3f}"
    )
    if se == 0:
        st.warning("Both arms converted 0% (or 100%): the pooled SE is 0, so the test has no information — we report z = 0, p = 1.")
    else:
        chi2, p_chi, _, _ = stats.chi2_contingency([[xa, n - xa], [xb, n - xb]], correction=False)
        st.caption(f"Cross-check: scipy chi2_contingency (no continuity correction) gives χ² = {chi2:.4f} = z² = {z * z:.4f} and p = {p_chi:.4f}.")
    if p_val < alpha:
        st.success(f"p = {p_val:.4f} < α = {alpha}: reject H₀ (no difference). " + ("And the true lift really is non-zero → a correct detection." if pb != pa else "But the true lift is 0 → this is a **Type I error** (false positive)!"))
    else:
        st.info(f"p = {p_val:.4f} ≥ α = {alpha}: not enough evidence to reject H₀. " + ("The true lift is non-zero → this is a **Type II error** (missed effect)." if pb != pa else "Correct — there truly is no difference.") + " “Not significant” ≠ “no effect”.")
    return pa, pb, n, alpha


def render_power(pa, pb, n, alpha):
    st.subheader("⚡ Errors and power")
    pw = float(power_formula(pa, pb, n, alpha))
    df = pd.DataFrame(
        {"H₀ true (no real lift)": [f"Type I error — prob. α = {alpha}", f"correct — prob. 1 − α = {1 - alpha:.2f}"],
         "H₁ true (real lift)": [f"correct detection — power = {pw:.3f}", f"Type II error — β = {1 - pw:.3f}"]},
        index=["reject H₀", "fail to reject H₀"],
    )
    st.table(df)
    st.caption("Power and β use the current true lift; with lift = 0 the 'power' formula returns α — the false-positive rate.")

    ns = np.unique(np.round(np.logspace(np.log10(100), np.log10(50000), 120)).astype(int))
    fig = go.Figure()
    delta = pb - pa
    for factor, dash in ((0.5, "dot"), (1.0, "solid"), (2.0, "dash")):
        pbf = float(np.clip(pa + factor * delta, 0.0, 1.0))
        fig.add_trace(go.Scatter(x=ns, y=power_formula(pa, pbf, ns, alpha), mode="lines", line=dict(dash=dash, width=3 if factor == 1 else 2), name=f"formula, lift {100 * (pbf - pa):+.2f} pp"))
    sim_n = np.array([100, 300, 1000, 3000, 10000, 30000])
    rng = np.random.default_rng(_seed("ab", 880) + 1)
    sims = 2000
    sim_power = []
    for m in sim_n:
        _, pv, _ = two_prop_z(rng.binomial(m, pa, sims), rng.binomial(m, pb, sims), m)
        sim_power.append(float(np.mean(pv < alpha)))
    fig.add_trace(go.Scatter(x=sim_n, y=sim_power, mode="markers", marker=dict(size=10, color="#fbbf24", symbol="diamond"), name=f"simulation ({sims} experiments each)"))
    fig.add_hline(y=0.8, line_dash="dot", line_color="#94a3b8", annotation_text="80% power")
    fig.add_trace(go.Scatter(x=[n, n], y=[0, 1], mode="lines", line=dict(color="#f472b6", width=2), name=f"your n = {n} (power {float(power_formula(pa, pb, n, alpha)):.2f})"))
    fig.update_layout(title="Power vs sample size and effect size", xaxis_type="log", xaxis_title="users per arm n (log scale)", yaxis_title="P(reject H₀)", yaxis_range=[0, 1.02], height=400, margin=dict(t=50, b=40), legend=dict(orientation="h", y=-0.25))
    st.plotly_chart(fig, width="stretch")
    if delta != 0:
        zc, zb = stats.norm.isf(alpha / 2), stats.norm.isf(0.2)
        pbar = (pa + pb) / 2
        n80 = (zc * np.sqrt(2 * pbar * (1 - pbar)) + zb * np.sqrt(pa * (1 - pa) + pb * (1 - pb))) ** 2 / delta**2
        st.latex(rf"n_{{80\%}} \approx \frac{{\big(z_{{1-\alpha/2}}\sqrt{{2\bar p(1-\bar p)}} + z_{{0.8}}\sqrt{{p_A(1-p_A)+p_B(1-p_B)}}\big)^2}}{{(p_B-p_A)^2}} = {int(np.ceil(n80)):,}\text{{ users per arm}}")
        st.caption("Halve the effect → need about 4× the users (n ∝ 1/Δ²).")


def render_multiple_testing(pa, n, alpha):
    st.header(f"🎰 Lab 3 — Multiple testing: {N_TESTS} A/B tests where nothing works")
    st.markdown(f"Every variant below is **identical** to control (true lift 0, p = {pa:.2f}, n = {n} per arm). Any 'significant' result is a false positive.")
    st.button("🎲 Run 20 new null tests", key="p88_resample_multi", on_click=_bump_seed, args=("multi",))
    rng = np.random.default_rng(_seed("multi", 8800))
    _, pvals, _ = two_prop_z(rng.binomial(n, pa, N_TESTS), rng.binomial(n, pa, N_TESTS), n)
    bonf = alpha / N_TESTS
    colors = np.where(pvals < bonf, "#f87171", np.where(pvals < alpha, "#fbbf24", "#60a5fa"))
    surprise = -np.log10(np.clip(pvals, 1e-300, 1.0))
    fig = go.Figure(go.Bar(x=[f"#{i + 1}" for i in range(N_TESTS)], y=surprise, marker_color=colors, customdata=pvals, hovertemplate="test %{x}<br>p = %{customdata:.4f}<extra></extra>"))
    fig.add_hline(y=-np.log10(alpha), line_dash="dash", line_color="#fbbf24", annotation_text=f"α = {alpha}")
    fig.add_hline(y=-np.log10(bonf), line_dash="dash", line_color="#f87171", annotation_text=f"Bonferroni α/{N_TESTS} = {bonf:.4f}")
    fig.update_layout(yaxis_title="−log₁₀(p)  (taller = more 'significant')", height=340, margin=dict(t=40, b=40), title="p-values of the 20 null tests: yellow = p < α, red = p < α/20")
    st.plotly_chart(fig, width="stretch")
    fam = np.random.default_rng(_seed("multi", 8800) + 1).standard_normal((5000, N_TESTS))
    fam_p = 2 * stats.norm.sf(np.abs(fam))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(f"False positives at α = {alpha}", int(np.sum(pvals < alpha)), f"expected {alpha * N_TESTS:.1f}", delta_color="off", delta_arrow="off")
    c2.metric("…after Bonferroni", int(np.sum(pvals < bonf)))
    c3.metric("P(≥ 1 false positive), uncorrected", f"{1 - (1 - alpha) ** N_TESTS:.1%}", f"simulated {np.mean((fam_p < alpha).any(axis=1)):.1%}", delta_color="off", delta_arrow="off")
    c4.metric("…with Bonferroni", f"{1 - (1 - bonf) ** N_TESTS:.1%}", f"simulated {np.mean((fam_p < bonf).any(axis=1)):.1%}", delta_color="off", delta_arrow="off")
    st.caption("Simulated family-wise rates use 5000 families of 20 independent z-tests under H₀. Bonferroni keeps the family-wise error ≤ α at the cost of power; the p-values of discrete binomial tests are slightly conservative.")


def render_ai_connection():
    st.header("🤖 AI / ML connection — is +0.5% accuracy real?")
    c1, c2 = st.columns([1, 2], gap="large")
    with c1:
        n_test = st.select_slider("Test-set size", [500, 1000, 2000, 5000, 10000, 50000, 100000], 10000, key="p88_test_n")
        acc = st.slider("Baseline accuracy", 0.50, 0.99, 0.90, 0.01, key="p88_acc")
        gain = st.slider("Improvement (percentage points)", 0.1, 5.0, 0.5, 0.1, key="p88_gain")
    acc_b = min(acc + gain / 100, 1.0)
    se_one = np.sqrt(acc * (1 - acc) / n_test)
    pbar = (acc + acc_b) / 2
    se_diff = np.sqrt(2 * pbar * (1 - pbar) / n_test)
    z = (acc_b - acc) / se_diff if se_diff > 0 else 0.0
    p = float(2 * stats.norm.sf(abs(z)))
    with c2:
        m1, m2, m3 = st.columns(3)
        m1.metric("Benchmark noise ±1.96·SE", f"±{1.96 * se_one:.2%}")
        m2.metric("z for the difference", f"{z:.2f}")
        m3.metric("two-sided p (unpaired)", f"{p:.4f}")
        (st.success if p < 0.05 else st.warning)(
            f"{acc:.1%} → {acc_b:.1%} on {n_test:,} examples is {'' if p < 0.05 else 'NOT '}significant at α = 0.05 by an unpaired test."
        )
        st.caption("When both models are scored on the **same** test set, a paired test (McNemar, or a bootstrap over examples) is more powerful because it only counts examples where the models disagree.")
    st.markdown(
        "- **Benchmark noise:** leaderboard gaps smaller than the CI width are often noise; report CIs or seeds × runs.\n"
        "- **A/B tests of ML features:** a new recommender is shipped only if the online metric lift is significant — with power planned *before* the test.\n"
        "- **Multiple comparisons:** tuning 50 hyper-parameter configs and reporting the best on the test set is the 20-null-tests trap — use a validation set or correct for it."
    )


def render_takeaways():
    st.header("📌 Key takeaways")
    st.markdown(
        r"""
- The sample mean varies from sample to sample with SD $\sigma/\sqrt n$ — the **standard error**.
- A 95% CI $\bar x \pm t\,s/\sqrt n$ captures μ in 95% of repetitions; it is a statement about the procedure, not one interval.
- A p-value is the tail area of the null distribution beyond the observed statistic; reject when $p<\alpha$.
- Type I = false alarm (rate α); Type II = miss (rate β); **power** $=1-\beta$ grows with n and effect size ($n\propto 1/\Delta^2$).
- Many tests ⇒ many false positives; Bonferroni ($\alpha/m$) controls the family-wise error.
"""
    )
    c1, c2 = st.columns(2)
    with c1:
        safe_page_link("pages/87Maximum Likelihood Estimation.py", "← Previous: 87 · Maximum Likelihood Estimation", icon="⬅️")
    with c2:
        safe_page_link("pages/89Mutual Information.py", "Next: 89 · Mutual Information →", icon="➡️")
    safe_page_link("pages/36Central Limit Theorem.py", "Related: 36 · Central Limit Theorem", icon="🔗")


def main():
    render_intuition()
    st.divider()
    sample, conf = render_ci_lab()
    render_ci_worked(sample, conf)
    st.divider()
    pa, pb, n, alpha = render_ab_lab()
    render_power(pa, pb, n, alpha)
    st.divider()
    render_multiple_testing(pa, n, alpha)
    st.divider()
    render_ai_connection()
    st.divider()
    render_takeaways()


main()
