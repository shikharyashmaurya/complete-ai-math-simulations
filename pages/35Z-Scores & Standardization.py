import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm

st.set_page_config(page_title="Z-Scores & Standardization", layout="wide")

def local_css():
    st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: sans-serif;
    }

    .hero-box {
        background: linear-gradient(135deg, #0f172a 0%, #312e81 50%, #0f172a 100%);
        border: 1px solid #6366f1;
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
        background: linear-gradient(90deg, #c7d2fe, #818cf8, #4f46e5);
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
        color: #818cf8;
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
        border: 1px solid #10b981;
        border-radius: 14px;
        padding: 20px 24px;
        margin: 8px 0;
        border-left: 4px solid #34d399;
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
        <div class="hero-title">📏 Page 35: Z-Scores & Standardization</div>
        <div class="hero-sub">
            Apples to Oranges? Not anymore. Standardization translates any normal distribution into a universal language: the <strong>Standard Normal Distribution</strong>.<br><br>
            A <strong>Z-Score</strong> is simply a visual ruler. It answers one question: <em>"How many standard deviations is this data point away from the mean?"</em>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_interactive_ruler():
    st.markdown('<div class="section-header">⚖️ The Visual Ruler</div>', unsafe_allow_html=True)
   
    st.markdown("""
    Imagine you took a test with an average score of **70** and a standard deviation of **10**.
    You scored an **85**. Is that good? Let's use the Z-score ruler to find out!
    """)
   
    left, right = st.columns([1, 2], gap="large")

    with left:
        st.markdown("### 🎛️ Customize Your Distribution")
        mu = st.slider("Mean (μ) — The Average", min_value=0.0, max_value=100.0, value=70.0, step=1.0)
        sigma = st.slider("Std Deviation (σ) — The Spread", min_value=1.0, max_value=30.0, value=10.0, step=1.0)
       
        st.markdown("### 🎯 Pick Your Data Point")
        x_val = st.slider("Data Point (x)", min_value=mu - 4*sigma, max_value=mu + 4*sigma, value=mu + 1.5*sigma, step=0.1)
       
        # Calculate Z-score
        z_score = (x_val - mu) / sigma
       
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="stat-card" style="border-top-color: #34d399;">
            <div class="stat-label" style="color: #34d399;">Calculated Z-Score</div>
            <div class="stat-val" style="color: #10b981;">{z_score:.2f}</div>
            <div style="color: #cbd5e1; font-size: 0.9rem; margin-top: 10px;">
                Your point is exactly <strong>{abs(z_score):.2f} standard deviations</strong>
                {'above' if z_score >= 0 else 'below'} the mean.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        # Create tabs for Raw vs Standardized
        tab1, tab2 = st.tabs(["🌎 Raw Distribution (Real World)", "🔬 Standardized (Z-Score World)"])
       
        with tab1:
            # Raw Distribution Plot
            x_raw = np.linspace(mu - 4*sigma, mu + 4*sigma, 500)
            y_raw = norm.pdf(x_raw, mu, sigma)
           
            fig_raw = go.Figure()
           
            # The Bell Curve
            fig_raw.add_trace(go.Scatter(
                x=x_raw, y=y_raw, mode='lines', line=dict(color='#6366f1', width=3), name='Distribution'
            ))
           
            # Fill Area up to x_val to show percentile
            x_fill = x_raw[x_raw <= x_val]
            y_fill = y_raw[x_raw <= x_val]
            fig_raw.add_trace(go.Scatter(
                x=np.concatenate([x_fill, [x_val, x_raw[0]]]),
                y=np.concatenate([y_fill, [0, 0]]),
                fill='toself', fillcolor='rgba(99, 102, 241, 0.2)', line=dict(color='rgba(255,255,255,0)'),
                name=f'Percentile Area'
            ))
           
            # Mean Line
            fig_raw.add_vline(x=mu, line_dash="dash", line_color="#94a3b8", line_width=2, annotation_text="Mean (μ)", annotation_position="top right")
           
            # Data Point Line
            fig_raw.add_vline(x=x_val, line_color="#10b981", line_width=3)
            fig_raw.add_annotation(
                x=x_val, y=max(y_raw)*0.5,
                text=f"x = {x_val:.1f}", showarrow=True, arrowhead=2, ax=50 if x_val > mu else -50, ay=0,
                font=dict(color="#10b981", size=14, family="sans-serif")
            )
           
            # Draw Sigma Ruler arrows
            current_x = mu
            step = sigma if x_val > mu else -sigma
            num_full_steps = int(abs((x_val - mu) / sigma))
           
            for i in range(num_full_steps):
                fig_raw.add_annotation(
                    x=current_x + step/2, y=max(y_raw)*0.1,
                    text="1σ", showarrow=False, font=dict(color="#f8fafc", size=12)
                )
                fig_raw.add_shape(
                    type="line", x0=current_x, y0=max(y_raw)*0.08, x1=current_x+step, y1=max(y_raw)*0.08,
                    line=dict(color="#f8fafc", width=2), opacity=0.5
                )
                fig_raw.add_shape(type="line", x0=current_x, y0=max(y_raw)*0.07, x1=current_x, y1=max(y_raw)*0.09, line=dict(color="#f8fafc", width=2), opacity=0.5)
                current_x += step
               
            # Remaining fraction
            if abs(x_val - current_x) > 0.01:
                fig_raw.add_shape(
                    type="line", x0=current_x, y0=max(y_raw)*0.08, x1=x_val, y1=max(y_raw)*0.08,
                    line=dict(color="#f8fafc", width=2), opacity=0.5
                )
                fig_raw.add_shape(type="line", x0=current_x, y0=max(y_raw)*0.07, x1=current_x, y1=max(y_raw)*0.09, line=dict(color="#f8fafc", width=2), opacity=0.5)
                fig_raw.add_shape(type="line", x0=x_val, y0=max(y_raw)*0.07, x1=x_val, y1=max(y_raw)*0.09, line=dict(color="#f8fafc", width=2), opacity=0.5)

            fig_raw.update_layout(
                title="The Raw Data",
                xaxis=dict(title="Original Value (x)", gridcolor='rgba(51,65,85,0.4)'),
                yaxis=dict(title="Density", gridcolor='rgba(51,65,85,0.4)'),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#f8fafc'), margin=dict(t=40, b=40), height=400, showlegend=False
            )
            st.plotly_chart(fig_raw, use_container_width=True)
           
        with tab2:
            # Standardized Plot
            x_std = np.linspace(-4, 4, 500)
            y_std = norm.pdf(x_std, 0, 1)
           
            fig_std = go.Figure()
           
            fig_std.add_trace(go.Scatter(
                x=x_std, y=y_std, mode='lines', line=dict(color='#ec4899', width=3), name='Standard Normal'
            ))
           
            # Fill Area
            x_fill_std = x_std[x_std <= z_score]
            y_fill_std = y_std[x_std <= z_score]
            fig_std.add_trace(go.Scatter(
                x=np.concatenate([x_fill_std, [z_score, x_std[0]]]),
                y=np.concatenate([y_fill_std, [0, 0]]),
                fill='toself', fillcolor='rgba(236, 72, 153, 0.2)', line=dict(color='rgba(255,255,255,0)')
            ))
           
            # Mean Line (0)
            fig_std.add_vline(x=0, line_dash="dash", line_color="#94a3b8", line_width=2, annotation_text="μ = 0", annotation_position="top right")
           
            # Data Point Line (Z-Score)
            fig_std.add_vline(x=z_score, line_color="#34d399", line_width=3)
            fig_std.add_annotation(
                x=z_score, y=max(y_std)*0.5,
                text=f"z = {z_score:.2f}", showarrow=True, arrowhead=2, ax=50 if z_score > 0 else -50, ay=0,
                font=dict(color="#34d399", size=14, family="sans-serif")
            )
           
            # Ruler marks
            for i in range(-3, 4):
                fig_std.add_annotation(x=i, y=-0.02, text=str(i), showarrow=False, font=dict(color="#94a3b8", size=12))
               
            fig_std.update_layout(
                title="Standard Normal Distribution",
                xaxis=dict(title="Z-Score (Standard Deviations from Mean)", gridcolor='rgba(51,65,85,0.4)', range=[-4, 4]),
                yaxis=dict(title="Density", gridcolor='rgba(51,65,85,0.4)'),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#f8fafc'), margin=dict(t=40, b=40), height=400, showlegend=False
            )
            st.plotly_chart(fig_std, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    <p>
    <strong>Notice the trick?</strong><br>
    The shape of the shaded area is <strong>exactly the same</strong> in both graphs. Standardization doesn't change the underlying probability or distribution shape; it simply shifts the center to 0 and scales the width to 1. It gives us a universal coordinate system!
    </p>
    </div>
    """, unsafe_allow_html=True)


def render_math_breakdown():
    st.markdown('<div class="section-header">🧮 The Formula: Shift & Scale</div>', unsafe_allow_html=True)
   
    st.markdown("The Z-score formula performs two geometric operations on our data:")
   
    st.latex(r"Z = \frac{x - \mu}{\sigma}")
   
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(r"""
        <div class="stat-card" style="border-top-color:#f59e0b;">
            <div class="stat-label" style="color:#f59e0b;">Step 1: Shift (Center to 0)</div>
            <div style="font-size:1.8rem; margin:10px 0; color:#f8fafc;"><i>Numerator: (x - μ)</i></div>
            <div style="color:#cbd5e1; font-size:0.95rem; text-align: left;">
                By subtracting the mean from our data point, we calculate the absolute distance. If everyone does this, the new mean becomes exactly 0.
                <br><br><strong>Geometric View:</strong> We slide the entire bell curve left or right until its peak rests perfectly on the y-axis.
            </div>
        </div>""", unsafe_allow_html=True)
       
    with c2:
        st.markdown(r"""
        <div class="stat-card" style="border-top-color:#0ea5e9;">
            <div class="stat-label" style="color:#0ea5e9;">Step 2: Scale (Standardize Spread)</div>
            <div style="font-size:1.8rem; margin:10px 0; color:#f8fafc;"><i>Denominator: ÷ σ</i></div>
            <div style="color:#cbd5e1; font-size:0.95rem; text-align: left;">
                By dividing by the standard deviation, we are changing our unit of measurement. Instead of measuring in "points" or "meters," we measure in "standard deviations."
                <br><br><strong>Geometric View:</strong> We pinch or stretch the bell curve until its standard deviation is exactly 1 unit wide.
            </div>
        </div>""", unsafe_allow_html=True)

def render_ai_context():
    st.markdown('<div class="section-header">🤖 Why does AI care about Standardization?</div>', unsafe_allow_html=True)
   
    cols = st.columns(3)
    examples = [
        ("⚖️ Feature Scaling", "#8b5cf6",
         "Imagine predicting house prices based on Square Footage (1000s) and Number of Bedrooms (1 to 5). Without standardization, the huge numbers of Square Footage will overpower the tiny Bedroom numbers. Z-scores put all features on a level playing field!"),
        ("⚡ Faster Gradient Descent", "#ef4444",
         "When features are on vastly different scales, the loss landscape becomes a long, skinny valley. Gradient descent bounces back and forth, learning slowly. Standardized data creates a nice round bowl shape, allowing the model to slide directly to the minimum!"),
        ("🧠 Activation Functions", "#14b8a6",
         "Many activation functions (like Sigmoid or Tanh) 'saturate' and stop learning if inputs are too large or too small. Keeping inputs centered around 0 with a variance of 1 ensures the neurons stay in their active, learning 'sweet spot'.")
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
    render_interactive_ruler()
   
    st.divider()
    render_math_breakdown()
   
    st.divider()
    render_ai_context()

if __name__ == "__main__":
    main()
