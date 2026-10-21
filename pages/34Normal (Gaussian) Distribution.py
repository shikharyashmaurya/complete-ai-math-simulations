import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm

st.set_page_config(page_title="Normal (Gaussian) Distribution", layout="wide")

def local_css():
    st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .hero-box {
        background: linear-gradient(135deg, #020617 0%, #172554 50%, #020617 100%);
        border: 1px solid #3b82f6;
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
        background: radial-gradient(circle, rgba(59,130,246,0.15) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #93c5fd, #60a5fa, #3b82f6);
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
        border-top: 3px solid #3b82f6;
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
        color: #93c5fd;
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
        <div class="hero-title">🔔 Page 34: Normal (Gaussian) Distribution</div>
        <div class="hero-sub">
            Meet the <strong>Bell Curve</strong>. It is the most important probability distribution in all of statistics and AI.
            Why? Under suitable conditions, the <em>Central Limit Theorem</em> says that sums of many independent random variables become approximately bell-shaped when standardized.
            <br><br>
            It has two knobs: <strong>Mean (μ)</strong> to shift it left or right, and <strong>Standard Deviation (σ)</strong> to make it fat or thin.
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_interactive_distribution():
    left, right = st.columns([1, 2], gap="large")

    with left:
        st.markdown('<div class="section-header">🎛️ Shape the Bell</div>', unsafe_allow_html=True)
        st.markdown("""
        See how the parameters **μ** and **σ** control the exact shape and position of the Normal Distribution.
        """)
       
        mu = st.slider(
            "Mean (μ) — Shifts Left/Right",
            min_value=-10.0, max_value=10.0, value=0.0, step=0.5,
            help="Changes the center of the distribution."
        )
       
        sigma = st.slider(
            "Std Deviation (σ) — Makes Fat/Thin",
            min_value=0.5, max_value=5.0, value=1.5, step=0.1,
            help="Controls the spread. Smaller σ means taller and thinner peak."
        )
       
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">📏 The Empirical Rule</div>', unsafe_allow_html=True)
       
        show_1sigma = st.checkbox("Show 1σ Area (68.2%)", value=True)
        show_2sigma = st.checkbox("Show 2σ Area (95.4%)")
        show_3sigma = st.checkbox("Show 3σ Area (99.7%)")
       
        st.markdown("""
        <div class="insight-box">
        <p>
        <strong>Did you know?</strong><br>
        No matter how you change μ and σ, the area under the curve is <strong>always exactly 1</strong> (100% probability).
        As it gets thinner, it <i>must</i> get taller to keep the area equal to 1.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with right:
        x_min = mu - 4 * sigma
        x_max = mu + 4 * sigma
        x = np.linspace(x_min, x_max, 1000)
        y = norm.pdf(x, mu, sigma)
       
        fig = go.Figure()

        # Fill areas for the empirical rule
        if show_3sigma:
            x_3sig = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
            y_3sig = norm.pdf(x_3sig, mu, sigma)
            fig.add_trace(go.Scatter(
                x=np.concatenate([x_3sig, x_3sig[::-1]]),
                y=np.concatenate([y_3sig, np.zeros_like(y_3sig)]),
                fill='toself', fillcolor='rgba(239, 68, 68, 0.2)', line=dict(color='rgba(255,255,255,0)'),
                name='99.7% (3σ)'
            ))

        if show_2sigma:
            x_2sig = np.linspace(mu - 2*sigma, mu + 2*sigma, 100)
            y_2sig = norm.pdf(x_2sig, mu, sigma)
            fig.add_trace(go.Scatter(
                x=np.concatenate([x_2sig, x_2sig[::-1]]),
                y=np.concatenate([y_2sig, np.zeros_like(y_2sig)]),
                fill='toself', fillcolor='rgba(245, 158, 11, 0.3)', line=dict(color='rgba(255,255,255,0)'),
                name='95.4% (2σ)'
            ))

        if show_1sigma:
            x_1sig = np.linspace(mu - sigma, mu + sigma, 100)
            y_1sig = norm.pdf(x_1sig, mu, sigma)
            fig.add_trace(go.Scatter(
                x=np.concatenate([x_1sig, x_1sig[::-1]]),
                y=np.concatenate([y_1sig, np.zeros_like(y_1sig)]),
                fill='toself', fillcolor='rgba(16, 185, 129, 0.4)', line=dict(color='rgba(255,255,255,0)'),
                name='68.2% (1σ)'
            ))

        # The PDF Bell Curve
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='lines',
            name='Normal Distribution',
            line=dict(color='#3b82f6', width=4),
            hoverinfo='skip'
        ))

        # Mean line
        fig.add_vline(x=mu, line_dash="dash", line_color="#94a3b8", line_width=2)
        fig.add_annotation(
            x=mu, y=max(y) + 0.05,
            text=f"μ = {mu}",
            showarrow=False,
            font=dict(color="#f8fafc", size=14, family="Inter")
        )

        fig.update_layout(
            title="The Gaussian Bell Curve",
            xaxis=dict(
                title="Value (x)",
                range=[x_min, x_max],
                gridcolor='rgba(51,65,85,0.4)',
                zerolinecolor='rgba(148,163,184,0.4)',
                zerolinewidth=2
            ),
            yaxis=dict(
                title="Probability Density",
                range=[0, 1.0],
                gridcolor='rgba(51,65,85,0.4)',
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f8fafc', family="Inter"),
            margin=dict(l=20, r=20, t=50, b=40),
            height=500,
            showlegend=True,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )

        st.plotly_chart(fig, use_container_width=True)

def render_math_breakdown():
    st.markdown('<div class="section-header">🧮 Deconstructing the Gaussian Formula</div>', unsafe_allow_html=True)
    st.markdown("The formula for the Normal Distribution looks intimidating, but it is just an elegant mathematical machine. Let's break it down.")
   
    st.latex(r"f(x) = \frac{1}{\sigma \sqrt{2\pi}} e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}")
   
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(r"""
        <div class="stat-card" style="border-top-color:#10b981;">
            <div class="stat-label" style="color:#10b981;">The Distance</div>
            <div style="font-size:1.5rem; margin:10px 0; color:#f8fafc; font-family: 'Times New Roman', serif;"><i>(x - μ)</i></div>
            <div style="color:#cbd5e1; font-size:0.9rem;">Measures how far our point $x$ is from the center $\mu$.</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(r"""
        <div class="stat-card" style="border-top-color:#f43f5e;">
            <div class="stat-label" style="color:#f43f5e;">The Exponential Decay</div>
            <div style="font-size:1.5rem; margin:10px 0; color:#f8fafc; font-family: 'Times New Roman', serif;"><i>e<sup> -(distance)²</sup></i></div>
            <div style="color:#cbd5e1; font-size:0.9rem;">Squaring the distance makes it symmetric (left & right). The negative exponential creates the rapidly falling "bell" shape.</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(r"""
        <div class="stat-card" style="border-top-color:#fbbf24;">
            <div class="stat-label" style="color:#fbbf24;">The Normalizer</div>
            <div style="font-size:1.5rem; margin:10px 0; color:#f8fafc; font-family: 'Times New Roman', serif;"><i>1 / (σ√2π)</i></div>
            <div style="color:#cbd5e1; font-size:0.9rem;">Ensures the total area exactly equals 1. Without this, it wouldn't be a valid probability distribution!</div>
        </div>""", unsafe_allow_html=True)

def render_ai_context():
    st.markdown('<div class="section-header">🤖 Why the Normal Distribution Rules AI</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    examples = [
        ("🎲 Weight Initialization", "#3b82f6",
         "When we create a new Neural Network, we don't start weights at zero. We sample them from a Normal Distribution! This random start gives the network symmetry breaking."),
        ("🖼️ Diffusion Models (AI Art)", "#8b5cf6",
         "Models like Midjourney and DALL-E work by starting with pure Gaussian noise (static). They slowly 'denoise' this bell-curve static into a beautiful image."),
        ("🧠 Variational Autoencoders", "#ec4899",
         "VAEs force their internal 'latent space' to follow a Normal Distribution. This makes the space continuous, so you can smoothly morph one face into another face!")
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
   
    st.divider()
    render_interactive_distribution()
   
    st.divider()
    render_math_breakdown()
   
    st.divider()
    render_ai_context()

if __name__ == "__main__":
    main()
