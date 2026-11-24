import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from scipy.special import xlogy
from scipy.stats import norm

# Repo root on sys.path so `common` also imports when this page runs on its own (or under AppTest).
_ROOT = str(Path(__file__).resolve().parents[1])
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from common.mathutils import sigmoid  # noqa: E402
from common.nav import safe_page_link  # noqa: E402

st.set_page_config(page_title="87 · Maximum Likelihood Estimation", page_icon="🎯", layout="wide")

LN2 = np.log(2.0)


def _seed(name, default):
    key = f"p87_seed_{name}"
    if key not in st.session_state:
        st.session_state[key] = default
    return st.session_state[key]


def _bump_seed(name):
    st.session_state[f"p87_seed_{name}"] += 1


def bernoulli_loglik(h, n, p):
    """ℓ(p) = h ln p + (n − h) ln(1 − p) in nats; xlogy makes 0·ln 0 = 0 so h = 0 or h = n is fine."""
    p = np.asarray(p, dtype=float)
    return xlogy(h, p) + xlogy(n - h, 1.0 - p)


def gauss_loglik(xbar, var_mle, n, mu, sigma):
    """Gaussian log-likelihood (nats) written with the sufficient statistics x̄ and σ̂²_MLE."""
    return -0.5 * n * np.log(2 * np.pi * sigma**2) - n * ((xbar - mu) ** 2 + var_mle) / (2 * sigma**2)


def render_intuition():
    st.title("🎯 Maximum Likelihood Estimation")
    st.markdown(
        "You flip a coin 20 times and see 7 heads. Which coin bias $p$ *best explains* what you saw? "
        "**Maximum likelihood** answers: pick the parameter under which the observed data would have been most probable."
    )
    c1, c2 = st.columns(2)
    with c1, st.container(border=True):
        st.markdown("**Probability** — parameter fixed, data varies")
        st.latex(r"P(\text{data} \mid p=0.5) \;\text{: how likely are different outcomes?}")
    with c2, st.container(border=True):
        st.markdown("**Likelihood** — data fixed, parameter varies")
        st.latex(r"L(p) = P(\text{observed data} \mid p) \;\text{: which } p \text{ fits best?}")
    st.info(
        "The likelihood is **not** a probability distribution over $p$ (it need not integrate to 1). "
        r"We maximize the **log**-likelihood $\ell = \ln L$ instead: products become sums, tiny numbers stop underflowing, "
        r"and the argmax is unchanged because $\ln$ is increasing. Logs on this page are natural logs (**nats**) "
        r"unless marked *bits* ($\log_2$, as on the information-theory pages; 1 nat = 1/ln 2 ≈ 1.443 bits)."
    )
    st.markdown("**Why it matters for AI:** almost every training loss — cross-entropy, MSE, next-token loss of an LLM — is a negative log-likelihood. *Training = maximum likelihood.*")


