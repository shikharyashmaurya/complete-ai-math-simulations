import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from scipy import stats

st.set_page_config(page_title="86 · Beta Distribution — Beliefs about Probabilities", page_icon="🎯", layout="wide")

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.nav import safe_page_link  # noqa: E402

MAX_FLIPS = 10_000
MAX_TS_STEPS = 3_000
ARM_COLORS = ["#38bdf8", "#f59e0b", "#22c55e"]


def beta_mode(a, b):
    """Mode of Beta(a, b) as text, covering every shape (interior peak, edges, U-shape, flat)."""
    a1, b1 = np.isclose(a, 1.0), np.isclose(b, 1.0)
    if a > 1 and b > 1 and not (a1 or b1):
        return f"{(a - 1) / (a + b - 2):.4f}", (a - 1) / (a + b - 2)
    if a1 and b1:
        return "every p (flat: Beta(1,1) is Uniform)", None
    if a < 1 and b < 1 and not (a1 or b1):
        return "0 and 1 (U-shape, density → ∞ at both ends)", None
    if (a < 1 or a1) and (b > 1 or b1):
        return "0 (density largest at the left edge)", 0.0
    return "1 (density largest at the right edge)", 1.0


def beta_grid(a, b):
    """x-grid on (0, 1) refined around the bulk of Beta(a, b) so very peaked curves stay smooth."""
    mean = a / (a + b)
    sd = np.sqrt(a * b / ((a + b) ** 2 * (a + b + 1)))
    local = np.clip(mean + sd * np.linspace(-7, 7, 500), 5e-4, 1 - 5e-4)
    return np.unique(np.concatenate([np.linspace(5e-4, 1 - 5e-4, 1000), local]))


def y_cap(*curves_and_grids):
    """Upper y-limit ignoring the (possibly infinite) spikes at the very edges."""
    peaks = [float(np.max(y[(x > 0.01) & (x < 0.99)], initial=0.0)) for x, y in curves_and_grids]
    return 1.1 * max(max(peaks), 1.0)


def render_intro():
    st.title("🎯 Page 86: Beta Distribution — Beliefs about Probabilities")
    st.markdown("### A distribution *over* a probability: how sure are you that the click-through rate is 3 %?")
    with st.container(border=True):
        st.markdown(
            r"""
**Intuition.** A new ad was clicked 3 times out of 10 views. Is its click rate $p$ exactly $0.3$? Surely not — it
could plausibly be 0.15 or 0.5. The **Beta distribution** puts a probability density over every possible
$p\in[0,1]$:

$$\text{Beta}(p;\alpha,\beta)=\frac{p^{\alpha-1}(1-p)^{\beta-1}}{B(\alpha,\beta)}$$

Read $\alpha$ as "successes seen + prior" and $\beta$ as "failures seen + prior". Seeing data just **adds counts**:
heads raise $\alpha$, tails raise $\beta$. That is Bayes' theorem in its friendliest form, and it powers
A/B tests and the bandit algorithms that choose which ad, prompt or model variant to show next.
"""
        )


