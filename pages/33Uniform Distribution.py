import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

st.set_page_config(page_title="Uniform Distribution", layout="wide", initial_sidebar_state="expanded")

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
        background: linear-gradient(90deg, #6ee7b7, #34d399, #10b981);
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
        color: #6ee7b7;
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
        background: linear-gradient(135deg, #0f172a, #064e3b);
        border: 1px solid #059669;
        border-radius: 14px;
        padding: 20px 24px;
        margin: 8px 0;
        border-left: 4px solid #10b981;
    }
    .insight-box p { color: #e2e8f0; margin: 0; line-height: 1.7; }

    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #e2e8f0;
        margin: 0 0 16px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .die-container {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        justify-content: center;
        padding: 20px;
        background: #0f172a;
        border-radius: 20px;
        border: 1px solid #1e293b;
    }
    .die-face {
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, #34d399, #10b981);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        font-weight: 900;
        color: #022c22;
        box-shadow: inset 0px 4px 10px rgba(255,255,255,0.4), 0 8px 20px rgba(0,0,0,0.4);
        transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .die-face:hover {
        transform: scale(1.1) rotate(5deg);
    }

    .spinner-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 40px;
        background: #0f172a;
        border-radius: 20px;
        border: 1px solid #1e293b;
        position: relative;
    }
    .spinner-wheel {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        background: conic-gradient(#10b981, #3b82f6, #8b5cf6, #f43f5e, #f59e0b, #10b981);
        box-shadow: 0 0 30px rgba(16, 185, 129, 0.4);
        animation: spin 10s linear infinite;
        position: relative;
    }
    .spinner-center {
        position: absolute;
        width: 40px;
        height: 40px;
        background: #0f172a;
        border-radius: 50%;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        border: 3px solid #cbd5e1;
        z-index: 2;
    }
    .spinner-pointer {
        position: absolute;
        top: 0px;
        left: 50%;
        transform: translateX(-50%);
        width: 0;
        height: 0;
        border-left: 15px solid transparent;
        border-right: 15px solid transparent;
        border-top: 30px solid #f8fafc;
        z-index: 3;
        filter: drop-shadow(0 4px 4px rgba(0,0,0,0.5));
    }
    @keyframes spin {
        100% { transform: rotate(360deg); }
    }
    </style>
    """, unsafe_allow_html=True)

def render_hero():
    st.markdown("""
    <div class="hero-box">
        <div class="hero-title">📏 Page 33: The Uniform Distribution</div>
        <div class="hero-sub">
            The baseline of all randomness. <strong>Every equal-sized interval is equally likely.</strong>
            Before we introduce complex curves, bell shapes, and biases, we start here.
            Whether you're rolling a perfectly fair die or picking a random number between A and B,
            each discrete outcome or equal-width interval has the same probability.
            <br><br>
            It's the ultimate state of <strong>maximum uncertainty</strong> when you know the boundaries but nothing else.
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_discrete_section(n):
    st.markdown('<div class="section-header">🎲 Discrete Uniform: The Perfect Die</div>', unsafe_allow_html=True)
    st.markdown(f"Imagine a perfect, symmetrical die with **{n}** sides. Rolling any number from 1 to {n} has the exact same probability.")
   
    st.latex(r"P(X = x) = \frac{1}{n} \quad \text{for } x \in \{1, 2, \dots, n\}")

    # Visual die faces
    faces_html = "".join([f'<div class="die-face">{i}</div>' for i in range(1, n+1)])
    st.markdown(f'<div class="die-container">{faces_html}</div>', unsafe_allow_html=True)
   
    # Math & Chart
    prob = 1 / n
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=list(range(1, n+1)),
        y=[prob]*n,
        name=f"P(X=x) = 1/{n}",
        marker=dict(
            color='rgba(16, 185, 129, 0.85)',
            line=dict(color='#34d399', width=2)
        ),
        text=[f"1/{n}"]*n,
        textposition="outside",
        textfont=dict(color="#6ee7b7", size=14)
    ))
    fig.update_layout(
        title="Probability Mass Function (PMF)",
        xaxis=dict(title="Outcome (x)", tickmode='linear', tick0=1, dtick=1, gridcolor='rgba(51,65,85,0.4)', title_font=dict(color="#cbd5e1")),
        yaxis=dict(title="Probability P(x)", range=[0, prob*1.5], gridcolor='rgba(51,65,85,0.4)', title_font=dict(color="#cbd5e1")),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f8fafc', family="Inter"),
        height=350,
        margin=dict(l=20, r=20, t=50, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Stats
    mean = (n + 1) / 2
    variance = (n**2 - 1) / 12
    std_dev = np.sqrt(variance)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-val">{mean:.2f}</div>
            <div class="stat-label">Expected Value (Mean)</div>
            <div class="stat-formula">E[X] = (a+b)/2</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="stat-card" style="border-top-color:#3b82f6;">
            <div class="stat-val" style="color:#60a5fa;">{variance:.2f}</div>
            <div class="stat-label">Variance</div>
            <div class="stat-formula">Var(X) = (n²-1)/12</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="stat-card" style="border-top-color:#f43f5e;">
            <div class="stat-val" style="color:#fb7185;">{std_dev:.2f}</div>
            <div class="stat-label">Std Deviation</div>
            <div class="stat-formula">σ = √Var(X)</div>
        </div>""", unsafe_allow_html=True)

def render_continuous_section(a, b):
    st.markdown('<div class="section-header">🌀 Continuous Uniform: The Infinite Spinner</div>', unsafe_allow_html=True)
    st.markdown(f"Imagine a spinner that can land on **any real number** between **{a}** and **{b}**. It doesn't just hit integers; it could be {a + 0.12345:.5f} or {b - 0.98765:.5f}. There are infinite possibilities.")
   
    st.latex(r"f(x) = \begin{cases} \frac{1}{b - a} & \text{for } a \le x \le b \\ 0 & \text{otherwise} \end{cases}")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("""
        <div class="spinner-container">
            <div class="spinner-pointer"></div>
            <div class="spinner-wheel">
                <div class="spinner-center"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("The spinner wheel stops uniformly anywhere in the 360° circle.")
   
    with col2:
        # Chart
        height = 1 / (b - a)
       
        # We need a small pad for x axis
        pad = (b - a) * 0.2
        x_vals = np.linspace(a - pad, b + pad, 500)
        y_vals = np.where((x_vals >= a) & (x_vals <= b), height, 0)
       
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            fill='tozeroy',
            fillcolor='rgba(59, 130, 246, 0.4)',
            mode='lines',
            line=dict(color='#3b82f6', width=3),
            name=f"PDF f(x) = 1/({b}-{a})"
        ))
       
        # Add dashed lines for boundaries
        fig.add_vline(x=a, line_dash="dash", line_color="#94a3b8")
        fig.add_vline(x=b, line_dash="dash", line_color="#94a3b8")
       
        fig.update_layout(
            title="Probability Density Function (PDF) — The Rectangle",
            xaxis=dict(title="Continuous Value (x)", range=[a-pad, b+pad], gridcolor='rgba(51,65,85,0.4)', title_font=dict(color="#cbd5e1")),
            yaxis=dict(title="Density f(x)", range=[0, height*1.5], gridcolor='rgba(51,65,85,0.4)', title_font=dict(color="#cbd5e1")),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f8fafc', family="Inter"),
            height=300,
            margin=dict(l=20, r=20, t=50, b=40),
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)

    # Stats
    mean = (a + b) / 2
    variance = ((b - a)**2) / 12
    std_dev = np.sqrt(variance)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-val">{mean:.2f}</div>
            <div class="stat-label">Expected Value (Mean)</div>
            <div class="stat-formula">E[X] = (a+b)/2</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="stat-card" style="border-top-color:#3b82f6;">
            <div class="stat-val" style="color:#60a5fa;">{variance:.2f}</div>
            <div class="stat-label">Variance</div>
            <div class="stat-formula">Var(X) = (b-a)²/12</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="stat-card" style="border-top-color:#f43f5e;">
            <div class="stat-val" style="color:#fb7185;">{std_dev:.2f}</div>
            <div class="stat-label">Std Deviation</div>
            <div class="stat-formula">σ = (b-a)/√12</div>
        </div>""", unsafe_allow_html=True)
       
    st.markdown("""
    <div class="insight-box">
    <p>🔑 <strong>Why is the height 1/(b-a)?</strong> In continuous probability, the total area under the PDF curve must equal 1 (representing 100% probability). The area of a rectangle is width × height. Since the width is (b-a), the height must be 1/(b-a) so that (b-a) * 1/(b-a) = 1.</p>
    </div>
    """, unsafe_allow_html=True)

def render_simulation(mode, a, b, n):
    st.markdown('<div class="section-header">🛠️ Law of Large Numbers Simulation</div>', unsafe_allow_html=True)
    st.markdown("Let's draw random samples. Watch how the histogram starts chunky and random, but slowly forms the perfect flat uniform rectangle as we pull more samples.")
   
    n_samples = st.select_slider(
        "Number of Samples to Draw",
        options=[10, 50, 100, 500, 1000, 5000, 10000, 50000],
        value=500
    )
   
    if st.button("🚀 Draw Samples!", use_container_width=True):
        if mode.startswith("Discrete"):
            samples = np.random.default_rng().integers(1, n + 1, n_samples)
            fig = go.Figure()
            # Count frequencies
            unique, counts = np.unique(samples, return_counts=True)
            freqs = counts / n_samples
           
            # Map all possible faces so missing ones show as 0
            full_freqs = []
            for i in range(1, n+1):
                if i in unique:
                    idx = np.where(unique == i)[0][0]
                    full_freqs.append(freqs[idx])
                else:
                    full_freqs.append(0)
                   
            fig.add_trace(go.Bar(
                x=list(range(1, n+1)),
                y=full_freqs,
                name="Observed Frequency",
                marker_color='rgba(16, 185, 129, 0.7)',
                marker_line_color='#34d399',
                marker_line_width=1
            ))
            fig.add_hline(y=1/n, line_dash="dash", line_color="#ef4444", annotation_text=f"True Prob (1/{n})")
           
            fig.update_layout(
                title=f"Discrete Empirical Distribution ({n_samples} rolls)",
                xaxis_title="Outcome",
                yaxis_title="Relative Frequency",
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#f8fafc'),
                xaxis=dict(tickmode='linear', dtick=1)
            )
            st.plotly_chart(fig, use_container_width=True)
           
        else:
            samples = np.random.default_rng().uniform(a, b, n_samples)
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=samples,
                histnorm='probability density',
                name="Observed Density",
                marker_color='rgba(59, 130, 246, 0.7)',
                marker_line_color='#60a5fa',
                marker_line_width=1,
                nbinsx=30
            ))
            fig.add_shape(type="rect", x0=a, y0=0, x1=b, y1=1/(b-a), line=dict(color="#ef4444", width=2, dash="dash"), fillcolor="rgba(0,0,0,0)")
            fig.add_annotation(x=(a+b)/2, y=1/(b-a), text=f"True Density (1/{b-a})", showarrow=False, yshift=15, font=dict(color="#ef4444"))
           
            fig.update_layout(
                title=f"Continuous Empirical Distribution ({n_samples} draws)",
                xaxis_title="Value",
                yaxis_title="Density",
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#f8fafc'),
                bargap=0.05
            )
            st.plotly_chart(fig, use_container_width=True)

def render_ai_connection():
    st.markdown('<div class="section-header">🤖 Why Does AI Care About This?</div>', unsafe_allow_html=True)
   
    cols = st.columns(3)
    examples = [
        ("🎲 Weight Initialization", "#10b981",
         "When a neural network starts, its weights are often initialized using a uniform distribution (e.g., <strong>Xavier/Glorot Uniform</strong> or <strong>He Uniform</strong>) to break symmetry without favoring any specific value."),
        ("🔍 Random Search for Hyperparameters", "#3b82f6",
         "When tuning models, picking learning rates or dropout rates uniformly at random from a range is often more efficient than a rigid grid search."),
        ("🛡️ Noise Injection & Augmentation", "#f59e0b",
         "Adding uniform random noise to images or audio during training makes models more robust to small, unexpected variations.")
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

    st.sidebar.markdown("## ⚙️ Uniform Settings")
    mode = st.sidebar.radio("Distribution Type", ["Discrete (Dice/Coins)", "Continuous (Ranges)"])
   
    st.sidebar.markdown("---")
    if mode.startswith("Discrete"):
        st.sidebar.markdown("**Discrete Parameters**")
        n = st.sidebar.slider("Number of Outcomes (N)", min_value=2, max_value=20, value=6, step=1, help="Like an N-sided die. Outcomes will be 1 to N.")
       
        st.sidebar.markdown("""
        **Formulas:**
        ```
        X ~ U{1, n}
        P(X=x) = 1/n
        E[X] = (n+1)/2
        Var(X) = (n²-1)/12
        ```
        """)
       
        render_discrete_section(n)
        st.divider()
        render_simulation(mode, 0, 0, n)
       
    else:
        st.sidebar.markdown("**Continuous Parameters**")
        a = st.sidebar.number_input("Minimum Boundary (a)", value=0.0, step=1.0)
        b = st.sidebar.number_input("Maximum Boundary (b)", value=10.0, step=1.0)
       
        if a >= b:
            st.sidebar.error("Error: Minimum boundary 'a' must be less than maximum boundary 'b'.")
            st.stop()
           
        st.sidebar.markdown("""
        **Formulas:**
        ```
        X ~ U(a, b)
        f(x) = 1/(b-a)
        E[X] = (a+b)/2
        Var(X) = (b-a)²/12
        ```
        """)
       
        render_continuous_section(a, b)
        st.divider()
        render_simulation(mode, a, b, 0)

    st.divider()
    render_ai_connection()
   
    st.divider()
    st.info("💡 **Takeaway:** The Uniform distribution represents total neutrality. It is the starting point of probability, ensuring fairness before any specific bias, clustering, or trend is learned by a model.")

if __name__ == "__main__":
    main()