def render_bernoulli_lab():
    st.header("🪙 Lab 1 — Coin flips: the likelihood curve")
    left, right = st.columns([1, 2], gap="large")
    with left:
        n = st.slider("Number of flips n", 1, 200, 20, key="p87_n")
        p_true = st.slider("True (hidden) bias p", 0.0, 1.0, 0.3, 0.05, key="p87_p_true")
        st.button("🎲 Resample flips", key="p87_resample_coin", on_click=_bump_seed, args=("coin",))
        rng = np.random.default_rng(_seed("coin", 87))
        x = (rng.random(n) < p_true).astype(int)
        h = int(x.sum())
        p_hat = h / n
        m1, m2 = st.columns(2)
        m1.metric("Heads h", f"{h} / {n}")
        m2.metric("MLE  p̂ = h/n", f"{p_hat:.3f}")
        p_model = st.slider("Try a model p (for the loss check)", 0.01, 0.99, 0.6, 0.01, key="p87_p_model")
        st.caption("Flips: " + "".join("H" if v else "T" for v in x[:60]) + (" …" if n > 60 else ""))

    p_grid = np.linspace(0.0, 1.0, 1001)
    ll = bernoulli_loglik(h, n, p_grid)
    ll_max = float(bernoulli_loglik(h, n, p_hat))
    rel_lik = np.exp(ll - ll_max)  # L(p)/L(p̂): avoids underflow of p^h(1-p)^(n-h) for large n
    ll_plot = np.where(np.isfinite(ll), ll, np.nan)
    ll_model = float(bernoulli_loglik(h, n, p_model))

    with right:
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Likelihood L(p) / L(p̂)", "Log-likelihood ℓ(p) (nats)"))
        fig.add_trace(go.Scatter(x=p_grid, y=rel_lik, name="L(p)/L(p̂)", line=dict(color="#60a5fa", width=3)), row=1, col=1)
        fig.add_trace(go.Scatter(x=p_grid, y=ll_plot, name="ℓ(p)", line=dict(color="#34d399", width=3)), row=1, col=2)
        fig.add_trace(go.Scatter(x=[p_hat], y=[1.0], mode="markers", name=f"max at p̂={p_hat:.3f}", marker=dict(size=12, color="#fbbf24", symbol="star")), row=1, col=1)
        fig.add_trace(go.Scatter(x=[p_hat], y=[ll_max], mode="markers", showlegend=False, marker=dict(size=12, color="#fbbf24", symbol="star")), row=1, col=2)
        fig.add_trace(go.Scatter(x=[p_model], y=[ll_model], mode="markers", name=f"model p={p_model:.2f}", marker=dict(size=10, color="#f472b6")), row=1, col=2)
        for col in (1, 2):
            fig.add_vline(x=p_true, line_dash="dot", line_color="#94a3b8", row=1, col=col)
        finite = ll_plot[np.isfinite(ll_plot)]
        y_low = max(float(finite.min()), ll_max - max(15.0, 0.6 * n))
        fig.update_yaxes(range=[y_low, ll_max + 0.08 * (ll_max - y_low) + 0.1], row=1, col=2)
        fig.update_xaxes(title_text="p", range=[0, 1])
        fig.update_layout(height=400, margin=dict(t=50, b=40), legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig, width="stretch")
        st.caption("Dotted grey line = true p. The star (the MLE) sits at h/n, which is generally *not* the true p — it moves every time you resample.")
    return x, h, n, p_hat, p_model


def render_bernoulli_math(x, h, n, p_hat, p_model):
    st.subheader("🧮 Worked example — why the peak is at h/n, and why NLL = binary cross-entropy")
    st.latex(rf"\ell(p) = h\ln p + (n-h)\ln(1-p) = {h}\ln p + {n - h}\ln(1-p)")
    st.latex(r"\frac{d\ell}{dp} = \frac{h}{p} - \frac{n-h}{1-p} = 0 \;\Longrightarrow\; \hat p = \frac{h}{n} = " + rf"\frac{{{h}}}{{{n}}} = {p_hat:.4f}")
    if h in (0, n):
        st.warning(f"All flips are {'tails' if h == 0 else 'heads'}: ℓ(p) is monotone and the maximum sits on the boundary p̂ = {p_hat:.0f} — the derivative is never zero inside (0, 1).")

    per_sample = -(x * np.log(p_model) + (1 - x) * np.log(1 - p_model))
    bce = float(per_sample.mean())
    nll_per_n = -float(bernoulli_loglik(h, n, p_model)) / n
    df = pd.DataFrame(
        {
            "quantity": ["−ℓ(p)/n from counts h, n", "binary cross-entropy averaged over the n flips", "same BCE in bits (÷ ln 2)"],
            "value": [f"{nll_per_n:.6f} nats", f"{bce:.6f} nats", f"{bce / LN2:.6f} bits"],
        }
    )
    st.markdown(f"At the model value **p = {p_model:.2f}** (pink dot):")
    st.table(df)
    st.latex(r"\text{BCE} = -\frac{1}{n}\sum_{i}\big[x_i\ln p + (1-x_i)\ln(1-p)\big] = -\frac{\ell(p)}{n}")
    st.success("Identical numbers: minimizing binary cross-entropy **is** maximizing the Bernoulli likelihood. Move the pink slider to p̂ to see the smallest possible loss on this data.")


