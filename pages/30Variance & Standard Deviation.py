import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm

st.set_page_config(page_title="Variance & Standard Deviation", layout="wide")

def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
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

    .stat-card {
        background: #1e293b;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        border-top: 3px solid #6366f1;
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
        color: #a5b4fc;
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
        color: #1e293b;
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
        <div class="hero-title">📏 Page 30: Variance & Standard Deviation</div>
        <div class="hero-sub">
            The Expected Value (Mean) tells us the "center" of the data. But how spread out is it?
            That's where <strong>Variance</strong> and <strong>Standard Deviation (σ)</strong> come in.
            <br><br>
            If data is clustered tightly around the mean, the standard deviation is small.
            If the data is spread wide, it's large. Watch how changing σ stretches the distribution!
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_interactive_distribution():
    left, right = st.columns([1, 2], gap="large")

    with left:
        st.markdown('<div class="section-header">🎛️ Control the Spread</div>', unsafe_allow_html=True)
        st.markdown("""
        Use the sliders to adjust the true mean ($\mu$) and the true standard deviation ($\sigma$) of the distribution.
        """)
       
        mu = st.slider(
            "Mean (μ) — The Center Point",
            min_value=-10.0, max_value=10.0, value=0.0, step=0.5,
            help="Shifts the distribution left or right."
        )
       
        sigma = st.slider(
            "Std Deviation (σ) — The Spread",
            min_value=0.5, max_value=5.0, value=1.5, step=0.1,
            help="Stretches or squishes the distribution."
        )
       
        variance = sigma ** 2
       
        st.markdown(f"""
        <div class="insight-box">
        <p>
        <strong>Variance (σ²) = {variance:.2f}</strong><br>
        Variance is the average of the <i>squared</i> differences from the Mean. Because it's squared, the units are squared too!
        </p>
        <p style="margin-top:10px;">
        <strong>Standard Deviation (σ) = {sigma:.2f}</strong><br>
        By taking the square root of Variance, we get Standard Deviation, which brings the units back to the original scale.
        It acts as a standard "ruler" for spread.
        </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("**Population Formulae**")
        st.latex(r"\text{Variance } (\sigma^2) = \frac{\sum_{i=1}^{N} (x_i - \mu)^2}{N}")
        st.latex(r"\text{Standard Deviation } (\sigma) = \sqrt{\frac{\sum_{i=1}^{N} (x_i - \mu)^2}{N}}")
        
        st.markdown("**Sample Formulae**")
        st.latex(r"\text{Variance } (s^2) = \frac{\sum_{i=1}^{n} (x_i - \bar{x})^2}{n-1}")
        st.latex(r"\text{Standard Deviation } (s) = \sqrt{\frac{\sum_{i=1}^{n} (x_i - \bar{x})^2}{n-1}}")

    with right:
        # Generate data for the bell curve (PDF)
        x = np.linspace(-15, 15, 1000)
        y = norm.pdf(x, mu, sigma)
       
        # Generate random sample points to visually show "data points"
        np.random.seed(42) # For stability in animation/slider movement
        sample_size = 150
        sample_x = np.random.normal(mu, sigma, sample_size)
        # Random y jitter just to spread the dots out vertically a little bit below the curve
        sample_y = np.random.uniform(-0.05, -0.01, sample_size)

        fig = go.Figure()

        # The PDF Bell Curve
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='lines',
            name='Probability Density',
            line=dict(color='#6366f1', width=4),
            fill='tozeroy',
            fillcolor='rgba(99,102,241,0.2)'
        ))

        # The scatter plot of data points
        fig.add_trace(go.Scatter(
            x=sample_x, y=sample_y,
            mode='markers',
            name='Sample Data Points',
            marker=dict(
                color='#fbbf24',
                size=6,
                line=dict(color='#f59e0b', width=1),
                opacity=0.7
            )
        ))

        # Mean line
        fig.add_vline(x=mu, line_dash="dash", line_color="#10b981", line_width=2)
        fig.add_annotation(
            x=mu, y=max(y),
            text=f"Mean (μ) = {mu}",
            showarrow=False,
            yshift=10,
            font=dict(color="#10b981", size=14, family="Inter")
        )
       
        # 1 Standard Deviation ranges (Visual Ruler)
        fig.add_vrect(
            x0=mu - sigma, x1=mu + sigma,
            fillcolor="rgba(16, 185, 129, 0.1)", layer="below", line_width=0,
            annotation_text="68% of data", annotation_position="top left",
            annotation_font_size=12, annotation_font_color="#34d399"
        )
        fig.add_vline(x=mu - sigma, line_dash="dot", line_color="rgba(16, 185, 129, 0.6)")
        fig.add_vline(x=mu + sigma, line_dash="dot", line_color="rgba(16, 185, 129, 0.6)")
       
        # +/- 1 Sigma arrows
        fig.add_annotation(
            x=mu + (sigma/2), y=max(y)*0.6,
            ax=mu, ay=max(y)*0.6,
            xref='x', yref='y', axref='x', ayref='y',
            text='+1σ', showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='#34d399',
            font=dict(color="#34d399")
        )
        fig.add_annotation(
            x=mu - (sigma/2), y=max(y)*0.6,
            ax=mu, ay=max(y)*0.6,
            xref='x', yref='y', axref='x', ayref='y',
            text='-1σ', showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='#34d399',
            font=dict(color="#34d399")
        )

        # Ensure axes stay fixed so the animation effect of "stretching/squishing" is obvious
        fig.update_layout(
            title="Normal Distribution: Stretching with σ",
            xaxis=dict(
                title="Data Value",
                range=[-15, 15],
                gridcolor='rgba(51,65,85,0.4)',
                title_font=dict(color="#cbd5e1"),
                zerolinecolor='rgba(148,163,184,0.4)',
                zerolinewidth=2
            ),
            yaxis=dict(
                title="Density",
                range=[-0.07, 0.9],
                gridcolor='rgba(51,65,85,0.4)',
                title_font=dict(color="#cbd5e1"),
                showticklabels=False
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f8fafc', family="Inter"),
            margin=dict(l=20, r=20, t=50, b=40),
            height=450,
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    return mu, sigma, variance

def render_stats_cards(mu, sigma, variance):
    st.markdown('<div class="section-header">📐 Mathematical Definitions</div>', unsafe_allow_html=True)
   
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-val" style="color:#10b981;">{mu:.2f}</div>
            <div class="stat-label">Expected Value (μ)</div>
            <div class="stat-formula">E[X] = \u2211(x \u00b7 P(x))</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="stat-card" style="border-top-color:#f43f5e;">
            <div class="stat-val" style="color:#fb7185;">{variance:.2f}</div>
            <div class="stat-label">Variance (σ²)</div>
            <div class="stat-formula">Var(X) = E[(X - μ)²]</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="stat-card" style="border-top-color:#fbbf24;">
            <div class="stat-val" style="color:#fbbf24;">{sigma:.2f}</div>
            <div class="stat-label">Standard Deviation (σ)</div>
            <div class="stat-formula">σ = \u221A(Var(X))</div>
        </div>""", unsafe_allow_html=True)


def render_ai_context():
    st.markdown('<div class="section-header">🤖 Why Spread Matters in AI</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    examples = [
        ("⚖️ Weight Initialization", "#6366f1",
         "When building Neural Networks, we start by randomly generating weights. If the <strong>Variance</strong> is too high, the network's outputs explode. If it's too low, the signal dies. We tune σ carefully!"),
        ("🌫️ Noise & Uncertainty", "#10b981",
         "In Reinforcement Learning or generative models (like Diffusion), we constantly add or remove random 'noise'. The 'amount of noise' is directly controlled by the <strong>Standard Deviation (σ)</strong>."),
        ("📊 Feature Scaling", "#f59e0b",
         "If one feature has σ=1000 and another has σ=0.1, the AI will get confused. We 'Standardize' data by dividing by σ so all features have the exact same spread (σ=1).")
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
    mu, sigma, variance = render_interactive_distribution()
   
    st.divider()
    render_stats_cards(mu, sigma, variance)
   
    st.divider()
    render_ai_context()
   
    st.divider()
    st.info("💡 **Takeaway:** Variance and Standard Deviation measure the *uncertainty* or *spread* of our data. "
            "A high standard deviation means we are less confident about where the next data point will land. "
            "This concept is the bedrock for dealing with Noise and Distributions in AI.")


if __name__ == "__main__":
    main()

