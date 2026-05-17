import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time
from scipy.stats import binom

st.set_page_config(page_title="Binomial Distribution", page_icon="🪙", layout="wide")

def reset_sim():
    st.session_state['binom_results'] = []

if 'binom_results' not in st.session_state:
    st.session_state['binom_results'] = []

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

st.title("🪙 32. Binomial Distribution")
st.markdown("### From Single Flips to Predictable Patterns")
st.write("A **Bernoulli trial** is a single event with two outcomes (like a coin flip). But what happens if you run $n$ Bernoulli trials and count the successes? That count follows a **Binomial Distribution**. Let's see it in action.")

st.divider()

col_control, col_vis = st.columns([1, 2.5])

with col_control:
    st.markdown("### 🎛️ Parameters")
    n_flips = st.slider("Number of Coins ($n$)", min_value=1, max_value=100, value=10, step=1, on_change=reset_sim,
                       help="How many coins are flipped in each trial?")
    p_heads = st.slider("Probability of Heads ($p$)", min_value=0.0, max_value=1.0, value=0.5, step=0.01, on_change=reset_sim,
                       help="How biased is the coin? (0.5 = fair)")
   
    st.markdown("### 🧪 Run Experiments")
    st.write("Click to simulate flipping $n$ coins:")
   
    c1, c2 = st.columns(2)
    with c1:
        btn_1 = st.button("🎲 1 Trial", use_container_width=True)
        btn_100 = st.button("🚀 100 Trials", use_container_width=True)
    with c2:
        btn_10 = st.button("⚡ 10 Trials", use_container_width=True)
        btn_1000 = st.button("🔥 1000 Trials", use_container_width=True)
       
    btn_animate = st.button("🎬 Animate 100 Trials", use_container_width=True, type="primary")
   
    if st.button("🔄 Reset Data", use_container_width=True):
        reset_sim()
        st.rerun()

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
    results = st.session_state['binom_results']
    x = np.arange(0, n_flips + 1)
    theoretical_pmf = binom.pmf(x, n_flips, p_heads)
   
    fig = go.Figure()

    if len(results) > 0:
        counts = pd.Series(results).value_counts()
        empirical_pmf = np.zeros(n_flips + 1)
        for k, v in counts.items():
            empirical_pmf[k] = v / len(results)
           
        fig.add_trace(go.Bar(
            x=x, y=empirical_pmf,
            name='Empirical (Simulation)',
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
        title=f"Distribution of Heads in {n_flips} Flips (Trials Run: {len(results)})",
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
    plot_placeholder.plotly_chart(create_plot(), use_container_width=True)
   
    # Handle actions
    if btn_1:
        if n_flips <= 40:
            flips = []
            for i in range(n_flips):
                flips.append(np.random.rand() < p_heads)
                trial_vis_placeholder.markdown(render_coins(flips), unsafe_allow_html=True)
                time.sleep(0.05)
            heads_count = sum(flips)
            st.session_state['binom_results'].append(heads_count)
            trial_vis_placeholder.markdown(
                render_coins(flips) + f"<div style='text-align:center; font-size: 22px; margin-top: 10px; color: #F5B041;'><b>Result: {heads_count} Heads</b></div>",
                unsafe_allow_html=True
            )
        else:
            heads_count = np.random.binomial(n=n_flips, p=p_heads)
            st.session_state['binom_results'].append(heads_count)
            trial_vis_placeholder.success(f"Quick Simulated 1 trial: Got {heads_count} Heads out of {n_flips}.")
           
        plot_placeholder.plotly_chart(create_plot(), use_container_width=True)

    elif btn_10:
        res = np.random.binomial(n=n_flips, p=p_heads, size=10)
        st.session_state['binom_results'].extend(res)
        plot_placeholder.plotly_chart(create_plot(), use_container_width=True)
        trial_vis_placeholder.info(f"Added 10 trials. Last result: {res[-1]} Heads.")
       
    elif btn_100:
        res = np.random.binomial(n=n_flips, p=p_heads, size=100)
        st.session_state['binom_results'].extend(res)
        plot_placeholder.plotly_chart(create_plot(), use_container_width=True)
        trial_vis_placeholder.info(f"Added 100 trials. Last result: {res[-1]} Heads.")
       
    elif btn_1000:
        res = np.random.binomial(n=n_flips, p=p_heads, size=1000)
        st.session_state['binom_results'].extend(res)
        plot_placeholder.plotly_chart(create_plot(), use_container_width=True)
        trial_vis_placeholder.info(f"Added 1000 trials.")
       
    elif btn_animate:
        for i in range(20): # 20 steps of 5 trials
            res = np.random.binomial(n=n_flips, p=p_heads, size=5)
            st.session_state['binom_results'].extend(res)
            plot_placeholder.plotly_chart(create_plot(), use_container_width=True)
            trial_vis_placeholder.markdown(f"<div style='text-align:center; font-size: 18px; color: #3498DB;'>Animating... Trial {len(st.session_state['binom_results'])}</div>", unsafe_allow_html=True)
            time.sleep(0.1)
        trial_vis_placeholder.success("Animation complete!")

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
    - $p^k$: The probability of getting $k$ heads.
    - $(1-p)^{n-k}$: The probability of getting $n-k$ tails.
    """)

st.info("💡 **Notice:** As you increase the number of trials, the blue empirical histogram perfectly molds to the red theoretical dotted line. This is the **Law of Large Numbers** in action! Furthermore, as you increase $n$ (number of flips), the distribution shape becomes increasingly bell-like, hinting at the **Central Limit Theorem** (which connects Binomial to Normal Distribution!).")