def render_gaussian_lab():
    st.header("📏 Lab 2 — Gaussian data: estimating μ and σ")
    left, right = st.columns([1, 2], gap="large")
    with left:
        n = st.slider("Sample size n", 2, 200, 10, key="p87_g_n")
        mu_true = st.slider("True μ", -3.0, 3.0, 1.0, 0.1, key="p87_mu_true")
        sigma_true = st.slider("True σ", 0.5, 3.0, 1.5, 0.1, key="p87_sigma_true")
        st.button("🎲 Resample data", key="p87_resample_gauss", on_click=_bump_seed, args=("gauss",))
    seed = _seed("gauss", 870)
    rng = np.random.default_rng(seed)
    data = rng.normal(mu_true, sigma_true, n)
    xbar = float(data.mean())
    var_mle = float(data.var(ddof=0))
    var_unb = float(data.var(ddof=1))
    sig_hat = max(np.sqrt(var_mle), 1e-6)

    with left:
        st.latex(rf"\hat\mu = \bar x = {xbar:.3f}")
        st.latex(rf"\hat\sigma^2_{{\text{{MLE}}}} = \tfrac{{1}}{{n}}\textstyle\sum(x_i-\bar x)^2 = {var_mle:.3f}")
        st.latex(rf"s^2 = \tfrac{{1}}{{n-1}}\textstyle\sum(x_i-\bar x)^2 = {var_unb:.3f}")

    half_mu = max(4.0 * sig_hat / np.sqrt(n), 0.5)
    mus = np.linspace(xbar - half_mu, xbar + half_mu, 121)
    sigmas = np.linspace(max(0.05, 0.3 * sig_hat), max(2.5 * sig_hat, sigma_true * 1.2), 121)
    M, S = np.meshgrid(mus, sigmas)
    ll = gauss_loglik(xbar, var_mle, n, M, S)
    ll_max = float(gauss_loglik(xbar, var_mle, n, xbar, sig_hat))
    with right:
        fig = go.Figure(
            go.Contour(x=mus, y=sigmas, z=np.maximum(ll - ll_max, -40.0), colorscale="Viridis", contours=dict(start=-40, end=0, size=2), colorbar=dict(title="ℓ − ℓmax"))
        )
        fig.add_trace(go.Scatter(x=[xbar], y=[sig_hat], mode="markers", name="MLE (x̄, σ̂)", marker=dict(size=14, color="#fbbf24", symbol="star")))
        fig.add_trace(go.Scatter(x=[mu_true], y=[sigma_true], mode="markers", name="truth (μ, σ)", marker=dict(size=11, color="#f472b6", symbol="x")))
        fig.update_layout(title="Log-likelihood surface ℓ(μ, σ), relative to its maximum (nats)", xaxis_title="μ", yaxis_title="σ", height=430, margin=dict(t=50, b=40), legend=dict(orientation="h", y=-0.18))
        st.plotly_chart(fig, width="stretch")
        st.caption("Contours are clipped at 40 nats below the peak. With small n the hill is wide (uncertain); with large n it becomes a sharp peak near the truth (if the truth lies off-grid, the pink × is not shown).")

    st.subheader("⚖️ The MLE of σ² is biased (divides by n, not n − 1)")
    sims = 4000
    rng_b = np.random.default_rng(seed + 10_000)
    sim = rng_b.normal(mu_true, sigma_true, size=(sims, n))
    mean_mle = float(sim.var(axis=1, ddof=0).mean())
    mean_unb = float(sim.var(axis=1, ddof=1).mean())
    c1, c2, c3 = st.columns(3)
    c1.metric("True σ²", f"{sigma_true**2:.3f}")
    c2.metric(f"Avg σ̂²_MLE over {sims} datasets", f"{mean_mle:.3f}", f"theory (n−1)/n·σ² = {(n - 1) / n * sigma_true**2:.3f}", delta_color="off", delta_arrow="off")
    c3.metric(f"Avg s² over {sims} datasets", f"{mean_unb:.3f}", f"theory σ² = {sigma_true**2:.3f}", delta_color="off", delta_arrow="off")
    st.markdown(
        r"$\hat\mu = \bar x$ uses up one degree of freedom, so squared deviations from $\bar x$ are on average smaller than from the true $\mu$: "
        r"$\mathbb E[\hat\sigma^2_{\text{MLE}}] = \frac{n-1}{n}\sigma^2$. Try **n = 2**: the MLE is about half the truth. The bias vanishes as $n\to\infty$ (the MLE is still *consistent*)."
    )
    return data, xbar, var_mle, sigma_true


