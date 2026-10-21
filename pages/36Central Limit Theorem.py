import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm

st.set_page_config(page_title="Central Limit Theorem", layout="wide")

def local_css():
    st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: system-ui, sans-serif;
    }

    .hero-box {
        background: linear-gradient(135deg, #0f172a 0%, #064e3b 50%, #0f172a 100%);
        border: 1px solid #10b981;
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
        background: radial-gradient(circle, rgba(16,185,129,0.15) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #a7f3d0, #34d399, #059669);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 12px 0;
    }
    .hero-sub {
        color: #cbd5e1;
        font-size: 1.1rem;
        line-height: 1.7;
        max-width: 800px;
    }

    .stat-card {
        background: #1e293b;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        border-top: 3px solid #10b981;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        height: 100%;
        transition: transform 0.2s ease;
    }
    .stat-card:hover {
        transform: translateY(-5px);
    }
    .stat-val {
        font-size: 2.2rem;
        font-weight: 800;
        color: #34d399;
        line-height: 1.1;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #b0bec5;
        margin-top: 6px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .insight-box {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid #f59e0b;
        border-radius: 14px;
        padding: 20px 24px;
        margin: 8px 0;
        border-left: 4px solid #fbbf24;
    }
    .insight-box p, .insight-box ul, .insight-box li { color: #e2e8f0; margin: 0; line-height: 1.7; }
    .insight-box ul { margin-top: 10px; padding-left: 20px; }

    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0 0 16px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

def render_hero():
    st.markdown("""
    <div class="hero-box">
        <div class="hero-title">🎲 Page 36: Central Limit Theorem</div>
        <div class="hero-sub">
            The Central Limit Theorem explains why, under suitable conditions (including finite variance), averages of sufficiently large independent samples are approximately Normal—even when the original data is not.<br><br>
            It is the grand bridge between chaotic randomness and structured predictability!
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_interactive_simulation():
    st.markdown('<div class="section-header">✨ The Magic Trick (Dice Simulation)</div>', unsafe_allow_html=True)
   
    st.markdown("""
    Let's roll some virtual 6-sided dice.
    A single die roll is flat (Uniform Distribution). Any number 1 through 6 is equally likely.
    But what happens if we roll multiple dice, add them up, and plot the sums?
    """)
   
    left, right = st.columns([1, 2], gap="large")

    with left:
        st.markdown("### 🎛️ Run the Experiment")
        n_dice = st.slider("Number of Dice per Roll (n)", min_value=1, max_value=50, value=1, step=1,
                           help="How many dice do we roll at the same time?")
        n_rolls = st.select_slider("Number of Rolls (Experiments)", options=[10, 50, 100, 500, 1000, 5000, 10000, 50000], value=1000,
                                   help="How many times do we repeat the experiment to build our histogram?")
       
        # Calculate theoretical expected values
        mu_single = 3.5
        var_single = 35 / 12  # Variance of a 6-sided die
       
        mu_sum = n_dice * mu_single
        std_sum = np.sqrt(n_dice * var_single)
       
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="stat-card" style="border-top-color: #3b82f6;">
            <div class="stat-label" style="color: #3b82f6;">Theoretical Expected Sum</div>
            <div class="stat-val" style="color: #60a5fa;">{mu_sum:.1f}</div>
            <div style="color: #cbd5e1; font-size: 0.9rem; margin-top: 10px;">
                With {n_dice} dice, the average sum is {mu_sum:.1f}.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        # Generate the random data
        # n_rolls rows (experiments), n_dice cols (dice per experiment)
        rng = np.random.default_rng(42)
        rolls = rng.integers(1, 7, size=(n_rolls, n_dice))
        sums = np.sum(rolls, axis=1)
       
        fig = go.Figure()
       
        # Histogram of experimental sums
        fig.add_trace(go.Histogram(
            x=sums,
            histnorm='probability density',
            name='Experimental Data',
            marker_color='#10b981',
            opacity=0.75,
            xbins=dict(start=n_dice-0.5, end=n_dice*6+0.5, size=1)
        ))
       
        # Theoretical Normal Curve Overlay
        x_curve = np.linspace(n_dice - 1, n_dice * 6 + 1, 500)
        y_curve = norm.pdf(x_curve, mu_sum, std_sum)
       
        fig.add_trace(go.Scatter(
            x=x_curve, y=y_curve, mode='lines',
            name='Normal Approximation (not exact)',
            line=dict(color='#fbbf24', width=4, dash='dot')
        ))
       
        # Plot Layout styling
        fig.update_layout(
            title=f"Distribution of Sums ({n_rolls} rolls of {n_dice} dice)",
            xaxis_title="Sum of Dice",
            yaxis_title="Probability Density",
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f8fafc'),
            margin=dict(t=40, b=40),
            height=450,
            bargap=0.05,
            legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
        )
       
        fig.update_xaxes(gridcolor='rgba(51,65,85,0.4)', range=[n_dice-1, n_dice*6+1])
        fig.update_yaxes(gridcolor='rgba(51,65,85,0.4)')
       
        st.plotly_chart(fig, use_container_width=True)
        st.caption("The overlaid Normal curve is an approximation; for small numbers of dice, the sum distribution is discrete and can differ substantially.")

    st.markdown("""
    <div class="insight-box">
    <p>
    <strong>See the Magic? Try moving the sliders!</strong><br>
    <ul>
        <li><strong>n = 1:</strong> The shape is a flat block (Uniform Distribution). Any number from 1 to 6 is equally likely.</li>
        <li><strong>n = 2:</strong> The shape is a triangle. There are many ways to roll a 7 (1+6, 2+5...), but only one way to roll a 2 (1+1).</li>
        <li><strong>n = 10:</strong> The sums are more bell-shaped, but remain discrete and are not a perfect Normal curve.</li>
    </ul>
    </p>
    </div>
    """, unsafe_allow_html=True)


def render_math_breakdown():
    st.markdown('<div class="section-header">🧮 The Formula: Formalizing the Magic</div>', unsafe_allow_html=True)
   
    st.markdown("Here is the formal definition of the Central Limit Theorem:")
   
    st.latex(r"\sqrt{n} \left( \bar{X}_n - \mu \right) \xrightarrow{d} \mathcal{N}(0, \sigma^2)")
   
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(r"""
        <div class="stat-card" style="border-top-color:#ec4899;">
            <div class="stat-label" style="color:#ec4899;">What it means in English</div>
            <div style="color:#cbd5e1; font-size:0.95rem; text-align: left; margin-top: 15px;">
                Take any distribution (dice, coin flips, human heights, crazy irregular shapes). If you take a sample of size <strong>n</strong> and calculate the <strong>mean</strong> (or sum), and repeat this many times... <br><br>
                Under suitable conditions, the distribution of sample means approaches a <strong>Normal Distribution</strong> as <strong>n</strong> grows. A rule such as n > 30 is only a rough guide; highly skewed or heavy-tailed populations may need larger samples.
            </div>
        </div>""", unsafe_allow_html=True)
       
    with c2:
        st.markdown(r"""
        <div class="stat-card" style="border-top-color:#8b5cf6;">
            <div class="stat-label" style="color:#8b5cf6;">Why does this happen?</div>
            <div style="color:#cbd5e1; font-size:0.95rem; text-align: left; margin-top: 15px;">
                When you add many independent random variables together, their extreme values tend to cancel each other out. <br><br>
                Rolling ten 1s in a row is extremely rare. Rolling a mix of highs and lows that average out to the middle is extremely common. This "regression to the mean" creates the peak of the bell curve!
            </div>
        </div>""", unsafe_allow_html=True)

def render_ai_context():
    st.markdown('<div class="section-header">🤖 Why does AI care about the CLT?</div>', unsafe_allow_html=True)
   
    cols = st.columns(3)
    examples = [
        ("🧠 Weight Initialization", "#3b82f6",
         "When initializing Neural Networks, weights are often drawn from a Normal Distribution. Why? Because the output of a neuron is a sum of many inputs (wx + b). Thanks to CLT, this sum tends to be normally distributed, keeping the network stable!"),
        ("📉 Noise in Data", "#f43f5e",
         "Real-world data is full of noise. Because noise is often the sum of many small, independent random factors (sensor jitter, environmental changes, rounding errors), the CLT tells us this noise is usually Normally Distributed (Gaussian noise)."),
        ("🚀 Stochastic Gradient Descent", "#10b981",
         "SGD uses a random mini-batch of data to estimate the true gradient. By the CLT, the average gradient of the mini-batch is a normally distributed random variable centered around the true, full-batch gradient. This allows the model to learn smoothly despite the randomness!")
    ]

    for col, (title, color, desc) in zip(cols, examples):
        with col:
            st.markdown(f"""
            <div class="stat-card" style="border-top-color:{color}; text-align:left; padding:22px;">
                <div style="font-size:1.1rem; font-weight:700; color:{color}; margin-bottom:10px;">{title}</div>
                <div style="color:#cbd5e1; font-size:0.9rem; line-height:1.7;">{desc}</div>
            </div>""", unsafe_allow_html=True)

def main():
    local_css()
    render_hero()
   
    st.divider()
    render_interactive_simulation()
   
    st.divider()
    render_math_breakdown()
   
    st.divider()
    render_ai_context()

if __name__ == "__main__":
    main()
