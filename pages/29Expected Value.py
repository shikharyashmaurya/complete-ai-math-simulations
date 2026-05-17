import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Expected Value", layout="wide")

def local_css():
    st.markdown("""
    <style>
    .narrative-box {
        background: #1e293b;
        color: #f8fafc;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #f59e0b;
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
    .stat-box {
        text-align: center;
        padding: 15px;
        background: #1e293b;
        border-radius: 12px;
        border-top: 3px solid #6366f1;
        margin-top: 10px;
    }
    .stat-val {
        font-size: 2rem;
        font-weight: bold;
        color: #f8fafc;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .math-formula {
        font-size: 1.5rem;
        color: #fcd34d;
        text-align: center;
        font-family: monospace;
        margin: 15px 0;
        background: #1e293b;
        padding: 10px;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

def render_intro():
    st.title("Page 29: Expected Value")
    st.markdown(
        """
        <div class="narrative-box">
        <h3>The Center of Mass of Probability ⚖️</h3>
        Expected Value (<b>E[X]</b>) isn't necessarily what you "expect" to happen on any single try. It is a <i>weighted average</i>.<br><br>
        Think of it as the <b>balance point</b> or <b>center of mass</b> of a probability distribution. 
        If outcomes are positions on a seesaw, and probabilities are weights placed at those positions, the Expected Value is exactly where you must place the fulcrum to balance the universe.
        </div>
        """, unsafe_allow_html=True
    )

def render_balance_beam():
    st.header("1️⃣ The Balance Beam Playground")
    st.markdown("Adjust the relative weights (probabilities) of different outcomes. Watch how the fulcrum shifts to maintain perfect balance.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("<div class='concept-box'>", unsafe_allow_html=True)
        st.markdown("#### Adjust Weights (Relative Probability)")
        
        w1 = st.slider("Weight at x = 1", min_value=0, max_value=100, value=20)
        w2 = st.slider("Weight at x = 5", min_value=0, max_value=100, value=50)
        w3 = st.slider("Weight at x = 9", min_value=0, max_value=100, value=10)
        
        total = w1 + w2 + w3
        if total == 0:
            st.warning("Total weight cannot be zero. Resetting to uniform.")
            p1, p2, p3 = 1/3, 1/3, 1/3
        else:
            p1, p2, p3 = w1/total, w2/total, w3/total
            
        ev = 1*p1 + 5*p2 + 9*p3
        
        st.markdown(f"<br>**Calculated Expected Value:**", unsafe_allow_html=True)
        st.markdown(f"E[X] = (1 × {p1:.2f}) + (5 × {p2:.2f}) + (9 × {p3:.2f})")
        st.markdown(f"**E[X] = {ev:.2f}**")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        fig = go.Figure()
        
        # The Plank
        fig.add_shape(type="line", x0=0, y0=0, x1=10, y1=0, line=dict(color="#94a3b8", width=8))
        
        # The Fulcrum
        fig.add_trace(go.Scatter(
            x=[ev], y=[-0.08],
            mode='markers+text',
            marker=dict(symbol='triangle-up', size=40, color='#f59e0b', line=dict(color='white', width=2)),
            text=[f"E[X] = {ev:.2f}"],
            textposition='bottom center',
            textfont=dict(size=16, color='#fcd34d'),
            hoverinfo='skip'
        ))
        
        # The Weights (Bars)
        x_vals = [1, 5, 9]
        y_vals = [p1, p2, p3]
        fig.add_trace(go.Bar(
            x=x_vals, y=y_vals, width=0.6,
            marker=dict(
                color=['#3b82f6', '#10b981', '#f43f5e'],
                line=dict(color='white', width=1.5)
            ),
            text=[f"{p*100:.0f}%" for p in y_vals],
            textposition='outside',
            textfont=dict(size=14, color='white'),
            hoverinfo='none'
        ))
        
        # Dashed line from fulcrum up
        fig.add_shape(type="line", x0=ev, y0=0, x1=ev, y1=max(y_vals)+0.1, line=dict(color="#f59e0b", width=2, dash="dash"))
        
        fig.update_layout(
            title="Distribution and its Balance Point",
            xaxis=dict(range=[-0.5, 10.5], tickmode='linear', dtick=1, gridcolor='rgba(51,65,85,0.3)', title="Outcome (x)"),
            yaxis=dict(range=[-0.3, max(max(y_vals) + 0.2, 0.5)], showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f8fafc'),
            margin=dict(l=20, r=20, t=40, b=40),
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

def render_casino():
    st.header("2️⃣ Real World: The Casino's Secret")
    st.markdown("Casinos don't rely on luck. They rely on the math of Expected Value. Let's design a casino game and see who really wins in the long run.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("<div class='concept-box'>", unsafe_allow_html=True)
        cost = st.slider("Cost to Play ($)", 1, 50, 10)
        prize = st.slider("Jackpot Prize ($)", 10, 500, 100)
        win_prob = st.slider("Win Probability (%)", 1, 50, 5)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='concept-box'>", unsafe_allow_html=True)
        
        p_win = win_prob / 100.0
        p_lose = 1.0 - p_win
        
        # Player net outcome
        net_win = prize - cost
        net_lose = -cost
        
        ev = (p_win * net_win) + (p_lose * net_lose)
        
        st.markdown("<div class='math-formula'>E[X] = P(Win) × (Prize - Cost) + P(Lose) × (-Cost)</div>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"<div class='stat-box'><div class='stat-val'>+${net_win}</div><div class='stat-label'>If you win ({win_prob}%)</div></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='stat-box' style='border-top-color:#f43f5e;'><div class='stat-val' style='color:#fb7185;'>${net_lose}</div><div class='stat-label'>If you lose ({100-win_prob}%)</div></div>", unsafe_allow_html=True)
        with c3:
            border_col = "#10b981" if ev > 0 else "#f43f5e" if ev < 0 else "#94a3b8"
            text_col = "#34d399" if ev > 0 else "#fb7185" if ev < 0 else "#f8fafc"
            st.markdown(f"<div class='stat-box' style='border-top-color:{border_col};'><div class='stat-val' style='color:{text_col};'>${ev:.2f}</div><div class='stat-label'>Expected Value</div></div>", unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        if ev > 0:
            st.success("✅ **Positive EV!** The player has the edge. The casino will go bankrupt offering this game.")
        elif ev < 0:
            st.error("❌ **Negative EV!** The house has the edge. You will lose money in the long run. (This is how real casinos work!)")
        else:
            st.info("⚖️ **Zero EV!** A perfectly fair game. Nobody makes money in the long run.")
            
        st.markdown("</div>", unsafe_allow_html=True)

def render_ai_connection():
    st.header("3️⃣ Why AI Cares")
    st.markdown("""
    <div class="concept-box" style="border-left: 5px solid #8b5cf6;">
    In AI and Machine Learning, Expected Value is everywhere:
    <ul>
        <li><b>Loss Functions:</b> When training a neural network, the "Loss" is literally an Expected Value (the average error over the training data). Gradient descent minimizes this expected error.</li>
        <li><b>Reinforcement Learning:</b> Agents (like AlphaGo or autonomous cars) learn by maximizing the <i>Expected Future Reward</i> of their actions.</li>
        <li><b>Probabilistic Models:</b> When an AI is uncertain, it predicts a probability distribution. The final chosen answer is often just the Expected Value of that distribution!</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

def main():
    local_css()
    render_intro()
    st.divider()
    render_balance_beam()
    st.divider()
    render_casino()
    st.divider()
    render_ai_connection()
    
    st.divider()
    st.info("💡 **Takeaway:** Expected Value is the mathematical center of mass. It tells you what happens on average over the long run, and it's the foundation for making optimal decisions in casinos and AI.")

if __name__ == "__main__":
    main()