def render_pdf_lab():
    st.header("🧪 Lab 1 — Shapes of Beta(α, β)")
    c1, c2 = st.columns([1, 2])
    with c1:
        a = st.slider("α", 0.1, 20.0, 2.0, 0.1, key="p86_a")
        b = st.slider("β", 0.1, 20.0, 5.0, 0.1, key="p86_b")
        mean = a / (a + b)
        var = a * b / ((a + b) ** 2 * (a + b + 1))
        mode_text, mode_val = beta_mode(a, b)
        st.metric("Mean α / (α + β)", f"{mean:.4f}")
        st.metric("Variance αβ / ((α+β)²(α+β+1))", f"{var:.5f}", help=f"Standard deviation = {np.sqrt(var):.4f}")
        st.markdown(f"**Mode:** {mode_text}")
        sc_mean, sc_var = stats.beta.stats(a, b, moments="mv")
        st.caption(f"scipy.stats.beta check: mean {float(sc_mean):.4f}, variance {float(sc_var):.5f}")
    x = beta_grid(a, b)
    pdf = stats.beta.pdf(x, a, b)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=pdf, fill="tozeroy", line=dict(color="#a78bfa", width=3), name=f"Beta({a:g}, {b:g})"))
    fig.add_vline(x=mean, line_color="#22c55e", line_dash="dash", annotation_text="mean")
    if mode_val is not None:
        fig.add_vline(x=mode_val, line_color="#f59e0b", line_dash="dot", annotation_text="mode",
                      annotation_position="bottom right")
    fig.update_layout(template="plotly_dark", height=380, margin=dict(l=10, r=10, t=30, b=10),
                      xaxis=dict(title="p", range=[0, 1]), yaxis=dict(title="density", range=[0, y_cap((x, pdf))]))
    with c2:
        st.plotly_chart(fig, width="stretch")
    if a < 1 or b < 1:
        st.info("α < 1 or β < 1 pushes density to the edges (it is infinite at p = 0 and/or 1, so the plot is clipped). "
                "Beta(0.5, 0.5) says: 'p is probably near 0 or near 1 — I just don't know which.'")

    gallery = [(1, 1, "flat: no idea"), (0.5, 0.5, "U: extreme"), (2, 8, "skewed: p small"), (20, 20, "peaked: p≈½")]
    gfig = make_subplots(rows=1, cols=4, subplot_titles=[f"Beta({ga:g},{gb:g}) — {t}" for ga, gb, t in gallery])
    gx = np.linspace(0.005, 0.995, 300)
    for i, (ga, gb, _) in enumerate(gallery, start=1):
        gfig.add_trace(go.Scatter(x=gx, y=stats.beta.pdf(gx, ga, gb), line=dict(color="#94a3b8")), 1, i)
    gfig.update_layout(template="plotly_dark", height=200, showlegend=False, margin=dict(l=10, r=10, t=40, b=10))
    gfig.update_yaxes(range=[0, 6])
    st.plotly_chart(gfig, width="stretch")


def coin_counts():
    """Return (heads, tails, true_p or None) from the selected data source."""
    source = st.radio("Data", ["🪙 Flip a simulated coin", "⌨️ Type counts"], horizontal=True, key="p86_source")
    if source.startswith("⌨️"):
        c1, c2 = st.columns(2)
        h = int(c1.number_input("Heads h", 0, MAX_FLIPS, 7, 1, key="p86_h"))
        t = int(c2.number_input("Tails t", 0, MAX_FLIPS, 3, 1, key="p86_t"))
        return h, t, None, None

    true_p = st.slider("True (hidden) probability of heads p", 0.0, 1.0, 0.7, 0.01, key="p86_true_p")
    b1, b2, b3, b4, b5 = st.columns(5)
    n = st.session_state["p86_nflips"]
    if b1.button("Flip 1", key="p86_flip1"):
        n += 1
    if b2.button("Flip 10", key="p86_flip10"):
        n += 10
    if b3.button("Flip 100", key="p86_flip100"):
        n += 100
    if b4.button("↩️ Reset flips", key="p86_reset_flips"):
        n = 0
    if b5.button("🎲 New coin seed", key="p86_coin_resample"):
        st.session_state["p86_coin_seed"] += 1
    n = min(n, MAX_FLIPS)
    st.session_state["p86_nflips"] = n
    flips = np.random.default_rng(st.session_state["p86_coin_seed"]).random(n) < true_p
    h = int(flips.sum())
    if n == MAX_FLIPS:
        st.caption(f"Capped at {MAX_FLIPS:,} flips.")
    return h, n - h, true_p, flips