def render_gauss_nll_mse(data, xbar, var_mle, sigma):
    st.subheader("🔗 Gaussian negative log-likelihood = scaled MSE")
    n = len(data)
    mu_try = st.slider("Candidate prediction μ", -10.0, 10.0, 1.0, 0.1, key="p87_mu_try")
    mse = float(np.mean((data - mu_try) ** 2))
    nll_scipy = -float(norm.logpdf(data, mu_try, sigma).sum())
    nll_formula = 0.5 * n * np.log(2 * np.pi * sigma**2) + n * mse / (2 * sigma**2)
    st.latex(
        r"-\ell(\mu) = \underbrace{\tfrac{n}{2}\ln(2\pi\sigma^2)}_{\text{constant}} + \frac{n}{2\sigma^2}\,\underbrace{\tfrac1n\textstyle\sum(x_i-\mu)^2}_{\text{MSE}(\mu)}"
        + rf"= {0.5 * n * np.log(2 * np.pi * sigma**2):.3f} + {n / (2 * sigma**2):.3f}\times {mse:.3f} = {nll_formula:.3f}"
    )
    c1, c2, c3 = st.columns(3)
    c1.metric("NLL via scipy norm.logpdf", f"{nll_scipy:.4f} nats")
    c2.metric("NLL via the formula", f"{nll_formula:.4f} nats")
    c3.metric("MSE(μ)", f"{mse:.4f}", f"min at μ = x̄ = {xbar:.3f} (MSE = σ̂² = {var_mle:.3f})", delta_color="off", delta_arrow="off")
    st.caption(f"σ is held fixed at the true value {sigma:.1f}. Because NLL is an increasing affine function of MSE, both are minimized by the same μ — the sample mean.")


def render_gradient_ascent(h, n):
    st.header("⛰️ Lab 3 — Gradient ascent finds the same answer")
    st.markdown(
        r"Real models have no closed form, so we climb the log-likelihood numerically. Parametrize the coin by a **logit** $\theta$ with "
        r"$p = \sigma(\theta)$ (exactly what logistic regression does). The gradient of the average log-likelihood is the famous *target − prediction*:"
    )
    st.latex(r"\frac{1}{n}\frac{\partial \ell}{\partial \theta} = \bar x - \sigma(\theta), \qquad \theta_{t+1} = \theta_t + \eta\,\big(\bar x - \sigma(\theta_t)\big)")
    c1, c2 = st.columns([1, 2], gap="large")
    with c1:
        lr = st.slider("Learning rate η", 0.1, 5.0, 1.0, 0.1, key="p87_lr")
        steps = st.slider("Steps", 5, 300, 60, 5, key="p87_steps")
    p_hat = h / n
    theta = np.zeros(steps + 1)
    for t in range(steps):
        theta[t + 1] = theta[t] + lr * (p_hat - sigmoid(theta[t]))
    p_path = sigmoid(theta)
    avg_ll = p_hat * theta - np.logaddexp(0.0, theta)  # ℓ(σ(θ))/n, finite for every θ
    with c1:
        st.metric("Final p after gradient ascent", f"{p_path[-1]:.5f}", f"closed form h/n = {p_hat:.5f}", delta_color="off", delta_arrow="off")
        st.metric("Gap |p_T − h/n|", f"{abs(p_path[-1] - p_hat):.2e}")
        if h in (0, n):
            st.warning(f"h/n = {p_hat:.0f} is on the boundary: the optimal logit is {'−' if h == 0 else '+'}∞, so θ keeps drifting and p only creeps towards {p_hat:.0f} — it never gets there. That is MLE overfitting in action.")
    with c2:
        fig = make_subplots(rows=1, cols=2, subplot_titles=("p_t = σ(θ_t)", "average log-likelihood ℓ/n (nats)"))
        fig.add_trace(go.Scatter(y=p_path, mode="lines+markers", marker=dict(size=4), name="p_t", line=dict(color="#60a5fa")), row=1, col=1)
        fig.add_hline(y=p_hat, line_dash="dash", line_color="#fbbf24", annotation_text="h/n", row=1, col=1)
        fig.add_trace(go.Scatter(y=avg_ll, mode="lines", name="ℓ_t/n", line=dict(color="#34d399")), row=1, col=2)
        best = float(bernoulli_loglik(h, n, p_hat)) / n
        fig.add_hline(y=best, line_dash="dash", line_color="#fbbf24", annotation_text="max", row=1, col=2)
        fig.update_xaxes(title_text="step")
        fig.update_layout(height=340, margin=dict(t=50, b=40), showlegend=False)
        st.plotly_chart(fig, width="stretch")
    st.caption("The curvature of ℓ/n in θ is at most 1/4, so any η < 8 converges (smoothly when η ≤ 4); bigger η just gets there in fewer steps.")


