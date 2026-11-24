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
        color: #c7d2fe;
        margin: 0 0 16px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

def format_percent(p: float) -> str:
    if p > 99.99:
        return ">99.99%"
    if p < 0.01:
        return "<0.01%"
    return f"{p:.2f}%" if (p > 99.0 or p < 1.0) else f"{p:.1f}%"


def curve_points(lo: float, hi: float, width: float) -> int:
    # Keep ~100 samples per σ so the bell stays smooth when the axis is stretched far out.
    return int(np.clip((hi - lo) / width * 100, 500, 20000))


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
    Explore how a data point relates to the average by adjusting the distribution parameters below.
    For example, imagine a test with average score μ = 70 and standard deviation σ = 10, where you scored x = 85.
    Watch how the Z-score and step-by-step calculations respond in real-time as you move each slider!
    """)
   
    left, right = st.columns([1, 2], gap="large")

    with left:
        st.markdown("### 🎛️ Customize Your Distribution")
        mu = st.slider("Mean (μ) — The Average", min_value=0.0, max_value=100.0, value=70.0, step=1.0, key="p35_mean")
        sigma = st.slider("Std Deviation (σ) — The Spread", min_value=1.0, max_value=30.0, value=10.0, step=1.0, key="p35_sigma")
       
        st.markdown("### 🎯 Pick Your Data Point")
        x_val = st.slider("Data Point (x)", min_value=-20.0, max_value=160.0, value=85.0, step=0.5, key="p35_x_val")
       
        # Calculate Z-score
        diff = x_val - mu
        z_score = diff / sigma
        # Φ(z) is only a valid percentile if the data are (approximately) Normal.
        percentile = norm.cdf(z_score) * 100
        percentile_str = format_percent(percentile)
       
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="stat-card" style="border-top-color: #34d399;">
            <div class="stat-label" style="color: #34d399;">Step-by-Step Calculation</div>
            <div style="font-family: monospace; font-size: 1.05rem; color: #f8fafc; margin: 12px 0; background: rgba(15,23,42,0.7); padding: 10px 14px; border-radius: 8px; border: 1px solid rgba(52,211,153,0.3); text-align: left;">
                Z = (x - μ) / σ<br>
                Z = ({x_val:.1f} - {mu:.1f}) / {sigma:.1f}<br>
                Z = {diff:+.1f} / {sigma:.1f} = <strong style="color: #34d399;">{z_score:+.2f}</strong>
            </div>
            <div class="stat-label" style="color: #94a3b8;">Final Z-Score</div>
            <div class="stat-val" style="color: #10b981;">{z_score:+.2f}</div>
            <div style="color: #cbd5e1; font-size: 0.9rem; margin-top: 10px; line-height: 1.5;">
                Your point is <strong>{abs(z_score):.2f} standard deviations</strong>
                {'above' if z_score >= 0 else 'below'} the mean.<br>
                <span style="color: #94a3b8; font-size: 0.85rem;">Percentile <em>if the data are Normal</em>: <strong>{percentile_str}</strong> (≈ {percentile_str} of a Normal population lies below x)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        # Create tabs for Raw vs Standardized
        tab1, tab2 = st.tabs(["🌎 Raw Distribution (Real World)", "🔬 Standardized (Z-Score World)"])
       
        with tab1:
            # Raw Distribution Plot
            x_min_plot = min(mu - 4*sigma, x_val - 0.5*sigma)
            x_max_plot = max(mu + 4*sigma, x_val + 0.5*sigma)
            x_raw = np.linspace(x_min_plot, x_max_plot, curve_points(x_min_plot, x_max_plot, sigma))
            y_raw = norm.pdf(x_raw, mu, sigma)
           
            fig_raw = go.Figure()
           
            # The Bell Curve
            fig_raw.add_trace(go.Scatter(
                x=x_raw, y=y_raw, mode='lines', line=dict(color='#6366f1', width=3), name='Distribution'
            ))
           
            # Fill Area up to x_val to show percentile
            x_fill = x_raw[x_raw <= x_val]
            y_fill = y_raw[x_raw <= x_val]
            if len(x_fill) > 0:
                fig_raw.add_trace(go.Scatter(
                    x=np.concatenate([x_fill, [x_val, x_fill[0]]]),
                    y=np.concatenate([y_fill, [0, 0]]),
                    fill='toself', fillcolor='rgba(99, 102, 241, 0.2)', line=dict(color='rgba(255,255,255,0)'),
                    name='Percentile Area'
                ))
           
            # Mean Line
            fig_raw.add_vline(x=mu, line_dash="dash", line_color="#94a3b8", line_width=2, annotation_text="Mean (μ)", annotation_position="top right")
           
            # Data Point Line
            fig_raw.add_vline(x=x_val, line_color="#10b981", line_width=3)
            fig_raw.add_annotation(
                x=x_val, y=max(y_raw)*0.5,
                text=f"x = {x_val:.1f}", showarrow=True, arrowhead=2, ax=50 if x_val >= mu else -50, ay=0,
                font=dict(color="#10b981", size=14, family="sans-serif")
            )
           
            # Draw Sigma Ruler arrows
            current_x = mu
            step = sigma if x_val >= mu else -sigma
            num_full_steps = min(int(abs((x_val - mu) / sigma)), 6)
           
            for _ in range(num_full_steps):
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
            if abs(x_val - current_x) > 0.01 and num_full_steps < 6:
                fig_raw.add_shape(
                    type="line", x0=current_x, y0=max(y_raw)*0.08, x1=x_val, y1=max(y_raw)*0.08,
                    line=dict(color="#f8fafc", width=2), opacity=0.5
                )
                fig_raw.add_shape(type="line", x0=current_x, y0=max(y_raw)*0.07, x1=current_x, y1=max(y_raw)*0.09, line=dict(color="#f8fafc", width=2), opacity=0.5)
                fig_raw.add_shape(type="line", x0=x_val, y0=max(y_raw)*0.07, x1=x_val, y1=max(y_raw)*0.09, line=dict(color="#f8fafc", width=2), opacity=0.5)
            elif num_full_steps == 6 and abs(z_score) > 6:
                fig_raw.add_annotation(
                    x=current_x, y=max(y_raw)*0.16,
                    text=f"… ruler stops at 6σ (x is {abs(z_score):.1f}σ away)", showarrow=False,
                    xanchor="left" if step > 0 else "right", font=dict(color="#fbbf24", size=12)
                )
            fig_raw.update_layout(
                title=f"The Raw Data (μ = {mu:.1f}, σ = {sigma:.1f}, x = {x_val:.1f})",
                xaxis=dict(title="Original Value (x)", gridcolor='rgba(51,65,85,0.4)'),
                yaxis=dict(title="Density", gridcolor='rgba(51,65,85,0.4)'),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#f8fafc'), margin=dict(t=40, b=40), height=400, showlegend=False
            )
            st.plotly_chart(fig_raw, width="stretch")
           
        with tab2:
            # Standardized Plot
            z_min_plot = min(-4.0, z_score - 0.5)
            z_max_plot = max(4.0, z_score + 0.5)
            x_std = np.linspace(z_min_plot, z_max_plot, curve_points(z_min_plot, z_max_plot, 1.0))
            y_std = norm.pdf(x_std, 0, 1)
           
            fig_std = go.Figure()
           
            fig_std.add_trace(go.Scatter(
                x=x_std, y=y_std, mode='lines', line=dict(color='#ec4899', width=3), name='Standard Normal'
            ))
           
            # Fill Area
            x_fill_std = x_std[x_std <= z_score]
            y_fill_std = y_std[x_std <= z_score]
            if len(x_fill_std) > 0:
                fig_std.add_trace(go.Scatter(
                    x=np.concatenate([x_fill_std, [z_score, x_fill_std[0]]]),
                    y=np.concatenate([y_fill_std, [0, 0]]),
                    fill='toself', fillcolor='rgba(236, 72, 153, 0.2)', line=dict(color='rgba(255,255,255,0)')
                ))
           
            # Mean Line (0)
            fig_std.add_vline(x=0, line_dash="dash", line_color="#94a3b8", line_width=2, annotation_text="μ = 0", annotation_position="top right")
           
            # Data Point Line (Z-Score)
            fig_std.add_vline(x=z_score, line_color="#34d399", line_width=3)
            fig_std.add_annotation(
                x=z_score, y=max(y_std)*0.5,
                text=f"z = {z_score:+.2f}", showarrow=True, arrowhead=2, ax=50 if z_score >= 0 else -50, ay=0,
                font=dict(color="#34d399", size=14, family="sans-serif")
            )
           
            # Integer z ticks (one per σ) while the axis is short enough to stay readable
            z_dtick = 1 if (z_max_plot - z_min_plot) <= 16 else None
               
            fig_std.update_layout(
                title=f"Standard Normal Distribution (Z = {z_score:+.2f})",
                xaxis=dict(title="Z-Score (Standard Deviations from Mean)", gridcolor='rgba(51,65,85,0.4)', range=[z_min_plot, z_max_plot], dtick=z_dtick),
                yaxis=dict(title="Density", gridcolor='rgba(51,65,85,0.4)'),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#f8fafc'), margin=dict(t=40, b=40), height=400, showlegend=False
            )
            st.plotly_chart(fig_std, width="stretch")

    st.markdown("""
    <div class="insight-box">
    <p>
    <strong>Notice the trick?</strong><br>
    The shape of the shaded area is <strong>exactly the same</strong> in both graphs. Standardization doesn't change the underlying probability or distribution shape; it simply shifts the center to 0 and scales the width to 1. It gives us a universal coordinate system!<br><br>
    <strong>Caveat:</strong> a Z-score can be computed for <em>any</em> data, but reading it as a percentile with the bell-curve area Φ(z) is only valid when the data are (approximately) <strong>Normal</strong>. Standardizing skewed data keeps it skewed — it does not make it Normal.
    </p>
    </div>
    """, unsafe_allow_html=True)
    return x_val, mu, sigma, z_score


def render_math_breakdown(x_val: float, mu: float, sigma: float, z_score: float):
    diff = x_val - mu
    st.markdown('<div class="section-header">🧮 The Formula: Shift & Scale</div>', unsafe_allow_html=True)
   
    st.markdown("The Z-score formula performs two geometric operations on our data:")
   
    st.latex(rf"Z = \frac{{x - \mu}}{{\sigma}} = \frac{{{x_val:.1f} - {mu:.1f}}}{{{sigma:.1f}}} = \frac{{{diff:+.1f}}}{{{sigma:.1f}}} = \mathbf{{{z_score:+.2f}}}")
   
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="stat-card" style="border-top-color:#f59e0b;">
            <div class="stat-label" style="color:#f59e0b;">Step 1: Shift (Center to 0)</div>
            <div style="font-size:1.5rem; margin:8px 0; color:#f8fafc;"><i>Numerator: (x - μ)</i></div>
            <div style="background: rgba(15,23,42,0.7); padding: 8px 12px; border-radius: 8px; font-family: monospace; font-size: 1.05rem; color: #fbbf24; margin: 10px 0; border: 1px solid rgba(245,158,11,0.3);">
                {x_val:.1f} - {mu:.1f} = <strong>{diff:+.1f}</strong>
            </div>
            <div style="color:#cbd5e1; font-size:0.95rem; text-align: left; line-height: 1.6;">
                By subtracting the mean ({mu:.1f}) from our data point ({x_val:.1f}), we calculate the signed distance ({diff:+.1f}). If everyone does this, the new mean becomes exactly 0.
                <br><br><strong>Geometric View:</strong> We slide the entire bell curve horizontally until its peak rests perfectly on the y-axis (center 0).
            </div>
        </div>""", unsafe_allow_html=True)
       
    with c2:
        st.markdown(f"""
        <div class="stat-card" style="border-top-color:#0ea5e9;">
            <div class="stat-label" style="color:#0ea5e9;">Step 2: Scale (Standardize Spread)</div>
            <div style="font-size:1.5rem; margin:8px 0; color:#f8fafc;"><i>Denominator: ÷ σ</i></div>
            <div style="background: rgba(15,23,42,0.7); padding: 8px 12px; border-radius: 8px; font-family: monospace; font-size: 1.05rem; color: #38bdf8; margin: 10px 0; border: 1px solid rgba(14,165,233,0.3);">
                {diff:+.1f} ÷ {sigma:.1f} = <strong>{z_score:+.2f}</strong>
            </div>
            <div style="color:#cbd5e1; font-size:0.95rem; text-align: left; line-height: 1.6;">
                By dividing by the standard deviation ({sigma:.1f}), we change our unit of measurement. Instead of measuring in raw units, we measure in "standard deviations".
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
         "When features are on vastly different scales, the loss landscape becomes a long, skinny valley. Gradient descent bounces back and forth, learning slowly. Standardized features give a much rounder bowl (correlated features can still leave it somewhat tilted), so the model can head far more directly to the minimum!"),
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
    x_val, mu, sigma, z_score = render_interactive_ruler()
   
    st.divider()
    render_math_breakdown(x_val, mu, sigma, z_score)
   
    st.divider()
    render_ai_context()

if __name__ == "__main__":
    main()