def render_coin_lab():
    st.header("🧪 Lab 2 — Learning a coin's bias, one flip at a time")
    c1, c2, c3 = st.columns(3)
    a0 = c1.slider("Prior α₀ (pseudo-heads)", 0.5, 50.0, 2.0, 0.5, key="p86_a0")
    b0 = c2.slider("Prior β₀ (pseudo-tails)", 0.5, 50.0, 2.0, 0.5, key="p86_b0")
    level = c3.slider("Credible level (%)", 50, 99, 95, 1, key="p86_level")
    h, t, true_p, flips = coin_counts()
    n = h + t
    a, b = a0 + h, b0 + t
    lo, hi = stats.beta.ppf([(1 - level / 100) / 2, (1 + level / 100) / 2], a, b)
    post_mean = a / (a + b)
    prior_mean = a0 / (a0 + b0)
    mle = h / n if n > 0 else None

    x = np.unique(np.concatenate([beta_grid(a, b), beta_grid(a0, b0)]))
    prior_pdf = stats.beta.pdf(x, a0, b0)
    post_pdf = stats.beta.pdf(x, a, b)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=prior_pdf, name=f"prior Beta({a0:g}, {b0:g})", line=dict(color="#94a3b8", dash="dot")))
    curves = [(x, prior_pdf), (x, post_pdf)]
    if n > 0:
        lik = stats.beta.pdf(x, h + 1, t + 1)  # likelihood p^h (1-p)^t rescaled to integrate to 1
        curves.append((x, lik))
        fig.add_trace(go.Scatter(x=x, y=lik, name="likelihood (normalized)", line=dict(color="#f59e0b", dash="dash")))
    band = (x >= lo) & (x <= hi)
    fig.add_trace(go.Scatter(x=x[band], y=post_pdf[band], fill="tozeroy", line=dict(width=0),
                             fillcolor="rgba(167,139,250,0.35)", name=f"{level}% credible interval"))
    fig.add_trace(go.Scatter(x=x, y=post_pdf, name=f"posterior Beta({a:g}, {b:g})", line=dict(color="#a78bfa", width=3)))
    if true_p is not None:
        fig.add_vline(x=true_p, line_color="#ef4444", annotation_text="true p")
    fig.update_layout(template="plotly_dark", height=400, margin=dict(l=10, r=10, t=30, b=10),
                      xaxis=dict(title="p", range=[0, 1]), yaxis=dict(title="density", range=[0, y_cap(*curves)]),
                      legend=dict(orientation="h", y=1.12))
    st.plotly_chart(fig, width="stretch")

    m = st.columns(5)
    m[0].metric("Data", f"{h} H / {t} T")
    m[1].metric("Posterior mean", f"{post_mean:.4f}")
    m[2].metric("MLE h / n", "undefined (n = 0)" if mle is None else f"{mle:.4f}")
    m[3].metric(f"{level}% credible interval", f"[{lo:.3f}, {hi:.3f}]")
    m[4].metric("Interval width", f"{hi - lo:.4f}")

    if flips is not None and flips.size > 0:
        k = np.arange(flips.size + 1)
        cum_h = np.concatenate([[0], np.cumsum(flips)])
        ah, bh = a0 + cum_h, b0 + (k - cum_h)
        lo_h, hi_h = stats.beta.ppf((1 - level / 100) / 2, ah, bh), stats.beta.ppf((1 + level / 100) / 2, ah, bh)
        hfig = go.Figure()
        hfig.add_trace(go.Scatter(x=k, y=hi_h, line=dict(width=0), showlegend=False))
        hfig.add_trace(go.Scatter(x=k, y=lo_h, fill="tonexty", line=dict(width=0), fillcolor="rgba(167,139,250,0.3)",
                                  name=f"{level}% credible band"))
        hfig.add_trace(go.Scatter(x=k, y=ah / (ah + bh), name="posterior mean", line=dict(color="#a78bfa")))
        hfig.add_hline(y=true_p, line_color="#ef4444", annotation_text="true p")
        hfig.update_layout(template="plotly_dark", height=260, margin=dict(l=10, r=10, t=30, b=10),
                           xaxis_title="number of flips", yaxis=dict(title="p", range=[0, 1]))
        st.plotly_chart(hfig, width="stretch")
        st.caption("The band narrows roughly like 1/√n: the posterior concentrates around the true p.")
    return a0, b0, h, t, level, (lo, hi), prior_mean, post_mean, mle


