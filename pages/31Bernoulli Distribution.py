import math

import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Bernoulli Distribution", layout="wide")

def local_css():
    st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: system-ui, sans-serif;
    }

    .hero-box {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        border: 1px solid #4f46e5;
        border-radius: 20px;
        padding: 36px 40px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
    }
    .hero-box::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #a5b4fc, #818cf8, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 12px 0;
    }
    .hero-sub {
        color: #cbd5e1;
        font-size: 1.1rem;
        line-height: 1.7;
        max-width: 750px;
    }

    .coin-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 16px;
        padding: 30px;
        background: #0f172a;
        border-radius: 20px;
        border: 1px solid #1e293b;
    }
    .coin {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        font-weight: 900;
        box-shadow: 0 8px 32px rgba(0,0,0,0.5);
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        cursor: default;
        user-select: none;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    .coin-heads {
        background: linear-gradient(135deg, #fbbf24, #f59e0b, #d97706);
        border: 4px solid #fcd34d;
        color: #1c1917;
    }
    .coin-tails {
        background: linear-gradient(135deg, #94a3b8, #64748b, #475569);
        border: 4px solid #cbd5e1;
        color: #0f172a;
    }
    .coin-label {
        font-size: 1rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        padding: 6px 20px;
        border-radius: 999px;
    }
    .label-heads {
        background: rgba(251,191,36,0.15);
        color: #fbbf24;
        border: 1px solid rgba(251,191,36,0.3);
    }
    .label-tails {
        background: rgba(148,163,184,0.15);
        color: #94a3b8;
        border: 1px solid rgba(148,163,184,0.3);
    }

    .stat-card {
        background: #1e293b;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        border-top: 3px solid #6366f1;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        height: 100%;
    }
    .stat-val {
        font-size: 2.2rem;
        font-weight: 800;
        color: #a5b4fc;
        line-height: 1.1;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-top: 6px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stat-formula {
        font-size: 0.95rem;
        color: #94a3b8;
        margin-top: 8px;
        font-family: 'Courier New', monospace;
    }

    .insight-box {
        background: linear-gradient(135deg, #0f172a, #1e1b4b);
        border: 1px solid #4338ca;
        border-radius: 14px;
        padding: 20px 24px;
        margin: 8px 0;
        border-left: 4px solid #6366f1;
    }
    .insight-box p { color: #e2e8f0; margin: 0; line-height: 1.7; }

    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f1f5f9;
        margin: 0 0 16px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .special-note {
        background: rgba(99,102,241,0.08);
        border: 1px solid rgba(99,102,241,0.25);
        border-radius: 12px;
        padding: 16px 20px;
        color: #c7d2fe;
        font-size: 0.95rem;
        line-height: 1.7;
        margin-top: 12px;
    }
    </style>
    """, unsafe_allow_html=True)


def render_hero():
    st.markdown("""
    <div class="hero-box">
        <div class="hero-title">📊 Page 31: The Bernoulli Distribution</div>
        <div class="hero-sub">
            The <strong>simplest possible random experiment</strong>: flip a (possibly biased) coin.
            You get one of two outcomes — <strong style="color:#fbbf24">Heads (Success)</strong> or
            <strong style="color:#94a3b8">Tails (Failure)</strong>. One slider, <em>p</em>, controls
            the probability of heads. Everything else follows from it.
            <br><br>
            This tiny building block powers spam filters, neural network activations, and A/B tests.
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_coin_section(p):
    """Render the animated coin that visually represents the current bias."""
    # The coin face changes based on p
    if math.isclose(p, 0.5):
        coin_class = "coin-heads"
        coin_emoji = "H"
        label_class = "label-heads"
        label_text = "Fair Coin"
    elif p > 0.5:
        coin_class = "coin-heads"
        coin_emoji = "H"
        label_class = "label-heads"
        label_text = "Always Heads" if math.isclose(p, 1.0) else "Biased → Heads"
    else:
        coin_class = "coin-tails"
        coin_emoji = "T"
        label_class = "label-tails"
        label_text = "Always Tails" if math.isclose(p, 0.0) else "Biased → Tails"

    # Visual fill showing p vs q (round, and derive tails from heads so they sum to 100)
    heads_pct = round(p * 100)
    tails_pct = 100 - heads_pct

    st.markdown(f"""
    <div class="coin-container">
        <div class="coin {coin_class}">{coin_emoji}</div>
        <span class="coin-label {label_class}">{label_text}</span>
        <div style="width:100%; background:#1e293b; border-radius:999px; height:14px; overflow:hidden; margin-top:6px;">
            <div style="
                width:{heads_pct}%;
                height:100%;
                background:linear-gradient(90deg,#fbbf24,#f59e0b);
                border-radius:999px;
                transition: width 0.5s ease;
            "></div>
        </div>
        <div style="display:flex; justify-content:space-between; width:100%; color:#94a3b8; font-size:0.85rem; font-weight:600;">
            <span style="color:#fbbf24;">Heads: {heads_pct}%</span>
            <span style="color:#818cf8;">Tails: {tails_pct}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_distribution_chart(p):
    """PMF bar chart — the core of Bernoulli."""
    q = round(1 - p, 10)

    fig = go.Figure()

    # Tails bar (X=0)
    fig.add_trace(go.Bar(
        x=["0 (Tails / Failure)"],
        y=[q],
        name="P(X=0) = 1-p",
        marker=dict(
            color='rgba(99,102,241,0.85)',
            line=dict(color='#818cf8', width=2)
        ),
        width=0.35,
        text=[f"<b>{q:.3f}</b>"],
        textposition="outside",
        textfont=dict(color="#a5b4fc", size=16, family="Inter")
    ))

    # Heads bar (X=1)
    fig.add_trace(go.Bar(
        x=["1 (Heads / Success)"],
        y=[p],
        name="P(X=1) = p",
        marker=dict(
            color='rgba(251,191,36,0.85)',
            line=dict(color='#fcd34d', width=2)
        ),
        width=0.35,
        text=[f"<b>{p:.3f}</b>"],
        textposition="outside",
        textfont=dict(color="#fcd34d", size=16, family="Inter")
    ))

    fig.update_layout(
        title=dict(
            text="Bernoulli PMF — Probability Mass Function",
            font=dict(size=17, color="#e2e8f0")
        ),
        xaxis=dict(
            title="Outcome (X)",
            tickfont=dict(color="#94a3b8", size=13),
            gridcolor='rgba(51,65,85,0.4)',
            title_font=dict(color="#94a3b8")
        ),
        yaxis=dict(
            title="Probability P(X)",
            range=[0, 1.15],
            tickfont=dict(color="#94a3b8"),
            gridcolor='rgba(51,65,85,0.4)',
            title_font=dict(color="#94a3b8")
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f8fafc', family="Inter"),
        showlegend=True,
        legend=dict(
            bgcolor='rgba(15,23,42,0.8)',
            bordercolor='#334155',
            borderwidth=1,
            font=dict(size=12)
        ),
        bargap=0.5,
        margin=dict(l=20, r=20, t=60, b=40),
        height=380
    )

    # Reference line at 0.5
    fig.add_hline(
        y=0.5, line_dash="dot", line_color="rgba(148,163,184,0.4)",
        annotation_text="p = 0.5 (fair)", annotation_position="right",
        annotation_font=dict(color="#94a3b8", size=11)
    )

    st.plotly_chart(fig, width="stretch")


def render_simulation(p):
    """Simulate many flips and show convergence."""
    st.markdown('<div class="section-header">🎲 Simulate Many Flips — Watch the Law of Large Numbers</div>', unsafe_allow_html=True)
    st.markdown("Flip the coin up to 10,000 times. Watch the observed frequency creep toward the true **p**.")

    n_flips = st.select_slider(
        "Number of flips",
        options=[10, 50, 100, 500, 1000, 5000, 10000],
        value=500
    )

    if st.button("🪙 Flip Again (new random flips)", key="p31_flip_again", width="stretch"):
        st.session_state["p31_flip_seed"] = st.session_state.get("p31_flip_seed", 0) + 1

    # Deterministic by default: the same seed always gives the same flips, so the chart
    # matches the current p and n. Comparing uniforms with p keeps the flips coherent as p changes.
    seed = st.session_state.get("p31_flip_seed", 0)
    rng = np.random.default_rng(seed)
    results = (rng.random(n_flips) < p).astype(int)
    sim_p = p
    sim_n = n_flips

    heads_count = int(np.sum(results))
    tails_count = sim_n - heads_count
    obs_freq = heads_count / sim_n

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="stat-card" style="border-top-color:#fbbf24;">
            <div class="stat-val" style="color:#fbbf24;">{heads_count}</div>
            <div class="stat-label">Heads</div>
            <div class="stat-formula">= {obs_freq:.3f} observed</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card" style="border-top-color:#6366f1;">
            <div class="stat-val" style="color:#818cf8;">{tails_count}</div>
            <div class="stat-label">Tails</div>
            <div class="stat-formula">= {tails_count/sim_n:.3f} observed</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        diff = abs(obs_freq - sim_p)
        # Typical sampling error shrinks like 1/sqrt(n): flag errors beyond ~2 standard errors.
        tolerance = 2 * math.sqrt(sim_p * (1 - sim_p) / sim_n)
        within = diff <= tolerance + 1e-12
        color = "#10b981" if within else "#f59e0b"
        st.markdown(f"""
        <div class="stat-card" style="border-top-color:{color};">
            <div class="stat-val" style="color:{color};">{diff:.4f}</div>
            <div class="stat-label">Error from True p</div>
            <div class="stat-formula">|obs - {sim_p:.2f}| · typical ≤ {tolerance:.4f}</div>
        </div>""", unsafe_allow_html=True)
        st.caption(
            ("✅ Within" if within else "⚠️ Outside")
            + " the usual random range (±2·√(p(1−p)/n)) for this many flips."
        )

    # Running average convergence chart
    running_avg = np.cumsum(results) / np.arange(1, sim_n + 1)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(1, sim_n + 1)),
        y=running_avg,
        mode='lines',
        name='Running frequency of Heads',
        line=dict(color='#fbbf24', width=2)
    ))
    fig.add_hline(
        y=sim_p, line_dash="dash", line_color="#6366f1", line_width=2,
        annotation_text=f"True p = {sim_p:.2f}",
        annotation_position="right",
        annotation_font=dict(color="#a5b4fc", size=12)
    )
    fig.update_layout(
        title="Running Frequency → Converges to p (Law of Large Numbers)",
        xaxis=dict(title="Number of Flips", gridcolor='rgba(51,65,85,0.4)', title_font=dict(color="#94a3b8")),
        yaxis=dict(title="Fraction of Heads", range=[0, 1], gridcolor='rgba(51,65,85,0.4)', title_font=dict(color="#94a3b8")),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f8fafc', family="Inter"),
        margin=dict(l=20, r=20, t=50, b=40),
        height=320,
        showlegend=False
    )
    st.plotly_chart(fig, width="stretch")

    st.markdown(f"""
    <div class="special-note">
    💡 With <strong>{sim_n} flips</strong>, the observed frequency was <strong>{obs_freq:.4f}</strong>
    vs the true probability <strong>p = {sim_p:.2f}</strong>.  
    On average, more flips bring us closer (though not in a perfectly straight line — try "Flip Again").
    This is the <strong>Law of Large Numbers</strong> in action — randomness averages out over time.
    </div>
    """, unsafe_allow_html=True)


def render_stats(p):
    """Show derived statistics with visual formulas."""
    q = 1 - p
    mean = p
    variance = p * q
    std_dev = np.sqrt(variance)

    st.markdown('<div class="section-header">📐 Key Properties — All Derived from p</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-val">{mean:.3f}</div>
            <div class="stat-label">Expected Value (Mean)</div>
            <div class="stat-formula">E[X] = p = {p:.3f}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="stat-card" style="border-top-color:#10b981;">
            <div class="stat-val" style="color:#34d399;">{variance:.4f}</div>
            <div class="stat-label">Variance</div>
            <div class="stat-formula">Var(X) = p·(1-p) = {p:.2f}·{q:.2f}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="stat-card" style="border-top-color:#f43f5e;">
            <div class="stat-val" style="color:#fb7185;">{std_dev:.4f}</div>
            <div class="stat-label">Std Deviation</div>
            <div class="stat-formula">σ = √(p·q) = √{variance:.4f}</div>
        </div>""", unsafe_allow_html=True)

    # Variance landscape: show how variance peaks at p=0.5
    st.markdown("<br>", unsafe_allow_html=True)
    p_range = np.linspace(0, 1, 200)
    var_range = p_range * (1 - p_range)

    fig = go.Figure()
    # Shade area
    fig.add_trace(go.Scatter(
        x=p_range, y=var_range,
        fill='tozeroy',
        fillcolor='rgba(99,102,241,0.15)',
        mode='lines',
        line=dict(color='#6366f1', width=3),
        name='Variance = p(1-p)'
    ))
    # Current p marker
    fig.add_trace(go.Scatter(
        x=[p], y=[variance],
        mode='markers',
        marker=dict(color='#fbbf24', size=14, symbol='circle', line=dict(color='white', width=2)),
        name=f'Current p = {p:.2f}'
    ))
    fig.add_vline(x=p, line_dash="dot", line_color="rgba(251,191,36,0.5)")
    fig.update_layout(
        title="Variance Landscape — Maximum Uncertainty at p = 0.5",
        xaxis=dict(title="p (probability of success)", gridcolor='rgba(51,65,85,0.4)', title_font=dict(color="#94a3b8")),
        yaxis=dict(title="Variance = p·(1-p)", gridcolor='rgba(51,65,85,0.4)', title_font=dict(color="#94a3b8")),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f8fafc', family="Inter"),
        margin=dict(l=20, r=20, t=50, b=40),
        height=280,
        legend=dict(bgcolor='rgba(15,23,42,0.8)', bordercolor='#334155', borderwidth=1)
    )
    st.plotly_chart(fig, width="stretch")

    st.markdown("""
    <div class="insight-box">
    <p>🔑 <strong>Key insight:</strong> Variance peaks at <strong>p = 0.5</strong> (maximum uncertainty —
    you have no idea which way the coin will land) and drops to 0 at p=0 or p=1
    (you always know the outcome — no randomness left).</p>
    </div>
    """, unsafe_allow_html=True)


def render_special_cases():
    """Highlight special cases and where Bernoulli appears in AI."""
    st.markdown('<div class="section-header">🤖 Where Does This Appear in AI?</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    examples = [
        ("🔍 Binary Classification", "#6366f1",
         "Binary classifiers (spam/not-spam, cat/dog, fraud/legit) model each label as a Bernoulli trial. "
         "The output neuron predicts its parameter: <strong>P(Y=1 | input)</strong>."),
        ("🧠 Dropout Regularization", "#10b981",
         "During training, each neuron is randomly <em>dropped</em> with a chosen drop rate r (e.g. 0.5). "
         "That random on/off switch is a Bernoulli(r) random variable per neuron — r here is not the coin's p."),
        ("📊 A/B Testing", "#f59e0b",
         "Did the user click? Yes/No. Each user visit is a Bernoulli trial. "
         "Millions of them form the Binomial distribution — the next page!")
    ]

    for col, (title, color, desc) in zip(cols, examples):
        with col:
            st.markdown(f"""
            <div class="stat-card" style="border-top-color:{color}; text-align:left; padding:22px;">
                <div style="font-size:1.05rem; font-weight:700; color:{color}; margin-bottom:10px;">{title}</div>
                <div style="color:#cbd5e1; font-size:0.9rem; line-height:1.7;">{desc}</div>
            </div>""", unsafe_allow_html=True)


def main():
    local_css()
    render_hero()

    # ── Sidebar slider ──────────────────────────────────────────────────────
    st.sidebar.markdown("## ⚙️ Coin Bias")
    st.sidebar.markdown("Drag **p** to make the coin unfair.")
    p = st.sidebar.slider(
        "p — Probability of Heads (Success)",
        min_value=0.0, max_value=1.0, value=0.5, step=0.01,
        help="p=0.5 is a fair coin. p>0.5 favors heads. p<0.5 favors tails."
    )

    st.sidebar.markdown("---")
    if math.isclose(p, 0.5):
        st.sidebar.success("⚖️ Fair coin! Both outcomes equally likely.")
    elif math.isclose(p, 1.0):
        st.sidebar.info("🔒 Deterministic: the coin always lands Heads — no randomness left.")
    elif math.isclose(p, 0.0):
        st.sidebar.info("🔒 Deterministic: the coin always lands Tails — no randomness left.")
    elif p > 0.7:
        st.sidebar.warning(f"🪙 Heavily biased toward Heads ({p:.0%})")
    elif p < 0.3:
        st.sidebar.warning(f"🪙 Heavily biased toward Tails ({(1-p):.0%})")
    else:
        st.sidebar.info(f"🪙 Slightly biased (p = {p:.2f})")

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    **The Bernoulli Distribution:**
    ```
    X ~ Bernoulli(p)

    P(X=1) = p
    P(X=0) = 1-p

    E[X]   = p
    Var(X) = p(1-p)
    ```
    """)

    # ── Main layout ──────────────────────────────────────────────────────────
    left, right = st.columns([1, 1.6], gap="large")

    with left:
        st.markdown('<div class="section-header">🪙 The Coin</div>', unsafe_allow_html=True)
        render_coin_section(p)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="insight-box">
        <p>
        A <strong>Bernoulli trial</strong> is any experiment with exactly two outcomes.  
        We label them <strong>1 (Success)</strong> and <strong>0 (Failure)</strong>.
        The single parameter <strong>p = {p:.2f}</strong> fully describes the distribution.
        </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Mathematical Formula")
        st.latex(r"P(X = x) = p^x (1-p)^{1-x} \quad \text{for } x \in \{0, 1\}")

    with right:
        render_distribution_chart(p)

    st.divider()
    render_stats(p)

    st.divider()
    render_simulation(p)

    st.divider()
    render_special_cases()

    st.divider()
    st.info("💡 **Takeaway:** Bernoulli(p) is the atom of probability. It has only two outcomes, "
            "one parameter, and yet it forms the foundation for the Binomial distribution (next page) "
            "and the cross-entropy loss (later pages), and it also underlies logistic regression and dropout.")


if __name__ == "__main__":
    main()
