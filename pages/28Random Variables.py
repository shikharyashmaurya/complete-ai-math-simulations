import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import binom, norm

st.set_page_config(page_title="Random Variables", layout="wide")

def local_css():
    st.markdown("""
    <style>
    .narrative-box {
        background: #1e293b;
        color: #f8fafc;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #8b5cf6;
        margin-bottom: 20px;
        font-size: 1.1rem;
    }
    .narrative-box h3 {
        color: #ffffff !important;
        margin-top: 0;
    }
    .concept-box {
        background: #0f172a;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #334155;
        height: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

def render_intro():
    st.title("Page 28: Random Variables (Discrete vs Continuous)")
    st.markdown(
        """
        <div class="narrative-box">
        <h3>Counting vs. Measuring 📏</h3>
        A <b>Random Variable</b> is just a way to map the outcome of a random event to a number. <br><br>
        But there are two fundamentally different types of numbers we care about in math:<br>
        1. <b>Discrete:</b> Things you can count (like the number of heads in 10 coin flips). You can't have 2.5 heads.<br>
        2. <b>Continuous:</b> Things you can measure (like a person's exact height). You can be 170 cm, 170.5 cm, or 170.539... cm.<br><br>
        Let's explore the difference, and see how the two worlds connect.
        </div>
        """, unsafe_allow_html=True
    )

def render_discrete():
    st.header("1️⃣ Discrete: The World of Counting")
    st.markdown("In a discrete world, outcomes fall into distinct 'buckets'. Let's flip some coins. The random variable is the **number of heads**.")
   
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("<div class='concept-box'>", unsafe_allow_html=True)
        n_coins = st.slider("Number of Coins", min_value=1, max_value=50, value=10)
        p_heads = st.slider("Probability of Heads", min_value=0.0, max_value=1.0, value=0.5, step=0.05)
        st.markdown("<br><small>Notice how the x-axis only has whole numbers. There is no such thing as getting 3.4 heads!</small>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
       
    with col2:
        x = np.arange(0, n_coins + 1)
        y = binom.pmf(x, n_coins, p_heads)
       
        fig = go.Figure(data=[go.Bar(x=x, y=y, marker_color='#8b5cf6', opacity=0.8)])
        fig.update_layout(
            title=f"Probability of getting X heads (Flipping {n_coins} coins)",
            xaxis_title="Number of Heads (X)",
            yaxis_title="Probability P(X)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f8fafc'),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        fig.update_xaxes(tickmode='linear', tick0=0, dtick=max(1, n_coins//10), gridcolor='#334155')
        fig.update_yaxes(gridcolor='#334155')
        st.plotly_chart(fig, use_container_width=True)

def render_continuous():
    st.header("2️⃣ Continuous: The World of Measuring")
    st.markdown("In a continuous world, outcomes can be *any* value within a range. The probability of getting *exactly* a specific number (like 170.0000000 cm) is essentially zero. Instead, we look at the probability of falling within a range (an area under the curve).")
   
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("<div class='concept-box'>", unsafe_allow_html=True)
        mu = st.slider("Average Height (cm)", min_value=150.0, max_value=190.0, value=170.0)
        sigma = st.slider("Spread (Standard Deviation)", min_value=2.0, max_value=20.0, value=7.0)
        st.markdown("<br><small>Notice how the x-axis is a smooth line. A person's height could be absolutely any value.</small>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
       
    with col2:
        x = np.linspace(130, 210, 500)
        y = norm.pdf(x, mu, sigma)
       
        fig = go.Figure(data=[go.Scatter(x=x, y=y, fill='tozeroy', mode='lines', line=dict(color='#10b981', width=3))])
        fig.update_layout(
            title="Distribution of Human Heights",
            xaxis_title="Height (cm)",
            yaxis_title="Probability Density",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f8fafc'),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        fig.update_xaxes(gridcolor='#334155')
        fig.update_yaxes(gridcolor='#334155')
        st.plotly_chart(fig, use_container_width=True)

def render_bridge():
    st.header("3️⃣ The Bridge: From Counting to Measuring")
    st.markdown("What happens if we take a discrete measurement (like grouping people by height) and make the buckets smaller and smaller? The discrete histogram morphs into the continuous density curve!")
   
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("<div class='concept-box'>", unsafe_allow_html=True)
        bins = st.select_slider(
            "Measurement Precision (Bucket Size)",
            options=["10 cm (Nearest 10cm)", "5 cm", "2 cm", "1 cm", "0.1 cm (Continuous)"],
            value="10 cm (Nearest 10cm)"
        )
       
        bin_mapping = {
            "10 cm (Nearest 10cm)": 10,
            "5 cm": 5,
            "2 cm": 2,
            "1 cm": 1,
            "0.1 cm (Continuous)": 0.1
        }
        bin_width = bin_mapping[bins]
        st.markdown(f"**Current Bucket Width:** {bin_width} cm")
        st.markdown("Notice how as the buckets get thinner, the tops of the bars start to form a smooth curve. Calculus takes this to the extreme: an infinite number of infinitely thin bars!")
        st.markdown("</div>", unsafe_allow_html=True)
       
    with col2:
        # Simulate data
        np.random.seed(42)
        data = np.random.normal(170, 7, 10000)
       
        fig = go.Figure()
       
        if bin_width > 0.5:
            # Discrete histogram
            counts, edges = np.histogram(data, bins=np.arange(130, 210 + bin_width, bin_width))
            # Normalize to density so it matches the curve
            density = counts / (counts.sum() * bin_width)
           
            fig.add_trace(go.Bar(
                x=edges[:-1] + bin_width/2,
                y=density,
                width=bin_width,
                marker_color='rgba(59, 130, 246, 0.6)',
                marker_line_color='rgba(59, 130, 246, 1)',
                marker_line_width=1,
                name="Discrete Bins"
            ))
           
        # Always show the continuous curve as a target
        x_smooth = np.linspace(130, 210, 500)
        y_smooth = norm.pdf(x_smooth, 170, 7)
        fig.add_trace(go.Scatter(
            x=x_smooth,
            y=y_smooth,
            mode='lines',
            line=dict(color='#f43f5e', width=3, dash='dash' if bin_width > 0.5 else 'solid'),
            name="Continuous Curve"
        ))
       
        # If the smallest bin width, fill the curve
        if bin_width <= 0.5:
            fig.data[0].fill = 'tozeroy'
            fig.data[0].fillcolor = 'rgba(244, 63, 94, 0.3)'
            fig.data[0].name = "Smooth Distribution"
           
        fig.update_layout(
            title="Histogram Approaching Continuous Density",
            xaxis_title="Height (cm)",
            yaxis_title="Density",
            barmode='overlay',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f8fafc'),
            margin=dict(l=20, r=20, t=40, b=20),
            showlegend=True
        )
        fig.update_xaxes(gridcolor='#334155', range=[140, 200])
        fig.update_yaxes(gridcolor='#334155')
        st.plotly_chart(fig, use_container_width=True)

def main():
    local_css()
    render_intro()
    st.divider()
    render_discrete()
    st.divider()
    render_continuous()
    st.divider()
    render_bridge()
   
    st.divider()
    st.info("💡 **Takeaway:** Discrete variables are counted, continuous variables are measured. The bridge between them is making your measuring stick infinitely precise. That's why we use sum (∑) for discrete math and integrals (∫) for continuous math!")

if __name__ == "__main__":
    main()