def render_small_n(h, n):
    st.header("⚠️ Small data: MLE overfits")
    st.markdown(
        r"Flip a coin 3 times, see 0 heads → the MLE says $\hat p = 0$: heads is *impossible*. One future head then costs "
        r"$-\ln 0 = \infty$ nats of loss. A **prior** fixes this: with a Beta(a, a) prior the MAP estimate adds pseudo-counts "
        "(see the Beta-distribution page)."
    )
    st.latex(r"\hat p_{\text{MLE}} = \frac{h}{n}, \qquad \hat p_{\text{MAP}} = \frac{h + a - 1}{n + 2a - 2} \quad (\text{Beta}(a,a)\text{ prior}; \; a=2 \text{ gives Laplace smoothing } \tfrac{h+1}{n+2})")
    a = st.slider("Prior strength a (Beta(a, a); a = 1 is a flat prior = plain MLE)", 1.0, 10.0, 2.0, 0.5, key="p87_prior")

    def loss_head(p):
        return "∞" if p <= 0 else f"{-np.log(p) + 0.0:.3f}"

    rows = []
    for hh in range(4):
        mle = hh / 3
        mapp = (hh + a - 1) / (3 + 2 * a - 2)
        rows.append({"data (n = 3)": f"{hh} heads", "MLE p̂": f"{mle:.3f}", f"MAP, a = {a:g}": f"{mapp:.3f}", "loss of a new head, MLE (nats)": loss_head(mle), "… with MAP": loss_head(mapp)})
    st.table(pd.DataFrame(rows))
    mle_cur = h / n
    map_cur = (h + a - 1) / (n + 2 * a - 2)
    st.markdown(f"**Your coin data from Lab 1** (h = {h}, n = {n}): MLE = {mle_cur:.3f}, MAP = {map_cur:.3f}. With large n the two agree — the data swamps the prior.")


def render_ai_connection():
    st.header("🤖 AI / ML connection")
    c1, c2, c3 = st.columns(3)
    with c1, st.container(border=True):
        st.markdown("**Training = MLE**")
        st.markdown(
            "Classifiers minimize cross-entropy = categorical NLL; regressors minimize MSE = Gaussian NLL with fixed σ; "
            "an LLM minimizes the average next-token NLL, and *perplexity* = exp(average NLL in nats)."
        )
    with c2, st.container(border=True):
        st.markdown("**Priors = MAP = regularization**")
        st.markdown(
            "Adding −ln(prior) to the loss gives MAP estimation. A Gaussian prior on weights is exactly **L2 / weight decay**; "
            "a Laplace prior is **L1**. Pseudo-counts (Laplace / add-k smoothing) are a Beta/Dirichlet prior."
        )
    with c3, st.container(border=True):
        st.markdown("**Label smoothing & calibration**")
        st.markdown(
            "Pure MLE pushes predicted probabilities to 0 or 1 on the training set (the logit drifts to ±∞ as in Lab 3). "
            "**Label smoothing** trains against slightly softened targets — it plays a prior-like role, keeping predictions away from overconfident extremes."
        )


def render_takeaways():
    st.header("📌 Key takeaways")
    st.markdown(
        r"""
- **Likelihood** $L(\theta)=P(\text{data}\mid\theta)$ is a function of the parameter with the data held fixed.
- The MLE maximizes $\ell=\ln L$: coin → $\hat p = h/n$; Gaussian → $\hat\mu=\bar x$, $\hat\sigma^2=\frac1n\sum(x_i-\bar x)^2$ (biased low by the factor $\frac{n-1}{n}$).
- Negative log-likelihood **is** the loss: Bernoulli NLL = binary cross-entropy, Gaussian NLL = scaled MSE + constant.
- Gradient ascent on $\ell$ reaches the closed-form answer — when the optimum is finite.
- With little data the MLE overfits ($\hat p = 0$); priors/MAP and smoothing fix it.
"""
    )
    c1, c2 = st.columns(2)
    with c1:
        safe_page_link("pages/86Beta Distribution — Beliefs about Probabilities.py", "← Previous: 86 · Beta Distribution", icon="⬅️")
    with c2:
        safe_page_link("pages/88Confidence Intervals & Hypothesis Tests.py", "Next: 88 · Confidence Intervals & Hypothesis Tests →", icon="➡️")
    safe_page_link("pages/59Cross-Entropy — Predicted vs Reality.py", "Related: 59 · Cross-Entropy (in bits)", icon="🔗")


def main():
    render_intuition()
    st.divider()
    x, h, n, p_hat, p_model = render_bernoulli_lab()
    render_bernoulli_math(x, h, n, p_hat, p_model)
    st.divider()
    data, xbar, var_mle, sigma_true = render_gaussian_lab()
    render_gauss_nll_mse(data, xbar, var_mle, sigma_true)
    st.divider()
    render_gradient_ascent(h, n)
    st.divider()
    render_small_n(h, n)
    st.divider()
    render_ai_connection()
    st.divider()
    render_takeaways()


main()