def render_coin_example(a0, b0, h, t, level, ci, prior_mean, post_mean, mle):
    st.header("🧮 Worked example — conjugate update with your numbers")
    n = h + t
    a, b = a0 + h, b0 + t
    st.latex(r"\underbrace{p^{h}(1-p)^{t}}_{\text{likelihood}}\cdot\underbrace{p^{\alpha_0-1}(1-p)^{\beta_0-1}}"
             r"_{\text{prior}}\;\propto\;p^{\alpha_0+h-1}(1-p)^{\beta_0+t-1}\;\Rightarrow\;"
             r"\text{posterior}=\text{Beta}(\alpha_0+h,\ \beta_0+t)")
    st.latex(rf"\text{{Beta}}({a0:g},{b0:g})\ +\ ({h}\ \text{{H}},\ {t}\ \text{{T}})\ \longrightarrow\ "
             rf"\text{{Beta}}({a:g},{b:g})")
    w = (a0 + b0) / (a0 + b0 + n)
    st.latex(rf"\mathbb E[p\mid\text{{data}}]=\frac{{\alpha_0+h}}{{\alpha_0+\beta_0+n}}=\frac{{{a:g}}}{{{a + b:g}}}"
             rf"={post_mean:.4f}")
    if mle is not None:
        st.latex(rf"=\underbrace{{{w:.3f}}}_{{w=\frac{{\alpha_0+\beta_0}}{{\alpha_0+\beta_0+n}}}}\times"
                 rf"\underbrace{{{prior_mean:.4f}}}_{{\text{{prior mean}}}}+{1 - w:.3f}\times"
                 rf"\underbrace{{{mle:.4f}}}_{{\text{{MLE }}h/n}}={w * prior_mean + (1 - w) * mle:.4f}")
    else:
        st.caption("No data yet (n = 0): the posterior is the prior, and the MLE h/n is undefined (0/0).")
    st.latex(rf"{level}\%\ \text{{credible interval}} = \big[F^{{-1}}({(1 - level / 100) / 2:.3f}),\ "
             rf"F^{{-1}}({(1 + level / 100) / 2:.3f})\big] = [{ci[0]:.4f},\ {ci[1]:.4f}]")
    st.caption(
        f"The prior acts like {a0 + b0:g} imaginary flips ({a0:g} heads, {b0:g} tails); with n = {n} real flips the "
        f"prior keeps weight w = {w:.3f}. Laplace smoothing is the special case Beta(1, 1): (h+1)/(n+2) = "
        f"{(h + 1) / (n + 2):.4f}. This is Bayes' theorem (page 27) with a continuous hypothesis p."
    )


def thompson_replay(true_ps, steps, seed):
    """Replay Thompson sampling deterministically; returns successes, failures, regret curve, last draw."""
    rng = np.random.default_rng(seed)
    k = len(true_ps)
    succ, fail = np.zeros(k), np.zeros(k)
    best = max(true_ps)
    regret = np.zeros(steps + 1)
    last = None
    for s in range(steps):
        theta = rng.beta(1 + succ, 1 + fail)
        arm = int(np.argmax(theta))
        reward = int(rng.random() < true_ps[arm])
        succ[arm] += reward
        fail[arm] += 1 - reward
        regret[s + 1] = regret[s] + best - true_ps[arm]
        last = (theta, arm, reward)
    return succ, fail, regret, last


def render_thompson_lab():
    st.header("🧪 Lab 3 — Thompson sampling: 3 slot machines")
    st.markdown("Each round: draw one plausible rate θᵢ from every arm's Beta posterior, play the arm with the largest "
                "draw, then update that arm. Uncertain arms sometimes draw high → exploration for free.")
    cols = st.columns(3)
    true_ps = [cols[i].slider(f"Arm {i + 1} true rate", 0.0, 1.0, d, 0.01, key=f"p86_arm_{i}")
               for i, d in enumerate([0.30, 0.50, 0.60])]
    b1, b2, b3, b4 = st.columns(4)
    steps = st.session_state["p86_ts_steps"]
    if b1.button("▶️ Step 1 round", key="p86_ts_step1"):
        steps += 1
    if b2.button("⏩ Run 50 rounds", key="p86_ts_step50"):
        steps += 50
    if b3.button("↩️ Reset bandit", key="p86_ts_reset"):
        steps = 0
    if b4.button("🎲 New bandit seed", key="p86_ts_resample"):
        st.session_state["p86_ts_seed"] += 1
    steps = min(steps, MAX_TS_STEPS)
    st.session_state["p86_ts_steps"] = steps
    succ, fail, regret, last = thompson_replay(true_ps, steps, st.session_state["p86_ts_seed"])
    pulls = succ + fail

    x = np.linspace(5e-4, 1 - 5e-4, 2001)
    fig = make_subplots(rows=1, cols=2, column_widths=[0.65, 0.35],
                        subplot_titles=("Posterior Beta(1+wins, 1+losses) per arm", "Cumulative regret"))
    curves = []
    for i in range(3):
        pdf = stats.beta.pdf(x, 1 + succ[i], 1 + fail[i])
        curves.append((x, pdf))
        fig.add_trace(go.Scatter(x=x, y=pdf, name=f"Arm {i + 1}: {int(pulls[i])} pulls",
                                 line=dict(color=ARM_COLORS[i], width=3)), 1, 1)
        fig.add_vline(x=true_ps[i], line_color=ARM_COLORS[i], line_dash="dot", row=1, col=1)
    fig.add_trace(go.Scatter(x=np.arange(steps + 1), y=regret, name="regret Σ(p* − p_chosen)",
                             line=dict(color="#ef4444")), 1, 2)
    fig.update_xaxes(range=[0, 1], title_text="rate θ", row=1, col=1)
    fig.update_xaxes(title_text="round", row=1, col=2)
    fig.update_yaxes(range=[0, y_cap(*curves)], row=1, col=1)
    fig.update_layout(template="plotly_dark", height=400, margin=dict(l=10, r=10, t=40, b=10),
                      legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig, width="stretch")

    draws = np.random.default_rng(st.session_state["p86_ts_seed"] + 1).beta(1 + succ, 1 + fail, size=(20_000, 3))
    p_best = np.bincount(np.argmax(draws, axis=1), minlength=3) / draws.shape[0]
    m = st.columns(4)
    m[0].metric("Rounds played", f"{steps}")
    for i in range(3):
        m[i + 1].metric(f"P(arm {i + 1} is best)", f"{p_best[i]:.3f}", f"{int(pulls[i])} pulls")
    if last is not None:
        theta, arm, reward = last
        st.caption(f"Last round: sampled θ = ({', '.join(f'{v:.3f}' for v in theta)}) → played arm {arm + 1} → "
                   f"{'win ✅' if reward else 'loss ❌'}. With no data every posterior is Beta(1, 1) = Uniform.")
    else:
        st.caption("Press ▶️ to play. With no data every posterior is Beta(1, 1) = Uniform, so each arm is equally likely.")


