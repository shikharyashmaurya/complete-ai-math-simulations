import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time
from scipy.stats import binom

st.set_page_config(page_title="Binomial Distribution", page_icon="🪙", layout="wide")

MAX_STORED_TRIALS = 10_000
RNG_SEED = 0

def reset_sim():
    st.session_state['p32_results'] = []
    st.session_state['p32_total_trials'] = 0
    # Seeded generator: the same sequence of button clicks reproduces the same results.
    st.session_state['p32_rng'] = np.random.default_rng(RNG_SEED)

if 'p32_results' not in st.session_state or 'p32_rng' not in st.session_state:
    reset_sim()
st.session_state['p32_results'] = st.session_state['p32_results'][-MAX_STORED_TRIALS:]

def get_rng():
    return st.session_state['p32_rng']

def record_results(results):
    results = [int(r) for r in results]
    st.session_state['p32_total_trials'] += len(results)
    st.session_state['p32_results'] = (
        st.session_state['p32_results'] + results
    )[-MAX_STORED_TRIALS:]

# Styling
st.markdown("""
<style>
    .coin-container {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        justify-content: center;
        padding: 20px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        min-height: 80px;
    }
    .coin {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        font-size: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        transition: transform 0.2s;
    }
    .coin.head {
        background: radial-gradient(circle at 30% 30%, #FFE066, #F5B041);
        color: #7E5109;
        border: 2px solid #F39C12;
    }
    .coin.tail {
        background: radial-gradient(circle at 30% 30%, #E5E7E9, #BDC3C7);
        color: #424949;
        border: 2px solid #95A5A6;
    }
    .coin-pulse {
        animation: pulse 0.3s ease-out;
    }
    @keyframes pulse {
        0% { transform: scale(0.8); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

st.title("🪙 Page 32: Binomial Distribution")
st.markdown("### From Single Flips to Predictable Patterns")
st.write("A **Bernoulli trial** is a single event with two outcomes (like a coin flip). But what happens if you run $n$ Bernoulli trials and count the successes? That count follows a **Binomial Distribution**. Let's see it in action.")

st.divider()

col_control, col_vis = st.columns([1, 2.5])

with col_control:
    st.markdown("### 🎛️ Parameters")
    n_flips = st.slider("Number of Coins ($n$)", min_value=1, max_value=100, value=10, step=1, key="p32_n",
                       help="How many coins are flipped in each trial? (Changing it clears the simulated trials.)")
    p_heads = st.slider("Probability of Heads ($p$)", min_value=0.0, max_value=1.0, value=0.5, step=0.01, key="p32_p",
                       help="How biased is the coin? (0.5 = fair) (Changing it clears the simulated trials.)")

    # Stored trials only make sense for the (n, p) that produced them. Widgets can also reset to
    # their defaults when you leave and return to this page without firing on_change, so compare
    # explicitly instead of relying on callbacks.
    if st.session_state.get('p32_params') != (n_flips, p_heads):
        reset_sim()
        st.session_state['p32_params'] = (n_flips, p_heads)
   
    st.markdown("### 🧪 Run Experiments")
    st.write("Click to simulate flipping $n$ coins:")
   
    c1, c2 = st.columns(2)
    with c1:
        btn_1 = st.button("🎲 1 Trial", key="p32_btn_1", width="stretch")
        btn_100 = st.button("🚀 100 Trials", key="p32_btn_100", width="stretch")
    with c2:
        btn_10 = st.button("⚡ 10 Trials", key="p32_btn_10", width="stretch")
        btn_1000 = st.button("🔥 1000 Trials", key="p32_btn_1000", width="stretch")
       
    btn_animate = st.button("🎬 Animate 100 Trials", key="p32_btn_animate", width="stretch", type="primary")
    animate_coins = st.checkbox("Animate single-trial coin flips", value=True, key="p32_animate_coins",
                                help="Reveal coins one by one for the 🎲 1 Trial button (n ≤ 40).")
   
    st.button("🔄 Reset Data", key="p32_btn_reset", width="stretch", on_click=reset_sim)

def render_coins(flips):
    html = '<div class="coin-container">'
    for f in flips:
        if f:
            html += '<div class="coin head coin-pulse">H</div>'
        else:
            html += '<div class="coin tail coin-pulse">T</div>'
    html += '</div>'
    return html

def create_plot():
    results = st.session_state['p32_results']
    total_trials = st.session_state['p32_total_trials']
    x = np.arange(0, n_flips + 1)
    theoretical_pmf = binom.pmf(x, n_flips, p_heads)
   
    fig = go.Figure()

    if len(results) > 0:
        arr = np.asarray(results, dtype=int)
        # Ignore any value that cannot come from Binomial(n, p) (defensive; stale data is reset above).
        arr = arr[(arr >= 0) & (arr <= n_flips)]
        empirical_pmf = np.bincount(arr, minlength=n_flips + 1) / max(len(arr), 1)
           
        fig.add_trace(go.Bar(
            x=x, y=empirical_pmf,
            name=('Empirical (latest stored trials)' if total_trials > len(results)
                  else 'Empirical (Simulation)'),
            marker_color='#3498DB',
            opacity=0.8,
            hovertemplate="Heads: %{x}<br>Probability: %{y:.4f}<extra></extra>"
        ))

    fig.add_trace(go.Scatter(
        x=x, y=theoretical_pmf,
        mode='lines+markers',
        name='Theoretical (Math)',
        line=dict(color='#E74C3C', width=3, dash='dot'),
        marker=dict(size=8, color='#E74C3C'),
        hovertemplate="Heads: %{x}<br>Theoretical Prob: %{y:.4f}<extra></extra>"
    ))

    fig.update_layout(
        title=f"Distribution of Heads in {n_flips} Flips (Trials Run: {total_trials})",
        xaxis_title="Number of Heads (Successes)",
        yaxis_title="Probability",
        bargap=0.15,
        template="plotly_dark",
        margin=dict(l=40, r=40, t=60, b=40),
        height=450,
        legend=dict(x=0.01, y=0.99, bgcolor="rgba(0,0,0,0.5)"),
        xaxis=dict(tickmode='linear', tick0=0, dtick=max(1, n_flips // 10))
    )
    return fig

with col_vis:
    plot_placeholder = st.empty()
    trial_vis_placeholder = st.empty()

    # Initial plot
    plot_placeholder.plotly_chart(create_plot(), width="stretch")
   
    # Handle actions
    rng = get_rng()
    if btn_1:
        if n_flips <= 40:
            flips = list(rng.random(n_flips) < p_heads)
            if animate_coins:
                # Short reveal (≤ ~0.8 s total); untick the checkbox to show all coins at once.
                for i in range(1, n_flips + 1):
                    trial_vis_placeholder.markdown(render_coins(flips[:i]), unsafe_allow_html=True)
                    time.sleep(0.02)
            heads_count = int(sum(flips))
            record_results([heads_count])
            trial_vis_placeholder.markdown(
                render_coins(flips) + f"<div style='text-align:center; font-size: 22px; margin-top: 10px; color: #F5B041;'><b>Result: {heads_count} Heads</b></div>",
                unsafe_allow_html=True
            )
        else:
            heads_count = int(rng.binomial(n=n_flips, p=p_heads))
            record_results([heads_count])
            trial_vis_placeholder.success(f"Quick Simulated 1 trial: Got {heads_count} Heads out of {n_flips}.")
           
        plot_placeholder.plotly_chart(create_plot(), width="stretch")

    elif btn_10:
        res = rng.binomial(n=n_flips, p=p_heads, size=10)
        record_results(res)
        plot_placeholder.plotly_chart(create_plot(), width="stretch")
        trial_vis_placeholder.info(f"Added 10 trials. Last result: {res[-1]} Heads.")
       
    elif btn_100:
        res = rng.binomial(n=n_flips, p=p_heads, size=100)
        record_results(res)
        plot_placeholder.plotly_chart(create_plot(), width="stretch")
        trial_vis_placeholder.info(f"Added 100 trials. Last result: {res[-1]} Heads.")
       
    elif btn_1000:
        res = rng.binomial(n=n_flips, p=p_heads, size=1000)
        record_results(res)
        plot_placeholder.plotly_chart(create_plot(), width="stretch")
        trial_vis_placeholder.info("Added 1000 trials.")
       
    elif btn_animate:
        # 10 quick frames of 10 trials each (~0.5 s of pauses in total).
        for _ in range(10):
            res = rng.binomial(n=n_flips, p=p_heads, size=10)
            record_results(res)
            plot_placeholder.plotly_chart(create_plot(), width="stretch")
            trial_vis_placeholder.markdown(f"<div style='text-align:center; font-size: 18px; color: #3498DB;'>Animating... Trial {st.session_state['p32_total_trials']}</div>", unsafe_allow_html=True)
            time.sleep(0.05)
        trial_vis_placeholder.success("Animation complete!")

    total_trials = st.session_state['p32_total_trials']
    retained_trials = len(st.session_state['p32_results'])
    if total_trials > retained_trials:
        st.caption(
            f"Showing the latest {retained_trials:,} of {total_trials:,} trials; "
            f"older trials are excluded from the empirical histogram. The limit is "
            f"{MAX_STORED_TRIALS:,} retained trials."
        )
    else:
        st.caption(f"Retaining all {retained_trials:,} simulated trials (limit {MAX_STORED_TRIALS:,}).")

st.divider()

# The Math section
st.markdown("### 🧮 The Math Behind It")
st.write("The exact probability of getting exactly $k$ heads (successes) in $n$ flips is given by the Binomial Probability Mass Function:")

math_col1, math_col2 = st.columns([1, 1])

with math_col1:
    st.latex(r"P(X = k) = \binom{n}{k} \cdot p^k \cdot (1-p)^{n-k}")
   
with math_col2:
    st.markdown("""
    **Breaking it down:**
    - $\\binom{n}{k}$: The number of different ways to arrange $k$ heads in $n$ flips.
    - $p^k$: The probability that the $k$ chosen flips all land heads.
    - $(1-p)^{n-k}$: The probability that the other $n-k$ flips all land tails.
    """)

st.info("💡 **Notice:** As you increase the number of trials, the blue empirical histogram gets closer and closer to the red theoretical dotted line (small random wiggles remain at any finite number of trials). This is the **Law of Large Numbers** in action! Furthermore, as you increase $n$ (number of flips), the distribution shape becomes increasingly bell-like (fastest when $p$ is near 0.5), hinting at the **Central Limit Theorem** (which connects Binomial to Normal Distribution!).")