def render_ai_connection():
    st.header("🤖 AI / ML connection")
    c1, c2, c3 = st.columns(3)
    with c1, st.container(border=True):
        st.markdown("**A/B testing.** Give each variant (button colour, prompt template, model version) a Beta "
                    "posterior over its conversion rate and report *P(B beats A)* — computed exactly like the "
                    "'P(arm is best)' metrics above — instead of a bare p-value.")
    with c2, st.container(border=True):
        st.markdown("**Bandits & Thompson sampling.** Recommenders, ad servers and LLM routing systems pick among "
                    "options online; Thompson sampling balances exploring uncertain options with exploiting good "
                    "ones, and its regret grows only logarithmically.")
    with c3, st.container(border=True):
        st.markdown(r"**Smoothing & CTR uncertainty.** Laplace (add-one) smoothing is the posterior mean under "
                    r"Beta(1,1): $(h+1)/(n+2)$ never returns 0 for unseen events. Ranking items by a lower credible "
                    r"bound avoids promoting an item with 1 click out of 1 view.")


def render_takeaways():
    st.header("✅ Key takeaways")
    st.markdown(
        r"""
* $\text{Beta}(\alpha,\beta)$ is a distribution over a probability $p\in[0,1]$: mean $\frac{\alpha}{\alpha+\beta}$,
  variance $\frac{\alpha\beta}{(\alpha+\beta)^2(\alpha+\beta+1)}$; $\alpha,\beta<1$ gives a U-shape.
* It is **conjugate** to Bernoulli/Binomial data: prior $\text{Beta}(\alpha,\beta)$ + $h$ heads, $t$ tails
  → posterior $\text{Beta}(\alpha+h,\beta+t)$. The prior is worth $\alpha+\beta$ pseudo-flips.
* The posterior mean is a weighted average of prior mean and MLE $h/n$; data wins as $n$ grows.
* Credible intervals come straight from quantiles (`scipy.stats.beta.ppf`); Thompson sampling turns posteriors into decisions.
"""
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        safe_page_link("pages/85Poisson & Exponential Distributions.py", "⬅️ Previous: 85 · Poisson & Exponential")
    with c2:
        safe_page_link("pages/27Bayes' Theorem.py", "📎 Related: 27 · Bayes' Theorem")
    with c3:
        safe_page_link("pages/87Maximum Likelihood Estimation.py", "➡️ Next: 87 · Maximum Likelihood Estimation")


def main():
    for key, value in [("p86_nflips", 0), ("p86_coin_seed", 86), ("p86_ts_steps", 0), ("p86_ts_seed", 860)]:
        st.session_state.setdefault(key, value)
    render_intro()
    render_pdf_lab()
    st.divider()
    result = render_coin_lab()
    render_coin_example(*result)
    st.divider()
    render_thompson_lab()
    st.divider()
    render_ai_connection()
    render_takeaways()


main()
